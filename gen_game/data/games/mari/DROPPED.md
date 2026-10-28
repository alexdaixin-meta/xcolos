# Dropped: too complex

it is too large for the platform: the built game has 6 choice steps per round, over the limit of 4 (after 3 variation(s))

## The last variation tried

Mini Mariáš with Hidden Talon: A five-deal, three-player Mariáš. Each deal is freshly shuffled with a 3-card hidden talon. Players bid a contract of 40, 50 or 60 card points, the declarer picks trump, defenders may Flek, and 7 tricks are played under the original must-follow, must-head, must-trump rules.

## What was tried

- design 1: the critic found it not sound (playable)
- round 1: behavior problem; triage said fix_game: The tests match the rules: a trump beats the Ace of the led suit, a player void in the led suit must trump and overtrump, and a player with neither may play any
- round 1: behavior problem; triage said fix_game: Several independent trick-play scenarios fail in the same way: the trick points go to the wrong side, a trump does not beat a led-suit Ace, the trick winner doe
- round 1: build problem; triage said revise_rules: Across five attempts the coder fixed each reported problem, yet the match kept crashing in the card-handling core. The trick-winner calculation failed twice (at
- round 2: behavior problem; triage said fix_game: The rules are sound and the tests read them correctly. The game never offered the flek poll options, so each player's `offer` list stayed empty, every answer de
- round 2: design problem; triage said revise_rules: The game was built as specified, and evaluation shows two design flaws. Each round has five choice steps (bid, flek poll, three cards), over the limit of four. 
- design 1: the critic found it not sound (reasoning_over_luck)
- design 2: the critic found it not sound (playable)
- round 3: design problem; triage said revise_rules: The game was built and behaves as specified, but the design itself fails evaluation. It needs 6 choice steps per round, over the limit of 4. A fixed thoughtless

To bring the game back, clear `dropped` in its inventory record.
