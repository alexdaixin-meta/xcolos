# Button Men: Guard and Strike

Two players each hold a d4, d8 and d12 with hidden values. Over 30 exchanges they pick at the same moment to guard one of their dice or to attack an opponent's die, capturing it if the attacker's value is at least the target's. Legs reset the dice, and surviving dice score bonuses.

Players: 2 to 2, best with 2

## Parameters

- `dice_per_player` = 3
- `small_die_size` = 4
- `medium_die_size` = 8
- `large_die_size` = 12
- `starting_score` = 0
- `random_max` = 110075314175
- `digit_base` = 24
- `digit_count` = 8
- `total_exchanges` = 30
- `max_exchanges_per_leg` = 10
- `action_count` = 12
- `guard_defense_points` = 3
- `failed_attack_defense_points` = 2
- `survive_bonus_d4` = 2
- `survive_bonus_d8` = 4
- `survive_bonus_d12` = 6
- `a_d4_digit` = 0
- `a_d8_digit` = 1
- `a_d12_digit` = 2
- `b_d4_digit` = 3
- `b_d8_digit` = 4
- `b_d12_digit` = 5
- `a_reroll_digit` = 6
- `b_reroll_digit` = 7

## Round

1. **update** (all players): Draw R uniformly from 0 to 110075314175 and store its base-24 digits D0..D7 in digits, where Dk = floor(R/24^k) mod 24. If leg_start: set every die's alive flag to true; set A's d4_value=(D0 mod 4)+1, d8_value=(D1 mod 8)+1, d12_value=(D2 mod 12)+1; set B's d4_value=(D3 mod 4)+1, d8_value=(D4 mod 8)+1, d12_value=(D5 mod 12)+1; set leg_exchange=1 and leg_start=false. Clear each player's revealed_values and attack_result.
2. **tell** (all players): Announce exchange, leg_exchange, both scores, and both players' d4_alive, d8_alive and d12_alive.
3. **sync** (all players): Each player privately sees their own d4_value, d8_value and d12_value.
4. **poll** (all players): Set each player's action. Nobody sees the other's choice until both are in.
5. **update** (all players): Resolve both attacks at once, using the values held at the start of this exchange. For each attacker X against opponent Y, where the action is 4-12 with attacking die a and target die t: if the X die a or the Y die t is not alive at the start of the exchange, attack_result=no_effect. Otherwise, if Y's action is the guard of die t (guard of d4=1, d8=2, d12=3) and that die is alive, attack_result=fail_guarded, Y.score += 3, and X's a value is appended to X.revealed_values. Otherwise, if X.a_value >= Y.t_value, attack_result=success, X.score += size of t (4, 8 or 12), and Y.t_alive is set to false after both attacks are resolved. Otherwise attack_result=fail_low, Y.score += 2, X's a value is appended to X.revealed_values and Y's t value is appended to Y.revealed_values. A die may capture and be captured in the same exchange.
6. **update** (all players): Rerolls, at most one die per player. A player's die is rerolled if it was guarded this exchange and was alive at the start (action 1-3), or if it attacked with attack_result=success and is still alive after the captures. Player A's rerolled die is set to (D6 mod size)+1. Player B's rerolled die is set to (D7 mod size)+1. New values are visible only to their owner.
7. **tell** (all players): Announce both actions, each attack_result, each player's revealed_values, which dice were captured, and both scores. Rerolled values are not announced.
8. **update** (all players): If a player has d4_alive, d8_alive and d12_alive all false, or leg_exchange = 10, or exchange = 30, the leg ends: each player's score += 2*d4_alive + 4*d8_alive + 6*d12_alive, and leg_start is set to true. Otherwise leg_exchange += 1. Then exchange += 1.
9. **check** (all players): End the game if exchange > 30; otherwise continue to the next exchange.

## Ending

- ends when: exchange > 30
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After 30 exchanges and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals share the win, which is a draw.

## Choices the source did not make

- 2 players, as filed: The designer fixed the game at 2. It is a head-to-head duel in which every action targets the single opponent's dice, so there is no room for more seats.
- Seat 1 is player A and seat 2 is player B: The rules assign different random digits to A and B, so each seat needs a fixed role.
- No talk step: The rules give no communication, and the game is purely adversarial with simultaneous choices.
- All 12 actions are offered even when a named die is captured: The rules list exactly 12 actions and state that an action naming a captured die does nothing, so offering them stays faithful.
- Strategy at the table: A thoughtful player tracks announced values and which dice were rerolled, guards a high-value die that is likely to be attacked, and attacks dice whose values are revealed as low or that are small. A thoughtless player attacks blindly into guards.

## Simplifications

- R is stored as its eight base-24 digits: 24^8 = 110075314176, so a uniform R from 0 to 110075314175 is exactly eight independent uniform digits from 0 to 23. Every die value rule is unchanged.
- The match-end leg closure is folded into the leg-end step as the condition exchange = 30: This gives the same scoring without needing a separate block of steps.
- Announced die values are kept in a per-exchange public list, revealed_values: Every reveal needs a stated piece of state.

## Unsupported (needs engine work)

- none
