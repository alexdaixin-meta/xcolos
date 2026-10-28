# 24 spec

- time: 2026-10-28T02:12:42+00:00 (58.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 020a8ec61e198496, reply sha256 c3a91c9f7f909ea9

## Sent

````
Game: Deception: Four Tiles
Players in the source: 6 to 8
Suggested table size, chosen by the designer of these rules (keep it): 7

Rules, as filed in the inventory:
COMPONENTS.
- Clue words (16): Glove, Key, Diary, Ring, Cigarette, Phone, Wallet, Mask, Train Ticket, Lipstick, Receipt, Hair, Button, Watch, Letter, Coin.
- Means words (16): Rope, Poison, Knife, Pillow, Insulin, Pistol, Electric Wire, Scarf, Bottle, Axe, Hammer, Candlestick, Brick, Razor, Bag, Ice.
- Scene tiles (8), each with a name and 6 items:
  - Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident
  - Location: Living Room, Bedroom, Bathroom, Kitchen, Street, Office
  - Time of Death: Dawn, Morning, Noon, Afternoon, Evening, Night
  - Weather: Sunny, Stormy, Dry, Humid, Cold, Hot
  - Victim's Build: Large, Thin, Tall, Short, Disfigured, Fit
  - Trace at Scene: Fingerprint, Footprint, Bruise, Blood Stain, Body Fluid, Scar
  - Corpse Condition: Still Warm, Stiff, Decayed, Incomplete, Intact, Twisted
  - Duration of Crime: Instant, Brief, Gradual, Prolonged, Days, Unclear

GAME STATE, set once before setup and never reset by setup:
- solved = false
- hunt_target = 0
- key_evidence and means_of_murder are empty unless given
- Every player starts with badge 0, won 0, acc_clue empty and acc_means empty.

SETUP.
1. Seat 1 is always the Forensic Scientist. This is public. The Scientist gets no cards and badge 0.
2. Seats 2..N receive exactly 1 Murderer, 1 Accomplice, 1 Witness and N-4 Investigators.
   - A role already given to a seat is kept.
   - Remaining roles are dealt at random to seats without a role.
   - Sides: Murderer and Accomplice are on the Murderer side. Scientist, Witness and Investigators are on the Investigator side.
3. Each of seats 2..N holds exactly 2 Clue cards and 2 Means cards, face up for everyone to see.
   - Cards already given are kept and removed from the decks first.
   - Missing cards are dealt at random from the remaining decks.
   - Undealt words stay in the clue deck and means deck. They are not 'on the table'.
   - Seats 2..N get badge 1.
4. Unless already given, the Murderer secretly chooses one of their own 2 Clues as key_evidence, then one of their own 2 Means as means_of_murder.
5. Private intel, written from the final roles:
   - The Scientist learns every role, key_evidence and means_of_murder.
   - The Accomplice learns the Murderer's seat.
   - The Witness learns the two Murderer-side seats, but not which is which.
   - The Murderer learns the Accomplice's seat.
   - Investigators learn nothing.

EACH ROUND (rounds 1 to 4):
1. Tile. Round 1 reveals Cause of Death. Rounds 2-4 each reveal one tile drawn at random from the tiles not yet revealed. This is the only random draw in a round.
2. Marker. The Scientist privately chooses one of the 6 items on the new tile, and the marked item is announced to all. The Scientist never speaks.
3. Talk. Every seat 2..N writes one short message at the same time, without seeing the others. All messages are then shown to everyone.
4. Accusation, Poll A. All seats with badge 1 are asked at the same time to choose PASS or one Clue word. The only Clue words offered are those currently in the clues lists of seats 2..N. The answer is stored in acc_clue (PASS leaves it empty).
5. Accusation, Poll B. All seats that named a Clue in Poll A this round are asked at the same time to choose one Means word. The only Means words offered are those currently in the means lists of seats 2..N. The answer is stored in acc_means.
6. Every seat with a non-empty acc_clue has badge set to 0. It will never be asked to accuse again.
7. Resolution. Each accusation (acc_clue, acc_means) is announced with its seat.
   - If acc_clue equals key_evidence and acc_means equals means_of_murder, it is announced as correct and solved becomes true.
   - Otherwise it is announced as wrong.
   - solved, once true, stays true.
8. acc_clue and acc_means are cleared for all players.
9. Witness Hunt. This happens only if solved became true this round. The Murderer chooses one seat from seats 2..N other than their own, stored as hunt_target.
10. End check. The game ends if solved is true or round 4 has finished. Otherwise the next round begins.

SCORING at the end:
- If solved is true and hunt_target is the Witness's seat, every Murderer-side player gets won = 1.
- If solved is true and hunt_target is not the Witness's seat, every Investigator-side player (including the Scientist) gets won = 1.
- If solved is false after round 4, every Murderer-side player gets won = 1.

How the winner is decided: Team win, decided by arithmetic on the stored values.
- Investigator side wins if some accusation exactly matched key_evidence and means_of_murder and the Murderer's hunt_target is not the Witness's seat.
- Murderer side wins if the case is never solved in 4 rounds, or if it is solved and hunt_target equals the Witness's seat.
- The winners are the players with won = 1. There are no draws.
````

## Reply

````
```json
{
  "name": "Deception: Four Tiles",
  "summary": "A hidden-role deduction game: a silent Forensic Scientist marks scene items to steer the Investigators toward the Murderer's secret clue and means within 4 rounds, and if the case is solved the Murderer gets one guess at the Witness to steal the win.",
  "players": {"min": 6, "max": 8, "suggested": 7},
  "parameters": {
    "clue_words": 16,
    "means_words": 16,
    "scene_tiles": 8,
    "items_per_tile": 6,
    "rounds": 4,
    "clues_per_seat": 2,
    "means_per_seat": 2,
    "scientist_seat": 1,
    "murderers": 1,
    "accomplices": 1,
    "witnesses": 1,
    "investigators_formula_offset": 4,
    "starting_badge_cardholder": 1,
    "starting_badge_scientist": 0,
    "accusations_per_seat": 1,
    "win_value": 1
  },
  "attributes": {
    "player": [
      {"key": "role", "type": "text", "visible": "ally", "initial": "", "meaning": "scientist, murderer, accomplice, witness or investigator. The Scientist's role is also announced publicly through the table attribute scientist_seat.", "observable": false},
      {"key": "side", "type": "text", "visible": "ally", "initial": "", "meaning": "murderer (Murderer and Accomplice) or investigator (Scientist, Witness and Investigators)", "observable": false},
      {"key": "clues", "type": "list", "visible": "public", "initial": [], "meaning": "the seat's 2 face-up Clue cards (empty for the Scientist)", "observable": true},
      {"key": "means", "type": "list", "visible": "public", "initial": [], "meaning": "the seat's 2 face-up Means cards (empty for the Scientist)", "observable": true},
      {"key": "badge", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if the seat may still accuse, 0 if not", "observable": true},
      {"key": "acc_clue", "type": "text", "visible": "public", "initial": "", "meaning": "the Clue named in this round's accusation (empty means PASS)", "observable": false},
      {"key": "acc_means", "type": "text", "visible": "public", "initial": "", "meaning": "the Means named in this round's accusation", "observable": false},
      {"key": "intel", "type": "text", "visible": "ally", "initial": "", "meaning": "the private information given at setup", "observable": false},
      {"key": "won", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if this player is on the winning side", "observable": true}
    ],
    "game": [
      {"key": "scientist_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "the public seat of the Forensic Scientist", "observable": true},
      {"key": "solved", "type": "bool", "visible": "public", "initial": false, "meaning": "true once an accusation exactly matched key_evidence and means_of_murder; never reset", "observable": true},
      {"key": "solved_this_round", "type": "bool", "visible": "none", "initial": false, "meaning": "true if solved became true in the current round", "observable": false},
      {"key": "hunt_target", "type": "number", "visible": "public", "initial": 0, "meaning": "the seat the Murderer named in the Witness Hunt (0 means no hunt)", "observable": true},
      {"key": "key_evidence", "type": "text", "visible": "none", "initial": "", "meaning": "the Murderer's secret Clue", "observable": false},
      {"key": "means_of_murder", "type": "text", "visible": "none", "initial": "", "meaning": "the Murderer's secret Means", "observable": false},
      {"key": "murderer_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "the seat of the Murderer", "observable": false},
      {"key": "accomplice_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "the seat of the Accomplice", "observable": false},
      {"key": "witness_seat", "type": "number", "visible": "none", "initial": 0, "meaning": "the seat of the Witness", "observable": false},
      {"key": "role_deck", "type": "list", "visible": "none", "initial": [], "meaning": "the roles still to be dealt to seats 2..N", "observable": false},
      {"key": "clue_deck", "type": "list", "visible": "none", "initial": ["Glove", "Key", "Diary", "Ring", "Cigarette", "Phone", "Wallet", "Mask", "Train Ticket", "Lipstick", "Receipt", "Hair", "Button", "Watch", "Letter", "Coin"], "meaning": "undealt Clue words", "observable": false},
      {"key": "means_deck", "type": "list", "visible": "none", "initial": ["Rope", "Poison", "Knife", "Pillow", "Insulin", "Pistol", "Electric Wire", "Scarf", "Bottle", "Axe", "Hammer", "Candlestick", "Brick", "Razor", "Bag", "Ice"], "meaning": "undealt Means words", "observable": false},
      {"key": "tile_deck", "type": "list", "visible": "none", "initial": ["Location", "Time of Death", "Weather", "Victim's Build", "Trace at Scene", "Corpse Condition", "Duration of Crime"], "meaning": "scene tiles not yet revealed (Cause of Death is revealed in round 1)", "observable": false},
      {"key": "current_tile", "type": "text", "visible": "public", "initial": "", "meaning": "the tile revealed this round", "observable": true},
      {"key": "revealed_tiles", "type": "list", "visible": "public", "initial": [], "meaning": "the tiles revealed so far", "observable": true},
      {"key": "marked_items", "type": "list", "visible": "public", "initial": [], "meaning": "the items marked by the Scientist, one per revealed tile", "observable": true},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "the current round number (1 to 4)", "observable": true}
    ]
  },
  "setup": [
    "Seat 1 is given role scientist and side investigator, and badge 0, no Clue cards and no Means cards. It is announced to all that seat 1 is the Forensic Scientist.",
    "role_deck is set to 1 murderer, 1 accomplice, 1 witness and N-4 investigator. Any role already given to a seat is kept and removed from role_deck. Each of seats 2..N without a role draws one role at random from role_deck.",
    "Each seat's side is set: murderer for the Murderer and the Accomplice, investigator for everyone else. murderer_seat, accomplice_seat and witness_seat are recorded.",
    "Cards already given to seats are removed from clue_deck and means_deck. Each of seats 2..N then draws at random from clue_deck until it holds 2 Clues, and from means_deck until it holds 2 Means, all face up (public). Undealt words stay in the decks and are not on the table.",
    "Seats 2..N get badge 1.",
    "Unless already given, the Murderer is asked privately to choose one of their own 2 clues, which is stored as key_evidence, then one of their own 2 means, which is stored as means_of_murder.",
    "Private intel is written to each seat's intel. The Scientist learns every seat's role, key_evidence and means_of_murder. The Accomplice learns murderer_seat. The Witness learns murderer_seat and accomplice_seat as an unordered pair. The Murderer learns accomplice_seat. Investigators learn nothing.",
    "Each player is sent their own state (sync)."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round += 1; solved_this_round = false. If round == 1, current_tile = 'Cause of Death'. Otherwise one tile is drawn at random from tile_deck, removed from it, and stored as current_tile. current_tile is appended to revealed_tiles and announced with its 6 items."},
    {"action": "ask", "who": "seat 1 (Scientist)", "answer": "one of the 6 items on current_tile", "effect": "the chosen item is appended to marked_items and announced to all as the marker on current_tile"},
    {"action": "poll", "who": "seats 2..N", "answer": "short text", "effect": "all messages are revealed together, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}; no state change"},
    {"action": "poll", "who": "all seats with badge == 1", "answer": "PASS or one Clue word currently in the clues of seats 2..N", "effect": "a Clue answer is stored in acc_clue; PASS leaves acc_clue empty"},
    {"action": "poll", "who": "all seats whose acc_clue is non-empty", "answer": "one Means word currently in the means of seats 2..N", "effect": "stored in acc_means"},
    {"action": "update", "who": "all players", "answer": null, "effect": "for each seat with acc_clue != '': badge = 0"},
    {"action": "update", "who": "all players", "answer": null, "effect": "each accusation (acc_clue, acc_means) with its seat is announced. If acc_clue == key_evidence and acc_means == means_of_murder, it is announced correct, and if solved was false, then solved = true and solved_this_round = true. Otherwise it is announced wrong. solved never returns to false."},
    {"action": "update", "who": "all players", "answer": null, "effect": "acc_clue = '' and acc_means = '' for every player"},
    {"action": "ask", "who": "the Murderer (seat murderer_seat), only when solved_this_round == true", "answer": "one seat from 2..N other than murderer_seat", "effect": "hunt_target = the chosen seat; it is announced"},
    {"action": "update", "who": "all players, only when solved == true or round >= 4", "answer": null, "effect": "if solved == true and hunt_target == witness_seat: won = 1 for every player with side == murderer. If solved == true and hunt_target != witness_seat: won = 1 for every player with side == investigator. If solved == false: won = 1 for every player with side == murderer. All roles are revealed."},
    {"action": "check", "who": "table", "answer": null, "effect": "the game ends if solved == true or round >= 4; otherwise the next round begins"}
  ],
  "ending": {
    "condition": "solved == true or round >= 4",
    "rank_by": "you.won",
    "min_to_win": 1,
    "decided_by": "A team win. Every player whose side won has won = 1 and shares the win. The Investigator side wins if the case is solved and hunt_target is not the Witness's seat. The Murderer side wins if the case is unsolved after 4 rounds, or if it is solved and hunt_target is the Witness's seat."
  },
  "rules": [
    {"id": "R1", "text": "When the game sets up, then seat 1 is the Forensic Scientist, publicly, with badge 0 and empty clues and means."},
    {"id": "R2", "text": "When the game sets up with N players, then seats 2..N hold exactly 1 murderer, 1 accomplice, 1 witness and N-4 investigators, and any pre-given role is kept."},
    {"id": "R3", "text": "When roles are dealt, then the Murderer and the Accomplice have side murderer, and the Scientist, the Witness and the Investigators have side investigator."},
    {"id": "R4", "text": "When the game sets up, then each of seats 2..N holds exactly 2 public clues and 2 public means, and pre-given cards are kept and removed from the decks first."},
    {"id": "R5", "text": "When cards are dealt, then no word appears twice across hands and decks, and undealt words remain in clue_deck or means_deck."},
    {"id": "R6", "text": "When setup finishes, then seats 2..N have badge 1."},
    {"id": "R7", "text": "When the Murderer chooses, then key_evidence is one of the Murderer's own 2 clues and means_of_murder is one of the Murderer's own 2 means."},
    {"id": "R8", "text": "When intel is written, then the Scientist learns all roles, key_evidence and means_of_murder, the Accomplice learns murderer_seat, the Witness learns the two murderer-side seats unordered, the Murderer learns accomplice_seat, and Investigators learn nothing."},
    {"id": "R9", "text": "When round 1 starts, then current_tile is Cause of Death."},
    {"id": "R10", "text": "When rounds 2, 3 or 4 start, then one tile not yet revealed is drawn at random from tile_deck and removed from it."},
    {"id": "R11", "text": "When a tile is revealed, then the Scientist chooses exactly one of its 6 items, and that item is announced and appended to marked_items."},
    {"id": "R12", "text": "When the Talk step runs, then only seats 2..N write a message, simultaneously, and all messages are shown to everyone afterward; the Scientist never speaks."},
    {"id": "R13", "text": "When Poll A runs, then only seats with badge 1 are asked, and each may choose PASS or a Clue currently in the clues of seats 2..N."},
    {"id": "R14", "text": "When a seat names a Clue in Poll A, then in Poll B it must choose a Means currently in the means of seats 2..N; a seat that passed is not asked in Poll B."},
    {"id": "R15", "text": "When a seat has made an accusation (acc_clue non-empty), then its badge becomes 0 and it is never asked to accuse again."},
    {"id": "R16", "text": "When an accusation has acc_clue == key_evidence and acc_means == means_of_murder, then it is announced correct and solved becomes true."},
    {"id": "R17", "text": "When an accusation matches only one of the two words or neither, then it is announced wrong and solved is unchanged."},
    {"id": "R18", "text": "When solved is true, then it stays true for the rest of the game."},
    {"id": "R19", "text": "When resolution finishes, then acc_clue and acc_means are cleared for all players."},
    {"id": "R20", "text": "When solved became true this round, then the Murderer chooses hunt_target from seats 2..N other than their own seat; otherwise no hunt happens and hunt_target stays 0."},
    {"id": "R21", "text": "When solved is true or round 4 has finished, then the game ends."},
    {"id": "R22", "text": "When the game ends with solved true and hunt_target == witness_seat, then the Murderer and the Accomplice get won = 1 and all others keep won = 0."},
    {"id": "R23", "text": "When the game ends with solved true and hunt_target != witness_seat, then the Scientist, the Witness and every Investigator get won = 1."},
    {"id": "R24", "text": "When round 4 ends with solved false, then the Murderer and the Accomplice get won = 1."}
  ],
  "offers": [
    {"question": "Setup: the Murderer's choice of key_evidence", "who": "the Murderer", "options": "the 2 Clue words in the Murderer's own clues"},
    {"question": "Setup: the Murderer's choice of means_of_murder", "who": "the Murderer", "options": "the 2 Means words in the Murderer's own means"},
    {"question": "Marker", "who": "seat 1 (Scientist)", "options": "the 6 items of current_tile, e.g. for Cause of Death: Suffocation, Severe Injury, Loss of Blood, Illness, Poisoning, Accident"},
    {"question": "Talk", "who": "seats 2..N", "options": "one short free-text message; the Scientist is not asked"},
    {"question": "Accusation Poll A", "who": "every seat with badge 1 (never seat 1, never a seat that already accused)", "options": "PASS, or any Clue word currently in the clues of seats 2..N, including the asker's own"},
    {"question": "Accusation Poll B", "who": "every seat that named a Clue in Poll A this round", "options": "any Means word currently in the means of seats 2..N, including the asker's own; PASS is not offered"},
    {"question": "Witness Hunt", "who": "the Murderer, only in the round solved became true", "options": "every seat from 2..N except the Murderer's own seat"}
  ],
  "choices": [
    {"what": "6 to 8 players, suggested 7", "why": "The designer chose 7, and it is kept. The minimum is 6 because seats 2..N must hold the Murderer, the Accomplice, the Witness and at least 2 Investigators, so that the Murderer side can hide and the Witness Hunt is a real guess. The maximum is 8 because more card-holders dilute each accusation and lengthen the talk beyond what can be followed."},
    {"what": "Talk is a simultaneous poll of one short message from seats 2..N, broadcast to all", "why": "The source says messages are written at the same time without seeing the others. Talk earns its place because the two sides disagree: the Murderer side misleads, Investigators argue readings of the markers, and the Witness must hint without exposing themselves."},
    {"what": "Role, side and intel are owner-only (ally), and seat knowledge is delivered through the intel text", "why": "Each player sees only their own role. Cross-seat knowledge (Accomplice to Murderer, Witness to the pair, Scientist to all) is given exactly as the rules list it."},
    {"what": "Scoring is applied as a single conditional update just before the end check, and the winner is ranked by you.won with min_to_win 1", "why": "This makes the team win pure arithmetic on stored values, as the source states."},
    {"what": "All roles are revealed when the game ends", "why": "Revealing roles lets observers verify the result. It does not change play."}
  ],
  "simplifications": [
    {"what": "The Scientist's marker is a single choice from the 6 tile items, announced as text", "why": "There are no physical tiles or bullet markers; the source already defines the marker as a choice of one item."}
  ],
  "unsupported": []
}
```
````
