"""gen_game: harness, spec, encode, scenarios, evaluation, the CLI and the small pieces.

The flow itself is in test_flow.py. Nothing here touches a model or the network.
"""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fixtures import *  # noqa: E402,F401,F403 - the shared scripted models and fixtures
from fixtures import (ALWAYS_ROCK, ALWAYS_ROCK_MOVES, LIBRARY, PLAN, RPS, RPS_TEXT, SEAT1_WINS, SPEC, Models, record, run_flow, world)  # noqa: E402

from gen_game import adapt as adaptmod  # noqa: E402
from gen_game import complexity  # noqa: E402
from gen_game import encode as enc  # noqa: E402
from gen_game import evaluate, flow, harness, prompt, scenarios, spec as specmod  # noqa: E402
from gen_game.cli import main  # noqa: E402
from xcolos.games.loader import load  # noqa: E402

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


def test_a_spec_without_rank_by_is_a_problem_and_the_ranking_reaches_the_reviewer_and_the_coder():
    assert specmod.problems(SPEC) == []
    for ending in ({"condition": "rounds_left == 0", "decided_by": "higher score"},
                   {"condition": "rounds_left == 0", "rank_by": " ", "decided_by": "higher score"},
                   {"condition": "rounds_left == 0", "results": ["seat 1", "seat 2", "draw"], "decided_by": "higher score"}):
        assert any("rank_by" in p for p in specmod.problems({**SPEC, "ending": ending})), ending
    assert "you.score" in specmod.render(SPEC) and "you.score" in specmod.script(SPEC)
    assert "rank_by" in specmod.SYSTEM and "share the win" in specmod.SYSTEM


# -- step 3 ----------------------------------------------------------------


def test_the_encoder_is_shown_the_format_and_told_to_use_arithmetic():
    system = enc.system_prompt()
    assert "calc" in system and "# THE FORMAT" in system and "Example game: rps" in system
    assert "rank_by" in system and "you." in system
    assert "Do NOT copy" not in system  # both examples now end with `rank_by`, so there is nothing to warn about


def test_the_coder_prompt_asks_for_one_ending_ranked_by_the_spec():
    for flag in (True, False):
        text = prompt.build("rps", PLAN, SPEC, agent=flag)
        assert "`rank_by` is `you.score`" in text and "rank_by" in text
        assert "do NOT copy" not in text and "not the `auction`" not in text


def test_a_loader_error_goes_back_to_the_model_and_the_next_reply_is_used():
    g = json.loads(RPS_TEXT)
    g["steps"][0]["use"] = "shout"  # not an action
    broken = json.dumps(g)
    m = Models(games=[broken, RPS_TEXT])
    got = enc.encode(m, SPEC, "rps")
    assert got.ok and len(got.attempts) == 2 and "loader" in got.attempts[0] and got.attempts[1] == ""
    assert "shout" in m.prompts[-1]  # the loader's own words went back to the model


def test_a_game_decided_by_a_model_is_refused_with_the_reason():
    from fixtures import WINNER_RPS_DICT

    problem = enc.check(copy.deepcopy(WINNER_RPS_DICT), "rps")[2]
    assert "decided by arithmetic" in problem and "winner" in problem


def test_an_ending_without_rank_by_is_refused():
    from fixtures import RESULT_RPS_DICT

    problem = enc.check(copy.deepcopy(RESULT_RPS_DICT), "rps")[2]
    assert "ending 'seat_1_wins' has no rank_by" in problem and "ending 'draw' has no rank_by" in problem


def test_a_match_that_ends_without_standings_fails_smoke_play_and_tier_zero():
    from fixtures import RESULT_RPS_DICT
    from xcolos.games.loader import load

    defn = load(json.dumps(RESULT_RPS_DICT), source="rps")
    played = harness.play(defn, harness.random_agents(2, 1), 1)
    assert played.result.status == "ended" and played.result.winner and played.standings is None
    assert any("standings" in p for p in harness.smoke(defn))
    t0 = evaluate.tier0(defn, seeds=range(1, 3))
    assert not t0["passed"] and any("standings" in p for p in t0["problems"])
    assert harness.play(RPS, harness.random_agents(2, 1), 1).standings.keys() == {"1", "2"}


def test_a_judged_step_and_llm_wording_with_a_text_fallback_pass_the_check():
    from fixtures import JUDGED_RPS_DICT

    assert enc.check(copy.deepcopy(JUDGED_RPS_DICT), "rps")[2] == ""


