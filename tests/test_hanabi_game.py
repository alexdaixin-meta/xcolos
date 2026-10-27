"""Hanabi Trio: a team target. The team wins together with team_score at or over win_threshold, or nobody wins.

The game ranks every seat by the table's `team_score`, with `min_to_win: win_threshold`. Every seat scores the
same, so at the target all seats share the win, and below it the match ends with no winner, its standings still
logged.
"""

from __future__ import annotations

import re

from gen_game import harness
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games import available
from xcolos.log import MatchLog

DEFINITION = available()["hanabi"]

#: Three hands and a short deck, as the game's own rule scenarios state them.
HANDS = {
    "1": {"hand_ids": ["#1", "#2", "#3", "#4"], "hand_faces": ["G2", "R1", "B3", "R4"]},
    "2": {"hand_ids": ["#5", "#6", "#7", "#8"], "hand_faces": ["G1", "B1", "G3", "B4"]},
    "3": {"hand_ids": ["#9", "#10", "#11", "#12"], "hand_faces": ["R2", "B2", "G4", "R3"]},
}
DECK = {"deck_ids": ["#13", "#14", "#15"], "deck_faces": ["R1", "G1", "B1"], "deck_count": 3, "active_seat": 1}


def ranked(team_score: int, players: int = 3):
    """The game's own ending, worked out on the given team score."""
    game = Game("hanabi_rank", DEFINITION.id, 1, MatchLog("hanabi_rank"))
    for seat in range(1, players + 1):
        game.register_seat(f"P{seat}", "h", None)
    orch = FlowOrchestrator(DEFINITION)
    orch.setup(game)
    orch.flow.set_attribute(None, "team_score", team_score)
    return orch._rank(DEFINITION.end[0])


def seat_one(option: str) -> list[harness.RuleAgent]:
    """Seat 1 takes `option` on its turn; the match below ends on that turn."""
    return [harness.RuleAgent(harness.NAMES[0], [{"seat": 1, "options_include": option, "times": "all"}])] + [
        harness.RuleAgent(harness.NAMES[i], []) for i in (1, 2)]


def test_the_ending_ranks_every_seat_by_the_team_score_with_the_target_as_the_bar():
    assert [(r.rank_by, r.min_to_win) for r in DEFINITION.end] == [("team_score", "win_threshold")]
    rules = DEFINITION.rules_text
    assert "the team either wins together with team_score 13 or more, or loses together below 13" in rules


def test_reaching_the_target_is_a_win_shared_by_every_seat():
    for players in (2, 3, 4):
        seats = list(range(1, players + 1))
        assert ranked(13, players) == (harness.name_seats(seats), {s: 13 for s in seats}), players
    assert ranked(15) == ("seats 1, 2 and 3", {1: 15, 2: 15, 3: 15})

    # The game ends on the third fuse with team_score 13 (a failed play costs the last fuse): the team still wins.
    given = {"players": HANDS, "game": {**DECK, "fuses": 1, "pile_red": 5, "pile_green": 5, "pile_blue": 3, "team_score": 13}}
    p = harness.play(DEFINITION, seat_one("PLAY #1"), 1, given=given)
    assert p.result.status == "ended" and p.game_attribute("fuses") == 0
    assert p.result.winner == "seats 1, 2 and 3"
    assert p.standings == {"1": 13, "2": 13, "3": 13}
    assert p.game.summary.startswith("All seats win. Team score 13 of 15 (target 13)")
    assert p.end_problems() == []


def test_missing_the_target_ends_with_no_winner_and_the_standings_logged():
    result, standings = ranked(12)
    assert result.startswith(FlowOrchestrator.NO_WINNER) and standings == {1: 12, 2: 12, 3: 12}
    assert ranked(0, 2) == (result, {1: 0, 2: 0})

    # The 40th turn ends the game with team_score 12, one short of the target.
    given = {"players": HANDS, "game": {**DECK, "turns_played": 39, "pile_red": 5, "pile_green": 4, "pile_blue": 3, "team_score": 12}}
    p = harness.play(DEFINITION, seat_one("HINT 2 G"), 1, given=given)
    assert p.result.status == "ended" and p.game_attribute("turns_played") == 40
    assert p.result.winner.startswith(FlowOrchestrator.NO_WINNER) and not re.match(r"seats? \d", p.result.winner)
    assert p.standings == {"1": 12, "2": 12, "3": 12}
    assert p.game.summary.startswith("No seat wins. Team score 12 of 15 (target 13)")
    assert p.end_problems() == []
