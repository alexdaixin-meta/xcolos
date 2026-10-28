# Loaded Button Men

Two players secretly load four dice (d4, d6, d8, d12) to total 16, then take turns capturing each other's dice with power or skill attacks over two 20-turn legs; the higher total of captured sizes wins.

Players: 2 to 2, best with 2

## Parameters

- `d4_size` = 4
- `d6_size` = 6
- `d8_size` = 8
- `d12_size` = 12
- `dice_per_player` = 4
- `load_total` = 16
- `default_d4` = 2
- `default_d6` = 3
- `default_d8` = 4
- `default_d12` = 7
- `legs` = 2
- `turns_per_leg` = 20
- `leg1_first_turn` = 1
- `leg1_last_turn` = 20
- `leg2_first_turn` = 21
- `leg2_last_turn` = 40
- `consecutive_passes_to_end_leg` = 2
- `skill_attack_dice` = 2
- `power_attack_dice` = 1
- `starting_score` = 0
- `min_die_value` = 1

## Round

1. **update** (all players): turn += 1; leg = 1 if turn <= 20, otherwise 2. If turn == 21, set leg_over = false. active_seat = first_seat when (turn is odd and leg == 1) or (turn is even and leg == 2); otherwise active_seat = the other seat.
2. **poll** (all players): Runs only when turn == 1 or turn == 21. Stores the answer in each player's load_d4. Nobody sees any answer.
3. **poll** (all players): Runs only when turn == 1 or turn == 21. Stores the answer in load_d6.
4. **poll** (all players): Runs only when turn == 1 or turn == 21. Stores the answer in load_d8.
5. **poll** (all players): Runs only when turn == 1 or turn == 21. Stores the answer in load_d12.
6. **update** (all players): Runs only when turn == 1 or turn == 21. For each player: if load_d4 + load_d6 + load_d8 + load_d12 == 16, then d4_value = load_d4, d6_value = load_d6, d8_value = load_d8 and d12_value = load_d12; otherwise d4_value = 2, d6_value = 3, d8_value = 4 and d12_value = 7. For both players, in_play = [4, 6, 8, 12]. previous_was_pass = false. Announces only that loading is done.
7. **tell** (all players): Runs only when leg_over == false. Public status: turn, leg, active_seat, each player's in_play, both scores, and previous_was_pass.
8. **sync** (all players): Runs only when leg_over == false. Each player privately receives the values (d4_value, d6_value, d8_value, d12_value) of the dice in their own in_play.
9. **ask** (seat active_seat): Runs only when leg_over == false. Stores the choice in declaration. Sets this_is_pass, target_size, attacker_large_size (the power die, or the larger of the two skill dice) and attacker_small_size (the smaller skill die, or 0).
10. **update** (all players): Runs only when leg_over == false and this_is_pass == false. target_value = the defender's value for the die of size target_size. For a power attack, attack_value = the attacker's value for the die of size attacker_large_size, and attack_success = (attack_value >= target_value). For a skill attack, attack_value = the sum of the attacker's values for the dice of sizes attacker_large_size and attacker_small_size, and attack_success = (attack_value == target_value).
11. **update** (all players): Runs only when leg_over == false, this_is_pass == false and attack_success == true. Remove target_size from the defender's in_play; the attacker's score += target_size; announce publicly that the target (size target_size) was captured and its value target_value. The attacker's die of size attacker_large_size is rerolled to a uniform random value from 1 to attacker_large_size, and its new value is told only to its owner. The smaller skill attacker keeps its value.
12. **update** (all players): Runs only when leg_over == false, this_is_pass == false and attack_success == false. Remove attacker_large_size from the attacker's in_play; the defender's score += attacker_large_size; announce publicly the captured die's size and value. Nothing is rerolled, the smaller skill attacker keeps its value, and target_value is not revealed.
13. **tell** (all players): Runs only when leg_over == false. Public result: 'pass', or the target size, the attacking die sizes, and whether the attack succeeded.
14. **update** (all players): Runs only when leg_over == false. leg_over = true if either player's in_play is empty, or (this_is_pass and previous_was_pass), or turn == 20. Then previous_was_pass = this_is_pass. If leg == 1 and leg_over == true and turn < 20, set turn = 20 (the remaining leg-1 turns are skipped). If leg == 2 and (leg_over == true or turn == 40), set match_over = true.
15. **check** (all players): End the game if match_over == true; otherwise continue to the next round.

## Ending

- ends when: match_over == true (set when turn == 40 or when leg 2 ends early)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score: the total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks. The higher score wins; equal scores share the win (a draw).

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the table at 2. Every mechanic (attacker vs defender, alternating turns, loading against one opponent) is head-to-head and has no meaning with more seats.
- No pre-choice talk step: The source has no talk. In a two-player zero-sum duel, talk adds no shared decision to negotiate.
- Leg-1 early end jumps the turn counter to 20: The source says the skipped turns pass with no actions. Jumping turn to 20 is equivalent and avoids empty rounds.
- Die sizes listed as separate parameters d4_size, d6_size, d8_size, d12_size: Each parameter must be a single number.
- Strategy note: A thoughtful player loads to bait or defend, for example a high d12 for power and small dice that sum to likely targets. They infer hidden values from failed attacks and rerolls, and pass when attacking risks feeding the opponent a large die.

## Simplifications

- Loading is asked as four simultaneous number questions, one per die, then validated: The engine takes one number per question. The sum-to-16 check and the default replacement are done by arithmetic afterwards.
- Turn declarations are offered as a list of legal choices only: Choosing from a list makes illegal declarations impossible, so the 'invalid counts as pass' rule never triggers. The effect on play is identical.
- Attack resolution copies the attacker's and target's values into table scratch attributes (attack_value, target_value) before comparing: The engine has no direct operand for comparing attributes of two different players.
- The winner is computed as the highest you.score with ties shared: The engine has no separate draw. Equal top scores sharing the win is how a draw is represented.

## Unsupported (needs engine work)

- none
