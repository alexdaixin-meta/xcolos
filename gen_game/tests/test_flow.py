"""The flow: design (designer and critic), build (coder), test, and triage of every failure.

A scripted completion plays every model, so what is tested is the flow's own logic: who is asked
what, in what order, and what each answer causes.
"""

from __future__ import annotations

import json
import stat
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import (ALWAYS_ROCK, CRITIC_OK, PLAN, RPS, RPS_TEXT, SEAT1_WINS, SPEC, Models, critic_fails, record, run_flow, triage_says, world)  # noqa: E402

from gen_game import adapt as adaptmod  # noqa: E402
from gen_game import agent, complexity, critic, evaluate, flow, prompt, triage  # noqa: E402


def calls(m: Models) -> list[str]:
    return m.calls


def designer_prompts(m: Models) -> list[str]:
    return [p for p, c in zip(m.prompts, m.calls) if c == "adapt"]


def wrong_game() -> str:
    g = json.loads(RPS_TEXT)
    for a in g["attributes"]["game"]:
        if a["key"] == "rounds_left":
            a["initial"] = 3  # three rounds, not ten: the scenarios will say so
    return json.dumps(g)


# -- the designer and the critic ---------------------------------------------


def test_the_designer_works_from_the_goal_and_the_restrictions_not_the_file_format():
    system = adaptmod.system_prompt()
    for must in ("BALANCED", "PLAYABLE", "REASONING", "do not design with it", "spatial_board"):
        assert must in system
    head = system.split("What the engine supports")[0]
    for api in ("design/actions.md", "`poll`", "visible:", "\"use\""):
        assert api not in head and api not in system


def test_the_critic_checks_balance_playability_and_reasoning_over_luck_and_must_show_its_work():
    system = critic.system_prompt()
    for must in ("balanced", "playable", "reasoning_over_luck", "SHOW YOUR WORK", "thoughtless policy", "payoff"):
        assert must in system
    assert "design/actions.md" not in system


def test_a_review_needs_all_three_verdicts_with_evidence_and_failures_need_changes():
    assert critic.problems(CRITIC_OK) == []
    assert any("balanced" in p for p in critic.problems({**CRITIC_OK, "balanced": {"verdict": "maybe", "evidence": "x"}}))
    assert any("required_changes" in p for p in critic.problems({**CRITIC_OK, "playable": {"verdict": "fail", "evidence": "x"}}))
    assert critic.problems("nope")


def test_soundness_is_decided_from_the_verdicts_not_the_critics_own_claim():
    claimed = {**critic_fails("balanced"), "sound": True}
    got, err = critic.review(Models(critics=[claimed]), record().to_dict(), PLAN)
    assert err == "" and got["sound"] is False


def test_a_critic_that_fails_the_first_design_sends_the_findings_to_the_designer():
    inv, root = world()
    m = Models(critics=[critic_fails("balanced", change="make the mixed payoffs unequal"), CRITIC_OK],
               plans=[PLAN, {**PLAN, "variation": {**PLAN["variation"], "name": "Rebalanced"}}])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m)[:5] == ["adapt", "critic", "adapt", "critic", "spec"]
    second = designer_prompts(m)[1]
    assert "balanced FAILED" in second and "make the mixed payoffs unequal" in second
    assert "Rock Paper Scissors, weighted" in second  # the designer is shown the variation that was rejected
    saved = json.loads((root / "rps" / "variation.json").read_text())
    assert saved["critic"]["rounds"] == 2 and saved["critic"]["sound"] is True and saved["variation"]["name"] == "Rebalanced"


def test_nothing_is_built_until_the_critic_passes_the_rules():
    inv, root = world()
    m = Models(critics=[critic_fails("reasoning_over_luck")])
    run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert "spec" not in calls(m) and "encode" not in calls(m)


def test_a_design_the_critic_never_passes_is_dropped_as_too_simple_with_the_critics_reason():
    inv, root = world()
    m = Models(critics=[critic_fails("balanced")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "dropped" and out.detail.startswith("too simple: no design got past the critic")
    assert calls(m).count("adapt") == flow.CRITIC_ROUNDS == calls(m).count("critic")
    assert "balanced" in out.detail and inv.get("rps").dropped


def test_a_design_that_is_not_playable_is_dropped_as_too_complex():
    inv, root = world()
    out = run_flow("rps", Models(critics=[critic_fails("playable", "balanced")]), inv, root, adapt=True, judge=True)
    assert out.verdict == "dropped" and out.detail.startswith("too complex:")


def test_a_critic_outage_stops_the_flow_without_dropping_the_game():
    class Down(Models):
        def complete(self, prompt, system=""):
            if system.startswith("You are a strict reviewer"):
                raise RuntimeError("503")
            return super().complete(prompt, system)
    inv, root = world()
    out = run_flow("rps", Down(), inv, root, adapt=True, judge=True)
    assert out.verdict == "adapt_failed" and "critic" in out.detail
    assert inv.get("rps").status == "ready" and not inv.get("rps").dropped


# -- the happy path -------------------------------------------------------------


def test_the_flow_designs_reviews_specs_builds_tests_and_evaluates():
    inv, root = world()
    m = Models()
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m) == ["adapt", "critic", "spec", "scenarios", "encode"]  # the tests are written from the spec before the file; they do not decide whether it was written
    assert "weighted" in m.prompts[2] and "Two players each hold hidden cards" not in m.prompts[2]  # the spec saw the variation
    folder = root / "rps"
    for name in ("variation.json", "VARIATION.md", "spec.json", "game.json", "scenarios.json", "report.json", "REPORT.md"):
        assert (folder / name).exists(), name
    report = (folder / "REPORT.md").read_text()
    assert "## The critic" in report and "balanced: pass" in report
    assert inv.get("rps").status == "evaluated"


def test_the_designer_is_never_shown_the_file_format_but_the_coder_is():
    inv, root = world()
    m = Models()
    run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert "design/actions.md" not in designer_prompts(m)[0]
    assert "The complete file format" not in adaptmod.system_prompt()
    assert "THE FORMAT" in __import__("gen_game.encode", fromlist=["x"]).system_prompt()


# -- triage: whose problem is it? ---------------------------------------------------


def test_triage_knows_the_three_outcomes_and_when_to_stop():
    system = triage.system_prompt()
    for must in ("fix_game", "revise_rules", "platform_limit", "Choose this only when the evidence shows"):
        assert must in system
    assert triage.problems(triage_says("fix_game")) == []
    assert any("missing" in p for p in triage.problems(triage_says("platform_limit")))
    assert any("guidance" in p for p in triage.problems({**triage_says("fix_game"), "guidance": ""}))
    assert triage.problems({"decision": "shrug"})


def test_by_default_the_tests_are_written_first_and_the_coder_is_judged_only_on_whether_the_file_works():
    inv, root = world()
    m = Models(games=[wrong_game()], triages=[triage_says("fix_game", "set rounds_left to 10")])
    # a game that runs fine but does not follow the rules (three rounds, not ten): the coder's loop accepts it
    stop_early = run_flow("rps", m, inv, root)  # no design step, no triage
    assert stop_early.verdict == "needs_review"
    assert calls(m) == ["spec", "scenarios", "encode"]  # the tests are written first; one coder call: it was not refused for what the tests say
    assert (root / "rps" / "game.json").exists()  # the file was written and stands
    report = json.loads((root / "rps" / "report.json").read_text())
    assert report["tier0"]["passed"] and any(not o["passed"] for o in report["scenarios"])  # works on the platform; does not follow the rules
    text = (root / "rps" / "REPORT.md").read_text()
    assert "Works on the platform" in text and "Fidelity to the rules" in text and "do not decide whether the file works" in text


def test_the_tests_can_still_be_put_inside_the_coders_own_loop_when_asked():
    inv, root = world()
    m = Models(games=[wrong_game(), RPS_TEXT])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, fidelity_in_loop=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m)[3:6] == ["scenarios", "encode", "encode"] and "triage" not in calls(m)
    retry = [p for p, c in zip(m.prompts, m.calls) if c == "encode"][1]
    assert "tests written independently from the rules disagree with the game" in retry and "rounds_left" in retry


