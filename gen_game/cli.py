"""Command line for gen_game.

    python3 -m gen_game convert ID --model SPEC [--encoder claude|metacode|command:...] [--redo spec,encode,scenarios]
    python3 -m gen_game evaluate ID           tiers 0 and 1 on an existing game.json
    python3 -m gen_game show ID               the report
    python3 -m gen_game verify ID variation|spec|game|scenarios   check a file written by hand or by an agent
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from gen_game import evaluate, flow
from gen_inventory.inventory import DEFAULT_DIR, Inventory
from xcolos.games.loader import load


#: The Muse model gen_game writes games with. The platform's default (1-1) is a playground model that
#: sheds load with 503s for long stretches, and the 1-3 model is slow and drops the connection. The 1-2
#: model answered a 10,000-character generation in 25 to 45 seconds at every reasoning effort. Models are
#: granted per key: `MuseCompletion().models()` lists what a key holds.
MUSE_MODEL = "rl-muse-spark-1-2-playground"


class Patient:
    """A model that is asked again when the connection fails, with waits that grow.

    Every step (design, spec, encode, scenarios) is one long generation, and a connection to
    a model sometimes closes in the middle of one or is shed with a 503. That says nothing about
    the game, so it is retried here, once, for all of them, before a step sees an error.
    """

    def __init__(self, inner, retries: int = 4, pause=None):
        import time

        self.inner = inner
        self.retries = retries
        self.pause = pause or time.sleep

    def __getattr__(self, name):  # model, command and the rest are the inner model's
        if name == "converse":
            # offered only when the model can hold a conversation, so callers can ask with hasattr(); retried like complete()
            inner = getattr(self.inner, "converse")  # AttributeError when it cannot
            return lambda messages, system="": self._patiently(lambda: inner(messages, system=system))
        return getattr(self.inner, name)

    def _patiently(self, call):
        for attempt in range(self.retries + 1):
            try:
                return call()
            except Exception:  # noqa: BLE001 - whatever the backend raised, it is the backend's trouble
                if attempt == self.retries:
                    raise
                self.pause(10 * 2 ** attempt)  # 10, 20, 40, 80 seconds

    def complete(self, prompt: str, system: str = "") -> str:
        return self._patiently(lambda: self.inner.complete(prompt, system=system))



def completion_for(spec: str, effort: str):
    """The model for a backend spec. Muse gets a reasoning effort and room for a whole game file:
    the platform's default (minimal effort, 8192 output tokens) suits a referee, not an author."""
    from xcolos.flow.backends import from_spec

    kind, _, rest = spec.partition(":")
    if kind.strip().lower() == "claude":
        # The `claude` CLI in print mode, through the platform's command adapter: prompt on stdin, reply on
        # stdout, no API key to handle. `claude`, or `claude:<model>`.
        from xcolos.flow.backends import CommandCompletion

        model = rest.strip() or "claude-opus-5-5"
        return Patient(CommandCompletion(["claude", "-p", "--model", model], timeout_s=1800))
    if kind.strip().lower() == "muse":
        from gen_game.chat import MuseChat

        # a request that has not answered in 3 minutes is hung (a 10,000-character generation takes 25 to 45 seconds): cut it and ask again
        return Patient(MuseChat(model=rest.strip() or MUSE_MODEL, reasoning_effort=effort, max_output_tokens=16384, timeout_s=180))
    return from_spec(spec)


