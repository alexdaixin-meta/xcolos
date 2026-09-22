"""Kernel guarantees: visibility, determinism, termination, failure handling."""

from __future__ import annotations

import pytest

from xcolos.agents import BrokenAgent, ScriptedAgent, SilentAgent
from xcolos.cli import SEAT_NAMES, build_match, run_match
from xcolos.game import Game
from xcolos.log import MatchLog
from xcolos.orchestrators.mafia import MafiaOrchestrator
from xcolos.protocol import DirectiveRejected
from xcolos.runner import Runner
from xcolos.state import Rng


def build(seed: int, agent_factory=None):
    """Returns (game, orchestrator, registry) so a Runner can be built directly."""
    game, orch, registry, _host = build_match(seed, agent_factory=agent_factory)
    return game, orch, registry


# ----------------------------------------------------------------------
# Visibility
# ----------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(1, 21))
def test_delivery_equals_entitlement(seed):
    """Two-way equality, not a subset.

    A subset test alone passes silently when a seat dies before delivery and
    never receives what it was owed.
    """
    game, orch, registry = build(seed)
    Runner(game, orch, registry).run()

    for seat in game.seats:
        delivered = set(game.log.deliveries_to(seat))
        entitled = {f.seq for f in game.entitled_facts(seat)}
        assert delivered == entitled, f"seat {seat} delivered != entitled"


@pytest.mark.parametrize("seed", range(1, 21))
def test_no_seat_receives_another_seats_secret(seed):
    game, orch, registry = build(seed)
    Runner(game, orch, registry).run()

    for seat in game.seats:
        for seq in game.log.deliveries_to(seat):
            assert seat in game.facts[seq].entitled


@pytest.mark.parametrize("seed", range(1, 11))
def test_role_secrecy_in_rendered_transcripts(seed):
    """The strongest check: does any seat's actual text name a foreign role?

    A scripted agent cannot infer, so anything in its transcript came from the
    kernel. If a villager's transcript says who the mafia are before a reveal,
    the kernel leaked.
    """
    game, orch, registry, host = build_match(seed)
    Runner(game, orch, registry).run()

    mafia = {i for i, s in game.seats.items() if s.role == "mafia"}
    for seat in game.seats:
        if seat in mafia:
            continue
        text = host.agent(seat).transcript()
        # A non-mafia seat must never be told the allies list.
        assert "Your allies are seats" not in text


def test_entitlement_is_frozen_at_emission_time():
    """Audience resolves against state as it stood, not current state."""
    log = MatchLog("m_freeze")
    game = Game("m_freeze", "test", 1, log)
    for name in ["a", "b"]:
        game.register_seat(name)
    game.set_role(0, "mafia", "evil")
    game.set_role(1, "mafia", "evil")

    from xcolos.state import Audience

    fact = game.emit_fact("secret", {}, Audience.faction("evil"))
    assert fact.entitled == frozenset({0, 1})

    game.eliminate(1)
    later = game.emit_fact("secret", {}, Audience.faction("evil"))
    # Entitlement on the earlier fact is unchanged by a later death.
    assert game.facts[fact.seq].entitled == frozenset({0, 1})
    assert later.entitled == frozenset({0, 1})  # faction membership survives death


# ----------------------------------------------------------------------
# Determinism
# ----------------------------------------------------------------------


@pytest.mark.parametrize("seed", [1, 7, 42])
def test_same_seed_same_match(seed):
    a, _ = run_match(seed)
    b, _ = run_match(seed)
    assert (a.winner, a.turns, a.rounds) == (b.winner, b.turns, b.rounds)


def test_same_seed_same_log():
    game1, orch1, reg1 = build(5)
    Runner(game1, orch1, reg1).run()
    game2, orch2, reg2 = build(5)
    Runner(game2, orch2, reg2).run()
    # Wall-clock stamps are the one field allowed to differ between two runs.
    assert game1.log.stable_records() == game2.log.stable_records()


def test_rng_is_reproducible_and_independent_of_globals():
    a, b = Rng(99), Rng(99)
    assert [a.below(100) for _ in range(50)] == [b.below(100) for _ in range(50)]
    assert a.digest() == b.digest()


