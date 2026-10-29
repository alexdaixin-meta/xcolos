# 01 design

- time: 2026-10-28T03:47:41+00:00 (70.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 43e28601cec8f9d6, reply sha256 76da1018245c2ce3

## Sent

````
Original game: Jukha
Players in the original: 3 to 13

Original rules:
Use 4 cards of each rank per player plus one Joker in total. Deal all cards clockwise so player left of dealer gets 5, others 4; keep hands hidden. Suits irrelevant. On a turn, if you have 4 cards and they are all equal, show them and exit and cannot lose. Otherwise you must request a card from the player who currently has 5 cards. You may name a rank you want. The 5-card player must offer one card face down and may claim any rank, truthfully or not. You may take it and end your turn with 5 cards, or reject it to ask for a second. If second offered, you must take one of the two offered and other returns. You may instead ask for a third; then you must take the third and both first return. After your turn you have 5 and are asked next. Having 4 of a kind plus extra does not let you exit; you need exactly 4 at start of your turn. Joker cannot exit. Play until only two players remain; they both lose.
````

## Reply

````
```json
{
  "original_summary": "Jukha is a hidden-hand card game in the Old Maid family. Cards pass around the table one at a time: the player holding 5 cards offers a face-down card with a claim about its rank that may be a lie, and the taker accepts it or asks for another. A player who starts a turn holding exactly four of a kind leaves the game safe, and the last two players left both lose.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. Always taking the first offer lets a lying offerer push the Joker or useless cards onto you. Always telling the truth teaches the receiver what you are dumping. Always asking for a third card gives up all control. The giver controls what the next player gets, so what each player keeps and gives changes who exits first. The only seat edge is the deal: the player left of the dealer starts with 5 cards and gives first."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Reading the bluffs and tracking which ranks each neighbour is collecting are real skills. With up to 13 players, though, each player only meets two neighbours, the deal is large, and the order of exits is heavily shaped by the starting hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Several things can keep improving: building a picture of a neighbour's target rank from their requests, judging how far their claims can be trusted, and deciding which cards to deny. A weak player still exits sometimes, because collecting four of a kind needs no deep play."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, claims can be lies, and requests reveal what a player wants. Doing well means inferring neighbours' target ranks and the Joker's location, and deciding when a claim is a bluff."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Exiting is an arithmetic check (four cards of one rank at the start of the turn). Losing is simply being one of the last two players left. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only, but there are four problems. The offer–reject–offer–reject–third chain needs up to 5 sequential choices per turn. With up to 13 players the deck runs to 53 cards and the hand state is large. There is no length cap, so the game may never end. 'Last two lose' with many players gives a ranking, not a single winner."
    }
  ],
  "problems": [
    "P1: The offer/reject/second offer/third card chain needs up to 5 sequential choice steps per turn, above the limit of 4.",
    "P2: With 3 to 13 players the deck (up to 53 cards) and hidden hand state are far too large to track, and each player only ever deals with two neighbours.",
    "P3: There is no turn limit; if nobody completes a set, the game can loop forever.",
    "P4: 'Last two lose' produces several winners and a ranking rather than one arithmetic winner, and with many players most players simply 'don't lose'.",
    "P5: The fixed deal gives the player left of the dealer a built-in first-giver role."
  ],
  "changes": [
    {
      "what": "Compress the offer chain. The giver offers TWO face-down cards at once, each with a public rank claim. The taker either picks one of them or refuses both and takes one card at random from the giver's other three cards.",
      "why": "This keeps the bluff-and-reject core, including the gamble of the blind third card, in 3 choice steps: request, offer, take.",
      "fixes": "P1: The offer/reject/second offer/third card chain needs up to 5 sequential choice steps per turn, above the limit of 4."
    },
    {
      "what": "Fix the game at 3 players, with 3 ranks of 4 cards each plus one Joker (13 cards).",
      "why": "Hand state stays small. Each player both receives from and gives to a real rival. With three ranks and three players, the players compete over who settles on which rank.",
      "fixes": "P2: With 3 to 13 players the deck (up to 53 cards) and hidden hand state are far too large to track, and each player only ever deals with two neighbours."
    },
    {
      "what": "Cap the game at 30 turns. If nobody has exited by then, an arithmetic score decides: the size of the largest same-rank group in hand, minus 2 for holding the Joker.",
      "why": "The game is guaranteed to end, and the fallback still rewards progress toward a set and getting rid of the Joker.",
      "fixes": "P3: There is no turn limit; if nobody completes a set, the game can loop forever."
    },
    {
      "what": "With 3 players, 'last two lose' becomes 'the first player to exit wins'. This is identical in spirit, since the moment one player exits the remaining two are the last two.",
      "why": "This gives a single, arithmetic winner.",
      "fixes": "P4: 'Last two lose' produces several winners and a ranking rather than one arithmetic winner, and with many players most players simply 'don't lose'."
    },
    {
      "what": "Assign seats at random, then pick at random which seat starts with 5 cards.",
      "why": "This removes any built-in seat advantage before the deal.",
      "fixes": "P5: The fixed deal gives the player left of the dealer a built-in first-giver role."
    }
  ],
  "keeps": [
    "Hidden hands with suits ignored, a single Joker that blocks exiting, and the goal of collecting four of a kind.",
    "One card passes per turn from the 5-card holder to the next player, so every player is alternately giver and taker.",
    "The giver offers face down and may claim any rank, truthfully or not.",
    "The taker may name the rank they want, giving away information.",
    "The taker may reject offers and gamble on a blind card instead.",
    "The exit rule: exactly four of one rank at the start of your turn, never with the Joker.",
    "The losers are the last players left in the game."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of the game (bluffed face-down offers, reading what a neighbour collects, dumping the Joker) is strong strategic reasoning. It only needs its offer chain compressed and its size and length bounded."
  },
  "variation": {
    "name": "Jukha Three",
    "summary": "A 3-player bluffing card-passing race. Each turn, the player holding 5 cards offers two face-down cards with rank claims to the next player. That player picks one or gambles on a blind card. The first player to start a turn holding four of a kind wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "SETUP. Use 13 cards: four each of ranks A, B and C, plus one Joker. Assign the 3 players to seats 1, 2 and 3 at random; play passes 1 -> 2 -> 3 -> 1. Pick one seat at random to be the first giver. Shuffle and deal 5 cards to the first giver and 4 to each other player. Hands are private. Each player always knows only their own hand and every public announcement.\n\nTURN ORDER. Each turn has a giver, who holds 5 cards, and a taker, the next player in seat order, who holds 4. On the first turn the giver is the first giver. After each turn, the taker of that turn becomes the giver of the next turn, and the next seat becomes the taker.\n\nEACH TURN:\n1. Exit check. If the taker's 4 cards are all the same rank (four A, four B or four C), the taker shows them and wins immediately; the game ends. The Joker never counts toward a set.\n2. Request. The taker publicly names one rank they want (A, B or C), or says 'none'. This is not binding on anyone.\n3. Offer. The giver chooses two different cards from their hand and places them face down as Offer 1 and Offer 2. For each, they publicly claim a rank (A, B, C or Joker), truthfully or not.\n4. Take. The taker chooses one of three options: take Offer 1, take Offer 2, or 'blind', which means taking one card chosen uniformly at random from the giver's three cards that were not offered. The taker then privately sees the card they received. The cards not taken stay in the giver's hand, unrevealed to anyone else.\n5. Pass. The chosen card moves from the giver's hand to the taker's hand. The taker now holds 5 cards and the giver holds 4.\n6. Advance. The turn counter goes up by 1. If it reaches 30, the game ends with the fallback scoring below. Otherwise the next turn begins, with the old taker as the new giver.\n\nFALLBACK SCORING (only if 30 turns pass with no exit). Each player reveals their hand and scores the number of cards in their largest same-rank group among A, B and C, counting at most 4. If they hold the Joker, they subtract 2. The highest score wins. If two or more players tie for the highest score, the game is a draw.\n\nNo free talk; the only public statements are requests and claims.",
    "objective": "The first player who begins their taking turn holding exactly four cards of one rank (A, B or C) wins, and the other two lose. If no one has done so after 30 turns, the single player with the highest score wins, where score = largest same-rank group (at most 4) minus 2 if holding the Joker. A tie for the top score is a draw.",
    "expected_effect": "With three ranks and three players, each player has to settle on a rank while hiding which one from neighbours who can starve them of it. The giver uses two claimed offers to dump the Joker and unwanted ranks while withholding what the taker requested. The taker weighs the giver's past honesty, which they learn privately each time they see a taken card, against the blind gamble. Requests trade information for help, since an honest request tells the giver what to withhold. Any simple policy can lose:\n- Always taking Offer 1 lets a liar route the Joker to you.\n- Always going blind ignores everything you know.\n- Always telling the truth lets the taker avoid your dumps.\n- Always requesting your true rank invites denial.\nTalk is deliberately left out: requests and claims already carry all the useful signalling, and free chat would only repeat them."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 10,
    "choice_steps_per_round": 3,
    "attributes": 14,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 30
  }
}
```
````
