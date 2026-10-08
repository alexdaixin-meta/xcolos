"""A record of every model call, so what the models were asked and what they said can be read afterwards.

Each call is written twice: one line in `calls.jsonl`, and a page `NN-step.md` with the prompt (or the whole
conversation) and the reply. The system prompts are long and repeat, so each is written once under `system/`
and the call carries its hash. Every prompt and reply also carries a sha256, so a prompt that was saved
elsewhere (the coder's `CODER_PROMPT.md`) can be shown to be exactly the one that was sent.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

#: What each step is called in the log, from how its system prompt starts.
STEPS = (
    ("You are a game designer", "design"),
    ("You are a strict reviewer", "critic"),
    ("You convert a game's rules", "spec"),
    ("You write test scenarios", "scenarios"),
    ("You write game files", "coder"),
    ("A game design for XColos", "triage"),
)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def step_of(system: str) -> str:
    return next((name for prefix, name in STEPS if system.startswith(prefix)), "other")


class Recorded:
    """Wraps a model and records each call. Put it outside any retrying wrapper, so a call that was retried is
    one entry, with the time it took."""

    def __init__(self, inner, folder: Path):
        self.inner = inner
        self.folder = Path(folder)
        self.count = len(list(self.folder.glob("[0-9][0-9]-*.md"))) if self.folder.exists() else 0
        self._now: dict | None = None
        # a model that reports its own progress (Muse's background polls) is shown in current.json while a call is open
        x = inner
        for _ in range(3):
            if x is not None and hasattr(type(x), "on_status"):
                x.on_status = self._progress
                break
            x = getattr(x, "inner", None)

    def __getattr__(self, name):
        if name == "converse":
            inner = getattr(self.inner, "converse")  # AttributeError when the model cannot converse
            return lambda messages, system="": self._record(system, messages, lambda: inner(messages, system=system))
        return getattr(self.inner, name)

    def complete(self, prompt: str, system: str = "") -> str:
        return self._record(system, prompt, lambda: self.inner.complete(prompt, system=system))

    def _progress(self, info: dict) -> None:
        if self._now is not None:
            self._now.update(info)
            self._write_current()

    def _write_current(self) -> None:
        self.folder.mkdir(parents=True, exist_ok=True)
        now = dict(self._now or {})
        now["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        (self.folder / "current.json").write_text(json.dumps(now, indent=2) + "\n")

    def _record(self, system: str, sent, call):
        started, t0, error, reply = datetime.now(timezone.utc), time.time(), "", ""
        self._now = {"state": "waiting for the model", "call": self.count + 1, "step": step_of(system),
                     "started": started.isoformat(timespec="seconds"), "sent_chars": len(sent if isinstance(sent, str) else json.dumps(sent))}
        self._write_current()
        try:
            reply = call()
            return reply
        except Exception as exc:  # noqa: BLE001 - recorded, then raised again unchanged
            error = f"{type(exc).__name__}: {str(exc)[:300]}"
            raise
        finally:
            self._write(system, sent, reply, error, started, time.time() - t0)
            self._now = {"state": "idle: last call " + ("failed" if error else "finished"), "call": self.count, "step": step_of(system),
                         "seconds": round(time.time() - t0, 1), "error": error}
            self._write_current()

    def _write(self, system, sent, reply, error, started, seconds) -> None:
        self.count += 1
        step = step_of(system)
        (self.folder / "system").mkdir(parents=True, exist_ok=True)
        sys_hash = sha(system)
        sys_file = self.folder / "system" / f"{sys_hash[:8]}-{step}.md"
        if not sys_file.exists():
            sys_file.write_text(system)
        text = sent if isinstance(sent, str) else json.dumps(sent, indent=2)
        entry = {
            "n": self.count, "step": step, "at": started.isoformat(timespec="seconds"), "seconds": round(seconds, 1),
            "model": getattr(self.inner, "model", "") or getattr(getattr(self.inner, "inner", None), "model", ""),
            "kind": "conversation" if not isinstance(sent, str) else "single",
            "system_sha256": sys_hash, "system_file": f"system/{sys_file.name}",
            "sent_sha256": sha(text), "reply_sha256": sha(reply), "sent_chars": len(text), "reply_chars": len(reply), "error": error,
        }
        with (self.folder / "calls.jsonl").open("a") as fh:
            fh.write(json.dumps(entry) + "\n")
        page = [f"# {self.count:02d} {step}", "", f"- time: {entry['at']} ({entry['seconds']}s)  model: {entry['model']}",
                f"- system prompt: [{entry['system_file']}]({entry['system_file']}) (sha256 {sys_hash[:16]})",
                f"- sent sha256 {entry['sent_sha256'][:16]}, reply sha256 {entry['reply_sha256'][:16]}"]
        if error:
            page.append(f"- ERROR: {error}")
        page += ["", "## Sent" if isinstance(sent, str) else "## Sent (the whole conversation)", "", "````", text, "````", "", "## Reply", "", "````", reply, "````", ""]
        (self.folder / f"{self.count:02d}-{step}.md").write_text("\n".join(page))
