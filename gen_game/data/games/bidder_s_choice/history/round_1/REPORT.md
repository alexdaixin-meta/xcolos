# bidder_s_choice: needs review

Built from the variation **Bidder's Choice: Shared Worth** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Every player's private valuations are a random shuffle of the same six values {2, 4, 6, 8, 10, 14} across the six objects. (fixes: Independent private valuations with no stated distribution create a lottery: whoever is dealt bigger values wins under a highest-total rule.): Everyone holds the same total worth, so the deal changes only what each player wants, not who is richer. Rivals' preferences stay hidden and worth inferring.
- Each player starts with 20 coins. Bids are whole numbers from 0 up to the coins still held. Unspent coins count toward the final score. (fixes: There is no budget, so nothing links rounds through a scarce resource, and overbidding has no cap beyond a negative score.): Coins become a scarce resource across rounds, so spending heavily early limits later rounds and every coin bid is a real cost. Overbidding is capped.
- Tied high bids go to the tied player holding the fewest objects. If they are still tied, a random draw among them decides. (fixes: Tie-breaking for the high bid is unspecified, and a seat-order tie-break would give a built-in edge.): No seat order is used, and the tie-break slightly favours players who are behind in objects.
- The game is fixed at 3 to 5 players (4 suggested), 6 objects and 6 rounds, with all numbers stated. (fixes: The valuation range, number of objects and bid limits are unstated, so the game cannot be built or balanced.): This makes the game buildable and keeps it short.
- Final score is coins left plus the values of objects taken. The highest score wins, and a tie for highest is a draw. (fixes: No winner rule is stated, and with a payoff that can go negative, always bidding 0 can be hard to beat against reckless rivals.): Bidding 0 always keeps 20 coins, but a rival who pays 5 for an object worth 14 to them reaches 29, so passivity loses. Bidding everything for one object leaves at most about 14. Every simple policy can lose.
- Each round opens with one simultaneous short public message from every player, before bidding. (fixes: Independent private valuations with no stated distribution create a lottery: whoever is dealt bigger values wins under a highest-total rule.): Players can claim or bluff which objects they want, to steer rivals away or provoke them into overpaying. This gives a further layer of inference.

Objective: The player with the highest final score (remaining coins plus their own values for the objects they hold) wins. If two or more players tie for the highest score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. WHAT A ROUND IS WORTH: if you win at bid b and pick an object you value v, your score changes by v-b and nobody else's changes. Your best remaining object is always worth at least 2, and early on usually 10 or 14. Each player holds 44 in values against 20 coins, so items are underpriced relative to 
- playable: pass. COMPLETENESS:
- Every situation is covered: bid range 0..coins, resolution of ties, the winner must pick a remaining object, the announce step, scoring and a draw on a tied top score.
- A 0 bid can win if it is the highest.
- A broke player bids 0.
- The game is finite: exactly 6 rounds and 6 object
- reasoning_over_luck: pass. CHANCE SOURCES:
(1) Whether your high values coincide with others' high values. If your 10 is everyone else's 2, you can buy it late and cheaply. P(all three players' 14s on distinct objects) = 120/216 ≈ 0.56.
(2) The random tie lottery. It mostly matters in late rounds when several players are brok

## Complexity

- steps_per_round: designed 10, built 10, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 9, built 28, limit 20 (built: 80)
- hidden_elements: designed 1, built 4, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 20 coins each, no objects, full pool, round 0
- pass: Dealt values total 44: seat 1 takes all six objects for 1 coin each and scores 14+44 (chance-free)
- pass: Values stay private mid-game: no final score is set after round 1
- pass: A round with the talk poll then the bid resolves normally
- pass: Bids range from 0 to the seat's current coins
- pass: Strictly highest bid wins the round
- pass: Tie on top bid goes to the tied seat with fewer objects
- FAIL: Full tie broken at random: only chance-free facts (one object taken, price 5, the third seat untouched) | rule R8 is broken: When tied players also hold equally few objects, then the winner is chosen at random among them with equal chance.; Ada: the rule for 'A' was never matched (the game never put that option to this seat)
- pass: Winner pays its bid; losing bidders pay nothing
- pass: Winner picks only from the pool; the object moves to its holdings
- pass: Same seat can win consecutive rounds
- pass: All bids, winner, price and object are announced
- pass: Round 6 ends the game with the pool empty and final scores set
- pass: Final score is coins + object_points; level top scores share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 1': 13, 'seat 2': 9, 'seat 3': 10, 'seats 3 and 5': 1, 'seats 1 and 2': 1, 'seats 2 and 5': 1, 'seat 5': 2, 'seat 4': 2, 'seats 2 and 3': 1}, 41-65 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 54.0 decisions, prompts of 202 characters on average (longest 236)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 20, 'seat 2': 19, 'seat 3': 20, 'seats 1 and 2': 1}
- always `first@seat1`: won 29, lost 31, drew 0
- always `first@seat2`: won 21, lost 34, drew 5
- always `last@seat1`: won 3, lost 56, drew 1
- always `last@seat2`: won 3, lost 56, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: Each failure says a scripted pick ('A' or 'F') was never offered to a particular seat. That happens when the test assumes that seat wins a round whose winner is really decided by chance (an equal-count tie broken at random) or by other seats' default bids. The single-round test where seat 1 clearly outbids and picks 'A' passes, so bidding, paying and picking are implemented.
- round 1: fix_game: The game file is broken. It stops after round 1, leaving the pool at B–F, the round at 1 and final scores unset, and it changes coins outside the payment step. Seats 1 and 2 lost coins (20→5 and 20→0) without winning or paying anything. The tests are correct and simply never got the later rounds or bids they expected.
- round 1: fix_tests: In a full tie the round winner is chosen at random, so seat 1 may not win and may never be offered a pick. The test still scripts seat 1 to pick 'A' and fails when that pick never happens. The test is depending on the outcome of the random tie-break, which the rules leave to chance.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4, so it is kept as suggested. Fewer than 3 leaves only one rival, so there is no real auction or tie-breaking pressure. More than 5 makes six objects too scarce for one bid to matter and makes the talk long.
- Keep the simultaneous talk poll before each bid: The source specifies it. Players' values differ, so they disagree about which objects are worth fighting for. Talk lets them bluff about their values or about intentions to stay out, which can steer rivals' bids.
- Store private values as a 6-entry list ordered A to F: This lets the pick add the value by position arithmetically.
- Keep a public last_bid beside the hidden bid: Bids are sealed during the poll but must all be announced afterwards.
- Players can see their own strategy points: The source says the player sees their own assignment. Showing them their running sum of held values is just derived from that.

## Simplifications

- A draw is represented as a shared win among the players tied at the top: The engine has no separate draw; tied top players share the win, which matches a draw between them.
- The final value reveal is done by an update step conditioned on round == 6, inside the round: The step list repeats each round; a condition on a single step avoids needing a separate end block.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'you.coins >= price' reads `you` where there is no player
- 2: it plays, but part of it does nothing: game attribute `object_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
