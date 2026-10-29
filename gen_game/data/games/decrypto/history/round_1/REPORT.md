# decrypto: needs review

Built from the variation **Decrypto Duel (Paired Rounds)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Group rounds into pairs (rounds 1-2, 3-4, ... 15-16) in which each team encrypts once. Run the end check only after the second round of each pair. (fixes: Seat edge: the end check ran after every round while Team A always encrypted first. Equal-pace failure races therefore went against A, giving B about a 7-point advantage.): Both teams then have the same number of encryptions and interception chances before any win or loss is checked. This restores the original's same-round symmetry.
- Alternate which team encrypts first in a pair: Team A in odd pairs, Team B in even pairs. (fixes: Second-mover information edge: within any fixed pairing, the team that encrypts second sees the other team's result first and can adjust its risk.): Each team is the second mover equally often, so neither team gets the information edge more often.
- Replace the Interceptor rule with fixed per-pair roles. In each pair, each team has one Encryptor and one Guesser. The Guesser decodes their own team's code and intercepts the other team's. Odd pairs: A1 and B1 encrypt. Even pairs: A2 and B2 encrypt. A full table is given. (fixes: Ambiguous roles: the Interceptor definition and the Interceptor list disagreed in rounds 5-8 and 13-16.): This gives one simple rule, stated both as a principle and as a table that agree. Every player has a role in every pair.
- The announcement in rounds 1-2 names the Encryptor and Decoder only, and states that there is no interception. (fixes: Minor: the round announcement named Interceptors in rounds 1-2, where interception does not happen.): This removes the contradiction between the announcement and the interception rule.
- Define that a team 'triggers' when it has 2 or more Interceptions, or when the other team has 2 or more Miscommunications. If exactly one team triggers at a pair check, it wins. If both trigger, the team with the higher Interceptions minus Miscommunications wins, and equal values are a draw. (fixes: The rules claimed that win conditions cannot conflict. Once checks are done per pair this claim is false, and no rule covered both teams triggering a win together.): This handles simultaneous triggers arithmetically and removes the false claim.

Objective: The winner is decided only at the end of an even-numbered round. A team triggers if it holds 2 or more Interceptions or if the opponent holds 2 or more Miscommunications. If exactly one team triggers, it wins. If both trigger, or if neither has triggered by the end of round 16, each team's value is its Interceptions minus its Miscommunications: the higher value wins and equal values are a draw. Both members of a team share its result.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Thoughtless policies, judged by the WINNER RULE.
(1) Decoder always submits 1-2-3, or any fixed code. P(correct) = 1/24, so P(Miscommunication) is about 0.958 per own encrypt. The team holds 2 Miscommunications after its first two encrypts in about 92% of games, so the opponent triggers by the end o
- playable: pass. Rules cover every case:
- invalid clue set: code revealed, +1 Miscommunication, clues not added to history, jump to the end check;
- no interception in rounds 1-2;
- both teams trigger: comparison rule;
- neither triggers by round 16: comparison rule.
A guess with repeated digits or a non-matching g
- reasoning_over_luck: pass. Chance sources:
- the keyword deal: some sets are easier to clue, which is symmetric in expectation;
- the code draw: by itself it decides nothing, because the Decoder knows the keywords;
- blind interception: about 4% for 2 or more lucky hits in 7 attempts.
I estimate chance accounts for roughly 15

## Complexity

- steps_per_round: designed 10, built 17, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 16, built 39, limit 20 (built: 80)
- hidden_elements: designed 3, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup deals 4 keywords to each seat and removes 8 words from the 120-word list
- pass: All four token counts, standings and round number start at 0
- pass: Team A encrypts in round 1 and Team B in round 2: invalid clues give each team one Miscommunication, and the game continues
- pass: Round 4 (even pair, Team A encrypts): Decoder seat 1 and Interceptor seat 3 guess; seats 2 and 4 are not asked
- pass: Round 5 (odd pair, Team A encrypts): Decoder seat 2 and Interceptor seat 4 guess; seats 1 and 3 are not asked
- pass: Round 3: Decoder seat 3 and Interceptor seat 1 are asked to guess; Encryptor seat 4 and seat 2 are not
- pass: Round 1 with valid clues: only Decoder seat 2 guesses, there is no Interceptor and no team gains an Interception
- pass: Guess options are the 24 ordered codes of distinct digits 1-4 (the code drawn is chance, so only the option set is checked)
- pass: The Encryptor (seat 1 in round 1) writes the clues and is not asked to guess
- pass: Invalid clue set in round 3 (Team B encrypts): B gains 1 Miscommunication, nobody guesses, no Interception and no history
- pass: Valid clue set: the guess step is reached and the Decoder is asked
- pass: Round 3 valid clues: both Decoder seat 3 and Interceptor seat 1 are polled in the same round
- pass: The Decoder's guess only affects the encrypting team's Miscommunications (whether it is right is chance): round 1 Team A encrypts, B's counts stay 0
- pass: An Interception only credits the Interceptor's team (whether it hits is chance): round 3 Team B encrypts, B gains no Interception and A no Miscommunication
- pass: Valid clues in round 1 add three clues to Team A's history and none to Team B's
- pass: After odd round 3 play continues even though Team A holds 2 Interceptions; standings are not recomputed
- pass: Team A triggers with 2 Interceptions at the end of round 2 and wins
- pass: Team B's second Miscommunication in round 2 makes Team A the only team to trigger: A wins
- pass: Both teams trigger at round 2: A has the better Interceptions minus Miscommunications (-1 against -2) and wins
- pass: Both teams trigger at round 2 with equal Interceptions minus Miscommunications: all four share the win
- pass: No trigger by round 16: A (1-1=0) beats B (0-1=-1) on Interceptions minus Miscommunications
- pass: No trigger by round 16 with equal values: all four share the win
- pass: Both members of Team B share its win when Team A has 2 Miscommunications at the end of round 2 (Team B encrypts in round 2)

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `sync` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seats 1, 2, 3 and 4': 20}, 4-4 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 4.0 decisions, prompts of 353 characters on average (longest 353)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- every random match ended 'seats 1, 2, 3 and 4': choices do not change the result
- random seats: {'seats 1, 2, 3 and 4': 60}
- always `first@seat1`: won 0, lost 0, drew 60
- always `first@seat2`: won 0, lost 0, drew 60
- always `last@seat1`: won 0, lost 0, drew 60
- always `last@seat2`: won 0, lost 0, drew 60

## Triage (whose problem each failure was)

- round 1: fix_game: The game over-counts Miscommunications: in the shared-standing scenario each team ended one token too many (b_miscommunications 2 instead of 1, every standing 1 lower than expected). This fits an invalid clue set being charged twice, once at the referee check and again at decoder scoring, when the rules skip straight to the end check. The clue history also stores a valid clue set as one entry, while the rules add each clue separately under the keyword it clued.
- round 1: fix_game: With no moves played, every clue set should be invalid. Under step 4 an invalid set gives exactly 1 Miscommunication and skips straight to step 8, but the game charged 2 Miscommunications (b_miscommunications 2 instead of 1, and every standing one lower). That looks like a second penalty from the failed Decoder guess, a step the rules skip when the clue set is invalid.
- round 1: fix_tests: Under random play, interceptions almost never happen. A random Decoder misses about 23 times in 24, so both teams usually reach 2 Miscommunications by round 4 and the game ends there; that leaves only rounds 3-4 for interception, each a 1-in-24 exact guess. The check that `a_interceptions`/`b_interceptions` never changed in 3 random matches is chance deciding, not a missing update; it repeated across attempts even after the coder reworked the scoring step.
- round 1: revise_rules: The game is built as specified, yet every random match ends in a four-way draw. The design is symmetric: both teams encrypt once per pair, and a near-random Decoder misses 23 times in 24, so both teams reach 2 Miscommunications together at the end of pair 2. Both trigger, the comparison is usually -2 vs -2, and choices almost never change the result.

## Choices the rules did not make

- 4 players, min 4, max 4, suggested 4: The designer fixed two teams of two, one Encryptor and one Guesser each, and the role table names exactly four seats. Fewer seats would break a team, and more have no role.
- Seat mapping: seat 1 = A1, seat 2 = A2, seat 3 = B1, seat 4 = B2: This gives a fixed arithmetic for roles from round_number and pair parity that reproduces the source's role table.
- One engine round equals one game round (16 at most): This lets the end check run after every even round, using a `when` condition on round_number parity.
- Ranking expression: (own trigger - other trigger) * 1000 + Interceptions - Miscommunications: A sole trigger outranks any comparison value (which lies within -16 to 16), while a double trigger or no trigger falls back to the comparison. Equal values share the win, which is the draw.
- The 120-word list's contents are chosen by the implementer: The source names the list's size and kind (common concrete nouns) but not the words.
- No talk phase: The source forbids talk; players communicate only through clues.
- Guesses are chosen from the 24 legal codes: The code space is fixed, so a choice list prevents malformed guesses.

## Simplifications

- The three clues are one text answer separated by ' / ': A single short-text question keeps the clue step to one ask. The referee and the history read the clues in code order.
- Each teammate holds their own copy of the team's keywords as a private player attribute: The engine has no team-visible table attribute, so giving both members the same list gives the same information.
- Clue validity (meaning, no spelling hints, no keyword forms, no repeats) is decided by a referee's true/false ruling: These checks are too complex for arithmetic, which the engine allows to be judged. The tokens that result are still calculated.
