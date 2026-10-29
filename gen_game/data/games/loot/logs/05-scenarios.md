# 05 scenarios

- time: 2026-10-28T05:06:16+00:00 (41.8s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 6a76aff691765842, reply sha256 b0e0a41baf0d8d3d

## Sent

````
SPEC:
{
  "name": "Loot: Sealed Raids",
  "summary": "Each round one seat sails a hidden-value merchant ship and every seat secretly commits crew from a fixed budget of 30 to defend it or raid it, with one-shot Captain and Admiral trumps. The most gold after 3 x N rounds wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "min_players": 3,
    "max_players": 5,
    "suggested_players": 4,
    "starting_crew": 30,
    "starting_gold": 0,
    "ship_value_small": 3,
    "ship_value_medium": 5,
    "ship_value_large": 7,
    "ships_per_player": 3,
    "captains_per_player": 1,
    "admirals_per_player": 1,
    "captain_bonus": 6,
    "rounds_per_player": 3,
    "min_commit": 0,
    "unspent_crew_value": 0
  },
  "attributes": {
    "player": [
      {
        "key": "crew",
        "type": "number",
        "visible": "ally",
        "initial": 30,
        "meaning": "Remaining crew. Only the owner of the attribute and the engine know it.",
        "observable": false
      },
      {
        "key": "gold",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Gold won from ships. This is the score.",
        "observable": true
      },
      {
        "key": "ships",
        "type": "list",
        "visible": "public",
        "initial": [
          3,
          5,
          7
        ],
        "meaning": "Values of this player's unsailed ships. A value is removed only at bookkeeping, after it has been revealed.",
        "observable": true
      },
      {
        "key": "captain_used",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this player's Captain has been used.",
        "observable": true
      },
      {
        "key": "admiral_used",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this player's Admiral has been used.",
        "observable": true
      },
      {
        "key": "committed",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Crew this player committed this round.",
        "observable": false
      },
      {
        "key": "trump_declared",
        "type": "bool",
        "visible": "ally",
        "initial": false,
        "meaning": "Whether this player validly declared a trump this round (an Admiral for the owner, a Captain for a non-owner).",
        "observable": false
      },
      {
        "key": "strength",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's strength: committed crew, plus 6 for an attacker who declared the Captain. For the owner it is the defense.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number.",
        "observable": true
      },
      {
        "key": "owner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this round's owner: ((round - 1) mod N) + 1.",
        "observable": true
      },
      {
        "key": "current_ship",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Value of the ship sailed this round. It stays hidden until the announcement.",
        "observable": false
      },
      {
        "key": "last_ship_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value of the ship revealed at the end of the round.",
        "observable": true
      },
      {
        "key": "last_taker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that got this round's ship.",
        "observable": true
      },
      {
        "key": "defense",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch value: the owner's defense this round.",
        "observable": false
      },
      {
        "key": "top_attack",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch value: the highest attacker strength this round.",
        "observable": false
      },
      {
        "key": "top_count",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch value: how many attackers have the highest strength.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat the players 1 to N.",
    "Every player gets 30 crew (private), 0 gold, unsailed ships worth 3, 5 and 7 gold, an unused Captain and an unused Admiral.",
    "Set round to 0. The game lasts 3 x N rounds."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; owner = ((round - 1) mod N) + 1; for every player, set committed = 0, trump_declared = false and strength = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Round {round}: Seat {owner} is the owner. Unsailed ships: {owner.ships}.'"
    },
    {
      "action": "update",
      "who": "seat owner",
      "answer": null,
      "effect": "When the length of owner.ships = 1, set current_ship = the only value in owner.ships (it sails automatically)."
    },
    {
      "action": "ask",
      "who": "seat owner",
      "answer": "one value from owner.ships",
      "effect": "When the length of owner.ships > 1, set current_ship = the chosen value. The choice is private."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "Every message is shown to everyone after all are in: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk binds no one."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "A whole number of crew from 0 to your crew. Also a trump choice: the owner chooses 'none' or 'admiral', with 'admiral' offered only if admiral_used is false; a non-owner chooses 'none' or 'captain', with 'captain' offered only if captain_used is false.",
      "effect": "committed = the amount, or 0 if the amount is invalid. trump_declared = true only for a valid declaration; an invalid declaration is ignored."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "crew -= committed. strength = committed + (6 if the seat is not the owner and trump_declared, else 0). defense = owner.strength."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "top_attack = the highest strength among non-owners; top_count = the number of non-owners whose strength = top_attack. If owner.trump_declared, last_taker = owner. Otherwise, if top_attack > defense and top_count = 1, last_taker = the non-owner whose strength = top_attack. Otherwise last_taker = owner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The player in seat last_taker adds current_ship to gold. last_ship_value = current_ship."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Remove current_ship from owner.ships. If owner.trump_declared, set owner.admiral_used = true. For each non-owner with trump_declared, set captain_used = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'The ship was worth {last_ship_value}. Seat {last_taker} got it.' Then list who used a Captain or Admiral this round. No crew amounts are revealed."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= 3 * N; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round >= 3 * N",
    "rank_by": "you.gold",
    "decided_by": "Each player's standing is their gold. The player with the most gold wins. Players tied for the most gold share the result, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has 30 crew, 0 gold, ships [3, 5, 7], an unused Captain and an unused Admiral."
    },
    {
      "id": "R2",
      "text": "When it is round r, then the owner is seat ((r - 1) mod N) + 1, so with 4 players round 5 is owned by seat 1."
    },
    {
      "id": "R3",
      "text": "When the game has N players, then it lasts 3 x N rounds (12 with 4 players) and each seat is owner exactly 3 times."
    },
    {
      "id": "R4",
      "text": "When a round begins, then the owner and the owner's unsailed ships are announced."
    },
    {
      "id": "R5",
      "text": "When the owner has more than one unsailed ship, then the owner privately chooses which one sails."
    },
    {
      "id": "R6",
      "text": "When the owner has exactly one unsailed ship, then it sails automatically."
    },
    {
      "id": "R7",
      "text": "When a ship sails, then its value is not revealed until the end-of-round announcement."
    },
    {
      "id": "R8",
      "text": "When the talk step runs, then every player writes one message at the same time and all messages are shown to everyone only after all are in."
    },
    {
      "id": "R9",
      "text": "When crew is committed, then every player chooses at the same time a whole number from 0 to their remaining crew."
    },
    {
      "id": "R10",
      "text": "When a committed amount is invalid, then it is set to 0."
    },
    {
      "id": "R11",
      "text": "When a player commits crew, then it is subtracted from their crew whatever the result, so 30 crew minus a commit of 10 leaves 20."
    },
    {
      "id": "R12",
      "text": "When a non-owner declares an unused Captain, then their strength is their committed crew + 6."
    },
    {
      "id": "R13",
      "text": "When the owner declares an unused Admiral, then the owner keeps the ship regardless of any attack."
    },
    {
      "id": "R14",
      "text": "When a trump declaration is invalid (already used, or the wrong role), then it is ignored."
    },
    {
      "id": "R15",
      "text": "When no Admiral is declared and one attacker's strength is strictly greater than the defense and strictly greater than every other attacker's, then that attacker gets the ship (attack 8 against defense 7 wins)."
    },
    {
      "id": "R16",
      "text": "When the highest attacker strength equals the defense, then the owner keeps the ship (attack 7 against defense 7 loses)."
    },
    {
      "id": "R17",
      "text": "When two or more attackers tie for the highest strength, then the owner keeps the ship, even if that strength beats the defense."
    },
    {
      "id": "R18",
      "text": "When a player gets a ship, then they add its value to their gold."
    },
    {
      "id": "R19",
      "text": "When the round ends, then the sailed ship is removed from the owner's unsailed ships and declared trumps are marked used."
    },
    {
      "id": "R20",
      "text": "When the round ends, then the ship's value, its taker and who used a Captain or Admiral are announced, but no crew amounts are."
    },
    {
      "id": "R21",
      "text": "When the game ends, then unspent crew is worth 0 and the player with the most gold wins; players tied for the most gold share the result, standing for the source's draw."
    }
  ],
  "offers": [
    {
      "question": "Sail: which ship to sail",
      "who": "the owner, only when they have 2 or more unsailed ships",
      "options": "each value in owner.ships"
    },
    {
      "question": "Talk message",
      "who": "all seats",
      "options": "a short free-text message"
    },
    {
      "question": "Commit: crew amount",
      "who": "all seats",
      "options": "a whole number from 0 to that seat's crew"
    },
    {
      "question": "Commit: trump",
      "who": "all seats",
      "options": "The owner with an unused Admiral: none, admiral. The owner with a used Admiral: none. A non-owner with an unused Captain: none, captain. A non-owner with a used Captain: none."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggests 4, and the minimum of 3 keeps it from being a plain duel. Two or more raiders are needed for ties between attackers and for a raider to free-ride while others overbid. Beyond 5 players each seat is owner rarely and the ties between attackers dominate."
    },
    {
      "what": "Keep the simultaneous talk poll",
      "why": "The source requires it. Players have opposing interests over who raids which ship, so a non-binding message can bluff, threaten or deter, and following someone else's proposal can cost a player."
    },
    {
      "what": "The unsailed-ships list is public and a value is removed only at bookkeeping",
      "why": "The source announces the owner's unsailed ships each round. Removing the value at sail time would leak the hidden value before the announcement."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player rations 30 crew over 3 x N rounds. They infer which ship sailed from the remaining list, time the one-shot Admiral and Captain, and use talk to bluff or provoke ties between rival raiders."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most gold is a shared win instead of a draw",
      "why": "The engine ranks by an arithmetic expression and players level at the top share the win. This is the closest equivalent to 'the game is a draw'."
    },
    {
      "what": "The commit poll offers only valid amounts and valid trumps",
      "why": "The engine constrains answers to the offered range, so the source's 'invalid amounts are set to 0' and 'invalid trumps are ignored' rarely trigger. Both are kept as rules anyway."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: gold, ships, captain_used, admiral_used; table: round, owner, last_ship_value, last_taker.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup: 30 crew, 0 gold, ships [3,5,7], Captain and Admiral unused", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"players": {
     "1": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "2": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "3": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "4": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false}},
     "game": {"round": 0},
     "lens": {"players": {"1": {"ships": 3}, "2": {"ships": 3}, "3": {"ships": 3}, "4": {"ships": 3}}}}},

  {"name": "With 4 players round 5 is owned by seat 1", "rule": "R2", "players": 4, "rounds": 1,
   "given": {"game": {"round": 4}},
   "expect": {"game": {"round": 5, "owner": 1}}},

  {"name": "Game with 4 players ends after round 12; owner seat 4 keeps its last ship and wins", "rule": "R3", "players": 4,
   "given": {"game": {"round": 11},
             "players": {"1": {"gold": 10}, "2": {"gold": 0}, "3": {"gold": 0}, "4": {"gold": 5, "ships": [7]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0}],
   "expect": {"winner": 4, "standings": {"1": 10, "2": 0, "3": 0, "4": 12},
              "game": {"round": 12, "owner": 4, "last_ship_value": 7, "last_taker": 4},
              "players": {"4": {"gold": 12, "ships": []}}}},

  {"name": "Round 1 begins with seat 1 as owner, offered its unsailed ships", "rule": "R4", "players": 3, "rounds": 1,
   "expect": {"game": {"round": 1, "owner": 1},
              "offered": [{"seat": 1, "option": 3}, {"seat": 1, "option": 5}, {"seat": 1, "option": 7}]}},

  {"name": "Owner with several ships chooses the 7 to sail", "rule": "R5", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [3, 5], "gold": 7}},
              "game": {"last_ship_value": 7, "last_taker": 1}}},

  {"name": "Owner with one ship left sails it automatically", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ships": [5]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [], "gold": 5}},
              "game": {"last_ship_value": 5, "last_taker": 1},
              "lens": {"players": {"1": {"ships": 0}}}}},

  {"name": "Sailed ship value is revealed at the end of the round", "rule": "R7", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"last_ship_value": 3, "last_taker": 1}, "players": {"1": {"ships": [5, 7]}}}},

  {"name": "Talk step runs and the round completes", "rule": "R8", "players": 3, "rounds": 1,
   "expect": {"game": {"round": 1, "owner": 1}}},

  {"name": "Seat with 10 crew may commit up to 10 but not 11, and wins the ship alone", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"crew": 10}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 5}}, "game": {"last_taker": 2, "last_ship_value": 5},
              "offered": [{"seat": 2, "option": 10}],
              "not_offered": [{"seat": 2, "option": 11}]}},

  {"name": "Committed crew is spent: seat 2 spends all 10, then can commit only 0 as owner and loses its 7", "rule": "R11", "players": 3, "rounds": 2,
   "given": {"players": {"2": {"crew": 10}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0, "times": 2},
             {"seat": 2, "options_include": 10}, {"seat": 2, "options_include": 7},
             {"seat": 3, "options_include": 0}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"2": {"gold": 5, "ships": [3, 5]}, "3": {"gold": 7}},
              "game": {"round": 2, "owner": 2, "last_ship_value": 7, "last_taker": 3}}},

  {"name": "Captain adds 6: commit 2 + Captain beats defense 7", "rule": "R12", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "captain"},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 7, "captain_used": true}, "1": {"gold": 0}},
              "game": {"last_taker": 2, "last_ship_value": 7}}},

  {"name": "Admiral keeps the ship against a 20-crew attack", "rule": "R13", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "admiral"},
             {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 7, "admiral_used": true}, "2": {"gold": 0}},
              "game": {"last_taker": 1}}},

  {"name": "Wrong-role and used trumps are not offered", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"3": {"captain_used": true}}},
   "expect": {"players": {"3": {"captain_used": true}},
              "offered": [{"seat": 2, "option": "captain"}, {"seat": 1, "option": "admiral"}],
              "not_offered": [{"seat": 1, "option": "captain"}, {"seat": 2, "option": "admiral"},
                              {"seat": 3, "option": "admiral"}, {"seat": 3, "option": "captain"}]}},

  {"name": "Attack 8 beats defense 7 and the other attacker's 5", "rule": "R15", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 8}, {"seat": 3, "options_include": 5}],
   "expect": {"players": {"2": {"gold": 5}, "1": {"gold": 0}, "3": {"gold": 0}},
              "game": {"last_taker": 2, "last_ship_value": 5}}},

  {"name": "Attack 7 against defense 7: owner keeps the ship", "rule": "R16", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 3}, "2": {"gold": 0}}, "game": {"last_taker": 1, "last_ship_value": 3}}},

  {"name": "Two attackers tied at 10 against defense 0: owner keeps the ship", "rule": "R17", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 10}],
   "expect": {"players": {"1": {"gold": 7}, "2": {"gold": 0}, "3": {"gold": 0}}, "game": {"last_taker": 1}}},

  {"name": "Taker adds the ship value to gold: 4 + 3 = 7", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"gold": 4}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 7}}, "game": {"last_taker": 2, "last_ship_value": 3}}},

  {"name": "Sailed ship removed and declared trumps marked used", "rule": "R19", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "admiral"},
             {"seat": 2, "options_include": 0}, {"seat": 2, "options_include": "captain"},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [3, 7], "admiral_used": true, "captain_used": false, "gold": 5},
                          "2": {"captain_used": true, "admiral_used": false},
                          "3": {"captain_used": false, "admiral_used": false}},
              "game": {"last_taker": 1, "last_ship_value": 5}}},

  {"name": "End of round reveals ship value and taker", "rule": "R20", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 3}],
   "expect": {"game": {"last_ship_value": 7, "last_taker": 3}, "players": {"3": {"gold": 7}}}},

  {"name": "Final round ties seats 2 and 3 at 13 gold: shared win, unspent crew worth 0", "rule": "R21", "players": 3,
   "given": {"game": {"round": 8},
             "players": {"1": {"gold": 10, "crew": 30}, "2": {"gold": 13}, "3": {"gold": 10, "ships": [3]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [2, 3], "standings": {"1": 10, "2": 13, "3": 13},
              "game": {"round": 9, "owner": 3, "last_taker": 3, "last_ship_value": 3}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Setup: 30 crew, 0 gold, ships [3,5,7], Captain and Admiral unused", "rule": "R1", "players": 4, "rounds": 0,
   "rules": [],
   "expect": {"players": {
     "1": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "2": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "3": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false},
     "4": {"gold": 0, "ships": [3, 5, 7], "captain_used": false, "admiral_used": false}},
     "game": {"round": 0},
     "lens": {"players": {"1": {"ships": 3}, "2": {"ships": 3}, "3": {"ships": 3}, "4": {"ships": 3}}}}},

  {"name": "With 4 players round 5 is owned by seat 1", "rule": "R2", "players": 4, "rounds": 1,
   "given": {"game": {"round": 4}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0}],
   "expect": {"game": {"round": 5, "owner": 1, "last_ship_value": 3, "last_taker": 1}}},

  {"name": "Game with 4 players ends after round 12; owner seat 4 keeps its last ship and wins", "rule": "R3", "players": 4,
   "given": {"game": {"round": 11},
             "players": {"1": {"gold": 10}, "2": {"gold": 0}, "3": {"gold": 0}, "4": {"gold": 5, "ships": [7]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0},
             {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0}],
   "expect": {"winner": 4, "standings": {"1": 10, "2": 0, "3": 0, "4": 12},
              "game": {"round": 12, "owner": 4, "last_ship_value": 7, "last_taker": 4},
              "players": {"4": {"gold": 12, "ships": []}}}},

  {"name": "Round 1 begins with seat 1 as owner, offered its unsailed ships", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"round": 1, "owner": 1},
              "offered": [{"seat": 1, "option": 3}, {"seat": 1, "option": 5}, {"seat": 1, "option": 7}]}},

  {"name": "Owner with several ships chooses the 7 to sail", "rule": "R5", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [3, 5], "gold": 7}},
              "game": {"last_ship_value": 7, "last_taker": 1}}},

  {"name": "Owner with one ship left sails it automatically", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ships": [5]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [], "gold": 5}},
              "game": {"last_ship_value": 5, "last_taker": 1},
              "lens": {"players": {"1": {"ships": 0}}}}},

  {"name": "Sailed ship value is revealed at the end of the round", "rule": "R7", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"last_ship_value": 3, "last_taker": 1}, "players": {"1": {"ships": [5, 7]}}}},

  {"name": "Talk step runs and the round completes", "rule": "R8", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"round": 1, "owner": 1, "last_ship_value": 3, "last_taker": 1}}},

  {"name": "Seat with 10 crew may commit up to 10 but not 11, and wins the ship alone", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"crew": 10}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 5}}, "game": {"last_taker": 2, "last_ship_value": 5},
              "offered": [{"seat": 2, "option": 10}],
              "not_offered": [{"seat": 2, "option": 11}]}},

  {"name": "Committed crew is spent: seat 2 spends all 10, then can commit only 0 as owner and loses its 7", "rule": "R11", "players": 3, "rounds": 2,
   "given": {"players": {"2": {"crew": 10}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0, "times": 2},
             {"seat": 2, "options_include": 10}, {"seat": 2, "options_include": 7},
             {"seat": 3, "options_include": 0}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"2": {"gold": 5, "ships": [3, 5]}, "3": {"gold": 7}},
              "game": {"round": 2, "owner": 2, "last_ship_value": 7, "last_taker": 3}}},

  {"name": "Captain adds 6: commit 2 + Captain beats defense 7", "rule": "R12", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "captain"},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 7, "captain_used": true}, "1": {"gold": 0}},
              "game": {"last_taker": 2, "last_ship_value": 7}}},

  {"name": "Admiral keeps the ship against a 20-crew attack", "rule": "R13", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "admiral"},
             {"seat": 2, "options_include": 20}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 7, "admiral_used": true}, "2": {"gold": 0}},
              "game": {"last_taker": 1}}},

  {"name": "Wrong-role and used trumps are not offered", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"3": {"captain_used": true}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"3": {"captain_used": true}},
              "offered": [{"seat": 2, "option": "captain"}, {"seat": 1, "option": "admiral"}],
              "not_offered": [{"seat": 1, "option": "captain"}, {"seat": 2, "option": "admiral"},
                              {"seat": 3, "option": "admiral"}, {"seat": 3, "option": "captain"}]}},

  {"name": "Attack 8 beats defense 7 and the other attacker's 5", "rule": "R15", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 8}, {"seat": 3, "options_include": 5}],
   "expect": {"players": {"2": {"gold": 5}, "1": {"gold": 0}, "3": {"gold": 0}},
              "game": {"last_taker": 2, "last_ship_value": 5}}},

  {"name": "Attack 7 against defense 7: owner keeps the ship", "rule": "R16", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 7},
             {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"gold": 3}, "2": {"gold": 0}}, "game": {"last_taker": 1, "last_ship_value": 3}}},

  {"name": "Two attackers tied at 10 against defense 0: owner keeps the ship", "rule": "R17", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 10}],
   "expect": {"players": {"1": {"gold": 7}, "2": {"gold": 0}, "3": {"gold": 0}}, "game": {"last_taker": 1}}},

  {"name": "Taker adds the ship value to gold: 4 + 3 = 7", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"gold": 4}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"2": {"gold": 7}}, "game": {"last_taker": 2, "last_ship_value": 3}}},

  {"name": "Sailed ship removed and declared trumps marked used", "rule": "R19", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "admiral"},
             {"seat": 2, "options_include": 0}, {"seat": 2, "options_include": "captain"},
             {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"ships": [3, 7], "admiral_used": true, "captain_used": false, "gold": 5},
                          "2": {"captain_used": true, "admiral_used": false},
                          "3": {"captain_used": false, "admiral_used": false}},
              "game": {"last_taker": 1, "last_ship_value": 5}}},

  {"name": "End of round reveals ship value and taker", "rule": "R20", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 3}],
   "expect": {"game": {"last_ship_value": 7, "last_taker": 3}, "players": {"3": {"gold": 7}}}},

  {"name": "Final round ties seats 2 and 3 at 13 gold: shared win, unspent crew worth 0", "rule": "R21", "players": 3,
   "given": {"game": {"round": 8},
             "players": {"1": {"gold": 10, "crew": 30}, "2": {"gold": 13}, "3": {"gold": 10, "ships": [3]}}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [2, 3], "standings": {"1": 10, "2": 13, "3": 13},
              "game": {"round": 9, "owner": 3, "last_taker": 3, "last_ship_value": 3}}}
]
```
````
