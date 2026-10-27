# 05 scenarios

- time: 2026-10-27T17:25:50+00:00 (37.0s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 dd1b49b7eba18fed, reply sha256 b0b7b5c4f788d7e5

## Sent

````
SPEC:
{
  "name": "Three Fronts",
  "summary": "Two players fight 4 battles of 6 rounds over three theaters (Air, Land, Sea). Each round a player deploys a card face-up, improvises it face-down for strength 2, or withdraws to give up fewer VP; winning 2 of 3 theaters scores 6 VP.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 18,
    "suits": 3,
    "ranks_per_suit": 6,
    "min_rank": 1,
    "max_rank": 6,
    "battles": 4,
    "rounds_per_battle": 6,
    "total_rounds": 24,
    "hand_size": 6,
    "set_aside_cards": 6,
    "improvise_strength": 2,
    "withdraw_min_cards_held": 1,
    "withdraw_vp_4_or_more_cards": 4,
    "withdraw_vp_value_4_or_more": 2,
    "withdraw_vp_value_2_or_3": 3,
    "withdraw_vp_value_1": 4,
    "theaters_to_win_battle": 2,
    "battle_win_vp": 6,
    "starting_vp": 0
  },
  "attributes": {
    "player": [
      {
        "key": "vp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory points scored in the match so far.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards the player holds in the current battle, such as 'Air 4'.",
        "observable": false
      },
      {
        "key": "air_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total strength on this player's side of Air this battle: face-up cards count their rank, face-down cards count 2.",
        "observable": true
      },
      {
        "key": "land_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total strength on this player's side of Land this battle.",
        "observable": true
      },
      {
        "key": "sea_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total strength on this player's side of Sea this battle.",
        "observable": true
      },
      {
        "key": "face_up_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards deployed face-up this battle. Each card sits in the theater of its own suit.",
        "observable": false
      },
      {
        "key": "face_down_theaters",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The theater of each face-down card placed this battle. Both players see this.",
        "observable": false
      },
      {
        "key": "face_down_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The identity and theater of each face-down card this player placed, such as 'Land 5 in Sea'. Only the owner knows it until the battle is fought to the end.",
        "observable": false
      }
    ],
    "game": [
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
        "meaning": "The 18-card deck that is dealt from at the start of each battle.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 6 undealt cards, set aside unseen for the battle.",
        "observable": false
      },
      {
        "key": "battle",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current battle, from 1 to 4. A value of 5 means the match is over.",
        "observable": true
      },
      {
        "key": "round_in_battle",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current round within the battle, from 1 to 6.",
        "observable": false
      },
      {
        "key": "first_player",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that is first player this battle: seat 1 (A) in battles 1 and 3, seat 2 (B) in battles 2 and 4.",
        "observable": true
      },
      {
        "key": "battle_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once someone has withdrawn from the current battle.",
        "observable": true
      },
      {
        "key": "seat1_theaters",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value: the number of theaters seat 1 controls at the end of a battle fought to the end (the workaround for comparing players).",
        "observable": false
      },
      {
        "key": "seat2_theaters",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scratch value: the number of theaters seat 2 controls at the end of a battle fought to the end.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Each player's vp is 0.",
    "battle is 1, round_in_battle is 1 and first_player is 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_battle == 1: the deck is reset to all 18 cards. Each player's hand, face_up_cards, face_down_theaters and face_down_cards are emptied, and air_strength, land_strength and sea_strength are set to 0. battle_over is set to false. Each player then draws 6 cards at random: each card is removed from deck and appended to that player's hand. The remaining 6 deck cards are moved to set_aside, unseen."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own hand and the public state: strengths, face-up cards, face-down theaters, vp, battle, round_in_battle and first_player."
    },
    {
      "action": "ask",
      "who": "the seat equal to first_player",
      "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand, or 'withdraw'",
      "effect": "Only when battle_over == false. DEPLOY: the card is removed from hand and appended to face_up_cards, and the strength attribute of the card's suit rises by its rank. IMPROVISE: the card is removed from hand, '<card> in <theater>' is appended to face_down_cards, the theater is appended to face_down_theaters, and that theater's strength rises by 2. WITHDRAW: with n = the number of cards in the withdrawer's hand, the opponent's vp rises by 2 if n >= 4, by 3 if n is 2 or 3, and by 4 if n == 1; battle_over is set to true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Only when that action was taken: everyone is told the result. A deploy names the card and its theater. An improvise names only the theater ('a face-down card was placed in X'). A withdraw states the VP awarded. The updated strengths are shown."
    },
    {
      "action": "ask",
      "who": "the seat not equal to first_player",
      "answer": "one choice: 'deploy <card>' for a card in hand, 'improvise <card> to <Air|Land|Sea>' for a card in hand, or 'withdraw'",
      "effect": "Only when battle_over == false. The effects are the same as for the first player's action."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Only when that action was taken: everyone is told the result in the same way, with face-down card identities hidden."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_battle == 6 and battle_over == false: for each theater, seat 1 controls it if seat 1's strength > seat 2's strength. On an equal sum, including 0-0, the seat equal to first_player controls it. Otherwise seat 2 controls it. seat1_theaters and seat2_theaters are set to these counts. The seat with 2 or more theaters gains 6 vp."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_battle == 6 and battle_over == false: the control of each theater and the battle winner are announced, and each player's face_down_cards are revealed to everyone for the record."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round_in_battle == 6: battle rises by 1, round_in_battle becomes 1 and first_player becomes 3 - first_player. Otherwise round_in_battle rises by 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "The game ends if battle > 4, which is after round 24. Otherwise play continues."
    }
  ],
  "ending": {
    "condition": "battle > 4",
    "rank_by": "you.vp",
    "decided_by": "After 4 battles (24 rounds), the player with more VP wins. Equal VP is a draw, in which both players share the win."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a battle starts (rounds 1, 7, 13 and 19), then all 18 cards are shuffled, 6 are dealt privately to each player's hand, and the remaining 6 go to set_aside unseen."
    },
    {
      "id": "R2",
      "text": "When a battle starts, then all strengths, face-up cards and face-down cards of both players are reset to empty or 0."
    },
    {
      "id": "R3",
      "text": "When it is battle 1 or 3, then seat 1 (A) is first player; when it is battle 2 or 4, then seat 2 (B) is first player."
    },
    {
      "id": "R4",
      "text": "When a round is played and the battle has not ended by withdrawal, then the first player takes one action, then the second player takes one action, and both see each result."
    },
    {
      "id": "R5",
      "text": "When a player deploys a card, then it leaves the hand, is shown face-up, and adds its rank (1 to 6) to that player's strength in the theater of its suit."
    },
    {
      "id": "R6",
      "text": "When a player improvises a card to a theater, then it leaves the hand, adds 2 to that player's strength in the chosen theater, and the opponent learns only the theater."
    },
    {
      "id": "R7",
      "text": "When a player withdraws holding 4 or more cards, then the opponent gains 2 VP."
    },
    {
      "id": "R8",
      "text": "When a player withdraws holding 2 or 3 cards, then the opponent gains 3 VP."
    },
    {
      "id": "R9",
      "text": "When a player withdraws holding 1 card, then the opponent gains 4 VP."
    },
    {
      "id": "R10",
      "text": "When a player holds 0 cards, then they may not withdraw."
    },
    {
      "id": "R11",
      "text": "When a player withdraws, then no further actions are taken in that battle and its remaining rounds pass with no actions."
    },
    {
      "id": "R12",
      "text": "When a later card is placed on a theater, then every card on that side still counts, covered or not."
    },
    {
      "id": "R13",
      "text": "When a battle is fought to the end (after its round 6, with no withdrawal), then for each theater the player with the higher strength sum controls it."
    },
    {
      "id": "R14",
      "text": "When the strength sums in a theater are equal, including 0-0, then the first player of that battle controls it."
    },
    {
      "id": "R15",
      "text": "When a player controls 2 or 3 theaters at the end of a battle fought to the end, then that player gains 6 VP."
    },
    {
      "id": "R16",
      "text": "When a battle is fought to the end, then all face-down cards are revealed for the record."
    },
    {
      "id": "R17",
      "text": "When round 24 is over, then the game ends and the player with more VP wins; equal VP is a draw."
    }
  ],
  "offers": [
    {
      "question": "First player's action for the round",
      "who": "the seat equal to first_player, only while battle_over is false",
      "options": "'deploy <card>' for each card in hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in hand; and 'withdraw', which is always offered because the player always holds at least 1 card on their turn."
    },
    {
      "question": "Second player's action for the round",
      "who": "the seat not equal to first_player, only while battle_over is false",
      "options": "'deploy <card>' for each card in hand; 'improvise <card> to Air', 'improvise <card> to Land' and 'improvise <card> to Sea' for each card in hand; and 'withdraw' (the player holds at least 1 card on their turn)."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed the game at 2. It is a head-to-head duel over who controls each theater, and the first-player alternation and the withdrawal payoffs are built for two sides."
    },
    {
      "what": "No talk step before actions",
      "why": "The source has no negotiation. In a two-player zero-sum duel, talk would only add words, and bluffing already happens through face-down cards and withdrawal timing."
    },
    {
      "what": "Seat 1 is Player A and seat 2 is Player B",
      "why": "The source names A and B but does not say who is who."
    },
    {
      "what": "Strength totals are public",
      "why": "Face-down cards always count 2, so each side's strength sum is known to both players. Only the identity of face-down cards is hidden."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player decides which theaters to contest and which to concede, uses improvise to bluff or to shore up a theater, and withdraws early (giving up 2 VP) when the battle is lost rather than giving up 6."
    }
  ],
  "simplifications": [
    {
      "what": "The three possible actions are offered as one choice list combining action, card and theater",
      "why": "The engine takes one choice per question. A single list keeps each action to one step."
    },
    {
      "what": "The stacking order of cards is not tracked",
      "why": "Every card counts whether or not it is covered, so the order has no effect on play."
    },
    {
      "what": "Theater control is compared through the table scratch values seat1_theaters and seat2_theaters",
      "why": "This is the engine's workaround for comparing two players' attributes."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: vp, air_strength, land_strength, sea_strength; table: battle, first_player, battle_over.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Battle start deals 6 cards to each hand and sets 6 aside, leaving the deck empty (deal is random, only counts asserted)", "rule": "R1", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"lens": {"game": {"set_aside": 6, "deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}},
              "players": {"2": {"vp": 2}}, "game": {"battle_over": true}}},

  {"name": "Battle start resets all strengths to 0 (seat 1 then withdraws)", "rule": "R2", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"air_strength": 5, "land_strength": 4, "sea_strength": 3, "face_down_theaters": ["Air"]},
                         "2": {"air_strength": 2, "land_strength": 6, "sea_strength": 1, "face_down_theaters": ["Sea", "Land"]}},
             "game": {"round_in_battle": 1, "battle": 1, "first_player": 1, "battle_over": true}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"air_strength": 0, "land_strength": 0, "sea_strength": 0},
                          "2": {"air_strength": 0, "land_strength": 0, "sea_strength": 0}},
              "lens": {"players": {"1": {"face_down_theaters": 0}, "2": {"face_down_theaters": 0}}}}},

  {"name": "After battle 1 ends, battle 2 has seat 2 as first player", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"battle": 1, "round_in_battle": 6, "first_player": 1, "battle_over": true}},
   "expect": {"game": {"battle": 2, "first_player": 2}}},

  {"name": "After battle 2 ends, battle 3 has seat 1 as first player", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"battle": 2, "round_in_battle": 6, "first_player": 2, "battle_over": true}},
   "expect": {"game": {"battle": 3, "first_player": 1}}},

  {"name": "Each player takes one action in a round", "rule": "R4", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 4", "Land 1"]}, "2": {"hand": ["Sea 5", "Air 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 4"}, {"seat": 2, "options_include": "deploy Sea 5"}],
   "expect": {"players": {"1": {"air_strength": 4, "land_strength": 0}, "2": {"sea_strength": 5, "air_strength": 0}},
              "game": {"battle_over": false},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "offered": [{"seat": 1, "option": "deploy Air 4"}, {"seat": 2, "option": "deploy Sea 5"}]}},

  {"name": "Deploying Land 6 adds 6 to land strength and leaves the hand", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 6", "Air 1"], "land_strength": 3}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Land 6"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"land_strength": 9, "air_strength": 0}, "2": {"sea_strength": 1}},
              "lens": {"players": {"1": {"hand": 1, "face_up_cards": 1}}}}},

  {"name": "Improvising Land 5 to Sea adds 2 to sea only", "rule": "R6", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 5", "Air 1"]}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "improvise Land 5 to Sea"}, {"seat": 2, "options_include": "deploy Sea 2"}],
   "expect": {"players": {"1": {"sea_strength": 2, "land_strength": 0, "air_strength": 0}, "2": {"sea_strength": 2}},
              "lens": {"players": {"1": {"hand": 1, "face_down_theaters": 1}}}}},

  {"name": "Withdrawing with 4 cards gives the opponent 2 VP", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1", "Land 2"]}, "2": {"hand": ["Sea 1", "Sea 2", "Sea 3", "Sea 4"], "vp": 3}},
             "game": {"round_in_battle": 3, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 5}}, "game": {"battle_over": true}}},

  {"name": "Second player withdrawing with 3 cards gives the opponent 3 VP", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1"]}, "2": {"hand": ["Sea 1", "Sea 2", "Sea 3"]}},
             "game": {"round_in_battle": 4, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 2"}, {"seat": 2, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 3, "air_strength": 2}, "2": {"vp": 0}}, "game": {"battle_over": true}}},

  {"name": "Withdrawing with 1 card gives the opponent 4 VP", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 3"]}, "2": {"hand": ["Sea 1"], "vp": 6}},
             "game": {"round_in_battle": 6, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 10}}, "game": {"battle_over": true}}},

  {"name": "A player holding 0 cards is not offered withdraw", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": []}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"not_offered": [{"seat": 1, "option": "withdraw"}],
              "players": {"2": {"vp": 0, "sea_strength": 1}}}},

  {"name": "After a withdrawal the rest of the battle passes with no actions and no scoring", "rule": "R11", "players": 2, "rounds": 4,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1", "Land 2"], "air_strength": 4},
                         "2": {"hand": ["Sea 5", "Sea 2", "Sea 3", "Sea 4"]}},
             "game": {"round_in_battle": 3, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0, "air_strength": 4}, "2": {"vp": 2, "sea_strength": 0}},
              "game": {"battle": 2, "first_player": 2},
              "not_offered": [{"seat": 2, "option": "deploy Sea 5"}, {"seat": 1, "option": "deploy Air 1"}]}},

  {"name": "A card placed on an occupied theater adds to what is already there", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 3", "Land 1"], "air_strength": 5}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 3"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"air_strength": 8}}}},

  {"name": "Higher strength controls each theater; seat 1 wins Air and Sea and gains 6", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Sea 1"], "air_strength": 7, "land_strength": 3, "sea_strength": 2},
                         "2": {"hand": ["Air 1"], "air_strength": 4, "land_strength": 6, "sea_strength": 1}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Sea 1"}, {"seat": 2, "options_include": "deploy Air 1"}],
   "expect": {"players": {"1": {"vp": 6}, "2": {"vp": 0}}, "game": {"battle": 2, "first_player": 2}}},

  {"name": "Ties, including 0-0, go to the first player (seat 2 in battle 2)", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 1"], "air_strength": 5, "land_strength": 5, "sea_strength": 0},
                         "2": {"hand": ["Air 2"], "air_strength": 3, "land_strength": 3, "sea_strength": 0}},
             "game": {"round_in_battle": 6, "battle": 2, "first_player": 2, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Air 2"}, {"seat": 1, "options_include": "deploy Land 1"}],
   "expect": {"players": {"1": {"vp": 0, "land_strength": 6}, "2": {"vp": 6, "air_strength": 5}},
              "game": {"battle": 3, "first_player": 1}}},

  {"name": "Controlling all 3 theaters still gains exactly 6 VP", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1"], "vp": 2},
                         "2": {"hand": ["Sea 1"], "air_strength": 2, "land_strength": 2, "sea_strength": 2, "vp": 4}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 1"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"vp": 2, "air_strength": 1}, "2": {"vp": 10, "sea_strength": 3}}}},

  {"name": "A face-down card counts 2 when the battle is fought to the end (reveal itself not observable)", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 6"], "air_strength": 3, "land_strength": 0, "sea_strength": 0},
                         "2": {"hand": ["Sea 1"], "air_strength": 4, "land_strength": 0, "sea_strength": 0}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "improvise Land 6 to Air"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"vp": 6, "air_strength": 5, "land_strength": 0}, "2": {"vp": 0, "sea_strength": 1}}}},

  {"name": "Game ends after round 24; the last battle's 6 VP decides the winner", "rule": "R17", "players": 2,
   "given": {"players": {"1": {"hand": ["Air 1"], "air_strength": 3, "land_strength": 3, "sea_strength": 0, "vp": 6},
                         "2": {"hand": ["Sea 1"], "air_strength": 0, "land_strength": 0, "sea_strength": 0, "vp": 10}},
             "game": {"round_in_battle": 6, "battle": 4, "first_player": 2, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Sea 1"}, {"seat": 1, "options_include": "deploy Air 1"}],
   "expect": {"winner": 1, "standings": {"1": 12, "2": 10}, "players": {"1": {"vp": 12}, "2": {"vp": 10}}, "game": {"battle": 5}}},

  {"name": "Equal VP after round 24 is a shared win", "rule": "R17", "players": 2,
   "given": {"players": {"1": {"vp": 8}, "2": {"vp": 8}},
             "game": {"round_in_battle": 6, "battle": 4, "first_player": 2, "battle_over": true}},
   "expect": {"winner": [1, 2], "standings": {"1": 8, "2": 8}}}
]
```

Why it was refused: scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Battle start deals 6 cards to each hand and sets 6 aside, leaving the deck empty (deal is random, only counts asserted)", "rule": "R1", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"lens": {"game": {"set_aside": 6, "deck": 0}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}},
              "players": {"2": {"vp": 2}}, "game": {"battle_over": true}}},

  {"name": "Battle start resets all strengths to 0 (seat 1 then withdraws)", "rule": "R2", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"air_strength": 5, "land_strength": 4, "sea_strength": 3, "face_down_theaters": ["Air"]},
                         "2": {"air_strength": 2, "land_strength": 6, "sea_strength": 1, "face_down_theaters": ["Sea", "Land"]}},
             "game": {"round_in_battle": 1, "battle": 1, "first_player": 1, "battle_over": true}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"air_strength": 0, "land_strength": 0, "sea_strength": 0},
                          "2": {"air_strength": 0, "land_strength": 0, "sea_strength": 0}},
              "lens": {"players": {"1": {"face_down_theaters": 0}, "2": {"face_down_theaters": 0}}}}},

  {"name": "After battle 1 ends, battle 2 has seat 2 as first player", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"battle": 1, "round_in_battle": 6, "first_player": 1, "battle_over": true}},
   "rules": [{"seat": 1, "options_include": "withdraw"}, {"seat": 2, "options_include": "withdraw"}],
   "expect": {"game": {"battle": 2, "first_player": 2}}},

  {"name": "After battle 2 ends, battle 3 has seat 1 as first player", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"battle": 2, "round_in_battle": 6, "first_player": 2, "battle_over": true}},
   "rules": [{"seat": 1, "options_include": "withdraw"}, {"seat": 2, "options_include": "withdraw"}],
   "expect": {"game": {"battle": 3, "first_player": 1}}},

  {"name": "Each player takes one action in a round", "rule": "R4", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 4", "Land 1"]}, "2": {"hand": ["Sea 5", "Air 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 4"}, {"seat": 2, "options_include": "deploy Sea 5"}],
   "expect": {"players": {"1": {"air_strength": 4, "land_strength": 0}, "2": {"sea_strength": 5, "air_strength": 0}},
              "game": {"battle_over": false},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}}},
              "offered": [{"seat": 1, "option": "deploy Air 4"}, {"seat": 2, "option": "deploy Sea 5"}]}},

  {"name": "Deploying Land 6 adds 6 to land strength and leaves the hand", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 6", "Air 1"], "land_strength": 3}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Land 6"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"land_strength": 9, "air_strength": 0}, "2": {"sea_strength": 1}},
              "lens": {"players": {"1": {"hand": 1, "face_up_cards": 1}}}}},

  {"name": "Improvising Land 5 to Sea adds 2 to sea only", "rule": "R6", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 5", "Air 1"]}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "improvise Land 5 to Sea"}, {"seat": 2, "options_include": "deploy Sea 2"}],
   "expect": {"players": {"1": {"sea_strength": 2, "land_strength": 0, "air_strength": 0}, "2": {"sea_strength": 2}},
              "lens": {"players": {"1": {"hand": 1, "face_down_theaters": 1}}}}},

  {"name": "Withdrawing with 4 cards gives the opponent 2 VP", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1", "Land 2"]}, "2": {"hand": ["Sea 1", "Sea 2", "Sea 3", "Sea 4"], "vp": 3}},
             "game": {"round_in_battle": 3, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 5}}, "game": {"battle_over": true}}},

  {"name": "Second player withdrawing with 3 cards gives the opponent 3 VP", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1"]}, "2": {"hand": ["Sea 1", "Sea 2", "Sea 3"]}},
             "game": {"round_in_battle": 4, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 2"}, {"seat": 2, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 3, "air_strength": 2}, "2": {"vp": 0}}, "game": {"battle_over": true}}},

  {"name": "Withdrawing with 1 card gives the opponent 4 VP", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 3"]}, "2": {"hand": ["Sea 1"], "vp": 6}},
             "game": {"round_in_battle": 6, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0}, "2": {"vp": 10}}, "game": {"battle_over": true}}},

  {"name": "A player holding 0 cards is not offered withdraw", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": []}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"not_offered": [{"seat": 1, "option": "withdraw"}],
              "players": {"2": {"vp": 0, "sea_strength": 1}}}},

  {"name": "After a withdrawal the rest of the battle passes with no actions and no scoring", "rule": "R11", "players": 2, "rounds": 4,
   "given": {"players": {"1": {"hand": ["Air 1", "Air 2", "Land 1", "Land 2"], "air_strength": 4},
                         "2": {"hand": ["Sea 5", "Sea 2", "Sea 3", "Sea 4"]}},
             "game": {"round_in_battle": 3, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "withdraw"}],
   "expect": {"players": {"1": {"vp": 0, "air_strength": 4}, "2": {"vp": 2, "sea_strength": 0}},
              "game": {"battle": 2, "first_player": 2},
              "not_offered": [{"seat": 2, "option": "deploy Sea 5"}, {"seat": 1, "option": "deploy Air 1"}]}},

  {"name": "A card placed on an occupied theater adds to what is already there", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 3", "Land 1"], "air_strength": 5}, "2": {"hand": ["Sea 1", "Sea 2"]}},
             "game": {"round_in_battle": 2, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 3"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"air_strength": 8}}}},

  {"name": "Higher strength controls each theater; seat 1 wins Air and Sea and gains 6", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Sea 1"], "air_strength": 7, "land_strength": 3, "sea_strength": 2},
                         "2": {"hand": ["Air 1"], "air_strength": 4, "land_strength": 6, "sea_strength": 1}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Sea 1"}, {"seat": 2, "options_include": "deploy Air 1"}],
   "expect": {"players": {"1": {"vp": 6}, "2": {"vp": 0}}, "game": {"battle": 2, "first_player": 2}}},

  {"name": "Ties, including 0-0, go to the first player (seat 2 in battle 2)", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 1"], "air_strength": 5, "land_strength": 5, "sea_strength": 0},
                         "2": {"hand": ["Air 2"], "air_strength": 3, "land_strength": 3, "sea_strength": 0}},
             "game": {"round_in_battle": 6, "battle": 2, "first_player": 2, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Air 2"}, {"seat": 1, "options_include": "deploy Land 1"}],
   "expect": {"players": {"1": {"vp": 0, "land_strength": 6}, "2": {"vp": 6, "air_strength": 5}},
              "game": {"battle": 3, "first_player": 1}}},

  {"name": "Controlling all 3 theaters still gains exactly 6 VP", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Air 1"], "vp": 2},
                         "2": {"hand": ["Sea 1"], "air_strength": 2, "land_strength": 2, "sea_strength": 2, "vp": 4}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "deploy Air 1"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"vp": 2, "air_strength": 1}, "2": {"vp": 10, "sea_strength": 3}}}},

  {"name": "A face-down card counts 2 when the battle is fought to the end (reveal itself not observable)", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"players": {"1": {"hand": ["Land 6"], "air_strength": 3, "land_strength": 0, "sea_strength": 0},
                         "2": {"hand": ["Sea 1"], "air_strength": 4, "land_strength": 0, "sea_strength": 0}},
             "game": {"round_in_battle": 6, "battle": 1, "first_player": 1, "battle_over": false}},
   "rules": [{"seat": 1, "options_include": "improvise Land 6 to Air"}, {"seat": 2, "options_include": "deploy Sea 1"}],
   "expect": {"players": {"1": {"vp": 6, "air_strength": 5, "land_strength": 0}, "2": {"vp": 0, "sea_strength": 1}}}},

  {"name": "Game ends after round 24; the last battle's 6 VP decides the winner", "rule": "R17", "players": 2,
   "given": {"players": {"1": {"hand": ["Air 1"], "air_strength": 3, "land_strength": 3, "sea_strength": 0, "vp": 6},
                         "2": {"hand": ["Sea 1"], "air_strength": 0, "land_strength": 0, "sea_strength": 0, "vp": 10}},
             "game": {"round_in_battle": 6, "battle": 4, "first_player": 2, "battle_over": false}},
   "rules": [{"seat": 2, "options_include": "deploy Sea 1"}, {"seat": 1, "options_include": "deploy Air 1"}],
   "expect": {"winner": 1, "standings": {"1": 12, "2": 10}, "players": {"1": {"vp": 12}, "2": {"vp": 10}}, "game": {"battle": 5}}},

  {"name": "Equal VP after round 24 is a shared win", "rule": "R17", "players": 2,
   "given": {"players": {"1": {"vp": 8}, "2": {"vp": 8}},
             "game": {"round_in_battle": 6, "battle": 4, "first_player": 2, "battle_over": true}},
   "rules": [{"seat": 1, "options_include": "withdraw"}, {"seat": 2, "options_include": "withdraw"}],
   "expect": {"winner": [1, 2], "standings": {"1": 8, "2": 8}}}
]
```
````
