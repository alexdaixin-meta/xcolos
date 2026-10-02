"""The Sequential Budget Auction.

Every number in it — the total, the budgets, the raise, the value range — is
declared in the game file, so these tests read them from there too. Each test
replays the auction from the moves themselves and checks it against the rules,
not against what the engine says happened.
"""

from __future__ import annotations

import sys
from pathlib import Path

from xcolos.agents import RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games import available
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

sys.path.insert(0, str(Path(__file__).resolve().parent))
from referee import referee  # noqa: E402

DEFINITION = available()["auction"]


def declared(key):
    return next(a.initial for a in DEFINITION.game_attributes if a.key == key)


def play(seed: int, n: int = 4):
    log = MatchLog(f"auction_{seed}_{n}")
    game = Game(f"auction_{seed}_{n}", "auction", seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [RandomAgent(name=f"p{i}", seed=seed * 10 + i) for i in range(n)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    # The referee decides the winner by final wealth, as the file says in words.
    orchestrator = FlowOrchestrator(
        DEFINITION, referee(lambda you: you["cash"] + you["holdings"]))
    return Runner(game, orchestrator, registry).run(), game, orchestrator


def bids_by_item(game):
    """Each item's answers in the order given: [(seat, bid or "pass"), ...]."""
    items: dict[int, list] = {}
    for r in game.log.records:
        if r["type"] == "move" and r["action"]["type"] == "bid":
            items.setdefault(r["round"], []).append((r["seat"], r["action"]["target"]))
    return items


def cases():
    for n in range(2, 7):
        for seed in range(1, 6):
            yield seed, n


def test_the_numbers_come_from_the_file():
    assert declared("total_value") == 2000
    assert declared("start_cash") == 1000
    assert declared("min_raise") == 10
    rules = DEFINITION.rules_text
    assert "{" not in rules and "2000" in rules and "1000" in rules


def test_every_table_size_sells_every_item_and_ends():
    for seed, n in cases():
        result, _, orchestrator = play(seed, n)
        assert result.status == "ended", (seed, n, result)
        assert result.rounds == declared("items")
        assert orchestrator.flow.game_attributes["item"] == declared("items")


def test_values_are_hidden_but_fixed_in_sum_and_range():
    for seed, n in cases():
        _, _, orchestrator = play(seed, n)
        table = orchestrator.flow.game_attributes
        values = table["values"]
        assert len(values) == declared("items")
        assert sum(values) == declared("total_value")
        assert all(declared("value_min") <= v <= declared("value_max") for v in values)
        assert table["revealed"] == values


def test_a_minimum_bid_is_a_fraction_of_the_true_value():
    step = declared("min_raise")
    for seed, n in cases():
        _, _, orchestrator = play(seed, n)
        table = orchestrator.flow.game_attributes
        for value, low in zip(table["values"], table["min_bids"]):
            assert low % step == 0
            # Rounded to the raise, so allow half a step either side.
            assert declared("ratio_min") * value - step / 2 <= low
            assert low <= declared("ratio_max") * value + step / 2


def test_every_bid_is_legal_and_the_last_bidder_pays_it():
    for seed, n in cases():
        result, game, orchestrator = play(seed, n)
        flow = orchestrator.flow
        values = flow.game_attributes["values"]
        min_bids = flow.game_attributes["min_bids"]
        cash = {s: declared("start_cash") for s in range(1, n + 1)}
        holdings = {s: 0 for s in cash}
        won = {s: [] for s in cash}

        for item, answers in sorted(bids_by_item(game).items()):
            high, leader = 0, 0
            for seat, bid in answers:
                if bid == "pass":
                    continue
                assert bid >= max(min_bids[item - 1], high + declared("min_raise")), (
                    seed, n, item, seat, bid, high)
                assert bid <= cash[seat], (seed, n, item, seat, bid, cash[seat])
                assert seat != leader, "the leader was asked again"
                high, leader = bid, seat
            if leader:
                cash[leader] -= high
                holdings[leader] += values[item - 1]
                won[leader].append(item)

        for s in cash:
            assert cash[s] >= 0
            assert flow.attribute(s, "cash") == cash[s], (seed, n, s)
            assert flow.attribute(s, "holdings") == holdings[s], (seed, n, s)
            assert flow.attribute(s, "won") == won[s], (seed, n, s)

        wealth = {s: cash[s] + holdings[s] for s in cash}
        best = max(wealth.values())
        top = [s for s in wealth if wealth[s] == best]
        expected = f"seat {top[0]}" if len(top) == 1 else (
            "seats " + ", ".join(map(str, top[:-1])) + f" and {top[-1]}")
        assert result.winner == expected, (seed, n, result.winner, wealth)


def test_no_seat_is_told_the_hidden_values():
    for seed, n in cases():
        _, game, orchestrator = play(seed, n)
        values = orchestrator.flow.game_attributes["values"]
        for fact in game.facts:
            assert "values" not in (fact.payload.get("state") or {}).get("table", {})
        for r in game.log.records:
            if r["type"] == "to_agent":
                assert str(values) not in str(r), (seed, n)


def test_an_items_value_is_revealed_only_after_it_sells():
    _, game, orchestrator = play(2, 4)
    values = orchestrator.flow.game_attributes["values"]
    for fact in game.facts:
        table = (fact.payload.get("state") or {}).get("table")
        if table:
            assert table["revealed"] == values[: len(table["revealed"])]
            assert len(table["revealed"]) <= table["item"]


def test_a_turn_states_the_legal_range_once():
    _, game, _ = play(1, 3)
    bodies = [r for r in game.log.records if r["type"] == "to_agent"
              and "Answer with a whole number" in str(r)]
    assert bodies
    for r in bodies:
        assert str(r).count("Answer with a whole number") == 1


def test_bidding_goes_round_the_table_from_a_rotating_opener():
    """Who is asked next is worked out here from the rules, not read back.

    Seat order, round and round, opening one seat later with each item. A
    pass does not take a player out. Skipped: the high bidder, and anyone who
    cannot afford the next legal bid. An item ends once everyone else has
    passed since the last bid.
    """
    step = declared("min_raise")
    for seed, n in cases():
        _, game, orchestrator = play(seed, n)
        min_bids = orchestrator.flow.game_attributes["min_bids"]
        cash = {s: declared("start_cash") for s in range(1, n + 1)}
        seats = sorted(cash)

        for item, answers in sorted(bids_by_item(game).items()):
            high, leader, passed = 0, None, set()
            need = lambda: max(min_bids[item - 1], high + step)  # noqa: E731
            able = lambda: {s for s in seats if s != leader and cash[s] >= need()}  # noqa: E731
            at = (item - 1) % n
            for seat, bid in answers:
                assert not able() <= passed, (seed, n, item, "asked after it was over")
                while seats[at] not in able():
                    at = (at + 1) % n
                assert seat == seats[at], (seed, n, item, "expected", seats[at], "got", seat)
                at = (at + 1) % n
                if bid == "pass":
                    passed.add(seat)
                else:
                    high, leader, passed = bid, seat, set()
            assert able() <= passed, (seed, n, item, "stopped early")
            if leader:
                cash[leader] -= high
