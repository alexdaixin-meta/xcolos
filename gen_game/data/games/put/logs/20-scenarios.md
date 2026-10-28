# 20 scenarios

- time: 2026-10-28T06:35:26+00:00 (63.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 12d13805816e90cc, reply sha256 6ca8cf633ee00085

## Sent

````
SPEC:
{
  "name": "Put: Twelve Hands",
  "summary": "Two players play 12 hands of three-card Put. Each hand they may check or Put, then see or fold, then secretly order their cards for three tricks. The higher total score wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "hands": 12,
    "deck_size": 52,
    "copies_per_rank": 4,
    "ranks": 13,
    "cards_per_player": 3,
    "face_up_cards_per_player": 1,
    "tricks_per_hand": 3,
    "fold_points": 1,
    "check_win_points": 1,
    "put_seen_points": 3,
    "start_score": 0,
    "max_puts_per_hand": 1
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total points so far in the match",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "This hand's 3 cards in the order dealt, as rank values (4=1, 5=2, 6=3, 7=4, 8=5, 9=6, 10=7, J=8, Q=9, K=10, A=11, 2=12, 3=13)",
        "observable": false
      },
      {
        "key": "up_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rank value of the first dealt card, which is face up",
        "observable": true
      },
      {
        "key": "order",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's 3 cards in the chosen play order. It is revealed at Results.",
        "observable": false
      },
      {
        "key": "tricks",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won this hand",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "52 cards: rank values 1 to 13, four of each",
        "meaning": "The shuffled deck that cards are dealt from",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current hand, from 1 to 12",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the leader: 1 in odd hands, 2 in even hands",
        "observable": true
      },
      {
        "key": "leader_call",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The leader's call: Check or Put",
        "observable": true
      },
      {
        "key": "responder_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The responder's action: See, Fold, Check or Put",
        "observable": true
      },
      {
        "key": "leader_reply",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The leader's reply to a responder Put: See or Fold. Empty if there was none.",
        "observable": true
      },
      {
        "key": "putter",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that made the Put this hand, or 0 if nobody put",
        "observable": true
      },
      {
        "key": "folded",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether someone folded this hand",
        "observable": true
      }
    ]
  },
  "setup": [
    "Both players' scores are set to 0.",
    "hand_number is set to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "hand_number += 1; leader = 1 if hand_number is odd, else 2; deck is rebuilt as the full 52 cards (rank values 1 to 13, four each); each player's hand, order, tricks and up_card are reset; leader_call, responder_action and leader_reply are set to empty; putter = 0; folded = false"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal: 3 times for each player, a random card is removed from deck and appended to that player's hand. Each player's up_card = the first card of their hand."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand and both up_cards."
    },
    {
      "action": "ask",
      "who": "the leader (seat 1 in odd hands, seat 2 in even hands)",
      "answer": "one of: Check, Put",
      "effect": "leader_call = answer; if Put, putter = leader"
    },
    {
      "action": "ask",
      "who": "the responder (the seat that is not the leader)",
      "answer": "if leader_call = Put: one of See, Fold; if leader_call = Check: one of Check, Put",
      "effect": "responder_action = answer; if answer = Put, putter = responder; if answer = Fold, folded = true"
    },
    {
      "action": "ask",
      "who": "the leader, only when leader_call = Check and responder_action = Put",
      "answer": "one of: See, Fold",
      "effect": "leader_reply = answer; if Fold, folded = true"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when folded = true: the putter's score += 1; the folder scores 0; no cards are played"
    },
    {
      "action": "poll",
      "who": "all players, only when folded = false",
      "answer": "one of the 6 orders of the player's own three cards, by dealt position: 1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2, 3-2-1",
      "effect": "Each player's order = their hand rearranged by the chosen permutation. Nobody sees the other's order until both are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when folded = false: for each trick i from 1 to 3, the player whose order[i] is higher gets tricks += 1; equal values give no one a trick"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when folded = false and putter = 0: the player with more tricks scores += 1, and nobody scores if tricks are equal. When folded = false and putter > 0: if the putter's tricks > the opponent's tricks, the putter's score += 3; otherwise the opponent's score += 3."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal both hands, both orders, each trick's result, tricks, points scored this hand and the total scores."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_number = 12; otherwise continue to the next hand."
    }
  ],
  "ending": {
    "condition": "hand_number = 12",
    "rank_by": "you.score",
    "decided_by": "After hand 12 the player with the higher total score wins; equal totals share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card ranks from highest to lowest are 3, 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, and suits do not matter."
    },
    {
      "id": "R2",
      "text": "The match is exactly 12 hands, and both players start at 0 points."
    },
    {
      "id": "R3",
      "text": "When hand_number is odd, seat 1 leads; when it is even, seat 2 leads."
    },
    {
      "id": "R4",
      "text": "Each hand, a full 52-card deck is shuffled and each player is dealt 3 cards, so the deck holds 46 after the deal."
    },
    {
      "id": "R5",
      "text": "Each player's first dealt card is visible to both players, and their other two cards are visible only to that player."
    },
    {
      "id": "R6",
      "text": "The leader chooses Check or Put."
    },
    {
      "id": "R7",
      "text": "When the leader puts, the responder chooses See or Fold."
    },
    {
      "id": "R8",
      "text": "When the leader checks, the responder chooses Check or Put."
    },
    {
      "id": "R9",
      "text": "When the leader checked and the responder put, the leader chooses See or Fold."
    },
    {
      "id": "R10",
      "text": "Only one Put is made per hand: a player facing a Put is never offered Put."
    },
    {
      "id": "R11",
      "text": "When a player folds, the putter scores 1 point, the folder scores 0, and no cards are played."
    },
    {
      "id": "R12",
      "text": "When nobody folded, both players secretly and at the same moment choose an order of their 3 cards."
    },
    {
      "id": "R13",
      "text": "Trick i compares the two players' i-th played cards: the higher rank wins the trick, and equal ranks give the trick to no one."
    },
    {
      "id": "R14",
      "text": "When both players checked, the player with more tricks scores 1 point, and equal tricks score nothing."
    },
    {
      "id": "R15",
      "text": "When a Put was seen and the putter won strictly more tricks, the putter scores 3 points."
    },
    {
      "id": "R16",
      "text": "When a Put was seen and the putter won equal or fewer tricks, the opponent scores 3 points."
    },
    {
      "id": "R17",
      "text": "At the end of each hand, all cards, both orders, the trick results and the scores are revealed."
    },
    {
      "id": "R18",
      "text": "After hand 12 the higher total score wins, and equal totals are a draw."
    }
  ],
  "offers": [
    {
      "question": "Leader's call",
      "who": "the leader",
      "options": "Check, Put"
    },
    {
      "question": "Responder's action",
      "who": "the responder",
      "options": "if the leader put: See, Fold; if the leader checked: Check, Put"
    },
    {
      "question": "Leader's reply",
      "who": "the leader, only after leader Check and responder Put",
      "options": "See, Fold"
    },
    {
      "question": "Card order",
      "who": "both seats, only when nobody folded",
      "options": "1-2-3, 1-3-2, 2-1-3, 2-3-1, 3-1-2, 3-2-1 (positions in the dealt order)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the game at 2. It is a heads-up bluffing duel, and the leader/responder structure is built for two seats."
    },
    {
      "what": "Ranks stored as numbers 1 (for 4) to 13 (for 3)",
      "why": "Tricks are then decided by a plain numeric comparison."
    },
    {
      "what": "Card order answered as a permutation of dealt positions",
      "why": "This gives a fixed choice list that names the player's own cards unambiguously."
    },
    {
      "what": "No talk step",
      "why": "The rules say talk is not part of the game."
    },
    {
      "what": "Strategy at the table",
      "why": "A good player reads the opponent's face-up card, bluffs or value-puts with their hidden cards, and chooses a card order that anticipates the opponent's ordering."
    }
  ],
  "simplifications": [],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, up_card, tricks; table: hand_number, leader, leader_call, responder_action, leader_reply, putter, folded.
