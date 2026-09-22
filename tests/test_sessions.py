"""Per-agent sessions.

The kernel guarantees a seat is only ever *sent* what it is entitled to. The
session is what guarantees a seat only ever *remembers* what it was sent. These
tests cover the second half.
"""

from __future__ import annotations

import pytest

from xcolos.agents import (
    LLMAgent,
    RandomAgent,
    ScriptedAgent,
    offline_model,
    parse_action,
)
from xcolos.cli import build_match
from xcolos.protocol import Action, ActionSchema, Envelope, MsgType
from xcolos.runner import Runner
from xcolos.session import Session

SPEAK = ActionSchema(id="speak", target="text")
VOTE = ActionSchema(id="vote", target="seat", default="random")
JA_NEIN = ActionSchema(id="ballot", target="enum", choices=("ja", "nein"))


def play(seed: int, factory=None):
    game, orch, registry, host = build_match(seed, agent_factory=factory)
    Runner(game, orch, registry).run()
    return game, host


# ----------------------------------------------------------------------
# Isolation
# ----------------------------------------------------------------------


def test_every_seat_has_its_own_session_object():
    game, host = play(3)
    sessions = [host.agent(i).session for i in sorted(game.seats)]
    assert len({id(s) for s in sessions}) == len(sessions)
    assert len({s.session_id for s in sessions}) == len(sessions)


def test_session_ids_are_unique_per_seat_and_match():
    game_a, host_a = play(3)
    game_b, host_b = play(4)
    a = {host_a.agent(i).session.session_id for i in game_a.seats}
    b = {host_b.agent(i).session.session_id for i in game_b.seats}
    assert not (a & b), "two matches must not share a session id"


@pytest.mark.parametrize("seed", range(1, 11))
def test_a_session_holds_only_what_its_seat_was_sent(seed):
    """The sharpest leak check available.

    A scripted agent cannot infer anything, so everything in its session came
    from the kernel. Each session must match that seat's delivered messages
    exactly, with nothing extra.
    """
    game, host = play(seed)
    for seat in game.seats:
        session = host.agent(seat).session
        sent = [
            r["body"]
            for r in game.log.where("message", "to_agent", seat=seat)
        ]
        remembered = [t.content for t in session if t.role == "game"]
        # Repair prompts are also sent, so remembered is what arrived, in order.
        assert remembered == sent


@pytest.mark.parametrize("seed", range(1, 11))
def test_no_seat_remembers_another_seats_secret(seed):
    game, host = play(seed)
    mafia = {i for i, s in game.seats.items() if s.role == "mafia"}
    for seat in game.seats:
        if seat in mafia:
            continue
        text = host.agent(seat).session.transcript()
        assert "Your allies are seats" not in text
        assert "Your side has chosen to kill" not in text


def test_two_agents_of_the_same_class_do_not_share_state():
    a, b = ScriptedAgent(name="a"), ScriptedAgent(name="b")
    a.bind(0, "m")
    b.bind(1, "m")
    a.session.note("only mine")
    assert a.session is not b.session
    assert "only mine" in a.session.transcript()
    assert "only mine" not in b.session.transcript()


def test_binding_opens_a_fresh_session():
    agent = ScriptedAgent(name="a")
    agent.bind(2, "m1")
    agent.session.note("from the first match")
    agent.bind(2, "m2")
    assert agent.session.session_id == "m2:seat2"
    assert "from the first match" not in agent.session.transcript()


# ----------------------------------------------------------------------
# Context
# ----------------------------------------------------------------------


def test_the_session_is_in_chat_shape():
    s = Session(1, "m", system="you are a player")
    s.observe(Envelope(type=MsgType.SITUATION, match_id="m", seat=1, body="a death"))
    s.record_action(Action(type="speak", text="I saw nothing"))

    roles = [m["role"] for m in s.messages()]
    assert roles == ["system", "user", "assistant"]
    assert s.messages()[-1]["content"] == "I saw nothing"


def test_setup_is_pinned_and_survives_compaction():
    """A seat that forgets its own role is not playing the game."""
    s = Session(1, "m", system="system rules", token_budget=40)
    s.observe(Envelope(type=MsgType.GAME_START, match_id="m", seat=1, body="you are seat 1"))
    s.observe(Envelope(type=MsgType.SITUATION, match_id="m", seat=1, body="your role is mafia"))

    for i in range(60):
        s.observe(
            Envelope(
                type=MsgType.YOUR_TURN,
                match_id="m",
                seat=1,
                body=f"chatter number {i} padded out to take up room",
                turn_seq=i,
            )
        )

    text = s.transcript()
    assert "system rules" in text
    assert "your role is mafia" in text
    assert s.dropped > 0
    assert s.estimated_tokens <= s.token_budget


