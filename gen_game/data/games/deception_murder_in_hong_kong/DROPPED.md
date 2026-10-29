# Dropped: too simple

no design got past the critic in 3 rounds; still failing balanced, reasoning_over_luck: TAG ARITHMETIC. Each Cause of Death option appears on 8 of the 16 Means: Breathing 3+3+2, Blunt 3+2+3, Bleeding 3+2+3, Chemical 2+3+3. Each Location option appears on 8 of the 16 Clues: Home 3+3+2, Outdoors 3+2+3, Public 3+2+3, Workplace 2+

## The last variation tried

Deception: Tagged Case File: A team hidden-role deduction game for 5-8 players. A silent Scientist gives two exact hints over a public tag table. The table votes on at most 1-2 accusations, so a secret Witness must steer the vote, and a caught Murderer can still win by reading the talk and vote record to find the Witness.

## What was tried

- round 1: build problem; triage said fix_game: Every failure is a mistake in the game file: a prompt uses a `{acc_clue}` placeholder the step cannot fill, and internal or not-yet-set fields are printed empty
- round 1: behavior problem; triage said fix_game: The tests follow the rules: an accuser may name any Clue and any Means word currently on the table. The game never offered seats valid table words such as Glove
- round 1: behavior problem; triage said fix_game: The tests follow the rules, and the game breaks the accusation step. It offered seat 6 'Mask', a word still in clue_deck and not on the table. It never put a Cl
- round 2: build problem; triage said fix_game: Each attempt failed on a different coder-side problem: an unfilled placeholder, then bookkeeping fields shown to players, and now an attribute (`seat_names`) th
- round 2: build problem; triage said revise_rules: The same 'solved / solved_this_round / hunt_target never changed' failure came back in attempts 2 and 4 after the coder had fixed the other problems in between.
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (reasoning_over_luck)
- design 3: the critic found it not sound (balanced, reasoning_over_luck)

To bring the game back, clear `dropped` in its inventory record.
