# Variation: Masterpiece: Secret Collectors

Four collectors each secretly prize one of four styles. They take turns selling paintings in sealed-bid private sales, and must infer who collects what, whether a lot is a forgery, and how much surplus to demand or concede.

Players: 4 to 4, best with 4

## Review of the original

Masterpiece is an art-auction game for 2 to 6 players. Each painting is public but has a private value card. Players move around a track whose spaces trigger bank auctions, private auctions of their own paintings, buys, sales and inheritances, and the winner has the most cash plus painting value at the end. The reviewed variation cut this to a rotating sealed-bid private sale: the left neighbour picks the lot, the seller sets a secret reserve, and a kept painting costs the seller the high bid, paid to the bank.

- **non_degenerate**: bad. Every player valued a painting at the same v, so there were no gains from trade. Keeping a painting cost the seller B, which made the seller's best reserve v/2. A bid B then wins only lots with v < 2B, and the buyer's expected gain is negative at every B (-50, -50, -50, -125, -475). 'Always bid 0' therefore never loses money. Rational play gives no trades and an all-way draw at 3600.
- **skill_sensitive**: bad. The best play is never to bid, which ties. Against imperfect players, the result depends on who errs and on the random value of a lot chosen blind. Superior reasoning has no profitable action to exploit.
- **headroom**: bad. The game is solved by the passive equilibrium (bid 0, reserve about v/2), and no deviation improves on it. Nothing remains to learn beyond 'do not trade'.
- **reasoning_dependent**: weak. Values are hidden, but the published reserve (about v/2) revealed each auctioned value. There was no opponent type to model, and a correct inference never led to a profitable action.
- **verifiable**: good. The score is cash plus painting values, all tracked by the engine, and the highest score wins. The previous version lacked a tie-break, so ties were common draws.
- **fits_platform**: good. The original's board was already removed. Play is turn-based with sealed bids, simultaneous talk and 9 to 15 rounds. Painting storage was underspecified but buildable as hidden-hand items.

## Problems

- P1: There are no gains from trade. Every player values a painting at the same v, so any trade is zero-sum between two players and the passive 'bid 0' policy cannot lose.
- P2: The keep penalty (the seller pays the full high bid to the bank) pushes the seller's reserve to v/2. That makes every bid unprofitable in expectation, creating a pure lemons market.
- P3: Publishing the reserve reveals each auctioned painting's value to everyone, destroying the hidden information.
- P4: There is no hidden type, so there is nothing about opponents to infer or model.
- P5: There is no tie-break, so the rational outcome is an all-way draw.
- P6: Random value deals could hand some players better positions if any value advantage were reintroduced, so a fix must not create a lottery.
- P7: The storage of paintings, owners and values was underspecified for the 20-attribute limit.

## Changes

- There are 4 public styles. Each player gets a secret collector theme, one distinct style per player. Every painting of your theme style is worth +400 extra to you at scoring. (fixes: P1, P4): A matching collector values a lot at v+400 while a non-matching seller values it at v. Mutually profitable trades now exist, and buyers who are not the matching collector still face a lemons market and should stay out. Inferring who collects what becomes the core skill.
- A seller who keeps the painting pays only a flat fee of 50 to the bank, and only if the highest bid was at least 50. (fixes: P2): The seller's honest reservation price becomes about v-50 instead of v/2. A matching buyer then has positive expected bids: against an unknown value, bidding 50 gives +87.5 in expectation and bidding 350 gives +100. Sellers in turn shade reserves upward to capture the collector's surplus. The small fee keeps stonewalling from being free.
- The reserve is never published. Only the bids, sold-or-kept, the money moved and cash totals are announced. (fixes: P3): Values stay private to past owners. A 'kept despite a high bid' outcome is only a hint, open to interpretation.
- Each player holds one painting of each style. Values are dealt by a Latin square: each player holds one each of 0, 300, 600 and 1200, and each style has exactly one painting of each value. (fixes: P6, P4): Every player starts at exactly 1500 + 2100 + 400 = 4000, with one theme painting each, so the deal is no lottery. Owning your own painting of a style tells you which values the other three paintings of that style have, which gives a deduction to plan with.
- The tie-break is most cash, then a draw. The game is fixed at 4 players. (fixes: P5, P1): This removes most draws. Four players also means a trade benefits both parties relative to the two bystanders, so trading beats passivity.
- Paintings are stored as hidden-hand items with three fields: style, value and owner. Seats 1 to 4 are defined at setup. (fixes: P7): This states exactly how the 16 paintings fit within the attribute limits.

