"""Scenarios that answer by naming the option on offer, and the tiers that no longer judge reasoning."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import evaluate, harness, scenarios  # noqa: E402
from xcolos.games.loader import load, load_file  # noqa: E402

RPS = load_file(Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library" / "rps.json")

from fixtures import JUDGED  # noqa: E402 - rps with a judged +100 bonus step for seat 1 and `llm` wording on the reveal


def _rock_vs_scissors():
    return [harness.RuleAgent("Ada", [{"seat": 1, "options_include": "rock", "times": "all"}]),
            harness.RuleAgent("Blaise", [{"seat": 2, "options_include": "scissors", "times": "all"}])]


def _seat1_score_after_one_round(judge=None):
    p = harness.play(JUDGED, _rock_vs_scissors(), 1, given={"players": {"1": {"score": 5}}}, rounds=1, judge=judge)
    return p.orchestrator.flow.player_attributes[1]["score"]


def test_offline_play_answers_an_unscripted_judged_step_false():
    assert _seat1_score_after_one_round() == 6  # 5 given, plus the round; no bonus


def test_a_scripted_judge_opens_the_judged_step_case_insensitively():
    assert _seat1_score_after_one_round(harness.offline_judge({"Bonus Rule": True})) == 106


def test_the_longest_matching_key_decides():
    assert _seat1_score_after_one_round(harness.offline_judge({"bonus": True, "the bonus rule applies": False})) == 6


def test_an_llm_step_played_offline_sends_its_text():
    p = harness.play(JUDGED, _rock_vs_scissors(), 1, rounds=1)
    sent = json.dumps([r for r in p.game.log.records if r.get("type") == "to_agent"], default=str)
    assert "Cards down. Seat 1 played rock" in sent and "False" not in sent


def test_tier0_ends_every_match_of_a_judged_game_and_the_judged_step_never_fires():
    t0 = evaluate.tier0(JUDGED, seeds=range(1, 6))
    assert t0["passed"], t0["problems"]
    p = harness.play(JUDGED, harness.random_agents(2, 1), 1)
    assert "Bonus to seat 1" not in json.dumps(p.game.log.records, default=str)

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


def test_a_rule_for_a_question_the_engine_answers_alone_is_used_by_that_answer():
    # seat 1 holds only a rock, so the engine plays it without asking: the rule naming rock was still met
    s = {"name": "a forced card", "players": 2, "rounds": 1,
         "given": {"players": {"1": {"hand": ["rock"]}}},
         "rules": [{"seat": 1, "options_include": "rock"}, {"seat": 2, "options_include": "scissors"}],
         "expect": {"offered": [{"seat": 1, "option": "rock"}]}}
    out = scenarios.run_scenario(RPS, s)
    assert out.passed, out.failures
    other = {**s, "rules": [{"seat": 1, "options_include": "paper"}, {"seat": 2, "options_include": "scissors"}], "expect": {}}
    out = scenarios.run_scenario(RPS, other)
    assert any("'paper' was never matched" in f for f in out.failures), out.failures


def test_the_answer_the_engine_gives_uses_up_its_rule_at_once_so_the_next_rule_answers_the_next_question():
    # seat 1 holds only a rock (the engine plays it), then is dealt a rock and a paper. The rule naming rock was met in round 1,
    # so round 2 is the paper rule's, as the script means; Hanamikoji lost a passing scenario when the rock rule took round 2
    raw = json.loads((Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library" / "rps.json").read_text())
    reveal = next(i for i, step in enumerate(raw["steps"]) if step.get("label") == "the reveal")
    raw["steps"].insert(reveal + 1, {"use": "update", "label": "a new hand", "when": {"calc": "rounds_left == 9"},
                                     "do": [{"set": {"player": 1, "key": "hand", "value": {"calc": "['rock', 'paper']"}}}]})
    game = load(json.dumps(raw), source="rps")
    s = {"name": "a forced card, then a choice", "players": 2, "rounds": 2, "default": "first",
         "given": {"players": {"1": {"hand": ["rock"]}}},
         "rules": [{"seat": 1, "options_include": "rock"}, {"seat": 1, "options_include": "paper"}],
         "expect": {"players": {"1": {"hand": ["rock"]}}}}
    out = scenarios.run_scenario(game, s)
    assert out.passed, out.failures


def test_a_scenario_that_scripts_an_answer_it_says_is_never_offered_is_sent_back():
    # Lost Cities lost a correct game to this: the seat whose turn it was not was scripted "in case", and its unused rule failed
    s = {"name": "seat 2 acts on even rounds", "players": 2, "rounds": 1,
         "rules": [{"seat": 2, "options_include": "draw pile"}, {"seat": 1, "options_include": "draw pile"}],
         "expect": {"not_offered": [{"seat": 1, "option": "Draw Pile"}]}}
    found = scenarios.problems([s])
    assert len(found) == 1 and "seat 1 is scripted to answer 'draw pile'" in found[0], found
    assert scenarios.problems([{**s, "rules": s["rules"][:1]}]) == []


def test_the_test_writer_and_triage_know_an_unused_rule_fails_and_an_invalid_answer_cannot_be_tested():
    from gen_game import triage
    assert "EVERY RULE MUST BE USED" in scenarios.SYSTEM and "never set scratch values in `given` to imitate one" in scenarios.SYSTEM
    system = triage.system_prompt()
    assert "never matched" in system and "invalid or malformed answer" in system


def test_a_scenario_can_script_the_judge_for_a_judged_step():
    s = {"name": "bonus", "players": 2, "rounds": 1, "given": {"players": {"1": {"score": 5}}},
         "rules": [{"seat": 1, "options_include": "rock", "times": "all"}, {"seat": 2, "options_include": "scissors", "times": "all"}],
         "judge": {"bonus rule applies": True}, "expect": {"players": {"1": {"score": 106}}}}
    out = scenarios.run_scenario(JUDGED, s)
    assert out.passed, out.failures
    assert not scenarios.run_scenario(JUDGED, {**s, "judge": {}}).passed  # unscripted, so false: 6, not 106


def test_a_judge_that_is_not_a_map_of_sentences_to_booleans_is_refused():
    found = " ".join(scenarios.problems([{**ROCK_BEATS_SCISSORS, "judge": {"bonus": "yes"}}]))
    assert "judge" in found
    assert scenarios.problems([{**ROCK_BEATS_SCISSORS, "judge": {"bonus": True}}]) == []


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
    bad = {**ok, "given": {"players": {"1": {"gold": 7}}}, "rounds": -1}
    found = " ".join(scenarios.problems([bad], attribute_keys=keys))
    assert "`gold` is not in the spec" in found and "rounds is a whole number" in found


def test_a_scenario_can_check_how_many_items_a_list_holds_right_after_setup():
    # rps deals a twelve-card hand to each seat
    ok = {"name": "the deal", "players": 2, "rounds": 0, "rules": [], "expect": {"lens": {"players": {"1": {"hand": 12}}}}}
    assert scenarios.run_scenario(RPS, ok).passed
    wrong = {**ok, "expect": {"lens": {"players": {"1": {"hand": 9}}}}}
    out = scenarios.run_scenario(RPS, wrong)
    assert not out.passed and "expected 9 items, got 12" in " ".join(out.failures)


def test_a_scenario_can_say_what_a_seat_was_and_was_not_offered():
    base = {"name": "offers", "players": 2, "rounds": 1, "rules": [{"seat": 1, "options_include": "rock"}],
            "expect": {"offered": [{"seat": 1, "option": "paper"}], "not_offered": [{"seat": 1, "option": "lizard"}]}}
    assert scenarios.run_scenario(RPS, base).passed
    bad = {**base, "expect": {"not_offered": [{"seat": 1, "option": "paper"}]}}
    assert any("was offered 'paper', but must not be" in f for f in scenarios.run_scenario(RPS, bad).failures)
    assert any("never offered" in f for f in scenarios.run_scenario(RPS, {**base, "expect": {"offered": [{"seat": 1, "option": "lizard"}]}}).failures)


def test_a_rule_in_a_scenario_that_stops_after_setup_is_not_reported_unused_because_nothing_is_asked():
    s = {"name": "the deal", "players": 2, "rounds": 0, "rules": [{"seat": 1, "options_include": "rock"}], "expect": {"lens": {"players": {"1": {"hand": 12}}}}}
    out = scenarios.run_scenario(RPS, s)
    assert out.passed, out.failures


def test_a_scenario_can_check_the_status_the_platform_holds_for_a_seat():
    ok = {"name": "status", "players": 2, "rounds": 0, "rules": [], "expect": {"status": {"1": "playing"}}}
    assert scenarios.run_scenario(RPS, ok).passed
    bad = scenarios.run_scenario(RPS, {**ok, "expect": {"status": {"1": "out"}}})
    assert not bad.passed and "platform status: expected 'out', got 'playing'" in " ".join(bad.failures)


# -- number questions (bids) -----------------------------------------------------

AUCTION = load_file(Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library" / "auction.json")


def test_a_bid_is_scripted_by_naming_the_number_and_a_pass_by_naming_the_word():
    s = {"name": "seat 1 bids 300, seat 2 passes", "players": 2, "rounds": 1,
         "rules": [{"seat": 1, "options_include": 300}, {"seat": 2, "options_include": "pass", "times": "all"}],
         "expect": {"players": {"1": {"cash": 700}, "2": {"cash": 1000}}}}
    out = scenarios.run_scenario(AUCTION, s)
    assert out.passed, out.failures


def test_a_number_outside_the_range_is_not_used_and_the_decline_default_passes():
    agent = harness.RuleAgent("Ada", [{"seat": 1, "options_include": 5000}])
    s = {"name": "nobody can bid 5000", "players": 2, "rounds": 1,
         "rules": [{"seat": 1, "options_include": 5000}], "expect": {"players": {"1": {"cash": 1000}, "2": {"cash": 1000}}}}
    out = scenarios.run_scenario(AUCTION, s)
    assert not out.passed and any("5000" in f and "never matched" in f for f in out.failures)  # reported unused, nobody bid
    assert agent.number("300") == 300 and agent.number(300.0) == 300 and agent.number("pass") is None and agent.number(True) is None


def test_offered_checks_a_number_against_the_range_the_seat_was_given():
    base = {"name": "ranges", "players": 2, "rounds": 1,
            "rules": [{"seat": 1, "options_include": 300}, {"seat": 2, "options_include": "pass", "times": "all"}]}
    good = {**base, "expect": {"offered": [{"seat": 1, "option": 300}, {"seat": 2, "option": 310}, {"seat": 2, "option": "pass"}],
                               "not_offered": [{"seat": 2, "option": 300}, {"seat": 2, "option": 1200}]}}
    out = scenarios.run_scenario(AUCTION, good)
    assert out.passed, out.failures
    bad = {**base, "expect": {"offered": [{"seat": 2, "option": 300}]}}
    assert any("seat 2 was never offered 300" in f for f in scenarios.run_scenario(AUCTION, bad).failures)


def test_the_older_number_rule_still_answers():
    agent = harness.RuleAgent("Ada", [{"seat": 1, "number": True, "answer": 7}])
    assert agent.unused() == ["Ada: the rule for 7 was never matched (the game never put that option to this seat)"]
