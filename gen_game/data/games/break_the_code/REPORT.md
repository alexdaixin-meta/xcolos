# break_the_code: ready for review

Built from the variation **Break the Code: Duel of Two Tiles** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- A wrong guess costs no points and gives the guessed code's owner nothing. Its only cost is the turn, and it still returns a little information (whether the guess shares a tile with the code). (fixes: P1): Guessing must never be self-destructive. Random play then no longer feeds points to passive players, and an informed early guess becomes a real option.
- Points come only from correct guesses: 7 minus the turn number within the leg (6 down to 1). Nothing is scored for an unsolved leg. (fixes: P2): Passivity scores zero, so an always-ask policy loses to anyone who ever guesses right. Guessing earlier pays more, so committing under uncertainty is rewarded.
- The code shrinks to two tiles valued 0-5, sorted low-high (21 possible codes). There are five fixed coarse questions with three possible answers each, and a leg lasts 6 turns. (fixes: P3): A code can now be pinned down in about three good questions, so deduction decides the leg. Each answer has only three values, so one cannot solve a code in two questions and guessing at turn 3 versus turn 4 is a real gamble.
- Each player chooses their own secret code at the start of every leg instead of having it dealt. (fixes: P4): This adds opponent modelling. Setters try to pick codes that stay ambiguous under the questions, and guessers can exploit an opponent's habits over four legs. It also removes deal luck and the need for random draws.
- Both players act simultaneously each turn, using the same fixed menu of questions. Answers are announced publicly. Draws and discards are removed. (fixes: P5): Simultaneous play removes the seat advantage. A fixed menu keeps the step count and attributes within the platform's limits.
- A wrong guess reveals whether 0 or 1 of the guessed tiles appear in the code. (fixes: P6): A guess becomes a weak question as well as a gamble. Choosing between a sharp question and a rewarding but risky guess is then a real decision.
- The winner is the higher total after 4 legs. If totals are tied, the player who solved more legs wins; if that is also tied, the match is a draw. (fixes: P1): The winner rule is simple arithmetic. The only way to gain on the opponent is to solve faster, so risk-free passivity cannot win.

Objective: After 4 legs, the player with the higher total score wins. If totals are equal, the player who solved more legs wins. If that is also equal, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. The two seats are fully symmetric. Codes are chosen at the same moment, actions are chosen at the same moment, and both players see the same announcements, so neither seat gains from move order or information.

Code partitions over the 21 codes, from my enumeration:
| Question | Answer counts |
|---
- playable: pass. **Completeness.** Every answer is a defined function of the opponent's code: sum bands cover 0-10, odd/big/edge counts are 0-2, and the gap bands cover every value. The wrong-guess feedback is well defined. Because codes are sorted, a wrong guess can match at most 1 tile, so the stated 0/1 holds: gu
- reasoning_over_luck: pass. **Deduction drives the score.** An optimal adaptive tree (questions, plus guesses used as probes) solves by about turn 4 for about 3-4 points per leg, roughly 12-16 per match. A poor deducer who repeats questions or ignores the 0/1 feedback solves on turn 5-6 or not at all, roughly 4-8 per match. Si

## Complexity

- steps_per_round: designed 11, built 11, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 15, built 38, limit 20 (built: 80)
- hidden_elements: designed 1, built 8, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Both scores start at 0 and stay 0 after a turn of questions; leg 1 goes on to turn 2
- pass: Codes chosen on turn 1 are used to answer questions
- pass: Code chosen on turn 1 is kept on turn 2
- pass: Each unsolved player is offered the five questions and guesses
- pass: Sum: 2-5 gives HIGH, 0-1 gives LOW
- pass: Odd: 1-3 gives 2, 0-4 gives 0
- pass: Gap: 2-4 gives APART, 3-3 gives PAIR
- pass: Big: 2-3 gives 1, 4-5 gives 2
- pass: Edge: 0-5 gives 2, 0-0 gives 2
- pass: Repeating odd in the same leg gives the same answer
- pass: Correct guess on turn 3 scores 4
- pass: Correct guess adds a solved leg and the solver sits out the next turn
- pass: Wrong guess scores 0 and costs nothing
- pass: A solved player is not asked and scores nothing; the other keeps playing
- pass: Both actions and their truthful answers are reported
- pass: After turn 6 the next leg starts and solved is reset
- pass: Match ends after turn 6 of leg 4; higher score wins
- pass: Equal scores: more legs solved wins
- pass: Equal scores and legs solved: shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 12, 'seat 2': 5, 'seats 1 and 2': 3}, 42-56 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 49.7 decisions, prompts of 259 characters on average (longest 281)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 26, 'seat 2': 20, 'seats 1 and 2': 14}
- always `first@seat1`: won 0, lost 36, drew 24
- always `first@seat2`: won 0, lost 38, drew 22
- always `last@seat1`: won 9, lost 31, drew 20
- always `last@seat2`: won 10, lost 33, drew 17

## Choices the rules did not make

- 2 players (min 2, max 2, suggested 2): The designer set 2. Each player cracks the one opponent's code, and every answer is computed from that opponent's code, so a third seat would have no defined target. The strategy is to pick questions that split the remaining codes well, to guess when the expected value of an early guess beats one more question, and to choose codes that are hard to narrow down.
- No talk step: The source has no talk, and in a two-player duel talk would only add words that could be bluffs about one's own code; the rules are kept as written.
- The code is chosen from a list of the 21 valid codes: This makes an invalid code (low > high) impossible to enter with a single answer, and it matches the source's count of 21.
- A guess is one of 26 action options: Asking the action and the guess in one poll avoids a separate follow-up question that only guessers would get.
- Turns still run after both players have solved a leg: The source always plays 6 turns per leg. With nobody unsolved, a turn simply asks no one and scores nothing.
- Tie-break expressed as score * 10 + legs_solved: legs_solved is at most 4, so a weight of 10 keeps score first and legs solved second. A full tie becomes a shared win, which is the source's draw.

## Simplifications

- Each code is mirrored into hidden table attributes (seat1_code_low, seat1_code_high, seat2_code_low, seat2_code_high): The engine has no operand for another player's attribute, and answers must be computed from the opponent's code (player_attribute_compare workaround).
- Ranking by a single arithmetic expression, with the draw as a shared top value: The engine ranks by one expression and players level at the top share the win, which reproduces the source's draw.
