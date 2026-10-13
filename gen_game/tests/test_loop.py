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

    def __init__(self, per_iteration, confirms=True, rebuilt="ready"):
        self.per_iteration, self.confirms, self.rebuilt = list(per_iteration), confirms, rebuilt
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
            return self.rebuilt

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


def judged(world, answer):
    hooks = world.hooks()
    hooks.judge = lambda plays, reviews, findings: answer(plays, reviews, findings)
    return hooks


def test_the_judge_can_ask_for_a_pass_over_a_minor_finding_and_that_finding_is_fixed():
    w = World([[finding(severity="minor", expected="the end screen lists every seat")], []])
    seen = {}

    def answer(plays, reviews, findings):
        seen.setdefault("ids", [f["id"] for f in findings])
        seen.setdefault("reviews", len(reviews))  # one review for each play of the pass
        return {"decision": "iterate" if w.iteration == 1 else "good_enough", "fix": ["I1.1"] if w.iteration == 1 else [], "reason": "players read a wrong tally",
                "result_reasonable": True, "aligned": True}

    res = loop.run_loop(judged(w, answer), max_iterations=3)
    assert seen == {"ids": ["I1.1"], "reviews": 2}
    assert res.status == "clean" and res.iterations == 2
    assert w.revised and w.revised[0][0]["by_judge"] is True
    assert "regenerate" in w.calls
    assert any("Judge:" in t and "iterate" in t for t in w.log_text)


def test_a_judge_that_says_good_enough_ends_the_loop_with_the_minor_findings_carried():
    w = World([[finding(severity="minor")]])
    res = loop.run_loop(judged(w, lambda *a: {"decision": "good_enough", "fix": [], "reason": "cosmetic", "result_reasonable": True, "aligned": True}), 3)
    assert res.status == "clean" and res.iterations == 1 and len(res.carried) == 1 and "regenerate" not in w.calls
    assert res.judgement["decision"] == "good_enough"


def test_a_judge_cannot_wave_away_a_confirmed_major_finding():
    w = World([[finding(severity="major")], []])
    res = loop.run_loop(judged(w, lambda *a: {"decision": "good_enough", "fix": [], "reason": "fine"}), 3)
    assert "regenerate" in w.calls and res.iterations == 2


def test_a_judge_that_cannot_answer_leaves_the_severity_rules_to_decide():
    w = World([[finding(severity="minor")]])
    res = loop.run_loop(judged(w, lambda *a: None), 3)
    assert res.status == "clean" and "regenerate" not in w.calls


def test_the_judge_is_not_asked_when_there_is_an_infra_finding_and_cannot_clear_it():
    w = World([[finding(category="infra", severity="minor")]])
    asked = []
    res = loop.run_loop(judged(w, lambda *a: asked.append(1)), 3)
    assert res.status == "escalated" and not asked


def test_the_judge_may_only_pick_findings_that_exist():
    w = World([[finding(severity="minor")]])
    res = loop.run_loop(judged(w, lambda *a: {"decision": "iterate", "fix": ["I9.9"], "reason": "x"}), 3)
    assert res.status == "clean" and "regenerate" not in w.calls


def test_a_rebuild_that_did_not_produce_a_checked_game_stops_the_loop_instead_of_playing_it():
    w = World([[finding()], []], rebuilt="scenarios_failed")
    res = loop.run_loop(w.hooks(), 3)
    assert res.status == "escalated" and res.iterations == 1 and w.calls.count("simulate") == 1
    assert w.escalations and "scenarios_failed" in w.escalations[0]
