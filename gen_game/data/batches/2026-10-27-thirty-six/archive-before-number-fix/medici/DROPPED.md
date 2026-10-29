# Dropped: too complex

it could not be built to behave as designed: scenario `The revealed top 3 cards form a lot of 3, and the winner loads exactly those` failed: rule R5 is broken: When a round's reveal happens, then the top 3 deck cards are shown to everyone.; seat 1 florins: expected 35, got 40; seat 1 ship_value: expected 7, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat) (after 3 variation(s))

## The last variation tried

Medici: Sealed Lots: A 3-6 player sealed-bid auction over 3 days. The active player picks a lot of 1-3 revealed commodity cards, and everyone bids secretly at once, with ties discarding the lot. Ships of 5 slots score daily for value. Cumulative goods counts score daily for majorities. A secret favoured good pays at the end.

## What was tried

- round 1: behavior problem; triage said fix_game: The tests follow the rules. In all four failing scenarios the active seat was never offered the lot-size choice that rule R4 gives it, or was offered only part 
- round 1: behavior problem; triage said fix_game: The trace shows the game moves `round` from 1 to 2 and `active_seat` from 1 to 2 before round 1 is played, so seat 2 chooses the lot size in round 1. The rules 
- round 1: behavior problem; triage said fix_game: The tests follow the rules. In R2 the 58-florin result checks out: 40, plus 3 from each of the 4 split majorities, plus 6 for favoured cards, gives 58008. The t
- design 1: the critic found it not sound (playable)
- round 2: behavior problem; triage said fix_game: The trace shows two bugs in the game file. The deck is built as only three copies of 'Spice-3' instead of the 48-card deck. The round counter also advances from
- round 2: behavior problem; triage said fix_game: The trace shows clear bugs in the game file. The deck is built as only three 'Spice-3' cards instead of the 48-card deck. The round counter moves 0→1→2 inside t
- round 2: behavior problem; triage said fix_game: The trace shows the game file breaking the rules. The deck is built as only three copies of 'Spice-3' instead of 48 cards, and the round counter goes 0→1→2 with
- design 1: the critic found it not sound (playable)
- design 2: the critic found it not sound (playable)
- round 3: behavior problem; triage said fix_game: The trace shows the game's own errors. In round 1 the table round went 0 -> 1 and then 1 -> 2 before any choice, so active_seat became 2 instead of 1, and seat 
- round 3: behavior problem; triage said fix_game: The trace shows the file is wrong, not the tests. In the first round `round` goes 0→1 and then 1→2, so it is advanced twice. `active_seat` stays 0 and then beco
- round 3: behavior problem; triage said fix_game: The trace shows the game file is wrong in two places. Round goes 0 -> 1 -> 2 before the lot choice, so active_seat is 2 in what should be round 1 (seat 2 chose 

To bring the game back, clear `dropped` in its inventory record.
