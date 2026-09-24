"""The judge: one stateless call, with a declared output type.

A definition may state a rule as arithmetic the system performs itself, or in
plain language. Prose is what someone writing a new game reaches for first, and
it is the only way to express a rule the comparison language does not cover.
Someone has to read it. That someone is a model, and it is a different model
from the ones playing.

Every call carries the same six things and nothing else:

    the rules          what game this is
    the table          game state: attributes, who is still acting
    the players        player state: status and every attribute, full sight
    the record         what everyone has done so far
    where we are       round, phase, and which step is asking
    the task           what to generate, and the output type it must match

The output type is the part that makes this usable. A call does not ask for
prose and hope; it names one of a fixed set of shapes, each of which maps onto
something the system can actually do:

    boolean   open a gate, or end the game
    player    name a seat for an operation to act on
    choice    one of a declared set
    number    a value for `set` or `adjust`
    text      one message
    messages  one message per named recipient
    message   one message for one recipient, marked info or action
    dispatch  one message per recipient, each marked info or action
    state     whatever the step said it writes: a table object, a record per
              player, or a record for named players — each field checked
    update    a list of declared operations to apply

The reply is parsed and validated against that shape before anything sees it.
Anything that does not match is discarded, and discarding is safe, because of
the defaults below.

Four properties make this safe to add at all.

**Stateless.** No session, no history, no memory of the last round. Each call
carries the whole table. A referee should answer from the state in front of it
rather than something it half-remembers, and the same seed should replay the
same way.

**Full sight, no channel.** The judge sees every role, because it never sits at
the table. It returns a typed value and a sentence of reasoning, and the
executor decides what, if anything, to say to anyone. A judge that hallucinates
can end a game early. It cannot leak a role.

**Never asked what the system can compute.** Tallies, counts and comparisons
stay declarative. Asking a model to count is how you get a result that is wrong
one time in fifty and unreproducible every time.

**Silence is not a yes.** With no judge wired in, or with a reply that does not
parse, a prose ending is declined and a prose gate opens. Both defaults keep
the match running, because a match that overruns hits the round cap and says
so, while a match that ended on a question nobody answered is indistinguishable
from one that ended correctly.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol

#: Every shape a call may ask for. Each one names something the system can do
#: with the answer; there is deliberately no "freeform" member.
OUTPUT_KINDS = (
    "boolean",
    "player",
    "players",
    "choice",
    "number",
    "text",
    "messages",
    "message",
    "dispatch",
    "state",
    "update",
)

#: What a dispatched message expects back from its recipient. `info` is read
#: and acknowledged and the game moves on; `action` stops the game until that
#: player answers.
MESSAGE_TYPES = ("info", "action")

#: Operations an `update` reply may contain. Mirrors the executor's own set, so
#: a model cannot propose a state change the system has no code to apply.
UPDATE_OPS = ("set", "adjust", "append", "remove", "set_status", "disclose")


class JudgeError(Exception):
    """A call was built wrong. Never raised because a model answered badly."""


# ----------------------------------------------------------------------
# What a call asks for
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Output:
    """The expected output type, and the constraints on it.

    Both a prompt fragment and a validator, on purpose. Describing a shape to
    the model and checking the reply against it are the same knowledge, and
    splitting them is how the two drift apart.
    """

    kind: str
    #: For `choice`: the permitted values. For `player`/`players`: the seats
    #: that may be named. An empty tuple means unconstrained.
    options: tuple[Any, ...] = ()
    #: For `messages`: who must receive one. For `players`: how many to name.
    recipients: tuple[int, ...] = ()
    count: int = 0
    max_words: int = 0
    #: For `state`: what this call writes, keyed by target — `table`,
    #: `players`, or `each` — each holding a field schema of
    #: `{key: {"type": ..., "values": [...], "min": ..., "max": ...}}`.
    #:
    #: Both the prompt and the validator are built from this, so a model cannot
    #: be told about a field the engine will not accept, or return one it was
    #: never told about. The target names decide the shape: a `table` object, a
    #: `players` list, an `each` map keyed by player.
    targets: dict[str, dict[str, dict[str, Any]]] = field(default_factory=dict)
    #: Who `each` may name, and how long a `players` list must be.
    players: tuple[int, ...] = ()
    minimum: float | None = None
    maximum: float | None = None

    def __post_init__(self) -> None:
        if self.kind not in OUTPUT_KINDS:
            raise JudgeError(f"unknown output type {self.kind!r}")
        if self.kind == "choice" and not self.options:
            raise JudgeError("a choice output needs options")
        if self.kind in ("messages", "dispatch") and not self.recipients:
            raise JudgeError(f"a {self.kind} output needs recipients")
        if self.kind == "state":
            if not self.targets:
                raise JudgeError("a state output needs at least one target")
            for name in self.targets:
                if name not in ("table", "players", "each"):
                    raise JudgeError(f"unknown update target {name!r}")
            if {"players", "each"} & set(self.targets) and not self.players:
                raise JudgeError("writing players needs the player list")

    # -- describing it to the model ------------------------------------

    def schema_text(self) -> str:
        """The exact JSON shape the model is told to return."""
        body = {
            "boolean": '"answer": true or false',
            "player": '"answer": <one seat number>',
            "players": '"answer": [<seat number>, ...]',
            "choice": '"answer": <one of the options below>',
            "number": '"answer": <a number>',
            "text": '"answer": "<what to say>"',
            "messages": '"answer": {"<seat number>": "<what to say to them>", ...}',
            "message": (
                '"answer": {"type": "info" or "action", '
                '"text": "<what to say>"}'
            ),
            "dispatch": (
                '"answer": {"<seat number>": {"type": "info" or "action", '
                '"text": "<what to say to them>"}, ...}'
            ),
            "state": '"answer": ' + self._state_shape(),
            "update": (
                '"answer": [{"op": "<one of the operations below>", '
                '"args": {...}}, ...]'
            ),
        }[self.kind]
        lines = ["Reply with JSON and nothing else:", "",
                 "{" + body + ', "reason": "one short sentence"}']
        for constraint in self.constraints():
            lines.append(constraint)
        return "\n".join(lines)

    def _state_shape(self) -> str:
        """The JSON shape, one entry per target the step declared."""
        def obj(fields):
            return "{" + ", ".join(f'"{k}": <{k}>' for k in fields) + "}"

        parts = []
        for name, fields in self.targets.items():
            if name == "table":
                parts.append('"table": ' + obj(fields))
            elif name == "players":
                rows = ", ".join(obj(fields) for _ in range(min(len(self.players), 2)))
                parts.append('"players": [' + rows
                             + (", ..." if len(self.players) > 2 else "") + "]")
            else:
                parts.append('"each": {'
                             + ", ".join(f'"{p}": {obj(fields)}'
                                         for p in self.players[:2])
                             + (", ..." if len(self.players) > 2 else "") + "}")
        return "{" + ", ".join(parts) + "}"

    def constraints(self) -> list[str]:
        out: list[str] = []
        if self.kind == "choice":
            out.append(f"Options: {list(self.options)}.")
        if self.kind in ("player", "players") and self.options:
            out.append(f"You may only name these seats: {list(self.options)}.")
        if self.kind == "players" and self.count:
            out.append(f"Name exactly {self.count}.")
        if self.kind in ("messages", "dispatch"):
            out.append(f"One message for each of these seats: {list(self.recipients)}.")
        if self.kind in ("dispatch", "message"):
            out.append(
                'Mark a message "action" only if that player must answer before '
                'the game can continue. Otherwise mark it "info".'
            )
        if self.kind in ("text", "messages", "dispatch", "message") and self.max_words:
            out.append(f"At most {self.max_words} words each.")
        if self.kind == "number":
            if self.minimum is not None:
                out.append(f"At least {self.minimum}.")
            if self.maximum is not None:
                out.append(f"At most {self.maximum}.")
        if self.kind == "update":
            out.append(f"Operations: {list(UPDATE_OPS)}.")
        if self.kind == "state":
            headings = {
                "table": "Set these on the table:",
                "players": f"Give exactly {len(self.players)} records, one per "
                           f"player. The order does not matter: the system "
                           f"shuffles them and deals them out itself.",
                "each": f"Give one record for each of these players, keyed by "
                        f"their id: {list(self.players)}. Which player gets "
                        f"which is your decision here.",
            }
            for name, fields in self.targets.items():
                out.append(headings[name])
                for key, spec in fields.items():
                    out.append(f"  {key}: {_describe_field(spec)}")
        return out

    # -- checking a reply against it -----------------------------------

    def read(self, value: Any) -> Any:
        """Coerce and validate. Returns None for anything that does not fit.

        None is the only failure signal, and every caller treats it as "nobody
        answered". A wrong answer and a missing answer are the same thing here,
        which is what lets the defaults stay simple.
        """
        reader = getattr(self, "_read_" + self.kind)
        try:
            return reader(value)
        except (TypeError, ValueError):
            return None

    def _read_boolean(self, value: Any) -> bool | None:
        return value if isinstance(value, bool) else None

    def _read_player(self, value: Any) -> int | None:
        if isinstance(value, bool) or value is None:
            return None
        seat = int(value)
        if self.options and seat not in self.options:
            return None
        return seat

    def _read_players(self, value: Any) -> list[int] | None:
        if not isinstance(value, list):
            return None
        seats = []
        for item in value:
            seat = self._read_player(item)
            if seat is None:
                return None
            seats.append(seat)
        if self.count and len(seats) != self.count:
            return None
        return seats

    def _read_choice(self, value: Any) -> Any:
        return value if value in self.options else None

    def _read_number(self, value: Any) -> float | int | None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        if self.minimum is not None and value < self.minimum:
            return None
        if self.maximum is not None and value > self.maximum:
            return None
        return value

    def _read_text(self, value: Any) -> str | None:
        if not isinstance(value, str) or not value.strip():
            return None
        return _clip(value.strip(), self.max_words)

    def _read_messages(self, value: Any) -> dict[int, str] | None:
        if not isinstance(value, dict):
            return None
        out: dict[int, str] = {}
        for key, text in value.items():
            try:
                seat = int(key)
            except (TypeError, ValueError):
                return None
            body = self._read_text(text)
            if seat not in self.recipients or body is None:
                return None
            out[seat] = body
        if set(out) != set(self.recipients):
            return None  # a missing recipient is a silent drop, so reject it all
        return out

    def _read_message(self, value: Any) -> dict[str, str] | None:
        """One typed message, for one player. The per-recipient form.

        Written to one reader at a time because that is the only shape that can
        be given a restricted view: a call that writes to several players at
        once has to be shown all of them.
        """
        if not isinstance(value, dict):
            return None
        kind = value.get("type")
        text = self._read_text(value.get("text"))
        if kind not in MESSAGE_TYPES or text is None:
            return None
        return {"type": kind, "text": text}

    def _read_dispatch(self, value: Any) -> dict[int, dict[str, str]] | None:
        """One typed message per recipient, all or nothing.

        Rejecting the whole reply when one message is missing or mistyped is
        deliberate. A partial dispatch would silently drop a player out of the
        round, and a player who was never spoken to looks exactly like a player
        who had nothing to say.
        """
        if not isinstance(value, dict):
            return None
        out: dict[int, dict[str, str]] = {}
        for key, item in value.items():
            try:
                seat = int(key)
            except (TypeError, ValueError):
                return None
            if seat not in self.recipients or not isinstance(item, dict):
                return None
            kind = item.get("type")
            text = self._read_text(item.get("text"))
            if kind not in MESSAGE_TYPES or text is None:
                return None
            out[seat] = {"type": kind, "text": text}
        if set(out) != set(self.recipients):
            return None
        return out

    def _read_state(self, value: Any) -> dict[str, Any] | None:
        """One entry per declared target, every field checked.

        Whole-reply, like every other shape here: a roster with one bad field
        is not partly usable, and applying half of it would leave a table
        nobody declared.
        """
        if not isinstance(value, dict) or set(value) != set(self.targets):
            return None
        out: dict[str, Any] = {}
        for name, fields in self.targets.items():
            got = value[name]
            if name == "table":
                checked = _read_fields(got, fields)
                if checked is None:
                    return None
                out[name] = checked
            elif name == "players":
                if not isinstance(got, list) or len(got) != len(self.players):
                    return None
                rows = [_read_fields(row, fields) for row in got]
                if any(row is None for row in rows):
                    return None
                out[name] = rows
            else:  # "each"
                if not isinstance(got, dict):
                    return None
                rows: dict[int, Any] = {}
                for key, row in got.items():
                    try:
                        player = int(key)
                    except (TypeError, ValueError):
                        return None
                    if player not in self.players:
                        return None
                    checked = _read_fields(row, fields)
                    if checked is None:
                        return None
                    rows[player] = checked
                if set(rows) != set(self.players):
                    return None
                out[name] = rows
        return out

    def _read_update(self, value: Any) -> list[dict[str, Any]] | None:
        if not isinstance(value, list):
            return None
        out: list[dict[str, Any]] = []
        for item in value:
            if not isinstance(item, dict):
                return None
            op = item.get("op")
            args = item.get("args", {})
            if op not in UPDATE_OPS or not isinstance(args, dict):
                return None
            out.append({"op": op, "args": args})
        return out


@dataclass(frozen=True)
class Where:
    """Where in the match the call was made. Part of every prompt and log."""

    round: int = 0
    phase: str = ""
    slot: str = ""
    label: str = ""
    #: A stable handle for the log, e.g. "end[1]" or "gate:the investigation".
    tag: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "round": self.round,
            "phase": self.phase,
            "slot": self.slot,
            "label": self.label,
            "tag": self.tag,
        }

    def sentence(self) -> str:
        parts = [f"Round {self.round}"]
        if self.phase:
            parts.append(f'phase "{self.phase}"')
        if self.slot:
            parts.append(f"step {self.slot}")
        return ", ".join(parts) + "."


@dataclass(frozen=True)
class Call:
    """One request to the judge. Everything it is given, and nothing more."""

    #: What to generate, in plain language. The only free-form field.
    task: str
    #: The shape the answer must take.
    output: Output
    #: The rules of the game, verbatim from the definition.
    rules: str = ""
    #: Game state and player state, full sight. See FlowState.full_view.
    table: dict[str, Any] = field(default_factory=dict)
    where: Where = field(default_factory=Where)

    def to_json(self) -> dict[str, Any]:
        """The logged form. Omits the rules, which never change within a match."""
        return {
            "task": self.task,
            "output": self.output.kind,
            "where": self.where.to_json(),
        }


@dataclass(frozen=True)
class Reply:
    """What came back, after validation."""

    #: The validated value, of whatever type the Output named. None means
    #: nothing usable came back, for any reason.
    value: Any = None
    reason: str = ""
    #: Who answered, for the log: a model name, "stub", "oracle", "error".
    source: str = ""
    #: Exactly what came back, before parsing. Kept so the console can show the
    #: model's own words next to what the system made of them: when a ruling
    #: looks wrong, the question is always whether the model said something
    #: odd or the parser read it wrongly, and only the raw text settles that.
    raw: str = ""

    @property
    def ok(self) -> bool:
        return self.value is not None

    @property
    def yes(self) -> bool:
        """True only for a boolean reply that actually said true."""
        return self.value is True

    def to_json(self) -> dict[str, Any]:
        # Seat-keyed values come back with integer keys, which JSON cannot
        # hold. The log round-trips every record through JSON and rejects
        # anything that does not survive, so the conversion happens here rather
        # than at each call site that might forget.
        return {
            "value": _jsonable(self.value),
            "reason": self.reason,
            "source": self.source,
            "raw": self.raw,
        }


#: The answer when nobody could be asked, or nobody answered usably.
NO_REPLY = Reply(value=None, reason="nobody answered", source="none")


# ----------------------------------------------------------------------
# Judges
# ----------------------------------------------------------------------


class Judge(Protocol):
    """Answers one call about the table."""

    def decide(self, call: Call) -> Reply: ...


class ScriptedJudge:
    """A judge with the answers written down. For tests and offline runs.

    Takes a callable so a test can supply the *declarative* version of the very
    rule being asked in prose. That is the oracle: the prose path and the
    arithmetic path must reach the same verdict on the same table, and any run
    where they disagree is a bug in one of them.
    """

    def __init__(self, answer: Callable[[Call], Any]) -> None:
        self._answer = answer
        #: Every call made, in order. Tests assert on this.
        self.asked: list[Call] = []

    def decide(self, call: Call) -> Reply:
        self.asked.append(call)
        given = self._answer(call)
        if isinstance(given, Reply):
            return given
        return Reply(value=call.output.read(given), source="stub")


class AlwaysJudge:
    """Answers every call the same way. The simplest possible stub."""

    def __init__(self, answer: Any = False, reason: str = "") -> None:
        self._answer, self._reason = answer, reason

    def decide(self, call: Call) -> Reply:
        return Reply(
            value=call.output.read(self._answer),
            reason=self._reason,
            source="stub",
        )


INSTRUCTIONS = """\
You are the referee of a turn-based game. You are not a player and you never \
speak to one. You are shown the complete state of the table, including \
information the players cannot see, and asked to produce one thing.