def test_a_game_that_works_but_breaks_the_rules_is_sent_back_by_triage_with_guidance_and_the_rules_are_left_alone():
    inv, root = world()
    m = Models(games=[wrong_game(), RPS_TEXT], triages=[triage_says("fix_game", "set rounds_left to 10, the rules say ten rounds")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m).count("adapt") == 1 and calls(m).count("critic") == 1  # the design was not revisited
    assert calls(m).count("encode") == 2 and calls(m).count("triage") == 1
    retry = [p for p, c in zip(m.prompts, m.calls) if c == "encode"][1]
    assert "set rounds_left to 10" in retry and "## Guidance from the last attempt" in retry
    triage_prompt = [p for p, c in zip(m.prompts, m.calls) if c == "triage"][0]
    assert "what the game did on" in triage_prompt and "moves played:" in triage_prompt  # triage sees what the game did, not just the verdict
    report = json.loads((root / "rps" / "report.json").read_text())
    assert [d["decision"] for d in report["triage"]] == ["fix_game"]


def test_a_problem_in_the_rules_goes_back_to_the_designer_with_triages_guidance():
    inv, root = world()
    m = Models(games=[wrong_game(), RPS_TEXT], plans=[PLAN, {**PLAN, "variation": {**PLAN["variation"], "name": "Simpler"}}],
               triages=[triage_says("revise_rules", "drop the talk phase; the rules cannot be built as written")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m).count("adapt") == 2
    assert "drop the talk phase" in designer_prompts(m)[1]
    old = root / "rps" / "history" / "round_1"
    assert (old / "variation.json").exists() and (old / "game.json").exists()


def test_when_the_platform_cannot_do_it_the_flow_stops_and_records_exactly_what_is_missing():
    inv, root = world()
    m = Models(games=[wrong_game()], triages=[triage_says("platform_limit", missing="one player proposing an exchange that another accepts")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "platform_limit" and "exchange" in out.detail
    assert calls(m).count("adapt") == 1 and calls(m).count("triage") == 1  # nothing more was tried after the stop
    assert "exchange" in (root / "rps" / "PLATFORM_LIMIT.md").read_text()
    rec = inv.get("rps")
    assert rec.status == "blocked" and rec.blocked_by == ["unmapped: one player proposing an exchange that another accepts"]
    assert inv.gaps().most_common() == [("unmapped: one player proposing an exchange that another accepts", 1)]
    assert not rec.dropped  # blocked, not dropped: it returns when the engine can do it


def test_a_spec_that_lists_unsupported_needs_goes_to_triage_not_to_the_coder():
    inv, root = world()
    m = Models(spec={**SPEC, "unsupported": ["a shared market where players trade cards"]},
               triages=[triage_says("platform_limit", missing="trading cards between players")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "platform_limit" and "encode" not in calls(m)
    assert "market" in [p for p, c in zip(m.prompts, m.calls) if c == "triage"][0]


def test_unsupported_needs_that_the_designer_can_remove_send_the_rules_back():
    inv, root = world()
    m = Models(spec={**SPEC, "unsupported": ["a spatial board"]}, plans=[PLAN, PLAN],
               triages=[triage_says("revise_rules", "remove the board; use a simple track")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, design_rounds=2)
    assert calls(m).count("adapt") == 2 and "remove the board" in designer_prompts(m)[1]


def test_a_design_flaw_found_by_evaluation_goes_to_triage_and_back_to_the_designer():
    real, count = evaluate.tier1, []

    def flagged_then_clean(defn, seeds=range(1, 61)):
        count.append(1)
        out = real(defn, seeds=range(1, 6))
        return {**out, "flags": ["always taking the first option as seat 1 wins 90% of decided matches against random seats"]} if len(count) == 1 else out
    evaluate.tier1 = flagged_then_clean
    try:
        inv, root = world()
        m = Models(plans=[PLAN, {**PLAN, "variation": {**PLAN["variation"], "name": "Revised"}}],
                   triages=[triage_says("revise_rules", "make the first option risky")])
        out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    finally:
        evaluate.tier1 = real
    assert out.verdict == "ready_for_review", out
    assert calls(m).count("adapt") == 2
    assert "wins 90%" in designer_prompts(m)[1] and "make the first option risky" in designer_prompts(m)[1]
    assert "wins 90%" in (root / "rps" / "history" / "round_1" / "REPORT.md").read_text()
    assert json.loads((root / "rps" / "report.json").read_text())["design_rounds"] == 2


def test_a_flaw_that_survives_every_round_drops_the_game_as_too_simple():
    real = evaluate.tier1
    evaluate.tier1 = lambda defn, seeds=range(1, 61): {**real(defn, seeds=range(1, 6)), "flags": ["every random match ended 'draw'"]}
    try:
        inv, root = world()
        m = Models()
        out = run_flow("rps", m, inv, root, adapt=True, judge=True, design_rounds=2)
    finally:
        evaluate.tier1 = real
    assert out.verdict == "dropped" and out.detail.startswith("too simple: it is still degenerate or luck-driven: every random match ended 'draw'")
    assert "after 2 variation(s)" in out.detail
    rec = inv.get("rps")
    assert rec.status == "rejected" and rec.dropped == out.detail
    note = (root / "rps" / "DROPPED.md").read_text()
    assert "round 1" in note and "round 2" in note and "clear `dropped`" in note
    inv.check("rps")
    assert inv.get("rps").status == "rejected"


def test_a_game_that_keeps_failing_its_scenarios_is_dropped_as_too_complex_after_the_last_round():
    wrong = {**ALWAYS_ROCK, "expect": {"result": "seat 1"}}
    inv, root = world()
    m = Models(scenario_lists=[[wrong]], triages=[triage_says("revise_rules", "simplify")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, design_rounds=2)
    assert out.verdict == "dropped" and out.detail.startswith("too complex: it could not be built to behave as designed")
    assert calls(m).count("adapt") == 2


def test_a_built_game_over_the_limits_is_too_large_and_a_persistent_one_is_dropped_for_it():
    inv, root = world()
    claims_small = {**PLAN, "complexity": {**PLAN["complexity"], "steps_per_round": 4}}  # the design says 4; the built file has 22
    out = run_flow("rps", Models(plans=[claims_small]), inv, root, adapt=True, judge=True, design_rounds=2, steps=5)
    assert out.verdict == "dropped" and out.detail.startswith("too complex: it is too large for the platform")
    assert "steps per round" in out.detail


def test_triage_that_cannot_decide_stops_without_dropping_anything():
    class NoTriage(Models):
        def complete(self, prompt, system=""):
            if system.startswith("A game design for XColos"):
                raise RuntimeError("503")
            return super().complete(prompt, system)
    inv, root = world()
    out = run_flow("rps", NoTriage(games=[wrong_game()]), inv, root, adapt=True, judge=True)
    assert out.verdict == "needs_review" and "could not decide whose problem" in out.detail
    assert inv.get("rps").status == "ready" and not inv.get("rps").dropped


def test_without_the_design_step_a_disagreeing_test_is_reported_for_a_person_and_triage_is_not_asked():
    wrong = {**ALWAYS_ROCK, "expect": {"result": "seat 1"}}
    inv, root = world()
    m = Models(scenario_lists=[[wrong]])
    out = run_flow("rps", m, inv, root)  # adapt off
    assert out.verdict == "needs_review" and "triage" not in calls(m)
    assert inv.get("rps").status == "ready" and "FAIL" in (root / "rps" / "REPORT.md").read_text()
    assert (root / "rps" / "game.json").exists()  # the file works; only the fidelity check disagrees


# -- the designer can drop a game; a backend outage never does -----------------------------


def test_the_designer_can_recommend_dropping_a_game_and_nothing_else_runs():
    drop = {**PLAN, "recommendation": {"decision": "drop", "kind": "too_simple",
                                       "reason": "Every move is visible and one option always wins; nothing inside the limits changes that."}}
    del drop["variation"], drop["complexity"]
    inv, root = world()
    m = Models(plans=[drop])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "dropped" and out.detail.startswith("too simple: Every move is visible")
    assert calls(m) == ["adapt"]
    assert "Recommended drop" in (root / "rps" / "VARIATION.md").read_text()
    row = next(l for l in inv.index_path.read_text().splitlines() if "`rps`" in l)
    assert "| dropped |" in row and "too simple" in row


def test_a_variation_over_the_complexity_limits_is_sent_back_and_one_that_never_fits_is_dropped():
    big = {**PLAN, "complexity": {**PLAN["complexity"], "steps_per_round": complexity.LIMITS["steps_per_round"] + 5}}
    m = Models(plans=[big])
    plan, err = adaptmod.adapt(m, record().to_dict())
    assert plan is None and adaptmod.only_too_complex(err) and "simplify:" in m.prompts[1]
    inv, root = world()
    out = run_flow("rps", Models(plans=[big]), inv, root, adapt=True, judge=True, steps=complexity.LIMITS["steps_per_round"])
    assert out.verdict == "dropped" and out.detail.startswith("too complex: the designer could not bring")


def test_a_dropped_game_is_not_converted_again_until_the_reason_is_cleared():
    inv, root = world()
    run_flow("rps", Models(plans=[{**PLAN, "recommendation": {"decision": "drop", "kind": "too_complex",
             "reason": "Needs four roles and a long chain of conditional rules."}}]), inv, root, adapt=True, judge=True)
    out = run_flow("rps", Models(), inv, root, adapt=True, judge=True)
    assert out.verdict == "needs_review" and "dropped" in out.detail
    inv.save(__import__("dataclasses").replace(inv.get("rps"), dropped=""))
    assert inv.check("rps").status == "ready"


def test_a_backend_outage_while_building_is_not_a_reason_to_drop_a_game():
    class DownOnEncode(Models):
        def complete(self, prompt, system=""):
            if system.startswith("You write game files"):
                raise RuntimeError("503")
            return super().complete(prompt, system)
    m = DownOnEncode()
    inv, root = world()
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, encoder=agent.CompletionEncoder(m, pause=lambda s: None))
    assert out.verdict == "encode_failed" and inv.get("rps").status == "ready" and not inv.get("rps").dropped


# -- the coding agent --------------------------------------------------------------


def test_the_agent_prompt_carries_the_rules_the_interface_the_api_and_how_to_check():
    text = prompt.build("rps", PLAN, SPEC, "fix the payoffs")
    for must in ("Rock Paper Scissors, weighted", "higher total score", "`score`", "`seat 1`", "design/actions.md", "xcolos/games/library/rps.json",
                 "python3 -m gen_game verify rps game", "never `none`", "Do NOT read", "fix the payoffs", "platform genuinely cannot"):
        assert must in text, must
    assert "gen_game/data/games/rps/game.json" in text


def test_an_agent_is_a_command_that_reads_the_prompt_on_stdin_in_the_repository():
    assert agent.agent_for("claude").argv[:2] == ["claude", "-p"]
    assert agent.agent_for("metacode:some-model").argv[:4] == ["metacode", "run", "--model", "some-model"]
    muse = agent.agent_for("muse:some-model").argv
    assert muse[:4] == ["muse", "exec", "--model", "some-model"] and "--prompt-file" in muse and "{prompt_file}" in muse
    assert "--dangerously-disable-osx-sandbox" not in " ".join(sum((c for c in agent.AGENT_COMMANDS.values()), []))  # never added for you
    assert agent.agent_for("command:python3 -c 1").argv == ["python3", "-c", "1"]
    try:
        agent.agent_for("gpt")
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown agent was accepted")
    assert "no such command" in agent.CommandAgent(["definitely-not-a-program-xyz"]).run("x").error


def fake_agent(tmp: Path, body: str) -> agent.CommandAgent:
    """A real subprocess standing in for a coding agent: it gets the prompt on stdin and writes files."""
    script = tmp / "fake_agent.py"
    script.write_text("import sys, shutil, pathlib\nprompt = sys.stdin.read()\n" + body)
    return agent.CommandAgent([sys.executable, str(script)], timeout_s=60, cwd=tmp)


def test_a_coding_agent_writes_the_file_and_the_pipeline_checks_it_itself():
    inv, root = world()
    tmp = Path(tempfile.mkdtemp())
    good = fake_agent(tmp, f"folder = pathlib.Path({str(root / 'rps')!r})\nfolder.mkdir(parents=True, exist_ok=True)\n"
                           f"shutil.copy({str(Path(__file__).resolve().parents[2] / 'xcolos/games/library/rps.json')!r}, folder / 'game.json')\n"
                           "(folder / 'encode_notes.md').write_text('chose ten rounds')\nprint('done')\n")
    m = Models()
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, encoder=agent.AgentEncoder(good))
    assert out.verdict == "ready_for_review", out
    assert "encode" not in calls(m)  # the model was not the coder
    assert "Rock Paper Scissors, weighted" in (root / "rps" / "AGENT_PROMPT.md").read_text()
    assert "chose ten rounds" in (root / "rps" / "encode_notes.md").read_text()


def test_an_agent_that_claims_success_but_wrote_a_bad_file_is_not_believed():
    inv, root = world()
    tmp = Path(tempfile.mkdtemp())
    liar = fake_agent(tmp, f"folder = pathlib.Path({str(root / 'rps')!r})\nfolder.mkdir(parents=True, exist_ok=True)\n"
                           "(folder / 'game.json').write_text('{}')\nprint('verify printed ok, all done')\n")
    built = agent.AgentEncoder(liar).build("rps", SPEC, PLAN, root / "rps")
    assert not built.ok and "refused by the loader" in built.attempts[0]


def test_an_agent_that_crashes_or_writes_nothing_is_reported_as_a_build_problem():
    inv, root = world()
    tmp = Path(tempfile.mkdtemp())
    assert "exited 3" in agent.AgentEncoder(fake_agent(tmp, "sys.exit(3)\n")).build("rps", SPEC, PLAN, root / "rps").attempts[0]
    assert "without writing game.json" in agent.AgentEncoder(fake_agent(tmp, "print('nothing')\n")).build("rps", SPEC, PLAN, root / "rps").attempts[0]


def test_a_failed_agent_build_goes_to_triage_with_the_agents_notes():
    inv, root = world()
    tmp = Path(tempfile.mkdtemp())
    stuck = fake_agent(tmp, f"folder = pathlib.Path({str(root / 'rps')!r})\nfolder.mkdir(parents=True, exist_ok=True)\n"
                            "(folder / 'encode_notes.md').write_text('the engine has no way for one player to accept another offer')\nsys.exit(0)\n")
    m = Models(triages=[triage_says("platform_limit", missing="one player accepting another's offer")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, encoder=agent.AgentEncoder(stuck))
    assert out.verdict == "platform_limit"
    seen = [p for p, c in zip(m.prompts, m.calls) if c == "triage"][0]
    assert "no way for one player to accept" in seen and "without writing game.json" in seen


def test_an_agent_that_takes_a_prompt_file_is_given_the_path_and_not_stdin():
    tmp = Path(tempfile.mkdtemp())
    script = tmp / "reads_file.py"
    script.write_text("import sys, pathlib\ntext = pathlib.Path(sys.argv[1]).read_text()\nprint('FILE:' + text[:20])\nassert sys.stdin.read() == ''\n")
    a = agent.CommandAgent([sys.executable, str(script), "{prompt_file}"], cwd=tmp)
    got = a.run("the whole prompt text")
    assert got.ok and "FILE:the whole prompt tex" in got.text
    kept = tmp / "kept" / "AGENT_PROMPT.md"
    kept.parent.mkdir()
    a.run("again", prompt_file=kept)
    assert kept.read_text() == "again"


# -- a repair shows the model what it got wrong ------------------------------------


class Records(Models):
    """Answers each step with junk once, then properly; keeps what it was sent."""

    def __init__(self, junk_for, **kw):
        super().__init__(**kw)
        self.junk_for, self.sent = junk_for, []

    def complete(self, prompt, system=""):
        self.sent.append(prompt)
        kind = ("adapt" if system.startswith("You are a game designer") else "critic" if system.startswith("You are a strict reviewer") else
                "triage" if system.startswith("A game design for XColos") else "spec" if system.startswith("You convert") else
                "encode" if system.startswith("You write game files") else "scenarios")
        if kind == self.junk_for and len([s for s in self.sent if s]) and not getattr(self, "_spent", False):
            self._spent = True
            return f"JUNK-REPLY-FOR-{kind}"
        return super().complete(prompt, system)


def test_every_repair_prompt_carries_the_refused_reply_so_the_model_fixes_it_instead_of_rewriting_blind():
    from gen_game import encode as enc
    from gen_game import scenarios as sc
    from gen_game import spec as specmod

    for kind, run in (
        ("adapt", lambda m: adaptmod.adapt(m, record().to_dict())),
        ("critic", lambda m: critic.review(m, record().to_dict(), PLAN)),
        ("triage", lambda m: triage.decide(m, "rules", "interface", "evidence")),
        ("spec", lambda m: specmod.write_spec(m, record().to_dict())),
        ("scenarios", lambda m: sc.write_scenarios(m, SPEC)),
    ):
        m = Records(kind)
        run(m)
        repair = m.sent[1]
        assert f"JUNK-REPLY-FOR-{kind}" in repair and "WAS REFUSED" in repair and "Why it was refused" in repair, kind
    # the encoder: the refused game FILE goes back with the loader's complaint
    m = Records("encode", games=[RPS_TEXT])
    got = enc.encode(m, SPEC, "rps", pause=lambda s: None)
    assert got.ok and "JUNK-REPLY-FOR-encode" in m.sent[1] and "PREVIOUS GAME FILE WAS REFUSED" in m.sent[1]


def test_a_repair_is_built_from_the_original_request_so_prompts_do_not_grow_with_each_attempt():
    from gen_game import repair
    base = "ORIGINAL REQUEST"
    second = repair.refused(base, "first bad reply", "problem one")
    third = repair.refused(base, "second bad reply", "problem two")
    assert "first bad reply" not in third and "problem one" not in third and third.startswith(base)
    assert len(third) < len(second) + 50
    long = repair.refused(base, "x" * 100000, "too long")
    assert len(long) < repair.MAX_PREVIOUS + 600 and "(cut)" in long


# -- multi-turn repair and the lint -----------------------------------------------


class Chatty(Models):
    """A model that can converse: records the messages of every turn."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.turns = []

    def converse(self, messages, system=""):
        self.turns.append([dict(m) for m in messages])
        self.calls.append("encode")
        return self.games.pop(0) if len(self.games) > 1 else self.games[0]


def test_a_model_that_can_converse_is_repaired_in_real_turns_with_its_own_refused_file_as_its_turn():
    from gen_game import encode as enc
    g = json.loads(RPS_TEXT)
    g["steps"][0]["use"] = "shout"
    m = Chatty(games=[json.dumps(g), RPS_TEXT])
    got = enc.encode(m, SPEC, "rps", pause=lambda s: None)
    assert got.ok and len(m.turns) == 2
    first, second = m.turns
    assert [t["role"] for t in first] == ["user"]
    assert [t["role"] for t in second] == ["user", "assistant", "user"]
    assert "shout" in second[1]["content"] and "shout" in second[2]["content"] and "refused" in second[2]["content"]
    assert second[0] == first[0]  # the original request is unchanged; nothing was rewritten or piled up


def test_a_model_that_cannot_converse_still_gets_the_refused_file_in_the_prompt():
    from gen_game import encode as enc
    m = Records("encode", games=[RPS_TEXT])
    assert not hasattr(m, "converse")
    assert enc.encode(m, SPEC, "rps", pause=lambda s: None).ok


def test_the_patient_wrapper_offers_converse_only_when_the_model_does_and_retries_it():
    from gen_game.cli import Patient

    class Plain:
        def complete(self, prompt, system=""):
            return "x"

    class Talks(Plain):
        n = 0

        def converse(self, messages, system=""):
            Talks.n += 1
            if Talks.n < 3:
                raise RuntimeError("Remote end closed connection")
            return f"{len(messages)} messages"
    assert not hasattr(Patient(Plain()), "converse")
    waits = []
    assert Patient(Talks(), pause=waits.append).converse([{"role": "user", "content": "hi"}]) == "1 messages" and waits == [10, 20]


def test_muse_chat_sends_the_whole_conversation_as_its_input():
    from gen_game.chat import MuseChat
    chat = MuseChat(model="m", reasoning_effort="low", api_key="LLM|1|abc")
    body = chat.body("", "sys")
    body["input"] = [{"role": "user", "content": "a"}]
    assert body["instructions"] == "sys" and isinstance(body["input"], list)
    assert hasattr(chat, "converse")


def test_the_lint_reports_every_known_mistake_in_one_message():
    from gen_game import encode as enc
    g = json.loads(RPS_TEXT)
    g["attributes"]["player"][0]["visible"] = "none"
    g["steps"][1]["use"] = "poll"
    g["steps"][1]["each"] = {"adjust": 1}
    g["deal"] = {"types": ["a"]}
    found = enc.lint(g)
    assert len(found) == 3
    assert any("visible: none" in f for f in found) and any("no `each` key" in f for f in found) and any("`into`" in f for f in found)
    problem = enc.check(g, "rps")[2]
    assert problem.startswith("known mistakes, all of them:") and problem.count("|") == 2
    assert enc.lint(json.loads(RPS_TEXT)) == []


# -- one generated prompt for both kinds of coder ------------------------------------


def test_a_model_and_an_agent_get_the_same_game_interface_and_rules_but_reach_the_api_differently():
    agent_text = prompt.build("rps", PLAN, SPEC, agent=True)
    model_text = prompt.build("rps", PLAN, SPEC, agent=False)
    for shared in ("Rock Paper Scissors, weighted", "higher total score", "`score`", "`seat 1`", "never `none`", "bound and then stored" if False else "binds it"):
        assert shared in agent_text and shared in model_text, shared
    assert "python3 -m gen_game verify rps game" in agent_text and "design/actions.md" in agent_text
    assert "python3 -m gen_game verify" not in model_text and "design/actions.md" not in model_text  # a reply cannot read files or run commands
    assert "system prompt" in model_text


def test_the_model_coder_is_called_with_the_generated_prompt_and_it_is_kept_on_disk():
    inv, root = world()
    m = Models()
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    sent = [p for p, c in zip(m.prompts, m.calls) if c == "encode"][0]
    assert sent == (root / "rps" / "CODER_PROMPT.md").read_text()  # exactly what the model received
    assert "Rock Paper Scissors, weighted" in sent and "The interface the file must use" in sent and sent.startswith("# Task: write the XColos game file")
    assert '"parameters"' not in sent  # not the bare spec JSON


def test_guidance_from_triage_is_part_of_the_generated_prompt_the_coder_receives():
    inv, root = world()
    m = Models(games=[wrong_game()] * 5 + [RPS_TEXT], triages=[triage_says("fix_game", "set rounds_left to 10")])
    run_flow("rps", m, inv, root, adapt=True, judge=True)
    last = [p for p, c in zip(m.prompts, m.calls) if c == "encode"][-1]
    assert "## Guidance from the last attempt" in last and "set rounds_left to 10" in last


# -- the call log and VERIFIED.md -------------------------------------------------------


def test_every_model_call_is_recorded_with_its_prompt_reply_and_hashes():
    from gen_game import calls
    folder = Path(tempfile.mkdtemp()) / "logs"
    rec = calls.Recorded(Models(), folder)
    inv, root = world()
    out = run_flow("rps", rec, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    log = [json.loads(l) for l in (folder / "calls.jsonl").read_text().splitlines()]
    assert [c["step"] for c in log] == ["design", "critic", "spec", "scenarios", "coder"]
    assert [c["n"] for c in log] == [1, 2, 3, 4, 5]
    coder = log[4]  # the coder comes after the tests, which are written first
    page = (folder / "05-coder.md").read_text()
    assert "Rock Paper Scissors, weighted" in page and coder["sent_sha256"][:16] in page and "## Reply" in page
    assert (folder / coder["system_file"]).read_text().startswith("You write game files")  # the system prompt, once
    assert coder["sent_sha256"] == calls.sha((root / "rps" / "CODER_PROMPT.md").read_text())  # the saved prompt IS the sent one


def test_a_failed_call_is_recorded_with_its_error_and_raised_again():
    from gen_game import calls

    class Down:
        model = "m"

        def complete(self, prompt, system=""):
            raise RuntimeError("Remote end closed connection")
    folder = Path(tempfile.mkdtemp())
    rec = calls.Recorded(Down(), folder)
    try:
        rec.complete("hi", system="You are a strict reviewer ...")
    except RuntimeError:
        pass
    else:
        raise AssertionError("the error was swallowed")
    entry = json.loads((folder / "calls.jsonl").read_text())
    assert entry["step"] == "critic" and "Remote end closed" in entry["error"] and entry["reply_chars"] == 0


def test_a_conversation_is_recorded_whole_and_converse_is_offered_only_when_the_model_has_it():
    from gen_game import calls
    assert not hasattr(calls.Recorded(Models(), Path(tempfile.mkdtemp())), "converse")
    chatty = Chatty(games=[RPS_TEXT])
    folder = Path(tempfile.mkdtemp())
    rec = calls.Recorded(chatty, folder)
    rec.converse([{"role": "user", "content": "write it"}, {"role": "assistant", "content": "{}"}, {"role": "user", "content": "fix it"}],
                 system="You write game files ...")
    page = (folder / "01-coder.md").read_text()
    assert "the whole conversation" in page and '"role": "assistant"' in page and "fix it" in page


def test_verified_md_shows_the_saved_prompt_is_the_sent_one_and_reruns_the_checks():
    from gen_game import calls, verified
    inv, root = world()
    rec = calls.Recorded(Models(), root / "rps" / "logs")
    run_flow("rps", rec, inv, root, adapt=True, judge=True)
    text = verified.write(root / "rps").read_text()
    assert "| 05 | coder |" in text and "MATCHES call 05: this is exactly what was sent" in text
    assert "all pass" in text and "independent scenarios: 2 of 2 pass" in text and "tier 0" in text and "reasoning and balance: not checked" in text


def test_verified_md_says_so_when_the_saved_prompt_is_not_the_one_that_was_sent():
    from gen_game import calls, verified
    inv, root = world()
    rec = calls.Recorded(Models(), root / "rps" / "logs")
    run_flow("rps", rec, inv, root, adapt=True, judge=True)
    (root / "rps" / "CODER_PROMPT.md").write_text("a prompt somebody edited afterwards")
    assert "no coder call in the log carries this hash" in verified.write(root / "rps").read_text()


def test_verified_md_catches_a_game_file_that_no_longer_passes():
    from gen_game import calls, verified
    inv, root = world()
    rec = calls.Recorded(Models(), root / "rps" / "logs")
    run_flow("rps", rec, inv, root, adapt=True, judge=True)
    (root / "rps" / "game.json").write_text("{}")
    assert "FAIL" in verified.write(root / "rps").read_text()


def test_muse_gets_the_reasoning_effort_and_the_command_line_can_be_shown_before_it_is_run():
    a = agent.agent_for("muse:some-model", "high")
    assert a.argv[:6] == ["muse", "exec", "--model", "some-model", "--reasoning-effort", "high"]
    assert "--reasoning-effort" not in agent.agent_for("claude", "high").argv
    shown = a.command_line(Path("/tmp/p.md"))
    assert shown[shown.index("--prompt-file") + 1] == "/tmp/p.md" and shown[shown.index("--workspace") + 1] == str(a.cwd)
    assert "{prompt_file}" not in " ".join(shown) and "{workspace}" not in " ".join(shown)


def test_the_cli_prints_the_exact_command_that_python_would_run_for_an_agent(capsys=None):
    import io
    import contextlib
    from gen_game.cli import main
    inv, root = world()
    folder = root / "rps"
    folder.mkdir(parents=True)
    (folder / "variation.json").write_text(json.dumps(PLAN))
    (folder / "spec.json").write_text(json.dumps(SPEC))
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(["--inventory", str(inv.root), "--root", str(root), "agent-command", "rps", "--encoder", "muse", "--effort", "low"])
    text = out.getvalue()
    assert code == 0 and "muse exec" in text and "--reasoning-effort low" in text and "--prompt-file" in text
    assert str(folder / "AGENT_PROMPT.md") in text and "python3 -m gen_game verify rps game" in text and "outside Claude Code" in text
    assert "Rock Paper Scissors, weighted" in (folder / "AGENT_PROMPT.md").read_text()


# -- is it running, finished, or stopped? ----------------------------------------------------


def test_a_live_run_is_running_a_finished_one_says_its_verdict_and_a_dead_one_without_a_verdict_is_stopped():
    from gen_game import status
    import os
    folder = Path(tempfile.mkdtemp()) / "g"
    assert status.state(folder)[0] == "NOT STARTED"
    status.started(folder / "logs")
    word, why = status.state(folder)
    assert word == "RUNNING" and str(os.getpid()) in why
    status.ended(folder / "logs", "ready_for_review", "6/6 scenarios")
    word, why = status.state(folder)
    assert word == "FINISHED" and "ready_for_review" in why
    status.ended(folder / "logs", "crashed", "RuntimeError: boom")
    assert status.state(folder)[0] == "STOPPED" and "boom" in status.state(folder)[1]
    # a process that vanished without writing a verdict: killed, or the machine slept
    import json
    (folder / "logs" / "run.json").write_text(json.dumps({"pid": 2 ** 22 + 12345, "started": status._now(), "state": "running"}))
    word, why = status.state(folder)
    assert word == "STOPPED" and "never wrote a verdict" in why


def test_the_recorder_shows_the_model_working_while_a_call_is_open_and_idle_after():
    from gen_game import calls, status
    from gen_game.chat import MuseChat
    import os
    folder = Path(tempfile.mkdtemp()) / "logs"
    seen = []

    class Opener:
        """A Muse that answers queued, in_progress twice, then completed; and notes what current.json said at each step."""
        n = 0

        def urlopen(self, request, timeout=0):
            Opener.n += 1
            if (folder / "current.json").exists():
                seen.append(json.loads((folder / "current.json").read_text()))
            statuses = ["queued", "in_progress", "in_progress", "completed"]
            body = {"id": "resp_abc", "status": statuses[min(Opener.n - 1, 3)],
                    "output": [{"type": "message", "content": [{"type": "output_text", "text": "the reply"}]}]}
            return type("R", (), {"read": lambda self: json.dumps(body).encode(), "__enter__": lambda self: self, "__exit__": lambda self, *a: None})()

    import gen_game.chat as chatmod
    real = chatmod._sleep
    chatmod._sleep = lambda s: None
    try:
        chat = MuseChat(model="m", api_key="LLM|1|abc", opener=Opener())
        rec = calls.Recorded(chat, folder)
        assert rec.complete("hello", system="You are a game designer ...") == "the reply"
    finally:
        chatmod._sleep = real
    working = [c for c in seen if c.get("response_id")]
    assert working and working[-1]["muse_status"] in ("in_progress", "queued") and working[-1]["step"] == "design"
    assert working[-1]["state"] == "waiting for the model" and working[-1]["polls"] >= 1
    final = json.loads((folder / "current.json").read_text())
    assert final["state"] == "idle: last call finished" and final["call"] == 1
    folder.parent.joinpath("logs", "run.json").write_text(json.dumps({"pid": os.getpid(), "started": status._now(), "state": "running"}))
    text = status.describe(folder.parent)
    assert "RUNNING" in text and "1 model call(s) finished" in text and "idle: last call finished" in text


def test_a_call_that_has_made_no_progress_for_minutes_is_flagged_as_possibly_stuck():
    from gen_game import status
    import os
    folder = Path(tempfile.mkdtemp()) / "g"
    status.started(folder / "logs")
    old = "2020-01-01T00:00:00+00:00"
    (folder / "logs" / "current.json").write_text(json.dumps({"state": "waiting for the model", "call": 3, "step": "coder", "updated": old}))
    assert "WARNING: a call has made no progress for over 4 minutes" in status.describe(folder)


def test_the_cli_status_command_describes_a_game(capsys=None):
    import io, contextlib
    from gen_game.cli import main
    from gen_game import status
    inv, root = world()
    status.started(root / "rps" / "logs")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert main(["--inventory", str(inv.root), "--root", str(root), "status", "rps"]) == 0
    assert "rps: RUNNING" in out.getvalue()


def test_the_designer_is_warned_of_the_higher_total_trap_and_the_critic_judges_the_winner_rule_not_the_payoffs():
    designer = adaptmod.system_prompt()
    for must in ("HIGHER TOTAL WINS", "only the\nDIFFERENCE between the totals matters", "against EVERY opponent action", "a target a player must reach"):
        assert must in designer, must
    reviewer = critic.system_prompt()
    assert "Apply the WINNER RULE, not the payoffs" in reviewer and "A policy that never loses fails the check" in reviewer


def test_the_coder_is_told_to_keep_a_round_within_the_step_limit_in_both_prompts():
    for agent_flag in (True, False):
        text = prompt.build("rps", PLAN, SPEC, agent=agent_flag)
        assert f"at most {complexity.LIMITS['steps_per_round']} steps" in text and "one `update`" in text


def test_the_designer_and_critic_are_told_that_a_lottery_under_good_play_is_a_failure():
    assert "THE LOTTERY TRAP" in adaptmod.system_prompt() and "intended good strategy" in adaptmod.system_prompt()
    assert "not a trap" in adaptmod.system_prompt()  # a deal that good play can overcome is welcome


def test_the_designer_is_told_to_keep_the_idea_and_that_rounds_need_not_be_fixed():
    for need in ("KEEP THE IDEA", "RANDOM STARTS ARE GOOD", "ROUNDS NEED NOT BE FIXED"):
        assert need in adaptmod.IDEA_MODE
    assert "decided by the random draw alone" in critic.system_prompt() and "intended good strategy" in critic.system_prompt()


def test_what_a_person_already_knows_is_wrong_goes_to_the_first_designer_call():
    inv, root = world()
    m = Models()
    out = run_flow("rps", m, inv, root, adapt=True, judge=True, design_feedback="always Defect wins 71% against random seats; types are a lottery")
    assert out.verdict == "ready_for_review", out
    first = designer_prompts(m)[0]
    assert "PREVIOUS VARIATION" in first and "always Defect wins 71%" in first


def test_the_cli_reads_design_feedback_from_a_file():
    import io, contextlib
    from gen_game.cli import main
    inv, root = world(status="blocked", blocked_by=["real_time"])
    note = root / "feedback.txt"
    note.write_text("the last design was a lottery")
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = main(["--inventory", str(inv.root), "--root", str(root), "convert", "rps", "--model", "echo:x", "--design-feedback", f"@{note}"])
    assert code == 2  # not converted (the game is blocked), but the option was accepted


# -- the rules, played with numbers ------------------------------------------------------------------

from gen_game import modelcheck  # noqa: E402

TRI = {"players": 3, "rounds": 8, "actions": ["C", "D"], "types": {"values": ["High", "Low"], "probs": [0.5, 0.5]},
       "payoff": "((6 if type == 'High' else 5) if n_C == 3 else (4 if type == 'High' else 3) if n_C == 2 else 0) if action == 'C' else (3 if n_C >= 1 else 2)",
       "winner": {"kind": "highest_total"}}
# always D never loses: it pays 3 whatever the other does, and the other can at best match it
SAFE_NEVER_LOSES = {"players": 2, "rounds": 10, "actions": ["C", "D"], "types": None,
                    "payoff": "(4 if o_C == 1 else 0) if action == 'C' else 3", "winner": {"kind": "highest_total"}}
# rock paper scissors by counts: nothing is safe, nothing is a lottery
FAIR = {"players": 2, "rounds": 10, "actions": ["R", "P", "S"], "types": None,
        "payoff": "1 if (action == 'R' and o_S == 1) or (action == 'P' and o_R == 1) or (action == 'S' and o_P == 1) else 0",
        "winner": {"kind": "highest_total"}}


def test_the_rules_simulator_finds_what_was_found_by_hand_in_the_three_player_design():
    r = modelcheck.simulate(TRI)
    text = " | ".join(r.flags)
    assert "'always D' wins" in text and "too good" in text
    assert "knowing your type does not pay" in text
    assert "decided by the random draw" in text and r.good_play["policy"] == "always C"
    best = max(r.rows, key=lambda x: x["random"]["win"])
    assert best["policy"] == "always D" and 0.6 < best["random"]["win"] < 0.8 and best["random"]["loss"] < 0.2  # the hand-run figures: 71% / 13%


def test_a_policy_that_never_loses_is_named_with_the_reason():
    r = modelcheck.simulate(SAFE_NEVER_LOSES)
    assert any("'always D' never loses" in f for f in r.flags)


def test_a_fair_game_has_no_flags_and_a_target_objective_changes_the_verdict():
    assert modelcheck.simulate(FAIR).flags == []
    stag = {"players": 2, "rounds": 10, "actions": ["C", "D"], "types": None,
            "payoff": "(4 if o_C == 1 else 0) if action == 'C' else 3", "winner": {"kind": "target", "target": 36}}
    r = modelcheck.simulate(stag)
    assert not any("never loses" in f for f in r.flags)  # only sustained cooperation (4 x 10) reaches 36, so Defect (30) cannot win


def test_a_model_is_checked_before_it_is_played_and_nothing_but_arithmetic_is_allowed_in_the_payoff():
    assert modelcheck.problems(None) == [] and modelcheck.problems(FAIR) == []
    assert any("players" in p for p in modelcheck.problems({**FAIR, "players": 1}))
    assert any("actions" in p for p in modelcheck.problems({**FAIR, "actions": ["C"]}))
    assert any("types" in p for p in modelcheck.problems({**FAIR, "types": {"values": ["a", "b"], "probs": [0.9, 0.9]}}))
    assert any("winner" in p for p in modelcheck.problems({**FAIR, "winner": {"kind": "vibes"}}))
    for evil in ("__import__('os').system('echo hi')", "open('/etc/passwd').read()", "(lambda: 1)()", "action.upper()", "[x for x in range(3)]"):
        assert modelcheck.problems({**FAIR, "payoff": evil}), evil
    assert any("not a number" in p for p in modelcheck.problems({**FAIR, "payoff": "'win' if action == 'R' else 0"}))
    assert any("failed" in p for p in modelcheck.problems({**FAIR, "payoff": "1 / (n_R - 1)"}))
    assert any("not a valid expression" in p for p in modelcheck.problems({**FAIR, "payoff": "1 +"}))


def test_the_designer_is_told_how_to_give_a_model_and_a_bad_model_is_sent_back_for_repair():
    system = adaptmod.system_prompt()
    assert "MODEL." in system and "n_<A>" in system and "{\"kind\": \"target\"" in system
    bad = {**PLAN, "model": {**FAIR, "payoff": "1 +"}}
    found = adaptmod.problems(bad)
    assert any(f.startswith("model:") and "not a valid expression" in f for f in found)
    assert any("model.players is 5" in f for f in adaptmod.problems({**PLAN, "model": {**FAIR, "players": 5}}))
    assert adaptmod.problems({**PLAN, "model": FAIR}) == []


def test_rules_that_fail_the_numbers_go_straight_back_to_the_designer_with_the_numbers_and_the_critic_is_not_asked():
    flawed = {**PLAN, "model": SAFE_NEVER_LOSES}
    fixed = {**PLAN, "variation": {**PLAN["variation"], "name": "Fixed"}, "model": FAIR}
    inv, root = world()
    m = Models(plans=[flawed, fixed])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m)[:4] == ["adapt", "adapt", "critic", "spec"]  # no critic call for the flawed design
    second = designer_prompts(m)[1]
    assert "Playing the rules with numbers" in second and "'always D' never loses" in second and "Do not tweak it" in second
    assert "win " in second and "against random opponents" in second  # the numbers themselves
    saved = json.loads((root / "rps" / "variation.json").read_text())
    assert saved["simulation"]["flags"] == [] and saved["critic"]["sound"] is True
    assert "The rules played with numbers" in (root / "rps" / "VARIATION.md").read_text()


def test_rules_that_never_pass_the_numbers_are_dropped_as_too_simple_with_the_last_flaw_as_the_reason():
    inv, root = world()
    m = Models(plans=[{**PLAN, "model": SAFE_NEVER_LOSES}])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "dropped" and out.detail.startswith("too simple: no design survived playing it with numbers")
    assert "never loses" in out.detail and "critic" not in calls(m) and calls(m).count("adapt") == flow.CRITIC_ROUNDS


def test_a_game_that_does_not_fit_the_model_is_not_simulated_and_the_page_says_so():
    inv, root = world()
    m = Models(plans=[{**PLAN, "model": None}])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review"
    assert "not simulated: the game does not fit" in (root / "rps" / "VARIATION.md").read_text()


# -- a spec entry with no `why` crashed the run: the check and the page must both cope -------------------------


def test_a_choice_or_simplification_without_a_why_is_sent_back_for_repair_not_left_to_crash_the_page():
    from gen_game import spec as specmod
    bad = {**SPEC, "simplifications": [{"what": "payoff matrix done in three update steps"}], "choices": [{"what": "x", "why": ""}]}
    found = specmod.problems(bad)
    assert any("simplifications[1]" in f and "why" in f for f in found) and any("choices[1]" in f for f in found)
    assert specmod.problems({**SPEC, "simplifications": ["a plain sentence is fine"], "choices": [{"what": "a", "why": "b"}]}) == []
    page = specmod.render({**SPEC, "simplifications": [{"what": "no reason given"}]})  # an old spec on disk must still render
    assert "no reason given" in page


def test_the_report_page_copes_with_an_entry_that_has_no_why():
    r = {"game": "g", "verdict": "needs_review", "scenarios": [], "conformance": [], "attempts": [],
         "tier0": {"passed": True, "problems": [], "metrics": {"matches": 1, "tables": [2], "results": {}, "turns_min": 1, "turns_max": 1}},
         "tier1": {"flags": [], "random_results": {}, "dominance": {}}, "spec_choices": [{"what": "only what"}], "simplifications": []}
    assert "only what" in flow.render_report(r)


def test_the_spec_writer_repairs_a_reply_with_a_missing_why():
    class Once(Models):
        n = 0

        def complete(self, prompt, system=""):
            Once.n += 1
            self.prompts.append(prompt)
            return json.dumps({**SPEC, "simplifications": [{"what": "no why"}]} if Once.n == 1 else SPEC)
    from gen_game import spec as specmod
    m = Once()
    spec, err = specmod.write_spec(m, record().to_dict())
    assert err == "" and spec is not None and "simplifications[1]" in m.prompts[1]


# -- a missing bracket: mended, explained, and never blamed on the rules ------------------------------------------------------


MISSING_BRACE = '{"a": {"set": {"player": 1, "key": "k", "value": ""}, {"set": {"player": 2, "key": "k", "value": ""}}}}'


def test_a_closing_brace_missing_before_a_comma_is_mended_and_nothing_else_is_guessed():
    from gen_game import encode as enc
    mended, n = enc.mend_json('{"a": [{"b": {"c": 1}, {"d": 2}]}')
    assert n == 1 and json.loads(mended) == {"a": [{"b": {"c": 1}}, {"d": 2}]}
    mended, n = enc.mend_json('{"a": {"b": 1}')  # a missing closer at the very end
    assert json.loads(mended) == {"a": {"b": 1}} and n == 1
    good = '{"a": 1}'
    assert enc.mend_json(good) == (good, 0)
    assert enc.mend_json("no json here") == ("no json here", 0)
    garbage = '{"a": tru, "b": }'
    assert enc.mend_json(garbage)[1] == 0 or "tru" in enc.mend_json(garbage)[0]  # meaning is never invented


def test_a_mended_file_still_goes_through_every_other_check():
    from gen_game import encode as enc
    broken = RPS_TEXT.replace('"visible": "public"', '"visible": "public"', 1)
    # remove one closing brace from the pretty file: the mender restores it and the game then loads as before
    i = broken.index('},\n    "game"') if '},\n    "game"' in broken else None
    text = json.dumps(json.loads(RPS_TEXT), separators=(",", ":"))
    j = text.index('"game":[') if '"game":[' in text else text.index('"game"')
    no_closer = text[: text.rindex("}")]  # the very last brace missing
    assert enc.check(no_closer, "rps")[1] is not None and enc.check(no_closer, "rps")[2] == ""
    wrong = json.loads(RPS_TEXT)
    wrong["steps"][0]["use"] = "shout"
    assert "refused by the loader" in enc.check(json.dumps(wrong, separators=(",", ":"))[:-1], "rps")[2]


def test_a_reply_that_cannot_be_mended_shows_the_model_where_it_stopped_parsing():
    from gen_game import encode as enc
    problem = enc.check('{"a": 1, "b": tru, "c": 3}', "x")[2]
    assert "did not parse" in problem and "<<HERE>>" in problem and "count the brackets" in problem


def test_a_failure_that_is_only_json_syntax_goes_back_to_the_coder_without_asking_triage():
    assert flow.syntax_only(["the game file was refused by the loader: the JSON did not parse. x"] * 5)
    assert not flow.syntax_only(["the game file was refused by the loader: the JSON did not parse.", "playing it with random seats failed: crashed"])
    assert not flow.syntax_only([])
    inv, root = world()
    syntax = "{ this is not json"
    m = Models(games=[syntax] * 5 + [RPS_TEXT])  # five unparseable files, then a good one
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert "triage" not in calls(m) and calls(m).count("adapt") == 1  # the rules were never reconsidered
    report = json.loads((root / "rps" / "report.json").read_text())
    assert report["triage"][0]["decision"] == "fix_game" and "JSON syntax" in report["triage"][0]["reason"]


def test_the_triage_prompt_and_the_coder_prompts_know_about_syntax_slips_and_static_attributes():
    from gen_game import encode as enc
    assert "always `fix_game`" in triage.system_prompt() and "typing\nslip" in triage.system_prompt()
    for text in (prompt.build("rps", PLAN, SPEC, agent=True), prompt.build("rps", PLAN, SPEC, agent=False)):
        assert "WRITE IT INDENTED" in text and "declared static" in text and '"mutable": false' in text


# -- three fixes from the battle_of_wits run -----------------------------------------------------------------------------------


def test_a_platform_limit_may_name_the_missing_capability_in_one_word():
    one_word = {"decision": "platform_limit", "reason": "the rules need the platform to do this thing it cannot do", "guidance": "", "missing": "conditional_subsequence"}
    assert triage.problems(one_word) == []
    assert triage.problems({**one_word, "missing": ""}) and triage.problems({**one_word, "missing": "ab"})
    got, err = triage.decide(Models(triages=[one_word]), "rules", "interface", "evidence")
    assert err == "" and got["missing"] == "conditional_subsequence"


def test_the_manifest_says_a_conditional_award_is_not_the_conditional_subsequence_limit():
    from gen_inventory import gates
    note = gates.load_manifest()["needs"]["conditional_subsequence"]["note"]
    assert "NOT a limit on conditional scoring" in note and "`when`" in note and "`if`" in note
    for text in (adaptmod.restrictions_text(), triage.system_prompt(), critic.system_prompt()):
        assert "NOT a limit on conditional scoring" in text


def test_a_dead_attribute_message_names_the_steps_that_mention_it_or_says_none_does():
    from gen_game import encode as enc
    g = json.loads(RPS_TEXT)
    g["attributes"]["game"] += [{"key": "orphan", "visible": "public", "type": "number", "initial": 0},
                                {"key": "stuck", "visible": "public", "type": "number", "initial": 0}]
    g["steps"].append({"use": "update", "label": "tally", "do": [{"set": {"key": "stuck", "value": {"calc": "0"}}}]})
    problem = enc.check(g, "rps")[2]
    assert "`orphan`" in problem and "No step sets it. Either remove the attribute" in problem
    assert "`stuck`" in problem and "Steps that name it: tally" in problem and "may never be true" in problem
    assert enc.steps_mentioning(g, "stuck") == ["tally"] and enc.steps_mentioning(g, "orphan") == []


# -- the tested recipe the coder is shown ------------------------------------------------------------------------------------


def test_the_recipe_game_passes_every_check_the_pipeline_applies_and_scores_as_described():
    from gen_game import encode as enc, harness
    from gen_game.prompt import RECIPE_FILE
    game = json.loads(RECIPE_FILE.read_text())
    obj, defn, problem = enc.check(game, "match_or_miss")
    assert problem == "" and defn is not None  # loads, arithmetic outcome, random play, every attribute updated
    p = harness.play(defn, [harness.QueueAgent("A", ["A", "A", "B"]), harness.QueueAgent("B", ["A", "B", "B"])], 1)
    assert p.result.winner == "seat 1" and [p.attribute(s, "score") for s in (1, 2)] == [2, 1]  # matches in rounds 1 and 3


def test_both_coder_prompts_show_the_recipe_and_say_how_an_answer_reaches_the_state():
    for flag in (True, False):
        text = prompt.build("rps", PLAN, SPEC, agent=flag)
        assert "A pattern that works" in text and '"bind": "a1"' in text and '"value": "$a1"' in text and "Adapt this" in text
        assert '"id": "match_or_miss"' in text  # the whole game is in the prompt, not a description of it


# -- the coder's feedback, and tests that can be wrong ------------------------------------------------------------------------


OBSERVING_SPEC = {**SPEC, "attributes": {
    "player": [{"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "points", "observable": True},
               {"key": "scratch_code", "type": "number", "visible": "none", "initial": 0, "meaning": "bookkeeping", "observable": False}],
    "game": [{"key": "rounds_left", "type": "number", "visible": "public", "initial": 10, "meaning": "rounds to go", "observable": True},
             {"key": "last_match", "type": "number", "visible": "none", "initial": 0, "meaning": "a flag", "observable": False}]}}


def test_only_observable_attributes_are_part_of_the_interface_and_the_rest_is_the_coders_to_design():
    from gen_game import spec as specmod
    assert specmod.observable(OBSERVING_SPEC) == {"player": ["score"], "game": ["rounds_left"]}
    assert specmod.observable(SPEC) == {"player": ["score"], "game": ["rounds_left"]}  # a spec that does not say: all of them
    text = prompt.interface(OBSERVING_SPEC)
    assert "`score`" in text and "`rounds_left`" in text and "scratch_code" not in text and "last_match" not in text
    assert "yours to design" in text
    assert any("observable must be true or false" in p for p in specmod.problems({**OBSERVING_SPEC, "attributes": {
        "player": [{"key": "s", "visible": "public", "observable": "yes"}], "game": []}}))


def test_a_test_that_asserts_on_internal_bookkeeping_is_sent_back_to_its_writer():
    from gen_game import scenarios as sc
    obs = {"player": ["score"], "game": ["rounds_left"]}
    bad = {**ALWAYS_ROCK, "expect": {"result": "draw", "players": {"1": {"scratch_code": 3}}, "game": {"last_match": 0}}}
    found = sc.problems([bad], obs)
    assert any("scratch_code" in f and "not observable" in f for f in found) and any("last_match" in f for f in found)
    assert sc.problems([ALWAYS_ROCK], obs) == []
    m = Models(spec=OBSERVING_SPEC, scenario_lists=[[bad], [ALWAYS_ROCK]])
    items, err = sc.write_scenarios(m, OBSERVING_SPEC)
    assert err == "" and items[0]["name"] == ALWAYS_ROCK["name"]
    first = [p for p, c in zip(m.prompts, m.calls) if c == "scenarios"][0]
    assert "OBSERVABLE (the only attributes you may assert on): player: score; table: rounds_left" in first
    assert "ASSERT ONLY ON WHAT AN OUTSIDE OBSERVER SEES" in sc.SYSTEM


def test_a_failing_test_shows_the_coder_what_its_game_actually_did():
    from gen_game import encode as enc
    wrong = {**SEAT1_WINS, "name": "seat 1 should lose", "expect": {"result": "seat 2", "players": {"1": {"score": 0}}}}
    _, defn, problem = enc.check(json.loads(RPS_TEXT), "rps", tests=[wrong])
    assert defn is None and "What YOUR game did on the first of them (seat 1 should lose)" in problem
    assert "moves played:" in problem and "seat 1: 'scissors'" in problem
    assert "First attribute changes:" in problem and "score:" in problem and "Final: players" in problem


def test_triage_can_say_the_tests_are_wrong_and_the_tests_are_rewritten_and_the_coder_starts_fresh():
    assert "fix_tests" in triage.system_prompt() and "internal bookkeeping" in triage.system_prompt()
    assert triage.problems(triage_says("fix_tests", "assert only on scores")) == []
    assert any("guidance" in p for p in triage.problems({**triage_says("fix_tests"), "guidance": ""}))
    wrong = {**ALWAYS_ROCK, "name": "a test that misreads the rules", "expect": {"result": "seat 1"}}
    inv, root = world()
    m = Models(scenario_lists=[[wrong], [ALWAYS_ROCK, SEAT1_WINS]], triages=[triage_says("fix_tests", "assert only on the result and the scores")])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "ready_for_review", out
    assert calls(m).count("scenarios") == 2 and calls(m).count("adapt") == 1 and calls(m).count("encode") == 1  # the tests were rewritten; the file and the rules stand
    second = [p for p, c in zip(m.prompts, m.calls) if c == "scenarios"][1]
    assert "EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG" in second and "assert only on the result and the scores" in second
    triage_prompt = [p for p, c in zip(m.prompts, m.calls) if c == "triage"][0]
    assert "THE TESTS (written from the rules alone; judge whether they are right)" in triage_prompt and "a test that misreads the rules" in triage_prompt
    report = json.loads((root / "rps" / "report.json").read_text())
    assert report["triage"][0]["decision"] == "fix_tests"


# -- putting a working game into the platform's library, to play it by hand --------------------------------------------------


def test_install_puts_a_game_that_works_into_the_library_and_uninstall_takes_it_out():
    import io, contextlib
    from gen_game.cli import main
    inv, root = world()
    (root / "rps").mkdir(parents=True)
    (root / "rps" / "game.json").write_text(RPS_TEXT)
    library = Path(tempfile.mkdtemp())
    base = ["--inventory", str(inv.root), "--root", str(root)]
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        assert main([*base, "install", "rps", "--library", str(library)]) == 0
    assert (library / "rps.json").exists() and "restart the server" in out.getvalue() and "Rock, Paper, Scissors" in out.getvalue()
    assert main([*base, "install", "rps", "--library", str(library)]) == 0  # the same game again is fine
    assert main([*base, "uninstall", "rps", "--library", str(library)]) == 0 and not (library / "rps.json").exists()
    assert main([*base, "uninstall", "rps", "--library", str(library)]) == 1


def test_install_refuses_a_game_that_fails_the_checks_and_never_overwrites_a_different_game():
    from gen_game.cli import main
    inv, root = world()
    (root / "rps").mkdir(parents=True)
    library = Path(tempfile.mkdtemp())
    base = ["--inventory", str(inv.root), "--root", str(root)]
    (root / "rps" / "game.json").write_text("{}")
    assert main([*base, "install", "rps", "--library", str(library)]) == 1 and not (library / "rps.json").exists()
    (root / "rps" / "game.json").write_text(RPS_TEXT)
    other = json.loads(RPS_TEXT)
    other["meta"]["blurb"] = "a different game that happens to share the id"
    (library / "rps.json").write_text(json.dumps(other))
    assert main([*base, "install", "rps", "--library", str(library)]) == 1
    assert json.loads((library / "rps.json").read_text())["meta"]["blurb"].startswith("a different game")


def test_the_verify_command_treats_the_specs_parameters_as_constants_exactly_as_the_flow_does():
    from gen_game.cli import main
    inv, root = world()
    folder = root / "rps"
    folder.mkdir(parents=True)
    g = json.loads(RPS_TEXT)
    g["attributes"]["game"].append({"key": "num_rounds", "visible": "public", "type": "number", "initial": 10})  # a parameter nothing changes
    (folder / "game.json").write_text(json.dumps(g))
    base = ["--inventory", str(inv.root), "--root", str(root)]
    assert main([*base, "verify", "rps", "game"]) == 1  # no spec: an attribute nothing updates is reported
    (folder / "spec.json").write_text(json.dumps({**SPEC, "parameters": {**SPEC["parameters"], "num_rounds": 10}}))
    assert main([*base, "verify", "rps", "game"]) == 0  # the spec says it is a parameter: it is meant to stay put


def test_scenarios_that_cannot_be_written_before_the_build_do_not_stop_the_build():
    class Flaky(Models):
        failures = 2  # the first two scenario calls fail (one retry is made), then it works

        def complete(self, prompt, system=""):
            if "write test scenarios" in system and self.failures > 0:
                self.failures -= 1
                raise RuntimeError("The model failed to generate a response.")
            return super().complete(prompt, system)

    inv, root = world()
    out = run_flow("rps", Flaky(), inv, root, adapt=True, judge=True)
    assert out.verdict != "scenarios_failed", out