def test_sequence_numbers_are_contiguous():
    game, orch, registry = build(3)
    Runner(game, orch, registry).run()
    assert [f.seq for f in game.facts] == list(range(len(game.facts)))


# ----------------------------------------------------------------------
# Termination and failure
# ----------------------------------------------------------------------


@pytest.mark.parametrize("seed", range(1, 31))
def test_every_match_terminates_with_a_winner(seed):
    game, orch, registry = build(seed)
    result = Runner(game, orch, registry).run()
    assert result.status == "ended"
    assert result.winner in {"good", "evil"}


@pytest.mark.parametrize("mode", ["bad_type", "bad_target", "silent"])
def test_broken_agents_do_not_stall_the_match(mode):
    game, orch, registry = build(11, lambda i, name: BrokenAgent(name=name, mode=mode))
    result = Runner(game, orch, registry).run()
    assert result.status in {"ended", "abandoned"}
    assert result.degraded_turns > 0


def test_silent_agents_are_carried_by_defaults():
    game, orch, registry = build(13, lambda i, name: SilentAgent(name=name))
    result = Runner(game, orch, registry).run()
    assert result.status in {"ended", "abandoned"}


def test_turn_cap_abandons_rather_than_looping():
    # Seed 2 ends naturally on turn 3, so the cap has to be below that to be
    # exercised at all. A cap at or above the natural length proves nothing.
    natural = build(2)
    natural_turns = Runner(*natural[:2], natural[2]).run().turns

    game, orch, registry = build(2)
    result = Runner(game, orch, registry, max_turns=natural_turns - 1).run()
    assert result.status == "abandoned"
    assert result.turns == natural_turns - 1
    assert "turn cap" in (result.reason or "")


def test_one_broken_seat_still_lets_the_match_finish():
    def factory(i, name):
        return BrokenAgent(name=name) if i == 0 else ScriptedAgent(name=name)

    game, orch, registry = build(17, factory)
    result = Runner(game, orch, registry).run()
    assert result.status == "ended"


# ----------------------------------------------------------------------
# System function validation
# ----------------------------------------------------------------------


def test_rejected_calls_are_rejected_not_silently_applied():
    log = MatchLog("m_reject")
    game = Game("m_reject", "test", 1, log)
    game.register_seat("a")

    with pytest.raises(DirectiveRejected):
        game.eliminate(99)
    with pytest.raises(DirectiveRejected):
        game.assign_office("president", 0)
    with pytest.raises(DirectiveRejected):
        game.set_global("never_declared", 1)
    with pytest.raises(DirectiveRejected):
        game._zone("no_such_zone")

    game.eliminate(0)
    with pytest.raises(DirectiveRejected):
        game.eliminate(0)  # already eliminated


def test_zone_operations_are_bounds_checked():
    from xcolos.state import Zone

    log = MatchLog("m_zone")
    game = Game("m_zone", "test", 1, log)
    game.declare_zone(Zone(id="deck", tokens=["a", "b"]))
    game.declare_zone(Zone(id="hand"))

    with pytest.raises(DirectiveRejected):
        game.zone_draw("deck", "hand", count=5)
    assert game.zone_draw("deck", "hand", count=2) == ["a", "b"]
    with pytest.raises(DirectiveRejected):
        game.zone_remove_at("hand", 7, "deck")


def test_rotation_skips_ineligible_seats_and_survives_phases():
    log = MatchLog("m_rot")
    game = Game("m_rot", "test", 1, log)
    for name in "abcd":
        game.register_seat(name)

    assert [game.next_in_rotation() for _ in range(4)] == [0, 1, 2, 3]

    game.eliminate(1)
    game.block(2, "silenced")
    game.set_rotation_cursor(0)
    assert game.next_in_rotation() == 3  # skips dead 1 and silenced 2

    game.set_phase("other")
    assert game.cursor == 3  # cursor survives the phase change

    game.unblock_all("silenced")
    assert game.next_in_rotation() == 0
