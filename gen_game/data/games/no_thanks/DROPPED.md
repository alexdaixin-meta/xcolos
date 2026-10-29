# Dropped: too simple

it is still degenerate or luck-driven: always taking the last option as seat 1 wins 98% of decided matches against random seats (after 3 variation(s))

## The last variation tried

No Thanks! (Two-Lap): No Thanks! for 3 to 4 players with a 20-card deck. A card that goes twice around the table untaken is burned, and its chips roll onto the next card. Offer order and take effects are stated exactly.

## What was tried

- design 1: the critic found it not sound (balanced, reasoning_over_luck)
- round 1: behavior problem; triage said fix_game: In three scenarios the game never actually put a PAY/TAKE choice to the seats: 'moves played' is empty, yet seat 1 ended up holding card 20 with offer ['TAKE'].
- round 1: behavior problem; triage said fix_game: The test follows rule 5: after a lap where everyone pays, the card stays current and the next round offers it again from the same lead seat. The game never offe
- round 1: behavior problem; triage said fix_game: The test matches the rules: after a full lap of PAYs with lap_count becoming 1, the card stays current and is offered again starting at lead_seat. The game neve
- round 2: behavior problem; triage said fix_tests: The game did what the rules require: seat 1 had 0 chips, could not PAY, and ended up taking the card. Its tableau became [10], it collected the pot (chips 0 -> 
- round 2: behavior problem; triage said fix_game: The rules say TAKE is offered to every seat whenever current_card is not 0. In three separate scenarios the game never offered TAKE to the seat in question, inc
- round 2: behavior problem; triage said fix_game: The rules say TAKE is always offered to each seat while a card is current. In both failing scenarios the game never put TAKE to a seat that the rules say should
- round 3: design problem; triage said revise_rules: The game file works as specified, but one thoughtless policy, always PAY until out of chips, beats random seats 59 of 60 times from both seat 1 and seat 2. The 

To bring the game back, clear `dropped` in its inventory record.
