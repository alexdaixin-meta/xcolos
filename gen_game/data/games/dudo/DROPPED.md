# Dropped: too simple

no design got past the critic in 3 rounds; still failing balanced: The step structure gives the responder a built-in per-round edge, and the opener's step-4 raise is almost never right.

STEP 5 (responder, facing the opener's raise b3 = (q,f)). The responder wins if b3 is false (call Dudo) OR if some highe

## The last variation tried

Four-Bid Dudo: Two-player Dudo with wild ones, a four-action cap on bidding each round, an alternating opener and elimination at 0 dice. When the current bid is the maximum (T sixes), the player to act must call Dudo.

## What was tried

- design 1: the critic found it not sound (balanced, reasoning_over_luck)
- round 1: behavior problem; triage said fix_tests: With T = 9 the opening quantity may be anything from 2 to 9, so offering 7 on the quantity prompt is correct. The test treats 7 as forbidden, apparently meaning
- round 1: design problem; triage said revise_rules: The game file works as specified, but one fixed choice dominates. Always taking the first option wins about 90% of decided matches from either seat. Always taki
- design 1: the critic found it not sound (playable)
- round 2: behavior problem; triage said fix_tests: The game asks the opener for the face (options 2 to 6) and then the quantity as two separate prompts. Every 'offered but must not be' failure (2 and 6 at T=9, 5
- round 2: design problem; triage said revise_rules: The game was built as specified, so the failures come from the design. Mindless policies decide the outcome: always taking the first option wins 92–97% of decid
- design 1: the critic found it not sound (balanced)
- design 2: the critic found it not sound (playable)
- design 3: the critic found it not sound (balanced)

To bring the game back, clear `dropped` in its inventory record.
