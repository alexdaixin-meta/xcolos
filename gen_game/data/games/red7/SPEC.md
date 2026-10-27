# Red3 Duel

A Red7-style shedding duel: on your turn play a card to your palette and/or change the Canvas rule so that you lead under it, or you are out; the last player alive wins the hand, and points across hands win the match.

Players: 2 to 3, best with 2

## Parameters

- `card_numbers_min` = 1
- `card_numbers_max` = 7
- `colours` = 3
- `deck_size` = 21
- `rank_red` = 3
- `rank_green` = 2
- `rank_violet` = 1
- `strength_number_multiplier` = 10
- `key_count_multiplier` = 100
- `hand_size` = 5
- `palette_start_size` = 1
- `set_aside_2p` = 9
- `set_aside_3p` = 3
- `winner_points_2p` = 1
- `loser_points_2p` = 0
- `winner_points_3p` = 2
- `second_points_3p` = 1
- `first_out_points_3p` = 0
- `target_points_2p` = 3
- `target_points_3p` = 6
- `round_cap` = 40
- `even_number_1` = 2
- `even_number_2` = 4
- `even_number_3` = 6
- `low_number_max` = 3

## Round

1. **update** (all players): New hand: deck = all 21 strengths [11..73]. For every player: hand = [], palette = [], alive = true, elim_order = 0. Set eliminated_count = 0, alive_count = number of players, canvas = 3 (Red).
2. **update** (each player in turn): Deal: for each player, 5 times move a random card from deck to that player's hand, then move 1 random card from deck to that player's palette.
3. **update** (all players): Move all remaining deck cards to set_aside (9 with 2 players, 3 with 3 players). Compute key_value under Red (max of palette) for everyone. Set turn_seat = the next seat in seat order after the player with the highest palette strength. Set hand_over = false. Announce palettes and the Canvas.
4. **update** (all players): Start of round: acted_this_round = false for every player.
5. **sync** (all players): Each player sees their own hand plus all palettes, the canvas, alive flags, points and most_recent_winner.
6. **repeat** (each living player in turn, starting at turn_seat): Repeat the next four steps (turn, resolve, hand end, pass) until hand_over is true or every living player has acted_this_round = true.
7. **ask** (the player at turn_seat): Play X: move X from hand to palette. Discard X: remove X from hand (it leaves play) and set canvas = X mod 10. Play X then discard Y: do both, in that order. Fold: nothing moves. In every case set acted_this_round = true.
8. **update** (all players): Recompute key_value for every living player under canvas. Red (3): max strength in palette. Green (2): 100 * count of palette cards with floor(s/10) in {2,4,6} + max such strength, or 0 if none. Violet (1): 100 * count of palette cards with floor(s/10) <= 3 + max such strength, or 0 if none. If the acting player folded, or their key_value is not strictly greater than every other living player's key_value: alive = false, eliminated_count += 1, elim_order = eliminated_count, alive_count -= 1. Announce the action, the canvas and any elimination.
9. **update** (all players): Hand ends and the survivor is the hand winner. With 2 players: winner points += 1 (the other gets 0). With 3 players: winner points += 2, the player with elim_order 2 points += 1, the player with elim_order 1 points += 0. Set is_recent_winner = 1 for the winner and 0 for everyone else, most_recent_winner = winner's seat, hand_over = true. Announce the points.
10. **update** (all players): turn_seat = the next living seat in seat order after the seat that just acted.
11. **update** (all players): round_no += 1.
12. **check** (all players): End the match if (number of players == 2 and any player's points >= 3) or (number of players == 3 and hand_over and any player's points >= 6) or round_no >= 40. Otherwise continue to the next round.

## Ending

- ends when: (player_count == 2 and max(points) >= 3) or (player_count == 3 and hand_over and max(points) >= 6) or round_no >= 40
- ranked by: `you.points * 10 + you.is_recent_winner` (the highest wins; players level at the top share the win)
- min_to_win: `1` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: Most points wins. Among players tied on points, the one who won the most recently completed hand wins. If no hand was ever completed, nobody reaches the bar of 1 and the match is a draw with no winner.

## Choices the source did not make

- 2 to 3 players, suggested 2: The designer's suggested size is 2, which keeps it a pure duel of reading the rival's palette and timing rule changes. The minimum is 2 because a duel needs a rival. The maximum is 3 because the deck and the scoring are only defined for 2 or 3 players.
- Cards are stored as their strength numbers (11 to 73): Number = floor(s/10) and colour = s mod 10, so every key is plain arithmetic on the list.
- Even numbers listed as three separate parameters (even_number_1..3 = 2, 4, 6): Parameters must be single numbers.
- No talk step: The rules say there is no table talk.
- Turns use sequential ask: Turns are taken one at a time in seat order, and each player sees the result of the turns before.
- The draw when no hand was completed is made with min_to_win 1: With no completed hand everyone ranks at 0 and nobody qualifies, giving no winner. Any completed hand gives someone at least 1 point.
- A player's strategy: Hold back strong cards. Switch the rule only when a discard both keeps you leading and leaves the rival needing cards they may not have. Read what a rival's palette implies about their hand.

## Simplifications

- Naming a card not held is never offered: Options are built from the player's hand, so the 'named a card you do not hold' elimination cannot arise.
- The turns within a round are a repeat loop over living players who have not yet acted: Turn order starts at turn_seat and must skip eliminated seats, and the loop must stop the moment a hand ends.
- The new-hand setup is a set of update steps each guarded by 'when hand_over': The step list is flat, so the setup steps run only when a new hand is needed.

## Unsupported (needs engine work)

- none
