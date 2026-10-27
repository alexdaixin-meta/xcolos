"""Notes the game declares: the private fields an agent is asked to fill in."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from xcolos.agents import ScriptedAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.definition import (
    DEFAULT_NOTES,
    RESERVED_NOTE_NAMES,
    STANDARD_NOTES,
    DefinitionError,
    parse,
)
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import MatchLog
from xcolos.messages import parse_action
from xcolos.protocol import Action, ActionSchema
from xcolos.remote import ConnectorHost
from xcolos.runner import Runner
from xcolos.tools import TableTools

LIBRARY = Path(__file__).resolve().parent.parent / "xcolos" / "games" / "library"


def rps_raw(**extra):
    raw = json.loads((LIBRARY / "rps.json").read_text(encoding="utf-8"))
    raw.update(extra)
    return copy.deepcopy(raw)


def names(definition):
    return [n.name for n in definition.notes]


def test_default_notes_when_absent():
    d = parse(rps_raw())
    assert names(d) == ["reason", "predict", "adjust"]
    assert d.notes == DEFAULT_NOTES
    assert d.declares_notes is False


def test_declared_notes_parse():
    d = parse(rps_raw(notes=[{"name": "plan"}, {"name": "reason"},
                             {"name": "adjust", "describe": "x"}]))
    assert names(d) == ["plan", "reason", "adjust"]
    assert d.notes[0].describe == STANDARD_NOTES["plan"]
    assert d.notes[2].describe == "x"
    assert d.declares_notes is True


@pytest.mark.parametrize("bad", [
    [{"name": "plan"}, {"name": "plan"}],
    *[[{"name": n, "describe": "d"}] for n in RESERVED_NOTE_NAMES],
    [{"name": "my plan", "describe": "d"}],
    [{"name": "mood"}],
])
def test_notes_rejected(bad):
    with pytest.raises(DefinitionError):
        parse(rps_raw(notes=bad))


SCHEMA = ActionSchema(id="play", target="choice", choices=("rock", "paper"))
NOTES = parse(rps_raw(notes=[{"name": "plan"}, {"name": "reason"}])).notes


def test_parse_action_keeps_declared_notes():
    action = parse_action({"response": "rock", "plan": "p", "reason": "r"},
                          SCHEMA, ("rock", "paper"), NOTES)
    assert action.notes == {"plan": "p", "reason": "r"}


def test_parse_action_drops_undeclared_notes():
    action = parse_action({"response": "rock", "plan": "p", "reason": "r", "predict": "x"},
                          SCHEMA, ("rock", "paper"), NOTES)
    assert "predict" not in action.notes


def test_action_to_json_flat():
    assert Action("play", "rock", notes={"plan": "p"}).to_json()["plan"] == "p"


def test_table_tools_ask_carries_game_notes():
    definition = parse(rps_raw(notes=[{"name": "plan"}, {"name": "reason"}, {"name": "adjust"}]))
    log = MatchLog("m_notes")
    game = Game("m_notes", definition.id, 1, log)
    registry = Registry(game.match_id)
    bots = LocalAgentHost([ScriptedAgent(name="Bot")], player=Player.new("operator"))
    conn = ConnectorHost(Player.new("table"), ["Open0"])
    b = next(iter(bots.register()))
    registry.attach(game.register_seat(b.name, bots.host_id, b.profile), bots, b)
    c = next(iter(conn.register()))
    index = game.register_seat(c.name, conn.host_id, c.profile)
    registry.attach(index, conn, c)
    runner = Runner(game, FlowOrchestrator(definition), registry, deadline_ms=60_000)
    tools = TableTools(game, runner, registry, poll_seconds=5)
    tools.offer(index, c.name)
    runner.start()
    pid = tools.summary()["open_seats"][0]["player_id"]
    ack = None
    for _ in range(60):
        state = tools.read_state(pid, ack)
        ack = state.get("ack_through", ack)
        if state.get("your_turn"):
            assert list(state["ask"]["reply_with"]) == ["response", "plan", "reason", "adjust"]
            return
    raise AssertionError("never asked to act")
