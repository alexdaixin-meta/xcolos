"""Who writes the game file: a model answering in a loop, or a coding agent with tools.

Both are an *encoder*: given a spec, the final rules and any guidance, it produces `game.json` and
reports back. The pipeline never trusts what an encoder says about its own work. Whatever it
returns, `game.json` is checked again here by the loader, the arithmetic-outcome rule and smoke play.

  CompletionEncoder  one model, asked for the whole file, repaired from the checks' complaints
  AgentEncoder       a coding agent (Muse's `muse exec`, MetaCode, or Claude Code) run non-interactively in the
                     repository with the prompt in `prompt.py`; it reads the platform's docs, writes
                     the file and runs `verify` itself until it passes
"""

from __future__ import annotations

import shlex
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from gen_game import encode as enc
from gen_game import prompt as promptmod

ROOT = Path(__file__).resolve().parent.parent

#: The coding agents' command lines. `{workspace}` is the repository, `{prompt_file}` the file the prompt was
#: written to. A command with `{prompt_file}` is given the file; any other gets the prompt on stdin.
#:
#:   claude    Claude Code in print mode (prompt on stdin); edits are auto-accepted, and it may read, write and run commands.
#:   muse      `muse exec`, Muse's headless coding agent, which is what `metacode run` is now redirected to. It takes no
#:             stdin and no timeout, so the prompt is a file and the time limit is ours. `--yolo` is what lets it write files
#:             and run `verify` without asking: it approves everything, inside the workspace. Run it yourself, in a terminal.
#:   metacode  `metacode run` (native), with the prompt on stdin. On hosts where it has been redirected to `muse exec` it
#:             rejects stdin: use `muse` there.
#:
#: Run from inside another sandbox (as this was built), the macOS launchers fail with `sandbox-exec: Operation not
#: permitted` and need `--dangerously-disable-osx-sandbox`. That is a security decision, so it is never added here:
#: put it in a `command:` agent yourself if you want it. None of these commands has been run by the author.
AGENT_COMMANDS = {
    "claude": ["claude", "-p", "--permission-mode", "acceptEdits", "--allowedTools", "Read", "Write", "Edit", "Bash"],
    "muse": ["muse", "exec", "--yolo", "--workspace", "{workspace}", "--max-model-steps", "80", "--prompt-file", "{prompt_file}"],
    "metacode": ["metacode", "run", "--format", "text", "--yolo", "--dir", "{workspace}"],
}
#: Where a `--model` goes in each: after the command word(s), before everything else.
MODEL_AT = {"claude": 1, "muse": 2, "metacode": 2}


@dataclass
class AgentResult:
    ok: bool
    text: str = ""
    error: str = ""


class CommandAgent:
    """Run a program with the prompt on stdin, or as a file it is told the path of, in the repository."""

    def command_line(self, prompt_file: Path | None = None) -> list[str]:
        """The command exactly as `run` would execute it, with the placeholders filled in."""
        argv = [a.replace("{workspace}", str(self.cwd)) for a in self.argv]
        if prompt_file is not None:
            argv = [a.replace("{prompt_file}", str(prompt_file)) for a in argv]
        return argv

    def __init__(self, argv: list[str], timeout_s: int = 2400, cwd: Path = ROOT):
        self.argv = list(argv)
        self.timeout_s = timeout_s
        self.cwd = cwd

    def run(self, prompt: str, prompt_file: Path | None = None) -> AgentResult:
        argv = [a.replace("{workspace}", str(self.cwd)) for a in self.argv]
        wants_file = any("{prompt_file}" in a for a in argv)
        if wants_file:
            if prompt_file is None:
                import tempfile

                prompt_file = Path(tempfile.mkdtemp()) / "AGENT_PROMPT.md"
            prompt_file.write_text(prompt)
            argv = [a.replace("{prompt_file}", str(prompt_file)) for a in argv]
        try:
            # with a prompt file the agent must not wait on stdin, so it is closed rather than inherited
            feed = {"stdin": subprocess.DEVNULL} if wants_file else {"input": prompt}
            done = subprocess.run(argv, capture_output=True, text=True, timeout=self.timeout_s, cwd=self.cwd, **feed)
        except FileNotFoundError:
            return AgentResult(False, error=f"no such command: {argv[0]}")
        except subprocess.TimeoutExpired:
            return AgentResult(False, error=f"{argv[0]} did not finish in {self.timeout_s}s")
        if done.returncode != 0:
            return AgentResult(False, done.stdout, f"{argv[0]} exited {done.returncode}: {(done.stderr or done.stdout).strip()[-300:]}")
        return AgentResult(True, done.stdout)


