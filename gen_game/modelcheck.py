"""Do the rules make sense? Play them, with numbers, before anything is built.

A critic reading a payoff table is an opinion, and one let through a design in which "always Defect" won 71% of games and
the winner under good play was a coin toss. So for the large family of games this fits (every round all players choose at
the same moment from the same actions, and a payoff depends on your action, your private type and how many players chose
each action) the designer gives a small MODEL of the rules, and this module plays it:

    {"players": 3, "rounds": 8, "actions": ["C", "D"],
     "types": {"values": ["High", "Low"], "probs": [0.5, 0.5]},          # or null
     "payoff": "(6 if type == 'High' else 5) if action == 'C' and n_C == 3 else ... ",
     "winner": {"kind": "highest_total"}}                                  # or {"kind": "target", "target": 40}

The payoff is one expression over `action`, `type`, `round`, `n_<A>` (how many players, you included, chose action A) and
`o_<A>` (how many others did). It is evaluated with a small whitelist, never `eval` on anything else.

Every simple policy (each action always; each mapping from type to action; random) is played against opponents who play at
random, who each pick a policy, and who all play one policy; and the best symmetric profile is played against itself. What is
reported is what a designer needs to fix the rules, in numbers, and none of it is judgment:

  * a policy that NEVER LOSES, whatever the opponents do
  * a policy that wins most games against random play, with a policy that uses your type doing no better
  * a winner under the intended good play that is decided by the random draw (a lottery)

Games that do not fit (sequential moves, bidding, private hands) give `model: null` and are not simulated here; the built
game is still tested by the platform's own tier 1.
"""

from __future__ import annotations

import ast
import itertools
import random
from dataclasses import dataclass, field

SAFE_NODES = (ast.Expression, ast.IfExp, ast.BoolOp, ast.And, ast.Or, ast.Not, ast.UnaryOp, ast.USub, ast.UAdd, ast.BinOp, ast.Add, ast.Sub,
              ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn,
              ast.Name, ast.Load, ast.Constant, ast.Call, ast.Tuple, ast.List)
FUNCTIONS = {"min": min, "max": max, "abs": abs}
MATCHES = 1200
LOTTERY = 0.5          # more of the games than this are decided by the draw under good play: a lottery
BEST_VS_RANDOM = 0.6   # a policy that wins this much of the time against random play is too good for being simple
NEVER_LOSES_MIN_WIN = 0.0


class ModelError(ValueError):
    pass


def compile_payoff(expr: str):
    """The payoff expression, checked against a whitelist and compiled."""
    try:
        tree = ast.parse(expr.strip(), mode="eval")
    except SyntaxError as exc:
        raise ModelError(f"payoff is not a valid expression: {exc.msg}") from None
    for node in ast.walk(tree):
        if not isinstance(node, SAFE_NODES):
            raise ModelError(f"payoff may only use arithmetic, comparisons, `if else`, and min/max/abs; found {type(node).__name__}")
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS):
            raise ModelError("payoff may only call min, max and abs")
    return compile(tree, "<payoff>", "eval")


def problems(model) -> list[str]:
    """What is wrong with a model, in words a designer can act on. [] when it can be played."""
    if model is None:
        return []
    if not isinstance(model, dict):
        return ["model must be an object, or null when the game does not fit"]
    out = []
    n, rounds, actions = model.get("players"), model.get("rounds"), model.get("actions")
    if not (isinstance(n, int) and not isinstance(n, bool) and 2 <= n <= 8):
        out.append("model.players must be a whole number from 2 to 8")
    if not (isinstance(rounds, int) and not isinstance(rounds, bool) and 1 <= rounds <= 30):
        out.append("model.rounds must be a whole number from 1 to 30")
    if not (isinstance(actions, list) and 2 <= len(actions) <= 5 and all(isinstance(a, str) and a.isidentifier() for a in actions) and len(set(actions)) == len(actions)):
        out.append("model.actions must be 2 to 5 different names made of letters, digits and underscores, like [\"C\", \"D\"]")
    types = model.get("types")
    if types is not None:
        vals, probs = (types or {}).get("values"), (types or {}).get("probs")
        if not (isinstance(vals, list) and 2 <= len(vals) <= 4 and all(isinstance(v, str) for v in vals) and isinstance(probs, list)
                and len(probs) == len(vals) and all(isinstance(p, (int, float)) and p >= 0 for p in probs) and abs(sum(probs) - 1) < 1e-6):
            out.append("model.types must be null or {\"values\": [2 to 4 names], \"probs\": [one probability each, adding to 1]}")
    winner = model.get("winner")
    if not (isinstance(winner, dict) and (winner.get("kind") == "highest_total" or (winner.get("kind") == "target" and isinstance(winner.get("target"), (int, float))))):
        out.append("model.winner must be {\"kind\": \"highest_total\"} or {\"kind\": \"target\", \"target\": a number}")
    if out:
        return out
    try:
        code = compile_payoff(str(model.get("payoff", "")))
    except ModelError as exc:
        return [str(exc)]
    # every situation the payoff can meet must give a number
    for t in (types["values"] if types else [""]):
        for a in actions:
            for counts in itertools.product(range(n + 1), repeat=len(actions)):
                if sum(counts) != n or counts[actions.index(a)] < 1:
                    continue
                try:
                    v = _payoff(code, actions, a, t, counts, 1)
                except Exception as exc:  # noqa: BLE001 - reported as the designer's expression being wrong
                    return [f"payoff failed for action={a!r} type={t!r} counts={dict(zip(actions, counts))}: {type(exc).__name__}: {exc}"]
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    return [f"payoff gave {v!r}, not a number, for action={a!r} type={t!r} counts={dict(zip(actions, counts))}"]
    return []


