# Loot: Sealed Raids

Each round one seat sails a hidden-value merchant ship and every seat secretly commits crew from a fixed budget of 30 to defend it or raid it, with one-shot Captain and Admiral trumps. The most gold after 3 x N rounds wins.

Players: 3 to 5, best with 4

## Parameters

- `min_players` = 3
- `max_players` = 5
- `suggested_players` = 4
- `starting_crew` = 30
- `starting_gold` = 0
- `ship_value_small` = 3
- `ship_value_medium` = 5
- `ship_value_large` = 7
- `ships_per_player` = 3
- `captains_per_player` = 1
- `admirals_per_player` = 1
- `captain_bonus` = 6
- `rounds_per_player` = 3
- `min_commit` = 0
- `unspent_crew_value` = 0

## Round

1. **update** (all players): round += 1; owner = ((round - 1) mod N) + 1; for every player, set committed = 0, trump_declared = false and strength = 0.
2. **tell** (all players): Announce: 'Round {round}: Seat {owner} is the owner. Unsailed ships: {owner.ships}.'
3. **update** (seat owner): When the length of owner.ships = 1, set current_ship = the only value in owner.ships (it sails automatically).
4. **ask** (seat owner): When the length of owner.ships > 1, set current_ship = the chosen value. The choice is private.
5. **poll** (all players): Every message is shown to everyone after all are in: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
6. **poll** (all players): committed = the amount, or 0 if the amount is invalid. trump_declared = true only for a valid declaration; an invalid declaration is ignored.
7. **update** (all players): crew -= committed. strength = committed + (6 if the seat is not the owner and trump_declared, else 0). defense = owner.strength.
8. **update** (all players): top_attack = the highest strength among non-owners; top_count = the number of non-owners whose strength = top_attack. If owner.trump_declared, last_taker = owner. Otherwise, if top_attack > defense and top_count = 1, last_taker = the non-owner whose strength = top_attack. Otherwise last_taker = owner.
9. **update** (all players): The player in seat last_taker adds current_ship to gold. last_ship_value = current_ship.
10. **update** (all players): Remove current_ship from owner.ships. If owner.trump_declared, set owner.admiral_used = true. For each non-owner with trump_declared, set captain_used = true.
11. **tell** (all players): Announce: 'The ship was worth {last_ship_value}. Seat {last_taker} got it.' Then list who used a Captain or Admiral this round. No crew amounts are revealed.
12. **check** (all players): End the game if round >= 3 * N; otherwise continue.

## Ending

- ends when: round >= 3 * N
- ranked by: `you.gold` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their gold. The player with the most gold wins. Players tied for the most gold share the result, which stands for the source's draw.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggests 4, and the minimum of 3 keeps it from being a plain duel. Two or more raiders are needed for ties between attackers and for a raider to free-ride while others overbid. Beyond 5 players each seat is owner rarely and the ties between attackers dominate.
- Keep the simultaneous talk poll: The source requires it. Players have opposing interests over who raids which ship, so a non-binding message can bluff, threaten or deter, and following someone else's proposal can cost a player.
- The unsailed-ships list is public and a value is removed only at bookkeeping: The source announces the owner's unsailed ships each round. Removing the value at sail time would leak the hidden value before the announcement.
- Strategy at the table: A thoughtful player rations 30 crew over 3 x N rounds. They infer which ship sailed from the remaining list, time the one-shot Admiral and Captain, and use talk to bluff or provoke ties between rival raiders.

## Simplifications

- A tie for the most gold is a shared win instead of a draw: The engine ranks by an arithmetic expression and players level at the top share the win. This is the closest equivalent to 'the game is a draw'.
- The commit poll offers only valid amounts and valid trumps: The engine constrains answers to the offered range, so the source's 'invalid amounts are set to 0' and 'invalid trumps are ignored' rarely trigger. Both are kept as rules anyway.

## Unsupported (needs engine work)

- none
