# 20 scenarios

- time: 2026-10-28T04:30:22+00:00 (57.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 05605d7f4d3c4e3c, reply sha256 ad5ef3c17f2b2aa3

## Sent

````
SPEC:
{
  "name": "Go Nuts for Donuts: Secret Budget",
  "summary": "Four players spend 10 simultaneous rounds picking one of five donuts. A donut scores only for a player who picks it alone, and each player has a secret split of 6 premium picks between Glazed and Jelly.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "glazed_points": 9,
    "jelly_points": 6,
    "cruller_points": 4,
    "sprinkle_points": 2,
    "plain_points": 1,
    "rounds": 10,
    "premium_picks": 6,
    "split_g_min": 0,
    "split_g_max": 6,
    "rank_score_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points from donuts won alone",
        "observable": true
      },
      {
        "key": "donuts",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of donuts won",
        "observable": true
      },
      {
        "key": "split_g",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Secret number of the 6 premium picks that are Glazed picks. Jelly picks are 6 - split_g. Set once by the split poll and never changed.",
        "observable": false
      },
      {
        "key": "glazed_used",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Non-void Glazed choices made so far",
        "observable": false
      },
      {
        "key": "jelly_used",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Non-void Jelly choices made so far",
        "observable": false
      },
      {
        "key": "choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's donut choice, gathered by a simultaneous poll and shown at the reveal",
        "observable": false
      },
      {
        "key": "void",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this round's choice is void",
        "observable": false
      },
      {
        "key": "gained",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points gained this round",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rounds completed",
        "observable": false
      },
      {
        "key": "count_glazed",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Non-void Glazed choices this round",
        "observable": false
      },
      {
        "key": "count_jelly",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Non-void Jelly choices this round",
        "observable": false
      },
      {
        "key": "count_cruller",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cruller choices this round",
        "observable": false
      },
      {
        "key": "count_sprinkle",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sprinkle choices this round",
        "observable": false
      },
      {
        "key": "count_plain",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Plain choices this round",
        "observable": false
      }
    ]
  },
  "setup": [
    "Initialize every player with score 0, donuts 0, split_g 0, glazed_used 0 and jelly_used 0, and set round to 0.",
    "Poll all players at once: 'How many of your 6 premium picks are Glazed picks?' The options are 0, 1, 2, 3, 4, 5 and 6. Store each answer as that player's split_g, visible only to that player.",
    "Sync each player their own state."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reset each player's choice to empty, void to false and gained to 0. Reset count_glazed, count_jelly, count_cruller, count_sprinkle and count_plain to 0."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one short text message",
      "effect": "Gather all messages at once, then broadcast to all: 'Seat {seat} says: {value}'. Messages bind no one."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Privately remind each player of their Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used)."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Glazed, Jelly, Cruller, Sprinkle, Plain",
      "effect": "Store each answer in that player's choice."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set void = true if (choice == Glazed and glazed_used >= split_g) or (choice == Jelly and jelly_used >= 6 - split_g). Otherwise set void = false."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set count_glazed to the number of players with choice Glazed and not void, and count_jelly to the number with choice Jelly and not void. Set count_cruller, count_sprinkle and count_plain to the number of players who chose each."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each non-void player whose donut's count == 1, set gained to that donut's points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), add gained to score and add 1 to donuts. Every other player gets gained 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Every player with a non-void Glazed choice adds 1 to glazed_used. Every player with a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal each player's choice (marked VOID if void), gained, score and donuts. split_g is never shown."
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
      "effect": "End the game if round >= 10. Otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 100 + you.donuts",
    "decided_by": "The highest score wins, with ties broken by most donuts won. Players still level on both share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Before round 1, each player's answer to the split poll (0 to 6) is stored as split_g, visible only to that player, and is never changed afterwards."
    },
    {
      "id": "R2",
      "text": "When a player has split_g = s, they have s Glazed picks and 6 - s Jelly picks."
    },
    {
      "id": "R3",
      "text": "Each round, every player sends one message at the same time, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R4",
      "text": "Before choosing, each player is privately told split_g - glazed_used Glazed picks left and 6 - split_g - jelly_used Jelly picks left."
    },
    {
      "id": "R5",
      "text": "When a player chooses Glazed while glazed_used >= split_g, the choice is void, gains 0 and does not count toward Glazed."
    },
    {
      "id": "R6",
      "text": "When a player chooses Jelly while jelly_used >= 6 - split_g, the choice is void, gains 0 and does not count toward Jelly."
    },
    {
      "id": "R7",
      "text": "When a player chooses Cruller, Sprinkle or Plain, the choice is never void."
    },
    {
      "id": "R8",
      "text": "When exactly 1 player makes a non-void choice of a donut, that player gains its points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1) and adds 1 to donuts."
    },
    {
      "id": "R9",
      "text": "When 2 or more players make a non-void choice of the same donut, none of them gains points or donuts for it."
    },
    {
      "id": "R10",
      "text": "When a player makes a non-void Glazed choice, glazed_used rises by 1 whether the donut was won or discarded."
    },
    {
      "id": "R11",
      "text": "When a player makes a non-void Jelly choice, jelly_used rises by 1 whether the donut was won or discarded."
    },
    {
      "id": "R12",
      "text": "When a choice is void, glazed_used and jelly_used do not change."
    },
    {
      "id": "R13",
      "text": "When a void choice of Glazed is made alongside one non-void Glazed choice, the non-void player still wins the Glazed for 9 points."
    },
    {
      "id": "R14",
      "text": "After each round, every player's choice (marked VOID if void), gain, score and donuts are shown to everyone, and split_g is never shown."
    },
    {
      "id": "R15",
      "text": "When round 10 ends, the game ends."
    },
    {
      "id": "R16",
      "text": "At the end, the player with the highest score * 100 + donuts wins, and players tied on that value share the win."
    }
  ],
  "offers": [
    {
      "question": "Secret split: how many of your 6 premium picks are Glazed picks?",
      "who": "all players, at once, before round 1",
      "options": "0, 1, 2, 3, 4, 5, 6"
    },
    {
      "question": "Talk",
      "who": "all players, at once, each round",
      "options": "one short free-text message"
    },
    {
      "question": "Choose a donut",
      "who": "all players, at once, each round",
      "options": "Glazed, Jelly, Cruller, Sprinkle, Plain, always all five, even with no picks left (such a choice is then void)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players, suggested 4",
      "why": "The rules fix the table at 4 and the designer chose it. Five donuts for four players makes collisions frequent but avoidable, which is what the game is about."
    },
    {
      "what": "Keep simultaneous talk each round, built as a poll and then a broadcast",
      "why": "The rules require it. Players disagree about who should take the high donuts, so talk can be used to bluff about one's remaining budget or to stake claims."
    },
    {
      "what": "glazed_used and jelly_used are public",
      "why": "The reveal shows every choice and whether it was void, so these counts can be deduced by anyone. Only split_g stays secret."
    },
    {
      "what": "Per-donut counters and the per-player choice, void and gained fields as attributes",
      "why": "The void check, the count and the award need state to work on. These are reset at the start of each round."
    },
    {
      "what": "Rank value score * 100 + donuts",
      "why": "This is given by the rules. Donuts can never exceed 10, so the score always dominates the tie-break."
    }
  ],
  "simplifications": [
    {
      "what": "The private reminder of picks left is delivered as a sync of each player's own state, with the computed values",
      "why": "The engine sends private state through sync. This has the same effect as the rule's reminder."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, donuts; table: none.
````

## Reply

````
[
{"name":"Split poll answers are stored: split 0 makes Glazed void, split 6 makes Jelly void","rule":"R1","players":4,"seed":1,"rounds":1,"default":"last",
 "rules":[{"seat":1,"options_include":0},{"seat":2,"options_include":6},
          {"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Cruller"},{"seat":4,"options_include":"Sprinkle"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":0,"donuts":0},"3":{"score":4,"donuts":1},"4":{"score":2,"donuts":1}}}},
{"name":"Split 2 gives Glazed picks and 4 Jelly picks","rule":"R2","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":2,"glazed_used":1},"2":{"split_g":2,"jelly_used":3}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Plain"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":9,"donuts":1},"2":{"score":6,"donuts":1},"3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}}},
{"name":"Talk binds no one; round resolves on choices","rule":"R3","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":6},"2":{"split_g":0}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Cruller"},{"seat":4,"options_include":"Sprinkle"}],
 "expect":{"players":{"1":{"score":9,"donuts":1},"2":{"score":6,"donuts":1},"3":{"score":4,"donuts":1},"4":{"score":2,"donuts":1}}}},
{"name":"With Jelly picks left, a Jelly choice is valid; Glazed still offered with none left","rule":"R4","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":3,"glazed_used":3,"jelly_used":0}}},
 "rules":[{"seat":1,"options_include":"Jelly"},{"seat":2,"options_include":"Cruller"},
          {"seat":3,"options_include":"Sprinkle"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":6,"donuts":1},"2":{"score":4,"donuts":1},"3":{"score":2,"donuts":1},"4":{"score":1,"donuts":1}},
           "offered":[{"seat":1,"option":"Glazed"}]}},
{"name":"Glazed with no Glazed picks left is void and gains nothing","rule":"R5","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":2,"glazed_used":2}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Cruller"},
          {"seat":3,"options_include":"Sprinkle"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":4,"donuts":1},"3":{"score":2,"donuts":1},"4":{"score":1,"donuts":1}}}},
{"name":"Jelly with no Jelly picks left is void and gains nothing","rule":"R6","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":4,"jelly_used":2}}},
 "rules":[{"seat":1,"options_include":"Jelly"},{"seat":2,"options_include":"Cruller"},
          {"seat":3,"options_include":"Sprinkle"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":4,"donuts":1},"3":{"score":2,"donuts":1},"4":{"score":1,"donuts":1}}}},
{"name":"Cruller and Sprinkle are never void even with no premium picks left","rule":"R7","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":6,"glazed_used":6},"2":{"split_g":0,"jelly_used":6}}},
 "rules":[{"seat":1,"options_include":"Cruller"},{"seat":2,"options_include":"Sprinkle"},
          {"seat":3,"options_include":"Plain"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":4,"donuts":1},"2":{"score":2,"donuts":1},"3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}}},
{"name":"A lone chooser gains the donut's points and one donut","rule":"R8","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":6,"score":10,"donuts":2},"2":{"split_g":0}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Sprinkle"},{"seat":4,"options_include":"Plain"}],
 "expect":{"players":{"1":{"score":19,"donuts":3},"2":{"score":6,"donuts":1},"3":{"score":2,"donuts":1},"4":{"score":1,"donuts":1}}}},
{"name":"Two players on the same donut both get nothing","rule":"R9","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":6},"2":{"split_g":6}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Glazed"},
          {"seat":3,"options_include":"Cruller"},{"seat":4,"options_include":"Cruller"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":0,"donuts":0},"3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}}},
{"name":"A discarded Glazed still uses the pick, so the next Glazed is void","rule":"R10","players":4,"seed":1,"rounds":2,"default":"last",
 "given":{"players":{"1":{"split_g":1,"glazed_used":0},"2":{"split_g":6}}},
 "rules":[{"seat":1,"options_include":"Glazed","times":2},
          {"seat":2,"options_include":"Glazed","times":1},{"seat":2,"options_include":"Plain","times":1},
          {"seat":3,"options_include":"Cruller","times":"all"},{"seat":4,"options_include":"Sprinkle","times":"all"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":1,"donuts":1},"3":{"score":8,"donuts":2},"4":{"score":4,"donuts":2}}}},
{"name":"A discarded Jelly still uses the pick, so the next Jelly is void","rule":"R11","players":4,"seed":1,"rounds":2,"default":"last",
 "given":{"players":{"1":{"split_g":5,"jelly_used":0},"2":{"split_g":0}}},
 "rules":[{"seat":1,"options_include":"Jelly","times":2},
          {"seat":2,"options_include":"Jelly","times":1},{"seat":2,"options_include":"Plain","times":1},
          {"seat":3,"options_include":"Cruller","times":"all"},{"seat":4,"options_include":"Sprinkle","times":"all"}],
 "expect":{"players":{"1":{"score":0,"donuts":0},"2":{"score":1,"donuts":1},"3":{"score":8,"donuts":2},"4":{"score":4,"donuts":2}}}},
{"name":"A void Glazed does not use up the last Jelly pick","rule":"R12","players":4,"seed":1,"rounds":2,"default":"last",
 "given":{"players":{"1":{"split_g":5,"glazed_used":5,"jelly_used":0}}},
 "rules":[{"seat":1,"options_include":"Glazed","times":1},{"seat":1,"options_include":"Jelly","times":1},
          {"seat":2,"options_include":"Cruller","times":"all"},{"seat":3,"options_include":"Sprinkle","times":"all"},
          {"seat":4,"options_include":"Plain","times":"all"}],
 "expect":{"players":{"1":{"score":6,"donuts":1},"2":{"score":8,"donuts":2},"3":{"score":4,"donuts":2},"4":{"score":2,"donuts":2}}}},
{"name":"A void Glazed beside one valid Glazed lets the valid one win 9","rule":"R13","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"1":{"split_g":6},"2":{"split_g":0}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Glazed"},
          {"seat":3,"options_include":"Cruller"},{"seat":4,"options_include":"Cruller"}],
 "expect":{"players":{"1":{"score":9,"donuts":1},"2":{"score":0,"donuts":0},"3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}}},
{"name":"After a round each seat's score and donuts reflect the reveal","rule":"R14","players":4,"seed":1,"rounds":1,"default":"last",
 "given":{"players":{"2":{"split_g":0}}},
 "rules":[{"seat":1,"options_include":"Cruller"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Sprinkle"},{"seat":4,"options_include":"Sprinkle"}],
 "expect":{"players":{"1":{"score":4,"donuts":1},"2":{"score":6,"donuts":1},"3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}}},
{"name":"Game ends after round 10 and the highest score wins","rule":"R15","players":4,"seed":1,"default":"last",
 "given":{"game":{"round":9},
          "players":{"1":{"split_g":6,"glazed_used":0,"score":20,"donuts":3},"2":{"split_g":0,"jelly_used":0,"score":25,"donuts":3},
                     "3":{"score":0,"donuts":0},"4":{"score":0,"donuts":0}}},
 "rules":[{"seat":1,"options_include":"Glazed"},{"seat":2,"options_include":"Jelly"},
          {"seat":3,"options_include":"Cruller"},{"seat":4,"options_include":"Cruller"}],
 "expect":{"winner":2,"standings":{"1":2904,"2":3104,"3":0,"4":0},
           "players":{"1":{"score":29,"donuts":4},"2":{"score":31,"donuts":4}}}},
{"name":"Equal score is broken by more donuts","rule":"R16","players":4,"seed":1,"default":"last",
 "given":{"game":{"round":9},
          "players":{"1":{"score":30,"donuts":5},"2":{"score":30,"donuts":4},"3":{"score":10,"donuts":2},"4":{"score":5,"donuts":1}}},
 "rules":[{"seat":1,"options_include":"Plain"},{"seat":2,"options_include":"Plain"},
          {"seat":3,"options_include":"Plain"},{"seat":4,"options_include":"Plain"}],
 "expect":{"winner":1,"standings":{"1":3005,"2":3004,"3":1002,"4":501}}},
{"name":"Seats level on score and donuts share the win","rule":"R16","players":4,"seed":1,"default":"last",
 "given":{"game":{"round":9},
          "players":{"1":{"score":30,"donuts":5},"2":{"score":30,"donuts":5},"3":{"score":10,"donuts":2},"4":{"score":5,"donuts":1}}},
 "rules":[{"seat":1,"options_include":"Plain"},{"seat":2,"options_include":"Plain"},
          {"seat":3,"options_include":"Plain"},{"seat":4,"options_include":"Plain"}],
 "expect":{"winner":[1,2],"standings":{"1":3005,"2":3005,"3":1002,"4":501}}}
]
````