def _payoff(code, actions, action, type_, counts, rnd) -> float:
    ctx = {"action": action, "type": type_, "round": rnd}
    for a, c in zip(actions, counts):
        ctx[f"n_{a}"] = c
        ctx[f"o_{a}"] = c - (1 if a == action else 0)
    return eval(code, {"__builtins__": {}, **FUNCTIONS}, ctx)  # noqa: S307 - whitelisted AST, no builtins


@dataclass
class Policy:
    name: str
    #: action by type name; None means random each round
    by_type: dict | None


def policies(model) -> list[Policy]:
    actions = model["actions"]
    vals = model["types"]["values"] if model.get("types") else [""]
    out = [Policy("random", None)]
    if len(vals) == 1:
        out += [Policy(f"always {a}", {"": a}) for a in actions]
    else:
        for combo in itertools.product(actions, repeat=len(vals)):
            uniform = len(set(combo)) == 1
            out.append(Policy(f"always {combo[0]}" if uniform else "if " + ", ".join(f"{v}->{a}" for v, a in zip(vals, combo)), dict(zip(vals, combo))))
    return out


def _play(model, code, mine: Policy, opponents, rng: random.Random):
    """One match; seat 0 plays `mine`. `opponents` is 'random', 'mix' or a Policy all opponents play. Returns (totals, types)."""
    n, rounds, actions = model["players"], model["rounds"], model["actions"]
    tv = model["types"]
    types = [rng.choices(tv["values"], tv["probs"])[0] if tv else "" for _ in range(n)]
    pols = [mine]
    for _ in range(n - 1):
        pols.append(opponents if isinstance(opponents, Policy) else (policies_all[id(model)][rng.randrange(len(policies_all[id(model)]))] if opponents == "mix" else Policy("random", None)))
    totals = [0.0] * n
    for r in range(1, rounds + 1):
        chosen = [rng.choice(actions) if p.by_type is None else p.by_type[types[i]] for i, p in enumerate(pols)]
        counts = [chosen.count(a) for a in actions]
        for i in range(n):
            totals[i] += _payoff(code, actions, chosen[i], types[i], counts, r)
    return totals, types


policies_all: dict[int, list[Policy]] = {}


def _outcome(model, totals, seat=0) -> str:
    w = model["winner"]
    if w["kind"] == "highest_total":
        top = max(totals)
        winners = [i for i, t in enumerate(totals) if t == top]
    else:
        winners = [i for i, t in enumerate(totals) if t >= w["target"]]
        if not winners:
            return "draw"
    if len(winners) == len(totals):
        return "draw"
    if seat in winners:
        return "win" if len(winners) == 1 else "draw"
    return "loss"


@dataclass
class Result:
    flags: list[str] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)
    good_play: dict = field(default_factory=dict)

    def text(self) -> str:
        lines = [f"- {f}" for f in self.flags]
        lines.append("- numbers (seat 1's policy, outcome against random opponents): " +
                     "; ".join(f"{r['policy']}: win {r['random']['win']:.0%} draw {r['random']['draw']:.0%} loss {r['random']['loss']:.0%}" for r in self.rows))
        if self.good_play:
            g = self.good_play
            lines.append(f"- everyone playing '{g['policy']}' (best joint play): mean total {g['mean_total']:.1f}; every player tied in {g['all_tie']:.0%} of games, "
                         f"so {1 - g['all_tie']:.0%} are decided by the draw")
        return "\n".join(lines)


