# 03 spec

- time: 2026-10-28T04:37:25+00:00 (71.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 0237a041f3b38cb5, reply sha256 466b8e6fdd0ab610

## Sent

````
Game: Three Pigs: Secret Materials
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP
- Materials: Straw, Wood, Brick.
- Locations: Fields (Straw), Forest (Wood), Brickyard (Brick). Each starts with a pile of 0.
- Each player is secretly dealt a Favoured Material:
  - 3 players: shuffle one Straw, one Wood and one Brick card and deal one each, so all three differ.
  - 4 players: shuffle two each of Straw, Wood and Brick and deal one each.
- A player's Favoured Material is known only to them.
- Each player starts with 0 Straw, 0 Wood and 0 Brick. A player's stockpile is private, known only to them.

HOUSES
- A house is one material and has three sections, built in order: Floor, Walls, Roof.
- Each section costs 2 of that house's material, or 1 if it is the builder's Favoured Material.
- A player may have at most one unfinished house of each material.
- A player may complete at most 2 houses of any one material.
- Which sections each player has built, and of what material, is public. The cost paid is not shown.

EACH ROUND (up to 15 rounds)
1. Bonus: one location is drawn at random (each 1/3) and announced.
2. Refill: every location's pile gains 3, and the announced location gains 2 more.
3. Talk: everyone writes one short message at the same time, then all messages are shown to everyone. Messages bind no one.
4. Gather choice: everyone simultaneously chooses one of seven options:
   - Fields, Forest, Brickyard, Market;
   - Wolf-Fields, Wolf-Forest, Wolf-Brickyard.
5. Reveal: all choices are shown.
6. Resolve each of the three locations:
   - If any player chose Wolf at that location, nobody gathers there and its pile is unchanged.
   - Otherwise, the pile is divided equally among the players who chose it, rounding down. Each takes their share of that material, and the remainder stays in the pile.
   - If nobody chose the location, the pile stays.
   - Each player is told only their own gain, but the piles and the number of gatherers are public, so gains can be computed by anyone.
7. Market: every player who chose Market gains 1 of their Favoured Material. Any number of players can use the Market without sharing.
8. Players who chose a Wolf gain nothing.
9. Build action 1: everyone simultaneously chooses Build Straw, Build Wood, Build Brick or Pass.
   - A build adds the next section to that player's house of that material, starting a new house at the Floor if none is unfinished, and pays the cost from their stockpile.
   - If the player cannot pay, or the build would start a third house of that material, it counts as Pass.
   - The resulting public build state is shown.
10. Build action 2: exactly as build action 1.
11. Win check: any player with 3 completed houses has finished.
    - If exactly one player has finished, they win.
    - If several have, the finisher with the most total leftover resources wins. If that is tied, it is a draw among them.
    - The game then ends.
12. If round 15 ends with no finisher, the game ends. The winner is the player with the most completed houses, then the most built sections. If still tied, it is a draw.

How the winner is decided: The first player to complete 3 houses (at most 2 of any one material) wins. If several do so in the same round, the one with the most leftover resources wins, and a further tie is a draw. If nobody finishes in 15 rounds, the winner is the player with the most completed houses, then the most sections. Any remaining tie is a draw.
````

## Reply

````
```json
{
  "name": "Three Pigs: Secret Materials",
  "summary": "Each player has a secret Favoured Material. Players gather straw, wood and brick from shared piles at the same time, can send the Wolf to stop a location paying out, and build houses section by section. The first to finish 3 houses wins.",
  "players": {"min": 3, "max": 4, "suggested": 3},
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
      {"key": "favoured", "type": "text", "visible": "ally", "initial": "", "meaning": "Secret Favoured Material: Straw, Wood or Brick, dealt from favour_deck", "observable": false},
      {"key": "straw", "type": "number", "visible": "ally", "initial": 0, "meaning": "Private stockpile of Straw", "observable": false},
      {"key": "wood", "type": "number", "visible": "ally", "initial": 0, "meaning": "Private stockpile of Wood", "observable": false},
      {"key": "brick", "type": "number", "visible": "ally", "initial": 0, "meaning": "Private stockpile of Brick", "observable": false},
      {"key": "last_gain", "type": "text", "visible": "ally", "initial": "", "meaning": "This round's gather and market gain, told only to the owner", "observable": false},
      {"key": "gather_choice", "type": "text", "visible": "public", "initial": "", "meaning": "This round's gather choice, collected by poll and revealed to all afterwards", "observable": true},
      {"key": "build_choice", "type": "text", "visible": "ally", "initial": "", "meaning": "The build choice in the current build action", "observable": false},
      {"key": "straw_progress", "type": "number", "visible": "public", "initial": 0, "meaning": "Sections built on the unfinished Straw house: 0 none, 1 Floor, 2 Floor and Walls", "observable": true},
      {"key": "wood_progress", "type": "number", "visible": "public", "initial": 0, "meaning": "Sections built on the unfinished Wood house (0-2)", "observable": true},
      {"key": "brick_progress", "type": "number", "visible": "public", "initial": 0, "meaning": "Sections built on the unfinished Brick house (0-2)", "observable": true},
      {"key": "straw_done", "type": "number", "visible": "public", "initial": 0, "meaning": "Completed Straw houses (at most 2)", "observable": true},
      {"key": "wood_done", "type": "number", "visible": "public", "initial": 0, "meaning": "Completed Wood houses (at most 2)", "observable": true},
      {"key": "brick_done", "type": "number", "visible": "public", "initial": 0, "meaning": "Completed Brick houses (at most 2)", "observable": true},
      {"key": "completed", "type": "number", "visible": "public", "initial": 0, "meaning": "Total completed houses: straw_done + wood_done + brick_done", "observable": true},
      {"key": "sections", "type": "number", "visible": "public", "initial": 0, "meaning": "Total sections ever built, in all houses", "observable": true},
      {"key": "finished", "type": "number", "visible": "public", "initial": 0, "meaning": "1 once completed >= 3, otherwise 0", "observable": true}
    ],
    "game": [
      {"key": "favour_deck", "type": "list", "visible": "none", "initial": [], "meaning": "Favoured Material cards: [Straw, Wood, Brick] for 3 players, two of each for 4 players", "observable": false},
      {"key": "locations", "type": "list", "visible": "public", "initial": ["Fields", "Forest", "Brickyard"], "meaning": "The locations the bonus is drawn from", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round number", "observable": true},
      {"key": "bonus_location", "type": "text", "visible": "public", "initial": "", "meaning": "This round's bonus location", "observable": true},
      {"key": "fields_pile", "type": "number", "visible": "public", "initial": 0, "meaning": "Straw waiting at the Fields", "observable": true},
      {"key": "forest_pile", "type": "number", "visible": "public", "initial": 0, "meaning": "Wood waiting at the Forest", "observable": true},
      {"key": "brickyard_pile", "type": "number", "visible": "public", "initial": 0, "meaning": "Brick waiting at the Brickyard", "observable": true},
      {"key": "fields_gatherers", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Fields this round", "observable": false},
      {"key": "forest_gatherers", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Forest this round", "observable": false},
      {"key": "brickyard_gatherers", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Brickyard this round", "observable": false},
      {"key": "fields_wolves", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Wolf-Fields this round", "observable": false},
      {"key": "forest_wolves", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Wolf-Forest this round", "observable": false},
      {"key": "brickyard_wolves", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players who chose Wolf-Brickyard this round", "observable": false}
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
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; bonus_location = one entry of locations drawn at random (each 1/3)."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce 'Round {round}: the bonus location is {bonus_location}.'"},
    {"action": "update", "who": "all players", "answer": null, "effect": "fields_pile += 3; forest_pile += 3; brickyard_pile += 3; then the pile of bonus_location gains 2 more. Announce the three piles."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "Every message is broadcast to all players as 'Seat {seat} says: {value}'. Messages bind no one."},
    {"action": "poll", "who": "all players", "answer": "one of: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard", "effect": "Each player's gather_choice = their answer. Nobody sees any choice until all are in."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal every player's gather_choice to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Count fields_gatherers (gather_choice = Fields), forest_gatherers, brickyard_gatherers, fields_wolves (gather_choice = Wolf-Fields), forest_wolves and brickyard_wolves. Set every player's last_gain = 'nothing'."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Fields: if fields_wolves = 0 and fields_gatherers > 0, then share = floor(fields_pile / fields_gatherers); each player with gather_choice = Fields gets straw += share and last_gain = share Straw; fields_pile -= share * fields_gatherers. Otherwise fields_pile is unchanged."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Forest: if forest_wolves = 0 and forest_gatherers > 0, then share = floor(forest_pile / forest_gatherers); each Forest chooser gets wood += share and last_gain = share Wood; forest_pile -= share * forest_gatherers. Otherwise forest_pile is unchanged."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Brickyard: if brickyard_wolves = 0 and brickyard_gatherers > 0, then share = floor(brickyard_pile / brickyard_gatherers); each Brickyard chooser gets brick += share and last_gain = share Brick; brickyard_pile -= share * brickyard_gatherers. Otherwise brickyard_pile is unchanged."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Market: each player with gather_choice = Market gains 1 of their favoured material (straw, wood or brick) and last_gain = 1 of that material. Players who chose a Wolf gain nothing."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce the piles after resolution and the number of gatherers and wolves at each location."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately receives their own last_gain and stockpile (straw, wood, brick)."},
    {"action": "poll", "who": "all players", "answer": "one of the offered options: Build Straw, Build Wood, Build Brick, Pass", "effect": "build_choice = answer (build action 1)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player with build_choice = Build M: cost = 1 if favoured = M, else 2. If stock of M < cost, or (M_done = 2 and M_progress = 0), it counts as Pass. Otherwise stock of M -= cost; M_progress += 1; sections += 1; if M_progress = 3, then M_progress = 0, M_done += 1 and completed += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Show every player's public build state: straw/wood/brick progress and done, completed and sections. The cost paid is not shown."},
    {"action": "poll", "who": "all players", "answer": "one of the offered options: Build Straw, Build Wood, Build Brick, Pass", "effect": "build_choice = answer (build action 2)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Apply build action 2 exactly as build action 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Show every player's public build state again."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player, finished = 1 if completed >= 3, otherwise 0."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if any player has finished = 1, or if round >= 15. Otherwise start the next round."}
  ],
  "ending": {
    "condition": "count of players with finished = 1 >= 1, or round >= 15",
    "rank_by": "you.finished * (100000 + you.straw + you.wood + you.brick) + (1 - you.finished) * (you.completed * 100 + you.sections)",
    "decided_by": "If anyone has completed 3 houses, the finishers rank above everyone else and are ordered by total leftover straw + wood + brick. Otherwise players are ranked by completed houses, then by total sections built. The highest value wins, and players level at the top share the win (a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When setup runs with 3 players, then favour_deck holds one Straw, one Wood and one Brick and each player is dealt one, so all three favoured materials differ."},
    {"id": "R2", "text": "When setup runs with 4 players, then favour_deck holds two Straw, two Wood and two Brick, each player is dealt one, and the 2 undealt cards stay hidden."},
    {"id": "R3", "text": "When the game starts, then every pile is 0 and every player has straw = 0, wood = 0 and brick = 0."},
    {"id": "R4", "text": "When a player's favoured material or stockpile changes, then only that player is told it."},
    {"id": "R5", "text": "When a round begins, then bonus_location is drawn at random from Fields, Forest and Brickyard and announced to all."},
    {"id": "R6", "text": "When the refill happens, then each pile gains 3 and the bonus location's pile gains 2 more, so it gains 5 in total."},
    {"id": "R7", "text": "When the talk step runs, then every player submits one message at the same time and all messages are shown to everyone."},
    {"id": "R8", "text": "When the gather choice is made, then all players choose at the same time from Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest and Wolf-Brickyard, and all choices are revealed afterwards."},
    {"id": "R9", "text": "When at least one player chose Wolf at a location, then nobody gathers there and that pile is unchanged."},
    {"id": "R10", "text": "When no Wolf is at a location and g >= 1 players chose it, then each of them gains floor(pile / g) of its material and the remainder stays: 5 straw split by 2 gives each 2 and leaves 1."},
    {"id": "R11", "text": "When nobody chose a location, then its pile stays and carries over to the next round."},
    {"id": "R12", "text": "When a player chose Market, then they gain 1 of their favoured material, however many others also chose Market."},
    {"id": "R13", "text": "When a player chose a Wolf option, then they gain nothing that round."},
    {"id": "R14", "text": "When gathering is resolved, then each player is privately told their own gain, and the remaining piles and the counts of gatherers and wolves are public."},
    {"id": "R15", "text": "When a player builds a section of material M, then it costs 1 M if favoured = M, otherwise 2 M, taken from their stockpile."},
    {"id": "R16", "text": "When a player builds M and has an unfinished M house, then the next section is added (Floor, then Walls, then Roof); otherwise a new M house is started at the Floor."},
    {"id": "R17", "text": "When a build brings M_progress to 3, then the house is complete: M_done += 1, completed += 1 and M_progress returns to 0."},
    {"id": "R18", "text": "When a player cannot pay the cost, or the build would start a third house of material M (M_done = 2), then the build counts as Pass and nothing changes."},
    {"id": "R19", "text": "When a section is built, then sections += 1, and the house states are shown to all but the cost paid is not."},
    {"id": "R20", "text": "When a round's builds happen, then there are exactly 2 simultaneous build actions, the second resolved after the first."},
    {"id": "R21", "text": "When a player has completed >= 3 at the end of a round, then finished = 1 and the game ends after that round."},
    {"id": "R22", "text": "When exactly one player has finished, then that player wins."},
    {"id": "R23", "text": "When several players finish in the same round, then the one with the most leftover straw + wood + brick wins, and players tied for the most share a draw."},
    {"id": "R24", "text": "When round 15 ends with no finisher, then the game ends and the most completed houses wins, then the most sections, and a remaining tie is a draw."}
  ],
  "offers": [
    {"question": "Talk message", "who": "all players", "options": "Any short free-text message."},
    {"question": "Gather choice", "who": "all players", "options": "Every seat, in every situation: Fields, Forest, Brickyard, Market, Wolf-Fields, Wolf-Forest, Wolf-Brickyard."},
    {"question": "Build action 1 and build action 2", "who": "all players", "options": "Pass, always. Build M (Straw, Wood or Brick) only when the seat's stock of M is at least the cost (1 if favoured = M, else 2) and the build would not start a third M house (not M_done = 2). A seat that can afford nothing is offered only Pass."}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 3", "why": "The designer suggests 3 and the deal is defined for 3 and 4. At 3, the favoured materials are a perfect split, so guessing the others' materials is clean deduction, and contesting a pile or sending the Wolf has a clear target. A fifth player has no deal defined, and splitting the piles that many ways would leave almost no gains."},
    {"what": "Talk kept as one simultaneous poll per round, broadcast to all", "why": "The source requires it. Players disagree: each wants a pile to themselves and wants to hide their favoured material. Bluffing about where you will go, or threatening a Wolf, gives everyone something to reason about. The talk is simultaneous because the source says messages are written at the same time."},
    {"what": "Build offers include only legal builds, plus Pass", "why": "A seat is never offered what it may not do. The 'counts as Pass' rule stays as a backstop. The filter uses only the seat's own private stockpile, so it leaks nothing."},
    {"what": "Ranking expression: finisher offset 100000, completed weight 100", "why": "A non-finisher's value is at most 2*100 + 12 sections, well below 100000, so finishers always rank above everyone. The weight of 100 makes completed houses outrank sections, since sections never reach 100."},
    {"what": "Sections tie-break counts every section ever built, including those in completed houses", "why": "The source says 'most built sections' without restricting it."},
    {"what": "Gather and wolf counts are announced after resolution", "why": "The source says the piles and the number of gatherers are public, so anyone can work out each gain."}
  ],
  "simplifications": [
    {"what": "Each house is tracked as a progress counter (0-2) plus a completed count per material, not as a list of named sections", "why": "Floor, Walls and Roof are always built in order, so a counter holds the same information."},
    {"what": "The 'one unfinished house per material' rule is enforced by the build always adding to the existing unfinished house", "why": "The engine has no separate choice to start a second unfinished house, so the limit holds automatically."}
  ],
  "unsupported": []
}
```
````
