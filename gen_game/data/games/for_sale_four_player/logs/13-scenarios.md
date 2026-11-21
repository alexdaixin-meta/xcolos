# 13 scenarios

- time: 2026-11-21T01:30:45+00:00 (178.0s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 d88eddd8fe7e407b, reply sha256 e1738ba6361a6b8e

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
````

## Reply

````
[{"default": "decline", "expect": {"game": {"current_offer": []}, "players": {"1": {"final_money": 0, "properties": []}, "2": {"final_money": 0, "properties": []}, "3": {"final_money": 0, "properties": []}, "4": {"final_money": 0, "properties": []}}}, "name": "Initial holds 18 coins 0 total empty hand", "players": 4, "rounds": 0, "rule": "R1", "rules": [], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 1}, "2": {"properties": 1}, "3": {"properties": 1}, "4": {"properties": 1}}}}, "name": "Property deck deals 4 to start buying", "players": 4, "rounds": 1, "rule": "R2", "rules": [], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 0}, "2": {"properties": 0}, "3": {"properties": 0}, "4": {"properties": 0}}}}, "given": {"game": {"property_deck": [], "round_number": 8}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "name": "Cheque deck reveals 4 cheques in selling", "players": 4, "rounds": 1, "rule": "R3", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 6}, "2": {"properties": 6}, "3": {"properties": 6}, "4": {"properties": 6}}}}, "given": {"game": {"property_deck": [25, 26, 27, 28], "round_number": 7}, "players": {"1": {"properties": [1, 2, 3, 4, 5, 6]}, "2": {"properties": [7, 8, 9, 10, 11, 12]}, "3": {"properties": [13, 14, 15, 16, 17, 18]}, "4": {"properties": [19, 20, 21, 22, 23, 24]}}}, "name": "Round 7 buying then round 8 selling boundary", "players": 4, "rounds": 2, "rule": "R4", "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 13}, {"seat": 4, "options_include": 19}], "seed": 1}, {"default": "decline", "expect": {"lens": {"players": {"1": {"properties": 7}, "2": {"properties": 7}, "3": {"properties": 7}, "4": {"properties": 7}}}}, "name": "Seven buying rounds deal 28 properties", "players": 4, "rounds": 7, "rule": "R5", "rules": [], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [30, 20, 10, 1]}}}, "given": {"game": {"property_deck": [30, 20, 10, 1], "round_number": 2}, "players": {"1": {"properties": []}, "2": {"properties": []}, "3": {"properties": []}, "4": {"properties": []}}}, "name": "Buying reveal sorted HIGH to LOW", "players": 4, "rounds": 1, "rule": "R6", "rules": [], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 1}, "2": {"properties": 1}, "3": {"properties": 1}, "4": {"properties": 1}}}}, "name": "Sealed bid 5 within coins is allowed", "players": 4, "rounds": 1, "rule": "R7", "rules": [{"seat": 1, "options_include": 5}], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [30, 20, 10, 1]}, "players": {"1": {"properties": [1]}, "2": {"properties": [30]}, "3": {"properties": [20]}, "4": {"properties": [10]}}}, "given": {"game": {"property_deck": [30, 20, 10, 1], "round_number": 2}, "players": {"1": {"properties": []}, "2": {"properties": []}, "3": {"properties": []}, "4": {"properties": []}}}, "name": "Tie bids break by priority seat 2 order", "players": 4, "rounds": 1, "rule": "R8", "rules": [], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [30, 20, 10, 1]}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "given": {"game": {"property_deck": [30, 20, 10, 1], "round_number": 2}, "players": {"1": {"properties": []}, "2": {"properties": []}, "3": {"properties": []}, "4": {"properties": []}}}, "name": "First takes HIGH others take lower in order", "players": 4, "rounds": 1, "rule": "R9", "rules": [{"seat": 1, "options_include": 10}, {"seat": 2, "options_include": 6}, {"seat": 3, "options_include": 4}, {"seat": 4, "options_include": 0}], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [30, 20, 10, 1]}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "given": {"game": {"property_deck": [30, 20, 10, 1], "round_number": 2}, "players": {"1": {"properties": []}, "2": {"properties": []}, "3": {"properties": []}, "4": {"properties": []}}}, "name": "Payments to bank for HIGH and half shares", "players": 4, "rounds": 1, "rule": "R10", "rules": [{"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 4}, {"seat": 3, "options_include": 2}, {"seat": 4, "options_include": 0}], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [30, 20, 10, 1]}, "players": {"1": {"properties": [1]}, "2": {"properties": [30]}, "3": {"properties": [20]}, "4": {"properties": [10]}}}, "given": {"game": {"property_deck": [30, 20, 10, 1], "round_number": 2}, "players": {"1": {"properties": []}, "2": {"properties": []}, "3": {"properties": []}, "4": {"properties": []}}}, "name": "Public takes HIGH SECOND THIRD LOW", "players": 4, "rounds": 1, "rule": "R11", "rules": [], "seed": 1}, {"default": "decline", "expect": {"lens": {"players": {"1": {"properties": 7}, "2": {"properties": 7}, "3": {"properties": 7}, "4": {"properties": 7}}}}, "given": {"game": {"property_deck": [25, 26, 27, 28], "round_number": 7}, "players": {"1": {"properties": [1, 2, 3, 4, 5, 6]}, "2": {"properties": [7, 8, 9, 10, 11, 12]}, "3": {"properties": [13, 14, 15, 16, 17, 18]}, "4": {"properties": [19, 20, 21, 22, 23, 24]}}}, "name": "After round 7 each holds 7 properties", "players": 4, "rounds": 1, "rule": "R12", "rules": [], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [15, 10, 5, 0]}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 9}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "name": "Selling reveal sorted highest to lowest", "players": 4, "rounds": 1, "rule": "R13", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [15, 10, 5, 0]}, "lens": {"players": {"1": {"properties": 1}, "2": {"properties": 1}, "3": {"properties": 1}, "4": {"properties": 1}}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 9}, "players": {"1": {"properties": [30, 29]}, "2": {"properties": [20, 19]}, "3": {"properties": [10, 9]}, "4": {"properties": [4, 3]}}}, "name": "Secretly choose one property from hand", "players": 4, "rounds": 1, "rule": "R14", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 4}], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 0}, "2": {"properties": 0}, "3": {"properties": 0}, "4": {"properties": 0}}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 9}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "name": "Distinct properties so no ties", "players": 4, "rounds": 1, "rule": "R15", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"players": {"1": {"final_money": 15}, "2": {"final_money": 10}, "3": {"final_money": 5}, "4": {"final_money": 0}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 14}, "players": {"1": {"cheque_total": 0, "coins": 0, "properties": [30]}, "2": {"cheque_total": 0, "coins": 0, "properties": [20]}, "3": {"cheque_total": 0, "coins": 0, "properties": [10]}, "4": {"cheque_total": 0, "coins": 0, "properties": [1]}}}, "name": "Highest property takes highest cheque", "players": 4, "rounds": 1, "rule": "R16", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"lens": {"players": {"1": {"properties": 0}, "2": {"properties": 0}, "3": {"properties": 0}, "4": {"properties": 0}}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 14}, "players": {"1": {"cheque_total": 0, "coins": 0, "properties": [30]}, "2": {"cheque_total": 0, "coins": 0, "properties": [20]}, "3": {"cheque_total": 0, "coins": 0, "properties": [10]}, "4": {"cheque_total": 0, "coins": 0, "properties": [1]}}}, "name": "Played properties are discarded", "players": 4, "rounds": 1, "rule": "R17", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"game": {"current_offer": [15, 10, 5, 0]}, "players": {"1": {"final_money": 0}, "2": {"final_money": 0}, "3": {"final_money": 0}, "4": {"final_money": 0}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 9}, "players": {"1": {"properties": [30]}, "2": {"properties": [20]}, "3": {"properties": [10]}, "4": {"properties": [1]}}}, "name": "Public plays and takes keep totals private", "players": 4, "rounds": 1, "rule": "R18", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"lens": {"players": {"1": {"properties": 0}, "2": {"properties": 0}, "3": {"properties": 0}, "4": {"properties": 0}}}, "players": {"1": {"final_money": 15}, "2": {"final_money": 10}, "3": {"final_money": 5}, "4": {"final_money": 0}}}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 14}, "players": {"1": {"cheque_total": 0, "coins": 0, "properties": [30]}, "2": {"cheque_total": 0, "coins": 0, "properties": [20]}, "3": {"cheque_total": 0, "coins": 0, "properties": [10]}, "4": {"cheque_total": 0, "coins": 0, "properties": [1]}}}, "name": "Round 14 ends hands empty totals revealed", "players": 4, "rounds": 1, "rule": "R19", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"players": {"1": {"final_money": 15}, "2": {"final_money": 10}, "3": {"final_money": 5}, "4": {"final_money": 0}}, "winner": 1}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 14}, "players": {"1": {"cheque_total": 0, "coins": 0, "properties": [30]}, "2": {"cheque_total": 0, "coins": 0, "properties": [20]}, "3": {"cheque_total": 0, "coins": 0, "properties": [10]}, "4": {"cheque_total": 0, "coins": 0, "properties": [1]}}}, "name": "Most final money wins", "players": 4, "rule": "R20", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"players": {"1": {"final_money": 15}, "2": {"final_money": 15}, "3": {"final_money": 5}, "4": {"final_money": 0}}, "winner": 2}, "given": {"game": {"cheque_deck": [15, 10, 5, 0], "property_deck": [], "round_number": 14}, "players": {"1": {"cheque_total": 0, "coins": 0, "properties": [30]}, "2": {"cheque_total": 0, "coins": 5, "properties": [20]}, "3": {"cheque_total": 0, "coins": 0, "properties": [10]}, "4": {"cheque_total": 0, "coins": 0, "properties": [1]}}}, "name": "Tie on final money more coins wins", "players": 4, "rule": "R21", "rules": [{"seat": 1, "options_include": 30}, {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 10}, {"seat": 4, "options_include": 1}], "seed": 1}, {"default": "decline", "expect": {"lens": {"game": {"current_offer": 4}, "players": {"1": {"properties": 1}, "2": {"properties": 1}, "3": {"properties": 1}, "4": {"properties": 1}}}}, "name": "All choices sealed simultaneous bids", "players": 4, "rounds": 1, "rule": "R22", "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 4}, {"seat": 3, "options_include": 3}, {"seat": 4, "options_include": 2}], "seed": 1}]
````
