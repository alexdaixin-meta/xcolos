"""Reading any website politely: fetch, obey robots.txt, cache, turn HTML into text.

Nothing here knows about games. It is the part of a generic reader that does not
change from site to site: a fetcher that asks `robots.txt` first, waits between
requests and remembers what it has fetched; an HTML-to-text pass built on the
standard library; and a sitemap reader.
"""

from __future__ import annotations

import hashlib
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

USER_AGENT = "xcolos-generator/0.1 (game inventory research)"
CACHE_DIR = Path(__file__).parent / "data" / "cache"
MAX_BYTES = 2_000_000


class FetchError(OSError):
    """A page that could not be read: refused by robots.txt, missing, or not text."""


def _raw_get(url: str, timeout: float = 20) -> tuple[str, str]:
    """One GET. Returns (content type, text). Raises FetchError with the status."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xml,text/plain"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - http(s) only, checked by the caller
            body = resp.read(MAX_BYTES)
            return resp.headers.get("Content-Type", ""), body.decode(resp.headers.get_content_charset() or "utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        err = FetchError(f"{url}: HTTP {exc.code}")
        err.code = exc.code  # type: ignore[attr-defined]
        raise err from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise FetchError(f"{url}: {exc}") from None


class Fetcher:
    """GET with robots.txt, a pause between requests to one host, and a disk cache.

    A page already fetched is read from the cache, so a rerun costs no requests
    and the rater and the extractor see the same text.
    """

    def __init__(
        self,
        cache_dir: Path | None = CACHE_DIR,
        delay: float = 1.0,
        raw: Callable[[str], tuple[str, str]] = _raw_get,
        obey_robots: bool = True,
    ):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.delay = delay
        self.raw = raw
        self.obey_robots = obey_robots
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self._why: dict[str, str] = {}
        self._last: dict[str, float] = {}

    def allowed(self, url: str) -> bool:
        if not self.obey_robots:
            return True
        parts = urllib.parse.urlparse(url)
        base = f"{parts.scheme}://{parts.netloc}"
        if base not in self._robots:
            parser: urllib.robotparser.RobotFileParser | None = urllib.robotparser.RobotFileParser()
            try:
                parser.parse(self._get(base + "/robots.txt").splitlines())
            except FetchError as exc:
                if getattr(exc, "code", None) in (404, 410):
                    parser = None  # no robots.txt: nothing is restricted
                else:
                    parser.disallow_all = True  # could not tell, so do not read
                    self._why[base] = f"robots.txt could not be read ({exc}), so the site is not read"
            self._robots[base] = parser
        parser = self._robots[base]
        return True if parser is None else parser.can_fetch(USER_AGENT, url)

    def refusal(self, url: str) -> str | None:
        """Why a URL may not be read, or None if it may."""
        if self.allowed(url):
            return None
        base = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(url))
        return self._why.get(base) or f"robots.txt at {base} does not allow reading it"

    def sitemaps(self, base: str) -> list[str]:
        try:
            lines = self._get(base + "/robots.txt").splitlines()
        except FetchError:
            return []
        return [l.split(":", 1)[1].strip() for l in lines if l.lower().startswith("sitemap:")]

    def get(self, url: str) -> str:
        if urllib.parse.urlparse(url).scheme not in ("http", "https"):
            raise FetchError(f"{url}: not a web address")
        if not self.allowed(url):
            raise FetchError(f"{url}: disallowed by robots.txt")
        return self._get(url)

    def _get(self, url: str) -> str:
        path = self.cache_dir / (hashlib.sha1(url.encode()).hexdigest() + ".txt") if self.cache_dir else None
        if path is not None and path.exists():
            return path.read_text()
        host = urllib.parse.urlparse(url).netloc
        for attempt in range(1, 5):
            wait = self._last.get(host, 0) + self.delay - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last[host] = time.monotonic()
            try:
                kind, text = self.raw(url)
                break
            except FetchError as exc:
                if getattr(exc, "code", None) not in (429, 503) or attempt == 4:
                    raise
                time.sleep(min(2.0**attempt, 30))
        if not re.search(r"html|xml|text", kind, re.I):
            raise FetchError(f"{url}: not text ({kind})")
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        return text


# ----------------------------------------------------------------------
# HTML to text
# ----------------------------------------------------------------------

_SKIP = {"script", "style", "noscript", "svg", "nav", "header", "footer", "aside", "form", "iframe", "template"}
_BLOCK = {"p", "div", "li", "br", "tr", "section", "article", "table", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "dt", "dd", "pre"}


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.links: list[str] = []
        self._in_title = False
        self._skip = 0
        self._main = 0
        self._all: list[str] = []
        self._main_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)
        if tag == "title":
            self._in_title = True
        if tag in _SKIP:
            self._skip += 1
        if tag in ("main", "article"):
            self._main += 1
        if tag in _BLOCK:
            self._put("\n")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in _SKIP and self._skip:
            self._skip -= 1
        if tag in ("main", "article") and self._main:
            self._main -= 1
        if tag in _BLOCK:
            self._put("\n")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        else:
            # a newline inside text is a space; only block tags break lines
            self._put(re.sub(r"\s+", " ", data))

    def _put(self, text: str) -> None:
        if self._skip:
            return
        self._all.append(text)
        if self._main:
            self._main_text.append(text)

    @staticmethod
    def _clean(chunks: list[str]) -> str:
        lines = (re.sub(r"[ \t\r\f\v]+", " ", l).strip() for l in "".join(chunks).split("\n"))
        return "\n".join(l for l in lines if l)

    def text(self) -> str:
        main = self._clean(self._main_text)
        return main if len(main) >= 400 else self._clean(self._all)


def html_to_text(html: str) -> tuple[str, str, list[str]]:
    """Returns (title, text, links). Navigation, scripts and footers are dropped,
    and the text inside <main> or <article> is preferred when there is enough."""
    page = _Page()
    page.feed(html)
    return re.sub(r"\s+", " ", page.title).strip(), page.text(), page.links


# ----------------------------------------------------------------------
# Sitemaps
# ----------------------------------------------------------------------


def sitemap_urls(fetcher: Fetcher, url: str, limit: int = 5000, depth: int = 2, errors: list[str] | None = None) -> list[str]:
    """Every page URL a sitemap lists, following sitemap indexes a little way.
    A sitemap that cannot be read is reported in `errors`, not raised."""
    try:
        xml = fetcher.get(url)
    except FetchError as exc:
        if errors is not None:
            errors.append(str(exc))
        return []
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.S)
    if "<sitemapindex" in xml and depth > 0:
        out: list[str] = []
        for child in locs[:20]:
            if child.endswith(".gz"):
                continue
            out += sitemap_urls(fetcher, child, limit - len(out), depth - 1, errors)
            if len(out) >= limit:
                break
        return out[:limit]
    return locs[:limit]
