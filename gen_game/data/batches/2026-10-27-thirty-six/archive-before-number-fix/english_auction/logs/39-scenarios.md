# 39 scenarios

- time: 2026-10-27T17:11:11+00:00 (41.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 538a53844a7fc441, reply sha256 e24f85bdfb0ffe45

## Sent

````
SPEC:
{
  "name": "Budget English Auction",
  "summary": "Six items are auctioned in turn, each over three rounds of simultaneous bids. Each player has a private value for every item and a budget of 30, and the highest total profit (value minus price paid) wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "value_1": 3,
    "value_2": 5,
    "value_3": 7,
    "value_4": 9,
    "value_5": 11,
    "value_6": 13,
    "value_sum": 48,
    "starting_budget": 30,
    "rounds": 6,
    "bidding_turns_per_round": 3,
    "minimum_first_bid": 1,
    "minimum_raise": 1,
    "pass_code": 0,
    "no_leader_code": 0
  },
  "attributes": {
    "player": [
      {
        "key": "budget",
        "type": "number",
        "visible": "public",
        "initial": 30,
        "meaning": "Money left to spend; it falls by the price of each item won.",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum over items won of (own value for the item - price paid); it can be negative.",
        "observable": true
      },
      {
        "key": "spent",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total money paid for items won.",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The bid submitted in the current bidding turn (0 = pass).",
        "observable": false
      },
      {
        "key": "valid_bid",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the current bid is valid: the player is eligible, bid >= standing_bid + 1 and bid <= budget.",
        "observable": false
      },
      {
        "key": "eligible",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player is still in the bidding for the current item.",
        "observable": false
      },
      {
        "key": "values",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's private random ordering of value_set; entry r is their value for item r.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, which is also the number of the item being sold (1 to 6).",
        "observable": true
      },
      {
        "key": "standing_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current highest accepted bid on this item.",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat holding standing_bid (0 = no leader).",
        "observable": false
      },
      {
        "key": "last_price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The price the last item sold for (0 if it went unsold).",
        "observable": true
      },
      {
        "key": "top_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The largest valid bid in the current turn (0 if none).",
        "observable": false
      },
      {
        "key": "top_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many valid bids equal top_bid in the current turn.",
        "observable": false
      },
      {
        "key": "value_set",
        "type": "list",
        "visible": "none",
        "initial": [
          3,
          5,
          7,
          9,
          11,
          13
        ],
        "meaning": "The values that are shuffled into each player's values list.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player starts with budget 30, score 0, spent 0, bid 0, valid_bid false and eligible false.",
    "The table starts with round 0, standing_bid 0, leader 0, last_price 0, top_bid 0 and top_count 0.",
    "For each player whose values list has length 0, values is set in one operation to a random ordering of value_set [3,5,7,9,11,13]. A values list that already has length 6 is left unchanged.",
    "Each player sees only their own values list."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. Announce that item {round} is for sale."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a short text message",
      "effect": "Messages are collected at the same time and then broadcast to all as 'Seat {seat} says: {value}'. Messages bind no one."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reset: standing_bid = 0 and leader = 0; for every player eligible = true, bid = 0 and valid_bid = false."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 (pass) to the player's own budget",
      "effect": "Bidding turn 1: each player's choice is stored in bid. All bids are revealed after everyone has answered."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 1 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest bid among players with valid_bid (0 if none). top_count = the number of players with valid_bid whose bid equals top_bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 1 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then for every player, eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 (pass) to the player's own budget",
      "effect": "Bidding turn 2: each player's choice is stored in bid. All bids are revealed after everyone has answered."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 2 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest valid bid (0 if none). top_count = the number of valid bids equal to top_bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 2 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 (pass) to the player's own budget",
      "effect": "Bidding turn 3: each player's choice is stored in bid. All bids are revealed after everyone has answered."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 3 validity: for each player, valid_bid = (eligible and bid >= standing_bid + 1 and bid <= budget). top_bid = the largest valid bid (0 if none). top_count = the number of valid bids equal to top_bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Turn 3 resolve: if top_count == 1, standing_bid = top_bid and leader = that bidder's seat. Then eligible = valid_bid or (seat == leader). Announce all bids, standing_bid and leader."
    },
    {
      "action": "update",
      "who": "the leader, if any",
      "answer": null,
      "effect": "Settle: if leader != 0, the leader's budget -= standing_bid, spent += standing_bid, score += values[round] - standing_bid, and last_price = standing_bid. If leader == 0, last_price = 0 and the item goes unsold. Announce the result, each player's budget and score, and last_price."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= 6; otherwise play the next round."
    }
  ],
  "ending": {
    "condition": "round >= 6",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score after round 6. The highest score wins, and players tied at the top share the result."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At the start, every player has budget 30, score 0 and spent 0, and the table has round 0, standing_bid 0, leader 0 and last_price 0."
    },
    {
      "id": "R2",
      "text": "At setup, when a player's values list has length 0, it is set in one operation to a random ordering of [3,5,7,9,11,13], so its entries sum to 48. A values list of length 6 is left unchanged."
    },
    {
      "id": "R3",
      "text": "A player's values list is visible only to that player. Budgets, scores, spent, eligibility, all bids after each turn, standing_bid, leader and last_price are public."
    },
    {
      "id": "R4",
      "text": "In round r, item r is sold, and a player's value for it is entry r (counting from 1) of their values list."
    },
    {
      "id": "R5",
      "text": "At the start of each round, every player submits one short message simultaneously, and all messages are then shown to everyone."
    },
    {
      "id": "R6",
      "text": "After talk, standing_bid = 0 and leader = 0, and every player has eligible = true, bid = 0 and valid_bid = false."
    },
    {
      "id": "R7",
      "text": "In each of the 3 bidding turns, every player simultaneously chooses 0 (pass) or a whole number from 1 to their current budget, and the options are not filtered by eligibility or standing_bid."
    },
    {
      "id": "R8",
      "text": "When a player is eligible and bids at least standing_bid + 1 and at most their budget, then valid_bid = true; otherwise valid_bid = false (for example, a bid of 5 against a standing_bid of 5 is invalid)."
    },
    {
      "id": "R9",
      "text": "top_bid is the largest valid bid (0 if none), and top_count is the number of valid bids equal to top_bid."
    },
    {
      "id": "R10",
      "text": "When top_count == 1, standing_bid = top_bid and leader = that bidder's seat. When top_count is 0 or 2 or more, standing_bid and leader are unchanged (two valid bids tied at the top both fail)."
    },
    {
      "id": "R11",
      "text": "After each turn resolves, a player stays eligible only if their bid was valid or they are the leader. An ineligible player stays out for the rest of the round, because any later bid from them is invalid."
    },
    {
      "id": "R12",
      "text": "After turn 3, when leader != 0, the leader's budget falls by standing_bid, spent rises by standing_bid, score changes by (their value for item r - standing_bid), and last_price = standing_bid."
    },
    {
      "id": "R13",
      "text": "After turn 3, when leader == 0, the item goes unsold, no attribute but last_price changes, and last_price = 0."
    },
    {
      "id": "R14",
      "text": "Scores can be negative when a player pays more than their value (for example, winning value 3 at price 8 gives -5), and unspent budget is worth 0 points."
    },
    {
      "id": "R15",
      "text": "After round 6 the game ends, and the player with the highest score wins."
    }
  ],
  "offers": [
    {
      "question": "Talk message each round",
      "who": "every seat",
      "options": "a short free-text message"
    },
    {
      "question": "Bid in bidding turns 1, 2 and 3",
      "who": "every seat, eligible or not",
      "options": "0 (pass) or any whole number from 1 to that seat's current budget; a seat with budget 0 is offered only 0"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "This is the designer's range and size. Three is the smallest table where several rivals compete and collude for each item; above 5, each player wins too few of the 6 items and the talk gets too long to follow."
    },
    {
      "what": "Keep simultaneous talk before bidding, as a poll with broadcast",
      "why": "The rules require it. Players disagree about who should win each item, so proposals to share items out or hold prices down are worth reasoning about but may be betrayed."
    },
    {
      "what": "The three bidding turns are written out as explicit step triples instead of a repeat",
      "why": "The number of turns is fixed at 3, so a flat step list is the simplest faithful form."
    },
    {
      "what": "Player strategy",
      "why": "A thoughtful player bids up to their private value on the items they value most, saves budget for high-value items, avoids tied top bids, and uses talk to propose dividing items while watching for defection."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is treated as the tied players sharing the win rather than as a separate draw",
      "why": "The engine treats players level at the top as sharing the win, which is equivalent to the source's draw outcome."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: budget, score, spent; table: round, last_price.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Initial state: budget 30, score 0, spent 0, round 0, last_price 0",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 0, "last_price": 0}
    }
  },
  {
    "name": "Each player's values list holds 6 entries after setup (ordering is random, only length asserted)",
    "rule": "R2",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "expect": {
      "lens": {"players": {"1": {"values": 6}, "2": {"values": 6}, "3": {"values": 6}, "4": {"values": 6}}}
    }
  },
  {
    "name": "Public results after a sale: highest of three distinct valid bids wins at its own bid",
    "rule": "R3",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"values": [11, 3, 5, 7, 9, 13]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 7, "times": 1},
      {"seat": 3, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 23, "score": 4, "spent": 7},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 7}
    }
  },
  {
    "name": "In round 3 the value used is entry 3 of the values list",
    "rule": "R4",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 9, 11, 13]}},
      "game": {"round": 2}
    },
    "rules": [{"seat": 1, "options_include": 2, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 28, "score": 5, "spent": 2}},
      "game": {"round": 3, "last_price": 2}
    }
  },
  {
    "name": "A round with talk and all passes advances the round and changes nothing else",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 0}
    }
  },
  {
    "name": "Reset clears a stale standing_bid and leader and makes everyone eligible, so a bid of 1 wins",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13], "eligible": false},
        "2": {"eligible": true}
      },
      "game": {"round": 0, "standing_bid": 5, "leader": 2}
    },
    "rules": [{"seat": 1, "options_include": 1, "times": 1}],
    "expect": {
      "players": {
        "1": {"budget": 29, "score": 2, "spent": 1},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 1}
    }
  },
  {
    "name": "Bid options run from 0 to the seat's budget; a seat with budget 0 is offered only 0",
    "rule": "R7",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"budget": 10},
        "3": {"budget": 0}
      },
      "game": {"round": 0}
    },
    "rules": [{"seat": 1, "options_include": 5, "times": 1}],
    "expect": {
      "offered": [{"seat": 2, "option": 10}, {"seat": 2, "option": 0}, {"seat": 3, "option": 0}],
      "not_offered": [{"seat": 2, "option": 11}, {"seat": 3, "option": 1}]
    }
  },
  {
    "name": "A bid equal to standing_bid is invalid, so the earlier bid of 5 wins",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [9, 3, 5, 7, 11, 13]},
        "2": {"values": [13, 3, 5, 7, 9, 11]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 5, "times": 1},
      {"seat": 2, "options_include": 4, "times": 1},
      {"seat": 2, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 25, "score": 4, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 5}
    }
  },
  {
    "name": "top_bid is the largest valid bid: bids 3, 7 and 5, so seat 2 wins at 7",
    "rule": "R9",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"values": [11, 3, 5, 7, 9, 13]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 7, "times": 1},
      {"seat": 3, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"score": 0, "budget": 30},
        "2": {"score": 4, "budget": 23, "spent": 7},
        "3": {"score": 0, "budget": 30}
      },
      "game": {"last_price": 7}
    }
  },
  {
    "name": "Two bids tied at 6 both fail, leaving standing_bid 0, so a later bid of 2 wins",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [13, 3, 5, 7, 9, 11]},
        "2": {"values": [13, 3, 5, 7, 9, 11]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 3, "options_include": 3, "times": 1},
      {"seat": 3, "options_include": 2, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 28, "score": 3, "spent": 2}
      },
      "game": {"last_price": 2}
    }
  },
  {
    "name": "A seat that passes in turn 1 becomes ineligible, so its bid of 10 in turn 2 is invalid",
    "rule": "R11",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [7, 3, 5, 9, 11, 13]},
        "2": {"values": [13, 3, 5, 7, 9, 11]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 10, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 28, "score": 5, "spent": 2},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 2}
    }
  },
  {
    "name": "Settlement adds onto existing budget, spent and score in round 4",
    "rule": "R12",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 13, 9, 11], "budget": 20, "score": 3, "spent": 10}},
      "game": {"round": 3}
    },
    "rules": [{"seat": 1, "options_include": 6, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 14, "spent": 16, "score": 10}},
      "game": {"round": 4, "last_price": 6}
    }
  },
  {
    "name": "With no bids the item goes unsold: last_price becomes 0 and nothing else changes",
    "rule": "R13",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"budget": 25, "score": 2, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 7}
    },
    "expect": {
      "players": {
        "1": {"budget": 25, "score": 2, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 2, "last_price": 0}
    }
  },
  {
    "name": "Winning an item of value 3 at price 8 gives a score of -5",
    "rule": "R14",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 9, 11, 13]}},
      "game": {"round": 0}
    },
    "rules": [{"seat": 1, "options_include": 8, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 22, "spent": 8, "score": -5}},
      "game": {"last_price": 8}
    }
  },
  {
    "name": "Game ends after round 6 and the highest score wins",
    "rule": "R15",
    "players": 3,
    "seed": 15,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13], "score": 10},
        "2": {"values": [3, 5, 7, 9, 13, 11], "score": 12},
        "3": {"values": [3, 5, 7, 9, 13, 11], "score": 4}
      },
      "game": {"round": 5}
    },
    "rules": [{"seat": 1, "options_include": 5, "times": 1}],
    "expect": {
      "winner": 1,
      "standings": {"1": 18, "2": 12, "3": 4},
      "players": {"1": {"budget": 25, "score": 18}},
      "game": {"round": 6, "last_price": 5}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Initial state: budget 30, score 0, spent 0, round 0, last_price 0",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 0, "last_price": 0}
    }
  },
  {
    "name": "Each player's values list holds 6 entries after setup (ordering is random, only length asserted)",
    "rule": "R2",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "lens": {"players": {"1": {"values": 6}, "2": {"values": 6}, "3": {"values": 6}, "4": {"values": 6}}}
    }
  },
  {
    "name": "Public results after a sale: highest of three distinct valid bids wins at its own bid",
    "rule": "R3",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"values": [11, 3, 5, 7, 9, 13]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 7, "times": 1},
      {"seat": 3, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 23, "score": 4, "spent": 7},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 7}
    }
  },
  {
    "name": "In round 3 the value used is entry 3 of the values list",
    "rule": "R4",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 9, 11, 13]}},
      "game": {"round": 2}
    },
    "rules": [{"seat": 1, "options_include": 2, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 28, "score": 5, "spent": 2}},
      "game": {"round": 3, "last_price": 2}
    }
  },
  {
    "name": "A round with talk and all passes advances the round and changes nothing else",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 0}
    }
  },
  {
    "name": "Reset clears a stale standing_bid and leader and makes everyone eligible, so a bid of 1 wins",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13], "eligible": false},
        "2": {"eligible": true}
      },
      "game": {"round": 0, "standing_bid": 5, "leader": 2}
    },
    "rules": [{"seat": 1, "options_include": 1, "times": 1}],
    "expect": {
      "players": {
        "1": {"budget": 29, "score": 2, "spent": 1},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 1}
    }
  },
  {
    "name": "Bid options run from 0 to the seat's budget; a seat with budget 0 is offered only 0",
    "rule": "R7",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"budget": 10},
        "3": {"budget": 0}
      },
      "game": {"round": 0}
    },
    "rules": [{"seat": 1, "options_include": 5, "times": 1}],
    "expect": {
      "offered": [{"seat": 2, "option": 10}, {"seat": 2, "option": 0}, {"seat": 3, "option": 0}],
      "not_offered": [{"seat": 2, "option": 11}, {"seat": 3, "option": 1}]
    }
  },
  {
    "name": "A bid equal to standing_bid is invalid, so the earlier bid of 5 wins",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [9, 3, 5, 7, 11, 13]},
        "2": {"values": [13, 3, 5, 7, 9, 11]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 5, "times": 1},
      {"seat": 2, "options_include": 4, "times": 1},
      {"seat": 2, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 25, "score": 4, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 5}
    }
  },
  {
    "name": "top_bid is the largest valid bid: bids 3, 7 and 5, so seat 2 wins at 7",
    "rule": "R9",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13]},
        "2": {"values": [11, 3, 5, 7, 9, 13]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 7, "times": 1},
      {"seat": 3, "options_include": 5, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"score": 0, "budget": 30},
        "2": {"score": 4, "budget": 23, "spent": 7},
        "3": {"score": 0, "budget": 30}
      },
      "game": {"last_price": 7}
    }
  },
  {
    "name": "Two bids tied at 6 both fail, leaving standing_bid 0, so a later bid of 2 wins",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [13, 3, 5, 7, 9, 11]},
        "2": {"values": [13, 3, 5, 7, 9, 11]},
        "3": {"values": [5, 3, 7, 9, 11, 13]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 3, "options_include": 3, "times": 1},
      {"seat": 3, "options_include": 2, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 30, "score": 0, "spent": 0},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 28, "score": 3, "spent": 2}
      },
      "game": {"last_price": 2}
    }
  },
  {
    "name": "A seat that passes in turn 1 becomes ineligible, so its bid of 10 in turn 2 is invalid",
    "rule": "R11",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [7, 3, 5, 9, 11, 13]},
        "2": {"values": [13, 3, 5, 7, 9, 11]}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 10, "times": 1}
    ],
    "expect": {
      "players": {
        "1": {"budget": 28, "score": 5, "spent": 2},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"last_price": 2}
    }
  },
  {
    "name": "Settlement adds onto existing budget, spent and score in round 4",
    "rule": "R12",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 13, 9, 11], "budget": 20, "score": 3, "spent": 10}},
      "game": {"round": 3}
    },
    "rules": [{"seat": 1, "options_include": 6, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 14, "spent": 16, "score": 10}},
      "game": {"round": 4, "last_price": 6}
    }
  },
  {
    "name": "With no bids the item goes unsold: last_price becomes 0 and nothing else changes",
    "rule": "R13",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"budget": 25, "score": 2, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 1, "last_price": 7}
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"budget": 25, "score": 2, "spent": 5},
        "2": {"budget": 30, "score": 0, "spent": 0},
        "3": {"budget": 30, "score": 0, "spent": 0}
      },
      "game": {"round": 2, "last_price": 0}
    }
  },
  {
    "name": "Winning an item of value 3 at price 8 gives a score of -5",
    "rule": "R14",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"values": [3, 5, 7, 9, 11, 13]}},
      "game": {"round": 0}
    },
    "rules": [{"seat": 1, "options_include": 8, "times": 1}],
    "expect": {
      "players": {"1": {"budget": 22, "spent": 8, "score": -5}},
      "game": {"last_price": 8}
    }
  },
  {
    "name": "Game ends after round 6 and the highest score wins",
    "rule": "R15",
    "players": 3,
    "seed": 15,
    "default": "decline",
    "given": {
      "players": {
        "1": {"values": [3, 5, 7, 9, 11, 13], "score": 10},
        "2": {"values": [3, 5, 7, 9, 13, 11], "score": 12},
        "3": {"values": [3, 5, 7, 9, 13, 11], "score": 4}
      },
      "game": {"round": 5}
    },
    "rules": [{"seat": 1, "options_include": 5, "times": 1}],
    "expect": {
      "winner": 1,
      "standings": {"1": 18, "2": 12, "3": 4},
      "players": {"1": {"budget": 25, "score": 18}},
      "game": {"round": 6, "last_price": 5}
    }
  }
]
```
````
