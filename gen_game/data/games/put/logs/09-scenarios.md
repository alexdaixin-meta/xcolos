# 09 scenarios

- time: 2026-10-28T06:21:36+00:00 (61.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 dcbf7ae26e696809, reply sha256 75f457e3c7fb367d

## Sent

````
SPEC:
{
  "name": "Put: Show One, Keep Three",
  "summary": "A two-player betting card duel over 40 hands. Each player holds 3 hidden cards and 1 face-up card, calls are made to raise the stake, and then each secretly orders 3 of their 4 cards to fight 3 tricks.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "hands_total": 40,
    "deck_size": 52,
    "cards_dealt_per_player": 4,
    "private_cards_per_player": 3,
    "face_up_cards_per_player": 1,
    "cards_played": 3,
    "tricks_per_hand": 3,
    "tricks_to_win_hand": 2,
    "starting_points": 0,
    "starting_hands_won": 0,
    "stake_pass_pass": 1,
    "stake_put_see": 2,
    "stake_pass_put_see": 2,
    "stake_reput_see": 4,
    "fold_to_put_points": 1,
    "fold_to_reput_points": 2,
    "fold_to_put_after_pass_points": 1,
    "strength_3": 13,
    "strength_2": 12,
    "strength_A": 11,
    "strength_K": 10,
    "strength_Q": 9,
    "strength_J": 8,
    "strength_10": 7,
    "strength_9": 6,
    "strength_8": 5,
    "strength_7": 4,
    "strength_6": 3,
    "strength_5": 2,
    "strength_4": 1,
    "suits": 4,
    "rank_points_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match points scored so far.",
        "observable": true
      },
      {
        "key": "hands_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Hands won, either on tricks or because the opponent folded. Used as the tie-break.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's 3 private cards this hand. Each card is coded as strength*10+suit, e.g. 134 is a 3 (strength 13) of suit 4.",
        "observable": false
      },
      {
        "key": "face_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's 4th card, dealt face up and announced to both players (same coding).",
        "observable": true
      },
      {
        "key": "play",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The ordered list of 3 different cards the player secretly chose from hand plus face_up. It is revealed in the announcement.",
        "observable": false
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won in the current hand (0 to 3).",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 52 codes s*10+u for strength s in 1..13 and suit u in 1..4",
        "meaning": "The shuffled deck that cards are dealt from. It is refilled every hand.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, from 1 to 40. When odd, seat 1 (A) is the Caller; when even, seat 2 (B) is the Caller.",
        "observable": true
      },
      {
        "key": "caller_call",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The Caller's call: PUT or PASS.",
        "observable": false
      },
      {
        "key": "responder_answer",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The Responder's answer: SEE, FOLD, RE-PUT, PUT or PASS.",
        "observable": false
      },
      {
        "key": "caller_answer",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The Caller's second answer: SEE or FOLD, or empty if step 4 did not happen.",
        "observable": false
      },
      {
        "key": "stake",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The stake played for on tricks: 1, 2 or 4.",
        "observable": false
      },
      {
        "key": "folded",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when a FOLD ended the hand before play.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is player A and seat 2 is player B.",
    "Both players start with points = 0 and hands_won = 0.",
    "hand_number is set to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Refill deck with all 52 cards. Clear each player's hand and play, set tricks_won = 0 and face_up = 0. Set stake = 0, folded = false, and caller_call, responder_answer and caller_answer to empty."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal: for each player, draw 3 cards at random from deck into hand, then draw 1 card at random from deck into face_up. Each drawn card is removed from deck."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce hand_number, who is Caller and who is Responder, and both players' face_up cards."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand and face_up, the opponent's face_up, and both players' points and hands_won."
    },
    {
      "action": "ask",
      "who": "the Caller (seat 1 if hand_number is odd, seat 2 if even)",
      "answer": "PUT or PASS",
      "effect": "Set caller_call to the answer."
    },
    {
      "action": "ask",
      "who": "the Responder (seat 2 if hand_number is odd, seat 1 if even)",
      "answer": "If caller_call = PUT: SEE, FOLD or RE-PUT. If caller_call = PASS: PUT or PASS.",
      "effect": "Set responder_answer to the answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If caller_call = PUT and responder_answer = SEE, set stake = 2. If caller_call = PUT and responder_answer = FOLD, the Caller gets points += 1 and hands_won += 1, and folded = true. If caller_call = PASS and responder_answer = PASS, set stake = 1."
    },
    {
      "action": "ask",
      "who": "the Caller, only when responder_answer is RE-PUT or PUT",
      "answer": "SEE or FOLD",
      "effect": "Set caller_answer to the answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If responder_answer = RE-PUT and caller_answer = SEE, set stake = 4. If responder_answer = RE-PUT and caller_answer = FOLD, the Responder gets points += 2 and hands_won += 1, and folded = true. If responder_answer = PUT and caller_answer = SEE, set stake = 2. If responder_answer = PUT and caller_answer = FOLD, the Responder gets points += 1 and hands_won += 1, and folded = true."
    },
    {
      "action": "poll",
      "who": "all players, only when folded = false",
      "answer": "One of the 24 ordered lists of 3 different cards drawn from the player's 4 cards (hand plus face_up).",
      "effect": "Set each player's play to the chosen ordered list. Neither player sees the other's choice until both are in."
    },
    {
      "action": "update",
      "who": "all players, only when folded = false",
      "answer": null,
      "effect": "For each position i = 1, 2, 3, compare floor(play[i]/10) between the two players. The higher strength gets tricks_won += 1. Equal strength gives the trick to no one."
    },
    {
      "action": "update",
      "who": "all players, only when folded = false",
      "answer": null,
      "effect": "A player with tricks_won >= 2 gets points += stake and hands_won += 1. Otherwise nobody scores."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce caller_call, responder_answer, caller_answer, all 8 cards (both hands and face_up cards, including cards left out or never played), both play lists, tricks_won, the hand result, and both players' points and hands_won."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "hand_number += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_number > 40. Otherwise run the round again."
    }
  ],
  "ending": {
    "condition": "hand_number > 40",
    "rank_by": "you.points * 1000 + you.hands_won",
    "decided_by": "After 40 hands the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the players share the result, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card strengths are 3=13, 2=12, A=11, K=10, Q=9, J=8, 10=7, 9=6, 8=5, 7=4, 6=3, 5=2, 4=1, and suits do not matter."
    },
    {
      "id": "R2",
      "text": "Both players start with 0 points and 0 hands won, and the match lasts exactly 40 hands."
    },
    {
      "id": "R3",
      "text": "When hand_number is odd, seat 1 (A) is the Caller and seat 2 (B) is the Responder; when it is even, seat 2 is the Caller and seat 1 is the Responder."
    },
    {
      "id": "R4",
      "text": "Each hand, all 52 cards are shuffled and each player gets 3 private cards in hand and 1 face_up card that is announced to both players."
    },
    {
      "id": "R5",
      "text": "The Caller first says PUT or PASS."
    },
    {
      "id": "R6",
      "text": "When the Caller said PUT and the Responder says SEE, the stake is 2 and play follows."
    },
    {
      "id": "R7",
      "text": "When the Caller said PUT and the Responder says FOLD, the Caller scores 1 point and 1 hand won, and the hand ends without play."
    },
    {
      "id": "R8",
      "text": "When the Caller said PUT and the Responder says RE-PUT, the Caller must answer SEE or FOLD."
    },
    {
      "id": "R9",
      "text": "When the Caller said PASS and the Responder says PASS, the stake is 1 and play follows."
    },
    {
      "id": "R10",
      "text": "When the Caller said PASS and the Responder says PUT, the Caller must answer SEE or FOLD."
    },
    {
      "id": "R11",
      "text": "When the Caller answers SEE after a RE-PUT, the stake is 4 and play follows."
    },
    {
      "id": "R12",
      "text": "When the Caller answers FOLD after a RE-PUT, the Responder scores 2 points and 1 hand won, and the hand ends without play."
    },
    {
      "id": "R13",
      "text": "When the Caller answers SEE after PASS then PUT, the stake is 2 and play follows."
    },
    {
      "id": "R14",
      "text": "When the Caller answers FOLD after PASS then PUT, the Responder scores 1 point and 1 hand won, and the hand ends without play."
    },
    {
      "id": "R15",
      "text": "When play happens, both players simultaneously choose an ordered list of 3 different cards from their 4 cards, and the face-up card may be used or left out."
    },
    {
      "id": "R16",
      "text": "Trick i compares the i-th cards of the two lists; the higher strength wins the trick, and equal strength ties it so no one gets it."
    },
    {
      "id": "R17",
      "text": "When a player wins at least 2 of the 3 tricks, that player scores the stake (1, 2 or 4) and 1 hand won."
    },
    {
      "id": "R18",
      "text": "When no player wins at least 2 tricks (e.g. 1-1 with a tie, 1 win and 2 ties, or 3 ties), nobody scores that hand."
    },
    {
      "id": "R19",
      "text": "After every hand, all calls, all 8 cards, the result, and both players' points and hands won are announced."
    },
    {
      "id": "R20",
      "text": "After hand 40 the match ends; more points wins, then more hands won breaks a tie, and if both are equal it is a draw."
    }
  ],
  "offers": [
    {
      "question": "Caller's call",
      "who": "the Caller",
      "options": "PUT, PASS"
    },
    {
      "question": "Responder's answer",
      "who": "the Responder",
      "options": "If caller_call = PUT: SEE, FOLD, RE-PUT. If caller_call = PASS: PUT, PASS."
    },
    {
      "question": "Caller's answer",
      "who": "the Caller, only when responder_answer is RE-PUT or PUT",
      "options": "SEE, FOLD"
    },
    {
      "question": "Play",
      "who": "both seats, only when folded = false",
      "options": "Each of the 24 ordered lists of 3 different cards from that seat's own 3 hand cards plus its face_up card."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (suggested 2)",
      "why": "The designer fixed the game at 2. The call structure (Caller/Responder alternating by hand) and the head-to-head tricks only work with two seats."
    },
    {
      "what": "Card coding as strength*10+suit",
      "why": "Strength is then floor(card/10), which makes trick comparison pure arithmetic while keeping 52 distinct cards."
    },
    {
      "what": "Play offered as one choice among 24 ordered triples",
      "why": "This makes the simultaneous secret ordered list a single poll with only legal options (3 different cards from own 4)."
    },
    {
      "what": "No free-text talk step",
      "why": "The rules contain no talk. With two players the calls themselves are the signalling and bluffing channel."
    },
    {
      "what": "Strategy check",
      "why": "A thoughtful player weighs the opponent's visible face-up card against their own, bluffs PUT or RE-PUT with weak hands, folds cheaply when outmatched, and orders cards to dodge the opponent's likely ordering (e.g. sacrificing a weak card against a strong one)."
    },
    {
      "what": "rank_by weight 1000",
      "why": "Hands won is at most 40, so points*1000 + hands_won ranks by points first, then by hands won."
    }
  ],
  "simplifications": [
    {
      "what": "The Caller and Responder are worked out from hand_number parity in each step's 'who'",
      "why": "The engine has no role-swap action; parity gives the same alternation."
    },
    {
      "what": "Conditional steps 4 and 5\u20137 are written as individual steps with when-conditions on caller_call, responder_answer and folded",
      "why": "The step list is flat, and per-step conditions reproduce the branching of the hand faithfully."
    },
    {
      "what": "Trick comparison between the two players' play lists uses a table-side comparison",
      "why": "Comparing one player's attribute with another's needs the documented workaround of copying values to the table."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: points, hands_won, face_up; table: hand_number.
````

## Reply

````
```json
[
  {
    "name": "Setup: both players start at 0 points and 0 hands won, on hand 1",
    "rule": "R2",
    "players": 2,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"points": 0, "hands_won": 0},
        "2": {"points": 0, "hands_won": 0}
      },
      "game": {"hand_number": 1}
    }
  },
  {
    "name": "Hand 1 (odd): seat 1 is Caller, seat 2 Responder; PUT then FOLD scores for seat 1",
    "rule": "R3",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 1, "hands_won": 1},
        "2": {"points": 0, "hands_won": 0}
      },
      "game": {"hand_number": 2},
      "offered": [
        {"seat": 1, "option": "PUT"},
        {"seat": 2, "option": "RE-PUT"}
      ],
      "not_offered": [
        {"seat": 2, "option": "PASS"},
        {"seat": 2, "option": "PUT"}
      ]
    }
  },
  {
    "name": "Hand 2 (even): seat 2 is Caller, seat 1 Responder; PUT then FOLD scores for seat 2",
    "rule": "R3",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"hand_number": 2}},
    "rules": [
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0, "hands_won": 0},
        "2": {"points": 1, "hands_won": 1}
      },
      "game": {"hand_number": 3},
      "offered": [
        {"seat": 2, "option": "PUT"},
        {"seat": 1, "option": "RE-PUT"}
      ],
      "not_offered": [
        {"seat": 1, "option": "PASS"},
        {"seat": 1, "option": "PUT"}
      ]
    }
  },
  {
    "name": "Each player is dealt 3 private cards; 8 cards leave the 52-card deck (counts only, the deal is random)",
    "rule": "R4",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "lens": {
        "game": {"deck": 44},
        "players": {"1": {"hand": 3}, "2": {"hand": 3}}
      },
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "Caller is offered PUT and PASS first; after PUT the Responder is not offered PUT or PASS",
    "rule": "R5",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "PUT"},
        {"seat": 1, "option": "PASS"},
        {"seat": 2, "option": "SEE"},
        {"seat": 2, "option": "FOLD"},
        {"seat": 2, "option": "RE-PUT"}
      ],
      "not_offered": [
        {"seat": 2, "option": "PASS"},
        {"seat": 2, "option": "PUT"}
      ]
    }
  },
  {
    "name": "PUT then SEE goes straight to play: the Caller gets no second question (trick result is random, not asserted)",
    "rule": "R6",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "SEE"}
    ],
    "expect": {
      "game": {"hand_number": 2},
      "not_offered": [
        {"seat": 1, "option": "SEE"},
        {"seat": 1, "option": "FOLD"}
      ]
    }
  },
  {
    "name": "PUT then FOLD: the Caller scores 1 point and 1 hand won, with no play",
    "rule": "R7",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"points": 3, "hands_won": 2},
        "2": {"points": 5, "hands_won": 4}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 4, "hands_won": 3},
        "2": {"points": 5, "hands_won": 4}
      },
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "PUT then RE-PUT: the Caller is offered SEE and FOLD",
    "rule": "R8",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "RE-PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "SEE"},
        {"seat": 1, "option": "FOLD"}
      ],
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "PASS then PASS goes straight to play: no SEE/FOLD question for the Caller (result random, not asserted)",
    "rule": "R9",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "PASS"},
      {"seat": 2, "options_include": "PASS"}
    ],
    "expect": {
      "game": {"hand_number": 2},
      "offered": [
        {"seat": 2, "option": "PUT"},
        {"seat": 2, "option": "PASS"}
      ],
      "not_offered": [
        {"seat": 1, "option": "SEE"},
        {"seat": 1, "option": "FOLD"},
        {"seat": 2, "option": "RE-PUT"},
        {"seat": 2, "option": "SEE"}
      ]
    }
  },
  {
    "name": "PASS then PUT: the Caller is offered SEE and FOLD",
    "rule": "R10",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PASS"},
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "SEE"},
        {"seat": 1, "option": "FOLD"}
      ],
      "not_offered": [
        {"seat": 2, "option": "RE-PUT"}
      ],
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "PUT, RE-PUT, SEE leads to play and the hand completes (stake 4 result is random, not asserted)",
    "rule": "R11",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "RE-PUT"},
      {"seat": 1, "options_include": "SEE"}
    ],
    "expect": {
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "FOLD after RE-PUT: the Responder scores 2 points and 1 hand won",
    "rule": "R12",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "RE-PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0, "hands_won": 0},
        "2": {"points": 2, "hands_won": 1}
      },
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "PASS, PUT, SEE leads to play and the hand completes (result random, not asserted)",
    "rule": "R13",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "PASS"},
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "SEE"}
    ],
    "expect": {
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "FOLD after PASS then PUT: the Responder scores 1 point and 1 hand won",
    "rule": "R14",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "PASS"},
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0, "hands_won": 0},
        "2": {"points": 1, "hands_won": 1}
      },
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "Hand 2 with seat 2 as Caller: FOLD after PASS then PUT gives seat 1 (the Responder) 1 point",
    "rule": "R14",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"hand_number": 2}},
    "rules": [
      {"seat": 2, "options_include": "PASS"},
      {"seat": 1, "options_include": "PUT"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {
        "1": {"points": 1, "hands_won": 1},
        "2": {"points": 0, "hands_won": 0}
      },
      "game": {"hand_number": 3}
    }
  },
  {
    "name": "When play happens, the hand is played out and the match moves on (cards random; only the hand number is asserted)",
    "rule": "R15",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "PASS"},
      {"seat": 2, "options_include": "PASS"}
    ],
    "expect": {
      "game": {"hand_number": 2}
    }
  },
  {
    "name": "After hand 40 the match ends: equal points, more hands won wins",
    "rule": "R20",
    "players": 2,
    "seed": 16,
    "default": "decline",
    "given": {
      "players": {
        "1": {"points": 5, "hands_won": 3},
        "2": {"points": 4, "hands_won": 10}
      },
      "game": {"hand_number": 40}
    },
    "rules": [
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 5003, "2": 5011},
      "players": {
        "1": {"points": 5, "hands_won": 3},
        "2": {"points": 5, "hands_won": 11}
      }
    }
  },
  {
    "name": "After hand 40 the match ends: more points wins despite fewer hands won",
    "rule": "R20",
    "players": 2,
    "seed": 17,
    "default": "decline",
    "given": {
      "players": {
        "1": {"points": 10, "hands_won": 2},
        "2": {"points": 3, "hands_won": 20}
      },
      "game": {"hand_number": 40}
    },
    "rules": [
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 10002, "2": 4021},
      "players": {
        "1": {"points": 10, "hands_won": 2},
        "2": {"points": 4, "hands_won": 21}
      }
    }
  },
  {
    "name": "After hand 40 the match ends: equal points and hands won is a shared draw",
    "rule": "R20",
    "players": 2,
    "seed": 18,
    "default": "decline",
    "given": {
      "players": {
        "1": {"points": 5, "hands_won": 4},
        "2": {"points": 4, "hands_won": 3}
      },
      "game": {"hand_number": 40}
    },
    "rules": [
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 5004, "2": 5004},
      "players": {
        "1": {"points": 5, "hands_won": 4},
        "2": {"points": 5, "hands_won": 4}
      }
    }
  },
  {
    "name": "Hand 40 is the last: the match ends after it with the scores from that hand",
    "rule": "R2",
    "players": 2,
    "seed": 19,
    "default": "decline",
    "given": {"game": {"hand_number": 40}},
    "rules": [
      {"seat": 2, "options_include": "PUT"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 0, "2": 1001},
      "players": {
        "1": {"points": 0, "hands_won": 0},
        "2": {"points": 1, "hands_won": 1}
      }
    }
  }
]
```
````
