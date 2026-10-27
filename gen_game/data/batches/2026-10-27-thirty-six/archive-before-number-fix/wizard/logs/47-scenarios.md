# 47 scenarios

- time: 2026-10-27T18:56:07+00:00 (82.5s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 2c8381b95b585ce0, reply sha256 d9f7a6a26faa34d9

## Sent

````
SPEC:
{
  "name": "Pocket Wizard",
  "summary": "A three-player Wizard-style trick-taking game: 9 hands of 3 tricks each, where every seat bids how many tricks it will take and scores for hitting its bid exactly.",
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
    "total_rounds": 27,
    "tricks_per_hand": 3,
    "hands": 9,
    "cards_dealt_per_seat": 3,
    "trump_cards_turned": 1,
    "deck_left_after_deal": 18,
    "bid_min": 0,
    "bid_max": 3,
    "default_bid": 1,
    "best_value_start": -1,
    "wizard_strength": 100,
    "jester_strength": 0,
    "second_wizard_strength": 0,
    "trump_bonus": 20,
    "exact_bid_bonus": 20,
    "points_per_trick_on_exact_bid": 10,
    "penalty_per_trick_off": 10,
    "first_leader": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Ordered list of the cards this seat holds.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks this seat bid for the current hand (0 to 3).",
        "observable": true
      },
      {
        "key": "bid_answer",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This seat's raw answer to the bidding question, before validation.",
        "observable": false
      },
      {
        "key": "tricks_taken",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks this seat has won in the current hand.",
        "observable": true
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this seat played to the current trick.",
        "observable": true
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The legal cards this seat may play right now, in hand order.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This seat's running score.",
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
        "meaning": "The cards not yet dealt.",
        "observable": false
      },
      {
        "key": "trump_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card turned up after the deal.",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "none",
        "meaning": "R, B, G or none.",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Which hand is being played (1 to 9).",
        "observable": true
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Which trick of the hand this round is (1 to 3).",
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
        "meaning": "The suit led in this trick, or none.",
        "observable": false
      },
      {
        "key": "best_value",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The highest strength played so far in this trick.",
        "observable": false
      },
      {
        "key": "best_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat currently winning the trick.",
        "observable": false
      },
      {
        "key": "cur_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card just played.",
        "observable": false
      },
      {
        "key": "cur_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that just played.",
        "observable": false
      },
      {
        "key": "cur_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The strength of the card just played.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every seat's score, bid and tricks_taken are set to 0, and every hand is empty.",
    "hand_number is set to 0, trick_in_hand to 1 and leader to 1.",
    "The deck is filled with all 28 cards in the order R1-R8, B1-B8, G1-G8, W1, W2, J1, J2."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: hand_number += 1. The deck is reset to the full 28 cards. Every tricks_taken = 0. Dealing goes seat 1, then seat 2, then seat 3: each seat draws 3 cards at random from the deck, one at a time, and each card is appended to its hand in the order drawn and removed from the deck. leader = ((hand_number - 1) mod 3) + 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: one card is drawn at random from the deck into trump_card and removed from the deck, leaving 18 cards. trump_suit = the first letter of trump_card if that letter is R, B or G, otherwise 'none'. Announce trump_card and trump_suit to everyone."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each seat is shown its own hand, trump_card and trump_suit."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 3: 'How many tricks will you take this hand?'",
      "effect": "When trick_in_hand == 1: each answer is stored in that seat's bid_answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: bid = bid_answer if it is exactly 0, 1, 2 or 3; otherwise bid = 1. Announce all three bids."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Start of trick: led_suit = 'none', best_value = -1, best_seat = leader."
    },
    {
      "action": "update",
      "who": "seat leader",
      "answer": null,
      "effect": "Build the leader's offer. If led_suit is not 'none' and the hand holds at least one card of led_suit, offer = the cards of led_suit plus every W and J card, in hand order. Otherwise offer = the whole hand, in hand order."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "one card from that seat's offer",
      "effect": "If the answer is missing or not in the offer, the first card of the offer is used. The card is removed from the hand, and the remaining cards keep their order. played_card = that card, cur_card = that card, cur_seat = this seat. The card is shown to all players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If led_suit == 'none' and best_value < 100 and cur_card is an R, B or G card, then led_suit = the suit of cur_card. Then set cur_strength: 100 if cur_card is a W and best_value < 100; 0 if cur_card is a W and best_value >= 100; 0 if cur_card is a J; 20 + rank if the suit of cur_card == trump_suit; rank if the suit of cur_card == led_suit; otherwise 0. If cur_strength > best_value, then best_value = cur_strength and best_seat = cur_seat."
    },
    {
      "action": "update",
      "who": "seat (leader mod 3) + 1",
      "answer": null,
      "effect": "Build that seat's offer by the same rule as for the leader."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 3) + 1",
      "answer": "one card from that seat's offer",
      "effect": "Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Apply the led-suit and strength rules to cur_card, exactly as after the leader's play."
    },
    {
      "action": "update",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": null,
      "effect": "Build that seat's offer by the same rule as for the leader."
    },
    {
      "action": "ask",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": "one card from that seat's offer",
      "effect": "Same as the leader's play: an invalid answer plays the first card of the offer; the card is removed from the hand; played_card, cur_card and cur_seat are set; the card is shown to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Apply the led-suit and strength rules to cur_card, exactly as after the leader's play."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Trick award: the tricks_taken of seat best_seat += 1; leader = best_seat. Announce the trick winner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 3: for each seat, if tricks_taken == bid then score += 20 + 10 * tricks_taken, otherwise score -= 10 * |tricks_taken - bid|. Announce all scores."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_in_hand += 1; if trick_in_hand == 4, then trick_in_hand = 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_number == 9 and trick_in_hand == 1 (27 rounds have been played); otherwise continue."
    }
  ],
  "ending": {
    "condition": "hand_number == 9 and trick_in_hand == 1",
    "rank_by": "you.score",
    "decided_by": "After 27 rounds (9 hands), each seat's standing is its score. The highest score wins, and seats tied for the highest score share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a round starts with trick_in_hand == 1, then hand_number increases by 1, the deck is refilled to 28 cards, every tricks_taken becomes 0, and seats 1, 2 and 3 each receive 3 cards in that order."
    },
    {
      "id": "R1b",
      "text": "When a round starts with trick_in_hand == 2 or 3, then no cards are dealt and no hand changes except through play."
    },
    {
      "id": "R1c",
      "text": "When a hand is dealt, then leader becomes ((hand_number - 1) mod 3) + 1, so hand 1 is led by seat 1, hand 2 by seat 2 and hand 4 by seat 1."
    },
    {
      "id": "R2",
      "text": "When a hand is dealt, then one more card becomes trump_card and exactly 18 cards remain in the deck."
    },
    {
      "id": "R2b",
      "text": "When trump_card is an R, B or G card, then trump_suit is that suit; when it is W1, W2, J1 or J2, then trump_suit is 'none'."
    },
    {
      "id": "R3",
      "text": "When trick_in_hand == 1, then all three seats are asked for a bid at the same time, and none sees another's bid before answering."
    },
    {
      "id": "R4",
      "text": "When a bid answer is exactly 0, 1, 2 or 3, then bid equals that answer (a 0 stays 0); when it is missing or anything else, then bid is 1."
    },
    {
      "id": "R5",
      "text": "When a trick starts, then led_suit is 'none', best_value is -1 and best_seat is the leader."
    },
    {
      "id": "R6",
      "text": "When a trick is played, then the seats play in the order leader, (leader mod 3) + 1, ((leader + 1) mod 3) + 1, so a trick led by seat 3 is played by seats 3, 1, 2."
    },
    {
      "id": "R7",
      "text": "When led_suit is a suit and the seat holds a card of that suit, then its offer is exactly its cards of that suit plus its W and J cards, in hand order; otherwise its offer is its whole hand."
    },
    {
      "id": "R8",
      "text": "When a seat's answer is missing or not in its offer, then the first card of the offer is played; the played card leaves the hand and the other cards keep their order."
    },
    {
      "id": "R9",
      "text": "When led_suit is 'none', best_value < 100 and an R, B or G card is played, then led_suit becomes that card's suit (so after a Jester lead, the first suited card sets the led suit, but after a Wizard lead it does not)."
    },
    {
      "id": "R10a",
      "text": "When a Wizard is played and best_value < 100, then its strength is 100, so the first Wizard always wins the trick."
    },
    {
      "id": "R10b",
      "text": "When a Wizard is played after another Wizard in the same trick, or a Jester is played, then its strength is 0."
    },
    {
      "id": "R10c",
      "text": "When a card of trump_suit is played, then its strength is 20 + rank (for example, trump 3 = 23)."
    },
    {
      "id": "R10d",
      "text": "When a card of led_suit that is not trump is played, then its strength is its rank; any other card has strength 0."
    },
    {
      "id": "R10e",
      "text": "When a strength is strictly greater than best_value, then best_value and best_seat update; a tie never changes best_seat, so if only Jesters are played, the first Jester wins."
    },
    {
      "id": "R11",
      "text": "When all three seats have played, then best_seat's tricks_taken increases by 1 and best_seat leads the next trick."
    },
    {
      "id": "R12a",
      "text": "When trick_in_hand == 3 and a seat's tricks_taken equals its bid, then its score increases by 20 + 10 * tricks_taken (bid 0 and took 0 gives +20; bid 2 and took 2 gives +40)."
    },
    {
      "id": "R12b",
      "text": "When trick_in_hand == 3 and tricks_taken differs from bid, then score decreases by 10 * |tricks_taken - bid| (bid 3 and took 1 gives -20)."
    },
    {
      "id": "R13",
      "text": "When a round ends, then trick_in_hand increases by 1, wrapping from 3 back to 1."
    },
    {
      "id": "R14",
      "text": "When 27 rounds (9 hands) have been played, then the game ends and the highest score wins; seats tied at the top share the result."
    }
  ],
  "offers": [
    {
      "question": "Bid: how many tricks will you take this hand?",
      "who": "all three seats, at the same time, when trick_in_hand == 1",
      "options": "a whole number 0, 1, 2 or 3"
    },
    {
      "question": "Play a card",
      "who": "the seat whose turn it is in the trick",
      "options": "The leader, or any seat while led_suit is 'none': every card in its hand. A follower holding at least one card of led_suit: those cards plus its Wizards and Jesters, in hand order. A follower holding no card of led_suit: every card in its hand."
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3. The deck size, the 3-card deal, the 18 cards left after the deal and the 3-trick hands all assume exactly 3 seats. More seats would not fit the 28-card deck at this deal size, and fewer would leave no rivals to bid against."
    },
    {
      "what": "No talk step before bids or plays",
      "why": "The source has no table talk, and adding it would add a mechanic. The strategy is in the cards: estimating your hand's trick count from the trump, reading the other bids, and ducking or taking tricks to hit your bid or spoil an opponent's."
    },
    {
      "what": "Bids are gathered with a simultaneous poll",
      "why": "The source says all three seats answer at the same moment."
    },
    {
      "what": "The hand-start steps are separate steps, each with the condition trick_in_hand == 1",
      "why": "The step list is flat, so the condition is placed on each step instead of on a block."
    },
    {
      "what": "The game ends on hand_number == 9 and trick_in_hand == 1, checked after the advance",
      "why": "This is true exactly after round 27, without adding a round counter."
    },
    {
      "what": "'A Wizard was already played this trick' is tested as best_value >= 100",
      "why": "Only a Wizard can reach strength 100, so the two are equivalent and no extra state is needed."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling and taking the top cards is done as random draws from the deck list",
      "why": "The engine's draw picks a random card, which gives the same distribution as shuffling and dealing from the top."
    },
    {
      "what": "A tie for the highest score is a shared win rather than a declared draw",
      "why": "The engine has no separate draw: players level at the top share the win, which is equivalent."
    },
    {
      "what": "Each trick is written as three fixed offer/ask/strength step groups, with seats picked from leader by arithmetic",
      "why": "The engine has no per-player sub-loop, so each play position gets its own steps."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bid, tricks_taken, played_card, score; table: trump_card, trump_suit, hand_number.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Treat the bid as a free numeric answer (numeric_bids), not a choice from an offered list. Script bids by giving each seat's answer directly as a number (e.g. seat answers 1), not with `options_include` rules for '0'/'1'. Do not assert that '0' was 'offered' in the R3 test. Instead, check that all three seats gave a bid in round 1 and that `bid` holds the validated value: 0–3 kept unchanged, anything else becomes 1. Keep `options_include` only for card plays, where the offer really is a list. Assert on the public result (hand_number, hand and deck sizes, bid, tricks_taken, score). Do not assert on scratch values or on which cards chance deals.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "R1: a new hand refills the deck and deals 3 cards to each seat (cards dealt are random, only counts asserted)", "rule": "R1", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"deck": ["R1", "R2"]}},
   "rules": [{"seat": 1, "answer": 1, "times": 1}, {"seat": 2, "answer": 1, "times": 1}, {"seat": 3, "answer": 1, "times": 1}],
   "expect": {"game": {"hand_number": 1},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R1b: a round starting at trick 2 deals nothing; each hand only loses its played card", "rule": "R1b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none", "deck": ["B1"]},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R6", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R4", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"game": {"hand_number": 1, "trump_card": "W2"},
              "lens": {"game": {"deck": 1}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R1c: the next hand is dealt and hand_number advances to 2 (random cards, only counts asserted)", "rule": "R1c", "players": 3, "rounds": 1, "seed": 2, "default": "first",
   "given": {"game": {"hand_number": 1, "trick_in_hand": 1}},
   "rules": [{"seat": 1, "answer": 1, "times": 1}, {"seat": 2, "answer": 1, "times": 1}, {"seat": 3, "answer": 1, "times": 1}],
   "expect": {"game": {"hand_number": 2},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R2: after the deal and the trump card, 18 cards remain in the deck (trump itself is random)", "rule": "R2", "players": 3, "rounds": 1, "seed": 3, "default": "first",
   "rules": [{"seat": 1, "answer": 2, "times": 1}, {"seat": 2, "answer": 2, "times": 1}, {"seat": 3, "answer": 2, "times": 1}],
   "expect": {"game": {"hand_number": 1}, "lens": {"game": {"deck": 18}}}},

  {"name": "R2b: with a Wizard as trump card there is no trump suit, so off-suit cards cannot win", "rule": "R2b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B8", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G8", "B3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"game": {"trump_suit": "none"},
              "players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B8"}, "3": {"tricks_taken": 0, "played_card": "G8"}}}},

  {"name": "R3: all three seats bid in the first round and each bid is stored", "rule": "R3", "players": 3, "rounds": 1, "seed": 4, "default": "first",
   "rules": [{"seat": 1, "answer": 0, "times": 1}, {"seat": 2, "answer": 2, "times": 1}, {"seat": 3, "answer": 3, "times": 1}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 2}, "3": {"bid": 3}}}},

  {"name": "R4: an out-of-range bid becomes 1 and a bid of 0 stays 0", "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "first",
   "rules": [{"seat": 1, "answer": 7, "times": 1}, {"seat": 2, "answer": 0, "times": 1}, {"seat": 3, "answer": 4, "times": 1}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 1}}}},

  {"name": "R5: stale led suit and best value from before the trick are cleared at the start of the trick", "rule": "R5", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none", "led_suit": "R", "best_value": 50, "best_seat": 3},
             "players": {"1": {"hand": ["B5", "R1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B1", "R2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G1", "R3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "B5"}, "2": {"tricks_taken": 0, "played_card": "B1"}, "3": {"tricks_taken": 0, "played_card": "G1"}}}},

  {"name": "R6: a trick led by seat 3 is played 3, 1, 2, so seat 1's suited card sets the led suit after a Jester lead", "rule": "R6", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 3, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G4"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B5", "G5"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["J1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B5"}, "3": {"tricks_taken": 0, "played_card": "J1"}}}},

  {"name": "R7: a follower holding the led suit is offered only that suit plus Wizards and Jesters; one without it is offered everything", "rule": "R7", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B3", "R2", "W1", "J1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["B4", "G6"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R5"}, "2": {"played_card": "R2"}, "3": {"played_card": "B4"}},
              "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "W1"}, {"seat": 2, "option": "J1"}, {"seat": 3, "option": "B4"}, {"seat": 3, "option": "G6"}],
              "not_offered": [{"seat": 2, "option": "B3"}]}},

  {"name": "R8: an answer outside the offer plays the first card of the offer", "rule": "R8", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B3", "J1", "R2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G6", "B4"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 2, "options_include": "R2", "answer": "B3"}],
   "expect": {"players": {"1": {"played_card": "R5", "tricks_taken": 1}, "2": {"played_card": "J1", "tricks_taken": 0}, "3": {"played_card": "G6"}},
              "lens": {"players": {"2": {"hand": 2}}}}},

  {"name": "R9: after a Wizard lead no suit is led, so later seats may play anything", "rule": "R9", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R7", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B2"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "W1"}, "2": {"played_card": "R7"}, "3": {"played_card": "R1"}},
              "offered": [{"seat": 3, "option": "B2"}, {"seat": 3, "option": "R1"}]}},

  {"name": "R9: after a Jester lead the first suited card sets the led suit and must be followed", "rule": "R9", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["J1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R3", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B6"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "J1"}, "2": {"tricks_taken": 1, "played_card": "R3"}, "3": {"tricks_taken": 0, "played_card": "R1"}},
              "not_offered": [{"seat": 3, "option": "B6"}]}},

  {"name": "R10a: a Wizard beats the highest trump", "rule": "R10a", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"},
             "players": {"1": {"hand": ["R8", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["W2", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "R8"}, "2": {"tricks_taken": 1, "played_card": "W2"}, "3": {"tricks_taken": 0, "played_card": "R1"}}}},

  {"name": "R10b: the second Wizard and a Jester do not beat the first Wizard", "rule": "R10b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["W2", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["J1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0, "played_card": "W2"}, "3": {"tricks_taken": 0, "played_card": "J1"}}}},

  {"name": "R10c: a low trump beats high cards of the led suit", "rule": "R10c", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "B4", "trump_suit": "B"},
             "players": {"1": {"hand": ["R8", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B1", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R7", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1, "played_card": "B1"}, "3": {"tricks_taken": 0, "played_card": "R7"}}}},

  {"name": "R10d: an off-suit non-trump card has strength 0 and loses to a low led-suit card", "rule": "R10d", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "G4", "trump_suit": "G"},
             "players": {"1": {"hand": ["R2", "B1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B8", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B8"}, "3": {"tricks_taken": 0, "played_card": "R1"}}}},

  {"name": "R10e: a strictly higher card of the led suit takes over the trick", "rule": "R10e", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R6", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R4", "G3"], "bid": 1, "tricks_taken": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "R11: the trick winner gains a trick and leads the next trick", "rule": "R11", "players": 3, "rounds": 2, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G1"], "bid": 0, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R8", "B1"], "bid": 2, "tricks_taken": 0, "score": 0},
                         "3": {"hand": ["R3", "G2"], "bid": 1, "tricks_taken": 0, "score": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "G1", "score": 20},
                          "2": {"tricks_taken": 2, "played_card": "B1", "score": 40},
                          "3": {"tricks_taken": 0, "played_card": "G2", "score": -10}}}},

  {"name": "R12a: exact bids score 20 + 10 per trick at the end of the hand", "rule": "R12a", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R8"], "bid": 2, "tricks_taken": 1, "score": 50},
                         "2": {"hand": ["R1"], "bid": 0, "tricks_taken": 0, "score": 50},
                         "3": {"hand": ["R2"], "bid": 3, "tricks_taken": 1, "score": 50}}},
   "expect": {"players": {"1": {"tricks_taken": 2, "score": 90}, "2": {"tricks_taken": 0, "score": 70}, "3": {"tricks_taken": 1, "score": 30}}}},

  {"name": "R12b: missed bids lose 10 per trick off, over or under", "rule": "R12b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["G2"], "bid": 3, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["G1"], "bid": 1, "tricks_taken": 1, "score": 0},
                         "3": {"hand": ["G8"], "bid": 0, "tricks_taken": 1, "score": 0}}},
   "expect": {"players": {"1": {"tricks_taken": 0, "score": -30}, "2": {"tricks_taken": 1, "score": 30}, "3": {"tricks_taken": 2, "score": -20}}}},

  {"name": "R13: after trick 3 the next round is trick 1 of a new hand, which deals again", "rule": "R13", "players": 3, "rounds": 2, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R8"], "bid": 1, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R1"], "bid": 1, "tricks_taken": 1, "score": 0},
                         "3": {"hand": ["R2"], "bid": 1, "tricks_taken": 1, "score": 0}}},
   "expect": {"game": {"hand_number": 2},
              "players": {"1": {"score": 30}, "2": {"score": 30}, "3": {"score": 30}},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R14: the game ends after the last trick of hand 9 and the highest score wins", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 9, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["B1"], "bid": 1, "tricks_taken": 1, "score": 100},
                         "2": {"hand": ["B2"], "bid": 1, "tricks_taken": 1, "score": 90},
                         "3": {"hand": ["B8"], "bid": 1, "tricks_taken": 0, "score": 95}}},
   "expect": {"winner": 1, "standings": {"1": 130, "2": 120, "3": 125},
              "players": {"1": {"score": 130}, "2": {"score": 120}, "3": {"score": 125}}}},

  {"name": "R14: seats level on the top score share the win", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 9, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["B1"], "bid": 1, "tricks_taken": 1, "score": 100},
                         "2": {"hand": ["B2"], "bid": 1, "tricks_taken": 1, "score": 90},
                         "3": {"hand": ["B8"], "bid": 1, "tricks_taken": 0, "score": 100}}},
   "expect": {"winner": [1, 3], "standings": {"1": 130, "2": 120, "3": 130}}}
]

