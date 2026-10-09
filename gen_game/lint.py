"""Play-trace lint: what the match log of a built game shows that the rules checks cannot.

Rules scenarios say whether the game plays the design. They do not say whether the game talks to its
players sensibly. These checks read the logs of a few random matches, with no knowledge of the game,
for the faults that cost model calls, clutter prompts or send players garbage:

  placeholder  a message that still has `{name}` in it: the engine could not fill it in
  empty        an announcement that says nothing ("Seat 4 answers: .")
  repeated     the same announcement, to the same people, twice in one round
  one option   a question with a single possible answer, which only costs a call

`scan` is the pure part (records in, findings out), so it can be tested on its own.
"""

from __future__ import annotations

import json
import re
from collections import Counter

from gen_game import harness
from xcolos.games.definition import GameDefinition

PLACEHOLDER = re.compile(r"\{[A-Za-z_][\w.\[\]]*\}")
EMPTY = re.compile(r"(?:[:=]\s*[.,;]|\bNone|\bnull)\s*$")  # "answers: ." and "None", not a heading that ends in a colon
#: Facts that carry state dumps or per-listener text, where two equal lines are not a repeat.
NOT_A_REPEAT = ("the_table", "game_over")


def _texts(records: list[dict]):
    """(round, kind, audience, text, per_answer) for every sentence the table was told or a player was asked."""
    for r in records:
        cat = r.get("category")
        if cat == "fact":
            payload = r.get("payload") or {}
            text = payload.get("rendered")
            if text:
                yield r.get("round"), r.get("type"), json.dumps(r.get("audience"), sort_keys=True), str(text), "seat" in payload
        elif cat == "orchestrator" and r.get("type") == "action_request" and r.get("prompt"):
            yield r.get("round"), "prompt", f"seat {r.get('seat')}", str(r["prompt"]), False


def scan(records: list[dict], number_steps: frozenset = frozenset()) -> list[str]:
    """The findings in one match log, each as a sentence a coder can act on. Empty when the log is clean.

    `number_steps` are the questions that take a number: their only listed option is the word "pass", and the
    number range is what the player is really asked about, so they are not one-option questions.
    """
    found: list[str] = []
    seen: Counter = Counter()
    for rnd, kind, audience, text, per_answer in _texts(records):
        for line in text.splitlines():
            if m := PLACEHOLDER.search(line):
                found.append(f"placeholder: players are shown the literal {m.group(0)} (in `{kind}`: {line.strip()[:90]!r}); "
                             "use only names the step can fill in (see the broadcast rule: {value} and {seat})")
            if EMPTY.search(line.strip()) and kind not in ("prompt", "the_table"):
                found.append(f"empty: an announcement says nothing (in `{kind}`: {line.strip()[:90]!r}); "
                             "skip the announcement when there is nothing to say, or give it an `if`")
        if kind not in NOT_A_REPEAT and kind != "prompt" and not per_answer:  # one line per answer is a broadcast, not a repeat
            seen[(rnd, kind, audience, text)] += 1
    for (rnd, kind, audience, text), n in seen.items():
        if n > 1:
            found.append(f"repeated: the same announcement was made {n} times in round {rnd} (`{kind}`: {text[:90]!r})")
    for r in records:
        if r.get("category") == "orchestrator" and r.get("type") == "action_request":
            legal = r.get("legal_targets")
            if isinstance(legal, list) and len(legal) == 1 and r.get("action_schema") not in number_steps:
                found.append(f"one option: `{r.get('action_schema')}` offered a single option {legal[0]!r}; it only costs a call")
    return found


def trace_lint(defn: GameDefinition, seeds: range = range(1, 4)) -> dict:
    """Play a few random matches at the smallest and largest table and scan each. Findings are grouped by kind and counted."""
    findings: Counter = Counter()
    decisions, prompt_chars, matches = [], [], 0
    numbers = frozenset(_number_steps(defn))
    for n in sorted({defn.min_players, defn.max_players}):
        for seed in seeds:
            try:
                played = harness.play(defn, harness.random_agents(n, seed), seed)
            except Exception:  # noqa: BLE001 - a crash is tier 0's to report
                continue
            matches += 1
            records = played.game.log.records
            for f in scan(records, numbers):
                findings[f] += 1
            decisions.append(sum(1 for r in records if r.get("category") == "turn" and r.get("type") == "move"))
            prompt_chars += [len(str(r.get("prompt", ""))) for r in records if r.get("category") == "orchestrator" and r.get("type") == "action_request"]
    return {
        "findings": [f"{f} (in {c} of {matches} matches)" for f, c in findings.most_common(12)],
        "metrics": {"matches": matches,
                    "decisions_per_match": round(sum(decisions) / len(decisions), 1) if decisions else 0,
                    "prompt_chars_avg": round(sum(prompt_chars) / len(prompt_chars)) if prompt_chars else 0,
                    "prompt_chars_max": max(prompt_chars, default=0)},
    }


def _number_steps(defn: GameDefinition):
    def walk(steps):
        for step in steps:
            yield step
            yield from walk(getattr(step, "steps", ()) or ())

    for step in walk(defn.steps):
        if step.use in ("ask", "poll") and step.answer is not None and step.answer.type == "number":
            yield step.label.replace(" ", "_")
