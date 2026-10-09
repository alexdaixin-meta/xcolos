"""The flow: one inventory game through design, build and test, leaving everything on disk.

    A  design    a designer works out rules for XColos from the goal and the platform's RESTRICTIONS
                 (never its file format), and a separate critic must find them balanced, playable and
                 reasoning-over-luck before they go further           variation.json / VARIATION.md
    B  spec      the rules' interface and parameters as a contract      spec.json / SPEC.md
    C  build     a coding agent (or a model in a loop) writes the game file from a prompt that carries
                 the platform's API; independent tests are written from the spec  game.json, scenarios.json
    D  evaluate  tier 0 (valid, ends, replays) and tier 1 (does a thoughtless policy always win?)
                                                                         report.json / REPORT.md
    E  triage    whenever C or D finds a problem, a model decides whose it is:
                   fix_game        the file is wrong: the coder tries again with guidance
                   revise_rules    the rules are the problem: back to A with guidance
                   platform_limit  the rules need what the platform cannot do: STOP, and record exactly what

`history/round_N/` keeps the artifacts of earlier designs. A game is dropped, with a reason, when the
designer says it is too simple or too complex, when no design gets past the critic, or when the last
design still cannot be built or still has a design flaw. A platform limit is not a drop: the game is
recorded as blocked on the missing capability, so it counts as engine work and returns when the engine
can do it.

A game is `ported` in the inventory when it passes its scenarios and validity checks, and `evaluated`
only when nothing is left to flag. `accepted` is a person's.
"""

from __future__ import annotations

import dataclasses
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from gen_game import adapt as adaptmod
from gen_game import complexity, critic, evaluate, lint, modelcheck, prompt as promptmod, scenarios, triage
from gen_game import spec as specmod
from gen_game.agent import CompletionEncoder
from gen_inventory.inventory import Inventory

DATA = Path(__file__).parent / "data" / "games"
STEPS = ("adapt", "spec", "encode", "scenarios", "evaluate")
#: How many times the rules may be revised after a build or test finds the rules are the problem.
DESIGN_ROUNDS = 3
#: How many times the designer and critic go back and forth before the rules go to a coder.
CRITIC_ROUNDS = 3
#: How many times the coder is sent back with guidance before the rules are blamed.
FIX_ROUNDS = 2
ARTIFACTS = ("variation.json", "VARIATION.md", "spec.json", "SPEC.md", "AGENT_PROMPT.md", "CODER_PROMPT.md", "encode_attempts.json", "encode_notes.md",
             "game.json", "scenarios.json", "report.json", "REPORT.md")
IGNORED_FLAGS = ("dominance was not checked",)


@dataclass
class Outcome:
    game_id: str
    # dropped | platform_limit | needs_engine | adapt_failed | spec_failed | encode_failed | scenarios_failed | needs_review | ready_for_review
    verdict: str
    detail: str = ""


@dataclass
class Evidence:
    """What went wrong with a build, in words, and which kind of thing it was."""
    kind: str  # build | behavior | design | spec
    text: str


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def conformance(spec: dict, defn) -> list[str]:
    """Where the game file's shape departs from the spec's. Flags for a person, not failures.

    Scenarios test outcomes; they cannot see that a simultaneous choice was encoded as
    one player answering after another.
    """
    def kinds(steps):
        out = []
        for s in steps:
            out.append(s.use)
            out += kinds(getattr(s, "steps", ()) or ())
        return out

    have = set(kinds(defn.setup) + kinds(defn.steps))
    want = {s["action"] for s in spec["round"]}
    flags = []
    if "poll" in want and "poll" not in have:
        flags.append("the spec has a simultaneous choice (poll) but the game file has none: players may answer after seeing others")
    for k in sorted(want - have - {"poll"}):
        flags.append(f"the spec uses `{k}` but the game file does not")
    declared = {a.key for a in defn.player_attributes} | {a.key for a in defn.game_attributes}
    for scope in ("player", "game"):
        for a in spec["attributes"][scope]:
            if a["key"] not in declared:
                flags.append(f"the spec declares {scope} attribute `{a['key']}` but the game file does not: a piece of state the rules need is missing")
    return flags


