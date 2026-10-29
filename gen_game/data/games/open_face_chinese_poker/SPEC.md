# Duplicate Open-Face Pairs

Two players build 1-2-2 card rows from mirrored deals over 4 hands. Rows must not foul. Players score row wins, scoops and royalties, and both players face the same cards in each pair of hands.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 32
- `card_value_min` = 1
- `card_value_max` = 8
- `copies_per_value` = 4
- `hands` = 4
- `rounds_per_hand` = 5
- `total_rounds` = 20
- `cards_per_seat_per_round` = 3
- `cards_kept_per_round` = 1
- `cards_discarded_per_round` = 2
- `cards_used_per_hand` = 30
- `unused_positions` = 2
- `front_slots` = 1
- `middle_slots` = 2
- `back_slots` = 2
- `front_multiplier` = 2
- `pair_bonus` = 100
- `row_win_points` = 1
- `scoop_bonus` = 3
- `foul_win_points` = 6
- `front_royalty_min_value` = 7
- `front_royalty` = 1
- `middle_pair_royalty` = 2
- `back_pair_royalty` = 1

## Round

1. **update** (table): When round_in_hand == 1 and hand_number is 1 or 3: shuffle deck into a new random fixed order.
2. **update** (all players): Deal by position. Take the first 3 cards of deck, append them to the back of deck, and copy them into the Seat X player's hand. Then take the next 3 cards the same way into the Seat Y player's hand. Seat X is Player A when hand_number is odd and Player B when it is even; Seat Y is the other player.
3. **sync** (all players): Each player privately sees their own hand, all placed rows, hand_number and round_in_hand.
4. **poll** (all players): chosen_card = the chosen value. Nobody sees the other's answer.
5. **poll** (all players): chosen_row = the named row. Nobody sees the other's answer.
6. **update** (all players): Place chosen_card in the first empty slot of chosen_row: front, else mid1 then mid2, else back1 then back2. If that row is full, place it in the first non-full row in the order Back, Middle, Front. Then empty hand: the 2 unkept cards are discarded unseen.
7. **tell** (all players): Announce both kept cards face up and the row each went to.
8. **update** (all players): Score the hand. front = 2*front. mid1 = mid1+mid2+100*(mid1==mid2), using the old values. back1 = back1+back2+100*(back1==back2), using the old values. fouled = (front > mid1) or (mid1 > back1). Copy front, mid1, back1 and fouled into seat_strengths. royalty = 0 if fouled, else (old front >= 7)*1 + (old mid1 == old mid2)*2 + (old back1 == old back2)*1. hand_score: if neither player fouled = rows won (1 per row with strictly higher strength than the opponent's) + 3 if all 3 rows won + royalty; if only the opponent fouled = 6 + royalty; if this player fouled = 0. total += hand_score.
9. **tell** (all players): Announce all six row strengths, both foul results and both hand scores.
10. **update** (table): If round_in_hand == 5: set every player's front, mid1, mid2, back1 and back2 to 0. If hand_number is odd, rotate 2 more cards from the front of deck to the back, so deck returns to its starting order. Then hand_number += 1 and round_in_hand = 1. Otherwise round_in_hand += 1.
11. **check** (table): End the game if hand_number > 4; otherwise continue.

## Ending

- ends when: hand_number > 4
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their match total, the sum of their four hand scores. The higher total wins, and equal totals share the win (a draw).

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer set 2, and the duplicate format mirrors one seat's deal onto the other, which only works with two seats. The strategy is to remember the cards seen in the odd hand and use them to predict the opponent's options in the even hand, and to balance foul risk against pairs.
- Player A is seat 1 and Player B is seat 2: The rules name players A and B but not their seats.
- No talk step: The rules have no communication, and in a two-player zero-sum game talk adds nothing to reason about.
- Row choice offers all three rows even when one is full: The rules let a player name a full row and apply a fallback, so the fallback is kept rather than hiding options.
- Strengths are stored back into front, mid1 and back1 at scoring: This follows the build note, so foul tests, comparisons and royalties are single expressions.

## Simplifications

- Fixed deck order is encoded by rotating dealt cards from the front of the deck list to the back, plus 2 extra rotations after each odd hand: The engine has no position lookup. Rotation keeps the order so the even hand repeats the odd hand's deal exactly.
- Row comparison uses a table list, seat_strengths, holding both players' strengths and fouls: The engine cannot compare one player's attribute directly to another's; a table copy is the documented workaround.
- Discards are simply removed from the hand list rather than kept in a discard pile: Discards are never shown or used again, so no pile is needed.

## Unsupported (needs engine work)

- none
