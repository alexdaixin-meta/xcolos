# 23 scenarios

- time: 2026-10-27T16:58:09+00:00 (30.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 f4327bcc2182ca05, reply sha256 fb57cac053647698

## Sent

````
SPEC:
{
  "name": "Escalation Auction",
  "summary": "Six sealed all-pay auctions, each with three simultaneous raise stages. Every bidder pays what they committed, only a sole top bidder wins their private prize value, and the highest coins plus prize points wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 3
  },
  "parameters": {
    "starting_coins": 100,
    "auctions": 6,
    "raise_stages": 3,
    "min_winning_bid": 1,
    "prize_value_1": 10,
    "prize_value_2": 15,
    "prize_value_3": 20,
    "prize_value_4": 25,
    "prize_value_5": 30,
    "prize_value_6": 40,
    "prize_values_total": 140,
    "initial_prize_points": 0,
    "initial_committed": 0,
    "initial_final_score": 0,
    "min_raise": 0,
    "winning_top_count": 1
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 100,
        "meaning": "Coins the player still holds. All committed coins are paid at the end of each auction.",
        "observable": true
      },
      {
        "key": "prize_points",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of the player's own private values for the auctions they won.",
        "observable": false
      },
      {
        "key": "committed",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total the player has raised so far in the current auction. It is announced after each raise stage.",
        "observable": true
      },
      {
        "key": "final_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "coins + prize_points, computed after the 6th auction.",
        "observable": true
      },
      {
        "key": "values",
        "type": "list",
        "visible": "ally",
        "initial": "a random order of [10, 15, 20, 25, 30, 40], dealt independently to each player",
        "meaning": "Entry k is the player's private value for auction k.",
        "observable": false
      },
      {
        "key": "current_value",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's value for the current auction (entry number 'auction' of values).",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "prize_deck",
        "type": "list",
        "visible": "public",
        "initial": [
          10,
          15,
          20,
          25,
          30,
          40
        ],
        "meaning": "The six prize values that each player's values list is a permutation of.",
        "observable": false
      },
      {
        "key": "auction",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of the current auction, from 1 to 6.",
        "observable": true
      },
      {
        "key": "top_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest committed total at the resolution of the auction.",
        "observable": true
      },
      {
        "key": "top_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players whose committed equals top_bid.",
        "observable": true
      },
      {
        "key": "auction_winner",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "The seat that won the current auction, or 'none'.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player gets coins = 100, prize_points = 0, committed = 0, final_score = 0 and current_value = 0.",
    "The table gets auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none' and prize_deck = [10, 15, 20, 25, 30, 40].",
    "Each player is dealt their own values list, a random order of prize_deck (total 140). The lists are dealt independently and seeded, and each is visible only to its owner.",
    "Each player is sent their own state (sync)."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auction += 1. Every player's committed = 0. Every player's current_value = entry number 'auction' (1-based) of their values list."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is privately sent their current_value for this auction."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Auction {auction} of 6.' plus every seat's coins."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "No state change. Broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all are in."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number from 0 to (you.coins - you.committed)",
      "effect": "Raise stage 1: each player's committed += their raise."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every seat's committed after stage 1."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number from 0 to (you.coins - you.committed)",
      "effect": "Raise stage 2: each player's committed += their raise."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every seat's committed after stage 2."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number from 0 to (you.coins - you.committed)",
      "effect": "Raise stage 3: each player's committed += their raise."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every seat's committed after stage 3."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "top_bid = max over players of committed. top_count = number of players with committed == top_bid. Every player's coins -= committed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If top_count == 1 and top_bid >= 1: auction_winner = the seat with committed == top_bid, and that player's prize_points += their current_value. Otherwise auction_winner = 'none'."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Auction {auction} winner: {auction_winner}.' plus every seat's coins."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Every player's committed = 0. If auction == 6: every player's final_score = coins + prize_points."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if auction >= 6. Otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "auction >= 6",
    "rank_by": "you.final_score",
    "decided_by": "Each player's standing is final_score = coins remaining + prize_points. The highest final_score wins, and players tied at the top share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup every player has coins = 100, prize_points = 0, committed = 0, final_score = 0, and the table has auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'."
    },
    {
      "id": "R2",
      "text": "At setup each player is dealt a values list that is a random order of [10, 15, 20, 25, 30, 40] (sum 140), visible only to its owner. Lists are dealt independently, so two players may hold the same value for the same auction."
    },
    {
      "id": "R3",
      "text": "When a round starts, auction increases by 1, every player's committed becomes 0, and each player's current_value becomes entry number 'auction' of their values list."
    },
    {
      "id": "R4",
      "text": "At the start of each auction, each player is told only their own current_value, and everyone is told the auction number and every player's coins."
    },
    {
      "id": "R5",
      "text": "Each auction, every player sends one short message simultaneously, all messages are shown to everyone, and no number changes."
    },
    {
      "id": "R6",
      "text": "Each auction has exactly 3 simultaneous raise stages, and after each one every player's committed increases by the raise they chose."
    },
    {
      "id": "R7",
      "text": "In a raise stage a player's options are exactly the whole numbers 0 to (coins - committed): 0..100 with coins 100 and committed 0, 0..55 with coins 85 and committed 30, 0..10 with coins 40 and committed 30."
    },
    {
      "id": "R8",
      "text": "A player's committed can never exceed their coins within one auction."
    },
    {
      "id": "R9",
      "text": "After each of the 3 raise stages, every player's committed total is announced to all."
    },
    {
      "id": "R10",
      "text": "After the third stage, top_bid = the highest committed and top_count = the number of players whose committed equals top_bid."
    },
    {
      "id": "R11",
      "text": "After the third stage every player's coins decrease by their committed, win or lose: bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100."
    },
    {
      "id": "R12",
      "text": "When top_count = 1 and top_bid >= 1, the player with committed = top_bid becomes auction_winner and adds their current_value to prize_points."
    },
    {
      "id": "R13",
      "text": "When top_count >= 2 (a tie for the highest bid), auction_winner = 'none' and nobody's prize_points change, although all players still pay their committed."
    },
    {
      "id": "R14",
      "text": "When top_bid = 0 (everyone bid 0), auction_winner = 'none' and nobody's prize_points change."
    },
    {
      "id": "R15",
      "text": "After resolution the auction_winner and every player's coins are announced, and every player's committed is reset to 0."
    },
    {
      "id": "R16",
      "text": "After the 6th auction, each player's final_score = coins + prize_points, and the game ends."
    },
    {
      "id": "R17",
      "text": "The player with the highest final_score wins, and players tied for the highest final_score share the win as a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message each auction",
      "who": "every seat",
      "options": "one short free-text message"
    },
    {
      "question": "Raise in each of the 3 raise stages",
      "who": "every seat",
      "options": "every whole number from 0 to (own coins - own committed). A seat with coins equal to committed is offered only 0."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 3",
      "why": "The designer chose 3, and an auction needs at least two rivals for ties and bid-reading to matter. Above 5, the talk and announcements grow long and each player wins too few of the 6 auctions for budgeting to matter."
    },
    {
      "what": "Keep the simultaneous talk poll",
      "why": "The rules require it, and players genuinely disagree: everyone wants rivals to back off. Bluffs and threats about which auctions they value give players something to reason about, and since talk is not binding, believing it can be costly."
    },
    {
      "what": "prize_points visible only to its owner",
      "why": "The rules announce only the winner and coins. Publishing prize_points would reveal the winner's private value for that auction."
    },
    {
      "what": "Values entries indexed from 1",
      "why": "The rules say entry k is the value for auction k, and auction runs from 1 to 6."
    },
    {
      "what": "Strategy at the table",
      "why": "This is an all-pay auction, so overbidding is costly and ties waste both bids. A thoughtful player rations 100 coins over 6 auctions, pushes on high-value auctions, watches rivals' committed totals between stages, and avoids matching a rival's total."
    }
  ],
  "simplifications": [
    {
      "what": "The 3 raise stages are written out as explicit poll and tell steps rather than as a repeat",
      "why": "This keeps the flat step list clear without a scratch stage counter, and the behaviour is identical."
    },
    {
      "what": "final_score is computed in the last update of the 6th round",
      "why": "It is the same arithmetic as R10, placed just before the ending check."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, committed, final_score; table: auction, top_bid, top_count, auction_winner.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name": "Setup: every player starts with 100 coins and zeros, and the table starts at zero with no winner", "rule": "R1", "players": 3, "rounds": 0,
 "expect": {"players": {"1": {"coins": 100, "committed": 0, "final_score": 0}, "2": {"coins": 100, "committed": 0, "final_score": 0}, "3": {"coins": 100, "committed": 0, "final_score": 0}},
            "game": {"auction": 0, "top_bid": 0, "top_count": 0, "auction_winner": "none"}}},

{"name": "Setup: each player holds a values list of 6 entries (the order is random, so only the length is checked)", "rule": "R2", "players": 3, "rounds": 0,
 "expect": {"lens": {"players": {"1": {"values": 6}, "2": {"values": 6}, "3": {"values": 6}}, "game": {"prize_deck": 6}}}},

{"name": "A round start raises auction by 1 (from 2 to 3) and committed is 0 afterwards", "rule": "R3", "players": 3, "rounds": 1,
 "given": {"game": {"auction": 2}},
 "expect": {"game": {"auction": 3}, "players": {"1": {"committed": 0}, "2": {"committed": 0}, "3": {"committed": 0}}}},

{"name": "The first auction is numbered 1 and announcing coins changes no coins", "rule": "R4", "players": 3, "rounds": 1,
 "expect": {"game": {"auction": 1}, "players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}}},

{"name": "The talk poll changes no numbers when everyone raises 0", "rule": "R5", "players": 3, "rounds": 1,
 "expect": {"players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}, "game": {"top_bid": 0}}},

{"name": "Three raise stages of 5 each add up to a committed total of 15", "rule": "R6", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 5, "times": 3}],
 "expect": {"players": {"1": {"coins": 85}, "2": {"coins": 100}, "3": {"coins": 100}}, "game": {"top_bid": 15, "top_count": 1}}},

{"name": "With 100 coins the raise options go up to 100 and no higher", "rule": "R7", "players": 3, "rounds": 1,
 "expect": {"offered": [{"seat": 1, "option": 100}, {"seat": 1, "option": 0}], "not_offered": [{"seat": 1, "option": 101}]}},

{"name": "With 40 coins and 30 committed, a raise of 20 is not offered in later stages", "rule": "R7", "players": 3, "rounds": 1,
 "given": {"players": {"1": {"coins": 40}}},
 "rules": [{"seat": 1, "options_include": 30, "times": 1}, {"seat": 1, "options_include": 20, "times": "all"}],
 "expect": {"players": {"1": {"coins": 10}}, "game": {"top_bid": 30}, "not_offered": [{"seat": 1, "option": 41}]}},

{"name": "Committed cannot exceed coins: after going all in with 40, a later raise of 10 is not possible", "rule": "R8", "players": 3, "rounds": 1,
 "given": {"players": {"1": {"coins": 40}}},
 "rules": [{"seat": 1, "options_include": 40, "times": 1}, {"seat": 1, "options_include": 10, "times": "all"}],
 "expect": {"players": {"1": {"coins": 0}}, "game": {"top_bid": 40, "top_count": 1}, "not_offered": [{"seat": 1, "option": 41}]}},

{"name": "Raises spread over the stages are all counted in the committed totals", "rule": "R9", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 10, "times": 1}, {"seat": 2, "options_include": 7, "times": 2}],
 "expect": {"players": {"1": {"coins": 90}, "2": {"coins": 86}, "3": {"coins": 100}}, "game": {"top_bid": 14, "top_count": 1}}},

{"name": "top_bid is the highest committed total and top_count counts the seats tied on it (20, 20, 5)", "rule": "R10", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 20}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 5}],
 "expect": {"game": {"top_bid": 20, "top_count": 2}}},

