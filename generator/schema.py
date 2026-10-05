"""The inventory record: one candidate game, as data.

A record says what a game is, in a fixed vocabulary, and where it stands. The
gates read these fields and nothing else, so a game is judged on what was
written down about it and never on a model's mood at the time.

Like the game loader, `from_dict` refuses a key it does not know: a misspelled
field that is silently ignored is a gate that silently passes.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import MISSING, asdict, dataclass, field, fields
from typing import Any

#: Where a game can stand. The first group is what the gates assign; the second
#: is the lifecycle the later pipeline steps assign, and a gate never touches it.
GATED = ("candidate", "incomplete", "rejected", "duplicate", "blocked", "ready")
LIFECYCLE = ("ported", "evaluated", "accepted")
STATUSES = GATED + LIFECYCLE

TURNS = ("sequential", "simultaneous", "mixed")
HIDDEN = ("hands", "roles", "private_values", "signals")
RANDOMNESS = ("none", "deal", "dice", "both")
COMMUNICATION = ("none", "public", "private", "both")
ENDINGS = ("fixed_rounds", "threshold", "elimination", "goal", "open")
OUTCOMES = ("win_lose", "score", "rank")
CONTAMINATION = ("famous", "known", "obscure")

#: What a game may train. A game with none of these has no reason to be here.
SKILLS = (
    "hidden_state_inference",
    "planning",
    "opponent_modeling",
    "negotiation",
    "bluffing",
    "resource_allocation",
    "counterfactual",
)

#: Rules are not copyrightable but their wording is, so the text in a record is
#: a paraphrase and the licence says what it was paraphrased from.
#:   original      written for this project
#:   public_domain the source is out of copyright
#:   cc0, cc_by    the source's licence allows reuse
#:   rules_only    the source's wording is not free; only the mechanics were kept
LICENCES = ("original", "public_domain", "cc0", "cc_by", "rules_only")

MIN_RULES_WORDS = 40
MAX_SUMMARY = 140


class RecordError(ValueError):
    """A record that cannot be read, as opposed to one that is merely weak."""


@dataclass
class Record:
    id: str
    name: str
    #: One line, for the index: what the game is, not how it is played.
    summary: str
    rules_text: str
    licence: str
    source: dict[str, str]
    players_min: int
    players_max: int
    turns: str
    randomness: str
    communication: str
    ending: str
    outcome: str
    aliases: list[str] = field(default_factory=list)
    contamination: str = "known"
    hidden: list[str] = field(default_factory=list)
    needs: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    #: The outcome cannot be computed, only judged. Allowed, but kept out of the
    #: RL set by default, because a judge's verdict is noisy and costs a call.
    judged: bool = False
    #: Things the game needs that the manifest has no word for, in the author's
    #: own words. Each blocks the game and shows up in the gap census, because a
    #: need nobody has named yet is exactly the engine work worth knowing about.
    unmapped: list[str] = field(default_factory=list)
    value_override: int | None = None
    #: 1-5 fit with the platform, judged from the title and opening text before
    #: the game was read in full. Set by the crawl, never by the model that
    #: extracts the record. A hint for ordering; the gates are what decide.
    rating: int | None = None
    rating_reason: str = ""

    # Everything below is written by the gates, never by the author.
    status: str = "candidate"
    reasons: list[str] = field(default_factory=list)
    blocked_by: list[str] = field(default_factory=list)
    workarounds: list[str] = field(default_factory=list)
    family: str | None = None
    duplicate_of: str | None = None
    value: int | None = None
    reward: str | None = None
    checked_with: int | None = None
    #: Where the ported game lives, once it has been.
    port: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def family_key(self) -> str:
        return self.family or self.id


_FIELD_NAMES = {f.name for f in fields(Record)}
_REQUIRED = [
    f.name
    for f in fields(Record)
    if f.default is MISSING and f.default_factory is MISSING
]


def from_dict(data: dict[str, Any]) -> Record:
    if not isinstance(data, dict):
        raise RecordError("a record is an object")
    unknown = sorted(set(data) - _FIELD_NAMES)
    if unknown:
        raise RecordError(f"unknown key(s): {', '.join(unknown)}")
    missing = [k for k in _REQUIRED if k not in data]
    if missing:
        raise RecordError(f"missing key(s): {', '.join(missing)}")
    return Record(**data)


def problems(rec: Record, vocabulary: set[str]) -> list[str]:
    """Everything wrong with a record that a person could fix by editing it."""
    out: list[str] = []

    if not re.fullmatch(r"[a-z][a-z0-9_]*", rec.id):
        out.append("id must be lowercase letters, digits and underscores")
    if not rec.name.strip():
        out.append("name is empty")
    if not rec.summary.strip():
        out.append("summary is empty; the index needs one line")
    elif len(rec.summary) > MAX_SUMMARY or "\n" in rec.summary:
        out.append(f"summary must be one line of at most {MAX_SUMMARY} characters")
    if len(rec.rules_text.split()) < MIN_RULES_WORDS:
        out.append(f"rules_text under {MIN_RULES_WORDS} words; not playable from it")
    if not rec.source.get("kind") or not (rec.source.get("url") or rec.source.get("ref")):
        out.append("source needs a kind and a url or ref")
    if not (1 <= rec.players_min <= rec.players_max):
        out.append("players_min..players_max is not a range")

    for name, value, allowed in (
        ("turns", rec.turns, TURNS),
        ("randomness", rec.randomness, RANDOMNESS),
        ("communication", rec.communication, COMMUNICATION),
        ("ending", rec.ending, ENDINGS),
        ("outcome", rec.outcome, OUTCOMES),
        ("contamination", rec.contamination, CONTAMINATION),
    ):
        if value not in allowed:
            out.append(f"{name} {value!r} is not one of {', '.join(allowed)}")
    for name, values, allowed in (
        ("hidden", rec.hidden, HIDDEN),
        ("skills", rec.skills, SKILLS),
        ("needs", rec.needs, tuple(sorted(vocabulary))),
    ):
        bad = sorted(set(values) - set(allowed))
        if bad:
            out.append(f"{name} has unknown value(s): {', '.join(bad)}")
    if not rec.skills:
        out.append("skills is empty; say what the game trains")
    return out


# ----------------------------------------------------------------------
# What identifies a game, and what only resembles one
# ----------------------------------------------------------------------


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def names(rec: Record) -> set[str]:
    return {slug(n) for n in [rec.name, *rec.aliases] if slug(n)}


def text_hash(rec: Record) -> str:
    words = re.sub(r"\s+", " ", rec.rules_text.strip().lower())
    return hashlib.sha1(words.encode()).hexdigest()


def fingerprint(rec: Record) -> tuple:
    """What two games share when they are the same mechanic in different clothes.

    Players are bucketed, because a game for 2-4 and a game for 2-5 are not
    different games. Theme, name and numbers are left out on purpose.
    """
    lo = "two" if rec.players_max <= 2 else "few" if rec.players_max <= 6 else "many"
    return (
        lo,
        rec.turns,
        tuple(sorted(rec.hidden)),
        rec.randomness,
        rec.communication,
        rec.ending,
        rec.outcome,
    )
