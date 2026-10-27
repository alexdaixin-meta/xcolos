# Variation: Medici: Sealed Ledgers (revised)

A 3-6 player sealed-bid commodity auction over three days. The active player picks how many of 3 revealed cards form the lot, and everyone bids secretly at the same moment. Day-end payouts reward the most valuable ships, cumulative commodity majorities and each player's secret favoured good.

Players: 3 to 6, best with 4

## Review of the original

Medici is a 2-6 player auction game over 3 days. The active player draws a lot of 1-3 commodity cards, players bid in turn once each, and the winner loads the lot onto a limited ship. At each day's end, florins are paid for ship value rank and for commodity track majorities, and the most florins after day 3 wins.

- **non_degenerate**: good. Simple policies all lose. Always passing scores nothing while buyers convert florins into rank and majority payouts worth more than they paid. Always bidding the maximum spends the whole bankroll on one lot and cannot recover. The drawer bids last, which gives the active seat an edge on its own lot. That edge rotates, so no seat holds a lasting advantage. The previous variation's simultaneous sealed bids remove the last-bidder edge entirely.
- **skill_sensitive**: good. Card draws are random, but prices adjust to lot quality. Winning depends on valuing a lot against your ship space, the rank race and the majority race, and on judging when to stop drawing. Strong players reliably buy value cheaply. Luck matters mainly through which cards appear late in a day.
- **headroom**: good. Valuing a lot means weighing ship capacity, the expected supply left in the day, rivals' ship space and commodity counts across three days. This is far from solved. A weak player still scores by buying an occasional cheap lot.
- **reasoning_dependent**: weak. In the original everything is public except the deck order, so inference is mostly arithmetic on open positions. The previous variation added a secret favoured good and private florins, and the revision keeps them. Rivals must infer each other's valuations from their bids and purchases.
- **verifiable**: good. Payments, ship values, rank awards and majority awards are all arithmetic on tracked numbers. No judge is needed.
- **fits_platform**: weak. The original's clockwise one-bid auction and variable day ending are awkward to build. The previous variation fixed the structure with a fixed day length and simultaneous sealed bids. It then failed on limits: 'draw 3 cards at random' read as 3 draws per round, it needed at least 21 attributes against a declared 20, and day-end scoring was understated at 17 steps. The revision addresses each of these with an explicit attribute list and step list.

## Problems

- P1 Random draws: the previous variation said 'draw 3 cards at random' every round from an unshuffled rebuilt deck. Read literally, that is 3 random draws per round against a limit of 1.
- P2 Attribute overflow: a faithful build of the previous variation needed at least 21 attributes (11 per player, 10 or more on the table) against a declared and capped 20. It also needed lot composition tracking on top of that.
- P3 Understated step count: day-end scoring (ship rank top and second, four majorities, favoured cards) needed about 18-19 steps in total against a declared 17, with no published step list to check.
- P4 Tie-break bloat: the total-cards tie-break cost an attribute for very little gameplay value.
- P5 In the original, the drawer bids last, which gives the active seat a structural edge on its own lots. The previous variation already fixed this with sealed simultaneous bids, and the fix must be kept.

## Changes

- At the start of each day, the rebuilt 48-card deck is shuffled once. That single shuffle is the only random draw in any round, and it happens only in the first round of a day. Each round then moves the top 3 cards of the deck into the revealed row, with no further randomness. (fixes: P1 Random draws): This makes random_draws_per_round exactly 1 (in day-start rounds) or 0 (in all other rounds), explicitly.
- Track the favoured bonus with one per-player ship_favoured counter, incremented at LOAD. Reuse two table attributes (temp and high_bid) as scratch space for the tie count, the ship rank values and two of the majority maxima. Add two dedicated maxima for Spice and Dye. Do not store the day number or the active seat; compute both from the round number. (fixes: P2 Attribute overflow): This brings the explicit attribute list to 18, below the cap of 20, with a margin.
- Drop the total-cards tie-break. Equal florins at the end is a shared draw. (fixes: P4 Tie-break bloat): It saves an attribute, and ties are rare with 40-florin bankrolls and varied awards.
- Publish a numbered 19-step round. Ship rank uses 4 steps (compute top, award, compute second distinct, award). All four majority maxima are computed in one step and awarded in one step. Favoured scoring and the end check are one step each. (fixes: P3 Understated step count): The declared steps_per_round then matches the real build: 19 of 20, with 2 choice steps.
- Keep sealed simultaneous bids, with every player, the active seat included, bidding at the same moment. Ties for the high bid void the sale. (fixes: P5 In the original, the drawer bids last, which gives the active seat a structural edge on its own lots.): This removes the last-bidder edge, and voiding ties stops coordinated equal bids from winning anything.

## Kept from the original

