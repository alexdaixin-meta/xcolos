# 04 scenarios

- time: 2026-10-27T17:11:18+00:00 (94.5s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 08ecdd4a661efb4a, reply sha256 c957f7fb5d629e28

## Sent

````
SPEC:
{
  "name": "Schotten Totten: Five Stones",
  "summary": "Two players take turns placing cards from a private hand onto their side of five Stones, forming three-card poker-like formations; a player claims a Stone with the stronger side, and the first to claim 3 of the 5 Stones wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 36,
    "colours": 4,
    "max_card_value": 9,
    "stones": 5,
    "side_capacity": 3,
    "hand_size": 6,
    "draw_pile_after_deal": 24,
    "max_rounds": 30,
    "stones_to_win": 3,
    "straight_flush_bonus": 120,
    "three_of_a_kind_bonus": 90,
    "flush_bonus": 60,
    "straight_bonus": 30,
    "no_formation_bonus": 0,
    "straight_span": 2
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The card codes this player holds, like 'R7'. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "claimed",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Stones this player has claimed. This is the score.",
        "observable": true
      },
      {
        "key": "role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "'A' for seat 1 or 'B' for seat 2. A acts in odd rounds and B in even rounds.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 36 codes R1..R9, B1..B9, G1..G9, Y1..Y9",
        "meaning": "The face-down draw pile.",
        "observable": false
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 36,
        "meaning": "Number of cards left in the draw pile. It is 24 after the deal.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, from 1 to 30.",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "1 (A) in odd rounds and 2 (B) in even rounds.",
        "observable": false
      },
      {
        "key": "stone_1_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up cards on A's side of Stone 1, at most 3.",
        "observable": false
      },
      {
        "key": "stone_1_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up cards on B's side of Stone 1, at most 3.",
        "observable": false
      },
      {
        "key": "stone_2_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "A's side of Stone 2.",
        "observable": false
      },
      {
        "key": "stone_2_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "B's side of Stone 2.",
        "observable": false
      },
      {
        "key": "stone_3_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "A's side of Stone 3.",
        "observable": false
      },
      {
        "key": "stone_3_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "B's side of Stone 3.",
        "observable": false
      },
      {
        "key": "stone_4_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "A's side of Stone 4.",
        "observable": false
      },
      {
        "key": "stone_4_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "B's side of Stone 4.",
        "observable": false
      },
      {
        "key": "stone_5_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "A's side of Stone 5.",
        "observable": false
      },
      {
        "key": "stone_5_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "B's side of Stone 5.",
        "observable": false
      },
      {
        "key": "stone_owner",
        "type": "list",
        "visible": "public",
        "initial": [
          "",
          "",
          "",
          "",
          ""
        ],
        "meaning": "Who has claimed each Stone 1-5: '' (unclaimed), 'A' or 'B'.",
        "observable": true
      },
      {
        "key": "first_finisher",
        "type": "list",
        "visible": "public",
        "initial": [
          "",
          "",
          "",
          "",
          ""
        ],
        "meaning": "For each Stone, 'A' or 'B': the player who first completed 3 cards on their side while the other side held fewer than 3.",
        "observable": false
      }
    ]
  },
  "setup": [
    "The deck holds the 36 cards R1-R9, B1-B9, G1-G9 and Y1-Y9.",
    "Seats are assigned at random: seat 1 is Player A (role 'A') and seat 2 is Player B (role 'B'). A takes the first turn.",
    "Each player is dealt 6 cards: each draw picks a random card from deck, appends it to that player's hand and removes it from deck.",
    "deck_count is set to 24.",
    "All ten Stone sides start empty. stone_owner and first_finisher start as five empty entries."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; active_seat = 1 if round is odd, else 2."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every Stone's sides (stone_k_a, stone_k_b), stone_owner, each player's claimed, and deck_count."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand."
    },
    {
      "action": "ask",
      "who": "the active player (seat active_seat)",
      "answer": "one card code from their hand",
      "effect": "The chosen card is remembered as the card to play."
    },
    {
      "action": "ask",
      "who": "the active player (seat active_seat)",
      "answer": "one Stone number from 1-5 that is unclaimed (stone_owner[k] == '') and where the active player's side holds fewer than 3 cards",
      "effect": "The chosen Stone k is remembered."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "Remove the chosen card from the active player's hand and append it to stone_k_a (if active_seat == 1) or stone_k_b (if active_seat == 2). Cards never move again."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "If the active side of Stone k now has 3 cards and the opposite side has fewer than 3, set first_finisher[k] = the active player's role."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "If deck_count > 0, draw a random card from deck into the active player's hand and set deck_count -= 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each Stone k = 1..5 where stone_owner[k] == '' and both len(stone_k_a) == 3 and len(stone_k_b) == 3, compute strength_a and strength_b by the strength formula. If strength_a > strength_b, the owner is 'A'. If strength_b > strength_a, the owner is 'B'. If they are equal, the owner is first_finisher[k]. Set stone_owner[k] to the owner and add 1 to that player's claimed. Announce the result."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any player's claimed >= 3, or if round >= 30. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "max over players of claimed >= 3, or round >= 30",
    "rank_by": "you.claimed",
    "decided_by": "A player's standing is the number of Stones they have claimed. The first to reach 3 wins at once. If round 30 ends without that, the player with more claimed Stones wins, and equal counts share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, each player holds 6 cards in hand and the deck holds 24."
    },
    {
      "id": "R2",
      "text": "When the round number is odd, seat 1 (A) is the only player asked to act; when it is even, seat 2 (B) is the only one asked."
    },
    {
      "id": "R3",
      "text": "When the active player is asked for a card, the options are exactly the cards in their hand."
    },
    {
      "id": "R4",
      "text": "When the active player is asked for a Stone, the options are exactly the Stones that are unclaimed and whose side for that player holds fewer than 3 cards."
    },
    {
      "id": "R5",
      "text": "When a card is played on Stone k, it leaves the player's hand, is appended to that player's side of Stone k, and never moves again."
    },
    {
      "id": "R6",
      "text": "When a played card is the third on its side and the other side holds fewer than 3 cards, first_finisher[k] is set to the player's role."
    },
    {
      "id": "R7",
      "text": "When deck_count > 0 after a play, the active player draws one card and deck_count drops by 1; when deck_count == 0, no card is drawn."
    },
    {
      "id": "R8",
      "text": "When all three cards on a side share a colour, have different values, and highest minus lowest is 2, the strength is the sum of the values + 120 (for example, R3 R4 R5 has strength 132)."
    },
    {
      "id": "R9",
      "text": "When all three values on a side are equal, the strength is the sum + 90 (for example, R7 B7 G7 has strength 111)."
    },
    {
      "id": "R10",
      "text": "When all three cards share a colour but the side is not a straight flush, the strength is the sum + 60 (for example, B1 B5 B9 has strength 75)."
    },
    {
      "id": "R11",
      "text": "When the values are all different with highest minus lowest equal to 2 but the colours are mixed, the strength is the sum + 30 (for example, R6 B7 G8 has strength 51)."
    },
    {
      "id": "R12",
      "text": "When a side has no formation, its strength is just the sum (for example, R2 B5 G9 has strength 16)."
    },
    {
      "id": "R13",
      "text": "When both sides of an unclaimed Stone hold 3 cards, the side with the higher strength claims it and that player's claimed goes up by 1."
    },
    {
      "id": "R14",
      "text": "When both sides of a completed Stone have equal strength, the Stone's first_finisher claims it."
    },
    {
      "id": "R15",
      "text": "When a Stone is claimed, it can no longer be offered as a Stone to play on."
    },
    {
      "id": "R16",
      "text": "When a player's claimed reaches 3, the game ends immediately and that player wins."
    },
    {
      "id": "R17",
      "text": "When round 30 ends and nobody has 3 Stones, the player with more claimed Stones wins, and equal counts are a draw."
    }
  ],
  "offers": [
    {
      "question": "Which card to play",
      "who": "the active seat only (seat 1 in odd rounds, seat 2 in even rounds)",
      "options": "Every card code currently in that seat's hand. The inactive seat is asked nothing."
    },
    {
      "question": "Which Stone to play on",
      "who": "the active seat only",
      "options": "Every Stone number 1-5 with stone_owner[k] == '' whose side for the active player holds fewer than 3 cards. Claimed Stones and Stones where the player's side is full are never offered."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players, suggested 2",
      "why": "The designer fixed the game at 2. Each Stone has exactly two sides, A and B, so the game does not scale to more seats."
    },
    {
      "what": "No talk step",
      "why": "The rules include no table talk. This is a two-player positional duel, and messages would add nothing the rules call for."
    },
    {
      "what": "Card choice and Stone choice are two sequential asks",
      "why": "The source lists them as separate steps (2) and (3). Asking them separately keeps each option list exact."
    },
    {
      "what": "Drawing the top card is a random pick from deck",
      "why": "The deck is shuffled, so a random draw is equivalent to taking the top card."
    },
    {
      "what": "The round counter and active seat are updated at the start of each round",
      "why": "This lets the engine pick the active player by arithmetic on round parity."
    },
    {
      "what": "The end check also fires at round >= 30",
      "why": "The source caps the game at 30 rounds. At that point all 30 slots are filled and every Stone has been resolved."
    },
    {
      "what": "Strategy at the table",
      "why": "Each card commits to one Stone permanently. A thoughtful player judges which formations are still possible given the visible cards, decides which Stones to contest and which to concede, and races to finish a side first so they win ties."
    }
  ],
  "simplifications": [
    {
      "what": "Stone sides are table attributes (stone_k_a and stone_k_b) rather than per-player lists",
      "why": "The engine has no player-attribute operand for comparison. Keeping both sides on the table lets resolution compare the two strengths directly."
    },
    {
      "what": "Strength is computed by calculating each card's colour (first letter) and value (digit) inside the resolution update",
      "why": "The engine has no lookup operation. The formation test is pure arithmetic on the three values and colours, so no referee is needed."
    },
    {
      "what": "All five Stones are resolved in one update step, using per-Stone conditional operations",
      "why": "Each Stone's resolution is an independent conditional update. No branching block of steps is needed."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: claimed; table: stone_owner.
````

## Reply

````
[
{"name":"R1 setup: each seat holds 6 cards and the deck holds 24","rule":"R1","players":2,"rounds":0,
 "expect":{"lens":{"game":{"deck":24},"players":{"1":{"hand":6},"2":{"hand":6}}},
           "players":{"1":{"claimed":0},"2":{"claimed":0}},
           "game":{"stone_owner":["","","","",""]}}},

{"name":"R2 odd round: only seat 1 is asked","rule":"R2","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","R2","R3","R4","R5","R6"]},"2":{"hand":["Y4","Y5","Y6","Y7","Y8","Y9"]}},
          "game":{"round":0,"deck":[],"deck_count":0}},
 "rules":[{"seat":1,"options_include":"R1"},{"seat":1,"options_include":1}],
 "expect":{"offered":[{"seat":1,"option":"R1"}],
           "not_offered":[{"seat":2,"option":"Y9"},{"seat":2,"option":"Y4"},{"seat":2,"option":1}]}},

