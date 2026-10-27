# 63 scenarios

- time: 2026-10-27T10:32:00+00:00 (64.8s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e6ebcf2ef61003b0, reply sha256 9b056156dc6de7cc

## Sent

````
SPEC:
{
  "name": "Lost Cities: Wager Draft",
  "summary": "Two players draft face-up cards from a 27-card, three-colour deck over 12 rounds. They build rising expeditions, pay 3 for every burial, and score a secret colour Wager at double.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 27,
    "colours": 3,
    "min_card_value": 2,
    "max_card_value": 10,
    "rounds": 12,
    "row_size": 2,
    "wager_round": 5,
    "burial_penalty": 3,
    "empty_wager_score": -15,
    "empty_expedition_score": 0,
    "base_offset": 10,
    "wager_multiplier": 2,
    "bonus_threshold": 25,
    "bonus": 10,
    "cards_left_unrevealed": 3
  },
  "attributes": {
    "player": [
      {
        "key": "red_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "top value of the Red expedition (0 when empty)",
        "observable": true
      },
      {
        "key": "red_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "sum of the Red expedition",
        "observable": true
      },
      {
        "key": "blue_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "top value of the Blue expedition (0 when empty)",
        "observable": true
      },
      {
        "key": "blue_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "sum of the Blue expedition",
        "observable": true
      },
      {
        "key": "green_top",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "top value of the Green expedition (0 when empty)",
        "observable": true
      },
      {
        "key": "green_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "sum of the Green expedition",
        "observable": true
      },
      {
        "key": "burial",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Burial penalty, rising by 3 per buried card",
        "observable": true
      },
      {
        "key": "wager",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "secret Wager colour (Red, Blue or Green), named in round 5 and revealed at the end",
        "observable": false
      },
      {
        "key": "choice",
        "type": "text",
        "visible": "public",
        "initial": "NONE",
        "meaning": "this round's pick: A, B or NONE (an already-taken card is recorded as NONE)",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "final total, the sum of the three colour scores minus burial, computed after round 12",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red-2",
          "Red-3",
          "Red-4",
          "Red-5",
          "Red-6",
          "Red-7",
          "Red-8",
          "Red-9",
          "Red-10",
          "Blue-2",
          "Blue-3",
          "Blue-4",
          "Blue-5",
          "Blue-6",
          "Blue-7",
          "Blue-8",
          "Blue-9",
          "Blue-10",
          "Green-2",
          "Green-3",
          "Green-4",
          "Green-5",
          "Green-6",
          "Green-7",
          "Green-8",
          "Green-9",
          "Green-10"
        ],
        "meaning": "the shuffled face-down deck",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number, 1 to 12",
        "observable": true
      },
      {
        "key": "priority_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "seat with priority this round: 1 in odd rounds, 2 in even rounds",
        "observable": true
      },
      {
        "key": "card_a_colour",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of face-up Card A",
        "observable": false
      },
      {
        "key": "card_a_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "value of face-up Card A",
        "observable": false
      },
      {
        "key": "card_b_colour",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of face-up Card B",
        "observable": false
      },
      {
        "key": "card_b_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "value of face-up Card B",
        "observable": false
      },
      {
        "key": "taken",
        "type": "text",
        "visible": "public",
        "initial": "NONE",
        "meaning": "which card the priority player took this round (A, B or NONE)",
        "observable": false
      }
    ]
  },
  "setup": [
    "The table deck is filled with the 27 cards Red, Blue and Green 2 to 10 and shuffled once (cards are later drawn from it at random). Both players are told this composition.",
    "Each player's six expedition values (red_top, red_sum, blue_top, blue_sum, green_top, green_sum) and their burial start at 0, all public.",
    "Each player's wager starts empty and score starts at 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; priority_seat = 1 if round is odd, else 2; taken = NONE; every player's choice = NONE. Announce: 'Round {round}: seat {priority_seat} has priority.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of Red, Blue, Green",
      "effect": "when round == 5: each player's wager = their answer. Nobody sees another's wager. This runs before Card A and Card B are revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Draw one card at random from deck and remove it: card_a_colour and card_a_value are set from it. Draw another and remove it: card_b_colour and card_b_value are set from it. Announce both cards to both players."
    },
    {
      "action": "ask",
      "who": "seat {priority_seat}",
      "answer": "one of A, B, NONE",
      "effect": "the priority player's choice = answer; taken = answer. Both players are told what was chosen."
    },
    {
      "action": "update",
      "who": "seat {priority_seat}",
      "answer": null,
      "effect": "If choice is A or B, place that card (colour C, value v) for the priority player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game."
    },
    {
      "action": "ask",
      "who": "the seat that is not priority_seat",
      "answer": "one of A, B, NONE",
      "effect": "choice = answer, except that choice = NONE if answer equals taken."
    },
    {
      "action": "update",
      "who": "the seat that is not priority_seat",
      "answer": null,
      "effect": "If choice is A or B, place that card (colour C, value v) for this player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Any card in the row that nobody took is removed from the game. Announce both choices, where each card went (added or buried), every player's red/blue/green top and sum, and every player's burial."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round == 12: for each colour C, colour_score = (C_sum == 0 ? (wager == C ? -15 : 0) : (C_sum - 10) * (wager == C ? 2 : 1) + (C_sum >= 25 ? 10 : 0)); score = red score + blue score + green score - burial. Reveal each player's wager publicly and announce the totals. The 3 cards left in the deck are never revealed."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round >= 12, otherwise continue"
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final total (the three colour scores minus the Burial penalty). The higher total wins, and equal totals share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup the deck holds exactly 27 cards, Red, Blue and Green each valued 2 to 10, and every expedition top, sum and burial is 0."
    },
    {
      "id": "R2",
      "text": "When the round is odd, priority_seat is 1. When it is even, priority_seat is 2."
    },
    {
      "id": "R3",
      "text": "Each round, two cards are drawn from the deck as Card A and Card B and shown to both players, so the deck shrinks by 2 per round and holds 3 cards after round 12."
    },
    {
      "id": "R4",
      "text": "When round is 5, both players name a Wager of Red, Blue or Green simultaneously, before that round's cards are revealed. The Wager is never changed and stays hidden until the end."
    },
    {
      "id": "R5",
      "text": "The priority player chooses A, B or NONE first. The other player is then told that choice and chooses A, B or NONE."
    },
    {
      "id": "R6",
      "text": "When the second player names the card the priority player already took, their choice counts as NONE and they receive nothing."
    },
    {
      "id": "R7",
      "text": "When a player receives a card of colour C and value v, and v is greater than C_top, then C_top becomes v and C_sum rises by v (for example, Red 7 on an empty Red gives red_top 7 and red_sum 7)."
    },
    {
      "id": "R8",
      "text": "When a player receives a card of colour C and value v, and v is not greater than C_top, the card is buried and that player's burial rises by 3 (for example, Red 5 on red_top 7 gives burial +3)."
    },
    {
      "id": "R9",
      "text": "When a player chooses NONE, none of their attributes change."
    },
    {
      "id": "R10",
      "text": "Cards in the row that nobody took are removed from the game."
    },
    {
      "id": "R11",
      "text": "After each round, both choices, where each card went, all expedition tops and sums, and both burials are announced."
    },
    {
      "id": "R12",
      "text": "At final scoring, an empty expedition scores 0, unless it is in the player's Wager colour, in which case it scores -15."
    },
    {
      "id": "R13",
      "text": "At final scoring, a non-empty expedition's base is its sum minus 10 (for example, sum 18 gives base 8 and sum 6 gives base -4)."
    },
    {
      "id": "R14",
      "text": "When the expedition is in the player's Wager colour, its base is doubled, negative or not (for example, sum 6 gives -8 and sum 18 gives 16)."
    },
    {
      "id": "R15",
      "text": "When a non-empty expedition's sum is 25 or more, it gains 10 after any doubling (for example, a Wager-colour sum of 27 scores 2*17 + 10 = 44)."
    },
    {
      "id": "R16",
      "text": "A player's score is the sum of their three colour scores minus their burial."
    },
    {
      "id": "R17",
      "text": "The game ends after round 12. Wagers are then revealed, the higher score wins, and equal scores are a draw."
    }
  ],
  "offers": [
    {
      "question": "Wager (round 5 only)",
      "who": "both seats, simultaneously",
      "options": "Red, Blue, Green"
    },
    {
      "question": "Priority pick",
      "who": "seat {priority_seat}",
      "options": "A, B, NONE"
    },
    {
      "question": "Second pick",
      "who": "the non-priority seat",
      "options": "A, B, NONE (naming the card already taken is accepted but counts as NONE)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players, suggested 2",
      "why": "The designer fixed the table at 2. The draft is a head-to-head contest over a shared row, and the second pick depends on reading the one opponent."
    },
    {
      "what": "No talk step",
      "why": "The rules include no talk, and with two players in direct competition a message would add nothing the rules ask for."
    },
    {
      "what": "Cards stored as 'Colour-Value' strings in the deck, split into card_a/card_b colour and value attributes when drawn",
      "why": "This lets placement and scoring be done by plain arithmetic comparisons on numbers."
    },
    {
      "what": "The second player is still offered the taken card",
      "why": "The rules say that naming the taken card counts as NONE, so the option exists and is resolved to NONE."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player times the Wager against the cards already seen in rounds 1 to 4. They also deny the opponent high cards, avoid burials that cost 3, and take NONE rather than bury a card."
    }
  ],
  "simplifications": [
    {
      "what": "The 'shuffle once, take the top two' draw is done as two random draws from the deck list each round",
      "why": "The engine draws at random from a list. This is equivalent to drawing from the top of a shuffled deck."
    },
    {
      "what": "Removed and buried cards are not kept in a discard list",
      "why": "The rules take them out of the game and never refer to them again. Only the burial counter matters."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: red_top, red_sum, blue_top, blue_sum, green_top, green_sum, burial, score; table: round, priority_seat.
````

## Reply

````
```json
[
  {
    "name": "Setup: 27-card deck, all expeditions and burials at 0",
    "rule": "R1",
    "players": 2,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"deck": 27}},
      "players": {
        "1": {"red_top": 0, "red_sum": 0, "blue_top": 0, "blue_sum": 0, "green_top": 0, "green_sum": 0, "burial": 0},
        "2": {"red_top": 0, "red_sum": 0, "blue_top": 0, "blue_sum": 0, "green_top": 0, "green_sum": 0, "burial": 0}
      },
      "game": {"round": 0}
    }
  },
  {
    "name": "Odd round 1 gives priority to seat 1",
    "rule": "R2",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "rules": [],
    "expect": {"game": {"round": 1, "priority_seat": 1}}
  },
  {
    "name": "Even round 2 gives priority to seat 2",
    "rule": "R2",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"round": 1}},
    "rules": [],
    "expect": {"game": {"round": 2, "priority_seat": 2}}
  },
  {
    "name": "One round draws two cards, so the deck shrinks from 27 to 25",
    "rule": "R3",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "rules": [],
    "expect": {"lens": {"game": {"deck": 25}}, "game": {"round": 1}}
  },
  {
    "name": "Both seats are offered a Wager colour in round 5",
    "rule": "R4",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"round": 4}},
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Green"}
    ],
    "expect": {
      "game": {"round": 5},
      "offered": [
        {"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"},
        {"seat": 2, "option": "Red"}, {"seat": 2, "option": "Blue"}, {"seat": 2, "option": "Green"}
      ]
    }
  },
  {
    "name": "No Wager is asked outside round 5",
    "rule": "R4",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"round": 5}},
    "rules": [],
    "expect": {
      "game": {"round": 6},
      "not_offered": [
        {"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"},
        {"seat": 2, "option": "Red"}, {"seat": 2, "option": "Blue"}, {"seat": 2, "option": "Green"}
      ]
    }
  },
  {
    "name": "Priority seat picks, then the other seat picks the other card",
    "rule": "R5",
    "players": 2,
    "rounds": 1,
    "given": {"game": {"deck": ["Red-7", "Red-7"]}},
    "rules": [
      {"seat": 1, "options_include": "A"},
      {"seat": 2, "options_include": "B"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "A"}, {"seat": 1, "option": "B"}, {"seat": 1, "option": "NONE"},
        {"seat": 2, "option": "A"}, {"seat": 2, "option": "B"}, {"seat": 2, "option": "NONE"}
      ],
      "players": {
        "1": {"red_top": 7, "red_sum": 7, "burial": 0},
        "2": {"red_top": 7, "red_sum": 7, "burial": 0}
      }
    }
  },
  {
    "name": "Second seat naming the taken card gets nothing",
    "rule": "R6",
    "players": 2,
    "rounds": 1,
    "given": {"game": {"deck": ["Red-7", "Red-7"]}},
    "rules": [
      {"seat": 1, "options_include": "A"},
      {"seat": 2, "options_include": "A"}
    ],
    "expect": {
      "players": {
        "1": {"red_top": 7, "red_sum": 7, "burial": 0},
        "2": {"red_top": 0, "red_sum": 0, "blue_top": 0, "blue_sum": 0, "green_top": 0, "green_sum": 0, "burial": 0}
      }
    }
  },
  {
    "name": "Red 7 on red_top 3 raises the top to 7 and the sum by 7",
    "rule": "R7",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"red_top": 3, "red_sum": 5}},
      "game": {"deck": ["Red-7", "Red-7"]}
    },
    "rules": [{"seat": 1, "options_include": "A"}],
    "expect": {"players": {"1": {"red_top": 7, "red_sum": 12, "burial": 0}}}
  },
  {
    "name": "Red 7 on an empty Red gives top 7 and sum 7",
    "rule": "R7",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"deck": ["Red-7", "Red-7"]}},
    "rules": [{"seat": 1, "options_include": "B"}],
    "expect": {"players": {"1": {"red_top": 7, "red_sum": 7, "burial": 0}}}
  },
  {
    "name": "Red 5 on red_top 7 is buried for +3 burial",
    "rule": "R8",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"red_top": 7, "red_sum": 7}},
      "game": {"deck": ["Red-5", "Red-5"]}
    },
    "rules": [{"seat": 1, "options_include": "A"}],
    "expect": {"players": {"1": {"red_top": 7, "red_sum": 7, "burial": 3}}}
  },
  {
    "name": "A card equal to the top is buried too",
    "rule": "R8",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"red_top": 7, "red_sum": 7, "burial": 3}},
      "game": {"deck": ["Red-7", "Red-7"]}
    },
    "rules": [{"seat": 1, "options_include": "A"}],
    "expect": {"players": {"1": {"red_top": 7, "red_sum": 7, "burial": 6}}}
  },
  {
    "name": "Choosing NONE changes nothing for the player",
    "rule": "R9",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"red_top": 4, "red_sum": 4, "blue_top": 6, "blue_sum": 9, "burial": 6}},
      "game": {"deck": ["Red-8", "Blue-10", "Green-2"]}
    },
    "rules": [{"seat": 1, "options_include": "NONE"}],
    "expect": {
      "players": {
        "1": {"red_top": 4, "red_sum": 4, "blue_top": 6, "blue_sum": 9, "green_top": 0, "green_sum": 0, "burial": 6}
      }
    }
  },
  {
    "name": "Untaken cards leave the game and do not return to the deck",
    "rule": "R10",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"deck": ["Red-7", "Blue-4", "Green-9"]}},
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 1}},
      "players": {
        "1": {"red_sum": 0, "blue_sum": 0, "green_sum": 0, "burial": 0},
        "2": {"red_sum": 0, "blue_sum": 0, "green_sum": 0, "burial": 0}
      }
    }
  },
  {
    "name": "After the round both players' public tops, sums and burials show the placements",
    "rule": "R11",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {"2": {"red_top": 9, "red_sum": 9}},
      "game": {"deck": ["Red-7", "Red-7"]}
    },
    "rules": [
      {"seat": 1, "options_include": "B"},
      {"seat": 2, "options_include": "A"}
    ],
    "expect": {
      "players": {
        "1": {"red_top": 7, "red_sum": 7, "burial": 0},
        "2": {"red_top": 9, "red_sum": 9, "burial": 3}
      }
    }
  },
  {
    "name": "Empty Wager colour scores -15, other empty colours score 0",
    "rule": "R12",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Red", "blue_top": 7, "blue_sum": 12},
        "2": {"wager": "Blue", "green_top": 9, "green_sum": 15}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": 2,
      "standings": {"1": -13, "2": -10},
      "players": {"1": {"score": -13}, "2": {"score": -10}},
      "game": {"round": 12}
    }
  },
  {
    "name": "Non-empty expedition base is sum minus 10",
    "rule": "R13",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Green", "green_top": 10, "green_sum": 10, "red_top": 10, "red_sum": 18, "blue_top": 4, "blue_sum": 6},
        "2": {"wager": "Red", "red_top": 10, "red_sum": 10, "blue_top": 9, "blue_sum": 13}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 4, "2": 3},
      "players": {"1": {"score": 4}, "2": {"score": 3}}
    }
  },
  {
    "name": "Wager colour doubles the base, negative or positive",
    "rule": "R14",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Red", "red_top": 4, "red_sum": 6, "blue_top": 10, "blue_sum": 18},
        "2": {"wager": "Blue", "blue_top": 10, "blue_sum": 18, "red_top": 4, "red_sum": 6}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": 2,
      "standings": {"1": 0, "2": 12},
      "players": {"1": {"score": 0}, "2": {"score": 12}}
    }
  },
  {
    "name": "Sum of 25 or more adds 10 after doubling",
    "rule": "R15",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Red", "red_top": 10, "red_sum": 27},
        "2": {"wager": "Green", "blue_top": 10, "blue_sum": 25}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 44, "2": 10},
      "players": {"1": {"score": 44}, "2": {"score": 10}}
    }
  },
  {
    "name": "Score is the three colour scores minus burial",
    "rule": "R16",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Blue", "blue_top": 10, "blue_sum": 20, "red_top": 8, "red_sum": 12, "burial": 9},
        "2": {"wager": "Red", "red_top": 9, "red_sum": 14, "green_top": 7, "green_sum": 11, "burial": 3}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 13, "2": 6},
      "players": {"1": {"score": 13}, "2": {"score": 6}}
    }
  },
  {
    "name": "Equal final scores share the win",
    "rule": "R17",
    "players": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"wager": "Red", "red_top": 9, "red_sum": 15},
        "2": {"wager": "Blue", "blue_top": 9, "blue_sum": 15}
      },
      "game": {"round": 11, "deck": ["Red-2", "Red-3", "Blue-2", "Blue-3", "Green-2"]}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 10, "2": 10},
      "players": {"1": {"score": 10}, "2": {"score": 10}},
      "game": {"round": 12}
    }
  },
  {
    "name": "Full 12-round game with no picks ends after round 12 with 3 cards left and empty Wagers at -15 each",
    "rule": "R17",
    "players": 2,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -15, "2": -15},
      "players": {"1": {"score": -15, "burial": 0}, "2": {"score": -15, "burial": 0}},
      "game": {"round": 12},
      "lens": {"game": {"deck": 3}}
    }
  }
]
```
````
