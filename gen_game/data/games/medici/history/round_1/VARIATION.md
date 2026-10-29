# Variation: Medici: Secret Patrons

A 3-player, 3-day Medici. The active player picks 1-3 cards from an open Dock as a lot and auctions it once around, bidding last. Ships score by value and cumulative commodity tracks score by majority. Each merchant secretly serves a Patron who doubles their majority award in one commodity, so bids must be read for hidden intent.

Players: 3 to 3, best with 3

## Review of the original

Medici is a 2-6 player auction game over 3 days. The active player turns up a lot of 1-3 commodity cards and the lot is auctioned once around the table, with the drawer bidding last. Players fill limited ships, and at the end of each day florins are paid for the most valuable ships and for majorities on cumulative commodity tracks. Most florins wins.

- **non_degenerate**: good. Every simple policy can lose. Always passing earns nothing, so it loses whenever rivals buy at fair prices. Always bidding your whole purse leaves you broke after one lot. Always bidding the minimum only wins lots nobody wants. The drawer bids last, which is an edge, but the drawer role rotates.
- **skill_sensitive**: good. Valuing a lot against the ship and track bonuses still at stake, and sizing a lot to squeeze rivals, separate strong players from weak ones. Face-down deck order adds some luck: a player can draw a gold card or a dud. It does not swamp skill.
- **headroom**: good. Pricing depends on rivals' remaining ship space, money and track standings, which leaves a deep valuation problem. A novice who buys cheaply still scores something.
- **reasoning_dependent**: weak. Almost everything is public: lots, ships, tracks and usually money. The only hidden thing is the order of the deck, which is luck rather than something to infer. There is no opponent type to read. Reasoning is mostly calculation plus some opponent modelling of how high rivals will bid.
- **verifiable**: good. All scoring is arithmetic on card values, track counts and florins.
- **fits_platform**: weak. The game is turn-based and text-only, but several things break the limits. Drawing 1-3 cards one at a time with a stop decision after each needs several random draws and conditional loops. Five commodities and per-player tracks for 6 players exceed the attribute limits. With 6 players an auction needs 6 sequential bid steps, more than 4 choice steps per round. Ending a day when ships fill and the fill-free rule add irregular flow.

## Problems

- P1: Nothing hidden worth inferring. Lots and tracks are public, so play is calculation, not inference about opponents.
- P2: Card-by-card drawing with a stop after each card needs several random draws per round and loop-like control flow the engine cannot build.
- P3: Up to 6 players means up to 6 sequential bids per auction, beyond 4 choice steps per round.
- P4: Five commodities and per-player tracks for many players exceed the attribute budget.
- P5: The day ends at an irregular moment (all ships but one full, plus the fill-free last ship), which needs conditional blocks and makes length unpredictable.
- P6: Face-down draw luck (who happens to flip the high cards) adds randomness that is not skill.
- P7: A fixed first player each day would gain a seat edge in an auction game where early lots set the tempo.

## Changes

- Each player is secretly dealt a different Patron commodity. Commodity-majority awards in your Patron commodity are paid to you twice. Patrons are revealed only at the end. (fixes: P1): This creates one strong hidden element. Bids now signal which commodity a rival is chasing, and players must infer the two unknown patrons from bidding behaviour, and can bluff by bidding on a commodity that is not theirs. Patrons are a permutation of three equal commodities, so no one is dealt a better type: the type changes what to buy, not who is ahead.
- Replace card-by-card drawing with an open Dock: the next 3 cards of the deck are always face up. The active player chooses to auction the first 1, 2 or 3 Dock cards as the lot. The Dock is then refilled from the deck. (fixes: P2): This keeps the drawer's key decision, sizing the lot to tempt or starve rivals, in a single choice with no loop. It also removes blind-flip luck, because everyone sees what is coming next.
- Fix the game at exactly 3 players. (fixes: P3): An auction then needs 2 rival bids plus the drawer's bid. With the lot-size choice that is 4 choice steps. Three players also fit the patron permutation exactly.
- Use 3 commodities (Spice, Silk, Grain), each with 10 cards valued 0,1,1,2,2,3,3,4,4,5, a 30-card deck reshuffled each day, and ship capacity 5. (fixes: P4): This keeps the attribute count low and the arithmetic easy while preserving the ship-value and track-majority trade-off.
- Each day is exactly 9 auction rounds: each player is active 3 times. A full ship simply cannot bid. The fill-free rule is dropped. (fixes: P5): This gives fixed length and a flat step list. With about 2 cards per lot against 15 total ship space, ships still fill and space stays scarce.
- The Dock shows the next 3 cards openly. (fixes: P6): Players plan around known upcoming lots, so outcomes depend on valuation rather than on flips.
- Rotate the first active player each day (day 1 player A, day 2 player B, day 3 player C). (fixes: P7): Every seat gets the same number of drawer turns and each seat leads one day.

