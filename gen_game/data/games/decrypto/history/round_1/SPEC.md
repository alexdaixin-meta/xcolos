# Decrypto Duel (Paired Rounds)

Two teams of two take turns sending a secret three-digit code through clues about their own four hidden keywords; the rival Guesser tries to intercept, and a team wins at the end of a pair with 2 Interceptions or when its rival has 2 Miscommunications, otherwise by Interceptions minus Miscommunications.

Players: 4 to 4, best with 4

## Parameters

- `player_count` = 4
- `team_size` = 2
- `keywords_per_team` = 4
- `word_list_size` = 120
- `max_rounds` = 16
- `pairs` = 8
- `code_length` = 3
- `code_digit_max` = 4
- `code_count` = 24
- `clue_max_words` = 3
- `interception_trigger` = 2
- `miscommunication_trigger` = 2
- `first_interception_round` = 3
- `trigger_weight` = 1000

## Round

1. **update** (engine): round_number += 1; pair = (round_number + 1) div 2; enc_team = A if pair % 2 == round_number % 2, else B; in an odd pair encryptor_seat = 1 (A) or 3 (B) and decoder_seat = 2 (A) or 4 (B); in an even pair encryptor_seat = 2 (A) or 4 (B) and decoder_seat = 1 (A) or 3 (B); interceptor_seat = 0 if round_number < 3, otherwise the other team's Guesser (odd pair: 4 if enc_team = A, else 2; even pair: 3 if enc_team = A, else 1); clear my_code for every player; clear revealed_code, decoder_guess, interceptor_guess, current_clues; set clue_valid = false
2. **tell** (all players): announce round_number, enc_team, encryptor_seat and decoder_seat; if interceptor_seat > 0, announce the Interceptor; otherwise announce that there is no interception this round
3. **update** (engine): current_code = one entry of code_list drawn uniformly at random; set my_code of encryptor_seat = current_code
4. **sync** (all players): each player receives their own state; only the Encryptor sees my_code; each player sees their own keywords
5. **ask** (seat encryptor_seat): current_clues = the answer
6. **update** (engine): clue_valid = the referee's ruling (judged: "Each of the three clues in current_clues relates by meaning or association to the keyword (from the encrypting team's keywords) numbered by its digit of current_code, no clue hints by spelling, letters, letter count, rhyme or keyword number or position, no clue contains its keyword or a form of it, and no clue repeats a clue already in the encrypting team's clue history.")
7. **update** (engine): when clue_valid is false: revealed_code = current_code; the encrypting team's miscommunications += 1 (a_miscommunications if enc_team = A, else b_miscommunications); the clues are not added to the history; the guess steps of this round are skipped
8. **tell** (all players): when clue_valid is true: show current_clues to everyone; when clue_valid is false: announce that the clue set was invalid, the code revealed_code, and the Miscommunication
9. **poll** (seat decoder_seat, and seat interceptor_seat when interceptor_seat > 0): when clue_valid is true: decoder_guess = the Decoder's answer; interceptor_guess = the Interceptor's answer (if any); neither sees the other's guess until both are in
10. **update** (engine): when clue_valid is true: revealed_code = current_code; if decoder_guess != current_code, the encrypting team's miscommunications += 1; if interceptor_seat > 0 and interceptor_guess == current_code, the Interceptor's team's interceptions += 1 (b_interceptions if enc_team = A, else a_interceptions); append each clue tagged with its digit to clue_history_a (enc_team = A) or clue_history_b (enc_team = B)
11. **tell** (all players): when clue_valid is true: announce revealed_code, decoder_guess, interceptor_guess (if any) and all four token counts
12. **update** (engine): when round_number % 2 == 0: trig_a = 1 if a_interceptions >= 2 or b_miscommunications >= 2, else 0; trig_b = 1 if b_interceptions >= 2 or a_miscommunications >= 2, else 0; for seats 1-2 standing = (trig_a - trig_b) * 1000 + a_interceptions - a_miscommunications; for seats 3-4 standing = (trig_b - trig_a) * 1000 + b_interceptions - b_miscommunications
13. **check** (engine): end the game if round_number % 2 == 0 and (a_interceptions >= 2 or b_miscommunications >= 2 or b_interceptions >= 2 or a_miscommunications >= 2 or round_number >= 16); otherwise continue

## Ending

- ends when: round_number % 2 == 0 and (a_interceptions >= 2 or b_miscommunications >= 2 or b_interceptions >= 2 or a_miscommunications >= 2 or round_number >= 16)
- ranked by: `you.standing` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their team's trigger edge times 1000 plus the team's Interceptions minus its Miscommunications. A team triggers with 2 or more Interceptions or when the other team has 2 or more Miscommunications. If exactly one team triggers, both its members rank highest and win. If both trigger, or neither has triggered by round 16, the team with the higher Interceptions minus Miscommunications wins. Equal values are a draw: all four players share the win.

## Choices the source did not make

- 4 players, min 4, max 4, suggested 4: The designer fixed two teams of two, one Encryptor and one Guesser each, and the role table names exactly four seats. Fewer seats would break a team, and more have no role.
- Seat mapping: seat 1 = A1, seat 2 = A2, seat 3 = B1, seat 4 = B2: This gives a fixed arithmetic for roles from round_number and pair parity that reproduces the source's role table.
- One engine round equals one game round (16 at most): This lets the end check run after every even round, using a `when` condition on round_number parity.
- Ranking expression: (own trigger - other trigger) * 1000 + Interceptions - Miscommunications: A sole trigger outranks any comparison value (which lies within -16 to 16), while a double trigger or no trigger falls back to the comparison. Equal values share the win, which is the draw.
- The 120-word list's contents are chosen by the implementer: The source names the list's size and kind (common concrete nouns) but not the words.
- No talk phase: The source forbids talk; players communicate only through clues.
- Guesses are chosen from the 24 legal codes: The code space is fixed, so a choice list prevents malformed guesses.

## Simplifications

- The three clues are one text answer separated by ' / ': A single short-text question keeps the clue step to one ask. The referee and the history read the clues in code order.
- Each teammate holds their own copy of the team's keywords as a private player attribute: The engine has no team-visible table attribute, so giving both members the same list gives the same information.
- Clue validity (meaning, no spelling hints, no keyword forms, no repeats) is decided by a referee's true/false ruling: These checks are too complex for arithmetic, which the engine allows to be judged. The tokens that result are still calculated.

## Unsupported (needs engine work)

- none
