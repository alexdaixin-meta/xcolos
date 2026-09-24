"""Conditions written in plain language, answered by a judge.

The shipped Mafia states its endings as arithmetic. These tests take that same
file, rewrite only the endings as English, and give the judge a callable that
computes the original arithmetic. The two paths must then agree move for move.

That is the whole point of keeping the declarative path: it is the oracle. A
prose ending can be graded against a rule that cannot be wrong, so the question
"did the judge get it right" has an answer rather than an opinion.
"""

from __future__ import annotations

import json
from pathlib import Path

from xcolos.agents import ScriptedAgent
from xcolos.flow import FlowOrchestrator
from xcolos.flow.judge import (
    AlwaysJudge,
    Call,
    ModelJudge,
    Output,
    Reply,
    ScriptedJudge,
    Where,
    prompt,
    read_reply,
)
from xcolos.flow.state import FlowError, FlowState
from xcolos.game import Game
from xcolos.games.definition import Condition, DefinitionError, parse
from xcolos.games.loader import LIBRARY, load
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.runner import Runner

NAMES = ["Ada", "Blaise", "Curie", "Dirac", "Euler", "Fermi", "Gauss"]

MAFIA_RAW = json.loads((LIBRARY / "mafia_oracle.json").read_text(encoding="utf-8"))

#: The two endings, said in English instead of arithmetic.
PROSE_ENDINGS = [
    "Every player whose faction is evil has been eliminated.",
    "The number of living evil players is greater than or equal to the number "
    "of living good players.",
]


#: The endings are named now, so the oracle answers with a name.
ENDING_NAMES = ["town_wins", "mafia_wins"]


def prose_mafia() -> dict:
    """Mafia with its endings restated as sentences. Nothing else changes."""
    raw = json.loads(json.dumps(MAFIA_RAW))
    for name, sentence in zip(ENDING_NAMES, PROSE_ENDINGS):
        raw["end"][name]["when"] = sentence
    return raw


def living(table: dict, faction: str) -> int:
    return sum(
        1
        for p in table["players"]
        if p["attributes"].get("faction") == faction and p["status"] == "active"
    )


def oracle(call: Call) -> Reply:
    """Answer by computing what the arithmetic version of the rule would say.

    The endings arrive as one `choice` call listing all of them, so this picks
    the first label whose statement is true, exactly as the declarative loop
    picks the first rule that holds.
    """
    if call.output.kind != "choice":
        # This oracle knows the win conditions and nothing else. Anything else
        # asked of it — composing a step's messages, say — goes unanswered, and
        # the engine falls back to the game's own templates.
        return Reply(None, "not a question this oracle answers", "oracle")
    evil, good = living(call.table, "evil"), living(call.table, "good")
    verdicts = [
        ("town_wins", evil == 0, "every mafia is eliminated"),
        ("mafia_wins", evil >= good, "the mafia equal or outnumber the town"),
    ]
    for name, holds, reason in verdicts:
        if holds and name in call.output.options:
            return Reply(name, reason, "oracle")
    return Reply("continue", "the game continues", "oracle")


def play(definition, seed: int = 1, seats: int = 5, judge=None):
    log = MatchLog(f"m{seed}")
    game = Game(f"m{seed}", definition.id, seed, log)
    registry = Registry(game.match_id)
    host = LocalAgentHost(
        [ScriptedAgent(name=NAMES[i]) for i in range(seats)],
        player=Player.new("operator"),
    )
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition, judge=judge)
    return Runner(game, orchestrator, registry).run(), game


def trace(game) -> list[tuple]:
    """Every fact, who got it and what it said. The comparable shape of a match."""
    return [
        (f.round, f.type, tuple(sorted(f.entitled)), str(f.payload.get("rendered", "")))
        for f in game.facts
    ]


# ----------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------


def test_a_bare_sentence_parses_as_a_prose_condition():
    condition = Condition.parse("the town has no one left to lose", "end[0]")
    assert condition.kind == "prose"
    assert condition.prose == "the town has no one left to lose"


def test_an_explicit_prose_key_parses_the_same_way():
    condition = Condition.parse({"prose": "  nobody is left  "}, "end[0]")
    assert condition.kind == "prose"
    assert condition.prose == "nobody is left", "surrounding space is not meaning"


def test_an_empty_sentence_is_rejected_at_load():
    for empty in ("", "   ", {"prose": ""}):
        try:
            Condition.parse(empty, "end[0]")
        except DefinitionError:
            pass
        else:
            raise AssertionError(f"{empty!r} should not load")


