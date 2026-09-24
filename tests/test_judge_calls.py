"""The judge call: what goes out, what comes back, and what is rejected.

The output type is the load-bearing part. A call names one of a fixed set of
shapes, each of which maps onto something the system can do, and the reply is
validated against that shape before anything sees it. These tests are mostly
about what gets thrown away, because an answer the system half-understands is
worse than no answer at all.
"""

from __future__ import annotations

from xcolos.flow.judge import (
    INSTRUCTIONS,
    NO_REPLY,
    OUTPUT_KINDS,
    UPDATE_OPS,
    AlwaysJudge,
    Call,
    JudgeError,
    ModelJudge,
    Output,
    Reply,
    ScriptedJudge,
    Where,
    full_prompt,
    prompt,
    read_reply,
    system_prompt,
)

TABLE = {
    "players": [
        {"id": 1, "status": "active", "attributes": {"role": "mafia"}},
        {"id": 2, "status": "active", "attributes": {"role": "villager"}},
        {"id": 3, "status": "eliminated", "attributes": {"role": "detective"}},
    ],
    "table": {"policies": 2},
    "acting": [1, 2],
    "record": [{"round": 1, "step": "vote", "player": 1, "value": 2}],
}


def call(output: Output, task: str = "Do the thing.") -> Call:
    return Call(
        task=task,
        output=output,
        rules="A game of hidden roles.",
        table=TABLE,
        where=Where(round=2, phase="dawn", slot="check", label="dawn", tag="end[0]"),
    )


# ----------------------------------------------------------------------
# Declaring an output
# ----------------------------------------------------------------------


def test_every_declared_kind_can_describe_itself():
    needs = {
        "choice": {"options": (1, 2)},
        "messages": {"recipients": (1, 2)},
        "dispatch": {"recipients": (1, 2)},
        "state": {"players": (1, 2),
                  "targets": {"players": {"role": {"type": "text"}}}},
    }
    for kind in OUTPUT_KINDS:
        text = Output(kind=kind, **needs.get(kind, {})).schema_text()
        assert '"reason"' in text, f"{kind} must always ask for a reason"
        assert "JSON" in text


def test_an_unknown_output_type_is_refused_when_the_call_is_built():
    for bad in ("freeform", "", "Boolean"):
        try:
            Output(kind=bad)
        except JudgeError:
            pass
        else:
            raise AssertionError(f"{bad!r} should not be a valid output type")


def test_an_output_that_cannot_be_answered_is_refused():
    # A choice with nothing to choose from, or messages with nobody to write
    # to, is a bug in the caller, not something to ask a model about.
    for kwargs in ({"kind": "choice"}, {"kind": "messages"}, {"kind": "dispatch"},
                   {"kind": "state"},
                   {"kind": "state", "targets": {"players": {"role": {}}}}):
        try:
            Output(**kwargs)
        except JudgeError:
            pass
        else:
            raise AssertionError(f"{kwargs} should not build")


# ----------------------------------------------------------------------
# Reading each shape
# ----------------------------------------------------------------------


def test_boolean_takes_only_a_real_boolean():
    output = Output(kind="boolean")
    assert output.read(True) is True
    assert output.read(False) is False
    for bad in ("true", 1, 0, None, [], "yes"):
        assert output.read(bad) is None, f"{bad!r} is not a boolean"


def test_player_is_constrained_to_the_seats_offered():
    output = Output(kind="player", options=(1, 2))
    assert output.read(2) == 2
    assert output.read("2") == 2, "a seat written as text is still that seat"
    for bad in (3, 99, None, True, "Curie", [1]):
        assert output.read(bad) is None, f"{bad!r} is not a legal seat"


def test_players_checks_the_count_and_every_member():
    output = Output(kind="players", options=(1, 2, 3), count=2)
    assert output.read([1, 3]) == [1, 3]
    for bad in ([1], [1, 2, 3], [1, 9], "1,2", None, [[1], 2]):
        assert output.read(bad) is None, f"{bad!r} is not two legal seats"


def test_choice_takes_only_a_declared_option():
    output = Output(kind="choice", options=("liberal", "fascist"))
    assert output.read("liberal") == "liberal"
    for bad in ("Liberal", "", None, ["liberal"]):
        assert output.read(bad) is None


