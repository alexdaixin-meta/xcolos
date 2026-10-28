# Dungeon Dare

Three players push their luck through a shuffled monster deck. Each turn they add the monster they drew to a hidden dungeon, strip the adventurer of an item, or pass out; the last player left must survive the run.

Players: 3 to 3, best with 3

## Parameters

- `seats` = 3
- `deck_size` = 13
- `goblin_strength` = 1
- `goblin_count` = 2
- `skeleton_strength` = 2
- `skeleton_count` = 2
- `orc_strength` = 3
- `orc_count` = 2
- `vampire_strength` = 4
- `vampire_count` = 2
- `golem_strength` = 5
- `golem_count` = 2
- `lich_strength` = 6
- `lich_count` = 1
- `demon_strength` = 7
- `demon_count` = 1
- `dragon_strength` = 9
- `dragon_count` = 1
- `base_hp` = 3
- `armor_hp` = 4
- `shield_hp` = 3
- `torch_max_strength` = 3
- `spear_min_strength` = 7
- `item_count` = 4
- `forced_pass_deck_max` = 2
- `run_extra_cards` = 2
- `success_points` = 2
- `fail_penalty` = 1
- `added_bonus` = 1
- `points_floor` = 0
- `win_points` = 4
- `max_turns` = 40
- `starting_points` = 0

## Round

1. **update** (all players): Applies only when new_dungeon is true. Set dungeon_number += 1 and leader_seat = ((dungeon_number - 1) mod 3) + 1. Set deck = the 13 strengths [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order; this seeded shuffle is the only random event. Set armor, shield, torch and spear = true. Set dungeon_pile = [] and dungeon_count = 0. For every player set set_aside = [], drawn_card = [], in_dungeon = true and added = false. Set in_count = 3, runner_seat = 0, active_seat = leader_seat and new_dungeon = false.
2. **update** (all players): Set turn += 1. Set forced_pass = (length(deck) <= 2). If forced_pass is false, move the first element of deck into the active player's drawn_card; that player privately sees it.
3. **sync** (the active player): The active player is shown their drawn_card, unless forced_pass is true.
4. **poll** (all players): Applies only when forced_pass is false. Every player, IN or OUT, writes one message at the same time. All are then broadcast as {"to": "all", "text": "Seat {seat} says: {value}"}. Messages bind no one.
5. **ask** (the active player (seat active_seat)): Sets last_action to the chosen option.
6. **update** (the active player): If last_action = PASS: set in_dungeon = false, in_count -= 1, and put drawn_card (if any) back as the first element of deck. If ADD: append drawn_card to dungeon_pile, set dungeon_count += 1 and added = true. If SACRIFICE_X: set item X = false and append drawn_card to the player's set_aside. In every case clear drawn_card.
7. **tell** (all players): Announce: 'Seat {active_seat} chose {last_action}. Dungeon pile: {dungeon_count} cards. Items left: armor {armor}, shield {shield}, torch {torch}, spear {spear}.' The drawn monster is not revealed.
8. **update** (all players): Applies only when in_count = 1 (the run). Set runner_seat = the seat with in_dungeon = true. Set run_hp = 3 + 4*armor + 3*shield. Set faced = dungeon_pile + the first 2 elements of deck. Set run_damage = the sum over faced of strength s, except that s is counted as 0 if (torch and s <= 3) or (spear and s >= 7). If run_damage < run_hp, the runner gets points += 2. Otherwise the runner gets points = max(0, points - 1), and every player with in_dungeon = false and added = true gets points += 1. Set new_dungeon = true.
9. **tell** (all players): Applies only when a run happened this turn. Announce: 'Seat {runner_seat} ran: monsters {faced}, HP {run_hp}, damage {run_damage}.' Then announce success or failure and the new points.
10. **update** (all players): Applies only when new_dungeon is false. Set active_seat = the next seat after active_seat in the order 1, 2, 3, 1, ... that has in_dungeon = true.
11. **check** (all players): End the game if (a run happened this turn and some player has points >= 4) or turn >= 40. Otherwise run the next turn.

## Ending

- ends when: (new_dungeon = true and max over players of points >= 4) or turn >= 40
- ranked by: `you.points` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their point total; the most points wins. Players tied for the most share the result, which the source calls a draw.

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3. Leadership rotation and the push-your-luck tension are built around three seats. With more seats each player's added bet matters less and turns run long; with two, the first pass ends the dungeon at once.
- Talk kept as a simultaneous poll each drawing turn: The rules require a simultaneous message from every player. Players disagree, since each wants the others to pass or to run a deadly dungeon, so bluffing about the drawn card carries real strategic weight.
- Deck as an ordered list shuffled once per dungeon; draws take the first element: This honors 'top card', the card returned on top after a PASS, and 'top 2 cards' in the run, with the shuffle as the only random event.
- Monsters stored by strength only: Names carry no rule effect; strength alone decides damage, TORCH and SPEAR.
- Talk is skipped on a forced pass: The rules send a forced pass straight from step (a) to step (d), skipping the talk in (c).

## Simplifications

- A tie for most points is reported as a shared win rather than a draw: The engine ranks by one expression and players level at the top share the win; this is equivalent to the source's draw.
- Dungeon reset, run and turn advance are single steps gated by arithmetic conditions: The step list is flat, so each block is expressed as conditional updates within one round.

## Unsupported (needs engine work)

- none
