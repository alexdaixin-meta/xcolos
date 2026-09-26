"""Flow state: attributes, the record, selectors, conditions and operations.

This is the game-shaped state the flow engine keeps alongside the kernel's own.
The kernel knows seats, facts and audiences. This knows what a game declared:
which attributes exist, who may see them, who is allied with whom, and what
every player has done.

Nothing here knows about Mafia. Every name it handles came out of a definition.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from xcolos.games.definition import (
    AttributeDef,
    Condition,
    GameDefinition,
    Operand,
    NOBODY,
    RERUN,
    Selector,
)


class FlowError(Exception):
    """A definition asked for something the state cannot do."""


@dataclass
class Answer:
    """One thing one player did, at one step of one round."""

    round: int
    step: str
    player: int
    value: Any
    visible: str = "none"
    reason: str = ""

    def to_json(self) -> dict[str, Any]:
        return {
            "round": self.round,
            "step": self.step,
            "player": self.player,
            "value": self.value,
            "visible": self.visible,
        }


class FlowState:
    """Attributes and the record, for one game driven by a definition."""

    def __init__(self, definition: GameDefinition, players: list[int]) -> None:
        self.definition = definition
        self.players = list(players)

        self.status: dict[int, str] = {
            p: definition.initial_status for p in self.players
        }
        self.player_attributes: dict[int, dict[str, Any]] = {
            p: {a.key: a.initial for a in definition.player_attributes}
            for p in self.players
        }
        self.game_attributes: dict[str, Any] = {
            a.key: a.initial for a in definition.game_attributes
        }

        #: Everything anybody has done. The single source of truth for a tally,
        #: so a vote count is a query rather than a number kept on a player.
        self.record: list[Answer] = []

        #: Named results from `verify`, valid for the round that made them.
        self.bindings: dict[str, Any] = {}

        #: Facts the system decided to tell somebody, from `disclose`. Keyed by
        #: the player who learned it.
        self.disclosed: dict[int, list[dict[str, Any]]] = {p: [] for p in self.players}

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def acts(self, player: int) -> bool:
        status = self.definition.status(self.status[player])
        return bool(status and status.acts)

    def acting(self) -> list[int]:
        return [p for p in self.players if self.acts(p)]

    def attribute(self, player: int, key: str) -> Any:
        return self.player_attributes[player].get(key)

    def allies_of(self, player: int) -> set[int]:
        """Players sharing this one's allegiance, including itself.

        With no `allies_by` declared, or a null value, a player is their own
        only ally. That is what makes a lone villager and a mafia pair work
        from the same `visible: ally` declaration.
        """
        allegiance = self.definition.allies_by
        if not allegiance:
            return {player}
        mine = self.attribute(player, allegiance.attribute)
        if mine is None or not allegiance.knows(mine):
            return {player}
        return {
            p for p in self.players
            if self.attribute(p, allegiance.attribute) == mine
        }

    def can_see(self, viewer: int, owner: int, attribute: AttributeDef) -> bool:
        if attribute.visible == "public":
            return True
        if attribute.visible == "others":
            return viewer != owner
        return owner in self.allies_of(viewer)  # "ally"

    # ------------------------------------------------------------------
    # Selectors and conditions
    # ------------------------------------------------------------------

    def select(
        self, selector: Selector, *, acting_only: bool = True,
        subject: int | None = None,
    ) -> list[int]:
        """Who a selector names. Intersected with "may act" unless told not to.

        Doing the intersection here is why no definition has to remember to
        exclude eliminated players.

        `subject` is who the message is about — the player who just answered.
        Three kinds are relative to them: `others` is everyone else, `ally` is
        their own side, `author` is just them. A selector using one of those
        without a subject names nobody, which is the safe direction.

        An `ids` selector may also hold `$name`, which resolves here against
        whatever an earlier step bound. That is deliberately late: the seat is
        not known when the file loads. A name bound to NOBODY — a tie, or a
        step that was gated out — names nobody rather than seat zero.
        """
        if selector.kind in ("others", "ally", "author"):
            if subject is None:
                return []
            if selector.kind == "author":
                chosen = [subject]
            elif selector.kind == "ally":
                chosen = sorted(self.allies_of(subject))
            else:
                chosen = [p for p in self.players if p != subject]
            return sorted(p for p in chosen if not acting_only or self.acts(p))
        if selector.kind == "ids":
            named = [seat_of(self.bindings.get(r)) for r in selector.refs]
            wanted = list(selector.ids) + [s for s in named if s is not None]
            chosen = [p for p in wanted if p in self.status]
        elif selector.kind == "attribute":
            chosen = [
                p
                for p in self.players
                if (self.attribute(p, selector.attribute) == selector.is_)
                != selector.negate
            ]
        else:  # "acting" or "all"
            chosen = list(self.players)

        if selector.kind == "all":
            return sorted(chosen)
        return sorted(p for p in chosen if not acting_only or self.acts(p))

    def measure(self, operand: Operand) -> Any:
        if operand.kind == "game":
            return self.game_attributes.get(operand.attribute)
        return len(self.select(operand.selector, acting_only=operand.acting_only))

    def holds(self, condition: Condition) -> bool:
        """Whether an arithmetic condition is true right now.

        Prose never reaches here. The executor routes it to a judge, and this
        raises rather than guessing so that a missing route is a crash in a
        test instead of a silently wrong verdict in a match.
        """
        if condition.kind == "prose":
            raise FlowError(
                f"prose needs a judge, not arithmetic: {condition.prose!r}"
            )
        left = self.measure(condition.left)
        right = (
            self.measure(condition.other) if condition.other is not None
            else condition.value
        )
        return _compare(left, condition.op, right)

    # ------------------------------------------------------------------
    # Writing
    # ------------------------------------------------------------------

    def set_status(self, player: int, status: str) -> None:
        if self.definition.status(status) is None:
            raise FlowError(f"{status!r} is not a declared status")
        self.status[player] = status

    def set_attribute(
        self, player: int | None, key: str, value: Any, *, dealing: bool = False
    ) -> None:
        """Write an attribute, honouring whether the game says it may change.

        `mutable: false` means static: set once when the game is dealt, frozen
        after. It was declared on roles in both shipped games and never read,
        so a mid-game operation could rewrite somebody's role and nothing would
        object — the loudest possible bug reported as silence.

        `dealing` is the one exemption, for `initialize`, which is where a
        static attribute gets the value it then keeps.
        """
        attribute = (
            self.definition.game_attribute(key) if player is None
            else self.definition.player_attribute(key)
        )
        if attribute is None:
            kind = "table" if player is None else "player"
            raise FlowError(f"{key!r} is not a declared {kind} attribute")
        if not attribute.mutable and not dealing:
            raise FlowError(
                f"{key!r} is declared static and has already been dealt; "
                f"only an `initialize` step may set it"
            )
        if player is None:
            self.game_attributes[key] = value
        else:
            self.player_attributes[player][key] = value

    def remember(self, answer: Answer) -> None:
        self.record.append(answer)

    def answers_at(self, round: int, step: str) -> dict[int, Any]:
        """What each player answered at one step of one round, in player order."""
        return {
            a.player: a.value
            for a in sorted(self.record, key=lambda a: a.player)
            if a.round == round and a.step == step
        }

    def disclose(self, to: list[int], owner: int, key: str, value: Any) -> None:
        for player in to:
            self.disclosed[player].append({"player": owner, "key": key, "value": value})

    # ------------------------------------------------------------------
    # Views
    # ------------------------------------------------------------------

    def view(self, viewer: int) -> dict[str, Any]:
        """Everything this player may see. The only thing a renderer is given."""
        definition = self.definition
        return {
            "you": {
                "id": viewer,
                "status": self.status[viewer],
                "attributes": {
                    a.key: self.attribute(viewer, a.key)
                    for a in definition.player_attributes
                    if self.can_see(viewer, viewer, a)
                },
            },
            "players": [
                {
                    "id": p,
                    "status": self.status[p],
                    "attributes": {
                        a.key: self.attribute(p, a.key)
                        for a in definition.player_attributes
                        if self.can_see(viewer, p, a)
                    },
                }
                for p in self.players
            ],
            "table": {
                a.key: self.game_attributes.get(a.key)
                for a in definition.game_attributes
                if a.visible == "public"
            },
            "acting": self.acting(),
            "learned": list(self.disclosed[viewer]),
        }


    def full_view(self) -> dict[str, Any]:
        """The whole table, hiding nothing. Only ever given to a judge.

        A judge is not a player and returns no prose to the table, so full
        sight costs nothing and saves it from reasoning about a partial view.
        Never pass this to a renderer.
        """
        return {
            "players": [
                {
                    "id": p,
                    "status": self.status[p],
                    "attributes": dict(self.player_attributes[p]),
                }
                for p in self.players
            ],
            "table": dict(self.game_attributes),
            "acting": self.acting(),
            "record": [a.to_json() for a in self.record],
        }


def seat_of(value: Any) -> int | None:
    """A seat number, or None if this does not name one.

    Bindings hold whatever the last `verify` produced, which is NOBODY for a
    tie, and nothing at all for a step that was gated out. Every place that
    acts on a player goes through here, so the absence of a subject is a thing
    that does not happen rather than a crash or a wrong seat.
    """
    if value is None or value == NOBODY or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _compare(left: Any, op: str, right: Any) -> bool:
    if op == "==":
        return left == right
    if op == "!=":
        return left != right
    if left is None or right is None:
        return False
    if op == "<":
        return left < right
    if op == "<=":
        return left <= right
    if op == ">":
        return left > right
    return left >= right


def tally(values: list[Any], rule: str, on_tie: str, rng) -> Any:
    """Reduce a step's answers to one result, or NOBODY.

    Arithmetic, done by the system. This is the whole reason `verify` exists:
    who a vote fell on should never be a judgement call.
    """
    if not values:
        return NOBODY

    counts: dict[Any, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], _sortable(kv[0])))
    best, top = ordered[0][1], [v for v, n in ordered if n == ordered[0][1]]

    if rule == "unanimity" and len(counts) > 1:
        return NOBODY
    if rule == "majority" and best * 2 <= len(values):
        return NOBODY

    if len(top) == 1:
        return top[0]
    if on_tie == "random":
        return rng.choice(sorted(top, key=_sortable))
    if on_tie == RERUN:
        return RERUN
    return NOBODY


def _sortable(value: Any) -> tuple[int, Any]:
    """Order values of mixed type deterministically, numbers before text."""
    return (0, value) if isinstance(value, (int, float)) else (1, str(value))
