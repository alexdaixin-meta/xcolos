# 07 scenarios

- time: 2026-10-27T17:59:20+00:00 (65.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 172a9507188748a6, reply sha256 e615e5ec166d2650

## Sent

````
SPEC:
{
  "name": "Wizard Triad",
  "summary": "A three-player trick-taking game over 12 hands of 3 tricks each. Players secretly bid how many tricks they will take, then follow suit, with Wizards, Jesters and trump, and score for hitting the bid exactly.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 28,
    "suits": 3,
    "rank_min": 1,
    "rank_max": 8,
    "wizards": 2,
    "jesters": 2,
    "hands": 12,
    "tricks_per_hand": 3,
    "total_rounds": 36,
    "cards_dealt_per_player": 3,
    "trump_card_position": 10,
    "bid_min": 0,
    "bid_max": 3,
    "default_bid": 1,
    "exact_base": 30,
    "exact_per_bid": 5,
    "miss_penalty_per_trick": 10,
    "wizard_strength": 100,
    "trump_strength_bonus": 20,
    "jester_strength": 0,
    "offsuit_strength": -1,
    "no_card_strength": -1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player holds this hand, such as 'R5', 'B1', 'G8', 'W1', 'W2', 'J1', 'J2'.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's bid this hand (0-3). It is revealed after the simultaneous poll.",
        "observable": true
      },
      {
        "key": "tricks_taken",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won so far this hand.",
        "observable": true
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this player played in the current trick (empty if not yet played).",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total score.",
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
        "meaning": "The undealt cards.",
        "observable": false
      },
      {
        "key": "trump_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The face-up 10th card of this hand.",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "'R', 'B' or 'G' if the trump card is suited; 'none' if it is a Wizard or a Jester.",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current hand, 1-12.",
        "observable": true
      },
      {
        "key": "hands_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of hands fully scored.",
        "observable": false
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Which trick of the hand is being played (1-3).",
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
        "initial": "",
        "meaning": "'' means no led suit yet; 'R', 'B' or 'G' is the led suit; 'none' means a Wizard came before any suited card.",
        "observable": false
      },
      {
        "key": "wizard_played",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether a Wizard has been played in the current trick.",
        "observable": false
      },
      {
        "key": "best_value",
        "type": "number",
        "visible": "none",
        "initial": -1,
        "meaning": "Strength of the card currently winning the trick.",
        "observable": false
      },
      {
        "key": "best_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "The seat currently winning the trick.",
        "observable": false
      },
      {
        "key": "played_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "All cards played so far this hand, visible to everyone.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are P1, P2 and P3. Play order is always 1 -> 2 -> 3 -> 1.",
    "Every score is set to 0, hand_number to 0, hands_done to 0, and trick_in_hand to 1.",
    "There is no talk phase."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: hand_number += 1. All 28 cards are returned to deck; every hand, played_card, bid and tricks_taken is reset to empty or 0; played_cards is cleared. Then 3 random draws are made from deck into each player's hand (remove from deck, append to hand). Then one random card is drawn from deck into trump_card. trump_suit = that card's suit letter if it is suited, else 'none'. leader = ((hand_number - 1) mod 3) + 1."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each player is sent their own hand, plus trump_card, trump_suit, hand_number and leader."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 3",
      "effect": "When trick_in_hand == 1: each player's bid is set to their answer. A missing or invalid answer sets bid = 1. Nobody sees any bid until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: all bids are announced (Seat 1, Seat 2, Seat 3)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Start of trick: led_suit = '', wizard_played = false, best_value = -1, best_seat = 0, and every played_card = ''."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "one card from the offered legal cards in their hand",
      "effect": "The card (or the fallback card from rule R9 if the answer is missing or invalid) is removed from hand, set as played_card and appended to played_cards. If it is a Wizard: strength = 100, and if led_suit == '' then led_suit = 'none'; wizard_played = true. If it is a Jester: strength = 0. If it is suited with suit s and rank r: if led_suit == '' and wizard_played == false then led_suit = s; strength = 20 + r if s == trump_suit, else r if s == led_suit, else -1. If strength > best_value, then best_value = strength and best_seat = this seat. Announced to all."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 3) + 1",
      "answer": "one card from the offered legal cards in their hand",
      "effect": "Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all."
    },
    {
      "action": "ask",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": "one card from the offered legal cards in their hand",
      "effect": "Same processing as the leader's play: remove from hand, set played_card, append to played_cards, update led_suit, wizard_played, best_value and best_seat. Announced to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "tricks_taken of seat best_seat += 1; leader = best_seat. The trick winner is announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 3: for each player, if tricks_taken == bid then score += 30 + 5 * bid, else score -= 10 * |tricks_taken - bid|. hands_done += 1. Scores, bids and tricks_taken are announced. Then tricks_taken = 0 for everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_in_hand = (trick_in_hand mod 3) + 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hands_done == 12; otherwise continue."
    }
  ],
  "ending": {
    "condition": "hands_done == 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after hand 12. The highest total wins; if two or three players tie for the highest total, they share the result (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand starts (trick_in_hand == 1), then all 28 cards are shuffled into deck and each player is dealt exactly 3 cards into their hand, seen only by them."
    },
    {
      "id": "R2",
      "text": "When the 10th card (the trump card) is suited, then trump_suit is its suit; when it is a Wizard or a Jester, then trump_suit is 'none' for that hand."
    },
    {
      "id": "R3",
      "text": "When bidding, then all three players bid 0, 1, 2 or 3 simultaneously, and a missing or invalid bid becomes 1; all bids are then revealed, and they need not sum to 3."
    },
    {
      "id": "R4",
      "text": "When hand h starts, then the first leader is seat ((h - 1) mod 3) + 1: P1 for hands 1, 4, 7, 10; P2 for hands 2, 5, 8, 11; P3 for hands 3, 6, 9, 12."
    },
    {
      "id": "R5",
      "text": "When a trick is played, then the leader plays first, then the next seat in order 1 -> 2 -> 3 -> 1, then the third seat, each card face up."
    },
    {
      "id": "R6",
      "text": "When the first suited card of a trick is played and no Wizard was played before it, then its suit becomes the led suit; when a Wizard is played before any suited card, then the trick has no led suit."
    },
    {
      "id": "R7",
      "text": "When there is a led suit and a player holds a card of it, then they may play only a Wizard, a Jester or a card of the led suit; otherwise any card they hold is legal."
    },
    {
      "id": "R8",
      "text": "When a Wizard or a Jester is played, then it is always legal."
    },
    {
      "id": "R9",
      "text": "When a player's choice is missing or not a legal card they hold, then the engine plays, in order of priority: (a) their lowest led-suit card if a led suit exists and they hold one; (b) else a Jester; (c) else their lowest suited card, with ties broken Red, then Blue, then Green; (d) else a Wizard."
    },
    {
      "id": "R10",
      "text": "When any Wizard is played in a trick, then the first Wizard played wins the trick."
    },
    {
      "id": "R11",
      "text": "When no Wizard is played but at least one trump-suit card is, then the highest-ranked trump card wins the trick."
    },
    {
      "id": "R12",
      "text": "When no Wizard and no trump is played, then the highest-ranked card of the led suit wins the trick."
    },
    {
      "id": "R13",
      "text": "When no card qualifies under R10-R12, then the first Jester played wins the trick."
    },
    {
      "id": "R14",
      "text": "When a trick ends, then its winner's tricks_taken increases by 1 and that player leads the next trick of the hand."
    },
    {
      "id": "R15",
      "text": "When a card is played, then it stays visible in played_cards for the rest of the hand."
    },
    {
      "id": "R16",
      "text": "When a hand ends and a player's tricks_taken equals their bid, then they score 30 + 5 x bid (bid 0 = 30, 1 = 35, 2 = 40, 3 = 45)."
    },
    {
      "id": "R17",
      "text": "When a hand ends and a player's tricks_taken differs from their bid, then they lose 10 x |tricks_taken - bid| points (for example, bid 2 and take 0 = -20)."
    },
    {
      "id": "R18",
      "text": "When a hand ends, then scores, bids and tricks taken are announced, and tricks_taken resets to 0."
    },
    {
      "id": "R19",
      "text": "When hand 12 (round 36) has been scored, then the game ends and the highest total score wins; a tie for the highest total is a draw."
    }
  ],
  "offers": [
    {
      "question": "Bid at the start of each hand",
      "who": "all three seats, simultaneously",
      "options": "0, 1, 2 or 3"
    },
    {
      "question": "Card to play in a trick",
      "who": "the seat whose turn it is (leader, then the next seat, then the third)",
      "options": "If led_suit is 'R', 'B' or 'G' and the seat holds a card of that suit: only their cards of the led suit plus any Wizards and Jesters they hold. Otherwise (no led suit yet, led_suit 'none', or no card of the led suit held): every card in their hand."
    }
  ],
  "choices": [
    {
      "what": "3 players (min = max = suggested = 3)",
      "why": "The designer fixed the table at 3, and the lead rotation, 3-card hands and deck size are built for exactly 3 seats."
    },
    {
      "what": "No talk step",
      "why": "The rules say explicitly that there is no talk phase. The strategy lies in judging hand strength for the bid and in playing to hit the bid exactly, including ducking tricks."
    },
    {
      "what": "Card codes such as 'R5', 'W1', 'J2'",
      "why": "These give a text form for cards in list attributes, so suits and ranks can be compared arithmetically."
    },
    {
      "what": "Trick winner tracked by a running strength value (Wizard 100, trump 20 + rank, led suit = rank, Jester 0, off-suit -1), replaced only when strictly greater",
      "why": "This reproduces rule (9) by arithmetic. A strict comparison keeps the first Wizard and the first Jester winning ties."
    },
    {
      "what": "Only legal cards are offered",
      "why": "This enforces rule (7) directly. The fallback priority of rule (8) still applies to missing or invalid answers."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is a shared win rather than a labelled draw",
      "why": "The engine has no separate draw outcome: players level at the top share the win."
    },
    {
      "what": "The trump card is drawn at random from the remaining deck rather than taken as the literal 10th card",
      "why": "With a random shuffle the two are equivalent."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: bid, tricks_taken, played_card, score; table: trump_card, trump_suit, hand_number.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "R1: a new hand deals 3 cards to each seat and turns 1 trump card (deck 28-9-1=18); after the first trick each hand holds 2 (the deal is random, only counts are asserted)",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "expect": {
      "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "R2: with a Jester as trump card trump_suit is none, so no suit is trump and the led R2 beats off-suit 8s",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R2"], "tricks_taken": 0},
        "2": {"hand": ["B8"], "tricks_taken": 0},
        "3": {"hand": ["G8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "J1", "trump_suit": "none", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "R2"},
      {"seat": 2, "options_include": "B8"},
      {"seat": 3, "options_include": "G8"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
      "game": {"trump_suit": "none"}
    }
  },
  {
    "name": "R3: bids are set from each seat's answer and need not sum to 3 (2, 0, 3)",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "2"},
      {"seat": 2, "options_include": "0"},
      {"seat": 3, "options_include": "3"}
    ],
    "expect": {
      "players": {"1": {"bid": 2}, "2": {"bid": 0}, "3": {"bid": 3}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "R4: after hand 1 the next hand is hand 2 and a new 3-card hand is dealt (chance-independent counts only)",
    "rule": "R4",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"trick_in_hand": 1, "hand_number": 1, "hands_done": 1}},
    "expect": {
      "game": {"hand_number": 2},
      "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}
    }
  },
  {
    "name": "R5: the leader (seat 3) plays first, so its B5 sets the led suit and wins over off-suit R8 and R7",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["R7"], "tricks_taken": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 3, "trump_card": "G1", "trump_suit": "G", "hand_number": 3}
    },
    "expect": {
      "players": {
        "1": {"tricks_taken": 0, "played_card": "R8"},
        "2": {"tricks_taken": 0, "played_card": "R7"},
        "3": {"tricks_taken": 1, "played_card": "B5"}
      }
    }
  },
  {
    "name": "R6: a Wizard led means there is no led suit, so later seats may play any card",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1", "R1"], "tricks_taken": 0},
        "2": {"hand": ["R8", "B3"], "tricks_taken": 0},
        "3": {"hand": ["B8", "R2"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "W1"},
      {"seat": 2, "options_include": "B3"},
      {"seat": 3, "options_include": "R2"}
    ],
    "expect": {
      "offered": [{"seat": 2, "option": "R8"}, {"seat": 2, "option": "B3"}, {"seat": 3, "option": "B8"}, {"seat": 3, "option": "R2"}],
      "players": {"1": {"tricks_taken": 1}, "2": {"played_card": "B3"}, "3": {"played_card": "R2"}}
    }
  },
  {
    "name": "R6: after a Jester lead, the first suited card (R3) sets the led suit, so seat 3 must follow red and wins with R5",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["J1"], "tricks_taken": 0},
        "2": {"hand": ["R3"], "tricks_taken": 0},
        "3": {"hand": ["R5", "B8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 3, "options_include": "R5"}],
    "expect": {
      "not_offered": [{"seat": 3, "option": "B8"}],
      "players": {"3": {"tricks_taken": 1, "played_card": "R5"}, "1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R7: a seat holding the led suit may play only led-suit cards, Wizards or Jesters; a seat without it may play anything",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R2", "B8", "J1"], "tricks_taken": 0},
        "3": {"hand": ["B5", "G6"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "B1", "trump_suit": "B", "hand_number": 1}
    },
    "rules": [
      {"seat": 2, "options_include": "R2"},
      {"seat": 3, "options_include": "G6"}
    ],
    "expect": {
      "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "J1"}, {"seat": 3, "option": "B5"}, {"seat": 3, "option": "G6"}],
      "not_offered": [{"seat": 2, "option": "B8"}],
      "players": {"1": {"tricks_taken": 1}, "2": {"played_card": "R2"}, "3": {"played_card": "G6"}}
    }
  },
  {
    "name": "R8: a Wizard is legal even when holding the led suit, and it wins",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R2", "W2"], "tricks_taken": 0},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 2, "options_include": "W2"}],
    "expect": {
      "offered": [{"seat": 2, "option": "W2"}],
      "players": {"2": {"tricks_taken": 1, "played_card": "W2"}, "1": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R9: an illegal answer (B8 while holding red) is replaced by the lowest led-suit card, R2",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R6", "R2", "B8"], "tricks_taken": 0},
        "3": {"hand": ["R1"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 2, "options_include": "R6", "answer": "B8"}],
    "expect": {
      "players": {"2": {"played_card": "R2", "tricks_taken": 0}, "1": {"tricks_taken": 1}, "3": {"played_card": "R1"}}
    }
  },
  {
    "name": "R10: the first Wizard played wins, even over a second Wizard and a trump",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["W1"], "tricks_taken": 0},
        "3": {"hand": ["W2"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "R1", "trump_suit": "R", "hand_number": 1}
    },
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R11: with no Wizard, the highest trump wins (G3 beats G1 and led R8)",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["G1"], "tricks_taken": 0},
        "3": {"hand": ["G3"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}
    }
  },
  {
    "name": "R12: with no Wizard or trump, the highest led-suit card wins (B6 beats B3 and off-suit R8)",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["B3"], "tricks_taken": 0},
        "2": {"hand": ["B6"], "tricks_taken": 0},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R13: two Jesters led do not win when a suited card follows; R1 sets the led suit and wins",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["J1"], "tricks_taken": 0},
        "2": {"hand": ["J2"], "tricks_taken": 0},
        "3": {"hand": ["R1"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}
    }
  },
  {
    "name": "R14: the trick winner (seat 2) leads the next trick, and its R1 lead then wins; all three hit their bids",
    "rule": "R14",
    "players": 3,
    "rounds": 2,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R3", "B8"], "tricks_taken": 1, "bid": 1, "score": 0},
        "2": {"hand": ["R7", "R1"], "tricks_taken": 0, "bid": 2, "score": 0},
        "3": {"hand": ["R5", "B2"], "tricks_taken": 0, "bid": 0, "score": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "J1", "trump_suit": "none", "hand_number": 1, "hands_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "R3"},
      {"seat": 2, "options_include": "R7"},
      {"seat": 3, "options_include": "R5"}
    ],
    "expect": {
      "players": {
        "1": {"score": 35, "played_card": "B8", "tricks_taken": 0},
        "2": {"score": 40, "played_card": "R1", "tricks_taken": 0},
        "3": {"score": 30, "played_card": "B2", "tricks_taken": 0}
      }
    }
  },
  {
    "name": "R15: cards played stay in played_cards for the hand (3 earlier + 3 now = 6)",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["B3"], "tricks_taken": 0},
        "2": {"hand": ["B6"], "tricks_taken": 1},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "played_cards": ["R1", "R2", "R3"]}
    },
    "expect": {
      "lens": {"game": {"played_cards": 6}},
      "players": {"2": {"tricks_taken": 2}}
    }
  },
  {
    "name": "R16: exact bids score 30 + 5 x bid (bid 3: +45, bid 0: +30, bid 1: +35)",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 2, "bid": 3, "score": 10},
        "2": {"hand": ["R1"], "tricks_taken": 0, "bid": 0, "score": 0},
        "3": {"hand": ["B2"], "tricks_taken": 1, "bid": 1, "score": -10}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "expect": {
      "players": {"1": {"score": 55}, "2": {"score": 30}, "3": {"score": 25}}
    }
  },
  {
    "name": "R17: missed bids lose 10 per trick of difference (-10, -20, -10)",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0, "bid": 2, "score": 0},
        "2": {"hand": ["R2"], "tricks_taken": 2, "bid": 0, "score": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0, "bid": 1, "score": 0}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "expect": {
      "players": {"1": {"score": -10}, "2": {"score": -20}, "3": {"score": -10}}
    }
  },
  {
    "name": "R18: after scoring, tricks_taken resets to 0 for everyone while bids stay as announced",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 1, "bid": 2, "score": 0},
        "2": {"hand": ["R2"], "tricks_taken": 1, "bid": 1, "score": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0, "bid": 0, "score": 0}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "expect": {
      "players": {
        "1": {"tricks_taken": 0, "bid": 2, "score": 40},
        "2": {"tricks_taken": 0, "bid": 1, "score": 35},
        "3": {"tricks_taken": 0, "bid": 0, "score": 30}
      }
    }
  },
  {
    "name": "R19: after hand 12 is scored the game ends and the highest total wins (135 vs 80 vs 130)",
    "rule": "R19",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 0, "bid": 1, "score": 100},
        "2": {"hand": ["R3"], "tricks_taken": 1, "bid": 0, "score": 90},
        "3": {"hand": ["B4"], "tricks_taken": 1, "bid": 1, "score": 95}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 12, "hands_done": 11}
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 135, "2": 80, "3": 130}
    }
  },
  {
    "name": "R19: a tie for the highest final total is shared (seats 1 and 3 on 135)",
    "rule": "R19",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 0, "bid": 1, "score": 100},
        "2": {"hand": ["R3"], "tricks_taken": 2, "bid": 2, "score": 50},
        "3": {"hand": ["B4"], "tricks_taken": 0, "bid": 0, "score": 105}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 12, "hands_done": 11}
    },
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 135, "2": 90, "3": 135}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "R1: a new hand deals 3 cards to each seat and turns 1 trump card (deck 28-9-1=18); after the first trick each hand holds 2 (the deal is random, only counts are asserted)",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "1"},
      {"seat": 2, "options_include": "1"},
      {"seat": 3, "options_include": "1"}
    ],
    "expect": {
      "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "R2: with a Jester as trump card trump_suit is none, so no suit is trump and the led R2 beats off-suit 8s",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R2"], "tricks_taken": 0},
        "2": {"hand": ["B8"], "tricks_taken": 0},
        "3": {"hand": ["G8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "J1", "trump_suit": "none", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "R2"},
      {"seat": 2, "options_include": "B8"},
      {"seat": 3, "options_include": "G8"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
      "game": {"trump_suit": "none"}
    }
  },
  {
    "name": "R3: bids are set from each seat's answer and need not sum to 3 (2, 0, 3)",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "2"},
      {"seat": 2, "options_include": "0"},
      {"seat": 3, "options_include": "3"}
    ],
    "expect": {
      "players": {"1": {"bid": 2}, "2": {"bid": 0}, "3": {"bid": 3}},
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "R4: after hand 1 the next hand is hand 2 and a new 3-card hand is dealt (chance-independent counts only)",
    "rule": "R4",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"trick_in_hand": 1, "hand_number": 1, "hands_done": 1}},
    "rules": [
      {"seat": 1, "options_include": "1"},
      {"seat": 2, "options_include": "1"},
      {"seat": 3, "options_include": "1"}
    ],
    "expect": {
      "game": {"hand_number": 2},
      "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}
    }
  },
  {
    "name": "R5: the leader (seat 3) plays first, so its B5 sets the led suit and wins over off-suit R8 and R7",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["R7"], "tricks_taken": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 3, "trump_card": "G1", "trump_suit": "G", "hand_number": 3}
    },
    "rules": [
      {"seat": 3, "options_include": "B5"},
      {"seat": 1, "options_include": "R8"},
      {"seat": 2, "options_include": "R7"}
    ],
    "expect": {
      "players": {
        "1": {"tricks_taken": 0, "played_card": "R8"},
        "2": {"tricks_taken": 0, "played_card": "R7"},
        "3": {"tricks_taken": 1, "played_card": "B5"}
      }
    }
  },
  {
    "name": "R6: a Wizard led means there is no led suit, so later seats may play any card",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1", "R1"], "tricks_taken": 0},
        "2": {"hand": ["R8", "B3"], "tricks_taken": 0},
        "3": {"hand": ["B8", "R2"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "W1"},
      {"seat": 2, "options_include": "B3"},
      {"seat": 3, "options_include": "R2"}
    ],
    "expect": {
      "offered": [{"seat": 2, "option": "R8"}, {"seat": 2, "option": "B3"}, {"seat": 3, "option": "B8"}, {"seat": 3, "option": "R2"}],
      "players": {"1": {"tricks_taken": 1}, "2": {"played_card": "B3"}, "3": {"played_card": "R2"}}
    }
  },
  {
    "name": "R6: after a Jester lead, the first suited card (R3) sets the led suit, so seat 3 must follow red and wins with R5",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["J1"], "tricks_taken": 0},
        "2": {"hand": ["R3"], "tricks_taken": 0},
        "3": {"hand": ["R5", "B8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 3, "options_include": "R5"}],
    "expect": {
      "not_offered": [{"seat": 3, "option": "B8"}],
      "players": {"3": {"tricks_taken": 1, "played_card": "R5"}, "1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R7: a seat holding the led suit may play only led-suit cards, Wizards or Jesters; a seat without it may play anything",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R2", "B8", "J1"], "tricks_taken": 0},
        "3": {"hand": ["B5", "G6"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "B1", "trump_suit": "B", "hand_number": 1}
    },
    "rules": [
      {"seat": 2, "options_include": "R2"},
      {"seat": 3, "options_include": "G6"}
    ],
    "expect": {
      "offered": [{"seat": 2, "option": "R2"}, {"seat": 2, "option": "J1"}, {"seat": 3, "option": "B5"}, {"seat": 3, "option": "G6"}],
      "not_offered": [{"seat": 2, "option": "B8"}],
      "players": {"1": {"tricks_taken": 1}, "2": {"played_card": "R2"}, "3": {"played_card": "G6"}}
    }
  },
  {
    "name": "R8: a Wizard is legal even when holding the led suit, and it wins",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R2", "W2"], "tricks_taken": 0},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 2, "options_include": "W2"}],
    "expect": {
      "offered": [{"seat": 2, "option": "W2"}],
      "players": {"2": {"tricks_taken": 1, "played_card": "W2"}, "1": {"tricks_taken": 0}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R9: an illegal answer (B8 while holding red) is replaced by the lowest led-suit card, R2",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R4"], "tricks_taken": 0},
        "2": {"hand": ["R6", "R2", "B8"], "tricks_taken": 0},
        "3": {"hand": ["R1"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G1", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [{"seat": 2, "options_include": "R6", "answer": "B8"}],
    "expect": {
      "players": {"2": {"played_card": "R2", "tricks_taken": 0}, "1": {"tricks_taken": 1}, "3": {"played_card": "R1"}}
    }
  },
  {
    "name": "R10: the first Wizard played wins, even over a second Wizard and a trump",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["W1"], "tricks_taken": 0},
        "3": {"hand": ["W2"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "R1", "trump_suit": "R", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "R8"},
      {"seat": 2, "options_include": "W1"},
      {"seat": 3, "options_include": "W2"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R11: with no Wizard, the highest trump wins (G3 beats G1 and led R8)",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0},
        "2": {"hand": ["G1"], "tricks_taken": 0},
        "3": {"hand": ["G3"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "R8"},
      {"seat": 2, "options_include": "G1"},
      {"seat": 3, "options_include": "G3"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}
    }
  },
  {
    "name": "R12: with no Wizard or trump, the highest led-suit card wins (B6 beats B3 and off-suit R8)",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["B3"], "tricks_taken": 0},
        "2": {"hand": ["B6"], "tricks_taken": 0},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "B3"},
      {"seat": 2, "options_include": "B6"},
      {"seat": 3, "options_include": "R8"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "R13: two Jesters led do not win when a suited card follows; R1 sets the led suit and wins",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["J1"], "tricks_taken": 0},
        "2": {"hand": ["J2"], "tricks_taken": 0},
        "3": {"hand": ["R1"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "J1"},
      {"seat": 2, "options_include": "J2"},
      {"seat": 3, "options_include": "R1"}
    ],
    "expect": {
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 1}}
    }
  },
  {
    "name": "R14: the trick winner (seat 2) leads the next trick, and its R1 lead then wins; all three hit their bids",
    "rule": "R14",
    "players": 3,
    "rounds": 2,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R3", "B8"], "tricks_taken": 1, "bid": 1, "score": 0},
        "2": {"hand": ["R7", "R1"], "tricks_taken": 0, "bid": 2, "score": 0},
        "3": {"hand": ["R5", "B2"], "tricks_taken": 0, "bid": 0, "score": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "J1", "trump_suit": "none", "hand_number": 1, "hands_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "R3"},
      {"seat": 2, "options_include": "R7"},
      {"seat": 3, "options_include": "R5"}
    ],
    "expect": {
      "players": {
        "1": {"score": 35, "played_card": "B8", "tricks_taken": 0},
        "2": {"score": 40, "played_card": "R1", "tricks_taken": 0},
        "3": {"score": 30, "played_card": "B2", "tricks_taken": 0}
      }
    }
  },
  {
    "name": "R15: cards played stay in played_cards for the hand (3 earlier + 3 now = 6)",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["B3"], "tricks_taken": 0},
        "2": {"hand": ["B6"], "tricks_taken": 1},
        "3": {"hand": ["R8"], "tricks_taken": 0}
      },
      "game": {"trick_in_hand": 2, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "played_cards": ["R1", "R2", "R3"]}
    },
    "rules": [
      {"seat": 1, "options_include": "B3"},
      {"seat": 2, "options_include": "B6"},
      {"seat": 3, "options_include": "R8"}
    ],
    "expect": {
      "lens": {"game": {"played_cards": 6}},
      "players": {"2": {"tricks_taken": 2}}
    }
  },
  {
    "name": "R16: exact bids score 30 + 5 x bid (bid 3: +45, bid 0: +30, bid 1: +35)",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 2, "bid": 3, "score": 10},
        "2": {"hand": ["R1"], "tricks_taken": 0, "bid": 0, "score": 0},
        "3": {"hand": ["B2"], "tricks_taken": 1, "bid": 1, "score": -10}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "W1"},
      {"seat": 2, "options_include": "R1"},
      {"seat": 3, "options_include": "B2"}
    ],
    "expect": {
      "players": {"1": {"score": 55}, "2": {"score": 30}, "3": {"score": 25}}
    }
  },
  {
    "name": "R17: missed bids lose 10 per trick of difference (-10, -20, -10)",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 0, "bid": 2, "score": 0},
        "2": {"hand": ["R2"], "tricks_taken": 2, "bid": 0, "score": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0, "bid": 1, "score": 0}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "R8"},
      {"seat": 2, "options_include": "R2"},
      {"seat": 3, "options_include": "B5"}
    ],
    "expect": {
      "players": {"1": {"score": -10}, "2": {"score": -20}, "3": {"score": -10}}
    }
  },
  {
    "name": "R18: after scoring, tricks_taken resets to 0 for everyone while bids stay as announced",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["R8"], "tricks_taken": 1, "bid": 2, "score": 0},
        "2": {"hand": ["R2"], "tricks_taken": 1, "bid": 1, "score": 0},
        "3": {"hand": ["B5"], "tricks_taken": 0, "bid": 0, "score": 0}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 1, "hands_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "R8"},
      {"seat": 2, "options_include": "R2"},
      {"seat": 3, "options_include": "B5"}
    ],
    "expect": {
      "players": {
        "1": {"tricks_taken": 0, "bid": 2, "score": 40},
        "2": {"tricks_taken": 0, "bid": 1, "score": 35},
        "3": {"tricks_taken": 0, "bid": 0, "score": 30}
      }
    }
  },
  {
    "name": "R19: after hand 12 is scored the game ends and the highest total wins (135 vs 80 vs 130)",
    "rule": "R19",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 0, "bid": 1, "score": 100},
        "2": {"hand": ["R3"], "tricks_taken": 1, "bid": 0, "score": 90},
        "3": {"hand": ["B4"], "tricks_taken": 1, "bid": 1, "score": 95}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 12, "hands_done": 11}
    },
    "rules": [
      {"seat": 1, "options_include": "W1"},
      {"seat": 2, "options_include": "R3"},
      {"seat": 3, "options_include": "B4"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 135, "2": 80, "3": 130}
    }
  },
  {
    "name": "R19: a tie for the highest final total is shared (seats 1 and 3 on 135)",
    "rule": "R19",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["W1"], "tricks_taken": 0, "bid": 1, "score": 100},
        "2": {"hand": ["R3"], "tricks_taken": 2, "bid": 2, "score": 50},
        "3": {"hand": ["B4"], "tricks_taken": 0, "bid": 0, "score": 105}
      },
      "game": {"trick_in_hand": 3, "leader": 1, "trump_card": "G5", "trump_suit": "G", "hand_number": 12, "hands_done": 11}
    },
    "rules": [
      {"seat": 1, "options_include": "W1"},
      {"seat": 2, "options_include": "R3"},
      {"seat": 3, "options_include": "B4"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 135, "2": 90, "3": 135}
    }
  }
]
```
````
