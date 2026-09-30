"""The generic pieces the auction needed, tested on a game that is not one.

`{"calc": ...}` expressions, the `repeat` action, `each` on an `ask`, number
answers with a worked-out range, `players` and `if` on an operation, `say`,
ranked endings, and `{key}` in the rules. Each is written so any game can use
it; this file uses them in a toy climbing game to keep that honest.
"""

from __future__ import annotations

import copy
import json

from xcolos.agents import BaseAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.calc import CalcError, Expr, Scope, evaluate, split
from xcolos.games.definition import DefinitionError
from xcolos.games.loader import load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.protocol import Action, ActionInvalid, ActionSchema, validate
from xcolos.runner import Runner
from xcolos.state import Rng

# Every climber raises the pot by the least they may, one at a time, until it
# reaches the top. Four climbers answer eight times each, so all four tie.
CLIMB = {
    "schema": 1,
    "meta": {"id": "climb", "name": "Climb", "players": {"min": 2, "max": 6}},
    "statuses": [{"id": "playing", "acts": True, "initial": True}],
    "attributes": {
        "player": [
            {"key": "score", "visible": "public", "type": "number", "initial": 0},
        ],
        "game": [
            {"key": "pot", "visible": "public", "type": "number", "initial": 0},
            {"key": "top", "visible": "public", "type": "number", "initial": 30},
            {"key": "step", "visible": "public", "type": "number", "initial": 5},
        ],
    },
    "setup": [],
    "steps": [
        {
            "use": "repeat",
            "label": "the climb",
            "until": {"calc": "pot >= top"},
            "max": 20,
            "steps": [
                {
                    "use": "ask",
                    "label": "raise",
                    "to": "acting",
                    "answer": {"type": "number",
                               "min": {"calc": "pot + 1"},
                               "max": {"calc": "pot + step"}},
                    "each": {"do": [
                        {"set": {"key": "pot", "value": "$answer"}},
                        {"adjust": {"player": "$seat", "key": "score", "value": 1,
                                    "text": "Seat {player} climbs to {value}."}},
                    ]},
                    "text": "The pot is {pot}. Raise it.",
                }
            ],
        },
        {"use": "update", "label": "the top",
         "do": [{"say": {"text": "The pot reached {pot}."}}]},
        {"use": "check", "label": "at the top", "when": {"calc": "pot >= top"}},
    ],
    "end": {
        "most_climbs": {
            "when": {"calc": "pot >= top"},
            "rank": {"by": "you.score", "highest": True},
            "text": "{result} climbed most, {score} times. {standings}.",
        }
    },
    "limits": {"rounds": 5, "rounds_max": 5, "actions_max": 500, "deadline_s": 60},
    "rules": "Raise the pot by 1 to {step} until it reaches {top}.",
}


class Lowest(BaseAgent):
    """Always gives the least a number answer allows."""

    def decide(self, env):
        schema = self._schema(env)
        if schema.minimum is not None and schema.maximum is not None \
                and schema.minimum <= schema.maximum:
            return Action(type=schema.id, target=schema.minimum)
        return Action(type=schema.id, target=schema.choices[0])


def variant(**changes):
    raw = copy.deepcopy(CLIMB)
    for path, value in changes.items():
        node = raw
        keys = path.split("__")
        for k in keys[:-1]:
            node = node[int(k)] if k.isdigit() else node[k]
        last = keys[-1]
        node[int(last) if last.isdigit() else last] = value
    return raw


def play(raw: dict, seats: int = 4, seed: int = 1):
    definition = load(json.dumps(raw), source="climb")
    game = Game("climb", definition.id, seed, MatchLog("climb"))
    registry = Registry(game.match_id)
    host = LocalAgentHost([Lowest(name=f"P{i}") for i in range(seats)],
                          player=Player.new("operator"))
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition)
    return Runner(game, orchestrator, registry).run(), game, orchestrator


