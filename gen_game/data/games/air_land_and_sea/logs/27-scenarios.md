# 27 scenarios

- time: 2026-10-27T17:57:07+00:00 (79.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 5b80a274594cebc8, reply sha256 b15b599e96c652eb

## Sent

````
SPEC:
{
  "name": "Air, Land and Sea: Four Battles",
  "summary": "Two commanders fight 4 battles of 6 rounds over three theaters, playing cards face-up for their strength or face-down for 2, and may withdraw early to limit the VP the opponent gains.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "total_cards": 18,
    "theaters": 3,
    "min_strength": 1,
    "max_strength": 6,
    "total_rounds": 24,
    "battles": 4,
    "rounds_per_battle": 6,
    "hand_size": 6,
    "set_aside_count": 6,
    "improvise_strength": 2,
    "withdraw_vp_4_plus_cards": 2,
    "withdraw_vp_2_or_3_cards": 3,
    "withdraw_vp_1_card": 4,
    "battle_win_vp": 6,
    "theaters_to_win_battle": 2
  },
  "attributes": {
    "player": [
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "victory points earned so far",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "cards held this battle, such as 'Air 3'",
        "observable": false
      },
      {
        "key": "air",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "this player's strength in the Air theater this battle",
        "observable": true
      },
      {
        "key": "land",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "this player's strength in the Land theater this battle",
        "observable": true
      },
      {
        "key": "sea",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "this player's strength in the Sea theater this battle",
        "observable": true
      },
      {
        "key": "face_up",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "cards this player deployed face-up this battle",
        "observable": false
      },
      {
        "key": "face_down",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "identities of cards this player improvised face-down this battle, with their theater; the opponent sees only the +2 in that theater's strength",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current round, 1 to 24",
        "observable": true
      },
      {
        "key": "battle",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current battle, floor((round-1)/6)+1",
        "observable": true
      },
      {
        "key": "round_in_battle",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "round - 6*(battle-1)",
        "observable": false
      },
      {
        "key": "first_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "first player: seat 1 in battles 1 and 3, seat 2 in battles 2 and 4",
        "observable": false
      },
      {
        "key": "battle_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once the current battle has been decided by withdrawal or by the battle end",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Air 1",
          "Air 2",
          "Air 3",
          "Air 4",
          "Air 5",
          "Air 6",
          "Land 1",
          "Land 2",
          "Land 3",
          "Land 4",
          "Land 5",
          "Land 6",
          "Sea 1",
          "Sea 2",
          "Sea 3",
          "Sea 4",
          "Sea 5",
          "Sea 6"
        ],
        "meaning": "the 18 cards to be shuffled and dealt at each battle start",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 6 undealt cards, out of play this battle",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat both players. Each player's vp is 0.",
    "round is set to 1 and battle_over to false.",
    "The deck holds all 18 cards: Air 1-6, Land 1-6 and Sea 1-6."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set battle = floor((round-1)/6)+1. Set round_in_battle = round - 6*(battle-1). Set first_seat = 1 if battle is 1 or 3, and 2 if battle is 2 or 4. Announce the round, the battle and the first player."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Only when round_in_battle = 1 (battle start): set battle_over = false. Set every player's air, land and sea to 0. Return every card in each hand, face_up, face_down and set_aside to deck, so deck holds all 18 cards. Draw 6 cards at random from deck into each player's hand, removing each from deck. Move the remaining 6 deck cards to set_aside."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand and face_down, plus every public attribute: all air, land and sea strengths, all face_up cards, vp, round, battle, first_seat and battle_over."
    },
    {
      "action": "ask",
      "who": "the seat named by first_seat, only when battle_over is false",
      "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'",
      "effect": "Deploy: remove the card from hand, append it to face_up, and add its number to the player's strength in the theater named on the card. Improvise: remove the card from hand, append it with the chosen theater to face_down, and add 2 to the player's strength in the chosen theater; only the theater and the +2 are announced. Withdraw: let n = length of the player's hand; the opponent's vp += 4 if n = 1, 3 if n is 2 or 3, and 2 if n >= 4; set battle_over = true."
    },
    {
      "action": "ask",
      "who": "the seat that is not first_seat, only when battle_over is false",
      "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand and any theater, or 'withdraw'",
      "effect": "Same effects as the first player's action, applied to this player."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Only when round_in_battle = 6 and battle_over is false (battle end): in each of air, land and sea, the player with the higher strength controls that theater, and a tie goes to the first_seat player. The player who controls 2 or more theaters gains vp += 6. Set battle_over = true. Announce the strengths and the battle winner."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round = 24, end the game. Otherwise continue."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1."
    }
  ],
  "ending": {
    "condition": "round = 24 after that round's steps have run",
    "rank_by": "you.vp",
    "decided_by": "Each player's standing is their total VP after round 24. The player with more VP wins. Equal VP is a draw, and both players share the win."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 18 cards, Air 1-6, Land 1-6 and Sea 1-6, and a card's strength is its number."
    },
    {
      "id": "R2",
      "text": "The match has 24 rounds, and battle = floor((round-1)/6)+1, so rounds 1-6 are battle 1, rounds 7-12 battle 2, rounds 13-18 battle 3 and rounds 19-24 battle 4."
    },
    {
      "id": "R3",
      "text": "When the battle is 1 or 3, then seat 1 is the first player; when the battle is 2 or 4, then seat 2 is the first player."
    },
    {
      "id": "R4",
      "text": "When round_in_battle = 1, then battle_over becomes false, every air, land and sea strength becomes 0, and all played cards are cleared."
    },
    {
      "id": "R5",
      "text": "When round_in_battle = 1, then all 18 cards are shuffled, each player is dealt 6 cards privately into hand, and the remaining 6 go to set_aside, out of play and unseen."
    },
    {
      "id": "R6",
      "text": "When battle_over is false, then the first player takes exactly one action, and the second player then takes one action if battle_over is still false."
    },
    {
      "id": "R7",
      "text": "When a player deploys a card such as Land 5, then it leaves their hand face-up and their land strength rises by 5."
    },
    {
      "id": "R8",
      "text": "When a player improvises a card to a chosen theater, then it leaves their hand face-down and their strength in that theater rises by 2, whatever the card's number or suit."
    },
    {
      "id": "R9",
      "text": "When a card is improvised, then the opponent sees only the theater and the +2, never the card's identity."
    },
    {
      "id": "R10",
      "text": "When a player withdraws with 4 or more cards in hand, then the opponent gains 2 VP."
    },
    {
      "id": "R11",
      "text": "When a player withdraws with 2 or 3 cards in hand, then the opponent gains 3 VP."
    },
    {
      "id": "R12",
      "text": "When a player withdraws with 1 card in hand, then the opponent gains 4 VP."
    },
    {
      "id": "R13",
      "text": "When a player withdraws, then battle_over becomes true at once, and if the first player withdrew, then the second player does not act that round."
    },
    {
      "id": "R14",
      "text": "When battle_over is true, then the remaining rounds of that battle pass with no actions and no scoring, and the next battle starts at its fixed round."
    },
    {
      "id": "R15",
      "text": "When round_in_battle = 6 and battle_over is false after both actions, then in each theater the player with the higher strength controls it, and a tie goes to the battle's first player."
    },
    {
      "id": "R16",
      "text": "When a player controls 2 or more of the 3 theaters at a battle end, then they gain 6 VP and battle_over becomes true."
    },
    {
      "id": "R17",
      "text": "When round 24 ends, then the game ends, the player with more VP wins, and equal VP is a draw."
    }
  ],
  "offers": [
    {
      "question": "First player's action (when battle_over is false)",
      "who": "the seat named by first_seat",
      "options": "'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'."
    },
    {
      "question": "Second player's action (when battle_over is still false)",
      "who": "the seat that is not first_seat",
      "options": "'deploy <card>' for each card in their hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in their hand; 'withdraw'. Not asked at all if the first player withdrew this round."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed the table at 2. Theater control is a head-to-head comparison, the tie rule names the battle's first player, and withdrawal VP goes to 'the opponent', so the game is defined only for two."
    },
    {
      "what": "No talk step",
      "why": "The source has none. With two directly opposed players there is no coalition to form, so talk would only add words. The strategy lies in bluffing with face-down cards, reading the opponent's public strengths and judging when to withdraw cheaply."
    },
    {
      "what": "Actions use sequential ask",
      "why": "The rules order the first player before the second, and the second player reacts to the first player's public play."
    },
    {
      "what": "Withdrawal VP for 0 cards is not defined",
      "why": "A player always holds at least 1 card when acting, since 6 cards cover 6 actions, so the 0-card case never occurs."
    }
  ],
  "simplifications": [
    {
      "what": "Theater control compares two players' attributes",
      "why": "The engine has no player-attribute operand. The comparison of seat 1's and seat 2's air, land and sea is done with a table-attribute mirror beside the strengths, the listed workaround; the outcome is unchanged."
    },
    {
      "what": "Battle start is a single update with operations guarded by round_in_battle = 1",
      "why": "The step list is flat, so conditional operations replace a separate block. The behavior is identical."
    },
    {
      "what": "Shuffling is modeled as random draws from the deck list",
      "why": "Drawing at random is equivalent to shuffling and then dealing."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: vp, air, land, sea; table: round, battle.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the 'After battle_over the rest of the battle passes with no actions and no scoring' scenario. Do not attach option rules (withdraw or anything else) to rounds where battle_over is already true, because no seat is offered any action then. Choose one of two shapes. (1) Start mid-battle with battle_over false, have one seat withdraw in the first round played, and attach no rules to later rounds of that battle. (2) Start with battle_over true at, say, round_in_battle 3 or 4 and attach no option rules. In both, run until the battle's remaining rounds pass, then assert only on public results: both players' vp unchanged after the withdrawal award (no battle-end 6 VP at round_in_battle 6), the round number advanced, and, if the run crosses into the next battle, battle updated with air/land/sea reset to 0. If you want to show play resuming, add a rule for the first player of the next battle at its first round (seat 2 for battles 2 and 4, seat 1 for battles 1 and 3). Do not assert on battle_over itself or on whose turn it is.
````

## Reply

````
```json
[
  {
    "name": "A card's strength is its number: deploying Sea 6 adds 6 to sea, Land 3 adds 3 to land",
    "rule": "R1",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Sea 6", "Air 1", "Land 1", "Air 2", "Land 2"], "air": 0, "land": 0, "sea": 0, "vp": 0},
        "2": {"hand": ["Land 3", "Air 4", "Sea 1", "Sea 2", "Air 3"], "air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 2, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Sea 6"},
      {"seat": 2, "options_include": "deploy Land 3"}
    ],
    "expect": {
      "players": {
        "1": {"sea": 6, "air": 0, "land": 0},
        "2": {"land": 3, "air": 0, "sea": 0}
      }
    }
  },
  {
    "name": "Round 7 belongs to battle 2",
    "rule": "R2",
    "players": 2,
    "rounds": 2,
    "given": {
      "players": {"1": {"vp": 0}, "2": {"vp": 0}},
      "game": {"round": 6, "battle_over": true}
    },
    "rules": [
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "game": {"round": 8, "battle": 2}
    }
  },
  {
    "name": "In battle 2 seat 2 acts first; its withdrawal means seat 1 is never asked",
    "rule": "R3",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Air 3", "Land 1", "Land 2"], "vp": 0, "air": 0, "land": 0, "sea": 0},
        "2": {"hand": ["Sea 1", "Sea 2", "Sea 3", "Land 4", "Land 5"], "vp": 0, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 8, "battle_over": false}
    },
    "rules": [
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {"1": {"vp": 2}, "2": {"vp": 0}},
      "offered": [{"seat": 2, "option": "withdraw"}],
      "not_offered": [{"seat": 1, "option": "withdraw"}]
    }
  },
  {
    "name": "In battle 3 seat 1 acts first; its withdrawal means seat 2 is never asked",
    "rule": "R3",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Air 3", "Land 1", "Land 2"], "vp": 0, "air": 0, "land": 0, "sea": 0},
        "2": {"hand": ["Sea 1", "Sea 2", "Sea 3", "Land 4", "Land 5"], "vp": 0, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 14, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {"1": {"vp": 0}, "2": {"vp": 2}},
      "offered": [{"seat": 1, "option": "withdraw"}],
      "not_offered": [{"seat": 2, "option": "withdraw"}]
    }
  },
  {
    "name": "At the start of battle 2 every theater strength is reset to 0",
    "rule": "R4",
    "players": 2,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"air": 5, "land": 4, "sea": 3, "vp": 0},
        "2": {"air": 2, "land": 6, "sea": 1, "vp": 0}
      },
      "game": {"round": 6, "battle_over": true}
    },
    "rules": [
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {
        "1": {"air": 0, "land": 0, "sea": 0, "vp": 2},
        "2": {"air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 8, "battle": 2}
    }
  },
  {
    "name": "Battle start deals 6 cards to each hand and sets 6 aside (first player withdraws, so no card leaves a hand)",
    "rule": "R5",
    "players": 2,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "withdraw"}
    ],
    "expect": {
      "lens": {
        "players": {"1": {"hand": 6}, "2": {"hand": 6}},
        "game": {"set_aside": 6, "deck": 0}
      },
      "players": {"1": {"vp": 0}, "2": {"vp": 2}}
    }
  },
  {
    "name": "With the battle running, the first player acts and then the second player acts once",
    "rule": "R6",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 4", "Air 1", "Land 1", "Sea 1", "Land 2"], "air": 0, "land": 0, "sea": 0, "vp": 0},
        "2": {"hand": ["Sea 5", "Air 2", "Land 3", "Sea 2", "Air 3"], "air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 2, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Air 4"},
      {"seat": 2, "options_include": "deploy Sea 5"}
    ],
    "expect": {
      "players": {
        "1": {"air": 4, "land": 0, "sea": 0},
        "2": {"sea": 5, "air": 0, "land": 0}
      },
      "offered": [{"seat": 1, "option": "deploy Air 4"}, {"seat": 2, "option": "deploy Sea 5"}]
    }
  },
  {
    "name": "Deploying Land 5 raises land strength by 5",
    "rule": "R7",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Land 5", "Air 1", "Sea 1", "Air 2"], "air": 1, "land": 2, "sea": 0, "vp": 0},
        "2": {"hand": ["Air 6", "Land 1", "Sea 2", "Sea 3"], "air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 3, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Land 5"},
      {"seat": 2, "options_include": "deploy Air 6"}
    ],
    "expect": {
      "players": {
        "1": {"land": 7, "air": 1, "sea": 0},
        "2": {"air": 6, "land": 0, "sea": 0}
      }
    }
  },
  {
    "name": "Improvising Sea 6 to Air adds only 2 to air and nothing to sea",
    "rule": "R8",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Sea 6", "Air 1", "Land 1", "Air 2"], "air": 3, "land": 0, "sea": 0, "vp": 0},
        "2": {"hand": ["Land 6", "Air 3", "Sea 2", "Sea 3"], "air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 3, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "improvise Sea 6 to Air"},
      {"seat": 2, "options_include": "deploy Land 6"}
    ],
    "expect": {
      "players": {
        "1": {"air": 5, "sea": 0, "land": 0},
        "2": {"land": 6, "air": 0, "sea": 0}
      }
    }
  },
  {
    "name": "An improvised Land 6 shows publicly as only +2 in land, not 6",
    "rule": "R9",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Sea 1", "Sea 2", "Land 1"], "air": 0, "land": 0, "sea": 0, "vp": 0},
        "2": {"hand": ["Land 6", "Air 3", "Sea 3", "Air 4", "Land 2"], "air": 0, "land": 0, "sea": 0, "vp": 0}
      },
      "game": {"round": 2, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Air 1"},
      {"seat": 2, "options_include": "improvise Land 6 to Land"}
    ],
    "expect": {
      "players": {
        "1": {"air": 1, "land": 0, "sea": 0},
        "2": {"land": 2, "air": 0, "sea": 0}
      }
    }
  },
  {
    "name": "Withdrawing with 4 cards in hand gives the opponent 2 VP",
    "rule": "R10",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Land 1", "Sea 1"], "vp": 0},
        "2": {"hand": ["Air 3", "Land 2", "Sea 2", "Sea 3"], "vp": 1}
      },
      "game": {"round": 3, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {"1": {"vp": 0}, "2": {"vp": 3}}
    }
  },
  {
    "name": "The second player withdrawing with 2 cards in hand gives the opponent 3 VP",
    "rule": "R11",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Land 1"], "vp": 0, "air": 0, "land": 0, "sea": 0},
        "2": {"hand": ["Sea 2", "Sea 3"], "vp": 0, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 5, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Air 1"},
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {"1": {"vp": 3, "air": 1}, "2": {"vp": 0}}
    }
  },
  {
    "name": "Withdrawing with 1 card in hand in round 6 gives the opponent 4 VP and no battle-end scoring",
    "rule": "R12",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1"], "vp": 0, "air": 1, "land": 1, "sea": 1},
        "2": {"hand": ["Sea 2"], "vp": 0, "air": 6, "land": 6, "sea": 6}
      },
      "game": {"round": 6, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {"1": {"vp": 0}, "2": {"vp": 4}}
    }
  },
  {
    "name": "When the first player withdraws, the second player gets no action that round",
    "rule": "R13",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Land 1", "Sea 1"], "vp": 0, "air": 0, "land": 0, "sea": 0},
        "2": {"hand": ["Air 3", "Land 2", "Sea 2", "Sea 3"], "vp": 0, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 3, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {
        "1": {"vp": 0},
        "2": {"vp": 2, "air": 0, "land": 0, "sea": 0}
      },
      "not_offered": [
        {"seat": 2, "option": "withdraw"},
        {"seat": 2, "option": "deploy Air 3"}
      ]
    }
  },
  {
    "name": "After a withdrawal the rest of the battle passes with no actions and no scoring, then battle 2 starts at round 7",
    "rule": "R14",
    "players": 2,
    "rounds": 5,
    "given": {
      "players": {
        "1": {"hand": ["Air 1", "Air 2", "Land 1", "Sea 1"], "vp": 0, "air": 1, "land": 0, "sea": 0},
        "2": {"hand": ["Air 3", "Land 2", "Sea 2", "Sea 3"], "vp": 0, "air": 6, "land": 6, "sea": 6}
      },
      "game": {"round": 3, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "withdraw"},
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "players": {
        "1": {"vp": 2, "air": 0, "land": 0, "sea": 0},
        "2": {"vp": 2, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 8, "battle": 2}
    }
  },
  {
    "name": "At the end of battle 1, tied theaters go to seat 1 (the first player), so seat 1 wins the battle",
    "rule": "R15",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Sea 1"], "vp": 0, "air": 5, "land": 3, "sea": 0},
        "2": {"hand": ["Sea 2"], "vp": 0, "air": 5, "land": 3, "sea": 0}
      },
      "game": {"round": 6, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Sea 1"},
      {"seat": 2, "options_include": "deploy Sea 2"}
    ],
    "expect": {
      "players": {
        "1": {"vp": 6, "sea": 1},
        "2": {"vp": 0, "sea": 2}
      }
    }
  },
  {
    "name": "At the end of battle 2, tied theaters go to seat 2 (the first player), so seat 2 wins the battle",
    "rule": "R15",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Sea 2"], "vp": 0, "air": 4, "land": 2, "sea": 0},
        "2": {"hand": ["Sea 1"], "vp": 0, "air": 4, "land": 2, "sea": 0}
      },
      "game": {"round": 12, "battle_over": false}
    },
    "rules": [
      {"seat": 2, "options_include": "deploy Sea 1"},
      {"seat": 1, "options_include": "deploy Sea 2"}
    ],
    "expect": {
      "players": {
        "1": {"vp": 0, "sea": 2},
        "2": {"vp": 6, "sea": 1}
      }
    }
  },
  {
    "name": "Controlling 2 of the 3 theaters at battle end gains 6 VP",
    "rule": "R16",
    "players": 2,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Land 2"], "vp": 0, "air": 6, "land": 1, "sea": 2},
        "2": {"hand": ["Air 1"], "vp": 3, "air": 2, "land": 4, "sea": 3}
      },
      "game": {"round": 6, "battle_over": false}
    },
    "rules": [
      {"seat": 1, "options_include": "deploy Land 2"},
      {"seat": 2, "options_include": "improvise Air 1 to Sea"}
    ],
    "expect": {
      "players": {
        "1": {"vp": 0, "land": 3, "air": 6, "sea": 2},
        "2": {"vp": 9, "sea": 5, "air": 2, "land": 4}
      }
    }
  },
  {
    "name": "After round 24 the game ends and the seat with more VP wins",
    "rule": "R17",
    "players": 2,
    "given": {
      "players": {
        "1": {"hand": ["Air 6"], "vp": 10, "air": 0, "land": 4, "sea": 4},
        "2": {"hand": ["Air 1"], "vp": 8, "air": 3, "land": 5, "sea": 5}
      },
      "game": {"round": 24, "battle_over": false}
    },
    "rules": [
      {"seat": 2, "options_include": "deploy Air 1"},
      {"seat": 1, "options_include": "deploy Air 6"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 10, "2": 14},
      "players": {"1": {"vp": 10}, "2": {"vp": 14}}
    }
  },
  {
    "name": "Equal VP after round 24 is a draw shared by both seats",
    "rule": "R17",
    "players": 2,
    "given": {
      "players": {
        "1": {"hand": ["Air 6"], "vp": 8, "air": 0, "land": 0, "sea": 0},
        "2": {"hand": ["Air 1"], "vp": 12, "air": 0, "land": 0, "sea": 0}
      },
      "game": {"round": 24, "battle_over": false}
    },
    "rules": [
      {"seat": 2, "options_include": "withdraw"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 12, "2": 12},
      "players": {"1": {"vp": 12}, "2": {"vp": 12}}
    }
  }
]
```
````
