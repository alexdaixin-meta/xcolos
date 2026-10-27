# break_the_code: needs review

Built from the variation **Break the Code: Three-Leg Duel** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the first-correct-wins race with points. In each leg, a correct guess scores 4, 3, 2 or 1 points in leg-round 1, 2, 3 or 4. A wrong guess costs 1 point. The leg does not stop when one player is correct; the other can still score less by guessing later. The higher match total wins. (fixes: P1): Same-round ties now depend on how early each player committed. A player who solves in leg-round 2 beats one who solves in leg-round 3. When to guess among k candidates becomes an expected-value decision, not a coin toss with nothing at stake.
- Play 3 legs of 4 rounds each (12 rounds). Each leg uses fresh secret codes, and both codes are revealed at the end of each leg. (fixes: P2): Three independent legs average out the luck of a final 1/2 pick. Revealing codes lets players learn and exploit each other's code-choice habits in later legs.
- Each leg has only 4 ask rounds, so each player uses 4 of the 6 cards. A card cannot be repeated within a leg; all cards become available again next leg. (fixes: P3): Which 4 cards to ask, and in which order given earlier answers, becomes a real adaptive planning decision. The two players reach different information at different speeds.
- Same leg structure as above, with code choice repeated at the start of every leg. (fixes: P4): Gives multiple deduction samples and repeated code-choice duels, where opponent modelling can pay off.
- Card default: a missing, invalid or already-used card number is replaced by the lowest-numbered card that player has not used this leg. (fixes: P5): Every ask resolves deterministically.
- Guess defaults:
- Three different digits 0-9 written in any order are sorted ascending and accepted.
- Anything else (repeats, wrong length, non-digits, blank) counts as a pass and costs nothing.
- A guess written with no guesses left, or after already guessing correctly this leg, counts as a pass and costs nothing. (fixes: P6): Every guess resolves deterministically.
- Code default: three different digits in any order are sorted. Any other entry becomes 0-1-2. This code is identifiable from the SUM card alone, which is a natural penalty. (fixes: P7): Setup always produces a legal code.
- Store each code as one number 100A+10B+C and each guess the same way. Store used cards as one bitmask per player (card n adds 2^(n-1)). Compute each answer in a single calculation step per player. (fixes: P8): Keeps the game at 17 attributes and 13 steps.
- Tie-break: if totals are equal, the player with fewer wrong guesses over the match wins. Otherwise it is a draw. (fixes: P1): Turns remaining ties into results that reward careful play.

Objective: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Code space: C(10,3) = 120 codes. Scoring for a correct guess is 5 - leg-round: 4, 3, 2, 1 in rounds 1 to 4 of a leg. A wrong guess costs -1. Each player has 2 guesses per leg.

How much the cards reveal. Range d has (10-d)(d-1) codes: d=2:8, 3:14, 4:18, 5:20, 6:20, 7:18, 8:14, 9:8. Knowing SUM s and
- playable: pass. Rules cover every case:
- invalid codes default to 0-1-2;
- invalid or used cards default to the lowest unused card;
- invalid guesses, guesses after solving, and guesses with 0 left all count as a pass;
- scoring, reveal and tie-breaks are fully specified.

All six card formulas are arithmetic on t
- reasoning_over_luck: pass. There are no random draws. Chance is essentially 0%, apart from a guess between 2 or 3 candidates, and those candidates exist only because of the opponent's chosen code.

