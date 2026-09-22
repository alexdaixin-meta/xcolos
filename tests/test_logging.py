"""The log must be complete, clear and structured.

It is not in the gameplay path, so nothing reads it back at runtime. That makes
these tests the only thing keeping it honest.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from xcolos.agents import BrokenAgent, ScriptedAgent
from xcolos.cli import SEAT_NAMES, build_match
from xcolos.log import CATEGORIES, MatchLog, validate_log
from xcolos.protocol import MsgType
from xcolos.runner import Runner
from xcolos.transcript import seat_transcript, summarize, timeline


def play(seed: int, agent_factory=None):
    game, orch, registry, _host = build_match(seed, agent_factory=agent_factory)
    result = Runner(game, orch, registry).run()
    return result, game


# ----------------------------------------------------------------------
# Structure
# ----------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(1, 16))
def test_log_is_structurally_valid(seed):
    _, game = play(seed)
    assert validate_log(game.log.records) == []


@pytest.mark.parametrize("seed", range(1, 11))
def test_every_record_has_the_common_fields(seed):
    _, game = play(seed)
    for r in game.log.records:
        for f in ("log_seq", "ts", "category", "type"):
            assert f in r, f"record {r} is missing {f}"
        assert r["category"] in CATEGORIES


def test_context_is_stamped_on_records_written_during_play():
    _, game = play(4)
    during = [r for r in game.log.records if r["category"] in {"turn", "fact"}]
    assert during
    for r in during:
        assert "round" in r and "phase" in r and "turn_seq" in r


def test_log_is_valid_json_lines_on_disk():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        game, orch, registry, _ = build_match(9, out)
        Runner(game, orch, registry).run()
        path = out / "m_00000009.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        assert rows == game.log.records
        assert validate_log(rows) == []


def test_field_order_puts_identifying_fields_first():
    """Insertion order is preserved, so a human scanning the file reads
    log_seq, time, category and type before anything type-specific."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        game, orch, registry, _ = build_match(9, out)
        Runner(game, orch, registry).run()
        first = (out / "m_00000009.jsonl").read_text().splitlines()[0]
        keys = list(json.loads(first).keys())
        assert keys[:4] == ["log_seq", "ts", "category", "type"]


# ----------------------------------------------------------------------
# Completeness
# ----------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(1, 11))
def test_every_message_in_both_directions_is_logged(seed):
    _, game = play(seed)
    out = game.log.where("message", "to_agent")
    back = game.log.where("message", "from_agent")

    turns = game.log.where("turn", "move")
    prompts = [m for m in out if m["msg_type"] == MsgType.YOUR_TURN.value]

    # Every turn produced at least one prompt, and every prompt got a logged
    # reply, including the rejected ones from the repair ladder.
    assert len(prompts) >= len(turns)
    assert len(back) == len(prompts)


@pytest.mark.parametrize("seed", range(1, 11))
def test_every_seat_is_greeted_and_dismissed(seed):
    _, game = play(seed)
    for seat in game.seats:
        kinds = {
            r["msg_type"] for r in game.log.where("message", "to_agent", seat=seat)
        }
        assert MsgType.GAME_START.value in kinds
        assert MsgType.GAME_END.value in kinds


@pytest.mark.parametrize("seed", range(1, 11))
def test_every_orchestrator_request_is_logged_with_its_reason(seed):
    _, game = play(seed)
    requests = game.log.where("orchestrator", "action_request")
    assert requests
    for r in requests:
        assert r["reason"], "every request must say why this seat was chosen"
        assert r["prompt"]


def test_every_state_change_is_logged():
    _, game = play(6)
    eliminations = game.log.where("state", "eliminate")
    dead = [i for i, s in game.seats.items() if not s.alive]
    assert {r["seat"] for r in eliminations} == set(dead)


def test_failed_attempts_are_recorded_not_swallowed():
    _, game = play(11, lambda i, name: BrokenAgent(name=name))
    moves = game.log.where("turn", "move")
    assert moves
    degraded = [m for m in moves if m["degraded"]]
    assert degraded
    for m in degraded:
        assert len(m["attempts"]) > 1
        assert all(a["outcome"] == "invalid" for a in m["attempts"])
        assert m["outcome"] == "defaulted"


def test_roles_are_revealed_in_the_result_not_only_mid_match():
    result, game = play(8)
    summary = game.log.where("result", "summary")[0]
    assert summary["roles"] == {str(i): s.role for i, s in game.seats.items()}
    assert summary["winner"] == result.winner


# ----------------------------------------------------------------------
# Determinism of the log itself
# ----------------------------------------------------------------------


def test_two_runs_of_a_seed_log_the_same_thing():
    _, a = play(5)
    _, b = play(5)
    assert a.log.stable_records() == b.log.stable_records()


def test_timestamps_are_the_only_volatile_field():
    _, a = play(5)
    _, b = play(5)
    differing = [
        k
        for ra, rb in zip(a.log.records, b.log.records)
        for k in ra
        if ra[k] != rb.get(k)
    ]
    assert set(differing) <= {"ts"}


# ----------------------------------------------------------------------
# Views
# ----------------------------------------------------------------------


def test_seat_transcript_contains_only_that_seats_messages():
    _, game = play(7)
    for seat in game.seats:
        text = seat_transcript(game.log.records, seat)
        assert text
        for other in game.seats:
            if other == seat:
                continue
            # No other seat's private delivery can appear in this one's world.
            assert f"You are seat {other} in a game" not in text


def test_timeline_renders_and_marks_phases():
    _, game = play(7)
    text = timeline(game.log.records)
    assert "round 1 / night" in text
    assert "RESULT" in text


def test_summarize_counts_every_record():
    _, game = play(7)
    s = summarize(game.log.records)
    assert s["records"] == len(game.log.records)
    assert sum(s["counts"].values()) == len(game.log.records)


def test_validate_log_catches_a_broken_log():
    _, game = play(3)
    rows = [dict(r) for r in game.log.records]
    rows[5]["log_seq"] = 999
    assert validate_log(rows)

    rows2 = [r for r in game.log.records if r["category"] != "result"]
    assert "log has no result record" in validate_log(rows2)


def test_unknown_category_is_rejected():
    log = MatchLog("m_cat")
    with pytest.raises(ValueError):
        log.record("not_a_category", "whatever")
