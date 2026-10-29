# english_auction: needs review

Built from the variation **Budgeted English Auction with Activity Rule** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Remove priority weights entirely. A turn has a winner only if exactly one player made the highest valid bid. If two or more players tie at the top, nobody wins that turn and the standing bid and leader stay as they were. A lower bid never wins because of a tie above it. (fixes: P1): The rule treats every seat the same in every round, for any N from 3 to 6. A tie also becomes a strategic risk, because a tied bid wins nothing, rather than a matter of seat luck.
- Add an activity rule. Turn 1 is open to everyone. In turn 2 or turn 3, a player may bid only if they made a valid bid in the previous turn, or they are the leader at the start of that turn. A player who drops out cannot return for that item. (fixes: P2): Waiting now forfeits the right to snipe. To contest the final turn you must enter at a binding price in earlier turns. Early bids become real commitments and signals, the field visibly narrows as in an English auction, and turn-3 bidders know exactly who they face and what those players committed.
- Record each player's eligibility in a visible yes/no attribute that is announced after each turn. (fixes: P2): Everyone can reason about who is still in, and the engine can enforce eligibility with a simple condition.

Objective: After round 6, the player with the strictly highest score wins. If two or more players share the highest score, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SETUP. Each player holds a private permutation of [3,5,7,9,11,13], so everyone's values total 48. Budget is 30, which is less than 33 (13+11+9), so no one can buy all their best items. Bids are simultaneous, so no seat has an edge from move order. Every player sees the same public information, so no
- playable: pass. RULES COVERAGE. The rules cover every situation:
- validity of bids (eligibility, minimum standing+1, budget cap);
- tie handling at the top (no change);
- no-bid handling;
- eligibility (made a valid bid or is leader);
- unsold items (leader 0, so last_price is 0);
- negative scores;
- a budget of 
- reasoning_over_luck: pass. WHAT CHANCE DECIDES. The deal is the only chance element, and it is equalised: every player holds the same multiset {3,...,13}. Chance decides only which rounds a player's high values collide with opponents' high values. Example: my 13 lands where the others hold 3 and 5, so I win cheaply.

WHAT REA

## Complexity