{"name":"R2 even round: only seat 2 is asked","rule":"R2","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","R2","R3","R4","R5","R6"]},"2":{"hand":["Y4","Y5","Y6","Y7","Y8","Y9"]}},
          "game":{"round":1,"deck":[],"deck_count":0}},
 "rules":[{"seat":2,"options_include":"Y9"},{"seat":2,"options_include":1}],
 "expect":{"offered":[{"seat":2,"option":"Y9"}],
           "not_offered":[{"seat":1,"option":"R1"},{"seat":1,"option":"R6"},{"seat":1,"option":1}]}},

{"name":"R3 the card options are exactly the cards in hand","rule":"R3","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","B2","G3","Y4","R5","B6"]},"2":{"hand":["Y9","G9","B9","R9","Y8","G8"]}},
          "game":{"round":0,"deck":[],"deck_count":0}},
 "rules":[{"seat":1,"options_include":"R1"},{"seat":1,"options_include":1}],
 "expect":{"offered":[{"seat":1,"option":"R1"},{"seat":1,"option":"B2"},{"seat":1,"option":"G3"},{"seat":1,"option":"Y4"},{"seat":1,"option":"R5"},{"seat":1,"option":"B6"}],
           "not_offered":[{"seat":1,"option":"Y9"},{"seat":1,"option":"R7"}]}},

