"""One record per game: removing what the duplicate gate stopped, and merging
what a model says is one game under different names.

A scripted model plays the judge, so nothing here calls a model.
"""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from gen_inventory import dedup
from gen_inventory.crawl import CrawlLog, Lead
from gen_inventory.inventory import Inventory
from gen_inventory.schema import from_dict

BASE = dict(
    id="dudo", name="Dudo", summary="Hidden dice and claims about the whole table.", aliases=[],
    rules_text=" ".join(f"dudo{i}" for i in range(60)), licence="rules_only",
    source={"kind": "url", "url": "https://a.test/dudo"}, players_min=2, players_max=6, turns="sequential",
    randomness="dice", communication="none", ending="elimination", outcome="win_lose", contamination="known",
    hidden=["hands"], needs=["hidden_hands", "sequential_choice"], skills=["bluffing"],
)


def make(**over):
    data = copy.deepcopy(BASE)
    data.update(over)
    data.setdefault("rules_text", BASE["rules_text"])
    return from_dict(data)


def own(word: str) -> str:
    return " ".join(f"{word}{i}" for i in range(60))


class Scripted:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        return self.replies.pop(0)


def world():
    root = Path(tempfile.mkdtemp())
    inv = Inventory(root / "inv")
    log = CrawlLog(root / "log.jsonl")
    return inv, log


def logged(log: CrawlLog, rec) -> None:
    log.write(Lead(rec.name, rec.source["url"], "x", "shape:/*"), "added", rec.status)


def test_prune_removes_what_the_gate_stopped_and_marks_its_page():
    inv, log = world()
    logged(log, inv.add(make()))
    twin = inv.add(make(id="dudo_2", source={"kind": "url", "url": "https://b.test/dudo"}, rules_text=own("other")))
    logged(log, twin)
    assert twin.status == "duplicate"
    assert dedup.prune(inv, log) == [("dudo_2", "dudo")]
    assert [r.id for r in inv.all()] == ["dudo"]
    entry = CrawlLog(log.path).entries["https://b.test/dudo"]
    assert (entry["outcome"], entry["detail"]) == ("duplicate", "dudo")


def test_judge_keeps_only_groups_of_real_ids():
    inv, _ = world()
    inv.add(make())
    inv.add(make(id="perudo", name="Perudo", rules_text=own("perudo"), source={"kind": "url", "url": "https://b.test/p"}))
    model = Scripted('{"same": [["dudo", "perudo", "made_up"], ["dudo"], ["ghost", "phantom"]]}')
    assert dedup.judge(model, inv.all()) == [["dudo", "perudo"]]
    assert "dudo | Dudo | - |" in model.prompts[0]


def test_canonical_names_a_chunk_at_a_time_and_ignores_ids_from_elsewhere():
    inv, _ = world()
    for word in ("alpha", "beta", "gamma"):
        inv.add(make(id=word, name=word.title(), rules_text=own(word), source={"kind": "url", "url": f"https://x.test/{word}"}))
    model = Scripted('{"names": {"alpha": "Oh Hell", "beta": "Oh hell!", "gamma": "stray"}}', '{"names": {"gamma": "Whist"}}')
    assert dedup.canonical(model, inv.all(), chunk=2) == {"alpha": "Oh Hell", "beta": "Oh hell!", "gamma": "Whist"}
    assert len(model.prompts) == 2 and "gamma" not in model.prompts[0]


def test_find_confirms_each_named_group_alone_before_calling_it_one_game():
    inv, _ = world()
    for word in ("blackout", "blob", "omaha", "texas"):
        inv.add(make(id=word, name=word.title(), rules_text=own(word), source={"kind": "url", "url": f"https://x.test/{word}"}))
    named = json.dumps({"names": {"blackout": "Oh Hell", "blob": "Oh Hell", "omaha": "Poker", "texas": "Poker"}})
    model = Scripted(named, '{"same": [["blackout", "blob"]]}', '{"same": []}')
    groups, names = dedup.find(model, inv.all())
    assert groups == [["blackout", "blob"]] and names["blob"] == "Oh Hell"
    assert "omaha" not in model.prompts[1] and "blackout" not in model.prompts[2]  # each group asked about alone


