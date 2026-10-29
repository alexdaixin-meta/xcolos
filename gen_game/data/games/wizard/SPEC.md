# Wizard Duel of Three

A three-player trick-taking game of 6 hands of 5 tricks. Players bid how many tricks they will take and score for exact bids, using Wizards, Jesters and a turned trump suit.

Players: 3 to 3, best with 3

## Parameters

- `num_hands` = 6
- `tricks_per_hand` = 5
- `total_rounds` = 30
- `deck_size` = 32
- `num_suits` = 4
- `max_rank` = 7
- `numbered_cards` = 28
- `num_wizards` = 2
- `num_jesters` = 2
- `hand_size` = 5
- `unused_cards_per_hand` = 16
- `bid_min` = 0
- `bid_max` = 5
- `exact_bid_bonus` = 20
- `exact_bid_per_trick` = 10
- `miss_penalty_per_trick` = 10
- `first_dealer_seat` = 1
- `trick_win_increment` = 1

## Round

1. **update** (table): When trick_in_hand == 1: deck is set to all 32 cards (R1-R7, B1-B7, G1-G7, Y1-Y7, W1, W2, J1, J2). Every hand is emptied and every played_history entry is cleared.
2. **update** (all players): When trick_in_hand == 1: each player draws 5 cards at random from deck into their hand, each card removed from deck as it is drawn.
3. **update** (table): When trick_in_hand == 1: one more card is drawn at random from deck into trump_card. trump_suit is set to its suit letter if it is numbered, or to none if it is W or J. The 16 cards left in deck stay hidden and unused this hand.
4. **tell** (all players): When trick_in_hand == 1: announce 'Hand {hand_number}: dealer is seat {dealer}; turned card is {trump_card}; trump is {trump_suit}.'
5. **update** (all players): When trick_in_hand == 1: every bid and every tricks_taken is set to 0.
6. **sync** (all players): When trick_in_hand == 1: each player is sent their own hand, trump_card and the scores.
7. **poll** (all players): When trick_in_hand == 1: each player's bid is set to their answer. Nobody sees any bid until all are in.
8. **tell** (all players): When trick_in_hand == 1: one message per player: 'Seat {seat} bids {bid}.'
9. **update** (table): led_suit is set to none, trick_cards is emptied and every played_card is set to empty.
10. **ask** (seat leader): The card is removed from the leader's hand and appended to trick_cards and played_history. The leader's played_card is set to it. If the card is numbered, led_suit is set to its suit.
11. **ask** (seat leader % 3 + 1): The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit.
12. **ask** (seat (leader + 1) % 3 + 1): The card is removed from the player's hand and appended to trick_cards and played_history. The player's played_card is set to it. If led_suit == none and trick_cards[0] is not a Wizard and the card is numbered, led_suit is set to its suit.
13. **update** (table): The trick winner is worked out by arithmetic. Each card in trick_cards gets a power by its play position p (0, 1, 2). A Wizard has power 1000 - p. A card of trump_suit has power 200 + rank. A card of led_suit that is not trump has power 100 + rank. Any other numbered card has power 0. A Jester has power 3 - p only if all three cards are Jesters, otherwise 0. The seat that played the card with the highest power wins. That seat's tricks_taken increases by 1, and leader is set to that seat.
14. **tell** (all players): Announce 'Seat {leader} wins trick {trick_in_hand} with cards {trick_cards}; tricks taken now {tricks_taken}.'
15. **update** (all players): When trick_in_hand == 5: for each player, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |bid - tricks_taken|.
16. **tell** (all players): When trick_in_hand == 5: separate messages per player: 'Seat {seat} took {tricks_taken} tricks' and 'Seat {seat} score is now {score}'.
17. **update** (table): round_number += 1. If trick_in_hand == 5: hand_number += 1, trick_in_hand is set to 1, dealer is set to dealer % 3 + 1, and leader is set to dealer % 3 + 1 using the new dealer. Otherwise trick_in_hand += 1.
18. **check** (table): End the game if round_number > 30. Otherwise continue with the next round.

## Ending

- ends when: round_number > 30
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's final score after 6 hands (30 tricks). The highest score wins, and players tied for the highest score share the win (a draw).

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed the game at three. The deck arithmetic (15 dealt, 1 turned, 16 unused) and the seat rotation depend on exactly three seats, and a fourth would change the card counts.
- No talk step: The rules state there is no discussion phase.
- Cards coded as short text (R5, W1, J2) and the trick winner computed as a power value per card: This turns the trick-winning rules into pure arithmetic: the first Wizard beats everything, then the highest trump, then the highest led-suit card, and an all-Jester trick goes to the first Jester.
- Strategy at this table: A thoughtful player bids from hand strength and the trump suit, then plays to hit the bid exactly. They dump high cards or Jesters when they have enough tricks, and track played cards and others' bids to judge which cards are still out.

## Simplifications

- Start-of-hand and end-of-hand steps are ordinary round steps, each carrying a when-condition on trick_in_hand: The step list is flat. Each step is individually conditional on a counter rather than being a separately chosen block, so the game stays faithful.
- The order of play is addressed by seat expressions relative to leader: The engine asks named seats; leader, leader % 3 + 1 and (leader + 1) % 3 + 1 reproduce seat order starting from the trick winner.

## Unsupported (needs engine work)

- none
