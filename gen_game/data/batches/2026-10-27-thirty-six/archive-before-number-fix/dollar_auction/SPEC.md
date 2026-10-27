# Sealed Escalation: Three-Way Dollar Auction

Three players hold 6 sealed all-pay auctions. Each auction has 3 simultaneous raise stages, everyone pays what they committed, and a unique top bidder gains their private value for the prize; the final score is coins left plus prize points.

Players: 3 to 3, best with 3

## Parameters

- `starting_coins` = 100
- `auctions` = 6
- `raise_stages_per_auction` = 3
- `prize_value_1` = 10
- `prize_value_2` = 15
- `prize_value_3` = 20
- `prize_value_4` = 25
- `prize_value_5` = 30
- `prize_value_6` = 40
- `prize_values_total` = 140
- `min_raise` = 0
- `min_winning_bid` = 1
- `unique_top_required_count` = 1

## Round

1. **update** (all players): auction += 1. For every player: committed = 0; current_value = values[auction], counting from 1.
2. **sync** (all players): Each player is told privately their current_value.
3. **tell** (all players): Announce the auction number and every player's coins and prize_points.
4. **poll** (all players): Messages are collected at once, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes, and messages bind no one.
5. **update** (all players): Stage 1 bound: each player's max_raise = coins - committed.
6. **poll** (all players): Stage 1: the choice is stored in raise_amt, and no one sees a choice until all are in.
7. **update** (all players): Each player's committed += raise_amt.
8. **tell** (all players): Announce every player's committed after stage 1.
9. **update** (all players): Stage 2 bound: each player's max_raise = coins - committed.
10. **poll** (all players): Stage 2: the choice is stored in raise_amt.
11. **update** (all players): Each player's committed += raise_amt.
12. **tell** (all players): Announce every player's committed after stage 2.
13. **update** (all players): Stage 3 bound: each player's max_raise = coins - committed.
14. **poll** (all players): Stage 3: the choice is stored in raise_amt.
15. **update** (all players): Each player's committed += raise_amt.
16. **tell** (all players): Announce every player's committed after stage 3.
17. **update** (all players): top_bid = max over players of committed. top_count = count of players with committed = top_bid. Every player: coins -= committed. If top_count = 1 and top_bid >= 1: the player with committed = top_bid gets prize_points += current_value, and auction_winner = that seat. Otherwise auction_winner = 'none'.
18. **tell** (all players): Announce auction_winner and top_bid.
19. **update** (all players): When auction = 6: each player's final_score = coins + prize_points.
20. **check** (all players): End the game if auction >= 6; otherwise start the next round.

## Ending

- ends when: auction >= 6
- ranked by: `you.final_score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is final_score = coins left + prize points. The highest final_score wins, and players tied at the top share the win (the source calls this a draw).

## Choices the source did not make

- 3 players (min 3, max 3): The designer fixed the size at 3 and the game is built as a three-way dollar auction. The minimum is 3 because with 2 it collapses to a simple duel with no third bidder to exploit a war of attrition. The maximum stays 3 because the design and name are three-way.
- Strategy check: Because the auction is all-pay and ties win nothing, a thoughtful player reads the committed totals between stages and drops out before over-paying. They save coins for their high-value auctions, use talk to bluff low interest or to propose rotations, and exploit two rivals tying each other out. Talk is kept because players' private values conflict, so following a proposal can cost a player.
- Talk as a simultaneous poll broadcast to all: The rules say everyone writes at the same time and all messages are then shown, so order of speaking does not matter.
- The three raise stages are written out explicitly rather than with repeat: This avoids a stage counter the rules never mention, and each stage's bound, poll, update and announcement stay visible.
- auction_winner stores the winning seat number as text: The rules say auction_winner = that player and otherwise 'none'.
- Each player is sent their full values list at setup: The rules say values is visible to its owner; current_value is also told each round as R3 requires.

## Simplifications

- A tie for the highest final_score is a shared win rather than a separate draw result: The engine ranks by one expression and players level at the top share the win, which is equivalent to the source's draw.
- The message 'everyone is told every player's committed' after each stage is an announcement, with committed kept public: During a poll no answer is seen until all are in, so making committed public only reveals the totals after each stage, as the rules require.

## Unsupported (needs engine work)

- none
