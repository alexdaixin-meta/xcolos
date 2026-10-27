"""From a generated game to a real-model play, and back: the loop and its rules.

The rules are in `design/2026-10-12-evaluation-loop-policy.md`. In short:

  * the game is played by real models at its SUGGESTED table size, a few plays, and each play is reviewed against the idea, the design, the rule table and the prompt;
  * a finding is acted on only when it is critical or major, belongs to the game (its file, its design, the prompt players see) and a verifier CONFIRMS it from the log;
  * the generator is run again for those, and the open MINOR findings go with them; minor findings alone never start a pass;
  * a finding about the platform, the harness or the tools (infra) stops the loop, is written to ESCALATIONS.md, and waits for a person, whatever its severity;
  * a fixed finding that comes back stops the loop and is escalated; so does running out of passes;
  * after each iteration's plays, the plays are read for reasoning and planning (`reasoning.py`): a weak verdict is a major design finding that
    needs no verifier (its quotes are checked against the players' own replies), an adequate one a minor finding, a strong one nothing.

Everything the loop does to the world (play, review, confirm, revise, regenerate) is passed in, so the rules can be tested without a model.
"""

from __future__ import annotations

import difflib
import time
from dataclasses import dataclass, field
from typing import Callable

LOOPABLE = ("game_file", "design", "prompt")  # the generator can fix these
SEVERE = ("critical", "major")
REBUILT = ("ready_for_review", "needs_review", "ready")  # verdicts of a rebuild that produced a checked game


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
    #: (plays, reviews, findings) -> the model's overall call: {"decision": "iterate"|"good_enough", "fix": [finding ids], "result_reasonable", "aligned", "reason"}, or None when it could not answer
    judge: Callable[[list[str], list[dict], list[dict]], dict | None] | None = None
    #: plays -> the reasoning-and-planning check of those plays ({"verdict": "strong"|"adequate"|"weak", "summary", "reasoning", "planning", "luck"}), or None when it could not be made
    reasoning: Callable[[list[str]], dict | None] | None = None


@dataclass
class Result:
    status: str                                            # clean | escalated | max_iterations
    iterations: int = 0
    fixed: list[dict] = field(default_factory=list)
    carried: list[dict] = field(default_factory=list)      # minor, not fixed
    unconfirmed: list[dict] = field(default_factory=list)  # critical or major that nothing confirmed: for a person
    escalated: list[dict] = field(default_factory=list)
    judgement: dict | None = None                          # the last overall call by the judge
    reasoning: dict | None = None                          # the last reasoning-and-planning check
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


ASPECTS = ("reasoning", "planning", "luck")
#: What every game is held to by the reasoning check; a weak or adequate verdict is measured against it.
REASONING_EXPECTED = "winning takes reasoning and planning (each at least 2 of 3) and chance decides at most the margin (luck at most 1 of 3)"


def _scores(check: dict) -> str:
    return ", ".join(f"{a} {check[a]['score']}" for a in ASPECTS)


