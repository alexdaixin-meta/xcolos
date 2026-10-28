# 18 spec

- time: 2026-10-28T05:42:00+00:00 (47.0s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 5b9de39751612b84, reply sha256 18ada756a1de841b

## Sent

````
Game: Short Dudo
Players in the source: 2 to 4
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP. 2 to 4 players sit in a fixed seat order: seat 1, seat 2, and so on. Each player starts with 5 dice. Seat 1 is the opener for round 1. There is no random draw before play.

EACH ROUND.
1. ROLL. In one deal operation, every player still in the game receives a fresh random roll of as many six-sided dice as they currently hold. This single operation produces all hands at once and is the only random event of the round. Each player is shown only their own dice. T is the total number of dice still in play, and every player is told T and every player's dice count.
2. OPENING BID (choice 1). The opener chooses a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). The bid means 'at least Q dice among all players show this face, with every 1 counting as this face'. The bid is announced to all.
3. RESPONSE 1 (choice 2). The next player in seat order who is still in the game chooses one of four options:
   (a) Raise +1: the new quantity is the current quantity + 1, with any face from 2 to 6 the player chooses.
   (b) Raise +2: the new quantity is the current quantity + 2, with any face from 2 to 6 the player chooses.
   (c) Dudo: challenge the current bid as false.
   (d) Calza: claim the count is exactly the current quantity.
   A raise is illegal if the new quantity would exceed T. If both raises are illegal, only Dudo or Calza may be chosen. The choice is announced. A player who raises becomes the current bidder.
4. RESPONSE 2 (choice 3). This step happens only if response 1 was a raise. The next player in seat order who is still in the game makes the same kind of choice against the current bid. With 2 players, this is the opener again.
5. FINAL RESPONSE (choice 4). This step happens only if response 2 was a raise. The next player in seat order who is still in the game must choose Dudo or Calza. Raising is not allowed.
6. REVEAL. All dice are shown. N is the number of dice showing the current bid face plus the number showing 1, computed as one count over all dice.
7. SETTLE. If the call was Dudo: when N >= the current quantity, the caller loses 1 die; otherwise the current bidder loses 1 die. If the call was Calza: when N equals the current quantity exactly, the caller gains 1 die, up to a maximum of 5; otherwise the caller loses 1 die.
8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from then on.
9. NEXT OPENER. The player who lost a die opens the next round. After a successful Calza, the caller opens. If that player was eliminated, the next player in seat order who is still in the game opens.
10. END CHECK. If only one player remains, the game ends. If 30 rounds have been played, the game ends. Otherwise a new round begins.

There is no talk phase. Bids and calls are the only communication.

How the winner is decided: If only one player has dice left, that player wins. If 30 rounds are completed with two or more players still in, the player holding the most dice wins. If two or more players tie for the most dice, the game is a draw.
````

## Reply