Answer only from the state you are given. Do not guess at anything not shown, \
do not reason about what a player is likely to do next, and do not soften a \
clear answer. If the state does not settle the question, say so by answering \
false or by returning nothing usable, rather than inventing an answer."""


class ModelJudge:
    """Asks a language model, over the same completion seam the agents use.

    Deliberately thin: build the prompt, one call, parse, validate. Stateless
    between calls, so `history` is for reading back afterwards and is never fed
    into the next prompt.

    The prompt goes out in two pieces. The standing instructions and the rules
    are the system prompt and are identical on every call in a match, so a
    backend can cache them. The table, the question and the expected output are
    the user turn and change every time. Statelessness and caching are not in
    tension: nothing is remembered between calls, and the unchanging half is
    simply not re-read.
    """

    def __init__(self, completion: Any, name: str = "judge") -> None:
        self._completion = completion
        self.name = name
        self.history: list[tuple[Call, Reply]] = []

    def decide(self, call: Call) -> Reply:
        try:
            raw = self._completion.complete(prompt(call), system=system_prompt(call))
        except Exception as error:  # a referee that crashes must not end a game
            reply = Reply(None, f"the judge could not be reached: {error}", "error",
                          raw=str(error))
        else:
            reply = read_reply(raw, call.output, self.name)
        self.history.append((call, reply))
        return reply


# ----------------------------------------------------------------------
# The prompt, and reading the reply
# ----------------------------------------------------------------------


def system_prompt(call: Call) -> str:
    """The half of the prompt that does not change within a match.

    The referee's standing instructions and the rules of the game, and nothing
    else. Every call in a match produces a byte-identical string here, which is
    what makes it worth caching: a provider that supports prompt caching reads
    the rules once instead of on every check.

    Nothing that varies may move into here, however tempting. A cache that
    misses every call is the same cost with extra machinery, and a cache that
    *hits* when it should not would answer this round's question with last
    round's table.
    """
    return "\n\n".join(
        part for part in (INSTRUCTIONS, _section("THE GAME", call.rules)) if part
    )


def prompt(call: Call) -> str:
    """The half that changes: the table now, and what is being asked of it."""
    table = call.table or {}
    sections = [
        _section("THE TABLE", _json({
            "attributes": table.get("table", {}),
            "still acting": table.get("acting", []),
        })),
        _section("THE PLAYERS", _json(table.get("players", []))),
        _section("THE RECORD", _json(table.get("record", []))),
        _section("WHERE WE ARE", call.where.sentence()),
        _section("YOUR TASK", call.task),
        _section("YOUR ANSWER", call.output.schema_text()),
    ]
    return "\n\n".join(s for s in sections if s)


def full_prompt(call: Call) -> str:
    """Both halves, for a backend with nowhere to put a system prompt."""
    return "\n\n".join(p for p in (system_prompt(call), prompt(call)) if p)


def read_reply(raw: Any, output: Output, source: str = "") -> Reply:
    """Read a reply out of a model's text. Anything unreadable answers nothing."""
    match = re.search(r"\{.*\}", str(raw), re.DOTALL)
    text = str(raw)
    if not match:
        return Reply(None, "the judge did not answer in JSON", source, text)
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return Reply(None, "the judge's answer was not valid JSON", source, text)
    if not isinstance(data, dict) or "answer" not in data:
        return Reply(None, "the judge's answer had no `answer` field", source, text)

    value = output.read(data["answer"])
    if value is None:
        return Reply(None, f"the answer was not a valid {output.kind}", source, text)
    return Reply(value, str(data.get("reason", "")), source, text)


