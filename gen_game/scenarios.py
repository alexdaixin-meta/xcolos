"""Scenario tests: does the encoded game play the game the spec describes?

A second model writes them, from the spec alone: it never sees the game file, so
a misreading the encoder made is not one the tester shares. A scenario scripts
every seat's moves and states what must be true when the match ends. They are
run on the encoded game with scripted seats.

    {"name": "both cooperate every round",
     "players": 2, "seed": 1,
     "moves": {"1": ["cooperate", ...], "2": ["cooperate", ...]},
     "expect": {"result": "draw",
                "players": {"1": {"score": 40}, "2": {"score": 40}},
                "game": {"rounds_left": 0}}}

`moves` are the answers a seat gives to every question that is not free text, in
the order it is asked. Chat is answered by the harness.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from gen_game import harness
from gen_game.repair import refused
from gen_inventory.crawl import first_json
from xcolos.games.definition import GameDefinition


class Completion(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


SYSTEM = """You write test scenarios for a game, from its SPEC alone. You have not seen the game file and must not
guess at it: use only the spec's attribute keys, parameters, round steps and result names.

A scenario scripts what every seat answers and says what must be true when the match ends:

  {"name": "...", "players": n, "seed": 1,
   "moves": {"1": [answers of seat 1], "2": [answers of seat 2]},
   "expect": {"result": "<one of the spec's result names>",
              "players": {"1": {"<player attribute key>": value}, ...},
              "game": {"<game attribute key>": value}}}

`moves` lists a seat's answers, in the order it is asked, to every question that is NOT free text (a choice
from a list, or a whole number). Free-text chat is answered for you, so leave it out. Give each seat one
answer for every such question over the WHOLE game, so count the rounds and steps in the spec.

ASSERT ONLY ON WHAT AN OUTSIDE OBSERVER SEES: the result, and the attributes the message lists as observable. Never assert on
counters, scratch values, codes or whose turn it is: the coder keeps those however it likes, and a test that depends on them
fails a correct game. Assert on each player's score and on the result.

Write 4 to 6 scenarios that together exercise: each distinct way a round can score, a tie or draw if the
game has one, and the ending condition. Work out every expected value by hand from the spec's parameters and
rules. If the game has chance (a random deal or draw), only assert what chance cannot change, and say so in
the name. Never assert a value you cannot derive from the spec.

