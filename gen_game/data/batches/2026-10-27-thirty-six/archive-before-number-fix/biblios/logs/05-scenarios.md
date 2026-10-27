# 05 scenarios

- time: 2026-10-27T17:18:57+00:00 (74.7s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 944a5662a226404d, reply sha256 e420ac518bacb66a

## Sent

````
SPEC:
{
  "name": "Biblios: Scriptorium",
  "summary": "Over 12 rounds, the active player draws 2 cards, secretly keeps one and auctions the other in a sealed bid. Church cards shift colour values, and the most cards in a colour wins that colour's VP.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 24,
    "colour_cards_per_colour": 6,
    "colour_cards_value_1_per_colour": 2,
    "colour_cards_value_2_per_colour": 2,
    "colour_cards_value_3_per_colour": 1,
    "colour_cards_value_4_per_colour": 1,
    "gold_cards": 4,
    "gold_cards_value_2": 2,
    "gold_cards_value_3": 2,
    "church_cards": 2,
    "starting_gold": 4,
    "vp_start": 3,
    "vp_min": 1,
    "vp_max": 5,
    "rounds": 12,
    "cards_drawn_per_round": 2,
    "cards_kept_per_round": 1,
    "min_bid": 0,
    "min_winning_bid": 1,
    "church_change": 1,
    "rank_vp_multiplier": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "gold",
        "type": "number",
        "visible": "ally",
        "initial": 4,
        "meaning": "Private Gold. It pays bids, receives sale proceeds and Gold cards, and breaks VP ties.",
        "observable": false
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Kept cards, face-down and private (colour cards and kept Church cards)",
        "observable": false
      },
      {
        "key": "kept_red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of values of kept Red cards",
        "observable": false
      },
      {
        "key": "kept_blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of values of kept Blue cards",
        "observable": false
      },
      {
        "key": "kept_green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Sum of values of kept Green cards",
        "observable": false
      },
      {
        "key": "bought",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Lots won at auction, face-up",
        "observable": true
      },
      {
        "key": "bought_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of values of bought Red cards",
        "observable": true
      },
      {
        "key": "bought_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of values of bought Blue cards",
        "observable": true
      },
      {
        "key": "bought_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of values of bought Green cards",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid",
        "observable": false
      },
      {
        "key": "church_pending",
        "type": "bool",
        "visible": "ally",
        "initial": false,
        "meaning": "True if the player gained a Church card this round (kept or bought); revealed when it is played at step 9",
        "observable": false
      },
      {
        "key": "church_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's Church play: a colour and +1 or -1",
        "observable": true
      },
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory points, calculated at end scoring",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "red-1",
          "red-1",
          "red-2",
          "red-2",
          "red-3",
          "red-4",
          "blue-1",
          "blue-1",
          "blue-2",
          "blue-2",
          "blue-3",
          "blue-4",
          "green-1",
          "green-1",
          "green-2",
          "green-2",
          "green-3",
          "green-4",
          "gold-2",
          "gold-2",
          "gold-3",
          "gold-3",
          "church",
          "church"
        ],
        "meaning": "Undrawn cards; the composition is public knowledge but the order is hidden",
        "observable": false
      },
      {
        "key": "drawn",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 2 cards drawn this round; shown only to the active player, as the options of the keep question",
        "observable": false
      },
      {
        "key": "lot",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card offered at auction this round",
        "observable": true
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Lots that went unsold",
        "observable": false
      },
      {
        "key": "vp_red",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Red VP value, 1-5",
        "observable": true
      },
      {
        "key": "vp_blue",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Blue VP value, 1-5",
        "observable": true
      },
      {
        "key": "vp_green",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Green VP value, 1-5",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the active player: ((round-1) mod player_count)+1",
        "observable": true
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch: highest bid this round",
        "observable": false
      },
      {
        "key": "high_count",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch: number of bidders at the highest bid",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the lot this round (0 if discarded)",
        "observable": false
      },
      {
        "key": "sale_price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Price paid this round (0 if discarded)",
        "observable": true
      }
    ]
  },
  "setup": [
    "Put the 24 cards listed above in the table list deck. The order is random because each draw takes a random card.",
    "Every player starts with gold = 4 (private), an empty hand, an empty bought list and all colour sums at 0.",
    "Set vp_red = vp_blue = vp_green = 3 (public).",
    "Set round = 0. Seat 1 will be the active player in round 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; active_seat = ((round-1) mod player_count) + 1; reset every player's bid = 0, church_pending = false, church_choice = ''; winner_seat = 0, sale_price = 0, high_bid = 0, high_count = 0, lot = ''"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Draw: move 2 random cards from deck into drawn (remove from deck, append to drawn)"
    },
    {
      "action": "ask",
      "who": "the active seat (active_seat)",
      "answer": "one card from drawn (only the active player sees these options)",
      "effect": "Kept colour card <c>-<v>: append it to the active player's hand and add v to kept_<c>. Kept gold-<v>: add v to the active player's gold. Kept church: append it to hand and set church_pending = true. The other card in drawn becomes lot, then drawn is cleared."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Offer: announce 'The lot is {lot}.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Talk: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}; talk is not binding"
    },
    {
      "action": "poll",
      "who": "every seat except active_seat",
      "answer": "whole number from 0 to the bidder's current gold",
      "effect": "Set each bidder's bid; no one sees a bid until all are in"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "high_bid = max bid among non-active seats; high_count = number of non-active seats with bid == high_bid. If high_count == 1 and high_bid >= 1: winner_seat = that seat, sale_price = high_bid, winner's gold -= high_bid, active player's gold += high_bid. Otherwise: winner_seat = 0, sale_price = 0, append lot to discard."
    },
    {
      "action": "update",
      "who": "the winner (when winner_seat > 0)",
      "answer": null,
      "effect": "Take: append lot to the winner's bought (public). Colour lot <c>-<v>: bought_<c> += v. Gold lot gold-<v>: winner's gold += v. Church lot: winner's church_pending = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {winner_seat} bought {lot} for {sale_price} Gold.', or 'The lot {lot} was discarded.' when winner_seat == 0"
    },
    {
      "action": "poll",
      "who": "every player with church_pending == true (skipped if none)",
      "answer": "one of: red+1, red-1, blue+1, blue-1, green+1, green-1",
      "effect": "Set church_choice and reveal that the player played a Church card. Then apply every choice one after another: vp_<c> = min(5, max(1, vp_<c> \u00b1 1)), so a colour may receive two changes."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce each church_choice made this round and the VP values: 'Red {vp_red}, Blue {vp_blue}, Green {vp_green}.'"
    },
    {
      "action": "update",
      "who": "table (end scoring, only when round == 12)",
      "answer": null,
      "effect": "For each colour c: each player's total_c = kept_c + bought_c; m_c = max total_c over players. If m_c > 0, each player with total_c == m_c adds vp_c / (number of players with total_c == m_c) to vp. Gold adds no VP. Reveal all hands."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round == 12, end the game; otherwise continue"
    }
  ],
  "ending": {
    "condition": "round == 12 after the step 9 Church resolution and end scoring",
    "rank_by": "you.vp * 1000 + you.gold",
    "decided_by": "Most VP wins. A tie on VP is broken by the most leftover Gold. Players still tied on both share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, the deck holds 24 cards: Red, Blue and Green each 1,1,2,2,3,4, Gold 2,2,3,3, and 2 Church. Each player has 4 Gold, and the Red, Blue and Green VP values are each 3."
    },
    {
      "id": "R2",
      "text": "When round r begins, the active seat is ((r-1) mod player_count)+1, so round 1 is seat 1."
    },
    {
      "id": "R3",
      "text": "When a round begins, 2 cards are removed from the deck, and only the active player sees them."
    },
    {
      "id": "R4",
      "text": "When the active player keeps a colour card of value v, it goes into their private hand and adds v to their kept sum for that colour."
    },
    {
      "id": "R5",
      "text": "When the active player keeps a Gold card of value v, their gold increases by v immediately."
    },
    {
      "id": "R6",
      "text": "When the active player keeps a Church card, they play it at step 9 that round."
    },
    {
      "id": "R7",
      "text": "When a card is kept, the other drawn card becomes the public lot."
    },
    {
      "id": "R8",
      "text": "When the talk step runs, every player including the active player sends one message at once, and all messages are shown to everyone."
    },
    {
      "id": "R9",
      "text": "When bidding, every non-active player at once bids a whole number from 0 to their current gold, and the active player does not bid."
    },
    {
      "id": "R10",
      "text": "When exactly one player has the highest bid and it is at least 1, that player pays the bid from their gold to the active player's gold and takes the lot."
    },
    {
      "id": "R11",
      "text": "When the highest bid is tied or all bids are 0, nobody pays and the lot is discarded."
    },
    {
      "id": "R12",
      "text": "When a colour lot of value v is won, it is public in the winner's bought cards and adds v to their bought sum for that colour."
    },
    {
      "id": "R13",
      "text": "When a Gold lot of value v is won, the winner's gold increases by v."
    },
    {
      "id": "R14",
      "text": "When a Church lot is won, the winner plays it at step 9 that round."
    },
    {
      "id": "R15",
      "text": "When the auction resolves, the sale price, or that the lot was discarded, is announced."
    },
    {
      "id": "R16",
      "text": "When players gained a Church card this round, each chooses at once one colour and +1 or -1. All changes apply, each VP value is limited to 1-5, and a colour may receive two changes."
    },
    {
      "id": "R17",
      "text": "When a Church card is played, it and the chosen change are revealed, and the new VP values are announced."
    },
    {
      "id": "R18",
      "text": "When round 12 ends, the game ends and the deck is empty."
    },
    {
      "id": "R19",
      "text": "When scoring a colour, each player's total is their kept plus bought values in it, and the sole highest total gains that colour's VP value."
    },
    {
      "id": "R20",
      "text": "When several players tie for the highest total in a colour, they split its VP value equally, and fractions are allowed."
    },
    {
      "id": "R21",
      "text": "When every player has 0 in a colour, that colour scores for no one."
    },
    {
      "id": "R22",
      "text": "When scoring, Gold scores no VP."
    },
    {
      "id": "R23",
      "text": "When VP totals tie for first, the tied player with more leftover gold wins; if gold also ties, those players draw."
    }
  ],
  "offers": [
    {
      "question": "Keep: which drawn card to keep",
      "who": "the active seat only",
      "options": "exactly the 2 cards in drawn"
    },
    {
      "question": "Talk: short message",
      "who": "every seat, including the active seat",
      "options": "free short text"
    },
    {
      "question": "Bid",
      "who": "every seat except the active seat",
      "options": "whole numbers from 0 to that seat's current gold; the active seat is not asked"
    },
    {
      "question": "Church: colour and direction",
      "who": "only seats with church_pending == true this round",
      "options": "red+1, red-1, blue+1, blue-1, green+1, green-1; seats without a Church card this round are not asked"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The designer suggests 3, so it is kept. The minimum is 3 because with 2 players the auction has a single bidder and no rivalry. The maximum is 4 because that is the source's limit; the 24-card deck and 12 rounds are fixed, so more seats would leave each player too few turns as the active seller."
    },
    {
      "what": "Keep the simultaneous talk step as a poll broadcast to all",
      "why": "The source requires it, and it earns its place: players disagree about who should take each colour, and the seller can bluff about the hidden kept card to raise the price."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player reads the others' bought cards and their bluffs to infer majorities. They price a lot by the gold it hands the seller, and use Church cards to raise colours they lead and lower colours they trail."
    },
    {
      "what": "Card encoding as text 'colour-value', 'gold-value', 'church'",
      "why": "It gives the keep options and lots a readable, parseable form."
    },
    {
      "what": "Card distribution expressed as numeric counts per value in parameters",
      "why": "Parameters must be numbers, so the value lists are given as how many cards of each value exist."
    },
    {
      "what": "rank_by = vp*1000 + gold",
      "why": "It folds the Gold tie-break into one expression. Fractional VP differences are at least 1/12, and 1000/12 is about 83, which exceeds the maximum possible gold (26 with 4 players)."
    },
    {
      "what": "Church changes applied one after another, with clamping at each step",
      "why": "The source says to apply all changes, limited to 1-5, but does not say whether clamping happens per change or at the end. Applying them in sequence is the natural reading."
    },
    {
      "what": "Separate kept (private) and bought (public) sums per colour",
      "why": "Kept cards are hidden and bought cards are face-up, so their visibility differs. Scoring adds the two."
    },
    {
      "what": "End scoring runs as an update conditioned on round == 12, placed before the end check",
      "why": "The check ends the game, so scoring must happen before it."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling is replaced by drawing random cards from the deck list",
      "why": "This is equivalent to a shuffled deck in the engine's draw model."
    },
    {
      "what": "The drawn cards are shown only to the active player as the options of the keep question, not through an 'active player only' visibility",
      "why": "The engine has no per-round visibility for the active player; private question options give the same effect."
    },
    {
      "what": "The Gold tie-break and the draw are folded into a single ranking where tied players share the win",
      "why": "The engine ranks by one arithmetic expression and has no separate draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bought, bought_red, bought_blue, bought_green, church_choice, vp; table: lot, vp_red, vp_blue, vp_green, round, active_seat, sale_price.
````

## Reply

````
```json
[
  {"name": "Setup: 24-card deck, empty bought lists, VP values all 3", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 24}, "players": {"1": {"bought": 0, "hand": 0}, "2": {"bought": 0, "hand": 0}, "3": {"bought": 0, "hand": 0}}},
              "game": {"vp_red": 3, "vp_blue": 3, "vp_green": 3, "round": 0},
              "players": {"1": {"bought_red": 0, "bought_blue": 0, "bought_green": 0}}}},

  {"name": "Round 5 with 3 players makes seat 2 active", "rule": "R2", "players": 3, "rounds": 1,
   "given": {"game": {"round": 4, "deck": ["red-1", "blue-2"]}},
   "rules": [{"seat": 2, "options_include": "red-1"}],
   "expect": {"game": {"round": 5, "active_seat": 2, "lot": "blue-2"},
              "offered": [{"seat": 2, "option": "red-1"}],
              "not_offered": [{"seat": 1, "option": "red-1"}, {"seat": 3, "option": "red-1"}]}},

  {"name": "Round start removes 2 cards from the deck, only the active seat is offered them", "rule": "R3", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-1", "red-2", "blue-1", "blue-2"]}},
   "default": "first",
   "expect": {"lens": {"game": {"deck": 2, "drawn": 0}},
              "not_offered": [{"seat": 2, "option": "red-1"}, {"seat": 2, "option": "red-2"}, {"seat": 2, "option": "blue-1"}, {"seat": 2, "option": "blue-2"},
                              {"seat": 3, "option": "red-1"}, {"seat": 3, "option": "red-2"}, {"seat": 3, "option": "blue-1"}, {"seat": 3, "option": "blue-2"}]}},

  {"name": "A kept red-3 goes to the hand and scores Red at the end", "rule": "R4", "players": 3,
   "given": {"game": {"round": 11, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 3, "options_include": "red-3"}],
   "expect": {"winner": 3, "standings": {"1": 4, "2": 4, "3": 3004},
              "lens": {"players": {"3": {"hand": 1}}},
              "players": {"1": {"vp": 0}, "2": {"vp": 0}, "3": {"vp": 3}}}},

  {"name": "A kept gold-3 adds 3 gold at once", "rule": "R5", "players": 3,
   "given": {"game": {"round": 11, "deck": ["gold-3", "green-1"]}},
   "rules": [{"seat": 3, "options_include": "gold-3"}],
   "expect": {"winner": 3, "standings": {"1": 4, "2": 4, "3": 7},
              "players": {"1": {"vp": 0}, "2": {"vp": 0}, "3": {"vp": 0}}}},

  {"name": "A kept Church is played the same round", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["church", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "church"}, {"seat": 1, "options_include": "blue+1"}],
   "expect": {"game": {"vp_blue": 4, "vp_red": 3, "vp_green": 3, "lot": "red-1"},
              "players": {"1": {"church_choice": "blue+1"}},
              "offered": [{"seat": 1, "option": "blue+1"}],
              "not_offered": [{"seat": 2, "option": "blue+1"}, {"seat": 3, "option": "blue+1"}]}},

  {"name": "The card not kept becomes the lot", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["green-4", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}],
   "expect": {"game": {"lot": "green-4", "sale_price": 0}}},

  {"name": "The talk step runs and the round continues normally", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["green-2", "blue-1"]}},
   "rules": [{"seat": 1, "options_include": "blue-1"}],
   "expect": {"game": {"round": 1, "lot": "green-2"}}},

  {"name": "Only non-active seats bid, from 0 up to their gold", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"3": {"gold": 2}}, "game": {"deck": ["green-2", "blue-1"]}},
   "rules": [{"seat": 1, "options_include": "blue-1"}],
   "expect": {"offered": [{"seat": 2, "option": 4}, {"seat": 2, "option": 0}, {"seat": 3, "option": 2}],
              "not_offered": [{"seat": 2, "option": 5}, {"seat": 3, "option": 3}, {"seat": 1, "option": 0}]}},

  {"name": "The sole highest bidder pays and takes the lot", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-1", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 1}],
   "expect": {"game": {"sale_price": 3, "lot": "blue-2"},
              "players": {"2": {"bought": ["blue-2"], "bought_blue": 2}, "3": {"bought": [], "bought_blue": 0}}}},

  {"name": "Tied top bids: lot discarded, nobody pays", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-1", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 2}],
   "expect": {"game": {"sale_price": 0},
              "lens": {"game": {"discard": 1}, "players": {"2": {"bought": 0}, "3": {"bought": 0}}},
              "players": {"2": {"bought_blue": 0}, "3": {"bought_blue": 0}}}},

  {"name": "All bids 0: lot discarded", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-1", "green-3"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"sale_price": 0},
              "lens": {"game": {"discard": 1}, "players": {"2": {"bought": 0}, "3": {"bought": 0}}}}},

  {"name": "A won green-3 is public and adds 3 to bought_green", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-1", "green-3"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 1}],
   "expect": {"game": {"sale_price": 1},
              "players": {"3": {"bought": ["green-3"], "bought_green": 3}, "2": {"bought_green": 0}}}},

  {"name": "A won gold-2 adds 2 gold to the winner (seen in the final standings)", "rule": "R13", "players": 3,
   "given": {"game": {"round": 11, "deck": ["gold-2", "red-1"]}},
   "rules": [{"seat": 3, "options_include": "red-1"}, {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 5, "2": 4, "3": 3005},
              "players": {"1": {"bought": ["gold-2"], "vp": 0}, "3": {"vp": 3}}}},

  {"name": "A won Church is played by the buyer that round", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["church", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0},
             {"seat": 2, "options_include": "green-1"}],
   "expect": {"game": {"vp_green": 2, "sale_price": 1},
              "players": {"2": {"bought": ["church"], "church_choice": "green-1"}},
              "offered": [{"seat": 2, "option": "green-1"}],
              "not_offered": [{"seat": 1, "option": "green-1"}, {"seat": 3, "option": "green-1"}]}},

  {"name": "The sale price is made public", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["red-2", "blue-4"]}},
   "rules": [{"seat": 1, "options_include": "red-2"}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"sale_price": 2, "lot": "blue-4"}, "players": {"2": {"bought": ["blue-4"]}}}},

  {"name": "Two Church plays on the same colour both apply, capped at 5", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"game": {"vp_red": 4, "deck": ["church", "church"]}},
   "rules": [{"seat": 1, "options_include": "church"}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "red+1"}, {"seat": 2, "options_include": "red+1"}],
   "expect": {"game": {"vp_red": 5, "vp_blue": 3, "vp_green": 3},
              "players": {"1": {"church_choice": "red+1"}, "2": {"church_choice": "red+1"}}}},

  {"name": "Two Church plays lower a colour by 2", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["church", "church"]}},
   "rules": [{"seat": 1, "options_include": "church"}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0},
             {"seat": 1, "options_include": "red-1"}, {"seat": 2, "options_include": "red-1"}],
   "expect": {"game": {"vp_red": 1, "vp_blue": 3, "vp_green": 3}}},

  {"name": "A played Church choice is revealed publicly with the new value", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"game": {"deck": ["church", "blue-1"]}},
   "rules": [{"seat": 1, "options_include": "church"}, {"seat": 1, "options_include": "green+1"}],
   "expect": {"game": {"vp_green": 4}, "players": {"1": {"church_choice": "green+1"}, "2": {"church_choice": ""}}}},

  {"name": "The game ends after round 12 with the deck empty", "rule": "R18", "players": 3,
   "given": {"game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-3"}],
   "expect": {"winner": 3, "standings": {"1": 4, "2": 4, "3": 7},
              "lens": {"game": {"deck": 0}}, "game": {"round": 12}}},

  {"name": "Kept plus bought: total 5 beats total 4 and takes Red", "rule": "R19", "players": 3,
   "given": {"players": {"1": {"kept_red": 4, "hand": ["red-4"]},
                         "2": {"kept_red": 2, "hand": ["red-2"], "bought": ["red-3"], "bought_red": 3}},
             "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": 2, "standings": {"1": 4, "2": 3004, "3": 6},
              "players": {"1": {"vp": 0}, "2": {"vp": 3}, "3": {"vp": 0}}}},

  {"name": "A tie for most Blue splits its 3 VP as 1.5 each", "rule": "R20", "players": 3,
   "given": {"players": {"1": {"kept_blue": 3, "hand": ["blue-3"]},
                         "2": {"bought": ["blue-3"], "bought_blue": 3}},
             "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": [1, 2], "standings": {"1": 1504, "2": 1504, "3": 6},
              "players": {"1": {"vp": 1.5}, "2": {"vp": 1.5}, "3": {"vp": 0}}}},

  {"name": "Colours nobody holds score for no one", "rule": "R21", "players": 3,
   "given": {"players": {"1": {"kept_red": 1, "hand": ["red-1"]}},
             "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": 1, "standings": {"1": 3004, "2": 4, "3": 6},
              "players": {"1": {"vp": 3}, "2": {"vp": 0}, "3": {"vp": 0}}}},

  {"name": "Gold scores no VP", "rule": "R22", "players": 3,
   "given": {"players": {"2": {"gold": 20}}, "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": 2, "standings": {"1": 4, "2": 20, "3": 6},
              "players": {"1": {"vp": 0}, "2": {"vp": 0}, "3": {"vp": 0}}}},

  {"name": "A VP tie is won by the seat with more leftover gold", "rule": "R23", "players": 3,
   "given": {"players": {"1": {"kept_red": 2, "hand": ["red-2"]},
                         "2": {"kept_red": 2, "hand": ["red-2"], "gold": 7}},
             "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": 2, "standings": {"1": 1504, "2": 1507, "3": 6},
              "players": {"1": {"vp": 1.5}, "2": {"vp": 1.5}, "3": {"vp": 0}}}},

  {"name": "A tie on both VP and gold shares the win", "rule": "R23", "players": 3,
   "given": {"players": {"1": {"kept_red": 2, "hand": ["red-2"]},
                         "2": {"kept_red": 2, "hand": ["red-2"]}},
             "game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"}],
   "expect": {"winner": [1, 2], "standings": {"1": 1504, "2": 1504, "3": 6},
              "players": {"1": {"vp": 1.5}, "2": {"vp": 1.5}}}}
]
```
````
