# english_auction: needs review

Built from the variation **Budgeted English Auction Series** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Play a sequence of 6 items, one per round, instead of one item. (fixes: P3): This creates a multi-round game where players must plan across items and can learn from opponents' earlier bids.
- Every player receives the same six values {3,5,7,9,11,13}, privately shuffled across the six items. (fixes: P2, P4): Every player's values sum to the same 48, so the deal no longer decides who is richer; it only decides where each player's strength lies. It also makes inference work like card counting: a rival who fought hard for an early item probably spent their 13 or 11 there and cannot hold it again.
- Each player has a fixed budget of 30 coins for the whole game. Bids above your remaining budget are invalid. (fixes: P1, P3): Truthful bidding is no longer dominant. Winning an item at a high price can leave you unable to afford your 13 later. Rivals can deliberately push prices up to drain a leader's budget, so players must budget across rounds.
- Each item gets exactly three simultaneous raise-or-pass bidding turns. The standing bid and leader are announced after each turn, and ties go to a priority order that rotates each round. (fixes: P5): This keeps the open, ascending, see-the-standing-bid character of an English auction in a fixed number of steps. Rotating priority removes any seat advantage.
- Use 3 to 5 players. The highest total profit (values of items won minus prices paid) wins, and equal top totals draw. (fixes: P6, P1): With three or more players, one rival's gain is not automatically another's loss. Passing scores 0 and loses to anyone who wins an item profitably, and overbidding produces negative totals.
- Add one simultaneous message per round before bidding. (fixes: P4): It allows players to propose bidding rings ('you take this one, I take the next'), bluff about their values, and threaten to push prices. Because only one player can win, every ring is tempting to betray, so promises must be read and tested.

Objective: After round 6, the player with the highest score wins. If two or more players share the highest score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Main decision: how much to bid on an item with private value v in {3,5,7,9,11,13}, given a budget of 30 that cannot cover all 48 points of value (13+11+9 = 33 already exceeds 30). Winning at price p scores v - p. Losing scores 0.

Thoughtless policies, judged by the WINNER RULE (highest total wins):
- playable: pass. Rules are complete:
- Valid and invalid bids are defined: an invalid bid counts as a pass.
- The floor for turns 2 and 3 is the standing bid + 1.
- The leader may re-raise.
- Ties go by an explicit rotating priority formula.
- An unsold item scores nothing.
- Negative scores are allowed.
- Budget is
- reasoning_over_luck: pass. Chance enters only through the deal: which item gets your 13 versus your rivals' high values. Under competitive play, the surplus of the highest-value bidder on an item is roughly max - second value.
- For N=3 independent permutations of {3..13}, E[max - second] is about 2.5 per item.
- Across 6 ite

## Complexity

