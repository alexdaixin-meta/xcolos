# dollar_auction: needs review

Built from the variation **War of Attrition Auctions** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Three or four players instead of two. (fixes: In a two-player highest-total game, winning the auction always beats losing it by 0.95 regardless of price, so 'always raise' cannot lose and escalation is unbounded.): Two bidders locked in an escalation war both bleed coins while a bystander who stayed out pulls ahead. Escalation becomes genuinely costly under a highest-total rule, which restores the trap's meaning.
- A series of 6 auctions funded from one budget of 100 coins per player. Final score is coins left plus the value of prizes won. (fixes: A single one-shot auction gives no planning over several rounds and no budget trade-offs.): Coins spent fighting in one auction are unavailable later, so players must plan across rounds and pick their battles.
- Each player is secretly dealt their own random order of prize values: the six numbers 10, 15, 20, 25, 30 and 40, one per auction. Everyone's list totals 140. (fixes: Perfect information: there is no hidden state to infer, only an unbounded test of will.): This is one hidden element. Players must infer from bidding behaviour which auctions rivals value highly. Because every list has the same total, the deal changes what to do, not who is ahead.
- Each auction is played as exactly 3 simultaneous raise stages, with cumulative bids revealed after each stage. All players pay their full cumulative bid (all-pay, as in the original), and the sole highest bidder takes the prize. (fixes: The open-ended alternating raise loop has no fixed number of steps, which the flat step list cannot build cleanly.): This keeps the dollar auction's escalation and sunk-cost pressure: after stage 1 you see you are behind and must decide whether to throw more in. The length is fixed and buildable.
- A tie for the highest cumulative bid leaves the prize unclaimed, though everyone still pays. The winner is whoever has the highest final score. (fixes: Skill at the game, knowing when to stay out or stop, is not rewarded by a who-ends-higher rule with two players.): Matching bids is punished rather than rewarded. Restraint (staying out, stopping early) shows up directly in the score, and with three or more players a fighter's loss is the bystander's gain.
- A simultaneous one-message talk phase before each auction. (fixes: Perfect information: there is no hidden state to infer, only an unbounded test of will.): Players have opposed interests: only one can win, and values are private. Talk enables bluffing about values, proposing bid rings ('you take this one, I take the next'), and testing whether such promises are kept. All of this is non-binding.