def complexity_flags(report: dict) -> list[str]:
    m = report.get("complexity_measured") or {}
    return [f"the built game has {m[k]} {k.replace('_', ' ')}, over the limit of {complexity.LIMITS[k]}"
            for k in ("steps_per_round", "choice_steps_per_round", "attributes") if m.get(k, 0) > complexity.LIMITS[k]]


def design_flags(report: dict) -> list[str]:
    """What the evaluation found that better rules could fix: a thoughtless policy that wins, chance that
    decides everything, or a built game larger than the limits."""
    return ([f for f in report["tier1"]["flags"] if not any(i in f for i in IGNORED_FLAGS)] + complexity_flags(report)
            + list((report.get("lint") or {}).get("findings", [])))


def syntax_only(attempts: list[str]) -> bool:
    """Every attempt failed only because the JSON did not parse: a typing slip, never the rules' fault."""
    shown = [a for a in attempts if a]
    return bool(shown) and all("did not parse" in a for a in shown)


def _flag_text(report: dict, plan: dict | None) -> str:
    t1 = report["tier1"]
    lines = [f"- {f}" for f in design_flags(report)]
    lines.append(f"- against random seats the results were {t1['random_results']}")
    for k, v in t1["dominance"].items():
        lines.append(f"- a thoughtless policy `{k}`: won {v['win']}, lost {v['loss']}, drew {v['draw']}")
    return "\n".join(lines)


def _behavior_text(report: dict) -> str:
    lines = [f"- scenario `{o['name']}` failed: " + "; ".join(o["failures"])[:300] for o in report["scenarios"] if not o["passed"]][:4]
    first = next((o for o in report["scenarios"] if not o["passed"] and o.get("trace")), None)
    if first:
        lines.append(f"- what the game did on `{first['name']}`: {first['trace']}")
    lines += [f"- validity: {p}" for p in report["tier0"]["problems"][:3]]
    return "\n".join(lines)


def _save_report(folder: Path, report: dict, plan: dict | None, round_no: int, decisions: list[dict]) -> None:
    flags = design_flags(report)
    sound = all(o["passed"] for o in report["scenarios"]) and report["tier0"]["passed"]
    report["variation"] = plan
    report["design_rounds"] = round_no
    report["design_flags_left"] = flags
    report["triage"] = decisions
    report["complexity"] = {"reported": (plan or {}).get("complexity"), "measured": report.get("complexity_measured")}
    report["verdict"] = "ready_for_review" if sound and not flags else "needs_review"
    _write(folder / "report.json", json.dumps(report, indent=2) + "\n")
    _write(folder / "REPORT.md", render_report(report))


def _drop(inv: Inventory, rec, folder: Path, kind: str, reason: str, plan: dict | None, tried: list[str]) -> Outcome:
    """Record that a game is not worth building, with the reason, in the folder and in the inventory.

    The inventory keeps it as `rejected` with `dropped` set, so no recheck revives it; clearing
    `dropped` puts it back through the gates. Everything made so far stays in the folder.
    """
    text = f"{kind.replace('_', ' ')}: {reason}"
    lines = [f"# Dropped: {kind.replace('_', ' ')}", "", reason, ""]
    if plan and not adaptmod.is_drop(plan):
        lines += ["## The last variation tried", "", f"{plan['variation']['name']}: {plan['variation']['summary']}", ""]
    if tried:
        lines += ["## What was tried", ""] + [f"- {t}" for t in tried] + [""]
    lines += ["To bring the game back, clear `dropped` in its inventory record."]
    _write(folder / "DROPPED.md", "\n".join(lines) + "\n")
    inv.save(dataclasses.replace(rec, status="rejected", dropped=text, reasons=[f"dropped: {text}"]))
    return Outcome(rec.id, "dropped", text)


def _platform_limit(inv: Inventory, rec, folder: Path, decision: dict, tried: list[str]) -> Outcome:
    """Stop: the rules are sound and need something the platform cannot do.

    Not a drop. The record is given the missing capability as an unmapped need, so the gates mark it
    blocked and `gaps` counts it, and it is converted again when the engine can do it.
    """
    missing = str(decision["missing"]).strip()
    lines = ["# Stopped: the platform cannot do this", "", f"Missing: {missing}", "", str(decision["reason"]).strip(), ""]
    if tried:
        lines += ["## What was tried", ""] + [f"- {t}" for t in tried] + [""]
    lines += ["The inventory records the game as blocked on this need. It is converted again once the engine can do it."]
    _write(folder / "PLATFORM_LIMIT.md", "\n".join(lines) + "\n")
    unmapped = list(dict.fromkeys([*rec.unmapped, missing]))
    inv.save(dataclasses.replace(rec, unmapped=unmapped, status="candidate", port=None))
    inv.check(rec.id)
    return Outcome(rec.id, "platform_limit", missing)