{"name":"R4 a claimed Stone and a Stone with a full side are not offered","rule":"R4","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R9","G1","G2","G3","G4","G5"],"claimed":1},"2":{"hand":["Y5","Y6","Y7","Y8","Y9","B9"],"claimed":0}},
          "game":{"round":0,"deck":[],"deck_count":0,
                  "stone_1_a":["R1","R2","R3"],"stone_1_b":["B1","B4","G7"],
                  "stone_2_a":["Y1","Y2","Y3"],
                  "stone_owner":["A","","","",""]}},
 "rules":[{"seat":1,"options_include":"R9"},{"seat":1,"options_include":3}],
 "expect":{"offered":[{"seat":1,"option":3},{"seat":1,"option":4},{"seat":1,"option":5}],
           "not_offered":[{"seat":1,"option":1},{"seat":1,"option":2}],
           "game":{"stone_owner":["A","","","",""]},
           "players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R5 the played card leaves the hand and goes onto the chosen Stone side","rule":"R5","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","B2","G3","Y4","R5","B6"]},"2":{"hand":["Y9","G9","B9","R9","Y8","G8"]}},
          "game":{"round":0,"deck":[],"deck_count":0}},
 "rules":[{"seat":1,"options_include":"G3"},{"seat":1,"options_include":2}],
 "expect":{"lens":{"players":{"1":{"hand":5},"2":{"hand":6}},"game":{"stone_2_a":1,"stone_1_a":0,"stone_2_b":0}},
           "game":{"stone_owner":["","","","",""]}}},

