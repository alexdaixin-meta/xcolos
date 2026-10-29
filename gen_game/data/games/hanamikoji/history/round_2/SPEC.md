# Hanamikoji: Paired Hands

Two players win the favour of five Geisha over up to four hands, played as two pairs, by keeping, discarding, gifting and splitting Item cards with four one-use actions; Victory Markers move after each pair.

Players: 2 to 2, best with 2

## Parameters

- `geisha_count_total` = 5
- `charm_g1` = 3
- `charm_g2` = 3
- `charm_g3` = 4
- `charm_g4` = 5
- `charm_g5` = 6
- `charm_total` = 21
- `cards_g1` = 3
- `cards_g2` = 3
- `cards_g3` = 4
- `cards_g4` = 5
- `cards_g5` = 6
- `cards_total` = 21
- `cards_removed_per_hand` = 1
- `hand_size_dealt` = 6
- `deck_size_after_deal` = 8
- `max_hands` = 4
- `rounds_per_hand` = 8
- `max_rounds` = 32
- `hands_per_pair` = 2
- `secret_cards` = 1
- `tradeoff_cards` = 2
- `gift_cards` = 3
- `competition_cards` = 4
- `charm_to_win` = 11
- `geisha_to_win` = 3
- `default_pick` = 1

## Round

1. **update** (all players): When round_in_hand == 1 (start of a hand): build deck as the 21 Items [1,1,1,2,2,2,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5]; move one random card from deck to removed_card (replacing its previous content); move 6 random deck cards into each player's hand (hand emptied first); deck now holds 8; discard emptied; each player's unused_actions = [Secret, Trade-off, Gift, Competition]; each secret emptied; if hand_number is 1 or 3, each kept = []; starting_seat = 1 if hand_number is 1 or 3, else 2.
2. **update** (all players): active_seat = starting_seat if round_in_hand is odd, else the other seat.
3. **tell** (all players): Announce hand_number, round_in_hand, active_seat, each player's unused_actions, each player's pair totals (count of 1..5 in kept), and marker_1..marker_5.
4. **update** (the active seat): Move one random card from deck to the active player's hand (the draw).
5. **sync** (all players): Each player privately sees their own sorted hand and secret.
6. **ask** (the active seat): chosen_action = the answer; if illegal or missing, chosen_action = the first of Secret, Trade-off, Gift, Competition still in unused_actions.
7. **ask** (the active seat): If legal, chosen_cards = the written numbers in order; otherwise chosen_cards = the required number of lowest cards in hand in ascending order. Remove chosen_cards from the active player's hand. (judged: "The answer is exactly the required number of card numbers for chosen_action (Secret 1, Trade-off 2, Gift 3, Competition 4), and no number appears more often than that card appears in the active player's hand.")
8. **update** (the active seat): If chosen_action is Secret, append chosen_cards to the active player's secret; if Trade-off, append chosen_cards to discard. Remove chosen_action from the active player's unused_actions.
9. **ask** (the opponent (the seat that is not active_seat)): When chosen_action is Gift or Competition: the opponent is shown the revealed chosen_cards (Gift as offers 1,2,3; Competition as pair A, pair B); pick = the answer, or 1 if illegal or missing.
10. **update** (both players): When chosen_action is Gift: append offer number pick to the opponent's kept and the other two offers to the active player's kept. When chosen_action is Competition: append the picked pair to the opponent's kept and the other pair to the active player's kept.
11. **tell** (all players): Publicly announce the active seat and chosen_action; for Gift or Competition also the revealed chosen_cards and who kept which; for Secret or Trade-off only that the action was used.
12. **update** (all players): When round_in_hand == 8 (end of hand): reveal each player's secret, append it to that player's kept, and announce both secrets and both players' pair totals.
13. **update** (all players): When round_in_hand == 8 and hand_number is 2 or 4 (end of pair): for each Geisha g, if count of g in Player 1's kept > count in Player 2's kept then marker_g = 1, if lower then marker_g = 2, if equal marker_g unchanged; for each player charm = sum of Charm (3,3,4,5,6) of Geisha with marker on their side, geisha_count = number of markers on their side, standing = (charm>=11)*1000 + (geisha_count>=3)*100 + charm*10 + geisha_count; game_over = true if any player has charm >= 11 or geisha_count >= 3, or if hand_number == 4. Announce all markers, charm and geisha counts.
14. **check** (all players): End the game if game_over is true; otherwise continue.
15. **update** (all players): If round_in_hand == 8 then hand_number += 1 and round_in_hand = 1; otherwise round_in_hand += 1.

## Ending

- ends when: game_over == true, set after a pair (round_in_hand == 8 and hand_number in {2,4}) when any player has charm >= 11 or geisha_count >= 3, or when hand_number == 4
- ranked by: `you.standing` (the highest wins; players level at the top share the win)
- decided by: A player with 11 or more Charm wins. Otherwise a player with 3 or more Geisha wins. If neither holds after hand 4, the higher Charm wins, then the higher Geisha count. Equal standing is a shared result, which is the draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed the game at 2, and Gift and Competition are built as a split between the active player and one opponent.
- No talk step: The rules have no talk. In a two-player zero-sum game talk adds nothing to reason about.
- A standing attribute used as rank_by: It encodes the ordered win checks (Charm >= 11, then Geisha >= 3, then Charm, then Geisha) as one number. Equal standing gives the draw.
- Pair totals kept as a list `kept`: The total for Geisha g is the count of g in the list. This keeps the five per-Geisha counts in one attribute.
- Ask, not poll, for each choice: Each choice is made by one player in sequence, and the opponent picks after seeing the revealed cards.

## Simplifications

- 'Top card' draws and removals are random picks from the deck list: The engine draws at random from a list, which is equivalent to drawing from a shuffled deck.
- Hand-start, end-of-hand and end-of-pair steps run inside the round list, gated by when-conditions on round_in_hand and hand_number: The step list is flat, and single conditional steps express these phases without choosing between blocks.
- Legality of the written cards is ruled by a judged sentence: Parsing free text and checking it as a sub-multiset of the hand is beyond plain arithmetic. The default and all scoring stay arithmetic.

## Unsupported (needs engine work)

- none
