# Dropped: too complex

it could not be built to behave as designed: scenario `Stage bound: with coins 85 and committed 30 the next stage allows at most 55` failed: rule R6 is broken: Immediately before each of the 3 raise stages, each player's max_raise = coins - committed (for example coins 85 and committed 30 give max_raise 55).; seat 1 committed: expected 85, got 0; seat 1 coins: expected 0, got 85; seat 1 prize_points: expected 20, got 0; game top_bid: exp (after 3 variation(s))

## The last variation tried

Sealed Escalation: Three-Way Dollar Auction: Three players each have 100 coins and play 6 all-pay auctions. Each auction has 3 simultaneous raise stages, and every player pays everything they commit. Only a unique top bidder wins the prize, valued privately by each player. The highest coins-plus-prizes total wins.

## What was tried

- round 1: behavior problem; triage said fix_game: The tests correctly expect each raise stage to offer every whole number from 0 to coins − committed. In the game, no seat was ever offered 5, 10, 20 or even 100
- round 1: behavior problem; triage said fix_game: The tests read the rules correctly: raises from 0 to coins minus committed, raises summed across the three stages, and every committed bid paid at resolution. T
- round 1: behavior problem; triage said fix_game: In every raise stage the game offered each seat only a raise of 0, so 10, 15, 20 and 100 were never put to any seat and coins never fell below 100. The tests as
- round 2: behavior problem; triage said fix_game: The rules use a per-player numeric bid range, which the platform supports through numeric_bids. In every failing scenario the raise poll put no option above 0 t
- round 2: behavior problem; triage said fix_game: Every player chose 0 in all nine raise polls. The tests report that options like 5, 40 and 100 were 'never put to this seat', so the raise poll is not offering 
- round 2: behavior problem; triage said fix_game: In every failing scenario the raise poll offered only 0. Seats were never offered 5, 40 or 100, so committed, coins and top_bid never moved. The rules allow a p
- round 3: behavior problem; triage said fix_game: In every failing scenario all three seats played 0 in all three stages, so committed, coins, top_bid and auction_winner never moved. That happened even where th
- round 3: behavior problem; triage said fix_game: Every failing scenario expects a nonzero raise (12, 7, 15, 55, 10), yet every move recorded is 0 and coins never drop. The tests' chosen amounts are not reachin
- round 3: behavior problem; triage said fix_game: In every failing scenario all nine raise moves came out as 0, even where the tests asked for positive raises (12, 7, 15) that R6 allows. So the file's raise pol

To bring the game back, clear `dropped` in its inventory record.
