"""How complex a game may be, for this platform to build and for models to play.

Two things bound a game. It must be simple enough for the encoder to build correctly (the
first redesign of the stag hunt, with a hidden world state, a private type, noisy signals
and chat every round, came out with every payoff at zero), and rich enough to be worth
training on. These limits are on the *variation*, before anything is built, so a design
that cannot be built is sent back to the designer and not discovered at the end.

The numbers come from the shipped games and from what the encoder has actually built: the
largest hand-written game has 10 to 22 steps a round (22 only because of a payoff-matrix
workaround), and the game the encoder built correctly had 12. Raise a limit when evidence
says the encoder can build more; do not raise it to make a game fit.
"""

from __future__ import annotations

from xcolos.games.definition import GameDefinition

#: What the designer reports about its variation, and the most each may be.
LIMITS = {
    "steps_per_round": 12,        # actions in one round: asks, polls, tells, updates, checks
    "choice_steps_per_round": 4,  # places a player must answer in one round
    "attributes": 20,             # player attributes plus table attributes
    "hidden_elements": 3,         # private types, hidden states and private signals, counted separately
    "random_draws_per_round": 1,  # chance events in one round (a deal, a state, a signal)
    "rounds": 15,
}
KEYS = tuple(LIMITS)


def problems(reported) -> list[str]:
    """What is wrong with a self-reported complexity: missing, not whole numbers, or over a limit."""
    if not isinstance(reported, dict):
        return ["complexity must be an object"]
    out = []
    for k in KEYS:
        v = reported.get(k)
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            out.append(f"complexity.{k} must be a whole number")
        elif v > LIMITS[k]:
            out.append(f"{k} is {v}, over the limit of {LIMITS[k]}")
    return out


def over(reported: dict) -> list[str]:
    """Only the limits exceeded, for sending back to the designer."""
    return [p for p in problems(reported) if "over the limit" in p]


def _walk(steps):
    for s in steps:
        yield s
        yield from _walk(getattr(s, "steps", ()) or ())


def measure(defn: GameDefinition) -> dict:
    """The same numbers, counted from the built game, so a report can show how far the
    design's claim was from the file."""
    steps = list(_walk(defn.steps))
    attrs = list(defn.player_attributes) + list(defn.game_attributes)
    return {
        "steps_per_round": len(steps),
        "choice_steps_per_round": sum(s.use in ("ask", "poll") for s in steps),
        "attributes": len(attrs),
        "hidden_elements": sum(getattr(a, "visible", "public") != "public" for a in attrs),
    }


def describe_limits() -> str:
    return "; ".join(f"{k} at most {v}" for k, v in LIMITS.items())