def _describe_field(spec: dict[str, Any]) -> str:
    bits = [f"type {spec.get('type', 'text')}"]
    if spec.get("values"):
        bits.append("one of " + str(list(spec["values"])))
    for bound, word in (("min", "at least"), ("max", "at most")):
        if spec.get(bound) is not None:
            bits.append(f"{word} {spec[bound]}")
    return ", ".join(bits)


def _read_fields(
    row: Any, fields: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    """One object, every field checked against its declared type and values."""
    if not isinstance(row, dict) or set(row) != set(fields):
        return None
    checked: dict[str, Any] = {}
    for key, spec in fields.items():
        got = row[key]
        allowed = spec.get("values")
        if allowed and got not in allowed:
            return None
        kind = spec.get("type", "text")
        if kind == "number":
            if isinstance(got, bool) or not isinstance(got, (int, float)):
                return None
            if spec.get("min") is not None and got < spec["min"]:
                return None
            if spec.get("max") is not None and got > spec["max"]:
                return None
        elif kind == "bool":
            if not isinstance(got, bool):
                return None
        elif kind == "list":
            if not isinstance(got, list):
                return None
        else:
            if not isinstance(got, str) or not got.strip():
                return None
            got = got.strip()
        checked[key] = got
    return checked


def _jsonable(value: Any) -> Any:
    """The same value, with every dict key a string. Recursive."""
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    return value


def _section(heading: str, body: Any) -> str:
    body = str(body).strip()
    return f"{heading}\n{body}" if body else ""


def _json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, default=str)


def _clip(text: str, max_words: int) -> str:
    if not max_words:
        return text
    words = text.split()
    return text if len(words) <= max_words else " ".join(words[:max_words])
