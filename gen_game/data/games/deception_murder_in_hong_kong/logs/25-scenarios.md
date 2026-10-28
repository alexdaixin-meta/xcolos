# 25 scenarios

- time: 2026-10-28T02:13:41+00:00 (127.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 9c78a8f2346e7c77, reply sha256 ff0a5068237058e4

## Sent

````
SPEC:
{
  "name": "Deception: Four Tiles",
  "summary": "A hidden-role deduction game: a silent Forensic Scientist marks scene items to steer the Investigators toward the Murderer's secret clue and means within 4 rounds, and if the case is solved the Murderer gets one guess at the Witness to steal the win.",
  "players": {
    "min": 6,
    "max": 8,
    "suggested": 7
  },
  "parameters": {
    "clue_words": 16,
    "means_words": 16,
    "scene_tiles": 8,
    "items_per_tile": 6,
    "rounds": 4,
    "clues_per_seat": 2,
    "means_per_seat": 2,
    "scientist_seat": 1,
    "murderers": 1,
    "accomplices": 1,
    "witnesses": 1,
    "investigators_formula_offset": 4,
    "starting_badge_cardholder": 1,
    "starting_badge_scientist": 0,
    "accusations_per_seat": 1,
    "win_value": 1
  },
  "attributes": {
    "player": [
      {
        "key": "role",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "scientist, murderer, accomplice, witness or investigator. The Scientist's role is also announced publicly through the table attribute scientist_seat.",
        "observable": false
      },
      {
        "key": "side",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "murderer (Murderer and Accomplice) or investigator (Scientist, Witness and Investigators)",
        "observable": false
      },
      {
        "key": "clues",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the seat's 2 face-up Clue cards (empty for the Scientist)",
        "observable": true
      },
      {
        "key": "means",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the seat's 2 face-up Means cards (empty for the Scientist)",
        "observable": true
      },
      {
        "key": "badge",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if the seat may still accuse, 0 if not",
        "observable": true
      },
      {
        "key": "acc_clue",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the Clue named in this round's accusation (empty means PASS)",
        "observable": false
      },
      {
        "key": "acc_means",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the Means named in this round's accusation",
        "observable": false
      },
      {
        "key": "intel",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "the private information given at setup",
        "observable": false
      },
      {
        "key": "won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if this player is on the winning side",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "scientist_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the public seat of the Forensic Scientist",
        "observable": true
      },
      {
        "key": "solved",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once an accusation exactly matched key_evidence and means_of_murder; never reset",
        "observable": true
      },
      {
        "key": "solved_this_round",
        "type": "bool",
        "visible": "none",
        "initial": false,
        "meaning": "true if solved became true in the current round",
        "observable": false
      },
      {
        "key": "hunt_target",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat the Murderer named in the Witness Hunt (0 means no hunt)",
        "observable": true
      },
      {
        "key": "key_evidence",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "the Murderer's secret Clue",
        "observable": false
      },
      {
        "key": "means_of_murder",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "the Murderer's secret Means",
        "observable": false
      },
      {
        "key": "murderer_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "the seat of the Murderer",
        "observable": false
      },
      {
        "key": "accomplice_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "the seat of the Accomplice",
        "observable": false
      },
      {
        "key": "witness_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "the seat of the Witness",
        "observable": false
      },
      {
        "key": "role_deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the roles still to be dealt to seats 2..N",
        "observable": false
      },
      {
        "key": "clue_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Glove",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Mask",
          "Train Ticket",
          "Lipstick",
          "Receipt",
          "Hair",
          "Button",
          "Watch",
          "Letter",
          "Coin"
        ],
        "meaning": "undealt Clue words",
        "observable": false
      },
      {
        "key": "means_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Rope",
          "Poison",
          "Knife",
          "Pillow",
          "Insulin",
          "Pistol",
          "Electric Wire",
          "Scarf",
          "Bottle",
          "Axe",
          "Hammer",
          "Candlestick",
          "Brick",
          "Razor",
          "Bag",
          "Ice"
        ],
        "meaning": "undealt Means words",
        "observable": false
      },
      {
        "key": "tile_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Location",
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ],
        "meaning": "scene tiles not yet revealed (Cause of Death is revealed in round 1)",
        "observable": false
      },
      {
        "key": "current_tile",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the tile revealed this round",
        "observable": true
      },
      {
        "key": "revealed_tiles",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the tiles revealed so far",
        "observable": true
      },
      {
        "key": "marked_items",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the items marked by the Scientist, one per revealed tile",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the current round number (1 to 4)",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat 1 is given role scientist and side investigator, and badge 0, no Clue cards and no Means cards. It is announced to all that seat 1 is the Forensic Scientist.",
    "role_deck is set to 1 murderer, 1 accomplice, 1 witness and N-4 investigator. Any role already given to a seat is kept and removed from role_deck. Each of seats 2..N without a role draws one role at random from role_deck.",
    "Each seat's side is set: murderer for the Murderer and the Accomplice, investigator for everyone else. murderer_seat, accomplice_seat and witness_seat are recorded.",
    "Cards already given to seats are removed from clue_deck and means_deck. Each of seats 2..N then draws at random from clue_deck until it holds 2 Clues, and from means_deck until it holds 2 Means, all face up (public). Undealt words stay in the decks and are not on the table.",
    "Seats 2..N get badge 1.",
    "Unless already given, the Murderer is asked privately to choose one of their own 2 clues, which is stored as key_evidence, then one of their own 2 means, which is stored as means_of_murder.",
    "Private intel is written to each seat's intel. The Scientist learns every seat's role, key_evidence and means_of_murder. The Accomplice learns murderer_seat. The Witness learns murderer_seat and accomplice_seat as an unordered pair. The Murderer learns accomplice_seat. Investigators learn nothing.",
    "Each player is sent their own state (sync)."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; solved_this_round = false. If round == 1, current_tile = 'Cause of Death'. Otherwise one tile is drawn at random from tile_deck, removed from it, and stored as current_tile. current_tile is appended to revealed_tiles and announced with its 6 items."
    },
    {
      "action": "ask",
      "who": "seat 1 (Scientist)",
      "answer": "one of the 6 items on current_tile",
      "effect": "the chosen item is appended to marked_items and announced to all as the marker on current_tile"
    },
    {
      "action": "poll",
      "who": "seats 2..N",
      "answer": "short text",
      "effect": "all messages are revealed together, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}; no state change"
    },
    {
      "action": "poll",
      "who": "all seats with badge == 1",
      "answer": "PASS or one Clue word currently in the clues of seats 2..N",
      "effect": "a Clue answer is stored in acc_clue; PASS leaves acc_clue empty"
    },
    {
      "action": "poll",
      "who": "all seats whose acc_clue is non-empty",
      "answer": "one Means word currently in the means of seats 2..N",
      "effect": "stored in acc_means"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each seat with acc_clue != '': badge = 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "each accusation (acc_clue, acc_means) with its seat is announced. If acc_clue == key_evidence and acc_means == means_of_murder, it is announced correct, and if solved was false, then solved = true and solved_this_round = true. Otherwise it is announced wrong. solved never returns to false."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "acc_clue = '' and acc_means = '' for every player"
    },
    {
      "action": "ask",
      "who": "the Murderer (seat murderer_seat), only when solved_this_round == true",
      "answer": "one seat from 2..N other than murderer_seat",
      "effect": "hunt_target = the chosen seat; it is announced"
    },
    {
      "action": "update",
      "who": "all players, only when solved == true or round >= 4",
      "answer": null,
      "effect": "if solved == true and hunt_target == witness_seat: won = 1 for every player with side == murderer. If solved == true and hunt_target != witness_seat: won = 1 for every player with side == investigator. If solved == false: won = 1 for every player with side == murderer. All roles are revealed."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "the game ends if solved == true or round >= 4; otherwise the next round begins"
    }
  ],
  "ending": {
    "condition": "solved == true or round >= 4",
    "rank_by": "you.won",
    "min_to_win": 1,
    "decided_by": "A team win. Every player whose side won has won = 1 and shares the win. The Investigator side wins if the case is solved and hunt_target is not the Witness's seat. The Murderer side wins if the case is unsolved after 4 rounds, or if it is solved and hunt_target is the Witness's seat."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game sets up, then seat 1 is the Forensic Scientist, publicly, with badge 0 and empty clues and means."
    },
    {
      "id": "R2",
      "text": "When the game sets up with N players, then seats 2..N hold exactly 1 murderer, 1 accomplice, 1 witness and N-4 investigators, and any pre-given role is kept."
    },
    {
      "id": "R3",
      "text": "When roles are dealt, then the Murderer and the Accomplice have side murderer, and the Scientist, the Witness and the Investigators have side investigator."
    },
    {
      "id": "R4",
      "text": "When the game sets up, then each of seats 2..N holds exactly 2 public clues and 2 public means, and pre-given cards are kept and removed from the decks first."
    },
    {
      "id": "R5",
      "text": "When cards are dealt, then no word appears twice across hands and decks, and undealt words remain in clue_deck or means_deck."
    },
    {
      "id": "R6",
      "text": "When setup finishes, then seats 2..N have badge 1."
    },
    {
      "id": "R7",
      "text": "When the Murderer chooses, then key_evidence is one of the Murderer's own 2 clues and means_of_murder is one of the Murderer's own 2 means."
    },
    {
      "id": "R8",
      "text": "When intel is written, then the Scientist learns all roles, key_evidence and means_of_murder, the Accomplice learns murderer_seat, the Witness learns the two murderer-side seats unordered, the Murderer learns accomplice_seat, and Investigators learn nothing."
    },
    {
      "id": "R9",
      "text": "When round 1 starts, then current_tile is Cause of Death."
    },
    {
      "id": "R10",
      "text": "When rounds 2, 3 or 4 start, then one tile not yet revealed is drawn at random from tile_deck and removed from it."
    },
    {
      "id": "R11",
      "text": "When a tile is revealed, then the Scientist chooses exactly one of its 6 items, and that item is announced and appended to marked_items."
    },
    {
      "id": "R12",
      "text": "When the Talk step runs, then only seats 2..N write a message, simultaneously, and all messages are shown to everyone afterward; the Scientist never speaks."
    },
    {
      "id": "R13",
      "text": "When Poll A runs, then only seats with badge 1 are asked, and each may choose PASS or a Clue currently in the clues of seats 2..N."
    },
    {
      "id": "R14",
      "text": "When a seat names a Clue in Poll A, then in Poll B it must choose a Means currently in the means of seats 2..N; a seat that passed is not asked in Poll B."
    },
    {
      "id": "R15",
      "text": "When a seat has made an accusation (acc_clue non-empty), then its badge becomes 0 and it is never asked to accuse again."
    },
    {
      "id": "R16",
      "text": "When an accusation has acc_clue == key_evidence and acc_means == means_of_murder, then it is announced correct and solved becomes true."
    },
    {
      "id": "R17",
      "text": "When an accusation matches only one of the two words or neither, then it is announced wrong and solved is unchanged."
    },
    {
      "id": "R18",
      "text": "When solved is true, then it stays true for the rest of the game."
    },
    {
      "id": "R19",
      "text": "When resolution finishes, then acc_clue and acc_means are cleared for all players."
    },
    {
      "id": "R20",
      "text": "When solved became true this round, then the Murderer chooses hunt_target from seats 2..N other than their own seat; otherwise no hunt happens and hunt_target stays 0."
    },
    {
      "id": "R21",
      "text": "When solved is true or round 4 has finished, then the game ends."
    },
    {
      "id": "R22",
      "text": "When the game ends with solved true and hunt_target == witness_seat, then the Murderer and the Accomplice get won = 1 and all others keep won = 0."
    },
    {
      "id": "R23",
      "text": "When the game ends with solved true and hunt_target != witness_seat, then the Scientist, the Witness and every Investigator get won = 1."
    },
    {
      "id": "R24",
      "text": "When round 4 ends with solved false, then the Murderer and the Accomplice get won = 1."
    }
  ],
  "offers": [
    {
      "question": "Setup: the Murderer's choice of key_evidence",
      "who": "the Murderer",
      "options": "the 2 Clue words in the Murderer's own clues"
    },
    {
      "question": "Setup: the Murderer's choice of means_of_murder",
      "who": "the Murderer",
      "options": "the 2 Means words in the Murderer's own means"
    },
    {
      "question": "Marker",
      "who": "seat 1 (Scientist)",
      "options": "the 6 items of current_tile, e.g. for Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident"
    },
    {
      "question": "Talk",
      "who": "seats 2..N",
      "options": "one short free-text message; the Scientist is not asked"
    },
    {
      "question": "Accusation Poll A",
      "who": "every seat with badge 1 (never seat 1, never a seat that already accused)",
      "options": "PASS, or any Clue word currently in the clues of seats 2..N, including the asker's own"
    },
    {
      "question": "Accusation Poll B",
      "who": "every seat that named a Clue in Poll A this round",
      "options": "any Means word currently in the means of seats 2..N, including the asker's own; PASS is not offered"
    },
    {
      "question": "Witness Hunt",
      "who": "the Murderer, only in the round solved became true",
      "options": "every seat from 2..N except the Murderer's own seat"
    }
  ],
  "choices": [
    {
      "what": "6 to 8 players, suggested 7",
      "why": "The designer chose 7, and it is kept. The minimum is 6 because seats 2..N must hold the Murderer, the Accomplice, the Witness and at least 2 Investigators, so that the Murderer side can hide and the Witness Hunt is a real guess. The maximum is 8 because more card-holders dilute each accusation and lengthen the talk beyond what can be followed."
    },
    {
      "what": "Talk is a simultaneous poll of one short message from seats 2..N, broadcast to all",
      "why": "The source says messages are written at the same time without seeing the others. Talk earns its place because the two sides disagree: the Murderer side misleads, Investigators argue readings of the markers, and the Witness must hint without exposing themselves."
    },
    {
      "what": "Role, side and intel are owner-only (ally), and seat knowledge is delivered through the intel text",
      "why": "Each player sees only their own role. Cross-seat knowledge (Accomplice to Murderer, Witness to the pair, Scientist to all) is given exactly as the rules list it."
    },
    {
      "what": "Scoring is applied as a single conditional update just before the end check, and the winner is ranked by you.won with min_to_win 1",
      "why": "This makes the team win pure arithmetic on stored values, as the source states."
    },
    {
      "what": "All roles are revealed when the game ends",
      "why": "Revealing roles lets observers verify the result. It does not change play."
    }
  ],
  "simplifications": [
    {
      "what": "The Scientist's marker is a single choice from the 6 tile items, announced as text",
      "why": "There are no physical tiles or bullet markers; the source already defines the marker as a choice of one item."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: clues, means, badge, won; table: scientist_seat, solved, hunt_target, current_tile, revealed_tiles, marked_items, round.
````

## Reply

````
```json
[
  {
    "name": "Seat 1 is the public Forensic Scientist with no badge and no cards",
    "rule": "R1",
    "players": 6,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"scientist_seat": 1},
      "players": {"1": {"badge": 0}},
      "lens": {"players": {"1": {"clues": 0, "means": 0}}}
    }
  },
  {
    "name": "A pre-given Murderer role is kept: seat 2 wins when the case stays unsolved",
    "rule": "R2",
    "players": 6,
    "seed": 2,
    "rounds": 4,
    "default": "decline",
    "given": {
      "players": {"2": {"role": "murderer", "side": "murderer"}},
      "game": {"murderer_seat": 2}
    },
    "rules": [],
    "expect": {
      "game": {"solved": false, "round": 4},
      "players": {"1": {"won": 0}, "2": {"won": 1}}
    }
  },
  {
    "name": "Sides follow roles: Murderer and Accomplice share the unsolved win",
    "rule": "R3",
    "players": 6,
    "seed": 3,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer"},
        "3": {"role": "accomplice"},
        "4": {"role": "witness"},
        "5": {"role": "investigator"},
        "6": {"role": "investigator"}
      }
    },
    "rules": [],
    "expect": {
      "winner": [2, 3],
      "players": {
        "1": {"won": 0},
        "2": {"won": 1},
        "3": {"won": 1},
        "4": {"won": 0},
        "5": {"won": 0},
        "6": {"won": 0}
      }
    }
  },
  {
    "name": "Each card-holder has 2 clues and 2 means, and pre-given cards are kept",
    "rule": "R4",
    "players": 6,
    "seed": 4,
    "rounds": 0,
    "default": "decline",
    "given": {
      "players": {"2": {"clues": ["Glove", "Key"], "means": ["Rope", "Poison"]}}
    },
    "rules": [],
    "expect": {
      "players": {"2": {"clues": ["Glove", "Key"], "means": ["Rope", "Poison"]}},
      "lens": {
        "players": {
          "2": {"clues": 2, "means": 2},
          "3": {"clues": 2, "means": 2},
          "4": {"clues": 2, "means": 2},
          "5": {"clues": 2, "means": 2},
          "6": {"clues": 2, "means": 2}
        }
      }
    }
  },
  {
    "name": "With 7 players, 12 clues and 12 means are dealt and 4 of each stay in the decks",
    "rule": "R5",
    "players": 7,
    "seed": 5,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "lens": {
        "game": {"clue_deck": 4, "means_deck": 4},
        "players": {
          "2": {"clues": 2, "means": 2},
          "7": {"clues": 2, "means": 2}
        }
      }
    }
  },
  {
    "name": "After setup, seats 2..8 have badge 1 and seat 1 has badge 0",
    "rule": "R6",
    "players": 8,
    "seed": 6,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "players": {
        "1": {"badge": 0},
        "2": {"badge": 1},
        "3": {"badge": 1},
        "4": {"badge": 1},
        "5": {"badge": 1},
        "6": {"badge": 1},
        "7": {"badge": 1},
        "8": {"badge": 1}
      }
    }
  },
  {
    "name": "The Murderer picks Key and Poison from their own cards, and accusing exactly that solves the case",
    "rule": "R7",
    "players": 6,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 2, "options_include": "Key"},
      {"seat": 2, "options_include": "Poison"},
      {"seat": 5, "options_include": "Key"},
      {"seat": 5, "options_include": "Poison"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 5},
      "players": {"5": {"won": 1}, "2": {"won": 0}},
      "offered": [{"seat": 2, "option": "Glove"}, {"seat": 2, "option": "Rope"}]
    }
  },
  {
    "name": "Intel is private: only the public Scientist seat is observable after setup",
    "rule": "R8",
    "players": 6,
    "seed": 8,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"scientist_seat": 1, "round": 0, "solved": false, "hunt_target": 0}
    }
  },
  {
    "name": "Round 1 reveals Cause of Death",
    "rule": "R9",
    "players": 6,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"round": 1, "current_tile": "Cause of Death", "revealed_tiles": ["Cause of Death"]},
      "lens": {"game": {"revealed_tiles": 1, "marked_items": 1}}
    }
  },
  {
    "name": "Round 2 draws one tile from the deck (which tile is chance; only counts asserted)",
    "rule": "R10",
    "players": 6,
    "seed": 10,
    "rounds": 2,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"round": 2},
      "lens": {"game": {"revealed_tiles": 2, "tile_deck": 6, "marked_items": 2}}
    }
  },
  {
    "name": "The Scientist marks Poisoning on Cause of Death",
    "rule": "R11",
    "players": 6,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "Poisoning"}],
    "expect": {
      "game": {"marked_items": ["Poisoning"], "current_tile": "Cause of Death"},
      "offered": [{"seat": 1, "option": "Accident"}, {"seat": 1, "option": "Suffocation"}]
    }
  },
  {
    "name": "Talk changes no state and the Scientist is not polled",
    "rule": "R12",
    "players": 6,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"round": 1, "solved": false, "hunt_target": 0},
      "players": {"1": {"badge": 0}, "2": {"badge": 1}, "5": {"badge": 1}},
      "not_offered": [{"seat": 1, "option": "PASS"}]
    }
  },
  {
    "name": "Poll A offers PASS and any card-holder clue, never deck clues, and never asks the Scientist",
    "rule": "R13",
    "players": 6,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [],
    "expect": {
      "offered": [
        {"seat": 3, "option": "PASS"},
        {"seat": 3, "option": "Diary"},
        {"seat": 3, "option": "Lipstick"}
      ],
      "not_offered": [
        {"seat": 3, "option": "Coin"},
        {"seat": 1, "option": "PASS"}
      ],
      "game": {"solved": false}
    }
  },
  {
    "name": "A seat naming a clue must name a card-holder means; a seat that passed is not asked for a means",
    "rule": "R14",
    "players": 6,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Wallet"},
      {"seat": 5, "options_include": "Axe"}
    ],
    "expect": {
      "offered": [{"seat": 5, "option": "Rope"}],
      "not_offered": [
        {"seat": 5, "option": "Ice"},
        {"seat": 6, "option": "Rope"}
      ],
      "game": {"solved": false},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "An accuser's badge drops to 0 and stays 0 the next round",
    "rule": "R15",
    "players": 6,
    "seed": 15,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Wallet"},
      {"seat": 5, "options_include": "Axe"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false},
      "players": {
        "5": {"badge": 0},
        "2": {"badge": 1},
        "3": {"badge": 1},
        "4": {"badge": 1},
        "6": {"badge": 1}
      }
    }
  },
  {
    "name": "Accusing Glove and Rope (the key evidence and the means) solves the case",
    "rule": "R16",
    "players": 6,
    "seed": 16,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"}
    ],
    "expect": {
      "game": {"solved": true},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Accusations matching only one word are wrong and leave solved false",
    "rule": "R17",
    "players": 6,
    "seed": 17,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Knife"},
      {"seat": 6, "options_include": "Key"},
      {"seat": 6, "options_include": "Rope"}
    ],
    "expect": {
      "game": {"solved": false, "hunt_target": 0},
      "players": {"5": {"badge": 0}, "6": {"badge": 0}}
    }
  },
  {
    "name": "A wrong accusation in the same round does not undo a correct one",
    "rule": "R18",
    "players": 6,
    "seed": 18,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 6, "options_include": "Mask"},
      {"seat": 6, "options_include": "Axe"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 6}
    }
  },
  {
    "name": "After a wrong accusation is cleared, the next round plays on unsolved",
    "rule": "R19",
    "players": 6,
    "seed": 19,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 6, "options_include": "Lipstick"},
      {"seat": 6, "options_include": "Bottle"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false, "hunt_target": 0},
      "players": {"6": {"badge": 0}}
    }
  },
  {
    "name": "Without a solve there is no Witness Hunt and hunt_target stays 0",
    "rule": "R20",
    "players": 6,
    "seed": 20,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [],
    "expect": {
      "game": {"hunt_target": 0, "solved": false},
      "not_offered": [{"seat": 2, "option": 3}, {"seat": 2, "option": 4}]
    }
  },
  {
    "name": "The Witness Hunt offers seats 2..N except the Murderer's own seat and never seat 1",
    "rule": "R20",
    "players": 6,
    "seed": 21,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 3}
    ],
    "expect": {
      "game": {"hunt_target": 3, "solved": true},
      "offered": [{"seat": 2, "option": 4}, {"seat": 2, "option": 6}],
      "not_offered": [{"seat": 2, "option": 2}, {"seat": 2, "option": 1}]
    }
  },
  {
    "name": "A solve in round 1 ends the game in round 1",
    "rule": "R21",
    "players": 6,
    "seed": 22,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "winner": [1, 4, 5, 6],
      "game": {"round": 1, "solved": true, "hunt_target": 5}
    }
  },
  {
    "name": "Solved, but the Murderer finds the Witness: the Murderer side wins",
    "rule": "R22",
    "players": 6,
    "seed": 23,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 4}
    ],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "game": {"hunt_target": 4, "solved": true},
      "players": {
        "1": {"won": 0},
        "2": {"won": 1},
        "3": {"won": 1},
        "4": {"won": 0},
        "5": {"won": 0},
        "6": {"won": 0}
      }
    }
  },
  {
    "name": "Solved and the Murderer misses the Witness: the Investigator side wins",
    "rule": "R23",
    "players": 6,
    "seed": 24,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4}
    },
    "rules": [
      {"seat": 4, "options_include": "Glove"},
      {"seat": 4, "options_include": "Rope"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "winner": [1, 4, 5, 6],
      "standings": {"1": 1, "2": 0, "3": 0, "4": 1, "5": 1, "6": 1},
      "game": {"hunt_target": 6, "solved": true},
      "players": {
        "1": {"won": 1},
        "2": {"won": 0},
        "3": {"won": 0},
        "4": {"won": 1},
        "5": {"won": 1},
        "6": {"won": 1}
      }
    }
  },
  {
    "name": "Round 4 ends unsolved: the Murderer and the Accomplice win",
    "rule": "R24",
    "players": 6,
    "seed": 25,
    "default": "decline",
    "given": {
      "players": {
        "2": {"role": "murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Insulin", "Pistol"]},
        "5": {"role": "investigator", "side": "investigator", "clues": ["Wallet", "Mask"], "means": ["Electric Wire", "Scarf"]},
        "6": {"role": "investigator", "side": "investigator", "clues": ["Train Ticket", "Lipstick"], "means": ["Bottle", "Axe"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "murderer_seat": 2, "accomplice_seat": 3, "witness_seat": 4, "round": 3}
    },
    "rules": [],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "game": {"round": 4, "solved": false, "hunt_target": 0},
      "players": {
        "1": {"won": 0},
        "2": {"won": 1},
        "3": {"won": 1},
        "4": {"won": 0},
        "5": {"won": 0},
        "6": {"won": 0}
      }
    }
  }
]
```
````
