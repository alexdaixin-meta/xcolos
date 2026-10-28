# 26 scenarios

- time: 2026-10-28T04:34:53+00:00 (72.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 ffc6b0683197659b, reply sha256 f84ba48e47b5d73e

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
Rewrite the two R16 scenarios.
- Script the split poll answers (0 to 6) so each seat matches them exactly once, before round 1. Do not use times 'all' or more than one, because the poll happens once per game.
- If a scenario starts from a given mid-game state, do not script split answers it will never be asked.
- Set split_g through the poll, not through internal counters.
- To get a tie on score and donuts, use non-premium donuts each round, for example by rotating Cruller, Sprinkle and Plain so that seats win equal totals.
- For 'more donuts wins', give two seats equal scores but different donut counts, for example one Cruller (4 points, 1 donut) against two Sprinkles (4 points, 2 donuts).
- Assert only on the final scores, the donut counts and the winner or shared win under rank score*100+donuts.
````

## Reply

````
[
  {"name": "R1: split poll answers are stored and used (seat 1 splits 6 Glazed, seat 2 splits 0 Glazed)", "rule": "R1", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Jelly"},
             {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Sprinkle"}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 6, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 2, "donuts": 1}},
              "offered": [{"seat": 1, "option": 6}, {"seat": 2, "option": 0}]}},
  {"name": "R2: split 2 gives exactly 2 Glazed picks, so the third Glazed is void", "rule": "R2", "players": 4, "rounds": 3, "default": "decline",
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Glazed", "times": 3},
             {"seat": 2, "options_include": "Cruller", "times": 3},
             {"seat": 3, "options_include": "Sprinkle", "times": 3},
             {"seat": 4, "options_include": "Plain", "times": 3}],
   "expect": {"players": {"1": {"score": 18, "donuts": 2}, "2": {"score": 12, "donuts": 3}, "3": {"score": 6, "donuts": 3}, "4": {"score": 3, "donuts": 3}}}},
  {"name": "R3: a round with talk still resolves the donut picks normally", "rule": "R3", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Jelly"},
             {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 6, "donuts": 1}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},
  {"name": "R4: with 1 Glazed pick, it is spent after one use and the next Glazed is void", "rule": "R4", "players": 4, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": "Glazed", "times": 2},
             {"seat": 2, "options_include": "Cruller", "times": 2},
             {"seat": 3, "options_include": "Sprinkle", "times": 2},
             {"seat": 4, "options_include": "Plain", "times": 2}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 8, "donuts": 2}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},
  {"name": "R5: Glazed with split 0 is void and gains nothing", "rule": "R5", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "Glazed"},
             {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},
  {"name": "R6: Jelly with split 6 is void and gains nothing", "rule": "R6", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 1, "options_include": "Jelly"},
             {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},
  {"name": "R7: Cruller, Sprinkle and Plain are never void, whatever the split", "rule": "R7", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 6}, {"seat": 4, "options_include": 0},
             {"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Sprinkle"},
             {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Jelly"}],
   "expect": {"players": {"1": {"score": 4, "donuts": 1}, "2": {"score": 2, "donuts": 1}, "3": {"score": 1, "donuts": 1}, "4": {"score": 6, "donuts": 1}}}},
  {"name": "R8: a lone non-void pick scores the donut's points and 1 donut", "rule": "R8", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 6}, {"seat": 2, "options_include": 0},
             {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Jelly"},
             {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 9, "donuts": 1}, "2": {"score": 6, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},
  {"name": "R9: two non-void picks of the same donut both score nothing", "rule": "R9", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 3},
             {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Glazed"},
             {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Cruller"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 0, "donuts": 0}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},
  {"name": "R10: a discarded Glazed still uses the pick, so the next Glazed is void", "rule": "R10", "players": 4, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 6},
             {"seat": 1, "options_include": "Glazed", "times": 2},
             {"seat": 2, "options_include": "Glazed", "times": 1}, {"seat": 2, "options_include": "Cruller", "times": 1},
             {"seat": 3, "options_include": "Sprinkle", "times": 2},
             {"seat": 4, "options_include": "Plain", "times": 2}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},
  {"name": "R11: a discarded Jelly still uses the pick, so the next Jelly is void", "rule": "R11", "players": 4, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 0},
             {"seat": 1, "options_include": "Jelly", "times": 2},
             {"seat": 2, "options_include": "Jelly", "times": 1}, {"seat": 2, "options_include": "Cruller", "times": 1},
             {"seat": 3, "options_include": "Sprinkle", "times": 2},
             {"seat": 4, "options_include": "Plain", "times": 2}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},
  {"name": "R12: a void Glazed uses no pick, and a later Jelly still scores", "rule": "R12", "players": 4, "rounds": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": 0},
             {"seat": 1, "options_include": "Glazed", "times": 1}, {"seat": 1, "options_include": "Jelly", "times": 1},
             {"seat": 2, "options_include": "Cruller", "times": 2},
             {"seat": 3, "options_include": "Sprinkle", "times": 2},
             {"seat": 4, "options_include": "Plain", "times": 2}],
   "expect": {"players": {"1": {"score": 6, "donuts": 1}, "2": {"score": 8, "donuts": 2}, "3": {"score": 4, "donuts": 2}, "4": {"score": 2, "donuts": 2}}}},
  {"name": "R13: a void Glazed does not block a lone non-void Glazed", "rule": "R13", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 6},
             {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Glazed"},
             {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Sprinkle"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 9, "donuts": 1}, "3": {"score": 4, "donuts": 1}, "4": {"score": 2, "donuts": 1}}}},
  {"name": "R14: scores and donuts after a round with a collision", "rule": "R14", "players": 4, "rounds": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Sprinkle"}, {"seat": 2, "options_include": "Sprinkle"},
             {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Plain"}],
   "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 0, "donuts": 0}, "3": {"score": 4, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},
  {"name": "R15: the game ends after round 10 (10 lone Crullers give 40)", "rule": "R15", "players": 4, "default": "decline",
   "rules": [{"seat": 1, "options_include": "Cruller", "times": "all"},
             {"seat": 2, "options_include": "Sprinkle", "times": "all"},
             {"seat": 3, "options_include": "Plain", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"winner": 1,
              "standings": {"1": 4010, "2": 2010, "3": 0, "4": 0},
              "players": {"1": {"score": 40, "donuts": 10}, "2": {"score": 20, "donuts": 10}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},
  {"name": "R16: seats level on score and donuts share the win", "rule": "R16", "players": 4, "default": "decline",
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 3}, {"seat": 4, "options_include": 3},
             {"seat": 1, "options_include": "Cruller", "times": 5}, {"seat": 1, "options_include": "Sprinkle", "times": 5},
             {"seat": 2, "options_include": "Sprinkle", "times": 5}, {"seat": 2, "options_include": "Cruller", "times": 5},
             {"seat": 3, "options_include": "Plain", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 3010, "2": 3010, "3": 0, "4": 0},
              "players": {"1": {"score": 30, "donuts": 10}, "2": {"score": 30, "donuts": 10}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},
  {"name": "R16: on equal scores, more donuts wins", "rule": "R16", "players": 4, "default": "decline",
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 4}, {"seat": 3, "options_include": 1}, {"seat": 4, "options_include": 5},
             {"seat": 1, "options_include": "Cruller", "times": 5}, {"seat": 1, "options_include": "Plain", "times": 5},
             {"seat": 2, "options_include": "Sprinkle", "times": "all"},
             {"seat": 3, "options_include": "Plain", "times": "all"},
             {"seat": 4, "options_include": "Plain", "times": "all"}],
   "expect": {"winner": 2,
              "standings": {"1": 2005, "2": 2010, "3": 0, "4": 0},
              "players": {"1": {"score": 20, "donuts": 5}, "2": {"score": 20, "donuts": 10}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}}
]
````
