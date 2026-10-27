# Variation: Decrypto Duel (Paired Rounds)

Two teams of two run a 4-keyword Decrypto. Rounds are grouped into pairs in which each team encrypts once, and the first mover alternates between pairs. Wins and losses are checked only at the end of a pair, so neither seat has an edge.

Players: 4 to 4, best with 4

## Review of the original

Decrypto is a team word-deduction game. Each team holds four secret keywords. Each round an Encryptor gives three meaning-based clues for a secret 3-digit code. Teammates try to decode it while the opponents try to intercept it from the growing public clue history. Two Interceptions win and two Miscommunications lose.

- **non_degenerate**: weak. No simple policy wins. A fixed decode guess is right 1/24 of the time and loses by about the second encryption. A fixed intercept hits 1/24 and almost never reaches 2. The always-obvious clue is decoded but becomes interceptable as history builds. The previous variation, however, ran the end check after every single round, with Team A always encrypting first. Equal-pace races then resolved against A: about 53.5% against 46.5%, a 7-point seat edge for B. The original Decrypto avoids this by resolving both teams in the same round before checking.
- **skill_sensitive**: good. Results are driven by skill. Good clues must be clear to a partner who shares the keywords, yet vague to an opponent who sees only the history. Good interceptors cross-reference past clues per column. The random code only fixes which digits are clued and does not favour either team.
- **headroom**: good. Clue calibration against a growing public history has no ceiling. A weak team still decodes most of its own codes and can win on the opponent's mistakes.
- **reasoning_dependent**: good. Interceptors infer hidden keywords from scattered clues. Encryptors model what the opponent can already infer and plan clue choices across rounds.
- **verifiable**: good. Code matches are exact digit comparisons and the tokens are public counts. Only clue validity goes to the referee, which the platform allows.
- **fits_platform**: weak. The step, attribute, hidden-element and draw counts are within limits, and the game is text-only and turn-based. The previous variation's Interceptor list contradicted its own stated rule in half the rounds, so a model could not tell who intercepts. It also announced Interceptors in rounds 1 and 2, when none exist.

## Problems

- Seat edge: the end check ran after every round while Team A always encrypted first. Equal-pace failure races therefore went against A, giving B about a 7-point advantage.
- Second-mover information edge: within any fixed pairing, the team that encrypts second sees the other team's result first and can adjust its risk.
- Ambiguous roles: the Interceptor definition and the Interceptor list disagreed in rounds 5-8 and 13-16.
- Minor: the round announcement named Interceptors in rounds 1-2, where interception does not happen.
- The rules claimed that win conditions cannot conflict. Once checks are done per pair this claim is false, and no rule covered both teams triggering a win together.

## Changes

