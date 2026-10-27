# 21 design

- time: 2026-10-27T09:03:53+00:00 (73.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 8011e944941e1042, reply sha256 4004ff088fa89117

## Sent

````
Original game: Coyote
Players in the original: 2 to 6

Original rules:
Each player wears a bandana with a feather whose value they cannot see but all others can. Feathers are drawn from a shuffled deck; some are positive, negative, or blue specials that modify the total. Starting player declares a total for all feathers in play. Clockwise each player must either declare a strictly higher total or call Coyote. When Coyote is called the round ends, all feathers are revealed and summed: add positives, subtract negatives, then apply blue cards in order (add top of deck, discard highest positive, turn highest positive negative, double positives, zero forces reshuffle). If the true total is less than the last declaration, that declarer loses; otherwise the caller loses. Loser takes a coyote token. Three tokens eliminates a player. Survivors draw new unseen feathers and the player who did not lose starts the next round. Last player remaining wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Don't assert on the size of the internal deck list after a round has finished. The rules reset the full deck each hand, and when cards go back is an implementation detail. Check dealing only through observable effects: each player holds a card, and the hand's true_total and token outcome agree with the dealt cards. For the declaration-60 scenario, don't expect an option named 'raise'. Raises are numeric declarations. Drive the bidding to 60 with numeric moves (for example the opener declares 60). Then check that the responder's only usable choice is call_coyote, or simply that the declarer (current_declarer) takes the token: with 3 players the true total is at most 50, below 60. Assert on hand_loser and tokens.
the game was built and works on the platform, but it does not behave as the independent tests say the rules require:
- scenario `Each of 3 players is dealt 1 card from the 33-card deck, leaving 30 (cards are random, so only counts are checked)` failed: rule R2 is broken: When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck.; game deck: expected 30 items, got 33
- scenario `Each of 4 players is dealt 1 card, leaving 29 in the deck` failed: rule R2 is broken: When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck.; game deck: expected 29 items, got 33
- scenario `At a declaration of 60 the responder can only call, and with 3 players the total never exceeds 50, so the declarer loses` failed: rule R6 is broken: When current_declaration is 60, a responder is offered only call_coyote.; Blaise: the rule for 'raise' was never matched (the game never put that option to this seat)
- what the game did on `Each of 3 players is dealt 1 card from the 33-card deck, leaving 30 (cards are random, so only counts are checked)`: moves played: r1 seat 1: -30; r1 seat 2: 'call_coyote'. First attribute changes: table pick: 0 -> 5; seat 1 card: 0 -> 5; table deck: [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100] -> [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]; table pick: 5 -> 4; seat 2 card: 0 -> 4; table deck: [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100] -> [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]; table pick: 4 -> 5; seat 3 card: 0 -> 5; table deck: [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100] -> [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 10, 10, 10, 15, 15, 20, 100]; table resp1: 0 -> 2; table resp2: 0 -> 3; table resp3: 0 -> 1; table bidding_open: False -> True; table current_declaration: 0 -> -30 .... Final: players {"seat 1": {"tokens": 0, "card": 5}, "seat 2": {"tokens": 1, "card": 4}, "seat 3": {"tokens": 0, "card": 5}}; table {"deck": [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 10, 10, 10, 15, 15, 20, 100, 5, 4, 5], "pick": 5, "hand_number": 2, "opener_seat": 2, "current_declaration": -30, "current_declarer": 1, "bidding_open": false, "caller": 2, "true_total": 14, "hand_loser": 2, "last_cards": [[1, 5], [2, 4], [3, 5]], "resp1": 2, "resp2": 3, "resp3": 1, "response": "call_coyote", "deck_size": 33, "count_mi
THE TESTS (written from the rules alone; judge whether they are right):
[
 {
  "name": "Start of game: 0 tokens, hand 1, opener seat 1",
  "rule": "R1",
  "players": 4,
  "rounds": 0,
  "seed": 1,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": -30
   }
  ],
  "expect": {
   "players": {
    "1": {
     "tokens": 0
    },
    "2": {
     "tokens": 0
    },
    "3": {
     "tokens": 0
    },
    "4": {
     "tokens": 0
    }
   },
   "game": {
    "hand_number": 1,
    "opener_seat": 1
   }
  },
  "rule_text": "When the game starts, every player has 0 tokens, hand_number is 1 and opener_seat is 1."
 },
 {
  "name": "Each of 3 players is dealt 1 card from the 33-card deck, leaving 30 (cards are random, so only counts are checked)",
  "rule": "R2",
  "players": 3,
  "rounds": 1,
  "seed": 2,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": -30
   },
   {
    "seat": 2,
    "options_include": "call_coyote"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck": 30
    }
   }
  },
  "rule_text": "When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max\u21920), and each player is dealt exactly 1 card that is removed from the deck."
 },
 {
  "name": "Each of 4 players is dealt 1 card, leaving 29 in the deck",
  "rule": "R2",
  "players": 4,
  "rounds": 1,
  "seed": 3,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": -30
   },
   {
    "seat": 2,
    "options_include": "call_coyote"
   }
  ],
  "expect": {
   "lens": {
    "game": {
     "deck": 29
    }
   }
  },
  "rule_text": "When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max\u21920), and each player is dealt exactly 1 card that is removed from the deck."
 },
 {
  "name": "Hidden cards are dealt and a hand still resolves: a call against -30 always costs the caller (any deal totals at least -20)",
  "rule": "R3",
  "players": 3,
  "rounds": 1,
  "seed": 4,
  "default": "decline",
  "rules": [
   {
    "seat": 1,
    "options_include": -30
   },
   {
    "seat": 2,
    "options_include": "call_coyote"
   }
  ],
  "expect": {
   "game": {
    "caller": 2,
    "hand_loser": 2,
    "hand_number": 2
   },
   "players": {
    "1": {
     "tokens": 0
    },
    "2": {
     "tokens": 1
    },
    "3": {
     "tokens": 0
    }
   }
  },
  "rule_text": "When cards are dealt, each player can see every other player's card but not their own."
 },
 {
  "name": "The opener may declare from -30 to 60 and becomes current_declarer",
  

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Coyote is a bluffing and estimation game in the style of Indian Poker. Each player sees every feather except their own. Players take turns declaring ever-higher guesses of the sum of all feathers, and anyone may call 'Coyote' instead. A wrong overbid or a wrong call costs a token, and three tokens eliminate a player.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Every simple policy can lose. 'Always call at once' loses whenever the opener declares a safe, low total. 'Always raise by 1' eventually overbids and loses when called. 'Always declare the maximum' loses almost every time, because the sum rarely reaches the cap. 'Always open at the minimum' only passes the risk on to a responder, who can raise cheaply. Seats rotate because the loser opens the next hand, so no seat has a fixed edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Each player's information differs from everyone else's by exactly one card. Players who estimate their own card well, who infer it from what others declare, and who judge whether a declarer is bluffing will win far more often than players who bid mechanically. The deal adds variance to single hands, but elimination over several hands averages it out."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player can still score with the expected value of the unseen card. A strong player goes further: they read the earlier declarations as signals about their own card, they choose bids that leave the next player in a bad spot, and they weigh the risk of the special card."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player has hidden information (their own card), and everyone else holds a different partial view. Doing well means inferring your own card from how others bid and modelling whether the current declarer is overreaching."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The true total is plain arithmetic on the cards. The loser follows from comparing that total with the last declaration, and eliminations follow from counting tokens."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "Several things do not fit well. The original has five ordered blue special cards, including a reshuffle and an 'add the top card of the deck' effect. Its bidding has no limit on length. Its declarations have no stated range. When it was built previously, two ambiguities produced tests that disagreed with the build: the rules did not say when cards return to the deck, so tests asserted the deck size after a hand and failed; and the rules did not say how raises are expressed, so tests looked for an option called 'raise'."
    }
  ],
  "problems": [
    "P1: The five ordered blue special cards (draw an extra card, discard the highest, flip the highest to negative, double positives, reshuffle) make a long, order-dependent rule chain that is expensive to build and easy to get wrong.",
    "P2: Bidding can go on for any number of turns, which breaks the limit of 4 choice steps per round.",
    "P3: Declarations have no stated range, so the option list is unbounded.",
    "P4: The previous rules did not say when dealt cards go back into the deck. Tests asserted that the deck held 30 cards after a finished hand, but the build had already returned the cards, leaving 33.",
    "P5: The previous rules did not say how a raise is expressed. Tests expected an option named 'raise', but raises are numeric declarations, so the test at a declaration of 60 checked for something that never exists.",
    "P6: The original does not say who opens after a loss in a game with more than two players, or how bidding skips eliminated players."
  ],
  "changes": [
    {
      "what": "Keep a single special card, Max→0. It counts as 0, and it also makes the single highest-valued other card in play count as 0, provided that card is positive.",
      "why": "This keeps the special-card uncertainty, which forces reasoning about the risk of an unseen modifier, with a one-step rule.",
      "fixes": "P1"
    },
    {
      "what": "Each hand has at most 4 choice steps: the opener's declaration, a first response, a second response, and a third response that may only call Coyote.",
      "why": "This bounds the hand within the engine's limit. The second responder knows the next player must call, so they must declare something they believe is true, which adds a planning layer.",
      "fixes": "P2"
    },
    {
      "what": "Declarations are whole numbers from -30 to 60, and each raise must be strictly higher than the current declaration. When the declaration is 60, the responder is offered only call_coyote.",
      "why": "This gives a finite option list, and every possible total that matters lies inside it.",
      "fixes": "P3"
    },
    {
      "what": "The rules now say explicitly that the deck is rebuilt to all 33 cards at the start of each hand, and that all dealt cards go back when the hand ends, so between hands the deck always holds 33. Dealing is checked through each player holding exactly one card and through the true total and token outcome agreeing with the dealt cards, not through the deck size after a hand.",
      "why": "This removes the timing ambiguity the tests tripped on.",
      "fixes": "P4"
    },
    {
      "what": "The rules now say plainly that there is no option named 'raise': a raise is choosing a number. Each responder's options are the legal numbers plus call_coyote.",
      "why": "This matches the build and the tests to one reading.",
      "fixes": "P5"
    },
    {
      "what": "The loser of a hand opens the next hand, or the next surviving player clockwise if the loser was just eliminated. Bidding goes clockwise among surviving players only and wraps past the opener if needed.",
      "why": "This gives a deterministic order for any number of players and rotates the opening seat.",
      "fixes": "P6"
    }
  ],
  "keeps": [
    "Each player sees everyone's card but their own.",
    "Players make rising declarations of the total of all cards in play, or call Coyote instead.",
    "If the true total is below the last declaration the declarer loses; otherwise the caller loses.",
    "The loser of a hand takes a coyote token, three tokens eliminate a player, and the last player standing wins.",
    "The deck mixes negative, zero and positive cards with a special card that cancels the highest card."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core is strong hidden-information inference and bluffing that fits the engine. It needs only a simplified special card, bounded bidding, and rules wording that removes the two ambiguities the tests exposed."
  },
  "variation": {
    "name": "Coyote: Short Count",
    "summary": "Each player sees every card but their own. Players make up to three rising declarations of the table's total, and a call settles the hand: whoever was wrong takes a token. Three tokens and you are out, and the last player standing wins.",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "rules": "R1 Setup. At the start of the game every player has 0 tokens, hand_number is 1 and opener_seat is 1. Seats are numbered 1 to N clockwise.\n\nR2 The deck and the deal. The deck has exactly 33 cards: one -10, two -5, three 0, four each of 1, 2, 3, 4 and 5, three 10, two 15, one 20, and one special card called Max→0. At the start of every hand the deck is rebuilt to these 33 cards and shuffled. Each surviving player is then dealt exactly 1 card, which is removed from the deck for the rest of the hand. When the hand ends, all dealt cards go back to the deck, so between hands the deck always holds all 33 cards. Dealing is correct when every surviving player holds exactly one card and the hand's true total and token outcome agree with those cards. The deck size after a finished hand is not a measure of dealing.\n\nR3 Who sees what. Each player is privately told the card of every other surviving player, but never their own card.\n\nR4 Opening. The player in opener_seat declares a whole number from -30 to 60, inclusive. That player becomes current_declarer, and the number becomes current_declaration.\n\nR5 Responses. The surviving players after the opener, going clockwise and wrapping past the opener if there are fewer than four survivors, make up to three responses in turn.\n- First response and second response: the responder either declares a whole number strictly higher than current_declaration and at most 60, or chooses call_coyote. There is no option named 'raise'. Raising simply means choosing a number. A responder who declares becomes current_declarer, and the number becomes current_declaration. If current_declaration is 60, the responder is offered only call_coyote.\n- Third response: if no one has called yet, the third responder must choose call_coyote; it is their only option.\nAs soon as anyone calls, that player is the caller, bidding stops, and the hand is resolved.\n\nR6 True total. All cards are revealed to everyone. The true total is computed in two steps. First, add up the values of all cards, counting Max→0 as 0. Second, if Max→0 is among the dealt cards, find the single highest-valued other card. If its value is positive, subtract its value from the sum, so that card counts as 0. If two or more cards tie for highest, only one of them is cancelled.\n\nR7 The loser. If the true total is less than current_declaration, the current_declarer loses the hand. Otherwise, when the true total is equal to or greater than current_declaration, the caller loses the hand. The loser gains 1 token. The dealt cards and the true total are announced to everyone.\n\nR8 Elimination. A player who reaches 3 tokens is eliminated. They take no further part, are dealt no cards and are skipped in the bidding order.\n\nR9 Next hand. The loser of the hand becomes opener_seat for the next hand. If the loser has just been eliminated, the next surviving player clockwise from them opens instead. hand_number increases by 1, and the next hand begins with R2.\n\nR10 End. The game ends as soon as only one player is not eliminated. Each hand produces exactly one token, so with N players the game lasts at most 3(N-1)+2 hands, which is 14 hands for 5 players.",
    "objective": "The last player not eliminated wins. Every hand gives exactly one token to exactly one player, so the game always ends with a single winner and never in a draw.",
    "expected_effect": "Players must estimate their own unseen card from the deck composition and the visible cards, and then refine that estimate by reading the other players' declarations, which each player makes from a different view. Bounding the bidding at three responses makes position strategic. The second responder knows the third must call, so they should declare a number they believe is true, while earlier bidders can push the total up to squeeze later players. The single Max→0 card keeps a real risk of a sudden collapse in the total, which rewards players who track which high cards are visible. Talk is deliberately left out. The declarations already serve as the signalling and bluffing channel, and free messages would let players simply tell each other their cards at no cost, which would erase the hidden information that the game is built on."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 16,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 14
  }
}
```
````
