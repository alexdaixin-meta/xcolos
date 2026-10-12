"""Reviewing a simulated play: the exact facts, the transcript the reviewer reads, and what a review must contain."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import playreview  # noqa: E402

SIM = {
    "players": ["muse", "muse"], "seed": 3,
    "snapshot": {"status": "ended", "winner": "seat 1", "round": 2},
    "events": {"records": [
        {"category": "fact", "type": "start", "round": 1, "audience": {"kind": "all"}, "payload": {"rendered": "Seat 1 plays tax."}},
        {"category": "orchestrator", "type": "action_request", "round": 1, "seat": 2, "action_schema": "react", "legal_targets": ["pass", "block"], "prompt": "React."},
        {"category": "turn", "type": "move", "round": 1, "seat": 2, "action_schema": "react", "action": {"target": "block"}},
        {"category": "orchestrator", "type": "action_request", "round": 1, "seat": 2, "action_schema": "react", "legal_targets": ["pass"], "prompt": "React."},
        {"category": "turn", "type": "move", "round": 1, "seat": 2, "action_schema": "react", "action": {"target": "pass"}},
        {"category": "model", "type": "model_call", "round": 1, "for": "seat 2", "model": "muse", "system": "S", "prompt": "P", "raw": "block", "seconds": 4.0},
        {"category": "model", "type": "model_call", "round": 1, "for": "seat 2", "model": "muse", "system": "S", "prompt": "P", "error": "down", "seconds": 1.0},
    ]},
}


def test_the_exact_facts_are_counted_from_the_log():
    s = playreview.stats(SIM)
    assert (s["decisions"], s["model_calls"], s["model_errors"], s["winner"]) == (2, 2, 1, "seat 1")
    assert any(f.startswith("refused:") for f in s["trace_lint"])  # offered `block`, taken, then asked again without it


def test_the_transcript_is_round_by_round_with_what_each_seat_was_offered_and_answered():
    t = playreview.compact_trace(SIM)
    assert "== round 1 ==" in t and "[ALL] Seat 1 plays tax." in t
    assert "seat 2 asked `react` with options ['pass', 'block']" in t and "seat 2 answers `react`: block" in t


def test_a_review_needs_a_verdict_findings_with_evidence_and_a_known_category():
    ok = {"verdict": "gaps", "findings": [{"where": "round 1", "observed": "a", "expected": "b", "category": "game_file", "fix": "c"}]}
    assert playreview.problems(ok) == []
    assert playreview.problems({"verdict": "aligned", "findings": []}) == []
    assert any("cannot come with findings" in p for p in playreview.problems({"verdict": "aligned", "findings": ok["findings"]}))
    bad = {"verdict": "gaps", "findings": [{"where": "x", "observed": "a", "expected": "b", "category": "luck", "fix": "c"}]}
    assert any("category must be one of" in p for p in playreview.problems(bad))
    assert any("verdict must be" in p for p in playreview.problems({"verdict": "maybe", "findings": []}))
