"""Find candidate games and put the ones worth keeping into the inventory.

    discover   a source lists leads: a title and a page
    pre-gate   drop what is plainly not a game, and what is already known
    extract    a model reads the page and fills a record in the fixed vocabulary
    admit      the inventory runs the gates and files it

Three things are decided by code and never by the model: where a game came from
(source and licence are facts about the page, not opinions), what the id is, and
whether a game is already here. The model fills only the mechanic fields, and a
reply that does not fit the vocabulary is sent back with the reason until it
does or the attempts run out.

Every lead's outcome is written to a log, so a rerun spends nothing on pages it
has already read.
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from gen_inventory import schema
from gen_inventory.inventory import Inventory
from gen_inventory.schema import Record, RecordError, from_dict, problems, slug

CONFIG_PATH = Path(__file__).parent / "crawl_sources.json"
LOG_PATH = Path(__file__).parent / "data" / "crawl_log.jsonl"
USER_AGENT = "xcolos-gen-inventory/0.1 (game inventory research)"
API = "https://en.wikipedia.org/w/api.php"


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


@dataclass(frozen=True)
class Lead:
    title: str
    url: str
    source: str
    #: What found it: `category:...` or `query:...`. The yield report keys on this.
    via: str = ""


# ----------------------------------------------------------------------
# Sources
# ----------------------------------------------------------------------


def http_get(url: str, timeout: float = 20, tries: int = 5) -> str:
    """GET with the politeness a public API asks for: wait out a 429 or 503,
    for as long as the server says, instead of failing the crawl."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - fixed https hosts
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 503) or attempt == tries:
                raise
            try:
                wait = float(exc.headers.get("Retry-After", ""))
            except ValueError:
                wait = 2.0 ** attempt
            time.sleep(min(wait, 60))
    raise AssertionError("unreachable")


class Wikipedia:
    """Leads from Wikipedia searches and categories; the page is its plain text.

    The text is CC BY-SA, and the model is told to paraphrase, so a record's
    licence is `rules_only`: the mechanics are kept and the wording is not.
    """

    name = "wikipedia"
    host = "en.wikipedia.org"
    licence = "rules_only"

    def __init__(self, config: dict, get: Callable[[str], str] = http_get, pause: float = 0.5):
        self.config = config
        self.get = get
        self.pause = pause
        self._exclude = [re.compile(p, re.I) for p in config.get("exclude_title", [])]

    def _api(self, **params) -> dict:
        time.sleep(self.pause)
        return json.loads(self.get(API + "?" + urllib.parse.urlencode({**params, "format": "json"})))

    def wanted(self, title: str) -> bool:
        return not any(p.search(title) for p in self._exclude)

    def discover(self, per_query: int = 10) -> list[Lead]:
        found: list[tuple[str, str]] = []
        for cat in self.config.get("categories", []):
            data = self._api(action="query", list="categorymembers", cmtitle=cat, cmlimit=500, cmtype="page")
            found += [(m["title"], f"category:{cat}") for m in data["query"]["categorymembers"]]
        for q in self.config.get("queries", []):
            data = self._api(action="query", list="search", srsearch=q, srlimit=per_query)
            found += [(r["title"], f"query:{q}") for r in data["query"]["search"]]

        seen: set[str] = set()
        leads = []
        for t, via in found:
            if t in seen or not self.wanted(t):
                continue
            seen.add(t)
            leads.append(Lead(t, "https://en.wikipedia.org/wiki/" + urllib.parse.quote(t.replace(" ", "_")), self.name, via))
        return leads

    def snippets(self, leads: list[Lead], chars: int = 500) -> dict[str, str]:
        """The opening of each lead's page, twenty to a request. url -> text."""
        out: dict[str, str] = {}
        for start in range(0, len(leads), 20):
            chunk = leads[start : start + 20]
            data = self._api(action="query", prop="extracts", exintro=1, explaintext=1, exchars=chars,
                             exlimit=20, redirects=1, titles="|".join(l.title for l in chunk))
            query = data["query"]
            # a title may come back normalised or redirected; follow it to the page
            moved = {m["from"]: m["to"] for m in query.get("normalized", [])}
            redirected = {m["from"]: m["to"] for m in query.get("redirects", [])}
            text = {p["title"]: p.get("extract", "") for p in query["pages"].values()}
            for lead in chunk:
                final = moved.get(lead.title, lead.title)
                final = redirected.get(final, final)
                out[lead.url] = text.get(final, "")
        return out

    def page(self, lead: Lead) -> str:
        data = self._api(action="query", prop="extracts", explaintext=1, exsectionformat="plain",
                         redirects=1, titles=lead.title)
        pages = data["query"]["pages"].values()
        text = next(iter(pages)).get("extract", "")
        return text[: self.config.get("max_chars", 9000)]


