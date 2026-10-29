# 06 spec

- time: 2026-10-28T05:17:40+00:00 (42.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 295abf53857ccd4c, reply sha256 df7846027d161de7

## Sent

````
Game: Loaded Button Men
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DICE. Each player owns four dice: a d4, a d6, a d8 and a d12.
- A die's SIZE is its number of sides (4, 6, 8 or 12). Sizes are public.
- A die's VALUE is a whole number from 1 to its size. A player always knows their own values. A player is never told the opponent's values, except as stated below.
- Each player has a SCORE that starts at 0 and carries over between legs.

MATCH STRUCTURE.
- The match has two legs: leg 1 is turns 1 to 20 and leg 2 is turns 21 to 40.
- Before turn 1, one player is chosen at random to be First.
- Leg 1: First acts on odd turns (1, 3, ..., 19) and the other player, Second, acts on even turns (2, 4, ..., 20).
- Leg 2: Second acts on odd turns (21, 23, ..., 39) and First acts on even turns (22, ..., 40).

LOADING (at the start of each leg, on turns 1 and 21).
- Both players at the same moment secretly choose a value for each of their four dice.
- Each value must be at least 1 and at most that die's size, and the four values must total exactly 16.
- An invalid loading is replaced by the default loading: d4=2, d6=3, d8=4, d12=7.
- All four dice of both players are in play at the start of each leg. Captures from leg 1 do not carry over, but scores do.

EACH TURN (while the current leg is not over):
1. Public status. Announce the turn number, the leg, whose turn it is, which die sizes each player still has in play, both scores, and whether the previous turn in this leg was a pass.
2. Private status. Tell each player the current values of their own remaining dice.
3. Choice. The active player either PASSES or declares an ATTACK:
   - one of the opponent's remaining dice as TARGET, and
   - either one of their own remaining dice (a POWER attack) or exactly two different dice of their own (a SKILL attack).
   A die may not be listed twice. Any declaration that breaks these rules counts as a pass.
4. Resolution.
   - A power attack succeeds if the attacker's value is greater than or equal to the target's value.
   - A skill attack succeeds if the two attackers' values sum exactly to the target's value.
5. Public result. Announce the pass, or the target size, the attacking die sizes and whether the attack succeeded.
6. Success.
   - The target is captured and removed from the leg.
   - Its value is announced publicly.
   - The attacker's score rises by the target's size.
   - The attacking die (in a skill attack, only the larger-size of the two) is rerolled to a uniformly random value from 1 to its size. Its new value is told only to its owner.
   - In a skill attack the smaller attacker keeps its value.
7. Failure.
   - The attacking die is captured by the defender. In a skill attack, only the larger-size attacker is captured; the smaller stays in play with its value unchanged.
   - The captured die's value is announced publicly.
   - The defender's score rises by the captured die's size.
   - Nothing is rerolled, and the target's value is not revealed.
8. Leg end check. The leg ends immediately if any of these is true:
   - either player has no dice left;
   - this turn and the previous turn in this leg were both passes;
   - this is turn 20 (for leg 1).
   If leg 1 ends early, the remaining turns up to 20 are skipped with no actions.
9. Match end. After turn 40, or when leg 2 ends, the match ends.

NOTES.
- Values change only by loading at the start of a leg or by the reroll after a successful attack.
- Captured dice never return within a leg.
- Captures are not compulsory: a player may always pass.

How the winner is decided: When the match ends, the player with the higher score (total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks) wins. Equal scores are a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Loaded Button Men",
  "summary": "Two players secretly load four dice (d4, d6, d8, d12) to total 16, then take turns capturing each other's dice with power or skill attacks over two 20-turn legs; the higher total of captured sizes wins.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "die_sizes": [4, 6, 8, 12],
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total sizes of all dice this player has captured across both legs", "observable": true},
      {"key": "is_first", "type": "bool", "visible": "public", "initial": false, "meaning": "True for the player chosen at random to be First", "observable": true},
      {"key": "in_play", "type": "list", "visible": "public", "initial": [4, 6, 8, 12], "meaning": "Sizes of this player's dice still in play this leg", "observable": true},
      {"key": "d4_value", "type": "number", "visible": "ally", "initial": 2, "meaning": "Current value of this player's d4 (1-4)", "observable": false},
      {"key": "d6_value", "type": "number", "visible": "ally", "initial": 3, "meaning": "Current value of this player's d6 (1-6)", "observable": false},
      {"key": "d8_value", "type": "number", "visible": "ally", "initial": 4, "meaning": "Current value of this player's d8 (1-8)", "observable": false},
      {"key": "d12_value", "type": "number", "visible": "ally", "initial": 7, "meaning": "Current value of this player's d12 (1-12)", "observable": false},
      {"key": "load_d4", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d4, before validation", "observable": false},
      {"key": "load_d6", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d6, before validation", "observable": false},
      {"key": "load_d8", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d8, before validation", "observable": false},
      {"key": "load_d12", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d12, before validation", "observable": false}
    ],
    "game": [
      {"key": "turn", "type": "number", "visible": "public", "initial": 0, "meaning": "Current turn number, 1 to 40", "observable": true},
      {"key": "leg", "type": "number", "visible": "public", "initial": 1, "meaning": "Current leg, 1 or 2", "observable": true},
      {"key": "first_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the player who is First", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat acting this turn", "observable": false},
      {"key": "previous_was_pass", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the previous turn in this leg was a pass", "observable": false},
      {"key": "this_is_pass", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this turn's action is a pass", "observable": false},
      {"key": "declaration", "type": "text", "visible": "public", "initial": "", "meaning": "The active player's chosen declaration this turn", "observable": false},
      {"key": "target_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the declared target die", "observable": false},
      {"key": "attacker_large_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the power attacker, or the larger-size skill attacker", "observable": false},
      {"key": "attacker_small_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the smaller-size skill attacker (0 for a power attack)", "observable": false},
      {"key": "attack_value", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch copy of the attacking value (power) or the sum of the two values (skill)", "observable": false},
      {"key": "target_value", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch copy of the target's value", "observable": false},
      {"key": "attack_success", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this turn's attack succeeded", "observable": false},
      {"key": "leg_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the current leg has ended", "observable": false},
      {"key": "match_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the match has ended", "observable": true}
    ]
  },
  "setup": [
    "Each player's score is set to 0.",
    "One seat is chosen uniformly at random to be First: first_seat is set to that seat and its is_first is set to true; the other seat is Second.",
    "turn is set to 0 and leg to 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "turn += 1; leg = 1 if turn <= 20, otherwise 2. If turn == 21, set leg_over = false. active_seat = first_seat when (turn is odd and leg == 1) or (turn is even and leg == 2); otherwise active_seat = the other seat."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-4 for the d4", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in each player's load_d4. Nobody sees any answer."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-6 for the d6", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d6."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-8 for the d8", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d8."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-12 for the d12", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d12."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when turn == 1 or turn == 21. For each player: if load_d4 + load_d6 + load_d8 + load_d12 == 16, then d4_value = load_d4, d6_value = load_d6, d8_value = load_d8 and d12_value = load_d12; otherwise d4_value = 2, d6_value = 3, d8_value = 4 and d12_value = 7. For both players, in_play = [4, 6, 8, 12]. previous_was_pass = false. Announces only that loading is done."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Public status: turn, leg, active_seat, each player's in_play, both scores, and previous_was_pass."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Each player privately receives the values (d4_value, d6_value, d8_value, d12_value) of the dice in their own in_play."},
    {"action": "ask", "who": "seat active_seat", "answer": "one choice: 'pass', or 'power: my dA -> your dT' for each own die A in in_play and each opponent die T in the opponent's in_play, or 'skill: my dA + my dB -> your dT' for each unordered pair of two different own dice A, B in in_play and each opponent die T", "effect": "Runs only when leg_over == false. Stores the choice in declaration. Sets this_is_pass, target_size, attacker_large_size (the power die, or the larger of the two skill dice) and attacker_small_size (the smaller skill die, or 0)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false and this_is_pass == false. target_value = the defender's value for the die of size target_size. For a power attack, attack_value = the attacker's value for the die of size attacker_large_size, and attack_success = (attack_value >= target_value). For a skill attack, attack_value = the sum of the attacker's values for the dice of sizes attacker_large_size and attacker_small_size, and attack_success = (attack_value == target_value)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == true. Remove target_size from the defender's in_play; the attacker's score += target_size; announce publicly that the target (size target_size) was captured and its value target_value. The attacker's die of size attacker_large_size is rerolled to a uniform random value from 1 to attacker_large_size, and its new value is told only to its owner. The smaller skill attacker keeps its value."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == false. Remove attacker_large_size from the attacker's in_play; the defender's score += attacker_large_size; announce publicly the captured die's size and value. Nothing is rerolled, the smaller skill attacker keeps its value, and target_value is not revealed."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Public result: 'pass', or the target size, the attacking die sizes, and whether the attack succeeded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. leg_over = true if either player's in_play is empty, or (this_is_pass and previous_was_pass), or turn == 20. Then previous_was_pass = this_is_pass. If leg == 1 and leg_over == true and turn < 20, set turn = 20 (the remaining leg-1 turns are skipped). If leg == 2 and (leg_over == true or turn == 40), set match_over = true."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if match_over == true; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "match_over == true (set when turn == 40 or when leg 2 ends early)",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score: the total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks. The higher score wins; equal scores share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "Each player owns four dice of sizes 4, 6, 8 and 12; the sizes in each player's in_play are public."},
    {"id": "R2", "text": "Each player's score starts at 0 and carries over from leg 1 to leg 2."},
    {"id": "R3", "text": "Before turn 1, exactly one of the two seats is chosen at random as First (is_first = true)."},
    {"id": "R4", "text": "In leg 1 (turns 1-20), First acts on odd turns and Second acts on even turns."},
    {"id": "R5", "text": "In leg 2 (turns 21-40), Second acts on odd turns and First acts on even turns."},
    {"id": "R6", "text": "On turns 1 and 21, both players secretly and simultaneously choose values d4 in 1-4, d6 in 1-6, d8 in 1-8 and d12 in 1-12."},
    {"id": "R7", "text": "When a player's four loaded values total exactly 16, those values become the dice values."},
    {"id": "R8", "text": "When a player's four loaded values do not total 16, the values become d4=2, d6=3, d8=4, d12=7."},
    {"id": "R9", "text": "At the start of each leg, both players' in_play is reset to [4, 6, 8, 12]; captures from leg 1 do not carry over, but scores do."},
    {"id": "R10", "text": "Each turn, the public status announces the turn, the leg, the active seat, each player's in_play, both scores, and whether the previous turn in this leg was a pass."},
    {"id": "R11", "text": "Each turn, each player is privately told only the values of their own remaining dice and never the opponent's values, except values announced on capture."},
    {"id": "R12", "text": "The active player may pass, declare a power attack (one own remaining die against one opponent remaining die), or declare a skill attack (two different own remaining dice against one opponent remaining die)."},
    {"id": "R13", "text": "When a power attack has attacker value >= target value (for example 5 vs 5), it succeeds; when the attacker value is lower (4 vs 5), it fails."},
    {"id": "R14", "text": "When a skill attack's two values sum exactly to the target value (3 + 4 vs 7), it succeeds; any other sum (3 + 4 vs 6 or vs 8) fails."},
    {"id": "R15", "text": "When an attack succeeds, the target is removed from the defender's in_play, its value is announced publicly, and the attacker's score rises by the target's size (for example +12 for a d12)."},
    {"id": "R16", "text": "When an attack succeeds, the attacking die (in a skill attack, only the larger-size one) is rerolled to a uniform value from 1 to its size, told only to its owner; the smaller skill attacker keeps its value."},
    {"id": "R17", "text": "When an attack fails, the attacking die (in a skill attack, only the larger-size one) is removed from the attacker's in_play, its value is announced publicly, and the defender's score rises by its size."},
    {"id": "R18", "text": "When an attack fails, nothing is rerolled, the smaller skill attacker keeps its value, and the target's value is not revealed."},
    {"id": "R19", "text": "When either player's in_play becomes empty, the current leg ends immediately."},
    {"id": "R20", "text": "When this turn and the previous turn in the same leg are both passes, the current leg ends immediately."},
    {"id": "R21", "text": "When turn 20 is completed, leg 1 ends."},
    {"id": "R22", "text": "When leg 1 ends before turn 20, the remaining turns up to 20 are skipped with no actions, and play resumes at turn 21 with leg 2 loading."},
    {"id": "R23", "text": "When turn 40 is completed or leg 2 ends early, the match ends."},
    {"id": "R24", "text": "When the match ends, the player with the higher score wins; equal scores are a draw."},
    {"id": "R25", "text": "Values change only by loading on turns 1 and 21 or by the reroll after a successful attack."}
  ],
  "offers": [
    {"question": "Loading of the d4 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 4"},
    {"question": "Loading of the d6 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 6"},
    {"question": "Loading of the d8 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 8"},
    {"question": "Loading of the d12 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 12"},
    {"question": "Turn choice", "who": "the active seat only", "options": "'pass'; 'power: my dA -> your dT' for every own die A in own in_play and every die T in the opponent's in_play; 'skill: my dA + my dB -> your dT' for every unordered pair of two different own dice A, B in own in_play (offered only if at least 2 own dice remain) and every die T in the opponent's in_play. The non-active seat is not asked."}
  ],
  "choices": [
    {"what": "Exactly 2 players (min 2, max 2, suggested 2)", "why": "The designer fixed the table at 2; every mechanic (attacker vs defender, alternating turns, loading against one opponent) is head-to-head and has no meaning with more seats."},
    {"what": "No pre-choice talk step", "why": "The source has no talk. In a two-player zero-sum duel, talk adds no shared decision to negotiate."},
    {"what": "Leg-1 early end jumps the turn counter to 20", "why": "The source says the skipped turns pass with no actions; jumping turn to 20 is equivalent and avoids empty rounds."},
    {"what": "Strategy note", "why": "A thoughtful player loads to bait or defend (for example a high d12 for power and small dice that sum to likely targets), infers hidden values from failed attacks and rerolls, and passes when attacking risks feeding the opponent a large die."}
  ],
  "simplifications": [
    {"what": "Loading is asked as four simultaneous number questions, one per die, then validated", "why": "The engine takes one number per question; the sum-to-16 check and the default replacement are done by arithmetic afterwards."},
    {"what": "Turn declarations are offered as a list of legal choices only", "why": "Choosing from a list makes illegal declarations impossible, so the 'invalid counts as pass' rule never triggers; the effect on play is identical."},
    {"what": "Attack resolution copies the attacker's and target's values into table scratch attributes (attack_value, target_value) before comparing", "why": "The engine has no direct operand for comparing attributes of two different players."},
    {"what": "The winner is computed as the highest you.score with ties shared", "why": "The engine has no separate draw; equal top scores sharing the win is how a draw is represented."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Loaded Button Men",
  "summary": "Two players secretly load four dice (d4, d6, d8, d12) to total 16, then take turns capturing each other's dice with power or skill attacks over two 20-turn legs; the higher total of captured sizes wins.",
  "players": {"min": 2, "max": 2, "suggested": 2},
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total sizes of all dice this player has captured across both legs", "observable": true},
      {"key": "is_first", "type": "bool", "visible": "public", "initial": false, "meaning": "True for the player chosen at random to be First", "observable": true},
      {"key": "in_play", "type": "list", "visible": "public", "initial": [4, 6, 8, 12], "meaning": "Sizes of this player's dice still in play this leg", "observable": true},
      {"key": "d4_value", "type": "number", "visible": "ally", "initial": 2, "meaning": "Current value of this player's d4 (1-4)", "observable": false},
      {"key": "d6_value", "type": "number", "visible": "ally", "initial": 3, "meaning": "Current value of this player's d6 (1-6)", "observable": false},
      {"key": "d8_value", "type": "number", "visible": "ally", "initial": 4, "meaning": "Current value of this player's d8 (1-8)", "observable": false},
      {"key": "d12_value", "type": "number", "visible": "ally", "initial": 7, "meaning": "Current value of this player's d12 (1-12)", "observable": false},
      {"key": "load_d4", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d4, before validation", "observable": false},
      {"key": "load_d6", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d6, before validation", "observable": false},
      {"key": "load_d8", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d8, before validation", "observable": false},
      {"key": "load_d12", "type": "number", "visible": "ally", "initial": 0, "meaning": "Loading answer for the d12, before validation", "observable": false}
    ],
    "game": [
      {"key": "turn", "type": "number", "visible": "public", "initial": 0, "meaning": "Current turn number, 1 to 40", "observable": true},
      {"key": "leg", "type": "number", "visible": "public", "initial": 1, "meaning": "Current leg, 1 or 2", "observable": true},
      {"key": "first_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the player who is First", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat acting this turn", "observable": false},
      {"key": "previous_was_pass", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether the previous turn in this leg was a pass", "observable": false},
      {"key": "this_is_pass", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this turn's action is a pass", "observable": false},
      {"key": "declaration", "type": "text", "visible": "public", "initial": "", "meaning": "The active player's chosen declaration this turn", "observable": false},
      {"key": "target_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the declared target die", "observable": false},
      {"key": "attacker_large_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the power attacker, or the larger-size skill attacker", "observable": false},
      {"key": "attacker_small_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Size of the smaller-size skill attacker (0 for a power attack)", "observable": false},
      {"key": "attack_value", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch copy of the attacking value (power) or the sum of the two values (skill)", "observable": false},
      {"key": "target_value", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch copy of the target's value", "observable": false},
      {"key": "attack_success", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this turn's attack succeeded", "observable": false},
      {"key": "leg_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the current leg has ended", "observable": false},
      {"key": "match_over", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the match has ended", "observable": true}
    ]
  },
  "setup": [
    "Each player's score is set to 0.",
    "One seat is chosen uniformly at random to be First: first_seat is set to that seat and its is_first is set to true; the other seat is Second.",
    "turn is set to 0 and leg to 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "turn += 1; leg = 1 if turn <= 20, otherwise 2. If turn == 21, set leg_over = false. active_seat = first_seat when (turn is odd and leg == 1) or (turn is even and leg == 2); otherwise active_seat = the other seat."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-4 for the d4", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in each player's load_d4. Nobody sees any answer."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-6 for the d6", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d6."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-8 for the d8", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d8."},
    {"action": "poll", "who": "all players", "answer": "a whole number 1-12 for the d12", "effect": "Runs only when turn == 1 or turn == 21. Stores the answer in load_d12."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when turn == 1 or turn == 21. For each player: if load_d4 + load_d6 + load_d8 + load_d12 == 16, then d4_value = load_d4, d6_value = load_d6, d8_value = load_d8 and d12_value = load_d12; otherwise d4_value = 2, d6_value = 3, d8_value = 4 and d12_value = 7. For both players, in_play = [4, 6, 8, 12]. previous_was_pass = false. Announces only that loading is done."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Public status: turn, leg, active_seat, each player's in_play, both scores, and previous_was_pass."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Each player privately receives the values (d4_value, d6_value, d8_value, d12_value) of the dice in their own in_play."},
    {"action": "ask", "who": "seat active_seat", "answer": "one choice: 'pass', or 'power: my dA -> your dT' for each own die A in in_play and each opponent die T in the opponent's in_play, or 'skill: my dA + my dB -> your dT' for each unordered pair of two different own dice A, B in in_play and each opponent die T", "effect": "Runs only when leg_over == false. Stores the choice in declaration. Sets this_is_pass, target_size, attacker_large_size (the power die, or the larger of the two skill dice) and attacker_small_size (the smaller skill die, or 0)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false and this_is_pass == false. target_value = the defender's value for the die of size target_size. For a power attack, attack_value = the attacker's value for the die of size attacker_large_size, and attack_success = (attack_value >= target_value). For a skill attack, attack_value = the sum of the attacker's values for the dice of sizes attacker_large_size and attacker_small_size, and attack_success = (attack_value == target_value)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == true. Remove target_size from the defender's in_play; the attacker's score += target_size; announce publicly that the target (size target_size) was captured and its value target_value. The attacker's die of size attacker_large_size is rerolled to a uniform random value from 1 to attacker_large_size, and its new value is told only to its owner. The smaller skill attacker keeps its value."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false, this_is_pass == false and attack_success == false. Remove attacker_large_size from the attacker's in_play; the defender's score += attacker_large_size; announce publicly the captured die's size and value. Nothing is rerolled, the smaller skill attacker keeps its value, and target_value is not revealed."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. Public result: 'pass', or the target size, the attacking die sizes, and whether the attack succeeded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Runs only when leg_over == false. leg_over = true if either player's in_play is empty, or (this_is_pass and previous_was_pass), or turn == 20. Then previous_was_pass = this_is_pass. If leg == 1 and leg_over == true and turn < 20, set turn = 20 (the remaining leg-1 turns are skipped). If leg == 2 and (leg_over == true or turn == 40), set match_over = true."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if match_over == true; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "match_over == true (set when turn == 40 or when leg 2 ends early)",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score: the total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks. The higher score wins; equal scores share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "Each player owns four dice of sizes 4, 6, 8 and 12; the sizes in each player's in_play are public."},
    {"id": "R2", "text": "Each player's score starts at 0 and carries over from leg 1 to leg 2."},
    {"id": "R3", "text": "Before turn 1, exactly one of the two seats is chosen at random as First (is_first = true)."},
    {"id": "R4", "text": "In leg 1 (turns 1-20), First acts on odd turns and Second acts on even turns."},
    {"id": "R5", "text": "In leg 2 (turns 21-40), Second acts on odd turns and First acts on even turns."},
    {"id": "R6", "text": "On turns 1 and 21, both players secretly and simultaneously choose values d4 in 1-4, d6 in 1-6, d8 in 1-8 and d12 in 1-12."},
    {"id": "R7", "text": "When a player's four loaded values total exactly 16, those values become the dice values."},
    {"id": "R8", "text": "When a player's four loaded values do not total 16, the values become d4=2, d6=3, d8=4, d12=7."},
    {"id": "R9", "text": "At the start of each leg, both players' in_play is reset to [4, 6, 8, 12]; captures from leg 1 do not carry over, but scores do."},
    {"id": "R10", "text": "Each turn, the public status announces the turn, the leg, the active seat, each player's in_play, both scores, and whether the previous turn in this leg was a pass."},
    {"id": "R11", "text": "Each turn, each player is privately told only the values of their own remaining dice and never the opponent's values, except values announced on capture."},
    {"id": "R12", "text": "The active player may pass, declare a power attack (one own remaining die against one opponent remaining die), or declare a skill attack (two different own remaining dice against one opponent remaining die)."},
    {"id": "R13", "text": "When a power attack has attacker value >= target value (for example 5 vs 5), it succeeds; when the attacker value is lower (4 vs 5), it fails."},
    {"id": "R14", "text": "When a skill attack's two values sum exactly to the target value (3 + 4 vs 7), it succeeds; any other sum (3 + 4 vs 6 or vs 8) fails."},
    {"id": "R15", "text": "When an attack succeeds, the target is removed from the defender's in_play, its value is announced publicly, and the attacker's score rises by the target's size (for example +12 for a d12)."},
    {"id": "R16", "text": "When an attack succeeds, the attacking die (in a skill attack, only the larger-size one) is rerolled to a uniform value from 1 to its size, told only to its owner; the smaller skill attacker keeps its value."},
    {"id": "R17", "text": "When an attack fails, the attacking die (in a skill attack, only the larger-size one) is removed from the attacker's in_play, its value is announced publicly, and the defender's score rises by its size."},
    {"id": "R18", "text": "When an attack fails, nothing is rerolled, the smaller skill attacker keeps its value, and the target's value is not revealed."},
    {"id": "R19", "text": "When either player's in_play becomes empty, the current leg ends immediately."},
    {"id": "R20", "text": "When this turn and the previous turn in the same leg are both passes, the current leg ends immediately."},
    {"id": "R21", "text": "When turn 20 is completed, leg 1 ends."},
    {"id": "R22", "text": "When leg 1 ends before turn 20, the remaining turns up to 20 are skipped with no actions, and play resumes at turn 21 with leg 2 loading."},
    {"id": "R23", "text": "When turn 40 is completed or leg 2 ends early, the match ends."},
    {"id": "R24", "text": "When the match ends, the player with the higher score wins; equal scores are a draw."},
    {"id": "R25", "text": "Values change only by loading on turns 1 and 21 or by the reroll after a successful attack."}
  ],
  "offers": [
    {"question": "Loading of the d4 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 4"},
    {"question": "Loading of the d6 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 6"},
    {"question": "Loading of the d8 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 8"},
    {"question": "Loading of the d12 (turns 1 and 21)", "who": "both seats", "options": "a whole number from 1 to 12"},
    {"question": "Turn choice", "who": "the active seat only", "options": "'pass'; 'power: my dA -> your dT' for every own die A in own in_play and every die T in the opponent's in_play; 'skill: my dA + my dB -> your dT' for every unordered pair of two different own dice A, B in own in_play (offered only if at least 2 own dice remain) and every die T in the opponent's in_play. The non-active seat is not asked."}
  ],
  "choices": [
    {"what": "Exactly 2 players (min 2, max 2, suggested 2)", "why": "The designer fixed the table at 2. Every mechanic (attacker vs defender, alternating turns, loading against one opponent) is head-to-head and has no meaning with more seats."},
    {"what": "No pre-choice talk step", "why": "The source has no talk. In a two-player zero-sum duel, talk adds no shared decision to negotiate."},
    {"what": "Leg-1 early end jumps the turn counter to 20", "why": "The source says the skipped turns pass with no actions. Jumping turn to 20 is equivalent and avoids empty rounds."},
    {"what": "Die sizes listed as separate parameters d4_size, d6_size, d8_size, d12_size", "why": "Each parameter must be a single number."},
    {"what": "Strategy note", "why": "A thoughtful player loads to bait or defend, for example a high d12 for power and small dice that sum to likely targets. They infer hidden values from failed attacks and rerolls, and pass when attacking risks feeding the opponent a large die."}
  ],
  "simplifications": [
    {"what": "Loading is asked as four simultaneous number questions, one per die, then validated", "why": "The engine takes one number per question. The sum-to-16 check and the default replacement are done by arithmetic afterwards."},
    {"what": "Turn declarations are offered as a list of legal choices only", "why": "Choosing from a list makes illegal declarations impossible, so the 'invalid counts as pass' rule never triggers. The effect on play is identical."},
    {"what": "Attack resolution copies the attacker's and target's values into table scratch attributes (attack_value, target_value) before comparing", "why": "The engine has no direct operand for comparing attributes of two different players."},
    {"what": "The winner is computed as the highest you.score with ties shared", "why": "The engine has no separate draw. Equal top scores sharing the win is how a draw is represented."}
  ],
  "unsupported": []
}
```
````
