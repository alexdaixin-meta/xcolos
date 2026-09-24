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
from xcolos.state import FIRST_SEAT, Fact


def _one(view: dict[str, Any], fact: Fact) -> str:
    p = fact.payload
    t = fact.type
    me = view["you"]["index"]

    # A definition-driven game renders from its own declared templates and
    # carries the result on the fact, so the kernel needs no game knowledge.
    if "rendered" in p:
        return str(p["rendered"])

    # No game knowledge. A definition-driven game renders from its own
    # declared templates and puts the result on the fact, which the branch
    # above returns. The hardcoded Mafia is the only thing that still arrives
    # here without one, and its wording now lives with it.
    from xcolos.legacy.render import legacy_text

    return legacy_text(view, fact) or f"{t}: {p}"


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
        # Numbered from FIRST_SEAT, not from zero. This line said "0 to N-1"
        # while the very next one said "you are seat 1", so every agent was
        # handed two contradictory statements about the only identifier the
        # protocol uses. Read from the constant now, so the two cannot drift.
        f"Players: {brief.seat_count}. Seats are numbered {FIRST_SEAT} to "
        f"{FIRST_SEAT + brief.seat_count - 1}.",
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
