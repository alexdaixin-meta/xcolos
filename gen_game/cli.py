"""Command line for gen_game.

    python3 -m gen_game convert ID --model SPEC [--encoder claude|metacode|command:...] [--redo spec,encode,scenarios]
    python3 -m gen_game evaluate ID           tiers 0 and 1 on an existing game.json
    python3 -m gen_game show ID               the report
    python3 -m gen_game verify ID variation|spec|game|scenarios   check a file written by hand or by an agent
"""

from __future__ import annotations

import os

import argparse
import json
import sys
import time
from pathlib import Path

from gen_game import evaluate, flow
from gen_inventory.inventory import DEFAULT_DIR, Inventory
from xcolos.games.loader import load


#: The Muse model gen_game writes games with. The platform's default (1-1) is a playground model that
#: sheds load with 503s for long stretches, and the 1-3 model is slow and drops the connection. The 1-2
#: model answered a 10,000-character generation in 25 to 45 seconds at every reasoning effort. Models are
#: granted per key: `MuseCompletion().models()` lists what a key holds.
MUSE_MODEL = os.environ.get("XCOLOS_MUSE_MODEL", "").strip() or "rl-muse-spark-1-3-sglang-playground"  # the newest; 1-1 and 1-2 shed load or crawl on some days


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
        return Patient(CommandCompletion(["claude", "-p", "--bare", "--model", model], timeout_s=1800))
    if kind.strip().lower() == "muse":
        from gen_game.chat import MuseChat

        # a request that has not answered in 3 minutes is hung (a 10,000-character generation takes 25 to 45 seconds): cut it and ask again
        return Patient(MuseChat(model=rest.strip() or MUSE_MODEL, reasoning_effort=effort, max_output_tokens=16384, timeout_s=180))
    return from_spec(spec)


