# 3Up Clear Race

Three players shed a 10-card hand onto a climbing pile. A run of three equal ranks or a Clear card wipes the pile, a stuck player must take the pile, and the first to empty hand and face-up cards wins.

Players: 3 to 3, best with 3

## Parameters

- `min_rank` = 1
- `max_rank` = 9
- `copies_per_rank` = 3
- `clear_cards` = 3
- `low_band_max` = 3
- `mid_band_min` = 4
- `mid_band_max` = 6
- `high_band_min` = 7
- `cards_per_band_dealt` = 3
- `clears_per_seat` = 1
- `hand_size` = 10
- `face_up_picks` = 3
- `hand_after_picks` = 7
- `run_to_clear` = 3
- `max_rounds` = 30
- `empty_top_rank` = 0

## Round

1. **update** (all players): round = round + 1; lead = ((round - 1) mod 3) + 1; announce the round and the leading seat
2. **ask** (seat lead (turn slot 1); skipped when game_over is true): the choice is recorded for this slot and announced to all
3. **update** (seat lead (turn slot 1); skipped when game_over is true): 'r xk': move k cards of rank r from the source to pile; if top_rank == r then run_count += k else run_count = k; top_rank = r. 'C': remove that C from the source and from the game. 'take': append all pile cards to hand, pile = empty, top_rank = 0, run_count = 0. Then, if 'C' was played or run_count >= 3: remove all pile cards from the game, top_rank = 0, run_count = 0. Then hand_count = length of hand, up_count = length of up_pile, cards_left = hand_count + up_count; if cards_left == 0 then game_over = true. Announce the play.
4. **ask** (seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true): the choice is recorded and announced to all
5. **update** (seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true): the same play, clear and count updates as slot 1, applied to this seat
6. **ask** (seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true): the choice is recorded and announced to all
7. **update** (seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true): the same play, clear and count updates as slot 1, applied to this seat
8. **update** (all players): if round == 30 then game_over = true
9. **check** (all players): end the game if game_over is true; otherwise run the round again

## Ending

- ends when: game_over == true
- ranked by: `0 - you.cards_left` (the highest wins; players level at the top share the win)
- decided by: A player's standing is how few cards they have left. A seat that reaches 0 cards_left ends the game at once and is the only seat at 0, so it wins. Otherwise, after round 30, the seat with the fewest cards_left wins, and seats tied for fewest share the result, which the source calls a draw.

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixed the game at 3: the deck splits exactly into three 10-card hands and the lead rotates over 3 seats. Fewer seats would leave stacks undealt and more would need more cards. At 3, each seat must read the public up_piles and the pile to decide when to dump runs, save a C, or force an opponent to take.
- No talk phase: The source says there is none; plays are announced publicly instead.
- Score expressed as 0 - cards_left: The engine ranks highest-first, and fewer cards is better.
- Card entries stored as text '1'..'9' and 'C': A single list can then hold both ranks and Clear cards; ranks are compared numerically.

## Simplifications

- The three turns of a round are written as three fixed turn slots (seat lead, lead+1, lead+2), each an ask followed by an update guarded by game_over == false: The step list is flat, so the rotating order is unrolled into slots whose seat is computed from lead.
- A tie for fewest cards_left is shown as a shared win: The engine has no separate draw; players level at the top share the win, which stands for the source's draw.
- Removed cards (cleared piles and played C cards) are dropped from all lists rather than kept in a discard list: The rules only say they leave the game and never refer to them again.

## Unsupported (needs engine work)

- none
