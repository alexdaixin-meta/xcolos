"""A cheap first look: how well might this game fit the platform, from 1 to 5?

The rater sees a title and the opening of its page, a few hundred characters,
and a batch of games at a time. It is far cheaper than extracting a record,
which reads the whole page, so the crawl rates everything it finds and extracts
only what rates high. The rating is a hint for what to read first. It decides
nothing: the gates still judge every game that is extracted.

The scale is anchored in what the platform can and cannot do, taken from the
capability manifest, because "suitable for our platform" with no anchor drifts.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Protocol

from generator.crawl import Lead, first_json

BATCH = 10
SNIPPET_CHARS = 500


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


@dataclass(frozen=True)
class Rating:
    rating: int
    reason: str


def system_prompt(manifest: dict) -> str:
    can = [k for k, v in manifest["needs"].items() if v["verdict"] in ("ok", "workaround")]
    cannot = [f"{k} ({v['note']})" for k, v in manifest["needs"].items() if v["verdict"] == "blocked"]
    out = [f"{k} ({v['note']})" for k, v in manifest["needs"].items() if v["verdict"] == "excluded"]
    return f"""You triage games for an engine that runs turn-based, text-only strategy games between language
models, for a player count of 2 to {manifest['max_players']}, and decides the winner by arithmetic on the moves.
The point of the games is to train strategic reasoning: hidden information, bluffing, bidding, bargaining,
opponent modelling, planning.

For each numbered item you get a page title and the opening of its page. Rate how well that game would fit:

  5  A specific playable game. Turn-based, strategic, with hidden information or bidding or bargaining or
     bluffing, an outcome that follows from the moves, short, and needing nothing from the "cannot" list.
  4  Specific, playable, clearly strategic, but one thing is doubtful or needs a workaround.
  3  Playable, but little reasoning (mostly luck, trivial or solved), or good but needs something on the
     "cannot" list.
  2  Playable but a poor fit: real-time or very long.
  1  Not a specific playable game: a concept, a list, an algorithm, a person, a company, a physical sport,
     a video game, or something that cannot be played turn by turn as text. Also 1: any game that depends
     on a spatial board (the "out of scope" list), whatever else it offers.

The engine can express: {', '.join(can)}.
The engine cannot express: {'; '.join(cannot)}.
Out of scope, never wanted: {'; '.join(out)}.

Judge from the text you are given. If it says too little to tell, rate 3. Reply with one JSON object and
nothing else:
  {{"ratings": [{{"i": 0, "rating": 4, "reason": "<at most 15 words>"}}, ...]}}
with one entry for every item."""


class Rater:
    def __init__(self, completion: Completion, manifest: dict, batch: int = BATCH, repairs: int = 1):
        self.completion = completion
        self.system = system_prompt(manifest)
        self.batch = batch
        self.repairs = repairs

    def rate(self, items: list[tuple[Lead, str]]) -> dict[str, Rating]:
        """Rate leads, a batch per call. Returns url -> Rating for the ones that
        got a valid answer; the rest are simply absent and will be asked again."""
        out: dict[str, Rating] = {}
        for start in range(0, len(items), self.batch):
            out.update(self._rate_batch(items[start : start + self.batch]))
        return out

    def _rate_batch(self, items: list[tuple[Lead, str]]) -> dict[str, Rating]:
        got: dict[int, Rating] = {}
        note = ""
        for _ in range(self.repairs + 1):
            pending = [i for i in range(len(items)) if i not in got]
            if not pending:
                break
            ask = "\n\n".join(
                f"[{i}] {items[i][0].title}\n{items[i][1].strip()[:SNIPPET_CHARS] or '(no text)'}" for i in pending
            ) + note
            try:
                data = first_json(self.completion.complete(ask, system=self.system))
            except ValueError as exc:
                note = f"\n\nYour previous reply was refused: {exc}\nReply again with the JSON object only."
                continue
            for entry in data.get("ratings") or []:
                try:
                    i, rating = entry["i"], entry["rating"]
                    if i in pending and isinstance(rating, int) and not isinstance(rating, bool) and 1 <= rating <= 5:
                        got[i] = Rating(rating, str(entry.get("reason", ""))[:120])
                except (KeyError, TypeError):
                    continue
            missing = [i for i in range(len(items)) if i not in got]
            note = f"\n\nYour previous reply left out or mis-rated items {missing}. Rate those, 1 to 5." if missing else ""
        return {items[i][0].url: r for i, r in got.items()}


def calibrate(rater: Rater, source, log, inventory) -> list[tuple[int, str]]:
    """Rate pages already read in full and pair each rating with what became of
    the page, in the index's words: `queued`, `blocked`, `dropped`, `needs work`
    or `covered`, or `skipped` when the page was not a game.

    This is how to learn whether a 5 is worth more than a 2 before trusting the
    rating to decide what is read.
    """
    from generator import index

    by_url = {r.source.get("url"): r for r in inventory.all()}
    leads, label = [], {}
    for e in log.entries.values():
        if e["outcome"] == "added" and e["url"] in by_url:
            label[e["url"]] = index.disposition(by_url[e["url"]])
        elif e["outcome"] == "skipped":
            label[e["url"]] = "skipped"
        else:
            continue
        leads.append(Lead(e["title"], e["url"], source.name))
    snippets = source.snippets(leads)
    rated = rater.rate([(lead, snippets.get(lead.url, "")) for lead in leads])
    return [(rated[u].rating, label[u]) for u in label if u in rated]


def crosstab(pairs: list[tuple[int, str]]) -> str:
    labels = ["queued", "blocked", "dropped", "needs work", "skipped"]
    counts = Counter(pairs)
    rows = [f"{'rating':<8}" + "".join(f"{lab:>12}" for lab in labels) + f"{'worth reading':>16}"]
    for r in range(5, 0, -1):
        n = [counts[(r, lab)] for lab in labels]
        total = sum(n)
        if not total:
            continue
        worth = (n[0] + n[1]) / total  # became a real game, whether or not the engine can run it yet
        rows.append(f"{r:<8}" + "".join(f"{x:>12}" for x in n) + f"{worth:>15.0%}")
    return "\n".join(rows)
