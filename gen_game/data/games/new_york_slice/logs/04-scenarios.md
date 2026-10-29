# 04 scenarios

- time: 2026-10-27T22:11:39+00:00 (84.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 4eaf428ba67d356a, reply sha256 f853ea041fb5ef26

## Sent

````
SPEC:
{
  "name": "Secret Slice",
  "summary": "Three players take turns cutting a row of six pizza slices into three portions. The others pick first and the cutter gets the last portion. Each player chooses whether to eat pepperoni for points or collect it toward majorities, while chasing a secret favourite topping.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "slices_per_type": 9,
    "deck_size": 36,
    "rows": 6,
    "row_size": 6,
    "rounds": 6,
    "cut_min": 1,
    "cut_max": 5,
    "majority_cheese": 7,
    "majority_mushroom": 7,
    "majority_pepperoni": 5,
    "majority_anchovy": 10,
    "eaten_pepperoni_point": 1,
    "anchovy_penalty": 1,
    "favourite_bonus": 1
  },
  "attributes": {
    "player": [
      {
        "key": "favourite",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "secret favourite topping: Cheese, Mushroom, Pepperoni or Anchovy; revealed at final scoring",
        "observable": true
      },
      {
        "key": "cheese",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "collected Cheese slices",
        "observable": true
      },
      {
        "key": "mushroom",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "collected Mushroom slices",
        "observable": true
      },
      {
        "key": "pepperoni",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "collected Pepperoni slices",
        "observable": true
      },
      {
        "key": "anchovy",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "collected Anchovy slices",
        "observable": true
      },
      {
        "key": "eaten",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "eaten Pepperoni slices",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "final total, computed after round 6",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "9 x Cheese, 9 x Mushroom, 9 x Pepperoni, 9 x Anchovy",
        "meaning": "the undealt slices; each row is drawn from it at random",
        "observable": false
      },
      {
        "key": "toppings",
        "type": "list",
        "visible": "none",
        "initial": [
          "Cheese",
          "Mushroom",
          "Pepperoni",
          "Anchovy"
        ],
        "meaning": "favourites still undealt; one is left over and is nobody's favourite",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round, 1 to 6",
        "observable": true
      },
      {
        "key": "slicer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat of this round's Slicer",
        "observable": false
      },
      {
        "key": "first_picker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat after the Slicer",
        "observable": false
      },
      {
        "key": "second_picker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "remaining non-Slicer seat",
        "observable": false
      },
      {
        "key": "row",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "this round's 6 slices, positions 1 to 6 in order",
        "observable": false
      },
      {
        "key": "c1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "first cut",
        "observable": false
      },
      {
        "key": "c2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "second cut",
        "observable": false
      },
      {
        "key": "slicer_mode",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "eat or collect, declared by the Slicer at the cut",
        "observable": false
      },
      {
        "key": "portion_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "positions 1..c1",
        "observable": false
      },
      {
        "key": "portion_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "positions c1+1..c2",
        "observable": false
      },
      {
        "key": "portion_c",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "positions c2+1..6",
        "observable": false
      },
      {
        "key": "taken",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "portions already picked this round (A, B, C)",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are P1, P2, P3.",
    "The deck list is filled with 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy.",
    "Each player is dealt a favourite at random from the toppings list, which is removed from that list (without replacement), so the three favourites differ and one topping is nobody's favourite.",
    "Each player is synced their own favourite, kept secret (ally) until final scoring."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; slicer = ((round-1) mod 3) + 1; first_picker = (slicer mod 3) + 1; second_picker = (first_picker mod 3) + 1; taken = []"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "row = []; 6 times: draw one slice at random from deck, append it to row, remove it from deck. Announce the row with positions 1 to 6 and who is Slicer, first picker and second picker."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Nothing changes; all messages are broadcast at once: {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"
    },
    {
      "action": "ask",
      "who": "seat slicer",
      "answer": "one choice 'c1-c2 mode' with 1 <= c1 < c2 <= 5 and mode eat or collect (20 options)",
      "effect": "set c1, c2, slicer_mode; portion_a = row[1..c1]; portion_b = row[c1+1..c2]; portion_c = row[c2+1..6]; announce the three portions"
    },
    {
      "action": "ask",
      "who": "seat first_picker",
      "answer": "one of: A eat, A collect, B eat, B collect, C eat, C collect",
      "effect": "the picker adds the chosen portion's Cheese to cheese, Mushroom to mushroom and Anchovy to anchovy; its Pepperoni goes to eaten if eat, or to pepperoni if collect; append the letter to taken; announce"
    },
    {
      "action": "ask",
      "who": "seat second_picker",
      "answer": "one of the two portions not in taken, each with eat or collect (4 options)",
      "effect": "same accounting as the first pick for the second picker; append the letter to taken; announce"
    },
    {
      "action": "update",
      "who": "seat slicer",
      "answer": null,
      "effect": "the Slicer takes the portion not in taken, with slicer_mode: Cheese to cheese, Mushroom to mushroom, Anchovy to anchovy, Pepperoni to eaten if slicer_mode = eat, otherwise to pepperoni; announce"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round = 6: for each player, score = 7 if cheese is strictly greater than both other players' cheese + 7 if mushroom is strictly greater than both others' + 5 if pepperoni is strictly greater than both others' + 10 if anchovy is strictly greater than both others' + eaten - anchovy + the collected count of their own favourite (cheese, mushroom, pepperoni or anchovy). Reveal every favourite and announce all totals."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round >= 6, otherwise continue"
    }
  ],
  "ending": {
    "condition": "round >= 6",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final total; the highest total wins, and players tied for the highest share the win (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, the deck holds 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni, 9 Anchovy."
    },
    {
      "id": "R2",
      "text": "At setup, each of the 3 players gets a different favourite from {Cheese, Mushroom, Pepperoni, Anchovy}, visible only to its owner until final scoring."
    },
    {
      "id": "R3",
      "text": "In each round, 6 slices are drawn from the deck into the row, so after round r the deck holds 36 - 6r slices."
    },
    {
      "id": "R4",
      "text": "The Slicer is P1 in rounds 1 and 4, P2 in rounds 2 and 5, and P3 in rounds 3 and 6."
    },
    {
      "id": "R5",
      "text": "The first picker is the seat after the Slicer (P1 to P2, P2 to P3, P3 to P1), and the second picker is the remaining seat."
    },
    {
      "id": "R6",
      "text": "Each round, every player sends one text message in a simultaneous poll, and all messages are shown together; messages change no state."
    },
    {
      "id": "R7",
      "text": "The Slicer chooses c1 and c2 with 1 <= c1 < c2 <= 5, plus eat or collect, in one answer; for example 2-4 gives A = positions 1-2, B = 3-4, C = 5-6."
    },
    {
      "id": "R8",
      "text": "The first picker may choose any of A, B or C with eat or collect; the second picker may choose only one of the two portions left."
    },
    {
      "id": "R9",
      "text": "The Slicer receives the last remaining portion, using the mode declared at the cut."
    },
    {
      "id": "R10",
      "text": "When a portion is taken with eat, each Pepperoni in it adds 1 to eaten and nothing to pepperoni."
    },
    {
      "id": "R11",
      "text": "When a portion is taken with collect, each Pepperoni in it adds 1 to pepperoni."
    },
    {
      "id": "R12",
      "text": "Cheese, Mushroom and Anchovy slices in a taken portion are always added to cheese, mushroom and anchovy, whichever mode is declared."
    },
    {
      "id": "R13",
      "text": "At final scoring, a player with strictly the most collected Cheese scores 7, Mushroom 7, Pepperoni 5, Anchovy 10; if the most is tied, nobody scores that type."
    },
    {
      "id": "R14",
      "text": "At final scoring, each eaten Pepperoni is worth +1."
    },
    {
      "id": "R15",
      "text": "At final scoring, each collected Anchovy is worth -1."
    },
    {
      "id": "R16",
      "text": "At final scoring, each collected slice of your own favourite type is worth +1; eaten slices do not count."
    },
    {
      "id": "R17",
      "text": "The game ends after round 6; the highest score wins, and tied top scores share the win."
    }
  ],
  "offers": [
    {
      "question": "Talk",
      "who": "all players",
      "options": "a short free-text message"
    },
    {
      "question": "Cut",
      "who": "the Slicer",
      "options": "1-2 eat, 1-2 collect, 1-3 eat, 1-3 collect, 1-4 eat, 1-4 collect, 1-5 eat, 1-5 collect, 2-3 eat, 2-3 collect, 2-4 eat, 2-4 collect, 2-5 eat, 2-5 collect, 3-4 eat, 3-4 collect, 3-5 eat, 3-5 collect, 4-5 eat, 4-5 collect"
    },
    {
      "question": "First pick",
      "who": "the seat after the Slicer",
      "options": "A eat, A collect, B eat, B collect, C eat, C collect"
    },
    {
      "question": "Second pick",
      "who": "the remaining non-Slicer seat",
      "options": "the two portions not taken by the first picker, each with eat or collect (e.g. after A is taken: B eat, B collect, C eat, C collect)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at 3. The rotation of Slicer and pickers, the three portions and the three distinct favourites from four toppings all depend on exactly 3 seats."
    },
    {
      "what": "Strategy check",
      "why": "A thoughtful Slicer cuts so that every portion is equally unattractive to the others and reads their collections and talk to guess their favourites. Pickers weigh eating pepperoni (+1 now) against contesting the 5-point pepperoni majority, and avoid or deny anchovy around the 10-point majority."
    },
    {
      "what": "Keep the talk step as a simultaneous poll broadcast to all",
      "why": "The source says messages are written at the same time without seeing the others. Players have opposing interests over portions and majorities, so the talk gives them bluffing and bargaining material."
    },
    {
      "what": "Cut and mode given as one combined choice of 20 options",
      "why": "The source says the Slicer declares eat or collect in the same answer as the cut. One choice list enforces 1 <= c1 < c2 <= 5 exactly."
    },
    {
      "what": "Picks offered as portion plus mode in one choice",
      "why": "The source has each picker choose a portion and declare eat or collect together."
    }
  ],
  "simplifications": [
    {
      "what": "Rows are drawn at random from the deck each round instead of shuffling once and splitting into 6 rows at setup",
      "why": "Drawing 6 random slices per round without replacement gives the same distribution and keeps future rows hidden, using the engine's draw operation."
    },
    {
      "what": "A tie for the highest total is a shared win rather than a draw",
      "why": "The engine has no separate draw; players level at the top share the win, which matches the outcome that nobody wins alone."
    },
    {
      "what": "Strict majority is computed by comparing each player's count with both other players' counts",
      "why": "There is no direct player-attribute operand; the comparison is written out across the 3 seats in arithmetic."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: favourite, cheese, mushroom, pepperoni, anchovy, eaten, score; table: round.
````

## Reply

````
```json
[
  {
    "name": "Setup: deck holds 36 slices",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"deck": 36}},
      "game": {"round": 0}
    }
  },
  {
    "name": "Setup: three favourites dealt from four toppings, one left over (which ones is chance)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"toppings": 1}}
    }
  },
  {
    "name": "After round 1 the deck holds 30 slices",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 30}},
      "game": {"round": 1}
    }
  },
  {
    "name": "After round 2 the deck holds 24 slices",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 2,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"game": {"deck": 24}},
      "game": {"round": 2}
    }
  },
  {
    "name": "P1 is the Slicer in round 1",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "offered": [{"seat": 1, "option": "1-2 eat"}],
      "not_offered": [
        {"seat": 2, "option": "1-2 eat"},
        {"seat": 3, "option": "1-2 eat"}
      ]
    }
  },
  {
    "name": "P1 is the Slicer in round 4",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round": 3}},
    "rules": [],
    "expect": {
      "game": {"round": 4},
      "offered": [{"seat": 1, "option": "1-2 eat"}],
      "not_offered": [
        {"seat": 2, "option": "1-2 eat"},
        {"seat": 3, "option": "1-2 eat"}
      ]
    }
  },
  {
    "name": "P2 is the Slicer in round 5",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round": 4}},
    "rules": [],
    "expect": {
      "game": {"round": 5},
      "offered": [{"seat": 2, "option": "1-2 eat"}],
      "not_offered": [
        {"seat": 1, "option": "1-2 eat"},
        {"seat": 3, "option": "1-2 eat"}
      ]
    }
  },
  {
    "name": "P3 is the Slicer in round 3",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round": 2}},
    "rules": [],
    "expect": {
      "game": {"round": 3},
      "offered": [{"seat": 3, "option": "1-2 eat"}],
      "not_offered": [
        {"seat": 1, "option": "1-2 eat"},
        {"seat": 2, "option": "1-2 eat"}
      ]
    }
  },
  {
    "name": "Round 1: P2 picks first, P3 second, Slicer P1 does not pick",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "offered": [
        {"seat": 2, "option": "A eat"},
        {"seat": 3, "option": "B eat"}
      ],
      "not_offered": [
        {"seat": 3, "option": "A eat"},
        {"seat": 1, "option": "A eat"},
        {"seat": 1, "option": "B eat"}
      ]
    }
  },
  {
    "name": "Round 2: P3 picks first, P1 second, Slicer P2 does not pick",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"round": 1}},
    "rules": [],
    "expect": {
      "offered": [
        {"seat": 3, "option": "A eat"},
        {"seat": 1, "option": "B eat"}
      ],
      "not_offered": [
        {"seat": 1, "option": "A eat"},
        {"seat": 2, "option": "A eat"},
        {"seat": 2, "option": "B eat"}
      ]
    }
  },
  {
    "name": "Talk changes nothing: an all-Cheese row split 1/1/4 lands as cut",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"deck": ["Cheese", "Cheese", "Cheese", "Cheese", "Cheese", "Cheese"]}},
    "rules": [],
    "expect": {
      "players": {
        "1": {"cheese": 4, "mushroom": 0, "pepperoni": 0, "anchovy": 0, "eaten": 0},
        "2": {"cheese": 1, "mushroom": 0, "pepperoni": 0, "anchovy": 0, "eaten": 0},
        "3": {"cheese": 1, "mushroom": 0, "pepperoni": 0, "anchovy": 0, "eaten": 0}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Cut 1-4 gives A=1, B=3, C=2 slices",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {"game": {"deck": ["Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom"]}},
    "rules": [
      {"seat": 1, "options_include": "1-4 collect"},
      {"seat": 2, "options_include": "C collect"},
      {"seat": 3, "options_include": "B collect"}
    ],
    "expect": {
      "players": {
        "1": {"mushroom": 1},
        "2": {"mushroom": 2},
        "3": {"mushroom": 3}
      }
    }
  },
  {
    "name": "Second picker cannot take the portion the first picker took",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "offered": [
        {"seat": 2, "option": "A eat"},
        {"seat": 2, "option": "C collect"},
        {"seat": 3, "option": "A eat"},
        {"seat": 3, "option": "C collect"}
      ],
      "not_offered": [
        {"seat": 3, "option": "B eat"},
        {"seat": 3, "option": "B collect"}
      ]
    }
  },
  {
    "name": "Slicer gets the last portion with declared eat",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {"game": {"deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]}},
    "rules": [
      {"seat": 1, "options_include": "1-2 eat"},
      {"seat": 2, "options_include": "A collect"},
      {"seat": 3, "options_include": "B collect"}
    ],
    "expect": {
      "players": {
        "1": {"eaten": 4, "pepperoni": 0},
        "2": {"pepperoni": 1, "eaten": 0},
        "3": {"pepperoni": 1, "eaten": 0}
      }
    }
  },
  {
    "name": "Slicer gets the last portion with declared collect",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {"game": {"deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]}},
    "rules": [
      {"seat": 1, "options_include": "3-5 collect"},
      {"seat": 2, "options_include": "A eat"},
      {"seat": 3, "options_include": "C eat"}
    ],
    "expect": {
      "players": {
        "1": {"pepperoni": 2, "eaten": 0},
        "2": {"eaten": 3, "pepperoni": 0},
        "3": {"eaten": 1, "pepperoni": 0}
      }
    }
  },
  {
    "name": "Eat sends Pepperoni to eaten",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]}},
    "rules": [
      {"seat": 1, "options_include": "2-4 collect"},
      {"seat": 2, "options_include": "C eat"}
    ],
    "expect": {
      "players": {"2": {"eaten": 2, "pepperoni": 0}}
    }
  },
  {
    "name": "Collect sends Pepperoni to pepperoni",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]}},
    "rules": [
      {"seat": 1, "options_include": "2-4 eat"},
      {"seat": 2, "options_include": "C collect"}
    ],
    "expect": {
      "players": {"2": {"pepperoni": 2, "eaten": 0}}
    }
  },
  {
    "name": "Anchovy is collected whether the mode is eat or collect",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {"game": {"deck": ["Anchovy", "Anchovy", "Anchovy", "Anchovy", "Anchovy", "Anchovy"]}},
    "rules": [
      {"seat": 1, "options_include": "2-4 eat"},
      {"seat": 2, "options_include": "A eat"},
      {"seat": 3, "options_include": "B collect"}
    ],
    "expect": {
      "players": {
        "1": {"anchovy": 2, "eaten": 0},
        "2": {"anchovy": 2, "eaten": 0},
        "3": {"anchovy": 2, "eaten": 0}
      }
    }
  },
  {
    "name": "Strict majorities score; tied majorities score nothing",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom", "Mushroom"]},
      "players": {
        "1": {"favourite": "Cheese", "cheese": 5, "mushroom": 0, "pepperoni": 2, "anchovy": 1, "eaten": 0},
        "2": {"favourite": "Pepperoni", "cheese": 3, "mushroom": 0, "pepperoni": 2, "anchovy": 4, "eaten": 0},
        "3": {"favourite": "Anchovy", "cheese": 3, "mushroom": 0, "pepperoni": 0, "anchovy": 1, "eaten": 0}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 collect"},
      {"seat": 1, "options_include": "A collect"},
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 11, "2": 8, "3": 0},
      "players": {
        "1": {"score": 11, "mushroom": 2},
        "2": {"score": 8, "mushroom": 2},
        "3": {"score": 0, "mushroom": 2}
      },
      "game": {"round": 6}
    }
  },
  {
    "name": "Each eaten Pepperoni is worth 1",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]},
      "players": {
        "1": {"favourite": "Cheese", "eaten": 3},
        "2": {"favourite": "Mushroom", "eaten": 0},
        "3": {"favourite": "Anchovy", "eaten": 0}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 eat"},
      {"seat": 1, "options_include": "A eat"},
      {"seat": 2, "options_include": "B eat"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 5, "2": 2, "3": 2},
      "players": {
        "1": {"score": 5, "eaten": 5},
        "2": {"score": 2, "eaten": 2},
        "3": {"score": 2, "eaten": 2}
      }
    }
  },
  {
    "name": "Each collected Anchovy costs 1 (tied anchovy, no majority)",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Anchovy", "Anchovy", "Anchovy", "Anchovy", "Anchovy", "Anchovy"]},
      "players": {
        "1": {"favourite": "Cheese", "eaten": 5},
        "2": {"favourite": "Mushroom"},
        "3": {"favourite": "Pepperoni"}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 collect"},
      {"seat": 1, "options_include": "A collect"},
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 3, "2": -2, "3": -2},
      "players": {
        "1": {"score": 3, "anchovy": 2},
        "2": {"score": -2, "anchovy": 2},
        "3": {"score": -2, "anchovy": 2}
      }
    }
  },
  {
    "name": "Collected favourite slices count, eaten ones do not",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni", "Pepperoni"]},
      "players": {
        "1": {"favourite": "Pepperoni", "cheese": 0},
        "2": {"favourite": "Cheese", "cheese": 3},
        "3": {"favourite": "Mushroom", "cheese": 3}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 collect"},
      {"seat": 1, "options_include": "A eat"},
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 2, "2": 3, "3": 0},
      "players": {
        "1": {"score": 2, "eaten": 2, "pepperoni": 0},
        "2": {"score": 3, "pepperoni": 2},
        "3": {"score": 0, "pepperoni": 2}
      }
    }
  },
  {
    "name": "Tied top scores share the win",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Cheese", "Cheese", "Cheese", "Cheese", "Cheese", "Cheese"]},
      "players": {
        "1": {"favourite": "Mushroom", "eaten": 3},
        "2": {"favourite": "Pepperoni", "eaten": 3},
        "3": {"favourite": "Anchovy", "eaten": 0}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 collect"},
      {"seat": 1, "options_include": "A collect"},
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 3, "2": 3, "3": 0},
      "players": {
        "1": {"score": 3, "cheese": 2},
        "2": {"score": 3, "cheese": 2},
        "3": {"score": 0, "cheese": 2}
      },
      "game": {"round": 6}
    }
  },
  {
    "name": "All level at the end: every seat shares the win",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 5, "deck": ["Cheese", "Cheese", "Cheese", "Cheese", "Cheese", "Cheese"]},
      "players": {
        "1": {"favourite": "Mushroom"},
        "2": {"favourite": "Pepperoni"},
        "3": {"favourite": "Anchovy"}
      }
    },
    "rules": [
      {"seat": 3, "options_include": "2-4 collect"},
      {"seat": 1, "options_include": "A collect"},
      {"seat": 2, "options_include": "B collect"}
    ],
    "expect": {
      "winner": [1, 2, 3],
      "standings": {"1": 0, "2": 0, "3": 0},
      "players": {
        "1": {"score": 0},
        "2": {"score": 0},
        "3": {"score": 0}
      }
    }
  }
]
```
````
