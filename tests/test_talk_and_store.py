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


def _told(attribute: dict, op: str, change: dict) -> list[dict]:
    """The facts one announced change makes, on the toy with `attribute` declared."""
    raw = json.loads(toy())
    raw["attributes"]["player" if "player" in change else "game"].append(attribute)
    raw["steps"] = [
        {"use": "update", "label": "the change", "do": [{op: change}]},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    return [r for r in played.game.log.records
            if r.get("category") == "fact" and r.get("type") == f"the_change_{op}"]


def test_announcing_a_change_to_a_hidden_table_attribute_tells_the_words_but_not_the_value():
    told = _told({"key": "slot", "visible": "none", "type": "number", "initial": 0},
                 "set", {"key": "slot", "value": 7, "text": "Someone put a card face down."})
    assert [t["payload"]["rendered"] for t in told] == ["Someone put a card face down."]
    assert sorted(told[0]["entitled"]) == [1, 2, 3]
    assert "value" not in told[0]["payload"], told[0]["payload"]


def test_announcing_a_change_to_a_private_player_attribute_gives_the_value_to_its_owner_alone():
    told = _told({"key": "cash", "visible": "ally", "type": "number", "initial": 0},
                 "adjust", {"player": 2, "key": "cash", "value": 12,
                            "text": "Seat {player} takes a cheque of {value}."})
    by_seat = {seat: t["payload"] for t in told for seat in t["entitled"]}
    assert sorted(by_seat) == [1, 2, 3]
    # The words are the game's, and these say the amount: everyone reads them.
    assert {p["rendered"] for p in by_seat.values()} == {"Seat 2 takes a cheque of 12."}
    assert by_seat[2]["value"] == 12
    assert "value" not in by_seat[1] and "value" not in by_seat[3]


def test_announcing_a_change_to_a_public_attribute_is_one_fact_with_its_value_for_everyone():
    told = _told({"key": "up", "visible": "public", "type": "number", "initial": 0},
                 "set", {"key": "up", "value": 4, "text": "The face-up card is now {value}."})
    assert len(told) == 1 and sorted(told[0]["entitled"]) == [1, 2, 3]
    assert told[0]["payload"]["value"] == 4


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


def test_a_model_seat_gets_its_session_the_rules_and_the_question_and_its_reply_is_the_move():
    from xcolos.seat_models import SEAT_SYSTEM, seat_completion
    from xcolos.agents import LLMAgent

    seen = []

    class Echo:  # stands in for a provider: prompt in, one legal answer out
        def complete(self, prompt, system=""):
            seen.append((system, prompt))
            return "Pass"

    import xcolos.seat_models as sm
    original = sm.from_spec
    sm.from_spec = lambda spec: Echo()
    try:
        completion = seat_completion("command:ignored")
    finally:
        sm.from_spec = original
    raw = json.loads(toy())
    raw["steps"][1]["answer"]["options"] = ["Challenge", "Pass"]
    agents = [LLMAgent(f"M{i}", completion, system=SEAT_SYSTEM) for i in range(3)]
    played = harness.play(load(json.dumps(raw)), agents, 1)
    assert played.result.status == "ended" and seen
    system, prompt = seen[0]
    assert system.startswith("You are one player in a game") and "[user]" in prompt  # the seat's own session, flattened
    assert all(a.calls > 0 for a in agents)


def test_two_of_the_same_card_in_a_hand_are_one_choice_and_a_hand_of_identical_cards_is_not_asked():
    raw = json.loads(toy())
    raw["attributes"]["player"].append({"key": "hand", "visible": "ally", "type": "list", "initial": ["Duke", "Duke"]})
    raw["steps"] = [
        {"use": "ask", "label": "which to show", "to": "acting", "text": "Choose a card to show.",
         "answer": {"type": "choice", "options": {"attribute": "hand"}}, "store": "said"},
        {"use": "check", "label": "the end", "when": {"calc": "True"}},
    ]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    asked = [r for r in played.game.log.records if r.get("type") == "action_request"]
    auto = [r for r in played.game.log.records if r.get("type") == "auto_answer"]
    assert asked == [] and len(auto) == 3 and all(a["value"] == "Duke" for a in auto)
    assert all(played.attribute(s, "said") == "Duke" for s in (1, 2, 3))  # the forced answer is still an answer


def test_a_seat_that_starts_a_scenario_already_out_is_given_its_platform_status_and_is_not_asked():
    raw = json.loads(toy())
    raw["statuses"] = [{"id": "playing", "acts": True, "initial": True}, {"id": "out", "acts": False}]
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1, given={"status": {"2": "out"}})
    asked = {r["seat"] for r in played.game.log.records if r.get("type") == "action_request"}
    assert 2 not in asked and asked == {1, 3}, asked


