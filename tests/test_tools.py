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
from xcolos.legacy.mafia import MafiaOrchestrator
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
        if state["status"] != "running":
            return state, reads, token
        if state["your_turn"]:
            tools.post_action(token, decide(state))
    raise AssertionError("the match never finished")


def news(state):
    """Just the information messages. The action request is not news."""
    return [m for m in state.get("messages", []) if m["kind"] == "information"]


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
    assert state["status"] == "ended"
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
            if state["status"] != "running":
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
    assert state["you"]["role"], "the first read carries who you are"
    assert state["table"]["living_seats"]
    assert state["at"]["phase"]
    assert "briefing" in state, "the rules come with the first read"
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
    assert [f["seq"] for f in news(a)] == [f["seq"] for f in news(b)]

    c = tools.read_state(token, a["ack_through"])
    assert len(news(c)) < len(news(a))


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
        seen.extend(f["seq"] for f in news(state))
        if state["status"] != "running":
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
        state = tools.read_state(pid, full=True)
        me = state["you"]["seat"]

        assert state["you"]["role"] == truth[me], "a seat must know its own role"

        # Other seats are seat number, name and alive-or-not. Nothing else.
        for other in state["table"]["seats"]:
            assert set(other) == {"seat", "name", "status"}

        said = " ".join(f["text"] for f in news(state)).lower()
        for other, role in truth.items():
            if other == me:
                continue
            assert not (f"seat {other}" in said and role in said), (
                f"seat {me} was told seat {other} is a {role}"
            )


def test_a_seat_knows_how_many_players_there_are_and_their_names():
    game, runner, tools = build(32, pullers=2, bots=4)
    runner.start()
    pid = tools.summary()["open_seats"][0]["player_id"]

    state = tools.read_state(pid, full=True)
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
        for item in news(state):
            text = item["text"]
            if any(r in text for r in ("mafia", "detective", "villager")):
                fact = game.facts[item["seq"]]
                assert fact.type in {
                    "role_assigned", "allies", "death", "eliminated", "game_over",
                }, f"a role surfaced in an unexpected fact: {fact.type}"
        if state["status"] != "running":
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
        if state["status"] != "running":
            break
        if state["your_turn"]:
            time.sleep(0.4)  # think for too long
            tools.read_state(token, ack)  # any call notices the expiry
    assert game.log.where("message", "expired"), "no turn ever expired"
    assert game.status.value in {"ended", "abandoned"}


def test_a_quiet_read_says_nothing_and_says_it_cheaply():
    """Most polls at a one second cadence have no news. Those must be tiny.

    The agent keeps its own history, so repeating the role and the table on
    every poll would be pure waste.
    """
    import json

    # Two pulling seats, so one can read while the game waits on the other.
    # With a single puller the game always parks straight back on it and a
    # quiet moment never exists.
    game, runner, tools = build(13, pullers=2, bots=3)
    runner.start()
    a = tools.summary()["open_seats"][0]["player_id"]

    news = tools.read_state(a)
    assert news["new"] is True

    quiet = tools.read_state(a, news["ack_through"])
    assert quiet == {
        "new": False,
        "status": "running",
        "game": game.match_id,
        "check_back_in_seconds": tools.poll_seconds,
    }
    assert len(json.dumps(quiet)) < 120


def test_the_standing_state_is_not_resent_on_every_read():
    game, runner, tools = build(14)
    runner.start()
    pid = seat_in(tools)

    first = tools.read_state(pid)
    assert "you" in first and "table" in first and "briefing" in first

    later = tools.read_state(pid, first["ack_through"])
    assert "briefing" not in later
    assert "you" not in later or later.get("status") != "running"


