"""The gates a candidate passes, cheapest first, and the status each one assigns.

    1 completeness   can the game be played, and judged, from what is written?
    2 provenance     may the text be used?
    3 duplication    is it already here, or already here in other clothes?
    4 capability     can the engine express it?
    5 verifiability  can the outcome be computed? (tags the record, never stops it)
    6 value          is it worth porting?

Duplication comes before capability because a duplicate would otherwise cost a
model call for every copy. Each gate is a plain function of the record, the rest
of the inventory and the manifest, so a verdict can be reproduced and a gate can
be tested alone.
"""

from __future__ import annotations

import difflib
import json
from dataclasses import dataclass, replace
from pathlib import Path

from gen_inventory.schema import (
    LICENCES,
    LIFECYCLE,
    Record,
    fingerprint,
    names,
    problems,
    text_hash,
)

MANIFEST_PATH = Path(__file__).parent / "capabilities.json"

#: Two rules texts this alike are the same game worded twice.
SAME_TEXT = 0.85

#: A game that passed duplication, and so can be duplicated *of*. Among these,
#: a lifecycle game outranks a gated one, and then the lower id wins, so two
#: twins on a recheck cannot both call the other the original.
ESTABLISHED = ("ready", "blocked") + LIFECYCLE

_SEVERITY = {"ok": 0, "workaround": 1, "blocked": 2, "excluded": 3}


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    manifest = json.loads(Path(path).read_text())
    for need, entry in manifest["needs"].items():
        if entry["verdict"] not in _SEVERITY:
            raise ValueError(f"manifest: {need}: verdict {entry['verdict']!r}")
    return manifest


@dataclass(frozen=True)
class Verdict:
    status: str
    gate: str
    reasons: tuple[str, ...] = ()
    #: For a duplicate, the game it copies.
    of: str | None = None


def _rank(r: Record, seen: bool | None = None) -> tuple[int, str]:
    """Lifecycle games first, then games the gates have already seen, then new
    ones; the id only breaks a tie. A new arrival is therefore never the
    original of a game that was here before it."""
    seen = r.checked_with is not None if seen is None else seen
    return (0 if r.status in LIFECYCLE else 1 if seen else 2, r.id)


def completeness(rec: Record, manifest: dict) -> Verdict | None:
    found = problems(rec, set(manifest["needs"]))
    if found:
        return Verdict("incomplete", "completeness", tuple(found))
    return None


def provenance(rec: Record, manifest: dict) -> Verdict | None:
    if rec.licence not in LICENCES:
        return Verdict(
            "rejected",
            "provenance",
            (f"licence {rec.licence!r} is not one of {', '.join(LICENCES)}",),
        )
    return None


def duplication(rec: Record, others: list[Record], seen: bool) -> tuple[Verdict | None, str | None]:
    """Returns a duplicate verdict, or the family this game joins.

    `seen` is whether the gates had run on `rec` before this check.
    """
    mine = _rank(rec, seen)
    originals = [o for o in others if o.id != rec.id and o.status in ESTABLISHED and _rank(o) < mine]

    for o in originals:
        if names(rec) & names(o):
            return Verdict("duplicate", "duplication", (f"same name as {o.id}",), o.id), None
        if text_hash(rec) == text_hash(o):
            return Verdict("duplicate", "duplication", (f"same rules text as {o.id}",), o.id), None
        ratio = difflib.SequenceMatcher(None, rec.rules_text.lower().split(), o.rules_text.lower().split()).ratio()
        if ratio >= SAME_TEXT:
            return Verdict("duplicate", "duplication", (f"rules text {ratio:.0%} like {o.id}",), o.id), None

    for o in originals:
        if fingerprint(o) == fingerprint(rec):
            return None, o.family_key
    return None, None


def capability(rec: Record, manifest: dict) -> tuple[Verdict | None, list[str], list[str]]:
    """Returns a verdict if the game is rejected or blocked, plus the blockers and workarounds."""
    blocked: list[str] = []
    workarounds: list[str] = []
    reasons: list[str] = []

    # Out of scope by decision: not an engine gap, so it is dropped, not queued behind one.
    out = [n for n in rec.needs if manifest["needs"][n]["verdict"] == "excluded"]
    if out:
        return Verdict("rejected", "scope", tuple(f"{n}: {manifest['needs'][n]['note']}" for n in out)), [], []

    if rec.players_min > manifest["max_players"]:
        blocked.append("player_count")
        reasons.append(f"needs at least {rec.players_min} players; the engine's largest table is {manifest['max_players']}")

    for need in rec.needs:
        entry = manifest["needs"][need]
        if entry["verdict"] == "blocked":
            blocked.append(need)
            reasons.append(f"{need}: {entry['note']}")
        elif entry["verdict"] == "workaround":
            workarounds.append(need)

    for what in rec.unmapped:
        blocked.append(f"unmapped: {what}")
        reasons.append(f"needs something the manifest has no word for: {what}")

    if blocked:
        return Verdict("blocked", "capability", tuple(reasons)), blocked, workarounds
    return None, blocked, workarounds


def value(rec: Record, new_family: bool) -> int:
    """Skills trained, plus one for a family the library lacks, minus one for a
    famous game a model may simply remember. A person may override it."""
    if rec.value_override is not None:
        return rec.value_override
    return len(rec.skills) + (1 if new_family else 0) - (1 if rec.contamination == "famous" else 0)


def check(rec: Record, inventory: list[Record], manifest: dict) -> Record:
    """Run every gate and return the record as it now stands.

    A record past the gates (`ported` and later) is returned unchanged: its
    status belongs to the step that gave it.
    """
    if rec.status in LIFECYCLE:
        return rec
    if rec.dropped:  # decided against by a person or by gen_game: the gates do not revive it
        return replace(rec, status="rejected", reasons=[f"dropped: {rec.dropped}"], checked_with=manifest["version"])

    seen = rec.checked_with is not None
    base = replace(
        rec,
        status="candidate",
        reasons=[],
        blocked_by=[],
        workarounds=[],
        family=None,
        duplicate_of=None,
        value=None,
        reward=None,
        checked_with=manifest["version"],
    )

    def stop(v: Verdict, **extra) -> Record:
        return replace(base, status=v.status, reasons=[f"{v.gate}: {r}" for r in v.reasons], **extra)

    if (v := completeness(base, manifest)) or (v := provenance(base, manifest)):
        return stop(v)

    v, family = duplication(base, inventory, seen)
    if v:
        return stop(v, duplicate_of=v.of)

    v, blocked, workarounds = capability(base, manifest)
    reward = "judged" if base.judged else "verifiable"
    if v:
        return stop(v, family=family, blocked_by=blocked, workarounds=workarounds, reward=reward)

    score = value(base, new_family=family is None)
    if score <= 0:
        return replace(
            base,
            status="rejected",
            reasons=[f"value: score {score}; trains too little for its size or is too likely remembered"],
            family=family,
            workarounds=workarounds,
            value=score,
            reward=reward,
        )
    return replace(base, status="ready", family=family, workarounds=workarounds, value=score, reward=reward)

