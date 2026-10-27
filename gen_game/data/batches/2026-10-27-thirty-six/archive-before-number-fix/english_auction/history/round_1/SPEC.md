# Budgeted English Auction Series

Six items are auctioned one per round. Each auction has three simultaneous sealed bidding turns, and players hold private values and separate budgets of 30 coins; the highest total of value won minus price paid wins.

Players: 3 to 5, best with 3

## Parameters

- `items` = 6
- `rounds` = 6
- `item_value_1` = 3
- `item_value_2` = 5
- `item_value_3` = 7
- `item_value_4` = 9
- `item_value_5` = 11
- `item_value_6` = 13
- `value_sum` = 48
- `starting_budget` = 30
- `starting_score` = 0
- `min_bid` = 1
- `min_raise` = 1
- `bidding_turns_per_round` = 3
- `no_leader_code` = 0
- `pass_code` = 0
- `tiebreak_multiplier` = 10

## Round

1. **update** (all players): first_seat = ((round - 1) mod N) + 1. priority_order = [first_seat, first_seat+1, ..., N, 1, ..., first_seat-1]. standing_bid = 0. leader = 0. Every player's bid = 0 and bid_valid = false.
2. **tell** (all players): Announce: 'Item {round} is on sale. Priority order: {priority_order}. Budgets: {budget of each seat}. Scores: {score of each seat}.'
3. **poll** (all players): Each player's message is set to their reply. Once all replies are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages bind nobody.
4. **poll** (all players): Bidding turn 1. Each player's bid = reply. bid_valid = (bid >= 1 and bid <= budget). If any bid_valid: the valid bidder with the highest key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)) becomes leader, and standing_bid = that bid. Otherwise standing_bid = 0 and leader = 0.
5. **tell** (all players): Announce 'Standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid.'
6. **poll** (all players): Bidding turn 2. Each player's bid = reply. bid_valid = (bid >= standing_bid + 1 and bid >= 1 and bid <= budget). The leader may bid too. If any bid_valid: the valid bidder with the highest key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)) becomes leader, and standing_bid = that bid. Otherwise standing_bid and leader are unchanged.
7. **tell** (all players): Announce 'Standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid.'
8. **poll** (all players): Bidding turn 3, the same as turn 2: bid_valid = (bid >= standing_bid + 1 and bid >= 1 and bid <= budget). The valid bidder with the highest key becomes leader, and standing_bid = that bid. If there is no valid bid, nothing changes.
9. **tell** (all players): Announce 'Final standing bid {standing_bid} by seat {leader}' if leader > 0, else 'No bid; item {round} goes unsold.'
10. **update** (seat leader): When leader > 0: the leader's budget -= standing_bid, the leader's score += values[round - 1] - standing_bid, and last_price = standing_bid. When leader = 0: last_price = 0 and nobody's budget or score changes.
11. **tell** (all players): If leader > 0, announce 'Item {round} sold to seat {leader} for {last_price}.' The winner's value is not announced. Otherwise announce 'Item {round} unsold.'
12. **update** (all players): round += 1.
13. **check** (all players): End the game if round > 6. Otherwise continue with the next round.

## Ending

- ends when: round > 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score: the total of private values of items won minus prices paid. Unspent budget counts for nothing. The highest score wins. Players level at the top share the win, which stands in for the source's draw.

## Choices the source did not make

- 3 to 5 players, suggested 3: The designer suggested 3, so it is kept. The minimum is 3 because an auction needs at least two rivals for price competition and for the tie-break rotation to matter. The maximum stays at the source's 5 because larger tables make each seat's bids marginal and the talk long.
- Kept simultaneous talk as a poll with broadcast: The rules require it. Players disagree, since each wants the others to stay out of the items they value most, so non-binding claims about values and intentions are worth reasoning about and doubting.
- Pass encoded as bid 0, with a bid range of 0 to budget: The engine takes whole numbers in a range. Bids above budget cannot be entered, and the source treats them as passes anyway.
- Tie-break computed as key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)): This gives the priority order arithmetically. The multiplier 10 exceeds N, so the bid always dominates.
- Leader 0 and standing_bid 0 encode 'no bid': The source's 'no standing bid' needs a concrete state value.
- The six item values are listed as separate parameters item_value_1 to item_value_6: Each parameter must be a single number. They are the values dealt to every player, not tied to specific items.
- Scores remain public, as the source states: The source says budgets and scores are public but values are private. A public score change lets observers deduce the winner's value; this is kept faithfully.
- Strategy note: With 30 coins against a 48-value set, a thoughtful player plans which items to chase given their own values and the rotating tie-break. They shade bids below value and read rivals' remaining budgets and talk. A thoughtless one overspends early or bids above value.

## Simplifications

- An invalid bid in turns 2 and 3 (1 to standing_bid) can still be typed and is treated as a pass: The engine range cannot have a gap between pass and the minimum raise. The source's own rule says invalid bids count as passes.
- The source's 'draw' is a shared win among the top-scoring players: The engine has no separate draw outcome. Players level at the top share the win.

## Unsupported (needs engine work)

- none
