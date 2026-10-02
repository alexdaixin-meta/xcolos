"""The review: after a match, a model reads the whole of it and grades each player.

Written once the game has ended, so nothing in it can change the result or
reach a player mid-game. It is the one place every player's private thinking —
`reason`, `predict`, `adjust` — is read side by side, which is the point: a
prediction can only be judged against what the opponent was actually thinking
and actually did.

What the reviewer is given:

    the rules        what game this was
    the players      seat, name, role or side, and where each finished
    the table        the game's own state at the end, hidden values included
    the messages     what the table was told, in order, and who was told it
    the moves        every answer, with its reason, prediction and adjustment
    the result       who won, and why

What it must return, checked before anything is logged as a review:

    {"summary": "...",
     "players": [{"seat": 1, "review": "...", "score": 7}, ...]}

Every seat exactly once, every score a whole number from 1 to 10. A reply that
does not fit is logged as a failed review with the model's own words, rather
than half-used.
"""

from __future__ import annotations

import json
import re
from typing import Any

from xcolos import calls
from xcolos.game import Game

INSTRUCTIONS = """\
You are reviewing a game that has finished. You were not a player. You are \
shown everything: the messages the table was told, every move, and each \
player's private thinking at every move, which no other player ever saw:

  reason   why they made that move
  predict  what they expected their opponents to do
  adjust   how they changed their own strategy because of that

Write two things.

First, a summary of the whole game as it unfolded: the turning points, the \
moves that decided it, and how it ended. Concrete: name seats, rounds and \
numbers.

Second, a review of each player. Judge their play, not their luck. For each \
one, compare their predictions with what their opponents were actually \
thinking and actually did: were they right, and did they see it in time? Did \
their adjustments follow from their predictions, and did their moves follow \
from their reasons? Point out their best and worst moves. Then score their play \
from 1 to 10, where 1 is aimless or self-defeating and 10 is sharp, well read \
and well executed. A player can lose and still score well, or win and score \
badly.

A player who gave no reasons, predictions or adjustments is judged on their \
moves alone; say that their thinking was not recorded.

Refer to each player by seat, and as "they"."""

ANSWER = """\
Reply with JSON and nothing else:

{"summary": "<the whole game, in concrete details>",
 "players": [{"seat": <seat number>, "review": "<the review>", "score": <1 to 10>}, ...]}

One entry for every seat: %s."""


def record(game: Game, final: dict[str, Any] | None = None) -> dict[str, Any]:
    """Everything the reviewer reads, taken from the match as it was logged.

    `final` is the engine's full view at the end, where there is one: every
    player's attributes and the table's, hidden ones included. The game is
    over, so nothing in it is a secret any more.
    """
    final = final or {}
    ending = {p["id"]: p for p in final.get("players", [])}
    players = []
    for index, seat in sorted(game.seats.items()):
        entry: dict[str, Any] = {"seat": index, "name": seat.name}
        if seat.role:
            entry["role"] = seat.role
        if seat.faction:
            entry["side"] = seat.faction
        if index in ending:
            entry["status"] = ending[index].get("status")
            entry["at_the_end"] = ending[index].get("attributes", {})
        players.append(entry)
    everyone = set(game.seats)

    messages = []
    seen: set[tuple[int, str]] = set()
    for fact in game.facts:
        text = (fact.payload or {}).get("rendered")
        if not text:
            continue
        # A message sent separately to each player shows up once per player.
        # Kept once when everybody got the same words.
        if (fact.round, text) in seen:
            continue
        seen.add((fact.round, text))
        told = set(fact.entitled)
        messages.append({
            "round": fact.round,
            "to": "everyone" if told >= everyone else sorted(told),
            "text": text,
        })

    moves = []
    for r in game.log.records:
        if r.get("type") != "move":
            continue
        action = r.get("action") or {}
        move: dict[str, Any] = {
            "round": r.get("round"),
            "step": r.get("phase"),
            "seat": r.get("seat"),
            "answer": action.get("text") or action.get("target"),
        }
        for key in ("reason", "predict", "adjust"):
            if action.get(key):
                move[key] = action[key]
        if r.get("degraded"):
            move["note"] = "no usable answer; the default was taken"
        moves.append(move)

    return {
        "players": players,
        "table": final.get("table", {}),
        "messages": messages,
        "moves": moves,
        "result": {"winner": game.winner, "reason": game.reason},
    }


