# Duel Durak (seeded)

Two-player Durak with a fixed 8-card hand each, no drawing, a trump picked by offer and choice, and up to 39 single-attack bouts. The first player to empty their hand wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 36
- `suit_count` = 4
- `ranks_per_suit` = 9
- `lowest_rank` = 6
- `highest_rank` = 14
- `hand_size_start` = 8
- `set_aside_size` = 20
- `deal_p1_first_position` = 1
- `deal_p1_last_position` = 8
- `deal_p2_first_position` = 9
- `deal_p2_last_position` = 16
- `set_aside_first_position` = 17
- `set_aside_last_position` = 36
- `offer_suit_count` = 2
- `default_offer_suit_a` = 2
- `default_offer_suit_b` = 3
- `default_first_attacker_seat` = 2
- `first_bout_round` = 2
- `last_round` = 40
- `max_bouts` = 39
- `max_throw_ins_per_bout` = 1

## Round

1. **update** (table): Reset for the bout: table_cards = [], attack_card = -1, throw_card = -1, defender_took = false.
2. **ask** (the attacker (seat = attacker)): attack_card = the chosen id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. If the answer is missing or illegal, play the card minimising (rank, suit), that is the lowest rank with ties broken by lower suit index.
3. **ask** (the defender (seat = 3 - attacker)): If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true. X beats Y when (suit(X) = suit(Y) and rank(X) > rank(Y)) or (suit(X) = trump and suit(Y) != trump).
4. **ask** (the attacker): If a card is chosen, throw_card = that id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. A missing or illegal answer counts as PASS. Only PASS is offered when defender_took = false and the defender's hand_size = 0.
5. **ask** (the defender, when throw_card != -1 and defender_took = false): If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true.
6. **update** (table): If defender_took: add every card in table_cards to the defender's hand (re-sorted ascending), add len(table_cards) to the defender's hand_size, and leave attacker unchanged. Otherwise: add table_cards to discard (re-sorted ascending) and set attacker = 3 - attacker. In both cases bout += 1.
7. **tell** (all players): Announce table_cards in play order, the result (taken or beaten off), and both hand_size values.
8. **check** (table): End the game if any seat has hand_size = 0, or if bout = 39 (round 40 done). Otherwise continue.

## Ending

- ends when: any player's hand_size = 0, or bout = 39
- ranked by: `0 - you.hand_size` (the highest wins; players level at the top share the win)
- decided by: Fewer cards in hand ranks higher. If exactly one player has 0 cards after a bout, that player wins. If both reach 0 together, they tie and share the result (a draw). After round 40 the player with fewer cards wins, and equal counts are a draw (shared).

## Choices the source did not make

- 2 players, suggested 2: The designer fixed the table at 2. This is a head-to-head duel of card management, where a thoughtful player saves trumps, chooses the trump offer to fit their own hand, and throws in to unload cards.
- No talk step: The source has no talk, and in a two-player zero-sum duel talk adds nothing to reason about.
- Draw expressed as a shared top rank: rank_by = -hand_size makes both seats level when both have 0 cards or equal counts, and the engine treats a level top as shared, which is the draw.
- The bout counter ends the game at 39 bouts: Rounds 2 to 40 are 39 bouts.

## Simplifications

- The source's round 1 is modelled as setup steps: It runs once before the bouts.
- Dynamic attacker and defender are named by the attacker attribute: The engine addresses seats, so the roles are read from a table number.

## Unsupported (needs engine work)

- none
