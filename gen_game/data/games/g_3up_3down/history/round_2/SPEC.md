# 3Up Shed (Equal Turns)

Three players shed a 10-card hand onto a shared pile by matching or beating its top rank. They wipe the pile with three of a rank or a Clear, or pick it up when stuck. The first seats to run out of cards win, and every seat gets the same number of turns.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 30
- `min_rank` = 1
- `max_rank` = 9
- `copies_per_rank` = 3
- `clear_cards` = 3
- `low_stack_size` = 9
- `mid_stack_size` = 9
- `high_stack_size` = 9
- `clear_stack_size` = 3
- `cards_dealt_per_stack` = 3
- `clears_dealt_per_seat` = 1
- `starting_hand_size` = 10
- `up_pile_size` = 3
- `hand_after_up` = 7
- `max_copies_per_play` = 3
- `run_wipe_threshold` = 3
- `max_rounds` = 20
- `empty_top_rank` = 0
- `clear_sort_value` = 10

## Round

1. **update** (all players): round += 1; lead = ((round - 1) mod 3) + 1.
2. **ask** (each player in turn, starting at seat lead, then lead+1, then lead+2 (seat 3 is followed by seat 1); a seat with out = true is skipped): Right after each seat answers, its choice is applied as in the next step, so the next seat sees the updated pile.
3. **update** (the seat that just answered (applied after each turn)): Rank play r x k: move k cards of rank r from the source to pile; if top_rank == r then run_count += k, else run_count = k; top_rank = r; if run_count >= 3, clear pile (removed from game), top_rank = 0, run_count = 0. C: remove the C from the source and clear pile (both removed from game), top_rank = 0, run_count = 0. PICK UP: append all of pile to hand, pile = [], picked_up += 1, top_rank = 0, run_count = 0. Then hand_count = len(hand), up_count = len(up_pile), cards_left = hand_count + up_count; if cards_left == 0 then out = true.
4. **update** (all players): After all three turns: if the number of seats with out = true is at least 1, set game_over = true.
5. **check** (all players): End the game if game_over == true or round == 20; otherwise start the next round.

## Ending

- ends when: game_over == true or round >= 20
- ranked by: `0 - you.cards_left` (the highest wins; players level at the top share the win)
- decided by: Fewest cards_left wins. If a seat went out, every seat with cards_left = 0 shares the win (one such seat wins alone; two or three is a draw). If round 20 ends with nobody out, the seat with the fewest cards_left wins, and seats tied for fewest share it (a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. Rotating the lead over 3 seats and the equal-turns ending are built for that count.
- No talk step before turns: The source has no talk. Turns are sequential and fully specified, so adding talk would add a mechanic.
- rank_by = 0 - cards_left for both endings: A seat that is out has cards_left 0, the lowest possible. Ranking by fewest cards therefore picks exactly the out seats when game_over is true, and the fewest-cards seat at round 20.
- C sorts as 10 in up_offer: The source says C counts above 9, so a numeric stand-in of 10 keeps the ordering.

## Simplifications

- A shared top rank is a shared win: The engine has no separate draw. The source's draw (two or three seats out, or a tie for fewest at round 20) becomes a shared win among the tied seats.
- The turn rotation is described as 'each player in turn starting at seat lead': The step list is flat. The three turns are one ask over the seats in rotated order, each followed by its update, with out seats skipped.

## Unsupported (needs engine work)

- none
