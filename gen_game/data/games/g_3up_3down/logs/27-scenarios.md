# 27 scenarios

- time: 2026-10-28T04:41:27+00:00 (103.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5b232851d2d69f6f, reply sha256 abce271d75222c3b

## Sent

````
SPEC:
{
  "name": "3Up Shed (Equal Turns)",
  "summary": "Three players shed a 10-card hand onto a shared pile by matching or beating its top rank. They wipe the pile with three of a rank or a Clear, or pick it up when stuck. The first seats to run out of cards win, and every seat gets the same number of turns.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 30,
    "min_rank": 1,
    "max_rank": 9,
    "copies_per_rank": 3,
    "clear_cards": 3,
    "low_stack_size": 9,
    "mid_stack_size": 9,
    "high_stack_size": 9,
    "clear_stack_size": 3,
    "cards_dealt_per_stack": 3,
    "clears_dealt_per_seat": 1,
    "starting_hand_size": 10,
    "up_pile_size": 3,
    "hand_after_up": 7,
    "max_copies_per_play": 3,
    "run_wipe_threshold": 3,
    "max_rounds": 20,
    "empty_top_rank": 0,
    "clear_sort_value": 10
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards in this seat's secret hand (ranks 1-9 and C).",
        "observable": false
      },
      {
        "key": "up_offer",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Every distinct 3-card set from the dealt hand, each written ascending with C above 9, and the list sorted ascending. Used only at setup.",
        "observable": false
      },
      {
        "key": "up_pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The seat's face-up cards. It is played from only once the hand is empty.",
        "observable": true
      },
      {
        "key": "hand_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the hand.",
        "observable": true
      },
      {
        "key": "up_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the up_pile.",
        "observable": true
      },
      {
        "key": "cards_left",
        "type": "number",
        "visible": "public",
        "initial": 10,
        "meaning": "hand_count + up_count. This is the score: lower is better.",
        "observable": true
      },
      {
        "key": "out",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once cards_left = 0. The seat then skips its turns.",
        "observable": true
      },
      {
        "key": "picked_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many times this seat has picked up the pile.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "low_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          1,
          1,
          2,
          2,
          2,
          3,
          3,
          3
        ],
        "meaning": "The Low stack (ranks 1-3), shuffled at setup.",
        "observable": false
      },
      {
        "key": "mid_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          4,
          4,
          4,
          5,
          5,
          5,
          6,
          6,
          6
        ],
        "meaning": "The Mid stack (ranks 4-6), shuffled at setup.",
        "observable": false
      },
      {
        "key": "high_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          7,
          7,
          7,
          8,
          8,
          8,
          9,
          9,
          9
        ],
        "meaning": "The High stack (ranks 7-9), shuffled at setup.",
        "observable": false
      },
      {
        "key": "clear_stack",
        "type": "list",
        "visible": "none",
        "initial": [
          "C",
          "C",
          "C"
        ],
        "meaning": "The Clear stack.",
        "observable": false
      },
      {
        "key": "pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards currently on the shared play pile.",
        "observable": true
      },
      {
        "key": "top_rank",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rank on top of the pile. 0 means the pile is empty.",
        "observable": true
      },
      {
        "key": "run_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many cards of top_rank have been played in a row on the pile.",
        "observable": true
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
        "key": "lead",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that takes the first turn this round.",
        "observable": false
      },
      {
        "key": "game_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Set true after a round in which at least one seat is out.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Shuffle low_stack, mid_stack and high_stack separately.",
    "In seat order 1, 2, 3, move the top 3 cards of low_stack, then the top 3 of mid_stack, then the top 3 of high_stack, then 1 card of clear_stack into that seat's hand. Each hand then holds 10 cards and every stack is empty.",
    "For each seat, set up_offer to every distinct set of 3 cards from its hand. Each set is written ascending with C counting as 10, and the list is sorted ascending.",
    "Poll all seats at once. Each picks one set from its own up_offer; a missing or invalid answer takes the first set listed.",
    "Move each seat's chosen 3 cards from hand to up_pile. Up piles are public; hands stay secret.",
    "For each seat set hand_count = 7, up_count = 3, cards_left = 10, out = false, picked_up = 0.",
    "Set pile = [], top_rank = 0, run_count = 0, round = 0, game_over = false."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; lead = ((round - 1) mod 3) + 1."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting at seat lead, then lead+1, then lead+2 (seat 3 is followed by seat 1); a seat with out = true is skipped",
      "answer": "One option from the legal plays drawn from the source (hand if hand_count > 0, otherwise up_pile). An option is a rank r with r >= top_rank played as k copies, for k = 1 up to min(3, copies of r held); or a single C; or PICK UP only if no play is legal. Options are listed by ascending rank, then by copies, with C last. A missing or invalid answer takes the first option.",
      "effect": "Right after each seat answers, its choice is applied as in the next step, so the next seat sees the updated pile."
    },
    {
      "action": "update",
      "who": "the seat that just answered (applied after each turn)",
      "answer": null,
      "effect": "Rank play r x k: move k cards of rank r from the source to pile; if top_rank == r then run_count += k, else run_count = k; top_rank = r; if run_count >= 3, clear pile (removed from game), top_rank = 0, run_count = 0. C: remove the C from the source and clear pile (both removed from game), top_rank = 0, run_count = 0. PICK UP: append all of pile to hand, pile = [], picked_up += 1, top_rank = 0, run_count = 0. Then hand_count = len(hand), up_count = len(up_pile), cards_left = hand_count + up_count; if cards_left == 0 then out = true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "After all three turns: if the number of seats with out = true is at least 1, set game_over = true."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if game_over == true or round == 20; otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "game_over == true or round >= 20",
    "rank_by": "0 - you.cards_left",
    "decided_by": "Fewest cards_left wins. If a seat went out, every seat with cards_left = 0 shares the win (one such seat wins alone; two or three is a draw). If round 20 ends with nobody out, the seat with the fewest cards_left wins, and seats tied for fewest share it (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When setup is done, each seat has hand_count 7, up_count 3 and cards_left 10. Its 10 dealt cards were 3 Low (1-3), 3 Mid (4-6), 3 High (7-9) and 1 C."
    },
    {
      "id": "R2",
      "text": "When a seat picks its up set at setup, then exactly those 3 cards move from hand to the public up_pile, and an invalid or missing pick takes the first set of up_offer."
    },
    {
      "id": "R3",
      "text": "When a round starts, round increases by 1 and lead = ((round - 1) mod 3) + 1, so rounds 1, 2, 3, 4 are led by seats 1, 2, 3, 1."
    },
    {
      "id": "R4",
      "text": "When a seat has hand_count > 0, then its legal plays come only from its hand; when hand_count = 0, they come only from its up_pile."
    },
    {
      "id": "R5",
      "text": "When top_rank = t > 0, then a rank r is offered only if r >= t, as 1 to min(3, copies held) copies, and a single C is always offered if held."
    },
    {
      "id": "R6",
      "text": "When top_rank = 0, then every rank held in the source is offered (1 up to the copies held, at most 3) and C if held."
    },
    {
      "id": "R7",
      "text": "When no rank or C play is legal, then PICK UP is the only option."
    },
    {
      "id": "R8",
      "text": "When a seat plays k cards of rank r and top_rank was already r, then run_count increases by k; otherwise run_count = k. In both cases top_rank = r."
    },
    {
      "id": "R9",
      "text": "When run_count reaches 3 or more after a play, then pile is emptied out of the game, top_rank = 0 and run_count = 0."
    },
    {
      "id": "R10",
      "text": "When a seat plays a C, then the C and the whole pile leave the game, top_rank = 0 and run_count = 0."
    },
    {
      "id": "R11",
      "text": "When a seat picks up, then every card of pile goes into its hand, pile becomes empty, picked_up increases by 1, top_rank = 0 and run_count = 0."
    },
    {
      "id": "R12",
      "text": "When any turn ends, then hand_count, up_count and cards_left = hand_count + up_count are recomputed, and cards_left = 0 sets out = true."
    },
    {
      "id": "R13",
      "text": "When a seat has out = true, then it is skipped: it is asked nothing and its attributes do not change."
    },
    {
      "id": "R14",
      "text": "When a missing or invalid answer is given on a turn, then the first listed option is applied."
    },
    {
      "id": "R15",
      "text": "When a round's three turns end with at least one seat out, then game_over = true and the game ends after that round, so every seat has had the same number of turns."
    },
    {
      "id": "R16",
      "text": "When round 20 ends, then the game ends even if nobody is out."
    },
    {
      "id": "R17",
      "text": "When the game ends, then the seats with the lowest cards_left win, and seats tied at the lowest share the win."
    }
  ],
  "offers": [
    {
      "question": "Setup: choose your up set",
      "who": "every seat, simultaneously",
      "options": "Every distinct 3-card set from that seat's own 10-card hand, each ascending with C above 9, the list sorted ascending (up_offer)."
    },
    {
      "question": "Turn: choose a play",
      "who": "the seat whose turn it is, if out = false",
      "options": "From the source (hand if not empty, else up_pile): each rank r >= top_rank held, as 1, 2 or 3 copies up to the number held; 'C' if a C is held. When top_rank = 0, every held rank is offered. Sorted by rank, then by copies, with C last. If none of these exist: only 'PICK UP'."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at 3. Rotating the lead over 3 seats and the equal-turns ending are built for that count."
    },
    {
      "what": "No talk step before turns",
      "why": "The source has no talk. Turns are sequential and fully specified, so adding talk would add a mechanic."
    },
    {
      "what": "rank_by = 0 - cards_left for both endings",
      "why": "A seat that is out has cards_left 0, the lowest possible. Ranking by fewest cards therefore picks exactly the out seats when game_over is true, and the fewest-cards seat at round 20."
    },
    {
      "what": "C sorts as 10 in up_offer",
      "why": "The source says C counts above 9, so a numeric stand-in of 10 keeps the ordering."
    }
  ],
  "simplifications": [
    {
      "what": "A shared top rank is a shared win",
      "why": "The engine has no separate draw. The source's draw (two or three seats out, or a tie for fewest at round 20) becomes a shared win among the tied seats."
    },
    {
      "what": "The turn rotation is described as 'each player in turn starting at seat lead'",
      "why": "The step list is flat. The three turns are one ask over the seats in rotated order, each followed by its update, with out seats skipped."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: up_pile, hand_count, up_count, cards_left, out, picked_up; table: pile, top_rank, run_count, round, game_over.
````

## Reply

````
```json
[
  {
    "name": "After setup each seat holds 7 in hand and 3 up, cards_left 10, and every stack is empty",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "default": "first",
    "rounds": 0,
    "rules": [],
    "expect": {
      "players": {
        "1": {"hand_count": 7, "up_count": 3, "cards_left": 10, "out": false, "picked_up": 0},
        "2": {"hand_count": 7, "up_count": 3, "cards_left": 10, "out": false, "picked_up": 0},
        "3": {"hand_count": 7, "up_count": 3, "cards_left": 10, "out": false, "picked_up": 0}
      },
      "game": {"pile": [], "top_rank": 0, "run_count": 0, "round": 0, "game_over": false},
      "lens": {
        "game": {"low_stack": 0, "mid_stack": 0, "high_stack": 0, "clear_stack": 0},
        "players": {
          "1": {"hand": 7, "up_pile": 3},
          "2": {"hand": 7, "up_pile": 3},
          "3": {"hand": 7, "up_pile": 3}
        }
      }
    }
  },
  {
    "name": "The chosen up set of 3 cards moves from hand to up_pile (only counts asserted, the deal is random)",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "default": "first",
    "rounds": 0,
    "rules": [],
    "expect": {
      "players": {
        "1": {"up_count": 3, "hand_count": 7},
        "2": {"up_count": 3, "hand_count": 7},
        "3": {"up_count": 3, "hand_count": 7}
      },
      "lens": {
        "players": {
          "1": {"hand": 7, "up_pile": 3},
          "2": {"hand": 7, "up_pile": 3},
          "3": {"hand": 7, "up_pile": 3}
        }
      }
    }
  },
  {
    "name": "Round 2 is led by seat 2, so the order is 2, 3, 1",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [7], "up_pile": [8]},
        "2": {"hand": [5], "up_pile": [8]},
        "3": {"hand": [3], "up_pile": [8]}
      },
      "game": {"round": 1, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "game": {"round": 2, "pile": [7], "top_rank": 7, "run_count": 1, "game_over": false},
      "players": {
        "1": {"hand_count": 0, "cards_left": 1, "picked_up": 0},
        "2": {"hand_count": 0, "cards_left": 1, "picked_up": 0},
        "3": {"hand_count": 2, "cards_left": 3, "picked_up": 1}
      },
      "offered": [{"seat": 3, "option": "PICK UP"}]
    }
  },
  {
    "name": "With an empty hand a seat plays from up_pile; with a hand it plays only from the hand",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [], "up_pile": [4, 6], "hand_count": 0, "up_count": 2, "cards_left": 2},
        "2": {"hand": [2], "up_pile": [9]},
        "3": {"hand": [5], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"up_pile": [6], "up_count": 1, "hand_count": 0, "cards_left": 1},
        "2": {"up_pile": [9], "up_count": 1, "hand_count": 2, "cards_left": 3, "picked_up": 1},
        "3": {"hand_count": 0, "cards_left": 1}
      },
      "game": {"pile": [5], "top_rank": 5, "run_count": 1},
      "offered": [{"seat": 2, "option": "PICK UP"}]
    }
  },
  {
    "name": "With top_rank 5, a held 3 is not offered: the first option is 6, and C is offered",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 6, 6, "C"], "up_pile": [8]},
        "2": {"hand": [1], "up_pile": [8]},
        "3": {"hand": [2], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [5], "top_rank": 5, "run_count": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"hand_count": 3, "cards_left": 4},
        "2": {"hand_count": 3, "cards_left": 4, "picked_up": 1},
        "3": {"hand_count": 0, "cards_left": 1}
      },
      "game": {"pile": [2], "top_rank": 2, "run_count": 1},
      "offered": [{"seat": 1, "option": "C"}, {"seat": 2, "option": "PICK UP"}]
    }
  },
  {
    "name": "With an empty pile, any held rank is offered, even 9, and so is C",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [9, 9, "C"], "up_pile": [8]},
        "2": {"hand": [1], "up_pile": [8]},
        "3": {"hand": [2], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"hand_count": 2, "cards_left": 3},
        "2": {"hand_count": 2, "cards_left": 3, "picked_up": 1},
        "3": {"hand_count": 0, "cards_left": 1}
      },
      "game": {"pile": [2], "top_rank": 2, "run_count": 1},
      "offered": [{"seat": 1, "option": "C"}]
    }
  },
  {
    "name": "A seat holding only cards below top_rank and no C is offered only PICK UP",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2], "up_pile": [8]},
        "2": {"hand": [3], "up_pile": [8]},
        "3": {"hand": [4], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [5], "top_rank": 5, "run_count": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"hand_count": 3, "cards_left": 4, "picked_up": 1},
        "2": {"hand_count": 0, "cards_left": 1},
        "3": {"hand_count": 0, "cards_left": 1}
      },
      "game": {"pile": [3, 4], "top_rank": 4, "run_count": 1},
      "offered": [{"seat": 1, "option": "PICK UP"}],
      "not_offered": [{"seat": 1, "option": "C"}]
    }
  },
  {
    "name": "Playing the same rank as the top adds to run_count",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [5, 9], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "3": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true}
      },
      "game": {"round": 0, "pile": [5], "top_rank": 5, "run_count": 1},
      "status": {"2": "out", "3": "out"}
    },
    "rules": [],
    "expect": {
      "game": {"pile": [5, 5], "top_rank": 5, "run_count": 2},
      "players": {"1": {"hand_count": 1, "cards_left": 2}}
    }
  },
  {
    "name": "Playing a higher rank resets run_count to the copies played",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 4, 9], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "3": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true}
      },
      "game": {"round": 0, "pile": [3, 3], "top_rank": 3, "run_count": 2},
      "status": {"2": "out", "3": "out"}
    },
    "rules": [],
    "expect": {
      "game": {"pile": [3, 3, 4], "top_rank": 4, "run_count": 1},
      "players": {"1": {"hand_count": 2, "cards_left": 3}}
    }
  },
  {
    "name": "A third 5 in a row wipes the pile",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [5, 9], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "3": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true}
      },
      "game": {"round": 0, "pile": [2, 5, 5], "top_rank": 5, "run_count": 2},
      "status": {"2": "out", "3": "out"}
    },
    "rules": [],
    "expect": {
      "game": {"pile": [], "top_rank": 0, "run_count": 0},
      "players": {"1": {"hand_count": 1, "cards_left": 2}}
    }
  },
  {
    "name": "Playing C removes it and the whole pile",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["C", 9], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "3": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true}
      },
      "game": {"round": 0, "pile": [3, 5], "top_rank": 5, "run_count": 1},
      "status": {"2": "out", "3": "out"}
    },
    "rules": [{"seat": 1, "options_include": "C"}],
    "expect": {
      "game": {"pile": [], "top_rank": 0, "run_count": 0},
      "players": {"1": {"hand_count": 1, "cards_left": 2, "picked_up": 0}}
    }
  },
  {
    "name": "Picking up moves the whole pile into the hand and resets the pile",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "3": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true}
      },
      "game": {"round": 0, "pile": [3, 6, 6], "top_rank": 6, "run_count": 2},
      "status": {"2": "out", "3": "out"}
    },
    "rules": [{"seat": 1, "options_include": "PICK UP"}],
    "expect": {
      "game": {"pile": [], "top_rank": 0, "run_count": 0},
      "players": {"1": {"hand_count": 4, "up_count": 1, "cards_left": 5, "picked_up": 1}}
    }
  },
  {
    "name": "Counts are recomputed after each turn and a seat with no cards left is out",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4], "up_pile": [], "hand_count": 1, "up_count": 0, "cards_left": 1},
        "2": {"hand": [6], "up_pile": [8]},
        "3": {"hand": [1], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"hand_count": 0, "up_count": 0, "cards_left": 0, "out": true},
        "2": {"hand_count": 0, "up_count": 1, "cards_left": 1, "out": false},
        "3": {"hand_count": 3, "up_count": 1, "cards_left": 4, "out": false, "picked_up": 1}
      },
      "game": {"pile": [], "top_rank": 0, "run_count": 0}
    }
  },
  {
    "name": "An out seat is skipped and asked nothing",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3], "up_pile": [8]},
        "2": {"hand": [], "up_pile": [], "hand_count": 0, "up_count": 0, "cards_left": 0, "out": true, "picked_up": 0},
        "3": {"hand": [4], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0},
      "status": {"2": "out"}
    },
    "rules": [],
    "expect": {
      "game": {"pile": [3, 4], "top_rank": 4, "run_count": 1},
      "players": {
        "1": {"cards_left": 1},
        "2": {"cards_left": 0, "picked_up": 0, "out": true, "hand_count": 0, "up_count": 0},
        "3": {"cards_left": 1}
      },
      "not_offered": [{"seat": 2, "option": "PICK UP"}, {"seat": 2, "option": "C"}]
    }
  },
  {
    "name": "Lead seat 3 goes out in round 3, seats 1 and 2 still play their turns, then the game ends",
    "rule": "R15",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [6, 7], "up_pile": [8]},
        "2": {"hand": [5], "up_pile": [8]},
        "3": {"hand": [4], "up_pile": [], "hand_count": 1, "up_count": 0, "cards_left": 1}
      },
      "game": {"round": 2, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "winner": 3,
      "standings": {"1": -2, "2": -4, "3": 0},
      "game": {"round": 3, "game_over": true},
      "players": {
        "1": {"cards_left": 2},
        "2": {"cards_left": 4, "picked_up": 1},
        "3": {"cards_left": 0, "out": true}
      },
      "offered": [{"seat": 2, "option": "PICK UP"}]
    }
  },
  {
    "name": "Round 20 ends the game with nobody out; the fewest cards wins",
    "rule": "R16",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [5, 6, 6, 6], "up_pile": [9]},
        "2": {"hand": [1, 1], "up_pile": [9]},
        "3": {"hand": [2, 3, 3], "up_pile": [9]}
      },
      "game": {"round": 19, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "winner": 2,
      "standings": {"1": -4, "2": -2, "3": -3},
      "game": {"round": 20, "game_over": false, "pile": [1, 2, 5], "top_rank": 5},
      "players": {
        "1": {"cards_left": 4, "out": false},
        "2": {"cards_left": 2, "out": false},
        "3": {"cards_left": 3, "out": false}
      }
    }
  },
  {
    "name": "Two seats tied for fewest cards at round 20 share the win",
    "rule": "R17",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [3, 4, 4], "up_pile": [9]},
        "2": {"hand": [1], "up_pile": [9, 9]},
        "3": {"hand": [2], "up_pile": [9, 9]}
      },
      "game": {"round": 19, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": -3, "2": -2, "3": -2},
      "game": {"round": 20}
    }
  },
  {
    "name": "Two seats going out in the same round share the win",
    "rule": "R17",
    "players": 3,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4], "up_pile": [], "hand_count": 1, "up_count": 0, "cards_left": 1},
        "2": {"hand": [6], "up_pile": [], "hand_count": 1, "up_count": 0, "cards_left": 1},
        "3": {"hand": [5], "up_pile": [8]}
      },
      "game": {"round": 0, "pile": [], "top_rank": 0, "run_count": 0}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 0, "2": 0, "3": -4},
      "game": {"round": 1, "game_over": true},
      "players": {
        "1": {"out": true},
        "2": {"out": true},
        "3": {"out": false, "picked_up": 1, "cards_left": 4}
      }
    }
  }
]
```
````
