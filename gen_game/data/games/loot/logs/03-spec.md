# 03 spec

- time: 2026-10-28T05:04:19+00:00 (47.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 311776bad5e02c46, reply sha256 f68c311ae957932b

## Sent

````
Game: Loot: Sealed Raids
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP: Each player starts with 30 crew (private: only that player and the engine know their remaining crew), 0 gold, three unsailed merchant ships worth 3, 5 and 7 gold, one unused Captain and one unused Admiral. Players are seated 1 to N. The game lasts 3 x N rounds (12 with 4 players).

EACH ROUND:
1. Owner. The owner is player ((round - 1) mod N) + 1. Each player is owner exactly 3 times. The engine announces who the owner is and which of the owner's ships are still unsailed.
2. Sail. The owner privately chooses one of their unsailed ships to sail. If only one remains, it is sailed automatically. Its value is not yet revealed.
3. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.
4. Commit. At the same moment, every player secretly chooses a whole number of crew to commit, from 0 up to their remaining crew. In the same poll, the owner may declare their Admiral if it is unused, and each non-owner may declare their Captain if it is unused. Invalid amounts are set to 0. Invalid trump declarations are ignored.
5. Spend. Every player's committed crew is subtracted from their remaining crew, whatever the result.
6. Strength. The owner's defense equals the crew they committed. Each attacker's strength equals the crew they committed, plus 6 if they declared their Captain this round.
7. Resolve. The rules are applied in this order:
   (a) If the owner declared the Admiral, the owner keeps the ship.
   (b) Otherwise, find the highest attacker strength. The ship goes to that attacker only if their strength is strictly greater than the owner's defense and strictly greater than every other attacker's strength.
   (c) In every other case, including ties between the top attackers or an attack that does not beat the defense, the owner keeps the ship.
8. Score. Whoever gets the ship adds its value to their gold.
9. Bookkeeping. The ship is marked sailed. Declared trumps are marked used.
10. Announce. The engine reveals the ship's value, who got it, and who used a Captain or Admiral this round. It does not reveal any crew amounts.
11. Advance. Move to the next round, or end the game after round 3 x N.

END: Unspent crew is worth nothing.

How the winner is decided: After the final round, the player with the most gold wins. If two or more players tie for the most gold, the game is a draw.
````

## Reply

````
```json
{
  "name": "Loot: Sealed Raids",
  "summary": "Each round one seat sails a hidden-value merchant ship and every seat secretly commits crew from a fixed budget of 30 to defend it or raid it, with one-shot Captain and Admiral trumps. The most gold after 3 x N rounds wins.",
  "players": {"min": 3, "max": 5, "suggested": 4},
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
      {"key": "crew", "type": "number", "visible": "ally", "initial": 30, "meaning": "Remaining crew. Only the owner of the attribute and the engine know it.", "observable": false},
      {"key": "gold", "type": "number", "visible": "public", "initial": 0, "meaning": "Gold won from ships. This is the score.", "observable": true},
      {"key": "ships", "type": "list", "visible": "public", "initial": [3, 5, 7], "meaning": "Values of this player's unsailed ships. A value is removed only at bookkeeping, after it has been revealed.", "observable": true},
      {"key": "captain_used", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this player's Captain has been used.", "observable": true},
      {"key": "admiral_used", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this player's Admiral has been used.", "observable": true},
      {"key": "committed", "type": "number", "visible": "ally", "initial": 0, "meaning": "Crew this player committed this round.", "observable": false},
      {"key": "trump_declared", "type": "bool", "visible": "ally", "initial": false, "meaning": "Whether this player validly declared a trump this round (an Admiral for the owner, a Captain for a non-owner).", "observable": false},
      {"key": "strength", "type": "number", "visible": "ally", "initial": 0, "meaning": "This round's strength: committed crew, plus 6 for an attacker who declared the Captain. For the owner it is the defense.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Current round number.", "observable": true},
      {"key": "owner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of this round's owner: ((round - 1) mod N) + 1.", "observable": true},
      {"key": "current_ship", "type": "number", "visible": "none", "initial": 0, "meaning": "Value of the ship sailed this round. It stays hidden until the announcement.", "observable": false},
      {"key": "last_ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Value of the ship revealed at the end of the round.", "observable": true},
      {"key": "last_taker", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that got this round's ship.", "observable": true},
      {"key": "defense", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: the owner's defense this round.", "observable": false},
      {"key": "top_attack", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: the highest attacker strength this round.", "observable": false},
      {"key": "top_count", "type": "number", "visible": "none", "initial": 0, "meaning": "Scratch value: how many attackers have the highest strength.", "observable": false}
    ]
  },
  "setup": [
    "Seat the players 1 to N.",
    "Every player gets 30 crew (private), 0 gold, unsailed ships worth 3, 5 and 7 gold, an unused Captain and an unused Admiral.",
    "Set round to 0. The game lasts 3 x N rounds."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; owner = ((round - 1) mod N) + 1; for every player, set committed = 0, trump_declared = false and strength = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'Round {round}: Seat {owner} is the owner. Unsailed ships: {owner.ships}.'"},
    {"action": "update", "who": "seat owner", "answer": null, "effect": "When the length of owner.ships = 1, set current_ship = the only value in owner.ships (it sails automatically)."},
    {"action": "ask", "who": "seat owner", "answer": "one value from owner.ships", "effect": "When the length of owner.ships > 1, set current_ship = the chosen value. The choice is private."},
    {"action": "poll", "who": "all players", "answer": "short text", "effect": "Every message is shown to everyone after all are in: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk binds no one."},
    {"action": "poll", "who": "all players", "answer": "A whole number of crew from 0 to your crew. Also a trump choice: the owner chooses 'none' or 'admiral', with 'admiral' offered only if admiral_used is false; a non-owner chooses 'none' or 'captain', with 'captain' offered only if captain_used is false.", "effect": "committed = the amount, or 0 if the amount is invalid. trump_declared = true only for a valid declaration; an invalid declaration is ignored."},
    {"action": "update", "who": "all players", "answer": null, "effect": "crew -= committed. strength = committed + (6 if the seat is not the owner and trump_declared, else 0). defense = owner.strength."},
    {"action": "update", "who": "all players", "answer": null, "effect": "top_attack = the highest strength among non-owners; top_count = the number of non-owners whose strength = top_attack. If owner.trump_declared, last_taker = owner. Otherwise, if top_attack > defense and top_count = 1, last_taker = the non-owner whose strength = top_attack. Otherwise last_taker = owner."},
    {"action": "update", "who": "all players", "answer": null, "effect": "The player in seat last_taker adds current_ship to gold. last_ship_value = current_ship."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Remove current_ship from owner.ships. If owner.trump_declared, set owner.admiral_used = true. For each non-owner with trump_declared, set captain_used = true."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce: 'The ship was worth {last_ship_value}. Seat {last_taker} got it.' Then list who used a Captain or Admiral this round. No crew amounts are revealed."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round >= 3 * N; otherwise continue."}
  ],
  "ending": {
    "condition": "round >= 3 * N",
    "rank_by": "you.gold",
    "decided_by": "Each player's standing is their gold. The player with the most gold wins. Players tied for the most gold share the result, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then each player has 30 crew, 0 gold, ships [3, 5, 7], an unused Captain and an unused Admiral."},
    {"id": "R2", "text": "When it is round r, then the owner is seat ((r - 1) mod N) + 1, so with 4 players round 5 is owned by seat 1."},
    {"id": "R3", "text": "When the game has N players, then it lasts 3 x N rounds (12 with 4 players) and each seat is owner exactly 3 times."},
    {"id": "R4", "text": "When a round begins, then the owner and the owner's unsailed ships are announced."},
    {"id": "R5", "text": "When the owner has more than one unsailed ship, then the owner privately chooses which one sails."},
    {"id": "R6", "text": "When the owner has exactly one unsailed ship, then it sails automatically."},
    {"id": "R7", "text": "When a ship sails, then its value is not revealed until the end-of-round announcement."},
    {"id": "R8", "text": "When the talk step runs, then every player writes one message at the same time and all messages are shown to everyone only after all are in."},
    {"id": "R9", "text": "When crew is committed, then every player chooses at the same time a whole number from 0 to their remaining crew."},
    {"id": "R10", "text": "When a committed amount is invalid, then it is set to 0."},
    {"id": "R11", "text": "When a player commits crew, then it is subtracted from their crew whatever the result, so 30 crew minus a commit of 10 leaves 20."},
    {"id": "R12", "text": "When a non-owner declares an unused Captain, then their strength is their committed crew + 6."},
    {"id": "R13", "text": "When the owner declares an unused Admiral, then the owner keeps the ship regardless of any attack."},
    {"id": "R14", "text": "When a trump declaration is invalid (already used, or the wrong role), then it is ignored."},
    {"id": "R15", "text": "When no Admiral is declared and one attacker's strength is strictly greater than the defense and strictly greater than every other attacker's, then that attacker gets the ship (attack 8 against defense 7 wins)."},
    {"id": "R16", "text": "When the highest attacker strength equals the defense, then the owner keeps the ship (attack 7 against defense 7 loses)."},
    {"id": "R17", "text": "When two or more attackers tie for the highest strength, then the owner keeps the ship, even if that strength beats the defense."},
    {"id": "R18", "text": "When a player gets a ship, then they add its value to their gold."},
    {"id": "R19", "text": "When the round ends, then the sailed ship is removed from the owner's unsailed ships and declared trumps are marked used."},
    {"id": "R20", "text": "When the round ends, then the ship's value, its taker and who used a Captain or Admiral are announced, but no crew amounts are."},
    {"id": "R21", "text": "When the game ends, then unspent crew is worth 0 and the player with the most gold wins; players tied for the most gold share the result, standing for the source's draw."}
  ],
  "offers": [
    {"question": "Sail: which ship to sail", "who": "the owner, only when they have 2 or more unsailed ships", "options": "each value in owner.ships"},
    {"question": "Talk message", "who": "all seats", "options": "a short free-text message"},
    {"question": "Commit: crew amount", "who": "all seats", "options": "a whole number from 0 to that seat's crew"},
    {"question": "Commit: trump", "who": "all seats", "options": "The owner with an unused Admiral: none, admiral. The owner with a used Admiral: none. A non-owner with an unused Captain: none, captain. A non-owner with a used Captain: none."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer suggests 4, and the minimum of 3 keeps it from being a plain duel. Two or more raiders are needed for ties between attackers and for a raider to free-ride while others overbid. Beyond 5 players each seat is owner rarely and the ties between attackers dominate."},
    {"what": "Keep the simultaneous talk poll", "why": "The source requires it. Players have opposing interests over who raids which ship, so a non-binding message can bluff, threaten or deter, and following someone else's proposal can cost a player."},
    {"what": "The unsailed-ships list is public and a value is removed only at bookkeeping", "why": "The source announces the owner's unsailed ships each round. Removing the value at sail time would leak the hidden value before the announcement."},
    {"what": "Strategy at the table", "why": "A thoughtful player rations 30 crew over 3 x N rounds. They infer which ship sailed from the remaining list, time the one-shot Admiral and Captain, and use talk to bluff or provoke ties between rival raiders."}
  ],
  "simplifications": [
    {"what": "A tie for the most gold is a shared win instead of a draw", "why": "The engine ranks by an arithmetic expression and players level at the top share the win. This is the closest equivalent to 'the game is a draw'."},
    {"what": "The commit poll offers only valid amounts and valid trumps", "why": "The engine constrains answers to the offered range, so the source's 'invalid amounts are set to 0' and 'invalid trumps are ignored' rarely trigger. Both are kept as rules anyway."}
  ],
  "unsupported": []
}
```
````
