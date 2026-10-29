# dollar_auction: needs review

Built from the variation **Collector's Dollar Auction** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use exactly 4 players, with the highest final score (coins plus prize points) winning. (fixes: P1): Two players locked in a war both fall behind the two who stayed out. Escalating 'to win' the auction can now lose the game, which brings back the dollar auction's real trap.
- Make it a bystander game: every player pays whatever they bid (all-pay), and only the top bidder receives the prize. (fixes: P5): This keeps the original's 'losers pay too' and makes every coin spent a real cost against the players who did not spend.
- Give each player a hidden type, Red collector or Blue collector, with exactly two of each. Prizes alternate Red and Blue. A prize is worth 12 points to a matching player and 6 to the others. The points a winner earns are kept private. (fixes: P2): Players must infer who truly values the current prize and therefore who will fight hard. Every type faces exactly one same-type rival and an equal number of matching prizes, so the deal decides what to do, not who is ahead.
- Replace open-ended alternating raises with three fixed simultaneous stages per round: a sealed opening bid, then up to two raise stages open only to the leading contenders. Raising 0 means dropping out. (fixes: P3): This keeps the escalation dynamic, adding more on top of money already sunk while seeing the rival's commitment, inside a bounded number of steps.
- Play 8 rounds from a shared starting purse of 40 coins, with bids limited by coins in hand. (fixes: P4): Spending in one war reduces your power later. Players must choose which prizes to contest and track rivals' remaining coins.
- Add one simultaneous message each round before bidding. (fixes: P2): Players can claim types, bluff, or propose splitting prizes. Same-type rivals and the winner rule (only one player wins) keep their interests in conflict, so promises must be tested against the bids they produce.

Objective: The player with the highest final score (coins plus prize points) wins. If two or more players tie for the highest score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Payoff per round for the round winner is (12 or 6) minus their total bid. Every other player gets minus their total bid. Score is coins plus points, so the labels 'worth 12 if matching, 6 if not' agree with the arithmetic. Bids are all-pay, so there is no hidden overpay trap beyond the stated one.


- playable: pass. Rules cover every case.
- Contenders are defined for unique highest bids, ties, a single positive bidder, and no positive bidder.
- Raise 1 runs only with at least 2 contenders. Raise 2 runs only with at least 2 contenders who raised more than 0.
- Dropped contenders keep their opening bid in their 
- reasoning_over_luck: pass. The only random element is the setup deal of a 2/2 type split, which is symmetric. No player is advantaged by their type beyond the minor round-8 Blue edge.

When all players play well (rotation or equilibrium bidding), the winner is decided by strategic choices:
- mixing in all-pay bids;
- who defe

## Complexity

- steps_per_round: designed 14, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 12, built 30, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat has 40 coins and 0 prize points, kept through an all-zero round
- pass: All four types are dealt out of the deck (random split, so only the empty deck is checked)
- pass: Round 1 prize is Red: a Red sole bidder gains 12
- pass: Round 2 prize is Blue: a Blue sole bidder gains 12
- pass: Talk step runs and the round proceeds with no effect on coins
- pass: Opening bid range is 0 to current coins
- pass: Bids 5,5,5,2 give three contenders; seat 1 raises 1 and wins
- pass: Bids 7,0,0,0: the bidder of 7 is sole contender and wins
- pass: All opening bids 0: nobody wins
- pass: Two contenders get Raise 1; seat 1 raises 2 and wins
- pass: Sole contender: raises skipped, pays only the opening bid
- pass: Contender raising 0 drops out; the others go on to Raise 2
- pass: Two positive Raise 1s lead to Raise 2
- pass: Total bid is opening + Raise 1 + Raise 2 (4+6+5 vs 4+6+0)
- pass: Single highest total wins the prize
- pass: Tie for the highest total: nobody wins, both still pay
- pass: Every player pays their own bid, winner or not
- pass: Mismatched type: a Red winner of the Blue prize gains 6
- pass: The prize winner is announced; only the winner gains points
- pass: Round 8 ends the game; score = coins + prize points
- pass: Tied top scores share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seats 2 and 4': 1, 'seat 4': 4, 'seat 3': 5, 'seat 2': 4, 'seat 1': 5, 'seats 1 and 4': 1}, 70-78 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 73.0 decisions, prompts of 167 characters on average (longest 207)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 88% of decided matches against random seats
- random seats: {'seats 2 and 4': 2, 'seat 4': 11, 'seat 3': 13, 'seat 2': 12, 'seat 1': 15, 'seats 1 and 4': 1, 'seats 2 and 3': 2, 'seats 1, 2 and 4': 1, 'seats 1, 2 and 3': 1, 'seats 1 and 2': 1, 'seats 2, 3 and 4': 1}
- always `first@seat1`: won 53, lost 7, drew 0
- always `first@seat2`: won 49, lost 11, drew 0
- always `last@seat1`: won 1, lost 54, drew 5
- always `last@seat2`: won 0, lost 52, drew 8

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file works as specified. The flaw is in the design: every player pays their whole bid, a prize is worth at most 12 points, and unspent coins count fully toward the score. So never bidding (the first option, 0) keeps all 40 coins and beats any player who bids, and it won 88% of decided matches against random seats.

## Choices the rules did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer fixed 4 and the type split of 2 Red and 2 Blue depends on it. Each type has one rival with the same interest, so bidding wars and bluffing about type both happen.
- Talk kept as a simultaneous poll broadcast to all: The source specifies simultaneous, non-binding talk. Players disagree about who should win each prize and can bluff their type or threaten bidding wars, so the talk gives them something to reason about.
- A round with all total bids at 0 has no winner: This follows from the tie rule: all four tie at 0. Writing highest_total > 0 makes it explicit.
- The second-highest opening bid is the 2nd value of the four bids sorted descending, ties counted: This matches the source's 'ties included' and its sole-contender case: with one positive bid the second-highest is 0, so that bidder qualifies.
- The score attribute is computed only at the end: Prize points are private until the end, so a public running score would leak them.
- Strategy at the table: A thoughtful player bids only when the value is worth the sunk cost (12 points for a matching type, 6 otherwise), reads opening bids for type signals, avoids escalation because losers still pay, and saves coins, which count directly toward the score.

## Simplifications

- A draw is represented as a shared win among the players tied at the top: The engine's ranking has no separate draw outcome. Tied top players share the win.
- Conditional raise steps use a `when` condition on a single poll: The step list is flat. Each raise is a single step that is skipped when its condition fails, which needs no block branching.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 4 players: the match crashed: FlowError: 'you.total_bid <= you.coins' reads `you` where there is no player
- 2: passed
