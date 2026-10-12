"""From a generated game to a real-model play, and back: the loop and its rules.

The rules are in `design/2026-10-12-evaluation-loop-policy.md`. In short:

  * the game is played by real models at its SUGGESTED table size, a few plays, and each play is reviewed against the idea, the design, the rule table and the prompt;
  * a finding is acted on only when it is critical or major, belongs to the game (its file, its design, the prompt players see) and a verifier CONFIRMS it from the log;
  * the generator is run again for those, and the open MINOR findings go with them; minor findings alone never start a pass;
  * a finding about the platform, the harness or the tools (infra) stops the loop, is written to ESCALATIONS.md, and waits for a person, whatever its severity;
  * a fixed finding that comes back stops the loop and is escalated; so does running out of passes.

Everything the loop does to the world (play, review, confirm, revise, regenerate) is passed in, so the rules can be tested without a model.
"""

from __future__ import annotations

import difflib
import time
from dataclasses import dataclass, field
from typing import Callable

LOOPABLE = ("game_file", "design", "prompt")  # the generator can fix these
SEVERE = ("critical", "major")


def same(a: dict, b: dict) -> bool:
    """Two findings about the same thing: the same kind, and expected-behavior wording that is mostly the same."""
    if a.get("category") != b.get("category"):
        return False
    return difflib.SequenceMatcher(None, str(a.get("expected", "")).lower(), str(b.get("expected", "")).lower()).ratio() >= 0.6


@dataclass
class Hooks:
    simulate: Callable[[], list[str]]                      # plays the game, returns the saved plays
    review: Callable[[str], dict]                          # one play -> a normalized review
    confirm: Callable[[str, dict], tuple[bool | None, str]]  # (play, finding) -> (confirmed, why)
    revise: Callable[[list[dict]], tuple[bool, str]]       # findings -> (spec revised?, notes)
    regenerate: Callable[[], str]                          # rebuild from the revised spec and reinstall -> a verdict
    log: Callable[[str], None]                             # appended to LOOP_LOG.md
    escalate: Callable[[str], None]                        # appended to ESCALATIONS.md
    say: Callable[[str], None] = print


@dataclass
class Result:
    status: str                                            # clean | escalated | max_iterations
    iterations: int = 0
    fixed: list[dict] = field(default_factory=list)
    carried: list[dict] = field(default_factory=list)      # minor, not fixed
    unconfirmed: list[dict] = field(default_factory=list)  # critical or major that nothing confirmed: for a person
    escalated: list[dict] = field(default_factory=list)
    rules_never_seen: list[str] = field(default_factory=list)


def _merge(found: list[dict]) -> list[dict]:
    """One finding for each thing found, however many plays saw it."""
    out: list[dict] = []
    for f in found:
        for g in out:
            if same(f, g):
                g["plays"] = sorted(set(g["plays"]) | set(f["plays"]))
                if f["severity"] in SEVERE and g["severity"] not in SEVERE:
                    g["severity"] = f["severity"]
                break
        else:
            out.append(f)
    return out


def _line(f: dict) -> str:
    return f"- {f.get('id', '?')} [{f['severity']}, {f['category']}] {f['where']}: {f['observed']} (expected: {f['expected']})"


