"""Revising the spec from a play review's findings."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import SPEC  # noqa: E402
from gen_game import revise, spec as specmod  # noqa: E402

REVIEW = {"verdict": "gaps", "findings": [
    {"id": "F1", "where": "setup", "observed": "the deck holds 12", "expected": "9", "category": "game_file", "fix": "remove what is dealt"},
    {"id": "F2", "where": "round 3", "observed": "everyone offered a block", "expected": "only the target", "category": "game_file", "fix": "per-seat offers"},
    {"id": "F5", "where": "round 14", "observed": "wrongly out", "expected": "in", "category": "game_file", "fix": "x"},
    {"id": "F6", "where": "brief", "observed": "empty list", "expected": "a list", "category": "engine", "fix": "engine"},
    {"id": "F7", "where": "round 2", "observed": "odd play", "expected": "-", "category": "players", "fix": "-"}]}


class Model:
    def __init__(self, reply):
        self.reply, self.prompts = reply, []

    def complete(self, prompt, system=""):
        self.prompts.append(prompt)
        return json.dumps(self.reply)


CHANGE = {"rules_add": [{"id": "R1", "text": "After the deal the deck holds 9 cards."}],
          "offers": [{"question": "the reaction", "who": "every seat but the actor", "options": "pass; block only for the target"}],
          "step_edits": [{"step": 1, "effect": "the corrected effect"}], "notes": "added the deal rule and the offers"}


def test_only_findings_a_spec_can_fix_and_a_person_did_not_reject_are_shown_to_the_model():
    m = Model(CHANGE)
    revised, change, error = revise.revise_spec(m, SPEC, REVIEW, drop=("F5",))
    assert error == "" and revised is not None
    shown = m.prompts[0]
    assert "F1" in shown and "F2" in shown
    assert "F5" not in shown and "F6" not in shown and "F7" not in shown  # dropped by a person; the engine's; the players'


def test_the_additions_are_merged_and_the_old_spec_is_untouched_and_a_clashing_id_takes_the_next_number():
    before = json.dumps(SPEC)
    revised, _, error = revise.revise_spec(Model(CHANGE), SPEC, REVIEW)
    assert error == "" and json.dumps(SPEC) == before
    ids = [r["id"] for r in revised["rules"]]
    assert len(ids) == len(set(ids)) and revised["rules"][-1]["text"] == "After the deal the deck holds 9 cards."
    assert revised["offers"][0]["question"] == "the reaction" and revised["round"][0]["effect"] == "the corrected effect"
    assert specmod.problems(revised) == []
    assert "OFFERS" in specmod.script(revised) and "the reaction | asked: every seat but the actor" in specmod.script(revised)


def test_a_reply_that_changes_nothing_is_sent_back_and_no_fixable_finding_means_no_call():
    _, _, error = revise.revise_spec(Model({"notes": "x"}), SPEC, REVIEW)
    assert "nothing was changed" in error
    m = Model(CHANGE)
    _, _, error = revise.revise_spec(m, SPEC, {"findings": [REVIEW["findings"][3]]})
    assert "no finding" in error and m.prompts == []


def test_save_keeps_the_old_spec_in_history_and_writes_the_new_one():
    import tempfile

    folder = Path(tempfile.mkdtemp())
    (folder / "spec.json").write_text(specmod.dumps(SPEC))
    revised, _, _ = revise.revise_spec(Model(CHANGE), SPEC, REVIEW)
    backup = revise.save(folder, revised)
    assert json.loads(backup.read_text())["name"] == SPEC["name"] and "rules" not in json.loads(backup.read_text())
    assert json.loads((folder / "spec.json").read_text())["offers"] and (folder / "SPEC.md").exists()


def test_the_designer_is_given_the_design_as_it_stands_and_the_findings_so_it_revises_rather_than_starts_again():
    from fixtures import PLAN
    from gen_game import adapt

    findings = [{"id": "I1.1", "severity": "major", "category": "game_file", "where": "setup", "observed": "the deck held 12 cards",
                 "expected": "9 cards after the deal", "fix": "remove what is dealt"},
                {"id": "I1.2", "severity": "minor", "category": "prompt", "where": "every turn", "observed": "constants in the state line",
                 "expected": "only what a player can use", "fix": "hide them"}]
    text = revise.compose_design_feedback(PLAN, findings)
    assert PLAN["variation"]["rules"][:40] in text and "THE DESIGN AS IT STANDS" in text           # the current design is in it
    assert "CONFIRMED (critical or major):" in text and "the deck held 12 cards" in text            # the confirmed finding
    assert "MINOR (fix them in this pass too):" in text and "constants in the state line" in text  # the minor one rides along
    assert "write the missing fact into the rules itself" in text and "Do not make the game simpler" in text

    seen = []

    class Capture:
        def complete(self, prompt, system=""):
            seen.append(prompt)
            return json.dumps(PLAN)

    record = {"name": "Rock Paper Scissors", "players_min": 2, "players_max": 2, "rules_text": "The idea as filed."}
    adapt.adapt(Capture(), record, text, idea=True)
    assert "The idea as filed." in seen[0] and PLAN["variation"]["rules"][:40] in seen[0] and "the deck held 12 cards" in seen[0]
    assert "Revise the variation to fix these" in seen[0]


def test_before_anything_is_rebuilt_every_artifact_of_the_old_version_is_kept_and_the_feedback_is_written():
    import tempfile

    from fixtures import PLAN

    folder = Path(tempfile.mkdtemp()) / "demo"
    folder.mkdir()
    (folder / "variation.json").write_text(json.dumps(PLAN))
    for name in ("spec.json", "game.json", "scenarios.json"):
        (folder / name).write_text('{"x": 1}')
    finding = {"severity": "major", "category": "game_file", "where": "setup", "observed": "o", "expected": "e", "fix": "f"}
    feedback, keep = revise.prepare_redesign(folder, [finding], 2)
    assert keep.name == "iteration-2" and keep.parent.name == "history"
    assert sorted(p.name for p in keep.iterdir()) == ["game.json", "scenarios.json", "spec.json", "variation.json"]
    assert json.loads((keep / "variation.json").read_text()) == PLAN and "CONFIRMED" in feedback
