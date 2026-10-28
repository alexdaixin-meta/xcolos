# Growl: Charmed Nights

A hidden-wolf game: wolves bite humans at night to turn them into wolves, humans charm and accuse to find the wolves, and the winning team is decided by counting living roles.

Players: 5 to 7, best with 6

## Parameters

- `min_players` = 5
- `max_players` = 7
- `wolves_at_5_or_6` = 1
- `wolves_at_7` = 2
- `human_start_charms_at_5_or_6` = 2
- `human_start_charms_at_7` = 3
- `rounds_per_player` = 2
- `card_weight_wound` = 30
- `card_weight_charm` = 30
- `card_weight_salve` = 25
- `card_weight_bite` = 15
- `card_pool_wound` = 6
- `card_pool_charm` = 6
- `card_pool_salve` = 5
- `card_pool_bite` = 3
- `accusation_wounds` = 1
- `death_threshold` = 2
- `infection_threshold` = 3
- `end_alive_at_most` = 2
- `charm_cost` = 1

## Round

1. **update** (all players): round += 1; active_seat = the first living seat after active_seat in seat order, wrapping from N to 1 (round 1 gives seat 1, since active_seat starts at 0). Announce the round and the active seat.
2. **update** (all players): card = one entry picked at random from card_pool, which is not removed (30% Wound, 30% Charm, 25% Salve, 15% Bite). Announce card to everyone.
3. **poll** (all living players): No state changes. Once all messages are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
4. **ask** (the active player (seat active_seat)): recipient_seat = the chosen seat. If card is Wound, the recipient's wounds += 1. If Salve, salves += 1. If Charm, charms += 1. If Bite and the recipient is human, bites += 1; if Bite and the recipient is a wolf, nothing changes and only that wolf is told privately that the Bite was discarded. Announce the recipient to everyone.
5. **poll** (all living players): Each living player's votes_received = the number of votes naming them. If some player has 2 x votes_received > living_count, that player's wounds += 1. Announce every vote count.
6. **update** (all players): Each living player with wounds - salves >= 2: alive = false, revealed_role = role. Announce each death and the revealed role. Recompute living_count, living_wolves and living_humans. Reset votes_received to 0.
7. **check** (all players): If living_wolves == 0: wolves_won = 0, game_over = 1, each human's won = 1, and the game ends with a human win. Otherwise continue.
8. **poll** (all living players): Store each player's answer in their night_choice. No messages are allowed at Night.
9. **update** (all players): 1. A Bite is valid only if the chooser's role is wolf; a human's Bite counts as None. 2. A Charm is valid only if the chooser has charms >= 1, and that chooser loses 1 charm; a Charm with no charms counts as None. 3. charms_tonight = the number of valid Charms aimed at the player. 4. Each wolf with charms_tonight >= 1 has calmed = true, and that wolf's Bite tonight is cancelled. 5. For each human, bites_tonight = the number of valid, uncancelled Bites aimed at them; Bites aimed at wolves have no effect. 6. Each human's bites = max(0, bites + bites_tonight - charms_tonight), so Bites land first and Charms then cure them, never below 0. 7. bites_landed_tonight = the sum of bites_tonight over humans; wolves_calmed_tonight = the number of wolves with calmed = true.
10. **tell** (each living player privately): Tell each player their bites_tonight (0 for a wolf) and charms_tonight, without naming any sender. Tell each calmed wolf that it was calmed.
11. **tell** (all players): Announce: 'Tonight {bites_landed_tonight} Bites landed on humans and {wolves_calmed_tonight} wolves were calmed.'
12. **update** (all players): Each living human with bites >= 3: role = 'wolf', is_wolf = 1, bites = 0, charms unchanged. They are told privately. Recompute living_wolves and living_humans. Reset night_choice, bites_tonight, charms_tonight and calmed.
13. **check** (all players): If living_humans == 0: wolves_won = 1 and the game ends. Otherwise, if living_count <= 2 or round == total_rounds: wolves_won = 1 if living_wolves >= living_humans, else 0, and the game ends. When the game ends, set game_over = 1 and won = 1 for every player whose is_wolf equals wolves_won. Otherwise continue to the next round.

## Ending

- ends when: game_over == 1, which is set when living_wolves == 0 after a Day death check, or after a Night when living_humans == 0, living_count <= 2 or round == total_rounds
- ranked by: `1 - abs(you.is_wolf - game.wolves_won)` (the highest wins; players level at the top share the win)
- min_to_win: `1` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: A team win. Every player whose current role is on the winning team (wolves if wolves_won is 1, humans otherwise) scores 1 and shares the win, including dead players and humans converted to wolves. Everyone else scores 0.

## Choices the source did not make

- 5 to 7 players, suggested 6: The designer gives 5 to 7 and suggests 6. Below 5 a single wolf has too few humans to hide among. Above 7 the accusation majority and the night charms get too diffuse for one player's choice to matter.
- Keep the simultaneous Day talk as a poll with broadcast: The rules require it. Humans want to find the wolf while wolves want to misdirect, so the talk is real disagreement worth reasoning about.
- Card odds as a 20-entry pool drawn with replacement: 6/6/5/3 out of 20 gives exactly 30/30/25/15 percent, and the rules state odds, not a depleting deck.
- Every seat is offered the same Night options, including Bite and Charm: The rules define a human's Bite and a chargeless Charm as None. Offering identical lists keeps the private offer itself from revealing a role or a charm count.
- Night action as one choice combining action and target: This fits the engine's single choice-from-a-list answer.
- A Bite card given to a human is never infection-checked during the Day: The source checks infection only at the Night Infection step.
- Team win encoded as is_wolf compared with wolves_won, with min_to_win 1: The engine ranks by one expression. This gives 1 to every member of the winning team and 0 to the rest.
- Ties and simultaneous end conditions are checked in this order: no living humans, then two or fewer alive or the final round: The outcome is the same either way: if no humans remain, wolves outnumber them.

## Simplifications

- Roles revealed on death are copied into a public revealed_role attribute: Visibility is fixed per attribute, so a public copy is how one player's secret becomes public.
- is_wolf kept as a number beside role: The ranking expression needs arithmetic on the role.

## Unsupported (needs engine work)

- none
