# 25 design

- time: 2026-10-27T09:09:30+00:00 (301.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 3d26e7905493ea22, reply sha256 4c09639918b62d38

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: DECK NUMBERS. 33 cards, values sum to 120 (Max→0 counts as 0). Card mean = 120/33 ≈ 3.64. E[x²] = 1520/33 ≈ 46.1, so card SD ≈ 5.7. Max→0 is dealt with probability about 4/33 ≈ 0.12 in a 4-player hand and cancels the highest other card (about 9 on average), costing about 1.1. Four-card true total: mean ≈ 13.4, SD ≈ 11. Three-card true total: mean ≈ 10.1, SD ≈ 9.5. Your uncertainty is your own card only: K + own, SD 5.7, while declarations must step by 3.

WHERE THE LOSS LANDS (4 players, F = 12, everyone playing sensibly). Each band is followed by its probability and the player who loses.
- Total < 12 (≈ 43%). The opener must declare at least 12, so the claim is already false. Turn 2 calls and wins, and the opener loses. Turn 2 cannot safely declare 15 either, because turn 3 would call.
- Total 12–14 (≈ 10%). Turn 2 is stuck: calling loses because true ≥ 12, and declaring 15 loses to turn 3's call. Turn 2 loses.
- Total 15–17 (≈ 10%). Turn 3 is stuck: calling loses because true ≥ 15, and declaring 18 loses to turn 4's call. Turn 3 loses.
- Total ≥ 18 (≈ 35%). Turn 3 must declare D3. Turn 4 calls if true < D3 and declares D3+3 if true ≥ D3+3. Turn 3 escapes only if true lands in [D3, D3+2]. The best 3-value own-card window, for example {1,2,3} or {3,4,5}, holds 12/33 ≈ 36%. So turn 3 loses about 60% of this band and turn 4 the rest.
- Approximate loss rates per hand: opener ≈ 0.43, turn 2 ≈ 0.12, turn 3 ≈ 0.31, turn 4 ≈ 0.14. A fair share is 0.25. The 3-player case is the same: F = 9 against a mean of ≈ 10.1, so P(total < F) ≈ 45% and the opener absorbs it.

SEAT EDGE AND SNOWBALL. R13 makes the loser the next opener. Losing a hand therefore puts you in the seat that loses about 43% of hands, and you lose about 1.7× as often as a fair share. Tokens snowball onto whoever lost first. This is a structural seat edge set by move order, not by play.

R9 ALSO PUNISHES A TRUE CLAIM. When turn 4 declares and true ≥ D4, the turn-3 player loses even though their own claim D3 < D4 was true. That is the source of turn 3's narrow escape window.

THOUGHTLESS POLICIES (none dominates, but this does not rescue the seat imbalance).
- Always call at turn 2: loses whenever true ≥ D1 = 12, ≈ 57% of hands.
- Always declare the minimum: at turn 4 it declares D3+3 ≥ 21 and loses when true < 21, ≈ 70%.
- Always call at turn 4: loses when true ≥ D3 ≥ 18, ≈ 35%.
- No option is strictly dominant, and both or all players can still win. The check fails on the opener and loser-opens edge.
- reasoning_over_luck FAILED: WHAT THERE IS TO INFER. There is real inference: others see your card, so their declarations leak information about it.

WHY CHANCE DOMINATES.
- With sensible play, the hand's loser is essentially fixed by which band the true total falls in, and that comes from the deal: <12 → opener; 12–14 → turn 2; 15–17 → turn 3.
- In the ≥18 band, turn 3 survives only if their unseen card lands in a 3-wide window (≤ 36%).
- Inside a band, the stuck player loses whatever they choose. Their remaining uncertainty is their own card, SD 5.7, against a step of 3.
- Skill matters only near band edges and in reading others' declarations. Those are only about 2 decisions per hand, with little room because the minimum step is 3 and there are only 4 turns.

ROUGH SHARE. About 60–70% of hand outcomes are fixed by the deal plus seat, not by decisions.

ALL-GOOD-PLAY TEST. When every player plays the intended strategy (declare the minimum when true is likely above it, call when it is likely below), the loser each hand is the player sitting at the band the deal produced. Because the loser then opens and the opener loses ≈ 43%, the first unlucky deal tends to cascade. A good reasoner is not clearly favoured over a mediocre one.
- change: Remove the forced opening floor: let the opener declare any whole number from −20 to 80, or set F = 0, so the opener is not pushed above the median total about 43% of the time.
- change: Replace 'loser opens' (R13) with a fixed rotation: the opener moves one surviving seat clockwise each hand. This removes the snowball onto the worst seat.
- change: Change the minimum raise from +3 to +1, so 'stuck' bands shrink to a single value and outcomes depend on judging the total, not on which 3-wide band the deal hit.
- change: Fix R9 so a true lower claim is not punished. If the turn-4 declaration is true (true ≥ D4), the player with the lowest declaration this hand loses only if it was also the furthest below the true total. Simpler: make turn 4 call-only, so every hand ends in an R8 call.
- change: Reduce own-card variance so reasoning outweighs the deal: remove the −10 and 20 and one 15, or tell each player privately one coarse fact about their own card (e.g. whether it is ≥ 3) as a single hidden element.
The variation that was reviewed: Coyote: Four Calls: R1 Setup. Seats are numbered 1 to N clockwise (N is 3 or 4). Every player starts with 0 tokens, opener_seat is 1 and hand_number is 1.

R2 Deck and deal. The deck has exactly 33 cards:
- one -10
- two -5
- three 0
- four each of 1, 2, 3, 4 and 5
- three 10
- two 15
- one 20
- one special card called Max→0
At the start of every hand the deck is restored to these 33 cards and shuffled. Each surviving player is dealt exactly 1 card. All dealt cards return to the deck at the end of the hand.

R3 Who sees what. Each player is privately told the card of every other surviving player, never their own.

R4 Turn order. Each hand has exactly 4 turns. Turn 1 is the player in opener_seat. Turns 2, 3 and 4 go to the next surviving players clockwise, wrapping around as needed. With 3 survivors the opener also takes turn 4. With 2 survivors the two players alternate: opener, other, opener, other.

R5 Turn 1 (opening). The opener declares a whole number from F to 80 inclusive, where F = 3 × (number of surviving players). That player becomes current_declarer and the number becomes current_declaration. previous_declarer is set to none.

R6 Turns 2 and 3. The player either declares a whole number at least current_declaration + 3 and at most 80, or calls Coyote. If current_declaration + 3 is more than 80, only calling is allowed.
- On a declaration, the old current_declarer becomes previous_declarer, the new player becomes current_declarer and the number becomes current_declaration.
- On a call, that player is the caller, the hand stops and goes to R8.

R7 Turn 4. The player either calls Coyote (go to R8 as caller) or declares a whole number at least current_declaration + 3 and at most 80. If current_declaration + 3 is more than 80, only calling is allowed. If they declare, the old current_declarer becomes previous_declarer, this player becomes current_declarer, and the hand goes to R9.

R8 Resolving a call. Compute the true total (R10).
- If the true total is less than current_declaration, the current_declarer loses the hand.
- Otherwise the caller loses the hand.

R9 Resolving the final declaration. Compute the true total (R10).
- If the true total is less than current_declaration, the current_declarer (the turn-4 player) loses the hand.
- Otherwise the previous_declarer loses the hand.

R10 True total. Reveal all cards to everyone.
- Add all card values, counting Max→0 as 0.
- If Max→0 was dealt, find the single highest-valued other dealt card. If its value is positive, subtract it from the sum, so that card counts as 0. If two or more cards tie for highest, only one of them is cancelled.

R11 Token. The loser gains 1 token. All cards, the true total and the loser are announced to everyone.

R12 Elimination. A player with 3 tokens is eliminated. They are dealt no further cards and are skipped in turn order.

R13 Next hand. The loser becomes opener_seat. If the loser was just eliminated, the next surviving player clockwise from them opens. hand_number increases by 1. Return to R2.

R14 End. The game ends when only one player remains. Each hand gives exactly one token, so a 4-player game lasts at most 11 hands and a 3-player game at most 8. Winner: The last player not eliminated wins. Every hand gives exactly one token to exactly one player, so the game always ends with a single winner and never in a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluff-and-deduction game. Each player wears a feather card they cannot see but everyone else can. Players take turns declaring ever-higher estimates of the total of all feathers, until someone calls 'Coyote'. If the true total is below the last declaration, the declarer takes a token; otherwise the caller does. Three tokens eliminate a player, and the last survivor wins. The previous variation capped each hand at 4 turns, used a 33-card deck, forced an opening floor of 3×players and a +3 minimum raise, and made the loser open the next hand.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "The previous variation has a structural seat edge. Testing gave these loss rates per hand: opener ≈ 0.43, turn 2 ≈ 0.12, turn 3 ≈ 0.31, turn 4 ≈ 0.14, against a fair share of 0.25. The opener is hurt by the forced floor F = 3N, which sits near the median total. Turn 3 is hurt because R9 punishes a true claim when turn 4 declares truthfully. 'Loser opens' then puts the last loser into the worst seat, so tokens snowball onto whoever lost first. No simple policy is unbeatable: always calling at turn 2 loses ≈57% and always raising the minimum at turn 4 loses ≈70%. The imbalance comes from move order, not play."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Under sensible play the loser is fixed by which band the true total falls in: below 12 the opener loses, 12–14 turn 2, 15–17 turn 3. Inside a band the stuck player loses whatever they choose, because their uncertainty is one card with SD 5.7 against a forced step of 3. About 60–70% of hand outcomes are set by the deal plus seat. The 4-turn cap stops the real Coyote contest of creeping toward the true total and judging when to stop."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Skill matters only near band edges, roughly 2 decisions per hand. Little can be learned beyond 'declare the minimum when likely true, call when likely false'. Weak players are not shut out, but strong players cannot pull away."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The hidden information is genuine: you see everyone's card but your own, and others' declarations leak information about yours. However, the +3 step, the 4-turn cap and the huge card spread (−10 to 20) leave too few turns for that leaked information to be used before the band decides the hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The true total, the comparison with the last declaration, the token and elimination are all arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based, text-only, has one hidden card per player and one shuffle per hand, and has no board. It fits the limits, though the 4-turn hand cap was a workaround that damaged the game."
    }
  ],
  "problems": [
    "P1: The forced opening floor (3 × players) sits near the median total, so the opener's claim is false about 43% of the time before anyone thinks.",
    "P2: 'Loser opens next hand' sends the loser into the worst seat, so tokens snowball onto the first unlucky player.",
    "P3: The 4-turn cap with a turn-4 showdown (R9) punishes a TRUE claim by turn 3 and puts the end-of-hand burden on fixed seats instead of on whoever misjudges the total.",
    "P4: The +3 minimum raise creates 3-wide 'stuck' bands in which the player to act loses whatever they choose.",
    "P5: Card variance is too high (SD ≈ 5.7, values −10 to 20). One unseen card swamps everything that can be inferred from others' declarations.",
    "P6: Too few decisions per hand. Reasoning acts on about 2 choices, so the deal decides most hands."
  ],
  "changes": [
    {
      "what": "Remove the hand turn cap. A hand passes around the table lap after lap, one lap per engine round, until someone calls Coyote. A new hand can begin only at the start of a round, and once Coyote is called the remaining turns of that round are skipped.",
      "why": "This restores real Coyote. Nobody is forced to end the hand by seat. The loss lands on whoever misjudges the total, or is caught when the declaration reaches it. It also keeps choice steps at no more than 4 per round and one deal per round.",
      "fixes": "P3"
    },
    {
      "what": "Abolish the R9 showdown. Every hand ends with a Coyote call: the declarer loses if the true total is below the declaration, otherwise the caller loses.",
      "why": "A true claim is never punished, so the only ways to lose are overclaiming or calling a true claim.",
      "fixes": "P3"
    },
    {
      "what": "The opener may declare any whole number from −3 to 20.",
      "why": "The floor of −3 is below almost every possible total, so the opener is no longer forced into a false claim. The opener chooses how aggressive to be.",
      "fixes": "P1"
    },
    {
      "what": "The opener rotates one surviving seat clockwise every hand, whoever lost.",
      "why": "Every player opens equally often and there is no snowball.",
      "fixes": "P2"
    },
    {
      "what": "The minimum raise is +1.",
      "why": "The 'stuck' situation shrinks to the single case where the declaration equals the true total exactly. Aiming at that exact value, and avoiding it, becomes the skill.",
      "fixes": "P4"
    },
    {
      "what": "Use a new 20-card deck: values −2 to 5 plus one Max→0. The card SD is about 2.0 and the 4-player total has mean ≈ 5.7.",
      "why": "Your own-card uncertainty (about ±4) becomes comparable to what others' declarations reveal. Inference can narrow it, and totals are small, so hands last 1–3 laps.",
      "fixes": "P5"
    },
    {
      "what": "Each hand has many +1-sized decisions near the true total, made over several laps, with the full declaration history visible.",
      "why": "Players can read jumps and hesitations, which carry information about their own card. They can jump to pin the next player or creep safely. This gives many reasoned decisions per hand.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Each player's own feather is hidden from them and visible to everyone else.",
    "Strictly increasing declarations of the total of all feathers, ended by a 'Coyote!' call.",
    "The liar-or-caller rule: the declarer loses if the total is below the declaration, otherwise the caller loses.",
    "The special Max→0 card that cancels the highest feather.",
    "Coyote tokens, elimination at 3 tokens, and last survivor wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of the game, inferring your own hidden card from what others see and how they declare, is excellent for training. The previous failures came from the turn cap, the opening floor, the step size and the deck, and all of these can be fixed inside the limits."
  },
  "variation": {
    "name": "Coyote: Around the Fire",
    "summary": "Each player sees every feather but their own. Declarations of the feather total climb by at least 1 around the table, lap after lap, until someone calls Coyote. A wrong declarer or a wrong caller takes a token. The opener rotates every hand, three tokens eliminate a player, and the last survivor wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "R1 Setup. Seats are numbered 1 to N clockwise (N is 3 or 4). Every player starts with 0 tokens and is alive. opener_seat = 1, hand_active = no, round = 1.\n\nR2 Deck. The deck has exactly 20 cards:\n- one −2\n- two −1\n- three 0\n- three 1\n- three 2\n- three 3\n- two 4\n- two 5\n- one special card, Max→0\n\nR3 Start of a round. If hand_active is no, a new hand begins:\n- The deck is restored to all 20 cards and shuffled.\n- Each alive player is dealt exactly 1 card face-down.\n- Each player is privately told the card of every other alive player, never their own.\n- current_declaration is set to none and hand_active to yes.\n- Everyone is told that a new hand begins and who opens it.\nIf hand_active is already yes, the hand in progress simply continues.\n\nR4 Turn order. In every round the alive players take exactly one turn each:\n- The first turn goes to the player in opener_seat, then each next alive player clockwise, so a round has as many turns as there are alive players (at most 4).\n- The order is the same in every round of a hand, so a hand passes around the table lap after lap.\n- If Coyote is called, the hand ends and any remaining turns of that round are skipped.\nBefore each turn, all players are shown the current declaration, who made it, and every declaration made so far this hand.\n\nR5 A turn.\n(a) If there is no declaration yet this hand, the player must declare a whole number from −3 to 20.\n(b) Otherwise the player either declares a whole number at least current_declaration + 1 and at most 20, or calls Coyote. If current_declaration is 20, the player must call Coyote.\n(c) A declaration makes that player the current declarer and the number the current declaration.\n\nR6 True total. All cards are revealed to everyone.\n- Add all card values, counting Max→0 as 0.\n- If Max→0 was dealt, the single highest other dealt card counts as 0 instead, provided its value is positive. If several cards tie for highest, only one of them is cancelled.\n\nR7 Resolving Coyote. Compute the true total.\n- If the true total is less than the current declaration, the current declarer loses the hand.\n- Otherwise the caller loses the hand.\nThe loser gains 1 token. All cards, the true total and the loser are announced to everyone. hand_active becomes no.\n\nR8 Elimination. A player with 3 tokens is eliminated. They receive no more cards and are skipped in turn order.\n\nR9 Next opener. After every hand, opener_seat moves to the next alive player clockwise from the current opener, whoever lost. If the current opener was just eliminated, it moves to the next alive player clockwise from their seat.\n\nR10 End. The game ends immediately when only one player is alive, and that player wins. If round 40 ends first, any unfinished hand is discarded without a token. The alive player with the fewest tokens then wins; if two or more alive players tie for fewest, the game is a draw.\n\nThere is no table talk: declarations and calls are the only communication.",
    "objective": "Be the last player not eliminated (3 tokens eliminate). If 40 rounds pass with more than one player alive, the alive player with the fewest tokens wins, and a tie for fewest is a draw.",
    "expected_effect": "Losses now fall on whoever misjudges the total, not on a seat. Every player opens equally often, a true claim is never punished, and the only 'stuck' case is the declaration equalling the total exactly.\n\nYour own card (SD ≈ 2) is the only unknown, and everyone else's jumps, creeps and calls are evidence about it. The reasoning in play includes:\n- inferring your own card from how far others dared to raise;\n- jumping to exactly the likely total so the next player is pinned;\n- creeping by +1 when unsure;\n- calling when the declarer has stretched past what the visible cards support;\n- opening with deliberately uninformative numbers so others learn less about their cards.\n\nSimple policies all lose:\n- Always calling loses to any true opening.\n- Always raising by +1 eventually overclaims and is called.\n- Always opening at 20 is called at once.\n\nLuck remains in which player is facing the declaration when it reaches the true total. However, with +1 steps, many laps and visible histories, accurate inference shifts that risk onto weaker estimators.\n\nTalk is left out. Only one player can win, so any message would be an unverifiable claim about another player's card, which careful players would ignore. Declarations already serve as the costly, informative signal."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
