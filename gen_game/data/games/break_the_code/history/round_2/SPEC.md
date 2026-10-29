# Break the Code: Coarse Clues

Two players each hide a three-digit code of distinct digits, ask coarse clue cards about the opponent's code, and try to guess it early in a 4-round leg, over 3 legs.

Players: 2 to 2, best with 2

## Parameters

- `total_rounds` = 12
- `legs` = 3
- `rounds_per_leg` = 4
- `leg_start_1` = 1
- `leg_start_2` = 5
- `leg_start_3` = 9
- `guesses_per_leg` = 2
- `code_min` = 0
- `code_max` = 999
- `invalid_code_default` = 12
- `card_min` = 1
- `card_max` = 6
- `high_threshold` = 5
- `correct_score_base` = 5
- `wrong_guess_penalty` = -1
- `owner_bonus_on_wrong_guess` = 1
- `unsolved_leg_bonus` = 1
- `initial_score` = 0
- `initial_wrong_count` = 0
- `rank_score_weight` = 100

## Round

1. **update** (table): round += 1; leg_round = ((round - 1) mod 4) + 1; for each player, card_asked = 0, answer = -1, guess = -1 and result = 'pass'.
2. **update** (all players): When leg_round == 1: for each player, guesses_left = 2, solved = 0 and revealed_code = -1.
3. **poll** (all players (only when leg_round == 1)): Each player's entry x is parsed into A = floor(x/100), B = floor(x/10) mod 10 and C = x mod 10. If A, B and C are all different, they are sorted ascending as a<b<c and code = 100a+10b+c. Otherwise, or if the player declines, code = 12. Neither player sees the other's entry.
4. **poll** (all players): card_asked = the chosen card, or 0 if the player declines. Answers stay hidden until both are in.
5. **update** (all players): For each player with card_asked > 0, using the opponent's code digits a<b<c: card 1 gives the count of digits >= 5; card 2 the count of odd digits; card 3 the count of digits in {2,3,5,7}; card 4 the count of digits in {0,3,6,9}; card 5 gives (1 if b-a == 1 else 0) + (1 if c-b == 1 else 0); card 6 gives (a+b+c) mod 4. The result goes into that player's answer (ally, seen only by the asker).
6. **sync** (all players): Each player privately sees their own answer.
7. **tell** (all players): Announce 'Seat 1 asked card {card_asked of seat 1}; Seat 2 asked card {card_asked of seat 2}', where 0 means no question.
8. **poll** (each player with guesses_left > 0 and solved == 0): The entry is parsed as for codes. If its three digits are all different, guess = the sorted value; otherwise, or on a pass, guess = -1.
9. **update** (all players): Applied to each player separately, using the guesses as entered. If guess == -1: result = 'pass'. If guess == the opponent's code: score += 5 - leg_round, solved = 1 and result = 'right'. If guess >= 0 and guess != the opponent's code: score -= 1, wrong_count += 1, guesses_left -= 1, result = 'wrong', and the opponent's score += 1.
10. **tell** (all players): Announce 'Seat 1: {result of seat 1}; Seat 2: {result of seat 2}'. Codes are not shown.
11. **update** (all players): When leg_round == 4: each player whose opponent's solved == 0 gets score += 1. Then, for each player, revealed_code = code.
12. **tell** (all players): When leg_round == 4, announce 'Codes this leg: Seat 1 {revealed_code of seat 1}, Seat 2 {revealed_code of seat 2}'.
13. **check** (table): If round >= 12, end the game; otherwise continue to the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.score * 100 - you.wrong_count` (the highest wins; players level at the top share the win)
- decided by: The higher total score wins. If the scores are level, the player with fewer wrong guesses wins. If both are level, the two players share the win, which is a draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed the game at 2. Each player attacks the single opponent's code, and owner bonuses refer to that one opponent.
- No talk step: The rules contain no table talk. With two players racing to deduce each other's codes, talk would add nothing the rules want.
- Rank by score*100 - wrong_count: Wrong guesses are at most 6 per match, so score dominates and fewer wrong guesses breaks ties. Players level on both share the win, which is the draw.
- Leg starts listed as leg_start_1, leg_start_2 and leg_start_3: Each parameter must be a single number.
- guesses_left, solved and card_asked are public: The rules announce each player's card and guess results, so both players can infer these values anyway.
- A revealed_code attribute copies the code at the end of each leg: This gives the R9 reveal a stated piece of public state, while the live code stays private during play.
- Strategy at the table: A thoughtful player picks the cards that split the remaining candidate codes most evenly. They also weigh an early guess, which is worth more points, against the -1 penalty plus +1 to the opponent for a wrong guess.

## Simplifications

- Code and guess entries are taken as a whole number from 0 to 999 or a decline, rather than as free text: The engine's number answer has a range, so out-of-range and non-numeric entries cannot occur. Declining covers the 'missing' case, which still maps to code 12 or a pass as the rules require.
- Invalid card numbers are reduced to the decline option: The choice list offers only cards 1 to 6 or decline. Declining has the same effect as the rules' invalid entry: no question.

## Unsupported (needs engine work)

- none
