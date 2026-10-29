# 13 spec

- time: 2026-10-28T06:00:47+00:00 (63.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 891e9457cba83918, reply sha256 5fb446ea75f46262

## Sent

````
Game: Dungeon Dare
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
COMPONENTS.

Monster deck of 13 cards (name: strength):
- Goblin 1 (x2)
- Skeleton 2 (x2)
- Orc 3 (x2)
- Vampire 4 (x2)
- Golem 5 (x2)
- Lich 6 (x1)
- Demon 7 (x1)
- Dragon 9 (x1)

Adventurer base HP: 3.

Equipment (4 items, all present at the start of each dungeon):
- ARMOR: +4 HP.
- SHIELD: +3 HP.
- TORCH: defeats every monster of strength 3 or less.
- SPEAR: defeats every monster of strength 7 or more.

Each player has a point total starting at 0.

SEATS AND TURNS.
Seats are 1, 2 and 3. The game is played as a series of turns, at most 40. Turns are grouped into dungeons.

STARTING A DUNGEON.
1. At the start of each dungeon, shuffle all 13 monsters into a face-down deck. This shuffle is the only random event.
2. Return all 4 items to the adventurer.
3. Empty the dungeon pile and all players' set-aside piles.
4. Mark all three players as IN, and clear every player's 'added' mark.
5. The leader acts first. Dungeon 1 is led by seat 1, dungeon 2 by seat 2, dungeon 3 by seat 3, dungeon 4 by seat 1, and so on.
6. Turns then pass in seat order (1, 2, 3, 1, ...), skipping players who are OUT.

A TURN (for the active player, who is IN).
(a) Forced pass check: if the deck holds 2 or fewer cards, the active player must PASS this turn. Skip to (d).
(b) Draw: the active player privately looks at the top card of the deck. Only they see it.
(c) Talk: every player, in or out, writes one short message at the same time without seeing the others. Then all messages are shown to everyone. Messages bind no one and may be lies.
(d) Action: the active player chooses one option from this list, in this order, offering only the legal ones.
    - PASS: you become OUT for this dungeon. The card you drew, if any, goes back on top of the deck, unseen by others.
    - ADD: put the drawn monster face-down on the dungeon pile, and mark yourself as 'added' for this dungeon.
    - SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR: available only for items still present. Remove that item from the adventurer for this dungeon. Put the drawn monster face-down in your own set-aside pile; it is out of play and seen only by you. This does NOT mark you as 'added'.
(e) Announcement: everyone learns which option was chosen, which item was removed if any, and how many cards are in the dungeon pile. Nobody learns which monster was drawn.
(f) If exactly one player is still IN, that player becomes the RUNNER and the run happens now (see below). Otherwise the turn passes to the next IN player.

THE RUN.
1. The runner's HP = 3, +4 if ARMOR remains, +3 if SHIELD remains.
2. Reveal every card in the dungeon pile, then the top 2 cards of the deck. All of these are the monsters faced.
3. Each monster is defeated with no damage if TORCH remains and its strength is 3 or less, or if SPEAR remains and its strength is 7 or more. Otherwise it deals damage equal to its strength.
4. If total damage is less than HP, the run SUCCEEDS: the runner gains 2 points.
5. Otherwise the run FAILS:
    - The runner loses 1 point (never below 0).
    - Every OUT player who is marked 'added' for this dungeon gains 1 point.
6. All revealed cards are announced. The dungeon ends, and the next turn starts a new dungeon.

END OF GAME.
- After any run, if any player has 4 or more points, the game ends.
- The game also ends after turn 40, even mid-dungeon. An unfinished dungeon is not scored.

How the winner is decided: When the game ends, the player with the most points wins. If two or more players tie for the most points, the game is a draw.
````

## Reply

````
```json
{
  "name": "Dungeon Dare",
  "summary": "Three players push their luck through a shuffled monster deck. Each turn they add the monster they drew to a hidden dungeon, strip the adventurer of an item, or pass out; the last player left must survive the run.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "seats": 3,
    "deck_size": 13,
    "goblin_strength": 1, "goblin_count": 2,
    "skeleton_strength": 2, "skeleton_count": 2,
    "orc_strength": 3, "orc_count": 2,
    "vampire_strength": 4, "vampire_count": 2,
    "golem_strength": 5, "golem_count": 2,
    "lich_strength": 6, "lich_count": 1,
    "demon_strength": 7, "demon_count": 1,
    "dragon_strength": 9, "dragon_count": 1,
    "base_hp": 3,
    "armor_hp": 4,
    "shield_hp": 3,
    "torch_max_strength": 3,
    "spear_min_strength": 7,
    "item_count": 4,
    "forced_pass_deck_max": 2,
    "run_extra_cards": 2,
    "success_points": 2,
    "fail_penalty": 1,
    "added_bonus": 1,
    "points_floor": 0,
    "win_points": 4,
    "max_turns": 40,
    "starting_points": 0
  },
  "attributes": {
    "player": [
      {"key": "points", "type": "number", "visible": "public", "initial": 0, "meaning": "The player's point total.", "observable": true},
      {"key": "in_dungeon", "type": "bool", "visible": "public", "initial": true, "meaning": "True if the player is IN the current dungeon; false once they PASS (OUT).", "observable": true},
      {"key": "added", "type": "bool", "visible": "public", "initial": false, "meaning": "True if the player chose ADD at least once in the current dungeon. It is public because each chosen option is announced.", "observable": true},
      {"key": "drawn_card", "type": "list", "visible": "ally", "initial": [], "meaning": "The monster strength the player privately drew this turn (empty if none). Only the owner sees it.", "observable": false},
      {"key": "set_aside", "type": "list", "visible": "ally", "initial": [], "meaning": "Monsters this player removed with a sacrifice in the current dungeon. They are out of play and seen only by the owner.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down monster deck as an ordered list of strengths. The first element is the top card.", "observable": false},
      {"key": "dungeon_pile", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down monsters added to the dungeon this dungeon.", "observable": false},
      {"key": "dungeon_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the dungeon pile, as announced.", "observable": true},
      {"key": "armor", "type": "bool", "visible": "public", "initial": true, "meaning": "ARMOR still with the adventurer.", "observable": true},
      {"key": "shield", "type": "bool", "visible": "public", "initial": true, "meaning": "SHIELD still with the adventurer.", "observable": true},
      {"key": "torch", "type": "bool", "visible": "public", "initial": true, "meaning": "TORCH still with the adventurer.", "observable": true},
      {"key": "spear", "type": "bool", "visible": "public", "initial": true, "meaning": "SPEAR still with the adventurer.", "observable": true},
      {"key": "turn", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of turns started so far (at most 40).", "observable": true},
      {"key": "dungeon_number", "type": "number", "visible": "public", "initial": 0, "meaning": "Index of the current dungeon, starting at 1.", "observable": true},
      {"key": "leader_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that leads the current dungeon: ((dungeon_number - 1) mod 3) + 1.", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the player taking this turn.", "observable": false},
      {"key": "new_dungeon", "type": "bool", "visible": "none", "initial": true, "meaning": "Scratch flag: true when the next turn must start a new dungeon.", "observable": false},
      {"key": "forced_pass", "type": "bool", "visible": "public", "initial": false, "meaning": "True this turn if the deck held 2 or fewer cards at the start of the turn.", "observable": false},
      {"key": "last_action", "type": "text", "visible": "public", "initial": "", "meaning": "Option chosen by the active player this turn, as announced.", "observable": false},
      {"key": "in_count", "type": "number", "visible": "public", "initial": 3, "meaning": "Number of players still IN.", "observable": false},
      {"key": "runner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the runner when a run happens, else 0.", "observable": false},
      {"key": "faced", "type": "list", "visible": "public", "initial": [], "meaning": "Monsters revealed in the last run: the dungeon pile plus the top 2 deck cards.", "observable": true},
      {"key": "run_hp", "type": "number", "visible": "public", "initial": 0, "meaning": "Runner's HP in the last run.", "observable": false},
      {"key": "run_damage", "type": "number", "visible": "public", "initial": 0, "meaning": "Total damage taken in the last run.", "observable": false}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each start with points = 0.",
    "Set turn = 0, dungeon_number = 0 and new_dungeon = true, so the first turn starts dungeon 1 led by seat 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Applies only when new_dungeon is true. Set dungeon_number += 1 and leader_seat = ((dungeon_number - 1) mod 3) + 1. Set deck = the 13 strengths [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order; this seeded shuffle is the only random event. Set armor, shield, torch and spear = true. Set dungeon_pile = [] and dungeon_count = 0. For every player set set_aside = [], drawn_card = [], in_dungeon = true and added = false. Set in_count = 3, runner_seat = 0, active_seat = leader_seat and new_dungeon = false."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Set turn += 1. Set forced_pass = (length(deck) <= 2). If forced_pass is false, move the first element of deck into the active player's drawn_card; that player privately sees it."},
    {"action": "sync", "who": "the active player", "answer": null,
     "effect": "The active player is shown their drawn_card, unless forced_pass is true."},
    {"action": "poll", "who": "all players", "answer": "short text message",
     "effect": "Applies only when forced_pass is false. Every player, IN or OUT, writes one message at the same time. All are then broadcast as {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages bind no one."},
    {"action": "ask", "who": "the active player (seat active_seat)", "answer": "one of: PASS, ADD, SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR (only the legal ones, in this order)",
     "effect": "Sets last_action to the chosen option."},
    {"action": "update", "who": "the active player", "answer": null,
     "effect": "If last_action = PASS: set in_dungeon = false, in_count -= 1, and put drawn_card (if any) back as the first element of deck. If ADD: append drawn_card to dungeon_pile, set dungeon_count += 1 and added = true. If SACRIFICE_X: set item X = false and append drawn_card to the player's set_aside. In every case clear drawn_card."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Announce: 'Seat {active_seat} chose {last_action}. Dungeon pile: {dungeon_count} cards. Items left: armor {armor}, shield {shield}, torch {torch}, spear {spear}.' The drawn monster is not revealed."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Applies only when in_count = 1 (the run). Set runner_seat = the seat with in_dungeon = true. Set run_hp = 3 + 4*armor + 3*shield. Set faced = dungeon_pile + the first 2 elements of deck. Set run_damage = the sum over faced of strength s, except that s is counted as 0 if (torch and s <= 3) or (spear and s >= 7). If run_damage < run_hp, the runner gets points += 2. Otherwise the runner gets points = max(0, points - 1), and every player with in_dungeon = false and added = true gets points += 1. Set new_dungeon = true."},
    {"action": "tell", "who": "all players", "answer": null,
     "effect": "Applies only when a run happened this turn. Announce: 'Seat {runner_seat} ran: monsters {faced}, HP {run_hp}, damage {run_damage}.' Then announce success or failure and the new points."},
    {"action": "update", "who": "all players", "answer": null,
     "effect": "Applies only when new_dungeon is false. Set active_seat = the next seat after active_seat in the order 1, 2, 3, 1, ... that has in_dungeon = true."},
    {"action": "check", "who": "all players", "answer": null,
     "effect": "End the game if (a run happened this turn and some player has points >= 4) or turn >= 40. Otherwise run the next turn."}
  ],
  "ending": {
    "condition": "(new_dungeon = true and max over players of points >= 4) or turn >= 40",
    "rank_by": "you.points",
    "decided_by": "Each player's standing is their point total; the most points wins. Players tied for the most share the result, which the source calls a draw."
  },
  "rules": [
    {"id": "R1", "text": "When a dungeon starts, then the deck is set to the 13 monsters [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order, all 4 items are present, the dungeon pile and all set-aside piles are empty, all 3 players are IN and no player is marked added."},
    {"id": "R2", "text": "When dungeon number d starts, then its leader is seat ((d - 1) mod 3) + 1 and that seat takes the first turn (dungeon 1: seat 1, dungeon 2: seat 2, dungeon 4: seat 1)."},
    {"id": "R3", "text": "When a turn ends without a run, then the next active seat is the next seat in the order 1, 2, 3, 1 that is still IN, skipping OUT seats."},
    {"id": "R4", "text": "When the deck holds 2 or fewer cards at the start of a turn, then the active player draws nothing, there is no talk, and PASS is the only option offered."},
    {"id": "R5", "text": "When the deck holds 3 or more cards at the start of a turn, then the active player privately receives the top card of the deck in drawn_card, and no one else sees it."},
    {"id": "R6", "text": "When the active player has drawn, then every player, IN or OUT, submits one message simultaneously, and all messages are shown to everyone afterwards."},
    {"id": "R7", "text": "When the active player chooses PASS, then they become OUT (in_dungeon = false) and any drawn card returns to the top of the deck."},
    {"id": "R8", "text": "When the active player chooses ADD, then the drawn card is appended to the dungeon pile, dungeon_count increases by 1, and the player is marked added = true."},
    {"id": "R9", "text": "When the active player chooses SACRIFICE_X for an item X still present, then X is removed for this dungeon, the drawn card goes to that player's set_aside, and added is not changed."},
    {"id": "R10", "text": "When an item has been removed this dungeon, then its SACRIFICE option is not offered."},
    {"id": "R11", "text": "When an action is taken, then everyone is told the option chosen, any item removed and the dungeon pile count, but not the drawn monster."},
    {"id": "R12", "text": "When exactly one player is IN after an action, then that player is the runner and the run happens immediately."},
    {"id": "R13", "text": "When a run happens, then the runner's HP is 3, plus 4 if ARMOR remains, plus 3 if SHIELD remains (maximum 10)."},
    {"id": "R14", "text": "When a run happens, then the monsters faced are every card in the dungeon pile plus the top 2 cards of the deck, and all of them are announced."},
    {"id": "R15", "text": "When a faced monster has strength 3 or less and TORCH remains, or strength 7 or more and SPEAR remains, then it deals 0 damage; otherwise it deals damage equal to its strength."},
    {"id": "R16", "text": "When total damage is less than the runner's HP, then the run succeeds and the runner gains 2 points."},
    {"id": "R17", "text": "When total damage is at least the runner's HP, then the run fails and the runner loses 1 point, never going below 0."},
    {"id": "R18", "text": "When a run fails, then every OUT player marked added gains 1 point."},
    {"id": "R19", "text": "When a run ends, then the dungeon ends and the next turn starts a new dungeon."},
    {"id": "R20", "text": "When, after a run, any player has 4 or more points, then the game ends."},
    {"id": "R21", "text": "When turn 40 has been played, then the game ends, even mid-dungeon, and the unfinished dungeon is not scored."},
    {"id": "R22", "text": "When the game ends, then the player with the most points wins, and players tied for the most share the result."}
  ],
  "offers": [
    {"question": "Talk message each turn", "who": "all three seats, IN or OUT, only when the active player drew a card", "options": "free short text"},
    {"question": "Action of the active player", "who": "the active seat only", "options": "If the deck held 2 or fewer cards at the start of the turn: PASS only. Otherwise: PASS, ADD, then SACRIFICE_ARMOR if armor remains, SACRIFICE_SHIELD if shield remains, SACRIFICE_TORCH if torch remains, SACRIFICE_SPEAR if spear remains."}
  ],
  "choices": [
    {"what": "3 players (min 3, max 3, suggested 3)", "why": "The designer fixed 3. Leadership rotation and the push-your-luck tension are built around three seats. With more seats each player's added bet matters less and turns run long; with two, the first pass ends the dungeon at once."},
    {"what": "Talk kept as a simultaneous poll each drawing turn", "why": "The rules require a simultaneous message from every player. Players disagree, since each wants the others to pass or to run a deadly dungeon, so bluffing about the drawn card carries real strategic weight."},
    {"what": "Deck as an ordered list shuffled once per dungeon; draws take the first element", "why": "This honors 'top card', the card returned on top after a PASS, and 'top 2 cards' in the run, with the shuffle as the only random event."},
    {"what": "Monsters stored by strength only", "why": "Names carry no rule effect; strength alone decides damage, TORCH and SPEAR."},
    {"what": "Talk is skipped on a forced pass", "why": "The rules send a forced pass straight from step (a) to step (d), skipping the talk in (c)."}
  ],
  "simplifications": [
    {"what": "A tie for most points is reported as a shared win rather than a draw", "why": "The engine ranks by one expression and players level at the top share the win; this is equivalent to the source's draw."},
    {"what": "Dungeon reset, run and turn advance are single steps gated by arithmetic conditions", "why": "The step list is flat, so each block is expressed as conditional updates within one round."}
  ],
  "unsupported": []
}
```
````