{"name": "Everyone pays their bid, win or lose: 20, 15 and 0 leave 80, 85 and 100", "rule": "R11", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 20}, {"seat": 2, "options_include": 15}],
 "expect": {"players": {"1": {"coins": 80}, "2": {"coins": 85}, "3": {"coins": 100}}, "game": {"top_bid": 20, "top_count": 1}}},

{"name": "The sole top bidder in auction 6 gains their value of 40 for that auction", "rule": "R12", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"values": [10, 15, 20, 25, 30, 40], "prize_points": 0}, "2": {"prize_points": 0}, "3": {"prize_points": 0}}},
 "rules": [{"seat": 1, "options_include": 10}],
 "expect": {"winner": 1, "standings": {"1": 130, "2": 100, "3": 100},
            "players": {"1": {"coins": 90, "final_score": 130}, "2": {"final_score": 100}, "3": {"final_score": 100}},
            "game": {"top_bid": 10, "top_count": 1}}},

{"name": "A tie for the top bid gives no winner and no prize, but both tied seats still pay", "rule": "R13", "players": 3,
 "given": {"game": {"auction": 5}, "players": {"1": {"prize_points": 0}, "2": {"prize_points": 0}, "3": {"prize_points": 0}}},
 "rules": [{"seat": 1, "options_include": 10}, {"seat": 2, "options_include": 10}],
 "expect": {"winner": 3, "standings": {"1": 90, "2": 90, "3": 100},
            "players": {"1": {"coins": 90, "final_score": 90}, "2": {"coins": 90, "final_score": 90}, "3": {"coins": 100, "final_score": 100}},
            "game": {"top_bid": 10, "top_count": 2, "auction_winner": "none"}}},