## Kept from the original

- Paintings are public objects with private values, and a forgery is worth 0.
- Private auctions are rotated around the table, and the player to the seller's left chooses which painting goes up.
- The seller sets a secret reserve against sealed bids, and the buyer learns the value privately.
- Paintings can be resold, and the score is cash plus collection value.
- Starting cash of 1500 and the value set 0, 300, 600, 1200 are carried over.

## The variation's rules

MONEY: All amounts are in thousands of dollars. Bids and reserves are whole multiples of 50.

SETUP:
1. Seat the players 1 to 4 in a fixed circle. The player 'to the left' of player p is player p+1, and player 4's left is player 1.
2. Each player starts with 1500 cash. Cash is always public.
3. There are 4 public styles: Red, Blue, Gold and Green.
4. Each player receives 4 paintings, one of each style, with public names (for example 'P2-Gold'). Who owns which painting, and each painting's style, are always public.
5. Secret themes: the engine randomly gives each player a different style as their collector theme. Each player is told only their own theme. Everyone knows that the four themes are all different.
6. Painting values are dealt as follows.
   - Start from the pattern value(player p, style s) = [0, 300, 600, 1200][(p + s) mod 4], with players and styles indexed 0 to 3.
   - Then randomly shuffle which player is which row, which style is which column, and which value is which number.
   - The result: every player holds exactly one painting each worth 0, 300, 600 and 1200, and every style has exactly one painting of each of those values.
7. Each player is told privately the values of their own four paintings. A painting's value is known only to players who have owned it.

ROUNDS: The game has 12 rounds. The seller in round r is player ((r-1) mod 4) + 1, so each player sells 3 times. Each round:
1. ANNOUNCE: The engine names the seller. If the seller owns no paintings, skip to step 9.
2. LOT CHOICE: The player to the seller's left chooses one painting from the seller's current collection. The engine announces it, with its style, as the lot.
3. TALK: Every player, seller included, writes one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. SEALED BIDS AND RESERVE: At the same moment, each non-seller submits a bid from 0 up to their current cash, and the seller submits a secret reserve from 0 to 2000.
5. HIGH BID: Let B be the highest bid. A tie goes to the tied bidder nearest the seller going clockwise (seller's left first).
6. RESOLVE:
   - If B > reserve, the high bidder pays B to the seller, takes the painting, and is told its value privately.
   - Otherwise the seller keeps the painting. If B is at least 50, the seller pays a fee of 50 to the bank, or all their cash if they have less than 50. Fee money leaves the game.
7. ANNOUNCE: The engine publishes all bids, whether the lot was sold or kept, the money moved and the new cash totals. The reserve and the painting's value are NOT published.
8. A painting that was bought can be chosen as a lot again later, when its new owner is the seller.
9. END CHECK: After round 12, go to scoring.

SCORING:
1. All values and themes are revealed.
2. Each player's score = cash + the total value of the paintings they own + 400 for each painting they own whose style is their own theme.

Objective: The highest score wins. If several players tie for the highest score, the one among them with the most cash wins. If they are still tied, the game is a draw.

Expected effect: Every player starts at exactly 4000. Each lot has at most one collector who gains 400 from it, so for a non-matching buyer bidding is still a losing lemons bet. The matching collector can profit, but bidding reveals their theme. Sellers must guess who the collector is and set a hidden reserve above their honest floor (about v-50) to capture part of the 400. The left neighbour's lot choice is itself strategic: picking a lot of their own style hints at their theme, and picking a lot of the seller's own theme is effectively a block, since nobody else gains from it and it will likely be kept. Owning your own painting of a style tells you which values the other three paintings of that style can have, which sharpens bids. Simple policies lose. 'Always bid 0' never gains the bonus and falls behind players who trade profitably. 'Always bid all cash' pays up to 1500 for lots worth on average 525 plus 400 at most. 'Always reserve the maximum' forgoes surplus and pays fees. 'Always reserve 0' sells 1200-value paintings for 50. Talk passes both tests. Players disagree about prices and about who wins, since only one can. A buyer who believes a seller's claim that the lot is no forgery may overpay, and a seller who believes a bluffed 'I am not your collector' may undercharge.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 14 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
