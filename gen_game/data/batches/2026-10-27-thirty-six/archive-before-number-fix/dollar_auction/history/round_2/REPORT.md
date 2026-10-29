# dollar_auction: needs review

Built from the variation **Escalation Auction** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Three to five players, with the winner decided by the highest final score (coins left plus prize points). (fixes: P1): One rival's gain is not every other's loss, and a player who sits out every auction is overtaken by anyone who wins a prize cheaply.
- Each player privately holds a value list: a random order of [10, 15, 20, 25, 30, 40], one value per auction. Only the owner sees it. (fixes: P2): Each player must infer from bids and talk who values the current prize highly. Every list has the same total of 140, so the deal changes what to do, not who is ahead.
- Six auctions drawn from one budget of 100 coins. (fixes: P3): Players must plan when to spend: whether to chase their 40-auction or win cheap prizes others ignore. They can also read opponents' remaining budgets.
- Each auction has exactly three simultaneous sealed raise stages. Committed bids are announced after each stage, and it is all-pay: everyone pays their committed total. (fixes: P4): This keeps the dollar auction's sunk-cost escalation in a fixed, buildable number of steps with no seat order.
- Ties at the top bid produce no winner, though everyone still pays. (fixes: P1): Matching an opponent is not safe, so the 'can't lose' option disappears.
- The raise poll's options are every whole number from 0 to (that player's coins − that player's committed), read live from those two player attributes at that moment. The chosen raise is added straight to committed. There are no scratch raise/stage_raise attributes. (fixes: P5): This removes the source of the 0-only option range, so bids accumulate and coins are deducted at resolution.
- Only the parameters actually used are kept as attributes (starting_coins, auctions, raise_stages, min_winning_bid, prize_deck). prize_value_1..6 and prize_value_total are dropped. (fixes: P6): This keeps the attribute count small and stops references to stale values.
- A simultaneous one-message talk phase before the first raise stage of each auction. (fixes: P2): Only one player can win each auction, so players disagree. They can bluff a high value to scare others off or feign disinterest, and listeners must judge it against bidding behaviour.

Objective: After 6 auctions, the player with the highest final_score (coins remaining + prize_points) wins. If several players tie for the highest final_score, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Main decision: in each auction you pay all of your committed coins whether you win or not (all-pay), and you score your private value v (10-40) only if your bid is the single highest. Net per auction: a sole top bidder gets v - b; everyone else gets -b. A player who bids 0 loses 0. Example with 3 pl
- playable: pass. Rules are complete. Setup, value deal, the 3 simultaneous raise stages with a range computed from coins - committed, announcements, payment, prize (sole top with top_bid >= 1, otherwise none) and the end score are all specified. Edge cases are covered: all bids 0 gives no winner; a tie at the top gi
- reasoning_over_luck: pass. Every player holds the same six values in a different order, so total potential value is identical (140) for all. Chance only affects how often high values collide in the same auction, which I estimate at about 20-30% of outcome variance. The rest is opponent modelling and planning. There is a lot t

## Complexity

