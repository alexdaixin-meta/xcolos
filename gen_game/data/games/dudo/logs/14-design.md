# 14 design

- time: 2026-10-28T05:36:32+00:00 (85.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b0f3f45a375ddb09, reply sha256 0fd011e3f1b9bfbe

## Sent

````
Original game: Dudo
Players in the original: 2 to 10

Original rules:
Each player starts with 5 dice and a cup. Each round all players shake and conceal their dice, then look at only their own. In clockwise order starting from the loser of last round, players bid: a number and a face, claiming at least that many dice among all players show that face. Ones are wild and count as any face. A bid must increase either the quantity, the face value, or both. Bidding aces is special: to switch to aces you may halve the current quantity rounded up; to switch from aces you must more than double the quantity. Instead of raising, a player may call Dudo. All cups are lifted. If the bid is true (at least as many dice as claimed), the caller loses one die; otherwise the bidder loses one die. Losing your last die eliminates you. Last player with dice wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rework bidding so that neither a fixed 'call Dudo or bid the minimum' choice nor an extreme bid is automatically right or wrong. Suggested changes:
- Narrow the raise range so bids climb gradually, not in jumps to absurd quantities. For example, a raise is either the same quantity with a higher face, or the quantity plus 1 or 2 with any face. Give the step limits as parameters.
- Cap the opening bid near the expected count, for example at most about T/2, so openings stay plausible. Keep the opening floor so the opener cannot always bid trivially low.
- Consider an exact-count call ('calza') that rewards a precise call. Alternatively, make a failed Dudo cost the caller more, for example 2 dice. Either way, calling Dudo every time stops being a free win.
- Re-check balance against thoughtless policies (first, last, random) at every player count until none of them wins far above its fair share.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 1 wins 90% of decided matches against random seats
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- against random seats the results were {'seat 1': 22, 'seat 2': 38}
- a thoughtless policy `first@seat1`: won 54, lost 6, drew 0
- a thoughtless policy `first@seat2`: won 53, lost 7, drew 0
- a thoughtless policy `last@seat1`: won 0, lost 60, drew 0
- a thoughtless policy `last@seat2`: won 26, lost 34, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Dudo (Perudo) is a bluffing dice game. Each player hides their own roll, and players take turns raising claims about how many dice of a face are showing across all cups, with ones wild. Anyone may call 'Dudo' to challenge the standing bid, the loser of the challenge loses a die, and the last player with dice wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the previous variation a thoughtless 'always first option' policy won 90% and 88% of decided matches from seats 1 and 2 against random seats. 'Always last' lost 60 of 60 from seat 1. The menu ordering and an unbounded raise range let a fixed reflex (in effect, challenge or bid the minimum) beat players who drift into absurd bids. The seat results were also lopsided (22 vs 38), so the turn order gave one seat an edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The core of Dudo rewards estimating counts and reading bids. But when a reflex policy captures almost all the value, it is not clear that a thinking player beats it. The dice roll adds variance in every hand, though elimination over many hands averages it out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Real Dudo play has a lot of depth: probability of counts, inferring an opponent's hand from their bids, bluffing, and choosing when to stop raising. Weak players still win challenges by chance."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's dice are hidden. Bids are noisy signals of hands. Whether to challenge depends on your own dice, the total in play and what the opponent's bidding reveals."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "A challenge is settled by counting dice showing the face plus ones. Losses are dice counts. The winner is the last player with dice."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Open-ended bidding sequences, the special ace-switching arithmetic and the unbounded raises exceed the 4-choice-step limit and are hard to build. A match can also run long. It is text-only and has no board, though."
    }
  ],
  "problems": [
    "P1: An unbounded raise range lets random or careless bids climb to absurd quantities, so a reflex challenger (or a reflex minimum bidder that lets opponents overreach) wins far above its fair share.",
    "P2: The opening bid could be trivially low or absurdly high, so neither the opener nor the responder faced a real decision.",
    "P3: A failed challenge was cheap relative to how often bids were false, so challenging was almost a free win against loose bidders.",
    "P4: The previous seat results (22 vs 38) and the 'last@seat1 lost 60/60' result show a structural seat edge and an ordering trap in the option menu.",
    "P5: Open-ended bidding rounds and ace-switching rules exceed the 4 choice steps per round and add arithmetic the builder may get wrong.",
    "P6: There was no hard length cap, so a match could run past what the platform can play."
  ],
  "changes": [
    {
      "what": "A raise is exactly one of two options: quantity +1 or quantity +2, with any face 2-6. Quantity may never exceed the total dice in play.",
      "why": "Bids climb in small steps and stay near the plausible range. Raising by +1 every time drives the bid above the expected count within two raises, where it is usually false and gets punished.",
      "fixes": "P1"
    },
    {
      "what": "The opening bid must have a quantity from floor(T/3) to ceil(T/2), where T is the total dice in play.",
      "why": "The floor sits at the expected count, so a minimum opening is true about 70% of the time and a reflex challenge against it usually fails. The cap stops absurd openings. The opener must pick face and quantity from their own hand, possibly bluffing.",
      "fixes": "P2"
    },
    {
      "what": "Add Calza, an exact-count call. If the count exactly equals the bid quantity, the caller regains one die (up to 5). Otherwise the caller loses one die.",
      "why": "This gives a precise alternative to Dudo that rewards accurate estimation. 'Always Calza' (the last option) loses most of the time, and 'always Dudo' meets bids that are often true.",
      "fixes": "P3"
    },
    {
      "what": "Each hand has at most 4 choice steps: the opening bid, two responses that may raise or call, and a final response that must be Dudo or Calza. The menu order is Raise +1, Raise +2, Dudo, Calza.",
      "why": "This fits the platform limit. A forced final call means the third bidder must leave a bid that is likely true, so overbidding at step 3 is punished, and players must plan for the cutoff. The 'first' option, Raise +1, is never automatically safe or automatically wrong. At the final step 'first' becomes Dudo, which is right only when the bid is false.",
      "fixes": "P5"
    },
    {
      "what": "A random draw chooses the first opener. After that, the player who lost a die opens the next hand, or the caller does if a Calza succeeded.",
      "why": "This removes the fixed seat-1 structural edge. Losing a die is compensated by gaining the choice of opening face.",
      "fixes": "P4"
    },
    {
      "what": "Drop the special ace bidding. Ones stay wild, and only faces 2-6 may be bid.",
      "why": "This removes the halving and doubling arithmetic and keeps the identity of wild ones.",
      "fixes": "P5"
    },
    {
      "what": "Cap the match at 30 hands. At the cap, the player with the most dice wins, and a tie for most is a draw.",
      "why": "This keeps matches short enough to play while elimination remains the normal ending.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Hidden dice in cups: each player sees only their own five dice",
    "Bids claim 'at least Q dice show face F' across all cups, with ones wild",
    "The Dudo challenge: a true bid costs the caller a die, a false bid costs the bidder a die",
    "Calza, the traditional exact-count call",
    "The loser of a hand opens the next",
    "Elimination when a player's last die is gone; last player with dice wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The bluffing and inference core is strong. The flaws were in raise range, opening limits and turn structure, and all of these can be fixed within the platform limits."
  },
  "variation": {
    "name": "Short Dudo",
    "summary": "Dudo with tight raises, a plausible opening window, at most four decisions per hand ending in a forced call, and Calza as an exact-count alternative to the challenge.",
    "players": {"min": 2, "max": 4, "suggested": 3},
    "rules": "SETUP. Each player starts with 5 dice. Seats are in a fixed order. Before hand 1, one random draw picks the first opener.\n\nEACH HAND.\n1. ROLL. Every player still in the game rolls all their dice. Each player is shown only their own dice. T is the total number of dice still in play, and every player is told T and each player's dice count.\n2. OPENING BID (choice step 1). The opener chooses a face from 2 to 6 and a quantity Q with floor(T/3) <= Q <= ceil(T/2). The bid means 'at least Q dice among all players show this face, counting ones as wild'. The bid is announced.\n3. RESPONSE 1 (choice step 2). The next player in seat order who is still in the game chooses one of: (a) Raise +1: new quantity = Q+1, with a face 2-6 of their choice; (b) Raise +2: new quantity = Q+2, with a face 2-6 of their choice; (c) Dudo: challenge the current bid; (d) Calza: claim the count is exactly Q. A raise is not allowed if it would make the quantity exceed T. If both raises are illegal, only Dudo and Calza may be chosen. The choice is announced.\n4. RESPONSE 2 (choice step 3). This happens only if response 1 was a raise. The next player in seat order makes the same kind of choice against the new bid. In a 2-player game this is the opener again.\n5. FINAL RESPONSE (choice step 4). This happens only if response 2 was a raise. The next player in seat order must choose Dudo or Calza. Raising is not allowed.\n6. REVEAL. All dice are revealed. N is the number of dice showing the bid face plus all dice showing 1.\n7. SETTLE. If the call was Dudo: if N >= Q, the caller loses 1 die; otherwise the player who made the current bid loses 1 die. If the call was Calza: if N = Q exactly, the caller gains 1 die (never above 5); otherwise the caller loses 1 die.\n8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from now on.\n9. NEXT OPENER. The player who lost a die opens the next hand. If no one lost a die (a successful Calza), the caller opens. If that player was eliminated, the next player in seat order who is still in opens.\n10. END CHECK. If one player remains, they win. Otherwise, if 30 hands have been played, the game ends as described below. Otherwise start a new hand.\n\nThere is no talk phase. Bids are the only communication.",
    "objective": "The last player with dice wins. If 30 hands are completed with two or more players still in, the player with the most dice wins. If two or more players tie for the most dice, the game is a draw.",
    "expected_effect": "Thoughtless policies should each be beatable. 'Always first' opens at the minimum on face 2, raises by 1 on face 2, and calls Dudo when forced. It overbids at step 3 into likely-false bids, so a thinking player challenges it, and its fixed face choice ignores its own dice. 'Always last' (Calza every time, or the highest opening) loses a die on most hands, because an exact count is hit only about a quarter of the time. 'Always Dudo' meets an opening floor at the expected count that is true about 70% of the time. Good play means opening on your strongest face, choosing +1 or +2 to leave a likely-true bid before the forced call, reading opponents' faces as hints about their hands, and choosing between Dudo and Calza from your own dice. Talk is left out. Bids already carry the signalling and bluffing, and in a last-player-standing game a talk phase would only add claims that cost nothing to make. Loser-opens and the random first opener remove the fixed seat edge."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 11,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
