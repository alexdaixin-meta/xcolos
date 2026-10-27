# 12 scenarios

- time: 2026-10-27T20:55:00+00:00 (70.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 0ac5f7f8e97adf17, reply sha256 c510458ce11aca4d

## Sent

````
SPEC:
{
  "name": "Code 777: Ask and Guess",
  "summary": "Each player sees every rack but their own. Players ask engine-answered counting questions and guess their own three hidden tiles; the first to 3 points ends the game.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "tiles_total": 28,
    "count_of_1": 1,
    "count_of_2": 2,
    "count_of_3": 3,
    "count_of_4": 4,
    "count_of_5": 5,
    "count_of_6": 6,
    "count_of_7": 7,
    "rack_size": 3,
    "starting_score": 0,
    "correct_guess_points": 1,
    "wrong_guess_points": -1,
    "pass_points": 0,
    "win_points": 3,
    "rounds_per_player": 10,
    "final_round_3_players": 30,
    "final_round_4_players": 40,
    "k_min": 1,
    "k_max": 7,
    "sum_threshold": 15,
    "pair_min_same": 2,
    "high_min": 5,
    "number_range_min": 1,
    "number_range_max": 7
  },
  "attributes": {
    "player": [
      {
        "key": "rack",
        "type": "list",
        "visible": "others",
        "initial": [],
        "meaning": "The player's three tiles. Every other player sees them; the owner never does.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points; may be negative.",
        "observable": true
      },
      {
        "key": "guess",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's answer to the guess poll: PASS or three numbers.",
        "observable": false
      },
      {
        "key": "guessed",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if the player submitted a guess (not PASS) this round.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s",
        "meaning": "The face-down pile.",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The public discard pile of revealed tiles.",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round number.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat of this round's active player: ((round - 1) mod N) + 1.",
        "observable": false
      },
      {
        "key": "question",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's chosen question: EVEN, HIGH, NUMBER, SUM15, PAIR or MISSING.",
        "observable": false
      },
      {
        "key": "respondent",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat named as respondent.",
        "observable": false
      },
      {
        "key": "k",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number named for the NUMBER question.",
        "observable": false
      },
      {
        "key": "answer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The engine-computed answer to this round's question.",
        "observable": true
      },
      {
        "key": "final_round",
        "type": "number",
        "visible": "public",
        "initial": "10 * N",
        "meaning": "The last round: 30 with 3 players, 40 with 4.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Fill the deck with the 28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s and seven 7s.",
    "Deal 3 tiles at random from deck to each player's rack, removing each from deck.",
    "Set every score to 0 and discard to empty; set final_round to 10 * N.",
    "Sync: each player is privately shown the racks of every other player, never their own."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; active_seat = ((round - 1) mod N) + 1; every guess = '' and guessed = false. Announce the round number and the active seat."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat",
      "answer": "a choice of question (EVEN, HIGH, NUMBER, SUM15, PAIR, MISSING) paired with a respondent, who is one other seat",
      "effect": "question and respondent are set from the choice."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat, only when question = NUMBER",
      "answer": "a whole number from 1 to 7",
      "effect": "k is set."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "answer is computed over the racks of every seat except respondent (the active player's rack included). EVEN = count of tiles in {2,4,6}; HIGH = count of tiles in {5,6,7}; NUMBER = count of tiles equal to k; SUM15 = count of those racks whose sum >= 15; PAIR = count of those racks holding at least two tiles of the same number; MISSING = count of the numbers 1..7 that appear on none of those racks. Announce the question, the respondent (and k if used) and the answer to everyone."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text: PASS, or three numbers from 1 to 7 (order irrelevant)",
      "effect": "guess is set for each player; guessed = (guess != PASS)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with guessed = true: if sorted(guess) equals sorted(rack), score += 1; otherwise score -= 1. A PASS leaves score unchanged."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with guessed = true: announce their rack to all, append the rack to discard, and set rack = []. If length(deck) < 3 * (number of players with guessed = true), move every tile from discard into deck. Then deal 3 tiles at random from deck to the rack of each player who guessed, removing each from deck."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is privately shown the current racks of all other players."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any score >= 3 or round >= final_round; otherwise continue."
    }
  ],
  "ending": {
    "condition": "max over players of score >= 3 OR round >= final_round (final_round = 10 * N)",
    "rank_by": "you.score",
    "decided_by": "The player with the highest score wins. Players tied at the top share it, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck holds 28 tiles (one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s), each player is dealt 3 tiles into rack, and the deck then holds 28 - 3N."
    },
    {
      "id": "R2",
      "text": "When racks are shown, each player sees every other player's rack and never their own."
    },
    {
      "id": "R3",
      "text": "When the game starts, every score is 0 and discard is empty."
    },
    {
      "id": "R4",
      "text": "When round r begins, the active seat is ((r - 1) mod N) + 1, so seat 1 is active in round 1."
    },
    {
      "id": "R5",
      "text": "When the active player chooses a respondent, the respondent must be a seat other than the active player."
    },
    {
      "id": "R6",
      "text": "When the question is NUMBER, the active player also names k from 1 to 7."
    },
    {
      "id": "R7",
      "text": "When an answer is computed, it counts only the racks of every seat except the respondent, including the active player's rack."
    },
    {
      "id": "R8",
      "text": "When the question is EVEN, the answer is the number of tiles showing 2, 4 or 6 on those racks."
    },
    {
      "id": "R9",
      "text": "When the question is HIGH, the answer is the number of tiles showing 5, 6 or 7 on those racks."
    },
    {
      "id": "R10",
      "text": "When the question is NUMBER with k, the answer is the number of tiles equal to k on those racks."
    },
    {
      "id": "R11",
      "text": "When the question is SUM15, the answer is the number of those racks whose three tiles sum to 15 or more."
    },
    {
      "id": "R12",
      "text": "When the question is PAIR, the answer is the number of those racks holding at least two tiles of the same number."
    },
    {
      "id": "R13",
      "text": "When the question is MISSING, the answer is how many of the numbers 1 to 7 appear on none of those racks."
    },
    {
      "id": "R14",
      "text": "When an answer is computed, the question, the respondent and the answer are announced to everyone."
    },
    {
      "id": "R15",
      "text": "When the guess poll runs, all players answer simultaneously, each with PASS or three numbers."
    },
    {
      "id": "R16",
      "text": "When a guess matches the player's rack as a multiset of three numbers, the player's score rises by 1."
    },
    {
      "id": "R17",
      "text": "When a guess does not match the player's rack, the player's score falls by 1, and the score may go negative."
    },
    {
      "id": "R18",
      "text": "When a player answers PASS, the player's score is unchanged and the rack is kept."
    },
    {
      "id": "R19",
      "text": "When a player guessed, right or wrong, their three tiles are announced to all and moved to discard, and they are dealt 3 new tiles from deck."
    },
    {
      "id": "R20",
      "text": "When the deck holds fewer than 3 times the number of guessers, all of discard is moved into deck before dealing."
    },
    {
      "id": "R21",
      "text": "When any player's score is 3 or more after scoring, the game ends."
    },
    {
      "id": "R22",
      "text": "When round 30 (with 3 players) or round 40 (with 4 players) has been played, the game ends."
    },
    {
      "id": "R23",
      "text": "When the game ends, the highest score wins, and a tie for the highest score is a draw shared by the tied players."
    }
  ],
  "offers": [
    {
      "question": "Choose a question and a respondent",
      "who": "the active seat only",
      "options": "each of EVEN, HIGH, NUMBER, SUM15, PAIR, MISSING, paired with each seat other than the active seat (6 \u00d7 (N - 1) options)"
    },
    {
      "question": "Choose k for NUMBER",
      "who": "the active seat, only when question = NUMBER",
      "options": "1, 2, 3, 4, 5, 6, 7"
    },
    {
      "question": "Guess poll",
      "who": "every seat",
      "options": "PASS, or any three numbers each from 1 to 7 (repeats allowed, order irrelevant)"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The designer's suggested size is 3 and the source allows 3 to 4. The minimum is 3 because with 2 players a respondent sees only the asker's rack, so answers reveal it almost directly. The maximum stays at 4, as in the source; more racks per question would make answers too diluted and turns too slow."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player picks questions and respondents whose answers best split the possible racks they could hold, uses the public discard and the tile counts, notes what the questions reveal to opponents, and passes until confident, because a wrong guess costs a point."
    },
    {
      "what": "No talk phase",
      "why": "The source explicitly has none; the engine-answered questions are the only shared information."
    },
    {
      "what": "Question and respondent combined into one choice, with k asked in a separate step only for NUMBER",
      "why": "It fits the engine's choice-from-a-list answer type while keeping the active player's single decision."
    },
    {
      "what": "An unparseable guess is treated as PASS",
      "why": "The source does not cover malformed answers; PASS is the neutral reading."
    },
    {
      "what": "When the deck is replenished, the whole discard pile moves into the deck",
      "why": "The source says the discard pile is shuffled in; drawing at random makes an explicit shuffle unnecessary."
    }
  ],
  "simplifications": [
    {
      "what": "The guess is free text parsed into three numbers rather than a menu of all 84 multisets",
      "why": "This avoids an oversized option list."
    },
    {
      "what": "The two ways the game can end share one ranking (highest score; ties share the win)",
      "why": "The source decides the winner the same way for both endings, and the engine treats a shared top as a draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: discard, round, answer.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Match options by content, not exact label. An option whose text starts with or contains the question name and a respondent seat (for example 'EVEN to seat 2') satisfies 'question offered'.
- For R4: check that seat 1 in round 1 and seat 2 in round 2 get question options, and that the other seats get only the guess poll.
- For R5: check that no offered option names the active seat itself as respondent (seat 1 sees only 'to seat 2' and 'to seat 3').
- For R6: accept k being folded into the option (for example 'NUMBER 5 to seat 2') or asked in a follow-up step. Check that the values 1 through 7 are all available, in whatever form the game offers them.
- Do not assert an exact answer that depends on the random deal. Either compute the expected answer from the racks the game actually dealt in that run (the respondent's view: all racks except its own), or assert only that the answer is a number between 0 and 3N - 3.
````

## Reply

````
```json
[
  {
    "name": "Setup: 3 tiles per rack, deck holds 28 - 9 = 19",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "seed": 1,
    "expect": {
      "lens": {
        "game": {"deck": 19, "discard": 0},
        "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}
      }
    }
  },
  {
    "name": "Setup with 4 players: deck holds 28 - 12 = 16",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "seed": 2,
    "expect": {
      "lens": {
        "game": {"deck": 16},
        "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}, "4": {"rack": 3}}
      }
    }
  },
  {
    "name": "Racks are dealt to every seat so they can be shown to the others",
    "rule": "R2",
    "players": 3,
    "rounds": 0,
    "seed": 3,
    "expect": {
      "lens": {"players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}}
    }
  },
  {
    "name": "At start every score is 0, discard is empty and round is 0",
    "rule": "R3",
    "players": 3,
    "rounds": 0,
    "seed": 4,
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}},
      "game": {"discard": [], "round": 0},
      "lens": {"game": {"discard": 0}}
    }
  },
  {
    "name": "Seat 1 asks in round 1, seat 2 asks in round 2, seat 3 only gets the poll",
    "rule": "R4",
    "players": 3,
    "rounds": 2,
    "seed": 5,
    "default": "decline",
    "expect": {
      "game": {"round": 2},
      "offered": [
        {"seat": 1, "option": "EVEN"},
        {"seat": 2, "option": "EVEN"}
      ],
      "not_offered": [{"seat": 3, "option": "EVEN"}]
    }
  },
  {
    "name": "Active seat 1 cannot name itself as respondent",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "seed": 6,
    "default": "decline",
    "expect": {
      "offered": [
        {"seat": 1, "option": "to seat 2"},
        {"seat": 1, "option": "to seat 3"}
      ],
      "not_offered": [{"seat": 1, "option": "to seat 1"}]
    }
  },
  {
    "name": "NUMBER question offers k from 1 to 7",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "seed": 7,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "NUMBER"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": 1},
        {"seat": 1, "option": 2},
        {"seat": 1, "option": 3},
        {"seat": 1, "option": 4},
        {"seat": 1, "option": 5},
        {"seat": 1, "option": 6},
        {"seat": 1, "option": 7}
      ]
    }
  },
  {
    "name": "Answer excludes the respondent and includes the asker (EVEN: 1 + 3 = 4)",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "seed": 8,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [2, 3, 5]},
        "2": {"rack": [2, 4, 6]},
        "3": {"rack": [2, 4, 6]}
      }
    },
    "rules": [{"seat": 1, "options_include": "EVEN"}],
    "expect": {
      "game": {"answer": 4},
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}}
    }
  },
  {
    "name": "EVEN counts tiles showing 2, 4 or 6 (2 + 2 = 4)",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "seed": 9,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [2, 4, 7]},
        "2": {"rack": [6, 6, 1]},
        "3": {"rack": [6, 6, 1]}
      }
    },
    "rules": [{"seat": 1, "options_include": "EVEN"}],
    "expect": {"game": {"answer": 4}}
  },
  {
    "name": "HIGH counts tiles showing 5, 6 or 7 (3 + 1 = 4)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 10,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [5, 6, 7]},
        "2": {"rack": [1, 5, 2]},
        "3": {"rack": [1, 5, 2]}
      }
    },
    "rules": [{"seat": 1, "options_include": "HIGH"}],
    "expect": {"game": {"answer": 4}}
  },
  {
    "name": "NUMBER with k = 7 counts the 7s (2 + 1 = 3)",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "seed": 11,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [7, 7, 1]},
        "2": {"rack": [7, 2, 2]},
        "3": {"rack": [7, 2, 2]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "NUMBER"},
      {"seat": 1, "options_include": 7}
    ],
    "expect": {"game": {"answer": 3}}
  },
  {
    "name": "SUM15 counts racks summing to 15 or more (15 counts, 14 does not)",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "seed": 12,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [7, 7, 1]},
        "2": {"rack": [5, 5, 4]},
        "3": {"rack": [5, 5, 4]}
      }
    },
    "rules": [{"seat": 1, "options_include": "SUM15"}],
    "expect": {"game": {"answer": 1}}
  },
  {
    "name": "PAIR counts racks holding two or more of a number (a triple counts once)",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "seed": 13,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [3, 3, 3]},
        "2": {"rack": [1, 2, 4]},
        "3": {"rack": [1, 2, 4]}
      }
    },
    "rules": [{"seat": 1, "options_include": "PAIR"}],
    "expect": {"game": {"answer": 1}}
  },
  {
    "name": "MISSING counts the numbers 1-7 on no counted rack (4, 5, 6, 7 = 4)",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "seed": 14,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [1, 2, 3]},
        "2": {"rack": [1, 2, 3]},
        "3": {"rack": [1, 2, 3]}
      }
    },
    "rules": [{"seat": 1, "options_include": "MISSING"}],
    "expect": {"game": {"answer": 4}}
  },
  {
    "name": "The computed answer is published (HIGH: 1 + 0 = 1)",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "seed": 15,
    "default": "decline",
    "given": {
      "players": {
        "1": {"rack": [7, 1, 1]},
        "2": {"rack": [2, 3, 4]},
        "3": {"rack": [2, 3, 4]}
      }
    },
    "rules": [{"seat": 1, "options_include": "HIGH"}],
    "expect": {"game": {"answer": 1, "round": 1}}
  },
  {
    "name": "Two seats guess correctly in the same poll and both score",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "seed": 16,
    "default": "decline",
    "given": {
      "players": {
        "2": {"rack": [1, 2, 3]},
        "3": {"rack": [4, 4, 5]}
      },
      "game": {"deck": [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]}
    },
    "rules": [
      {"seat": 2, "options_include": "PASS", "answer": "3 1 2"},
      {"seat": 3, "options_include": "PASS", "answer": "5 4 4"}
    ],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 1}, "3": {"score": 1}}
    }
  },
  {
    "name": "Correct guess in any order scores +1",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "seed": 17,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [3, 1, 3]}},
      "game": {"deck": [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]}
    },
    "rules": [{"seat": 2, "options_include": "PASS", "answer": "3 3 1"}],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 1}, "3": {"score": 0}}
    }
  },
  {
    "name": "Wrong guess scores -1 and can go negative",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "seed": 18,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [1, 2, 3], "score": 0}},
      "game": {"deck": [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]}
    },
    "rules": [{"seat": 2, "options_include": "PASS", "answer": "7 7 7"}],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": -1}, "3": {"score": 0}}
    }
  },
  {
    "name": "PASS keeps score and rack, nothing is discarded",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "seed": 19,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [1, 2, 3], "score": 2}}
    },
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 2}, "3": {"score": 0}},
      "lens": {"game": {"discard": 0}, "players": {"2": {"rack": 3}}}
    }
  },
  {
    "name": "A guesser's rack goes to discard and 3 new tiles come from the deck",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "seed": 20,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [1, 2, 3]}},
      "game": {"deck": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4], "discard": []}
    },
    "rules": [{"seat": 2, "options_include": "PASS", "answer": "7 7 7"}],
    "expect": {
      "players": {"2": {"score": -1}},
      "lens": {"game": {"discard": 3, "deck": 7}, "players": {"2": {"rack": 3}}}
    }
  },
  {
    "name": "A short deck takes in the whole discard before dealing",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "seed": 21,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [1, 2, 3]}},
      "game": {"deck": [4, 4], "discard": [5, 5, 5, 6, 6, 6]}
    },
    "rules": [{"seat": 2, "options_include": "PASS", "answer": "7 7 7"}],
    "expect": {
      "players": {"2": {"score": -1}},
      "lens": {"game": {"discard": 0, "deck": 8}, "players": {"2": {"rack": 3}}}
    }
  },
  {
    "name": "Reaching 3 points ends the game and that seat wins",
    "rule": "R21",
    "players": 3,
    "seed": 22,
    "default": "decline",
    "given": {
      "players": {"2": {"rack": [1, 2, 3], "score": 2}},
      "game": {"deck": [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]}
    },
    "rules": [{"seat": 2, "options_include": "PASS", "answer": "1 2 3"}],
    "expect": {
      "winner": 2,
      "standings": {"1": 0, "2": 3, "3": 0},
      "players": {"2": {"score": 3}}
    }
  },
  {
    "name": "With 3 players the game ends after round 30; highest score wins",
    "rule": "R22",
    "players": 3,
    "seed": 23,
    "default": "decline",
    "given": {
      "players": {"1": {"score": 1}, "2": {"score": 2}, "3": {"score": 0}},
      "game": {"round": 29}
    },
    "expect": {
      "winner": 2,
      "standings": {"1": 1, "2": 2, "3": 0},
      "game": {"round": 30}
    }
  },
  {
    "name": "With 4 players the game ends after round 40",
    "rule": "R22",
    "players": 4,
    "seed": 24,
    "default": "decline",
    "given": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 1}, "4": {"score": 0}},
      "game": {"round": 39}
    },
    "expect": {
      "winner": 3,
      "standings": {"1": 0, "2": 0, "3": 1, "4": 0},
      "game": {"round": 40}
    }
  },
  {
    "name": "A tie at the top is shared by the tied seats",
    "rule": "R23",
    "players": 3,
    "seed": 25,
    "default": "decline",
    "given": {
      "players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 0}},
      "game": {"round": 29}
    },
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 2, "2": 2, "3": 0}
    }
  }
]
```
````
