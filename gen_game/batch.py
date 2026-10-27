"""Convert many games side by side, play-test the ones that come out whole, and stop the line when a failure repeats.

    python -m gen_game batch --name 2026-10-27-forty --ids-file ids.txt --jobs 8 --plays 3

Each game runs in its own processes: `convert --judge`, then, when it comes out ready for review, `install` and `simulate`
(which ends with the reasoning check). One game's trouble never stops another.

The processes run a PINNED copy of the code: the committed tree of one commit, under `.pins/<commit>/`, with the data folders
linked back to this checkout so every result lands where it belongs. The batch folder's CODE file names the copy and is read
before each game starts, so a fix is deployed by pinning its commit (`--pin <commit> --pin-only`): games already running finish
on the code they started with, and the games started after it use the fix. Editing this checkout never reaches a running game.

When the same failure (outcome and wording, numbers and the game's name aside) ends `stop_after` games, no new game is started
and the running ones finish. Outcomes the pipeline means (ready for review, dropped, a platform limit) never stop the line. Run
the batch again with the same name to resume: games that finished are kept, the rest run again. BATCH.md is rewritten after
every game.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

#: Kept in this checkout and linked into every pinned copy: the games, the inventory, the platform's library.
SHARED = ("gen_game/data", "gen_inventory/data", "xcolos/games/library")
#: Outcomes the pipeline means. They never stop the line, and a game that has one is not run again on resume.
FINISHED = ("ready_for_review", "dropped", "platform_limit", "needs_engine")
#: The play-test's players: Claude for every game, so plays compare across games and the reasoning check has the players' reasons
#: to read. (`muse|gateway` would make the players depend on whether Muse can be reached that hour.)
PLAYERS = "gateway"

Runner = Callable[[list[str], Path, Path], int]


def pin(repo: Path, commit: str, pins: Path) -> Path:
    """The committed code of `commit` in its own folder, with the shared data linked back to `repo`. Reused if already pinned."""
    sha = subprocess.run(["git", "-C", str(repo), "rev-parse", commit], capture_output=True, text=True, check=True).stdout.strip()
    dest = pins / sha[:10]
    if dest.exists():
        return dest
    tmp = pins / f".{sha[:10]}.{os.getpid()}.tmp"
    tmp.mkdir(parents=True)
    tree = subprocess.run(["git", "-C", str(repo), "archive", sha, "--", ".", *(f":(exclude){rel}" for rel in SHARED)],
                          capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tmp)], input=tree, check=True)
    for rel in SHARED:
        link = tmp / rel
        if link.is_symlink() or link.is_file():
            link.unlink()
        elif link.exists():
            shutil.rmtree(link)
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to((repo / rel).resolve())
    os.replace(tmp, dest)
    return dest


def run_logged(cmd: list[str], cwd: Path, log: Path) -> int:
    """One step of one game, its output appended to the game's log, with the pinned code first on the path."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    with open(log, "a") as out:
        out.write(f"\n$ {' '.join(cmd[2:])}   (code {cwd.name}, {time.strftime('%H:%M:%S')})\n")
        out.flush()
        return subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, env=env).returncode


def _last_error(log: Path) -> str:
    lines = [x.strip() for x in log.read_text().splitlines() if x.strip()] if log.exists() else []
    errors = [x for x in lines if re.match(r"^[\w.]*(Error|Exception|Exit)\b.*:", x) or x.startswith("error:")]
    return (errors or lines or ["no output"])[-1][:300]


def _fresh_json(path: Path, since: float) -> dict | None:
    """The file's content if it was written during this run; an older one belongs to an earlier run."""
    if not path.exists() or path.stat().st_mtime < since - 1:
        return None
    try:
        return json.loads(path.read_text())
    except ValueError:
        return None


def run_game(game_id: str, code: Path, python: str, plays: int, log: Path, runner: Runner = run_logged) -> dict:
    """Convert one game and, when it comes out ready for review, install it and play it (simulate ends with the reasoning check)."""
    start = time.time()
    folder = code / "gen_game" / "data" / "games" / game_id
    gen = [python, "-m", "gen_game"]
    row = {"id": game_id, "code": code.name, "log": str(log), "plays": None, "reasoning": None}
    runner(gen + ["convert", game_id, "--judge"], code, log)
    status = _fresh_json(folder / "logs" / "run.json", start)
    if status and status.get("state") == "finished":
        row["outcome"], row["detail"] = status["verdict"], status.get("detail", "")
    else:
        row["outcome"], row["detail"] = "crashed", (status or {}).get("detail") or _last_error(log)
    if row["outcome"] == "ready_for_review" and plays > 0:
        play_game(row, code, python, plays, log, runner)
    row["minutes"] = round((time.time() - start) / 60, 1)
    return row


def play_game(row: dict, code: Path, python: str, plays: int, log: Path, runner: Runner = run_logged) -> dict:
    """Install a game that came out ready and play it; `simulate` ends with the reasoning check. Fills in the row's plays and reasoning."""
    game_id, gen = row["id"], [python, "-m", "gen_game"]
    folder = code / "gen_game" / "data" / "games" / game_id
    row.update(code=code.name, plays=None, reasoning=None)
    runner(gen + ["uninstall", game_id], code, log)  # an earlier version of this game, if any
    if runner(gen + ["install", game_id], code, log) != 0:
        row["outcome"], row["detail"] = "install_failed", _last_error(log)
        return row
    began = time.time()
    rc = runner(gen + ["simulate", game_id, "--players", PLAYERS, "--matches", str(plays), "--seed", "1"], code, log)
    sims = [s for s in (_fresh_json(p, began) for p in sorted((folder / "sim").glob("*.json")) if not p.name.endswith(".review.json")) if s]
    ended = [s for s in sims if (s.get("snapshot") or {}).get("status") == "ended"]
    row["plays"] = {"of": plays, "ended": len(ended), "results": dict(Counter(str(s["snapshot"].get("winner")) for s in ended)), "players": PLAYERS}
    if rc != 0 or len(ended) < plays:
        row["outcome"], row["detail"] = "play_failed", f"{len(ended)} of {plays} plays ended; " + _last_error(log)
    check = _fresh_json(folder / "reasoning.json", began)
    if check and "verdict" in check:
        row["reasoning"] = {"verdict": check["verdict"], "scores": ", ".join(
            f"{a} {'-' if (check.get(a) or {}).get('score') is None else check[a]['score']}" for a in ("reasoning", "planning", "luck"))}
    return row


