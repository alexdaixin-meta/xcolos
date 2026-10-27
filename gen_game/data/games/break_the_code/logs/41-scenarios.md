# 41 scenarios

- time: 2026-10-27T19:12:32+00:00 (59.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 dd31654419288ef8, reply sha256 905851eff53fa5ea

## Sent

````
SPEC:
{
  "name": "Break the Code: Duel of Two Tiles",
  "summary": "Two players each hide a two-tile code (tiles 0-5) every leg, then ask simultaneous property questions or guess the opponent's code; earlier correct guesses score more over 4 legs of 6 turns.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "legs": 4,
    "turns_per_leg": 6,
    "total_turns": 24,
    "starting_score": 0,
    "tile_min": 0,
    "tile_max": 5,
    "possible_codes": 21,
    "guess_score_base": 7,
    "sum_low_max": 3,
    "sum_middle_min": 4,
    "sum_middle_max": 6,
    "sum_high_min": 7,
    "sum_high_max": 10,
    "gap_pair": 0,
    "gap_adjacent": 1,
    "gap_apart_min": 2,
    "big_tile_min": 3,
    "edge_tile_low": 0,
    "edge_tile_high": 5,
    "wrong_guess_cost": 0,
    "tie_break_weight": 10
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "total points from correct guesses",
        "observable": true
      },
      {
        "key": "legs_solved",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of legs in which this player guessed the opponent's code; first tie-break",
        "observable": true
      },
      {
        "key": "code_low",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "low tile of this player's secret code for the current leg (0-5)",
        "observable": false
      },
      {
        "key": "code_high",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "high tile of this player's secret code for the current leg (0-5, at least code_low)",
        "observable": false
      },
      {
        "key": "solved",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once this player has guessed the opponent's code correctly in the current leg",
        "observable": false
      },
      {
        "key": "last_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this turn's action (sum, odd, gap, big, edge or guess low-high), or 'solved' if the player's choices are ignored",
        "observable": true
      },
      {
        "key": "last_answer",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the truthful answer to last_action, computed from the opponent's code",
        "observable": true
      },
      {
        "key": "guess_low",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "low tile of this turn's guess, if the action was a guess",
        "observable": false
      },
      {
        "key": "guess_high",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "high tile of this turn's guess, if the action was a guess",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "leg",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current leg, 1 to 4; becomes 5 when the match is over",
        "observable": true
      },
      {
        "key": "turn_in_leg",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current turn within the leg, 1 to 6",
        "observable": true
      },
      {
        "key": "seat1_code_low",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "mirror of seat 1's code_low, so that seat 2's questions can be answered (player-attribute compare workaround)",
        "observable": false
      },
      {
        "key": "seat1_code_high",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "mirror of seat 1's code_high",
        "observable": false
      },
      {
        "key": "seat2_code_low",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "mirror of seat 2's code_low",
        "observable": false
      },
      {
        "key": "seat2_code_high",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "mirror of seat 2's code_high",
        "observable": false
      }
    ]
  },
  "setup": [
    "Two seats are filled; score and legs_solved start at 0 for both.",
    "leg is set to 1 and turn_in_leg is set to 1.",
    "Both players are told the rules: 4 legs of 6 turns, the 21 codes, the five questions and how guesses score."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when turn_in_leg == 1: set solved = false, last_action = '', last_answer = '' for both players"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of the 21 codes: 0-0, 0-1, 0-2, 0-3, 0-4, 0-5, 1-1, 1-2, 1-3, 1-4, 1-5, 2-2, 2-3, 2-4, 2-5, 3-3, 3-4, 3-5, 4-4, 4-5, 5-5",
      "effect": "when turn_in_leg == 1: set code_low and code_high from the chosen code (low <= high), and copy them to seatN_code_low and seatN_code_high; no one sees another's choice"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "each player is shown their own code_low and code_high, their score, legs_solved, leg and turn_in_leg"
    },
    {
      "action": "poll",
      "who": "each player with solved == false",
      "answer": "one of 26 choices: sum, odd, gap, big, edge, or guess X-Y for one of the 21 codes",
      "effect": "set last_action to the choice; for a guess, set guess_low and guess_high from it. Players with solved == true are not asked and get last_action = 'solved'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each unsolved player, with the opponent's code (L, H) taken from the opponent's mirror attributes: sum -> last_answer = LOW if L+H <= 3, MIDDLE if 4 <= L+H <= 6, HIGH if L+H >= 7; odd -> number of odd tiles among L, H (0-2); gap -> PAIR if H-L == 0, ADJACENT if H-L == 1, APART if H-L >= 2; big -> number of tiles >= 3 (0-2); edge -> number of tiles equal to 0 or 5 (0-2); guess -> if guess_low == L and guess_high == H then last_answer = CORRECT, score += 7 - turn_in_leg, legs_solved += 1, solved = true; otherwise last_answer = WRONG with the count of guessed tiles that appear in the code, each code tile matching at most one guessed tile (0 or 1), and no other cost"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce to both: 'Leg {leg}, turn {turn_in_leg}. Seat 1: {last_action} -> {last_answer}. Seat 2: {last_action} -> {last_answer}. Scores: {score} / {score}.'"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when turn_in_leg == 6: reveal both codes to both players: 'Seat 1's code was {seat1_code_low}-{seat1_code_high}; Seat 2's code was {seat2_code_low}-{seat2_code_high}.' Unsolved legs score nothing"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if turn_in_leg == 6 then turn_in_leg = 1 and leg += 1, else turn_in_leg += 1"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if leg > 4, otherwise continue with the next turn"
    }
  ],
  "ending": {
    "condition": "leg > 4",
    "rank_by": "you.score * 10 + you.legs_solved",
    "decided_by": "The higher total score wins. If scores are equal, the player who solved more legs wins (legs_solved is at most 4, so a weight of 10 keeps score first). If both are equal, both share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The match is 4 legs of 6 turns each, 24 turns in all, and both scores start at 0."
    },
    {
      "id": "R2",
      "text": "When turn_in_leg is 1, both players choose a code at the same time and in secret from the 21 codes low-high with 0 <= low <= high <= 5, for example 3-3."
    },
    {
      "id": "R3",
      "text": "A player's code is not changed during a leg; code_low and code_high are only set on turn 1 of a leg."
    },
    {
      "id": "R4",
      "text": "On each turn, every unsolved player picks at the same time exactly one action: sum, odd, gap, big, edge, or guess of a full code."
    },
    {
      "id": "R5",
      "text": "When a player asks sum and the opponent's code is (L, H), then the answer is LOW if L+H is 0-3, MIDDLE if 4-6, HIGH if 7-10; for example code 2-5 gives HIGH."
    },
    {
      "id": "R6",
      "text": "When a player asks odd, then the answer is the number of odd tiles in the opponent's code; for example code 1-3 gives 2 and code 0-4 gives 0."
    },
    {
      "id": "R7",
      "text": "When a player asks gap, then the answer is PAIR if H-L = 0, ADJACENT if H-L = 1, APART if H-L >= 2; for example code 2-4 gives APART."
    },
    {
      "id": "R8",
      "text": "When a player asks big, then the answer is the number of tiles that are 3 or more; for example code 2-3 gives 1."
    },
    {
      "id": "R9",
      "text": "When a player asks edge, then the answer is the number of tiles equal to 0 or 5; for example code 0-5 gives 2 and code 0-0 gives 2."
    },
    {
      "id": "R10",
      "text": "When a player repeats a question in the same leg, then the answer is the same as before, because the code has not changed."
    },
    {
      "id": "R11",
      "text": "When a guess equals the opponent's code exactly, then it is CORRECT and the guesser scores 7 minus turn_in_leg: 6 on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5, 1 on turn 6."
    },
    {
      "id": "R12",
      "text": "When a guess is correct, then the guesser's legs_solved increases by 1 and solved becomes true for the rest of the leg."
    },
    {
      "id": "R13",
      "text": "When a guess is wrong, then it scores 0, costs nothing, and the answer is how many guessed tiles appear in the code, each code tile matching at most one guessed tile; for example guess 3-3 against code 3-4 answers 1, and guess 1-2 against code 3-4 answers 0."
    },
    {
      "id": "R14",
      "text": "When a player has solved == true, then they are not asked for an action for the rest of that leg and score nothing more in it, while the other player keeps playing normally."
    },
    {
      "id": "R15",
      "text": "After both have chosen on a turn, then both players are told each player's action and its truthful answer, computed from the opponent's code."
    },
    {
      "id": "R16",
      "text": "When turn 6 of a leg ends, then both codes are revealed to both players, solved is reset, and the next leg starts with new codes; a leg nobody solved scores nothing."
    },
    {
      "id": "R17",
      "text": "When leg becomes 5 after the fourth leg, then the match ends."
    },
    {
      "id": "R18",
      "text": "When the match ends, then the higher score wins; on equal scores the player with more legs_solved wins; if both are equal the match is a draw (shared win)."
    }
  ],
  "offers": [
    {
      "question": "choose your secret code (turn 1 of each leg)",
      "who": "both seats",
      "options": "the 21 codes: 0-0, 0-1, 0-2, 0-3, 0-4, 0-5, 1-1, 1-2, 1-3, 1-4, 1-5, 2-2, 2-3, 2-4, 2-5, 3-3, 3-4, 3-5, 4-4, 4-5, 5-5"
    },
    {
      "question": "choose your action this turn",
      "who": "each seat with solved == false; a solved seat is not asked",
      "options": "sum, odd, gap, big, edge, or guess one of the 21 codes (guess 0-0 ... guess 5-5), 26 options in all"
    }
  ],
  "choices": [
    {
      "what": "2 players (min 2, max 2, suggested 2)",
      "why": "The designer set 2. Each player cracks the one opponent's code, and every answer is computed from that opponent's code, so a third seat would have no defined target. The strategy is to pick questions that split the remaining codes well, to guess when the expected value of an early guess beats one more question, and to choose codes that are hard to narrow down."
    },
    {
      "what": "No talk step",
      "why": "The source has no talk, and in a two-player duel talk would only add words that could be bluffs about one's own code; the rules are kept as written."
    },
    {
      "what": "The code is chosen from a list of the 21 valid codes",
      "why": "This makes an invalid code (low > high) impossible to enter with a single answer, and it matches the source's count of 21."
    },
    {
      "what": "A guess is one of 26 action options",
      "why": "Asking the action and the guess in one poll avoids a separate follow-up question that only guessers would get."
    },
    {
      "what": "Turns still run after both players have solved a leg",
      "why": "The source always plays 6 turns per leg. With nobody unsolved, a turn simply asks no one and scores nothing."
    },
    {
      "what": "Tie-break expressed as score * 10 + legs_solved",
      "why": "legs_solved is at most 4, so a weight of 10 keeps score first and legs solved second. A full tie becomes a shared win, which is the source's draw."
    }
  ],
  "simplifications": [
    {
      "what": "Each code is mirrored into hidden table attributes (seat1_code_low, seat1_code_high, seat2_code_low, seat2_code_high)",
      "why": "The engine has no operand for another player's attribute, and answers must be computed from the opponent's code (player_attribute_compare workaround)."
    },
    {
      "what": "Ranking by a single arithmetic expression, with the draw as a shared top value",
      "why": "The engine ranks by one expression and players level at the top share the win, which reproduces the source's draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, legs_solved, last_action, last_answer; table: leg, turn_in_leg.
````

## Reply

````
[
  {"name": "Setup: both scores start at 0, leg 1, turn 1", "rule": "R1", "players": 2, "rounds": 0,
   "expect": {"players": {"1": {"score": 0, "legs_solved": 0}, "2": {"score": 0, "legs_solved": 0}},
              "game": {"leg": 1, "turn_in_leg": 1}}},

  {"name": "Codes chosen on turn 1 are used to answer questions", "rule": "R2", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "2-5"}, {"seat": 2, "options_include": "1-3"},
             {"seat": 1, "options_include": "sum"}, {"seat": 2, "options_include": "gap"}],
   "expect": {"players": {"1": {"last_action": "sum", "last_answer": "MIDDLE"}, "2": {"last_action": "gap", "last_answer": "APART"}},
              "game": {"leg": 1, "turn_in_leg": 2}}},

  {"name": "Code chosen on turn 1 is kept on turn 2", "rule": "R3", "players": 2, "rounds": 2,
   "rules": [{"seat": 2, "options_include": "4-5"},
             {"seat": 1, "options_include": "sum"}, {"seat": 1, "options_include": "big"}],
   "expect": {"players": {"1": {"last_action": "big", "last_answer": "2"}}, "game": {"turn_in_leg": 3}}},

  {"name": "Each unsolved player is offered the five questions and guesses", "rule": "R4", "players": 2, "rounds": 1,
   "expect": {"offered": [{"seat": 1, "option": "sum"}, {"seat": 1, "option": "odd"}, {"seat": 1, "option": "gap"},
                          {"seat": 1, "option": "big"}, {"seat": 1, "option": "edge"}, {"seat": 1, "option": "guess 3-3"},
                          {"seat": 2, "option": "sum"}, {"seat": 2, "option": "guess 0-5"}]}},

  {"name": "Sum: 2-5 gives HIGH, 0-1 gives LOW", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 1, "seat2_code_low": 2, "seat2_code_high": 5},
             "players": {"1": {"code_low": 0, "code_high": 1}, "2": {"code_low": 2, "code_high": 5}}},
   "rules": [{"seat": 1, "options_include": "sum"}, {"seat": 2, "options_include": "sum"}],
   "expect": {"players": {"1": {"last_answer": "HIGH"}, "2": {"last_answer": "LOW"}}}},

  {"name": "Odd: 1-3 gives 2, 0-4 gives 0", "rule": "R6", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 4, "seat2_code_low": 1, "seat2_code_high": 3},
             "players": {"1": {"code_low": 0, "code_high": 4}, "2": {"code_low": 1, "code_high": 3}}},
   "rules": [{"seat": 1, "options_include": "odd"}, {"seat": 2, "options_include": "odd"}],
   "expect": {"players": {"1": {"last_answer": "2"}, "2": {"last_answer": "0"}}}},

  {"name": "Gap: 2-4 gives APART, 3-3 gives PAIR", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 3, "seat1_code_high": 3, "seat2_code_low": 2, "seat2_code_high": 4},
             "players": {"1": {"code_low": 3, "code_high": 3}, "2": {"code_low": 2, "code_high": 4}}},
   "rules": [{"seat": 1, "options_include": "gap"}, {"seat": 2, "options_include": "gap"}],
   "expect": {"players": {"1": {"last_answer": "APART"}, "2": {"last_answer": "PAIR"}}}},

  {"name": "Big: 2-3 gives 1, 4-5 gives 2", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 4, "seat1_code_high": 5, "seat2_code_low": 2, "seat2_code_high": 3},
             "players": {"1": {"code_low": 4, "code_high": 5}, "2": {"code_low": 2, "code_high": 3}}},
   "rules": [{"seat": 1, "options_include": "big"}, {"seat": 2, "options_include": "big"}],
   "expect": {"players": {"1": {"last_answer": "1"}, "2": {"last_answer": "2"}}}},

  {"name": "Edge: 0-5 gives 2, 0-0 gives 2", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 0, "seat2_code_high": 5},
             "players": {"1": {"code_low": 0, "code_high": 0}, "2": {"code_low": 0, "code_high": 5}}},
   "rules": [{"seat": 1, "options_include": "edge"}, {"seat": 2, "options_include": "edge"}],
   "expect": {"players": {"1": {"last_answer": "2"}, "2": {"last_answer": "2"}}}},

  {"name": "Repeating odd in the same leg gives the same answer", "rule": "R10", "players": 2, "rounds": 2,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 1, "seat2_code_high": 4},
             "players": {"1": {"code_low": 0, "code_high": 0}, "2": {"code_low": 1, "code_high": 4}}},
   "rules": [{"seat": 1, "options_include": "odd", "times": 2}],
   "expect": {"players": {"1": {"last_action": "odd", "last_answer": "1"}}, "game": {"turn_in_leg": 4}}},

  {"name": "Correct guess on turn 3 scores 4", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 3, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 2, "seat2_code_high": 5},
             "players": {"1": {"code_low": 0, "code_high": 0, "score": 0}, "2": {"code_low": 2, "code_high": 5, "score": 0}}},
   "rules": [{"seat": 1, "options_include": "guess 2-5"}, {"seat": 2, "options_include": "sum"}],
   "expect": {"players": {"1": {"score": 4, "last_answer": "CORRECT"}, "2": {"score": 0}}}},

  {"name": "Correct guess adds a solved leg and the solver sits out the next turn", "rule": "R12", "players": 2, "rounds": 2,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 1, "seat2_code_high": 4},
             "players": {"1": {"code_low": 0, "code_high": 0}, "2": {"code_low": 1, "code_high": 4}}},
   "rules": [{"seat": 1, "options_include": "guess 1-4"}, {"seat": 2, "options_include": "sum", "times": "all"}],
   "expect": {"players": {"1": {"score": 5, "legs_solved": 1, "last_action": "solved"}, "2": {"score": 0, "legs_solved": 0}}}},

  {"name": "Wrong guess scores 0 and costs nothing", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 3, "seat2_code_high": 4},
             "players": {"1": {"code_low": 0, "code_high": 0, "score": 3, "legs_solved": 1}, "2": {"code_low": 3, "code_high": 4}}},
   "rules": [{"seat": 1, "options_include": "guess 3-3"}, {"seat": 2, "options_include": "sum"}],
   "expect": {"players": {"1": {"score": 3, "legs_solved": 1}}}},

  {"name": "A solved player is not asked and scores nothing; the other keeps playing", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 3, "seat1_code_low": 2, "seat1_code_high": 2, "seat2_code_low": 1, "seat2_code_high": 4},
             "players": {"1": {"code_low": 2, "code_high": 2, "solved": true, "score": 5, "legs_solved": 1},
                         "2": {"code_low": 1, "code_high": 4}}},
   "rules": [{"seat": 2, "options_include": "guess 2-2"}],
   "expect": {"players": {"1": {"score": 5, "legs_solved": 1, "last_action": "solved"}, "2": {"score": 4, "legs_solved": 1, "last_answer": "CORRECT"}},
              "not_offered": [{"seat": 1, "option": "sum"}, {"seat": 1, "option": "guess 1-4"}],
              "offered": [{"seat": 2, "option": "sum"}]}},

  {"name": "Both actions and their truthful answers are reported", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"game": {"turn_in_leg": 2, "seat1_code_low": 3, "seat1_code_high": 5, "seat2_code_low": 1, "seat2_code_high": 2},
             "players": {"1": {"code_low": 3, "code_high": 5}, "2": {"code_low": 1, "code_high": 2}}},
   "rules": [{"seat": 1, "options_include": "gap"}, {"seat": 2, "options_include": "big"}],
   "expect": {"players": {"1": {"last_action": "gap", "last_answer": "ADJACENT"}, "2": {"last_action": "big", "last_answer": "2"}}}},

  {"name": "After turn 6 the next leg starts and solved is reset", "rule": "R16", "players": 2, "rounds": 2,
   "given": {"game": {"leg": 1, "turn_in_leg": 6, "seat1_code_low": 0, "seat1_code_high": 0, "seat2_code_low": 1, "seat2_code_high": 1},
             "players": {"1": {"code_low": 0, "code_high": 0, "solved": true, "score": 4, "legs_solved": 1},
                         "2": {"code_low": 1, "code_high": 1}}},
   "rules": [{"seat": 2, "options_include": "sum", "times": "all"}, {"seat": 1, "options_include": "edge"}],
   "expect": {"game": {"leg": 2, "turn_in_leg": 2},
              "players": {"1": {"score": 4, "legs_solved": 1, "last_action": "edge"}, "2": {"score": 0, "legs_solved": 0}},
              "offered": [{"seat": 1, "option": "guess 0-0"}]}},

  {"name": "Match ends after turn 6 of leg 4; higher score wins", "rule": "R17", "players": 2,
   "given": {"game": {"leg": 4, "turn_in_leg": 6},
             "players": {"1": {"score": 10, "legs_solved": 2}, "2": {"score": 8, "legs_solved": 3}}},
   "rules": [{"seat": 1, "options_include": "sum", "times": "all"}, {"seat": 2, "options_include": "sum", "times": "all"}],
   "expect": {"winner": 1, "standings": {"1": 102, "2": 83}, "game": {"leg": 5}}},

  {"name": "Equal scores: more legs solved wins", "rule": "R18", "players": 2,
   "given": {"game": {"leg": 4, "turn_in_leg": 6},
             "players": {"1": {"score": 9, "legs_solved": 2}, "2": {"score": 9, "legs_solved": 3}}},
   "rules": [{"seat": 1, "options_include": "sum", "times": "all"}, {"seat": 2, "options_include": "sum", "times": "all"}],
   "expect": {"winner": 2, "standings": {"1": 92, "2": 93}}},

  {"name": "Equal scores and legs solved: shared win", "rule": "R18", "players": 2,
   "given": {"game": {"leg": 4, "turn_in_leg": 6},
             "players": {"1": {"score": 7, "legs_solved": 2}, "2": {"score": 7, "legs_solved": 2}}},
   "rules": [{"seat": 1, "options_include": "sum", "times": "all"}, {"seat": 2, "options_include": "sum", "times": "all"}],
   "expect": {"winner": [1, 2], "standings": {"1": 72, "2": 72}}}
]
````
