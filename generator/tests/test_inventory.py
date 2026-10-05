"""The gates, one at a time, and the inventory that applies them.

Plain asserts and no pytest features, so the suite runs under either runner.
"""

from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from generator import gates, rate
from generator.cli import main
from generator.inventory import Inventory
from generator.schema import RecordError, from_dict

RULES = (
    "Two players take turns naming a number between one and ten. The first to reach "
    "a total of fifty wins the match and the other loses it. Each player sees every "
    "number named so far and nothing else, and there is no chance involved at all."
)

BASE = dict(
    id="race",
    name="Race to Fifty",
    summary="Two players race to a running total of fifty.",
    aliases=[],
    rules_text=RULES,
    licence="original",
    source={"kind": "url", "url": "https://example.invalid/race"},
    players_min=2,
    players_max=2,
    turns="sequential",
    randomness="none",
    communication="none",
    ending="goal",
    outcome="win_lose",
    contamination="obscure",
    hidden=[],
    needs=["sequential_choice"],
    skills=["planning"],
)


def make(**over):
    data = copy.deepcopy(BASE)
    data.update(over)
    return from_dict(data)


def inventory() -> Inventory:
    return Inventory(Path(tempfile.mkdtemp()))


def status(inv: Inventory, **over) -> str:
    return inv.add(make(**over)).status


# -- the record ------------------------------------------------------------


def test_unknown_key_is_refused():
    try:
        from_dict({**BASE, "playres_max": 3})
    except RecordError as exc:
        assert "playres_max" in str(exc)
    else:
        raise AssertionError("a misspelled key was accepted")


def test_missing_key_is_refused():
    data = {k: v for k, v in BASE.items() if k != "turns"}
    try:
        from_dict(data)
    except RecordError as exc:
        assert "turns" in str(exc)
    else:
        raise AssertionError("a record without turns was accepted")


# -- completeness ----------------------------------------------------------


def test_a_good_record_is_ready():
    rec = inventory().add(make())
    assert rec.status == "ready", rec.reasons
    assert rec.reward == "verifiable"
    assert rec.value == 2  # one skill, plus a mechanic nobody has yet


def test_short_rules_are_incomplete():
    inv = inventory()
    rec = inv.add(make(rules_text="Take turns naming numbers."))
    assert rec.status == "incomplete"
    assert any("words" in r for r in rec.reasons)


def test_unknown_need_is_incomplete_not_ignored():
    rec = inventory().add(make(needs=["sequential_choice", "teleportation"]))
    assert rec.status == "incomplete"
    assert any("teleportation" in r for r in rec.reasons)


def test_no_skills_is_incomplete():
    assert status(inventory(), skills=[]) == "incomplete"


def test_bad_enum_is_incomplete():
    rec = inventory().add(make(turns="sideways"))
    assert rec.status == "incomplete" and "turns" in rec.reasons[0]


# -- provenance ------------------------------------------------------------


def test_unfree_licence_is_rejected():
    rec = inventory().add(make(licence="copied_proprietary"))
    assert rec.status == "rejected"
    assert rec.reasons[0].startswith("provenance")


# -- duplication -----------------------------------------------------------


def test_same_name_is_a_duplicate():
    inv = inventory()
    inv.add(make())
    rec = inv.add(make(id="race2", name="race to fifty!"))
    assert (rec.status, rec.duplicate_of) == ("duplicate", "race")


def test_alias_counts_as_the_name():
    inv = inventory()
    inv.add(make())
    rec = inv.add(make(id="sprint", name="Sprint", aliases=["Race to 50", "Race to Fifty"]))
    assert rec.status == "duplicate"


def test_near_identical_text_is_a_duplicate():
    inv = inventory()
    inv.add(make())
    rec = inv.add(make(id="sprint", name="Sprint", rules_text=RULES.replace("fifty", "fifty five")))
    assert (rec.status, rec.duplicate_of) == ("duplicate", "race")


