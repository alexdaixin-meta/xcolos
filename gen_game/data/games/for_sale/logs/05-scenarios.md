# 05 scenarios

- time: 2026-10-27T08:39:30+00:00 (66.7s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 a7edf5281e41f1f2, reply sha256 6c0f8586e97ac970

## Sent

````
SPEC:
{
  "name": "For Sale: Sealed Bids",
  "summary": "Three players spend 8 sealed-bid rounds buying property cards with private coins, then 8 simultaneous rounds selling those properties for cheques; the most cheques plus leftover coins wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "starting_coins": 18,
    "property_min": 1,
    "property_max": 30,
    "property_deck_size": 30,
    "properties_used": 24,
    "properties_unused": 6,
    "cheque_min_value": 0,
    "cheque_max_value": 15,
    "cheque_missing_value": 1,
    "cheque_distinct_values": 15,
    "cheque_copies_each": 2,
    "cheque_deck_size": 30,
    "cheques_used": 24,
    "total_rounds": 16,
    "buying_rounds": 8,
    "first_selling_round": 9,
    "cards_revealed_per_round": 3,
    "first_place_pay_fraction": 1,
    "second_third_pay_divisor": 2,
    "properties_per_player_after_buying": 8,
    "initial_cheque_total": 0,
    "tie_break_bid_multiplier": 10,
    "rank_coin_tiebreak_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "coins",
        "type": "number",
        "visible": "ally",
        "initial": 18,
        "meaning": "Private coin total. Bids are paid from it, and what is left counts toward final money.",
        "observable": false
      },
      {
        "key": "cheques",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Private running total of cheques won in selling rounds.",
        "observable": false
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Property cards the player holds. Hands are public.",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This buying round's secret bid, from 0 to coins.",
        "observable": false
      },
      {
        "key": "bid_key",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Engine scratch: bid*10 plus a priority weight of 3, 2 or 1. It ranks the bids with this round's tie-break. The rules never mention it.",
        "observable": false
      },
      {
        "key": "bid_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This buying round's rank: 1 takes HIGH, 2 takes MIDDLE, 3 takes LOW. It is announced through who took which card.",
        "observable": false
      },
      {
        "key": "played",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The property chosen in this selling round, revealed after everyone has chosen.",
        "observable": false
      },
      {
        "key": "final_money",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Set and revealed after round 16 as cheques + coins.",
        "observable": true
      },
      {
        "key": "final_coins",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Remaining coins, revealed after round 16 because they are the tie-break.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current round, 1 to 16. Rounds 1-8 are buying rounds and rounds 9-16 are selling rounds.",
        "observable": true
      },
      {
        "key": "property_deck",
        "type": "list",
        "visible": "none",
        "initial": "[1..30]",
        "meaning": "The undrawn property cards. Drawing at random is the shuffle; 6 cards are never drawn.",
        "observable": false
      },
      {
        "key": "cheque_deck",
        "type": "list",
        "visible": "none",
        "initial": "[0,0,2,2,3,3,...,15,15]",
        "meaning": "The undrawn cheques, 30 in all. Drawing at random is the shuffle; 6 are never drawn.",
        "observable": false
      },
      {
        "key": "revealed_properties",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The 3 property cards revealed this buying round.",
        "observable": false
      },
      {
        "key": "revealed_cheques",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The 3 cheques revealed this selling round.",
        "observable": false
      },
      {
        "key": "priority_first",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat with first tie-break priority this round: ((round-1) mod 3)+1.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat the 3 players as seats 1, 2 and 3.",
    "Give each player coins = 18, cheques = 0 and an empty public hand.",
    "Put the property cards 1 to 30, one of each, into the hidden table list property_deck.",
    "Put two of each cheque value 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 and 15 (30 cheques) into the hidden table list cheque_deck.",
    "Set round = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Set priority_first = ((round-1) mod 3)+1. When round <= 8: clear revealed_properties, then draw 3 cards at random from property_deck, removing each from property_deck and appending it to revealed_properties. Announce the 3 cards as LOW = min, MIDDLE = the remaining card and HIGH = max, and announce priority_first."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When round <= 8: each player is sent their own coins, all hands, revealed_properties and priority_first."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to your coins",
      "effect": "When round <= 8: set bid for each player. Nobody sees any bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round <= 8: for each player, bid_key = bid*10 + (3 - ((seat - priority_first + 3) mod 3)). Then bid_rank = 1 + the number of other players whose bid_key is larger than this player's."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round <= 8: the player with bid_rank 1 appends max(revealed_properties) to hand and pays coins -= bid. The player with bid_rank 2 appends the middle card to hand and pays coins -= floor(bid/2). The player with bid_rank 3 appends min(revealed_properties) to hand and pays coins -= floor(bid/2). Payments go to the bank. Publicly announce which seat took LOW, MIDDLE and HIGH, without bids or coin totals."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round >= 9: clear revealed_cheques, then draw 3 cheques at random from cheque_deck, removing each from cheque_deck and appending it to revealed_cheques. Announce the 3 cheques."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When round >= 9: each player is sent their own cheques and coins, all hands, and revealed_cheques."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one property card from your own hand",
      "effect": "When round >= 9: set played for each player. The choices are revealed only after all are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round >= 9: the player with the highest played adds max(revealed_cheques) to cheques. The player with the middle played adds the middle cheque. The player with the lowest played adds min(revealed_cheques). Each player removes played from hand, which discards the card. Publicly announce who played which property and who took which cheque; cheque totals stay private."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round > 16: final_money = cheques + coins and final_coins = coins, both revealed publicly."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round > 16; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round > 16",
    "rank_by": "you.final_money * 100 + you.final_coins",
    "decided_by": "The most final money (cheque total plus remaining coins) wins. A tie goes to the tied player with more remaining coins; coins are at most 18, so the x100 weighting keeps money first. Players still level share the win, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, each of the 3 players has coins = 18, cheques = 0 and an empty hand."
    },
    {
      "id": "R2",
      "text": "When the game starts, property_deck holds the 30 cards 1 to 30, and cheque_deck holds two each of 0 and 2 to 15, for 30 cheques."
    },
    {
      "id": "R3",
      "text": "When a buying round (1-8) begins, 3 cards are drawn at random from property_deck into revealed_properties, and property_deck shrinks by 3."
    },
    {
      "id": "R4",
      "text": "When a player bids in a buying round, the bid is a whole number from 0 to that player's current coins, and all bids are made simultaneously."
    },
    {
      "id": "R5",
      "text": "When bids are ranked, the higher bid ranks higher."
    },
    {
      "id": "R6",
      "text": "When bids tie in round r, priority goes first to seat ((r-1) mod 3)+1, then to the next seat, wrapping from 3 to 1; for example, in round 2 the order is 2, 3, 1."
    },
    {
      "id": "R7",
      "text": "When a player ranks first in a buying round, they take the HIGH card and pay their full bid; for example, a bid of 7 costs 7."
    },
    {
      "id": "R8",
      "text": "When a player ranks second or third, they take MIDDLE or LOW respectively and pay floor(bid/2); for example, a bid of 5 costs 2."
    },
    {
      "id": "R9",
      "text": "When a buying round ends, it is announced who took LOW, MIDDLE and HIGH, but bids and coin totals are not announced."
    },
    {
      "id": "R10",
      "text": "When round 8 ends, each player holds exactly 8 properties and 6 cards remain unused in property_deck."
    },
    {
      "id": "R11",
      "text": "When a selling round (9-16) begins, 3 cheques are drawn at random from cheque_deck into revealed_cheques."
    },
    {
      "id": "R12",
      "text": "When a selling round is played, each player simultaneously chooses one property from their own hand."
    },
    {
      "id": "R13",
      "text": "When the properties are revealed, the highest takes the highest cheque, the middle takes the middle cheque and the lowest takes the lowest cheque, each added to that player's cheques."
    },
    {
      "id": "R14",
      "text": "When a property is played, it is removed from its owner's hand."
    },
    {
      "id": "R15",
      "text": "When a selling round ends, it is announced who played which property and who took which cheque; cheque totals stay private."
    },
    {
      "id": "R16",
      "text": "When round 16 ends, the game ends and each player's final_money = cheques + coins is revealed."
    },
    {
      "id": "R17",
      "text": "When final money is compared, the most wins; a tie goes to more remaining coins, and a remaining tie is a shared win (a draw)."
    }
  ],
  "offers": [
    {
      "question": "Buying round bid (rounds 1-8)",
      "who": "all three seats at once",
      "options": "every whole number from 0 to that seat's current coins"
    },
    {
      "question": "Selling round property choice (rounds 9-16)",
      "who": "all three seats at once",
      "options": "each property card currently in that seat's own hand, and nothing else"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3. The 3-card reveals, the 3-way priority rotation and the LOW/MIDDLE/HIGH payment tiers are all built for exactly 3 seats."
    },
    {
      "what": "No talk step before bids or plays",
      "why": "The source has no communication phase, and talk would add a mechanic. Strategy comes from reading public hands and the inferable coin spending: bid low when the top card is weak, keep coins for the tie-break, and time high properties against strong cheques."
    },
    {
      "what": "Tie-break computed as bid*10 + priority weight (3, 2, 1)",
      "why": "This puts the rotating priority rule into one arithmetic key. Bids are at most 18, so the weight never outranks a higher bid."
    },
    {
      "what": "bid_key is visible to its owner only (ally)",
      "why": "It is engine scratch derived from the player's own private bid, and a player attribute cannot be fully hidden."
    },
    {
      "what": "Cheque values described by numeric parameters (min 0, max 15, value 1 missing, 2 copies each)",
      "why": "Parameters must be numbers, so the value list is given as its bounds and the one skipped value."
    },
    {
      "what": "rank_by = final_money*100 + final_coins",
      "why": "This encodes the remaining-coins tie-break in one expression. Coins never exceed 18, so the x100 weighting keeps final money first."
    },
    {
      "what": "Separate public final_coins attribute",
      "why": "Remaining coins decide ties and are revealed at the end, so they are made public then. Coins stay private during play."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling and taking the top of a deck are done as random draws from the deck list",
      "why": "Drawing at random is equivalent to drawing from the top of a shuffled deck. The 6 never-drawn cards and cheques simply remain in the hidden lists."
    },
    {
      "what": "Buying and selling steps share one flat round list, gated by 'when round <= 8' and 'when round >= 9'",
      "why": "The engine has one repeating step list. Per-step arithmetic conditions select the phase without needing conditional blocks."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand, final_money, final_coins; table: round.
````

## Reply

````
```json
[
  {
    "name": "R1: at setup no seat holds any property and the game is at round 1",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}},
      "players": {"1": {"hand": []}, "2": {"hand": []}, "3": {"hand": []}},
      "game": {"round": 1}
    }
  },
  {
    "name": "R2: at setup property_deck holds 30 cards and cheque_deck holds 30 cheques",
    "rule": "R2",
    "players": 3,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"property_deck": 30, "cheque_deck": 30}}
    }
  },
  {
    "name": "R3: a buying round draws 3 properties, so the deck shrinks by 3 and each seat gains one card (which cards is chance)",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "expect": {
      "lens": {"game": {"property_deck": 27}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}},
      "game": {"round": 2}
    }
  },
  {
    "name": "R4: bid options run from 0 to the seat's current coins and no higher",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"coins": 5}},
      "game": {"round": 1, "property_deck": [5, 10, 20]}
    },
    "expect": {
      "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 5}],
      "not_offered": [{"seat": 1, "option": 6}, {"seat": 1, "option": 18}]
    }
  },
  {
    "name": "R5: the highest bid takes HIGH, the next takes MIDDLE and the lowest takes LOW",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 1, "property_deck": [5, 10, 20]}},
    "rules": [
      {"seat": 3, "options_include": 4},
      {"seat": 2, "options_include": 2},
      {"seat": 1, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"hand": [5]}, "2": {"hand": [10]}, "3": {"hand": [20]}}
    }
  },
  {
    "name": "R6: in round 2, tied bids give priority in the order 2, 3, 1",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 2, "property_deck": [5, 10, 20]}},
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "players": {"1": {"hand": [5]}, "2": {"hand": [20]}, "3": {"hand": [10]}}
    }
  },
  {
    "name": "R6: in round 1, tied bids give priority in the order 1, 2, 3",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 1, "property_deck": [5, 10, 20]}},
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"hand": [20]}, "2": {"hand": [10]}, "3": {"hand": [5]}}
    }
  },
  {
    "name": "R7: the top bidder pays the full bid of 7; all cheques are 0, so final money is the coins left",
    "rule": "R7",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 18, "cheques": 0, "hand": [1, 2, 3, 4, 6, 7, 8]},
        "2": {"coins": 18, "cheques": 0, "hand": [9, 11, 12, 13, 14, 15, 16]},
        "3": {"coins": 18, "cheques": 0, "hand": [17, 18, 19, 21, 22, 23, 24]}
      },
      "game": {"round": 8, "property_deck": [5, 10, 20], "cheque_deck": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    },
    "rules": [
      {"seat": 1, "options_include": 7},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 1111, "2": 1818, "3": 1818},
      "players": {
        "1": {"final_coins": 11, "final_money": 11, "hand": []},
        "2": {"final_coins": 18, "final_money": 18, "hand": []},
        "3": {"final_coins": 18, "final_money": 18, "hand": []}
      },
      "game": {"round": 17}
    }
  },
  {
    "name": "R8: second and third place pay floor(bid/2), so a bid of 5 costs 2 and a bid of 3 costs 1; all cheques are 0",
    "rule": "R8",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 18, "cheques": 0, "hand": [1, 2, 3, 4, 6, 7, 8]},
        "2": {"coins": 18, "cheques": 0, "hand": [9, 11, 12, 13, 14, 15, 16]},
        "3": {"coins": 18, "cheques": 0, "hand": [17, 18, 19, 21, 22, 23, 24]}
      },
      "game": {"round": 8, "property_deck": [5, 10, 20], "cheque_deck": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    },
    "rules": [
      {"seat": 1, "options_include": 7},
      {"seat": 2, "options_include": 5},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "winner": 3,
      "standings": {"1": 1111, "2": 1616, "3": 1717},
      "players": {
        "1": {"final_coins": 11, "final_money": 11},
        "2": {"final_coins": 16, "final_money": 16},
        "3": {"final_coins": 17, "final_money": 17}
      }
    }
  },
  {
    "name": "R9: after a buying round the public hands show who took LOW, MIDDLE and HIGH",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"round": 3, "property_deck": [2, 15, 28]}},
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"hand": [28]}, "2": {"hand": [15]}, "3": {"hand": [2]}},
      "game": {"round": 4}
    }
  },
  {
    "name": "R10: after round 8 each seat holds 8 properties and 6 cards stay in property_deck",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3, 4, 6, 7, 8]},
        "2": {"hand": [9, 11, 12, 13, 14, 15, 16]},
        "3": {"hand": [17, 18, 19, 21, 22, 23, 24]}
      },
      "game": {"round": 8, "property_deck": [5, 10, 20, 25, 26, 27, 28, 29, 30]}
    },
    "expect": {
      "lens": {"game": {"property_deck": 6}, "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}},
      "game": {"round": 9}
    }
  },
  {
    "name": "R11: a selling round draws 3 cheques from cheque_deck (which cheques is chance)",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3, 4, 6, 7, 8, 5]},
        "2": {"hand": [9, 11, 12, 13, 14, 15, 16, 10]},
        "3": {"hand": [17, 18, 19, 21, 22, 23, 24, 20]}
      },
      "game": {"round": 9}
    },
    "expect": {
      "lens": {"game": {"cheque_deck": 27}, "players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}}},
      "game": {"round": 10}
    }
  },
  {
    "name": "R12: in a selling round a seat is offered only the cards in its own hand",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [3, 7]}, "2": {"hand": [10, 12]}, "3": {"hand": [1, 20]}},
      "game": {"round": 9}
    },
    "expect": {
      "offered": [{"seat": 1, "option": 3}, {"seat": 1, "option": 7}, {"seat": 2, "option": 12}],
      "not_offered": [{"seat": 1, "option": 10}, {"seat": 1, "option": 20}, {"seat": 2, "option": 3}, {"seat": 3, "option": 7}]
    }
  },
  {
    "name": "R13: in the last round the highest property takes cheque 15, the middle takes 9 and the lowest takes 2",
    "rule": "R13",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 3, "cheques": 0, "hand": [30]},
        "2": {"coins": 3, "cheques": 0, "hand": [10]},
        "3": {"coins": 3, "cheques": 0, "hand": [5]}
      },
      "game": {"round": 16, "cheque_deck": [2, 9, 15]}
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 1803, "2": 1203, "3": 503},
      "players": {"1": {"final_money": 18}, "2": {"final_money": 12}, "3": {"final_money": 5}}
    }
  },
  {
    "name": "R14: a played property is removed from its owner's hand",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [3, 7]}, "2": {"hand": [10, 12]}, "3": {"hand": [1, 20]}},
      "game": {"round": 9}
    },
    "rules": [
      {"seat": 1, "options_include": 7},
      {"seat": 2, "options_include": 12},
      {"seat": 3, "options_include": 1}
    ],
    "expect": {
      "players": {"1": {"hand": [3]}, "2": {"hand": [10]}, "3": {"hand": [20]}},
      "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}
    }
  },
  {
    "name": "R15: after a selling round the public hands show which property each seat played",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [4, 25]}, "2": {"hand": [11, 13]}, "3": {"hand": [2, 29]}},
      "game": {"round": 12}
    },
    "rules": [
      {"seat": 1, "options_include": 25},
      {"seat": 2, "options_include": 11},
      {"seat": 3, "options_include": 2}
    ],
    "expect": {
      "players": {"1": {"hand": [4]}, "2": {"hand": [13]}, "3": {"hand": [29]}},
      "game": {"round": 13}
    }
  },
  {
    "name": "R16: after round 16 the game ends with final_money = cheques + coins",
    "rule": "R16",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 4, "cheques": 10, "hand": [5]},
        "2": {"coins": 0, "cheques": 20, "hand": [6]},
        "3": {"coins": 8, "cheques": 5, "hand": [7]}
      },
      "game": {"round": 16, "cheque_deck": [0, 0, 0]}
    },
    "expect": {
      "winner": 2,
      "standings": {"1": 1404, "2": 2000, "3": 1308},
      "players": {
        "1": {"final_money": 14, "final_coins": 4},
        "2": {"final_money": 20, "final_coins": 0},
        "3": {"final_money": 13, "final_coins": 8}
      },
      "game": {"round": 17}
    }
  },
  {
    "name": "R17: equal final money is won by the seat with more remaining coins",
    "rule": "R17",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 5, "cheques": 10, "hand": [5]},
        "2": {"coins": 3, "cheques": 12, "hand": [6]},
        "3": {"coins": 0, "cheques": 0, "hand": [7]}
      },
      "game": {"round": 16, "cheque_deck": [0, 0, 0]}
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 1505, "2": 1503, "3": 0},
      "players": {
        "1": {"final_money": 15, "final_coins": 5},
        "2": {"final_money": 15, "final_coins": 3},
        "3": {"final_money": 0, "final_coins": 0}
      }
    }
  },
  {
    "name": "R17: seats level on both money and coins share the win",
    "rule": "R17",
    "players": 3,
    "given": {
      "players": {
        "1": {"coins": 6, "cheques": 9, "hand": [5]},
        "2": {"coins": 6, "cheques": 9, "hand": [6]},
        "3": {"coins": 2, "cheques": 4, "hand": [7]}
      },
      "game": {"round": 16, "cheque_deck": [0, 0, 0]}
    },
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 1506, "2": 1506, "3": 602},
      "players": {
        "1": {"final_money": 15, "final_coins": 6},
        "2": {"final_money": 15, "final_coins": 6},
        "3": {"final_money": 6, "final_coins": 2}
      }
    }
  }
]
```
````
