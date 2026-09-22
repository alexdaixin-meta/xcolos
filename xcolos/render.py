"""Per-recipient rendering.

The orchestrator sees everything, so it must never author the text an agent
receives. It emits structured facts with explicit audiences. This renderer turns
those facts into prose while holding only one recipient's entitled subset, so it
cannot leak what it was never given.

Stage 1a renders from templates: deterministic, free, and no model call.
"""

from __future__ import annotations

from typing import Any

from xcolos.protocol import PROTOCOL_BRIEFING, ActionSchema
from xcolos.state import Fact


def _one(view: dict[str, Any], fact: Fact) -> str:
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
    return f"{t}: {p}"


def render_facts(view: dict[str, Any], facts: list[Fact]) -> str:
    """Render one seat's entitled facts. Never called with anything else."""
    return "\n".join(_one(view, f) for f in facts)


def render_briefing(view: dict[str, Any], facts: list[Fact], brief: Any) -> str:
    """The pre-match briefing for one seat.

    Assembled from two sources that never mix. The orchestrator supplies the
    game content, which is identical for everyone. The seat's own starting
    state comes from its entitled facts, so the private half of this message is
    built the same way every other message is, and is subject to the same rule.
    """
    me = view["you"]
    lines: list[str] = [
        f"=== {brief.name} ===",
        "",
        brief.rules,
        "",
        "--- Your place at the table ---",
        "",
        f"Players: {brief.seat_count}. Seats are numbered 0 to {brief.seat_count - 1}.",
        f"You are seat {me['index']}, {me['name']}. Seats are referred to by number.",
    ]

    starting = render_facts(view, facts)
    if starting:
        lines += ["", "What you know to begin with:", "", starting]

    if brief.round_shape:
        lines += [
            "",
            "Each round runs in this order: " + " → ".join(brief.round_shape) + ".",
        ]

    if brief.actions:
        lines += ["", "Actions you may be asked for:"]
        for schema in brief.actions:
            lines.append(f"  {schema.id:12} {_answer_hint(schema)}")

    lines += ["", PROTOCOL_BRIEFING]
    return "\n".join(lines)


def _answer_hint(schema: ActionSchema) -> str:
    if schema.target == "text":
        return "answer with what you want to say"
    if schema.target == "seat":
        return "answer with one seat number, from the list you are given"
    if schema.target == "enum":
        return f"answer with one of: {', '.join(str(c) for c in schema.choices)}"
    if schema.target == "none":
        return "answer to confirm"
    return f"answer with one {schema.target}"


def render_turn(
    view: dict[str, Any],
    facts: list[Fact],
    schema: ActionSchema,
    legal_targets: tuple[Any, ...],
    prompt: str,
) -> str:
    """Build the YOUR_TURN body: situation, what you may do, what to answer."""
    lines: list[str] = []
    situation = render_facts(view, facts)
    if situation:
        lines.append(situation)
    living = [s["index"] for s in view["seats"] if s["status"] == "active"]
    lines.append(f"Living seats: {living}.")
    lines.append(prompt)
    if schema.target == "text":
        lines.append("Answer with the text you want to say.")
    elif legal_targets:
        lines.append(f"Answer with one of: {list(legal_targets)}.")
    return "\n".join(lines)
