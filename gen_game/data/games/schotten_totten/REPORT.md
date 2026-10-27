# schotten_totten: ready for review

Built from the variation **Schotten Totten: Five Stones** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Remove the adjacency win. The game is won by claiming 3 of the 5 Stones, which is a strict majority. (fixes: The '3 adjacent Stones' victory depends on adjacency in a line, which is a spatial element the platform excludes.): This keeps a 'first to a majority' race without any spatial relation.
- Use 5 Stones instead of 9, and a 36-card deck (4 colours x values 1-9) instead of 54 cards. (fixes: Nine Stones need 18 side attributes plus hands, deck and scores, which is more than 20 attributes.): Ten Stone-side lists plus hands, deck and claim tracking fit within 20 attributes. The smaller deck keeps formations about as frequent relative to the number of Stones.
- Make one round equal one player's turn. Players alternate, and each round has at most one draw. (fixes: A round in which both players play and draw has two random draws, but the limit is one.): This gives exactly one chance event per round.
- Fix the length at 30 rounds: 5 Stones x 3 cards x 2 players. The game can end earlier when someone reaches 3 Stones. (fixes: A full game runs past 40 rounds.): This keeps the game within 40 rounds.
- Remove early claims. A Stone is resolved automatically as soon as both sides hold 3 cards. The tie-break 'player who completed their side first' is kept and tracked with one attribute per Stone. (fixes: The early-claim 'proof' rule cannot be checked by simple arithmetic.): Every resolution becomes pure arithmetic, while the tempo element of the tie-break survives.
- Define formation strength numerically: strength = sum of values + a tier bonus. The bonus is 120 for a Straight Flush, 90 for Three of a Kind, 60 for a Flush, 30 for a Straight, and 0 otherwise. (fixes: Recognising formations is described in words and needs an exact arithmetic definition for the engine.): The highest possible sum is 27, which is less than the 30-point gap between tiers. So the formula reproduces the original order exactly, and a single calculation compares two sides.

Objective: The first player to claim 3 of the 5 Stones wins immediately. If the game reaches the end of round 30 without this, the player with more claimed Stones wins, and equal counts are a draw. With the first-finisher tie-break every resolved Stone has an owner, so in practice someone reaches 3.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. FORMATION ORDERING, checked against the labels. Strength = S + bonus.
| Formation | Min strength | Max strength |
|---|---|---|
| High sum | 1+1+2 = 4 | 9+9+8 = 26 |
| Straight | 1+2+3+30 = 36 | 7+8+9+30 = 54 |
| Flush (not straight flush) | 1+2+4+60 = 67 | 9+8+6+60 = 83 |
| Three of a Kind | 3+90 =
- playable: pass. COMPLETENESS:
- Setup, turn order, legal plays and first finisher are specified. Step 5 records the first finisher only if the other side is not yet full, so exactly one finisher exists per Stone.
- Resolution is specified, and only the Stone just played can become full in a round, so step 7 handles
- reasoning_over_luck: pass. CHANCE. The deal and the draws decide which formations are available, as in the original. Rough estimate: about 30-40% of outcomes are driven by the cards.

WHAT REASONING DOES:
- Players choose which Stones to concede and which to contest, with 3 of 5 needed.
- They commit cards irrevocably, with t

## Complexity

- steps_per_round: designed 12, built 10, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 20, built 41, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 setup: each seat holds 6 cards and the deck holds 24
- pass: R2 odd round: only seat 1 is asked
- pass: R2 even round: only seat 2 is asked
- pass: R3 the card options are exactly the cards in hand
- pass: R4 a claimed Stone and a Stone with a full side are not offered
- pass: R5 the played card leaves the hand and goes onto the chosen Stone side
- pass: R6 A finishes Stone 1 first, then B ties it: A claims
- pass: R7 with cards in the deck the active player draws one
- pass: R7 with an empty deck no card is drawn
- pass: R8 straight flush R3 R4 R5 (132) beats three 9s (117)
- pass: R9 three 1s (93) beat flush Y6 Y8 Y9 (83)
- pass: R10 flush B1 B2 B4 (67) beats straight R7 B8 G9 (54)
- pass: R11 mixed straight R1 B2 G3 (36) beats G9 Y9 R8 (26)
- pass: R12 no formation is just the sum: R2 B5 G9 (16) beats a pair Y7 G7 R1 (15)
- pass: R13 B completes Stone 1 with the stronger side (22 vs 10) and claims it
- pass: R14 B finishes Stone 1 first, then A ties it at 16: B claims
- pass: R15 a claimed Stone is not offered even though A's side is not full
- pass: R16 A claims a third Stone and wins at once
- pass: R17 round 30 ends with B ahead 2 to 1: B wins
- pass: R17 round 30 ends level at 1 Stone each: both seats share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 13, 'seat 1': 7}, 52-58 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 54.7 decisions, prompts of 92 characters on average (longest 114)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 32, 'seat 1': 28}
- always `first@seat1`: won 35, lost 25, drew 0
- always `first@seat2`: won 35, lost 25, drew 0
- always `last@seat1`: won 30, lost 30, drew 0
- always `last@seat2`: won 36, lost 24, drew 0

## Choices the rules did not make

- Exactly 2 players, suggested 2: The designer fixed the game at 2. Each Stone has exactly two sides, A and B, so the game does not scale to more seats.
- No talk step: The rules include no table talk. This is a two-player positional duel, and messages would add nothing the rules call for.
- Card choice and Stone choice are two sequential asks: The source lists them as separate steps (2) and (3). Asking them separately keeps each option list exact.
- Drawing the top card is a random pick from deck: The deck is shuffled, so a random draw is equivalent to taking the top card.
- The round counter and active seat are updated at the start of each round: This lets the engine pick the active player by arithmetic on round parity.
- The end check also fires at round >= 30: The source caps the game at 30 rounds. At that point all 30 slots are filled and every Stone has been resolved.
- Strategy at the table: Each card commits to one Stone permanently. A thoughtful player judges which formations are still possible given the visible cards, decides which Stones to contest and which to concede, and races to finish a side first so they win ties.

## Simplifications

- Stone sides are table attributes (stone_k_a and stone_k_b) rather than per-player lists: The engine has no player-attribute operand for comparison. Keeping both sides on the table lets resolution compare the two strengths directly.
- Strength is computed by calculating each card's colour (first letter) and value (digit) inside the resolution update: The engine has no lookup operation. The formation test is pure arithmetic on the three values and colours, so no referee is needed.
- All five Stones are resolved in one update step, using per-Stone conditional operations: Each Stone's resolution is an independent conditional update. No branching block of steps is needed.
