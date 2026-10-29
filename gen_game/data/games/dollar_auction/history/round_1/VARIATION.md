# Variation: Collector's Dollar Auction

Four players with hidden collector types contest 8 alternating Red and Blue prizes. Each prize goes through a sealed opening bid and up to two escalation raises between the leaders. Everyone pays what they bid, so bidding wars enrich the bystanders.

Players: 4 to 4, best with 4

## Review of the original

Shubik's dollar auction: two players take turns raising bids for a $1 bill. The highest bidder gets the dollar, and both the highest and second-highest bidders pay their bids. Because what is already spent is lost either way, bidding often escalates past the prize's value.

- **non_degenerate**: bad. Under 'higher total wins' with two players, only the difference counts. The final high bidder ends 1 - b1 and the other ends -b2. The difference is 1 - (b1 - b2), which is positive whenever the increment is below 1. So whoever holds the high bid when the auction stops always wins. 'Never drop out' cannot lose: it either wins or the auction never ends. Dropping out is always a loss, so there is no real choice.
- **skill_sensitive**: bad. With the winner rule, the only sensible move is to keep raising, so a skilled player cannot outplay an unskilled one. The result depends on who blinks or on an arbitrary turn limit.
- **headroom**: bad. Once 'never drop' is seen, the game is solved. There is no deeper plan to discover and nothing to improve on.
- **reasoning_dependent**: weak. Information is perfect: the current bid and the high bidder are public, and the prize value is common. In the money version the interesting reasoning is the sunk-cost trap and guessing the opponent's resolve. Under the winner rule even that disappears, and nothing is hidden.
- **verifiable**: good. Payoffs are simple arithmetic on bids and the prize.
- **fits_platform**: weak. It is text-only and arithmetic, but alternating raises have no fixed length, and the step list is flat and bounded. The auction could run forever under the winner rule.

## Problems

- P1: In a two-player 'higher total wins' contest the high bidder always ends ahead, so never dropping out cannot lose and the escalation choice is meaningless.
- P2: There is no hidden information: prize value, bids and leader are all public, so there is nothing to infer.
- P3: Open-ended alternating raises have no fixed length and do not fit a bounded, flat step list.
- P4: A single auction gives no multi-round planning and no budget management.
- P5: Two players means a bidding war only ever hurts the two people in it relative to each other. The real dollar-auction lesson, that the war enriches the bystanders, cannot appear.

## Changes

- Use exactly 4 players, with the highest final score (coins plus prize points) winning. (fixes: P1): Two players locked in a war both fall behind the two who stayed out. Escalating 'to win' the auction can now lose the game, which brings back the dollar auction's real trap.
- Make it a bystander game: every player pays whatever they bid (all-pay), and only the top bidder receives the prize. (fixes: P5): This keeps the original's 'losers pay too' and makes every coin spent a real cost against the players who did not spend.
- Give each player a hidden type, Red collector or Blue collector, with exactly two of each. Prizes alternate Red and Blue. A prize is worth 12 points to a matching player and 6 to the others. The points a winner earns are kept private. (fixes: P2): Players must infer who truly values the current prize and therefore who will fight hard. Every type faces exactly one same-type rival and an equal number of matching prizes, so the deal decides what to do, not who is ahead.
- Replace open-ended alternating raises with three fixed simultaneous stages per round: a sealed opening bid, then up to two raise stages open only to the leading contenders. Raising 0 means dropping out. (fixes: P3): This keeps the escalation dynamic, adding more on top of money already sunk while seeing the rival's commitment, inside a bounded number of steps.
- Play 8 rounds from a shared starting purse of 40 coins, with bids limited by coins in hand. (fixes: P4): Spending in one war reduces your power later. Players must choose which prizes to contest and track rivals' remaining coins.
- Add one simultaneous message each round before bidding. (fixes: P2): Players can claim types, bluff, or propose splitting prizes. Same-type rivals and the winner rule (only one player wins) keep their interests in conflict, so promises must be tested against the bids they produce.

## Kept from the original

- An auction for a prize where losing bidders still pay their bids.
- The escalation trap: raising on top of money already sunk to avoid losing it, sometimes past the prize's worth.
- Public bids and a visible leader during escalation, with each raise building on the previous commitment.
- Dropping out by declining to raise.

## The variation's rules

SETUP: There are exactly 4 players. Each starts with 40 coins (public) and 0 prize points (private). At the start, two players are secretly dealt the type Red and two the type Blue, uniformly at random. Each player knows only their own type. The game lasts 8 rounds. Odd rounds (1, 3, 5, 7) offer a Red prize and even rounds (2, 4, 6, 8) offer a Blue prize. A prize is worth 12 prize points to a player whose type matches its colour and 6 prize points to a player whose type does not. Coins and all bids are public. Prize points are private until the end.

EACH ROUND:
1. Announce the round number and the prize colour.
2. TALK: every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.
3. OPENING BID: every player at the same time secretly chooses a whole-number opening bid from 0 up to their current coins.
4. Reveal all opening bids. The CONTENDERS are every player whose opening bid is greater than 0 and at least as large as the second-highest opening bid (ties included). If only one player bid more than 0, that player is the sole contender. If nobody bid more than 0, there are no contenders.
5. RAISE 1: if there are at least two contenders, each contender at the same time chooses a whole-number raise from 0 up to (their current coins minus what they have already bid this round). A contender who raises 0 has dropped out and may not raise again this round.
6. Reveal all Raise 1 amounts and each player's running total bid.
7. RAISE 2: if at least two contenders raised more than 0 in Raise 1, each of those contenders at the same time chooses a further whole-number raise from 0 up to (current coins minus what they have already bid this round). Contenders who dropped out in Raise 1 add nothing.
8. Reveal Raise 2 amounts and final total bids. A player's total bid is their opening bid plus their raises.
9. The round winner is the single player with the highest total bid. If two or more players tie for the highest total bid, nobody wins the prize this round.
10. PAYMENT: every player, winner or not, loses coins equal to their total bid.
11. The round winner, if any, privately gains 12 prize points if the prize colour matches their type, otherwise 6. Everyone is told who won, but not how many points they gained.
12. Go to the next round. After round 8 the game ends.

END: Each player's final score is their coins plus their prize points. All scores and types are revealed.

Objective: The player with the highest final score (coins plus prize points) wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: Players weigh whether a prize is worth contesting. Their own type sets the value (12 or 6), and they read rivals' types from claims and bidding history: who bid big on Red rounds? The real conflict is between the two same-type players, who both want the same four prizes. Opposite-type players can try to split prizes peacefully, but each also wants to grab cheap off-colour prizes. Everyone wants the others to fight. Talk lets players claim a type to scare off rivals or to bluff. A player who simply follows a proposal such as 'I take Red, you stay out' can lose: the proposer may be a Blue type pocketing cheap points, or may stop holding back once the follower has stood aside. Escalation recreates the dollar auction. Once two contenders have sunk coins, raising again is tempting, but every coin spent in a war is a coin the two bystanders keep. Simple policies all lose. Always bidding 0 ends at 40 and loses to anyone who wins prizes cheaply. Always bidding high burns coins well past prize value and loses. Random bids overpay. No seat has an edge because all choices are simultaneous, and every type has exactly one rival and four matching prizes.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 8 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
