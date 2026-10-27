# Budget English Auction

Six items are auctioned in turn, each over three rounds of simultaneous bids. Each player has a private value for every item and a budget of 30, and the highest total profit (value minus price paid) wins.

Players: 3 to 5, best with 4

## Parameters

- `value_1` = 3
- `value_2` = 5
- `value_3` = 7
- `value_4` = 9
- `value_5` = 11
- `value_6` = 13
- `value_sum` = 48
- `starting_budget` = 30
- `rounds` = 6
- `bidding_turns_per_round` = 3
- `minimum_first_bid` = 1
- `minimum_raise` = 1
- `pass_code` = 0
- `no_leader_code` = 0

## Round

1. **update** (all players): round += 1. Announce that item {round} is for sale.
2. **poll** (all players): Messages are collected at the same time and then broadcast to all as 'Seat {seat} says: {value}'. Messages bind no one.
3. **update** (all players): Reset: standing_bid = 0 and leader = 0; for every player eligible = true, bid = 0 and valid_bid = false.
4. **poll** (all players): Bidding turn 1: each player's choice is stored in bid. All bids are revealed after everyone has answered.
5. **update** (all players): Turn 1 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest bid among players with valid_bid (0 if none). top_count = the number of players with valid_bid whose bid equals top_bid.
6. **update** (all players): Turn 1 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then for every player, eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader.
7. **poll** (all players): Bidding turn 2: each player's choice is stored in bid. All bids are revealed after everyone has answered.
8. **update** (all players): Turn 2 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest valid bid (0 if none). top_count = the number of valid bids equal to top_bid.
9. **update** (all players): Turn 2 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader.
10. **poll** (all players): Bidding turn 3: each player's choice is stored in bid. All bids are revealed after everyone has answered.
11. **update** (all players): Turn 3 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest valid bid (0 if none). top_count = the number of valid bids equal to top_bid.
12. **update** (all players): Turn 3 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader.
13. **update** (the leader, if any): Settle: if leader != 0, the leader's budget -= standing_bid, spent += standing_bid, score += values[round] - standing_bid, and last_price = standing_bid. If leader == 0, last_price = 0 and the item goes unsold. Announce the result, each player's budget and score, and last_price.
14. **check** (all players): End the game if round >= 6; otherwise play the next round.

## Ending

- ends when: round >= 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score after round 6. The highest score wins, and players tied at the top share the result.

## Choices the source did not make

- 3 to 5 players, suggested 4: This is the designer's range and size. Three is the smallest table where several rivals compete and collude for each item; above 5, each player wins too few of the 6 items and the talk gets too long to follow.
- Keep simultaneous talk before bidding, as a poll with broadcast: The rules require it. Players disagree about who should win each item, so proposals to share items out or hold prices down are worth reasoning about but may be betrayed.
- The three bidding turns are written out as explicit step triples instead of a repeat: The number of turns is fixed at 3, so a flat step list is the simplest faithful form.
- Player strategy: A thoughtful player bids up to their private value on the items they value most, saves budget for high-value items, avoids tied top bids, and uses talk to propose dividing items while watching for defection.

## Simplifications

- A tie for the highest score is treated as the tied players sharing the win rather than as a separate draw: The engine treats players level at the top as sharing the win, which is equivalent to the source's draw outcome.

## Unsupported (needs engine work)

- none
