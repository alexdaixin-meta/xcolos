"""Generic message protocol.

Message types are owned by the system and are game-agnostic. A game never invents
a message type. This is what lets one agent implementation play every game, and
what lets a local in-process agent and a remote agent share one contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any

PROTOCOL_VERSION = 1


class MsgType(str, Enum):
    """Kernel to agent."""

    #: The briefing, sent once before the first round. Carries the rules, the
    #: table size, this seat's own starting state and index, the shape of a
    #: round, and the communication format. Everything a seat needs to play.
    GAME_START = "GAME_START"
    #: Something happened that this seat is entitled to know. Do not reply.
    SITUATION = "SITUATION"
    #: Act now. Exactly one structured action is expected.
    YOUR_TURN = "YOUR_TURN"
    #: The last answer was not legal. Answer again. Distinct from YOUR_TURN so
    #: a retry is never mistaken for a new turn, by the agent or by the log.
    ACTION_REJECTED = "ACTION_REJECTED"
    #: The match is over. Outcome and reveals.
    GAME_END = "GAME_END"


#: Only these cost an inference call. Everything else appends to the agent's
#: context and returns immediately, which is what makes eager delivery to every
#: entitled seat affordable.
RESPONSE_REQUIRED = frozenset({MsgType.YOUR_TURN, MsgType.ACTION_REJECTED})


#: The communication format, told to every seat in its briefing. Kernel-owned
#: and game-agnostic: a game never invents a message type, so this text is true
#: of every game the runtime will ever run.
PROTOCOL_BRIEFING = """How we will talk, for the rest of the match:

  GAME_START       This message. Sent once, before the first round.
  SITUATION        Something happened that you are allowed to know.
                   Do not reply. Wait to be asked.
  YOUR_TURN        Your turn to act. Reply with exactly one action,
                   in the format the message states.
  ACTION_REJECTED  Your last answer was not legal. Answer again.
  GAME_END         The match is over.

