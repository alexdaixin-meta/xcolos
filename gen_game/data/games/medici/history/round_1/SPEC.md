# Medici: Secret Patrons

Three merchants auction lots of commodity cards from a dock over 3 days of 9 rounds. They score for ship value, for commodity track majorities and a second time for majorities in their own secret Patron commodity. The most florins wins.

Players: 3 to 3, best with 3

## Parameters

- `starting_florins` = 30
- `ship_capacity` = 5
- `days` = 3
- `rounds_per_day` = 9
- `dock_size` = 3
- `max_lot_size` = 3
- `min_lot_size` = 1
- `min_bid` = 1
- `deck_size` = 30
- `commodities` = 3
- `cards_per_commodity` = 10
- `card_value_min` = 0
- `card_value_max` = 5
- `copies_of_value_0_per_commodity` = 1
- `copies_of_value_1_per_commodity` = 2
- `copies_of_value_2_per_commodity` = 2
- `copies_of_value_3_per_commodity` = 2
- `copies_of_value_4_per_commodity` = 2
- `copies_of_value_5_per_commodity` = 1
- `track_start` = 0
- `track_max` = 10
- `ship_prize_first` = 20
- `ship_prize_second` = 10
- `majority_prize_first` = 10
- `majority_prize_second` = 5
- `patron_multiplier_extra` = 1

## Round

1. **update** (all players): When round_in_day == 1 (start of a day): set deck to all 30 cards (Spice, Silk and Grain, each valued 0,1,1,2,2,3,3,4,4,5). Empty every ship and set ship_count = 0 and ship_value = 0 for all players (tracks are NOT reset). Empty dock, then draw 3 cards at random from deck, removing them, and append them in order to dock.
2. **update** (all players): active_seat = ((day - 1) + (round_in_day - 1)) mod 3 + 1. high_bid = 0, high_bidder = 0, lot = [], lot_size = 0, lot_value = 0.
3. **tell** (all players): Announce day, round_in_day, active_seat, the dock in order, and every player's ship, ship_value, track_spice, track_silk, track_grain and florins.
4. **ask** (the seat equal to active_seat): lot_size = answer. lot = the first lot_size cards of dock. lot_value = sum of the values of the cards in lot. Announce the lot.
5. **ask** (each player in turn: seat active_seat+1, then seat active_seat+2, then active_seat (seats counted mod 3)): If answer > 0: high_bid = answer, high_bidder = this seat. Each later bidder hears the earlier bids.
6. **update** (the seat equal to high_bidder): If high_bidder > 0: that player's florins -= high_bid. Append every card of lot to their ship. ship_count += lot_size. ship_value += lot_value. For each commodity, add the number of lot cards of that commodity to the matching track, capped at 10. Whether or not anyone bid, remove the lot cards from dock (if nobody bid they are discarded).
7. **update** (all players): Refill dock: while length of dock < 3 and deck is not empty, draw a random card from deck (remove it) and append it to the end of dock.
8. **tell** (all players): Announce who won the lot and for how much (high_bidder, high_bid), or that everyone passed and the lot was discarded.
9. **update** (all players): When round_in_day == 9, ship scoring. Only players with ship_count > 0 take part. For each such player, h = number of participants with a higher ship_value and e = number of participants with an equal ship_value (self included). The player occupies places h+1 to h+e. Prizes are place 1 = 20, place 2 = 10, place 3 = 0. florins += floor((sum of the prizes for places h+1..h+e) / e). Players with ship_count == 0 get nothing.
10. **update** (all players): When round_in_day == 9, for each commodity in Spice, Silk, Grain: only players with that track > 0 take part. For each such player, h = participants with a higher track and e = participants with an equal track (self included). Prizes are place 1 = 10, place 2 = 5, place 3 = 0. award = floor((sum of the prizes for places h+1..h+e) / e) and florins += award. If that commodity equals the player's patron, florins += award again (Patron bonus).
11. **update** (all players): round_in_day += 1. If round_in_day > 9: day += 1 and round_in_day = 1.
12. **tell** (all players): When day > 3: reveal every player's patron and announce final florins.
13. **check** (all players): If day > 3, end the game. Otherwise continue with the next round.

## Ending

- ends when: day > 3
- ranked by: `you.florins` (the highest wins; players level at the top share the win)
- decided by: After the day 3 end-of-day scoring, each player's standing is their florins. The player with the most florins wins. Players tied for the most share the top, which the source calls a draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed 3 seats. The game needs exactly three different Patrons for the three commodities, so the count cannot change. The strategy lies in reading rivals' Patrons from their bidding and hiding your own while still building your Patron track.
- No free-text talk step: The source rules have no negotiation phase. Adding talk would be a new mechanic.
- A pass is answered as bid 0: This keeps the bid as one whole-number answer. 0 can never be a legal bid because the minimum is 1.
- Players with an empty ship, or a track at 0, are left out of the ranking and occupy no place: The source says they earn nothing but does not say whether they occupy a place. Leaving them out lets the other players take the prizes in order.
- Third place earns 0 in the tie-split arithmetic: Only first and second prizes exist, so a place beyond second contributes 0 to a tied group's sum.
- Cards are written as 'Commodity-value' text in lists: This lets one card carry both its commodity, for tracks, and its value, for ship_value.
- The card value list is given as separate copy-count parameters: Parameters must each be a single number. The values 0,1,1,2,2,3,3,4,4,5 are written as how many copies of each value every commodity has.

## Simplifications

- A tie for the most florins is a shared win at the top, not a separate draw: The engine has no draw outcome. Tied leaders sharing the win expresses the same result.
- Start-of-day and end-of-day work are single updates with a round_in_day condition: The engine runs one flat round list. Each conditional step is a single arithmetic update, not a separate block.

## Unsupported (needs engine work)

- none
