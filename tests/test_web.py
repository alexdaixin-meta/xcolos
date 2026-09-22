"""The operator console's HTTP API.

The UI holds no game state, so these tests cover the contract it depends on:
create a match, poll its log, read the outcome.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
from contextlib import contextmanager

import pytest

from xcolos.web.server import AGENT_TYPES, GAMES, MatchManager, build_server


@contextmanager
def running_server():
    server = build_server(port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()


def get(base: str, path: str):
    with urllib.request.urlopen(base + path, timeout=5) as r:
        return r.status, json.loads(r.read())


def post(base: str, path: str, payload: dict):
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


def table(n: int, kind: str = "scripted"):
    return [{"name": f"P{i}", "kind": kind} for i in range(n)]


# ----------------------------------------------------------------------
# Manager
# ----------------------------------------------------------------------


def wait_for(manager: MatchManager, match_id: str, timeout: float = 10.0):
    """Start the match, then wait for it.

    Creating a table no longer runs it. Whoever set the table presses start,
    so a test that wants a finished match has to do the same.
    """
    manager.start_match(match_id)
    deadline = time.time() + timeout
    while time.time() < deadline:
        handle = manager.get(match_id)
        if handle and handle.thread and not handle.thread.is_alive():
            return handle
        time.sleep(0.01)
    raise AssertionError("match did not finish in time")


def test_a_match_runs_to_completion():
    m = MatchManager()
    handle = m.create({"game": "mafia", "seed": 3, "seats": table(5)})
    done = wait_for(m, handle.match_id)
    assert done.error is None
    assert done.snapshot()["winner"] in {"good", "evil"}


@pytest.mark.parametrize("n", [4, 5, 7, 9, 12])
def test_any_legal_table_size_plays(n):
    m = MatchManager()
    handle = m.create({"game": "mafia", "seed": 2, "seats": table(n)})
    done = wait_for(m, handle.match_id)
    assert done.error is None, done.error
    assert done.snapshot()["status"] == "ended"
    assert len(done.snapshot()["seats"]) == n


@pytest.mark.parametrize("n", [0, 1, 3, 13])
def test_illegal_table_sizes_are_refused(n):
    m = MatchManager()
    with pytest.raises(ValueError):
        m.create({"game": "mafia", "seats": table(n)})


def test_unknown_game_is_refused():
    m = MatchManager()
    with pytest.raises(ValueError):
        m.create({"game": "chess", "seats": table(5)})


@pytest.mark.parametrize("kind", ["random", "scripted", "broken", "silent"])
def test_every_agent_type_can_fill_a_table(kind):
    m = MatchManager()
    handle = m.create({"game": "mafia", "seed": 5, "seats": table(5, kind)})
    done = wait_for(m, handle.match_id)
    assert done.error is None, done.error
    assert done.snapshot()["status"] in {"ended", "abandoned"}


def test_events_are_paged_and_never_repeat():
    m = MatchManager()
    handle = m.create({"game": "mafia", "seed": 4, "seats": table(5)})
    wait_for(m, handle.match_id)

    seen, since = [], 0
    while True:
        page = m.events(handle.match_id, since)
        seen.extend(page["records"])
        if since == page["next"]:
            break
        since = page["next"]

    assert [r["log_seq"] for r in seen] == list(range(len(seen)))
    assert seen == handle.game.log.records


def test_the_same_seed_and_table_give_the_same_result():
    m = MatchManager()
    a = wait_for(m, m.create({"seed": 8, "seats": table(6)}).match_id)
    b = wait_for(m, m.create({"seed": 8, "seats": table(6)}).match_id)
    assert a.snapshot()["winner"] == b.snapshot()["winner"]
    assert a.game.log.stable_records()[1:] == b.game.log.stable_records()[1:]


# ----------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------


def test_reference_endpoints_describe_what_the_ui_needs():
    with running_server() as base:
        status, games = get(base, "/api/games")
        assert status == 200
        assert {g["id"] for g in games} == {g["id"] for g in GAMES}
        for g in games:
            assert g["min_seats"] < g["max_seats"]

        status, kinds = get(base, "/api/agent_types")
        assert status == 200
        assert {k["id"] for k in kinds} == {k["id"] for k in AGENT_TYPES}


def test_the_ui_is_served():
    with running_server() as base:
        with urllib.request.urlopen(base + "/", timeout=5) as r:
            body = r.read().decode()
        assert r.status == 200
        assert "XColos" in body
        for asset in ("/static/app.js", "/static/style.css"):
            with urllib.request.urlopen(base + asset, timeout=5) as r:
                assert r.status == 200


def test_create_then_poll_to_the_end():
    with running_server() as base:
        status, created = post(
            base, "/api/matches", {"seed": 6, "seats": table(5), "pace_ms": 0}
        )
        assert status == 201
        match_id = created["match_id"]
        assert created["ready"] and not created["started"]

        started, _ = post(base, f"/api/matches/{match_id}/start", {})
        assert started == 200

        since, records, done = 0, [], False
        deadline = time.time() + 10
        while not done and time.time() < deadline:
            _, page = get(base, f"/api/matches/{match_id}/events?since={since}")
            records.extend(page["records"])
            since = page["next"]
            done = page["done"]
            if not done:
                time.sleep(0.02)

        assert done, "match did not finish"
        assert records
        assert page["state"]["winner"] in {"good", "evil"}
        assert any(r["category"] == "result" for r in records)


def test_a_bad_table_returns_a_readable_error():
    with running_server() as base:
        status, body = post(base, "/api/matches", {"seats": table(2)})
        assert status == 400
        assert "seats" in body["error"]


def test_unknown_paths_are_not_found():
    with running_server() as base:
        for path in ("/api/nope", "/api/matches/does-not-exist"):
            try:
                urllib.request.urlopen(base + path, timeout=5)
                raise AssertionError(f"{path} should not have succeeded")
            except urllib.error.HTTPError as e:
                assert e.code == 404


def test_static_serving_refuses_to_escape_its_directory():
    with running_server() as base:
        try:
            urllib.request.urlopen(base + "/static/../server.py", timeout=5)
            raise AssertionError("path traversal should be refused")
        except urllib.error.HTTPError as e:
            assert e.code == 404
        except urllib.error.URLError:
            pass  # the client normalised the path away, which is also fine


# ----------------------------------------------------------------------
# A table that waits on a pulling agent
# ----------------------------------------------------------------------


def connector_table(m: MatchManager, seed: int = 21):
    """Four bots and one seat played by an agent that pulls."""
    handle = m.create(
        {
            "seed": seed,
            "seats": [{"name": "Agent", "kind": "connector"}]
            + [{"name": f"B{i}", "kind": "random"} for i in range(4)],
        }
    )
    pid = handle.tools.summary()["open_seats"][0]["player_id"]
    return handle, pid


def test_the_console_keeps_polling_while_it_waits_on_an_agent():
    """A pulling table has no thread, so "done" cannot mean "no thread".

    Getting this wrong stopped the console dead on its first poll: it saw no
    running thread, concluded the match was over, and never logged again.
    """
    m = MatchManager()
    handle, pid = connector_table(m)

    # Before anyone connects, and before start, the match is plainly not over.
    assert m.events(handle.match_id, 0)["done"] is False

    m.tools_for_player(pid)[1].play(pid)
    m.start_match(handle.match_id)

    page = m.events(handle.match_id, 0)
    assert page["done"] is False, "parked on an agent is not finished"
    assert page["records"], "starting should have logged something"


def test_the_log_grows_as_the_agent_pulls_and_posts():
    m = MatchManager()
    handle, pid = connector_table(m)
    tools = m.tools_for_player(pid)[1]
    tools.play(pid)
    m.start_match(handle.match_id)

    since, ack, answer, sizes = 0, None, None, []
    for _ in range(60):
        page = m.events(handle.match_id, since)
        since = page["next"]
        sizes.append(since)
        if page["done"]:
            break
        state = tools.play(pid, ack, answer)
        ack, answer = state.get("ack_through"), None
        if state.get("your_turn"):
            ask = state["ask"]
            answer = (
                ask["legal_answers"][0] if ask["legal_answers"] else "Nothing yet."
            )

    assert page["done"], "the match never finished"
    assert sizes[-1] > sizes[0], "the log never grew while the agent played"
    assert handle.game.status.value == "ended"
    assert page["state"]["winner"] in {"good", "evil"}


def test_done_only_becomes_true_when_the_match_actually_ends():
    m = MatchManager()
    handle, pid = connector_table(m, seed=5)
    tools = m.tools_for_player(pid)[1]
    tools.play(pid)
    m.start_match(handle.match_id)

    ack, answer = None, None
    for _ in range(60):
        done = m.events(handle.match_id, 0)["done"]
        running = handle.game.status.value == "running"
        assert done != running, "done must track the match, not a thread"
        if done:
            return
        state = tools.play(pid, ack, answer)
        ack, answer = state.get("ack_through"), None
        if state.get("your_turn"):
            ask = state["ask"]
            answer = ask["legal_answers"][0] if ask["legal_answers"] else "Hmm."
    raise AssertionError("the match never finished")
