"""Step 4: evaluate an encoded game.

Tiers. The pipeline checks two things: that the game runs, and that it plays the rules the design says.

  Tier 0, validity. Random seats play at the smallest and largest table; every
  match must end with a winner, the standings its `rank_by` ending logged, and a
  valid log, no seat may be left unable to answer, and the same seed must replay
  to the same log.

  Tier 1, rules (`scenarios.py`, not here): situations written from the design's own rules, each answered by naming
  the option on offer, with the result and scores each must give. A rule the game plays differently fails.

  Reasoning (the function below, `tier1`, kept for `--judge` and `evaluate`; NOT part of the pipeline by default).
  A game where chance alone decides, or where a policy as
  thoughtless as "always take the last option" beats random seats nearly every
  time, is not asking the players to think. Reported as flags, not failures:
  a person decides what to do about one.

Whether a game rewards reasoning is to be measured later by having real models play it. These scripted checks
cannot say.
"""

from __future__ import annotations

import ast
import re
from collections import Counter

from gen_game import harness
from xcolos.agents import RandomAgent
from xcolos.games.calc import SEEDED, Expr
from xcolos.games.definition import GameDefinition
from xcolos.protocol import Action

DOMINANCE = 0.85
MIN_DECIDED = 10
#: A result saying nobody won. In a game with one shared outcome, that is the team missing its target.
NOBODY_WINS = re.compile(r"\b(no|nobody|none|no one)\b.*\bwins?\b|\blos(?:e|es|t)\b", re.I)


def not_run() -> dict:
    """The reasoning and balance checks, left out: the same shape, nothing flagged."""
    return {"flags": [], "notes": [], "random_results": {}, "dominance": {}, "skipped": True}


def shared_outcome(defn: GameDefinition) -> bool:
    """Every ending gives the whole table one outcome, as a team target does.

    Either a fixed result that names no seat, no draw and no winner, or a `rank_by` every seat scores level on
    (it reads no `you` and draws nothing at random), so the table shares the win, or nobody wins under `min_to_win`.
    """
    return bool(defn.end) and all(_ranks_level(r.rank_by) if r.rank_by else
                                  r.result and not r.winner and r.result != "draw" and not r.result.startswith("seat ")
                                  for r in defn.end)


