# Escalation Ledger III

Three players with secret high-value schedules bid over 12 rounds for a prize; tied top bids go to a raise-or-drop escalation, and the highest total wins.

Players: 3 to 3, best with 3

## Parameters

- `num_rounds` = 12
- `high_value` = 12
- `low_value` = 6
- `bid_option_1` = 0
- `bid_option_2` = 2
- `bid_option_3` = 4
- `bid_option_4` = 6
- `bid_option_5` = 8
- `raise_cost` = 3
- `loser_pay_fraction` = 0.5
- `schedule_types` = 4
- `schedule_cycle` = 4
- `starting_total` = 0

## Round

1. **update** (all players): Add 1 to round. Set each player's prize_value = 12 if round % 4 == schedule_slot, else 6. Reset bid to 0, in_tie to false, escalation to empty and raise_count to 0. Announce 'Round {round} of 12.'
2. **poll** (all players): Every player writes one message at the same time. All messages are then broadcast to everyone as 'Seat {seat} says: {value}'. Nothing is binding, and players may lie.
3. **poll** (all players): Store each player's answer in bid. No bid is seen until all are in.
4. **update** (all players): Set high_bid = max of all bids and top_count = number of players with bid == high_bid. Announce every player's bid.
5. **update** (all players): When high_bid > 0 and top_count == 1: the player with bid == high_bid adds prize_value - bid to total, and every other player subtracts bid / 2 from total. When high_bid == 0: nothing changes.
6. **update** (all players): When high_bid > 0 and top_count >= 2: set in_tie = (bid == high_bid) for each player, and every player with in_tie false subtracts bid / 2 from total.
7. **poll** (each player with in_tie true (only when high_bid > 0 and top_count >= 2)): Store each tied player's answer in escalation. Choices are simultaneous and secret until all are in.
8. **update** (tied players): When high_bid > 0 and top_count >= 2: set raise_count = number of players with escalation == RAISE. Every raiser subtracts 3 from total. If raise_count == 1, the raiser adds prize_value - bid to total and every other tied player subtracts bid / 2. Otherwise every tied player subtracts bid / 2.
9. **tell** (all players): Announce every bid, every escalation choice and every total.
10. **check** (all players): If round >= 12, end the game; otherwise continue with the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total after round 12. The highest total wins, and players level at the top share the win (a draw).

## Choices the source did not make

- 3 players (min, max and suggested 3): The designer fixed the table at 3. Three seats are dealt from four types, so one type stays hidden, which the deduction depends on. A fourth seat would leave no unused type, and fewer seats would remove the multi-way ties.
- Talk kept, as a simultaneous poll broadcast to all: The rules require simultaneous talk. Players disagree over who should win each prize, and claims about one's own schedule can be bluffs, so the talk gives players something to reason about.
- Type stored as schedule_slot = round % 4 value (North 1, East 2, South 3, West 0): This makes the 12-or-6 prize value a single arithmetic test.
- In a no-winner escalation, the tied players pay half the bid as well as the 3 for raising: This follows the rules exactly: every tied player pays half, and raisers have also paid 3.

## Simplifications

- The escalation poll and its resolution are steps that always appear in the round, with a when-condition, instead of a separate block: The engine's step list is flat. A conditional step reproduces step 6 exactly.
- The winner's payment and prize are applied as one net change (prize_value - bid): The arithmetic result is identical.

## Unsupported (needs engine work)

- none
