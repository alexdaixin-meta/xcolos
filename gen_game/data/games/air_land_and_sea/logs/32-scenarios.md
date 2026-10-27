# 32 scenarios

- time: 2026-10-27T18:02:08+00:00 (86.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 ca64c191be4f104c, reply sha256 1968038801cc5f1d

## Sent

````
SPEC:
{
  "name": "Air, Land and Sea: Three Fronts",
  "summary": "Two commanders fight a series of 6-round battles over three theaters, placing cards face-up or face-down and deciding each round whether to withdraw; the first to 12 VP wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 18,
    "theaters": 3,
    "min_strength": 1,
    "max_strength": 6,
    "hand_size": 6,
    "max_match_rounds": 36,
    "battle_rounds": 6,
    "last_battle_start_round": 31,
    "withdraw_base_vp": 2,
    "facedown_strength": 3,
    "battle_win_vp": 4,
    "sweep_vp": 6,
    "target_vp": 12
  },
  "attributes": {
    "player": [
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory points; the score",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards in hand, e.g. 'Air 4', in the order dealt",
        "observable": false
      },
      {
        "key": "air",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This player's total strength in Air this battle",
        "observable": true
      },
      {
        "key": "land",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This player's total strength in Land this battle",
        "observable": true
      },
      {
        "key": "sea",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This player's total strength in Sea this battle",
        "observable": true
      },
      {
        "key": "faceup_played",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards this player has placed face-up this battle, with their theater",
        "observable": false
      },
      {
        "key": "facedown_played",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Identities of cards this player has placed face-down this battle, with the theater each was placed in; the opponent sees only 'face-down card (strength 3) in [theater]'",
        "observable": false
      },
      {
        "key": "withdraw_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's secret Fight/Withdraw choice",
        "observable": false
      },
      {
        "key": "card_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's secret card choice",
        "observable": false
      },
      {
        "key": "theater_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's secret theater choice",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Undealt cards of the current battle; the 6 left after dealing stay unseen",
        "observable": false
      },
      {
        "key": "match_round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current match round, 1 to 36",
        "observable": true
      },
      {
        "key": "battle_round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round within the battle, 1 to 6",
        "observable": true
      },
      {
        "key": "battle_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the current battle has ended by withdrawal or resolution",
        "observable": false
      },
      {
        "key": "match_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when not enough match rounds remain for another full battle",
        "observable": false
      }
    ]
  },
  "setup": [
    "Both players start with 0 vp.",
    "The table sets match_round to 1, battle_round to 1, battle_over to false and match_over to false.",
    "Both players are told the full 18-card deck list: Air 1-6, Land 1-6 and Sea 1-6."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When battle_round == 1: deck is set to all 18 cards; each player's hand, faceup_played and facedown_played are emptied and air, land and sea are set to 0; then 6 random cards are moved from deck to each player's hand (6 draws each). The 6 cards left in deck stay unseen."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand in the order dealt, their facedown_played, and all public state."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "Fight or Withdraw",
      "effect": "Sets withdraw_choice for each player; nobody sees the other's answer until both are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If exactly one player's withdraw_choice is Withdraw, the other player's vp += 2 + floor((battle_round - 1) / 2). If at least one player withdrew, battle_over = true. Both choices are announced."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from own hand",
      "effect": "When battle_over is false: sets card_choice for each player; it stays secret until placement."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "Air, Land or Sea",
      "effect": "When battle_over is false: sets theater_choice for each player; it stays secret until placement."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When battle_over is false: card_choice is removed from each player's hand. If its theater equals theater_choice, it is appended to faceup_played and its printed strength is added to that player's attribute for theater_choice (air, land or sea). Otherwise it is appended to facedown_played and 3 is added to that attribute."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When battle_over is false: both new placements are announced. A face-up card shows its identity and theater. A face-down card shows only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced (each player's air, land and sea)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When battle_round == 6 and battle_over is false: in each theater the player with the higher strength controls it, and a tie means nobody does. The player controlling more theaters wins. If both control the same number, the player with the higher air+land+sea wins. If that is also equal, the battle is drawn and nobody scores. The winner's vp += 6 if they control all 3 theaters, otherwise += 4. battle_over = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When the battle was just resolved at battle_round 6: the battle result is announced and every card in both players' facedown_played is revealed to both players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "match_round += 1. If battle_over is true: battle_round = 1 and battle_over = false, and if match_round > 31 then match_over = true. Otherwise battle_round += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any player's vp >= 12, or match_over is true, or match_round > 36. Otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "any player's vp >= 12 OR match_over == true OR match_round > 36",
    "rank_by": "you.vp",
    "decided_by": "A player's standing is their VP. The first player to reach 12 VP wins; only one player can score in a battle, so both cannot reach 12 together. If the match ends on the round limit, the player with more VP wins, and equal VP is a draw (both share the result)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a battle starts (battle_round 1), then all 18 cards are shuffled, 6 are dealt into each player's hand, the remaining 6 stay unseen in the deck, and every theater strength is set to 0."
    },
    {
      "id": "R2",
      "text": "When each battle round starts, then both players choose Fight or Withdraw simultaneously, and neither sees the other's choice before both are in."
    },
    {
      "id": "R3",
      "text": "When exactly one player withdraws in battle round 1 or 2, then the other player gains 2 VP and the battle ends immediately."
    },
    {
      "id": "R4",
      "text": "When exactly one player withdraws in battle round 3 or 4, then the other player gains 3 VP and the battle ends immediately."
    },
    {
      "id": "R5",
      "text": "When exactly one player withdraws in battle round 5 or 6, then the other player gains 4 VP and the battle ends immediately."
    },
    {
      "id": "R6",
      "text": "When both players withdraw, then nobody scores and the battle ends immediately."
    },
    {
      "id": "R7",
      "text": "When a battle ends by withdrawal, then no card or theater choice is made that round."
    },
    {
      "id": "R8",
      "text": "When both players fight, then each secretly picks one card from their own hand and then secretly names Air, Land or Sea."
    },
    {
      "id": "R9",
      "text": "When a card is placed in its own theater, then it is face-up and adds its printed strength (1 to 6) to its owner's strength in that theater."
    },
    {
      "id": "R10",
      "text": "When a card is placed in a theater other than its own, then it is face-down and adds exactly 3 strength to its owner's strength in that theater."
    },
    {
      "id": "R11",
      "text": "When cards are placed, then each card leaves its owner's hand and both players are told every placement: face-up cards by identity, face-down cards only as 'face-down card (strength 3) in [theater]'. All six theater strengths are announced."
    },
    {
      "id": "R12",
      "text": "When battle round 6 is completed without a withdrawal, then in each theater the player with the higher strength controls it, and a tie means nobody controls it."
    },
    {
      "id": "R13",
      "text": "When a battle is resolved, then the player controlling more theaters wins the battle."
    },
    {
      "id": "R14",
      "text": "When both players control the same number of theaters, then the player with the higher total strength across all three theaters wins the battle."
    },
    {
      "id": "R15",
      "text": "When both players also have equal total strength, then the battle is drawn and nobody scores."
    },
    {
      "id": "R16",
      "text": "When a player wins a battle controlling fewer than 3 theaters, then they gain 4 VP."
    },
    {
      "id": "R17",
      "text": "When a player wins a battle controlling all 3 theaters, then they gain 6 VP."
    },
    {
      "id": "R18",
      "text": "When a battle is resolved, then all face-down card identities are revealed to both players."
    },
    {
      "id": "R19",
      "text": "When a battle ends and the next match round is 31 or earlier, then a new battle begins in the next match round."
    },
    {
      "id": "R20",
      "text": "When a battle ends and the next match round would be 32 or later, then the match ends."
    },
    {
      "id": "R21",
      "text": "When any player has 12 or more VP at the end of a round, then the match ends and that player wins."
    },
    {
      "id": "R22",
      "text": "When the match ends on the round limit, then the player with more VP wins, and equal VP is a draw."
    }
  ],
  "offers": [
    {
      "question": "Withdraw decision",
      "who": "both seats, every battle round",
      "options": "Fight, Withdraw"
    },
    {
      "question": "Card choice",
      "who": "both seats, only when neither player withdrew this round",
      "options": "each card currently in that seat's own hand, and nothing else"
    },
    {
      "question": "Theater choice",
      "who": "both seats, only when neither player withdrew this round",
      "options": "Air, Land, Sea"
    }
  ],
  "choices": [
    {
      "what": "2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed the game at 2. It is a head-to-head duel of bluffing and tempo: theater control is a two-sided comparison, and withdrawal VP go to 'the other player'. More seats would break both."
    },
    {
      "what": "No talk step",
      "why": "The source has no communication. With two opponents in a zero-sum duel, talk would only add bluffing words that the rules do not call for."
    },
    {
      "what": "Card choice and theater choice are two separate simultaneous polls",
      "why": "The source lists them as separate simultaneous steps. Neither answer is revealed until placement."
    },
    {
      "what": "Steps after the withdrawal are skipped with a `when battle_over is false` condition",
      "why": "This ends the battle immediately within a flat step list."
    },
    {
      "what": "The round limit is enforced through match_over, set when the next match round after a battle ends would be greater than 31",
      "why": "This states the rule that only a full battle may start."
    },
    {
      "what": "Card names are written as text like 'Air 4'",
      "why": "Each card is identified by its theater and strength."
    }
  ],
  "simplifications": [
    {
      "what": "A drawn match (equal VP at the round limit) is shown as both players sharing the top rank",
      "why": "The engine has no separate draw; players level at the top share the result."
    },
    {
      "what": "The battle resolution (controls, tie-break by total strength, 4 or 6 VP) is computed in one update step with conditional operations",
      "why": "It is all arithmetic on air, land and sea, so it needs no referee."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: vp, air, land, sea; table: match_round, battle_round.
````

## Reply

````
```json
[
  {"name": "Battle start resets strengths and deals 6 cards each with 6 left in the deck", "rule": "R1", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 9, "land": 5, "sea": 2}, "2": {"air": 4, "sea": 7}}, "game": {"battle_round": 1, "match_round": 1}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"players": {"1": {"air": 0, "land": 0, "sea": 0, "vp": 0}, "2": {"air": 0, "land": 0, "sea": 0, "vp": 0}},
              "lens": {"game": {"deck": 6}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},

  {"name": "Both seats are offered Fight and Withdraw each battle round", "rule": "R2", "players": 2, "rounds": 1, "default": "first",
   "given": {"game": {"battle_round": 1, "match_round": 1}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"offered": [{"seat": 1, "option": "Fight"}, {"seat": 1, "option": "Withdraw"}, {"seat": 2, "option": "Fight"}, {"seat": 2, "option": "Withdraw"}]}},

  {"name": "Withdrawal in battle round 2 gives the opponent 2 VP and ends the battle", "rule": "R3", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": ["Air 4", "Land 2", "Sea 1", "Air 2", "Land 6"]}, "2": {"hand": ["Land 5", "Sea 3", "Air 1", "Sea 6", "Land 3"]}},
             "game": {"battle_round": 2, "match_round": 2}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"players": {"1": {"vp": 2}, "2": {"vp": 0}}, "game": {"battle_round": 1, "match_round": 3}}},

  {"name": "Withdrawal in battle round 1 gives the opponent 2 VP", "rule": "R3", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"2": {"vp": 1}}, "game": {"battle_round": 1, "match_round": 1}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Fight"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 3}}, "game": {"battle_round": 1, "match_round": 2}}},

  {"name": "Withdrawal in battle round 3 gives the opponent 3 VP", "rule": "R4", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": ["Air 4", "Land 2", "Sea 1", "Air 2"]}, "2": {"hand": ["Land 5", "Sea 3", "Air 1", "Sea 6"]}},
             "game": {"battle_round": 3, "match_round": 3}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Fight"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 3}}, "game": {"battle_round": 1, "match_round": 4}}},

  {"name": "Withdrawal in battle round 4 gives the opponent 3 VP", "rule": "R4", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"vp": 2, "hand": ["Air 4", "Land 2", "Sea 1"]}, "2": {"hand": ["Land 5", "Sea 3", "Air 1"]}},
             "game": {"battle_round": 4, "match_round": 10}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"players": {"1": {"vp": 5}, "2": {"vp": 0}}, "game": {"battle_round": 1, "match_round": 11}}},

  {"name": "Withdrawal in battle round 5 gives the opponent 4 VP", "rule": "R5", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": ["Air 4", "Land 2"]}, "2": {"hand": ["Land 5", "Sea 3"]}},
             "game": {"battle_round": 5, "match_round": 5}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"players": {"1": {"vp": 4}, "2": {"vp": 0}}, "game": {"battle_round": 1, "match_round": 6}}},

  {"name": "Withdrawal in battle round 6 gives the opponent 4 VP and no resolution happens", "rule": "R5", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 10, "land": 10, "sea": 10, "hand": ["Air 4"]}, "2": {"vp": 1, "hand": ["Land 5"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Fight"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 5}}, "game": {"battle_round": 1, "match_round": 7}}},

  {"name": "Both withdraw: nobody scores and the battle ends", "rule": "R6", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"vp": 3, "hand": ["Air 4", "Land 2", "Sea 1"]}, "2": {"vp": 2, "hand": ["Land 5", "Sea 3", "Air 1"]}},
             "game": {"battle_round": 4, "match_round": 4}},
   "rules": [{"seat": 1, "options_include": "Withdraw"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"players": {"1": {"vp": 3}, "2": {"vp": 2}}, "game": {"battle_round": 1, "match_round": 5}}},

  {"name": "After a withdrawal no card or theater is chosen and no strength changes", "rule": "R7", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 2, "land": 1, "sea": 0, "hand": ["Air 4", "Land 2", "Sea 1"]}, "2": {"air": 0, "land": 3, "sea": 1, "hand": ["Land 5", "Sea 3", "Air 1"]}},
             "game": {"battle_round": 4, "match_round": 4}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Withdraw"}],
   "expect": {"not_offered": [{"seat": 1, "option": "Air 4"}, {"seat": 2, "option": "Land 5"}, {"seat": 1, "option": "Sea"}, {"seat": 2, "option": "Sea"}],
              "players": {"1": {"vp": 3}}}},

  {"name": "When both fight, each picks a card from its own hand and then a theater", "rule": "R8", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": ["Air 4", "Land 2"]}, "2": {"hand": ["Land 5", "Sea 1"]}},
             "game": {"battle_round": 2, "match_round": 2}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 4"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 5"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"offered": [{"seat": 1, "option": "Air 4"}, {"seat": 1, "option": "Land 2"}, {"seat": 2, "option": "Land 5"}, {"seat": 2, "option": "Sea 1"},
                          {"seat": 1, "option": "Air"}, {"seat": 1, "option": "Land"}, {"seat": 1, "option": "Sea"},
                          {"seat": 2, "option": "Air"}, {"seat": 2, "option": "Land"}, {"seat": 2, "option": "Sea"}],
              "not_offered": [{"seat": 1, "option": "Land 5"}, {"seat": 2, "option": "Air 4"}]}},

  {"name": "A card placed in its own theater adds its printed strength", "rule": "R9", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 2, "land": 0, "sea": 0, "hand": ["Air 4", "Land 2"]}, "2": {"air": 0, "land": 0, "sea": 1, "hand": ["Land 5", "Sea 1"]}},
             "game": {"battle_round": 2, "match_round": 2}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 4"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 5"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"air": 6, "land": 0, "sea": 0}, "2": {"air": 0, "land": 5, "sea": 1}}, "game": {"battle_round": 3, "match_round": 3}}},

  {"name": "A card placed outside its theater adds exactly 3", "rule": "R10", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 1, "land": 0, "sea": 0, "hand": ["Sea 6", "Land 2"]}, "2": {"air": 0, "land": 0, "sea": 2, "hand": ["Land 1", "Air 5"]}},
             "game": {"battle_round": 2, "match_round": 2}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Sea 6"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Sea"}],
   "expect": {"players": {"1": {"air": 4, "land": 0, "sea": 0}, "2": {"air": 0, "land": 0, "sea": 5}}}},

  {"name": "Placed cards leave their owners' hands", "rule": "R11", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"hand": ["Air 4", "Land 2", "Sea 3"]}, "2": {"hand": ["Land 5", "Sea 1", "Air 6"]}},
             "game": {"battle_round": 3, "match_round": 3}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Land 2"}, {"seat": 1, "options_include": "Land"},
             {"seat": 2, "options_include": "Air 6"}, {"seat": 2, "options_include": "Sea"}],
   "expect": {"lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}}}}},

  {"name": "A tied theater is controlled by nobody: 2 theaters to 0 earns 4, not 6", "rule": "R12", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 4, "land": 6, "sea": 7, "hand": ["Air 1"]}, "2": {"air": 2, "land": 2, "sea": 3, "hand": ["Air 3"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 1"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Air 3"}, {"seat": 2, "options_include": "Air"}],
   "expect": {"players": {"1": {"vp": 4}, "2": {"vp": 0}}}},

  {"name": "More theaters controlled wins even with a lower total strength", "rule": "R13", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 4, "land": 4, "sea": 1, "hand": ["Air 1"]}, "2": {"air": 1, "land": 1, "sea": 15, "hand": ["Land 1"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 1"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"vp": 4, "air": 5, "land": 4, "sea": 1}, "2": {"vp": 0, "air": 1, "land": 2, "sea": 15}}}},

  {"name": "Equal theaters controlled: higher total strength wins", "rule": "R14", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 4, "land": 6, "sea": 2, "hand": ["Air 1"]}, "2": {"air": 2, "land": 3, "sea": 9, "hand": ["Air 3"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 1"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Air 3"}, {"seat": 2, "options_include": "Air"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 4}}}},

  {"name": "Equal theaters and equal total strength: the battle is drawn", "rule": "R15", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"vp": 3, "air": 5, "land": 2, "sea": 4, "hand": ["Air 1"]}, "2": {"vp": 3, "air": 2, "land": 5, "sea": 4, "hand": ["Land 1"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Air 1"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"vp": 3}, "2": {"vp": 3}}, "game": {"battle_round": 1, "match_round": 7}}},

  {"name": "Winning with 2 theaters gives 4 VP", "rule": "R16", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"vp": 5, "air": 6, "land": 7, "sea": 1, "hand": ["Sea 2"]}, "2": {"vp": 2, "air": 3, "land": 3, "sea": 6, "hand": ["Land 1"]}},
             "game": {"battle_round": 6, "match_round": 12}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Sea 2"}, {"seat": 1, "options_include": "Sea"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"vp": 9, "sea": 3}, "2": {"vp": 2, "land": 4}}}},

  {"name": "Winning with all 3 theaters gives 6 VP", "rule": "R17", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"vp": 2, "air": 6, "land": 7, "sea": 5, "hand": ["Sea 2"]}, "2": {"vp": 0, "air": 3, "land": 3, "sea": 4, "hand": ["Land 1"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Sea 2"}, {"seat": 1, "options_include": "Sea"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"vp": 8}, "2": {"vp": 0}}}},

  {"name": "A battle resolved with a face-down card counts it as 3 and a new battle follows", "rule": "R18", "players": 2, "rounds": 1, "default": "first",
   "given": {"players": {"1": {"air": 3, "land": 5, "sea": 1, "hand": ["Sea 6"]}, "2": {"air": 5, "land": 2, "sea": 4, "hand": ["Land 1"]}},
             "game": {"battle_round": 6, "match_round": 6}},
   "rules": [{"seat": 1, "options_include": "Fight"}, {"seat": 2, "options_include": "Fight"},
             {"seat": 1, "options_include": "Sea 6"}, {"seat": 1, "options_include": "Air"},
             {"seat": 2, "options_include": "Land 1"}, {"seat": 2, "options_include": "Land"}],
   "expect": {"players": {"1": {"vp": 4}, "2": {"vp": 0}}, "game": {"battle_round": 1, "match_round": 7}}},

  {"name": "A battle ending at match round 30 lets a new battle start in round 31", "rule": "R19", "players": 2, "rounds": 2, "default": "first",
   "given": {"game": {"battle_round": 1, "match_round": 30}},
   "rules": [{"seat": 1, "options_include": "Fight", "times": "all"}, {"seat": 2, "options_include": "Withdraw", "times": "all"}],
   "expect": {"players": {"1": {"vp": 4}, "2": {"vp": 0}}, "game": {"match_round": 32}}},

  {"name": "A battle ending at match round 31 ends the match; higher VP wins", "rule": "R20", "players": 2, "default": "first",
   "given": {"players": {"1": {"vp": 5}, "2": {"vp": 6}}, "game": {"battle_round": 1, "match_round": 31}},
   "rules": [{"seat": 1, "options_include": "Fight", "times": "all"}, {"seat": 2, "options_include": "Withdraw", "times": "all"}],
   "expect": {"winner": 1, "standings": {"1": 7, "2": 6}, "players": {"1": {"vp": 7}, "2": {"vp": 6}}, "game": {"match_round": 32}}},

  {"name": "Reaching 12 VP ends the match at once and that player wins", "rule": "R21", "players": 2, "default": "first",
   "given": {"players": {"1": {"vp": 10, "hand": ["Air 4", "Land 2", "Sea 1", "Air 2", "Land 6"]}, "2": {"vp": 8, "hand": ["Land 5", "Sea 3", "Air 1", "Sea 6", "Land 3"]}},
             "game": {"battle_round": 2, "match_round": 5}},
   "rules": [{"seat": 1, "options_include": "Fight", "times": "all"}, {"seat": 2, "options_include": "Withdraw", "times": 1}],
   "expect": {"winner": 1, "standings": {"1": 12, "2": 8}, "players": {"1": {"vp": 12}, "2": {"vp": 8}}, "game": {"match_round": 6}}},

  {"name": "Equal VP at the round limit is a shared result", "rule": "R22", "players": 2, "default": "first",
   "given": {"players": {"1": {"vp": 5}, "2": {"vp": 5}}, "game": {"battle_round": 1, "match_round": 31}},
   "rules": [{"seat": 1, "options_include": "Withdraw", "times": "all"}, {"seat": 2, "options_include": "Withdraw", "times": "all"}],
   "expect": {"winner": [1, 2], "standings": {"1": 5, "2": 5}, "players": {"1": {"vp": 5}, "2": {"vp": 5}}}}
]
```
````
