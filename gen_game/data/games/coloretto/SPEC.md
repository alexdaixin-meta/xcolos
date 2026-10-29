# Coloretto: Secret Favourites

Three players take turns placing face-up cards into three rows or taking a row. Over three cycles they collect colours, scored against a secret Favourite colour that each player sees only for themselves.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 38
- `cards_per_colour` = 7
- `colour_count` = 5
- `plus2_cards` = 3
- `row_count` = 3
- `row_capacity` = 3
- `cycles` = 3
- `end_cycle` = 4
- `plus2_value` = 2
- `max_turns_per_cycle` = 12
- `max_turns` = 36
- `max_cards_used` = 28
- `undealt_favourites` = 2

## Round

1. **tell** (all players): Announce row_1, row_2, row_3, closed_rows, top_card, every player's red/blue/green/yellow/purple/plus2, every player's taken, cycle and active_seat.
2. **ask** (seat active_seat): Records the active player's action.
3. **update** (seat active_seat): If place_k: append top_card to row_k, then draw one card at random from deck into top_card and remove it from deck.
4. **update** (seat active_seat): If take_k: for each card in row_k, add 1 to the active player's matching red/blue/green/yellow/purple, or to plus2 for a '+2' card. Then set row_k to empty, append k to closed_rows, and set the active player's taken = true.
5. **update** (all players): When every player's taken = true: set every taken = false, empty row_1, row_2, row_3 and closed_rows, add 1 to cycle, and leave active_seat unchanged (the last taker starts). Otherwise: set active_seat to the first seat in order s+1, s+2, s (wrapping 3 to 1) whose taken = false.
6. **update** (all players): When cycle == 4: set favourite_shown = favourite for each player. With T(c) = c*(c+1)/2, F = the count of the player's favourite colour and o1..o4 = the other four counts, set score = T(F) + 2*max(T(o1),T(o2),T(o3),T(o4)) - (T(o1)+T(o2)+T(o3)+T(o4)) + 2*plus2.
7. **tell** (all players): When cycle == 4: announce every player's favourite_shown and score.
8. **check** (all players): End the game if cycle == 4; otherwise continue.

## Ending

- ends when: cycle == 4
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score from the formula (Favourite colour plus the single largest other colour score positive, the other three colours score negative, and each +2 card adds 2). The highest score wins; players tied at the top share the result, which the source calls a draw.

## Choices the source did not make

- Exactly 3 players: The designer fixed the table at 3, and the rules tie the 3 rows and 3 distinct Favourites to 3 players, so the minimum and maximum are both 3.
- No talk step: The rules state there is no table talk. The strategy is in reading which colours rivals take, guessing their hidden Favourites, and placing cards that hurt them while hiding your own.
- favourite_pool table list and favourite_shown attribute: These give the dealing of distinct Favourites and the end-of-game reveal a concrete piece of state to act on.
- Score computed only at game end: The rules say scoring happens once, at game end.

## Simplifications

- One engine round is one player's turn, with the active seat tracked in active_seat: The engine runs a flat step list. Turn order, including the same player acting again, is handled by arithmetic on taken.
- A tie for the highest score is shown as a shared win: The engine has no separate draw; players level at the top share the win, which corresponds to the source's draw.
- Shuffling is done as random draws from the deck list: The engine draws at random from a list.

## Unsupported (needs engine work)

- none
