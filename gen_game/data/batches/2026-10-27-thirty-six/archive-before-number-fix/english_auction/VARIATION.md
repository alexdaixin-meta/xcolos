# Variation: Budget English Auction

Six items are auctioned one per round in short ascending auctions. Every player values the same six numbers in a private shuffled order and has 30 coins for the whole game. The highest total profit wins.

Players: 3 to 5, best with 4

## Review of the original

An ascending open-outcry auction for one object. Bidders with private valuations take turns raising a standing bid by at least an increment or passing. The last bidder left wins and earns valuation minus price.

- **non_degenerate**: weak. With one object and private values, 'bid up to your value, then stop' is dominant. 'Always pass' earns 0, and only one player earns anything, so under a winner rule the highest-value player wins almost automatically. Turn order matters little, and choices barely change the outcome beyond following the dominant rule.
- **skill_sensitive**: bad. The winner is whoever was dealt the highest valuation, as long as they follow the dominant strategy. Skill only decides how much surplus is captured, which a winner-only platform cannot see. This is the lottery trap.
- **headroom**: bad. The single-item English auction is solved: bid to your value. A strong player has nothing to improve once they know that.
- **reasoning_dependent**: weak. Values are hidden, but the dominant strategy does not need you to infer them. There is no plan over several rounds and no budget trade-off.
- **verifiable**: good. Price, winner and surplus are pure arithmetic on recorded bids.
- **fits_platform**: weak. The original is text-only, but rotating open-ended bidding until a full lap of passes is an unbounded loop the engine cannot express. It needs a fixed number of bidding turns.

## Problems

- P1: With one item, the winner is the player dealt the highest valuation (lottery trap), and bidding to value is dominant, so there is no reasoning to reward.
- P2: There is no planning over several rounds, no budget, and nothing gained from inferring rivals' values.
- P3: Open-ended rotating bidding until a full pass lap is not a bounded, flat step list.
- P4 (previous build): the bid option list was shrunk by eligibility or standing bid, so a test bid of 4 could not be offered, and every recorded move was a pass.
- P5 (previous build): the round reset (standing bid 0, leader 0, everyone eligible) did not run before bidding, so players ended ineligible and nothing sold.
- P6 (previous build): dealing used a needs_deal flag and one-at-a-time appends, which fired on players whose list was already given, and the deal check did not read the given list.
- P7 (previous build): bids were never recorded into bid/valid_bid before resolution, so the leader, the payment and the score never changed.

## Changes

- Sell 6 items over 6 rounds. Each player privately holds a shuffled copy of the same value set [3,5,7,9,11,13] (sum 48). (fixes: P1): Every player's values are worth the same in total, so the deal changes WHAT to fight for, not who is ahead.
- Give each player a budget of 30 for the whole game, less than the 48 in total value, and make the winner the highest total score (value minus price). (fixes: P2): Players must ration money across items, guess which items rivals value highly, and pick their battles. Overpaying loses and always passing scores 0.
- Each round has exactly 3 simultaneous bidding turns with fixed resolution. A tie at the top changes nothing. (fixes: P3): This keeps the auction bounded and flat while keeping the ascending standing bid and drop-out (eligibility) feel.
- State that every bid poll offers every player the same options: pass (0) and every whole number from 1 to that player's current budget. Validity is checked only at resolution. (fixes: P4): The builder must not filter options. Invalid bids are simply treated as passes.
- Make the round reset an explicit step placed right after the talk poll and before bidding turn 1: standing_bid 0, leader 0, eligible true for all, bid 0 and valid_bid false for all. (fixes: P5): This guarantees fresh eligibility each round.
- Replace the deal with one setup step: for each player whose values list has length 0, set values to a random shuffle of value_set in one operation. Remove needs_deal and the per-entry appends. (fixes: P6): A given list is read and left alone. A list is never built incrementally.
- Spell out each bidding turn as four ordered steps: poll into bid; compute valid_bid; compute top_bid and top_count over valid bids; update standing_bid, leader and eligibility. (fixes: P7): This makes recording before resolution unambiguous.
- Add a simultaneous one-message talk phase at the start of each round. (fixes: P2): Players can bluff about their values, propose splitting items or test promises. Only one player can win, so following a proposal can hand a rival cheap items.