````
```json
{
  "name": "Short Dudo",
  "summary": "A short bluffing dice game. Players bid on how many dice around the table show a face, with 1s wild. The next players raise, call Dudo (false) or call Calza (exact), and the loser of each call loses a die.",
  "players": {"min": 2, "max": 4, "suggested": 3},
  "parameters": {
    "start_dice": 5,
    "max_dice": 5,
    "die_faces": 6,
    "wild_face": 1,
    "min_bid_face": 2,
    "max_bid_face": 6,
    "opening_min_divisor": 3,
    "opening_min_floor": 1,
    "opening_max_divisor": 2,
    "raise_small": 1,
    "raise_big": 2,
    "dudo_loss": 1,
    "calza_loss": 1,
    "calza_gain": 1,
    "max_rounds": 30,
    "first_opener_seat": 1,
    "max_responses_per_round": 3
  },
  "attributes": {
    "player": [
      {"key": "dice_count", "type": "number", "visible": "public", "initial": 5, "meaning": "How many dice this player holds. This is the score.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "This round's die faces (1-6) for this player, seen only by the owner until the reveal.", "observable": false},
      {"key": "out", "type": "bool", "visible": "public", "initial": false, "meaning": "True once the player has 0 dice. An out player is skipped in seat order.", "observable": true}
    ],
    "game": [
      {"key": "round_num", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds started so far.", "observable": true},
      {"key": "opener_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat that opens the bidding this round.", "observable": false},
      {"key": "total_dice", "type": "number", "visible": "public", "initial": 0, "meaning": "T: total dice held by players still in the game.", "observable": false},
      {"key": "current_face", "type": "number", "visible": "public", "initial": 0, "meaning": "Face (2-6) of the standing bid.", "observable": false},
      {"key": "current_qty", "type": "number", "visible": "public", "initial": 0, "meaning": "Quantity of the standing bid.", "observable": false},
      {"key": "current_bidder", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that made the standing bid.", "observable": false},
      {"key": "responder_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat due to respond next: the next seat after current_bidder that is not out.", "observable": false},
      {"key": "call_type", "type": "text", "visible": "public", "initial": "", "meaning": "Empty while bidding continues, otherwise 'dudo' or 'calza'.", "observable": false},
      {"key": "caller_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that called Dudo or Calza.", "observable": false},
      {"key": "reveal_count", "type": "number", "visible": "public", "initial": 0, "meaning": "N: dice in all hands showing current_face plus dice showing 1.", "observable": false},
      {"key": "loser_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that lost a die this round, or 0 if none did.", "observable": false}
    ]
  },
  "setup": [
    "Seats are numbered 1 to the player count in a fixed order.",
    "Each player's dice_count is set to 5, hand is set empty and out is set false.",
    "opener_seat is set to 1 and round_num to 0.",
    "There is no random draw before play."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round_num += 1. call_type = '', caller_seat = 0 and loser_seat = 0. total_dice = sum of dice_count over players with out = false."},
    {"action": "initialize", "who": "all players", "answer": null, "effect": "In one deal, every player with out = false gets hand set to dice_count random faces from 1 to 6. Out players keep an empty hand."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees their own hand, total_dice and every player's dice_count and out."},
    {"action": "ask", "who": "seat opener_seat", "answer": "a face from 2 to 6", "effect": "current_face = the chosen face. current_bidder = opener_seat."},
    {"action": "ask", "who": "seat opener_seat", "answer": "a whole number from max(1, floor(total_dice/3)) to ceil(total_dice/2)", "effect": "current_qty = the number. The bid is announced to all. responder_seat = the next seat after current_bidder with out = false."},
    {"action": "ask", "who": "seat responder_seat (response 1)", "answer": "one of raise1_faceF (F = 2..6, offered only if current_qty+1 <= total_dice), raise2_faceF (F = 2..6, offered only if current_qty+2 <= total_dice), dudo, calza", "effect": "On raiseK_faceF: current_qty += K, current_face = F, current_bidder = responder_seat, then responder_seat = the next seat after current_bidder with out = false. On dudo or calza: call_type = the choice, caller_seat = responder_seat. The choice is announced to all."},
    {"action": "ask", "who": "seat responder_seat (response 2), when call_type = ''", "answer": "the same options as response 1, with the same legality limits", "effect": "The same as response 1. With 2 players this seat is the opener."},
    {"action": "ask", "who": "seat responder_seat (final response), when call_type = ''", "answer": "dudo or calza", "effect": "call_type = the choice, caller_seat = responder_seat. The choice is announced to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Reveal: every hand is shown to all. reveal_count = count over all hands of dice equal to current_face or equal to 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Settle. If call_type = 'dudo' and reveal_count >= current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. If call_type = 'dudo' and reveal_count < current_qty: current_bidder dice_count -= 1, loser_seat = current_bidder. If call_type = 'calza' and reveal_count = current_qty: caller_seat dice_count = min(dice_count + 1, 5), loser_seat = 0. If call_type = 'calza' and reveal_count != current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. The result is announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Elimination: any player with dice_count = 0 gets out = true."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Next opener. If loser_seat > 0, opener_seat = loser_seat; otherwise (a successful Calza) opener_seat = caller_seat. If that seat has out = true, opener_seat = the next seat after it with out = false."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if the number of players with out = false is 1, or if round_num >= 30. Otherwise start a new round."}
  ],
  "ending": {
    "condition": "count of players with out = false == 1 OR round_num >= 30",
    "rank_by": "you.dice_count",
    "decided_by": "Each player's standing is the dice they hold. A lone survivor holds the only dice and wins. After 30 rounds the player with the most dice wins, and players tied for the most share the result, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "At setup every player has dice_count 5 and out false, and seat 1 opens round 1."},
    {"id": "R2", "text": "Each round, every player not out gets a fresh hand of exactly dice_count random faces from 1 to 6, visible only to the owner."},
    {"id": "R3", "text": "total_dice equals the sum of dice_count over players not out, and it is told to everyone with every dice_count."},
    {"id": "R4", "text": "The opener bids a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). For example, with T = 15, Q is from 5 to 8."},
    {"id": "R5", "text": "When a responder chooses Raise +1, current_qty increases by 1, current_face becomes their chosen face from 2 to 6, and they become current_bidder."},
    {"id": "R6", "text": "When a responder chooses Raise +2, current_qty increases by 2, current_face becomes their chosen face from 2 to 6, and they become current_bidder."},
    {"id": "R7", "text": "When a raise would make current_qty exceed total_dice, that raise is not offered. If both raises exceed it, only Dudo and Calza are offered."},
    {"id": "R8", "text": "The responder is always the next seat in order after the current bidder that is not out. With 2 players, response 2 is answered by the opener."},
    {"id": "R9", "text": "Response 2 happens only when response 1 was a raise, and the final response happens only when response 2 was a raise."},
    {"id": "R10", "text": "The final responder may choose only Dudo or Calza."},
    {"id": "R11", "text": "At reveal, N counts every die in all hands that shows current_face or shows 1."},
    {"id": "R12", "text": "When Dudo is called and N >= current_qty, the caller loses 1 die."},
    {"id": "R13", "text": "When Dudo is called and N < current_qty, the current bidder loses 1 die."},
    {"id": "R14", "text": "When Calza is called and N == current_qty, the caller gains 1 die, but never above 5."},
    {"id": "R15", "text": "When Calza is called and N != current_qty, the caller loses 1 die."},
    {"id": "R16", "text": "When a player's dice_count reaches 0, out becomes true, and the player is skipped in seat order and gets no hand from then on."},
    {"id": "R17", "text": "The player who lost a die opens the next round. After a successful Calza the caller opens. If that player is out, the next seat in order that is not out opens."},
    {"id": "R18", "text": "When only one player is not out, the game ends and that player wins."},
    {"id": "R19", "text": "When 30 rounds have been played, the game ends and the highest dice_count wins. Players tied at the top share the result as a draw."}
  ],
  "offers": [
    {"question": "Opening face", "who": "the opener", "options": "faces 2, 3, 4, 5, 6"},
    {"question": "Opening quantity", "who": "the opener", "options": "whole numbers from max(1, floor(total_dice/3)) to ceil(total_dice/2)"},
    {"question": "Response 1 and response 2", "who": "the next seat after the current bidder that is not out", "options": "If current_qty + 2 <= total_dice: raise1_face2..raise1_face6, raise2_face2..raise2_face6, dudo, calza. If only current_qty + 1 <= total_dice: raise1_face2..raise1_face6, dudo, calza. If current_qty + 1 > total_dice: dudo, calza."},
    {"question": "Final response", "who": "the next seat after the current bidder that is not out", "options": "dudo, calza"}
  ],
  "choices": [
    {"what": "2 to 4 players, suggested 3", "why": "The designer suggests 3. Two is the smallest table where a bid can be doubted. Above 4 the 3-response limit means most seats never act in a round."},
    {"what": "No talk phase", "why": "The source says bids and calls are the only communication. Bluffing happens through the bids themselves."},
    {"what": "Strategy at the table", "why": "A thoughtful player estimates the expected count from their own hand plus T/3 for the unseen dice, bluffs bids toward faces they hold, reads the raises of others, and saves Calza for when they hold the bid face, since a correct Calza gains a die."}
  ],
  "simplifications": [
    {"what": "The opening bid is asked as two questions to the same seat, face then quantity", "why": "One answer is either a choice or a number, never both."},
    {"what": "A raise and its face are offered as one combined choice, such as raise2_face4", "why": "This lets one choice question carry the raise size and the face, with illegal raises left out."},
    {"what": "A tie for most dice after 30 rounds is a shared top result rather than a separate 'draw' outcome", "why": "The engine has no separate draw. Players level at the top share the win, which records the draw."}
  ],
  "unsupported": []
}
```
````
