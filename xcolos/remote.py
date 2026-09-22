"""Seats held by a player's own process.

This is the answer to "how does a player link a real model": they do not hand
the server a key and ask it to call a provider. They run a client on their own
machine, claim a seat, and answer its turns. Whatever sits behind that client is
their business entirely, and the server never learns what it is.

    server                              player's machine
    ------                              ----------------
    RemoteAgentHost   <-- HTTP -->      XColosClient
      outbox  (envelopes out)             their agent
      replies (actions back)              their model, script, harness, or self

The transport is long polling, deliberately. The turn model is strictly
sequential, so at most one seat is ever waiting, and a blocking read plus a post
needs no sockets, no dependencies, and no reconnect protocol. A client that
stops answering looks exactly like a seat that did not answer, which the failure
ladder already handles.
"""

from __future__ import annotations

import queue
import threading
from dataclasses import dataclass, field
from typing import Any

from xcolos.host import HostUnavailable, SeatBinding
from xcolos.identity import Player
from xcolos.protocol import RESPONSE_REQUIRED, Action, Envelope

#: How long past a turn's own deadline the server waits before giving up. The
#: client has to receive, think and reply inside the deadline; this only covers
#: transport.
GRACE_MS = 2000


@dataclass
class RemoteSeat:
    """One seat's two mailboxes."""

    index: int
    name: str
    binding: SeatBinding
    outbox: queue.Queue = field(default_factory=queue.Queue)
    replies: queue.Queue = field(default_factory=queue.Queue)
    claimed: bool = False
    #: Every envelope ever sent, so a client that reconnects can catch up.
    history: list[dict[str, Any]] = field(default_factory=list)
    awaiting: int | None = None


class RemoteAgentHost:
    """Server-side stand-in for a client that lives somewhere else.

    Satisfies the same host interface as the in-process one, so the runner
    cannot tell the difference between a local agent and a player's laptop.
    """

    def __init__(self, player: Player, seat_names: list[str]) -> None:
        self.player = player
        self.host_id = f"remote:{player.player_id}"
        self._names = list(seat_names)
        self.seats: dict[int, RemoteSeat] = {}
        self._pending: list[SeatBinding] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Host interface
    # ------------------------------------------------------------------

    def register(self) -> list[SeatBinding]:
        self._pending = [
            SeatBinding(name=n, profile={"kind": "remote"}, player_id=self.player.player_id)
            for n in self._names
        ]
        return list(self._pending)

    def bind(self, index: int, binding: SeatBinding, match_id: str) -> None:
        self.seats[index] = RemoteSeat(index=index, name=binding.name, binding=binding)

    def connected(self, index: int) -> bool:
        seat = self.seats.get(index)
        return seat is not None and seat.claimed

    def deliver(self, env: Envelope) -> Action | None:
        seat = self.seats.get(env.seat)
        if seat is None:
            raise HostUnavailable(f"this host does not own seat {env.seat}")
        if not seat.claimed:
            raise HostUnavailable(f"seat {env.seat} has not been claimed by a client")

        wire = env.to_json()
        wire["reply_required"] = env.type in RESPONSE_REQUIRED
        seat.history.append(wire)
        seat.outbox.put(wire)

        if env.type not in RESPONSE_REQUIRED:
            return None

        # Park the runner until the player's client answers. Only one seat is
        # ever waiting, because turns are strictly sequential.
        seat.awaiting = env.turn_seq
        timeout = ((env.deadline_ms or 30_000) + GRACE_MS) / 1000
        try:
            return seat.replies.get(timeout=timeout)
        except queue.Empty:
            raise HostUnavailable(
                f"seat {env.seat} did not answer within {timeout:.0f}s"
            ) from None
        finally:
            seat.awaiting = None

    def agent(self, index: int) -> Any:
        """There is no agent here. It is on the player's machine.

        Raising rather than returning a stub is deliberate: a remote seat's
        session is genuinely not on this server, and pretending otherwise would
        make the console show something misleading.
        """
        raise KeyError(f"seat {index} is held by a remote client")

    # ------------------------------------------------------------------
    # Client-facing
    # ------------------------------------------------------------------

    def claim(self, index: int, credential: str) -> RemoteSeat:
        seat = self.seats.get(index)
        if seat is None:
            raise HostUnavailable(f"no such seat: {index}")
        if not _same(seat.binding.credential, credential):
            raise HostUnavailable(f"credential rejected for seat {index}")
        with self._lock:
            seat.claimed = True
        return seat

    def poll(self, index: int, timeout_s: float) -> dict[str, Any] | None:
        """Block until this seat has a message, or the wait runs out."""
        seat = self.seats[index]
        try:
            return seat.outbox.get(timeout=timeout_s)
        except queue.Empty:
            return None

    def reply(self, index: int, action: Action | None) -> bool:
        seat = self.seats[index]
        if seat.awaiting is None:
            return False  # nothing was asked; a stray reply is dropped
        seat.replies.put(action)
        return True

    def catch_up(self, index: int) -> list[dict[str, Any]]:
        """Everything this seat has ever been sent, for a client rebuilding."""
        return list(self.seats[index].history)

    @property
    def all_claimed(self) -> bool:
        return bool(self.seats) and all(s.claimed for s in self.seats.values())


def _same(a: str, b: str) -> bool:
    import secrets

    return secrets.compare_digest(a or "", b or "")


class ConnectorHost:
    """A seat answered by an agent that pulls.

    Holds nothing. The runner parks the turn in the game's own state and the
    agent reads it through the tools, so there is no queue here and no thread
    waiting. `pull` is what tells the runner to park rather than block.
    """

    #: Read by the runner. The whole difference between the two transports.
    pull = True

    def __init__(self, player: Player, seat_names: list[str]) -> None:
        self.player = player
        self.host_id = f"connector:{player.player_id}"
        self._names = list(seat_names)
        self.seats: dict[int, SeatBinding] = {}

    def register(self) -> list[SeatBinding]:
        return [
            SeatBinding(
                name=n, profile={"kind": "connector"}, player_id=self.player.player_id
            )
            for n in self._names
        ]

    def bind(self, index: int, binding: SeatBinding, match_id: str) -> None:
        self.seats[index] = binding

    def connected(self, index: int) -> bool:
        return index in self.seats

    def deliver(self, env: Envelope) -> Action | None:
        """Never called for a turn; the runner parks those instead.

        Broadcasts land here and are simply dropped, because a pull agent reads
        what it missed from its own state rather than being handed it.
        """
        if env.type in RESPONSE_REQUIRED:
            raise HostUnavailable(
                f"seat {env.seat} pulls its turns; it cannot be pushed one"
            )
        return None

    def agent(self, index: int) -> Any:
        raise KeyError(f"seat {index} is answered by a connected session")
