# Variation: War of Attrition Auctions

Three or four players fight six all-pay auctions from one 100-coin budget. Each auction has three rounds of sealed raises, and every bidder pays what they committed. Each player privately values each prize differently, so escalating against the wrong rival hands the game to whoever stayed out.

Players: 3 to 4, best with 3

## Review of the original

Shubik's dollar auction: two players take turns raising a public bid for a $1 prize by a minimum increment. The highest bidder wins the dollar and pays their bid, and the losing bidder also pays their last bid. The game is a classic escalation trap in which sunk costs push both players to bid past the prize's value.

- **non_degenerate**: bad. The platform only decides who wins. With two players, the auction winner nets 1 - b and the loser pays b - 0.05. The winner therefore always ends 0.95 ahead, whatever the bid level. Raising is always relatively better than dropping, so 'always raise' cannot lose, the auction never ends rationally, and dropping out always loses.
- **skill_sensitive**: bad. Under a who-ends-higher rule the outcome is decided by who refuses to stop, or by a tie-breaking cap. Absolute payoffs, where real skill (not entering, or stopping early) lives, are invisible to the winner rule.
- **headroom**: bad. It is a single one-shot event with an obvious relative strategy (never yield). There is nothing to improve beyond that.
- **reasoning_dependent**: weak. Information is perfect: the bid and the high bidder are public, and the prize value is common knowledge. The only inference is guessing the opponent's resolve, and the winner rule makes resolve infinite.
- **verifiable**: good. Payoffs are pure arithmetic on bids.
- **fits_platform**: weak. Turn-based and text-only, but the alternating open-ended raise loop has no fixed length. That needs unbounded repetition, which the flat step list handles poorly.

## Problems

- In a two-player highest-total game, winning the auction always beats losing it by 0.95 regardless of price, so 'always raise' cannot lose and escalation is unbounded.
- Perfect information: there is no hidden state to infer, only an unbounded test of will.
- A single one-shot auction gives no planning over several rounds and no budget trade-offs.
- The open-ended alternating raise loop has no fixed number of steps, which the flat step list cannot build cleanly.
- Skill at the game, knowing when to stay out or stop, is not rewarded by a who-ends-higher rule with two players.

## Changes

- Three or four players instead of two. (fixes: In a two-player highest-total game, winning the auction always beats losing it by 0.95 regardless of price, so 'always raise' cannot lose and escalation is unbounded.): Two bidders locked in an escalation war both bleed coins while a bystander who stayed out pulls ahead. Escalation becomes genuinely costly under a highest-total rule, which restores the trap's meaning.
- A series of 6 auctions funded from one budget of 100 coins per player. Final score is coins left plus the value of prizes won. (fixes: A single one-shot auction gives no planning over several rounds and no budget trade-offs.): Coins spent fighting in one auction are unavailable later, so players must plan across rounds and pick their battles.
- Each player is secretly dealt their own random order of prize values: the six numbers 10, 15, 20, 25, 30 and 40, one per auction. Everyone's list totals 140. (fixes: Perfect information: there is no hidden state to infer, only an unbounded test of will.): This is one hidden element. Players must infer from bidding behaviour which auctions rivals value highly. Because every list has the same total, the deal changes what to do, not who is ahead.
- Each auction is played as exactly 3 simultaneous raise stages, with cumulative bids revealed after each stage. All players pay their full cumulative bid (all-pay, as in the original), and the sole highest bidder takes the prize. (fixes: The open-ended alternating raise loop has no fixed number of steps, which the flat step list cannot build cleanly.): This keeps the dollar auction's escalation and sunk-cost pressure: after stage 1 you see you are behind and must decide whether to throw more in. The length is fixed and buildable.
- A tie for the highest cumulative bid leaves the prize unclaimed, though everyone still pays. The winner is whoever has the highest final score. (fixes: Skill at the game, knowing when to stay out or stop, is not rewarded by a who-ends-higher rule with two players.): Matching bids is punished rather than rewarded. Restraint (staying out, stopping early) shows up directly in the score, and with three or more players a fighter's loss is the bystander's gain.
- A simultaneous one-message talk phase before each auction. (fixes: Perfect information: there is no hidden state to infer, only an unbounded test of will.): Players have opposed interests: only one can win, and values are private. Talk enables bluffing about values, proposing bid rings ('you take this one, I take the next'), and testing whether such promises are kept. All of this is non-binding.

## Kept from the original

- Ascending bidding for a prize in which losing bidders also pay what they bid.
- The escalation and sunk-cost trap: seeing you are behind, with coins already committed, tempts you to raise past the prize's worth.
- Public visibility of the current bids during the auction.
- The core lesson that the best move is often not to enter, or to stop early.

## The variation's rules

SETUP: Each player starts with 100 coins. Each player is secretly dealt a random ordering of the six prize values 10, 15, 20, 25, 30 and 40, one value for each of auctions 1 to 6. A player sees only their own list, so every player's six values total 140. Coin totals are public; prize values are private.

The game has 6 auctions (rounds). Each auction proceeds as follows.

1. Announce the auction number.

2. TALK: Every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding: players may claim values, propose who takes which auction, or bluff.

3. RAISE STAGE 1: At the same time, each player secretly chooses a raise, a whole number from 0 up to their available coins. Available coins are coins held minus everything they have already committed in this auction. Each player's committed bid for this auction becomes the sum of their raises so far. All committed bids are then announced.

4. RAISE STAGE 2: Same as stage 1. Committed bids are announced again.

5. RAISE STAGE 3: Same as stage 1. Final committed bids are announced.

6. RESOLUTION: Every player pays their full committed bid, which is subtracted from their coins, whether or not they win. If exactly one player has the highest committed bid and it is at least 1, that player wins the prize and adds their OWN private value for this auction to their prize points. The value is not revealed to others. If two or more players tie for the highest bid, or all bids are 0, nobody wins the prize.

7. Announce who (if anyone) won and everyone's remaining coins. Committed bids reset to 0 for the next auction.

END: After auction 6, each player's final score is coins remaining plus prize points. All private value lists are then revealed.

Objective: The player with the highest final score (coins remaining plus prize points) wins. If two or more players tie for the highest final score, the game is a draw.

Expected effect: Simple policies all lose. Never bidding scores exactly 100, which loses to anyone who wins a single prize for less than its value. Going all-in early wins at most one prize worth 40 and finishes with at most 40 points. Any fixed bid can be topped by one coin. Good play means reading which auctions rivals value highly from their stage-1 bids and their talk, then fighting only where your value is high and theirs seems low. It also means cutting losses mid-auction rather than escalating, and remembering that two fighters both lose ground to the bystander. Players disagree on everything: there is one winner, and the values are private. A player who simply follows a proposed rotation ('you take auction 3, I take 4') can be undercut by a rival who breaks the deal on a prize they value at 40, or can give away their own best prize. Talk therefore rewards reading credibility, not just agreeing. Because every value list totals 140, good play rather than the deal decides the winner.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
