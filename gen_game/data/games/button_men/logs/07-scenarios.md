# 07 scenarios

- time: 2026-10-28T05:18:23+00:00 (143.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 45f74627b45243f0, reply sha256 ac75b42bfcefa31b

## Sent

````
SPEC:
{
  "name": "Loaded Button Men",
  "summary": "Two players secretly load four dice (d4, d6, d8, d12) to total 16, then take turns capturing each other's dice with power or skill attacks over two 20-turn legs; the higher total of captured sizes wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "d4_size": 4,
    "d6_size": 6,
    "d8_size": 8,
    "d12_size": 12,
    "dice_per_player": 4,
    "load_total": 16,
    "default_d4": 2,
    "default_d6": 3,
    "default_d8": 4,
    "default_d12": 7,
    "legs": 2,
    "turns_per_leg": 20,
    "leg1_first_turn": 1,
    "leg1_last_turn": 20,
    "leg2_first_turn": 21,
    "leg2_last_turn": 40,
    "consecutive_passes_to_end_leg": 2,
    "skill_attack_dice": 2,
    "power_attack_dice": 1,
    "starting_score": 0,
    "min_die_value": 1
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total sizes of all dice this player has captured across both legs",
        "observable": true
      },
      {
        "key": "is_first",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True for the player chosen at random to be First",
        "observable": true
      },
      {
        "key": "in_play",
        "type": "list",
        "visible": "public",
        "initial": [
          4,
          6,
          8,
          12
        ],
        "meaning": "Sizes of this player's dice still in play this leg",
        "observable": true
      },
      {
        "key": "d4_value",
        "type": "number",
        "visible": "ally",
        "initial": 2,
        "meaning": "Current value of this player's d4 (1-4)",
        "observable": false
      },
      {
        "key": "d6_value",
        "type": "number",
        "visible": "ally",
        "initial": 3,
        "meaning": "Current value of this player's d6 (1-6)",
        "observable": false
      },
      {
        "key": "d8_value",
        "type": "number",
        "visible": "ally",
        "initial": 4,
        "meaning": "Current value of this player's d8 (1-8)",
        "observable": false
      },
      {
        "key": "d12_value",
        "type": "number",
        "visible": "ally",
        "initial": 7,
        "meaning": "Current value of this player's d12 (1-12)",
        "observable": false
      },
      {
        "key": "load_d4",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Loading answer for the d4, before validation",
        "observable": false
      },
      {
        "key": "load_d6",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Loading answer for the d6, before validation",
        "observable": false
      },
      {
        "key": "load_d8",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Loading answer for the d8, before validation",
        "observable": false
      },
      {
        "key": "load_d12",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Loading answer for the d12, before validation",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "turn",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current turn number, 1 to 40",
        "observable": true
      },
      {
        "key": "leg",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current leg, 1 or 2",
        "observable": true
      },
      {
        "key": "first_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the player who is First",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat acting this turn",
        "observable": false
      },
      {
        "key": "previous_was_pass",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the previous turn in this leg was a pass",
        "observable": false
      },
      {
        "key": "this_is_pass",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this turn's action is a pass",
        "observable": false
      },
      {
        "key": "declaration",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The active player's chosen declaration this turn",
        "observable": false
      },
      {
        "key": "target_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Size of the declared target die",
        "observable": false
      },
      {
        "key": "attacker_large_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Size of the power attacker, or the larger-size skill attacker",
        "observable": false
      },
      {
        "key": "attacker_small_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Size of the smaller-size skill attacker (0 for a power attack)",
        "observable": false
      },
      {
        "key": "attack_value",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch copy of the attacking value (power) or the sum of the two values (skill)",
        "observable": false
      },
      {
        "key": "target_value",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch copy of the target's value",
        "observable": false
      },
      {
        "key": "attack_success",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this turn's attack succeeded",
        "observable": false
      },
      {
        "key": "leg_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the current leg has ended",
        "observable": false
      },
      {
        "key": "match_over",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the match has ended",
        "observable": true
      }
    ]
  },
  "setup": [
    "Each player's score is set to 0.",
    "One seat is chosen uniformly at random to be First: first_seat is set to that seat and its is_first is set to true; the other seat is Second.",
    "turn is set to 0 and leg to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "turn += 1; leg = 1 if turn <= 20, otherwise 2. If turn == 21, set leg_over = false. active_seat = first_seat when (turn is odd and leg == 1) or (turn is even and leg == 2); otherwise active_seat = the other seat."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number 1-4 for the d4",
      "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in each player's load_d4. Nobody sees any answer."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number 1-6 for the d6",
      "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d6."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number 1-8 for the d8",
      "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d8."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number 1-12 for the d12",
      "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d12."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when turn == 1 or turn == 21. For each player: if load_d4 + load_d6 + load_d8 + load_d12 == 16, then d4_value = load_d4, d6_value = load_d6, d8_value = load_d8 and d12_value = load_d12; otherwise d4_value = 2, d6_value = 3, d8_value = 4 and d12_value = 7. For both players, in_play = [4, 6, 8, 12]. previous_was_pass = false. Announces only that loading is done."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false. Public status: turn, leg, active_seat, each player's in_play, both scores, and previous_was_pass."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false. Each player privately receives the values (d4_value, d6_value, d8_value, d12_value) of the dice in their own in_play."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one choice: 'pass', or 'power: my dA -> your dT' for each own die A in in_play and each opponent die T in the opponent's in_play, or 'skill: my dA + my dB -> your dT' for each unordered pair of two different own dice A, B in in_play and each opponent die T",
      "effect": "Runs only when leg_over == false. Stores the choice in declaration. Sets this_is_pass, target_size, attacker_large_size (the power die, or the larger of the two skill dice) and attacker_small_size (the smaller skill die, or 0)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false and this_is_pass == false. target_value = the defender's value for the die of size target_size. For a power attack, attack_value = the attacker's value for the die of size attacker_large_size, and attack_success = (attack_value >= target_value). For a skill attack, attack_value = the sum of the attacker's values for the dice of sizes attacker_large_size and attacker_small_size, and attack_success = (attack_value == target_value)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == true. Remove target_size from the defender's in_play; the attacker's score += target_size; announce publicly that the target (size target_size) was captured and its value target_value. The attacker's die of size attacker_large_size is rerolled to a uniform random value from 1 to attacker_large_size, and its new value is told only to its owner. The smaller skill attacker keeps its value."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == false. Remove attacker_large_size from the attacker's in_play; the defender's score += attacker_large_size; announce publicly the captured die's size and value. Nothing is rerolled, the smaller skill attacker keeps its value, and target_value is not revealed."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false. Public result: 'pass', or the target size, the attacking die sizes, and whether the attack succeeded."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when leg_over == false. leg_over = true if either player's in_play is empty, or (this_is_pass and previous_was_pass), or turn == 20. Then previous_was_pass = this_is_pass. If leg == 1 and leg_over == true and turn < 20, set turn = 20 (the remaining leg-1 turns are skipped). If leg == 2 and (leg_over == true or turn == 40), set match_over = true."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if match_over == true; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "match_over == true (set when turn == 40 or when leg 2 ends early)",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score: the total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks. The higher score wins; equal scores share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Each player owns four dice of sizes 4, 6, 8 and 12; the sizes in each player's in_play are public."
    },
    {
      "id": "R2",
      "text": "Each player's score starts at 0 and carries over from leg 1 to leg 2."
    },
    {
      "id": "R3",
      "text": "Before turn 1, exactly one of the two seats is chosen at random as First (is_first = true)."
    },
    {
      "id": "R4",
      "text": "In leg 1 (turns 1-20), First acts on odd turns and Second acts on even turns."
    },
    {
      "id": "R5",
      "text": "In leg 2 (turns 21-40), Second acts on odd turns and First acts on even turns."
    },
    {
      "id": "R6",
      "text": "On turns 1 and 21, both players secretly and simultaneously choose values d4 in 1-4, d6 in 1-6, d8 in 1-8 and d12 in 1-12."
    },
    {
      "id": "R7",
      "text": "When a player's four loaded values total exactly 16, those values become the dice values."
    },
    {
      "id": "R8",
      "text": "When a player's four loaded values do not total 16, the values become d4=2, d6=3, d8=4, d12=7."
    },
    {
      "id": "R9",
      "text": "At the start of each leg, both players' in_play is reset to [4, 6, 8, 12]; captures from leg 1 do not carry over, but scores do."
    },
    {
      "id": "R10",
      "text": "Each turn, the public status announces the turn, the leg, the active seat, each player's in_play, both scores, and whether the previous turn in this leg was a pass."
    },
    {
      "id": "R11",
      "text": "Each turn, each player is privately told only the values of their own remaining dice and never the opponent's values, except values announced on capture."
    },
    {
      "id": "R12",
      "text": "The active player may pass, declare a power attack (one own remaining die against one opponent remaining die), or declare a skill attack (two different own remaining dice against one opponent remaining die)."
    },
    {
      "id": "R13",
      "text": "When a power attack has attacker value >= target value (for example 5 vs 5), it succeeds; when the attacker value is lower (4 vs 5), it fails."
    },
    {
      "id": "R14",
      "text": "When a skill attack's two values sum exactly to the target value (3 + 4 vs 7), it succeeds; any other sum (3 + 4 vs 6 or vs 8) fails."
    },
    {
      "id": "R15",
      "text": "When an attack succeeds, the target is removed from the defender's in_play, its value is announced publicly, and the attacker's score rises by the target's size (for example +12 for a d12)."
    },
    {
      "id": "R16",
      "text": "When an attack succeeds, the attacking die (in a skill attack, only the larger-size one) is rerolled to a uniform value from 1 to its size, told only to its owner; the smaller skill attacker keeps its value."
    },
    {
      "id": "R17",
      "text": "When an attack fails, the attacking die (in a skill attack, only the larger-size one) is removed from the attacker's in_play, its value is announced publicly, and the defender's score rises by its size."
    },
    {
      "id": "R18",
      "text": "When an attack fails, nothing is rerolled, the smaller skill attacker keeps its value, and the target's value is not revealed."
    },
    {
      "id": "R19",
      "text": "When either player's in_play becomes empty, the current leg ends immediately."
    },
    {
      "id": "R20",
      "text": "When this turn and the previous turn in the same leg are both passes, the current leg ends immediately."
    },
    {
      "id": "R21",
      "text": "When turn 20 is completed, leg 1 ends."
    },
    {
      "id": "R22",
      "text": "When leg 1 ends before turn 20, the remaining turns up to 20 are skipped with no actions, and play resumes at turn 21 with leg 2 loading."
    },
    {
      "id": "R23",
      "text": "When turn 40 is completed or leg 2 ends early, the match ends."
    },
    {
      "id": "R24",
      "text": "When the match ends, the player with the higher score wins; equal scores are a draw."
    },
    {
      "id": "R25",
      "text": "Values change only by loading on turns 1 and 21 or by the reroll after a successful attack."
    }
  ],
  "offers": [
    {
      "question": "Loading of the d4 (turns 1 and 21)",
      "who": "both seats",
      "options": "a whole number from 1 to 4"
    },
    {
      "question": "Loading of the d6 (turns 1 and 21)",
      "who": "both seats",
      "options": "a whole number from 1 to 6"
    },
    {
      "question": "Loading of the d8 (turns 1 and 21)",
      "who": "both seats",
      "options": "a whole number from 1 to 8"
    },
    {
      "question": "Loading of the d12 (turns 1 and 21)",
      "who": "both seats",
      "options": "a whole number from 1 to 12"
    },
    {
      "question": "Turn choice",
      "who": "the active seat only",
      "options": "'pass'; 'power: my dA -> your dT' for every own die A in own in_play and every die T in the opponent's in_play; 'skill: my dA + my dB -> your dT' for every unordered pair of two different own dice A, B in own in_play (offered only if at least 2 own dice remain) and every die T in the opponent's in_play. The non-active seat is not asked."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed the table at 2. Every mechanic (attacker vs defender, alternating turns, loading against one opponent) is head-to-head and has no meaning with more seats."
    },
    {
      "what": "No pre-choice talk step",
      "why": "The source has no talk. In a two-player zero-sum duel, talk adds no shared decision to negotiate."
    },
    {
      "what": "Leg-1 early end jumps the turn counter to 20",
      "why": "The source says the skipped turns pass with no actions. Jumping turn to 20 is equivalent and avoids empty rounds."
    },
    {
      "what": "Die sizes listed as separate parameters d4_size, d6_size, d8_size, d12_size",
      "why": "Each parameter must be a single number."
    },
    {
      "what": "Strategy note",
      "why": "A thoughtful player loads to bait or defend, for example a high d12 for power and small dice that sum to likely targets. They infer hidden values from failed attacks and rerolls, and pass when attacking risks feeding the opponent a large die."
    }
  ],
  "simplifications": [
    {
      "what": "Loading is asked as four simultaneous number questions, one per die, then validated",
      "why": "The engine takes one number per question. The sum-to-16 check and the default replacement are done by arithmetic afterwards."
    },
    {
      "what": "Turn declarations are offered as a list of legal choices only",
      "why": "Choosing from a list makes illegal declarations impossible, so the 'invalid counts as pass' rule never triggers. The effect on play is identical."
    },
    {
      "what": "Attack resolution copies the attacker's and target's values into table scratch attributes (attack_value, target_value) before comparing",
      "why": "The engine has no direct operand for comparing attributes of two different players."
    },
    {
      "what": "The winner is computed as the highest you.score with ties shared",
      "why": "The engine has no separate draw. Equal top scores sharing the win is how a draw is represented."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, is_first, in_play; table: turn, leg, match_over.
````

## Reply

````
```json
[
  {
    "name": "Each player starts with dice of sizes 4, 6, 8 and 12 in play",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "players": {
        "1": {"in_play": [4, 6, 8, 12], "score": 0},
        "2": {"in_play": [4, 6, 8, 12], "score": 0}
      },
      "lens": {"players": {"1": {"in_play": 4}, "2": {"in_play": 4}}}
    }
  },
  {
    "name": "Scores carry over from leg 1 into leg 2",
    "rule": "R2",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "score": 10},
        "2": {"is_first": false, "score": 6}
      },
      "game": {"turn": 20, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"score": 10}, "2": {"score": 6}},
      "game": {"turn": 21, "leg": 2, "match_over": false}
    }
  },
  {
    "name": "Chance picks First; only chance-independent facts after turn 1 are checked",
    "rule": "R3",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 0, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 6, 8, 12]}
      },
      "game": {"turn": 1, "leg": 1}
    }
  },
  {
    "name": "Leg 1 odd turn: First acts, Second is not asked",
    "rule": "R4",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 3, "leg": 1},
      "offered": [{"seat": 1, "option": "pass"}],
      "not_offered": [{"seat": 2, "option": "pass"}]
    }
  },
  {
    "name": "Leg 1 even turn: Second acts, First is not asked",
    "rule": "R4",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 3, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 4, "leg": 1},
      "offered": [{"seat": 2, "option": "pass"}],
      "not_offered": [{"seat": 1, "option": "pass"}]
    }
  },
  {
    "name": "Leg 2 even turn: First acts",
    "rule": "R5",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 21, "leg": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 22, "leg": 2},
      "offered": [{"seat": 1, "option": "pass"}],
      "not_offered": [{"seat": 2, "option": "pass"}]
    }
  },
  {
    "name": "Leg 2 odd turn: Second acts",
    "rule": "R5",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 22, "leg": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 23, "leg": 2},
      "offered": [{"seat": 2, "option": "pass"}],
      "not_offered": [{"seat": 1, "option": "pass"}]
    }
  },
  {
    "name": "On turn 1 both seats load all four dice",
    "rule": "R6",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 1, "options_include": 6},
      {"seat": 1, "options_include": 1},
      {"seat": 1, "options_include": 5}
    ],
    "expect": {
      "game": {"turn": 1},
      "offered": [
        {"seat": 1, "option": 4},
        {"seat": 1, "option": 12},
        {"seat": 2, "option": 4},
        {"seat": 2, "option": 12}
      ]
    }
  },
  {
    "name": "No loading on a turn other than 1 or 21",
    "rule": "R6",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 1, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 2},
      "not_offered": [
        {"seat": 1, "option": 12},
        {"seat": 2, "option": 12}
      ]
    }
  },
  {
    "name": "Loads totalling 16 become the values: loaded d4=4 beats loaded d8=2",
    "rule": "R7",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"first_seat": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 1, "options_include": 6},
      {"seat": 1, "options_include": 1},
      {"seat": 1, "options_include": 5},
      {"seat": 2, "options_include": 1},
      {"seat": 2, "options_include": 1},
      {"seat": 2, "options_include": 2},
      {"seat": 2, "options_include": 12},
      {"seat": 1, "options_include": "power: my d4 -> your d8"}
    ],
    "expect": {
      "players": {
        "1": {"score": 8, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 6, 12]}
      },
      "game": {"turn": 1}
    }
  },
  {
    "name": "Loads not totalling 16 fall back to defaults: loaded d8=1 fails against default d4=2",
    "rule": "R8",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"first_seat": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 1, "options_include": 6},
      {"seat": 1, "options_include": 1},
      {"seat": 1, "options_include": 5},
      {"seat": 2, "options_include": 1, "times": 4},
      {"seat": 1, "options_include": "power: my d8 -> your d4"}
    ],
    "expect": {
      "players": {
        "1": {"score": 0, "in_play": [4, 6, 12]},
        "2": {"score": 8, "in_play": [4, 6, 8, 12]}
      }
    }
  },
  {
    "name": "At the start of leg 2 both in_play lists reset and scores stay",
    "rule": "R9",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "in_play": [4], "score": 20},
        "2": {"is_first": false, "in_play": [6, 12], "score": 4}
      },
      "game": {"turn": 20, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"in_play": [4, 6, 8, 12], "score": 20},
        "2": {"in_play": [4, 6, 8, 12], "score": 4}
      },
      "game": {"turn": 21, "leg": 2}
    }
  },
  {
    "name": "Each turn advances the public turn counter within leg 1",
    "rule": "R10",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "score": 3},
        "2": {"is_first": false, "score": 5}
      },
      "game": {"turn": 4, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"score": 3}, "2": {"score": 5}},
      "game": {"turn": 5, "leg": 1}
    }
  },
  {
    "name": "A pass turn leaves the public state unchanged",
    "rule": "R11",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "in_play": [4, 8]},
        "2": {"is_first": false, "in_play": [6, 12]}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"in_play": [4, 8], "score": 0},
        "2": {"in_play": [6, 12], "score": 0}
      },
      "game": {"turn": 3}
    }
  },
  {
    "name": "Active seat is offered pass, power and skill only with remaining dice",
    "rule": "R12",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "in_play": [4, 8]},
        "2": {"is_first": false, "in_play": [4, 12]}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "offered": [
        {"seat": 1, "option": "pass"},
        {"seat": 1, "option": "power: my d8 -> your d12"},
        {"seat": 1, "option": "power: my d4 -> your d4"},
        {"seat": 1, "option": "skill: my d4 + my d8 -> your d12"}
      ],
      "not_offered": [
        {"seat": 1, "option": "power: my d6 -> your d4"},
        {"seat": 1, "option": "power: my d8 -> your d6"},
        {"seat": 1, "option": "power: my d12 -> your d12"},
        {"seat": 2, "option": "pass"}
      ]
    }
  },
  {
    "name": "Power attack 5 vs 5 succeeds",
    "rule": "R13",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d12_value": 5},
        "2": {"is_first": false, "d8_value": 5}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "power: my d12 -> your d8"}],
    "expect": {
      "players": {
        "1": {"score": 8, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 6, 12]}
      }
    }
  },
  {
    "name": "Power attack 4 vs 5 fails",
    "rule": "R13",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d12_value": 4},
        "2": {"is_first": false, "d8_value": 5}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "power: my d12 -> your d8"}],
    "expect": {
      "players": {
        "1": {"score": 0, "in_play": [4, 6, 8]},
        "2": {"score": 12, "in_play": [4, 6, 8, 12]}
      }
    }
  },
  {
    "name": "Skill attack 3 + 4 vs 7 succeeds",
    "rule": "R14",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d6_value": 3, "d8_value": 4},
        "2": {"is_first": false, "d12_value": 7}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "skill: my d6 + my d8 -> your d12"}],
    "expect": {
      "players": {
        "1": {"score": 12, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 6, 8]}
      }
    }
  },
  {
    "name": "Skill attack 3 + 4 vs 6 fails",
    "rule": "R14",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d6_value": 3, "d8_value": 4},
        "2": {"is_first": false, "d12_value": 6}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "skill: my d6 + my d8 -> your d12"}],
    "expect": {
      "players": {
        "1": {"score": 0, "in_play": [4, 6, 12]},
        "2": {"score": 8, "in_play": [4, 6, 8, 12]}
      }
    }
  },
  {
    "name": "Capturing a d12 adds 12 to the attacker's score",
    "rule": "R15",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d12_value": 12, "score": 5},
        "2": {"is_first": false, "d12_value": 7}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "power: my d12 -> your d12"}],
    "expect": {
      "players": {
        "1": {"score": 17, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 6, 8]}
      }
    }
  },
  {
    "name": "After a successful skill attack the smaller die keeps its value (d6=3 later captures a d6 showing 3)",
    "rule": "R16",
    "players": 2,
    "seed": 1,
    "rounds": 3,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d6_value": 3, "d8_value": 4},
        "2": {"is_first": false, "d12_value": 7, "d6_value": 3}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "skill: my d6 + my d8 -> your d12"},
      {"seat": 1, "options_include": "power: my d6 -> your d6"}
    ],
    "expect": {
      "players": {
        "1": {"score": 18, "in_play": [4, 6, 8, 12]},
        "2": {"score": 0, "in_play": [4, 8]}
      },
      "game": {"turn": 5}
    }
  },
  {
    "name": "Failed skill attack: only the larger attacker is lost and the defender gains its size",
    "rule": "R17",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d4_value": 1, "d6_value": 2, "score": 2},
        "2": {"is_first": false, "d12_value": 7, "score": 1}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "skill: my d4 + my d6 -> your d12"}],
    "expect": {
      "players": {
        "1": {"score": 2, "in_play": [4, 8, 12]},
        "2": {"score": 7, "in_play": [4, 6, 8, 12]}
      }
    }
  },
  {
    "name": "After a failed skill attack the smaller die keeps its value (d4=1 later captures a d4 showing 1)",
    "rule": "R18",
    "players": 2,
    "seed": 1,
    "rounds": 3,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d4_value": 1, "d6_value": 2},
        "2": {"is_first": false, "d12_value": 7, "d4_value": 1}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "skill: my d4 + my d6 -> your d12"},
      {"seat": 1, "options_include": "power: my d4 -> your d4"}
    ],
    "expect": {
      "players": {
        "1": {"score": 4, "in_play": [4, 8, 12]},
        "2": {"score": 6, "in_play": [6, 8, 12]}
      },
      "game": {"turn": 5}
    }
  },
  {
    "name": "Capturing the opponent's last die ends leg 1 at once (turn jumps to 20)",
    "rule": "R19",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d12_value": 7},
        "2": {"is_first": false, "in_play": [4], "d4_value": 2}
      },
      "game": {"turn": 4, "first_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "power: my d12 -> your d4"}],
    "expect": {
      "players": {
        "1": {"score": 4},
        "2": {"score": 0, "in_play": []}
      },
      "game": {"turn": 20, "leg": 1, "match_over": false}
    }
  },
  {
    "name": "Two passes in a row end leg 1 (turn jumps to 20)",
    "rule": "R20",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {"1": {"is_first": true}, "2": {"is_first": false}},
      "game": {"turn": 4, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "game": {"turn": 20, "leg": 1, "match_over": false},
      "offered": [
        {"seat": 1, "option": "pass"},
        {"seat": 2, "option": "pass"}
      ]
    }
  },
  {
    "name": "Completing turn 20 ends leg 1 and the next turn starts leg 2",
    "rule": "R21",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "in_play": [4], "score": 9},
        "2": {"is_first": false, "in_play": [8, 12], "score": 3}
      },
      "game": {"turn": 19, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"in_play": [4, 6, 8, 12], "score": 9},
        "2": {"in_play": [4, 6, 8, 12], "score": 3}
      },
      "game": {"turn": 21, "leg": 2, "match_over": false}
    }
  },
  {
    "name": "Early end of leg 1 skips to turn 21 with leg 2 loading",
    "rule": "R22",
    "players": 2,
    "seed": 1,
    "rounds": 3,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "in_play": [4, 8], "score": 3},
        "2": {"is_first": false, "in_play": [6], "score": 5}
      },
      "game": {"turn": 4, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"in_play": [4, 6, 8, 12], "score": 3},
        "2": {"in_play": [4, 6, 8, 12], "score": 5}
      },
      "game": {"turn": 21, "leg": 2, "match_over": false},
      "offered": [
        {"seat": 1, "option": 12},
        {"seat": 2, "option": 12}
      ]
    }
  },
  {
    "name": "Completing turn 40 ends the match and the higher score wins",
    "rule": "R23",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "score": 20},
        "2": {"is_first": false, "score": 14}
      },
      "game": {"turn": 39, "leg": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 20, "2": 14},
      "game": {"match_over": true, "turn": 40}
    }
  },
  {
    "name": "Leg 2 ending early (last die captured) ends the match",
    "rule": "R23",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": false, "score": 10, "d12_value": 7},
        "2": {"is_first": true, "score": 12, "in_play": [4], "d4_value": 2}
      },
      "game": {"turn": 30, "leg": 2, "first_seat": 2}
    },
    "rules": [{"seat": 1, "options_include": "power: my d12 -> your d4"}],
    "expect": {
      "winner": 1,
      "standings": {"1": 14, "2": 12},
      "game": {"match_over": true}
    }
  },
  {
    "name": "Equal scores at the end share the win",
    "rule": "R24",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "score": 10},
        "2": {"is_first": false, "score": 10}
      },
      "game": {"turn": 39, "leg": 2, "first_seat": 1}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 10, "2": 10},
      "game": {"match_over": true}
    }
  },
  {
    "name": "A failed attack rerolls nothing: defender's d12=8 then captures a d8 showing 8",
    "rule": "R25",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"is_first": true, "d12_value": 1, "d8_value": 8},
        "2": {"is_first": false, "d12_value": 8}
      },
      "game": {"turn": 2, "first_seat": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "power: my d12 -> your d12"},
      {"seat": 2, "options_include": "power: my d12 -> your d8"}
    ],
    "expect": {
      "players": {
        "1": {"score": 0, "in_play": [4, 6]},
        "2": {"score": 20, "in_play": [4, 6, 8, 12]}
      },
      "game": {"turn": 4}
    }
  }
]
```
````