{"name": "When everyone bids 0 there is no winner", "rule": "R14", "players": 3, "rounds": 1,
 "expect": {"game": {"top_bid": 0, "top_count": 3, "auction_winner": "none"}, "players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}}},

{"name": "After resolution every committed is reset to 0 and the coins reflect the payments", "rule": "R15", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 12}, {"seat": 2, "options_include": 8}],
 "expect": {"players": {"1": {"committed": 0, "coins": 88}, "2": {"committed": 0, "coins": 92}, "3": {"committed": 0, "coins": 100}}}},

{"name": "After the 6th auction final_score is coins + prize_points and the game ends", "rule": "R16", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"coins": 50, "prize_points": 25}, "2": {"coins": 60, "prize_points": 0}, "3": {"coins": 70, "prize_points": 10}}},
 "expect": {"winner": 3, "standings": {"1": 75, "2": 60, "3": 80},
            "players": {"1": {"final_score": 75}, "2": {"final_score": 60}, "3": {"final_score": 80}},
            "game": {"auction": 6}}},

{"name": "Seats tied on the highest final_score share the win", "rule": "R17", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"coins": 60, "prize_points": 20}, "2": {"coins": 80, "prize_points": 0}, "3": {"coins": 70, "prize_points": 0}}},
 "expect": {"winner": [1, 2], "standings": {"1": 80, "2": 80, "3": 70},
            "players": {"1": {"final_score": 80}, "2": {"final_score": 80}, "3": {"final_score": 70}}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name": "Setup: every player starts with 100 coins and zeros, and the table starts at zero with no winner", "rule": "R1", "players": 3, "rounds": 0,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"players": {"1": {"coins": 100, "committed": 0, "final_score": 0}, "2": {"coins": 100, "committed": 0, "final_score": 0}, "3": {"coins": 100, "committed": 0, "final_score": 0}},
            "game": {"auction": 0, "top_bid": 0, "top_count": 0, "auction_winner": "none"}}},

