# Break the Code: Three-Leg Duel

Two players each hide a three-digit code. Over three legs of four rounds they ask the same number-question cards at the same time and score points for cracking the opponent's code early.

Players: 2 to 2, best with 2

## Parameters

- `legs` = 3
- `rounds_per_leg` = 4
- `total_rounds` = 12
- `digit_min` = 0
- `digit_max` = 9
- `code_length` = 3
- `default_code` = 12
- `question_cards` = 6
- `cards_used_per_leg` = 4
- `guesses_per_leg` = 2
- `correct_score_base` = 5
- `wrong_guess_penalty` = 1
- `high_digit_threshold` = 5
- `pass_value` = 0
- `starting_score` = 0

## Round

1. **update** (all players): round += 1. Leg-round L = ((round - 1) mod 4) + 1.
2. **poll** (all players (only when L = 1, i.e. rounds 1, 5, 9)): Three different digits are sorted ascending and stored as code = 100A+10B+C. Any other entry sets code = 12 (0-1-2). Then guesses_left = 2, solved = 0, used_mask = 0. Each player's code is visible only to its owner.
3. **sync** (all players): Each player receives their own state: code, guesses_left, solved, used_mask, score.
4. **poll** (all players): ask = the chosen card. If the answer is missing or invalid, ask = the lowest card n with floor(used_mask/2^(n-1)) mod 2 = 0. Then used_mask += 2^(ask-1).
5. **update** (all players): For each player, with the opponent's code digits A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10: answer = A+B+C if ask=1; count of digits with d mod 2 = 0 if ask=2; C-A if ask=3; count of digits >= 5 if ask=4; (B-A=1)+(C-B=1) if ask=5; count of digits with d mod 3 = 0 if ask=6. Announce to both players each player's ask and answer.
6. **poll** (all players): If the entry is three different digits AND guesses_left > 0 AND solved = 0, guess = the sorted code as 100A+10B+C and guesses_left -= 1. Otherwise guess = 0 (a pass).
7. **update** (all players): For each player with guess > 0: if guess = opponent's code, score += 5 - L and solved = 1; otherwise score -= 1 and wrong_count += 1. Announce every guess and its result (correct or wrong) to both players.
8. **tell** (all players (only when L = 4, i.e. rounds 4, 8, 12)): Reveal both players' code to both players and announce the current score of each player.
9. **check** (all players): If round >= 12, end the game; otherwise continue to the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.score * 100 - you.wrong_count` (the highest wins; players level at the top share the win)
- decided by: Highest total score wins. If scores are equal, the player with fewer wrong guesses over the match wins. If both are equal, both share the win (a draw).

## Choices the source did not make

- Exactly 2 players: The designer fixed the table at 2. It is a head-to-head deduction duel in which each player reads one opponent's code. With 3 or more there is no single opponent to question.
- No talk step: The source has no talk. With two rivals racing to deduce, words would add nothing the rules use.
- Codes are visible to their owner (ally): The source says only the engine knows the codes. The owner wrote their own code, and a player attribute cannot be fully hidden, so the opponent simply never sees it.
- Tie-break expression score*100 - wrong_count: wrong_count is at most 6, so the score always dominates and fewer wrong guesses breaks ties. Players who are equal on both share the win, which is the draw.
- guesses_left, solved, used_mask, ask, answer and guess made public: The rules announce each ask, answer, guess and result to both players, so this state is common knowledge.
- Strategy at the table: A thoughtful player picks cards that split the remaining codes best and weighs guessing early for more points against the 1-point penalty and the limit of 2 guesses.

## Simplifications

- Opponent's code is referenced inside a player's update: The engine has no direct player-attribute operand. With exactly 2 seats, 'opponent' is the other seat, and a table-mirror workaround may be used for the comparison.
- Steps 1 and 6 run every round but act only when their leg-round condition holds: The step list is flat; the per-step `when` conditions express 'leg-round 1 only' and 'leg-round 4 only'.

## Unsupported (needs engine work)

- none