def signature(row: dict) -> str:
    """The failure, with numbers and the game's own name taken out, so the same failure in two games reads the same."""
    text = re.sub(rf"\b{re.escape(row['id'].lower())}\b", "<game>", str(row.get("detail", "")).lower())
    return f"{row['outcome']}: {re.sub(r'[0-9]+', '#', text)[:80]}"


def should_stop(rows: list[dict], n: int) -> str | None:
    """The failure that has ended `n` games, if one has."""
    counts = Counter(signature(r) for r in rows if r["outcome"] not in FINISHED)
    if not counts:
        return None
    sig, count = counts.most_common(1)[0]
    return sig if count >= n else None


def render(name: str, ids: list[str], rows: list[dict], stopped: str | None) -> str:
    done = {r["id"] for r in rows}
    counts = Counter(r["outcome"] for r in rows)
    out = [f"# Batch {name}", "", f"{len(rows)} of {len(ids)} games done: " + (", ".join(f"{k} {v}" for k, v in counts.most_common()) or "none yet"), ""]
    if stopped:
        out += [f"**Stopped the line:** the same failure ended several games: `{stopped}`. No new game was started. Fix it, pin the fix "
                "(`--pin <commit> --pin-only`), and run the batch again with the same name: only the games that did not finish run.", ""]
    out += ["| game | outcome | detail | plays | reasoning | minutes |", "|---|---|---|---|---|---|"]
    for r in rows:
        plays = f"{r['plays']['ended']}/{r['plays']['of']}: {r['plays']['results']}" if r.get("plays") else ""
        reasoning = f"{r['reasoning']['verdict']} ({r['reasoning']['scores']})" if r.get("reasoning") else ""
        detail = str(r.get("detail", "")).replace("|", "/").replace("\n", " ")[:160]
        out.append(f"| {r['id']} | {r['outcome']} | {detail} | {plays} | {reasoning} | {r.get('minutes', '')} |")
    waiting = [i for i in ids if i not in done]
    if waiting:
        out += ["", ("Not started: " if stopped else "Waiting or running: ") + ", ".join(waiting)]
    return "\n".join(out) + "\n"


def _save(out: Path, ids: list[str], rows: list[dict], stopped: str | None) -> None:
    (out / "batch.json").write_text(json.dumps({"ids": ids, "rows": rows, "stopped": stopped}, indent=1) + "\n")
    (out / "BATCH.md").write_text(render(out.name, ids, rows, stopped))


def run_batch(ids: list[str], out: Path, jobs: int, plays: int, stop_after: int, python: str, runner: Runner = run_logged,
              say: Callable[[str], None] = print, replay: bool = False) -> list[dict]:
    """Run the games `jobs` at a time on the code the batch's CODE file names; keep the games that finished in an earlier run.
    With `replay`, a game that came out ready on older code is played again on the current code (not converted again)."""
    path = out / "batch.json"
    earlier = {r["id"]: r for r in json.loads(path.read_text())["rows"]} if path.exists() else {}
    pinned = Path((out / "CODE").read_text().strip()).name
    stale = {i for i in ids if replay and i in earlier and earlier[i]["outcome"] == "ready_for_review" and earlier[i].get("code") != pinned}
    rows = [earlier[i] for i in ids if i in earlier and earlier[i]["outcome"] in FINISHED and i not in stale]
    todo = [i for i in ids if not (i in earlier and earlier[i]["outcome"] in FINISHED) or i in stale]
    (out / "logs").mkdir(parents=True, exist_ok=True)
    lock, state = threading.Lock(), {"stopped": None}
    _save(out, ids, rows, None)

    def one(game_id: str) -> None:
        if state["stopped"]:
            return
        code = Path((out / "CODE").read_text().strip())  # read now, so a newly pinned fix reaches the games that start after it
        say(f"{game_id}: started on {code.name}")
        log = out / "logs" / f"{game_id}.log"
        try:
            row = play_game(dict(earlier[game_id]), code, python, plays, log, runner) if game_id in stale else run_game(game_id, code, python, plays, log, runner)
        except Exception as exc:  # noqa: BLE001 - the runner itself failing is that game's failure, not the batch's
            row = {"id": game_id, "code": code.name, "log": str(log), "outcome": "crashed", "detail": f"the batch could not run it: {exc}"[:300],
                   "plays": None, "reasoning": None}
        with lock:
            rows.append(row)
            if not state["stopped"]:
                state["stopped"] = should_stop(rows, stop_after)
                if state["stopped"]:
                    say(f"stopping the line: {state['stopped']}")
            _save(out, ids, rows, state["stopped"])
        say(f"{game_id}: {row['outcome']}" + (f" ({row['detail'][:120]})" if row.get("detail") else ""))

    with ThreadPoolExecutor(max_workers=max(1, jobs)) as pool:
        list(pool.map(one, todo))
    _save(out, ids, rows, state["stopped"])
    return rows
