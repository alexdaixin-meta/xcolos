"""`rank_by` endings: the engine ranks the seats and logs the standings."""

from __future__ import annotations

import copy
import json

import pytest

from xcolos.agents import RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.flow.state import FlowError
from xcolos.game import Game
from xcolos.games.definition import DefinitionError, parse
from xcolos.games.loader import LIBRARY
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

RPS = json.loads((LIBRARY / "rps.json").read_text(encoding="utf-8"))

OVER = {
    "when": {"calc": "rounds_left == 0"},
    "rank_by": "you.score",
    "reveal": ["hand"],
    "text": "{result} wins.",
}


def raw(over=None):
    d = copy.deepcopy(RPS)
    d["end"] = {"over": dict(over or OVER)}
    for step in _walk(d["steps"]):
        if step.get("against"):
            step["against"] = ["over"]
    return d


def _walk(steps):
    for s in steps:
        yield s
        yield from _walk(s.get("steps", ()))


def test_rank_by_exclusive():
    with pytest.raises(DefinitionError):
        parse(raw({**OVER, "result": "seat 1"}))
    with pytest.raises(DefinitionError):
        parse(raw({**OVER, "winner": "the richest"}))


def test_rank_by_checked_at_load():
    for bad in ("score", "you.scor", "you.score +"):
        with pytest.raises(DefinitionError):
            parse(raw({**OVER, "rank_by": bad}))
    parse(raw())


def ranked(scores):
    d = raw()
    d["meta"]["players"] = {"min": 1, "max": 8}
    game = Game("rank", "rps", 1, MatchLog("rank"))
    for i in scores:
        game.register_seat(f"P{i}", "h", None)
    orch = FlowOrchestrator(parse(d))
    orch.setup(game)
    for seat, value in scores.items():
        orch.flow.set_attribute(seat, "score", value)
    return orch, orch._rank(orch.definition.end[0])


def test_rank_by_single_winner():
    _, got = ranked({1: 5, 2: 3})
    assert got == ("seat 1", {1: 5, 2: 3})


def test_rank_by_shared_win():
    assert ranked({1: 4, 2: 4, 3: 1})[1][0] == "seats 1 and 2"
    assert ranked({1: 2, 2: 2, 3: 2, 4: 0})[1][0] == "seats 1, 2 and 3"


def test_rank_by_non_number():
    for value in ("lots", True):
        orch, _ = ranked({1: 1, 2: 2})
        orch.flow.set_attribute(1, "score", value)
        with pytest.raises(FlowError):
            orch._rank(orch.definition.end[0])


def test_rank_by_match_logs_standings():
    log = MatchLog("rank_match")
    game = Game("rank_match", "rps", 3, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [RandomAgent(name=n, seed=i) for i, n in enumerate(["Ada", "Blaise"])],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    Runner(game, FlowOrchestrator(parse(raw())), registry).run()
    assert game.winner
    record = [r for r in log.records if r["category"] == "process"
              and r["type"] == "end_game"][-1]
    assert set(record["standings"]) == {"1", "2"}
    assert set(game.standings) == {1, 2}
