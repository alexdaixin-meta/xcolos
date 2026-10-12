"""The loop's rules, with the world (plays, reviews, a model) replaced by fakes."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import loop  # noqa: E402


def finding(category="game_file", severity="major", expected="the deck holds nine cards after the deal", where="setup"):
    return {"where": where, "observed": "what was seen", "expected": expected, "category": category, "severity": severity, "fix": "do it right"}


class World:
    """Plays that return scripted reviews, one list of findings per iteration."""

    def __init__(self, per_iteration, confirms=True):
        self.per_iteration, self.confirms = list(per_iteration), confirms
        self.calls, self.log_text, self.escalations, self.revised, self.iteration = [], [], [], [], 0

    def hooks(self):
        def simulate():
            self.iteration += 1
            self.calls.append("simulate")
            return [f"play-{self.iteration}a", f"play-{self.iteration}b"]

        def review(play):
            findings = self.per_iteration[min(self.iteration, len(self.per_iteration)) - 1] if play.endswith("a") else []
            return {"findings": [dict(f) for f in findings], "rules_not_seen": ["R9", "R4"] if play.endswith("a") else ["R9"]}

        def confirm(play, f):
            self.calls.append("confirm")
            return self.confirms, "checked"

        def revise(findings):
            self.calls.append("revise")
            self.revised.append(findings)
            return True, "added rules"

        def regenerate():
            self.calls.append("regenerate")
            return "ready"

        return loop.Hooks(simulate, review, confirm, revise, regenerate, self.log_text.append, self.escalations.append, say=lambda m: None)


def test_a_play_with_nothing_critical_or_major_ends_the_loop_and_minor_findings_are_only_carried():
    w = World([[finding(severity="minor", expected="the state line prints constants")]])
    r = loop.run_loop(w.hooks())
    assert r.status == "clean" and r.iterations == 1 and len(r.carried) == 1
    assert "revise" not in w.calls and "regenerate" not in w.calls  # a minor finding never starts a pass
    assert r.rules_never_seen == ["R9"]  # seen by neither play: the rules in common


def test_a_confirmed_major_finding_revises_and_regenerates_and_the_open_minor_ones_go_with_it():
    w = World([[finding(), finding(severity="minor", expected="a header is repeated")], []])
    r = loop.run_loop(w.hooks())
    assert r.status == "clean" and r.iterations == 2 and len(r.fixed) == 1
    assert w.calls.count("regenerate") == 1
    assert sorted(f["severity"] for f in w.revised[0]) == ["major", "minor"]


def test_a_major_finding_nothing_confirms_is_not_acted_on_and_is_left_for_a_person():
    w = World([[finding()]], confirms=None)
    r = loop.run_loop(w.hooks())
    assert r.status == "clean" and "revise" not in w.calls and len(r.unconfirmed) == 1
    refuted = World([[finding()]], confirms=False)
    assert loop.run_loop(refuted.hooks()).status == "clean" and "revise" not in refuted.calls


def test_any_infra_finding_stops_the_loop_before_anything_is_changed_and_is_written_down():
    w = World([[finding(category="infra", severity="minor", expected="the summary call failed"), finding()]])
    r = loop.run_loop(w.hooks())
    assert r.status == "escalated" and "revise" not in w.calls and "regenerate" not in w.calls
    assert w.escalations and "infra findings" in w.escalations[0] and "Nothing was changed" in w.escalations[0]


def test_a_fixed_finding_that_comes_back_is_escalated_and_so_is_running_out_of_passes():
    back = World([[finding()], [finding()]])
    r = loop.run_loop(back.hooks())
    assert r.status == "escalated" and "came back" in back.escalations[0] and back.calls.count("regenerate") == 1
    always = World([[finding(expected="one thing")], [finding(expected="something wholly different here")], [finding(expected="a third unrelated matter at all")]])
    r = loop.run_loop(always.hooks(), max_iterations=3)
    assert r.status == "max_iterations" and r.iterations == 3 and always.escalations and "Out of passes" in always.escalations[-1]


def test_findings_about_the_players_own_play_are_ignored_and_the_same_finding_in_two_plays_is_one():
    w = World([[finding(category="players", expected="odd play")]])
    assert loop.run_loop(w.hooks()).status == "clean" and "confirm" not in w.calls
    both = [finding(), finding()]
    merged = loop._merge([{**f, "plays": [p]} for f, p in zip(both, ("a", "b"))])
    assert len(merged) == 1 and merged[0]["plays"] == ["a", "b"]
