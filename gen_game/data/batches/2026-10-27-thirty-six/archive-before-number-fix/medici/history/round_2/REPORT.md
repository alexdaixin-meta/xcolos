# medici: needs review

Built from the variation **Medici: Sealed Ledgers (revised)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- At the start of each day, the rebuilt 48-card deck is shuffled once. That single shuffle is the only random draw in any round, and it happens only in the first round of a day. Each round then moves the top 3 cards of the deck into the revealed row, with no further randomness. (fixes: P1 Random draws): This makes random_draws_per_round exactly 1 (in day-start rounds) or 0 (in all other rounds), explicitly.
- Track the favoured bonus with one per-player ship_favoured counter, incremented at LOAD. Reuse two table attributes (temp and high_bid) as scratch space for the tie count, the ship rank values and two of the majority maxima. Add two dedicated maxima for Spice and Dye. Do not store the day number or the active seat; compute both from the round number. (fixes: P2 Attribute overflow): This brings the explicit attribute list to 18, below the cap of 20, with a margin.
- Drop the total-cards tie-break. Equal florins at the end is a shared draw. (fixes: P4 Tie-break bloat): It saves an attribute, and ties are rare with 40-florin bankrolls and varied awards.
- Publish a numbered 19-step round. Ship rank uses 4 steps (compute top, award, compute second distinct, award). All four majority maxima are computed in one step and awarded in one step. Favoured scoring and the end check are one step each. (fixes: P3 Understated step count): The declared steps_per_round then matches the real build: 19 of 20, with 2 choice steps.
- Keep sealed simultaneous bids, with every player, the active seat included, bidding at the same moment. Ties for the high bid void the sale. (fixes: P5 In the original, the drawer bids last, which gives the active seat a structural edge on its own lots.): This removes the last-bidder edge, and voiding ties stops coordinated equal bids from winning anything.

Objective: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, they share a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PRIZE SIZES. At the end of each day a player can earn:
- 10 for the top ship value;
- 5 for the second;
- 4 for each good where they hold or share the highest cumulative count (4 goods, paid on all 3 days, so an early majority keeps paying);
- 3 per favoured card on the ship (at most 15).
Payments l
- playable: pass. TIMING CHECKS.
- Day start runs when round mod 2N = 1, which holds at rounds 1, 2N+1 and 4N+1 because 2N is at least 6.
- Day end runs when round mod 2N = 0, at rounds 2N, 4N and 6N, so day 3 is scored before the game ends at 6N.
- A day uses 3 cards per round over 2N rounds, at most 36 cards with 6
- reasoning_over_luck: pass. WHERE CHANCE COMES IN. There are two sources:
- the favour deal, which is symmetric in 3-4 player games because the goods are distinct and identical in value;
- the daily shuffle, whose revealed cards are public and open to every bidder equally.
The main luck is whether cards of your favoured good h

## Complexity

