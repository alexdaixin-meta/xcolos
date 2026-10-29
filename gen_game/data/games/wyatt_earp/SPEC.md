# Wanted: Dead or Alive (Majority Rule)

Over 6 rounds, players secretly spread 12 deputies across five outlaws whose posters grow. The player with the most deputies on each outlaw collects its poster, and each player's secret informant outlaw is worth $3,000 more at the end.

Players: 3 to 4, best with 3

## Parameters

- `outlaw_count` = 5
- `starting_poster` = 2000
- `sighting_bonus` = 1000
- `starting_deputies` = 12
- `starting_money` = 0
- `informant_tip` = 3000
- `rounds` = 6
- `max_commit_per_round` = 4
- `min_commit_per_round` = 0

## Round

1. **update** (all players): round += 1. sighted is set to one outlaw picked uniformly at random from outlaws, which is not removed (with replacement). The poster of sighted rises by 1000, for example poster_red += 1000 if sighted is Red.
2. **tell** (all players): The table hears: 'Round {round}: {sighted} was sighted; its poster is now {poster of sighted}.'
3. **sync** (all players): Each player is sent their own state: deputies, informant, their deputy counts, all posters and all public deputy counts.
4. **poll** (all players): All messages are collected at once, then broadcast to everyone as 'Seat {seat} says: {value}'. Talk is not binding.
5. **poll** (all players): choice_outlaw is set to the outlaw and choice_number to min(n, deputies). No answer is seen until all are in.
6. **tell** (all players): Every player's choice is announced: 'Seat {seat} commits {choice_number} deputies to {choice_outlaw}.'
7. **update** (all players): For each player, deputies -= choice_number, and the deputy count matching choice_outlaw (d_red, d_blue, d_green, d_yellow or d_black) += choice_number. Posters do not change.
8. **update** (all players): This step runs only when round == 6. Every player's informant is revealed to all. For each player, the poster of their informant += 3000.
9. **update** (all players): This step runs only when round == 6. For each outlaw X: max_X = the maximum over players of d_X, and tied_X = the number of players with d_X == max_X. For each player and each outlaw X, if max_X > 0 and d_X == max_X, then money += floor(poster_X / tied_X). An outlaw with max_X == 0 escapes and pays nobody. Unused deputies are worth nothing.
10. **tell** (all players): This step runs only when round == 6. The final posters, the informants and each player's money are announced.
11. **check** (all players): If round >= 6 the game ends. Otherwise play continues with the next round.

## Ending

- ends when: round >= 6
- ranked by: `you.money` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their money after the final payout. The player with the most money wins, and players tied for the most money share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer suggests 3, and the source allows 3 to 4. Majority contests need rivals, and 3 is the smallest table where a player can be outbid or split. With 5 informants the table cannot exceed 5, and the source caps it at 4.
- Talk kept as a simultaneous poll broadcast to all: The rules require it. Players disagree about which outlaws to contest and can bluff about their informant, so talk gives them something to reason about.
- Commitment offered as one combined choice of outlaw and number: This keeps both parts of the commitment in a single simultaneous poll, so no part is seen early.
- Remaining deputies made public: They follow directly from the announced commitments, so hiding them would hide nothing.
- Strategy at the table: A thoughtful player pushes deputies onto their own informant without giving it away, saves deputies for late sightings, avoids costly ties, and reads others' talk and commitments for hints about their informants.

## Simplifications

- A tie for the most money is a shared win rather than a separate draw: The engine ranks by one expression, and players level at the top share the win.
- End-of-game payout steps sit in the round with a 'round == 6' condition: The step list is flat. Conditional single steps reproduce the end-of-game payout exactly.
- Per-outlaw maximum and tie counts kept as table scratch attributes: Comparing player attributes needs a table attribute beside them.

## Unsupported (needs engine work)

- none
