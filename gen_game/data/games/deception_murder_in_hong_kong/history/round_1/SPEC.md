# Deception: Five Clues

A hidden-role deduction game. A public Forensic Scientist marks scene-tile options to steer Investigators towards the Murderer's secret Clue and Means. The Murderer side wins by evading for 5 rounds, or by finding the Witness after the case is solved.

Players: 6 to 8, best with 7

## Parameters

- `rounds` = 5
- `scientist_seat` = 1
- `clue_list_size` = 16
- `means_list_size` = 16
- `clues_per_player` = 2
- `means_per_player` = 2
- `starting_badges` = 1
- `options_per_tile` = 6
- `deck_tiles` = 6
- `deck_draws` = 3
- `murderers` = 1
- `accomplices` = 1
- `witnesses` = 1
- `investigators_formula_offset` = 4
- `win_value` = 1

## Round

1. **update** (table): round += 1; current_tile = 'Cause of Death' if round==1, 'Location' if round==2, otherwise a random tile removed from tile_deck; every acc_clue and acc_means is cleared; current_tile is announced with its 6 options
2. **ask** (seat 1): marker = the chosen option; the marker is announced to all
3. **poll** (every player except seat 1): broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
4. **poll** (every player with badge == 1): acc_clue = the answer; hidden until resolution
5. **poll** (every player whose acc_clue is not PASS): acc_means = the answer; badge -= 1 for each such player; hidden until resolution
6. **update** (table): each accusation is announced with its accuser and marked correct if acc_clue == key_evidence and acc_means == means_of_murder, wrong otherwise; solved = true if any accusation is correct
7. **ask** (the player whose role is Murderer, when solved == true): hunt_target = the chosen seat
8. **update** (table): when solved == true: if the role of hunt_target is Witness, won = 1 for side murderer, else won = 1 for side investigator; game_over = 1. Else when round == 5: won = 1 for side murderer; game_over = 1
9. **check** (table): end the game if game_over == 1, otherwise continue to the next round

## Ending

- ends when: game_over == 1
- ranked by: `you.won` (the highest wins; players level at the top share the win)
- min_to_win: `1` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: Team win: every player on the winning side has won = 1 and shares the win; the losing side has 0.

## Choices the source did not make

- 6 to 8 players, suggested 7: Kept the designer's 7. Six is the minimum because the four special roles plus 2 Investigators are needed for the Murderer side to hide. Above 8 the talk becomes too long and the Scientist's single marker per round is spread too thin.
- The accusation is split into two simultaneous polls (Clue or PASS, then Means): Offering every Clue-Means pair would mean up to about 200 options. Answers stay hidden until resolution, so the choice is still effectively simultaneous.
- Talk is kept as a simultaneous poll broadcast to all: The source requires it. Players disagree because the Murderer side wants to mislead, so reading each other's statements against the marker is the core of the game.
- The win is recorded as won = 1 for each player on the winning side, with min_to_win 1: This expresses a team win as an arithmetic ranking.
- The Witness Hunt is a single conditional step inside the round, followed by game_over: A flat step list cannot branch into a separate block, but a step with a 'when' condition works.
- Strategy at the table: The Scientist picks markers that point towards one player's cards. Investigators cross-reference the markers with the face-up cards and spend their single badge carefully. The Murderer and Accomplice steer talk towards innocent pairs. The Witness must hint without revealing themself.

## Simplifications

- The Scientist's ban on sending any other message is enforced by never asking seat 1 to talk: The engine only lets players speak when asked.

## Unsupported (needs engine work)

- none
