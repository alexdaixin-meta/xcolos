# Break the Code: Duel of Two Tiles

Two players each hide a two-tile code (tiles 0-5) every leg, then ask simultaneous property questions or guess the opponent's code; earlier correct guesses score more over 4 legs of 6 turns.

Players: 2 to 2, best with 2

## Parameters

- `legs` = 4
- `turns_per_leg` = 6
- `total_turns` = 24
- `starting_score` = 0
- `tile_min` = 0
- `tile_max` = 5
- `possible_codes` = 21
- `guess_score_base` = 7
- `sum_low_max` = 3
- `sum_middle_min` = 4
- `sum_middle_max` = 6
- `sum_high_min` = 7
- `sum_high_max` = 10
- `gap_pair` = 0
- `gap_adjacent` = 1
- `gap_apart_min` = 2
- `big_tile_min` = 3
- `edge_tile_low` = 0
- `edge_tile_high` = 5
- `wrong_guess_cost` = 0
- `tie_break_weight` = 10

## Round

1. **update** (all players): when turn_in_leg == 1: set solved = false, last_action = '', last_answer = '' for both players
2. **poll** (all players): when turn_in_leg == 1: set code_low and code_high from the chosen code (low <= high), and copy them to seatN_code_low and seatN_code_high; no one sees another's choice
3. **sync** (all players): each player is shown their own code_low and code_high, their score, legs_solved, leg and turn_in_leg
4. **poll** (each player with solved == false): set last_action to the choice; for a guess, set guess_low and guess_high from it. Players with solved == true are not asked and get last_action = 'solved'
5. **update** (all players): for each unsolved player, with the opponent's code (L, H) taken from the opponent's mirror attributes: sum -> last_answer = LOW if L+H <= 3, MIDDLE if 4 <= L+H <= 6, HIGH if L+H >= 7; odd -> number of odd tiles among L, H (0-2); gap -> PAIR if H-L == 0, ADJACENT if H-L == 1, APART if H-L >= 2; big -> number of tiles >= 3 (0-2); edge -> number of tiles equal to 0 or 5 (0-2); guess -> if guess_low == L and guess_high == H then last_answer = CORRECT, score += 7 - turn_in_leg, legs_solved += 1, solved = true; otherwise last_answer = WRONG with the count of guessed tiles that appear in the code, each code tile matching at most one guessed tile (0 or 1), and no other cost
6. **tell** (all players): announce to both: 'Leg {leg}, turn {turn_in_leg}. Seat 1: {last_action} -> {last_answer}. Seat 2: {last_action} -> {last_answer}. Scores: {score} / {score}.'
7. **tell** (all players): when turn_in_leg == 6: reveal both codes to both players: 'Seat 1's code was {seat1_code_low}-{seat1_code_high}; Seat 2's code was {seat2_code_low}-{seat2_code_high}.' Unsolved legs score nothing
8. **update** (all players): if turn_in_leg == 6 then turn_in_leg = 1 and leg += 1, else turn_in_leg += 1
9. **check** (all players): end the game if leg > 4, otherwise continue with the next turn

## Ending

- ends when: leg > 4
- ranked by: `you.score * 10 + you.legs_solved` (the highest wins; players level at the top share the win)
- decided by: The higher total score wins. If scores are equal, the player who solved more legs wins (legs_solved is at most 4, so a weight of 10 keeps score first). If both are equal, both share the win, which is a draw.

## Choices the source did not make

- 2 players (min 2, max 2, suggested 2): The designer set 2. Each player cracks the one opponent's code, and every answer is computed from that opponent's code, so a third seat would have no defined target. The strategy is to pick questions that split the remaining codes well, to guess when the expected value of an early guess beats one more question, and to choose codes that are hard to narrow down.
- No talk step: The source has no talk, and in a two-player duel talk would only add words that could be bluffs about one's own code; the rules are kept as written.
- The code is chosen from a list of the 21 valid codes: This makes an invalid code (low > high) impossible to enter with a single answer, and it matches the source's count of 21.
- A guess is one of 26 action options: Asking the action and the guess in one poll avoids a separate follow-up question that only guessers would get.
- Turns still run after both players have solved a leg: The source always plays 6 turns per leg. With nobody unsolved, a turn simply asks no one and scores nothing.
- Tie-break expressed as score * 10 + legs_solved: legs_solved is at most 4, so a weight of 10 keeps score first and legs solved second. A full tie becomes a shared win, which is the source's draw.

## Simplifications

- Each code is mirrored into hidden table attributes (seat1_code_low, seat1_code_high, seat2_code_low, seat2_code_high): The engine has no operand for another player's attribute, and answers must be computed from the opponent's code (player_attribute_compare workaround).
- Ranking by a single arithmetic expression, with the draw as a shared top value: The engine ranks by one expression and players level at the top share the win, which reproduces the source's draw.

## Unsupported (needs engine work)

- none