def _ranks_level(rank_by: str) -> bool:
    """A `rank_by` that gives every seat the same value: `you` is the only thing that differs from seat to seat."""
    expr = Expr(rank_by)
    called = {n.func.id for n in ast.walk(expr.tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    return "you" not in expr.names() and not called & set(SEEDED)


def tier0(defn: GameDefinition, seeds: range = range(1, 21)) -> dict:
    problems: list[str] = []
    results: Counter = Counter()
    turns: list[int] = []
    sizes = sorted({defn.min_players, defn.max_players})
    for n in sizes:
        for seed in seeds:
            try:
                p = harness.play(defn, harness.random_agents(n, seed), seed)
            except Exception as exc:  # noqa: BLE001
                problems.append(f"{n} players, seed {seed}: crashed: {type(exc).__name__}: {exc}")
                break
            r = p.result
            problems += [f"{n} players, seed {seed}: {m}, result {r.winner!r}" for m in p.end_problems()]
            if r.degraded_turns:
                problems.append(f"{n} players, seed {seed}: {r.degraded_turns} degraded turn(s)")
            problems += [f"{n} players, seed {seed}: log: {m}" for m in p.log_problems()[:2]]
            if r.winner:
                results[r.winner] += 1
            turns.append(r.turns)
            if len(problems) >= 5:
                break
    n = defn.min_players
    a = harness.play(defn, harness.random_agents(n, 1), 1)
    b = harness.play(defn, harness.random_agents(n, 1), 1)
    if a.comparable_log() != b.comparable_log():
        problems.append("the same seed did not replay to the same log")
    return {
        "passed": not problems,
        "problems": problems[:8],
        "metrics": {"matches": len(turns), "tables": sizes, "results": dict(results),
                    "turns_min": min(turns, default=0), "turns_max": max(turns, default=0)},
    }


#: Open play (open_play): random matches per deal, more per forced answer to the seat's first choice, how many answers
#: to force, and when one answer decides (it wins OPEN_GAP more often than the next best and OPEN_RATIO times as
#: often). The same screen the task kit's `seeds` runs before it offers a starting seed.
OPEN_PLAYOUTS, OPEN_BRANCH, OPEN_OPTIONS, OPEN_GAP, OPEN_RATIO = 24, 12, 6, 0.4, 3.0


class _FirstChoice(RandomAgent):
    """A random player that can be made to give one answer to its first choice (the first question with two or more
    options on offer), and remembers that choice's options."""

    def __init__(self, name: str, seed: int, force=None) -> None:
        super().__init__(name=name, seed=seed)
        self.force, self.first = force, None

    def decide(self, env):
        options = list(env.legal_targets or ())
        if self.first is None and len(options) >= 2:
            self.first = options
            if self.force is not None and self.force in options:
                return Action(type=self._schema(env).id, target=self.force)
        return super().decide(env)


def open_verdict(seats: int, share: float, rates: dict[str, float]) -> str | None:
    """Why one deal plays narrow with random players, or None: the tested seat wins at most 1/(4 x seats) of the
    matches or loses at most that share (the deal decides), or one answer to its first choice decides."""
    edge = 1 / (4 * seats)
    if share <= edge or share >= 1 - edge:
        return f"the deal decides: the seat won {share:.0%} of random matches (open is {edge:.0%} to {1 - edge:.0%})"
    ordered = sorted(rates.items(), key=lambda kv: -kv[1])
    if len(ordered) >= 2:
        (top, best), (_, second) = ordered[0], ordered[1]
        if best - second >= OPEN_GAP and best >= OPEN_RATIO * second:
            return f"one first move decides: {top!r} won {best:.0%} of its random matches, the next best {second:.0%}"
    return None


def open_play(defn: GameDefinition, seeds: range = range(1, 4), playouts: int = OPEN_PLAYOUTS,
              branch: int = OPEN_BRANCH, options: int = OPEN_OPTIONS) -> dict:
    """Is the game narrow from a fixed deal? A task fixes the deal, so a deal where the deal itself or one first move
    decides makes every trial alike. For each seed (one deal) at the suggested table, seats tested in turn: `playouts`
    matches of random players, then `branch` more for each of up to `options` answers to the tested seat's first
    choice, that answer forced. Flags for a person, like tier1: random players cannot show what thinking players make
    of a deal, only a deal that is narrow whatever anyone thinks. No model."""
    import random as _random

    n = defn.suggested_players
    rows, flags = [], []
    for seed in seeds:
        seat = (seed - 1) % n + 1

        def play(k: int, force=None) -> tuple[bool, list]:
            agents = [_FirstChoice(name, seed * 7919 + k * 104729 + i, force if i + 1 == seat else None)
                      for i, name in enumerate(harness.NAMES[:n])]
            winner = harness.play(defn, agents, seed).result.winner
            return seat in harness.winning_seats(winner), agents[seat - 1].first or []
        base = [play(k) for k in range(playouts)]
        share = sum(w for w, _ in base) / playouts
        first = next((f for _, f in base if f), [])
        answers = first if len(first) <= options else _random.Random(seed).sample(first, options)
        rates = {str(a): round(sum(play(playouts + j * branch + k, a)[0] for k in range(branch)) / branch, 3)
                 for j, a in enumerate(answers)}
        why = open_verdict(n, share, rates)
        rows.append({"seed": seed, "seat": seat, "share": round(share, 3), "first_rates": rates, "narrow": why})
        if why:
            flags.append(f"seed {seed}, seat {seat}: {why}")
    return {"players": n, "playouts": playouts, "branch": branch, "deals": rows, "flags": flags}


def _share(counter: Counter, key: str) -> float:
    total = sum(counter.values())
    return counter[key] / total if total else 0.0


def tier1(defn: GameDefinition, seeds: range = range(1, 61)) -> dict:
    """Flags for a person to read; nothing here fails a game."""
    n = defn.min_players
    flags: list[str] = []
    random_results: Counter = Counter()
    for seed in seeds:
        random_results[harness.play(defn, harness.random_agents(n, seed), seed).result.winner] += 1
    seat_named = all(w is None or w == "draw" or harness.winning_seats(w) or harness.no_winner(w) for w in random_results)

    notes: list[str] = []
    top, count = random_results.most_common(1)[0]
    share = count / sum(random_results.values())
    if shared_outcome(defn) and (harness.no_winner(top) or NOBODY_WINS.search(str(top))):
        # a team target random play misses is what a target is for; only thinking play can show it is reachable
        notes.append(f"random teams end {top!r} in {share:.0%} of matches, as a shared target should; whether thinking play reaches it is for a model play-test")
    elif len(random_results) == 1:
        flags.append(f"every random match ended {top!r}: choices do not change the result")
    elif share > 0.9:
        flags.append(f"random seats end {top!r} in {share:.0%} of matches")

    dominance: dict[str, dict] = {}
    if not seat_named:
        flags.append("result names are not 'seat N', so dominance was not checked")
    else:
        for policy in ("first", "last"):
            for seat in range(1, min(n, 2) + 1):
                tally: Counter = Counter()
                for seed in seeds:
                    agents = harness.random_agents(n, seed)
                    agents[seat - 1] = harness.FixedAgent(harness.NAMES[seat - 1], policy)
                    w = harness.play(defn, agents, seed).result.winner
                    won = harness.winning_seats(w)
                    # a win shared at the top, or a match nobody won, counts as a draw: the policy did not beat the table
                    tally["win" if won == [seat] else "draw" if w == "draw" or seat in won or harness.no_winner(w) else "loss"] += 1
                decided = tally["win"] + tally["loss"]
                rate = tally["win"] / decided if decided else 0.0
                dominance[f"{policy}@seat{seat}"] = {"win": tally["win"], "loss": tally["loss"], "draw": tally["draw"], "win_rate": round(rate, 2)}
                if decided >= MIN_DECIDED and rate >= DOMINANCE:
                    flags.append(f"always taking the {policy} option as seat {seat} wins {rate:.0%} of decided matches against random seats")
    return {"flags": flags, "notes": notes, "random_results": dict(random_results), "dominance": dominance}