def test_a_prose_game_loads_even_though_the_loader_cannot_read_english():
    definition = load(json.dumps(prose_mafia()), source="prose-mafia")
    assert [r.when.kind for r in definition.end] == ["prose", "prose"]
    assert definition.end[0].name == "town_wins"
    assert definition.end[0].when.prose == PROSE_ENDINGS[0]


def test_arithmetic_refuses_to_guess_at_a_sentence():
    definition = load(json.dumps(prose_mafia()), source="prose-mafia")
    state = FlowState(definition, [1, 2])
    try:
        state.holds(definition.end[0].when)
    except FlowError as error:
        assert "judge" in str(error)
    else:
        raise AssertionError("prose must not be evaluated as arithmetic")


# ----------------------------------------------------------------------
# The oracle
# ----------------------------------------------------------------------


def test_prose_endings_play_the_identical_match_to_arithmetic_ones():
    declared = load(json.dumps(MAFIA_RAW), source="mafia")
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")

    for seed in (1, 2, 3, 5, 8):
        a, game_a = play(declared, seed=seed)
        b, game_b = play(spoken, seed=seed, judge=ScriptedJudge(oracle))
        assert (a.winner, a.rounds, a.turns) == (b.winner, b.rounds, b.turns), (
            f"seed {seed}: {a.winner}/{a.rounds} vs {b.winner}/{b.rounds}"
        )
        assert trace(game_a) == trace(game_b), f"seed {seed} diverged"


def test_the_judge_is_asked_only_at_the_check_steps():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    judge = ScriptedJudge(oracle)
    play(spoken, seed=1, judge=judge)
    assert judge.asked, "a prose ending must reach the judge"
    assert {c.where.tag for c in judge.asked} == {"check"}
    assert all(c.where.slot == "check" for c in judge.asked)
    assert all(c.where.round >= 1 for c in judge.asked)


def test_all_the_endings_are_asked_about_in_a_single_call():
    """Three spoken endings must not be three sequential round trips."""
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    judge = ScriptedJudge(oracle)
    _, game = play(spoken, seed=1, judge=judge)

    checks = [r for r in game.log.records
              if r.get("category") == "process" and r.get("type") == "set_phase"]
    assert len(judge.asked) <= len(checks), (
        "at most one call per check step, however many endings are declared"
    )
    only = judge.asked[-1]
    assert only.output.kind == "choice"
    assert "continue" in only.output.options
    assert set(only.output.options) <= {"town_wins", "mafia_wins", "continue"}


def test_the_judge_sees_the_whole_table_and_the_players_do_not():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    judge = ScriptedJudge(oracle)
    play(spoken, seed=1, judge=judge)
    first = judge.asked[0].table
    assert all("role" in p["attributes"] for p in first["players"]), (
        "a referee that cannot see the roles cannot referee a hidden-role game"
    )
    assert first["record"] is not None


def test_every_ruling_is_written_to_the_log():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    _, game = play(spoken, seed=1, judge=ScriptedJudge(oracle))
    calls = [r for r in game.log.records if r.get("type") == "judge_call"]
    assert calls, "a ruling that decided a game must be readable afterwards"
    assert {"task", "output", "where", "value", "reason", "source"} <= set(calls[0])
    assert any(r["value"] not in (None, "continue") for r in calls), (
        "one ruling named the ending that finished the match"
    )


# ----------------------------------------------------------------------
# When the judge is absent or wrong
# ----------------------------------------------------------------------


def test_with_no_judge_a_prose_ending_is_declined_and_the_cap_ends_it():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    result, _ = play(spoken, seed=1)
    assert result.status != "ended", "silence must not be read as a win"
    assert "cap" in (result.reason or "").lower()


def test_a_judge_that_declines_every_ending_never_ends_a_game():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    result, _ = play(spoken, seed=1, judge=AlwaysJudge("continue"))
    assert result.status != "ended"


def test_a_judge_that_picks_an_ending_ends_the_game_on_that_one():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    result, _ = play(spoken, seed=1,
                     judge=AlwaysJudge("mafia_wins", "because I said so"))
    assert result.status == "ended"
    assert result.winner == "mafia", "mafia_wins is the mafia's ending"
    assert result.reason == "because I said so"


def test_an_answer_that_names_no_declared_ending_ends_nothing():
    spoken = load(json.dumps(prose_mafia()), source="prose-mafia")
    for answer in (True, "no_such_ending", "", "none"):
        result, _ = play(spoken, seed=1, judge=AlwaysJudge(answer))
        assert result.status != "ended", f"{answer!r} is not an ending"