def simulate(model, matches: int = MATCHES, seed: int = 1) -> Result:
    """Play every simple policy through the model and report what is wrong with the rules, in numbers."""
    assert not problems(model), problems(model)
    code = compile_payoff(model["payoff"])
    rng = random.Random(seed)
    pols = policies(model)
    policies_all[id(model)] = [p for p in pols if p.by_type is not None]
    res = Result()

    def rates(mine, opponents, n):
        c = {"win": 0, "draw": 0, "loss": 0}
        for _ in range(n):
            totals, _types = _play(model, code, mine, opponents, rng)
            c[_outcome(model, totals)] += 1
        return {k: v / n for k, v in c.items()}

    never_loses: list[str] = []
    for p in pols:
        vs_random = rates(p, "random", matches)
        row = {"policy": p.name, "random": vs_random}
        if p.by_type is not None:
            small = max(200, matches // 5)
            profiles = {"mix": rates(p, "mix", small)} | {f"all {q.name}": rates(p, q, small) for q in pols if q.by_type is not None} | {"random": vs_random}
            row["worst_loss"] = max(v["loss"] for v in profiles.values())
            row["wins_somewhere"] = any(v["win"] > 0 for v in profiles.values())
            if row["worst_loss"] == 0 and row["wins_somewhere"]:
                never_loses.append(p.name)
        res.rows.append(row)
    for name in never_loses:
        res.flags.append(f"the policy '{name}' never loses: against random play, against any mix of policies and against every single opponent policy it never finishes behind. Something that simple should be able to lose.")

    best = max(res.rows, key=lambda r: r["random"]["win"] - r["random"]["loss"])
    if best["policy"] != "random" and best["random"]["win"] >= BEST_VS_RANDOM:
        res.flags.append(f"the policy '{best['policy']}' wins {best['random']['win']:.0%} of games against random opponents and loses {best['random']['loss']:.0%}: the simple policy is too good")
    if model.get("types"):
        typed = [r for r in res.rows if r["policy"].startswith("if ")]
        flat = [r for r in res.rows if r["policy"].startswith("always ")]
        if typed and flat:
            bt, bf = max(typed, key=lambda r: r["random"]["win"] - r["random"]["loss"]), max(flat, key=lambda r: r["random"]["win"] - r["random"]["loss"])
            if (bt["random"]["win"] - bt["random"]["loss"]) <= (bf["random"]["win"] - bf["random"]["loss"]) + 0.02:
                res.flags.append(f"knowing your type does not pay: the best policy that uses it ('{bt['policy']}', wins {bt['random']['win']:.0%}, loses {bt['random']['loss']:.0%}) "
                                 f"does no better than the best that ignores it ('{bf['policy']}', wins {bf['random']['win']:.0%}, loses {bf['random']['loss']:.0%})")

    # the best joint play, everyone the same: is the winner then decided by the draw?
    n = model["players"]
    best_joint, best_mean = None, None
    for q in [p for p in pols if p.by_type is not None]:
        total = 0.0
        for _ in range(200):
            t, _ = _play_all_same(model, code, q, rng)
            total += sum(t) / n
        if best_mean is None or total > best_mean:
            best_joint, best_mean = q, total
    ties = 0
    for _ in range(matches):
        t, _ = _play_all_same(model, code, best_joint, rng)
        ties += _outcome(model, t) == "draw" and len(set(t)) == 1
    res.good_play = {"policy": best_joint.name, "mean_total": best_mean / 200, "all_tie": ties / matches}
    if 1 - res.good_play["all_tie"] > LOTTERY:
        res.flags.append(f"when everyone plays the best joint policy ('{best_joint.name}'), {1 - res.good_play['all_tie']:.0%} of games are decided by the random draw "
                         "(someone finishes ahead only because of a hidden type or deal): reasoning does not decide the winner")
    return res


def _play_all_same(model, code, policy: Policy, rng):
    n, rounds, actions = model["players"], model["rounds"], model["actions"]
    tv = model["types"]
    types = [rng.choices(tv["values"], tv["probs"])[0] if tv else "" for _ in range(n)]
    totals = [0.0] * n
    for r in range(1, rounds + 1):
        chosen = [policy.by_type[types[i]] for i in range(n)]
        counts = [chosen.count(a) for a in actions]
        for i in range(n):
            totals[i] += _payoff(code, actions, chosen[i], types[i], counts, r)
    return totals, types
