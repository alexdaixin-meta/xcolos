# Collector's Dollar Auction

Four players with hidden Red or Blue types bid over 8 rounds for alternating Red and Blue prizes; every player pays their own bid, win or lose, and the highest coins plus prize points wins.

Players: 4 to 4, best with 4

## Parameters

- `player_count` = 4
- `starting_coins` = 40
- `starting_prize_points` = 0
- `red_types` = 2
- `blue_types` = 2
- `rounds` = 8
- `match_prize_points` = 12
- `mismatch_prize_points` = 6
- `min_bid` = 0
- `min_contenders_for_raise` = 2
- `raise_rounds` = 2

## Round

1. **update** (all players): round += 1; prize_colour = 'Red' if round is odd, else 'Blue'; for every player opening_bid = 0, raise1 = 0, raise2 = 0, total_bid = 0, contender = false; round_winner = 0.
2. **tell** (all players): Announce: 'Round {round} of 8: the prize is {prize_colour}.'
3. **poll** (all players): Every message is broadcast to all: 'Seat {seat} says: {value}'. Messages are not binding.
4. **poll** (all players): Set each player's opening_bid. Nobody sees a bid until all are in.
5. **update** (all players): Reveal all opening_bid values. second_highest_opening = the 2nd value of the four opening bids sorted descending. For each player, contender = (opening_bid > 0 and opening_bid >= second_highest_opening). contender_count = number of players with contender true.
6. **poll** (each player with contender true, only when contender_count >= 2): Set raise1 for each contender. A raise of 0 means that contender has dropped out for this round.
7. **update** (all players): Reveal raise1 values and running totals opening_bid + raise1. raise2_count = number of contenders with raise1 > 0.
8. **poll** (each contender with raise1 > 0, only when raise2_count >= 2): Set raise2 for each eligible contender.
9. **update** (all players): For each player total_bid = opening_bid + raise1 + raise2. Reveal raise2 values and every total_bid. highest_total = max total_bid; top_count = number of players with total_bid == highest_total. round_winner = the seat with total_bid == highest_total if top_count == 1 and highest_total > 0, else 0.
10. **update** (all players): Payment: each player coins -= total_bid, winner or not.
11. **update** (the round winner, only when round_winner != 0): Winner's prize_points += 12 if type == prize_colour, else += 6 (private). Announce to all: 'Seat {round_winner} wins the {prize_colour} prize' (or 'Nobody wins the prize' if round_winner == 0), without the points gained.
12. **sync** (all players): Each player is sent their own state: coins, prize_points, type.
13. **check** (all players): If round == 8: for each player score = coins + prize_points; reveal every type, prize_points and score to all; end the game. Otherwise continue to the next round.

## Ending

- ends when: round == 8 (after the round-8 steps)
- ranked by: `you.coins + you.prize_points` (the highest wins; players level at the top share the win)
- decided by: Each player's final score is coins plus prize points. The highest score wins, and players tied at the top share the result (the source's draw).

## Choices the source did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer fixed 4 and the type split of 2 Red and 2 Blue depends on it. Each type has one rival with the same interest, so bidding wars and bluffing about type both happen.
- Talk kept as a simultaneous poll broadcast to all: The source specifies simultaneous, non-binding talk. Players disagree about who should win each prize and can bluff their type or threaten bidding wars, so the talk gives them something to reason about.
- A round with all total bids at 0 has no winner: This follows from the tie rule: all four tie at 0. Writing highest_total > 0 makes it explicit.
- The second-highest opening bid is the 2nd value of the four bids sorted descending, ties counted: This matches the source's 'ties included' and its sole-contender case: with one positive bid the second-highest is 0, so that bidder qualifies.
- The score attribute is computed only at the end: Prize points are private until the end, so a public running score would leak them.
- Strategy at the table: A thoughtful player bids only when the value is worth the sunk cost (12 points for a matching type, 6 otherwise), reads opening bids for type signals, avoids escalation because losers still pay, and saves coins, which count directly toward the score.

## Simplifications

- A draw is represented as a shared win among the players tied at the top: The engine's ranking has no separate draw outcome. Tied top players share the win.
- Conditional raise steps use a `when` condition on a single poll: The step list is flat. Each raise is a single step that is skipped when its condition fails, which needs no block branching.

## Unsupported (needs engine work)

- none
