"""A game that did not pass is marked twice: `not_passed` in its inventory record, and a file in its game folder.

A drop or a platform limit already writes its own file (DROPPED.md, PLATFORM_LIMIT.md) and its own status;
anything else that did not pass (a person must review it, a step or the play-test failed) gets NOT_PASSED.md.
Passing moves every mark an earlier run left into history/. The record's status is never changed here, so a game that
is not dropped or blocked is converted again.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

PASSED = "ready_for_review"
FILE = "NOT_PASSED.md"
OWN_FILES = {"dropped": "DROPPED.md", "platform_limit": "PLATFORM_LIMIT.md"}
CONVERTED = ("ready", "ported", "evaluated", "accepted")  # what convert runs; any other record was refused, not tried

NEXT = {
    "needs_review": "A person reads REPORT.md and decides: fix the game file or its tests, or drop the game.",
    "play_failed": "The game converted; its play-test did not finish. Play it again: `gen_game batch --name <batch> --replay`, "
                   "or `gen_game simulate <id> --players gateway`.",
    "install_failed": "The game converted but could not be installed into the library; see the batch log.",
}
AGAIN = "Convert it again (`gen_game convert <id> --judge`, or run its batch again with the same name); see logs/ for what failed."


def mark(inv, game_id: str, folder: Path, outcome: str, detail: str) -> None:
    """Record how gen_game's last run of a game came out, in the inventory and in the folder."""
    try:
        rec = inv.get(game_id)
    except KeyError:
        rec = None
    passed = outcome == PASSED
    if not passed and outcome not in OWN_FILES and rec is not None and rec.status not in CONVERTED:
        return  # refused before anything was tried: whatever marked it (a drop, a block) still stands
    text = "" if passed else f"{outcome}: {detail}".strip().rstrip(":")
    if rec is not None:
        # a game built through a pinned copy of the code has its port there; the copy goes, the game stays
        port = str(Path(rec.port).resolve()) if passed and rec.port else rec.port
        if (rec.not_passed, rec.port) != (text, port):
            inv.save(dataclasses.replace(rec, not_passed=text, port=port))
    stale = [FILE, *OWN_FILES.values()] if passed else [FILE] if outcome in OWN_FILES else []
    for name in stale:  # an earlier run's mark: kept in history/, out of the way
        if (folder / name).exists():
            (folder / "history").mkdir(exist_ok=True)
            (folder / name).replace(folder / "history" / name)
    if not passed and outcome not in OWN_FILES:
        folder.mkdir(parents=True, exist_ok=True)
        lines = [f"# Not passed: {outcome.replace('_', ' ')}", "", detail or "(no detail)", "",
                 NEXT.get(outcome, AGAIN).replace("<id>", game_id), "",
                 "The inventory record has the same reason in `not_passed`; passing clears both."]
        (folder / FILE).write_text("\n".join(lines) + "\n")
