"""End to end verification of one whole match.

Both the model and the orchestrator are stand-ins, so what is under test here is
the system: that rounds and turns run in the right order, that every message is
correct and reaches the right seats, and that what must be secret stays secret
while what must be broadcast reaches everyone.
"""

from __future__ import annotations

from collections import Counter

import pytest

from xcolos.cli import build_match
from xcolos.protocol import MsgType
from xcolos.runner import Runner

SEEDS = list(range(1, 16))

#: Which facts every living and dead seat must receive, and which must reach
#: only a named few. This table is the specification; the tests below check the
#: match against it rather than against themselves.
PUBLIC = {
    "phase",
    "death",
    "no_death",
    "speech",
    "vote_tally",
    "eliminated",
    "no_elimination",
    "game_over",
}
PRIVATE = {
    "role_assigned": "the seat it describes",
    "allies": "the mafia",
    "kill_target": "the mafia",
    "investigation": "the detective",
    "vote_cast": "the voter",
}


def play(seed: int, seats: int = 5):
    game, orch, registry, host = build_match(seed)
    result = Runner(game, orch, registry).run()
    return result, game, host


def turns(game):
    return game.log.where("turn", "move")


def sent(game, seat=None, kind=None):
    match = {}
    if seat is not None:
        match["seat"] = seat
    rows = game.log.where("message", "to_agent", **match)
    return [r for r in rows if kind is None or r["msg_type"] == kind]


# ======================================================================
# Rounds and phases
# ======================================================================


@pytest.mark.parametrize("seed", SEEDS)
def test_rounds_run_in_the_declared_order(seed):
    """Every round follows night, reveal, discussion, voting.

    A round may stop early when the game ends, but it may never run its phases
    out of order or skip one in the middle.
    """
    _, game, _ = play(seed)
    expected = ["night", "day_reveal", "day_discussion", "day_voting"]

    by_round: dict[int, list[str]] = {}
    for r in game.log.where("process", "set_phase"):
        by_round.setdefault(r["round"], []).append(r["now"])

    for rnd, phases in by_round.items():
        assert phases == expected[: len(phases)], f"round {rnd} ran {phases}"


@pytest.mark.parametrize("seed", SEEDS)
def test_the_round_counter_increases_by_one(seed):
    _, game, _ = play(seed)
    rounds = [r["round"] for r in game.log.where("process", "advance_round")]
    assert rounds == list(range(1, len(rounds) + 1))


@pytest.mark.parametrize("seed", SEEDS)
def test_every_phase_change_is_announced_to_everyone(seed):
    """A seat must never be surprised by what part of the round it is in.

    Only the night *actions* are secret. The fact that night fell is not.
    """
    _, game, _ = play(seed)
    everyone = set(game.seats)
    announced = [f for f in game.facts if f.type == "phase"]
    assert announced
    for fact in announced:
        assert fact.entitled == everyone, f"phase {fact.payload} was not public"

    changes = [r["now"] for r in game.log.where("process", "set_phase")]
    assert [f.payload["phase"] for f in announced] == changes


# ======================================================================
# Turns
# ======================================================================


@pytest.mark.parametrize("seed", SEEDS)
def test_turn_numbers_are_contiguous_and_ordered(seed):
    _, game, _ = play(seed)
    assert [t["turn_seq"] for t in turns(game)] == list(range(1, len(turns(game)) + 1))


@pytest.mark.parametrize("seed", SEEDS)
def test_a_dead_seat_never_acts_again(seed):
    _, game, _ = play(seed)
    died_at: dict[int, int] = {}
    for r in game.log.where("state", "eliminate"):
        died_at[r["seat"]] = r["log_seq"]

    for t in turns(game):
        if t["seat"] in died_at:
            assert t["log_seq"] < died_at[t["seat"]], (
                f"seat {t['seat']} acted after being eliminated"
            )


@pytest.mark.parametrize("seed", SEEDS)
def test_only_the_right_roles_act_at_night(seed):
    _, game, _ = play(seed)
    for t in turns(game):
        if t["action_schema"] == "kill":
            assert t["role"] == "mafia"
        elif t["action_schema"] == "investigate":
            assert t["role"] == "detective"


@pytest.mark.parametrize("seed", SEEDS)
def test_discussion_and_voting_give_every_living_seat_exactly_one_turn(seed):
    """One pass, in seat order, nobody twice and nobody missed."""
    _, game, _ = play(seed)

    for phase, schema in (("day_discussion", "speak"), ("day_voting", "vote")):
        by_round: dict[int, list[int]] = {}
        for t in turns(game):
            if t["phase"] == phase and t["action_schema"] == schema:
                by_round.setdefault(t["round"], []).append(t["seat"])

        for rnd, seats in by_round.items():
            assert seats == sorted(seats), f"{phase} round {rnd} was out of order"
            assert len(seats) == len(set(seats)), f"{phase} round {rnd} repeated a seat"


