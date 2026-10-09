"""Scenario tests: does the encoded game play the rules the design says?

A second model writes them, from the spec alone: it never sees the game file, so
a misreading the encoder made is not one the tester shares. A scenario says what
each seat answers, by naming the option on offer, and states what must be true when
the match ends. They are run on the encoded game with rule-following seats.

    {"name": "a bluff that is challenged loses influence",
     "players": 3, "seed": 1, "default": "decline",
     "rules": [{"seat": 1, "options_include": "Duke", "times": 1},
               {"seat": 2, "options_include": "Challenge Yes", "times": 1}],
     "expect": {"result": "seat 1",
                "players": {"1": {"coins": 4}}}}

A rule names an option, not a position in the script, so one extra prompt in the game cannot
shift every later answer. The older form, `moves` (each seat's answers in the order asked), still
runs. Chat is answered by the harness.
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
guess at it: use only the spec's attribute keys, parameters, round steps, answer options and result names.

A scenario says what each seat answers and what must be true when the match ends. Seats answer by NAMING THE OPTION
on offer, not by counting questions:

  {"name": "...", "rule": "R3", "players": n, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "<an option from the spec>", "answer": "<optional, defaults to the same>", "times": 1},
             {"seat": 2, "options_include": "Pass", "times": "all"}],
   "expect": {"result": "<one of the spec's result names; optional when `rounds` is set>",
              "players": {"1": {"<player attribute key>": value}, ...},
              "game": {"<game attribute key>": value}}}

How a seat picks: for each question put to it, the first rule of that seat that still has uses left and whose option is on offer
is used (`times` is how many times, default 1, or "all"). A choice of seats lists the seat numbers as options
(`"options_include": 2` picks seat 2). A question no rule matches gets the scenario's `default`: "decline" (the option
that says no, pass or none, else the first), "first" or "last". Free-text chat is answered for you. Use the option names the
spec gives, exactly (for example "Income", "Challenge Yes"). Never script a rule that depends on how many questions came before:
say WHAT the seat does, and let the default cover everything else.

TEST ONE RULE AT A TIME, FROM A SITUATION YOU STATE. Do not play twenty turns to reach a situation (that needs a long hand calculation, and
long calculations go wrong). Start the match in the situation the rule needs, and stop it after the round that tests the rule:

  {"name": "Coup costs 7 and the target loses one influence", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"hand": ["Duke", "Captain"], "influence_remaining": 2}},
             "game": {"current_seat": 1}},
   "rules": [{"seat": 1, "options_include": "Coup"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"influence_remaining": 1}}}}

`given` overwrites attributes after the game has set itself up: any player attribute and any table attribute the spec lists, hidden ones
included (a hand, a deck, whose turn it is). `rounds` is how many rounds to play before stopping (one pass through the spec's round steps;
with it you assert the state at that point and `expect.result` is optional). Use `given` and `rounds: 1` for each rule's cost, gain,
block, challenge, bluff and forced action. Use a whole match (no `rounds`, so a `result`) only for an ending, from a `given` that is one move
from the end.

ASSERT ONLY ON WHAT AN OUTSIDE OBSERVER SEES: the result, and the attributes the message lists as observable. Never assert on
counters, scratch values, codes or whose turn it is: the coder keeps those however it likes, and a test that depends on them
fails a correct game. Assert on each player's score and on the result.

If the spec lists RULES (R1, R2...), write at least one scenario for EACH, and put the rule's id in the scenario as `"rule": "R3"`. A failing
scenario is then reported against that rule, so each scenario should test one rule. Otherwise write 4 to 8 scenarios, ONE PER RULE of the spec where you can: each action's cost and gain, each block, each challenge (true
claim and bluff), each forced action, each way the game ends. Work out every expected value by hand from the spec's parameters
and rules. If the game has chance (a random deal or draw), only assert what chance cannot change, and say so in the name.
Never assert a value you cannot derive from the spec.

Reply with a JSON list of scenarios and nothing else."""