def test_number_respects_its_bounds_and_rejects_booleans():
    output = Output(kind="number", minimum=0, maximum=5)
    assert output.read(3) == 3
    assert output.read(0) == 0
    assert output.read(2.5) == 2.5
    for bad in (-1, 6, "3", None, True):
        assert output.read(bad) is None, f"{bad!r} is not a number in range"


def test_text_is_trimmed_to_the_word_limit_rather_than_rejected():
    output = Output(kind="text", max_words=3)
    assert output.read("  one two  ") == "one two"
    assert output.read("one two three four five") == "one two three"
    for bad in ("", "   ", None, 4, ["hi"]):
        assert output.read(bad) is None


def test_messages_must_cover_exactly_the_named_recipients():
    output = Output(kind="messages", recipients=(1, 2))
    assert output.read({"1": "hello", "2": "goodbye"}) == {1: "hello", 2: "goodbye"}
    assert output.read({1: "a", 2: "b"}) == {1: "a", 2: "b"}
    # A missing recipient would be a silent drop, so the whole reply is refused
    # rather than delivering a partial round of messages.
    assert output.read({"1": "hello"}) is None
    assert output.read({"1": "a", "2": "b", "3": "c"}) is None
    assert output.read({"1": "a", "2": ""}) is None
    assert output.read([["1", "a"]]) is None


def test_update_accepts_only_operations_the_system_can_apply():
    output = Output(kind="update")
    good = [{"op": "set_status", "args": {"player": 3, "to": "eliminated"}}]
    assert output.read(good) == good
    assert output.read([]) == []
    for bad in (
        [{"op": "delete_player", "args": {}}],
        [{"op": "set"}],  # args missing is fine, but this one has no args key
        [{"op": "set", "args": "everything"}],
        [{"args": {}}],
        "set everything",
        {"op": "set", "args": {}},
    ):
        if bad == [{"op": "set"}]:
            assert output.read(bad) == [{"op": "set", "args": {}}]
            continue
        assert output.read(bad) is None, f"{bad!r} must not reach the state"


def test_the_update_ops_match_what_the_executor_implements():
    from xcolos.flow import executor

    implemented = {
        name[len("_op_"):] for name in dir(executor.FlowOrchestrator)
        if name.startswith("_op_")
    }
    assert set(UPDATE_OPS) == implemented, (
        "a model must not be offered an operation with no code behind it"
    )


def test_dispatch_types_every_message_and_refuses_a_partial_round():
    output = Output(kind="dispatch", recipients=(1, 2))
    good = {"1": {"type": "info", "text": "Night falls."},
            "2": {"type": "action", "text": "Choose a target."}}
    assert output.read(good) == {
        1: {"type": "info", "text": "Night falls."},
        2: {"type": "action", "text": "Choose a target."},
    }
    for bad in (
        {"1": {"type": "info", "text": "hi"}},              # a player dropped
        {"1": {"type": "maybe", "text": "hi"},
         "2": {"type": "info", "text": "ho"}},              # not a message type
        {"1": {"type": "info"}, "2": {"type": "info", "text": "ho"}},
        {"1": "hi", "2": "ho"},                             # untyped
        {"1": {"type": "info", "text": "hi"},
         "3": {"type": "info", "text": "ho"}},              # not a recipient
    ):
        assert output.read(bad) is None, f"{bad!r} must not dispatch"


def test_a_dispatch_prompt_explains_when_to_mark_an_action():
    text = Output(kind="dispatch", recipients=(1, 2)).schema_text()
    assert "must answer before" in text
    assert '"info"' in text and '"action"' in text


# ----------------------------------------------------------------------
# Reading a whole reply
# ----------------------------------------------------------------------


def test_a_reply_missing_the_answer_field_answers_nothing():
    reply = read_reply('{"reason": "I think so"}', Output(kind="boolean"))
    assert reply.ok is False
    assert "answer" in reply.reason


def test_a_reply_whose_answer_is_the_wrong_shape_is_discarded():
    reply = read_reply('{"answer": 7, "reason": "sure"}', Output(kind="boolean"))
    assert reply.ok is False
    assert "boolean" in reply.reason
    assert reply.value is None


def test_a_valid_reply_keeps_its_reason_and_source():
    reply = read_reply(
        '{"answer": 2, "reason": "seat 2 has the most votes"}',
        Output(kind="player", options=(1, 2)),
        source="opus",
    )
    assert reply.value == 2
    assert reply.reason == "seat 2 has the most votes"
    assert reply.source == "opus"
    assert reply.ok is True
    assert reply.yes is False, "only a boolean true is a yes"