def test_a_session_that_lost_the_thread_can_ask_for_everything():
    """The recovery path. Cheap to offer, and it removes a whole failure mode."""
    game, runner, tools = build(15)
    runner.start()
    pid = seat_in(tools)

    first = tools.read_state(pid)
    tools.read_state(pid, first["ack_through"])

    resync = tools.read_state(pid, None, full=True)
    assert resync["new"] is True
    assert resync["you"]["role"]
    assert resync["table"]["living_seats"]
    assert resync["at"]["phase"]


def test_the_advised_cadence_is_two_seconds_by_default():
    from xcolos.tools import DEFAULT_POLL_SECONDS

    assert DEFAULT_POLL_SECONDS == 2
    game, runner, tools = build(16)
    tools.poll_seconds = DEFAULT_POLL_SECONDS
    runner.start()
    pid = seat_in(tools)
    assert tools.read_state(pid)["check_back_in_seconds"] == 2


def test_a_turn_always_arrives_as_news():
    """A quiet read must never hide a turn that is owed."""
    game, runner, tools = build(17)
    runner.start()
    pid = seat_in(tools)

    ack, saw_turn = None, False
    for _ in range(200):
        state = tools.read_state(pid, ack)
        if state["new"]:
            ack = state.get("ack_through", ack)
            if state.get("your_turn"):
                saw_turn = True
                assert state["ask"]["legal_answers"] or state["ask"]["answer_with"] == "text"
                tools.post_action(pid, first_legal(state))
        if state["status"] != "running":
            break
    assert saw_turn, "the seat was never told it had a turn"


def test_acknowledging_is_receipt_not_an_answer():
    """An ack says "I got it". A turn still needs an answer.

    The two are separate on purpose. A seat can confirm it has read everything
    and still owe a move, and the game keeps waiting until the move arrives or
    the deadline passes.
    """
    game, runner, tools = build(9)
    runner.start()
    pid = seat_in(tools)

    state = tools.read_state(pid)
    assert state["your_turn"] is True
    seat = tools.open_seats[pid].seat
    owed = runner.parked_for(seat)

    ack = state["ack_through"]
    for _ in range(3):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        assert state["your_turn"] is True, "an ack must not clear a turn"
        assert runner.parked_for(seat) is owed, "the same turn is still parked"
        assert not news(state), "everything has been confirmed"

    answer = (
        state["ask"]["legal_answers"][0]
        if state["ask"]["legal_answers"]
        else "Something worth saying."
    )
    assert tools.post_action(pid, answer)["accepted"] is True
    assert runner.parked_for(seat) is not owed, "answering is what moves the game on"


def test_a_seat_that_only_acknowledges_is_eventually_defaulted():
    """Receipt without an answer is still silence, as far as the game cares."""
    import time

    game, runner, tools = build(10, deadline_ms=300)
    runner.start()
    pid = seat_in(tools)

    state = tools.read_state(pid)
    assert state["your_turn"] is True
    time.sleep(0.4)
    tools.read_state(pid, state["ack_through"])  # acknowledge, still no answer

    assert game.log.where("message", "expired"), "the turn should have run out"


def test_a_speech_is_capped_and_the_limit_is_stated_up_front():
    """An agent should learn the limit from the request, not from a refusal."""
    from xcolos.legacy.mafia import SPEECH_WORD_LIMIT

    game, runner, tools = build(26)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(60):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if not state.get("your_turn"):
            continue
        ask = state["ask"]
        if ask["answer_with"] != "text":
            tools.post_action(pid, first_legal(state))
            continue

        assert ask["max_words"] == SPEECH_WORD_LIMIT
        assert str(SPEECH_WORD_LIMIT) in ask["prompt"]

        long = " ".join(["padding"] * (SPEECH_WORD_LIMIT + 40))
        out = tools.post_action(pid, {"kind": "action", "action": "speak",
                                      "response": long})
        assert out["accepted"] is False
        assert "words" in out["reason"]
        assert "`reason`" in out["reason"], "the refusal should say where to put it"

        again = tools.read_state(pid, ack)
        assert again["your_turn"], "a refusal leaves the turn open"
        assert tools.post_action(
            pid, {"kind": "action", "action": "speak", "response": "Seat 1 is off."}
        )["accepted"] is True
        return
    raise AssertionError("never asked to speak")


