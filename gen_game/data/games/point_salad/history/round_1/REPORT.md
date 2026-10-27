# point_salad: needs review

Built from the variation **Secret Salad** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Reduce to 3 veggies (Tomato, Lettuce, Carrot), a fixed market of one of each per round, and one public point card per round drawn from 6 types. (fixes: Far too many unique cards and moving parts (three piles, pile splitting, refilling market) to build within the step, attribute and draw limits.): This keeps the drafting choice (take a veggie or take a scoring card) inside 1 random draw per round and a handful of steps.
- Deal each player a secret Recipe. The three Recipes are rotations of one another, each prizing a different pair of veggies, and they score at game end on the player's whole basket. (fixes: Nearly perfect information: there is little hidden to infer about opponents, so it tests optimisation more than opponent modelling.): This creates hidden types to infer from picks and talk. Every veggie is wanted by exactly two Recipes, so interests clash. Because the Recipes are rotationally symmetric, no Recipe is better than another.
- Point cards score immediately on your basket at the moment you take them. (fixes: End-of-game scoring of many cards against the whole tableau needs per-player storage of every drafted card, which exceeds the attribute limit.): This keeps 'the same veggie counts for many cards' while needing no storage of drafted cards. It also adds a timing decision: take the card early for a little or late for a lot.
- Picks are simultaneous. If two or more players pick the same item, nobody gets it. (fixes: Sequential turns give a seat edge (first pick, tie-break by turn order).): This removes the seat edge, makes predicting opponents central, and lets a player deny a rival at a cost to themselves.
- Use only 6 point-card types of similar value, drawn with replacement, with every card open to all players. (fixes: Luck of which scoring cards appear is large relative to skill.): A card's luck is shared by everyone. What it is worth depends on each player's basket and timing, not on who saw it first.

Objective: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. VALUE OF ITEMS. A Recipe pays 2 per wanted vegetable plus 2 per matched pair. A balanced pair (+1 of each) is worth 2+2+2 = 6, or 3 per vegetable. A wanted vegetable added without a match is worth 2. The unwanted vegetable is worth 0 to the Recipe but still counts for Big Bowl, Rainbow, Balance and 
- playable: pass. RULES COMPLETE. The rules define every case: the vegetable counts, all six Card formulas, collision (2+ pickers means nobody receives it), unclaimed items discarded, Card scored before vegetables are added, Recipe formulas, and the end and draw rules. The game is finite (12 rounds) and decided by ar
- reasoning_over_luck: pass. RANDOMNESS. There are two random sources: the Recipe deal (symmetric, so its luck is near zero) and the per-round Card type (6 equiprobable types, with replacement). Each vegetable's Fan appears about 2 times in 12 rounds. Big Bowl, Rainbow and Balance (about half of the draws) reward any well-built

## Complexity

