"""XColos - The AI Colosseum.

A runtime for hidden-role social deduction games played by LLM agents.

Layers:
  kernel        deterministic, game-agnostic, the only thing trusted with secrets
  orchestrator  game-aware, decides what happens next, never touches an agent
  agents        seats behind one uniform message interface
"""

from xcolos.game import Game, RunStatus
from xcolos.log import MatchLog
from xcolos.protocol import Action, ActionSchema, Envelope, MsgType
from xcolos.runner import MatchResult, Runner
from xcolos.state import Audience, Fact, Rng, Seat, SeatStatus, Zone

__version__ = "0.1.0"

__all__ = [
    "Action",
    "ActionSchema",
    "Audience",
    "Envelope",
    "Fact",
    "Game",
    "MatchLog",
    "MatchResult",
    "MsgType",
    "Rng",
    "RunStatus",
    "Runner",
    "Seat",
    "SeatStatus",
    "Zone",
]
