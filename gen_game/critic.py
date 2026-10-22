"""A second pair of eyes on a design, before anything is built.

The designer reviews its own work, and a designer that has just fixed a flaw is the last
reader to see the one it left in (the stag hunt variation whose mixed payoffs were swapped).
So a separate call, with no stake in the design, checks the three things XColos needs from a
game, and a design is only sound when all three pass:

  balanced            no seat and no simple policy has the edge; the main decision is a real one
  playable            complete, unambiguous rules a model can follow, inside the platform's restrictions
  reasoning_over_luck what wins is inference, planning and opponent modelling, not the draw

The critic is told to work the numbers out (write the payoff table, test a thoughtless policy)
and show the work as evidence, because a verdict with no arithmetic behind it is an opinion.
It sees the rules and the platform's restrictions, never the engine's file format.
"""

from __future__ import annotations

import json
from typing import Protocol

from gen_game import adapt, complexity
from gen_game.repair import refused
from gen_inventory.crawl import first_json

CHECKS = ("balanced", "playable", "reasoning_over_luck")


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


def system_prompt(manifest: dict | None = None) -> str:
    return f"""You are a strict reviewer of game designs for XColos, a platform that trains and tests language models on
strategic reasoning: inference from limited information, opponent modelling, and planning over rounds. It runs
turn-based, text-only games between models and scores them by arithmetic. You did not design the game you are
shown and you want it to fail review if it should.

You are given the original game's rules and a proposed VARIATION. Check three things, each pass or fail, and
SHOW YOUR WORK as evidence:

  balanced
    Work out the payoffs or the main decision numerically. Write the table. Test a thoughtless policy (always the
    first option, always the last, always pass, always the highest bid) against sensible play and against random
    play: does it win or draw almost every time? Is any option strictly better whatever the opponent does? Does
    either seat have an edge from move order or information? Can both players realistically win? Check the
    arithmetic of any labelled payoff ordering: a game described as one thing but whose numbers are another fails.
    Apply the WINNER RULE, not the payoffs: for each thoughtless policy work out who WINS or DRAWS against each opponent
    action. A policy that never loses fails the check, even when no option is strictly better. In a two-player game
    decided by "higher total wins", an option that never leaves you behind makes cooperation pointless and the game
    fails.
  playable
    Are the rules complete and unambiguous, so a model that has only these words could play every situation? Is
    the game finite, and decided by arithmetic on numbers the game keeps? Is it inside the platform's
    restrictions and complexity limits ({complexity.describe_limits()})? Does it need a judge, a board, a real
    clock, or something the platform cannot do? With three or more players, did the design decide
    sensibly whether each round opens with talk? Talk belongs where players disagree about something, so that following a
    proposal can cost them, and where it gives them something to reason about; it does not where everyone wants the same
    outcome (the first speaker proposes and the rest copy) or where it only adds words. Talk should be simultaneous (all write,
    all are shown, then all choose), not one speaker after another, unless the order is the point. Fail it if talk is present where
    everyone just follows, or missing where players could then only guess each other.
    In a repeated game of fixed length decided by the highest total, does cooperation still pay after a betrayal, or does
    the safe option win every late round? If the latter, it fails.
  reasoning_over_luck
    What decides who wins: inference, planning and opponent modelling, or the random draw? Estimate how much of
    the result is chance. Also work out the outcome when every player follows the intended good strategy: if the winner is
    then decided by the random draw alone (a hidden type, a deal), it fails; a random deal that good play can overcome is fine and adds variety. If a player who reasons well is not clearly favoured over one who does not, or if chance
    alone often decides the winner, it fails. Is there something to infer (hidden information, an opponent's type or
    likely move) and a way to act on it?

{adapt.restrictions_text(manifest)}
Reply with ONE JSON object and nothing else:
  {{"balanced": {{"verdict": "pass" or "fail", "evidence": ...}},
    "playable": {{"verdict": "pass" or "fail", "evidence": ...}},
    "reasoning_over_luck": {{"verdict": "pass" or "fail", "evidence": ...}},
    "required_changes": [specific changes that would make each failing check pass; empty only if nothing fails]}}"""


def problems(review) -> list[str]:
    if not isinstance(review, dict):
        return ["reply with a JSON object"]
    out = []
    for c in CHECKS:
        e = review.get(c)
        if not (isinstance(e, dict) and e.get("verdict") in ("pass", "fail") and str(e.get("evidence", "")).strip()):
            out.append(f"{c} needs a verdict of pass or fail and evidence")
    if not out and any(review[c]["verdict"] == "fail" for c in CHECKS):
        rc = review.get("required_changes")
        if not (isinstance(rc, list) and rc and all(isinstance(x, str) and x.strip() for x in rc)):
            out.append("a failed check needs required_changes: specific changes that would fix it")
    return out


def sound(review: dict) -> bool:
    return all(review[c]["verdict"] == "pass" for c in CHECKS)


def review(completion: Completion, record: dict, plan: dict, repairs: int = 2, manifest: dict | None = None) -> tuple[dict | None, str]:
    """Check a variation. Returns (review, error). `sound` is decided here from the three verdicts,
    never taken from the model's say-so."""
    v = plan["variation"]
    prompt = (f"ORIGINAL GAME: {record['name']}\n{record['rules_text']}\n\n"
              f"PROPOSED VARIATION: {v['name']}\nPlayers: {v['players']['min']} to {v['players']['max']}\n"
              f"Rules: {v['rules']}\nHow the winner is decided: {v['objective']}\n"
              f"The designer's stated complexity: {json.dumps(plan.get('complexity'))}")
    system = system_prompt(manifest)
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=system)
            got = first_json(reply)
            found = problems(got)
        except ValueError as exc:
            got, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad design
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            got["sound"] = sound(got)
            return got, ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, error


def feedback(r: dict) -> str:
    """The critic's findings as a request to the designer."""
    lines = [f"- {c} FAILED: {r[c]['evidence']}" for c in CHECKS if r[c]["verdict"] == "fail"]
    lines += [f"- change: {x}" for x in r.get("required_changes", [])]
    return "\n".join(lines)
