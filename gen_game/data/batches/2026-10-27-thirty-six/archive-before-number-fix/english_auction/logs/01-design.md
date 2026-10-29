# 01 design

- time: 2026-10-27T16:38:15+00:00 (68.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c63a6e59375d47ce, reply sha256 927d0d4fbc93678c

## Sent

````
Original game: English Auction
Players in the original: 2 to 8

Original rules:
Each bidder has a private valuation for the object. A minimum bid increment is set and a standing bid starts at zero or a reserve price. In turn order, the current player may raise the standing bid by at least the increment or pass. The new standing bid becomes the highest bid so far and that bidder is the provisional winner. Bidding continues rotating through players who have not dropped out. When a full round passes with no new bid, the auction ends. The provisional winner wins the object and pays their last bid, earning valuation minus price; all others earn zero.
````

## Reply

````
```json
{
  "original_summary": "An open ascending (English) auction for a single object. Bidders with private valuations take turns raising the standing bid by at least an increment or passing until nobody raises. The last bidder wins and earns valuation minus price; everyone else earns zero.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "One simple policy dominates: stay in until the price reaches your value, then drop. No other policy beats it. Turn order gives no edge, but choices barely matter beyond that rule. Under 'highest total wins', the result is fixed once values are dealt: the highest-value bidder wins."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "If both players bid truthfully, the winner is whoever was dealt the higher valuation. Skill cannot overturn the deal. This is a pure lottery."
    },
    {
      "criterion": "headroom",
      "verdict": "bad",
      "evidence": "The game is solved in one line, so a strong player has nothing to improve. A weak player who overbids can only lose by paying more than the item is worth."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Valuations are hidden, but the dominant strategy does not depend on anyone else's value. There is nothing to infer and nothing to plan, because it is a single item in a single round."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Price, winner and surplus all follow by arithmetic from the bids."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only with numeric bids. However, open-ended rotating bidding until a full pass is a loop of unknown length, which the flat step list cannot express. One item is also far too short to make a game."
    }
  ],
  "problems": [
    "P1: Bidding up to your value is a dominant strategy, so the game is solved and needs no thought.",
    "P2: The winner is decided by who was dealt the highest valuation (lottery trap).",
    "P3: There is a single item and a single round, so there is no planning over time and nothing to learn about opponents.",
    "P4: Hidden values do not need to be inferred, because the best action ignores what others hold.",
    "P5: The open-ended bidding loop cannot be built on a flat, fixed step list.",
    "P6: With two players and 'higher total wins', only the difference between totals matters, and the losers' zero payoff makes the comparison trivial."
  ],
  "changes": [
    {
      "what": "Play a sequence of 6 items, one per round, instead of one item.",
      "why": "This creates a multi-round game where players must plan across items and can learn from opponents' earlier bids.",
      "fixes": "P3"
    },
    {
      "what": "Every player receives the same six values {3,5,7,9,11,13}, privately shuffled across the six items.",
      "why": "Every player's values sum to the same 48, so the deal no longer decides who is richer; it only decides where each player's strength lies. It also makes inference work like card counting: a rival who fought hard for an early item probably spent their 13 or 11 there and cannot hold it again.",
      "fixes": "P2, P4"
    },
    {
      "what": "Each player has a fixed budget of 30 coins for the whole game. Bids above your remaining budget are invalid.",
      "why": "Truthful bidding is no longer dominant. Winning an item at a high price can leave you unable to afford your 13 later. Rivals can deliberately push prices up to drain a leader's budget, so players must budget across rounds.",
      "fixes": "P1, P3"
    },
    {
      "what": "Each item gets exactly three simultaneous raise-or-pass bidding turns. The standing bid and leader are announced after each turn, and ties go to a priority order that rotates each round.",
      "why": "This keeps the open, ascending, see-the-standing-bid character of an English auction in a fixed number of steps. Rotating priority removes any seat advantage.",
      "fixes": "P5"
    },
    {
      "what": "Use 3 to 5 players. The highest total profit (values of items won minus prices paid) wins, and equal top totals draw.",
      "why": "With three or more players, one rival's gain is not automatically another's loss. Passing scores 0 and loses to anyone who wins an item profitably, and overbidding produces negative totals.",
      "fixes": "P6, P1"
    },
    {
      "what": "Add one simultaneous message per round before bidding.",
      "why": "It allows players to propose bidding rings ('you take this one, I take the next'), bluff about their values, and threaten to push prices. Because only one player can win, every ring is tempting to betray, so promises must be read and tested.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Ascending open bidding: each turn, players see the standing bid and leader and decide whether to raise by at least the increment or pass.",
    "Private valuations.",
    "The winner of an item pays their own last bid and earns value minus price; everyone else earns nothing on that item.",
    "A minimum increment and a standing bid that starts at zero."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The single-item auction is solved, but a short sequence of auctions with equal value sets and a shared budget constraint turns it into a game about inference, budgeting and opponent modelling while staying an English auction."
  },
  "variation": {
    "name": "Budgeted English Auction Series",
    "summary": "Three to five bidders auction six items one at a time in short open ascending auctions. Everyone holds the same six private values in a secret order and must make one 30-coin budget last the whole series. The highest total profit wins.",
    "players": {"min": 3, "max": 5, "suggested": 3},
    "rules": "SETUP. There are 6 items, auctioned one per round in a known order (item 1 in round 1, and so on to item 6 in round 6). Before round 1, each player is privately dealt the six values 3, 5, 7, 9, 11 and 13 in a random order: one value per item, each value used exactly once. Each player sees only their own values. Every player's values sum to 48. Each player starts with a budget of 30 coins and a score of 0. Seats are numbered 1 to N.\n\nPRIORITY. In round r, the tie-break priority goes to seat ((r - 1) mod N) + 1 first, then the following seats in increasing order, wrapping around. The priority order is announced at the start of the round.\n\nEACH ROUND (one item):\n1. Announce the item number, the priority order, and every player's remaining budget. Budgets and scores are public.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.\n3. Bidding turn 1: every player at the same time either submits a whole-number bid of at least 1 or passes. A bid is valid only if it does not exceed the bidder's remaining budget; an invalid bid counts as a pass. If at least one valid bid was made, the highest becomes the standing bid and its bidder becomes the leader. Equal highest bids go to the player earliest in this round's priority order.\n4. Announce the standing bid and the leader, or announce that there is no bid.\n5. Bidding turn 2: every player at the same time either passes or submits a whole-number bid. To be valid, the bid must be at least the standing bid plus 1 (at least 1 if there is no standing bid) and must not exceed the bidder's remaining budget; otherwise it counts as a pass. The leader may also bid, though they need not. If any valid bid was made, the highest becomes the new standing bid and its bidder the new leader, with ties broken by priority. If nobody makes a valid bid, the standing bid and leader stay as they were.\n6. Announce the standing bid and the leader.\n7. Bidding turn 3: same as turn 2.\n8. Announce the final standing bid and the leader.\n9. Resolution: if there is a leader, that player wins the item. They pay the standing bid from their budget, and their score changes by (their private value for this item minus the standing bid), which may be negative. The price is announced, but the winner's value stays private. If there is no leader, the item goes unsold and nobody scores for it.\n10. Advance to the next round. After round 6 the game ends.\n\nUnspent coins are worth nothing at the end. Scores count only item values won minus prices paid.",
    "objective": "After round 6, the player with the highest score wins. If two or more players share the highest score, the game is a draw.",
    "expected_effect": "Because everyone holds the same values, the deal decides where each player is strong, not how strong. Wins come from reading rivals and managing the budget. Rivals' bids reveal which of their high values are used up: someone who paid 10 on item 2 likely holds 11 or 13 there, so they cannot hold 13 again later. A 30-coin budget against 48 points of value means nobody can win everything, so players must choose which items to fight for. A key tactic is pushing a rival's price up just below what you infer their value to be, draining their budget for later. Truthful bidding is beatable: it overpays early and loses late items. Talk passes both tests. Players disagree because only one can win, so every bidding ring ('I skip item 3 if you skip item 4') rewards whoever breaks it at the last bidding turn. A player who simply follows a proposed ring can be outbid in turn 3 after holding back, or can watch the proposer bluff about a value to win an item cheaply. Simple policies all lose: always passing scores 0 and loses to anyone with a single profitable win; bidding the whole budget at once pays up to 30 for an item worth at most 13; random bidding tends to go negative. Some luck remains in how players' strengths happen to collide on the same items, but over six items, inference and budgeting should dominate."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
