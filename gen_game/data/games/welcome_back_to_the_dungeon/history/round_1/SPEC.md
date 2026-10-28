# Back to the Dungeon: Single Delve

Players take turns drawing monsters and either secretly add them to a shared dungeon or sacrifice equipment. The last player who has not passed must run the dungeon. The first to 2 successful runs wins; 2 failures eliminate a player.

Players: 3 to 4, best with 3

## Parameters

- `base_hp` = 3
- `armor_hp` = 5
- `shield_hp` = 3
- `torch_max_strength` = 3
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
- `deck_size` = 13
- `item_count` = 5
- `successes_to_win` = 2
- `failures_to_eliminate` = 2
- `max_rounds` = 40
- `initial_successes` = 0
- `initial_failures` = 0

## Round

1. **tell** (all players): Announce active_seat, dungeon_count, items, deck_count, which seats have passed = true, and every seat's successes and failures.
2. **poll** (all players with eliminated = false): Every message is broadcast to all players: 'Seat {seat} says: {value}'. Talk is not binding.
3. **ask** (seat active_seat): If PASS: set the active player's passed = true.
4. **update** (seat active_seat, when they chose DRAW): Pick one card at random from deck, put it in the active player's drawn_card (privately shown to them), remove it from deck, and set deck_count -= 1. Set drawn_strength to its strength: Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9.
5. **ask** (seat active_seat, when they chose DRAW): Records the decision.
6. **update** (seat active_seat, when they chose DRAW): If ADD: append drawn_card to dungeon and to the active player's added_cards; dungeon_count += 1; dungeon_total += drawn_strength; if drawn_strength <= 3 then dungeon_low += drawn_strength; if drawn_card is Vampire or Lich then dungeon_undead += drawn_strength; if drawn_card is Dragon then dungeon_dragon += 9. If SACRIFICE X: remove X from items and discard the card unseen. In both cases set drawn_card to empty.
7. **update** (table): Set active_seat to the next seat clockwise after active_seat whose eliminated = false and passed = false.
8. **update** (table): round += 1.
9. **update** (table, when exactly one player has eliminated = false and passed = false): runner_seat = that player's seat. last_hp = 3 + (5 if Armor is in items) + (3 if Shield is in items). last_damage = dungeon_total - (dungeon_low if Torch is in items) - (dungeon_undead if Holy Water is in items) - (dungeon_dragon if Dragon Spear is in items).
10. **tell** (all players, when a run happened this round): Reveal every card in dungeon, together with last_damage and last_hp, for runner_seat.
11. **update** (seat runner_seat, when a run happened this round): If last_damage < last_hp then the runner's successes += 1, otherwise the runner's failures += 1. If the runner's failures >= 2, set the runner's eliminated = true.
12. **check** (table): End the game if any player has successes >= 2, or if exactly one player has eliminated = false.
13. **update** (table, when a run happened this round): New dungeon: refill deck with all 13 monsters; deck_count = 13; dungeon = []; dungeon_count = 0; dungeon_total = dungeon_low = dungeon_undead = dungeon_dragon = 0; items = all five; every player's passed = false and added_cards = []; active_seat = the first seat clockwise after runner_seat with eliminated = false.
14. **check** (table): End the game if round >= 40.

## Ending

- ends when: any player has successes >= 2, OR the count of players with eliminated = false is 1, OR round >= 40
- ranked by: `(1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures)` (the highest wins; players level at the top share the win)
- decided by: Non-eliminated players rank above eliminated ones. Among them, more successes ranks higher, then fewer failures. A player with 2 successes, or the sole survivor, therefore wins. Players level at the top share the win, which stands for the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer's suggested size is 3. Three is the smallest table where the bluff about what was secretly added and the pressure of who ends up running both work. Four is the maximum because the 13-card deck gets thin and turns grow long.
- Talk is kept as a simultaneous poll with a broadcast: The source says messages are written at the same time without seeing the others. Players disagree, since nobody wants to be the runner, so claims about added cards are worth reasoning about.
- The dungeon is tracked with hidden counters (total, low, undead, dragon) alongside the card list: These let damage be computed by plain arithmetic, while the card list is what gets revealed.
- The rank expression gives non-eliminated players +1000: This keeps eliminated players from winning the round-40 tiebreak.

## Simplifications

- Drawing the top card of a shuffled deck is a random pick from the deck list: The engine shuffles by drawing at random, and the two are equivalent.
- A draw after round 40 is a shared win among the tied leaders: The engine has no separate draw outcome.
- The run and the new-dungeon steps are single steps with a 'when' condition: The step list is flat, and these are conditional updates rather than alternative blocks.

## Unsupported (needs engine work)

- none
