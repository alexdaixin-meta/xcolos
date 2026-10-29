# 05 spec

- time: 2026-10-27T17:30:12+00:00 (74.6s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 51850d2fe34ba6a0, reply sha256 147eddb6097878c5

## Sent

````
Game: Blind Scuttle
Players in the source: 2 to 2
Suggested table size, chosen by the designer of these rules (keep it): 2

Rules, as filed in the inventory:
DECK: 48 cards.
- 40 point cards: ranks 1 to 10, four copies of each, no suits.
- 4 Jacks and 4 Kings.
Shuffle the deck.

BANDS: Every point card has a band. Low is ranks 1-4, Mid is ranks 5-7, High is ranks 8-10.

SETUP:
- Randomly pick the First player.
- Deal 6 cards to each player. Hands are private.
- The other 36 cards are the face-down draw pile.
- The scrap pile is face up and fully public.
- Each player has a point pile (starting empty) and a King count (starting 0).

THRESHOLD:
- First player: 32 with 0 Kings, 24 with 1, 18 with 2, 14 with 3, 11 with 4.
- Second player: 30 with 0 Kings, 22 with 1, 16 with 2, 12 with 3, 9 with 4.
- Points are the sum of the ranks in your point pile.
- Shortfall is threshold minus points, with a minimum of 0.

TURNS: Players alternate single turns, First player first. There are at most 40 turns in total (20 each), numbered 1 to 40.

START OF TURN:
1. If the acting player's points are at or above their threshold right now, they win immediately.
2. Otherwise the engine shows everyone the public state:
   - each point pile as a list of cards, each shown as its band if face down or its rank if face up;
   - both King counts and thresholds;
   - the scrap pile;
   - the draw pile size;
   - both hand sizes;
   - the turn number.
3. The acting player also sees their own hand and the exact ranks of their own face-down cards.

ACTION: The acting player chooses exactly one of the following.
(a) DRAW: Take the top card of the draw pile. Not allowed if you hold 8 cards or the pile is empty.
(b) POINTS: Place one point card from your hand face down in your point pile. Its band is visible to the opponent.
(c) SCUTTLE: Choose one point card from your hand and one card in the opponent's point pile. Reveal both.
   - If your rank is equal to or higher than the target's rank, both go to scrap.
   - Otherwise your card goes to scrap and the target stays in place, now face up.
(d) KING-SCUTTLE: Play a 10 from your hand against an opponent's King. Both go to scrap and the opponent's King count falls by 1.
(e) JACK: Play a Jack from your hand and choose any card in the opponent's point pile. It moves to your point pile face up, and the Jack goes to scrap.
(f) KING: Place a King from your hand. Your King count rises by 1.
(g) PASS: Allowed only if you cannot draw.
An illegal or unparseable choice counts as PASS.

END: After turn 40, the player with the smaller shortfall wins. Equal shortfalls are a draw.

How the winner is decided: You win at the start of any of your own turns if your point total is at or above your threshold. If no one has won after turn 40, the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls are a draw.
````

## Reply

````
```json
{
  "name": "Blind Scuttle",
  "summary": "Two players race to build a point pile that reaches a threshold lowered by Kings. Point cards go in face down with only their band visible, and the opponent can scuttle, steal or flip them.",
  "players": {"min": 2, "max": 2, "suggested": 2},
  "parameters": {
    "deck_size": 48,
    "point_ranks_min": 1,
    "point_ranks_max": 10,
    "copies_per_rank": 4,
    "point_cards": 40,
    "jacks": 4,
    "kings": 4,
    "hand_deal": 6,
    "draw_pile_start": 36,
    "hand_limit_for_draw": 8,
    "max_turns": 40,
    "turns_each": 20,
    "low_band_max": 4,
    "mid_band_min": 5,
    "mid_band_max": 7,
    "high_band_min": 8,
    "first_threshold_0k": 32,
    "first_threshold_1k": 24,
    "first_threshold_2k": 18,
    "first_threshold_3k": 14,
    "first_threshold_4k": 11,
    "second_threshold_0k": 30,
    "second_threshold_1k": 22,
    "second_threshold_2k": 16,
    "second_threshold_3k": 12,
    "second_threshold_4k": 9,
    "king_scuttle_rank": 10,
    "shortfall_min": 0
  },
  "attributes": {
    "player": [
      {"key": "is_first", "type": "bool", "visible": "public", "initial": false, "meaning": "True for the randomly chosen First player.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Private hand. Cards are coded '1'..'10', 'J' and 'K'.", "observable": false},
      {"key": "hand_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in hand, which is public.", "observable": false},
      {"key": "point_pile", "type": "list", "visible": "ally", "initial": [], "meaning": "Exact point pile in order. Each entry is 'D<rank>' if face down or 'U<rank>' if face up.", "observable": false},
      {"key": "point_pile_view", "type": "list", "visible": "public", "initial": [], "meaning": "Public view of the point pile, position by position. A face-down card shows as Low, Mid or High; a face-up card shows its rank.", "observable": true},
      {"key": "points", "type": "number", "visible": "ally", "initial": 0, "meaning": "Sum of the ranks in the point pile.", "observable": true},
      {"key": "king_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of Kings placed and not yet scuttled.", "observable": true},
      {"key": "threshold", "type": "number", "visible": "public", "initial": 30, "meaning": "Target points, set from is_first and king_count by the threshold table.", "observable": true},
      {"key": "shortfall", "type": "number", "visible": "ally", "initial": 30, "meaning": "max(threshold - points, 0).", "observable": true},
      {"key": "won", "type": "number", "visible": "public", "initial": 0, "meaning": "Set to 1 when the player wins at the start of their own turn.", "observable": true}
    ],
    "game": [
      {"key": "draw_pile", "type": "list", "visible": "none", "initial": [], "meaning": "Face-down draw pile, shuffled. Drawing takes a random entry.", "observable": false},
      {"key": "scrap", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up scrap pile.", "observable": false},
      {"key": "turn", "type": "number", "visible": "public", "initial": 1, "meaning": "Current turn number, 1 to 40.", "observable": true},
      {"key": "acting_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat whose turn it is.", "observable": false},
      {"key": "action", "type": "text", "visible": "public", "initial": "", "meaning": "Action chosen this turn.", "observable": false},
      {"key": "chosen_card", "type": "text", "visible": "public", "initial": "", "meaning": "Hand card chosen for POINTS or SCUTTLE. It is revealed when it is played.", "observable": false},
      {"key": "target_index", "type": "number", "visible": "public", "initial": 0, "meaning": "Position in the opponent's point pile targeted by SCUTTLE or JACK.", "observable": false}
    ]
  },
  "setup": [
    "Build the 48-card deck as a list: four each of '1' to '10', four 'J' and four 'K'. Put it in draw_pile.",
    "Pick one seat at random as First player: set is_first true for it and set acting_seat to that seat.",
    "Deal 6 cards to each player by drawing at random from draw_pile into hand. This leaves 36 in draw_pile. Set hand_count to 6.",
    "Set threshold to 32 for the First player and 30 for the second. Set shortfall equal to threshold, points to 0 and king_count to 0. point_pile, point_pile_view and scrap start empty. turn is 1."
  ],
  "round": [
    {"action": "update", "who": "acting seat", "answer": null, "effect": "If the acting player's points >= threshold, set their won = 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if any player's won == 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce the public state: each player's point_pile_view, king_count and threshold; scrap; len(draw_pile); each hand_count; turn; acting_seat."},
    {"action": "sync", "who": "acting seat", "answer": null, "effect": "The acting player sees their own hand and point_pile, which includes the exact ranks of their face-down cards."},
    {"action": "ask", "who": "acting seat", "answer": "one of the legal actions: draw, points, scuttle, king_scuttle, jack, king, pass", "effect": "Set action. An illegal or unparseable reply sets action = pass."},
    {"action": "ask", "who": "acting seat", "answer": "a point card ('1'..'10') from hand", "effect": "When action is points or scuttle, set chosen_card. If the reply is not a point card in hand, set action = pass."},
    {"action": "ask", "who": "acting seat", "answer": "a position in the opponent's point_pile_view, from 1 to its length", "effect": "When action is scuttle or jack, set target_index. An invalid reply sets action = pass."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == draw: move a random card from draw_pile to the acting player's hand, and add 1 to hand_count."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == points: remove chosen_card from hand, append 'D<rank>' to point_pile, append its band (Low for 1-4, Mid for 5-7, High for 8-10) to point_pile_view, add rank to points, and subtract 1 from hand_count."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == scuttle: remove chosen_card from hand, subtract 1 from hand_count, and reveal chosen_card and the target's rank. If chosen rank >= target rank, remove the target entry from the opponent's point_pile and point_pile_view, subtract its rank from the opponent's points, and append both ranks to scrap. Otherwise append chosen_card to scrap and turn the target face up: its point_pile entry becomes 'U<rank>' and its view entry becomes its rank."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == king_scuttle: remove one '10' from hand, subtract 1 from hand_count, append '10' and 'K' to scrap, subtract 1 from the opponent's king_count, and recompute the opponent's threshold."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == jack: remove 'J' from hand, subtract 1 from hand_count, and append 'J' to scrap. Remove the target entry from the opponent's point_pile and point_pile_view and subtract its rank from the opponent's points. Append 'U<rank>' to the acting point_pile, append the rank to the acting point_pile_view, and add the rank to the acting points."},
    {"action": "update", "who": "acting seat", "answer": null, "effect": "When action == king: remove 'K' from hand, subtract 1 from hand_count, add 1 to king_count, and recompute threshold."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Recompute each player's threshold from the table: First is [32,24,18,14,11][king_count] and second is [30,22,16,12,9][king_count]. Set shortfall = max(threshold - points, 0). Add 1 to turn and switch acting_seat to the other seat."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if turn > 40."}
  ],
  "ending": {
    "condition": "any player's won == 1, or turn > 40",
    "rank_by": "you.won * 1000 - you.shortfall",
    "decided_by": "A player who reaches their threshold at the start of their own turn wins at once. Otherwise, after turn 40, the player with the smaller shortfall (threshold minus points, minimum 0) wins, and equal shortfalls share the result as a draw."
  },
  "rules": [
    {"id": "R1", "text": "When setup is done, each player has 6 cards in hand, draw_pile has 36 cards, and the deck had 40 point cards (ranks 1-10, four each), 4 Jacks and 4 Kings."},
    {"id": "R2", "text": "When the game starts, a random seat is First, and the First player takes turn 1."},
    {"id": "R3", "text": "When the players alternate single turns, the game has at most 40 turns, numbered 1 to 40."},
    {"id": "R4", "text": "When the First player has 0, 1, 2, 3 or 4 Kings, then their threshold is 32, 24, 18, 14 or 11."},
    {"id": "R5", "text": "When the second player has 0, 1, 2, 3 or 4 Kings, then their threshold is 30, 22, 16, 12 or 9."},
    {"id": "R6", "text": "When a turn starts and the acting player's points are at or above their threshold, then that player wins immediately."},
    {"id": "R7", "text": "When a player chooses DRAW, then a card moves from draw_pile to their hand. DRAW is not allowed with 8 cards in hand or an empty draw_pile."},
    {"id": "R8", "text": "When a player plays POINTS with a card of rank r, then it goes face down into their point pile, their points rise by r, and the opponent sees only its band (Low 1-4, Mid 5-7, High 8-10)."},
    {"id": "R9", "text": "When a player scuttles with rank a against a target of rank t and a >= t, then both cards go to scrap and the opponent's points fall by t."},
    {"id": "R10", "text": "When a player scuttles with rank a against a target of rank t and a < t, then the attacking card goes to scrap and the target stays in place, now face up."},
    {"id": "R11", "text": "When a player plays a 10 against an opponent who has at least one King, then the 10 and a King go to scrap and the opponent's king_count falls by 1."},
    {"id": "R12", "text": "When a player plays a Jack on any card in the opponent's point pile, then that card moves face up into the player's point pile, both point totals change by its rank, and the Jack goes to scrap."},
    {"id": "R13", "text": "When a player places a King, then their king_count rises by 1 and their threshold drops to the next table value."},
    {"id": "R14", "text": "When a player cannot draw, then PASS is allowed."},
    {"id": "R15", "text": "When a reply is illegal or unparseable, then it counts as PASS and nothing changes."},
    {"id": "R16", "text": "When turn 40 ends with no winner, then the player with the smaller max(threshold - points, 0) wins, and equal shortfalls are a draw."}
  ],
  "offers": [
    {"question": "Action choice", "who": "acting seat", "options": "draw if hand_count < 8 and draw_pile is not empty; points if the hand holds a point card; scuttle if the hand holds a point card and the opponent's point pile is not empty; king_scuttle if the hand holds a 10 and the opponent's king_count >= 1; jack if the hand holds a J and the opponent's point pile is not empty; king if the hand holds a K; pass only if draw is not allowed."},
    {"question": "Card to play", "who": "acting seat, when action is points or scuttle", "options": "each distinct point-card rank ('1'..'10') in the acting player's hand."},
    {"question": "Target card", "who": "acting seat, when action is scuttle or jack", "options": "each position 1..n in the opponent's point pile, shown by its public view (band or face-up rank)."}
  ],
  "choices": [
    {"what": "Exactly 2 players, suggested 2", "why": "The designer fixed the game at two, and the asymmetric thresholds for First and second only make sense head to head."},
    {"what": "Card codes '1'..'10', 'J', 'K' and point-pile entries 'D<rank>' / 'U<rank>'", "why": "Lists of text codes are needed to track face-down versus face-up cards and their ranks."},
    {"what": "A separate public point_pile_view beside the private point_pile", "why": "The opponent may see bands and face-up ranks but not face-down ranks, while the owner sees the exact ranks."},
    {"what": "One turn per round, with acting_seat alternating", "why": "Players take single alternating turns and the turn count is capped at 40."},
    {"what": "rank_by = won*1000 - shortfall", "why": "An immediate win outranks everything. Otherwise the smaller shortfall ranks higher, and equal values share the win, which models the draw."},
    {"what": "No talk step", "why": "The source has no communication. Players reason only from bands, the scrap pile and King counts."},
    {"what": "The King-scuttle and Jack card choices are not asked", "why": "The card used is fixed (a 10 or a J), and a King-scuttle target is just one of the opponent's Kings, which are interchangeable."}
  ],
  "simplifications": [
    {"what": "The top card of the draw pile is a random card from draw_pile", "why": "The engine draws at random from a list, which is equivalent to a shuffled pile."},
    {"what": "Placed Kings are tracked only by king_count, not as a list of cards", "why": "Kings have no identity beyond their count. When one is scuttled, a 'K' is appended to scrap."},
    {"what": "Only legal actions are offered, and any invalid reply becomes PASS", "why": "This follows the rule that an illegal choice counts as PASS and keeps the offers clean."}
  ],
  "unsupported": []
}
```
````