def install_command(args) -> int:
    """Put a game that works on the platform into the platform's library so it can be played in the console, or take it out.

    Only a file that passes the infrastructure checks is installed, the platform must load the whole library afterwards, and a
    different game with the same id is never overwritten. The server reads the library when it starts, so restart it.
    """
    from gen_game import encode as enc
    from xcolos.games import loader

    library = args.library or loader.LIBRARY
    target = library / f"{args.id}.json"
    if args.cmd == "uninstall":
        if not target.exists():
            print(f"{args.id} is not installed ({target} does not exist)")
            return 1
        target.unlink()
        print(f"removed {target}\nrestart the server to drop it from the picker")
        return 0
    source = args.root / args.id / "game.json"
    text = source.read_text()
    spec = json.loads((args.root / args.id / "spec.json").read_text()) if (args.root / args.id / "spec.json").exists() else {}
    _, defn, problem = enc.check(text, args.id, set(spec.get("parameters", {})))
    if defn is None:
        print(f"not installed: the game does not pass the platform checks: {problem}", file=sys.stderr)
        return 1
    if target.exists() and json.loads(target.read_text()) != json.loads(text):
        print(f"not installed: {target} already holds a different game with this id; remove it first with `uninstall`", file=sys.stderr)
        return 1
    existed = target.exists()
    target.write_text(text)
    try:
        loaded = loader.available() if library == loader.LIBRARY else {p.stem: loader.load_file(p) for p in library.glob("*.json")}
    except Exception as exc:  # noqa: BLE001 - the library must keep loading, whatever this file did to it
        if not existed:
            target.unlink()
        print(f"not installed: the platform could not load the library with it: {exc}", file=sys.stderr)
        return 1
    print(f"installed {target}\n  the platform loads it: {defn.name}, {defn.min_players} to {defn.max_players} players\n"
          f"  library now holds: {', '.join(sorted(loaded))}\n  restart the server to play it:  python3 -m xcolos.web --port 8000")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="gen_game", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inventory", type=Path, default=DEFAULT_DIR, help="gen_inventory's directory")
    ap.add_argument("--root", type=Path, default=flow.DATA, help="where converted games are kept")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("convert")
    p.add_argument("id")
    p.add_argument("--model", required=True, help="a backend spec: claude[:model], muse[:model], anthropic[:model], command:<program>, echo:<reply>")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"),
                   help="Muse reasoning effort for the conversion (default: medium)")
    p.add_argument("--encoder", default="completion",
                   help="who writes the game file: `completion` (the --model, in a repair loop), or a coding agent: "
                        "claude[:model], metacode[:model], command:<program>")
    p.add_argument("--judge", action="store_true",
                   help="also review the design with a critic and balance checks, revise it, and drop games that fail them (default: no quality gates)")
    p.add_argument("--no-adapt", action="store_true", help="the entry is finished rules: convert them as written, with no design step")
    p.add_argument("--design-feedback", default="", help="what is already known to be wrong with an earlier design, as text, or @path to a file; the designer reads it first")
    p.add_argument("--rounds", type=int, default=flow.DESIGN_ROUNDS, help="how many variations to try when the evaluation finds a design flaw")
    p.add_argument("--redo", default="", help=f"steps to run again, from: {', '.join(flow.STEPS)}")
    p = sub.add_parser("verify")
    p.add_argument("id")
    p.add_argument("what", choices=("variation", "spec", "game", "scenarios", "rules"),
                   help="check variation.json, spec.json, game.json (loader and smoke play), scenarios.json against the pipeline's own rules, "
                        "or play game.json through the design's rule scenarios (`rules`)")
    p = sub.add_parser("agent-command")
    p.add_argument("id")
    p.add_argument("--encoder", default="muse", help="claude[:model], muse[:model], metacode[:model] or command:...")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"))
    for name in ("install", "uninstall"):
        q = sub.add_parser(name)
        q.add_argument("id")
        q.add_argument("--library", type=Path, default=None, help="the platform's game library (default: xcolos/games/library)")
    sub.add_parser("status").add_argument("id")
    sub.add_parser("verified").add_argument("id")
    for name in ("evaluate", "show"):
        sub.add_parser(name).add_argument("id")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "convert":
            redo = tuple(s for s in args.redo.split(",") if s)
            bad = [s for s in redo if s not in flow.STEPS]
            if bad:
                print(f"error: unknown step(s) {', '.join(bad)}", file=sys.stderr)
                return 1
            from gen_game.agent import AgentEncoder, CompletionEncoder, agent_for

            from gen_game.calls import Recorded

            # every model call is recorded under <game>/logs, outside the retrying wrapper so a retried call is one entry
            completion = Recorded(completion_for(args.model, args.effort), args.root / args.id / "logs")
            encoder = CompletionEncoder(completion) if args.encoder == "completion" else AgentEncoder(agent_for(args.encoder, args.effort))
            from gen_game import status as runstatus

            runstatus.started(args.root / args.id / "logs")
            try:
                out = flow.convert(args.id, completion, Inventory(args.inventory), args.root, redo,
                                   log=lambda m: print(m, flush=True), adapt=not args.no_adapt, judge=args.judge, design_rounds=args.rounds, encoder=encoder,
                                   design_feedback=(Path(args.design_feedback[1:]).read_text() if args.design_feedback.startswith("@") else args.design_feedback))
            except BaseException as exc:
                runstatus.ended(args.root / args.id / "logs", "crashed", f"{type(exc).__name__}: {str(exc)[:300]}")
                raise
            runstatus.ended(args.root / args.id / "logs", out.verdict, out.detail)
            print(f"\n{args.id}: {out.verdict.replace('_', ' ')}" + (f"\n  {out.detail}" if out.detail else ""))
            print(f"  {args.root / args.id}")
            from gen_game import verified

            if (args.root / args.id / "logs").exists():
                print(f"  {verified.write(args.root / args.id)}")
            return 0 if out.verdict == "ready_for_review" else 2
        if args.cmd == "verify":
            from gen_game import encode as enc
            from gen_game import scenarios

            folder = args.root / args.id
            if args.what in ("variation", "spec"):
                from gen_game import adapt as adaptmod
                from gen_game import spec as specmod

                data = json.loads((folder / f"{args.what}.json").read_text())
                found = (adaptmod.problems(data) if args.what == "variation" else specmod.problems(data))
                print("ok" if not found else "; ".join(found))
                return 0 if not found else 1
            if args.what == "game":
                # the spec's parameters are meant to stay constant, so they are not "dead": the same rule the flow applies
                spec_path = folder / "spec.json"
                constants = set(json.loads(spec_path.read_text()).get("parameters", {})) if spec_path.exists() else set()
                _, defn, problem = enc.check(json.loads((folder / "game.json").read_text()), args.id, constants)
                print("ok" if defn else problem)
                if defn:
                    from gen_game import complexity, lint

                    for finding in lint.trace_lint(defn, seeds=range(1, 3))["findings"][:6]:
                        print(f"note: {finding}")

                    steps = complexity.measure(defn)["steps_per_round"]
                    if steps > complexity.LIMITS["steps_per_round"]:
                        print(f"note: the round has {steps} steps, over the guideline of {complexity.LIMITS['steps_per_round']}; "
                              "the report will flag it. Merge steps that always run together, or give a step a `when`.")
                return 0 if defn else 1
            if args.what == "rules":
                from xcolos.games.loader import load_file

                if not (folder / "scenarios.json").exists():
                    print("no rule scenarios have been written yet; nothing to check")
                    return 0
                items = json.loads((folder / "scenarios.json").read_text())
                results = scenarios.run_all(load_file(folder / "game.json"), items)
                bad = [o for o in results if not o.passed]
                print(f"ok: the game plays all {len(results)} rule scenarios" if not bad else
                      f"{len(bad)} of {len(results)} rule scenarios fail:\n" + "\n".join(f"- {o.name}: " + "; ".join(o.failures[:5]) for o in bad))
                return 0 if not bad else 1
            found = scenarios.problems(json.loads((folder / "scenarios.json").read_text()))
            print("ok" if not found else "; ".join(found))
            return 0 if not found else 1
        if args.cmd == "agent-command":
            import shlex

            from gen_game import prompt as promptmod
            from gen_game.agent import agent_for

            folder = args.root / args.id
            plan = json.loads((folder / "variation.json").read_text())
            spec = json.loads((folder / "spec.json").read_text())
            (folder / "AGENT_PROMPT.md").write_text(promptmod.build(args.id, plan, spec))
            a = agent_for(args.encoder, args.effort)
            file = folder / "AGENT_PROMPT.md"
            uses_file = any("{prompt_file}" in x for x in a.argv)
            cmd = shlex.join(a.command_line(file if uses_file else None))
            print(f"prompt written to {file}\n\nrun this in a terminal (outside Claude Code):\n\n  cd {a.cwd} && " +
                  (cmd if uses_file else f"{cmd} < {file}") +
                  f"\n\nwhen it finishes, check what it wrote:\n\n  cd {a.cwd} && python3 -m gen_game verify {args.id} game")
            return 0
        if args.cmd in ("install", "uninstall"):
            return install_command(args)
        if args.cmd == "status":
            from gen_game import status as runstatus

            print(runstatus.describe(args.root / args.id))
            return 0
        if args.cmd == "verified":
            from gen_game import verified

            print(verified.write(args.root / args.id))
            return 0
        if args.cmd == "evaluate":
            defn = load((args.root / args.id / "game.json").read_text(), source=args.id)
            print(json.dumps({"tier0": evaluate.tier0(defn), "tier1": evaluate.tier1(defn)}, indent=2))
        elif args.cmd == "show":
            print((args.root / args.id / "REPORT.md").read_text())
    except (OSError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0
