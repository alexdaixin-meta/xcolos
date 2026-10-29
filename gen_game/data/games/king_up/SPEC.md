# King Up: Fair Throne

Players secretly favour three characters each, take turns raising characters up a ladder, and vote on any character that reaches the top: all Yes crowns it king, any No eliminates it.

Players: 3 to 5, best with 4

## Parameters

- `characters_per_player` = 3
- `no_cards_start` = 2
- `round_limit_3_players` = 15
- `round_limit_4_players` = 16
- `round_limit_5_players` = 15
- `start_height` = 0
- `raise_amount` = 1
- `max_active_height` = 5
- `king_height` = 6
- `eliminated_height` = -1
- `unused_height` = -2
- `king_score` = 10
- `eliminated_score` = 0
- `first_raiser_round_1` = 1

## Round

1. **update** (all players): round += 1; candidate = ''; no_count = 0; every player's vote = ''.
2. **tell** (all players): Announce the round number and the heights of all characters in play (h_a ... up to the last label in play).
3. **poll** (all players): Each message is broadcast to all as 'Seat {seat} says: {value}'. Messages bind no one.
4. **ask** (each player in turn, in seat order starting at seat first_raiser and wrapping from seat N to seat 1): The chosen character's height += 1. Each later player sees the updated heights. A pass changes nothing.
5. **update** (all players): candidate = the label of the character whose height is 5, if any; otherwise candidate stays empty.
6. **poll** (all players): when candidate is not empty: each player's vote is recorded secretly. Skipped when candidate is empty.
7. **update** (all players): when candidate is not empty: no_count = number of players with vote = No. If no_count = 0, the candidate's height = 6 and king_crowned = true. If no_count >= 1, each player with vote = No has no_cards -= 1, and the candidate's height = -1.
8. **tell** (all players): when candidate is not empty: announce the candidate, the number of No votes (no_count, not who cast them), and whether it was crowned king or eliminated.
9. **update** (all players): first_raiser = (first_raiser mod N) + 1.
10. **update** (all players): when king_crowned or round >= round_limit: reveal every player's goal; each player's score = the sum over their 3 goal characters of (10 if height = 6; 0 if height = -1; otherwise height).
11. **check** (all players): End the game if king_crowned is true or round >= round_limit; otherwise continue to the next round.

## Ending

- ends when: king_crowned == true OR round >= round_limit
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's score is the sum over their 3 secret goal characters: 10 for a king, 0 for an eliminated character, otherwise its height (0 to 5). The highest score wins; players tied for the highest score share a draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer's suggested size is 4 and is kept. 3 is the minimum because with fewer players secret goals are easy to deduce and there is no group to veto against. 5 is the maximum because the label set only goes up to O, and with more players each player's raise and veto would matter little.
- Talk as a simultaneous poll broadcast to all: The rules say messages are written at the same time without seeing the others. Talk earns its place because players' goals conflict: players bluff about which characters they favour and try to steer others into spending No cards.
- Score computed only at game end: The rules reveal goals only at scoring, so a running public score would leak the secret goals.
- Unused letters set to height -2: This keeps a fixed set of 15 height attributes for every table size while marking the unused letters as never raisable and never in any goal.
- Strategy at the table: A thoughtful player hides their goal, raises characters that help them without revealing them, saves No cards for candidates that help rivals more, and reads the No counts and others' raises to infer goals. A thoughtless player rushes one favourite to 5 and gets it vetoed.

## Simplifications

- Characters stored as 15 fixed height attributes h_a..h_o rather than a variable-length list: Arithmetic and per-character options are simpler on named numbers. Letters not in play are fixed at -2 and never offered.
- Election and resolve steps carry a 'when candidate is not empty' condition instead of being skipped as a block: The step list is flat. Each step is gated individually by the same arithmetic condition, which matches the rule exactly.
- The secret vote is stored in a per-player vote attribute visible only to its owner: This is needed to deduct No cards from the No voters while announcing only the count.

## Unsupported (needs engine work)

- none