def agent_for(spec: str, effort: str | None = None) -> CommandAgent:
    """`claude[:model]`, `muse[:model]`, `metacode[:model]`, or `command:<program and arguments>`.

    `effort` is Muse's reasoning effort (`--reasoning-effort`); the other agents have no such flag here.
    """
    kind, _, rest = spec.partition(":")
    kind = kind.strip().lower()
    if kind in AGENT_COMMANDS:
        argv = list(AGENT_COMMANDS[kind])
        extra = (["--model", rest.strip()] if rest.strip() else []) + (["--reasoning-effort", effort] if effort and kind == "muse" else [])
        at = MODEL_AT[kind]
        return CommandAgent(argv[:at] + extra + argv[at:])
    if kind == "command" and rest.strip():
        return CommandAgent(shlex.split(rest))
    raise ValueError(f"unknown agent {spec!r}; expected claude[:model], muse[:model], metacode[:model] or command:<program>")


@dataclass
class Built:
    game: dict | None = None
    definition: object | None = None
    #: What was wrong with each attempt ('' for the one that passed), or the agent's own failure.
    attempts: list[str] = field(default_factory=list)
    #: What the encoder said about ambiguities and limits (an agent's `encode_notes.md`).
    notes: str = ""

    @property
    def ok(self) -> bool:
        return self.definition is not None


class CompletionEncoder:
    def __init__(self, completion, pause=time.sleep):
        self.completion = completion
        self.pause = pause  # how a dropped connection is waited out; tests pass a no-op

    def build(self, game_id: str, spec: dict, plan: dict | None, folder: Path, guidance: str = "", tests: list[dict] | None = None) -> Built:
        # the same generated prompt an agent gets, kept on disk, with the API put in the system prompt instead of read from files
        text = promptmod.build(game_id, plan, spec, guidance, agent=False) if plan else None
        if text is not None:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "CODER_PROMPT.md").write_text(text)
        got = enc.encode(self.completion, spec, game_id, guidance=guidance, pause=self.pause, tests=tests, prompt_text=text)
        return Built(got.game, got.definition, got.attempts)


class AgentEncoder:
    def __init__(self, agent):
        self.agent = agent

    def build(self, game_id: str, spec: dict, plan: dict, folder: Path, guidance: str = "", tests: list[dict] | None = None) -> Built:
        """`tests` are not given to the agent (it must not see them); the pipeline runs them on what it wrote."""
        folder.mkdir(parents=True, exist_ok=True)
        for stale in ("game.json", "encode_notes.md"):
            (folder / stale).unlink(missing_ok=True)
        prompt = promptmod.build(game_id, plan, spec, guidance)
        (folder / "AGENT_PROMPT.md").write_text(prompt)
        run = self.agent.run(prompt, prompt_file=folder / "AGENT_PROMPT.md")
        (folder / "logs").mkdir(exist_ok=True)
        (folder / "logs" / "agent_output.md").write_text(f"# What the coding agent printed\n\nok: {run.ok}\n\nerror: {run.error}\n\n````\n{run.text}\n````\n")
        notes = (folder / "encode_notes.md").read_text() if (folder / "encode_notes.md").exists() else ""
        if not run.ok:
            return Built(None, None, [f"the coding agent failed: {run.error}"], notes)
        path = folder / "game.json"
        if not path.exists():
            return Built(None, None, ["the coding agent finished without writing game.json"], notes)
        # the agent's own word that it passed counts for nothing: check the file here
        obj, defn, problem = enc.check(path.read_text(), game_id, set(spec.get("parameters", {})))
        return Built(obj, defn, [problem], notes)
