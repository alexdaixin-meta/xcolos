# 15 scenarios

- time: 2026-10-28T06:03:14+00:00 (59.1s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 60c2492094b13c94, reply sha256 659b64d909878c7f

## Sent

````
SPEC:
{
  "name": "Dungeon Dare",
  "summary": "Three players push their luck through a shuffled monster deck. Each turn they add the monster they drew to a hidden dungeon, strip the adventurer of an item, or pass out; the last player left must survive the run.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "seats": 3,
    "deck_size": 13,
    "goblin_strength": 1,
    "goblin_count": 2,
    "skeleton_strength": 2,
    "skeleton_count": 2,
    "orc_strength": 3,
    "orc_count": 2,
    "vampire_strength": 4,
    "vampire_count": 2,
    "golem_strength": 5,
    "golem_count": 2,
    "lich_strength": 6,
    "lich_count": 1,
    "demon_strength": 7,
    "demon_count": 1,
    "dragon_strength": 9,
    "dragon_count": 1,
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
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's point total.",
        "observable": true
      },
      {
        "key": "in_dungeon",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "True if the player is IN the current dungeon; false once they PASS (OUT).",
        "observable": true
      },
      {
        "key": "added",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True if the player chose ADD at least once in the current dungeon. It is public because each chosen option is announced.",
        "observable": true
      },
      {
        "key": "drawn_card",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The monster strength the player privately drew this turn (empty if none). Only the owner sees it.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Monsters this player removed with a sacrifice in the current dungeon. They are out of play and seen only by the owner.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down monster deck as an ordered list of strengths. The first element is the top card.",
        "observable": false
      },
      {
        "key": "dungeon_pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down monsters added to the dungeon this dungeon.",
        "observable": false
      },
      {
        "key": "dungeon_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the dungeon pile, as announced.",
        "observable": true
      },
      {
        "key": "armor",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "ARMOR still with the adventurer.",
        "observable": true
      },
      {
        "key": "shield",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "SHIELD still with the adventurer.",
        "observable": true
      },
      {
        "key": "torch",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "TORCH still with the adventurer.",
        "observable": true
      },
      {
        "key": "spear",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "SPEAR still with the adventurer.",
        "observable": true
      },
      {
        "key": "turn",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of turns started so far (at most 40).",
        "observable": true
      },
      {
        "key": "dungeon_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Index of the current dungeon, starting at 1.",
        "observable": true
      },
      {
        "key": "leader_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that leads the current dungeon: ((dungeon_number - 1) mod 3) + 1.",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the player taking this turn.",
        "observable": false
      },
      {
        "key": "new_dungeon",
        "type": "bool",
        "visible": "none",
        "initial": true,
        "meaning": "Scratch flag: true when the next turn must start a new dungeon.",
        "observable": false
      },
      {
        "key": "forced_pass",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True this turn if the deck held 2 or fewer cards at the start of the turn.",
        "observable": false
      },
      {
        "key": "last_action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Option chosen by the active player this turn, as announced.",
        "observable": false
      },
      {
        "key": "in_count",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Number of players still IN.",
        "observable": false
      },
      {
        "key": "runner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the runner when a run happens, else 0.",
        "observable": false
      },
      {
        "key": "faced",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Monsters revealed in the last run: the dungeon pile plus the top 2 deck cards.",
        "observable": true
      },
      {
        "key": "run_hp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Runner's HP in the last run.",
        "observable": false
      },
      {
        "key": "run_damage",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total damage taken in the last run.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each start with points = 0.",
    "Set turn = 0, dungeon_number = 0 and new_dungeon = true, so the first turn starts dungeon 1 led by seat 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Applies only when new_dungeon is true. Set dungeon_number += 1 and leader_seat = ((dungeon_number - 1) mod 3) + 1. Set deck = the 13 strengths [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order; this seeded shuffle is the only random event. Set armor, shield, torch and spear = true. Set dungeon_pile = [] and dungeon_count = 0. For every player set set_aside = [], drawn_card = [], in_dungeon = true and added = false. Set in_count = 3, runner_seat = 0, active_seat = leader_seat and new_dungeon = false."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set turn += 1. Set forced_pass = (length(deck) <= 2). If forced_pass is false, move the first element of deck into the active player's drawn_card; that player privately sees it."
    },
    {
      "action": "sync",
      "who": "the active player",
      "answer": null,
      "effect": "The active player is shown their drawn_card, unless forced_pass is true."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Applies only when forced_pass is false. Every player, IN or OUT, writes one message at the same time. All are then broadcast as {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages bind no one."
    },
    {
      "action": "ask",
      "who": "the active player (seat active_seat)",
      "answer": "one of: PASS, ADD, SACRIFICE_ARMOR, SACRIFICE_SHIELD, SACRIFICE_TORCH, SACRIFICE_SPEAR (only the legal ones, in this order)",
      "effect": "Sets last_action to the chosen option."
    },
    {
      "action": "update",
      "who": "the active player",
      "answer": null,
      "effect": "If last_action = PASS: set in_dungeon = false, in_count -= 1, and put drawn_card (if any) back as the first element of deck. If ADD: append drawn_card to dungeon_pile, set dungeon_count += 1 and added = true. If SACRIFICE_X: set item X = false and append drawn_card to the player's set_aside. In every case clear drawn_card."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {active_seat} chose {last_action}. Dungeon pile: {dungeon_count} cards. Items left: armor {armor}, shield {shield}, torch {torch}, spear {spear}.' The drawn monster is not revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Applies only when in_count = 1 (the run). Set runner_seat = the seat with in_dungeon = true. Set run_hp = 3 + 4*armor + 3*shield. Set faced = dungeon_pile + the first 2 elements of deck. Set run_damage = the sum over faced of strength s, except that s is counted as 0 if (torch and s <= 3) or (spear and s >= 7). If run_damage < run_hp, the runner gets points += 2. Otherwise the runner gets points = max(0, points - 1), and every player with in_dungeon = false and added = true gets points += 1. Set new_dungeon = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Applies only when a run happened this turn. Announce: 'Seat {runner_seat} ran: monsters {faced}, HP {run_hp}, damage {run_damage}.' Then announce success or failure and the new points."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Applies only when new_dungeon is false. Set active_seat = the next seat after active_seat in the order 1, 2, 3, 1, ... that has in_dungeon = true."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if (a run happened this turn and some player has points >= 4) or turn >= 40. Otherwise run the next turn."
    }
  ],
  "ending": {
    "condition": "(new_dungeon = true and max over players of points >= 4) or turn >= 40",
    "rank_by": "you.points",
    "decided_by": "Each player's standing is their point total; the most points wins. Players tied for the most share the result, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a dungeon starts, then the deck is set to the 13 monsters [1,1,2,2,3,3,4,4,5,5,6,7,9] in a random order, all 4 items are present, the dungeon pile and all set-aside piles are empty, all 3 players are IN and no player is marked added."
    },
    {
      "id": "R2",
      "text": "When dungeon number d starts, then its leader is seat ((d - 1) mod 3) + 1 and that seat takes the first turn (dungeon 1: seat 1, dungeon 2: seat 2, dungeon 4: seat 1)."
    },
    {
      "id": "R3",
      "text": "When a turn ends without a run, then the next active seat is the next seat in the order 1, 2, 3, 1 that is still IN, skipping OUT seats."
    },
    {
      "id": "R4",
      "text": "When the deck holds 2 or fewer cards at the start of a turn, then the active player draws nothing, there is no talk, and PASS is the only option offered."
    },
    {
      "id": "R5",
      "text": "When the deck holds 3 or more cards at the start of a turn, then the active player privately receives the top card of the deck in drawn_card, and no one else sees it."
    },
    {
      "id": "R6",
      "text": "When the active player has drawn, then every player, IN or OUT, submits one message simultaneously, and all messages are shown to everyone afterwards."
    },
    {
      "id": "R7",
      "text": "When the active player chooses PASS, then they become OUT (in_dungeon = false) and any drawn card returns to the top of the deck."
    },
    {
      "id": "R8",
      "text": "When the active player chooses ADD, then the drawn card is appended to the dungeon pile, dungeon_count increases by 1, and the player is marked added = true."
    },
    {
      "id": "R9",
      "text": "When the active player chooses SACRIFICE_X for an item X still present, then X is removed for this dungeon, the drawn card goes to that player's set_aside, and added is not changed."
    },
    {
      "id": "R10",
      "text": "When an item has been removed this dungeon, then its SACRIFICE option is not offered."
    },
    {
      "id": "R11",
      "text": "When an action is taken, then everyone is told the option chosen, any item removed and the dungeon pile count, but not the drawn monster."
    },
    {
      "id": "R12",
      "text": "When exactly one player is IN after an action, then that player is the runner and the run happens immediately."
    },
    {
      "id": "R13",
      "text": "When a run happens, then the runner's HP is 3, plus 4 if ARMOR remains, plus 3 if SHIELD remains (maximum 10)."
    },
    {
      "id": "R14",
      "text": "When a run happens, then the monsters faced are every card in the dungeon pile plus the top 2 cards of the deck, and all of them are announced."
    },
    {
      "id": "R15",
      "text": "When a faced monster has strength 3 or less and TORCH remains, or strength 7 or more and SPEAR remains, then it deals 0 damage; otherwise it deals damage equal to its strength."
    },
    {
      "id": "R16",
      "text": "When total damage is less than the runner's HP, then the run succeeds and the runner gains 2 points."
    },
    {
      "id": "R17",
      "text": "When total damage is at least the runner's HP, then the run fails and the runner loses 1 point, never going below 0."
    },
    {
      "id": "R18",
      "text": "When a run fails, then every OUT player marked added gains 1 point."
    },
    {
      "id": "R19",
      "text": "When a run ends, then the dungeon ends and the next turn starts a new dungeon."
    },
    {
      "id": "R20",
      "text": "When, after a run, any player has 4 or more points, then the game ends."
    },
    {
      "id": "R21",
      "text": "When turn 40 has been played, then the game ends, even mid-dungeon, and the unfinished dungeon is not scored."
    },
    {
      "id": "R22",
      "text": "When the game ends, then the player with the most points wins, and players tied for the most share the result."
    }
  ],
  "offers": [
    {
      "question": "Talk message each turn",
      "who": "all three seats, IN or OUT, only when the active player drew a card",
      "options": "free short text"
    },
    {
      "question": "Action of the active player",
      "who": "the active seat only",
      "options": "If the deck held 2 or fewer cards at the start of the turn: PASS only. Otherwise: PASS, ADD, then SACRIFICE_ARMOR if armor remains, SACRIFICE_SHIELD if shield remains, SACRIFICE_TORCH if torch remains, SACRIFICE_SPEAR if spear remains."
    }
  ],
  "choices": [
    {
      "what": "3 players (min 3, max 3, suggested 3)",
      "why": "The designer fixed 3. Leadership rotation and the push-your-luck tension are built around three seats. With more seats each player's added bet matters less and turns run long; with two, the first pass ends the dungeon at once."
    },
    {
      "what": "Talk kept as a simultaneous poll each drawing turn",
      "why": "The rules require a simultaneous message from every player. Players disagree, since each wants the others to pass or to run a deadly dungeon, so bluffing about the drawn card carries real strategic weight."
    },
    {
      "what": "Deck as an ordered list shuffled once per dungeon; draws take the first element",
      "why": "This honors 'top card', the card returned on top after a PASS, and 'top 2 cards' in the run, with the shuffle as the only random event."
    },
    {
      "what": "Monsters stored by strength only",
      "why": "Names carry no rule effect; strength alone decides damage, TORCH and SPEAR."
    },
    {
      "what": "Talk is skipped on a forced pass",
      "why": "The rules send a forced pass straight from step (a) to step (d), skipping the talk in (c)."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for most points is reported as a shared win rather than a draw",
      "why": "The engine ranks by one expression and players level at the top share the win; this is equivalent to the source's draw."
    },
    {
      "what": "Dungeon reset, run and turn advance are single steps gated by arithmetic conditions",
      "why": "The step list is flat, so each block is expressed as conditional updates within one round."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: points, in_dungeon, added; table: dungeon_count, armor, shield, torch, spear, turn, dungeon_number, faced.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"R1 a new dungeon resets deck, items, piles and player flags","rule":"R1","players":3,"seed":1,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":1,"torch":false,"spear":false,"armor":false,"dungeon_pile":[3],"dungeon_count":1,"deck":[4]},
          "players":{"2":{"added":true,"in_dungeon":false,"set_aside":[5]},"1":{"in_dungeon":false},"3":{"added":true}}},
 "expect":{"game":{"dungeon_number":2,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0},
           "players":{"1":{"in_dungeon":true,"added":false},"2":{"in_dungeon":false,"added":false},"3":{"in_dungeon":true,"added":false}},
           "lens":{"game":{"deck":13,"dungeon_pile":0},"players":{"1":{"set_aside":0},"2":{"set_aside":0},"3":{"set_aside":0}}},
           "offered":[{"seat":2,"option":"PASS"}]}},
{"name":"R1 first turn of the match starts dungeon 1 with a full deck","rule":"R1","players":3,"seed":2,"default":"decline","rounds":1,
 "expect":{"game":{"dungeon_number":1,"turn":1,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0},
           "players":{"1":{"in_dungeon":false,"added":false},"2":{"in_dungeon":true,"added":false},"3":{"in_dungeon":true,"added":false}},
           "lens":{"game":{"deck":13,"dungeon_pile":0}}}},
{"name":"R2 dungeon 2 is led by seat 2","rule":"R2","players":3,"seed":3,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":1}},
 "expect":{"game":{"dungeon_number":2},"players":{"1":{"in_dungeon":true},"2":{"in_dungeon":false},"3":{"in_dungeon":true}},
           "offered":[{"seat":2,"option":"PASS"}],"not_offered":[{"seat":1,"option":"PASS"},{"seat":3,"option":"PASS"}]}},
{"name":"R2 dungeon 4 is led by seat 1","rule":"R2","players":3,"seed":4,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":3}},
 "expect":{"game":{"dungeon_number":4},"players":{"1":{"in_dungeon":false},"2":{"in_dungeon":true},"3":{"in_dungeon":true}},
           "offered":[{"seat":1,"option":"PASS"}],"not_offered":[{"seat":2,"option":"PASS"},{"seat":3,"option":"PASS"}]}},
{"name":"R3 the turn passes from seat 1 to seat 3, skipping OUT seat 2","rule":"R3","players":3,"seed":5,"default":"decline","rounds":2,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4,5,6],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"2":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"ADD"},{"seat":3,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":2,"turn":5},"players":{"1":{"added":true},"2":{"in_dungeon":false,"added":false},"3":{"added":true,"in_dungeon":true}},
           "not_offered":[{"seat":2,"option":"PASS"}]}},
{"name":"R4 with 2 cards in the deck only PASS is offered and nothing is drawn","rule":"R4","players":3,"seed":6,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[5,6],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "expect":{"players":{"1":{"in_dungeon":false}},"lens":{"game":{"deck":2}},
           "offered":[{"seat":1,"option":"PASS"}],"not_offered":[{"seat":1,"option":"ADD"},{"seat":1,"option":"SACRIFICE_ARMOR"}]}},
{"name":"R5 with 3 or more cards the active player draws the top card","rule":"R5","players":3,"seed":7,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":1},"lens":{"game":{"deck":4,"dungeon_pile":1}},"offered":[{"seat":1,"option":"ADD"}]}},
{"name":"R6 a drawing turn with an OUT seat runs its talk and continues normally","rule":"R6","players":3,"seed":8,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":1,"turn":4},"players":{"1":{"added":true},"3":{"in_dungeon":false}}}},
{"name":"R7 PASS makes the player OUT and returns the drawn card to the deck","rule":"R7","players":3,"seed":9,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"1":{"in_dungeon":false,"added":false},"2":{"in_dungeon":true},"3":{"in_dungeon":true}},"game":{"dungeon_count":0},
           "lens":{"game":{"deck":5,"dungeon_pile":0}}}},
{"name":"R8 ADD puts the drawn card in the dungeon and marks the player","rule":"R8","players":3,"seed":10,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[2],"dungeon_count":1,"turn":3}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"players":{"1":{"added":true,"in_dungeon":true}},"game":{"dungeon_count":2},"lens":{"game":{"deck":4,"dungeon_pile":2}}}},
{"name":"R9 SACRIFICE_TORCH removes the torch and sets the card aside without marking added","rule":"R9","players":3,"seed":11,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"SACRIFICE_TORCH"}],
 "expect":{"players":{"1":{"added":false,"in_dungeon":true}},"game":{"torch":false,"armor":true,"shield":true,"spear":true,"dungeon_count":0},
           "lens":{"game":{"deck":4,"dungeon_pile":0},"players":{"1":{"set_aside":1}}}}},
{"name":"R10 a removed item's sacrifice is not offered","rule":"R10","players":3,"seed":12,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3,"torch":false,"armor":false}},
 "expect":{"offered":[{"seat":1,"option":"SACRIFICE_SHIELD"},{"seat":1,"option":"SACRIFICE_SPEAR"}],
           "not_offered":[{"seat":1,"option":"SACRIFICE_TORCH"},{"seat":1,"option":"SACRIFICE_ARMOR"}]}},
{"name":"R11 a sacrifice is shown in the public item state and the pile count is unchanged","rule":"R11","players":3,"seed":13,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[3],"dungeon_count":1,"turn":4}},
 "rules":[{"seat":1,"options_include":"SACRIFICE_SHIELD"}],
 "expect":{"game":{"shield":false,"armor":true,"torch":true,"spear":true,"dungeon_count":1,"turn":5}}},
{"name":"R12 when only one player is left IN that player runs at once","rule":"R12","players":3,"seed":14,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4,5],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[1,2]},"players":{"1":{"points":0,"in_dungeon":false},"2":{"points":2},"3":{"points":0}}}},
{"name":"R13 HP is 6 without armor: damage 5 succeeds","rule":"R13","players":3,"seed":15,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,9,3,3],"dungeon_pile":[4],"dungeon_count":1,"turn":3,"armor":false,"torch":false},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[4,1,9]},"players":{"2":{"points":2}}}},
{"name":"R13 HP is 7 without shield: damage 7 fails","rule":"R13","players":3,"seed":16,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[2,9,3,3],"dungeon_pile":[5],"dungeon_count":1,"turn":3,"shield":false,"torch":false},
          "players":{"2":{"points":2},"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[5,2,9]},"players":{"1":{"points":0},"2":{"points":1},"3":{"points":0}}}},
{"name":"R14 the faced monsters are the dungeon pile plus the top 2 deck cards","rule":"R14","players":3,"seed":17,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[3,5,7,1],"dungeon_pile":[6,4],"dungeon_count":2,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[6,4,3,5]},"lens":{"game":{"faced":4}},"players":{"2":{"points":0}}}},
{"name":"R15 torch and spear cancel weak and strong monsters","rule":"R15","players":3,"seed":18,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[9,2,4,4],"dungeon_pile":[3,7],"dungeon_count":2,"turn":3,"armor":false,"shield":false},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[3,7,9,2]},"players":{"2":{"points":2}}}},
{"name":"R15 without torch weak monsters deal their strength","rule":"R15","players":3,"seed":19,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,1,4,4],"dungeon_pile":[1],"dungeon_count":1,"turn":3,"armor":false,"shield":false,"torch":false,"spear":false},
          "players":{"2":{"points":1},"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[1,1,1]},"players":{"2":{"points":0}}}},
{"name":"R16 a successful run gives the runner 2 points","rule":"R16","players":3,"seed":20,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"2":{"points":1},"3":{"in_dungeon":false}}},
 "expect":{"players":{"1":{"points":0},"2":{"points":3},"3":{"points":0}}}},
{"name":"R17 a failed run costs the runner 1 point","rule":"R17","players":3,"seed":21,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"2":{"points":3},"3":{"in_dungeon":false}}},
 "expect":{"game":{"faced":[4,5,6]},"players":{"1":{"points":0},"2":{"points":2},"3":{"points":0}}}},
{"name":"R17 a failed run at 0 points stays at 0","rule":"R17","players":3,"seed":22,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"players":{"2":{"points":0}}}},
{"name":"R18 on a failed run OUT players who added gain 1 point","rule":"R18","players":3,"seed":23,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"1":{"added":true},"2":{"points":1},"3":{"in_dungeon":false,"added":false,"points":1}}},
 "expect":{"players":{"1":{"points":1},"2":{"points":0},"3":{"points":1}}}},
{"name":"R19 after a run the next turn starts a new dungeon","rule":"R19","players":3,"seed":24,"default":"decline","rounds":2,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":3,"torch":true,"armor":false},
          "players":{"3":{"in_dungeon":false}}},
 "expect":{"game":{"dungeon_number":2,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0,"turn":5},
           "players":{"1":{"in_dungeon":true,"points":0},"2":{"in_dungeon":false,"points":2},"3":{"in_dungeon":true,"points":0}},
           "lens":{"game":{"deck":13}}}},
{"name":"R20 a run that brings a player to 4 points ends the game","rule":"R20","players":3,"seed":25,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":5},
          "players":{"2":{"points":2},"3":{"in_dungeon":false}}},
 "expect":{"winner":2,"standings":{"1":0,"2":4,"3":0},"game":{"turn":6}}},
{"name":"R21 the game ends after turn 40 even mid-dungeon","rule":"R21","players":3,"seed":26,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":5,"leader_seat":2,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":39},
          "players":{"1":{"points":3},"2":{"points":1}}},
 "expect":{"winner":1,"standings":{"1":3,"2":1,"3":0},"game":{"turn":40}}},
{"name":"R22 players tied for the most points share the win","rule":"R22","players":3,"seed":27,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":5,"leader_seat":2,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":39},
          "players":{"1":{"points":2},"2":{"points":2},"3":{"points":1}}},
 "expect":{"winner":[1,2],"standings":{"1":2,"2":2,"3":1}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name); scenario 26: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"R1 a new dungeon resets deck, items, piles and player flags","rule":"R1","players":3,"seed":1,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":1,"torch":false,"spear":false,"armor":false,"dungeon_pile":[3],"dungeon_count":1,"deck":[4]},
          "players":{"2":{"added":true,"in_dungeon":false,"set_aside":[5]},"1":{"in_dungeon":false},"3":{"added":true}}},
 "rules":[{"seat":2,"options_include":"PASS"}],
 "expect":{"game":{"dungeon_number":2,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0},
           "players":{"1":{"in_dungeon":true,"added":false},"2":{"in_dungeon":false,"added":false},"3":{"in_dungeon":true,"added":false}},
           "lens":{"game":{"deck":13,"dungeon_pile":0},"players":{"1":{"set_aside":0},"2":{"set_aside":0},"3":{"set_aside":0}}},
           "offered":[{"seat":2,"option":"PASS"}]}},
{"name":"R1 first turn of the match starts dungeon 1 with a full deck","rule":"R1","players":3,"seed":2,"default":"decline","rounds":1,
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"dungeon_number":1,"turn":1,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0},
           "players":{"1":{"in_dungeon":false,"added":false},"2":{"in_dungeon":true,"added":false},"3":{"in_dungeon":true,"added":false}},
           "lens":{"game":{"deck":13,"dungeon_pile":0}}}},
{"name":"R2 dungeon 2 is led by seat 2","rule":"R2","players":3,"seed":3,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":1}},
 "rules":[{"seat":2,"options_include":"PASS"}],
 "expect":{"game":{"dungeon_number":2},"players":{"1":{"in_dungeon":true},"2":{"in_dungeon":false},"3":{"in_dungeon":true}},
           "offered":[{"seat":2,"option":"PASS"}],"not_offered":[{"seat":1,"option":"PASS"},{"seat":3,"option":"PASS"}]}},
{"name":"R2 dungeon 4 is led by seat 1","rule":"R2","players":3,"seed":4,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":true,"dungeon_number":3}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"dungeon_number":4},"players":{"1":{"in_dungeon":false},"2":{"in_dungeon":true},"3":{"in_dungeon":true}},
           "offered":[{"seat":1,"option":"PASS"}],"not_offered":[{"seat":2,"option":"PASS"},{"seat":3,"option":"PASS"}]}},
{"name":"R3 the turn passes from seat 1 to seat 3, skipping OUT seat 2","rule":"R3","players":3,"seed":5,"default":"decline","rounds":2,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4,5,6],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"2":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"ADD"},{"seat":3,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":2,"turn":5},"players":{"1":{"added":true},"2":{"in_dungeon":false,"added":false},"3":{"added":true,"in_dungeon":true}},
           "not_offered":[{"seat":2,"option":"PASS"}]}},
{"name":"R4 with 2 cards in the deck only PASS is offered and nothing is drawn","rule":"R4","players":3,"seed":6,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[5,6],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"1":{"in_dungeon":false}},"lens":{"game":{"deck":2}},
           "offered":[{"seat":1,"option":"PASS"}],"not_offered":[{"seat":1,"option":"ADD"},{"seat":1,"option":"SACRIFICE_ARMOR"}]}},
{"name":"R5 with 3 or more cards the active player draws the top card","rule":"R5","players":3,"seed":7,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":1},"lens":{"game":{"deck":4,"dungeon_pile":1}},"offered":[{"seat":1,"option":"ADD"}]}},
{"name":"R6 a drawing turn with an OUT seat runs its talk and continues normally","rule":"R6","players":3,"seed":8,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"game":{"dungeon_count":1,"turn":4},"players":{"1":{"added":true},"3":{"in_dungeon":false}}}},
{"name":"R7 PASS makes the player OUT and returns the drawn card to the deck","rule":"R7","players":3,"seed":9,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"1":{"in_dungeon":false,"added":false},"2":{"in_dungeon":true},"3":{"in_dungeon":true}},"game":{"dungeon_count":0},
           "lens":{"game":{"deck":5,"dungeon_pile":0}}}},
{"name":"R8 ADD puts the drawn card in the dungeon and marks the player","rule":"R8","players":3,"seed":10,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[2],"dungeon_count":1,"turn":3}},
 "rules":[{"seat":1,"options_include":"ADD"}],
 "expect":{"players":{"1":{"added":true,"in_dungeon":true}},"game":{"dungeon_count":2},"lens":{"game":{"deck":4,"dungeon_pile":2}}}},
{"name":"R9 SACRIFICE_TORCH removes the torch and sets the card aside without marking added","rule":"R9","players":3,"seed":11,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3}},
 "rules":[{"seat":1,"options_include":"SACRIFICE_TORCH"}],
 "expect":{"players":{"1":{"added":false,"in_dungeon":true}},"game":{"torch":false,"armor":true,"shield":true,"spear":true,"dungeon_count":0},
           "lens":{"game":{"deck":4,"dungeon_pile":0},"players":{"1":{"set_aside":1}}}}},
{"name":"R10 a removed item's sacrifice is not offered","rule":"R10","players":3,"seed":12,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":3,"torch":false,"armor":false}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"offered":[{"seat":1,"option":"SACRIFICE_SHIELD"},{"seat":1,"option":"SACRIFICE_SPEAR"}],
           "not_offered":[{"seat":1,"option":"SACRIFICE_TORCH"},{"seat":1,"option":"SACRIFICE_ARMOR"}]}},
{"name":"R11 a sacrifice is shown in the public item state and the pile count is unchanged","rule":"R11","players":3,"seed":13,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[3],"dungeon_count":1,"turn":4}},
 "rules":[{"seat":1,"options_include":"SACRIFICE_SHIELD"}],
 "expect":{"game":{"shield":false,"armor":true,"torch":true,"spear":true,"dungeon_count":1,"turn":5}}},
{"name":"R12 when only one player is left IN that player runs at once","rule":"R12","players":3,"seed":14,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4,5],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[1,2]},"players":{"1":{"points":0,"in_dungeon":false},"2":{"points":2},"3":{"points":0}}}},
{"name":"R13 HP is 6 without armor: damage 5 succeeds","rule":"R13","players":3,"seed":15,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,9,3,3],"dungeon_pile":[4],"dungeon_count":1,"turn":3,"armor":false,"torch":false},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[4,1,9]},"players":{"2":{"points":2}}}},
{"name":"R13 HP is 7 without shield: damage 7 fails","rule":"R13","players":3,"seed":16,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[2,9,3,3],"dungeon_pile":[5],"dungeon_count":1,"turn":3,"shield":false,"torch":false},
          "players":{"2":{"points":2},"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[5,2,9]},"players":{"1":{"points":0},"2":{"points":1},"3":{"points":0}}}},
{"name":"R14 the faced monsters are the dungeon pile plus the top 2 deck cards","rule":"R14","players":3,"seed":17,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[3,5,7,1],"dungeon_pile":[6,4],"dungeon_count":2,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[6,4,3,5]},"lens":{"game":{"faced":4}},"players":{"2":{"points":0}}}},
{"name":"R15 torch and spear cancel weak and strong monsters","rule":"R15","players":3,"seed":18,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[9,2,4,4],"dungeon_pile":[3,7],"dungeon_count":2,"turn":3,"armor":false,"shield":false},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[3,7,9,2]},"players":{"2":{"points":2}}}},
{"name":"R15 without torch weak monsters deal their strength","rule":"R15","players":3,"seed":19,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,1,4,4],"dungeon_pile":[1],"dungeon_count":1,"turn":3,"armor":false,"shield":false,"torch":false,"spear":false},
          "players":{"2":{"points":1},"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[1,1,1]},"players":{"2":{"points":0}}}},
{"name":"R16 a successful run gives the runner 2 points","rule":"R16","players":3,"seed":20,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":3},
          "players":{"2":{"points":1},"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"1":{"points":0},"2":{"points":3},"3":{"points":0}}}},
{"name":"R17 a failed run costs the runner 1 point","rule":"R17","players":3,"seed":21,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"2":{"points":3},"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"game":{"faced":[4,5,6]},"players":{"1":{"points":0},"2":{"points":2},"3":{"points":0}}}},
{"name":"R17 a failed run at 0 points stays at 0","rule":"R17","players":3,"seed":22,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"2":{"points":0}}}},
{"name":"R18 on a failed run OUT players who added gain 1 point","rule":"R18","players":3,"seed":23,"default":"decline","rounds":1,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[5,6,1,1],"dungeon_pile":[4],"dungeon_count":1,"turn":3},
          "players":{"1":{"added":true},"2":{"points":1},"3":{"in_dungeon":false,"added":false,"points":1}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"players":{"1":{"points":1},"2":{"points":0},"3":{"points":1}}}},
{"name":"R19 after a run the next turn starts a new dungeon","rule":"R19","players":3,"seed":24,"default":"decline","rounds":2,
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":3,"torch":true,"armor":false},
          "players":{"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"}],
 "expect":{"game":{"dungeon_number":2,"armor":true,"shield":true,"torch":true,"spear":true,"dungeon_count":0,"turn":5},
           "players":{"1":{"in_dungeon":true,"points":0},"2":{"in_dungeon":false,"points":2},"3":{"in_dungeon":true,"points":0}},
           "lens":{"game":{"deck":13}}}},
{"name":"R20 a run that brings a player to 4 points ends the game","rule":"R20","players":3,"seed":25,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":1,"leader_seat":1,"active_seat":1,"in_count":2,"deck":[1,2,3,4],"dungeon_pile":[],"dungeon_count":0,"turn":5},
          "players":{"2":{"points":2},"3":{"in_dungeon":false}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"winner":2,"standings":{"1":0,"2":4,"3":0},"game":{"turn":6}}},
{"name":"R21 the game ends after turn 40 even mid-dungeon","rule":"R21","players":3,"seed":26,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":5,"leader_seat":2,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":39},
          "players":{"1":{"points":3},"2":{"points":1}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"winner":1,"standings":{"1":3,"2":1,"3":0},"game":{"turn":40}}},
{"name":"R22 players tied for the most points share the win","rule":"R22","players":3,"seed":27,"default":"decline",
 "given":{"game":{"new_dungeon":false,"dungeon_number":5,"leader_seat":2,"active_seat":1,"in_count":3,"deck":[4,1,2,3,5],"dungeon_pile":[],"dungeon_count":0,"turn":39},
          "players":{"1":{"points":2},"2":{"points":2},"3":{"points":1}}},
 "rules":[{"seat":1,"options_include":"PASS"}],
 "expect":{"winner":[1,2],"standings":{"1":2,"2":2,"3":1}}}
]
````
