# 14 scenarios

- time: 2026-11-21T01:33:43+00:00 (175.6s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 a05eacce950ff237, reply sha256 0fd9e7919c411ecb

## Sent

````
SPEC:
{
  "name": "For Sale: Sealed Bids - Four Player",
  "summary": "Bid secretly for properties then sell them secretly for cheques; richest total wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "starting_coins": 18,
    "property_low": 1,
    "property_high": 30,
    "property_deck_size": 30,
    "property_deck_used": 28,
    "cheque_low": 0,
    "cheque_high": 15,
    "cheque_copies": 2,
    "cheque_deck_size": 30,
    "cheque_deck_used": 28,
    "total_rounds": 14,
    "buying_rounds": 7,
    "selling_rounds": 7,
    "cards_per_round": 4
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "ally",
        "initial": 18,
        "meaning": "remaining private coins for bidding",
        "observable": false
      },
      {
        "key": "cheque_total",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sum of cheques won kept private until end",
        "observable": false
      },
      {
        "key": "properties",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "property cards held in hand public",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sealed bid submitted this buying round",
        "observable": false
      },
      {
        "key": "selected_property",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "property chosen to sell this selling round",
        "observable": false
      },
      {
        "key": "final_money",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "cheque_total plus remaining coins revealed at end",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "property_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30
        ],
        "meaning": "unseen property cards 1 to 30",
        "observable": false
      },
      {
        "key": "cheque_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          0,
          0,
          2,
          2,
          3,
          3,
          4,
          4,
          5,
          5,
          6,
          6,
          7,
          7,
          8,
          8,
          9,
          9,
          10,
          10,
          11,
          11,
          12,
          12,
          13,
          13,
          14,
          14,
          15,
          15
        ],
        "meaning": "unseen cheques 0 and 2 to 15 two each",
        "observable": false
      },
      {
        "key": "current_offer",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "4 properties or cheques revealed this round sorted high to low",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current round 1 to 14",
        "observable": false
      },
      {
        "key": "priority_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "first seat in tie break order this round",
        "observable": false
      },
      {
        "key": "property_discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "played properties discarded",
        "observable": false
      }
    ]
  },
  "setup": [
    "Give each of seats 1 to 4 exactly 18 coins, 0 cheque_total, 0 final_money and empty properties hand.",
    "Build property_deck as cards 1 to 30 one each and cheque_deck as 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two each for 30 cheques.",
    "Set round_number to 1 and current_offer to empty and property_discard to empty.",
    "Only the top 28 properties and top 28 cheques will ever be used and the bottom 2 of each deck stay unseen.",
    "There is no talk phase and all choices are sealed."
  ],
  "round": [
    {
      "action": "initialize",
      "who": "all players",
      "answer": null,
      "effect": "set coins to 18 cheque_total to 0 properties to [] bid to 0 selected_property to 0 final_money to 0 property_deck to 1 to 30 cheque_deck to 0,0,2,2 to 15,15 round_number to 1 current_offer to []"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "send each player their coins cheque_total and properties"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_number <= 7",
      "effect": "when round_number is 1 remove 2 unseen cards from property_deck then move next 4 cards from property_deck to current_offer sorted HIGH SECOND THIRD LOW and set priority_seat to ((round_number-1) mod 4)+1"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "number",
        "min": 0,
        "max": "coins"
      },
      "when": "round_number <= 7",
      "effect": "set you.bid to sealed bid 0 up to you.coins"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_number <= 7",
      "effect": "rank bids high to low breaking ties by priority_seat order wrapping 4 to 1 then first-ranked takes HIGH and pays full bid from coins second takes SECOND and pays (bid+1)//2 third takes THIRD and pays (bid+1)//2 fourth takes LOW and pays (bid+1)//2 and append taken property to you.properties"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "round_number <= 7",
      "effect": "broadcast which player took HIGH SECOND THIRD LOW without revealing bid amounts or coin totals"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_number >= 8",
      "effect": "when round_number is 8 remove 2 unseen cheques from cheque_deck then move next 4 cheques from cheque_deck to current_offer sorted highest to lowest"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "choice",
        "from": "you.properties"
      },
      "when": "round_number >= 8",
      "effect": "set you.selected_property to one property from you.properties"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_number >= 8",
      "effect": "rank selected_property high to low with no ties then highest adds highest cheque in current_offer to cheque_total second-highest adds second-highest third adds third lowest adds lowest and remove selected_property from you.properties to property_discard"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "round_number >= 8",
      "effect": "broadcast who played which property and who took which cheque without revealing running cheque totals"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "set round_number to round_number+1 and if round_number>14 set you.final_money to you.cheque_total+you.coins"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game when round_number>14 else continue"
    }
  ],
  "ending": {
    "condition": "round_number > 14",
    "rank_by": "you.final_money * 1000 + you.coins",
    "decided_by": "Standing is final_money equal to cheque_total plus remaining coins with remaining coins as tie-break; highest value wins and players level at the top share the win"
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each of 4 players holds 18 coins, 0 cheque_total and empty properties hand."
    },
    {
      "id": "R2",
      "text": "When built, then property_deck holds cards 1 to 30 one each for 30 cards."
    },
    {
      "id": "R3",
      "text": "When built, then cheque_deck holds values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two of each for 30 cheques."
    },
    {
      "id": "R4",
      "text": "When the game runs, then rounds 1 to 7 are buying and rounds 8 to 14 are selling for 14 rounds total."
    },
    {
      "id": "R5",
      "text": "When decks are prepared, then only the top 28 properties and top 28 cheques are ever used and the bottom 2 stay unseen."
    },
    {
      "id": "R6",
      "text": "When a buying round starts, then reveal the next 4 property cards sorted HIGH SECOND THIRD LOW by value."
    },
    {
      "id": "R7",
      "text": "When bidding, then all players at the same moment secretly submit a whole-number bid from 0 up to current coins."
    },
    {
      "id": "R8",
      "text": "When bids are ranked, then rank highest to lowest and break ties by priority order starting at seat ((r-1) mod 4)+1 then next wrapping 4 to 1 in round r."
    },
    {
      "id": "R9",
      "text": "When buying resolves, then first-ranked takes HIGH and pays full bid and second-ranked takes SECOND and pays half rounded up and third takes THIRD and pays half rounded up and fourth takes LOW and pays half rounded up where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2."
    },
    {
      "id": "R10",
      "text": "When payments are made, then they go to the bank from private coins."
    },
    {
      "id": "R11",
      "text": "When a buying round ends, then announce publicly which player took HIGH SECOND THIRD LOW and do not announce bid amounts or coin totals."
    },
    {
      "id": "R12",
      "text": "When round 7 ends, then each player holds 7 properties."
    },
    {
      "id": "R13",
      "text": "When a selling round starts, then reveal the next 4 cheques sorted highest to lowest."
    },
    {
      "id": "R14",
      "text": "When selling, then all players at the same moment secretly choose one property from own hand."
    },
    {
      "id": "R15",
      "text": "When chosen properties are revealed, then all properties are different so there are no ties."
    },
    {
      "id": "R16",
      "text": "When cheques are awarded, then highest property adds highest cheque to cheque total and second-highest adds second-highest and third adds third and lowest adds lowest."
    },
    {
      "id": "R17",
      "text": "When cheques are awarded, then played properties are discarded."
    },
    {
      "id": "R18",
      "text": "When a selling round ends, then announce publicly who played which property and who took which cheque and keep running cheque totals private."
    },
    {
      "id": "R19",
      "text": "When round 14 ends, then hands are empty and cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed."
    },
    {
      "id": "R20",
      "text": "When the game ends, then the player with most final money wins."
    },
    {
      "id": "R21",
      "text": "When players tie for most final money, then the tied player with more remaining coins wins and if still tied the game is a draw among them."
    },
    {
      "id": "R22",
      "text": "When choices are made, then there is no talk phase and every choice is sealed."
    }
  ],
  "offers": [
    {
      "question": "sealed bid",
      "who": "all players",
      "options": "in buying rounds 1 to 7: any whole number 0 up to your current coins"
    },
    {
      "question": "choose property to sell",
      "who": "all players",
      "options": "in selling rounds 8 to 14: any one property from your own properties hand (7 options in round 8 down to 1 option in round 14)"
    }
  ],
  "choices": [
    {
      "what": "4 to 4 players with suggested 4",
      "why": "designer fixed 4 seats with 4 cards per round and 28 usable cards for 7 each; smallest table where sealed simultaneous bidding and priority tie-break matter and larger table breaks 4-per-round reveal"
    },
    {
      "what": "no talk poll, sealed poll for bids and for property choice",
      "why": "source says no talk phase and every choice sealed; simultaneous choice must use poll not ask so later seats do not hear earlier answers"
    },
    {
      "what": "half rounded up as (bid+1)//2",
      "why": "matches example 0->0 1->1 2->1 3->2 4->2 with integer arithmetic"
    },
    {
      "what": "rank_by you.final_money * 1000 + you.coins",
      "why": "encodes most final money wins with more remaining coins as tie-break within arithmetic ranking since coins never reach 1000"
    },
    {
      "what": "priority_seat ((round_number-1) mod 4)+1",
      "why": "concrete arithmetic for stated tie-break rotation"
    }
  ],
  "simplifications": [
    {
      "what": "shuffle represented as random draw from list and remove bottom 2 unseen first",
      "why": "engine shuffles by drawing at random from game list with remove/append operations"
    },
    {
      "what": "current_offer holds sorted HIGH to LOW reveal and property_discard holds played properties",
      "why": "engine has no board so cards live in table lists and player lists"
    },
    {
      "what": "final_money attribute set to cheque_total+coins after round 14",
      "why": "enables arithmetic ranking and observable score without model opinion"
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: properties, final_money; table: current_offer.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Remove offered/not-offered checks that conflate bid amounts with property values: with 18 coins bid 5 must be offered so never assert not_offered 5 in buying; assert only public results like current_offer and properties counts. Do not predict exact current_offer after the required round-1/round-8 shuffle and do not use illegal duplicate property decks; use legal full decks or allow any sorted draw.

YOUR PREVIOUS LIST BROKE: its JSON did not parse (Expecting ',' delimiter: line 1 column 2365 (char 2364)). The 5 complete scenarios before the break were kept: Initial holds 18 coins 0 total empty hand; Property deck deals 4 to start buying; Cheque deck reveals 4 cheques in selling; Round 7 buying then round 8 selling boundary; Seven buying rounds deal 28 properties.
Write ONLY the scenarios that come after them (the rules and cases they do not cover yet), as a JSON list in the same format. Write the list again, indented two spaces per level with one key per line, and count the brackets of each scenario before you finish.
````

## Reply

````
[
  {
    "name": "R6 reveal next 4 sorted HIGH to LOW",
    "rule": "R6",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          5,
          12,
          20,
          25
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 0
      },
      {
        "seat": 2,
        "options_include": 0
      },
      {
        "seat": 3,
        "options_include": 0
      },
      {
        "seat": 4,
        "options_include": 0
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          25,
          20,
          12,
          5
        ]
      },
      "lens": {
        "players": {
          "1": {
            "properties": 1
          },
          "2": {
            "properties": 1
          },
          "3": {
            "properties": 1
          },
          "4": {
            "properties": 1
          }
        }
      }
    }
  },
  {
    "name": "R7 bids from 0 up to coins are accepted",
    "rule": "R7",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          6,
          13,
          21,
          26
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 18
      },
      {
        "seat": 2,
        "options_include": 0
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 5
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          26,
          21,
          13,
          6
        ]
      },
      "lens": {
        "players": {
          "1": {
            "properties": 1
          },
          "2": {
            "properties": 1
          },
          "3": {
            "properties": 1
          },
          "4": {
            "properties": 1
          }
        }
      }
    }
  },
  {
    "name": "R8 tie bids break by priority starting seat 2 in round 2",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          5,
          12,
          20,
          25
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 5
      },
      {
        "seat": 2,
        "options_include": 5
      },
      {
        "seat": 3,
        "options_include": 5
      },
      {
        "seat": 4,
        "options_include": 5
      }
    ],
    "expect": {
      "players": {
        "1": {
          "properties": [
            5
          ]
        },
        "2": {
          "properties": [
            25
          ]
        },
        "3": {
          "properties": [
            20
          ]
        },
        "4": {
          "properties": [
            12
          ]
        }
      }
    }
  },
  {
    "name": "R9 first takes HIGH others take lower after half payments",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          5,
          12,
          20,
          25
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 10
      },
      {
        "seat": 2,
        "options_include": 7
      },
      {
        "seat": 3,
        "options_include": 4
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "players": {
        "1": {
          "properties": [
            25
          ]
        },
        "2": {
          "properties": [
            20
          ]
        },
        "3": {
          "properties": [
            12
          ]
        },
        "4": {
          "properties": [
            5
          ]
        }
      }
    }
  },
  {
    "name": "R10 payments leave public property allocation",
    "rule": "R10",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          1,
          2,
          3,
          4
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 8
      },
      {
        "seat": 2,
        "options_include": 6
      },
      {
        "seat": 3,
        "options_include": 4
      },
      {
        "seat": 4,
        "options_include": 2
      }
    ],
    "expect": {
      "players": {
        "1": {
          "properties": [
            4
          ]
        },
        "2": {
          "properties": [
            3
          ]
        },
        "3": {
          "properties": [
            2
          ]
        },
        "4": {
          "properties": [
            1
          ]
        }
      }
    }
  },
  {
    "name": "R11 public HIGH SECOND THIRD LOW allocation",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 3,
        "property_deck": [
          9,
          18,
          27,
          6
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 9
      },
      {
        "seat": 2,
        "options_include": 7
      },
      {
        "seat": 3,
        "options_include": 5
      },
      {
        "seat": 4,
        "options_include": 3
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          27,
          18,
          9,
          6
        ]
      },
      "players": {
        "1": {
          "properties": [
            27
          ]
        },
        "2": {
          "properties": [
            18
          ]
        },
        "3": {
          "properties": [
            9
          ]
        },
        "4": {
          "properties": [
            6
          ]
        }
      }
    }
  },
  {
    "name": "R12 after round 7 each holds 7 properties",
    "rule": "R12",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 7,
        "property_deck": [
          25,
          26,
          27,
          28
        ]
      },
      "players": {
        "1": {
          "properties": [
            1,
            5,
            9,
            13,
            17,
            21
          ]
        },
        "2": {
          "properties": [
            2,
            6,
            10,
            14,
            18,
            22
          ]
        },
        "3": {
          "properties": [
            3,
            7,
            11,
            15,
            19,
            23
          ]
        },
        "4": {
          "properties": [
            4,
            8,
            12,
            16,
            20,
            24
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 8
      },
      {
        "seat": 2,
        "options_include": 5
      },
      {
        "seat": 3,
        "options_include": 3
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {
            "properties": 7
          },
          "2": {
            "properties": 7
          },
          "3": {
            "properties": 7
          },
          "4": {
            "properties": 7
          }
        }
      }
    }
  },
  {
    "name": "R13 selling reveals 4 cheques sorted high to low",
    "rule": "R13",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 9,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ]
        },
        "2": {
          "properties": [
            20
          ]
        },
        "3": {
          "properties": [
            10
          ]
        },
        "4": {
          "properties": [
            1
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          14,
          10,
          7,
          4
        ]
      },
      "lens": {
        "players": {
          "1": {
            "properties": 0
          },
          "2": {
            "properties": 0
          },
          "3": {
            "properties": 0
          },
          "4": {
            "properties": 0
          }
        }
      }
    }
  },
  {
    "name": "R14 secretly choose one property from hand",
    "rule": "R14",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 9,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30,
            1
          ]
        },
        "2": {
          "properties": [
            20,
            2
          ]
        },
        "3": {
          "properties": [
            10,
            3
          ]
        },
        "4": {
          "properties": [
            9,
            4
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 9
      }
    ],
    "expect": {
      "players": {
        "1": {
          "properties": [
            1
          ]
        },
        "2": {
          "properties": [
            2
          ]
        },
        "3": {
          "properties": [
            3
          ]
        },
        "4": {
          "properties": [
            4
          ]
        }
      }
    }
  },
  {
    "name": "R15 distinct properties have no ties",
    "rule": "R15",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 9,
        "cheque_deck": [
          3,
          5,
          8,
          12
        ]
      },
      "players": {
        "1": {
          "properties": [
            28
          ]
        },
        "2": {
          "properties": [
            17
          ]
        },
        "3": {
          "properties": [
            11
          ]
        },
        "4": {
          "properties": [
            2
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 28
      },
      {
        "seat": 2,
        "options_include": 17
      },
      {
        "seat": 3,
        "options_include": 11
      },
      {
        "seat": 4,
        "options_include": 2
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          12,
          8,
          5,
          3
        ]
      },
      "lens": {
        "players": {
          "1": {
            "properties": 0
          },
          "2": {
            "properties": 0
          },
          "3": {
            "properties": 0
          },
          "4": {
            "properties": 0
          }
        }
      }
    }
  },
  {
    "name": "R16 highest property adds highest cheque",
    "rule": "R16",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {
        "round_number": 14,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ],
          "cheque_total": 0,
          "coins": 0
        },
        "2": {
          "properties": [
            20
          ],
          "cheque_total": 0,
          "coins": 0
        },
        "3": {
          "properties": [
            10
          ],
          "cheque_total": 0,
          "coins": 0
        },
        "4": {
          "properties": [
            1
          ],
          "cheque_total": 0,
          "coins": 0
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "winner": 1,
      "players": {
        "1": {
          "final_money": 14
        },
        "2": {
          "final_money": 10
        },
        "3": {
          "final_money": 7
        },
        "4": {
          "final_money": 4
        }
      }
    }
  },
  {
    "name": "R17 played properties are discarded",
    "rule": "R17",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 10,
        "cheque_deck": [
          2,
          6,
          9,
          13
        ]
      },
      "players": {
        "1": {
          "properties": [
            29,
            5
          ]
        },
        "2": {
          "properties": [
            22,
            6
          ]
        },
        "3": {
          "properties": [
            15,
            7
          ]
        },
        "4": {
          "properties": [
            8,
            3
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 29
      },
      {
        "seat": 2,
        "options_include": 22
      },
      {
        "seat": 3,
        "options_include": 15
      },
      {
        "seat": 4,
        "options_include": 8
      }
    ],
    "expect": {
      "players": {
        "1": {
          "properties": [
            5
          ]
        },
        "2": {
          "properties": [
            6
          ]
        },
        "3": {
          "properties": [
            7
          ]
        },
        "4": {
          "properties": [
            3
          ]
        }
      }
    }
  },
  {
    "name": "R18 public property and cheque allocation",
    "rule": "R18",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 9,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30,
            2
          ]
        },
        "2": {
          "properties": [
            20,
            3
          ]
        },
        "3": {
          "properties": [
            10,
            5
          ]
        },
        "4": {
          "properties": [
            1,
            6
          ]
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          14,
          10,
          7,
          4
        ]
      },
      "players": {
        "1": {
          "properties": [
            2
          ]
        },
        "2": {
          "properties": [
            3
          ]
        },
        "3": {
          "properties": [
            5
          ]
        },
        "4": {
          "properties": [
            6
          ]
        }
      }
    }
  },
  {
    "name": "R19 hands empty and final money revealed at end",
    "rule": "R19",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {
        "round_number": 14,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ],
          "cheque_total": 10,
          "coins": 2
        },
        "2": {
          "properties": [
            20
          ],
          "cheque_total": 10,
          "coins": 2
        },
        "3": {
          "properties": [
            10
          ],
          "cheque_total": 10,
          "coins": 2
        },
        "4": {
          "properties": [
            1
          ],
          "cheque_total": 10,
          "coins": 2
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "winner": 1,
      "players": {
        "1": {
          "final_money": 26
        },
        "2": {
          "final_money": 22
        },
        "3": {
          "final_money": 19
        },
        "4": {
          "final_money": 16
        }
      },
      "lens": {
        "players": {
          "1": {
            "properties": 0
          },
          "2": {
            "properties": 0
          },
          "3": {
            "properties": 0
          },
          "4": {
            "properties": 0
          }
        }
      }
    }
  },
  {
    "name": "R20 most final money wins",
    "rule": "R20",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {
        "round_number": 14,
        "cheque_deck": [
          5,
          8,
          11,
          15
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ],
          "cheque_total": 20,
          "coins": 1
        },
        "2": {
          "properties": [
            19
          ],
          "cheque_total": 20,
          "coins": 1
        },
        "3": {
          "properties": [
            12
          ],
          "cheque_total": 20,
          "coins": 1
        },
        "4": {
          "properties": [
            4
          ],
          "cheque_total": 20,
          "coins": 1
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 19
      },
      {
        "seat": 3,
        "options_include": 12
      },
      {
        "seat": 4,
        "options_include": 4
      }
    ],
    "expect": {
      "winner": 1,
      "players": {
        "1": {
          "final_money": 36
        },
        "2": {
          "final_money": 32
        },
        "3": {
          "final_money": 29
        },
        "4": {
          "final_money": 26
        }
      }
    }
  },
  {
    "name": "R21 tie final more coins wins",
    "rule": "R21",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {
        "round_number": 14,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ],
          "cheque_total": 50,
          "coins": 0
        },
        "2": {
          "properties": [
            20
          ],
          "cheque_total": 40,
          "coins": 14
        },
        "3": {
          "properties": [
            10
          ],
          "cheque_total": 0,
          "coins": 0
        },
        "4": {
          "properties": [
            1
          ],
          "cheque_total": 0,
          "coins": 0
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "winner": 2,
      "players": {
        "1": {
          "final_money": 64
        },
        "2": {
          "final_money": 64
        },
        "3": {
          "final_money": 7
        },
        "4": {
          "final_money": 4
        }
      }
    }
  },
  {
    "name": "R21 still tied shares win",
    "rule": "R21",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {
        "round_number": 14,
        "cheque_deck": [
          4,
          7,
          10,
          14
        ]
      },
      "players": {
        "1": {
          "properties": [
            30
          ],
          "cheque_total": 45,
          "coins": 5
        },
        "2": {
          "properties": [
            20
          ],
          "cheque_total": 49,
          "coins": 5
        },
        "3": {
          "properties": [
            10
          ],
          "cheque_total": 0,
          "coins": 0
        },
        "4": {
          "properties": [
            1
          ],
          "cheque_total": 0,
          "coins": 0
        }
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 30
      },
      {
        "seat": 2,
        "options_include": 20
      },
      {
        "seat": 3,
        "options_include": 10
      },
      {
        "seat": 4,
        "options_include": 1
      }
    ],
    "expect": {
      "winner": [
        1,
        2
      ],
      "players": {
        "1": {
          "final_money": 64
        },
        "2": {
          "final_money": 64
        },
        "3": {
          "final_money": 7
        },
        "4": {
          "final_money": 4
        }
      }
    }
  },
  {
    "name": "R22 sealed simultaneous choices",
    "rule": "R22",
    "players": 4,
    "seed": 1,
    "default": "decline",
    "rounds": 1,
    "given": {
      "game": {
        "round_number": 2,
        "property_deck": [
          7,
          14,
          21,
          28
        ]
      }
    },
    "rules": [
      {
        "seat": 1,
        "options_include": 12
      },
      {
        "seat": 2,
        "options_include": 9
      },
      {
        "seat": 3,
        "options_include": 6
      },
      {
        "seat": 4,
        "options_include": 3
      }
    ],
    "expect": {
      "game": {
        "current_offer": [
          28,
          21,
          14,
          7
        ]
      },
      "lens": {
        "players": {
          "1": {
            "properties": 1
          },
          "2": {
            "properties": 1
          },
          "3": {
            "properties": 1
          },
          "4": {
            "properties": 1
          }
        }
      }
    }
  }
]
````