def test_a_bare_sentence_when_counts_as_a_judged_step():
    from fixtures import JUDGED_RPS_DICT

    g = copy.deepcopy(JUDGED_RPS_DICT)
    g["steps"][20]["when"] = "The bonus rule applies this round."
    assert enc.check(g, "rps")[2] == ""


def test_llm_without_text_and_a_prose_ending_are_still_refused():
    from fixtures import JUDGED_RPS_DICT

    g = copy.deepcopy(JUDGED_RPS_DICT)
    del g["steps"][5]["text"]
    assert "no `text`" in enc.check(g, "rps")[2]
    g = copy.deepcopy(JUDGED_RPS_DICT)
    next(iter(g["end"].values()))["when"] = {"prose": "Seat 1 played better."}
    assert "decided by arithmetic" in enc.check(g, "rps")[2]


def test_a_spec_step_may_be_judged_and_render_shows_it():
    s = copy.deepcopy(SPEC)
    s["round"][0]["judged"] = "The bonus rule applies this round."
    assert specmod.problems(s) == [] and 'judged: "The bonus rule applies this round."' in specmod.render(s)
    s["round"][0]["judged"] = ""
    assert any("judged" in p for p in specmod.problems(s))


def _judged_copy():
    from fixtures import JUDGED_RPS_DICT

    return copy.deepcopy(JUDGED_RPS_DICT)


def test_the_coder_sees_a_judged_step_and_its_sentence():
    s = copy.deepcopy(SPEC)
    s["round"][0]["judged"] = "The bonus rule applies this round."
    shown = specmod.script(s)
    assert "The bonus rule applies this round." in shown and '"prose"' in shown


def test_a_null_judged_is_the_same_as_no_judged():
    s = copy.deepcopy(SPEC)
    s["round"][0]["judged"] = None
    assert specmod.problems(s) == [] and "judged" not in specmod.render(s) and "judged" not in specmod.script(s)


def test_an_attribute_only_a_judged_step_changes_is_not_reported_dead():
    g = _judged_copy()
    g["attributes"]["player"].append({"key": "bonuses", "visible": "public", "type": "number", "initial": 0})
    g["steps"][20]["do"].append({"adjust": {"player": 1, "key": "bonuses", "value": 1}})
    assert enc.check(g, "rps")[2] == ""


def test_llm_on_a_question_is_refused_because_it_can_skip_a_seat():
    g = _judged_copy()
    g["steps"][3]["llm"] = "Ask seat 1 for a card."
    assert "`llm`" in enc.check(g, "rps")[2]


def test_llm_on_an_outcome_branch_and_a_broadcast_without_text_are_refused():
    g = _judged_copy()
    g["steps"][1]["broadcast"] = {"llm": "Pass the opening on."}
    assert "broadcast" in enc.check(g, "rps")[2]
    g = _judged_copy()
    g["steps"][3]["outcome"] = {"chosen": {"do": [], "text": "Seat 1 has played.", "llm": "Say seat 1 has played."}}
    assert "outcome" in enc.check(g, "rps")[2]


def test_a_prose_when_that_is_really_arithmetic_is_refused():
    for when in ("rounds_left >= 3", {"prose": "rounds_left >= 3"}):
        g = _judged_copy()
        g["steps"][20]["when"] = when
        assert "calc" in enc.check(g, "rps")[2], when


def test_a_judged_when_on_a_check_is_refused_because_it_would_choose_when_the_game_ends():
    g = _judged_copy()
    g["steps"][22]["when"] = {"prose": "The table has had enough."}
    assert "check" in enc.check(g, "rps")[2]


def test_the_gateway_model_takes_the_pipelines_effort():
    import types

    from gen_game.cli import completion_for

    stand_in = "anthropic" not in sys.modules and not _importable("anthropic")
    if stand_in:  # only the construction is checked, never a call: a placeholder module is enough without the SDK
        sys.modules["anthropic"] = types.ModuleType("anthropic")
    try:
        for effort, want in (("minimal", "low"), ("low", "low"), ("medium", "medium"), ("high", "high")):
            c = completion_for("gateway", effort)
            assert c.inner.effort == want and c.inner.model == "claude-opus-5-5"
        assert completion_for("gateway:claude-sonnet-5-5", "high").inner.model == "claude-sonnet-5-5"
    finally:
        if stand_in:
            del sys.modules["anthropic"]


