# Rutersju Hook

A trick-taking game played with a 36-card pack. In each deal players bid 0-3 tricks in turn, and the last bidder may not make the bids total exactly 3. Players then play 3 tricks with simultaneous card choices and score for hitting their bid exactly.

Players: 3 to 5, best with 4

## Parameters

- `deck_size` = 36
- `hand_size` = 3
- `tricks_per_deal` = 3
- `deals_per_player` = 3
- `min_bid` = 0
- `max_bid` = 3
- `forbidden_bid_total` = 3
- `exact_base_points` = 3
- `miss_penalty_per_trick` = 2
- `declarer_bonus` = 1
- `declarer_penalty` = 1
- `starting_score` = 0
- `highest_strength` = 36
- `lowest_strength` = 1

## Round

1. **update** (all players): Start a deal. Refill deck with all 36 cards. Clear every hand and played_cards. Set every bid, tricks and played to 0 or empty, every is_declarer to false, and bid_sum, declarer_seat and trick_number to 0. Deal 3 cards to each player: each card is a random draw removed from deck and appended to that player's hand.
2. **sync** (all players): Each player sees only their own hand.
3. **ask** (each player in turn, starting with seat (priority_seat mod N) + 1, going up the seat numbers with wraparound, and ending with priority_seat): The player's bid is set to the answer and bid_sum is increased by the answer. Each bidder hears all earlier bids.
4. **update** (all players): If max bid is 0, set declarer_seat to 0. Otherwise declarer_seat is the seat with the highest bid; among tied players it is the one who bid latest in this deal's bidding order. Set is_declarer to true for that seat.
5. **tell** (all players): Announce every bid and the declarer (or 'no declarer').
6. **repeat** (all players): Repeat the next three steps until trick_number = 3.
7. **poll** (all players): Each player's played is set to the chosen card. No player sees any choice until all choices are in.
8. **update** (all players): Remove each played card from its hand and append it to played_cards. The player whose played card has the highest strength (the number before the colon) adds 1 to tricks. Increase trick_number by 1.
9. **tell** (all players): Reveal all played cards together and announce the trick winner.
10. **update** (all players): Settle the deal. For each player, let d = |bid - tricks|. If d = 0, score += 3 + bid; otherwise score -= 2 * d. In addition, if is_declarer is true: if d = 0, score += 1; otherwise score -= 1. Then deal_number += 1 and priority_seat = (priority_seat mod N) + 1.
11. **tell** (all players): Announce all bids, trick counts and scores, and the new priority_seat.
12. **check** (all players): End the game if deal_number >= total_deals; otherwise start the next deal.

## Ending

- ends when: deal_number >= total_deals
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 3N deals, the player with the highest score wins. If several players tie for the highest score, they share the result, which is the source's draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. 3 is the smallest table where the hook and declarer contests bite. Above 5, 3 tricks spread over too many players, so most bids are 0 and one choice matters little.
- 'Left' means the next higher seat number, wrapping from N to 1: The engine has no physical table, and seat order must be concrete.
- Cards are written as 'strength:card', for example '36:♦7': The engine has no lookup table, so putting the strength in the card text lets the trick winner be found by comparing numbers.
- No talk step: The rules forbid discussion; players communicate only through bids and cards.
- Bidding uses ask; card play uses poll: Bids are made in turn and each bidder hears earlier bids, while cards are chosen secretly and simultaneously.

## Simplifications

- A tie for the highest score is shown as a shared win among the tied players: The engine ranks by one expression and players level at the top share the win. This is equivalent to the source's draw.
- Scratch value d = |bid - tricks| is computed inside the settlement step rather than stored: The rules never refer to it outside settlement.

## Unsupported (needs engine work)

- none
