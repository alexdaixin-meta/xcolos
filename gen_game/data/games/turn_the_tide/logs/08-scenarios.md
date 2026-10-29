# 08 scenarios

- time: 2026-10-28T06:14:56+00:00 (71.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5f14f8ec2032b756, reply sha256 12783e502e0d2613

## Sent

````
SPEC:
{
  "name": "Turn The Tide: Short Seas (revised)",
  "summary": "Over P deals of 10 hands, players play Weather cards at the same time to dodge high Tide levels and keep their lifelines. Each deal the hands pass to the left, and the highest total score wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "weather_cards_per_player": 12,
    "hand_size": 11,
    "hands_per_deal": 10,
    "tide_deck_size": 20,
    "tide_start_level": 15,
    "lifelines_per_deal": 4,
    "sunk_penalty": 1,
    "lowest_tide_bonus": 1,
    "deals_per_player": 1,
    "set_aside_cards_per_player": 1,
    "tie_break_weight": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Game score summed over the deals.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Weather cards held and not yet played.",
        "observable": false
      },
      {
        "key": "played",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Weather cards this player has played face up in the current deal.",
        "observable": false
      },
      {
        "key": "card_played",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Weather card played in the current hand.",
        "observable": false
      },
      {
        "key": "tide",
        "type": "number",
        "visible": "public",
        "initial": 15,
        "meaning": "Current Tide level.",
        "observable": true
      },
      {
        "key": "lifelines",
        "type": "number",
        "visible": "public",
        "initial": 4,
        "meaning": "Lifelines left in this deal.",
        "observable": true
      },
      {
        "key": "sunk",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Sunk status for this deal.",
        "observable": true
      },
      {
        "key": "pass_buffer",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 11 cards gathered for passing to the left at the start of a deal.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "weather_deck",
        "type": "list",
        "visible": "none",
        "initial": "cards 1 to 12*P",
        "meaning": "Shuffled Weather deck used for dealing.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The P Weather cards set aside unseen for the whole game.",
        "observable": false
      },
      {
        "key": "tide_deck",
        "type": "list",
        "visible": "none",
        "initial": "cards 1 to 20",
        "meaning": "Tide deck, refilled at the start of each deal.",
        "observable": false
      },
      {
        "key": "low_tide",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Smaller of the two Tide cards revealed this hand.",
        "observable": false
      },
      {
        "key": "high_tide",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Larger of the two Tide cards revealed this hand.",
        "observable": false
      },
      {
        "key": "deal_no",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current deal, from 1 to P.",
        "observable": true
      },
      {
        "key": "hand_no",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand within the deal, from 1 to 10.",
        "observable": false
      },
      {
        "key": "max_tide",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch value: highest Tide level among non-Sunk players.",
        "observable": false
      },
      {
        "key": "min_tide",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch value: lowest Tide level among non-Sunk players at the end of a deal.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Let P be the number of players (3 or 4).",
    "weather_deck is set to the cards 1 to 12*P, each number once.",
    "Each player draws 11 cards at random from weather_deck into hand, and each card is removed from weather_deck.",
    "The remaining P cards move from weather_deck to set_aside, which is never shown.",
    "Every score is 0, deal_no is 1 and hand_no is 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When hand_no == 1 and deal_no >= 2: each player's pass_buffer = played + hand; then each player's hand = pass_buffer of the player on their right (each player passes to the left); played = [] for everyone.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When hand_no == 1: tide_deck = cards 1 to 20; every tide = 15; every lifelines = 4; every sunk = false.",
      "judged": null
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When hand_no == 1, each player is sent their hand, along with deal_no and all public attributes.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Draw 2 cards at random from tide_deck and remove them from it; low_tide = the smaller, high_tide = the larger.",
      "judged": null
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Deal {deal_no}, hand {hand_no}: Low Tide {low_tide}, High Tide {high_tide}.'",
      "judged": null
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your hand",
      "effect": "Each player's card_played = the chosen card; it is removed from hand and appended to played. All are revealed together.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The player with the highest card_played sets tide = low_tide. The player with the second-highest card_played sets tide = high_tide. Sunk players are included. Everyone else keeps their tide.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "max_tide = the highest tide among players with sunk == false. For each player with sunk == false and tide == max_tide: if lifelines == 0 then sunk = true, else lifelines -= 1. If every player is Sunk, nothing changes.",
      "judged": null
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every card_played, tide, lifelines and sunk.",
      "judged": null
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When hand_no == 10: each player with sunk == false adds lifelines to score; each player with sunk == true subtracts 1 from score; min_tide = the lowest tide among players with sunk == false; each player with sunk == false and tide == min_tide adds 1 to score.",
      "judged": null
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "hand_no += 1; if hand_no > 10 then hand_no = 1 and deal_no += 1.",
      "judged": null
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game when deal_no > P; otherwise continue.",
      "judged": null
    }
  ],
  "ending": {
    "condition": "deal_no > P (number of players)",
    "rank_by": "you.score * 100 - you.tide",
    "decided_by": "The highest game score wins. A tie is broken by the lowest Tide level at the end of the last deal. Players still level on both share the win, which stands in for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, the Weather deck is the cards 1 to 12*P, each player is dealt 11 cards into hand, and the remaining P cards go to set_aside and are never shown."
    },
    {
      "id": "R2",
      "text": "At setup, every score is 0."
    },
    {
      "id": "R3",
      "text": "At the start of every deal, tide_deck is reset to 1 to 20, every tide is 15, every lifelines is 4 and every sunk is false."
    },
    {
      "id": "R4",
      "text": "At the start of deals 2 to P, each player's played cards plus their 1 remaining card (11 cards) pass to the player on their left as that player's hand, and played becomes empty."
    },
    {
      "id": "R5",
      "text": "Each hand, two Tide cards are drawn from tide_deck; the smaller is low_tide and the larger is high_tide."
    },
    {
      "id": "R6",
      "text": "Each hand, every player chooses one card from hand at the same time; it is removed from hand, appended to played and revealed."
    },
    {
      "id": "R7",
      "text": "The player who played the highest Weather card sets tide = low_tide, and the player who played the second highest sets tide = high_tide; this includes Sunk players."
    },
    {
      "id": "R8",
      "text": "Every non-Sunk player whose tide equals the highest tide among non-Sunk players loses 1 lifeline; a player at 0 lifelines who must lose one becomes Sunk instead."
    },
    {
      "id": "R9",
      "text": "A Sunk player stays Sunk until the next deal, still plays cards and is ignored when lifelines are lost; if all players are Sunk, no lifelines are lost."
    },
    {
      "id": "R10",
      "text": "After hand 10 of a deal, each non-Sunk player adds their lifelines (0 to 4) to score."
    },
    {
      "id": "R11",
      "text": "After hand 10 of a deal, each Sunk player subtracts 1 from score."
    },
    {
      "id": "R12",
      "text": "After hand 10 of a deal, each non-Sunk player whose tide is the lowest among non-Sunk players adds 1 to score."
    },
    {
      "id": "R13",
      "text": "A deal has 10 hands and the game ends after deal P."
    },
    {
      "id": "R14",
      "text": "The highest score wins; a tie is broken by the lowest final tide; players still level share the win."
    }
  ],
  "offers": [
    {
      "question": "Choose a Weather card to play this hand",
      "who": "every seat",
      "options": "Exactly the cards currently in that seat's hand: 11 options on hand 1 of a deal, down to 2 on hand 10."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer suggests 4, and the deck size and deal count scale with P. With fewer than 3 players, the highest and second-highest cards decide everyone's Tide. More than 4 is outside the deck design."
    },
    {
      "what": "No talk phase",
      "why": "The rules state there is no talk phase."
    },
    {
      "what": "Tie-break encoded as score*100 - tide",
      "why": "Tide is between 1 and 20, so it never outweighs a point of score, and a lower tide ranks higher."
    },
    {
      "what": "Hand passing modelled with a pass_buffer list",
      "why": "All players pass at once, so each 11-card set is gathered first and then moved to the left-hand neighbour."
    },
    {
      "what": "Count-dependent numbers written per player (weather_cards_per_player 12, deals_per_player 1, set_aside_cards_per_player 1)",
      "why": "Parameters must be plain numbers. The Weather deck is 12*P cards, there are 1*P deals and 1*P cards set aside, so each holds at 3 and at 4 players."
    }
  ],
  "simplifications": [
    {
      "what": "The source's draw becomes a shared win",
      "why": "The engine has no separate draw: players level at the top share the win."
    },
    {
      "what": "Start-of-deal and end-of-deal work is done by steps conditioned on hand_no",
      "why": "The step list is flat, so these steps run every round but act only on hand 1 or hand 10."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, tide, lifelines, sunk; table: deal_no.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup: each of 4 seats holds 11 cards, 4 cards set aside, deck empty",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"set_aside": 4, "weather_deck": 0},
        "players": {"1": {"hand": 11}, "2": {"hand": 11}, "3": {"hand": 11}, "4": {"hand": 11}}
      }
    }
  },
  {
    "name": "Setup: every score is 0 and deal 1 begins",
    "rule": "R2",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"deal_no": 1}
    }
  },
  {
    "name": "Start of deal resets sunk and lifelines (highest card never loses a lifeline whatever the random tide)",
    "rule": "R3",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [48, 47], "played": [], "lifelines": 0, "sunk": true, "tide": 3},
        "2": {"hand": [46, 45], "played": [], "lifelines": 0, "sunk": true, "tide": 3},
        "3": {"hand": [2, 3], "played": [], "lifelines": 1, "sunk": false, "tide": 20},
        "4": {"hand": [4, 5], "played": [], "lifelines": 0, "sunk": true, "tide": 20}
      },
      "game": {"hand_no": 1, "deal_no": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 48},
      {"seat": 2, "options_include": 46},
      {"seat": 3, "options_include": 2},
      {"seat": 4, "options_include": 4}
    ],
    "expect": {
      "players": {
        "1": {"lifelines": 4, "sunk": false},
        "2": {"sunk": false},
        "3": {"sunk": false},
        "4": {"sunk": false}
      }
    }
  },
  {
    "name": "Start of deal 2: hands pass on, so no seat is offered its own old cards",
    "rule": "R4",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"played": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "hand": [11]},
        "2": {"played": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "hand": [22]},
        "3": {"played": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32], "hand": [33]},
        "4": {"played": [34, 35, 36, 37, 38, 39, 40, 41, 42, 43], "hand": [44]}
      },
      "game": {"deal_no": 2, "hand_no": 1}
    },
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 10, "played": 1},
          "2": {"hand": 10, "played": 1},
          "3": {"hand": 10, "played": 1},
          "4": {"hand": 10, "played": 1}
        }
      },
      "not_offered": [
        {"seat": 1, "option": 11},
        {"seat": 1, "option": 1},
        {"seat": 2, "option": 22},
        {"seat": 2, "option": 12},
        {"seat": 3, "option": 33},
        {"seat": 4, "option": 44}
      ]
    }
  },
  {
    "name": "Two tide cards 3 and 18 drawn: low 3 to the highest card, high 18 to the second",
    "rule": "R5",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [3, 18]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "lens": {"game": {"tide_deck": 0}},
      "players": {
        "1": {"tide": 3, "lifelines": 4},
        "2": {"tide": 18, "lifelines": 3},
        "3": {"tide": 15, "lifelines": 4},
        "4": {"tide": 15, "lifelines": 4}
      }
    }
  },
  {
    "name": "The chosen card leaves the hand and joins played; only cards in hand are offered",
    "rule": "R6",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [3, 18]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 1, "played": 1},
          "2": {"hand": 1, "played": 1},
          "3": {"hand": 1, "played": 1},
          "4": {"hand": 1, "played": 1}
        }
      },
      "offered": [{"seat": 1, "option": 1}],
      "not_offered": [
        {"seat": 1, "option": 30},
        {"seat": 2, "option": 40},
        {"seat": 3, "option": 7}
      ]
    }
  },
  {
    "name": "A sunk player with the highest card still takes low tide",
    "rule": "R7",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 0, "sunk": true},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [4, 9]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 4, "lifelines": 0, "sunk": true},
        "2": {"tide": 9, "lifelines": 4},
        "3": {"tide": 15, "lifelines": 3},
        "4": {"tide": 15, "lifelines": 3}
      }
    }
  },
  {
    "name": "Highest-tide player at 0 lifelines becomes sunk",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 0, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 19]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4, "sunk": false},
        "2": {"tide": 19, "lifelines": 0, "sunk": true},
        "3": {"tide": 15, "lifelines": 4, "sunk": false},
        "4": {"tide": 15, "lifelines": 4, "sunk": false}
      }
    }
  },
  {
    "name": "All players level at the highest tide each lose a lifeline",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 2, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 1, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 10]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4},
        "2": {"tide": 10, "lifelines": 4},
        "3": {"tide": 15, "lifelines": 1, "sunk": false},
        "4": {"tide": 15, "lifelines": 0, "sunk": false}
      }
    }
  },
  {
    "name": "A sunk player with the highest tide is ignored; the non-sunk maximum loses lifelines",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 1, "sunk": true},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 19]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4},
        "2": {"tide": 19, "lifelines": 1, "sunk": true},
        "3": {"tide": 15, "lifelines": 3, "sunk": false},
        "4": {"tide": 15, "lifelines": 3, "sunk": false}
      }
    }
  },
  {
    "name": "When every player is sunk, no lifelines change",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 2, "sunk": true}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [5, 6]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 5, "lifelines": 2, "sunk": true},
        "2": {"tide": 6, "lifelines": 2, "sunk": true},
        "3": {"tide": 15, "lifelines": 2, "sunk": true},
        "4": {"tide": 15, "lifelines": 2, "sunk": true}
      }
    }
  },
  {
    "name": "After hand 10, a non-sunk player adds remaining lifelines to score",
    "rule": "R10",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"2": {"score": 4}, "3": {"score": 2}}
    }
  },
  {
    "name": "After hand 10, a sunk player loses 1 point",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"4": {"score": -1}}
    }
  },
  {
    "name": "After hand 10, the lowest non-sunk tide gains a bonus point",
    "rule": "R12",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"1": {"tide": 1, "score": 3}, "2": {"score": 4}}
    }
  },
  {
    "name": "Hand 10 ends the deal and deal_no moves to 2",
    "rule": "R13",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "game": {"deal_no": 2}
    }
  },
  {
    "name": "Game ends after hand 10 of deal P (3 players) and the highest score wins",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [10, 5], "tide": 15, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 499, "2": 398, "3": 285},
      "players": {"1": {"score": 5}, "2": {"score": 4}, "3": {"score": 3}}
    }
  },
  {
    "name": "Tied score broken by lower final tide",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 1},
        "3": {"hand": [10, 5], "tide": 15, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 499, "2": 498, "3": 285},
      "players": {"1": {"score": 5, "tide": 1}, "2": {"score": 5, "tide": 2}}
    }
  },
  {
    "name": "Players level on score and tide share the win",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [10, 5], "tide": 1, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 499, "2": 298, "3": 499},
      "players": {"1": {"score": 5}, "2": {"score": 3, "lifelines": 3}, "3": {"score": 5}}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Setup: 4 cards set aside and the weather deck is empty (still true after one hand)",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "played": []},
        "2": {"hand": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "played": []},
        "3": {"hand": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33], "played": []},
        "4": {"hand": [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44], "played": []}
      },
      "game": {"hand_no": 1, "deal_no": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 12},
      {"seat": 3, "options_include": 23},
      {"seat": 4, "options_include": 34}
    ],
    "expect": {
      "lens": {
        "game": {"set_aside": 4, "weather_deck": 0},
        "players": {"1": {"hand": 10}, "2": {"hand": 10}, "3": {"hand": 10}, "4": {"hand": 10}}
      }
    }
  },
  {
    "name": "Setup: every score is 0 and still 0 after the first hand of deal 1",
    "rule": "R2",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "played": []},
        "2": {"hand": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "played": []},
        "3": {"hand": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33], "played": []},
        "4": {"hand": [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44], "played": []}
      },
      "game": {"hand_no": 1, "deal_no": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 12},
      {"seat": 3, "options_include": 23},
      {"seat": 4, "options_include": 34}
    ],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"deal_no": 1}
    }
  },
  {
    "name": "Start of deal resets sunk and lifelines (highest card never loses a lifeline whatever the random tide)",
    "rule": "R3",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [48, 47], "played": [], "lifelines": 0, "sunk": true, "tide": 3},
        "2": {"hand": [46, 45], "played": [], "lifelines": 0, "sunk": true, "tide": 3},
        "3": {"hand": [2, 3], "played": [], "lifelines": 1, "sunk": false, "tide": 20},
        "4": {"hand": [4, 5], "played": [], "lifelines": 0, "sunk": true, "tide": 20}
      },
      "game": {"hand_no": 1, "deal_no": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 48},
      {"seat": 2, "options_include": 46},
      {"seat": 3, "options_include": 2},
      {"seat": 4, "options_include": 4}
    ],
    "expect": {
      "players": {
        "1": {"lifelines": 4, "sunk": false},
        "2": {"sunk": false},
        "3": {"sunk": false},
        "4": {"sunk": false}
      }
    }
  },
  {
    "name": "Start of deal 2: hands pass to the left, so each seat plays a card from its right-hand neighbour's old set",
    "rule": "R4",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"played": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "hand": [11]},
        "2": {"played": [12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "hand": [22]},
        "3": {"played": [23, 24, 25, 26, 27, 28, 29, 30, 31, 32], "hand": [33]},
        "4": {"played": [34, 35, 36, 37, 38, 39, 40, 41, 42, 43], "hand": [44]}
      },
      "game": {"deal_no": 2, "hand_no": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 34},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": 12},
      {"seat": 4, "options_include": 23}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 10, "played": 1},
          "2": {"hand": 10, "played": 1},
          "3": {"hand": 10, "played": 1},
          "4": {"hand": 10, "played": 1}
        }
      },
      "not_offered": [
        {"seat": 1, "option": 11},
        {"seat": 1, "option": 1},
        {"seat": 2, "option": 22},
        {"seat": 2, "option": 12},
        {"seat": 3, "option": 33},
        {"seat": 4, "option": 44}
      ]
    }
  },
  {
    "name": "Two tide cards 3 and 18 drawn: low 3 to the highest card, high 18 to the second",
    "rule": "R5",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [3, 18]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "lens": {"game": {"tide_deck": 0}},
      "players": {
        "1": {"tide": 3, "lifelines": 4},
        "2": {"tide": 18, "lifelines": 3},
        "3": {"tide": 15, "lifelines": 4},
        "4": {"tide": 15, "lifelines": 4}
      }
    }
  },
  {
    "name": "The chosen card leaves the hand and joins played; only cards in hand are offered",
    "rule": "R6",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [3, 18]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"hand": 1, "played": 1},
          "2": {"hand": 1, "played": 1},
          "3": {"hand": 1, "played": 1},
          "4": {"hand": 1, "played": 1}
        }
      },
      "offered": [{"seat": 1, "option": 1}],
      "not_offered": [
        {"seat": 1, "option": 30},
        {"seat": 2, "option": 40},
        {"seat": 3, "option": 7}
      ]
    }
  },
  {
    "name": "A sunk player with the highest card still takes low tide",
    "rule": "R7",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 0, "sunk": true},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [4, 9]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 4, "lifelines": 0, "sunk": true},
        "2": {"tide": 9, "lifelines": 4},
        "3": {"tide": 15, "lifelines": 3},
        "4": {"tide": 15, "lifelines": 3}
      }
    }
  },
  {
    "name": "Highest-tide player at 0 lifelines becomes sunk",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 0, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 19]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4, "sunk": false},
        "2": {"tide": 19, "lifelines": 0, "sunk": true},
        "3": {"tide": 15, "lifelines": 4, "sunk": false},
        "4": {"tide": 15, "lifelines": 4, "sunk": false}
      }
    }
  },
  {
    "name": "All players level at the highest tide each lose a lifeline",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 2, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 1, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 10]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4},
        "2": {"tide": 10, "lifelines": 4},
        "3": {"tide": 15, "lifelines": 1, "sunk": false},
        "4": {"tide": 15, "lifelines": 0, "sunk": false}
      }
    }
  },
  {
    "name": "A sunk player with the highest tide is ignored; the non-sunk maximum loses lifelines",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 1, "sunk": true},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 4, "sunk": false},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 4, "sunk": false}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [2, 19]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 2, "lifelines": 4},
        "2": {"tide": 19, "lifelines": 1, "sunk": true},
        "3": {"tide": 15, "lifelines": 3, "sunk": false},
        "4": {"tide": 15, "lifelines": 3, "sunk": false}
      }
    }
  },
  {
    "name": "When every player is sunk, no lifelines change",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "2": {"hand": [30, 2], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "3": {"hand": [5, 6], "played": [], "tide": 15, "lifelines": 2, "sunk": true},
        "4": {"hand": [7, 8], "played": [], "tide": 15, "lifelines": 2, "sunk": true}
      },
      "game": {"hand_no": 2, "deal_no": 1, "tide_deck": [5, 6]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"tide": 5, "lifelines": 2, "sunk": true},
        "2": {"tide": 6, "lifelines": 2, "sunk": true},
        "3": {"tide": 15, "lifelines": 2, "sunk": true},
        "4": {"tide": 15, "lifelines": 2, "sunk": true}
      }
    }
  },
  {
    "name": "After hand 10, a non-sunk player adds remaining lifelines to score",
    "rule": "R10",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"2": {"score": 4}, "3": {"score": 2}}
    }
  },
  {
    "name": "After hand 10, a sunk player loses 1 point",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"4": {"score": -1}}
    }
  },
  {
    "name": "After hand 10, the lowest non-sunk tide gains a bonus point",
    "rule": "R12",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "players": {"1": {"tide": 1, "score": 3}, "2": {"score": 4}}
    }
  },
  {
    "name": "Hand 10 ends the deal and deal_no moves to 2",
    "rule": "R13",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [40, 1], "tide": 15, "lifelines": 2, "sunk": false, "score": 0},
        "2": {"hand": [30, 2], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [5, 6], "tide": 10, "lifelines": 3, "sunk": false, "score": 0},
        "4": {"hand": [7, 8], "tide": 20, "lifelines": 0, "sunk": true, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 1, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 5},
      {"seat": 4, "options_include": 7}
    ],
    "expect": {
      "game": {"deal_no": 2}
    }
  },
  {
    "name": "Game ends after hand 10 of deal P (3 players) and the highest score wins",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [10, 5], "tide": 15, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 499, "2": 398, "3": 285},
      "players": {"1": {"score": 5}, "2": {"score": 4}, "3": {"score": 3}}
    }
  },
  {
    "name": "Tied score broken by lower final tide",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 1},
        "3": {"hand": [10, 5], "tide": 15, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 499, "2": 498, "3": 285},
      "players": {"1": {"score": 5, "tide": 1}, "2": {"score": 5, "tide": 2}}
    }
  },
  {
    "name": "Players level on score and tide share the win",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [30, 3], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "2": {"hand": [20, 4], "tide": 15, "lifelines": 4, "sunk": false, "score": 0},
        "3": {"hand": [10, 5], "tide": 1, "lifelines": 4, "sunk": false, "score": 0}
      },
      "game": {"hand_no": 10, "deal_no": 3, "tide_deck": [1, 2]}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 2, "options_include": 20},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 499, "2": 298, "3": 499},
      "players": {"1": {"score": 5}, "2": {"score": 3, "lifelines": 3}, "3": {"score": 5}}
    }
  }
]
```
````
