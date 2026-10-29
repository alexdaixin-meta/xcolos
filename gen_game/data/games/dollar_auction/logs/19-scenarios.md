# 19 scenarios

- time: 2026-10-27T18:33:05+00:00 (41.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 57903b877bc86cf5, reply sha256 ed58bced8359d6e7

## Sent

````
SPEC:
{
  "name": "Escalation Ledger III",
  "summary": "Three players with secret high-value schedules bid over 12 rounds for a prize; tied top bids go to a raise-or-drop escalation, and the highest total wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "num_rounds": 12,
    "high_value": 12,
    "low_value": 6,
    "bid_option_1": 0,
    "bid_option_2": 2,
    "bid_option_3": 4,
    "bid_option_4": 6,
    "bid_option_5": 8,
    "raise_cost": 3,
    "loser_pay_fraction": 0.5,
    "schedule_types": 4,
    "schedule_cycle": 4,
    "starting_total": 0
  },
  "attributes": {
    "player": [
      {
        "key": "schedule_type",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This player's secret schedule type: North, East, South or West.",
        "observable": false
      },
      {
        "key": "schedule_slot",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Value of round % 4 in this player's high-value rounds: North 1, East 2, South 3, West 0.",
        "observable": false
      },
      {
        "key": "prize_value",
        "type": "number",
        "visible": "ally",
        "initial": 6,
        "meaning": "This player's value of this round's prize: 12 if round % 4 == schedule_slot, else 6.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This round's bid: 0, 2, 4, 6 or 8. It is chosen secretly and revealed after all bids are in.",
        "observable": true
      },
      {
        "key": "in_tie",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if this player tied for the highest bid above 0 this round.",
        "observable": false
      },
      {
        "key": "escalation",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's escalation choice, RAISE or DROP, or empty if the player was not in a tie.",
        "observable": true
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total. It may go below 0.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round, 1 to 12.",
        "observable": true
      },
      {
        "key": "schedule_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "North",
          "East",
          "South",
          "West"
        ],
        "meaning": "The four schedule types, dealt from at setup.",
        "observable": false
      },
      {
        "key": "unused_type",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "The schedule type dealt to nobody. Nobody is told which it is.",
        "observable": false
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
        "key": "top_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players whose bid equals high_bid.",
        "observable": false
      },
      {
        "key": "raise_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of tied players who chose RAISE this round.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Set every player's total to 0 and the round to 0.",
    "For each player, draw one type at random from schedule_deck into that player's schedule_type and remove it from schedule_deck.",
    "Set each player's schedule_slot from their type: North 1, East 2, South 3, West 0.",
    "Move the one type left in schedule_deck into unused_type, which stays hidden from everyone.",
    "Tell each player privately only their own schedule type and its high-value rounds (North 1, 5, 9; East 2, 6, 10; South 3, 7, 11; West 4, 8, 12)."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Add 1 to round. Set each player's prize_value = 12 if round % 4 == schedule_slot, else 6. Reset bid to 0, in_tie to false, escalation to empty and raise_count to 0. Announce 'Round {round} of 12.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Every player writes one message at the same time. All messages are then broadcast to everyone as 'Seat {seat} says: {value}'. Nothing is binding, and players may lie."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of 0, 2, 4, 6, 8",
      "effect": "Store each player's answer in bid. No bid is seen until all are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set high_bid = max of all bids and top_count = number of players with bid == high_bid. Announce every player's bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When high_bid > 0 and top_count == 1: the player with bid == high_bid adds prize_value - bid to total, and every other player subtracts bid / 2 from total. When high_bid == 0: nothing changes."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When high_bid > 0 and top_count >= 2: set in_tie = (bid == high_bid) for each player, and every player with in_tie false subtracts bid / 2 from total."
    },
    {
      "action": "poll",
      "who": "each player with in_tie true (only when high_bid > 0 and top_count >= 2)",
      "answer": "RAISE or DROP",
      "effect": "Store each tied player's answer in escalation. Choices are simultaneous and secret until all are in."
    },
    {
      "action": "update",
      "who": "tied players",
      "answer": null,
      "effect": "When high_bid > 0 and top_count >= 2: set raise_count = number of players with escalation == RAISE. Every raiser subtracts 3 from total. If raise_count == 1, the raiser adds prize_value - bid to total and every other tied player subtracts bid / 2. Otherwise every tied player subtracts bid / 2."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every bid, every escalation choice and every total."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 12, end the game; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their total after round 12. The highest total wins, and players level at the top share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, three of the four types North, East, South and West are dealt at random, one to each player. Each player sees only their own type, and the fourth type is dealt to nobody and revealed to nobody."
    },
    {
      "id": "R2",
      "text": "When it is round r, then a player's prize value is 12 if r is one of their high-value rounds (North 1, 5, 9; East 2, 6, 10; South 3, 7, 11; West 4, 8, 12), and 6 otherwise."
    },
    {
      "id": "R3",
      "text": "Every total starts at 0, and a total may go below 0."
    },
    {
      "id": "R4",
      "text": "Each round, every player sends one short message at the same time, and all messages are then shown to everyone."
    },
    {
      "id": "R5",
      "text": "Each round, every player secretly and simultaneously bids 0, 2, 4, 6 or 8, and all bids are then revealed."
    },
    {
      "id": "R6",
      "text": "When all bids are 0, then no total changes in that round."
    },
    {
      "id": "R7",
      "text": "When one bid is strictly highest, then that player's total changes by prize value minus bid (for example, a bid of 8 in a high-value round gives +4), and each other player loses half their own bid (a bid of 4 costs 2)."
    },
    {
      "id": "R8",
      "text": "When two or three players tie for the highest bid above 0, then players not in the tie lose half their own bid, and only the tied players choose RAISE or DROP, simultaneously."
    },
    {
      "id": "R9",
      "text": "When a tied player chooses RAISE, then that player loses 3."
    },
    {
      "id": "R10",
      "text": "When exactly one tied player raises, then that player's total changes by prize value minus bid minus 3 (for example, a tie at 6 with prize value 12 gives +3), and each other tied player loses half the bid."
    },
    {
      "id": "R11",
      "text": "When zero, two or three tied players raise, then nobody receives the prize, every tied player loses half the bid, and each raiser also loses 3."
    },
    {
      "id": "R12",
      "text": "After each round, every bid, every escalation choice and every total is announced."
    },
    {
      "id": "R13",
      "text": "When round 12 has been resolved, then the game ends, and the player or players with the highest total win."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all seats",
      "options": "any short text, from every seat in every round"
    },
    {
      "question": "Bid",
      "who": "all seats",
      "options": "0, 2, 4, 6, 8 for every seat in every round"
    },
    {
      "question": "Escalation",
      "who": "only seats whose bid equals the highest bid, when that bid is above 0 and two or three seats share it",
      "options": "a tied seat: RAISE, DROP; any other seat is not asked"
    }
  ],
  "choices": [
    {
      "what": "3 players (min, max and suggested 3)",
      "why": "The designer fixed the table at 3. Three seats are dealt from four types, so one type stays hidden, which the deduction depends on. A fourth seat would leave no unused type, and fewer seats would remove the multi-way ties."
    },
    {
      "what": "Talk kept, as a simultaneous poll broadcast to all",
      "why": "The rules require simultaneous talk. Players disagree over who should win each prize, and claims about one's own schedule can be bluffs, so the talk gives players something to reason about."
    },
    {
      "what": "Type stored as schedule_slot = round % 4 value (North 1, East 2, South 3, West 0)",
      "why": "This makes the 12-or-6 prize value a single arithmetic test."
    },
    {
      "what": "In a no-winner escalation, the tied players pay half the bid as well as the 3 for raising",
      "why": "This follows the rules exactly: every tied player pays half, and raisers have also paid 3."
    }
  ],
  "simplifications": [
    {
      "what": "The escalation poll and its resolution are steps that always appear in the round, with a when-condition, instead of a separate block",
      "why": "The engine's step list is flat. A conditional step reproduces step 6 exactly."
    },
    {
      "what": "The winner's payment and prize are applied as one net change (prize_value - bid)",
      "why": "The arithmetic result is identical."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bid, escalation, total; table: round.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup: totals start at 0, round 0, schedule deck emptied into seats and unused type",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "players": {"1": {"total": 0}, "2": {"total": 0}, "3": {"total": 0}},
      "game": {"round": 0},
      "lens": {"game": {"schedule_deck": 0}}
    }
  },
  {
    "name": "Prize value is 12 in own high-value round: North sole bid 8 in round 1 gives +4",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 4, "bid": 8},
        "2": {"total": 0},
        "3": {"total": 0}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Prize value is 6 outside own high-value round: East sole bid 8 in round 1 goes negative to -2",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 8},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 0},
        "2": {"total": -2},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "A round with talk and all zero bids advances the round without changing totals",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 3},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 3},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 3}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 3},
        "2": {"total": 3},
        "3": {"total": 3}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Bids 2, 4 and 6 are revealed; sole top bid with no tie means no escalation",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 6}
    ],
    "expect": {
      "players": {
        "1": {"bid": 2, "total": -1},
        "2": {"bid": 4, "total": -2},
        "3": {"bid": 6, "total": 0}
      },
      "not_offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"},
        {"seat": 3, "option": "RAISE"}
      ]
    }
  },
  {
    "name": "All bids 0: no total changes",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 5},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": -2},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 7}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 5},
        "2": {"total": -2},
        "3": {"total": 7}
      },
      "not_offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"},
        {"seat": 3, "option": "RAISE"}
      ]
    }
  },
  {
    "name": "Strict highest bid 8 at prize 12 gives +4; a bid of 4 costs 2; a bid of 0 costs nothing",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 4},
        "2": {"total": -2},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "Tie at 6: non-tied seat bidding 4 loses 2 and is not asked; tied seats both DROP and lose 3",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 4},
      {"seat": 1, "options_include": "DROP"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": -3, "escalation": "DROP"},
        "2": {"total": -3, "escalation": "DROP"},
        "3": {"total": -2}
      },
      "offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"}
      ],
      "not_offered": [
        {"seat": 3, "option": "RAISE"},
        {"seat": 3, "option": "DROP"}
      ]
    }
  },
  {
    "name": "Three-way tie at 4, all RAISE: each pays 3 for raising plus half the bid, total -5",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 4},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "RAISE"},
      {"seat": 3, "options_include": "RAISE"}
    ],
    "expect": {
      "players": {
        "1": {"total": -5, "escalation": "RAISE"},
        "2": {"total": -5, "escalation": "RAISE"},
        "3": {"total": -5, "escalation": "RAISE"}
      }
    }
  },
  {
    "name": "Tie at 6, lone raiser at prize 12 gets +3, dropper loses 3, outside bid 2 loses 1",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 2},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": 3},
        "2": {"total": -3},
        "3": {"total": -1}
      }
    }
  },
  {
    "name": "Tie at 8 with zero raisers: nobody gets the prize, each tied seat loses 4",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 8},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "DROP"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": -4},
        "2": {"total": -4},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "Tie at 6 with two raisers: each raiser loses 3 plus half the bid, total -6",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "RAISE"}
    ],
    "expect": {
      "players": {
        "1": {"total": -6},
        "2": {"total": -6},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "After the round, bids, escalation choices and totals are visible",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"bid": 4, "escalation": "RAISE", "total": 5},
        "2": {"bid": 4, "escalation": "DROP", "total": -2},
        "3": {"bid": 0, "escalation": "", "total": 0}
      }
    }
  },
  {
    "name": "Game ends after round 12; highest total wins",
    "rule": "R13",
    "players": 3,
    "given": {
      "players": {
        "1": {"schedule_type": "West", "schedule_slot": 0, "total": 10},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 12},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 5}
      },
      "game": {"round": 11}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 14, "2": 12, "3": 5},
      "players": {
        "1": {"total": 14},
        "2": {"total": 12},
        "3": {"total": 5}
      },
      "game": {"round": 12}
    }
  },
  {
    "name": "Game ends after round 12; seats level at the top share the win",
    "rule": "R13",
    "players": 3,
    "given": {
      "players": {
        "1": {"schedule_type": "West", "schedule_slot": 0, "total": 10},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 10},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 3}
      },
      "game": {"round": 11}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 10, "2": 10, "3": 3}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Setup: totals start at 0, round 0, schedule deck emptied into seats and unused type",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "rules": [],
    "expect": {
      "players": {"1": {"total": 0}, "2": {"total": 0}, "3": {"total": 0}},
      "game": {"round": 0},
      "lens": {"game": {"schedule_deck": 0}}
    }
  },
  {
    "name": "Prize value is 12 in own high-value round: North sole bid 8 in round 1 gives +4",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 4, "bid": 8},
        "2": {"total": 0},
        "3": {"total": 0}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Prize value is 6 outside own high-value round: East sole bid 8 in round 1 goes negative to -2",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 8},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 0},
        "2": {"total": -2},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "A round with talk and all zero bids advances the round without changing totals",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 3},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 3},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 3}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 3},
        "2": {"total": 3},
        "3": {"total": 3}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Bids 2, 4 and 6 are revealed; sole top bid with no tie means no escalation",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 6}
    ],
    "expect": {
      "players": {
        "1": {"bid": 2, "total": -1},
        "2": {"bid": 4, "total": -2},
        "3": {"bid": 6, "total": 0}
      },
      "not_offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"},
        {"seat": 3, "option": "RAISE"}
      ]
    }
  },
  {
    "name": "All bids 0: no total changes",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 5},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": -2},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 7}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 5},
        "2": {"total": -2},
        "3": {"total": 7}
      },
      "not_offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"},
        {"seat": 3, "option": "RAISE"}
      ]
    }
  },
  {
    "name": "Strict highest bid 8 at prize 12 gives +4; a bid of 4 costs 2; a bid of 0 costs nothing",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"total": 4},
        "2": {"total": -2},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "Tie at 6: non-tied seat bidding 4 loses 2 and is not asked; tied seats both DROP and lose 3",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 4},
      {"seat": 1, "options_include": "DROP"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": -3, "escalation": "DROP"},
        "2": {"total": -3, "escalation": "DROP"},
        "3": {"total": -2}
      },
      "offered": [
        {"seat": 1, "option": "RAISE"},
        {"seat": 2, "option": "RAISE"}
      ],
      "not_offered": [
        {"seat": 3, "option": "RAISE"},
        {"seat": 3, "option": "DROP"}
      ]
    }
  },
  {
    "name": "Three-way tie at 4, all RAISE: each pays 3 for raising plus half the bid, total -5",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 4},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "RAISE"},
      {"seat": 3, "options_include": "RAISE"}
    ],
    "expect": {
      "players": {
        "1": {"total": -5, "escalation": "RAISE"},
        "2": {"total": -5, "escalation": "RAISE"},
        "3": {"total": -5, "escalation": "RAISE"}
      }
    }
  },
  {
    "name": "Tie at 6, lone raiser at prize 12 gets +3, dropper loses 3, outside bid 2 loses 1",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 2},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": 3},
        "2": {"total": -3},
        "3": {"total": -1}
      }
    }
  },
  {
    "name": "Tie at 8 with zero raisers: nobody gets the prize, each tied seat loses 4",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 8},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "DROP"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"total": -4},
        "2": {"total": -4},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "Tie at 6 with two raisers: each raiser loses 3 plus half the bid, total -6",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "RAISE"}
    ],
    "expect": {
      "players": {
        "1": {"total": -6},
        "2": {"total": -6},
        "3": {"total": 0}
      }
    }
  },
  {
    "name": "After the round, bids, escalation choices and totals are visible",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"schedule_type": "North", "schedule_slot": 1, "total": 0},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 0},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 0}
      },
      "game": {"round": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0},
      {"seat": 1, "options_include": "RAISE"},
      {"seat": 2, "options_include": "DROP"}
    ],
    "expect": {
      "players": {
        "1": {"bid": 4, "escalation": "RAISE", "total": 5},
        "2": {"bid": 4, "escalation": "DROP", "total": -2},
        "3": {"bid": 0, "escalation": "", "total": 0}
      }
    }
  },
  {
    "name": "Game ends after round 12; highest total wins",
    "rule": "R13",
    "players": 3,
    "given": {
      "players": {
        "1": {"schedule_type": "West", "schedule_slot": 0, "total": 10},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 12},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 5}
      },
      "game": {"round": 11}
    },
    "rules": [
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 14, "2": 12, "3": 5},
      "players": {
        "1": {"total": 14},
        "2": {"total": 12},
        "3": {"total": 5}
      },
      "game": {"round": 12}
    }
  },
  {
    "name": "Game ends after round 12; seats level at the top share the win",
    "rule": "R13",
    "players": 3,
    "given": {
      "players": {
        "1": {"schedule_type": "West", "schedule_slot": 0, "total": 10},
        "2": {"schedule_type": "East", "schedule_slot": 2, "total": 10},
        "3": {"schedule_type": "South", "schedule_slot": 3, "total": 3}
      },
      "game": {"round": 11}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 10, "2": 10, "3": 3}
    }
  }
]
```
````
