# 32 scenarios

- time: 2026-10-27T09:09:27+00:00 (37.6s)  model: claude-opus-5-5
- system prompt: [system/2ddacf4d-scenarios.md](system/2ddacf4d-scenarios.md) (sha256 2ddacf4d74fa3789)
- sent sha256 3b60d56b1fe9f2ab, reply sha256 ce399d918dff883d

## Sent

````
SPEC:
{
  "name": "Bidder's Choice: Sealed Pool",
  "summary": "Over 6 rounds, players talk and then place sealed bids from 20 coins; each round's winner pays and picks one of six objects that every player values privately, and the score is coins left plus own values of held objects.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 3
  },
  "parameters": {
    "starting_coins": 20,
    "object_count": 6,
    "value_1": 2,
    "value_2": 4,
    "value_3": 6,
    "value_4": 8,
    "value_5": 10,
    "value_6": 14,
    "value_total": 44,
    "rounds": 6,
    "talk_max_words": 40,
    "min_bid": 0,
    "tiebreak_key_multiplier": 10,
    "min_players": 3,
    "max_players": 5,
    "suggested_players": 3
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 20,
        "meaning": "Coins the player still holds.",
        "observable": true
      },
      {
        "key": "holdings",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Letters of the objects the player has won.",
        "observable": true
      },
      {
        "key": "holdings_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of objects in holdings, used for the tie-break.",
        "observable": false
      },
      {
        "key": "value_a",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object A, dealt at setup.",
        "observable": false
      },
      {
        "key": "value_b",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object B.",
        "observable": false
      },
      {
        "key": "value_c",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object C.",
        "observable": false
      },
      {
        "key": "value_d",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object D.",
        "observable": false
      },
      {
        "key": "value_e",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object E.",
        "observable": false
      },
      {
        "key": "value_f",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for object F.",
        "observable": false
      },
      {
        "key": "value_bag",
        "type": "list",
        "visible": "ally",
        "initial": [
          2,
          4,
          6,
          8,
          10,
          14
        ],
        "meaning": "The player's own six values, not yet assigned to objects. They are drawn at random during setup, so the list is empty after setup.",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message, at most 40 words, shown after all are in.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid, revealed to all in the reveal step.",
        "observable": false
      },
      {
        "key": "bid_key",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "bid * 10 + (6 - holdings_count). The highest value wins, and a tie at the top means no sale.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final score: coins + the sum of own values of held objects, computed after round 6.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number, from 1 to 6.",
        "observable": true
      },
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
        "meaning": "Objects still available.",
        "observable": true
      },
      {
        "key": "top_key",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Highest bid_key this round.",
        "observable": false
      },
      {
        "key": "top_count",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Number of players whose bid_key equals top_key.",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this round's winner, or 0 for no sale.",
        "observable": true
      },
      {
        "key": "taken_object",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Object taken this round, or empty if there was no sale.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player starts with coins = 20, empty holdings and holdings_count = 0.",
    "The table pool is set to [A, B, C, D, E, F] and round = 0.",
    "Each player's value_bag starts as [2, 4, 6, 8, 10, 14]. For that player, value_a through value_f are assigned in turn: each draws one value at random from the player's own value_bag and removes it, so each player gets an independent random permutation that totals 44.",
    "Each player's values are visible only to that player (ally)."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; winner_seat = 0; taken_object = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, pool, and every player's coins and holdings."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text, at most 40 words (words beyond the 40th are dropped)",
      "effect": "Set each player's message, truncated to 40 words. Once all are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to you.coins",
      "effect": "Set each player's bid. A missing, non-integer, negative or over-coins answer sets bid = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, bid_key = bid * 10 + (6 - holdings_count); top_key = max of bid_key; top_count = number of players with bid_key == top_key; winner_seat = the seat with bid_key == top_key if top_count == 1, else 0."
    },
    {
      "action": "update",
      "who": "the winner (when winner_seat != 0)",
      "answer": null,
      "effect": "The winner's coins -= the winner's bid."
    },
    {
      "action": "ask",
      "who": "the winner (when winner_seat != 0)",
      "answer": "one object letter from pool",
      "effect": "Set taken_object to the chosen letter. If there is no valid answer, taken_object = the pool object with the highest of the winner's own values (ties: earliest letter)."
    },
    {
      "action": "update",
      "who": "the winner (when winner_seat != 0)",
      "answer": null,
      "effect": "Remove taken_object from pool; append it to the winner's holdings; the winner's holdings_count += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal every player's bid, the winner (or 'no sale' if winner_seat == 0), and taken_object."
    },
    {
      "action": "update",
      "who": "all players (when round == 6)",
      "answer": null,
      "effect": "Pool objects are discarded (pool = []). For each player, score = coins + the sum of value_x over each object x in holdings."
    },
    {
      "action": "tell",
      "who": "all players (when round == 6)",
      "answer": null,
      "effect": "Reveal all players' value_a through value_f and every score."
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
    "rank_by": "you.score",
    "decided_by": "Each player's standing is his final score: coins left plus the sum of his own values for the objects he holds. The highest score wins, and players level at the top share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has 20 coins, no objects, and the pool is A, B, C, D, E, F."
    },
    {
      "id": "R2",
      "text": "When values are dealt, then each player's values for A through F are a random permutation of 2, 4, 6, 8, 10, 14, totalling 44, and are visible only to that player."
    },
    {
      "id": "R3",
      "text": "When a round begins, then the round number, pool, and every player's coins and holdings are announced to all."
    },
    {
      "id": "R4",
      "text": "When players talk, then every player submits one message simultaneously, words beyond the 40th are dropped, and all messages are then shown to everyone."
    },
    {
      "id": "R5",
      "text": "When bids are made, then every player simultaneously bids a whole number from 0 to his current coins."
    },
    {
      "id": "R6",
      "text": "When a bid is missing, not a whole number, negative or above the bidder's coins, then it counts as 0."
    },
    {
      "id": "R7",
      "text": "When one player has the strictly highest bid, then he wins the round."
    },
    {
      "id": "R8",
      "text": "When several players share the highest bid, then the one among them with the fewest objects wins."
    },
    {
      "id": "R9",
      "text": "When several players share both the highest bid and the fewest objects, then there is no sale: nobody pays, the pool is unchanged, and the round still counts."
    },
    {
      "id": "R10",
      "text": "When there is a winner, then his coins decrease by his bid (for example, a bid of 7 from 20 coins leaves 13)."
    },
    {
      "id": "R11",
      "text": "When the winner names an object in the pool, then it leaves the pool and is added to his holdings."
    },
    {
      "id": "R12",
      "text": "When the winner gives no valid object, then he receives the pool object with his highest own value, with ties going to the earliest letter."
    },
    {
      "id": "R13",
      "text": "When a player has won earlier rounds, then he may still bid and win again."
    },
    {
      "id": "R14",
      "text": "When a round ends, then all bids, the winner or 'no sale', and the object taken are announced to all."
    },
    {
      "id": "R15",
      "text": "When round 6 has been played, then the game ends and objects left in the pool are discarded."
    },
    {
      "id": "R16",
      "text": "When the game ends, then each player's score = coins + the sum of his own values for his held objects, and all values are revealed."
    },
    {
      "id": "R17",
      "text": "When the game ends, then the highest score wins, and a shared highest score is a draw among those players."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every player",
      "options": "free text of at most 40 words"
    },
    {
      "question": "Sealed bid",
      "who": "every player",
      "options": "any whole number from 0 to that player's current coins"
    },
    {
      "question": "Pick an object",
      "who": "the round's winner only (no one when there is no sale)",
      "options": "each object letter currently in pool"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 3",
      "why": "The designer suggests 3, which is kept. 3 is the minimum where the fewest-objects tie-break and rival bidding create real competition. Above 5, there is less than one object per player and the talk grows long."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules specify simultaneous talk. Players disagree because their private values differ, so bluffing about which object one wants, or about intending to sit out, can steer rivals' bids."
    },
    {
      "what": "Tie-break encoded as bid_key = bid * 10 + (6 - holdings_count)",
      "why": "Holdings never exceed 6, so this single number orders players by bid first and then by fewest objects. A tie in bid_key at the top is exactly the no-sale case."
    },
    {
      "what": "Values stored as six ally attributes value_a through value_f, dealt by drawing from each player's own value_bag list",
      "why": "This gives each player an independent random permutation, as the rules require, and declares the dealing source as state."
    },
    {
      "what": "bid_key is an ally player attribute",
      "why": "It is a scratch number derived from the player's own bid, so only the owner may see it until bids are revealed."
    },
    {
      "what": "Score computed only after round 6",
      "why": "A public running score would leak private values."
    },
    {
      "what": "Strategy note",
      "why": "A thoughtful player bids up only for his high-value objects, shades bids against rivals' remaining coins, uses holding few objects as a tie-break edge, and bluffs in talk. A thoughtless one overpays for low-value objects."
    }
  ],
  "simplifications": [
    {
      "what": "A draw at the top is represented as a shared win among the tied players",
      "why": "The engine has no separate draw; players level at the top share the win."
    },
    {
      "what": "The pick is offered as a choice from the current pool, so an invalid letter cannot be chosen; the fallback applies only when there is no answer",
      "why": "Choice lists come from the pool list. The source's fallback rule is still kept."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, holdings, score; table: round, pool, winner_seat.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup: 20 coins each, no holdings, full pool, round 0", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"coins": 20, "holdings": []}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"round": 0, "pool": ["A", "B", "C", "D", "E", "F"]},
              "lens": {"game": {"pool": 6}, "players": {"1": {"holdings": 0}, "2": {"holdings": 0}, "3": {"holdings": 0}}}}},

  {"name": "Dealt values total 44 whatever the permutation: holding all six objects scores coins + 44", "rule": "R2", "players": 3,
   "given": {"players": {"1": {"coins": 20, "holdings": ["A", "B", "C", "D", "E"], "holdings_count": 5}},
             "game": {"round": 5, "pool": ["F"]}},
   "rules": [{"seat": 1, "options_include": 1, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "F"}],
   "expect": {"winner": 1,
              "standings": {"1": 63, "2": 20, "3": 20},
              "players": {"1": {"coins": 19, "holdings": ["A", "B", "C", "D", "E", "F"], "score": 63}, "2": {"score": 20}, "3": {"score": 20}},
              "game": {"pool": []}}},

  {"name": "A round begins: the round number advances to 1", "rule": "R3", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1}}},

  {"name": "After the talk, every player is still asked for a sealed bid", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1},
              "offered": [{"seat": 1, "option": 0}, {"seat": 2, "option": 0}, {"seat": 3, "option": 0}]}},

  {"name": "The bid range runs from 0 to the bidder's current coins", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"coins": 5}}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 5, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 20}, "2": {"coins": 0, "holdings": ["A"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2},
              "offered": [{"seat": 2, "option": 5}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 2, "option": 6}, {"seat": 1, "option": 21}]}},

  {"name": "An over-coins bid cannot be made: seat 1 falls to the default bid of 0 and seat 2 wins with a bid of 1", "rule": "R6", "players": 3, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 25, "times": "all"},
             {"seat": 2, "options_include": 1, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 20}, "2": {"coins": 19, "holdings": ["A"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2},
              "not_offered": [{"seat": 1, "option": 25}]}},

  {"name": "The strictly highest bid wins the round", "rule": "R7", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "B"}],
   "expect": {"players": {"1": {"coins": 13, "holdings": ["B"]}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"winner_seat": 1, "pool": ["A", "C", "D", "E", "F"]}}},

  {"name": "Tied highest bid: the bidder with fewer objects wins", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"holdings": ["A"], "holdings_count": 1}}, "game": {"pool": ["B", "C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 4, "times": "all"},
             {"seat": 2, "options_include": 4, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "B"}],
   "expect": {"players": {"1": {"coins": 20, "holdings": ["A"]}, "2": {"coins": 16, "holdings": ["B"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2, "pool": ["C", "D", "E", "F"]},
              "not_offered": [{"seat": 1, "option": "C"}]}},

  {"name": "Tie on both bid and object count: no sale, nobody pays, the pool is unchanged", "rule": "R9", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4, "times": "all"},
             {"seat": 2, "options_include": 4, "times": "all"},
             {"seat": 3, "options_include": 2, "times": "all"}],
   "expect": {"players": {"1": {"coins": 20, "holdings": []}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"winner_seat": 0, "round": 1, "pool": ["A", "B", "C", "D", "E", "F"]},
              "not_offered": [{"seat": 1, "option": "A"}, {"seat": 2, "option": "A"}, {"seat": 3, "option": "A"}]}},

  {"name": "The winner pays his bid: 12 coins minus a bid of 5 leaves 7", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"coins": 12}}},
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 2, "times": "all"},
             {"seat": 3, "options_include": 1, "times": "all"},
             {"seat": 1, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 7}, "2": {"coins": 20}, "3": {"coins": 20}}, "game": {"winner_seat": 1}}},

  {"name": "The named object leaves the pool and joins the winner's holdings", "rule": "R11", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "D"}],
   "expect": {"players": {"1": {"coins": 15, "holdings": ["D"]}},
              "game": {"pool": ["A", "B", "C", "E", "F"], "winner_seat": 1},
              "offered": [{"seat": 1, "option": "D"}]}},

  {"name": "Unscripted pick: the winner gets A, his highest-valued object", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10}}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"coins": 17, "holdings": ["A"]}},
              "game": {"pool": ["B", "C", "D", "E", "F"], "winner_seat": 1}}},

  {"name": "A player who already holds objects can win again", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"holdings": ["A", "B"], "holdings_count": 2}}, "game": {"pool": ["C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "C"}],
   "expect": {"players": {"1": {"coins": 15, "holdings": ["A", "B", "C"]}, "2": {"coins": 20}},
              "game": {"winner_seat": 1, "pool": ["D", "E", "F"]}}},

  {"name": "At round end the winner's seat is announced", "rule": "R14", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2, "times": "all"},
             {"seat": 2, "options_include": 2, "times": "all"},
             {"seat": 3, "options_include": 6, "times": "all"},
             {"seat": 3, "options_include": "E"}],
   "expect": {"players": {"3": {"coins": 14, "holdings": ["E"]}},
              "game": {"winner_seat": 3, "pool": ["A", "B", "C", "D", "F"]}}},

  {"name": "After round 6 the game ends and leftover pool objects are discarded", "rule": "R15", "players": 3,
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"winner": [1, 2, 3],
              "standings": {"1": 20, "2": 20, "3": 20},
              "players": {"1": {"score": 20}, "2": {"score": 20}, "3": {"score": 20}},
              "game": {"round": 6, "pool": [], "winner_seat": 0}}},

  {"name": "Final score is coins plus the player's own values of the objects he holds", "rule": "R16", "players": 3,
   "given": {"players": {"1": {"coins": 10, "holdings": ["A"], "holdings_count": 1, "value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10},
                         "2": {"coins": 20, "holdings": ["B"], "holdings_count": 1, "value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10},
                         "3": {"coins": 15, "holdings": [], "holdings_count": 0, "value_a": 2, "value_b": 4, "value_c": 8, "value_d": 6, "value_e": 10, "value_f": 14}},
             "game": {"round": 5, "pool": ["C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": "C"}],
   "expect": {"winner": 1,
              "standings": {"1": 24, "2": 22, "3": 23},
              "players": {"1": {"score": 24, "coins": 10}, "2": {"score": 22, "coins": 20}, "3": {"score": 23, "coins": 15, "holdings": ["C"]}},
              "game": {"pool": []}}},

  {"name": "A shared highest score is a shared win", "rule": "R17", "players": 3,
   "given": {"players": {"1": {"coins": 20, "holdings": [], "holdings_count": 0},
                         "2": {"coins": 16, "holdings": ["A"], "holdings_count": 1, "value_a": 4, "value_b": 2, "value_c": 6, "value_d": 8, "value_e": 10, "value_f": 14},
                         "3": {"coins": 10, "holdings": [], "holdings_count": 0}},
             "game": {"round": 5, "pool": ["B", "C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 20, "2": 20, "3": 10},
              "players": {"1": {"score": 20}, "2": {"score": 20}, "3": {"score": 10}},
              "game": {"pool": [], "winner_seat": 0}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Setup: 20 coins each, no holdings, full pool, round 0", "rule": "R1", "players": 3, "rounds": 0,
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"coins": 20, "holdings": []}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"round": 0, "pool": ["A", "B", "C", "D", "E", "F"]},
              "lens": {"game": {"pool": 6}, "players": {"1": {"holdings": 0}, "2": {"holdings": 0}, "3": {"holdings": 0}}}}},

  {"name": "Dealt values total 44 whatever the permutation: holding all six objects scores coins + 44", "rule": "R2", "players": 3,
   "given": {"players": {"1": {"coins": 20, "holdings": ["A", "B", "C", "D", "E"], "holdings_count": 5}},
             "game": {"round": 5, "pool": ["F"]}},
   "rules": [{"seat": 1, "options_include": 1, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "F"}],
   "expect": {"winner": 1,
              "standings": {"1": 63, "2": 20, "3": 20},
              "players": {"1": {"coins": 19, "holdings": ["A", "B", "C", "D", "E", "F"], "score": 63}, "2": {"score": 20}, "3": {"score": 20}},
              "game": {"pool": []}}},

  {"name": "A round begins: the round number advances to 1", "rule": "R3", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1}}},

  {"name": "After the talk, every player is still asked for a sealed bid", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1},
              "offered": [{"seat": 1, "option": 0}, {"seat": 2, "option": 0}, {"seat": 3, "option": 0}]}},

  {"name": "The bid range runs from 0 to the bidder's current coins", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"coins": 5}}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 5, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 20}, "2": {"coins": 0, "holdings": ["A"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2},
              "offered": [{"seat": 2, "option": 5}, {"seat": 1, "option": 20}],
              "not_offered": [{"seat": 2, "option": 6}, {"seat": 1, "option": 21}]}},

  {"name": "An over-coins bid cannot be made: seat 1 falls to the default bid of 0 and seat 2 wins with a bid of 1", "rule": "R6", "players": 3, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 25, "times": "all"},
             {"seat": 2, "options_include": 1, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 20}, "2": {"coins": 19, "holdings": ["A"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2},
              "not_offered": [{"seat": 1, "option": 25}]}},

  {"name": "The strictly highest bid wins the round", "rule": "R7", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "B"}],
   "expect": {"players": {"1": {"coins": 13, "holdings": ["B"]}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"winner_seat": 1, "pool": ["A", "C", "D", "E", "F"]}}},

  {"name": "Tied highest bid: the bidder with fewer objects wins", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"holdings": ["A"], "holdings_count": 1}}, "game": {"pool": ["B", "C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 4, "times": "all"},
             {"seat": 2, "options_include": 4, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": "B"}],
   "expect": {"players": {"1": {"coins": 20, "holdings": ["A"]}, "2": {"coins": 16, "holdings": ["B"]}, "3": {"coins": 20}},
              "game": {"winner_seat": 2, "pool": ["C", "D", "E", "F"]},
              "not_offered": [{"seat": 1, "option": "C"}]}},

  {"name": "Tie on both bid and object count: no sale, nobody pays, the pool is unchanged", "rule": "R9", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4, "times": "all"},
             {"seat": 2, "options_include": 4, "times": "all"},
             {"seat": 3, "options_include": 2, "times": "all"}],
   "expect": {"players": {"1": {"coins": 20, "holdings": []}, "2": {"coins": 20, "holdings": []}, "3": {"coins": 20, "holdings": []}},
              "game": {"winner_seat": 0, "round": 1, "pool": ["A", "B", "C", "D", "E", "F"]},
              "not_offered": [{"seat": 1, "option": "A"}, {"seat": 2, "option": "A"}, {"seat": 3, "option": "A"}]}},

  {"name": "The winner pays his bid: 12 coins minus a bid of 5 leaves 7", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"coins": 12}}},
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 2, "times": "all"},
             {"seat": 3, "options_include": 1, "times": "all"},
             {"seat": 1, "options_include": "A"}],
   "expect": {"players": {"1": {"coins": 7}, "2": {"coins": 20}, "3": {"coins": 20}}, "game": {"winner_seat": 1}}},

  {"name": "The named object leaves the pool and joins the winner's holdings", "rule": "R11", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "D"}],
   "expect": {"players": {"1": {"coins": 15, "holdings": ["D"]}},
              "game": {"pool": ["A", "B", "C", "E", "F"], "winner_seat": 1},
              "offered": [{"seat": 1, "option": "D"}]}},

  {"name": "Unscripted pick: the winner gets A, his highest-valued object", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10}}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"coins": 17, "holdings": ["A"]}},
              "game": {"pool": ["B", "C", "D", "E", "F"], "winner_seat": 1}}},

  {"name": "A player who already holds objects can win again", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"holdings": ["A", "B"], "holdings_count": 2}}, "game": {"pool": ["C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 5, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 1, "options_include": "C"}],
   "expect": {"players": {"1": {"coins": 15, "holdings": ["A", "B", "C"]}, "2": {"coins": 20}},
              "game": {"winner_seat": 1, "pool": ["D", "E", "F"]}}},

  {"name": "At round end the winner's seat is announced", "rule": "R14", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2, "times": "all"},
             {"seat": 2, "options_include": 2, "times": "all"},
             {"seat": 3, "options_include": 6, "times": "all"},
             {"seat": 3, "options_include": "E"}],
   "expect": {"players": {"3": {"coins": 14, "holdings": ["E"]}},
              "game": {"winner_seat": 3, "pool": ["A", "B", "C", "D", "F"]}}},

  {"name": "After round 6 the game ends and leftover pool objects are discarded", "rule": "R15", "players": 3,
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"winner": [1, 2, 3],
              "standings": {"1": 20, "2": 20, "3": 20},
              "players": {"1": {"score": 20}, "2": {"score": 20}, "3": {"score": 20}},
              "game": {"round": 6, "pool": [], "winner_seat": 0}}},

  {"name": "Final score is coins plus the player's own values of the objects he holds", "rule": "R16", "players": 3,
   "given": {"players": {"1": {"coins": 10, "holdings": ["A"], "holdings_count": 1, "value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10},
                         "2": {"coins": 20, "holdings": ["B"], "holdings_count": 1, "value_a": 14, "value_b": 2, "value_c": 4, "value_d": 6, "value_e": 8, "value_f": 10},
                         "3": {"coins": 15, "holdings": [], "holdings_count": 0, "value_a": 2, "value_b": 4, "value_c": 8, "value_d": 6, "value_e": 10, "value_f": 14}},
             "game": {"round": 5, "pool": ["C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": "C"}],
   "expect": {"winner": 1,
              "standings": {"1": 24, "2": 22, "3": 23},
              "players": {"1": {"score": 24, "coins": 10}, "2": {"score": 22, "coins": 20}, "3": {"score": 23, "coins": 15, "holdings": ["C"]}},
              "game": {"pool": []}}},

  {"name": "A shared highest score is a shared win", "rule": "R17", "players": 3,
   "given": {"players": {"1": {"coins": 20, "holdings": [], "holdings_count": 0},
                         "2": {"coins": 16, "holdings": ["A"], "holdings_count": 1, "value_a": 4, "value_b": 2, "value_c": 6, "value_d": 8, "value_e": 10, "value_f": 14},
                         "3": {"coins": 10, "holdings": [], "holdings_count": 0}},
             "game": {"round": 5, "pool": ["B", "C", "D", "E", "F"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 20, "2": 20, "3": 10},
              "players": {"1": {"score": 20}, "2": {"score": 20}, "3": {"score": 10}},
              "game": {"pool": [], "winner_seat": 0}}}
]
```
````
