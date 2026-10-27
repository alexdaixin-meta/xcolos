# Modern Art: Private Collections

Four players take turns auctioning paintings from five artists in sealed simultaneous bids over 12 rounds. At the end, paintings by the three most-offered artists pay out, and money plus collection value decides the winner.

Players: 4 to 4, best with 4

## Parameters

- `players` = 4
- `artists` = 5
- `cards_per_artist` = 4
- `deck_size` = 20
- `hand_size` = 5
- `starting_money` = 100
- `rounds` = 12
- `auctions_per_seat` = 3
- `unplayed_cards_per_seat` = 2
- `value_rank_1` = 60
- `value_rank_2` = 40
- `value_rank_3` = 20
- `value_rank_4_5` = 0
- `min_bid` = 0

## Round

1. **ask** (the seat equal to auctioneer): Remove one copy of the chosen card from the auctioneer's hand; set painting to its artist; add 1 to market_<artist>, whether or not it later sells.
2. **tell** (all players): Announce: 'Round {round_no}: Seat {auctioneer} offers a painting by {painting}. Market counts A {market_a}, B {market_b}, C {market_c}, D {market_d}, E {market_e}.'
3. **poll** (all players): Once all messages are in, broadcast them to all: 'Seat {seat} says: {value}'. Messages bind nobody.
4. **poll** (all players): Set each player's bid. Bids stay hidden until REVEAL.
5. **update** (all players): Let H be the maximum bid. (a) If H = 0: winner_seat = auctioneer, price = 0, and nobody pays. (c) Else, if the auctioneer's bid = H and no other bid equals H: winner_seat = auctioneer, price = H, and the auctioneer's money decreases by H (paid to the bank). (d) Else, if exactly one non-auctioneer bid H: that seat wins, price = H, its money decreases by H and the auctioneer's money increases by H. (e) Else, among the non-auctioneers who bid H, let M be the least money: if exactly one of them has money M, that seat wins and pays H to the auctioneer as in (d); (f) otherwise winner_seat = 0, price = 0, nobody pays and the painting is discarded, while the market count keeps its +1. (g) If winner_seat > 0, append painting to that seat's collection and add 1 to its coll_<painting>.
6. **tell** (all players): Announce all four bids (Seat 1..4: bid), the winner_seat (or 'discarded unsold' if 0) and the price.
7. **update** (all players): auctioneer = (auctioneer mod 4) + 1; round_no increases by 1.
8. **update** (all players): When round_no = 13: for each artist X with alphabet index i (A=0 .. E=4), let key_X = market_X * 10 + (4 - i) and rank_X = 1 + the number of artists whose key is greater than key_X; set value_X = 60 if rank_X = 1, 40 if rank_X = 2, 20 if rank_X = 3, else 0. Then for each player, score = money + coll_a*value_a + coll_b*value_b + coll_c*value_c + coll_d*value_d + coll_e*value_e.
9. **check** (all players): End the game if round_no > 12; otherwise continue to the next round.

## Ending

- ends when: round_no > 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After round 12, each player's score is their money plus the value of their collection. The highest score wins, and players tied at the top share the win (a draw between them).

## Choices the source did not make

- Exactly 4 players (min, max and suggested all 4): The designer fixes the game at 4 seats. The 12 rounds and the 3 auctions per seat depend on that count.
- Keep the simultaneous talk step as a poll, broadcast to all: The rules require simultaneous messages. Players disagree about prices and about which artists to push, so bluffing about values and hands gives the talk real strategic content.
- When two or more of the tied non-auctioneers share the least money, the painting is discarded: The source says 'if the tied players also have equal money'. This reading is applied to the least-money players among those tied, so that the least-money rule decides whenever it can.
- Alphabetical tie-break encoded as key = market*10 + (4 - index): Market counts never exceed 4 per artist, so this key orders artists by count and then alphabetically using plain arithmetic.
- The per-artist coll_* counters mirror the collection list: Collection value needs arithmetic per artist. The public list remains the stated collection.
- Strategy at the table: A thoughtful player judges which artists will reach the top three from the public market counts and their own hidden hand, offers cards to steer the rankings, bids up to a painting's expected value, and uses talk to mislead. Auctioneers weigh selling to rivals for cash against buying back from the bank.

## Simplifications

- A bid above the player's money cannot be entered; the bid range is capped at current money: The source treats an over-bid as all of the player's money. Capping the range has the same effect.
- 'Clockwise' rotation is implemented as the next seat number, wrapping from 4 to 1: The engine has no table geometry, and seat order stands in for clockwise.
- The step that offers the auction card is shown with the auctioneer's letter options taken from their hand list: Options come from a list attribute, and duplicates collapse into one option per artist, which does not change the choice.

## Unsupported (needs engine work)

- none
