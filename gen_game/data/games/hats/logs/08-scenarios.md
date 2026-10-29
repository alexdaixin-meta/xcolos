# 08 scenarios

- time: 2026-10-28T05:16:37+00:00 (28.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 440a0c65a59058c8, reply sha256 31dc72ae0879f38e

## Sent

````
SPEC:
{
  "name": "Ripening Hats",
  "summary": "Over 12 rounds, players secretly pick one of 5 hat colours (or safe Black); a colour picked by exactly one player pays its ripening value, plus a bonus if it is that player's secret favourite, and contested colours pay nothing.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "num_colours": 5,
    "initial_colour_value": 2,
    "max_colour_value": 7,
    "reset_value": 1,
    "value_increment": 1,
    "black_points": 1,
    "favourite_bonus": 3,
    "contested_gain": 0,
    "rounds": 12,
    "initial_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "favourite",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The player's secret favourite colour, dealt at random from the colour pool, different for every player; revealed at the end",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's private score, revealed at the end",
        "observable": true
      },
      {
        "key": "choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's secret choice: Red, Blue, Green, Yellow, Purple or Black",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message, shown to everyone after all are in",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current round number, 1 to 12",
        "observable": true
      },
      {
        "key": "colour_pool",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple"
        ],
        "meaning": "Hidden list of colours not yet dealt as favourites; each deal removes one",
        "observable": false
      },
      {
        "key": "value_red",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Current value of Red",
        "observable": true
      },
      {
        "key": "value_blue",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Current value of Blue",
        "observable": true
      },
      {
        "key": "value_green",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Current value of Green",
        "observable": true
      },
      {
        "key": "value_yellow",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Current value of Yellow",
        "observable": true
      },
      {
        "key": "value_purple",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Current value of Purple",
        "observable": true
      },
      {
        "key": "count_red",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "How many players chose Red this round",
        "observable": false
      },
      {
        "key": "count_blue",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "How many players chose Blue this round",
        "observable": false
      },
      {
        "key": "count_green",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "How many players chose Green this round",
        "observable": false
      },
      {
        "key": "count_yellow",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "How many players chose Yellow this round",
        "observable": false
      },
      {
        "key": "count_purple",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "How many players chose Purple this round",
        "observable": false
      },
      {
        "key": "status_red",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Red's result this round: COLLECTED, CONTESTED or UNTOUCHED",
        "observable": true
      },
      {
        "key": "status_blue",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Blue's result this round: COLLECTED, CONTESTED or UNTOUCHED",
        "observable": true
      },
      {
        "key": "status_green",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Green's result this round: COLLECTED, CONTESTED or UNTOUCHED",
        "observable": true
      },
      {
        "key": "status_yellow",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Yellow's result this round: COLLECTED, CONTESTED or UNTOUCHED",
        "observable": true
      },
      {
        "key": "status_purple",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Purple's result this round: COLLECTED, CONTESTED or UNTOUCHED",
        "observable": true
      },
      {
        "key": "black_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many players chose Black this round",
        "observable": true
      }
    ]
  },
  "setup": [
    "Set all five colour values (value_red, value_blue, value_green, value_yellow, value_purple) to 2.",
    "Set every player's score to 0 and round to 1.",
    "For each player, draw one colour at random from colour_pool into that player's favourite and remove it from colour_pool, so all favourites are different.",
    "Sync: each player is told their own favourite and score."
  ],
  "round": [
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Round {round} of 12. Values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}, Purple {value_purple}.'"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "Set each player's message to their text. Once all are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk binds no one."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Red, Blue, Green, Yellow, Purple, Black",
      "effect": "Set each player's choice to their answer. No answer is shown to anyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set count_red, count_blue, count_green, count_yellow and count_purple each to the number of players whose choice is that colour. Set black_count to the number of players whose choice is Black."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player: if choice = Black, add 1 to score. If choice is a colour C and count_C = 1, add value_C to score, and add a further 3 if favourite = C. If count_C >= 2, add 0. Do not announce scores."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each colour C, set status_C to COLLECTED if count_C = 1, CONTESTED if count_C >= 2, and UNTOUCHED if count_C = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce without naming players: 'Red {status_red}, Blue {status_blue}, Green {status_green}, Yellow {status_yellow}, Purple {status_purple}. Black chosen by {black_count}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each colour C: if count_C = 1, set value_C to 1; otherwise set value_C to min(7, value_C + 1)."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own score and favourite."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Add 1 to round."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round > 12, end the game. Reveal every player's favourite and score to everyone. Otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round > 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final score. The highest score wins. Players tied for the highest score share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then all five colour values are 2 and every player's score is 0."
    },
    {
      "id": "R2",
      "text": "When favourites are dealt, then each player gets one of Red, Blue, Green, Yellow or Purple at random, no two players get the same colour, and only the owner can see it."
    },
    {
      "id": "R3",
      "text": "When a round begins, then everyone is told the round number and the current value of each of the 5 colours."
    },
    {
      "id": "R4",
      "text": "When the talk step runs, then every player writes one short message at the same time, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R5",
      "text": "When the choice step runs, then every player secretly and simultaneously picks exactly one of Red, Blue, Green, Yellow, Purple or Black."
    },
    {
      "id": "R6",
      "text": "When a player chooses Black, then that player's score increases by 1."
    },
    {
      "id": "R7",
      "text": "When a player is the only one to choose colour C and C is not their favourite, then their score increases by value_C (for example, by 4 if value_C is 4)."
    },
    {
      "id": "R8",
      "text": "When a player is the only one to choose colour C and C is their favourite, then their score increases by value_C + 3 (for example, by 5 if value_C is 2)."
    },
    {
      "id": "R9",
      "text": "When two or more players choose the same colour, then none of them gains any points that round."
    },
    {
      "id": "R10",
      "text": "When choices are resolved, then each colour's status is announced as COLLECTED (exactly 1 chooser), CONTESTED (2 or more) or UNTOUCHED (0), along with the number of Black choosers, without naming any player."
    },
    {
      "id": "R11",
      "text": "When a colour was collected this round, then its value becomes 1 for the next round."
    },
    {
      "id": "R12",
      "text": "When a colour was contested or untouched this round, then its value rises by 1, but never above 7 (a colour at 7 stays at 7)."
    },
    {
      "id": "R13",
      "text": "When the game is running, then individual choices and scores are never announced."
    },
    {
      "id": "R14",
      "text": "When round 12 has been resolved, then the game ends and all favourites and scores are revealed."
    },
    {
      "id": "R15",
      "text": "When the game ends, then the player with the highest score wins, and if two or more players tie for the highest score, the result is a draw among them."
    }
  ],
  "offers": [
    {
      "question": "Talk: write one short message",
      "who": "all players",
      "options": "Any short free text, the same for every seat."
    },
    {
      "question": "Choice: pick a hat",
      "who": "all players",
      "options": "Every seat, in every round: Red, Blue, Green, Yellow, Purple, Black."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer's suggested size is 4, so it is kept. The minimum is 3 because with 2 players the competition over colours is too thin to be interesting. The maximum is 4 because with 5 colours, 4 players still leave room to spread out, while a fifth player would let every favourite be in play and make collisions near-constant."
    },
    {
      "what": "Talk is kept as a simultaneous poll with a broadcast",
      "why": "The rules say messages are written at the same time without seeing the others, so a poll fits rather than ask. Talk earns its place because players have conflicting interests. Each wants a ripe colour to themselves, so claiming, warning or bluffing about a favourite gives others something to weigh. Following a claim can cost a player a collision."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player tracks which colours are ripening, reads the COLLECTED and CONTESTED history to infer others' favourites, and uses talk to steer rivals away from their own targets. They also judge when the safe 1 point from Black beats a likely collision."
    },
    {
      "what": "Favourites are dealt from a hidden colour_pool list",
      "why": "This makes 'all different' a matter of draw-and-remove, which the engine supports."
    },
    {
      "what": "Score is marked observable",
      "why": "The source reveals scores at the end, and tests need the score. It stays ally-visible during play."
    },
    {
      "what": "Each player is synced their own score after collection",
      "why": "The source says each player can see their own private score. The source does not say when updates are delivered, so the sync timing is my choice."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is represented as a shared win",
      "why": "The engine has no separate draw outcome: players level at the top share the win, which corresponds to the source's draw."
    },
    {
      "what": "Per-colour counts and statuses are kept as separate table attributes (count_red, status_red and so on)",
      "why": "The engine has no lookup by colour, so each colour gets its own counter and status."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: round, value_red, value_blue, value_green, value_yellow, value_purple, status_red, status_blue, status_green, status_yellow, status_purple, black_count.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Game starts with all colour values at 2, scores at 0, round 1",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"round": 1, "value_red": 2, "value_blue": 2, "value_green": 2, "value_yellow": 2, "value_purple": 2}
    }
  },
  {
    "name": "Dealing favourites to 4 players removes 4 colours from the pool (which colours is random)",
    "rule": "R2",
    "players": 4,
    "rounds": 0,
    "expect": {"lens": {"game": {"colour_pool": 1}}}
  },
  {
    "name": "Dealing favourites to 3 players leaves 2 colours in the pool",
    "rule": "R2",
    "players": 3,
    "rounds": 0,
    "expect": {"lens": {"game": {"colour_pool": 2}}}
  },
  {
    "name": "After round 1 the round number advances and untouched values ripen to 3",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"game": {"round": 2, "value_red": 3, "value_blue": 3, "value_green": 3, "value_yellow": 3, "value_purple": 3}}
  },
  {
    "name": "Talk binds no one: after talk every seat still makes its own choice",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"},
      {"seat": 4, "options_include": "Black"}
    ],
    "expect": {
      "game": {"black_count": 4},
      "players": {"1": {"score": 1}, "2": {"score": 1}, "3": {"score": 1}, "4": {"score": 1}}
    }
  },
  {
    "name": "Every seat is offered all five colours and Black",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"},
        {"seat": 1, "option": "Yellow"}, {"seat": 1, "option": "Purple"}, {"seat": 1, "option": "Black"},
        {"seat": 2, "option": "Red"}, {"seat": 2, "option": "Purple"}, {"seat": 2, "option": "Black"},
        {"seat": 3, "option": "Green"}, {"seat": 3, "option": "Yellow"}, {"seat": 3, "option": "Black"}
      ]
    }
  },
  {
    "name": "Choosing Black gives 1 point",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Red"}
    ],
    "expect": {
      "players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 0}},
      "game": {"black_count": 1}
    }
  },
  {
    "name": "Sole chooser of a non-favourite colour gains its value",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Green"}},
      "game": {"value_yellow": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "players": {"1": {"score": 4}, "2": {"score": 1}, "3": {"score": 1}},
      "game": {"status_yellow": "COLLECTED"}
    }
  },
  {
    "name": "Sole chooser of their favourite gains value plus 3",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Green"}},
      "game": {"value_red": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"players": {"1": {"score": 5}, "2": {"score": 1}, "3": {"score": 1}}}
  },
  {
    "name": "Two players on the same colour gain nothing, even if it is a favourite",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Blue"}, "2": {"favourite": "Red"}, "3": {"favourite": "Green"}}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 1}},
      "game": {"status_blue": "CONTESTED"}
    }
  },
  {
    "name": "Statuses are COLLECTED, CONTESTED or UNTOUCHED, with the Black count",
    "rule": "R10",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Green"}, "2": {"favourite": "Yellow"}, "3": {"favourite": "Purple"}, "4": {"favourite": "Red"}}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Black"}
    ],
    "expect": {
      "game": {
        "status_red": "COLLECTED",
        "status_blue": "CONTESTED",
        "status_green": "UNTOUCHED",
        "status_yellow": "UNTOUCHED",
        "status_purple": "UNTOUCHED",
        "black_count": 1
      }
    }
  },
  {
    "name": "A collected colour resets to value 1",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Yellow"}},
      "game": {"value_green": 6}
    },
    "rules": [
      {"seat": 1, "options_include": "Green"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "game": {"value_green": 1},
      "players": {"1": {"score": 6}}
    }
  },
  {
    "name": "Contested and untouched colours rise by 1, capped at 7",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"value_red": 5, "value_blue": 2, "value_purple": 7, "value_green": 6, "value_yellow": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"game": {"value_red": 6, "value_blue": 3, "value_purple": 7, "value_green": 7, "value_yellow": 4}}
  },
  {
    "name": "Scores accumulate privately across a round without affecting public values",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"score": 3}, "2": {"score": 2}, "3": {"score": 0}}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Purple"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "players": {"1": {"score": 4}, "2": {"score": 3}},
      "game": {"black_count": 2, "status_purple": "COLLECTED", "value_purple": 1}
    }
  },
  {
    "name": "Game ends after round 12 is resolved; highest score wins",
    "rule": "R14",
    "players": 3,
    "given": {
      "players": {"1": {"score": 10}, "2": {"score": 8}, "3": {"score": 5}},
      "game": {"round": 12}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 11, "2": 9, "3": 6},
      "game": {"round": 13}
    }
  },
  {
    "name": "Tie for highest score is shared",
    "rule": "R15",
    "players": 3,
    "given": {
      "players": {"1": {"score": 10}, "2": {"score": 9}, "3": {"score": 10}},
      "game": {"round": 12}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 11, "2": 10, "3": 11}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Game starts with all colour values at 2, scores at 0, round 1",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "rules": [],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"round": 1, "value_red": 2, "value_blue": 2, "value_green": 2, "value_yellow": 2, "value_purple": 2}
    }
  },
  {
    "name": "Dealing favourites to 4 players removes 4 colours from the pool (which colours is random)",
    "rule": "R2",
    "players": 4,
    "rounds": 0,
    "rules": [],
    "expect": {"lens": {"game": {"colour_pool": 1}}}
  },
  {
    "name": "Dealing favourites to 3 players leaves 2 colours in the pool",
    "rule": "R2",
    "players": 3,
    "rounds": 0,
    "rules": [],
    "expect": {"lens": {"game": {"colour_pool": 2}}}
  },
  {
    "name": "After round 1 the round number advances and untouched values ripen to 3",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"game": {"round": 2, "value_red": 3, "value_blue": 3, "value_green": 3, "value_yellow": 3, "value_purple": 3}}
  },
  {
    "name": "Talk binds no one: after talk every seat still makes its own choice",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"},
      {"seat": 4, "options_include": "Black"}
    ],
    "expect": {
      "game": {"black_count": 4},
      "players": {"1": {"score": 1}, "2": {"score": 1}, "3": {"score": 1}, "4": {"score": 1}}
    }
  },
  {
    "name": "Every seat is offered all five colours and Black",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"},
        {"seat": 1, "option": "Yellow"}, {"seat": 1, "option": "Purple"}, {"seat": 1, "option": "Black"},
        {"seat": 2, "option": "Red"}, {"seat": 2, "option": "Purple"}, {"seat": 2, "option": "Black"},
        {"seat": 3, "option": "Green"}, {"seat": 3, "option": "Yellow"}, {"seat": 3, "option": "Black"}
      ]
    }
  },
  {
    "name": "Choosing Black gives 1 point",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Red"}
    ],
    "expect": {
      "players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 0}},
      "game": {"black_count": 1}
    }
  },
  {
    "name": "Sole chooser of a non-favourite colour gains its value",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Green"}},
      "game": {"value_yellow": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "players": {"1": {"score": 4}, "2": {"score": 1}, "3": {"score": 1}},
      "game": {"status_yellow": "COLLECTED"}
    }
  },
  {
    "name": "Sole chooser of their favourite gains value plus 3",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Green"}},
      "game": {"value_red": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"players": {"1": {"score": 5}, "2": {"score": 1}, "3": {"score": 1}}}
  },
  {
    "name": "Two players on the same colour gain nothing, even if it is a favourite",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Blue"}, "2": {"favourite": "Red"}, "3": {"favourite": "Green"}}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 1}},
      "game": {"status_blue": "CONTESTED"}
    }
  },
  {
    "name": "Statuses are COLLECTED, CONTESTED or UNTOUCHED, with the Black count",
    "rule": "R10",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Green"}, "2": {"favourite": "Yellow"}, "3": {"favourite": "Purple"}, "4": {"favourite": "Red"}}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Black"}
    ],
    "expect": {
      "game": {
        "status_red": "COLLECTED",
        "status_blue": "CONTESTED",
        "status_green": "UNTOUCHED",
        "status_yellow": "UNTOUCHED",
        "status_purple": "UNTOUCHED",
        "black_count": 1
      }
    }
  },
  {
    "name": "A collected colour resets to value 1",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"favourite": "Red"}, "2": {"favourite": "Blue"}, "3": {"favourite": "Yellow"}},
      "game": {"value_green": 6}
    },
    "rules": [
      {"seat": 1, "options_include": "Green"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "game": {"value_green": 1},
      "players": {"1": {"score": 6}}
    }
  },
  {
    "name": "Contested and untouched colours rise by 1, capped at 7",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"value_red": 5, "value_blue": 2, "value_purple": 7, "value_green": 6, "value_yellow": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {"game": {"value_red": 6, "value_blue": 3, "value_purple": 7, "value_green": 7, "value_yellow": 4}}
  },
  {
    "name": "Scores accumulate privately across a round without affecting public values",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"score": 3}, "2": {"score": 2}, "3": {"score": 0}}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Purple"}
    ],
    "expect": {
      "players": {"1": {"score": 4}, "2": {"score": 3}},
      "game": {"black_count": 2, "status_purple": "COLLECTED", "value_purple": 1}
    }
  },
  {
    "name": "Game ends after round 12 is resolved; highest score wins",
    "rule": "R14",
    "players": 3,
    "given": {
      "players": {"1": {"score": 10}, "2": {"score": 8}, "3": {"score": 5}},
      "game": {"round": 12}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 11, "2": 9, "3": 6},
      "game": {"round": 13}
    }
  },
  {
    "name": "Tie for highest score is shared",
    "rule": "R15",
    "players": 3,
    "given": {
      "players": {"1": {"score": 10}, "2": {"score": 9}, "3": {"score": 10}},
      "game": {"round": 12}
    },
    "rules": [
      {"seat": 1, "options_include": "Black"},
      {"seat": 2, "options_include": "Black"},
      {"seat": 3, "options_include": "Black"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 11, "2": 10, "3": 11}
    }
  }
]
```
````
