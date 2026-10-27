"""Playing a game definition offline, with agents that need no model.

This is the one place gen_game touches the platform's runtime: it builds a
match from a definition the way the platform's own tests do, plays it with the
agents it is given, and hands back what happened. Everything else in gen_game
(scenarios, evaluation) is a question asked of these results.
"""

from __future__ import annotations

import re

from dataclasses import dataclass
from typing import Any

from xcolos.agents import BaseAgent, RandomAgent
from xcolos.flow import FlowOrchestrator
from xcolos.flow.judge import NO_REPLY, ScriptedJudge
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


class RuleAgent(BaseAgent):
    """Answers by what is on offer, not by when it is asked.

    A scenario that scripts "the 7th answer is Steal" breaks the moment the game asks one more
    question than the script counted. These rules name the option instead:

        {"seat": 1, "options_include": "Steal"}                       answer Steal the first time it is on offer
        {"seat": 2, "options_include": "Block", "times": "all"}       answer Block every time
        {"seat": 1, "options_include": 2, "answer": 2}                pick seat 2 from a list of seats

    The first rule with uses left whose option is on offer to this seat wins. A question no rule
    matches gets the scenario's default: `decline` (No, Pass, None...), `first` or `last`.
    Rules left unused are reported, because a rule the game never matched means the game does
    not ask the question the design says it asks.
    """

    DECLINE = re.compile(r"\b(no|pass|none|nobody|decline|skip)\b", re.I)

    def __init__(self, name: str, rules: list[dict], default: str = "decline") -> None:
        super().__init__(name)
        self.rules = [dict(r, left=(None if r.get("times", 1) == "all" else int(r.get("times", 1)))) for r in rules]
        self.default = default
        self.unmatched: list[str] = []
        self.asked = 0

    @staticmethod
    def _pick(want, legal):
        for o in legal:
            if str(o).strip().lower() == str(want).strip().lower():
                return o
        near = [o for o in legal if str(want).strip().lower() in str(o).lower()]
        return near[0] if len(near) == 1 else None

    def decide(self, env) -> Action:
        schema = self._schema(env)
        if schema.target == "text":
            return Action(type=schema.id, text=SAY)
        if schema.target == "none":
            return Action(type=schema.id)
        self.asked += 1
        legal = list(env.legal_targets)
        if schema.target == "number":
            for r in self.rules:
                if r.get("number") and r["left"] != 0:
                    r["left"] = r["left"] - 1 if r["left"] else None
                    return Action(type=schema.id, target=r["answer"])
            return Action(type=schema.id, target=schema.minimum if schema.minimum is not None else 0)
        for r in self.rules:
            if r["left"] == 0 or "options_include" not in r:
                continue
            hit = self._pick(r["options_include"], legal)
            if hit is None:
                continue
            if r["left"]:
                r["left"] -= 1
            want = r.get("answer", r["options_include"])
            answer = self._pick(want, legal)
            return Action(type=schema.id, target=hit if answer is None else answer)
        if not legal:
            return Action(type=schema.id)
        if self.default == "decline":
            for o in legal:
                if self.DECLINE.search(str(o)):
                    return Action(type=schema.id, target=o)
        return Action(type=schema.id, target=legal[-1] if self.default == "last" else legal[0])

    def forced(self, value) -> None:
        """The engine answered a question with one legal option for this seat, without asking: a rule naming that option was met."""
        for r in self.rules:
            if r["left"] != 0 and "options_include" in r and self._pick(r["options_include"], [value]) is not None:
                if r["left"]:
                    r["left"] -= 1
                return

    def unused(self) -> list[str]:
        """Rules that still had uses left: `times: "all"` rules are never required to fire."""
        return [f"{self.name}: the rule for {r['options_include']!r} was never matched {'' if r['left'] == r.get('times', 1) else 'enough '}"
                "(the game never put that option to this seat)"
                for r in self.rules if r["left"] not in (None, 0)]


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

    @property
    def standings(self) -> dict[str, Any] | None:
        """Each seat's `rank_by` value as the game-over record logged it ({"1": 20, "2": 9}), or None when no ranked ending fired."""
        for r in reversed(self.game.log.records):
            if r.get("category") == "process" and r.get("type") == "end_game":
                return r.get("standings")
        return None

    @property
    def ending(self) -> Any:
        """The ending that finished the match (its EndRule), from the game-over fact; None if none fired."""
        for r in reversed(self.game.log.records):
            if r.get("category") == "fact" and r.get("type") == "game_over":
                name = (r.get("payload") or {}).get("ending")
                return next((e for e in self.orchestrator.definition.end if e.name == name), None)
        return None

    def end_problems(self) -> list[str]:
        """What is wrong with how the match finished: it must end, name a winner, and log the standings that decided it.

        A match may end with no winner only through an ending with `min_to_win`, when no seat reached the bar.
        """
        r = self.result
        if r.status != "ended":
            return [f"the match did not end ({r.status}: {r.reason})"]
        if not r.winner:
            return ["the match ended with no result"]
        if self.standings is None:
            return ["the match ended with no standings: its ending has no `rank_by`"]
        if not winning_seats(r.winner) and not (self.ending is not None and self.ending.min_to_win):
            return [f"the match ended with no winner ({r.winner!r}), and only an ending with `min_to_win` may"]
        return []


class ListenAgent(RandomAgent):
    """A random seat that keeps every message the server sent it: the text a player is actually shown, state dump and all."""

    def __init__(self, *a, **k) -> None:
        super().__init__(*a, **k)
        self.bodies: list[tuple[str, str]] = []

    def handle(self, env):
        self.bodies.append((env.type.value, env.body))
        return super().handle(env)


