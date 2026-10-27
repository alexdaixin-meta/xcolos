# 33 scenarios

- time: 2026-10-27T19:03:24+00:00 (83.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 19f5ba410c6bf930, reply sha256 34faba492f61f6f2

## Sent

````
SPEC:
{
  "name": "Break the Code: Coarse Clues",
  "summary": "Two players each hide a three-digit code of distinct digits, ask coarse clue cards about the opponent's code, and try to guess it early in a 4-round leg, over 3 legs.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "total_rounds": 12,
    "legs": 3,
    "rounds_per_leg": 4,
    "leg_start_1": 1,
    "leg_start_2": 5,
    "leg_start_3": 9,
    "guesses_per_leg": 2,
    "code_min": 0,
    "code_max": 999,
    "invalid_code_default": 12,
    "card_min": 1,
    "card_max": 6,
    "high_threshold": 5,
    "correct_score_base": 5,
    "wrong_guess_penalty": -1,
    "owner_bonus_on_wrong_guess": 1,
    "unsolved_leg_bonus": 1,
    "initial_score": 0,
    "initial_wrong_count": 0,
    "rank_score_weight": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total score, carried over between legs",
        "observable": true
      },
      {
        "key": "wrong_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of wrong guesses over the match. It is the tie-break, and fewer is better",
        "observable": true
      },
      {
        "key": "code",
        "type": "number",
        "visible": "ally",
        "initial": 12,
        "meaning": "Own stored code: sorted distinct digits stored as 100a+10b+c",
        "observable": false
      },
      {
        "key": "revealed_code",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Copy of code made public at the end of each leg; -1 means not yet revealed",
        "observable": true
      },
      {
        "key": "guesses_left",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Wrong guesses still allowed in this leg",
        "observable": false
      },
      {
        "key": "solved",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 once this player has correctly guessed the opponent's code in this leg",
        "observable": false
      },
      {
        "key": "card_asked",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card asked this round, 1-6; 0 means none. Announced after both players have asked",
        "observable": false
      },
      {
        "key": "answer",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "Private answer to this round's card about the opponent's code; -1 means no question",
        "observable": false
      },
      {
        "key": "guess",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "This round's parsed guess of the opponent's code; -1 means pass",
        "observable": false
      },
      {
        "key": "result",
        "type": "text",
        "visible": "public",
        "initial": "pass",
        "meaning": "This round's guess outcome: pass, right or wrong",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Round counter; increases by exactly 1 at the start of each round",
        "observable": true
      },
      {
        "key": "leg_round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "((round - 1) mod 4) + 1, running 1 to 4 within each leg",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 and seat 2 sit down; each seat's opponent is the other seat.",
    "Each player's score and wrong_count are set to 0. Each player's code is set to 12, revealed_code to -1, guesses_left to 2 and solved to 0.",
    "The table's round is set to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; leg_round = ((round - 1) mod 4) + 1; for each player, card_asked = 0, answer = -1, guess = -1 and result = 'pass'."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When leg_round == 1: for each player, guesses_left = 2, solved = 0 and revealed_code = -1."
    },
    {
      "action": "poll",
      "who": "all players (only when leg_round == 1)",
      "answer": "a whole number from 0 to 999, or decline",
      "effect": "Each player's entry x is parsed into A = floor(x/100), B = floor(x/10) mod 10 and C = x mod 10. If A, B and C are all different, they are sorted ascending as a<b<c and code = 100a+10b+c. Otherwise, or if the player declines, code = 12. Neither player sees the other's entry."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a card number from 1 to 6, or decline",
      "effect": "card_asked = the chosen card, or 0 if the player declines. Answers stay hidden until both are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with card_asked > 0, using the opponent's code digits a<b<c: card 1 gives the count of digits >= 5; card 2 the count of odd digits; card 3 the count of digits in {2,3,5,7}; card 4 the count of digits in {0,3,6,9}; card 5 gives (1 if b-a == 1 else 0) + (1 if c-b == 1 else 0); card 6 gives (a+b+c) mod 4. The result goes into that player's answer (ally, seen only by the asker)."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own answer."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce 'Seat 1 asked card {card_asked of seat 1}; Seat 2 asked card {card_asked of seat 2}', where 0 means no question."
    },
    {
      "action": "poll",
      "who": "each player with guesses_left > 0 and solved == 0",
      "answer": "a whole number from 0 to 999 as a guess of the opponent's code, or pass",
      "effect": "The entry is parsed as for codes. If its three digits are all different, guess = the sorted value; otherwise, or on a pass, guess = -1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Applied to each player separately, using the guesses as entered. If guess == -1: result = 'pass'. If guess == the opponent's code: score += 5 - leg_round, solved = 1 and result = 'right'. If guess >= 0 and guess != the opponent's code: score -= 1, wrong_count += 1, guesses_left -= 1, result = 'wrong', and the opponent's score += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce 'Seat 1: {result of seat 1}; Seat 2: {result of seat 2}'. Codes are not shown."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When leg_round == 4: each player whose opponent's solved == 0 gets score += 1. Then, for each player, revealed_code = code."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When leg_round == 4, announce 'Codes this leg: Seat 1 {revealed_code of seat 1}, Seat 2 {revealed_code of seat 2}'."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round >= 12, end the game; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score * 100 - you.wrong_count",
    "decided_by": "The higher total score wins. If the scores are level, the player with fewer wrong guesses wins. If both are level, the two players share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a round starts, round increases by exactly 1 and leg_round = ((round - 1) mod 4) + 1, so rounds 1, 5 and 9 have leg_round 1 and rounds 4, 8 and 12 have leg_round 4."
    },
    {
      "id": "R2",
      "text": "When the game starts, each player's score is 0 and wrong_count is 0, and neither is reset between legs."
    },
    {
      "id": "R3",
      "text": "When leg_round is 1, each player's guesses_left is set to 2 and solved to 0 before codes are entered."
    },
    {
      "id": "R4",
      "text": "When leg_round is 1, both players are polled at the same time for a code; when leg_round is 2, 3 or 4, no code is asked for and codes stay unchanged."
    },
    {
      "id": "R5",
      "text": "When a player enters 852 as a code, code is stored as 258; when a player enters 12, code is stored as 12."
    },
    {
      "id": "R6",
      "text": "When a code entry has repeated digits (for example 447) or is declined, code is stored as 12."
    },
    {
      "id": "R7",
      "text": "When a player asks card 1 and the opponent's code is 258, answer is 2 (digits 5 and 8 are 5 or higher)."
    },
    {
      "id": "R8",
      "text": "When a player asks card 2 and the opponent's code is 258, answer is 1 (the count of odd digits)."
    },
    {
      "id": "R9",
      "text": "When a player asks card 3 and the opponent's code is 258, answer is 2 (the count of digits in 2, 3, 5, 7)."
    },
    {
      "id": "R10",
      "text": "When a player asks card 4 and the opponent's code is 369, answer is 3 (the count of digits in 0, 3, 6, 9)."
    },
    {
      "id": "R11",
      "text": "When a player asks card 5 and the opponent's code is 123, answer is 2; when the code is 258, answer is 0."
    },
    {
      "id": "R12",
      "text": "When a player asks card 6 and the opponent's code is 258, answer is 3 ((2+5+8) mod 4)."
    },
    {
      "id": "R13",
      "text": "When a player declines to ask, card_asked is 0 and no answer is given; asking the same card again gives the same answer."
    },
    {
      "id": "R14",
      "text": "After asking, the answer is shown only to the asker, and both players are told which card each player asked."
    },
    {
      "id": "R15",
      "text": "When a player's guesses_left is 0 or solved is 1, that player is not asked for a guess."
    },
    {
      "id": "R16",
      "text": "When a guess is declined or has repeated digits, it is a pass, and score, wrong_count and guesses_left are unchanged."
    },
    {
      "id": "R17",
      "text": "When a valid guess equals the opponent's code, the guesser scores 5 - leg_round (4, 3, 2 or 1 in leg-rounds 1 to 4) and solved becomes 1."
    },
    {
      "id": "R18",
      "text": "When a valid guess does not equal the opponent's code, the guesser's score decreases by 1, wrong_count increases by 1, guesses_left decreases by 1, and the opponent's score increases by 1."
    },
    {
      "id": "R19",
      "text": "When both players guess correctly in the same round, both score 5 - leg_round."
    },
    {
      "id": "R20",
      "text": "After guessing, both players are told whether each player passed, guessed right or guessed wrong, and codes are not shown."
    },
    {
      "id": "R21",
      "text": "When leg_round is 4, each player whose opponent's solved is 0 scores +1, and then both codes are revealed to both players."
    },
    {
      "id": "R22",
      "text": "When round 12 has finished, the game ends; the higher score wins, a level score is broken by the lower wrong_count, and a full tie is a draw."
    }
  ],
  "offers": [
    {
      "question": "Enter your secret code (only when leg_round is 1)",
      "who": "both seats",
      "options": "any whole number from 0 to 999, or decline"
    },
    {
      "question": "Pick a card to ask about the opponent's code",
      "who": "both seats, every round",
      "options": "card 1 (High), 2 (Odd), 3 (Prime), 4 (Threes), 5 (Chain), 6 (Sum mod 4), or decline"
    },
    {
      "question": "Guess the opponent's code",
      "who": "each seat with guesses_left > 0 and solved == 0; a seat with guesses_left 0 or solved 1 is not asked",
      "options": "any whole number from 0 to 999, or pass"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the game at 2. Each player attacks the single opponent's code, and owner bonuses refer to that one opponent."
    },
    {
      "what": "No talk step",
      "why": "The rules contain no table talk. With two players racing to deduce each other's codes, talk would add nothing the rules want."
    },
    {
      "what": "Rank by score*100 - wrong_count",
      "why": "Wrong guesses are at most 6 per match, so score dominates and fewer wrong guesses breaks ties. Players level on both share the win, which is the draw."
    },
    {
      "what": "Leg starts listed as leg_start_1, leg_start_2 and leg_start_3",
      "why": "Each parameter must be a single number."
    },
    {
      "what": "guesses_left, solved and card_asked are public",
      "why": "The rules announce each player's card and guess results, so both players can infer these values anyway."
    },
    {
      "what": "A revealed_code attribute copies the code at the end of each leg",
      "why": "This gives the R9 reveal a stated piece of public state, while the live code stays private during play."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player picks the cards that split the remaining candidate codes most evenly. They also weigh an early guess, which is worth more points, against the -1 penalty plus +1 to the opponent for a wrong guess."
    }
  ],
  "simplifications": [
    {
      "what": "Code and guess entries are taken as a whole number from 0 to 999 or a decline, rather than as free text",
      "why": "The engine's number answer has a range, so out-of-range and non-numeric entries cannot occur. Declining covers the 'missing' case, which still maps to code 12 or a pass as the rules require."
    },
    {
      "what": "Invalid card numbers are reduced to the decline option",
      "why": "The choice list offers only cards 1 to 6 or decline. Declining has the same effect as the rules' invalid entry: no question."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, wrong_count, revealed_code; table: round.
````

## Reply

````
```json
[
  {"name": "R1 first round sets round to 1", "rule": "R1", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"game": {"round": 1}, "players": {"1": {"score": 0, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "R1 round 5 is leg_round 1 so revealed codes reset to -1", "rule": "R1", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 4}, "players": {"1": {"revealed_code": 258}, "2": {"revealed_code": 369}}},
   "rules": [],
   "expect": {"game": {"round": 5}, "players": {"1": {"revealed_code": -1}, "2": {"revealed_code": -1}}}},

  {"name": "R2 initial score, wrong_count and revealed_code", "rule": "R2", "players": 2, "seed": 1, "default": "decline", "rounds": 0,
   "expect": {"game": {"round": 0}, "players": {"1": {"score": 0, "wrong_count": 0, "revealed_code": -1}, "2": {"score": 0, "wrong_count": 0, "revealed_code": -1}}}},

  {"name": "R2 score and wrong_count are not reset at a new leg", "rule": "R2", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 4}, "players": {"1": {"score": 3, "wrong_count": 1}, "2": {"score": 2, "wrong_count": 0}}},
   "rules": [],
   "expect": {"game": {"round": 5}, "players": {"1": {"score": 3, "wrong_count": 1}, "2": {"score": 2, "wrong_count": 0}}}},

  {"name": "R3 guesses_left and solved reset at leg start so both may guess and score 4", "rule": "R3", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 4}, "players": {"1": {"guesses_left": 0, "score": 0}, "2": {"solved": 1, "score": 0}}},
   "rules": [{"seat": 1, "options_include": 12, "times": 2},
             {"seat": 2, "options_include": 12, "times": 2}],
   "expect": {"game": {"round": 5}, "players": {"1": {"score": 4, "wrong_count": 0}, "2": {"score": 4, "wrong_count": 0}}}},

  {"name": "R4 codes stay unchanged in leg_round 2 so correct guesses score 3", "rule": "R4", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258}, "2": {"code": 369}}},
   "rules": [{"seat": 1, "options_include": 369}, {"seat": 2, "options_include": 258}],
   "expect": {"game": {"round": 2}, "players": {"1": {"score": 3, "wrong_count": 0}, "2": {"score": 3, "wrong_count": 0}}}},

  {"name": "R5 entries 852 and 12 are stored as 258 and 12, so guesses of them are right", "rule": "R5", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": 852}, {"seat": 1, "options_include": 12},
             {"seat": 2, "options_include": 12}, {"seat": 2, "options_include": 258}],
   "expect": {"game": {"round": 1}, "players": {"1": {"score": 4, "wrong_count": 0}, "2": {"score": 4, "wrong_count": 0}}}},

  {"name": "R5 entries 852 and 12 are revealed as 258 and 12 after the leg", "rule": "R5", "players": 2, "seed": 1, "default": "decline", "rounds": 4,
   "rules": [{"seat": 1, "options_include": 852}, {"seat": 2, "options_include": 12}],
   "expect": {"game": {"round": 4}, "players": {"1": {"revealed_code": 258, "score": 1}, "2": {"revealed_code": 12, "score": 1}}}},

  {"name": "R6 repeated digits and a declined entry both store code 12", "rule": "R6", "players": 2, "seed": 1, "default": "decline", "rounds": 4,
   "rules": [{"seat": 1, "options_include": 447}],
   "expect": {"game": {"round": 4}, "players": {"1": {"revealed_code": 12, "score": 1}, "2": {"revealed_code": 12, "score": 1}}}},

  {"name": "R7 asking card 1 is offered and changes no score (answer is private)", "rule": "R7", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 1}],
   "expect": {"offered": [{"seat": 1, "option": 1}], "players": {"1": {"score": 0, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "R8 asking card 2 is offered and changes no score (answer is private)", "rule": "R8", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"offered": [{"seat": 1, "option": 2}], "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "R9 asking card 3 is offered and changes no score (answer is private)", "rule": "R9", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 3}],
   "expect": {"offered": [{"seat": 1, "option": 3}], "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "R10 asking card 4 is offered and changes no score (answer is private)", "rule": "R10", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258}, "2": {"code": 369}}},
   "rules": [{"seat": 1, "options_include": 4}],
   "expect": {"offered": [{"seat": 1, "option": 4}], "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "R11 both seats ask card 5 and no score changes (answers are private)", "rule": "R11", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258}, "2": {"code": 123}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 5}],
   "expect": {"offered": [{"seat": 1, "option": 5}, {"seat": 2, "option": 5}], "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "R12 asking card 6 is offered and changes no score (answer is private)", "rule": "R12", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 6}],
   "expect": {"offered": [{"seat": 1, "option": 6}], "players": {"1": {"score": 0}, "2": {"score": 0}}}},

  {"name": "R13 declining a card changes nothing observable", "rule": "R13", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [],
   "expect": {"game": {"round": 2}, "players": {"1": {"score": 0, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "R14 both seats ask cards; no score changes and codes stay hidden", "rule": "R14", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 369}, "2": {"code": 258}}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 6}],
   "expect": {"players": {"1": {"score": 0, "revealed_code": -1}, "2": {"score": 0, "revealed_code": -1}}}},

  {"name": "R15 seat with no guesses left and seat already solved are not asked to guess", "rule": "R15", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258, "guesses_left": 0, "score": 2}, "2": {"code": 369, "solved": 1, "score": 3}}},
   "rules": [],
   "expect": {"not_offered": [{"seat": 1, "option": 500}, {"seat": 2, "option": 500}],
              "players": {"1": {"score": 2, "wrong_count": 0}, "2": {"score": 3, "wrong_count": 0}}}},

  {"name": "R16 a guess with repeated digits is a pass", "rule": "R16", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258}, "2": {"code": 369}}},
   "rules": [{"seat": 1, "options_include": 447}],
   "expect": {"players": {"1": {"score": 0, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "R17 correct guess 852 against code 258 in leg_round 3 scores 2", "rule": "R17", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 2}, "players": {"1": {"code": 369, "score": 1}, "2": {"code": 258, "score": 0}}},
   "rules": [{"seat": 1, "options_include": 852}],
   "expect": {"game": {"round": 3}, "players": {"1": {"score": 3, "wrong_count": 0}, "2": {"score": 0, "wrong_count": 0}}}},

  {"name": "R18 wrong guess costs the guesser 1 and gives the opponent 1", "rule": "R18", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258, "score": 2}, "2": {"code": 369, "score": 2}}},
   "rules": [{"seat": 1, "options_include": 147}],
   "expect": {"players": {"1": {"score": 1, "wrong_count": 1}, "2": {"score": 3, "wrong_count": 0}}}},

  {"name": "R19 both guess right in leg_round 3 and both score 2", "rule": "R19", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 2}, "players": {"1": {"code": 258}, "2": {"code": 369}}},
   "rules": [{"seat": 1, "options_include": 369}, {"seat": 2, "options_include": 258}],
   "expect": {"players": {"1": {"score": 2, "wrong_count": 0}, "2": {"score": 2, "wrong_count": 0}}}},

  {"name": "R20 one right and one wrong guess; codes not revealed", "rule": "R20", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 1}, "players": {"1": {"code": 258}, "2": {"code": 369}}},
   "rules": [{"seat": 1, "options_include": 369}, {"seat": 2, "options_include": 147}],
   "expect": {"players": {"1": {"score": 4, "wrong_count": 0, "revealed_code": -1}, "2": {"score": -1, "wrong_count": 1, "revealed_code": -1}}}},

  {"name": "R21 leg end: unsolved-opponent bonus and codes revealed", "rule": "R21", "players": 2, "seed": 1, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 3}, "players": {"1": {"code": 258, "solved": 1, "score": 3}, "2": {"code": 369, "solved": 0, "score": 0}}},
   "rules": [],
   "expect": {"game": {"round": 4}, "not_offered": [{"seat": 1, "option": 500}],
              "players": {"1": {"score": 4, "revealed_code": 258}, "2": {"score": 0, "revealed_code": 369}}}},

  {"name": "R22 game ends after round 12; higher score wins", "rule": "R22", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"code": 258, "score": 3}, "2": {"code": 369, "score": 3}}},
   "rules": [{"seat": 1, "options_include": 369}],
   "expect": {"winner": 1, "standings": {"1": 500, "2": 300}, "game": {"round": 12},
              "players": {"1": {"score": 5, "revealed_code": 258}, "2": {"score": 3, "revealed_code": 369}}}},

  {"name": "R22 level score broken by fewer wrong guesses", "rule": "R22", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"code": 258, "score": 5, "wrong_count": 1}, "2": {"code": 369, "score": 5, "wrong_count": 0}}},
   "rules": [],
   "expect": {"winner": 2, "standings": {"1": 599, "2": 600}, "game": {"round": 12},
              "players": {"1": {"score": 6, "wrong_count": 1}, "2": {"score": 6, "wrong_count": 0}}}},

  {"name": "R22 full tie is a shared win", "rule": "R22", "players": 2, "seed": 1, "default": "decline",
   "given": {"game": {"round": 11}, "players": {"1": {"code": 258, "score": 4, "wrong_count": 1}, "2": {"code": 369, "score": 4, "wrong_count": 1}}},
   "rules": [],
   "expect": {"winner": [1, 2], "standings": {"1": 499, "2": 499}, "game": {"round": 12},
              "players": {"1": {"score": 5}, "2": {"score": 5}}}}
]
```
````