# ----------------------------------------------------------------------
# What a title is
# ----------------------------------------------------------------------


def clean_title(title: str) -> str:
    return re.sub(r"\s*\(.*?\)\s*", " ", title).strip()


def game_id(title: str) -> str:
    gid = re.sub(r"[^a-z0-9]+", "_", clean_title(title).lower()).strip("_")
    return gid if gid[:1].isalpha() else "g_" + gid


def known(title: str, inventory: list[Record]) -> Record | None:
    s = slug(clean_title(title))
    return next((r for r in inventory if s in schema.names(r)), None)


# ----------------------------------------------------------------------
# Extraction
# ----------------------------------------------------------------------

#: The model decides these. Everything else on a record is set by code.
MODEL_FIELDS = (
    "name", "aliases", "summary", "rules_text", "players_min", "players_max", "turns", "randomness",
    "communication", "ending", "outcome", "contamination", "hidden", "needs", "unmapped", "skills", "judged",
)


def system_prompt(manifest: dict) -> str:
    needs = "\n".join(f"  {k}: {v['note']}" for k, v in manifest["needs"].items())
    return f"""You file games into an inventory used to build turn-based, text-only, multi-player strategy
environments for training language models. You are given the text of one web page.

If the page is not about one specific, playable game with rules (it is a concept, a list, a person, a
real-time or physical sport, a video game that cannot be played turn by turn), reply with
{{"skip": "<one short reason>"}} and nothing else.

Otherwise reply with one JSON object and nothing else, with exactly these keys:

  name            the game's usual name
  aliases         other names, a list (may be empty)
  summary         one line, at most {schema.MAX_SUMMARY} characters: what the game is, not how it is played
  rules_text      the rules in YOUR OWN WORDS, {schema.MIN_RULES_WORDS} to 200 words, enough to play from.
                  Do not copy sentences from the page.
  players_min, players_max   integers
  turns           one of: {', '.join(schema.TURNS)}
  randomness      one of: {', '.join(schema.RANDOMNESS)}
  communication   one of: {', '.join(schema.COMMUNICATION)}   (talk between players that the rules allow)
  ending          one of: {', '.join(schema.ENDINGS)}
  outcome         one of: {', '.join(schema.OUTCOMES)}
  contamination   one of: {', '.join(schema.CONTAMINATION)}   (famous = a language model has surely seen its strategy)
  hidden          a list, any of: {', '.join(schema.HIDDEN)} (empty if all information is public)
  skills          a non-empty list, any of: {', '.join(schema.SKILLS)}
  judged          true only if who won cannot be computed from the moves and needs a judge's opinion
  needs           a list of everything the game requires, chosen ONLY from these (omit what it does not need):
{needs}
  unmapped        a list of short phrases for anything the game requires that none of the needs above
                  describes (empty if none). Be honest here: it is how missing engine features are found.

Judge the mechanics, not the theme. Reply with the JSON object only."""


def first_json(text: str) -> dict:
    """The first complete JSON object in a reply, however it is wrapped."""
    start = text.find("{")
    if start < 0:
        raise ValueError("no JSON object in the reply")
    try:
        obj, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as exc:
        raise ValueError(f"the JSON did not parse: {exc}") from None
    if not isinstance(obj, dict):
        raise ValueError("the reply is not a JSON object")
    return obj


@dataclass
class Extraction:
    record: Record | None = None
    skip: str | None = None
    error: str | None = None
    attempts: int = 0
    #: The model call itself failed (not the reply). Worth trying again later, so not logged.
    transient: bool = False


