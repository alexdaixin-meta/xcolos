# code_777: needs review

Built from the variation **Code 777: Ask and Guess** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace interrupts with a simultaneous guess poll at the end of every round: each player either guesses their three numbers or passes. (fixes: P1): It is turn-based and removes the reflex advantage; every player gets the same chance to act on the same information.
- A wrong guess costs 1 point, and scores may go negative. Your rack is still replaced after any guess, right or wrong. (fixes: P2): Guessing becomes a calculated risk, so you guess only once your deduction is confident. The always-guess policy now sinks below zero.
- Drop the question deck. The active player picks a question from a fixed menu of six, and names which other player (the respondent) must have the engine answer it from that player's point of view. (fixes: P3): This removes the luck of the question draw and leaves only one chance event per round, the tile replacement. Choosing the question means steering the information toward your own rack. Choosing the respondent means denying information to the leader, because the respondent learns nothing about their own rack from their own answer. Both choices take planning and opponent modelling.
- The engine computes every answer exactly from the tiles. (fixes: P3): Answers are verifiable and cannot be lied about or miscounted.
- The asker's choice of question and respondent is a deliberate strategic act, as described above. (fixes: P4): Every turn becomes a decision about which information to release and to whom.
- Remove colors. Tiles are numbers only, and the menu uses number properties instead (even, high, specific number, rack sum, pairs, missing numbers). (fixes: P5): It keeps state within 20 attributes for 4 players and keeps every question a simple count.
- Cap the game at 10 rounds per player (30 rounds with 3 players, 40 with 4). The first player to 3 points wins. At the cap, the highest score wins. (fixes: P6): This bounds the length. Each seat asks equally often, so asking first is not an edge.

Objective: When the game ends because someone reached 3 points, the player with the most points wins. If two or more players share that top score, the game is a draw. If the round limit is reached instead, the player with the highest score wins, and a tie for the highest score is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. WHO LEARNS WHAT. An answer counts every rack except the respondent's. The active player and every other non-respondent see all of those racks except their own. So each of them can subtract and learn an exact fact about their own rack: a count of evens, highs or k's, or whether their rack sums to 15+
- playable: pass. RULES ARE COMPLETE.
- Tile counts are given: 1 to 7 copies of each number, 28 in all.
- The deal, private views, public discard pile and active-player rotation are defined.
- The respondent must be another player. k is required only for question 3.
- The scoring set-match includes duplicates.
- Resh
- reasoning_over_luck: pass. WHAT THERE IS TO INFER.
- Each player must deduce their hidden rack. They use the known tile distribution (1 to 7 copies of each number), the visible racks of others, the public discard pile and exact engine answers.
- Good play means:
  - choosing the question that best splits one's own remaining c

## Complexity