{"name": "Setup: each player holds a values list of 6 entries (the order is random, so only the length is checked)", "rule": "R2", "players": 3, "rounds": 0,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"lens": {"players": {"1": {"values": 6}, "2": {"values": 6}, "3": {"values": 6}}, "game": {"prize_deck": 6}}}},

{"name": "A round start raises auction by 1 (from 2 to 3) and committed is 0 afterwards", "rule": "R3", "players": 3, "rounds": 1,
 "given": {"game": {"auction": 2}},
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"game": {"auction": 3}, "players": {"1": {"committed": 0}, "2": {"committed": 0}, "3": {"committed": 0}}}},

{"name": "The first auction is numbered 1 and announcing coins changes no coins", "rule": "R4", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"game": {"auction": 1}, "players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}}},

{"name": "The talk poll changes no numbers when everyone raises 0", "rule": "R5", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}, "game": {"top_bid": 0}}},

{"name": "Three raise stages of 5 each add up to a committed total of 15", "rule": "R6", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 5, "times": 3}],
 "expect": {"players": {"1": {"coins": 85}, "2": {"coins": 100}, "3": {"coins": 100}}, "game": {"top_bid": 15, "top_count": 1}}},

{"name": "With 100 coins the raise options go up to 100 and no higher", "rule": "R7", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"offered": [{"seat": 1, "option": 100}, {"seat": 1, "option": 0}], "not_offered": [{"seat": 1, "option": 101}]}},

{"name": "With 40 coins and 30 committed, a raise of 20 is not offered in later stages", "rule": "R7", "players": 3, "rounds": 1,
 "given": {"players": {"1": {"coins": 40}}},
 "rules": [{"seat": 1, "options_include": 30, "times": 1}, {"seat": 1, "options_include": 20, "times": "all"}],
 "expect": {"players": {"1": {"coins": 10}}, "game": {"top_bid": 30}, "not_offered": [{"seat": 1, "option": 41}]}},

