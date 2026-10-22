"""The play-trace lint reads match logs for what the rules scenarios cannot see."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import lint  # noqa: E402
from xcolos.games.loader import load_file  # noqa: E402

LIBRARY = Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library"


def fact(kind, text, rnd=1, audience="all", **payload):
    return {"category": "fact", "type": kind, "round": rnd, "audience": {"kind": audience}, "payload": {"rendered": text, **payload}}


def test_a_message_that_still_has_a_placeholder_is_found():
    found = lint.scan([fact("dawn", "Seat {subject} was found dead.")])
    assert len(found) == 1 and found[0].startswith("placeholder:") and "{subject}" in found[0]


def test_braces_that_are_not_a_placeholder_are_left_alone():
    assert lint.scan([fact("state", "hand ['a'] lost [] learned {}"), fact("x", "You hold {'a': 1}.")]) == []


def test_an_announcement_that_says_nothing_is_found_but_a_heading_with_a_colon_is_not():
    assert lint.scan([fact("count", "Seat 4 answers: .")])[0].startswith("empty:")
    assert lint.scan([fact("state", "Coins and cards:\nseat 1: 2 coins")]) == []


def test_the_same_announcement_twice_in_a_round_is_found_but_one_line_per_answer_is_not():
    twice = [fact("check", "That target is not legal.", rnd=3), fact("check", "That target is not legal.", rnd=3)]
    assert lint.scan(twice)[0].startswith("repeated:")
    answers = [fact("bid", "pass on item 5.", seat=1, value="pass"), fact("bid", "pass on item 5.", seat=2, value="pass")]
    assert lint.scan(answers) == []
    assert lint.scan([fact("check", "again", rnd=1), fact("check", "again", rnd=2)]) == []


def test_a_question_with_a_single_option_is_found_unless_it_asks_for_a_number():
    one = {"category": "orchestrator", "type": "action_request", "round": 1, "seat": 2, "action_schema": "react", "legal_targets": ["pass"], "prompt": "React."}
    assert lint.scan([one])[0].startswith("one option:")
    assert lint.scan([one], frozenset({"react"})) == []


def test_the_shipped_games_have_no_unfilled_placeholders_in_random_play():
    for name in ("rps", "auction", "battle_of_wits", "assurance_game"):
        result = lint.trace_lint(load_file(LIBRARY / f"{name}.json"), seeds=range(1, 3))
        assert not [f for f in result["findings"] if f.startswith("placeholder:")], (name, result["findings"])
        assert result["metrics"]["matches"] > 0 and result["metrics"]["prompt_chars_max"] > 0


def test_the_text_a_seat_is_sent_is_checked_too_not_only_the_logged_facts():
    clutter = ("Your state: you are seat 1. coins 1. action , action_status going, block_role , blocker 0, claimed_role , winner . "
               "Seat {subject} was found dead.")
    found = lint.scan_bodies([("YOUR_TURN", clutter)])
    assert any(f.startswith("blank:") and "action" in f for f in found)
    assert any(f.startswith("placeholder:") and "{subject}" in f for f in found)
    assert lint.scan_bodies([("YOUR_TURN", "You are seat 1. coins 2, hidden_cards ['Duke']. Choose one action: income, tax.")]) == []


def test_a_clean_game_has_no_blank_or_unfilled_text_in_what_its_seats_are_sent():
    from gen_game import harness

    for name in ("rps", "battle_of_wits", "assurance_game"):
        agents = harness.listening_agents(2 if name != "assurance_game" else 3, 1)
        harness.play(load_file(LIBRARY / f"{name}.json"), agents, 1)
        bodies = [b for a in agents for b in a.bodies]
        assert bodies and lint.scan_bodies(bodies) == [], (name, lint.scan_bodies(bodies)[:1])
