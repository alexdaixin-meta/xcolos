"""Is the run still going, finished, or stopped?

The call log only records a call when it ends, and a long model call is silent for minutes, so the logs alone cannot
tell a slow call from a dead process. Two small files can:

  logs/run.json      written when `convert` starts (its process id and start time) and again when it ends (the
                     verdict, or `crashed`). A process that is gone with no verdict was killed.
  logs/current.json  written by the call recorder while a model call is open: which step, how long it has waited,
                     and, for Muse's background mode, the response id and Muse's own status, refreshed on every poll.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def started(logs: Path) -> None:
    logs.mkdir(parents=True, exist_ok=True)
    (logs / "run.json").write_text(json.dumps({"pid": os.getpid(), "started": _now(), "state": "running"}, indent=2) + "\n")


def ended(logs: Path, verdict: str, detail: str = "") -> None:
    path = logs / "run.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.update({"state": "finished" if verdict != "crashed" else "crashed", "verdict": verdict, "detail": detail[:300], "ended": _now()})
    path.write_text(json.dumps(data, indent=2) + "\n")


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _age(iso: str) -> int:
    return int((datetime.now(timezone.utc) - datetime.fromisoformat(iso)).total_seconds())


def _process_for(game_id: str) -> int | None:
    """A `gen_game convert <id>` process, found by name: for a run that began before it kept a run record."""
    import subprocess

    try:
        out = subprocess.run(["pgrep", "-f", f"gen_game convert {game_id}"], capture_output=True, text=True, timeout=5).stdout.split()
    except (OSError, subprocess.SubprocessError):
        return None
    mine = {os.getpid(), os.getppid()}
    return next((int(p) for p in out if int(p) not in mine), None)


def state(folder: Path) -> tuple[str, str]:
    """(RUNNING | FINISHED | STOPPED | NOT STARTED, a sentence saying how we know)."""
    run = folder / "logs" / "run.json"
    if not run.exists():
        if (pid := _process_for(folder.name)) is not None:
            return "RUNNING", f"process {pid} is alive (it began before runs were recorded, so there is no start time)"
        return "NOT STARTED", "no logs/run.json and no running `gen_game convert` for this game"
    r = json.loads(run.read_text())
    if r.get("state") in ("finished", "crashed"):
        word = "FINISHED" if r["state"] == "finished" else "STOPPED"
        return word, f"{r['state']} at {r.get('ended')}: {r.get('verdict')}" + (f" ({r['detail']})" if r.get("detail") else "")
    if alive(r["pid"]):
        return "RUNNING", f"process {r['pid']} is alive, started {_age(r['started'])}s ago"
    return "STOPPED", f"process {r['pid']} is gone and never wrote a verdict: it was killed or the machine slept"


def describe(folder: Path) -> str:
    word, why = state(folder)
    out = [f"{folder.name}: {word}", f"  {why}"]
    cur = folder / "logs" / "current.json"
    if cur.exists():
        c = json.loads(cur.read_text())
        age = _age(c["updated"]) if "updated" in c else None
        line = f"  model call {c.get('call')} ({c.get('step')}): {c.get('state')}"
        if c.get("response_id"):
            line += f"; Muse says `{c.get('muse_status')}` after {c.get('polls')} poll(s), response {c['response_id']}"
        if age is not None:
            line += f"; last update {age}s ago"
        out.append(line)
        if word == "RUNNING" and age is not None and age > 240 and str(c.get("state", "")).startswith("waiting"):
            out.append("  WARNING: a call has made no progress for over 4 minutes; it may be stuck")
    log = folder / "logs" / "calls.jsonl"
    if log.exists():
        rows = [json.loads(l) for l in log.read_text().splitlines()]
        out.append(f"  {len(rows)} model call(s) finished" + (f"; the last: {rows[-1]['step']} in {rows[-1]['seconds']}s" + (f", ERROR {rows[-1]['error'][:80]}" if rows[-1]['error'] else "") if rows else ""))
    have = [n for n in ("variation.json", "spec.json", "scenarios.json", "CODER_PROMPT.md", "game.json", "report.json", "VERIFIED.md") if (folder / n).exists()]
    out.append("  files: " + (", ".join(have) or "none yet"))
    return "\n".join(out)
