# 08 scenarios

- time: 2026-10-28T05:07:31+00:00 (107.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 6c2d035b811044bc, reply sha256 a98b6da48b2b3cd4

## Sent

````
SPEC:
{
  "name": "Masterpiece: Secret Collectors",
  "summary": "Four collectors take turns selling paintings in sealed-bid auctions against secret reserves, each guarding private knowledge of painting values and a secret theme style worth a 400 bonus per matching painting.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "starting_cash": 1500,
    "num_styles": 4,
    "paintings_per_player": 4,
    "value_low": 0,
    "value_mid_low": 300,
    "value_mid_high": 600,
    "value_high": 1200,
    "rounds": 12,
    "sales_per_player": 3,
    "bid_step": 50,
    "reserve_max": 2000,
    "bid_min": 0,
    "reserve_min": 0,
    "unsold_fee": 50,
    "fee_trigger_min_bid": 50,
    "theme_bonus": 400
  },
  "attributes": {
    "player": [
      {
        "key": "cash",
        "type": "number",
        "visible": "public",
        "initial": 1500,
        "meaning": "Cash in thousands of dollars. Always public.",
        "observable": true
      },
      {
        "key": "paintings",
        "type": "list",
        "visible": "public",
        "initial": "four painting names, one of each style, e.g. ['P2-Red','P2-Blue','P2-Gold','P2-Green']",
        "meaning": "Names of the paintings this player currently owns. Ownership and style are public; a name encodes its style.",
        "observable": true
      },
      {
        "key": "theme",
        "type": "text",
        "visible": "ally",
        "initial": "a random style, different for every player",
        "meaning": "Secret collector theme style. Each owned painting of this style is worth +400 at scoring. Revealed at the end.",
        "observable": false
      },
      {
        "key": "known_values",
        "type": "list",
        "visible": "ally",
        "initial": "'name=value' entries for the player's own four paintings",
        "meaning": "Painting values this player has learned: the values of every painting they have ever owned.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sealed bid this round (non-sellers). Published after resolution.",
        "observable": false
      },
      {
        "key": "reserve",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Secret reserve this round (seller only). Never published.",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message, shown to all after everyone has written.",
        "observable": false
      },
      {
        "key": "tie_priority",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch tie-break key this round: 3 for the seller's left, 2 for the next seat, 1 for the seat after that, 0 for the seller.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final score = cash + total value of owned paintings + 400 for each owned painting of the player's theme. Computed at game end.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number, 1 to 12.",
        "observable": true
      },
      {
        "key": "seller",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this round's seller: ((round-1) mod 4) + 1.",
        "observable": true
      },
      {
        "key": "lot",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Name of the painting being auctioned this round.",
        "observable": true
      },
      {
        "key": "lot_style",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Style of the current lot.",
        "observable": false
      },
      {
        "key": "painting_values",
        "type": "list",
        "visible": "none",
        "initial": "16 'name=value' entries dealt from a shuffled Latin square of {0,300,600,1200}",
        "meaning": "True value of every painting. Hidden from all; each player learns only the values of paintings they have owned. Revealed at the end.",
        "observable": false
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest bid B this round.",
        "observable": true
      },
      {
        "key": "high_bidder",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the winning bidder after the tie-break.",
        "observable": true
      },
      {
        "key": "sold",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this round's lot was sold.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat players 1 to 4 in a fixed circle; the left of seat p is seat p+1, and the left of seat 4 is seat 1.",
    "Every player's cash is set to 1500.",
    "Each player p receives four paintings named 'Pp-Red', 'Pp-Blue', 'Pp-Gold' and 'Pp-Green' in their paintings list.",
    "The four styles Red, Blue, Gold and Green are dealt at random as secret themes, one different style per player, each stored in that player's theme (ally).",
    "Painting values are built from the pattern value(p, s) = [0,300,600,1200][(p+s) mod 4], with players and styles indexed 0 to 3. Rows (players), columns (styles) and the value labels are then shuffled at random, so each player holds one painting each worth 0, 300, 600 and 1200, and each style has one painting of each value. The result is stored in painting_values (hidden).",
    "Each player's known_values is set to the values of their own four paintings, and the engine tells each player those values privately.",
    "Everyone is told that the four themes are all different."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; seller = ((round-1) mod 4) + 1; sold = false; high_bid = 0; high_bidder = 0; lot = ''; each player's bid = 0 and reserve = 0; tie_priority = 3 for seat ((seller) mod 4)+1, 2 for seat ((seller+1) mod 4)+1, 1 for seat ((seller+2) mod 4)+1, 0 for the seller. Announces the seller."
    },
    {
      "action": "ask",
      "who": "the seat to the seller's left: ((seller) mod 4) + 1",
      "answer": "one painting name from the seller's current paintings list",
      "effect": "when the seller's paintings list is not empty: lot = chosen name; lot_style = its style. The lot and its style are announced to all."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "when the seller's paintings list is not empty: each player's message = their text; afterwards broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk is not binding."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "non-sellers: a whole number from 0 to their cash (bid); seller: a whole number from 0 to 2000 (reserve)",
      "effect": "when the seller's paintings list is not empty: each value is rounded down to a multiple of 50. Each non-seller's bid is set to their number; the seller's reserve is set to theirs. Nobody sees any answer until all are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when the seller's paintings list is not empty: high_bid = max over non-sellers of bid; high_bidder = the non-seller with the largest (bid * 10 + tie_priority)."
    },
    {
      "action": "update",
      "who": "seller and high bidder",
      "answer": null,
      "effect": "when the seller's paintings list is not empty: if high_bid > seller.reserve then sold = true; high_bidder.cash -= high_bid; seller.cash += high_bid; remove lot from seller.paintings; append lot to high_bidder.paintings; append the lot's 'name=value' entry from painting_values to high_bidder.known_values and tell the high bidder privately. Otherwise sold = false, and if high_bid >= 50 then seller.cash -= min(50, seller.cash), and that money leaves the game."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when the seller's paintings list is not empty: publish every non-seller's bid, whether the lot was sold or kept, the money moved (price or fee) and every player's new cash. The reserve and the painting's value are not published."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round == 12: reveal painting_values and every theme to all; each player's score = cash + sum of values of the paintings in their paintings list + 400 * (number of paintings in their list whose style equals their theme)."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round == 12, otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.score * 100000 + you.cash",
    "decided_by": "Each player's standing is their score (cash + value of owned paintings + 400 per owned painting of their theme), with cash breaking ties. The highest wins; players still level on both score and cash share the win, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has cash 1500 and owns exactly 4 paintings, one each of Red, Blue, Gold and Green."
    },
    {
      "id": "R2",
      "text": "When themes are dealt, then each of the 4 players has a different theme style, and each is told only their own."
    },
    {
      "id": "R3",
      "text": "When values are dealt, then each player holds one painting each worth 0, 300, 600 and 1200, and each style has exactly one painting of each of those values."
    },
    {
      "id": "R4",
      "text": "When values are dealt, then each player learns privately the values of their own 4 paintings and no other values."
    },
    {
      "id": "R5",
      "text": "When round r begins, then the seller is seat ((r-1) mod 4)+1, so seats 1, 2, 3, 4 sell in rounds 1, 2, 3, 4 and again in rounds 5 to 8 and 9 to 12."
    },
    {
      "id": "R6",
      "text": "When the seller owns no paintings, then the lot choice, talk, bids and resolution are skipped that round."
    },
    {
      "id": "R7",
      "text": "When a lot is chosen, then the chooser is the seat to the seller's left (seat seller mod 4 + 1), the lot is one of the seller's current paintings, and it is announced with its style."
    },
    {
      "id": "R8",
      "text": "When talk happens, then every player, seller included, submits one message at the same time, and all messages are shown to everyone afterwards."
    },
    {
      "id": "R9",
      "text": "When bids are made, then each non-seller bids a multiple of 50 from 0 to their current cash, and the seller sets a secret reserve that is a multiple of 50 from 0 to 2000, all at the same time."
    },
    {
      "id": "R10",
      "text": "When two or more bidders tie for the highest bid B, then the winner is the tied bidder nearest the seller going clockwise, the seller's left first."
    },
    {
      "id": "R11",
      "text": "When B > reserve, then the high bidder pays B to the seller, the lot moves to the high bidder's paintings, and the high bidder privately learns its value."
    },
    {
      "id": "R12",
      "text": "When B <= reserve and B >= 50, then the seller keeps the lot and pays a fee of 50 (or all their cash if under 50), which leaves the game."
    },
    {
      "id": "R13",
      "text": "When B <= reserve and B is 0, then the seller keeps the lot and pays no fee."
    },
    {
      "id": "R14",
      "text": "When an auction resolves, then all bids, sold or kept, the money moved and every new cash total are published, but not the reserve or the painting's value."
    },
    {
      "id": "R15",
      "text": "When a bought painting's new owner is the seller in a later round, then that painting may be chosen as the lot."
    },
    {
      "id": "R16",
      "text": "When round 12 ends, then the game ends, and all values and themes are revealed."
    },
    {
      "id": "R17",
      "text": "When scoring, then score = cash + the total value of owned paintings + 400 for each owned painting whose style equals the owner's theme."
    },
    {
      "id": "R18",
      "text": "When scores tie at the top, then the tied player with more cash wins, and players tied on both share the win (the draw)."
    }
  ],
  "offers": [
    {
      "question": "Lot choice",
      "who": "the seat to the seller's left",
      "options": "each painting name currently in the seller's paintings list; the step is not asked if that list is empty"
    },
    {
      "question": "Talk",
      "who": "all four seats",
      "options": "one short free-text message"
    },
    {
      "question": "Sealed bid",
      "who": "each non-seller",
      "options": "a whole number from 0 to their current cash, rounded down to a multiple of 50"
    },
    {
      "question": "Secret reserve",
      "who": "the seller",
      "options": "a whole number from 0 to 2000, rounded down to a multiple of 50"
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players (min 4, max 4, suggested 4)",
      "why": "The designer chose 4. The structure needs it: 4 styles, 4 distinct themes, a 4x4 Latin square of values and 3 sales per seat over 12 rounds. Fewer seats break the value deal, and more have no theme or values to receive."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The source requires simultaneous unbinding talk. It earns its place because interests conflict: sellers want to talk up lots, and bidders want to bluff their themes and known values."
    },
    {
      "what": "Tie-break encoded as bid*10 + tie_priority",
      "why": "Bids are multiples of 50, so adding a priority from 0 to 3 never changes the order of different bids. It ranks the seller's left first, as the rules say."
    },
    {
      "what": "Ranking expression score*100000 + cash",
      "why": "Scores stay well under 100000, so cash only breaks ties in score. Players tied on both share the win, which stands for the source's draw."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player infers others' themes from their bids and talk, uses known values to bid on undervalued lots, sets reserves to protect theme paintings, and bluffs in talk. A thoughtless one bids on face value."
    }
  ],
  "simplifications": [
    {
      "what": "Bids and reserves are entered as whole numbers and rounded down to a multiple of 50",
      "why": "The engine takes a whole number in a range; rounding enforces the multiple-of-50 rule."
    },
    {
      "what": "The skip when the seller has no paintings is done with a 'when' condition on each step",
      "why": "The step list is flat; per-step conditions give the same effect without choosing a block of steps."
    },
    {
      "what": "Painting values are stored as 'name=value' text entries in lists",
      "why": "The engine has lists, not maps; each player's known_values plays the role of 'values known to past owners'."
    },
    {
      "what": "Bids and the reserve are gathered in one simultaneous poll with different ranges per seat",
      "why": "The source makes them simultaneous; one poll keeps every answer hidden until all are in."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: cash, paintings, score; table: round, seller, lot, high_bid, high_bidder, sold.
````

## Reply

````
```json
[
  {"name": "Start: every seat has 1500 cash and its four paintings, one of each style", "rule": "R1", "players": 4, "seed": 1, "rounds": 0, "default": "decline",
   "rules": [],
   "expect": {"players": {"1": {"cash": 1500, "paintings": ["P1-Red", "P1-Blue", "P1-Gold", "P1-Green"]},
                          "2": {"cash": 1500, "paintings": ["P2-Red", "P2-Blue", "P2-Gold", "P2-Green"]},
                          "3": {"cash": 1500, "paintings": ["P3-Red", "P3-Blue", "P3-Gold", "P3-Green"]},
                          "4": {"cash": 1500, "paintings": ["P4-Red", "P4-Blue", "P4-Gold", "P4-Green"]}},
              "lens": {"players": {"1": {"paintings": 4}, "2": {"paintings": 4}, "3": {"paintings": 4}, "4": {"paintings": 4}}}}},

  {"name": "Dealt themes are real styles: with fixed values, each seat owning its own four paintings scores exactly one 400 bonus (themes random)", "rule": "R2", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11, "painting_values": ["P1-Red=0", "P1-Blue=300", "P1-Gold=600", "P1-Green=1200", "P2-Red=300", "P2-Blue=600", "P2-Gold=1200", "P2-Green=0", "P3-Red=600", "P3-Blue=1200", "P3-Gold=0", "P3-Green=300", "P4-Red=1200", "P4-Blue=0", "P4-Gold=300", "P4-Green=600"]}},
   "rules": [{"seat": 1, "options_include": "P4-Red"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0}],
   "expect": {"winner": [1, 2, 3, 4],
              "players": {"1": {"score": 4000}, "2": {"score": 4000}, "3": {"score": 4000}, "4": {"score": 4000}}}},

  {"name": "Values dealt: 16 painting values exist", "rule": "R3", "players": 4, "seed": 1, "rounds": 0, "default": "decline",
   "rules": [],
   "expect": {"lens": {"game": {"painting_values": 16}}}},

  {"name": "Each seat starts knowing exactly its own 4 values", "rule": "R4", "players": 4, "seed": 1, "rounds": 0, "default": "decline",
   "rules": [],
   "expect": {"lens": {"players": {"1": {"known_values": 4}, "2": {"known_values": 4}, "3": {"known_values": 4}, "4": {"known_values": 4}}}}},

  {"name": "Round 1 seller is seat 1", "rule": "R5", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Red"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0}],
   "expect": {"game": {"round": 1, "seller": 1}}},

  {"name": "Round 6 seller is seat 2", "rule": "R5", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 3, "options_include": "P2-Red"},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"game": {"round": 6, "seller": 2, "sold": false},
              "players": {"1": {"cash": 1500}, "2": {"cash": 1500}, "3": {"cash": 1500}, "4": {"cash": 1500}}}},

  {"name": "Seller with no paintings: no lot, no bids, nothing changes", "rule": "R6", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"paintings": []}}},
   "rules": [],
   "expect": {"game": {"round": 1, "seller": 1, "sold": false, "high_bid": 0},
              "players": {"1": {"cash": 1500, "paintings": []}, "2": {"cash": 1500}, "3": {"cash": 1500}, "4": {"cash": 1500}},
              "not_offered": [{"seat": 1, "option": 0}, {"seat": 2, "option": 0}, {"seat": 3, "option": 0}, {"seat": 4, "option": 0}]}},

  {"name": "Seat to the seller's left chooses the lot from the seller's paintings", "rule": "R7", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Gold"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0}],
   "expect": {"game": {"lot": "P1-Gold", "sold": false},
              "offered": [{"seat": 2, "option": "P1-Gold"}],
              "not_offered": [{"seat": 1, "option": "P1-Gold"}, {"seat": 3, "option": "P1-Gold"}, {"seat": 4, "option": "P1-Gold"}, {"seat": 2, "option": "P2-Red"}]}},

  {"name": "A round with talk proceeds to the auction normally", "rule": "R8", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Blue"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0}],
   "expect": {"game": {"round": 1, "lot": "P1-Blue", "sold": false}}},

  {"name": "Bids range to own cash, reserve to 2000, rounded down to 50", "rule": "R9", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"3": {"cash": 400}}},
   "rules": [{"seat": 2, "options_include": "P1-Red"},
             {"seat": 2, "options_include": 120},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0}],
   "expect": {"game": {"high_bid": 100, "high_bidder": 2, "sold": true},
              "players": {"1": {"cash": 1600}, "2": {"cash": 1400}, "3": {"cash": 400}, "4": {"cash": 1500}},
              "offered": [{"seat": 3, "option": 400}, {"seat": 1, "option": 2000}, {"seat": 2, "option": 1500}],
              "not_offered": [{"seat": 3, "option": 450}, {"seat": 1, "option": 2050}, {"seat": 2, "option": 1550}]}},

  {"name": "Tie between seats 4 and 1 with seat 2 selling: seat 4 is nearer clockwise and wins", "rule": "R10", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1}},
   "rules": [{"seat": 3, "options_include": "P2-Blue"},
             {"seat": 3, "options_include": 100},
             {"seat": 4, "options_include": 300},
             {"seat": 1, "options_include": 300},
             {"seat": 2, "options_include": 0}],
   "expect": {"game": {"seller": 2, "high_bid": 300, "high_bidder": 4, "sold": true},
              "players": {"1": {"cash": 1500}, "2": {"cash": 1800, "paintings": ["P2-Red", "P2-Gold", "P2-Green"]}, "3": {"cash": 1500},
                          "4": {"cash": 1200, "paintings": ["P4-Red", "P4-Blue", "P4-Gold", "P4-Green", "P2-Blue"]}}}},

  {"name": "Bid above reserve: buyer pays seller, gets the painting and learns its value", "rule": "R11", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Green"},
             {"seat": 2, "options_include": 500},
             {"seat": 3, "options_include": 400},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 450}],
   "expect": {"game": {"high_bid": 500, "high_bidder": 2, "sold": true, "lot": "P1-Green"},
              "players": {"1": {"cash": 2000, "paintings": ["P1-Red", "P1-Blue", "P1-Gold"]},
                          "2": {"cash": 1000, "paintings": ["P2-Red", "P2-Blue", "P2-Gold", "P2-Green", "P1-Green"]},
                          "3": {"cash": 1500}, "4": {"cash": 1500}},
              "lens": {"players": {"2": {"known_values": 5}, "1": {"paintings": 3}}}}},

  {"name": "Bid equal to reserve: lot kept, seller pays 50 fee", "rule": "R12", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Red"},
             {"seat": 2, "options_include": 500},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 50},
             {"seat": 1, "options_include": 500}],
   "expect": {"game": {"high_bid": 500, "sold": false},
              "players": {"1": {"cash": 1450, "paintings": ["P1-Red", "P1-Blue", "P1-Gold", "P1-Green"]}, "2": {"cash": 1500}, "3": {"cash": 1500}, "4": {"cash": 1500}}}},

  {"name": "Unsold with seller holding only 30: fee takes all 30", "rule": "R12", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"cash": 30}}},
   "rules": [{"seat": 2, "options_include": "P1-Red"},
             {"seat": 2, "options_include": 50},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 2000}],
   "expect": {"game": {"high_bid": 50, "sold": false},
              "players": {"1": {"cash": 0}, "2": {"cash": 1500}, "3": {"cash": 1500}, "4": {"cash": 1500}}}},

  {"name": "All bids 0: lot kept, no fee", "rule": "R13", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Red"},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0}],
   "expect": {"game": {"high_bid": 0, "sold": false},
              "players": {"1": {"cash": 1500, "paintings": ["P1-Red", "P1-Blue", "P1-Gold", "P1-Green"]}, "2": {"cash": 1500}, "3": {"cash": 1500}, "4": {"cash": 1500}}}},

  {"name": "Resolved auction publishes high bid, winner and new cash totals", "rule": "R14", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "P1-Gold"},
             {"seat": 2, "options_include": 250},
             {"seat": 3, "options_include": 700},
             {"seat": 4, "options_include": 650},
             {"seat": 1, "options_include": 300}],
   "expect": {"game": {"high_bid": 700, "high_bidder": 3, "sold": true},
              "players": {"1": {"cash": 2200}, "2": {"cash": 1500}, "3": {"cash": 800}, "4": {"cash": 1500}}}},

  {"name": "A bought painting can be the lot when its new owner sells", "rule": "R15", "players": 4, "seed": 1, "rounds": 1, "default": "decline",
   "given": {"game": {"round": 1},
             "players": {"1": {"paintings": ["P1-Blue", "P1-Gold", "P1-Green"]},
                         "2": {"paintings": ["P2-Red", "P2-Blue", "P2-Gold", "P2-Green", "P1-Red"]}}},
   "rules": [{"seat": 3, "options_include": "P1-Red"},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}],
   "expect": {"game": {"seller": 2, "lot": "P1-Red", "sold": false},
              "offered": [{"seat": 3, "option": "P1-Red"}]}},

  {"name": "Game ends after round 12; untraded seats all score 1500+2100+400 (values and themes random)", "rule": "R16", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}},
   "rules": [{"seat": 1, "options_include": "P4-Gold"},
             {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0},
             {"seat": 4, "options_include": 0}],
   "expect": {"winner": [1, 2, 3, 4],
              "game": {"round": 12, "seller": 4},
              "players": {"1": {"score": 4000}, "2": {"score": 4000}, "3": {"score": 4000}, "4": {"score": 4000}}}},

  {"name": "Scoring: cash + painting values + 400 per theme painting", "rule": "R17", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11, "painting_values": ["P1-Red=0", "P1-Blue=300", "P1-Gold=600", "P1-Green=1200", "P2-Red=300", "P2-Blue=600", "P2-Gold=1200", "P2-Green=0", "P3-Red=600", "P3-Blue=1200", "P3-Gold=0", "P3-Green=300", "P4-Red=1200", "P4-Blue=0", "P4-Gold=300", "P4-Green=600"]},
             "players": {"1": {"cash": 1000, "theme": "Red", "paintings": ["P1-Red", "P2-Red", "P4-Red", "P1-Blue"]},
                         "2": {"cash": 1500, "theme": "Blue", "paintings": ["P2-Blue", "P2-Gold", "P2-Green"]},
                         "3": {"cash": 2000, "theme": "Gold", "paintings": ["P3-Red", "P3-Blue", "P3-Gold", "P3-Green", "P1-Gold", "P1-Green"]},
                         "4": {"cash": 1500, "theme": "Green", "paintings": []}}},
   "rules": [],
   "expect": {"winner": 3,
              "standings": {"1": 400001000, "2": 370001500, "3": 670002000, "4": 150001500},
              "players": {"1": {"score": 4000}, "2": {"score": 3700}, "3": {"score": 6700}, "4": {"score": 1500}}}},

  {"name": "Tied top score: more cash wins", "rule": "R18", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11, "painting_values": ["P1-Red=0", "P1-Blue=300", "P1-Gold=600", "P1-Green=1200", "P2-Red=300", "P2-Blue=600", "P2-Gold=1200", "P2-Green=0", "P3-Red=600", "P3-Blue=1200", "P3-Gold=0", "P3-Green=300", "P4-Red=1200", "P4-Blue=0", "P4-Gold=300", "P4-Green=600"]},
             "players": {"1": {"cash": 1500, "theme": "Red", "paintings": ["P1-Red", "P1-Blue", "P1-Gold", "P1-Green"]},
                         "2": {"cash": 2700, "theme": "Blue", "paintings": ["P2-Red", "P2-Blue", "P2-Green"]},
                         "3": {"cash": 1000, "theme": "Gold", "paintings": ["P3-Red"]},
                         "4": {"cash": 1500, "theme": "Green", "paintings": []}}},
   "rules": [],
   "expect": {"winner": 2,
              "standings": {"1": 400001500, "2": 400002700, "3": 160001000, "4": 150001500},
              "players": {"1": {"score": 4000}, "2": {"score": 4000}, "3": {"score": 1600}, "4": {"score": 1500}}}},

  {"name": "Tied on score and cash: shared win", "rule": "R18", "players": 4, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11, "painting_values": ["P1-Red=0", "P1-Blue=300", "P1-Gold=600", "P1-Green=1200", "P2-Red=300", "P2-Blue=600", "P2-Gold=1200", "P2-Green=0", "P3-Red=600", "P3-Blue=1200", "P3-Gold=0", "P3-Green=300", "P4-Red=1200", "P4-Blue=0", "P4-Gold=300", "P4-Green=600"]},
             "players": {"1": {"cash": 1500, "theme": "Red", "paintings": ["P1-Red", "P1-Blue", "P1-Gold", "P1-Green"]},
                         "2": {"cash": 1500, "theme": "Blue", "paintings": ["P2-Red", "P2-Blue", "P2-Gold", "P2-Green"]},
                         "3": {"cash": 0, "theme": "Gold", "paintings": []},
                         "4": {"cash": 1500, "theme": "Green", "paintings": []}}},
   "rules": [],
   "expect": {"winner": [1, 2],
              "players": {"1": {"score": 4000}, "2": {"score": 4000}, "3": {"score": 0}, "4": {"score": 1500}}}}
]
```
````
