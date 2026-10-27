"""Many games at once: pinned code, one game's trouble never stopping another, and the line stopped when a failure repeats."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import batch  # noqa: E402


class FakeWorld:
    """Stands in for the processes: convert writes the verdict a game is scripted to get; simulate writes finished plays and a reasoning check."""

    def __init__(self, root: Path, verdicts: dict[str, tuple[str, str]]):
        self.root, self.verdicts, self.commands, self.full = root, verdicts, [], []

    def __call__(self, cmd: list[str], cwd: Path, log: Path) -> int:
        self.commands.append((cmd[3], cmd[4], cwd))
        self.full.append(cmd)
        step, game = cmd[3], cmd[4]
        folder = cwd / "gen_game" / "data" / "games" / game
        if step == "convert":
            verdict, detail = self.verdicts[game]
            if verdict == "crashed":
                log.write_text("Traceback (most recent call last):\nKeyError: 'steps'\n")
                return 1
            (folder / "logs").mkdir(parents=True, exist_ok=True)
            (folder / "logs" / "run.json").write_text(json.dumps({"state": "finished", "verdict": verdict, "detail": detail}))
            return 0 if verdict == "ready_for_review" else 2
        if step == "simulate":
            (folder / "sim").mkdir(exist_ok=True)
            for n in (1, 2):
                (folder / "sim" / f"w000{n}-seed{n}.json").write_text(json.dumps({"snapshot": {"status": "ended", "winner": "seat 1"}}))
            (folder / "reasoning.json").write_text(json.dumps({"verdict": "strong", **{a: {"score": 3} for a in ("reasoning", "planning")}, "luck": {"score": 1}}))
        return 0


def code_dir(d: str) -> Path:
    code = Path(d) / "code"
    (code / "gen_game" / "data" / "games").mkdir(parents=True)
    return code


def test_a_game_that_comes_out_whole_is_installed_play_tested_and_its_reasoning_read():
    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        world = FakeWorld(code, {"jaipur": ("ready_for_review", "34/34 scenarios")})
        row = batch.run_game("jaipur", code, "python", plays=2, log=Path(d) / "jaipur.log", runner=world)
        assert [c[0] for c in world.commands] == ["convert", "uninstall", "install", "simulate"]
        assert row["outcome"] == "ready_for_review" and row["plays"] == {"of": 2, "ended": 2, "results": {"seat 1": 2}, "players": "gateway"}
        assert row["reasoning"] == {"verdict": "strong", "scores": "reasoning 3, planning 3, luck 1"}
        simulate = next(c for c in world.full if c[3] == "simulate")
        assert simulate[simulate.index("--players") + 1] == "gateway"  # the same players for every game: Claude, which says why it plays


def test_a_dropped_game_is_not_played_and_a_crash_is_read_from_its_log():
    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        world = FakeWorld(code, {"hangman": ("dropped", "too simple"), "cuttle": ("crashed", "")})
        assert batch.run_game("hangman", code, "python", 2, Path(d) / "h.log", world)["outcome"] == "dropped"
        crashed = batch.run_game("cuttle", code, "python", 2, Path(d) / "c.log", world)
        assert crashed["outcome"] == "crashed" and "KeyError: 'steps'" in crashed["detail"]
        assert [c[0] for c in world.commands] == ["convert", "convert"]


def test_the_same_failure_in_three_games_stops_the_line_but_expected_outcomes_never_do():
    def row(game, outcome, detail):
        return {"id": game, "outcome": outcome, "detail": detail}

    spec = [row(g, "spec_failed", f"{g}: the model call failed after 4 tries") for g in ("a", "b")]
    assert batch.should_stop(spec, 3) is None
    assert batch.should_stop(spec + [row("c", "spec_failed", "c: the model call failed after 5 tries")], 3)  # same failure, other numbers and names
    expected = [row(g, o, "x") for g in "abcdef" for o in ("dropped", "platform_limit", "ready_for_review")]
    assert batch.should_stop(expected, 3) is None


def test_a_batch_runs_games_side_by_side_stops_launching_after_a_repeated_failure_and_resumes_only_the_unfinished():
    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        out = Path(d) / "batch"
        out.mkdir()
        (out / "CODE").write_text(str(code))
        verdicts = {g: ("encode_failed", "the game file did not parse") for g in ("a", "b", "c", "d")} | {"ok": ("ready_for_review", "")}
        world = FakeWorld(code, verdicts)
        rows = batch.run_batch(["ok", "a", "b", "c", "d"], out, jobs=1, plays=2, stop_after=3, python="python", runner=world, say=lambda m: None)
        assert [r["id"] for r in rows] == ["ok", "a", "b", "c"]  # d was never started: the line stopped after c
        report = (out / "BATCH.md").read_text()
        assert "Stopped" in report and "the game file did not parse" in report and "| ok | ready_for_review" in report
        world.verdicts.update({g: ("ready_for_review", "") for g in "abcd"})
        rows = batch.run_batch(["ok", "a", "b", "c", "d"], out, jobs=2, plays=2, stop_after=3, python="python", runner=world, say=lambda m: None)
        assert sorted(r["id"] for r in rows) == ["a", "b", "c", "d", "ok"] and all(r["outcome"] == "ready_for_review" for r in rows)
        assert sum(1 for c in world.commands if c[:2] == ("convert", "ok")) == 1  # a finished game is not run again


def test_pinning_copies_the_committed_code_and_links_the_data_back():
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d) / "repo"
        for rel in ("gen_game/flow.py", "gen_game/data/games/x/game.json", "gen_inventory/data/inventory/x.json", "xcolos/games/library/x.json"):
            (repo / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / rel).write_text("committed")
        git = ["git", "-C", str(repo), "-c", "user.email=t@t", "-c", "user.name=t"]
        subprocess.run(git[:3] + ["init", "-q"], check=True)
        subprocess.run(git + ["add", "-A"], check=True)
        subprocess.run(git + ["commit", "-qm", "c"], check=True)
        (repo / "gen_game" / "flow.py").write_text("an edit not committed")
        pinned = batch.pin(repo, "HEAD", Path(d) / "pins")
        assert (pinned / "gen_game" / "flow.py").read_text() == "committed"
        for rel in batch.SHARED:
            assert (pinned / rel).is_symlink() and (pinned / rel).resolve() == (repo / rel).resolve()
        assert batch.pin(repo, "HEAD", Path(d) / "pins") == pinned  # pinning the same commit again reuses the copy


def test_replay_plays_again_the_games_played_on_older_code_without_converting_them():
    with tempfile.TemporaryDirectory() as d:
        old, new = code_dir(d), Path(d) / "code2"
        (new / "gen_game" / "data").mkdir(parents=True)
        (new / "gen_game" / "data" / "games").symlink_to(old / "gen_game" / "data" / "games")
        out = Path(d) / "batch"
        out.mkdir()
        (out / "CODE").write_text(str(old))
        world = FakeWorld(old, {"ok": ("ready_for_review", ""), "gone": ("dropped", "too simple")})
        batch.run_batch(["ok", "gone"], out, 1, 2, 3, "python", runner=world, say=lambda m: None)
        (out / "CODE").write_text(str(new))  # a fix was pinned
        world.commands.clear()
        rows = batch.run_batch(["ok", "gone"], out, 1, 2, 3, "python", runner=world, say=lambda m: None, replay=True)
        assert [c[:2] for c in world.commands] == [("uninstall", "ok"), ("install", "ok"), ("simulate", "ok")]
        assert {r["id"]: r["code"] for r in rows} == {"ok": "code2", "gone": "code"}  # a dropped game is not played again


def test_replay_also_plays_again_a_game_played_by_other_players_on_the_same_code():
    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        out = Path(d) / "batch"
        out.mkdir()
        (out / "CODE").write_text(str(code))
        row = {"id": "ok", "code": "code", "outcome": "ready_for_review", "detail": "", "plays": {"of": 2, "ended": 2, "results": {}}, "reasoning": None}
        (out / "batch.json").write_text(json.dumps({"ids": ["ok"], "rows": [row], "stopped": None}))  # played before the players were recorded
        world = FakeWorld(code, {})
        batch.run_batch(["ok"], out, 1, 2, 3, "python", runner=world, say=lambda m: None, replay=True)
        assert [c[0] for c in world.commands] == ["uninstall", "install", "simulate"]


def test_running_some_of_a_batchs_games_keeps_the_others_rows():
    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        out = Path(d) / "batch"
        out.mkdir()
        (out / "CODE").write_text(str(code))
        world = FakeWorld(code, {"a": ("needs_review", "24/28 scenarios"), "b": ("encode_failed", "did not parse")})
        batch.run_batch(["a", "b"], out, 1, 0, 3, "python", runner=world, say=lambda m: None)
        world.verdicts["b"] = ("ready_for_review", "")
        batch.run_batch(["b"], out, 1, 0, 3, "python", runner=world, say=lambda m: None)
        kept = json.loads((out / "batch.json").read_text())
        assert {r["id"]: r["outcome"] for r in kept["rows"]} == {"a": "needs_review", "b": "ready_for_review"}
        assert "| a | needs_review" in (out / "BATCH.md").read_text()


def test_installs_from_parallel_games_never_overlap():
    import threading
    import time as clock

    with tempfile.TemporaryDirectory() as d:
        code = code_dir(d)
        inside, overlaps = [], []

        def runner(cmd, cwd, log):
            if cmd[3] in ("install", "uninstall"):
                if inside:
                    overlaps.append(cmd[4])
                inside.append(cmd[4])
                clock.sleep(0.05)
                inside.remove(cmd[4])
            return 1 if cmd[3] == "install" else 0  # stop after installing: only the installs matter here

        rows = [{"id": g, "outcome": "ready_for_review"} for g in ("a", "b", "c")]
        threads = [threading.Thread(target=batch.play_game, args=(r, code, "python", 1, Path(d) / f"{r['id']}.log", runner)) for r in rows]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert overlaps == []