def _importable(name: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(name) is not None


def test_claude_through_the_gateway_is_the_generators_default_and_muse_is_still_there():
    from gen_game import cli

    p = cli.parser()
    assert p.parse_args(["convert", "x"]).model == "gateway|muse"  # Claude, or Muse when Claude cannot be reached
    assert p.parse_args(["convert", "x", "--model", "muse"]).model == "muse"
    for cmd in ("review", "revise", "brief"):
        assert p.parse_args([cmd, "x"]).model == "gateway|muse", cmd
    a = p.parse_args(["loop", "x"])
    assert (a.model, a.review_model, a.encoder, a.players) == ("gateway|muse", "gateway|muse", "completion", "muse|gateway")


def test_the_generator_uses_claude_or_muse_whichever_answers():
    import types

    from gen_game.cli import completion_for
    from xcolos.flow.backends import FallbackCompletion

    stand_in = "anthropic" not in sys.modules and not _importable("anthropic")
    if stand_in:  # only the construction is checked, never a call
        sys.modules["anthropic"] = types.ModuleType("anthropic")
    try:
        c = completion_for("gateway|muse", "high")
    finally:
        if stand_in:
            del sys.modules["anthropic"]
    assert isinstance(c.inner, FallbackCompletion)
    assert [type(b).__name__ for b in c.inner.backends] == ["AnthropicCompletion", "MuseChat"]
    assert c.inner.backends[0].effort == "high"


def test_the_cli_trusts_the_corporate_ca_bundle_as_metas_python_does():
    from gen_game.cli import trust_corporate_ca

    with tempfile.TemporaryDirectory() as d:
        bundle = Path(d) / "ca.pem"
        bundle.write_text("certificates")
        env: dict[str, str] = {}
        trust_corporate_ca(env, bundles=(str(Path(d) / "missing.pem"), str(bundle)))
        assert env == {"SSL_CERT_FILE": str(bundle)}
        env = {"SSL_CERT_FILE": "/mine.pem"}
        trust_corporate_ca(env, bundles=(str(bundle),))
        assert env == {"SSL_CERT_FILE": "/mine.pem"}  # a bundle the user chose is kept


def test_without_the_sdk_the_generator_uses_muse_alone_instead_of_stopping():
    from gen_game.cli import completion_for

    saved = sys.modules.get("anthropic", "absent")
    sys.modules["anthropic"] = None  # makes `import anthropic` fail, as under a python without the package
    try:
        c = completion_for("gateway|muse", "high")
    finally:
        if saved == "absent":
            del sys.modules["anthropic"]
        else:
            sys.modules["anthropic"] = saved
    assert type(c.inner).__name__ == "MuseChat"


def test_the_gateway_default_says_at_once_how_to_run_it_when_the_sdk_is_missing():
    from gen_game.cli import completion_for

    saved = sys.modules.get("anthropic", "absent")
    sys.modules["anthropic"] = None  # makes `import anthropic` fail, as under a python without the package
    try:
        completion_for("gateway", "high")
    except SystemExit as stop:
        assert ".venv/bin/python" in str(stop) and "--model muse" in str(stop)
    else:
        raise AssertionError("a missing SDK must stop the command before any retry waits")
    finally:
        if saved == "absent":
            del sys.modules["anthropic"]
        else:
            sys.modules["anthropic"] = saved


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
    assert any("'winner'" in p for p in scenarios.problems([{**ALWAYS_ROCK, "expect": {}}]))
    for bad in ({"winner": "seat 1"}, {"winner": []}, {"winner": [1, "x"]}, {"winner": 1, "standings": [3, 1]}):
        assert any("winner" in p or "standings" in p for p in scenarios.problems([{**ALWAYS_ROCK, "expect": bad}])), bad
    assert scenarios.problems([{**ALWAYS_ROCK, "expect": {"winner": 1, "standings": {"1": 3, "2": 1}}}]) == []


def test_a_correct_game_passes_and_a_wrong_expectation_names_the_difference():
    assert scenarios.run_scenario(RPS, ALWAYS_ROCK).passed
    bad = {**SEAT1_WINS, "expect": {"result": "seat 2", "players": {"1": {"score": 5}}}}
    out = scenarios.run_scenario(RPS, bad)
    assert not out.passed
    assert any("result: expected 'seat 2'" in f for f in out.failures) and any("seat 1 score" in f for f in out.failures)


def test_a_scenario_may_assert_the_winner_and_the_standings():
    score = 4 * 3 + 4 * 1 + 2 * 2
    right = {**SEAT1_WINS, "expect": {"winner": 1, "standings": {"1": score, "2": 0}}}
    assert scenarios.run_scenario(RPS, right).passed
    assert scenarios.run_scenario(RPS, ALWAYS_ROCK).passed  # level scores: seats 1 and 2 share the win
    out = scenarios.run_scenario(RPS, {**SEAT1_WINS, "expect": {"winner": [1, 2], "standings": {"1": 3}}})
    assert not out.passed
    assert any("winner: expected 'seats 1 and 2', got 'seat 1'" in f for f in out.failures)
    assert any(f"seat 1 standing: expected 3, got {score}" in f for f in out.failures)


def _bar_rps():
    from fixtures import BAR_RPS_DICT
    from xcolos.games.loader import load

    return load(json.dumps(BAR_RPS_DICT), source="rps")


def test_min_to_win_is_optional_in_a_spec_and_reaches_the_reviewer_and_the_coder():
    barred = {**SPEC, "ending": {**SPEC["ending"], "min_to_win": 1}}
    assert specmod.problems(barred) == []
    for bad in ("", True, [1]):
        assert any("min_to_win" in p for p in specmod.problems({**SPEC, "ending": {**SPEC["ending"], "min_to_win": bad}})), bad
    assert "min_to_win" in specmod.render(barred) and "min_to_win" in specmod.script(barred)
    assert "min_to_win" not in specmod.render(SPEC) and "min_to_win" in specmod.SYSTEM
    for flag in (True, False):
        assert "`min_to_win` is `1`" in prompt.build("rps", PLAN, barred, agent=flag)
        assert "`min_to_win` is" not in prompt.build("rps", PLAN, SPEC, agent=flag)
    assert "min_to_win" in enc.system_prompt()


def test_a_match_with_no_winner_passes_only_when_its_ending_has_min_to_win():
    from fixtures import BAR_RPS_DICT

    defn = _bar_rps()
    played = harness.play(defn, harness.random_agents(2, 1), 1)
    assert harness.no_winner(played.result.winner) and played.standings.keys() == {"1", "2"}
    assert played.end_problems() == [] and harness.smoke(defn) == []
    assert evaluate.tier0(defn, seeds=range(1, 3))["passed"]
    assert enc.check(copy.deepcopy(BAR_RPS_DICT), "rps")[2] == ""
    import dataclasses

    unbarred = dataclasses.replace(played, orchestrator=SimpleNamespace(definition=RPS))  # an ending of the same name, with no bar
    assert any("no winner" in p for p in unbarred.end_problems())


def test_a_match_with_no_winner_counts_as_a_draw_in_the_dominance_tally():
    t1 = evaluate.tier1(_bar_rps(), seeds=range(1, 13))
    assert not any("not 'seat N'" in f for f in t1["flags"])
    assert all(v["draw"] == 12 and v["win"] == v["loss"] == 0 for v in t1["dominance"].values()), t1["dominance"]


def test_a_scenario_may_assert_that_nobody_wins():
    nobody = {**ALWAYS_ROCK, "expect": {"winner": None, "standings": {"1": 0, "2": 0}}}
    assert scenarios.problems([nobody]) == []
    assert scenarios.run_scenario(_bar_rps(), nobody).passed
    out = scenarios.run_scenario(RPS, nobody)  # no bar: level scores share the win
    assert any("winner: expected no winner, got 'seats 1 and 2'" in f for f in out.failures)
    assert any("expected no winner" in f for f in scenarios.run_scenario(RPS, {**SEAT1_WINS, "expect": {"winner": None}}).failures)


def test_scripting_too_many_or_too_few_moves_is_reported_as_that():
    few = {**ALWAYS_ROCK_MOVES, "moves": {"1": ["rock"], "2": ["rock"]}}
    assert any("more question" in f for f in scenarios.run_scenario(RPS, few).failures)
    many = {**ALWAYS_ROCK_MOVES, "moves": {"1": ALWAYS_ROCK_MOVES["moves"]["1"] + ["rock"] * 3, "2": ALWAYS_ROCK_MOVES["moves"]["2"]}}
    assert scenarios.run_scenario(RPS, ALWAYS_ROCK_MOVES).passed  # the older positional form still runs
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


def _shared_rps(result: str):
    """RPS where every ending gives the whole table one result, as a team target does."""
    d = json.loads(RPS_TEXT)
    for e in d["end"].values():
        e.pop("rank_by", None)
        e["result"] = result
    return load(json.dumps(d), source="rps")


def _team_rps(bar: int):
    """RPS ranked as a team target is: by a table value every seat shares (0 rounds left at the end), with a bar to reach."""
    d = json.loads(RPS_TEXT)
    for e in d["end"].values():
        e["rank_by"], e["min_to_win"] = "rounds_left", bar
    return load(json.dumps(d), source="rps")


def test_a_shared_outcome_is_one_where_no_ending_names_a_seat():
    assert evaluate.shared_outcome(_shared_rps("no seat wins"))
    assert not evaluate.shared_outcome(RPS)


def test_a_ranking_every_seat_scores_level_on_is_a_shared_outcome():
    assert evaluate.shared_outcome(_team_rps(1))
    assert not evaluate.shared_outcome(RPS)  # `you.score` differs from seat to seat
    d = json.loads(RPS_TEXT)
    d["end"]["over"]["rank_by"] = "rounds_left + uniform(0, 1)"  # a draw at random for each seat
    assert not evaluate.shared_outcome(load(json.dumps(d), source="rps"))


def test_tier_one_expects_random_teams_to_miss_a_ranked_shared_target():
    t1 = evaluate.tier1(_team_rps(1), seeds=range(1, 13))
    assert [f for f in t1["flags"] if not any(i in f for i in flow.IGNORED_FLAGS)] == []
    assert any("no winner decided" in n and "play-test" in n for n in t1["notes"]), t1["notes"]


def test_tier_one_flags_a_ranked_shared_target_random_teams_always_reach():
    t1 = evaluate.tier1(_team_rps(0), seeds=range(1, 13))
    assert any("every random match ended 'seats 1 and 2'" in f for f in t1["flags"])
    assert t1["notes"] == []


def test_tier_one_expects_random_teams_to_miss_a_shared_target():
    t1 = evaluate.tier1(_shared_rps("no seat wins"), seeds=range(1, 13))
    assert [f for f in t1["flags"] if not any(i in f for i in flow.IGNORED_FLAGS)] == []
    assert any("no seat wins" in n and "play-test" in n for n in t1["notes"])


def test_tier_one_flags_a_shared_target_random_teams_always_reach():
    t1 = evaluate.tier1(_shared_rps("all seats win"), seeds=range(1, 13))
    assert any("every random match ended 'all seats win'" in f for f in t1["flags"])
    assert t1["notes"] == []


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


def test_the_built_file_has_its_own_attribute_limit():
    """The design counts the game's state; the built file also holds the rules' fixed numbers and its working fields."""
    built = {"steps_per_round": 11, "choice_steps_per_round": 1, "attributes": 64}  # Hanabi Trio, built correctly by Claude
    assert flow.complexity_flags({"complexity_measured": built}) == []
    over = flow.complexity_flags({"complexity_measured": {**built, "attributes": complexity.BUILT_LIMITS["attributes"] + 1}})
    assert over and "attributes" in over[0] and f"limit of {complexity.BUILT_LIMITS['attributes']}" in over[0]
    assert complexity.over({**PLAN["complexity"], "attributes": 21})  # the designer's own count is still held to 20


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
    assert cli.MUSE_MODEL == "rl-muse-spark-1-3-sglang-playground"
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


def test_the_generated_games_are_the_library_games_and_each_ends_ranked():
    from xcolos.games.loader import load_file

    data = Path(enc.ROOT) / "gen_game" / "data" / "games"
    ids = sorted(p.name for p in data.iterdir() if (p / "game.json").exists())
    assert ids == ["agram", "assurance_game", "battle_of_wits", "coup", "hanabi"]
    for game_id in ids:
        assert (data / game_id / "game.json").read_bytes() == (LIBRARY / f"{game_id}.json").read_bytes(), game_id
        defn = load_file(data / game_id / "game.json")
        assert defn.end and all(rule.rank_by for rule in defn.end), game_id
        assert enc.model_use(defn) == [], (game_id, enc.model_use(defn))
        spec = json.loads((data / game_id / "spec.json").read_text())
        assert spec["ending"]["rank_by"] == defn.end[0].rank_by, game_id
        assert str(spec["ending"].get("min_to_win", "")) == defn.end[0].min_to_win, game_id
        assert not [p for p in specmod.problems(spec) if "ending" in p or "rank_by" in p], game_id
        assert scenarios.problems(json.loads((data / game_id / "scenarios.json").read_text())) == [], game_id


def test_the_encoder_is_warned_of_the_mistakes_the_loader_has_refused():
    system = enc.system_prompt()
    assert "never `none`" in system and "no `each` key" in system and "`into`" in system


def test_the_coder_is_told_to_ask_a_question_with_one_option_and_not_skip_it():
    # Hanamikoji skipped "choose an action" when one action was left, so the forced move was never made and its tests failed
    built = prompt.build("rps", PLAN, SPEC)
    assert "still ask the question" in built and "Do not skip the question with a `when`" in built



def test_a_muse_request_that_hangs_is_cut_after_three_minutes_not_ten():
    from gen_game import cli
    try:
        built = cli.completion_for("muse", "medium")
    except Exception:
        return
    assert built.inner.timeout_s == 180 and hasattr(built, "converse")
