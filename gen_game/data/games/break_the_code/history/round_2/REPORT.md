# break_the_code: needs review

Built from the variation **Break the Code: Coarse Clues** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Every per-player state value is written with an owner: 'that player's solved', 'that player's guesses left'. A rule states that both players are scored independently, so both can solve in the same leg, even in the same round. (fixes: P1 (previous variation): 'solved' had no owner): Removes the shared-flag reading and the same-round ambiguity.
- The card set is replaced with six coarse cards, each with at most 4 possible answers: count of digits 5 or higher, count of odd digits, count of primes (2, 3, 5, 7), count of multiples of 3 (0, 3, 6, 9), count of consecutive neighbouring pairs, and sum mod 4. There are 120 possible codes. Any plan of 3 asks, even an adaptive one, has at most 4×4×4 = 64 answer paths, so at least 56 codes cannot be pinned down by leg-round 3 under any asking plan. Even after 4 asks a code may remain ambiguous. (fixes: P2 (previous variation): cards 1, 4 and 5 identified any code with certainty): No recipe guarantees a solve. Players must choose cards adaptively for information, judge how many candidates remain, and decide when a guess is worth its risk.
- A wrong guess now gives -1 to the guesser and +1 to the code's owner, a swing of 2. An owner whose code is not cracked by the end of the leg scores +1. A correct guess scores 5 - leg-round as before. (fixes: P3 (previous variation): almost no interaction): Code choice now pays directly: an ambiguous code earns points by luring wrong guesses and surviving. Guess timing becomes a real expected-value calculation that depends on the remaining candidates and on the opponent's visible progress. For example, with 2 candidates at leg-round 3 a guess is worth +0.5 over waiting, while at leg-round 4 it is worth -0.5. Players also model which codes the opponent is likely to hide.
- Repeat asks are allowed and simply return the same answer. (fixes: P4 (previous variation): the once-only card restriction cost state for no gain): Saves the used-card attribute and parsing. A repeat is just a wasted ask, which is its own penalty.
- The game is kept as 2 players, 3 legs of 4 rounds, a 3-digit sorted numeric code, simultaneous asks and guesses, and arithmetic card answers. (fixes: P5 (original): the full game exceeds the platform's limits): Fits within 16 steps, 3 choice steps, 18 attributes, 1 hidden element and 0 random draws.

Objective: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If those are also equal, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SEATS: Both players enter codes, ask cards and guess simultaneously, and every rule applies to both. Neither seat has an edge from move order or information.

CODE SPACE: There are C(10,3) = 120 codes.

ANSWER DISTRIBUTIONS over the 120 codes:
| Card | Answer counts |
|---|---|
| 1 High (5-9 vs 0-4)
- playable: pass. RULES ARE COMPLETE: Code parsing, invalid defaults, card formulas, repeated cards, pass/wrong/correct, simultaneous solving, leg resets, end-of-leg points, reveals and the tie-break are all specified. The round counter and leg-round formula are explicit.

FINITE AND ARITHMETIC: The game ends after 1
- reasoning_over_luck: pass. CHANCE: The engine makes zero random draws, so chance is about 0%. The only uncertainty is the opponent's chosen code.

WHAT DECIDES THE WINNER:
- Choosing codes that sit in large ambiguity classes, for example ones containing 5 or 7 with feature-similar digits, rather than unique ones like 012 or 1

## Complexity

- steps_per_round: designed 16, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 18, built 39, limit 20 (built: 80)
- hidden_elements: designed 1, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 first round sets round to 1
- pass: R1 round 5 is leg_round 1 so revealed codes reset to -1
- pass: R2 initial score, wrong_count and revealed_code
- pass: R2 score and wrong_count are not reset at a new leg
- pass: R3 guesses_left and solved reset at leg start so both may guess and score 4
- pass: R4 codes stay unchanged in leg_round 2 so correct guesses score 3
- pass: R5 entries 852 and 12 are stored as 258 and 12, so guesses of them are right
- pass: R5 entries 852 and 12 are revealed as 258 and 12 after the leg
- pass: R6 repeated digits and a declined entry both store code 12
- pass: R7 asking card 1 is offered and changes no score (answer is private)
- pass: R8 asking card 2 is offered and changes no score (answer is private)
- pass: R9 asking card 3 is offered and changes no score (answer is private)
- pass: R10 asking card 4 is offered and changes no score (answer is private)
- pass: R11 both seats ask card 5 and no score changes (answers are private)
- pass: R12 asking card 6 is offered and changes no score (answer is private)
- pass: R13 declining a card changes nothing observable
- pass: R14 both seats ask cards; no score changes and codes stay hidden
- pass: R15 seat with no guesses left and seat already solved are not asked to guess
- pass: R16 a guess with repeated digits is a pass
- pass: R17 correct guess 852 against code 258 in leg_round 3 scores 2
- pass: R18 wrong guess costs the guesser 1 and gives the opponent 1
- pass: R19 both guess right in leg_round 3 and both score 2
- pass: R20 one right and one wrong guess; codes not revealed
- pass: R21 leg end: unsolved-opponent bonus and codes revealed
- pass: R22 game ends after round 12; higher score wins
- pass: R22 level score broken by fewer wrong guesses
- pass: R22 full tie is a shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 6, 'seat 1': 11, 'seats 1 and 2': 3}, 45-53 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 48.7 decisions, prompts of 416 characters on average (longest 438)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- always taking the last option as seat 1 wins 100% of decided matches against random seats
- always taking the last option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seat 2': 18, 'seat 1': 26, 'seats 1 and 2': 16}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 60, lost 0, drew 0
- always `last@seat1`: won 60, lost 0, drew 0
- always `last@seat2`: won 60, lost 0, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The rules explicitly accept a code or guess written as three different digits in any order, sorted afterwards. The game instead offers only a short list of pre-sorted codes, and that list (guess_offer) is filtered down to codes matching the revealed SUM answer, so valid guesses such as 5,8,2 or 8,5,2 become passes and score nothing. The round counter also jumps from 0 to 2 in round 1, so the round and leg-round bookkeeping is off.
- round 1: fix_game: The failures differ from attempt to attempt and are file bugs. The latest one shows the per-player `code` attribute is never written, so every guess is compared against an unset code and `solved` can never become 1.
- round 1: fix_tests: The rules say a guess from a player with 0 guesses left counts as a pass, so the outcome is the same whether the game polls that seat or skips it. The test failed only because it required a 'pass' option to be offered to Ada, who by the rule under test cannot act; it also leans on the internal guesses_left counter.
- round 1: fix_game: The game takes the leg-start code as free text, while the guess is a numeric entry. The tests' code choices (147, 258) were therefore never offered at the code step and were played as guesses instead: the codes defaulted to 0-1-2, both guesses were wrong, and each seat lost a point. The rules and tests are consistent; the game's code-entry step is the problem.
- round 2: revise_rules: The game behaves as specified, but the scoring makes never guessing dominant. A wrong guess is a 2-point swing (-1 to the guesser, +1 to the code's owner), there are 120 possible codes, four card answers rarely pin one down, and an unguessed code earns its owner +1 each leg. A fixed policy that effectively passes therefore beats random play every time, so the flaw is in the rules, not the file.

## Choices the rules did not make

- Exactly 2 players: The designer fixed the game at 2. Each player attacks the single opponent's code, and owner bonuses refer to that one opponent.
- No talk step: The rules contain no table talk. With two players racing to deduce each other's codes, talk would add nothing the rules want.
- Rank by score*100 - wrong_count: Wrong guesses are at most 6 per match, so score dominates and fewer wrong guesses breaks ties. Players level on both share the win, which is the draw.
- Leg starts listed as leg_start_1, leg_start_2 and leg_start_3: Each parameter must be a single number.
- guesses_left, solved and card_asked are public: The rules announce each player's card and guess results, so both players can infer these values anyway.
- A revealed_code attribute copies the code at the end of each leg: This gives the R9 reveal a stated piece of public state, while the live code stays private during play.
- Strategy at the table: A thoughtful player picks the cards that split the remaining candidate codes most evenly. They also weigh an early guess, which is worth more points, against the -1 penalty plus +1 to the opponent for a wrong guess.

## Simplifications

- Code and guess entries are taken as a whole number from 0 to 999 or a decline, rather than as free text: The engine's number answer has a range, so out-of-range and non-numeric entries cannot occur. Declining covers the 'missing' case, which still maps to code 12 or a pass as the rules require.
- Invalid card numbers are reduced to the decline option: The choice list offers only cards 1 to 6 or decline. Declining has the same effect as the rules' invalid entry: no question.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 2 players: the match crashed: FlowError: 'you.guesses_left > 0' reads `you` where there is no player
- 2: passed