def _reasoning_finding(check: dict, plays: list[str]) -> dict:
    """A weak verdict is a major design finding, already verified by its checked quotes; an adequate one is a minor finding."""
    weak = check["verdict"] == "weak"
    return {"where": "the plays as a whole (REASONING.md)", "observed": f"reasoning check {check['verdict']} ({_scores(check)}): {check.get('summary', '')}",
            "expected": REASONING_EXPECTED, "category": "design", "severity": "major" if weak else "minor", "fix": check.get("summary", ""),
            "plays": list(plays), "play": 0,
            **({"confirmed": True, "why": "the reasoning check quotes the players' own replies, and every quote was checked against them"} if weak else {})}


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
        reviews: list[dict] = []
        never: set[str] | None = None
        for n, play in enumerate(plays):
            review = h.review(play)
            reviews.append(review)
            for f in review.get("findings") or []:
                found.append({**f, "plays": [play], "play": n})
            not_seen = set(review.get("rules_not_seen") or [])
            never = not_seen if never is None else never & not_seen
        findings = _merge(found)
        check = h.reasoning(plays) if h.reasoning else None  # after the plays: did winning take reasoning and planning?
        res.reasoning = check
        if check and check.get("verdict") in ("weak", "adequate"):
            findings.append(_reasoning_finding(check, plays))
        for i, f in enumerate(findings, 1):
            f["id"] = f"I{it}.{i}"
        res.rules_never_seen = sorted(never or [])

        # who may act on what
        players = [f for f in findings if f["category"] == "players"]
        infra = [f for f in findings if f["category"] == "infra"]
        loopable = [f for f in findings if f["category"] in LOOPABLE]
        for f in loopable:
            if f["severity"] in SEVERE and "confirmed" not in f:
                f["confirmed"], f["why"] = h.confirm(f["plays"][0], f)
        triggers = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is True]
        refuted = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is False]
        unconfirmed = [f for f in loopable if f["severity"] in SEVERE and f.get("confirmed") is None]
        minors = [f for f in loopable if f["severity"] not in SEVERE]
        res.carried, res.unconfirmed = minors, unconfirmed

        # After the plays and the checks, a model reads the whole picture and says whether the results are reasonable, whether the game is the
        # one that was designed, and whether it needs another pass or is good enough. It may ask for more fixes (a minor that misleads players, or
        # recurs in every play); it can never wave away a confirmed critical or major finding, and it never touches infra.
        judgement = h.judge(plays, reviews, findings) if h.judge and not infra else None
        res.judgement = judgement
        by_judge: list[dict] = []
        if judgement and judgement.get("decision") == "iterate":
            wanted = set(judgement.get("fix") or [])
            by_judge = [f for f in minors if f.get("id") in wanted]
            for f in by_judge:
                f["by_judge"] = True
            triggers = triggers + by_judge
            minors = [f for f in minors if f not in by_judge]
            res.carried = minors

        verdict_text = ""
        if h.reasoning:
            verdict_text += (f"\n\n**Reasoning check:** {check['verdict']} ({_scores(check)}). {check.get('summary', '')}" if check
                             else "\n\n**Reasoning check:** could not be made.")
        if judgement:
            verdict_text += (f"\n\n**Judge:** {judgement.get('decision')}; result reasonable: {judgement.get('result_reasonable')}; aligned to the design: "
                            f"{judgement.get('aligned')}. {judgement.get('reason', '')}"
                            + (f" Asked for: {', '.join(sorted(set(judgement.get('fix') or [])))}." if judgement.get("fix") else ""))
        h.log(f"## Iteration {it}\n\nplays: {', '.join(plays)}\n\n"
              + "\n".join(["**Confirmed critical/major (fixed this pass):**"] + [_line(f) for f in triggers] if triggers else ["No confirmed critical or major findings."])
              + ("\n\n**Refuted by the verifier (not acted on):**\n" + "\n".join(_line(f) for f in refuted) if refuted else "")
              + ("\n\n**Unconfirmed critical/major (for a person):**\n" + "\n".join(_line(f) for f in unconfirmed) if unconfirmed else "")
              + ("\n\n**Minor (carried, never start a pass alone):**\n" + "\n".join(_line(f) for f in minors) if minors else "")
              + verdict_text
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
            h.say(f"clean after {it} iteration(s): " + ("the judge found it good enough" if judgement else "no confirmed critical or major finding") + (f"; {len(minors)} minor finding(s) carried" if minors else ""))
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
        if verdict not in REBUILT:  # a game that did not come out of the rebuild whole is not played as if it had
            h.escalate(f"## Iteration {it}: the rebuilt game is not usable ({verdict}), the loop stopped\n\n"
                       "The generator was run again from the revised design and ended with this verdict instead of a checked game, so nothing was played. "
                       "See the generation log, then decide whether to rerun the rebuild.\n")
            res.escalated, res.status = triggers, "escalated"
            h.say(f"stopped: the rebuild ended {verdict}, not a checked game (ESCALATIONS.md)")
            return res
        fixed += triggers
        res.fixed = list(fixed)
    return res
