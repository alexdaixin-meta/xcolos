# Deception: Four Tiles

A hidden-role deduction game: a silent Forensic Scientist marks scene items to steer the Investigators toward the Murderer's secret clue and means within 4 rounds, and if the case is solved the Murderer gets one guess at the Witness to steal the win.

Players: 6 to 8, best with 7

## Parameters

- `clue_words` = 16
- `means_words` = 16
- `scene_tiles` = 8
- `items_per_tile` = 6
- `rounds` = 4
- `clues_per_seat` = 2
- `means_per_seat` = 2
- `scientist_seat` = 1
- `murderers` = 1
- `accomplices` = 1
- `witnesses` = 1
- `investigators_formula_offset` = 4
- `starting_badge_cardholder` = 1
- `starting_badge_scientist` = 0
- `accusations_per_seat` = 1
- `win_value` = 1

## Round

1. **update** (table): round += 1; solved_this_round = false. If round == 1, current_tile = 'Cause of Death'. Otherwise one tile is drawn at random from tile_deck, removed from it, and stored as current_tile. current_tile is appended to revealed_tiles and announced with its 6 items.
2. **ask** (seat 1 (Scientist)): the chosen item is appended to marked_items and announced to all as the marker on current_tile
3. **poll** (seats 2..N): all messages are revealed together, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; no state change
4. **poll** (all seats with badge == 1): a Clue answer is stored in acc_clue; PASS leaves acc_clue empty
5. **poll** (all seats whose acc_clue is non-empty): stored in acc_means
6. **update** (all players): for each seat with acc_clue != '': badge = 0
7. **update** (all players): each accusation (acc_clue, acc_means) with its seat is announced. If acc_clue == key_evidence and acc_means == means_of_murder, it is announced correct, and if solved was false, then solved = true and solved_this_round = true. Otherwise it is announced wrong. solved never returns to false.
8. **update** (all players): acc_clue = '' and acc_means = '' for every player
9. **ask** (the Murderer (seat murderer_seat), only when solved_this_round == true): hunt_target = the chosen seat; it is announced
10. **update** (all players, only when solved == true or round >= 4): if solved == true and hunt_target == witness_seat: won = 1 for every player with side == murderer. If solved == true and hunt_target != witness_seat: won = 1 for every player with side == investigator. If solved == false: won = 1 for every player with side == murderer. All roles are revealed.
11. **check** (table): the game ends if solved == true or round >= 4; otherwise the next round begins

## Ending

- ends when: solved == true or round >= 4
- ranked by: `you.won` (the highest wins; players level at the top share the win)
- min_to_win: `1` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: A team win. Every player whose side won has won = 1 and shares the win. The Investigator side wins if the case is solved and hunt_target is not the Witness's seat. The Murderer side wins if the case is unsolved after 4 rounds, or if it is solved and hunt_target is the Witness's seat.

## Choices the source did not make

- 6 to 8 players, suggested 7: The designer chose 7, and it is kept. The minimum is 6 because seats 2..N must hold the Murderer, the Accomplice, the Witness and at least 2 Investigators, so that the Murderer side can hide and the Witness Hunt is a real guess. The maximum is 8 because more card-holders dilute each accusation and lengthen the talk beyond what can be followed.
- Talk is a simultaneous poll of one short message from seats 2..N, broadcast to all: The source says messages are written at the same time without seeing the others. Talk earns its place because the two sides disagree: the Murderer side misleads, Investigators argue readings of the markers, and the Witness must hint without exposing themselves.
- Role, side and intel are owner-only (ally), and seat knowledge is delivered through the intel text: Each player sees only their own role. Cross-seat knowledge (Accomplice to Murderer, Witness to the pair, Scientist to all) is given exactly as the rules list it.
- Scoring is applied as a single conditional update just before the end check, and the winner is ranked by you.won with min_to_win 1: This makes the team win pure arithmetic on stored values, as the source states.
- All roles are revealed when the game ends: Revealing roles lets observers verify the result. It does not change play.

## Simplifications

- The Scientist's marker is a single choice from the 6 tile items, announced as text: There are no physical tiles or bullet markers; the source already defines the marker as a choice of one item.

## Unsupported (needs engine work)

- none
