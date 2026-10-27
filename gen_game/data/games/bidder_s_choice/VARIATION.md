# Variation: Bidder's Choice: Sealed Pool

Three to five players with 20 coins each bid over six rounds for six objects. Every player privately values the objects at 2, 4, 6, 8, 10 and 14 in his own random order. Each round, the highest sealed bidder pays his bid and picks an object. Final score is coins left plus own values of objects held, and the highest score wins.

Players: 3 to 5, best with 3

## Review of the original

Bidder's Choice is a sequential sealed-bid auction. Each round every bidder submits a sealed bid, the highest bidder pays his bid and picks one object from a shrinking pool, and payoff is the sum of the bidder's private values for the objects he took minus what he paid.

- **non_degenerate**: weak. With no budget and payoff-only scoring, bidding 0 can never lose money. Under a 'higher total wins' rule, a player who bids 0 forever scores 0 and draws or beats anyone who overpays. Seats are symmetric, but the original gives no budget, value distribution, tie rule or winner rule, so simple policies are not clearly beatable.
- **skill_sensitive**: weak. Shading a bid, reading rivals' values from what they pick, and timing when to win all reward skill. However, the original lets valuations be arbitrary. If one bidder is dealt much higher values, the deal decides the game.
- **headroom**: good. Optimal bidding in a multi-round auction with private values is hard. It involves bid shading, saving budget for later rounds, and inferring rivals' preferences from their picks. A weak player can still score by winning one cheap round.
- **reasoning_dependent**: good. Valuations are private and bids are sealed. Each pick reveals something about the winner's values, which lets others infer who will contest which object in later rounds.
- **verifiable**: good. Payoff is values minus bids, which is pure arithmetic. No judge is needed.
- **fits_platform**: weak. The game is turn-based and text-only with no board. But the original lacks a budget, a value distribution, a tie rule and a winner rule. The previous variation supplied these but left an invalid pick undefined and gave no word limit for talk messages.

## Problems

- P1: The original has no budget and no winner rule. With 'higher payoff wins' and no cost to abstaining, bidding 0 cannot lose.
- P2: Arbitrary private valuations let the deal decide the winner (lottery trap).
- P3: There is no rule for tied bids.
- P4 (previous variation): Rule 7 has no default for a missing or invalid pick, such as naming an object not in the pool or giving no answer. A model cannot resolve that case.
- P5 (previous variation): The talk phase says 'one short message' but gives no concrete length limit.
- P6 (previous variation): The player count, and what counts as an invalid bid, were not stated precisely.

## Changes

- Every player starts with 20 coins. Final score is coins left plus own values of objects held. The highest score wins and a shared top score is a draw. (fixes: P1): Unspent coins count, so overpaying loses. Bidding 0 forever also loses to anyone who buys a 14-value object for a few coins. Bidding all 20 coins in round 1 yields at most 14 and loses to players who keep their 20.
- Each player receives the same six values (2, 4, 6, 8, 10, 14) in an independent random order. Every player's values total 44. (fixes: P2): The deal changes which objects a player wants and whom he competes with, not how much he can be worth. Good play decides the winner.
- Ties on the highest bid go to the tied player holding the fewest objects. If they are still tied, there is no sale that round. (fixes: P3): This gives a deterministic, arithmetic tie rule. It also makes everyone bidding 0 a stalemate rather than a free win.
- Pick default: if the winner names no object still in the pool, or gives no answer, he receives the remaining object with the highest of his own values. Ties go to the earliest letter, though they cannot occur since his values are distinct. (fixes: P4): Every pick outcome is now defined, so the engine and the players can always resolve it.
- Talk messages are limited to 40 words. Any words beyond the 40th are dropped before the messages are shown. (fixes: P5): A concrete, checkable limit.
- Players are set at 3 to 5, with 3 suggested. A bid that is not a whole number from 0 to the player's current coins counts as 0. (fixes: P6): With three or more players, rings and rotations proposed in talk can betray the follower. Six objects cover up to five players, and every bid input has a defined result.

## Kept from the original

- Sealed simultaneous bids each round, with the highest bidder paying his own bid.
- The winner of a round chooses which object to take from a shrinking pool.
- Private valuations per object.
- One round per object, and a player may win several rounds.
- Score is the value of objects taken, with money spent counting against the player.

## The variation's rules

SETUP.
1) There are 3 to 5 players. Every player starts with 20 coins and no objects. The pool holds six objects: A, B, C, D, E, F.
2) Each player privately receives the six values 2, 4, 6, 8, 10 and 14, one value per object, in an independent random order for each player. Every player's values therefore total 44. A player sees only his own values.

ROUNDS. The game lasts exactly 6 rounds. Each round:
3) ANNOUNCE. The round number, the objects still in the pool, every player's coins and every player's holdings are shown to all.
4) TALK. Every player writes one message of at most 40 words at the same time, without seeing the others. Any words beyond the 40th are dropped. Then all messages are shown to everyone. Messages are not binding and may be false.
5) BID. Every player at the same time submits a sealed bid: a whole number from 0 up to his current coins. A bid that is missing, not a whole number, negative, or above his current coins counts as 0.
6) WINNER. The highest bid wins. If several players share the highest bid, the one among them holding the fewest objects wins. If several of those also hold equally few objects, there is NO SALE this round: nobody pays, no object leaves the pool, and the round still counts as played.
7) PAY AND PICK. If there is a winner, he pays his bid, so his coins decrease by his bid. He then names one object still in the pool. That object leaves the pool and is added to his holdings. If he names no object still in the pool, or gives no answer, he receives instead the remaining object with the highest of his own values (ties: earliest letter). A player may win any number of rounds.
8) REVEAL. All bids, the winner (or 'no sale') and the object taken are announced to all.

END.
9) After round 6, any objects still in the pool are discarded.
10) Each player's final score = his remaining coins + the sum of HIS OWN values for the objects he holds. All values are then revealed.

Objective: The player with the highest final score (coins left plus the sum of his own values for the objects he holds) wins. If two or more players share the highest final score, the game is a draw.

Expected effect: Players must judge how much each object is worth to them against coins, which count fully at the end. They must also infer from others' picks and bids which objects rivals value, and so when a cheap win is possible. Spending everything early is punished, and so is never bidding: always-0 loses to anyone who buys a 14 for 1 coin, and always-max ends with at most 14 against 20. Talk earns its place because players disagree about who gets the scarce cheap wins. A proposed ring ('everyone bid 0 except a rotation') can be exploited by a defector who bids 1 and takes the best object. A player who simply follows a rotation can find that others have taken his high-value objects, or that he paid more than others for less. Only one player can win, so every proposal benefits its proposer.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
