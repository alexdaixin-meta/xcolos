"""`turns` on an `ask`: round and round the table until everyone else passes.

Played on a toy bidding game with scripted players, so every test can say
exactly who should be asked, in what order, and when it stops.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from xcolos.agents import BaseAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.definition import DefinitionError
from xcolos.games.loader import load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.protocol import Action
from xcolos.runner import Runner

sys.path.insert(0, str(Path(__file__).resolve().parent))
from referee import referee  # noqa: E402

BIDS = {
    "schema": 1,
    "meta": {"id": "bids", "name": "Bids", "players": {"min": 2, "max": 6}},
    "statuses": [{"id": "playing", "acts": True, "initial": True}],
    "attributes": {
        "player": [
            {"key": "cash", "visible": "public", "type": "number", "initial": 100},
            {"key": "won", "visible": "public", "type": "number", "initial": 0},
        ],
        "game": [
            {"key": "top", "visible": "public", "type": "number", "initial": 0},
            {"key": "leader", "visible": "public", "type": "number", "initial": 0},
            {"key": "lots", "visible": "public", "type": "number", "initial": 0},
            {"key": "of", "visible": "public", "type": "number", "initial": 1},
        ],
    },
    "setup": [],
    "steps": [
        {"use": "update", "label": "the lot", "do": [
            {"adjust": {"key": "lots", "value": 1}},
            {"set": {"key": "top", "value": 0}},
            {"set": {"key": "leader", "value": 0}},
        ]},
        {
            "use": "ask",
            "label": "bid",
            "to": "acting",
            "answer": {"type": "number", "min": {"calc": "top + 1"},
                       "max": {"calc": "you.cash"}, "or": ["pass"]},
            "turns": {"pass": "pass"},
            "each": {"do": [
                {"set": {"key": "top", "value": "$answer",
                         "if": {"calc": "$answer != 'pass'"}}},
                {"set": {"key": "leader", "value": "$seat",
                         "if": {"calc": "$answer != 'pass'"}}},
            ]},
            "text": "Top bid {top}. Bid or pass.",
        },
        {"use": "update", "label": "the sale", "do": [
            {"adjust": {"player": {"calc": "leader"}, "key": "won", "value": 1,
                        "if": {"calc": "leader > 0"}}},
        ]},
        {"use": "check", "label": "last lot", "when": {"calc": "lots >= of"}},
    ],
    "end": {
        "most": {"when": {"calc": "lots >= of"},
                 "winner": "Whoever won most lots wins.",
                 "text": "{result} won most."},
    },
    "limits": {"rounds": 10, "rounds_max": 10, "actions_max": 500, "deadline_s": 60},
    "rules": "Bid or pass.",
}


class Script(BaseAgent):
    """Answers from a list, in order; passes once the list runs out."""

    def __init__(self, name, answers):
        super().__init__(name=name)
        self.answers = list(answers)

    def decide(self, env):
        schema = self._schema(env)
        return Action(type=schema.id, target=self.answers.pop(0) if self.answers else "pass")


def variant(**changes):
    raw = copy.deepcopy(BIDS)
    for path, value in changes.items():
        node = raw
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[int(k)] if k.isdigit() else node[k]
        last = keys[-1]
        node[int(last) if last.isdigit() else last] = value
    return raw


def play(scripts, raw=BIDS):
    definition = load(json.dumps(raw), source="bids")
    game = Game("bids", definition.id, 1, MatchLog("bids"))
    registry = Registry(game.match_id)
    host = LocalAgentHost([Script(f"P{i}", s) for i, s in enumerate(scripts)],
                          player=Player.new("operator"))
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition, referee(lambda you: you["won"]))
    result = Runner(game, orchestrator, registry).run()
    return result, game, orchestrator.flow


def asked(game, lot=None):
    """[(seat, answer)] in the order they were given."""
    return [(r["seat"], r["action"]["target"]) for r in game.log.records
            if r["type"] == "move" and (lot is None or r["round"] == lot)]


def refused(raw, *fragments):
    try:
        load(json.dumps(raw), source="bids")
    except DefinitionError as exc:
        for fragment in fragments:
            assert fragment in str(exc), f"{fragment!r} not in {exc}"
        return
    raise AssertionError("loaded, but should have been refused")


def test_a_pass_does_not_take_a_player_out_and_it_ends_when_the_rest_pass():
    # 1 bids, 2 passes, 3 bids, 1 bids, 2 bids after all, 3 passes, 1 passes.
    result, game, flow = play([[10, 30, "pass"], ["pass", 40], [20, "pass"]])
    assert asked(game) == [(1, 10), (2, "pass"), (3, 20), (1, 30), (2, 40),
                           (3, "pass"), (1, "pass")]
    assert flow.game_attributes["top"] == 40
    assert result.winner == "seat 2"


def test_nobody_bidding_ends_after_everyone_has_passed_once():
    result, game, flow = play([[], [], []])
    assert asked(game) == [(1, "pass"), (2, "pass"), (3, "pass")]
    assert flow.game_attributes["leader"] == 0


def test_the_player_whose_bid_stands_is_never_asked_to_beat_it():
    _, game, _ = play([[10], [], []])
    assert asked(game) == [(1, 10), (2, "pass"), (3, "pass")]


def test_the_opener_moves_one_seat_round_each_time_the_step_runs():
    _, game, _ = play([[], [], []], variant(**{"attributes__game__3__initial": 4}))
    openers = [asked(game, lot)[0][0] for lot in range(1, 5)]
    assert openers == [1, 2, 3, 1]
    assert [s for s, _ in asked(game, 2)] == [2, 3, 1]


def test_the_opener_still_moves_on_when_nobody_can_be_asked():
    raw = variant(**{"attributes__game__3__initial": 3,
                     "steps__1__to": {"where": "lots != 2"}})
    _, game, _ = play([[], [], []], raw)
    assert asked(game, 2) == []
    assert asked(game, 3)[0][0] == 3


def test_a_player_with_no_legal_number_passes_without_being_asked():
    # Seat 2 holds 15, so once the top bid is 15 it has no number left.
    raw = variant(setup=[{"use": "update", "label": "purses", "do": [
        {"set": {"player": 2, "key": "cash", "value": 15}}]}])
    _, game, flow = play([[10, 20], [15], []], raw)
    assert asked(game) == [(1, 10), (2, 15), (3, "pass"), (1, 20), (3, "pass")]
    assert flow.attribute(1, "won") == 1


def test_a_player_outside_to_is_skipped_and_not_waited_for():
    raw = variant(**{"steps__1__to": {"where": "you.seat != 2"}})
    _, game, _ = play([[10], [], []], raw)
    assert asked(game) == [(1, 10), (3, "pass")]


def test_reaching_max_abandons_the_match():
    raw = variant(**{"steps__1__turns": {"pass": "pass", "max": 3}})
    result, _, _ = play([[1, 3, 5], [2, 4, 6], []], raw)
    assert result.status == "abandoned", result
    assert "bid" in (result.reason or "")


def test_the_loader_refuses_turns_it_could_not_run():
    refused(variant(**{"steps__1__turns": {"pass": "fold"}}), "fold", "or")
    refused(variant(**{"steps__1__turns": {"pass": "pass", "max": 0}}), "max")
    refused(variant(**{"steps__1__turns": {"pass": "pass", "until": 1}}), "until")
    refused(variant(**{"steps__1__turns": "pass"}), "turns")
