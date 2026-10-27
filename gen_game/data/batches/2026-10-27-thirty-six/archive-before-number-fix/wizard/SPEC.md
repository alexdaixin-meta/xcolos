# Pocket Wizard

A three-player Wizard-style trick-taking game: 9 hands of 3 tricks each, where every seat bids how many tricks it will take and scores for hitting its bid exactly.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 28
- `suits` = 3
- `ranks_per_suit` = 8
- `wizards` = 2
- `jesters` = 2
- `total_rounds` = 27
- `tricks_per_hand` = 3
- `hands` = 9
- `cards_dealt_per_seat` = 3
- `trump_cards_turned` = 1
- `deck_left_after_deal` = 18
- `bid_min` = 0
- `bid_max` = 3
- `default_bid` = 1
- `best_value_start` = -1
- `wizard_strength` = 100
- `jester_strength` = 0
- `second_wizard_strength` = 0
- `trump_bonus` = 20
- `exact_bid_bonus` = 20
- `points_per_trick_on_exact_bid` = 10
- `penalty_per_trick_off` = 10
- `first_leader` = 1

## Round

1. **update** (all players): When trick_in_hand == 1: hand_number += 1. The deck is reset to the full 28 cards. Every tricks_taken = 0. Dealing goes seat 1, then seat 2, then seat 3: each seat draws 3 cards at random from the deck, one at a time, and each card is appended to its hand in the order drawn and removed from the deck. leader = ((hand_number - 1) mod 3) + 1.
2. **update** (all players): When trick_in_hand == 1: one card is drawn at random from the deck into trump_card and removed from the deck, leaving 18 cards. trump_suit = the first letter of trump_card if that letter is R, B or G, otherwise 'none'. Announce trump_card and trump_suit to everyone.
3. **sync** (all players): When trick_in_hand == 1: each seat is shown its own hand, trump_card and trump_suit.
4. **poll** (all players): When trick_in_hand == 1: each answer is stored in that seat's bid_answer.
5. **update** (all players): When trick_in_hand == 1: bid = bid_answer if it is exactly 0, 1, 2 or 3; otherwise bid = 1. Announce all three bids.
6. **update** (all players): Start of trick: led_suit = 'none', best_value = -1, best_seat = leader.
7. **update** (seat leader): Build the leader's offer. If led_suit is not 'none' and the hand holds at least one card of led_suit, offer = the cards of led_suit plus every W and J card, in hand order. Otherwise offer = the whole hand, in hand order.
8. **ask** (seat leader): If the answer is missing or not in the offer, the first card of the offer is used. The card is removed from the hand, and the remaining cards keep their order. played_card = that card, cur_card = that card, cur_seat = this seat. The card is shown to all players.
9. **update** (all players): If led_suit == 'none' and best_value < 100 and cur_card is an R, B or G card, then led_suit = the suit of cur_card. Then set cur_strength: 100 if cur_card is a W and best_value < 100; 0 if cur_card is a W and best_value >= 100; 0 if cur_card is a J; 20 + rank if the suit of cur_card == trump_suit; rank if the suit of cur_card == led_suit; otherwise 0. If cur_strength > best_value, then best_value = cur_strength and best_seat = cur_seat.
10. **update** (seat (leader mod 3) + 1): Build that seat's offer by the same rule as for the leader.
11. **ask** (seat (leader mod 3) + 1): Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all.
12. **update** (all players): Apply the led-suit and strength rules to cur_card, exactly as after the leader's play.
13. **update** (seat ((leader + 1) mod 3) + 1): Build that seat's offer by the same rule as for the leader.
14. **ask** (seat ((leader + 1) mod 3) + 1): Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all.
15. **update** (all players): Apply the led-suit and strength rules to cur_card, exactly as after the leader's play.
16. **update** (all players): Trick award: the tricks_taken of seat best_seat += 1; leader = best_seat. Announce the trick winner.
17. **update** (all players): When trick_in_hand == 3: for each seat, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |tricks_taken - bid|. Announce all scores.
18. **update** (all players): trick_in_hand += 1; if trick_in_hand == 4, then trick_in_hand = 1.
19. **check** (all players): End the game if hand_number == 9 and trick_in_hand == 1 (27 rounds have been played); otherwise continue.

## Ending

- ends when: hand_number == 9 and trick_in_hand == 1
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 27 rounds (9 hands), each seat's standing is its score. The highest score wins, and seats tied for the highest score share the result (the source calls this a draw).

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3. The deck size, the 3-card deal, the 18 cards left after the deal and the 3-trick hands all assume exactly 3 seats. More seats would not fit the 28-card deck at this deal size, and fewer would leave no rivals to bid against.
- No talk step before bids or plays: The source has no table talk, and adding it would add a mechanic. The strategy is in the cards: estimating your hand's trick count from the trump, reading the other bids, and ducking or taking tricks to hit your bid or spoil an opponent's.
- Bids are gathered with a simultaneous poll: The source says all three seats answer at the same moment.
- The hand-start steps are separate steps, each with the condition trick_in_hand == 1: The step list is flat, so the condition is placed on each step instead of on a block.
- The game ends on hand_number == 9 and trick_in_hand == 1, checked after the advance: This is true exactly after round 27, without adding a round counter.
- 'A Wizard was already played this trick' is tested as best_value >= 100: Only a Wizard can reach strength 100, so the two are equivalent and no extra state is needed.

## Simplifications

- Shuffling and taking the top cards is done as random draws from the deck list: The engine's draw picks a random card, which gives the same distribution as shuffling and dealing from the top.
- A tie for the highest score is a shared win rather than a declared draw: The engine has no separate draw: players level at the top share the win, which is equivalent.
- Each trick is written as three fixed offer/ask/strength step groups, with seats picked from leader by arithmetic: The engine has no per-player sub-loop, so each play position gets its own steps.

## Unsupported (needs engine work)

- none
