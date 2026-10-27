# Blind Scuttle

Two players race to build a point pile that reaches a threshold lowered by Kings. Point cards go in face down with only their band visible, and the opponent can scuttle, steal or flip them.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 48
- `point_ranks_min` = 1
- `point_ranks_max` = 10
- `copies_per_rank` = 4
- `point_cards` = 40
- `jacks` = 4
- `kings` = 4
- `hand_deal` = 6
- `draw_pile_start` = 36
- `hand_limit_for_draw` = 8
- `max_turns` = 40
- `turns_each` = 20
- `low_band_max` = 4
- `mid_band_min` = 5
- `mid_band_max` = 7
- `high_band_min` = 8
- `first_threshold_0k` = 32
- `first_threshold_1k` = 24
- `first_threshold_2k` = 18
- `first_threshold_3k` = 14
- `first_threshold_4k` = 11
- `second_threshold_0k` = 30
- `second_threshold_1k` = 22
- `second_threshold_2k` = 16
- `second_threshold_3k` = 12
- `second_threshold_4k` = 9
- `king_scuttle_rank` = 10
- `shortfall_min` = 0

## Round

1. **update** (acting seat): If the acting player's points >= threshold, set their won = 1.
2. **check** (all players): End the game if any player's won == 1.
3. **tell** (all players): Announce the public state: each player's point_pile_view, king_count and threshold; scrap; len(draw_pile); each hand_count; turn; acting_seat.
4. **sync** (acting seat): The acting player sees their own hand and point_pile, which includes the exact ranks of their face-down cards.
5. **ask** (acting seat): Set action. An illegal or unparseable reply sets action = pass.
6. **ask** (acting seat): When action is points or scuttle, set chosen_card. If the reply is not a point card in hand, set action = pass.
7. **ask** (acting seat): When action is scuttle or jack, set target_index. An invalid reply sets action = pass.
8. **update** (acting seat): When action == draw: move a random card from draw_pile to the acting player's hand, and add 1 to hand_count.
9. **update** (acting seat): When action == points: remove chosen_card from hand, append 'D<rank>' to point_pile, append its band (Low for 1-4, Mid for 5-7, High for 8-10) to point_pile_view, add rank to points, and subtract 1 from hand_count.
10. **update** (acting seat): When action == scuttle: remove chosen_card from hand, subtract 1 from hand_count, and reveal chosen_card and the target's rank. If chosen rank >= target rank, remove the target entry from the opponent's point_pile and point_pile_view, subtract its rank from the opponent's points, and append both ranks to scrap. Otherwise append chosen_card to scrap and turn the target face up: its point_pile entry becomes 'U<rank>' and its view entry becomes its rank.
11. **update** (acting seat): When action == king_scuttle: remove one '10' from hand, subtract 1 from hand_count, append '10' and 'K' to scrap, subtract 1 from the opponent's king_count, and recompute the opponent's threshold.
12. **update** (acting seat): When action == jack: remove 'J' from hand, subtract 1 from hand_count, and append 'J' to scrap. Remove the target entry from the opponent's point_pile and point_pile_view and subtract its rank from the opponent's points. Append 'U<rank>' to the acting point_pile, append the rank to the acting point_pile_view, and add the rank to the acting points.
13. **update** (acting seat): When action == king: remove 'K' from hand, subtract 1 from hand_count, add 1 to king_count, and recompute threshold.
14. **update** (all players): Recompute each player's threshold from the table: First is [32,24,18,14,11][king_count] and second is [30,22,16,12,9][king_count]. Set shortfall = max(threshold - points, 0). Add 1 to turn and switch acting_seat to the other seat.
15. **check** (all players): End the game if turn > 40.

## Ending

- ends when: any player's won == 1, or turn > 40
- ranked by: `you.won * 1000 - you.shortfall` (the highest wins; players level at the top share the win)
- decided by: A player who reaches their threshold at the start of their own turn wins at once. Otherwise, after turn 40, the player with the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls share the result as a draw.

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed the game at two, and the asymmetric thresholds for First and second only make sense head to head.
- Card codes '1'..'10', 'J', 'K' and point-pile entries 'D<rank>' / 'U<rank>': Lists of text codes are needed to track face-down versus face-up cards and their ranks.
- A separate public point_pile_view beside the private point_pile: The opponent may see bands and face-up ranks but not face-down ranks, while the owner sees the exact ranks.
- One turn per round, with acting_seat alternating: Players take single alternating turns and the turn count is capped at 40.
- rank_by = won*1000 - shortfall: An immediate win outranks everything. Otherwise the smaller shortfall ranks higher, and equal values share the win, which models the draw.
- No talk step: The source has no communication. Players reason only from bands, the scrap pile and King counts.
- The King-scuttle and Jack card choices are not asked: The card used is fixed (a 10 or a J), and a King-scuttle target is just one of the opponent's Kings, which are interchangeable.

## Simplifications

- The top card of the draw pile is a random card from draw_pile: The engine draws at random from a list, which is equivalent to a shuffled pile.
- Placed Kings are tracked only by king_count, not as a list of cards: Kings have no identity beyond their count. When one is scuttled, a 'K' is appended to scrap.
- Only legal actions are offered, and any invalid reply becomes PASS: This follows the rule that an illegal choice counts as PASS and keeps the offers clean.

## Unsupported (needs engine work)

- none
