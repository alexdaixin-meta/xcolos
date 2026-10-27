# decrypto: needs review

Built from the variation **Decrypto: Points Race** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Replace the token race with a fixed 8-round game in which teams earn points every round, and the higher team total wins. (fixes: P1): Every round's guesses now move the score, so totals diverge and results vary with play instead of collapsing into a shared trigger.
- Score guesses position by position. A decode earns 1 point per correctly placed digit plus 1 bonus for the exact code (max 4). An interception earns 1 point per correctly placed digit plus 2 bonus for the exact code (max 5). (fixes: P2): Partial credit rewards better-than-random inference every round. The larger exact-interception bonus makes leaking a whole code costly, which prices the clear-versus-obscure tension.
- Break ties first by total exact interceptions, then by total exact decodes; only then is the game a draw. (fixes: P3): Ties now go to the team that showed more inference, so draws are rare.
- Use only arithmetic clue checks: one word, 2-20 letters, does not contain and is not contained in any of the team's own keywords (ignoring case), and does not repeat any earlier clue by either team. An invalid clue set makes that team's decode score 0 and gives the opponents 3 points. (fixes: P4): The meaning check is removed. Clue legality is computable, and breaking the rules has a fixed, arithmetic cost.
- The Encryptor chooses the team's secret code from the 24 possible codes, instead of drawing a code card. (fixes: P5): This removes the per-round random draws. It also adds a decision: a predictable code pattern (always the first code) is intercepted from the public history, so code choice becomes opponent modelling.
- Make every step simultaneous: both Encryptors choose codes, both write clues, then all four players guess at once. Fix the game at 4 players, two teams of 2, with roles alternating each round. (fixes: P6): This removes the read-first and announce-first order advantage, gives every seat the same position, and makes the length fixed and short.
- In each guess step, each team's Decoder decodes the own team's clues while that team's Encryptor intercepts the opponents' clues. Interceptions score nothing in round 1, as in the original. (fixes: P7): Every player has a reasoning task each round. Separating the two jobs makes the cost of a leaky clue (opponent points) and the value of a clear clue (own points) directly comparable.

Objective: The team with more points after round 8 wins, and both of its players win. If points are tied, the team with more exact interceptions wins. If still tied, the team with more exact decodes wins. If still tied, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Per-round scoring for one team: decode gives 1 per matching position plus a +1 bonus for an exact match (exact = 4). Interception, rounds 2-8, gives 1 per matching position plus +2 for exact (exact = 5). An invalid clue gives the opponent +3. A guess that ignores the clues, against a code spread eve
- playable: pass. The rules are complete. Setup draws 8 keywords from a fixed list of 40. Codes are an explicit list of 24. The role rotation is given. All three choices are simultaneous: code, clues, and the guess poll of all four players. Scoring is pure arithmetic on stored values: positional matches, bonuses, and
- reasoning_over_luck: pass. The only chance element is the setup keyword deal. Codes are chosen, not drawn, and the guesses are reasoned. Estimated chance share of the result is about 10-15%: some keyword sets are easier to clue than others, but both teams face the same 40-word pool.

What decides the result:
- writing clues y

## Complexity

- steps_per_round: designed 14, built 18, limit 20
- choice_steps_per_round: designed 3, built 5, limit 4
- attributes: designed 18, built 54, limit 20 (built: 80)
- hidden_elements: designed 2, built 19, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Seats 1-2 are Red and seats 3-4 are Blue at setup
- pass: Each team gets 4 keywords and 8 nouns leave the word list (draw is random, only counts asserted)
- pass: Each player holds their own team's 4 keywords (draw is random, only counts asserted)
- pass: Teams start with 0 points, 0 exact interceptions and 0 exact decodes
- pass: Odd round: seats 1 and 3 encrypt, seats 2 and 4 decode
- pass: Even round: seats 2 and 4 encrypt, seats 1 and 3 decode
- pass: Encryptors choose among the 24 codes
- pass: Valid clues leave both teams not invalid and the round is recorded
- pass: Red's clues ruled invalid: Red is marked invalid, Blue is not
- pass: Clues are shown, then all players guess; decoders guess correctly
- pass: All four seats are asked to guess one of the 24 codes
- pass: Decode guess 123 against code 132 gains 1 point
- pass: Exact decode gains 4 points and 1 exact decode
- pass: Both teams invalid: no decode points or exact decodes, each team gets only the 3 penalty points
- pass: Round 2: interception 123 against code 132 gains 1, exact interception gains 5
- pass: Round 2: exact interception adds 5 points and 1 exact interception
- pass: Round 1: exact interceptions score nothing
- pass: Blue invalid: Red gains 3 extra points
- pass: After round 1 the history holds one entry and the round advances
- pass: Teammates share score and exact counts
- pass: Game ends after round 8; the team with more points wins
- pass: Tied points: more exact interceptions wins
- pass: Fully tied teams: all four share the result
- pass: A round runs on codes, clues and guesses alone

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seats 3 and 4': 13, 'seats 1 and 2': 5, 'seats 1, 2, 3 and 4': 2}, 64-64 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 64.0 decisions, prompts of 260 characters on average (longest 484)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 3 and 4': 28, 'seats 1 and 2': 27, 'seats 1, 2, 3 and 4': 5}
- always `first@seat1`: won 0, lost 30, drew 30
- always `first@seat2`: won 0, lost 29, drew 31
- always `last@seat1`: won 0, lost 34, drew 26
- always `last@seat2`: won 0, lost 28, drew 32

