# Lost Cities: Embargo

Two players build ascending colour columns over two mirrored hands from one recorded shuffle. Each player secretly embargoes one opponent colour per hand, which halves a positive column score in that colour.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 30
- `colours` = 3
- `lowest_number_card` = 2
- `highest_number_card` = 10
- `wagers_per_colour` = 1
- `hands` = 2
- `turns_per_hand` = 20
- `total_rounds` = 40
- `hand_size` = 5
- `draw_pile_size` = 20
- `column_offset` = 8
- `wager_multiplier` = 1.5
- `long_column_threshold` = 5
- `long_column_bonus` = 10
- `illegal_play_penalty` = 1
- `embargo_divisor` = 2

## Round

1. **update** (table): When round == 1: draw all 30 cards at random into match_order. Seat 1 hand = match_order[1..5]. Seat 2 hand = match_order[6..10]. deck = match_order[11..30]. draw_count = 20.
2. **update** (table): When round == 21: hand_number = 2. Clear red_col, green_col and blue_col for both seats. Clear red_pile, green_pile and blue_pile and their tops. Set penalty = 0 for both seats and clear announcements. Without reshuffling: Seat 2 hand = match_order[1..5], Seat 1 hand = match_order[6..10], deck = match_order[11..30], draw_count = 20.
3. **poll** (all players): embargo = the answer, kept secret (ally) until end-of-hand scoring.
4. **update** (table): Set active_seat: if hand_number == 1 then (1 if round is odd else 2), otherwise (2 if round is odd else 1). Set last_discard = ''.
5. **sync** (all players): Each seat sees its own hand. Both see all columns, red_top, green_top, blue_top, draw_count and the announcements.
6. **ask** (seat active_seat): Records the chosen slot and action.
7. **update** (seat active_seat): Remove the chosen card from hand. DISCARD: append it to its colour's pile, set that colour's top = card, last_discard = card. PLAY of a number card: legal if it is higher than every number in that colour's column, and then it is appended to the column. PLAY of a Wager: legal if the column holds no number card, and then it is appended to the column. An illegal PLAY goes to its colour's pile as a discard: top = card, last_discard = card, penalty += 1.
8. **ask** (seat active_seat): Records the draw source.
9. **update** (seat active_seat): If a colour pile is chosen and it is non-empty and its top != last_discard: remove the top of that pile into hand slot 5 and reset that colour's top to the new top or ''. Otherwise remove deck[1] into hand slot 5 and set draw_count -= 1. The remaining cards close up to the left, so hand is ordered with the new card last.
10. **tell** (all players): Append to announcements and broadcast either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]' (illegal plays are also announced as discards), plus 'and drew from the draw pile' or 'and took [card] from the [colour] pile'. Penalties and totals are not announced.
11. **update** (all players): When round == 20 or round == 40: score each column. An empty column scores 0. Otherwise S = (sum of number cards) - 8. If S > 0 and the column holds the Wager, S = floor(S * 1.5). If the column has >= 5 cards, S += 10. If the column's colour equals the opponent's embargo and S > 0, S = floor(S / 2). hand_score = the sum of the three column scores - penalty. total += hand_score.
12. **tell** (all players): When round == 20 or round == 40: announce both seats' embargo, hand_score and total.
13. **update** (table): round += 1.
14. **check** (table): End the game if round > 40, otherwise continue.

## Ending

- ends when: round > 40 (after hand 2 is scored)
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's match total after both hands. The higher total wins, and equal totals share the win (a draw).

## Choices the source did not make

- Exactly 2 players: The designer fixed 2. The embargo and the mirrored hand swap are built around one opponent.
- No talk step: The source has no communication. With 2 players, free talk would only add cheap bluffing that the rules do not include.
- An illegal play counts as 'the card discarded this turn' for the draw fallback: The illegal card lands on the discard pile this turn exactly like a discard, and the announcement calls it a discard.
- Card codes R2..R10, RW and so on: Gives text tokens for list operations and arithmetic on the number part.

## Simplifications

- Slot and PLAY/DISCARD are combined into one 10-option choice: The engine takes one answer per question, and this keeps the two parts together.
- Discard piles are hidden lists with public top-card attributes: Only the top card is visible and takeable in the source.
- Hand setups and scoring are steps guarded by round == 1, 21, 20 and 40: The step list is flat. Single-step `when` conditions express the two hands without separate blocks.

## Unsupported (needs engine work)

- none
