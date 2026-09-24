"""The client and server split.

Agents live on the client. State, decisions, sequence numbers and the log live
on the server. The boundary is the agent host interface, and these tests assert
that the server keeps working when a client misbehaves or disappears.
"""

from __future__ import annotations

import pytest

from xcolos.agents import ScriptedAgent
from xcolos.cli import SEATS, build_match
from xcolos.host import HostUnavailable, LocalAgentHost, Registry, SeatBinding
from xcolos.runner import Runner
from xcolos.state import FIRST_SEAT


# ----------------------------------------------------------------------
# Registration
# ----------------------------------------------------------------------


def test_the_server_assigns_indices_not_the_client():
    game, _, registry, host = build_match(1)
    assert registry.seats() == list(range(FIRST_SEAT, FIRST_SEAT + SEATS))
    assert sorted(game.seats) == list(range(FIRST_SEAT, FIRST_SEAT + SEATS))
    # The client learned the indices it was given; it never chose them.
    for i in registry.seats():
        assert host.connected(i)


def test_registration_is_recorded_with_the_host():
    game, _, _, host = build_match(1)
    rows = game.log.where("setup", "register_seat")
    assert len(rows) == SEATS
    for r in rows:
        assert r["host"] == host.host_id
        assert r["profile"]["kind"] == "ScriptedAgent"


def test_a_credential_authorises_only_its_own_seat():
    _, _, registry, _ = build_match(1)
    good = registry.binding_of[2].credential
    assert registry.authorises(2, good)
    assert not registry.authorises(3, good)
    assert not registry.authorises(2, "not-the-credential")


def test_a_host_cannot_answer_for_a_seat_it_does_not_own():
    from xcolos.protocol import Envelope, MsgType

    host = LocalAgentHost([ScriptedAgent(name="only-one")])
    registry = Registry("m")
    binding = host.register()[0]
    registry.attach(0, host, binding)

    with pytest.raises(HostUnavailable):
        host.deliver(
            Envelope(type=MsgType.SITUATION, match_id="m", seat=9, body="hello")
        )


# ----------------------------------------------------------------------
# Multiple hosts
# ----------------------------------------------------------------------


def make_split_match(seed: int):
    """Two clients, as in an online match: seats 0-1 on one, 2-4 on the other."""
    from xcolos.cli import SEAT_NAMES
    from xcolos.game import Game
    from xcolos.log import MatchLog
    from xcolos.legacy.mafia import MafiaOrchestrator

    log = MatchLog(f"m_split_{seed}")
    game = Game(f"m_split_{seed}", MafiaOrchestrator.game_id, seed, log)

    a = LocalAgentHost([ScriptedAgent(name=n) for n in SEAT_NAMES[:2]])
    b = LocalAgentHost([ScriptedAgent(name=n) for n in SEAT_NAMES[2:5]])
    a.host_id, b.host_id = "client-a", "client-b"

    registry = Registry(game.match_id)
    for host in (a, b):
        for binding in host.register():
            index = game.register_seat(binding.name, host.host_id, binding.profile)
            registry.attach(index, host, binding)
    return game, MafiaOrchestrator(), registry, (a, b)


@pytest.mark.parametrize("seed", range(1, 11))
def test_a_match_plays_identically_across_two_clients(seed):
    """Where a seat is hosted must not change the game.

    The server assigns every sequence number and drives every turn, so the
    outcome depends on the seed, not on the topology.
    """
    game_a, orch_a, reg_a, _ = make_split_match(seed)
    split = Runner(game_a, orch_a, reg_a).run()

    game_b, orch_b, reg_b, _ = build_match(seed)
    single = Runner(game_b, orch_b, reg_b).run()

    assert (split.winner, split.turns, split.rounds) == (
        single.winner,
        single.turns,
        single.rounds,
    )


def test_each_seat_is_routed_to_its_own_host():
    game, orch, registry, (a, b) = make_split_match(3)
    Runner(game, orch, registry).run()
    assert [registry.host_of[i].host_id for i in range(1, 6)] == [
        "client-a",
        "client-a",
        "client-b",
        "client-b",
        "client-b",
    ]


# ----------------------------------------------------------------------
# Disconnection
# ----------------------------------------------------------------------


def test_a_dropped_client_does_not_stall_the_match():
    """An unreachable client is not a special case.

    It looks like a seat that did not answer, which the failure ladder already
    handles, so the match finishes and the turn is marked degraded.
    """
    game, orch, registry, host = build_match(6)
    host.drop(2)
    result = Runner(game, orch, registry).run()

    assert result.status in {"ended", "abandoned"}
    unreachable = game.log.where("message", "host_unavailable")
    assert unreachable
    assert {r["seat"] for r in unreachable} == {2}


def test_dropping_every_client_still_terminates():
    game, orch, registry, host = build_match(6)
    for i in registry.seats():
        host.drop(i)
    result = Runner(game, orch, registry).run()
    assert result.status in {"ended", "abandoned"}


def test_a_reconnecting_seat_receives_what_it_missed():
    """Delivery is eager push, so a dropped client misses pushes.

    The server already tracks how far delivery reached per seat, which is
    exactly the cursor a resume needs.
    """
    game, orch, registry, host = build_match(4)

    host.drop(3)
    result = Runner(game, orch, registry).run()
    assert result.status in {"ended", "abandoned"}

    # Everything seat 3 was entitled to was still marked delivered, because the
    # server, not the client, owns the delivery cursor.
    delivered = set(game.log.deliveries_to(4))
    entitled = {f.seq for f in game.entitled_facts(4)}
    assert delivered == entitled


def test_the_server_logs_every_attempt_to_reach_a_dead_client():
    game, orch, registry, host = build_match(6)
    host.drop(1)
    Runner(game, orch, registry).run()

    to_agent = game.log.where("message", "to_agent", seat=1)
    failures = game.log.where("message", "host_unavailable", seat=1)
    # Every message aimed at the dropped seat is recorded as attempted and as
    # having failed, so the log explains the silence.
    assert len(failures) == len(to_agent)


# ----------------------------------------------------------------------
# Trust
# ----------------------------------------------------------------------


def test_a_client_never_receives_another_clients_secrets():
    """The unit of entitlement is the seat.

    A host sees the union of its own seats' entitlements and nothing more, which
    is the rule that makes an online match safe.
    """
    game, orch, registry, (a, b) = make_split_match(5)
    Runner(game, orch, registry).run()

    a_seats, b_seats = {1, 2}, {3, 4, 5}
    for seat in b_seats:
        for seq in game.log.deliveries_to(seat):
            assert seat in game.facts[seq].entitled

    # Nothing entitled only to a seat on one client was ever delivered to the
    # other client's seats.
    for fact in game.facts:
        if fact.entitled and fact.entitled <= frozenset(a_seats):
            for seat in b_seats:
                assert fact.seq not in game.log.deliveries_to(seat)