def _design_idea(completion, rec, feedback: str, folder: Path, log) -> tuple[dict | None, Outcome | None]:
    """Design the rules from the idea, once. No critic, no playing it with numbers, no dropping: the game is built as designed."""
    log("step A: designing the rules from the idea")
    plan, error = adaptmod.adapt(completion, rec.to_dict(), feedback, idea=True)
    if plan is None:
        return None, Outcome(rec.id, "adapt_failed", error)
    if adaptmod.is_drop(plan):  # no variation came with it: ask once more, then say so rather than drop the game
        plan, error = adaptmod.adapt(completion, rec.to_dict(), "Do not recommend dropping. Design the best playable game you can from this idea.", idea=True)
        if plan is None or adaptmod.is_drop(plan):
            return None, Outcome(rec.id, "adapt_failed", error or "the designer would only recommend dropping the idea")
    _write(folder / "variation.json", adaptmod.dumps(plan))
    _write(folder / "VARIATION.md", adaptmod.render(plan))
    return plan, None


def _design(completion, rec, feedback: str, folder: Path, log, tried: list[str], inv: Inventory) -> tuple[dict | None, Outcome | None]:
    """The designer and the critic, back and forth until the critic finds the rules sound.

    Returns (the variation, None), or (None, an outcome) when the design stops: the designer recommends
    dropping the game, cannot fit the limits, or no design gets past the critic.
    """
    fb = feedback
    plan, crit, reviews, last_sim = None, None, [], None
    for i in range(1, CRITIC_ROUNDS + 1):
        log("step A: designing the rules" + (" (revising)" if fb else ""))
        plan, error = adaptmod.adapt(completion, rec.to_dict(), fb)
        if plan is None:
            if adaptmod.only_too_complex(error):
                return None, _drop(inv, rec, folder, "too_complex", f"the designer could not bring a variation within the complexity limits: {error[:300]}", None, tried)
            return None, Outcome(rec.id, "adapt_failed", error)
        if adaptmod.is_drop(plan):
            _write(folder / "variation.json", adaptmod.dumps(plan))
            _write(folder / "VARIATION.md", adaptmod.render(plan))
            kind, reason = adaptmod.drop_reason(plan)
            return None, _drop(inv, rec, folder, kind, reason, plan, tried)
        # the rules, played with numbers, before any model is asked its opinion: free, and it cannot be talked round
        if plan.get("model"):
            log("step A: playing the rules with numbers")
            sim = modelcheck.simulate(plan["model"])
            plan["simulation"] = {"flags": sim.flags, "text": sim.text()}
            if sim.flags:
                _write(folder / "variation.json", adaptmod.dumps(plan))
                _write(folder / "VARIATION.md", adaptmod.render(plan))
                tried.append(f"design {i}: playing the rules found {len(sim.flags)} problem(s): {sim.flags[0][:140]}")
                v = plan["variation"]
                fb = (f"Playing the rules with numbers (every simple policy, {modelcheck.MATCHES} games each) found:\n{sim.text()}\n"
                      f"The variation that was played: {v['name']}: {v['rules']} Winner: {v['objective']}\n"
                      "Do not tweak it: change the payoffs or the objective until every one of these problems is gone.")
                last_sim = sim
                crit = None
                continue
        log("step A: the critic reviews the rules")
        crit, error = critic.review(completion, rec.to_dict(), plan)
        if crit is None:
            return None, Outcome(rec.id, "adapt_failed", f"the critic could not review the design: {error}")
        reviews.append(crit)
        plan["critic"] = {"rounds": len(reviews), "reviews": reviews, "sound": crit["sound"]}
        _write(folder / "variation.json", adaptmod.dumps(plan))
        _write(folder / "VARIATION.md", adaptmod.render(plan))
        if crit["sound"]:
            return plan, None
        failed = [c for c in critic.CHECKS if crit[c]["verdict"] == "fail"]
        tried.append(f"design {i}: the critic found it not sound ({', '.join(failed)})")
        v = plan["variation"]
        fb = (f"{critic.feedback(crit)}\nThe variation that was reviewed: {v['name']}: {v['rules']} Winner: {v['objective']}")
    if crit is None and last_sim is not None:  # the last design never got past playing it with numbers
        return None, _drop(inv, rec, folder, "too_simple", f"no design survived playing it with numbers in {CRITIC_ROUNDS} rounds; the last: {last_sim.flags[0][:300]}", plan, tried)
    failed = [c for c in critic.CHECKS if crit[c]["verdict"] == "fail"]
    kind = "too_complex" if "playable" in failed else "too_simple"
    why = (f"no design got past the critic in {CRITIC_ROUNDS} rounds; still failing {', '.join(failed)}: "
           + str(crit[failed[0]]["evidence"])[:240])
    return None, _drop(inv, rec, folder, kind, why, plan, tried)


