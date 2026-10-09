"""Talk that reaches the table, and keeping who answered what.

A broadcast used to be able to name a `verify` binding that did not exist yet, so players were
sent the literal `{talk_msg}`. A tally also lost who answered what, so a challenge from one
player among three was counted as a pass. Both are shown here on a toy game.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gen_game import harness  # noqa: E402
from xcolos.games.definition import DefinitionError  # noqa: E402
from xcolos.games.loader import load  # noqa: E402

TOY = {
    "schema": 1,
    "meta": {"id": "toy", "name": "Toy", "players": {"min": 3, "max": 3}},
    "statuses": [{"id": "playing", "acts": True, "initial": True}],
    "attributes": {
        "player": [{"key": "said", "visible": "public", "type": "text", "initial": ""}],
        "game": [{"key": "who", "visible": "public", "type": "number", "initial": 0},
                 {"key": "n", "visible": "public", "type": "number", "initial": 0}],
    },
    "setup": [],
    "steps": [
        {"use": "poll", "label": "talk", "to": "acting",
         "answer": {"type": "text", "max_words": 20},
         "broadcast": {"to": "all", "text": "Seat {seat} says: {value}"},
         "text": "Say one thing to the table."},
        {"use": "poll", "label": "challenge", "to": "acting",
         "answer": {"type": "choice", "options": ["Challenge", "Pass"]},
         "store": "said", "text": "Challenge or pass?"},
        {"use": "update", "label": "tally", "text": "The votes are tallied.",
         "do": [{"set": {"key": "n", "value": {"calc": "count(p.said == 'Challenge' for p in players)"}}},
                {"set": {"key": "who", "value": {"calc": "min([p.seat for p in players if p.said == 'Challenge'] + [9])"}}}]},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ],
    "end": {"done": {"when": {"calc": "True"}, "result": "draw",
                     "text": "{n} challenged, the first was seat {who}."}},
}


def toy(**change) -> str:
    raw = copy.deepcopy(TOY)
    for path, value in change.items():
        step, key = path.split("__")
        raw["steps"][int(step)][key] = value
    return json.dumps(raw)


def refused(text: str) -> str:
    try:
        load(text)
    except DefinitionError as exc:
        return str(exc)
    raise AssertionError("the loader accepted it")


def test_a_broadcast_naming_a_verify_binding_is_refused_at_load():
    bad = toy(**{"0__broadcast": {"to": "all", "text": "Talk: {talk_msg}"}})
    assert "{talk_msg} is not available in a broadcast" in refused(bad)


def test_a_broadcast_with_value_and_seat_reaches_the_table_with_the_words_filled_in():
    played = harness.play(load(toy()), harness.random_agents(3, 1), 1)
    said = [r["payload"]["rendered"] for r in played.game.log.records
            if r.get("category") == "fact" and r.get("type") == "talk"]
    assert len(said) == 3
    assert all(s.startswith("Seat ") and "{" not in s for s in said), said


def test_store_keeps_each_players_own_answer_so_a_calc_can_say_who_gave_it():
    for seed in range(1, 8):
        played = harness.play(load(toy()), harness.random_agents(3, seed), seed)
        end = next(r["payload"]["rendered"] for r in played.game.log.records
                   if r.get("type") == "game_over")
        n, first = int(end.split()[0]), int(end.rsplit(" ", 1)[1].rstrip("."))
        assert (n == 0) == (first == 9), end
        assert 0 <= n <= 3 and (first == 9 or 1 <= first <= 3), end


def test_store_must_name_a_declared_player_attribute():
    assert "is not a player attribute" in refused(toy(**{"1__store": "nope"}))


def test_the_public_history_is_what_the_whole_table_was_told_in_order():
    played = harness.play(load(toy()), harness.random_agents(3, 2), 2)
    lines = played.orchestrator._public_history(played.game)
    talk = [line for line in lines if "says:" in line]
    assert [line.split(" says:")[0] for line in talk] == ["round 1: Seat 1", "round 1: Seat 2", "round 1: Seat 3"], lines
    assert lines[-1] == "round 1: The votes are tallied."


def test_an_expression_in_a_prompt_that_needs_a_seat_is_left_as_written_not_a_crash():
    raw = json.loads(toy())
    raw["steps"][1]["text"] = "You have {you.said} said so far. Challenge or pass?"
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    assert played.result.status == "ended"


def test_setting_a_status_a_player_already_has_changes_and_announces_nothing():
    raw = json.loads(toy())
    raw["statuses"] = [{"id": "playing", "acts": True, "initial": True}, {"id": "out", "acts": False}]
    out = {"set_status": {"player": 1, "to": "out", "text": "Seat {player} is out of the game."}}
    raw["steps"] = [
        {"use": "update", "label": "first", "text": "The first out.", "do": [out]},
        {"use": "update", "label": "again", "text": "The same again.", "do": [out]},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    told = [r for r in played.game.log.records
            if r.get("category") == "fact" and "is out of the game" in str(r["payload"].get("rendered"))]
    assert len(told) == 1, [t["payload"] for t in told]


def test_a_question_with_one_legal_option_is_answered_for_the_player_not_asked():
    raw = json.loads(toy())
    raw["steps"][1]["answer"]["options"] = ["Pass"]  # nothing to decide
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    asked = [r for r in played.game.log.records if r.get("type") == "action_request" and r.get("action_schema") == "challenge"]
    auto = [r for r in played.game.log.records if r.get("type") == "auto_answer"]
    assert asked == [] and len(auto) == 3, (len(asked), len(auto))
    end = next(r["payload"]["rendered"] for r in played.game.log.records if r.get("type") == "game_over")
    assert end.startswith("0 challenged")  # the forced answer is still an answer, and the tally saw it


def test_a_group_operation_does_not_announce_what_it_did_to_a_player_who_is_already_out():
    raw = json.loads(toy())
    raw["statuses"] = [{"id": "playing", "acts": True, "initial": True}, {"id": "out", "acts": False}]
    raw["steps"] = [
        {"use": "update", "label": "one leaves", "text": "Seat one is out.", "do": [{"set_status": {"player": 1, "to": "out"}}]},
        {"use": "update", "label": "everyone is told", "text": "The tally is in.",
         "do": [{"set": {"players": "all", "key": "said", "value": "x", "text": "Seat {player} answers: {value}."}}]},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    told = sorted(r["payload"]["rendered"] for r in played.game.log.records
                  if r.get("category") == "fact" and "answers:" in str(r["payload"].get("rendered")))
    assert told == ["Seat 2 answers: x.", "Seat 3 answers: x."], told


def test_a_tell_about_a_subject_nobody_was_chosen_for_says_nothing_instead_of_literal_braces():
    raw = json.loads(toy())
    raw["attributes"]["game"].append({"key": "victim", "visible": "public", "type": "number", "initial": 0})
    raw["steps"] = [
        {"use": "tell", "label": "dawn", "to": "all", "about": "$victim", "text": "Seat {subject} was found dead."},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    told = [r for r in played.game.log.records if r.get("category") == "fact" and "found dead" in str(r["payload"].get("rendered"))]
    assert told == [], [t["payload"] for t in told]
