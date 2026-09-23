"""The client side: an agent host.

Agents live on the client. The client registers the seats it owns, holds their
configuration, and relays messages to them. Everything authoritative stays on
the server: state, decisions, sequence numbers, and the log.

The boundary is exactly this interface. A local run is an in-process host
holding every seat. An online run is a remote host per principal. One code path,
two deployments.

The trust boundary is the seat, not the host. A host hosting several seats
necessarily sees the union of what those seats are entitled to, so a host may
only hold seats that one principal controls. Locally that is everyone; online it
is one competitor's seats.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Any, Protocol

from xcolos.agents import Agent
from xcolos.identity import AccessDenied, Ownership, Player
from xcolos.protocol import Action, Envelope


class HostUnavailable(Exception):
    """The host could not be reached, or refused the seat."""


@dataclass
class SeatBinding:
    """What the server learns about a seat at registration.

    The model configuration stays on the client. The server knows only that the
    seat exists, who may speak for it, and what to call it.
    """

    name: str
    #: Proves ownership on reconnect. A host cannot ask for another's traffic.
    credential: str = field(default_factory=lambda: secrets.token_hex(8))
    #: Opaque to the server, recorded for the log.
    profile: dict[str, Any] = field(default_factory=dict)
    #: The principal this seat belongs to. Set by the host at registration and
    #: recorded by the server, so a session is never ownerless.
    player_id: str = ""


class AgentHost(Protocol):
    """A client, acting for one player."""

    host_id: str
    player: Player

    def register(self) -> list[SeatBinding]:
        """Declare the seats this host owns. The server assigns the indices."""
        ...

    def bind(self, index: int, binding: SeatBinding, match_id: str) -> None:
        """Learn the index the server assigned, and open that seat's session."""
        ...

    def deliver(self, env: Envelope) -> Action | None:
        """Relay one message to the seat that owns it."""
        ...

    def connected(self, index: int) -> bool:
        ...


class LocalAgentHost:
    """In-process host. Every seat on one machine, one operator.

    This is the local run, and it is the same object the server talks to when a
    real client connects, which is the point.
    """

    host_id = "local"

    def __init__(self, agents: list[Agent], player: Player | None = None) -> None:
        self._agents = list(agents)
        self._by_index: dict[int, Agent] = {}
        self._credentials: dict[int, str] = {}
        self._down: set[int] = set()
        #: Every host acts for exactly one principal. A host holding seats for
        #: two players would see the union of their secrets.
        self.player = player or Player.new("local operator")

    def register(self) -> list[SeatBinding]:
        self.reset()
        return [
            SeatBinding(
                name=a.name,
                profile={"kind": type(a).__name__},
                player_id=self.player.player_id,
            )
            for a in self._agents
        ]

    def reset(self) -> None:
        """Forget which seats were bound, so this host can play another game.

        A table outlives any one game. The agents stay; their sessions do not,
        because a new game is a new conversation.
        """
        self._by_index.clear()
        self._credentials.clear()

    def bind(self, index: int, binding: SeatBinding, match_id: str) -> None:
        # Bindings come back in registration order, so the nth binding is the
        # nth agent this host offered.
        agent = self._agents[len(self._by_index)]
        self._by_index[index] = agent
        self._credentials[index] = binding.credential
        # Opening the session here, not at construction, is what makes it
        # seat-specific and owned. Every agent gets its own; none is shared.
        agent.bind(index, match_id, owner=binding.player_id or self.player.player_id)

    def deliver(self, env: Envelope) -> Action | None:
        if env.seat in self._down:
            raise HostUnavailable(f"seat {env.seat} is not reachable")
        agent = self._by_index.get(env.seat)
        if agent is None:
            raise HostUnavailable(f"this host does not own seat {env.seat}")
        return agent.handle(env)

    def connected(self, index: int) -> bool:
        return index in self._by_index and index not in self._down

    # -- test and simulation hooks -------------------------------------

    def drop(self, index: int) -> None:
        """Simulate a client losing its connection for one seat."""
        self._down.add(index)

    def restore(self, index: int) -> None:
        self._down.discard(index)

    def agent(self, index: int) -> Agent:
        return self._by_index[index]


class Registry:
    """Server-side view of which host speaks for which seat."""

    def __init__(self, match_id: str = "match") -> None:
        self.match_id = match_id
        self.host_of: dict[int, AgentHost] = {}
        self.binding_of: dict[int, SeatBinding] = {}
        #: The single place that decides who may read or act on a seat.
        self.ownership = Ownership(match_id)

    def attach(self, index: int, host: AgentHost, binding: SeatBinding) -> None:
        self.host_of[index] = host
        self.binding_of[index] = binding
        self.ownership.enrol(host.player)
        self.ownership.claim(
            index, binding.player_id or host.player.player_id, binding.credential
        )
        host.bind(index, binding, self.match_id)

    def authorises(self, index: int, credential: str) -> bool:
        return self.ownership.credential_fits(index, credential)

    # -- sessions ------------------------------------------------------

    def session_of(self, seat: int, player_id: str, token: str):
        """One seat's session, if this caller is allowed to see it.

        Reachable only for an in-process host. A remote client keeps its own
        memory on its own machine, and the server holds the record of what it
        was sent rather than what it chose to remember.
        """
        self.ownership.check_read(seat, player_id, token)
        host = self.host_of.get(seat)
        agent = getattr(host, "agent", None)
        if agent is None:
            raise AccessDenied(f"seat {seat} is hosted remotely; its session is not here")
        return agent(seat).session

    def readable_seats(self, player_id: str, token: str) -> list[int]:
        from xcolos.identity import OPERATOR

        if player_id == OPERATOR and self.ownership.is_player(OPERATOR, token):
            return sorted(self.host_of)
        if not self.ownership.is_player(player_id, token):
            return []
        return self.ownership.seats_of(player_id)

    def deliver(self, env: Envelope) -> Action | None:
        host = self.host_of.get(env.seat)
        if host is None:
            raise HostUnavailable(f"no host registered for seat {env.seat}")
        return host.deliver(env)

    def seats(self) -> list[int]:
        return sorted(self.host_of)