- steps_per_round: designed 12, built 10, limit 20
- choice_steps_per_round: designed 2, built 3, limit 4
- attributes: designed 19, built 43, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- FAIL: Setup: 3 tiles per rack, deck holds 28 - 9 = 19 (unchanged after a round where everyone passes) | rule R1 is broken: When the game is set up, the deck holds 28 tiles (one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s), each player is dealt 3 tiles into rack, and the deck then holds 28 - 3N.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: Setup with 4 players: deck holds 28 - 12 = 16 (unchanged after a round where everyone passes) | rule R1 is broken: When the game is set up, the deck holds 28 tiles (one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s), each player is dealt 3 tiles into rack, and the deck then holds 28 - 3N.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: Racks are dealt to every seat so they can be shown to the others | rule R2 is broken: When racks are shown, each player sees every other player's rack and never their own.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: At start every score is 0 and discard is empty (still so after a round of passes) | rule R3 is broken: When the game starts, every score is 0 and discard is empty.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: Seat 1 asks in round 1, seat 2 asks in round 2, seat 3 only gets the poll | rule R4 is broken: When round r begins, the active seat is ((r - 1) mod N) + 1, so seat 1 is active in round 1.; seat 1 was never offered 'EVEN', but should have been; seat 2 was never offered 'EVEN', but should have been; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat); Blaise: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: Active seat 1 cannot name itself as respondent | rule R5 is broken: When the active player chooses a respondent, the respondent must be a seat other than the active player.; seat 1 was never offered 'to seat 2', but should have been; seat 1 was never offered 'to seat 3', but should have been; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: NUMBER question offers k from 1 to 7 | rule R6 is broken: When the question is NUMBER, the active player also names k from 1 to 7.; seat 1 was never offered 1, but should have been; seat 1 was never offered 2, but should have been; seat 1 was never offered 3, but should have been; seat 1 was never offered 4, but should have been; seat 1 was never offered 5, but should have been; seat 1 was never offered 6, but should have been; seat 1 was never offered 7, but should have been; Ada: the rule for 'NUMBER' was never matched (the game never put that option to this seat)
- FAIL: Answer excludes the respondent and includes the asker (EVEN: 1 + 3 = 4) | rule R7 is broken: When an answer is computed, it counts only the racks of every seat except the respondent, including the active player's rack.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: EVEN counts tiles showing 2, 4 or 6 (2 + 2 = 4) | rule R8 is broken: When the question is EVEN, the answer is the number of tiles showing 2, 4 or 6 on those racks.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: HIGH counts tiles showing 5, 6 or 7 (3 + 1 = 4) | rule R9 is broken: When the question is HIGH, the answer is the number of tiles showing 5, 6 or 7 on those racks.; game answer: expected 4, got 2; Ada: the rule for 'HIGH' was never matched (the game never put that option to this seat)
- FAIL: NUMBER with k = 7 counts the 7s (2 + 1 = 3) | rule R10 is broken: When the question is NUMBER with k, the answer is the number of tiles equal to k on those racks.; game answer: expected 3, got 2; Ada: the rule for 'NUMBER' was never matched (the game never put that option to this seat); Ada: the rule for 7 was never matched (the game never put that option to this seat)
- FAIL: SUM15 counts racks summing to 15 or more (15 counts, 14 does not) | rule R11 is broken: When the question is SUM15, the answer is the number of those racks whose three tiles sum to 15 or more.; Ada: the rule for 'SUM15' was never matched (the game never put that option to this seat)
- FAIL: PAIR counts racks holding two or more of a number (a triple counts once) | rule R12 is broken: When the question is PAIR, the answer is the number of those racks holding at least two tiles of the same number.; game answer: expected 1, got 2; Ada: the rule for 'PAIR' was never matched (the game never put that option to this seat)
- FAIL: MISSING counts the numbers 1-7 on no counted rack (4, 5, 6, 7 = 4) | rule R13 is broken: When the question is MISSING, the answer is how many of the numbers 1 to 7 appear on none of those racks.; game answer: expected 4, got 2; Ada: the rule for 'MISSING' was never matched (the game never put that option to this seat)
- FAIL: The computed answer is published (HIGH: 1 + 0 = 1) | rule R14 is broken: When an answer is computed, the question, the respondent and the answer are announced to everyone.; game answer: expected 1, got 2; Ada: the rule for 'HIGH' was never matched (the game never put that option to this seat)
- FAIL: Two seats guess correctly in the same poll and both score | rule R15 is broken: When the guess poll runs, all players answer simultaneously, each with PASS or three numbers.; seat 2 score: expected 1, got 0; seat 3 score: expected 1, got 0
- FAIL: Correct guess in any order scores +1 | rule R16 is broken: When a guess matches the player's rack as a multiset of three numbers, the player's score rises by 1.; seat 2 score: expected 1, got 0
- pass: Wrong guess scores -1 and can go negative
- FAIL: PASS keeps score and rack, nothing is discarded | rule R18 is broken: When a player answers PASS, the player's score is unchanged and the rack is kept.; Ada: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- pass: A guesser's rack goes to discard and 3 new tiles come from the deck
- pass: A short deck takes in the whole discard before dealing
- pass: Reaching 3 points ends the game and that seat wins
- FAIL: With 3 players the game ends after round 30; highest score wins | rule R22 is broken: When round 30 (with 3 players) or round 40 (with 4 players) has been played, the game ends.; Cleo: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: With 4 players the game ends after round 40 | rule R22 is broken: When round 30 (with 3 players) or round 40 (with 4 players) has been played, the game ends.; Dara: the rule for 'EVEN' was never matched (the game never put that option to this seat)
- FAIL: A tie at the top is shared by the tied seats | rule R23 is broken: When the game ends, the highest score wins, and a tie for the highest score is a draw shared by the tied players.; Cleo: the rule for 'EVEN' was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seats 1 and 2': 3, 'seat 1': 7, 'seat 2': 9, 'seats 1 and 3': 2, 'seat 3': 10, 'seats 1, 2 and 3': 1, 'seats 1, 2, 3 and 4': 1, 'seats 1 and 4': 1, 'seat 4': 5, 'seats 2 and 4': 1}, 121-213 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 166.2 decisions, prompts of 344 characters on average (longest 486)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seats 1 and 2': 5, 'seat 1': 14, 'seat 2': 17, 'seats 1 and 3': 5, 'seat 3': 14, 'seats 1, 2 and 3': 4, 'seats 2 and 3': 1}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 60, lost 0, drew 0
- always `last@seat1`: won 9, lost 46, drew 5
- always `last@seat2`: won 8, lost 35, drew 17