- steps_per_round: designed 18, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 15, built 30, limit 20 (built: 80)
- hidden_elements: designed 1, built 6, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every player starts with 100 coins and zeros, and the table starts at zero with no winner
- pass: Setup: each player holds a values list of 6 entries (the order is random, so only the length is checked)
- pass: A round start raises auction by 1 (from 2 to 3) and committed is 0 afterwards
- pass: The first auction is numbered 1 and announcing coins changes no coins
- pass: The talk poll changes no numbers when everyone raises 0
- FAIL: Three raise stages of 5 each add up to a committed total of 15 | rule R6 is broken: Each auction has exactly 3 simultaneous raise stages, and after each one every player's committed increases by the raise they chose.; seat 1 coins: expected 85, got 100; game top_bid: expected 15, got 0; game top_count: expected 1, got 3; Ada: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: With 100 coins the raise options go up to 100 and no higher | rule R7 is broken: In a raise stage a player's options are exactly the whole numbers 0 to (coins - committed): 0..100 with coins 100 and committed 0, 0..55 with coins 85 and committed 30, 0..10 with coins 40 and committed 30.; seat 1 was never offered 100, but should have been; seat 1 was never offered 0, but should have been
- FAIL: With 40 coins and 30 committed, a raise of 20 is not offered in later stages | rule R7 is broken: In a raise stage a player's options are exactly the whole numbers 0 to (coins - committed): 0..100 with coins 100 and committed 0, 0..55 with coins 85 and committed 30, 0..10 with coins 40 and committed 30.; seat 1 coins: expected 10, got 40; game top_bid: expected 30, got 0; Ada: the rule for 30 was never matched (the game never put that option to this seat)
- FAIL: Committed cannot exceed coins: after going all in with 40, a later raise of 10 is not possible | rule R8 is broken: A player's committed can never exceed their coins within one auction.; seat 1 coins: expected 0, got 40; game top_bid: expected 40, got 0; game top_count: expected 1, got 3; Ada: the rule for 40 was never matched (the game never put that option to this seat)
- FAIL: Raises spread over the stages are all counted in the committed totals | rule R9 is broken: After each of the 3 raise stages, every player's committed total is announced to all.; seat 1 coins: expected 90, got 100; seat 2 coins: expected 86, got 100; game top_bid: expected 14, got 0; game top_count: expected 1, got 3; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat)
- FAIL: top_bid is the highest committed total and top_count counts the seats tied on it (20, 20, 5) | rule R10 is broken: After the third stage, top_bid = the highest committed and top_count = the number of players whose committed equals top_bid.; game top_bid: expected 20, got 0; game top_count: expected 2, got 3; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 20 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Everyone pays their bid, win or lose: 20, 15 and 0 leave 80, 85 and 100 | rule R11 is broken: After the third stage every player's coins decrease by their committed, win or lose: bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100.; seat 1 coins: expected 80, got 100; seat 2 coins: expected 85, got 100; game top_bid: expected 20, got 0; game top_count: expected 1, got 3; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 15 was never matched (the game never put that option to this seat)
- FAIL: The sole top bidder in auction 6 gains their value of 40 for that auction | rule R12 is broken: When top_count = 1 and top_bid >= 1, the player with committed = top_bid becomes auction_winner and adds their current_value to prize_points.; winner: expected 'seat 1', got 'seats 1, 2 and 3'; seat 1 standing: expected 130, got 100; seat 1 coins: expected 90, got 100; seat 1 final_score: expected 130, got 100; game top_bid: expected 10, got 0; game top_count: expected 1, got 3; Ada: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: A tie for the top bid gives no winner and no prize, but both tied seats still pay | rule R13 is broken: When top_count >= 2 (a tie for the highest bid), auction_winner = 'none' and nobody's prize_points change, although all players still pay their committed.; winner: expected 'seat 3', got 'seats 1, 2 and 3'; seat 1 standing: expected 90, got 100; seat 2 standing: expected 90, got 100; seat 1 coins: expected 90, got 100; seat 1 final_score: expected 90, got 100; seat 2 coins: expected 90, got 100; seat 2 final_score: expected 90, got 100; game top_bid: expected 10, got 0; game top_count: expected 2, got 3; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat)
- pass: When everyone bids 0 there is no winner
- FAIL: After resolution every committed is reset to 0 and the coins reflect the payments | rule R15 is broken: After resolution the auction_winner and every player's coins are announced, and every player's committed is reset to 0.; seat 1 coins: expected 88, got 100; seat 2 coins: expected 92, got 100; Ada: the rule for 12 was never matched (the game never put that option to this seat); Blaise: the rule for 8 was never matched (the game never put that option to this seat)
- pass: After the 6th auction final_score is coins + prize_points and the game ends
- pass: Seats tied on the highest final_score share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 10, 'seat 3': 11, 'seats 2 and 3': 1, 'seat 1': 10, 'seats 1, 2 and 3': 1, 'seat 4': 3, 'seat 5': 2, 'seats 1 and 4': 1, 'seats 4 and 5': 1}, 72-120 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 172 characters on average (longest 215)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 98% of decided matches against random seats
- random seats: {'seat 2': 16, 'seat 3': 20, 'seats 2 and 3': 2, 'seat 1': 19, 'seats 1, 2 and 3': 1, 'seats 1 and 2': 1, 'seats 1 and 3': 1}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 59, lost 1, drew 0
- always `last@seat1`: won 9, lost 47, drew 4
- always `last@seat2`: won 9, lost 47, drew 4

