"""Playing a game definition offline, with agents that need no model.

This is the one place gen_game touches the platform's runtime: it builds a
match from a definition the way the platform's own tests do, plays it with the
agents it is given, and hands back what happened. Everything else in gen_game
(scenarios, evaluation) is a question asked of these results.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from xcolos.agents import BaseAgent, RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.game import Game
from xcolos.games.definition import GameDefinition
from xcolos.host import LocalAgentHost, Registry
from xcolos.identity import Player
from xcolos.log import VOLATILE_FIELDS, MatchLog, validate_log
from xcolos.protocol import Action
from xcolos.runner import MatchResult, Runner

NAMES = ["Ada", "Blaise", "Cleo", "Dara", "Eli", "Fay", "Gus", "Hana", "Ivo", "Jun", "Kai", "Lia"]
#: What every scripted seat says when a game asks it to talk. Scenarios are about
#: the moves that change state, not the chat, so chat is fixed.
SAY = "Noted."


class QueueAgent(BaseAgent):
    """Answers every non-text question from a fixed list, in the order asked.

    If it is asked more than it was given, it answers with the first legal move
    and records the question in `overrun`, so a scenario that scripted too few
    moves is reported as that, not as a game that misbehaved.
    """

    def __init__(self, name: str, moves: list[Any]) -> None:
        super().__init__(name)
        self.moves = list(moves)
        self.used = 0
        self.overrun: list[str] = []

    def decide(self, env) -> Action:
        schema = self._schema(env)
        if schema.target == "text":
            return Action(type=schema.id, text=SAY)
        if schema.target == "none":
            return Action(type=schema.id)
        if self.used < len(self.moves):
            self.used += 1
            return Action(type=schema.id, target=self.moves[self.used - 1])
        self.overrun.append(schema.id)
        if schema.target == "number":
            return Action(type=schema.id, target=schema.minimum if schema.minimum is not None else 0)
        return Action(type=schema.id, target=env.legal_targets[0] if env.legal_targets else None)


class FixedAgent(BaseAgent):
    """Always plays the same end of every choice: `first` or `last` legal option,
    the smallest or largest number. A probe: if a policy this thoughtless beats
    a random one every time, the game does not ask the players to think."""

    def __init__(self, name: str, policy: str) -> None:
        super().__init__(name)
        assert policy in ("first", "last")
        self.policy = policy

    def decide(self, env) -> Action:
        schema = self._schema(env)
        if schema.target == "text":
            return Action(type=schema.id, text=SAY)
        if schema.target == "none":
            return Action(type=schema.id)
        if schema.target == "number":
            low = schema.minimum if schema.minimum is not None else 0
            high = schema.maximum if schema.maximum is not None else low + 10
            return Action(type=schema.id, target=low if self.policy == "first" else max(low, high))
        legal = list(env.legal_targets)
        if not legal:
            return Action(type=schema.id)
        return Action(type=schema.id, target=legal[0] if self.policy == "first" else legal[-1])


@dataclass
class Played:
    result: MatchResult
    game: Game
    orchestrator: FlowOrchestrator
    agents: list[BaseAgent]

    def attribute(self, seat: int, key: str) -> Any:
        return self.orchestrator.flow.attribute(seat, key)

    def game_attribute(self, key: str) -> Any:
        return self.orchestrator.flow.game_attributes.get(key)

    def log_problems(self) -> list[str]:
        return validate_log(self.game.log.records)

    def comparable_log(self) -> list[dict]:
        return [{k: v for k, v in r.items() if k not in VOLATILE_FIELDS} for r in self.game.log.records]


def random_agents(n: int, seed: int) -> list[BaseAgent]:
    return [RandomAgent(name=NAMES[i], seed=seed * 10 + i) for i in range(n)]


def play(definition: GameDefinition, agents: list[BaseAgent], seed: int) -> Played:
    """One match to the end. Seat `i + 1` is `agents[i]`."""
    match_id = f"{definition.id}_{seed}"
    game = Game(match_id, definition.id, seed, MatchLog(match_id))
    registry = Registry(game.match_id)
    host = LocalAgentHost(agents, player=Player.new("operator"))
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = FlowOrchestrator(definition)
    result = Runner(game, orchestrator, registry).run()
    return Played(result, game, orchestrator, agents)


def smoke(definition: GameDefinition, players: int | None = None, seeds: range = range(1, 4)) -> list[str]:
    """What is wrong, if anything, with a game played by random seats.

    Each of these is something a repair prompt can quote back to a model: the
    game crashed, did not end, ended with no result, wrote a malformed log, or
    left a seat unable to answer validly.
    """
    n = players or definition.min_players
    problems: list[str] = []
    for seed in seeds:
        try:
            p = play(definition, random_agents(n, seed), seed)
        except Exception as exc:  # noqa: BLE001 - whatever the game did, a model must be told
            return [f"seed {seed}, {n} players: the match crashed: {type(exc).__name__}: {exc}"]
        r = p.result
        if r.status != "ended":
            problems.append(f"seed {seed}, {n} players: the match did not end ({r.status}: {r.reason})")
        elif not r.winner:
            problems.append(f"seed {seed}, {n} players: the match ended with no result")
        if r.degraded_turns:
            problems.append(f"seed {seed}, {n} players: {r.degraded_turns} turn(s) a seat could not answer validly")
        problems += [f"seed {seed}: log: {m}" for m in p.log_problems()[:3]]
        if problems:
            return problems[:5]
    return problems
