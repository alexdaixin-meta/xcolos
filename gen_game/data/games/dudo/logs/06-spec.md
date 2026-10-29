# 06 spec

- time: 2026-10-28T05:29:58+00:00 (48.5s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 e88fb32b662920c8, reply sha256 9adff1e8d5a0b1c9

## Sent

````
Game: Open-Table Dudo
Players in the source: 2 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP: Seat the players in a random order, numbered seat 1 upward, with clockwise meaning increasing seat number and wrapping from the last seat to seat 1. Starting dice depend on the number of players: 2 players start with 4 dice each, 3 players with 3 each, 4 players with 2 each. Every player rolls their dice (six-sided, faces 1 to 6). Each player is privately shown their own faces and no one else's. Seat 1 is the opener of the first hand.

PUBLIC INFORMATION: At every turn all players are told how many dice each player holds, the total number of dice in play (T), the current bid and who made it (if any), and the list of bids made so far in this hand.

BIDS: A bid is a quantity and a face from 2 to 6, for example 'three 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be named as a bid face.

EACH ROUND IS ONE TURN by the player to act.
(a) If there is no current bid, the player to act is the opener and must make an opening bid. The quantity must be at least max(1, floor(T / 4)) and at most T. If the opener calls Dudo instead, or makes an invalid bid, the opener loses one die and the hand ends with no count.
(b) If there is a current bid, the player to act either raises or calls 'Dudo'. A raise is a new bid whose quantity is at least the current quantity plus 1 and at most T, with any face from 2 to 6. An invalid raise counts as a Dudo call. If the current quantity already equals T, the player must call Dudo.
(c) After a valid bid or raise, it becomes the current bid, and the next surviving player clockwise is the player to act in the next round. Bidding wraps around the table as many times as needed.
(d) DUDO: When a player calls Dudo on the current bid, all dice are revealed to everyone. Count the dice showing the bid face plus all ones. If the count is at least the bid quantity, the bid was true and the caller loses one die. Otherwise the bid was false and the bidder loses one die. The hand ends.

AFTER A HAND ENDS (this happens in the same round as the Dudo call or failed opening): A player with 0 dice is eliminated, and this is announced. The player who lost the die becomes the opener of the next hand. If that player was eliminated, the next surviving player clockwise from them is the opener. The current bid is cleared. Every surviving player rolls all their remaining dice and is privately shown their own faces. T is recomputed. The opener acts in the next round.

END: The game ends immediately when only one player has dice left. The game also ends after round 40. In that case any hand still in progress is not resolved and its bids are ignored.

How the winner is decided: The last player with at least one die wins, and every other player loses. If the game ends after round 40 with more than one player holding dice, the player holding the most dice wins. If several players are tied for the most dice, it is a draw among those tied and every other player loses.
````

## Reply

````
```json
{
  "name": "Open-Table Dudo",
  "summary": "Bluffing dice game: players secretly roll dice, raise bids on how many dice show a face (ones are wild), and call Dudo to challenge; each lost challenge costs a die, and the last player with dice wins.",
  "players": {"min": 2, "max": 4, "suggested": 3},
  "parameters": {
    "start_dice_2_players": 4,
    "start_dice_3_players": 3,
    "start_dice_4_players": 2,
    "die_sides": 6,
    "wild_face": 1,
    "bid_face_min": 2,
    "bid_face_max": 6,
    "opening_quantity_divisor": 4,
    "opening_quantity_floor": 1,
    "raise_quantity_step": 1,
    "dice_lost_per_challenge": 1,
    "max_rounds": 40
  },
  "attributes": {
    "player": [
      {"key": "dice", "type": "number", "visible": "public", "initial": "6 - player_count (4 with 2 players, 3 with 3, 2 with 4)", "meaning": "How many dice this player still holds; 0 means eliminated", "observable": true},
      {"key": "faces", "type": "list", "visible": "ally", "initial": "dice random integers from 1 to 6", "meaning": "This player's current rolled faces, shown only to the owner until a Dudo reveals them", "observable": false},
      {"key": "eliminated", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the player has 0 dice", "observable": true}
    ],
    "game": [
      {"key": "round_no", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of rounds (turns) played so far", "observable": true},
      {"key": "total_dice", "type": "number", "visible": "public", "initial": "sum of dice over all players", "meaning": "T, the total number of dice in play", "observable": false},
      {"key": "to_act", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the player to act this round", "observable": false},
      {"key": "opener", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that opens the current hand", "observable": false},
      {"key": "current_qty", "type": "number", "visible": "public", "initial": 0, "meaning": "Quantity of the current bid; 0 means no current bid", "observable": false},
      {"key": "current_face", "type": "number", "visible": "public", "initial": 0, "meaning": "Face of the current bid (2 to 6); 0 means no bid", "observable": false},
      {"key": "current_bidder", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that made the current bid; 0 means none", "observable": false},
      {"key": "bids", "type": "list", "visible": "public", "initial": [], "meaning": "Bids made so far in this hand, as 'seat: quantity x face'", "observable": false},
      {"key": "action", "type": "text", "visible": "public", "initial": "", "meaning": "This round's choice by the player to act: bid, raise or dudo", "observable": false},
      {"key": "bid_qty", "type": "number", "visible": "public", "initial": 0, "meaning": "Quantity named this round", "observable": false},
      {"key": "bid_face", "type": "number", "visible": "public", "initial": 0, "meaning": "Face named this round", "observable": false},
      {"key": "matching", "type": "number", "visible": "public", "initial": 0, "meaning": "At a Dudo, the count of revealed dice showing the bid face or 1", "observable": false},
      {"key": "loser", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that lost a die when the hand ended; 0 while the hand is in progress", "observable": false},
      {"key": "survivors", "type": "number", "visible": "public", "initial": "player_count", "meaning": "Number of players with at least one die", "observable": true}
    ]
  },
  "setup": [
    "Seat the players in random order, numbered seat 1 upward; clockwise means increasing seat number, wrapping from the last seat to seat 1.",
    "Each player's dice is set to 6 minus the player count: 4 with 2 players, 3 with 3, 2 with 4.",
    "Each player's faces is set to that many random integers from 1 to 6 and is shown privately to its owner only.",
    "total_dice is set to the sum of dice; opener and to_act are set to 1; current_qty, current_face and current_bidder are set to 0; bids is emptied; survivors is set to the player count."
  ],
  "round": [
    {"action": "update", "who": "table", "answer": null, "effect": "round_no += 1; loser = 0; action = ''; bid_qty = 0; bid_face = 0"},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce each seat's dice, total_dice (T), the current bid (current_qty x current_face by current_bidder, or 'none'), bids, and that seat to_act is to act"},
    {"action": "ask", "who": "seat to_act", "answer": "choice: 'bid' or 'dudo' when current_qty = 0; 'raise' or 'dudo' when 0 < current_qty < total_dice; only 'dudo' when current_qty = total_dice", "effect": "action = the choice"},
    {"action": "ask", "who": "seat to_act, when action is 'bid' or 'raise'", "answer": "whole number from max(1, floor(total_dice / 4)) to total_dice when action = 'bid'; from current_qty + 1 to total_dice when action = 'raise'", "effect": "bid_qty = the number"},
    {"action": "ask", "who": "seat to_act, when action is 'bid' or 'raise'", "answer": "whole number from 2 to 6", "effect": "bid_face = the number"},
    {"action": "update", "who": "table, when action is 'bid' or 'raise'", "answer": null, "effect": "current_qty = bid_qty; current_face = bid_face; current_bidder = to_act; append 'seat to_act: bid_qty x bid_face' to bids; to_act = the next seat clockwise from to_act with eliminated = false; announce the new bid"},
    {"action": "update", "who": "table, when action = 'dudo' and current_qty = 0", "answer": null, "effect": "Failed opening: loser = to_act; that player's dice -= 1; announce that the opener lost a die with no count"},
    {"action": "update", "who": "table, when action = 'dudo' and current_qty > 0", "answer": null, "effect": "Reveal every player's faces to all; matching = number of faces over all surviving players equal to current_face or to 1; if matching >= current_qty then loser = to_act (the caller), else loser = current_bidder; the loser's dice -= 1; announce the reveal, matching, and the loser"},
    {"action": "update", "who": "table, when loser > 0", "answer": null, "effect": "Every player with dice = 0 gets eliminated = true, announced; survivors = number of players with dice >= 1"},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if survivors = 1"},
    {"action": "update", "who": "table, when loser > 0", "answer": null, "effect": "opener = loser if the loser has eliminated = false, else the next seat clockwise from loser with eliminated = false; current_qty = 0; current_face = 0; current_bidder = 0; empty bids; each surviving player's faces = dice new random integers from 1 to 6, shown privately to the owner; total_dice = sum of dice; to_act = opener"},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player is sent their own faces and the public state"},
    {"action": "check", "who": "table", "answer": null, "effect": "End the game if round_no >= 40; a hand still in progress is not resolved"}
  ],
  "ending": {
    "condition": "survivors = 1 or round_no >= 40",
    "rank_by": "you.dice",
    "decided_by": "Each player's standing is the number of dice they hold. If only one player has dice, they win alone. If round 40 ends with several players holding dice, the player with the most dice wins, and players tied for the most share the win (a draw among them). Every other player loses."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts with 2, 3 or 4 players, then each player holds 4, 3 or 2 dice respectively."},
    {"id": "R2", "text": "When dice are rolled, then each die shows a face from 1 to 6, and each player sees only their own faces."},
    {"id": "R3", "text": "When the game starts, then seat 1 is the opener and acts in round 1."},
    {"id": "R4", "text": "When there is no current bid, then the player to act must make an opening bid with quantity from max(1, floor(T/4)) to T and face from 2 to 6, or call Dudo."},
    {"id": "R5", "text": "When the opener calls Dudo with no current bid, then the opener loses 1 die and the hand ends with no count."},
    {"id": "R6", "text": "When there is a current bid of quantity q with q < T, then the player to act either raises with quantity from q+1 to T and any face from 2 to 6, or calls Dudo."},
    {"id": "R7", "text": "When the current bid's quantity equals T, then the player to act must call Dudo."},
    {"id": "R8", "text": "When a valid bid or raise is made, then it becomes the current bid, it is added to the hand's bid list, and the next surviving seat clockwise acts next round."},
    {"id": "R9", "text": "When Dudo is called on a bid of q dice of face f, then all dice are revealed, and the count is the dice showing f plus all dice showing 1."},
    {"id": "R10", "text": "When at a Dudo the count is at least q, then the caller loses 1 die; otherwise the bidder loses 1 die."},
    {"id": "R11", "text": "When a player reaches 0 dice, then that player is eliminated and this is announced."},
    {"id": "R12", "text": "When a hand ends, then the player who lost the die opens the next hand, or the next surviving seat clockwise from them if they were eliminated."},
    {"id": "R13", "text": "When a hand ends, then the current bid and bid list are cleared, every surviving player rerolls all their dice privately, and T is recomputed."},
    {"id": "R14", "text": "When only one player has dice left, then the game ends immediately and that player wins."},
    {"id": "R15", "text": "When round 40 ends with more than one player holding dice, then the game ends, the hand in progress is not resolved, and the player(s) with the most dice win, sharing the win if tied."},
    {"id": "R16", "text": "At every turn, all players are told each player's dice count, T, the current bid and who made it, and this hand's bid list."}
  ],
  "offers": [
    {"question": "Choose an action", "who": "seat to_act", "options": "with no current bid: bid, dudo; with a current bid below T: raise, dudo; with a current bid equal to T: dudo"},
    {"question": "Bid quantity", "who": "seat to_act after choosing bid or raise", "options": "opening bid: max(1, floor(T/4)) to T; raise: current_qty + 1 to T"},
    {"question": "Bid face", "who": "seat to_act after choosing bid or raise", "options": "2, 3, 4, 5, 6"}
  ],
  "choices": [
    {"what": "2 to 4 players, suggested 3", "why": "The designer suggests 3. The minimum is 2 because one rival is enough to bluff against. The maximum is 4 because the source scales starting dice only that far (2 each at 4 players), and more seats would leave too few dice per player."},
    {"what": "Starting dice written as 6 minus the player count", "why": "This matches 4, 3 and 2 for 2, 3 and 4 players, so it holds at every table size."},
    {"what": "No separate talk step", "why": "The bids themselves are the communication and bluff. Free talk would add words without a decision the rules contain."},
    {"what": "The opener is offered 'dudo' at an empty table", "why": "The source explicitly gives this option and its penalty (the opener loses 1 die)."},
    {"what": "Strategy at the table", "why": "A thoughtful player estimates expected matches from their own faces plus about a third of unseen dice (ones are wild), raises to a bid they can defend, bluffs when the next player is likely to over-call, and calls Dudo when a bid exceeds a plausible count."}
  ],
  "simplifications": [
    {"what": "Invalid bids cannot be entered", "why": "The engine restricts answers to the allowed choices and number ranges, so the source rules 'an invalid bid or raise counts as Dudo / a failed opening' never trigger."},
    {"what": "A bid is asked as three questions: action, quantity, face", "why": "Each answer must be a single choice or a single number."},
    {"what": "'Next surviving seat clockwise' is computed arithmetically over seat numbers and eliminated flags", "why": "The engine has no seating operand; this uses the player-attribute comparison workaround."},
    {"what": "Rolling dice is modeled as setting the faces list to random integers from 1 to 6", "why": "The engine's seeded randomness stands in for physical dice."}
  ],
  "unsupported": []
}
```
````
