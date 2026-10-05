"""The rating step: a cheap look at every lead, so only the best are read.

A scripted model plays the rater and another plays the extractor, so what is
tested is the crawl's own logic: who gets rated, who gets read, in what order,
and what is remembered.
"""

from __future__ import annotations

import json
import tempfile
import urllib.parse
from pathlib import Path

from generator import crawl, gates, rate
from generator.crawl import CrawlLog, Extractor, Lead, Wikipedia
from generator.inventory import Inventory
from generator.rate import Rater, Rating

CONFIG = {"categories": ["Category:Games"], "queries": [], "exclude_title": [], "min_chars": 50, "max_chars": 5000}
TITLES = ["Alpha", "Beta", "Gamma", "Delta"]

RULES = (
    "Each player is dealt a hidden die and in turn names how many dice of one face the whole table holds. "
    "The next player must raise the claim or challenge it. A challenge reveals every die: a false claim "
    "costs the claimant a die, and a true one costs the challenger. The last player holding any dice wins."
)


def good(name: str, words: str = "") -> str:
    # every game gets its own text, or the gates would call the second a duplicate
    own = " ".join(f"{name.lower()}{i}" for i in range(80))
    return json.dumps({
        "name": name, "aliases": [], "summary": f"{name}: a bluffing game.", "rules_text": RULES + " " + own + words,
        "players_min": 2, "players_max": 6, "turns": "sequential", "randomness": "dice", "communication": "none",
        "ending": "elimination", "outcome": "win_lose", "contamination": "obscure", "hidden": ["hands"],
        "needs": ["hidden_hands", "sequential_choice"], "unmapped": [], "skills": ["bluffing"], "judged": False,
    })


def fake_get(url: str) -> str:
    q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    if q.get("list") == ["categorymembers"]:
        return json.dumps({"query": {"categorymembers": [{"title": t} for t in TITLES]}})
    asked = q["titles"][0].split("|")
    if "exintro" in q:
        return json.dumps({"query": {"pages": {str(i): {"title": t, "extract": f"{t} is a game of bluffing. " * 3}
                                               for i, t in enumerate(asked)}}})
    return json.dumps({"query": {"pages": {"1": {"title": asked[0], "extract": f"{asked[0]} full page. " * 20}}}})


class Scripted:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts: list[str] = []
        self.systems: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        self.systems.append(system)
        return self.replies.pop(0) if self.replies else '{"ratings": []}'


def ratings(**by_index) -> str:
    return json.dumps({"ratings": [{"i": int(k[1:]), "rating": v, "reason": f"because {k}"} for k, v in by_index.items()]})


def source() -> Wikipedia:
    return Wikipedia(CONFIG, get=fake_get, pause=0)


def world(rater_replies=(), extract_replies=()):
    inv = Inventory(Path(tempfile.mkdtemp()))
    log = CrawlLog(Path(tempfile.mkdtemp()) / "log.jsonl")
    rmodel, emodel = Scripted(*rater_replies), Scripted(*extract_replies)
    return inv, log, rmodel, emodel, Rater(rmodel, inv.manifest), Extractor(emodel, inv.manifest)


def lead(title: str) -> Lead:
    return Lead(title, "https://en.wikipedia.org/wiki/" + title, "wikipedia")


# -- the rater -------------------------------------------------------------


def test_a_batch_is_rated_in_one_call_and_returned_by_url():
    _, _, model, _, rater, _ = world([ratings(i0=5, i1=2)])
    got = rater.rate([(lead("A"), "text a"), (lead("B"), "text b")])
    assert got == {lead("A").url: Rating(5, "because i0"), lead("B").url: Rating(2, "because i1")}
    assert len(model.prompts) == 1 and "[0] A" in model.prompts[0] and "[1] B" in model.prompts[0]


def test_ratings_outside_one_to_five_are_refused_and_only_those_are_asked_again():
    bad = json.dumps({"ratings": [{"i": 0, "rating": 6, "reason": "x"}, {"i": 1, "rating": "4", "reason": "x"},
                                  {"i": 2, "rating": True, "reason": "x"}, {"i": 3, "rating": 3, "reason": "ok"}]})
    _, _, model, _, rater, _ = world([bad, ratings(i0=4, i1=1, i2=2)])
    got = rater.rate([(lead(c), "t") for c in "ABCD"])
    assert [got[lead(c).url].rating for c in "ABCD"] == [4, 1, 2, 3]
    assert "[3]" not in model.prompts[1] and "[0]" in model.prompts[1]


def test_an_item_that_never_gets_a_valid_rating_is_left_out_not_guessed():
    _, _, model, _, rater, _ = world(["nonsense", "more nonsense"])
    assert rater.rate([(lead("A"), "t")]) == {}
    assert len(model.prompts) == 2  # one attempt and one repair


def test_long_lists_go_in_batches_and_snippets_are_cut():
    _, _, model, _, _, _ = world([ratings(i0=3, i1=3), ratings(i0=3)])
    inv = Inventory(Path(tempfile.mkdtemp()))
    rater = Rater(model, inv.manifest, batch=2)
    rater.rate([(lead(c), "x" * 5000) for c in "ABCD"[:3]])
    assert len(model.prompts) == 2
    assert max(len(p) for p in model.prompts) < 2 * (rate.SNIPPET_CHARS + 100)


def test_the_rubric_is_anchored_in_the_manifest():
    system = rate.system_prompt(gates.load_manifest())
    assert "conditional_subsequence" in system and "spatial_board" in system  # the cannot list
    assert "hidden_hands" in system  # the can list
    assert "1  Not a specific playable game" in system


