# 42 design

- time: 2026-10-27T09:34:44+00:00 (88.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 dd2338d99271e689, reply sha256 51577459a6964dda

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: WORST-CASE TRUE TOTAL. The lowest cards are -2, -1, -1, then 0s. R8 only ever zeroes a positive card, so it can raise a negative total but never lower it. Minimum T is -2-1 = -3 with 2 alive, -2-1-1 = -4 with 3 alive, and -2-1-1+0 = -4 with 4 alive.

OPENER POLICY 'always declare the lowest number (-5)'. The opener can lose only if someone calls coyote while T < -5, and T >= -4 always. So with 3 or 4 alive the opener never loses, whatever the cards and whatever the others do. Coyote on -5 always loses (T >= -5), so the next player is forced to raise. With 3 or more alive the opener can never be previous_declarer at an automatic check, so the auto-check cannot reach them either. Any other opening carries some risk, so -5 weakly dominates, and the opener's only decision is trivial.

4 ALIVE, worse still. Seat 2 can declare -4 (T >= -4 always). Seat 3 then cannot profitably call: coyote loses whenever T >= -4, which is always. So seats 1 and 2 are both immune, and the round is a duel between seats 3 and 4 only.

3 ALIVE (A opens -5, then B and C), winner-rule table:
- C calls coyote on B's x: B loses if T < x, else C loses.
- C raises to y: auto-check; C loses if T < y, else B loses.
- A loses in 0% of cases.

SEAT EDGE FROM MOVE ORDER. R11 makes the previous loser the opener, so the previous loser is immune next round while 3 or more are alive. That is a large move-order effect: it hands immunity to the trailing player and pushes token counts toward equality. A plausible 3-player line is losses landing B, C, B, C and so on. With 12 rounds and ties for fewest tokens declared a draw, draws are likely.

2 ALIVE. The immunity reverses. If A opens -5, B declares -4 (T >= -3), is safe at the auto-check, and A loses. So the opener must take a real risk only in the endgame.

VERDICT. One thoughtless policy, opening at the minimum, never loses for most of the game. That fails the never-loses test.
- playable FAILED: R8 ambiguity. It says: 'Add the values of all dealt cards except the Max→0 card. If the Max→0 card was dealt, it counts 0. In addition, the single highest positive card among the other dealt cards counts 0.' It is unclear whether 'In addition' applies only when Max→0 was dealt, as in the original Coyote, or always.
- If always: the Max→0 card is just a 0 and the 'code 100' is pointless.
- If only with Max→0: the sentence 'If no positive card was dealt, nothing else changes' is misplaced.
- The two readings give different totals. Example: cards {1, 2, -1} give T = 0 under the 'always' reading and T = 2 under the conditional reading.
- Different referees, or a player and the engine, would disagree, and every loss is decided by this number.

The rest is complete and within limits:
- steps 15 <= 20, choice steps 4 <= 4, attributes 15 <= 20, hidden 1 <= 3, random draws 1 <= 1, rounds 12 <= 40;
- the game is finite;
- it needs no board or clock;
- turns are legitimately sequential, because the order is the point.

Talk absent: acceptable, since declarations are the communication channel.
- reasoning_over_luck FAILED: WHAT IS UNKNOWN. Each player's only unknown is their own card, and others' declarations leak a little about it.

WORKED CASE, 3 alive (A opens -5; B sees a=1 and c=2). B's own card b comes from the 18 remaining cards. Under the 'always zero highest positive' reading, T is distributed:

| T | Count (of 18) |
|---|---|
| -1 | 1 (b=-2) |
| 0 | 2 (b=-1) |
| 1 | 4 (b=0 x3, b=Max→0 x1) |
| 2 | 2 (b=1) |
| 3 | 9 (b=2,3,4,5) |

B's best declaration, x=3, is true only 50% of the time. Whatever B does, C (who sees a and b) chooses call or raise with a similar near-coin-flip about c. So the exposed players lose with probability around 35-50%, decided by the deal.

INTENDED GOOD STRATEGY BY ALL:
- the opener plays -5 and is immune;
- the remaining two (or the last two of four) face a guess about their own hidden card;
- the outcome of each round is mostly the deal;
- the long-run winner is mostly the deal plus R11's rotation of immunity, with frequent draws.

INFERENCE FROM DECLARATIONS. This exists only for the last mover in each duel, and the opener's forced -5 carries no information. Reasoning matters only marginally next to the draw.
- change: Remove the safe opening. Restrict the opening declaration to a range that can be false, e.g. the opener must declare at least the true minimum + 3 (from -1 up to 20), or score the opener as a loser whenever the final auto-check is true and no coyote was called. Show by table that no seat is immune.
- change: Make loss exposure symmetric: a full repeating lap until someone calls coyote, capped at 20 declarations, so every declarer can be challenged by the next player, instead of one lap with an auto-check against the previous declarer.
- change: Change R11 so the loser does not gain a protected opening seat. For example, the opener rotates clockwise each round regardless of who lost, to remove the move-order edge.
- change: Rewrite R8 unambiguously, e.g. 'If and only if the Max→0 card was dealt: it counts 0 and the single highest positive other card counts 0. Otherwise sum all cards.' Give a worked example.
- change: Reduce luck. Either give each player 2 cards, one visible to all and one hidden from themselves, or narrow the deck spread so own-card uncertainty is smaller and declarations carry more inferable information. Show that a reasoning player beats a random-declaring one in a clear majority of rounds.
- change: Add a tie-break for the round-12 ending (e.g. fewest coyote calls lost, or most correct declarations) to cut the draw rate.
The variation that was reviewed: Coyote: One Lap: SETUP (R1). Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = true. opener_seat = 1 and round = 1.

THE DECK (R2). At the start of every round the deck is reset to exactly these 20 cards and shuffled:
- one -2;
- two -1;
- three 0;
- three 1;
- three 2;
- three 3;
- two 4;
- two 5;
- one Max→0 card (recorded as code 100).

EACH ROUND, in this order:

1. TURN ORDER (R3). Build the order: opener_seat first, then each next alive seat clockwise, skipping eliminated seats, until every alive player appears once. Clear the hand state:
- current_declaration = none;
- current_declarer = none;
- previous_declarer = none;
- coyote_called = false;
- caller = none.

2. DEAL (R4). After shuffling, deal one card from the deck to each alive player. Eliminated players get no card.

3. PRIVATE VIEW (R5). Each alive player is told privately the cards of every other alive player, but never their own card.

4. TURNS (R6). Each player in the turn order gets exactly one turn, in order. A turn is skipped if coyote_called is true. On a turn:
- If current_declaration is none, the player must declare a whole number from -5 to 20.
- If current_declaration is a number d below 20, the player chooses either a whole number from d+1 to 20, or 'coyote'.
- If current_declaration is 20, the only option is 'coyote'.

5. EFFECT OF A TURN (R7).
- Declaring a number x: previous_declarer becomes the old current_declarer, current_declarer becomes this player, and current_declaration = x.
- Choosing 'coyote': coyote_called = true and caller = this player. All remaining turns this round are skipped.

6. TRUE TOTAL (R8). Add the values of all dealt cards except the Max→0 card. If the Max→0 card was dealt, it counts 0. In addition, the single highest positive card among the other dealt cards counts 0 (only one card, even if tied). If no positive card was dealt, nothing else changes.

7. RESOLUTION (R9).
- If coyote_called is true: if true total < current_declaration, current_declarer loses; otherwise caller loses.
- If coyote_called is false (everyone declared): if true total < current_declaration, current_declarer loses; otherwise previous_declarer loses.

8. TOKEN AND ELIMINATION (R10). The loser gains 1 token. A player with 3 tokens becomes alive = false and takes no further part.

9. NEXT OPENER (R11). If the loser is still alive, opener_seat = the loser. Otherwise opener_seat = the next alive seat clockwise after the loser.

10. ANNOUNCEMENT (R12). Reveal to everyone:
- all cards;
- the true total;
- the last declaration;
- who called or whether the check was automatic;
- who lost;
- everyone's tokens.

11. END CHECK (R13). The game ends immediately if only one player is alive. Otherwise round increases by 1, and the game ends after round 12.

There is no talk phase. All information comes from the private view and from the declarations made. Winner: If only one player is alive, that player wins. If the game reaches the end of round 12 with two or more players alive, the alive player with the fewest tokens wins. If two or more alive players tie for fewest tokens, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is an elimination bluffing game. Each player sees everyone's feather card except their own. Players take turns declaring ever-higher claims about the total of all cards, or call 'Coyote' on the last claim. Whoever is wrong about the true total takes a token, three tokens eliminate a player, and the last player standing wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation the lowest legal opening (-5) is below the lowest possible true total (-4 with 3 or 4 players alive), so opening at the minimum can never lose. Every other opening carries some risk, so -5 weakly dominates. With 4 alive, seat 2 can declare -4 and is also immune, so each round is a duel between seats 3 and 4. Rule R11 hands the opener seat, and with it immunity, to the previous loser. That is a large move-order effect that evens out token counts and produces many draws at round 12."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "The exposed players face a near coin-flip about their own card. In the worked case, the best declaration is true only 50% of the time. Within a single lap only the last mover can infer anything from declarations, and the opener's forced -5 carries no information. Who loses each round is decided mostly by the deal and by the rotation of immunity."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Part of the game is solved trivially: the opener always plays -5. The rest is a guess with little information. A strong player has little to improve on, and a weak player loses mainly to the cards. The original Coyote has real headroom, through reading other players' declarations about your own card over several turns, but the one-lap structure removed it."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "There is real hidden information: your own card. But a single lap with an automatic check gives almost no declarations to infer it from, and the safe opening removes one seat from the reasoning entirely. Inference matters only marginally next to the draw."
    },
    {
      "criterion": "verifiable",
      "verdict": "bad",
      "evidence": "Rule R8 is ambiguous about whether the highest positive card is zeroed always or only when the Max→0 card is dealt. Cards {1, 2, -1} give a total of 0 under one reading and 2 under the other. Every loss depends on this number, so the result does not follow unambiguously by arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is turn-based and text-only, needs no board, ends in at most 12 rounds and fits the step limits (15 steps, 4 choice steps, 1 hidden element, 1 draw). Sequential turns are legitimate because the order of declarations is the point of the game."
    }
  ],
  "problems": [
    "P1 Safe opening: the lowest legal opening is below the lowest possible true total, so 'always open at the minimum' never loses, and with 4 alive seat 2 is immune too.",
    "P2 Asymmetric exposure: one lap plus an automatic check against the previous declarer means some seats can never be challenged while others always face a forced guess.",
    "P3 Move-order edge: the previous loser opens next round and so inherits the protected seat. Losses alternate and draws are likely.",
    "P4 Ambiguous scoring: R8 can be read two ways that give different true totals.",
    "P5 Luck over reasoning: with one lap there are too few declarations to infer your own card, so rounds are near coin-flips decided by the deal.",
    "P6 Draws: the round-12 ending with ties for fewest tokens declared a draw often produces no winner."
  ],
  "changes": [
    {
      "what": "The opening declaration must be at least 1, while the true total can be as low as -4 with this deck. Every declaration, including the opening, can be false and can be challenged by the next player.",
      "why": "Opening at the lowest legal value now loses whenever the true total is 0 or less and the next player calls. Seat 2 sees three of the four cards and can spot those deals. No seat or opening is immune, and a low opening is only safe when the cards the opener sees justify it.",
      "fixes": "P1 Safe opening"
    },
    {
      "what": "Turns repeat around the table in clockwise laps until someone calls Coyote. A player who faces a declaration of 15 (the highest possible total) must call. The automatic check is removed.",
      "why": "Every declarer is exposed to exactly one challenger, the next player, so exposure is the same for every seat. Bounded strictly increasing declarations guarantee the round ends, after at most 15 turns.",
      "fixes": "P2 Asymmetric exposure"
    },
    {
      "what": "The opener seat rotates to the next alive seat clockwise every round, whoever lost.",
      "why": "This removes the protected-seat reward for losing and balances seats over the game.",
      "fixes": "P3 Move-order edge"
    },
    {
      "what": "R8 is rewritten with an 'if and only if' rule and worked examples.",
      "why": "There is now one unambiguous total for every deal.",
      "fixes": "P4 Ambiguous scoring"
    },
    {
      "what": "Multi-lap declarations replace the single lap, and the deck is trimmed to 15 cards with a tighter spread (one -2, two -1, three 0, two 1, two 2, two 3, one 4, one 5, one Max→0).",
      "why": "A player now hears several declarations from opponents who can see their card, and must infer their own card from how high those opponents dared to go. They must also judge whether an opponent is bluffing upward to set them up. Each card is a smaller share of the total, so careful inference shifts the odds markedly compared with random declaring.",
      "fixes": "P5 Luck over reasoning"
    },
    {
      "what": "The round cap and the fewest-tokens draw rule are removed. Exactly one player loses each round, so with 3 tokens to eliminate the game always ends with one survivor: by round 8 at the latest with 3 players, by round 11 with 4.",
      "why": "Every game has a single winner decided by elimination arithmetic, with no draws.",
      "fixes": "P6 Draws"
    }
  ],
  "keeps": [
    "Each player sees every card but their own.",
    "Strictly rising declarations about the total of all cards in play, with a 'Coyote' call against the last declaration.",
    "The loser-takes-a-token, three-tokens-eliminates structure, with the last player standing as winner.",
    "A special Max→0 card that zeroes the highest positive card, keeping the original's twist on the total.",
    "Declarations as the only communication channel."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Coyote, inferring your own hidden card from how opponents who can see it bid, is strong strategic reasoning. The failures came from the variation's safe opening, single lap, loser-opens rule and ambiguous total, and all of these can be fixed within the limits."
  },
  "variation": {
    "name": "Coyote: Open Circle",
    "summary": "Three or four players each see every card but their own and take turns in repeating laps, declaring ever-higher claims about the total of all cards until someone calls Coyote. The wrong party takes a token, three tokens eliminate a player, and the last survivor wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP. Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = yes. opener_seat = 1 and round = 1.\n\nDECK. At the start of every round the deck is reset to exactly these 15 cards and shuffled:\n- one -2;\n- two -1;\n- three 0;\n- two 1;\n- two 2;\n- two 3;\n- one 4;\n- one 5;\n- one Max→0 card.\n\nEACH ROUND:\n\n1. ORDER. The turn order is opener_seat first, then each next alive seat clockwise, skipping eliminated seats. After the last alive seat it wraps back to opener_seat and repeats. Reset current_declaration = none, current_declarer = none, coyote_called = no, caller = none.\n\n2. DEAL. Deal one card face down to each alive player.\n\n3. PRIVATE VIEW. Each alive player is told privately the card of every other alive player, but never their own.\n\n4. TURNS. Players act one at a time in the turn order, lap after lap, until someone calls Coyote. On a turn:\n- If there is no declaration yet, the player must declare a whole number from 1 to 15.\n- If the current declaration is d, from 1 to 14, the player either declares a whole number from d+1 to 15 or calls 'Coyote'.\n- If the current declaration is 15, the player must call 'Coyote'.\nA player may declare again on each of their later turns. Every declaration is announced to all players at once. A declaration sets current_declaration to that number and makes the player the current_declarer. Calling Coyote sets caller to that player and ends the turns. A round has at most 15 turns.\n\n5. TRUE TOTAL.\n- If and only if the Max→0 card was dealt: the Max→0 card counts 0, and exactly one other dealt card with the highest positive value also counts 0. If two cards tie for highest, only one of them counts 0. If no other dealt card is positive, nothing further changes. All remaining dealt cards are added.\n- If the Max→0 card was not dealt, the true total is the plain sum of the dealt cards.\nExamples:\n- {1, 2, -1}, no Max→0: total 2.\n- {Max→0, 5, 2, -1}: the 5 counts 0, total 1.\n- {Max→0, 3, 3, 0}: one 3 counts 0, total 3.\n- {Max→0, -1, 0}: total -1.\n\n6. RESOLUTION. If the true total is less than current_declaration, the current_declarer loses. Otherwise (the total is at least the declaration) the caller loses.\n\n7. TOKENS. The loser gains 1 token. A player who reaches 3 tokens is eliminated (alive = no) and takes no further part.\n\n8. NEXT OPENER. opener_seat becomes the next alive seat clockwise after the current opener_seat, whoever lost.\n\n9. ANNOUNCEMENT. Reveal to everyone: all cards, the true total, the final declaration, the declarer, the caller, the loser and everyone's tokens.\n\n10. END CHECK. If only one player is alive, the game ends. Otherwise round increases by 1 and a new round begins. Exactly one player loses each round, so the game always ends within 8 rounds with 3 players and within 11 rounds with 4 players.\n\nThere is no talk phase. The declarations are the only communication.",
    "objective": "The last player still alive, with fewer than 3 tokens, wins. Because exactly one token is given out every round, the game always ends with a single survivor, so there are no draws.",
    "expected_effect": "No seat or simple policy is safe.\n- 'Always open at 1' loses whenever the total is 0 or less and the next player, who sees three of the four cards, calls.\n- 'Always call Coyote' loses whenever the declaration was true, which is most low declarations.\n- 'Always raise by 1' eventually overshoots the true total and gets called.\n- Random declaring loses to a player who tracks the visible cards.\n\nThe repeating laps make the central skill the original's: reading how high opponents, who can see your card, are willing to go. You then decide whether a high declaration reflects your own strong card or is a bluff meant to leave you holding an impossible number.\n\nRotating the opener removes the seat edge, the unambiguous total removes referee disputes, and the elimination ending guarantees one winner.\n\nTalk is left out. Players do disagree, since only one can survive, but the declarations already carry the bluffing and signalling. Free talk would add cheap, unenforceable claims without new decisions."
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
