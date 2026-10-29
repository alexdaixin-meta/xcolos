# 06 scenarios

- time: 2026-10-28T06:01:03+00:00 (134.1s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 fd0102eecc6b51ec, reply sha256 ad11c3553dac9d03

## Sent

````
SPEC:
{
  "name": "King Up: Fair Throne",
  "summary": "Players secretly favour three characters each, take turns raising characters up a ladder, and vote on any character that reaches the top: all Yes crowns it king, any No eliminates it.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "characters_per_player": 3,
    "no_cards_start": 2,
    "round_limit_3_players": 15,
    "round_limit_4_players": 16,
    "round_limit_5_players": 15,
    "start_height": 0,
    "raise_amount": 1,
    "max_active_height": 5,
    "king_height": 6,
    "eliminated_height": -1,
    "unused_height": -2,
    "king_score": 10,
    "eliminated_score": 0,
    "first_raiser_round_1": 1
  },
  "attributes": {
    "player": [
      {
        "key": "goal",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 3 character labels this player favours, dealt at setup. Secret until scoring.",
        "observable": false
      },
      {
        "key": "no_cards",
        "type": "number",
        "visible": "ally",
        "initial": 2,
        "meaning": "Number of No cards this player still holds. Secret.",
        "observable": false
      },
      {
        "key": "vote",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's election vote, Yes or No. Never revealed individually.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final score: the sum over the 3 goal characters of 10 if king, 0 if eliminated, otherwise the character's height. Computed at game end, when goals are revealed.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "h_a",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character A. -1 means eliminated, 6 means king, 0 to 5 means active.",
        "observable": true
      },
      {
        "key": "h_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character B.",
        "observable": true
      },
      {
        "key": "h_c",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character C.",
        "observable": true
      },
      {
        "key": "h_d",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character D.",
        "observable": true
      },
      {
        "key": "h_e",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character E.",
        "observable": true
      },
      {
        "key": "h_f",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character F.",
        "observable": true
      },
      {
        "key": "h_g",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character G.",
        "observable": true
      },
      {
        "key": "h_h",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character H.",
        "observable": true
      },
      {
        "key": "h_i",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character I.",
        "observable": true
      },
      {
        "key": "h_j",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character J. Set to -2 (not in play) when N = 3.",
        "observable": true
      },
      {
        "key": "h_k",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character K. Set to -2 (not in play) when N = 3.",
        "observable": true
      },
      {
        "key": "h_l",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character L. Set to -2 (not in play) when N = 3.",
        "observable": true
      },
      {
        "key": "h_m",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character M. Set to -2 (not in play) when N < 5.",
        "observable": true
      },
      {
        "key": "h_n",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character N. Set to -2 (not in play) when N < 5.",
        "observable": true
      },
      {
        "key": "h_o",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Height of character O. Set to -2 (not in play) when N < 5.",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The shuffled character labels in play (3N of them), dealt out at setup.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number.",
        "observable": true
      },
      {
        "key": "round_limit",
        "type": "number",
        "visible": "public",
        "initial": 16,
        "meaning": "Last round: 15 if N = 3, 16 if N = 4, 15 if N = 5.",
        "observable": false
      },
      {
        "key": "first_raiser",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that raises first this round.",
        "observable": false
      },
      {
        "key": "candidate",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Label of the character at height 5 this round, or empty if there is none.",
        "observable": false
      },
      {
        "key": "no_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of No votes in this round's election. Announced.",
        "observable": true
      },
      {
        "key": "king_crowned",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once a character has become king.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Let N be the number of seats (3, 4 or 5). The characters in play are the first 3N letters: A-I for N=3, A-L for N=4, A-O for N=5.",
    "Set the height of every character in play to 0, and set the height of every letter not in play to -2 (not in play; never raisable and never in any goal).",
    "Put the 3N labels in play into deck. Shuffle once by drawing at random: seat 1 draws 3 labels into goal, then seat 2 draws 3, and so on until deck is empty. Each label is removed from deck as it is drawn, so no two players share a character.",
    "Set every player's no_cards to 2.",
    "Set round_limit to 15 if N = 3, 16 if N = 4, 15 if N = 5.",
    "Set first_raiser to 1, round to 0 and king_crowned to false.",
    "Sync: each player privately sees their own goal and no_cards."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; candidate = ''; no_count = 0; every player's vote = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the round number and the heights of all characters in play (h_a ... up to the last label in play)."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Each message is broadcast to all as 'Seat {seat} says: {value}'. Messages bind no one."
    },
    {
      "action": "ask",
      "who": "each player in turn, in seat order starting at seat first_raiser and wrapping from seat N to seat 1",
      "answer": "the label of one legal character, or 'pass' only if there is no legal raise. A character is legal if its height is 0 to 4, and if its height is 4 then no character is currently at height 5.",
      "effect": "The chosen character's height += 1. Each later player sees the updated heights. A pass changes nothing."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "candidate = the label of the character whose height is 5, if any; otherwise candidate stays empty."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "Yes or No; a player with no_cards = 0 is offered only Yes",
      "effect": "when candidate is not empty: each player's vote is recorded secretly. Skipped when candidate is empty."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when candidate is not empty: no_count = number of players with vote = No. If no_count = 0, the candidate's height = 6 and king_crowned = true. If no_count >= 1, each player with vote = No has no_cards -= 1, and the candidate's height = -1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when candidate is not empty: announce the candidate, the number of No votes (no_count, not who cast them), and whether it was crowned king or eliminated."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "first_raiser = (first_raiser mod N) + 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when king_crowned or round >= round_limit: reveal every player's goal; each player's score = the sum over their 3 goal characters of (10 if height = 6; 0 if height = -1; otherwise height)."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if king_crowned is true or round >= round_limit; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "king_crowned == true OR round >= round_limit",
    "rank_by": "you.score",
    "decided_by": "Each player's score is the sum over their 3 secret goal characters: 10 for a king, 0 for an eliminated character, otherwise its height (0 to 5). The highest score wins; players tied for the highest score share a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up with N players, then 3N characters are in play (A-I for 3, A-L for 4, A-O for 5), each at height 0."
    },
    {
      "id": "R2",
      "text": "When the game is set up, then each player's goal holds exactly 3 distinct labels, every label in play is in exactly one goal, and deck is empty."
    },
    {
      "id": "R3",
      "text": "When the game is set up, then every player has no_cards = 2."
    },
    {
      "id": "R4",
      "text": "When N is 3, 4 or 5, then round_limit is 15, 16 or 15 respectively."
    },
    {
      "id": "R5",
      "text": "When round 1 begins, then first_raiser is seat 1."
    },
    {
      "id": "R6",
      "text": "When a round begins, then the round number and all heights are announced to everyone."
    },
    {
      "id": "R7",
      "text": "When the talk step runs, then every player submits one message simultaneously, and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R8",
      "text": "When the raise step runs, then each player in seat order starting at first_raiser and wrapping from N to 1 raises one character by exactly 1."
    },
    {
      "id": "R9",
      "text": "When a character is at height -1, 5 or 6, then it may not be raised."
    },
    {
      "id": "R10",
      "text": "When a character is at height 4 and another character is at height 5, then it may not be raised."
    },
    {
      "id": "R11",
      "text": "When a character is at height 4 and no character is at height 5, then it may be raised to 5."
    },
    {
      "id": "R12",
      "text": "When a player has no legal raise, then that player passes and no height changes."
    },
    {
      "id": "R13",
      "text": "When no character is at height 5 after the raise step, then no election is held and no_cards are unchanged."
    },
    {
      "id": "R14",
      "text": "When a character is at height 5 after the raise step, then it is the candidate and every player votes Yes or No simultaneously."
    },
    {
      "id": "R15",
      "text": "When a player has no_cards = 0, then that player may vote only Yes."
    },
    {
      "id": "R16",
      "text": "When all votes are Yes, then the candidate's height becomes 6 and the game ends after this round."
    },
    {
      "id": "R17",
      "text": "When at least one vote is No, then each No voter loses 1 No card and the candidate's height becomes -1 for the rest of the game."
    },
    {
      "id": "R18",
      "text": "When an election resolves, then only the number of No votes is announced, not who cast them."
    },
    {
      "id": "R19",
      "text": "When a round ends, then first_raiser becomes the next seat in seat order (seat N goes to seat 1)."
    },
    {
      "id": "R20",
      "text": "When round reaches round_limit and no king has been crowned, then the game ends."
    },
    {
      "id": "R21",
      "text": "When the game ends, then each player scores 10 for each goal character at height 6, 0 for each at height -1, and its height for each at 0 to 5."
    },
    {
      "id": "R22",
      "text": "When the game ends, then the player with the highest score wins, and players tied for the highest score share a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk",
      "who": "every seat",
      "options": "a short free-text message"
    },
    {
      "question": "Raise",
      "who": "each seat in turn starting at first_raiser",
      "options": "every character label in play whose height is 0 to 3, plus every label at height 4 if no character is at height 5; if that set is empty, only 'pass'"
    },
    {
      "question": "Election vote",
      "who": "every seat, only when a candidate is at height 5",
      "options": "a seat with no_cards >= 1: Yes, No; a seat with no_cards = 0: Yes only"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer's suggested size is 4 and is kept. 3 is the minimum because with fewer players secret goals are easy to deduce and there is no group to veto against. 5 is the maximum because the label set only goes up to O, and with more players each player's raise and veto would matter little."
    },
    {
      "what": "Talk as a simultaneous poll broadcast to all",
      "why": "The rules say messages are written at the same time without seeing the others. Talk earns its place because players' goals conflict: players bluff about which characters they favour and try to steer others into spending No cards."
    },
    {
      "what": "Score computed only at game end",
      "why": "The rules reveal goals only at scoring, so a running public score would leak the secret goals."
    },
    {
      "what": "Unused letters set to height -2",
      "why": "This keeps a fixed set of 15 height attributes for every table size while marking the unused letters as never raisable and never in any goal."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player hides their goal, raises characters that help them without revealing them, saves No cards for candidates that help rivals more, and reads the No counts and others' raises to infer goals. A thoughtless player rushes one favourite to 5 and gets it vetoed."
    }
  ],
  "simplifications": [
    {
      "what": "Characters stored as 15 fixed height attributes h_a..h_o rather than a variable-length list",
      "why": "Arithmetic and per-character options are simpler on named numbers. Letters not in play are fixed at -2 and never offered."
    },
    {
      "what": "Election and resolve steps carry a 'when candidate is not empty' condition instead of being skipped as a block",
      "why": "The step list is flat. Each step is gated individually by the same arithmetic condition, which matches the rule exactly."
    },
    {
      "what": "The secret vote is stored in a per-player vote attribute visible only to its owner",
      "why": "This is needed to deduct No cards from the No voters while announcing only the count."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: h_a, h_b, h_c, h_d, h_e, h_f, h_g, h_h, h_i, h_j, h_k, h_l, h_m, h_n, h_o, round, no_count, king_crowned.
````

## Reply

````
```json
[
  {"name": "R1: 4 players put A-L in play at height 0, M-O are not in play", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"game": {"h_a": 0, "h_b": 0, "h_c": 0, "h_d": 0, "h_e": 0, "h_f": 0, "h_g": 0, "h_h": 0, "h_i": 0, "h_j": 0, "h_k": 0, "h_l": 0, "h_m": -2, "h_n": -2, "h_o": -2}}},
  {"name": "R1: 3 players put A-I in play at height 0, J-O are not in play", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"game": {"h_a": 0, "h_b": 0, "h_c": 0, "h_d": 0, "h_e": 0, "h_f": 0, "h_g": 0, "h_h": 0, "h_i": 0, "h_j": -2, "h_k": -2, "h_l": -2, "h_m": -2, "h_n": -2, "h_o": -2}}},
  {"name": "R1: 5 players put A-O in play at height 0", "rule": "R1", "players": 5, "rounds": 0,
   "expect": {"game": {"h_a": 0, "h_b": 0, "h_c": 0, "h_d": 0, "h_e": 0, "h_f": 0, "h_g": 0, "h_h": 0, "h_i": 0, "h_j": 0, "h_k": 0, "h_l": 0, "h_m": 0, "h_n": 0, "h_o": 0}}},
  {"name": "R2: each goal holds 3 labels and the deck is empty after the deal (random deal, counts only)", "rule": "R2", "players": 4, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"goal": 3}, "2": {"goal": 3}, "3": {"goal": 3}, "4": {"goal": 3}}}}},
  {"name": "R3: every seat starts with No cards, so every seat is offered No at the first election", "rule": "R3", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "No"}, {"seat": 2, "option": "No"}, {"seat": 3, "option": "No"}],
              "game": {"h_a": 6, "h_b": 2, "king_crowned": true}}},
  {"name": "R4: with 3 players the game ends after round 15", "rule": "R4", "players": 3,
   "given": {"players": {"1": {"goal": ["A", "D", "G"]}, "2": {"goal": ["B", "E", "H"]}, "3": {"goal": ["C", "F", "I"]}}, "game": {"round": 14}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "A"}, {"seat": 3, "options_include": "B"}],
   "expect": {"winner": 1, "standings": {"1": 2, "2": 1, "3": 0},
              "players": {"1": {"score": 2}, "2": {"score": 1}, "3": {"score": 0}},
              "game": {"round": 15, "h_a": 2, "h_b": 1, "king_crowned": false}}},
  {"name": "R4: with 4 players the game goes on past round 15 and ends after round 16", "rule": "R4", "players": 4,
   "given": {"players": {"1": {"goal": ["A", "B", "C"]}, "2": {"goal": ["D", "E", "F"]}, "3": {"goal": ["G", "H", "I"]}, "4": {"goal": ["J", "K", "L"]}}, "game": {"round": 14}},
   "rules": [{"seat": 1, "options_include": "J", "times": 2}, {"seat": 2, "options_include": "K", "times": 2},
             {"seat": 3, "options_include": "L", "times": 2}, {"seat": 4, "options_include": "J", "times": 2}],
   "expect": {"winner": 4, "standings": {"1": 0, "2": 0, "3": 0, "4": 8},
              "players": {"4": {"score": 8}, "1": {"score": 0}},
              "game": {"round": 16, "h_j": 4, "h_k": 2, "h_l": 2, "king_crowned": false}}},
  {"name": "R5: in round 1 seat 1 raises first, so seats 2 and 3 cannot raise A after it reaches 5", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "A"}],
              "not_offered": [{"seat": 2, "option": "A"}, {"seat": 3, "option": "A"}],
              "game": {"h_a": 6, "h_b": 2}}},
  {"name": "R6: after the first round the round number is 1 and the heights show the raises", "rule": "R6", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "C"}],
   "expect": {"game": {"round": 1, "h_a": 1, "h_b": 1, "h_c": 1, "h_d": 0}}},
  {"name": "R7: the talk step binds no one, and two rounds play normally", "rule": "R7", "players": 3, "rounds": 2,
   "rules": [{"seat": 1, "options_include": "A", "times": 2}, {"seat": 2, "options_include": "B", "times": 2}, {"seat": 3, "options_include": "C", "times": 2}],
   "expect": {"game": {"round": 2, "h_a": 2, "h_b": 2, "h_c": 2, "king_crowned": false}}},
  {"name": "R8: each of 4 seats raises one character by exactly 1", "rule": "R8", "players": 4, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "A"}, {"seat": 3, "options_include": "B"}, {"seat": 4, "options_include": "A"}],
   "expect": {"game": {"h_a": 3, "h_b": 1, "h_c": 0, "round": 1}}},
  {"name": "R8: raising order starts at first_raiser 3 and wraps to seats 1 and 2", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4, "first_raiser": 3}},
   "rules": [{"seat": 3, "options_include": "A"}, {"seat": 1, "options_include": "B"}, {"seat": 2, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 3, "option": "A"}],
              "not_offered": [{"seat": 1, "option": "A"}, {"seat": 2, "option": "A"}],
              "game": {"h_a": 6, "h_b": 2}}},
  {"name": "R9: an eliminated character and a character at height 5 cannot be raised", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": -1, "h_b": 4}},
   "rules": [{"seat": 1, "options_include": "B"}, {"seat": 2, "options_include": "C"}, {"seat": 3, "options_include": "C"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"not_offered": [{"seat": 1, "option": "A"}, {"seat": 2, "option": "A"}, {"seat": 3, "option": "A"},
                              {"seat": 2, "option": "B"}, {"seat": 3, "option": "B"}],
              "game": {"h_a": -1, "h_b": 6, "h_c": 2}}},
  {"name": "R10: a character at 4 cannot be raised while another is at 5", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4, "h_b": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "C"}, {"seat": 3, "options_include": "C"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "B"}],
              "not_offered": [{"seat": 2, "option": "B"}, {"seat": 3, "option": "B"}],
              "game": {"h_a": 6, "h_b": 4, "h_c": 2}}},
  {"name": "R11: a character at 4 with none at 5 can be raised to 5 and goes to election", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "A"}],
              "game": {"h_a": 6, "h_b": 2, "king_crowned": true, "no_count": 0}}},
  {"name": "R12: seats with no legal raise pass and nothing changes", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": -1, "h_b": -1, "h_c": -1, "h_d": -1, "h_e": -1, "h_f": -1, "h_g": -1, "h_h": -1, "h_i": 4}},
   "rules": [{"seat": 1, "options_include": "I"}, {"seat": 2, "options_include": "pass"}, {"seat": 3, "options_include": "pass"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 2, "option": "pass"}, {"seat": 3, "option": "pass"}],
              "not_offered": [{"seat": 2, "option": "I"}, {"seat": 3, "option": "I"}, {"seat": 1, "option": "pass"}],
              "game": {"h_a": -1, "h_b": -1, "h_c": -1, "h_d": -1, "h_e": -1, "h_f": -1, "h_g": -1, "h_h": -1, "h_i": 6}}},
  {"name": "R13: no character at 5 after raising means no election", "rule": "R13", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "C"}],
   "expect": {"not_offered": [{"seat": 1, "option": "Yes"}, {"seat": 2, "option": "Yes"}, {"seat": 3, "option": "Yes"},
                              {"seat": 1, "option": "No"}, {"seat": 2, "option": "No"}, {"seat": 3, "option": "No"}],
              "game": {"no_count": 0, "king_crowned": false, "h_a": 1, "h_b": 1, "h_c": 1}}},
  {"name": "R14: a character at 5 becomes candidate and every seat votes", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "Yes"}, {"seat": 2, "option": "Yes"}, {"seat": 3, "option": "Yes"},
                          {"seat": 1, "option": "No"}, {"seat": 2, "option": "No"}, {"seat": 3, "option": "No"}],
              "game": {"h_a": 6}}},
  {"name": "R15: a seat with no No cards is offered only Yes", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"no_cards": 0}}, "game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"offered": [{"seat": 1, "option": "No"}, {"seat": 3, "option": "No"}, {"seat": 2, "option": "Yes"}],
              "not_offered": [{"seat": 2, "option": "No"}],
              "game": {"h_a": 6, "no_count": 0}}},
  {"name": "R16: all Yes crowns the candidate at 6 and the game ends", "rule": "R16", "players": 3,
   "given": {"players": {"1": {"goal": ["A", "B", "C"]}, "2": {"goal": ["D", "E", "F"]}, "3": {"goal": ["G", "H", "I"]}},
             "game": {"h_a": 4, "h_d": 2, "h_g": 3}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "D"}, {"seat": 3, "options_include": "H"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"winner": 1, "standings": {"1": 10, "2": 3, "3": 4},
              "players": {"1": {"score": 10}, "2": {"score": 3}, "3": {"score": 4}},
              "game": {"h_a": 6, "king_crowned": true, "round": 1, "no_count": 0}}},
  {"name": "R17: any No eliminates the candidate at -1", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "No"}, {"seat": 3, "options_include": "No"}],
   "expect": {"game": {"h_a": -1, "h_b": 2, "no_count": 2, "king_crowned": false}}},
  {"name": "R17: a No voter loses a No card, so with its last card spent it can only vote Yes next election", "rule": "R17", "players": 3, "rounds": 2,
   "given": {"players": {"2": {"no_cards": 1}}, "game": {"h_a": 4, "h_b": 4}},
   "rules": [{"seat": 1, "options_include": "A", "times": 2}, {"seat": 1, "options_include": "C"},
             {"seat": 2, "options_include": "B"}, {"seat": 2, "options_include": "C"},
             {"seat": 3, "options_include": "C", "times": 2},
             {"seat": 1, "options_include": "Yes", "times": "all"}, {"seat": 3, "options_include": "Yes", "times": "all"},
             {"seat": 2, "options_include": "No", "times": "all"}],
   "expect": {"game": {"h_a": -1, "h_b": 6, "h_c": 4, "king_crowned": true, "no_count": 0, "round": 2}}},
  {"name": "R18: the number of No votes is announced", "rule": "R18", "players": 4, "rounds": 1,
   "given": {"game": {"h_a": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "B"}, {"seat": 3, "options_include": "B"}, {"seat": 4, "options_include": "B"},
             {"seat": 1, "options_include": "No"}, {"seat": 2, "options_include": "No"}, {"seat": 3, "options_include": "Yes"}, {"seat": 4, "options_include": "No"}],
   "expect": {"game": {"h_a": -1, "h_b": 3, "no_count": 3, "king_crowned": false}}},
  {"name": "R19: in round 2 seat 2 raises first, before seat 1", "rule": "R19", "players": 3, "rounds": 2,
   "given": {"game": {"h_a": 3, "h_b": 3}},
   "rules": [{"seat": 1, "options_include": "A", "times": 2}, {"seat": 1, "options_include": "C"},
             {"seat": 2, "options_include": "B", "times": 2},
             {"seat": 3, "options_include": "C", "times": 2},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"game": {"h_a": 4, "h_b": 6, "h_c": 3, "king_crowned": true, "round": 2}}},
  {"name": "R20: with 5 players and no king the game ends after round 15", "rule": "R20", "players": 5,
   "given": {"players": {"1": {"goal": ["A", "B", "C"]}, "2": {"goal": ["D", "E", "F"]}, "3": {"goal": ["G", "H", "I"]}, "4": {"goal": ["J", "K", "L"]}, "5": {"goal": ["M", "N", "O"]}},
             "game": {"round": 14}},
   "rules": [{"seat": 1, "options_include": "D"}, {"seat": 2, "options_include": "D"}, {"seat": 3, "options_include": "D"},
             {"seat": 4, "options_include": "G"}, {"seat": 5, "options_include": "G"}],
   "expect": {"winner": 2, "standings": {"1": 0, "2": 3, "3": 2, "4": 0, "5": 0},
              "players": {"2": {"score": 3}, "3": {"score": 2}, "1": {"score": 0}},
              "game": {"round": 15, "h_d": 3, "h_g": 2, "king_crowned": false}}},
  {"name": "R21: scoring gives 10 for a king, 0 for an eliminated character, height otherwise", "rule": "R21", "players": 3,
   "given": {"players": {"1": {"goal": ["A", "B", "C"]}, "2": {"goal": ["D", "E", "F"]}, "3": {"goal": ["G", "H", "I"]}},
             "game": {"h_a": 4, "h_b": -1, "h_c": 3, "h_d": 2, "h_e": 1, "h_f": 0, "h_g": -1, "h_h": -1, "h_i": 4}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "E"}, {"seat": 3, "options_include": "C"},
             {"seat": 1, "options_include": "Yes"}, {"seat": 2, "options_include": "Yes"}, {"seat": 3, "options_include": "Yes"}],
   "expect": {"winner": 1, "standings": {"1": 14, "2": 4, "3": 4},
              "players": {"1": {"score": 14}, "2": {"score": 4}, "3": {"score": 4}},
              "game": {"h_a": 6, "h_c": 4, "h_e": 2, "king_crowned": true}}},
  {"name": "R22: seats tied for the highest score share the win", "rule": "R22", "players": 3,
   "given": {"players": {"1": {"goal": ["A", "B", "C"]}, "2": {"goal": ["D", "E", "F"]}, "3": {"goal": ["G", "H", "I"]}},
             "game": {"round": 14, "h_d": 1}},
   "rules": [{"seat": 1, "options_include": "A"}, {"seat": 2, "options_include": "A"}, {"seat": 3, "options_include": "D"}],
   "expect": {"winner": [1, 2], "standings": {"1": 2, "2": 2, "3": 0},
              "players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 0}},
              "game": {"round": 15, "h_a": 2, "h_d": 2}}}
]
```
````
