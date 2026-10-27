# Variation: Escalation Auction

Three to five players with 100 coins each bid in six all-pay auctions. Each auction has three sealed raise stages, and committed bids are revealed after each stage. Each player privately values each prize differently, so they must read rivals' values from talk and bids and spend their budget wisely.

Players: 3 to 5, best with 3

## Review of the original

The dollar auction: two players take turns raising an open bid for a $1 bill by at least $0.05. When one drops out, the high bidder pays their bid and takes the dollar, and the runner-up pays their bid and gets nothing, so sunk costs push bids past the prize's value.

- **non_degenerate**: bad. With two players and 'higher total wins', only the difference matters. Opening at $0.05 and dropping out at once wins or draws against a bidder who also drops. Once escalation starts, the player willing to go further always wins the difference, so the game becomes a pure war of attrition where never yielding cannot lose. The first bidder also holds a built-in turn-order position.
- **skill_sensitive**: weak. There is no luck, but nothing to out-think either: the prize is common and known, and both players see every bid. The outcome depends on stubbornness, not insight.
- **headroom**: weak. One auction for one known prize. The analysis ends with 'bid once or escalate forever', and there is no repeated structure to learn from.
- **reasoning_dependent**: bad. It is a perfect-information game: the prize value, every bid and the high bidder are all public. Nothing is hidden to infer.
- **verifiable**: good. Payoffs are pure arithmetic on bids: 1 - bid for the winner and -bid for the others.
- **fits_platform**: weak. It is text-only and arithmetic. However, alternating raises with no cap can run for an unbounded number of turns, and dropping out is a sequential sub-loop of variable length.

## Problems

- P1: Two-player 'higher total wins' reduces the game to a war of attrition in which refusing to yield, or never bidding, cannot lose.
- P2: Perfect information. The prize value and all bids are public, so there is nothing to infer about opponents.
- P3: A single auction gives no multi-round planning and no budget trade-offs.
- P4: Alternating unbounded raises cannot be built as a fixed flat step list, and they give the first bidder a positional edge.
- P5 (previous build): the raise poll's option range read a scratch attribute (raise/stage_raise) that stayed 0. Every seat was offered only 0, committed never grew, and coins never fell (tests R5 to R8 failed).
- P6 (previous build): too many redundant parameter attributes (prize_value_1..6, prize_value_total) alongside scratch attributes, which wasted the attribute budget and invited wrong references.

## Changes

- Three to five players, with the winner decided by the highest final score (coins left plus prize points). (fixes: P1): One rival's gain is not every other's loss, and a player who sits out every auction is overtaken by anyone who wins a prize cheaply.
- Each player privately holds a value list: a random order of [10, 15, 20, 25, 30, 40], one value per auction. Only the owner sees it. (fixes: P2): Each player must infer from bids and talk who values the current prize highly. Every list has the same total of 140, so the deal changes what to do, not who is ahead.
- Six auctions drawn from one budget of 100 coins. (fixes: P3): Players must plan when to spend: whether to chase their 40-auction or win cheap prizes others ignore. They can also read opponents' remaining budgets.
- Each auction has exactly three simultaneous sealed raise stages. Committed bids are announced after each stage, and it is all-pay: everyone pays their committed total. (fixes: P4): This keeps the dollar auction's sunk-cost escalation in a fixed, buildable number of steps with no seat order.
- Ties at the top bid produce no winner, though everyone still pays. (fixes: P1): Matching an opponent is not safe, so the 'can't lose' option disappears.
- The raise poll's options are every whole number from 0 to (that player's coins − that player's committed), read live from those two player attributes at that moment. The chosen raise is added straight to committed. There are no scratch raise/stage_raise attributes. (fixes: P5): This removes the source of the 0-only option range, so bids accumulate and coins are deducted at resolution.
- Only the parameters actually used are kept as attributes (starting_coins, auctions, raise_stages, min_winning_bid, prize_deck). prize_value_1..6 and prize_value_total are dropped. (fixes: P6): This keeps the attribute count small and stops references to stale values.
- A simultaneous one-message talk phase before the first raise stage of each auction. (fixes: P2): Only one player can win each auction, so players disagree. They can bluff a high value to scare others off or feign disinterest, and listeners must judge it against bidding behaviour.

## Kept from the original

- Bidding for a prize where losing bidders still pay their bids (all-pay).
- Escalation through repeated raises on top of what you have already committed, with sunk-cost pressure.
- Public committed bids after each raise, so players see the war of attrition unfold.
- Highest bidder takes the prize, and the net gain is prize minus bid.

## The variation's rules

PARAMETERS (stored as table attributes): starting_coins = 100; auctions = 6; raise_stages = 3; min_winning_bid = 1; prize_deck = [10, 15, 20, 25, 30, 40].

R1 Setup: every player has coins = 100, prize_points = 0, committed = 0, final_score = 0. Table: auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'.

R2 Private values: at setup each player is dealt their own values list, a random order of [10, 15, 20, 25, 30, 40] (total 140), visible only to its owner. Entry k is that player's value for auction k. Players' lists are dealt independently, so two players may hold the same value for the same auction.

Each round is one auction. There are 6 rounds.

R3 Round start: auction increases by 1 and every player's committed is set to 0. Each player is privately told their value for this auction (entry number 'auction' of their values list). Everyone is told the auction number and every player's current coins.

R4 Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and change no numbers.

R5 Raise stage (runs 3 times per auction): all players choose at the same time a raise, a whole number from 0 up to (their own coins − their own committed). The range is computed for each player at that moment from their current coins and committed attributes. For example, it is 0..100 at the start of an auction with 100 coins, and 0..55 for a player with 85 coins who committed 30 earlier in the same auction. Immediately after the poll, each player's committed increases by the raise they chose.

R6 Budget limit: a player can never commit more than their coins in one auction. With coins 40 and committed 30, the options are exactly 0 to 10.

R7 Announcement: after each of the 3 raise stages, every player's committed total is announced to all.

R8 Resolution, payment: after the third stage, top_bid = the highest committed, and top_count = the number of players whose committed equals top_bid. Every player's coins decrease by their committed, whether or not they won. For example, bids of 20, 15 and 0 leave coins of 80, 85 and 100 from 100 each.

R9 Resolution, prize: if top_count = 1 and top_bid ≥ 1, that player is the auction_winner and adds their own value for this auction to prize_points. Otherwise auction_winner = 'none' and nobody gets a prize. The winner and every player's coins are announced. Each player's committed is then reset to 0.

R10 End: after the 6th auction, each player's final_score = coins + prize_points.

Objective: After 6 auctions, the player with the highest final_score (coins remaining + prize_points) wins. If several players tie for the highest final_score, the game is a draw among them.

Expected effect: Players disagree on every auction: only one can take the prize, and each values it differently in secret. Talk becomes bluffing ('this one is my 40, back off') and probing. A player who just believes a claim and drops out can lose a cheap prize to a bluffer, and one who escalates to call a bluff can pour coins into a prize worth little to them, because losers pay too. Always bidding 0 loses to anyone who wins one prize for a few coins. Bidding everything early wastes the budget, since prizes are worth at most 40 but cost the bid either way. Matching a rival risks a tie in which both pay and neither wins. Good play means inferring rivals' values from their escalation patterns and remaining coins, conceding contested auctions, and sniping uncontested ones. Value lists have equal totals and there is no seat order, so the deal changes what to do, not who is ahead.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
