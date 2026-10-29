# 45 scenarios

- time: 2026-10-28T05:14:03+00:00 (95.3s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e5925550bfe694d5, reply sha256 37f0e4c32ec0de73

## Sent

````
SPEC:
{
  "name": "3Up Clear Race",
  "summary": "Three players shed a 10-card hand onto a climbing pile. A run of three equal ranks or a Clear card wipes the pile, a stuck player must take the pile, and the first to empty hand and face-up cards wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "min_rank": 1,
    "max_rank": 9,
    "copies_per_rank": 3,
    "clear_cards": 3,
    "low_band_max": 3,
    "mid_band_min": 4,
    "mid_band_max": 6,
    "high_band_min": 7,
    "cards_per_band_dealt": 3,
    "clears_per_seat": 1,
    "hand_size": 10,
    "face_up_picks": 3,
    "hand_after_picks": 7,
    "run_to_clear": 3,
    "max_rounds": 30,
    "empty_top_rank": 0
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "the seat's private hand of cards; each entry is a rank '1'..'9' or 'C'",
        "observable": false
      },
      {
        "key": "up_pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the seat's three face-up cards, played only once the hand is empty",
        "observable": true
      },
      {
        "key": "hand_count",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "number of cards in hand",
        "observable": true
      },
      {
        "key": "up_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of cards in up_pile",
        "observable": true
      },
      {
        "key": "cards_left",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "hand_count + up_count; the score, where lower is better",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "1",
          "1",
          "1",
          "2",
          "2",
          "2",
          "3",
          "3",
          "3"
        ],
        "meaning": "shuffled low cards to deal from",
        "observable": false
      },
      {
        "key": "mid_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "4",
          "4",
          "4",
          "5",
          "5",
          "5",
          "6",
          "6",
          "6"
        ],
        "meaning": "shuffled mid cards to deal from",
        "observable": false
      },
      {
        "key": "high_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "7",
          "7",
          "7",
          "8",
          "8",
          "8",
          "9",
          "9",
          "9"
        ],
        "meaning": "shuffled high cards to deal from",
        "observable": false
      },
      {
        "key": "pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the central pile of played cards",
        "observable": false
      },
      {
        "key": "top_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rank on top of the pile; 0 means the pile is empty",
        "observable": false
      },
      {
        "key": "run_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "how many consecutive cards of top_rank are on the pile",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "round counter",
        "observable": false
      },
      {
        "key": "lead",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that plays first this round",
        "observable": false
      },
      {
        "key": "game_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once a seat empties or round 30 ends",
        "observable": false
      }
    ]
  },
  "setup": [
    "Set low_stack to 1,1,1,2,2,2,3,3,3, mid_stack to 4,4,4,5,5,5,6,6,6 and high_stack to 7,7,7,8,8,8,9,9,9, then shuffle each stack.",
    "For seats 1, 2 and 3 in turn, draw 3 random cards from low_stack, 3 from mid_stack and 3 from high_stack into that seat's hand, removing each from its stack, then append one 'C' to the hand. Every hand now has 10 cards and all stacks are empty.",
    "Face-up pick 1: a simultaneous poll in which every seat chooses one card from its own hand. Options are the distinct ranks in the hand in ascending order, then 'C' last if held. The chosen card moves from hand to up_pile. A missing or invalid answer takes the first listed option.",
    "Face-up pick 2: the same poll again.",
    "Face-up pick 3: the same poll again.",
    "For every seat set hand_count = 7, up_count = 3 and cards_left = 10. Set pile = empty, top_rank = 0 and run_count = 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round = round + 1; lead = ((round - 1) mod 3) + 1; announce the round and the leading seat"
    },
    {
      "action": "ask",
      "who": "seat lead (turn slot 1); skipped when game_over is true",
      "answer": "one option from the list built per rule T1: 'r xk' for each rank r >= top_rank in the source (the hand if hand_count > 0, else up_pile) and each k from 1 to the copies of r there, ascending by r then k; 'C' last if the source holds a C; if there are no options, only 'take'. A missing or invalid answer takes the first option.",
      "effect": "the choice is recorded for this slot and announced to all"
    },
    {
      "action": "update",
      "who": "seat lead (turn slot 1); skipped when game_over is true",
      "answer": null,
      "effect": "'r xk': move k cards of rank r from the source to pile; if top_rank == r then run_count += k else run_count = k; top_rank = r. 'C': remove that C from the source and from the game. 'take': append all pile cards to hand, pile = empty, top_rank = 0, run_count = 0. Then, if 'C' was played or run_count >= 3: remove all pile cards from the game, top_rank = 0, run_count = 0. Then hand_count = length of hand, up_count = length of up_pile, cards_left = hand_count + up_count; if cards_left == 0 then game_over = true. Announce the play."
    },
    {
      "action": "ask",
      "who": "seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true",
      "answer": "the same option list as slot 1, built for this seat",
      "effect": "the choice is recorded and announced to all"
    },
    {
      "action": "update",
      "who": "seat (lead mod 3) + 1 (turn slot 2); skipped when game_over is true",
      "answer": null,
      "effect": "the same play, clear and count updates as slot 1, applied to this seat"
    },
    {
      "action": "ask",
      "who": "seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true",
      "answer": "the same option list as slot 1, built for this seat",
      "effect": "the choice is recorded and announced to all"
    },
    {
      "action": "update",
      "who": "seat ((lead + 1) mod 3) + 1 (turn slot 3); skipped when game_over is true",
      "answer": null,
      "effect": "the same play, clear and count updates as slot 1, applied to this seat"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if round == 30 then game_over = true"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if game_over is true; otherwise run the round again"
    }
  ],
  "ending": {
    "condition": "game_over == true",
    "rank_by": "0 - you.cards_left",
    "decided_by": "A player's standing is how few cards they have left. A seat that reaches 0 cards_left ends the game at once and is the only seat at 0, so it wins. Otherwise, after round 30, the seat with the fewest cards_left wins, and seats tied for fewest share the result, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When setup ends, each seat has 7 cards in hand and 3 in up_pile, every hand began as 3 low (1-3), 3 mid (4-6), 3 high (7-9) and 1 'C', and all three stacks are empty."
    },
    {
      "id": "R2",
      "text": "When a face-up pick is made, the chosen card leaves the hand and joins that seat's public up_pile; this happens 3 times, simultaneously for all seats."
    },
    {
      "id": "R3",
      "text": "When a face-up pick answer is missing or invalid, the first listed card (lowest rank, or 'C' if only C remains) is taken."
    },
    {
      "id": "R4",
      "text": "When round increments, lead = ((round - 1) mod 3) + 1, so round 1 is led by seat 1, round 2 by seat 2, round 3 by seat 3 and round 4 by seat 1."
    },
    {
      "id": "R5",
      "text": "When a seat takes its turn, seats act in the order lead, lead+1, lead+2, wrapping from seat 3 to seat 1."
    },
    {
      "id": "R6",
      "text": "When hand_count > 0, a seat plays from its hand; when hand_count == 0, it plays from its up_pile."
    },
    {
      "id": "R7",
      "text": "When top_rank is t, a seat may play k copies (k from 1 to the copies held) of any rank r >= t from its source; with top_rank 0 any rank is legal."
    },
    {
      "id": "R8",
      "text": "When a seat holds a 'C' in its source, 'C' is always offered, listed last."
    },
    {
      "id": "R9",
      "text": "When a seat has no legal rank play and no C, its only option is 'take'."
    },
    {
      "id": "R10",
      "text": "When a seat takes, every pile card moves into its hand and top_rank and run_count become 0."
    },
    {
      "id": "R11",
      "text": "When k cards of rank r are played and top_rank == r, run_count increases by k; otherwise run_count becomes k; top_rank becomes r."
    },
    {
      "id": "R12",
      "text": "When run_count reaches 3 or more, all pile cards are removed from the game and top_rank and run_count become 0."
    },
    {
      "id": "R13",
      "text": "When a 'C' is played, the C and all pile cards are removed from the game and top_rank and run_count become 0."
    },
    {
      "id": "R14",
      "text": "When a turn ends, cards_left = hand_count + up_count for that seat."
    },
    {
      "id": "R15",
      "text": "When a seat's cards_left becomes 0, game_over becomes true, the remaining turns are skipped, and that seat wins."
    },
    {
      "id": "R16",
      "text": "When round 30 ends with no seat at 0, the game ends and the seat with the fewest cards_left wins; seats tied for fewest share the result (a draw)."
    },
    {
      "id": "R17",
      "text": "When a turn answer is missing or invalid, the first listed option is applied."
    }
  ],
  "offers": [
    {
      "question": "Face-up pick (setup, 3 times)",
      "who": "all seats at once",
      "options": "each distinct rank in the seat's own hand, ascending, then 'C' last if the hand holds a C"
    },
    {
      "question": "Turn play",
      "who": "the seat whose turn slot it is",
      "options": "source = hand if hand_count > 0, else up_pile. For each rank r in the source with r >= top_rank, options 'r x1' up to 'r xN' where N is the copies of r in the source, ascending by r then k; then 'C' if the source holds a C. If none of these exist, only 'take'."
    }
  ],
  "choices": [
    {
      "what": "3 players (min = max = suggested = 3)",
      "why": "The designer fixed the game at 3: the deck splits exactly into three 10-card hands and the lead rotates over 3 seats. Fewer seats would leave stacks undealt and more would need more cards. At 3, each seat must read the public up_piles and the pile to decide when to dump runs, save a C, or force an opponent to take."
    },
    {
      "what": "No talk phase",
      "why": "The source says there is none; plays are announced publicly instead."
    },
    {
      "what": "Score expressed as 0 - cards_left",
      "why": "The engine ranks highest-first, and fewer cards is better."
    },
    {
      "what": "Card entries stored as text '1'..'9' and 'C'",
      "why": "A single list can then hold both ranks and Clear cards; ranks are compared numerically."
    }
  ],
  "simplifications": [
    {
      "what": "The three turns of a round are written as three fixed turn slots (seat lead, lead+1, lead+2), each an ask followed by an update guarded by game_over == false",
      "why": "The step list is flat, so the rotating order is unrolled into slots whose seat is computed from lead."
    },
    {
      "what": "A tie for fewest cards_left is shown as a shared win",
      "why": "The engine has no separate draw; players level at the top share the win, which stands for the source's draw."
    },
    {
      "what": "Removed cards (cleared piles and played C cards) are dropped from all lists rather than kept in a discard list",
      "why": "The rules only say they leave the game and never refer to them again."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: up_pile, hand_count, up_count, cards_left; table: none.
````

## Reply

````
```json
[
  {
    "name": "R1: after setup each seat holds 7 in hand and 3 face-up, and the stacks are empty",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "default": "first",
    "expect": {
      "players": {
        "1": {"hand_count": 7, "up_count": 3, "cards_left": 10},
        "2": {"hand_count": 7, "up_count": 3, "cards_left": 10},
        "3": {"hand_count": 7, "up_count": 3, "cards_left": 10}
      },
      "lens": {
        "game": {"low_stack": 0, "mid_stack": 0, "high_stack": 0},
        "players": {
          "1": {"hand": 7, "up_pile": 3},
          "2": {"hand": 7, "up_pile": 3},
          "3": {"hand": 7, "up_pile": 3}
        }
      }
    }
  },
  {
    "name": "R2: a face-up pick moves the chosen card to up_pile (C is always pickable; only counts asserted because of the random deal)",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 0,
    "default": "first",
    "rules": [{"seat": 1, "options_include": "C"}],
    "expect": {
      "offered": [{"seat": 1, "option": "C"}],
      "players": {
        "1": {"hand_count": 7, "up_count": 3, "cards_left": 10}
      },
      "lens": {"players": {"1": {"hand": 7, "up_pile": 3}}}
    }
  },
  {
    "name": "R4: round 2 is led by seat 2, so seat 1 plays last and must take",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 1, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": ["2"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "2": {"hand": ["5"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["6"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4}
      }
    },
    "expect": {
      "offered": [{"seat": 1, "option": "take"}],
      "players": {
        "1": {"hand_count": 3, "cards_left": 6},
        "2": {"hand_count": 0, "cards_left": 3},
        "3": {"hand_count": 0, "cards_left": 3}
      }
    }
  },
  {
    "name": "R5: in round 3 the order wraps 3, 1, 2, so seat 2 plays last and takes",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 2, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": ["6"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "2": {"hand": ["2"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["5"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4}
      }
    },
    "expect": {
      "offered": [{"seat": 2, "option": "take"}],
      "players": {
        "1": {"hand_count": 0, "cards_left": 3},
        "2": {"hand_count": 3, "cards_left": 6},
        "3": {"hand_count": 0, "cards_left": 3}
      }
    }
  },
  {
    "name": "R6: with an empty hand a seat plays from its up_pile",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": [], "hand_count": 0, "up_pile": ["4", "7", "7"], "up_count": 3, "cards_left": 3},
        "2": {"hand": ["8"], "hand_count": 1, "up_pile": ["1", "2", "3"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["9"], "hand_count": 1, "up_pile": ["1", "2", "3"], "up_count": 3, "cards_left": 4}
      }
    },
    "rules": [{"seat": 1, "options_include": "7 x2"}],
    "expect": {
      "not_offered": [{"seat": 1, "option": "take"}],
      "players": {
        "1": {"up_pile": ["4"], "up_count": 1, "hand_count": 0, "cards_left": 1},
        "2": {"hand_count": 0, "cards_left": 3},
        "3": {"hand_count": 0, "cards_left": 3}
      }
    }
  },
  {
    "name": "R7: only ranks at or above top_rank are offered, and any rank is offered on an empty pile",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["5"], "top_rank": 5, "run_count": 1},
      "players": {
        "1": {"hand": ["3", "5", "5", "8"], "hand_count": 4, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 7},
        "2": {"hand": ["4", "6"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "3": {"hand": ["2", "7"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "rules": [{"seat": 1, "options_include": "8 x1"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "5 x1"},
        {"seat": 1, "option": "5 x2"},
        {"seat": 2, "option": "take"},
        {"seat": 3, "option": "2 x1"}
      ],
      "not_offered": [
        {"seat": 1, "option": "3 x1"},
        {"seat": 2, "option": "4 x1"}
      ],
      "players": {
        "1": {"hand_count": 3, "cards_left": 6},
        "2": {"hand_count": 4, "cards_left": 7},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  },
  {
    "name": "R8: a held C is offered even when no rank can be played",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["9"], "top_rank": 9, "run_count": 1},
      "players": {
        "1": {"hand": ["2", "C"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["3"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["1", "4"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "rules": [{"seat": 1, "options_include": "C"}],
    "expect": {
      "offered": [{"seat": 1, "option": "C"}],
      "not_offered": [
        {"seat": 1, "option": "take"},
        {"seat": 1, "option": "2 x1"}
      ],
      "players": {
        "1": {"hand_count": 1, "cards_left": 4},
        "2": {"hand_count": 0, "cards_left": 3},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  },
  {
    "name": "R9: with no legal rank and no C, the only option is take",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["8"], "top_rank": 8, "run_count": 1},
      "players": {
        "1": {"hand": ["2", "3"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["4"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["6"], "hand_count": 1, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 4}
      }
    },
    "expect": {
      "offered": [{"seat": 1, "option": "take"}],
      "not_offered": [
        {"seat": 1, "option": "2 x1"},
        {"seat": 1, "option": "3 x1"}
      ],
      "players": {
        "1": {"hand_count": 3, "cards_left": 6},
        "2": {"hand_count": 0, "cards_left": 3},
        "3": {"hand_count": 0, "cards_left": 3}
      }
    }
  },
  {
    "name": "R10: taking moves the whole pile into the hand and resets top_rank to 0",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["4", "6"], "top_rank": 6, "run_count": 1},
      "players": {
        "1": {"hand": ["2", "5"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["3", "9"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "3": {"hand": ["1", "2"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "expect": {
      "offered": [
        {"seat": 1, "option": "take"},
        {"seat": 2, "option": "3 x1"},
        {"seat": 3, "option": "take"}
      ],
      "players": {
        "1": {"hand_count": 4, "cards_left": 7},
        "2": {"hand_count": 1, "cards_left": 4},
        "3": {"hand_count": 3, "cards_left": 6}
      }
    }
  },
  {
    "name": "R11: a new rank restarts run_count, so two 5s on top of two 4s do not clear",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["4", "4"], "top_rank": 4, "run_count": 2},
      "players": {
        "1": {"hand": ["5", "7"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["5", "8"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "3": {"hand": ["1", "2"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "5 x1"},
      {"seat": 2, "options_include": "5 x1"}
    ],
    "expect": {
      "offered": [{"seat": 3, "option": "take"}],
      "players": {
        "1": {"hand_count": 1, "cards_left": 4},
        "2": {"hand_count": 1, "cards_left": 4},
        "3": {"hand_count": 6, "cards_left": 9}
      }
    }
  },
  {
    "name": "R12: a run reaching 3 clears the pile, so the next seat plays freely",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["5"], "top_rank": 5, "run_count": 1},
      "players": {
        "1": {"hand": ["5", "5", "9"], "hand_count": 3, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 6},
        "2": {"hand": ["1", "2"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "3": {"hand": ["1", "3"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "rules": [{"seat": 1, "options_include": "5 x2"}],
    "expect": {
      "offered": [{"seat": 2, "option": "1 x1"}],
      "not_offered": [{"seat": 2, "option": "take"}],
      "players": {
        "1": {"hand_count": 1, "cards_left": 4},
        "2": {"hand_count": 1, "cards_left": 4},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  },
  {
    "name": "R13: playing C removes it and clears the pile",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": ["7", "7"], "top_rank": 7, "run_count": 2},
      "players": {
        "1": {"hand": ["8", "C"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["1", "3"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "3": {"hand": ["2", "4"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "rules": [{"seat": 1, "options_include": "C"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "8 x1"},
        {"seat": 2, "option": "1 x1"}
      ],
      "not_offered": [{"seat": 2, "option": "take"}],
      "players": {
        "1": {"hand_count": 1, "cards_left": 4},
        "2": {"hand_count": 1, "cards_left": 4},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  },
  {
    "name": "R14: cards_left equals hand_count plus up_count after each turn",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": ["3", "4"], "hand_count": 2, "up_pile": ["5", "6", "7"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["5"], "hand_count": 1, "up_pile": ["1", "2", "3"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["6", "6"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "expect": {
      "players": {
        "1": {"hand_count": 1, "up_count": 3, "cards_left": 4},
        "2": {"hand_count": 0, "up_count": 3, "cards_left": 3},
        "3": {"hand_count": 1, "up_count": 3, "cards_left": 4}
      }
    }
  },
  {
    "name": "R15: emptying hand and up_pile ends the game at once and that seat wins",
    "rule": "R15",
    "players": 3,
    "default": "first",
    "given": {
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": [], "hand_count": 0, "up_pile": ["4"], "up_count": 1, "cards_left": 1},
        "2": {"hand": ["1"], "hand_count": 1, "up_pile": ["2", "3", "4"], "up_count": 3, "cards_left": 4},
        "3": {"hand": ["1"], "hand_count": 1, "up_pile": ["2", "3", "4"], "up_count": 3, "cards_left": 4}
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -4, "3": -4},
      "not_offered": [
        {"seat": 2, "option": "1 x1"},
        {"seat": 3, "option": "1 x1"}
      ],
      "players": {
        "1": {"up_pile": [], "up_count": 0, "hand_count": 0, "cards_left": 0},
        "2": {"hand_count": 1, "cards_left": 4},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  },
  {
    "name": "R16: after round 30 the fewest cards_left wins and a tie is shared",
    "rule": "R16",
    "players": 3,
    "default": "first",
    "given": {
      "game": {"round": 29, "pile": [], "top_rank": 0, "run_count": 0},
      "players": {
        "1": {"hand": ["3", "6"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5},
        "2": {"hand": ["1", "4", "4"], "hand_count": 3, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 6},
        "3": {"hand": ["2", "5"], "hand_count": 2, "up_pile": ["7", "8", "9"], "up_count": 3, "cards_left": 5}
      }
    },
    "expect": {
      "winner": [1, 3],
      "standings": {"1": -4, "2": -5, "3": -4},
      "players": {
        "1": {"hand_count": 1, "cards_left": 4},
        "2": {"hand_count": 2, "cards_left": 5},
        "3": {"hand_count": 1, "cards_left": 4}
      }
    }
  }
]
```
````