{"name":"R6 A finishes Stone 1 first, then B ties it: A claims","rule":"R6","players":2,"rounds":2,
 "given":{"players":{"1":{"hand":["G9","Y1","Y2","Y3","B1","B2"]},"2":{"hand":["R9","Y7","Y8","B7","B8","G7"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["R2","B5"],"stone_1_b":["G2","Y5"]}},
 "rules":[{"seat":1,"options_include":"G9"},{"seat":1,"options_include":1},
          {"seat":2,"options_include":"R9"},{"seat":2,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R7 with cards in the deck the active player draws one","rule":"R7","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","R2","R3","R4","R5","R6"]},"2":{"hand":["B1","B2","B3","B4","B5","B6"]}},
          "game":{"round":0,"deck":["Y1","Y2"],"deck_count":2}},
 "rules":[{"seat":1,"options_include":"R1"},{"seat":1,"options_include":1}],
 "expect":{"lens":{"players":{"1":{"hand":6},"2":{"hand":6}},"game":{"deck":1}}}},

{"name":"R7 with an empty deck no card is drawn","rule":"R7","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R1","R2","R3","R4","R5","R6"]},"2":{"hand":["B1","B2","B3","B4","B5","B6"]}},
          "game":{"round":0,"deck":[],"deck_count":0}},
 "rules":[{"seat":1,"options_include":"R1"},{"seat":1,"options_include":1}],
 "expect":{"lens":{"players":{"1":{"hand":5},"2":{"hand":6}},"game":{"deck":0}}}},

