"""The orchestrator interface.

An orchestrator decides what happens next. It never talks to an agent and never
writes text that reaches one. It mutates state only through the Game object's
system functions, and it asks for agent input by yielding an ActionRequest.

Stage 1a implements this with hardcoded Python. Stage 1b implements it with an
LLM reading a game file, yielding the same requests and calling the same system
functions. Nothing below this interface changes between them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generator, Protocol

from xcolos.game import Game
from xcolos.protocol import Action, ActionSchema


@dataclass
class GameBrief:
    """What the orchestrator tells every seat before the first round.

    Game content only. The orchestrator supplies the rules, the table size, the
    shape of a round and the actions that exist. The kernel supplies the seat's
    own index and starting state, and the communication format.

    Note what is absent: any prose naming a specific seat's secret. The brief is
    identical for everyone, and the private part of a seat's briefing is built
    from that seat's own entitled facts. An orchestrator that could write into
    the briefing directly would be a way around the visibility rule.
    """

    name: str
    rules: str
    seat_count: int
    #: Phase names in the order they repeat, so a seat knows the round shape.
    round_shape: list[str] = field(default_factory=list)
    #: Every action this game may ask for, with how to answer.
    actions: list[ActionSchema] = field(default_factory=list)


@dataclass
class ActionRequest:
    """Ask one seat to act. The only way an orchestrator reaches an agent."""

    seat: int
    schema: ActionSchema
    prompt: str
    legal_targets: tuple[Any, ...] = ()
    deadline_ms: int | None = 30_000
    #: Recorded on the move so a transcript explains why this seat was chosen.
    reason: str = ""


#: The orchestrator yields requests and is sent back the resulting Action.
Play = Generator[ActionRequest, Action, None]


class Orchestrator(Protocol):
    game_id: str

    def setup(self, game: Game) -> None:
        """Declare zones, offices and globals, and assign roles."""
        ...

    def brief(self, game: Game) -> GameBrief:
        """The game content of the pre-match briefing. Called after setup."""
        ...

    def play(self, game: Game) -> Play:
        """Drive the match. Yield an ActionRequest, receive the Action."""
        ...