def prompt(record: dict[str, Any], rules: str = "") -> tuple[str, str]:
    """(system, prompt). The system half carries the instructions and rules."""
    system = INSTRUCTIONS + (f"\n\nTHE GAME\n{rules.strip()}" if rules.strip() else "")
    seats = [p["seat"] for p in record["players"]]
    body = "\n\n".join([
        "THE PLAYERS\n" + _json(record["players"]),
        "THE TABLE AT THE END\n" + _json(record["table"]),
        "THE MESSAGES\n" + _json(record["messages"]),
        "THE MOVES\n" + _json(record["moves"]),
        "THE RESULT\n" + _json(record["result"]),
        ANSWER % seats,
    ])
    return system, body


def read(raw: Any, seats: list[int]) -> tuple[dict[str, Any] | None, str]:
    """The checked review, or None and why not."""
    match = re.search(r"\{.*\}", str(raw), re.DOTALL)
    if not match:
        return None, "the reviewer did not answer in JSON"
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None, "the reviewer's answer was not valid JSON"
    if not isinstance(data, dict):
        return None, "the reviewer's answer was not an object"
    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        return None, "the review has no summary"
    rows = data.get("players")
    if not isinstance(rows, list):
        return None, "the review has no player list"

    reviews: dict[int, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            return None, "a player entry is not an object"
        try:
            seat = int(row.get("seat"))
        except (TypeError, ValueError):
            return None, f"a player entry names no seat: {row.get('seat')!r}"
        score = row.get("score")
        if isinstance(score, float) and score.is_integer():
            score = int(score)
        if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 10:
            return None, f"seat {seat}'s score is not a whole number from 1 to 10: {score!r}"
        text = row.get("review")
        if not isinstance(text, str) or not text.strip():
            return None, f"seat {seat} has no review"
        if seat not in seats or seat in reviews:
            return None, f"seat {seat} is not a player, or is reviewed twice"
        reviews[seat] = {"seat": seat, "review": text.strip(), "score": score}
    if set(reviews) != set(seats):
        missing = sorted(set(seats) - set(reviews))
        return None, f"no review for seat(s) {missing}"
    return {
        "summary": summary.strip(),
        "players": [reviews[s] for s in sorted(reviews)],
    }, ""


def review(
    game: Game,
    completion: Any,
    rules: str = "",
    source: str = "",
    final: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Ask for the review and log it. Returns what was logged.

    `completion` is anything with `complete(prompt, system=)`, the seam the
    judge uses. None logs a skipped review, because a match with no model
    reachable still has to say why it has no review.
    """
    if completion is None:
        fields = {"status": "skipped", "error": "no model is configured to write a review"}
        game.log.record("result", "review", **fields)
        return fields

    facts = record(game, final)
    system, body = prompt(facts, rules)
    try:
        raw = calls.Logged(completion, game.log, "review").complete(body, system=system)
    except Exception as error:  # a review that fails must not break anything
        fields = {"status": "failed", "error": f"the reviewer could not be reached: {error}",
                  "source": source}
        game.log.record("result", "review", **fields)
        return fields

    checked, why = read(raw, [p["seat"] for p in facts["players"]])
    if checked is None:
        fields = {"status": "failed", "error": why, "source": source, "raw": str(raw)}
    else:
        fields = {"status": "ok", "source": source, **checked}
    game.log.record("result", "review", **fields)
    return fields


def _json(value: Any) -> str:
    return json.dumps(value, indent=1, default=str, ensure_ascii=False)
