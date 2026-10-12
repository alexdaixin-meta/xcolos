"""Patterns the coder is taught, shown working on a toy game, and the check that catches the opposite habit.

The pattern: offer each seat only what it may do, from its own state, so nothing has to be refused afterwards.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gen_game import harness, lint  # noqa: E402
from xcolos.games.loader import load  # noqa: E402

BASE = {
    "schema": 1,
    "meta": {"id": "toy", "name": "Toy", "players": {"min": 3, "max": 3}},
    "statuses": [{"id": "playing", "acts": True, "initial": True}],
    "attributes": {
        "player": [{"key": "coins", "visible": "public", "type": "number", "initial": 3},
                   {"key": "offer", "visible": "ally", "type": "list", "initial": []},
                   {"key": "said", "visible": "public", "type": "text", "initial": ""}],
        "game": [{"key": "target", "visible": "public", "type": "number", "initial": 0},
                 {"key": "price", "visible": "public", "type": "number", "initial": 3},
                 {"key": "act", "visible": "public", "type": "text", "initial": ""},
                 {"key": "turns", "visible": "public", "type": "number", "initial": 0}],
    },
    "setup": [],
}

#: Seat 1 acts; it may buy only with the price in coins. Seat 2, the target, may also block. Each seat is offered exactly that.
GOOD_STEPS = [
    {"use": "update", "label": "offers", "text": "The offers are made.", "do": [
        {"set": {"key": "target", "value": 2}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['wait'] + (['buy'] if you.coins >= price else [])"}}},
    ]},
    {"use": "ask", "label": "the actor chooses", "to": {"where": "you.seat == 1"}, "text": "Choose what to do.",
     "answer": {"type": "choice", "options": {"attribute": "offer"}}, "verify": {"bind": "choice"}},
    {"use": "update", "label": "react offers", "text": "The reactions are open.", "do": [
        {"set": {"key": "act", "value": "$choice"}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['pass'] + (['block'] if you.seat == target else [])"}}},
    ]},
    {"use": "poll", "label": "the others react", "to": {"where": "you.seat != 1"}, "text": "React to what was chosen.",
     "answer": {"type": "choice", "options": {"attribute": "offer"}}, "store": "said"},
    {"use": "update", "label": "turn counted", "text": "The turn is over.", "do": [{"adjust": {"key": "turns", "value": 1}}]},
    {"use": "check", "label": "the end", "when": {"calc": "turns >= 1"}},
]
END = {"done": {"when": {"calc": "turns >= 1"}, "result": "draw", "text": "The turn is done."}}


def game(steps) -> object:
    return load(json.dumps({**BASE, "steps": steps, "end": END}))


def offered(played):
    """What each seat was offered, by question."""
    return {(r["seat"], r["action_schema"]): r["legal_targets"] for r in played.game.log.records
            if r.get("category") == "orchestrator" and r.get("type") == "action_request"}


def test_each_seat_is_offered_only_what_it_may_do_from_its_own_state():
    played = harness.play(game(GOOD_STEPS), harness.random_agents(3, 1), 1)
    seen = offered(played)
    assert seen[(1, "the_actor_chooses")] == ["wait", "buy"]            # seat 1 has the 3 coins the price needs
    assert seen[(2, "the_others_react")] == ["pass", "block"]            # the target may block
    assert (3, "the_others_react") not in seen  # nothing to decide but pass, so the engine answers it and nobody is asked
    assert lint.scan(played.game.log.records) == []


def test_a_seat_that_cannot_afford_it_is_not_offered_it():
    steps = json.loads(json.dumps(GOOD_STEPS))
    steps[0]["do"].insert(0, {"set": {"player": 1, "key": "coins", "value": 1}})
    played = harness.play(game(steps), harness.random_agents(3, 1), 1)
    assert (1, "the_actor_chooses") not in offered(played)  # only "wait" is left, so it is answered for the seat, not asked
    assert any(r.get("type") == "auto_answer" and r.get("seat") == 1 for r in played.game.log.records)


# The opposite habit: offer everything, then refuse what is not allowed and ask again.
LOOP_STEPS = [
    {"use": "update", "label": "offers", "text": "The offers are made.", "do": [
        {"set": {"players": "all", "key": "offer", "value": ["pass", "block", "challenge"]}},
        {"set": {"key": "target", "value": 2}}]},
    {"use": "repeat", "label": "reactions", "until": {"calc": "count(p.said != '' for p in players if p.seat != 1) == 2"}, "max": 5, "steps": [
        {"use": "poll", "label": "the others react", "to": {"where": "you.seat != 1 and you.said == ''"}, "text": "React to what was chosen.",
         "answer": {"type": "choice", "options": {"attribute": "offer"}}, "store": "said"},
        {"use": "update", "label": "refuse what is not allowed", "text": "Some answers were refused.", "do": [
            {"set": {"players": {"where": "you.seat != target and you.said == 'block'"}, "key": "offer",
                     "value": {"calc": "[o for o in you.offer if o != you.said]"}}},
            {"set": {"players": {"where": "you.seat != target and you.said == 'block'"}, "key": "said", "value": ""}}]},
    ]},
    {"use": "update", "label": "turn counted", "text": "The turn is over.", "do": [{"adjust": {"key": "turns", "value": 1}}]},
    {"use": "check", "label": "the end", "when": {"calc": "turns >= 1"}},
]


def test_offering_everything_and_refusing_afterwards_is_found_in_the_log():
    found = []
    for seed in range(1, 12):
        played = harness.play(game(LOOP_STEPS), harness.random_agents(3, seed), seed)
        found += [f for f in lint.scan(played.game.log.records) if f.startswith("refused:")]
    assert found, "no match picked the option that was later refused, so there was nothing to find"
    assert "offered" in found[0] and "asked again" in found[0]