def test_same_mechanic_is_a_variant_not_a_duplicate():
    inv = inventory()
    first = inv.add(make())
    other = inv.add(make(id="climb", name="Climb", rules_text="Players alternately add to a running pile of stones, "
        "each taking up to four, and whoever takes the last stone loses. Both players see the pile at all times, "
        "no information is hidden, and nothing is left to chance, so only foresight decides the match."))
    assert other.status == "ready"
    assert other.family == first.id
    assert other.value == 1  # no new-mechanic bonus


def test_a_different_mechanic_is_its_own_family():
    inv = inventory()
    inv.add(make())
    other = inv.add(make(id="bluff", name="Bluff", hidden=["hands"], randomness="deal",
        rules_text="Each player is dealt a secret number and claims a total for the table in turn. "
        "A claim may be challenged by the next player, and the table is then revealed to decide who "
        "was right. A wrong claim loses a point and a wrong challenge does too, over several hands."))
    assert other.status == "ready" and other.family is None


def test_twins_on_a_recheck_do_not_both_call_the_other_the_original():
    inv = inventory()
    inv.add(make())
    inv.add(make(id="race2", name="Race Two", rules_text=RULES + " "))  # same text, different name
    inv.check_all()
    states = {r.id: r.status for r in inv.all()}
    assert states == {"race": "ready", "race2": "duplicate"}


def test_a_ported_game_is_the_original_over_a_ready_one():
    inv = inventory()
    ported = make(id="zz_ported", name="Zed", status="ported", port="x.json", rules_text=RULES)
    inv.save(ported)
    rec = inv.add(make(id="aa_race", name="Aardvark Race"))
    assert (rec.status, rec.duplicate_of) == ("duplicate", "zz_ported")


# -- capability ------------------------------------------------------------


def test_a_blocked_need_blocks_and_is_named():
    rec = inventory().add(make(needs=["sequential_choice", "conditional_subsequence"]))
    assert rec.status == "blocked"
    assert rec.blocked_by == ["conditional_subsequence"]
    assert "flat" in rec.reasons[0]


def test_a_workaround_is_ready_and_recorded():
    rec = inventory().add(make(needs=["payoff_matrix"]))
    assert rec.status == "ready" and rec.workarounds == ["payoff_matrix"]


def test_too_many_players_is_blocked():
    rec = inventory().add(make(players_min=20, players_max=30))
    assert rec.status == "blocked" and rec.blocked_by == ["player_count"]


def test_gaps_are_ranked_by_games_blocked():
    inv = inventory()
    texts = [
        "Players race across a live board in real time, grabbing tokens before the clock runs out, "
        "and nobody waits for anyone else to move. Every token is worth one point, tokens appear at random places "
        "every few seconds, and whoever holds the most tokens when time expires wins the match outright.",
        "A fast reflex contest where every player clicks targets as they appear on the shared screen "
        "with no turns at all, and the highest tally at the whistle takes the prize for the round. Targets shrink "
        "the longer they are left alone, so speed matters more than accuracy, and ties are settled by a rematch.",
        "Pieces move across a grid of squares toward the opposite edge, and a piece may capture any "
        "enemy on an adjacent square. Captured pieces leave the board for good, each side starts with eight pieces, "
        "and the first side to cross the whole board with a surviving piece wins the game for good.",
    ]
    for i, need in enumerate(["real_time", "real_time", "binding_agreements"]):
        inv.add(make(id=f"g{i}", name=f"G{i}", needs=[need], rules_text=texts[i]))
    assert inv.gaps().most_common() == [("real_time", 2), ("binding_agreements", 1)]


def test_recheck_moves_a_game_when_a_gap_closes():
    inv = inventory()
    inv.add(make(needs=["binding_agreements"]))
    assert inv.get("race").status == "blocked"

    manifest = copy.deepcopy(inv.manifest)
    manifest["version"] += 1
    manifest["needs"]["binding_agreements"]["verdict"] = "ok"
    inv.manifest = manifest
    assert inv.recheck() == [("race", "blocked", "ready")]
    assert inv.get("race").checked_with == manifest["version"]


def test_lifecycle_status_is_never_changed_by_a_gate():
    inv = inventory()
    inv.save(make(status="accepted", needs=["real_time"]))
    assert inv.check("race").status == "accepted"


