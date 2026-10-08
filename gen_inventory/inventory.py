"""The inventory: a directory of records, one JSON file per game.

Plain files on purpose. The inventory is reviewed by reading it, diffed by git,
and edited by hand when a gate is wrong; none of that survives a database.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from gen_inventory import gates, index
from gen_inventory.schema import GATED, Record, RecordError, from_dict

DEFAULT_DIR = Path(__file__).parent / "data" / "inventory"
DEFAULT_INDEX = Path(__file__).parent / "INDEX.md"


class Inventory:
    def __init__(self, root: Path = DEFAULT_DIR, manifest: dict | None = None):
        self.root = Path(root)
        self.index_path = DEFAULT_INDEX if self.root == DEFAULT_DIR else self.root / "INDEX.md"
        self.root.mkdir(parents=True, exist_ok=True)
        self.manifest = manifest or gates.load_manifest()

    # -- storage -------------------------------------------------------

    def _path(self, game_id: str) -> Path:
        return self.root / f"{game_id}.json"

    def all(self) -> list[Record]:
        out = []
        for path in sorted(self.root.glob("*.json")):
            if path.name == "INDEX.json":  # the index lives beside the records in a test directory
                continue
            try:
                out.append(from_dict(json.loads(path.read_text())))
            except (RecordError, json.JSONDecodeError, TypeError) as exc:
                raise RecordError(f"{path.name}: {exc}") from exc
        return out

    def get(self, game_id: str) -> Record:
        path = self._path(game_id)
        if not path.exists():
            raise KeyError(game_id)
        return from_dict(json.loads(path.read_text()))

    def save(self, rec: Record) -> None:
        self._path(rec.id).write_text(json.dumps(rec.to_dict(), indent=2) + "\n")
        self.write_index()

    def write_index(self) -> None:
        records = self.all()
        self.index_path.write_text(index.render(records))
        self.index_path.with_suffix(".json").write_text(index.render_json(records))

    def add(self, rec: Record) -> Record:
        """Store a new candidate and run it through the gates."""
        if self._path(rec.id).exists():
            raise RecordError(f"{rec.id} is already in the inventory")
        self.save(rec)
        return self.check(rec.id)

    # -- the gates -----------------------------------------------------

    def check(self, game_id: str) -> Record:
        rec = gates.check(self.get(game_id), self.all(), self.manifest)
        self.save(rec)
        return rec

    def check_all(self) -> list[Record]:
        """Check every game still on the gates, in an order a twin cannot depend on.

        One at a time and saved as it goes, so a game checked later sees the
        verdicts of the games checked before it.
        """
        todo = [r.id for r in self.all() if r.status in GATED]
        return [self.check(i) for i in todo]

    def recheck(self) -> list[tuple[str, str, str]]:
        """Re-run the gates after the engine or the manifest changed.

        Returns (id, before, after) for each game whose status moved, which is
        how a gap closing shows up: its blocked games become ready.
        """
        before = {r.id: r.status for r in self.all() if r.status in GATED}
        self.check_all()
        after = {r.id: r.status for r in self.all()}
        return [(i, b, after[i]) for i, b in before.items() if after[i] != b]

    # -- what the inventory says ---------------------------------------

    def by_status(self) -> dict[str, list[Record]]:
        out: dict[str, list[Record]] = {}
        for r in self.all():
            out.setdefault(r.status, []).append(r)
        return out

    def families(self) -> dict[str, list[Record]]:
        out: dict[str, list[Record]] = {}
        for r in self.all():
            if r.status in ("duplicate", "incomplete", "rejected"):
                continue
            out.setdefault(r.family_key, []).append(r)
        return out

    def gaps(self) -> Counter:
        """Which engine limits block how many games: the ranked list of work."""
        c: Counter = Counter()
        for r in self.all():
            if r.status == "blocked":
                c.update(r.blocked_by)
        return c

    def workarounds(self) -> Counter:
        c: Counter = Counter()
        for r in self.all():
            if r.status in ("ready", "ported", "evaluated", "accepted"):
                c.update(r.workarounds)
        return c

    def queue(self) -> list[Record]:
        """Ready games, best first: what step 2 should take next.

        A game whose mechanic is already in the library waits until every new
        mechanic has had a turn. Within each group the crawl's rating comes
        first, then the value the gates computed.
        """
        ready = [r for r in self.all() if r.status == "ready"]
        taken = {r.family_key for r in self.all() if r.status in ("ported", "evaluated", "accepted")}
        return sorted(ready, key=lambda r: (r.family_key in taken, -(r.rating or 0), -(r.value or 0), r.id))
