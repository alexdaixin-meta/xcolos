# Decrypto: Points Race

Two teams of two take turns encrypting three-digit codes as word clues for a partner who knows the team's secret keywords, while the rival team tries to intercept; points over 8 rounds decide the winning team.

Players: 4 to 4, best with 4

## Parameters

- `rounds` = 8
- `seats` = 4
- `team_size` = 2
- `keyword_list_size` = 40
- `keywords_per_team` = 4
- `code_length` = 3
- `code_digit_min` = 1
- `code_digit_max` = 4
- `code_count` = 24
- `clues_per_team_per_round` = 3
- `clue_min_letters` = 2
- `clue_max_letters` = 20
- `decode_points_per_position` = 1
- `exact_decode_bonus_points` = 1
- `exact_decode_count_gain` = 1
- `intercept_points_per_position` = 1
- `exact_intercept_bonus_points` = 2
- `exact_intercept_count_gain` = 1
- `first_scoring_interception_round` = 2
- `invalid_penalty_points` = 3
- `starting_points` = 0

## Round

1. **update** (all players): If round is odd: role = Encryptor for seats 1 and 3, Decoder for seats 2 and 4. If round is even: role = Encryptor for seats 2 and 4, Decoder for seats 1 and 3. Reset red_invalid, blue_invalid to false, red_gain, blue_gain to 0, and every guess to empty.
2. **tell** (all players): Announce: 'Round {round}: the Encryptors are seats {red encryptor} (Red) and {blue encryptor} (Blue); the Decoders are seats {red decoder} (Red) and {blue decoder} (Blue).'
3. **poll** (the two Encryptors): Red Encryptor's answer is set into red_code; Blue Encryptor's answer is set into blue_code (both hidden from all players, including the Decoder teammate).
4. **poll** (the two Encryptors): Red Encryptor's three clues are set into red_clues and Blue Encryptor's into blue_clues, in order.
5. **update** (Red): red_invalid = true if the referee rules the sentence false; otherwise it stays false. (judged: "Each of Red's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Red's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history.")
6. **update** (Blue): blue_invalid = true if the referee rules the sentence false; otherwise it stays false. (judged: "Each of Blue's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Blue's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history.")
7. **tell** (all players): Announce all six clues: 'Red clues: {red_clues}. Blue clues: {blue_clues}.'
8. **poll** (all players): Each Decoder's answer (a decode of their own team's clues) and each Encryptor's answer (an interception of the opposing team's clues) is stored in that player's guess.
9. **update** (both teams): Decode scoring. For Red, if red_invalid is false: matches = the number of positions 1-3 where the Red Decoder's guess digit equals red_code's digit; red_gain += matches; if matches == 3, red_gain += 1 and exact_decodes += 1 for seats 1 and 2. For Blue, the same with blue_invalid, the Blue Decoder's guess and blue_code, with exact_decodes added for seats 3 and 4. An invalid team gains 0 here.
10. **update** (both teams): Interception scoring, only when round >= 2. Red: matches = the number of positions where the Red Encryptor's guess equals blue_code; red_gain += matches; if matches == 3, red_gain += 2 and exact_interceptions += 1 for seats 1 and 2. Blue: the same with the Blue Encryptor's guess against red_code, adding to blue_gain and to seats 3 and 4. When round == 1, nothing changes.
11. **update** (both teams): Invalid penalty: if red_invalid, blue_gain += 3; if blue_invalid, red_gain += 3. Then red_points += red_gain and blue_points += blue_gain; score of seats 1,2 = red_points; score of seats 3,4 = blue_points.
12. **update** (all players): Append to history: 'Round {round} Red clues {red_clues}, code {red_code}; Blue clues {blue_clues}, code {blue_code}'.
13. **tell** (all players): Announce: 'Red's code was {red_code}, Blue's was {blue_code}. Guesses: seat 1 {guess}, seat 2 {guess}, seat 3 {guess}, seat 4 {guess}. Red invalid: {red_invalid}; Blue invalid: {blue_invalid}. Red gained {red_gain} (total {red_points}); Blue gained {blue_gain} (total {blue_points}).'
14. **update** (all players): round += 1
15. **check** (all players): End the game if round > 8; otherwise repeat the round.

## Ending

- ends when: round > 8
- ranked by: `you.score * 10000 + you.exact_interceptions * 100 + you.exact_decodes` (the highest wins; players level at the top share the win)
- decided by: Each player stands on their team's points, then its exact interceptions, then its exact decodes. The team that is higher wins and both its players win. If both teams are level on all three, all four players share the result as a draw.

## Choices the source did not make

- 4 players (min 4, max 4, suggested 4): The designer fixed two teams of two. The game needs an Encryptor and a Decoder on each side, so the minimum is 4. More seats would break the fixed role swap and the team structure, so the maximum is not larger. The strategy is to give clues obvious to a teammate who knows the keywords but opaque to rivals who read the growing history, and to read the rivals' clue patterns to intercept.
- The 40-noun word list: The source says a fixed list of 40 common nouns but does not name them, so a concrete list was chosen.
- No talk step: The source forbids all talk other than the clues.
- Clues are entered as one comma-separated text answer: The engine takes one short text per question, and the three clues belong to one simultaneous step.
- Ranking is score * 10000 + exact_interceptions * 100 + exact_decodes: This encodes the source's tie-break order in one expression. Exact counts never exceed 8, so the weights cannot overlap. A full tie shares the win, which is the source's draw.
- Interception guesses are still asked in round 1: The source has every Encryptor choose an interception every round and only says round 1 interceptions score nothing.

## Simplifications

- True codes are stored as hidden table attributes (red_code, blue_code) rather than on the Encryptor: A player's hidden attribute is visible to the whole team, but the source says no one else, including the Decoder teammate, may see the code.
- Team points are mirrored onto both teammates' score, exact_interceptions and exact_decodes: The ending ranks players, so each player carries the team totals in order to win or lose together.
- Clue validity is ruled by a referee from one sentence: Word, letter-count, substring and history-repeat checks on free text are beyond plain arithmetic. All scoring stays arithmetic.

## Unsupported (needs engine work)

- none