Why it was refused: scenario 1: each rule needs a `seat` and an `options_include`; scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: each rule needs a `seat` and an `options_include`; scenario 4: each rule needs a `seat` and an `options_include`; scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: each rule needs a `seat` and an `options_include`; scenario 7: each rule needs a `seat` and an `options_include`; scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "R1: a new hand refills the deck and deals 3 cards to each seat (cards dealt are random, only counts asserted)", "rule": "R1", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"deck": ["R1", "R2"]}},
   "rules": [{"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1}],
   "expect": {"game": {"hand_number": 1},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R1b: a round starting at trick 2 deals nothing; each hand only loses its played card", "rule": "R1b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none", "deck": ["B1"]},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R6", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R4", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"}, {"seat": 2, "options_include": "R6"}, {"seat": 3, "options_include": "R4"}],
   "expect": {"game": {"hand_number": 1, "trump_card": "W2"},
              "lens": {"game": {"deck": 1}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}}},

  {"name": "R1c: the next hand is dealt and hand_number advances to 2 (random cards, only counts asserted)", "rule": "R1c", "players": 3, "rounds": 1, "seed": 2, "default": "first",
   "given": {"game": {"hand_number": 1, "trick_in_hand": 1}},
   "rules": [{"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1}],
   "expect": {"game": {"hand_number": 2},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R2: after the deal and the trump card, 18 cards remain in the deck (trump itself is random)", "rule": "R2", "players": 3, "rounds": 1, "seed": 3, "default": "first",
   "rules": [{"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 2, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 2, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 2, "times": 1}],
   "expect": {"game": {"hand_number": 1}, "lens": {"game": {"deck": 18}}}},

  {"name": "R2b: with a Wizard as trump card there is no trump suit, so off-suit cards cannot win", "rule": "R2b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B8", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G8", "B3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R2"}, {"seat": 2, "options_include": "B8"}, {"seat": 3, "options_include": "G8"}],
   "expect": {"game": {"trump_suit": "none"},
              "players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B8"}, "3": {"tricks_taken": 0, "played_card": "G8"}}}},

  {"name": "R3: all three seats bid in the first round and each bid is stored", "rule": "R3", "players": 3, "rounds": 1, "seed": 4, "default": "first",
   "rules": [{"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 0, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 2, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 3, "times": 1}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 2}, "3": {"bid": 3}}}},

  {"name": "R4: an out-of-range bid becomes 1 and a bid of 0 stays 0", "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "first",
   "rules": [{"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 7, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 0, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 4, "times": 1}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 1}}}},

  {"name": "R5: stale led suit and best value from before the trick are cleared at the start of the trick", "rule": "R5", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none", "led_suit": "R", "best_value": 50, "best_seat": 3},
             "players": {"1": {"hand": ["B5", "R1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B1", "R2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G1", "R3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "B5"}, {"seat": 2, "options_include": "B1"}, {"seat": 3, "options_include": "G1"}],
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "B5"}, "2": {"tricks_taken": 0, "played_card": "B1"}, "3": {"tricks_taken": 0, "played_card": "G1"}}}},

  {"name": "R6: a trick led by seat 3 is played 3, 1, 2, so seat 1's suited card sets the led suit after a Jester lead", "rule": "R6", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 3, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G4"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B5", "G5"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["J1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 3, "options_include": "J1"}, {"seat": 1, "options_include": "R2"}, {"seat": 2, "options_include": "B5"}],
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B5"}, "3": {"tricks_taken": 0, "played_card": "J1"}}}},

  {"name": "R7: a follower holding the led suit is offered only that suit plus Wizards and Jesters; one without it is offered everything", "rule": "R7", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B3", "R2", "W1", "J1"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["B4", "G6"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"}, {"seat": 2, "options_include": "R2"}, {"seat": 3, "options_include": "B4"}],
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R5"}, "2": {"played_card": "R2"}, "3": {"played_card": "B4"}},
              "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "W1"}, {"seat": 2, "option": "J1"}, {"seat": 3, "option": "B4"}, {"seat": 3, "option": "G6"}],
              "not_offered": [{"seat": 2, "option": "B3"}]}},

  {"name": "R8: an answer outside the offer plays the first card of the offer", "rule": "R8", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B3", "J1", "R2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["G6", "B4"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"}, {"seat": 2, "options_include": "R2", "answer": "B3"}, {"seat": 3, "options_include": "G6"}],
   "expect": {"players": {"1": {"played_card": "R5", "tricks_taken": 1}, "2": {"played_card": "J1", "tricks_taken": 0}, "3": {"played_card": "G6"}},
              "lens": {"players": {"2": {"hand": 2}}}}},

  {"name": "R9: after a Wizard lead no suit is led, so later seats may play anything", "rule": "R9", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R7", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B2"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "R7"}, {"seat": 3, "options_include": "R1"}],
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "W1"}, "2": {"played_card": "R7"}, "3": {"played_card": "R1"}},
              "offered": [{"seat": 3, "option": "B2"}, {"seat": 3, "option": "R1"}]}},

  {"name": "R9: after a Jester lead the first suited card sets the led suit and must be followed", "rule": "R9", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W2", "trump_suit": "none"},
             "players": {"1": {"hand": ["J1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R3", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B6"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "J1"}, {"seat": 2, "options_include": "R3"}, {"seat": 3, "options_include": "R1"}],
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "J1"}, "2": {"tricks_taken": 1, "played_card": "R3"}, "3": {"tricks_taken": 0, "played_card": "R1"}},
              "not_offered": [{"seat": 3, "option": "B6"}]}},

  {"name": "R10a: a Wizard beats the highest trump", "rule": "R10a", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "R4", "trump_suit": "R"},
             "players": {"1": {"hand": ["R8", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["W2", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R8"}, {"seat": 2, "options_include": "W2"}, {"seat": 3, "options_include": "R1"}],
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "R8"}, "2": {"tricks_taken": 1, "played_card": "W2"}, "3": {"tricks_taken": 0, "played_card": "R1"}}}},

  {"name": "R10b: the second Wizard and a Jester do not beat the first Wizard", "rule": "R10b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J2", "trump_suit": "none"},
             "players": {"1": {"hand": ["W1", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["W2", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["J1", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "W1"}, {"seat": 2, "options_include": "W2"}, {"seat": 3, "options_include": "J1"}],
   "expect": {"players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0, "played_card": "W2"}, "3": {"tricks_taken": 0, "played_card": "J1"}}}},

  {"name": "R10c: a low trump beats high cards of the led suit", "rule": "R10c", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "B4", "trump_suit": "B"},
             "players": {"1": {"hand": ["R8", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B1", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R7", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R8"}, {"seat": 2, "options_include": "B1"}, {"seat": 3, "options_include": "R7"}],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1, "played_card": "B1"}, "3": {"tricks_taken": 0, "played_card": "R7"}}}},

  {"name": "R10d: an off-suit non-trump card has strength 0 and loses to a low led-suit card", "rule": "R10d", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "G4", "trump_suit": "G"},
             "players": {"1": {"hand": ["R2", "B1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["B8", "B2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R1", "B3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R2"}, {"seat": 2, "options_include": "B8"}, {"seat": 3, "options_include": "R1"}],
   "expect": {"players": {"1": {"tricks_taken": 1, "played_card": "R2"}, "2": {"tricks_taken": 0, "played_card": "B8"}, "3": {"tricks_taken": 0, "played_card": "R1"}}}},

  {"name": "R10e: a strictly higher card of the led suit takes over the trick", "rule": "R10e", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R5", "G1"], "bid": 1, "tricks_taken": 0},
                         "2": {"hand": ["R6", "G2"], "bid": 1, "tricks_taken": 0},
                         "3": {"hand": ["R4", "G3"], "bid": 1, "tricks_taken": 0}}},
   "rules": [{"seat": 1, "options_include": "R5"}, {"seat": 2, "options_include": "R6"}, {"seat": 3, "options_include": "R4"}],
   "expect": {"players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}}},

  {"name": "R11: the trick winner gains a trick and leads the next trick", "rule": "R11", "players": 3, "rounds": 2, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 2, "hand_number": 1, "leader": 1, "trump_card": "J1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R2", "G1"], "bid": 0, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R8", "B1"], "bid": 2, "tricks_taken": 0, "score": 0},
                         "3": {"hand": ["R3", "G2"], "bid": 1, "tricks_taken": 0, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "R2"}, {"seat": 2, "options_include": "R8"}, {"seat": 3, "options_include": "R3"},
             {"seat": 2, "options_include": "B1"}, {"seat": 3, "options_include": "G2"}, {"seat": 1, "options_include": "G1"}],
   "expect": {"players": {"1": {"tricks_taken": 0, "played_card": "G1", "score": 20},
                          "2": {"tricks_taken": 2, "played_card": "B1", "score": 40},
                          "3": {"tricks_taken": 0, "played_card": "G2", "score": -10}}}},

  {"name": "R12a: exact bids score 20 + 10 per trick at the end of the hand", "rule": "R12a", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R8"], "bid": 2, "tricks_taken": 1, "score": 50},
                         "2": {"hand": ["R1"], "bid": 0, "tricks_taken": 0, "score": 50},
                         "3": {"hand": ["R2"], "bid": 3, "tricks_taken": 1, "score": 50}}},
   "rules": [{"seat": 1, "options_include": "R8"}, {"seat": 2, "options_include": "R1"}, {"seat": 3, "options_include": "R2"}],
   "expect": {"players": {"1": {"tricks_taken": 2, "score": 90}, "2": {"tricks_taken": 0, "score": 70}, "3": {"tricks_taken": 1, "score": 30}}}},

  {"name": "R12b: missed bids lose 10 per trick off, over or under", "rule": "R12b", "players": 3, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["G2"], "bid": 3, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["G1"], "bid": 1, "tricks_taken": 1, "score": 0},
                         "3": {"hand": ["G8"], "bid": 0, "tricks_taken": 1, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "G2"}, {"seat": 2, "options_include": "G1"}, {"seat": 3, "options_include": "G8"}],
   "expect": {"players": {"1": {"tricks_taken": 0, "score": -30}, "2": {"tricks_taken": 1, "score": 30}, "3": {"tricks_taken": 2, "score": -20}}}},

  {"name": "R13: after trick 3 the next round is trick 1 of a new hand, which deals again (new cards random, only counts asserted)", "rule": "R13", "players": 3, "rounds": 2, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 1, "leader": 1, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["R8"], "bid": 1, "tricks_taken": 0, "score": 0},
                         "2": {"hand": ["R1"], "bid": 1, "tricks_taken": 1, "score": 0},
                         "3": {"hand": ["R2"], "bid": 1, "tricks_taken": 1, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "R8"}, {"seat": 2, "options_include": "R1"}, {"seat": 3, "options_include": "R2"},
             {"seat": 1, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 2, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1},
             {"seat": 3, "options_include": "How many tricks will you take this hand?", "answer": 1, "times": 1}],
   "expect": {"game": {"hand_number": 2},
              "players": {"1": {"score": 30}, "2": {"score": 30}, "3": {"score": 30}},
              "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "R14: the game ends after the last trick of hand 9 and the highest score wins", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 9, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["B1"], "bid": 1, "tricks_taken": 1, "score": 100},
                         "2": {"hand": ["B2"], "bid": 1, "tricks_taken": 1, "score": 90},
                         "3": {"hand": ["B8"], "bid": 1, "tricks_taken": 0, "score": 95}}},
   "rules": [{"seat": 3, "options_include": "B8"}, {"seat": 1, "options_include": "B1"}, {"seat": 2, "options_include": "B2"}],
   "expect": {"winner": 1, "standings": {"1": 130, "2": 120, "3": 125},
              "players": {"1": {"score": 130}, "2": {"score": 120}, "3": {"score": 125}}}},

  {"name": "R14: seats level on the top score share the win", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"trick_in_hand": 3, "hand_number": 9, "leader": 3, "trump_card": "W1", "trump_suit": "none"},
             "players": {"1": {"hand": ["B1"], "bid": 1, "tricks_taken": 1, "score": 100},
                         "2": {"hand": ["B2"], "bid": 1, "tricks_taken": 1, "score": 90},
                         "3": {"hand": ["B8"], "bid": 1, "tricks_taken": 0, "score": 100}}},
   "rules": [{"seat": 3, "options_include": "B8"}, {"seat": 1, "options_include": "B1"}, {"seat": 2, "options_include": "B2"}],
   "expect": {"winner": [1, 3], "standings": {"1": 130, "2": 120, "3": 130}}}
]
````