def test_an_ending_summary_is_asked_to_stay_within_the_history_and_to_say_who_won():
    from xcolos.flow import FlowOrchestrator

    raw = json.loads(toy())
    raw["end"]["done"]["llm"] = "Summarize how the game went."
    seen = []
    original = FlowOrchestrator._say

    def spy(self, game, heard, text, llm, extra, fact_type, max_words=0, once=False):
        if fact_type == "game_over":
            seen.append((llm, extra))
        return original(self, game, heard, text, llm, extra, fact_type, max_words, once)

    FlowOrchestrator._say = spy
    try:
        harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1)
    finally:
        FlowOrchestrator._say = original
    llm, extra = seen[0]
    assert llm.startswith("Summarize how the game went.") and "use ONLY the events listed in `history`" in llm and "State who won" in llm
    assert isinstance(extra["history"], list) and extra["history"]


def test_a_game_can_name_the_table_size_it_plays_best_at_and_it_must_lie_inside_its_range():
    from xcolos.games.definition import DefinitionError

    raw = json.loads(toy())
    raw["meta"]["players"] = {"min": 3, "max": 5, "suggested": 4}
    assert load(json.dumps(raw)).suggested_players == 4
    raw["meta"]["players"] = {"min": 3, "max": 5}
    assert load(json.dumps(raw)).suggested_players == 3  # not said: the minimum
    raw["meta"]["players"] = {"min": 3, "max": 5, "suggested": 7}
    try:
        load(json.dumps(raw))
    except DefinitionError as exc:
        assert "suggested" in str(exc)
    else:
        raise AssertionError("a suggestion outside the range must be refused")


def test_the_console_catalogue_carries_the_suggested_table_size():
    from xcolos.web.server import catalogue

    for g in catalogue():
        assert g["min_seats"] <= g["suggested_seats"] <= g["max_seats"], g


def _ending_with_a_model(reply_text):
    from xcolos.flow.judge import ScriptedJudge

    raw = json.loads(toy())
    raw["steps"] = [{"use": "check", "label": "the end", "when": {"calc": "True"}}]
    raw["end"] = {"done": {"when": {"calc": "True"}, "result": "draw", "text": "The game is over and nobody won.", "llm": "Tell how the game went."}}
    judge = ScriptedJudge(lambda call: {"type": "info", "text": reply_text})
    played = harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1, judge=judge)
    told = [(r["payload"]["rendered"], r.get("audience", {}).get("kind")) for r in played.game.log.records
            if r.get("category") == "fact" and r.get("type") == "game_over"]
    return judge, told


def test_a_models_ending_that_is_not_prose_is_never_announced_the_games_own_text_is():
    for bad in ("false", "True", "None", "  ", "null."):
        judge, told = _ending_with_a_model(bad)
        assert told == [("The game is over and nobody won.", "all")], (bad, told)


def test_a_public_ending_is_written_once_from_the_public_view_and_told_to_everyone():
    judge, told = _ending_with_a_model("Seat 1 opened, seat 2 replied, and it ended level.")
    assert len(judge.asked) == 1  # not one call, and one account, for each seat
    assert told == [("Seat 1 opened, seat 2 replied, and it ended level.", "all")]
    table = judge.asked[0].table
    assert "you" not in table and all(set(p["attributes"]) <= {"said"} for p in table["players"])  # only what is public


def test_an_announcement_that_is_not_an_ending_is_still_written_for_each_listener_separately():
    from xcolos.flow.judge import ScriptedJudge

    raw = json.loads(toy())
    raw["steps"] = [{"use": "update", "label": "the news", "text": "Something happened.", "llm": "Say what happened.", "do": [{"set": {"key": "n", "value": 1}}]},
                    {"use": "check", "label": "the end", "when": {"calc": "True"}}]
    judge = ScriptedJudge(lambda call: {"type": "info", "text": f"for seat {call.where.tag[-1]}"})
    harness.play(load(json.dumps(raw)), harness.random_agents(3, 1), 1, judge=judge)
    assert len(judge.asked) == 3