def test_a_long_reason_is_not_capped():
    """Only the table pays for speech. Thinking is between an agent and the log."""
    game, runner, tools = build(27)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(60):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if state.get("your_turn") and state["ask"]["answer_with"] == "text":
            out = tools.post_action(pid, {
                "kind": "action", "action": "speak",
                "response": "Short and to the point.",
                "reason": " ".join(["thinking"] * 400),
            })
            assert out["accepted"] is True
            return
        if state.get("your_turn"):
            tools.post_action(pid, first_legal(state))
    raise AssertionError("never asked to speak")


def test_the_limit_is_a_setting_not_a_rule():
    from xcolos.legacy.mafia import MafiaOrchestrator

    assert MafiaOrchestrator(speech_word_limit=40).speak.max_words == 40
    assert MafiaOrchestrator().speak.max_words == 100


# ======================================================================
# Simultaneous voting
# ======================================================================


def reach_vote(tools, runner, ids, acks, limit=80):
    """Play until the table is voting, and return the seats being asked."""
    for _ in range(limit):
        asked = [s for s in ids if runner.parked_for(s)]
        if tools.game.phase == "day_voting" and len(asked) > 1:
            return asked
        for s in ids:
            st = tools.play(ids[s], acks[s])
            acks[s] = st.get("ack_through", acks[s])
            if st.get("your_turn"):
                tools.post_action(ids[s], first_legal(st))
        if tools.game.status.value != "running":
            return []
    return []


def pulling_table(seed, pullers=3, bots=2):
    game, runner, tools = build(seed, pullers=pullers, bots=bots)
    runner.start()
    ids = {tools.open_seats[p["player_id"]].seat: p["player_id"]
           for p in tools.summary()["open_seats"]}
    return game, runner, tools, ids, {s: None for s in ids}


def test_a_vote_asks_every_living_seat_at_once():
    """No order to a vote, so asking seat by seat only makes everyone wait."""
    game, runner, tools, ids, acks = pulling_table(33)
    asked = reach_vote(tools, runner, ids, acks)
    assert len(asked) > 1, "voting should have several seats parked together"
    for seat in asked:
        state = tools.play(ids[seat], acks[seat])
        assert state["your_turn"] is True
        assert state["ask"]["action"] == "vote"


def test_the_last_answer_is_what_moves_the_vote_on():
    game, runner, tools, ids, acks = pulling_table(33)
    asked = reach_vote(tools, runner, ids, acks)
    assert len(asked) > 1

    before = game.round, game.phase
    for seat in asked[:-1]:
        tools.post_action(ids[seat], first_legal(tools.play(ids[seat])))
        assert (game.round, game.phase) == before, "the vote resolved too early"
    tools.post_action(ids[asked[-1]], first_legal(tools.play(ids[asked[-1]])))
    assert (game.round, game.phase) != before


def test_the_answer_order_does_not_change_the_result():
    """Whoever is quickest must not decide anything."""

    def run(reverse):
        game, runner, tools, ids, acks = pulling_table(33)
        asked = reach_vote(tools, runner, ids, acks)
        assert len(asked) > 1
        for seat in sorted(asked, reverse=reverse):
            tools.post_action(ids[seat], first_legal(tools.play(ids[seat])))
        casts = [f.payload for f in game.facts if f.type == "vote_cast"]
        tally = [f.payload for f in game.facts if f.type == "vote_tally"][-1]
        return casts, tally

    forwards, backwards = run(False), run(True)
    assert forwards == backwards