# -- scope: games that are out by decision -------------------------------------


def test_a_spatial_game_is_rejected_not_blocked():
    rec = inventory().add(make(needs=["sequential_choice", "spatial_board"]))
    assert rec.status == "rejected" and rec.blocked_by == []
    assert rec.reasons[0].startswith("scope: spatial_board") and "spatial board" in rec.reasons[0]


def test_an_excluded_game_is_not_counted_as_an_engine_gap():
    inv = inventory()
    inv.add(make(needs=["spatial_board", "real_time"]))
    assert inv.get("race").status == "rejected"
    assert inv.gaps() == {}


def test_games_that_do_not_need_a_spatial_board_are_untouched_by_the_exclusion():
    for needs, hidden in ((["hidden_hands", "shared_deck_draw"], ["hands"]),   # a card game
                          (["private_values", "numeric_bids"], ["private_values"]),   # an auction
                          (["roles_with_allies", "elimination"], ["roles"])):   # a social deduction game
        assert status(inventory(), hidden=hidden, needs=needs) == "ready", needs


def test_recheck_turns_games_blocked_by_a_now_excluded_need_into_rejected():
    inv = inventory()
    inv.manifest["needs"]["spatial_board"]["verdict"] = "blocked"
    inv.add(make(needs=["spatial_board"]))
    assert inv.get("race").status == "blocked"
    inv.manifest = gates.load_manifest()  # the shipped manifest excludes it
    assert inv.recheck() == [("race", "blocked", "rejected")]


def test_the_rater_is_told_spatial_games_are_out():
    system = rate.system_prompt(gates.load_manifest())
    assert "Out of scope, never wanted: spatial_board" in system and "spatial board" in system
    assert "spatial_board" not in system.split("The engine cannot express:")[1].split("Out of scope")[0]


# -- verifiability and value -----------------------------------------------


def test_judged_outcome_is_tagged_not_stopped():
    rec = inventory().add(make(judged=True))
    assert rec.status == "ready" and rec.reward == "judged"


def test_value_override_wins():
    assert inventory().add(make(value_override=7)).value == 7


def test_a_famous_one_skill_copy_is_rejected_for_value():
    inv = inventory()
    inv.add(make())
    rec = inv.add(make(id="climb", name="Climb", contamination="famous", value_override=None,
        rules_text="Players alternately add to a running pile of stones, each taking up to four, and "
        "whoever takes the last stone loses. Both players see the pile at all times, no information "
        "is hidden, and nothing is left to chance, so only foresight decides the match."))
    assert rec.status == "rejected" and rec.reasons[0].startswith("value")


def test_queue_puts_new_mechanics_before_variants_of_ported_ones():
    inv = inventory()
    inv.save(make(id="old", name="Old", status="ported", port="x.json", rules_text="x " * 60))
    inv.add(make(id="variant", name="Variant", skills=["planning", "bluffing", "opponent_modeling"],
        rules_text="A variant of the old climbing game in which both players may also pass once. " * 5))
    inv.add(make(id="fresh", name="Fresh", hidden=["hands"], randomness="deal",
        rules_text="A game of hidden hands and claims that shares nothing with the others here. " * 5))
    assert [r.id for r in inv.queue()] == ["fresh", "variant"]


# -- the index ---------------------------------------------------------------


def test_summary_is_required_and_one_line():
    assert status(inventory(), summary="") == "incomplete"
    assert status(inventory(), summary="two\nlines") == "incomplete"
    assert status(inventory(), summary="x" * 141) == "incomplete"


