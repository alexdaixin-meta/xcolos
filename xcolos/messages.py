"""The message structure, in one place.

Everything that passes between the game and an agent has a declared shape and
says what kind of message it is. An agent should never have to read prose to
work out whether it is being told something or asked for something.

Two directions, four kinds.

**Game to agent**, delivered in that seat's queue:

    {"kind": "information",
     "seq": 14, "type": "speech", "round": 1, "phase": "day_discussion",
     "text": "Seat 2: \\"Seat 4 has been quiet.\\"",
     "data": {"seat": 2, "text": "Seat 4 has been quiet."}}

    {"kind": "action_required",
     "action": "vote", "prompt": "Vote for a seat to eliminate.",
     "answer_with": "seat", "legal_answers": [0, 1, 3], "seconds_left": 58.2}

An information message says `"respond": false`. It is there to be read and
confirmed, and nothing is waiting on it.

An action message says `"respond": true`. The game is stopped until an answer
arrives. It carries no `seq`, because acknowledging receipt is not answering.

**Agent to game**, in the body of its next call:

    {"kind": "ack", "through": 14}

    {"kind": "action", "action": "vote",
     "response": 3,
     "reason": "Seat 3 answered a question nobody asked."}

    {"kind": "action", "action": "speak",
     "response": "Seat 1 has not accounted for last night.",
     "reason": "I am mafia. Pointing at 1 keeps the table off me."}

An action reply has two halves and the split is the point.

`response` is the move itself: a seat number, or the words you want the table
to hear. The game may make it public.

`reason` is your own thinking. It is recorded so whoever is watching the match
can see why you moved, and it is never turned into a fact, so no other player
is ever told it. Say what you actually think there.

The shorthand `{"ack": 14, "answer": 3}` means the same thing and is accepted
everywhere, because it is easier to type into a command line.
"""

from __future__ import annotations

from typing import Any

from xcolos.protocol import Action, ActionSchema

#: Game to agent.
INFORMATION = "information"
ACTION_REQUIRED = "action_required"
#: Agent to game.
ACTION = "action"
ACK = "ack"


def information(
    seq: int, type: str, round: int, phase: str, text: str, data: dict[str, Any]
) -> dict[str, Any]:
    """Something happened that this seat is entitled to know."""
    return {
        "kind": INFORMATION,
        # Stated outright so an agent never has to infer it. Take it in,
        # confirm it, and carry on. Nothing is waiting on you.
        "respond": False,
        "seq": seq,
        "type": type,
        "round": round,
        "phase": phase,
        "text": text,
        "data": data,
    }


def action_required(
    action: str,
    prompt: str,
    answer_with: str,
    legal_answers: list[Any],
    seconds_left: float,
    max_words: int = 0,
) -> dict[str, Any]:
    """The game is waiting on this seat.

    Deliberately has no `seq`. Acknowledging it would say "received", and a
    turn is not satisfied by receipt.
    """
    return {
        "kind": ACTION_REQUIRED,
        # The game is stopped until this is answered. Thinking is expected;
        # acknowledging is not enough.
        "respond": True,
        "action": action,
        "prompt": prompt,
        "answer_with": answer_with,
        "legal_answers": legal_answers,
        "seconds_left": seconds_left,
        **({"max_words": max_words} if max_words else {}),
    }


def is_information(message: dict[str, Any]) -> bool:
    return message.get("kind") == INFORMATION


def is_action_required(message: dict[str, Any]) -> bool:
    return message.get("kind") == ACTION_REQUIRED


# ----------------------------------------------------------------------
# Agent to game
# ----------------------------------------------------------------------


def read_ack(body: dict[str, Any]) -> int | None:
    """The acknowledgement out of a request body, structured or shorthand."""
    reply = body.get("reply")
    if isinstance(reply, dict) and reply.get("kind") == ACK:
        return _as_int(reply.get("through"))
    if isinstance(body.get("ack"), (int, str)):
        return _as_int(body.get("ack"))
    return None


def read_answer(body: dict[str, Any]) -> Any:
    """The answer out of a request body, structured or shorthand."""
    reply = body.get("reply")
    if isinstance(reply, dict) and reply.get("kind") == ACTION:
        return reply
    return body.get("answer")


def parse_action(
    answer: Any, schema: ActionSchema, legal: tuple[Any, ...]
) -> Action | None:
    """Turn whatever the agent sent into one action.

    Strict about what is legal, forgiving about how it is written. A structured
    reply is the documented form; a bare seat number or a sentence is accepted
    too, because that is what a person types and what a model often returns.
    """
    if answer is None or answer == "":
        return None

    if isinstance(answer, dict):
        reason = str(answer.get("reason") or "")
        named = answer.get("action")
        if named and named != schema.id:
            # Answering a different question than the one asked.
            return Action(type=str(named), reason=reason)

        # `response` is the documented field. The others are older spellings
        # and what a model tends to reach for, so they are accepted too.
        # Chained explicitly, not through `get` defaults: a default only
        # applies when the key is absent, and a model that fills every field
        # of a schema sends the unused ones as null.
        given = None
        for key in ("response", "target", "text", "seat", "choice"):
            value = answer.get(key)
            if value is not None and value != "":
                given = value
                break
        if given is None:
            return None

        if schema.target == "text":
            return Action(type=schema.id, text=str(given), reason=reason)
        return Action(type=schema.id, target=_coerce(given, legal), reason=reason)

    if schema.target == "text":
        return Action(type=schema.id, text=str(answer))
    return Action(type=schema.id, target=_coerce(answer, legal))


def _coerce(value: Any, legal: tuple[Any, ...]) -> Any:
    """Read a seat number out of whatever came in."""
    if legal and isinstance(legal[0], int):
        import re

        found = re.findall(r"-?\d+", str(value))
        if found:
            return int(found[-1])
    return value


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