def refused(raw: dict, *fragments: str) -> None:
    try:
        load(json.dumps(raw), source="climb")
    except DefinitionError as exc:
        for fragment in fragments:
            assert fragment in str(exc), f"{fragment!r} not in {exc}"
        return
    raise AssertionError("loaded, but should have been refused")


def scope(**table):
    return Scope(lookup=table.__getitem__, binding=lambda n: None,
                 player=lambda s: None, rng=Rng(7))


# ----------------------------------------------------------------------
# Expressions
# ----------------------------------------------------------------------


def test_an_expression_reads_the_table_and_does_arithmetic():
    s = scope(pot=12, step=5, values=[3, 4, 5])
    assert evaluate(Expr("max(pot + step, 20)"), s) == 20
    assert evaluate(Expr("[v * 2 for v in values if v > 3]"), s) == [8, 10]
    assert evaluate(Expr("'high' if pot > 10 else 'low'"), s) == "high"
    assert evaluate(Expr("values[pot - 11]"), s) == 4


def test_an_expression_can_only_call_what_is_listed():
    for source in ("__import__('os')", "open('x')", "pot.__class__",
                   "sorted(values, reverse=True)", "(lambda: 1)()",
                   "pot if (pot := 3) else 0"):
        try:
            Expr(source)
        except CalcError:
            continue
        raise AssertionError(f"{source!r} was accepted")


def test_a_failure_while_working_out_is_a_calc_error():
    try:
        evaluate(Expr("values[9]"), scope(values=[1]))
    except CalcError:
        return
    raise AssertionError("an index out of range escaped as itself")


def test_seeded_draws_replay_and_split_keeps_its_promise():
    for seed in range(1, 30):
        a, b = split(Rng(seed), 2000, 10, 100, 400), split(Rng(seed), 2000, 10, 100, 400)
        assert a == b
        assert sum(a) == 2000 and all(100 <= v <= 400 for v in a)
    assert len({tuple(split(Rng(s), 2000, 10, 100, 400)) for s in range(10)}) == 10
    try:
        split(Rng(1), 2000, 3, 100, 400)
    except CalcError:
        return
    raise AssertionError("an impossible split was attempted")


# ----------------------------------------------------------------------
# Number answers
# ----------------------------------------------------------------------


def test_a_number_answer_is_checked_against_its_range_and_its_words():
    schema = ActionSchema(id="bid", target="number", choices=("pass",),
                          minimum=50, maximum=90)
    assert validate(Action(type="bid", target="60"), schema, ()).target == 60
    assert validate(Action(type="bid", target=70.0), schema, ()).target == 70
    assert validate(Action(type="bid", target="Pass"), schema, ()).target == "pass"
    for bad in (40, 91, 55.5, "fold"):
        try:
            validate(Action(type="bid", target=bad), schema, ())
        except ActionInvalid:
            continue
        raise AssertionError(f"{bad!r} was accepted")


# ----------------------------------------------------------------------
# repeat, each, say, rank, rules
# ----------------------------------------------------------------------


def test_repeat_runs_until_its_condition_and_each_sees_every_answer():
    result, game, orchestrator = play(CLIMB)
    assert result.status == "ended", result
    flow = orchestrator.flow
    assert flow.game_attributes["pot"] == 32
    assert [flow.attribute(s, "score") for s in range(1, 5)] == [8, 8, 8, 8]
    moves = [r["action"]["target"] for r in game.log.records if r["type"] == "move"]
    # Each player was asked for more than the one before had just said.
    assert moves == list(range(1, 33))


def test_a_ranked_ending_shares_a_tie():
    result, game, _ = play(CLIMB)
    assert result.winner == "seats 1, 2, 3 and 4"
    ending = [f for f in game.facts if f.type == "game_over"][-1]
    assert "climbed most, 8 times" in ending.payload["rendered"]