def _build_and_test(game_id, completion, encoder, spec, plan, folder: Path, redo: set[str], guidance: str, log, fidelity_in_loop: bool = False, judge: bool = False):
    """Build the game file, write independent scenarios, run them, and evaluate.

    Returns (outcome, evidence, report). An `outcome` is a stop that is nobody's design problem (the
    backend is down); `evidence` is a problem with the build for triage; `report` is None when the file
    could not be built.
    """
    paths = {n: folder / n for n in ARTIFACTS}
    attempts: list[str] = []
    from gen_game import encode as enc

    # Writing the game file is judged on one thing: does it work on the platform (it parses, loads, plays to the end, replays the
    # same, and updates what it declares). Whether it follows the rules, and whether it is balanced, are asked afterwards and do not
    # decide whether the file was written. With `fidelity_in_loop` the independent tests are also in the coder's own loop.
    def ensure_scenarios():
        if "scenarios" in redo or not paths["scenarios.json"].exists():
            log("step C: writing independent scenarios from the spec")
            found, error = scenarios.write_scenarios(completion, spec)
            if found is None and "model call failed" in error:  # a service that failed to answer: ask once more
                found, error = scenarios.write_scenarios(completion, spec)
            if found is None:
                return None, Outcome(game_id, "scenarios_failed", f"no usable scenarios: {error}")
            _write(paths["scenarios.json"], json.dumps(found, indent=2) + "\n")
        return json.loads(paths["scenarios.json"].read_text()), None

    # The scenarios are written BEFORE the file, from the spec alone. The coder is judged only on whether the file works; the scenarios
    # are advisory while it builds (an agent can run `verify <id> rules`, and with `fidelity_in_loop` a model-coder's repair loop
    # includes them), and decide nothing about whether the file was written.
    items, stop = ensure_scenarios()
    if stop is not None:
        # They are advisory while building, so a model service that fails once does not stop the build: build the file now and try again after.
        log("the scenarios could not be written yet; building the file first and trying again after")
        items = None

    if "encode" in redo or guidance or not paths["game.json"].exists():
        log("step C: building the game file")
        for stale in ("report.json", "REPORT.md"):
            paths[stale].unlink(missing_ok=True)
        built = encoder.build(game_id, spec, plan, folder, guidance, tests=items if fidelity_in_loop else None)
        attempts = built.attempts
        if built.notes:
            _write(paths["encode_notes.md"], built.notes)
        if not built.ok:
            _write(paths["encode_attempts.json"], json.dumps(attempts, indent=2))
            last = attempts[-1] if attempts else "no attempt was made"
            if "model call failed" in last:
                return Outcome(game_id, "encode_failed", last), None, None
            shown = "\n".join(f"- attempt {i + 1}: {a}" for i, a in enumerate(attempts) if a)[:2400]
            tests = (f"\nTHE TESTS (written from the rules alone; judge whether they are right):\n{json.dumps(items, indent=1)[:2600]}"
                     if "tests written independently" in shown else "")
            return None, Evidence("build", "the game file could not be built. What the checks found on the attempts:\n" + shown + tests +
                                  (f"\nThe coder's notes:\n{built.notes[:800]}" if built.notes else "")), None
        _write(paths["game.json"], json.dumps(built.game, indent=2) + "\n")
    game = json.loads(paths["game.json"].read_text())
    _, defn, problem = enc.check(game, game_id, set(spec.get("parameters", {})))
    if defn is None:
        return None, Evidence("build", problem), None
    if items is None:
        items, stop = ensure_scenarios()
        if stop is not None:
            return stop, None, None
    outcomes = scenarios.run_all(defn, items)
    untested = scenarios.coverage(spec, items)

    log("step D: evaluating")
    t0 = evaluate.tier0(defn)
    traced = lint.trace_lint(defn)
    t1 = evaluate.tier1(defn) if judge else evaluate.not_run()  # reasoning and balance are not the pipeline's question
    report = {
        "game": game_id, "attempts": attempts, "conformance": conformance(spec, defn) + [f"rule {r} has no scenario: nothing checks it" for r in untested],
        "scenarios": [dataclasses.asdict(o) for o in outcomes], "tier0": t0, "tier1": t1, "lint": traced,
        "spec_choices": spec["choices"], "simplifications": spec["simplifications"],
        "complexity_measured": complexity.measure(defn),
    }
    if not (all(o.passed for o in outcomes) and t0["passed"]):
        tests = f"\nTHE TESTS (written from the rules alone; judge whether they are right):\n{json.dumps(items, indent=1)[:2600]}"
        return None, Evidence("behavior", "the game was built and works on the platform, but it does not behave as the independent tests say the rules require:\n"
                              + _behavior_text(report) + tests), report
    if (flags := design_flags(report)):
        return None, Evidence("design", "the game was built and behaves as specified, but evaluation found design flaws:\n" + _flag_text(report, plan)), report
    return None, None, report


