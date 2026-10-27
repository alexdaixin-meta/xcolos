# 03 spec

- time: 2026-10-27T22:10:47+00:00 (52.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 e3bc81f9e91ef0a7, reply sha256 e6db6ed4dba8e6c1

## Sent

````
Game: Secret Slice
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP
- There are 3 players, seated P1, P2, P3.
- The deck has 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy. It is shuffled once and split into 6 rows of 6.
- Each player is privately dealt one favourite topping, drawn without replacement from {Cheese, Mushroom, Pepperoni, Anchovy}. The three favourites are therefore all different, and one topping is nobody's favourite.
- Favourites stay secret until final scoring.

ROUNDS
The game has 6 rounds. The Slicer is P1 in round 1, then P2, P3, P1, P2, P3.

In each round:
1. Reveal. The next row of 6 slices is revealed, with positions numbered 1 to 6.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
3. Cut. The Slicer states two whole numbers c1 and c2 with 1 <= c1 < c2 <= 5.
   - Portion A is positions 1 to c1.
   - Portion B is positions c1+1 to c2.
   - Portion C is positions c2+1 to 6.
   - In the same answer, the Slicer declares 'eat' or 'collect'. This applies to the pepperoni in whichever portion the Slicer ends up with.
   - The three portions are announced.
4. First pick. The player after the Slicer (P1→P2→P3→P1) chooses one portion and declares 'eat' or 'collect'.
5. Second pick. The remaining non-Slicer player chooses one of the two remaining portions and declares 'eat' or 'collect'.
6. Slicer. The Slicer takes the last portion, with the 'eat' or 'collect' declared at the cut.

EAT OR COLLECT
When a player takes a portion:
- With 'eat', each Pepperoni slice in it is eaten for +1 point and does not count as collected.
- With 'collect', every slice in the portion is collected.
- Non-pepperoni slices are always collected.

FINAL SCORING (after round 6)
Scoring uses only collected slices, plus eaten pepperoni and anchovy penalties.
- Majority: the player with strictly the most collected slices of a type scores Cheese 7, Mushroom 7, Pepperoni 5, Anchovy 10. If there is a tie for most, nobody scores that type.
- Eaten pepperoni: +1 per eaten Pepperoni slice.
- Anchovy penalty: -1 per collected Anchovy slice.
- Favourite: +1 per collected slice of your own favourite type. Eaten slices do not count.

The totals are announced.

How the winner is decided: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Secret Slice",
  "summary": "Three players take turns cutting a row of six pizza slices into three portions. The others pick first and the cutter gets the last portion. Each player chooses whether to eat pepperoni for points or collect it toward majorities, while chasing a secret favourite topping.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "player_count": 3,
    "slices_per_type": 9,
    "deck_size": 36,
    "rows": 6,
    "row_size": 6,
    "rounds": 6,
    "cut_min": 1,
    "cut_max": 5,
    "majority_cheese": 7,
    "majority_mushroom": 7,
    "majority_pepperoni": 5,
    "majority_anchovy": 10,
    "eaten_pepperoni_point": 1,
    "anchovy_penalty": 1,
    "favourite_bonus": 1
  },
  "attributes": {
    "player": [
      {"key": "favourite", "type": "text", "visible": "ally", "initial": "", "meaning": "secret favourite topping: Cheese, Mushroom, Pepperoni or Anchovy; revealed at final scoring", "observable": true},
      {"key": "cheese", "type": "number", "visible": "public", "initial": 0, "meaning": "collected Cheese slices", "observable": true},
      {"key": "mushroom", "type": "number", "visible": "public", "initial": 0, "meaning": "collected Mushroom slices", "observable": true},
      {"key": "pepperoni", "type": "number", "visible": "public", "initial": 0, "meaning": "collected Pepperoni slices", "observable": true},
      {"key": "anchovy", "type": "number", "visible": "public", "initial": 0, "meaning": "collected Anchovy slices", "observable": true},
      {"key": "eaten", "type": "number", "visible": "public", "initial": 0, "meaning": "eaten Pepperoni slices", "observable": true},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "final total, computed after round 6", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "9 x Cheese, 9 x Mushroom, 9 x Pepperoni, 9 x Anchovy", "meaning": "the undealt slices; each row is drawn from it at random", "observable": false},
      {"key": "toppings", "type": "list", "visible": "none", "initial": ["Cheese", "Mushroom", "Pepperoni", "Anchovy"], "meaning": "favourites still undealt; one is left over and is nobody's favourite", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round, 1 to 6", "observable": true},
      {"key": "slicer", "type": "number", "visible": "public", "initial": 0, "meaning": "seat of this round's Slicer", "observable": false},
      {"key": "first_picker", "type": "number", "visible": "public", "initial": 0, "meaning": "seat after the Slicer", "observable": false},
      {"key": "second_picker", "type": "number", "visible": "public", "initial": 0, "meaning": "remaining non-Slicer seat", "observable": false},
      {"key": "row", "type": "list", "visible": "public", "initial": [], "meaning": "this round's 6 slices, positions 1 to 6 in order", "observable": false},
      {"key": "c1", "type": "number", "visible": "public", "initial": 0, "meaning": "first cut", "observable": false},
      {"key": "c2", "type": "number", "visible": "public", "initial": 0, "meaning": "second cut", "observable": false},
      {"key": "slicer_mode", "type": "text", "visible": "public", "initial": "", "meaning": "eat or collect, declared by the Slicer at the cut", "observable": false},
      {"key": "portion_a", "type": "list", "visible": "public", "initial": [], "meaning": "positions 1..c1", "observable": false},
      {"key": "portion_b", "type": "list", "visible": "public", "initial": [], "meaning": "positions c1+1..c2", "observable": false},
      {"key": "portion_c", "type": "list", "visible": "public", "initial": [], "meaning": "positions c2+1..6", "observable": false},
      {"key": "taken", "type": "list", "visible": "public", "initial": [], "meaning": "portions already picked this round (A, B, C)", "observable": false}
    ]
  },
  "setup": [
    "Seats are P1, P2, P3.",
    "The deck list is filled with 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy.",
    "Each player is dealt a favourite at random from the toppings list, which is removed from that list (without replacement), so the three favourites differ and one topping is nobody's favourite.",
    "Each player is synced their own favourite, kept secret (ally) until final scoring."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; slicer = ((round-1) mod 3) + 1; first_picker = (slicer mod 3) + 1; second_picker = (first_picker mod 3) + 1; taken = []"},
    {"action": "update", "who": "all players", "answer": null, "effect": "row = []; 6 times: draw one slice at random from deck, append it to row, remove it from deck. Announce the row with positions 1 to 6 and who is Slicer, first picker and second picker."},
    {"action": "poll", "who": "all players", "answer": "short text message", "effect": "Nothing changes; all messages are broadcast at once: {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}"},
    {"action": "ask", "who": "seat slicer", "answer": "one choice 'c1-c2 mode' with 1 <= c1 < c2 <= 5 and mode eat or collect (20 options)", "effect": "set c1, c2, slicer_mode; portion_a = row[1..c1]; portion_b = row[c1+1..c2]; portion_c = row[c2+1..6]; announce the three portions"},
    {"action": "ask", "who": "seat first_picker", "answer": "one of: A eat, A collect, B eat, B collect, C eat, C collect", "effect": "the picker adds the chosen portion's Cheese to cheese, Mushroom to mushroom and Anchovy to anchovy; its Pepperoni goes to eaten if eat, or to pepperoni if collect; append the letter to taken; announce"},
    {"action": "ask", "who": "seat second_picker", "answer": "one of the two portions not in taken, each with eat or collect (4 options)", "effect": "same accounting as the first pick for the second picker; append the letter to taken; announce"},
    {"action": "update", "who": "seat slicer", "answer": null, "effect": "the Slicer takes the portion not in taken, with slicer_mode: Cheese to cheese, Mushroom to mushroom, Anchovy to anchovy, Pepperoni to eaten if slicer_mode = eat, otherwise to pepperoni; announce"},
    {"action": "update", "who": "all players", "answer": null, "effect": "when round = 6: for each player, score = 7 if cheese is strictly greater than both other players' cheese + 7 if mushroom is strictly greater than both others' + 5 if pepperoni is strictly greater than both others' + 10 if anchovy is strictly greater than both others' + eaten - anchovy + the collected count of their own favourite (cheese, mushroom, pepperoni or anchovy). Reveal every favourite and announce all totals."},
    {"action": "check", "who": "all players", "answer": null, "effect": "end the game if round >= 6, otherwise continue"}
  ],
  "ending": {
    "condition": "round >= 6",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final total; the highest total wins, and players tied for the highest share the win (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup, the deck holds 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni, 9 Anchovy."},
    {"id": "R2", "text": "At setup, each of the 3 players gets a different favourite from {Cheese, Mushroom, Pepperoni, Anchovy}, visible only to its owner until final scoring."},
    {"id": "R3", "text": "In each round, 6 slices are drawn from the deck into the row, so after round r the deck holds 36 - 6r slices."},
    {"id": "R4", "text": "The Slicer is P1 in rounds 1 and 4, P2 in rounds 2 and 5, and P3 in rounds 3 and 6."},
    {"id": "R5", "text": "The first picker is the seat after the Slicer (P1 to P2, P2 to P3, P3 to P1), and the second picker is the remaining seat."},
    {"id": "R6", "text": "Each round, every player sends one text message in a simultaneous poll, and all messages are shown together; messages change no state."},
    {"id": "R7", "text": "The Slicer chooses c1 and c2 with 1 <= c1 < c2 <= 5, plus eat or collect, in one answer; for example 2-4 gives A = positions 1-2, B = 3-4, C = 5-6."},
    {"id": "R8", "text": "The first picker may choose any of A, B or C with eat or collect; the second picker may choose only one of the two portions left."},
    {"id": "R9", "text": "The Slicer receives the last remaining portion, using the mode declared at the cut."},
    {"id": "R10", "text": "When a portion is taken with eat, each Pepperoni in it adds 1 to eaten and nothing to pepperoni."},
    {"id": "R11", "text": "When a portion is taken with collect, each Pepperoni in it adds 1 to pepperoni."},
    {"id": "R12", "text": "Cheese, Mushroom and Anchovy slices in a taken portion are always added to cheese, mushroom and anchovy, whichever mode is declared."},
    {"id": "R13", "text": "At final scoring, a player with strictly the most collected Cheese scores 7, Mushroom 7, Pepperoni 5, Anchovy 10; if the most is tied, nobody scores that type."},
    {"id": "R14", "text": "At final scoring, each eaten Pepperoni is worth +1."},
    {"id": "R15", "text": "At final scoring, each collected Anchovy is worth -1."},
    {"id": "R16", "text": "At final scoring, each collected slice of your own favourite type is worth +1; eaten slices do not count."},
    {"id": "R17", "text": "The game ends after round 6; the highest score wins, and tied top scores share the win."}
  ],
  "offers": [
    {"question": "Talk", "who": "all players", "options": "a short free-text message"},
    {"question": "Cut", "who": "the Slicer", "options": "1-2 eat, 1-2 collect, 1-3 eat, 1-3 collect, 1-4 eat, 1-4 collect, 1-5 eat, 1-5 collect, 2-3 eat, 2-3 collect, 2-4 eat, 2-4 collect, 2-5 eat, 2-5 collect, 3-4 eat, 3-4 collect, 3-5 eat, 3-5 collect, 4-5 eat, 4-5 collect"},
    {"question": "First pick", "who": "the seat after the Slicer", "options": "A eat, A collect, B eat, B collect, C eat, C collect"},
    {"question": "Second pick", "who": "the remaining non-Slicer seat", "options": "the two portions not taken by the first picker, each with eat or collect (e.g. after A is taken: B eat, B collect, C eat, C collect)"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed the table at 3. The rotation of Slicer and pickers, the three portions and the three distinct favourites from four toppings all depend on exactly 3 seats."},
    {"what": "Strategy check", "why": "A thoughtful Slicer cuts so that every portion is equally unattractive to the others and reads their collections and talk to guess their favourites. Pickers weigh eating pepperoni (+1 now) against contesting the 5-point pepperoni majority, and avoid or deny anchovy around the 10-point majority."},
    {"what": "Keep the talk step as a simultaneous poll broadcast to all", "why": "The source says messages are written at the same time without seeing the others. Players have opposing interests over portions and majorities, so the talk gives them bluffing and bargaining material."},
    {"what": "Cut and mode given as one combined choice of 20 options", "why": "The source says the Slicer declares eat or collect in the same answer as the cut. One choice list enforces 1 <= c1 < c2 <= 5 exactly."},
    {"what": "Picks offered as portion plus mode in one choice", "why": "The source has each picker choose a portion and declare eat or collect together."}
  ],
  "simplifications": [
    {"what": "Rows are drawn at random from the deck each round instead of shuffling once and splitting into 6 rows at setup", "why": "Drawing 6 random slices per round without replacement gives the same distribution and keeps future rows hidden, using the engine's draw operation."},
    {"what": "A tie for the highest total is a shared win rather than a draw", "why": "The engine has no separate draw; players level at the top share the win, which matches the outcome that nobody wins alone."},
    {"what": "Strict majority is computed by comparing each player's count with both other players' counts", "why": "There is no direct player-attribute operand; the comparison is written out across the 3 seats in arithmetic."}
  ],
  "unsupported": []
}
```
````