- Group rounds into pairs (rounds 1-2, 3-4, ... 15-16) in which each team encrypts once. Run the end check only after the second round of each pair. (fixes: Seat edge: the end check ran after every round while Team A always encrypted first. Equal-pace failure races therefore went against A, giving B about a 7-point advantage.): Both teams then have the same number of encryptions and interception chances before any win or loss is checked. This restores the original's same-round symmetry.
- Alternate which team encrypts first in a pair: Team A in odd pairs, Team B in even pairs. (fixes: Second-mover information edge: within any fixed pairing, the team that encrypts second sees the other team's result first and can adjust its risk.): Each team is the second mover equally often, so neither team gets the information edge more often.
- Replace the Interceptor rule with fixed per-pair roles. In each pair, each team has one Encryptor and one Guesser. The Guesser decodes their own team's code and intercepts the other team's. Odd pairs: A1 and B1 encrypt. Even pairs: A2 and B2 encrypt. A full table is given. (fixes: Ambiguous roles: the Interceptor definition and the Interceptor list disagreed in rounds 5-8 and 13-16.): This gives one simple rule, stated both as a principle and as a table that agree. Every player has a role in every pair.
- The announcement in rounds 1-2 names the Encryptor and Decoder only, and states that there is no interception. (fixes: Minor: the round announcement named Interceptors in rounds 1-2, where interception does not happen.): This removes the contradiction between the announcement and the interception rule.
- Define that a team 'triggers' when it has 2 or more Interceptions, or when the other team has 2 or more Miscommunications. If exactly one team triggers at a pair check, it wins. If both trigger, the team with the higher Interceptions minus Miscommunications wins, and equal values are a draw. (fixes: The rules claimed that win conditions cannot conflict. Once checks are done per pair this claim is false, and no rule covered both teams triggering a win together.): This handles simultaneous triggers arithmetically and removes the false claim.

## Kept from the original

- Two teams with four secret numbered keywords each.
- A random 3-digit code of different digits 1-4, clued by meaning.
- A public clue history per keyword column, which makes interception possible over time.
- Two Interceptions win and two Miscommunications lose.
- Encryptors rotate within a team, and there is no interception in the first round of each team.
- Clues are the only communication channel.

## The variation's rules

SETUP
- There are 4 players: Team A (A1, A2) and Team B (B1, B2).
- The engine deals each team 4 different keywords from a fixed list of 120 common concrete nouns. No word is given to both teams.
- A team's keywords are numbered 1 to 4. They are shown privately to both members of that team and never to the other team.
- A public clue history shows, for each team, four columns (keywords 1-4) that start empty.
- Each team starts with 0 Interceptions and 0 Miscommunications. Token counts are always public.

PAIRS AND ROLES
- The game has up to 16 rounds, grouped into 8 pairs: pair 1 = rounds 1-2, pair 2 = rounds 3-4, ..., pair 8 = rounds 15-16.
- In each pair, each team encrypts exactly once.
- In odd pairs (1, 3, 5, 7), Team A encrypts in the first round of the pair and Team B in the second.
- In even pairs (2, 4, 6, 8), Team B encrypts first and Team A second.
- In each pair, each team has one Encryptor and one Guesser:
  - Odd pairs: A1 and B1 are Encryptors; A2 and B2 are Guessers.
  - Even pairs: A2 and B2 are Encryptors; A1 and B1 are Guessers.
- In a round where a team encrypts:
  - The Encryptor is that team's Encryptor for the pair.
  - The Decoder is that team's Guesser.
  - The Interceptor is the other team's Guesser.
  - The other team's Encryptor only watches.
- Full table (round: Encryptor / Decoder / Interceptor):
  - R1: A1 / A2 / none
  - R2: B1 / B2 / none
  - R3: B2 / B1 / A1
  - R4: A2 / A1 / B1
  - R5: A1 / A2 / B2
  - R6: B1 / B2 / A2
  - R7: B2 / B1 / A1
  - R8: A2 / A1 / B1
  - R9: A1 / A2 / B2
  - R10: B1 / B2 / A2
  - R11: B2 / B1 / A1
  - R12: A2 / A1 / B1
  - R13: A1 / A2 / B2
  - R14: B1 / B2 / A2
  - R15: B2 / B1 / A1
  - R16: A2 / A1 / B1

EACH ROUND
1. The engine announces the round number, the encrypting team, the Encryptor and the Decoder. In rounds 3-16 it also announces the Interceptor. In rounds 1 and 2 it announces that there is no interception.
2. The engine draws a code uniformly at random from the 24 ordered sequences of three different digits from 1 to 4 (for example 3-1-4). It shows the code privately to the Encryptor only.
3. The Encryptor writes three clues, one per digit, in code order. Each clue points to the keyword with that number and is at most 3 words.
4. Referee check. The clue set is valid only if all of these hold:
   - Every clue relates to its keyword by meaning or association.
   - No clue hints by spelling, letters, letter count, rhyme, or keyword number or position.
   - No clue contains its keyword or a form of it.
   - No clue repeats any clue this team has used before.
   If the set is invalid:
   - The code is revealed to everyone.
   - The encrypting team gains 1 Miscommunication.
   - The clues are not added to the history.
   - The round goes to step 8.
5. The valid clues are shown to all players.
6. At the same moment, the Decoder privately submits a guessed 3-digit code and the Interceptor (if any) privately submits a guessed 3-digit code.
7. The true code and the guesses are revealed, then scored:
   - If the Decoder's guess differs from the true code in any digit, the encrypting team gains 1 Miscommunication.
   - If the Interceptor's guess equals the true code exactly, the Interceptor's team gains 1 Interception.
   - Each clue is added to the encrypting team's public history column for the keyword it clued.
8. End check, only in even-numbered rounds (the end of a pair). In odd-numbered rounds, play continues.
   - A team TRIGGERS if it has 2 or more Interceptions, or if the other team has 2 or more Miscommunications.
   - If exactly one team triggers, it wins and the game ends.
   - If both teams trigger, apply the comparison rule and the game ends.
   - If neither team triggers and this was round 16, apply the comparison rule.
   - Otherwise play continues.

COMPARISON RULE
- Each team's value is its Interceptions minus its Miscommunications.
- The higher value wins. Equal values are a draw.

COMMUNICATION
- There is no talk phase. Players communicate only through clues. Teammates may not message each other.

Objective: The winner is decided only at the end of an even-numbered round. A team triggers if it holds 2 or more Interceptions or if the opponent holds 2 or more Miscommunications. If exactly one team triggers, it wins. If both trigger, or if neither has triggered by the end of round 16, each team's value is its Interceptions minus its Miscommunications: the higher value wins and equal values are a draw. Both members of a team share its result.

Expected effect: Both teams always have had the same number of encryptions and interception chances when the game is checked. Alternating the first mover each pair spreads the small advantage of seeing the other team's result first equally between the teams. Removing the 7-point structural edge should bring win rates for equal-skill teams near 50/50, with some draws. Fixed Encryptor/Guesser roles make every player's job unambiguous. The strategic core is unchanged: clue clearly enough for a partner but vaguely enough to survive a reader of the public history. Talk is left out because the two teams' interests are directly opposed and teammate talk would bypass the cluing that is the game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 16 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