def convert(
    game_id: str,
    completion,
    inv: Inventory,
    root: Path = DATA,
    redo: tuple[str, ...] = (),
    log: Callable[[str], None] = lambda _: None,
    adapt: bool = True,
    judge: bool = False,
    design_rounds: int = DESIGN_ROUNDS,
    encoder=None,
    design_feedback: str = "",
    fidelity_in_loop: bool = False,
) -> Outcome:
    rec = inv.get(game_id)
    folder = root / game_id
    encoder = encoder or CompletionEncoder(completion)
    if rec.status not in ("ready", "ported", "evaluated"):
        why = f"dropped ({rec.dropped})" if rec.dropped else rec.status
        return Outcome(game_id, "needs_review", f"the inventory has it as {why}; only ready games are converted")

    redo_set = set(redo)
    plan: dict | None = None
    feedback = design_feedback  # what a person already knows is wrong with a design: the first designer reads it too
    tried: list[str] = []
    decisions: list[dict] = []
    report: dict | None = None
    evidence: Evidence | None = None
    rounds = max(1, design_rounds) if adapt and judge else 1
    for round_no in range(1, rounds + 1):
        last = round_no == rounds
        # -- A: the design --------------------------------------------------
        if adapt:
            vpath = folder / "variation.json"
            if "adapt" in redo_set or feedback or not vpath.exists():
                if round_no > 1:
                    hist = folder / "history" / f"round_{round_no - 1}"
                    hist.mkdir(parents=True, exist_ok=True)
                    for name in ARTIFACTS:
                        if (folder / name).exists():
                            shutil.copy2(folder / name, hist / name)
                if judge:
                    plan, outcome = _design(completion, rec, feedback, folder, log, tried, inv)
                else:
                    plan, outcome = _design_idea(completion, rec, feedback, folder, log)
                if outcome is not None:
                    return outcome
                redo_set |= {"spec"}  # new rules mean a new spec, and so a new everything after it
                feedback = ""
            plan = json.loads(vpath.read_text())
            if judge and adaptmod.is_drop(plan):
                kind, reason = adaptmod.drop_reason(plan)
                return _drop(inv, rec, folder, kind, reason, plan, tried)
            source = adaptmod.source_record(plan)
        else:
            source = rec.to_dict()

        # -- B: the spec ------------------------------------------------------
        spath = folder / "spec.json"
        if "spec" in redo_set or not spath.exists():
            log("step B: writing the spec")
            spec, error = specmod.write_spec(completion, source)
            if spec is None:
                return Outcome(game_id, "spec_failed", error)
            _write(spath, specmod.dumps(spec))
            _write(folder / "SPEC.md", specmod.render(spec))
            for stale in ("game.json", "scenarios.json", "report.json", "REPORT.md"):
                (folder / stale).unlink(missing_ok=True)
        spec = json.loads(spath.read_text())
        redo_set -= {"spec"}
        rules = source["rules_text"]
        interface = promptmod.interface(spec)

        # -- C, D, E: build, test, and triage whatever goes wrong -----------------
        if spec["unsupported"]:
            evidence = Evidence("spec", "the spec lists what it needs that the platform cannot do: " + "; ".join(map(str, spec["unsupported"])))
            report = None
        else:
            guidance = ""
            for fix_no in range(FIX_ROUNDS + 1):
                stop, evidence, report = _build_and_test(game_id, completion, encoder, spec, plan, folder, redo_set, guidance, log, fidelity_in_loop, judge)
                redo_set -= {"encode", "scenarios", "evaluate"}
                if stop is not None:
                    return stop
                if evidence is None or not adapt or (not judge and evidence.kind == "design"):
                    break  # a design flaw is the report's to say, not a reason to stop
                if evidence.kind == "build" and "did not parse" in evidence.text and syntax_only(re.findall(r"- attempt \d+: (.*)", evidence.text)):
                    decision, error = {"decision": "fix_game", "reason": "every attempt failed only on JSON syntax, which is the coder's slip and not the rules'",
                                       "guidance": "Your JSON had a missing or extra bracket. Write the whole file again, indented two spaces per level with one key per line, "
                                                   "and count the brackets of each nested object before you finish.", "missing": ""}, ""
                else:
                    decision, error = triage.decide(completion, rules, interface, evidence.text)
                if decision is None:
                    return Outcome(game_id, "needs_review", f"could not decide whose problem it is: {error}")
                decisions.append({"round": round_no, "fix": fix_no, **decision})
                log(f"triage: {decision['decision']}: {decision['reason']}")
                tried.append(f"round {round_no}: {evidence.kind} problem; triage said {decision['decision']}: {decision['reason'][:160]}")
                if decision["decision"] == "platform_limit":
                    return _platform_limit(inv, rec, folder, decision, tried)
                if decision["decision"] == "fix_tests" and fix_no < FIX_ROUNDS:
                    log("rewriting the independent tests")
                    items, error = scenarios.write_scenarios(completion, spec, guidance=decision["guidance"])
                    if items is None:
                        return Outcome(game_id, "scenarios_failed", f"no usable scenarios: {error}")
                    _write(folder / "scenarios.json", json.dumps(items, indent=2) + "\n")
                    guidance = ""  # the coder starts fresh against the new tests
                    continue
                if decision["decision"] == "fix_game" and fix_no < FIX_ROUNDS:
                    guidance = decision["guidance"]
                    continue
                break
        if evidence is None:
            break
        if not adapt or not judge:
            break  # nobody to revise the rules: the report says what is wrong
        if spec["unsupported"]:
            decision, error = triage.decide(completion, rules, interface, evidence.text)
            if decision is None:
                return Outcome(game_id, "needs_review", f"could not decide whose problem it is: {error}")
            decisions.append({"round": round_no, "fix": 0, **decision})
            if decision["decision"] == "platform_limit":
                return _platform_limit(inv, rec, folder, decision, tried)
        # the rules are the problem, or the coder could not build them: revise, or give up on this game
        if last:
            cx = complexity_flags(report or {})
            if evidence.kind == "design" and not cx:
                kind, why = "too_simple", "it is still degenerate or luck-driven: " + design_flags(report)[0]
            elif evidence.kind == "design":
                kind, why = "too_complex", "it is too large for the platform: " + cx[0]
            else:
                lines = evidence.text.splitlines()
                kind, why = "too_complex", "it could not be built to behave as designed: " + (lines[1] if len(lines) > 1 else lines[0]).lstrip("- ")
            return _drop(inv, rec, folder, kind, f"{why} (after {rounds} variation(s))"[:500], plan, tried)
        feedback = (decisions[-1].get("guidance") or evidence.text) if decisions else evidence.text
        feedback += "\n" + evidence.text
        if report is not None:
            _save_report(folder, report, plan, round_no, decisions)  # so this round's findings are kept in its history
        log("sending the rules back to the designer")

    # -- the report and the inventory ----------------------------------------
    if report is None:
        return Outcome(game_id, "encode_failed", evidence.text[:300] if evidence else "nothing was built")
    flags = design_flags(report)
    sound = all(o["passed"] for o in report["scenarios"]) and report["tier0"]["passed"]
    _save_report(folder, report, plan, round_no, decisions)
    if rec.status != "accepted" and sound:
        inv.save(dataclasses.replace(rec, status="evaluated" if not flags else "ported", port=str(folder / "game.json")))
    t0 = report["tier0"]
    detail = (f"{sum(o['passed'] for o in report['scenarios'])}/{len(report['scenarios'])} scenarios, tier 0 "
              f"{'passed' if t0['passed'] else 'FAILED'}, {len(flags)} design flag(s) left after {round_no} variation(s)")
    return Outcome(game_id, report["verdict"], detail)


