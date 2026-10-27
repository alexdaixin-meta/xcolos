# 07 scenarios

- time: 2026-10-27T20:48:38+00:00 (57.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 a6b9962a2b98ea1b, reply sha256 2a56362fd79c87f9

## Sent

````
SPEC:
{
  "name": "Scriptorium Lots (Seller's Edition)",
  "summary": "Three players take turns seeing a secret two-card lot. The active player keeps one card and auctions the other to the two bidders. Winners can nudge colour worths, and majorities in each colour plus leftover gold decide the victor.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "start_gold": 12,
    "start_holding": 0,
    "start_worth": 3,
    "worth_min": 1,
    "worth_max": 5,
    "worth_shift": 1,
    "rounds": 12,
    "lot_count": 12,
    "cards_per_lot": 2,
    "lot_sum": 5,
    "lots_per_card": 2,
    "active_turns_per_seat": 4,
    "min_bid": 0,
    "tie_share_divisor": 2,
    "gold_per_vp": 4,
    "rank_vp_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "gold",
        "type": "number",
        "visible": "public",
        "initial": 12,
        "meaning": "Gold held; spent on bids, received when selling; 1 VP per full 4 at the end",
        "observable": true
      },
      {
        "key": "red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Own Red holding (sum of Red card values received); never shown to others during the game",
        "observable": false
      },
      {
        "key": "blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Own Blue holding",
        "observable": false
      },
      {
        "key": "green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Own Green holding",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid (bidders only); announced at resolve",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's non-binding talk message, shown after all are in",
        "observable": false
      },
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final victory points = colour VP + floor(gold/4), computed after round 12",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "lots",
        "type": "list",
        "visible": "none",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ],
        "meaning": "The 12 lots in a hidden random order fixed at setup; round k uses the k-th lot",
        "observable": false
      },
      {
        "key": "lot_list",
        "type": "list",
        "visible": "public",
        "initial": [
          "R1+B4",
          "R2+B3",
          "B1+R4",
          "B2+R3",
          "R1+G4",
          "R2+G3",
          "G1+R4",
          "G2+R3",
          "B1+G4",
          "B2+G3",
          "G1+B4",
          "G2+B3"
        ],
        "meaning": "The public list of all 12 lots, in unshuffled form",
        "observable": false
      },
      {
        "key": "current_lot",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "This round's lot; revealed privately to the active seat only",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round, 1 to 12",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that sells this round: ((round-1) mod 3) + 1",
        "observable": false
      },
      {
        "key": "auction_colour",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Colour of this round's auction card",
        "observable": false
      },
      {
        "key": "auction_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value of this round's auction card; the kept card's value is 5 minus this",
        "observable": false
      },
      {
        "key": "auction_recipient",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that received the auction card this round, as recorded in the log",
        "observable": true
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the winning bidder this round, or 0 if the bids tied",
        "observable": false
      },
      {
        "key": "worth_red",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Public worth of Red, kept between 1 and 5",
        "observable": true
      },
      {
        "key": "worth_blue",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Public worth of Blue, kept between 1 and 5",
        "observable": true
      },
      {
        "key": "worth_green",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Public worth of Green, kept between 1 and 5",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat the 3 players as seats 1, 2 and 3.",
    "Each player gets gold = 12 and red = blue = green = 0.",
    "Set worth_red = worth_blue = worth_green = 3.",
    "Shuffle the 12 lots into the hidden table list `lots` with a seeded random order. The public `lot_list` shows all 12 lots, unordered.",
    "Set round = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Set active_seat = ((round - 1) mod 3) + 1. Set current_lot = lots[round]. Reset every player's bid to 0, and reset winner_seat and auction_recipient to 0."
    },
    {
      "action": "ask",
      "who": "the active seat (active_seat)",
      "answer": "one of the two cards of current_lot, shown only to this seat (e.g. 'R2' or 'G3')",
      "effect": "Add the kept card's value to the active seat's holding in its colour (red, blue or green). Set auction_colour and auction_value to the other card. No other player sees current_lot or the kept card."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Round {round}: seat {active_seat} auctions {auction_colour} {auction_value}.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "Set each player's message, then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all are in. Messages are not binding."
    },
    {
      "action": "poll",
      "who": "the two seats other than active_seat",
      "answer": "a whole number from 0 to that bidder's gold",
      "effect": "Set each bidder's bid. No bid is seen until both are in."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Announce both bids. If one bid is strictly higher, set winner_seat to that bidder: the winner's gold falls by the bid, the active seat's gold rises by the bid, the auction_value is added to the winner's holding in auction_colour, and auction_recipient = winner_seat. If the bids are equal (including 0 and 0), nobody pays: the auction_value is added to the active seat's holding in auction_colour, and auction_recipient = active_seat."
    },
    {
      "action": "ask",
      "who": "seat winner_seat, when winner_seat > 0",
      "answer": "one of: no change, Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1",
      "effect": "Adjust the chosen worth by 1, but only if the result stays within 1..5; otherwise nothing changes."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {auction_recipient} received the auction card. Worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}.'"
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Increase round by 1."
    },
    {
      "action": "update",
      "who": "engine, when round > 12",
      "answer": null,
      "effect": "For each colour C with worth W: let M = the highest holding in C, and N = the number of players holding M. If M = 0, nobody scores C. If N = 1, that player gains W colour VP. If N >= 2, each tied player gains floor(W / 2). Then set each player's vp = colour VP + floor(gold / 4), and reveal all holdings."
    },
    {
      "action": "check",
      "who": "engine",
      "answer": null,
      "effect": "End the game if round > 12; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round > 12",
    "rank_by": "you.vp * 1000 + you.gold",
    "decided_by": "Most VP wins (colour majorities at final worth, plus 1 VP per full 4 gold). A tie on VP is broken by more remaining gold. Players still tied share the win, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At the start, each player has 12 gold and 0 Red, 0 Blue and 0 Green, and each colour's worth is 3."
    },
    {
      "id": "R2",
      "text": "Gold and worths are public; each player's holdings are visible only to that player until the end of the game."
    },
    {
      "id": "R3",
      "text": "The 12 lots (R1+B4, R2+B3, B1+R4, B2+R3, R1+G4, R2+G3, G1+R4, G2+R3, B1+G4, B2+G3, G1+B4, G2+B3) are put in a hidden random order, and round k uses the k-th lot, so each lot is used exactly once."
    },
    {
      "id": "R4",
      "text": "In round k, the active seat is ((k-1) mod 3) + 1, so seats 1, 2 and 3 are each active 4 times in 12 rounds."
    },
    {
      "id": "R5",
      "text": "When a round begins, only the active seat is shown the lot; no other player ever sees it."
    },
    {
      "id": "R6",
      "text": "When the active seat keeps a card, that card's value is added to the active seat's holding in its colour, e.g. keeping G3 adds 3 to green."
    },
    {
      "id": "R7",
      "text": "When a card is kept, the other card's colour and value are announced to everyone as the auction card."
    },
    {
      "id": "R8",
      "text": "Each round, all three players submit one short text message simultaneously, and all messages are then shown to everyone."
    },
    {
      "id": "R9",
      "text": "The two non-active seats bid simultaneously, each a whole number from 0 up to their current gold."
    },
    {
      "id": "R10",
      "text": "When one bid is strictly higher, that bidder pays the bid to the active seat and adds the auction card's value to their holding in its colour; e.g. bids 5 and 3 for B4 move 5 gold from the winner to the active seat and add 4 to the winner's blue."
    },
    {
      "id": "R11",
      "text": "When the bids are equal (including 0 and 0), no gold moves, and the active seat adds the auction card's value to their own holding in its colour."
    },
    {
      "id": "R12",
      "text": "Each round, auction_recipient records the seat that received the auction card."
    },
    {
      "id": "R13",
      "text": "When a bidder wins, that bidder may raise or lower one colour's worth by 1, or change nothing."
    },
    {
      "id": "R14",
      "text": "A worth change that would take a worth below 1 or above 5 has no effect; e.g. Red at 5 with Red +1 stays 5."
    },
    {
      "id": "R15",
      "text": "When the bids tie, no worth shift happens."
    },
    {
      "id": "R16",
      "text": "After each round's resolution, the three worths are announced."
    },
    {
      "id": "R17",
      "text": "The game ends after round 12."
    },
    {
      "id": "R18",
      "text": "At the end, the single highest holder of a colour scores VP equal to that colour's worth; e.g. a sole Red leader with Red worth 4 gains 4 VP."
    },
    {
      "id": "R19",
      "text": "At the end, when two or three players tie for highest in a colour, each scores floor(worth / 2); e.g. worth 5 gives each tied player 2 VP."
    },
    {
      "id": "R20",
      "text": "At the end, when all players hold 0 in a colour, nobody scores that colour."
    },
    {
      "id": "R21",
      "text": "At the end, each player scores floor(gold / 4) VP; e.g. 15 gold gives 3 VP."
    },
    {
      "id": "R22",
      "text": "The player with the most VP wins; a VP tie is broken by more gold; players still tied share the result as a draw."
    }
  ],
  "offers": [
    {
      "question": "Keep a card",
      "who": "the active seat only",
      "options": "exactly the two cards of this round's lot, e.g. for lot R2+G3: R2, G3"
    },
    {
      "question": "Talk message",
      "who": "all three seats",
      "options": "any short text"
    },
    {
      "question": "Bid",
      "who": "the two seats other than the active seat",
      "options": "any whole number from 0 to that seat's current gold; the active seat is not asked"
    },
    {
      "question": "Shift worth",
      "who": "the winning bidder only, and only when a bidder won",
      "options": "no change, Red +1, Red -1, Blue +1, Blue -1, Green +1, Green -1 (all always offered; a change past 1 or 5 has no effect); nobody is asked after a tie"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed 3: one seller and two rival bidders each round. The lot deduction and rotation (4 turns each) are built for 3 seats, so the minimum and maximum are both 3."
    },
    {
      "what": "Keep the simultaneous talk poll before bidding",
      "why": "The rules require it. Players disagree (the seller wants high bids, and bidders want cheap cards and to hide their colours), so bluffing about the kept card or about worth plans gives the others something to reason about."
    },
    {
      "what": "Ranking expression vp*1000 + gold",
      "why": "Total gold never exceeds 36, so a factor of 1000 puts VP first and gold as the tie-break. Remaining exact ties share the win, which is the engine's form of a draw."
    },
    {
      "what": "The shift question is always offered as all 7 options",
      "why": "The rules say a change past the limits simply has no effect, so the options do not need to depend on the current worths."
    },
    {
      "what": "A strategy exists",
      "why": "Thoughtful players track used lots to infer the seller's kept colour, bid by how much a card swings a majority, use worth shifts to raise colours they lead and sink rivals', and bluff in talk."
    }
  ],
  "simplifications": [
    {
      "what": "Bids are stored as a private attribute and announced in the resolve update",
      "why": "The engine's poll keeps answers hidden until all are in; the announcement then reveals both bids as the rules require."
    },
    {
      "what": "End scoring is a single update step that runs when round > 12, before the ending check",
      "why": "The engine's ending ranks by one expression, so the colour majorities are computed into vp first."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: gold, vp; table: auction_recipient, worth_red, worth_blue, worth_green.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Start: 12 gold each, worths 3, no VP yet", "rule": "R1", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"players": {"1": {"gold": 12, "vp": 0}, "2": {"gold": 12, "vp": 0}, "3": {"gold": 12, "vp": 0}},
              "game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3, "auction_recipient": 0}}},

  {"name": "Public gold and worths are at their starting values", "rule": "R2", "players": 3, "seed": 2, "rounds": 0,
   "expect": {"players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3}}},

  {"name": "The hidden lot order holds all 12 lots", "rule": "R3", "players": 3, "seed": 3, "rounds": 0,
   "expect": {"lens": {"game": {"lots": 12, "lot_list": 12}}}},

  {"name": "Round 2: seat 2 is active and seats 1 and 3 bid", "rule": "R4", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 2, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 2, "options_include": "R2"},
             {"seat": 1, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_recipient": 2},
              "players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "B3"}],
              "not_offered": [{"seat": 1, "option": "R2"}, {"seat": 3, "option": "R2"}, {"seat": 2, "option": 0}]}},

  {"name": "Only the active seat is offered the lot's cards", "rule": "R5", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "B3"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": "R2"}, {"seat": 1, "option": "B3"}],
              "not_offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "B3"}, {"seat": 3, "option": "R2"}, {"seat": 3, "option": "B3"}]}},

  {"name": "Kept G3 counts for the seller's green at the end", "rule": "R6", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5011, "2": 3012, "3": 6013},
              "players": {"1": {"gold": 11, "vp": 5}, "2": {"gold": 12, "vp": 3}, "3": {"gold": 13, "vp": 6}},
              "game": {"auction_recipient": 1}}},

  {"name": "Keeping B4 auctions R1, which goes to the winning bidder", "rule": "R7", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 3, "options_include": "B4"},
             {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5010, "2": 3012, "3": 6014},
              "players": {"1": {"gold": 10, "vp": 5}, "2": {"vp": 3}, "3": {"gold": 14, "vp": 6}},
              "game": {"auction_recipient": 1}}},

  {"name": "The talk poll does not stop the round from resolving", "rule": "R8", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_recipient": 1},
              "players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}}}},

  {"name": "A bid can go up to the bidder's gold but not above it", "rule": "R9", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"2": {"gold": 3}},
             "game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 15}, "2": {"gold": 0}, "3": {"gold": 12}},
              "game": {"auction_recipient": 2},
              "offered": [{"seat": 2, "option": 3}],
              "not_offered": [{"seat": 2, "option": 4}, {"seat": 1, "option": 0}]}},

  {"name": "Bids 5 and 3: the winner pays 5 to the seller", "rule": "R10", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 5},
             {"seat": 3, "options_include": 3}],
   "expect": {"players": {"1": {"gold": 17}, "2": {"gold": 7}, "3": {"gold": 12}},
              "game": {"auction_recipient": 2, "worth_red": 3, "worth_blue": 3, "worth_green": 3}}},

  {"name": "Equal bids: no gold moves and the seller takes the card", "rule": "R11", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 4},
             {"seat": 3, "options_include": 4}],
   "expect": {"players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "game": {"auction_recipient": 1}}},

  {"name": "auction_recipient records the winning bidder", "rule": "R12", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3"]}},
   "rules": [{"seat": 1, "options_include": "G2"},
             {"seat": 2, "options_include": 1},
             {"seat": 3, "options_include": 2}],
   "expect": {"players": {"1": {"gold": 14}, "2": {"gold": 12}, "3": {"gold": 10}},
              "game": {"auction_recipient": 3}}},

  {"name": "The winning bidder raises Red by 1", "rule": "R13", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": "Red +1"}],
   "expect": {"game": {"worth_red": 4, "worth_blue": 3, "worth_green": 3, "auction_recipient": 2},
              "offered": [{"seat": 2, "option": "Red -1"}, {"seat": 2, "option": "no change"}],
              "not_offered": [{"seat": 3, "option": "Red +1"}, {"seat": 1, "option": "Red +1"}]}},

  {"name": "Red at 5 with Red +1 stays at 5", "rule": "R14", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"worth_red": 5, "round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": "Red +1"}],
   "expect": {"game": {"worth_red": 5, "worth_blue": 3, "worth_green": 3}}},

  {"name": "Tied bids: nobody is asked to shift a worth", "rule": "R15", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3, "auction_recipient": 1},
              "not_offered": [{"seat": 1, "option": "Red +1"}, {"seat": 2, "option": "Red +1"}, {"seat": 3, "option": "Red +1"},
                              {"seat": 1, "option": "no change"}, {"seat": 2, "option": "no change"}, {"seat": 3, "option": "no change"}]}},

  {"name": "Worths after resolution reflect a Green -1 shift", "rule": "R16", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 1},
             {"seat": 3, "options_include": "Green -1"}],
   "expect": {"game": {"worth_red": 3, "worth_blue": 3, "worth_green": 2, "auction_recipient": 3},
              "players": {"1": {"gold": 13}, "3": {"gold": 11}}}},

  {"name": "Game ends after round 12 and is scored", "rule": "R17", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 3012, "2": 3012, "3": 9012},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "Sole Red leader at worth 4 gains 4 VP", "rule": "R18", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"red": 5}, "2": {"red": 2}},
             "game": {"worth_red": 4, "round": 12, "lots": ["G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3"]}},
   "rules": [{"seat": 3, "options_include": "B3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 7012, "2": 3012, "3": 9012},
              "players": {"1": {"vp": 7}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "Two tied Blue leaders at worth 5 score 2 each", "rule": "R19", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"blue": 4}, "2": {"blue": 4}},
             "game": {"worth_blue": 5, "round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5012, "2": 5012, "3": 9012},
              "players": {"1": {"vp": 5}, "2": {"vp": 5}, "3": {"vp": 9}}}},

  {"name": "A colour nobody holds scores nothing", "rule": "R20", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "R2"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "15 gold gives 3 VP, 7 gold gives 1 VP", "rule": "R21", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15}, "2": {"gold": 7}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 3015, "2": 1007, "3": 9012},
              "players": {"1": {"vp": 3, "gold": 15}, "2": {"vp": 1, "gold": 7}, "3": {"vp": 9}}}},

  {"name": "A VP tie is broken by more gold", "rule": "R22", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15, "red": 5}, "2": {"gold": 13, "green": 5}, "3": {"gold": 0}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 6015, "2": 6013, "3": 0},
              "players": {"1": {"vp": 6}, "2": {"vp": 6}, "3": {"vp": 0}}}},

  {"name": "Same VP and same gold share the win", "rule": "R22", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15, "red": 5}, "2": {"gold": 15, "green": 5}, "3": {"gold": 0}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 6015, "2": 6015, "3": 0},
              "players": {"1": {"vp": 6}, "2": {"vp": 6}, "3": {"vp": 0}}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Start: 12 gold each and worths 3; a 0-0 tie in round 1 changes nothing public", "rule": "R1", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 12, "vp": 0}, "2": {"gold": 12, "vp": 0}, "3": {"gold": 12, "vp": 0}},
              "game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3, "auction_recipient": 1}}},

  {"name": "Public gold and worths track a won auction", "rule": "R2", "players": 3, "seed": 2, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 0},
             {"seat": 2, "options_include": "no change"}],
   "expect": {"players": {"1": {"gold": 14}, "2": {"gold": 10}, "3": {"gold": 12}},
              "game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3, "auction_recipient": 2}}},

  {"name": "The public lot list holds all 12 lots whatever the shuffle", "rule": "R3", "players": 3, "seed": 3, "rounds": 1, "default": "first",
   "rules": [{"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"lens": {"game": {"lot_list": 12}},
              "players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "game": {"auction_recipient": 1}}},

  {"name": "Round 2: seat 2 is active and seats 1 and 3 bid", "rule": "R4", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 2, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 2, "options_include": "R2"},
             {"seat": 1, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_recipient": 2},
              "players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "B3"}],
              "not_offered": [{"seat": 1, "option": "R2"}, {"seat": 3, "option": "R2"}, {"seat": 2, "option": 0}]}},

  {"name": "Only the active seat is offered the lot's cards", "rule": "R5", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "B3"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": "R2"}, {"seat": 1, "option": "B3"}],
              "not_offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "B3"}, {"seat": 3, "option": "R2"}, {"seat": 3, "option": "B3"}]}},

  {"name": "Kept G3 counts for the seller's green at the end", "rule": "R6", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5011, "2": 3012, "3": 6013},
              "players": {"1": {"gold": 11, "vp": 5}, "2": {"gold": 12, "vp": 3}, "3": {"gold": 13, "vp": 6}},
              "game": {"auction_recipient": 1}}},

  {"name": "Keeping B4 auctions R1, which goes to the winning bidder", "rule": "R7", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 3, "options_include": "B4"},
             {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5010, "2": 3012, "3": 6014},
              "players": {"1": {"gold": 10, "vp": 5}, "2": {"vp": 3}, "3": {"gold": 14, "vp": 6}},
              "game": {"auction_recipient": 1}}},

  {"name": "The talk poll does not stop the round from resolving", "rule": "R8", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auction_recipient": 1},
              "players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}}}},

  {"name": "A bid can go up to the bidder's gold but not above it", "rule": "R9", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"2": {"gold": 3}},
             "game": {"round": 1, "lots": ["R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3","R2+B3"]}},
   "rules": [{"seat": 1, "options_include": "R2"},
             {"seat": 2, "options_include": 3},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 15}, "2": {"gold": 0}, "3": {"gold": 12}},
              "game": {"auction_recipient": 2},
              "offered": [{"seat": 2, "option": 3}],
              "not_offered": [{"seat": 2, "option": 4}, {"seat": 1, "option": 0}]}},

  {"name": "Bids 5 and 3: the winner pays 5 to the seller", "rule": "R10", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 5},
             {"seat": 3, "options_include": 3}],
   "expect": {"players": {"1": {"gold": 17}, "2": {"gold": 7}, "3": {"gold": 12}},
              "game": {"auction_recipient": 2, "worth_red": 3, "worth_blue": 3, "worth_green": 3}}},

  {"name": "Equal bids: no gold moves and the seller takes the card", "rule": "R11", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 4},
             {"seat": 3, "options_include": 4}],
   "expect": {"players": {"1": {"gold": 12}, "2": {"gold": 12}, "3": {"gold": 12}},
              "game": {"auction_recipient": 1}}},

  {"name": "auction_recipient records the winning bidder", "rule": "R12", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3"]}},
   "rules": [{"seat": 1, "options_include": "G2"},
             {"seat": 2, "options_include": 1},
             {"seat": 3, "options_include": 2}],
   "expect": {"players": {"1": {"gold": 14}, "2": {"gold": 12}, "3": {"gold": 10}},
              "game": {"auction_recipient": 3}}},

  {"name": "The winning bidder raises Red by 1", "rule": "R13", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": "Red +1"}],
   "expect": {"game": {"worth_red": 4, "worth_blue": 3, "worth_green": 3, "auction_recipient": 2},
              "offered": [{"seat": 2, "option": "Red -1"}, {"seat": 2, "option": "no change"}],
              "not_offered": [{"seat": 3, "option": "Red +1"}, {"seat": 1, "option": "Red +1"}]}},

  {"name": "Red at 5 with Red +1 stays at 5", "rule": "R14", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"worth_red": 5, "round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": "Red +1"}],
   "expect": {"game": {"worth_red": 5, "worth_blue": 3, "worth_green": 3}}},

  {"name": "Tied bids: nobody is asked to shift a worth", "rule": "R15", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}],
   "expect": {"game": {"worth_red": 3, "worth_blue": 3, "worth_green": 3, "auction_recipient": 1},
              "not_offered": [{"seat": 1, "option": "Red +1"}, {"seat": 2, "option": "Red +1"}, {"seat": 3, "option": "Red +1"},
                              {"seat": 1, "option": "no change"}, {"seat": 2, "option": "no change"}, {"seat": 3, "option": "no change"}]}},

  {"name": "Worths after resolution reflect a Green -1 shift", "rule": "R16", "players": 3, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1, "lots": ["R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4","R1+B4"]}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 1},
             {"seat": 3, "options_include": "Green -1"}],
   "expect": {"game": {"worth_red": 3, "worth_blue": 3, "worth_green": 2, "auction_recipient": 3},
              "players": {"1": {"gold": 13}, "3": {"gold": 11}}}},

  {"name": "Game ends after round 12 and is scored", "rule": "R17", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 3012, "2": 3012, "3": 9012},
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "Sole Red leader at worth 4 gains 4 VP", "rule": "R18", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"red": 5}, "2": {"red": 2}},
             "game": {"worth_red": 4, "round": 12, "lots": ["G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3","G2+B3"]}},
   "rules": [{"seat": 3, "options_include": "B3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 7012, "2": 3012, "3": 9012},
              "players": {"1": {"vp": 7}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "Two tied Blue leaders at worth 5 score 2 each", "rule": "R19", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"blue": 4}, "2": {"blue": 4}},
             "game": {"worth_blue": 5, "round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 5012, "2": 5012, "3": 9012},
              "players": {"1": {"vp": 5}, "2": {"vp": 5}, "3": {"vp": 9}}}},

  {"name": "A colour nobody holds scores nothing", "rule": "R20", "players": 3, "seed": 1, "default": "decline",
   "given": {"game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "R2"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "players": {"1": {"vp": 3}, "2": {"vp": 3}, "3": {"vp": 9}}}},

  {"name": "15 gold gives 3 VP, 7 gold gives 1 VP", "rule": "R21", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15}, "2": {"gold": 7}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3,
              "standings": {"1": 3015, "2": 1007, "3": 9012},
              "players": {"1": {"vp": 3, "gold": 15}, "2": {"vp": 1, "gold": 7}, "3": {"vp": 9}}}},

  {"name": "A VP tie is broken by more gold", "rule": "R22", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15, "red": 5}, "2": {"gold": 13, "green": 5}, "3": {"gold": 0}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": 1,
              "standings": {"1": 6015, "2": 6013, "3": 0},
              "players": {"1": {"vp": 6}, "2": {"vp": 6}, "3": {"vp": 0}}}},

  {"name": "Same VP and same gold share the win", "rule": "R22", "players": 3, "seed": 1, "default": "decline",
   "given": {"players": {"1": {"gold": 15, "red": 5}, "2": {"gold": 15, "green": 5}, "3": {"gold": 0}},
             "game": {"round": 12, "lots": ["R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3","R2+G3"]}},
   "rules": [{"seat": 3, "options_include": "G3"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 6015, "2": 6015, "3": 0},
              "players": {"1": {"vp": 6}, "2": {"vp": 6}, "3": {"vp": 0}}}}
]
```
````
