# 10 scenarios

- time: 2026-10-27T20:53:39+00:00 (42.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 964124427e27e087, reply sha256 3faa992f293ba02e

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
Do not assume the exact option strings. The interface fixes attribute names, not option labels.
- **Matching question options:** match by content, either an option containing the question name (e.g. 'EVEN') or the full combined form 'EVEN to seat 2'.
- **Respondent rule:** check that seat 1 is never offered any option naming seat 1 as respondent.
- **Active seat:** check that only the active seat gets question options, using containment matching. In round 2, seat 2's options should name seats 1 and 3.
- **NUMBER test:** first pick an option containing 'NUMBER'. Then expect a follow-up choice offering k from 1 to 7, matched by value.
- **Answer checks:** where possible, assert on the public `answer` and on scores rather than on option text.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup deals 3 tiles to each rack and leaves 28 - 3N = 19 in the deck",
   "rule": "R1", "players": 3, "rounds": 0, "seed": 1,
   "expect": {"lens": {"game": {"deck": 19},
                       "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}}}},

  {"name": "Setup with 4 players leaves 28 - 12 = 16 tiles in the deck",
   "rule": "R1", "players": 4, "rounds": 0, "seed": 2,
   "expect": {"lens": {"game": {"deck": 16},
                       "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}, "4": {"rack": 3}}}}},

  {"name": "Every rack holds three tiles when racks are first shown",
   "rule": "R2", "players": 3, "rounds": 0, "seed": 3,
   "expect": {"lens": {"players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}}}},

  {"name": "Game starts with all scores 0 and an empty discard",
   "rule": "R3", "players": 3, "rounds": 0, "seed": 4,
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}},
              "game": {"discard": [], "round": 0}}},

  {"name": "Round 1: only seat 1 is offered question choices",
   "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "decline",
   "expect": {"game": {"round": 1},
              "offered": [{"seat": 1, "option": "EVEN"}],
              "not_offered": [{"seat": 2, "option": "EVEN"}, {"seat": 3, "option": "EVEN"}]}},

  {"name": "Round 2: seat 2 is active and may name seats 1 and 3",
   "rule": "R4", "players": 3, "rounds": 1, "seed": 6, "default": "decline",
   "given": {"game": {"round": 1}},
   "expect": {"game": {"round": 2},
              "offered": [{"seat": 2, "option": "EVEN"},
                          {"seat": 2, "option": "EVEN to seat 1"},
                          {"seat": 2, "option": "EVEN to seat 3"}],
              "not_offered": [{"seat": 1, "option": "EVEN"},
                              {"seat": 3, "option": "EVEN"},
                              {"seat": 2, "option": "EVEN to seat 2"}]}},

  {"name": "Active seat 1 cannot name itself as respondent",
   "rule": "R5", "players": 3, "rounds": 1, "seed": 7, "default": "decline",
   "expect": {"offered": [{"seat": 1, "option": "EVEN to seat 2"},
                          {"seat": 1, "option": "EVEN to seat 3"}],
              "not_offered": [{"seat": 1, "option": "EVEN to seat 1"},
                              {"seat": 1, "option": "HIGH to seat 1"}]}},

  {"name": "NUMBER asks for k from 1 to 7; k=5 counts two 5s",
   "rule": "R6", "players": 3, "rounds": 1, "seed": 8, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "NUMBER"},
             {"seat": 1, "options_include": 5}],
   "expect": {"game": {"answer": 2},
              "offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 7}]}},

  {"name": "HIGH excludes the respondent's rack and includes the active rack (1 + 3 = 4)",
   "rule": "R7", "players": 3, "rounds": 1, "seed": 9, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [7, 7, 7]},
                         "3": {"rack": [7, 7, 7]}}},
   "rules": [{"seat": 1, "options_include": "HIGH"}],
   "expect": {"game": {"answer": 4}}},

  {"name": "EVEN counts tiles 2, 4 and 6 on the counted racks",
   "rule": "R8", "players": 3, "rounds": 1, "seed": 10, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "EVEN"}],
   "expect": {"game": {"answer": 3}}},

  {"name": "HIGH counts tiles 5, 6 and 7 on the counted racks",
   "rule": "R9", "players": 3, "rounds": 1, "seed": 11, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "HIGH"}],
   "expect": {"game": {"answer": 4}}},

  {"name": "NUMBER with k=7 counts the tiles equal to 7",
   "rule": "R10", "players": 3, "rounds": 1, "seed": 12, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 7, 7]},
                         "2": {"rack": [7, 5, 6]},
                         "3": {"rack": [7, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "NUMBER"},
             {"seat": 1, "options_include": 7}],
   "expect": {"game": {"answer": 3}}},

  {"name": "SUM15 counts the racks that sum to 15 or more (13 no, 16 yes)",
   "rule": "R11", "players": 3, "rounds": 1, "seed": 13, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "SUM15"}],
   "expect": {"game": {"answer": 1}}},

  {"name": "PAIR counts the racks holding two tiles of the same number",
   "rule": "R12", "players": 3, "rounds": 1, "seed": 14, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "PAIR"}],
   "expect": {"game": {"answer": 1}}},

  {"name": "MISSING counts numbers 1-7 absent from the counted racks (1 and 3 missing)",
   "rule": "R13", "players": 3, "rounds": 1, "seed": 15, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "MISSING"}],
   "expect": {"game": {"answer": 2}}},

  {"name": "The computed answer is published for everyone to see",
   "rule": "R14", "players": 3, "rounds": 1, "seed": 16, "default": "decline",
   "given": {"players": {"1": {"rack": [6, 6, 6]},
                         "2": {"rack": [7, 7, 7]},
                         "3": {"rack": [7, 7, 7]}}},
   "rules": [{"seat": 1, "options_include": "EVEN"}],
   "expect": {"game": {"answer": 3, "round": 1}}},

  {"name": "In the same poll two seats guess correctly and both score",
   "rule": "R15", "players": 3, "rounds": 1, "seed": 17, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [1, 3, 3]}}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "5 5 6"},
             {"seat": 3, "options_include": "3 1 3"}],
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 1}, "3": {"score": 1}}}},

  {"name": "A correct guess in any order scores +1",
   "rule": "R16", "players": 3, "rounds": 1, "seed": 18, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "7 4 2"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 0}}}},

  {"name": "A wrong guess scores -1 and the score may go negative",
   "rule": "R17", "players": 3, "rounds": 1, "seed": 19, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "1 1 1"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": -1}, "2": {"score": 0}, "3": {"score": 0}}}},

  {"name": "PASS leaves the score unchanged and nothing goes to discard",
   "rule": "R18", "players": 3, "rounds": 1, "seed": 20, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7], "score": 2},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 2}},
              "game": {"discard": []}}},

  {"name": "A guesser's three tiles go to the discard",
   "rule": "R19", "players": 3, "rounds": 1, "seed": 21, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "1 1 1"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": -1}},
              "lens": {"game": {"discard": 3}}}},

  {"name": "Deck of 2 is short for 1 guesser, so the whole discard moves to the deck",
   "rule": "R20", "players": 3, "rounds": 1, "seed": 22, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}},
             "game": {"deck": [7, 7], "discard": [1, 3, 3]}},
   "rules": [{"seat": 1, "options_include": "2 4 7"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 1}},
              "lens": {"game": {"discard": 0, "deck": 5}}}},

  {"name": "Reaching 3 points ends the game and that seat wins",
   "rule": "R21", "players": 3, "seed": 23, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7], "score": 2},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "2 4 7"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": 1,
              "standings": {"1": 3, "2": 0, "3": 0},
              "game": {"round": 1}}},

  {"name": "With 3 players the game ends after round 30 and the top score wins",
   "rule": "R22", "players": 3, "seed": 24, "default": "decline",
   "given": {"players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 2}},
             "game": {"round": 29}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": 3,
              "standings": {"1": 1, "2": 0, "3": 2},
              "game": {"round": 30}}},

  {"name": "With 4 players the game ends after round 40",
   "rule": "R22", "players": 4, "seed": 25, "default": "decline",
   "given": {"players": {"1": {"score": 0}, "2": {"score": 2}, "3": {"score": 1}, "4": {"score": 0}},
             "game": {"round": 39}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"},
             {"seat": 4, "options_include": "PASS"}],
   "expect": {"winner": 2,
              "standings": {"1": 0, "2": 2, "3": 1, "4": 0},
              "game": {"round": 40}}},

  {"name": "A tie for the highest score at the end is shared",
   "rule": "R23", "players": 3, "seed": 26, "default": "decline",
   "given": {"players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 0}},
             "game": {"round": 29}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 2, "2": 2, "3": 0}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Setup deals 3 tiles to each rack and leaves 28 - 3N = 19 in the deck",
   "rule": "R1", "players": 3, "rounds": 0, "seed": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 19},
                       "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}}}},

  {"name": "Setup with 4 players leaves 28 - 12 = 16 tiles in the deck",
   "rule": "R1", "players": 4, "rounds": 0, "seed": 2,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 16},
                       "players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}, "4": {"rack": 3}}}}},

  {"name": "Every rack holds three tiles when racks are first shown",
   "rule": "R2", "players": 3, "rounds": 0, "seed": 3,
   "rules": [],
   "expect": {"lens": {"players": {"1": {"rack": 3}, "2": {"rack": 3}, "3": {"rack": 3}}}}},

  {"name": "Game starts with all scores 0 and an empty discard",
   "rule": "R3", "players": 3, "rounds": 0, "seed": 4,
   "rules": [],
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}},
              "game": {"discard": [], "round": 0}}},

  {"name": "Round 1: only seat 1 is offered question choices",
   "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "decline",
   "rules": [{"seat": 1, "options_include": "EVEN"},
             {"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"game": {"round": 1},
              "offered": [{"seat": 1, "option": "EVEN"}],
              "not_offered": [{"seat": 2, "option": "EVEN"}, {"seat": 3, "option": "EVEN"}]}},

  {"name": "Round 2: seat 2 is active and may name seats 1 and 3",
   "rule": "R4", "players": 3, "rounds": 1, "seed": 6, "default": "decline",
   "given": {"game": {"round": 1}},
   "rules": [{"seat": 2, "options_include": "EVEN"},
             {"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"game": {"round": 2},
              "offered": [{"seat": 2, "option": "EVEN"},
                          {"seat": 2, "option": "EVEN to seat 1"},
                          {"seat": 2, "option": "EVEN to seat 3"}],
              "not_offered": [{"seat": 1, "option": "EVEN"},
                              {"seat": 3, "option": "EVEN"},
                              {"seat": 2, "option": "EVEN to seat 2"}]}},

  {"name": "Active seat 1 cannot name itself as respondent",
   "rule": "R5", "players": 3, "rounds": 1, "seed": 7, "default": "decline",
   "rules": [{"seat": 1, "options_include": "EVEN"},
             {"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"offered": [{"seat": 1, "option": "EVEN to seat 2"},
                          {"seat": 1, "option": "EVEN to seat 3"}],
              "not_offered": [{"seat": 1, "option": "EVEN to seat 1"},
                              {"seat": 1, "option": "HIGH to seat 1"}]}},

  {"name": "NUMBER asks for k from 1 to 7; k=5 counts two 5s",
   "rule": "R6", "players": 3, "rounds": 1, "seed": 8, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "NUMBER"},
             {"seat": 1, "options_include": 5}],
   "expect": {"game": {"answer": 2},
              "offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 7}]}},

  {"name": "HIGH excludes the respondent's rack and includes the active rack (1 + 3 = 4)",
   "rule": "R7", "players": 3, "rounds": 1, "seed": 9, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [7, 7, 7]},
                         "3": {"rack": [7, 7, 7]}}},
   "rules": [{"seat": 1, "options_include": "HIGH"}],
   "expect": {"game": {"answer": 4}}},

  {"name": "EVEN counts tiles 2, 4 and 6 on the counted racks",
   "rule": "R8", "players": 3, "rounds": 1, "seed": 10, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "EVEN"}],
   "expect": {"game": {"answer": 3}}},

  {"name": "HIGH counts tiles 5, 6 and 7 on the counted racks",
   "rule": "R9", "players": 3, "rounds": 1, "seed": 11, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "HIGH"}],
   "expect": {"game": {"answer": 4}}},

  {"name": "NUMBER with k=7 counts the tiles equal to 7",
   "rule": "R10", "players": 3, "rounds": 1, "seed": 12, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 7, 7]},
                         "2": {"rack": [7, 5, 6]},
                         "3": {"rack": [7, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "NUMBER"},
             {"seat": 1, "options_include": 7}],
   "expect": {"game": {"answer": 3}}},

  {"name": "SUM15 counts the racks that sum to 15 or more (13 no, 16 yes)",
   "rule": "R11", "players": 3, "rounds": 1, "seed": 13, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "SUM15"}],
   "expect": {"game": {"answer": 1}}},

  {"name": "PAIR counts the racks holding two tiles of the same number",
   "rule": "R12", "players": 3, "rounds": 1, "seed": 14, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "PAIR"}],
   "expect": {"game": {"answer": 1}}},

  {"name": "MISSING counts numbers 1-7 absent from the counted racks (1 and 3 missing)",
   "rule": "R13", "players": 3, "rounds": 1, "seed": 15, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "MISSING"}],
   "expect": {"game": {"answer": 2}}},

  {"name": "The computed answer is published for everyone to see",
   "rule": "R14", "players": 3, "rounds": 1, "seed": 16, "default": "decline",
   "given": {"players": {"1": {"rack": [6, 6, 6]},
                         "2": {"rack": [7, 7, 7]},
                         "3": {"rack": [7, 7, 7]}}},
   "rules": [{"seat": 1, "options_include": "EVEN"}],
   "expect": {"game": {"answer": 3, "round": 1}}},

  {"name": "In the same poll two seats guess correctly and both score",
   "rule": "R15", "players": 3, "rounds": 1, "seed": 17, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [1, 3, 3]}}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "5 5 6"},
             {"seat": 3, "options_include": "3 1 3"}],
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 1}, "3": {"score": 1}}}},

  {"name": "A correct guess in any order scores +1",
   "rule": "R16", "players": 3, "rounds": 1, "seed": 18, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "7 4 2"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 0}}}},

  {"name": "A wrong guess scores -1 and the score may go negative",
   "rule": "R17", "players": 3, "rounds": 1, "seed": 19, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "1 1 1"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": -1}, "2": {"score": 0}, "3": {"score": 0}}}},

  {"name": "PASS leaves the score unchanged and nothing goes to discard",
   "rule": "R18", "players": 3, "rounds": 1, "seed": 20, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7], "score": 2},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 2}},
              "game": {"discard": []}}},

  {"name": "A guesser's three tiles go to the discard",
   "rule": "R19", "players": 3, "rounds": 1, "seed": 21, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "1 1 1"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": -1}},
              "lens": {"game": {"discard": 3}}}},

  {"name": "Deck of 2 is short for 1 guesser, so the whole discard moves to the deck",
   "rule": "R20", "players": 3, "rounds": 1, "seed": 22, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7]},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}},
             "game": {"deck": [7, 7], "discard": [1, 3, 3]}},
   "rules": [{"seat": 1, "options_include": "2 4 7"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"players": {"1": {"score": 1}},
              "lens": {"game": {"discard": 0, "deck": 5}}}},

  {"name": "Reaching 3 points ends the game and that seat wins",
   "rule": "R21", "players": 3, "seed": 23, "default": "decline",
   "given": {"players": {"1": {"rack": [2, 4, 7], "score": 2},
                         "2": {"rack": [5, 5, 6]},
                         "3": {"rack": [5, 5, 6]}}},
   "rules": [{"seat": 1, "options_include": "2 4 7"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": 1,
              "standings": {"1": 3, "2": 0, "3": 0},
              "game": {"round": 1}}},

  {"name": "With 3 players the game ends after round 30 and the top score wins",
   "rule": "R22", "players": 3, "seed": 24, "default": "decline",
   "given": {"players": {"1": {"score": 1}, "2": {"score": 0}, "3": {"score": 2}},
             "game": {"round": 29}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": 3,
              "standings": {"1": 1, "2": 0, "3": 2},
              "game": {"round": 30}}},

  {"name": "With 4 players the game ends after round 40",
   "rule": "R22", "players": 4, "seed": 25, "default": "decline",
   "given": {"players": {"1": {"score": 0}, "2": {"score": 2}, "3": {"score": 1}, "4": {"score": 0}},
             "game": {"round": 39}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"},
             {"seat": 4, "options_include": "PASS"}],
   "expect": {"winner": 2,
              "standings": {"1": 0, "2": 2, "3": 1, "4": 0},
              "game": {"round": 40}}},

  {"name": "A tie for the highest score at the end is shared",
   "rule": "R23", "players": 3, "seed": 26, "default": "decline",
   "given": {"players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 0}},
             "game": {"round": 29}},
   "rules": [{"seat": 1, "options_include": "PASS"},
             {"seat": 2, "options_include": "PASS"},
             {"seat": 3, "options_include": "PASS"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": 2, "2": 2, "3": 0}}}
]
```
````
