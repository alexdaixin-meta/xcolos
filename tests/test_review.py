"""The post-game review.

What the reviewer is shown, what it must answer, and that a table waits for it
without the last player's request waiting too.
"""

from __future__ import annotations

import json
import sys
import threading
import time
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_calc_and_repeat import CLIMB, Lowest  # noqa: E402
from xcolos import review
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.loader import load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner


class Thinker(Lowest):
    """Plays the lowest legal answer and says why, what it expects, and what it changed."""

    def decide(self, env):
        return replace(super().decide(env),
                       reason=f"{self.name} REASON pot is low",
                       predict=f"{self.name} PREDICT others go low too",
                       adjust=f"{self.name} ADJUST stay low")


def play(seats: int = 3):
    definition = load(json.dumps(CLIMB), source="climb")
    game = Game("climb", definition.id, 1, MatchLog("climb"))
    registry = Registry(game.match_id)
    host = LocalAgentHost([Thinker(name=f"P{i}") for i in range(seats)],
                          player=Player.new("operator"))
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition)
    Runner(game, orchestrator, registry).run()
    return game, orchestrator, definition


class Canned:
    """A completion that returns a fixed reply and remembers what it was sent."""

    model = "canned"

    def __init__(self, reply):
        self.reply, self.sent = reply, []

    def complete(self, prompt, system=""):
        self.sent.append((system, prompt))
        return self.reply


def good_reply(seats):
    return json.dumps({
        "summary": "Everyone climbed by one, all the way.",
        "players": [{"seat": s, "review": f"seat {s} crept up", "score": 5} for s in seats],
    })


def reviews(game):
    return [r for r in game.log.records if r["type"] == "review"]


# ----------------------------------------------------------------------
# What the reviewer reads
# ----------------------------------------------------------------------


def test_the_record_holds_every_players_thinking_and_the_end_state():
    game, orchestrator, _ = play()
    facts = review.record(game, orchestrator.flow.full_view())
    assert [p["seat"] for p in facts["players"]] == [1, 2, 3]
    assert "score" in facts["players"][0]["at_the_end"]
    assert facts["table"]["pot"] >= 30
    moves = facts["moves"]
    assert moves and all({"reason", "predict", "adjust"} <= set(m) for m in moves)
    assert {m["seat"] for m in moves} == {1, 2, 3}
    assert facts["result"]["winner"]


def test_a_message_everyone_got_is_listed_once():
    game, orchestrator, _ = play()
    facts = review.record(game)
    keys = [(m["round"], m["text"]) for m in facts["messages"]]
    assert len(keys) == len(set(keys))
    assert any(m["to"] == "everyone" for m in facts["messages"])


def test_the_prompt_carries_the_rules_and_names_every_seat():
    game, orchestrator, definition = play()
    system, body = review.prompt(review.record(game), definition.rules_text)
    assert definition.rules_text in system
    assert "P1 PREDICT" in body and "P2 ADJUST" in body
    assert "[1, 2, 3]" in body


# ----------------------------------------------------------------------
# What it must answer
# ----------------------------------------------------------------------


def test_a_good_answer_is_read_even_inside_prose():
    checked, why = review.read("Here you go:\n" + good_reply([1, 2]) + "\nDone.", [1, 2])
    assert why == "" and checked["players"][1] == {"seat": 2, "review": "seat 2 crept up",
                                                   "score": 5}


def test_a_bad_answer_is_refused_with_a_reason():
    ok = json.loads(good_reply([1, 2]))
    cases = {
        "not json at all": "JSON",
        "{not json}": "valid JSON",
        json.dumps({**ok, "summary": " "}): "summary",
        json.dumps({**ok, "players": ok["players"][:1]}): "seat(s) [2]",
        json.dumps({**ok, "players": ok["players"] + ok["players"][:1]}): "twice",
        json.dumps({**ok, "players": [{**ok["players"][0], "score": 11}, ok["players"][1]]}):
            "1 to 10",
        json.dumps({**ok, "players": [{**ok["players"][0], "score": 6.5}, ok["players"][1]]}):
            "1 to 10",
        json.dumps({**ok, "players": [{**ok["players"][0], "review": ""}, ok["players"][1]]}):
            "no review",
    }
    for raw, fragment in cases.items():
        checked, why = review.read(raw, [1, 2])
        assert checked is None and fragment in why, (raw, why)


