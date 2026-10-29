# Witch's Brew: Claims

Over 3 sets of N rounds, players secretly hold 3 of 6 roles. Each round a leader names a role, holders choose at once to contest or yield, and the last contester clockwise takes the strong reward.

Players: 3 to 5, best with 4

## Parameters

- `num_sets` = 3
- `roles_per_hand` = 3
- `role_count` = 6
- `witch_strong` = 5
- `witch_weak` = 2
- `raven_keeper_strong` = 6
- `raven_keeper_weak` = 0
- `alchemist_strong` = 4
- `alchemist_weak` = 1
- `druid_strong` = 3
- `druid_weak` = 2
- `herb_hag_strong` = 2
- `herb_hag_weak` = 1
- `thief_steal` = 3
- `thief_weak` = 1
- `starting_score` = 0
- `overtaken_reward` = 0

## Round

1. **update** (all players): When round_in_set == 1: empty every player's hand (roles left unused from the previous set are lost) and empty led_list.
2. **poll** (all players): When round_in_set == 1: set each player's hand to the 3 roles in the chosen combination. Hands stay private (ally).
3. **update** (all players): Set leader_seat = ((set_number - 1) + (round_in_set - 1)) mod N + 1 and set every player's response to 'none'. Announce: 'Seat {leader_seat} leads this round.'
4. **ask** (seat leader_seat): Set named_role to the chosen role and append it to led_list. Set leader_holds = (named_role is in the leader's hand). Announce the named role.
5. **poll** (all players): Broadcast to all: 'Seat {seat} says: {value}'. Nothing binds.
6. **poll** (each player other than leader_seat whose hand contains named_role): Set response to 'contest' or 'yield'. Players who do not hold the role keep 'none' (an automatic pass).
7. **tell** (all players): Reveal every seat's response, which shows who held named_role.
8. **update** (all players): If any player's response == 'contest', set final_claimant to the contester with the largest (seat - leader_seat) mod N. Otherwise set final_claimant = leader_seat.
9. **update** (all players): Strong reward. If final_claimant != leader_seat or leader_holds is true, then: if named_role is not Thief, final_claimant's score += that role's strong value (Witch 5, Raven Keeper 6, Alchemist 4, Druid 3, Herb Hag 2). If named_role is Thief, set thief_target to the seat other than final_claimant with the highest score (ties go to the smallest (seat - final_claimant) mod N), then final_claimant's score += 3 and thief_target's score -= 3. If final_claimant == leader_seat and leader_holds is false, nobody gets the strong reward. The overtaken leader and overtaken contesters get 0.
10. **update** (all players): Weak reward: every player with response == 'yield' gets score += the weak value of named_role (Witch 2, Raven Keeper 0, Alchemist 1, Druid 2, Herb Hag 1, Thief 1).
11. **update** (all players): Remove named_role from the hand of leader_seat (if held) and from the hand of every player whose response != 'none'.
12. **update** (all players): round_count += 1 and round_in_set += 1. If round_in_set > N, set round_in_set = 1 and set_number += 1. Announce all scores.
13. **check** (all players): End the game if round_count >= 3 * N; otherwise continue.

## Ending

- ends when: round_count >= 3 * N
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's total score. The highest total wins, and players tied for the highest share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4 and the source range is 3 to 5. Three is the minimum so that claim order and contest bluffing matter; more than 5 would exceed the 6 roles, which could run out within a set.
- Hand choice offered as one pick from the 20 three-role combinations: This guarantees exactly 3 different roles in a single simultaneous answer.
- Talk kept as a simultaneous poll, broadcast to all: The rules specify simultaneous messages. Players disagree about who should claim, so bluffing about holdings is meaningful.
- Leader formula ((set_number-1)+(round_in_set-1)) mod N + 1: This matches 'set k starts with player k' and clockwise passing; with 3 players set 3 starts with player 3.
- Thief tie-break uses the first tied seat clockwise from the final claimant: The final claimant is the one using the Thief's reward.

## Simplifications

- A tie for the top score is a shared win rather than a declared draw: The engine has no separate draw; tied top players share the win.
- Roles left in a hand at the end of a set are discarded by emptying hands at the start of the next set: This has the same effect as losing them at the end of the set.

## Unsupported (needs engine work)

- none
