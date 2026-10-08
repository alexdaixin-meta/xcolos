"""When building or testing a game goes wrong: whose fault is it?

A failure can mean three different things, and they need three different responses:

  fix_game        the rules are sound and the platform can express them; the game file is wrong or
                  incomplete. Send the coder back with guidance.
  revise_rules    the rules are the problem: unbalanced, ambiguous, too complex to build, or awkward
                  to express. Send the designer back with guidance.
  platform_limit  the rules are sound but need something the platform cannot do. Stop, and say exactly
                  what is missing, so it can be counted as engine work.

Guessing the second as the first wastes rounds rebuilding a game that cannot be built; guessing the
first as the second bends good rules to a coder's mistake. A model makes the call, from the rules, the
platform's restrictions and the evidence, and is told to choose `platform_limit` only when the evidence
shows the capability is missing, not just that the coder got it wrong.
"""

from __future__ import annotations

from typing import Protocol

from gen_game import adapt
from gen_game.repair import refused
from gen_inventory.crawl import first_json

DECISIONS = ("fix_game", "fix_tests", "revise_rules", "platform_limit")


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


def system_prompt(manifest: dict | None = None) -> str:
    return f"""A game design for XColos (a platform that runs turn-based, text-only games between language models, decided by
arithmetic) was handed to a coder to build as a game file for the platform's engine, and building or testing it
went wrong. You are given the game's rules, its interface (the attribute names and result names the file must
use), and the evidence of what went wrong. Decide who needs to act:

  fix_game        The rules are sound and the platform can express them, but the game file is wrong or incomplete: a
                  mistake in the file, a rule not implemented, a misread of the rules. Give the coder concrete guidance.
  fix_tests       The game file follows the rules, but a TEST is wrong: it misreads the rules, asserts on internal bookkeeping
                  (a counter, a scratch value, whose turn it is) instead of the result and the scores, or predicts something that
                  chance decides. Compare the tests with the rules and with what the game actually did. The tests will be rewritten,
                  and `guidance` says what to do differently.
  revise_rules    The rules are the problem: a test is right and the rules are unbalanced or ambiguous, the design is
                  too complex to build correctly, or it relies on something awkward the platform can only approximate
                  badly. Say how the designer should change the rules (simplify, rebalance, drop a mechanic).
  platform_limit  The rules are sound and balanced, and they REQUIRE something the platform cannot do (see the
                  restrictions below, and the evidence). Choose this only when the evidence shows the capability is
                  missing, not merely that the coder made an error: a loader error about a wrong key is the coder's,
                  a rule that needs, for example, one player to propose and another to accept an exchange is the
                  platform's. Name exactly what is missing.

A JSON syntax error (the file does not parse, a bracket or brace is missing or extra) is always `fix_game`: it is a typing
slip in the file and says nothing about the rules, however many times it repeats.

If the same kind of failure has repeated across several attempts with the coder fixing things each time, that points to
revise_rules or platform_limit, not another fix_game.

{adapt.restrictions_text(manifest)}
Reply with ONE JSON object and nothing else:
  {{"decision": "fix_game" or "fix_tests" or "revise_rules" or "platform_limit",
    "reason": one or two sentences saying why,
    "guidance": what the coder (fix_game), the test writer (fix_tests) or the designer (revise_rules) should do; empty for platform_limit,
    "missing": for platform_limit only, exactly what the platform cannot do; otherwise empty}}"""


def problems(d) -> list[str]:
    if not isinstance(d, dict) or d.get("decision") not in DECISIONS:
        return [f"decision must be one of {', '.join(DECISIONS)}"]
    out = []
    if len(str(d.get("reason", "")).split()) < 4:
        out.append("give a reason")
    if d["decision"] == "platform_limit":
        if len(str(d.get("missing", "")).strip()) < 3:
            out.append("a platform_limit must say exactly what the platform cannot do, in `missing`")
    elif not str(d.get("guidance", "")).strip():
        out.append("fix_game, fix_tests and revise_rules need `guidance`")
    return out


def decide(completion: Completion, rules: str, interface: str, evidence: str, repairs: int = 2,
           manifest: dict | None = None) -> tuple[dict | None, str]:
    """Returns (decision, error)."""
    prompt = f"RULES:\n{rules}\n\nINTERFACE THE GAME FILE MUST USE:\n{interface}\n\nWHAT WENT WRONG:\n{evidence}"
    system = system_prompt(manifest)
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=system)
            got = first_json(reply)
            found = problems(got)
        except ValueError as exc:
            got, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a verdict
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            return got, ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, error
