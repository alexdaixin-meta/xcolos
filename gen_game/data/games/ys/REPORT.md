# ys: ready for review

Built from the variation **Ys: Brokers of the Blind Market** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace sequential broker placement with one simultaneous secret allocation: each player splits 6 broker strength among 4 districts. (fixes: Ten sequential broker placements per player per round far exceed the choice-step limit.): Keeps blind majority bidding and its bluff-by-concealment in a single choice step.
- Replace the market grid with a simultaneous market vote: each player names one gem color, each vote raises that color's price by 1, and colors receiving no vote drop by 1 (minimum 1). (fixes: The market grid (rows intersecting columns) is a spatial board structure.): Keeps price manipulation without any row/column structure.
- Remove the ship, market and character decks. Districts always offer fixed rewards. The only randomness is a one-time secret deal of each player's favored color. (fixes: Several random decks per round (ships, market card, characters) exceed one random draw per round and add luck.): Removes per-round luck and keeps random draws at 0 per round.
- Drop character cards. The palace is replaced by a Commerce district that pays flat points. (fixes: Character cards with special powers create long rule chains and many attributes.): Cuts rule chains while keeping a non-gem majority option like Ys's commercial area.
- Use ONE hidden element: each player's secret favored color, whose gems score double. Allocations are revealed after each round. (fixes: Face-down brokers create a large amount of hidden state (many hidden elements).): Bluffing is now about hiding which color you truly want. Opponents must infer it from bids and votes in order to avoid raising your color.
- Make all choices simultaneous and drop turn order. (fixes: Turn-order bidding plus sequential placement gives later or earlier seats structural edges that need a tie-break deck.): Removes seat advantage and the tie-break deck.
- Fix the player count at 3, one secret color per player, with colors dealt as a random permutation. (fixes: The 2-player version reduces to a pure difference contest in which denial dominates.): Three players mean a rival's gain is not purely your loss. Symmetric types mean no player is dealt a better type.

Objective: The player with the highest final score wins. If two or three players tie for the highest score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PER-DISTRICT AWARDS: gem district: single first 2 gems, second 1, each tied-first 1. Commerce: 8 / 3 / 3. Prices start at 3 and each round's three votes add +3 in total. If each player votes their own favored color, every price ends at 3+6=9, so a favored gem is worth 18 and any other gem 9. Even at
- playable: pass. COMPLETENESS: the tie and second-place rules are fully specified: strict highest wins first; a tie at the top means all tied are tied-first; second needs a single first and a strict, untied next-highest above 0. Zero influence earns nothing. Price changes are fully specified, including the floor of 
- reasoning_over_luck: pass. CHANCE: the only random element is the favored-color deal. Colors are symmetric (same starting price, same rules), so the deal gives no player an advantage. Chance's share of the result is close to 0%.

GOOD PLAY BY ALL: if all three play the same symmetric strategy (e.g. all-in on their own color, 

## Complexity

- steps_per_round: designed 12, built 11, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 10, built 36, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals all three favored colors, leaving the color deck empty after the first round
- pass: Setup sets prices to 3 and every player to zero gems and zero commerce (seen through one round)
- pass: Game ends after round 6 and the top score wins
- pass: A round with talk proceeds; all-commerce three-way tie gives 3 each
- pass: Allocations summing to 6 are offered, others are not
- pass: Revealed allocations decide every district
- pass: Single first in Red (4,1,0) gains 2 red gems
- pass: Untied second in Red (4,1,0) gains 1, third gains nothing
- pass: Tied first in Blue (3,3,1) gives 1, 1, 0
- pass: Tied second in Green (4,1,1) gets nothing
- pass: Commerce tied first (2,2,0) gives 3, 3, 0
- pass: Commerce single first gets 8 and untied second gets 3
- pass: Districts where everyone has 0 influence award nothing
- pass: Every seat is offered a vote among Red, Blue and Green
- pass: Two votes raise a price from 3 to 5
- pass: Unvoted colors fall by 1 but not below 1
- pass: Vote round updates prices from all votes
- pass: Final score counts favored gems twice plus commerce
- pass: Favored colors are revealed at game end
- pass: Three-way tie for top score is shared

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 6, 'seat 2': 7, 'seat 3': 7}, 54-54 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 54.0 decisions, prompts of 151 characters on average (longest 161)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 18, 'seat 2': 27, 'seat 3': 15}
- always `first@seat1`: won 30, lost 30, drew 0
- always `first@seat2`: won 39, lost 19, drew 2
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer chose 3, and the game has three colors dealt one per player, so it cannot run at any other size.
- Strategy check: A thoughtful player hides their favored color, reads rivals' colors from their allocations and votes, contests gem districts where rivals are thin, takes Commerce when gems are crowded, and steers votes toward their own color without revealing it.
- Keep talk as a simultaneous poll broadcast to all: The rules make talk simultaneous. Talk earns its place because each player wants a different color pumped and can bluff about it, so following a proposal can cost them.
- Allocation as one choice from the 84 valid 'r/b/g/c' splits: The engine takes one answer per question. A list of every valid split enforces the sum of 6 and keeps all four numbers in one simultaneous secret submission.
- Votes stored in a public attribute and announced after the price update: The poll keeps votes hidden until all are in, and the rules show the votes after prices change.
- Score computed in the round-6 update: The final score is needed only once the game ends, and computing it in that step keeps rank_by a single attribute.

## Simplifications

- A tie for highest score is a shared win at the top rather than a separately labeled draw: The engine has no separate draw: players level at the top share the win, which matches the source's draw outcome.
- Allocations are held in pending_allocation and copied to public alloc_* attributes at the reveal: This keeps the submission secret until all are in, then reveals it as the rules require.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `alloc_options` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
