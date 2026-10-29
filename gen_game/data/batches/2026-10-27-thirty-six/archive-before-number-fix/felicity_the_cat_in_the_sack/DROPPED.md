# Dropped: too complex

it could not be built to behave as designed: scenario `Sack order starts at start_seat 3 and wraps, so seat 3 wins a tie with seat 1` failed: rule R5 is broken: sack_owners lists the seats from start_seat ascending and wrapping (start_seat 3 of 4 gives [3,4,1,2]), and sack_cards holds the played cards in that order.; seat 1 mice: expected 18, got 15; seat 1 score: expected 18, got 15; seat 2 mice: expected 17, got 15; seat 2 score: expect (after 3 variation(s))

## The last variation tried

Cat in the Sack: Two Peeks: 3-5 players each secretly add a card to a sack every round. After the first card is shown, everyone bids at once, and passers take 2 mice. If two or more bid, a second card is shown and those still in bid again, with stage-2 passers taking 3 mice. The winner pays and takes the cats, and dogs may remove one cat. After 9 rounds, cats plus mice decide the winner.

## What was tried

- design 1: the critic found it not sound (playable)
- round 1: behavior problem; triage said fix_game: In the bidding scenarios the scripted bids were never offered to the players. Seat 1's bid of 1 and Blaise's bid of 3 were never put to them, so every stage-1 p
- round 1: build problem; triage said fix_game: Each failure is a fixable coding slip, not a flaw in the rules or a missing capability. The attempts hit an unfilled {mice} placeholder, private bookkeeping fie
- round 1: behavior problem; triage said fix_game: In several scenarios a lone legal bid of 1 (or another legal bid) is treated as a pass. Seat 1 ends with 17 mice (15 + the 2-mouse pass reward) and 0 cat points
- round 2: behavior problem; triage said fix_game: Every failing scenario has the same cause: the stage-1 bid poll never offers the numbers the rules require. Seats were never offered 0, 2, 4, 5 or 6, so everyon
- round 2: behavior problem; triage said fix_game: The sack held cat_3, cat_8 and small_dog. Under R10 a lone small dog with no negative cat removes the lowest positive cat, so the sack is worth 8, but the game 
- round 2: behavior problem; triage said fix_game: In every failing scenario the stage-1 bid poll never offered the numbers 0 to the player's mice: seat 1 was never offered 0 or 5, and the rules for 4 and 6 were
- round 3: behavior problem; triage said fix_game: Every failure traces to the stage-1 bidding poll. The tests report that seats were never offered 0, 3 or 15, so the scripted bids could not be made. All bids ca
- round 3: behavior problem; triage said fix_game: The rules are coherent and the platform can express them: they use simultaneous numeric polls, list operations and conditional updates. The failures come from t
- round 3: behavior problem; triage said fix_game: The rules are sound and the platform can express them, but the game file does not implement them. In the trace the stage-1 poll never offers the range 0..mice, 

To bring the game back, clear `dropped` in its inventory record.