def test_votes_are_recorded_in_seat_order_whoever_answered_first():
    game, runner, tools, ids, acks = pulling_table(33)
    asked = reach_vote(tools, runner, ids, acks)
    for seat in sorted(asked, reverse=True):
        tools.post_action(ids[seat], first_legal(tools.play(ids[seat])))

    seats = [f.payload["seat"] for f in game.facts if f.type == "vote_cast"]
    assert seats == sorted(seats)


def test_a_seat_told_it_is_not_being_waited_on_is_named_who_is():
    """Needs two pulling seats: with one, "not your turn" cannot happen.

    `your_turn` is exactly "is there a turn parked on me", so a single puller
    can never see the game waiting on somebody else, and the old version of
    this test never reached its own assertion.
    """
    game, runner, tools, ids, acks = pulling_table(34, pullers=2, bots=3)

    for _ in range(80):
        parked = sorted(runner.parked)
        idle = [s for s in ids if s not in parked]
        if parked and idle:
            out = tools.post_action(ids[idle[0]], 0)
            assert out["accepted"] is False
            assert "nothing is owed from you" in out["reason"]
            return
        for s in ids:
            state = tools.play(ids[s], acks[s])
            acks[s] = state.get("ack_through", acks[s])
            if state.get("your_turn"):
                tools.post_action(ids[s], first_legal(state))
        if game.status.value != "running":
            break
    raise AssertionError("never reached a moment with one seat idle and one owed")


# ======================================================================
# A table's second game
# ======================================================================


def table_of(manager, seed=5, connectors=1):
    handle = manager.create({"seed": seed, "seats":
        [{"name": f"C{i}", "kind": "connector"} for i in range(connectors)] +
        [{"name": f"B{i}", "kind": "random"} for i in range(5 - connectors)]})
    pid = handle.tools.summary()["open_seats"][0]["player_id"]
    handle.tools.play(pid)
    return handle, pid


def finish(tools, pid, ack=None, limit=200):
    for _ in range(limit):
        state = tools.play(pid, ack)
        ack = state.get("ack_through", ack)
        if state["status"] != "running":
            return ack
        if state.get("your_turn"):
            a = state["ask"]
            tools.play(pid, ack, a["legal_answers"][0] if a["legal_answers"] else "Hm.")
    raise AssertionError("game did not finish")


def test_a_stale_acknowledgement_cannot_confirm_a_new_game():
    """The nastiest failure this design allows.

    Each game on a table has its own facts numbered from zero, and an agent
    polling across the boundary still carries the last number from before.
    Clamping that to the fact count would confirm the whole new game unseen,
    and the seat would be asked to act having never been told its role.
    """
    from xcolos.web.server import MatchManager

    m = MatchManager()
    handle, pid = table_of(m)
    m.start_match(handle.match_id)
    stale = finish(handle.tools, pid)
    assert stale is not None and stale > 0

    m.start_match(handle.match_id)
    state = handle.tools.play(pid, stale)  # still sending the old number

    assert "you" in state, "the seat was never told who it is"
    assert state["you"]["role"], "no role in a brand new game"
    assert "briefing" in state, "no rules in a brand new game"
    assert state["messages"], "the whole game was marked read"
    assert handle.game.seats[min(handle.game.seats)].acked_upto == 0


def test_every_response_says_which_game_it_belongs_to():
    """Including the ones sent before play begins, so there is no special case."""
    from xcolos.web.server import MatchManager

    m = MatchManager()
    handle, pid = table_of(m, seed=11)
    waiting = handle.tools.play(pid)
    assert waiting["status"] in {"waiting_for_players", "ready_to_start"}
    assert waiting["game"] == handle.game.match_id

    m.start_match(handle.match_id)
    assert handle.tools.play(pid)["game"] == handle.game.match_id


def test_the_response_says_which_game_it_belongs_to():
    from xcolos.web.server import MatchManager

    m = MatchManager()
    handle, pid = table_of(m, seed=6)
    m.start_match(handle.match_id)
    first = handle.tools.play(pid)["game"]
    finish(handle.tools, pid)

    m.start_match(handle.match_id)
    assert handle.tools.play(pid)["game"] != first