## Triage (whose problem each failure was)

- round 1: fix_game: The tests correctly expect each raise stage to offer every whole number from 0 to coins − committed. In the game, no seat was ever offered 5, 10, 20 or even 100, so every raise came out 0 and coins never dropped. The raise-choice options in the game file are wrong. This is not a rules or platform problem.
- round 1: fix_game: The tests read the rules correctly: raises from 0 to coins minus committed, raises summed across the three stages, and every committed bid paid at resolution. The game never offered any raise above 0, since every seat played only 0 and options like 5, 10, 20 and 100 were never offered. So no coins ever moved, which is a bug in how the file builds the raise options.
- round 1: fix_game: In every raise stage the game offered each seat only a raise of 0, so 10, 15, 20 and 100 were never put to any seat and coins never fell below 100. The tests ask for exactly what the rules say: a raise from 0 to coins minus committed, and every committed bid paid at resolution.
- round 2: fix_game: The rules use a per-player numeric bid range, which the platform supports through numeric_bids. In every failing scenario the raise poll put no option above 0 to any seat (5, 40 and 100 were never offered, and all moves were 0), so the bug is in the game file's raise step, not in the tests or the rules.
- round 2: fix_game: Every player chose 0 in all nine raise polls. The tests report that options like 5, 40 and 100 were 'never put to this seat', so the raise poll is not offering the range 0..(coins − committed) that R5/R6 require. The tests' expectations (committed 15 → coins 85, top_bid 15, top_count 1, and so on) follow the rules correctly. The engine can express a per-player numeric range, so the fault is in the file.
- round 2: fix_game: In every failing scenario the raise poll offered only 0. Seats were never offered 5, 40 or 100, so committed, coins and top_bid never moved. The rules allow a per-player numeric range of 0..(coins − committed), and numeric bids are supported, so the game file builds the range wrong.

## Choices the rules did not make

- 3 to 5 players, suggested 3: The designer chose 3, and an auction needs at least two rivals for ties and bid-reading to matter. Above 5, the talk and announcements grow long and each player wins too few of the 6 auctions for budgeting to matter.
- Keep the simultaneous talk poll: The rules require it, and players genuinely disagree: everyone wants rivals to back off. Bluffs and threats about which auctions they value give players something to reason about, and since talk is not binding, believing it can be costly.
- prize_points visible only to its owner: The rules announce only the winner and coins. Publishing prize_points would reveal the winner's private value for that auction.
- Values entries indexed from 1: The rules say entry k is the value for auction k, and auction runs from 1 to 6.
- Strategy at the table: This is an all-pay auction, so overbidding is costly and ties waste both bids. A thoughtful player rations 100 coins over 6 auctions, pushes on high-value auctions, watches rivals' committed totals between stages, and avoids matching a rival's total.

## Simplifications

- The 3 raise stages are written out as explicit poll and tell steps rather than as a repeat: This keeps the flat step list clear without a scratch stage counter, and the behaviour is identical.
- final_score is computed in the last update of the 6th round: It is the same arithmetic as R10, placed just before the ending check.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `prize_deck` is never changed in 3 random matches, so nothing updates it. Steps that name it: the table. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
