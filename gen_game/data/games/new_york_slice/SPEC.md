# Secret Slice

Three players take turns cutting a row of six pizza slices into three portions. The others pick first and the cutter gets the last portion. Each player chooses whether to eat pepperoni for points or collect it toward majorities, while chasing a secret favourite topping.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `slices_per_type` = 9
- `deck_size` = 36
- `rows` = 6
- `row_size` = 6
- `rounds` = 6
- `cut_min` = 1
- `cut_max` = 5
- `majority_cheese` = 7
- `majority_mushroom` = 7
- `majority_pepperoni` = 5
- `majority_anchovy` = 10
- `eaten_pepperoni_point` = 1
- `anchovy_penalty` = 1
- `favourite_bonus` = 1

## Round

1. **update** (all players): round += 1; slicer = ((round-1) mod 3) + 1; first_picker = (slicer mod 3) + 1; second_picker = (first_picker mod 3) + 1; taken = []
2. **update** (all players): row = []; 6 times: draw one slice at random from deck, append it to row, remove it from deck. Announce the row with positions 1 to 6 and who is Slicer, first picker and second picker.
3. **poll** (all players): Nothing changes; all messages are broadcast at once: {"to": "all", "text": "Seat {seat} says: {value}"}
4. **ask** (seat slicer): set c1, c2, slicer_mode; portion_a = row[1..c1]; portion_b = row[c1+1..c2]; portion_c = row[c2+1..6]; announce the three portions
5. **ask** (seat first_picker): the picker adds the chosen portion's Cheese to cheese, Mushroom to mushroom and Anchovy to anchovy; its Pepperoni goes to eaten if eat, or to pepperoni if collect; append the letter to taken; announce
6. **ask** (seat second_picker): same accounting as the first pick for the second picker; append the letter to taken; announce
7. **update** (seat slicer): the Slicer takes the portion not in taken, with slicer_mode: Cheese to cheese, Mushroom to mushroom, Anchovy to anchovy, Pepperoni to eaten if slicer_mode = eat, otherwise to pepperoni; announce
8. **update** (all players): when round = 6: for each player, score = 7 if cheese is strictly greater than both other players' cheese + 7 if mushroom is strictly greater than both others' + 5 if pepperoni is strictly greater than both others' + 10 if anchovy is strictly greater than both others' + eaten - anchovy + the collected count of their own favourite (cheese, mushroom, pepperoni or anchovy). Reveal every favourite and announce all totals.
9. **check** (all players): end the game if round >= 6, otherwise continue

## Ending

- ends when: round >= 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final total; the highest total wins, and players tied for the highest share the win (the source calls this a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The rotation of Slicer and pickers, the three portions and the three distinct favourites from four toppings all depend on exactly 3 seats.
- Strategy check: A thoughtful Slicer cuts so that every portion is equally unattractive to the others and reads their collections and talk to guess their favourites. Pickers weigh eating pepperoni (+1 now) against contesting the 5-point pepperoni majority, and avoid or deny anchovy around the 10-point majority.
- Keep the talk step as a simultaneous poll broadcast to all: The source says messages are written at the same time without seeing the others. Players have opposing interests over portions and majorities, so the talk gives them bluffing and bargaining material.
- Cut and mode given as one combined choice of 20 options: The source says the Slicer declares eat or collect in the same answer as the cut. One choice list enforces 1 <= c1 < c2 <= 5 exactly.
- Picks offered as portion plus mode in one choice: The source has each picker choose a portion and declare eat or collect together.

## Simplifications

- Rows are drawn at random from the deck each round instead of shuffling once and splitting into 6 rows at setup: Drawing 6 random slices per round without replacement gives the same distribution and keeps future rows hidden, using the engine's draw operation.
- A tie for the highest total is a shared win rather than a draw: The engine has no separate draw; players level at the top share the win, which matches the outcome that nobody wins alone.
- Strict majority is computed by comparing each player's count with both other players' counts: There is no direct player-attribute operand; the comparison is written out across the 3 seats in arithmetic.

## Unsupported (needs engine work)

- none
