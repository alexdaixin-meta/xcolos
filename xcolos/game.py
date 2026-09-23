"""The Game object.

One object holds an entire match: its process, its state, and its log. It is the
aggregate root and the only thing a runner needs.

Two rules keep it honest:

  1. Every mutation goes through a system function, so nothing changes without
     being validated and recorded.
  2. Callers get a read-only digest (orchestrator) or a per-seat view (agents),
     never the object itself, so nobody can reach past visibility to raw state.
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Any, Callable

from xcolos.log import MatchLog
from xcolos.protocol import DirectiveRejected
from xcolos.state import FIRST_SEAT, Audience, Fact, Rng, Seat, SeatStatus, Zone


class RunStatus(str, Enum):
    SETUP = "setup"
    RUNNING = "running"
    ENDED = "ended"
    ABANDONED = "abandoned"


class Game:
    """Process, state and logging for one match."""

    def __init__(
        self,
        match_id: str,
        game_id: str,
        seed: int,
        log: MatchLog,
        manifest_hash: str = "",
    ) -> None:
        # Identity
        self.match_id = match_id
        self.game_id = game_id
        self.seed = seed
        self.manifest_hash = manifest_hash

        # State
        self.seats: dict[int, Seat] = {}
        self.globals: dict[str, Any] = {}
        self.zones: dict[str, Zone] = {}
        self.offices: dict[str, int | None] = {}
        self.rng = Rng(seed)
        self.cursor: int = -1

        # Process
        self.turn_seq = 0
        self.round = 0
        self.phase = "setup"
        self.status = RunStatus.SETUP
        self.winner: str | None = None
        self.reason: str | None = None

        # Logging. Every record carries where in the match it happened.
        self.log = log
        self.log.bind_context(
            lambda: {"round": self.round, "phase": self.phase, "turn_seq": self.turn_seq}
        )
        self.facts: list[Fact] = []

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    @property
    def identity(self) -> str:
        """Seed plus game plus manifest. Two matches compare only if equal."""
        raw = f"{self.game_id}:{self.seed}:{self.manifest_hash}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    # ------------------------------------------------------------------
    # Declaration
    # ------------------------------------------------------------------

    def register_seat(
        self, name: str, host_id: str = "local", profile: dict[str, Any] | None = None
    ) -> int:
        """Assign a fixed index. Assigned once, never reused, never changed.

        The server assigns the index, never the client. The profile is opaque
        here and recorded only so the log says what was sitting in the seat.
        """
        if self.status is not RunStatus.SETUP:
            raise DirectiveRejected("seats may only be registered during setup")
        index = FIRST_SEAT + len(self.seats)
        self.seats[index] = Seat(index=index, name=name)
        self.log.record(
            "setup",
            "register_seat",
            seat=index,
            name=name,
            host=host_id,
            profile=profile or {},
        )
        return index

    def declare_zone(self, zone: Zone) -> None:
        if zone.id in self.zones:
            raise DirectiveRejected(f"zone '{zone.id}' already declared")
        self.zones[zone.id] = zone
        self.log.record("setup", "declare_zone", **zone.to_json())

    def declare_office(self, office_id: str) -> None:
        if office_id in self.offices:
            raise DirectiveRejected(f"office '{office_id}' already declared")
        self.offices[office_id] = None
        self.log.record("setup", "declare_office", office=office_id)

    def declare_global(self, key: str, value: Any) -> None:
        self.globals[key] = value
        self.log.record("setup", "declare_global", key=key, value=value)

    # ------------------------------------------------------------------
    # Validation helpers
    # ------------------------------------------------------------------

    def _seat(self, index: Any, *, must_be_alive: bool = False) -> Seat:
        if not isinstance(index, int) or index not in self.seats:
            raise DirectiveRejected(f"no such seat: {index!r}")
        seat = self.seats[index]
        if must_be_alive and not seat.alive:
            raise DirectiveRejected(f"seat {index} is not active")
        return seat

    def _zone(self, zone_id: Any) -> Zone:
        if zone_id not in self.zones:
            raise DirectiveRejected(f"no such zone: {zone_id!r}")
        return self.zones[zone_id]

    # ------------------------------------------------------------------
    # System functions: state
    # ------------------------------------------------------------------

    def set_role(self, seat: int, role: str, faction: str) -> None:
        s = self._seat(seat)
        s.role, s.faction = role, faction
        self.log.record("setup", "set_role", seat=seat, role=role, faction=faction)

    def set_attribute(self, seat: int, key: str, value: Any) -> None:
        self._seat(seat).attributes[key] = value
        self.log.record("state", "set_attribute", seat=seat, key=key, value=value)

    def set_global(self, key: str, value: Any) -> None:
        if key not in self.globals:
            raise DirectiveRejected(f"global '{key}' was never declared")
        before = self.globals[key]
        self.globals[key] = value
        self.log.record("state", "set_global", key=key, was=before, now=value)

    def block(self, seat: int, flag: str) -> None:
        """Stop a living seat from acting without eliminating it."""
        self._seat(seat).eligibility_blocks.add(flag)
        self.log.record("state", "block", seat=seat, flag=flag)

    def unblock_all(self, flag: str) -> None:
        for s in self.seats.values():
            s.eligibility_blocks.discard(flag)
        self.log.record("state", "unblock_all", flag=flag)

    def eliminate(self, seat: int) -> None:
        s = self._seat(seat, must_be_alive=True)
        s.status = SeatStatus.ELIMINATED
        self.log.record("state", "eliminate", seat=seat, role=s.role)

    def assign_office(self, office: str, seat: int | None) -> None:
        if office not in self.offices:
            raise DirectiveRejected(f"office '{office}' was never declared")
        if seat is not None:
            self._seat(seat)
        before = self.offices[office]
        self.offices[office] = seat
        self.log.record("state", "assign_office", office=office, was=before, now=seat)

    # ------------------------------------------------------------------
    # System functions: zones
    # ------------------------------------------------------------------

    def zone_shuffle(self, zone_id: str) -> None:
        zone = self._zone(zone_id)
        self.rng.shuffle(zone.tokens)
        self.log.record("state", "zone_shuffle", zone=zone_id, count=len(zone.tokens))

    def zone_draw(self, zone_id: str, to: str, count: int = 1) -> list[str]:
        src, dst = self._zone(zone_id), self._zone(to)
        if len(src.tokens) < count:
            raise DirectiveRejected(
                f"zone '{zone_id}' holds {len(src.tokens)} tokens, need {count}"
            )
        moved = [src.tokens.pop(0) for _ in range(count)]
        dst.tokens.extend(moved)
        self.log.record(
            "state",
            "zone_draw",
            **{"from": zone_id, "to": to, "tokens": moved, "remaining": len(src.tokens)},
        )
        return moved

    def zone_remove_at(self, zone_id: str, position: int, to: str) -> str:
        src, dst = self._zone(zone_id), self._zone(to)
        if not 0 <= position < len(src.tokens):
            raise DirectiveRejected(
                f"position {position} out of range for zone '{zone_id}'"
            )
        token = src.tokens.pop(position)
        dst.tokens.append(token)
        self.log.record(
            "state",
            "zone_remove_at",
            **{"from": zone_id, "to": to, "position": position, "token": token},
        )
        return token

    # ------------------------------------------------------------------
    # System functions: facts and visibility
    # ------------------------------------------------------------------

    def emit_fact(
        self, fact_type: str, payload: dict[str, Any], audience: Audience
    ) -> Fact:
        """Record something that happened, with the audience entitled to know it.

        The audience is resolved now, against state as it stands now, and frozen
        onto the fact. That is what makes entitlement survive later eliminations.
        """
        fact = Fact(
            seq=len(self.facts),
            type=fact_type,
            payload=payload,
            audience=audience,
            entitled=frozenset(audience.resolve(self.seats)),
            round=self.round,
            phase=self.phase,
            turn_seq=self.turn_seq,
        )
        self.facts.append(fact)
        self.log.record("fact", fact_type, **fact.to_fields())
        return fact

    def entitled_facts(self, seat: int) -> list[Fact]:
        return [f for f in self.facts if seat in f.entitled]

    def undelivered(self, seat: int) -> list[Fact]:
        """Entitled facts this seat has not yet been pushed."""
        s = self._seat(seat)
        return [f for f in self.facts[s.delivered_upto :] if seat in f.entitled]

    def unacked(self, seat: int) -> list[Fact]:
        """Entitled facts this seat has not confirmed.

        This, not the read cursor, is what a pull client is shown. A session
        that fetched and then lost the thread sees the same material again,
        which is the cheapest possible recovery.
        """
        s = self._seat(seat)
        return [f for f in self.facts[s.acked_upto :] if seat in f.entitled]

    def record_read(self, seat: int, facts: list[Fact]) -> None:
        """Note that a seat fetched. Fetching is not acknowledging."""
        from datetime import datetime, timezone

        s = self._seat(seat)
        s.read_upto = len(self.facts)
        s.reads += 1
        s.last_read_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.log.record(
            "delivery",
            "read",
            seat=seat,
            fact_seqs=[f.seq for f in facts],
            acked_upto=s.acked_upto,
        )

    def ack(self, seat: int, through_seq: int | None) -> int:
        """Advance a seat's confirmed cursor. Never moves backwards.

        Clamped to what this seat has actually been *shown*, not to how many
        facts exist. A table can play several games, each with its own fact
        list starting at zero, and an agent polling across the boundary still
        carries the last number from the game before. Clamping to the fact
        count would let that stale number confirm a whole new game unseen, so
        the seat would be asked to act having never been told its role.
        """
        s = self._seat(seat)
        if through_seq is None:
            return s.acked_upto
        target = min(int(through_seq) + 1, s.read_upto)
        if target <= s.acked_upto:
            return s.acked_upto
        s.acked_upto = target
        self.log.record("delivery", "ack", seat=seat, acked_upto=target)
        return s.acked_upto

    def mark_delivered(self, seat: int, facts: list[Fact]) -> None:
        s = self._seat(seat)
        s.delivered_upto = len(self.facts)
        # A push hands the message over in process, so there is nothing to
        # confirm separately. Pull transports acknowledge explicitly.
        s.read_upto = s.acked_upto = len(self.facts)
        if facts:
            self.log.record(
                "delivery",
                "push",
                seat=seat,
                fact_seqs=[f.seq for f in facts],
            )

    # ------------------------------------------------------------------
    # System functions: turn selection
    # ------------------------------------------------------------------

    def active_seats(self) -> list[int]:
        return [i for i, s in sorted(self.seats.items()) if s.alive]

    def eligible_seats(self, where: Callable[[Seat], bool] | None = None) -> list[int]:
        """Seats that may act now, in index order."""
        return [
            i
            for i, s in sorted(self.seats.items())
            if s.eligible and (where is None or where(s))
        ]

    def next_in_rotation(self, where: Callable[[Seat], bool] | None = None) -> int:
        """Advance the cursor to the next eligible seat and return it.

        The cursor survives phase transitions, which is what makes rotating
        offices expressible without the orchestrator doing arithmetic.
        """
        order = sorted(self.seats)
        if not order:
            raise DirectiveRejected("no seats registered")
        # Walk the seats that exist rather than doing arithmetic on the index,
        # so the numbering can start wherever it likes.
        start = order.index(self.cursor) + 1 if self.cursor in order else 0
        for step in range(len(order)):
            candidate = order[(start + step) % len(order)]
            seat = self.seats[candidate]
            if seat.eligible and (where is None or where(seat)):
                self.cursor = candidate
                return candidate
        raise DirectiveRejected("no eligible seat in rotation")

    def set_rotation_cursor(self, seat: int) -> None:
        self._seat(seat)
        self.cursor = seat
        self.log.record("state", "set_rotation_cursor", seat=seat)

    # ------------------------------------------------------------------
    # System functions: process
    # ------------------------------------------------------------------

    def set_phase(self, phase: str) -> None:
        before = self.phase
        self.phase = phase
        self.log.record("process", "set_phase", was=before, now=phase)

    def advance_round(self) -> None:
        self.round += 1
        self.log.record("process", "advance_round")

    def end_game(self, winner: str, reason: str) -> None:
        self.status = RunStatus.ENDED
        self.winner, self.reason = winner, reason
        self.log.record("process", "end_game", winner=winner, reason=reason)

    def abandon(self, reason: str) -> None:
        self.status = RunStatus.ABANDONED
        self.reason = reason
        self.log.record("process", "abandon", reason=reason)

    # ------------------------------------------------------------------
    # Views
    # ------------------------------------------------------------------

    def digest(self) -> dict[str, Any]:
        """Read-only full-information view, for the orchestrator only.

        The orchestrator decides what happens. It never authors text that
        reaches a seat, so seeing everything here cannot leak anything.
        """
        return {
            "match_id": self.match_id,
            "round": self.round,
            "phase": self.phase,
            "status": self.status.value,
            "turn_seq": self.turn_seq,
            "cursor": self.cursor,
            "seats": [s.to_json() for s in self.seats.values()],
            "globals": dict(self.globals),
            "zones": [z.to_json() for z in self.zones.values()],
            "offices": dict(self.offices),
        }

    def seat_view(self, seat: int) -> dict[str, Any]:
        """Everything one seat is entitled to, and nothing else.

        This is the only state a renderer or an agent ever sees.
        """
        s = self._seat(seat)
        return {
            "you": {
                "index": s.index,
                "name": s.name,
                "role": s.role,
                "faction": s.faction,
                "status": s.status.value,
            },
            "round": self.round,
            "phase": self.phase,
            "seats": [
                {"index": o.index, "name": o.name, "status": o.status.value}
                for o in self.seats.values()
            ],
            "globals": dict(self.globals),
            "offices": dict(self.offices),
            "your_zones": [
                z.to_json() for z in self.zones.values() if seat in z.viewers(self.seats)
            ],
        }
