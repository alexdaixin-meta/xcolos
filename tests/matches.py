"""Five scripted seats playing the arithmetic Mafia: the match the kernel, protocol and client/server tests are written against."""

from __future__ import annotations

import oracle_game  # noqa: F401 - makes the fixture game available
from xcolos import cli
from xcolos.cli import SEAT_NAMES  # noqa: F401 - re-exported for the tests

SEATS = 5
GAME_ID = oracle_game.ORACLE_ID


def build_match(seed: int, out_dir=None, agent_factory=None):
    return cli.build_match(seed, out_dir, agent_factory, game_id=GAME_ID, seats=SEATS)


def orchestrator():
    """A fresh orchestrator for the fixture game."""
    from xcolos.flow import FlowOrchestrator
    from xcolos.games import available

    return FlowOrchestrator(available()[GAME_ID])


def run_match(seed: int, out_dir=None):
    from xcolos.runner import Runner

    game, orch, registry, _host = build_match(seed, out_dir)
    return Runner(game, orch, registry).run(), game
