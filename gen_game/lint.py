"""Play-trace lint: what the match log of a built game shows that the rules checks cannot.

Rules scenarios say whether the game plays the design. They do not say whether the game talks to its
players sensibly. These checks read the logs of a few random matches, with no knowledge of the game,
for the faults that cost model calls, clutter prompts or send players garbage:

  placeholder  a message that still has `{name}` in it: the engine could not fill it in
  empty        an announcement that says nothing ("Seat 4 answers: .")
  blank        state printed to players with empty fields ("block_role , blocker 0"): internal bookkeeping left public
  repeated     the same announcement, to the same people, twice in one round
  one option   a question with a single possible answer, which only costs a call
  refused      an option that was offered, taken, and then taken back: the seat is asked again without it

`scan` is the pure part (records in, findings out), so it can be tested on its own.
"""

from __future__ import annotations

import json
import re
from collections import Counter

from gen_game import harness
from xcolos.games.definition import GameDefinition

PLACEHOLDER = re.compile(r"\{[A-Za-z_][\w.\[\]]*\}")
BLANK = re.compile(r"\b[a-z][a-z_]{2,} (?=[,.])")  # `block_role ,` : a state field printed with nothing after it
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
            if kind not in ("prompt", "the_table") and (b := BLANK.findall(line)) and len(b) >= 2:
                found.append(f"blank: the state shown to players has empty fields ({', '.join(x.strip() for x in b[:4])}) in `{kind}`; hide bookkeeping attributes "
                             "(`none` on the table, `ally` on a player) so only what a player can use is printed")
            if EMPTY.search(line.strip()) and kind not in ("prompt", "the_table"):
                found.append(f"empty: an announcement says nothing (in `{kind}`: {line.strip()[:90]!r}); "
                             "skip the announcement when there is nothing to say, or give it an `if`")
        if kind not in NOT_A_REPEAT and kind != "prompt" and not per_answer:  # one line per answer is a broadcast, not a repeat
            seen[(rnd, kind, audience, text)] += 1
    for (rnd, kind, audience, text), n in seen.items():
        if n > 1:
            found.append(f"repeated: the same announcement was made {n} times in round {rnd} (`{kind}`: {text[:90]!r})")
    found += _refusals(records, number_steps)
    for r in records:
        if r.get("category") == "orchestrator" and r.get("type") == "action_request":
            legal = r.get("legal_targets")
            if isinstance(legal, list) and len(legal) == 1 and r.get("action_schema") not in number_steps:
                found.append(f"one option: `{r.get('action_schema')}` offered a single option {legal[0]!r}; it only costs a call")
    return found


def scan_bodies(bodies: list[tuple[str, str]]) -> list[str]:
    """The same checks on the text each seat was sent (the rules brief, the state, the question), which is not a logged fact."""
    found: list[str] = []
    for kind, text in bodies:
        for line in str(text).splitlines():
            if m := PLACEHOLDER.search(line):
                found.append(f"placeholder: a player is shown the literal {m.group(0)} (in a `{kind}` message: {line.strip()[:90]!r}); use only names the step can fill in")
            if len(blanks := BLANK.findall(line)) >= 2:
                found.append(f"blank: the state a player is shown has empty fields ({', '.join(x.strip() for x in blanks[:4])}); hide bookkeeping attributes "
                             "(`none` on the table, `ally` on a player) so only what a player can use is printed")
    return list(dict.fromkeys(found))


def _refusals(records: list[dict], number_steps: frozenset) -> list[str]:
    """A seat offered a list, answering from it, then asked the same question again with that answer gone.

    That is a game that offered an option and then refused it: the first offer was broader than the rules allow, and
    a check afterwards took the choice back. The outcome can still be right, which is why outcome tests never see it.
    The fix is in the offer: give each seat only the options it may use.
    """
    found: list[str] = []
    last: dict[tuple, dict] = {}
    for r in records:
        key = (r.get("seat"), r.get("action_schema"), r.get("round"))
        if r.get("category") == "orchestrator" and r.get("type") == "action_request":
            if r.get("action_schema") in number_steps or not isinstance(r.get("legal_targets"), list):
                continue
            before = last.get(key)
            legal = r["legal_targets"]
            if before and "answer" in before and before["answer"] not in legal and set(legal) < set(before["legal"]):
                found.append(f"refused: seat {r.get('seat')} was offered {before['answer']!r} in `{r.get('action_schema')}`, picked it, and was asked again "
                             f"without it (round {r.get('round')}): the first offer held an option that was not allowed. Offer each seat only what it may do, "
                             "from its own state, instead of refusing afterwards")
            last[key] = {"legal": legal}
        elif r.get("category") == "turn" and r.get("type") == "move" and key in last and "answer" not in last[key]:
            last[key]["answer"] = (r.get("action") or {}).get("target")
    return found


def trace_lint(defn: GameDefinition, seeds: range = range(1, 4)) -> dict:
    """Play a few random matches at the smallest and largest table and scan each. Findings are grouped by kind and counted."""
    findings: Counter = Counter()
    decisions, prompt_chars, matches = [], [], 0
    numbers = frozenset(_number_steps(defn))
    for n in sorted({defn.min_players, defn.max_players}):
        for seed in seeds:
            try:
                agents = harness.listening_agents(n, seed)
                played = harness.play(defn, agents, seed)
                for f in scan_bodies([b for a in agents for b in a.bodies]):
                    findings[f] += 1
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
