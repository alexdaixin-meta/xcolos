# 06 scenarios

- time: 2026-10-28T01:37:15+00:00 (69.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 2d26f8b65fd9dc5c, reply sha256 48fc417060e7b7ae

## Sent

````
SPEC:
{
  "name": "Deception: Five Clues",
  "summary": "A hidden-role deduction game. A public Forensic Scientist marks scene-tile options to steer Investigators towards the Murderer's secret Clue and Means. The Murderer side wins by evading for 5 rounds, or by finding the Witness after the case is solved.",
  "players": {
    "min": 6,
    "max": 8,
    "suggested": 7
  },
  "parameters": {
    "rounds": 5,
    "scientist_seat": 1,
    "clue_list_size": 16,
    "means_list_size": 16,
    "clues_per_player": 2,
    "means_per_player": 2,
    "starting_badges": 1,
    "options_per_tile": 6,
    "deck_tiles": 6,
    "deck_draws": 3,
    "murderers": 1,
    "accomplices": 1,
    "witnesses": 1,
    "investigators_formula_offset": 4,
    "win_value": 1
  },
  "attributes": {
    "player": [
      {
        "key": "role",
        "type": "text",
        "visible": "ally",
        "initial": "dealt: Scientist for seat 1; for the other seats a random one of Murderer, Accomplice, Witness, or Investigator (player count minus 4 Investigators)",
        "meaning": "secret role; the Scientist's role is publicly known",
        "observable": false
      },
      {
        "key": "side",
        "type": "text",
        "visible": "ally",
        "initial": "murderer for Murderer and Accomplice, investigator otherwise",
        "meaning": "team",
        "observable": false
      },
      {
        "key": "intel",
        "type": "text",
        "visible": "ally",
        "initial": "Accomplice: the Murderer's seat; Witness: the two seats of the Murderer and Accomplice in random order; Scientist: every seat's role; others: empty",
        "meaning": "private role knowledge given at setup",
        "observable": false
      },
      {
        "key": "solution_known",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Key Evidence and Means of Murder, filled in for the Scientist and the Accomplice",
        "observable": false
      },
      {
        "key": "clues",
        "type": "list",
        "visible": "public",
        "initial": "2 Clue words drawn from clue_deck (empty for seat 1)",
        "meaning": "face-up Clue cards",
        "observable": true
      },
      {
        "key": "means",
        "type": "list",
        "visible": "public",
        "initial": "2 Means words drawn from means_deck (empty for seat 1)",
        "meaning": "face-up Means cards",
        "observable": true
      },
      {
        "key": "badge",
        "type": "number",
        "visible": "public",
        "initial": "1 (0 for seat 1)",
        "meaning": "accusations remaining",
        "observable": true
      },
      {
        "key": "acc_clue",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's accused Clue, or PASS; revealed at resolution",
        "observable": false
      },
      {
        "key": "acc_means",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's accused Means; revealed at resolution",
        "observable": false
      },
      {
        "key": "won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if this player's side won",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "clue_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Glove",
          "Train Ticket",
          "Lipstick",
          "Key",
          "Diary",
          "Ring",
          "Cigarette",
          "Phone",
          "Wallet",
          "Photo",
          "Watch",
          "Umbrella",
          "Receipt",
          "Hair",
          "Button",
          "Mask"
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
          "Hammer",
          "Pistol",
          "Insulin",
          "Brick",
          "Drowning",
          "Electric Wire",
          "Scarf",
          "Bare Hands",
          "Fire",
          "Bottle",
          "Axe",
          "Car"
        ],
        "meaning": "undealt Means words",
        "observable": false
      },
      {
        "key": "tile_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Time of Death",
          "Weather",
          "Victim's Build",
          "Trace at Scene",
          "Corpse Condition",
          "Duration of Crime"
        ],
        "meaning": "undrawn scene tiles",
        "observable": false
      },
      {
        "key": "current_tile",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's scene tile",
        "observable": true
      },
      {
        "key": "marker",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "option the Scientist marked this round",
        "observable": true
      },
      {
        "key": "key_evidence",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "the Murderer's chosen Clue",
        "observable": false
      },
      {
        "key": "means_of_murder",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "the Murderer's chosen Means",
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
        "key": "solved",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "a correct accusation has been made",
        "observable": true
      },
      {
        "key": "hunt_target",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat named by the Murderer in the Witness Hunt",
        "observable": true
      },
      {
        "key": "game_over",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 when the game has ended",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is publicly the Forensic Scientist.",
    "The engine secretly and randomly deals the other seats 1 Murderer, 1 Accomplice, 1 Witness and (player count minus 4) Investigators into role, and sets side.",
    "Intel is set: the Accomplice learns the Murderer's seat; the Witness learns the two seats of the Murderer and Accomplice without learning which is which; the Scientist learns every role.",
    "Each seat except seat 1 draws 2 Clue words from clue_deck into clues and 2 Means words from means_deck into means, at random and without repeats. These cards are public.",
    "Each seat except seat 1 gets badge 1.",
    "The Murderer is asked privately to choose one of their own clues as key_evidence and one of their own means as means_of_murder.",
    "solution_known of seat 1 and of the Accomplice is set to the key_evidence and the means_of_murder.",
    "Every player is sent their own state (sync)."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; current_tile = 'Cause of Death' if round==1, 'Location' if round==2, otherwise a random tile removed from tile_deck; every acc_clue and acc_means is cleared; current_tile is announced with its 6 options"
    },
    {
      "action": "ask",
      "who": "seat 1",
      "answer": "one of the 6 options of current_tile",
      "effect": "marker = the chosen option; the marker is announced to all"
    },
    {
      "action": "poll",
      "who": "every player except seat 1",
      "answer": "short text",
      "effect": "broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"
    },
    {
      "action": "poll",
      "who": "every player with badge == 1",
      "answer": "PASS, or one Clue word currently in any player's clues",
      "effect": "acc_clue = the answer; hidden until resolution"
    },
    {
      "action": "poll",
      "who": "every player whose acc_clue is not PASS",
      "answer": "one Means word currently in any player's means",
      "effect": "acc_means = the answer; badge -= 1 for each such player; hidden until resolution"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "each accusation is announced with its accuser and marked correct if acc_clue == key_evidence and acc_means == means_of_murder, wrong otherwise; solved = true if any accusation is correct"
    },
    {
      "action": "ask",
      "who": "the player whose role is Murderer, when solved == true",
      "answer": "a seat other than seat 1, the Accomplice and the Murderer",
      "effect": "hunt_target = the chosen seat"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "when solved == true: if the role of hunt_target is Witness, won = 1 for side murderer, else won = 1 for side investigator; game_over = 1. Else when round == 5: won = 1 for side murderer; game_over = 1"
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "end the game if game_over == 1, otherwise continue to the next round"
    }
  ],
  "ending": {
    "condition": "game_over == 1",
    "rank_by": "you.won",
    "min_to_win": 1,
    "decided_by": "Team win: every player on the winning side has won = 1 and shares the win; the losing side has 0."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Seat 1 is always the Forensic Scientist, and that role is public."
    },
    {
      "id": "R2",
      "text": "When the game starts with N players, then the other N-1 seats are dealt exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators at random."
    },
    {
      "id": "R3",
      "text": "When roles are dealt, then the Accomplice's intel names the Murderer's seat."
    },
    {
      "id": "R4",
      "text": "When roles are dealt, then the Witness's intel names the two seats of the Murderer and the Accomplice without saying which is which, and the Witness does not get the solution."
    },
    {
      "id": "R5",
      "text": "When roles are dealt, then the Scientist's intel lists every seat's role."
    },
    {
      "id": "R6",
      "text": "When cards are dealt, then every seat except seat 1 holds 2 Clue words and 2 Means words, all public, with no word appearing twice at the table."
    },
    {
      "id": "R7",
      "text": "When the Murderer chooses the solution, then key_evidence must be one of the Murderer's own 2 clues and means_of_murder must be one of their own 2 means."
    },
    {
      "id": "R8",
      "text": "When the solution is chosen, then the Scientist and the Accomplice are told it, and no one else is."
    },
    {
      "id": "R9",
      "text": "When the game starts, then every seat except seat 1 has badge 1 and seat 1 has badge 0."
    },
    {
      "id": "R10",
      "text": "When round is 1, then current_tile is Cause of Death; when round is 2, then it is Location."
    },
    {
      "id": "R11",
      "text": "When round is 3, 4 or 5, then current_tile is drawn at random from tile_deck and removed from it."
    },
    {
      "id": "R12",
      "text": "When the Scientist marks, then exactly one of current_tile's 6 options becomes marker and is announced to all."
    },
    {
      "id": "R13",
      "text": "The Scientist never writes a talk message or makes an accusation."
    },
    {
      "id": "R14",
      "text": "When talk happens, then every player except seat 1 writes one message at the same time, and all messages are shown to everyone afterwards."
    },
    {
      "id": "R15",
      "text": "When accusations are made, then only players with badge 1 are asked, all at the same time, to choose PASS or one Clue on the table and one Means on the table."
    },
    {
      "id": "R16",
      "text": "When a player accuses, then their badge drops from 1 to 0 and they are not asked to accuse again."
    },
    {
      "id": "R17",
      "text": "When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong."
    },
    {
      "id": "R18",
      "text": "When an accusation pairs a Clue and a Means from two different players' cards, then it is always wrong."
    },
    {
      "id": "R19",
      "text": "When solved is true, then the Murderer names one seat other than seat 1, the Accomplice and themself."
    },
    {
      "id": "R20",
      "text": "When the named seat is the Witness, then the Murderer and the Accomplice get won = 1; otherwise the Scientist, the Witness and all Investigators get won = 1."
    },
    {
      "id": "R21",
      "text": "When round 5 ends with solved still false, then the Murderer and the Accomplice get won = 1 and the game ends."
    },
    {
      "id": "R22",
      "text": "When no accusation is correct in rounds 1 to 4, then the next round begins."
    }
  ],
  "offers": [
    {
      "question": "Murderer's choice of Key Evidence (setup)",
      "who": "the Murderer",
      "options": "the 2 Clue words in the Murderer's own clues"
    },
    {
      "question": "Murderer's choice of Means of Murder (setup)",
      "who": "the Murderer",
      "options": "the 2 Means words in the Murderer's own means"
    },
    {
      "question": "Marker",
      "who": "seat 1",
      "options": "the 6 options of current_tile"
    },
    {
      "question": "Talk",
      "who": "every seat except seat 1",
      "options": "short free text"
    },
    {
      "question": "Accusation: Clue",
      "who": "every seat with badge 1 (never seat 1)",
      "options": "PASS, or any Clue word in any player's clues"
    },
    {
      "question": "Accusation: Means",
      "who": "every seat that chose a Clue",
      "options": "any Means word in any player's means"
    },
    {
      "question": "Witness Hunt",
      "who": "the Murderer, only when solved is true",
      "options": "every seat except seat 1, the Accomplice and the Murderer"
    }
  ],
  "choices": [
    {
      "what": "6 to 8 players, suggested 7",
      "why": "Kept the designer's 7. Six is the minimum because the four special roles plus 2 Investigators are needed for the Murderer side to hide. Above 8 the talk becomes too long and the Scientist's single marker per round is spread too thin."
    },
    {
      "what": "The accusation is split into two simultaneous polls (Clue or PASS, then Means)",
      "why": "Offering every Clue-Means pair would mean up to about 200 options. Answers stay hidden until resolution, so the choice is still effectively simultaneous."
    },
    {
      "what": "Talk is kept as a simultaneous poll broadcast to all",
      "why": "The source requires it. Players disagree because the Murderer side wants to mislead, so reading each other's statements against the marker is the core of the game."
    },
    {
      "what": "The win is recorded as won = 1 for each player on the winning side, with min_to_win 1",
      "why": "This expresses a team win as an arithmetic ranking."
    },
    {
      "what": "The Witness Hunt is a single conditional step inside the round, followed by game_over",
      "why": "A flat step list cannot branch into a separate block, but a step with a 'when' condition works."
    },
    {
      "what": "Strategy at the table",
      "why": "The Scientist picks markers that point towards one player's cards. Investigators cross-reference the markers with the face-up cards and spend their single badge carefully. The Murderer and Accomplice steer talk towards innocent pairs. The Witness must hint without revealing themself."
    }
  ],
  "simplifications": [
    {
      "what": "The Scientist's ban on sending any other message is enforced by never asking seat 1 to talk",
      "why": "The engine only lets players speak when asked."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: clues, means, badge, won; table: current_tile, marker, round, solved, hunt_target.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Seat 1 is the Scientist: no cards and no badge at setup",
    "rule": "R1",
    "players": 6,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {"1": {"badge": 0, "won": 0}},
      "lens": {"players": {"1": {"clues": 0, "means": 0}}}
    }
  },
  {
    "name": "7 players: the 6 non-Scientist seats are each dealt cards, so 12 clue words leave the deck (roles hidden, only counts asserted)",
    "rule": "R2",
    "players": 7,
    "seed": 2,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"clue_deck": 4, "means_deck": 4},
        "players": {"1": {"clues": 0}, "2": {"clues": 2}, "3": {"clues": 2}, "4": {"clues": 2}, "5": {"clues": 2}, "6": {"clues": 2}, "7": {"clues": 2}}
      }
    }
  },
  {
    "name": "8 players: setup deals 7 seats (intel hidden, only observable setup state asserted)",
    "rule": "R3",
    "players": 8,
    "seed": 3,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"clue_deck": 2, "means_deck": 2}},
      "game": {"round": 0, "solved": false}
    }
  },
  {
    "name": "With stated roles, a round of passes leaves the case unsolved and nobody has won",
    "rule": "R4",
    "players": 6,
    "seed": 4,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "expect": {
      "game": {"round": 1, "solved": false},
      "players": {"1": {"won": 0}, "2": {"won": 0}, "4": {"won": 0}}
    }
  },
  {
    "name": "Setup leaves seat 1 without cards and every other seat with a badge (Scientist intel is hidden)",
    "rule": "R5",
    "players": 6,
    "seed": 5,
    "rounds": 0,
    "expect": {
      "players": {"1": {"badge": 0}, "2": {"badge": 1}},
      "lens": {"players": {"1": {"clues": 0, "means": 0}}}
    }
  },
  {
    "name": "6 players: seats 2-6 hold 2 clues and 2 means each, decks hold the rest",
    "rule": "R6",
    "players": 6,
    "seed": 6,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"clue_deck": 6, "means_deck": 6},
        "players": {
          "1": {"clues": 0, "means": 0},
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
    "name": "Murderer's other own clue and means (Key + Poison) is not the solution: wrong",
    "rule": "R7",
    "players": 6,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Key"},
      {"seat": 5, "options_include": "Poison"}
    ],
    "expect": {
      "game": {"solved": false, "round": 1},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Setup leaves the case unsolved and no round played (solution knowledge is hidden)",
    "rule": "R8",
    "players": 6,
    "seed": 8,
    "rounds": 0,
    "expect": {
      "game": {"solved": false, "round": 0, "hunt_target": 0}
    }
  },
  {
    "name": "Starting badges: seat 1 has 0, all others 1",
    "rule": "R9",
    "players": 7,
    "seed": 9,
    "rounds": 0,
    "expect": {
      "players": {"1": {"badge": 0}, "2": {"badge": 1}, "3": {"badge": 1}, "4": {"badge": 1}, "5": {"badge": 1}, "6": {"badge": 1}, "7": {"badge": 1}}
    }
  },
  {
    "name": "Round 1 tile is Cause of Death",
    "rule": "R10",
    "players": 6,
    "seed": 10,
    "rounds": 1,
    "expect": {
      "game": {"round": 1, "current_tile": "Cause of Death"}
    }
  },
  {
    "name": "Round 2 tile is Location",
    "rule": "R10",
    "players": 6,
    "seed": 11,
    "rounds": 2,
    "expect": {
      "game": {"round": 2, "current_tile": "Location"}
    }
  },
  {
    "name": "Round 3 draws a tile from tile_deck and removes it (which tile is random)",
    "rule": "R11",
    "players": 6,
    "seed": 12,
    "rounds": 1,
    "given": {"game": {"round": 2}},
    "expect": {
      "game": {"round": 3},
      "lens": {"game": {"tile_deck": 5}}
    }
  },
  {
    "name": "Scientist marks in round 1 on the Cause of Death tile",
    "rule": "R12",
    "players": 6,
    "seed": 13,
    "rounds": 1,
    "expect": {
      "game": {"round": 1, "current_tile": "Cause of Death"},
      "not_offered": [{"seat": 2, "option": "Cause of Death"}]
    }
  },
  {
    "name": "Scientist is never asked to accuse",
    "rule": "R13",
    "players": 6,
    "seed": 14,
    "rounds": 1,
    "expect": {
      "not_offered": [{"seat": 1, "option": "PASS"}],
      "offered": [{"seat": 2, "option": "PASS"}],
      "players": {"1": {"badge": 0}}
    }
  },
  {
    "name": "A full round of talk and passes keeps every badge",
    "rule": "R14",
    "players": 6,
    "seed": 15,
    "rounds": 1,
    "expect": {
      "game": {"round": 1, "solved": false},
      "players": {"2": {"badge": 1}, "3": {"badge": 1}, "4": {"badge": 1}, "5": {"badge": 1}, "6": {"badge": 1}}
    }
  },
  {
    "name": "Only badge holders are asked to accuse, and only clues on the table are offered",
    "rule": "R15",
    "players": 6,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"], "badge": 0},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "clue_deck": ["Train Ticket", "Lipstick", "Receipt", "Hair", "Button", "Mask"]}
    },
    "expect": {
      "offered": [{"seat": 6, "option": "PASS"}, {"seat": 6, "option": "Glove"}],
      "not_offered": [{"seat": 5, "option": "PASS"}, {"seat": 6, "option": "Mask"}, {"seat": 1, "option": "PASS"}],
      "players": {"5": {"badge": 0}, "6": {"badge": 1}}
    }
  },
  {
    "name": "A wrong accuser's badge drops to 0, and the game goes on",
    "rule": "R16",
    "players": 6,
    "seed": 17,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Wallet"},
      {"seat": 5, "options_include": "Insulin"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false},
      "players": {"5": {"badge": 0}, "6": {"badge": 1}}
    }
  },
  {
    "name": "Correct accusation Glove + Rope solves the case",
    "rule": "R17",
    "players": 6,
    "seed": 18,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 6},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Right clue with the wrong means (Glove + Poison) is wrong",
    "rule": "R17",
    "players": 6,
    "seed": 19,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Poison"}
    ],
    "expect": {
      "game": {"solved": false, "hunt_target": 0},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Clue and means from different players (Glove + Knife) is wrong",
    "rule": "R18",
    "players": 6,
    "seed": 20,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Knife"}
    ],
    "expect": {
      "game": {"solved": false, "round": 1},
      "players": {"5": {"badge": 0}, "2": {"won": 0}, "3": {"won": 0}}
    }
  },
  {
    "name": "Witness Hunt offers only seats other than 1, the Accomplice and the Murderer",
    "rule": "R19",
    "players": 6,
    "seed": 21,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 6, "options_include": "Glove"},
      {"seat": 6, "options_include": "Rope"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 5},
      "offered": [{"seat": 2, "option": 4}, {"seat": 2, "option": 5}, {"seat": 2, "option": 6}],
      "not_offered": [{"seat": 2, "option": 1}, {"seat": 2, "option": 2}, {"seat": 2, "option": 3}, {"seat": 3, "option": 4}]
    }
  },
  {
    "name": "Murderer finds the Witness: the Murderer side wins",
    "rule": "R20",
    "players": 6,
    "seed": 22,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 4}
    ],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "players": {"1": {"won": 0}, "2": {"won": 1}, "3": {"won": 1}, "4": {"won": 0}, "5": {"won": 0}, "6": {"won": 0}},
      "game": {"solved": true, "hunt_target": 4}
    }
  },
  {
    "name": "Murderer misses the Witness: the Investigator side, including the Scientist, wins",
    "rule": "R20",
    "players": 6,
    "seed": 23,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "winner": [1, 4, 5, 6],
      "standings": {"1": 1, "2": 0, "3": 0, "4": 1, "5": 1, "6": 1},
      "players": {"1": {"won": 1}, "2": {"won": 0}, "3": {"won": 0}, "4": {"won": 1}, "5": {"won": 1}, "6": {"won": 1}},
      "game": {"solved": true, "hunt_target": 6}
    }
  },
  {
    "name": "Round 5 ends unsolved: the Murderer side wins",
    "rule": "R21",
    "players": 6,
    "seed": 24,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "round": 4}
    },
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "players": {"1": {"won": 0}, "2": {"won": 1}, "3": {"won": 1}, "4": {"won": 0}, "5": {"won": 0}, "6": {"won": 0}},
      "game": {"round": 5, "solved": false, "hunt_target": 0}
    }
  },
  {
    "name": "A wrong accusation in round 1 leads to round 2, nobody has won",
    "rule": "R22",
    "players": 6,
    "seed": 25,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 6, "options_include": "Watch"},
      {"seat": 6, "options_include": "Drowning"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false, "current_tile": "Location"},
      "players": {"6": {"badge": 0}, "1": {"won": 0}, "2": {"won": 0}, "3": {"won": 0}, "6": {"won": 0}}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Seat 1 is the Scientist: no cards and no badge",
    "rule": "R1",
    "players": 6,
    "seed": 1,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "players": {"1": {"badge": 0, "won": 0}},
      "lens": {"players": {"1": {"clues": 0, "means": 0}}},
      "not_offered": [{"seat": 1, "option": "PASS"}]
    }
  },
  {
    "name": "7 players: the 6 non-Scientist seats are each dealt cards, so 12 clue words leave the deck (roles hidden, only counts asserted)",
    "rule": "R2",
    "players": 7,
    "seed": 2,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "lens": {
        "game": {"clue_deck": 4, "means_deck": 4},
        "players": {"1": {"clues": 0}, "2": {"clues": 2}, "3": {"clues": 2}, "4": {"clues": 2}, "5": {"clues": 2}, "6": {"clues": 2}, "7": {"clues": 2}}
      }
    }
  },
  {
    "name": "8 players: setup deals 7 seats (intel hidden, only observable state asserted)",
    "rule": "R3",
    "players": 8,
    "seed": 3,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "lens": {"game": {"clue_deck": 2, "means_deck": 2}},
      "game": {"round": 1, "solved": false}
    }
  },
  {
    "name": "With stated roles, a round of passes leaves the case unsolved and nobody has won",
    "rule": "R4",
    "players": 6,
    "seed": 4,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [{"seat": 4, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 1, "solved": false},
      "players": {"1": {"won": 0}, "2": {"won": 0}, "4": {"won": 0, "badge": 1}}
    }
  },
  {
    "name": "Seat 1 holds no cards and every other seat has a badge (Scientist intel is hidden)",
    "rule": "R5",
    "players": 6,
    "seed": 5,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "players": {"1": {"badge": 0}, "2": {"badge": 1}},
      "lens": {"players": {"1": {"clues": 0, "means": 0}}}
    }
  },
  {
    "name": "6 players: seats 2-6 hold 2 clues and 2 means each, decks hold the rest",
    "rule": "R6",
    "players": 6,
    "seed": 6,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "lens": {
        "game": {"clue_deck": 6, "means_deck": 6},
        "players": {
          "1": {"clues": 0, "means": 0},
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
    "name": "Murderer's other own clue and means (Key + Poison) is not the solution: wrong",
    "rule": "R7",
    "players": 6,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Key"},
      {"seat": 5, "options_include": "Poison"}
    ],
    "expect": {
      "game": {"solved": false, "round": 1},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "A round of passes leaves the case unsolved and no hunt (solution knowledge is hidden)",
    "rule": "R8",
    "players": 6,
    "seed": 8,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "game": {"solved": false, "round": 1, "hunt_target": 0}
    }
  },
  {
    "name": "Starting badges: seat 1 has 0, all others 1 (kept after a round of passes)",
    "rule": "R9",
    "players": 7,
    "seed": 9,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "players": {"1": {"badge": 0}, "2": {"badge": 1}, "3": {"badge": 1}, "4": {"badge": 1}, "5": {"badge": 1}, "6": {"badge": 1}, "7": {"badge": 1}}
    }
  },
  {
    "name": "Round 1 tile is Cause of Death",
    "rule": "R10",
    "players": 6,
    "seed": 10,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 1, "current_tile": "Cause of Death"}
    }
  },
  {
    "name": "Round 2 tile is Location",
    "rule": "R10",
    "players": 6,
    "seed": 11,
    "rounds": 2,
    "rules": [{"seat": 2, "options_include": "PASS", "times": "all"}],
    "expect": {
      "game": {"round": 2, "current_tile": "Location"}
    }
  },
  {
    "name": "Round 3 draws a tile from tile_deck and removes it (which tile is random)",
    "rule": "R11",
    "players": 6,
    "seed": 12,
    "rounds": 1,
    "given": {"game": {"round": 2}},
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 3},
      "lens": {"game": {"tile_deck": 5}}
    }
  },
  {
    "name": "Scientist marks in round 1 on the Cause of Death tile",
    "rule": "R12",
    "players": 6,
    "seed": 13,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 1, "current_tile": "Cause of Death"},
      "not_offered": [{"seat": 2, "option": "Cause of Death"}]
    }
  },
  {
    "name": "Scientist is never asked to accuse",
    "rule": "R13",
    "players": 6,
    "seed": 14,
    "rounds": 1,
    "rules": [{"seat": 2, "options_include": "PASS"}],
    "expect": {
      "not_offered": [{"seat": 1, "option": "PASS"}],
      "offered": [{"seat": 2, "option": "PASS"}],
      "players": {"1": {"badge": 0}}
    }
  },
  {
    "name": "A full round of talk and passes keeps every badge",
    "rule": "R14",
    "players": 6,
    "seed": 15,
    "rounds": 1,
    "rules": [{"seat": 3, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 1, "solved": false},
      "players": {"2": {"badge": 1}, "3": {"badge": 1}, "4": {"badge": 1}, "5": {"badge": 1}, "6": {"badge": 1}}
    }
  },
  {
    "name": "Only badge holders are asked to accuse, and only clues on the table are offered",
    "rule": "R15",
    "players": 6,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"], "badge": 0},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "clue_deck": ["Train Ticket", "Lipstick", "Receipt", "Hair", "Button", "Mask"]}
    },
    "rules": [{"seat": 6, "options_include": "PASS"}],
    "expect": {
      "offered": [{"seat": 6, "option": "PASS"}, {"seat": 6, "option": "Glove"}],
      "not_offered": [{"seat": 5, "option": "PASS"}, {"seat": 6, "option": "Mask"}, {"seat": 1, "option": "PASS"}],
      "players": {"5": {"badge": 0}, "6": {"badge": 1}}
    }
  },
  {
    "name": "A wrong accuser's badge drops to 0, and the game goes on",
    "rule": "R16",
    "players": 6,
    "seed": 17,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Wallet"},
      {"seat": 5, "options_include": "Insulin"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false},
      "players": {"5": {"badge": 0}, "6": {"badge": 1}}
    }
  },
  {
    "name": "Correct accusation Glove + Rope solves the case",
    "rule": "R17",
    "players": 6,
    "seed": 18,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 6},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Right clue with the wrong means (Glove + Poison) is wrong",
    "rule": "R17",
    "players": 6,
    "seed": 19,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Poison"}
    ],
    "expect": {
      "game": {"solved": false, "hunt_target": 0},
      "players": {"5": {"badge": 0}}
    }
  },
  {
    "name": "Clue and means from different players (Glove + Knife) is wrong",
    "rule": "R18",
    "players": 6,
    "seed": 20,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Knife"}
    ],
    "expect": {
      "game": {"solved": false, "round": 1},
      "players": {"5": {"badge": 0}, "2": {"won": 0}, "3": {"won": 0}}
    }
  },
  {
    "name": "Witness Hunt offers only seats other than 1, the Accomplice and the Murderer",
    "rule": "R19",
    "players": 6,
    "seed": 21,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 6, "options_include": "Glove"},
      {"seat": 6, "options_include": "Rope"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "game": {"solved": true, "hunt_target": 5},
      "offered": [{"seat": 2, "option": 4}, {"seat": 2, "option": 5}, {"seat": 2, "option": 6}],
      "not_offered": [{"seat": 2, "option": 1}, {"seat": 2, "option": 2}, {"seat": 2, "option": 3}, {"seat": 3, "option": 4}]
    }
  },
  {
    "name": "Murderer finds the Witness: the Murderer side wins",
    "rule": "R20",
    "players": 6,
    "seed": 22,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 4}
    ],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "players": {"1": {"won": 0}, "2": {"won": 1}, "3": {"won": 1}, "4": {"won": 0}, "5": {"won": 0}, "6": {"won": 0}},
      "game": {"solved": true, "hunt_target": 4}
    }
  },
  {
    "name": "Murderer misses the Witness: the Investigator side, including the Scientist, wins",
    "rule": "R20",
    "players": 6,
    "seed": 23,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 5, "options_include": "Glove"},
      {"seat": 5, "options_include": "Rope"},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "winner": [1, 4, 5, 6],
      "standings": {"1": 1, "2": 0, "3": 0, "4": 1, "5": 1, "6": 1},
      "players": {"1": {"won": 1}, "2": {"won": 0}, "3": {"won": 0}, "4": {"won": 1}, "5": {"won": 1}, "6": {"won": 1}},
      "game": {"solved": true, "hunt_target": 6}
    }
  },
  {
    "name": "Round 5 ends unsolved: the Murderer side wins",
    "rule": "R21",
    "players": 6,
    "seed": 24,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope", "round": 4}
    },
    "rules": [{"seat": 5, "options_include": "PASS"}],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 0, "2": 1, "3": 1, "4": 0, "5": 0, "6": 0},
      "players": {"1": {"won": 0}, "2": {"won": 1}, "3": {"won": 1}, "4": {"won": 0}, "5": {"won": 0}, "6": {"won": 0}},
      "game": {"round": 5, "solved": false, "hunt_target": 0}
    }
  },
  {
    "name": "A wrong accusation in round 1 leads to round 2, nobody has won",
    "rule": "R22",
    "players": 6,
    "seed": 25,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"role": "Scientist", "side": "investigator"},
        "2": {"role": "Murderer", "side": "murderer", "clues": ["Glove", "Key"], "means": ["Rope", "Poison"]},
        "3": {"role": "Accomplice", "side": "murderer", "clues": ["Diary", "Ring"], "means": ["Knife", "Pillow"]},
        "4": {"role": "Witness", "side": "investigator", "clues": ["Cigarette", "Phone"], "means": ["Hammer", "Pistol"]},
        "5": {"role": "Investigator", "side": "investigator", "clues": ["Wallet", "Photo"], "means": ["Insulin", "Brick"]},
        "6": {"role": "Investigator", "side": "investigator", "clues": ["Watch", "Umbrella"], "means": ["Drowning", "Electric Wire"]}
      },
      "game": {"key_evidence": "Glove", "means_of_murder": "Rope"}
    },
    "rules": [
      {"seat": 6, "options_include": "Watch"},
      {"seat": 6, "options_include": "Drowning"}
    ],
    "expect": {
      "game": {"round": 2, "solved": false, "current_tile": "Location"},
      "players": {"6": {"badge": 0, "won": 0}, "1": {"won": 0}, "2": {"won": 0}, "3": {"won": 0}}
    }
  }
]
```
````
