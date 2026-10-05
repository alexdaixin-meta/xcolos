"""A reader for any website: no code and no configuration per site.

It follows the same contract as `crawl.Wikipedia` (discover, snippets, page), so
rating, extraction, the gates and the log are shared. Which pages are games is
not decided here: the rater does that, from each page's opening.

To keep that cheap on a large site, `discover` returns the pages interleaved
across URL shapes (`/games/*`, `/blog/#/*`, ...), so a rating budget spent in
order samples every part of the site instead of exhausting the first one.
"""

from __future__ import annotations

import re
import urllib.parse
from collections import defaultdict
from itertools import zip_longest

from generator.crawl import Lead
from generator.web import FetchError, Fetcher, html_to_text, sitemap_urls

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


def title_from(url: str) -> str:
    seg = [s for s in urllib.parse.urlparse(url).path.split("/") if s][-1:] or [""]
    return re.sub(r"[-_+]+", " ", re.sub(r"\.\w{2,5}$", "", urllib.parse.unquote(seg[0]))).strip().title()


class GenericSite:
    licence = "rules_only"

    def __init__(self, host: str, seed_url: str, fetcher: Fetcher, config: dict | None = None, max_pages: int = 60):
        self.host = host
        self.name = host
        self.seed = seed_url
        self.fetcher = fetcher
        self.config = {"min_chars": 600, "max_chars": 9000, **(config or {})}
        self.max_pages = max_pages  # when there is no sitemap, pages fetched to find links
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
                seen.add(url)
                groups[shape(url)].append(Lead(title_from(url), url, self.name, f"shape:{shape(url)}"))
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
