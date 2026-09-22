"""A player's own process holding a seat.

This is how a real model gets into a seat: not by handing the server a key, but
by the player running a client that answers turns. These tests run an actual
client over actual HTTP on a loopback port, so the path exercised is the same
one a laptop on the other side of the world would take.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager

import pytest

from xcolos.agents import BaseAgent, RandomAgent, ScriptedAgent
from xcolos.client import ClientError, XColosClient
from xcolos.identity import OPERATOR
from xcolos.protocol import Action
from xcolos.web.server import build_server


@contextmanager
def server():
    httpd = build_server(port=0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        yield (
            f"http://127.0.0.1:{httpd.server_address[1]}",
            httpd.RequestHandlerClass.manager,
        )
    finally:
        httpd.shutdown()
        httpd.server_close()


def post(base, path, payload):
    req = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def table(local: int, remote: int):
    seats = [{"name": f"Bot{i}", "kind": "scripted"} for i in range(local)]
    seats += [{"name": f"Open{i}", "kind": "remote"} for i in range(remote)]
    return seats


class WatchfulAgent(BaseAgent):
    """A player's own agent. Records what it was told, answers legally.

    Stands in for whatever the player actually runs. The point is that the
    server never learns which this is.
    """

    def __init__(self, name: str = "mine", **kw):
        super().__init__(name, **kw)
        self.turns = 0
        self.saw_briefing = False

    def handle(self, env):
        if env.type.value == "GAME_START":
            self.saw_briefing = True
        return super().handle(env)

    def decide(self, env):
        self.turns += 1
        schema = env.schema
        if schema.target == "text":
            return Action(type=schema.id, text=f"{self.name} has nothing to add.")
        if env.legal_targets:
            return Action(type=schema.id, target=env.legal_targets[-1])
        return Action(type=schema.id)


# ======================================================================
# Waiting for players
# ======================================================================


def test_a_match_with_a_remote_seat_waits_before_starting():
    with server() as (base, manager):
        handle = manager.create({"seed": 2, "seats": table(4, 1)})
        assert handle.waiting
        assert handle.thread is None
        assert [s["name"] for s in handle.open_seats] == ["Open0"]


def test_a_table_of_bots_is_ready_but_still_waits_to_be_started():
    """Nothing runs itself. Whoever set the table decides when play begins."""
    with server() as (base, manager):
        handle = manager.create({"seed": 2, "seats": table(5, 0)})
        assert not handle.waiting
        assert handle.ready and not handle.started
        assert handle.thread is None

        manager.start_match(handle.match_id)
        assert handle.started and handle.thread is not None


def test_joining_the_last_open_seat_starts_the_match():
    with server() as (base, manager):
        handle = manager.create({"seed": 3, "seats": table(4, 1)})
        status, body = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Alex", "seats": ["mine"]},
        )
        assert status == 200
        assert body["started"] is True
        assert not handle.waiting
        assert handle.thread is not None


def test_a_player_cannot_claim_more_seats_than_are_open():
    with server() as (base, manager):
        handle = manager.create({"seed": 3, "seats": table(4, 1)})
        status, body = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Greedy", "seats": ["a", "b", "c"]},
        )
        assert status == 400
        assert "seats are open" in body["error"]


def test_joining_a_running_match_is_refused():
    with server() as (base, manager):
        handle = manager.create({"seed": 3, "seats": table(5, 0)})
        status, body = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Late", "seats": ["mine"]},
        )
        assert status == 400
        assert "not waiting" in body["error"]


def test_seat_numbering_follows_the_table_not_who_holds_the_seat():
    """A player's seat number means the same thing to them and to the console."""
    with server() as (base, manager):
        seats = [
            {"name": "A", "kind": "scripted"},
            {"name": "B", "kind": "remote"},
            {"name": "C", "kind": "scripted"},
            {"name": "D", "kind": "remote"},
            {"name": "E", "kind": "scripted"},
        ]
        handle = manager.create({"seed": 4, "seats": seats})
        assert [s["index"] for s in handle.open_seats] == [1, 3]
        assert [handle.game.seats[i].name for i in range(5)] == list("ABCDE")


# ======================================================================
# Playing from the player's own process
# ======================================================================


def test_a_remote_player_plays_a_whole_match():
    with server() as (base, manager):
        handle = manager.create({"seed": 5, "seats": table(4, 1)})

        agent = WatchfulAgent("my-bot")
        client = XColosClient(base, "Alex", poll_timeout_s=3)
        tickets = client.join(handle.match_id, [agent])
        assert len(tickets) == 1

        client.run(max_seconds=40)
        handle.thread.join(timeout=20)

        assert handle.error is None, handle.error
        assert handle.game.status.value == "ended"
        assert agent.saw_briefing, "the remote seat was never briefed"
        assert agent.turns > 0, "the remote seat never acted"


