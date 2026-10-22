"""Step 4: evaluate an encoded game.

Tiers. The pipeline checks two things: that the game runs, and that it plays the rules the design says.

  Tier 0, validity. Random seats play at the smallest and largest table; every
  match must end with a result and a valid log, no seat may be left unable to
  answer, and the same seed must replay to the same log.

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

from collections import Counter

from gen_game import harness
from xcolos.games.definition import GameDefinition

DOMINANCE = 0.85
MIN_DECIDED = 10


def not_run() -> dict:
    """The reasoning and balance checks, left out: the same shape, nothing flagged."""
    return {"flags": [], "random_results": {}, "dominance": {}, "skipped": True}


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
            if r.status != "ended" or not r.winner:
                problems.append(f"{n} players, seed {seed}: {r.status} ({r.reason}), result {r.winner!r}")
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
    seat_named = all(w is None or w == "draw" or w.startswith("seat ") for w in random_results)

    if len(random_results) == 1:
        flags.append(f"every random match ended {next(iter(random_results))!r}: choices do not change the result")
    top, count = random_results.most_common(1)[0]
    if len(random_results) > 1 and count / sum(random_results.values()) > 0.9:
        flags.append(f"random seats end {top!r} in {count / sum(random_results.values()):.0%} of matches")

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
                    tally["win" if w == f"seat {seat}" else "draw" if w == "draw" else "loss"] += 1
                decided = tally["win"] + tally["loss"]
                rate = tally["win"] / decided if decided else 0.0
                dominance[f"{policy}@seat{seat}"] = {"win": tally["win"], "loss": tally["loss"], "draw": tally["draw"], "win_rate": round(rate, 2)}
                if decided >= MIN_DECIDED and rate >= DOMINANCE:
                    flags.append(f"always taking the {policy} option as seat {seat} wins {rate:.0%} of decided matches against random seats")
    return {"flags": flags, "random_results": dict(random_results), "dominance": dominance}
