"""The reasoning-and-planning check: did winning take thought, read from what the players actually said?"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gen_game import reasoning  # noqa: E402

HINT = "Seat 2 holds R1 and doesn't know it. A red hint touches only #5, so they can play it next turn.\n\nHINT 2 R"
PLAY = "Seat 1 hinted red on #5 only, and red is at 0, so #5 must be R1.\n\nPLAY #5"
SIM = {
    "players": ["muse", "muse"], "seed": 1,
    "snapshot": {"status": "ended", "winner": "all seats win", "summary": "All seats win. Team score 13 of 15."},
    "events": {"records": [
        {"category": "fact", "type": "start", "round": 1, "audience": {"kind": "all"}, "payload": {"rendered": "Piles: R 0, G 0, B 0."}},
        {"category": "model", "type": "model_call", "turn_seq": 1, "for": "seat 1", "raw": HINT},
        {"category": "turn", "type": "move", "round": 1, "turn_seq": 1, "seat": 1, "legal_targets": ["PLAY #1", "HINT 2 R"], "action": {"target": "HINT 2 R"}},
        {"category": "fact", "type": "turn", "round": 1, "audience": {"kind": "all"}, "payload": {"rendered": "turn 1: seat 1 hints seat 2 R = #5."}},
        {"category": "model", "type": "model_call", "turn_seq": "2", "for": "seat 2", "raw": PLAY},
        {"category": "turn", "type": "move", "round": 2, "turn_seq": 2, "seat": 2, "legal_targets": ["PLAY #5", "DISCARD #5"], "action": {"target": "PLAY #5"}},
        {"category": "model", "type": "model_call", "turn_seq": 3, "for": "seat 1", "raw": "PASS"},
        {"category": "turn", "type": "move", "round": 3, "turn_seq": 3, "seat": 1, "legal_targets": ["PASS"], "action": {"target": "PASS"}},
    ]},
}
DESIGN = {"variation": {"name": "Tiny Hanabi", "rules": "R1 Hints touch every matching card.", "expected_effect": "Players infer their cards from hints."}}


def good_check(quote: str = "A red hint touches only #5") -> dict:
    return {
        "reasoning": {"score": 3, "notes": "every play rests on a hint", "evidence": [{"match": 1, "turn": 2, "seat": 2, "quote": "red is at 0, so #5 must be R1", "shows": "infers its card"}]},
        "planning": {"score": 2, "notes": "hints set up the next turn", "evidence": [{"match": 1, "turn": 1, "seat": 1, "quote": quote, "shows": "sets up a play"}]},
        "luck": {"score": 0, "notes": "no draw decided anything", "evidence": []},
        "weak_spots": [],
        "summary": "Both seats reason from hints.",
    }


class Scripted:
    def __init__(self, *replies: dict) -> None:
        self.replies = [json.dumps(r) for r in replies]
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        return self.replies[min(len(self.prompts), len(self.replies)) - 1]


def test_each_choice_comes_with_the_players_own_words_and_forced_moves_are_left_out():
    got = reasoning.decisions(SIM)
    assert [(d["turn"], d["seat"], d["chose"]) for d in got] == [(1, 1, "HINT 2 R"), (2, 2, "PLAY #5")]
    assert "touches only #5" in got[0]["said"] and got[0]["options"] == ["PLAY #1", "HINT 2 R"]
    assert got[1]["before"] == ["turn 1: seat 1 hints seat 2 R = #5."]  # what the table was told since the last choice


def test_the_exact_facts_count_choices_and_replies_that_give_reasons():
    bare = json.loads(json.dumps(SIM))
    bare["events"]["records"][4]["raw"] = "PLAY #5"  # an answer with no reason given
    s = reasoning.stats([SIM, bare])
    assert (s["matches"], s["decisions"], s["with_reasons"]) == (2, 4, 3)
    assert s["results"] == {"all seats win": 2}


def test_a_check_needs_scores_from_0_to_3_and_quotes_that_are_in_the_cited_reply():
    found = reasoning.decisions(SIM)
    assert reasoning.problems(good_check(), [found]) == []
    assert reasoning.problems(good_check(quote="touches only #5 ... next turn"), [found]) == []  # a quote may skip words with an ellipsis
    assert any("not found" in p for p in reasoning.problems(good_check(quote="I counted every card"), [found]))
    off = good_check()
    off["luck"]["score"] = 5
    assert any("luck.score" in p for p in reasoning.problems(off, [found]))
    bare = good_check()
    bare["planning"]["evidence"] = []
    assert any("planning" in p and "evidence" in p for p in reasoning.problems(bare, [found]))


def test_the_verdict_follows_the_scores():
    v = reasoning.verdict
    assert v({"reasoning": {"score": 3}, "planning": {"score": 2}, "luck": {"score": 1}}) == "strong"
    assert v({"reasoning": {"score": 2}, "planning": {"score": 2}, "luck": {"score": 2}}) == "adequate"
    assert v({"reasoning": {"score": 1}, "planning": {"score": 3}, "luck": {"score": 0}}) == "weak"
    assert v({"reasoning": {"score": 3}, "planning": {"score": 3}, "luck": {"score": 3}}) == "weak"


def test_a_made_up_quote_is_sent_back_and_the_corrected_check_is_kept():
    model = Scripted(good_check(quote="I counted every card"), good_check())
    result, error = reasoning.check(model, [SIM], DESIGN)
    assert error == "" and result["verdict"] == "strong"
    assert len(model.prompts) == 2 and "REFUSED" in model.prompts[1] and "not found" in model.prompts[1]
    assert "Players infer their cards from hints." in model.prompts[0] and "touches only #5" in model.prompts[0]


def test_the_reasoning_command_reads_the_play_logs_and_writes_the_report():
    from gen_game.cli import main

    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "tiny"
        (folder / "sim").mkdir(parents=True)
        (folder / "variation.json").write_text(json.dumps(DESIGN))
        (folder / "sim" / "w0001-seed1.json").write_text(json.dumps(SIM))
        (folder / "sim" / "w0001-seed1.review.json").write_text("{}")  # a play review, not a play
        assert main(["--root", d, "reasoning", "tiny", "--model", "echo:" + json.dumps(good_check())]) == 0
        report = (folder / "REASONING.md").read_text()
        assert "strong" in report and "red is at 0, so #5 must be R1" in report
        assert json.loads((folder / "reasoning.json").read_text())["stats"]["matches"] == 1


def test_the_loops_reasoning_hook_checks_an_iterations_plays_and_writes_the_report():
    from gen_game.cli import reasoning_hook

    with tempfile.TemporaryDirectory() as d:
        folder = Path(d) / "tiny"
        (folder / "sim").mkdir(parents=True)
        (folder / "variation.json").write_text(json.dumps(DESIGN))
        play = folder / "sim" / "w0001-seed1.json"
        play.write_text(json.dumps(SIM))
        said: list[str] = []
        out = reasoning_hook(folder, Scripted(good_check()), said.append)([str(play)])
        assert out["verdict"] == "strong" and (folder / "REASONING.md").exists()
        assert reasoning_hook(folder, Scripted({"nonsense": True}), said.append)([str(play)]) is None
        assert any("reasoning check failed" in s for s in said)


def test_a_play_test_is_followed_by_the_reasoning_check_unless_it_is_skipped():
    from gen_game.cli import parser

    a = parser().parse_args(["simulate", "tiny", "--players", "muse"])
    assert (a.no_reasoning, a.reasoning_model) == (False, "gateway|muse")
    assert parser().parse_args(["simulate", "tiny", "--players", "muse", "--no-reasoning"]).no_reasoning


def test_plays_whose_players_give_no_reasons_are_unmeasured_and_no_model_is_asked():
    bare = json.loads(json.dumps(SIM))
    for r in bare["events"]["records"]:
        if r.get("type") == "model_call":
            r["raw"] = r["raw"].splitlines()[-1]  # the answer alone
    model = Scripted(good_check())
    result, error = reasoning.check(model, [bare], DESIGN)
    assert error == "" and result["verdict"] == "unmeasured" and model.prompts == []
    assert "0 of 2" in result["summary"]
    assert "unmeasured" in reasoning.render(result, reasoning.stats([bare]), "Tiny")


def test_choices_between_numbers_are_read_too():
    numbers = json.loads(json.dumps(SIM))
    move = numbers["events"]["records"][2]
    move["legal_targets"], move["action"]["target"] = [1, 2, 3], 2
    numbers["events"]["records"][1]["raw"] = "Seat 2 holds the card I need, and only a bid of 2 keeps my coins for the next round.\n\n2"
    assert "offered [1, 2, 3]; chose '2'" in reasoning.transcript([numbers])
    assert reasoning.decisions(numbers)[0]["said"].endswith("for the next round.")


def test_bids_and_messages_are_choices_and_a_forced_move_is_not():
    sim = {"players": ["gateway"] * 2, "snapshot": {"status": "ended", "winner": "seat 1"}, "events": {"records": [
        {"category": "model", "type": "model_call", "turn_seq": 1, "for": "seat 1", "raw": "Claiming a top card may scare others off, so I win this item cheaply.\n\nI drew a 16 this round."},
        {"category": "turn", "type": "move", "turn_seq": 1, "seat": 1, "legal_targets": [], "action": {"target": None, "text": "I drew a 16 this round."}},
        {"category": "model", "type": "model_call", "turn_seq": 2, "for": "seat 2", "raw": "My value is 10 and the bid is 4, so raising to 6 still leaves me a profit of four.\n\n6"},
        {"category": "turn", "type": "move", "turn_seq": 2, "seat": 2, "legal_targets": ["DROP"], "action": {"target": 6, "text": ""}},
        {"category": "turn", "type": "move", "turn_seq": 3, "seat": 1, "legal_targets": ["PASS"], "action": {"target": "PASS", "text": ""}},
    ]}}
    got = reasoning.decisions(sim)
    assert [(d["turn"], d["chose"]) for d in got] == [(1, "I drew a 16 this round."), (2, "6")]
    assert got[0]["said"].startswith("Claiming a top card") and got[1]["said"].endswith("profit of four.")
    shown = reasoning.transcript([sim])
    assert "offered [a message]" in shown and "offered [a number, or DROP]" in shown


def test_plays_with_no_choices_are_unmeasured_and_no_model_is_asked():
    empty = json.loads(json.dumps(SIM))
    empty["events"]["records"] = [r for r in empty["events"]["records"] if r.get("category") != "turn"]
    model = Scripted(good_check())
    result, _ = reasoning.check(model, [empty], DESIGN)
    assert result["verdict"] == "unmeasured" and model.prompts == []


def test_a_message_gives_its_own_reasons_so_table_talk_never_leaves_plays_unmeasured():
    talk = "Seat 2, the big monsters seem scarce, so the Spear is the cheapest thing to give up."
    records = []
    for n in range(1, 4):  # three messages that are only the message, as table talk is
        records += [{"category": "model", "type": "model_call", "turn_seq": n, "for": "seat 1", "raw": talk},
                    {"category": "turn", "type": "move", "turn_seq": n, "seat": 1, "legal_targets": [], "action": {"target": None, "text": talk}}]
    records += [{"category": "model", "type": "model_call", "turn_seq": 4, "for": "seat 2", "raw": "PASS"},
                {"category": "turn", "type": "move", "turn_seq": 4, "seat": 2, "legal_targets": ["ADD", "PASS"], "action": {"target": "PASS"}}]
    sim = {"players": ["gateway"] * 2, "snapshot": {"status": "ended", "winner": "seat 1"}, "events": {"records": records}}
    assert reasoning.stats([sim])["with_reasons"] == 3
    cites = good_check()
    for aspect in ("reasoning", "planning"):  # quotes from the message itself are found in what the seat said
        cites[aspect]["evidence"] = [{"match": 1, "turn": 1, "seat": 1, "quote": "the big monsters seem scarce", "shows": "reads the deck"}]
    result, error = reasoning.check(Scripted(cites), [sim], DESIGN)
    assert error == "" and result["verdict"] != "unmeasured"
