# Decrypto Duel

Two teams of two take turns giving three meaning-only clues to a secret 3-digit code over their team's four hidden keywords. Teammates must decode their own code while the rival team tries to intercept it.

Players: 4 to 4, best with 4

## Parameters

- `player_count` = 4
- `team_size` = 2
- `word_list_size` = 40
- `keywords_per_team` = 4
- `code_length` = 3
- `code_digit_min` = 1
- `code_digit_max` = 4
- `max_rounds` = 8
- `interception_limit` = 2
- `miscommunication_limit` = 2
- `first_intercept_round` = 2
- `correct_decode_gain` = 1
- `miscommunication_gain` = 1
- `interception_gain` = 1

## Round

1. **update** (all players): round += 1; if round is odd, seats 1 and 3 get role = encryptor and seats 2 and 4 get role = decoder; if round is even, seats 2 and 4 get role = encryptor and seats 1 and 3 get role = decoder; set white_valid = true and black_valid = true; announce the round number and each team's Encryptor and Decoder.
2. **poll** (the two players with role = encryptor): the White Encryptor's answer is stored in white_code and the Black Encryptor's in black_code (both hidden).
3. **poll** (the two players with role = encryptor): the White Encryptor's text is stored in white_clues and the Black Encryptor's in black_clues.
4. **update** (the White Encryptor): if judged false: white_valid = false and white_miscommunications += 1. (judged: "White's three clues in white_clues each point to the White keyword numbered by the matching digit of white_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue White used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information.")
5. **update** (the Black Encryptor): if judged false: black_valid = false and black_miscommunications += 1. (judged: "Black's three clues in black_clues each point to the Black keyword numbered by the matching digit of black_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue Black used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information.")
6. **tell** (all players): show white_clues and black_clues to all four players at once; codes stay secret.
7. **poll** (all players): each player's answer is stored in their guess; no answer leaves guess empty, which never matches.
8. **update** (the two decoders): when white_valid: if the White decoder's guess == white_code then white_decodes += 1, else white_miscommunications += 1. When black_valid: if the Black decoder's guess == black_code then black_decodes += 1, else black_miscommunications += 1. A team with valid = false is not scored here.
9. **update** (the two encryptors): when round >= 2: if the White encryptor's guess == black_code then white_interceptions += 1; if the Black encryptor's guess == white_code then black_interceptions += 1 (regardless of validity).
10. **update** (all players): append to history an entry {round, white_clues, white_code, black_clues, black_code} and announce both true codes to everyone.
11. **update** (all players): compute result: let WQ = (white_interceptions >= 2 and white_miscommunications < 2), BQ = (black_interceptions >= 2 and black_miscommunications < 2), WM = (white_miscommunications >= 2), BM = (black_miscommunications >= 2). If WQ and not BQ then result = 1; else if BQ and not WQ then result = -1; else if BM and not WM then result = 1; else if WM and not BM then result = -1; else let K = (white_interceptions - white_miscommunications - black_interceptions + black_miscommunications) * 10000 + (white_interceptions - black_interceptions) * 100 + (white_decodes - black_decodes), and result = 1 if K > 0, -1 if K < 0, 0 if K == 0.
12. **check** (all players): end the game if white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8; otherwise continue to the next round.

## Ending

- ends when: white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8
- ranked by: `you.team_sign * result` (the highest wins; players level at the top share the win)
- decided by: result is +1 if White wins by the ordered rules (sole team with 2+ Interceptions and fewer than 2 Miscommunications; else the sole team without 2+ Miscommunications; else higher Interceptions minus Miscommunications, then more Interceptions, then more Correct Decodes), -1 if Black wins, and 0 on a draw. Both members of the winning team score 1 and win together. On a draw all four score 0 and share the result.

## Choices the source did not make

- Exactly 4 players, suggested 4: The designer fixed two teams of two (one Encryptor and one Decoder each), and the roles and teams depend on exactly these seats.
- No talk step: The rules forbid any discussion phase; teammates may communicate only through clues.
- Winner computed as a table attribute result in {+1, 0, -1}, ranked by you.team_sign * result: Ranking must be one arithmetic expression per player. This makes both members of the winning team top together and makes a draw a shared result.
- Tie-break key weighted 10000/100/1: Counters stay far below 100 in at most 8 rounds, so the weights apply net score, then Interceptions, then Correct Decodes in strict order.
- Clues submitted as one text with ' / ' separators: An answer is a single short text, and the three clues must stay in code order.
- Codes stored on the table with visibility none: A player attribute marked ally would show the code to the Encryptor's own Decoder, which would defeat the game.

## Simplifications

- Codes and guesses are picked from a list of the 24 valid permutations: The engine takes choices from a list, so a malformed code or guess cannot be entered. The referee then judges only the clue rules, and an empty guess still counts as wrong.
- Clue validity is judged by a referee model in one true/false sentence per team: The meaning-only clue rules are too complex for arithmetic. Scoring and the winner remain arithmetic.

## Unsupported (needs engine work)

- none
