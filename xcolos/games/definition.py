"""The game definition: the schema, as types.

A definition says everything about one game and nothing about the runtime. This
module parses one, validates it, and refuses anything it cannot check later.

Every authoring error is caught here, at load, rather than three rounds into a
match. That is the whole reason the declarative half exists.

On format: the design writes definitions in YAML, which is nicer to read. There
is no YAML parser available on this machine and no way to install one, so the
loader takes JSON with an identical shape. A YAML front-end is a dozen lines
once the dependency exists, and nothing below it changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

SCHEMA_VERSION = 1

#: The whole flow, in four kinds. A round is a list of steps, each of one of
#: these; a game says which, in what order, and may use any of them as often as
#: it likes.
#:
#: This replaced a list of twelve named slots (`secret_act`, `reveal`, `vote`,
#: `resolve_vote` and so on). The twelve were a taxonomy of what steps are
#: *for*, and a taxonomy is a guess about games nobody has written yet. These
#: four are what the engine actually *does*, and there is nothing else it can
#: do:
#:
#:   initialize  fill every player's declared fields, then deal them by seed
#:   sync    send each player their own state, as data rather than prose
#:   tell    send a message and carry on; nobody is waited for
#:   ask     address players one at a time, each seeing the last one's answer
#:   poll     address every player at once and gather; nobody sees another's
#:            answer until all are in, and answers commit in seat order
#:   update  change state, and say what changed
#:   check   continue, or end
#:
#: A game's own vocabulary lives in `phase` and `label`, so Mafia still has a
#: night and a vote; the engine has neither.
KINDS = ("initialize", "sync", "tell", "ask", "poll", "update", "check")

#: Kinds that address players. `tell` speaks and carries on; the other two
#: stop the game until the addressed players answer.
#:
#: These were one action whose behaviour depended on whether a sibling
#: `answer` key happened to be present — so `use` did not tell a reader whether
#: the flow waits, which is the single most important thing about a step. A
#: briefing was declared as `ask` and asked nothing. Splitting them is what
#: makes the word mean what it says.
SPEAKING_KINDS = ("sync", "tell", "ask", "poll")
#: Whose state a `sync` sends, and to whom.
SYNC_MODES = ("self", "others")

#: What kind of message a `tell` is. The action stays one action; the kind
#: says what the engine should assemble into the request, so a game states the
#: subject and the fields rather than describing them in prose.
#:
#:   message        just the prompt, on the recipient's view
#:   status_update  plus what the subject's named fields now hold, filtered
#:                  separately for each recipient
#:
#: Adding a kind is a row here and a branch in the request builder. The point
#: is that a game never has to write "player 3 is now eliminated" into a
#: prompt by hand; it says which player and which fields, and the engine puts
#: the current values in front of the model.
TELL_KINDS = ("message", "status_update")
#: Kinds that stop the game until an answer arrives.
ASKING_KINDS = ("ask", "poll")

#: Every key on a step, and nothing else. The union is long because it is the
#: union of seven actions' needs; no single action reads more than a third of
#: it.
COMMON_KEYS = ("use", "label", "phase", "when")

#: Which keys each action reads. A key an action ignores is refused at load,
#: because a silently ignored field is the same failure as a misspelled one —
#: the game does not do what the file says, and nothing says so. Six such
#: combinations used to load cleanly: a `check` with `about`, a `tell` with
#: `verify`, an `update` with `to`, and more.
#:
#: This table is also the honest answer to "which fields apply to me": a
#: reader of the schema sees a list of twenty-two, and a writer of a step
#: needs at most eight.
ACTION_KEYS = {
    "initialize": ("updates", "requires", "llm"),
    "sync": ("to", "mode", "fields", "text", "llm", "max_words"),
    "tell": ("to", "kind", "about", "fields", "text", "llm", "max_words"),
    "ask": ("to", "answer", "verify", "outcome", "broadcast", "text", "llm",
            "max_words", "deadline_s", "on_timeout"),
    "poll": ("to", "answer", "verify", "outcome", "broadcast", "text", "llm",
             "max_words", "deadline_s", "on_timeout"),
    "update": ("do", "text", "llm", "max_words"),
    "check": ("against", "llm"),
}

#: Kinds a `setup` step may use. Setup runs before the game is running and
#: before anybody has been greeted, so there is nobody to wait on and nothing
#: to end: an `ask` there may inform, never question.
SETUP_KINDS = ("initialize", "sync", "tell", "update")

#: Who can see a player attribute. `ally` resolves to the owner alone when the
#: game declares no allegiance, which is what makes a solo role work without a
#: special case.
PLAYER_VISIBILITY = ("public", "ally", "others")
#: A table attribute has no owner, so only these two make sense.
GAME_VISIBILITY = ("public", "none")

TYPES = ("text", "number", "bool", "list")
ANSWER_TYPES = ("text", "player", "players", "choice", "number", "none")
OPERATIONS = ("set", "adjust", "append", "remove", "set_status", "disclose")
OPERATORS = ("==", "!=", "<", "<=", ">", ">=")
TALLIES = ("plurality", "majority", "unanimity")
#: What a tally yields when it settles on no one: a tie under `on_tie:
#: nobody`, a rule that needed a majority and did not get one, or a step
#: nobody answered. Operations naming it as `unless` are skipped.
#:
#: One constant because the word travels between the engine and the game file
#: — `tally()` produces it, `_seat()` refuses it, and a definition writes
#: `"unless": "nobody"` to guard against it. Written independently in each
#: place, a typo in the file would silently disarm the guard, so the loader
#: checks any `unless` against this.
NOBODY = "nobody"

#: A tally that must be taken again. Distinct from NOBODY: one is a result,
#: the other is the absence of one.
RERUN = "rerun"

ON_TIE = (NOBODY, "random", RERUN)


class DefinitionError(Exception):
    """The definition is not loadable. Always names the path that is wrong."""


def _require(cond: bool, where: str, message: str) -> None:
    if not cond:
        raise DefinitionError(f"{where}: {message}")


def _only(raw: dict[str, Any], allowed: tuple[str, ...], where: str) -> None:
    """Reject any key this parser does not read.

    Without this a misspelling loads cleanly and does nothing: write
    `answers_visable` and the step silently keeps its default, so the leak you
    meant to prevent is simply not prevented and nothing says so. A game file
    is configuration written by hand, and the failure mode of hand-written
    configuration is always the field that was ignored.

    The cost is that adding a field to the schema means adding it here too. It
    is a short list per structure and the alternative is a game that is subtly
    not the game somebody wrote.
    """
    unknown = sorted(set(raw) - set(allowed))
    if unknown:
        raise DefinitionError(
            f"{where}: unknown {'key' if len(unknown) == 1 else 'keys'} "
            f"{', '.join(repr(k) for k in unknown)}. "
            f"This structure takes: {', '.join(sorted(allowed))}"
        )


def _one_of(value: Any, allowed: tuple[str, ...], where: str) -> str:
    _require(value in allowed, where, f"expected one of {list(allowed)}, got {value!r}")
    return str(value)


# ----------------------------------------------------------------------
# Pieces
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Allegiance:
    """Which attribute makes two players allies, and for which values.

    `mutual` is the part that matters. In Mafia both sides share a faction,
    but only the mafia know each other: declaring `mutual: ["evil"]` gives the
    conspiracy shared sight and leaves the town in the dark, from one line.

    Omit `mutual` and every value forms a knowing team, which is right for a
    game of declared, visible teams.
    """

    attribute: str
    mutual: tuple[Any, ...] = ()
    all_values: bool = True

    @staticmethod
    def parse(raw: Any, where: str) -> "Allegiance":
        if isinstance(raw, str):
            return Allegiance(attribute=raw)
        _require(isinstance(raw, dict), where, f"expected an allegiance, got {raw!r}")
        _require("attribute" in raw, where, "needs an `attribute`")
        mutual = raw.get("mutual")
        return Allegiance(
            attribute=str(raw["attribute"]),
            mutual=tuple(mutual or ()),
            all_values=mutual is None,
        )

    def knows(self, value: Any) -> bool:
        """Do players sharing this value know one another?"""
        return self.all_values or value in self.mutual


@dataclass(frozen=True)
class StatusDef:
    id: str
    acts: bool
    initial: bool = False


@dataclass(frozen=True)
class AttributeDef:
    key: str
    visible: str
    type: str
    initial: Any = None
    mutable: bool = True
    #: The values this attribute may hold. Optional, and load-bearing when
    #: present: it is what lets the engine reject a hallucinated role before it
    #: reaches state, instead of discovering it three rounds later when a
    #: selector matches nobody.
    values: tuple[Any, ...] = ()


@dataclass(frozen=True)
class Selector:
    """Who a step is addressed to. Never a string to parse.

    Always intersected with "may act", so a definition never has to remember
    to exclude eliminated players.
    """

    #: "acting" | "all" | "attribute" | "ids" | "others" | "ally" | "author"
    #:
    #: The last three are relative to whoever the message is about — the player
    #: who just answered. They were a separate four-value enum on `broadcast`,
    #: so "who" was spelled four ways across the schema with four types. One
    #: grammar means one word and one parser.
    kind: str
    attribute: str | None = None
    is_: Any = None
    negate: bool = False
    ids: tuple[int, ...] = ()

    @staticmethod
    def parse(raw: Any, where: str) -> "Selector":
        if raw is None or raw == "acting":
            return Selector(kind="acting")
        if raw in ("all", "others", "ally", "author"):
            return Selector(kind=str(raw))
        _require(isinstance(raw, dict), where, f"expected a selector, got {raw!r}")
        _only(raw, ("ids", "attribute", "is", "not", "acting"), where)
        if "ids" in raw:
            ids = raw["ids"]
            _require(isinstance(ids, list), where, "ids must be a list")
            return Selector(kind="ids", ids=tuple(int(i) for i in ids))
        _require("attribute" in raw, where, "a selector needs `attribute` or `ids`")
        return Selector(
            kind="attribute",
            attribute=str(raw["attribute"]),
            is_=raw.get("is"),
            negate=bool(raw.get("not", False)),
        )


@dataclass(frozen=True)
class Operand:
    """One side of a comparison: a count over a selector, or a table attribute.

    Separate from Condition because the right-hand side of `a >= b` is a thing
    to measure, not another question to answer.
    """

    kind: str  # "count" | "game"
    selector: Selector | None = None
    acting_only: bool = True
    attribute: str | None = None

    @staticmethod
    def parse(raw: Any, where: str, *, strict: bool = True) -> "Operand":
        """`strict=False` when reading the left side of a comparison.

        A comparison keeps its left operand in the same object as its operator
        and its right side, so that dict legitimately carries `op` and `value`
        as well. The condition checks the whole shape; this one must not
        object to the keys that belong to its parent.
        """
        _require(isinstance(raw, dict), where, f"expected an operand, got {raw!r}")
        if strict:
            _only(raw, ("count", "game"), where)
        if "count" in raw:
            inner = raw["count"]
            _require(isinstance(inner, dict), where + ".count", "takes a selector")
            return Operand(
                kind="count",
                selector=Selector.parse(inner, where + ".count"),
                acting_only=bool(inner.get("acting", True)),
            )
        _require("game" in raw, where, "an operand needs `count` or `game`")
        return Operand(kind="game", attribute=str(raw["game"]))


@dataclass(frozen=True)
class Condition:
    """A question about the table, asked one of two ways.

    A `compare` is arithmetic: an operand against a literal or another operand.
    The system answers it itself, the same way every time.

    A `prose` condition is a sentence, handed to a judge. It exists because the
    comparison language is deliberately small and always will be, and because a
    sentence is what someone writing a new game actually has in their head.
    The cost is that the answer becomes a judgement, so anything expressible as
    arithmetic should stay arithmetic.
    """

    kind: str  # "compare" | "prose"
    left: Operand | None = None
    op: str = "=="
    value: Any = None
    other: Operand | None = None
    #: The sentence a judge is asked, for `kind == "prose"`.
    prose: str = ""

    @staticmethod
    def parse(raw: Any, where: str) -> "Condition":
        if isinstance(raw, str):
            _require(raw.strip(), where, "an empty condition asks nothing")
            return Condition(kind="prose", prose=raw.strip())
        _require(isinstance(raw, dict), where, f"expected a condition, got {raw!r}")
        _only(raw, ("prose", "count", "game", "op", "value", "other"), where)
        if "prose" in raw:
            text = str(raw["prose"]).strip()
            _require(text, where + ".prose", "an empty condition asks nothing")
            return Condition(kind="prose", prose=text)
        left = Operand.parse(raw, where, strict=False)
        op = _one_of(raw.get("op", "=="), OPERATORS, where + ".op")
        other = Operand.parse(raw["other"], where + ".other") if "other" in raw else None
        _require(
            ("value" in raw) != (other is not None),
            where,
            "give exactly one of `value` or `other`",
        )
        return Condition(kind="compare", left=left, op=op,
                         value=raw.get("value"), other=other)


@dataclass(frozen=True)
class AnswerDef:
    type: str
    max_words: int = 0
    exclude_self: bool = False
    exclude: Selector | None = None
    options: tuple[Any, ...] = ()
    count: int = 0
    minimum: float | None = None
    maximum: float | None = None

    @staticmethod
    def parse(raw: Any, where: str) -> "AnswerDef":
        _require(isinstance(raw, dict), where, f"expected an answer spec, got {raw!r}")
        _only(raw, ("type", "max_words", "exclude_self", "exclude", "options",
                    "count", "min", "max"), where)
        kind = _one_of(raw.get("type"), ANSWER_TYPES, where + ".type")
        if kind == "choice":
            _require(raw.get("options"), where, "a choice needs `options`")
        # A string here is silently mangled: tuple("$hand") becomes five
        # one-character options and the file loads clean. Anything that is not
        # a list is a mistake, and this is the one place a mistake produces a
        # plausible-looking answer spec rather than an error.
        _require(
            "options" not in raw or isinstance(raw["options"], list),
            where + ".options",
            f"is a list of values, not {type(raw.get('options')).__name__}. "
            f"Options drawn from state are not supported yet.",
        )
        return AnswerDef(
            type=kind,
            max_words=int(raw.get("max_words", 0)),
            exclude_self=bool(raw.get("exclude_self", False)),
            exclude=Selector.parse(raw["exclude"], where + ".exclude")
            if "exclude" in raw
            else None,
            options=tuple(raw.get("options", ())),
            count=int(raw.get("count", 0)),
            minimum=raw.get("min"),
            maximum=raw.get("max"),
        )


#: What a step writes to, and therefore what shape must come back.
#:
#:   table    one object of table attributes
#:   players  one record per player, order irrelevant — the seed deals them
#:   each     a record per named player, assigned exactly as given
#:
#: `players` and `each` differ only in who decides who gets what, and that is
#: the whole distinction between dealing a hand and naming a winner. `players`
#: keeps a match replayable from its seed; `each` is for the games where
#: position is the point and shuffling would destroy the answer.
UPDATE_TARGETS = ("table", "players", "each")


@dataclass(frozen=True)
class UpdatesDef:
    """Which attributes a step writes, grouped by what they are written to.

    Replaces a pair of parallel keys (`into`, `into_table`) that could only ever
    express two of the three cases. Naming the target is what lets the engine
    derive both halves of the call — the shape it asks for and the code that
    applies the answer — from one declaration.
    """

    targets: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @staticmethod
    def parse(raw: Any, where: str) -> "UpdatesDef":
        _require(isinstance(raw, dict), where, f"expected an object, got {raw!r}")
        _only(raw, UPDATE_TARGETS, where)
        _require(bool(raw), where, "names nothing to update")
        out: dict[str, tuple[str, ...]] = {}
        for target, keys in raw.items():
            _require(isinstance(keys, list) and keys, f"{where}.{target}",
                     "is a non-empty list of attribute names")
            out[target] = tuple(str(k) for k in keys)
        return UpdatesDef(targets=out)

    def __bool__(self) -> bool:
        return bool(self.targets)


@dataclass(frozen=True)
class Branch:
    """What happens on one of the two outcomes a tally can have."""

    do: tuple["Operation", ...] = ()
    text: str = ""
    llm: str = ""
    to: Selector = field(default_factory=lambda: Selector(kind="all"))

    @staticmethod
    def parse(raw: Any, where: str) -> "Branch":
        _require(isinstance(raw, dict), where, f"expected an object, got {raw!r}")
        _only(raw, ("do", "text", "llm", "to"), where)
        return Branch(
            do=tuple(Operation.parse(o, f"{where}.do[{i}]")
                     for i, o in enumerate(raw.get("do", ()))),
            text=str(raw.get("text", "")),
            llm=str(raw.get("llm", "")),
            to=Selector.parse(raw.get("to", "all"), where + ".to"),
        )


@dataclass(frozen=True)
class OutcomeDef:
    """What a step does with the answers it just gathered.

    Asking, reducing, applying and announcing are one act in a game and were
    three things here: a `poll` that bound a name, an `update` that read it
    back, and a guard on every operation for the case where the tally chose
    nobody. The plumbing was visible and the tie was easy to forget — Mafia
    forgot it, and a tied vote told the table nothing at all.

    Naming both outcomes is the point. A tally either settles on someone or it
    does not, and a schema that names only the first invites a game that
    handles only the first.
    """

    chosen: Branch | None = None
    none: Branch | None = None

    @staticmethod
    def parse(raw: Any, where: str) -> "OutcomeDef":
        _require(isinstance(raw, dict), where, f"expected an object, got {raw!r}")
        _only(raw, ("chosen", "none"), where)
        _require(bool(raw), where, "names neither outcome, so it does nothing")
        return OutcomeDef(
            chosen=Branch.parse(raw["chosen"], where + ".chosen")
            if "chosen" in raw else None,
            none=Branch.parse(raw["none"], where + ".none")
            if "none" in raw else None,
        )


@dataclass(frozen=True)
class BroadcastDef:
    """What the table is told about an answer somebody just gave.

    Replaces a visibility enum and a template name that were really one
    decision in two fields. A broadcast says three things: who hears it, how it
    is worded, and whether a model does the wording.

    Absent means nobody is told. That is the safe default for a hidden-role
    game: a step has to ask to be published.
    """

    #: Who hears it, as a selector. `others` is the usual case: the author
    #: already knows what they said, and echoing it back reads as somebody
    #: else's words.
    to: Selector = field(default_factory=lambda: Selector(kind="others"))
    #: A template key from the game's `text` block.
    text: str = ""
    #: A prompt. With a model wired in, it writes the broadcast instead.
    llm: str = ""

    @staticmethod
    def parse(raw: Any, where: str) -> "BroadcastDef":
        if isinstance(raw, str):
            return BroadcastDef(to=Selector.parse(raw, where))
        _require(isinstance(raw, dict), where, f"expected a broadcast, got {raw!r}")
        _only(raw, ("to", "text", "llm"), where)
        return BroadcastDef(
            to=Selector.parse(raw.get("to", "others"), where + ".to"),
            text=str(raw.get("text", "")),
            llm=str(raw.get("llm", "")),
        )


@dataclass(frozen=True)
class VerifyDef:
    """A check the system performs itself, rather than trusting a model."""

    tally: str | None = None
    on_tie: str = "nobody"
    bind: str | None = None

    @staticmethod
    def parse(raw: Any, where: str) -> "VerifyDef":
        _require(isinstance(raw, dict), where, f"expected a verify block, got {raw!r}")
        _only(raw, ("tally", "on_tie", "bind"), where)
        tally = raw.get("tally")
        if tally is not None:
            tally = _one_of(tally, TALLIES, where + ".tally")
        return VerifyDef(
            tally=tally,
            on_tie=_one_of(raw.get("on_tie", "nobody"), ON_TIE, where + ".on_tie"),
            bind=raw.get("bind"),
        )


@dataclass(frozen=True)
class Operation:
    """One declared state change. The system performs these; a model does not."""

    op: str
    args: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def parse(raw: Any, where: str) -> "Operation":
        _require(
            isinstance(raw, dict) and len(raw) == 1,
            where,
            "an operation is a single-key object",
        )
        op = next(iter(raw))
        _one_of(op, OPERATIONS, where)
        args = raw[op]
        _require(isinstance(args, dict), where, f"{op} takes an object of arguments")
        return Operation(op=op, args=args)


@dataclass(frozen=True)
class StepDef:
    use: str
    #: Names the step. Becomes the fact type, the action id an agent answers
    #: with, the entry in the record, and the log tag. An identifier, not a
    #: sentence: it used to be shown to players as their instruction when a
    #: step declared no wording, which read sensibly only because these labels
    #: happen to be noun phrases. Call a step `s2` and that prompt is noise.
    label: str

    #: Derived from `use`, not declared. `ask` takes players one at a time so
    #: each hears the last; `poll` takes them together so none does. That was a
    #: `mode` field with a default, which meant a step addressing two players
    #: silently inherited whichever behaviour the default happened to be.
    #: The part of the round this belongs to: "night", "day", "the mission".
    #: Purely a game's own word, carried into the log and the console.
    phase: str = ""
    when: Condition | None = None
    to: Selector = field(default_factory=lambda: Selector(kind="acting"))
    mode: str = "simultaneous"
    answer: AnswerDef | None = None
    #: What to do with the answers once they are reduced: apply state, and say
    #: what happened. Both outcomes are named, so a tie cannot be forgotten.
    outcome: OutcomeDef | None = None
    #: What the table is told about the answers this step collects. None means
    #: nothing is said, which is what a secret ballot wants.
    broadcast: BroadcastDef | None = None
    #: For `check`: which endings this step tests, by name. Empty means all of
    #: them. This is the step's input, in the same way `into` is
    #: `initialize`'s: a check after the night need not ask about an ending
    #: only a vote can reach.
    against: tuple[str, ...] = ()
    #: For `initialize`: which player attributes the model fills. Naming them
    #: is what lets the engine build both halves of the call — the schema it
    #: shows the model, and the validator it checks the reply against. Without
    #: it the engine knows a model should be asked something, and nothing more.
    updates: UpdatesDef | None = None
    #: For `initialize`: how many players must end up with each value, checked
    #: before anything is dealt.
    #:
    #:     "requires": {"role": {"mafia": 1, "detective": 1}}
    #:
    #: The prompt already says "exactly one mafia", but a sentence is a request
    #: and this is the check. Four villagers and no mafia passes every type and
    #: value test and produces a game nobody can win; that is the failure this
    #: catches, and it is not one the schema can see.
    #:
    #: A count may be a number, or a two-item list for a range. Values not
    #: named are unconstrained, so "one mafia, everyone else whatever the
    #: prompt says" needs only the one entry.
    requires: dict[str, dict[str, Any]] = field(default_factory=dict)
    #: What this step asks the model for, in the game's own words. The action
    #: fixes the shape of the call; this is the only part a game writes.
    #:
    #: Declaring it is what turns the model on for this step — there is no
    #: separate switch. There used to be a `compose` flag beside it, and the
    #: two disagreed: `initialize` and `check` read `llm` directly, while
    #: `ask` and `poll` ignored it unless `compose` was also set. Writing a
    #: prompt and having it silently do nothing is the worst of the options.
    #:
    #: Absent, the step uses its `text` template, which is free, reproducible
    #: and cannot hallucinate.
    llm: str = ""
    #: How long the message a model writes for this step may be. Distinct
    #: from `answer.max_words`, which caps what a *player* replies: a
    #: briefing has no answer at all and still wants a length. Asking for
    #: a limit in the prose with nothing enforcing it is the worst of both.
    max_words: int = 0
    #: What this message is about — usually a binding an earlier step left,
    #: like `$target` or `$voted_out`. A template could already reach those
    #: through `{target}`; a prompt could not, so a model asked to "announce
    #: who died overnight" was never told who. Naming the subject puts it in
    #: both.
    about: str = ""
    #: For `tell`: what sort of message this is, which decides what the engine
    #: assembles into the request. See TELL_KINDS.
    kind: str = "message"
    #: For `sync`: which attributes to send. Empty sends everything the
    #: recipient may see, which is the usual case and the safe default —
    #: naming fields can only ever narrow it, never widen it.
    fields: tuple[str, ...] = ()
    #: For `sync`: whose state goes where.
    #:
    #:   self    each addressed player receives their own view — what they
    #:           know, including what they may see of everyone else
    #:   others  each addressed player's state is sent to everyone *but* them,
    #:           filtered by what each recipient is entitled to see
    #:
    #: `self` answers "what do I know?". `others` answers "what has just
    #: changed about them?", which is a different message even when it carries
    #: the same facts.
    sync_mode: str = "self"
    deadline_s: int | None = None
    on_timeout: Any = "random"
    verify: VerifyDef | None = None
    do: tuple[Operation, ...] = ()
    text: str | None = None

    @staticmethod
    def parse(raw: Any, index: int, where: str | None = None) -> "StepDef":
        where = where or f"steps[{index}]"
        _require(isinstance(raw, dict), where, f"expected an object, got {raw!r}")
        use = _one_of(raw.get("use"), KINDS, where + ".use")
        _only(raw, COMMON_KEYS + ACTION_KEYS[use], where + f" (a {use!r} step)")
        mode = "sequential" if use == "ask" else "simultaneous"
        _require(
            use != "initialize" or raw.get("updates"),
            where + ".updates",
            "an `initialize` step must say what it writes, e.g. "
            '{"updates": {"players": ["role"]}}',
        )
        _require(
            use in ASKING_KINDS or "outcome" not in raw,
            where + ".outcome",
            "only an `ask` or `poll` has answers to act on",
        )
        _require(
            use == "tell" or "kind" not in raw,
            where + ".kind",
            "only a `tell` has kinds; the other actions differ by name",
        )
        _require(
            raw.get("kind") != "status_update" or raw.get("about"),
            where + ".about",
            "a status update must say which player it is about",
        )
        _require(
            use in ("sync", "tell") or "fields" not in raw,
            where + ".fields",
            "only `sync` and a `tell` status update name fields",
        )
        _require(
            use == "sync" or "mode" not in raw,
            where + ".mode",
            "only a `sync` step takes a mode; `ask` and `poll` differ by the "
            "action name, not by a flag",
        )
        _require(
            use in ASKING_KINDS or "answer" not in raw,
            where + ".answer",
            f"a {use!r} step takes no `answer`: it does not wait for one. "
            f"Use `ask` or `poll` to ask a question.",
        )
        _require(
            use not in ASKING_KINDS or "answer" in raw,
            where + ".answer",
            f"an {use!r} step waits for a reply, so it must say what a reply "
            f"may be. Use `tell` to send a message without waiting.",
        )
        _require(
            use != "check" or not raw.get("do"),
            where + ".do",
            "a `check` step decides whether to end; it changes nothing",
        )
        return StepDef(
            use=use,
            label=str(raw.get("label", use)),

            phase=str(raw.get("phase", "")),
            when=Condition.parse(raw["when"], where + ".when") if "when" in raw else None,
            to=Selector.parse(raw.get("to"), where + ".to"),
            mode=mode,
            answer=AnswerDef.parse(raw["answer"], where + ".answer")
            if "answer" in raw
            else None,
            outcome=OutcomeDef.parse(raw["outcome"], where + ".outcome")
            if "outcome" in raw
            else None,
            broadcast=BroadcastDef.parse(raw["broadcast"], where + ".broadcast")
            if "broadcast" in raw
            else None,
            max_words=int(raw.get("max_words", 0)),
            about=str(raw.get("about", "")),
            kind=_one_of(raw.get("kind", "message"), TELL_KINDS, where + ".kind")
            if use == "tell"
            else "message",
            fields=tuple(raw.get("fields", ())),
            sync_mode=_one_of(raw.get("mode", "self"), SYNC_MODES, where + ".mode")
            if use == "sync"
            else "self",
            updates=UpdatesDef.parse(raw["updates"], where + ".updates")
            if "updates" in raw
            else None,
            requires=dict(raw.get("requires") or {}),
            against=tuple(raw.get("against", ())),
            llm=str(raw.get("llm", "")),
            deadline_s=raw.get("deadline_s"),
            on_timeout=raw.get("on_timeout", "random"),
            verify=VerifyDef.parse(raw["verify"], where + ".verify")
            if "verify" in raw
            else None,
            do=tuple(
                Operation.parse(o, f"{where}.do[{i}]")
                for i, o in enumerate(raw.get("do", ()))
            ),
            text=raw.get("text"),
        )

    @property
    def asks(self) -> bool:
        """Does this step stop the game and wait?

        The distinction the whole loop turns on. An `ask` carrying an answer
        spec is an action: the addressed players owe a reply and nothing moves
        until they give one. An `ask` without one is information: it is
        delivered, acknowledged, and the game carries straight on.
        """
        return self.use in ASKING_KINDS

    @property
    def informs(self) -> bool:
        """An `ask` that wants no reply. Delivered, never waited on."""
        return self.use == "tell"


@dataclass(frozen=True)
class EndRule:
    #: The name a step selects this ending by, and the label the model answers
    #: with. Named rather than positional because `end[1]` tells a reader
    #: nothing and tells a model less.
    name: str
    when: Condition
    result: str
    reason: str = ""
    #: What is made public when the game ends this way. Per ending, because
    #: some games reveal different things depending on how they finished.
    reveal: tuple[str, ...] = ()
    #: The template that announces this ending. Falls back to `game_over`.
    text: str = ""
    #: Or a prompt, and a model writes the announcement instead. Every
    #: announcement in the engine takes one or the other, so a game chooses
    #: per message whether it wants a fixed sentence or a written one.
    llm: str = ""

    @staticmethod
    def parse(name: str, raw: Any, where: str) -> "EndRule":
        _require(isinstance(raw, dict), where, f"expected an ending, got {raw!r}")
        _only(raw, ("when", "result", "reason", "reveal", "text", "llm"), where)
        _require("when" in raw, where, "needs a `when`")
        _require("result" in raw, where, "needs a `result`")
        return EndRule(
            name=name,
            when=Condition.parse(raw["when"], where + ".when"),
            result=str(raw["result"]),
            reason=str(raw.get("reason", "")),
            reveal=tuple(raw.get("reveal", ())),
            text=str(raw.get("text", "")),
            llm=str(raw.get("llm", "")),
        )


#: Legacy per-seat fields on the kernel's Seat, kept from Milestone 1 because
#: the console and the existing audience selectors read them. They are game
#: vocabulary living in a game-agnostic kernel, which is a wart; until it is
#: removed, a definition says which of *its* attributes fills each one instead
#: of the engine guessing that they are called "role" and "faction".
DISPLAY_FIELDS = ("role", "faction")


@dataclass(frozen=True)
class DealDef:
    into: tuple[str, ...]
    by_players: dict[int, list[dict[str, Any]]]

    def plan(self, players: int) -> list[dict[str, Any]]:
        """The role rows for this table size, filling forward.

        Sizes are declared where they change, so a six-player table uses the
        `4` row and a nine-player table uses the `7` row.
        """
        sizes = sorted(s for s in self.by_players if s <= players)
        if not sizes:
            raise DefinitionError(
                f"deal: no distribution declared at or below {players} players"
            )
        rows, out = self.by_players[sizes[-1]], []
        fixed = sum(int(r.get("count", 1)) for r in rows if not r.get("fill"))
        for row in rows:
            n = players - fixed if row.get("fill") else int(row.get("count", 1))
            if n < 0:
                raise DefinitionError(
                    f"deal: {players} players is fewer than the {fixed} the "
                    f"distribution at size {sizes[-1]} requires"
                )
            out += [{k: v for k, v in row.items() if k not in ("count", "fill")}] * n
        return out


@dataclass(frozen=True)
class Limits:
    rounds: int = 20
    #: The ceiling a game may not raise `rounds` past, so a typo in one file
    #: cannot make a match run for an hour.
    rounds_max: int = 200
    actions_max: int = 400
    deadline_s: int = 120


@dataclass(frozen=True)
class GameDefinition:
    id: str
    name: str
    min_players: int
    max_players: int
    statuses: tuple[StatusDef, ...]
    player_attributes: tuple[AttributeDef, ...]
    game_attributes: tuple[AttributeDef, ...]
    #: Runs once, after the deal and before round one. Declared like any other
    #: steps, so a game says for itself what its players are told to begin
    #: with, who is told it, and in what words. The engine used to emit a
    #: briefing and an allies notice on its own initiative, which meant a game
    #: that wanted neither got both and a game that wanted three got one.
    setup: tuple[StepDef, ...]
    steps: tuple[StepDef, ...]
    end: tuple[EndRule, ...]
    allies_by: Allegiance | None = None
    #: Maps a kernel display field to one of this game's attributes. Empty is
    #: fine: the seat simply shows no role, and nothing else changes.
    display: dict[str, str] = field(default_factory=dict)
    deal: DealDef | None = None
    reveal: tuple[str, ...] = ()
    limits: Limits = field(default_factory=Limits)
    text: dict[str, str] = field(default_factory=dict)
    rules: str = ""
    #: One line for a menu. Declared, not derived: slicing the first sentence
    #: off the rules put a game's words in the server's code, which is the
    #: thing this milestone exists to stop.
    blurb: str = ""

    # -- lookups -------------------------------------------------------

    @property
    def initial_status(self) -> str:
        return next(s.id for s in self.statuses if s.initial)

    def status(self, id: str) -> StatusDef | None:
        return next((s for s in self.statuses if s.id == id), None)

    def player_attribute(self, key: str) -> AttributeDef | None:
        return next((a for a in self.player_attributes if a.key == key), None)

    def game_attribute(self, key: str) -> AttributeDef | None:
        return next((a for a in self.game_attributes if a.key == key), None)


# ----------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------


def parse(raw: dict[str, Any]) -> GameDefinition:
    """Read a definition and refuse anything that cannot be checked later."""
    _require(isinstance(raw, dict), "<root>", "a definition is an object")
    version = raw.get("schema")
    _require(
        version == SCHEMA_VERSION,
        "schema",
        f"this runtime reads schema {SCHEMA_VERSION}, the file says {version!r}",
    )

    meta = raw.get("meta") or {}
    _require(bool(meta.get("id")), "meta.id", "required")
    players = meta.get("players") or {}
    lo, hi = int(players.get("min", 2)), int(players.get("max", 12))
    _require(lo <= hi, "meta.players", f"min {lo} is above max {hi}")

    statuses = tuple(
        StatusDef(
            id=str(s["id"]),
            acts=bool(s.get("acts", True)),
            initial=bool(s.get("initial", False)),
        )
        for s in raw.get("statuses", [])
    )
    _require(bool(statuses), "statuses", "at least one is required")
    initial = [s for s in statuses if s.initial]
    _require(len(initial) == 1, "statuses", "exactly one must set `initial: true`")

    attrs = raw.get("attributes") or {}
    player_attrs = tuple(
        _attribute(a, PLAYER_VISIBILITY, f"attributes.player[{i}]")
        for i, a in enumerate(attrs.get("player", []))
    )
    game_attrs = tuple(
        _attribute(a, GAME_VISIBILITY, f"attributes.game[{i}]")
        for i, a in enumerate(attrs.get("game", []))
    )

    deal = None
    if "deal" in raw:
        d = raw["deal"]
        deal = DealDef(
            into=tuple(str(k) for k in d.get("into", ())),
            by_players={int(k): list(v) for k, v in (d.get("by_players") or {}).items()},
        )
        _require(bool(deal.into), "deal.into", "required")
        _require(bool(deal.by_players), "deal.by_players", "required")

    steps = tuple(StepDef.parse(s, i) for i, s in enumerate(raw.get("steps", [])))
    setup = tuple(
        StepDef.parse(s, i, where=f"setup[{i}]")
        for i, s in enumerate(raw.get("setup", []))
    )
    for i, step in enumerate(setup):
        _require(step.use in SETUP_KINDS, f"setup[{i}].use",
                 f"setup takes {list(SETUP_KINDS)}; {step.use!r} belongs in `steps`")
        _require(step.answer is None, f"setup[{i}].answer",
                 "setup runs before anybody is greeted, so nothing can be asked "
                 "of them there; put the question in `steps`")
    _require(bool(steps), "steps", "at least one is required")

    endings = raw.get("end") or {}
    _require(
        isinstance(endings, dict),
        "end",
        "endings are named: a map of name to ending, not a list. Declaration "
        "order still decides which wins when two are true at once.",
    )
    end = tuple(
        EndRule.parse(name, e, f"end.{name}") for name, e in endings.items()
    )
    _require(bool(end), "end", "a game needs at least one way to finish")

    limits_raw = raw.get("limits") or {}
    definition = GameDefinition(
        id=str(meta["id"]),
        name=str(meta.get("name", meta["id"])),
        blurb=str(meta.get("blurb", "")),
        min_players=lo,
        max_players=hi,
        statuses=statuses,
        player_attributes=player_attrs,
        game_attributes=game_attrs,
        setup=setup,
        steps=steps,
        end=end,
        allies_by=Allegiance.parse(raw["allies_by"], "allies_by")
        if "allies_by" in raw
        else None,
        display=dict(raw.get("display") or {}),
        deal=deal,
        reveal=tuple(raw.get("reveal", ())),
        limits=Limits(
            rounds=int(limits_raw.get("rounds", 20)),
            rounds_max=int(limits_raw.get("rounds_max", 200)),
            actions_max=int(limits_raw.get("actions_max", 400)),
            deadline_s=int(limits_raw.get("deadline_s", 120)),
        ),
        text=dict(raw.get("text") or {}),
        rules=str(raw.get("rules", "")),
    )
    _check_references(definition)
    _check_text(definition)
    _check_endings(definition)
    _check_sentinels(definition)
    _check_prompts(definition)
    _check_requires(definition)
    return definition


def _attribute(raw: Any, allowed: tuple[str, ...], where: str) -> AttributeDef:
    _require(isinstance(raw, dict), where, f"expected an object, got {raw!r}")
    _require("key" in raw, where, "needs a `key`")
    _only(raw, ("key", "visible", "type", "initial", "mutable", "values"), where)
    return AttributeDef(
        key=str(raw["key"]),
        visible=_one_of(raw.get("visible"), allowed, where + ".visible"),
        type=_one_of(raw.get("type", "text"), TYPES, where + ".type"),
        initial=raw.get("initial"),
        mutable=bool(raw.get("mutable", True)),
        values=tuple(raw.get("values", ())),
    )


def _check_requires(d: GameDefinition) -> None:
    """A `requires` must name attributes and values the game declares."""
    for i, step in enumerate(d.setup):
        for key, counts in step.requires.items():
            where = f"setup[{i}].requires.{key}"
            attribute = d.player_attribute(key)
            _require(attribute is not None, where,
                     f"{key!r} is not a declared player attribute")
            # Either target writes players, so a roster requirement applies
            # to both. Checking only `players` meant a game that let the model
            # assign could not state its roster at all.
            t = step.updates.targets if step.updates else {}
            filled = tuple(t.get("players", ())) + tuple(t.get("each", ()))
            _require(key in filled, where,
                     f"{key!r} is not one of the player attributes this step "
                     f"writes; it fills {list(filled)}")
            _require(isinstance(counts, dict), where, "takes a map of value to count")
            for value, count in counts.items():
                spot = f"{where}.{value}"
                if attribute.values:
                    _require(value in attribute.values, spot,
                             f"{value!r} is not one of {list(attribute.values)}")
                if isinstance(count, list):
                    _require(len(count) == 2 and all(isinstance(c, int) for c in count),
                             spot, "a range is two whole numbers")
                    _require(count[0] <= count[1], spot, "the range is backwards")
                else:
                    _require(isinstance(count, int) and count >= 0, spot,
                             "a count is a whole number, or a two-item range")


def _check_prompts(d: GameDefinition) -> None:
    """A step that asks something must say what it is asking.

    Either `text` naming a template, or `llm` so a model writes it. There used
    to be a third field, `prompt`, holding the words themselves — so a game
    wrote an instruction one way for a `tell` and another way for an `ask`,
    and one of them indirected through the text block while the other did not.
    """
    for i, step in enumerate(d.steps):
        if not step.asks:
            continue
        _require(
            bool(step.text or step.llm),
            f"steps[{i}]",
            f"{step.label!r} asks players for an answer, so it needs `text` "
            f"naming a template that tells them what to do, or an `llm` to "
            f"write one",
        )
        if step.text:
            _wording(step.text, d.text, f"steps[{i}].text")


def _check_sentinels(d: GameDefinition) -> None:
    """An `unless` guard must name a value the engine can actually produce.

    `"unless": "noboby"` used to load and then never match, so the operation it
    guarded ran on a binding that named no one. The guard was written to stop
    exactly that, and a typo turned it off in silence.
    """
    for where, step in (
        [(f"setup[{i}]", x) for i, x in enumerate(d.setup)]
        + [(f"steps[{i}]", x) for i, x in enumerate(d.steps)]
    ):
        for j, op in enumerate(step.do):
            guard = op.args.get("unless")
            if guard is None:
                continue
            _require(
                guard in (NOBODY, RERUN),
                f"{where}.do[{j}].unless",
                f"{guard!r} is not a value a tally can produce. "
                f"Expected {NOBODY!r} or {RERUN!r}",
            )


def _check_endings(d: GameDefinition) -> None:
    """A check step must name endings the game actually declares."""
    known = {rule.name for rule in d.end}
    for i, step in enumerate(d.steps):
        for name in step.against:
            _require(
                name in known,
                f"steps[{i}].against",
                f"{name!r} is not a declared ending. This game has: "
                f"{', '.join(sorted(known))}",
            )
    for rule in d.end:
        for key in rule.reveal:
            _require(
                d.player_attribute(key) is not None,
                f"end.{rule.name}.reveal",
                f"{key!r} is not a declared player attribute",
            )
        if rule.text:
            _wording(rule.text, d.text, f"end.{rule.name}.text")


def _wording(value: str, declared: dict[str, str], where: str) -> None:
    """A message may be the words themselves or a name in the `text` block.

    Every template in the first game was referenced exactly once, so the
    indirection cost a lookup on every read and bought no reuse. Naming one is
    still allowed, for wording a game genuinely shares between steps.

    A bare identifier that names nothing is the mistake worth catching: it is
    almost certainly a typo'd template name, and taken literally it would send
    a player the word `found_dad`.
    """
    if value in declared:
        return
    _require(
        " " in value or "{" in value,
        where,
        f"{value!r} is neither a declared template nor a sentence. Write the "
        f"words here, or add {value!r} to the `text` block.",
    )


def _check_text(d: GameDefinition) -> None:
    """Every message the engine will need, the game must have written.

    The engine holds no wording of its own, so a missing template is not a
    cosmetic gap: it is a message that goes out empty. Caught at load, where it
    is one line to fix, rather than in front of players three rounds in.
    """
    text = d.text

    if d.end and not all(r.llm or r.text for r in d.end):
        _require("game_over" in text, "text.game_over",
                 "a game that can end must say how the ending is announced, "
                 "with `text.game_over` or an `llm` on each ending")

    for where, step in (
        [(f"setup[{i}]", s) for i, s in enumerate(d.setup)]
        + [(f"steps[{i}]", s) for i, s in enumerate(d.steps)]
    ):
        spec = step.broadcast
        if spec and not spec.llm:
            # A free-text answer is its own message: the player's words are
            # what the table hears, and the engine has nothing to add but who
            # said it. Anything else — a seat number, a choice — is not a
            # sentence, so the game has to say how it is announced.
            speaks = step.answer is not None and step.answer.type == "text"
            if spec.text:
                _wording(spec.text, text, where + ".broadcast.text")
            else:
                _require(
                    speaks,
                    where + ".broadcast",
                    f"a {step.answer.type if step.answer else 'silent'} answer "
                    f"is not a message on its own, so this needs `text` giving "
                    f"the words, or `llm` to have them written",
                )
        if step.text:
            _wording(step.text, text, where + ".text")
        # Any operation may word itself, and a disclosure must, because its
        # message is the disclosure.
        for j, op in enumerate(step.do):
            wording = op.args.get("text")
            if wording:
                _wording(str(wording), text, f"{where}.do[{j}].text")
            elif op.op == "disclose" and not op.args.get("llm"):
                _require(False, f"{where}.do[{j}]",
                         "a disclosure is a message, so it needs `text` giving "
                         "the words, or `llm` to have them written")


def _check_references(d: GameDefinition) -> None:
    """Every name a definition uses must resolve. Caught here, not mid-match."""
    player_keys = {a.key for a in d.player_attributes}
    game_keys = {a.key for a in d.game_attributes}
    status_ids = {s.id for s in d.statuses}

    if d.allies_by:
        _require(
            d.allies_by.attribute in player_keys,
            "allies_by",
            f"{d.allies_by.attribute!r} is not a declared player attribute",
        )
    for kernel_field, attribute in d.display.items():
        _require(
            kernel_field in DISPLAY_FIELDS,
            f"display.{kernel_field}",
            f"expected one of {list(DISPLAY_FIELDS)}",
        )
        _require(
            attribute in player_keys,
            f"display.{kernel_field}",
            f"{attribute!r} is not a declared player attribute",
        )

    if d.deal:
        for key in d.deal.into:
            _require(key in player_keys, "deal.into", f"{key!r} is not declared")
        for size, rows in d.deal.by_players.items():
            for row in rows:
                for key in row:
                    if key in ("count", "fill"):
                        continue
                    _require(
                        key in player_keys,
                        f"deal.by_players[{size}]",
                        f"{key!r} is not a declared player attribute",
                    )

    bound: set[str] = set()
    # Setup is checked on the same terms as a round's steps: a selector naming
    # an attribute nobody declared is a typo wherever it appears.
    numbered = [(f"setup[{i}]", s) for i, s in enumerate(d.setup)]
    numbered += [(f"steps[{i}]", s) for i, s in enumerate(d.steps)]
    for where, step in numbered:
        if step.to.kind == "attribute":
            _require(step.to.attribute in player_keys, where + ".to",
                     f"{step.to.attribute!r} is not a declared player attribute")
        if step.answer and step.answer.exclude and step.answer.exclude.kind == "attribute":
            _require(step.answer.exclude.attribute in player_keys,
                     where + ".answer.exclude",
                     f"{step.answer.exclude.attribute!r} is not declared")
        if step.when:
            _check_condition(step.when, player_keys, game_keys, where + ".when")
        if step.verify and step.verify.bind:
            bound.add(step.verify.bind)
        if step.text:
            _wording(step.text, d.text, where + ".text")
        for j, op in enumerate(step.do):
            _check_operation(op, bound, player_keys, game_keys, status_ids,
                             f"{where}.do[{j}]")

    for i, rule in enumerate(d.end):
        _check_condition(rule.when, player_keys, game_keys, f"end[{i}].when")
    for key in d.reveal:
        _require(key in player_keys, "reveal", f"{key!r} is not a declared attribute")


def _check_condition(c: Condition, player_keys, game_keys, where: str) -> None:
    if c.kind == "prose":
        return  # nothing to check against: a judge reads it, not the loader
    for side, operand in (("", c.left), (".other", c.other)):
        if operand is None:
            continue
        if operand.kind == "game":
            _require(operand.attribute in game_keys, where + side,
                     f"{operand.attribute!r} is not a declared table attribute")
        elif operand.selector and operand.selector.kind == "attribute":
            _require(operand.selector.attribute in player_keys, where + side,
                     f"{operand.selector.attribute!r} is not a declared player attribute")


def _check_operation(op: Operation, bound, player_keys, game_keys, status_ids,
                     where: str) -> None:
    args = op.args
    for name in _bindings_in(args):
        _require(name in bound, where,
                 f"${name} is used before any step binds it")

    if op.op == "set_status":
        _require(args.get("to") in status_ids, where,
                 f"{args.get('to')!r} is not a declared status")
    elif op.op == "disclose":
        _require("attribute" in args, where, "disclose needs an `attribute`")
        _require(args["attribute"] in player_keys, where,
                 f"{args['attribute']!r} is not a declared player attribute")
    elif op.op in ("set", "adjust", "append", "remove"):
        key = args.get("key")
        _require(key in player_keys or key in game_keys, where,
                 f"{key!r} is not a declared attribute")


def _bindings_in(value: Any) -> list[str]:
    if isinstance(value, str) and value.startswith("$"):
        return [value[1:]]
    if isinstance(value, dict):
        return [n for v in value.values() for n in _bindings_in(v)]
    if isinstance(value, list):
        return [n for v in value for n in _bindings_in(v)]
    return []
