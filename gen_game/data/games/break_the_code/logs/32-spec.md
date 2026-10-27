# 32 spec

- time: 2026-10-27T19:02:50+00:00 (34.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 15890c84f49a35a9, reply sha256 9d69bd0989d9efc7

## Sent

````
Game: Break the Code: Coarse Clues
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
R1. Structure. Two players play a match of 12 rounds, split into 3 legs of 4 rounds each. Legs start at rounds 1, 5 and 9. The round counter starts at 0 and increases by exactly 1 at the very start of each round; nothing else changes it. Leg-round = ((round - 1) mod 4) + 1, so it runs 1, 2, 3, 4 within each leg.

R2. Player state. Each player has their own: score, wrong count, code, guesses left, solved, card asked, answer and guess. Score and wrong count start at 0 and carry over between legs. Both players are always handled separately: one player's result never blocks or changes the other's, except where a rule says the code's owner scores.

R3. New leg. When leg-round is 1, first reset each player's own guesses left to 2 and each player's own solved to 0. Then both players secretly and at the same time enter a code as a number, for example 147, 852, or 12 (meaning 0-1-2). In other rounds there is no code prompt and codes stay unchanged.

R4. Parsing a code. Read the entry x as digits A = floor(x / 100), B = floor(x / 10) mod 10 and C = x mod 10. If x is a whole number from 0 to 999 and A, B and C are all different, sort them ascending as a < b < c and store 100*a + 10*b + c. For example, 852 is stored as 258.

R5. Invalid code. Any other entry is stored as code 12 (digits 0, 1, 2). This covers repeated digits, out-of-range or non-numeric entries, and missing or declined entries.

R6. Asking. Every round, both players at the same time may pick one card number from 1 to 6 to ask about the opponent's code. Declining or giving an invalid number means no question this round. A card may be asked again; it gives the same answer. With the opponent's sorted digits a < b < c, the answers are:
- Card 1, High: how many of the three digits are 5 or higher (0-3).
- Card 2, Odd: how many of the digits are odd (0-3).
- Card 3, Prime: how many of the digits are 2, 3, 5 or 7 (0-3).
- Card 4, Threes: how many of the digits are 0, 3, 6 or 9 (0-3).
- Card 5, Chain: (1 if b - a = 1 else 0) + (1 if c - b = 1 else 0) (0-2).
- Card 6, Sum mod 4: (a + b + c) mod 4 (0-3).
Each answer is shown privately to the player who asked. Then both players are told which card number (or none) each player asked.

R7. Guessing. Then both players at the same time may enter a guess of the opponent's code. A player is prompted only if that player's own guesses left is above 0 and that player's own solved is 0. The guess is parsed as in R4.
- Pass: declining, or an entry that does not give three different digits from 0 to 999. A pass costs nothing.
- Correct: a valid guess equal to the opponent's stored code. The guesser scores 5 - leg-round, that is 4, 3, 2 or 1. That player's own solved becomes 1 for the rest of the leg.
- Wrong: any other valid guess. The guesser scores -1, their wrong count increases by 1, and their guesses left decreases by 1. The opponent, the code's owner, scores +1.
If both players guess correctly in the same round, both score.

R8. Results. After guessing, both players are told whether each player passed, guessed right or guessed wrong. Codes are not shown.

R9. End of leg. When leg-round is 4, after R8, each player whose own code was not guessed correctly during this leg scores +1. That is, a player scores +1 if the opponent's solved is still 0. Then both codes are revealed to both players.

R10. End. The game ends after round 12.

How the winner is decided: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If those are also equal, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Break the Code: Coarse Clues",
  "summary": "Two players each hide a three-digit code of distinct digits, ask coarse clue cards about the opponent's code, and guess it in as few rounds of a 4-round leg as possible, over 3 legs.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "total_rounds": 12,
    "legs": 3,
    "rounds_per_leg": 4,
    "leg_starts": [1, 5, 9],
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total score, carried over between legs", "observable": true},
      {"key": "wrong_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of wrong guesses over the match; the tie-break, where fewer is better", "observable": true},
      {"key": "code", "type": "number", "visible": "ally", "initial": 12, "meaning": "Own stored code: sorted distinct digits stored as 100a+10b+c", "observable": false},
      {"key": "revealed_code", "type": "number", "visible": "public", "initial": -1, "meaning": "Copy of code made public at the end of each leg; -1 means not yet revealed", "observable": true},
      {"key": "guesses_left", "type": "number", "visible": "public", "initial": 2, "meaning": "Wrong guesses still allowed in this leg", "observable": false},
      {"key": "solved", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once this player has correctly guessed the opponent's code in this leg", "observable": false},
      {"key": "card_asked", "type": "number", "visible": "public", "initial": 0, "meaning": "Card asked this round, 1-6; 0 means none. Announced after both have asked", "observable": false},
      {"key": "answer", "type": "number", "visible": "ally", "initial": -1, "meaning": "Private answer to this round's card about the opponent's code; -1 means no question", "observable": false},
      {"key": "guess", "type": "number", "visible": "ally", "initial": -1, "meaning": "This round's parsed guess of the opponent's code; -1 means pass", "observable": false},
      {"key": "result", "type": "text", "visible": "public", "initial": "pass", "meaning": "This round's guess outcome: pass, right or wrong", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Round counter; increases by exactly 1 at the start of each round", "observable": true},
      {"key": "leg_round", "type": "number", "visible": "public", "initial": 0, "meaning": "((round - 1) mod 4) + 1, running 1 to 4 within each leg", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 and seat 2 sit down; each one's opponent is the other seat.",
    "Each player's score and wrong_count are set to 0. Each player's code is set to 12, revealed_code to -1, guesses_left to 2 and solved to 0.",
    "The table's round is set to 0."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null,
     "effect": "round += 1; leg_round = ((round - 1) mod 4) + 1; for each player, card_asked = 0, answer = -1, guess = -1 and result = 'pass'."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When leg_round == 1: for each player, guesses_left = 2, solved = 0 and revealed_code = -1."},
    {"action": "poll", "who": "all players (only when leg_round == 1)",
     "answer": "a whole number from 0 to 999, or decline",
     "effect": "Each player's entry x is parsed into A = floor(x/100), B = floor(x/10) mod 10 and C = x mod 10. If A, B and C are all different, they are sorted ascending as a<b<c and code = 100a+10b+c. Otherwise, or if the player declines, code = 12. Nobody sees the other's entry."},
    {"action": "poll", "who": "all players",
     "answer": "a card number from 1 to 6, or decline",
     "effect": "card_asked = the chosen card, or 0 if the player declines. Answers are hidden until both are in."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "For each player with card_asked > 0, using the opponent's code digits a<b<c: card 1 gives the count of digits >= 5; card 2 the count of odd digits; card 3 the count of digits in {2,3,5,7}; card 4 the count of digits in {0,3,6,9}; card 5 gives (1 if b-a == 1 else 0) + (1 if c-b == 1 else 0); card 6 gives (a+b+c) mod 4. The result goes into that player's answer (ally, seen only by the asker)."},
    {"action": "sync", "who": "all players", "answer": null,
     "effect": "Each player privately sees their own answer."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce 'Seat 1 asked card {card_asked of seat 1}; Seat 2 asked card {card_asked of seat 2}', where 0 means no question."},
    {"action": "poll", "who": "each player with guesses_left > 0 and solved == 0",
     "answer": "a whole number from 0 to 999 as a guess of the opponent's code, or pass",
     "effect": "The entry is parsed as for codes. If its three digits are all different, guess = the sorted value; otherwise, or on a pass, guess = -1."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Applied to each player separately, from the guesses as entered. If guess == -1: result = 'pass'. If guess == the opponent's code: score += 5 - leg_round, solved = 1 and result = 'right'. If guess >= 0 and guess != the opponent's code: score -= 1, wrong_count += 1, guesses_left -= 1, result = 'wrong', and the opponent's score += 1."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce 'Seat 1: {result of seat 1}; Seat 2: {result of seat 2}'. Codes are not shown."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When leg_round == 4: each player whose opponent's solved == 0 gets score += 1. Then for each player, revealed_code = code."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "When leg_round == 4, announce 'Codes this leg: Seat 1 {revealed_code of seat 1}, Seat 2 {revealed_code of seat 2}'."},
    {"action": "check", "who": "table", "answer": null,
     "effect": "If round >= 12, end the game; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score * 100 - you.wrong_count",
    "decided_by": "The higher total score wins. If the scores are level, the player with fewer wrong guesses wins. If both are level, the two players share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a round starts, round increases by exactly 1 and leg_round = ((round - 1) mod 4) + 1, so rounds 1, 5 and 9 have leg_round 1 and rounds 4, 8 and 12 have leg_round 4."},
    {"id": "R2", "text": "When the game starts, each player's score is 0 and wrong_count is 0, and neither is reset between legs."},
    {"id": "R3", "text": "When leg_round is 1, each player's guesses_left is set to 2 and solved to 0 before codes are entered."},
    {"id": "R4", "text": "When leg_round is 1, both players are polled at the same time for a code; when leg_round is 2, 3 or 4, no code is asked for and codes stay unchanged."},
    {"id": "R5", "text": "When a player enters 852 as a code, code is stored as 258; when a player enters 12, code is stored as 12."},
    {"id": "R6", "text": "When a code entry has repeated digits (for example 447) or is declined, code is stored as 12."},
    {"id": "R7", "text": "When a player asks card 1 and the opponent's code is 258, answer is 2 (digits 5 and 8 are 5 or higher)."},
    {"id": "R8", "text": "When a player asks card 2 and the opponent's code is 258, answer is 1 (the count of odd digits)."},
    {"id": "R9", "text": "When a player asks card 3 and the opponent's code is 258, answer is 2 (the count of digits in 2, 3, 5, 7)."},
    {"id": "R10", "text": "When a player asks card 4 and the opponent's code is 369, answer is 3 (the count of digits in 0, 3, 6, 9)."},
    {"id": "R11", "text": "When a player asks card 5 and the opponent's code is 123, answer is 2; when the code is 258, answer is 0."},
    {"id": "R12", "text": "When a player asks card 6 and the opponent's code is 258, answer is 3 ((2+5+8) mod 4)."},
    {"id": "R13", "text": "When a player declines to ask, card_asked is 0 and no answer is given; asking the same card again gives the same answer."},
    {"id": "R14", "text": "After asking, the answer is shown only to the asker, and both players are told which card each asked."},
    {"id": "R15", "text": "When a player's guesses_left is 0 or solved is 1, that player is not asked for a guess."},
    {"id": "R16", "text": "When a guess is declined or has repeated digits, it is a pass and score, wrong_count and guesses_left are unchanged."},
    {"id": "R17", "text": "When a valid guess equals the opponent's code, the guesser scores 5 - leg_round (4, 3, 2 or 1 in leg-rounds 1 to 4) and solved becomes 1."},
    {"id": "R18", "text": "When a valid guess does not equal the opponent's code, the guesser's score decreases by 1, wrong_count increases by 1, guesses_left decreases by 1, and the opponent's score increases by 1."},
    {"id": "R19", "text": "When both players guess correctly in the same round, both score 5 - leg_round."},
    {"id": "R20", "text": "After guessing, both players are told whether each one passed, guessed right or guessed wrong, and codes are not shown."},
    {"id": "R21", "text": "When leg_round is 4, each player whose opponent's solved is 0 scores +1, and then both codes are revealed to both players."},
    {"id": "R22", "text": "When round 12 has finished, the game ends; the higher score wins, a level score is broken by fewer wrong_count, and a full tie is a draw."}
  ],
  "offers": [
    {"question": "Enter your secret code (only when leg_round is 1)", "who": "both seats", "options": "any whole number from 0 to 999, or decline"},
    {"question": "Pick a card to ask about the opponent's code", "who": "both seats, every round", "options": "card 1 (High), 2 (Odd), 3 (Prime), 4 (Threes), 5 (Chain), 6 (Sum mod 4), or decline"},
    {"question": "Guess the opponent's code", "who": "each seat with guesses_left > 0 and solved == 0; a seat with guesses_left 0 or solved 1 is not asked", "options": "any whole number from 0 to 999, or pass"}
  ],
  "choices": [
    {"what": "Exactly 2 players", "why": "The designer fixed the game at 2. Each player attacks the single opponent's code, and owner bonuses refer to that one opponent."},
    {"what": "No talk step", "why": "The rules contain no table talk, and with two players racing to deduce each other's codes, talk would add nothing the rules want."},
    {"what": "Rank by score*100 - wrong_count", "why": "Wrong guesses are at most 6 per match, so scores dominate and fewer wrong guesses breaks ties. Players level on both share the win, which is the draw."},
    {"what": "guesses_left, solved and card_asked are public", "why": "The rules announce each player's card and guess results, so these values can be inferred by both players anyway."},
    {"what": "A revealed_code attribute copies the code at each leg's end", "why": "This gives the R9 reveal a stated piece of public state while the live code stays private during play."},
    {"what": "Strategy at the table", "why": "A thoughtful player picks the cards that split the remaining candidate codes most evenly and weighs an early guess, which is worth more points, against the -1 penalty plus +1 to the opponent for a wrong guess."}
  ],
  "simplifications": [
    {"what": "Code and guess entries are taken as a whole number from 0 to 999 or a decline, rather than as free text", "why": "The engine's number answer has a range. Out-of-range and non-numeric entries cannot occur, and declining covers the 'missing' case, which still maps to code 12 or a pass as the rules require."},
    {"what": "Invalid card numbers are reduced to the decline option", "why": "The choice list only offers cards 1 to 6 or decline, which has the same effect as the rules' invalid entry: no question."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Break the Code: Coarse Clues",
  "summary": "Two players each hide a three-digit code of distinct digits, ask coarse clue cards about the opponent's code, and try to guess it early in a 4-round leg, over 3 legs.",
  "players": {"min": 2, "max": 2, "suggested": 2},
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total score, carried over between legs", "observable": true},
      {"key": "wrong_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of wrong guesses over the match. It is the tie-break, and fewer is better", "observable": true},
      {"key": "code", "type": "number", "visible": "ally", "initial": 12, "meaning": "Own stored code: sorted distinct digits stored as 100a+10b+c", "observable": false},
      {"key": "revealed_code", "type": "number", "visible": "public", "initial": -1, "meaning": "Copy of code made public at the end of each leg; -1 means not yet revealed", "observable": true},
      {"key": "guesses_left", "type": "number", "visible": "public", "initial": 2, "meaning": "Wrong guesses still allowed in this leg", "observable": false},
      {"key": "solved", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once this player has correctly guessed the opponent's code in this leg", "observable": false},
      {"key": "card_asked", "type": "number", "visible": "public", "initial": 0, "meaning": "Card asked this round, 1-6; 0 means none. Announced after both players have asked", "observable": false},
      {"key": "answer", "type": "number", "visible": "ally", "initial": -1, "meaning": "Private answer to this round's card about the opponent's code; -1 means no question", "observable": false},
      {"key": "guess", "type": "number", "visible": "ally", "initial": -1, "meaning": "This round's parsed guess of the opponent's code; -1 means pass", "observable": false},
      {"key": "result", "type": "text", "visible": "public", "initial": "pass", "meaning": "This round's guess outcome: pass, right or wrong", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Round counter; increases by exactly 1 at the start of each round", "observable": true},
      {"key": "leg_round", "type": "number", "visible": "public", "initial": 0, "meaning": "((round - 1) mod 4) + 1, running 1 to 4 within each leg", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 and seat 2 sit down; each seat's opponent is the other seat.",
    "Each player's score and wrong_count are set to 0. Each player's code is set to 12, revealed_code to -1, guesses_left to 2 and solved to 0.",
    "The table's round is set to 0."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null,
     "effect": "round += 1; leg_round = ((round - 1) mod 4) + 1; for each player, card_asked = 0, answer = -1, guess = -1 and result = 'pass'."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When leg_round == 1: for each player, guesses_left = 2, solved = 0 and revealed_code = -1."},
    {"action": "poll", "who": "all players (only when leg_round == 1)",
     "answer": "a whole number from 0 to 999, or decline",
     "effect": "Each player's entry x is parsed into A = floor(x/100), B = floor(x/10) mod 10 and C = x mod 10. If A, B and C are all different, they are sorted ascending as a<b<c and code = 100a+10b+c. Otherwise, or if the player declines, code = 12. Neither player sees the other's entry."},
    {"action": "poll", "who": "all players",
     "answer": "a card number from 1 to 6, or decline",
     "effect": "card_asked = the chosen card, or 0 if the player declines. Answers stay hidden until both are in."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "For each player with card_asked > 0, using the opponent's code digits a<b<c: card 1 gives the count of digits >= 5; card 2 the count of odd digits; card 3 the count of digits in {2,3,5,7}; card 4 the count of digits in {0,3,6,9}; card 5 gives (1 if b-a == 1 else 0) + (1 if c-b == 1 else 0); card 6 gives (a+b+c) mod 4. The result goes into that player's answer (ally, seen only by the asker)."},
    {"action": "sync", "who": "all players", "answer": null,
     "effect": "Each player privately sees their own answer."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce 'Seat 1 asked card {card_asked of seat 1}; Seat 2 asked card {card_asked of seat 2}', where 0 means no question."},
    {"action": "poll", "who": "each player with guesses_left > 0 and solved == 0",
     "answer": "a whole number from 0 to 999 as a guess of the opponent's code, or pass",
     "effect": "The entry is parsed as for codes. If its three digits are all different, guess = the sorted value; otherwise, or on a pass, guess = -1."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Applied to each player separately, using the guesses as entered. If guess == -1: result = 'pass'. If guess == the opponent's code: score += 5 - leg_round, solved = 1 and result = 'right'. If guess >= 0 and guess != the opponent's code: score -= 1, wrong_count += 1, guesses_left -= 1, result = 'wrong', and the opponent's score += 1."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce 'Seat 1: {result of seat 1}; Seat 2: {result of seat 2}'. Codes are not shown."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "When leg_round == 4: each player whose opponent's solved == 0 gets score += 1. Then, for each player, revealed_code = code."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "When leg_round == 4, announce 'Codes this leg: Seat 1 {revealed_code of seat 1}, Seat 2 {revealed_code of seat 2}'."},
    {"action": "check", "who": "table", "answer": null,
     "effect": "If round >= 12, end the game; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score * 100 - you.wrong_count",
    "decided_by": "The higher total score wins. If the scores are level, the player with fewer wrong guesses wins. If both are level, the two players share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a round starts, round increases by exactly 1 and leg_round = ((round - 1) mod 4) + 1, so rounds 1, 5 and 9 have leg_round 1 and rounds 4, 8 and 12 have leg_round 4."},
    {"id": "R2", "text": "When the game starts, each player's score is 0 and wrong_count is 0, and neither is reset between legs."},
    {"id": "R3", "text": "When leg_round is 1, each player's guesses_left is set to 2 and solved to 0 before codes are entered."},
    {"id": "R4", "text": "When leg_round is 1, both players are polled at the same time for a code; when leg_round is 2, 3 or 4, no code is asked for and codes stay unchanged."},
    {"id": "R5", "text": "When a player enters 852 as a code, code is stored as 258; when a player enters 12, code is stored as 12."},
    {"id": "R6", "text": "When a code entry has repeated digits (for example 447) or is declined, code is stored as 12."},
    {"id": "R7", "text": "When a player asks card 1 and the opponent's code is 258, answer is 2 (digits 5 and 8 are 5 or higher)."},
    {"id": "R8", "text": "When a player asks card 2 and the opponent's code is 258, answer is 1 (the count of odd digits)."},
    {"id": "R9", "text": "When a player asks card 3 and the opponent's code is 258, answer is 2 (the count of digits in 2, 3, 5, 7)."},
    {"id": "R10", "text": "When a player asks card 4 and the opponent's code is 369, answer is 3 (the count of digits in 0, 3, 6, 9)."},
    {"id": "R11", "text": "When a player asks card 5 and the opponent's code is 123, answer is 2; when the code is 258, answer is 0."},
    {"id": "R12", "text": "When a player asks card 6 and the opponent's code is 258, answer is 3 ((2+5+8) mod 4)."},
    {"id": "R13", "text": "When a player declines to ask, card_asked is 0 and no answer is given; asking the same card again gives the same answer."},
    {"id": "R14", "text": "After asking, the answer is shown only to the asker, and both players are told which card each player asked."},
    {"id": "R15", "text": "When a player's guesses_left is 0 or solved is 1, that player is not asked for a guess."},
    {"id": "R16", "text": "When a guess is declined or has repeated digits, it is a pass, and score, wrong_count and guesses_left are unchanged."},
    {"id": "R17", "text": "When a valid guess equals the opponent's code, the guesser scores 5 - leg_round (4, 3, 2 or 1 in leg-rounds 1 to 4) and solved becomes 1."},
    {"id": "R18", "text": "When a valid guess does not equal the opponent's code, the guesser's score decreases by 1, wrong_count increases by 1, guesses_left decreases by 1, and the opponent's score increases by 1."},
    {"id": "R19", "text": "When both players guess correctly in the same round, both score 5 - leg_round."},
    {"id": "R20", "text": "After guessing, both players are told whether each player passed, guessed right or guessed wrong, and codes are not shown."},
    {"id": "R21", "text": "When leg_round is 4, each player whose opponent's solved is 0 scores +1, and then both codes are revealed to both players."},
    {"id": "R22", "text": "When round 12 has finished, the game ends; the higher score wins, a level score is broken by the lower wrong_count, and a full tie is a draw."}
  ],
  "offers": [
    {"question": "Enter your secret code (only when leg_round is 1)", "who": "both seats", "options": "any whole number from 0 to 999, or decline"},
    {"question": "Pick a card to ask about the opponent's code", "who": "both seats, every round", "options": "card 1 (High), 2 (Odd), 3 (Prime), 4 (Threes), 5 (Chain), 6 (Sum mod 4), or decline"},
    {"question": "Guess the opponent's code", "who": "each seat with guesses_left > 0 and solved == 0; a seat with guesses_left 0 or solved 1 is not asked", "options": "any whole number from 0 to 999, or pass"}
  ],
  "choices": [
    {"what": "Exactly 2 players", "why": "The designer fixed the game at 2. Each player attacks the single opponent's code, and owner bonuses refer to that one opponent."},
    {"what": "No talk step", "why": "The rules contain no table talk. With two players racing to deduce each other's codes, talk would add nothing the rules want."},
    {"what": "Rank by score*100 - wrong_count", "why": "Wrong guesses are at most 6 per match, so score dominates and fewer wrong guesses breaks ties. Players level on both share the win, which is the draw."},
    {"what": "Leg starts listed as leg_start_1, leg_start_2 and leg_start_3", "why": "Each parameter must be a single number."},
    {"what": "guesses_left, solved and card_asked are public", "why": "The rules announce each player's card and guess results, so both players can infer these values anyway."},
    {"what": "A revealed_code attribute copies the code at the end of each leg", "why": "This gives the R9 reveal a stated piece of public state, while the live code stays private during play."},
    {"what": "Strategy at the table", "why": "A thoughtful player picks the cards that split the remaining candidate codes most evenly. They also weigh an early guess, which is worth more points, against the -1 penalty plus +1 to the opponent for a wrong guess."}
  ],
  "simplifications": [
    {"what": "Code and guess entries are taken as a whole number from 0 to 999 or a decline, rather than as free text", "why": "The engine's number answer has a range, so out-of-range and non-numeric entries cannot occur. Declining covers the 'missing' case, which still maps to code 12 or a pass as the rules require."},
    {"what": "Invalid card numbers are reduced to the decline option", "why": "The choice list offers only cards 1 to 6 or decline. Declining has the same effect as the rules' invalid entry: no question."}
  ],
  "unsupported": []
}
```
````