You will only ever be told what you are entitled to know. Other seats are told
different things. Nothing reaches you except through these messages."""


@dataclass(frozen=True)
class ActionSchema:
    """The contract for one kind of action a seat may take."""

    id: str
    target: str  # "text" | "seat" | "enum" | "number" | "zone_position" | "none"
    choices: tuple[Any, ...] = ()
    default: str = "pass"  # how the failure ladder fills in for a broken agent
    #: Word ceiling for a text answer. Zero means no limit.
    #:
    #: Spoken turns are read by every other seat, so length is multiplied by
    #: the table. A limit declared here reaches the agent in the request, so it
    #: knows before it writes rather than after it is refused.
    max_words: int = 0
    #: For a number: the inclusive range, either end open when None. `choices`
    #: then holds the words accepted instead of a number, like "pass".
    minimum: int | None = None
    maximum: int | None = None

    def describe(self) -> dict[str, Any]:
        d: dict[str, Any] = {"id": self.id, "target": self.target}
        if self.choices:
            d["choices"] = list(self.choices)
        if self.max_words:
            d["max_words"] = self.max_words
        if self.minimum is not None:
            d["min"] = self.minimum
        if self.maximum is not None:
            d["max"] = self.maximum
        return d

    def range_text(self) -> str:
        """How to answer a number, in one sentence a player can act on."""
        if self.minimum is not None and self.maximum is not None:
            if self.minimum > self.maximum:
                span = ""
            elif self.minimum == self.maximum:
                span = f"exactly {self.minimum}"
            else:
                span = f"a whole number from {self.minimum} to {self.maximum}"
        elif self.minimum is not None:
            span = f"a whole number of at least {self.minimum}"
        elif self.maximum is not None:
            span = f"a whole number of at most {self.maximum}"
        else:
            span = "a whole number"
        words = " or ".join(str(c) for c in self.choices)
        if span and words:
            return f"Answer with {span}, or {words}."
        return f"Answer with {span or words}."


@dataclass(frozen=True)
class Envelope:
    """One message from the kernel to one seat."""

    type: MsgType
    match_id: str
    seat: int
    body: str  # rendered prose, produced under this seat's view only
    turn_seq: int | None = None
    schema: ActionSchema | None = None
    legal_targets: tuple[Any, ...] = ()
    deadline_ms: int | None = None
    protocol_version: int = PROTOCOL_VERSION

    def to_json(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "match_id": self.match_id,
            "seat": self.seat,
            "body": self.body,
            "turn_seq": self.turn_seq,
            "schema": self.schema.describe() if self.schema else None,
            "legal_targets": list(self.legal_targets),
            "deadline_ms": self.deadline_ms,
            "protocol_version": self.protocol_version,
        }


@dataclass(frozen=True)
class Action:
    """One structured response from a seat.

    Two halves, and the split matters. `target` and `text` are the response
    itself, which the game may make public. `reason`, `predict` and `adjust`
    are the agent's own thinking: why it moved, what it expects its opponents
    to do, and how that changed its own plan. Recorded for whoever is watching
    the match, and never turned into a fact, so no other seat can be told them.
    """

    type: str
    target: Any = None
    text: str = ""
    #: Private. Logged, shown to the operator, never shared with another seat.
    reason: str = ""
    #: Private, like `reason`: what the agent expects its opponents to do.
    predict: str = ""
    #: Private, like `reason`: how the agent changed its own plan in response.
    adjust: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "target": self.target,
            "text": self.text,
            "reason": self.reason,
            "predict": self.predict,
            "adjust": self.adjust,
        }


class ActionInvalid(Exception):
    """Raised when a response does not satisfy the declared schema."""


def validate(action: Action, schema: ActionSchema, legal_targets: tuple[Any, ...]) -> Action:
    """Validate a response against the schema the turn request declared.

    Rejects on the schema id, then on the target domain. The error text is
    returned to the failing seat as a repair prompt and to nobody else, so it
    must never quote state the seat is not entitled to.
    """
    if action.type != schema.id:
        raise ActionInvalid(f"expected action '{schema.id}', got '{action.type}'")

    if schema.target == "none":
        return action

    if schema.target == "text":
        if not isinstance(action.text, str) or not action.text.strip():
            raise ActionInvalid("text must be a non-empty string")
        if schema.max_words:
            words = len(action.text.split())
            if words > schema.max_words:
                raise ActionInvalid(
                    f"that is {words} words; keep it to {schema.max_words} or "
                    "fewer. Put your reasoning in `reason` instead, where it "
                    "costs nobody anything to read"
                )
        return action

    if action.target is None:
        raise ActionInvalid(f"action '{schema.id}' requires a target")

    if schema.target == "number":
        return _validate_number(action, schema)

    if legal_targets and action.target not in legal_targets:
        raise ActionInvalid(
            f"target {action.target!r} is not among the legal targets for '{schema.id}'"
        )

    if schema.target == "enum" and schema.choices and action.target not in schema.choices:
        raise ActionInvalid(f"target must be one of {list(schema.choices)}")

    return action


def _validate_number(action: Action, schema: ActionSchema) -> Action:
    """A whole number in range, or one of the words allowed instead.

    Returns the action with its target normalised — `"550"` and `550.0` both
    become `550`, `"Pass"` becomes `"pass"` — so what the game stores and
    compares is one type however the agent wrote it.
    """
    given = action.target
    if isinstance(given, str):
        word = given.strip().lower()
        for choice in schema.choices:
            if word == str(choice).lower():
                return _with_target(action, choice)
    number: int | None = None
    if isinstance(given, bool):
        number = None
    elif isinstance(given, int):
        number = given
    elif isinstance(given, float) and given.is_integer():
        number = int(given)
    elif isinstance(given, str):
        try:
            value = float(given.strip().replace(",", ""))
            number = int(value) if value.is_integer() else None
        except ValueError:
            number = None
    if number is None:
        raise ActionInvalid(schema.range_text())
    if schema.minimum is not None and number < schema.minimum:
        raise ActionInvalid(f"{number} is below {schema.minimum}. {schema.range_text()}")
    if schema.maximum is not None and number > schema.maximum:
        raise ActionInvalid(f"{number} is above {schema.maximum}. {schema.range_text()}")
    return _with_target(action, number)


def _with_target(action: Action, target: Any) -> Action:
    return replace(action, target=target)


@dataclass
class Directive:
    """One system function call issued by the orchestrator.

    The orchestrator has no other way to affect anything. Every directive is
    validated against the manifest before execution, so the orchestrator can be
    wrong but cannot be wrong silently or corrupt state.
    """

    op: str
    args: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {"op": self.op, "args": self.args}


class DirectiveRejected(Exception):
    """Raised by the kernel when a directive fails validation."""
