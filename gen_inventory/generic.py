"""A reader for any website: no code and no configuration per site.

It follows the same contract as `crawl.Wikipedia` (discover, snippets, page), so
rating, extraction, the gates and the log are shared. Which pages are games is
not decided here: the rater does that, from each page's opening.

To keep that cheap on a large site, `discover` returns the pages interleaved
across URL shapes (`/games/*`, `/blog/#/*`, ...), so a rating budget spent in
order samples every part of the site instead of exhausting the first one.

A site may have a few lines in `crawl_sources.json`, under its host, when its
addresses say which pages are games: `include_path` and `exclude_path` (regular
expressions on the path); `title_segment`, the path segment that names the game
(`-1`, the last, unless a site files every game as `/<game>/rules.php`); and
`title_strip`, what to cut from that name (a year a site appends, say), so the
name can be matched against the games already here. That is configuration, not
a reader: the pages are still read the same way.
"""

from __future__ import annotations

import re
import urllib.parse
from collections import defaultdict
from itertools import zip_longest

from gen_inventory.crawl import Lead
from gen_inventory.web import FetchError, Fetcher, html_to_text, sitemap_urls

#: Paths that are never a game's page.
SKIP_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp|ico|pdf|zip|gz|mp3|mp4|css|js|json|xml|rss|txt|docx?|xlsx?)$", re.I)
SKIP_PATH = re.compile(r"/(tag|tags|category|categories|author|authors|user|users|login|signin|register|cart|search|feed|"
                       r"wp-admin|wp-json|page|forum|forums|contact|about|privacy|terms|sitemap)(/|$)", re.I)


def shape(url: str) -> str:
    """A URL's pattern: digits and the last segment collapsed, so every page of
    one kind has the same shape."""
    segs = [s for s in urllib.parse.urlparse(url).path.split("/") if s]
    if not segs:
        return "/"
    head = [re.sub(r"\d+", "#", s) for s in segs[:-1]]
    return "/" + "/".join(head + ["*"])


def title_from(url: str, segment: int = -1) -> str:
    segs = [s for s in urllib.parse.urlparse(url).path.split("/") if s] or [""]
    seg = segs[segment] if -len(segs) <= segment < len(segs) else segs[-1]
    return re.sub(r"[-_+]+", " ", re.sub(r"\.\w{2,5}$", "", urllib.parse.unquote(seg))).strip().title()


#: When a site has no sitemap, the most pages fetched to find its links. Not a
#: budget: it only stops a site whose addresses never run out.
MAX_PAGES = 20_000


class GenericSite:
    licence = "rules_only"

    def __init__(self, host: str, seed_url: str, fetcher: Fetcher, config: dict | None = None,
                 max_pages: int | None = None):
        self.host = host
        self.name = host
        self.seed = seed_url
        self.fetcher = fetcher
        self.config = {"min_chars": 600, "max_chars": 9000, **(config or {})}
        self.max_pages = max_pages or self.config.get("max_pages", MAX_PAGES)
        self._include = [re.compile(p) for p in self.config.get("include_path", [])]
        self._exclude = [re.compile(p) for p in self.config.get("exclude_path", [])]
        self._title_segment = int(self.config.get("title_segment", -1))
        self._title_strip = re.compile(self.config["title_strip"]) if self.config.get("title_strip") else None
        self._leads: list[Lead] | None = None
        #: Why the site gave nothing, in plain words, when it did not.
        self.notes: list[str] = []

    # -- finding pages ---------------------------------------------------

    def _same_site(self, url: str) -> bool:
        return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.") == self.host

    def urls(self) -> list[str]:
        base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(self.seed))
        if (why := self.fetcher.refusal(self.seed)) is not None:
            self.notes.append(why)
            return []
        found: list[str] = []
        errors: list[str] = []
        for sm in (self.fetcher.sitemaps(base) or [base + "/sitemap.xml"]):
            found += sitemap_urls(self.fetcher, sm, errors=errors)
        if found:
            return found
        self.notes += [f"sitemap: {e}" for e in errors[:2]] or ["no sitemap found"]
        # no sitemap: follow links from the seed, breadth first, up to a page budget
        seen, queue, out = {self.seed}, [self.seed], []
        while queue and len(out) < self.max_pages:
            url = queue.pop(0)
            try:
                _, _, links = html_to_text(self.fetcher.get(url))
            except FetchError as exc:
                if url == self.seed:
                    self.notes.append(f"seed page: {exc}")
                continue
            out.append(url)
            for href in links:
                full = urllib.parse.urldefrag(urllib.parse.urljoin(url, href))[0]
                if full not in seen and self._same_site(full):
                    seen.add(full)
                    queue.append(full)
        return out + [u for u in queue if u not in out]

    def discover(self) -> list[Lead]:
        if self._leads is None:
            groups: dict[str, list[Lead]] = defaultdict(list)
            seen: set[str] = set()
            for url in self.urls():
                url = urllib.parse.urldefrag(url)[0]
                path = urllib.parse.urlparse(url).path
                if (url in seen or not self._same_site(url) or SKIP_EXT.search(path) or SKIP_PATH.search(path)
                        or path in ("", "/")):
                    continue
                if (self._include and not any(p.search(path) for p in self._include)) or any(
                        p.search(path) for p in self._exclude):
                    continue
                seen.add(url)
                title = title_from(url, self._title_segment)
                if self._title_strip:
                    title = self._title_strip.sub("", title).strip() or title
                groups[shape(url)].append(Lead(title, url, self.name, f"shape:{shape(url)}"))
            # one page from each shape in turn, so a budget samples the whole site
            self._leads = [l for row in zip_longest(*groups.values()) for l in row if l is not None]
            if not self._leads and not self.notes:
                self.notes.append("the site lists pages, but none look like content")
        return self._leads

    # -- reading them ----------------------------------------------------

    def _read(self, lead: Lead) -> tuple[str, str]:
        title, text, _ = html_to_text(self.fetcher.get(lead.url))
        return title, text

    def snippets(self, leads: list[Lead], chars: int = 500) -> dict[str, str]:
        out = {}
        for lead in leads:
            try:
                title, text = self._read(lead)
                out[lead.url] = (title + "\n" + text)[:chars]
            except FetchError:
                out[lead.url] = ""
        return out

    def page(self, lead: Lead) -> str:
        title, text = self._read(lead)
        return (title + "\n" + text)[: self.config["max_chars"]]
