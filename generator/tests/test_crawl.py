"""The crawl: leads, the pre-gate, extraction with repair, and the log.

Nothing here touches the network or a model. A fake `get` answers the API, and a
scripted completion plays the model, so what is tested is the crawl's own logic.
"""

from __future__ import annotations

import json
import tempfile
import urllib.parse
from pathlib import Path

from generator import crawl, gates
from generator.crawl import CrawlLog, Extractor, Lead, Wikipedia
from generator.inventory import Inventory

CONFIG = {
    "queries": ["bluffing game"],
    "categories": ["Category:Card_games"],
    "exclude_title": ["^List of", r"\(video game\)"],
    "min_chars": 100,
    "max_chars": 5000,
}

RULES = (
    "Each player is dealt a hidden die and in turn names how many dice of one face the whole table holds. "
    "The next player must raise the claim or challenge it. A challenge reveals every die: a false claim "
    "costs the claimant a die, and a true one costs the challenger. The last player holding any dice wins."
)

GOOD = {
    "name": "Liar's Dice",
    "aliases": ["Perudo"],
    "summary": "Hidden dice and escalating claims about the whole table.",
    "rules_text": RULES,
    "players_min": 2,
    "players_max": 6,
    "turns": "sequential",
    "randomness": "dice",
    "communication": "none",
    "ending": "elimination",
    "outcome": "win_lose",
    "contamination": "known",
    "hidden": ["hands"],
    "needs": ["hidden_hands", "sequential_choice", "variable_player_count", "elimination"],
    "unmapped": [],
    "skills": ["bluffing", "hidden_state_inference"],
    "judged": False,
}

PAGE = "Liar's dice is a class of dice games for two or more players. " * 5


def fake_get(url: str) -> str:
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    if q.get("list") == ["search"]:
        titles = ["Liar's dice", "List of dice games", "Dudo (video game)"]
        return json.dumps({"query": {"search": [{"title": t} for t in titles]}})
    if q.get("list") == ["categorymembers"]:
        return json.dumps({"query": {"categorymembers": [{"title": "Liar's dice"}, {"title": "Coup (card game)"}]}})
    title = q["titles"][0]
    return json.dumps({"query": {"pages": {"1": {"extract": PAGE if title != "Tiny" else "short"}}}})