def test_a_ranked_ending_names_a_single_winner():
    raw = variant(**{"end__most_climbs__rank__by": "you.score * 10 + you.seat"})
    result, _, _ = play(raw)
    assert result.winner == "seat 4"
    raw = variant(**{"end__most_climbs__rank": {"by": "you.score * 10 + you.seat",
                                                "highest": False}})
    assert play(raw)[0].winner == "seat 1"


def test_a_loop_that_never_ends_abandons_the_match():
    result, game, _ = play(variant(**{"steps__0__max": 3}))
    assert result.status == "abandoned", result
    assert "the climb" in (result.reason or ""), result.reason


def test_say_announces_and_operation_facts_are_named_for_their_step():
    _, game, _ = play(CLIMB)
    types = {f.type for f in game.facts}
    assert "the_top_say" in types
    assert "raise_each_adjust" in types
    said = [f for f in game.facts if f.type == "the_top_say"]
    assert said and "The pot reached 32." in said[0].payload["rendered"]


def test_the_rules_are_filled_from_the_table():
    definition = load(json.dumps(CLIMB), source="climb")
    assert definition.rules_text == "Raise the pot by 1 to 5 until it reaches 30."


def test_an_operation_can_apply_to_a_group_and_be_guarded():
    raw = variant(setup=[{"use": "update", "label": "head start", "do": [
        {"set": {"players": {"where": "you.seat % 2 == 0"}, "key": "score",
                 "value": {"calc": "you.seat * 100"}}},
        {"adjust": {"players": "all", "key": "score", "value": 1,
                    "if": {"calc": "top > 100"}}},
    ]}])
    _, _, orchestrator = play(raw)
    flow = orchestrator.flow
    # Even seats got 100 per seat; nobody got the guarded bonus; everyone
    # then climbed eight times.
    assert [flow.attribute(s, "score") for s in range(1, 5)] == [8, 208, 8, 408]


def test_a_player_with_an_empty_range_and_no_words_is_not_asked():
    # Seats may only raise to at most `pot + step`, and seat 1 is told to stop
    # at 10: once the pot is past that, its range is empty and it is skipped.
    raw = variant(**{"steps__0__steps__0__answer__max":
                     {"calc": "min(pot + step, 10) if you.seat == 1 else pot + step"}})
    _, game, orchestrator = play(raw)
    asked = [r for r in game.log.records if r["type"] == "move" and r["seat"] == 1]
    assert asked and all(r["action"]["target"] <= 10 for r in asked)


# ----------------------------------------------------------------------
# What the loader refuses
# ----------------------------------------------------------------------


def test_the_loader_refuses_what_would_fail_at_run_time():
    ask = "steps__0__steps__0"
    refused(variant(**{f"{ask}__answer__min": {"calc": "pott + 1"}}), "pott")
    refused(variant(**{f"{ask}__answer__min": {"calc": "open('x')"}}), "open")
    refused(variant(**{f"{ask}__answer": {"type": "player", "min": 1}}), "min")
    refused(variant(**{"steps__1__do": [{"set": {"key": "pot",
                                                 "value": {"calc": "$answer"}}}]}),
            "answer")
    refused(variant(**{"steps__0__until": None}), "until")
    refused(variant(**{"steps__0__max": 0}), "max")
    refused(variant(**{"steps__0__steps": [copy.deepcopy(CLIMB["steps"][0])]}),
            "repeat")
    refused(variant(**{"steps__1__do": [{"set": {"key": "score", "value": 1,
                                                 "player": 1, "players": "all"}}]}),
            "players")
    refused(variant(**{"steps__1__do": [{"say": {"text": "hi",
                                                 "if": "the pot is large"}}]}),
            "if")
    refused(variant(**{"steps__1__do": [{"say": {}}]}), "say")
    refused(variant(**{"end__most_climbs__result": "seat 1"}), "rank")
    refused(variant(**{"steps__1__do": [{"set": {"key": "pot",
                                                 "value": {"calc": "you.cash"}}}]}),
            "cash")
