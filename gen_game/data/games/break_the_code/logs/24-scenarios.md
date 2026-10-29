# 24 scenarios

- time: 2026-10-27T18:54:03+00:00 (83.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 ed053d644b7dce88, reply sha256 5e13dfcd585689ef

## Sent

````
SPEC:
{
  "name": "Break the Code: Three-Leg Duel",
  "summary": "Two players each hide a three-digit code. Over three legs of four rounds they ask the same number-question cards at the same time and score points for cracking the opponent's code early.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "legs": 3,
    "rounds_per_leg": 4,
    "total_rounds": 12,
    "digit_min": 0,
    "digit_max": 9,
    "code_length": 3,
    "default_code": 12,
    "question_cards": 6,
    "cards_used_per_leg": 4,
    "guesses_per_leg": 2,
    "correct_score_base": 5,
    "wrong_guess_penalty": 1,
    "high_digit_threshold": 5,
    "pass_value": 0,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total points across all legs.",
        "observable": true
      },
      {
        "key": "wrong_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wrong guesses over the whole match; used as the tie-break (fewer is better).",
        "observable": true
      },
      {
        "key": "guesses_left",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Valid guesses still allowed in this leg; reset to 2 at leg-round 1.",
        "observable": false
      },
      {
        "key": "solved",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if the player has guessed the opponent's code correctly this leg, else 0.",
        "observable": false
      },
      {
        "key": "used_mask",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bitmask of cards used this leg. Card n is used if floor(used_mask / 2^(n-1)) mod 2 = 1.",
        "observable": false
      },
      {
        "key": "code",
        "type": "number",
        "visible": "ally",
        "initial": 12,
        "meaning": "The player's secret code for this leg, written as 100A+10B+C with A<B<C. The opponent never sees it until the leg ends.",
        "observable": false
      },
      {
        "key": "ask",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The card (1-6) the player asked this round.",
        "observable": false
      },
      {
        "key": "answer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The value of the asked card, computed from the opponent's code.",
        "observable": false
      },
      {
        "key": "guess",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This round's guess as 100A+10B+C, or 0 for a pass.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round, 1-12. Leg-round = ((round - 1) mod 4) + 1.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat two players.",
    "Set every player's score and wrong_count to 0.",
    "Set round to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. Leg-round L = ((round - 1) mod 4) + 1."
    },
    {
      "action": "poll",
      "who": "all players (only when L = 1, i.e. rounds 1, 5, 9)",
      "answer": "short text: three different digits 0-9 in any order",
      "effect": "Three different digits are sorted ascending and stored as code = 100A+10B+C. Any other entry sets code = 12 (0-1-2). Then guesses_left = 2, solved = 0, used_mask = 0. Each player's code is visible only to its owner."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player receives their own state: code, guesses_left, solved, used_mask, score."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "choice of one card number from 1-6 not yet used this leg",
      "effect": "ask = the chosen card. If the answer is missing or invalid, ask = the lowest card n with floor(used_mask/2^(n-1)) mod 2 = 0. Then used_mask += 2^(ask-1)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, with the opponent's code digits A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10: answer = A+B+C if ask=1; count of digits with d mod 2 = 0 if ask=2; C-A if ask=3; count of digits >= 5 if ask=4; (B-A=1)+(C-B=1) if ask=5; count of digits with d mod 3 = 0 if ask=6. Announce to both players each player's ask and answer."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text: 'pass' or three different digits 0-9 in any order",
      "effect": "If the entry is three different digits AND guesses_left > 0 AND solved = 0, guess = the sorted code as 100A+10B+C and guesses_left -= 1. Otherwise guess = 0 (a pass)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with guess > 0: if guess = opponent's code, score += 5 - L and solved = 1; otherwise score -= 1 and wrong_count += 1. Announce every guess and its result (correct or wrong) to both players."
    },
    {
      "action": "tell",
      "who": "all players (only when L = 4, i.e. rounds 4, 8, 12)",
      "answer": null,
      "effect": "Reveal both players' code to both players and announce the current score of each player."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 12, end the game; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score * 100 - you.wrong_count",
    "decided_by": "Highest total score wins. If scores are equal, the player with fewer wrong guesses over the match wins. If both are equal, both share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The match has 12 rounds in 3 legs of 4 rounds each; leg-round = ((round - 1) mod 4) + 1."
    },
    {
      "id": "R2",
      "text": "Scores start at 0 and carry across legs."
    },
    {
      "id": "R3",
      "text": "When leg-round is 1 (rounds 1, 5, 9), both players secretly and simultaneously write a code."
    },
    {
      "id": "R4",
      "text": "When a code entry has three different digits in any order (e.g. 8,2,5), then it is sorted ascending and stored as code 258."
    },
    {
      "id": "R5",
      "text": "When a code entry is invalid (repeated digits, wrong count, non-digits, blank), then the code becomes 0-1-2 (code = 12)."
    },
    {
      "id": "R6",
      "text": "When a leg starts, each player's guesses_left is set to 2, solved to 0 and used_mask to 0."
    },
    {
      "id": "R7",
      "text": "Each round, both players simultaneously name one card 1-6 not used this leg; that card becomes used until the leg ends."
    },
    {
      "id": "R8",
      "text": "When a player names nothing, an invalid number or an already used card, then they are given the lowest-numbered unused card."
    },
    {
      "id": "R9",
      "text": "Card 1 SUM answers A+B+C of the opponent's code (e.g. 2-5-8 gives 15)."
    },
    {
      "id": "R10",
      "text": "Card 2 EVENS answers how many of the opponent's digits are even, with 0 counting as even (e.g. 2-5-8 gives 2)."
    },
    {
      "id": "R11",
      "text": "Card 3 RANGE answers C-A (e.g. 2-5-8 gives 6)."
    },
    {
      "id": "R12",
      "text": "Card 4 HIGH answers how many digits are 5 or more (e.g. 2-5-8 gives 2)."
    },
    {
      "id": "R13",
      "text": "Card 5 STEPS answers how many of the pairs (A,B), (B,C) differ by exactly 1 (e.g. 3-4-5 gives 2, 2-5-8 gives 0)."
    },
    {
      "id": "R14",
      "text": "Card 6 THREES answers how many digits are in {0,3,6,9} (e.g. 0-3-7 gives 2)."
    },
    {
      "id": "R15",
      "text": "After asking, the engine announces to both players which card each player asked and its answer."
    },
    {
      "id": "R16",
      "text": "Each round, both players simultaneously pass or write a guess; a guess of three different digits is sorted ascending."
    },
    {
      "id": "R17",
      "text": "When a guess entry is not three different digits, or the guesser has guesses_left = 0, or solved = 1, then it counts as a pass and costs nothing."
    },
    {
      "id": "R18",
      "text": "When a valid guess is made, then the guesser's guesses_left decreases by 1."
    },
    {
      "id": "R19",
      "text": "When a valid guess equals the opponent's code, then the guesser scores 5 - leg-round (4, 3, 2, 1 in leg-rounds 1-4) and solved = 1 for the rest of the leg."
    },
    {
      "id": "R20",
      "text": "When a valid guess does not equal the opponent's code, then the guesser loses 1 point and wrong_count increases by 1."
    },
    {
      "id": "R21",
      "text": "Every guess and its result (correct or wrong) is announced to both players."
    },
    {
      "id": "R22",
      "text": "When one player guesses correctly, the other player still keeps asking and guessing in that leg."
    },
    {
      "id": "R23",
      "text": "When leg-round is 4 (rounds 4, 8, 12), both codes are revealed to both players and the scores are announced."
    },
    {
      "id": "R24",
      "text": "When round 12 is finished, the match ends; the higher score wins, then fewer wrong guesses, else a draw."
    }
  ],
  "offers": [
    {
      "question": "Code choice (leg-round 1 only)",
      "who": "both seats",
      "options": "free short text; three different digits are expected, and anything else becomes 0-1-2"
    },
    {
      "question": "Ask a card",
      "who": "both seats",
      "options": "each card number 1-6 that seat has not used this leg (4 options in leg-round 2, 3 in leg-round 3, the remaining 3 in leg-round 4 as cards run down: 6, 5, 4, 3 options in leg-rounds 1-4)"
    },
    {
      "question": "Guess",
      "who": "both seats",
      "options": "a seat with guesses_left > 0 and solved = 0: 'pass' or a three-digit code in free text; a seat with guesses_left = 0 or solved = 1: pass only"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the table at 2. It is a head-to-head deduction duel in which each player reads one opponent's code. With 3 or more there is no single opponent to question."
    },
    {
      "what": "No talk step",
      "why": "The source has no talk. With two rivals racing to deduce, words would add nothing the rules use."
    },
    {
      "what": "Codes are visible to their owner (ally)",
      "why": "The source says only the engine knows the codes. The owner wrote their own code, and a player attribute cannot be fully hidden, so the opponent simply never sees it."
    },
    {
      "what": "Tie-break expression score*100 - wrong_count",
      "why": "wrong_count is at most 6, so the score always dominates and fewer wrong guesses breaks ties. Players who are equal on both share the win, which is the draw."
    },
    {
      "what": "guesses_left, solved, used_mask, ask, answer and guess made public",
      "why": "The rules announce each ask, answer, guess and result to both players, so this state is common knowledge."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player picks cards that split the remaining codes best and weighs guessing early for more points against the 1-point penalty and the limit of 2 guesses."
    }
  ],
  "simplifications": [
    {
      "what": "Opponent's code is referenced inside a player's update",
      "why": "The engine has no direct player-attribute operand. With exactly 2 seats, 'opponent' is the other seat, and a table-mirror workaround may be used for the comparison."
    },
    {
      "what": "Steps 1 and 6 run every round but act only when their leg-round condition holds",
      "why": "The step list is flat; the per-step `when` conditions express 'leg-round 1 only' and 'leg-round 4 only'."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, wrong_count; table: round.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the 'last guess leaves none' scenario so it checks only observable results. Set up Ada with guesses_left 1, let her make one wrong guess, then attempt another guess in a later round. Assert that her score dropped by exactly 1 and her wrong_count rose by exactly 1 in total, with no further penalty from the second attempt. Do not require the game to put a guess or pass option to a seat with 0 guesses left or a solved flag; make any rule for that seat optional, or drop it. Do not assert on guesses_left, used_mask or other internal bookkeeping; assert only on score, wrong_count and round.
````

## Reply

````
```json
[
  {
    "name": "Setup: scores, wrong counts and round all start at 0",
    "rule": "R2",
    "players": 2,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 0}
    }
  },
  {
    "name": "Scores carry into a new leg (round 5 starts leg 2, score stays)",
    "rule": "R2",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"score": 3, "wrong_count": 1},
        "2": {"score": 2, "wrong_count": 0}
      },
      "game": {"round": 4}
    },
    "expect": {
      "players": {
        "1": {"score": 3, "wrong_count": 1},
        "2": {"score": 2, "wrong_count": 0}
      },
      "game": {"round": 5}
    }
  },
  {
    "name": "Full match with nobody guessing lasts 12 rounds and ends in a shared win",
    "rule": "R1",
    "players": 2,
    "default": "decline",
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 0, "2": 0},
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 12}
    }
  },
  {
    "name": "Codes are written in round 1; a correct guess in leg-round 1 scores 4",
    "rule": "R3",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "147"},
      {"seat": 1, "options_include": "258"},
      {"seat": 2, "options_include": "258"}
    ],
    "expect": {
      "players": {
        "1": {"score": 4, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 1}
    }
  },
  {
    "name": "Code entry 852 is stored sorted as 258, so a guess of 258 is correct",
    "rule": "R4",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "147"},
      {"seat": 1, "options_include": "258"},
      {"seat": 2, "options_include": "852"}
    ],
    "expect": {
      "players": {
        "1": {"score": 4, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      }
    }
  },
  {
    "name": "Repeated-digit code entry becomes 0-1-2, so a guess of 012 is correct",
    "rule": "R5",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "147"},
      {"seat": 1, "options_include": "012"},
      {"seat": 2, "options_include": "112"}
    ],
    "expect": {
      "players": {
        "1": {"score": 4, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      }
    }
  },
  {
    "name": "New leg resets solved and guesses, so a previously solved seat can score again in round 5",
    "rule": "R6",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"score": 3, "solved": 1, "guesses_left": 0},
        "2": {"score": 0}
      },
      "game": {"round": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "147"},
      {"seat": 1, "options_include": "369"},
      {"seat": 2, "options_include": "369"}
    ],
    "expect": {
      "players": {
        "1": {"score": 7, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 5}
    }
  },
  {
    "name": "A card already used this leg is not offered again",
    "rule": "R7",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"used_mask": 4, "code": 147},
        "2": {"used_mask": 0, "code": 258}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 1}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": 1},
        {"seat": 1, "option": 2}
      ],
      "not_offered": [
        {"seat": 1, "option": 3}
      ],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Unscripted card choice: used card 1 not offered, remaining cards offered, no score change",
    "rule": "R8",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"used_mask": 1, "code": 147},
        "2": {"used_mask": 0, "code": 258}
      },
      "game": {"round": 1}
    },
    "expect": {
      "offered": [
        {"seat": 1, "option": 2}
      ],
      "not_offered": [
        {"seat": 1, "option": 1}
      ],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 1 SUM is allowed and costs nothing (answer not observable)",
    "rule": "R9",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 258, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 1}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 1}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 2 EVENS is allowed and costs nothing (answer not observable)",
    "rule": "R10",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 258, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 2}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 2}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 3 RANGE is allowed and costs nothing (answer not observable)",
    "rule": "R11",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 258, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 3}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 3}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 4 HIGH is allowed and costs nothing (answer not observable)",
    "rule": "R12",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 258, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 4}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 4}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 5 STEPS is allowed and costs nothing (answer not observable)",
    "rule": "R13",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 345, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 5}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 5}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Asking card 6 THREES is allowed and costs nothing (answer not observable)",
    "rule": "R14",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 37, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 6}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 6}],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Both seats ask a card in the same round; asking alone changes no score",
    "rule": "R15",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "used_mask": 0},
        "2": {"code": 258, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 1}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": 4},
        {"seat": 2, "option": 1}
      ],
      "players": {
        "1": {"score": 0, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Guess 852 is sorted to 258 and matches in leg-round 3 for 2 points",
    "rule": "R16",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "guesses_left": 2, "solved": 0, "used_mask": 0},
        "2": {"code": 258, "guesses_left": 2, "solved": 0, "used_mask": 0}
      },
      "game": {"round": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "852"}
    ],
    "expect": {
      "players": {
        "1": {"score": 2, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 3}
    }
  },
  {
    "name": "A seat that already solved the leg gets no further score change",
    "rule": "R17",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 4, "guesses_left": 1, "solved": 1, "used_mask": 0},
        "2": {"code": 258, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "expect": {
      "players": {
        "1": {"score": 4, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Last guess leaves none: one wrong guess costs 1, a later attempt costs nothing more",
    "rule": "R18",
    "players": 2,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 3, "wrong_count": 0, "guesses_left": 1, "solved": 0, "used_mask": 0},
        "2": {"code": 258, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "369", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"score": 2, "wrong_count": 1},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 3}
    }
  },
  {
    "name": "A correct guess in leg-round 4 scores 1",
    "rule": "R19",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 2, "guesses_left": 2, "solved": 0, "used_mask": 7},
        "2": {"code": 258, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 7}
      },
      "game": {"round": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "258"}
    ],
    "expect": {
      "players": {
        "1": {"score": 3, "wrong_count": 0},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 4}
    }
  },
  {
    "name": "A wrong guess costs 1 point and adds 1 wrong guess",
    "rule": "R20",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 5, "wrong_count": 0, "guesses_left": 2, "solved": 0, "used_mask": 0},
        "2": {"code": 258, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "259"}
    ],
    "expect": {
      "players": {
        "1": {"score": 4, "wrong_count": 1},
        "2": {"score": 0, "wrong_count": 0}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "Simultaneous guesses: one correct (+3 in leg-round 2), one wrong (-1)",
    "rule": "R21",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 0},
        "2": {"code": 258, "score": 2, "guesses_left": 2, "solved": 0, "used_mask": 0}
      },
      "game": {"round": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "258"},
      {"seat": 2, "options_include": "148"}
    ],
    "expect": {
      "players": {
        "1": {"score": 3, "wrong_count": 0},
        "2": {"score": 1, "wrong_count": 1}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "After the opponent solved, the other seat still asks and can score (+2 in leg-round 3)",
    "rule": "R22",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 3, "guesses_left": 1, "solved": 1, "used_mask": 1},
        "2": {"code": 258, "score": 0, "guesses_left": 2, "solved": 0, "used_mask": 1}
      },
      "game": {"round": 2}
    },
    "rules": [
      {"seat": 2, "options_include": 2},
      {"seat": 2, "options_include": "741"}
    ],
    "expect": {
      "offered": [{"seat": 2, "option": 2}],
      "players": {
        "1": {"score": 3, "wrong_count": 0},
        "2": {"score": 2, "wrong_count": 0}
      },
      "game": {"round": 3}
    }
  },
  {
    "name": "Leg-round 4 reveal leaves scores unchanged and the round reaches 4",
    "rule": "R23",
    "players": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 2, "wrong_count": 1, "guesses_left": 1, "solved": 0, "used_mask": 7},
        "2": {"code": 258, "score": 3, "wrong_count": 0, "guesses_left": 1, "solved": 1, "used_mask": 7}
      },
      "game": {"round": 3}
    },
    "expect": {
      "players": {
        "1": {"score": 2, "wrong_count": 1},
        "2": {"score": 3, "wrong_count": 0}
      },
      "game": {"round": 4}
    }
  },
  {
    "name": "Match ends after round 12: higher score wins",
    "rule": "R24",
    "players": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 10, "wrong_count": 2, "guesses_left": 2, "solved": 0, "used_mask": 7},
        "2": {"code": 258, "score": 8, "wrong_count": 0, "guesses_left": 2, "solved": 0, "used_mask": 7}
      },
      "game": {"round": 11}
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 998, "2": 800},
      "players": {
        "1": {"score": 10, "wrong_count": 2},
        "2": {"score": 8, "wrong_count": 0}
      },
      "game": {"round": 12}
    }
  },
  {
    "name": "Match end tie on score: fewer wrong guesses wins",
    "rule": "R24",
    "players": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 6, "wrong_count": 1, "guesses_left": 2, "solved": 0, "used_mask": 7},
        "2": {"code": 258, "score": 6, "wrong_count": 2, "guesses_left": 2, "solved": 0, "used_mask": 7}
      },
      "game": {"round": 11}
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 599, "2": 598},
      "players": {
        "1": {"score": 6, "wrong_count": 1},
        "2": {"score": 6, "wrong_count": 2}
      }
    }
  },
  {
    "name": "Match end with equal score and equal wrong guesses is a shared win",
    "rule": "R24",
    "players": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"code": 147, "score": 5, "wrong_count": 1, "guesses_left": 2, "solved": 0, "used_mask": 7},
        "2": {"code": 258, "score": 5, "wrong_count": 1, "guesses_left": 2, "solved": 0, "used_mask": 7}
      },
      "game": {"round": 11}
    },
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 499, "2": 499},
      "game": {"round": 12}
    }
  }
]
```
````