Outcomes depend on:
- choosing informative card sequences adaptively (for example, RANGE then SUM, then whichever card splits the

## Complexity

- steps_per_round: designed 13, built 12, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 17, built 35, limit 20 (built: 80)
- hidden_elements: designed 1, built 10, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: scores, wrong counts and round all start at 0
- FAIL: Scores carry into a new leg (round 5 starts leg 2, score stays) | rule R2 is broken: Scores start at 0 and carry across legs.; seat 1 score: expected 3, got 2; seat 1 wrong_count: expected 1, got 2; seat 2 score: expected 2, got 1; seat 2 wrong_count: expected 0, got 1
- pass: Full match with nobody guessing lasts 12 rounds and ends in a shared win
- FAIL: Codes are written in round 1; a correct guess in leg-round 1 scores 4 | rule R3 is broken: When leg-round is 1 (rounds 1, 5, 9), both players secretly and simultaneously write a code.; seat 1 score: expected 4, got -1; seat 1 wrong_count: expected 0, got 1; seat 2 score: expected 0, got -1; seat 2 wrong_count: expected 0, got 1; Ada: the rule for '258' was never matched (the game never put that option to this seat)
- FAIL: Code entry 852 is stored sorted as 258, so a guess of 258 is correct | rule R4 is broken: When a code entry has three different digits in any order (e.g. 8,2,5), then it is sorted ascending and stored as code 258.; seat 1 score: expected 4, got -1; seat 1 wrong_count: expected 0, got 1; seat 2 score: expected 0, got -1; seat 2 wrong_count: expected 0, got 1; Ada: the rule for '258' was never matched (the game never put that option to this seat)
- FAIL: Repeated-digit code entry becomes 0-1-2, so a guess of 012 is correct | rule R5 is broken: When a code entry is invalid (repeated digits, wrong count, non-digits, blank), then the code becomes 0-1-2 (code = 12).; seat 1 score: expected 4, got -1; seat 1 wrong_count: expected 0, got 1; Ada: the rule for '012' was never matched (the game never put that option to this seat)
- FAIL: New leg resets solved and guesses, so a previously solved seat can score again in round 5 | rule R6 is broken: When a leg starts, each player's guesses_left is set to 2, solved to 0 and used_mask to 0.; seat 1 score: expected 7, got 2; seat 1 wrong_count: expected 0, got 1; seat 2 score: expected 0, got -1; seat 2 wrong_count: expected 0, got 1; Ada: the rule for '369' was never matched (the game never put that option to this seat)
- pass: A card already used this leg is not offered again
- pass: Unscripted card choice: used card 1 not offered, remaining cards offered, no score change
- pass: Asking card 1 SUM is allowed and costs nothing (answer not observable)
- pass: Asking card 2 EVENS is allowed and costs nothing (answer not observable)
- pass: Asking card 3 RANGE is allowed and costs nothing (answer not observable)
- pass: Asking card 4 HIGH is allowed and costs nothing (answer not observable)
- pass: Asking card 5 STEPS is allowed and costs nothing (answer not observable)
- pass: Asking card 6 THREES is allowed and costs nothing (answer not observable)
- pass: Both seats ask a card in the same round; asking alone changes no score
- pass: Guess 852 is sorted to 258 and matches in leg-round 3 for 2 points
- pass: A seat that already solved the leg gets no further score change
- pass: Last guess leaves none: one wrong guess costs 1, a later attempt costs nothing more
- pass: A correct guess in leg-round 4 scores 1
- pass: A wrong guess costs 1 point and adds 1 wrong guess
- pass: Simultaneous guesses: one correct (+3 in leg-round 2), one wrong (-1)
- pass: After the opponent solved, the other seat still asks and can score (+2 in leg-round 3)
- pass: Leg-round 4 reveal leaves scores unchanged and the round reaches 4
- pass: Match ends after round 12: higher score wins
- pass: Match end tie on score: fewer wrong guesses wins
- pass: Match end with equal score and equal wrong guesses is a shared win

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `tell` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seats 1 and 2': 4, 'seat 2': 10, 'seat 1': 6}, 45-53 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 47.7 decisions, prompts of 389 characters on average (longest 546)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seats 1 and 2': 12, 'seat 2': 25, 'seat 1': 23}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 60, lost 0, drew 0
- always `last@seat1`: won 0, lost 45, drew 15
- always `last@seat2`: won 0, lost 42, drew 18

## Triage (whose problem each failure was)

- round 1: fix_game: The rules explicitly accept a code or guess written as three different digits in any order, sorted afterwards. The game instead offers only a short list of pre-sorted codes, and that list (guess_offer) is filtered down to codes matching the revealed SUM answer, so valid guesses such as 5,8,2 or 8,5,2 become passes and score nothing. The round counter also jumps from 0 to 2 in round 1, so the round and leg-round bookkeeping is off.
- round 1: fix_game: The failures differ from attempt to attempt and are file bugs. The latest one shows the per-player `code` attribute is never written, so every guess is compared against an unset code and `solved` can never become 1.
- round 1: fix_tests: The rules say a guess from a player with 0 guesses left counts as a pass, so the outcome is the same whether the game polls that seat or skips it. The test failed only because it required a 'pass' option to be offered to Ada, who by the rule under test cannot act; it also leans on the internal guesses_left counter.
- round 1: fix_game: The game takes the leg-start code as free text, while the guess is a numeric entry. The tests' code choices (147, 258) were therefore never offered at the code step and were played as guesses instead: the codes defaulted to 0-1-2, both guesses were wrong, and each seat lost a point. The rules and tests are consistent; the game's code-entry step is the problem.

## Choices the rules did not make

- Exactly 2 players: The designer fixed the table at 2. It is a head-to-head deduction duel in which each player reads one opponent's code. With 3 or more there is no single opponent to question.
- No talk step: The source has no talk. With two rivals racing to deduce, words would add nothing the rules use.
- Codes are visible to their owner (ally): The source says only the engine knows the codes. The owner wrote their own code, and a player attribute cannot be fully hidden, so the opponent simply never sees it.
- Tie-break expression score*100 - wrong_count: wrong_count is at most 6, so the score always dominates and fewer wrong guesses breaks ties. Players who are equal on both share the win, which is the draw.
- guesses_left, solved, used_mask, ask, answer and guess made public: The rules announce each ask, answer, guess and result to both players, so this state is common knowledge.
- Strategy at the table: A thoughtful player picks cards that split the remaining codes best and weighs guessing early for more points against the 1-point penalty and the limit of 2 guesses.

## Simplifications

- Opponent's code is referenced inside a player's update: The engine has no direct player-attribute operand. With exactly 2 seats, 'opponent' is the other seat, and a table-mirror workaround may be used for the comparison.
- Steps 1 and 6 run every round but act only when their leg-round condition holds: The step list is flat; the per-step `when` conditions express 'leg-round 1 only' and 'leg-round 4 only'.
