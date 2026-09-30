"""Rock, Paper, Scissors with limited hands, unequal wins and public hands.

Written with no engine change, so its scoring is spread across a dozen gated
steps. These tests replay what each seat played and score it from the rules
directly; if the gated steps and the rules ever disagree, the file is wrong.
"""

from __future__ import annotations

from collections import Counter

from xcolos.agents import RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games import available
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
#: What a win is worth, by the card it was won with.
VALUE = {"rock": 1, "paper": 2, "scissors": 3}


def points(a: str, b: str) -> tuple[int, int]:
    """(seat 1's points, seat 2's points) for one round."""
    if BEATS[a] == b:
        return VALUE[a], 0
    if BEATS[b] == a:
        return 0, VALUE[b]
    return 0, 0


def play(seed: int):
    log = MatchLog(f"rps_{seed}")
    game = Game(f"rps_{seed}", "rps", seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [RandomAgent(name=name, seed=seed * 10 + i)
         for i, name in enumerate(["Ada", "Blaise"])],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(available()["rps"])
    return Runner(game, orchestrator, registry).run(), game, orchestrator


def cards_played(game):
    """Each round's (seat 1 card, seat 2 card), from the moves themselves."""
    by_round: dict[int, dict[int, str]] = {}
    for r in game.log.records:
        if r["type"] == "move" and r["action"]["type"].endswith("_plays"):
            by_round.setdefault(r["round"], {})[r["seat"]] = r["action"]["target"]
    return [(cards[1], cards[2]) for _, cards in sorted(by_round.items())]


def test_a_match_lasts_ten_rounds_and_ends_on_a_declared_result():
    for seed in range(1, 6):
        result, game, _ = play(seed)
        assert result.status == "ended", result
        assert result.winner in {"seat 1", "seat 2", "draw"}
        assert len(cards_played(game)) == 10


def test_scores_follow_the_rules():
    for seed in range(1, 21):
        result, game, orchestrator = play(seed)
        expected = [0, 0]
        for pair in cards_played(game):
            a, b = points(*pair)
            expected[0] += a
            expected[1] += b
        flow = orchestrator.flow
        got = [flow.attribute(1, "score"), flow.attribute(2, "score")]
        assert got == expected, f"seed {seed}: {got} != {expected}"

        winner = ("seat 1" if expected[0] > expected[1]
                  else "seat 2" if expected[1] > expected[0] else "draw")
        assert result.winner == winner, f"seed {seed}"


def test_a_played_card_leaves_the_hand_and_two_are_kept():
    for seed in range(1, 6):
        _, game, orchestrator = play(seed)
        flow = orchestrator.flow
        played = cards_played(game)
        for seat in (1, 2):
            spent = Counter(pair[seat - 1] for pair in played)
            left = Counter(flow.attribute(seat, "hand"))
            assert sum(left.values()) == 2
            assert spent + left == Counter(rock=4, paper=4, scissors=4)


def test_a_card_stays_hidden_until_both_are_down():
    """Seat 2 plays after seat 1, so nothing about seat 1's card may reach it first."""
    _, game, _ = play(3)
    records = game.log.records
    for i, r in enumerate(records):
        if r["type"] == "move" and r["action"]["type"] == "seat_2_plays":
            earlier = [x for x in records[:i]
                       if x.get("round") == r["round"] and x["type"] == "the_reveal"]
            assert not earlier, "a reveal went out before seat 2 had played"


def test_each_seat_is_told_what_its_opponent_has_left():
    """Hands are public, so the standings show both, and they are the true hands."""
    _, game, orchestrator = play(2)
    flow = orchestrator.flow
    last = [f for f in game.facts if f.type == "the_standings" and 1 in f.entitled][-1]
    shown = {p["id"]: p["attributes"]["hand"] for p in last.payload["state"]["players"]}
    assert shown[2] == flow.attribute(2, "hand")