{"name":"R8 straight flush R3 R4 R5 (132) beats three 9s (117)","rule":"R8","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["R5","G1","G2","G3","B1","B2"]},"2":{"hand":["Y1","Y2","Y3","B3","B4","B6"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["R3","R4"],"stone_1_b":["B9","G9","Y9"],"first_finisher":["B","","","",""]}},
 "rules":[{"seat":1,"options_include":"R5"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R9 three 1s (93) beat flush Y6 Y8 Y9 (83)","rule":"R9","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["G1","G5","G6","R5","R6","B5"]},"2":{"hand":["R9","R8","B9","B8","G9","G8"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["R1","B1"],"stone_1_b":["Y6","Y8","Y9"],"first_finisher":["B","","","",""]}},
 "rules":[{"seat":1,"options_include":"G1"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R10 flush B1 B2 B4 (67) beats straight R7 B8 G9 (54)","rule":"R10","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["B4","Y1","Y2","Y3","R1","R2"]},"2":{"hand":["G1","G2","G3","Y5","Y6","Y7"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["B1","B2"],"stone_1_b":["R7","B8","G9"],"first_finisher":["B","","","",""]}},
 "rules":[{"seat":1,"options_include":"B4"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R11 mixed straight R1 B2 G3 (36) beats G9 Y9 R8 (26)","rule":"R11","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["G3","Y4","Y5","B6","B7","R6"]},"2":{"hand":["Y1","Y2","B3","B4","R5","G5"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["R1","B2"],"stone_1_b":["G9","Y9","R8"],"first_finisher":["B","","","",""]}},
 "rules":[{"seat":1,"options_include":"G3"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R12 no formation is just the sum: R2 B5 G9 (16) beats a pair Y7 G7 R1 (15)","rule":"R12","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["G9","Y1","Y2","Y3","B1","B2"]},"2":{"hand":["R9","R8","B9","B8","Y9","Y8"]}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_1_a":["R2","B5"],"stone_1_b":["Y7","G7","R1"],"first_finisher":["B","","","",""]}},
 "rules":[{"seat":1,"options_include":"G9"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["A","","","",""]},"players":{"1":{"claimed":1},"2":{"claimed":0}}}},

{"name":"R13 B completes Stone 1 with the stronger side (22 vs 10) and claims it","rule":"R13","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["Y1","Y2","Y3","B1","B2","G1"]},"2":{"hand":["R6","R7","B7","B8","B9","G9"]}},
          "game":{"round":1,"deck":[],"deck_count":0,"stone_1_a":["R2","B3","G5"],"stone_1_b":["Y8","G8"],"first_finisher":["A","","","",""]}},
 "rules":[{"seat":2,"options_include":"R6"},{"seat":2,"options_include":1}],
 "expect":{"game":{"stone_owner":["B","","","",""]},"players":{"1":{"claimed":0},"2":{"claimed":1}}}},

{"name":"R14 B finishes Stone 1 first, then A ties it at 16: B claims","rule":"R14","players":2,"rounds":2,
 "given":{"players":{"1":{"hand":["G9","Y1","Y2","Y3","B1","B2"]},"2":{"hand":["R9","Y7","Y8","B7","B8","G7"]}},
          "game":{"round":1,"deck":[],"deck_count":0,"stone_1_a":["R2","B5"],"stone_1_b":["G2","Y5"]}},
 "rules":[{"seat":2,"options_include":"R9"},{"seat":2,"options_include":1},
          {"seat":1,"options_include":"G9"},{"seat":1,"options_include":1}],
 "expect":{"game":{"stone_owner":["B","","","",""]},"players":{"1":{"claimed":0},"2":{"claimed":1}}}},

{"name":"R15 a claimed Stone is not offered even though A's side is not full","rule":"R15","players":2,"rounds":1,
 "given":{"players":{"1":{"hand":["G1","G2","G3","G4","G5","G6"],"claimed":0},"2":{"hand":["Y5","Y6","Y7","Y8","Y9","B9"],"claimed":1}},
          "game":{"round":0,"deck":[],"deck_count":0,"stone_2_a":["R1","R2"],"stone_2_b":["B1","B2","B3"],"stone_owner":["","B","","",""]}},
 "rules":[{"seat":1,"options_include":"G1"},{"seat":1,"options_include":1}],
 "expect":{"offered":[{"seat":1,"option":1},{"seat":1,"option":3}],
           "not_offered":[{"seat":1,"option":2}],
           "game":{"stone_owner":["","B","","",""]}}},

{"name":"R16 A claims a third Stone and wins at once","rule":"R16","players":2,
 "given":{"players":{"1":{"hand":["R9","G1","G2","G3","G4","G5"],"claimed":2},"2":{"hand":["Y5","Y6","Y7","Y8","Y9","B9"],"claimed":0}},
          "game":{"round":0,"deck":[],"deck_count":0,
                  "stone_1_a":["R1","R2","R3"],"stone_1_b":["B1","B4","G7"],
                  "stone_2_a":["R4","R5","R6"],"stone_2_b":["B2","B5","G8"],
                  "stone_3_a":["R7","R8"],"stone_3_b":["Y1","Y2","Y4"],
                  "stone_owner":["A","A","","",""]}},
 "rules":[{"seat":1,"options_include":"R9"},{"seat":1,"options_include":3}],
 "expect":{"winner":1,"standings":{"1":3,"2":0},
           "players":{"1":{"claimed":3},"2":{"claimed":0}},
           "game":{"stone_owner":["A","A","A","",""]}}},

{"name":"R17 round 30 ends with B ahead 2 to 1: B wins","rule":"R17","players":2,
 "given":{"players":{"1":{"hand":["R8","R9","G3","G4","G5","G6"],"claimed":1},"2":{"hand":["B7","B8","B9","Y9","G9","Y8"],"claimed":1}},
          "game":{"round":29,"deck":[],"deck_count":0,
                  "stone_1_a":["R1","R2","R3"],"stone_1_b":["B1","B4","G7"],
                  "stone_2_a":["B2","B5","R4"],"stone_2_b":["R5","R6","R7"],
                  "stone_3_a":["G1","G2","Y4"],"stone_3_b":["Y5","Y6"],
                  "stone_owner":["A","B","","",""]}},
 "rules":[{"seat":2,"options_include":"B7"},{"seat":2,"options_include":3}],
 "expect":{"winner":2,"standings":{"1":1,"2":2},
           "players":{"1":{"claimed":1},"2":{"claimed":2}},
           "game":{"stone_owner":["A","B","B","",""]}}},

{"name":"R17 round 30 ends level at 1 Stone each: both seats share the win","rule":"R17","players":2,
 "given":{"players":{"1":{"hand":["R8","R9","G3","G4","G5","G6"],"claimed":1},"2":{"hand":["B7","B8","B9","Y9","G9","Y8"],"claimed":1}},
          "game":{"round":29,"deck":[],"deck_count":0,
                  "stone_1_a":["R1","R2","R3"],"stone_1_b":["B1","B4","G7"],
                  "stone_2_a":["B2","B5","R4"],"stone_2_b":["R5","R6","R7"],
                  "stone_3_a":["G1","G2","Y4"],"stone_3_b":["Y5","Y6"],
                  "stone_owner":["A","B","","",""]}},
 "rules":[{"seat":2,"options_include":"B7"},{"seat":2,"options_include":4}],
 "expect":{"winner":[1,2],"standings":{"1":1,"2":1},
           "players":{"1":{"claimed":1},"2":{"claimed":1}},
           "game":{"stone_owner":["A","B","","",""]}}}
]
````
