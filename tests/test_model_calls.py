"""Every call the server makes to a model is in the log.

The review, a Model seat's turns, and any call that failed. The referee's own
`judge_call` record already carries the same, so it is not doubled.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review import Canned, good_reply, play  # noqa: E402
from xcolos import review
from xcolos.agents import LLMAgent
from xcolos.calls import Logged
from xcolos.log import MatchLog


def model_calls(log):
    return [r for r in log.records if r["type"] == "model_call"]


def test_a_review_call_is_logged_with_both_prompts_and_the_raw_reply():
    game, orchestrator, definition = play()
    model = Canned(good_reply([1, 2, 3]))
    review.review(game, model, rules=definition.rules_text, source="canned",
                  final=orchestrator.flow.full_view())
    [logged] = model_calls(game.log)
    [(system, prompt)] = model.sent
    assert logged["category"] == "model" and logged["for"] == "review"
    assert logged["model"] == "canned"
    assert logged["system"] == system and definition.rules_text in system
    assert logged["prompt"] == prompt and "THE MOVES" in prompt
    assert logged["raw"] == model.reply and "error" not in logged
    assert logged["seconds"] >= 0


def test_a_call_that_fails_is_logged_with_why():
    game, _, _ = play()

    class Down:
        model = "down"

        def complete(self, prompt, system=""):
            raise TimeoutError("slow")

    review.review(game, Down())
    [logged] = model_calls(game.log)
    assert logged["error"] == "slow" and "raw" not in logged
    assert logged["prompt"], "what was asked is kept even when nothing came back"


def test_a_reply_that_is_not_a_review_is_still_logged_as_the_model_said_it():
    game, _, _ = play()
    review.review(game, Canned("I refuse."))
    [logged] = model_calls(game.log)
    assert logged["raw"] == "I refuse."


def test_with_no_model_nothing_is_called_and_nothing_is_logged():
    game, _, _ = play()
    review.review(game, None)
    assert model_calls(game.log) == []


def test_the_wrapper_passes_the_reply_through_unchanged():
    log = MatchLog("calls")
    model = Canned("forty-two")
    assert Logged(model, log, "test").complete("q", system="s") == "forty-two"
    assert model.sent == [("s", "q")]
    [logged] = model_calls(log)
    assert (logged["for"], logged["system"], logged["prompt"]) == ("test", "s", "q")


def test_a_model_seat_logs_every_turn_it_is_asked():
    from xcolos.web import server

    m = server.MatchManager()
    handle = m.create({"game": "auction", "seed": 4,
                       "seats": [{"name": "M", "kind": "llm"},
                                 {"name": "R", "kind": "random"}]})
    m.start_match(handle.match_id)
    deadline = time.time() + 10
    while not m.events(handle.match_id, 0)["done"] and time.time() < deadline:
        time.sleep(0.01)
    game = handle.game
    seat = next(i for i, s in game.seats.items() if s.name == "M")
    mine = [c for c in model_calls(game.log) if c["for"] == f"seat {seat}"]
    asked = [r for r in game.log.records
             if r["type"] == "action_request" and r["seat"] == seat]
    assert asked and len(mine) >= len(asked)  # one per ask, more if refused
    assert all(c["model"] == "offline-stub" and c["raw"] for c in mine)
    assert "Answer with a whole number" in mine[0]["prompt"]
    assert not [c for c in model_calls(game.log) if c["for"] != f"seat {seat}"
                and c["for"] != "review"]


def test_a_model_seat_writes_to_each_new_games_own_log():
    from xcolos.web import server

    m = server.MatchManager()
    handle = m.create({"game": "rps", "seed": 4,
                       "seats": [{"name": "M", "kind": "llm"},
                                 {"name": "R", "kind": "random"}]})
    first = handle.game
    m.start_match(handle.match_id)
    deadline = time.time() + 10
    while not m.events(handle.match_id, 0)["done"] and time.time() < deadline:
        time.sleep(0.01)
    count = len(model_calls(first.log))
    assert count
    [agent] = [a for a in handle.hosts["bots"].agents if isinstance(a, LLMAgent)]
    m._new_game(handle)
    assert agent.log is handle.game.log and handle.game.log is not first.log
    assert len(model_calls(first.log)) == count


def test_a_model_call_never_reaches_a_seat():
    game, _, _ = play()
    review.review(game, Canned(good_reply([1, 2, 3])))
    for fact in game.facts:
        assert "THE MOVES" not in json.dumps(fact.payload, default=str)

