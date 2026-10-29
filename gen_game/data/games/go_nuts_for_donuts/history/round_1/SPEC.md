# Go Nuts for Donuts: Premium Picks

Four players secretly split 6 premium picks between Glazed and Jelly, then for 10 rounds talk and simultaneously pick one of five donuts; a donut scores only for a lone chooser.

Players: 4 to 4, best with 4

## Parameters

- `player_count` = 4
- `rounds` = 10
- `glazed_value` = 9
- `jelly_value` = 6
- `cruller_value` = 4
- `sprinkle_value` = 2
- `plain_value` = 1
- `premium_picks_total` = 6
- `split_min` = 0
- `split_max` = 6
- `lone_chooser_count` = 1
- `donut_collected_increment` = 1
- `pick_use_per_choice` = 1
- `tiebreak_multiplier` = 100

## Round

1. **update** (all players): round += 1
2. **tell** (all players): Announce the round number and, for every seat, score, donuts, glazed_used and jelly_used. Remaining picks are not announced.
3. **poll** (all players): Every message is broadcast to all once all are in: 'Seat {seat} says: {value}'. Messages are not binding.
4. **poll** (all players): choice = answer (secret until the reveal)
5. **update** (all players): void = (choice == 'Glazed' and glazed_picks == 0) or (choice == 'Jelly' and jelly_picks == 0); gain = 0
6. **tell** (all players): Reveal every seat's choice together, with VOID shown for each seat whose void is true.
7. **update** (all players): For each donut D, let n_D = the number of seats with choice == D and void == false. A seat with void == false whose choice D has n_D == 1 gets gain = value of D (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), score += gain and donuts += 1. When n_D >= 2, nobody gains from D.
8. **update** (all players): If void == false and choice == 'Glazed': glazed_picks -= 1 and glazed_used += 1. If void == false and choice == 'Jelly': jelly_picks -= 1 and jelly_used += 1. This applies whether the donut was won or discarded.
9. **tell** (all players): Announce each seat's gain this round and every seat's new score and donuts.
10. **check** (all players): End the game if round >= 10, otherwise continue.

## Ending

- ends when: round >= 10
- ranked by: `you.score * 100 + you.donuts` (the highest wins; players level at the top share the win)
- decided by: Highest point total wins. Among players tied on points, the one with the most donuts collected wins. Players still tied share the win, which stands for the source's draw.

## Choices the source did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer fixed the table at 4. The five-donut row against four choosers is what creates the collision tension, so another count would change the game.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous, non-binding messages. Players want different donuts, so claims and bluffs about plans (and hidden pick splits) give real material to reason about.
- Strategy at the table: A thoughtful player infers others' remaining premium picks from the public glazed_used and jelly_used, times Glazed for rounds when others are likely out, and uses talk to bluff or deter. A thoughtless player always grabs Glazed and collides.
- Tie-break encoded as score * 100 + donuts: Donuts can never exceed 10, so multiplying the score by 100 keeps points primary and donuts as the tie-break.
- Glazed and Jelly are always offered, even with no picks left: The rules define void choices as possible outcomes, so the option must exist.

## Simplifications

- A final draw among tied players is represented as a shared win: The engine has no separate draw: players level at the top share the win, which matches the source's draw among those players.

## Unsupported (needs engine work)

- none
