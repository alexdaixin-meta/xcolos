"""Playing through the game tools.

The server keeps each seat's state. When a turn is owed it writes the message
into that seat's state and waits. The agent reads its own state on its own
cadence and posts an action when one is due.

These tests drive a whole match that way, with no push to the pulling seat at
any point.
"""

from __future__ import annotations

import time

import pytest

from xcolos.agents import ScriptedAgent
from xcolos.cli import SEAT_NAMES
from xcolos.game import Game
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import AccessDenied, Player
from xcolos.log import MatchLog
from xcolos.orchestrators.mafia import MafiaOrchestrator
from xcolos.remote import ConnectorHost
from xcolos.runner import Runner
from xcolos.tools import MIN_POLL_SECONDS, TableTools


def build(seed: int, pullers: int = 1, bots: int = 4, deadline_ms: int = 60_000):
    """A table with some in-process bots and some seats that pull."""
    log = MatchLog(f"m_tools_{seed}")
    game = Game(f"m_tools_{seed}", MafiaOrchestrator.game_id, seed, log)
    registry = Registry(game.match_id)

    bot_host = LocalAgentHost(
        [ScriptedAgent(name=SEAT_NAMES[i]) for i in range(bots)],
        player=Player.new("operator"),
    )
    conn_host = ConnectorHost(
        Player.new("table"), [f"Open{i}" for i in range(pullers)]
    )

    bot_bindings = iter(bot_host.register())
    conn_bindings = iter(conn_host.register())

    runner_seats = []
    for i in range(bots + pullers):
        if i < bots:
            b = next(bot_bindings)
            index = game.register_seat(b.name, bot_host.host_id, b.profile)
            registry.attach(index, bot_host, b)
        else:
            b = next(conn_bindings)
            index = game.register_seat(b.name, conn_host.host_id, b.profile)
            registry.attach(index, conn_host, b)
            runner_seats.append((index, b.name))

    runner = Runner(game, MafiaOrchestrator(), registry, deadline_ms=deadline_ms)
    tools = TableTools(game, runner, registry, poll_seconds=5)
    for index, name in runner_seats:
        tools.offer(index, name)
    return game, runner, tools


def seat_in(tools: TableTools, name: str = "Alex") -> str:
    """The player id for the first open seat. Reading it takes the seat."""
    return tools.summary()["open_seats"][0]["player_id"]


def play_through(tools: TableTools, decide, limit: int = 200):
    """Drive a pulling seat the way an agent would: read, maybe act, repeat."""
    token = seat_in(tools)
    reads, ack = 0, None
    while reads < limit:
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        reads += 1
        if state["table"]["status"] != "running":
            return state, reads, token
        if state["your_turn"]:
            tools.post_action(token, decide(state))
    raise AssertionError("the match never finished")


def first_legal(state):
    ask = state["ask"]
    if ask["answer_with"] == "text":
        return "I have nothing useful yet."
    return ask["legal_answers"][0]


# ======================================================================
# A whole match, pulled
# ======================================================================


@pytest.mark.parametrize("seed", range(1, 11))
def test_a_pulling_agent_plays_a_whole_match(seed):
    game, runner, tools = build(seed)
    runner.start()

    state, reads, _ = play_through(tools, first_legal)
    assert state["table"]["status"] == "ended"
    assert state["outcome"]["winner"] in {"good", "evil"}
    assert reads > 1


def test_the_seat_is_never_pushed_anything():
    """A pull seat must not appear in the outbound message log at all."""
    game, runner, tools = build(3)
    runner.start()
    play_through(tools, first_legal)

    pulled = next(iter(tools.open_seats.values())).seat
    pushed = game.log.where("message", "to_agent", seat=pulled)
    assert pushed == [], "a pulling seat was pushed to"
    assert game.log.where("message", "offered", seat=pulled), "no turn was offered"


def test_two_pulling_seats_share_a_table():
    game, runner, tools = build(4, pullers=2, bots=3)
    runner.start()

    tokens = [s["player_id"] for s in tools.summary()["open_seats"]]
    acks = {t: None for t in tokens}

    for _ in range(300):
        done = False
        for t in tokens:
            state = tools.read_state(t, acks[t])
            acks[t] = state["ack_through"]
            if state["table"]["status"] != "running":
                done = True
                break
            if state["your_turn"]:
                tools.post_action(t, first_legal(state))
        if done:
            break

    assert game.status.value == "ended"


# ======================================================================
# The state an agent reads
# ======================================================================


