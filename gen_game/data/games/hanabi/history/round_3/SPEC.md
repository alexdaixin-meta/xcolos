# Hanabi Duo

A cooperative two-player card game: each player sees only the partner's two cards, and the pair use hints, plays and discards to build Red and Blue piles from 1 to 3, scoring 4 or more to win together.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 12
- `colours` = 2
- `red_colour_code` = 1
- `blue_colour_code` = 2
- `copies_of_rank_1_per_colour` = 3
- `copies_of_rank_2_per_colour` = 2
- `copies_of_rank_3_per_colour` = 1
- `hand_size` = 2
- `cards_left_after_deal` = 8
- `starting_hint_tokens` = 3
- `max_hint_tokens` = 3
- `starting_fuses` = 3
- `hint_cost` = 1
- `discard_gain` = 1
- `failed_play_fuse_loss` = 1
- `pile_start` = 0
- `pile_max` = 3
- `max_rounds` = 12
- `max_score` = 6
- `win_threshold` = 4
- `empty_slot_code` = 0

## Round

1. **sync** (seat 1): Seat 1 is shown: seat 2's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 1's own card_a and card_b are not shown.
2. **ask** (seat 1): game.action = the chosen option
3. **update** (seat 1): PLAY X (X = A or B), with c = seat 1 card_X: if c == 0, nothing changes. Otherwise colour = floor(c/10) and rank = c mod 10. If (colour == 1 and rank == red_pile + 1), then red_pile += 1. Else if (colour == 2 and rank == blue_pile + 1), then blue_pile += 1. Otherwise append c to discard and fuses -= 1. In every non-empty case, card_X is vacated (marked for drawing). DISCARD X: if c != 0, append c to discard, hints = min(3, hints + 1), and vacate card_X; if c == 0, nothing changes. HINT (colour or rank) of partner's X, with p = seat 2 card_X: if hints >= 1 and p != 0, then hints -= 1 and v = floor(p/10) (colour) or p mod 10 (rank). For each of seat 2's slots Y with card_Y != 0, append 'is V' to note_Y if the matching value equals v, else append 'not V'. V is the colour name (Red for 1, Blue for 2) or the rank number. Otherwise nothing changes and the turn is wasted. Set last_action to the option, any revealed code, success or failure, and any hint named.
4. **update** (seat 1): If seat 1's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = [].
5. **update** (all players): Each seat's score = red_pile + blue_pile.
6. **tell** (all players): Announce last_action: the option seat 1 chose, any card code revealed, whether a play succeeded, and the hint named. Also announce red_pile, blue_pile, hints and fuses.
7. **check** (all players): End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3); otherwise continue.
8. **sync** (seat 2): Seat 2 is shown: seat 1's card_a and card_b; note_a and note_b of both seats; red_pile, blue_pile, hints, fuses; discard and deck_left; last_action. Seat 2's own cards are not shown.
9. **ask** (seat 2): game.action = the chosen option
10. **update** (seat 2): Same resolution as seat 1's resolution step, with seat 2 as the active seat and seat 1 as the partner: plays and discards act on seat 2's card_X, and hints act on seat 1's cards and notes. Set last_action accordingly.
11. **update** (seat 2): If seat 2's slot X was vacated this turn: if deck_left > 0, then card_X = deck[0], remove deck[0], deck_left -= 1, note_X = []. If deck_left == 0, then card_X = 0 and note_X = [].
12. **update** (all players): Each seat's score = red_pile + blue_pile. round_number += 1.
13. **tell** (all players): Announce last_action for seat 2's turn (option, revealed card, success or failure, hint named), plus red_pile, blue_pile, hints and fuses.
14. **check** (all players): End the game if fuses == 0 or (red_pile == 3 and blue_pile == 3) or round_number >= 12; otherwise continue.

## Ending

- ends when: fuses == 0 OR (red_pile == 3 AND blue_pile == 3) OR round_number >= 12
- results: both seats win, no seat wins
- decided by: If red_pile + blue_pile (each seat's score) >= 4, the result is 'both seats win'; otherwise it is 'no seat wins'. This applies whichever ending condition triggered.

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the game at 2 and the card counts, hand size and hint structure are built for a pair. The minimum is 2 because each player needs a partner to see their cards. The maximum stays 2 because the rules define 'partner' as a single other player. Strategy lies in choosing hints that convey the most, inferring meaning from a partner's hint choice, and deciding when to risk a play versus discard to regain tokens.
- No talk step: The rules forbid all communication besides the 8 actions; information must flow only through hints.
- All 8 options are always offered: The source specifies a result (nothing happens) for empty-slot plays and discards and for hints without tokens, so those choices are legal moves, just wasted ones.
- Results named 'both seats win' and 'no seat wins': The game is cooperative with one shared outcome; the source gives no names for the results.
- Notes stored as one public list per slot: Both players see all four cards' notes, so each slot's notes are a public list that is cleared on draw.
- Discarding an empty slot gains no hint token: The source says 'If the slot is empty, nothing happens', which includes the token gain.

## Simplifications

- A turn is split into one resolution update and one draw update: The engine applies state changes as separate update steps; the order (resolve, then draw, then score) matches the source.
- The two turns of a round are written as two mirrored step blocks: The step list is flat, so seat 1's and seat 2's turns are each written out in order, with a check after each turn so the game ends immediately.

## Unsupported (needs engine work)

- none
