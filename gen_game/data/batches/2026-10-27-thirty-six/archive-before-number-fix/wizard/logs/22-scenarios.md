# 22 scenarios

- time: 2026-10-27T18:20:07+00:00 (116.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 c14bff829014efb0, reply sha256 73c25d6f6ff3dabb

## Sent

````
SPEC:
{
  "name": "Three-Card Wizard",
  "summary": "A three-player trick-taking game of 12 hands with 3 tricks each: players bid exactly how many tricks they will take, then play Wizards, Jesters and suited cards to hit that number.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 28,
    "suits": 3,
    "ranks_per_suit": 8,
    "wizards": 2,
    "jesters": 2,
    "hands": 12,
    "tricks_per_hand": 3,
    "rounds": 36,
    "cards_dealt_per_player": 3,
    "trump_card_position": 10,
    "cards_left_in_deck_after_deal": 18,
    "bid_min": 0,
    "bid_max": 3,
    "default_bid": 1,
    "wizard_strength": 100,
    "trump_strength_bonus": 20,
    "jester_or_offsuit_strength": 0,
    "initial_best_value": -1,
    "exact_bid_bonus": 20,
    "points_per_trick_when_exact": 10,
    "penalty_per_trick_off": 10,
    "starting_score": 0,
    "starting_hand_number": 0,
    "starting_trick_in_hand": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards this player holds in the current hand. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of tricks bid this hand. It is collected by a simultaneous poll and then announced, and it is reset to 0 after scoring.",
        "observable": true
      },
      {
        "key": "tricks_taken",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won so far in the current hand.",
        "observable": true
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this player played to the current trick.",
        "observable": false
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The legal cards this player may play now, in hand order.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative score.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "R1",
          "R2",
          "R3",
          "R4",
          "R5",
          "R6",
          "R7",
          "R8",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "B6",
          "B7",
          "B8",
          "G1",
          "G2",
          "G3",
          "G4",
          "G5",
          "G6",
          "G7",
          "G8",
          "W1",
          "W2",
          "J1",
          "J2"
        ],
        "meaning": "The undealt cards, refilled with all 28 cards and shuffled at the start of each hand.",
        "observable": false
      },
      {
        "key": "trump_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The face-up 10th card of the shuffled deck.",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "The suit letter of trump_card, or 'none' if it is a Wizard or a Jester.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current hand, 1 to 12.",
        "observable": true
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current trick within the hand, 1 to 3.",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "The suit led in this trick, or 'none'.",
        "observable": false
      },
      {
        "key": "wizard_played",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether a Wizard has been played in this trick.",
        "observable": false
      },
      {
        "key": "best_value",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The strength of the currently winning card in the trick.",
        "observable": false
      },
      {
        "key": "best_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat currently winning the trick.",
        "observable": false
      },
      {
        "key": "played_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards played to the current trick, in order.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are filled, and every score is set to 0.",
    "hand_number is set to 0, trick_in_hand to 1 and every bid to 0.",
    "The deck list holds the 28 cards R1-R8, B1-B8, G1-G8, W1, W2, J1 and J2."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand = 1: add 1 to hand_number; refill deck with all 28 cards and shuffle it; empty every hand and set every tricks_taken to 0; draw 3 cards at random from deck into seat 1's hand, then 3 into seat 2's, then 3 into seat 3's (each removed from deck); remove the next random card from deck and set it as trump_card (18 cards stay in deck); set trump_suit to the suit letter of trump_card if it is suited, otherwise 'none'; set leader = ((hand_number - 1) mod 3) + 1."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand = 1: each player sees their own hand; trump_card, trump_suit, hand_number and leader are announced to all."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of 0, 1, 2, 3",
      "effect": "When trick_in_hand = 1: each player's bid is set to their answer exactly (a 0 stays 0); a missing or invalid answer sets that bid to 1. All bids are then announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Every round: led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0, played_cards = []."
    },
    {
      "action": "update",
      "who": "seat leader",
      "answer": null,
      "effect": "Build the leader's offer from their hand, in hand order: if led_suit != 'none' and they hold a card of led_suit, the offer is those cards plus any W or J cards they hold; otherwise it is the whole hand."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "one card from their offer",
      "effect": "The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."
    },
    {
      "action": "update",
      "who": "seat leader",
      "answer": null,
      "effect": "Resolve the card. If it is suited and led_suit = 'none' and wizard_played = false, set led_suit to its suit. If it is a Wizard, set wizard_played = true. Strength is 100 for a Wizard, 20 + rank for a suit equal to trump_suit, rank for a suit equal to led_suit, and 0 otherwise. If strength > best_value, set best_value = strength and best_seat = this seat. The played card is announced."
    },
    {
      "action": "update",
      "who": "seat (leader mod 3) + 1",
      "answer": null,
      "effect": "Build this player's offer with the same rule as above."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 3) + 1",
      "answer": "one card from their offer",
      "effect": "The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."
    },
    {
      "action": "update",
      "who": "seat (leader mod 3) + 1",
      "answer": null,
      "effect": "Resolve the card with the same led-suit and strength rule as above, then announce it."
    },
    {
      "action": "update",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": null,
      "effect": "Build this player's offer with the same rule as above."
    },
    {
      "action": "ask",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": "one card from their offer",
      "effect": "The player sees played_cards. The chosen card is removed from hand, set as played_card and appended to played_cards; a missing or invalid answer plays offer[0]."
    },
    {
      "action": "update",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": null,
      "effect": "Resolve the card with the same led-suit and strength rule as above, then announce it."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Add 1 to tricks_taken of best_seat; announce best_seat as the trick winner; set leader = best_seat."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand = 3: for each player, if tricks_taken = bid, add 20 + 10 * tricks_taken to score; otherwise subtract 10 * |tricks_taken - bid|. Announce all scores, set every bid to 0 and set trick_in_hand = 1. Otherwise (trick_in_hand < 3) add 1 to trick_in_hand."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_number >= 12 and trick_in_hand = 1 (hand 12 has just been scored); otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "game.hand_number >= 12 and game.trick_in_hand = 1",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final score after hand 12. The highest score wins, and players tied at the top share the win (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When trick_in_hand = 1 at the start of a round, then hand_number increases by 1, the deck is refilled to 28 cards and shuffled, every tricks_taken becomes 0, and each seat receives exactly 3 cards in its hand."
    },
    {
      "id": "R2",
      "text": "When a hand is dealt, then one further card is removed from the deck and becomes trump_card, leaving exactly 18 cards in the deck."
    },
    {
      "id": "R3",
      "text": "When trump_card is suited (for example G5), then trump_suit is its letter (G); when trump_card is W1, W2, J1 or J2, then trump_suit is 'none'."
    },
    {
      "id": "R4",
      "text": "When a hand begins, then leader = ((hand_number - 1) mod 3) + 1: seat 1 leads in hands 1, 4, 7 and 10, seat 2 in hands 2, 5, 8 and 11, and seat 3 in hands 3, 6, 9 and 12."
    },
    {
      "id": "R5",
      "text": "When trick_in_hand = 1, then all three players bid at once from {0, 1, 2, 3}, and each bid is stored exactly as given (a 0 stays 0)."
    },
    {
      "id": "R6",
      "text": "When a bid answer is missing or not in {0, 1, 2, 3}, then that bid is 1."
    },
    {
      "id": "R7",
      "text": "When bidding is done, then all bids are announced, and they need not sum to 3."
    },
    {
      "id": "R8",
      "text": "When a trick starts, then led_suit = 'none', wizard_played = false, best_value = -1, best_seat = 0 and played_cards is empty."
    },
    {
      "id": "R9",
      "text": "When a trick is played, then the order is leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1."
    },
    {
      "id": "R10",
      "text": "When led_suit is not 'none' and the player holds a card of led_suit, then the offer is their led-suit cards plus any Wizards and Jesters they hold, in hand order; otherwise the offer is the whole hand."
    },
    {
      "id": "R11",
      "text": "When a play answer is missing or not in the offer, then the first card of the offer is played."
    },
    {
      "id": "R12",
      "text": "When a card is played, then it is removed from the hand, recorded as played_card and appended to played_cards."
    },
    {
      "id": "R13",
      "text": "When a suited card is played while led_suit = 'none' and wizard_played = false, then led_suit becomes its suit."
    },
    {
      "id": "R14",
      "text": "When a Wizard is played, then wizard_played = true and led_suit does not change; when a Jester is played, then led_suit does not change."
    },
    {
      "id": "R15",
      "text": "When a card is played, then its strength is 100 for a Wizard, 20 + rank for a trump-suit card, its rank for a led-suit card, and 0 for a Jester or an off-suit non-trump card."
    },
    {
      "id": "R16",
      "text": "When a card's strength is strictly greater than best_value, then best_value becomes that strength and best_seat becomes that seat; equal strength does not take the lead, so the first Wizard wins and three Jesters are won by the first Jester."
    },
    {
      "id": "R17",
      "text": "When a trick ends, then best_seat's tricks_taken increases by 1 and leader becomes best_seat."
    },
    {
      "id": "R18",
      "text": "When trick_in_hand = 3 at the end of a trick and a player's tricks_taken equals their bid, then they gain 20 + 10 * tricks_taken (for example bid 0 and 0 tricks gains 20, bid 2 and 2 tricks gains 40)."
    },
    {
      "id": "R19",
      "text": "When trick_in_hand = 3 at the end of a trick and a player's tricks_taken differs from their bid, then they lose 10 * |tricks_taken - bid| (for example bid 3 and 1 trick loses 20)."
    },
    {
      "id": "R20",
      "text": "When a hand is scored, then all scores are announced, every bid is set to 0 and trick_in_hand becomes 1; after tricks 1 and 2 of a hand, trick_in_hand increases by 1 instead."
    },
    {
      "id": "R21",
      "text": "When hand 12 has been scored (after round 36), then the game ends and the highest score wins, with players tied at the top sharing the win."
    }
  ],
  "offers": [
    {
      "question": "Bid for this hand (poll, only when trick_in_hand = 1)",
      "who": "seats 1, 2 and 3",
      "options": "every seat: 0, 1, 2, 3"
    },
    {
      "question": "Card to play to the trick",
      "who": "the leader, then (leader mod 3) + 1, then ((leader + 1) mod 3) + 1",
      "options": "the leader, or any later player when led_suit is 'none' (a Wizard was led, or only Wizards and Jesters have been played so far): every card in their hand; a later player when led_suit is set and they hold a card of led_suit: their led-suit cards plus any W1, W2, J1, J2 they hold; a later player when led_suit is set and they hold none of it: every card in their hand"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed 3 seats. The deal (9 cards plus the 10th as trump), the leader rotation mod 3 and the play order all assume three players. The game is about predicting tricks and managing the trick count against two rivals whose bids are public."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player bids from card strength and the trump suit, then plays to hit the bid exactly: dumping Jesters or low cards to avoid tricks, spending Wizards or trumps to take them, and reading the opponents' public bids to disrupt them. A thoughtless player bids blindly and plays cards in any order."
    },
    {
      "what": "No talk step",
      "why": "The source has no table talk, and adding it would add a mechanic."
    },
    {
      "what": "Shuffle and deal written as random draws from the deck list",
      "why": "The engine shuffles by drawing at random; drawing 9 cards and then one more for trump matches 'top 3 to each seat, the 10th is trump'."
    },
    {
      "what": "The bid and tricks_taken are public attributes",
      "why": "The rules announce bids after the simultaneous poll and announce each trick winner, so both are open information. The poll keeps bids secret until all are in."
    }
  ],
  "simplifications": [
    {
      "what": "The source's 'draw' when two or three players tie for the top score becomes a shared win",
      "why": "The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome."
    },
    {
      "what": "Each of the three plays is written as three steps (build offer, ask, resolve) addressed to the computed seat",
      "why": "The engine runs a flat list of steps; play order is expressed by naming the seat from leader."
    },
    {
      "what": "Hand-start steps carry a 'when trick_in_hand = 1' condition, and scoring carries 'when trick_in_hand = 3'",
      "why": "Single steps may be conditional, so no block substitution is needed."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bid, tricks_taken, score; table: trump_card, hand_number.
````

## Reply

````
[
  {"name": "Hand start: hand_number goes up, each seat is dealt 3 cards (2 left after trick 1), the deck holds 18. Chance: the cards are not asserted",
   "rule": "R1", "players": 3, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"hand_number": 3, "trick_in_hand": 1}},
   "rules": [],
   "expect": {"game": {"hand_number": 4},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "Trump card is taken from the deck after the deal, leaving 18 cards. Chance: the trump card itself is not asserted",
   "rule": "R2", "players": 3, "seed": 2, "rounds": 1, "default": "first",
   "rules": [],
   "expect": {"game": {"hand_number": 1}, "lens": {"game": {"deck": 18}}}},

  {"name": "Suited trump G5 makes G the trump suit: G1 from a void seat beats a led R8",
   "rule": "R3", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "G5", "trump_suit": "G"},
             "players": {"1": {"hand": ["R8"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["G1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R7"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "Wizard trump card means no trump suit: an off-suit G8 does not beat a led R1",
   "rule": "R3", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["G8"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["B8"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

  {"name": "A new hand begins after hand 1 (hand 2). Chance: the leader cannot be observed with a random deal, so only the hand start is asserted",
   "rule": "R4", "players": 3, "seed": 3, "rounds": 1, "default": "first",
   "given": {"game": {"hand_number": 1, "trick_in_hand": 1}},
   "rules": [],
   "expect": {"game": {"hand_number": 2},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "Bids are stored exactly as given, a 0 stays 0",
   "rule": "R5", "players": 3, "seed": 4, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": "0"},
             {"seat": 2, "options_include": "3"},
             {"seat": 3, "options_include": "2"}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 3}, "3": {"bid": 2}}}},

  {"name": "An invalid bid answer becomes a bid of 1",
   "rule": "R6", "players": 3, "seed": 5, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": "0", "answer": "7"},
             {"seat": 2, "options_include": "0"},
             {"seat": 3, "options_include": "0"}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 0}}}},

  {"name": "Bids need not sum to 3: all three seats bid 3",
   "rule": "R7", "players": 3, "seed": 6, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": "3"},
             {"seat": 2, "options_include": "3"},
             {"seat": 3, "options_include": "3"}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 3}, "3": {"bid": 3}}}},

  {"name": "A trick starts fresh: a stale best_seat 3 and best_value 100 do not carry over",
   "rule": "R8", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "G4", "trump_suit": "G",
                      "best_value": 100, "best_seat": 3, "wizard_played": true, "led_suit": "B"},
             "players": {"1": {"hand": ["R5", "B1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R3", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R2", "B3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"},
             {"seat": 2, "options_include": "R3"},
             {"seat": 3, "options_include": "R2"}],
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}}},

  {"name": "Play order with leader 2 is 2, 3, 1: J1, then B5 sets the led suit, then R7 is off-suit, so seat 3 wins",
   "rule": "R9", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 2, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R7"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["J1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["B5"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}}},

  {"name": "Follow suit: a seat holding the led suit is offered that suit plus Wizards, and a void seat is offered its whole hand",
   "rule": "R10", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "J1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R2", "B8", "W1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G3", "B4"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"},
             {"seat": 2, "options_include": "R2"},
             {"seat": 3, "options_include": "B4"}],
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
              "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "W1"},
                          {"seat": 3, "option": "G3"}, {"seat": 3, "option": "B4"},
                          {"seat": 1, "option": "G1"}],
              "not_offered": [{"seat": 2, "option": "B8"}]}},

  {"name": "An invalid card answer plays offer[0] (R2), which beats the led R1",
   "rule": "R11", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B8", "R2", "J1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G1"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 2, "options_include": "R2", "answer": "B8"}],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}},
              "lens": {"players": {"2": {"hand": 2}}}}},

  {"name": "A played card leaves the hand: 3 cards become 2",
   "rule": "R12", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "G4", "trump_suit": "G"},
             "players": {"1": {"hand": ["R5", "R6", "B1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R3", "B2", "B5"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R2", "B3", "B6"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "After a Jester lead, the first suited card (B3) sets the led suit and wins over an off-suit R7",
   "rule": "R13", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["J1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B3"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R7"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "A Wizard lead leaves the led suit unset: the third seat is offered its whole hand after R2, and the Wizard wins",
   "rule": "R14", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["B5", "R8"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 3, "options_include": "B5"}],
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
              "offered": [{"seat": 3, "option": "B5"}, {"seat": 3, "option": "R8"}]}},

  {"name": "Strength: a trump G1 (21) beats the led R8 (8) and R7",
   "rule": "R15", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "G4", "trump_suit": "G"},
             "players": {"1": {"hand": ["R8"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["G1", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R7"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 2, "options_include": "G1"}],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "Equal strength does not take the lead: the first Wizard wins over the second",
   "rule": "R16", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "J1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["W1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["W2"], "bid": 1, "tricks_taken": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "The trick winner leads the next trick: seat 3 wins trick 2, leads B5 in trick 3 and wins again; then scoring",
   "rule": "R17", "players": 3, "rounds": 2, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1", "R7"], "bid": 0, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R2", "J1"], "bid": 0, "tricks_taken": 0, "score": 0},
                         "3": {"hand": ["R5", "B5"], "bid": 2, "tricks_taken": 0, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "R1"},
             {"seat": 2, "options_include": "R2"},
             {"seat": 3, "options_include": "R5"}],
   "expect": {"players": {"1": {"tricks_taken": 0, "score": 20}, "2": {"tricks_taken": 0, "score": 20},
                          "3": {"tricks_taken": 2, "score": 40}}}},

  {"name": "Exact bids score 20 + 10 per trick: bid 1 and 1 trick +30, bid 0 and 0 +20, bid 2 and 2 +40",
   "rule": "R18", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 50},
                         "2": {"hand": ["R2"], "bid": 0, "tricks_taken": 0, "score": 10},
                         "3": {"hand": ["B3"], "bid": 2, "tricks_taken": 2, "score": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 1, "score": 80, "bid": 0},
                          "2": {"tricks_taken": 0, "score": 30, "bid": 0},
                          "3": {"tricks_taken": 2, "score": 40, "bid": 0}}}},

  {"name": "Missed bids lose 10 per trick off: bid 3 and 1 trick -20, bid 2 and 1 -10, bid 0 and 1 -10",
   "rule": "R19", "players": 3, "rounds": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1"], "bid": 3, "tricks_taken": 0, "score": 30},
                         "2": {"hand": ["R2"], "bid": 2, "tricks_taken": 1, "score": 30},
                         "3": {"hand": ["B3"], "bid": 0, "tricks_taken": 1, "score": 30}}},
   "rules": [],
   "expect": {"players": {"1": {"tricks_taken": 1, "score": 10},
                          "2": {"tricks_taken": 1, "score": 20},
                          "3": {"tricks_taken": 1, "score": 20}}}},

  {"name": "After scoring, bids reset and the next round deals a new hand with a new bid poll (no second scoring)",
   "rule": "R20", "players": 3, "seed": 7, "rounds": 2, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 5, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R3"], "bid": 0, "tricks_taken": 0, "score": 0},
                         "3": {"hand": ["B4"], "bid": 0, "tricks_taken": 0, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "2"},
             {"seat": 2, "options_include": "2"},
             {"seat": 3, "options_include": "2"}],
   "expect": {"game": {"hand_number": 6},
              "players": {"1": {"score": 30, "bid": 2}, "2": {"score": 20, "bid": 2}, "3": {"score": 20, "bid": 2}},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "Game ends after hand 12 is scored; seats 1 and 2 tie at 120 and share the win",
   "rule": "R21", "players": 3, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 12, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1"], "bid": 0, "tricks_taken": 0, "score": 100},
                         "2": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 90},
                         "3": {"hand": ["B5"], "bid": 1, "tricks_taken": 2, "score": 80}}},
   "rules": [],
   "expect": {"winner": [1, 2],
              "standings": {"1": 120, "2": 120, "3": 70},
              "players": {"1": {"score": 120}, "2": {"score": 120}, "3": {"score": 70}},
              "game": {"hand_number": 12}}},

  {"name": "Game ends after hand 12 is scored; the highest score (seat 3) wins alone",
   "rule": "R21", "players": 3, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 12, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R1"], "bid": 0, "tricks_taken": 0, "score": 100},
                         "2": {"hand": ["W1"], "bid": 1, "tricks_taken": 0, "score": 90},
                         "3": {"hand": ["B5"], "bid": 1, "tricks_taken": 2, "score": 200}}},
   "rules": [],
   "expect": {"winner": 3,
              "standings": {"1": 120, "2": 120, "3": 190}}}
]
````
