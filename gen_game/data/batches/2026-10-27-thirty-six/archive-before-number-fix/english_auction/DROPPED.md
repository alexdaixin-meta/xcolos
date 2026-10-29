# Dropped: too complex

it could not be built to behave as designed: scenario `Public results after a sale: highest of three distinct valid bids wins at its own bid` failed: rule R3 is broken: A player's values list is visible only to that player. Budgets, scores, spent, eligibility, all bids after each turn, standing_bid, leader and last_price are public.; seat 2 budget: expected 23, got 30; seat 2 score: expected 4, got 0; seat 2 spent: expected 7, got 0; game last_pr (after 3 variation(s))

## The last variation tried

Budget English Auction: Six items are auctioned one per round in short ascending auctions. Every player values the same six numbers in a private shuffled order and has 30 coins for the whole game. The highest total profit wins.

## What was tried

- round 1: behavior problem; triage said fix_game: Every scenario where a player is scripted to bid failed the same way: the scripted bid (4, 6, 2, 7) was never among the options the game offered, so every seat 
- round 1: behavior problem; triage said fix_game: In every failing scenario the scripted bid (4, 6, 2, 7) was never matched because the game never offered that amount as an option. Every recorded move was 0, so
- round 1: behavior problem; triage said fix_game: In every failing scenario each seat only ever played 0, and the harness reports that the scripted bid (4, 6, 2, 7) was never offered as an option. The rules all
- design 1: the critic found it not sound (balanced)
- round 2: behavior problem; triage said fix_game: In every failing scenario, a seat scripted to bid when 4 (or 1) is among its options actually played 0 on all three turns, so no valid bid ever registered and b
- round 2: behavior problem; triage said fix_game: In every failing scenario the scripted seat was told to bid an amount it is allowed to bid (4, 3 or 1, all within budget 30). The game still recorded 0 for ever
- round 2: behavior problem; triage said fix_game: All four failing scenarios show the same thing: no seat ever makes a winning bid, so nothing is sold. In the given-values scenario seat 1 answered 0 in all thre
- round 3: behavior problem; triage said fix_game: The bid poll is not offering the options R7 requires. Seat 2 was never offered 0 or 10, and the scripted bids of 1, 2, 3, 5 and 7 never matched, so every seat f
- round 3: behavior problem; triage said fix_game: The bid poll does not offer the options R7 requires. In every failing scenario the scripted bids (3, 7, 5, 2, 1, 10, and even 0) were never offered, every recor
- round 3: behavior problem; triage said fix_game: The tests follow the rules: R7 says every player is offered 0 or any whole number from 1 to their budget. The game's bid poll never offered values such as 0, 2,

To bring the game back, clear `dropped` in its inventory record.
