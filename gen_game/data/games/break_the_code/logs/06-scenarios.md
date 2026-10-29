# 06 scenarios

- time: 2026-10-27T18:24:18+00:00 (82.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 f8ccd572e0835386, reply sha256 f7623e89020ff709

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
````

## Reply

````
```json
[
  {"name": "Round counter advances by one per round (round 3 -> 4)", "rule": "R1", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 3}, "players": {"1": {"code": 258}, "2": {"code": 136}}},
   "rules": [],
   "expect": {"game": {"round": 4}, "players": {"1": {"score": 0, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "Leg-round of round 3 is 3: a correct guess scores 5-3 = 2", "rule": "R1", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "258"}],
   "expect": {"game": {"round": 3}, "players": {"1": {"score": 2, "wrong_count": 0}, "2": {"score": 0}}}},

  {"name": "Scores carry into a new leg", "rule": "R2", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 4}, "players": {"1": {"score": 6, "wrong_count": 1}, "2": {"score": 3, "wrong_count": 2}}},
   "rules": [],
   "expect": {"game": {"round": 5}, "players": {"1": {"score": 6, "wrong_count": 1}, "2": {"score": 3, "wrong_count": 2}}}},

  {"name": "A new leg starts at round 9 without changing scores", "rule": "R3", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 8}, "players": {"1": {"score": 4}, "2": {"score": 2}}},
   "rules": [],
   "expect": {"game": {"round": 9}, "players": {"1": {"score": 4, "wrong_count": 0}, "2": {"score": 2, "wrong_count": 0}}}},

  {"name": "Stored code 258 is matched by a guess of its digits in another order (5,8,2)", "rule": "R4", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "582"}],
   "expect": {"game": {"round": 3}, "players": {"1": {"score": 2, "wrong_count": 0}}}},

  {"name": "A blank code entry becomes 0-1-2, so guessing 2,0,1 in leg-round 1 scores 4", "rule": "R5", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "rules": [{"seat": 1, "options_include": "pass", "answer": "201"}],
   "expect": {"game": {"round": 1}, "players": {"1": {"score": 4, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "Leg start resets guesses_left, solved and used cards: an exhausted seat may guess again and ask card 1", "rule": "R6", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 4}, "players": {"1": {"guesses_left": 0, "solved": 1, "used_mask": 63}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "345"}],
   "expect": {"game": {"round": 5}, "players": {"1": {"score": -1, "wrong_count": 1}},
              "offered": [{"seat": 1, "option": 1}]}},

  {"name": "A card used this leg is not offered again; the other seat still has it", "rule": "R7", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"used_mask": 1, "code": 136}, "2": {"used_mask": 0, "code": 258}}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"game": {"round": 2},
              "offered": [{"seat": 1, "option": 2}, {"seat": 2, "option": 1}],
              "not_offered": [{"seat": 1, "option": 1}]}},

  {"name": "Already used cards 1-3 are not offered; only 4, 5 and 6 are", "rule": "R8", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"used_mask": 7, "code": 136}, "2": {"used_mask": 3, "code": 258}}},
   "rules": [],
   "expect": {"offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 5}, {"seat": 1, "option": 6}],
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 2}, {"seat": 1, "option": 3}]}},

  {"name": "Card 1 SUM can be asked and costs no points", "rule": "R9", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 1}],
   "expect": {"offered": [{"seat": 1, "option": 1}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Card 2 EVENS can be asked and costs no points", "rule": "R10", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"offered": [{"seat": 1, "option": 2}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Card 3 RANGE can be asked and costs no points", "rule": "R11", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"offered": [{"seat": 1, "option": 3}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Card 4 HIGH can be asked and costs no points", "rule": "R12", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"offered": [{"seat": 1, "option": 4}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Card 5 STEPS can be asked and costs no points", "rule": "R13", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 345}}},
   "rules": [{"seat": 1, "options_include": 5}],
   "expect": {"offered": [{"seat": 1, "option": 5}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Card 6 THREES can be asked and costs no points", "rule": "R14", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 37}}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"offered": [{"seat": 1, "option": 6}], "players": {"1": {"score": 0, "wrong_count": 0}}}},

  {"name": "Both seats ask different cards in the same round with no score change", "rule": "R15", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": 5}],
   "expect": {"offered": [{"seat": 1, "option": 3}, {"seat": 2, "option": 5}],
              "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "A guess written 8,5,2 is sorted to 258 and scores 3 in leg-round 2", "rule": "R16", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "852"}],
   "expect": {"game": {"round": 2}, "players": {"1": {"score": 3, "wrong_count": 0}, "2": {"score": 0}}}},

  {"name": "A seat with no guesses left can only pass and loses nothing", "rule": "R17", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"guesses_left": 0, "score": 3, "wrong_count": 2, "code": 136}, "2": {"code": 258}}},
   "rules": [],
   "expect": {"players": {"1": {"score": 3, "wrong_count": 2}}}},

  {"name": "A seat that already solved can only pass and keeps its score", "rule": "R17", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"solved": 1, "guesses_left": 1, "score": 3, "code": 136}, "2": {"code": 258}}},
   "rules": [],
   "expect": {"players": {"1": {"score": 3, "wrong_count": 0}}}},

  {"name": "Using the last guess leaves none: a later guess attempt counts as a pass", "rule": "R18", "players": 2, "rounds": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"guesses_left": 1, "code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "345"},
             {"seat": 1, "options_include": "pass", "answer": "678"}],
   "expect": {"game": {"round": 4}, "players": {"1": {"score": -1, "wrong_count": 1}}}},

  {"name": "A correct guess in leg-round 4 scores 5-4 = 1", "rule": "R19", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 3}, "players": {"1": {"score": 5, "code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "258"}],
   "expect": {"game": {"round": 4}, "players": {"1": {"score": 6, "wrong_count": 0}}}},

  {"name": "A wrong guess costs 1 point and adds 1 wrong", "rule": "R20", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"score": 2, "wrong_count": 1, "code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "013"}],
   "expect": {"players": {"1": {"score": 1, "wrong_count": 2}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "Both seats guess in the same round: one correct (+3), one wrong (-1)", "rule": "R21", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 1}, "players": {"1": {"code": 136}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": "pass", "answer": "258"},
             {"seat": 2, "options_include": "pass", "answer": "479"}],
   "expect": {"players": {"1": {"score": 3, "wrong_count": 0}, "2": {"score": -1, "wrong_count": 1}}}},

  {"name": "After the opponent solved, the other seat still asks and can solve too", "rule": "R22", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 2}, "players": {"1": {"solved": 1, "score": 4, "code": 136}, "2": {"code": 258, "used_mask": 1}}},
   "rules": [{"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "pass", "answer": "631"}],
   "expect": {"offered": [{"seat": 2, "option": 2}],
              "players": {"1": {"score": 4}, "2": {"score": 2, "wrong_count": 0}}}},

  {"name": "Leg-round 4 reveal leaves scores unchanged", "rule": "R23", "players": 2, "rounds": 1, "seed": 1, "default": "decline",
   "given": {"game": {"round": 3}, "players": {"1": {"score": 3, "code": 136}, "2": {"score": 1, "code": 258}}},
   "rules": [],
   "expect": {"game": {"round": 4}, "players": {"1": {"score": 3}, "2": {"score": 1}}}},

  {"name": "Match ends after round 12: equal scores, fewer wrong guesses wins", "rule": "R24", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"score": 5, "wrong_count": 0, "code": 136}, "2": {"score": 5, "wrong_count": 1, "code": 258}}},
   "rules": [],
   "expect": {"winner": 1, "standings": {"1": 500, "2": 499}, "game": {"round": 12}}},

  {"name": "Correct guess in round 12 (+1) gives the higher score and the win", "rule": "R24", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"score": 3, "wrong_count": 0, "code": 136}, "2": {"score": 3, "wrong_count": 0, "code": 258}}},
   "rules": [{"seat": 2, "options_include": "pass", "answer": "136"}],
   "expect": {"winner": 2, "standings": {"1": 300, "2": 400}, "players": {"2": {"score": 4}}}},

  {"name": "Equal score and equal wrong guesses share the win", "rule": "R24", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"score": 4, "wrong_count": 1, "code": 136}, "2": {"score": 4, "wrong_count": 1, "code": 258}}},
   "rules": [],
   "expect": {"winner": [1, 2], "standings": {"1": 399, "2": 399}}}
]
```
````