def problems(items, observable: dict | None = None, rule_ids: set[str] | None = None, attribute_keys: dict | None = None) -> list[str]:
    if not isinstance(items, list) or not items:
        return ["reply with a non-empty JSON list of scenarios"]
    out = []
    for i, s in enumerate(items, 1):
        if not isinstance(s, dict):
            out.append(f"scenario {i} is not an object")
            continue
        for k in ("name", "players", "expect"):
            if k not in s:
                out.append(f"scenario {i}: missing {k!r}")
        if rule_ids is not None and s.get("rule") is not None and s["rule"] not in rule_ids:
            out.append(f"scenario {i}: cites rule {s['rule']!r}, which the spec does not list (it lists: {', '.join(sorted(rule_ids))})")
        if "moves" not in s and "rules" not in s:
            out.append(f"scenario {i}: needs `rules` (what each seat answers, by option name)")
        if "rules" in s:
            if not isinstance(s["rules"], list) or not all(isinstance(r, dict) and "options_include" in r and r.get("seat") in range(1, 10) for r in s["rules"]):
                out.append(f"scenario {i}: each rule needs a `seat` and an `options_include`")
            if s.get("default", "decline") not in ("decline", "first", "last"):
                out.append(f"scenario {i}: default is decline, first or last")
        if isinstance(s.get("moves"), dict) and isinstance(s.get("players"), int):
            if set(s["moves"]) != {str(n) for n in range(1, s["players"] + 1)}:
                out.append(f"scenario {i}: moves needs one entry per seat, keyed '1' to '{s['players']}'")
        if isinstance(s.get("expect"), dict) and "result" not in s["expect"] and s.get("rounds") is None:
            out.append(f"scenario {i}: expect needs a 'result' (or set `rounds`, to stop after that many rounds and look at the state)")
        if s.get("rounds") is not None and not (isinstance(s["rounds"], int) and s["rounds"] >= 1):
            out.append(f"scenario {i}: rounds is a whole number, 1 or more")
        if s.get("given") is not None and attribute_keys is not None:
            g = s["given"]
            for seat, vals in (g.get("players") or {}).items():
                out += [f"scenario {i}: given player attribute `{k}` is not in the spec (spec has: {', '.join(attribute_keys['player'])})"
                        for k in (vals or {}) if k not in attribute_keys["player"]]
            out += [f"scenario {i}: given table attribute `{k}` is not in the spec (spec has: {', '.join(attribute_keys['game']) or 'none'})"
                    for k in (g.get("game") or {}) if k not in attribute_keys["game"]]
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
            keys = {sc: [a['key'] for a in spec['attributes'][sc]] for sc in ('player', 'game')}
            found = problems(items, obs, {r['id'] for r in spec.get('rules') or []} or None, keys)
        except (ValueError, TypeError) as exc:
            items, found = None, [str(exc)]
        except Exception as exc:  # noqa: BLE001 - a backend that is down is not bad scenarios
            return None, f"the model call failed: {str(exc)[:200]}"
        if not found:
            text = {r["id"]: r["text"] for r in spec.get("rules") or []}
            for item in items:
                if item.get("rule") in text:
                    item["rule_text"] = text[item["rule"]]
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
    if "rules" in s:
        agents = [harness.RuleAgent(harness.NAMES[i], [r for r in s["rules"] if r["seat"] == i + 1], s.get("default", "decline")) for i in range(n)]
    else:
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
        p = harness.play(defn, agents, int(s.get("seed", 1)), given=s.get("given"), rounds=s.get("rounds"))
    except Exception as exc:  # noqa: BLE001
        return Outcome(s["name"], False, [f"the match crashed: {type(exc).__name__}: {exc}"])
    finally:
        FlowState.set_attribute = original
    fails: list[str] = []
    exp = s["expect"]
    if s.get("rounds") is None:
        if p.result.status != "ended":
            fails.append(f"the match did not end ({p.result.status}: {p.result.reason})")
        if p.result.winner != exp["result"]:
            fails.append(f"result: expected {exp['result']!r}, got {p.result.winner!r}")
    elif "result" in exp and p.result.status == "ended" and p.result.winner != exp["result"]:
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
        if isinstance(a, harness.RuleAgent):
            fails += a.unused()
            continue
        if a.overrun:
            fails.append(f"{a.name} was asked {len(a.overrun)} more question(s) than scripted (first: {a.overrun[0]})")
        elif a.used < len(a.moves):
            fails.append(f"{a.name} scripted {len(a.moves)} answers but the game asked only {a.used}")
    return Outcome(s["name"], not fails, fails, trace)


def coverage(spec: dict, items: list[dict]) -> list[str]:
    """The ids of the spec's rules that no scenario cites: rules nothing checks."""
    cited = {s.get("rule") for s in items}
    return [r["id"] for r in spec.get("rules") or [] if r["id"] not in cited]


def run_all(defn: GameDefinition, scenarios: list[dict]) -> list[Outcome]:
    """Run every scenario. A failure of one that cites a rule names it, in the rule's own words."""
    out = []
    for s in scenarios:
        o = run_scenario(defn, s)
        if not o.passed and s.get("rule_text"):
            o.failures.insert(0, f"rule {s['rule']} is broken: {s['rule_text']}")
        out.append(o)
    return out