def test_a_remote_client_still_plays_a_tables_second_game():
    """A client that joined for game one is still connected for game two."""
    from xcolos.web.server import MatchManager

    m = MatchManager()
    handle = m.create({"seed": 7, "deadline_ms": 300, "seats":
        [{"name": "R", "kind": "remote"}] +
        [{"name": f"B{i}", "kind": "random"} for i in range(4)]})
    m.join(handle.match_id, "Alex", ["R"])
    # Nobody answers for the remote seat, so it is defaulted turn after turn
    # until the game resolves. That is enough to reach a second game.
    handle.thread.join(timeout=60)
    assert handle.game.status.value in {"ended", "abandoned"}

    m.start_match(handle.match_id)
    seat = min(handle.game.seats)
    assert seat in handle.registry.host_of, "the remote seat lost its host"
    assert handle.registry.ownership.owner_of.get(seat), "ownership was dropped"
    assert getattr(handle.registry.host_of[seat], "host_id", "").startswith("remote")


def test_a_late_answer_does_not_land_on_the_next_turn():
    """An expired speech must not be read for its digits and cast as a vote."""
    import time

    game, runner, tools = build(45, deadline_ms=250)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(60):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if state["status"] != "running":
            break
        if not state.get("your_turn"):
            continue
        if state["ask"]["answer_with"] != "text":
            tools.post_action(pid, first_legal(state))
            continue

        time.sleep(0.4)  # think past the deadline
        out = tools.post_action(pid, "I think seat 3 has been too quiet")
        assert out["accepted"] is False
        assert "expired" in out["reason"]

        votes = [f for f in game.facts if f.type == "vote_cast"]
        assert not any(v.payload["seat"] == tools.open_seats[pid].seat
                       and v.payload["target"] == 3 for v in votes), (
            "a speech was turned into a vote"
        )
        return


def test_a_null_field_does_not_defeat_the_others():
    """A model that fills every schema slot sends the unused ones as null."""
    from xcolos import messages
    from xcolos.protocol import ActionSchema

    speak = ActionSchema(id="speak", target="text")
    action = messages.parse_action(
        {"kind": "action", "action": "speak", "text": "hello there", "target": None},
        speak, ()
    )
    assert action is not None and action.text == "hello there"

    vote = ActionSchema(id="vote", target="seat")
    action = messages.parse_action(
        {"kind": "action", "action": "vote", "response": None, "target": 2},
        vote, (0, 1, 2)
    )
    assert action is not None and action.target == 2


# ======================================================================
# Message structure
# ======================================================================


def test_every_queue_item_declares_its_kind_and_whether_to_respond():
    """An agent should never infer what is expected of it."""
    game, runner, tools = build(21)
    runner.start()
    pid = seat_in(tools)

    state = tools.read_state(pid)
    assert state["messages"], "the queue was empty"
    for m in state["messages"]:
        assert m["kind"] in {"information", "action_required"}
        assert "respond" in m
        if m["kind"] == "information":
            assert m["respond"] is False
            assert {"seq", "type", "round", "phase", "text", "data"} <= set(m)
        else:
            assert m["respond"] is True
            assert {"action", "prompt", "answer_with", "legal_answers"} <= set(m)
            assert "seq" not in m, "a turn is not acknowledgeable"


def test_the_action_request_is_the_last_item_and_is_repeated_at_the_top():
    game, runner, tools = build(22)
    runner.start()
    pid = seat_in(tools)

    state = tools.read_state(pid)
    assert state["your_turn"] is True
    assert state["messages"][-1]["kind"] == "action_required"
    assert state["ask"] == state["messages"][-1]


