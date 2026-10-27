# Medici: Sealed Harbour

Three Florentine merchants spend 3 days auctioning commodity cards in sealed-bid rounds against a seller's secret reserve, filling 3-card ships for ship prizes and secret patron bonuses; the most florins wins.

Players: 3 to 3, best with 3

## Parameters

- `start_florins` = 25
- `deck_size` = 20
- `commodity_count` = 4
- `card_value_min` = 1
- `card_value_max` = 5
- `patron_commodities_dealt` = 3
- `days` = 3
- `rounds_per_day` = 6
- `total_rounds` = 18
- `ship_capacity` = 3
- `sales_per_player_per_day` = 2
- `reserve_min` = 1
- `reserve_max` = 6
- `bid_min` = 0
- `bid_max` = 10
- `first_ship_prize` = 12
- `second_ship_prize` = 6
- `patron_bonus_per_card` = 3
- `empty_slot_penalty` = 2
- `florin_floor` = 0

## Round

1. **update** (all players): When (round - 1) mod 6 == 0 (start of a day): set deck to the full 20 cards (each of Grain, Cloth, Spice, Dye with each value 1-5). Every player's ship = [], ship_count = 0, ship_value = 0, patron_cards = 0.
2. **update** (all players): Set seller = ((day - 1) + ((round - 1) mod 6)) mod 3 + 1. Day 1 runs 1,2,3,1,2,3, day 2 runs 2,3,1,2,3,1, and day 3 runs 3,1,2,3,1,2.
3. **update** (all players): Draw: remove one card at random from deck and set lot to it. Set lot_commodity and lot_value from that card. Announce the lot to everyone.
4. **poll** (all players): All messages are shown together: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. The talk is not binding.
5. **ask** (seat seller): The seller's reserve = the answer, kept secret.
6. **poll** (the two players other than seller): Each non-seller's bid = the answer, sealed until all bids are in.
7. **update** (all players): Resolve. Let R = seller's reserve. Let F = (seller mod 3) + 1, the first bidder clockwise after the seller. Case A, at least one non-seller bid >= R: the winner is the non-seller with the higher bid among those with bid >= R; if the two bids are equal, F wins. The winner's florins -= bid and the seller's florins += that bid. Set buyer = winner and price = bid. Case B, no bid >= R: if the seller's ship_count < 3, set buyer = seller, price = min(R, seller.florins), and seller.florins -= price, paid to the bank; otherwise set buyer = 0 and price = 0, and the lot is discarded. If buyer != 0: append lot to buyer's ship, buyer.ship_count += 1, buyer.ship_value += lot_value, and if lot_commodity == buyer.patron then buyer.patron_cards += 1.
8. **tell** (all players): Reveal to everyone: the seller's reserve, both non-sellers' bids, the buyer (or 'discarded'), and the price.
9. **update** (all players): When round mod 6 == 0 (end of day), in this order. (1) Ship prize: for each player with ship_count > 0, let h = the number of players with ship_count > 0 and a higher ship_value, and k = the number of players with ship_count > 0 and an equal ship_value (including themself). Those players occupy places h+1 to h+k. Place prizes are 12 for place 1, 6 for place 2 and 0 otherwise. The player gains floor(sum of the prizes for places h+1..h+k / k). Players with ship_count == 0 gain nothing. (2) Patron bonus: florins += 3 * patron_cards. (3) Empty-slot penalty: florins = max(0, florins - 2 * (3 - ship_count)). (4) Reset: ship = [], ship_count = 0, ship_value = 0, patron_cards = 0, and day += 1.
10. **update** (all players): round += 1.
11. **check** (all players): End the game if round > 18. Otherwise continue with the next round.

## Ending

- ends when: round > 18
- ranked by: `you.florins` (the highest wins; players level at the top share the win)
- decided by: After the end-of-day scoring of day 3, each player's standing is their florins. The most florins wins, and players tied for most share the win (a draw between them).

## Choices the source did not make

- 3 players, min = max = suggested = 3: The designer fixed 3. The seller order, two sales each per day, two bidders per lot and the 12/6 two-place prize are all built for exactly 3 seats.
- Keep the simultaneous talk as a poll with broadcast: The source requires it. Talk earns its place because patrons are secret and players compete for the same lots, so bluffing about which commodity you want, or talking down a lot's value to the seller, can mislead rivals.
- Strategy at this table: A thoughtful player prices reserves to extract bids without being forced to buy junk, infers rivals' patrons from what they bid on, bids to deny a rival's ship prize, and avoids empty-slot penalties. A thoughtless one bids face value.
- Reading of the empty-ship prize rule: Players with empty ships are excluded from ranking entirely, so places are counted only among non-empty ships. The next non-empty ship can therefore take a prize.
- Day-end order: ship prize, patron bonus, then penalty with the floor at 0: The source lists them in this order and applies the floor only to the penalty.
- In case B, the seller loading their own patron commodity counts for the patron bonus: The patron bonus counts every patron card in the ship, however it was loaded.
- Reserve asked of the seller with a single-player ask: Only one seat answers, so ask and poll behave the same. The answer is kept in the seller's ally-visible reserve.

## Simplifications

- Shuffling and drawing the top card is done as drawing a random card from the deck list: Drawing at random is how the engine shuffles. The odds are the same.
- The bank is not tracked as an attribute: It has unlimited funds in the rules. Payments to and from it only change player florins.
- Ship contents are public lists: Every lot and buyer is announced to everyone, so the ships are already public information.

## Unsupported (needs engine work)

- none
