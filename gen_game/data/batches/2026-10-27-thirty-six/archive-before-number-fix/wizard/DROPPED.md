# Dropped: too complex

it could not be built to behave as designed: scenario `First hand: hand_number becomes 1, 18 cards stay in the deck, each hand holds 2 after one trick (cards are random)` failed: rule R1 is broken: When a round starts with trick_in_hand == 1, then hand_number increases by 1, the deck is refilled to 28 cards, every tricks_taken becomes 0, and seats 1, 2 and 3 each receive 3 cards in that order.; Ada: the rule for [0, 1, 2, 3] was never matched (the game never put that option  (after 3 variation(s

## The last variation tried

Pocket Wizard: Three players play 9 hands of 3 tricks with a 28-card deck that includes Wizards and Jesters. At the start of each hand everyone secretly bids how many tricks they will take; the bids are revealed and the tricks are played. Exact bids score big, and the highest total after 27 tricks wins.

## What was tried

- design 1: the critic found it not sound (playable)
- round 1: behavior problem; triage said fix_tests: The game asks for bids as a numeric choice with no option list, and offers only legal cards when a player plays. The tests are built on matching option strings 
- round 1: behavior problem; triage said fix_game: Every failing scenario breaks at the bidding poll. No seat was ever offered the options 0 or 2 that the tests look for, and all bids came out as 0, even though 
- round 1: behavior problem; triage said fix_game: The bidding poll never offered the options 0, 1, 2 and 3 to any seat, so the tests' bid answers never matched. Even the 0 that was sent was overwritten with the
- round 2: behavior problem; triage said fix_game: The rules are clear and the platform can express them; the failures come from the game file. An invalid bid answer was stored as '0' (bid_said '0', bid 0) inste
- round 2: behavior problem; triage said fix_tests: In the failing scenario every seat's recorded bid answer was '0', which is a valid option. Rule 4 says 0 stays 0, so the game was right to store bid 0. The test
- round 2: behavior problem; triage said fix_tests: In both failing scenarios the game did what the rules say. In the bid scenario seat 1's recorded answer was '0', a legal bid that the rules say stays 0, so expe
- round 3: behavior problem; triage said fix_tests: The game matches the rules: after round 1, hand_number is 1, each seat holds 2 cards, the deck holds 18, and the trump card and leader are correct. The scenario
- round 3: behavior problem; triage said fix_tests: The game deals, turns trump, validates the play and awards the Wizard trick exactly as the rules require. The trace shows the bid poll was held in round 1 (r1 s
- round 3: behavior problem; triage said fix_game: Every failing scenario breaks on the same point: the bidding question never offered the options [0, 1, 2, 3], so the scripted bids (for example 2, 3 and 0) were

To bring the game back, clear `dropped` in its inventory record.
