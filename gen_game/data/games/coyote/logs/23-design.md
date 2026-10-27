# 23 design

- time: 2026-10-27T09:05:58+00:00 (86.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a4eeac5c583c5016, reply sha256 4784dc7172bfe1a6

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: Deck check: -10 + 2(-5) + 3(0) + 4(1+2+3+4+5) + 3(10) + 2(15) + 20 + Max->0 = 33 cards with total value 120, so the mean card is about 3.6. The lowest possible true total with 5 cards is -10-5-5+0+0 = -20, and with fewer cards it is higher. Any declaration of -21 or less is therefore always true. Opener declarations go down to -30.

Thoughtless policy 'always declare the minimum legal number (current+1)':
- Opener declares -30.
- R1 declares -29.
- R2 declares -28.
- R3 is forced by R5 to call_coyote. The true total is at least -20, which is at least -28, so the caller loses.

Winner-rule table for one hand, with the policy holder in the first or second response:
- If the opponent raises after them, they are no longer current declarer and cannot lose.
- If the opponent calls after their declaration of -21 or less, the caller loses.
- If the third responder is forced to call, the third responder loses.
- Result: the policy NEVER loses a hand from the R1 or R2 seat, whatever anyone else does.
The opener declaring -30 also never loses: a caller loses, and a raiser takes over as declarer.

The only player who can lose is the forced third responder, and they lose with certainty. The hand loser is fixed by seat:
- 3 survivors: the responders are 2, 3, then the opener, so the opener loses. The loser re-opens (R9), loses again, and is eliminated after 3 hands.
- 2 survivors: the order is A then B, A, B, so B loses. B re-opens, then A loses. The tokens simply alternate.
- 4-5 survivors: seat opener+3 loses every hand, a deterministic rotation.

No one ever has a reason to bid high, so the cards are irrelevant. Seat position decides everything. A strictly safe option exists, so the game fails.
- reasoning_over_luck FAILED: Under the intended good strategy, every R1, R2 and opener player declares -21 or less, which can never be false. The third responder loses with certainty. The loser of every hand is therefore fixed by seating and the R9 opener rule:
- Cards play no role.
- There is nothing to infer about one's own card.
- There is no opponent to model, since no declaration ever approaches the true total.

Chance share is about 0%, and reasoning share is about 0%. The outcome is mechanical from turn order. The original game's core inference (estimating your unseen card from the visible sum, about V + 3.6, and judging whether a bid near the true total is a bluff) is never exercised. A good reasoner is not favoured over a minimum-bidder; both get identical results.
- change: Remove the forced call. The third responder must choose between call_coyote and declaring a higher number. If they declare, the hand resolves immediately with the opener as caller, so the last declarer is exposed to a check. This stays within 4 choice steps.
- change: Add a floor so declarations must reflect the cards. The opener must declare at least the sum of the cards they can see (the game knows this number). Every raise must be at least 3 higher than current_declaration. After three raises the declaration then typically exceeds the true total (visible sum plus about 3.6), so calling becomes a live, inference-driven choice and no 'always safe' bid exists.
- change: Alternatively, raise the opener minimum to at least 0 and the minimum raise to 4. This removes the guaranteed-true region below -20.
- change: With 5 survivors, state explicitly that the seat before the opener sits out. Or rotate which responders act, so that every player bids over the game and seat position gives no systematic edge.
- change: Re-check with the new rules that no policy among always-minimum, always-call or always-maximum avoids losing against both sensible and random play.
The variation that was reviewed: Coyote: Short Count: R1 Setup. At the start of the game every player has 0 tokens, hand_number is 1 and opener_seat is 1. Seats are numbered 1 to N clockwise.

R2 The deck and the deal. The deck has exactly 33 cards: one -10, two -5, three 0, four each of 1, 2, 3, 4 and 5, three 10, two 15, one 20, and one special card called Max→0. At the start of every hand the deck is rebuilt to these 33 cards and shuffled. Each surviving player is then dealt exactly 1 card, which is removed from the deck for the rest of the hand. When the hand ends, all dealt cards go back to the deck, so between hands the deck always holds all 33 cards. Dealing is correct when every surviving player holds exactly one card and the hand's true total and token outcome agree with those cards. The deck size after a finished hand is not a measure of dealing.

R3 Who sees what. Each player is privately told the card of every other surviving player, but never their own card.

R4 Opening. The player in opener_seat declares a whole number from -30 to 60, inclusive. That player becomes current_declarer, and the number becomes current_declaration.

R5 Responses. The surviving players after the opener, going clockwise and wrapping past the opener if there are fewer than four survivors, make up to three responses in turn.
- First response and second response: the responder either declares a whole number strictly higher than current_declaration and at most 60, or chooses call_coyote. There is no option named 'raise'. Raising simply means choosing a number. A responder who declares becomes current_declarer, and the number becomes current_declaration. If current_declaration is 60, the responder is offered only call_coyote.
- Third response: if no one has called yet, the third responder must choose call_coyote; it is their only option.
As soon as anyone calls, that player is the caller, bidding stops, and the hand is resolved.

R6 True total. All cards are revealed to everyone. The true total is computed in two steps. First, add up the values of all cards, counting Max→0 as 0. Second, if Max→0 is among the dealt cards, find the single highest-valued other card. If its value is positive, subtract its value from the sum, so that card counts as 0. If two or more cards tie for highest, only one of them is cancelled.

R7 The loser. If the true total is less than current_declaration, the current_declarer loses the hand. Otherwise, when the true total is equal to or greater than current_declaration, the caller loses the hand. The loser gains 1 token. The dealt cards and the true total are announced to everyone.

R8 Elimination. A player who reaches 3 tokens is eliminated. They take no further part, are dealt no cards and are skipped in the bidding order.

R9 Next hand. The loser of the hand becomes opener_seat for the next hand. If the loser has just been eliminated, the next surviving player clockwise from them opens instead. hand_number increases by 1, and the next hand begins with R2.

R10 End. The game ends as soon as only one player is not eliminated. Each hand produces exactly one token, so with N players the game lasts at most 3(N-1)+2 hands, which is 14 hands for 5 players. Winner: The last player not eliminated wins. Every hand gives exactly one token to exactly one player, so the game always ends with a single winner and never in a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluffing and estimation game. Each player sees every feather but their own, players take turns declaring ever-higher claims about the total of all feathers, and anyone may call 'Coyote' to challenge. Whoever is wrong takes a token, and three tokens eliminate a player.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original, open-ended bidding gives every player a real choice between raising and calling. The previous variation broke this in two ways. Declarations of -21 or less were always true. The third responder was forced to call. So 'always declare current+1' never lost from the opener, R1 or R2 seats, and the loser of every hand was fixed by seat order."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The original rewards estimating your own card from the visible sum and reading others' bids. In the previous variation, seat position decided every hand, so a reasoner and a minimum-bidder got identical results."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Simple play is available in the original: estimate the visible sum plus the average card. Deeper play exists on top of it: infer your own card from what others' bids reveal, bluff, and time calls so the loss lands on a rival. Weak players can still survive several hands."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player is missing exactly one piece of information, their own card. Opponents' declarations leak what they see, so careful players can narrow down their own card. This was lost in the previous variation, where no bid ever approached the true total."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The true total, the comparison with the last declaration and the token count are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original's open-ended clockwise bidding has no step limit, and its five blue special cards (draw from deck, discard, flip, double, reshuffle) make long rule chains. A capped number of turns and a single special card fit the engine."
    }
  ],
  "problems": [
    "P1: A guaranteed-true region existed: any declaration below the lowest possible total (-20) could never lose, so minimum bidding was strictly safe.",
    "P2: The third responder was forced to call, so the hand's loser was fixed by seat order, not by judgement.",
    "P3: Nothing pushed declarations near the true total, so the cards and the core inference (own card is about visible sum plus 3.6) were never used.",
    "P4: With 5 survivors some seats never bid in a hand, and responder positions gave systematic risk differences.",
    "P5: The original's open-ended bidding and five chained special cards exceed the engine's step and choice limits."
  ],
  "changes": [
    {
      "what": "The opener must declare at least 3 times the number of surviving players. This is close to the expected total, since the mean card is about 3.6 and Max→0 lowers it.",
      "why": "A floor near the mean means the opening claim is false a substantial share of the time. No safe low bid exists, and the opener must judge from the cards they see whether the floor is risky.",
      "fixes": "P1: A guaranteed-true region existed: any declaration below the lowest possible total (-20) could never lose, so minimum bidding was strictly safe."
    },
    {
      "what": "Every raise must be at least 3 above the current declaration. The maximum declaration is 80.",
      "why": "After a few raises the claim usually exceeds the true total, so calling becomes a live choice that depends on inference.",
      "fixes": "P3: Nothing pushed declarations near the true total, so the cards and the core inference (own card is about visible sum plus 3.6) were never used."
    },
    {
      "what": "The forced call is removed. The fourth turn (the third responder) may call or declare. If they declare, the hand resolves at once: if the true total is below that final declaration, the final declarer loses; otherwise the player who made the declaration just before it loses (they were outbid by a true claim).",
      "why": "Every turn becomes a real decision. The last responder weighs 'the current claim is false' (call) against 'a claim 3 or more higher is true' (declare and dump the loss on the previous declarer). The second responder must foresee this.",
      "fixes": "P2: The third responder was forced to call, so the hand's loser was fixed by seat order, not by judgement."
    },
    {
      "what": "Player count is limited to 3–4. Every hand has exactly 4 turns, wrapping around the table when fewer than 4 players survive. The loser opens the next hand.",
      "why": "No seat ever sits out. The order relative to the loser keeps shifting, so no seat keeps a fixed role.",
      "fixes": "P4: With 5 survivors some seats never bid in a hand, and responder positions gave systematic risk differences."
    },
    {
      "what": "Each player gets one card from a fixed 33-card deck with a single special card, Max→0. The bidding is capped at 4 choice steps per hand.",
      "why": "This keeps the hand within 20 steps and 4 choices while preserving the unseen-own-card core and one special twist.",
      "fixes": "P5: The original's open-ended bidding and five chained special cards exceed the engine's step and choice limits."
    }
  ],
  "keeps": [
    "Everyone sees every card except their own.",
    "Strictly rising declarations about the total of all cards.",
    "Calling 'Coyote' to challenge the last claim; the wrong side takes a token.",
    "Negative cards and a special card (Max→0) that cancels the highest card.",
    "Three tokens eliminate a player; the last survivor wins.",
    "The loser opens the next hand."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The single-unseen-card inference is a strong, compact hidden element. The previous failures came from the bid floor and the forced call, both fixable within the limits."
  },
  "variation": {
    "name": "Coyote: Four Calls",
    "summary": "Each player sees every card but their own. Over exactly four turns per hand, players either raise the claimed total by at least 3 or call Coyote. If no one calls, the last claim is checked and the player it outbid is on the hook if it is true. Three tokens eliminate a player; the last survivor wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "R1 Setup. Seats are numbered 1 to N clockwise (N is 3 or 4). Every player starts with 0 tokens, opener_seat is 1 and hand_number is 1.\n\nR2 Deck and deal. The deck has exactly 33 cards:\n- one -10\n- two -5\n- three 0\n- four each of 1, 2, 3, 4 and 5\n- three 10\n- two 15\n- one 20\n- one special card called Max→0\nAt the start of every hand the deck is restored to these 33 cards and shuffled. Each surviving player is dealt exactly 1 card. All dealt cards return to the deck at the end of the hand.\n\nR3 Who sees what. Each player is privately told the card of every other surviving player, never their own.\n\nR4 Turn order. Each hand has exactly 4 turns. Turn 1 is the player in opener_seat. Turns 2, 3 and 4 go to the next surviving players clockwise, wrapping around as needed. With 3 survivors the opener also takes turn 4. With 2 survivors the two players alternate: opener, other, opener, other.\n\nR5 Turn 1 (opening). The opener declares a whole number from F to 80 inclusive, where F = 3 × (number of surviving players). That player becomes current_declarer and the number becomes current_declaration. previous_declarer is set to none.\n\nR6 Turns 2 and 3. The player either declares a whole number at least current_declaration + 3 and at most 80, or calls Coyote. If current_declaration + 3 is more than 80, only calling is allowed.\n- On a declaration, the old current_declarer becomes previous_declarer, the new player becomes current_declarer and the number becomes current_declaration.\n- On a call, that player is the caller, the hand stops and goes to R8.\n\nR7 Turn 4. The player either calls Coyote (go to R8 as caller) or declares a whole number at least current_declaration + 3 and at most 80. If current_declaration + 3 is more than 80, only calling is allowed. If they declare, the old current_declarer becomes previous_declarer, this player becomes current_declarer, and the hand goes to R9.\n\nR8 Resolving a call. Compute the true total (R10).\n- If the true total is less than current_declaration, the current_declarer loses the hand.\n- Otherwise the caller loses the hand.\n\nR9 Resolving the final declaration. Compute the true total (R10).\n- If the true total is less than current_declaration, the current_declarer (the turn-4 player) loses the hand.\n- Otherwise the previous_declarer loses the hand.\n\nR10 True total. Reveal all cards to everyone.\n- Add all card values, counting Max→0 as 0.\n- If Max→0 was dealt, find the single highest-valued other dealt card. If its value is positive, subtract it from the sum, so that card counts as 0. If two or more cards tie for highest, only one of them is cancelled.\n\nR11 Token. The loser gains 1 token. All cards, the true total and the loser are announced to everyone.\n\nR12 Elimination. A player with 3 tokens is eliminated. They are dealt no further cards and are skipped in turn order.\n\nR13 Next hand. The loser becomes opener_seat. If the loser was just eliminated, the next surviving player clockwise from them opens. hand_number increases by 1. Return to R2.\n\nR14 End. The game ends when only one player remains. Each hand gives exactly one token, so a 4-player game lasts at most 11 hands and a 3-player game at most 8.",
    "objective": "The last player not eliminated wins. Every hand gives exactly one token to exactly one player, so the game always ends with a single winner and never in a draw.",
    "expected_effect": "Minimum bidding is no longer safe:\n- The opening floor of 3 per player sits near the expected total (about 3.6 per card, less when Max→0 appears).\n- Raises of at least 3 quickly push claims above the true total.\n- Turn 4 is a genuine choice: call, or make a true-looking raise that shifts the loss to the previous declarer.\n\nSimple policies all lose against sensible play:\n- Always-minimum: as turn-2 or turn-3 bidder it gets called when its bid is likely too high, and as the turn-3 bidder it gets outbid by a true claim.\n- Always-call: it challenges claims near the floor that are true about half the time.\n- Always-maximum: it is called and loses at once.\n- Random play: it loses to all of the above.\n\nWinning comes from estimating your own card (the total is roughly the visible sum plus 3.6). It also comes from inferring your own card from rivals' declarations, since each bid leaks what that player sees and you know their card. Finally, it rewards choosing when to bluff or call so the token lands on someone else.\n\nThe rotating loser-opens order keeps any seat from holding a fixed role.\n\nTalk is left out for two reasons. Declarations are already the communication channel. Free talk would mostly add unverifiable claims about others' cards at the cost of extra steps."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 11
  }
}
```
````
