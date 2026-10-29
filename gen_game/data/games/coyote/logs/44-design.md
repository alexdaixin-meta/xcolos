# 44 design

- time: 2026-10-27T09:37:02+00:00 (46.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e913768b225d9caf, reply sha256 d3cb163b1f166e0e

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Most of the game is complete. Deck reset each round, the deal, the private views, the legal declarations, the Max→0 tie rule with examples, resolution, tokens, opener rotation and the end check are all specified. The round bounds are correct: 3 players give 3+3+2 = 8 rounds, and 4 players give 3+3+3+2 = 11 rounds. Stated complexity is within limits: 13 steps, 1 random draw, 1 hidden element, 11 rounds.

Defect 1, the turn cap. Rule 4 says 'A round has at most 15 turns'. But declarations can run 1, 2, ..., 15, which is 15 declaration turns, followed by a forced 16th turn that calls Coyote. If the engine enforces a 15-turn cap, a round can end with caller = none. Rule 6 ('otherwise the caller loses') then has no loser, the token rule breaks, and so does the claim that 'exactly one player loses each round'. The rules give no fallback for reaching the cap.

Defect 2, the turn loop. The turn loop ('lap after lap' until Coyote) is a variable-length repeated sequential choice. The engine's step list is flat, so this has to be counted_repetition of one choice step with an exit condition. The design does not say how the repetition is bounded or exited (call = stop). Its 'choice_steps_per_round: 1' is only valid if the repeated choice counts once.

Talk: having no talk phase in a 3-4 player game is acceptable. Interests conflict (exactly one loser per round), declarations already carry information to reason about, and cheap talk would only add words.
- change: Fix the turn cap. Change 'A round has at most 15 turns' to 'A round has at most 16 turns: 15 possible declarations (1 to 15) and then a forced Coyote call.' Alternatively, add an explicit fallback: if the cap is reached with no call, the current_declarer is resolved against the total as if the next player called. Either way, every round must produce exactly one caller and one loser.
- change: Specify the turn loop as counted_repetition of a single choice step. Give it a maximum of 16 iterations and an exit condition: stop when coyote_called = yes, or force the call when current_declaration = 15. Confirm that choice_steps_per_round stays at 1 under that implementation.
The variation that was reviewed: Coyote: Open Circle: SETUP. Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = yes. opener_seat = 1 and round = 1.

DECK. At the start of every round the deck is reset to exactly these 15 cards and shuffled:
- one -2;
- two -1;
- three 0;
- two 1;
- two 2;
- two 3;
- one 4;
- one 5;
- one Max→0 card.

EACH ROUND:

1. ORDER. The turn order is opener_seat first, then each next alive seat clockwise, skipping eliminated seats. After the last alive seat it wraps back to opener_seat and repeats. Reset current_declaration = none, current_declarer = none, coyote_called = no, caller = none.

2. DEAL. Deal one card face down to each alive player.

3. PRIVATE VIEW. Each alive player is told privately the card of every other alive player, but never their own.

4. TURNS. Players act one at a time in the turn order, lap after lap, until someone calls Coyote. On a turn:
- If there is no declaration yet, the player must declare a whole number from 1 to 15.
- If the current declaration is d, from 1 to 14, the player either declares a whole number from d+1 to 15 or calls 'Coyote'.
- If the current declaration is 15, the player must call 'Coyote'.
A player may declare again on each of their later turns. Every declaration is announced to all players at once. A declaration sets current_declaration to that number and makes the player the current_declarer. Calling Coyote sets caller to that player and ends the turns. A round has at most 15 turns.

5. TRUE TOTAL.
- If and only if the Max→0 card was dealt: the Max→0 card counts 0, and exactly one other dealt card with the highest positive value also counts 0. If two cards tie for highest, only one of them counts 0. If no other dealt card is positive, nothing further changes. All remaining dealt cards are added.
- If the Max→0 card was not dealt, the true total is the plain sum of the dealt cards.
Examples:
- {1, 2, -1}, no Max→0: total 2.
- {Max→0, 5, 2, -1}: the 5 counts 0, total 1.
- {Max→0, 3, 3, 0}: one 3 counts 0, total 3.
- {Max→0, -1, 0}: total -1.

6. RESOLUTION. If the true total is less than current_declaration, the current_declarer loses. Otherwise (the total is at least the declaration) the caller loses.

7. TOKENS. The loser gains 1 token. A player who reaches 3 tokens is eliminated (alive = no) and takes no further part.

8. NEXT OPENER. opener_seat becomes the next alive seat clockwise after the current opener_seat, whoever lost.

9. ANNOUNCEMENT. Reveal to everyone: all cards, the true total, the final declaration, the declarer, the caller, the loser and everyone's tokens.

10. END CHECK. If only one player is alive, the game ends. Otherwise round increases by 1 and a new round begins. Exactly one player loses each round, so the game always ends within 8 rounds with 3 players and within 11 rounds with 4 players.

There is no talk phase. The declarations are the only communication. Winner: The last player still alive, with fewer than 3 tokens, wins. Because exactly one token is given out every round, the game always ends with a single survivor, so there are no draws.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluff-and-bid elimination game. Each player sees every feather card except their own. Players take turns raising a declared total of all cards in play until someone calls 'Coyote'. If the true total falls short of the last declaration, the declarer loses; otherwise the caller loses. Three losses eliminate a player, and the last survivor wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies can lose. 'Always call at once' loses whenever the opening bid is at or below the true total, and a low opening bid usually is. 'Always raise by 1' eventually overshoots the true total and loses as declarer. 'Always open high' loses when it is called. The opener seat rotates, so no seat keeps an edge. Winning means surviving, not having the highest total, so there is no safe option that cannot lose."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Each player sees all cards but one, so a good player can estimate the total tightly from the known deck composition and from other players' bids. A weak player who ignores the distribution of their own unseen card, or who reads nothing from the bids, overshoots or calls too early. The deal randomises information, not advantage. Everyone has exactly one unknown card."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A basic player can survive by bidding near the visible sum plus the expected value of their own card. Strong play adds several layers: inferring one's own card from what others bid, pushing a dangerous bid onto the next player, and timing calls. The Max→0 card makes totals uncertain in a way that needs real reasoning. The game is not solved and not hopeless."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Every player has hidden information, their own card. Bids leak information about that card because other players can see it. Doing well requires inference from limited information and modelling opponents."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The true total, the comparison with the last declaration, token counts and elimination are all arithmetic. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and has no board. However, the original has an open-ended deck with chained blue specials, and the reviewed variation had two build defects. First, its 15-turn cap could cut off the forced 16th call and leave a round with no caller. Second, its open 'lap after lap' turn loop gave no bounded repetition and no exit condition."
    }
  ],
  "problems": [
    "The original's blue special cards (draw from the deck, discard the highest, negate, double, reshuffle) form a long chain of rules that the engine cannot build reliably.",
    "The original's deck has no fixed composition here, so players cannot reason about the distribution of their unseen card.",
    "Turn cap defect: the reviewed variation capped a round at 15 turns. Declarations 1 to 15 can use all 15 turns, so the forced Coyote call on turn 16 could be cut off. That leaves caller = none and a round with no loser, which breaks the token rule.",
    "Turn loop defect: the reviewed variation's 'lap after lap' loop was not specified as a bounded counted repetition of one choice step with an exit condition. The build is ambiguous and the claim of one choice step per round was unsupported."
  ],
  "changes": [
    {
      "what": "Keep a fixed 15-card deck that is reset and shuffled every round, with a single special card, Max→0, whose effect is fully specified with tie rules and examples.",
      "why": "This replaces the chained blue specials with one buildable rule. It also gives players a known distribution to reason about.",
      "fixes": "The original's blue special cards (draw from the deck, discard the highest, negate, double, reshuffle) form a long chain of rules that the engine cannot build reliably."
    },
    {
      "what": "Publish the deck list in the rules, so every player knows which cards could be their own.",
      "why": "This allows probabilistic inference about one's own card.",
      "fixes": "The original's deck has no fixed composition here, so players cannot reason about the distribution of their unseen card."
    },
    {
      "what": "Raise the cap to at most 16 turns per round: up to 15 declarations (1 to 15), then a forced Coyote call. Add a safety fallback: if 16 turns pass with no call, the next alive player after the current declarer is recorded as the caller and the round resolves normally.",
      "why": "Every round now always has exactly one declarer, one caller and one loser.",
      "fixes": "Turn cap defect: the reviewed variation capped a round at 15 turns. Declarations 1 to 15 can use all 15 turns, so the forced Coyote call on turn 16 could be cut off. That leaves caller = none and a round with no loser, which breaks the token rule."
    },
    {
      "what": "Specify the turns as a counted repetition of ONE choice step, at most 16 iterations, with a turn counter that picks the acting player. The repetition exits as soon as coyote_called = yes. When current_declaration = 15, the only legal option is Coyote. The first turn of a round may not call.",
      "why": "This makes the loop buildable on a flat step list and justifies counting one choice step per round.",
      "fixes": "Turn loop defect: the reviewed variation's 'lap after lap' loop was not specified as a bounded counted repetition of one choice step with an exit condition. The build is ambiguous and the claim of one choice step per round was unsupported."
    }
  ],
  "keeps": [
    "Each player sees every card but their own.",
    "Declarations must strictly rise until someone calls Coyote.",
    "Resolution: the declarer loses if the true total is below the declaration, otherwise the caller loses.",
    "One token per loss, three tokens eliminate, and the last player alive wins.",
    "A special card that alters the total (Max→0, the descendant of the blue cards).",
    "No talk phase: declarations are the only communication, because interests already conflict and the bids carry the information."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The game already rewards inference about hidden information and reading opponents. Only the build defects in the turn cap and turn loop needed fixing."
  },
  "variation": {
    "name": "Coyote: Open Circle",
    "summary": "Each player sees every card but their own and bids on the total of all cards. Bids strictly rise until someone calls Coyote. The loser of each round takes a token, three tokens eliminate a player, and the last player alive wins. Each round's turns run as a bounded loop of at most 16 turns that always ends in a call.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP. Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = yes. Set opener_seat = 1 and round = 1.\n\nDECK. At the start of every round the deck is reset to exactly these 15 cards and shuffled:\n- one -2;\n- two -1;\n- three 0;\n- two 1;\n- two 2;\n- two 3;\n- one 4;\n- one 5;\n- one Max→0 card.\nEvery player knows this list.\n\nEACH ROUND:\n\n1. RESET AND ORDER. Set current_declaration = none, current_declarer = none, coyote_called = no, caller = none and turn_count = 0. The turn order starts at opener_seat and goes clockwise through the alive seats, skipping eliminated seats. After the last alive seat it wraps around to opener_seat again.\n\n2. DEAL. Deal one card face down to each alive player.\n\n3. PRIVATE VIEW. Each alive player is told privately the card of every other alive player, but never their own card.\n\n4. TURNS (one choice step, repeated at most 16 times). Repeat the following until coyote_called = yes, or until it has been done 16 times:\n- Add 1 to turn_count. The acting player is the player in position turn_count of the turn order: position 1 is the opener, position 2 is the next alive seat clockwise, and so on, wrapping around.\n- If current_declaration is none, the acting player must declare a whole number from 1 to 15. Calling Coyote is not allowed on the first turn.\n- If current_declaration is a number d from 1 to 14, the acting player either declares a whole number from d+1 to 15 or calls Coyote.\n- If current_declaration is 15, the acting player's only option is to call Coyote.\n- A declaration is announced to all players at once. It sets current_declaration to that number and current_declarer to the acting player.\n- Calling Coyote sets caller to the acting player and coyote_called = yes, which ends the repetition.\nA player may declare again on each of their later turns. Because declarations strictly rise from at least 1 to at most 15, there are at most 15 declarations, and the call comes on turn 16 at the latest. Safety fallback: if the repetition ends with coyote_called = no, the next alive player in the turn order after current_declarer becomes the caller.\n\n5. TRUE TOTAL.\n- If the Max→0 card was dealt, it counts 0. Exactly one other dealt card with the highest positive value also counts 0. If two or more cards tie for highest, only one of them counts 0. If no other dealt card is positive, nothing further changes. All remaining dealt cards are added.\n- If the Max→0 card was not dealt, the true total is the plain sum of the dealt cards.\nExamples:\n- {1, 2, -1}, no Max→0: total 2.\n- {Max→0, 5, 2, -1}: the 5 counts 0, total 1.\n- {Max→0, 3, 3, 0}: one 3 counts 0, total 3.\n- {Max→0, -1, 0}: total -1.\n\n6. RESOLUTION. If the true total is less than current_declaration, the current_declarer loses. Otherwise, when the total is equal to or greater than the declaration, the caller loses.\n\n7. TOKENS. The loser gains 1 token. A player who reaches 3 tokens is eliminated (alive = no) and takes no further part.\n\n8. NEXT OPENER. opener_seat becomes the next alive seat clockwise after the seat number of the current opener_seat, whoever lost. This works even if the current opener was just eliminated.\n\n9. ANNOUNCEMENT. Reveal to everyone: all dealt cards, the true total, the final declaration, the declarer, the caller, the loser and everyone's tokens.\n\n10. END CHECK. If only one player is alive, the game ends. Otherwise round increases by 1 and a new round begins. Exactly one player loses each round, so the game ends within 8 rounds with 3 players (3+3+2) and within 11 rounds with 4 players (3+3+3+2).\n\nThere is no talk phase. Declarations are the only communication.",
    "objective": "The last player still alive, with fewer than 3 tokens, wins. Exactly one token is given out every round, so the game always ends with a single survivor and there are no draws.",
    "expected_effect": "Play is unchanged from the reviewed variation, but every round now resolves cleanly with exactly one caller and one loser. Players estimate the total from the visible cards plus the known distribution of their own card, which has an expected value of about 1.2, and adjust for the Max→0 risk. They also infer their own card from others' bids and try to leave a dangerous bid to the next player. No talk is added. Interests conflict, since exactly one player loses each round, and the bids already carry the information worth reasoning about."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 1,
    "attributes": 14,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 11
  }
}
```
````