def run_loop(h: Hooks, max_iterations: int = 3) -> Result:
    res = Result("max_iterations")
    fixed: list[dict] = []
    seen_rules: set[str] | None = None
    for it in range(1, max_iterations + 1):
        res.iterations = it
        h.say(f"iteration {it}: playing")
        plays = h.simulate()
        found: list[dict] = []
        never: set[str] | None = None
        for n, play in enumerate(plays):
            review = h.review(play)
            for f in review.get("findings") or []:
                found.append({**f, "plays": [play], "play": n})
            not_seen = set(review.get("rules_not_seen") or [])
            never = not_seen if never is None else never & not_seen
        findings = _merge(found)
        for i, f in enumerate(findings, 1):
            f["id"] = f"I{it}.{i}"
        res.rules_never_seen = sorted(never or [])

        # who may act on what
        players = [f for f in findings if f["category"] == "players"]
        infra = [f for f in findings if f["category"] == "infra"]
        loopable = [f for f in findings if f["category"] in LOOPABLE]
        for f in loopable:
            if f["severity"] in SEVERE:
                f["confirmed"], f["why"] = h.confirm(f["plays"][0], f)
        triggers = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is True]
        refuted = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is False]
        unconfirmed = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is None]
        minors = [f for f in loopable if f["severity"] not in SEVERE]
        res.carried, res.unconfirmed = minors, unconfirmed

        h.log(f"## Iteration {it}\n\nplays: {', '.join(plays)}\n\n"
              + "\n".join(["**Confirmed critical/major (fixed this pass):**"] + [_line(f) for f in triggers] if triggers else ["No confirmed critical or major findings."])
              + ("\n\n**Refuted by the verifier (not acted on):**\n" + "\n".join(_line(f) for f in refuted) if refuted else "")
              + ("\n\n**Unconfirmed critical/major (for a person):**\n" + "\n".join(_line(f) for f in unconfirmed) if unconfirmed else "")
              + ("\n\n**Minor (carried, never start a pass alone):**\n" + "\n".join(_line(f) for f in minors) if minors else "")
              + ("\n\n**Infra (stops the loop):**\n" + "\n".join(_line(f) for f in infra) if infra else "")
              + (f"\n\n{len(players)} finding(s) about the players' own play were ignored." if players else "")
              + (f"\n\nRules no play exercised: {', '.join(res.rules_never_seen)}" if res.rules_never_seen else "") + "\n")

        if infra:  # a fix in the platform or the tools needs a person, before anything is iterated
            res.escalated = infra
            h.escalate(f"## Iteration {it}: infra findings, the loop stopped\n\n" + "\n".join(_line(f) + f"\n  fix proposed: {f['fix']}" for f in infra)
                       + "\n\nNothing was changed. Review these, then decide what to change in the platform or the tools before the loop continues.\n")
            res.status = "escalated"
            h.say(f"stopped: {len(infra)} infra finding(s) need your review (ESCALATIONS.md)")
            return res

        came_back = [f for f in triggers if any(same(f, old) for old in fixed)]
        if came_back:
            res.escalated = came_back
            h.escalate(f"## Iteration {it}: a fixed finding came back, the loop stopped\n\n" + "\n".join(_line(f) for f in came_back)
                       + "\n\nThe generator was asked to fix this before and it is still there. Look at why the fix did not hold.\n")
            res.status = "escalated"
            h.say("stopped: a fixed finding came back (ESCALATIONS.md)")
            return res

        if not triggers:
            res.status = "clean"
            h.say(f"clean after {it} iteration(s): no confirmed critical or major finding" + (f"; {len(minors)} minor finding(s) carried" if minors else ""))
            return res
        if it == max_iterations:
            h.escalate(f"## Out of passes after {it}\n\nStill confirmed critical or major:\n" + "\n".join(_line(f) for f in triggers) + "\n")
            res.escalated, res.status = triggers, "max_iterations"
            h.say("stopped: out of iterations with confirmed findings left (ESCALATIONS.md)")
            return res

        h.say(f"iteration {it}: {len(triggers)} confirmed finding(s); revising the spec and regenerating (carrying {len(minors)} minor)")
        ok, notes = h.revise(triggers + minors)
        if not ok:
            h.escalate(f"## Iteration {it}: the spec could not be revised\n\n{notes}\n\n" + "\n".join(_line(f) for f in triggers) + "\n")
            res.escalated, res.status = triggers, "escalated"
            return res
        verdict = h.regenerate()
        h.log(f"Spec revised ({notes}); regenerated: {verdict}\n")
        fixed += triggers
        res.fixed = list(fixed)
    return res
