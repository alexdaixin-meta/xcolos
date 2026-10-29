# 13 scenarios

- time: 2026-10-27T18:25:18+00:00 (106.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 476eac159c6adb1d, reply sha256 b675c03f2bfb724e

## Sent

````
SPEC:
{
  "name": "Budget English Auctions",
  "summary": "Over 8 rounds, players with fixed coin budgets bid for items whose value only they can see, in short ascending auctions of up to 3 simultaneous bidding steps; the winner has the highest total of value minus price.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "starting_coins": 40,
    "starting_score": 0,
    "card_min_value": 2,
    "card_value_step": 2,
    "card_max_value": 16,
    "deck_size": 8,
    "rounds": 8,
    "bidding_steps_max": 3,
    "min_raise_increment": 2,
    "initial_standing_bid": 0,
    "no_leader_code": 0,
    "priority_raise_weight": 10000,
    "priority_score_offset": 500,
    "priority_score_weight": 10,
    "rank_score_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 40,
        "meaning": "Coins left to bid with. Unspent coins carry over between rounds.",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of (value - price) over all items won. It may be negative.",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "ally",
        "initial": [
          2,
          4,
          6,
          8,
          10,
          12,
          14,
          16
        ],
        "meaning": "The player's own private deck of value cards still to come. The next card is drawn from it at random, so its order is secret.",
        "observable": false
      },
      {
        "key": "value",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private value for this round's item, which is the card drawn this round.",
        "observable": false
      },
      {
        "key": "active",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "Whether the player is still in this round's auction.",
        "observable": false
      },
      {
        "key": "raise",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's raise in the current bidding step. 0 means DROP or not asked.",
        "observable": false
      },
      {
        "key": "priority",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Scratch number used to pick the highest raise and break ties: raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n), or 0 if the player did not raise.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, from 1 to 8.",
        "observable": true
      },
      {
        "key": "start_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that tie-breaks count from this round: ((round-1) mod n)+1.",
        "observable": false
      },
      {
        "key": "standing_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current standing bid in this round's auction.",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat of the current leader. 0 means there is no leader.",
        "observable": true
      },
      {
        "key": "step",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current bidding step within the round, from 1 to 3.",
        "observable": false
      },
      {
        "key": "bidding_open",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this round's bidding is still going on.",
        "observable": false
      },
      {
        "key": "revealed_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The value of the leader who bought the item this round, announced at settlement. 0 if the item went unsold.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats are numbered 1 to n.",
    "Each player gets coins = 40 and score = 0. Both are public.",
    "Each player's private deck is set to the list [2, 4, 6, 8, 10, 12, 14, 16]. Cards are later drawn from it at random, which keeps the order secret and has the same effect as a separate shuffle.",
    "Table: round = 0, standing_bid = 0, leader = 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; start_seat = ((round-1) mod n)+1; standing_bid = 0; leader = 0; step = 0; bidding_open = true; revealed_value = 0; for every player: active = true, raise = 0, priority = 0; for every player: draw one card at random from their deck, set value to it and remove it from deck."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own value, coins and score, along with all public coins and scores."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one short free-text message",
      "effect": "All messages are collected at once and then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages are not binding and change no state."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "BIDDING STEP START (when bidding_open): step += 1; every active player who is not the leader and has coins < standing_bid + 2 gets active = false (forced drop); raise = 0 and priority = 0 for all."
    },
    {
      "action": "poll",
      "who": "every active player whose seat is not leader (when bidding_open)",
      "answer": "DROP, or a whole number from standing_bid + 2 to their coins",
      "effect": "Answers are gathered at once, and nobody sees another's answer until all are in. On DROP: active = false and raise = 0. On a number: raise = that number, and the player stays active."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "(when bidding_open) For every player with raise > 0: priority = raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n). If any raise > 0: standing_bid = max raise, and leader = the seat with the highest priority (highest raise, then lowest score, then the first seat counting upward from start_seat). Outbid raisers remain active. If no player has raise > 0: bidding_open = false. If step = 3: bidding_open = false."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce step, standing_bid, leader (or 'no leader') and the seats that dropped this step."
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "Repeat from BIDDING STEP START (the update, poll, update and tell steps) until bidding_open = false. This happens at the latest after step 3."
    },
    {
      "action": "update",
      "who": "the leader",
      "answer": null,
      "effect": "When leader > 0: the leader's coins -= standing_bid; the leader's score += (leader's value - standing_bid); revealed_value = the leader's value. When leader = 0, nothing changes and the item is unsold."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "If leader > 0: 'Seat {leader} buys for {standing_bid}; their value was {revealed_value}.' Otherwise: 'The item goes unsold.' No other value is revealed."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 8, end the game. Otherwise continue to the next round. Unspent coins carry over."
    }
  ],
  "ending": {
    "condition": "round >= 8",
    "rank_by": "you.score * 1000 + you.coins",
    "decided_by": "The highest score (total of value minus price over items won) wins. A tie on score is broken by more coins remaining. Players still tied share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has coins = 40 and score = 0, both public."
    },
    {
      "id": "R2",
      "text": "When the game starts, then each player's private deck holds exactly the cards 2, 4, 6, 8, 10, 12, 14, 16."
    },
    {
      "id": "R3",
      "text": "When a round starts, then each player draws one card from their own deck as their private value, the deck shrinks by one, and after 8 rounds every card has been used exactly once."
    },
    {
      "id": "R4",
      "text": "When a round starts, then standing_bid = 0, leader = 0 and every player is active."
    },
    {
      "id": "R5",
      "text": "When the talk step runs, then every player sends one message at the same time, and all messages are shown to everyone afterwards with no effect on state."
    },
    {
      "id": "R6",
      "text": "When a bidding step runs, then only active players who are not the leader are asked, all at the same time, to RAISE or DROP."
    },
    {
      "id": "R7",
      "text": "When a player raises, then the raise is a whole number of at least standing_bid + 2 and at most their coins (e.g. with standing_bid 6 and coins 10, only 8, 9 or 10 is allowed)."
    },
    {
      "id": "R8",
      "text": "When an active non-leader has coins < standing_bid + 2 at the start of a step, then they are forced to drop and are not asked."
    },
    {
      "id": "R9",
      "text": "When a player drops, then they are out of this round's auction (active = false) and are not asked again this round."
    },
    {
      "id": "R10",
      "text": "When the leader exists during a step, then the leader is not asked and stays in."
    },
    {
      "id": "R11",
      "text": "When at least one player raised in a step, then standing_bid becomes the highest raise and its bidder becomes the leader."
    },
    {
      "id": "R12",
      "text": "When two or more players tie for the highest raise, then the one with the lowest score becomes leader."
    },
    {
      "id": "R13",
      "text": "When tied raisers also tie on score, then the leader is the first of them counting upward from seat ((r-1) mod n)+1, wrapping around (e.g. in round 2 with 4 seats, seat 2 beats seat 1)."
    },
    {
      "id": "R14",
      "text": "When a player raised but was outbid, then they remain active for the next step."
    },
    {
      "id": "R15",
      "text": "When a step resolves, then the standing bid, the leader and the seats that dropped are announced."
    },
    {
      "id": "R16",
      "text": "When nobody raises in a step, then bidding ends immediately."
    },
    {
      "id": "R17",
      "text": "When step 3 has resolved, then bidding ends."
    },
    {
      "id": "R18",
      "text": "When bidding ends with a leader, then the leader pays standing_bid from coins and their score changes by (value - standing_bid), e.g. value 6 bought at 10 gives score -4."
    },
    {
      "id": "R19",
      "text": "When bidding ends with a leader, then the leader's value is announced and no other player's value is revealed."
    },
    {
      "id": "R20",
      "text": "When nobody raised during the round, then the item is unsold and no coins or scores change."
    },
    {
      "id": "R21",
      "text": "When a round ends, then unspent coins carry over to the next round."
    },
    {
      "id": "R22",
      "text": "When round 8 has settled, then the game ends."
    },
    {
      "id": "R23",
      "text": "When the game ends, then the highest score wins, ties go to more remaining coins, and players still tied share the win as a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every seat",
      "options": "one short free-text message"
    },
    {
      "question": "Bidding step: RAISE or DROP",
      "who": "every active seat that is not the leader and has coins >= standing_bid + 2",
      "options": "DROP, or a whole number from standing_bid + 2 to that seat's coins"
    },
    {
      "question": "Bidding step",
      "who": "the leader",
      "options": "not asked; stays in"
    },
    {
      "question": "Bidding step",
      "who": "an active non-leader seat with coins < standing_bid + 2",
      "options": "not asked; forced DROP"
    },
    {
      "question": "Bidding step",
      "who": "a seat that dropped earlier this round",
      "options": "not asked"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer's suggested size of 4 is kept. The minimum is 3 because an auction needs at least two rivals for a bidder, so that the tie-breaks and the budget pressure matter. The maximum stays at 5 because with more seats one player's bids rarely decide an item and the talk becomes long."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The source requires simultaneous messages. Talk earns its place because players disagree about who should win each item and can bluff about their values or signal restraint, and none of it is binding."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player bids below their value, saves coins for high-value rounds since the deck's remaining cards are known to them, reads rivals' coins and messages, and uses the 3-step limit to jump-bid. A thoughtless player overpays early or drops good items."
    },
    {
      "what": "Tie-break encoded as a priority number",
      "why": "The priority raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n) orders by highest raise, then lowest score, then seat order from start_seat. Scores stay within about -40 to 128, so the terms never overlap."
    },
    {
      "what": "Ranking expression score*1000 + coins",
      "why": "Coins never exceed 40, so coins act only as a tie-break after score, as the source states."
    },
    {
      "what": "Forced drop applied at the start of each step",
      "why": "The source says such a player must drop. Applying it before the poll means they are never offered a choice they cannot make."
    },
    {
      "what": "Card values given as card_min_value 2, card_value_step 2 and card_max_value 16",
      "why": "Parameters must be single numbers. The deck 2, 4, ..., 16 is every value from the minimum to the maximum in steps of 2, which is 8 cards (deck_size)."
    }
  ],
  "simplifications": [
    {
      "what": "The secretly shuffled deck is modelled as random draws without replacement from the player's deck list",
      "why": "This is equivalent to drawing in order from a separately shuffled deck, and the order stays secret even from its owner."
    },
    {
      "what": "The 3 bidding steps are a repeated block of four steps that stops when bidding_open becomes false",
      "why": "The engine runs steps in a flat list with repeat. A step where nobody raises, or step 3, closes the bidding."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, score; table: round, standing_bid, leader, revealed_value.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the bidding scenarios so the expected result follows from the moves actually played.
1. Script a move for every active non-leader seat in every bidding step, up to 3 steps. If a seat should leave, script an explicit DROP for it rather than relying on the default.
2. Remember that bidding continues after a step in which anyone raised. A leader who is outbid becomes an active non-leader again and is asked in the next step.
3. Do not use `given` to set mid-auction values such as standing_bid 6 or leader. Each round's start resets standing_bid to 0 and leader to 0, so build that state with scripted raises in earlier steps instead.
4. Work out expected coins, score, standing_bid and leader only from the final leader after the last step. That leader pays the standing bid and scores value minus bid.
5. Predict the leader's value only when the deck order is fixed, since it otherwise depends on the shuffle.
6. Do not assert on internal fields such as step, priority or bid_said.
````

## Reply

````
```json
[
  {"name": "Start: every seat has 40 coins and score 0, round 0", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}, "4": {"coins": 40, "score": 0}},
              "game": {"round": 0}}},

  {"name": "Start: each private deck holds 8 cards", "rule": "R2", "players": 3, "rounds": 0,
   "expect": {"lens": {"players": {"1": {"deck": 8}, "2": {"deck": 8}, "3": {"deck": 8}}}}},

  {"name": "One round with everyone dropping: each deck shrinks by one", "rule": "R3", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"lens": {"players": {"1": {"deck": 7}, "2": {"deck": 7}, "3": {"deck": 7}}},
              "players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}}}},

  {"name": "Full match where everyone always drops: all 8 cards used, all tie and share the win", "rule": "R3", "players": 3,
   "rules": [{"seat": 1, "options_include": "DROP", "times": "all"}, {"seat": 2, "options_include": "DROP", "times": "all"}, {"seat": 3, "options_include": "DROP", "times": "all"}],
   "expect": {"winner": [1, 2, 3], "standings": {"1": 40, "2": 40, "3": 40},
              "lens": {"players": {"1": {"deck": 0}, "2": {"deck": 0}, "3": {"deck": 0}}},
              "game": {"round": 8}}},

  {"name": "Round 2 starts fresh: no leader, standing bid 0, the seats that dropped in round 1 are asked again", "rule": "R4", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"deck": [6, 6]}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": "DROP", "times": 2}, {"seat": 3, "options_include": "DROP", "times": 2}],
   "expect": {"players": {"1": {"coins": 36, "score": 2}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"round": 2, "standing_bid": 0, "leader": 0, "revealed_value": 0}}},

  {"name": "Talk changes no state", "rule": "R5", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"round": 1, "standing_bid": 0, "leader": 0}}},

  {"name": "Only active non-leaders are asked: seat 2 leads at 6 and seat 1 is asked and drops", "rule": "R6", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 6},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 34}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 6, "leader": 2},
              "offered": [{"seat": 1, "option": "DROP"}, {"seat": 3, "option": "DROP"}, {"seat": 2, "option": 6}]}},

  {"name": "Raise range: standing bid 6 and coins 10 allow 8 to 10 only", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"players": {"3": {"coins": 10, "deck": [12]}}},
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": 4}, {"seat": 3, "options_include": 9}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 40, "score": 0}, "3": {"coins": 1, "score": 3}},
              "game": {"standing_bid": 9, "leader": 3, "revealed_value": 12},
              "offered": [{"seat": 3, "option": 8}, {"seat": 3, "option": 10}],
              "not_offered": [{"seat": 3, "option": 11}]}},

  {"name": "A seat with 1 coin is forced to drop and never asked", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"3": {"coins": 1}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 2, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 36}, "2": {"coins": 40, "score": 0}, "3": {"coins": 1, "score": 0}},
              "game": {"standing_bid": 4, "leader": 1},
              "not_offered": [{"seat": 3, "option": "DROP"}, {"seat": 3, "option": 2}]}},

  {"name": "A seat that drops in step 1 stays out while the others bid on", "rule": "R9", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": 6},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 34}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 6, "leader": 2}}},

  {"name": "Leader at 10 is not asked and keeps the item when the others drop", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"deck": [16]}}},
   "rules": [{"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": 4}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": 2}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 30, "score": 6}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 10, "leader": 1, "revealed_value": 16}}},

  {"name": "Highest raise 8 sets the standing bid and its bidder leads", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"deck": [8]}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 8},
             {"seat": 3, "options_include": 3}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 32, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 8, "leader": 2, "revealed_value": 8}}},

  {"name": "Tie at 6: the lower score (seat 2 at -5) leads", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"score": -5, "deck": [10]}, "3": {"score": 4}}},
   "rules": [{"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 6},
             {"seat": 3, "options_include": 6}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 34, "score": -1}, "3": {"coins": 40, "score": 4}},
              "game": {"standing_bid": 6, "leader": 2, "revealed_value": 10}}},

  {"name": "Round 2 with 4 seats: tied raises and scores, seat 2 beats seat 1", "rule": "R13", "players": 4, "rounds": 1,
   "given": {"game": {"round": 1}},
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 6},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 34}, "3": {"coins": 40}, "4": {"coins": 40}},
              "game": {"round": 2, "standing_bid": 6, "leader": 2}}},

  {"name": "Round 3 with 4 seats: counting from seat 3 wraps, so seat 1 beats seat 2", "rule": "R13", "players": 4, "rounds": 1,
   "given": {"game": {"round": 2}},
   "rules": [{"seat": 1, "options_include": 6},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 34}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40}, "4": {"coins": 40}},
              "game": {"round": 3, "standing_bid": 6, "leader": 1}}},

  {"name": "Outbid seat 1 stays active, raises to 10 in step 2 and wins", "rule": "R14", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 30}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 10, "leader": 1}}},

  {"name": "After the steps resolve, standing bid and leader are public", "rule": "R15", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": 12}],
   "expect": {"players": {"1": {"coins": 40}, "2": {"coins": 40}, "3": {"coins": 28}},
              "game": {"standing_bid": 12, "leader": 3}}},

  {"name": "Nobody raises in step 2: bidding ends and leader seat 1 pays 4", "rule": "R16", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 4},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 36}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 4, "leader": 1}}},

  {"name": "Bidding ends after step 3: seat 2 leads at 8 and pays", "rule": "R17", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": 6},
             {"seat": 2, "options_include": 4}, {"seat": 2, "options_include": 8},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 32}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 8, "leader": 2}}},

  {"name": "Value 6 bought at 10: coins 30, score -4", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"deck": [6]}}},
   "rules": [{"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 30, "score": -4}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 10, "leader": 1, "revealed_value": 6}}},

  {"name": "The buyer's value 14 is revealed", "rule": "R19", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"deck": [14]}}},
   "rules": [{"seat": 1, "options_include": "DROP"},
             {"seat": 2, "options_include": 4},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"2": {"coins": 36, "score": 10}},
              "game": {"leader": 2, "standing_bid": 4, "revealed_value": 14}}},

  {"name": "Everyone drops at once: item unsold, nothing changes", "rule": "R20", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 40, "score": 0}, "3": {"coins": 40, "score": 0}},
              "game": {"standing_bid": 0, "leader": 0, "revealed_value": 0}}},

  {"name": "Coins carry over: buy at 10 in round 1, then spend the remaining 30 in round 2", "rule": "R21", "players": 3, "rounds": 2,
   "given": {"players": {"2": {"deck": [8, 12]}}},
   "rules": [{"seat": 2, "options_include": 10}, {"seat": 2, "options_include": 30},
             {"seat": 1, "options_include": "DROP", "times": 2}, {"seat": 3, "options_include": "DROP", "times": 2}],
   "expect": {"players": {"1": {"coins": 40, "score": 0}, "2": {"coins": 0, "score": -20}, "3": {"coins": 40, "score": 0}},
              "game": {"round": 2, "standing_bid": 30, "leader": 2}}},

  {"name": "Game ends after round 8 settles; highest score wins", "rule": "R22", "players": 3,
   "given": {"game": {"round": 7}, "players": {"1": {"score": 5}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 1, "standings": {"1": 5040, "2": 40, "3": 40},
              "game": {"round": 8}}},

  {"name": "Tie on score is broken by more coins", "rule": "R23", "players": 3,
   "given": {"game": {"round": 7}, "players": {"1": {"score": 10, "coins": 20}, "2": {"score": 10, "coins": 25}, "3": {"score": 3, "coins": 40}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 2, "standings": {"1": 10020, "2": 10025, "3": 3040}}},

  {"name": "Same score and same coins share the win", "rule": "R23", "players": 3,
   "given": {"game": {"round": 7}, "players": {"1": {"score": 10, "coins": 25}, "2": {"score": 10, "coins": 25}, "3": {"score": 3, "coins": 40}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": [1, 2], "standings": {"1": 10025, "2": 10025, "3": 3040}}}
]
```
````
