# Eleven Takes: Three Piles

Players play cards from hidden hands onto three shared piles in a clockwise number range, or take a pile into their hand and earn bulls that allow extra plays; the lowest ox-head penalty in hand wins.

Players: 3 to 4, best with 4

## Parameters

- `deck_low` = 1
- `deck_high` = 40
- `deck_size` = 40
- `oxheads_multiple_of_10` = 3
- `oxheads_multiple_of_5_not_10` = 2
- `oxheads_other` = 1
- `deck_total_oxheads` = 52
- `hand_size_start` = 6
- `pile_count` = 3
- `start_cards_per_pile` = 1
- `set_aside_with_4` = 13
- `set_aside_with_3` = 19
- `bull_supply_offset` = 1
- `legal_step_min` = 1
- `legal_step_max` = 6
- `legal_modulus` = 40
- `take_bull_threshold` = 3
- `bulls_for_first_extra` = 1
- `bulls_for_second_extra` = 2
- `max_cycles_with_4` = 10
- `max_cycles_with_3` = 12
- `max_turns_with_4` = 40
- `max_turns_with_3` = 36
- `empty_hand_penalty` = 0

## Round

1. **sync** (all players): Each player sees their own hand, and everyone sees the piles, every hand_size, bulls, bull_supply, cycle and last_action.
2. **ask** (the seat equal to active_seat): Sets action_kind to 'play' or 'take' and sets chosen_pile. A missing or invalid answer is replaced by taking the smallest pile, with ties broken A before B before C. Clears extra_stopped.
3. **update** (the seat equal to active_seat): When action_kind is 'play': remove X from hand, append X to the chosen pile, subtract 1 from hand_size, and set last_action to 'Seat s plays X on P'.
4. **ask** (the seat equal to active_seat, when action_kind is 'play' and bulls >= 1): If 'stop', set extra_stopped to true. Otherwise remove the card from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action.
5. **ask** (the seat equal to active_seat, when action_kind is 'play', bulls >= 2 and extra_stopped is false): If a card is given, remove it from hand, append it to the chosen pile, subtract 1 from hand_size, and add it to last_action.
6. **update** (the seat equal to active_seat): When action_kind is 'take': set taken_size to the length of the chosen pile, append all of its cards to hand, set the pile to empty, and add taken_size to hand_size.
7. **ask** (the seat equal to active_seat, when action_kind is 'take'): Remove that card from hand, set the chosen pile to a list holding only that card, subtract 1 from hand_size, and set last_action to 'Seat s takes P (k cards) and restarts it with Y'.
8. **update** (the seat equal to active_seat): When action_kind is 'take' and taken_size >= 3: if bull_supply > 0, subtract 1 from bull_supply and add 1 to the taker's bulls. Otherwise, if any opponent has bulls > 0, take 1 bull from the opponent with the most bulls, breaking ties by the smallest (seat - active_seat) mod N, and add it to the taker's bulls. If no opponent has a bull, nothing happens.
9. **update** (the seat equal to active_seat): If the active player's hand_size = 0, set ending_triggered to true.
10. **update** (all players): If active_seat = N, add 1 to cycle and set active_seat to 1. Otherwise add 1 to active_seat.
11. **update** (all players): When active_seat = 1 and (ending_triggered is true or cycle >= max_cycles): set every player's penalty to the sum, over the cards in their hand, of 3 for a multiple of 10, 2 for a multiple of 5 that is not a multiple of 10, and 1 otherwise. An empty hand gives 0.
12. **check** (all players): End the game if active_seat = 1 and (ending_triggered is true or cycle >= max_cycles). Otherwise continue with the next turn.

## Ending

- ends when: active_seat = 1 and (ending_triggered = true or cycle >= max_cycles)
- ranked by: `0 - you.penalty` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is minus their penalty, the total ox-heads in their hand at the end. The lowest penalty wins, and players tied for the lowest share the win as a draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer gives 3-4 and suggests 4. With fewer than 3 there are too few rivals to steal bulls from or to dump piles on. With more than 4 the 40-card deck cannot deal 6 cards each plus 3 piles with cards left to set aside as the rules intend, and the bull supply and cycle limits are defined only for 3 and 4.
- One engine round is one player's turn, with active_seat cycling 1..N: The rules say a turn is one engine round. The end check runs only after seat N's turn, so every player gets the same number of turns.
- max_cycles = 18 - 2*N and bull_supply = N - 1: These write the source's per-count numbers (10 cycles with 4 and 12 with 3; supply 3 with 4 and 2 with 3) as rules over the count.
- Penalty is computed only at the end of the game: A running public penalty would leak hidden hand contents. The rules make only hand size and bulls public.
- No pre-move talk step: The source has no talk, and adding it would add a mechanic. Play is purely sequential and every action is public.
- Ranking is 0 - penalty: Lowest penalty wins. Negating it lets the highest rank_by win, and ties at the top share the win, which matches the source's draw.
- The steal tie-break uses the smallest (seat - active_seat) mod N: This is 'the first such player in seat order after the taker' written as arithmetic.

## Simplifications

- Only legal plays are offered, so an illegal PLAY choice cannot be made. The fallback 'take the smallest pile' applies when a seat gives no valid answer.: The engine never offers a seat an action it may not take. The fallback still covers the same failure case.
- Only legal extra cards are offered, plus 'stop': This has the same effect as the rule that an illegal extra card is ignored and ends the run.
- The branches after the main action (extra cards for a play, restart card and bulls for a take) are separate steps, each with its own arithmetic 'when' condition: The step list is flat. A per-step condition on action_kind reproduces both branches without choosing between blocks of steps.

## Unsupported (needs engine work)

- none
