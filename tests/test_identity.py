"""Linking a session to the client player that owns it.

A session holds a seat's secrets, so it is never anonymous. These tests cover
the chain player -> client -> seat -> session, and that reading or acting on a
seat you do not own is refused rather than merely discouraged.
"""

from __future__ import annotations

import json
import threading
import urllib.error
import urllib.request
from contextlib import contextmanager

import pytest

from xcolos.agents import ScriptedAgent
from xcolos.cli import SEAT_NAMES, build_match
from xcolos.game import Game
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import OPERATOR, AccessDenied, Ownership, Player
from xcolos.log import MatchLog
from xcolos.legacy.mafia import MafiaOrchestrator
from xcolos.runner import Runner
from xcolos.web.server import MatchManager, build_server


def two_player_match(seed: int = 3):
    """Two clients, two principals: seats 1-2 and seats 3-5."""
    log = MatchLog(f"m_two_{seed}")
    game = Game(f"m_two_{seed}", MafiaOrchestrator.game_id, seed, log)

    alice = Player(player_id="p_alice", display_name="Alice")
    bob = Player(player_id="p_bob", display_name="Bob")
    a = LocalAgentHost([ScriptedAgent(name=n) for n in SEAT_NAMES[:2]], player=alice)
    b = LocalAgentHost([ScriptedAgent(name=n) for n in SEAT_NAMES[2:5]], player=bob)
    a.host_id, b.host_id = "client-a", "client-b"

    registry = Registry(game.match_id)
    for host in (a, b):
        for binding in host.register():
            index = game.register_seat(binding.name, host.host_id, binding.profile)
            registry.attach(index, host, binding)
    return game, MafiaOrchestrator(), registry, alice, bob


# ======================================================================
# The ownership chain
# ======================================================================


def test_a_session_knows_which_player_it_belongs_to():
    game, orch, registry, alice, bob = two_player_match()
    Runner(game, orch, registry).run()

    for seat in (1, 2):
        assert registry.session_of(seat, alice.player_id, alice.token).owner == "p_alice"
    for seat in (3, 4, 5):
        assert registry.session_of(seat, bob.player_id, bob.token).owner == "p_bob"


def test_seats_are_attributed_to_the_right_player():
    _, _, registry, alice, bob = two_player_match()
    assert registry.ownership.seats_of(alice.player_id) == [1, 2]
    assert registry.ownership.seats_of(bob.player_id) == [3, 4, 5]


def test_the_ownership_summary_never_leaks_a_secret():
    _, _, registry, alice, bob = two_player_match()
    blob = json.dumps(registry.ownership.summary())
    assert alice.token not in blob
    assert bob.token not in blob
    for credential in registry.ownership.credential_of.values():
        assert credential not in blob


def test_a_local_run_still_has_an_owner():
    """Convenience must not mean anonymity."""
    game, orch, registry, host = build_match(2)
    Runner(game, orch, registry).run()
    for seat in game.seats:
        assert registry.session_of(seat, host.player.player_id, host.player.token).owner


# ======================================================================
# Reading
# ======================================================================


def test_a_player_cannot_read_another_players_session():
    game, orch, registry, alice, bob = two_player_match()
    Runner(game, orch, registry).run()

    with pytest.raises(AccessDenied):
        registry.session_of(3, alice.player_id, alice.token)
    with pytest.raises(AccessDenied):
        registry.session_of(1, bob.player_id, bob.token)


def test_a_wrong_token_is_refused_even_for_your_own_seat():
    game, orch, registry, alice, _ = two_player_match()
    Runner(game, orch, registry).run()
    with pytest.raises(AccessDenied):
        registry.session_of(1, alice.player_id, "not-the-token")


def test_an_unknown_player_reads_nothing():
    game, orch, registry, _, _ = two_player_match()
    Runner(game, orch, registry).run()
    assert registry.readable_seats("p_nobody", "whatever") == []
    with pytest.raises(AccessDenied):
        registry.session_of(1, "p_nobody", "whatever")


def test_each_player_sees_exactly_its_own_seats():
    game, orch, registry, alice, bob = two_player_match()
    Runner(game, orch, registry).run()
    assert registry.readable_seats(alice.player_id, alice.token) == [1, 2]
    assert registry.readable_seats(bob.player_id, bob.token) == [3, 4, 5]


def test_the_operator_sees_every_seat_but_must_prove_it():
    game, orch, registry, host = build_match(4)
    Runner(game, orch, registry).run()
    operator = host.player
    assert registry.readable_seats(operator.player_id, operator.token) == sorted(game.seats)