{"name": "Committed cannot exceed coins: after going all in with 40, a later raise of 10 is not possible", "rule": "R8", "players": 3, "rounds": 1,
 "given": {"players": {"1": {"coins": 40}}},
 "rules": [{"seat": 1, "options_include": 40, "times": 1}, {"seat": 1, "options_include": 10, "times": "all"}],
 "expect": {"players": {"1": {"coins": 0}}, "game": {"top_bid": 40, "top_count": 1}, "not_offered": [{"seat": 1, "option": 41}]}},

{"name": "Raises spread over the stages are all counted in the committed totals", "rule": "R9", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 10, "times": 1}, {"seat": 2, "options_include": 7, "times": 2}],
 "expect": {"players": {"1": {"coins": 90}, "2": {"coins": 86}, "3": {"coins": 100}}, "game": {"top_bid": 14, "top_count": 1}}},

{"name": "top_bid is the highest committed total and top_count counts the seats tied on it (20, 20, 5)", "rule": "R10", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 20}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 5}],
 "expect": {"game": {"top_bid": 20, "top_count": 2}}},

{"name": "Everyone pays their bid, win or lose: 20, 15 and 0 leave 80, 85 and 100", "rule": "R11", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 20}, {"seat": 2, "options_include": 15}],
 "expect": {"players": {"1": {"coins": 80}, "2": {"coins": 85}, "3": {"coins": 100}}, "game": {"top_bid": 20, "top_count": 1}}},

{"name": "The sole top bidder in auction 6 gains their value of 40 for that auction", "rule": "R12", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"values": [10, 15, 20, 25, 30, 40], "prize_points": 0}, "2": {"prize_points": 0}, "3": {"prize_points": 0}}},
 "rules": [{"seat": 1, "options_include": 10}],
 "expect": {"winner": 1, "standings": {"1": 130, "2": 100, "3": 100},
            "players": {"1": {"coins": 90, "final_score": 130}, "2": {"final_score": 100}, "3": {"final_score": 100}},
            "game": {"top_bid": 10, "top_count": 1}}},

{"name": "A tie for the top bid gives no winner and no prize, but both tied seats still pay", "rule": "R13", "players": 3,
 "given": {"game": {"auction": 5}, "players": {"1": {"prize_points": 0}, "2": {"prize_points": 0}, "3": {"prize_points": 0}}},
 "rules": [{"seat": 1, "options_include": 10}, {"seat": 2, "options_include": 10}],
 "expect": {"winner": 3, "standings": {"1": 90, "2": 90, "3": 100},
            "players": {"1": {"coins": 90, "final_score": 90}, "2": {"coins": 90, "final_score": 90}, "3": {"coins": 100, "final_score": 100}},
            "game": {"top_bid": 10, "top_count": 2, "auction_winner": "none"}}},

{"name": "When everyone bids 0 there is no winner", "rule": "R14", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"game": {"top_bid": 0, "top_count": 3, "auction_winner": "none"}, "players": {"1": {"coins": 100}, "2": {"coins": 100}, "3": {"coins": 100}}}},

{"name": "After resolution every committed is reset to 0 and the coins reflect the payments", "rule": "R15", "players": 3, "rounds": 1,
 "rules": [{"seat": 1, "options_include": 12}, {"seat": 2, "options_include": 8}],
 "expect": {"players": {"1": {"committed": 0, "coins": 88}, "2": {"committed": 0, "coins": 92}, "3": {"committed": 0, "coins": 100}}}},

{"name": "After the 6th auction final_score is coins + prize_points and the game ends", "rule": "R16", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"coins": 50, "prize_points": 25}, "2": {"coins": 60, "prize_points": 0}, "3": {"coins": 70, "prize_points": 10}}},
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"winner": 3, "standings": {"1": 75, "2": 60, "3": 80},
            "players": {"1": {"final_score": 75}, "2": {"final_score": 60}, "3": {"final_score": 80}},
            "game": {"auction": 6}}},

{"name": "Seats tied on the highest final_score share the win", "rule": "R17", "players": 3,
 "given": {"game": {"auction": 5},
           "players": {"1": {"coins": 60, "prize_points": 20}, "2": {"coins": 80, "prize_points": 0}, "3": {"coins": 70, "prize_points": 0}}},
 "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
 "expect": {"winner": [1, 2], "standings": {"1": 80, "2": 80, "3": 70},
            "players": {"1": {"final_score": 80}, "2": {"final_score": 80}, "3": {"final_score": 70}}}}
]
````
