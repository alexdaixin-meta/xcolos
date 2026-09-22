"""Who owns what.

A session is a seat's whole memory, including its secrets. It therefore needs an
owner, and the server needs a way to tell the right client from every other one.

The chain of ownership:

    player  ->  client (host)  ->  seat(s)  ->  session

A **player** is a principal: a person, or an operator running a batch. It holds
one long-lived token.

A **seat credential** is issued by the server when a seat is assigned. It is
scoped to one seat of one match. A player presents its token to prove who it is,
and a seat credential to prove which seat it is speaking for.

Two separate checks, because they fail differently. A wrong player token is
someone else entirely. A wrong seat credential is the right player reaching for
a seat that is not theirs, which is the case that actually happens when a client
hosts several seats and gets its bookkeeping wrong.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field

#: The operator: whoever is running the match. Sees everything, the way a
#: spectator seat does. Distinct from any player, and never assigned a seat.
OPERATOR = "operator"


@dataclass(frozen=True)
class Player:
    """A principal that may own seats."""

    player_id: str
    display_name: str = ""
    token: str = field(default_factory=lambda: secrets.token_hex(16))

    @staticmethod
    def new(display_name: str) -> "Player":
        return Player(
            player_id=f"p_{secrets.token_hex(4)}",
            display_name=display_name or "player",
        )

    def public(self) -> dict[str, str]:
        """Safe to show anyone. Never includes the token."""
        return {"player_id": self.player_id, "display_name": self.display_name}


class AccessDenied(Exception):
    """The caller may not read or act on this seat."""


class Ownership:
    """Server-side record of which player owns which seat.

    This is the only place that decides whether a caller may see a session. It
    is deliberately small, because a scattered authorisation check is one that
    eventually disagrees with itself.
    """

    def __init__(self, match_id: str) -> None:
        self.match_id = match_id
        self.players: dict[str, Player] = {}
        self.owner_of: dict[int, str] = {}
        self.credential_of: dict[int, str] = {}

    # ------------------------------------------------------------------

    def enrol(self, player: Player) -> None:
        self.players[player.player_id] = player

    def claim(self, seat: int, player_id: str, credential: str) -> None:
        if player_id not in self.players:
            raise AccessDenied(f"unknown player {player_id!r}")
        self.owner_of[seat] = player_id
        self.credential_of[seat] = credential

    def seats_of(self, player_id: str) -> list[int]:
        return sorted(s for s, p in self.owner_of.items() if p == player_id)

    # ------------------------------------------------------------------

    def is_player(self, player_id: str, token: str) -> bool:
        player = self.players.get(player_id)
        return player is not None and secrets.compare_digest(player.token, token)

    def owns_seat(self, player_id: str, seat: int) -> bool:
        return self.owner_of.get(seat) == player_id

    def credential_fits(self, seat: int, credential: str) -> bool:
        held = self.credential_of.get(seat)
        return held is not None and secrets.compare_digest(held, credential)

    def check_read(self, seat: int, player_id: str, token: str) -> None:
        """Raise unless this caller may read this seat's session.

        The operator may read anything, because the console is a spectator
        surface and says so. Anyone else may read only their own seats.
        """
        if player_id == OPERATOR:
            if not self.is_player(OPERATOR, token):
                raise AccessDenied("operator token rejected")
            return
        if not self.is_player(player_id, token):
            raise AccessDenied("player token rejected")
        if not self.owns_seat(player_id, seat):
            raise AccessDenied(f"player {player_id} does not own seat {seat}")

    def check_act(self, seat: int, player_id: str, token: str, credential: str) -> None:
        """Raise unless this caller may speak for this seat.

        Acting needs the seat credential as well as the player token. The
        operator has no standing here: watching a match is not playing in one.
        """
        if player_id == OPERATOR:
            raise AccessDenied("the operator does not hold a seat")
        self.check_read(seat, player_id, token)
        if not self.credential_fits(seat, credential):
            raise AccessDenied(f"seat credential rejected for seat {seat}")

    # ------------------------------------------------------------------

    def summary(self) -> list[dict[str, object]]:
        """Who holds what. Tokens and credentials never appear here."""
        return [
            {
                "seat": seat,
                "player_id": player_id,
                "display_name": self.players[player_id].display_name
                if player_id in self.players
                else "",
                "session_id": f"{self.match_id}:seat{seat}",
            }
            for seat, player_id in sorted(self.owner_of.items())
        ]