Reply with a JSON list of scenarios and nothing else."""


def problems(items, observable: dict | None = None) -> list[str]:
    if not isinstance(items, list) or not items:
        return ["reply with a non-empty JSON list of scenarios"]
    out = []
    for i, s in enumerate(items, 1):
        if not isinstance(s, dict):
            out.append(f"scenario {i} is not an object")
            continue
        for k in ("name", "players", "moves", "expect"):
            if k not in s:
                out.append(f"scenario {i}: missing {k!r}")
        if isinstance(s.get("moves"), dict) and isinstance(s.get("players"), int):
            if set(s["moves"]) != {str(n) for n in range(1, s["players"] + 1)}:
                out.append(f"scenario {i}: moves needs one entry per seat, keyed '1' to '{s['players']}'")
        if isinstance(s.get("expect"), dict) and "result" not in s["expect"]:
            out.append(f"scenario {i}: expect needs a 'result'")
        if observable is not None and isinstance(s.get("expect"), dict):
            for seat, attrs in (s["expect"].get("players") or {}).items():
                out += [f"scenario {i}: asserts on player attribute `{k}`, which is not observable (use only: {', '.join(observable['player'])})"
                        for k in (attrs or {}) if k not in observable["player"]]
            out += [f"scenario {i}: asserts on table attribute `{k}`, which is not observable (use only: {', '.join(observable['game']) or 'none'})"
                    for k in (s["expect"].get("game") or {}) if k not in observable["game"]]
    return out


def write_scenarios(completion: Completion, spec: dict, repairs: int = 2, guidance: str = "") -> tuple[list[dict] | None, str]:
    from gen_game.spec import observable as observable_of

    obs = observable_of(spec)
    prompt = ("SPEC:\n" + json.dumps(spec, indent=2) + "\n\nOBSERVABLE (the only attributes you may assert on): player: "
              + ", ".join(obs["player"]) + "; table: " + (", ".join(obs["game"]) or "none") + ".")
    if guidance:
        prompt += "\n\nEARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:\n" + guidance
    base, error, reply = prompt, "", ""
    for _ in range(repairs + 1):
        try:
            reply = completion.complete(prompt, system=SYSTEM)
            start, end = reply.find("["), reply.rfind("]")
            items = json.loads(reply[start : end + 1]) if start >= 0 < end else first_json(reply)
            found = problems(items, obs)
        except (ValueError, TypeError) as exc:
            items, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not bad scenarios
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            return items, ""
        error = "; ".join(found)
        prompt = refused(base, reply, error)
    return None, error


@dataclass
class Outcome:
    name: str
    passed: bool
    failures: list[str]
    #: What the game did with the scripted moves, for a coder who cannot otherwise see why a score is wrong.
    trace: str = ""


def run_scenario(defn: GameDefinition, s: dict) -> Outcome:
    n = s["players"]
    if not defn.min_players <= n <= defn.max_players:
        return Outcome(s["name"], False, [f"the game takes {defn.min_players} to {defn.max_players} players, not {n}"])
    agents = [harness.QueueAgent(harness.NAMES[i], s["moves"][str(i + 1)]) for i in range(n)]
    writes: list[str] = []
    from xcolos.flow.state import FlowState

    original = FlowState.set_attribute

    def spy(self, player, key, value, *, dealing=False):
        now = self.game_attributes.get(key) if player is None else self.player_attributes[player].get(key)
        if now != value and len(writes) < 40:
            writes.append(f"{'table' if player is None else f'seat {player}'} {key}: {now!r} -> {value!r}")
        return original(self, player, key, value, dealing=dealing)

    FlowState.set_attribute = spy
    try:
        p = harness.play(defn, agents, int(s.get("seed", 1)))
    except Exception as exc:  # noqa: BLE001
        return Outcome(s["name"], False, [f"the match crashed: {type(exc).__name__}: {exc}"])
    finally:
        FlowState.set_attribute = original
    fails: list[str] = []
    if p.result.status != "ended":
        fails.append(f"the match did not end ({p.result.status}: {p.result.reason})")
    exp = s["expect"]
    if p.result.winner != exp["result"]:
        fails.append(f"result: expected {exp['result']!r}, got {p.result.winner!r}")
    for seat, attrs in (exp.get("players") or {}).items():
        for key, want in attrs.items():
            got = p.attribute(int(seat), key)
            if got != want:
                fails.append(f"seat {seat} {key}: expected {want!r}, got {got!r}")
    for key, want in (exp.get("game") or {}).items():
        got = p.game_attribute(key)
        if got != want:
            fails.append(f"game {key}: expected {want!r}, got {got!r}")
    trace = ""
    if fails:
        moves = [f"r{r.get('round')} seat {r['seat']}: {r['action'].get('target')!r}" for r in p.game.log.records if r.get("type") == "move" and r["action"].get("target") is not None]
        flow = p.orchestrator.flow
        final = {f"seat {seat}": dict(flow.player_attributes[seat]) for seat in sorted(flow.player_attributes)}
        trace = (f"moves played: {'; '.join(moves[:24])}{' ...' if len(moves) > 24 else ''}. First attribute changes: {'; '.join(writes[:14])}"
                 f"{' ...' if len(writes) > 14 else ''}. Final: players {json.dumps(final, default=str)[:420]}; table {json.dumps(flow.game_attributes, default=str)[:420]}")
    for a in agents:
        if a.overrun:
            fails.append(f"{a.name} was asked {len(a.overrun)} more question(s) than scripted (first: {a.overrun[0]})")
        elif a.used < len(a.moves):
            fails.append(f"{a.name} scripted {len(a.moves)} answers but the game asked only {a.used}")
    return Outcome(s["name"], not fails, fails, trace)


def run_all(defn: GameDefinition, scenarios: list[dict]) -> list[Outcome]:
    return [run_scenario(defn, s) for s in scenarios]
