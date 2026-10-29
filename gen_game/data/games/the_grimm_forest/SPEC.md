# Three Pigs: Secret Materials

Each player has a secret Favoured Material. Players gather straw, wood and brick from shared piles at the same time, can send the Wolf to stop a location paying out, and build houses section by section. The first to finish 3 houses wins.

Players: 3 to 4, best with 3

## Parameters

- `max_rounds` = 15
- `refill_per_location` = 3
- `bonus_extra` = 2
- `bonus_chance_each_location` = 0.3333
- `section_cost` = 2
- `favoured_section_cost` = 1
- `sections_per_house` = 3
- `max_unfinished_per_material` = 1
- `max_completed_per_material` = 2
- `houses_to_finish` = 3
- `market_gain` = 1
- `build_actions_per_round` = 2
- `initial_pile` = 0
- `initial_stock` = 0
- `favour_cards_each_material_3p` = 1
- `favour_cards_each_material_4p` = 2
- `finisher_rank_offset` = 100000
- `completed_weight` = 100

## Round

1. **update** (all players): round += 1; bonus_location = one entry of locations drawn at random (each 1/3).
2. **tell** (all players): Announce 'Round {round}: the bonus location is {bonus_location}.'
3. **update** (all players): fields_pile += 3; forest_pile += 3; brickyard_pile += 3; then the pile of bonus_location gains 2 more. Announce the three piles.
4. **poll** (all players): Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind no one.
5. **poll** (all players): Each player's gather_choice = their answer. Nobody sees any choice until all are in.
6. **tell** (all players): Reveal every player's gather_choice to all.
7. **update** (all players): Count fields_gatherers (gather_choice = Fields), forest_gatherers, brickyard_gatherers, fields_wolves (gather_choice = Wolf-Fields), forest_wolves and brickyard_wolves. Set every player's last_gain = 'nothing'.
8. **update** (all players): Fields: if fields_wolves = 0 and fields_gatherers > 0, then share = floor(fields_pile / fields_gatherers); each player with gather_choice = Fields gets straw += share and last_gain = share Straw; fields_pile -= share * fields_gatherers. Otherwise fields_pile is unchanged.
9. **update** (all players): Forest: if forest_wolves = 0 and forest_gatherers > 0, then share = floor(forest_pile / forest_gatherers); each Forest chooser gets wood += share and last_gain = share Wood; forest_pile -= share * forest_gatherers. Otherwise forest_pile is unchanged.
10. **update** (all players): Brickyard: if brickyard_wolves = 0 and brickyard_gatherers > 0, then share = floor(brickyard_pile / brickyard_gatherers); each Brickyard chooser gets brick += share and last_gain = share Brick; brickyard_pile -= share * brickyard_gatherers. Otherwise brickyard_pile is unchanged.
11. **update** (all players): Market: each player with gather_choice = Market gains 1 of their favoured material (straw, wood or brick) and last_gain = 1 of that material. Players who chose a Wolf gain nothing.
12. **tell** (all players): Announce the piles after resolution and the number of gatherers and wolves at each location.
13. **sync** (all players): Each player privately receives their own last_gain and stockpile (straw, wood, brick).
14. **poll** (all players): build_choice = answer (build action 1).
15. **update** (all players): For each player with build_choice = Build M: cost = 1 if favoured = M, else 2. If stock of M < cost, or (M_done = 2 and M_progress = 0), it counts as Pass. Otherwise stock of M -= cost; M_progress += 1; sections += 1; if M_progress = 3, then M_progress = 0, M_done += 1 and completed += 1.
16. **tell** (all players): Show every player's public build state: straw/wood/brick progress and done, completed and sections. The cost paid is not shown.
17. **poll** (all players): build_choice = answer (build action 2).
18. **update** (all players): Apply build action 2 exactly as build action 1.
19. **tell** (all players): Show every player's public build state again.
20. **update** (all players): For each player, finished = 1 if completed >= 3, otherwise 0.
21. **check** (all players): End the game if any player has finished = 1, or if round >= 15. Otherwise start the next round.

## Ending

- ends when: count of players with finished = 1 >= 1, or round >= 15
- ranked by: `you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections)` (the highest wins; players level at the top share the win)
- decided by: If anyone has completed 3 houses, the finishers rank above everyone else and are ordered by total leftover straw + wood + brick. Otherwise players are ranked by completed houses, then by total sections built. The highest value wins, and players level at the top share the win (a draw).

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer suggests 3 and the deal is defined for 3 and 4. At 3, the favoured materials are a perfect split, so guessing the others' materials is clean deduction, and contesting a pile or sending the Wolf has a clear target. A fifth player has no deal defined, and splitting the piles that many ways would leave almost no gains.
- Talk kept as one simultaneous poll per round, broadcast to all: The source requires it. Players disagree: each wants a pile to themselves and wants to hide their favoured material. Bluffing about where you will go, or threatening a Wolf, gives everyone something to reason about. The talk is simultaneous because the source says messages are written at the same time.
- Build offers include only legal builds, plus Pass: A seat is never offered what it may not do. The 'counts as Pass' rule stays as a backstop. The filter uses only the seat's own private stockpile, so it leaks nothing.
- Ranking expression: finisher offset 100000, completed weight 100: A non-finisher's value is at most 2*100 + 12 sections, well below 100000, so finishers always rank above everyone. The weight of 100 makes completed houses outrank sections, since sections never reach 100.
- Sections tie-break counts every section ever built, including those in completed houses: The source says 'most built sections' without restricting it.
- Gather and wolf counts are announced after resolution: The source says the piles and the number of gatherers are public, so anyone can work out each gain.

## Simplifications

- Each house is tracked as a progress counter (0-2) plus a completed count per material, not as a list of named sections: Floor, Walls and Roof are always built in order, so a counter holds the same information.
- The 'one unfinished house per material' rule is enforced by the build always adding to the existing unfinished house: The engine has no separate choice to start a second unfinished house, so the limit holds automatically.

## Unsupported (needs engine work)

- none
