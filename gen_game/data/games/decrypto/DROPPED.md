# Dropped: too complex

it could not be built to behave as designed: attempt 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (clue_text, code_pick, guess, role); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed (after 3 variation(s))

## The last variation tried

Decrypto Duel: Two teams of two each hold four secret keywords. Each round both Encryptors secretly choose a code and give meaning-only clues, which are revealed at the same time. Every player then guesses at once: Decoders decode their own team's code, and Encryptors try to intercept the other team's. Two Interceptions win, two Miscommunications lose, and the game lasts at most 8 rounds.

## What was tried

- design 1: the critic found it not sound (balanced, playable)
- round 1: behavior problem; triage said fix_game: The game over-counts Miscommunications: in the shared-standing scenario each team ended one token too many (b_miscommunications 2 instead of 1, every standing 1
- round 1: behavior problem; triage said fix_game: With no moves played, every clue set should be invalid. Under step 4 an invalid set gives exactly 1 Miscommunication and skips straight to step 8, but the game 
- round 1: build problem; triage said fix_tests: Under random play, interceptions almost never happen. A random Decoder misses about 23 times in 24, so both teams usually reach 2 Miscommunications by round 4 a
- round 1: design problem; triage said revise_rules: The game is built as specified, yet every random match ends in a four-way draw. The design is symmetric: both teams encrypt once per pair, and a near-random Dec
- round 2: design problem; triage said revise_rules: The game was built correctly, but the design needs 5 choice steps per round, which exceeds the platform's limit of 4. Each round asks Encryptors for a code, clu
- design 1: the critic found it not sound (playable)
- round 3: build problem; triage said revise_rules: Over five attempts the coder has cycled between two failures, and both come from the design. The interface requires public white_clues/black_clues that start as

To bring the game back, clear `dropped` in its inventory record.