- steps_per_round: designed 19, built 19, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 18, built 55, limit 20 (built: 80)
- hidden_elements: designed 2, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 40 florins, empty ship and zero good counts for every seat
- pass: Favour pool with 4 players is 4 tiles, all dealt (0 left)
- pass: Favour pool with 5 players is 8 tiles, 5 dealt (3 left)
- FAIL: Deck built with 48 cards in round 1: 45 remain after 3 are revealed | rule R3 is broken: When the deck is built, then it has 48 cards: 12 per good with values 0,1,1,2,2,3,3,3,4,4,5,5 (sum 33 per good).; Ada: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Round 5 with 3 players has active seat 2 | rule R4 is broken: When round is r, then the active seat is ((r-1) mod N)+1.; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Day start (round 7 of 3 players) empties ships and rebuilds the deck, keeping florins and counts | rule R5 is broken: When round mod 2N = 1, then the deck is rebuilt as all 48 cards and shuffled, and every ship_value, ship_count and ship_favoured is set to 0, while florins and cumulative counts are kept.; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Each round reveals 3 cards from the deck | rule R6 is broken: When a round begins, then 3 cards are drawn from the deck and revealed to everyone in order as revealed cards 1, 2 and 3.; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Lot size 2 takes two revealed cards and discards the third | rule R7 is broken: When the active seat chooses lot size k (1, 2 or 3), then the lot is the first k revealed cards and the other 3-k revealed cards are discarded for the day.; seat 1 ship_count: expected 2, got 0; seat 1 spice_count: expected 2, got 0; seat 1 ship_value: expected 6, got 0; seat 1 florins: expected 35, got 40; game lot_size: expected 2, got 1; game winner_seat: expected 1, got 0; game discard: expected 1 items, got 3; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Active seat bids too; bids range up to own florins only | rule R8 is broken: When bids are made, then every player, the active seat included, bids at the same time a whole number from 0 to their current florins, and 0 is a pass.; seat 2 florins: expected 33, got 40; seat 2 ship_count: expected 1, got 0; seat 2 ship_value: expected 2, got 0; seat 2 dye_count: expected 1, got 0; game winner_seat: expected 2, got 0; game high_bid: expected 7, got 0; seat 2 was never offered 7, but should have been; Blaise: the rule for 1 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat)
- FAIL: A bid from a seat whose ship cannot hold the lot is voided | rule R9 is broken: When a player's ship_count plus lot_size exceeds 5 (for example ship_count 4 and lot_size 2), then that player's bid becomes 0.; seat 3 florins: expected 35, got 40; seat 3 ship_count: expected 2, got 0; seat 3 ship_value: expected 8, got 0; seat 3 cloth_count: expected 2, got 0; game winner_seat: expected 3, got 0; game high_bid: expected 5, got 0; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Unique highest bidder pays the bid and wins the lot | rule R10 is broken: When the highest bid is above 0 and exactly one player made it, then that player pays their bid to the bank, the florins leave the game, and that player wins the lot.; seat 1 florins: expected 28, got 40; seat 1 ship_count: expected 1, got 0; seat 1 ship_value: expected 4, got 0; game winner_seat: expected 1, got 0; game high_bid: expected 12, got 0; Ada: the rule for 12 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 8 was never matched (the game never put that option to this seat)
- FAIL: Tied highest bids: no sale, nobody pays | rule R11 is broken: When all bids are 0, or two or more players tie for the highest bid, then the lot is discarded, nobody pays and there is no sale.; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: All bids 0: no sale, nobody pays | rule R11 is broken: When all bids are 0, or two or more players tie for the highest bid, then the lot is discarded, nobody pays and there is no sale.; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Winning a mixed 3-card lot adds values, count and per-good counts | rule R12 is broken: When a player wins a lot, then their ship_value increases by the sum of the lot values, their ship_count by the lot size, their ship_favoured by the number of lot cards of their favoured good, and each cumulative good count by the number of lot cards of that good.; seat 1 florins: expected 31, got 40; seat 1 ship_value: expected 11, got 4; seat 1 ship_count: expected 4, got 1; seat 1 grain_count: expected 3, got 1; seat 1 cloth_count: expected 1, got 0; game winner_seat: expected 1, got 0; game lot_size: expected 3, got 1; Ada: the rule for 9 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: After the auction the winner and price are public | rule R13 is broken: When a round's auction ends, then the lot, every bid, and the winner and price (or 'no sale') are announced to everyone.; seat 3 florins: expected 34, got 40; game winner_seat: expected 3, got 0; game high_bid: expected 6, got 0; Ada: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 1 was never matched (the game never put that option to this seat); Cleo: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: Day end: seats tied for top ship value each gain 10, next value gains 5 | rule R14 is broken: When round mod 2N = 0, then every player whose ship_value equals the highest ship_value gains 10 florins, if that value is above 0.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Day end: seats tied for second ship value each gain 5 | rule R15 is broken: When round mod 2N = 0, then every player whose ship_value equals the highest ship_value strictly below the top gains 5 florins, if that value is above 0.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Day end: majority in each good pays 4 to every seat tied at the max, none for a good nobody holds | rule R16 is broken: When round mod 2N = 0, then for each of the four goods, every player whose cumulative count equals the highest count of that good gains 4 florins, if that count is at least 1.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Day end: 3 florins per favoured-good card on the ship (equal ships all take the top bonus) | rule R17 is broken: When round mod 2N = 0, then each player gains 3 florins per card of their favoured good on their ship (3 * ship_favoured).; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Game ends after round 18 with 3 players, after day-end payouts | rule R18 is broken: When round = 6N (18 with 3 players, 24 with 4, 30 with 5, 36 with 6), then the game ends after that round's day-end payouts.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Seats tied for most florins at the end share the win | rule R19 is broken: When the game ends, then the player with the most florins wins, and players tied for the most share the win.; Cleo: the rule for 1 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 6], results {'seat 1': 8, 'seat 3': 9, 'seat 2': 10, 'seat 5': 4, 'seat 4': 5, 'seat 6': 3, 'seats 2 and 3': 1}, 58-235 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 146.2 decisions, prompts of 406 characters on average (longest 455)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 98% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seat 1': 22, 'seat 3': 18, 'seat 2': 19, 'seats 1 and 2': 1}
- always `first@seat1`: won 58, lost 1, drew 1
- always `first@seat2`: won 60, lost 0, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 3, lost 57, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The tests follow the rules. In all four failing scenarios the active seat was never offered the lot-size choice that rule R4 gives it, or was offered only part of it. The trace also shows other defects in the file: only seat 2 was polled for a bid, the deck held repeated 'Grain-2' cards, and the game stopped at round 6 instead of running 6N rounds.
- round 1: fix_game: The trace shows the game moves `round` from 1 to 2 and `active_seat` from 1 to 2 before round 1 is played, so seat 2 chooses the lot size in round 1. The rules make seat ((r-1) mod N)+1 active, which is seat 1 in round 1. Because of this off-by-one, the scripted lot sizes and bids never reach the right seats, every bid comes out 0, nobody wins, and all three revealed cards are discarded instead of only the unchosen one.
- round 1: fix_game: The tests follow the rules. In R2 the 58-florin result checks out: 40, plus 3 from each of the 4 split majorities, plus 6 for favoured cards, gives 58008. The traces show the game file does not give the active seat a correct lot-size choice: in round 5 seat 2 was never offered 3, and in rounds 18 (N=3), 7 (N=3) and 16 (N=4) the active seat was never asked for a lot size at all.
- round 2: fix_game: The trace shows two bugs in the game file. The deck is built as only three copies of 'Spice-3' instead of the 48-card deck. The round counter also advances from 1 to 2, moving the active seat from 1 to 2, before the lot-size choice, so seat 2 picks the lot size in round 1 and seat 1 is never offered it. These failures come from the implementation, not from the tests or the rules.
- round 2: fix_game: The trace shows clear bugs in the game file. The deck is built as only three 'Spice-3' cards instead of the 48-card deck. The round counter moves 0→1→2 inside the first round, so seat 2 rather than seat 1 is asked for the lot size in round 1. The tests' failures follow directly from these bugs, and the rules are expressible on the platform.
- round 2: fix_game: The trace shows the game file breaking the rules. The deck is built as only three copies of 'Spice-3' instead of 48 cards, and the round counter goes 0→1→2 within the first round. As a result, seat 2 is asked for the lot size in round 1 instead of seat 1. The tests read the rules correctly; the file is wrong.

