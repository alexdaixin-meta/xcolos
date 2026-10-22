"""A game played on the web server is logged to a file as it goes, with a summary beside it."""

import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oracle_game  # noqa: E402,F401 - the arithmetic Mafia fixture
from xcolos.log import MatchLog
from xcolos.web import server

SEATS = [{"name": f"P{i}", "kind": "scripted"} for i in range(5)]
TABLE = {"game": "mafia-oracle", "seed": 3, "seats": SEATS}


def finish(m, handle, timeout=10.0):
    server.build_completion = lambda: None  # no model: the review is skipped, not fetched over the network
    m.start_match(handle.match_id)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if handle.game.status.value != "running" and not handle.reviewing:
            break
        time.sleep(0.01)
    time.sleep(0.1)  # the runner thread writes the review and the summary as it concludes


def test_a_played_game_leaves_its_log_and_a_summary():
    with tempfile.TemporaryDirectory() as tmp:
        m = server.MatchManager(Path(tmp))
        handle = m.create(TABLE)
        finish(m, handle)
        log_file = Path(tmp) / "w0001.jsonl"
        on_disk = MatchLog.load(log_file)
        assert len(on_disk) == len(handle.game.log.records)
        assert on_disk == handle.game.log.records
        summary = json.loads((Path(tmp) / "w0001.summary.json").read_text())
        assert summary["game"] == "mafia-oracle" and summary["status"] == "ended"
        assert summary["winner"] == handle.game.winner and summary["log"] == "w0001.jsonl"
        assert [s["name"] for s in summary["seats"]] == [f"P{i}" for i in range(5)]
        assert summary["review"] == "skipped"  # offline: no model to review with
        assert any(r["type"] == "review" for r in MatchLog.load(log_file))


def test_the_log_says_which_model_is_behind_each_seat():
    seats = [{"name": "B", "kind": "llm", "model": "claude:haiku"}, {"name": "C", "kind": "llm"},
             {"name": "D", "kind": "random"}, {"name": "E", "kind": "scripted"}, {"name": "F", "kind": "scripted"}]
    with tempfile.TemporaryDirectory() as tmp:
        m = server.MatchManager(Path(tmp))
        handle = m.create({"game": "mafia-oracle", "seed": 1, "seats": seats})
        rows = {r["name"]: r for r in handle.game.log.where("setup", "seat_model")}
        assert rows["B"]["model"] == "claude:haiku" and rows["B"]["kind"] == "llm"
        assert rows["C"]["model"] == "offline-stub"
        assert rows["D"]["model"] is None and rows["D"]["kind"] == "random"
        assert [r["model"] for r in MatchLog.load(Path(tmp) / "w0001.jsonl") if r["type"] == "seat_model"] == [
            "claude:haiku", "offline-stub", None, None, None]


def test_each_game_on_a_table_has_its_own_files():
    with tempfile.TemporaryDirectory() as tmp:
        m = server.MatchManager(Path(tmp))
        handle = m.create(TABLE)
        finish(m, handle)
        finish(m, handle)
        names = sorted(p.name for p in Path(tmp).iterdir())
        assert names == ["w0001-g2.jsonl", "w0001-g2.summary.json", "w0001.jsonl", "w0001.summary.json"]


def test_without_a_log_dir_nothing_is_written():
    with tempfile.TemporaryDirectory() as tmp:
        m = server.MatchManager()
        handle = m.create(TABLE)
        finish(m, handle)
        assert handle.game.log.path is None and list(Path(tmp).iterdir()) == []
