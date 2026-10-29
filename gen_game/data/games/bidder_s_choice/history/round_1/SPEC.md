# Bidder's Choice: Shared Worth

Over 6 rounds players talk, then bid sealed coins for the right to take one of six objects A-F that each values privately; the highest coins plus own object values wins.

Players: 3 to 5, best with 4

## Parameters

- `object_count_total` = 6
- `starting_coins` = 20
- `value_1` = 2
- `value_2` = 4
- `value_3` = 6
- `value_4` = 8
- `value_5` = 10
- `value_6` = 14
- `values_total_per_player` = 44
- `rounds` = 6
- `min_bid` = 0
- `objects_won_per_round` = 1

## Round

1. **update** (all players): round += 1; announce 'Round {round} of 6'.
2. **poll** (all players): After all are in, each message is broadcast to all as 'Seat {seat} says: {value}'.
3. **poll** (all players): Sets each player's bid. Nobody sees any bid until all are in.
4. **update** (all players): high_bid = the maximum bid. Among players whose bid == high_bid, keep those with the minimum object_count. winner_seat = that player, or one of them chosen at random with equal chance if several remain. price = high_bid. Each player's last_bid = bid.
5. **update** (the winner_seat): The winner's coins -= price. The paid coins leave the game. All other players pay nothing.
6. **ask** (the winner_seat): last_object = the choice; remove it from pool; append it to the winner's holdings; the winner's object_count += 1; the winner's object_points += the winner's values entry for that object (A=1st ... F=6th).
7. **tell** (all players): Announce every seat's last_bid, winner_seat, price and last_object. Private values are not revealed.
8. **update** (all players): When round == 6: each player's final_score = coins + object_points, and every player's values and object_points are revealed to everyone.
9. **check** (all players): End the game if round == 6; otherwise continue to the next round.

## Ending

- ends when: round == 6
- ranked by: `you.coins + you.object_points` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their remaining coins plus the sum of their own private values for the objects they hold. The highest wins. Players level at the top share the result, which the source calls a draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept as suggested. Fewer than 3 leaves only one rival, so there is no real auction or tie-breaking pressure. More than 5 makes six objects too scarce for one bid to matter and makes the talk long.
- Keep the simultaneous talk poll before each bid: The source specifies it. Players' values differ, so they disagree about which objects are worth fighting for. Talk lets them bluff about their values or about intentions to stay out, which can steer rivals' bids.
- Store private values as a 6-entry list ordered A to F: This lets the pick add the value by position arithmetically.
- Keep a public last_bid beside the hidden bid: Bids are sealed during the poll but must all be announced afterwards.
- Players can see their own strategy points: The source says the player sees their own assignment. Showing them their running sum of held values is just derived from that.

## Simplifications

- A draw is represented as a shared win among the players tied at the top: The engine has no separate draw; tied top players share the win, which matches a draw between them.
- The final value reveal is done by an update step conditioned on round == 6, inside the round: The step list repeats each round; a condition on a single step avoids needing a separate end block.

## Unsupported (needs engine work)

- none
