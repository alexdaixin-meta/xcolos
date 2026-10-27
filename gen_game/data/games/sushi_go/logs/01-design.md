# 01 design

- time: 2026-10-27T16:38:15+00:00 (73.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c6273e877b90016e, reply sha256 66fa8aaf6b08917c

## Sent

````
Original game: Sushi Go
Players in the original: 2 to 5

Original rules:
Shuffle 108 sushi cards and deal hands: 10 cards for 2 players, 9 for 3, 8 for 4, 7 for 5. Game lasts 3 rounds. Each turn all players simultaneously choose 1 card from hand to keep face down, then reveal. Keep cards face up in front of you. Pass remaining hand left and repeat until hands are empty; last card is placed automatically. Wasabi multiplies next nigiri placed on it x3. Chopsticks in front can be used once per turn to pick 2 cards from hand instead of 1, then chopsticks returns to hand. After round score: maki icons - most 6 pts, second most 3 pts, ties split remainder ignored; tempura pair 5; sashimi triple 10; dumplings score 1/3/6/10/15 for 1-5+; nigiri squid 3 salmon 2 egg 1 triple if on wasabi. Discard all except pudding which is kept. Deal new hands. After 3 rounds score puddings: most 6, fewest -6, split ties, no penalty in 2p. Highest total wins, tie break most puddings.
````

## Reply

````
```json
{
  "original_summary": "Sushi Go is a 2-5 player card-drafting game over 3 hands. Each turn everyone secretly keeps one card from their hand and passes the rest to the left. Sets of sushi (tempura, sashimi, dumplings, maki, nigiri with wasabi, pudding) score by arithmetic, and the highest total after 3 hands wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies all lose to adaptive play. 'Always take the card worth the most points right now' ignores sets: half a tempura pair or one sashimi scores 0. 'Always chase sashimi' gives 0 when a neighbour takes the third copy. 'Always take dumplings' depends on how many others want them. 'Always grab maki' splits the 6 points when contested. 'Ignore pudding' risks -6. Seats are symmetric because every hand rotates past every player."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Drafting greatly reduces deal luck, since you see most hands in the round. Still, the shuffle decides which sets are available, and with 4-5 players a weaker player's choices change what the stronger player is passed, which adds noise. Chopsticks adds a swingy extra pick. Skill wins over a series but not every game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A beginner who collects obvious sets still scores 20-30 points per hand. Strong play adds several layers: remembering hands already seen, predicting what the left neighbour will take, denying sets ('hate drafting'), timing wasabi, and judging the maki and pudding majorities across hands."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, but you have seen earlier versions of the hands now held by others. You must infer what is still circulating, model which cards each neighbour needs from their face-up cards, and plan over the hand (will a third sashimi come back?) and over the game (pudding majority)."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every score comes from counts of cards: set sizes, majority comparisons and multipliers. No judgement is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based, text-only and uses no board. However, chopsticks needs a second pick inside a turn and a card returned into a hand that is being passed, which is a conditional extra block of steps. The 2-player variant needs a special pudding rule. With 5 players there are many steps per player, and hand sizes change with player count."
    }
  ],
  "problems": [
    "P1: Chopsticks needs a conditional second pick within a turn and returns the card into the hand being passed, which the flat step list cannot express cleanly. It also adds swingy extra picks.",
    "P2: The 2-player game needs a special no-penalty pudding rule, and in 2 players the highest-total rule makes play pure hate-drafting. The 5-player game adds noise from passing chains and almost uses up the deck.",
    "P3: The rules are vague in places: maki tie-breaking beyond the split, what happens when a wasabi never gets a nigiri, how ties for fewest pudding work, and how a final tie is resolved after the pudding tie-break.",
    "P4: Pick order and hand-size bookkeeping vary with player count, which raises build complexity and the number of steps.",
    "P5: Moderate luck from the shuffle and from passing chains weakens how reliably skill decides the winner."
  ],
  "changes": [
    {
      "what": "Remove chopsticks from the deck (104 cards remain, with the original proportions of everything else).",
      "why": "Every turn becomes exactly one simultaneous pick, so no conditional block of steps is needed. A swingy luck source disappears.",
      "fixes": "P1: Chopsticks needs a conditional second pick within a turn and returns the card into the hand being passed, which the flat step list cannot express cleanly. It also adds swingy extra picks."
    },
    {
      "what": "Restrict the game to 3 or 4 players (4 suggested): 9-card hands for 3 players and 8-card hands for 4.",
      "why": "This avoids the special 2-player pudding rule and the degenerate head-to-head denial game. It keeps the deck sufficient and the number of rounds at 27 or fewer. With 4 players every hand passes each player twice, which rewards memory and inference.",
      "fixes": "P2: The 2-player game needs a special no-penalty pudding rule, and in 2 players the highest-total rule makes play pure hate-drafting. The 5-player game adds noise from passing chains and almost uses up the deck."
    },
    {
      "what": "Spell out every scoring edge case: maki ties, unused wasabi, pudding ties including the case where all are tied, players with zero cards, and a final tie-break chain ending in a shared draw.",
      "why": "The winner must follow by arithmetic with no interpretation left to a referee.",
      "fixes": "P3: The rules are vague in places: maki tie-breaking beyond the split, what happens when a wasabi never gets a nigiri, how ties for fewest pudding work, and how a final tie is resolved after the pudding tie-break."
    },
    {
      "what": "Make each engine round one pick turn with a fixed sequence of steps. Hands are dealt only on the first pick of each hand (the single random draw that round). Set scoring happens only on the last pick of each hand, and pudding scoring only on the last pick of the game.",
      "why": "This keeps the game to one choice, one random draw and about 17 steps per round, with conditions only on single steps.",
      "fixes": "P4: Pick order and hand-size bookkeeping vary with player count, which raises build complexity and the number of steps."
    },
    {
      "what": "Each turn, publicly announce every player's face-up cards and the number of cards in each hand. Privately show each player their current hand.",
      "why": "Players have everything needed to reason about neighbours' needs. Skill then shows in inference and denial rather than in tracking bookkeeping, which reduces noise from misreading the state.",
      "fixes": "P5: Moderate luck from the shuffle and from passing chains weakens how reliably skill decides the winner."
    }
  ],
  "keeps": [
    "Simultaneous secret pick from a hidden hand, then pass the rest to the left",
    "Three hands with puddings carried across hands",
    "All original sushi scoring: tempura pairs, sashimi triples, the dumpling ladder, maki majorities, nigiri values tripled by wasabi, and the pudding majority and minority",
    "The original card proportions",
    "Highest total wins, with puddings as the tie-break"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core drafting loop is already a strong hidden-information, opponent-modelling game. It needs only the removal of chopsticks, fixed player counts and fully specified scoring to fit the engine."
  },
  "variation": {
    "name": "Sushi Draft",
    "summary": "A 3-4 player Sushi Go without chopsticks. Over three hands, players secretly keep one card at a time from a hidden hand and pass the rest left, building scoring sets while reading and denying their neighbours.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "DECK (104 cards): 14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1 (1 maki icon), 12 Maki-2 (2 icons), 8 Maki-3 (3 icons), 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi.\n\nSETUP: Shuffle the deck once at the start of the game. Every player starts with a score of 0 and 0 puddings. The game has 3 hands. Each hand has 9 picks with 3 players or 8 picks with 4 players, so the game lasts 27 or 24 rounds. One round is one pick.\n\nEACH ROUND:\n1. Deal (first pick of a hand only): deal each player a hand from the top of the deck, 9 cards with 3 players or 8 cards with 4 players. Undealt cards stay hidden and are not reshuffled.\n2. Announce: everyone is told every player's face-up cards for this hand, every player's pudding count and score, and how many cards each hand holds. Each player is shown privately the cards in their own current hand.\n3. Pick: all players at the same moment secretly choose one card from their own hand. If a hand holds one card, that card is taken automatically.\n4. Reveal: all chosen cards are revealed at once and placed face up in front of their owners.\n5. Record the chosen card:\n   - Tempura adds 1 to your tempura count.\n   - Sashimi adds 1 to your sashimi count.\n   - Dumpling adds 1 to your dumpling count.\n   - Maki adds its icons (1, 2 or 3) to your maki total.\n   - Pudding adds 1 to your puddings, which are kept across all hands.\n   - Wasabi adds 1 to your unused wasabi.\n   - Nigiri is worth 1 (Egg), 2 (Salmon) or 3 (Squid). If you have at least 1 unused wasabi, the nigiri is placed on it: its value is tripled (3, 6 or 9) and your unused wasabi drops by 1. Add the nigiri's value to your nigiri points for this hand.\n6. Pass: everyone passes their remaining hand to the player on their left.\n7. Hand scoring (last pick of a hand only). Each player adds the following to their score:\n   - Tempura: 5 points per complete pair, so floor(tempura/2) x 5.\n   - Sashimi: 10 points per complete set of three, so floor(sashimi/3) x 10.\n   - Dumplings: 0 for 0, 1 for 1, 3 for 2, 6 for 3, 10 for 4, and 15 for 5 or more.\n   - Nigiri: all nigiri points for the hand. Unused wasabi scores 0.\n   - Maki: among players with a maki total of at least 1, those with the highest total split 6 points equally, rounded down. If exactly one player has the highest total, the players with the second-highest total (at least 1) split 3 points equally, rounded down. If two or more players tie for highest, no second-place points are awarded.\n   Then every hand-only count (tempura, sashimi, dumplings, maki, unused wasabi, nigiri points) resets to 0. Puddings stay.\n8. Pudding scoring (last pick of the third hand only):\n   - Players with the most puddings split +6 equally, rounded down.\n   - Players with the fewest puddings split -6 equally, rounded toward zero (for example, two tied players get -3 each).\n   - Players with 0 puddings count for the fewest.\n   - If all players have the same number of puddings, nobody scores for pudding.\n9. End check: after the last pick of the third hand, the game ends.\n\nThere is no talk phase.",
    "objective": "After pudding scoring, the player with the highest score wins. If two or more players tie for the highest score, the one among them with the most puddings wins. If they are still tied, the game is a draw among those players.",
    "expected_effect": "Every turn is a choice that takes thought. Players weigh a card's value to their own sets against denying it to the left neighbour, who sees their hand next. They must remember which cards were in hands seen earlier to judge whether a missing tempura or third sashimi will come back around, and read neighbours' face-up cards to predict their picks. They must also balance the cross-hand pudding race against immediate points. Simple policies lose: grabbing the highest-value card leaves incomplete sets, chasing a single set is easily blocked, and ignoring pudding costs 6. Removing chopsticks and fixing 3-4 players makes the game buildable and slightly less luck-driven. Talk is left out: all picks are revealed anyway, and cheap claims about intentions would add words without a commitment worth testing."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 1,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 27
  }
}
```
````
