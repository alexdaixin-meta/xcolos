# 04 scenarios

- time: 2026-10-28T04:38:37+00:00 (109.3s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 76b3558f622673b7, reply sha256 26f3df7d9963ce75

## Sent

````
SPEC:
{
  "name": "Three Pigs: Secret Materials",
  "summary": "Each player has a secret Favoured Material. Players gather straw, wood and brick from shared piles at the same time, can send the Wolf to stop a location paying out, and build houses section by section. The first to finish 3 houses wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "max_rounds": 15,
    "refill_per_location": 3,
    "bonus_extra": 2,
    "bonus_chance_each_location": 0.3333,
    "section_cost": 2,
    "favoured_section_cost": 1,
    "sections_per_house": 3,
    "max_unfinished_per_material": 1,
    "max_completed_per_material": 2,
    "houses_to_finish": 3,
    "market_gain": 1,
    "build_actions_per_round": 2,
    "initial_pile": 0,
    "initial_stock": 0,
    "favour_cards_each_material_3p": 1,
    "favour_cards_each_material_4p": 2,
    "finisher_rank_offset": 100000,
    "completed_weight": 100
  },
  "attributes": {
    "player": [
      {
        "key": "favoured",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Secret Favoured Material: Straw, Wood or Brick, dealt from favour_deck",
        "observable": false
      },
      {
        "key": "straw",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Private stockpile of Straw",
        "observable": false
      },
      {
        "key": "wood",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Private stockpile of Wood",
        "observable": false
      },
      {
        "key": "brick",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Private stockpile of Brick",
        "observable": false
      },
      {
        "key": "last_gain",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's gather and market gain, told only to the owner",
        "observable": false
      },
      {
        "key": "gather_choice",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's gather choice, collected by poll and revealed to all afterwards",
        "observable": true
      },
      {
        "key": "build_choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The build choice in the current build action",
        "observable": false
      },
      {
        "key": "straw_progress",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sections built on the unfinished Straw house: 0 none, 1 Floor, 2 Floor and Walls",
        "observable": true
      },
      {
        "key": "wood_progress",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sections built on the unfinished Wood house (0-2)",
        "observable": true
      },
      {
        "key": "brick_progress",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sections built on the unfinished Brick house (0-2)",
        "observable": true
      },
      {
        "key": "straw_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Completed Straw houses (at most 2)",
        "observable": true
      },
      {
        "key": "wood_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Completed Wood houses (at most 2)",
        "observable": true
      },
      {
        "key": "brick_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Completed Brick houses (at most 2)",
        "observable": true
      },
      {
        "key": "completed",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total completed houses: straw_done + wood_done + brick_done",
        "observable": true
      },
      {
        "key": "sections",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total sections ever built, in all houses",
        "observable": true
      },
      {
        "key": "finished",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 once completed >= 3, otherwise 0",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "favour_deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Favoured Material cards: [Straw, Wood, Brick] for 3 players, two of each for 4 players",
        "observable": false
      },
      {
        "key": "locations",
        "type": "list",
        "visible": "public",
        "initial": [
          "Fields",
          "Forest",
          "Brickyard"
        ],
        "meaning": "The locations the bonus is drawn from",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number",
        "observable": true
      },
      {
        "key": "bonus_location",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's bonus location",
        "observable": true
      },
      {
        "key": "fields_pile",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Straw waiting at the Fields",
        "observable": true
      },
      {
        "key": "forest_pile",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wood waiting at the Forest",
        "observable": true
      },
      {
        "key": "brickyard_pile",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Brick waiting at the Brickyard",
        "observable": true
      },
      {
        "key": "fields_gatherers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Fields this round",
        "observable": false
      },
      {
        "key": "forest_gatherers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Forest this round",
        "observable": false
      },
      {
        "key": "brickyard_gatherers",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Brickyard this round",
        "observable": false
      },
      {
        "key": "fields_wolves",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Wolf-Fields this round",
        "observable": false
      },
      {
        "key": "forest_wolves",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Wolf-Forest this round",
        "observable": false
      },
      {
        "key": "brickyard_wolves",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of players who chose Wolf-Brickyard this round",
        "observable": false
      }
    ]
  },
  "setup": [
    "Set fields_pile, forest_pile and brickyard_pile to 0.",
    "Fill favour_deck: with 3 players it holds one Straw, one Wood and one Brick; with 4 players it holds two of each.",
    "For each player, draw one card at random from favour_deck, set it as their favoured and remove it from favour_deck. Leftover cards stay hidden.",
    "Every player starts with straw = 0, wood = 0, brick = 0, all house progress and done counts at 0, completed = 0, sections = 0 and finished = 0.",
    "Sync: each player is privately told their favoured material and their stockpile."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; bonus_location = one entry of locations drawn at random (each 1/3)."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce 'Round {round}: the bonus location is {bonus_location}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "fields_pile += 3; forest_pile += 3; brickyard_pile += 3; then the pile of bonus_location gains 2 more. Announce the three piles."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind no one."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard",
      "effect": "Each player's gather_choice = their answer. Nobody sees any choice until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal every player's gather_choice to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Count fields_gatherers (gather_choice = Fields), forest_gatherers, brickyard_gatherers, fields_wolves (gather_choice = Wolf-Fields), forest_wolves and brickyard_wolves. Set every player's last_gain = 'nothing'."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Fields: if fields_wolves = 0 and fields_gatherers > 0, then share = floor(fields_pile / fields_gatherers); each player with gather_choice = Fields gets straw += share and last_gain = share Straw; fields_pile -= share * fields_gatherers. Otherwise fields_pile is unchanged."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Forest: if forest_wolves = 0 and forest_gatherers > 0, then share = floor(forest_pile / forest_gatherers); each Forest chooser gets wood += share and last_gain = share Wood; forest_pile -= share * forest_gatherers. Otherwise forest_pile is unchanged."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Brickyard: if brickyard_wolves = 0 and brickyard_gatherers > 0, then share = floor(brickyard_pile / brickyard_gatherers); each Brickyard chooser gets brick += share and last_gain = share Brick; brickyard_pile -= share * brickyard_gatherers. Otherwise brickyard_pile is unchanged."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Market: each player with gather_choice = Market gains 1 of their favoured material (straw, wood or brick) and last_gain = 1 of that material. Players who chose a Wolf gain nothing."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the piles after resolution and the number of gatherers and wolves at each location."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately receives their own last_gain and stockpile (straw, wood, brick)."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of the offered options: Build Straw, Build Wood, Build Brick, Pass",
      "effect": "build_choice = answer (build action 1)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with build_choice = Build M: cost = 1 if favoured = M, else 2. If stock of M < cost, or (M_done = 2 and M_progress = 0), it counts as Pass. Otherwise stock of M -= cost; M_progress += 1; sections += 1; if M_progress = 3, then M_progress = 0, M_done += 1 and completed += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Show every player's public build state: straw/wood/brick progress and done, completed and sections. The cost paid is not shown."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of the offered options: Build Straw, Build Wood, Build Brick, Pass",
      "effect": "build_choice = answer (build action 2)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Apply build action 2 exactly as build action 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Show every player's public build state again."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player, finished = 1 if completed >= 3, otherwise 0."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if any player has finished = 1, or if round >= 15. Otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "count of players with finished = 1 >= 1, or round >= 15",
    "rank_by": "you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections)",
    "decided_by": "If anyone has completed 3 houses, the finishers rank above everyone else and are ordered by total leftover straw + wood + brick. Otherwise players are ranked by completed houses, then by total sections built. The highest value wins, and players level at the top share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When setup runs with 3 players, then favour_deck holds one Straw, one Wood and one Brick and each player is dealt one, so all three favoured materials differ."
    },
    {
      "id": "R2",
      "text": "When setup runs with 4 players, then favour_deck holds two Straw, two Wood and two Brick, each player is dealt one, and the 2 undealt cards stay hidden."
    },
    {
      "id": "R3",
      "text": "When the game starts, then every pile is 0 and every player has straw = 0, wood = 0 and brick = 0."
    },
    {
      "id": "R4",
      "text": "When a player's favoured material or stockpile changes, then only that player is told it."
    },
    {
      "id": "R5",
      "text": "When a round begins, then bonus_location is drawn at random from Fields, Forest and Brickyard and announced to all."
    },
    {
      "id": "R6",
      "text": "When the refill happens, then each pile gains 3 and the bonus location's pile gains 2 more, so it gains 5 in total."
    },
    {
      "id": "R7",
      "text": "When the talk step runs, then every player submits one message at the same time and all messages are shown to everyone."
    },
    {
      "id": "R8",
      "text": "When the gather choice is made, then all players choose at the same time from Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest and Wolf-Brickyard, and all choices are revealed afterwards."
    },
    {
      "id": "R9",
      "text": "When at least one player chose Wolf at a location, then nobody gathers there and that pile is unchanged."
    },
    {
      "id": "R10",
      "text": "When no Wolf is at a location and g >= 1 players chose it, then each of them gains floor(pile / g) of its material and the remainder stays: 5 straw split by 2 gives each 2 and leaves 1."
    },
    {
      "id": "R11",
      "text": "When nobody chose a location, then its pile stays and carries over to the next round."
    },
    {
      "id": "R12",
      "text": "When a player chose Market, then they gain 1 of their favoured material, however many others also chose Market."
    },
    {
      "id": "R13",
      "text": "When a player chose a Wolf option, then they gain nothing that round."
    },
    {
      "id": "R14",
      "text": "When gathering is resolved, then each player is privately told their own gain, and the remaining piles and the counts of gatherers and wolves are public."
    },
    {
      "id": "R15",
      "text": "When a player builds a section of material M, then it costs 1 M if favoured = M, otherwise 2 M, taken from their stockpile."
    },
    {
      "id": "R16",
      "text": "When a player builds M and has an unfinished M house, then the next section is added (Floor, then Walls, then Roof); otherwise a new M house is started at the Floor."
    },
    {
      "id": "R17",
      "text": "When a build brings M_progress to 3, then the house is complete: M_done += 1, completed += 1 and M_progress returns to 0."
    },
    {
      "id": "R18",
      "text": "When a player cannot pay the cost, or the build would start a third house of material M (M_done = 2), then the build counts as Pass and nothing changes."
    },
    {
      "id": "R19",
      "text": "When a section is built, then sections += 1, and the house states are shown to all but the cost paid is not."
    },
    {
      "id": "R20",
      "text": "When a round's builds happen, then there are exactly 2 simultaneous build actions, the second resolved after the first."
    },
    {
      "id": "R21",
      "text": "When a player has completed >= 3 at the end of a round, then finished = 1 and the game ends after that round."
    },
    {
      "id": "R22",
      "text": "When exactly one player has finished, then that player wins."
    },
    {
      "id": "R23",
      "text": "When several players finish in the same round, then the one with the most leftover straw + wood + brick wins, and players tied for the most share a draw."
    },
    {
      "id": "R24",
      "text": "When round 15 ends with no finisher, then the game ends and the most completed houses wins, then the most sections, and a remaining tie is a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all players",
      "options": "Any short free-text message."
    },
    {
      "question": "Gather choice",
      "who": "all players",
      "options": "Every seat, in every situation: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard."
    },
    {
      "question": "Build action 1 and build action 2",
      "who": "all players",
      "options": "Pass, always. Build M (Straw, Wood or Brick) only when the seat's stock of M is at least the cost (1 if favoured = M, else 2) and the build would not start a third M house (not M_done = 2). A seat that can afford nothing is offered only Pass."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The designer suggests 3 and the deal is defined for 3 and 4. At 3, the favoured materials are a perfect split, so guessing the others' materials is clean deduction, and contesting a pile or sending the Wolf has a clear target. A fifth player has no deal defined, and splitting the piles that many ways would leave almost no gains."
    },
    {
      "what": "Talk kept as one simultaneous poll per round, broadcast to all",
      "why": "The source requires it. Players disagree: each wants a pile to themselves and wants to hide their favoured material. Bluffing about where you will go, or threatening a Wolf, gives everyone something to reason about. The talk is simultaneous because the source says messages are written at the same time."
    },
    {
      "what": "Build offers include only legal builds, plus Pass",
      "why": "A seat is never offered what it may not do. The 'counts as Pass' rule stays as a backstop. The filter uses only the seat's own private stockpile, so it leaks nothing."
    },
    {
      "what": "Ranking expression: finisher offset 100000, completed weight 100",
      "why": "A non-finisher's value is at most 2*100 + 12 sections, well below 100000, so finishers always rank above everyone. The weight of 100 makes completed houses outrank sections, since sections never reach 100."
    },
    {
      "what": "Sections tie-break counts every section ever built, including those in completed houses",
      "why": "The source says 'most built sections' without restricting it."
    },
    {
      "what": "Gather and wolf counts are announced after resolution",
      "why": "The source says the piles and the number of gatherers are public, so anyone can work out each gain."
    }
  ],
  "simplifications": [
    {
      "what": "Each house is tracked as a progress counter (0-2) plus a completed count per material, not as a list of named sections",
      "why": "Floor, Walls and Roof are always built in order, so a counter holds the same information."
    },
    {
      "what": "The 'one unfinished house per material' rule is enforced by the build always adding to the existing unfinished house",
      "why": "The engine has no separate choice to start a second unfinished house, so the limit holds automatically."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: gather_choice, straw_progress, wood_progress, brick_progress, straw_done, wood_done, brick_done, completed, sections, finished; table: round, bonus_location, fields_pile, forest_pile, brickyard_pile.
````

## Reply

````
```json
[
  {
    "name": "3 players: the 3-card favour deck is fully dealt, one card each",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "lens": {"game": {"favour_deck": 0}}
    }
  },
  {
    "name": "4 players: 6-card favour deck, 4 dealt, 2 remain",
    "rule": "R2",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "lens": {"game": {"favour_deck": 2}}
    }
  },
  {
    "name": "At start every pile is 0 and nothing is built",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "game": {"fields_pile": 0, "forest_pile": 0, "brickyard_pile": 0, "round": 0},
      "players": {
        "1": {"sections": 0, "completed": 0},
        "2": {"sections": 0, "completed": 0},
        "3": {"sections": 0, "completed": 0}
      }
    }
  },
  {
    "name": "Market gain changes a private stock that enables only the owner to build",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Forest"},
      {"seat": 1, "options_include": "Build Straw"}
    ],
    "expect": {
      "players": {
        "1": {"straw_progress": 1, "sections": 1},
        "2": {"sections": 0},
        "3": {"sections": 0}
      },
      "not_offered": [
        {"seat": 2, "option": "Build Straw"},
        {"seat": 3, "option": "Build Straw"}
      ]
    }
  },
  {
    "name": "Round begins: round becomes 1 and bonus is drawn from the locations list",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"locations": ["Brickyard"]}},
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"round": 1, "bonus_location": "Brickyard"}
    }
  },
  {
    "name": "Refill: each pile +3, bonus Forest gets +5",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"locations": ["Forest"], "fields_pile": 0, "forest_pile": 0, "brickyard_pile": 0}},
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"fields_pile": 3, "forest_pile": 5, "brickyard_pile": 3}
    }
  },
  {
    "name": "Talk step runs for all and the round completes",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"round": 1},
      "players": {
        "1": {"gather_choice": "Market"},
        "2": {"gather_choice": "Market"},
        "3": {"gather_choice": "Market"}
      }
    }
  },
  {
    "name": "Gather choice offers all seven options and choices are public",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "Wolf-Brickyard"},
      {"seat": 2, "options_include": "Forest"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "players": {
        "1": {"gather_choice": "Wolf-Brickyard"},
        "2": {"gather_choice": "Forest"},
        "3": {"gather_choice": "Market"}
      },
      "offered": [
        {"seat": 1, "option": "Fields"},
        {"seat": 1, "option": "Wolf-Fields"},
        {"seat": 2, "option": "Wolf-Forest"},
        {"seat": 3, "option": "Brickyard"}
      ]
    }
  },
  {
    "name": "Wolf at Fields: gatherer gets nothing and pile unchanged",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"locations": ["Forest"], "fields_pile": 4},
      "players": {
        "1": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "2": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Fields"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Brickyard"}
    ],
    "expect": {
      "game": {"fields_pile": 7},
      "players": {"1": {"sections": 0, "straw_progress": 0}},
      "not_offered": [{"seat": 1, "option": "Build Straw"}]
    }
  },
  {
    "name": "5 straw split by 2: each gets 2, 1 stays",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"locations": ["Fields"], "fields_pile": 0},
      "players": {
        "1": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "2": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Fields"},
      {"seat": 2, "options_include": "Fields"},
      {"seat": 3, "options_include": "Wolf-Forest"},
      {"seat": 1, "options_include": "Build Straw", "times": "all"},
      {"seat": 2, "options_include": "Build Straw", "times": "all"}
    ],
    "expect": {
      "game": {"fields_pile": 1},
      "players": {
        "1": {"straw_progress": 1, "sections": 1},
        "2": {"straw_progress": 1, "sections": 1}
      }
    }
  },
  {
    "name": "Unchosen piles carry over",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"locations": ["Fields"], "fields_pile": 0, "forest_pile": 2, "brickyard_pile": 4}},
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"fields_pile": 5, "forest_pile": 5, "brickyard_pile": 7}
    }
  },
  {
    "name": "All choose Market: each gains 1 favoured and builds it at cost 1",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Market"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"},
      {"seat": 1, "options_include": "Build Straw"},
      {"seat": 2, "options_include": "Build Wood"},
      {"seat": 3, "options_include": "Build Brick"}
    ],
    "expect": {
      "players": {
        "1": {"straw_progress": 1, "sections": 1},
        "2": {"wood_progress": 1, "sections": 1},
        "3": {"brick_progress": 1, "sections": 1}
      },
      "not_offered": [
        {"seat": 1, "option": "Build Wood"},
        {"seat": 2, "option": "Build Brick"},
        {"seat": 3, "option": "Build Straw"}
      ]
    }
  },
  {
    "name": "Wolf chooser gains nothing and can build nothing",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"locations": ["Fields"], "forest_pile": 0},
      "players": {
        "1": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Forest"},
      {"seat": 2, "options_include": "Market"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"forest_pile": 3},
      "players": {"1": {"sections": 0}},
      "not_offered": [
        {"seat": 1, "option": "Build Straw"},
        {"seat": 1, "option": "Build Wood"},
        {"seat": 1, "option": "Build Brick"}
      ]
    }
  },
  {
    "name": "Lone gatherers empty their piles; choices and piles public (bonus-independent)",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"forest_pile": 0, "brickyard_pile": 0}},
    "rules": [
      {"seat": 1, "options_include": "Brickyard"},
      {"seat": 2, "options_include": "Forest"},
      {"seat": 3, "options_include": "Market"}
    ],
    "expect": {
      "game": {"forest_pile": 0, "brickyard_pile": 0},
      "players": {
        "1": {"gather_choice": "Brickyard"},
        "2": {"gather_choice": "Forest"},
        "3": {"gather_choice": "Market"}
      }
    }
  },
  {
    "name": "Favoured section costs 1, other costs 2",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Wood", "straw": 0, "wood": 2, "brick": 0},
        "2": {"favoured": "Straw", "straw": 0, "wood": 3, "brick": 0},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Brickyard"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Forest"},
      {"seat": 1, "options_include": "Build Wood", "times": "all"},
      {"seat": 2, "options_include": "Build Wood", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"wood_progress": 2, "sections": 2},
        "2": {"wood_progress": 1, "sections": 1}
      }
    }
  },
  {
    "name": "Build adds to the unfinished house, or starts a new one at the Floor",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Straw", "straw": 1, "wood": 0, "brick": 0, "straw_progress": 1, "sections": 1},
        "2": {"favoured": "Wood", "straw": 0, "wood": 1, "brick": 0, "wood_done": 1, "completed": 1, "sections": 3},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Brickyard"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Forest"},
      {"seat": 1, "options_include": "Build Straw"},
      {"seat": 2, "options_include": "Build Wood"}
    ],
    "expect": {
      "players": {
        "1": {"straw_progress": 2, "sections": 2},
        "2": {"wood_progress": 1, "wood_done": 1, "completed": 1, "sections": 4}
      }
    }
  },
  {
    "name": "Roof completes the house: done +1, completed +1, progress back to 0",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 1, "brick_progress": 2, "sections": 2},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick"}
    ],
    "expect": {
      "players": {
        "1": {"brick_progress": 0, "brick_done": 1, "completed": 1, "sections": 3, "finished": 0}
      }
    }
  },
  {
    "name": "No third house of a material, and unaffordable builds are not offered",
    "rule": "R18",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Straw", "straw": 5, "wood": 0, "brick": 0, "straw_done": 2, "completed": 2, "sections": 6},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 1},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Forest"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Brickyard"}
    ],
    "expect": {
      "players": {
        "1": {"straw_done": 2, "straw_progress": 0, "completed": 2, "sections": 6},
        "2": {"brick_progress": 0, "sections": 0}
      },
      "not_offered": [
        {"seat": 1, "option": "Build Straw"},
        {"seat": 2, "option": "Build Brick"}
      ]
    }
  },
  {
    "name": "Building a section adds 1 to sections",
    "rule": "R19",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Straw", "straw": 1, "wood": 0, "brick": 0},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Forest"},
      {"seat": 2, "options_include": "Wolf-Fields"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Straw"}
    ],
    "expect": {
      "players": {
        "1": {"straw_progress": 1, "sections": 1},
        "2": {"sections": 0},
        "3": {"sections": 0}
      }
    }
  },
  {
    "name": "Exactly 2 build actions per round even with stock for more",
    "rule": "R20",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 5},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"brick_progress": 2, "sections": 2, "completed": 0}}
    }
  },
  {
    "name": "Third completed house sets finished and ends the game after the round",
    "rule": "R21",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 1, "straw_done": 1, "wood_done": 1, "brick_progress": 2, "completed": 2, "sections": 8},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 100000, "2": 0, "3": 0},
      "game": {"round": 1},
      "players": {"1": {"completed": 3, "brick_done": 1, "finished": 1}, "2": {"finished": 0}}
    }
  },
  {
    "name": "Single finisher wins over a non-finisher with more leftovers",
    "rule": "R22",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 1, "straw_done": 1, "wood_done": 1, "brick_progress": 2, "completed": 2, "sections": 8},
        "2": {"favoured": "Wood", "straw": 9, "wood": 0, "brick": 0, "straw_done": 1, "brick_done": 1, "completed": 2, "sections": 6},
        "3": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 100000, "3": 0},
      "players": {"1": {"finished": 1}, "2": {"finished": 0}}
    }
  },
  {
    "name": "Two finishers: most leftover materials wins",
    "rule": "R23",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 4, "straw_done": 1, "wood_done": 1, "brick_progress": 2, "completed": 2, "sections": 8},
        "2": {"favoured": "Straw", "straw": 2, "wood": 0, "brick": 0, "wood_done": 1, "brick_done": 1, "straw_progress": 2, "completed": 2, "sections": 8},
        "3": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick"},
      {"seat": 2, "options_include": "Build Straw"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 100003, "2": 100001, "3": 0},
      "players": {"1": {"finished": 1}, "2": {"finished": 1}}
    }
  },
  {
    "name": "Two finishers with equal leftovers share the win",
    "rule": "R23",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 3, "straw_done": 1, "wood_done": 1, "brick_progress": 2, "completed": 2, "sections": 8},
        "2": {"favoured": "Straw", "straw": 3, "wood": 0, "brick": 0, "wood_done": 1, "brick_done": 1, "straw_progress": 2, "completed": 2, "sections": 8},
        "3": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"},
      {"seat": 1, "options_include": "Build Brick"},
      {"seat": 2, "options_include": "Build Straw"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 100002, "2": 100002, "3": 0}
    }
  },
  {
    "name": "Round 15 ends with no finisher: most completed, then sections",
    "rule": "R24",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {"round": 14},
      "players": {
        "1": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0, "straw_done": 1, "wood_done": 1, "straw_progress": 1, "completed": 2, "sections": 7},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0, "straw_done": 1, "wood_done": 1, "completed": 2, "sections": 6},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0, "brick_done": 1, "wood_progress": 2, "completed": 1, "sections": 5}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 207, "2": 206, "3": 105},
      "game": {"round": 15}
    }
  },
  {
    "name": "Round 15 ends with a full tie at the top: shared win",
    "rule": "R24",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "game": {"round": 14},
      "players": {
        "1": {"favoured": "Straw", "straw": 0, "wood": 0, "brick": 0, "straw_done": 1, "wood_done": 1, "completed": 2, "sections": 6},
        "2": {"favoured": "Wood", "straw": 0, "wood": 0, "brick": 0, "straw_done": 1, "brick_done": 1, "completed": 2, "sections": 6},
        "3": {"favoured": "Brick", "straw": 0, "wood": 0, "brick": 0, "brick_done": 1, "completed": 1, "sections": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Wolf-Fields"},
      {"seat": 2, "options_include": "Wolf-Forest"},
      {"seat": 3, "options_include": "Wolf-Brickyard"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 206, "2": 206, "3": 103}
    }
  }
]
```
````
