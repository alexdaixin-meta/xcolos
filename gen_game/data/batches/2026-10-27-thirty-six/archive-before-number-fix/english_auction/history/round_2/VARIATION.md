# Variation: Budgeted English Auction with Activity Rule

Six items are auctioned one per round to 3 to 6 bidders with private values and a shared-size budget. Each item gets three simultaneous bidding turns. You can only keep bidding if you bid in the previous turn or are leading, and an exact tie at the top wins nothing.

Players: 3 to 6, best with 4

## Review of the original

An English (ascending) auction: bidders with private valuations raise a standing bid in turn order until a full round passes with no raise. The last bidder wins and earns value minus price; everyone else earns zero. The reviewed variation made it a six-item budgeted auction with three simultaneous bidding turns per item, talk, and a rotating priority tie-break.

- **non_degenerate**: weak. No thoughtless policy dominates. Always-pass ends on 0 and loses to anyone who buys one item below value. Always-max bids 30 on item 1, scores at most 13-30=-17 and is bankrupt for the rest of the game. However, the priority tie-break gives a built-in seat edge for N=4 (summed weights 15/17/15/13) and N=5 (20/19/18/17/16, with seat 1 also first in round 6). Ties are common because bids are small integers.
- **skill_sensitive**: good. A budget of 30 against a value total of 48 forces players to choose which items to contest. Reading rivals' interest from talk and bids, and pacing the budget, separates good play from bad. The value lists are permutations of the same set, so luck of the deal is small.
- **headroom**: weak. Turns 1 and 2 are weakly dominated: a bid placed early commits you and leaks information, and it cannot deter anyone, because rivals can still bid standing+1 in turn 3 with no reply possible. Optimal play collapses to one sealed bid in turn 3, which removes the ascending-auction depth.
- **reasoning_dependent**: good. Values are private, and only the set {3,...,13} is common knowledge. Players must infer rivals' values for each item from talk and bids and plan their budget across 6 rounds.
- **verifiable**: good. Scores are value minus price, summed. The winner is the strictly highest score, otherwise a draw. It is pure arithmetic.
- **fits_platform**: good. Simultaneous polls, numeric bids, private values and talk are all supported. The round fits in about 15 steps and 4 choice steps, with 6 rounds and no board.

## Problems

- P1: The rotating priority tie-break creates a systematic seat advantage for N=4 and N=5. Integer bids make ties frequent, so the advantage matters.
- P2: Bids in turns 1 and 2 are weakly dominated by waiting and sniping in turn 3. The ascending auction degenerates into a first-price sealed bid, and the early turns only duplicate the talk channel.

## Changes

- Remove priority weights entirely. A turn has a winner only if exactly one player made the highest valid bid. If two or more players tie at the top, nobody wins that turn and the standing bid and leader stay as they were. A lower bid never wins because of a tie above it. (fixes: P1): The rule treats every seat the same in every round, for any N from 3 to 6. A tie also becomes a strategic risk, because a tied bid wins nothing, rather than a matter of seat luck.
- Add an activity rule. Turn 1 is open to everyone. In turn 2 or turn 3, a player may bid only if they made a valid bid in the previous turn, or they are the leader at the start of that turn. A player who drops out cannot return for that item. (fixes: P2): Waiting now forfeits the right to snipe. To contest the final turn you must enter at a binding price in earlier turns. Early bids become real commitments and signals, the field visibly narrows as in an English auction, and turn-3 bidders know exactly who they face and what those players committed.
- Record each player's eligibility in a visible yes/no attribute that is announced after each turn. (fixes: P2): Everyone can reason about who is still in, and the engine can enforce eligibility with a simple condition.

## Kept from the original

- Ascending bidding on each item, where the leader pays their last bid and earns value minus price
- Private valuations drawn from a common, known set, with every list worth the same total of 48
- Six items sold one per round with a shared budget of 30, forcing a choice of which items to fight for
- Simultaneous non-binding talk before each item
- The strictly highest total score wins; a tie at the top is a draw

## The variation's rules

R1 Setup. There are N players (3 to 6). Each player starts with budget 30, score 0 and spent 0. Before round 1, each player whose values list is empty receives a private values list: a random ordering of [3,5,7,9,11,13], so every list sums to 48. A list that is already set is never overwritten. Table state starts at standing_bid 0, leader 0 (0 means no leader) and last_price 0.
R2 Privacy. A player's values list is visible only to that player. Everyone sees all budgets, scores, eligibility flags, standing_bid, leader and last_price. Everyone knows the value set is {3,5,7,9,11,13}.
R3 Items. The game has 6 rounds. In round r, item r is sold. A player's value for item r is entry r of their own list, counting from 1.
R4 Talk. At the start of each round, every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
R5 Round reset. After talk, set standing_bid to 0 and leader to 0, and mark every player eligible.
R6 Bidding turns. Each round has exactly 3 bidding turns. Each turn is a simultaneous poll of all players. Each player answers pass (0) or a whole number from 1 up to their current budget.
R7 Validity. A bid is valid only if all three conditions hold:
(a) the bidder is eligible for this turn;
(b) the bid is at least standing_bid + 1 (in turn 1 that means at least 1);
(c) the bid is at most the bidder's budget.
Pass, and any bid that is not valid, counts as no bid.
R8 Turn result. Find the highest valid bid.
- If exactly one player made it, standing_bid becomes that amount and leader becomes that player.
- If two or more players made it (a tie), or nobody made a valid bid, standing_bid and leader stay unchanged.
- A lower valid bid never wins.
R9 Eligibility. After each turn, a player is eligible for the next turn only if they made a valid bid in this turn (winning, tied or beaten), or they are the leader after this turn. Everyone else is marked ineligible for the rest of the round. After each turn, standing_bid, leader and all eligibility flags are announced.
R10 Resolution. After turn 3:
- If leader is not 0, the leader's budget decreases by standing_bid, their spent increases by standing_bid, and their score increases by (their value for item r) minus standing_bid. This can be negative.
- last_price is set to standing_bid. If leader is 0, the item goes unsold and last_price is 0.
- The round's result is announced.
R11 End. After round 6 the game ends. Unspent budget is worth nothing.

Objective: After round 6, the player with the strictly highest score wins. If two or more players share the highest score, the game is a draw.

Expected effect: Waiting no longer pays, because a player who skips a turn cannot come back for that item. Players must enter in turn 1 and keep bidding to stay in, so prices rise step by step and the field narrows publicly, as in a real English auction. Entering at a low price in turn 1 is cheap, but the bid binds if nobody raises. In turn 2 a player must decide whether staying in is worth a higher committed price, knowing exactly who else is still in. Turn 3 is a final bid among known survivors whose earlier bids reveal information. The tie rule is identical for every seat. Matching a rival exactly blocks both bids, which turns ties into a risk to manage. Talk passes both tests. Players disagree because each wants items cheaply while rivals overpay or stay out, and only one player can win. A player who honours a proposal such as 'you take item 2, I take item 3' can be undercut, or can let a rival buy below value and fall behind. Simple policies all lose to sensible play: always-pass ends on 0, always-max goes bankrupt with a negative score, and always minimum-raise overpays on low-value items and runs out of budget for high-value ones.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 11 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
