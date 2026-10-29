# Variation: Sealed Escalation: Three-Way Dollar Auction

Three players each have 100 coins and play 6 all-pay auctions. Each auction has 3 simultaneous raise stages, and every player pays everything they commit. Only a unique top bidder wins the prize, valued privately by each player. The highest coins-plus-prizes total wins.

Players: 3 to 3, best with 3

## Review of the original

The Dollar Auction is a two-player auction in which players take turns raising a public bid for a $1 bill. Both the winner and the runner-up pay their bids, so players get drawn into escalating far past the prize's worth.

- **non_degenerate**: bad. With two players and a higher-net-total winner rule, the second mover can always top the first player's bid. Never bidding is safe: it scores 0. Opening at 0.05 and then quitting is close to dominant against a cautious rival. Against a stubborn rival, both players lose without limit. The play reduces to a war of attrition with a known value and nothing hidden.
- **skill_sensitive**: weak. The result depends on who blinks first in an escalation where neither player has information the other lacks. Skill shows only as 'don't enter' or 'quit early'.
- **headroom**: weak. Once a player sees that the sunk cost is irrelevant, the one-shot game is largely solved. Repeating it adds nothing because the prize and the stakes never change.
- **reasoning_dependent**: bad. The information is perfect. The prize value is public and the bids are public, so there is no type or signal to infer.
- **verifiable**: good. Payoffs follow from arithmetic: 1 minus the bid for the winner, minus the bid for the others.
- **fits_platform**: weak. The game is text-only and turn-based. However, the alternating raises have no fixed length, so it could run without end. It is also limited to two players, which brings in the higher-total trap.

## Problems

- P1: Two players with a higher-total winner make it zero-sum by difference. Staying out or quitting first is safe, and escalation is pure attrition.
- P2: Nothing is hidden. The prize value is common knowledge, so there is nothing to infer about opponents.
- P3: Alternating open-ended raises have unbounded length and do not fit fixed-round play.
- P4: A single auction with a known value is quickly solved, so there is no planning over rounds.
- P5 (previous build): the raise poll offered only 0, because the option upper bound evaluated to 0 instead of each player's own coins minus committed. As a result raises were never applied, coins never fell, top_bid stayed 0 and top_count was always 3.
- P6 (previous build): dealing values with a per-player pool/pick loop used many steps and attributes and was error-prone.

## Changes

- Three players, each with a 100-coin budget that carries across 6 auctions. Final score is coins left plus prize points, and the highest final score wins. (fixes: P1): A third player breaks the pure-difference logic. The shared budget forces players to plan which auctions to fight for.
- Each player privately holds their own random order of the same six prize values [10, 15, 20, 25, 30, 40], one value per auction. (fixes: P2): This creates hidden private values to infer from rivals' bidding. Every player's values sum to 140, so the deal changes what to fight for, not who is ahead.
- Each auction is exactly 3 simultaneous raise stages. Committed totals are announced after each stage. All committed coins are paid by everyone. The prize goes only to a unique top bidder with at least 1 committed. (fixes: P3): This keeps the all-pay escalation and sunk-cost tension in a fixed, bounded number of steps. A tie at the top wins nothing but still costs everyone, which is the dollar-auction trap.
- Six auctions, with values and budget carrying between them. (fixes: P4): Players must budget across auctions and read rivals' remaining coins and likely high-value auctions.
- Before every raise stage, a per-player attribute max_raise is set to that same player's own coins minus their own committed. The poll offers exactly the whole numbers 0..max_raise for that player. The chosen raise is stored in raise_amt and added to committed straight after the poll. (fixes: P5): This makes the poll bound the player's own computed value, never a table value, an uninitialised attribute or a constant. With 100 coins a player is offered 0..100. With coins 40 and committed 30 the player is offered 0..10. Committed can never exceed coins.
- Values are dealt in one setup step, giving each player an independent shuffled copy of the value list. In each auction, current_value is the entry at position 'auction', counting from 1. (fixes: P6): This removes the pool/pick loop, uses no random draws inside rounds and needs fewer steps.
- Add one simultaneous message per auction before stage 1. (fixes: P2): Players can bluff about their value ("this one is my 40, stay out") or propose sharing auctions. Only one player can win, so promises are worth testing. This gives players something to reason about.

## Kept from the original

- Everyone pays what they bid, winners and losers alike.
- Bids escalate in visible steps, and sunk costs pull players deeper.
- A prize that can be overpaid for, with ruinous ties at the top.
- Net payoff is the prize value minus the bid.

## The variation's rules

R1 Setup. Every player has coins = 100, prize_points = 0, committed = 0, max_raise = 0, raise_amt = 0, current_value = 0 and final_score = 0. The table has auction = 0, top_bid = 0, top_count = 0 and auction_winner = 'none'. The table prize_deck is [10, 15, 20, 25, 30, 40].

R2 Deal. At setup each player's values is set to an independent random shuffle of prize_deck, a list of 6 entries summing to 140. A player's values list is visible only to that player. Two players may hold the same value for the same auction.

R3 Round start. There are 6 rounds, and one round is one auction. At the start of a round:
- auction increases by 1.
- Every player's committed becomes 0.
- Each player's current_value becomes the entry of their values at position auction, counting from 1.
- Each player is told privately their current_value.
- Everyone is told the auction number and every player's coins and prize_points.

R4 Talk. Everyone writes one short message at the same time. All messages are then shown to everyone. Messages bind no one.

R5 Bound. Immediately before each raise stage, each player's max_raise is set to that same player's coins minus that same player's committed.

R6 Raise stages. Each auction has exactly 3 raise stages. In each stage all players choose at the same moment.
- Each player's options are exactly the whole numbers from 0 to their own max_raise. For example, 0..100 with coins 100 and committed 0; 0..55 with coins 85 and committed 30; 0..10 with coins 40 and committed 30.
- The choice is stored in raise_amt.
- Immediately after the stage, each player's committed increases by their raise_amt.
- Everyone is then told every player's committed.

R7 Limit. A player's committed can never exceed their coins within one auction. This is guaranteed by R5 and R6.

R8 Resolution. After the third stage:
- top_bid = the largest committed among players.
- top_count = the number of players whose committed equals top_bid.
- Every player's coins decreases by their committed.
- If top_count = 1 and top_bid ≥ 1, the player with committed = top_bid adds their own current_value to prize_points, and auction_winner = that player. Otherwise auction_winner = 'none' and no one gains prize_points.
- Everyone is told the auction_winner and top_bid.

R9 End. After auction 6, each player's final_score = coins + prize_points. The game ends.

Objective: The player with the highest final_score (coins left plus prize points) wins. If two or more players tie for the highest final_score, the game is a draw.

Expected effect: Players must infer which auctions rivals value highly from the size and timing of their raises, and from the remaining budgets. They must also budget 100 coins across 6 auctions and decide when to stop escalating once coins are sunk.

Simple policies all lose against some opponent:
- Always 0 keeps 100 but loses to anyone who wins prizes cheaply.
- Always all-in in auction 1 spends everything for at most 40.
- A fixed small raise each stage is beaten by any slightly higher fixed raise.
- Matching others produces ties that cost everyone and win nothing.

Talk matters because players disagree about who should take each prize, and only one player can win the game. A player who honours a claim like "this is my 40, I'll take it, you take the next" may be feeding a rival who lied about their value or who breaks the deal later. Following blindly can lose, and reading bluffs pays.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
