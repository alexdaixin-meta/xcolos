# Three-Card Wizard

A three-player trick-taking game of 12 hands with 3 tricks each: players bid exactly how many tricks they will take, then play Wizards, Jesters and suited cards to hit that number.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 28
- `suits` = 3
- `ranks_per_suit` = 8
- `wizards` = 2
- `jesters` = 2
- `hands` = 12
- `tricks_per_hand` = 3
- `rounds` = 36
- `cards_dealt_per_player` = 3
- `trump_card_position` = 10
- `cards_left_in_deck_after_deal` = 18
- `bid_min` = 0
- `bid_max` = 3
- `default_bid` = 1
- `wizard_strength` = 100
- `trump_strength_bonus` = 20
- `jester_or_offsuit_strength` = 0
- `initial_best_value` = -1
- `exact_bid_bonus` = 20
- `points_per_trick_when_exact` = 10
- `penalty_per_trick_off` = 10
- `starting_score` = 0
- `starting_hand_number` = 0
- `starting_trick_in_hand` = 1

## Round

1. **update** (all players): When trick_in_hand = 1: add 1 to hand_number; refill deck with all 28 cards and shuffle it; empty every hand and set every tricks_taken to 0; draw 3 cards at random from deck into seat 1's hand, then 3 into seat 2's, then 3 into seat 3's (each removed from deck); remove the next random card from deck and set it as trump_card (18 cards stay in deck); set trump_suit to the suit letter of trump_card if it is suited, otherwise 'none'; set leader = ((hand_number - 1) mod 3) + 1.
2. **sync** (all players): When trick_in_hand = 1: each player sees their own hand; trump_card, trump_suit, hand_number and leader are announced to all.
3. **poll** (all players): When trick_in_hand = 1: each player's bid is set to their answer exactly (a 0 stays 0); a missing or invalid answer sets that bid to 1. All bids are then announced.
4. **update** (all players): Every round: led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0, played_cards = [].
5. **update** (seat leader): Build the leader's offer from their hand, in hand order: if led_suit != 'none' and they hold a card of led_suit, the offer is those cards plus any W or J cards they hold; otherwise it is the whole hand.
6. **ask** (seat leader): The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
7. **update** (seat leader): Resolve the card. If it is suited and led_suit = 'none' and wizard_played = false, set led_suit to its suit. If it is a Wizard, set wizard_played = true. Strength is 100 for a Wizard, 20 + rank for a suit equal to trump_suit, rank for a suit equal to led_suit, and 0 otherwise. If strength > best_value, set best_value = strength and best_seat = this seat. The played card is announced.
8. **update** (seat (leader mod 3) + 1): Build this player's offer with the same rule as above.
9. **ask** (seat (leader mod 3) + 1): The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
10. **update** (seat (leader mod 3) + 1): Resolve the card with the same led-suit and strength rule as above, then announce it.
11. **update** (seat ((leader + 1) mod 3) + 1): Build this player's offer with the same rule as above.
12. **ask** (seat ((leader + 1) mod 3) + 1): The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0].
13. **update** (seat ((leader + 1) mod 3) + 1): Resolve the card with the same led-suit and strength rule as above, then announce it.
14. **update** (all players): Add 1 to tricks_taken of best_seat; announce best_seat as the trick winner; set leader = best_seat.
15. **update** (all players): When trick_in_hand = 3: for each player, if tricks_taken = bid, add 20 + 10 * tricks_taken to score; otherwise subtract 10 * |tricks_taken - bid|. Announce all scores, set every bid to 0 and set trick_in_hand = 1. Otherwise (trick_in_hand < 3) add 1 to trick_in_hand.
16. **check** (all players): End the game if hand_number >= 12 and trick_in_hand = 1 (hand 12 has just been scored); otherwise continue to the next round.

## Ending

- ends when: game.hand_number >= 12 and game.trick_in_hand = 1
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score after hand 12. The highest score wins, and players tied at the top share the win (the source calls this a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed 3 seats. The deal (9 cards plus the 10th as trump), the leader rotation mod 3 and the play order all assume three players. The game is about predicting tricks and managing the trick count against two rivals whose bids are public.
- Strategy at the table: A thoughtful player bids from card strength and the trump suit, then plays to hit the bid exactly: dumping Jesters or low cards to avoid tricks, spending Wizards or trumps to take them, and reading the opponents' public bids to disrupt them. A thoughtless player bids blindly and plays cards in any order.
- No talk step: The source has no table talk, and adding it would add a mechanic.
- Shuffle and deal written as random draws from the deck list: The engine shuffles by drawing at random; drawing 9 cards and then one more for trump matches 'top 3 to each seat, the 10th is trump'.
- The bid and tricks_taken are public attributes: The rules announce bids after the simultaneous poll and announce each trick winner, so both are open information. The poll keeps bids secret until all are in.

## Simplifications

- The source's 'draw' when two or three players tie for the top score becomes a shared win: The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome.
- Each of the three plays is written as three steps (build offer, ask, resolve) addressed to the computed seat: The engine runs a flat list of steps; play order is expressed by naming the seat from leader.
- Hand-start steps carry a 'when trick_in_hand = 1' condition, and scoring carries 'when trick_in_hand = 3': Single steps may be conditional, so no block substitution is needed.

## Unsupported (needs engine work)

- none