def listening_agents(n: int, seed: int) -> list[ListenAgent]:
    return [ListenAgent(name=NAMES[i], seed=seed * 10 + i) for i in range(n)]


def random_agents(n: int, seed: int) -> list[BaseAgent]:
    return [RandomAgent(name=NAMES[i], seed=seed * 10 + i) for i in range(n)]


def winning_seats(result: str | None) -> list[int]:
    """The seats a result names, worded as the engine words a ranked ending: "seat 2" -> [2], "seats 1, 3 and 4" -> [1, 3, 4]; else []."""
    m = re.fullmatch(r"seats? ((?:\d+, )*\d+(?: and \d+)?)", result or "")
    return [int(x) for x in re.findall(r"\d+", m.group(1))] if m else []


def no_winner(result: str | None) -> bool:
    """Whether a result is the engine's "no winner" (no seat reached `min_to_win`, or nobody could say who won)."""
    return bool(result) and result.startswith(FlowOrchestrator.NO_WINNER)


def name_seats(seats: list[int]) -> str:
    """The engine's words for the winning seats: [2] -> "seat 2", [1, 3, 4] -> "seats 1, 3 and 4"."""
    seats = sorted(seats)
    if len(seats) == 1:
        return f"seat {seats[0]}"
    return "seats " + ", ".join(map(str, seats[:-1])) + f" and {seats[-1]}"


class _GivenOrchestrator(FlowOrchestrator):
    """Starts the match from a stated situation: after setup has dealt and funded everything, the given values overwrite it.

    `given` is {"players": {"1": {"coins": 7, "hand": ["Duke", "Captain"]}}, "game": {"current_seat": 1}}. A test of one rule then
    starts at the situation that rule needs, instead of playing twenty turns to reach it.
    """

    def __init__(self, definition: GameDefinition, given: dict, judge=None) -> None:
        super().__init__(definition, judge)
        self.given = given

    def setup(self, game: Game) -> None:
        super().setup(game)
        for seat, values in (self.given.get("players") or {}).items():
            for key, value in values.items():
                self.flow.set_attribute(int(seat), key, value)
        for key, value in (self.given.get("game") or {}).items():
            self.flow.set_attribute(None, key, value)
        for seat, status in (self.given.get("status") or {}).items():  # a seat that starts the scenario already out of the game
            self.flow.set_status(int(seat), str(status))
            if not self.flow.acts(int(seat)) and game.seats[int(seat)].alive:
                game.eliminate(int(seat))


def offline_judge(answers: dict[str, bool] | None = None, default: bool = False) -> ScriptedJudge:
    """The referee for a match played with no model: a judged step is `default` (false) unless `answers` says otherwise.

    A key answers every prose condition whose sentence contains it, ignoring case; when several do, the longest wins, so a
    specific key overrides a general one. Anything that is not a true-or-false question (wording, a choice) gets no reply,
    so a step's `text` is used, as it is when no model is reachable.
    """
    keys = sorted(((k.lower(), v) for k, v in (answers or {}).items()), key=lambda kv: -len(kv[0]))

    def answer(call):
        if call.output.kind != "boolean":
            return NO_REPLY
        task = call.task.lower()
        return next((v for k, v in keys if k in task), default)

    return ScriptedJudge(answer)


def play(definition: GameDefinition, agents: list[BaseAgent], seed: int, given: dict | None = None, rounds: int | None = None, judge=None) -> Played:
    """One match to the end. Seat `i + 1` is `agents[i]`.

    `given` starts it from a stated situation, and `rounds` stops it after that many rounds (the match is then abandoned, which is
    the point: the state at the stop is what a single-rule test looks at). With no `judge`, judged steps are answered false.
    """
    judge = judge if judge is not None else offline_judge()
    if rounds is not None:
        import dataclasses

        definition = dataclasses.replace(definition, limits=dataclasses.replace(definition.limits, rounds=rounds, rounds_max=rounds))
    match_id = f"{definition.id}_{seed}"
    game = Game(match_id, definition.id, seed, MatchLog(match_id))
    registry = Registry(game.match_id)
    host = LocalAgentHost(agents, player=Player.new("operator"))
    for bound in host.register():
        index = game.register_seat(bound.name, host.host_id, bound.profile)
        registry.attach(index, host, bound)
    orchestrator = _GivenOrchestrator(definition, given, judge) if given else FlowOrchestrator(definition, judge)
    result = Runner(game, orchestrator, registry).run()
    return Played(result, game, orchestrator, agents)


def smoke(definition: GameDefinition, players: int | None = None, seeds: range = range(1, 4)) -> list[str]:
    """What is wrong, if anything, with a game played by random seats.

    Each of these is something a repair prompt can quote back to a model: the
    game crashed, did not end, ended with no result or no standings, wrote a
    malformed log, or left a seat unable to answer validly.
    """
    n = players or definition.min_players
    problems: list[str] = []
    for seed in seeds:
        try:
            p = play(definition, random_agents(n, seed), seed)
        except Exception as exc:  # noqa: BLE001 - whatever the game did, a model must be told
            return [f"seed {seed}, {n} players: the match crashed: {type(exc).__name__}: {exc}"]
        r = p.result
        problems += [f"seed {seed}, {n} players: {m}" for m in p.end_problems()]
        if r.degraded_turns:
            problems.append(f"seed {seed}, {n} players: {r.degraded_turns} turn(s) a seat could not answer validly")
        problems += [f"seed {seed}: log: {m}" for m in p.log_problems()[:3]]
        if problems:
            return problems[:5]
    return problems
