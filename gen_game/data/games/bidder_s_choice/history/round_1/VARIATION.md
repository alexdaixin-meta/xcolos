# Variation: Bidder's Choice: Shared Worth

Players bid sealed coins from a fixed budget for the right to pick one of six objects. Each player privately values the objects with a shuffled copy of the same six values. Coins kept and object values both count.

Players: 3 to 5, best with 4

## Review of the original

Bidder's Choice is a sequential sealed-bid auction for the right to choose. Each round the highest bidder pays his bid and picks one object from a shrinking pool. Payoff is the value of the objects taken minus the bids paid, and each bidder has private valuations for every object.

- **non_degenerate**: weak. There is no budget, so a player can overbid without limit and only loses payoff. Bidding 0 always guarantees a score of 0, which beats any player who ends negative. Tie handling is unspecified, and how a tie is resolved can give one seat an edge. Choices do matter, though: bid size, timing and which object to pick all change the outcome.
- **skill_sensitive**: weak. Valuations are independent and private with no stated distribution. One bidder can be dealt far higher values than the others and win under a highest-total rule whatever anyone does. Skill in bid shading and timing exists but can be swamped by the deal.
- **headroom**: good. Deciding when to fight for a round and when to wait for a cheaper one, and reading what rivals want from their picks, is open-ended. A weak player still collects some objects.
- **reasoning_dependent**: good. Valuations are hidden. Players must infer rivals' preferences from bids and picks, and plan across rounds because the pool shrinks.
- **verifiable**: good. Payoff is the sum of values minus the sum of bids, which is pure arithmetic.
- **fits_platform**: weak. It is turn-based and text-only with no board, and it uses sealed bids and a sequential pick. However, the valuation distribution, the tie rule and any bid limit are missing, so it cannot be built as written.

## Problems

- Independent private valuations with no stated distribution create a lottery: whoever is dealt bigger values wins under a highest-total rule.
- There is no budget, so nothing links rounds through a scarce resource, and overbidding has no cap beyond a negative score.
- Tie-breaking for the high bid is unspecified, and a seat-order tie-break would give a built-in edge.
- The valuation range, number of objects and bid limits are unstated, so the game cannot be built or balanced.
- No winner rule is stated, and with a payoff that can go negative, always bidding 0 can be hard to beat against reckless rivals.

## Changes

- Every player's private valuations are a random shuffle of the same six values {2, 4, 6, 8, 10, 14} across the six objects. (fixes: Independent private valuations with no stated distribution create a lottery: whoever is dealt bigger values wins under a highest-total rule.): Everyone holds the same total worth, so the deal changes only what each player wants, not who is richer. Rivals' preferences stay hidden and worth inferring.
- Each player starts with 20 coins. Bids are whole numbers from 0 up to the coins still held. Unspent coins count toward the final score. (fixes: There is no budget, so nothing links rounds through a scarce resource, and overbidding has no cap beyond a negative score.): Coins become a scarce resource across rounds, so spending heavily early limits later rounds and every coin bid is a real cost. Overbidding is capped.
- Tied high bids go to the tied player holding the fewest objects. If they are still tied, a random draw among them decides. (fixes: Tie-breaking for the high bid is unspecified, and a seat-order tie-break would give a built-in edge.): No seat order is used, and the tie-break slightly favours players who are behind in objects.
- The game is fixed at 3 to 5 players (4 suggested), 6 objects and 6 rounds, with all numbers stated. (fixes: The valuation range, number of objects and bid limits are unstated, so the game cannot be built or balanced.): This makes the game buildable and keeps it short.
- Final score is coins left plus the values of objects taken. The highest score wins, and a tie for highest is a draw. (fixes: No winner rule is stated, and with a payoff that can go negative, always bidding 0 can be hard to beat against reckless rivals.): Bidding 0 always keeps 20 coins, but a rival who pays 5 for an object worth 14 to them reaches 29, so passivity loses. Bidding everything for one object leaves at most about 14. Every simple policy can lose.
- Each round opens with one simultaneous short public message from every player, before bidding. (fixes: Independent private valuations with no stated distribution create a lottery: whoever is dealt bigger values wins under a highest-total rule.): Players can claim or bluff which objects they want, to steer rivals away or provoke them into overpaying. This gives a further layer of inference.

## Kept from the original

- Sealed first-price bids each round for the right to pick, not for a fixed object.
- The round winner chooses one object from a shrinking pool, and the others pay nothing.
- Private valuations per object.
- A player may win several rounds.
- One round per object.

## The variation's rules

SETUP
1. There are six objects, named A, B, C, D, E and F.
2. Each player starts with 20 coins.
3. Each player is privately dealt a random assignment of the values 2, 4, 6, 8, 10 and 14 to the six objects, one value per object, independently of the other players. Each player sees only their own assignment. Every player's values therefore total 44.

ROUNDS
The game lasts exactly 6 rounds. Each round:
1. TALK. Every player writes one short public message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding and may be false.
2. BID. Every player at the same moment submits a sealed bid. A bid is a whole number from 0 up to the coins that player currently holds.
3. RESOLVE. The highest bid wins the round. If several players tie for highest, the tied player holding the fewest objects wins. If they are still tied, one of them is chosen at random with equal chance.
4. PAY. The round winner pays their bid: it is subtracted from their coins and leaves the game. All other players pay nothing.
5. PICK. The round winner chooses one object still in the pool. That object is removed from the pool and added to the winner's holdings, and they gain their own private value for it. A player may win any number of rounds.
6. ANNOUNCE. Everyone is told all bids, who won, the price paid and which object was taken. Private values are never revealed.

END
After round 6 all six objects have been taken. Each player's final score is their remaining coins plus the sum of their own private values for the objects they hold. All values are then revealed.

Objective: The player with the highest final score (remaining coins plus their own values for the objects they hold) wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: Because every player holds the same total worth, the winner is whoever converts coins to value most efficiently. That means paying little for objects they value highly, and waiting when an object they want is not wanted by others. Players must infer rivals' hidden preferences from picks, bid sizes and talk, and plan their 20-coin budget across six rounds. Talk passes both tests. Players disagree about who gets the right to pick and at what price, and only one player can win. A player who believes a rival's claim ('I only want C, leave the bidding to me') and stops bidding may watch that rival take the object they themselves valued at 14 cheaply, and lose. Bluffs and tests of claims against later picks give the talk real content. Always bidding 0 ends with 20 points against rivals near 30. Always bidding everything ends near 14. Matching rivals' bids invites overpayment. No simple policy is safe.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 9 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
