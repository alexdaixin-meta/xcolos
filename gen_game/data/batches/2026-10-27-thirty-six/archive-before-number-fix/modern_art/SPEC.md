# Modern Art: Sealed Gallery

Three players take turns as auctioneer of 18 paintings by three artists. Everyone bids at once in sealed bids, artists gain value at each season's end, owned paintings pay out, and the richest player after round 18 wins.

Players: 3 to 3, best with 3

## Parameters

- `start_money` = 60
- `artist_count` = 3
- `die_sides` = 6
- `composition_major` = 4
- `composition_middle` = 2
- `composition_minor` = 1
- `cards_per_hand` = 7
- `auctions_per_seat` = 6
- `season_end_count` = 3
- `first_place_value` = 6
- `second_place_value` = 3
- `tie_value` = 3
- `min_season_count_to_score` = 1
- `total_rounds` = 18
- `first_auctioneer` = 1
- `min_bid` = 0

## Round

1. **update** (all players): round += 1; season_over = 0.
2. **ask** (the seat equal to auctioneer): The chosen artist is X.
3. **update** (the seat equal to auctioneer): That seat's hand_X -= 1; season_X += 1; current_artist = X. Announce current_artist to all.
4. **update** (all players): If season_X == 3, then season_over = 1 and announce that the card is discarded unsold and the season ends. Otherwise season_over stays 0.
5. **poll** (all players, when season_over == 0): Set each player's message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
6. **poll** (all players, when season_over == 0): Set each player's bid. Once all bids are in, announce all three bids.
7. **update** (all players, when season_over == 0): high_bid = max of the bids. If high_bid == 0: winner = auctioneer and price = 0. Otherwise price = high_bid and winner = the first seat with bid == high_bid in this order: auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer.
8. **update** (all players, when season_over == 0): If winner != auctioneer: the winner's money -= price and the auctioneer's money += price. If winner == auctioneer: the auctioneer's money -= price (paid to the bank). The winner's owned_X += 1. Announce winner and price.
9. **update** (all players): If round == 18, then season_over = 1.
10. **update** (all players, when season_over == 1): Set scored_red, scored_blue and scored_green to 0. Let top = the largest season count. If top >= 1 and exactly one artist has season == top, that artist gets value += 6 and scored = 1; then let s = the larger season count of the other two, and if s >= 1 and exactly one of them has season == s, that artist gets value += 3 and scored = 1. If top >= 1 and two or three artists have season == top, each of them gets value += 3 and scored = 1, and no other artist scores.
11. **update** (all players, when season_over == 1): For each player: last_payout = owned_red*value_red*scored_red + owned_blue*value_blue*scored_blue + owned_green*value_green*scored_green; money += last_payout.
12. **update** (all players, when season_over == 1): Every player's owned_red, owned_blue and owned_green = 0; season_red, season_blue and season_green = 0. Values are kept.
13. **tell** (all players, when season_over == 1): Announce the scoring artists, value_red, value_blue, value_green, and each player's last_payout and money.
14. **update** (all players): auctioneer = auctioneer % 3 + 1.
15. **check** (all players): If round == 18, end the game. Otherwise start the next round.

## Ending

- ends when: round == 18
- ranked by: `you.money` (the highest wins; players level at the top share the win)
- decided by: After round 18, including the last season's scoring and payout, the player with the most money wins. Players tied for the most money share the result, which is the source's draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed 3. The deal uses three compositions, one per seat, and 18 rounds give each seat exactly 6 auctions. With fewer seats there are no rivals to hide compositions from, and more seats would break the deal.
- Talk kept as a simultaneous poll broadcast to all: The rules say the messages are written at the same time without seeing the others. Players disagree about which artist to boost, so talk gives them something to bluff and bargain over.
- Tie order written as auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer: This is the source's seat order expressed as arithmetic.
- Owned counts and season counts are public: Every played artist, winner and price is announced, so these are already known to all.
- Season scoring is done by arithmetic, with no referee: The comparisons of the three season counts are all arithmetic.
- The round-18 auction still runs before the forced season end: The source's R11 sets season_over only after the sale steps.

## Simplifications

- A tie for the most money is reported as a shared win: The engine has no separate draw; players level at the top share the win, which is the source's draw.
- The die roll is a seeded random number from 1 to 6: The engine's randomness is seeded so a match replays exactly.

## Unsupported (needs engine work)

- none