def test_a_structured_reply_is_accepted():
    """The documented form: say what kind of reply it is."""
    from xcolos import messages

    game, runner, tools = build(23)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if not state.get("your_turn"):
            continue
        ask = state["ask"]
        if ask["answer_with"] == "seat":
            reply = {"kind": messages.ACTION, "action": ask["action"],
                     "target": ask["legal_answers"][0]}
        else:
            reply = {"kind": messages.ACTION, "action": ask["action"],
                     "text": "Something worth saying."}
        assert tools.post_action(pid, reply)["accepted"] is True
        return
    raise AssertionError("never asked to act")


def test_shorthand_and_structured_replies_mean_the_same_thing():
    from xcolos import messages
    from xcolos.protocol import ActionSchema

    vote = ActionSchema(id="vote", target="seat")
    legal = (0, 1, 2)
    structured = messages.parse_action(
        {"kind": "action", "action": "vote", "target": 2}, vote, legal
    )
    shorthand = messages.parse_action(2, vote, legal)
    assert structured == shorthand

    speak = ActionSchema(id="speak", target="text")
    a = messages.parse_action({"kind": "action", "action": "speak", "text": "hi"}, speak, ())
    b = messages.parse_action("hi", speak, ())
    assert a == b


def test_an_unreadable_reply_is_refused_with_a_reason():
    game, runner, tools = build(24)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if state.get("your_turn") and state["ask"]["answer_with"] == "seat":
            out = tools.post_action(pid, {"kind": "action"})
            assert out["accepted"] is False
            assert out["legal_answers"]
            return
        if state.get("your_turn"):
            tools.post_action(pid, first_legal(state))
    raise AssertionError("never asked for a targeted action")


def test_a_reply_carries_a_public_response_and_a_private_reason():
    game, runner, tools = build(25)
    runner.start()
    pid = seat_in(tools)

    ack = None
    for _ in range(50):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if not state.get("your_turn"):
            continue
        ask = state["ask"]
        response = (
            ask["legal_answers"][0] if ask["legal_answers"] else "Seat 1 is lying."
        )
        out = tools.post_action(
            pid,
            {"kind": "action", "action": ask["action"],
             "response": response, "reason": "PRIVATE-THINKING-MARKER"},
        )
        assert out["accepted"] is True

        # The last move overall belongs to whichever bot moved after us.
        seat = tools.open_seats[pid].seat
        mine = game.log.where("turn", "move", seat=seat)[-1]
        assert mine["action"]["reason"] == "PRIVATE-THINKING-MARKER"
        assert (mine["action"]["text"] or mine["action"]["target"]) == response
        return
    raise AssertionError("never asked to act")


@pytest.mark.parametrize("seed", range(25, 31))
def test_a_reason_never_reaches_another_seat(seed):
    """The whole point of the split. Thinking is logged, never shared.

    Checked against every fact in the game, not just the ones this seat can
    see, because a reason must not become a fact at all.
    """
    MARK = "PRIVATE-THINKING-MARKER"
    game, runner, tools = build(seed)
    runner.start()
    pid = seat_in(tools)

    ack, spoke = None, False
    for _ in range(200):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if state["status"] != "running":
            break
        if state.get("your_turn"):
            ask = state["ask"]
            response = (
                ask["legal_answers"][0] if ask["legal_answers"] else "A plain remark."
            )
            tools.post_action(
                pid,
                {"kind": "action", "action": ask["action"],
                 "response": response, "reason": MARK},
            )
            spoke = True

    assert spoke, "the seat never acted"
    for fact in game.facts:
        import json as _json

        assert MARK not in _json.dumps(fact.payload), (
            f"a private reason became fact {fact.seq} ({fact.type})"
        )


def test_an_acknowledgement_can_be_sent_structured():
    from xcolos import messages

    assert messages.read_ack({"reply": {"kind": "ack", "through": 14}}) == 14
    assert messages.read_ack({"ack": 14}) == 14
    assert messages.read_ack({"id": "x"}) is None


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
        if state["status"] != "running":
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