Objective: The player with the highest final score (coins remaining plus prize points) wins. If two or more players tie for the highest final score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Coins and prize points count 1:1. In an auction you win you net v - b; in one you lose you net -b. A bid above your own value can never pay. SEAT/ORDER: all choices and talk are simultaneous polls, so no seat moves first or sees more than another. Every player holds the same multiset {10,15,20,25,30
- playable: pass. RULES ARE COMPLETE: raise range, available coins, cumulative commitment, unique-highest test (ties or all-zero bids mean no winner), payment by everyone, scoring and the draw rule are all stated. A player with 0 coins can only raise 0. The game is finite (6 auctions x 3 raise polls) and decided by a
- reasoning_over_luck: pass. CHANCE is limited to how the values line up across players per auction. Every player's six values sum to 140, so in the two-bidder view the sum of (v1 - v2) over the 6 auctions is exactly 0. The positive gaps (A's rent) therefore equal the negative gaps (B's rent), so complete-information equilibriu

## Complexity

- steps_per_round: designed 15, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 10, built 24, limit 20 (built: 80)
- hidden_elements: designed 1, built 6, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat starts with 100 coins, nothing committed, auction 0
- pass: Setup: each seat holds a private values list of six entries (the order is random, so only the count is checked)
- pass: A new round advances the auction by 1 and committed is back to 0
- pass: The talk step changes no state when every seat then raises 0
- FAIL: Raises across stages add up: 10 then 5 costs 15 coins, and nothing above the coins is offered | rule R5 is broken: When a raise stage runs, then each player chooses a raise from 0 to coins - committed simultaneously, and committed increases by that raise.; seat 1 coins: expected 85, got 100; seat 1 was never offered 100, but should have been; Ada: the rule for 10 was never matched (the game never put that option to this seat); Ada: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: With 40 coins and 30 committed, a raise of 10 is still allowed and nothing above 40 in total is ever offered | rule R6 is broken: When a player has coins 40 and committed 30, then their raise options are 0 to 10.; seat 1 coins: expected 0, got 40; seat 1 was never offered 10, but should have been; Ada: the rule for 30 was never matched (the game never put that option to this seat); Ada: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: Three raise stages each run: a raise of 5 in each stage costs 15 | rule R7 is broken: When each of the 3 raise stages ends, then every player's committed bid is announced to all.; seat 2 coins: expected 85, got 100; Blaise: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Bids 20, 15, 0 leave coins 80, 85, 100 | rule R8 is broken: When an auction resolves, then every player's coins decrease by their committed bid, whether or not they won (bids 20, 15, 0 leave coins 80, 85, 100 from 100 each).; seat 1 coins: expected 80, got 100; seat 2 coins: expected 85, got 100; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 15 was never matched (the game never put that option to this seat)
- FAIL: A sole top bid of 20 wins this auction's value of 30 (every values entry is set to 30) | rule R9 is broken: When exactly one player holds the highest committed bid and it is at least 1, then that player's prize_points increase by their own values entry for this auction.; seat 1 coins: expected 80, got 100; Ada: the rule for 20 was never matched (the game never put that option to this seat)
- FAIL: A tie at the top (20, 20, 5) gives nobody the prize and all three still pay | rule R10 is broken: When two or more players tie for the highest committed bid (e.g. 20, 20, 5), then nobody's prize_points change, and all three still pay.; seat 1 coins: expected 80, got 100; seat 2 coins: expected 80, got 100; seat 3 coins: expected 95, got 100; Ada: the rule for 20 was never matched (the game never put that option to this seat); Blaise: the rule for 20 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- pass: All bids 0: no winner and no coins change
- FAIL: The winner's seat is recorded and every seat's coins are updated | rule R12 is broken: When an auction resolves, then the winner's seat (or none) and all coins are announced, but the prize value won is not.; seat 2 coins: expected 93, got 100; game auction_winner: expected '2', got 'none'; Blaise: the rule for 7 was never matched (the game never put that option to this seat)
- pass: After auction 6 the game ends and final_score = coins + prize_points
- pass: Seats level at the top of coins + prize_points share the win
- FAIL: A winning final bid decides the game: the bid's prize value lifts the seat to the top | rule R14 is broken: When the game ends, then the player with the highest coins + prize_points wins, and players tied at the top share the win.; winner: expected 'seat 1', got 'seat 2'; seat 1 standing: expected 90, got 70; seat 1 coins: expected 60, got 70; seat 1 final_score: expected 90, got 70; Ada: the rule for 10 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seats 1 and 2': 2, 'seat 2': 8, 'seat 1': 11, 'seat 3': 9, 'seats 1 and 3': 2, 'seats 1, 2 and 3': 1, 'seat 4': 6, 'seats 1 and 4': 1}, 26-65 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 39.8 decisions, prompts of 193 characters on average (longest 251)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 97% of decided matches against random seats
- random seats: {'seats 1 and 2': 3, 'seat 2': 19, 'seat 1': 19, 'seat 3': 15, 'seats 1 and 3': 1, 'seats 1, 2 and 3': 1, 'seats 2 and 3': 2}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 58, lost 2, drew 0
- always `last@seat1`: won 7, lost 47, drew 6
- always `last@seat2`: won 10, lost 42, drew 8

## Triage (whose problem each failure was)

- round 1: fix_game: The tests correctly expect each raise stage to offer every whole number from 0 to coins − committed. In the game, no seat was ever offered 5, 10, 20 or even 100, so every raise came out 0 and coins never dropped. The raise-choice options in the game file are wrong. This is not a rules or platform problem.
- round 1: fix_game: The tests read the rules correctly: raises from 0 to coins minus committed, raises summed across the three stages, and every committed bid paid at resolution. The game never offered any raise above 0, since every seat played only 0 and options like 5, 10, 20 and 100 were never offered. So no coins ever moved, which is a bug in how the file builds the raise options.
- round 1: fix_game: In every raise stage the game offered each seat only a raise of 0, so 10, 15, 20 and 100 were never put to any seat and coins never fell below 100. The tests ask for exactly what the rules say: a raise from 0 to coins minus committed, and every committed bid paid at resolution.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The designer suggested 3. With 3, a tie between two bidders lets the third steal cheaply, and talk can form two-against-one splits. At 4 the auctions are still contested. More would dilute each player's influence and lengthen talk beyond the source's range.
- Talk as a simultaneous poll with broadcast: The source says messages are written at the same time without seeing others. Players disagree over who takes which auction, so claims and bluffs about values matter.
- Each player's value ordering built by drawing all six values at random from a copy of prize_deck: This implements the 'random ordering' dealing with list draws.
- prize_points visible only to the owner until the end: The source says won values are not revealed. Only who won is announced.

## Simplifications

- A tie for the highest final score is a shared win rather than a separate draw: The engine ranking has tied top players share the win, which is equivalent to the source's draw.
- The highest bid is found through table attributes top_bid and top_count: The engine has no direct player-to-player attribute comparison, so a table attribute is kept beside the bids.
- A final_score attribute is set at the end: It gives an observable score, since prize_points stay hidden during play.

## Encoding attempts

- 1: the game file was refused by the loader: dollar_auction: steps[5].do[0].value.calc: cannot read 'you.raise': invalid syntax
- 2: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'auction_winner' is not a declared player attribute
- 3: it plays, but part of it does nothing: game attribute `prize_deck` is never changed in 3 random matches, so nothing updates it. Steps that name it: starting coins and the deal. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