def test_two_separate_players_share_one_table():
    with server() as (base, manager):
        handle = manager.create({"seed": 6, "seats": table(3, 2)})

        a, b = WatchfulAgent("alex-bot"), WatchfulAgent("blair-bot")
        ca = XColosClient(base, "Alex", poll_timeout_s=3)
        cb = XColosClient(base, "Blair", poll_timeout_s=3)
        ca.join(handle.match_id, [a])
        cb.join(handle.match_id, [b])

        threads = [
            threading.Thread(target=c.run, kwargs={"max_seconds": 40}, daemon=True)
            for c in (ca, cb)
        ]
        for t in threads:
            t.start()
        handle.thread.join(timeout=30)
        for c in (ca, cb):
            c.finished.set()
        for t in threads:
            t.join(timeout=5)

        assert handle.error is None, handle.error
        assert handle.game.status.value == "ended"
        assert ca.player_id != cb.player_id
        assert a.saw_briefing and b.saw_briefing


def test_the_players_session_lives_on_the_players_machine():
    """The server holds what it sent. The client holds what it remembers."""
    with server() as (base, manager):
        handle = manager.create({"seed": 7, "seats": table(4, 1)})
        agent = WatchfulAgent("mine")
        client = XColosClient(base, "Alex", poll_timeout_s=3)
        client.join(handle.match_id, [agent])
        client.run(max_seconds=40)
        handle.thread.join(timeout=20)

        seat = next(iter(client.tickets))
        assert agent.session.owner == client.player_id
        assert agent.session.session_id == f"{handle.match_id}:seat{seat}"
        assert len(agent.session) > 1

        # The server cannot produce it, because it is not there.
        sessions = manager.sessions(
            handle.match_id, OPERATOR, handle.operator.token
        )
        mine = next(s for s in sessions if s["seat"] == seat)
        assert mine["remote"] is True
        assert mine["history"] == [], "the server must not hold a remote memory"


def test_a_remote_seat_sees_only_what_it_is_entitled_to():
    with server() as (base, manager):
        handle = manager.create({"seed": 8, "seats": table(4, 1)})
        agent = WatchfulAgent("mine")
        client = XColosClient(base, "Alex", poll_timeout_s=3)
        client.join(handle.match_id, [agent])
        client.run(max_seconds=40)
        handle.thread.join(timeout=20)

        seat = next(iter(client.tickets))
        world = agent.session.transcript()
        game = handle.game
        if game.seats[seat].role != "mafia":
            assert "Your allies are seats" not in world
        for other in game.seats:
            if other != seat:
                assert f"You are seat {other} (" not in world


# ======================================================================
# Misbehaviour
# ======================================================================


def test_a_client_that_stops_answering_does_not_stall_the_match():
    """Silence from a laptop is just a seat that did not answer."""
    with server() as (base, manager):
        handle = manager.create(
            {"seed": 9, "seats": table(4, 1), "deadline_ms": 400}
        )
        post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Ghost", "seats": ["ghost"]},
        )
        # Nobody ever polls or replies.
        handle.thread.join(timeout=90)
        assert not handle.thread.is_alive(), "the match hung waiting for a client"
        assert handle.game.status.value in {"ended", "abandoned"}


def test_polling_a_seat_you_do_not_own_is_refused():
    with server() as (base, manager):
        handle = manager.create({"seed": 10, "seats": table(3, 2)})
        _, alex = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Alex", "seats": ["a"]},
        )
        _, blair = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Blair", "seats": ["b"]},
        )
        blair_seat = blair["seats"][0]["index"]

        status, body = post(
            base, f"/api/matches/{handle.match_id}/poll",
            {
                "player_id": alex["player_id"],
                "token": alex["token"],
                "seat": blair_seat,
                "credential": alex["seats"][0]["credential"],
                "timeout_ms": 200,
            },
        )
        assert status == 403


def test_a_wrong_credential_is_refused():
    with server() as (base, manager):
        handle = manager.create({"seed": 11, "seats": table(4, 1)})
        _, joined = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Alex", "seats": ["a"]},
        )
        status, _ = post(
            base, f"/api/matches/{handle.match_id}/poll",
            {
                "player_id": joined["player_id"],
                "token": joined["token"],
                "seat": joined["seats"][0]["index"],
                "credential": "not-the-credential",
                "timeout_ms": 200,
            },
        )
        assert status == 403


def test_a_stray_reply_is_dropped_rather_than_queued():
    """An answer to a question nobody asked must not be banked for later."""
    with server() as (base, manager):
        # Two open seats, one joiner, so the match has not started and no seat
        # is being asked anything yet.
        handle = manager.create({"seed": 12, "seats": table(3, 2)})
        _, joined = post(
            base, f"/api/matches/{handle.match_id}/join",
            {"player_name": "Alex", "seats": ["a"]},
        )
        assert handle.waiting
        seat = joined["seats"][0]
        status, body = post(
            base, f"/api/matches/{handle.match_id}/reply",
            {
                "player_id": joined["player_id"],
                "token": joined["token"],
                "seat": seat["index"],
                "credential": seat["credential"],
                "action": {"type": "vote", "target": 0},
            },
        )
        assert status == 200
        assert body["accepted"] is False


def test_joining_an_unknown_match_fails_cleanly():
    with server() as (base, _):
        client = XColosClient(base, "Alex", poll_timeout_s=2)
        with pytest.raises(ClientError):
            client.join("no-such-match", [RandomAgent(name="x")])
