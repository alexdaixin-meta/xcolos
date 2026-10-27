# Love Letter Duel: Long Courtship

A two-player Love Letter duel over exactly 40 turns. Each turn one player draws, discards one of two cards and resolves its effect. Winning a hand earns a token; most tokens wins, with total discarded ranks as the tie-break.

Players: 2 to 2, best with 2

## Parameters

- `total_rounds` = 40
- `deck_size` = 16
- `guard_count` = 5
- `priest_count` = 2
- `baron_count` = 2
- `handmaid_count` = 2
- `prince_count` = 2
- `king_count` = 1
- `countess_count` = 1
- `princess_count` = 1
- `guard_rank` = 1
- `priest_rank` = 2
- `baron_rank` = 3
- `handmaid_rank` = 4
- `prince_rank` = 5
- `king_rank` = 6
- `countess_rank` = 7
- `princess_rank` = 8
- `out_of_play_size` = 6
- `face_up_out_of_play` = 5
- `burned_cards` = 1
- `cards_dealt_per_player` = 1
- `deck_count_after_deal` = 8
- `guard_guess_min` = 2
- `guard_guess_max` = 8
- `tokens_per_hand_won` = 1
- `starting_tokens` = 0
- `starting_career_sum` = 0
- `starting_active_seat` = 1
- `rank_tiebreak_multiplier` = 1000

## Round

1. **update** (all players): round_number += 1; new_hand = 0; token_awarded = 0.
2. **update** (all players): When hand_over = 1: empty every hand, every player's discards, burned_card and face_up, and set deck to all 16 ranks. Draw 1 random rank from deck into burned_card, then 5 random ranks from deck into face_up. Draw 1 random rank from deck into each player's hand. Set deck_count = 8. For both players set protected = 0, eliminated = 0 and discard_sum = 0. Set hand_over = 0 and new_hand = 1.
3. **tell** (all players): When new_hand = 1, announce: 'The face-up out-of-play cards are ranks {face_up}.'
4. **update** (seat active_seat): Set the active player's protected = 0. Move 1 random rank from deck to the active player's hand; deck_count -= 1. Privately tell the active player: 'You kept rank X and just drew rank Y.'
5. **ask** (seat active_seat): Store the chosen rank in discard_choice.
6. **update** (seat active_seat): Countess: if the active player's hand contains 7 and also contains 5 or 6, set discard_choice = 7.
7. **update** (seat active_seat): Move one card of rank discard_choice from the active player's hand to their discards. Add discard_choice to their discard_sum and career_sum. Announce 'Seat s discards rank r (name).'
8. **ask** (seat active_seat): When discard_choice = 1: store the number in guess.
9. **update** (all players): When discard_choice = 1: if the opponent's protected = 1, announce no effect. Otherwise, if the opponent's hand card = guess, set the opponent's eliminated = 1 and announce a hit; if not, announce a miss.
10. **update** (seat active_seat): When discard_choice = 2: if the opponent's protected = 1, announce no effect. Otherwise privately tell the active player the opponent's hand rank, and announce 'Seat s looked at Seat o's card.'
11. **update** (all players): When discard_choice = 3: if the opponent's protected = 1, announce no effect. Otherwise compare the two hand cards. The owner of the lower one gets eliminated = 1, and the loser and the losing rank are announced. If the cards are equal, announce a tie and nobody is out.
12. **update** (seat active_seat): When discard_choice = 4: set the active player's protected = 1 and announce it.
13. **update** (all players): When discard_choice = 5: the target is the opponent, or the active player if the opponent's protected = 1. Move the target's hand card to their discards, add its rank to their discard_sum and career_sum, and announce the rank. If the rank was 8, set the target's eliminated = 1. Otherwise, if deck_count > 0, move 1 random rank from deck to the target's hand and deck_count -= 1; if deck_count = 0, move the burned_card rank to the target's hand.
14. **update** (all players): When discard_choice = 6: if the opponent's protected = 1, announce no effect. Otherwise swap the two players' hand lists and announce the swap.
15. **update** (seat active_seat): When discard_choice = 8: set the active player's eliminated = 1 and announce it.
16. **update** (all players): Showdown, when the sum of eliminated = 0 and (deck_count = 0 or round_number = 40): announce both hand ranks. The owner of the lower hand card gets eliminated = 1. If the cards are equal, the owner of the lower discard_sum gets eliminated = 1. If those are also equal, announce that the hand is tied and set hand_over = 1.
17. **update** (all players): Award, when the sum of eliminated = 1: the player with eliminated = 0 gains tokens += 1, and the new total is announced. Set hand_over = 1, token_awarded = 1, and active_seat = the seat of the eliminated player.
18. **update** (all players): Pass, when token_awarded = 0: active_seat = 3 - active_seat.
19. **check** (all players): End the game if round_number = 40; otherwise continue.

## Ending

- ends when: round_number = 40
- ranked by: `you.tokens * 1000 + you.career_sum` (the highest wins; players level at the top share the win)
- decided by: The player with more tokens wins. If tokens are equal, the higher career_sum wins. If both are equal, the players share the result as a draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed the duel at 2. All card effects target 'the opponent', and the game is two-person deduction and bluffing about one hidden card.
- No talk step: The source has no table talk. Adding it would be a new mechanic.
- Out-of-play split into burned_card (hidden) and face_up (public): Position 1 is face down while positions 2-6 are face up, so they need different visibility.
- Ranking expression tokens*1000 + career_sum: career_sum can never reach 1000 in 40 rounds (at most about 16 per round), so tokens come first and career_sum breaks ties. Equal values share the win, which is the draw.
- When the hand holds 7 with 5 or 6, only 7 is offered: A seat is never offered what it may not do. The Countess step still enforces it.
- Scratch flags new_hand, token_awarded and round_number added: Needed to condition the face-up announcement, the pass step and the round-40 showdown with arithmetic.

## Simplifications

- Deck draws are random picks from the deck list instead of taking the top card of one shuffle per hand: The engine draws at random. The deck order is hidden and unseen, so each draw has the same distribution as a single shuffle.

## Unsupported (needs engine work)

- none