def test_the_state_is_self_contained():
    """An assistant that lost the thread must still be able to play."""
    game, runner, tools = build(5)
    runner.start()
    token = seat_in(tools)

    state = tools.read_state(token)
    assert state["you"]["role"], "a seat must always be told its own role"
    assert state["table"]["living_seats"]
    assert state["table"]["phase"]
    assert "briefing" in state, "the rules are there until the seat acknowledges"
    assert "check_back_in_seconds" in state


def test_the_briefing_stops_repeating_once_acknowledged():
    game, runner, tools = build(5)
    runner.start()
    token = seat_in(tools)

    first = tools.read_state(token)
    assert "briefing" in first
    second = tools.read_state(token, first["ack_through"])
    assert "briefing" not in second


def test_unacknowledged_news_is_shown_again():
    """Reading is not confirming. A session that dropped it sees it again."""
    game, runner, tools = build(6)
    runner.start()
    token = seat_in(tools)

    a = tools.read_state(token)
    b = tools.read_state(token)  # no ack in between
    assert [f["fact_seq"] for f in a["new_for_you"]] == [
        f["fact_seq"] for f in b["new_for_you"]
    ]

    c = tools.read_state(token, a["ack_through"])
    assert len(c["new_for_you"]) < len(a["new_for_you"])


def test_acknowledging_never_goes_backwards():
    game, runner, tools = build(6)
    runner.start()
    token = seat_in(tools)
    seat = tools.open_seats[token].seat

    state = tools.read_state(token, None)
    tools.read_state(token, state["ack_through"])
    high = game.seats[seat].acked_upto
    tools.read_state(token, 0)
    assert game.seats[seat].acked_upto == high


def test_reads_and_acks_are_recorded():
    game, runner, tools = build(7)
    runner.start()
    token = seat_in(tools)
    seat = tools.open_seats[token].seat

    state = tools.read_state(token)
    tools.read_state(token, state["ack_through"])

    assert game.log.where("delivery", "read", seat=seat)
    assert game.log.where("delivery", "ack", seat=seat)
    assert game.seats[seat].reads >= 2
    assert game.seats[seat].last_read_at


def test_a_pulling_seat_learns_only_what_it_is_entitled_to():
    game, runner, tools = build(8)
    runner.start()
    token = seat_in(tools)
    seat = tools.open_seats[token].seat

    seen = []
    ack = None
    for _ in range(200):
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        seen.extend(f["fact_seq"] for f in state["new_for_you"])
        if state["table"]["status"] != "running":
            break
        if state["your_turn"]:
            tools.post_action(token, first_legal(state))

    for seq in seen:
        assert seat in game.facts[seq].entitled


def test_a_seat_sees_its_own_role_and_no_one_elses():
    """At the start, a role belongs to the seat that holds it and nobody else.

    The rules text names every role in the game, which is public and fine. What
    must never happen is a *seat* being tied to a role it did not earn.
    """
    game, runner, tools = build(31, pullers=5, bots=0)
    runner.start()

    truth = {i: st.role for i, st in game.seats.items()}
    for pid in [s["player_id"] for s in tools.summary()["open_seats"]]:
        state = tools.read_state(pid)
        me = state["you"]["seat"]

        assert state["you"]["role"] == truth[me], "a seat must know its own role"

        # Other seats are seat number, name and alive-or-not. Nothing else.
        for other in state["table"]["seats"]:
            assert set(other) == {"seat", "name", "status"}

        news = " ".join(f["text"] for f in state["new_for_you"]).lower()
        for other, role in truth.items():
            if other == me:
                continue
            assert not (f"seat {other}" in news and role in news), (
                f"seat {me} was told seat {other} is a {role}"
            )


def test_a_seat_knows_how_many_players_there_are_and_their_names():
    game, runner, tools = build(32, pullers=2, bots=4)
    runner.start()
    pid = tools.summary()["open_seats"][0]["player_id"]

    state = tools.read_state(pid)
    assert len(state["table"]["seats"]) == len(game.seats)
    assert all(s["name"] for s in state["table"]["seats"])
    assert state["table"]["living_seats"] == game.active_seats()


def test_a_role_only_becomes_public_when_its_holder_dies():
    """The one legitimate reveal. Mafia rules, not a leak."""
    game, runner, tools = build(33)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(200):
        state = tools.read_state(pid, ack)
        ack = state["ack_through"]
        for item in state["new_for_you"]:
            text = item["text"]
            if any(r in text for r in ("mafia", "detective", "villager")):
                fact = game.facts[item["fact_seq"]]
                assert fact.type in {
                    "role_assigned", "allies", "death", "eliminated", "game_over",
                }, f"a role surfaced in an unexpected fact: {fact.type}"
        if state["table"]["status"] != "running":
            break
        if state["your_turn"]:
            tools.post_action(pid, first_legal(state))


