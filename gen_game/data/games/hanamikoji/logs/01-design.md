# 01 design

- time: 2026-10-27T09:43:32+00:00 (87.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5d6a14f1d171d655, reply sha256 3c88418e28a63af2

## Sent

````
Original game: Hanamikoji
Players in the original: 2 to 2

Original rules:
Two players compete for 7 Geisha cards. Each Geisha has a Charm value and a set of Item cards (total 21 Items across types). First to win 4 Geisha or 11+ Charm points from won Geisha wins; 11 Charm beats 4 Geisha if both achieved same scoring.
Each round: shuffle 21 Items, secretly remove 1 card from play, deal 6 cards each as hidden hands, remaining 8 form a deck. Players alternate turns for 4 turns each: draw 1 from deck, then use one unused Action marker. Secret: set aside 1 hand card face-down for final scoring. Trade-off: set aside 2 hand cards face-down discarded this round. Gift: reveal 3 hand cards, opponent takes 1 to his side, you keep 2. Competition: reveal 4 hand cards as two pairs of 2, opponent chooses one pair, you keep the other. All kept cards are placed by their Geisha. After 8 turns, reveal Secret cards and compare counts per Geisha: higher count wins that Geisha and moves its Victory Marker; ties leave marker. If winning goal met, game ends. Otherwise collect all Item cards, retain Victory Markers, flip Action markers up, swap starting player, and start new round.
````

## Reply

````
```json
{
  "original_summary": "Hanamikoji is a two-player card game of hidden hands and divide-and-choose. Over repeated hands, players play Item cards to seven Geisha using four one-shot actions: Secret, Trade-off, Gift and Competition. The goal is to win 4 Geisha or 11 Charm, and when both reach a goal, 11 Charm beats 4 Geisha.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy dominates. 'Always play Competition first' reveals 4 cards early and lets the opponent take the best pair, while hiding the hand's shape for later. 'Always offer your best cards' hands the opponent the key Geisha. 'Always Secret first' commits blindly before seeing what the opponent wants. The starting player alternates between hands, and 7 Geisha with 21 Charm in total means only one player can reach each goal."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "The deal matters, but divide-and-choose lets the weaker hand limit the damage. Splitting a Gift or Competition so that every option is acceptable, and reading what the opponent's earlier picks reveal, decides most games. Strong players beat casual ones consistently."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Play improves with card counting (21 known Items, 1 removed, discards hidden), timing actions and building splits the opponent cannot exploit. A weak player still wins some Geisha from what they are dealt and from opponent mistakes."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, one card is removed unseen, Secret and Trade-off cards are face-down, and marker states carry between hands. Players must infer what the opponent holds from public placements and the cards still unaccounted for, and plan the order of four actions across a hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Each Geisha goes to whoever placed more cards on it, and the win check is a sum of Charm values and a count of markers. All of it is arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is turn-based and text-only, but one hand has 8 turns, each with up to two choices (16 choice steps against a limit of 4). Per-Geisha counts for two players plus markers would be 21+ attributes if stored one number each. A draw every turn looks like many random events. Ties can leave markers unchanged indefinitely, so there is no guaranteed end."
    }
  ],
  "problems": [
    "A full hand (8 turns, each with an action choice and sometimes an opponent pick) far exceeds 4 choice steps per engine round.",
    "Tracking 7 Geisha separately for each player, plus 7 markers, as individual numbers exceeds the 20-attribute limit.",
    "A draw on every turn reads as a random draw per turn, and resetting and dealing inside the same structure risks more than one chance event per round.",
    "The game has no length cap: repeated tied Geisha can leave the goals unmet hand after hand, which fails 'short enough to play' and fixed-round limits.",
    "Illegal or malformed card selections by a model have no defined handling."
  ],
  "changes": [
    {
      "what": "One engine round equals one turn of Hanamikoji (one action). A hand is 8 consecutive rounds, and set-up and scoring steps fire only on the first and last turn of a hand, using `when` conditions.",
      "why": "Each round then has at most 2 choice steps: the active player's action and the opponent's pick for Gift or Competition.",
      "fixes": "A full hand (8 turns, each with an action choice and sometimes an opponent pick) far exceeds 4 choice steps per engine round."
    },
    {
      "what": "Store each player's placed cards as one list of 7 counts and the markers as one list of 7 entries. Merge the removed card and Trade-off discards into one hidden out-of-play pile.",
      "why": "This brings the state to 19 attributes while keeping all 7 Geisha.",
      "fixes": "Tracking 7 Geisha separately for each player, plus 7 markers, as individual numbers exceeds the 20-attribute limit."
    },
    {
      "what": "Shuffle once at the start of each hand. The removed card, both hands and the ordered deck all come from that single shuffle, and each turn's draw takes the top card of the already-shuffled deck.",
      "why": "This gives one chance event per hand, inside the limit of one per round.",
      "fixes": "A draw on every turn reads as a random draw per turn, and resetting and dealing inside the same structure risks more than one chance event per round."
    },
    {
      "what": "Cap the game at 4 hands (32 rounds), with a tiebreak: more Charm from held markers, then more Geisha held, then a draw.",
      "why": "This guarantees an end. An even number of hands gives each player the last move equally often (2 hands each), so the cap adds no seat edge.",
      "fixes": "The game has no length cap: repeated tied Geisha can leave the goals unmet hand after hand, which fails 'short enough to play' and fixed-round limits."
    },
    {
      "what": "Define a default for any illegal selection: the lowest-numbered unused action, filled with the first cards of the hand in hand order; for an opponent's pick, option 1.",
      "why": "The engine can always continue deterministically.",
      "fixes": "Illegal or malformed card selections by a model have no defined handling."
    }
  ],
  "keeps": [
    "Seven Geisha with Charm 2,2,2,3,3,4,5 and 21 Items, one per Charm point.",
    "Removing one card face-down per hand, a 6-card hand each, an 8-card deck and a draw before each action.",
    "All four one-shot actions: Secret, Trade-off, Gift and Competition, including divide-and-choose.",
    "Majority per Geisha wins its marker, ties leave the marker where it is, and markers carry over between hands.",
    "The win at 11 Charm or 4 Geisha, with Charm taking precedence, checked at the end of each hand.",
    "The starting player alternates between hands."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The original is already a strong hidden-information reasoning game. It needs restructuring (one engine round per turn, list state, a length cap) to fit the engine, not redesign."
  },
  "variation": {
    "name": "Hanamikoji: Turn by Turn",
    "summary": "Two players court seven Geisha by playing Item cards through four one-shot actions, two of which are divide-and-choose offers. Majorities win Geisha markers that persist across up to four hands. The first player to 11 Charm or 4 Geisha wins.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS\n- Seven Geisha, G1 to G7, with Charm values G1=2, G2=2, G3=2, G4=3, G5=3, G6=4, G7=5 (21 in total).\n- 21 Item cards. Each Geisha has as many Items as her Charm value: two G1, two G2, two G3, three G4, three G5, four G6, five G7.\n- Each Geisha has a marker that is Neutral, on Player A's side, or on Player B's side. All markers start Neutral.\n- Each player has four action tokens: Secret, Trade-off, Gift, Competition.\n\nSTRUCTURE\n- The game has at most 4 hands. Each hand has 8 turns, alternating between players, so each player takes 4 turns per hand.\n- Player A takes the first turn of hands 1 and 3. Player B takes the first turn of hands 2 and 4.\n- One engine round is one turn, so the game lasts at most 32 rounds.\n\nSTART OF EACH HAND (first turn of the hand only)\n1. Shuffle all 21 Items.\n2. Put the top card face-down in the out-of-play pile. Nobody sees it, ever.\n3. Deal 6 cards to each player as a private hand. The remaining 8 cards form the deck, in shuffled order.\n4. Each player gets back all four action tokens.\n5. Every player's placed counts are reset to 0 for all seven Geisha. Markers are NOT reset.\n\nEACH TURN\n1. The active player takes the top card of the deck into their hand.\n2. Both players are shown the public state: markers, both players' placed counts per Geisha, each player's unused actions, the hand number and the turn number. Each player privately sees their own hand.\n3. The active player chooses one unused action and the cards for it:\n   - SECRET: choose 1 card. It is set aside face-down as your secret card for this hand.\n   - TRADE-OFF: choose 2 cards. They go face-down into the out-of-play pile, unseen by the opponent, and never score.\n   - GIFT: choose 3 cards and reveal them.\n   - COMPETITION: choose 4 cards and reveal them, arranged as Pair 1 (two cards) and Pair 2 (two cards).\n4. If the action was Gift: the opponent chooses 1 of the 3 revealed cards. That card is placed on the opponent's side of its Geisha, and the other 2 go on the active player's side of their Geisha.\n5. If the action was Competition: the opponent chooses Pair 1 or Pair 2. The chosen pair goes on the opponent's side, and the other pair goes on the active player's side.\n6. Each placed card adds 1 to its owner's placed count for that card's Geisha. Placed cards are public.\n7. The used action token is spent for this hand.\n8. ILLEGAL CHOICES: if the active player names a spent action, a card they do not hold, or the wrong number of cards, the engine instead uses their lowest-numbered unused action (order: Secret, Trade-off, Gift, Competition) filled with the first cards of their hand in hand order. If an opponent's Gift or Competition pick is invalid, option 1 (the first card, or Pair 1) is used.\n\nEND OF EACH HAND (after the 8th turn only)\n1. Both secret cards are revealed and added to their owners' placed counts.\n2. For each Geisha, compare the two players' placed counts:\n   - The player with the higher count moves that Geisha's marker to their side.\n   - On a tie the marker stays where it is.\n3. For each player, compute Geisha held (the number of markers on their side) and Charm held (the sum of Charm values of those Geisha).\n4. Win check:\n   - If a player has Charm held of 11 or more, that player wins immediately. Only one player can, since the total Charm is 21.\n   - Otherwise, if a player has 4 or more Geisha held, that player wins. Only one player can, since there are 7 Geisha.\n5. If nobody has won and this was hand 4, the game ends and the tiebreak decides.\n6. Otherwise the next hand begins, with the other player starting.\n\nINFORMATION\n- Public: placed cards, revealed Gift and Competition cards, markers, and spent actions.\n- Private: each hand (to its owner), and each secret card (to its owner, until the hand ends).\n- Never revealed: the removed card and Trade-off cards.\n- Players may use the known composition of the 21 Items to deduce what is still unaccounted for.",
    "objective": "After each hand, a player whose Geisha markers total 11 or more Charm wins. Otherwise, a player holding 4 or more Geisha markers wins. If neither has happened after hand 4, the player with the higher Charm held wins. If Charm is equal, the player with more Geisha held wins. If both are equal, the game is a draw.",
    "expected_effect": "Play should look like the original Hanamikoji. Players time their four actions, split Gifts and Competitions so every option costs the opponent something, and count cards to deduce the removed card, discards and the opponent's hand. Defending markers won in earlier hands adds planning across hands. The single shuffle per hand matters, but divide-and-choose keeps the outcome in the players' hands. The 4-hand cap with an even split of last moves keeps the seats balanced. Talk is omitted because this is a strictly zero-sum two-player game, where messages would add only noise."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 32
  }
}
```
````
