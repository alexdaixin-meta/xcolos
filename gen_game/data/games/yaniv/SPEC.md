# Row Yaniv

A simultaneous-choice take on Yaniv: each round every player secretly chooses to call YANIV, draw blind or take from a public offer row, and sheds a card (with any matches). The lowest hand at showdown avoids penalty, and the lowest penalty total wins.

Players: 2 to 4, best with 3

## Parameters

- `deck_size` = 54
- `joker_count` = 2
- `joker_value` = 0
- `copies_per_value_1_to_9` = 4
- `ten_value_cards` = 16
- `ten_value` = 10
- `slots_per_player` = 3
- `cards_dealt_per_player` = 3
- `initial_offer_row_length` = 1
- `max_rounds` = 24
- `yaniv_threshold` = 10
- `asaf_penalty` = 20
- `no_noncaller_n` = 99
- `end_penalty` = 50
- `initial_penalty` = 0
- `empty_slot_code` = -1

## Round

1. **update** (all players): When new_hand is true: draw_pile is set to the full 54-card list [0,0, four each of 1-9, sixteen 10s]; all slots are set to -1; dead_pile is emptied; in seat order, each player draws 3 cards at random from draw_pile into c1, c2 and c3 (removed from draw_pile); one more random card from draw_pile becomes offer_row = [that card]; new_hand = false. Then hand_total, card_count and draw_pile_size are recomputed.
2. **sync** (all players): Each player privately sees their own c1, c2, c3 and hand_total.
3. **tell** (all players): Announce offer_row with positions and values, dead_pile, draw_pile_size, priority_seat and every player's card_count.
4. **update** (all players): Reset for the round: is_caller = false, shed_values = [], claimed = [], any_valid_yaniv = false, showdown = false.
5. **poll** (all players): Stored privately in action; no answer is shown until all are in.
6. **poll** (all players): Stored privately in take_pos (used only for TAKE).
7. **poll** (all players): Stored in shed_slot; if that slot is -1, shed_slot is set to the lowest-numbered non-empty slot.
8. **update** (all players): YANIV check: for each player with action = YANIV, if hand_total <= 10 then is_caller = true, otherwise action = DRAW and the YANIV is announced as invalid. any_valid_yaniv = (count of is_caller > 0).
9. **update** (all players): SHED, when any_valid_yaniv is false: each player appends the value in their shed slot to shed_values, then for each of their other slots, in slot order, holding that same value, appends it and sets that slot to -1. The shed slot is set to -1. Every player's shed_values is announced.
10. **update** (each player in turn, starting at priority_seat and wrapping): TAKE, when any_valid_yaniv is false: for each player with action = TAKE in that order, if take_pos is not in claimed, the shed slot is set to offer_row[take_pos], take_pos is appended to claimed, and the take is announced; otherwise action = DRAW.
11. **update** (each player in turn, starting at priority_seat and wrapping): DRAW, when any_valid_yaniv is false: for each player with action = DRAW in that order, one random card is removed from draw_pile and placed in the shed slot, told only to that player; draw_pile_size decreases by 1.
12. **update** (all players): ROW UPDATE, when any_valid_yaniv is false: offer_row cards at positions not in claimed are appended to dead_pile; offer_row = the concatenation of shed_values from seat 1 upward. hand_total and card_count are recomputed, and every card_count and draw_pile_size is announced.
13. **sync** (all players): Each player privately sees their updated slots and hand_total.
14. **update** (all players): showdown = any_valid_yaniv OR draw_pile_size < number of players OR round = 24. When showdown is true: last_hand_total = hand_total for every player (all hands revealed); min_caller_h = the lowest hand_total among is_caller players (99 if none); min_noncaller_h = the lowest among the others (99 if none); min_h = the lowest hand_total overall.
15. **update** (all players): SCORING, when showdown is true. With any_valid_yaniv: a caller adds 0 if hand_total = min_caller_h and min_caller_h < min_noncaller_h, otherwise adds hand_total + 20; a non-caller adds 0 if hand_total <= min_caller_h, otherwise adds hand_total. Without any_valid_yaniv: a player adds 0 if hand_total = min_h, otherwise adds hand_total. Then max_penalty = the highest penalty, new_hand = true, and all hands and penalty totals are announced.
16. **update** (all players): priority_seat = (priority_seat mod number of players) + 1; round increases by 1.
17. **check** (all players): End the game if (showdown is true and max_penalty >= 50) or round > 24; otherwise continue.

## Ending

- ends when: (showdown == true and max_penalty >= 50) or round > 24
- ranked by: `0 - you.penalty` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their penalty total; the lowest penalty wins, and players tied for the lowest share the win (a draw among them).

## Choices the source did not make

- 2 to 4 players, suggested 3: The designer suggested 3, which is kept. The minimum is 2 because two players still race to a low hand, contest the row and time YANIV against Asaf. The maximum is 4 because each hand uses 3 cards per player plus the row, and more seats make take collisions and draws so frequent that one player's choice matters little.
- Empty slots are coded as -1: A Joker is worth 0, so 0 cannot also mean empty.
- No talk phase: The rules say there is no discussion phase.
- Strategy exists: Thoughtful players track the dead pile and offer row to count cards, set up pairs to shed several cards at once, avoid contested row positions, and time YANIV to avoid being undercut (Asaf).
- The end check uses max_penalty after a showdown: This keeps the 50-point condition arithmetic on a table attribute.

## Simplifications

- The three simultaneous answers are three consecutive polls: A question takes one answer. Answers are stored privately and never shown between polls, so the choices stay simultaneous.
- Shuffling and drawing from the top are modelled as random draws from the draw_pile list: Drawing at random from an unordered hidden list is equivalent to drawing the top card of a shuffled pile.
- Skipping steps 6-9 after a valid YANIV is done with a per-step condition (any_valid_yaniv is false): The step list is flat, but single steps can carry arithmetic conditions.

## Unsupported (needs engine work)

- none
