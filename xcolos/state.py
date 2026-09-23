"""Kernel state constructs: seats, zones, offices, audiences, facts.

These are general. The kernel knows about seats, turns, facts, audiences, zones
and offices. It does not know about Mafia or Secret Hitler.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:  # pragma: no cover
    from xcolos.game import Game


#: Seats are numbered from one. They are how players refer to each other out
#: loud, and "seat 0" reads as a machine detail rather than a place at a table.
FIRST_SEAT = 1


class SeatStatus(str, Enum):
    ACTIVE = "active"
    ELIMINATED = "eliminated"
    ABANDONED = "abandoned"


@dataclass
class Seat:
    """A seat, identified by a fixed index assigned once at registration.

    The index is the seat's identity in every message. Display names are
    metadata that never affect ordering, so turn order cannot depend on
    anything an agent controls.
    """

    index: int
    name: str
    role: str | None = None
    faction: str | None = None
    status: SeatStatus = SeatStatus.ACTIVE
    attributes: dict[str, Any] = field(default_factory=dict)
    #: Flags that block a living seat from acting right now, e.g. "silenced".
    eligibility_blocks: set[str] = field(default_factory=set)
    degraded_streak: int = 0
    #: How far the server has *pushed* to this seat. Used by push transports,
    #: where handing the message over and it being received are the same event.
    delivered_upto: int = 0
    #: How far this seat has *fetched*. A pull client may read and then lose
    #: what it read, so fetching is not the same as having it.
    read_upto: int = 0
    #: How far this seat has *confirmed*. Anything past this is re-sent on the
    #: next read, which makes delivery at-least-once with the agent holding the
    #: cursor. An assistant whose context was trimmed simply sees it again.
    acked_upto: int = 0
    #: When this seat last fetched anything, and how often. Presence, for a
    #: player who needs to know whether their session is still paying attention.
    last_read_at: str = ""
    reads: int = 0

    @property
    def alive(self) -> bool:
        return self.status is SeatStatus.ACTIVE

    @property
    def eligible(self) -> bool:
        """Alive and not blocked from acting this phase.

        Skipping is a predicate rather than a single dead flag, because a living
        seat that is silenced must be skipped without being eliminated.
        """
        return self.alive and not self.eligibility_blocks

    def to_json(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "name": self.name,
            "role": self.role,
            "faction": self.faction,
            "status": self.status.value,
            "attributes": dict(self.attributes),
            "eligibility_blocks": sorted(self.eligibility_blocks),
            "degraded_streak": self.degraded_streak,
            "read_upto": self.read_upto,
            "acked_upto": self.acked_upto,
            "last_read_at": self.last_read_at,
            "reads": self.reads,
        }


@dataclass
class Zone:
    """An ordered collection of opaque tokens with a visibility rule.

    A policy deck is an ordered hidden zone. A drawn hand is a zone visible to
    one holder. Zone operations draw from the seeded PRNG, so they replay.
    """

    id: str
    ordered: bool = True
    visibility: str = "none"  # "none" | "holder" | "all"
    tokens: list[str] = field(default_factory=list)
    holder: int | None = None

    def viewers(self, all_seats: Iterable[int]) -> set[int]:
        if self.visibility == "all":
            return set(all_seats)
        if self.visibility == "holder" and self.holder is not None:
            return {self.holder}
        return set()

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "ordered": self.ordered,
            "visibility": self.visibility,
            "count": len(self.tokens),
            "holder": self.holder,
        }


@dataclass(frozen=True)
class Audience:
    """Who is entitled to a fact.

    Visibility is selection, not redaction. A fact is only ever handed to seats
    this resolves to, so adding a field to a payload cannot leak it by omission.
    """

    kind: str  # "all" | "all_except" | "seats" | "faction" | "role" | "none"
    seats: tuple[int, ...] = ()
    value: str | None = None

    @staticmethod
    def all() -> "Audience":
        return Audience(kind="all")

    @staticmethod
    def all_except(*seats: int) -> "Audience":
        """Everyone but these.

        For content a seat authored. It already knows what it said, so putting
        its own words back in its queue wastes tokens and invites it to read
        them as somebody else's.
        """
        return Audience(kind="all_except", seats=tuple(sorted(seats)))

    @staticmethod
    def only(*seats: int) -> "Audience":
        return Audience(kind="seats", seats=tuple(sorted(seats)))

    @staticmethod
    def faction(name: str) -> "Audience":
        return Audience(kind="faction", value=name)

    @staticmethod
    def role(name: str) -> "Audience":
        return Audience(kind="role", value=name)

    @staticmethod
    def none() -> "Audience":
        return Audience(kind="none")

    def resolve(self, seats: dict[int, Seat]) -> set[int]:
        if self.kind == "all":
            return set(seats)
        if self.kind == "all_except":
            return set(seats) - set(self.seats)
        if self.kind == "seats":
            return {i for i in self.seats if i in seats}
        if self.kind == "faction":
            return {i for i, s in seats.items() if s.faction == self.value}
        if self.kind == "role":
            return {i for i, s in seats.items() if s.role == self.value}
        return set()

    def to_json(self) -> dict[str, Any]:
        d: dict[str, Any] = {"kind": self.kind}
        if self.seats:
            d["seats"] = list(self.seats)
        if self.value is not None:
            d["value"] = self.value
        return d


@dataclass(frozen=True)
class Fact:
    """One recorded thing that happened, with the audience entitled to know it.

    The audience is resolved when the fact is created, against the state as it
    stood then. A message sent to the mafia channel stays visible to whoever was
    in that channel at the time, even after someone is eliminated.
    """

    seq: int
    type: str
    payload: dict[str, Any]
    audience: Audience
    entitled: frozenset[int]
    round: int
    phase: str
    #: The turn in flight when this fact was created. Facts are emitted after a
    #: turn returns, so the move record cannot list them; this joins them back.
    turn_seq: int = 0

    def to_fields(self) -> dict[str, Any]:
        """Log fields for this fact.

        Deliberately omits "type" and "seq": those are the enclosing log line's,
        and colliding on them hid the fact's own identity. Round, phase and turn
        come from the log's bound context.
        """
        return {
            "fact_seq": self.seq,
            "payload": self.payload,
            "audience": self.audience.to_json(),
            "entitled": sorted(self.entitled),
        }


class Rng:
    """A seeded PRNG whose state lives inside game state, not module globals.

    Role assignment, shuffles, ordering and random defaults all draw from here,
    so a match is reproducible from its seed alone.
    """

    _MASK = (1 << 64) - 1

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self._s = (seed ^ 0x9E3779B97F4A7C15) & self._MASK
        self.draws = 0

    def _next(self) -> int:
        # SplitMix64. Small, dependency-free, and stable across Python versions,
        # which matters because golden replays compare its digest.
        self._s = (self._s + 0x9E3779B97F4A7C15) & self._MASK
        z = self._s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & self._MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & self._MASK
        self.draws += 1
        return z ^ (z >> 31)

    def below(self, n: int) -> int:
        if n <= 0:
            raise ValueError("n must be positive")
        return self._next() % n

    def choice(self, items: list[Any]) -> Any:
        if not items:
            raise ValueError("cannot choose from an empty sequence")
        return items[self.below(len(items))]

    def shuffle(self, items: list[Any]) -> None:
        for i in range(len(items) - 1, 0, -1):
            j = self.below(i + 1)
            items[i], items[j] = items[j], items[i]

    def digest(self) -> str:
        return f"{self._s:016x}"
