"""gen_game: harness, spec, encode, scenarios, evaluation, the CLI and the small pieces.

The flow itself is in test_flow.py. Nothing here touches a model or the network.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import *  # noqa: E402,F401,F403 - the shared scripted models and fixtures
from fixtures import (ALWAYS_ROCK, LIBRARY, PLAN, RPS, RPS_TEXT, SEAT1_WINS, SPEC, Models, record, run_flow, world)  # noqa: E402

from gen_game import adapt as adaptmod  # noqa: E402
from gen_game import complexity  # noqa: E402
from gen_game import encode as enc  # noqa: E402
from gen_game import evaluate, flow, harness, scenarios, spec as specmod  # noqa: E402
from gen_game.cli import main  # noqa: E402

def test_a_shipped_game_passes_smoke_and_replays_identically():
    assert harness.smoke(RPS) == []
    a, b = harness.play(RPS, harness.random_agents(2, 7), 7), harness.play(RPS, harness.random_agents(2, 7), 7)
    assert a.comparable_log() == b.comparable_log() and a.log_problems() == []


def test_scripted_seats_play_the_moves_they_were_given():
    p = harness.play(RPS, [harness.QueueAgent("A", ["rock"] * 4 + ["paper"] * 4 + ["scissors"] * 2),
                           harness.QueueAgent("B", ["scissors"] * 4 + ["rock"] * 4 + ["paper"] * 2)], 1)
    assert p.result.winner == "seat 1"
    assert p.attribute(1, "score") > 0 and p.attribute(2, "score") == 0


# -- step 2 ----------------------------------------------------------------


def test_a_valid_spec_is_accepted_and_a_bad_one_is_repaired():
    spec, err = specmod.write_spec(Models(), record().to_dict())
    assert err == "" and spec["name"] == "Rock, Paper, Scissors"

    class Once(Models):
        def complete(self, prompt, system=""):
            self.calls.append("x")
            return "no json" if len(self.calls) == 1 else json.dumps(SPEC)
    m = Once()
    assert specmod.write_spec(m, record().to_dict())[1] == "" and len(m.calls) == 2


def test_spec_problems_name_what_is_missing_or_wrong():
    assert any("choices" in p for p in specmod.problems({k: v for k, v in SPEC.items() if k != "choices"}))
    bad = json.loads(json.dumps(SPEC))
    bad["round"][0]["action"] = "shout"
    bad["attributes"]["player"][0]["visible"] = "secret"
    bad["parameters"]["rounds"] = "ten"
    found = " | ".join(specmod.problems(bad))
    assert "shout" in found or "action" in found
    assert "visible" in found and "parameters" in found


def test_a_spec_gives_up_after_its_repairs_and_says_why():
    class Junk(Models):
        def complete(self, prompt, system=""):
            return "{}"
    spec, err = specmod.write_spec(Junk(), record().to_dict())
    assert spec is None and "missing key" in err


def test_a_spec_renders_for_review_with_its_choices_and_gaps():
    page = specmod.render({**SPEC, "unsupported": ["a board"]})
    assert "twelve cards each" in page and "a board" in page and "`rounds` = 10" in page


# -- step 3 ----------------------------------------------------------------


def test_the_encoder_is_shown_the_format_and_told_to_use_arithmetic():
    system = enc.system_prompt()
    assert "calc" in system and "# THE FORMAT" in system and "Example game: rps" in system
    assert "Do NOT copy" in system


def test_a_loader_error_goes_back_to_the_model_and_the_next_reply_is_used():
    g = json.loads(RPS_TEXT)
    g["steps"][0]["use"] = "shout"  # not an action
    broken = json.dumps(g)
    m = Models(games=[broken, RPS_TEXT])
    got = enc.encode(m, SPEC, "rps")
    assert got.ok and len(got.attempts) == 2 and "loader" in got.attempts[0] and got.attempts[1] == ""
    assert "shout" in m.prompts[-1]  # the loader's own words went back to the model


def test_a_game_decided_by_a_model_is_refused_with_the_reason():
    problem = enc.check(json.loads((LIBRARY / "auction.json").read_text()), "x")[2]
    assert "decided by arithmetic" in problem and "winner" in problem


def test_a_reply_that_never_loads_ends_with_every_attempt_recorded():
    got = enc.encode(Models(games=["not json"]), SPEC, "rps", repairs=2)
    assert not got.ok and len(got.attempts) == 3


def test_the_inventory_id_wins_over_the_models():
    obj, defn, problem = enc.check(RPS_TEXT, "chosen_id")
    assert problem == "" and defn.id == "chosen_id" and obj["meta"]["id"] == "chosen_id"


def test_a_backend_that_is_down_ends_the_encoding_without_a_crash():
    class Down:
        calls = 0

        def complete(self, prompt, system=""):
            Down.calls += 1
            raise RuntimeError("503")
    got = enc.encode(Down(), SPEC, "rps", pause=lambda s: None)
    assert not got.ok and "model call failed" in got.attempts[0]
    assert Down.calls == 4 and len(got.attempts) == 4  # the call and three retries, then it gives up


def test_a_dropped_connection_is_retried_and_does_not_use_up_a_repair():
    class Flaky(Models):
        def complete(self, prompt, system=""):
            if len([c for c in self.calls if c == "try"]) < 2:
                self.calls.append("try")
                raise RuntimeError("Remote end closed connection without response")
            return super().complete(prompt, system)
    waits = []
    got = enc.encode(Flaky(), SPEC, "rps", pause=waits.append)
    assert got.ok and waits == [5, 10]
    assert [a for a in got.attempts if a == ""] == [""] and len(got.attempts) == 3


# -- scenarios -------------------------------------------------------------


def test_scenarios_parse_from_a_fenced_reply_and_bad_ones_are_named():
    class Fenced(Models):
        def complete(self, prompt, system=""):
            return "Here:\n```json\n" + json.dumps([ALWAYS_ROCK]) + "\n```"
    items, err = scenarios.write_scenarios(Fenced(), SPEC)
    assert err == "" and items[0]["name"] == ALWAYS_ROCK["name"]
    assert any("one entry per seat" in p for p in scenarios.problems([{**ALWAYS_ROCK, "moves": {"1": []}}]))
    assert any("'result'" in p for p in scenarios.problems([{**ALWAYS_ROCK, "expect": {}}]))


def test_a_correct_game_passes_and_a_wrong_expectation_names_the_difference():
    assert scenarios.run_scenario(RPS, ALWAYS_ROCK).passed
    bad = {**SEAT1_WINS, "expect": {"result": "seat 2", "players": {"1": {"score": 5}}}}
    out = scenarios.run_scenario(RPS, bad)
    assert not out.passed
    assert any("result: expected 'seat 2'" in f for f in out.failures) and any("seat 1 score" in f for f in out.failures)


def test_scripting_too_many_or_too_few_moves_is_reported_as_that():
    few = {**ALWAYS_ROCK, "moves": {"1": ["rock"], "2": ["rock"]}}
    assert any("more question" in f for f in scenarios.run_scenario(RPS, few).failures)
    many = {**ALWAYS_ROCK, "moves": {"1": ALWAYS_ROCK["moves"]["1"] + ["rock"] * 3, "2": ALWAYS_ROCK["moves"]["2"]}}
    assert any("asked only" in f for f in scenarios.run_scenario(RPS, many).failures)


def test_a_scenario_for_the_wrong_table_size_is_reported():
    assert "takes 2 to 2 players" in scenarios.run_scenario(RPS, {**ALWAYS_ROCK, "players": 3}).failures[0]


# -- step 4 ----------------------------------------------------------------


def test_tier_zero_passes_a_sound_game_and_counts_its_matches():
    t0 = evaluate.tier0(RPS, seeds=range(1, 6))
    assert t0["passed"] and t0["metrics"]["matches"] == 5 and sum(t0["metrics"]["results"].values()) == 5


def test_tier_one_flags_a_policy_that_always_wins(monkeypatch=None):
    real = harness.play

    def rigged(defn, agents, seed):
        for i, a in enumerate(agents):
            if isinstance(a, harness.FixedAgent) and a.policy == "last":
                return SimpleNamespace(result=SimpleNamespace(winner=f"seat {i + 1}"))
        return real(defn, agents, seed)
    harness.play = rigged
    try:
        flags = evaluate.tier1(RPS, seeds=range(1, 13))["flags"]
    finally:
        harness.play = real
    assert any("always taking the last option as seat 1" in f for f in flags)


def test_tier_one_does_not_flag_a_balanced_game():
    assert evaluate.tier1(RPS, seeds=range(1, 25))["flags"] == []


# -- the flow --------------------------------------------------------------


def test_the_flow_converts_a_game_and_leaves_every_artifact():
    inv, root = world()
    m = Models()
    out = run_flow("rps", m, inv, root)
    assert out.verdict == "ready_for_review", out
    for name in ("spec.json", "SPEC.md", "game.json", "scenarios.json", "report.json", "REPORT.md"):
        assert (root / "rps" / name).exists(), name
    assert m.calls == ["spec", "scenarios", "encode"]
    rec = inv.get("rps")
    assert rec.status == "evaluated" and rec.port.endswith("game.json")
    assert "# rps: ready for review" in (root / "rps" / "REPORT.md").read_text()


def test_a_second_run_asks_no_model_for_what_is_already_on_disk():
    inv, root = world()
    run_flow("rps", Models(), inv, root)
    again = Models()
    assert run_flow("rps", again, inv, root).verdict == "ready_for_review" and again.calls == []
    redo = Models()
    run_flow("rps", redo, inv, root, redo=("scenarios",))
    assert redo.calls == ["scenarios"]


def test_only_ready_games_are_converted():
    inv, root = world(status="blocked", blocked_by=["real_time"])
    out = run_flow("rps", Models(), inv, root)
    assert out.verdict == "needs_review" and "blocked" in out.detail


def test_a_test_that_misreads_the_spec_does_not_stop_a_file_that_works_and_leaves_the_game_unported_for_a_person():
    wrong = {**ALWAYS_ROCK, "name": "a test that misreads the spec", "expect": {"result": "seat 1"}}
    inv, root = world()
    out = run_flow("rps", Models(scenario_lists=[[wrong]]), inv, root)
    assert out.verdict == "needs_review"
    assert inv.get("rps").status == "ready"  # not ported: a person looks first
    assert (root / "rps" / "game.json").exists() and "FAIL" in (root / "rps" / "REPORT.md").read_text()


def test_attributes_that_nothing_ever_changes_are_named_but_parameters_and_scratch_attributes_are_not():
    g = json.loads(RPS_TEXT)
    g["attributes"]["player"].append({"key": "bonus", "visible": "public", "type": "number", "initial": 0})
    g["attributes"]["game"].append({"key": "rounds_total", "visible": "public", "type": "number", "initial": 10})
    _, defn, problem = enc.check(g, "rps")
    assert defn is None and "`bonus`" in problem and "`rounds_total`" in problem and "nothing updates it" in problem
    # a parameter is meant to stay put; RPS's scratch attributes (`cell`, `lead`) are written each round and so are alive
    _, defn, problem = enc.check(g, "rps", {"rounds_total"})
    assert "`rounds_total`" not in problem and "`cell`" not in problem and "`lead`" not in problem
    assert enc.dead_attributes(RPS) == []


def test_the_tests_inside_the_coders_loop_name_the_difference_so_a_zero_score_is_seen():
    g = json.loads(RPS_TEXT)
    for a in g["attributes"]["game"]:
        if a["key"] == "rounds_left":
            a["initial"] = 3
    _, defn, problem = enc.check(g, "rps", tests=[ALWAYS_ROCK, SEAT1_WINS])
    assert defn is None and "tests written independently" in problem
    assert "everyone plays the same cards" in problem or "seat 1 plays scissors" in problem
    assert enc.check(json.loads(RPS_TEXT), "rps", tests=[ALWAYS_ROCK, SEAT1_WINS])[2] == ""


def test_encoding_that_never_passes_is_reported_and_logged():
    inv, root = world()
    out = run_flow("rps", Models(games=["nope"]), inv, root)
    assert out.verdict == "encode_failed" and (root / "rps" / "encode_attempts.json").exists()


# -- the command line ------------------------------------------------------


def test_cli_show_and_evaluate_read_what_the_flow_left():
    inv, root = world()
    run_flow("rps", Models(), inv, root)
    base = ["--inventory", str(inv.root), "--root", str(root)]
    assert main([*base, "show", "rps"]) == 0
    assert main([*base, "evaluate", "rps"]) == 0
    assert main([*base, "show", "missing"]) == 1


def test_cli_rejects_an_unknown_step_and_reports_a_game_it_will_not_convert():
    inv, root = world(status="blocked", blocked_by=["real_time"])
    base = ["--inventory", str(inv.root), "--root", str(root)]
    assert main([*base, "convert", "rps", "--model", "echo:x", "--redo", "bogus"]) == 1
    assert main([*base, "convert", "rps", "--model", "echo:x"]) == 2


def test_the_spec_prompt_carries_the_engine_facts_from_the_manifest():
    system = specmod.system_with_engine_facts()
    assert "supported:" in system and "conditional_subsequence" in system and "spatial_board" in system
    assert "use `poll`, not `ask`" in system and system.startswith("You convert a game's rules")


def test_conformance_flags_a_simultaneous_choice_encoded_as_turns():
    flags = flow.conformance({**SPEC, "round": SPEC["round"] + [{"action": "poll", "who": "all", "answer": None, "effect": ""}]}, RPS)
    assert any("poll" in f for f in flags)
    assert flow.conformance(SPEC, RPS) == []


def test_a_non_muse_backend_is_built_as_the_platform_builds_it():
    from gen_game.cli import completion_for
    assert completion_for("echo:hello", "high").complete("x") == "hello"


def test_a_model_outage_in_the_spec_or_scenario_step_is_reported_not_raised():
    class Down:
        def complete(self, prompt, system=""):
            raise RuntimeError("Remote end closed connection")
    spec, err = specmod.write_spec(Down(), record().to_dict())
    assert spec is None and "model call failed" in err
    items, err = scenarios.write_scenarios(Down(), SPEC)
    assert items is None and "model call failed" in err
    inv, root = world()
    assert run_flow("rps", Down(), inv, root).verdict == "spec_failed"


def test_redoing_the_spec_discards_everything_made_from_the_old_one():
    inv, root = world()
    run_flow("rps", Models(), inv, root)
    folder = root / "rps"
    assert (folder / "game.json").exists() and (folder / "REPORT.md").exists()
    out = run_flow("rps", Models(games=["nope"]), inv, root, redo=("spec",))
    assert out.verdict == "encode_failed"
    for stale in ("game.json", "report.json", "REPORT.md"):
        assert not (folder / stale).exists(), stale
    assert (folder / "spec.json").exists()


# -- step 2: the design review -----------------------------------------------


def test_the_designer_is_given_the_goal_the_criteria_and_the_engine_s_limits():
    system = adaptmod.system_prompt()
    for c in adaptmod.CRITERIA:
        assert c in system
    assert "do not design with it" in system and "spatial_board" in system and "XColos" in system
    assert "list it under" not in system  # that wording is for the spec writer, not a designer


def test_a_valid_plan_is_accepted_and_each_flaw_is_named_when_it_is_not():
    plan, err = adaptmod.adapt(Models(), record().to_dict())
    assert err == "" and plan["variation"]["name"].startswith("Rock Paper")
    bad = json.loads(json.dumps(PLAN))
    bad["review"] = bad["review"][:3]
    bad["variation"]["rules"] = "too short"
    bad["changes"] = [{"what": "x"}]
    found = " | ".join(adaptmod.problems(bad))
    assert "one entry per criterion" in found and "too short" in found and "changes must be" in found


def test_the_designer_is_asked_again_with_the_reason_and_an_outage_is_reported():
    class Once(Models):
        def complete(self, prompt, system=""):
            self.calls.append("x")
            return "{}" if len(self.calls) == 1 else json.dumps(PLAN)
    m = Once()
    assert adaptmod.adapt(m, record().to_dict())[1] == "" and len(m.calls) == 2

    class Down:
        def complete(self, prompt, system=""):
            raise RuntimeError("503")
    assert "model call failed" in adaptmod.adapt(Down(), record().to_dict())[1]


def test_feedback_from_testing_goes_to_the_designer_as_a_request_to_revise():
    m = Models()
    adaptmod.adapt(m, record().to_dict(), feedback="- always taking the last option wins 100%")
    assert "PREVIOUS VARIATION" in m.prompts[0] and "wins 100%" in m.prompts[0]


def test_the_variation_becomes_the_source_the_spec_is_built_from():
    src = adaptmod.source_record(PLAN)
    assert src["name"] == "Rock Paper Scissors, weighted" and "How the winner is decided" in src["rules_text"]
    assert (src["players_min"], src["players_max"]) == (2, 2)


def test_the_designer_can_recommend_dropping_a_game_and_nothing_is_built():
    drop = {**PLAN, "recommendation": {"decision": "drop", "kind": "too_simple",
                                       "reason": "Every move is visible and one option always wins; nothing inside the limits changes that."}}
    del drop["variation"], drop["complexity"]
    inv, root = world()
    m = Models(plans=[drop])
    out = run_flow("rps", m, inv, root, adapt=True, judge=True)
    assert out.verdict == "dropped" and out.detail.startswith("too simple: Every move is visible")
    assert m.calls == ["adapt"]  # no spec, no encoding
    assert "Recommended drop" in (root / "rps" / "VARIATION.md").read_text()
    assert inv.get("rps").status == "rejected" and "too simple" in inv.get("rps").dropped
    row = next(l for l in inv.index_path.read_text().splitlines() if "`rps`" in l)
    assert "| dropped |" in row and "too simple" in row


def test_a_dropped_game_is_not_converted_again_until_the_reason_is_cleared():
    inv, root = world()
    run_flow("rps", Models(plans=[{**PLAN, "recommendation": {"decision": "drop", "kind": "too_complex",
             "reason": "Needs four roles and a long chain of conditional rules."}}]), inv, root, adapt=True, judge=True)
    out = run_flow("rps", Models(), inv, root, adapt=True, judge=True)
    assert out.verdict == "needs_review" and "dropped" in out.detail
    inv.save(__import__("dataclasses").replace(inv.get("rps"), dropped=""))
    assert inv.check("rps").status == "ready"


def test_a_variation_over_the_complexity_limits_is_sent_back_and_one_that_never_fits_is_dropped():
    big = {**PLAN, "complexity": {**PLAN["complexity"], "steps_per_round": complexity.LIMITS["steps_per_round"] + 5}}
    m = Models(plans=[big])
    plan, err = adaptmod.adapt(m, record().to_dict())
    assert plan is None and adaptmod.only_too_complex(err)
    assert len(m.prompts) == 3 and "simplify:" in m.prompts[1]  # the designer was told, twice
    inv, root = world()
    out = run_flow("rps", Models(plans=[big]), inv, root, adapt=True, judge=True, steps=complexity.LIMITS["steps_per_round"])
    assert out.verdict == "dropped" and out.detail.startswith("too complex: the designer could not bring")


def test_complexity_limits_measure_what_the_designer_reports_and_what_was_built():
    assert complexity.problems(PLAN["complexity"]) == []
    assert any("whole number" in p for p in complexity.problems({**PLAN["complexity"], "rounds": "ten"}))
    assert any("steps_per_round" in p and "over the limit" in p for p in complexity.over({**PLAN["complexity"], "steps_per_round": 99}))
    m = complexity.measure(RPS)
    assert m["steps_per_round"] == 22 and m["choice_steps_per_round"] == 4
    assert complexity.describe_limits().startswith(f"steps_per_round at most {complexity.LIMITS['steps_per_round']}")


def test_a_designer_that_gives_nothing_usable_stops_the_flow():
    class Junk(Models):
        def complete(self, prompt, system=""):
            return "{}"
    inv, root = world()
    assert flow.convert("rps", Junk(), inv, root).verdict == "adapt_failed"


def test_the_claude_backend_is_the_claude_cli_in_print_mode_through_the_command_adapter():
    from gen_game.cli import completion_for
    c = completion_for("claude:claude-sonnet-5-5", "low")
    assert c.command[:2] == ["claude", "-p"] and c.command[-1] == "claude-sonnet-5-5"
    assert completion_for("claude", "low").command[-1] == "claude-opus-5-5"


def test_only_outages_in_a_row_count_so_a_reply_between_them_resets_the_retries():
    class Pattern(Models):
        """outage, bad game, outage, bad game, outage, then a good game: six calls, more than the retries allow in a row"""
        script = ["out", "bad", "out", "bad", "out", "good"]

        def complete(self, prompt, system=""):
            step = self.script.pop(0)
            if step == "out":
                raise RuntimeError("Tunnel connection failed: 503")
            return "not json" if step == "bad" else RPS_TEXT
    got = enc.encode(Pattern(), SPEC, "rps", outage_retries=1, pause=lambda s: None)
    assert got.ok


def test_cli_verify_checks_a_game_file_and_a_scenarios_file_written_outside_the_flow():
    inv, root = world()
    folder = root / "rps"
    folder.mkdir(parents=True)
    base = ["--inventory", str(inv.root), "--root", str(root)]
    (folder / "game.json").write_text(RPS_TEXT)
    (folder / "scenarios.json").write_text(json.dumps([ALWAYS_ROCK]))
    assert main([*base, "verify", "rps", "game"]) == 0 and main([*base, "verify", "rps", "scenarios"]) == 0
    (folder / "game.json").write_text("{}")
    (folder / "scenarios.json").write_text("[]")
    assert main([*base, "verify", "rps", "game"]) == 1 and main([*base, "verify", "rps", "scenarios"]) == 1


def test_cli_verify_checks_a_variation_and_a_spec_too():
    inv, root = world()
    folder = root / "rps"
    folder.mkdir(parents=True)
    base = ["--inventory", str(inv.root), "--root", str(root)]
    (folder / "variation.json").write_text(json.dumps(PLAN))
    (folder / "spec.json").write_text(json.dumps(SPEC))
    assert main([*base, "verify", "rps", "variation"]) == 0 and main([*base, "verify", "rps", "spec"]) == 0
    (folder / "variation.json").write_text(json.dumps({**PLAN, "complexity": {**PLAN["complexity"], "rounds": 99}}))
    (folder / "spec.json").write_text("{}")
    assert main([*base, "verify", "rps", "variation"]) == 1 and main([*base, "verify", "rps", "spec"]) == 1


def test_muse_defaults_to_the_model_that_stays_up_and_a_named_model_wins():
    from gen_game import cli
    assert cli.MUSE_MODEL == "rl-muse-spark-1-2-playground"
    try:
        built = cli.completion_for("muse", "medium")
        named = cli.completion_for("muse:some-other-model", "low")
    except Exception:  # no key on this machine: the constructor reads it lazily, so this is not expected
        return
    assert built.model == cli.MUSE_MODEL and built.reasoning_effort == "medium" and built.max_output_tokens == 16384
    assert named.model == "some-other-model"  # Patient hands attribute lookups to the model it wraps


def test_a_patient_model_asks_again_with_growing_waits_and_gives_up_after_the_last_retry():
    from gen_game.cli import Patient

    class Flaky:
        calls = 0

        def __init__(self, fail):
            self.fail = fail

        def complete(self, prompt, system=""):
            Flaky.calls += 1
            if Flaky.calls <= self.fail:
                raise RuntimeError("Remote end closed connection without response")
            return "answer"
    waits = []
    assert Patient(Flaky(3), pause=waits.append).complete("x") == "answer" and waits == [10, 20, 40]
    Flaky.calls, waits[:] = 0, []
    try:
        Patient(Flaky(99), retries=2, pause=waits.append).complete("x")
    except RuntimeError:
        assert waits == [10, 20] and Flaky.calls == 3
    else:
        raise AssertionError("an endless outage was not reported")


def test_the_encoder_is_warned_of_the_mistakes_the_loader_has_refused():
    system = enc.system_prompt()
    assert "never `none`" in system and "no `each` key" in system and "`into`" in system



def test_a_muse_request_that_hangs_is_cut_after_three_minutes_not_ten():
    from gen_game import cli
    try:
        built = cli.completion_for("muse", "medium")
    except Exception:
        return
    assert built.inner.timeout_s == 180 and hasattr(built, "converse")
