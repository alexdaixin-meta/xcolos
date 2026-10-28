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
     "reason": "Seat 3 volunteered an answer nobody asked for.",
     "predict": "Seat 3 will push the vote onto seat 1 next round.",
     "adjust": "I vote early so seat 3 cannot set the agenda."}

(`reason`, `predict` and `adjust` are the default notes. A game may declare
others under `notes`, and `reply_with` on every ask lists the ones it wants.)

    {"kind": "action", "action": "speak",
     "response": "Seat 1 has not accounted for their last move.",
     "reason": "Pointing at seat 1 keeps attention away from me."}

An action reply has two halves and the split is the point.

`response` is the move itself: a seat number, or the words you want the table
to hear. The game may make it public.

The notes (`reason`, `predict` and `adjust` unless the game names others) are
your own thinking. `reason` is why you made this move, in concrete details: the
seats, numbers and facts it rests on. `predict` is what you expect your
opponents to do and why. `adjust` is how you changed your own strategy in
response. They are recorded so whoever is watching the match can see your
thinking, and none is ever turned into a fact, so no other player is ever told
them. Say what you actually think there.

The shorthand `{"ack": 14, "answer": 3}` means the same thing and is accepted
everywhere, because it is easier to type into a command line.
"""

from __future__ import annotations

from typing import Any, Sequence

from xcolos.games.definition import DEFAULT_NOTES, NoteDef
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


#: The shape of an answer, repeated on every turn so the private fields are
#: asked for each time rather than only in the briefing read once.
def reply_with(notes: Sequence[NoteDef]) -> dict[str, str]:
    """The shape of an answer: the move, then each note the game asks for."""
    return {
        "response": "your move: one of legal_answers, or your words if answer_with is text",
        **{n.name: n.describe for n in notes},
    }


REPLY_WITH = reply_with(DEFAULT_NOTES)


def action_required(
    action: str,
    prompt: str,
    answer_with: str,
    legal_answers: list[Any],
    seconds_left: float,
    max_words: int = 0,
    refused: dict[str, Any] | None = None,
    notes: Sequence[NoteDef] = DEFAULT_NOTES,
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
        # Your last answer to this question, why it was refused, and how many
        # more the game will take before it answers for you.
        **({"refused": refused} if refused else {}),
        "reply_with": reply_with(notes),
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
    answer: Any,
    schema: ActionSchema,
    legal: tuple[Any, ...],
    notes: Sequence[NoteDef] = DEFAULT_NOTES,
) -> Action | None:
    """Turn whatever the agent sent into one action.

    Strict about what is legal, forgiving about how it is written. A structured
    reply is the documented form; a bare seat number or a sentence is accepted
    too, because that is what a person types and what a model often returns.
    """
    if answer is None or answer == "":
        return None

    if isinstance(answer, dict):
        # The private half. Kept whatever the move turns out to be.
        private = {n.name: str(answer.get(n.name) or "") for n in notes}
        named = answer.get("action")
        if named and named != schema.id:
            # Answering a different question than the one asked.
            return Action(type=str(named), notes=private)

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
            return Action(type=schema.id, text=str(given), notes=private)
        return Action(type=schema.id, target=_coerce(given, legal), notes=private)

    blank = {n.name: "" for n in notes}
    if schema.target == "text":
        return Action(type=schema.id, text=str(answer), notes=blank)
    return Action(type=schema.id, target=_coerce(answer, legal), notes=blank)


def _coerce(value: Any, legal: tuple[Any, ...]) -> Any:
    """Read a seat number out of whatever came in."""
    if legal and isinstance(legal[0], int):
        import re

        found = re.findall(r"-?\d+", str(value))
        if found:
            return int(found[-1])
    # A number for an answer the game lists as text ("10" among a hand of cards): that text,
    # so it matches. Only an answer that would otherwise be refused changes.
    if isinstance(value, int) and not isinstance(value, bool) and value not in legal and str(value) in legal:
        return str(value)
    return value


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