- steps_per_round: designed 15, built 12, limit 20
- choice_steps_per_round: designed 4, built 2, limit 4
- attributes: designed 11, built 33, limit 20 (built: 80)
- hidden_elements: designed 1, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start state: budgets 30, scores 0, spent 0, empty table
- pass: Every seat gets a 6-entry values list (random order, only the count is asserted)
- FAIL: A values list that is already set is not overwritten: seat 1 with value 13 for item 1 wins it at 4 and scores 9 | rule R2 is broken: When setup runs and a player's values list is empty, then that player receives a random ordering of [3,5,7,9,11,13], which sums to 48. When a list is already set, then it is not overwritten.; seat 1 budget: expected 26, got 30; seat 1 score: expected 9, got 0; seat 1 spent: expected 4, got 0; game leader: expected 1, got 0; game standing_bid: expected 4, got 0; game last_price: expected 4, got 0; Ada: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Results are public: after seat 2 wins item 1 at 3, all budgets and scores are shown and each seat still holds 6 values | rule R3 is broken: When values are dealt, then a player's values list is visible only to that player, while all budgets, scores, spent, eligibility flags, standing_bid, leader and last_price are public.; seat 2 budget: expected 27, got 30; seat 2 score: expected 6, got 0; seat 2 spent: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: Round 3 sells item 3: seat 1's value is entry 3 of its list (13), so winning at 4 scores 9 | rule R4 is broken: When round r is played (r from 1 to 6), then item r is sold, and a player's value for it is entry r of their own values list, counting from 1.; seat 1 budget: expected 26, got 30; seat 1 score: expected 9, got 0; seat 1 spent: expected 4, got 0; game last_price: expected 4, got 0; game leader: expected 1, got 0; Ada: the rule for 4 was never matched (the game never put that option to this seat)
- pass: Talk binds nobody: a round where everyone talks and then passes leaves the item unsold
- FAIL: Standing bid and leader reset at round start: an old standing bid of 9 does not stop a bid of 1 | rule R6 is broken: When the talk phase of a round ends, then standing_bid becomes 0, leader becomes 0 and every player becomes eligible.; seat 1 budget: expected 29, got 30; seat 1 score: expected 4, got 0; seat 1 spent: expected 1, got 0; game leader: expected 1, got 0; game standing_bid: expected 1, got 0; game last_price: expected 1, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: Three bidding turns: bids 1/2, 3/4 and 5/6 leave seat 2 paying 6 | rule R7 is broken: When a round is played, then it has exactly 3 bidding turns. In each turn, all players answer at the same time with 0 (pass) or a whole number from 1 to their current budget.; seat 2 budget: expected 24, got 30; seat 2 score: expected 7, got 0; seat 2 spent: expected 6, got 0; game leader: expected 2, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; seat 1 was never offered 0, but should have been; seat 1 was never offered 30, but should have been; Ada: the rule for 1 was never matched (the game never put that option to this seat); Ada: the rule for 3 was never matched (the game never put that option to this seat); Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: A bid from a seat that passed earlier (ineligible) counts as no bid | rule R8 is broken: When a player bids, then the bid is valid only if the player is eligible, the bid is at least standing_bid + 1 (at least 1 in turn 1), and the bid is at most the player's budget. A pass or an invalid bid counts as no bid.; seat 2 budget: expected 27, got 30; seat 2 score: expected 2, got 0; seat 2 spent: expected 3, got 0; game leader: expected 2, got 0; game standing_bid: expected 3, got 0; game last_price: expected 3, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: A bid equal to the standing bid (not standing_bid + 1) is invalid | rule R8 is broken: When a player bids, then the bid is valid only if the player is eligible, the bid is at least standing_bid + 1 (at least 1 in turn 1), and the bid is at most the player's budget. A pass or an invalid bid counts as no bid.; seat 1 budget: expected 25, got 30; seat 1 score: expected 4, got 0; seat 1 spent: expected 5, got 0; game leader: expected 1, got 0; game standing_bid: expected 5, got 0; game last_price: expected 5, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat); Blaise: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: A unique highest bid of 6 against 4 takes the lead at 6 | rule R9 is broken: When exactly one player made the highest valid bid in a turn (for example a single bid of 6 against a bid of 4), then standing_bid becomes that amount and leader becomes that player's seat.; seat 1 budget: expected 24, got 30; seat 1 score: expected 5, got 0; seat 1 spent: expected 6, got 0; game leader: expected 1, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; Ada: the rule for 6 was never matched (the game never put that option to this seat); Blaise: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Two bids of 6 tie, so nobody leads; the lower 4 does not win and the item goes unsold | rule R10 is broken: When two or more players tie on the highest valid bid (for example two bids of 6), or nobody made a valid bid, then standing_bid and leader stay unchanged. A lower valid bid never wins.; Ada: the rule for 6 was never matched (the game never put that option to this seat); Blaise: the rule for 6 was never matched (the game never put that option to this seat); Cleo: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: The leader stays eligible after passing; a seat that passed cannot come back with 9 | rule R11 is broken: When a turn ends, then a player stays eligible for the next turn only if they made a valid bid in that turn (winning, tied or beaten) or they are the leader. Every other player is ineligible for the rest of the round.; seat 1 budget: expected 24, got 30; seat 1 score: expected 7, got 0; seat 1 spent: expected 6, got 0; game leader: expected 1, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat); Ada: the rule for 0 was never matched (the game never put that option to this seat); Ada: the rule for 6 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 9 was never matched (the game never put that option to this seat); Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: An outbid seat that made a valid bid stays eligible and can raise to win | rule R11 is broken: When a turn ends, then a player stays eligible for the next turn only if they made a valid bid in that turn (winning, tied or beaten) or they are the leader. Every other player is ineligible for the rest of the round.; seat 3 budget: expected 24, got 30; seat 3 score: expected 1, got 0; seat 3 spent: expected 6, got 0; game leader: expected 3, got 0; game standing_bid: expected 6, got 0; game last_price: expected 6, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat); Cleo: the rule for 2 was never matched (the game never put that option to this seat); Cleo: the rule for 6 was never matched (the game never put that option to this seat)
- FAIL: Standing bid and leader are public after the turns: seat 2 leads at 4 | rule R12 is broken: When a turn ends, then standing_bid, leader and every eligibility flag are announced to all.; seat 2 budget: expected 26, got 30; seat 2 score: expected 7, got 0; seat 2 spent: expected 4, got 0; game leader: expected 2, got 0; game standing_bid: expected 4, got 0; Blaise: the rule for 4 was never matched (the game never put that option to this seat)
- FAIL: Value 3 bought at price 8 gives a score of -5 | rule R13 is broken: When turn 3 ends with leader not 0 and standing_bid p, then the leader's budget decreases by p, their spent increases by p, and their score increases by (their value for item r) minus p. This can be negative: value 3 at price 8 gives -5.; seat 1 budget: expected 22, got 30; seat 1 score: expected -5, got 0; seat 1 spent: expected 8, got 0; game last_price: expected 8, got 0; game leader: expected 1, got 0; Ada: the rule for 8 was never matched (the game never put that option to this seat)
- pass: Unsold item sets last_price to 0 even if it was 7 before
- FAIL: Sold item sets last_price to the price | rule R14 is broken: When turn 3 ends, then last_price is set to standing_bid if there is a leader, and to 0 if leader is 0 (the item goes unsold). The round's result is announced.; seat 3 budget: expected 28, got 30; seat 3 score: expected 7, got 0; seat 3 spent: expected 2, got 0; game last_price: expected 2, got 0; game leader: expected 3, got 0; Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: Game ends after round 6; unspent budget counts for nothing, seat 1 wins with score 8 | rule R15 is broken: When round 6 has been resolved, then the game ends, and unspent budget is worth nothing.; winner: expected 'seat 1', got 'seat 2'; seat 1 standing: expected 8, got 0; seat 1 score: expected 8, got 0; seat 1 budget: expected 5, got 10; game last_price: expected 5, got 0; Ada: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: Two seats level at the top score share the win | rule R16 is broken: When the game ends, then the player with the strictly highest score wins. If two or more players share the highest score, then they share the result (a draw).; winner: expected 'seats 1 and 2', got 'seat 2'; seat 1 standing: expected 5, got 3; seat 1 score: expected 5, got 3; seat 1 budget: expected 27, got 30; Ada: the rule for 3 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 6], results {'seat 3': 7, 'seat 2': 5, 'seat 1': 13, 'seats 1 and 2': 1, 'seat 5': 6, 'seat 6': 7, 'seat 4': 1}, 72-144 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 108.0 decisions, prompts of 246 characters on average (longest 291)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 97% of decided matches against random seats
- always taking the first option as seat 2 wins 95% of decided matches against random seats
- random seats: {'seat 3': 21, 'seat 2': 17, 'seat 1': 18, 'seats 1 and 2': 3, 'seats 1 and 3': 1}
- always `first@seat1`: won 57, lost 2, drew 1
- always `first@seat2`: won 56, lost 3, drew 1
- always `last@seat1`: won 1, lost 59, drew 0
- always `last@seat2`: won 2, lost 57, drew 1