def render_report(r: dict) -> str:
    out = [f"# {r['game']}: {r['verdict'].replace('_', ' ')}", ""]
    plan = r.get("variation")
    if plan:
        v = plan["variation"]
        out += [f"Built from the variation **{v['name']}** (design round {r['design_rounds']}); see VARIATION.md.", "",
                "## What was changed from the original, and why", ""]
        out += [f"- {c['what']} (fixes: {c['fixes']}): {c['why']}" for c in plan["changes"]] or ["- nothing"]
        out += ["", f"Objective: {v['objective']}", ""]
        crit = (plan.get("critic") or {}).get("reviews") or []
        if crit:
            last = crit[-1]
            out += [f"## The critic ({len(crit)} review(s) before the rules went to a coder)", ""]
            out += [f"- {c}: {last[c]['verdict']}. {str(last[c]['evidence'])[:300]}" for c in critic.CHECKS] + [""]
    cx = r.get("complexity") or {}
    if cx.get("measured"):
        rep = cx.get("reported") or {}
        out += ["## Complexity", ""] + [
            f"- {k}: designed {rep.get(k, '?')}, built {cx['measured'].get(k, '-')}, limit {complexity.LIMITS[k]}" for k in complexity.KEYS] + [""]
    out += ["## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)", ""]
    for o in r["scenarios"]:
        out.append(f"- {'pass' if o['passed'] else 'FAIL'}: {o['name']}" + ("" if o["passed"] else " | " + "; ".join(o["failures"])))
    out += ["", "## Does the file follow the spec's shape? (flags for a person)", ""]
    out += [f"- {f}" for f in r["conformance"]] or ["- yes"]
    t0, t1 = r["tier0"], r["tier1"]
    out += ["", "## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)", "", f"- {'passed' if t0['passed'] else 'FAILED'}: {t0['metrics']['matches']} random matches at tables {t0['metrics']['tables']}, "
            f"results {t0['metrics']['results']}, {t0['metrics']['turns_min']}-{t0['metrics']['turns_max']} turns"]
    out += [f"- {p}" for p in t0["problems"]]
    lint_r = r.get("lint") or {}
    if lint_r:
        m = lint_r["metrics"]
        out += ["", "## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)", ""]
        out += [f"- {f}" for f in lint_r["findings"]] or ["- clean"]
        out += [f"- cost of a match: {m['decisions_per_match']} decisions, prompts of {m['prompt_chars_avg']} characters on average (longest {m['prompt_chars_max']})"]
    if t1.get("skipped"):
        out += ["", "## Reasoning and balance (not checked here: real models will play it later)", "", "- not run"]
    else:
        out += ["", "## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)", ""]
        out += [f"- {f}" for f in t1["flags"]] or ["- no flags"]
        out += [f"- random seats: {t1['random_results']}"]
        for k, v in t1["dominance"].items():
            out.append(f"- always `{k}`: won {v['win']}, lost {v['loss']}, drew {v['draw']}")
    if r.get("triage"):
        out += ["", "## Triage (whose problem each failure was)", ""]
        out += [f"- round {d['round']}: {d['decision']}: {d['reason']}" for d in r["triage"]]
    for title, key in (("Choices the rules did not make", "spec_choices"), ("Simplifications", "simplifications")):
        out += ["", f"## {title}", ""]
        out += [f"- {i.get('what', i)}: {i.get('why', '')}" if isinstance(i, dict) else f"- {i}" for i in r[key]] or ["- none"]
    if r["attempts"]:
        out += ["", "## Encoding attempts", ""] + [f"- {i + 1}: {a or 'passed'}" for i, a in enumerate(r["attempts"])]
    return "\n".join(out) + "\n"