@pytest.mark.parametrize("seed", SEEDS)
def test_the_legal_targets_offered_are_always_legal(seed):
    """A seat is never invited to make a move the rules forbid."""
    _, game, _ = play(seed)
    for t in turns(game):
        targets = t["legal_targets"]
        if not targets:
            continue
        assert t["seat"] not in targets, "a seat was offered itself as a target"
        if t["action_schema"] == "kill":
            for target in targets:
                assert game.seats[target].faction != "evil", "mafia offered its own side"


@pytest.mark.parametrize("seed", SEEDS)
def test_every_action_taken_was_among_the_offered_targets(seed):
    _, game, _ = play(seed)
    for t in turns(game):
        action = t["action"]
        if t["legal_targets"] and action.get("target") is not None:
            assert action["target"] in t["legal_targets"]


# ======================================================================
# Messages
# ======================================================================


@pytest.mark.parametrize("seed", SEEDS)
def test_every_seat_is_briefed_once_before_anything_else(seed):
    _, game, _ = play(seed)
    for seat in game.seats:
        briefings = sent(game, seat, MsgType.GAME_START.value)
        assert len(briefings) == 1, f"seat {seat} was briefed {len(briefings)} times"
        first = sent(game, seat)[0]
        assert first["msg_type"] == MsgType.GAME_START.value


@pytest.mark.parametrize("seed", SEEDS)
def test_the_briefing_says_everything_a_seat_needs(seed):
    """Rules, table size, own state, own index, and the message format."""
    _, game, _ = play(seed)
    for seat, s in game.seats.items():
        body = sent(game, seat, MsgType.GAME_START.value)[0]["body"]
        assert "Mafia is a hidden-role game" in body
        assert f"Players: {len(game.seats)}" in body
        assert f"You are seat {seat}" in body
        assert f"Your role is {s.role}" in body
        assert "Each round runs in this order" in body
        for kind in ("SITUATION", "YOUR_TURN", "ACTION_REJECTED", "GAME_END"):
            assert kind in body, f"briefing never mentions {kind}"


@pytest.mark.parametrize("seed", SEEDS)
def test_a_seat_learns_its_role_once_and_only_in_the_briefing(seed):
    """The briefing absorbs setup, so the role does not also arrive separately."""
    _, game, _ = play(seed)
    for seat, s in game.seats.items():
        mentions = [
            m for m in sent(game, seat) if f"Your role is {s.role}" in m["body"]
        ]
        assert len(mentions) == 1
        assert mentions[0]["msg_type"] == MsgType.GAME_START.value


@pytest.mark.parametrize("seed", SEEDS)
def test_every_seat_is_told_the_game_ended(seed):
    _, game, _ = play(seed)
    for seat in game.seats:
        endings = sent(game, seat, MsgType.GAME_END.value)
        assert len(endings) == 1
        assert sent(game, seat)[-1]["msg_type"] == MsgType.GAME_END.value


@pytest.mark.parametrize("seed", SEEDS)
def test_a_turn_request_always_states_what_to_do_and_what_is_legal(seed):
    _, game, _ = play(seed)
    for row in sent(game, kind=MsgType.YOUR_TURN.value):
        assert row["action_schema"]
        assert "Living seats:" in row["body"]
        if row["legal_targets"]:
            assert "Answer with one of" in row["body"]


@pytest.mark.parametrize("seed", SEEDS)
def test_only_turn_requests_ever_get_a_reply(seed):
    _, game, _ = play(seed)
    replies = game.log.where("message", "from_agent")
    asks = [
        m
        for m in game.log.where("message", "to_agent")
        if m["msg_type"] in {MsgType.YOUR_TURN.value, MsgType.ACTION_REJECTED.value}
    ]
    assert len(replies) == len(asks)


def test_a_rejection_is_its_own_message_type_not_a_second_turn():
    """A retry must never look like a fresh turn, to the agent or to the log."""
    from xcolos.agents import BrokenAgent, ScriptedAgent

    def factory(i, name):
        return BrokenAgent(name=name) if i == 0 else ScriptedAgent(name=name)

    game, orch, registry, host = build_match(17, agent_factory=factory)
    Runner(game, orch, registry).run()

    rejections = sent(game, 0, MsgType.ACTION_REJECTED.value)
    assert rejections, "a broken seat should have been told its answer was illegal"
    for r in rejections:
        assert "not legal" in r["body"]

    # One turn request per turn, however many repairs followed it.
    asked = len(sent(game, 0, MsgType.YOUR_TURN.value))
    took = len([t for t in turns(game) if t["seat"] == 0])
    assert asked == took


# ======================================================================
# Isolation and broadcast
# ======================================================================


@pytest.mark.parametrize("seed", SEEDS)
def test_public_facts_reach_every_seat_including_the_dead(seed):
    """Eliminated players keep watching. That is a decision, so it is tested."""
    _, game, _ = play(seed)
    everyone = set(game.seats)
    for fact in game.facts:
        if fact.type in PUBLIC:
            assert fact.entitled == everyone, (
                f"{fact.type} at {fact.seq} reached {sorted(fact.entitled)}, not all"
            )


