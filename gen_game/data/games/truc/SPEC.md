# Truc Duel

Two players play three-card hands of three tricks. They can raise the stakes, fold or re-raise, and the first to 12 points wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 32
- `ranks` = 8
- `copies_per_rank` = 4
- `hand_size` = 3
- `tricks_per_round` = 3
- `strength_7` = 8
- `strength_8` = 7
- `strength_A` = 6
- `strength_K` = 5
- `strength_Q` = 4
- `strength_J` = 3
- `strength_10` = 2
- `strength_9` = 1
- `value_both_stay` = 1
- `value_accept` = 2
- `value_four` = 4
- `value_both_raise` = 4
- `fold_payout` = 1
- `win_target` = 12
- `round_cap` = 30
- `starting_score` = 0

## Round

1. **update** (all players): round_number += 1. deck is reset to the full 32-card pack. Each player's hand, played_cards, raise_choice and order_choice are emptied, and tricks_won = 0. round_value = 0, raiser = 0, response = '', folded = false, trick1_winner = trick2_winner = trick3_winner = round_winner = 0.
2. **update** (each player in turn): Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck.
3. **sync** (all players): Each player privately sees their own hand (strengths shown with rank names); the opponent's hand stays hidden.
4. **poll** (all players): The chosen card is removed from hand and appended to played_cards. An answer that is not in the hand plays the first-listed card of hand. seat1_card and seat2_card are set to the two cards.
5. **update** (all players): trick1_winner = 1 if seat1_card > seat2_card, 2 if seat2_card > seat1_card, else 0. The trick winner's tricks_won += 1.
6. **tell** (all players): Announce both trick-1 cards and trick1_winner (or 'spoilt').
7. **poll** (all players): Each player's raise_choice is set, then revealed to both.
8. **update** (all players): If both raise_choice = STAY: round_value = 1. If both = TWO MORE: round_value = 4. If exactly one = TWO MORE: raiser = that seat.
9. **ask** (the seat that is not raiser (the responder), only when raiser != 0): response is set and revealed.
10. **update** (all players): If response = ACCEPT: round_value = 2. If response = FOUR: round_value = 4. If response = FOLD: the raiser's score += 1, folded = true, round_winner = raiser, and steps 11 to 13 do not apply this round.
11. **poll** (all players, only when folded = false): order_choice is set. An invalid answer uses dealt order. Both remaining cards are appended to played_cards in the chosen order and removed from hand.
12. **update** (all players, only when folded = false): Trick 2: seat1_card and seat2_card = each player's 2nd played card. trick2_winner = higher seat, or 0 if equal; the winner's tricks_won += 1. Trick 3: the same with the 3rd played card, giving trick3_winner. Then round_winner = the seat with more tricks_won. If tricks_won are equal, round_winner = the first non-zero of trick1_winner, trick2_winner, trick3_winner, or 0 if all are 0. If round_winner != 0, that seat's score += round_value.
13. **tell** (all players): Announce all played cards, the trick winners, round_winner (or 'void' or 'fold'), round_value and both scores.
14. **check** (all players): End the game if any player's score >= 12 or round_number >= 30; otherwise repeat the round.

## Ending

- ends when: max(score over players) >= 12 or round_number >= 30
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: The higher score wins. The game ends as soon as one player reaches 12 or more; only one player scores per round, so that player has the higher score. At the 30-round cap the higher score wins, and equal scores share the win (a draw).

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer set 2. The game is a heads-up duel of stakes, folds and trick order, and a third player would break the one-raiser/one-responder structure.
- Cards are stored as their strength numbers 1 to 8, with rank names used in what players are shown: Trick comparison is then plain arithmetic, and suits do not matter.
- No talk phase: The rules say there is none; all information comes from revealed cards and choices.
- The order poll is a choice between the two orderings, not free text: It still offers exactly the two legal orders. The dealt-order fallback is kept for any invalid answer.
- The garbled tie clause ('0-0 with three... see below') is read as: equal trick counts go to the earliest non-spoilt trick's winner, and all three spoilt is void: This is the only consistent reading, and the next bullet of the rules covers the all-spoilt case.
- 'The raiser may not fold' after FOUR, and 'no one may fold' after both raise, are built as no further question being asked: The rules give no later folding opportunity, so these lines mean the stakes are fixed.
- A draw at the round cap is equal scores sharing the win: The ranking treats players level at the top as sharing the win.

## Simplifications

- Trick comparison uses table scratch attributes seat1_card and seat2_card: The engine has no direct player-to-player attribute comparison; a table copy is the stated workaround.
- Reshuffling the full pack is a reset of the deck list followed by random draws: The engine draws by picking at random from a list, which is the same as shuffling.

## Unsupported (needs engine work)

- none
