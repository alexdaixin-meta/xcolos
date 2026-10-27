# Dropped: too complex

it could not be built to behave as designed: scenario `With the season open, talk happens and the round goes on to a sale (seat 2 buys at 5)` failed: rule R9 is broken: When season_over is 0, then all three players write one message at the same time, and all are shown labelled by seat.; seat 1 money: expected 65, got 60; seat 2 money: expected 55, got 60; seat 2 bid: expected 5, got 0; Blaise: the rule for 5 was never matched (the game never put  (after 3 variation(s))

## The last variation tried

Modern Art: Sealed Gallery: Three players each hold a hidden hand of seven paintings across three artists, in compositions 4/2/1 that are worth the same in total. They take turns as auctioneer, offering one painting per round to a simultaneous sealed-bid auction preceded by one round of simultaneous talk. The third painting of an artist in a season ends the season and is not sold. Artists ranked first and second gain value that accumulates over the game, owned paintings pay out, and after 18 rounds the richest player wins.

## What was tried

- round 1: behavior problem; triage said fix_game: The tests match the rules: the auctioneer must pick a reserve from 0 up to their current money. The game never put 0, 25 or 100 to seat 1 as a reserve option, s
- round 1: behavior problem; triage said fix_game: The reserve choice is not built correctly. Seat 1 was never offered a reserve of 0 or 100, and an auctioneer choosing 25 still left the table `reserve` at 0. Th
- round 1: behavior problem; triage said fix_game: The rules are clear and within the platform's capabilities, but the file deals 9 cards each instead of 10. Its trace shows some 'pick' draws (e.g. green) that n
- design 1: the critic found it not sound (playable)
- round 2: behavior problem; triage said fix_game: The trace shows the file departing from the rules. Seat 1's dealt hand was overwritten after the deal: on roll 6 it got C (2,1,4), then hand_blue went 1->2 and 
- round 2: behavior problem; triage said fix_game: The trace shows the game mishandling hands: after seat 1 played Green, its hand_blue rose from 1 to 2 and hand_green fell from 4 to 2, which breaks R4 (only the
- round 2: behavior problem; triage said fix_game: The tests' expectations follow R2, R3 and R7. The game never offered the sealed bids as options from 0 up to each bidder's money, so the bid rules 'never matche
- design 1: the critic found it not sound (playable)
- round 3: behavior problem; triage said fix_game: Sealed numeric bids are supported, yet the bid step never accepted the tested amounts (5, 12, 8, 10): every bid was recorded as 0 and the auctioneer took the pa
- round 3: behavior problem; triage said fix_game: The rules are coherent and use only supported features (simultaneous numeric bids, conditional updates). The game file is at fault. Its bid step never offered a
- round 3: behavior problem; triage said fix_game: The tests follow the rules. Seats 2 and 3 are scripted to bid 5, 12 or 10, but every bid came out 0 and no money moved, and the scripted rule for the bid amount

To bring the game back, clear `dropped` in its inventory record.
