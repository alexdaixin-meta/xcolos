# Dropped: too complex

it could not be built to behave as designed: scenario `Hand 1 even round: seat 2 acts, seat 1 does not` failed: rule R5 is broken: In hand 1, Seat 1 acts on odd rounds and Seat 2 on even rounds. In hand 2 (rounds 21-40), Seat 2 acts on odd rounds and Seat 1 on even rounds.; Ada: the rule for 'PLAY slot 1 (R6)' was never matched (the game never put that option to this seat); Ada: the rule for 'draw pile' was n (after 3 variation(s))

## The last variation tried

Lost Cities: Embargo: A two-player Lost Cities with 3 colours over two mirrored hands of 20 turns. Players build ascending colour columns, can discard freely to dump or deny, and each secretly embargoes one colour of the opponent, which halves that column's score.

## What was tried

- round 1: build problem; triage said revise_rules: Four of five attempts failed on the same check. The interface requires the public table attributes discard_red/blue/green/yellow to start as '' to mean 'no card
- round 2: behavior problem; triage said fix_game: The tests follow the rules, but the game's setup and draw options are wrong. The trace shows the setup rebuilding the full 33-card deck and dealing again on top
- round 2: behavior problem; triage said fix_game: The rules say every draw is a choice the player answers: 'DECK' or the name of an eligible card in discard_tops. The game skips that choice whenever only one op
- round 2: design problem; triage said revise_rules: The game is built correctly, but fixed one-option policies beat random play 85-95% of the time from either seat. The likely cause is the scoring: any expedition
- design 1: the critic found it not sound (reasoning_over_luck)
- round 3: behavior problem; triage said fix_game: Both turn-order scenarios fail the same way: the seat the rules say should act (Seat 2 on an even hand-1 round, Seat 1 on an even hand-2 round) is never offered
- round 3: build problem; triage said fix_game: Every failure is a coder-side defect, and none points to the rules or a missing capability. They are: scratch attributes left visible while empty, an unused `po
- round 3: behavior problem; triage said fix_game: The rules state plainly who acts each round, and the platform can express it. Both failing scenarios show the wrong seat being offered the turn on even rounds (

To bring the game back, clear `dropped` in its inventory record.
