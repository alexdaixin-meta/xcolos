# the_speicherstadt: ready for review

Built from the variation **Speicherstadt Queues (Even Rotation)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Play exactly 12 rounds with a 36-card deck: 6 colours (add Orange) × 6 cards each. Contracts are dealt from the 6 colours. (fixes: Seat edge: over 10 rounds the rotating priority leader gives some seats more lead rounds and more early-queue positions than others (N=3: 4/3/3; N=4: 3/3/2/2). Leading is worth about 2-4 points, so seat order alone skews results.): 12 is a multiple of 3 and of 4. Under the rotation, each seat holds every priority position (1st, 2nd, 3rd, 4th) exactly 12/N times: 4 times each at N=3, 3 times each at N=4. Each colour still appears exactly 6 times, so every contract stays equally supplied.
- The priority order each round is a full cyclic rotation starting from seat ((round-1) mod N)+1. It is stated as covering all positions, not just the leader. (fixes: The rest of the priority order is also unbalanced: with 10 rounds, seats do not hold each queue position (2nd, 3rd, 4th) equally often, so the edge extends beyond the lead.): With 12 rounds the rotation is a complete set of cyclic shifts repeated 12/N times, so every seat has an identical distribution of queue positions.
- Restrict the game to 3 or 4 players. (fixes: Allowing 2 players turns the higher-total rule into a pure difference contest, and 5 players cannot be made to rotate evenly through the round count.): With three or more players, one rival's gain is not another's loss, so the higher-total rule does not collapse into a difference contest. 12 rounds rotate evenly for both counts.
- Starting coins stay at 6 and income stays at 2 per round, so pass-only play reaches 30 coins. Limits stay 0-6. (fixes: Seat edge: over 10 rounds the rotating priority leader gives some seats more lead rounds and more early-queue positions than others (N=3: 4/3/3; N=4: 3/3/2/2). Leading is worth about 2-4 points, so seat order alone skews results.): The price scale (1-4) against values (2 or 5) is unchanged, so the tested economics carry over. The 12th-round tie-break remains arithmetic.

Objective: The player with the highest final score wins. If several tie for highest, the tied player with more goods of their own contract colour wins. If they are still tied, the game is a draw among them. If all players finish equal on both measures, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. VALUES AND PRICES. A good of your own colour is worth 5 points and any other good is worth 2. Coins are worth 1 point each. The offer price on a lot starts at k (the queue length, at most N, and N is at most 4) and drops by 1 per decline. So the price is always between 1 and 4.

Net gain from accept
- playable: pass. The rules are complete:
- The deck size (36) matches 12 rounds × 3 lots, and the end is fixed at round 12.
- The queue order is the announced priority order.
- The price starts at k and decreases by 1, with explicit coin and limit checks.
- There is an explicit overflow rule for more than 2 positive
- reasoning_over_luck: pass. Chance sources:
- the deal of contract colours, which is symmetric, since each colour has exactly 6 cards and all are revealed;
- the deck order, which decides whether your colour lands in rounds where you hold early priority, or on the same round as another player's colour.

Estimate. Each player s

## Complexity

- steps_per_round: designed 12, built 20, limit 20
- choice_steps_per_round: designed 2, built 4, limit 4
- attributes: designed 14, built 48, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck holds 36 cards (33 after the first round's 3 lots) and each of 4 seats takes a different contract from the pool of 6
- pass: Setup: every player starts with 6 coins and no goods (8 coins after one round's income with no purchases)
- pass: Each round draws 3 lots from the deck (36 -> 33)
- pass: Every player gains 2 coins in the round (6 -> 8 with no purchases)
- pass: Round 2 priority starts at seat 2: seat 2 buys Lot 1 at price 2 ahead of seat 1
- pass: Round 4 priority starts at seat 4: seat 4 buys Lot 1 at price 2 ahead of seat 1
- pass: Round 5 priority wraps back to seat 1: seat 1 buys Lot 1 at price 2 ahead of seat 4
- pass: Talk round happens and play continues normally (messages are answered automatically)
- pass: Limits range from 0 to 6: 0 and 6 offered, 7 never offered
- pass: Three positive limits: seat 1 buys only Lots 1 and 2, and Lot 3 goes to seat 2 at price 1
- pass: First offer is at price k=3 to the earliest queued seat in priority (seat 2)
- pass: Limit exactly equal to price 2 buys: seat 1 pays 2 and takes the good
- pass: Limits below price pass the offer down: the third queued seat buys at price 1
- pass: Too few coins passes the offer: seat 1 with 2 coins cannot pay 3, seat 2 buys at 2
- pass: Nobody queues: all three lots are discarded and nobody gains goods
- pass: Coins spent on Lot 1 count for Lot 2: seat 1 is then short and Lot 2 goes to seat 2 at price 1
- pass: After a lone purchase at price 1 the buyer's coins and goods are publicly updated
- pass: Game ends after round 12; all seats level at score 8 share the win
- pass: Final score: 10 coins + 2 own-colour goods + 3 other goods = 26
- pass: Game end reveals contracts and sets final scores (only scores are observable)
- pass: Tied score 15 is broken by more own-contract goods: seat 1 wins
- pass: Level on score and own-contract goods: seats 1 and 2 share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec declares player attribute `seat` but the game file does not: a piece of state the rules need is missing

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 12, 'seat 1': 7, 'seats 1 and 3': 2, 'seat 2': 13, 'seat 4': 6}, 113-162 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 136.8 decisions, prompts of 183 characters on average (longest 217)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 19, 'seat 1': 19, 'seats 1 and 3': 1, 'seat 2': 19, 'seats 1 and 2': 2}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 15, lost 44, drew 1
- always `last@seat2`: won 15, lost 44, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: Both failures are 'never matched' complaints about Ada's scripted answers, not wrong coins, goods or scores. That fits a correct game that stops asking for a Lot 3 limit once a player has placed both workers on Lots 1 and 2. Under R8 such a player's Lot 3 entry would be forced to 0 anyway, so the game is right not to put the Lot 3 option to that seat, and the scripts expecting a third answer go unmatched.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer chose 4, and the even rotation needs 12/N to be a whole number, which holds for 3 and 4. Three is the smallest table where two rivals contest a lot and the queue price ladder matters. Above 4, 6 contract colours and 3 lots per round get too thin. The strategy is to infer rivals' contracts from their purchases and talk, to bluff about your own, and to time your bids around the rounds where you hold priority.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Players compete for lots and hide their contracts, so talk invites bluffing and deterrence that could cost a player who believes it.
- Tie-break encoded as score * 100 + own_goods: own_goods is at most 6, which is below 100, so this ranks by score and then by own-contract goods. Players level on both share the win, which is the source's draw.
- Contracts marked not observable: They are hidden during play and revealed only at the end; the score is the observable outcome.

## Simplifications

- The three limits are collected as three consecutive simultaneous polls instead of one combined submission: The engine takes one number per question. Limits are never revealed, so no player learns anything between the polls.
- The falling-price offer is unrolled into one conditional update per priority position for each lot: The step list is flat. Up to N fixed steps with when/if conditions reproduce the sequential offer exactly.
- Final scoring and the contract reveal are a conditional update in round 12, just before the end check: The score must be computed before the arithmetic ranking runs.
