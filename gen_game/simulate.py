"""Play an installed game the way the console does, with a model in every seat, and keep everything.

It goes through the same server and the same HTTP calls the console makes: open a table whose seats are
`llm` seats with a model each, start it, wait for the end, then fetch the whole event log. The log holds
every message each seat was sent, every model call (the prompt it saw and the reply it gave), every fact the
table was told, and the result. Reviewing that log against the design is what says whether the game plays
as designed.

    python3 -m gen_game simulate coup --players claude,claude,claude
    python3 -m gen_game simulate coup --players muse                       # one model, at the game's suggested table size
    python3 -m gen_game simulate coup --players muse,muse,muse --matches 2
    python3 -m gen_game simulate coup --players offline,offline,offline        # checks the wiring, no model

The game must be installed (`install`) because the server plays what is in the library.
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

NAMES = ["Ada", "Blaise", "Curie", "Dirac", "Euler", "Fermat"]
DONE = ("ended", "abandoned", "error", "failed")


def _call(base: str, method: str, path: str, body: dict | None = None, timeout: float = 60):
    req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(),
                                 method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{method} {path}: {exc.code} {exc.read().decode('utf-8', 'replace')[:300]}") from None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _Server:
    """A server of our own on a free port, for the length of the run, unless one is given."""

    def __init__(self, url: str | None) -> None:
        self.proc = None
        if url:
            self.base = url.rstrip("/")
            return
        port = _free_port()
        self.base = f"http://127.0.0.1:{port}"
        self.proc = subprocess.Popen([sys.executable, "-m", "xcolos.web", "--port", str(port)],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                _call(self.base, "GET", "/api/games", timeout=2)
                return
            except Exception:  # noqa: BLE001 - not up yet
                time.sleep(0.5)
        self.stop()
        raise RuntimeError("the server did not start")

    def stop(self) -> None:
        if self.proc is not None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def fill_table(players: list[str], game: dict) -> list[str]:
    """One model named for a whole table is repeated up to the size the game plays best at; a list is used as given."""
    return players * (game.get("suggested_seats") or game["min_seats"]) if len(players) == 1 else players


def simulate(game_id: str, players: list[str], root: Path, matches: int = 1, seed: int = 1, server: str | None = None,
             timeout_s: int = 7200, log=print) -> list[dict]:
    """Play `matches` matches with `players[i]` (a model spec) in seat i + 1, and save each log. Returns a summary per match."""
    srv = _Server(server)
    out: list[dict] = []
    try:
        catalogue = {g["id"]: g for g in _call(srv.base, "GET", "/api/games")}
        if game_id not in catalogue:
            raise RuntimeError(f"{game_id!r} is not in the library: install it first (python3 -m gen_game install {game_id})")
        g = catalogue[game_id]
        players = fill_table(players, g)
        if not g["min_seats"] <= len(players) <= g["max_seats"]:
            raise RuntimeError(f"{g['name']} takes {g['min_seats']} to {g['max_seats']} seats, not {len(players)}")
        folder = root / game_id / "sim"
        folder.mkdir(parents=True, exist_ok=True)
        for n in range(matches):
            seats = [{"name": NAMES[i], "kind": "llm", "model": spec} for i, spec in enumerate(players)]
            table = _call(srv.base, "POST", "/api/matches", {"game": game_id, "seats": seats, "seed": seed + n, "pace_ms": 0})
            mid = table["match_id"]
            _call(srv.base, "POST", f"/api/matches/{mid}/start", {})
            log(f"match {n + 1}/{matches}: {mid} started, players {players}")
            started = time.time()
            snap = {}
            while time.time() - started < timeout_s:
                time.sleep(5)
                snap = next((m for m in _call(srv.base, "GET", "/api/matches") if m["match_id"] == mid), {})
                if snap.get("status") in DONE or snap.get("error"):
                    break
            else:
                log(f"match {mid} did not finish in {timeout_s}s")
            events = _call(srv.base, "GET", f"/api/matches/{mid}/events?since=0", timeout=120)
            path = folder / f"{mid}-seed{seed + n}.json"
            path.write_text(json.dumps({"game": game_id, "players": players, "seed": seed + n, "snapshot": snap,
                                        "events": events}, indent=1))
            calls = [r for r in events["records"] if r.get("type") == "model_call"]
            summary = {"match": mid, "file": str(path), "status": snap.get("status"), "winner": snap.get("winner"),
                       "rounds": snap.get("round"), "model_calls": len(calls),
                       "model_errors": sum(1 for r in calls if r.get("error")),
                       "seconds": round(time.time() - started)}
            log(json.dumps(summary))
            out.append(summary)
    finally:
        srv.stop()
    return out
