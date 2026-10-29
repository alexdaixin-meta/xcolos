# 11 design

- time: 2026-10-28T05:24:56+00:00 (97.7s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e6d9154a2b739f71, reply sha256 febdd60ab3739090

## Sent

````
Original game: Button Men
Players in the original: 2 to 2

Original rules:
Each player picks a Button that lists its dice, e.g. 3d6 2d10. A match is best of five rounds. To start a round both players roll all their dice at once; rolls are public. Players alternate turns. On your turn you must make a capture if able: a power attack uses one die whose value is at least the value of one opposing die to capture it; a skill attack uses any number of your dice whose values sum exactly to the value of one opposing die to capture it. Special skills on some dice modify this, but share the same structure. Captured dice are set aside and all dice used in the attack are rerolled immediately. If you cannot capture you must pass. When one player has no dice left, the round ends. The player who captured dice with higher total face-count (sum of sides, not rolled values) wins the round, and first to win three rounds wins the match.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Cut the number of decisions per round to 4 or fewer.
- Replace the free four-value loading with a single choice from a small public menu of preset loadings that each total 16, for example 4/3/4/5, 1/6/5/4 and 2/3/4/7.
- Make the attack one choice from an enumerated list of legal attacks plus pass, rather than separate target, mode and attacker picks.

Then rebalance so no fixed or passive option dominates:
- Make failure less lopsided. For example, a failed attacking die is returned unchanged or simply rerolled rather than captured, or the defender gains only half its size.
- Or give the attacker a small reward for attempting, or a cost for passing, such as a pass forfeiting 1 point or a limited number of passes per leg.
- Make sure the menu order does not put a reliably safe option first.

Check that both an all-pass policy and an always-attack policy lose to sensible play from both seats.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 1 wins 92% of decided matches against random seats
- always taking the first option as seat 2 wins 93% of decided matches against random seats
- the built game has 5 choice steps per round, over the limit of 4
- against random seats the results were {'seat 2': 34, 'seat 1': 26}
- a thoughtless policy `first@seat1`: won 55, lost 5, drew 0
- a thoughtless policy `first@seat2`: won 55, lost 4, drew 1
- a thoughtless policy `last@seat1`: won 4, lost 52, drew 4
- a thoughtless policy `last@seat2`: won 9, lost 48, drew 3

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Button Men is a two-player dice duel. Each player rolls a set of dice of different sizes in public and captures opposing dice by power attacks (one die showing at least the target's value) or skill attacks (dice summing exactly to the target's value). Captured dice score their size, and the first player to win three rounds wins the match.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "Captures are forced whenever one is possible, so many turns have a single legal move. In the previous built variation, 'always the first option' won 55 of 60 matches from either seat, and 'always the last option' lost about 50 of 60. The fixed menu order decided the result, not the choices."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "With all rolls public and captures mandatory, skill lies only in picking which legal capture to make. The rerolls after each attack supply most of the variance."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The tactical depth is real but shallow per turn. A careful player gains a little by choosing captures that leave fewer counter-captures. A random player still captures often because capturing is compulsory."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "Every rolled value is public, so nothing about the present state needs to be inferred. The only unknown is future rerolls, which is pure chance. The opponent has no hidden type or hidden information to model."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Captures and scores follow by arithmetic from die values and die sizes."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and turn-based. However, enumerating legal skill attacks over subsets of dice, plus special skills, best-of-five legs and alternating turns, made the previous build use 5 choice steps per round, over the limit of 4."
    }
  ],
  "problems": [
    "All rolled values are public, so there is nothing to infer and the game fails reasoning_dependent.",
    "Mandatory capture leaves most turns with one or two forced moves, so choices barely matter.",
    "The previous variation's fixed option menu let 'always first' win about 92% and doomed 'always last'. Menu order, not play, decided matches.",
    "The previous build used 5 choice steps per round, over the limit of 4.",
    "Skill attacks need subset-sum enumeration and special die skills, both too costly to build.",
    "Alternating turns give a seat-order edge (seat 2 won 34 to 26 against random seats), and best-of-five legs multiply steps.",
    "Passing had no clear cost and failed attacks had lopsided costs in the previous variation, so passive or fixed policies could dominate."
  ],
  "changes": [
    {
      "what": "Each player's rolled values are private. The opponent sees only which dice remain and their sizes (d4, d8, d12).",
      "why": "Attacking becomes a judgement about an unseen value: how likely is a d8 to show at most what my d12 shows? Players must also track what earlier exchanges revealed.",
      "fixes": "All rolled values are public, so there is nothing to infer and the game fails reasoning_dependent."
    },
    {
      "what": "When an attack fails, both dice's current values are announced to both players. Those values stay true until the die is rerolled.",
      "why": "This creates an information economy. A failed probe tells you a target's exact value, but also exposes your weak attacker to a counter-attack. Players must remember values and plan around them.",
      "fixes": "All rolled values are public, so there is nothing to infer and the game fails reasoning_dependent."
    },
    {
      "what": "Capture is no longer mandatory. Each exchange, each player chooses one action from a fixed list of 12: reroll one of their own dice (3 options) or attack any opposing die with any of their dice (9 options).",
      "why": "Every exchange becomes a real decision between probing, attacking with a known-high die, or refreshing an exposed low die.",
      "fixes": "Mandatory capture leaves most turns with one or two forced moves, so choices barely matter."
    },
    {
      "what": "The menu is ordered so that neither end is safe. The first options are rerolls, which never score. The last option is d12 attacking d12, a coin flip that becomes a wasted turn once that target is gone. An action naming a captured die does nothing.",
      "why": "Repeating the first option never captures. Repeating the last option captures at most one die and then idles while being attacked. Both lose to sensible play.",
      "fixes": "The previous variation's fixed option menu let 'always first' win about 92% and doomed 'always last'. Menu order, not play, decided matches."
    },
    {
      "what": "Both players choose at the same moment, in a single simultaneous poll per exchange. All attacks resolve on the values shown before the exchange.",
      "why": "This removes the seat-order edge and brings the round to 1 choice step.",
      "fixes": "The previous build used 5 choice steps per round, over the limit of 4."
    },
    {
      "what": "Only power attacks are kept, with ties going to the attacker. Skill attacks and special skills are dropped.",
      "why": "Power attacks keep the core capture-by-value mechanic and stay buildable in a handful of arithmetic steps.",
      "fixes": "Skill attacks need subset-sum enumeration and special die skills, both too costly to build."
    },
    {
      "what": "The match is a single duel of at most 12 exchanges instead of best of five legs.",
      "why": "This keeps the length short and the step count small. There is no seat order because play is simultaneous.",
      "fixes": "Alternating turns give a seat-order edge (seat 2 won 34 to 26 against random seats), and best-of-five legs multiply steps."
    },
    {
      "what": "A failed attack gives the defender 2 points. A reroll costs one exchange of tempo but hides an exposed value. Each player's surviving dice score half their size at the end.",
      "why": "Failure is costly but not crippling, so attacking is not reckless. Passivity has a real cost because the opponent captures freely while you score at most half of your own dice.",
      "fixes": "Passing had no clear cost and failed attacks had lopsided costs in the previous variation, so passive or fixed policies could dominate."
    }
  ],
  "keeps": [
    "Dice of different sizes, where size is what a capture is worth and rolled value is what decides a capture.",
    "The power attack: a die captures an opposing die if its value is at least the target's value.",
    "Attacking dice are rerolled after a successful capture.",
    "Captured dice score their full size, and surviving dice score half their size, as in Button Men's standard scoring.",
    "A two-player head-to-head duel."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Hiding rolled values and revealing them only through failed attacks gives the dice duel a real inference core. A single simultaneous 12-option choice per exchange fits the limits and removes the menu-order and seat biases that broke the previous build."
  },
  "variation": {
    "name": "Button Men: Blind Dice",
    "summary": "Two players each hold a hidden-value d4, d8 and d12. Over up to 12 simultaneous exchanges, each player either attacks an opposing die with one of their own, capturing it if their value is at least the target's, or rerolls one of their own dice. Failed attacks expose both dice's values, so players probe, remember and exploit what they learn.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "SETUP. Each player has three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). At the start, each player's three dice are rolled. Each player sees their own values; neither sees the opponent's. Both players can always see which dice each player still has and their sizes. Both scores start at 0.\n\nEXCHANGES. The match has up to 12 exchanges. Each exchange runs as follows.\n\n1. Announcement. The exchange number, both scores, and the dice each player still holds are announced to both players. Each player is privately reminded of the current values of their own remaining dice.\n\n2. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one action from this list:\n(1) Reroll my d4\n(2) Reroll my d8\n(3) Reroll my d12\n(4) My d4 attacks their d4\n(5) My d4 attacks their d8\n(6) My d4 attacks their d12\n(7) My d8 attacks their d4\n(8) My d8 attacks their d8\n(9) My d8 attacks their d12\n(10) My d12 attacks their d4\n(11) My d12 attacks their d8\n(12) My d12 attacks their d12\nAn action that names a die that has already been captured, whether your own or the opponent's, does nothing that exchange.\n\n3. Resolution. Both attacks are resolved using the values the dice showed at the start of the exchange, so the order does not matter.\n- An attack succeeds if the attacking die's value is greater than or equal to the target die's value. The attacker scores points equal to the target's size, and the target is captured and removed.\n- An attack fails if the attacking die's value is lower than the target's. The defender scores 2 points, and the current values of both dice are announced to both players.\n- A die may capture and be captured in the same exchange; both effects happen. If both attacks fail, both pairs of values are announced.\n\n4. Rerolls. After resolution, these dice are rerolled together, with new values shown only to their owner:\n- every attacking die whose attack succeeded and that was not itself captured this exchange;\n- every die its owner chose to reroll, if it was not captured this exchange.\nA die that was not rerolled keeps its value, including any value already announced.\n\n5. Results. Every attack and reroll action is announced, along with whether each attack succeeded or failed, any revealed values, which dice were captured, and the new scores. New rolled values are not announced.\n\n6. End check. The match ends immediately if either player has no dice left. Otherwise it ends after exchange 12.\n\nEND OF MATCH. Each player adds half the size of each of their own surviving dice to their score: d4 adds 2, d8 adds 4, d12 adds 6.",
    "objective": "After surviving-dice points are added, the player with the higher score wins. Equal scores are a draw.",
    "expected_effect": "Play shifts from forced captures to judgement under hidden information. Blind attacks rest on die-size odds: a d12 attacking a d4 succeeds about 79% of the time, a d4 attacking a d12 about 21%. Failed probes reveal exact values that persist until rerolled, so players must track which opposing dice are known-high or known-low. They must weigh tempo-costing rerolls against exposed weaknesses, and anticipate where the opponent will strike: a revealed low d12 is a 12-point target. The simplest fixed policies all lose to sensible play from either seat. Always choosing option 1 never captures and scores only failure points and survivors. Always choosing option 12 captures at most the opposing d12, then wastes every remaining exchange while being attacked. Simultaneous choice removes the seat edge. Dice luck stays real but is spread over up to 12 exchanges in which reading revealed values and the opponent's likely target matters."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 1,
    "attributes": 10,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
