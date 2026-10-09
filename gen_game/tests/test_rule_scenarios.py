"""Scenarios that answer by naming the option on offer, and the tiers that no longer judge reasoning."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import evaluate, harness, scenarios  # noqa: E402
from xcolos.games.loader import load_file  # noqa: E402

RPS = load_file(Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library" / "rps.json")

ROCK_BEATS_SCISSORS = {
    "name": "rock against scissors every round", "players": 2, "seed": 1,
    "rules": [{"seat": 1, "options_include": "rock", "times": "all"},
              {"seat": 2, "options_include": "scissors", "times": "all"}],
    "expect": {"result": "seat 1"},
}


def test_a_scenario_that_names_the_options_plays_the_game():
    out = scenarios.run_scenario(RPS, ROCK_BEATS_SCISSORS)
    assert out.passed, out.failures


def test_a_wrong_expectation_fails_with_the_difference():
    out = scenarios.run_scenario(RPS, {**ROCK_BEATS_SCISSORS, "expect": {"result": "seat 2"}})
    assert not out.passed and "expected 'seat 2', got 'seat 1'" in " ".join(out.failures)


def test_a_rule_the_game_never_matches_is_reported_as_the_game_not_asking_it():
    s = {**ROCK_BEATS_SCISSORS, "rules": ROCK_BEATS_SCISSORS["rules"] + [{"seat": 1, "options_include": "lizard", "times": 1}]}
    out = scenarios.run_scenario(RPS, s)
    assert not out.passed and any("'lizard' was never matched" in f for f in out.failures), out.failures


def test_an_extra_question_does_not_shift_later_answers_because_rules_name_options():
    agent = harness.RuleAgent("A", [{"seat": 1, "options_include": "rock", "times": "all"}], "decline")
    legal = ["paper", "rock", "scissors"]

    class Env:
        legal_targets = legal
        schema = None

    class Schema:
        id, target = "q", "choice"

    agent._schema = lambda env: Schema()
    assert agent.decide(Env()).target == "rock" and agent.decide(Env()).target == "rock"


def test_a_question_no_rule_matches_gets_the_decline_default():
    agent = harness.RuleAgent("A", [], "decline")

    class Env:
        legal_targets = ["Block Duke", "No block", "Block Captain"]

    class Schema:
        id, target = "q", "choice"

    agent._schema = lambda env: Schema()
    assert agent.decide(Env()).target == "No block"


def test_scenarios_with_rules_are_valid_and_without_either_form_are_not():
    assert scenarios.problems([ROCK_BEATS_SCISSORS]) == []
    bad = {k: v for k, v in ROCK_BEATS_SCISSORS.items() if k != "rules"}
    assert any("needs `rules`" in p for p in scenarios.problems([bad]))
    assert any("`seat` and an `options_include`" in p for p in scenarios.problems([{**ROCK_BEATS_SCISSORS, "rules": [{"options_include": "rock"}]}]))


def test_the_reasoning_and_balance_checks_are_not_run_unless_asked():
    skipped = evaluate.not_run()
    assert skipped["flags"] == [] and skipped["skipped"] is True


def test_a_scenario_can_start_from_a_stated_situation_and_stop_after_one_round():
    # rps: seat 1 holds a rock, seat 2 a scissors; after one round seat 1 has scored
    s = {"name": "rock beats scissors in one round", "players": 2, "rounds": 1,
         "given": {"players": {"1": {"score": 5}}},
         "rules": [{"seat": 1, "options_include": "rock", "times": "all"}, {"seat": 2, "options_include": "scissors", "times": "all"}],
         "expect": {"players": {"1": {"score": 6}}}}  # 5 given, plus the point for winning the round
    out = scenarios.run_scenario(RPS, s)
    assert out.passed, out.failures
    wrong = {**s, "expect": {"players": {"1": {"score": 99}}}}
    assert not scenarios.run_scenario(RPS, wrong).passed


def test_given_must_name_attributes_the_spec_lists_and_rounds_must_be_a_whole_number():
    keys = {"player": ["coins"], "game": ["deck"]}
    ok = {"name": "x", "players": 2, "rounds": 1, "given": {"players": {"1": {"coins": 7}}}, "rules": [{"seat": 1, "options_include": "a"}], "expect": {}}
    assert scenarios.problems([ok], attribute_keys=keys) == []
    bad = {**ok, "given": {"players": {"1": {"gold": 7}}}, "rounds": 0}
    found = " ".join(scenarios.problems([bad], attribute_keys=keys))
    assert "`gold` is not in the spec" in found and "rounds is a whole number" in found
