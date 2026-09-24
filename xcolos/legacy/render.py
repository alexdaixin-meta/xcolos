"""Deprecated. Per-fact wording for the hardcoded Mafia.

These thirteen branches used to sit in `xcolos/render.py`, which meant the
kernel's renderer — a module every orchestrator goes through — knew one game's
message types by name. A definition-driven game carries its own wording on the
fact, so the kernel needs none of this; only the hardcoded Mafia does, and it
is the thing being retired.

Reached only when a fact arrives with no `rendered` text, which for a flow game
never happens.
"""

from __future__ import annotations

from typing import Any

from xcolos.state import Fact


def legacy_text(view: dict[str, Any], fact: Fact) -> str | None:
    """The hardcoded Mafia's wording for one fact, or None if it has none."""
    p = fact.payload
    t = fact.type
    me = view["you"]["index"]

    if t == "role_assigned":
        return f"You are seat {me} ({view['you']['name']}). Your role is {p['role']} ({p['faction']})."
    if t == "allies":
        others = [s for s in p["seats"] if s != me]
        if not others:
            return "You have no allies."
        return "Your allies are seats " + ", ".join(str(s) for s in others) + "."
    if t == "phase":
        return f"--- Round {fact.round}: {p['phase']} ---"
    if t == "speech":
        return f"Seat {p['seat']}: \"{p['text']}\""
    if t == "death":
        return f"Seat {p['seat']} is dead. They were {p['role']}."
    if t == "no_death":
        return "Nobody died."
    if t == "investigation":
        return f"Your investigation of seat {p['seat']} says: {p['result']}."
    if t == "kill_target":
        return f"Your side has chosen to kill seat {p['seat']}."
    if t == "vote_cast":
        return f"Seat {p['seat']} voted for seat {p['target']}."
    if t == "vote_tally":
        parts = [f"seat {k} got {v}" for k, v in sorted(p["tally"].items())]
        return "Vote result: " + ", ".join(parts) + "."
    if t == "eliminated":
        return f"Seat {p['seat']} was voted out. They were {p['role']}."
    if t == "no_elimination":
        return "The vote was tied. Nobody was voted out."
    if t == "game_over":
        return f"Game over. {p['winner']} wins: {p['reason']}"
    return None
