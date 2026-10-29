# 03 design

- time: 2026-10-28T05:49:50+00:00 (45.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 04448dc11523005e, reply sha256 c09dc6c7b4b7b902

## Sent

````
Original game: Cat Lady
Players in the original: 2 to 4

Original rules:
Shuffle game cards (trimmed by player count: remove 3+ and 4 marks for 2 players, 4 marks for 3 players, plus 2 random cards for 2-3 players) as main deck and 13 stray cats as separate deck. Deal 9 cards face up as 3x3 grid and 3 stray cats face up. Place food cubes and cat blocking token aside. On your turn you must take all 3 cards from one row or column not blocked by the cat token. Resolve cards: cats stay in front of you, toys go to hand for set scoring, food cubes are taken and discarded cards replaced by cubes, costumes, catnip etc score, Lost Cat and Spray Bottle may be played anytime on your turn to claim strays or steal. After taking, move cat token to the row/column you took and refill those 3 spots from main deck. Continue clockwise until the deck cannot refill a row or column. Then apply -2 VP to player(s) with most leftover food, sum VP from fed cats, stray cats, costumes, catnip sets, toy sets, tokens and penalties. Highest total wins, tie-break most fed cats.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: CARD VALUES (base, then with Favourite). Stray: 3 flat, needs nothing (5 with Strays fav). Catnip: marginal 1,2,3,4,5,6, so 6 cards = 21 (3.5/card); beyond 6 = 0 (+1/card with Catnip fav). Toy: 1/card + 4 per R/B/G set, so 3 cards = 7 (2.33/card; 3.33 with Toys fav). Cat: needs 2 food, fed = 5, unfed = -1. Cat + Food-2 = 5 for 2 cards (2.5/card); Cat + 2xFood-1 = 5 for 3 cards (1.67/card); with Cats fav 7. Food is scarce: total food = 18x1 + 10x2 = 38 against 20 Cats needing 40, so at most 19 fed cats exist. Card counts work out: 3p is 12 rounds x 8 = 96 (the whole deck); 4p is 9 x 10 = 90.

THOUGHTLESS POLICIES (winner rule). Lots are random 2-card bundles, so no lot letter is ever strictly better. 'Always earliest remaining letter' and 'always latest letter' each take an effectively random lot. Against a greedy drafter (best lot by the values above), they lose most games, because the greedy player completes catnip runs and toy sets while the fixed-letter player accumulates unfed cats (-1) and is likely to take the food penalty. They also give no edge against random play. 'Always most catnip': catnip's increasing marginal value makes it a commitment. Two chasers split 16 cards (about 8 each, with the last 2 worth 0), and the policy ignores Strays (3 flat), so it can be beaten. 'Always most points now' is not dominant either, because it ignores feeding dependencies and hate-drafting. There is no strictly dominant option and no never-lose policy, and every player can realistically win.

SEAT ORDER (fails). 3p: 12 rounds / 3 gives each seat 4 firsts, 4 seconds and 4 thirds, which is symmetric. 4p: 9 rounds is not divisible by 4. The first picker by round is S1, S2, S3, S4, S1, S2, S3, S4, S1, and the last picker is S4, S1, S2, S3, S4, S1, S2, S3, S4. So S1 picks first 3 times and last 2 times, while S4 picks first 2 times and last 3 times. Choosing first from 5 lots rather than last from 2 is worth roughly 2-4 points per round. In a game with totals around 40-60, a structural edge of about 4-8 points for S1 over S4 is a move-order edge built into the rules.

FAVOURITES. They are roughly comparable: Cats about +10-12 (5-6 fed cats), Toys about +8-10 (a category others value less), Catnip about +6-7 (heavily contested), Strays about +6-8 in 4p. They are not decisive, but Cats/Toys are somewhat stronger than Catnip.
- change: Balanced: make the 4-player game a multiple of 4 rounds so every seat picks first, second, third and last equally often. Use 8 rounds of 5 lots (80 of 96 cards), or alternatively 12 rounds with 5 lots of 2 drawn from a 120-card deck scaled proportionally. Update stated complexity if rounds change.
- change: Optional for balance: narrow the gap between Favourites, for example Catnip fav +2 per Catnip card beyond the 3rd, or Cats fav +2 per fed cat capped at 10, so that the random Favourite deal is closer to even.
The variation that was reviewed: Cat Lady: Secret Favourites: SETUP. The deck has 96 cards: 18 Food-1 (1 food each), 10 Food-2 (2 food each), 20 Cat, 8 Stray Cat, 24 Toy (8 Red, 8 Blue, 8 Green) and 16 Catnip. Shuffle the deck once. Each player is secretly dealt one Favourite card. With 3 players the Favourites are drawn from {Cats, Toys, Catnip}; with 4 players they are drawn from {Cats, Toys, Catnip, Strays}. Every player gets a different Favourite, and only its owner knows it. Seat the players in a fixed order.

ROUNDS. With 3 players there are 12 rounds; with 4 players there are 9. In round r, the first picker is seat ((r-1) mod number of players) + 1, and the others follow in seat order.

EACH ROUND.
1. Deal the market from the top of the deck. With 3 players deal 4 lots (Lot A to Lot D) of 2 cards each; with 4 players deal 5 lots (A to E). Announce every lot's contents to all players.
2. Starting with the first picker, each player in turn chooses one remaining lot by its letter. Each player sees all earlier picks.
3. A chosen lot goes to that player at once. Food cards add their food value to the player's food total. Cats, Strays, Toys (by colour) and Catnip are added to the player's counts. Everything a player owns is public, except their Favourite.
4. When every player has picked, the one leftover lot is discarded.
5. If this was the last round, go to final scoring.

FINAL SCORING. For each player:
- Feeding: each Cat needs 2 food. The number of fed cats is the smaller of the player's Cats and (food ÷ 2, rounded down). Each fed cat scores 5 and each unfed Cat scores -1. Leftover food is the food total minus 2 × fed cats.
- Strays: each Stray Cat scores 3.
- Toys: each Toy scores 1, plus 4 for each complete set of one Red, one Blue and one Green (number of sets = the smallest of the three colour counts).
- Catnip: with n Catnip cards the player scores n(n+1)/2, counting at most 6 cards (maximum 21). Catnip beyond 6 scores nothing.
- Food penalty: the player or players with the most leftover food lose 2 points, provided that amount is at least 1.
- Favourite bonus, revealed now: Cats gives +2 per fed cat; Toys gives +1 per Toy card; Catnip gives +1 per Catnip card, including any beyond 6; Strays gives +2 per Stray Cat. Winner: The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Cat Lady is a 2-4 player card-drafting game. Players take rows or columns from a 3x3 market of cards and collect cats that must be fed with food, plus toys (scored in sets), catnip (scored on an increasing scale), stray cats and other cards. Highest victory points wins. The previously reviewed variation replaced the grid with a market of 2-card lots drafted in rotating seat order, and added one secret Favourite per player.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "No simple policy wins. 'Always earliest letter' and 'always latest letter' take effectively random lots, collect unfed cats at -1 and attract the food penalty, so they lose to a greedy drafter. 'Always most catnip' splits 16 cards with any other chaser and ignores Strays. 'Always most points now' ignores feeding dependencies. However, the 4-player game ran 9 rounds, so seat 1 picked first 3 times and last 2 times while seat 4 did the reverse. Picking first from 5 lots instead of last from 2 is worth about 2-4 points, which gave seat 1 an edge of about 4-8 points in totals of 40-60. That is a built-in seat edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Lot contents are public before anyone picks. Values depend on what a player already holds (food against cats, toy colours, the catnip curve) and on what rivals need. The skilled drafter plans feeding, completes sets and hate-drafts. Randomness lies only in which lots appear, and every player faces the same market."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player still scores through Strays (3 flat) and loose toys. A strong player can keep improving through timing, denial and reading Favourites from rivals' picks. Food scarcity (38 food for 20 cats) makes feeding a real planning problem."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's secret Favourite changes what they value, so players must infer rivals' Favourites from their picks to predict and deny. Planning across rounds matters for feeding, the catnip curve and toy sets. The Favourite gap was a minor lottery element: Cats was worth about +10-12 and Catnip about +6-7."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Every score is arithmetic on public counts plus a revealed Favourite. The winner and tie-break are numeric."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is text-only, sequential picks are turn-based, and there is no board. It uses one hidden element, one market deal per round, at most 4 choice steps per round and at most 12 rounds."
    }
  ],
  "problems": [
    "P1: In the 4-player game, 9 rounds cannot be split evenly over 4 seats. Seat 1 picks first 3 times and last 2 times while seat 4 does the reverse, a structural edge of about 4-8 points.",
    "P2: Favourite bonuses are uneven (Cats about +10-12, Toys about +8-10, Catnip about +6-7, Strays about +6-8), so the secret deal tilts the result before skill acts.",
    "P3: Because the deck is used differently at 4 players, the Favourite values need re-checking against how many Catnip and Stray cards actually appear."
  ],
  "changes": [
    {
      "what": "The 4-player game becomes 8 rounds of 5 lots of 2 cards (80 of the 96 cards are dealt; the bottom 16 are never used). The first picker still rotates by seat each round.",
      "why": "Every seat now picks first twice, second twice, third twice and last twice, so the move-order edge disappears. The 3-player game stays at 12 rounds of 4 lots, already symmetric at 4 of each position.",
      "fixes": "P1"
    },
    {
      "what": "The Cats Favourite becomes +2 per fed cat, capped at +10.",
      "why": "This removes the top end of the strongest Favourite: realistic value about +8-10.",
      "fixes": "P2"
    },
    {
      "what": "The Catnip Favourite becomes +2 per Catnip card owned (including any beyond 6), capped at +12.",
      "why": "This raises the weakest Favourite. Catnip is heavily contested, and a holder typically gets 4-5 cards, so it is worth about +8-10.",
      "fixes": "P2"
    },
    {
      "what": "The Strays Favourite (4 players only) becomes +3 per Stray Cat. The Toys Favourite stays at +1 per Toy card.",
      "why": "With about 6-7 Strays dealt across 8 rounds, a holder gets about 3, worth about +9. Toys is already about +8-10. All four Favourites now sit near +8-10, so the deal changes what to draft, not who leads.",
      "fixes": "P2, P3"
    },
    {
      "what": "No discussion phase is added.",
      "why": "Picks are sequential and public, so Favourites are already inferred from behaviour. Talk would add only cheap claims that cannot be checked, and no plan players could share, because every player competes for one win. It also costs steps.",
      "fixes": "P2"
    }
  ],
  "keeps": [
    "Drafting groups of cards from a shared face-up market, with the cut-down market of 2-card lots from the previous variation",
    "Cats must be fed: each needs 2 food, fed cats score 5, unfed cats score -1",
    "Toy sets of Red, Blue and Green; the increasing catnip scale capped at 6 cards; Strays at 3 flat",
    "The penalty for hoarding the most leftover food",
    "Secret Favourites revealed at the end, inferred from picks",
    "Highest total wins, tie-break most fed cats"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The drafting core was balanced and reasoning-rich. Only the 4-player seat asymmetry and the Favourite spread needed fixing, and both fixes fit the limits."
  },
  "variation": {
    "name": "Cat Lady: Secret Favourites (Balanced)",
    "summary": "Players draft 2-card lots from a public market, feeding cats, building toy sets, chasing catnip and collecting strays. Each player holds a secret Favourite that adds bonus points in one category. Seat order is fully symmetric, and the Favourites are tuned to be worth about the same.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP.\nThe deck has 96 cards:\n- 18 Food-1 (1 food each)\n- 10 Food-2 (2 food each)\n- 20 Cat\n- 8 Stray Cat\n- 24 Toy (8 Red, 8 Blue, 8 Green)\n- 16 Catnip\nShuffle the deck once.\nEach player is secretly dealt one Favourite, and every player gets a different one. With 3 players the Favourites are drawn from {Cats, Toys, Catnip}; with 4 players they are drawn from {Cats, Toys, Catnip, Strays}. Only the owner knows their Favourite.\nSeat the players in a fixed order, seat 1 to seat N.\n\nROUNDS.\nWith 3 players there are 12 rounds; with 4 players there are 8.\nIn round r, the first picker is seat ((r-1) mod N) + 1, and the others follow in seat order. Over the game, every seat holds each picking position equally often: 4 times each with 3 players, 2 times each with 4 players.\n\nEACH ROUND.\n1. Deal the market from the top of the deck. With 3 players deal 4 lots (Lot A to Lot D) of 2 cards each; with 4 players deal 5 lots (Lot A to Lot E) of 2 cards each. Announce every lot's contents to all players.\n2. Starting with the first picker, each player in turn chooses one remaining lot by its letter. Each player sees all earlier picks.\n3. A chosen lot goes to that player at once. Food cards add their food value to the player's food total. Cats, Strays, Toys (by colour) and Catnip are added to the player's counts. Everything a player owns is public, except their Favourite.\n4. When every player has picked, the one leftover lot is discarded.\n5. After the last round, go to final scoring. With 4 players, the 16 cards still in the deck are never used.\n\nFINAL SCORING. For each player:\n- Feeding: each Cat needs 2 food. Fed cats = the smaller of (Cats) and (food ÷ 2, rounded down). Each fed cat scores 5 and each unfed Cat scores -1. Leftover food = food total - 2 × fed cats.\n- Strays: each Stray Cat scores 3.\n- Toys: each Toy scores 1, plus 4 for each complete set of one Red, one Blue and one Green. Number of sets = the smallest of the three colour counts.\n- Catnip: with n Catnip cards, counting at most 6, the player scores n(n+1)/2 (maximum 21). Catnip beyond 6 scores nothing here.\n- Food penalty: the player or players with the most leftover food lose 2 points, provided that amount is at least 1.\n- Favourite bonus, revealed now:\n  - Cats: +2 per fed cat, maximum +10.\n  - Toys: +1 per Toy card.\n  - Catnip: +2 per Catnip card owned (including any beyond 6), maximum +12.\n  - Strays (4 players only): +3 per Stray Cat.",
    "objective": "The highest final total wins. If players are tied, the tied player with the most fed cats wins. If they are still tied, those players draw.",
    "expected_effect": "With 8 rounds at 4 players, every seat picks first, second, third and last twice, so seat order no longer decides close games. Favourites now cluster around +8-10, so the secret deal mainly changes what each player should draft rather than who is ahead. Skill shows in planning food against cats, timing toy sets and the catnip curve, inferring rivals' Favourites from their picks, and denying key lots. No simple policy is safe. Fixed-letter picking accumulates unfed cats and the food penalty. Catnip-only play splits a contested suit and ignores Strays. Greedy points-now play misses feeding dependencies and denial. Talk is left out: every player competes for one win, picks already reveal intent, and claims about Favourites cannot be checked, so a discussion would add words, not reasoning."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