def test_a_prose_gate_opens_when_nobody_can_answer_it():
    """No judge must not mean no phase. Compare against the arithmetic gate."""
    gated = json.loads(json.dumps(MAFIA_RAW))
    for step in gated["steps"]:
        if step.get("label") == "the investigation":
            step["when"] = "A detective is still alive."

    declared = load(json.dumps(MAFIA_RAW), source="mafia")
    spoken = load(json.dumps(gated), source="gated")

    _, expected = play(declared, seed=1)
    _, actual = play(spoken, seed=1)  # no judge wired in
    assert trace(actual) == trace(expected), (
        "an unanswerable gate must not silently delete a phase"
    )


def test_a_judge_can_close_a_prose_gate():
    gated = json.loads(json.dumps(MAFIA_RAW))
    for step in gated["steps"]:
        if step.get("label") == "the investigation":
            step["when"] = "A detective is still alive."
    spoken = load(json.dumps(gated), source="gated")

    _, game = play(spoken, seed=1, judge=AlwaysJudge(False))
    assert not any(f.type == "the_investigation" for f in game.facts), (
        "a closed gate must skip the step it guards"
    )


# ----------------------------------------------------------------------
# Reading a model's reply
# ----------------------------------------------------------------------


BOOL = Output(kind="boolean")


def test_a_clean_json_reply_is_read():
    reply = read_reply('{"answer": true, "reason": "no mafia remain"}', BOOL, "m")
    assert reply.value is True
    assert reply.yes is True
    assert reply.reason == "no mafia remain"


def test_json_wrapped_in_chatter_is_still_read():
    raw = 'Sure!\n```json\n{"answer": false, "reason": "two left"}\n```'
    reply = read_reply(raw, BOOL, "m")
    assert reply.value is False
    assert reply.yes is False, "false is an answer, but it is not a yes"
    assert reply.reason == "two left"


def test_an_unreadable_reply_answers_nothing():
    for raw in ("yes", "", "{not json}", '{"answer": "yes"}', "[1, 2]", "{}"):
        reply = read_reply(raw, BOOL, "m")
        assert reply.value is None, f"{raw!r} must not end a game"
        assert reply.yes is False
        assert reply.ok is False
        assert reply.reason, "a refusal must say why"


def test_a_judge_that_raises_does_not_take_the_match_down():
    class Broken:
        def complete(self, text):
            raise RuntimeError("no model here")

    reply = ModelJudge(Broken()).decide(Call(task="is it over?", output=BOOL))
    assert reply.yes is False
    assert reply.ok is False
    assert reply.source == "error"


def test_a_judge_call_is_stateless():
    """The second prompt must not contain the first question or its answer."""
    seen: list[str] = []

    class Capture:
        def complete(self, text, system=""):
            seen.append(text)
            return '{"answer": true, "reason": "ok"}'

    judge = ModelJudge(Capture())
    judge.decide(Call(task="Has the town won?", output=BOOL))
    judge.decide(Call(task="Has the mafia won?", output=BOOL))
    assert len(seen) == 2
    assert "Has the town won?" not in seen[1]
    assert "ok" not in seen[1]
    assert len(judge.history) == 2, "history is for reading back, not for prompting"


def shipped():
    for path in sorted(Path(LIBRARY).glob("*.json")):
        yield path, load(path.read_text(encoding="utf-8"), source=str(path))


def test_at_least_one_shipped_game_needs_no_model_at_all():
    """Somebody with no key, and this test suite, must still have a game.

    This used to demand it of every definition. That was too strong once a
    game deliberately written in English shipped, but the weaker version still
    protects the thing that mattered: the library is not collectively useless
    without a model.
    """
    offline = [
        path.name
        for path, definition in shipped()
        if all(rule.when.kind == "compare" for rule in definition.end)
    ]
    assert offline, "every shipped game now requires a judge"


def test_a_game_that_wants_a_judge_still_runs_without_one():
    """The fail-closed property, asserted against what actually ships.

    A definition whose endings are sentences must not end early, end wrongly,
    or crash when no model is reachable. It runs out the round cap and says so,
    which is a bug you can see rather than a match that looks finished.
    """
    for path, definition in shipped():
        if all(rule.when.kind == "compare" for rule in definition.end):
            continue
        result, _ = play(definition, seed=1)
        assert result.status != "ended", (
            f"{path.name} ended with no judge to decide its endings"
        )
        assert "cap" in (result.reason or "").lower(), (
            f"{path.name} stopped for an unclear reason: {result.reason!r}"
        )


def test_every_shipped_game_that_needs_a_judge_reaches_a_verdict_with_one():
    for path, definition in shipped():
        if all(rule.when.kind == "compare" for rule in definition.end):
            continue
        result, _ = play(definition, seed=1, judge=ScriptedJudge(oracle))
        assert result.status == "ended", f"{path.name} never finished"
        assert result.winner in {rule.result for rule in definition.end}