class Extractor:
    def __init__(self, completion: Completion, manifest: dict, repairs: int = 2):
        self.completion = completion
        self.system = system_prompt(manifest)
        self.vocabulary = set(manifest["needs"])
        self.repairs = repairs

    def extract(self, lead: Lead, text: str, licence: str) -> Extraction:
        prompt = f"Page title: {lead.title}\n\nPage text:\n{text}"
        result = Extraction()
        for attempt in range(1, self.repairs + 2):
            result.attempts = attempt
            try:
                reply = self.completion.complete(prompt, system=self.system)
            except Exception as exc:  # noqa: BLE001 - a backend that is down is not a bad game
                result.error, result.transient = f"model call failed: {str(exc)[:200]}", True
                return result
            try:
                data = first_json(reply)
                if "skip" in data:
                    result.skip = str(data["skip"])[:200]
                    return result
                result.record = self.build(lead, data, licence)
                return result
            except (ValueError, RecordError, TypeError) as exc:
                result.error = str(exc)
                prompt = (
                    f"{prompt}\n\nYour previous reply was refused: {exc}\n"
                    "Reply again with the corrected JSON object only."
                )
        return result

    def build(self, lead: Lead, data: dict, licence: str) -> Record:
        # Source and licence are facts about where the page came from, so a model
        # that offers its own is ignored rather than trusted. The id comes from the
        # game's name, not the page's address: a URL is often `index` or `rules`.
        fields = {k: data[k] for k in MODEL_FIELDS if k in data}
        named = game_id(str(fields["name"])) if str(fields.get("name", "")).strip() else game_id(lead.title)
        rec = from_dict({
            **fields,
            "id": named,
            "licence": licence,
            "source": {"kind": "url", "url": lead.url},
        })
        found = problems(rec, self.vocabulary)
        if found:
            raise RecordError("; ".join(found))
        return rec


# ----------------------------------------------------------------------
# The crawl
# ----------------------------------------------------------------------


class CrawlLog:
    """What happened to every lead, one JSON line each. A rerun skips these."""

    def __init__(self, path: Path = LOG_PATH):
        self.path = Path(path)
        self.entries: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if line.strip():
                    e = json.loads(line)
                    self.entries[e["url"]] = e

    def write(self, lead: Lead, outcome: str, detail: str = "", rating: int | None = None) -> dict:
        """Record what became of a lead. The rating, once given, stays on the
        entry through every later outcome, so it can be read after the fact."""
        if rating is None:
            rating = (self.entries.get(lead.url) or {}).get("rating")
        entry = {"url": lead.url, "title": lead.title, "outcome": outcome, "detail": detail, "via": lead.via,
                 "rating": rating}
        self.entries[lead.url] = entry
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as fh:
            fh.write(json.dumps(entry) + "\n")
        return entry


    def added(self, host: str | None = None) -> int:
        """Games admitted so far, overall or from one website."""
        return sum(1 for e in self.entries.values()
                   if e["outcome"] == "added" and (host is None or urllib.parse.urlparse(e["url"]).netloc.removeprefix("www.") == host))

    def render(self) -> str:
        """CRAWLED.md: every page ever read, by website, and what came of it."""
        by_site: dict[str, list[dict]] = {}
        for e in self.entries.values():
            by_site.setdefault(urllib.parse.urlparse(e["url"]).netloc, []).append(e)
        out = [
            "# Crawled pages",
            "",
            "Generated from `data/crawl_log.jsonl` by the crawl. A page listed here is never read again.",
            "",
        ]
        for site, entries in sorted(by_site.items()):
            tally: dict[str, int] = {}
            for e in entries:
                tally[e["outcome"]] = tally.get(e["outcome"], 0) + 1
            out += [f"## {site}", "", f"{len(entries)} pages: " + ", ".join(f"{n} {k}" for k, n in sorted(tally.items())), "",
                    "| page | rating | outcome | detail |", "|---|---|---|---|"]
            for e in entries:
                detail = e["detail"].replace("|", "\\|")
                out.append(f"| [{e['title']}]({e['url']}) | {e.get('rating') or '–'} | {e['outcome']} | {detail} |")
            out.append("")
        return "\n".join(out)