# ======================================================================
# Turn taking
# ======================================================================


def test_the_ask_says_exactly_what_is_acceptable():
    game, runner, tools = build(9)
    runner.start()
    token = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        if state["your_turn"]:
            ask = state["ask"]
            assert ask["action"] and ask["prompt"]
            assert ask["answer_with"] in {"text", "seat", "enum", "none"}
            assert ask["seconds_left"] > 0
            if ask["answer_with"] == "seat":
                assert ask["legal_answers"]
            return
        tools.post_action(token, "nothing")  # refused, harmless
    raise AssertionError("the seat was never asked to act")


def test_acting_out_of_turn_is_refused_not_banked():
    game, runner, tools = build(10)
    runner.start()
    token = seat_in(tools)

    state = tools.read_state(token)
    if state["your_turn"]:
        pytest.skip("this seat happened to be first")
    out = tools.post_action(token, 0)
    assert out["accepted"] is False
    assert "nothing is owed" in out["reason"]


def test_an_illegal_answer_leaves_the_turn_open():
    """A refusal is information. The seat may simply answer again."""
    game, runner, tools = build(11)
    runner.start()
    token = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        if state["your_turn"] and state["ask"]["answer_with"] == "seat":
            bad = tools.post_action(token, 9999)
            assert bad["accepted"] is False
            assert bad["legal_answers"], "a refusal should say what would work"

            again = tools.read_state(token, ack)
            assert again["your_turn"], "the turn must still be owed"

            good = tools.post_action(token, again["ask"]["legal_answers"][0])
            assert good["accepted"] is True
            return
        if state["your_turn"]:
            tools.post_action(token, first_legal(state))
    raise AssertionError("never reached a targeted action")


def test_a_turn_that_runs_out_is_defaulted():
    game, runner, tools = build(12, deadline_ms=250)
    runner.start()
    token = seat_in(tools)

    ack = None
    for _ in range(80):
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        if state["table"]["status"] != "running":
            break
        if state["your_turn"]:
            time.sleep(0.4)  # think for too long
            tools.read_state(token, ack)  # any call notices the expiry
    assert game.log.where("message", "expired"), "no turn ever expired"
    assert game.status.value in {"ended", "abandoned"}


def test_the_advised_interval_tightens_when_a_turn_is_owed():
    game, runner, tools = build(13)
    runner.start()
    token = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(token, ack)
        ack = state["ack_through"]
        if state["your_turn"]:
            assert state["check_back_in_seconds"] == MIN_POLL_SECONDS
            return
        assert state["check_back_in_seconds"] == tools.poll_seconds
        tools.post_action(token, "x")
    raise AssertionError("never owed a turn")


# ======================================================================
# Linking
# ======================================================================


def test_the_first_call_takes_the_seat():
    """There is no separate joining step. Reading is claiming."""
    game, runner, tools = build(14)
    pid = seat_in(tools)
    assert tools.presence(tools.open_seats[pid].seat)["claimed"] is False
    tools.read_state(pid)
    assert tools.presence(tools.open_seats[pid].seat)["claimed"] is True


def test_player_ids_are_unguessable_and_distinct():
    game, runner, tools = build(14, pullers=2, bots=3)
    ids = [s["player_id"] for s in tools.summary()["open_seats"]]
    assert len(set(ids)) == 2
    for pid in ids:
        assert pid.startswith("pl_") and len(pid) > 12


def test_an_unknown_player_id_is_refused():
    game, runner, tools = build(15)
    with pytest.raises(AccessDenied):
        tools.read_state("pl_not_a_real_player")


def test_one_call_both_reads_and_acts():
    """The whole agent loop is a single request shape."""
    game, runner, tools = build(17)
    runner.start()
    pid = seat_in(tools)

    ack, answer = None, None
    for _ in range(200):
        state = tools.play(pid, ack, answer)
        ack, answer = state["ack_through"], None
        if state["table"]["status"] != "running":
            assert state["outcome"]["winner"] in {"good", "evil"}
            return
        if state["your_turn"]:
            answer = first_legal(state)
    raise AssertionError("the match never finished")


def test_an_answer_sent_when_nothing_is_owed_is_reported_not_applied():
    game, runner, tools = build(18)
    runner.start()
    pid = seat_in(tools)

    state = tools.play(pid, None, None)
    if state["your_turn"]:
        pytest.skip("this seat happened to be first")
    state = tools.play(pid, None, 0)
    assert state["action_result"]["accepted"] is False
