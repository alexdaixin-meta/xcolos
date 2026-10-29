# Quick Reversis

A four-player trick-avoidance card game over 4 hands of 6 tricks: take as few card points as possible, unless you take every trick of a hand (a reversis), which wipes that hand's points for you and charges 15 to each opponent; the lowest total wins.

Players: 4 to 4, best with 4

## Parameters

- `deck_size` = 24
- `cards_per_suit` = 6
- `suits` = 4
- `cards_dealt_per_player` = 6
- `hands` = 4
- `tricks_per_hand` = 6
- `total_rounds` = 24
- `ace_points` = 4
- `king_points` = 3
- `queen_points` = 2
- `jack_points` = 1
- `nine_points` = 0
- `eight_points` = 0
- `quinola_points` = 5
- `points_per_hand` = 44
- `reversis_subtract` = 44
- `reversis_bonus_to_others` = 15
- `rank_ace` = 6
- `rank_king` = 5
- `rank_queen` = 4
- `rank_jack` = 3
- `rank_nine` = 2
- `rank_eight` = 1
- `sweeper_none_code` = 0

## Round

1. **update** (all players): round += 1; if (round - 1) % 6 == 0: hand_number += 1, deck is reset to all 24 cards, every player's hand is cleared and tricks_this_hand is set to 0, then 6 cards are dealt to each player by random draws (each card is removed from deck and appended to that player's hand), leader = hand_number, and sweeper = 0 (none). Every player's played_card is cleared.
2. **sync** (all players): Each player is sent their own hand, plus the public total, leader, round, hand_number and sweeper.
3. **ask** (the seat equal to leader): The card is removed from the leader's hand and set as the leader's played_card; led_suit = the suit of that card.
4. **tell** (all players): Announce: 'Seat {leader} leads {played_card}; the led suit is {led_suit}.'
5. **poll** (every seat except leader): Each chosen card is removed from that player's hand and set as their played_card. No answer is seen until all three are in.
6. **tell** (all players): Reveal all four played_card values together.
7. **update** (all players): trick_winner = the seat whose played_card is of led_suit with the highest rank (A=6, K=5, Q=4, J=3, 9=2, 8=1); trick_points = the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1, 9=0, 8=0, but JH=5); the trick_winner's total += trick_points and their tricks_this_hand += 1.
8. **update** (all players): If (round - 1) % 6 == 0: sweeper = trick_winner. Otherwise, if trick_winner != sweeper: sweeper = 0.
9. **update** (all players): leader = trick_winner.
10. **tell** (all players): Announce: 'Seat {trick_winner} wins the trick and takes {trick_points} points. Totals: seat 1 {total}, seat 2 {total}, seat 3 {total}, seat 4 {total}.'
11. **update** (all players): When round % 6 == 0 and sweeper != 0: the player whose seat equals sweeper subtracts 44 from total, and every other player adds 15 to total. Announce the reversis if it happened.
12. **check** (all players): If round == 24, end the game; otherwise continue with the next round.

## Ending

- ends when: round == 24
- ranked by: `0 - you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is minus their total, so the lowest total ranks highest. The player with the lowest total wins. If two or more players tie for the lowest total, they share the result, which is the source's draw.

## Choices the source did not make

- 4 players: min 4, max 4, suggested 4: The designer fixed 4. The 24-card deck deals exactly 6 cards to each of 4 players, and the 44-point and 15-point values assume this size. Fewer seats would leave cards undealt and change the avoidance tension; more would not fit the deck.
- The sweeper's 'none' is encoded as 0: Seats are 1 to 4, so 0 marks no sweeper unambiguously as a number.
- Card ranks are encoded as numbers (A=6, K=5, Q=4, J=3, 9=2, 8=1): This lets the trick winner be found by arithmetic comparison within the led suit.
- Card names are written as rank followed by suit letter (for example JH is the Quinola): Hands, the deck and played cards need a compact text form.
- No talk step: The source says there is no table talk.
- The leader is asked with ask; the followers answer with poll: The source plays the lead face up first, then has the other three choose at the same moment.
- Ranking expression 0 - total: The engine picks the highest value, and the source's winner is the lowest total. A tie at the top is shared, which matches the source's draw.
- Strategy at the table: A thoughtful player sheds high-point cards (especially the Quinola) when void in the led suit, ducks under the current high card, tracks which cards have left the hand, and judges when to try a reversis or deliberately break an opponent's sweep.

## Simplifications

- The reveal of the three simultaneous cards is a tell after the poll: The engine reveals the polled answers together once all are in, which matches 'all cards are revealed together'.
- The trick winner's tricks_this_hand counter is added: It is a scratch counter that makes 'took all 6 tricks' checkable. The sweeper alone already decides the reversis.

## Unsupported (needs engine work)

- none