def test_merge_keeps_the_game_furthest_along_and_takes_the_others_names():
    inv, log = world()
    logged(log, inv.add(make(rating=4)))
    perudo = inv.add(make(id="perudo", name="Perudo", aliases=["Call My Bluff"], rules_text=own("perudo"), rating=5,
                          source={"kind": "url", "url": "https://b.test/p"}))
    logged(log, perudo)
    blocked = inv.add(make(id="cachito", name="Cachito", rules_text=own("cachito"), unmapped=["a cup"],
                           source={"kind": "url", "url": "https://c.test/c"}))
    assert blocked.status == "blocked"
    assert dedup.merge(inv, log, [["cachito", "dudo", "perudo"]]) == [("perudo", ["cachito", "dudo"])]
    kept = inv.get("perudo")
    # the others' names, not their aliases: an alias a model guessed is not carried over
    assert kept.aliases == ["Call My Bluff", "Cachito", "Dudo"] and kept.status == "ready"
    assert [r.id for r in inv.all()] == ["perudo"]
    assert CrawlLog(log.path).entries["https://a.test/dudo"]["outcome"] == "duplicate"


def test_merge_adds_the_name_the_game_goes_by():
    inv, log = world()
    inv.add(make(id="blackout", name="Blackout", rules_text=own("blackout")))
    inv.add(make(id="blob", name="Blob", rules_text=own("blob"), source={"kind": "url", "url": "https://b.test/blob"}))
    dedup.merge(inv, log, [["blackout", "blob"]], {"blackout": "Oh Hell", "blob": "Oh hell"})
    assert inv.get("blackout").aliases == ["Blob", "Oh Hell"]


def test_merge_keeps_the_record_filed_under_the_name_the_game_goes_by():
    inv, log = world()
    inv.add(make(id="priests_of_ra", name="Priests Of Ra", rules_text=own("priests")))
    inv.add(make(id="ra", name="Ra", rules_text=own("ra"), source={"kind": "url", "url": "https://b.test/ra"}))
    assert dedup.merge(inv, log, [["priests_of_ra", "ra"]], {"priests_of_ra": "Ra", "ra": "Ra"}) == [("ra", ["priests_of_ra"])]


def test_merge_skips_a_group_already_merged():
    inv, log = world()
    inv.add(make())
    inv.add(make(id="perudo", name="Perudo", rules_text=own("perudo"), source={"kind": "url", "url": "https://b.test/p"}))
    assert len(dedup.merge(inv, log, [["dudo", "perudo"], ["perudo", "dudo"]])) == 1


def test_cli_dedup_prunes_then_merges_with_a_model():
    from gen_inventory.cli import main
    inv, log = world()
    inv.add(make())
    inv.add(make(id="dudo_2", rules_text=own("other"), source={"kind": "url", "url": "https://b.test/dudo"}))
    inv.add(make(id="perudo", name="Perudo", rules_text=own("perudo"), source={"kind": "url", "url": "https://b.test/p"}))
    # one fixed reply serves both questions: what each record is, and whether a group is one game
    reply = json.dumps({"names": {"dudo": "Liar's dice", "perudo": "Liar's Dice"}, "same": [["dudo", "perudo"]]})
    assert main(["--dir", str(inv.root), "dedup", "--dry-run", "--model", "echo:" + reply]) == 0
    assert len(inv.all()) == 3  # a dry run changes nothing
    assert main(["--dir", str(inv.root), "dedup", "--model", "echo:" + reply]) == 0
    assert [r.id for r in inv.all()] == ["dudo"] and inv.get("dudo").aliases == ["Perudo", "Liar's dice"]
