# Dropped: too complex

it could not be built to behave as designed: scenario `Countess with Prince must be discarded` failed: rule R6 is broken: When the active player holds rank 7 together with rank 5 or rank 6, then discard_choice = 7.; Ada: the rule for 5 was never matched (the game never put that option to this seat) (after 3 variation(s))

## The last variation tried

Love Letter Duel: Long Courtship: A two-player Love Letter played over exactly 40 turns. Each hand sets aside 1 hidden and 5 face-up cards, any hand still running at turn 40 is settled by showdown, and the player with more tokens wins, with ties broken by total ranks discarded across the game.

## What was tried

- design 1: the critic found it not sound (playable, reasoning_over_luck)
- design 2: the critic found it not sound (balanced, playable, reasoning_over_luck)
- round 1: build problem; triage said fix_game: Every failure is a mistake in the file, not in the rules. The prompts use a placeholder ({hand}) that the step cannot fill, bookkeeping fields are visible to pl
- round 1: behavior problem; triage said fix_game: The rules are expressible on the platform, but the game does not put the expected options to the active player. In R8 seat 1 discarded a Guard and was never off
- round 1: build problem; triage said fix_game: Each attempt failed on a different coder-side slip: an unfillable {hand} placeholder in prompts, bookkeeping attributes left visible, and attributes that no ste
- design 1: the critic found it not sound (playable, reasoning_over_luck)
- design 2: the critic found it not sound (playable, reasoning_over_luck)
- round 2: behavior problem; triage said fix_tests: The failures come from `options_include` rules that ask for options the rules themselves exclude or that the given state cannot produce. The Countess test requi
- round 2: behavior problem; triage said fix_game: The Guard guess step does not offer the ranks 2 to 8. The tests never saw 2, 3, 5 or 8 offered, and a correct guess of 5 did not eliminate the opponent. On a Co
- round 2: build problem; triage said fix_game: Both recurring failures are mistakes in the game file, not problems with the rules. A short announcement ('Miss' / 'Miss.') is used without being declared in th
- design 1: the critic found it not sound (reasoning_over_luck)
- round 3: behavior problem; triage said fix_game: The rules are clear and the platform can express them, but the game does not put the right options to the active player. The Guard guess is never offered as the
- round 3: behavior problem; triage said fix_game: The match crashed with a CalcError when it drew from an empty deck list, which is a bug in the file. A new hand must start from all 16 cards no matter what stat
- round 3: behavior problem; triage said fix_game: The rules are sound and the platform can express them, but the game file does not offer the choices the rules require. In the trace the Guard guess was recorded

To bring the game back, clear `dropped` in its inventory record.
