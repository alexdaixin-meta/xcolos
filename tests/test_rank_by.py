"""`rank_by` endings: the engine ranks the seats and logs the standings."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from xcolos.agents import RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.flow.state import FlowError
from xcolos.game import Game
from xcolos.games import available
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


# -- the library games decide their winner with `rank_by` ---------------------

#: The library's Coup as it was before `rank_by`: its own steps work the winner out into a `winner`
#: attribute, and there is one `result` ending per seat, plus `draw`. Only its id differs (and it is
#: unlisted): `tests/data` is also a directory of games (see oracle_game.py), and an id may be used once.
COUP_PRE_RANK_BY = Path(__file__).resolve().parent / "data" / "coup_pre_rank_by.json"


def _with_turn_cap(raw: dict, cap: int) -> dict:
    raw = copy.deepcopy(raw)
    for a in raw["attributes"]["game"]:
        if a["key"] == "turn_cap":
            a["initial"] = cap
    return raw


def _random_match(definition, seed: int, n: int):
    game = Game(f"coup_{seed}_{n}", "coup", seed, MatchLog(f"coup_{seed}_{n}"))
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [RandomAgent(name=f"p{i}", seed=seed * 10 + i) for i in range(n)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition)
    return Runner(game, orchestrator, registry).run(), game, orchestrator


def _named(seats: list[int]) -> str:
    return (f"seat {seats[0]}" if len(seats) == 1 else
            "seats " + ", ".join(map(str, seats[:-1])) + f" and {seats[-1]}")


def test_coup_rank_by_matches_old_winner():
    """50 seeded random matches of the old Coup and the converted one, at the shipped turn cap and at a
    short one (random seats rarely reach turn 40, and the cap is where the tie-breaks live): the same
    winner every time, except an old `draw`, which is now a win shared by exactly the seats it tied."""
    old_raw = json.loads(COUP_PRE_RANK_BY.read_text(encoding="utf-8"))
    new_raw = json.loads((LIBRARY / "coup.json").read_text(encoding="utf-8"))
    assert [r.get("rank_by") for r in new_raw["end"].values()] == ["you.hidden_count * 1000 + you.coins"]
    seen = {"eliminated": 0, "cap": 0, "shared": 0}
    for cap in (None, 6):
        old = parse(old_raw if cap is None else _with_turn_cap(old_raw, cap))
        new = parse(new_raw if cap is None else _with_turn_cap(new_raw, cap))
        for seed in range(1, 51):
            n = 3 + seed % 3
            before, _, flow_before = _random_match(old, seed, n)
            after, game, _ = _random_match(new, seed, n)
            where = (cap, seed, n, before.winner, after.winner)
            assert before.status == after.status == "ended", where
            assert after.turns == before.turns, where  # the same match, played the same way
            assert set(game.standings) == set(range(1, n + 1)), where
            state = flow_before.flow
            if before.winner == "draw":
                alive = [s for s in state.players if state.attribute(s, "alive")]
                key = {s: state.attribute(s, "hidden_count") * 1000 + state.attribute(s, "coins") for s in alive}
                tied = sorted(s for s in alive if key[s] == max(key.values()))
                assert len(tied) > 1 and after.winner == _named(tied), where
                seen["shared"] += 1
            else:
                assert after.winner == before.winner, where
                seen["cap" if state.game_attributes["turn_count"] >= state.game_attributes["turn_cap"]
                     else "eliminated"] += 1
    assert all(seen.values()), seen  # every way Coup ends was played


def test_library_games_rank_by():
    want = {"rps": "you.score", "auction": "you.cash + you.holdings", "agram": "you.match_points",
            "battle_of_wits": "you.score", "coup": "you.hidden_count * 1000 + you.coins",
            "assurance_game": "1 if you.total_score >= win_threshold else 0"}
    games = available()
    for game_id, rank_by in want.items():
        assert [r.rank_by for r in games[game_id].end] == [rank_by], game_id
    assert all(r.result for r in games["mafia"].end)  # hand-written, team results: not converted


def test_auction_and_agram_rules_say_how_the_game_is_decided():
    auction = json.loads((LIBRARY / "auction.json").read_text(encoding="utf-8"))
    assert auction["meta"]["players"]["suggested"] == 4
    assert auction["rules"].endswith(
        "\n\nEach minimum bid is rounded to the nearest {min_raise}, so it can fall slightly outside "
        "{ratio_min}-{ratio_max} times the item's value.")
    rules = available()["agram"].rules_text
    assert "If two or more players tie for most, they share the win." in rules and "draw" not in rules
    assert ("When you may play only one card (a single card of the led suit, or your last card), the game "
            "plays it for you without asking") in rules
    assert "you are never asked at trick 6" in rules
