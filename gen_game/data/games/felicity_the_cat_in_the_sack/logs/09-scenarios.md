# 09 scenarios

- time: 2026-10-27T18:22:02+00:00 (61.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 0542cd1eb801f93e, reply sha256 f1c4538311248f0d

## Sent

````
SPEC:
{
  "name": "Cat in the Sack: Paid Entry",
  "summary": "Each round every player secretly puts one card into a shared sack. Some sack cards are revealed, players talk, then pay to stay or get paid to drop. Stayers bid sealed mice for the sack, whose cat value may be negative.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "cat_value_1": -8,
    "cat_value_2": -5,
    "cat_value_3": 3,
    "cat_value_4": 5,
    "cat_value_5": 8,
    "cat_value_6": 11,
    "cat_value_7": 15,
    "rabbit_value": 0,
    "dog_value": 0,
    "cards_per_hand": 9,
    "cards_removed_per_hand": 1,
    "starting_mice": 15,
    "starting_cat_points": 0,
    "rounds": 8,
    "stay_fee": 1,
    "drop_payment": 2,
    "min_mice_to_stay": 2,
    "min_bid": 1,
    "first_reveal_with_3_players": 1,
    "first_reveal_with_4_or_5_players": 2,
    "second_reveal_count": 1,
    "dogs_that_cancel_top_cat": 1,
    "start_seat_round_1": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [
          "cat_-8",
          "cat_-5",
          "cat_3",
          "cat_5",
          "cat_8",
          "cat_11",
          "cat_15",
          "rabbit",
          "dog"
        ],
        "meaning": "Cards still held. Before round 1 it holds 8 cards, after one is removed at random.",
        "observable": false
      },
      {
        "key": "removed_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The card removed at random from this player's hand at setup. Only its owner knows it.",
        "observable": false
      },
      {
        "key": "placed_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The card this player put into the sack this round.",
        "observable": false
      },
      {
        "key": "mice",
        "type": "number",
        "visible": "public",
        "initial": 15,
        "meaning": "Current mice.",
        "observable": true
      },
      {
        "key": "cat_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Accumulated sack values won.",
        "observable": true
      },
      {
        "key": "stayed",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if the player chose STAY this round.",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sealed bid this round, revealed with all other bids. 0 if the player dropped.",
        "observable": true
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message. Not binding.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number, 1 to 8.",
        "observable": true
      },
      {
        "key": "start_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Start player this round, used only for the sack tie-break.",
        "observable": true
      },
      {
        "key": "sack",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "This round's sack cards in shuffled order. It does not record who placed which card.",
        "observable": false
      },
      {
        "key": "revealed_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Sack cards shown so far this round, without owners.",
        "observable": true
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "All face-up discarded sack cards from earlier rounds.",
        "observable": true
      },
      {
        "key": "stayer_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose STAY this round.",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the sack this round, or 0 if nobody did.",
        "observable": true
      },
      {
        "key": "sack_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Computed value of this round's sack.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player's hand is set to the same 9 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog.",
    "For each player, one card is picked at random from their hand, removed from the hand and stored in that player's removed_card, which only that player can see.",
    "Each player's mice is set to 15 and cat_points to 0. The bank is unlimited, so it is not tracked.",
    "round is set to 0, start_seat to 1, and sack, revealed_cards and discard to empty lists."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1. start_seat = ((round - 1) mod player_count) + 1. Every player: stayed = false, bid = 0, placed_card = ''. sack = [], revealed_cards = [], winner_seat = 0, sack_value = 0. Announce the round and the start seat."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own hand",
      "effect": "Each player's choice is removed from hand, stored in placed_card and appended to sack. Nobody sees the choices."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Shuffle the sack: rebuild it by repeatedly drawing a card at random from it, which gives a random order."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "First reveal: append the first k cards of sack to revealed_cards, where k = 1 if player_count = 3, else 2. Tell everyone the revealed cards, without owners."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "message is set for each player. Broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"} once all messages are in."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "STAY or DROP (DROP only, if mice < 2)",
      "effect": "stayed = true for STAY, false for DROP. stayer_count = number of players with stayed = true. All choices are shown together."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Each player with stayed = true: mice -= 1 (never refunded). Each player with stayed = false: mice += 2."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Second reveal: append sack card number k+1 to revealed_cards, where k is the first-reveal count. Tell everyone."
    },
    {
      "action": "poll",
      "who": "each player with stayed = true",
      "answer": "whole number from 1 to your current mice",
      "effect": "bid is set for each stayer. All bids are revealed together."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If stayer_count = 0: winner_seat = 0. Otherwise winner_seat is the stayer with the highest key = bid * 100000 - mice * 100 - ((seat - start_seat + player_count) mod player_count). The ordering is: highest bid, then fewer current mice, then first in seat order counting from start_seat. Announce it."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Reveal all sack cards to everyone. Let cats = the values of the cat_ cards in sack, and dogs = the count of 'dog' in sack. sack_value = sum(cats), minus max(cats) if dogs = 1 and at least one cat is present. Rabbit and dog are worth 0, and 2 or more dogs have no effect. Announce sack_value."
    },
    {
      "action": "update",
      "who": "the winner_seat player",
      "answer": null,
      "effect": "If winner_seat != 0: that player's mice -= bid and cat_points += sack_value (which may be negative). Losing stayers change nothing more."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Append every sack card to discard (face up, public). sack = []. Announce mice and cat_points."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round >= 8, end the game. Otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= 8",
    "rank_by": "(you.mice + you.cat_points) * 1000 + you.cat_points",
    "decided_by": "Each player's total is cat_points plus mice, and the highest total wins. If totals tie, the tied player with more cat points wins. If that also ties, those players share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup every player's hand holds cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit and dog (9 cards)."
    },
    {
      "id": "R2",
      "text": "At setup exactly one random card is removed from each hand and recorded in that player's removed_card, visible only to that player, leaving 8 cards in hand."
    },
    {
      "id": "R3",
      "text": "At setup each player has mice = 15 and cat_points = 0."
    },
    {
      "id": "R4",
      "text": "In round r, start_seat = ((r - 1) mod player_count) + 1, so it is seat 1 in round 1 and seat 2 in round 2."
    },
    {
      "id": "R5",
      "text": "Each round every player simultaneously places one card from their hand into the sack, and that card leaves their hand permanently."
    },
    {
      "id": "R6",
      "text": "After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them."
    },
    {
      "id": "R7",
      "text": "Each round every player sends one simultaneous short message, and all messages are shown only after all are in. Messages are not binding."
    },
    {
      "id": "R8",
      "text": "When a player has fewer than 2 mice at the stay-or-drop step, they may only choose DROP."
    },
    {
      "id": "R9",
      "text": "When a player chooses STAY, they immediately pay 1 mouse, which is never refunded."
    },
    {
      "id": "R10",
      "text": "When a player chooses DROP, they receive 2 mice and take no further part in that round."
    },
    {
      "id": "R11",
      "text": "After stay-or-drop, one more sack card is revealed to everyone."
    },
    {
      "id": "R12",
      "text": "Each stayer bids a whole number from 1 to their mice after paying the fee, and all bids are revealed together."
    },
    {
      "id": "R13",
      "text": "When bids differ, the highest bidder wins the sack."
    },
    {
      "id": "R14",
      "text": "When two or more stayers tie for the highest bid, the tied stayer with fewer current mice wins."
    },
    {
      "id": "R15",
      "text": "When the tied stayers also have equal mice, the one first in seat order counting from start_seat wins."
    },
    {
      "id": "R16",
      "text": "When nobody stays, nobody wins, no bid is paid and the sack is discarded."
    },
    {
      "id": "R17",
      "text": "When exactly one player stays, that player wins the sack and pays their bid."
    },
    {
      "id": "R18",
      "text": "The sack value is the sum of its cat card values. The rabbit and dogs are worth 0."
    },
    {
      "id": "R19",
      "text": "When the sack holds exactly 1 dog and at least one cat, the highest-valued cat is excluded from the sum (for example, cat_15 + cat_3 + dog + rabbit = 3)."
    },
    {
      "id": "R20",
      "text": "When the sack holds 2 or more dogs, they have no effect (for example, cat_15 + dog + dog = 15)."
    },
    {
      "id": "R21",
      "text": "The winner pays their bid in mice and adds the sack value, which may be negative, to cat_points."
    },
    {
      "id": "R22",
      "text": "Losing stayers receive nothing and do not get back the 1-mouse fee."
    },
    {
      "id": "R23",
      "text": "All sack cards are added to the public discard list at the end of each round."
    },
    {
      "id": "R24",
      "text": "The game ends after round 8."
    },
    {
      "id": "R25",
      "text": "The player with the highest cat_points + mice wins. On a tie the higher cat_points wins, and if that also ties those players share the win."
    }
  ],
  "offers": [
    {
      "question": "Fill the sack",
      "who": "all players",
      "options": "any card currently in that player's own hand"
    },
    {
      "question": "Talk",
      "who": "all players",
      "options": "one short free-text message"
    },
    {
      "question": "Stay or drop",
      "who": "all players",
      "options": "a player with mice >= 2: STAY, DROP. A player with mice < 2: DROP only."
    },
    {
      "question": "Sealed bid",
      "who": "each player with stayed = true",
      "options": "a whole number from 1 to that player's current mice (after the fee). Players who dropped are not asked."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer chose 4 and the source allows 3 to 5. 3 is the minimum because an auction needs rivals and the sack needs enough unknown cards to hide one's own. 5 is the maximum because the hand and reveal structure is built for 5, and with more seats one's own card would barely affect the sack."
    },
    {
      "what": "Talk kept as a simultaneous poll with broadcast",
      "why": "The source specifies simultaneous non-binding messages. Players disagree about the sack, since each wants others to drop or to overbid, so bluffing about one's placed card gives the others something to reason about."
    },
    {
      "what": "Cards encoded as text labels cat_<value>, rabbit and dog",
      "why": "The rabbit and dog are both worth 0 but behave differently, so a label is needed to count dogs."
    },
    {
      "what": "Cat card values listed as separate parameters cat_value_1 to cat_value_7",
      "why": "Each parameter must be a single number."
    },
    {
      "what": "Sack winner computed as one key: bid * 100000 - mice * 100 - seat offset from start_seat",
      "why": "This puts the source's three-level tie-break (bid, fewer mice, seat order from the start player) into a single arithmetic maximum."
    },
    {
      "what": "Ranking expression (mice + cat_points) * 1000 + cat_points",
      "why": "Cat points can never reach plus or minus 500, so the total is compared first and cat points break ties. Exact ties share the win, which is the source's draw."
    },
    {
      "what": "Stay/drop choices and bids are public once revealed",
      "why": "The source reveals bids together, and paying the fee or receiving the drop payment is visible. Who placed which card stays secret."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player infers others' cards from the public discard, the reveals and their own removed card. They bluff in talk and weigh the 1-mouse fee against the 2-mouse drop payment. They also use the fewer-mice tie-break and the dog rule when sizing a bid."
    }
  ],
  "simplifications": [
    {
      "what": "The shuffle is done by drawing the sack cards at random into a new order",
      "why": "The engine shuffles by random draws from a list."
    },
    {
      "what": "The bank of mice is not tracked",
      "why": "It is unlimited, so only player mice change."
    },
    {
      "what": "A draw is represented as a shared win among the players tied at the top",
      "why": "The engine has no separate draw outcome."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: mice, cat_points, stayed, bid; table: round, start_seat, revealed_cards, discard, winner_seat, sack_value.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "R1 setup: each hand starts from the 9-card set, so 8 remain after the one random removal",
   "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "expect": {"lens": {"players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}, "4": {"hand": 8}}}}},

  {"name": "R2 setup: exactly one card is removed from each hand, leaving 8 (3 players, the removed card itself is random)",
   "rule": "R2", "players": 3, "seed": 2, "rounds": 0,
   "expect": {"lens": {"players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}}}},

  {"name": "R3 setup: 15 mice and 0 cat points each",
   "rule": "R3", "players": 4, "seed": 3, "rounds": 0,
   "expect": {"players": {"1": {"mice": 15, "cat_points": 0}, "2": {"mice": 15, "cat_points": 0},
                          "3": {"mice": 15, "cat_points": 0}, "4": {"mice": 15, "cat_points": 0}},
              "game": {"round": 0}}},

  {"name": "R4 start seat is 2 in round 2 with 4 players",
   "rule": "R4", "players": 4, "seed": 4, "rounds": 1,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"game": {"round": 2, "start_seat": 2}}},

  {"name": "R4 start seat wraps: round 5 with 3 players is seat 2",
   "rule": "R4", "players": 3, "seed": 5, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"round": 5, "start_seat": 2}}},

  {"name": "R5 each player places one card that leaves the hand (the card itself depends on the random removal)",
   "rule": "R5", "players": 4, "seed": 6, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"lens": {"players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}, "4": {"hand": 7}},
                       "game": {"discard": 4}}}},

  {"name": "R6 with 3 players the first reveal shows 1 card (2 shown in total after the second reveal)",
   "rule": "R6", "players": 3, "seed": 7, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["cat_3", "cat_3"]}, "lens": {"game": {"revealed_cards": 2}}}},

  {"name": "R6 with 4 players the first reveal shows 2 cards (3 shown in total after the second reveal)",
   "rule": "R6", "players": 4, "seed": 8, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_5"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_5"]}, "4": {"hand": ["cat_5"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["cat_5", "cat_5", "cat_5"]}, "lens": {"game": {"revealed_cards": 3}}}},

  {"name": "R7 the talk step happens and the round carries on to stay-or-drop and payment",
   "rule": "R7", "players": 3, "seed": 9, "rounds": 1,
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"round": 1},
              "players": {"1": {"mice": 17}, "2": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "R8 a player with 1 mouse may only drop",
   "rule": "R8", "players": 3, "seed": 10, "rounds": 1,
   "given": {"players": {"1": {"mice": 1, "hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 3, "stayed": false}},
              "offered": [{"seat": 1, "option": "DROP"}],
              "not_offered": [{"seat": 1, "option": "STAY"}]}},

  {"name": "R9 staying costs 1 mouse: losing stayer 15 -> 14, winner 15 - 1 - 5 = 9",
   "rule": "R9", "players": 3, "seed": 11, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 3}],
   "expect": {"players": {"1": {"mice": 9, "stayed": true, "bid": 5, "cat_points": 8},
                          "2": {"mice": 14, "stayed": true, "bid": 3, "cat_points": 0},
                          "3": {"mice": 17, "stayed": false}},
              "game": {"winner_seat": 1, "sack_value": 8}}},

  {"name": "R10 dropping gives 2 mice and no bid is asked",
   "rule": "R10", "players": 3, "seed": 12, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 17, "stayed": false, "bid": 0, "cat_points": 0},
                          "3": {"mice": 17, "stayed": false, "bid": 0, "cat_points": 0}},
              "game": {"winner_seat": 1},
              "not_offered": [{"seat": 2, "option": 1}, {"seat": 3, "option": 1}]}},

  {"name": "R11 a second reveal adds one card: 5 players show 2 + 1 = 3",
   "rule": "R11", "players": 5, "seed": 13, "rounds": 1,
   "given": {"players": {"1": {"hand": ["dog"]}, "2": {"hand": ["dog"]}, "3": {"hand": ["dog"]}, "4": {"hand": ["dog"]}, "5": {"hand": ["dog"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"},
             {"seat": 5, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["dog", "dog", "dog"]}, "lens": {"game": {"revealed_cards": 3}}}},

  {"name": "R12 the bid range is 1 to mice after the fee (5 mice -> up to 4)",
   "rule": "R12", "players": 3, "seed": 14, "rounds": 1,
   "given": {"players": {"1": {"mice": 5, "hand": ["cat_3"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 4},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 0, "bid": 4, "cat_points": 9}},
              "game": {"winner_seat": 1, "sack_value": 9},
              "offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 1}],
              "not_offered": [{"seat": 1, "option": 5}]}},

  {"name": "R13 the highest bid wins the sack",
   "rule": "R13", "players": 3, "seed": 15, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_8"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 6}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 8, "cat_points": 11}},
              "game": {"winner_seat": 2, "sack_value": 11}}},

  {"name": "R14 tied bids: the stayer with fewer mice wins",
   "rule": "R14", "players": 3, "seed": 16, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_5"]}, "2": {"mice": 10, "hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 5, "cat_points": 10}},
              "game": {"winner_seat": 2, "sack_value": 10}}},

  {"name": "R15 tied bids and mice: the first in seat order from start seat 2 wins (seat 3 beats seat 1)",
   "rule": "R15", "players": 3, "seed": 17, "rounds": 1,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 3, "options_include": "STAY"},
             {"seat": 2, "options_include": "DROP"},
             {"seat": 1, "options_include": 4}, {"seat": 3, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "3": {"mice": 10, "cat_points": 6}, "2": {"mice": 17}},
              "game": {"start_seat": 2, "winner_seat": 3, "sack_value": 6}}},

  {"name": "R16 nobody stays: no winner, no points and the sack is discarded",
   "rule": "R16", "players": 3, "seed": 18, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_11"]}, "3": {"hand": ["cat_8"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 17, "cat_points": 0}, "2": {"mice": 17, "cat_points": 0}, "3": {"mice": 17, "cat_points": 0}},
              "game": {"winner_seat": 0},
              "lens": {"game": {"discard": 3}}}},

  {"name": "R17 a single stayer wins and pays the bid: 15 - 1 - 2 = 12",
   "rule": "R17", "players": 4, "seed": 19, "rounds": 1,
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 2, "options_include": "STAY"}, {"seat": 2, "options_include": 2},
             {"seat": 1, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"},
             {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 12, "cat_points": 5, "bid": 2}},
              "game": {"winner_seat": 2, "sack_value": 5}}},

  {"name": "R18 sack value is the sum of the cats, rabbit worth 0: 15 + 3 = 18",
   "rule": "R18", "players": 3, "seed": 20, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 18}},
              "game": {"sack_value": 18, "winner_seat": 1}}},

  {"name": "R19 one dog cancels the top cat: cat_15 + cat_3 + dog + rabbit = 3",
   "rule": "R19", "players": 4, "seed": 21, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["dog"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"},
             {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 3}},
              "game": {"sack_value": 3, "winner_seat": 1}}},

  {"name": "R19 one dog with only negative cats removes the highest one: -8 + -5 with -5 removed = -8",
   "rule": "R19", "players": 3, "seed": 22, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_-8"]}, "2": {"hand": ["cat_-5"]}, "3": {"hand": ["dog"]}}},
   "rules": [{"seat": 3, "options_include": "STAY"}, {"seat": 3, "options_include": 1},
             {"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}],
   "expect": {"players": {"3": {"mice": 13, "cat_points": -8}},
              "game": {"sack_value": -8, "winner_seat": 3}}},

  {"name": "R20 two dogs have no effect: cat_15 + dog + dog = 15",
   "rule": "R20", "players": 3, "seed": 23, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["dog"]}, "3": {"hand": ["dog"]}}},
   "rules": [{"seat": 2, "options_include": "STAY"}, {"seat": 2, "options_include": 3},
             {"seat": 1, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 11, "cat_points": 15}},
              "game": {"sack_value": 15, "winner_seat": 2}}},

  {"name": "R21 the winner pays the bid and takes a negative sack value: -8 + -5 = -13",
   "rule": "R21", "players": 3, "seed": 24, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_-8"]}, "2": {"hand": ["cat_-5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 3},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 11, "cat_points": -13}},
              "game": {"sack_value": -13, "winner_seat": 1}}},

  {"name": "R22 a losing stayer keeps the fee paid and gets no points",
   "rule": "R22", "players": 3, "seed": 25, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_11"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 7}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 7, "cat_points": 26}},
              "game": {"winner_seat": 2, "sack_value": 26}}},

  {"name": "R23 all sack cards join the public discard (1 earlier card + 3 = 4)",
   "rule": "R23", "players": 3, "seed": 26, "rounds": 1,
   "given": {"game": {"discard": ["cat_8"]},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"lens": {"game": {"discard": 4}}}},

  {"name": "R24 the game ends after round 8",
   "rule": "R24", "players": 3, "seed": 27,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 20, "hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 1,
              "standings": {"1": 22000, "2": 17000, "3": 17000},
              "game": {"round": 8},
              "players": {"1": {"mice": 22}, "2": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "R25 equal totals: the higher cat points wins",
   "rule": "R25", "players": 3, "seed": 28,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 10, "cat_points": 5, "hand": ["rabbit"]},
                         "2": {"mice": 15, "cat_points": 0, "hand": ["rabbit"]},
                         "3": {"mice": 3, "cat_points": 0, "hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 1, "standings": {"1": 17005, "2": 17000, "3": 5000}}},

  {"name": "R25 equal totals and equal cat points share the win",
   "rule": "R25", "players": 3, "seed": 29,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 12, "cat_points": 4, "hand": ["rabbit"]},
                         "2": {"mice": 12, "cat_points": 4, "hand": ["rabbit"]},
                         "3": {"mice": 5, "cat_points": 0, "hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": [1, 2], "standings": {"1": 18004, "2": 18004, "3": 7000}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "R1 setup: each hand starts from the 9-card set, so after the one random removal and one placed card 7 remain",
   "rule": "R1", "players": 4, "seed": 1, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"lens": {"players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}, "4": {"hand": 7}}}}},

  {"name": "R2 setup: exactly one card is removed from each hand, so 7 remain after one placed card (3 players, the removed card itself is random)",
   "rule": "R2", "players": 3, "seed": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"lens": {"players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}}}}},

  {"name": "R3 setup: 15 mice and 0 cat points each, shown by everyone dropping (15 + 2 = 17, still 0 points)",
   "rule": "R3", "players": 4, "seed": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 17, "cat_points": 0}, "2": {"mice": 17, "cat_points": 0},
                          "3": {"mice": 17, "cat_points": 0}, "4": {"mice": 17, "cat_points": 0}},
              "game": {"round": 1}}},

  {"name": "R4 start seat is 2 in round 2 with 4 players",
   "rule": "R4", "players": 4, "seed": 4, "rounds": 1,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"game": {"round": 2, "start_seat": 2}}},

  {"name": "R4 start seat wraps: round 5 with 3 players is seat 2",
   "rule": "R4", "players": 3, "seed": 5, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"round": 5, "start_seat": 2}}},

  {"name": "R5 each player places one card that leaves the hand (the card itself depends on the random removal)",
   "rule": "R5", "players": 4, "seed": 6, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"lens": {"players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}, "4": {"hand": 7}},
                       "game": {"discard": 4}}}},

  {"name": "R6 with 3 players the first reveal shows 1 card (2 shown in total after the second reveal)",
   "rule": "R6", "players": 3, "seed": 7, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["cat_3", "cat_3"]}, "lens": {"game": {"revealed_cards": 2}}}},

  {"name": "R6 with 4 players the first reveal shows 2 cards (3 shown in total after the second reveal)",
   "rule": "R6", "players": 4, "seed": 8, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_5"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_5"]}, "4": {"hand": ["cat_5"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["cat_5", "cat_5", "cat_5"]}, "lens": {"game": {"revealed_cards": 3}}}},

  {"name": "R7 the talk step happens and the round carries on to stay-or-drop and payment",
   "rule": "R7", "players": 3, "seed": 9, "rounds": 1,
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"game": {"round": 1},
              "players": {"1": {"mice": 17}, "2": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "R8 a player with 1 mouse may only drop",
   "rule": "R8", "players": 3, "seed": 10, "rounds": 1,
   "given": {"players": {"1": {"mice": 1, "hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 3, "stayed": false}},
              "offered": [{"seat": 1, "option": "DROP"}],
              "not_offered": [{"seat": 1, "option": "STAY"}]}},

  {"name": "R9 staying costs 1 mouse: losing stayer 15 -> 14, winner 15 - 1 - 5 = 9",
   "rule": "R9", "players": 3, "seed": 11, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 3}],
   "expect": {"players": {"1": {"mice": 9, "stayed": true, "bid": 5, "cat_points": 8},
                          "2": {"mice": 14, "stayed": true, "bid": 3, "cat_points": 0},
                          "3": {"mice": 17, "stayed": false}},
              "game": {"winner_seat": 1, "sack_value": 8}}},

  {"name": "R10 dropping gives 2 mice and no bid is asked",
   "rule": "R10", "players": 3, "seed": 12, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 2},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 17, "stayed": false, "bid": 0, "cat_points": 0},
                          "3": {"mice": 17, "stayed": false, "bid": 0, "cat_points": 0}},
              "game": {"winner_seat": 1},
              "not_offered": [{"seat": 2, "option": 1}, {"seat": 3, "option": 1}]}},

  {"name": "R11 a second reveal adds one card: 5 players show 2 + 1 = 3",
   "rule": "R11", "players": 5, "seed": 13, "rounds": 1,
   "given": {"players": {"1": {"hand": ["dog"]}, "2": {"hand": ["dog"]}, "3": {"hand": ["dog"]}, "4": {"hand": ["dog"]}, "5": {"hand": ["dog"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}, {"seat": 4, "options_include": "DROP"},
             {"seat": 5, "options_include": "DROP"}],
   "expect": {"game": {"revealed_cards": ["dog", "dog", "dog"]}, "lens": {"game": {"revealed_cards": 3}}}},

  {"name": "R12 the bid range is 1 to mice after the fee (5 mice -> up to 4)",
   "rule": "R12", "players": 3, "seed": 14, "rounds": 1,
   "given": {"players": {"1": {"mice": 5, "hand": ["cat_3"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 4},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 0, "bid": 4, "cat_points": 9}},
              "game": {"winner_seat": 1, "sack_value": 9},
              "offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 1}],
              "not_offered": [{"seat": 1, "option": 5}]}},

  {"name": "R13 the highest bid wins the sack",
   "rule": "R13", "players": 3, "seed": 15, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_8"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 6}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 8, "cat_points": 11}},
              "game": {"winner_seat": 2, "sack_value": 11}}},

  {"name": "R14 tied bids: the stayer with fewer mice wins",
   "rule": "R14", "players": 3, "seed": 16, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_5"]}, "2": {"mice": 10, "hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 5, "cat_points": 10}},
              "game": {"winner_seat": 2, "sack_value": 10}}},

  {"name": "R15 tied bids and mice: the first in seat order from start seat 2 wins (seat 3 beats seat 1)",
   "rule": "R15", "players": 3, "seed": 17, "rounds": 1,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["cat_3"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 3, "options_include": "STAY"},
             {"seat": 2, "options_include": "DROP"},
             {"seat": 1, "options_include": 4}, {"seat": 3, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "3": {"mice": 10, "cat_points": 6}, "2": {"mice": 17}},
              "game": {"start_seat": 2, "winner_seat": 3, "sack_value": 6}}},

  {"name": "R16 nobody stays: no winner, no points and the sack is discarded",
   "rule": "R16", "players": 3, "seed": 18, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_11"]}, "3": {"hand": ["cat_8"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 17, "cat_points": 0}, "2": {"mice": 17, "cat_points": 0}, "3": {"mice": 17, "cat_points": 0}},
              "game": {"winner_seat": 0},
              "lens": {"game": {"discard": 3}}}},

  {"name": "R17 a single stayer wins and pays the bid: 15 - 1 - 2 = 12",
   "rule": "R17", "players": 4, "seed": 19, "rounds": 1,
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["rabbit"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 2, "options_include": "STAY"}, {"seat": 2, "options_include": 2},
             {"seat": 1, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"},
             {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 12, "cat_points": 5, "bid": 2}},
              "game": {"winner_seat": 2, "sack_value": 5}}},

  {"name": "R18 sack value is the sum of the cats, rabbit worth 0: 15 + 3 = 18",
   "rule": "R18", "players": 3, "seed": 20, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 18}},
              "game": {"sack_value": 18, "winner_seat": 1}}},

  {"name": "R19 one dog cancels the top cat: cat_15 + cat_3 + dog + rabbit = 3",
   "rule": "R19", "players": 4, "seed": 21, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_3"]}, "3": {"hand": ["dog"]}, "4": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 1},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"},
             {"seat": 4, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 3}},
              "game": {"sack_value": 3, "winner_seat": 1}}},

  {"name": "R19 one dog with only negative cats removes the highest one: -8 + -5 with -5 removed = -8",
   "rule": "R19", "players": 3, "seed": 22, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_-8"]}, "2": {"hand": ["cat_-5"]}, "3": {"hand": ["dog"]}}},
   "rules": [{"seat": 3, "options_include": "STAY"}, {"seat": 3, "options_include": 1},
             {"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"}],
   "expect": {"players": {"3": {"mice": 13, "cat_points": -8}},
              "game": {"sack_value": -8, "winner_seat": 3}}},

  {"name": "R20 two dogs have no effect: cat_15 + dog + dog = 15",
   "rule": "R20", "players": 3, "seed": 23, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["dog"]}, "3": {"hand": ["dog"]}}},
   "rules": [{"seat": 2, "options_include": "STAY"}, {"seat": 2, "options_include": 3},
             {"seat": 1, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"2": {"mice": 11, "cat_points": 15}},
              "game": {"sack_value": 15, "winner_seat": 2}}},

  {"name": "R21 the winner pays the bid and takes a negative sack value: -8 + -5 = -13",
   "rule": "R21", "players": 3, "seed": 24, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_-8"]}, "2": {"hand": ["cat_-5"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 1, "options_include": 3},
             {"seat": 2, "options_include": "DROP"}, {"seat": 3, "options_include": "DROP"}],
   "expect": {"players": {"1": {"mice": 11, "cat_points": -13}},
              "game": {"sack_value": -13, "winner_seat": 1}}},

  {"name": "R22 a losing stayer keeps the fee paid and gets no points",
   "rule": "R22", "players": 3, "seed": 25, "rounds": 1,
   "given": {"players": {"1": {"hand": ["cat_15"]}, "2": {"hand": ["cat_11"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "STAY"}, {"seat": 2, "options_include": "STAY"},
             {"seat": 3, "options_include": "DROP"},
             {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 7}],
   "expect": {"players": {"1": {"mice": 14, "cat_points": 0}, "2": {"mice": 7, "cat_points": 26}},
              "game": {"winner_seat": 2, "sack_value": 26}}},

  {"name": "R23 all sack cards join the public discard (1 earlier card + 3 = 4)",
   "rule": "R23", "players": 3, "seed": 26, "rounds": 1,
   "given": {"game": {"discard": ["cat_8"]},
             "players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"lens": {"game": {"discard": 4}}}},

  {"name": "R24 the game ends after round 8",
   "rule": "R24", "players": 3, "seed": 27,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 20, "hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 1,
              "standings": {"1": 22000, "2": 17000, "3": 17000},
              "game": {"round": 8},
              "players": {"1": {"mice": 22}, "2": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "R25 equal totals: the higher cat points wins",
   "rule": "R25", "players": 3, "seed": 28,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 10, "cat_points": 5, "hand": ["rabbit"]},
                         "2": {"mice": 15, "cat_points": 0, "hand": ["rabbit"]},
                         "3": {"mice": 3, "cat_points": 0, "hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": 1, "standings": {"1": 17005, "2": 17000, "3": 5000}}},

  {"name": "R25 equal totals and equal cat points share the win",
   "rule": "R25", "players": 3, "seed": 29,
   "given": {"game": {"round": 7},
             "players": {"1": {"mice": 12, "cat_points": 4, "hand": ["rabbit"]},
                         "2": {"mice": 12, "cat_points": 4, "hand": ["rabbit"]},
                         "3": {"mice": 5, "cat_points": 0, "hand": ["rabbit"]}}},
   "rules": [{"seat": 1, "options_include": "DROP"}, {"seat": 2, "options_include": "DROP"},
             {"seat": 3, "options_include": "DROP"}],
   "expect": {"winner": [1, 2], "standings": {"1": 18004, "2": 18004, "3": 7000}}}
]
````
