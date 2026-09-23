"""The match log.

The log is the god view of one match: it holds every secret, and entitlement is
a field on each record rather than a filter applied to the file. It exists for
observation, debugging and analysis. It is not in the gameplay path, and nothing
in the runtime reads it back.

Because it is the only durable record, it has to be complete. Every state
change, every fact, every orchestrator request, every message sent to a seat and
every response returned from one is recorded here.

Record shape, consistent across every line:

    log_seq   monotonic, assigned by this class, unique per line
    ts        wall clock, recorded for humans and never read by the runtime
    category  the coarse bucket, see CATEGORIES
    type      the specific event within that bucket
    round     game round at the time of writing
    phase     game phase at the time of writing
    turn_seq  the turn in flight, 0 during setup
    ...       fields specific to the type
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

LOG_SCHEMA_VERSION = 2

#: The coarse buckets. Filtering a log by category is the first thing anyone
#: reading one wants to do, so the vocabulary is small and fixed.
CATEGORIES = (
    "setup",  # seats registered, roles assigned, zones and offices declared
    "process",  # phase and round transitions, termination
    "state",  # mutations to seats, globals, zones, offices
    "fact",  # something happened, with the audience entitled to know it
    "delivery",  # which facts were pushed to which seat
    "orchestrator",  # what the orchestrator asked for, and why
    "message",  # every envelope out to a seat, every response back
    "turn",  # the move record, one per turn, end to end
    "result",  # the final summary
)

#: Fields that differ between two identical runs and must be ignored when
#: comparing logs for determinism.
VOLATILE_FIELDS = ("ts",)


@dataclass
class MoveRecord:
    """One turn, end to end.

    What the seat was shown, what was asked of it, what it returned, every
    attempt through the failure ladder, and how it resolved.
    """

    turn_seq: int
    seat: int
    role: str | None
    delta_fact_seqs: list[int]
    action_schema: str
    legal_targets: list[Any]
    reason: str = ""
    attempts: list[dict[str, Any]] = field(default_factory=list)
    final_outcome: str = "ok"  # ok | repaired | defaulted
    degraded: bool = False
    action: dict[str, Any] | None = None
    rng_state_after: str = ""

    def to_fields(self) -> dict[str, Any]:
        return {
            # Its own number, not the counter's value when it was written.
            # Simultaneous turns are all opened before any is answered, so the
            # ambient counter labelled every answer in a batch identically.
            "turn_seq": self.turn_seq,
            "seat": self.seat,
            "role": self.role,
            "reason": self.reason,
            "shown_fact_seqs": self.delta_fact_seqs,
            "action_schema": self.action_schema,
            "legal_targets": self.legal_targets,
            "attempts": self.attempts,
            "outcome": self.final_outcome,
            "degraded": self.degraded,
            "action": self.action,
            "rng_state_after": self.rng_state_after,
        }


class MatchLog:
    """Append-only, structured, complete."""

    def __init__(self, match_id: str, path: Path | None = None) -> None:
        self.match_id = match_id
        self.path = path
        self.records: list[dict[str, Any]] = []
        self._handle = None
        self._context: Callable[[], dict[str, Any]] = lambda: {}

        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            self._handle = path.open("w", encoding="utf-8")

        self.record(
            "setup",
            "header",
            log_schema_version=LOG_SCHEMA_VERSION,
            match_id=match_id,
        )

    def bind_context(self, fn: Callable[[], dict[str, Any]]) -> None:
        """Supply round, phase and turn for every subsequent record."""
        self._context = fn

    # ------------------------------------------------------------------

    def record(self, category: str, type: str, **fields: Any) -> dict[str, Any]:
        if category not in CATEGORIES:
            raise ValueError(f"unknown log category {category!r}")
        rec: dict[str, Any] = {
            "log_seq": len(self.records),
            "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
            "category": category,
            "type": type,
        }
        rec.update(self._context())
        rec.update(fields)

        # A record that does not survive a round trip through its own file is
        # not a record. The usual cause is integer dict keys, which JSON turns
        # into strings, so the file and memory silently disagree.
        encoded = json.dumps(rec)
        if json.loads(encoded) != rec:
            raise ValueError(
                f"log record {category}/{type} does not survive a JSON round trip. "
                "Check for non-string dict keys or non-JSON values in the payload."
            )

        self.records.append(rec)
        if self._handle is not None:
            # Insertion order, not sorted: the leading fields are the ones a
            # human scanning the file needs first.
            self._handle.write(encoded + "\n")
            self._handle.flush()
        return rec

    def close(self) -> None:
        if self._handle is not None:
            self._handle.close()
            self._handle = None

    # ------------------------------------------------------------------
    # Reading
    # ------------------------------------------------------------------

    def where(
        self, category: str | None = None, type: str | None = None, **match: Any
    ) -> list[dict[str, Any]]:
        out = []
        for r in self.records:
            if category is not None and r.get("category") != category:
                continue
            if type is not None and r.get("type") != type:
                continue
            if any(r.get(k) != v for k, v in match.items()):
                continue
            out.append(r)
        return out

    def deliveries_to(self, seat: int) -> list[int]:
        """Fact sequence numbers actually pushed to one seat."""
        out: list[int] = []
        for r in self.where("delivery", seat=seat):
            out.extend(r.get("fact_seqs", []))
        return out

    def stable_records(self) -> list[dict[str, Any]]:
        """Records with wall-clock fields stripped, for comparing two runs."""
        return [
            {k: v for k, v in r.items() if k not in VOLATILE_FIELDS}
            for r in self.records
        ]

    @staticmethod
    def load(path: Path) -> list[dict[str, Any]]:
        with path.open(encoding="utf-8") as fh:
            return [json.loads(line) for line in fh if line.strip()]

    def counts(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in self.records:
            key = f"{r['category']}/{r['type']}"
            out[key] = out.get(key, 0) + 1
        return out


def validate_log(records: Iterable[dict[str, Any]]) -> list[str]:
    """Structural check. Returns a list of problems, empty when the log is sound."""
    problems: list[str] = []
    rows = list(records)

    seqs = [r.get("log_seq") for r in rows]
    if seqs != list(range(len(rows))):
        problems.append("log_seq is not contiguous and monotonic from zero")

    required = ("log_seq", "ts", "category", "type")
    for r in rows:
        missing = [f for f in required if f not in r]
        if missing:
            problems.append(f"log_seq {r.get('log_seq')}: missing {missing}")
        if r.get("category") not in CATEGORIES:
            problems.append(f"log_seq {r.get('log_seq')}: bad category {r.get('category')!r}")

    facts = [r for r in rows if r["category"] == "fact"]
    fact_seqs = [r["fact_seq"] for r in facts]
    if fact_seqs != list(range(len(facts))):
        problems.append("fact_seq is not contiguous and monotonic from zero")

    known = {r["fact_seq"] for r in facts}
    for r in rows:
        if r["category"] == "delivery":
            unknown = [s for s in r.get("fact_seqs", []) if s not in known]
            if unknown:
                problems.append(f"delivery references unknown facts {unknown}")

    if not any(r["category"] == "result" for r in rows):
        problems.append("log has no result record")

    return problems
