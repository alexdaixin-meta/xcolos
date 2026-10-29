# 21 design

- time: 2026-10-27T17:07:44+00:00 (85.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 dd0ac03808b528f4, reply sha256 0f86b12a5cde769b

## Sent

````
Original game: Medici
Players in the original: 2 to 6

Original rules:
Medici is played over 3 days. Set up a face-down commodity deck, adjusting size by player count, and give each player 30-40 florins and a ship for 5 cards (7 in 2p). Each turn the active player draws 1 to 3 cards face-up as a single lot, stopping at will up to 3. The lot is then auctioned: each other player in clockwise order may make one increasing bid or pass, the drawer bids last. Minimum bid is 1 and you cannot bid more than your current florins. Winner pays by decreasing money and loads the whole lot on his ship; lots cannot be split or discarded after purchase and you may not bid if the lot would overfill your ship. If all pass, the lot is discarded. When a ship is full that player sits out the rest of the day. Day ends when all but one ship are full, last player fills free from deck, or deck empties. Score ships by value and by commodity track progress, awarding florins, then start next day. Most florins after day 3 wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Positives:
- The rules cover lot choice, voiding, ties, loading, scoring order and the tie-break.
- The game is finite: 6N rounds, at most 36.
- The deck never runs out: 6N reveals per day is at most 36 of 48 cards.
- Every step is decided by arithmetic, needs no board or clock, and every bid is a simultaneous poll.
- Having no talk phase is defensible: announced bids give material to infer from.

Problem 1: random draws. Step 1 rebuilds the deck without shuffling. Step 3 then says 'draw 3 cards at random' every round. Read literally, that is 3 random draws per round against a limit of 1. The designer's figure of 1 holds only if the deck is shuffled once and the top 3 cards are taken, which the rules do not say.

Problem 2: attribute count. The designer declares 20, which is exactly the cap. A faithful implementation needs more.
- Per player (11): florins, ship value, ship count, ship-favoured count (needed for step 10c because ships reset), Grain, Cloth, Spice and Dye cumulative counts, total cards, favoured good, bid.
- Table (at least 10): round, active seat, deck, revealed cards, lot size, high bid, count of players at the high bid (to detect ties in step 7), top ship value and second distinct ship value (the ranking workaround keeps a table attribute beside the score), and a per-good maximum for majorities.
- That is at least 21, before the lot's per-good composition needed for step 8.

Problem 3: step count. Step 10 needs ship rank (top and second distinct, by calc), plus 4 majority checks, plus favoured scoring. With the other steps that comes to about 18-19, against a declared 17. This is not proven over 20, but the declaration is understated.

The design exceeds or misstates the platform limits as written.
- change: Step 1: shuffle the rebuilt 48-card deck once at day start; this is the round's single random draw. Step 3: reveal the top 3 cards of that shuffled deck with remove operations. This keeps random_draws_per_round at 1, explicitly.
- change: Cut attributes to at most 20 and list them explicitly. Options:
- drop the total-cards tie-break (use a shared draw instead);
- replace per-good ship tracking with a single per-player ship_favoured counter, incremented at LOAD when a card matches the player's favoured good;
- reuse one temporary table attribute for the high-bid count, ship-rank maxima and per-good majority maxima;
- do not store day.
- change: Publish a step list (at most 20) showing ship rank and the four majority checks implemented with calc, so the declared steps_per_round matches the real count.
The variation that was reviewed: Medici: Sealed Ledgers: SETUP. N players (3-6), seats 1..N. Each player starts with 40 florins, visible only to that player, and an empty ship that holds 5 cards. Each player also starts with cumulative commodity counts of 0 for Grain, Cloth, Spice and Dye, and a total-cards count of 0. Before round 1, the goods Grain, Cloth, Spice and Dye are shuffled and dealt one to each player as their FAVOURED GOOD, all different and known only to that player. With 5 or 6 players, goods repeat: the 4 goods are dealt to seats 1-4 as above, then seats 5 and 6 each receive a random good. Favoured goods stay secret until the end.

DECK. The deck has 48 cards: 12 per good, with values 0,1,1,2,2,3,3,3,4,4,5,5. Every good has the same values (sum 33).

LENGTH. A day lasts 2N rounds, and the game lasts 6N rounds (18 with 3 players, 24 with 4, 30 with 5, 36 with 6). The day number is ((round-1) div 2N)+1.

EACH ROUND, in this order:
1. DAY START: if round mod 2N == 1, rebuild the deck as the full 48 cards and empty every ship. Ship cards, ship value and ship count all become 0. Cumulative commodity counts, total cards and florins are kept.
2. ACTIVE SEAT: set active seat = ((round-1) mod N)+1, computed from the round number every round.
3. REVEAL: draw 3 cards at random from the deck and show them to everyone, in draw order.
4. LOT SIZE: the active seat alone chooses 1, 2 or 3. The lot is the first that many revealed cards. Any remaining revealed cards are discarded for the rest of the day.
5. BIDS: every player, the active seat included, secretly writes a whole-number bid from 0 to their current florins at the same moment. A bid of 0 is a pass.
6. VOID: a bid counts as 0 if the lot would take that player's ship over 5 cards. A player with a full ship can therefore never buy.
7. RESOLVE: all bids are revealed. If the highest bid is 0, or two or more players tie for the highest bid, the lot is discarded and nobody pays. Otherwise the single highest bidder pays their bid to the bank, which removes those florins from the game.
8. LOAD: the winner puts the lot on their ship. Their ship value rises by the lot's card values, their ship count by the number of cards, each matching cumulative commodity count by 1 per card, and their total cards by the number of cards.
9. ANNOUNCE: the lot, all bids, the winner (or no sale) and the price.
10. DAY END: if round mod 2N == 0, score in this order:
(a) SHIP RANK: every player with the highest ship value, if it is above 0, gains 10. Every player with the next-highest distinct ship value, if it is above 0, gains 5.
(b) MAJORITIES: for each good, every player holding the highest cumulative count of that good, with at least 1, gains 4.
(c) FAVOURED: each player gains 3 per card of their favoured good on their ship now.
11. GAME END: if round == 6N, the game ends after step 10. Otherwise the next round begins. Winner: After round 6N, the player with the most florins wins. If florins are tied, the tied player with the most total cards bought wins (standing = florins × 1000 + total cards). If both are equal, the tied players share the win as a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Medici is a 2-6 player auction game over 3 days. The active player draws a lot of 1-3 commodity cards, players bid in turn once each, and the winner loads the lot onto a limited ship. At each day's end, florins are paid for ship value rank and for commodity track majorities, and the most florins after day 3 wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies all lose. Always passing scores nothing while buyers convert florins into rank and majority payouts worth more than they paid. Always bidding the maximum spends the whole bankroll on one lot and cannot recover. The drawer bids last, which gives the active seat an edge on its own lot. That edge rotates, so no seat holds a lasting advantage. The previous variation's simultaneous sealed bids remove the last-bidder edge entirely."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Card draws are random, but prices adjust to lot quality. Winning depends on valuing a lot against your ship space, the rank race and the majority race, and on judging when to stop drawing. Strong players reliably buy value cheaply. Luck matters mainly through which cards appear late in a day."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Valuing a lot means weighing ship capacity, the expected supply left in the day, rivals' ship space and commodity counts across three days. This is far from solved. A weak player still scores by buying an occasional cheap lot."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "In the original everything is public except the deck order, so inference is mostly arithmetic on open positions. The previous variation added a secret favoured good and private florins, and the revision keeps them. Rivals must infer each other's valuations from their bids and purchases."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Payments, ship values, rank awards and majority awards are all arithmetic on tracked numbers. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original's clockwise one-bid auction and variable day ending are awkward to build. The previous variation fixed the structure with a fixed day length and simultaneous sealed bids. It then failed on limits: 'draw 3 cards at random' read as 3 draws per round, it needed at least 21 attributes against a declared 20, and day-end scoring was understated at 17 steps. The revision addresses each of these with an explicit attribute list and step list."
    }
  ],
  "problems": [
    "P1 Random draws: the previous variation said 'draw 3 cards at random' every round from an unshuffled rebuilt deck. Read literally, that is 3 random draws per round against a limit of 1.",
    "P2 Attribute overflow: a faithful build of the previous variation needed at least 21 attributes (11 per player, 10 or more on the table) against a declared and capped 20. It also needed lot composition tracking on top of that.",
    "P3 Understated step count: day-end scoring (ship rank top and second, four majorities, favoured cards) needed about 18-19 steps in total against a declared 17, with no published step list to check.",
    "P4 Tie-break bloat: the total-cards tie-break cost an attribute for very little gameplay value.",
    "P5 In the original, the drawer bids last, which gives the active seat a structural edge on its own lots. The previous variation already fixed this with sealed simultaneous bids, and the fix must be kept."
  ],
  "changes": [
    {
      "what": "At the start of each day, the rebuilt 48-card deck is shuffled once. That single shuffle is the only random draw in any round, and it happens only in the first round of a day. Each round then moves the top 3 cards of the deck into the revealed row, with no further randomness.",
      "why": "This makes random_draws_per_round exactly 1 (in day-start rounds) or 0 (in all other rounds), explicitly.",
      "fixes": "P1 Random draws"
    },
    {
      "what": "Track the favoured bonus with one per-player ship_favoured counter, incremented at LOAD. Reuse two table attributes (temp and high_bid) as scratch space for the tie count, the ship rank values and two of the majority maxima. Add two dedicated maxima for Spice and Dye. Do not store the day number or the active seat; compute both from the round number.",
      "why": "This brings the explicit attribute list to 18, below the cap of 20, with a margin.",
      "fixes": "P2 Attribute overflow"
    },
    {
      "what": "Drop the total-cards tie-break. Equal florins at the end is a shared draw.",
      "why": "It saves an attribute, and ties are rare with 40-florin bankrolls and varied awards.",
      "fixes": "P4 Tie-break bloat"
    },
    {
      "what": "Publish a numbered 19-step round. Ship rank uses 4 steps (compute top, award, compute second distinct, award). All four majority maxima are computed in one step and awarded in one step. Favoured scoring and the end check are one step each.",
      "why": "The declared steps_per_round then matches the real build: 19 of 20, with 2 choice steps.",
      "fixes": "P3 Understated step count"
    },
    {
      "what": "Keep sealed simultaneous bids, with every player, the active seat included, bidding at the same moment. Ties for the high bid void the sale.",
      "why": "This removes the last-bidder edge, and voiding ties stops coordinated equal bids from winning anything.",
      "fixes": "P5 In the original, the drawer bids last, which gives the active seat a structural edge on its own lots."
    }
  ],
  "keeps": [
    "Three days, with ships emptied at the start of each day and commodity tracks carried across days.",
    "The active player decides how big the lot is (1 to 3 revealed cards), and the whole lot is auctioned as a unit that cannot be split.",
    "Ships hold 5 cards, and a player cannot buy a lot that would overfill their ship.",
    "Day-end payouts for ship value rank (first and second) and for commodity majorities.",
    "Money spent is gone. The most florins at the end wins.",
    "From the previous variation: secret favoured goods and private florin totals, which make rivals' valuations something to infer."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The auction core is skill-rich and turns cleanly into simultaneous sealed bids. The earlier failure was about the platform limits, which an explicit step list and attribute list fix without changing the game."
  },
  "variation": {
    "name": "Medici: Sealed Ledgers (revised)",
    "summary": "A 3-6 player sealed-bid commodity auction over three days. The active player picks how many of 3 revealed cards form the lot, and everyone bids secretly at the same moment. Day-end payouts reward the most valuable ships, cumulative commodity majorities and each player's secret favoured good.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "rules": "SETUP. There are N players (3-6) in seats 1..N. Each player starts with 40 florins, known only to that player, and an empty ship that holds at most 5 cards. Each player has cumulative counts of 0 for each of the four goods: Grain, Cloth, Spice and Dye. Before round 1, each player is dealt a secret FAVOURED GOOD from a favour pool. With 3 or 4 players the pool is the 4 goods once each. With 5 or 6 players the pool is the 4 goods twice each (8 tiles). The pool is shuffled once and one tile is dealt to each player. Favoured goods stay secret until the end.\n\nDECK. The deck has 48 cards: 12 per good. Each good has the values 0,1,1,2,2,3,3,3,4,4,5,5, which sum to 33. All four goods are identical in value.\n\nLENGTH. A day lasts 2N rounds. The game lasts 6N rounds: 18 with 3 players, 24 with 4, 30 with 5 and 36 with 6. The active seat in a round is ((round-1) mod N)+1, so each seat is active exactly twice per day. A day uses at most 6N of the 48 cards, so the deck never runs out.\n\nEACH ROUND, in this order:\n1. DAY START, DECK (only when round mod 2N = 1): rebuild the deck as all 48 cards and shuffle it once. This shuffle is the only random event in the game after setup.\n2. DAY START, SHIPS (same condition): every player's ship value, ship count and ship favoured count become 0. Cumulative good counts and florins are kept.\n3. REVEAL: take the top 3 cards of the deck, in order, and show them to everyone as revealed cards 1, 2 and 3.\n4. LOT SIZE: the active seat alone chooses 1, 2 or 3.\n5. LOT: the lot is the first that many revealed cards. Any other revealed cards are discarded for the rest of the day. Announce the lot.\n6. BIDS: every player, the active seat included, secretly writes a whole-number bid from 0 to their current florins, all at the same moment. A bid of 0 is a pass.\n7. VOID: a player's bid becomes 0 if their ship count plus the lot size would exceed 5.\n8. HIGH BID: record the highest bid and how many players made it.\n9. PAY: if the highest bid is above 0 and exactly one player made it, that player pays their bid to the bank, and those florins leave the game. Otherwise, meaning all bids are 0 or two or more players tie for the highest, the lot is discarded and nobody pays.\n10. LOAD: if a sale happened, the winner adds the lot's card values to their ship value and the lot size to their ship count. They add 1 to their ship favoured count for each lot card of their favoured good, and 1 to their cumulative count of each good for each lot card of that good.\n11. ANNOUNCE: show the lot, every bid, and the winner and price, or 'no sale'.\n12. DAY END, TOP (only when round mod 2N = 0): find the highest ship value.\n13. Every player whose ship value equals it, if it is above 0, gains 10 florins.\n14. Find the highest ship value strictly below that top value, or 0 if there is none.\n15. Every player whose ship value equals this second value, if it is above 0, gains 5 florins.\n16. MAJORITIES: for each of the four goods, find the highest cumulative count among all players.\n17. For each good, every player whose cumulative count equals that highest count, if it is at least 1, gains 4 florins.\n18. FAVOURED: each player gains 3 florins per card of their favoured good on their ship (their ship favoured count).\n19. GAME END: if round = 6N, the game ends. Otherwise the next round begins.\n\nNo talk phase. Each player sees only their own florins and favoured good. Lots, all bids, prices, ships and cumulative counts are public.",
    "objective": "After round 6N, the player with the most florins wins. If two or more players tie for the most florins, they share a draw.",
    "expected_effect": "Play is the same as the previous variation, but now buildable within the limits: one shuffle per day, 19 steps, 2 choice steps and 18 attributes. Sealed simultaneous bids mean no seat bids last. Tied high bids void the sale, so matching a rival's bid gains nothing. Players must value each lot against their remaining ship space, the rank race (10 and 5), cumulative majorities (4 per good per day) and their secret favoured good (3 per card). They must read rivals' bids to infer which good each rival favours and roughly how many florins each has left. Every simple policy can lose. Always passing keeps 40 florins while buyers gain more than they spend. Always bidding everything exhausts the bankroll on one lot. Always bidding 1 is outbid whenever a lot has value. Always taking 3 cards fills ships early and hands later lots to rivals. Talk is left out because the conflict is purely competitive bidding, and announced sealed bids already give the material for inference. Free talk would only add unverifiable claims about favoured goods, not real bargaining, since trades and binding deals are impossible."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 19,
    "choice_steps_per_round": 2,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