class Scripted:
    """A model that answers from a list, and remembers what it was asked."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        return self.replies.pop(0) if self.replies else '{"skip": "script ran out"}'


def source() -> Wikipedia:
    return Wikipedia(CONFIG, get=fake_get, pause=0)


def setup(*replies):
    inv = Inventory(Path(tempfile.mkdtemp()))
    model = Scripted(*replies)
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    return inv, model, log, Extractor(model, inv.manifest)


def run(inv, ex, log, **kw):
    return crawl.crawl(source(), inv, ex, log, **kw)


# -- discovery -------------------------------------------------------------


def test_discover_filters_titles_and_does_not_repeat_a_lead():
    titles = [lead.title for lead in source().discover()]
    assert titles == ["Liar's dice", "Coup (card game)"]  # categories first; no list, no video game, no repeat


def test_a_lead_has_a_wikipedia_url():
    assert source().discover()[0].url == "https://en.wikipedia.org/wiki/Liar%27s_dice"


def test_discover_reads_no_pages_and_calls_no_model():
    inv, model, log, _ = setup()
    counts = run(inv, None, log)
    assert counts == {"lead": 2} and model.prompts == []


# -- titles ----------------------------------------------------------------


def test_ids_and_known_titles():
    assert crawl.game_id("Chicken (game)") == "chicken"
    assert crawl.game_id("Liar's dice") == "liar_s_dice"
    assert crawl.game_id("2048 (video game)") == "g_2048"
    inv = Inventory(Path(tempfile.mkdtemp()))
    inv.add(crawl.from_dict({**GOOD, "id": "liars_dice", "licence": "rules_only",
                             "source": {"kind": "url", "url": "https://x.example"}}))
    assert crawl.known("Perudo (dice game)", inv.all()).id == "liars_dice"


# -- extraction ------------------------------------------------------------


def test_a_good_reply_is_admitted_through_the_gates():
    inv, model, log, ex = setup(json.dumps(GOOD), '{"skip": "not a game"}')
    counts = run(inv, ex, log, limit=1)
    assert counts == {"added:ready": 1}
    rec = inv.get("liar_s_dice")
    assert rec.status == "ready" and rec.reward == "verifiable"
    assert rec.licence == "rules_only"
    assert rec.source == {"kind": "url", "url": "https://en.wikipedia.org/wiki/Liar%27s_dice"}
    assert "Liar's Dice" in inv.index_path.read_text()


def test_the_model_cannot_set_its_own_source_licence_or_id():
    reply = json.dumps({**GOOD, "id": "mine", "licence": "cc0", "source": {"kind": "url", "url": "https://evil.example"},
                        "status": "accepted"})
    inv, model, log, ex = setup(reply)
    run(inv, ex, log, limit=1)
    rec = inv.get("liar_s_dice")
    assert (rec.licence, rec.status) == ("rules_only", "ready")
    assert "evil" not in rec.source["url"]


def test_a_reply_wrapped_in_prose_and_fences_still_parses():
    inv, model, log, ex = setup("Here you go:\n```json\n" + json.dumps(GOOD) + "\n```\nHope that helps.")
    assert run(inv, ex, log, limit=1) == {"added:ready": 1}


def test_a_bad_reply_is_repaired_with_the_reason_in_the_prompt():
    bad = {**GOOD, "turns": "sideways", "needs": ["hidden_hands", "teleportation"]}
    inv, model, log, ex = setup(json.dumps(bad), json.dumps(GOOD))
    assert run(inv, ex, log, limit=1) == {"added:ready": 1}
    assert len(model.prompts) == 2
    assert "turns" in model.prompts[1] and "teleportation" in model.prompts[1]


def test_a_reply_that_never_gets_better_is_logged_failed_and_not_added():
    inv, model, log, ex = setup("no json", "still no json", "nope")
    assert run(inv, ex, log, limit=1) == {"failed": 1}
    assert len(model.prompts) == 3  # one attempt and two repairs
    assert inv.all() == []
    assert log.entries[next(iter(log.entries))]["outcome"] == "failed"


def test_a_skip_is_logged_and_nothing_is_added():
    inv, model, log, ex = setup('{"skip": "a concept, not a game"}')
    assert run(inv, ex, log, limit=1) == {"skipped": 1}
    assert inv.all() == []


def test_unmapped_needs_block_the_game_and_name_the_gap():
    odd = {**GOOD, "unmapped": ["players secretly swap hands"]}
    inv, model, log, ex = setup(json.dumps(odd))
    run(inv, ex, log, limit=1)
    rec = inv.get("liar_s_dice")
    assert rec.status == "blocked" and rec.blocked_by == ["unmapped: players secretly swap hands"]
    assert inv.gaps().most_common() == [("unmapped: players secretly swap hands", 1)]


def test_a_game_the_gates_drop_is_still_filed_so_it_is_not_asked_again():
    inv, model, log, ex = setup(json.dumps(GOOD), json.dumps({**GOOD, "name": "Perudo Two"}))
    run(inv, ex, log, limit=2)
    states = {r.id: r.status for r in inv.all()}
    # the id follows the name the model read, not the page it was on
    assert states == {"liar_s_dice": "ready", "perudo_two": "duplicate"}


# -- the pre-gate and the log ------------------------------------------------


def test_a_known_game_costs_no_model_call():
    inv, model, log, ex = setup(json.dumps(GOOD))
    inv.add(crawl.from_dict({**GOOD, "id": "liars_dice", "licence": "rules_only",
                             "source": {"kind": "url", "url": "https://x.example"}}))
    counts = run(inv, ex, log, limit=5)
    assert counts.get("known") == 1 and len(model.prompts) <= 1  # only Coup was read


def test_a_short_page_is_filtered_before_the_model():
    class Tiny(Wikipedia):
        def page(self, lead):
            return "short"
    inv, model, log, ex = setup()
    counts = crawl.crawl(Tiny(CONFIG, get=fake_get, pause=0), inv, ex, log, limit=5)
    assert counts == {"filtered": 2} and model.prompts == []


def test_a_rerun_skips_every_lead_it_has_already_read():
    inv, model, log, ex = setup(json.dumps(GOOD), '{"skip": "x"}')
    run(inv, ex, log, limit=5)
    asked = len(model.prompts)
    again = run(inv, ex, CrawlLog(log.path), limit=5)
    assert again == {} and len(model.prompts) == asked


def test_retry_failed_reads_a_failed_lead_again():
    inv, model, log, ex = setup("x", "x", "x", json.dumps(GOOD))
    run(inv, ex, log, limit=1)
    assert inv.all() == []
    assert run(inv, ex, CrawlLog(log.path), limit=1, retry_failed=True) == {"added:ready": 1}


def test_limit_counts_pages_read_not_leads_seen():
    inv, model, log, ex = setup(json.dumps(GOOD), '{"skip": "x"}')
    run(inv, ex, log, limit=1)
    assert len(model.prompts) == 1


def test_the_prompt_lists_the_manifest_vocabulary_so_the_model_cannot_guess_it():
    system = crawl.system_prompt(gates.load_manifest())
    for need in gates.load_manifest()["needs"]:
        assert need in system
    assert "own words" in system.lower()


# -- the target and the record of what was crawled ---------------------------


def test_target_stops_when_the_log_holds_that_many_added_games():
    inv, model, log, ex = setup(json.dumps(GOOD), json.dumps({**GOOD, "name": "Other", "rules_text": RULES + " More."}))
    assert run(inv, ex, log, target=1) == {"added:ready": 1}
    assert len(model.prompts) == 1


def test_target_counts_games_from_earlier_runs():
    inv, model, log, ex = setup(json.dumps(GOOD))
    run(inv, ex, log, target=1)
    # a later run, a fresh log object over the same file, has nothing left to do
    assert run(inv, ex, CrawlLog(log.path), target=1) == {}


def test_skips_do_not_count_toward_the_target():
    inv, model, log, ex = setup('{"skip": "x"}', json.dumps(GOOD))
    assert run(inv, ex, log, target=1) == {"skipped": 1, "added:ready": 1}


def test_the_crawled_report_lists_every_page_by_website():
    inv, model, log, ex = setup(json.dumps(GOOD), '{"skip": "a concept"}')
    run(inv, ex, log)
    text = log.render()
    assert "## en.wikipedia.org" in text
    assert "2 pages: 1 added, 1 skipped" in text
    assert "[Liar's dice](https://en.wikipedia.org/wiki/Liar%27s_dice) | – | added | ready" in text
    assert "| skipped | a concept |" in text


def test_the_cli_writes_crawled_md_next_to_the_index():
    from generator.cli import main
    root = Path(tempfile.mkdtemp())
    assert main(["--dir", str(root / "inv"), "crawled"]) == 0
    assert (root / "inv" / "CRAWLED.md").exists()
