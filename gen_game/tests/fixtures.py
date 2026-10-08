"""Shared fixtures for gen_game's tests.

Nothing here touches a model or the network. The shipped RPS game stands in for "the game the
pipeline produced", and a scripted completion plays every model: designer, critic, spec writer,
coder, test writer and triage, each answering by the system prompt it is sent.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from gen_game import adapt as adaptmod
from gen_game import complexity, critic, flow
from gen_inventory.inventory import Inventory
from gen_inventory.schema import from_dict
from xcolos.games import available

LIBRARY = Path(__file__).resolve().parents[2] / "xcolos" / "games" / "library"
RPS_TEXT = (LIBRARY / "rps.json").read_text()
RPS = available()["rps"]

SPEC = {
    "name": "Rock, Paper, Scissors", "summary": "ten rounds of hidden cards",
    "players": {"min": 2, "max": 2},
    "parameters": {"rounds": 10, "rock": 1, "paper": 2, "scissors": 3},
    "attributes": {"player": [{"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "points"}],
                   "game": [{"key": "rounds_left", "type": "number", "visible": "public", "initial": 10, "meaning": "rounds to go"}]},
    "setup": ["each player gets four of each card"],
    "round": [{"action": "ask", "who": "each player in turn", "answer": "a card from the hand", "effect": "the card leaves the hand"},
              {"action": "update", "who": "table", "answer": None, "effect": "the winner scores the card's value"}],
    "ending": {"condition": "rounds_left == 0", "results": ["seat 1", "seat 2", "draw"], "decided_by": "higher score"},
    "choices": [{"what": "twelve cards each", "why": "so ten rounds fit"}], "simplifications": [], "unsupported": [],
}
ALWAYS_ROCK = {"name": "everyone plays the same cards", "players": 2, "seed": 1,
               "moves": {"1": ["rock"] * 4 + ["paper"] * 4 + ["scissors"] * 2, "2": ["rock"] * 4 + ["paper"] * 4 + ["scissors"] * 2},
               "expect": {"result": "draw", "players": {"1": {"score": 0}, "2": {"score": 0}}, "game": {"rounds_left": 0}}}
SEAT1_WINS = {"name": "seat 1 plays scissors against paper", "players": 2, "seed": 1,
              "moves": {"1": ["scissors"] * 4 + ["rock"] * 4 + ["paper"] * 2, "2": ["paper"] * 4 + ["scissors"] * 4 + ["rock"] * 2},
              "expect": {"result": "seat 1", "players": {"1": {"score": 4 * 3 + 4 * 1 + 2 * 2}, "2": {"score": 0}}, "game": {"rounds_left": 0}}}


PLAN = {
    "original_summary": "Ten rounds of hidden cards.",
    "review": [{"criterion": c, "verdict": "good", "evidence": "tested by hand"} for c in adaptmod.CRITERIA],
    "problems": ["scoring is lopsided"],
    "changes": [{"what": "unequal card values", "why": "so the choice matters", "fixes": "scoring is lopsided"}],
    "keeps": ["hidden simultaneous cards"],
    "recommendation": {"decision": "adapt", "kind": "none", "reason": "worth adapting"},
    "complexity": {"steps_per_round": 6, "choice_steps_per_round": 2, "attributes": 8, "hidden_elements": 1,
                   "random_draws_per_round": 0, "rounds": 10},
    "variation": {"name": "Rock Paper Scissors, weighted", "summary": "ten rounds, unequal wins",
                  "players": {"min": 2, "max": 2},
                  "rules": "Two players each hold four rock, four paper and four scissors cards. Every round both play one card face down at "
                           "the same moment and then reveal. Rock beats scissors, scissors beats paper and paper beats rock. A win scores "
                           "the winning card's value: rock one, paper two, scissors three. A played card is spent. After ten rounds the "
                           "higher total score wins and equal totals are a draw.",
                  "objective": "higher total score after ten rounds wins; equal totals draw", "expected_effect": "choices carry risk"},
}


CRITIC_OK = {c: {"verdict": "pass", "evidence": "worked the table by hand"} for c in critic.CHECKS} | {"required_changes": []}


def critic_fails(*checks, change="make it fairer"):
    return {c: {"verdict": "fail" if c in checks else "pass", "evidence": f"{c}: the numbers say so"} for c in critic.CHECKS} | {"required_changes": [change]}


def triage_says(decision, guidance="do the thing", missing=""):
    return {"decision": decision, "reason": "the evidence points that way clearly", "guidance": "" if decision == "platform_limit" else guidance,
            "missing": missing}


class Models:
    """One scripted completion that answers each step by the system prompt it is sent."""

    def __init__(self, spec=SPEC, games=(RPS_TEXT,), scenario_lists=None, plans=None, critics=None, triages=None):
        self.critics = list(critics or [CRITIC_OK])
        self.triages = list(triages or [triage_says("revise_rules", "simplify the rules")])
        self.plans = list(plans or [PLAN])
        self.spec = spec
        self.games = list(games)
        self.scenario_lists = list(scenario_lists or [[ALWAYS_ROCK, SEAT1_WINS]])
        self.calls: list[str] = []
        self.prompts: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.prompts.append(prompt)
        if system.startswith("You are a game designer"):
            self.calls.append("adapt")
            return json.dumps(self.plans.pop(0) if len(self.plans) > 1 else self.plans[0])
        if system.startswith("You are a strict reviewer"):
            self.calls.append("critic")
            return json.dumps(self.critics.pop(0) if len(self.critics) > 1 else self.critics[0])
        if system.startswith("A game design for XColos"):
            self.calls.append("triage")
            return json.dumps(self.triages.pop(0) if len(self.triages) > 1 else self.triages[0])
        if system.startswith("You convert a game's rules"):
            self.calls.append("spec")
            return json.dumps(self.spec)
        if system.startswith("You write game files"):
            self.calls.append("encode")
            return self.games.pop(0) if len(self.games) > 1 else self.games[0]
        self.calls.append("scenarios")
        return json.dumps(self.scenario_lists.pop(0) if len(self.scenario_lists) > 1 else self.scenario_lists[0])


def run_flow(*a, steps=40, **k):
    """flow.convert with the design step off by default, and a step limit RPS fits under:
    the shipped RPS has 22 steps a round (a payoff-matrix workaround), which is over the real limit."""
    k.setdefault("adapt", False)
    saved = dict(complexity.LIMITS)
    complexity.LIMITS["steps_per_round"] = steps
    try:
        return flow.convert(*a, **k)
    finally:
        complexity.LIMITS.clear()
        complexity.LIMITS.update(saved)


def record(**over):
    base = dict(id="rps", name="Rock Paper Scissors", summary="cards", licence="original",
                rules_text="Two players each hold hidden cards. " * 12, source={"kind": "url", "url": "https://x.example"},
                players_min=2, players_max=2, turns="simultaneous", randomness="none", communication="public",
                ending="fixed_rounds", outcome="score", hidden=[], needs=["simultaneous_choice"], skills=["planning"],
                status="ready")
    base.update(over)
    return from_dict(base)


def world(**over):
    inv = Inventory(Path(tempfile.mkdtemp()) / "inv")
    inv.save(record(**over))
    return inv, Path(tempfile.mkdtemp())


# -- the harness -----------------------------------------------------------

