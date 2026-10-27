# Modern Art: Sealed Season

Players auction paintings from their hands with a secret reserve and sealed bids, while trying to make the artists they own the most-played in each season, which raises those artists' value; most money after three seasons wins.

Players: 3 to 4, best with 4

## Parameters

- `starting_money` = 100
- `deck_size` = 46
- `red_cards` = 10
- `blue_cards` = 11
- `green_cards` = 12
- `yellow_cards` = 13
- `hand_size_3_players` = 10
- `hand_size_4_players` = 8
- `season_end_count` = 4
- `first_place_award` = 30
- `second_place_award` = 20
- `seasons_to_end` = 3
- `max_rounds` = 32
- `min_reserve` = 0
- `min_bid` = 0
- `artist_tiebreak_red` = 3
- `artist_tiebreak_blue` = 2
- `artist_tiebreak_green` = 1
- `artist_tiebreak_yellow` = 0

## Round

1. **update** (engine): round_number += 1; season_ended = false; buyer = 0; price = 0; every player's bid = 0.
2. **ask** (seat auctioneer): auctioneer.chosen_card = answer (kept secret).
3. **ask** (seat auctioneer): auctioneer.reserve_choice = answer (kept secret).
4. **update** (engine): Remove one copy of auctioneer.chosen_card from auctioneer.hand; current_artist = chosen_card; count_<current_artist> += 1; season_ended = (count_<current_artist> == 4). Announce the artist to all.
5. **update** (engine): When season_ended is false: reserve = auctioneer.reserve_choice and the reserve is announced to all. When season_ended is true: announce that the card is discarded unsold and the season ends (the reserve is ignored).
6. **poll** (all players (when season_ended is false)): Messages are broadcast to all: {"to": "all", "text": "Seat {seat} says: {value}"}. They are not binding.
7. **poll** (all players except the auctioneer (when season_ended is false)): Each bidder's bid = answer, hidden until all bids are in.
8. **update** (engine): When season_ended is false: the eligible bids are those with bid >= reserve. If any exist, buyer = the highest eligible bidder, with ties going to the tied seat that comes first in seat order after the auctioneer; price = buyer.bid; buyer.money -= price; auctioneer.money += price; append current_artist to buyer.paintings. Otherwise buyer = auctioneer; price = reserve; auctioneer.money -= reserve (the money leaves the game); append current_artist to auctioneer.paintings.
9. **tell** (all players (when season_ended is false)): Announce every bidder's bid, the buyer and the price.
10. **update** (engine): When season_ended is true or the sum of hand sizes == 0, score the season. (a) Each artist's key = count*4 + tiebreak (red 3, blue 2, green 1, yellow 0); first = the highest key, second = the next highest. (b) value_<first> += 30; if count_<second> > 0 then value_<second> += 20, otherwise second scores nothing. (c) Each player's money += value_<first> times the number of first in paintings, plus (if count_<second> > 0) value_<second> times the number of second in paintings. (d) Every paintings list is emptied; every count_<artist> = 0; season += 1; seasons_scored += 1. Announce the new values and payouts.
11. **check** (engine): End the game if seasons_scored >= 3, or the sum of hand sizes == 0, or round_number >= 32; otherwise continue.
12. **update** (engine): auctioneer = the next seat in seat order after the current auctioneer whose hand is not empty. Seats with empty hands are skipped as auctioneer but still bid.
13. **sync** (all players): Each player is sent their own money and hand, plus the public state.

## Ending

- ends when: seasons_scored >= 3 or sum over players of size(hand) == 0 or round_number >= 32
- ranked by: `you.money` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final money; it is revealed at the end and the most money wins. Players tied at the top share the win (the source calls this a draw).

## Choices the source did not make

- 3 to 4 players, suggested 4: Kept from the designer. The minimum is 3 because a sealed auction needs at least two rival bidders against the auctioneer. The maximum is 4 because the 46-card deck and the 32-round limit are sized for it (4 x 8 = 32 cards).
- Talk kept as a simultaneous poll before the bids: The rules say messages are written at the same time. Players disagree about which artists should rise, since each holds different hands and paintings, so talk gives material for bluffing and persuasion.
- Artist ranking computed as count*4 + tiebreak (red 3, blue 2, green 1, yellow 0): Turns 'rank by count, ties by artist order' into arithmetic. Counts never exceed 4, so the tiebreak never outweighs a count difference.
- The auctioneer picks an artist name instead of a specific card: Cards of the same artist are identical, so naming the artist is equivalent.
- Cards the auctioneer chooses that end the season are revealed before the reserve is announced: Follows the step order: the reserve is chosen secretly, then announced only if the season did not end.

## Simplifications

- A tie for most money is a shared win rather than a declared draw: The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome.
- The card choice and the reserve choice are two consecutive questions to the auctioneer: A question takes one answer; both stay secret until the reveal, so nothing changes.

## Unsupported (needs engine work)

- none
