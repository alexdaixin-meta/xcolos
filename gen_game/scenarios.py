"""Scenario tests: does the encoded game play the rules the design says?

A second model writes them, from the spec alone: it never sees the game file, so
a misreading the encoder made is not one the tester shares. A scenario says what
each seat answers, by naming the option on offer, and states what must be true when
the match ends. They are run on the encoded game with rule-following seats.

    {"name": "a bluff that is challenged loses influence",
     "players": 3, "seed": 1, "default": "decline",
     "rules": [{"seat": 1, "options_include": "Duke", "times": 1},
               {"seat": 2, "options_include": "Challenge Yes", "times": 1}],
     "expect": {"winner": 1,
                "players": {"1": {"coins": 4}}}}

A rule names an option, not a position in the script, so one extra prompt in the game cannot
shift every later answer. `winner` is the seat that wins, the list of seats that share the win, or
null when nobody wins (no seat reached the ending's `min_to_win`); `standings` may give seats'
`rank_by` values at the end. The older forms, `result` (the winner as the
engine words it) and `moves` (each seat's answers in the order asked), still run. Chat is answered by
the harness.
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
guess at it: use only the spec's attribute keys, parameters, round steps, answer options and ending.

A scenario says what each seat answers and what must be true when the match ends. Seats answer by NAMING THE OPTION
on offer, not by counting questions:

  {"name": "...", "rule": "R3", "players": n, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "<an option from the spec>", "answer": "<optional, defaults to the same>", "times": 1},
             {"seat": 2, "options_include": "Pass", "times": "all"}],
   "expect": {"winner": <the seat that wins, or a list of seats that share the win; optional when `rounds` is set>,
              "standings": {"1": <seat 1's value of the spec's rank_by at the end>, ...},
              "players": {"1": {"<player attribute key>": value}, ...},
              "game": {"<game attribute key>": value}}}

The winner follows the spec's ending: its `rank_by` is worked out for every seat when the game ends, the highest value wins and
seats level at the top share the win (`"winner": [1, 3]`). There is no draw: when every seat is level, `winner` lists them all.
If the ending has a `min_to_win`, a seat below it cannot win, and when no seat reaches it nobody wins: write `"winner": null`.
`standings` is optional; give it for the seats whose value you can work out by hand.

How a seat picks: for each question put to it, the first rule of that seat that still has uses left and whose option is on offer
is used (`times` is how many times, default 1, or "all"). A choice of seats lists the seat numbers as options
(`"options_include": 2` picks seat 2). A question that asks for a NUMBER (a bid, a declared total, an amount) is answered by
naming the number: `{"seat": 1, "options_include": 300}` answers 300 the first time seat 1 is asked for a number that may be
300, and a word the question accepts instead of a number is named the same way (`"options_include": "pass"`). In
`expect.offered`, a number holds when the seat was asked for a number whose range included it. A question no rule matches
gets the scenario's `default`: "decline" (the option
that says no, pass or none, else the first), "first" or "last". Free-text chat is answered for you. Use the option names the
spec gives, exactly (for example "Income", "Challenge Yes"). Never script a rule that depends on how many questions came before:
say WHAT the seat does, and let the default cover everything else.

EVERY RULE MUST BE USED: a rule the game never uses fails the scenario, because it says the game never offered that option. So
script only the answers the scenario needs. Never script a seat that the rule under test says does not act (it is not its turn,
it is out, it may not): check that with `not_offered` and with its attributes staying as they were. A question with only one
option is answered for the seat, and that uses up a rule naming the option.

An answer that was not on offer never reaches the game: the platform refuses it and asks again. So a rule about an invalid,
illegal or malformed answer cannot be tested: give it no scenario, and never set scratch values in `given` to imitate one.

TEST ONE RULE AT A TIME, FROM A SITUATION YOU STATE. Do not play twenty turns to reach a situation (that needs a long hand calculation, and
long calculations go wrong). Start the match in the situation the rule needs, and stop it after the round that tests the rule:

  {"name": "Coup costs 7 and the target loses one influence", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"coins": 7}, "2": {"hand": ["Duke", "Captain"], "influence_remaining": 2}},
             "game": {"current_seat": 1}},
   "rules": [{"seat": 1, "options_include": "Coup"}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"coins": 0}, "2": {"influence_remaining": 1}}}}

`given` overwrites attributes after the game has set itself up: any player attribute and any table attribute the spec lists, hidden ones
included (a hand, a deck, whose turn it is). A seat that is already OUT of the game needs its platform status too: `"status": {"2": "out"}` in `given`,
next to its attributes (the status id the spec names for an eliminated player). `rounds` is how many rounds to play before stopping (one pass through the spec's round steps;
with it you assert the state at that point and `expect.winner` is optional). Use `given` and `rounds: 1` for each rule's cost, gain,
block, challenge, bluff and forced action. Use a whole match (no `rounds`, so a `winner`) only for an ending, from a `given` that is one move
from the end.

Besides values, `expect` can say what status the PLATFORM holds for a seat (`"status": {"1": "out"}`: the status ids the spec names, as
set when a player is eliminated or similar), how many items a list holds (any list attribute, hidden ones included) and what a seat was or was not offered:

   "expect": {"lens": {"game": {"deck": 9}, "players": {"1": {"hand": 2}}},
              "offered": [{"seat": 2, "option": "block"}],
              "not_offered": [{"seat": 1, "option": "block"}]}

`lens` checks counts you can work out from the rules (the deck after a deal, a hand's size); `offered` / `not_offered` check the options a seat was put in
any question during the scenario (a question with one option is answered for the seat and still counts as offered). Use `rounds: 0` to look at the state
right after the game has set itself up, with no turn played and so no question asked (give it no `rules`): that is where "each seat holds 2 cards and the deck holds the rest" is checked. Write a
`not_offered` for each restriction the spec states (only the target may block, nobody may target itself, an unaffordable action is not offered).

A round step in the spec may be JUDGED: it has a `judged` sentence that a referee answers true or false at play time. For a scenario that needs
a judged step to apply, give `"judge": {"<that sentence, or a distinctive part of it>": true}`. A judged step you do not list is answered false.

ASSERT ONLY ON WHAT AN OUTSIDE OBSERVER SEES: the winner, the standings, and the attributes the message lists as observable. Never assert on
counters, scratch values, codes or whose turn it is: the coder keeps those however it likes, and a test that depends on them
fails a correct game. Assert on each player's score and on the winner.

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
        exp = s.get("expect") if isinstance(s.get("expect"), dict) else None
        if exp is not None and "result" not in exp and "winner" not in exp and s.get("rounds") is None:
            out.append(f"scenario {i}: expect needs a 'winner' (or set `rounds`, to stop after that many rounds and look at the state)")
        if exp is not None and exp.get("winner") is not None and not _seats(exp["winner"]):
            out.append(f"scenario {i}: expect.winner is a seat number, a non-empty list of seat numbers when the win is shared, "
                       "or null when nobody wins")
        if exp is not None and "standings" in exp and not (isinstance(exp["standings"], dict) and all(
                str(k).isdigit() and isinstance(v, (int, float)) and not isinstance(v, bool) for k, v in exp["standings"].items())):
            out.append(f"scenario {i}: expect.standings maps a seat number to its rank_by value, such as {{\"1\": 20}}")
        if "judge" in s and not (isinstance(s["judge"], dict) and all(isinstance(k, str) and k.strip() and isinstance(v, bool) for k, v in s["judge"].items())):
            out.append(f"scenario {i}: judge is a map from a sentence (or part of one) to true or false")
        if s.get("rounds") is not None and not (isinstance(s["rounds"], int) and s["rounds"] >= 0):
            out.append(f"scenario {i}: rounds is a whole number, 0 or more (0 looks at the state right after setup)")
        for form in ("offered", "not_offered"):
            items = (s.get("expect") or {}).get(form) if isinstance(s.get("expect"), dict) else None
            if items is not None and not (isinstance(items, list) and all(isinstance(x, dict) and "seat" in x and "option" in x for x in items)):
                out.append(f"scenario {i}: expect.{form} is a list of {{\"seat\": n, \"option\": ...}}")
        never = (s.get("expect") or {}).get("not_offered") if isinstance(s.get("expect"), dict) else None
        if isinstance(never, list) and isinstance(s.get("rules"), list):
            barred = {(str(x.get("seat")), str(x.get("option")).strip().lower()) for x in never if isinstance(x, dict)}
            out += [f"scenario {i}: seat {r['seat']} is scripted to answer {r['options_include']!r}, but `not_offered` says it is never offered that. "
                    "A rule the game never uses fails the scenario: drop the rule, and let `not_offered` check it"
                    for r in s["rules"] if isinstance(r, dict) and (str(r.get("seat")), str(r.get("options_include")).strip().lower()) in barred]
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


def _seats(winner) -> list[int]:
    """`expect.winner` as a sorted list of seats: 2 -> [2], [3, 1] -> [1, 3]; [] when it is neither."""
    items = winner if isinstance(winner, list) else [winner]
    if not items or not all(isinstance(x, int) and not isinstance(x, bool) and x >= 1 for x in items):
        return []
    return sorted(items)


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
        p = harness.play(defn, agents, int(s.get("seed", 1)), given=s.get("given"), rounds=s.get("rounds"), judge=harness.offline_judge(s.get("judge")))
    except Exception as exc:  # noqa: BLE001
        return Outcome(s["name"], False, [f"the match crashed: {type(exc).__name__}: {exc}"])
    finally:
        FlowState.set_attribute = original
    fails: list[str] = []
    exp = s["expect"]
    whole = s.get("rounds") is None
    if whole and p.result.status != "ended":
        fails.append(f"the match did not end ({p.result.status}: {p.result.reason})")
    if whole or p.result.status == "ended":  # a match stopped after `rounds` has no result to compare
        if "result" in exp and p.result.winner != exp["result"]:
            fails.append(f"result: expected {exp['result']!r}, got {p.result.winner!r}")
        if "winner" in exp and exp["winner"] is None:
            if not harness.no_winner(p.result.winner):
                fails.append(f"winner: expected no winner, got {p.result.winner!r}")
        elif "winner" in exp:
            seats = _seats(exp["winner"])
            want = harness.name_seats(seats) if seats else None
            if want is None or p.result.winner != want:
                fails.append(f"winner: expected {want or exp['winner']!r}, got {p.result.winner!r}")
        if exp.get("standings"):
            got = p.standings
            if got is None:
                fails.append("standings: expected some, but the match logged none (it did not end on a `rank_by` ending)")
            else:
                fails += [f"seat {seat} standing: expected {want!r}, got {got.get(str(seat))!r}"
                          for seat, want in exp["standings"].items() if got.get(str(seat)) != want]
    for seat, attrs in (exp.get("players") or {}).items():
        for key, want in attrs.items():
            got = p.attribute(int(seat), key)
            if got != want:
                fails.append(f"seat {seat} {key}: expected {want!r}, got {got!r}")
    for key, want in (exp.get("game") or {}).items():
        got = p.game_attribute(key)
        if got != want:
            fails.append(f"game {key}: expected {want!r}, got {got!r}")
    lens = exp.get("lens") or {}
    for seat, attrs in (lens.get("players") or {}).items():
        for key, want in attrs.items():
            got = p.attribute(int(seat), key)
            got = len(got) if isinstance(got, (list, tuple)) else got
            if got != want:
                fails.append(f"seat {seat} {key}: expected {want} items, got {got}")
    for key, want in (lens.get("game") or {}).items():
        got = p.game_attribute(key)
        got = len(got) if isinstance(got, (list, tuple)) else got
        if got != want:
            fails.append(f"game {key}: expected {want} items, got {got}")
    for seat, want in (exp.get("status") or {}).items():
        got = p.orchestrator.flow.status.get(int(seat))
        if got != want:
            fails.append(f"seat {seat} platform status: expected {want!r}, got {got!r}")
    shown: dict[int, set] = {}
    for r in p.game.log.records:
        if r.get("category") == "orchestrator" and r.get("type") == "action_request" and isinstance(r.get("legal_targets"), list):
            shown.setdefault(r.get("seat"), set()).update(map(str, r["legal_targets"]))
        elif r.get("type") == "auto_answer":
            shown.setdefault(r.get("seat"), set()).add(str(r.get("value")))
    ranges: dict[int, list] = {}  # a number question offers a range, not a list: what each seat's agent was asked
    for seat, agent in enumerate(p.agents, 1):
        for low, high, words in getattr(agent, "ranges", []):
            ranges.setdefault(seat, []).append((low, high))
            shown.setdefault(seat, set()).update(map(str, words))

    def offered(seat: int, option) -> bool:
        if str(option) in shown.get(seat, set()):
            return True
        n = harness.RuleAgent.number(option)
        return n is not None and any(harness.RuleAgent.within(n, low, high) for low, high in ranges.get(seat, []))

    for x in exp.get("offered") or []:
        if not offered(int(x["seat"]), x["option"]):
            fails.append(f"seat {x['seat']} was never offered {x['option']!r}, but should have been")
    for x in exp.get("not_offered") or []:
        if offered(int(x["seat"]), x["option"]):
            fails.append(f"seat {x['seat']} was offered {x['option']!r}, but must not be")
    trace = ""
    if fails:
        moves = [f"r{r.get('round')} seat {r['seat']}: {r['action'].get('target')!r}" for r in p.game.log.records if r.get("type") == "move" and r["action"].get("target") is not None]
        flow = p.orchestrator.flow
        final = {f"seat {seat}": dict(flow.player_attributes[seat]) for seat in sorted(flow.player_attributes)}
        trace = (f"moves played: {'; '.join(moves[:24])}{' ...' if len(moves) > 24 else ''}. First attribute changes: {'; '.join(writes[:14])}"
                 f"{' ...' if len(writes) > 14 else ''}. Final: players {json.dumps(final, default=str)[:420]}; table {json.dumps(flow.game_attributes, default=str)[:420]}")
    for a in agents:
        if isinstance(a, harness.RuleAgent):
            if s.get("rounds") != 0:  # at rounds 0 nothing is asked, so no rule can be used and none is required to be
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
