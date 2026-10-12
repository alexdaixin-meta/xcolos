"""Does the rules text the players read say what the numbered rules say?

Scenarios test what the game DOES. They cannot test what the players are TOLD. A player who has only the rules text must be able to play:
if a numbered rule has an outcome the text never states (a failed challenge does not stop the action), a player weighs a decision on a
rule they were not given. Nothing in play shows this, because the game still behaves correctly; a reader has to compare the two.

A model reads the numbered rules and the rules text and lists each rule whose outcome the text leaves out or states differently. It is
asked for clear omissions only, not for every detail.
"""

from __future__ import annotations

import json
from typing import Protocol

from gen_game.repair import refused
from gen_inventory.crawl import first_json


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You check that the RULES TEXT a player reads says what a game's numbered rules say. A player has only the rules text (plus their own state and the question
they are asked); if a numbered rule has an outcome the text never states, or states differently, the player decides without knowing a rule that applies to them.

For each numbered rule, ask: could a player who read only the rules text know what this rule says will happen, in each case it covers (true and false, success and failure,
who is affected, whether the action still goes ahead)? Report a rule only when the text OMITS an outcome a player needs for a decision, or says something DIFFERENT (a different
order of steps, a different cost, a different winner). Do not report wording, style or detail a player would not decide on, and do not report rules about hidden bookkeeping.
Report at most eight, the most important first. If the text covers everything, report none.

Reply with ONE JSON object and nothing else:
  {"gaps": [{"rule": "R21", "problem": "what the text leaves out or gets wrong", "add": "the sentence to add or the wording to use"}]}"""


def build_prompt(spec: dict, text: str) -> str:
    rules = "\n".join(f"{r['id']}. {r['text']}" for r in spec.get("rules") or [])
    return f"THE NUMBERED RULES:\n{rules}\n\nTHE RULES TEXT THE PLAYERS READ:\n{text}"


def problems(reply) -> list[str]:
    if not isinstance(reply, dict) or not isinstance(reply.get("gaps"), list):
        return ['reply with {"gaps": [...]}, empty when the text covers everything']
    out = []
    for i, g in enumerate(reply["gaps"], 1):
        if not (isinstance(g, dict) and all(str(g.get(k, "")).strip() for k in ("rule", "problem", "add"))):
            out.append(f"gap {i} needs rule, problem and add")
    return out


def check_brief(completion: Completion, spec: dict, text: str, repairs: int = 1) -> tuple[list[dict], str]:
    """(gaps, error). No numbered rules or no text means nothing to compare; a model that cannot be reached is an error, not a gap."""
    if not spec.get("rules") or not str(text).strip():
        return [], ""
    prompt = build_prompt(spec, text)
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=SYSTEM)
            parsed = first_json(reply)
            found = problems(parsed)
        except ValueError as exc:
            parsed, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not a gap in the text
            return [], f"the model call failed: {str(exc)[:200]}"
        if not found:
            return parsed["gaps"], ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return [], error


def as_text(gaps: list[dict]) -> str:
    return "\n".join(f"- {g['rule']}: {g['problem']} Say it: {g['add']}" for g in gaps)