# ----------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------


def test_a_review_is_logged_with_its_scores():
    game, orchestrator, definition = play()
    model = Canned(good_reply([1, 2, 3]))
    review.review(game, model, rules=definition.rules_text, source="canned",
                  final=orchestrator.flow.full_view())
    [logged] = reviews(game)
    assert logged["status"] == "ok" and logged["source"] == "canned"
    assert [p["score"] for p in logged["players"]] == [5, 5, 5]
    assert len(model.sent) == 1
    json.loads(json.dumps(logged))  # survives the log's round trip


def test_no_model_and_a_bad_model_both_say_why():
    game, _, _ = play()
    review.review(game, None)
    review.review(game, Canned("I refuse."))

    class Down:
        def complete(self, prompt, system=""):
            raise TimeoutError("slow")

    review.review(game, Down())
    skipped, bad, down = reviews(game)
    assert skipped["status"] == "skipped"
    assert bad["status"] == "failed" and bad["raw"] == "I refuse."
    assert down["status"] == "failed" and "slow" in down["error"]


def test_the_review_is_never_sent_to_a_seat():
    game, _, _ = play()
    review.review(game, Canned(good_reply([1, 2, 3])))
    for fact in game.facts:
        assert "crept up" not in json.dumps(fact.payload, default=str)


# ----------------------------------------------------------------------
# The table
# ----------------------------------------------------------------------


def test_a_table_holds_done_until_its_review_is_written():
    from xcolos.web import server

    gate = threading.Event()

    class Slow(Canned):
        def complete(self, prompt, system=""):
            gate.wait(5)
            return super().complete(prompt, system)

    model = Slow(good_reply([1, 2, 3, 4, 5]))
    original = server.build_completion
    server.build_completion = lambda: model
    try:
        m = server.MatchManager()
        handle = m.create({"game": "mafia-oracle", "seed": 3,
                           "seats": [{"name": f"P{i}", "kind": "scripted"}
                                     for i in range(5)]})
        m.start_match(handle.match_id)
        deadline = time.time() + 10
        while handle.game.status.value == "running" and time.time() < deadline:
            time.sleep(0.01)
        assert handle.game.status.value != "running"
        page = m.events(handle.match_id, 0)
        assert page["done"] is False and page["state"]["reviewing"] is True

        gate.set()
        while m.events(handle.match_id, 0)["done"] is False and time.time() < deadline:
            time.sleep(0.01)
        page = m.events(handle.match_id, 0)
        assert page["done"] is True
        [logged] = [r for r in page["records"] if r["type"] == "review"]
        assert logged["status"] == "ok" and logged["source"] == "canned"
        assert "THE GAME" in model.sent[0][0]  # the flow game's rules went along
    finally:
        server.build_completion = original


def test_an_offline_table_says_there_is_no_review_and_is_done_at_once():
    from xcolos.web import server

    m = server.MatchManager()
    handle = m.create({"game": "mafia-oracle", "seed": 3,
                       "seats": [{"name": f"P{i}", "kind": "scripted"} for i in range(5)]})
    m.start_match(handle.match_id)
    deadline = time.time() + 10
    while handle.game.status.value == "running" and time.time() < deadline:
        time.sleep(0.01)
    time.sleep(0.05)  # the runner thread logs the review as it concludes
    page = m.events(handle.match_id, 0)
    assert page["done"] is True
    [logged] = [r for r in page["records"] if r["type"] == "review"]
    assert logged["status"] == "skipped"