def test_index_has_every_game_with_its_disposition():
    inv = inventory()
    inv.add(make())
    inv.add(make(id="rt", name="Real Time", needs=["real_time"], rules_text=
        "Players race across a live board grabbing tokens as they appear, with no turns at all and a clock "
        "that never stops. Every token is worth one point, tokens appear at random places every few seconds, "
        "and whoever holds the most tokens when time expires wins the match."))
    inv.save(make(id="old", name="Old", status="ported", port="x.json", rules_text=
        "Pieces move across a grid of squares toward the opposite edge, and a piece may capture any enemy on "
        "an adjacent square. Captured pieces leave the board for good, each side starts with eight pieces, "
        "and the first side across the board wins."))
    text = inv.index_path.read_text()
    rows = {l.split("|")[1].strip(" `"): l for l in text.splitlines() if l.startswith("| `")}
    assert set(rows) == {"race", "rt", "old"}
    assert "| covered |" in rows["old"] and "| queued |" in rows["race"]
    assert "| blocked |" in rows["rt"] and "blocked by real_time" in rows["rt"]
    assert "Two players race to a running total of fifty." in rows["race"]
    # covered first, then queued, then blocked
    assert text.index("`old`") < text.index("`race`") < text.index("`rt`")


def test_a_dropped_game_says_what_it_duplicates():
    inv = inventory()
    inv.add(make())
    inv.add(make(id="again", name="Race to Fifty"))
    row = next(l for l in inv.index_path.read_text().splitlines() if "`again`" in l)
    assert "| dropped |" in row and "duplicate of race" in row


def test_the_shipped_index_is_current():
    from generator import index
    inv = Inventory()
    if not inv.index_path.exists():  # the generated index is not committed; a fresh checkout has none
        return
    assert inv.index_path.read_text() == index.render(inv.all())
    assert inv.index_path.with_suffix(".json").read_text() == index.render_json(inv.all())


def test_the_json_index_lists_every_game_once_with_a_unique_id_and_its_state():
    inv = inventory()
    inv.add(make())
    inv.add(make(id="rt", name="Real Time", needs=["real_time"], rules_text=
        "Players race across a live board grabbing tokens as they appear, with no turns at all and a clock "
        "that never stops. Every token is worth one point, tokens appear at random places every few seconds, "
        "and whoever holds the most tokens when time expires wins the match."))
    inv.add(make(id="again", name="Race to Fifty"))
    rows = json.loads(inv.index_path.with_suffix(".json").read_text())
    assert [r["id"] for r in rows] == ["again", "race", "rt"]
    assert len({r["id"] for r in rows}) == len(rows) == len(inv.all())
    by = {r["id"]: r for r in rows}
    assert by["race"]["status"] == "ready" and by["race"]["disposition"] == "queued"
    assert by["rt"]["status"] == "blocked" and by["rt"]["note"] == "blocked by real_time"
    assert by["again"]["status"] == "duplicate" and by["again"]["duplicate_of"] == "race"


def test_two_records_with_one_id_are_refused_by_the_index():
    from generator import index
    a, b = make(), make()
    try:
        index.render_json([a, b])
    except ValueError as exc:
        assert "race" in str(exc)
    else:
        raise AssertionError("duplicate ids were indexed")


# -- the shipped inventory and the command line ------------------------------


def test_the_shipped_inventory_is_consistent_with_its_gates():
    """Every stored verdict is what the gates give today."""
    inv = Inventory()
    for rec in inv.all():
        again = gates.check(rec, inv.all(), inv.manifest)
        assert (again.status, again.reasons) == (rec.status, rec.reasons), rec.id


def test_the_manifest_loads_and_every_verdict_is_known():
    manifest = gates.load_manifest()
    assert manifest["needs"]
    assert {e["verdict"] for e in manifest["needs"].values()} <= {"ok", "workaround", "blocked", "excluded"}
    assert {e["basis"] for e in manifest["needs"].values()} <= {"documented", "assumed", "decided"}


def test_cli_add_list_and_gaps(capsys=None):
    root = Path(tempfile.mkdtemp())
    record = root / "in.json"
    record.write_text(json.dumps({**BASE, "needs": ["real_time"]}))
    assert main(["--dir", str(root / "inv"), "add", str(record)]) == 0
    assert main(["--dir", str(root / "inv"), "list", "--status", "blocked"]) == 0
    assert main(["--dir", str(root / "inv"), "gaps"]) == 0
    assert main(["--dir", str(root / "inv"), "show", "nope"]) == 1
