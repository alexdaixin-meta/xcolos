# new_york_slice: ready for review

Built from the variation **Secret Slice** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each player is secretly dealt a distinct favourite topping. Every collected slice of that type is worth +1 at the end. (fixes: With perfect information there is nothing hidden to infer, so opponent modelling reduces to calculation.): This creates a hidden type. The Slicer must guess what each picker wants, and pickers can bluff or reveal through their picks.
- Each round, every player writes one short message at the same time, before the cut. All messages are then shown. (fixes: With perfect information there is nothing hidden to infer, so opponent modelling reduces to calculation.): Players can claim favourites, true or false, to steer the Slicer's cut. Since only one player can win, each player benefits from a cut that favours them, so believing a claim has a cost.
- Slices are laid out in a numbered line of 6. The Slicer gives two cut positions, which produce three contiguous portions. (fixes: The circular layout and wrap-around cuts suggest a spatial arrangement and make the cut harder to state as numbers.): The cut becomes two numbers, with no circle or adjacency.
- Special cards are removed. The game uses four topping types with fixed majority values and a fixed anchovy penalty. (fixes: Many unique Special cards with different effects create a long chain of rules and too many attributes to build.): This keeps the rules short and buildable.
- The game is fixed at 3 players, 6 rounds and a 36-slice deck shuffled once. Each player is Slicer twice. (fixes: Eleven slices per round, up to 6 players and a variable number of stacks make rounds long and the step count high.): The game becomes short and has a fixed size. Every player slices equally often and holds every pick position equally often.
- The Slicer declares eat or collect for their eventual leftover portion as part of the cut. (fixes: The Slicer would need a separate eat-or-collect decision after the picks, which exceeds the limit on choice steps per round.): This keeps choice steps at 4. It also adds a commitment tension, because the Slicer does not know which portion will be left.

Objective: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SEAT SYMMETRY. Over 6 rounds the Slicer order is P1, P2, P3, P1, P2, P3. Each player is Slicer twice, First picker twice and Second picker twice. Role counts are identical, so move order gives no lasting edge. The only asymmetry is timing: P1 cuts round 1 with no history, and P1 picks first in round
- playable: pass. COMPLETENESS.
- The cut constraint 1<=c1<c2<=5 always yields three non-empty contiguous portions.
- Pick order is fully specified: the player after the Slicer picks first, the remaining player second, the Slicer takes the last portion.
- The eat/collect rule is defined for every slice type. Non-pepp
- reasoning_over_luck: pass. CHANCE SOURCES.
(1) Row order. Each row is fully revealed before any decision, so all players face the same visible information. Only future rows are unknown.
(2) The favourite deal. A favourite is worth +1 per collected slice, roughly +3 to +5, plus a tiebreak edge in one majority race. The prize s

## Complexity

- steps_per_round: designed 12, built 12, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 12, built 41, limit 20 (built: 80)
- hidden_elements: designed 1, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck holds 36 slices
- pass: Setup: three favourites dealt from four toppings, one left over (which ones is chance)
- pass: After round 1 the deck holds 30 slices
- pass: After round 2 the deck holds 24 slices
- pass: P1 is the Slicer in round 1
- pass: P1 is the Slicer in round 4
- pass: P2 is the Slicer in round 5
- pass: P3 is the Slicer in round 3
- pass: Round 1: P2 picks first, P3 second, Slicer P1 does not pick
- pass: Round 2: P3 picks first, P1 second, Slicer P2 does not pick
- pass: Talk changes nothing: an all-Cheese row split 1/1/4 lands as cut
- pass: Cut 1-4 gives A=1, B=3, C=2 slices
- pass: Second picker cannot take the portion the first picker took
- pass: Slicer gets the last portion with declared eat
- pass: Slicer gets the last portion with declared collect
- pass: Eat sends Pepperoni to eaten
- pass: Collect sends Pepperoni to pepperoni
- pass: Anchovy is collected whether the mode is eat or collect
- pass: Strict majorities score; tied majorities score nothing
- pass: Each eaten Pepperoni is worth 1
- pass: Each collected Anchovy costs 1 (tied anchovy, no majority)
- pass: Collected favourite slices count, eaten ones do not
- pass: Tied top scores share the win
- pass: All level at the end: every seat shares the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 8, 'seats 1 and 2': 1, 'seat 2': 6, 'seat 3': 4, 'seats 2 and 3': 1}, 36-36 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 36.0 decisions, prompts of 235 characters on average (longest 312)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 20, 'seats 1 and 2': 2, 'seat 2': 14, 'seat 3': 21, 'seats 2 and 3': 1, 'seats 1 and 3': 2}
- always `first@seat1`: won 16, lost 40, drew 4
- always `first@seat2`: won 16, lost 40, drew 4
- always `last@seat1`: won 17, lost 42, drew 1
- always `last@seat2`: won 20, lost 38, drew 2

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The rotation of Slicer and pickers, the three portions and the three distinct favourites from four toppings all depend on exactly 3 seats.
- Strategy check: A thoughtful Slicer cuts so that every portion is equally unattractive to the others and reads their collections and talk to guess their favourites. Pickers weigh eating pepperoni (+1 now) against contesting the 5-point pepperoni majority, and avoid or deny anchovy around the 10-point majority.
- Keep the talk step as a simultaneous poll broadcast to all: The source says messages are written at the same time without seeing the others. Players have opposing interests over portions and majorities, so the talk gives them bluffing and bargaining material.
- Cut and mode given as one combined choice of 20 options: The source says the Slicer declares eat or collect in the same answer as the cut. One choice list enforces 1 <= c1 < c2 <= 5 exactly.
- Picks offered as portion plus mode in one choice: The source has each picker choose a portion and declare eat or collect together.

## Simplifications

- Rows are drawn at random from the deck each round instead of shuffling once and splitting into 6 rows at setup: Drawing 6 random slices per round without replacement gives the same distribution and keeps future rows hidden, using the engine's draw operation.
- A tie for the highest total is a shared win rather than a draw: The engine has no separate draw; players level at the top share the win, which matches the outcome that nobody wins alone.
- Strict majority is computed by comparing each player's count with both other players' counts: There is no direct player-attribute operand; the comparison is written out across the 3 seats in arithmetic.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `positions` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