## Kept from the original

- Three trading days with florins as both purse and score
- Lots of 1-3 commodity cards whose size the drawer chooses
- A once-around auction with each rival bidding once in order and the drawer bidding last
- Paying the bank; lots cannot be split, and a lot that would overfill your ship cannot be bid on
- Limited ship holds scored by total value each day
- Cumulative commodity tracks scored by majority each day
- Most florins after day 3 wins

## The variation's rules

SETUP. Three players sit in fixed order A, B, C. Each starts with 30 florins (public). Each has a ship with room for 5 cards and three public commodity tracks (Spice, Silk, Grain), all at 0. The three commodities are shuffled and one is dealt secretly to each player as their Patron, so every player has a different Patron and knows only their own. The deck has 30 cards: for each of Spice, Silk and Grain there are 10 cards valued 0, 1, 1, 2, 2, 3, 3, 4, 4, 5.

START OF EACH DAY. There are 3 days. Shuffle all 30 cards into a face-down deck and empty every ship (tracks are NOT reset). Turn the top 3 cards face up in a row: this is the Dock, ordered first, second, third. The first active player is A on day 1, B on day 2 and C on day 3. The active role then passes in seat order A, B, C, A... each round. Each day has exactly 9 rounds.

EACH ROUND.
(1) The Dock, all ships, tracks and florins are announced.
(2) The active player chooses a lot size of 1, 2 or 3 (no more than the cards in the Dock). The lot is the first that many Dock cards. Its size is its card count and its value is the sum of its card values.
(3) Auction, once around. The next player in seat order after the active player bids first, then the other non-active player, then the active player last. Each bidder either passes or bids a whole number that is at least 1, higher than the current highest bid, and no more than their florins. A player whose ship lacks room for the whole lot must pass.
(4) If anyone bid, the highest bidder pays that many florins to the bank and loads every card of the lot onto their ship. For each card loaded, that player's track in the card's commodity rises by 1, to a maximum of 10. If everyone passed, the lot is discarded.
(5) Remove the lot's cards from the Dock, slide the remaining Dock cards forward, and refill the Dock to 3 cards from the top of the deck (fewer if the deck runs out).

END OF DAY (after round 9 of the day).
(a) Ship scoring: rank players by total value of the cards on their ship. The highest gets 20 florins and the second gets 10. Tied players add the prizes for the places they occupy and split them equally, rounded down. A player with an empty ship gets nothing.
(b) Commodity majorities: for each commodity, the player with the highest track gets 10 florins and the second highest gets 5. Ties split as above. A track at 0 earns nothing.
(c) Patron: a player who earned a majority award in step (b) in their own Patron commodity receives that same amount again.
All awards are added to florins.

END OF GAME. After day 3 scoring, Patrons are revealed and the player with the most florins wins.

Objective: After the end-of-day scoring of day 3, the player with the most florins wins. If two or more players tie for the most, the game is a draw.

Expected effect: Lots are priced against known ship space, cash and track standings, which keeps Medici's valuation depth. The hidden Patron adds inference. A rival who keeps paying over the odds for Silk is probably the Silk Patron, so contesting Silk costs more than it looks, while letting them have it hands them a doubled award. Players can also bluff by bidding up a non-patron commodity to drain rivals' purses. The open Dock removes blind-flip luck and makes lot sizing a deliberate squeeze: a 3-card lot that only one player can still fit, or a single juicy card to force a bidding war. Always passing earns nothing and loses to anyone buying at fair prices. Bidding your whole purse leaves you broke. Bidding the minimum wins only junk. There is no talk phase: with only 3 players and 4 choice steps already used, the auction itself carries the signalling, and cheap talk would add no conflict the bids do not already express.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 27 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
