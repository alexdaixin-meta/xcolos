"""Assurance Threshold: every seat at or over the threshold wins; if nobody reaches it, nobody wins.

The game ranks seats 0/1 by whether their total reached `win_threshold`, with `min_to_win: 1`: seats over
the threshold share the win, and when none reaches it the match ends with no winner (a draw), its standings
still logged. A higher total below the threshold never wins.
"""

from __future__ import annotations

import re

from gen_game import harness
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games import available
from xcolos.log import MatchLog

DEFINITION = available()["assurance_game"]


def ranked(totals: dict[int, int]):
    """The game's own ending, worked out on the given final totals."""
    game = Game("assurance_rank", DEFINITION.id, 1, MatchLog("assurance_rank"))
    for seat in totals:
        game.register_seat(f"P{seat}", "h", None)
    orch = FlowOrchestrator(DEFINITION)
    orch.setup(game)
    for seat, total in totals.items():
        orch.flow.set_attribute(seat, "total_score", total)
    return orch._rank(DEFINITION.end[0])


def test_the_ending_ranks_by_the_threshold_with_a_bar_of_one():
    assert [(r.rank_by, r.min_to_win) for r in DEFINITION.end] == [("1 if you.total_score >= win_threshold else 0", "1")]
    rules = DEFINITION.rules_text
    assert "If none reaches threshold the game is a draw." in rules and "share the win" in rules


def test_two_seats_over_the_threshold_share_the_win():
    assert ranked({1: 40, 2: 38, 3: 37}) == ("seats 1 and 2", {1: 1, 2: 1, 3: 0})


def test_the_highest_total_below_the_threshold_does_not_win():
    assert ranked({1: 40, 2: 30, 3: 10})[0] == "seat 1"
    result, standings = ranked({1: 37, 2: 30, 3: 10})
    assert result.startswith(FlowOrchestrator.NO_WINNER) and standings == {1: 0, 2: 0, 3: 0}


def test_nobody_reaching_the_threshold_ends_the_match_with_no_winner():
    """Everyone defects every round: 2 points a round, 20 in all, under the threshold of 38."""
    agents = [harness.RuleAgent(harness.NAMES[i], [{"seat": i + 1, "options_include": "D", "times": "all"}]) for i in range(3)]
    p = harness.play(DEFINITION, agents, 1)
    assert p.result.status == "ended" and [p.attribute(s, "total_score") for s in (1, 2, 3)] == [20, 20, 20]
    assert p.result.winner.startswith(FlowOrchestrator.NO_WINNER) and not re.match(r"seats? \d", p.result.winner)
    assert p.standings == {"1": 0, "2": 0, "3": 0}
    assert "No player reached threshold" in p.game.summary and "no winner" in p.game.summary
