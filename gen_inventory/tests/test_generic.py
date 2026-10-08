"""The generic site reader: fetching politely, HTML to text, sitemaps, and a crawl.

A dictionary of pages plays the website, so nothing here touches the network.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from gen_inventory import crawl, generic, web
from gen_inventory.crawl import CrawlLog, Extractor, Lead
from gen_inventory.generic import GenericSite, shape, title_from
from gen_inventory.inventory import Inventory
from gen_inventory.rate import Rater
from gen_inventory.web import FetchError, Fetcher, html_to_text, sitemap_urls

RULES = (
    "Each player is dealt a hidden die and in turn names how many dice of one face the whole table holds. "
    "The next player must raise the claim or challenge it. A challenge reveals every die: a false claim "
    "costs the claimant a die, and a true one costs the challenger. The last player holding any dice wins."
)


def page(title: str, body: str, nav: str = "Home About Contact") -> str:
    return (f"<html><head><title>{title}</title><script>var x = 'IGNORED';</script></head><body>"
            f"<nav>{nav} <a href='/games/other'>Other</a></nav><main><h1>{title}</h1><p>{body}</p></main>"
            f"<footer>Copyright junk</footer></body></html>")


class Site:
    """A fake website: url -> (content type, text). Counts every request."""

    def __init__(self, pages: dict[str, str], robots: str | None = "User-agent: *\nAllow: /\n"):
        self.pages = {u: ("text/html", t) for u, t in pages.items()}
        if robots is not None:
            self.pages["https://x.test/robots.txt"] = ("text/plain", robots)
        self.requests: list[str] = []

    def raw(self, url: str):
        self.requests.append(url)
        if url not in self.pages:
            err = FetchError(f"{url}: HTTP 404")
            err.code = 404
            raise err
        return self.pages[url]


def fetcher(site: Site, **kw) -> Fetcher:
    return Fetcher(cache_dir=Path(tempfile.mkdtemp()), delay=0, raw=site.raw, **kw)


def sitemap(*urls: str) -> str:
    return "<urlset>" + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>"


# -- html to text ----------------------------------------------------------


def test_text_keeps_the_content_and_drops_navigation_scripts_and_footers():
    title, text, links = html_to_text(page("Liar's Dice", "A bluffing game. " * 40))
    assert title == "Liar's Dice"
    assert "bluffing game" in text
    for junk in ("IGNORED", "Copyright", "Home About"):
        assert junk not in text
    assert "/games/other" in links


def test_a_page_with_no_main_block_falls_back_to_the_whole_body():
    _, text, _ = html_to_text("<html><body><h1>Poker</h1><p>Deal five cards.</p></body></html>")
    assert text == "Poker\nDeal five cards."


def test_entities_and_whitespace_are_cleaned():
    _, text, _ = html_to_text("<body><p>Tom &amp;   Jerry\n\n   play</p><p></p><p>  now </p></body>")
    assert text == "Tom & Jerry play\nnow"


# -- urls ------------------------------------------------------------------


def test_shape_groups_pages_of_one_kind():
    assert shape("https://x.test/games/poker") == shape("https://x.test/games/chess") == "/games/*"
    assert shape("https://x.test/blog/2019/05/why-bid") == "/blog/#/#/*"
    assert shape("https://x.test/") == "/"


def test_title_comes_from_the_last_path_segment():
    assert title_from("https://x.test/games/texas-holdem.html") == "Texas Holdem"
    assert title_from("https://x.test/rules/Liar%27s_Dice/") == "Liar'S Dice"


# -- the fetcher -----------------------------------------------------------


def test_robots_txt_can_forbid_a_page():
    site = Site({"https://x.test/secret/a": "x", "https://x.test/open/a": "y"}, robots="User-agent: *\nDisallow: /secret/\n")
    f = fetcher(site)
    assert f.get("https://x.test/open/a") == "y"
    try:
        f.get("https://x.test/secret/a")
    except FetchError as exc:
        assert "robots" in str(exc)
    else:
        raise AssertionError("a disallowed page was fetched")
    assert "https://x.test/secret/a" not in site.requests


def test_no_robots_txt_means_no_restriction_but_a_failing_one_means_no():
    site = Site({"https://x.test/a": "ok"}, robots=None)
    assert fetcher(site).get("https://x.test/a") == "ok"

    def broken(url):
        if url.endswith("robots.txt"):
            err = FetchError("boom")
            err.code = 500
            raise err
        return "text/html", "ok"
    f = Fetcher(cache_dir=None, delay=0, raw=broken)
    try:
        f.get("https://x.test/a")
    except FetchError:
        pass
    else:
        raise AssertionError("read a site whose robots.txt could not be read")


def test_a_page_is_fetched_once_then_read_from_the_cache():
    site = Site({"https://x.test/a": "hello"})
    f = fetcher(site)
    f.get("https://x.test/a")
    f.get("https://x.test/a")
    assert site.requests.count("https://x.test/a") == 1


def test_a_cache_outlives_the_fetcher():
    site = Site({"https://x.test/a": "hello"})
    f = fetcher(site)
    f.get("https://x.test/a")
    again = Fetcher(cache_dir=f.cache_dir, delay=0, raw=Site({}).raw)
    assert again.get("https://x.test/a") == "hello"


def test_binary_content_and_odd_schemes_are_refused():
    site = Site({})
    site.pages["https://x.test/img"] = ("image/png", "xx")
    f = fetcher(site)
    for url in ("https://x.test/img", "ftp://x.test/a", "file:///etc/passwd"):
        try:
            f.get(url)
        except FetchError:
            continue
        raise AssertionError(f"{url} was read")


def test_a_busy_server_is_retried(monkeypatch=None):
    calls = []

    def flaky(url):
        calls.append(url)
        if url.endswith("robots.txt"):
            err = FetchError("nope")
            err.code = 404
            raise err
        if len(calls) < 3:
            err = FetchError("busy")
            err.code = 503
            raise err
        return "text/html", "finally"
    real = web.time.sleep
    web.time.sleep = lambda s: None
    try:
        assert Fetcher(cache_dir=None, delay=0, raw=flaky).get("https://x.test/a") == "finally"
    finally:
        web.time.sleep = real


# -- sitemaps --------------------------------------------------------------


def test_a_sitemap_index_is_followed_a_level_down():
    site = Site({
        "https://x.test/sitemap.xml": "<sitemapindex><sitemap><loc>https://x.test/s1.xml</loc></sitemap>"
                                      "<sitemap><loc>https://x.test/s2.xml</loc></sitemap></sitemapindex>",
        "https://x.test/s1.xml": sitemap("https://x.test/games/a", "https://x.test/games/b"),
        "https://x.test/s2.xml": sitemap("https://x.test/games/c"),
    })
    assert sitemap_urls(fetcher(site), "https://x.test/sitemap.xml") == [
        "https://x.test/games/a", "https://x.test/games/b", "https://x.test/games/c"]


def test_robots_txt_names_the_sitemap():
    site = Site({}, robots="User-agent: *\nSitemap: https://x.test/maps/all.xml\n")
    assert fetcher(site).sitemaps("https://x.test") == ["https://x.test/maps/all.xml"]


# -- discovery -------------------------------------------------------------


def reader(site: Site, **kw) -> GenericSite:
    return GenericSite("x.test", "https://x.test/", fetcher(site), **kw)


def test_discover_interleaves_shapes_and_drops_what_is_not_a_page_of_the_site():
    site = Site({"https://x.test/sitemap.xml": sitemap(
        "https://x.test/games/a", "https://x.test/games/b", "https://x.test/games/c",
        "https://x.test/blog/2019/one", "https://x.test/blog/2019/two",
        "https://x.test/img/logo.png", "https://x.test/tag/dice", "https://x.test/", "https://other.test/games/z")})
    urls = [l.url for l in reader(site).discover()]
    assert urls == ["https://x.test/games/a", "https://x.test/blog/2019/one", "https://x.test/games/b",
                    "https://x.test/blog/2019/two", "https://x.test/games/c"]


def test_without_a_sitemap_links_are_followed_within_the_site_up_to_a_budget():
    site = Site({
        "https://x.test/": "<a href='/games/a'>a</a><a href='/games/b'>b</a><a href='https://elsewhere.test/x'>x</a>",
        "https://x.test/games/a": "<a href='/games/c'>c</a>",
        "https://x.test/games/b": "", "https://x.test/games/c": "",
    })
    urls = [l.url for l in reader(site, max_pages=10).discover()]
    assert set(urls) == {"https://x.test/games/a", "https://x.test/games/b", "https://x.test/games/c"}
    assert not any("elsewhere" in r for r in site.requests)


# -- a crawl over a generic site -------------------------------------------------


class Scripted:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        return self.replies.pop(0)


def good(name: str) -> str:
    own = " ".join(f"{name.lower()}{i}" for i in range(80))
    return json.dumps({
        "name": name, "aliases": [], "summary": f"{name}: a bluffing game.", "rules_text": RULES + " " + own,
        "players_min": 2, "players_max": 6, "turns": "sequential", "randomness": "dice", "communication": "none",
        "ending": "elimination", "outcome": "win_lose", "contamination": "obscure", "hidden": ["hands"],
        "needs": ["hidden_hands", "sequential_choice"], "unmapped": [], "skills": ["bluffing"], "judged": False})


def sitemap_for(pages):
    return Site({**pages, "https://x.test/sitemap.xml": sitemap(*pages)})


def test_a_crawl_of_a_generic_site_rates_then_reads_the_best_and_files_the_record():
    body = "A game of hidden dice and claims about the whole table. " * 20
    pages = {"https://x.test/games/liars-dice": page("Liar's Dice", body),
             "https://x.test/blog/news": page("News", "We moved offices. " * 40)}
    site = sitemap_for(pages)
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    rater = Rater(Scripted(json.dumps({"ratings": [{"i": 0, "rating": 5, "reason": "dice"}, {"i": 1, "rating": 1, "reason": "news"}]})),
                  inv.manifest)
    ex = Extractor(Scripted(good("Liars Dice")), inv.manifest)
    counts = crawl.crawl(reader(site), inv, ex, log, target=5, rater=rater, rate_budget=10)
    assert counts == {"rated:5": 1, "rated:1": 1, "added:ready": 1}
    rec = inv.get("liars_dice")
    assert rec.source["url"] == "https://x.test/games/liars-dice" and rec.rating == 5 and rec.licence == "rules_only"
    assert log.added("x.test") == 1 and log.added("en.wikipedia.org") == 0


def test_the_rating_budget_limits_how_many_pages_are_fetched_and_rated():
    pages = {f"https://x.test/games/g{i}": page(f"G{i}", "text " * 200) for i in range(30)}
    site = sitemap_for(pages)
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    model = Scripted(*[json.dumps({"ratings": [{"i": i, "rating": 1, "reason": "x"} for i in range(5)]})] * 2)
    rater = Rater(model, inv.manifest, batch=5)
    crawl.crawl(reader(site), inv, None, log, rater=rater, rate_only=True, rate_budget=10)
    fetched = [r for r in site.requests if "/games/" in r]
    assert len(fetched) == 10 and len(model.prompts) == 2


def test_a_page_with_no_text_is_filtered_not_rated():
    pages = {"https://x.test/games/a": "<html><body></body></html>",
             "https://x.test/games/b": page("B", "A game of claims. " * 40)}
    site = sitemap_for(pages)
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    model = Scripted(json.dumps({"ratings": [{"i": 0, "rating": 4, "reason": "ok"}]}))
    counts = crawl.crawl(reader(site), inv, None, log, rater=Rater(model, inv.manifest), rate_only=True)
    assert counts == {"filtered": 1, "rated:4": 1}
    assert "[0] B" in model.prompts[0] and "[1]" not in model.prompts[0]


def test_a_page_that_cannot_be_fetched_at_read_time_is_logged_failed():
    pages = {"https://x.test/games/a": page("A", "A game of claims. " * 40)}
    site = sitemap_for(pages)
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    rater = Rater(Scripted(json.dumps({"ratings": [{"i": 0, "rating": 5, "reason": "ok"}]})), inv.manifest)
    src = reader(site)
    src.page = lambda lead: (_ for _ in ()).throw(FetchError("gone"))
    counts = crawl.crawl(src, inv, Extractor(Scripted(), inv.manifest), log, rater=rater)
    assert counts == {"rated:5": 1, "failed": 1} and inv.all() == []


# -- the command line, end to end ------------------------------------------------


def cli_world(approved: bool = True):
    """A temp inventory with one approved site whose single page is a game."""
    from gen_inventory import cli
    from gen_inventory.sources import Registry

    root = Path(tempfile.mkdtemp())
    reg = Registry(root / "sources.json")
    reg.add_source("X", "https://x.test/", "catalogue", "why", "human", status="approved" if approved else "suggested")
    site = sitemap_for({"https://x.test/games/liars-dice": page("Liar's Dice", "Hidden dice and claims. " * 40)})
    cli.make_fetcher = lambda: fetcher(site)
    return root, site


def run_cli(root, *argv) -> int:
    from gen_inventory.cli import main
    return main(["--dir", str(root / "inv"), *argv])


RATING = json.dumps({"ratings": [{"i": 0, "rating": 5, "reason": "dice"}]})


def test_cli_crawl_a_generic_site_end_to_end():
    root, site = cli_world()
    code = run_cli(root, "crawl", "--site", "x.test", "--target", "5", "--model", "echo:" + good("Liars Dice"),
                   "--rate-model", "echo:" + RATING)
    assert code == 0
    inv = Inventory(root / "inv")
    assert [r.id for r in inv.all()] == ["liars_dice"]
    assert inv.get("liars_dice").rating == 5
    assert (root / "inv" / "CRAWLED.md").exists() and (root / "inv" / "SOURCES.md").exists()
    assert (root / "crawl_log.jsonl").exists()
    # a second run reads nothing new
    assert run_cli(root, "crawl", "--site", "x.test", "--target", "5", "--model", "echo:" + good("Liars Dice"),
                   "--rate-model", "echo:" + RATING) == 0
    assert len(Inventory(root / "inv").all()) == 1


def test_cli_refuses_a_site_that_is_not_approved():
    root, _ = cli_world(approved=False)
    assert run_cli(root, "crawl", "--site", "x.test", "--model", "echo:x") == 1
    assert run_cli(root, "crawl", "--site", "unknown.test", "--model", "echo:x") == 1
    assert Inventory(root / "inv").all() == []


def test_cli_rate_only_files_no_game():
    root, _ = cli_world()
    assert run_cli(root, "crawl", "--site", "x.test", "--rate-only", "--model", "echo:" + RATING) == 0
    assert Inventory(root / "inv").all() == []
    assert "rated" in (root / "crawl_log.jsonl").read_text()


def test_cli_calibrate_runs_over_a_generic_site():
    root, _ = cli_world()
    run_cli(root, "crawl", "--site", "x.test", "--model", "echo:" + good("Liars Dice"), "--rate-model", "echo:" + RATING)
    assert run_cli(root, "calibrate", "--site", "x.test", "--model", "echo:" + RATING) == 0


def test_the_wikipedia_reader_takes_its_phrases_from_the_registry():
    from gen_inventory import cli
    from gen_inventory.sources import Registry
    import argparse

    root = Path(tempfile.mkdtemp())
    reg = Registry(root / "sources.json")
    reg.add_source("Wikipedia", "https://en.wikipedia.org", "encyclopedia", "x", "human", status="crawling")
    reg.add_query("en.wikipedia.org", "auction game", "model")
    src = cli.wikipedia_source(argparse.Namespace(dir=root / "inv"))
    assert src.config["queries"] == ["auction game"] and src.host == "en.wikipedia.org"


# -- ids come from the game, and an empty site says why ------------------------


def named_world(pages, replies):
    site = sitemap_for(pages)
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    ratings = json.dumps({"ratings": [{"i": i, "rating": 5, "reason": "ok"} for i in range(len(pages))]})
    return site, inv, log, Rater(Scripted(ratings), inv.manifest), Extractor(Scripted(*replies), inv.manifest)


def test_pages_called_index_become_games_with_their_own_names():
    pages = {f"https://x.test/{d}/index.html": page(f"Page {d}", "A game of hidden dice. " * 40) for d in ("a", "b", "c")}
    site, inv, log, rater, ex = named_world(pages, [good("Poker"), good("Bridge"), good("Hearts")])
    counts = crawl.crawl(reader(site), inv, ex, log, rater=rater)
    assert sorted(r.id for r in inv.all()) == ["bridge", "hearts", "poker"]
    assert not counts.get("failed")


def test_two_pages_that_name_the_same_game_both_get_filed_and_the_gates_pick_the_duplicate():
    pages = {f"https://x.test/rules/{d}": page(f"Rules {d}", "A game of hidden dice. " * 40) for d in ("a", "b")}
    site, inv, log, rater, ex = named_world(pages, [good("Poker"), good("Poker")])
    counts = crawl.crawl(reader(site), inv, ex, log, rater=rater)
    assert not counts.get("failed")
    by_id = {r.id: r for r in inv.all()}
    assert set(by_id) == {"poker", "poker_2"}
    assert by_id["poker_2"].status == "duplicate" and by_id["poker_2"].duplicate_of == "poker"


def test_a_site_that_robots_txt_forbids_says_so():
    site = Site({"https://x.test/sitemap.xml": sitemap("https://x.test/games/a")}, robots="User-agent: *\nDisallow: /\n")
    r = reader(site)
    assert r.discover() == [] and "robots.txt" in r.notes[0]


def test_a_robots_txt_that_cannot_be_read_says_so():
    def raw(url):
        err = FetchError("HTTP 403")
        err.code = 403
        raise err
    r = GenericSite("x.test", "https://x.test/", Fetcher(cache_dir=None, delay=0, raw=raw))
    assert r.discover() == [] and "could not be read" in r.notes[0]


def test_a_site_with_no_sitemap_and_an_unreadable_seed_says_so():
    site = Site({})
    r = reader(site)
    assert r.discover() == [] and any("seed page" in n for n in r.notes)


def test_a_sitemap_that_lists_only_non_content_says_so():
    site = Site({"https://x.test/sitemap.xml": sitemap("https://x.test/tag/a", "https://x.test/img/b.png")})
    r = reader(site)
    assert r.discover() == [] and r.notes
