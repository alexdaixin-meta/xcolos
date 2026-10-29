# Modern Art: Three Studios

Three dealers take turns auctioning paintings by three artists with sealed bids; at the end of each season the most-played artists pay out, and after 3 seasons or when all cards are gone the richest player wins.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `starting_money` = 60
- `hand_size` = 7
- `composition_A_red` = 4
- `composition_A_blue` = 2
- `composition_A_green` = 1
- `composition_B_red` = 1
- `composition_B_blue` = 4
- `composition_B_green` = 2
- `composition_C_red` = 2
- `composition_C_blue` = 1
- `composition_C_green` = 4
- `deal_roll_min` = 1
- `deal_roll_max` = 6
- `season_ending_count` = 3
- `first_place_bonus` = 20
- `second_place_bonus` = 10
- `seasons_to_end` = 3
- `max_rounds` = 21
- `min_bid` = 0
- `first_auctioneer_seat` = 1

## Round

1. **sync** (all players): Each player sees their own hand counts and all public state: money, owned counts, season counts, values and auctioneer.
2. **ask** (the seat named by auctioneer): current_artist := the chosen artist
3. **update** (all players): The auctioneer's hand_<current_artist> -= 1; season_<current_artist> += 1; season_ended := (season_<current_artist> == 3). Announce: 'Seat {auctioneer} plays {current_artist}.' If season_ended, also announce that the card is discarded unsold.
4. **poll** (all players): when season_ended is false: message := the answer; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. The talk is not binding.
5. **poll** (all players): when season_ended is false: bid := the answer, hidden until all are in
6. **update** (all players): when season_ended is false: compute each seat's offset = (seat - auctioneer + 3) mod 3 and key = bid*3 + ((3 - offset) mod 3), so the seat after the auctioneer breaks ties first and the auctioneer last. If the highest bid is 0, winner_seat := auctioneer and price := 0. Otherwise winner_seat := the seat with the highest key and price := that seat's bid. If winner_seat != auctioneer, the winner's money -= price and the auctioneer's money += price. If winner_seat == auctioneer, the auctioneer's money -= price (paid to the bank). The winner's owned_<current_artist> += 1. Announce all three bids, winner_seat and price.
7. **update** (all players): scoring_now := season_ended OR (sum over players of hand_red+hand_blue+hand_green == 0 AND season_red+season_blue+season_green > 0)
8. **update** (all players): when scoring_now: first_artist := the artist with the highest season count, ties broken Red > Blue > Green; value_<first_artist> += 20. second_artist := the highest of the other two by season count (same tie order) if its season count > 0, otherwise empty; if not empty, value_<second_artist> += 10. Each player's money += owned_<first_artist>*value_<first_artist> + (owned_<second_artist>*value_<second_artist> if second_artist is not empty). Unplaced artists pay 0. Announce the placings, the new values and each payout.
9. **update** (all players): when scoring_now: every owned_red, owned_blue and owned_green := 0; season_red, season_blue and season_green := 0; seasons_done += 1
10. **update** (all players): auctioneer := the next seat after auctioneer in the order 1->2->3->1 whose hand_red+hand_blue+hand_green > 0. If no seat has cards, it is left unchanged.
11. **check** (all players): End the game if seasons_done >= 3 or the sum over players of hand_red+hand_blue+hand_green == 0; otherwise continue.

## Ending

- ends when: seasons_done >= 3 OR sum over players of (hand_red + hand_blue + hand_green) == 0
- ranked by: `you.money` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their money. The player with the most money wins. Players tied for the most money share the result, which the source calls a draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3, and the deal (six permutations of three compositions) only works for 3 seats.
- Tie-break encoded as key = bid*3 + ((3 - offset) mod 3), where offset = (seat - auctioneer + 3) mod 3: This turns the seat-order tie rule into arithmetic: the seat after the auctioneer has priority 2, the next has 1, and the auctioneer has 0. All-zero bids are a separate case that gives the painting to the auctioneer.
- Talk kept as a simultaneous poll broadcast to all, before the bid poll: The source requires it. It also earns its place: players disagree about which artist to push and can bluff about their hidden compositions.
- Helper table attributes season_ended, scoring_now, winner_seat, price, first_artist and second_artist: The flat step list needs flags so that later steps can carry arithmetic 'when' conditions.
- If no seat has cards when the role passes, the auctioneer is left unchanged: The game ends at the check in the same round, so the value never matters.
- Strategy at the table: A thoughtful player infers the others' compositions from what they play and bid, steers seasons toward artists they own, bids up to an artist's likely payout, and sometimes buys their own card so it scores for them.

## Simplifications

- A tie for the most money is reported as a shared win among the tied players, not as a separate draw: The engine ranks by one expression and players level at the top share the win, which corresponds to the source's draw.
- The hand is three counters (hand_red, hand_blue, hand_green) rather than a list of cards: Cards of one artist are identical, so counts carry exactly the same information.

## Unsupported (needs engine work)

- none
