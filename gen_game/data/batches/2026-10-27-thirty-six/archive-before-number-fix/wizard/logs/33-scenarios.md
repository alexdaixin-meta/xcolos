# 33 scenarios

- time: 2026-10-27T18:36:55+00:00 (94.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 da11032d6b961113, reply sha256 087a393277d43c2a

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

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite 'An invalid bid answer becomes a bid of 1' so that seat 1 really gives an invalid bid answer in round 1, for example '5', 'seven' or an empty or missing answer, and is not left to the 'first' default (which answers 0). Then assert seat 1's bid is 1 and the other seats' valid bids are stored exactly as given. Check the bid right after the poll or at the end of the round, not after hand scoring, since Rule 10 resets bids to 0 at the end of trick 3. Add a separate check that a valid answer of '0' stays 0.
````

## Reply

````
[
{"name":"Setup: scores 0, bids 0, hand_number 0, deck holds 28 cards","rule":"R1","players":3,"rounds":0,
 "expect":{"players":{"1":{"score":0,"bid":0},"2":{"score":0,"bid":0},"3":{"score":0,"bid":0}},"game":{"hand_number":0},"lens":{"game":{"deck":28}}}},
{"name":"First round deals a hand: hand_number 1, each seat got 3 cards (2 left after one trick)","rule":"R1","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"1","times":1},{"seat":2,"options_include":"1","times":1},{"seat":3,"options_include":"1","times":1}],
 "expect":{"game":{"hand_number":1},"lens":{"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"Deal removes one more card as trump, leaving 18 in the deck","rule":"R2","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"1"},{"seat":2,"options_include":"1"},{"seat":3,"options_include":"1"}],
 "expect":{"lens":{"game":{"deck":18}}}},
{"name":"Trump suit card beats led suit (trump_suit G stated in given)","rule":"R3","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_card":"G5","trump_suit":"G"},
  "players":{"1":{"hand":["R8"],"bid":1,"tricks_taken":0},"2":{"hand":["G1"],"bid":1,"tricks_taken":0},"3":{"hand":["R7"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":1},"3":{"tricks_taken":0}}}},
{"name":"New hand after hand 3 is hand 4 (seat 1 leads); random deal so only the count is checked","rule":"R4","players":3,"rounds":1,"default":"first",
 "given":{"game":{"hand_number":3,"trick_in_hand":1}},
 "rules":[{"seat":1,"options_include":"1"},{"seat":2,"options_include":"1"},{"seat":3,"options_include":"1"}],
 "expect":{"game":{"hand_number":4},"lens":{"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"Valid bids are stored exactly, a 0 stays 0","rule":"R5","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"0","answer":"0"},{"seat":2,"options_include":"2","answer":"2"},{"seat":3,"options_include":"3","answer":"3"}],
 "expect":{"players":{"1":{"bid":0},"2":{"bid":2},"3":{"bid":3}}}},
{"name":"An invalid bid answer becomes a bid of 1","rule":"R6","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"0","answer":"5"},{"seat":2,"options_include":"0","answer":"0"},{"seat":3,"options_include":"3","answer":"3"}],
 "expect":{"players":{"1":{"bid":1},"2":{"bid":0},"3":{"bid":3}}}},
{"name":"Bids need not sum to 3: all three bid 3","rule":"R7","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"3","answer":"3"},{"seat":2,"options_include":"3","answer":"3"},{"seat":3,"options_include":"3","answer":"3"}],
 "expect":{"players":{"1":{"bid":3},"2":{"bid":3},"3":{"bid":3}}}},
{"name":"Trick state is reset: stale best_seat 3 and led_suit B do not carry over","rule":"R8","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J1","best_value":50,"best_seat":3,"led_suit":"B"},
  "players":{"1":{"hand":["R2"],"bid":1,"tricks_taken":0},"2":{"hand":["R1"],"bid":1,"tricks_taken":0},"3":{"hand":["B5"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":1},"2":{"tricks_taken":0},"3":{"tricks_taken":0}}}},
{"name":"Play order leader 2, then 3, then 1: seat 3's Wizard comes before seat 1's","rule":"R9","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":2,"leader":2,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W2"],"bid":1,"tricks_taken":0},"2":{"hand":["J1"],"bid":1,"tricks_taken":0},"3":{"hand":["W1"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":0},"3":{"tricks_taken":1}}}},
{"name":"Follower holding the led suit must follow (or play W/J); a void player may play anything","rule":"R10","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"B","trump_card":"B8"},
  "players":{"1":{"hand":["R5"],"bid":1,"tricks_taken":0},"2":{"hand":["B3","R2","J1"],"bid":1,"tricks_taken":0},"3":{"hand":["W1","G4"],"bid":1,"tricks_taken":0}}},
 "rules":[{"seat":2,"options_include":"R2"},{"seat":3,"options_include":"G4"}],
 "expect":{"players":{"1":{"tricks_taken":1},"2":{"tricks_taken":0},"3":{"tricks_taken":0}},
  "offered":[{"seat":2,"option":"R2"},{"seat":2,"option":"J1"},{"seat":3,"option":"G4"},{"seat":3,"option":"W1"}],
  "not_offered":[{"seat":2,"option":"B3"}]}},
{"name":"An invalid card answer plays the first card of the offer","rule":"R11","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"W1"},
  "players":{"1":{"hand":["R2","R5"],"bid":1,"tricks_taken":0},"2":{"hand":["R3"],"bid":1,"tricks_taken":0},"3":{"hand":["R1"],"bid":1,"tricks_taken":0}}},
 "rules":[{"seat":1,"options_include":"R5","answer":"Z9"}],
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":1},"3":{"tricks_taken":0}}}},
{"name":"A played card leaves the hand","rule":"R12","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"W1"},
  "players":{"1":{"hand":["R2","R5"],"bid":1,"tricks_taken":0},"2":{"hand":["R3","G1"],"bid":1,"tricks_taken":0},"3":{"hand":["R1","G2"],"bid":1,"tricks_taken":0}}},
 "rules":[{"seat":1,"options_include":"R5"},{"seat":2,"options_include":"R3"},{"seat":3,"options_include":"R1"}],
 "expect":{"lens":{"players":{"1":{"hand":1},"2":{"hand":1},"3":{"hand":1}}},"players":{"1":{"tricks_taken":1}}}},
{"name":"After a Jester lead, the first suited card sets the led suit","rule":"R13","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["J1"],"bid":1,"tricks_taken":0},"2":{"hand":["B2"],"bid":1,"tricks_taken":0},"3":{"hand":["R8"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":1},"3":{"tricks_taken":0}}}},
{"name":"After a Wizard lead no suit is led, so a later player may play any card, and the Wizard wins","rule":"R14","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":1,"tricks_taken":0},"2":{"hand":["R8"],"bid":1,"tricks_taken":0},"3":{"hand":["R2","B1"],"bid":1,"tricks_taken":0}}},
 "rules":[{"seat":3,"options_include":"B1"}],
 "expect":{"players":{"1":{"tricks_taken":1},"2":{"tricks_taken":0},"3":{"tricks_taken":0}},"offered":[{"seat":3,"option":"B1"}]}},
{"name":"Strength: a low trump (20+1) beats high led-suit cards","rule":"R15","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"G","trump_card":"G5"},
  "players":{"1":{"hand":["R8"],"bid":1,"tricks_taken":0},"2":{"hand":["G1"],"bid":1,"tricks_taken":0},"3":{"hand":["R7"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":1},"3":{"tricks_taken":0}}}},
{"name":"Equal strength does not take the lead: the first Wizard wins","rule":"R16","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J1"},
  "players":{"1":{"hand":["R3"],"bid":1,"tricks_taken":0},"2":{"hand":["W1"],"bid":1,"tricks_taken":0},"3":{"hand":["W2"],"bid":1,"tricks_taken":0}}},
 "expect":{"players":{"1":{"tricks_taken":0},"2":{"tricks_taken":1},"3":{"tricks_taken":0}}}},
{"name":"Trick winner leads the next trick (seat 3's Wizard comes before seat 1's), then the hand is scored","rule":"R17","players":3,"rounds":2,"default":"first",
 "given":{"game":{"trick_in_hand":2,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J1"},
  "players":{"1":{"hand":["R2","W2"],"bid":0,"tricks_taken":0,"score":0},"2":{"hand":["R1","B1"],"bid":0,"tricks_taken":0,"score":0},"3":{"hand":["R6","W1"],"bid":2,"tricks_taken":0,"score":0}}},
 "rules":[{"seat":1,"options_include":"R2"},{"seat":3,"options_include":"R6"}],
 "expect":{"players":{"1":{"tricks_taken":0,"score":20,"bid":0},"2":{"tricks_taken":0,"score":20,"bid":0},"3":{"tricks_taken":2,"score":40,"bid":0}}}},
{"name":"Exact bids score 20 + 10 per trick at the end of trick 3","rule":"R18","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":3,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":1,"tricks_taken":0,"score":10},"2":{"hand":["J1"],"bid":0,"tricks_taken":0,"score":10},"3":{"hand":["R3"],"bid":2,"tricks_taken":2,"score":10}}},
 "expect":{"players":{"1":{"tricks_taken":1,"score":40},"2":{"tricks_taken":0,"score":30},"3":{"tricks_taken":2,"score":50}}}},
{"name":"Missed bids lose 10 per trick off","rule":"R19","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":3,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":3,"tricks_taken":0,"score":0},"2":{"hand":["J1"],"bid":1,"tricks_taken":0,"score":0},"3":{"hand":["R3"],"bid":0,"tricks_taken":2,"score":0}}},
 "expect":{"players":{"1":{"score":-20},"2":{"score":-10},"3":{"score":-20}}}},
{"name":"Bids are reset to 0 after the hand is scored","rule":"R20","players":3,"rounds":1,"default":"first",
 "given":{"game":{"trick_in_hand":3,"hand_number":1,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":1,"tricks_taken":0,"score":0},"2":{"hand":["J1"],"bid":2,"tricks_taken":0,"score":0},"3":{"hand":["R3"],"bid":3,"tricks_taken":0,"score":0}}},
 "expect":{"players":{"1":{"bid":0,"score":30},"2":{"bid":0,"score":-20},"3":{"bid":0,"score":-30}}}},
{"name":"After trick 1 the hand continues: no new deal, bids kept, hand_number stays 1","rule":"R20","players":3,"rounds":2,"default":"first",
 "rules":[{"seat":1,"options_include":"2","answer":"2"},{"seat":2,"options_include":"1","answer":"1"},{"seat":3,"options_include":"0","answer":"0"}],
 "expect":{"game":{"hand_number":1},"players":{"1":{"bid":2},"2":{"bid":1},"3":{"bid":0}},"lens":{"players":{"1":{"hand":1},"2":{"hand":1},"3":{"hand":1}}}}},
{"name":"Game ends after hand 12 is scored; the highest score wins","rule":"R21","players":3,"default":"first",
 "given":{"game":{"trick_in_hand":3,"hand_number":12,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":1,"tricks_taken":0,"score":100},"2":{"hand":["J1"],"bid":0,"tricks_taken":0,"score":120},"3":{"hand":["R3"],"bid":0,"tricks_taken":0,"score":90}}},
 "expect":{"winner":2,"standings":{"1":130,"2":140,"3":110},"players":{"1":{"score":130},"2":{"score":140},"3":{"score":110}}}},
{"name":"Players tied at the top after hand 12 share the win","rule":"R21","players":3,"default":"first",
 "given":{"game":{"trick_in_hand":3,"hand_number":12,"leader":1,"trump_suit":"none","trump_card":"J2"},
  "players":{"1":{"hand":["W1"],"bid":1,"tricks_taken":0,"score":50},"2":{"hand":["J1"],"bid":0,"tricks_taken":0,"score":60},"3":{"hand":["R3"],"bid":0,"tricks_taken":0,"score":0}}},
 "expect":{"winner":[1,2],"standings":{"1":80,"2":80,"3":20}}}
]
````