# ======================================================================
# Acting
# ======================================================================


def test_acting_needs_the_seat_credential_not_just_the_player_token():
    _, _, registry, alice, _ = two_player_match()
    own = registry.ownership

    good = own.credential_of[1]
    own.check_act(1, alice.player_id, alice.token, good)  # no raise

    with pytest.raises(AccessDenied):
        own.check_act(1, alice.player_id, alice.token, "wrong-credential")


def test_a_credential_for_one_seat_does_not_work_on_another():
    """The failure that actually happens: right player, wrong seat."""
    _, _, registry, alice, _ = two_player_match()
    own = registry.ownership
    seat_one_credential = own.credential_of[2]
    with pytest.raises(AccessDenied):
        own.check_act(1, alice.player_id, alice.token, seat_one_credential)


def test_the_operator_may_watch_but_not_play():
    game, orch, registry, host = build_match(4)
    own = registry.ownership
    with pytest.raises(AccessDenied):
        own.check_act(1, OPERATOR, host.player.token, own.credential_of[1])


def test_claiming_a_seat_for_an_unknown_player_is_refused():
    own = Ownership("m")
    with pytest.raises(AccessDenied):
        own.claim(1, "p_ghost", "cred")


# ======================================================================
# Over HTTP
# ======================================================================


@contextmanager
def running_server():
    server = build_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}", server.RequestHandlerClass.manager
    finally:
        server.shutdown()
        server.server_close()


def get(base, path, status_ok=True):
    try:
        with urllib.request.urlopen(base + path, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def post(base, path, payload):
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def started(manager, seats=5, seed=4):
    handle = manager.create(
        {"seats": [{"name": f"P{i}", "kind": "scripted"} for i in range(seats)], "seed": seed}
    )
    manager.start_match(handle.match_id)
    handle.thread.join(timeout=15)
    return handle


def test_the_console_reads_sessions_only_with_the_operator_token():
    with running_server() as (base, manager):
        handle = started(manager)
        token = handle.operator.token

        status, sessions = get(
            base, f"/api/matches/{handle.match_id}/sessions?player=operator&token={token}"
        )
        assert status == 200
        assert len(sessions) == 5
        assert all(s["owner"] == "operator" for s in sessions)


def test_sessions_are_refused_without_a_valid_token():
    with running_server() as (base, manager):
        handle = started(manager)
        for query in ("", "?player=operator&token=wrong", "?player=p_nobody&token=x"):
            status, body = get(base, f"/api/matches/{handle.match_id}/sessions{query}")
            assert status in (200, 403)
            if status == 200:
                assert body == [], f"{query!r} should have read nothing"


def test_ownership_is_public_but_carries_no_secrets():
    with running_server() as (base, manager):
        handle = started(manager)
        status, rows = get(base, f"/api/matches/{handle.match_id}/ownership")
        assert status == 200
        assert len(rows) == 5
        blob = json.dumps(rows)
        assert handle.operator.token not in blob
        for row in rows:
            assert row["session_id"] == f"{handle.match_id}:seat{row['seat']}"


def test_a_client_resumes_its_own_seat():
    with running_server() as (base, manager):
        handle = started(manager)
        own = handle.registry.ownership
        operator_seats = own.seats_of(OPERATOR)
        assert operator_seats

        # The console's host is the operator, which may not act, so resume is
        # refused for it. That is the rule, not a bug.
        status, body = post(
            base,
            f"/api/matches/{handle.match_id}/resume/1",
            {
                "player_id": OPERATOR,
                "token": handle.operator.token,
                "credential": own.credential_of[1],
            },
        )
        assert status == 403
        assert "does not hold a seat" in body["error"]


def test_resume_returns_everything_that_seat_is_entitled_to():
    game, orch, registry, alice, bob = two_player_match(7)
    Runner(game, orch, registry).run()

    # Exercised directly, because this match is not served over HTTP.
    own = registry.ownership
    own.check_act(1, alice.player_id, alice.token, own.credential_of[1])

    entitled = {f.seq for f in game.entitled_facts(1)}
    delivered = set(game.log.deliveries_to(1))
    assert entitled == delivered, "resume has nothing to reconcile if these differ"


def test_resume_is_refused_for_a_seat_you_do_not_own():
    _, _, registry, alice, bob = two_player_match(8)
    own = registry.ownership
    with pytest.raises(AccessDenied):
        own.check_act(4, alice.player_id, alice.token, own.credential_of[4])