def crawl(
    source,
    inventory: Inventory,
    extractor: Extractor | None,
    log: CrawlLog,
    limit: int | None = None,
    target: int | None = None,
    retry_failed: bool = False,
    rater=None,
    min_rating: int = 3,
    rate_only: bool = False,
    rate_budget: int | None = None,
    on_event: Callable[[str, Lead, str], None] = lambda *_: None,
) -> dict[str, int]:
    """Find every lead on `source`, rate them, and extract the best.

      1 enumerate  list the source's games; drop what is already known
      2 rate       a cheap look at each new lead's opening (needs a `rater`)
      3 extract    read the leads rated at least `min_rating` in full, best first,
                   and admit what passes the gates

    Stops extracting after `limit` pages this run, or once the log holds
    `target` admitted games from this source. `rate_budget` caps how many new
    leads are rated this run, in the order the source listed them, which is what
    keeps a large site affordable. A rating is kept in the log, so lowering
    `min_rating` later reads the leads that were rated below it, without asking
    again. With no rater every lead is eligible; with no extractor and no rater
    it only lists leads. Returns a count per outcome.
    """
    counts: dict[str, int] = {}

    def done(outcome: str, lead: Lead, detail: str = "") -> None:
        counts[outcome] = counts.get(outcome, 0) + 1
        on_event(outcome, lead, detail)

    # 1. enumerate
    fresh: list[Lead] = []
    queue: list[tuple[int, int, Lead]] = []  # (rating, order, lead) to extract
    order = 0
    for lead in source.discover():
        order += 1
        before = log.entries.get(lead.url)
        if before:
            rating = before.get("rating")
            if before["outcome"] in ("rated", "below") and rating is not None:
                if rating >= min_rating:
                    queue.append((rating, order, lead))
            elif before["outcome"] == "failed" and retry_failed:
                queue.append((rating or 0, order, lead))
            continue
        if (dup := known(lead.title, inventory.all())) is not None:
            log.write(lead, "known", dup.id)
            done("known", lead, dup.id)
            continue
        fresh.append(lead)
        if rater is None:
            queue.append((0, order, lead))

    # 2. rate
    if rater is not None and fresh:
        fresh = fresh[:rate_budget] if rate_budget is not None else fresh
        snippets = source.snippets(fresh)
        for lead in [l for l in fresh if not snippets.get(l.url, "").strip()]:
            log.write(lead, "filtered", "no text to read")  # unreadable: nothing to rate
            done("filtered", lead, "no text")
        fresh = [l for l in fresh if snippets.get(l.url, "").strip()]
        rated = rater.rate([(lead, snippets[lead.url]) for lead in fresh])
        for n, lead in enumerate(fresh):
            got = rated.get(lead.url)
            if got is None:  # no valid answer: leave it unlogged, it is asked again next run
                done("unrated", lead)
                continue
            keep = got.rating >= min_rating
            log.write(lead, "rated" if keep else "below", got.reason, rating=got.rating)
            done(f"rated:{got.rating}", lead, got.reason)
            if keep:
                queue.append((got.rating, 10_000 + n, lead))

    if rate_only:
        return counts
    if extractor is None:
        for _, _, lead in sorted(queue, key=lambda q: (-q[0], q[1]))[: limit if limit is not None else None]:
            done("lead", lead)
        return counts

    # 3. extract, best first
    spent = 0
    outages = 0  # model calls failed in a row; a backend that is down ends the run
    for rating, _, lead in sorted(queue, key=lambda q: (-q[0], q[1])):
        if outages >= 3:
            break
        if (limit is not None and spent >= limit) or (target is not None and log.added(source.host) >= target):
            break
        try:
            text = source.page(lead)
        except OSError as exc:  # a page that cannot be fetched is a failed lead, not a failed crawl
            log.write(lead, "failed", str(exc))
            done("failed", lead, str(exc))
            continue
        if len(text) < source.config.get("min_chars", 0):
            log.write(lead, "filtered", f"page under {source.config['min_chars']} characters")
            done("filtered", lead, "too short")
            continue

        spent += 1
        got = extractor.extract(lead, text, source.licence)
        if got.transient:  # not logged: the lead is read again on the next run
            outages += 1
            done("deferred", lead, got.error or "")
            continue
        outages = 0
        if got.skip:
            log.write(lead, "skipped", got.skip)
            done("skipped", lead, got.skip)
        elif got.record is None:
            log.write(lead, "failed", got.error or "")
            done("failed", lead, got.error or "")
        else:
            taken = {r.id for r in inventory.all()}
            base, n = got.record.id, 2
            while got.record.id in taken:  # another page gave the same name: the duplicate gate decides, not a crash
                got.record.id, n = f"{base}_{n}", n + 1
            entry = log.entries.get(lead.url) or {}
            got.record.rating = entry.get("rating")
            got.record.rating_reason = entry.get("detail", "") if entry.get("outcome") in ("rated", "below") else ""
            try:
                rec = inventory.add(got.record)
            except RecordError as exc:  # an id already taken by a different game
                log.write(lead, "failed", str(exc))
                done("failed", lead, str(exc))
                continue
            log.write(lead, "added", rec.status)
            done(f"added:{rec.status}", lead, rec.reasons[0] if rec.reasons else "")
    return counts
