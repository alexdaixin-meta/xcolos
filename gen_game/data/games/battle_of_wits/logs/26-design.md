# 26 design

- time: 2026-10-07T00:22:17+00:00 (58.2s)  model: rl-muse-spark-1-2-playground
- system prompt: [system/c9011363-design.md](system/c9011363-design.md) (sha256 c9011363dbe8f358)
- sent sha256 0f44d7d41bcc2a50, reply sha256 833ecb768c05126f

## Sent

````
Original game: Battle of Wits
Players in the original: 2 to 2

Original rules:
The game is for two players: the Poisoner and the Chooser. Two identical goblets of wine are placed on the table. In secret, the Poisoner decides which goblet(s) contain poison - in the classic version, exactly one goblet is poisoned, though the story version allows both. The Chooser then studies the opponent and selects one goblet for himself; the remaining goblet goes to the Poisoner. Both players drink simultaneously. If the Chooser drank poison he dies and loses; if he drank the safe goblet, the Poisoner dies and loses. In a variant, the Poisoner may be immune and wins regardless, making the choice purely about deduction and bluffing about who would poison which glass.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Designer should simplify/re-balance: remove the High=3 vs Low=1 private-type multiplier and make any round win worth 1 point, or collapse scoring to a single fixed payoff matrix without type-dependence, and/or reduce to fewer rounds without alternating Poisoner/Chooser roles so arithmetic ranking can be implemented with simple calc instead of nested conditionals.
the game file could not be built. What the checks found on the attempts:
- attempt 1: it plays, but part of it does nothing: game attribute `last_chooser_points` is never changed in 3 random matches, so nothing updates it. Check that every answer the rules use is bound and then stored, and that every update runs.
- attempt 2: it plays, but part of it does nothing: game attribute `last_match` is never changed in 3 random matches, so nothing updates it; game attribute `last_poisoner_points` is never changed in 3 random matches, so nothing updates it. Check that every answer the rules use is bound and then stored, and that every update runs.
- attempt 3: it plays, but part of it does nothing: game attribute `last_match` is never changed in 3 random matches, so nothing updates it; game attribute `last_poisoner_points` is never changed in 3 random matches, so nothing updates it. Check that every answer the rules use is bound and then stored, and that every update runs.
- attempt 4: it plays, but part of it does nothing: game attribute `last_match` is never changed in 3 random matches, so nothing updates it; game attribute `last_poisoner_points` is never changed in 3 random matches, so nothing updates it. Check that every answer the rules use is bound and then stored, and that every update runs.
- attempt 5: it plays, but part of it does nothing: game attribute `last_match` is never changed in 3 random matches, so nothing updates it; game attribute `last_poisoner_points` is never changed in 3 random matches, so nothing updates it. Check that every answer the rules use is bound and then stored, and that every update runs.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Two-player asymmetric one-shot: Poisoner secretly poisons one (or both) goblets; Chooser picks one to drink; Chooser dies if poisoned, otherwise Poisoner dies. No repetition or scoring.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "One-shot zero-sum with fixed Poisoner/Chooser seats. No repeated play to learn or adapt. With variant 'Poisoner immune' Chooser choice is irrelevant (payoff independent of action). With standard win/lose only, any mixed strategy yields 50% - no action strictly dominates but seat is fixed and no simple policy can be punished over time because game ends after one decision. Always-pick-Left vs always-pick-Right are equally good (0.5 expected) - choices barely change outcome beyond coin flip."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Single simultaneous deduction with no signal, no history, no private type that changes optimal action. Outcome is pure matching-pennies guess. Better player cannot reliably beat worse one; variance dominates. Tested thoughtless policy: random Chooser wins 50% vs any Poisoner - luck swamps skill."
    },
    {
      "criterion": "headroom",
      "verdict": "bad",
      "evidence": "Solved: optimal is 50/50 randomization. No improvement path, no weak-player scoring - one win/loss, no cumulative total. Game is trivial once mixed strategy known, and hopeless to demonstrate growing skill."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Has hidden state (poison placement) requiring opponent modelling, but only one round and no private type/history, so inference is reduced to one-shot bluff without feedback or updating. Perfect-information after reveal but nothing to carry forward."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Win/loss follows deterministically from poison choice + drinking choice. No judge needed, purely arithmetic/boolean."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Text-only and could be turn-based (Poisoner then Chooser), but as a single round it is too short, not fixed-rounds repetition, and asymmetric fixed seats require workaround for balanced scoring. The previous variation attempted alternating roles with type-dependent 3/1 payoffs and nested conditional ranking, exceeding simple calc and leaving attributes never updated."
    }
  ],
  "problems": [
    "One-shot with fixed Poisoner/Chooser seats - no repetition, seat imbalance and no learning",
    "Private-type multiplier (High=3 vs Low=1) makes payoff depend on luck of dealt type, creating lottery where winner is decided by random type draw not play (lottery trap) and requires nested conditionals",
    "Per-role bonus attributes (last_poisoner_points, last_chooser_points, last_match) were bound but never stored/updated - build checks found them never changed in 3 random matches",
    "Alternating-role scoring with type-dependent matrix forced arithmetic_ranking via nested if-else (about 13+ steps for payoff matrix), exceeding simple build limits and causing silent no-ops",
    "Higher-total-wins on single zero-sum round collapses to coin flip - no sustained cooperation vs risk tension needed for reasoning"
  ],
  "changes": [
    {
      "what": "Replace one-shot with 8 fixed rounds, roles alternate each round (odd rounds P1=Poisoner, even rounds P2=Poisoner)",
      "why": "Provides repetition for inference/planning and balances asymmetric seats over match; ensures many observations of opponent's poison/choice patterns",
      "fixes": "One-shot with fixed Poisoner/Chooser seats - no repetition, seat imbalance and no learning"
    },
    {
      "what": "Remove private type and type-multiplier entirely; every round win = 1 point to round winner, nothing else",
      "why": "Eliminates lottery effect where High type auto-wins and removes type-dependent payoff branching; allows single fixed payoff (Chooser wins if picks safe, Poisoner wins if Chooser poisoned)",
      "fixes": "Private-type multiplier (High=3 vs Low=1) makes payoff depend on luck of dealt type, creating lottery where winner is decided by random type draw not play (lottery trap) and requires nested conditionals"
    },
    {
      "what": "Keep only two player total scores (Score_P1, Score_P2) and round counter; remove last_chooser_points, last_poisoner_points, last_match",
      "why": "Every attribute is now updated every round (winner +1), so no attribute remains unchanged - fixes dead-attribute build failure",
      "fixes": "Per-role bonus attributes (last_poisoner_points, last_chooser_points, last_match) were bound but never stored/updated - build checks found them never changed in 3 random matches"
    },
    {
      "what": "Collapse scoring to simple calc highest-total-wins; no payoff matrix or ranking table, just +1 to winner, compare totals at end",
      "why": "Removes need for nested conditional arithmetic_ranking/player_attribute_compare workaround; can be implemented with two increments and one final comparison, well within 12 steps/round",
      "fixes": "Alternating-role scoring with type-dependent matrix forced arithmetic_ranking via nested if-else (about 13+ steps for payoff matrix), exceeding simple build limits and causing silent no-ops"
    },
    {
      "what": "Define Poisoner must poison exactly one goblet (Left or Right), Chooser must drink exactly one; no 'both poisoned' or immunity variant",
      "why": "Keeps game recognizably Battle of Wits but gives deterministic zero-sum round that is balanced 50/50 under optimal play and has no unbeatable simple policy - must outguess opponent over 8 rounds",
      "fixes": "Higher-total-wins on single zero-sum round collapses to coin flip - no sustained cooperation vs risk tension needed for reasoning"
    }
  ],
  "keeps": [
    "Core bluffing/deduction: Poisoner secretly chooses poisoned goblet, Chooser chooses goblet to drink without seeing poison",
    "Simultaneous drinking reveal and zero-sum round resolution (Chooser safe => Chooser wins round, Chooser poisoned => Poisoner wins round)",
    "Identical goblets and hidden poison placement as sole hidden element"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": ""
  },
  "variation": {
    "name": "Battle of Wits - Alternating Goblets",
    "summary": "Two players alternate Poisoner/Chooser for 8 rounds. Each round Poisoner secretly poisons one goblet, Chooser picks one to drink. Round winner gets 1 point. Most points after 8 wins.",
    "players": {
      "min": 2,
      "max": 2
    },
    "rules": "Players: 2 (P1, P2). Rounds: 8 fixed. Roles: On odd rounds (1,3,5,7) P1 is Poisoner and P2 is Chooser; on even rounds (2,4,6,8) P2 is Poisoner and P1 is Chooser.\nSetup: Scores Score_P1=0, Score_P2=0. Each round labels goblets Left and Right.\nEach round in order:\n1. Poison step: The Poisoner privately chooses one goblet to poison: Left or Right. Exactly one must be poisoned. This choice is hidden from the Chooser.\n2. Choice step: The Chooser chooses one goblet to drink: Left or Right, without seeing the Poisoner's choice.\n3. Reveal step: Both choices are revealed to both players.\n4. Scoring step: If Chooser's choice equals Poisoner's choice (drank poison), Poisoner wins the round and gets 1 point (their Score +1). Otherwise (different goblets, drank safe), Chooser wins the round and gets 1 point (their Score +1). No other points are awarded. Ties within a round are impossible.\n5. Proceed to next round until round 8 finishes.\nAll choices are mandatory; there is no pass. No immunity, no both-poisoned option, no private type, no bonus points.",
    "objective": "After 8 rounds, player with higher total Score wins. If Score_P1 == Score_P2, the match is a draw. Winner is decided solely by arithmetic comparison of totals.",
    "expected_effect": "Removes lottery and complex branching while preserving hidden-information bluffing. Over 8 alternating rounds players must model opponent's pattern (e.g., tendency to switch, stick, or alternate) and randomize to avoid exploitation. No simple always-Left/always-Right policy can dominate because opponent can best-respond; skill is inference and unpredictability. Simple +1 scoring and only two total attributes guarantees every update runs and calc is trivial."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 5,
    "choice_steps_per_round": 2,
    "attributes": 3,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 8
  }
}
````
