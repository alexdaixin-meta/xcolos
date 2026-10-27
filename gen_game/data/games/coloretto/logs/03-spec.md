# 03 spec

- time: 2026-10-27T16:40:24+00:00 (51.0s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 2aaa0d155c2b2f8b, reply sha256 223a79834a46209e

## Sent

````
Game: Coloretto: Secret Favourites
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
COMPONENTS. 38 cards: 7 each of Red, Blue, Green, Yellow and Purple, plus 3 '+2' cards. There are three rows, numbered 1, 2 and 3, and each holds at most 3 cards.

SETUP. Shuffle the 38 cards into a face-down deck. The top card is always shown face up to everyone. Deal each player a different secret Favourite colour, chosen at random from the 5 colours. Only that player knows it. All rows start empty and open. No player has taken. Player 1 is active.

CYCLE. A cycle runs until all three players have taken a row.
- A player who has taken a row in the current cycle sits out until the cycle ends.
- A row that has been taken is closed for the rest of the cycle.
- When the third player takes, the cycle ends immediately. All three rows reopen empty, all players become eligible again, and the player who took last is active.

TURN (one per round, 36 rounds). The game shows everyone: the face-up top card, the contents of every row and whether it is open, every player's collected cards, who has taken this cycle, and the turn number. The active player chooses one action:
(a) PLACE on row k. This is legal only if row k is open and has fewer than 3 cards. Move the top card onto row k; the next card becomes the face-up top card.
(b) TAKE row k. This is legal only if row k is open and has at least 1 card. Add all its cards to your collection, close the row, and mark yourself as taken.
If every open row is full, the player must TAKE. An illegal or missing choice becomes TAKE of the lowest-numbered open row that has a card. If there is none, it becomes PLACE on the lowest-numbered open row that has room.

NEXT ACTIVE PLAYER. After a PLACE, or after a TAKE that does not end the cycle, the next active player is the next player in seat order (1, 2, 3, 1, ...) who has not taken this cycle. This may be the same player again if they are the only one left; that player may keep placing on the remaining row until it is full, then must take it.

END. The game ends after round 36. Cards still lying in rows are discarded.

SCORING. For each colour, count the cards of that colour you hold and convert the count to points: 0 = 0, 1 = 1, 2 = 3, 3 = 6, 4 = 10, 5 = 15, 6 = 21, 7 = 28.
- Your three colours with the highest counts score positive. If counts tie for third place, either tied colour can be counted; the points are the same.
- Your other two colours score negative.
- Add 2 for each '+2' card you hold.
- Add 6 if your Favourite colour's count is at least your third-highest colour count, that is, if it can be one of your scoring colours.
All favourites are revealed at the end.

How the winner is decided: The player with the highest final score wins. If two or three players tie for the highest score, those players draw.
````

## Reply

````
```json
{
  "name": "Coloretto: Secret Favourites",
  "summary": "Three players take turns either adding the face-up card to one of three rows or taking a row. They collect colours, score their best three and lose points for the rest, and earn a bonus for a secret Favourite colour.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "colours": 5,
    "cards_per_colour": 7,
    "plus_two_cards": 3,
    "deck_size": 38,
    "rows": 3,
    "row_capacity": 3,
    "rounds": 36,
    "positive_colours": 3,
    "negative_colours": 2,
    "plus_two_value": 2,
    "favourite_bonus": 6,
    "points_for_count_0": 0,
    "points_for_count_1": 1,
    "points_for_count_2": 3,
    "points_for_count_3": 6,
    "points_for_count_4": 10,
    "points_for_count_5": 15,
    "points_for_count_6": 21,
    "points_for_count_7": 28
  },
  "attributes": {
    "player": [
      {"key": "red", "type": "number", "visible": "public", "initial": 0, "meaning": "Red cards collected", "observable": false},
      {"key": "blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Blue cards collected", "observable": false},
      {"key": "green", "type": "number", "visible": "public", "initial": 0, "meaning": "Green cards collected", "observable": false},
      {"key": "yellow", "type": "number", "visible": "public", "initial": 0, "meaning": "Yellow cards collected", "observable": false},
      {"key": "purple", "type": "number", "visible": "public", "initial": 0, "meaning": "Purple cards collected", "observable": false},
      {"key": "plus_two", "type": "number", "visible": "public", "initial": 0, "meaning": "'+2' cards collected", "observable": false},
      {"key": "favourite", "type": "text", "visible": "ally", "initial": "", "meaning": "Secret Favourite colour, known only to its owner during play", "observable": false},
      {"key": "favourite_revealed", "type": "text", "visible": "public", "initial": "", "meaning": "Favourite colour, copied here when all favourites are revealed at the end", "observable": true},
      {"key": "taken", "type": "bool", "visible": "public", "initial": false, "meaning": "Has taken a row in the current cycle", "observable": false},
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Final score, computed after round 36", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "7 each of red, blue, green, yellow, purple plus 3 plus_two (38 cards)", "meaning": "Face-down draw deck", "observable": false},
      {"key": "favourite_pool", "type": "list", "visible": "none", "initial": ["red", "blue", "green", "yellow", "purple"], "meaning": "Colours not yet dealt as favourites", "observable": false},
      {"key": "top_card", "type": "text", "visible": "public", "initial": "", "meaning": "Face-up top card of the deck", "observable": false},
      {"key": "row_1", "type": "list", "visible": "public", "initial": [], "meaning": "Cards in row 1", "observable": false},
      {"key": "row_2", "type": "list", "visible": "public", "initial": [], "meaning": "Cards in row 2", "observable": false},
      {"key": "row_3", "type": "list", "visible": "public", "initial": [], "meaning": "Cards in row 3", "observable": false},
      {"key": "row_1_open", "type": "bool", "visible": "public", "initial": true, "meaning": "Row 1 not yet taken this cycle", "observable": false},
      {"key": "row_2_open", "type": "bool", "visible": "public", "initial": true, "meaning": "Row 2 not yet taken this cycle", "observable": false},
      {"key": "row_3_open", "type": "bool", "visible": "public", "initial": true, "meaning": "Row 3 not yet taken this cycle", "observable": false},
      {"key": "takers", "type": "number", "visible": "public", "initial": 0, "meaning": "Players who have taken this cycle", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the active player", "observable": false},
      {"key": "turn", "type": "number", "visible": "public", "initial": 1, "meaning": "Current turn number", "observable": true}
    ]
  },
  "setup": [
    "Fill the deck with the 38 cards: 7 each of red, blue, green, yellow and purple, plus 3 plus_two.",
    "Draw one card at random from deck into top_card, where it is face up for everyone.",
    "For each player, draw one colour at random from favourite_pool into that player's favourite and remove it from the pool, so every favourite is different and private.",
    "All rows are empty and open, no player has taken, takers = 0, active_seat = 1 and turn = 1.",
    "Send each player their own state."
  ],
  "round": [
    {"action": "sync", "who": "all players", "answer": null, "effect": "Everyone sees top_card, row_1..row_3 with their open flags, every player's colour counts and plus_two, every taken flag and turn. Each player also sees their own favourite."},
    {"action": "ask", "who": "the player at seat game.active_seat", "answer": "one of: place_1, place_2, place_3, take_1, take_2, take_3, limited to the legal options (see offers)", "effect": "Records the chosen action. An illegal or missing choice becomes take of the lowest-numbered open row with at least 1 card; if there is none, it becomes place on the lowest-numbered open row with fewer than 3 cards."},
    {"action": "update", "who": "the active player", "answer": null, "effect": "When the action is place_k: append top_card to row_k, then draw a random card from deck into top_card and remove it from deck."},
    {"action": "update", "who": "the active player", "answer": null, "effect": "When the action is take_k: for each card in row_k, add 1 to the active player's matching colour count, or to plus_two for a '+2' card. Then set row_k = [], row_k_open = false, active.taken = true and takers += 1."},
    {"action": "update", "who": "table", "answer": null, "effect": "When takers < 3: set active_seat to the first seat in order active_seat+1, active_seat+2, active_seat (wrapping 3 to 1) whose taken is false. This may be the same seat again."},
    {"action": "update", "who": "table", "answer": null, "effect": "When takers == 3 (the cycle has ended): set row_1, row_2 and row_3 to [], set every row_k_open = true, set every player's taken = false and takers = 0. active_seat stays the player who took last."},
    {"action": "update", "who": "table", "answer": null, "effect": "turn += 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When turn > 36: rows are discarded. For each player, sort the counts of red, blue, green, yellow and purple from highest to lowest as s1..s5, with T(c) = c*(c+1)/2. Set score = T(s1)+T(s2)+T(s3) - T(s4) - T(s5) + 2*plus_two + (6 if the favourite colour's count >= s3, else 0). Copy favourite into favourite_revealed."},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game when turn > 36; otherwise run the next round."}
  ],
  "ending": {
    "condition": "game.turn > 36",
    "rank_by": "you.score",
    "decided_by": "Each player's final score is their best three colours positive, their other two colours negative, plus 2 per '+2' card, plus 6 if their Favourite is among the colours that can score. The highest score wins, and players tied for the highest score draw (share the win)."
  },
  "rules": [
    {"id": "R1", "text": "At setup the deck holds 38 cards (7 each of 5 colours plus 3 '+2'), and one random card is face up as top_card."},
    {"id": "R2", "text": "At setup each player receives a different random Favourite colour, visible only to that player."},
    {"id": "R3", "text": "When a player chooses place_k, then the action is legal only if row_k is open and holds fewer than 3 cards; top_card is appended to row_k and a new top_card is drawn from deck."},
    {"id": "R4", "text": "When a player chooses take_k, then the action is legal only if row_k is open and holds at least 1 card; every card in row_k is added to that player's counts, row_k becomes empty and closed, and the player is marked taken."},
    {"id": "R5", "text": "When every open row holds 3 cards, then the active player is offered only take options."},
    {"id": "R6", "text": "When a choice is illegal or missing, then it becomes take of the lowest-numbered open row with a card; if there is none, it becomes place on the lowest-numbered open row with room."},
    {"id": "R7", "text": "When a player has taken a row this cycle, then that player is never active again until the cycle ends."},
    {"id": "R8", "text": "When a place or a non-final take happens, then the next active player is the next seat in order 1,2,3,1 whose taken is false, which may be the same player."},
    {"id": "R9", "text": "When the third player takes in a cycle, then all three rows reopen empty, all taken flags reset to false, and the player who took last stays active."},
    {"id": "R10", "text": "When a '+2' card is taken, then the taker's plus_two rises by 1."},
    {"id": "R11", "text": "When round 36 has been played, then the game ends and cards left in rows are discarded."},
    {"id": "R12", "text": "When scoring, then a colour count c is worth c*(c+1)/2 points (0,1,3,6,10,15,21,28 for 0 to 7)."},
    {"id": "R13", "text": "When scoring, then the three highest colour counts score positive and the other two score negative."},
    {"id": "R14", "text": "When scoring, then each '+2' card adds 2 points."},
    {"id": "R15", "text": "When the player's Favourite colour count is at least their third-highest colour count, then they gain 6 points."},
    {"id": "R16", "text": "When the game ends, then every player's Favourite is revealed in favourite_revealed."},
    {"id": "R17", "text": "When the game ends, then the highest score wins, and players tied for the highest score draw."}
  ],
  "offers": [
    {"question": "Active player's action", "who": "seat game.active_seat", "options": "place_k for each row k that is open and holds fewer than 3 cards, and take_k for each row k that is open and holds at least 1 card. If every open row is full, only the take_k options. A seat that has taken this cycle is never asked."}
  ],
  "choices": [
    {"what": "Exactly 3 players", "why": "The designer fixed the size at 3, and the rules are built around three rows and three takers per cycle. A fourth player has no row to take, and with two the cycle logic breaks."},
    {"what": "No talk step", "why": "The source rules include no discussion, and adding one would add a mechanic. The strategy lies in reading the other players' collections, guessing their Favourites from what they take, and deciding when to take a small row rather than wait."},
    {"what": "Points written as c*(c+1)/2", "why": "This matches the source table 0,1,3,6,10,15,21,28 exactly and is arithmetic."},
    {"what": "Favourite pool removes dealt colours", "why": "This makes every Favourite different, as the source requires."}
  ],
  "simplifications": [
    {"what": "One action per round; the active seat is tracked in active_seat and the asked seat is taken from it", "why": "The engine runs flat rounds, so the 'who' of the ask step comes from a table attribute."},
    {"what": "Top-3 versus bottom-2 scoring is computed by sorting the five colour counts in a calc step", "why": "There is no lookup operation; sorting counts gives the same result as sorting points because the points table is increasing."},
    {"what": "Favourites are revealed by copying them to a public attribute at the end", "why": "This is the engine's way to reveal hidden player state."}
  ],
  "unsupported": []
}
```
````
