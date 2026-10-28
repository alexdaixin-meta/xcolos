# 04 scenarios

- time: 2026-10-28T05:46:55+00:00 (78.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 c3d9de21bec5c237, reply sha256 2323bd290b5981a2

## Sent

````
SPEC:
{
  "name": "Back to the Dungeon: Single Delve",
  "summary": "Players take turns drawing monsters and either secretly add them to a shared dungeon or sacrifice equipment. The last player who has not passed must run the dungeon. The first to 2 successful runs wins; 2 failures eliminate a player.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "base_hp": 3,
    "armor_hp": 5,
    "shield_hp": 3,
    "torch_max_strength": 3,
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
    "deck_size": 13,
    "item_count": 5,
    "successes_to_win": 2,
    "failures_to_eliminate": 2,
    "max_rounds": 40,
    "initial_successes": 0,
    "initial_failures": 0
  },
  "attributes": {
    "player": [
      {
        "key": "successes",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "successful runs",
        "observable": true
      },
      {
        "key": "failures",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "failed runs",
        "observable": true
      },
      {
        "key": "eliminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true once the player has 2 failures",
        "observable": true
      },
      {
        "key": "passed",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "the player has passed in the current dungeon",
        "observable": true
      },
      {
        "key": "drawn_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "the monster this player just drew and is deciding on; empty otherwise",
        "observable": false
      },
      {
        "key": "added_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "the monsters this player has added face-down to the current dungeon (only they know them)",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Goblin",
          "Goblin",
          "Skeleton",
          "Skeleton",
          "Orc",
          "Orc",
          "Vampire",
          "Vampire",
          "Golem",
          "Golem",
          "Lich",
          "Demon",
          "Dragon"
        ],
        "meaning": "the shuffled monster deck",
        "observable": false
      },
      {
        "key": "dungeon",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the face-down monsters in the current dungeon",
        "observable": false
      },
      {
        "key": "items",
        "type": "list",
        "visible": "public",
        "initial": [
          "Armor",
          "Shield",
          "Torch",
          "Holy Water",
          "Dragon Spear"
        ],
        "meaning": "the equipment items remaining in this dungeon",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the seat whose turn it is",
        "observable": true
      },
      {
        "key": "deck_count",
        "type": "number",
        "visible": "public",
        "initial": 13,
        "meaning": "cards left in the deck",
        "observable": true
      },
      {
        "key": "dungeon_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "cards in the dungeon",
        "observable": true
      },
      {
        "key": "drawn_strength",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "strength of the card just drawn (scratch)",
        "observable": false
      },
      {
        "key": "dungeon_total",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "sum of the strengths of the dungeon cards",
        "observable": false
      },
      {
        "key": "dungeon_low",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "sum of the strengths of dungeon cards of strength 3 or less (Torch targets)",
        "observable": false
      },
      {
        "key": "dungeon_undead",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "sum of the strengths of dungeon Vampires and the Lich (Holy Water targets)",
        "observable": false
      },
      {
        "key": "dungeon_dragon",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "strength of the Dragon if it is in the dungeon (Dragon Spear target)",
        "observable": false
      },
      {
        "key": "runner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat that ran the last dungeon",
        "observable": true
      },
      {
        "key": "last_hp",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the runner's HP in the last run",
        "observable": true
      },
      {
        "key": "last_damage",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the damage in the last run",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rounds completed",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat the players in a fixed order, seats 1 to N; clockwise means increasing seat number, wrapping around.",
    "Set every player's successes and failures to 0, eliminated to false, passed to false, drawn_card empty and added_cards empty.",
    "Fill the deck with the 13 monsters (Goblin x2, Skeleton x2, Orc x2, Vampire x2, Golem x2, Lich, Demon, Dragon); every draw is random, which shuffles it.",
    "The dungeon starts empty, items holds all five items, and every dungeon counter is 0.",
    "Set active_seat to 1 and deck_count to 13."
  ],
  "round": [
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce active_seat, dungeon_count, items, deck_count, which seats have passed = true, and every seat's successes and failures."
    },
    {
      "action": "poll",
      "who": "all players with eliminated = false",
      "answer": "short text",
      "effect": "Every message is broadcast to all players: 'Seat {seat} says: {value}'. Talk is not binding."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "choice: PASS or DRAW (only PASS when deck_count = 0)",
      "effect": "If PASS: set the active player's passed = true."
    },
    {
      "action": "update",
      "who": "seat active_seat, when they chose DRAW",
      "answer": null,
      "effect": "Pick one card at random from deck, put it in the active player's drawn_card (privately shown to them), remove it from deck, and set deck_count -= 1. Set drawn_strength to its strength: Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9."
    },
    {
      "action": "ask",
      "who": "seat active_seat, when they chose DRAW",
      "answer": "choice: ADD, or SACRIFICE <item> for each item still in items",
      "effect": "Records the decision."
    },
    {
      "action": "update",
      "who": "seat active_seat, when they chose DRAW",
      "answer": null,
      "effect": "If ADD: append drawn_card to dungeon and to the active player's added_cards; dungeon_count += 1; dungeon_total += drawn_strength; if drawn_strength <= 3 then dungeon_low += drawn_strength; if drawn_card is Vampire or Lich then dungeon_undead += drawn_strength; if drawn_card is Dragon then dungeon_dragon += 9. If SACRIFICE X: remove X from items and discard the card unseen. In both cases set drawn_card to empty."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Set active_seat to the next seat clockwise after active_seat whose eliminated = false and passed = false."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1."
    },
    {
      "action": "update",
      "who": "table, when exactly one player has eliminated = false and passed = false",
      "answer": null,
      "effect": "runner_seat = that player's seat. last_hp = 3 + (5 if Armor is in items) + (3 if Shield is in items). last_damage = dungeon_total - (dungeon_low if Torch is in items) - (dungeon_undead if Holy Water is in items) - (dungeon_dragon if Dragon Spear is in items)."
    },
    {
      "action": "tell",
      "who": "all players, when a run happened this round",
      "answer": null,
      "effect": "Reveal every card in dungeon, together with last_damage and last_hp, for runner_seat."
    },
    {
      "action": "update",
      "who": "seat runner_seat, when a run happened this round",
      "answer": null,
      "effect": "If last_damage < last_hp then the runner's successes += 1, otherwise the runner's failures += 1. If the runner's failures >= 2, set the runner's eliminated = true."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if any player has successes >= 2, or if exactly one player has eliminated = false."
    },
    {
      "action": "update",
      "who": "table, when a run happened this round",
      "answer": null,
      "effect": "New dungeon: refill deck with all 13 monsters; deck_count = 13; dungeon = []; dungeon_count = 0; dungeon_total = dungeon_low = dungeon_undead = dungeon_dragon = 0; items = all five; every player's passed = false and added_cards = []; active_seat = the first seat clockwise after runner_seat with eliminated = false."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round >= 40."
    }
  ],
  "ending": {
    "condition": "any player has successes >= 2, OR the count of players with eliminated = false is 1, OR round >= 40",
    "rank_by": "(1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures)",
    "decided_by": "Non-eliminated players rank above eliminated ones. Among them, more successes ranks higher, then fewer failures. A player with 2 successes, or the sole survivor, therefore wins. Players level at the top share the win, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a run happens, the runner's HP is 3, plus 5 if Armor is in items, plus 3 if Shield is in items, so all five items give HP 11."
    },
    {
      "id": "R2",
      "text": "When a run happens, damage is the sum of the dungeon card strengths (Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9)."
    },
    {
      "id": "R3",
      "text": "When Torch is in items at a run, every dungeon card of strength 3 or less adds 0 damage."
    },
    {
      "id": "R4",
      "text": "When Holy Water is in items at a run, every dungeon Vampire and Lich adds 0 damage."
    },
    {
      "id": "R5",
      "text": "When Dragon Spear is in items at a run, the Dragon adds 0 damage."
    },
    {
      "id": "R6",
      "text": "When damage < HP, the runner's successes increase by 1; otherwise (damage >= HP) the runner's failures increase by 1."
    },
    {
      "id": "R7",
      "text": "When a player's failures reach 2, eliminated becomes true and they are no longer asked anything."
    },
    {
      "id": "R8",
      "text": "When the active player chooses PASS, their passed becomes true for the rest of this dungeon."
    },
    {
      "id": "R9",
      "text": "When deck_count is 0, the active player is offered only PASS."
    },
    {
      "id": "R10",
      "text": "When the active player chooses DRAW, one card leaves deck, deck_count drops by 1, and only that player sees it."
    },
    {
      "id": "R11",
      "text": "When the player chooses ADD, the card joins dungeon face-down, dungeon_count rises by 1, and it is added to that player's added_cards."
    },
    {
      "id": "R12",
      "text": "When the player chooses SACRIFICE X, X is removed from items and the card is discarded unseen; SACRIFICE is offered only for items still in items."
    },
    {
      "id": "R13",
      "text": "When a turn ends, active_seat moves to the next seat clockwise with eliminated = false and passed = false."
    },
    {
      "id": "R14",
      "text": "When, at the end of a round, exactly one non-eliminated player has passed = false, that player runs the dungeon."
    },
    {
      "id": "R15",
      "text": "When a run happens, all dungeon cards, the damage and the HP are revealed to everyone."
    },
    {
      "id": "R16",
      "text": "When a run ends without ending the game, the deck is refilled to 13, the dungeon is emptied, all 5 items are restored, all passes are cleared, and active_seat becomes the first surviving seat clockwise from the runner."
    },
    {
      "id": "R17",
      "text": "When a player reaches 2 successes, the game ends and that player wins."
    },
    {
      "id": "R18",
      "text": "When only one player is not eliminated, the game ends and that player wins."
    },
    {
      "id": "R19",
      "text": "When round 40 ends with no winner, the non-eliminated player with the most successes wins, ties are broken by fewer failures, and any remaining tie is shared."
    },
    {
      "id": "R20",
      "text": "Each round, every non-eliminated player sends one short message at the same time, and all messages are then shown to everyone."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every seat with eliminated = false",
      "options": "one short free-text message"
    },
    {
      "question": "Pass or draw",
      "who": "seat active_seat",
      "options": "when deck_count > 0: PASS, DRAW; when deck_count = 0: PASS only"
    },
    {
      "question": "Add or sacrifice",
      "who": "seat active_seat after a DRAW",
      "options": "ADD, plus SACRIFICE <item> for each item still in items (Armor, Shield, Torch, Holy Water, Dragon Spear); when items is empty: ADD only"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The designer's suggested size is 3. Three is the smallest table where the bluff about what was secretly added and the pressure of who ends up running both work. Four is the maximum because the 13-card deck gets thin and turns grow long."
    },
    {
      "what": "Talk is kept as a simultaneous poll with a broadcast",
      "why": "The source says messages are written at the same time without seeing the others. Players disagree, since nobody wants to be the runner, so claims about added cards are worth reasoning about."
    },
    {
      "what": "The dungeon is tracked with hidden counters (total, low, undead, dragon) alongside the card list",
      "why": "These let damage be computed by plain arithmetic, while the card list is what gets revealed."
    },
    {
      "what": "The rank expression gives non-eliminated players +1000",
      "why": "This keeps eliminated players from winning the round-40 tiebreak."
    }
  ],
  "simplifications": [
    {
      "what": "Drawing the top card of a shuffled deck is a random pick from the deck list",
      "why": "The engine shuffles by drawing at random, and the two are equivalent."
    },
    {
      "what": "A draw after round 40 is a shared win among the tied leaders",
      "why": "The engine has no separate draw outcome."
    },
    {
      "what": "The run and the new-dungeon steps are single steps with a 'when' condition",
      "why": "The step list is flat, and these are conditional updates rather than alternative blocks."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: successes, failures, eliminated, passed; table: items, active_seat, deck_count, dungeon_count, runner_seat, last_hp, last_damage, round.
````

## Reply

````
```json
[
  {
    "name": "All five items give the runner HP 11",
    "rule": "R1",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "dungeon": [], "dungeon_count": 0, "dungeon_total": 0, "dungeon_low": 0, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_hp": 11, "last_damage": 0},
      "players": {"3": {"successes": 1, "failures": 0}}
    }
  },
  {
    "name": "Without Armor the HP is 3 + 3 = 6",
    "rule": "R1",
    "players": 3,
    "rounds": 1,
    "seed": 2,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Shield", "Torch", "Holy Water", "Dragon Spear"], "dungeon": [], "dungeon_count": 0, "dungeon_total": 0, "dungeon_low": 0, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_hp": 6, "last_damage": 0}
    }
  },
  {
    "name": "With no items, damage is the sum of strengths (Golem 5 + Orc 3 = 8) against HP 3",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "seed": 3,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": [], "dungeon": ["Golem", "Orc"], "dungeon_count": 2, "dungeon_total": 8, "dungeon_low": 3, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_hp": 3, "last_damage": 8},
      "players": {"3": {"failures": 1, "successes": 0}}
    }
  },
  {
    "name": "Torch removes the cards of strength 3 or less: Goblin+Orc+Golem gives damage 5",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "seed": 4,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Torch"], "dungeon": ["Goblin", "Orc", "Golem"], "dungeon_count": 3, "dungeon_total": 9, "dungeon_low": 4, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"last_hp": 3, "last_damage": 5},
      "players": {"3": {"failures": 1}}
    }
  },
  {
    "name": "Holy Water removes Vampire and Lich: Vampire+Lich+Goblin gives damage 1",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "seed": 5,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Holy Water"], "dungeon": ["Vampire", "Lich", "Goblin"], "dungeon_count": 3, "dungeon_total": 11, "dungeon_low": 1, "dungeon_undead": 10, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"last_hp": 3, "last_damage": 1},
      "players": {"3": {"successes": 1}}
    }
  },
  {
    "name": "Dragon Spear removes the Dragon: Dragon+Skeleton gives damage 2",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "seed": 6,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Dragon Spear"], "dungeon": ["Dragon", "Skeleton"], "dungeon_count": 2, "dungeon_total": 11, "dungeon_low": 2, "dungeon_undead": 0, "dungeon_dragon": 9}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"last_hp": 3, "last_damage": 2},
      "players": {"3": {"successes": 1}}
    }
  },
  {
    "name": "Damage equal to HP (3 vs 3) is a failure",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "seed": 7,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": [], "dungeon": ["Orc"], "dungeon_count": 1, "dungeon_total": 3, "dungeon_low": 3, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"last_hp": 3, "last_damage": 3},
      "players": {"3": {"failures": 1, "successes": 0}}
    }
  },
  {
    "name": "Damage below HP (2 vs 3) is a success",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "seed": 8,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": [], "dungeon": ["Skeleton"], "dungeon_count": 1, "dungeon_total": 2, "dungeon_low": 2, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"last_hp": 3, "last_damage": 2},
      "players": {"3": {"successes": 1, "failures": 0}}
    }
  },
  {
    "name": "A second failure eliminates the runner",
    "rule": "R7",
    "players": 4,
    "rounds": 1,
    "seed": 9,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}, "4": {"passed": true}, "3": {"failures": 1}},
      "game": {"active_seat": 1, "items": [], "dungeon": ["Demon"], "dungeon_count": 1, "dungeon_total": 7, "dungeon_low": 0, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_damage": 7, "last_hp": 3},
      "players": {"3": {"failures": 2, "eliminated": true}, "1": {"eliminated": false}}
    }
  },
  {
    "name": "PASS marks the active player as passed and no run happens yet",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "seed": 10,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "players": {"1": {"passed": true}, "2": {"passed": false}, "3": {"passed": false}},
      "game": {"active_seat": 2, "round": 1, "deck_count": 13}
    }
  },
  {
    "name": "With an empty deck only PASS is offered",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 11,
    "default": "decline",
    "given": {"game": {"active_seat": 1, "deck": [], "deck_count": 0}},
    "expect": {
      "not_offered": [{"seat": 1, "option": "DRAW"}],
      "offered": [{"seat": 1, "option": "PASS"}],
      "players": {"1": {"passed": true}}
    }
  },
  {
    "name": "DRAW takes one card from the deck (which card is chance, only counts asserted)",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "seed": 12,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "DRAW"}, {"seat": 1, "options_include": "ADD"}],
    "expect": {
      "game": {"deck_count": 12},
      "lens": {"game": {"deck": 12}},
      "players": {"1": {"passed": false}}
    }
  },
  {
    "name": "ADD puts the drawn card into the dungeon and the player's added cards",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "seed": 13,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "DRAW"}, {"seat": 1, "options_include": "ADD"}],
    "expect": {
      "game": {"dungeon_count": 1, "deck_count": 12, "items": ["Armor", "Shield", "Torch", "Holy Water", "Dragon Spear"], "active_seat": 2},
      "lens": {"game": {"dungeon": 1}, "players": {"1": {"added_cards": 1}}}
    }
  },
  {
    "name": "SACRIFICE Armor removes Armor and discards the card",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "seed": 14,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "DRAW"}, {"seat": 1, "options_include": "SACRIFICE Armor"}],
    "expect": {
      "game": {"items": ["Shield", "Torch", "Holy Water", "Dragon Spear"], "dungeon_count": 0, "deck_count": 12},
      "lens": {"game": {"dungeon": 0}, "players": {"1": {"added_cards": 0}}}
    }
  },
  {
    "name": "SACRIFICE is offered only for items still present",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "seed": 15,
    "default": "decline",
    "given": {"game": {"items": ["Torch"]}},
    "rules": [{"seat": 1, "options_include": "DRAW"}, {"seat": 1, "options_include": "SACRIFICE Torch"}],
    "expect": {
      "not_offered": [{"seat": 1, "option": "SACRIFICE Armor"}, {"seat": 1, "option": "SACRIFICE Shield"}, {"seat": 1, "option": "SACRIFICE Holy Water"}, {"seat": 1, "option": "SACRIFICE Dragon Spear"}],
      "game": {"items": [], "dungeon_count": 0}
    }
  },
  {
    "name": "The turn skips eliminated and passed seats",
    "rule": "R13",
    "players": 4,
    "rounds": 1,
    "seed": 16,
    "default": "decline",
    "given": {
      "players": {"2": {"eliminated": true, "failures": 2}, "3": {"passed": true}},
      "game": {"active_seat": 1}
    },
    "rules": [{"seat": 1, "options_include": "DRAW"}, {"seat": 1, "options_include": "ADD"}],
    "expect": {
      "game": {"active_seat": 4, "dungeon_count": 1},
      "not_offered": [{"seat": 2, "option": "DRAW"}, {"seat": 3, "option": "DRAW"}],
      "players": {"4": {"successes": 0, "failures": 0}}
    }
  },
  {
    "name": "The last seat that has not passed runs the dungeon",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "seed": 17,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "dungeon": ["Goblin"], "dungeon_count": 1, "dungeon_total": 1, "dungeon_low": 1, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_hp": 11, "last_damage": 0},
      "players": {"3": {"successes": 1}, "1": {"successes": 0, "failures": 0}, "2": {"successes": 0, "failures": 0}}
    }
  },
  {
    "name": "A run publishes its damage and HP",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "seed": 18,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Armor"], "dungeon": ["Golem", "Vampire"], "dungeon_count": 2, "dungeon_total": 9, "dungeon_low": 0, "dungeon_undead": 4, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"runner_seat": 3, "last_hp": 8, "last_damage": 9},
      "players": {"3": {"failures": 1}}
    }
  },
  {
    "name": "After a run the dungeon is reset and the seat after the runner starts",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "seed": 19,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}},
      "game": {"active_seat": 1, "items": ["Armor", "Torch"], "deck": ["Orc", "Orc", "Vampire", "Vampire", "Golem"], "deck_count": 5, "dungeon": ["Goblin", "Skeleton"], "dungeon_count": 2, "dungeon_total": 3, "dungeon_low": 3, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"deck_count": 13, "dungeon_count": 0, "items": ["Armor", "Shield", "Torch", "Holy Water", "Dragon Spear"], "active_seat": 1, "runner_seat": 3, "last_hp": 8, "last_damage": 0},
      "players": {"1": {"passed": false}, "2": {"passed": false}, "3": {"passed": false, "successes": 1}},
      "lens": {"game": {"deck": 13, "dungeon": 0}}
    }
  },
  {
    "name": "A second success wins the game",
    "rule": "R17",
    "players": 3,
    "seed": 20,
    "default": "decline",
    "given": {
      "players": {"2": {"passed": true}, "3": {"successes": 1}},
      "game": {"active_seat": 1, "dungeon": [], "dungeon_count": 0, "dungeon_total": 0, "dungeon_low": 0, "dungeon_undead": 0, "dungeon_dragon": 0}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "winner": 3,
      "standings": {"1": 1002, "2": 1002, "3": 1022},
      "players": {"3": {"successes": 2}}
    }
  },
  {
    "name": "The sole survivor wins when the other runner is eliminated",
    "rule": "R18",
    "players": 3,
    "seed": 21,
    "default": "decline",
    "given": {
      "players": {"2": {"eliminated": true, "failures": 2}, "3": {"failures": 1}},
      "game": {"active_seat": 1, "items": [], "dungeon": ["Dragon"], "dungeon_count": 1, "dungeon_total": 9, "dungeon_low": 0, "dungeon_undead": 0, "dungeon_dragon": 9}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "winner": 1,
      "standings": {"1": 1002, "2": 0, "3": 0},
      "players": {"3": {"failures": 2, "eliminated": true}}
    }
  },
  {
    "name": "At round 40 the most successes wins",
    "rule": "R19",
    "players": 3,
    "seed": 22,
    "default": "decline",
    "given": {
      "players": {"2": {"successes": 1}, "3": {"successes": 1, "failures": 1}},
      "game": {"active_seat": 1, "round": 39}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "winner": 2,
      "standings": {"1": 1002, "2": 1012, "3": 1011},
      "game": {"round": 40}
    }
  },
  {
    "name": "At round 40 a tie on successes and failures is shared",
    "rule": "R19",
    "players": 3,
    "seed": 23,
    "default": "decline",
    "given": {
      "players": {"2": {"successes": 1}, "3": {"successes": 1}},
      "game": {"active_seat": 1, "round": 39}
    },
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 1002, "2": 1012, "3": 1012}
    }
  },
  {
    "name": "Talk does not change the state; the round goes on",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "seed": 24,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "PASS"}],
    "expect": {
      "game": {"round": 1, "active_seat": 2, "deck_count": 13},
      "players": {"1": {"passed": true, "successes": 0}, "2": {"successes": 0}, "3": {"successes": 0}}
    }
  }
]
```
````
