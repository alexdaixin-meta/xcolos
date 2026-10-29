# Hanamikoji: Five Geisha

Two players each take four one-shot actions per hand to place Item cards for five Geisha, aiming for 11 Charm or 3 Geisha at the end of each pair of hands.

Players: 2 to 2, best with 2

## Parameters

- `geisha_count_total` = 5
- `charm_geisha_1` = 3
- `charm_geisha_2` = 3
- `charm_geisha_3` = 4
- `charm_geisha_4` = 5
- `charm_geisha_5` = 6
- `items_total` = 21
- `items_geisha_1` = 3
- `items_geisha_2` = 3
- `items_geisha_3` = 4
- `items_geisha_4` = 5
- `items_geisha_5` = 6
- `removed_per_hand` = 1
- `deal_per_player` = 6
- `deck_after_deal` = 8
- `hands` = 4
- `rounds_per_hand` = 8
- `rounds_total` = 32
- `turns_per_player_per_hand` = 4
- `secret_cards` = 1
- `tradeoff_cards` = 2
- `gift_cards` = 3
- `gift_cards_to_opponent` = 1
- `competition_cards` = 4
- `competition_pair_size` = 2
- `win_charm` = 11
- `win_geisha` = 3

## Round

1. **update** (all players): When round_in_hand == 1: build deck as the 21 Items (three 1s, three 2s, four 3s, five 4s, six 5s). Draw 1 at random into removed_card. Draw 6 at random into each player's hand; the remaining 8 stay in deck. Set each secret, pending and discard to empty. Set each unused_actions to [Secret, Trade-off, Gift, Competition]. If hand_number is 1 or 3, set each kept to empty; in hands 2 and 4, kept carries over. Markers carry over.
2. **update** (all players): active_seat = starting_seat if round_in_hand is odd, otherwise the other seat (3 - starting_seat).
3. **update** (seat active_seat): Draw 1 card at random from deck (the top of a shuffled deck), append it to the active player's hand and remove it from deck.
4. **sync** (all players): Each player sees their own hand and secret, and both players' kept, unused_actions, markers and counters.
5. **ask** (seat active_seat): last_action = the choice; remove it from the active player's unused_actions.
6. **ask** (seat active_seat): Move that card from hand to pending (pick 1).
7. **ask** (seat active_seat): When last_action is Trade-off, Gift or Competition: move that card from hand to pending (pick 2).
8. **ask** (seat active_seat): When last_action is Gift or Competition: move that card from hand to pending (pick 3).
9. **ask** (seat active_seat): When last_action is Competition: move that card from hand to pending (pick 4). Picks 1-2 form Pair A and picks 3-4 form Pair B.
10. **update** (seat active_seat): When last_action is Secret: move the 1 pending card to the active player's secret, face-down.
11. **update** (seat active_seat): When last_action is Trade-off: move the 2 pending cards to discard, face-down.
12. **tell** (all players): When last_action is Gift: announce the 3 pending cards. When last_action is Competition: announce Pair A (picks 1-2) and Pair B (picks 3-4).
13. **ask** (the seat that is not active_seat): When last_action is Gift: append the chosen card to the opponent's kept, append the other 2 pending cards to the active player's kept, and empty pending.
14. **ask** (the seat that is not active_seat): When last_action is Competition: append the chosen pair to the opponent's kept, append the other pair to the active player's kept, and empty pending.
15. **update** (all players): When round_in_hand == 8: reveal each player's secret card, append it to their kept, and empty secret.
16. **update** (all players): When round_in_hand == 8 and hand_number is 2 or 4: (a) for each g in 1-5, count the cards of number g in each player's kept; if Player 1's count is strictly higher, marker_g = 1; if Player 2's is strictly higher, marker_g = 2; on a tie marker_g is unchanged. (b) Each player's charm = sum of the Charm (3,3,4,5,6) of g whose marker_g equals their seat; geisha_count = number of markers equal to their seat; standing = charm. (c) game_over = 1 if either charm >= 11, or either geisha_count >= 3, or hand_number == 4.
17. **tell** (all players): When round_in_hand == 8 and hand_number is 2 or 4: announce marker_1 to marker_5 and each player's charm and geisha_count.
18. **check** (all players): End the game if game_over == 1; otherwise continue.
19. **update** (all players): If round_in_hand < 8: round_in_hand += 1. Otherwise: round_in_hand = 1, hand_number += 1, starting_seat = 3 - starting_seat.

## Ending

- ends when: game_over == 1
- ranked by: `(you.charm >= 11) * 10000 + (you.geisha_count >= 3) * 1000 + you.charm * 10 + you.geisha_count` (the highest wins; players level at the top share the win)
- decided by: A player with 11 or more Charm wins first. Otherwise a player with 3 or more Geisha wins. If nobody has won after hand 4, the higher Charm wins, then the higher Geisha count. Players level on all of these share the result, which is a draw.

## Choices the source did not make

- 2 players, min = max = suggested: The designer fixed 2. The Gift and Competition splits are a duel between the active player and one opponent, and the 21-card budget fits exactly two players.
- Strategy at the table: A thoughtful player hides key Geisha with Secret, offers Gift and Competition splits where every option leaves them ahead, and tracks the visible kept lists to guess what the opponent is holding.
- No talk step: The source has no negotiation, so none is added.
- unused_actions is public: The source does not state its visibility; the physical game shows used action tokens face-down, so both players know which actions remain.
- last_action is public: Which action was taken is visible in the physical game, even when the cards are not.
- Marker encoded as 0/1/2: Middle / Player 1 side / Player 2 side, so the marker can be used in arithmetic.
- rank_by weights 10000 / 1000 / 10 / 1: These weights encode the win order: 11 Charm, then 3 Geisha, then Charm, then Geisha count. Charm totals at most 21, so the weights never overlap. Both players cannot reach the same goal, so ties only occur in the final fallback, where a tie is a draw.

## Simplifications

- Cards for an action are named one pick at a time from the hand list: Choosing from the hand list guarantees the player names only cards they hold, with no free-text parsing.
- Competition pairs are set by pick order: picks 1-2 are Pair A, picks 3-4 are Pair B: This lets the split be made with sequential single-card choices.
- Drawing 'the top card' is a random draw from deck: The deck is shuffled, so the two are equivalent.
- Player-versus-player card counts for markers are compared in one update: The engine has no player-attribute operand, so the comparison is computed at the table level.

## Unsupported (needs engine work)

- none