## Kept from the original

- An ascending standing bid that each new bid must beat by at least the increment
- Private valuations, with the winner paying their own last bid
- Players drop out by passing: once you pass while not leading, you cannot re-enter that item
- Surplus = valuation minus price, and losers earn nothing on the item

## The variation's rules

CONSTANTS: value_set = [3,5,7,9,11,13] (sum 48); starting budget 30; rounds 6; bidding turns per round 3; minimum first bid 1; minimum raise 1; pass is coded 0; 'no leader' is coded 0.

R1 START: Every player has budget 30, score 0, spent 0, bid 0, valid_bid false and eligible false. The table has round 0, standing_bid 0, leader 0, last_price 0, top_bid 0 and top_count 0.

R2 DEAL (once, at setup, before round 1): for each player, if that player's values list has length 0, set it in ONE operation to a random ordering of value_set. If a player's values list is already set (length 6), leave it unchanged. Do not use any other flag and do not append entries one at a time.

R3 INFORMATION: A player's values list is visible only to that player. Budgets, scores, spent, eligibility, all submitted bids after each turn, standing_bid, leader and last_price are public.

R4 ITEMS: In round r (r = 1 to 6), item r is sold. A player's value for it is entry r of their own values list, counting from 1.

Each round runs these steps in order:

R5 TALK: Every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages bind no one.

R6 RESET (immediately after talk, before bidding turn 1): set standing_bid = 0 and leader = 0. For every player set eligible = true, bid = 0 and valid_bid = false.

BIDDING TURNS t = 1, 2, 3, each made of steps R7 to R9:

R7 BID POLL (simultaneous): every player chooses from the SAME kind of list: 0 (pass) or any whole number from 1 up to their current budget. The options are never filtered by eligibility or standing bid. Record the choice in that player's bid.

R8 VALIDITY AND TOP: for each player, set valid_bid = true if they are eligible, their bid is at least standing_bid + 1, and their bid is at most their budget; otherwise set valid_bid = false. Then set top_bid = the largest bid among players with valid_bid true (0 if none), and top_count = how many players with valid_bid true bid exactly top_bid.

R9 RESOLVE: if top_count is exactly 1, set standing_bid = top_bid and leader = the seat number of that bidder. If top_count is 0 or 2 or more, standing_bid and leader do not change. Then for every player set eligible = true if (valid_bid is true) or (they are the leader); otherwise eligible = false. A player who drops out stays out for the rest of the round.

R10 SETTLE (after turn 3): if leader is not 0, the leader's budget decreases by standing_bid, their spent increases by standing_bid, and their score increases by (entry r of their values list) - standing_bid. Set last_price = standing_bid. If leader is 0, the item goes unsold and last_price = 0.

R11 END CHECK: after round 6 the game ends.

Scores can go negative if a player pays more than their value. Money left unspent is worth nothing.

Objective: After round 6, the player with the highest score wins. If two or more players tie for the highest score, the game is a draw.

Expected effect: With a budget of 30 against 48 in total value, no one can buy everything. Players must decide which of their high-value items to fight for. They infer rivals' orderings from the public bids in earlier rounds (each player's values are a permutation of the same set, so whoever chased item 2 hard probably holds a 13 or 11 there and a low value elsewhere). They must also save money for later rounds. Always passing scores 0 and loses to anyone who buys at a profit. Always bidding high overpays and runs out of budget. Because every hand sums to 48, the deal decides what to target, not who leads. Talk passes both tests. Players disagree because only one can win: one may propose 'you take item 3, I take item 4' while holding a 13 on item 3, or bluff low interest to win an item cheaply. A player who simply follows a proposal can concede a high-value item and watch the proposer pull ahead, so promises must be read and tested against later bids.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