def loop_command(args) -> int:
    """Wire the loop's rules (gen_game/loop.py) to the real play, review, verifier, spec revision and generator."""
    import types

    from gen_game import loop as loopmod
    from gen_game import playreview, revise as revisemod
    from gen_game import simulate as sim
    from gen_game.agent import AgentEncoder, CompletionEncoder, agent_for
    from gen_game.calls import Recorded

    folder = args.root / args.id
    inv = Inventory(args.inventory)
    players = [x.strip() for x in args.players.split(",") if x.strip()]
    reviewer = completion_for(args.review_model, args.effort)
    state = {"pass": 0}

    def say(message: str) -> None:
        print(message, flush=True)

    def append(name: str):
        def write(text: str) -> None:
            with open(folder / name, "a") as out:
                out.write(f"\n{time.strftime('%Y-%m-%d %H:%M')} {text}\n")
        return write

    def install() -> None:
        """Make the library hold the current game.json; an installed copy that cannot be replaced is put back."""
        from xcolos.games import loader

        target = loader.LIBRARY / f"{args.id}.json"
        source = folder / "game.json"
        before = target.read_text() if target.exists() else None
        if before is not None and json.loads(before).get("meta") == json.loads(source.read_text()).get("meta") and json.loads(before) == json.loads(source.read_text()):
            return
        ns = types.SimpleNamespace(id=args.id, root=args.root, library=None, cmd="uninstall")
        if before is not None:
            install_command(ns)
        ns.cmd = "install"
        if install_command(ns) != 0:
            if before is not None:
                target.write_text(before)
            raise SystemExit("the game could not be installed, so the loop stopped (the previous copy was left in place)")

    def play() -> list[str]:
        state["pass"] += 1
        done = sim.simulate(args.id, players, args.root, matches=args.plays, seed=args.seed + 100 * (state["pass"] - 1), timeout_s=args.timeout, log=say)
        return [d["file"] for d in done]

    def review(path: str) -> dict:
        simulated = playreview.load_sim(Path(path))
        design = json.loads((folder / "variation.json").read_text())
        spec = json.loads((folder / "spec.json").read_text())
        found, error = playreview.review_play(reviewer, simulated, inv.get(args.id).rules_text, design, spec)
        if found is None:  # a reviewer that cannot answer is a problem with the tools, which a person decides about
            return {"findings": [{"where": "the review", "observed": f"the reviewer could not review the play: {error}", "expected": "a review",
                                  "category": "infra", "severity": "major", "fix": "check the reviewer model and its limits"}]}
        out = Path(path).with_suffix(".review.json")
        out.write_text(json.dumps(found, indent=1))
        Path(path).with_suffix(".review.md").write_text(playreview.render(found, simulated, design["variation"]["name"]))
        return found

    def confirm(path: str, finding: dict):
        return playreview.confirm(reviewer, playreview.load_sim(Path(path)), finding, json.loads((folder / "spec.json").read_text()))

    def judge(paths: list[str], reviews: list[dict], findings: list[dict]):
        design = json.loads((folder / "variation.json").read_text())
        out = playreview.judge(reviewer, [playreview.load_sim(Path(p)) for p in paths], reviews, findings, inv.get(args.id).rules_text, design)
        if out is not None:
            (folder / "sim" / f"judge-{state['pass']}.json").write_text(json.dumps(out, indent=1))
        return out

    def prepare_redesign(findings: list[dict]):
        """The design is revised first, from the idea, the design as it stands and the findings; the spec, scenarios and game are then rebuilt from it."""
        state["feedback"], keep = revisemod.prepare_redesign(folder, findings, state["pass"])
        return True, f"the design goes back to the designer with {len(findings)} finding(s); the earlier version is kept in {keep.name}"

    def regenerate() -> str:
        completion = Recorded(completion_for(args.model, args.effort), folder / "logs")
        encoder = CompletionEncoder(completion) if args.encoder == "completion" else AgentEncoder(agent_for(args.encoder, args.effort))
        # adapt first: a new design means a new spec, new scenarios and a new game file, so nothing downstream is left from the old one
        out = flow.convert(args.id, completion, inv, args.root, ("adapt",), log=say, adapt=True, check_brief=True, encoder=encoder, design_feedback=state["feedback"])
        install()
        return out.verdict

    if not (folder / "game.json").exists():  # a game that has not been generated yet is generated first, with the same rules-text check the iterations use
        completion = Recorded(completion_for(args.model, args.effort), folder / "logs")
        encoder = CompletionEncoder(completion) if args.encoder == "completion" else AgentEncoder(agent_for(args.encoder, args.effort))
        say(f"{args.id} has not been generated: generating it first")
        first = flow.convert(args.id, completion, inv, args.root, (), log=say, adapt=True, check_brief=True, encoder=encoder)
        say(f"generated: {first.verdict}" + (f" ({first.detail})" if first.detail else ""))
        if not (folder / "game.json").exists():
            raise SystemExit("no game file was produced, so there is nothing to play: see the generation log above")
    install()
    result = loopmod.run_loop(loopmod.Hooks(play, review, confirm, prepare_redesign, regenerate, append("LOOP_LOG.md"), append("ESCALATIONS.md"), say, judge), args.max_iterations)
    say(f"\nloop {result.status} after {result.iterations} iteration(s); log {folder / 'LOOP_LOG.md'}")
    if result.escalated:
        say(f"needs your review: {folder / 'ESCALATIONS.md'}")
    if result.unconfirmed:
        say(f"{len(result.unconfirmed)} critical/major finding(s) nothing confirmed: see the log")
    return 0 if result.status == "clean" else 2


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
    obj, defn, problem = enc.check(text, args.id, set(spec.get("parameters", {})), players=spec.get("players"))
    if defn is None:
        print(f"not installed: the game does not pass the platform checks: {problem}", file=sys.stderr)
        return 1
    text = json.dumps(obj, indent=2) + "\n"  # the checked file: the table size is the spec's, written in by the check
    if target.exists() and json.loads(target.read_text()) != obj:
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
    p.add_argument("--check-brief", action="store_true", help="also have a model check that the rules text players read says what each numbered rule says; gaps go back to the coder")
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
    p = sub.add_parser("simulate", help="play an installed game with a model in every seat, through the server, and save the full logs")
    p.add_argument("id")
    p.add_argument("--players", required=True, help="one model per seat, comma separated: claude[:model], muse[:model], anthropic[:model], command:..., offline")
    p.add_argument("--matches", type=int, default=1)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--server", default=None, help="a running server's URL (default: start one on a free port for this run)")
    p.add_argument("--timeout", type=int, default=7200, help="seconds to wait for one match")
    p = sub.add_parser("review", help="read a simulated play against the idea, the design, the spec and the prompt, and say what is aligned and what is not")
    p.add_argument("id")
    p.add_argument("--sim", type=Path, default=None, help="a saved play (default: the newest under <game>/sim/)")
    p.add_argument("--model", default="muse", help="the reviewer: muse[:model], claude[:model], anthropic[:model]")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"))
    p = sub.add_parser("revise", help="revise the spec from a play review's findings, so the coder is told what it got wrong")
    p.add_argument("id")
    p.add_argument("--review", type=Path, default=None, help="a saved review (default: the newest under <game>/sim/)")
    p.add_argument("--drop", default="", help="finding ids a person judged wrong, comma separated, e.g. F5")
    p.add_argument("--model", default="muse")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"))
    p = sub.add_parser("brief", help="check that the rules text players read says what the spec's numbered rules say")
    p.add_argument("id")
    p.add_argument("--model", default="muse")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"))
    p = sub.add_parser("loop", help="play the installed game with real models at its suggested size, review it, and loop back to the generator for confirmed critical and major findings")
    p.add_argument("id")
    p.add_argument("--players", default="muse", help="the model for the seats: one name fills the table to the game's suggested size, or a comma-separated list (muse, claude, offline...)")
    p.add_argument("--plays", type=int, default=2, help="plays per iteration, at different seeds")
    p.add_argument("--max-iterations", type=int, default=3)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--review-model", default="claude", help="reviews each play and verifies each finding")
    p.add_argument("--model", default="claude", help="the generator's model (design, spec, scenarios, triage) when the loop goes back to it")
    p.add_argument("--encoder", default="claude", help="who writes the game file when the loop goes back to the generator")
    p.add_argument("--effort", default="medium", choices=("minimal", "low", "medium", "high"))
    p.add_argument("--timeout", type=int, default=3600, help="seconds to wait for one play")
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
                                   log=lambda m: print(m, flush=True), adapt=not args.no_adapt, judge=args.judge, check_brief=args.check_brief, design_rounds=args.rounds, encoder=encoder,
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
                _, defn, problem = enc.check(json.loads((folder / "game.json").read_text()), args.id, constants,
                                             players=json.loads(spec_path.read_text()).get("players") if spec_path.exists() else None)
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
        if args.cmd == "loop":
            return loop_command(args)
        if args.cmd == "brief":
            from gen_game import brief as briefmod
            from xcolos.games.loader import load_file

            folder = args.root / args.id
            defn = load_file(folder / "game.json")
            spec = json.loads((folder / "spec.json").read_text())
            gaps, error = briefmod.check_brief(completion_for(args.model, args.effort), spec, defn.rules_text)
            if error:
                print(f"could not check: {error}")
                return 1
            print("the rules text covers every numbered rule" if not gaps else f"{len(gaps)} gap(s) in the rules text:\n" + briefmod.as_text(gaps))
            return 0 if not gaps else 1
        if args.cmd == "revise":
            from gen_game import revise as revisemod

            folder = args.root / args.id
            path = args.review or max((folder / "sim").glob("*.review.json"), key=lambda f: f.stat().st_mtime)
            review = json.loads(path.read_text())
            spec = json.loads((folder / "spec.json").read_text())
            drop = tuple(x.strip() for x in args.drop.split(",") if x.strip())
            revised, change, error = revisemod.revise_spec(completion_for(args.model, args.effort), spec, review, drop)
            if revised is None:
                print(f"no revision: {error}")
                return 1
            backup = revisemod.save(folder, revised)
            print(f"revised the spec from {path.name} (dropped: {', '.join(drop) or 'none'}); the old one is kept at {backup}")
            print("note: this edits the spec only. The design (variation.json) is unchanged, so a later `--redo adapt` or `--redo spec` drops these edits; the loop revises the design instead.")
            print(f"- notes: {change.get('notes', '')}")
            print(f"- rules added: {len(change.get('rules_add') or [])}; offers rows: {len(change.get('offers') or [])}; step edits: {len(change.get('step_edits') or [])}")
            return 0
        if args.cmd == "review":
            from gen_game import playreview

            folder = args.root / args.id
            sim_path = args.sim or max((folder / "sim").glob("*.json"), key=lambda f: f.stat().st_mtime)
            sim = playreview.load_sim(sim_path)
            rec = Inventory(args.inventory).get(args.id)
            design = json.loads((folder / "variation.json").read_text())
            spec = json.loads((folder / "spec.json").read_text())
            review, error = playreview.review_play(completion_for(args.model, args.effort), sim, rec.rules_text, design, spec)
            if review is None:
                print(f"review failed: {error}")
                return 1
            out_json = sim_path.with_suffix(".review.json")
            out_json.write_text(json.dumps(review, indent=1))
            out_md = sim_path.with_suffix(".review.md")
            out_md.write_text(playreview.render(review, sim, design["variation"]["name"]))
            print(out_md.read_text())
            print(f"saved {out_md} and {out_json}")
            return 0
        if args.cmd == "simulate":
            from gen_game import simulate as sim

            done = sim.simulate(args.id, [x.strip() for x in args.players.split(",") if x.strip()], args.root, args.matches, args.seed,
                                args.server, args.timeout)
            return 0 if all(d["status"] == "ended" for d in done) else 1
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