def test_no_reply_is_not_an_answer():
    assert NO_REPLY.ok is False
    assert NO_REPLY.yes is False


# ----------------------------------------------------------------------
# The prompt
# ----------------------------------------------------------------------


def test_the_prompt_carries_all_six_parts():
    made = call(Output(kind="boolean"), task="Has the town won?")
    text = full_prompt(made)
    for heading in (
        "THE GAME",
        "THE TABLE",
        "THE PLAYERS",
        "THE RECORD",
        "WHERE WE ARE",
        "YOUR TASK",
        "YOUR ANSWER",
    ):
        assert heading in text, f"{heading} is missing from the prompt"
    assert INSTRUCTIONS in text
    assert "A game of hidden roles." in text
    assert "Has the town won?" in text
    assert "Round 2" in text and 'phase "dawn"' in text and "step check" in text
    assert '"role": "mafia"' in text, "the judge is given full sight"
    assert '"policies": 2' in text, "game state as well as player state"
    assert '"step": "vote"' in text, "the record of what everyone has done"


def test_only_the_unchanging_half_is_in_the_system_prompt():
    """What is cacheable must be exactly what does not change within a match."""
    first = call(Output(kind="boolean"), task="Has the town won?")
    later = Call(
        task="Has the mafia won?",
        output=Output(kind="player", options=(1, 2)),
        rules=first.rules,
        table={"players": [{"id": 9, "status": "resting", "attributes": {}}]},
        where=Where(round=7, phase="night", slot="ask", tag="gate:x"),
    )
    assert system_prompt(first) == system_prompt(later), (
        "a system prompt that differs between calls can never be cached"
    )

    system = system_prompt(first)
    assert INSTRUCTIONS in system
    assert "A game of hidden roles." in system
    for varying in ("THE TABLE", "THE PLAYERS", "WHERE WE ARE", "YOUR TASK",
                    "YOUR ANSWER", "Round 2", "Has the town won?"):
        assert varying not in system, f"{varying!r} changes and must not be cached"

    user = prompt(first)
    assert "THE GAME" not in user, "the rules are sent once, not twice"
    assert "Has the town won?" in user


def test_the_prompt_states_the_constraints_of_the_output():
    text = prompt(call(Output(kind="choice", options=("a", "b"))))
    assert "Options: ['a', 'b']." in text

    text = prompt(call(Output(kind="player", options=(1, 2))))
    assert "only name these seats: [1, 2]" in text

    text = prompt(call(Output(kind="text", max_words=40)))
    assert "At most 40 words" in text

    text = prompt(call(Output(kind="update")))
    assert all(op in text for op in UPDATE_OPS)


def test_an_empty_section_is_left_out_rather_than_left_blank():
    text = prompt(Call(task="Decide.", output=Output(kind="boolean")))
    assert "THE GAME" not in text, "a game with no rules text needs no rules section"
    assert "YOUR TASK" in text


# ----------------------------------------------------------------------
# The stubs
# ----------------------------------------------------------------------


def test_the_scripted_judge_validates_what_its_callable_returns():
    judge = ScriptedJudge(lambda c: "not a boolean")
    reply = judge.decide(call(Output(kind="boolean")))
    assert reply.ok is False, "a stub is not exempt from the output type"
    assert len(judge.asked) == 1


def test_the_scripted_judge_passes_a_reply_through_untouched():
    judge = ScriptedJudge(lambda c: Reply(True, "because", "oracle"))
    reply = judge.decide(call(Output(kind="boolean")))
    assert (reply.yes, reply.reason, reply.source) == (True, "because", "oracle")


def test_the_always_judge_is_also_validated():
    assert AlwaysJudge(True).decide(call(Output(kind="boolean"))).yes is True
    # The same stub against an output it cannot satisfy answers nothing rather
    # than forcing a value through.
    assert AlwaysJudge(True).decide(call(Output(kind="player"))).ok is False


def test_a_model_judge_round_trips_a_typed_answer():
    class Fixed:
        def complete(self, text, system=""):
            return '{"answer": [1, 2], "reason": "both voted"}'

    judge = ModelJudge(Fixed(), name="stubbed")
    reply = judge.decide(call(Output(kind="players", options=(1, 2, 3), count=2)))
    assert reply.value == [1, 2]
    assert reply.source == "stubbed"
    assert len(judge.history) == 1