- steps_per_round: designed 11, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 12, built 31, limit 20 (built: 80)
- hidden_elements: designed 1, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: every seat starts with budget 30 and score 0, nothing sold yet
- pass: Setup with 4 players: public state only shows budgets and scores, values stay private
- FAIL: Round 3 sells item 3: seat 1 values item 3 at 7, buys at 4 | rule R3 is broken: In round r, item r is sold, for r from 1 to 6.; seat 1 budget: expected 26, got 30; seat 1 score: expected 3, got 0; game leader: expected 1, got 0; game standing_bid: expected 4, got 0; game last_price: expected 4, got 0; Ada: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Round 2 with 3 players: priority 2,3,1, so seat 3 beats seat 1 on a tie at 6 | rule R4 is broken: In round r with N players, priority starts at seat ((r - 1) mod N) + 1 and continues in increasing seat order, wrapping around; with N = 3, round 2's order is 2, 3, 1.; seat 3 budget: expected 24, got 30; seat 3 score: expected -1, got 0; game leader: expected 3, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; Ada: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 6 was never matched (the game never put that option to this seat)
- pass: A round where everyone passes leaves the announced budgets and scores unchanged
- FAIL: Talk binds nobody: after talk, a single bid of 2 by seat 2 still decides the round | rule R6 is broken: Before bidding each round, every player submits one short message simultaneously, and all messages are then shown to everyone.; seat 2 budget: expected 28, got 30; seat 2 score: expected 7, got 0; game leader: expected 2, got 0; game standing_bid: expected 2, got 0; game last_price: expected 2, got 0; Blaise: the rule for 2 was never matched (the game never put that option to this seat)
- pass: Turn 1: a seat with budget 0 may only pass, and a bid cannot exceed the budget
- FAIL: Turn 1: bids 3, 7 and 5, so the highest (seat 2, 7) leads and buys | rule R8 is broken: In bidding turn 1, if at least one valid bid is made, the highest valid bid becomes standing_bid and its bidder becomes leader; if none is made, standing_bid = 0 and leader = 0.; seat 2 budget: expected 23, got 30; seat 2 score: expected 2, got 0; game leader: expected 2, got 0; game standing_bid: expected 7, got 0; game last_price: expected 7, got 0; Ada: the rule for 3 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Turn 2: a bid equal to the standing bid counts as a pass | rule R9 is broken: In bidding turns 2 and 3, a bid is valid only if it is at least standing_bid + 1 (at least 1 when there is no standing bid) and at most the bidder's budget; otherwise it counts as a pass.; seat 1 budget: expected 25, got 30; game leader: expected 1, got 0; game standing_bid: expected 5, got 0; game last_price: expected 5, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Turn 2 raise to 8 by seat 2 takes the lead; no bid in turn 3 keeps it | rule R10 is broken: In bidding turns 2 and 3, if any valid bid is made, the highest valid bid becomes standing_bid and its bidder becomes leader; if none is made, standing_bid and leader are unchanged.; seat 2 budget: expected 22, got 30; seat 2 score: expected 3, got 0; game leader: expected 2, got 0; game standing_bid: expected 8, got 0; game last_price: expected 8, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 8 was never matched (the game never put that option to this seat)
- FAIL: Round 1 tie at 8 between seats 1 and 3: seat 1 leads by priority | rule R11 is broken: When two or more players make the same highest valid bid in a turn, the one earliest in this round's priority order becomes leader; e.g. in round 1 with seats 1 and 3 both bidding 8, seat 1 leads.; seat 1 budget: expected 22, got 30; seat 1 score: expected 5, got 0; game leader: expected 1, got 0; game standing_bid: expected 8, got 0; game last_price: expected 8, got 0; Ada: the rule for 8 was never matched (the game never put that option to this seat); Cleo: the rule for 8 was never matched (the game never put that option to this seat)
- FAIL: The leader may raise its own bid: seat 1 bids 4, then 6 | rule R12 is broken: The current leader may bid in turns 2 and 3 but need not.; seat 1 budget: expected 24, got 30; seat 1 score: expected 3, got 0; game leader: expected 1, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; seat 1 was never offered 6, but should have been; Ada: the rule for 4 was never matched (the game never put that option to this seat); Ada: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: No bid in turn 1, then a bid of 3 in turn 2 sets the standing bid and leader | rule R13 is broken: After each bidding turn, the standing bid and leader (or no bid) are announced.; seat 2 budget: expected 27, got 30; seat 2 score: expected 2, got 0; game leader: expected 2, got 0; game standing_bid: expected 3, got 0; game last_price: expected 3, got 0; Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Value 7 bought at 10 gives score -3 and budget 20 | rule R14 is broken: When a round ends with a leader, the leader's budget falls by standing_bid and their score changes by (their value for this item minus standing_bid); e.g. value 7 bought at 10 gives score -3.; seat 1 budget: expected 20, got 30; seat 1 score: expected -3, got 0; game leader: expected 1, got 0; game last_price: expected 10, got 0; Ada: the rule for 10 was never matched (the game never put that option to this seat)
- FAIL: Sale price 6 is recorded as last_price | rule R15 is broken: When a round ends with a leader, the price is announced but the winner's private value is not.; seat 3 budget: expected 24, got 30; seat 3 score: expected -3, got 0; game leader: expected 3, got 0; game last_price: expected 6, got 0; Cleo: the rule for 6 was never matched (the game never put that option to this seat)
- pass: Unsold item: no budget or score changes and last_price becomes 0
- pass: After round 6 the game ends: all pass, seat 1 with the top score wins
- FAIL: Seat 2 buys item 6 (value 11) for 8 and ties seat 1 at 5; unspent budget is worth nothing | rule R18 is broken: When the game ends, the player with the highest score wins, unspent budget is worth 0, and players tied at the highest score share the result as a draw.; winner: expected 'seats 1 and 2', got 'seat 1'; seat 2 standing: expected 5, got 2; seat 2 budget: expected 2, got 10; seat 2 score: expected 5, got 2; Blaise: the rule for 8 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 12, 'seat 1': 9, 'seat 3': 10, 'seats 1 and 3': 2, 'seat 4': 4, 'seat 5': 2, 'seats 3 and 4': 1}, 31-97 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 61.0 decisions, prompts of 259 characters on average (longest 373)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 2 wins 93% of decided matches against random seats
- random seats: {'seat 2': 23, 'seat 1': 18, 'seat 3': 17, 'seats 1 and 3': 1, 'seats 1, 2 and 3': 1}
- always `first@seat1`: won 49, lost 9, drew 2
- always `first@seat2`: won 56, lost 4, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 1, lost 59, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: Every scenario where a player is scripted to bid failed the same way: the scripted bid (4, 6, 2, 7) was never among the options the game offered, so every seat fell back to 0, nothing sold, and budgets and scores stayed at 30 and 0. The rules plainly allow any whole-number bid from min_bid up to the remaining budget, so the tests are right and the game's bid choice is built wrong.
- round 1: fix_game: In every failing scenario the scripted bid (4, 6, 2, 7) was never matched because the game never offered that amount as an option. Every recorded move was 0, so no item was ever sold. The tests read the rules correctly; the game file's bidding choice does not offer whole-number bids, so the auction never runs.
- round 1: fix_game: In every failing scenario each seat only ever played 0, and the harness reports that the scripted bid (4, 6, 2, 7) was never offered as an option. The rules allow any whole-number bid from 1 up to the bidder's remaining budget, so the game's bidding choice is not presenting the legal bid amounts. The tests themselves are consistent with the rules.

