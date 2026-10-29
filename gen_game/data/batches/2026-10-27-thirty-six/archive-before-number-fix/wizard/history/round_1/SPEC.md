# Wizard Triad

A three-player trick-taking game over 12 hands of 3 tricks each. Players secretly bid how many tricks they will take, then follow suit, with Wizards, Jesters and trump, and score for hitting the bid exactly.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 28
- `suits` = 3
- `rank_min` = 1
- `rank_max` = 8
- `wizards` = 2
- `jesters` = 2
- `hands` = 12
- `tricks_per_hand` = 3
- `total_rounds` = 36
- `cards_dealt_per_player` = 3
- `trump_card_position` = 10
- `bid_min` = 0
- `bid_max` = 3
- `default_bid` = 1
- `exact_base` = 30
- `exact_per_bid` = 5
- `miss_penalty_per_trick` = 10
- `wizard_strength` = 100
- `trump_strength_bonus` = 20
- `jester_strength` = 0
- `offsuit_strength` = -1
- `no_card_strength` = -1

## Round

1. **update** (all players): When trick_in_hand == 1: hand_number += 1. All 28 cards are returned to deck; every hand, played_card, bid and tricks_taken is reset to empty or 0; played_cards is cleared. Then 3 random draws are made from deck into each player's hand (remove from deck, append to hand). Then one random card is drawn from deck into trump_card. trump_suit = that card's suit letter if it is suited, else 'none'. leader = ((hand_number - 1) mod 3) + 1.
2. **sync** (all players): When trick_in_hand == 1: each player is sent their own hand, plus trump_card, trump_suit, hand_number and leader.
3. **poll** (all players): When trick_in_hand == 1: each player's bid is set to their answer. A missing or invalid answer sets bid = 1. Nobody sees any bid until all are in.
4. **tell** (all players): When trick_in_hand == 1: all bids are announced (Seat 1, Seat 2, Seat 3).
5. **update** (all players): Start of trick: led_suit = '', wizard_played = false, best_value = -1, best_seat = 0, and every played_card = ''.
6. **ask** (seat leader): The card (or the fallback card from rule R9 if the answer is missing or invalid) is removed from hand, set as played_card and appended to played_cards. If it is a Wizard: strength = 100, and if led_suit == '' then led_suit = 'none'; wizard_played = true. If it is a Jester: strength = 0. If it is suited with suit s and rank r: if led_suit == '' and wizard_played == false then led_suit = s; strength = 20 + r if s == trump_suit, else r if s == led_suit, else -1. If strength > best_value, then best_value = strength and best_seat = this seat. Announced to all.
7. **ask** (seat (leader mod 3) + 1): Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all.
8. **ask** (seat ((leader + 1) mod 3) + 1): Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all.
9. **update** (all players): tricks_taken of seat best_seat += 1; leader = best_seat. The trick winner is announced.
10. **update** (all players): When trick_in_hand == 3: for each player, if tricks_taken == bid then score += 30 + 5 * bid, else score -= 10 * |tricks_taken - bid|. hands_done += 1. Scores, bids and tricks_taken are announced. Then tricks_taken = 0 for everyone.
11. **update** (all players): trick_in_hand = (trick_in_hand mod 3) + 1.
12. **check** (all players): End the game if hands_done == 12; otherwise continue.

## Ending

- ends when: hands_done == 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after hand 12. The highest total wins; if two or three players tie for the highest total, they share the result (a draw).

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixed the table at 3, and the lead rotation, 3-card hands and deck size are built for exactly 3 seats.
- No talk step: The rules say explicitly that there is no talk phase. The strategy lies in judging hand strength for the bid and in playing to hit the bid exactly, including ducking tricks.
- Card codes such as 'R5', 'W1', 'J2': These give a text form for cards in list attributes, so suits and ranks can be compared arithmetically.
- Trick winner tracked by a running strength value (Wizard 100, trump 20 + rank, led suit = rank, Jester 0, off-suit -1), replaced only when strictly greater: This reproduces rule (9) by arithmetic. A strict comparison keeps the first Wizard and the first Jester winning ties.
- Only legal cards are offered: This enforces rule (7) directly. The fallback priority of rule (8) still applies to missing or invalid answers.

## Simplifications

- A tie for the highest score is a shared win rather than a labelled draw: The engine has no separate draw outcome: players level at the top share the win.
- The trump card is drawn at random from the remaining deck rather than taken as the literal 10th card: With a random shuffle the two are equivalent.

## Unsupported (needs engine work)

- none
