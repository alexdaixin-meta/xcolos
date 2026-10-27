# Duel Durak

Two-player Durak with no drawing: one bout per round, each with one attack and at most one throw-in; the first player to empty their hand wins, or after round 40 the player with fewer cards wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 36
- `suits` = 4
- `cards_per_suit` = 9
- `rank_offset` = 6
- `hand_size` = 8
- `set_aside_size` = 20
- `seat1_first_position` = 1
- `seat1_last_position` = 8
- `seat2_first_position` = 9
- `seat2_last_position` = 16
- `set_aside_first_position` = 17
- `set_aside_last_position` = 36
- `trump_unset` = -1
- `card_unset` = -1
- `max_throw_ins_per_bout` = 1
- `trump_round` = 1
- `first_bout_round` = 2
- `last_round` = 40
- `suit_pairs` = 6

## Round

1. **update** (all players): round_number += 1
2. **ask** (seat 2 (only when round_number = 1)): suit_pair = the chosen pair, announced
3. **ask** (seat 1 (only when round_number = 1)): trump = the chosen suit's number (0-3), announced to both
4. **update** (all players (only when round_number = 1)): attacker = the seat whose hand holds the lowest id c with floor(c/9) = trump. If neither seat holds a trump card, attacker = 2. Announced.
5. **update** (all players (only when round_number >= 2)): Step 1: table_cards = [], attack_card = -1, defence_card = -1, throw_card = -1, defender_took = false
6. **ask** (the attacker (only when round_number >= 2)): Step 2: remove the card from attacker.hand, append it to table_cards, set attack_card = card, and show it to both players
7. **ask** (the defender (only when round_number >= 2)): Steps 3-4: if a card is chosen, remove it from defender.hand, append it to table_cards, set defence_card = card, and show it. If TAKE, defender_took = true.
8. **ask** (the attacker (only when round_number >= 2)): Steps 5-6: if a card is chosen, remove it from attacker.hand, append it to table_cards, set throw_card = card, and show it
9. **ask** (the defender (only when round_number >= 2 and throw_card != -1 and defender_took = false)): Steps 7-8: if a card is chosen, remove it from defender.hand and append it to table_cards. If TAKE, defender_took = true.
10. **update** (all players (only when round_number >= 2)): Step 9: if defender_took, append all table_cards to defender.hand (sorted ascending), keep the attacker, and announce 'taken'. Otherwise append table_cards to discard, set attacker = the defender's seat, and announce 'beaten off'. Then table_cards = [].
11. **update** (all players (only when round_number >= 2)): Step 10: hand_size = length of hand for both seats, announced. bout += 1.
12. **check** (all players): Step 11: end if round_number >= 2 and any seat has hand_size = 0, or if round_number = 40. Otherwise continue.

## Ending

- ends when: (round_number >= 2 and (seat1.hand_size = 0 or seat2.hand_size = 0)) or round_number = 40
- ranked by: `0 - you.hand_size` (the highest wins; players level at the top share the win)
- decided by: Fewer cards in hand ranks higher. A seat at 0 cards while the other holds cards wins. Both at 0 is a shared result (draw). After round 40 the seat with fewer cards wins, and equal counts share (draw).

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed the table at 2. The rules (one attacker, one defender, seat-specific trump choice) only work for 2.
- No talk step: The source has none. With two opposed players, talk would only add words.
- attacker = 0 stands for 'none': The attribute is numeric, and seats are 1 and 2.
- A round_number counter gates the round-1 trump steps and the round 2-40 bout steps: The step list is flat. Single-step `when` conditions reproduce the source's distinct round 1 without choosing blocks.
- rank_by = 0 - hand_size: This gives every stated outcome: an empty hand beats a non-empty one, both empty ties (draw), and after round 40 fewer cards wins with equal counts tying.
- Strategy at the table: Seat 2 offers a suit pair that avoids its opponent's likely strength, seat 1 picks the trump that suits its hand, and attackers lead cards the defender is unlikely to beat or that set up a same-rank throw-in, while defenders weigh beating against saving trumps.

## Simplifications

- Hand sorting is described in the update, not computed by a dedicated operation: Order affects only how a hand is displayed, never an outcome.

## Unsupported (needs engine work)

- none
