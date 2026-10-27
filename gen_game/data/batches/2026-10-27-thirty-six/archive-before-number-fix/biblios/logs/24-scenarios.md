# 24 scenarios

- time: 2026-10-27T17:41:01+00:00 (77.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 9e6f84c0c736baef, reply sha256 d0b8c3f002b95ca5

## Sent

````
SPEC:
{
  "name": "Biblios: Scriptorium Duel of Three",
  "summary": "Three scribes take turns as the active seat. Each round the active seat secretly keeps one of two drawn cards, and the other two seats bid gold for the other card. Church cards shift colour values, and each colour scores for the single player with the strictly highest total.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 24,
    "colour_cards": 18,
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
    "starting_colour_vp": 3,
    "vp_min": 1,
    "vp_max": 5,
    "rounds": 12,
    "cards_drawn_per_round": 2,
    "turns_active_per_seat": 4,
    "min_winning_bid": 1,
    "church_choices_max_per_round": 2,
    "tiebreak_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "cards kept as the active player; never announced until the end",
        "observable": false
      },
      {
        "key": "bought",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "lots this player won at auction",
        "observable": true
      },
      {
        "key": "red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sum of the red card values held (hand plus bought)",
        "observable": false
      },
      {
        "key": "blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sum of the blue card values held",
        "observable": false
      },
      {
        "key": "green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "sum of the green card values held",
        "observable": false
      },
      {
        "key": "gold",
        "type": "number",
        "visible": "ally",
        "initial": 4,
        "meaning": "gold coins; hidden during play, revealed at scoring, used as the tie-break",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "secret bid this round; announced after both bids are in, then reset to 0",
        "observable": false
      },
      {
        "key": "church_pending",
        "type": "bool",
        "visible": "ally",
        "initial": false,
        "meaning": "true if the player gained a Church card this round and must make a Church choice",
        "observable": false
      },
      {
        "key": "church_choice",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "the Church choice made this round",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's talk message",
        "observable": false
      },
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "victory points, scored at the end",
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
        "meaning": "the shuffled deck; its order is unknown to all, and its composition is public",
        "observable": false
      },
      {
        "key": "drawn",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the two cards drawn this round; shown only to the active player",
        "observable": false
      },
      {
        "key": "lot",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "the card up for auction",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the current round number, 1 to 12",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "((round-1) mod 3)+1",
        "observable": false
      },
      {
        "key": "vp_red",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "VP value of red, kept between 1 and 5",
        "observable": true
      },
      {
        "key": "vp_blue",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "VP value of blue, kept between 1 and 5",
        "observable": true
      },
      {
        "key": "vp_green",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "VP value of green, kept between 1 and 5",
        "observable": true
      }
    ]
  },
  "setup": [
    "The deck is filled with the 24 cards listed and is drawn from at random, which is equivalent to one shuffle; it is never reshuffled.",
    "Each player gets gold 4, red/blue/green 0, an empty hand and an empty bought list, bid 0, church_pending false, church_choice 'none', an empty message and vp 0.",
    "The table gets vp_red=3, vp_blue=3, vp_green=3, round=0, lot='none' and drawn empty.",
    "Each player is sent their own state."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; active_seat = ((round-1) mod 3)+1; announce the round and the active seat."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Two cards are drawn at random from deck into drawn and removed from deck. They are shown only to the active seat."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "one of the two cards in drawn",
      "effect": "The chosen card is appended to the active player's hand. If it is red-v, blue-v or green-v, that colour total += v; if it is gold-v, gold += v; if it is church, church_pending = true. The choice is not announced."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "The other drawn card becomes lot and is announced to everyone; drawn is emptied."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a short text message",
      "effect": "message is set for each player; then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Nothing said is binding."
    },
    {
      "action": "poll",
      "who": "the two non-active seats",
      "answer": "a whole number from 0 to the bidder's current gold",
      "effect": "bid is set for each bidder and stays secret until both bids are in."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If one bid is strictly greater than the other and at least 1, that bidder: gold -= bid; the active player's gold += that bid; lot is appended to bought; a colour lot adds its value to that colour total, a gold lot adds its value to gold, and a church lot sets church_pending = true. If the bids are equal (including 0-0), nobody pays and the lot is discarded. Both bids and the result (the winner and the price, or 'discarded') are announced. Then both bids are reset to 0 and lot = 'none'."
    },
    {
      "action": "poll",
      "who": "every player with church_pending true (at most two)",
      "answer": "one of: red up, red down, blue up, blue down, green up, green down",
      "effect": "church_choice is set for each chooser."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "For each colour C: vp_C = min(5, max(1, vp_C + (count of 'C up') - (count of 'C down'))). All choices are announced with who made them. Then church_pending = false and church_choice = 'none' for everyone."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round == 12, go to the end: reveal every hand, colour total and gold. For each colour C, a player whose C total is strictly greater than both other players' C totals gets vp += vp_C; a tied top total scores no one. Then the game ends. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "round == 12 after the Church step, with colour scoring applied",
    "rank_by": "you.vp * 1000 + you.gold",
    "decided_by": "The player with the highest vp wins. A tie on vp goes to the player with more remaining gold. Players still tied share the win, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At the start the deck holds exactly 24 cards: red, blue and green each with values 1,1,2,2,3,4, plus gold-2, gold-2, gold-3, gold-3 and 2 church cards."
    },
    {
      "id": "R2",
      "text": "At the start each player has gold 4, red/blue/green 0, vp 0, an empty hand and an empty bought list."
    },
    {
      "id": "R3",
      "text": "At the start vp_red, vp_blue and vp_green are each 3."
    },
    {
      "id": "R4",
      "text": "In round r the active seat is ((r-1) mod 3)+1, so over 12 rounds each seat is active exactly 4 times."
    },
    {
      "id": "R5",
      "text": "Each round, 2 cards are removed from the deck into drawn, and only the active player is shown them."
    },
    {
      "id": "R6",
      "text": "When the active player keeps a colour card of value v, that colour total rises by v and the card goes to their hand unannounced."
    },
    {
      "id": "R7",
      "text": "When the active player keeps gold-v, their gold rises by v; when they keep church, their church_pending becomes true."
    },
    {
      "id": "R8",
      "text": "The drawn card that was not kept becomes the lot and is announced to everyone, and drawn is emptied."
    },
    {
      "id": "R9",
      "text": "Every round all 3 players simultaneously write one message, and all messages are then shown to everyone with the writer's seat."
    },
    {
      "id": "R10",
      "text": "Only the 2 non-active seats bid, simultaneously, each a whole number from 0 to their current gold."
    },
    {
      "id": "R11",
      "text": "When one bid is strictly higher and at least 1, that bidder pays the bid from their gold to the active player's gold and gains the lot in bought, with its colour value, gold value or church_pending applied."
    },
    {
      "id": "R12",
      "text": "When the two bids are equal (for example 2 and 2, or 0 and 0), nobody pays and the lot is discarded."
    },
    {
      "id": "R13",
      "text": "Both bids and the auction result are announced, then the bids reset to 0 and lot becomes 'none'."
    },
    {
      "id": "R14",
      "text": "Each player with church_pending true chooses one of red up, red down, blue up, blue down, green up, green down, simultaneously with any other chooser."
    },
    {
      "id": "R15",
      "text": "Each colour's VP value changes by (ups minus downs) this round and is then clamped once to 1..5: for example 5 with 1 up stays 5, and 3 with 1 up and 1 down stays 3."
    },
    {
      "id": "R16",
      "text": "After the Church step, every church_pending becomes false and every church_choice becomes 'none'."
    },
    {
      "id": "R17",
      "text": "The game ends after round 12, when the deck is empty."
    },
    {
      "id": "R18",
      "text": "At the end, a player whose total in a colour is strictly greater than both others' gains that colour's VP value in vp; if the top total is tied, nobody scores that colour."
    },
    {
      "id": "R19",
      "text": "The highest vp wins; tied vp is broken by more gold; a further tie is a shared win (draw)."
    }
  ],
  "offers": [
    {
      "question": "Keep a card",
      "who": "the active seat only",
      "options": "exactly the two cards currently in drawn (if both are the same card, that card)"
    },
    {
      "question": "Talk",
      "who": "all three seats",
      "options": "any short free-text message"
    },
    {
      "question": "Bid on the lot",
      "who": "the two non-active seats; the active seat is not asked",
      "options": "whole numbers from 0 to the bidder's current gold"
    },
    {
      "question": "Church choice",
      "who": "only seats with church_pending true; seats without a pending Church are not asked",
      "options": "red up, red down, blue up, blue down, green up, green down"
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3. The rotation ((r-1) mod 3)+1, the two-bidder auction and 4 active turns each over a 24-card deck only work at exactly 3. At 3, one rival always sits out of each auction, which creates kingmaking tension."
    },
    {
      "what": "Talk kept as a simultaneous poll with broadcast",
      "why": "The source requires simultaneous messages. Talk earns its place because players disagree about prices and Church moves, and they can bluff about their hidden keeps."
    },
    {
      "what": "rank_by = vp*1000 + gold",
      "why": "This puts vp first and gold as the tie-break. Total gold can never exceed 22, so 1000 separates the two cleanly. Equal values share the win, which is the source's draw."
    },
    {
      "what": "gold marked observable",
      "why": "The rules reveal all gold at scoring, and gold decides ties."
    },
    {
      "what": "Drawing two random cards stands in for taking the top two of a once-shuffled deck",
      "why": "This is equivalent in distribution, and the deck order is unknown to all anyway."
    },
    {
      "what": "The card values are listed as counts per value in parameters",
      "why": "Parameters must be numbers, so the value lists 1,1,2,2,3,4 and 2,2,3,3 are written as how many cards carry each value."
    }
  ],
  "simplifications": [
    {
      "what": "Comparing the two bids, and comparing colour totals at the end, use table helper values (for example the top and second bid, and the maximum of the other players' totals)",
      "why": "The engine has no direct player-to-player attribute compare; this is the documented workaround."
    },
    {
      "what": "Card effects are applied by parsing the card name (colour and value) with conditional operations",
      "why": "There is no card-type lookup; the cards are text in lists."
    },
    {
      "what": "The end-of-game reveal and colour scoring are carried out within the final check step",
      "why": "The step list is flat, but the scoring is pure arithmetic, so it can be done with conditional updates when round == 12."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bought, gold, vp; table: round, vp_red, vp_blue, vp_green.
````

## Reply

````
```json
[
  {"name": "R1: the deck starts with 24 cards", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 24, "drawn": 0}},
              "game": {"round": 0}}},

  {"name": "R2: each player starts with 4 gold, 0 vp, an empty hand and an empty bought list", "rule": "R2", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"gold": 4, "vp": 0, "bought": []}, "2": {"gold": 4, "vp": 0, "bought": []}, "3": {"gold": 4, "vp": 0, "bought": []}},
              "lens": {"players": {"1": {"hand": 0, "bought": 0}, "2": {"hand": 0, "bought": 0}, "3": {"hand": 0, "bought": 0}}}}},

  {"name": "R3: each colour's VP value starts at 3", "rule": "R3", "players": 3, "rounds": 0,
   "expect": {"game": {"vp_red": 3, "vp_blue": 3, "vp_green": 3, "round": 0}}},

  {"name": "R4: in round 2 seat 2 is active, keeps a card and does not bid", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"game": {"round": 1, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 2, "options_include": "red-3"},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 2},
              "offered": [{"seat": 2, "option": "red-3"}, {"seat": 1, "option": 0}, {"seat": 3, "option": 0}],
              "not_offered": [{"seat": 1, "option": "red-3"}, {"seat": 3, "option": "red-3"}, {"seat": 2, "option": 0}],
              "players": {"1": {"gold": 4}, "2": {"gold": 4}, "3": {"gold": 4}},
              "lens": {"players": {"2": {"hand": 1}}}}},

  {"name": "R5: one round removes 2 cards from the deck (the cards drawn are random, so only the counts are checked)", "rule": "R5", "players": 3, "rounds": 1,
   "rules": [{"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1},
              "lens": {"game": {"deck": 22, "drawn": 0}, "players": {"1": {"hand": 1}}}}},

  {"name": "R6: keeping red-3 adds 3 to red, which wins red at the final scoring", "rule": "R6", "players": 3,
   "given": {"game": {"round": 11, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 3, "options_include": "red-3"},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"}],
   "expect": {"winner": 3,
              "standings": {"1": 4, "2": 4, "3": 3004},
              "players": {"1": {"vp": 0, "gold": 4, "bought": []}, "2": {"vp": 0, "gold": 4, "bought": []}, "3": {"vp": 3, "gold": 4, "bought": []}},
              "lens": {"players": {"3": {"hand": 1}}},
              "game": {"round": 12}}},

  {"name": "R7: keeping gold-3 adds 3 gold to the active player", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["gold-3", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "gold-3"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"gold": 7, "bought": []}, "2": {"gold": 4}, "3": {"gold": 4}},
              "lens": {"players": {"1": {"hand": 1}}}}},

  {"name": "R7: keeping church gives the keeper a Church choice (red up makes red 4)", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["church", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "church"},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"vp_red": 4, "vp_blue": 3, "vp_green": 3},
              "offered": [{"seat": 1, "option": "red up"}],
              "not_offered": [{"seat": 2, "option": "red up"}, {"seat": 3, "option": "red up"}],
              "players": {"1": {"gold": 4}, "2": {"gold": 4}, "3": {"gold": 4}}}},

  {"name": "R8: the card not kept becomes the lot that a bidder can win", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-3"},
             {"seat": 2, "options_include": 1},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"2": {"bought": ["blue-2"]}, "1": {"bought": []}, "3": {"bought": []}},
              "lens": {"game": {"drawn": 0}, "players": {"1": {"hand": 1}}}}},

  {"name": "R9: a round with talk changes nothing binding", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-3"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"round": 1},
              "players": {"1": {"gold": 4, "bought": []}, "2": {"gold": 4, "bought": []}, "3": {"gold": 4, "bought": []}}}},

  {"name": "R10: a bidder may bid up to its current gold but not more, and the active seat does not bid", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"gold": 2}}, "game": {"round": 0, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-3"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"offered": [{"seat": 2, "option": 2}, {"seat": 3, "option": 4}],
              "not_offered": [{"seat": 2, "option": 3}, {"seat": 1, "option": 0}],
              "players": {"1": {"gold": 6}, "2": {"gold": 0, "bought": ["blue-2"]}, "3": {"gold": 4}}}},

  {"name": "R11: the higher bidder pays the active player and gains a gold lot's value", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-1", "gold-3"]}},
   "rules": [{"seat": 1, "options_include": "red-1"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"gold": 6}, "2": {"gold": 5, "bought": ["gold-3"]}, "3": {"gold": 4, "bought": []}}}},

  {"name": "R11: winning a church lot gives the buyer a Church choice", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-1", "church"]}},
   "rules": [{"seat": 1, "options_include": "red-1"},
             {"seat": 2, "options_include": 1},
             {"seat": 2, "options_include": "blue down"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"gold": 5}, "2": {"gold": 3, "bought": ["church"]}, "3": {"gold": 4}},
              "game": {"vp_blue": 2, "vp_red": 3, "vp_green": 3},
              "offered": [{"seat": 2, "option": "blue down"}],
              "not_offered": [{"seat": 1, "option": "blue down"}, {"seat": 3, "option": "blue down"}]}},

  {"name": "R12: equal bids (2 and 2) mean nobody pays and the lot is discarded", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-3"},
             {"seat": 2, "options_include": 2},
             {"seat": 3, "options_include": 2}],
   "expect": {"players": {"1": {"gold": 4, "bought": []}, "2": {"gold": 4, "bought": []}, "3": {"gold": 4, "bought": []}}}},

  {"name": "R13: the winner pays its own bid once, and the loser pays nothing", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["red-3", "blue-2"]}},
   "rules": [{"seat": 1, "options_include": "red-3"},
             {"seat": 2, "options_include": 1},
             {"seat": 3, "options_include": 3}],
   "expect": {"players": {"1": {"gold": 7}, "2": {"gold": 4, "bought": []}, "3": {"gold": 1, "bought": ["blue-2"]}}}},

  {"name": "R14: two church holders both choose, and their choices add up", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["church", "church"]}},
   "rules": [{"seat": 1, "options_include": "church"},
             {"seat": 1, "options_include": "green up"},
             {"seat": 2, "options_include": 1},
             {"seat": 2, "options_include": "green up"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"vp_green": 5, "vp_red": 3, "vp_blue": 3},
              "offered": [{"seat": 1, "option": "green up"}, {"seat": 2, "option": "green up"}],
              "not_offered": [{"seat": 3, "option": "green up"}],
              "players": {"1": {"gold": 5}, "2": {"gold": 3, "bought": ["church"]}}}},

  {"name": "R15: red at 5 with one up stays 5", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "vp_red": 5, "deck": ["church", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "church"},
             {"seat": 1, "options_include": "red up"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"vp_red": 5, "vp_blue": 3, "vp_green": 3}}},

  {"name": "R15: blue at 3 with one up and one down stays 3", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "deck": ["church", "church"]}},
   "rules": [{"seat": 1, "options_include": "church"},
             {"seat": 1, "options_include": "blue up"},
             {"seat": 2, "options_include": 2},
             {"seat": 2, "options_include": "blue down"},
             {"seat": 3, "options_include": 1}],
   "expect": {"game": {"vp_blue": 3, "vp_red": 3, "vp_green": 3},
              "players": {"1": {"gold": 6}, "2": {"gold": 2, "bought": ["church"]}, "3": {"gold": 4}}}},

  {"name": "R15: green at 1 with one down stays 1", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"game": {"round": 0, "vp_green": 1, "deck": ["church", "red-1"]}},
   "rules": [{"seat": 1, "options_include": "church"},
             {"seat": 1, "options_include": "green down"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"vp_green": 1, "vp_red": 3, "vp_blue": 3}}},

  {"name": "R16: a pending Church is cleared after the Church step, so it is not chosen again next round (the draws are random, so only vp_red is checked)", "rule": "R16", "players": 3, "rounds": 2,
   "given": {"players": {"2": {"church_pending": true}}, "game": {"round": 0, "deck": ["red-1", "red-1", "blue-1", "blue-1"]}},
   "rules": [{"seat": 2, "options_include": "red up", "times": 1},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"},
             {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"game": {"vp_red": 4, "round": 2},
              "players": {"1": {"gold": 4}, "2": {"gold": 4}, "3": {"gold": 4}},
              "lens": {"game": {"deck": 0}}}},

  {"name": "R17: the game ends after round 12 with the deck empty, and gold breaks the vp tie", "rule": "R17", "players": 3,
   "given": {"game": {"round": 11, "deck": ["gold-2", "gold-3"]}},
   "rules": [{"seat": 3, "options_include": "gold-3"},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"}],
   "expect": {"winner": 3,
              "standings": {"1": 4, "2": 4, "3": 7},
              "game": {"round": 12},
              "lens": {"game": {"deck": 0}},
              "players": {"1": {"vp": 0, "gold": 4}, "2": {"vp": 0, "gold": 4}, "3": {"vp": 0, "gold": 7}}}},

  {"name": "R18: a tied top red total scores nobody, while sole leaders score blue and green", "rule": "R18", "players": 3,
   "given": {"players": {"1": {"red": 5, "blue": 1}, "2": {"red": 5, "blue": 4}, "3": {"red": 2, "blue": 1}},
             "game": {"round": 11, "deck": ["green-1", "green-2"]}},
   "rules": [{"seat": 3, "options_include": "green-2"},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": 4, "2": 3004, "3": 3004},
              "players": {"1": {"vp": 0, "gold": 4}, "2": {"vp": 3, "gold": 4}, "3": {"vp": 3, "gold": 4}}}},

  {"name": "R19: with vp tied, the seat with more gold wins", "rule": "R19", "players": 3,
   "given": {"players": {"1": {"red": 4, "gold": 6}, "2": {"blue": 4, "gold": 5}},
             "game": {"round": 11, "deck": ["green-1", "gold-2"]}},
   "rules": [{"seat": 3, "options_include": "gold-2"},
             {"seat": 1, "options_include": 0, "times": "all"},
             {"seat": 2, "options_include": 0, "times": "all"}],
   "expect": {"winner": 1,
              "standings": {"1": 3006, "2": 3005, "3": 6},
              "players": {"1": {"vp": 3, "gold": 6}, "2": {"vp": 3, "gold": 5}, "3": {"vp": 0, "gold": 6}}}}
]
```
````
