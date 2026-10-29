# 03 spec

- time: 2026-10-28T05:45:53+00:00 (61.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 51485a04f9c171cf, reply sha256 6e3231332de6dc7f

## Sent

````
Game: Back to the Dungeon: Single Delve
Players in the source: 3 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
COMPONENTS
- The adventurer has base HP 3 and five equipment items:
  - Armor: +5 HP.
  - Shield: +3 HP.
  - Torch: defeats every monster of strength 3 or less.
  - Holy Water: defeats Vampires and the Lich.
  - Dragon Spear: defeats the Dragon.
- Monster deck (13 cards): Goblin 1 x2, Skeleton 2 x2, Orc 3 x2, Vampire 4 x2, Golem 5 x2, Lich 6 x1, Demon 7 x1, Dragon 9 x1.
- Each player tracks successes (start 0) and failures (start 0).

SETUP
- Seat players in a fixed order. Player 1 begins the first dungeon.
- Shuffle the deck. The dungeon starts empty. All five items are present. No one has passed.

EACH ROUND (one turn)
1. Announcement. The engine announces to everyone:
   - whose turn it is (the active player);
   - the number of cards in the dungeon;
   - which equipment items remain;
   - the number of cards left in the deck;
   - who has passed;
   - everyone's successes and failures.
2. Talk. Every surviving (not eliminated) player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Pass or draw. The active player chooses PASS or DRAW.
   - If the deck is empty, the active player must PASS.
   - PASS: the player sits out the rest of this dungeon.
4. Secret draw. If the player chose DRAW, they privately see the top card of the deck, which leaves the deck. They then choose one of:
   - ADD: the card goes face-down into the dungeon. Only this player knows what it is.
   - SACRIFICE an item: one remaining equipment item (the player names which) is permanently removed for this dungeon, and the card is discarded unseen by others. This is allowed only if at least one item remains.
5. Advance. The turn passes to the next player clockwise who is neither eliminated nor passed in this dungeon.

THE RUN
- The run happens at the end of a round as soon as exactly one non-eliminated player has not passed. That player is the runner.
- HP = 3, plus 5 if Armor remains, plus 3 if Shield remains.
- Damage = the sum of the strengths of all dungeon cards, minus the strength of each card defeated by a remaining item:
  - Torch defeats strength 1, 2 and 3.
  - Holy Water defeats Vampires and the Lich.
  - Dragon Spear defeats the Dragon.
- All dungeon cards are then revealed to everyone, along with the damage and HP.
- If damage < HP, the runner gains 1 success. Otherwise the runner gains 1 failure.
- A player with 2 failures is eliminated and takes no further part.

NEW DUNGEON
- After a run, reshuffle all 13 monsters into a new deck.
- Empty the dungeon, restore all five items, and clear all passes.
- The next active player is the first surviving player clockwise from the runner.

GAME END
- The game ends immediately when:
  - a player reaches 2 successes (that player wins); or
  - only one player is not eliminated (that player wins).
- Otherwise the game ends after round 40. The surviving player with the most successes wins. If tied, the one among them with the fewest failures wins. If still tied, the game is a draw.

How the winner is decided: The first player to reach 2 successes wins. A player is also the winner if every other player has been eliminated by 2 failures. If neither happens by the end of round 40: among non-eliminated players, the highest successes wins, then the fewest failures; any remaining tie is a draw.
````

## Reply

````
```json
{
  "name": "Back to the Dungeon: Single Delve",
  "summary": "Players take turns drawing monsters and either secretly add them to a shared dungeon or sacrifice equipment. The last player who has not passed must run the dungeon. The first to 2 successful runs wins; 2 failures eliminate a player.",
  "players": {"min": 3, "max": 4, "suggested": 3},
  "parameters": {
    "base_hp": 3,
    "armor_hp": 5,
    "shield_hp": 3,
    "torch_max_strength": 3,
    "goblin_strength": 1, "goblin_count": 2,
    "skeleton_strength": 2, "skeleton_count": 2,
    "orc_strength": 3, "orc_count": 2,
    "vampire_strength": 4, "vampire_count": 2,
    "golem_strength": 5, "golem_count": 2,
    "lich_strength": 6, "lich_count": 1,
    "demon_strength": 7, "demon_count": 1,
    "dragon_strength": 9, "dragon_count": 1,
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
      {"key": "successes", "type": "number", "visible": "public", "initial": 0, "meaning": "successful runs", "observable": true},
      {"key": "failures", "type": "number", "visible": "public", "initial": 0, "meaning": "failed runs", "observable": true},
      {"key": "eliminated", "type": "bool", "visible": "public", "initial": false, "meaning": "true once the player has 2 failures", "observable": true},
      {"key": "passed", "type": "bool", "visible": "public", "initial": false, "meaning": "the player has passed in the current dungeon", "observable": true},
      {"key": "drawn_card", "type": "text", "visible": "ally", "initial": "", "meaning": "the monster this player just drew and is deciding on; empty otherwise", "observable": false},
      {"key": "added_cards", "type": "list", "visible": "ally", "initial": [], "meaning": "the monsters this player has added face-down to the current dungeon (only they know them)", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": ["Goblin", "Goblin", "Skeleton", "Skeleton", "Orc", "Orc", "Vampire", "Vampire", "Golem", "Golem", "Lich", "Demon", "Dragon"], "meaning": "the shuffled monster deck", "observable": false},
      {"key": "dungeon", "type": "list", "visible": "none", "initial": [], "meaning": "the face-down monsters in the current dungeon", "observable": false},
      {"key": "items", "type": "list", "visible": "public", "initial": ["Armor", "Shield", "Torch", "Holy Water", "Dragon Spear"], "meaning": "the equipment items remaining in this dungeon", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "the seat whose turn it is", "observable": true},
      {"key": "deck_count", "type": "number", "visible": "public", "initial": 13, "meaning": "cards left in the deck", "observable": true},
      {"key": "dungeon_count", "type": "number", "visible": "public", "initial": 0, "meaning": "cards in the dungeon", "observable": true},
      {"key": "drawn_strength", "type": "number", "visible": "none", "initial": 0, "meaning": "strength of the card just drawn (scratch)", "observable": false},
      {"key": "dungeon_total", "type": "number", "visible": "none", "initial": 0, "meaning": "sum of the strengths of the dungeon cards", "observable": false},
      {"key": "dungeon_low", "type": "number", "visible": "none", "initial": 0, "meaning": "sum of the strengths of dungeon cards of strength 3 or less (Torch targets)", "observable": false},
      {"key": "dungeon_undead", "type": "number", "visible": "none", "initial": 0, "meaning": "sum of the strengths of dungeon Vampires and the Lich (Holy Water targets)", "observable": false},
      {"key": "dungeon_dragon", "type": "number", "visible": "none", "initial": 0, "meaning": "strength of the Dragon if it is in the dungeon (Dragon Spear target)", "observable": false},
      {"key": "runner_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "the seat that ran the last dungeon", "observable": true},
      {"key": "last_hp", "type": "number", "visible": "public", "initial": 0, "meaning": "the runner's HP in the last run", "observable": true},
      {"key": "last_damage", "type": "number", "visible": "public", "initial": 0, "meaning": "the damage in the last run", "observable": true},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "rounds completed", "observable": true}
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
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce active_seat, dungeon_count, items, deck_count, which seats have passed = true, and every seat's successes and failures."},
    {"action": "poll", "who": "all players with eliminated = false", "answer": "short text", "effect": "Every message is broadcast to all players: 'Seat {seat} says: {value}'. Talk is not binding."},
    {"action": "ask", "who": "seat active_seat", "answer": "choice: PASS or DRAW (only PASS when deck_count = 0)", "effect": "If PASS: set the active player's passed = true."},
    {"action": "update", "who": "seat active_seat, when they chose DRAW", "answer": null, "effect": "Pick one card at random from deck, put it in the active player's drawn_card (privately shown to them), remove it from deck, and set deck_count -= 1. Set drawn_strength to its strength: Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9."},
    {"action": "ask", "who": "seat active_seat, when they chose DRAW", "answer": "choice: ADD, or SACRIFICE <item> for each item still in items", "effect": "Records the decision."},
    {"action": "update", "who": "seat active_seat, when they chose DRAW", "answer": null, "effect": "If ADD: append drawn_card to dungeon and to the active player's added_cards; dungeon_count += 1; dungeon_total += drawn_strength; if drawn_strength <= 3 then dungeon_low += drawn_strength; if drawn_card is Vampire or Lich then dungeon_undead += drawn_strength; if drawn_card is Dragon then dungeon_dragon += 9. If SACRIFICE X: remove X from items and discard the card unseen. In both cases set drawn_card to empty."},
    {"action": "update", "who": "table", "answer": null, "effect": "Set active_seat to the next seat clockwise after active_seat whose eliminated = false and passed = false."},
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1."},
    {"action": "update", "who": "table, when exactly one player has eliminated = false and passed = false", "answer": null, "effect": "runner_seat = that player's seat. last_hp = 3 + (5 if Armor is in items) + (3 if Shield is in items). last_damage = dungeon_total - (dungeon_low if Torch is in items) - (dungeon_undead if Holy Water is in items) - (dungeon_dragon if Dragon Spear is in items)."},
    {"action": "tell", "who": "all players, when a run happened this round", "answer": null, "effect": "Reveal every card in dungeon, together with last_damage and last_hp, for runner_seat."},
    {"action": "update", "who": "seat runner_seat, when a run happened this round", "answer": null, "effect": "If last_damage < last_hp then the runner's successes += 1, otherwise the runner's failures += 1. If the runner's failures >= 2, set the runner's eliminated = true."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if any player has successes >= 2, or if exactly one player has eliminated = false."},
    {"action": "update", "who": "table, when a run happened this round", "answer": null, "effect": "New dungeon: refill deck with all 13 monsters; deck_count = 13; dungeon = []; dungeon_count = 0; dungeon_total = dungeon_low = dungeon_undead = dungeon_dragon = 0; items = all five; every player's passed = false and added_cards = []; active_seat = the first seat clockwise after runner_seat with eliminated = false."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if round >= 40."}
  ],
  "ending": {
    "condition": "any player has successes >= 2, OR the count of players with eliminated = false is 1, OR round >= 40",
    "rank_by": "(1 - you.eliminated) * 1000 + you.successes * 10 + (2 - you.failures)",
    "decided_by": "Non-eliminated players rank above eliminated ones. Among them, more successes ranks higher, then fewer failures. A player with 2 successes, or the sole survivor, therefore wins. Players level at the top share the win, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When a run happens, the runner's HP is 3, plus 5 if Armor is in items, plus 3 if Shield is in items, so all five items give HP 11."},
    {"id": "R2", "text": "When a run happens, damage is the sum of the dungeon card strengths (Goblin 1, Skeleton 2, Orc 3, Vampire 4, Golem 5, Lich 6, Demon 7, Dragon 9)."},
    {"id": "R3", "text": "When Torch is in items at a run, every dungeon card of strength 3 or less adds 0 damage."},
    {"id": "R4", "text": "When Holy Water is in items at a run, every dungeon Vampire and Lich adds 0 damage."},
    {"id": "R5", "text": "When Dragon Spear is in items at a run, the Dragon adds 0 damage."},
    {"id": "R6", "text": "When damage < HP, the runner's successes increase by 1; otherwise (damage >= HP) the runner's failures increase by 1."},
    {"id": "R7", "text": "When a player's failures reach 2, eliminated becomes true and they are no longer asked anything."},
    {"id": "R8", "text": "When the active player chooses PASS, their passed becomes true for the rest of this dungeon."},
    {"id": "R9", "text": "When deck_count is 0, the active player is offered only PASS."},
    {"id": "R10", "text": "When the active player chooses DRAW, one card leaves deck, deck_count drops by 1, and only that player sees it."},
    {"id": "R11", "text": "When the player chooses ADD, the card joins dungeon face-down, dungeon_count rises by 1, and it is added to that player's added_cards."},
    {"id": "R12", "text": "When the player chooses SACRIFICE X, X is removed from items and the card is discarded unseen; SACRIFICE is offered only for items still in items."},
    {"id": "R13", "text": "When a turn ends, active_seat moves to the next seat clockwise with eliminated = false and passed = false."},
    {"id": "R14", "text": "When, at the end of a round, exactly one non-eliminated player has passed = false, that player runs the dungeon."},
    {"id": "R15", "text": "When a run happens, all dungeon cards, the damage and the HP are revealed to everyone."},
    {"id": "R16", "text": "When a run ends without ending the game, the deck is refilled to 13, the dungeon is emptied, all 5 items are restored, all passes are cleared, and active_seat becomes the first surviving seat clockwise from the runner."},
    {"id": "R17", "text": "When a player reaches 2 successes, the game ends and that player wins."},
    {"id": "R18", "text": "When only one player is not eliminated, the game ends and that player wins."},
    {"id": "R19", "text": "When round 40 ends with no winner, the non-eliminated player with the most successes wins, ties are broken by fewer failures, and any remaining tie is shared."},
    {"id": "R20", "text": "Each round, every non-eliminated player sends one short message at the same time, and all messages are then shown to everyone."}
  ],
  "offers": [
    {"question": "Talk message", "who": "every seat with eliminated = false", "options": "one short free-text message"},
    {"question": "Pass or draw", "who": "seat active_seat", "options": "when deck_count > 0: PASS, DRAW; when deck_count = 0: PASS only"},
    {"question": "Add or sacrifice", "who": "seat active_seat after a DRAW", "options": "ADD, plus SACRIFICE <item> for each item still in items (Armor, Shield, Torch, Holy Water, Dragon Spear); when items is empty: ADD only"}
  ],
  "choices": [
    {"what": "3 to 4 players, suggested 3", "why": "The designer's suggested size is 3. Three is the smallest table where the bluff about what was secretly added and the pressure of who ends up running both work. Four is the maximum because the 13-card deck gets thin and turns grow long."},
    {"what": "Talk is kept as a simultaneous poll with a broadcast", "why": "The source says messages are written at the same time without seeing the others. Players disagree, since nobody wants to be the runner, so claims about added cards are worth reasoning about."},
    {"what": "The dungeon is tracked with hidden counters (total, low, undead, dragon) alongside the card list", "why": "These let damage be computed by plain arithmetic, while the card list is what gets revealed."},
    {"what": "The rank expression gives non-eliminated players +1000", "why": "This keeps eliminated players from winning the round-40 tiebreak."}
  ],
  "simplifications": [
    {"what": "Drawing the top card of a shuffled deck is a random pick from the deck list", "why": "The engine shuffles by drawing at random, and the two are equivalent."},
    {"what": "A draw after round 40 is a shared win among the tied leaders", "why": "The engine has no separate draw outcome."},
    {"what": "The run and the new-dungeon steps are single steps with a 'when' condition", "why": "The step list is flat, and these are conditional updates rather than alternative blocks."}
  ],
  "unsupported": []
}
```
````