# -- snippets --------------------------------------------------------------


def test_snippets_follow_normalised_and_redirected_titles():
    def get(url):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        assert q["titles"] == ["liar's dice|Perudo"]
        return json.dumps({"query": {
            "normalized": [{"from": "liar's dice", "to": "Liar's dice"}],
            "redirects": [{"from": "Perudo", "to": "Dudo"}],
            "pages": {"1": {"title": "Liar's dice", "extract": "dice"}, "2": {"title": "Dudo", "extract": "claims"}}}})
    src = Wikipedia(CONFIG, get=get, pause=0)
    got = src.snippets([lead("liar's dice"), lead("Perudo")])
    assert got == {lead("liar's dice").url: "dice", lead("Perudo").url: "claims"}


def test_snippets_are_fetched_twenty_to_a_request():
    calls = []
    def get(url):
        calls.append(url)
        return json.dumps({"query": {"pages": {}}})
    Wikipedia(CONFIG, get=get, pause=0).snippets([lead(f"G{i}") for i in range(45)])
    assert len(calls) == 3


# -- the crawl with a rater ----------------------------------------------------


def run(inv, log, rater, extractor, **kw):
    return crawl.crawl(source(), inv, extractor, log, rater=rater, **kw)


def test_only_high_rated_leads_are_read_and_best_first():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=4, i1=2, i2=5, i3=1)], [good("Gamma"), good("Alpha", " Extra.")])
    counts = run(inv, log, rater, ex)
    assert counts == {"rated:4": 1, "rated:2": 1, "rated:5": 1, "rated:1": 1, "added:ready": 2}
    assert "Page title: Gamma" in emodel.prompts[0]  # the 5 before the 4
    assert "Page title: Alpha" in emodel.prompts[1]
    assert len(emodel.prompts) == 2  # Beta and Delta were never read in full


def test_a_low_rating_is_remembered_with_its_reason():
    inv, log, *_ = world([ratings(i0=2, i1=2, i2=2, i3=2)])
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=2, i1=2, i2=2, i3=2)])
    run(inv, log, rater, ex)
    e = log.entries[lead("Beta").url]
    assert (e["outcome"], e["rating"], e["detail"]) == ("below", 2, "because i1")


def test_lowering_the_threshold_reads_earlier_leads_without_rating_them_again():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=3, i1=3, i2=3, i3=3)], [good("Alpha")])
    run(inv, log, rater, ex, min_rating=4)
    assert emodel.prompts == []
    asked = len(rmodel.prompts)
    run(inv, CrawlLog(log.path), rater, ex, min_rating=3, limit=1)
    assert len(rmodel.prompts) == asked and len(emodel.prompts) == 1


def test_a_lead_with_no_valid_rating_is_not_logged_so_it_is_asked_again():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=5, i1=5, i2=5), "junk"], [good("Alpha"), good("Beta", " More.")])
    counts = run(inv, log, rater, ex, limit=1)
    assert counts.get("unrated") == 1
    assert lead("Delta").url not in log.entries


def test_rate_only_reads_nothing_in_full():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=5, i1=5, i2=5, i3=5)])
    counts = run(inv, log, rater, None, rate_only=True)
    assert counts == {"rated:5": 4} and emodel.prompts == [] and inv.all() == []


def test_the_record_carries_the_rating_and_the_model_cannot_set_it():
    reply = json.loads(good("Alpha"))
    reply.update(rating=1, rating_reason="mine")
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=5, i1=1, i2=1, i3=1)], [json.dumps(reply)])
    run(inv, log, rater, ex)
    rec = inv.get("alpha")
    assert (rec.rating, rec.rating_reason) == (5, "because i0")
    assert log.entries[lead("Alpha").url]["rating"] == 5  # kept through the later outcome


def test_a_known_game_is_not_rated():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=5, i1=5, i2=5)], [good("Beta")])
    inv.add(crawl.from_dict({**json.loads(good("Alpha")), "id": "alpha", "licence": "rules_only",
                             "source": {"kind": "url", "url": "https://x.example"}}))
    run(inv, log, rater, ex, rate_only=True)
    assert "[0] Beta" in rmodel.prompts[0] and "Alpha" not in rmodel.prompts[0]


def test_the_queue_puts_the_higher_rating_first_and_the_index_shows_it():
    inv, log, rmodel, emodel, rater, ex = world([ratings(i0=4, i1=5, i2=1, i3=1)],
                                                [good("Beta", " First."), good("Alpha", " Second.")])
    run(inv, log, rater, ex)
    assert [r.id for r in inv.queue()] == ["beta", "alpha"]
    row = next(l for l in inv.index_path.read_text().splitlines() if "`beta`" in l)
    assert "| 5 |" in row


# -- calibration -----------------------------------------------------------


def test_calibrate_pairs_each_rating_with_what_the_page_became():
    inv, log, rmodel, emodel, rater, ex = world([], [good("Alpha"), '{"skip": "concept"}'])
    run(inv, log, None, ex, limit=2)
    judge = Rater(Scripted(ratings(i0=5, i1=1)), inv.manifest)
    pairs = rate.calibrate(judge, source(), log, inv)
    assert sorted(pairs) == [(1, "skipped"), (5, "queued")]
    table = rate.crosstab(pairs)
    assert table.splitlines()[1].startswith("5") and "100%" in table