- Three days, with ships emptied at the start of each day and commodity tracks carried across days.
- The active player decides how big the lot is (1 to 3 revealed cards), and the whole lot is auctioned as a unit that cannot be split.
- Ships hold 5 cards, and a player cannot buy a lot that would overfill their ship.
- Day-end payouts for ship value rank (first and second) and for commodity majorities.
- Money spent is gone. The most florins at the end wins.
- From the previous variation: secret favoured goods and private florin totals, which make rivals' valuations something to infer.

## The variation's rules

SETUP. There are N players (3-6) in seats 1..N. Each player starts with 40 florins, known only to that player, and an empty ship that holds at most 5 cards. Each player has cumulative counts of 0 for each of the four goods: Grain, Cloth, Spice and Dye. Before round 1, each player is dealt a secret FAVOURED GOOD from a favour pool. With 3 or 4 players the pool is the 4 goods once each. With 5 or 6 players the pool is the 4 goods twice each (8 tiles). The pool is shuffled once and one tile is dealt to each player. Favoured goods stay secret until the end.

DECK. The deck has 48 cards: 12 per good. Each good has the values 0,1,1,2,2,3,3,3,4,4,5,5, which sum to 33. All four goods are identical in value.

LENGTH. A day lasts 2N rounds. The game lasts 6N rounds: 18 with 3 players, 24 with 4, 30 with 5 and 36 with 6. The active seat in a round is ((round-1) mod N)+1, so each seat is active exactly twice per day. A day uses at most 6N of the 48 cards, so the deck never runs out.

EACH ROUND, in this order:
1. DAY START, DECK (only when round mod 2N = 1): rebuild the deck as all 48 cards and shuffle it once. This shuffle is the only random event in the game after setup.
2. DAY START, SHIPS (same condition): every player's ship value, ship count and ship favoured count become 0. Cumulative good counts and florins are kept.
3. REVEAL: take the top 3 cards of the deck, in order, and show them to everyone as revealed cards 1, 2 and 3.
4. LOT SIZE: the active seat alone chooses 1, 2 or 3.
5. LOT: the lot is the first that many revealed cards. Any other revealed cards are discarded for the rest of the day. Announce the lot.
6. BIDS: every player, the active seat included, secretly writes a whole-number bid from 0 to their current florins, all at the same moment. A bid of 0 is a pass.
7. VOID: a player's bid becomes 0 if their ship count plus the lot size would exceed 5.
8. HIGH BID: record the highest bid and how many players made it.
9. PAY: if the highest bid is above 0 and exactly one player made it, that player pays their bid to the bank, and those florins leave the game. Otherwise, meaning all bids are 0 or two or more players tie for the highest, the lot is discarded and nobody pays.
10. LOAD: if a sale happened, the winner adds the lot's card values to their ship value and the lot size to their ship count. They add 1 to their ship favoured count for each lot card of their favoured good, and 1 to their cumulative count of each good for each lot card of that good.
11. ANNOUNCE: show the lot, every bid, and the winner and price, or 'no sale'.
12. DAY END, TOP (only when round mod 2N = 0): find the highest ship value.
13. Every player whose ship value equals it, if it is above 0, gains 10 florins.
14. Find the highest ship value strictly below that top value, or 0 if there is none.
15. Every player whose ship value equals this second value, if it is above 0, gains 5 florins.
16. MAJORITIES: for each of the four goods, find the highest cumulative count among all players.
17. For each good, every player whose cumulative count equals that highest count, if it is at least 1, gains 4 florins.
18. FAVOURED: each player gains 3 florins per card of their favoured good on their ship (their ship favoured count).
19. GAME END: if round = 6N, the game ends. Otherwise the next round begins.

No talk phase. Each player sees only their own florins and favoured good. Lots, all bids, prices, ships and cumulative counts are public.

Objective: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, they share a draw.

Expected effect: Play is the same as the previous variation, but now buildable within the limits: one shuffle per day, 19 steps, 2 choice steps and 18 attributes. Sealed simultaneous bids mean no seat bids last. Tied high bids void the sale, so matching a rival's bid gains nothing. Players must value each lot against their remaining ship space, the rank race (10 and 5), cumulative majorities (4 per good per day) and their secret favoured good (3 per card). They must read rivals' bids to infer which good each rival favours and roughly how many florins each has left. Every simple policy can lose. Always passing keeps 40 florins while buyers gain more than they spend. Always bidding everything exhausts the bankroll on one lot. Always bidding 1 is outbid whenever a lot has value. Always taking 3 cards fills ships early and hands later lots to rivals. Talk is left out because the conflict is purely competitive bidding, and announced sealed bids already give the material for inference. Free talk would only add unverifiable claims about favoured goods, not real bargaining, since trades and binding deals are impossible.

## Complexity (the designer's count, against the limits)

- steps_per_round: 19 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
