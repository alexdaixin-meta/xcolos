"""One record per game.

The duplicate gate stops a game that comes back under a name, an alias or a
rules text already here. It cannot stop the same game under a name nobody listed:
Perudo filed from one page and Dudo from another. Two passes keep the inventory
to one record per game:

    prune   records the duplicate gate stopped are removed
    find    a model names the game each record is an instance of, a chunk of
            the inventory at a time (Blackout and Up and Down the River are both
            Oh Hell); records given one name are then put to the model again,
            alone, to confirm they are one game. In each confirmed group the
            game furthest along is kept and takes the others' names as aliases,
            so a later page under one of those names is dropped before it is
            read; the others are removed

The whole inventory is never sent at once: a long prompt is cut off by the
server, and a chunk of sixty lines is not.

A removed record's page stays in the crawl log, marked `duplicate` with the game
it repeats, so it is never read again.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Protocol

from gen_inventory.crawl import CrawlLog, Lead, first_json
from gen_inventory.inventory import Inventory
from gen_inventory.schema import LIFECYCLE, Record, slug


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You check an inventory of games for duplicates. Each line is one record:
  id | name | other names | what the game is

Two records are duplicates when they are the same game: the same rules under another name, or an edition
whose rules differ only in small details. Records that merely share a mechanic, a family or a theme are NOT
duplicates: two different poker variants, two different trick-taking games, two different auctions, a game
and a variant whose changed rule changes how it is played.

Reply with one JSON object and nothing else:
  {"same": [["<id>", "<id>"], ...]}
one list per group of duplicates, the ids exactly as given; an empty list if there are none."""


NAMING = """You name games. Each line is one record:
  id | name | other names | what the game is

For each record give the game it is an instance of: that game's most common name, in English. Give the SAME
name to records that are one game under different names, or an edition whose rules differ only in small
details (Oh Hell, Blackout and Up and Down the River are all "Oh Hell"). A genuinely different game keeps its
own name even in the same family (Texas hold 'em and Omaha hold 'em are different games).

Reply with one JSON object and nothing else: {"names": {"<id>": "<game>", ...}}, with every id given."""

#: Records named in one call. A longer prompt is cut off by the server.
CHUNK = 60


def _remove(inv: Inventory, log: CrawlLog, rec: Record, of: str) -> None:
    inv.remove(rec.id)
    url = rec.source.get("url")
    if url and url in log.entries:
        log.write(Lead(log.entries[url]["title"], url, "", log.entries[url].get("via", "")), "duplicate", of)


def prune(inv: Inventory, log: CrawlLog) -> list[tuple[str, str]]:
    """Remove every record the duplicate gate stopped. Returns (removed, original)."""
    out = []
    for rec in inv.all():
        if rec.status == "duplicate":
            _remove(inv, log, rec, rec.duplicate_of or "")
            out.append((rec.id, rec.duplicate_of or ""))
    return out


def lines(records: list[Record]) -> str:
    rows = sorted(records, key=lambda r: r.name.lower())
    return "\n".join(f"{r.id} | {r.name} | {', '.join(r.aliases) or '-'} | {r.summary}" for r in rows)


def judge(completion: Completion, records: list[Record], repairs: int = 1) -> list[list[str]]:
    """Groups of ids that a model says are one game. Ids it made up are dropped."""
    ids = {r.id for r in records}
    ask = "Inventory:\n" + lines(records)
    for _ in range(repairs + 1):
        try:
            data = first_json(completion.complete(ask, system=SYSTEM))
        except ValueError as exc:
            ask += f"\n\nYour previous reply was refused: {exc}\nReply again with the JSON object only."
            continue
        groups = []
        for group in data.get("same") or []:
            if isinstance(group, list):
                kept = list(dict.fromkeys(g for g in group if isinstance(g, str) and g in ids))
                if len(kept) >= 2:
                    groups.append(kept)
        return groups
    raise ValueError("the model gave no usable answer")


def canonical(completion: Completion, records: list[Record], chunk: int = CHUNK, repairs: int = 1) -> dict[str, str]:
    """id -> the game a model says the record is an instance of, a chunk at a
    time. A chunk with no usable answer names nothing."""
    out: dict[str, str] = {}
    rows = sorted(records, key=lambda r: r.name.lower())
    for start in range(0, len(rows), chunk):
        part = rows[start : start + chunk]
        ids = {r.id for r in part}
        ask = "Records:\n" + lines(part)
        for _ in range(repairs + 1):
            try:
                data = first_json(completion.complete(ask, system=NAMING))
            except ValueError as exc:
                ask += f"\n\nYour previous reply was refused: {exc}\nReply again with the JSON object only."
                continue
            named = data.get("names")
            if isinstance(named, dict):
                out.update({i: n for i, n in named.items() if i in ids and isinstance(n, str) and slug(n)})
            break
    return out


def find(completion: Completion, records: list[Record]) -> tuple[list[list[str]], dict[str, str]]:
    """Groups of ids that are one game: given one name by `canonical`, then
    confirmed by `judge` with nothing else in the prompt. Also returns the names
    `canonical` gave, by id."""
    names = canonical(completion, records)
    by_name: dict[str, list[str]] = {}
    for i, n in names.items():
        by_name.setdefault(slug(n), []).append(i)
    by_id = {r.id: r for r in records}
    out = []
    for ids in by_name.values():
        if len(ids) > 1:
            out += judge(completion, [by_id[i] for i in sorted(ids)])
    return out, names


def _keeper(group: list[Record], name: str = "") -> Record:
    """The game furthest along: a ported one, then a ready one, then a blocked one;
    then the one filed under the name the game goes by; then the better rating;
    the id breaks a tie."""
    stage = {**{s: 0 for s in LIFECYCLE}, "ready": 1, "blocked": 2}
    return min(group, key=lambda r: (stage.get(r.status, 3), slug(r.name) != slug(name), -(r.rating or 0), r.id))


def merge(inv: Inventory, log: CrawlLog, groups: list[list[str]],
          names: dict[str, str] | None = None) -> list[tuple[str, list[str]]]:
    """Keep one game per group. The kept game takes the others' names as aliases,
    and the name the group's game goes by (`names`, from `canonical`) if it is
    not one of them, so a later page under any of them is known before it is
    read. Returns (kept, removed) per group that changed."""
    out = []
    for group in groups:
        recs = []
        for i in group:
            try:
                recs.append(inv.get(i))
            except KeyError:  # removed by an earlier group
                continue
        if len(recs) < 2:
            continue
        keep = _keeper(recs, next((names[r.id] for r in recs if names and r.id in names), ""))
        others = [r for r in recs if r.id != keep.id]
        mine = {slug(n) for n in [keep.name, *keep.aliases]}
        aliases = list(keep.aliases)
        for name in [r.name for r in others] + [names[r.id] for r in recs if names and r.id in names]:
            if slug(name) not in mine:  # once each, however it is spelled
                aliases.append(name)
                mine.add(slug(name))
        inv.save(replace(keep, aliases=aliases))
        for r in others:
            _remove(inv, log, r, keep.id)
        inv.check(keep.id)
        out.append((keep.id, [r.id for r in others]))
    return out