## Choices the rules did not make

- 3 to 6 players, suggested 4: The designer suggests 4. Three is the minimum where sealed bids face more than one rival and majorities can be contested. Above 6, the favour pool and the day length would no longer fit the 48-card deck.
- No talk phase: The source states there is no talk phase. The strategy lies in reading public bids, ships and counts to infer others' florins and favoured goods.
- Cards encoded as Good-Value text in lists: This lets drawing, lots, ships and discards be list operations, and lets values and goods be counted arithmetically.
- Card value distribution given as one count per value (value_0_cards_per_good ... value_5_cards_per_good): Parameters must be single numbers, so the list 0,1,1,2,2,3,3,3,4,4,5,5 is written as how many cards of each value each good has.
- ship_favoured kept visible only to its owner (ally): Making it public would reveal the favoured good, which the rules keep secret until the end.
- Bids stored in a public attribute filled by a poll: Nobody sees a bid until all are in, and the rules make all bids public at the announcement.

## Simplifications

- Shuffling the deck is done as drawing cards at random from the deck list: The engine has no shuffle operation; random draws are equivalent and seeded.
- Day-start and day-end steps run every round but carry a 'when round mod 2N' condition: The step list is flat; each conditional step is a single conditioned update, not an alternative block.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'winner_seat > 0 and you.florins >= high_bid' reads `you` where there is no player
- 2: it plays, but part of it does nothing: game attribute `goods` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `unique_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `unique_values` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