## Triage (whose problem each failure was)

- round 1: fix_tests: The game legitimately combines the question and the respondent into one choice, offering options like 'EVEN to seat 2', which fits the rule that the active player makes one choice of question plus respondent. The tests look for a bare option named 'EVEN', 'HIGH' or 'NUMBER' that the rules never prescribe, so their rules never matched and the follow-up steps (such as naming k) were never reached.
- round 1: fix_tests: The rules call the active player's question and respondent one choice. The game offers combined options such as 'EVEN to seat 2' and 'EVEN to seat 3', which follows the rules. The tests look for a bare option string 'EVEN', and 'k' values offered as separate options, which this faithful encoding never produces. The NUMBER scenario also expects an exact answer of 2 that depends on which tiles the shuffle deals, so chance decides it, not the rules.
- round 1: fix_tests: The game deals racks and keeps the deck at 28 - 3N: the trace shows 19 tiles in the deck after two all-pass rounds with 3 players, scores at 0 and an empty discard. It offers the active player one combined choice of question and respondent, labelled like 'EVEN to seat 2'. Every failure is the test's rule `options_include: "EVEN"` never matching, because no option is labelled exactly 'EVEN'.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer's suggested size is 3 and the source allows 3 to 4. The minimum is 3 because with 2 players a respondent sees only the asker's rack, so answers reveal it almost directly. The maximum stays at 4, as in the source; more racks per question would make answers too diluted and turns too slow.
- Strategy at the table: A thoughtful player picks questions and respondents whose answers best split the possible racks they could hold, uses the public discard and the tile counts, notes what the questions reveal to opponents, and passes until confident, because a wrong guess costs a point.
- No talk phase: The source explicitly has none; the engine-answered questions are the only shared information.
- Question and respondent combined into one choice, with k asked in a separate step only for NUMBER: It fits the engine's choice-from-a-list answer type while keeping the active player's single decision.
- An unparseable guess is treated as PASS: The source does not cover malformed answers; PASS is the neutral reading.
- When the deck is replenished, the whole discard pile moves into the deck: The source says the discard pile is shuffled in; drawing at random makes an explicit shuffle unnecessary.

## Simplifications

- The guess is free text parsed into three numbers rather than a menu of all 84 multisets: This avoids an oversized option list.
- The two ways the game can end share one ranking (highest score; ties share the win): The source decides the winner the same way for both endings, and the engine treats a shared top as a draw.
