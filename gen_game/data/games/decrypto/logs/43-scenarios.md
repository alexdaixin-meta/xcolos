# 43 scenarios

- time: 2026-10-27T21:54:43+00:00 (65.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 effd44e1aece5adf, reply sha256 84838c270617caa6

## Sent

````
SPEC:
{
  "name": "Decrypto Duel",
  "summary": "Two teams of two take turns giving three meaning-only clues to a secret 3-digit code over their team's four hidden keywords. Teammates must decode their own code while the rival team tries to intercept it.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "player_count": 4,
    "team_size": 2,
    "word_list_size": 40,
    "keywords_per_team": 4,
    "code_length": 3,
    "code_digit_min": 1,
    "code_digit_max": 4,
    "max_rounds": 8,
    "interception_limit": 2,
    "miscommunication_limit": 2,
    "first_intercept_round": 2,
    "correct_decode_gain": 1,
    "miscommunication_gain": 1,
    "interception_gain": 1
  },
  "attributes": {
    "player": [
      {
        "key": "team",
        "type": "text",
        "visible": "public",
        "initial": "white for seats 1-2, black for seats 3-4",
        "meaning": "the player's team",
        "observable": true
      },
      {
        "key": "team_sign",
        "type": "number",
        "visible": "public",
        "initial": "1 for seats 1-2, -1 for seats 3-4",
        "meaning": "+1 for White, -1 for Black, used to rank by the table result",
        "observable": false
      },
      {
        "key": "keywords",
        "type": "list",
        "visible": "ally",
        "initial": "[] (dealt in setup)",
        "meaning": "the team's 4 keywords in order 1-4, the same list for both teammates, never changing",
        "observable": false
      },
      {
        "key": "role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "encryptor or decoder this round",
        "observable": false
      },
      {
        "key": "guess",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "this round's code guess, as one of the 24 permutations such as 3-1-4",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "the 40 words: apple, anchor, bridge, candle, castle, cloud, crown, desert, diamond, dragon, drum, eagle, engine, feather, forest, ghost, glacier, hammer, island, jungle, key, ladder, lantern, mirror, moon, needle, ocean, piano, pirate, pyramid, rocket, saddle, shadow, ship, snake, spider, sword, tiger, volcano, whistle",
        "meaning": "undealt words",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number",
        "observable": true
      },
      {
        "key": "white_code",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "White's secret code this round, until it is revealed in history",
        "observable": false
      },
      {
        "key": "black_code",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Black's secret code this round, until it is revealed in history",
        "observable": false
      },
      {
        "key": "white_clues",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "White's three clues this round, in code order, separated by ' / '",
        "observable": true
      },
      {
        "key": "black_clues",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Black's three clues this round, in code order, separated by ' / '",
        "observable": true
      },
      {
        "key": "white_valid",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "whether White's encryption was ruled valid this round",
        "observable": false
      },
      {
        "key": "black_valid",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "whether Black's encryption was ruled valid this round",
        "observable": false
      },
      {
        "key": "white_interceptions",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "White's Interceptions",
        "observable": true
      },
      {
        "key": "white_miscommunications",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "White's Miscommunications",
        "observable": true
      },
      {
        "key": "white_decodes",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "White's Correct Decodes",
        "observable": true
      },
      {
        "key": "black_interceptions",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Black's Interceptions",
        "observable": true
      },
      {
        "key": "black_miscommunications",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Black's Miscommunications",
        "observable": true
      },
      {
        "key": "black_decodes",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Black's Correct Decodes",
        "observable": true
      },
      {
        "key": "history",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "for each finished round: each team's three clues and true code",
        "observable": true
      },
      {
        "key": "result",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "+1 if White currently wins by the winner rules, -1 if Black does, 0 if it is a draw",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats 1 and 2 get team = white and team_sign = 1; seats 3 and 4 get team = black and team_sign = -1.",
    "The engine draws 4 different words at random from deck, removing each from deck, into seat 1's keywords as keywords 1-4, and copies that list into seat 2's keywords.",
    "The engine draws 4 more different words at random from deck, removing each from deck, into seat 3's keywords as keywords 1-4, and copies that list into seat 4's keywords.",
    "All six team counters start at 0, history starts empty and round starts at 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; if round is odd, seats 1 and 3 get role = encryptor and seats 2 and 4 get role = decoder; if round is even, seats 2 and 4 get role = encryptor and seats 1 and 3 get role = decoder; set white_valid = true and black_valid = true; announce the round number and each team's Encryptor and Decoder."
    },
    {
      "action": "poll",
      "who": "the two players with role = encryptor",
      "answer": "one of the 24 codes of three different digits from 1 to 4: 1-2-3, 1-2-4, 1-3-2, 1-3-4, 1-4-2, 1-4-3, 2-1-3, 2-1-4, 2-3-1, 2-3-4, 2-4-1, 2-4-3, 3-1-2, 3-1-4, 3-2-1, 3-2-4, 3-4-1, 3-4-2, 4-1-2, 4-1-3, 4-2-1, 4-2-3, 4-3-1, 4-3-2",
      "effect": "the White Encryptor's answer is stored in white_code and the Black Encryptor's in black_code (both hidden)."
    },
    {
      "action": "poll",
      "who": "the two players with role = encryptor",
      "answer": "short text: three clues in code order, separated by ' / '",
      "effect": "the White Encryptor's text is stored in white_clues and the Black Encryptor's in black_clues."
    },
    {
      "action": "update",
      "who": "the White Encryptor",
      "answer": null,
      "effect": "if judged false: white_valid = false and white_miscommunications += 1.",
      "judged": "White's three clues in white_clues each point to the White keyword numbered by the matching digit of white_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue White used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information."
    },
    {
      "action": "update",
      "who": "the Black Encryptor",
      "answer": null,
      "effect": "if judged false: black_valid = false and black_miscommunications += 1.",
      "judged": "Black's three clues in black_clues each point to the Black keyword numbered by the matching digit of black_code by general meaning only, and none uses spelling, letters, sound, rhyme, length or alphabetical position, contains the keyword or part of it or a same-root word, repeats word for word a clue Black used in an earlier round of history, refers to the game itself (seats, rounds, codes, digits, keyword numbers, earlier clues, the other team's words), or refers to private information."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "show white_clues and black_clues to all four players at once; codes stay secret."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of the 24 codes of three different digits from 1 to 4 (decoders guess their own team's code, encryptors guess the opposing team's code)",
      "effect": "each player's answer is stored in their guess; no answer leaves guess empty, which never matches."
    },
    {
      "action": "update",
      "who": "the two decoders",
      "answer": null,
      "effect": "when white_valid: if the White decoder's guess == white_code then white_decodes += 1, else white_miscommunications += 1. When black_valid: if the Black decoder's guess == black_code then black_decodes += 1, else black_miscommunications += 1. A team with valid = false is not scored here."
    },
    {
      "action": "update",
      "who": "the two encryptors",
      "answer": null,
      "effect": "when round >= 2: if the White encryptor's guess == black_code then white_interceptions += 1; if the Black encryptor's guess == white_code then black_interceptions += 1 (regardless of validity)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "append to history an entry {round, white_clues, white_code, black_clues, black_code} and announce both true codes to everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "compute result: let WQ = (white_interceptions >= 2 and white_miscommunications < 2), BQ = (black_interceptions >= 2 and black_miscommunications < 2), WM = (white_miscommunications >= 2), BM = (black_miscommunications >= 2). If WQ and not BQ then result = 1; else if BQ and not WQ then result = -1; else if BM and not WM then result = 1; else if WM and not BM then result = -1; else let K = (white_interceptions - white_miscommunications - black_interceptions + black_miscommunications) * 10000 + (white_interceptions - black_interceptions) * 100 + (white_decodes - black_decodes), and result = 1 if K > 0, -1 if K < 0, 0 if K == 0."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "white_interceptions >= 2 or black_interceptions >= 2 or white_miscommunications >= 2 or black_miscommunications >= 2 or round >= 8",
    "rank_by": "you.team_sign * result",
    "decided_by": "result is +1 if White wins by the ordered rules (sole team with 2+ Interceptions and fewer than 2 Miscommunications; else the sole team without 2+ Miscommunications; else higher Interceptions minus Miscommunications, then more Interceptions, then more Correct Decodes), -1 if Black wins, and 0 on a draw. Both members of the winning team score 1 and win together. On a draw all four score 0 and share the result."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When setup runs, then seats 1 and 2 are Team White, seats 3 and 4 are Team Black, and each team receives 4 different words from the 40-word list, so 8 distinct words are dealt in total."
    },
    {
      "id": "R2",
      "text": "When keywords are dealt, then both members of a team hold the same keyword list, it is visible only to them, and it never changes."
    },
    {
      "id": "R3",
      "text": "When a round is odd (1, 3, 5, 7), then seats 1 and 3 are Encryptors and seats 2 and 4 are Decoders."
    },
    {
      "id": "R4",
      "text": "When a round is even (2, 4, 6, 8), then seats 2 and 4 are Encryptors and seats 1 and 3 are Decoders."
    },
    {
      "id": "R5",
      "text": "When the Encryptors submit, then only Encryptors are asked, simultaneously, for a code of three different digits from 1 to 4 and three clues in code order."
    },
    {
      "id": "R6",
      "text": "When the referee rules a team's clues invalid, then that team gains exactly 1 Miscommunication and its decode is not scored that round, with no further Miscommunication and no Correct Decode."
    },
    {
      "id": "R7",
      "text": "When clues are revealed, then both teams' clues are shown to all four players and both codes stay hidden until the history step."
    },
    {
      "id": "R8",
      "text": "When guesses are taken, then all four players answer simultaneously: decoders guess their own team's code and encryptors guess the opposing team's code."
    },
    {
      "id": "R9",
      "text": "When a valid team's Decoder guess equals its true code digit by digit, then that team gains 1 Correct Decode; otherwise it gains 1 Miscommunication."
    },
    {
      "id": "R10",
      "text": "When round >= 2 and an Encryptor's guess equals the opposing team's true code digit by digit, then the Encryptor's team gains 1 Interception, whether or not the opposing team's clues were valid."
    },
    {
      "id": "R11",
      "text": "When it is round 1, then Encryptors' guesses are ignored and no Interception can be scored."
    },
    {
      "id": "R12",
      "text": "When a player gives no answer to the guess, then it counts as a wrong guess."
    },
    {
      "id": "R13",
      "text": "When a round's scoring finishes, then both true codes are shown to everyone and appended to history beside that round's clues."
    },
    {
      "id": "R14",
      "text": "When, after a round, any team has 2 or more Interceptions or 2 or more Miscommunications, or round 8 has finished, then the game ends."
    },
    {
      "id": "R15",
      "text": "When the game ends and exactly one team has 2 or more Interceptions with fewer than 2 Miscommunications, then that team wins."
    },
    {
      "id": "R16",
      "text": "When rule R15 does not decide it and exactly one team has 2 or more Miscommunications, then the other team wins."
    },
    {
      "id": "R17",
      "text": "When neither R15 nor R16 decides, then the team with the higher Interceptions minus Miscommunications wins; if tied, the team with more Interceptions wins; if still tied, the team with more Correct Decodes wins; if still tied, it is a draw."
    },
    {
      "id": "R18",
      "text": "When the game is running, then there is no discussion phase, and teammates communicate only through official clues."
    }
  ],
  "offers": [
    {
      "question": "Encrypt: choose your secret code",
      "who": "the two seats with role = encryptor (seats 1 and 3 in odd rounds, seats 2 and 4 in even rounds)",
      "options": "any of the 24 orderings of three different digits from 1 to 4; decoders are not asked"
    },
    {
      "question": "Encrypt: give three clues in code order",
      "who": "the two encryptor seats",
      "options": "free short text with three clues separated by ' / '"
    },
    {
      "question": "Guess a code",
      "who": "all four seats",
      "options": "any of the 24 orderings of three different digits from 1 to 4 (a decoder guesses their own team's code, an encryptor guesses the opposing team's code; in round 1 encryptors are still offered these, but their answers are ignored)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players, suggested 4",
      "why": "The designer fixed two teams of two (one Encryptor and one Decoder each), and the roles and teams depend on exactly these seats."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid any discussion phase; teammates may communicate only through clues."
    },
    {
      "what": "Winner computed as a table attribute result in {+1, 0, -1}, ranked by you.team_sign * result",
      "why": "Ranking must be one arithmetic expression per player. This makes both members of the winning team top together and makes a draw a shared result."
    },
    {
      "what": "Tie-break key weighted 10000/100/1",
      "why": "Counters stay far below 100 in at most 8 rounds, so the weights apply net score, then Interceptions, then Correct Decodes in strict order."
    },
    {
      "what": "Clues submitted as one text with ' / ' separators",
      "why": "An answer is a single short text, and the three clues must stay in code order."
    },
    {
      "what": "Codes stored on the table with visibility none",
      "why": "A player attribute marked ally would show the code to the Encryptor's own Decoder, which would defeat the game."
    }
  ],
  "simplifications": [
    {
      "what": "Codes and guesses are picked from a list of the 24 valid permutations",
      "why": "The engine takes choices from a list, so a malformed code or guess cannot be entered. The referee then judges only the clue rules, and an empty guess still counts as wrong."
    },
    {
      "what": "Clue validity is judged by a referee model in one true/false sentence per team",
      "why": "The meaning-only clue rules are too complex for arithmetic. Scoring and the winner remain arithmetic."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: team; table: round, white_clues, black_clues, white_interceptions, white_miscommunications, white_decodes, black_interceptions, black_miscommunications, black_decodes, history, result.
````

## Reply

````
[
{"name":"Setup: seats 1-2 are white, seats 3-4 black, 4 keywords each, 8 words dealt from the 40","rule":"R1","players":4,"seed":1,"rounds":0,"default":"decline",
 "rules":[],
 "expect":{"players":{"1":{"team":"white"},"2":{"team":"white"},"3":{"team":"black"},"4":{"team":"black"}},
           "game":{"round":0,"white_interceptions":0,"white_miscommunications":0,"white_decodes":0,"black_interceptions":0,"black_miscommunications":0,"black_decodes":0},
           "lens":{"game":{"deck":32,"history":0},"players":{"1":{"keywords":4},"2":{"keywords":4},"3":{"keywords":4},"4":{"keywords":4}}}}},
{"name":"Keyword lists keep 4 words each after a round is played","rule":"R2","players":4,"seed":2,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"lens":{"game":{"deck":32},"players":{"1":{"keywords":4},"2":{"keywords":4},"3":{"keywords":4},"4":{"keywords":4}}}}},
{"name":"Round 1: seat 1 encrypts and seat 2 decodes it","rule":"R3","players":4,"seed":3,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":1,"options_include":"2-1-3"},{"seat":2,"options_include":"2-1-3"}],
 "expect":{"game":{"round":1,"white_decodes":1,"white_miscommunications":0,"black_decodes":1,"black_miscommunications":0,"white_interceptions":0,"black_interceptions":0}}},
{"name":"Round 2: seat 2 encrypts, seat 1 decodes, white encryptor intercepts black's code","rule":"R4","players":4,"seed":4,"rounds":1,"default":"decline",
 "given":{"game":{"round":1}},
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":2,"options_include":"2-1-3"},{"seat":1,"options_include":"2-1-3"}],
 "expect":{"game":{"round":2,"white_decodes":1,"white_miscommunications":0,"black_decodes":1,"black_miscommunications":0,"white_interceptions":1,"black_interceptions":0}}},
{"name":"Both encryptors set their own codes and their decoders match them","rule":"R5","players":4,"seed":5,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":1,"options_include":"4-3-2"},{"seat":3,"options_include":"3-4-1"},{"seat":2,"options_include":"4-3-2"},{"seat":4,"options_include":"3-4-1"}],
 "expect":{"game":{"white_decodes":1,"black_decodes":1,"white_miscommunications":0,"black_miscommunications":0}}},
{"name":"Invalid white clues: exactly 1 miscommunication and no decode, even with a correct guess","rule":"R6","players":4,"seed":6,"rounds":1,"default":"decline",
 "judge":{"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"game":{"white_miscommunications":1,"white_decodes":0,"black_decodes":1,"black_miscommunications":0}}},
{"name":"Clues are revealed and the round is recorded in history","rule":"R7","players":4,"seed":7,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"game":{"round":1},"lens":{"game":{"history":1}}}},
{"name":"All four seats guess; black encryptor guesses white's code and intercepts","rule":"R8","players":4,"seed":8,"rounds":1,"default":"decline",
 "given":{"game":{"round":1}},
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":2,"options_include":"2-4-1"},{"seat":4,"options_include":"3-1-2"},{"seat":4,"options_include":"2-4-1"},{"seat":1,"options_include":"2-4-1"},{"seat":3,"options_include":"3-1-2"}],
 "expect":{"game":{"white_decodes":1,"black_decodes":1,"black_interceptions":1,"white_interceptions":0,"white_miscommunications":0,"black_miscommunications":0},
           "offered":[{"seat":1,"option":"1-2-3"},{"seat":2,"option":"1-2-3"},{"seat":3,"option":"1-2-3"},{"seat":4,"option":"1-2-3"}]}},
{"name":"Wrong decoder guess gives a miscommunication instead of a decode","rule":"R9","players":4,"seed":9,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":2,"options_include":"3-2-1"}],
 "expect":{"game":{"white_miscommunications":1,"white_decodes":0,"black_decodes":1,"black_miscommunications":0}}},
{"name":"Interception counts even when the intercepted team's clues are invalid","rule":"R10","players":4,"seed":10,"rounds":1,"default":"decline",
 "given":{"game":{"round":1}},
 "judge":{"White's three clues in white_clues":true},
 "rules":[{"seat":2,"options_include":"4-1-2"},{"seat":1,"options_include":"4-1-2"}],
 "expect":{"game":{"white_interceptions":1,"black_interceptions":0,"black_miscommunications":1,"black_decodes":0,"white_decodes":1,"white_miscommunications":0}}},
{"name":"Round 1: matching encryptor guesses score no interception","rule":"R11","players":4,"seed":11,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"game":{"white_interceptions":0,"black_interceptions":0,"white_decodes":1,"black_decodes":1}}},
{"name":"After scoring the round's entry is appended to history","rule":"R13","players":4,"seed":13,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"lens":{"game":{"history":1}}}},
{"name":"Game ends after round 8; all counters level gives a draw","rule":"R14","players":4,"seed":14,"default":"decline",
 "given":{"game":{"round":7}},
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"winner":[1,2,3,4],"standings":{"1":0,"2":0,"3":0,"4":0},
           "game":{"round":8,"result":0,"white_interceptions":1,"black_interceptions":1,"white_decodes":1,"black_decodes":1}}},
{"name":"White reaches 2 interceptions with no miscommunications and wins","rule":"R15","players":4,"seed":15,"default":"decline",
 "given":{"game":{"round":1,"white_interceptions":1}},
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[{"seat":2,"options_include":"4-3-2"},{"seat":1,"options_include":"4-3-2"}],
 "expect":{"winner":[1,2],"standings":{"1":1,"2":1,"3":-1,"4":-1},
           "game":{"round":2,"white_interceptions":2,"black_interceptions":0,"result":1}}},
{"name":"Black reaches 2 miscommunications, white wins","rule":"R16","players":4,"seed":16,"default":"decline",
 "given":{"game":{"round":1,"black_miscommunications":1}},
 "judge":{"White's three clues in white_clues":true},
 "rules":[],
 "expect":{"winner":[1,2],"standings":{"1":1,"2":1,"3":-1,"4":-1},
           "game":{"round":2,"black_miscommunications":2,"white_miscommunications":0,"result":1}}},
{"name":"Round 8 end with level net and interceptions: more correct decodes wins","rule":"R17","players":4,"seed":17,"default":"decline",
 "given":{"game":{"round":7,"white_decodes":2,"black_decodes":1}},
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"winner":[1,2],"standings":{"1":1,"2":1,"3":-1,"4":-1},
           "game":{"round":8,"white_decodes":3,"black_decodes":2,"white_interceptions":1,"black_interceptions":1,"result":1}}},
{"name":"A round runs encrypt, reveal, guess and score with no discussion step","rule":"R18","players":4,"seed":18,"rounds":1,"default":"decline",
 "judge":{"White's three clues in white_clues":true,"Black's three clues in black_clues":true},
 "rules":[],
 "expect":{"game":{"round":1,"white_decodes":1,"black_decodes":1,"white_miscommunications":0,"black_miscommunications":0}}}
]
````