## Choices the rules did not make

- 3 to 5 players, suggested 3: The designer suggested 3, so it is kept. The minimum is 3 because an auction needs at least two rivals for price competition and for the tie-break rotation to matter. The maximum stays at the source's 5 because larger tables make each seat's bids marginal and the talk long.
- Kept simultaneous talk as a poll with broadcast: The rules require it. Players disagree, since each wants the others to stay out of the items they value most, so non-binding claims about values and intentions are worth reasoning about and doubting.
- Pass encoded as bid 0, with a bid range of 0 to budget: The engine takes whole numbers in a range. Bids above budget cannot be entered, and the source treats them as passes anyway.
- Tie-break computed as key = bid * 10 + (N - 1 - ((seat - first_seat) mod N)): This gives the priority order arithmetically. The multiplier 10 exceeds N, so the bid always dominates.
- Leader 0 and standing_bid 0 encode 'no bid': The source's 'no standing bid' needs a concrete state value.
- The six item values are listed as separate parameters item_value_1 to item_value_6: Each parameter must be a single number. They are the values dealt to every player, not tied to specific items.
- Scores remain public, as the source states: The source says budgets and scores are public but values are private. A public score change lets observers deduce the winner's value; this is kept faithfully.
- Strategy note: With 30 coins against a 48-value set, a thoughtful player plans which items to chase given their own values and the rotating tie-break. They shade bids below value and read rivals' remaining budgets and talk. A thoughtless one overspends early or bids above value.

## Simplifications

- An invalid bid in turns 2 and 3 (1 to standing_bid) can still be typed and is treated as a pass: The engine range cannot have a gap between pass and the minimum raise. The source's own rule says invalid bids count as passes.
- The source's 'draw' is a shared win among the top-scoring players: The engine has no separate draw outcome. Players level at the top share the win.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'leader != no_leader_code and standing_bid <= you.budget' reads `you` where there is no player
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, message, message) in `your_private_values`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
