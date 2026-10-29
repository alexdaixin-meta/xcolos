# 01 design

- time: 2026-10-28T05:47:51+00:00 (59.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 d33cd217fab392f0, reply sha256 a0418ce93859864c

## Sent

````
Original game: Cat Lady
Players in the original: 2 to 4

Original rules:
Shuffle game cards (trimmed by player count: remove 3+ and 4 marks for 2 players, 4 marks for 3 players, plus 2 random cards for 2-3 players) as main deck and 13 stray cats as separate deck. Deal 9 cards face up as 3x3 grid and 3 stray cats face up. Place food cubes and cat blocking token aside. On your turn you must take all 3 cards from one row or column not blocked by the cat token. Resolve cards: cats stay in front of you, toys go to hand for set scoring, food cubes are taken and discarded cards replaced by cubes, costumes, catnip etc score, Lost Cat and Spray Bottle may be played anytime on your turn to claim strays or steal. After taking, move cat token to the row/column you took and refill those 3 spots from main deck. Continue clockwise until the deck cannot refill a row or column. Then apply -2 VP to player(s) with most leftover food, sum VP from fed cats, stray cats, costumes, catnip sets, toy sets, tokens and penalties. Highest total wins, tie-break most fed cats.
````

## Reply

````
```json
{
  "original_summary": "Cat Lady is a 2-4 player card-drafting game. On each turn a player takes a row or column of three face-up cards from a 3x3 grid that a blocking token restricts. Players collect cats and the food to feed them, along with toys, catnip, costumes and strays, and the highest victory-point total wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed policy works. 'Always take the most cats' ends with unfed cats and no food, and 'always take food' ends with the leftover-food penalty and few points. The blocking token stops anyone repeating the same pick, and turn order rotates naturally. The first player has only a mild edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Balancing food against cats, timing set collection and leaving poor lines for the next player reliably beat naive drafting. The refill draws add some noise, but everyone drafts from the same shared market, which limits luck."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still score from whatever they draft. Strong players can keep improving through hate-drafting, tempo and reading what the next player needs."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Almost everything is face up. The only hidden things are the deck order and a few held cards, so there is little to infer about opponents beyond reading their visible tableaus."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is arithmetic: fed cats, sets, catnip counts and the food penalty."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The core choice is a row or column of a 3x3 grid with a positional blocking token, which is a spatial board. The game also has many card types with special timings (Lost Cat, Spray Bottle, costumes, cube replacement), which far exceeds the step and attribute limits."
    }
  ],
  "problems": [
    "The 3x3 grid with row/column selection and the blocking token is a spatial board, which the platform excludes.",
    "There are too many card types and anytime-play effects (Lost Cat, Spray Bottle, costumes, cube replacement, separate stray deck) to build within 20 steps and 20 attributes.",
    "Almost all information is public, so there is little inference or opponent modelling.",
    "Refilling individual grid spots means many random draws per turn, while the platform allows one draw per round.",
    "Running until the deck cannot refill gives a variable game length, and the trimmed deck depends on player count, which is fiddly to build."
  ],
  "changes": [
    {
      "what": "Replace the grid with a market of numbered lots of 2 cards each, dealt fresh every round. Players take whole lots in turn, and the untaken lot is discarded.",
      "why": "This keeps the drafting choice of taking a bundle and leaving the rest for others, without any spatial structure.",
      "fixes": "The 3x3 grid with row/column selection and the blocking token is a spatial board, which the platform excludes."
    },
    {
      "what": "Cut the card types to six: Food 1, Food 2, Cat (needs 2 food), Stray Cat (already fed), Toy in three colours, and Catnip. All scoring happens at the end and nothing can be played at any time.",
      "why": "These keep the food-versus-cats tension and the set collection while fitting the step and attribute limits.",
      "fixes": "There are too many card types and anytime-play effects (Lost Cat, Spray Bottle, costumes, cube replacement, separate stray deck) to build within 20 steps and 20 attributes."
    },
    {
      "what": "Deal each player a secret Favourite (Cats, Toys, Catnip or Strays) that gives bonus points for that category. Favourites are revealed only at final scoring.",
      "why": "Players must infer rivals' favourites from their picks so they can deny the right lots, and must hide their own by drafting with some ambiguity. The favourite changes what to draft without being worth more in total.",
      "fixes": "Almost all information is public, so there is little inference or opponent modelling."
    },
    {
      "what": "Use a fixed 96-card deck, shuffled once. Each round's whole market is dealt in one draw.",
      "why": "This means one random draw per round.",
      "fixes": "Refilling individual grid spots means many random draws per turn, while the platform allows one draw per round."
    },
    {
      "what": "Fix the game length (12 rounds for 3 players, 9 for 4) and rotate the first picker every round.",
      "why": "The length is now predictable, all cards are used, and each seat picks first an equal number of times.",
      "fixes": "Running until the deck cannot refill gives a variable game length, and the trimmed deck depends on player count, which is fiddly to build."
    }
  ],
  "keeps": [
    "Drafting bundles from a shared face-up market, where what you leave matters as much as what you take.",
    "Cats must be fed with food: unfed cats hurt you, and hoarding food is penalised (-2 for the most leftover food).",
    "Strays as an already-fed cat source.",
    "Toy colour sets and escalating catnip sets.",
    "Highest victory-point total wins, with most fed cats as the tie-break."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The drafting and feeding core survives once the grid becomes a set of lots, and a secret favourite adds the inference the original lacks, all within the limits."
  },
  "variation": {
    "name": "Cat Lady: Secret Favourites",
    "summary": "Players take turns drafting 2-card lots from a fresh market each round. They collect and feed cats, gather toy sets and catnip, and chase a secret favourite category while guessing and blocking their rivals' favourites.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "SETUP. The deck has 96 cards: 18 Food-1 (1 food each), 10 Food-2 (2 food each), 20 Cat, 8 Stray Cat, 24 Toy (8 Red, 8 Blue, 8 Green) and 16 Catnip. Shuffle the deck once. Each player is secretly dealt one Favourite card. With 3 players the Favourites are drawn from {Cats, Toys, Catnip}; with 4 players they are drawn from {Cats, Toys, Catnip, Strays}. Every player gets a different Favourite, and only its owner knows it. Seat the players in a fixed order.\n\nROUNDS. With 3 players there are 12 rounds; with 4 players there are 9. In round r, the first picker is seat ((r-1) mod number of players) + 1, and the others follow in seat order.\n\nEACH ROUND.\n1. Deal the market from the top of the deck. With 3 players deal 4 lots (Lot A to Lot D) of 2 cards each; with 4 players deal 5 lots (A to E). Announce every lot's contents to all players.\n2. Starting with the first picker, each player in turn chooses one remaining lot by its letter. Each player sees all earlier picks.\n3. A chosen lot goes to that player at once. Food cards add their food value to the player's food total. Cats, Strays, Toys (by colour) and Catnip are added to the player's counts. Everything a player owns is public, except their Favourite.\n4. When every player has picked, the one leftover lot is discarded.\n5. If this was the last round, go to final scoring.\n\nFINAL SCORING. For each player:\n- Feeding: each Cat needs 2 food. The number of fed cats is the smaller of the player's Cats and (food ÷ 2, rounded down). Each fed cat scores 5 and each unfed Cat scores -1. Leftover food is the food total minus 2 × fed cats.\n- Strays: each Stray Cat scores 3.\n- Toys: each Toy scores 1, plus 4 for each complete set of one Red, one Blue and one Green (number of sets = the smallest of the three colour counts).\n- Catnip: with n Catnip cards the player scores n(n+1)/2, counting at most 6 cards (maximum 21). Catnip beyond 6 scores nothing.\n- Food penalty: the player or players with the most leftover food lose 2 points, provided that amount is at least 1.\n- Favourite bonus, revealed now: Cats gives +2 per fed cat; Toys gives +1 per Toy card; Catnip gives +1 per Catnip card, including any beyond 6; Strays gives +2 per Stray Cat.",
    "objective": "The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.",
    "expected_effect": "Players must balance food against cats, decide when to commit to toy sets or catnip, and choose what to leave behind. They will watch rivals' picks to infer their Favourites, for example a rival grabbing every Catnip lot, and deny those lots late in the draft, while blurring their own signals. The single shared market and the rotating first pick keep luck and seat advantage small. There is no talk phase. The players' interests conflict, but there is nothing to bargain over and no binding trades, so messages would mostly be cheap bluffs about Favourites that add words rather than decisions."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 4,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