````

## Reply

````
```json
[
  {
    "name": "Setup: both scores start at 0 and no hand has been played",
    "rule": "R2",
    "players": 2,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}},
      "game": {"hand_number": 0}
    }
  },
  {
    "name": "Match lasts exactly 12 hands: every hand the leader puts and the responder folds, 6-6 draw",
    "rule": "R2",
    "players": 2,
    "seed": 2,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put", "times": "all"},
      {"seat": 1, "options_include": "Fold", "times": "all"},
      {"seat": 2, "options_include": "Put", "times": "all"},
      {"seat": 2, "options_include": "Fold", "times": "all"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 6, "2": 6},
      "players": {"1": {"score": 6}, "2": {"score": 6}},
      "game": {"hand_number": 12}
    }
  },
  {
    "name": "Hand 1 is odd so seat 1 leads",
    "rule": "R3",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "game": {"hand_number": 1, "leader": 1, "leader_call": "Put", "responder_action": "Fold", "putter": 1, "folded": true},
      "players": {"1": {"score": 1}, "2": {"score": 0}},
      "offered": [{"seat": 1, "option": "Check"}, {"seat": 1, "option": "Put"}],
      "not_offered": [{"seat": 2, "option": "Check"}]
    }
  },
  {
    "name": "Hand 2 is even so seat 2 leads",
    "rule": "R3",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"hand_number": 1}},
    "rules": [
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "Fold"}
    ],
    "expect": {
      "game": {"hand_number": 2, "leader": 2, "leader_call": "Put", "responder_action": "Fold", "putter": 2, "folded": true},
      "players": {"1": {"score": 0}, "2": {"score": 1}},
      "offered": [{"seat": 2, "option": "Check"}, {"seat": 2, "option": "Put"}],
      "not_offered": [{"seat": 1, "option": "Check"}, {"seat": 1, "option": "Put"}]
    }
  },
  {
    "name": "After the deal each player holds 3 cards and the deck holds 46",
    "rule": "R4",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "lens": {"game": {"deck": 46}, "players": {"1": {"hand": 3}, "2": {"hand": 3}}}
    }
  },
  {
    "name": "Each player is dealt three cards, the first of which is the face-up card (values are chance, only counts asserted)",
    "rule": "R5",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "lens": {"players": {"1": {"hand": 3}, "2": {"hand": 3}}},
      "game": {"folded": true}
    }
  },
  {
    "name": "Leader is offered Check and Put and checks",
    "rule": "R6",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Check"}
    ],
    "expect": {
      "game": {"leader_call": "Check", "responder_action": "Check", "putter": 0, "folded": false},
      "offered": [{"seat": 1, "option": "Check"}, {"seat": 1, "option": "Put"}]
    }
  },
  {
    "name": "Leader puts, responder is offered See and Fold and sees",
    "rule": "R7",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "See"}
    ],
    "expect": {
      "game": {"leader_call": "Put", "responder_action": "See", "putter": 1, "folded": false, "leader_reply": ""},
      "offered": [{"seat": 2, "option": "See"}, {"seat": 2, "option": "Fold"}]
    }
  },
  {
    "name": "Leader checks, responder is offered Check and Put and puts",
    "rule": "R8",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "See"}
    ],
    "expect": {
      "game": {"leader_call": "Check", "responder_action": "Put", "leader_reply": "See", "putter": 2, "folded": false},
      "offered": [{"seat": 2, "option": "Check"}, {"seat": 2, "option": "Put"}],
      "not_offered": [{"seat": 2, "option": "See"}, {"seat": 2, "option": "Fold"}]
    }
  },
  {
    "name": "Leader checked, responder put: leader is offered See or Fold and folds, putter scores 1",
    "rule": "R9",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "Fold"}
    ],
    "expect": {
      "game": {"leader_call": "Check", "responder_action": "Put", "leader_reply": "Fold", "putter": 2, "folded": true},
      "players": {"1": {"score": 0, "tricks": 0}, "2": {"score": 1, "tricks": 0}},
      "offered": [{"seat": 1, "option": "See"}, {"seat": 1, "option": "Fold"}]
    }
  },
  {
    "name": "Responder facing the leader's Put is not offered Put",
    "rule": "R10",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "game": {"putter": 1},
      "offered": [{"seat": 2, "option": "See"}],
      "not_offered": [{"seat": 2, "option": "Put"}, {"seat": 2, "option": "Check"}]
    }
  },
  {
    "name": "A fold gives the putter 1 point, the folder 0, and no cards are played",
    "rule": "R11",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "given": {"players": {"1": {"score": 4}, "2": {"score": 2}}},
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "players": {"1": {"score": 5, "tricks": 0}, "2": {"score": 2, "tricks": 0}},
      "game": {"folded": true, "putter": 1},
      "not_offered": [{"seat": 1, "option": "1-2-3"}, {"seat": 2, "option": "1-2-3"}]
    }
  },
  {
    "name": "With no fold both seats are offered the six card orders",
    "rule": "R12",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Check"},
      {"seat": 1, "options_include": "3-2-1"},
      {"seat": 2, "options_include": "2-3-1"}
    ],
    "expect": {
      "game": {"folded": false},
      "offered": [
        {"seat": 1, "option": "1-2-3"}, {"seat": 1, "option": "1-3-2"}, {"seat": 1, "option": "2-1-3"},
        {"seat": 1, "option": "2-3-1"}, {"seat": 1, "option": "3-1-2"}, {"seat": 1, "option": "3-2-1"},
        {"seat": 2, "option": "1-2-3"}, {"seat": 2, "option": "1-3-2"}, {"seat": 2, "option": "2-1-3"},
        {"seat": 2, "option": "2-3-1"}, {"seat": 2, "option": "3-1-2"}, {"seat": 2, "option": "3-2-1"}
      ]
    }
  },
  {
    "name": "Card ranks decide tricks (dealt cards are chance: only that cards are played is asserted)",
    "rule": "R1",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Check"}
    ],
    "expect": {
      "game": {"folded": false, "putter": 0},
      "offered": [{"seat": 1, "option": "1-2-3"}, {"seat": 2, "option": "1-2-3"}]
    }
  },
  {
    "name": "Three tricks are played when nobody folds (trick winners are chance, not asserted)",
    "rule": "R13",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "See"}
    ],
    "expect": {
      "game": {"folded": false, "putter": 1, "leader_call": "Put", "responder_action": "See"},
      "offered": [{"seat": 1, "option": "3-2-1"}, {"seat": 2, "option": "3-2-1"}]
    }
  },
  {
    "name": "Both check: an unput hand with no fold (point winner is chance, not asserted)",
    "rule": "R14",
    "players": 2,
    "seed": 16,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Check"}
    ],
    "expect": {
      "game": {"leader_call": "Check", "responder_action": "Check", "putter": 0, "folded": false, "leader_reply": ""}
    }
  },
  {
    "name": "Leader's Put is seen and the hand is played out (who gets the 3 points is chance, not asserted)",
    "rule": "R15",
    "players": 2,
    "seed": 17,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "See"}
    ],
    "expect": {
      "game": {"putter": 1, "folded": false, "responder_action": "See"}
    }
  },
  {
    "name": "Responder's Put is seen by the leader and the hand is played out (scoring is chance, not asserted)",
    "rule": "R16",
    "players": 2,
    "seed": 18,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Check"},
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "See"}
    ],
    "expect": {
      "game": {"putter": 2, "folded": false, "leader_reply": "See"}
    }
  },
  {
    "name": "End of hand reveal: public results stay visible after a fold",
    "rule": "R17",
    "players": 2,
    "seed": 19,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put"},
      {"seat": 2, "options_include": "Fold"}
    ],
    "expect": {
      "players": {"1": {"score": 1, "tricks": 0}, "2": {"score": 0, "tricks": 0}},
      "game": {"hand_number": 1, "leader_call": "Put", "responder_action": "Fold", "folded": true}
    }
  },
  {
    "name": "After hand 12 the higher score wins",
    "rule": "R18",
    "players": 2,
    "seed": 20,
    "default": "decline",
    "given": {"game": {"hand_number": 11}, "players": {"1": {"score": 5}, "2": {"score": 3}}},
    "rules": [
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "Fold"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 5, "2": 4},
      "players": {"1": {"score": 5}, "2": {"score": 4}},
      "game": {"hand_number": 12, "leader": 2}
    }
  },
  {
    "name": "After hand 12 equal totals are a shared win",
    "rule": "R18",
    "players": 2,
    "seed": 21,
    "default": "decline",
    "given": {"game": {"hand_number": 11}, "players": {"1": {"score": 4}, "2": {"score": 3}}},
    "rules": [
      {"seat": 2, "options_include": "Put"},
      {"seat": 1, "options_include": "Fold"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 4, "2": 4},
      "players": {"1": {"score": 4}, "2": {"score": 4}}
    }
  },
  {
    "name": "Full match: seat 1 always puts and seat 2 always checks then folds, so seat 1 wins 12-0",
    "rule": "R18",
    "players": 2,
    "seed": 22,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Put", "times": "all"},
      {"seat": 2, "options_include": "Check", "times": "all"},
      {"seat": 2, "options_include": "Fold", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 12, "2": 0},
      "players": {"1": {"score": 12}, "2": {"score": 0}},
      "game": {"hand_number": 12}
    }
  }
]
```
````