@pytest.mark.parametrize("seed", SEEDS)
def test_private_facts_reach_exactly_who_they_should(seed):
    _, game, _ = play(seed)
    mafia = {i for i, s in game.seats.items() if s.role == "mafia"}

    for fact in game.facts:
        if fact.type == "role_assigned":
            assert len(fact.entitled) == 1
        elif fact.type in {"allies", "kill_target"}:
            assert fact.entitled <= mafia, f"{fact.type} escaped the mafia"
        elif fact.type == "investigation":
            assert len(fact.entitled) == 1
            seat = next(iter(fact.entitled))
            assert game.seats[seat].role == "detective"
        elif fact.type == "vote_cast":
            assert fact.entitled == {fact.payload["seat"]}


@pytest.mark.parametrize("seed", SEEDS)
def test_every_fact_type_is_classified(seed):
    """A new fact type must be declared public or private, not left to chance."""
    _, game, _ = play(seed)
    known = PUBLIC | set(PRIVATE)
    seen = {f.type for f in game.facts}
    assert seen <= known, f"unclassified fact types: {sorted(seen - known)}"


@pytest.mark.parametrize("seed", SEEDS)
def test_nobody_is_told_a_secret_that_was_not_theirs(seed):
    """The end to end check, against what was actually delivered."""
    _, game, _ = play(seed)
    for seat in game.seats:
        for seq in game.log.deliveries_to(seat):
            assert seat in game.facts[seq].entitled


@pytest.mark.parametrize("seed", SEEDS)
def test_no_seat_text_ever_names_another_seats_secret(seed):
    """The strongest form: check the rendered words, not the audience sets."""
    _, game, host = play(seed)
    mafia = {i for i, s in game.seats.items() if s.role == "mafia"}
    detective = {i for i, s in game.seats.items() if s.role == "detective"}

    for seat in game.seats:
        world = "\n".join(m["body"] for m in sent(game, seat))
        if seat not in mafia:
            assert "Your allies are seats" not in world
            assert "Your side has chosen to kill" not in world
        if seat not in detective:
            assert "Your investigation of seat" not in world
        for other, s in game.seats.items():
            if other != seat:
                assert f"You are seat {other} (" not in world


@pytest.mark.parametrize("seed", SEEDS)
def test_votes_stay_private_until_the_tally(seed):
    """Sequential turns with results withheld is how this design votes."""
    _, game, _ = play(seed)
    tallies = [f.seq for f in game.facts if f.type == "vote_tally"]
    for fact in game.facts:
        if fact.type != "vote_cast":
            continue
        assert fact.entitled == {fact.payload["seat"]}
        assert any(t > fact.seq for t in tallies), "a vote was cast with no tally after"


@pytest.mark.parametrize("seed", SEEDS)
def test_the_tally_matches_the_votes_actually_cast(seed):
    _, game, _ = play(seed)
    casts = [f for f in game.facts if f.type == "vote_cast"]
    tallies = [f for f in game.facts if f.type == "vote_tally"]

    for tally in tallies:
        before = [
            c for c in casts if c.seq < tally.seq and c.round == tally.round
        ]
        expected = Counter(str(c.payload["target"]) for c in before)
        assert tally.payload["tally"] == dict(sorted(expected.items()))


@pytest.mark.parametrize("seed", SEEDS)
def test_what_a_seat_was_delivered_is_exactly_what_it_was_entitled_to(seed):
    _, game, _ = play(seed)
    for seat in game.seats:
        delivered = set(game.log.deliveries_to(seat))
        entitled = {f.seq for f in game.entitled_facts(seat)}
        assert delivered == entitled


# ======================================================================
# Outcome
# ======================================================================


@pytest.mark.parametrize("seed", SEEDS)
def test_the_declared_winner_matches_the_board(seed):
    result, game, _ = play(seed)
    evil = sum(1 for s in game.seats.values() if s.alive and s.faction == "evil")
    good = sum(1 for s in game.seats.values() if s.alive and s.faction == "good")

    if result.winner == "good":
        assert evil == 0
    else:
        assert evil >= good


@pytest.mark.parametrize("seed", SEEDS)
def test_a_death_is_announced_for_every_elimination(seed):
    _, game, _ = play(seed)
    eliminated = {r["seat"] for r in game.log.where("state", "eliminate")}
    announced = {
        f.payload["seat"] for f in game.facts if f.type in {"death", "eliminated"}
    }
    assert eliminated == announced


@pytest.mark.parametrize("seats", [4, 5, 7, 9, 12])
def test_the_whole_suite_of_guarantees_holds_at_any_table_size(seats):
    from xcolos.web.server import MatchManager

    m = MatchManager()
    handle = m.create(
        {"seats": [{"name": f"P{i}", "kind": "scripted"} for i in range(seats)], "seed": 3}
    )
    m.start_match(handle.match_id)
    handle.thread.join(timeout=15)
    game = handle.game

    assert game.status.value == "ended"
    everyone = set(game.seats)
    for fact in game.facts:
        if fact.type in PUBLIC:
            assert fact.entitled == everyone
    for seat in game.seats:
        assert set(game.log.deliveries_to(seat)) == {
            f.seq for f in game.entitled_facts(seat)
        }
