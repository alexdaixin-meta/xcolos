# 39 design

- time: 2026-10-27T09:32:12+00:00 (66.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 e9136fc84bbf159f, reply sha256 f2a511e909eb61c0

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Build the turn order at the start of EVERY round, not only when a new hand is dealt. Compute it from opener_seat: the opener first, then each next alive player clockwise, skipping eliminated seats. Do this whether or not hand_active is true, so a continuing hand still gives each alive player exactly one turn per round. On each turn, offer the options from the rules. With no declaration, offer -3..20. With a declaration, offer current_declaration+1..20 plus 'coyote'. At 20, offer only 'coyote'. Decide 'is there a declaration' from current_declaration being non-null, or keep any has_declaration flag consistent with it. Do not depend on scratch state such as the declarations list that is only filled at deal time. When a round starts with hand_active true, do not deal cards and do not touch the deck. After Coyote, resolve it with R6/R7 using the cards the players actually hold: award the token, set hand_active to false, move opener_seat per R9, and skip the remaining turns of that round.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `Hand in progress: no new deal and the declaration carries on` failed: rule R6 is broken: When a round starts with hand_active true, then no cards are dealt and the hand continues with the same cards and declarations.; seat 1 was never offered 5, but should have been; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule 
- scenario `Coyote by the first player skips the rest of the round` failed: rule R8 is broken: When Coyote is called, then the remaining turns of that round are skipped.; seat 3 tokens: expected 1, got 0; game opener_seat: expected 2, got 1; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- scenario `With declaration 7: Coyote or 8..20 offered, not 7` failed: rule R10 is broken: When a declaration exists, then the player to act may declare a whole number from current_declaration+1 to 20 or call Coyote.; seat 1 was never offered 'coyote', but should have been; seat 1 was never offered 8, but should have been; seat 1 was never offered 20, but should have b
- scenario `Declaration 20 forces Coyote (cards 1,2,3 total 6 < 20, declarer loses)` failed: rule R11 is broken: When current_declaration is 20, then the player to act must call Coyote.; seat 3 tokens: expected 1, got 0; seat 1 was never offered 'coyote', but should have been; Ada: the rule for 'coyote' was never matched (the game never put that option to this seat)
- what the game did on `Hand in progress: no new deal and the declaration carries on`: moves played: . First attribute changes: seat 1 seat: None -> 1; seat 2 seat: None -> 2; seat 3 seat: None -> 3; table alive_count: 0 -> 3; seat 1 card: None -> 1; seat 2 card: None -> 2; seat 3 card: None -> 3; table hand_active: False -> True; table has_declaration: False -> True; table current_declaration: None -> 4; table current_declarer: None -> 1; table deck: [-2, -1, -1, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 100] -> [-2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 100]; table round: 1 -> 2; table rounds_done: 0 -> 1. Final: players {"seat 1": {"seat": 1, "tokens": 0, "alive": true, "card": 1}, "seat 2": {"seat": 2, "tokens": 0, "alive": true, "card": 2}, "seat 3": {"seat": 3, "tokens": 0, "alive": true, "card": 3}}; table {"deck": [-2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 100], "opener_seat": 1, "hand_active": true, "round": 2, "has_declaration": true, "current_declaration": 4, "current_declarer": 1, "declarations": [], "coyote_called": false, "caller": null, "true_total": null, "last_loser": null, "alive_count": 3, "revealed": [], "token_board": [], "pick": 0, "order": [], "turn_idx": 0, "turn_seat": 0, "new_hand": false, "
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Start: every player has 0 tokens and is alive, opener 1, round 1",
  "rule": "R1",
  "players": 4,
  "rounds": 0,
  "rules": [
   {
    "seat": 1,
    "options_include": 0
   }
  ],
  "expect": {
   "players": {
    "1": {
     "tokens": 0,
     "alive": true
    },
    "2": {
     "tokens": 0,
     "alive": true
    },
    "3": {
     "tokens": 0,
     "alive": true
    },
    "4": {
     "tokens": 0,
     "alive": true
    }
   },
   "game": {
    "opener_seat": 1,
    "round": 1
   }
  },
  "rule_text": "When the game starts, then every player has tokens 0 and alive true, opener_seat is 1, hand_active is false and round is 1."
 },
 {
  "name": "New hand resets deck to 20 cards before dealing 4 (16 left)",
  "rule": "R2",
  "players": 4,
  "rounds": 1,
  "given": {
   "game": {
    "deck": [
     1,
     2
    ]
   }
  },
  "rules": [
   {
    "seat": 1,
    "options_include": 0
   },
   {
    "seat": 2,
    "options_include": 1
   },
   {
    "seat": 3,
    "options_include": 2
   },
   {
    "seat": 4,
    "options_include": 3
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck": 16
    }
   },
   "game": {
    "round": 2
   }
  },
  "rule_text": "When a new hand begins, then deck is reset to exactly 20 cards: one -2, two -1, three 0, three 1, three 2, three 3, two 4, two 5 and one Max\u21920 (code 100)."
 },
 {
  "name": "Only alive players are dealt a card: 3 alive of 4 leaves 17 in deck",
  "rule": "R3",
  "players": 4,
  "rounds": 1,
  "given": {
   "players": {
    "4": {
     "tokens": 3,
     "alive": false
    }
   },
   "game": {
    "alive_count": 3
   },
   "status": {
    "4": "out"
   }
  },
  "rules": [
   {
    "seat": 1,
    "options_include": 0
   },
   {
    "seat": 2,
    "options_include": 1
   },
   {
    "seat": 3,
    "options_include": 2
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck": 17
    }
   },
   "players": {
    "4": {
     "tokens": 3,
     "alive": false
    }
   },
   "not_offered": [
    {
     "seat": 4,
     "option": 5
    },
    {
     "seat": 4,
     "option": "coyote"
    }
   ]
  },
  "rule_text": "When a round starts with hand_active false, then each alive player gets exactly 1 card drawn from deck, those cards leave deck, and eliminated players get no card."
 },
 {
  "name": "Deal gives one card per player (visibility itself is not observable)",
  "rule": "R4",
  "players": 3,
  "rounds": 1,
  "rules": [
   {
    "seat": 1,
    "options_include": 0
   },
   {
    "seat": 2,
    "options_include": 1
   },
   {
    "seat": 3,
    "options_include": 2
   }
  ],
  "expe

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluffing and bidding game for 2 to 6 players. Each player sees every feather card except their own, players take turns declaring ever-higher estimates of the true total of all cards, and anyone may call 'Coyote' to challenge the last declaration. Whoever is wrong takes a token, and three tokens eliminate a player.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy can lose. 'Always call Coyote' loses whenever the opener declares a cautious number. 'Always raise by one' loses once the declaration passes the true total. 'Open with the maximum' is called and loses. The seat advantage is small because the opener rotates."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "A player who sums the visible cards, estimates their own card from the remaining deck and reads what the others' declarations imply about it will beat a random bidder over many hands. The deal adds variance to single hands but not to the whole game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players survive some hands because errors land on whoever is last caught. Strong play keeps improving through better inference, bluffing and choosing whom to pass risk to."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's own card is hidden only from them. Players must infer it from the deck composition and from the others' declarations, which are made with sight of that card."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The true total is an arithmetic sum with fixed special-card rules. Who loses follows from comparing the total with the last declaration."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original lets a single hand run for an unbounded number of turns around the table and has five chained special cards. The previous adaptation let a hand continue across engine rounds through a hand_active flag. It failed tests: no turns were offered in continuing hands, Coyote did not resolve, and option ranges were wrong."
    }
  ],
  "problems": [
    "An unbounded hand (players go round the table until someone calls Coyote) does not fit a fixed number of choice steps per round. The previous fix, carrying the hand across rounds with hand_active, broke in testing: continuing rounds offered no turns, and Coyote never resolved.",
    "Five chained blue specials (add top of deck, discard highest, turn highest negative, double positives, zero forces reshuffle) create long rule chains and extra random draws. That exceeds the limits and invites resolution errors.",
    "A 6-player game would need more than 4 choice steps per round.",
    "Elimination alone has no fixed length, but the platform needs a bounded number of rounds.",
    "The option ranges and the handling of a declaration at the cap were underspecified, which produced the failed 'offered 8..20 plus coyote' and 'at 20 only coyote' tests."
  ],
  "changes": [
    {
      "what": "Each round is exactly one complete hand: a fresh deal, then one turn for each alive player in order. If nobody calls Coyote by the end of the order, the last declaration is checked automatically. If the true total is below it, its maker loses. Otherwise the player whose declaration it outbid loses. There is no hand_active flag and nothing carries between rounds except tokens, alive status and the opener.",
      "why": "Bounds every hand to at most 4 choice steps and removes the cross-round state that broke the build. Raising as the last player becomes a real bet that pushes risk onto the previous declarer.",
      "fixes": "An unbounded hand (players go round the table until someone calls Coyote) does not fit a fixed number of choice steps per round. The previous fix, carrying the hand across rounds with hand_active, broke in testing: continuing rounds offered no turns, and Coyote never resolved."
    },
    {
      "what": "Only one special card is kept, Max→0: it counts 0, and the single highest positive card among the others also counts 0. The deck is reset to the same 20 cards and shuffled every round.",
      "why": "Keeps Coyote's signature twist with a single comparison and exactly one random event per round.",
      "fixes": "Five chained blue specials (add top of deck, discard highest, turn highest negative, double positives, zero forces reshuffle) create long rule chains and extra random draws. That exceeds the limits and invites resolution errors."
    },
    {
      "what": "Player count is limited to 3 to 4.",
      "why": "One turn per alive player per round then never exceeds 4 choice steps.",
      "fixes": "A 6-player game would need more than 4 choice steps per round."
    },
    {
      "what": "The game is capped at 12 rounds. If more than one player is still alive at the end, the fewest tokens wins, and a tie for fewest is a draw.",
      "why": "Guarantees a bounded game. Four players can absorb at most 11 tokens before only one remains, so elimination usually decides the game first.",
      "fixes": "Elimination alone has no fixed length, but the platform needs a bounded number of rounds."
    },
    {
      "what": "Exact option lists. With no declaration yet, the player may declare a whole number from -5 to 20. With a current declaration d below 20, the options are d+1 to 20 or 'coyote'. At d = 20 the only option is 'coyote'. Whether a declaration exists is decided only by whether current_declaration is set. Every turn step is skipped once Coyote has been called.",
      "why": "Removes the ambiguity behind the failed option tests and makes skipping the rest of the round after Coyote a simple condition on each turn step.",
      "fixes": "The option ranges and the handling of a declaration at the cap were underspecified, which produced the failed 'offered 8..20 plus coyote' and 'at 20 only coyote' tests."
    }
  ],
  "keeps": [
    "Each player sees every card but their own.",
    "Strictly rising declarations of the total of all cards in play, with 'Coyote' as the challenge.",
    "The caller-or-declarer-loses resolution against the true total.",
    "The Max→0 style special that wipes out the highest card.",
    "Coyote tokens, elimination at 3, last player standing wins.",
    "The loser opens the next hand."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is a strong hidden-information bluffing game. Bounding each hand to one pass round the table and keeping one special card fits it within the limits and fixes the failed tests."
  },
  "variation": {
    "name": "Coyote: One Lap",
    "summary": "A 3 to 4 player Coyote in which each round is one complete hand of a single lap round the table. Players see everyone's card but their own and declare rising estimates of the total. They call Coyote to challenge, and if no one challenges, the last declaration is checked automatically. Three tokens eliminate a player, and the last player standing wins, within at most 12 rounds.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP (R1). Seats are numbered 1 to N clockwise, with N = 3 or 4. Every player starts with tokens = 0 and alive = true. opener_seat = 1 and round = 1.\n\nTHE DECK (R2). At the start of every round the deck is reset to exactly these 20 cards and shuffled:\n- one -2;\n- two -1;\n- three 0;\n- three 1;\n- three 2;\n- three 3;\n- two 4;\n- two 5;\n- one Max→0 card (recorded as code 100).\n\nEACH ROUND, in this order:\n\n1. TURN ORDER (R3). Build the order: opener_seat first, then each next alive seat clockwise, skipping eliminated seats, until every alive player appears once. Clear the hand state:\n- current_declaration = none;\n- current_declarer = none;\n- previous_declarer = none;\n- coyote_called = false;\n- caller = none.\n\n2. DEAL (R4). After shuffling, deal one card from the deck to each alive player. Eliminated players get no card.\n\n3. PRIVATE VIEW (R5). Each alive player is told privately the cards of every other alive player, but never their own card.\n\n4. TURNS (R6). Each player in the turn order gets exactly one turn, in order. A turn is skipped if coyote_called is true. On a turn:\n- If current_declaration is none, the player must declare a whole number from -5 to 20.\n- If current_declaration is a number d below 20, the player chooses either a whole number from d+1 to 20, or 'coyote'.\n- If current_declaration is 20, the only option is 'coyote'.\n\n5. EFFECT OF A TURN (R7).\n- Declaring a number x: previous_declarer becomes the old current_declarer, current_declarer becomes this player, and current_declaration = x.\n- Choosing 'coyote': coyote_called = true and caller = this player. All remaining turns this round are skipped.\n\n6. TRUE TOTAL (R8). Add the values of all dealt cards except the Max→0 card. If the Max→0 card was dealt, it counts 0. In addition, the single highest positive card among the other dealt cards counts 0 (only one card, even if tied). If no positive card was dealt, nothing else changes.\n\n7. RESOLUTION (R9).\n- If coyote_called is true: if true total < current_declaration, current_declarer loses; otherwise caller loses.\n- If coyote_called is false (everyone declared): if true total < current_declaration, current_declarer loses; otherwise previous_declarer loses.\n\n8. TOKEN AND ELIMINATION (R10). The loser gains 1 token. A player with 3 tokens becomes alive = false and takes no further part.\n\n9. NEXT OPENER (R11). If the loser is still alive, opener_seat = the loser. Otherwise opener_seat = the next alive seat clockwise after the loser.\n\n10. ANNOUNCEMENT (R12). Reveal to everyone:\n- all cards;\n- the true total;\n- the last declaration;\n- who called or whether the check was automatic;\n- who lost;\n- everyone's tokens.\n\n11. END CHECK (R13). The game ends immediately if only one player is alive. Otherwise round increases by 1, and the game ends after round 12.\n\nThere is no talk phase. All information comes from the private view and from the declarations made.",
    "objective": "If only one player is alive, that player wins. If the game reaches the end of round 12 with two or more players alive, the alive player with the fewest tokens wins. If two or more alive players tie for fewest tokens, the game is a draw.",
    "expected_effect": "Every hand finishes inside one round. This removes the broken hand_active continuation, and each turn's options follow directly from current_declaration.\n\nThe automatic check at the end of the lap makes the last player's choice sharp. Calling Coyote risks being wrong about the current declaration. Raising instead passes the risk to the previous declarer, but only if the raise is still true.\n\nEarlier players must keep their declarations near the truth, because they may be the previous declarer when the check falls. Good play means inferring your own card from the remaining deck and from how others bid while they can see it, bluffing to push neighbours into overreaching, and watching for the Max→0 card.\n\nThere is no talk phase. Each player's information gap is the same, one unseen card, so the deal changes what players know rather than who ends ahead. The loser opening the next hand gives some catch-up.\n\nEvery simple policy can lose:\n- Always Coyote loses to cautious openers.\n- Always +1 loses when the total is exceeded.\n- Always 20 loses to any caller.\n- Always the minimum is outbid and is exposed when it is the previous declaration and the last raise is true."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