def test_compaction_reports_what_it_dropped():
    s = Session(1, "m", token_budget=20)
    s.observe(Envelope(type=MsgType.YOUR_TURN, match_id="m", seat=1, body="x" * 40))
    for i in range(10):
        s.observe(
            Envelope(type=MsgType.SITUATION, match_id="m", seat=1, body="y" * 100)
        )
    assert s.dropped > 0
    assert "were dropped" in s.messages()[0]["content"]


def test_an_agent_only_knows_the_living_seats_it_was_told_about():
    s = Session(1, "m")
    assert s.living_seats() == []
    s.observe(
        Envelope(
            type=MsgType.YOUR_TURN, match_id="m", seat=1, body="Living seats: [0, 1, 4]."
        )
    )
    assert s.living_seats() == [0, 1, 4]


def test_sessions_grow_during_a_real_match():
    game, host = play(7)
    for seat in game.seats:
        session = host.agent(seat).session
        assert len(session) > 1
        assert session.estimated_tokens > 0


# ----------------------------------------------------------------------
# Model-backed decisions
# ----------------------------------------------------------------------


def test_a_model_agent_plays_a_whole_match():
    game, host = play(
        5, lambda i, name: LLMAgent(name=name, completion=offline_model(i))
    )
    assert game.status.value == "ended"
    for seat in game.seats:
        agent = host.agent(seat)
        assert agent.calls > 0
        # It was prompted from its own conversation and nothing else.
        assert all(m["content"] for m in agent.session.messages())


def test_the_model_sees_only_its_own_session():
    seen: dict[int, list] = {}

    def spy(seat: int):
        def complete(messages, env):
            seen.setdefault(seat, []).append(messages)
            return f'{{"target": {env.legal_targets[0]}}}' if env.legal_targets else "ok"

        return complete

    game, host = play(6, lambda i, name: LLMAgent(name=name, completion=spy(i)))

    mafia = {i for i, s in game.seats.items() if s.role == "mafia"}
    for seat, prompts in seen.items():
        if seat in mafia:
            continue
        blob = " ".join(m["content"] for call in prompts for m in call)
        assert "Your allies are seats" not in blob


@pytest.mark.parametrize(
    "raw,expected",
    [
        ('{"target": 3}', 3),
        ("```json\n{\"target\": 2}\n```", 2),
        ("I choose seat 4.", 4),
        ("After thinking it over, seat 1 it is", 1),
        ('{"seat": 0}', 0),
    ],
)
def test_loose_model_output_is_parsed(raw, expected):
    """Forgiving about form, strict about content.

    A model that wraps a number in prose should not lose the game.
    """
    action = parse_action(raw, VOTE, (0, 1, 2, 3, 4))
    assert action is not None
    assert action.target == expected


@pytest.mark.parametrize("raw", ["", "   ", "I refuse to participate"])
def test_unusable_model_output_yields_nothing(raw):
    """Returning None hands the turn to the repair ladder, which is correct."""
    assert parse_action(raw, VOTE, (0, 1, 2)) is None


def test_enum_targets_are_matched_by_name():
    assert parse_action("I vote ja", JA_NEIN, ()).target == "ja"
    assert parse_action("nein, absolutely not", JA_NEIN, ()).target == "nein"
    assert parse_action("maybe", JA_NEIN, ()) is None


def test_text_actions_take_the_whole_reply():
    action = parse_action("  Seat 3 is lying.  ", SPEAK, ())
    assert action.text == "Seat 3 is lying."


def test_a_model_agent_records_its_own_answer_in_its_session():
    agent = LLMAgent(name="m", completion=lambda msgs, env: '{"target": 2}')
    agent.bind(0, "m")
    env = Envelope(
        type=MsgType.YOUR_TURN,
        match_id="m",
        seat=0,
        body="Vote.",
        schema=VOTE,
        legal_targets=(1, 2, 3),
    )
    action = agent.handle(env)
    assert action.target == 2
    assert agent.session.turns[-1].role == "agent"


def test_random_agents_are_reproducible_and_independent():
    a, host_a = play(9, lambda i, name: RandomAgent(name=name, seed=i))
    b, host_b = play(9, lambda i, name: RandomAgent(name=name, seed=i))
    assert a.log.stable_records()[1:] == b.log.stable_records()[1:]
