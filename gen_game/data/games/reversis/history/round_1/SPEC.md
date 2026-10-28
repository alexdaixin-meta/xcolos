# Short Reversis

A 4-player trick-avoidance card game over 4 hands with a 24-card deck. Players pass cards, then try not to take points; whoever takes all 6 tricks in a hand (a reversis) scores 0 and every other player scores 15. The lowest total after 4 hands wins.

Players: 4 to 4, best with 4

## Parameters

- `num_players` = 4
- `deck_size` = 24
- `num_hands` = 4
- `cards_dealt_per_player` = 6
- `pass_count` = 2
- `last_passing_hand` = 3
- `tricks_per_hand` = 6
- `rounds_per_hand` = 7
- `total_rounds` = 28
- `points_ace` = 4
- `points_king` = 3
- `points_queen` = 2
- `points_jack` = 1
- `points_quinola_jack_of_hearts` = 5
- `points_nine` = 0
- `points_eight` = 0
- `points_total_per_hand` = 44
- `reversis_tricks` = 6
- `reversis_taker_score` = 0
- `reversis_other_score` = 15
- `rank_value_ace` = 6
- `rank_value_king` = 5
- `rank_value_queen` = 4
- `rank_value_jack` = 3
- `rank_value_nine` = 2
- `rank_value_eight` = 1

## Round

1. **update** (all players): One round of the script is one hand. hand_number += 1. deck is reset to all 24 cards. Every hand, played_cards, pass_1, pass_2 and played_card is cleared. Each player draws 6 cards at random from deck into their hand (24 draws in all, emptying the deck). trick_number = 0. leader = hand_number.
2. **sync** (all players): Each player privately sees their own hand of 6 cards.
3. **poll** (all players): when hand_number <= 3: pass_1 = the chosen card. Nobody sees any choice until all are in.
4. **poll** (all players): when hand_number <= 3: pass_2 = the chosen card.
5. **update** (all players): when hand_number <= 3: each player's pass_1 and pass_2 are removed from their hand and appended to the receiver's hand. The receiver is seat (seat mod 4)+1 (left) in hand 1, seat ((seat+2) mod 4)+1 (right) in hand 2, and seat ((seat+1) mod 4)+1 (across) in hand 3. Each passer and receiver is told privately which two cards moved. Every hand again holds 6 cards.
6. **tell** (all players): Announce: 'Passing is complete.' In hand 4 the announcement says there was no pass.
7. **repeat** (all players): Run the next 6 steps (one trick) until trick_number = 6.
8. **ask** (seat leader): played_card = the chosen card; led_suit = its suit; the card is removed from hand and appended to played_cards; the play is announced to everyone.
9. **ask** (seat (leader mod 4)+1): played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
10. **ask** (seat ((leader+1) mod 4)+1): played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
11. **ask** (seat ((leader+2) mod 4)+1): played_card = the chosen card; removed from hand and appended to played_cards; announced to everyone.
12. **update** (all players): trick_winner = the seat whose played_card has suit led_suit and the highest rank value (A=6, K=5, Q=4, J=3, 9=2, 8=1). That seat's hand_points += the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1 except JH=5, 9=0, 8=0). That seat's tricks_won += 1. leader = trick_winner. trick_number += 1.
13. **tell** (all players): Announce: 'Seat {trick_winner} wins trick {trick_number} and takes {points} points.' with each player's hand_points and tricks_won.
14. **update** (all players): End of hand. If some player has tricks_won = 6, that player's hand_score = 0 and every other player's hand_score = 15. Otherwise each player's hand_score = hand_points. Each player's total += hand_score. Then hand_points = 0 and tricks_won = 0 for every player.
15. **tell** (all players): Announce each player's hand_score and running total, and whether a reversis happened.
16. **check** (all players): If hand_number = 4, end the game; otherwise start the next hand.

## Ending

- ends when: hand_number = 4 after the end-of-hand scoring
- ranked by: `0 - you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their running total after 4 hands, and lower is better. The player with the lowest total wins; players tied for the lowest total share the result (the source calls this a draw).

## Choices the source did not make

- 4 players, minimum 4 and maximum 4: The designer fixed 4 seats. The deck of 24 cards deals exactly 6 to each of 4 players, the left/right/across passing needs exactly 4 seats, and the 15-point reversis payment is set for 3 opponents.
- No talk step before plays: The source has no table talk. Adding it would add a mechanic, and in a trick game it would leak hidden hands.
- One script round equals one hand (deal, pass, then 6 tricks run by a repeat): The source's 7 rounds per hand (1 pass + 6 tricks) map onto one script round, and the game ends after 4 such rounds, giving 28 source rounds in all.
- Cards coded as rank+suit text (e.g. 'JH'), with rank values A=6, K=5, Q=4, J=3, 9=2, 8=1 for comparing: Finding the trick winner needs a number to compare; these values keep the source order A > K > Q > J > 9 > 8.
- Strategy at the table: Players pass away dangerous high cards and the Quinola, then duck under the led card and discard point cards when void. A player with a very strong hand may instead aim to win all 6 tricks for a reversis, so opponents must watch for it and take one trick to stop it.

## Simplifications

- Passing 2 cards is two simultaneous polls of one card each: A question takes a single choice from a list. The second poll excludes the first card, and no card moves until both polls are done, so passing stays simultaneous and secret.
- The winner is computed as the highest of 0 - total, and a tie at the lowest total is a shared result: The engine ranks by highest value and shares ties at the top. This matches 'lowest total wins, a tie for lowest is a draw'.

## Unsupported (needs engine work)

- none
