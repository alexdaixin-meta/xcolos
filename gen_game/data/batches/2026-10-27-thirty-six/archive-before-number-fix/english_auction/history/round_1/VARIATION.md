# Variation: Budgeted English Auction Series

Three to five bidders auction six items one at a time in short open ascending auctions. Everyone holds the same six private values in a secret order and must make one 30-coin budget last the whole series. The highest total profit wins.

Players: 3 to 5, best with 3

## Review of the original

An open ascending (English) auction for a single object. Bidders with private valuations take turns raising the standing bid by at least an increment or passing until nobody raises. The last bidder wins and earns valuation minus price; everyone else earns zero.

- **non_degenerate**: bad. One simple policy dominates: stay in until the price reaches your value, then drop. No other policy beats it. Turn order gives no edge, but choices barely matter beyond that rule. Under 'highest total wins', the result is fixed once values are dealt: the highest-value bidder wins.
- **skill_sensitive**: bad. If both players bid truthfully, the winner is whoever was dealt the higher valuation. Skill cannot overturn the deal. This is a pure lottery.
- **headroom**: bad. The game is solved in one line, so a strong player has nothing to improve. A weak player who overbids can only lose by paying more than the item is worth.
- **reasoning_dependent**: weak. Valuations are hidden, but the dominant strategy does not depend on anyone else's value. There is nothing to infer and nothing to plan, because it is a single item in a single round.
- **verifiable**: good. Price, winner and surplus all follow by arithmetic from the bids.
- **fits_platform**: weak. It is text-only with numeric bids. However, open-ended rotating bidding until a full pass is a loop of unknown length, which the flat step list cannot express. One item is also far too short to make a game.

## Problems

- P1: Bidding up to your value is a dominant strategy, so the game is solved and needs no thought.
- P2: The winner is decided by who was dealt the highest valuation (lottery trap).
- P3: There is a single item and a single round, so there is no planning over time and nothing to learn about opponents.
- P4: Hidden values do not need to be inferred, because the best action ignores what others hold.
- P5: The open-ended bidding loop cannot be built on a flat, fixed step list.
- P6: With two players and 'higher total wins', only the difference between totals matters, and the losers' zero payoff makes the comparison trivial.

## Changes

- Play a sequence of 6 items, one per round, instead of one item. (fixes: P3): This creates a multi-round game where players must plan across items and can learn from opponents' earlier bids.
- Every player receives the same six values {3,5,7,9,11,13}, privately shuffled across the six items. (fixes: P2, P4): Every player's values sum to the same 48, so the deal no longer decides who is richer; it only decides where each player's strength lies. It also makes inference work like card counting: a rival who fought hard for an early item probably spent their 13 or 11 there and cannot hold it again.
- Each player has a fixed budget of 30 coins for the whole game. Bids above your remaining budget are invalid. (fixes: P1, P3): Truthful bidding is no longer dominant. Winning an item at a high price can leave you unable to afford your 13 later. Rivals can deliberately push prices up to drain a leader's budget, so players must budget across rounds.
- Each item gets exactly three simultaneous raise-or-pass bidding turns. The standing bid and leader are announced after each turn, and ties go to a priority order that rotates each round. (fixes: P5): This keeps the open, ascending, see-the-standing-bid character of an English auction in a fixed number of steps. Rotating priority removes any seat advantage.
- Use 3 to 5 players. The highest total profit (values of items won minus prices paid) wins, and equal top totals draw. (fixes: P6, P1): With three or more players, one rival's gain is not automatically another's loss. Passing scores 0 and loses to anyone who wins an item profitably, and overbidding produces negative totals.
- Add one simultaneous message per round before bidding. (fixes: P4): It allows players to propose bidding rings ('you take this one, I take the next'), bluff about their values, and threaten to push prices. Because only one player can win, every ring is tempting to betray, so promises must be read and tested.

## Kept from the original

- Ascending open bidding: each turn, players see the standing bid and leader and decide whether to raise by at least the increment or pass.
- Private valuations.
- The winner of an item pays their own last bid and earns value minus price; everyone else earns nothing on that item.
- A minimum increment and a standing bid that starts at zero.

## The variation's rules

SETUP. There are 6 items, auctioned one per round in a known order (item 1 in round 1, and so on to item 6 in round 6). Before round 1, each player is privately dealt the six values 3, 5, 7, 9, 11 and 13 in a random order: one value per item, each value used exactly once. Each player sees only their own values. Every player's values sum to 48. Each player starts with a budget of 30 coins and a score of 0. Seats are numbered 1 to N.

PRIORITY. In round r, the tie-break priority goes to seat ((r - 1) mod N) + 1 first, then the following seats in increasing order, wrapping around. The priority order is announced at the start of the round.

EACH ROUND (one item):
1. Announce the item number, the priority order, and every player's remaining budget. Budgets and scores are public.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
3. Bidding turn 1: every player at the same time either submits a whole-number bid of at least 1 or passes. A bid is valid only if it does not exceed the bidder's remaining budget; an invalid bid counts as a pass. If at least one valid bid was made, the highest becomes the standing bid and its bidder becomes the leader. Equal highest bids go to the player earliest in this round's priority order.
4. Announce the standing bid and the leader, or announce that there is no bid.
5. Bidding turn 2: every player at the same time either passes or submits a whole-number bid. To be valid, the bid must be at least the standing bid plus 1 (at least 1 if there is no standing bid) and must not exceed the bidder's remaining budget; otherwise it counts as a pass. The leader may also bid, though they need not. If any valid bid was made, the highest becomes the new standing bid and its bidder the new leader, with ties broken by priority. If nobody makes a valid bid, the standing bid and leader stay as they were.
6. Announce the standing bid and the leader.
7. Bidding turn 3: same as turn 2.
8. Announce the final standing bid and the leader.
9. Resolution: if there is a leader, that player wins the item. They pay the standing bid from their budget, and their score changes by (their private value for this item minus the standing bid), which may be negative. The price is announced, but the winner's value stays private. If there is no leader, the item goes unsold and nobody scores for it.
10. Advance to the next round. After round 6 the game ends.

Unspent coins are worth nothing at the end. Scores count only item values won minus prices paid.

Objective: After round 6, the player with the highest score wins. If two or more players share the highest score, the game is a draw.

Expected effect: Because everyone holds the same values, the deal decides where each player is strong, not how strong. Wins come from reading rivals and managing the budget. Rivals' bids reveal which of their high values are used up: someone who paid 10 on item 2 likely holds 11 or 13 there, so they cannot hold 13 again later. A 30-coin budget against 48 points of value means nobody can win everything, so players must choose which items to fight for. A key tactic is pushing a rival's price up just below what you infer their value to be, draining their budget for later. Truthful bidding is beatable: it overpays early and loses late items. Talk passes both tests. Players disagree because only one can win, so every bidding ring ('I skip item 3 if you skip item 4') rewards whoever breaks it at the last bidding turn. A player who simply follows a proposed ring can be outbid in turn 3 after holding back, or can watch the proposer bluff about a value to win an item cheaply. Simple policies all lose: always passing scores 0 and loses to anyone with a single profitable win; bidding the whole budget at once pays up to 30 for an item worth at most 13; random bidding tends to go negative. Some luck remains in how players' strengths happen to collide on the same items, but over six items, inference and budgeting should dominate.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
