"""A game that did not pass is marked twice: in its inventory record and in its game folder."""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import world  # noqa: E402

from gen_game import marks  # noqa: E402


def test_a_game_that_needs_review_is_marked_in_the_record_and_the_folder_and_can_still_be_converted():
    inv, root = world()
    marks.mark(inv, "rps", root / "rps", "needs_review", "25/27 scenarios")
    rec = inv.get("rps")
    assert rec.not_passed == "needs_review: 25/27 scenarios" and rec.status == "ready"
    text = (root / "rps" / "NOT_PASSED.md").read_text()
    assert "needs review" in text and "25/27 scenarios" in text and "REPORT.md" in text


def test_passing_later_clears_every_mark_an_earlier_run_left():
    inv, root = world()
    marks.mark(inv, "rps", root / "rps", "encode_failed", "the game file did not parse")
    (root / "rps" / "DROPPED.md").write_text("# Dropped\n")  # from a drop that was cleared since
    marks.mark(inv, "rps", root / "rps", "ready_for_review", "34/34 scenarios")
    assert inv.get("rps").not_passed == ""
    assert not (root / "rps" / "NOT_PASSED.md").exists() and not (root / "rps" / "DROPPED.md").exists()
    assert (root / "rps" / "history" / "DROPPED.md").read_text() == "# Dropped\n"  # kept, out of the way


def test_a_drop_or_a_platform_limit_keeps_the_file_the_flow_wrote_and_is_recorded_too():
    inv, root = world()
    marks.mark(inv, "rps", root / "rps", "needs_review", "25/27 scenarios")
    (root / "rps" / "DROPPED.md").write_text("# Dropped: too simple\n")
    inv.save(dataclasses.replace(inv.get("rps"), status="rejected", dropped="too simple: always rock"))
    marks.mark(inv, "rps", root / "rps", "dropped", "too simple: always rock")
    assert inv.get("rps").not_passed == "dropped: too simple: always rock"
    assert (root / "rps" / "DROPPED.md").exists() and not (root / "rps" / "NOT_PASSED.md").exists()


def test_a_game_the_flow_refused_to_convert_is_left_as_it_was():
    inv, root = world(status="rejected", dropped="too simple: always rock")
    (root / "rps").mkdir()
    (root / "rps" / "DROPPED.md").write_text("# Dropped: too simple\n")
    marks.mark(inv, "rps", root / "rps", "needs_review", "the inventory has it as dropped (too simple: always rock); only ready games are converted")
    assert inv.get("rps").not_passed == "" and not (root / "rps" / "NOT_PASSED.md").exists()
    assert (root / "rps" / "DROPPED.md").exists()


def test_a_play_test_that_did_not_finish_marks_a_converted_game_and_says_how_to_play_it_again():
    inv, root = world(status="evaluated", port="/x/rps/game.json")
    marks.mark(inv, "rps", root / "rps", "play_failed", "2 of 3 plays ended; 429 rate_limit_error")
    rec = inv.get("rps")
    assert rec.status == "evaluated" and rec.not_passed == "play_failed: 2 of 3 plays ended; 429 rate_limit_error"
    assert "--replay" in (root / "rps" / "NOT_PASSED.md").read_text()


def test_a_game_with_no_inventory_record_is_marked_in_its_folder():
    inv, root = world()
    marks.mark(inv, "other", root / "other", "crashed", "KeyError: 'steps'")
    assert "KeyError" in (root / "other" / "NOT_PASSED.md").read_text()


def test_passing_records_where_the_game_really_is_not_the_pinned_copy_it_was_built_through():
    inv, root = world()
    (root / "real" / "rps").mkdir(parents=True)
    (root / "pin").symlink_to(root / "real")
    inv.save(dataclasses.replace(inv.get("rps"), status="evaluated", port=str(root / "pin" / "rps" / "game.json")))
    marks.mark(inv, "rps", root / "pin" / "rps", "ready_for_review", "34/34 scenarios")
    assert inv.get("rps").port == str((root / "real" / "rps" / "game.json").resolve())


def test_convert_marks_a_game_that_did_not_pass():
    from gen_game.cli import main

    inv, root = world()
    assert main(["--inventory", str(inv.root), "--root", str(root), "convert", "rps", "--model", "echo:x", "--no-adapt"]) == 2
    assert inv.get("rps").not_passed and (root / "rps" / "NOT_PASSED.md").exists()
