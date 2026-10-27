# Budgeted English Auction with Activity Rule

Six items are auctioned one per round. In each round there are three simultaneous sealed bidding turns, and a player who stops bidding drops out of that item. Each player has a budget of 30 and private values, and the highest score (value minus price, summed) wins.

Players: 3 to 6, best with 4

## Parameters

- `starting_budget` = 30
- `starting_score` = 0
- `starting_spent` = 0
- `rounds` = 6
- `items` = 6
- `bidding_turns_per_round` = 3
- `value_1` = 3
- `value_2` = 5
- `value_3` = 7
- `value_4` = 9
- `value_5` = 11
- `value_6` = 13
- `values_sum` = 48
- `min_first_bid` = 1
- `min_raise` = 1
- `pass_bid` = 0
- `no_leader_code` = 0

## Round

1. **update** (all players): round += 1. Announce that item {round} is now for sale.
2. **poll** (all players): Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind nobody.
3. **update** (all players): standing_bid = 0; leader = 0; turn = 0; every player's eligible = true; every player's valid_bid = false.
4. **update** (all players): turn += 1.
5. **poll** (all players): Each player's answer is stored in their bid. Nobody sees any bid until all are in.
6. **update** (all players): For each player: valid_bid = (eligible == true AND bid >= standing_bid + 1 AND bid <= budget AND bid >= 1).
7. **update** (all players): top_bid = the maximum bid among players with valid_bid true (0 if none). top_count = the number of players with valid_bid true AND bid == top_bid.
8. **update** (all players): If top_count == 1 and top_bid >= 1: standing_bid = top_bid and leader = the seat of that player. Otherwise (a tie or no valid bid), standing_bid and leader are unchanged.
9. **update** (all players): For each player: eligible = (valid_bid == true OR seat == leader). Announce standing_bid, leader and every player's eligible flag.
10. **repeat** (all players): Run the steps from 'turn += 1' through the eligibility update again until turn == 3.
11. **update** (all players): If leader != 0: the leader's budget -= standing_bid, spent += standing_bid, and score += values[round] - standing_bid. Set last_price = standing_bid if leader != 0, otherwise last_price = 0 (the item goes unsold). Announce the round's result: the item, the winner's seat or 'unsold', the price, and every budget and score.
12. **check** (all players): If round == 6, the game ends. Otherwise, start the next round.

## Ending

- ends when: round == 6 (checked after round 6's resolution)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score (the sum of value minus price over the items won). The highest score wins. Players level at the highest score share the result, which the source calls a draw.

## Choices the source did not make

- 3 to 6 players, 4 suggested: The designer set 3 to 6 with 4 suggested. Three is the smallest table where an auction has several rivals, so ties and drop-outs matter. Above 6, talk gets long and each player wins too few of the 6 items for their choices to matter.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages shown to all. Talk earns its place because players have conflicting private values: they may signal, bluff about which items they value, or try to arrange not to bid against each other.
- The strategy a thoughtful player follows: Each player has a budget of 30 against values totaling 48, so they must save money for their high-value items. Bidding in every turn keeps a player eligible, tied bids win nothing, and players must guess rivals' values from talk and past prices.
- Bids are polled from ineligible players too, and their bids are simply invalid: The source says each turn polls all players, and the validity check handles eligibility.
- Leader stores the seat number, with 0 meaning no leader: The source uses 0 for no leader, and seats are numbered from 1.
- The value set is listed as six numeric parameters value_1 to value_6: Each parameter must be a single number. The set itself is kept as the public table list value_set.

## Simplifications

- A draw at the top is expressed as a shared win among the players tied for highest score: The engine has no separate draw. Players level at the top share the win, which is the arithmetic equivalent of the source's draw.
- The three bidding turns are one block of steps run by a repeat until turn == 3: This avoids writing the same steps three times. The behavior is identical.
- Scratch attributes top_bid, top_count and valid_bid are added: The engine needs stored intermediate values to compute the highest unique valid bid by arithmetic.

## Unsupported (needs engine work)

- none