- steps_per_round: designed 13, built 10, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 17, built 28, limit 20 (built: 80)
- hidden_elements: designed 1, built 3, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 setup: no turn played yet, every seat starts empty (recipes are hidden, so only the clean start is checked)
- pass: R2 setup: every player has t=l=c=0 and points=0
- pass: R3 a round draws a card and advances the round; all pick Card so the draw cannot change any score
- pass: R4 baskets and points carry through a round where everybody collides on Card
- pass: R5 the talk poll happens and play continues normally
- pass: R6 every seat is offered Tomato, Lettuce, Carrot and Card
- pass: R7 the sole Tomato picker gains one tomato; two Card pickers score nothing
- pass: R8 the sole Lettuce picker gains one lettuce
- pass: R9 the sole Carrot picker gains one carrot
- pass: R10 two Tomato pickers get nothing; the sole Card picker on an empty basket gains 0 whatever card is drawn
- pass: R10 three Card pickers on full baskets: nobody scores, whatever card is drawn
- pass: R11 the sole Card picker on an empty basket gains 0 whatever card is drawn, while others collect vegetables
- pass: R12 sole Card picker with t=3: basket unchanged, other seats' points unchanged (card value depends on the draw, not asserted)
- pass: R13 sole Card picker with l=2: basket unchanged, other seats unaffected (card value depends on the draw)
- pass: R14 sole Card picker with c=1: basket unchanged, other seats unaffected (card value depends on the draw)
- pass: R15 sole Card picker with t=2,l=3,c=1: basket unchanged, others collect normally (card value depends on the draw)
- pass: R16 sole Card picker with t=2,l=3,c=1: basket unchanged, others unaffected (card value depends on the draw)
- pass: R17 sole Card picker with t=2,l=2,c=1: basket unchanged, others unaffected (card value depends on the draw)
- pass: R18 sole Card picker with t=3,l=1,c=1: basket unchanged, others unaffected (card value depends on the draw)
- pass: R19 each player's pick is recorded and shown after the round
- pass: R20 the game ends after round 12; empty baskets give everyone 0, so all share the win
- pass: R21 TL player ending with t=3,l=2 scores recipe 14
- pass: R22 LC player ending with l=1,c=4 scores recipe 12
- FAIL: R23 CT player ending with c=2,t=2 scores recipe 16 | rule R23 is broken: When a CT player ends with c=2, t=2, then recipe_score=16.; seat 3 standing: expected 16, got 12; seat 3 recipe_score: expected 16, got 12; seat 3 final_total: expected 16, got 12
- pass: R24 final total adds points to recipe score; a tie at the top is shared
- FAIL: R24 points can decide the winner over a higher recipe score | rule R24 is broken: Final total = points + recipe_score, and the highest final total wins, with players tied at the top sharing the win.; seat 3 standing: expected 16, got 12; seat 3 recipe_score: expected 16, got 12; seat 3 final_total: expected 16, got 12

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 7, 'seat 1': 5, 'seats 1 and 2': 1, 'seat 2': 7}, 72-72 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 72.0 decisions, prompts of 158 characters on average (longest 187)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 18, 'seat 1': 20, 'seats 1 and 2': 2, 'seat 2': 16, 'seats 1, 2 and 3': 1, 'seats 1 and 3': 3}
- always `first@seat1`: won 17, lost 37, drew 6
- always `first@seat2`: won 10, lost 46, drew 4
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: Under the rules, Recipe CT with c=2 and t=2 scores 2x2 + 2x2 + 2 x min(2,2) = 4 + 4 + 4 = 12, which is exactly what the game computed. The test's expected 16 is a miscalculation, probably counting the pair bonus as 2 per vegetable in the pair.
- round 1: fix_tests: The interface defines `card_types` as a numeric parameter equal to 6, but the R3, R10, R11 and R12 tests overwrite it with a list such as ["Balance"]. The game's draw `card_pool[min(card_types - 1, ...)]` then crashes on list minus int, so the crash comes from the tests misusing a parameter, not from a fault in the game file.
- round 1: fix_tests: Under the rules, a CT recipe with c=2, t=2 scores 2×2 + 2×2 + 2×min(2,2) = 4 + 4 + 4 = 12, so the game's 12 is correct and the tests' expected 16 is an arithmetic error. R24 inherits the same wrong expected value.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer set 3. The game needs exactly three Recipes split among three players, and three seats against four market items is what makes collisions and deduction interesting.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous talk. Players disagree about which vegetables to take, since two Recipes overlap on each vegetable, so messages can steer or mislead picks.
- Card scored before vegetables in the same resolve: The rules say the card is scored on the basket as it stands before this round's vegetables are added, so the card update runs first.
- recipe_score and final_total stored as attributes computed after round 12: This makes the Recipe score explicit and checkable before ranking.
- Strategy at this table: A thoughtful player infers others' Recipes from their picks and talk, avoids collisions, contests the Card when it is valuable, and may bluff about their Recipe to send rivals elsewhere.

## Simplifications

- A tie for the highest total is treated as a shared win rather than a 'draw': The engine ranks by one expression and players level at the top share the win, which carries the same outcome information.
- The Recipe reveal is an announcement: The recipe attribute stays ally-visible; the closing tell reveals every Recipe and score to all.