## Triage (whose problem each failure was)

- round 1: fix_game: Every scenario where a player is scripted to bid failed the same way: the scripted bid (4, 6, 2, 7) was never among the options the game offered, so every seat fell back to 0, nothing sold, and budgets and scores stayed at 30 and 0. The rules plainly allow any whole-number bid from min_bid up to the remaining budget, so the tests are right and the game's bid choice is built wrong.
- round 1: fix_game: In every failing scenario the scripted bid (4, 6, 2, 7) was never matched because the game never offered that amount as an option. Every recorded move was 0, so no item was ever sold. The tests read the rules correctly; the game file's bidding choice does not offer whole-number bids, so the auction never runs.
- round 1: fix_game: In every failing scenario each seat only ever played 0, and the harness reports that the scripted bid (4, 6, 2, 7) was never offered as an option. The rules allow any whole-number bid from 1 up to the bidder's remaining budget, so the game's bidding choice is not presenting the legal bid amounts. The tests themselves are consistent with the rules.
- round 2: fix_game: In every failing scenario, a seat scripted to bid when 4 (or 1) is among its options actually played 0 on all three turns, so no valid bid ever registered and budgets, scores and last_price never changed. This points to the game's bidding poll not offering the whole-number amounts 1..budget as choosable options (or not recording the chosen amount as the bid), not to a problem with the rules or the tests.
- round 2: fix_game: In every failing scenario the scripted seat was told to bid an amount it is allowed to bid (4, 3 or 1, all within budget 30). The game still recorded 0 for every move, so its bid poll never offers those amounts. The tests follow R6–R10 correctly; all-pass leading to everyone ineligible and no sale is the right outcome, but only because the bids were never available.
- round 2: fix_game: All four failing scenarios show the same thing: no seat ever makes a winning bid, so nothing is sold. In the given-values scenario seat 1 answered 0 in all three turns although its rule was to pick 4 whenever 4 was offered. That means the game file never offered a real bid (or treated every bid as invalid), so the fault is in the file, not the rules or the tests.

## Choices the rules did not make

- 3 to 6 players, 4 suggested: The designer set 3 to 6 with 4 suggested. Three is the smallest table where an auction has several rivals, so ties and drop-outs matter. Above 6, talk gets long and each player wins too few of the 6 items for their choices to matter.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages shown to all. Talk earns its place because players have conflicting private values: they may signal, bluff about which items they value, or try to arrange not to bid against each other.
- The strategy a thoughtful player follows: Each player has a budget of 30 against values totaling 48, so they must save money for their high-value items. Bidding in every turn keeps a player eligible, tied bids win nothing, and players must guess rivals' values from talk and past prices.
- Bids are polled from ineligible players too, and their bids are simply invalid: The source says each turn polls all players, and the validity check handles eligibility.
- Leader stores the seat number, with 0 meaning no leader: The source uses 0 for no leader, and seats are numbered from 1.
- The value set is listed as six numeric parameters value_1 to value_6: Each parameter must be a single number. The set itself is kept as the public table list value_set.

## Simplifications

- A draw at the top is expressed as a shared win among the players tied for highest score: The engine has no separate draw. Players level at the top share the win, which is the arithmetic equivalent of the source's draw.
- The three bidding turns are one block of steps run by a repeat until turn == 3: This avoids writing the same steps three times. The behavior is identical.
- Scratch attributes top_bid, top_count and valid_bid are added: The engine needs stored intermediate values to compute the highest unique valid bid by arithmetic.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {budget} (in `prompt`: 'Item 1, bidding turn 1 of 3. Standing bid 0, leader seat 0 (0 = none). Answer 0 to pass, o'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {budget} (in `prompt`: 'Item 1, bidding turn 1 of 3. Standing bid 0, leader seat 0 (0 = none). Answer 0 to pass, o'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {budget} (in `prompt`: 'Item 1, bidding turn 1 of 3. Standing bid 0, leader seat 0 (0 = none). Answer 0 to pass, o'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: it plays, but part of it does nothing: game attribute `value_set` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
