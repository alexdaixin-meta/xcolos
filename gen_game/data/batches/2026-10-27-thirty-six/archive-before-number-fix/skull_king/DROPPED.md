# Dropped: too complex

it could not be built to behave as designed: attempt 1: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 31 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 0 in `play_a_card`, picked it, and was asked again without it (round 1): the first offe

## The last variation tried

Skull King: Blind Broadsides: A short Skull King for 3 to 4 players played over 10 rounds of 3 cards. Players bid their exact trick count after seeing 3 revealed spare cards. Each trick is played by everyone revealing a card at the same moment. Any exact bid scores the same 30 points, so the game is about predicting and timing, not about being dealt the Skull King.

## What was tried

- round 1: behavior problem; triage said fix_tests: The failing assertions check `deck` and `hand`, which are the coder's own bookkeeping and not part of the interface. The deck is legitimately refilled to 18 for
- round 1: behavior problem; triage said fix_game: The trace shows only 12 moves in round 1. That is exactly three simultaneous card plays of 4 seats, so the game never polls a bid: `bid` stays at its starting 0
- round 1: behavior problem; triage said fix_game: The tests correctly expect each player to be offered the bids 0, 1, 2 and 3 and to have the chosen value recorded in `bid`. In the game file, the bid step never
- round 2: behavior problem; triage said fix_tests: The R6 trace shows the game working as the rules say. The deck is refilled to 18 and 3 cards are dealt to each seat. A bid poll offering 0–3 stores the bids (al
- round 2: behavior problem; triage said fix_game: The bid poll did not offer every seat the options 0 to 3. Seat 1's rule matched, but seats 2 and 3 were never offered option 3 and fell back to the default 0, s
- round 2: behavior problem; triage said fix_game: The rules say the bid poll offers exactly 0, 1, 2 and 3, and the tests rightly answer 3 whenever that option is offered. The game never offered 3 to any seat, s
- design 1: the critic found it not sound (playable, reasoning_over_luck)
- round 3: build problem; triage said revise_rules: The same failure has repeated on attempts 2, 3 and 4: `bonus` (and the coder's `capture` helper) never changes in random matches, even though the coder changed 

To bring the game back, clear `dropped` in its inventory record.
