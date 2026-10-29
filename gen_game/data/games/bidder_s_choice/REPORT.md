# bidder_s_choice: ready for review

Built from the variation **Bidder's Choice: Sealed Pool** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Every player starts with 20 coins. Final score is coins left plus own values of objects held. The highest score wins and a shared top score is a draw. (fixes: P1): Unspent coins count, so overpaying loses. Bidding 0 forever also loses to anyone who buys a 14-value object for a few coins. Bidding all 20 coins in round 1 yields at most 14 and loses to players who keep their 20.
- Each player receives the same six values (2, 4, 6, 8, 10, 14) in an independent random order. Every player's values total 44. (fixes: P2): The deal changes which objects a player wants and whom he competes with, not how much he can be worth. Good play decides the winner.
- Ties on the highest bid go to the tied player holding the fewest objects. If they are still tied, there is no sale that round. (fixes: P3): This gives a deterministic, arithmetic tie rule. It also makes everyone bidding 0 a stalemate rather than a free win.
- Pick default: if the winner names no object still in the pool, or gives no answer, he receives the remaining object with the highest of his own values. Ties go to the earliest letter, though they cannot occur since his values are distinct. (fixes: P4): Every pick outcome is now defined, so the engine and the players can always resolve it.
- Talk messages are limited to 40 words. Any words beyond the 40th are dropped before the messages are shown. (fixes: P5): A concrete, checkable limit.
- Players are set at 3 to 5, with 3 suggested. A bid that is not a whole number from 0 to the player's current coins counts as 0. (fixes: P6): With three or more players, rings and rotations proposed in talk can betray the follower. Six objects cover up to five players, and every bid input has a defined result.

Objective: The player with the highest final score (coins left plus the sum of his own values for the objects he holds) wins. If two or more players share the highest final score, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Value of winning a round: the winner picks his own best remaining object. In round 1 that is worth exactly 14 to every player, because each player's values are a permutation of {2,4,6,8,10,14}. Start is 20 coins, so a player who never wins ends at exactly 20. A winner's net gain is (value picked - b
- playable: pass. Rules are complete.
- Invalid bids count as 0.
- The tie chain is: highest bid, then fewest holdings, then no sale.
- An invalid pick defaults to the winner's own top remaining value, with ties broken by earliest letter.
- Leftover objects are discarded.
- Score is coins plus own values. A tie for t
- reasoning_over_luck: pass. The deal gives everyone the same multiset of values. Chance enters only through collisions: an opponent taking the object you value at 14 or 10, about 1/6 per opposing win for your top object. That typically costs at most 4 points (14 to 10). Picks are your own top, so the deal is largely symmetric.

## Complexity

- steps_per_round: designed 13, built 13, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 16, built 37, limit 20 (built: 80)
- hidden_elements: designed 2, built 12, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 6, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 20 coins each, no holdings, full pool, round 0
- pass: Dealt values total 44 whatever the permutation: holding all six objects scores coins + 44
- pass: A round begins: the round number advances to 1
- pass: After the talk, every player is still asked for a sealed bid
- pass: The bid range runs from 0 to the bidder's current coins
- pass: An over-coins bid cannot be made: seat 1 falls to the default bid of 0 and seat 2 wins with a bid of 1
- pass: The strictly highest bid wins the round
- pass: Tied highest bid: the bidder with fewer objects wins
- pass: Tie on both bid and object count: no sale, nobody pays, the pool is unchanged
- pass: The winner pays his bid: 12 coins minus a bid of 5 leaves 7
- pass: The named object leaves the pool and joins the winner's holdings
- pass: Unscripted pick: the winner gets A, his highest-valued object
- pass: A player who already holds objects can win again
- pass: At round end the winner's seat is announced
- pass: After round 6 the game ends and leftover pool objects are discarded
- pass: Final score is coins plus the player's own values of the objects he holds
- pass: A shared highest score is a shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 10, 'seat 2': 7, 'seat 1': 16, 'seats 2 and 5': 1, 'seat 5': 3, 'seat 4': 2, 'seats 2 and 3': 1}, 40-65 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 53.0 decisions, prompts of 233 characters on average (longest 261)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 20, 'seat 2': 16, 'seat 1': 22, 'seats 1 and 2': 2}
- always `first@seat1`: won 25, lost 32, drew 3
- always `first@seat2`: won 23, lost 32, drew 5
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 2, lost 57, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: Each failure says a scripted pick ('A' or 'F') was never offered to a particular seat. That happens when the test assumes that seat wins a round whose winner is really decided by chance (an equal-count tie broken at random) or by other seats' default bids. The single-round test where seat 1 clearly outbids and picks 'A' passes, so bidding, paying and picking are implemented.
- round 1: fix_game: The game file is broken. It stops after round 1, leaving the pool at B–F, the round at 1 and final scores unset, and it changes coins outside the payment step. Seats 1 and 2 lost coins (20→5 and 20→0) without winning or paying anything. The tests are correct and simply never got the later rounds or bids they expected.
- round 1: fix_tests: In a full tie the round winner is chosen at random, so seat 1 may not win and may never be offered a pick. The test still scripts seat 1 to pick 'A' and fails when that pick never happens. The test is depending on the outcome of the random tie-break, which the rules leave to chance.

## Choices the rules did not make

- 3 to 5 players, suggested 3: The designer suggests 3, which is kept. 3 is the minimum where the fewest-objects tie-break and rival bidding create real competition. Above 5, there is less than one object per player and the talk grows long.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous talk. Players disagree because their private values differ, so bluffing about which object one wants, or about intending to sit out, can steer rivals' bids.
- Tie-break encoded as bid_key = bid * 10 + (6 - holdings_count): Holdings never exceed 6, so this single number orders players by bid first and then by fewest objects. A tie in bid_key at the top is exactly the no-sale case.
- Values stored as six ally attributes value_a through value_f, dealt by drawing from each player's own value_bag list: This gives each player an independent random permutation, as the rules require, and declares the dealing source as state.
- bid_key is an ally player attribute: It is a scratch number derived from the player's own bid, so only the owner may see it until bids are revealed.
- Score computed only after round 6: A public running score would leak private values.
- Strategy note: A thoughtful player bids up only for his high-value objects, shades bids against rivals' remaining coins, uses holding few objects as a tie-break edge, and bluffs in talk. A thoughtless one overpays for low-value objects.

## Simplifications

- A draw at the top is represented as a shared win among the tied players: The engine has no separate draw; players level at the top share the win.
- The pick is offered as a choice from the current pool, so an invalid letter cannot be chosen; the fallback applies only when there is no answer: Choice lists come from the pool list. The source's fallback rule is still kept.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'you.coins >= you.bid' reads `you` where there is no player
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (fallback_pick, message, message, message) in `your_private_values`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