## Triage (whose problem each failure was)

- round 1: fix_game: The game over-counts Miscommunications: in the shared-standing scenario each team ended one token too many (b_miscommunications 2 instead of 1, every standing 1 lower than expected). This fits an invalid clue set being charged twice, once at the referee check and again at decoder scoring, when the rules skip straight to the end check. The clue history also stores a valid clue set as one entry, while the rules add each clue separately under the keyword it clued.
- round 1: fix_game: With no moves played, every clue set should be invalid. Under step 4 an invalid set gives exactly 1 Miscommunication and skips straight to step 8, but the game charged 2 Miscommunications (b_miscommunications 2 instead of 1, and every standing one lower). That looks like a second penalty from the failed Decoder guess, a step the rules skip when the clue set is invalid.
- round 1: fix_tests: Under random play, interceptions almost never happen. A random Decoder misses about 23 times in 24, so both teams usually reach 2 Miscommunications by round 4 and the game ends there; that leaves only rounds 3-4 for interception, each a 1-in-24 exact guess. The check that `a_interceptions`/`b_interceptions` never changed in 3 random matches is chance deciding, not a missing update; it repeated across attempts even after the coder reworked the scoring step.
- round 1: revise_rules: The game is built as specified, yet every random match ends in a four-way draw. The design is symmetric: both teams encrypt once per pair, and a near-random Decoder misses 23 times in 24, so both teams reach 2 Miscommunications together at the end of pair 2. Both trigger, the comparison is usually -2 vs -2, and choices almost never change the result.
- round 2: revise_rules: The game was built correctly, but the design needs 5 choice steps per round, which exceeds the platform's limit of 4. Each round asks Encryptors for a code, clues and an interception, and asks Decoders for a decode. The other results (thoughtless policies never winning, random seats near even) look healthy, so the problem is the round's length, not balance.

## Choices the rules did not make

- 4 players (min 4, max 4, suggested 4): The designer fixed two teams of two. The game needs an Encryptor and a Decoder on each side, so the minimum is 4. More seats would break the fixed role swap and the team structure, so the maximum is not larger. The strategy is to give clues obvious to a teammate who knows the keywords but opaque to rivals who read the growing history, and to read the rivals' clue patterns to intercept.
- The 40-noun word list: The source says a fixed list of 40 common nouns but does not name them, so a concrete list was chosen.
- No talk step: The source forbids all talk other than the clues.
- Clues are entered as one comma-separated text answer: The engine takes one short text per question, and the three clues belong to one simultaneous step.
- Ranking is score * 10000 + exact_interceptions * 100 + exact_decodes: This encodes the source's tie-break order in one expression. Exact counts never exceed 8, so the weights cannot overlap. A full tie shares the win, which is the source's draw.
- Interception guesses are still asked in round 1: The source has every Encryptor choose an interception every round and only says round 1 interceptions score nothing.

## Simplifications

- True codes are stored as hidden table attributes (red_code, blue_code) rather than on the Encryptor: A player's hidden attribute is visible to the whole team, but the source says no one else, including the Decoder teammate, may see the code.
- Team points are mirrored onto both teammates' score, exact_interceptions and exact_decodes: The ending ranks players, so each player carries the team totals in order to win or lose together.
- Clue validity is ruled by a referee from one sentence: Word, letter-count, substring and history-repeat checks on free text are beyond plain arithmetic. All scoring stays arithmetic.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {code_pick} (in `prompt`: 'Your code is {code_pick}. Write three clues separated by commas: clue 1 for your keyword n'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {code_pick} (in `prompt`: 'Your code is {code_pick}. Write three clues separated by commas: clue 1 for your keyword n'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {code_pick} (in `prompt`: 'Your code is {code_pick}. Write three clues separated by commas: clue 1 for your keyword n'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (clue_text, code_pick, guess, role); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `codes` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
