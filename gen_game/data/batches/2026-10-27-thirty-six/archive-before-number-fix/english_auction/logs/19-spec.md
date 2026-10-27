# 19 spec

- time: 2026-10-27T16:56:02+00:00 (46.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0f0b637b461a3e31, reply sha256 920ce7f54b01d779

## Sent

````
Game: Budgeted English Auction with Activity Rule
Players in the source: 3 to 6
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
R1 Setup. There are N players (3 to 6). Each player starts with budget 30, score 0 and spent 0. Before round 1, each player whose values list is empty receives a private values list: a random ordering of [3,5,7,9,11,13], so every list sums to 48. A list that is already set is never overwritten. Table state starts at standing_bid 0, leader 0 (0 means no leader) and last_price 0.
R2 Privacy. A player's values list is visible only to that player. Everyone sees all budgets, scores, eligibility flags, standing_bid, leader and last_price. Everyone knows the value set is {3,5,7,9,11,13}.
R3 Items. The game has 6 rounds. In round r, item r is sold. A player's value for item r is entry r of their own list, counting from 1.
R4 Talk. At the start of each round, every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind nobody.
R5 Round reset. After talk, set standing_bid to 0 and leader to 0, and mark every player eligible.
R6 Bidding turns. Each round has exactly 3 bidding turns. Each turn is a simultaneous poll of all players. Each player answers pass (0) or a whole number from 1 up to their current budget.
R7 Validity. A bid is valid only if all three conditions hold:
(a) the bidder is eligible for this turn;
(b) the bid is at least standing_bid + 1 (in turn 1 that means at least 1);
(c) the bid is at most the bidder's budget.
Pass, and any bid that is not valid, counts as no bid.
R8 Turn result. Find the highest valid bid.
- If exactly one player made it, standing_bid becomes that amount and leader becomes that player.
- If two or more players made it (a tie), or nobody made a valid bid, standing_bid and leader stay unchanged.
- A lower valid bid never wins.
R9 Eligibility. After each turn, a player is eligible for the next turn only if they made a valid bid in this turn (winning, tied or beaten), or they are the leader after this turn. Everyone else is marked ineligible for the rest of the round. After each turn, standing_bid, leader and all eligibility flags are announced.
R10 Resolution. After turn 3:
- If leader is not 0, the leader's budget decreases by standing_bid, their spent increases by standing_bid, and their score increases by (their value for item r) minus standing_bid. This can be negative.
- last_price is set to standing_bid. If leader is 0, the item goes unsold and last_price is 0.
- The round's result is announced.
R11 End. After round 6 the game ends. Unspent budget is worth nothing.

How the winner is decided: After round 6, the player with the strictly highest score wins. If two or more players share the highest score, the game is a draw.
````

## Reply

````
```json
{
  "name": "Budgeted English Auction with Activity Rule",
  "summary": "Six items are auctioned one per round. In each round there are three simultaneous sealed bidding turns, and a player who stops bidding drops out of that item. Each player has a budget of 30 and private values, and the highest score (value minus price, summed) wins.",
  "players": {"min": 3, "max": 6, "suggested": 4},
  "parameters": {
    "starting_budget": 30,
    "starting_score": 0,
    "starting_spent": 0,
    "rounds": 6,
    "items": 6,
    "bidding_turns_per_round": 3,
    "value_set": [3, 5, 7, 9, 11, 13],
    "values_sum": 48,
    "min_first_bid": 1,
    "min_raise": 1,
    "pass_bid": 0,
    "no_leader_code": 0
  },
  "attributes": {
    "player": [
      {"key": "budget", "type": "number", "visible": "public", "initial": 30, "meaning": "Money left to bid with. Unspent budget is worth nothing at the end.", "observable": true},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of (value minus price paid) over the items won. It can be negative.", "observable": true},
      {"key": "spent", "type": "number", "visible": "public", "initial": 0, "meaning": "Total paid for the items won.", "observable": true},
      {"key": "values", "type": "list", "visible": "ally", "initial": [], "meaning": "Private values. Entry r (counting from 1) is this player's value for item r. It is a random ordering of [3,5,7,9,11,13].", "observable": false},
      {"key": "eligible", "type": "bool", "visible": "public", "initial": true, "meaning": "Whether this player may make a valid bid in the current bidding turn.", "observable": false},
      {"key": "bid", "type": "number", "visible": "ally", "initial": 0, "meaning": "This player's answer in the current bidding turn (0 = pass).", "observable": false},
      {"key": "valid_bid", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this player's bid in the current turn met all three validity conditions.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round; item r is sold in round r.", "observable": true},
      {"key": "turn", "type": "number", "visible": "public", "initial": 0, "meaning": "Current bidding turn within the round (1 to 3).", "observable": false},
      {"key": "standing_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "The current highest uniquely-made valid bid on this round's item.", "observable": true},
      {"key": "leader", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat number of the player holding the standing bid (0 = no leader).", "observable": true},
      {"key": "last_price", "type": "number", "visible": "public", "initial": 0, "meaning": "Price of the last item sold (0 if it went unsold).", "observable": true},
      {"key": "value_set", "type": "list", "visible": "public", "initial": [3, 5, 7, 9, 11, 13], "meaning": "The public set of values that every private list is an ordering of.", "observable": false},
      {"key": "top_bid", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch: the highest valid bid in the current turn (0 if none).", "observable": false},
      {"key": "top_count", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch: how many players made top_bid as a valid bid this turn.", "observable": false}
    ]
  },
  "setup": [
    "Every player starts with budget 30, score 0 and spent 0.",
    "Each player whose values list is empty receives a random ordering of [3,5,7,9,11,13] as their private values list (visible only to them). A list that is already set is never overwritten.",
    "The table starts with round 0, standing_bid 0, leader 0 (no leader) and last_price 0.",
    "Everyone is told that the value set is {3,5,7,9,11,13}, that each list sums to 48, and that there are 6 rounds with 3 bidding turns each."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; announce that item {round} is now for sale."},
    {"action": "poll", "who": "all players", "answer": "one short text message", "effect": "Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind nobody."},
    {"action": "update", "who": "all players", "answer": null, "effect": "standing_bid = 0; leader = 0; turn = 0; every player's eligible = true; every player's valid_bid = false."},
    {"action": "update", "who": "all players", "answer": null, "effect": "turn += 1."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 (pass) to the player's current budget", "effect": "Each player's answer is stored in their bid. Nobody sees any bid until all are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: valid_bid = (eligible == true AND bid >= standing_bid + 1 AND bid <= budget AND bid >= 1)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "top_bid = the maximum bid among players with valid_bid true (0 if none); top_count = the number of players with valid_bid true AND bid == top_bid."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If top_count == 1 and top_bid >= 1: standing_bid = top_bid and leader = the seat of that player. Otherwise (a tie or no valid bid) standing_bid and leader are unchanged."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: eligible = (valid_bid == true OR seat == leader). Announce standing_bid, leader and every player's eligible flag."},
    {"action": "repeat", "who": "all players", "answer": null, "effect": "Run the four steps above (turn += 1 through the eligibility update) again until turn == 3."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If leader != 0: the leader's budget -= standing_bid, spent += standing_bid, and score += values[round] - standing_bid. Set last_price = standing_bid if leader != 0, otherwise last_price = 0 (the item goes unsold). Announce the round's result: item, winner seat or unsold, price, and every budget and score."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round == 6 the game ends; otherwise start the next round."}
  ],
  "ending": {
    "condition": "round == 6 (checked after round 6's resolution)",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score (sum of value minus price over the items won). The highest score wins. Players level at the highest score share the result, which the source calls a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has budget 30, score 0 and spent 0, and the table has standing_bid 0, leader 0 and last_price 0."},
    {"id": "R2", "text": "When setup runs and a player's values list is empty, then that player receives a random ordering of [3,5,7,9,11,13], which sums to 48. When a list is already set, then it is not overwritten."},
    {"id": "R3", "text": "When values are dealt, then a player's values list is visible only to that player, while all budgets, scores, spent, eligibility flags, standing_bid, leader and last_price are public."},
    {"id": "R4", "text": "When round r is played (r from 1 to 6), then item r is sold, and a player's value for it is entry r of their own values list, counting from 1."},
    {"id": "R5", "text": "When a round starts, then every player writes one short message simultaneously, and all messages are then shown to everyone. No message binds anyone."},
    {"id": "R6", "text": "When the talk phase of a round ends, then standing_bid becomes 0, leader becomes 0 and every player becomes eligible."},
    {"id": "R7", "text": "When a round is played, then it has exactly 3 bidding turns. In each turn all players simultaneously answer 0 (pass) or a whole number from 1 to their current budget."},
    {"id": "R8", "text": "When a player bids, then the bid is valid only if the player is eligible, the bid is at least standing_bid + 1 (at least 1 in turn 1), and the bid is at most the player's budget. A pass or an invalid bid counts as no bid."},
    {"id": "R9", "text": "When exactly one player made the highest valid bid in a turn (for example a single bid of 6 against a bid of 4), then standing_bid becomes that amount and leader becomes that player's seat."},
    {"id": "R10", "text": "When two or more players tie on the highest valid bid (for example two bids of 6), or nobody made a valid bid, then standing_bid and leader stay unchanged, and a lower valid bid never wins."},
    {"id": "R11", "text": "When a turn ends, then a player stays eligible for the next turn only if they made a valid bid in that turn (winning, tied or beaten) or they are the leader. Every other player is ineligible for the rest of the round."},
    {"id": "R12", "text": "When a turn ends, then standing_bid, leader and every eligibility flag are announced to all."},
    {"id": "R13", "text": "When turn 3 ends with leader not 0 and standing_bid p, then the leader's budget decreases by p, their spent increases by p, and their score increases by (their value for item r) minus p, which can be negative (value 3 at price 8 gives -5)."},
    {"id": "R14", "text": "When turn 3 ends, then last_price is set to standing_bid if there is a leader, and to 0 if leader is 0 (the item goes unsold). The round's result is announced."},
    {"id": "R15", "text": "When round 6 has been resolved, then the game ends and unspent budget is worth nothing."},
    {"id": "R16", "text": "When the game ends, then the player with the strictly highest score wins. If two or more players share the highest score, then they share the result (a draw)."}
  ],
  "offers": [
    {"question": "Talk message at the start of each round", "who": "every seat", "options": "one short free-text message"},
    {"question": "Bid in each of the 3 bidding turns", "who": "every seat, eligible or not (the poll goes to all players)", "options": "0 (pass) or any whole number from 1 to that seat's current budget. A bid from an ineligible seat, or one below standing_bid + 1, is accepted as an answer but counts as no bid."}
  ],
  "choices": [
    {"what": "3 to 6 players, 4 suggested", "why": "The designer set 3 to 6 with 4 suggested. Three is the smallest table where an auction has several rivals, so ties and drop-outs matter. Above 6, talk gets long and each player wins too few of the 6 items for their choices to matter."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The source requires simultaneous messages shown to all. Talk earns its place because players have conflicting private values and may signal, bluff about which items they value, or try to arrange not to bid against each other."},
    {"what": "The strategy a thoughtful player follows", "why": "Each player has a budget of 30 against values totaling 48, so they must save money for their high-value items. Bidding in every turn keeps a player eligible, tied bids win nothing, and they must guess rivals' values from talk and past prices."},
    {"what": "Bids are polled from ineligible players too, and their bids are simply invalid", "why": "The source says each turn polls all players, and validity handles eligibility."},
    {"what": "Leader stores the seat number, with 0 meaning no leader", "why": "The source uses 0 for no leader, and seats are numbered from 1."}
  ],
  "simplifications": [
    {"what": "A draw at the top is expressed as a shared win among the players tied for highest score", "why": "The engine has no separate draw: players level at the top share the win, which is the arithmetic equivalent of the source's draw."},
    {"what": "The three bidding turns are one block of steps run by a repeat until turn == 3", "why": "This avoids writing the same four steps three times. The behavior is identical."},
    {"what": "Scratch attributes top_bid, top_count and valid_bid are added", "why": "The engine needs stored intermediate values to compute the highest unique valid bid by arithmetic."}
  ],
  "unsupported": []
}
```
````
