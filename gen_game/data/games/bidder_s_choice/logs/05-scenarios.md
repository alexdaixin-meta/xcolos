# 05 scenarios

- time: 2026-10-27T08:39:33+00:00 (25.4s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 952a1b8aacdd1ca8, reply sha256 0e4bcf08f328e106

## Sent

````
SPEC:
{
  "name": "Bidder's Choice: Shared Worth",
  "summary": "Over 6 rounds players talk, then bid sealed coins for the right to take one of six objects A-F that each values privately; the highest coins plus own object values wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "object_count_total": 6,
    "starting_coins": 20,
    "value_1": 2,
    "value_2": 4,
    "value_3": 6,
    "value_4": 8,
    "value_5": 10,
    "value_6": 14,
    "values_total_per_player": 44,
    "rounds": 6,
    "min_bid": 0,
    "objects_won_per_round": 1
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 20,
        "meaning": "Coins the player currently holds. Everyone can track this because winning prices are announced.",
        "observable": true
      },
      {
        "key": "values",
        "type": "list",
        "visible": "ally",
        "initial": "a private random ordering of [2,4,6,8,10,14]; position 1..6 is the player's value for object A..F",
        "meaning": "The player's private value for each object.",
        "observable": false
      },
      {
        "key": "holdings",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Names of the objects this player has taken.",
        "observable": true
      },
      {
        "key": "object_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many objects the player holds. Used to break ties.",
        "observable": true
      },
      {
        "key": "object_points",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of the player's own private values for the objects they hold.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's sealed bid this round.",
        "observable": false
      },
      {
        "key": "last_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's bid in the last resolved round, revealed at the announcement.",
        "observable": true
      },
      {
        "key": "final_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "coins + object_points, set and revealed after round 6.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "pool",
        "type": "list",
        "visible": "public",
        "initial": [
          "A",
          "B",
          "C",
          "D",
          "E",
          "F"
        ],
        "meaning": "Objects not yet taken.",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round number, from 1 to 6.",
        "observable": true
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest bid this round.",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that won this round.",
        "observable": true
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The amount the round winner paid.",
        "observable": true
      },
      {
        "key": "last_object",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The object taken this round.",
        "observable": true
      }
    ]
  },
  "setup": [
    "The pool is set to the six objects A, B, C, D, E and F.",
    "Each player's coins are set to 20.",
    "Each player is privately dealt a random assignment of the values 2, 4, 6, 8, 10 and 14 to objects A to F, one value per object, independently of the other players. This is stored in that player's values list, visible only to them, and totals 44.",
    "Each player's holdings start empty, with object_count 0 and object_points 0.",
    "A sync step sends each player their own state."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; announce 'Round {round} of 6'."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short free text: one public message, not binding and possibly false",
      "effect": "After all are in, each message is broadcast to all as 'Seat {seat} says: {value}'."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to that player's coins",
      "effect": "Sets each player's bid. Nobody sees any bid until all are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "high_bid = the maximum bid. Among players whose bid == high_bid, keep those with the minimum object_count. winner_seat = that player, or one of them chosen at random with equal chance if several remain. price = high_bid. Each player's last_bid = bid."
    },
    {
      "action": "update",
      "who": "the winner_seat",
      "answer": null,
      "effect": "The winner's coins -= price. The paid coins leave the game. All other players pay nothing."
    },
    {
      "action": "ask",
      "who": "the winner_seat",
      "answer": "one object name from the current pool",
      "effect": "last_object = the choice; remove it from pool; append it to the winner's holdings; the winner's object_count += 1; the winner's object_points += the winner's values entry for that object (A=1st ... F=6th)."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every seat's last_bid, winner_seat, price and last_object. Private values are not revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == 6: each player's final_score = coins + object_points, and every player's values and object_points are revealed to everyone."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round == 6; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round == 6",
    "rank_by": "you.coins + you.object_points",
    "decided_by": "Each player's standing is their remaining coins plus the sum of their own private values for the objects they hold. The highest wins. Players level at the top share the result, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has 20 coins, no objects, and the pool is A, B, C, D, E, F."
    },
    {
      "id": "R2",
      "text": "When values are dealt, then each player privately receives the values 2, 4, 6, 8, 10 and 14, one per object A-F in random order, independently of others, totalling 44."
    },
    {
      "id": "R3",
      "text": "When a player's values are dealt, then only that player sees them until the game ends."
    },
    {
      "id": "R4",
      "text": "When a round begins, then every player writes one short message at the same time, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R5",
      "text": "When bidding, then every player simultaneously submits a whole-number bid from 0 to their current coins."
    },
    {
      "id": "R6",
      "text": "When one player has the strictly highest bid, then that player wins the round."
    },
    {
      "id": "R7",
      "text": "When several players tie for the highest bid, then the tied player with the fewest objects wins."
    },
    {
      "id": "R8",
      "text": "When tied players also hold equally few objects, then the winner is chosen at random among them with equal chance."
    },
    {
      "id": "R9",
      "text": "When a player wins a round with bid X, then their coins drop by X, and every other player's coins are unchanged."
    },
    {
      "id": "R10",
      "text": "When a player wins a round, then they choose one object still in the pool; it is removed from the pool, added to their holdings, and their object_points rise by their own value for it."
    },
    {
      "id": "R11",
      "text": "When a player has already won rounds, then they may still win again; there is no limit."
    },
    {
      "id": "R12",
      "text": "When a round resolves, then everyone is told all bids, the winner, the price and the object taken, but no private values."
    },
    {
      "id": "R13",
      "text": "When round 6 ends, then the game ends with the pool empty and all values revealed."
    },
    {
      "id": "R14",
      "text": "When the game ends, then each player's final score is coins + object_points, and the highest score wins; tied top scores share the result (a draw)."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every seat",
      "options": "any short free-text message"
    },
    {
      "question": "Sealed bid",
      "who": "every seat",
      "options": "whole numbers from 0 to that seat's current coins (only 0 if the seat has 0 coins)"
    },
    {
      "question": "Pick an object",
      "who": "only the round winner",
      "options": "exactly the object names still in the pool; the other seats are not asked"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer chose 4, so it is kept as suggested. Fewer than 3 leaves only one rival, so there is no real auction or tie-breaking pressure. More than 5 makes six objects too scarce for one bid to matter and makes the talk long."
    },
    {
      "what": "Keep the simultaneous talk poll before each bid",
      "why": "The source specifies it. Players' values differ, so they disagree about which objects are worth fighting for. Talk lets them bluff about their values or about intentions to stay out, which can steer rivals' bids."
    },
    {
      "what": "Store private values as a 6-entry list ordered A to F",
      "why": "This lets the pick add the value by position arithmetically."
    },
    {
      "what": "Keep a public last_bid beside the hidden bid",
      "why": "Bids are sealed during the poll but must all be announced afterwards."
    },
    {
      "what": "Players can see their own strategy points",
      "why": "The source says the player sees their own assignment. Showing them their running sum of held values is just derived from that."
    }
  ],
  "simplifications": [
    {
      "what": "A draw is represented as a shared win among the players tied at the top",
      "why": "The engine has no separate draw; tied top players share the win, which matches a draw between them."
    },
    {
      "what": "The final value reveal is done by an update step conditioned on round == 6, inside the round",
      "why": "The step list repeats each round; a condition on a single step avoids needing a separate end block."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, holdings, object_count, last_bid, final_score; table: pool, round, winner_seat, price, last_object.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"Setup: 20 coins each, no objects, full pool","rule":"R1","players":4,"rounds":0,
 "expect":{"players":{"1":{"coins":20,"holdings":[],"object_count":0},"2":{"coins":20,"holdings":[],"object_count":0},"3":{"coins":20,"holdings":[],"object_count":0},"4":{"coins":20,"holdings":[],"object_count":0}},
 "game":{"pool":["A","B","C","D","E","F"],"round":0}}},
{"name":"Each player is dealt six values, one per object (the order is random, so only the count is checked)","rule":"R2","players":4,"rounds":0,
 "expect":{"lens":{"players":{"1":{"values":6},"2":{"values":6},"3":{"values":6},"4":{"values":6}},"game":{"pool":6}}}},
{"name":"Every seat has its own private value list of six entries (privacy itself is not observable)","rule":"R3","players":3,"rounds":0,
 "expect":{"lens":{"players":{"1":{"values":6},"2":{"values":6},"3":{"values":6}}}}},
{"name":"A round runs talk then bidding: round advances to 1 and bids are recorded","rule":"R4","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":3,"times":1},{"seat":1,"options_include":"A"}],
 "expect":{"game":{"round":1,"winner_seat":1,"price":3},"players":{"1":{"last_bid":3},"2":{"last_bid":0},"3":{"last_bid":0}}}},
{"name":"Bids are offered only from 0 up to the seat's coins","rule":"R5","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"2":{"coins":5}}},
 "rules":[{"seat":1,"options_include":1},{"seat":1,"options_include":"A"}],
 "expect":{"offered":[{"seat":2,"option":5},{"seat":2,"option":0},{"seat":1,"option":20}],
 "not_offered":[{"seat":2,"option":6},{"seat":1,"option":21}]}},
{"name":"Strictly highest bid wins the round","rule":"R6","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":2,"options_include":7},{"seat":3,"options_include":5},{"seat":2,"options_include":"B"}],
 "expect":{"game":{"winner_seat":2,"price":7,"last_object":"B"},"players":{"2":{"coins":13,"last_bid":7},"3":{"coins":20,"last_bid":5},"1":{"coins":20,"last_bid":0}}}},
{"name":"Tie on the highest bid goes to the tied seat holding fewer objects","rule":"R7","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"holdings":["A"],"object_count":1}},"game":{"pool":["B","C","D","E","F"],"round":1}},
 "rules":[{"seat":1,"options_include":6},{"seat":2,"options_include":6},{"seat":2,"options_include":"C"}],
 "expect":{"game":{"winner_seat":2,"price":6,"last_object":"C","pool":["B","D","E","F"]},"players":{"1":{"coins":20,"object_count":1},"2":{"coins":14,"object_count":1,"holdings":["C"]},"3":{"coins":20}}}},
{"name":"Tie with equal object counts: a random tied seat wins (only chance-free facts are checked)","rule":"R8","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":6},{"seat":2,"options_include":6},{"seat":3,"options_include":4},{"seat":1,"options_include":"A"},{"seat":2,"options_include":"A"}],
 "expect":{"game":{"price":6,"last_object":"A","pool":["B","C","D","E","F"]},"players":{"3":{"coins":20,"object_count":0,"last_bid":4},"1":{"last_bid":6},"2":{"last_bid":6}}}},
{"name":"Winner pays their bid; losers pay nothing","rule":"R9","players":4,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":9},{"seat":2,"options_include":4},{"seat":3,"options_include":4},{"seat":4,"options_include":4},{"seat":1,"options_include":"E"}],
 "expect":{"game":{"winner_seat":1,"price":9},"players":{"1":{"coins":11},"2":{"coins":20},"3":{"coins":20},"4":{"coins":20}}}},
{"name":"Winner picks an object: it leaves the pool and joins their holdings","rule":"R10","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"D"}],
 "expect":{"game":{"last_object":"D","pool":["A","B","C","E","F"]},"players":{"1":{"holdings":["D"],"object_count":1,"coins":18}},
 "not_offered":[{"seat":2,"option":"D"},{"seat":3,"option":"D"}]}},
{"name":"A seat that already won rounds can win again","rule":"R11","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"holdings":["A","B"],"object_count":2,"coins":15}},"game":{"pool":["C","D","E","F"],"round":2}},
 "rules":[{"seat":1,"options_include":1},{"seat":1,"options_include":"C"}],
 "expect":{"game":{"winner_seat":1,"price":1,"pool":["D","E","F"],"round":3},"players":{"1":{"holdings":["A","B","C"],"object_count":3,"coins":14}}}},
{"name":"After resolution all bids, winner, price and object are public","rule":"R12","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":3},{"seat":2,"options_include":2},{"seat":3,"options_include":1},{"seat":1,"options_include":"F"}],
 "expect":{"game":{"winner_seat":1,"price":3,"last_object":"F"},"players":{"1":{"last_bid":3,"coins":17},"2":{"last_bid":2,"coins":20},"3":{"last_bid":1,"coins":20}}}},
{"name":"Round 6 ends the game with the pool empty and final scores set","rule":"R13","players":3,"default":"decline",
 "given":{"game":{"round":5,"pool":["F"]},
  "players":{"1":{"coins":10,"values":[2,4,6,8,10,14],"holdings":["A","B"],"object_count":2,"object_points":6},
   "2":{"coins":12,"values":[14,10,8,6,4,2],"holdings":["C","D"],"object_count":2,"object_points":14},
   "3":{"coins":5,"values":[2,4,6,8,10,14],"holdings":["E"],"object_count":1,"object_points":10}}},
 "rules":[{"seat":3,"options_include":5},{"seat":3,"options_include":"F"}],
 "expect":{"winner":2,"standings":{"1":16,"2":26,"3":24},
  "game":{"pool":[],"round":6,"winner_seat":3,"price":5,"last_object":"F"},
  "players":{"1":{"final_score":16},"2":{"final_score":26},"3":{"final_score":24,"coins":0,"holdings":["E","F"],"object_count":2}}}},
{"name":"Final score is coins + object points; tied top scores share the win","rule":"R14","players":3,"default":"decline",
 "given":{"game":{"round":5,"pool":["F"]},
  "players":{"1":{"coins":10,"values":[14,10,8,6,4,2],"holdings":["D","E"],"object_count":2,"object_points":10},
   "2":{"coins":10,"values":[2,4,6,8,10,14],"holdings":["A"],"object_count":1,"object_points":2},
   "3":{"coins":5,"values":[14,2,4,6,8,10],"holdings":["B","C"],"object_count":2,"object_points":6}}},
 "rules":[{"seat":2,"options_include":6},{"seat":2,"options_include":"F"}],
 "expect":{"winner":[1,2],"standings":{"1":20,"2":20,"3":11},
  "players":{"1":{"final_score":20,"coins":10},"2":{"final_score":20,"coins":4,"holdings":["A","F"]},"3":{"final_score":11,"coins":5}},
  "game":{"pool":[],"round":6}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"Setup: 20 coins each, no objects, full pool","rule":"R1","players":4,"rounds":0,"default":"decline",
 "rules":[{"seat":1,"options_include":0,"times":"all"}],
 "expect":{"players":{"1":{"coins":20,"holdings":[],"object_count":0},"2":{"coins":20,"holdings":[],"object_count":0},"3":{"coins":20,"holdings":[],"object_count":0},"4":{"coins":20,"holdings":[],"object_count":0}},
 "game":{"pool":["A","B","C","D","E","F"],"round":0}}},
{"name":"Each player is dealt six values, one per object (the order is random, so only the count is checked)","rule":"R2","players":4,"rounds":0,"default":"decline",
 "rules":[{"seat":1,"options_include":0,"times":"all"}],
 "expect":{"lens":{"players":{"1":{"values":6},"2":{"values":6},"3":{"values":6},"4":{"values":6}},"game":{"pool":6}}}},
{"name":"Every seat has its own private value list of six entries (privacy itself is not observable)","rule":"R3","players":3,"rounds":0,"default":"decline",
 "rules":[{"seat":1,"options_include":0,"times":"all"}],
 "expect":{"lens":{"players":{"1":{"values":6},"2":{"values":6},"3":{"values":6}}}}},
{"name":"A round runs talk then bidding: round advances to 1 and bids are recorded","rule":"R4","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":3,"times":1},{"seat":1,"options_include":"A"}],
 "expect":{"game":{"round":1,"winner_seat":1,"price":3},"players":{"1":{"last_bid":3},"2":{"last_bid":0},"3":{"last_bid":0}}}},
{"name":"Bids are offered only from 0 up to the seat's coins","rule":"R5","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"2":{"coins":5}}},
 "rules":[{"seat":1,"options_include":1},{"seat":1,"options_include":"A"}],
 "expect":{"offered":[{"seat":2,"option":5},{"seat":2,"option":0},{"seat":1,"option":20}],
 "not_offered":[{"seat":2,"option":6},{"seat":1,"option":21}]}},
{"name":"Strictly highest bid wins the round","rule":"R6","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":2,"options_include":7},{"seat":3,"options_include":5},{"seat":2,"options_include":"B"}],
 "expect":{"game":{"winner_seat":2,"price":7,"last_object":"B"},"players":{"2":{"coins":13,"last_bid":7},"3":{"coins":20,"last_bid":5},"1":{"coins":20,"last_bid":0}}}},
{"name":"Tie on the highest bid goes to the tied seat holding fewer objects","rule":"R7","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"holdings":["A"],"object_count":1}},"game":{"pool":["B","C","D","E","F"],"round":1}},
 "rules":[{"seat":1,"options_include":6},{"seat":2,"options_include":6},{"seat":2,"options_include":"C"}],
 "expect":{"game":{"winner_seat":2,"price":6,"last_object":"C","pool":["B","D","E","F"]},"players":{"1":{"coins":20,"object_count":1},"2":{"coins":14,"object_count":1,"holdings":["C"]},"3":{"coins":20}}}},
{"name":"Tie with equal object counts: a random tied seat wins (only chance-free facts are checked)","rule":"R8","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":6},{"seat":2,"options_include":6},{"seat":3,"options_include":4},{"seat":1,"options_include":"A"},{"seat":2,"options_include":"A"}],
 "expect":{"game":{"price":6,"last_object":"A","pool":["B","C","D","E","F"]},"players":{"3":{"coins":20,"object_count":0,"last_bid":4},"1":{"last_bid":6},"2":{"last_bid":6}}}},
{"name":"Winner pays their bid; losers pay nothing","rule":"R9","players":4,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":9},{"seat":2,"options_include":4},{"seat":3,"options_include":4},{"seat":4,"options_include":4},{"seat":1,"options_include":"E"}],
 "expect":{"game":{"winner_seat":1,"price":9},"players":{"1":{"coins":11},"2":{"coins":20},"3":{"coins":20},"4":{"coins":20}}}},
{"name":"Winner picks an object: it leaves the pool and joins their holdings","rule":"R10","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":2},{"seat":1,"options_include":"D"}],
 "expect":{"game":{"last_object":"D","pool":["A","B","C","E","F"]},"players":{"1":{"holdings":["D"],"object_count":1,"coins":18}},
 "not_offered":[{"seat":2,"option":"D"},{"seat":3,"option":"D"}]}},
{"name":"A seat that already won rounds can win again","rule":"R11","players":3,"rounds":1,"default":"decline",
 "given":{"players":{"1":{"holdings":["A","B"],"object_count":2,"coins":15}},"game":{"pool":["C","D","E","F"],"round":2}},
 "rules":[{"seat":1,"options_include":1},{"seat":1,"options_include":"C"}],
 "expect":{"game":{"winner_seat":1,"price":1,"pool":["D","E","F"],"round":3},"players":{"1":{"holdings":["A","B","C"],"object_count":3,"coins":14}}}},
{"name":"After resolution all bids, winner, price and object are public","rule":"R12","players":3,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":3},{"seat":2,"options_include":2},{"seat":3,"options_include":1},{"seat":1,"options_include":"F"}],
 "expect":{"game":{"winner_seat":1,"price":3,"last_object":"F"},"players":{"1":{"last_bid":3,"coins":17},"2":{"last_bid":2,"coins":20},"3":{"last_bid":1,"coins":20}}}},
{"name":"Round 6 ends the game with the pool empty and final scores set","rule":"R13","players":3,"default":"decline",
 "given":{"game":{"round":5,"pool":["F"]},
  "players":{"1":{"coins":10,"values":[2,4,6,8,10,14],"holdings":["A","B"],"object_count":2,"object_points":6},
   "2":{"coins":12,"values":[14,10,8,6,4,2],"holdings":["C","D"],"object_count":2,"object_points":14},
   "3":{"coins":5,"values":[2,4,6,8,10,14],"holdings":["E"],"object_count":1,"object_points":10}}},
 "rules":[{"seat":3,"options_include":5},{"seat":3,"options_include":"F"}],
 "expect":{"winner":2,"standings":{"1":16,"2":26,"3":24},
  "game":{"pool":[],"round":6,"winner_seat":3,"price":5,"last_object":"F"},
  "players":{"1":{"final_score":16},"2":{"final_score":26},"3":{"final_score":24,"coins":0,"holdings":["E","F"],"object_count":2}}}},
{"name":"Final score is coins + object points; tied top scores share the win","rule":"R14","players":3,"default":"decline",
 "given":{"game":{"round":5,"pool":["F"]},
  "players":{"1":{"coins":10,"values":[14,10,8,6,4,2],"holdings":["D","E"],"object_count":2,"object_points":10},
   "2":{"coins":10,"values":[2,4,6,8,10,14],"holdings":["A"],"object_count":1,"object_points":2},
   "3":{"coins":5,"values":[14,2,4,6,8,10],"holdings":["B","C"],"object_count":2,"object_points":6}}},
 "rules":[{"seat":2,"options_include":6},{"seat":2,"options_include":"F"}],
 "expect":{"winner":[1,2],"standings":{"1":20,"2":20,"3":11},
  "players":{"1":{"final_score":20,"coins":10},"2":{"final_score":20,"coins":4,"holdings":["A","F"]},"3":{"final_score":11,"coins":5}},
  "game":{"pool":[],"round":6}}}
]
````
