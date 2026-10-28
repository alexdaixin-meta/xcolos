# 04 spec

- time: 2026-10-28T01:34:46+00:00 (55.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 8145f1c4abd27cfb, reply sha256 0b623a008cd35bf0

## Sent

````
Game: Deception: Five Clues
Players in the source: 6 to 8
Suggested table size, chosen by the designer of these rules (keep it): 7

Rules, as filed in the inventory:
ROLES. One player is publicly the Forensic Scientist (seat 1). The engine secretly and randomly deals the other players these roles: 1 Murderer, 1 Accomplice, 1 Witness, and Investigators for the rest (2, 3 or 4 Investigators with 6, 7 or 8 players). The Murderer and Accomplice are the Murderer side. The Scientist, Witness and Investigators are the Investigator side. The Accomplice is told who the Murderer is. The Witness is told who the Murderer and Accomplice are, but not which of the two is which, and not the solution. The Scientist is told all roles.

CARDS. Every player except the Scientist is dealt, face up for all to see, 2 Clue words from the Clue list and 2 Means words from the Means list, with no repeats.
- Clue list (16): Glove, Train Ticket, Lipstick, Key, Diary, Ring, Cigarette, Phone, Wallet, Photo, Watch, Umbrella, Receipt, Hair, Button, Mask.
- Means list (16): Rope, Poison, Knife, Pillow, Hammer, Pistol, Insulin, Brick, Drowning, Electric Wire, Scarf, Bare Hands, Fire, Bottle, Axe, Car.

SOLUTION. The Murderer privately chooses one of their own 2 Clues as the Key Evidence and one of their own 2 Means as the Means of Murder. The engine then privately tells the Scientist and the Accomplice the solution.

SCENE TILES. Each tile lists 6 options.
- Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident.
- Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office.
The Deck holds 6 tiles:
- Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night.
- Weather: Sunny, Stormy, Dry, Humid, Cold, Hot.
- Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit.
- Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar.
- Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted.
- Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear.

BADGES. Every player except the Scientist starts with 1 badge.

EACH ROUND (5 rounds):
1. Tile. In round 1 the tile is Cause of Death. In round 2 it is Location. In rounds 3, 4 and 5, one tile is drawn at random from the Deck and removed.
2. Marker. The Scientist privately chooses exactly one of the tile's 6 options, and the marked option is announced to all. The Scientist may never send any other message.
3. Talk. Every player except the Scientist writes one short message at the same time. All messages are then shown to everyone.
4. Accusation. Every player who still has a badge chooses at the same time either PASS or one accusation: one Clue word and one Means word currently on the table. Anyone who accuses loses their badge.
5. Resolution. Every accusation is announced with its accuser. An accusation is correct only if its Clue is the Key Evidence and its Means is the Means of Murder, and each is announced as correct or wrong. A pair taken from two different players' cards is always wrong. If any accusation is correct, the case is SOLVED and play moves to the Witness Hunt. Otherwise the next round begins.

WITNESS HUNT. When the case is solved, the Murderer privately names one player other than the Scientist, the Accomplice and themself. If that player is the Witness, the Murderer side wins. Otherwise the Investigator side wins.

END. If the case is not solved by the end of round 5, the Murderer side wins.

How the winner is decided: Team win, decided purely by matching. If any accusation exactly matches the secret Clue and Means, and the Murderer then fails to name the Witness, the Scientist, the Witness and all Investigators win. If the Murderer names the Witness correctly after a solve, or if no correct accusation happens within 5 rounds, the Murderer and Accomplice win. There are no draws.
````

## Reply

````
```json
{
  "name": "Deception: Five Clues",
  "summary": "A hidden-role deduction game. A public Forensic Scientist marks scene-tile options to steer Investigators towards the Murderer's secret Clue and Means. The Murderer side wins by evading for 5 rounds, or by finding the Witness after the case is solved.",
  "players": {"min": 6, "max": 8, "suggested": 7},
  "parameters": {
    "rounds": 5,
    "scientist_seat": 1,
    "clue_list_size": 16,
    "means_list_size": 16,
    "clues_per_player": 2,
    "means_per_player": 2,
    "starting_badges": 1,
    "options_per_tile": 6,
    "deck_tiles": 6,
    "deck_draws": 3,
    "murderers": 1,
    "accomplices": 1,
    "witnesses": 1,
    "investigators_formula_offset": 4,
    "win_value": 1
  },
  "attributes": {
    "player": [
      {"key": "role", "type": "text", "visible": "ally", "initial": "dealt: Scientist for seat 1; for the other seats a random one of Murderer, Accomplice, Witness, or Investigator (player count minus 4 Investigators)", "meaning": "secret role; the Scientist's role is publicly known", "observable": false},
      {"key": "side", "type": "text", "visible": "ally", "initial": "murderer for Murderer and Accomplice, investigator otherwise", "meaning": "team", "observable": false},
      {"key": "intel", "type": "text", "visible": "ally", "initial": "Accomplice: the Murderer's seat; Witness: the two seats of the Murderer and Accomplice in random order; Scientist: every seat's role; others: empty", "meaning": "private role knowledge given at setup", "observable": false},
      {"key": "solution_known", "type": "text", "visible": "ally", "initial": "", "meaning": "Key Evidence and Means of Murder, filled in for the Scientist and the Accomplice", "observable": false},
      {"key": "clues", "type": "list", "visible": "public", "initial": "2 Clue words drawn from clue_deck (empty for seat 1)", "meaning": "face-up Clue cards", "observable": true},
      {"key": "means", "type": "list", "visible": "public", "initial": "2 Means words drawn from means_deck (empty for seat 1)", "meaning": "face-up Means cards", "observable": true},
      {"key": "badge", "type": "number", "visible": "public", "initial": "1 (0 for seat 1)", "meaning": "accusations remaining", "observable": true},
      {"key": "acc_clue", "type": "text", "visible": "public", "initial": "", "meaning": "this round's accused Clue, or PASS; revealed at resolution", "observable": false},
      {"key": "acc_means", "type": "text", "visible": "public", "initial": "", "meaning": "this round's accused Means; revealed at resolution", "observable": false},
      {"key": "won", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if this player's side won", "observable": true}
    ],
    "game": [
      {"key": "clue_deck", "type": "list", "visible": "none", "initial": ["Glove", "Train Ticket", "Lipstick", "Key", "Diary", "Ring", "Cigarette", "Phone", "Wallet", "Photo", "Watch", "Umbrella", "Receipt", "Hair", "Button", "Mask"], "meaning": "undealt Clue words", "observable": false},
      {"key": "means_deck", "type": "list", "visible": "none", "initial": ["Rope", "Poison", "Knife", "Pillow", "Hammer", "Pistol", "Insulin", "Brick", "Drowning", "Electric Wire", "Scarf", "Bare Hands", "Fire", "Bottle", "Axe", "Car"], "meaning": "undealt Means words", "observable": false},
      {"key": "tile_deck", "type": "list", "visible": "none", "initial": ["Time of Death", "Weather", "Victim's Build", "Trace at Scene", "Corpse Condition", "Duration of Crime"], "meaning": "undrawn scene tiles", "observable": false},
      {"key": "current_tile", "type": "text", "visible": "public", "initial": "", "meaning": "this round's scene tile", "observable": true},
      {"key": "marker", "type": "text", "visible": "public", "initial": "", "meaning": "option the Scientist marked this round", "observable": true},
      {"key": "key_evidence", "type": "text", "visible": "none", "initial": "", "meaning": "the Murderer's chosen Clue", "observable": false},
      {"key": "means_of_murder", "type": "text", "visible": "none", "initial": "", "meaning": "the Murderer's chosen Means", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number", "observable": true},
      {"key": "solved", "type": "bool", "visible": "public", "initial": false, "meaning": "a correct accusation has been made", "observable": true},
      {"key": "hunt_target", "type": "number", "visible": "public", "initial": 0, "meaning": "seat named by the Murderer in the Witness Hunt", "observable": true},
      {"key": "game_over", "type": "number", "visible": "public", "initial": 0, "meaning": "1 when the game has ended", "observable": false}
    ]
  },
  "setup": [
    "Seat 1 is publicly the Forensic Scientist.",
    "The engine secretly and randomly deals the other seats 1 Murderer, 1 Accomplice, 1 Witness and (player count minus 4) Investigators into role, and sets side.",
    "Intel is set: the Accomplice learns the Murderer's seat; the Witness learns the two seats of the Murderer and Accomplice without learning which is which; the Scientist learns every role.",
    "Each seat except seat 1 draws 2 Clue words from clue_deck into clues and 2 Means words from means_deck into means, at random and without repeats. These cards are public.",
    "Each seat except seat 1 gets badge 1.",
    "The Murderer is asked privately to choose one of their own clues as key_evidence and one of their own means as means_of_murder.",
    "solution_known of seat 1 and of the Accomplice is set to the key_evidence and the means_of_murder.",
    "Every player is sent their own state (sync)."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1; current_tile = 'Cause of Death' if round==1, 'Location' if round==2, otherwise a random tile removed from tile_deck; every acc_clue and acc_means is cleared; current_tile is announced with its 6 options"},
    {"action": "ask", "who": "seat 1", "answer": "one of the 6 options of current_tile", "effect": "marker = the chosen option; the marker is announced to all"},
    {"action": "poll", "who": "every player except seat 1", "answer": "short text", "effect": "broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"},
    {"action": "poll", "who": "every player with badge == 1", "answer": "PASS, or one Clue word currently in any player's clues", "effect": "acc_clue = the answer; hidden until resolution"},
    {"action": "poll", "who": "every player whose acc_clue is not PASS", "answer": "one Means word currently in any player's means", "effect": "acc_means = the answer; badge -= 1 for each such player; hidden until resolution"},
    {"action": "update", "who": "table", "answer": null, "effect": "each accusation is announced with its accuser and marked correct if acc_clue == key_evidence and acc_means == means_of_murder, wrong otherwise; solved = true if any accusation is correct"},
    {"action": "ask", "who": "the player whose role is Murderer, when solved == true", "answer": "a seat other than seat 1, the Accomplice and the Murderer", "effect": "hunt_target = the chosen seat"},
    {"action": "update", "who": "table", "answer": null, "effect": "when solved == true: if the role of hunt_target is Witness, won = 1 for side murderer, else won = 1 for side investigator; game_over = 1. Else when round == 5: won = 1 for side murderer; game_over = 1"},
    {"action": "check", "who": "table", "answer": null, "effect": "end the game if game_over == 1, otherwise continue to the next round"}
  ],
  "ending": {
    "condition": "game_over == 1",
    "rank_by": "you.won",
    "min_to_win": 1,
    "decided_by": "Team win: every player on the winning side has won = 1 and shares the win; the losing side has 0."
  },
  "rules": [
    {"id": "R1", "text": "Seat 1 is always the Forensic Scientist, and that role is public."},
    {"id": "R2", "text": "When the game starts with N players, then the other N-1 seats are dealt exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators at random."},
    {"id": "R3", "text": "When roles are dealt, then the Accomplice's intel names the Murderer's seat."},
    {"id": "R4", "text": "When roles are dealt, then the Witness's intel names the two seats of the Murderer and the Accomplice without saying which is which, and the Witness does not get the solution."},
    {"id": "R5", "text": "When roles are dealt, then the Scientist's intel lists every seat's role."},
    {"id": "R6", "text": "When cards are dealt, then every seat except seat 1 holds 2 Clue words and 2 Means words, all public, with no word appearing twice at the table."},
    {"id": "R7", "text": "When the Murderer chooses the solution, then key_evidence must be one of the Murderer's own 2 clues and means_of_murder must be one of their own 2 means."},
    {"id": "R8", "text": "When the solution is chosen, then the Scientist and the Accomplice are told it, and no one else is."},
    {"id": "R9", "text": "When the game starts, then every seat except seat 1 has badge 1 and seat 1 has badge 0."},
    {"id": "R10", "text": "When round is 1, then current_tile is Cause of Death; when round is 2, then it is Location."},
    {"id": "R11", "text": "When round is 3, 4 or 5, then current_tile is drawn at random from tile_deck and removed from it."},
    {"id": "R12", "text": "When the Scientist marks, then exactly one of current_tile's 6 options becomes marker and is announced to all."},
    {"id": "R13", "text": "The Scientist never writes a talk message or makes an accusation."},
    {"id": "R14", "text": "When talk happens, then every player except seat 1 writes one message at the same time, and all messages are shown to everyone afterwards."},
    {"id": "R15", "text": "When accusations are made, then only players with badge 1 are asked, all at the same time, to choose PASS or one Clue on the table and one Means on the table."},
    {"id": "R16", "text": "When a player accuses, then their badge drops from 1 to 0 and they are not asked to accuse again."},
    {"id": "R17", "text": "When an accusation's Clue equals key_evidence and its Means equals means_of_murder, then it is announced as correct and solved becomes true; otherwise it is announced as wrong."},
    {"id": "R18", "text": "When an accusation pairs a Clue and a Means from two different players' cards, then it is always wrong."},
    {"id": "R19", "text": "When solved is true, then the Murderer names one seat other than seat 1, the Accomplice and themself."},
    {"id": "R20", "text": "When the named seat is the Witness, then the Murderer and the Accomplice get won = 1; otherwise the Scientist, the Witness and all Investigators get won = 1."},
    {"id": "R21", "text": "When round 5 ends with solved still false, then the Murderer and the Accomplice get won = 1 and the game ends."},
    {"id": "R22", "text": "When no accusation is correct in rounds 1 to 4, then the next round begins."}
  ],
  "offers": [
    {"question": "Murderer's choice of Key Evidence (setup)", "who": "the Murderer", "options": "the 2 Clue words in the Murderer's own clues"},
    {"question": "Murderer's choice of Means of Murder (setup)", "who": "the Murderer", "options": "the 2 Means words in the Murderer's own means"},
    {"question": "Marker", "who": "seat 1", "options": "the 6 options of current_tile"},
    {"question": "Talk", "who": "every seat except seat 1", "options": "short free text"},
    {"question": "Accusation: Clue", "who": "every seat with badge 1 (never seat 1)", "options": "PASS, or any Clue word in any player's clues"},
    {"question": "Accusation: Means", "who": "every seat that chose a Clue", "options": "any Means word in any player's means"},
    {"question": "Witness Hunt", "who": "the Murderer, only when solved is true", "options": "every seat except seat 1, the Accomplice and the Murderer"}
  ],
  "choices": [
    {"what": "6 to 8 players, suggested 7", "why": "Kept the designer's 7. Six is the minimum because the four special roles plus 2 Investigators are needed for the Murderer side to hide. Above 8 the talk becomes too long and the Scientist's single marker per round is spread too thin."},
    {"what": "The accusation is split into two simultaneous polls (Clue or PASS, then Means)", "why": "Offering every Clue-Means pair would mean up to about 200 options. Answers stay hidden until resolution, so the choice is still effectively simultaneous."},
    {"what": "Talk is kept as a simultaneous poll broadcast to all", "why": "The source requires it. Players disagree because the Murderer side wants to mislead, so reading each other's statements against the marker is the core of the game."},
    {"what": "The win is recorded as won = 1 for each player on the winning side, with min_to_win 1", "why": "This expresses a team win as an arithmetic ranking."},
    {"what": "The Witness Hunt is a single conditional step inside the round, followed by game_over", "why": "A flat step list cannot branch into a separate block, but a step with a 'when' condition works."},
    {"what": "Strategy at the table", "why": "The Scientist picks markers that point towards one player's cards. Investigators cross-reference the markers with the face-up cards and spend their single badge carefully. The Murderer and Accomplice steer talk towards innocent pairs. The Witness must hint without revealing themself."}
  ],
  "simplifications": [
    {"what": "The Scientist's ban on sending any other message is enforced by never asking seat 1 to talk", "why": "The engine only lets players speak when asked."}
  ],
  "unsupported": []
}
```
````
