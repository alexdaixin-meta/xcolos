"""The registry of sources and the model that suggests more.

A suggestion is a line in a list until a person approves it; a search phrase on
a site already being crawled is the only thing a model may add on its own.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from generator import sources
from generator.cli import main
from generator.crawl import CrawlLog, Lead
from generator.sources import Registry, SourceError, host_of, norm_query


class Scripted:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        return self.replies.pop(0)


def registry() -> Registry:
    reg = Registry(Path(tempfile.mkdtemp()) / "sources.json")
    reg.add_source("Wikipedia", "https://en.wikipedia.org", "encyclopedia", "rules pages", "human", status="crawling")
    return reg


def reply(sources_=(), queries=()):
    return json.dumps({"sources": list(sources_), "queries": [{"host": h, "q": q} for h, q in queries]})


SITE = {"name": "OpenSpiel games", "url": "https://github.com/google-deepmind/open_spiel", "kind": "catalogue",
        "why": "lists dozens of imperfect-information games"}


# -- hosts and phrases -----------------------------------------------------


def test_host_is_the_site_not_the_page():
    assert host_of("https://www.BoardGameGeek.com/boardgame/1234/x") == "boardgamegeek.com"
    assert host_of("http://en.wikipedia.org/wiki/Go") == "en.wikipedia.org"


def test_not_a_web_address_and_file_hosts_are_refused():
    for bad in ("ftp://example.com/x", "example", "javascript:alert(1)", "https://pastebin.com/abc", "https://i.imgur.com/x.png"):
        try:
            host_of(bad)
        except SourceError:
            continue
        raise AssertionError(f"{bad} was accepted")


def test_a_phrase_is_the_same_phrase_however_it_is_written():
    assert norm_query("  Bluffing,  Game! ") == norm_query("bluffing game")


def test_a_site_and_a_phrase_are_each_kept_once():
    reg = registry()
    entry, new = reg.add_source("WP again", "https://www.en.wikipedia.org/wiki/Poker", "other", "dup", "model")
    assert not new and entry["name"] == "Wikipedia"
    assert reg.add_query("en.wikipedia.org", "bluffing game", "human") is True
    assert reg.add_query("en.wikipedia.org", "Bluffing  game.", "model") is False
    assert reg.queries("en.wikipedia.org") == ["bluffing game"]


def test_the_registry_survives_a_reload():
    reg = registry()
    reg.add_query("en.wikipedia.org", "auction game", "model")
    assert Registry(reg.path).queries("en.wikipedia.org") == ["auction game"]


def test_unknown_kind_becomes_other_and_status_is_checked():
    reg = registry()
    entry, _ = reg.add_source("X", "https://x.example.com", "mystery", "why", "model")
    assert entry["kind"] == "other"
    try:
        reg.set_status("x.example.com", "banana")
    except SourceError:
        pass
    else:
        raise AssertionError("a made-up status was accepted")


# -- suggestions -----------------------------------------------------------


def test_a_new_site_is_only_suggested_never_crawled():
    reg = registry()
    got = sources.suggest(Scripted(reply([SITE])), reg, "summary", {})
    assert [s["host"] for s in got.new_sources] == ["github.com"]
    assert reg.get("github.com")["status"] == "suggested"
    assert reg.get("github.com")["origin"] == "model"


def test_a_phrase_on_a_crawling_site_is_added_and_a_repeat_is_not():
    reg = registry()
    reg.add_query("en.wikipedia.org", "bluffing game", "human")
    got = sources.suggest(Scripted(reply(queries=[("en.wikipedia.org", "bluffing game"), ("en.wikipedia.org", "negotiation game")])),
                          reg, "s", {})
    assert got.new_queries == [("en.wikipedia.org", "negotiation game")]
    assert any("already listed" in s for s in got.skipped)


def test_a_phrase_for_a_site_that_is_not_crawled_is_refused():
    reg = registry()
    reg.add_source(*("OpenSpiel", "https://github.com/x", "catalogue", "why", "model"))
    got = sources.suggest(Scripted(reply(queries=[("github.com", "poker"), ("nowhere.example.com", "poker")])), reg, "s", {})
    assert got.new_queries == []
    assert len(got.skipped) == 2


def test_bad_suggestions_are_skipped_not_fatal():
    reg = registry()
    got = sources.suggest(Scripted(reply([{"name": "x", "url": "not a url"}, {"name": "paste", "url": "https://pastebin.com/x"}, SITE])),
                          reg, "s", {})
    assert [s["host"] for s in got.new_sources] == ["github.com"]
    assert len(got.skipped) == 2


def test_a_reply_that_is_not_json_is_asked_again_once_then_gives_up():
    reg = registry()
    model = Scripted("sorry", reply([SITE]))
    assert len(sources.suggest(model, reg, "s", {}).new_sources) == 1
    assert "refused" in model.prompts[1]
    try:
        sources.suggest(Scripted("no", "still no"), registry(), "s", {})
    except SourceError:
        pass
    else:
        raise AssertionError("an unusable model was not reported")


def test_the_prompt_lists_everything_already_tried_so_the_model_can_avoid_it():
    reg = registry()
    reg.add_query("en.wikipedia.org", "bluffing game", "human")
    model = Scripted(reply())
    sources.suggest(model, reg, "3 covered", {"query:bluffing game": __import__("collections").Counter(added=2, skipped=1)}, n=4)
    ask = model.prompts[0]
    assert "en.wikipedia.org" in ask and "bluffing game" in ask and "3 covered" in ask
    assert "3 pages read, 2 added" in ask


# -- yield -----------------------------------------------------------------


def test_the_log_remembers_what_found_each_page_and_yield_counts_it():
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    log.write(Lead("A", "https://en.wikipedia.org/wiki/A", "wikipedia", "query:auction game"), "added", "ready")
    log.write(Lead("B", "https://en.wikipedia.org/wiki/B", "wikipedia", "query:auction game"), "skipped", "concept")
    log.write(Lead("C", "https://en.wikipedia.org/wiki/C", "wikipedia", "category:Category:Dice_games"), "added", "blocked")
    y = sources.yields_from(CrawlLog(log.path).entries.values())
    assert y["query:auction game"] == {"added": 1, "skipped": 1}
    assert y["category:Category:Dice_games"]["added"] == 1


def test_sources_md_lists_sites_phrases_and_their_yield():
    reg = registry()
    reg.add_source(*("OpenSpiel", "https://github.com/x", "catalogue", "many games", "model"))
    reg.add_query("en.wikipedia.org", "auction game", "model")
    from collections import Counter
    text = reg.render({"query:auction game": Counter(added=3, skipped=1)})
    assert "| [github.com](https://github.com/x) | catalogue | suggested | model |" in text
    assert "| auction game | model | 4 | 3 |" in text


# -- the command line ------------------------------------------------------


def run(root, *argv):
    return main(["--dir", str(root / "inv"), *argv])


def test_cli_sources_approve_reject_and_crawl_only_after_approval():
    root = Path(tempfile.mkdtemp())
    reg = Registry(root / "sources.json")
    reg.add_source("OpenSpiel", "https://github.com/x", "catalogue", "why", "model")
    assert run(root, "sources", "approve", "github.com") == 0
    assert Registry(reg.path).get("github.com")["status"] == "approved"
    assert run(root, "sources", "crawl", "github.com") == 0  # approved, so it may be crawled
    assert Registry(reg.path).get("github.com")["status"] == "crawling"
    assert run(root, "sources", "reject", "github.com") == 0
    reg2 = Registry(reg.path)
    reg2.add_source("Other", "https://other.example.com", "catalogue", "why", "model")
    assert run(root, "sources", "crawl", "other.example.com") == 1  # never approved: refused
    assert run(root, "sources", "approve", "unknown.example.com") == 1
    assert (root / "inv" / "SOURCES.md").exists()


def test_cli_suggest_with_a_fixed_reply_files_the_site():
    root = Path(tempfile.mkdtemp())
    reg = Registry(root / "sources.json")
    reg.add_source("Wikipedia", "https://en.wikipedia.org", "encyclopedia", "x", "human", status="crawling")
    answer = reply([SITE], [("en.wikipedia.org", "negotiation game")])
    assert run(root, "suggest", "--model", "echo:" + answer) == 0
    reg = Registry(reg.path)
    assert reg.get("github.com")["status"] == "suggested"
    assert reg.queries("en.wikipedia.org") == ["negotiation game"]
    # asking again with the same answer adds nothing
    assert run(root, "suggest", "--model", "echo:" + answer) == 0
    assert len(Registry(reg.path).sources) == 2


def test_the_shipped_registry_has_wikipedia_with_its_phrases():
    reg = Registry()
    wiki = reg.get("en.wikipedia.org")
    assert wiki["status"] == "crawling" and wiki["queries"] and wiki["categories"]
