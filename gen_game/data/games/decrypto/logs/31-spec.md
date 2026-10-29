# 31 spec

- time: 2026-10-27T21:39:58+00:00 (65.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 17120eb6d9183c29, reply sha256 7f96fc18f20979be

## Sent

````
Game: Decrypto: Points Race
Players in the source: 4 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP. Four players: seats 1 and 2 form team Red, seats 3 and 4 form team Blue. Eight distinct keywords are drawn at random from a fixed list of 40 common nouns. The first four go to Red, numbered 1-4; the next four go to Blue, numbered 1-4. Each team's keywords are shown only to that team's two players. Each team starts with 0 points, 0 exact interceptions and 0 exact decodes. A public history lists, for each team and each past round, its three clues and its revealed true code.

CODES. A code is three different digits from 1-4 in order. There are 24 codes, offered in this order: 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432.

ROLES. In odd rounds, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders. In even rounds, the roles swap.

EACH ROUND (8 rounds):
1. Roles for the round are announced.
2. Code choice (simultaneous, secret): each Encryptor chooses one of the 24 codes for their team. No one else sees it.
3. Clues (simultaneous): each Encryptor writes three clues, one per digit of the code in order. Clue 1 should point to the team keyword numbered by the first digit, and so on.
4. Clue check. A clue is valid only if all of these hold: it is a single word with no spaces; it is 2-20 letters long; ignoring case, it does not contain any of the team's own four keywords and is not contained in any of them; it is not identical, ignoring case, to any clue either team has given in an earlier round. A team with any invalid clue this round is marked invalid.
5. All six clues are shown to everyone.
6. Guesses (simultaneous): each Decoder chooses one of the 24 codes as a decode of their own team's clues. Each Encryptor chooses one of the 24 codes as an interception of the opposing team's clues.
7. Decode scoring, for each team that is not invalid: the team gains 1 point for each position (first, second, third) where the Decoder's guess matches the team's true code. If all three match, the team gains 1 more point and 1 exact decode. A team marked invalid gains 0 decode points this round.
8. Interception scoring, rounds 2-8 only: each team gains 1 point for each position where its Encryptor's interception matches the opposing team's true code. If all three match, the team gains 2 more points and 1 exact interception. In round 1 interceptions score nothing.
9. Invalid penalty: if a team is marked invalid, the opposing team gains 3 points.
10. Both true codes, all guesses and all points gained are announced, and the clues and codes are added to the public history.

No other talk is allowed. The clues are the only communication.

END. After round 8 the game ends.

How the winner is decided: The team with more points after round 8 wins, and both of its players win. If points are tied, the team with more exact interceptions wins. If still tied, the team with more exact decodes wins. If still tied, the game is a draw.
````

## Reply

````
```json
{
  "name": "Decrypto: Points Race",
  "summary": "Two teams of two take turns encrypting three-digit codes as word clues for a partner who knows the team's secret keywords, while the rival team tries to intercept; points over 8 rounds decide the winning team.",
  "players": {"min": 4, "max": 4, "suggested": 4},
  "parameters": {
    "rounds": 8,
    "seats": 4,
    "team_size": 2,
    "keyword_list_size": 40,
    "keywords_per_team": 4,
    "code_length": 3,
    "code_digit_min": 1,
    "code_digit_max": 4,
    "code_count": 24,
    "clues_per_team_per_round": 3,
    "clue_min_letters": 2,
    "clue_max_letters": 20,
    "decode_points_per_position": 1,
    "exact_decode_bonus_points": 1,
    "exact_decode_count_gain": 1,
    "intercept_points_per_position": 1,
    "exact_intercept_bonus_points": 2,
    "exact_intercept_count_gain": 1,
    "first_scoring_interception_round": 2,
    "invalid_penalty_points": 3,
    "starting_points": 0
  },
  "attributes": {
    "player": [
      {"key": "team", "type": "text", "visible": "public", "initial": "seats 1,2: Red; seats 3,4: Blue", "meaning": "the player's team", "observable": true},
      {"key": "keywords", "type": "list", "visible": "ally", "initial": [], "meaning": "the team's four keywords in order (position 1-4 is keyword number 1-4); both teammates hold the same list", "observable": false},
      {"key": "role", "type": "text", "visible": "public", "initial": "", "meaning": "Encryptor or Decoder for the current round", "observable": true},
      {"key": "guess", "type": "text", "visible": "ally", "initial": "", "meaning": "this round's guessed code: a decode of the own team's clues for a Decoder, an interception of the opposing clues for an Encryptor", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "the team's points (kept equal for both teammates)", "observable": true},
      {"key": "exact_interceptions", "type": "number", "visible": "public", "initial": 0, "meaning": "the team's exact interceptions (kept equal for both teammates)", "observable": true},
      {"key": "exact_decodes", "type": "number", "visible": "public", "initial": 0, "meaning": "the team's exact decodes (kept equal for both teammates)", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 1, "meaning": "current round number, 1-8", "observable": true},
      {"key": "word_list", "type": "list", "visible": "none", "initial": ["apple","river","castle","dragon","piano","rocket","garden","window","mirror","candle","forest","bridge","anchor","pencil","tiger","cloud","engine","island","ladder","moon","needle","orange","pirate","queen","robot","shadow","tower","umbrella","violin","whale","bottle","camera","desert","feather","glove","hammer","jungle","kettle","lemon","mountain"], "meaning": "the fixed list of 40 nouns that keywords are drawn from", "observable": false},
      {"key": "codes", "type": "list", "visible": "public", "initial": ["123","124","132","134","142","143","213","214","231","234","241","243","312","314","321","324","341","342","412","413","421","423","431","432"], "meaning": "the 24 legal codes in offer order", "observable": false},
      {"key": "red_code", "type": "text", "visible": "none", "initial": "", "meaning": "Red's true code this round; revealed at step 10", "observable": false},
      {"key": "blue_code", "type": "text", "visible": "none", "initial": "", "meaning": "Blue's true code this round; revealed at step 10", "observable": false},
      {"key": "red_clues", "type": "list", "visible": "none", "initial": [], "meaning": "Red's three clues this round, in code order; revealed at step 5", "observable": false},
      {"key": "blue_clues", "type": "list", "visible": "none", "initial": [], "meaning": "Blue's three clues this round, in code order; revealed at step 5", "observable": false},
      {"key": "red_invalid", "type": "bool", "visible": "public", "initial": false, "meaning": "Red gave an invalid clue this round", "observable": true},
      {"key": "blue_invalid", "type": "bool", "visible": "public", "initial": false, "meaning": "Blue gave an invalid clue this round", "observable": true},
      {"key": "red_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Red's points (mirrors seats 1-2 score)", "observable": true},
      {"key": "blue_points", "type": "number", "visible": "public", "initial": 0, "meaning": "Blue's points (mirrors seats 3-4 score)", "observable": true},
      {"key": "red_gain", "type": "number", "visible": "public", "initial": 0, "meaning": "points Red gained this round (announced at step 10)", "observable": false},
      {"key": "blue_gain", "type": "number", "visible": "public", "initial": 0, "meaning": "points Blue gained this round (announced at step 10)", "observable": false},
      {"key": "history", "type": "list", "visible": "public", "initial": [], "meaning": "public record: for each past round and team, its three clues and its true code", "observable": true}
    ]
  },
  "setup": [
    "Seats 1 and 2 are team Red; seats 3 and 4 are team Blue.",
    "Draw 8 distinct nouns at random from word_list, removing each from word_list as it is drawn.",
    "The first four drawn, in draw order, become keywords 1-4 of seats 1 and 2 (Red); the next four become keywords 1-4 of seats 3 and 4 (Blue). keywords is ally, so each team sees only its own.",
    "Every player's score, exact_interceptions and exact_decodes start at 0; red_points and blue_points start at 0; history starts empty; round is 1.",
    "Sync: each player is sent their own state, including their team's keywords."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "If round is odd: role = Encryptor for seats 1 and 3, Decoder for seats 2 and 4. If round is even: role = Encryptor for seats 2 and 4, Decoder for seats 1 and 3. Reset red_invalid, blue_invalid to false, red_gain, blue_gain to 0, and every guess to empty."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Round {round}: the Encryptors are seats {red encryptor} (Red) and {blue encryptor} (Blue); the Decoders are seats {red decoder} (Red) and {blue decoder} (Blue).'"},
    {"action": "poll", "who": "the two Encryptors", "answer": "one of the 24 codes, from codes", "effect": "Red Encryptor's answer is set into red_code; Blue Encryptor's answer is set into blue_code (both hidden from all players, including the Decoder teammate)."},
    {"action": "poll", "who": "the two Encryptors", "answer": "short text: three clues separated by commas, clue 1 for the keyword numbered by the code's first digit, clue 2 for the second, clue 3 for the third", "effect": "Red Encryptor's three clues are set into red_clues and Blue Encryptor's into blue_clues, in order."},
    {"action": "update", "who": "Red", "answer": null, "effect": "red_invalid = true if the referee rules the sentence false; otherwise it stays false.", "judged": "Each of Red's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Red's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."},
    {"action": "update", "who": "Blue", "answer": null, "effect": "blue_invalid = true if the referee rules the sentence false; otherwise it stays false.", "judged": "Each of Blue's three clues this round is a single word with no spaces, 2 to 20 letters long, does not contain (ignoring case) any of Blue's four keywords and is not contained in any of them, and is not identical (ignoring case) to any clue in history."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce all six clues: 'Red clues: {red_clues}. Blue clues: {blue_clues}.'"},
    {"action": "poll", "who": "all players", "answer": "one of the 24 codes, from codes", "effect": "Each Decoder's answer (a decode of their own team's clues) and each Encryptor's answer (an interception of the opposing team's clues) is stored in that player's guess."},
    {"action": "update", "who": "both teams", "answer": null, "effect": "Decode scoring. For Red, if red_invalid is false: matches = the number of positions 1-3 where the Red Decoder's guess digit equals red_code's digit; red_gain += matches; if matches == 3, red_gain += 1 and exact_decodes += 1 for seats 1 and 2. For Blue, the same with blue_invalid, the Blue Decoder's guess and blue_code, with exact_decodes added for seats 3 and 4. An invalid team gains 0 here."},
    {"action": "update", "who": "both teams", "answer": null, "effect": "Interception scoring, only when round >= 2. Red: matches = the number of positions where the Red Encryptor's guess equals blue_code; red_gain += matches; if matches == 3, red_gain += 2 and exact_interceptions += 1 for seats 1 and 2. Blue: the same with the Blue Encryptor's guess against red_code, adding to blue_gain and to seats 3 and 4. When round == 1, nothing changes."},
    {"action": "update", "who": "both teams", "answer": null, "effect": "Invalid penalty: if red_invalid, blue_gain += 3; if blue_invalid, red_gain += 3. Then red_points += red_gain and blue_points += blue_gain; score of seats 1,2 = red_points; score of seats 3,4 = blue_points."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Append to history: 'Round {round} Red clues {red_clues}, code {red_code}; Blue clues {blue_clues}, code {blue_code}'."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Red's code was {red_code}, Blue's was {blue_code}. Guesses: seat 1 {guess}, seat 2 {guess}, seat 3 {guess}, seat 4 {guess}. Red invalid: {red_invalid}; Blue invalid: {blue_invalid}. Red gained {red_gain} (total {red_points}); Blue gained {blue_gain} (total {blue_points}).'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1"},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round > 8; otherwise repeat the round."}
  ],
  "ending": {
    "condition": "round > 8",
    "rank_by": "you.score * 10000 + you.exact_interceptions * 100 + you.exact_decodes",
    "decided_by": "Each player stands on their team's points, then its exact interceptions, then its exact decodes. The team that is higher wins and both its players win. If both teams are level on all three, all four players share the result as a draw."
  },
  "rules": [
    {"id": "R1", "text": "At setup, seats 1 and 2 are team Red and seats 3 and 4 are team Blue."},
    {"id": "R2", "text": "At setup, 8 distinct keywords are drawn at random from the 40-noun word_list: the first 4 become Red's keywords 1-4 and the next 4 become Blue's keywords 1-4."},
    {"id": "R3", "text": "A team's keywords are visible to its own two players only, never to the opposing team."},
    {"id": "R4", "text": "At setup, each team has 0 points, 0 exact interceptions and 0 exact decodes."},
    {"id": "R5", "text": "When the round is odd, seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders."},
    {"id": "R6", "text": "When the round is even, seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders."},
    {"id": "R7", "text": "Each round, each Encryptor secretly chooses one of the 24 codes (three different digits from 1-4), and no other player, including the teammate, sees it before step 10."},
    {"id": "R8", "text": "Each round, each Encryptor writes exactly three clues, one per digit of their code, in order."},
    {"id": "R9", "text": "When any of a team's clues has a space, has fewer than 2 or more than 20 letters, contains or is contained in one of the team's own keywords (ignoring case), or repeats a clue from an earlier round (ignoring case), that team is marked invalid for the round."},
    {"id": "R10", "text": "All six clues are shown to all four players before guesses are made."},
    {"id": "R11", "text": "Guesses are simultaneous: each Decoder picks one of the 24 codes as a decode of their own team's clues, and each Encryptor picks one of the 24 codes as an interception of the opposing team's clues."},
    {"id": "R12", "text": "When a team is not invalid, it gains 1 point for each position where its Decoder's guess matches its true code (e.g. guess 123 against code 132 gains 1)."},
    {"id": "R13", "text": "When a team's Decoder's guess matches all three positions and the team is not invalid, the team gains 3 + 1 = 4 points and 1 exact decode."},
    {"id": "R14", "text": "When a team is marked invalid, it gains 0 decode points that round even if its Decoder's guess is correct."},
    {"id": "R15", "text": "In rounds 2-8, a team gains 1 point for each position where its Encryptor's interception matches the opposing team's true code."},
    {"id": "R16", "text": "In rounds 2-8, when a team's interception matches all three positions, the team gains 3 + 2 = 5 points and 1 exact interception."},
    {"id": "R17", "text": "In round 1, interceptions score 0 points and add no exact interceptions."},
    {"id": "R18", "text": "When a team is marked invalid, the opposing team gains 3 points."},
    {"id": "R19", "text": "At the end of each round, both true codes, all four guesses and each team's points gained are announced, and both teams' clues and codes are appended to the public history."},
    {"id": "R20", "text": "Both players on a team always have the same score, exact_interceptions and exact_decodes."},
    {"id": "R21", "text": "The game ends after round 8."},
    {"id": "R22", "text": "When the game ends, the team with more points wins; if points are tied, the team with more exact interceptions wins; if still tied, the team with more exact decodes wins; if still tied, it is a draw and all four players share the result."},
    {"id": "R23", "text": "Players have no talk step: the clues are the only communication."}
  ],
  "offers": [
    {"question": "Code choice", "who": "the two Encryptors of the round (seats 1 and 3 in odd rounds, seats 2 and 4 in even rounds)", "options": "each Encryptor: the 24 codes 123, 124, 132, 134, 142, 143, 213, 214, 231, 234, 241, 243, 312, 314, 321, 324, 341, 342, 412, 413, 421, 423, 431, 432; Decoders are not asked"},
    {"question": "Clues", "who": "the two Encryptors of the round", "options": "each Encryptor: short free text with three clues separated by commas; Decoders are not asked"},
    {"question": "Guesses", "who": "all four seats", "options": "a Decoder: the 24 codes, as a decode of their own team's clues; an Encryptor: the 24 codes, as an interception of the opposing team's clues (asked in round 1 too, though it scores nothing)"}
  ],
  "choices": [
    {"what": "4 players (min 4, max 4, suggested 4)", "why": "The designer fixed two teams of two. The game needs an Encryptor and a Decoder on each side, so the minimum is 4. More seats would break the fixed role swap and the team structure, so the maximum is not larger. The strategy is to give clues obvious to a teammate who knows the keywords but opaque to rivals who read the growing history, and to read the rivals' clue patterns to intercept."},
    {"what": "The 40-noun word list", "why": "The source says a fixed list of 40 common nouns but does not name them, so a concrete list was chosen."},
    {"what": "No talk step", "why": "The source forbids all talk other than the clues."},
    {"what": "Clues are entered as one comma-separated text answer", "why": "The engine takes one short text per question, and the three clues belong to one simultaneous step."},
    {"what": "Ranking is score * 10000 + exact_interceptions * 100 + exact_decodes", "why": "This encodes the source's tie-break order in one expression. Exact counts never exceed 8, so the weights cannot overlap. A full tie shares the win, which is the source's draw."},
    {"what": "Interception guesses are still asked in round 1", "why": "The source has every Encryptor choose an interception every round and only says round 1 interceptions score nothing."}
  ],
  "simplifications": [
    {"what": "True codes are stored as hidden table attributes (red_code, blue_code) rather than on the Encryptor", "why": "A player's hidden attribute is visible to the whole team, but the source says no one else, including the Decoder teammate, may see the code."},
    {"what": "Team points are mirrored onto both teammates' score, exact_interceptions and exact_decodes", "why": "The ending ranks players, so each player carries the team totals in order to win or lose together."},
    {"what": "Clue validity is ruled by a referee from one sentence", "why": "Word, letter-count, substring and history-repeat checks on free text are beyond plain arithmetic. All scoring stays arithmetic."}
  ],
  "unsupported": []
}
```
````
