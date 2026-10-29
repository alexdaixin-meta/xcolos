# 24 scenarios

- time: 2026-10-28T04:33:22+00:00 (68.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 2743c37b4b0e39da, reply sha256 0616b133c0a9293d

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

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Do not seed split_g through `given`, because the mandatory split poll overwrites it. Set each seat's split with a poll-answer rule instead, for example {seat: 1, options_include: 2}, as the R1 test does. To test picks being used up, either play several rounds so glazed_used and jelly_used build up through real non-void choices, or seed only glazed_used and jelly_used while setting split_g through the poll answer. Recompute the expected score and donuts from the rules for those poll answers. Give every seat an explicit poll answer rather than relying on the default.
````

## Reply

````
```json
[
  {"name": "R1: split poll answer of 2 gives exactly two Glazed picks, so the third lone Glazed is void", "rule": "R1", "players": 4, "seed": 1, "rounds": 3, "default": "first",
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": "all"},
             {"seat": 2, "options_include": "Cruller", "times": "all"},
             {"seat": 3, "options_include": "Sprinkle", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"players": {"1": {"score": 18, "donuts": 2}, "2": {"score": 12, "donuts": 3}, "3": {"score": 6, "donuts": 3}, "4": {"score": 3, "donuts": 3}},
              "offered": [{"seat": 1, "option": 6}]}},

  {"name": "R2: split 1 gives 1 Glazed and 5 Jelly picks; with 4 Jelly already used, one Jelly wins and the next is void", "rule": "R2", "players": 4, "seed": 1, "rounds": 3, "default": "first",
   "given": {"players": {"1": {"glazed_used": 0, "jelly_used": 4}}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": 1},
             {"seat": 1, "options_include": "Jelly", "times": 2},
             {"seat": 2, "options_include": "Cruller", "times": "all"},
             {"seat": 3, "options_include": "Sprinkle", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"players": {"1": {"score": 15, "donuts": 2}, "2": {"score": 12, "donuts": 3}, "3": {"score": 6, "donuts": 3}, "4": {"score": 3, "donuts": 3}}}},

  {"name": "R3: a round with simultaneous talk completes and awards donuts normally", "rule": "R3", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Jelly"},
             {"seat": 3, "options_include": "Cruller"},
             {"seat": 4, "options_include": "Sprinkle"}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 6, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 2, "donuts": 1}}}},

  {"name": "R4: a player with 1 Glazed pick left (split 3, 2 used) can still win Glazed", "rule": "R4", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"glazed_used": 2, "jelly_used": 0}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Cruller"},
             {"seat": 3, "options_include": "Sprinkle"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R5: Glazed with split 0 is void and gains nothing even when alone", "rule": "R5", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Jelly"},
             {"seat": 3, "options_include": "Cruller"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 6, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R6: Jelly with split 6 (no Jelly picks) is void and gains nothing even when alone", "rule": "R6", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Jelly"},
             {"seat": 2, "options_include": "Cruller"},
             {"seat": 3, "options_include": "Sprinkle"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R7: Cruller, Sprinkle and Plain are never void, even with all premium picks used", "rule": "R7", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"glazed_used": 6, "jelly_used": 0}, "2": {"glazed_used": 0, "jelly_used": 6}, "3": {"glazed_used": 3, "jelly_used": 3}}},
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 3}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Cruller"},
             {"seat": 2, "options_include": "Sprinkle"},
             {"seat": 3, "options_include": "Plain"},
             {"seat": 4, "options_include": "Glazed"}],
   "expect": {"players": {"1": {"score": 4, "donuts": 1}, "2": {"score": 2, "donuts": 1}, "3": {"score": 1, "donuts": 1}, "4": {"score": 0, "donuts": 0}}}},

  {"name": "R8: each lone non-void choice gains its donut's points and one donut", "rule": "R8", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Jelly"},
             {"seat": 3, "options_include": "Cruller"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 6, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R9: two players choosing Cruller both get nothing", "rule": "R9", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Cruller"},
             {"seat": 2, "options_include": "Cruller"},
             {"seat": 3, "options_include": "Sprinkle"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 0, "donuts": 0}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R10: a discarded Glazed still uses up the single Glazed pick, so the next Glazed is void", "rule": "R10", "players": 4, "seed": 1, "rounds": 2, "default": "first",
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": "all"},
             {"seat": 2, "options_include": "Glazed", "times": 1},
             {"seat": 2, "options_include": "Cruller", "times": 1},
             {"seat": 3, "options_include": "Sprinkle", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},

  {"name": "R11: a discarded Jelly still uses up the single Jelly pick, so the next Jelly is void", "rule": "R11", "players": 4, "seed": 1, "rounds": 2, "default": "first",
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Jelly", "times": "all"},
             {"seat": 2, "options_include": "Jelly", "times": 1},
             {"seat": 2, "options_include": "Cruller", "times": 1},
             {"seat": 3, "options_include": "Sprinkle", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},

  {"name": "R12: a void Glazed does not use up the last Jelly pick, so the Jelly that follows still wins", "rule": "R12", "players": 4, "seed": 1, "rounds": 2, "default": "first",
   "given": {"players": {"1": {"glazed_used": 5, "jelly_used": 0}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": 1},
             {"seat": 1, "options_include": "Jelly", "times": 1},
             {"seat": 2, "options_include": "Cruller", "times": "all"},
             {"seat": 3, "options_include": "Sprinkle", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"players": {"1": {"score": 6, "donuts": 1}, "2": {"score": 8, "donuts": 2}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},

  {"name": "R13: a void Glazed next to one valid Glazed lets the valid player win 9", "rule": "R13", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 6}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Glazed"},
             {"seat": 3, "options_include": "Cruller"},
             {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 9, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

  {"name": "R14: public score and donuts add up across two rounds", "rule": "R14", "players": 4, "seed": 1, "rounds": 2, "default": "first",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": "all"},
             {"seat": 2, "options_include": "Jelly", "times": "all"},
             {"seat": 3, "options_include": "Cruller", "times": "all"},
             {"seat": 4, "options_include": "Cruller", "times": "all"}],
   "expect": {"players": {"1": {"score": 18, "donuts": 2}, "2": {"score": 12, "donuts": 2}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},

  {"name": "R15: the full 10-round match ends, with the 6 Glazed picks used up after round 6", "rule": "R15", "players": 4, "seed": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": "all"},
             {"seat": 2, "options_include": "Jelly", "times": "all"},
             {"seat": 3, "options_include": "Cruller", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"winner": 1,
              "standings": {"1": 5406, "2": 3606, "3": 4010, "4": 1010},
              "players": {"1": {"score": 54, "donuts": 6}, "2": {"score": 36, "donuts": 6}, "3": {"score": 40, "donuts": 10}, "4": {"score": 10, "donuts": 10}}}},

  {"name": "R16: seats level on score and donuts after the last round share the win", "rule": "R16", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 9},
             "players": {"1": {"score": 10, "donuts": 3}, "2": {"score": 7, "donuts": 3}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Plain"},
             {"seat": 2, "options_include": "Cruller"},
             {"seat": 3, "options_include": "Sprinkle"},
             {"seat": 4, "options_include": "Glazed"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 1104, "2": 1104, "3": 201, "4": 0},
              "players": {"1": {"score": 11, "donuts": 4}, "2": {"score": 11, "donuts": 4}, "3": {"score": 2, "donuts": 1}, "4": {"score": 0, "donuts": 0}}}},

  {"name": "R16: on equal score, more donuts wins", "rule": "R16", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 9},
             "players": {"1": {"score": 10, "donuts": 5}, "2": {"score": 7, "donuts": 3}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Plain"},
             {"seat": 2, "options_include": "Cruller"},
             {"seat": 3, "options_include": "Sprinkle"},
             {"seat": 4, "options_include": "Glazed"}],
   "expect": {"winner": 1,
              "standings": {"1": 1106, "2": 1104, "3": 201, "4": 0},
              "players": {"1": {"score": 11, "donuts": 6}, "2": {"score": 11, "donuts": 4}}}}
]
```
````
