# 19 spec

- time: 2026-10-28T05:32:39+00:00 (45.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0968e2ed1e4f0fe4, reply sha256 adec2fa198b12e9c

## Sent

````
Game: Button Men: Guard and Strike
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DICE. Each player (A and B) owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.

RANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 110,075,314,175. Write R in base 24 as digits D0 to D7, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.

LEGS. The match is exactly 30 exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.

EACH EXCHANGE:
1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.
2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.
3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.
4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.
- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.
- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.
- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.
- A die may capture and be captured in the same exchange; both effects happen.
5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.
6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.
7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.
8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.

How the winner is decided: After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.
````

## Reply

````
```json
{
  "name": "Button Men: Guard and Strike",
  "summary": "Two players each hold a d4, d8 and d12 with hidden values. Over 30 exchanges they pick at the same moment to guard one of their dice or to attack an opponent's die, capturing it if the attacker's value is at least the target's. Legs reset the dice, and surviving dice score bonuses.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "dice_per_player": 3,
    "small_die_size": 4,
    "medium_die_size": 8,
    "large_die_size": 12,
    "starting_score": 0,
    "random_max": 110075314175,
    "digit_base": 24,
    "digit_count": 8,
    "total_exchanges": 30,
    "max_exchanges_per_leg": 10,
    "action_count": 12,
    "guard_defense_points": 3,
    "failed_attack_defense_points": 2,
    "survive_bonus_d4": 2,
    "survive_bonus_d8": 4,
    "survive_bonus_d12": 6,
    "a_d4_digit": 0,
    "a_d8_digit": 1,
    "a_d12_digit": 2,
    "b_d4_digit": 3,
    "b_d8_digit": 4,
    "b_d12_digit": 5,
    "a_reroll_digit": 6,
    "b_reroll_digit": 7
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points so far", "observable": true},
      {"key": "d4_value", "type": "number", "visible": "ally", "initial": 1, "meaning": "Current value of own d4 (1-4)", "observable": false},
      {"key": "d8_value", "type": "number", "visible": "ally", "initial": 1, "meaning": "Current value of own d8 (1-8)", "observable": false},
      {"key": "d12_value", "type": "number", "visible": "ally", "initial": 1, "meaning": "Current value of own d12 (1-12)", "observable": false},
      {"key": "d4_alive", "type": "bool", "visible": "public", "initial": true, "meaning": "Own d4 not captured this leg", "observable": true},
      {"key": "d8_alive", "type": "bool", "visible": "public", "initial": true, "meaning": "Own d8 not captured this leg", "observable": true},
      {"key": "d12_alive", "type": "bool", "visible": "public", "initial": true, "meaning": "Own d12 not captured this leg", "observable": true},
      {"key": "action", "type": "number", "visible": "ally", "initial": 0, "meaning": "Action chosen this exchange (1-12); revealed in results", "observable": false},
      {"key": "attack_result", "type": "text", "visible": "public", "initial": "", "meaning": "Outcome of own attack this exchange: none, success, fail_guarded, fail_low, or no_effect", "observable": false},
      {"key": "revealed_values", "type": "list", "visible": "public", "initial": [], "meaning": "Die values of this player announced this exchange because of failed attacks", "observable": false}
    ],
    "game": [
      {"key": "exchange", "type": "number", "visible": "public", "initial": 1, "meaning": "Current exchange number (1-30)", "observable": true},
      {"key": "leg_exchange", "type": "number", "visible": "public", "initial": 1, "meaning": "Exchange number within the current leg (1-10)", "observable": true},
      {"key": "leg_start", "type": "bool", "visible": "public", "initial": true, "meaning": "This exchange starts a new leg", "observable": false},
      {"key": "digits", "type": "list", "visible": "none", "initial": [], "meaning": "D0 to D7, the base-24 digits of this exchange's random R", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is player A and seat 2 is player B.",
    "Both scores are set to 0.",
    "Set exchange to 1, leg_exchange to 1 and leg_start to true.",
    "All dice are marked alive."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Draw R uniformly from 0 to 110075314175 and store its base-24 digits D0..D7 in digits, where Dk = floor(R/24^k) mod 24. If leg_start: set every die's alive flag to true; set A's d4_value=(D0 mod 4)+1, d8_value=(D1 mod 8)+1, d12_value=(D2 mod 12)+1; set B's d4_value=(D3 mod 4)+1, d8_value=(D4 mod 8)+1, d12_value=(D5 mod 12)+1; set leg_exchange=1 and leg_start=false. Clear each player's revealed_values and attack_result."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce exchange, leg_exchange, both scores, and both players' d4_alive, d8_alive and d12_alive."},
    {"action": "sync", "who": "all players", "answer": null,
     "effect": "Each player privately sees their own d4_value, d8_value and d12_value."},
    {"action": "poll", "who": "all players", "answer": "one of 12 actions: 1 Guard my d4; 2 Guard my d8; 3 Guard my d12; 4 My d4 attacks their d4; 5 My d4 attacks their d8; 6 My d4 attacks their d12; 7 My d8 attacks their d4; 8 My d8 attacks their d8; 9 My d8 attacks their d12; 10 My d12 attacks their d4; 11 My d12 attacks their d8; 12 My d12 attacks their d12",
     "effect": "Set each player's action. Nobody sees the other's choice until both are in."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Resolve both attacks at once, using the values held at the start of this exchange. For each attacker X against opponent Y, where the action is 4-12 with attacking die a and target die t: if the X die a or the Y die t is not alive at the start of the exchange, attack_result=no_effect. Otherwise, if Y's action is the guard of die t (guard of d4=1, d8=2, d12=3) and that die is alive, attack_result=fail_guarded, Y.score += 3, and X's a value is appended to X.revealed_values. Otherwise, if X.a_value >= Y.t_value, attack_result=success, X.score += size of t (4, 8 or 12), and Y.t_alive is set to false after both attacks are resolved. Otherwise attack_result=fail_low, Y.score += 2, X's a value is appended to X.revealed_values and Y's t value is appended to Y.revealed_values. A die may capture and be captured in the same exchange."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Rerolls, at most one die per player. A player's die is rerolled if it was guarded this exchange and was alive at the start (action 1-3), or if it attacked with attack_result=success and is still alive after the captures. Player A's rerolled die is set to (D6 mod size)+1. Player B's rerolled die is set to (D7 mod size)+1. New values are visible only to their owner."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce both actions, each attack_result, each player's revealed_values, which dice were captured, and both scores. Rerolled values are not announced."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "If a player has d4_alive, d8_alive and d12_alive all false, or leg_exchange = 10, or exchange = 30, the leg ends: each player's score += 2*d4_alive + 4*d8_alive + 6*d12_alive, and leg_start is set to true. Otherwise leg_exchange += 1. Then exchange += 1."},
    {"action": "check", "who": "all players", "answer": null,
     "effect": "End the game if exchange > 30; otherwise continue to the next exchange."}
  ],
  "ending": {
    "condition": "exchange > 30",
    "rank_by": "you.score",
    "decided_by": "After 30 exchanges and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals share the win, which is a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the match begins, then each player has a d4, a d8 and a d12, all alive, and both scores are 0."},
    {"id": "R2", "text": "When an exchange starts, then a random R from 0 to 110075314175 is drawn and split into base-24 digits D0..D7, with Dk = floor(R/24^k) mod 24."},
    {"id": "R3", "text": "When a leg starts, then all six dice are alive again; A's d4, d8 and d12 are set to (D0 mod 4)+1, (D1 mod 8)+1 and (D2 mod 12)+1; and B's d4, d8 and d12 are set to (D3 mod 4)+1, (D4 mod 8)+1 and (D5 mod 12)+1."},
    {"id": "R4", "text": "When an exchange begins, then both players are told the exchange number, the leg exchange number, both scores and which dice each player still has, and each player privately sees only their own die values."},
    {"id": "R5", "text": "When choosing, then both players choose at the same time one of the 12 actions, without seeing the other's choice."},
    {"id": "R6", "text": "When an action names a die that was already captured before this exchange (the actor's or the opponent's), then that action does nothing."},
    {"id": "R7", "text": "When an attack targets a die its owner guards this exchange, then the attack fails, the defender scores 3, and the attacking die's value is announced to both players."},
    {"id": "R8", "text": "When an unguarded target is attacked and the attacking value is greater than or equal to the target's value, then the attacker scores the target's size (4, 8 or 12) and the target is captured for the rest of the leg."},
    {"id": "R9", "text": "When an unguarded target is attacked and the attacking value is lower than the target's value, then the attack fails, the defender scores 2, and both dice's values are announced to both players."},
    {"id": "R10", "text": "When both attacks are resolved, then they use the values from the start of the exchange, and a die may both capture and be captured in the same exchange."},
    {"id": "R11", "text": "When a die guarded this exchange, or a die that attacked successfully and was not captured this exchange, then it is rerolled: A's from (D6 mod size)+1 and B's from (D7 mod size)+1, with the new value shown only to its owner."},
    {"id": "R12", "text": "When results are announced, then both actions, each attack's outcome, any announced values, any captures and the new scores are shown, but rerolled values are not."},
    {"id": "R13", "text": "When a player has no dice left, or the leg reaches its 10th exchange, then the leg ends and each player scores +2 for a surviving d4, +4 for a surviving d8 and +6 for a surviving d12."},
    {"id": "R14", "text": "When a leg ends, then the next exchange starts a new leg."},
    {"id": "R15", "text": "When exchange 30 ends and the leg in progress has not already ended, then it ends and the surviving-dice bonuses are scored."},
    {"id": "R16", "text": "When the match is over, then the higher total score wins, and equal totals are a draw."}
  ],
  "offers": [
    {"question": "Choice of action each exchange", "who": "both seats",
     "options": "always all 12: Guard my d4; Guard my d8; Guard my d12; My d4 attacks their d4/d8/d12; My d8 attacks their d4/d8/d12; My d12 attacks their d4/d8/d12. An action naming an already-captured die is allowed but does nothing."}
  ],
  "choices": [
    {"what": "2 players, as filed", "why": "The designer fixed the game at 2. It is a head-to-head duel in which every action targets the single opponent's dice, so there is no room for more seats."},
    {"what": "Seat 1 is player A and seat 2 is player B", "why": "The rules assign different random digits to A and B, so each seat needs a fixed role."},
    {"what": "No talk step", "why": "The rules give no communication, and the game is purely adversarial with simultaneous choices."},
    {"what": "All 12 actions are offered even when a named die is captured", "why": "The rules list exactly 12 actions and state that an action naming a captured die does nothing, so offering them stays faithful."},
    {"what": "Strategy at the table", "why": "A thoughtful player tracks announced values and which dice were rerolled, guards a high-value die that is likely to be attacked, and attacks dice whose values are revealed as low or that are small. A thoughtless player attacks blindly into guards."}
  ],
  "simplifications": [
    {"what": "R is stored as its eight base-24 digits", "why": "24^8 = 110075314176, so a uniform R from 0 to 110075314175 is exactly eight independent uniform digits from 0 to 23. Every die value rule is unchanged."},
    {"what": "The match-end leg closure is folded into the leg-end step as the condition exchange = 30", "why": "This gives the same scoring without needing a separate block of steps."},
    {"what": "Announced die values are kept in a per-exchange public list, revealed_values", "why": "Every reveal needs a stated piece of state."}
  ],
  "unsupported": []
}
```
````
