# 11 scenarios

- time: 2026-10-28T05:34:26+00:00 (69.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 2cddd254c9461499, reply sha256 9258a7312742aa2b

## Sent

````
SPEC:
{
  "name": "Open-Table Dudo",
  "summary": "Bluffing dice game: players secretly roll dice, raise bids on how many dice show a face (ones are wild), and call Dudo to challenge; each lost challenge costs a die, and the last player with dice wins.",
  "players": {
    "min": 2,
    "max": 4,
    "suggested": 3
  },
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
      {
        "key": "dice",
        "type": "number",
        "visible": "public",
        "initial": "6 - player_count (4 with 2 players, 3 with 3, 2 with 4)",
        "meaning": "How many dice this player still holds; 0 means eliminated",
        "observable": true
      },
      {
        "key": "faces",
        "type": "list",
        "visible": "ally",
        "initial": "dice random integers from 1 to 6",
        "meaning": "This player's current rolled faces, shown only to the owner until a Dudo reveals them",
        "observable": false
      },
      {
        "key": "eliminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the player has 0 dice",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of rounds (turns) played so far",
        "observable": true
      },
      {
        "key": "total_dice",
        "type": "number",
        "visible": "public",
        "initial": "sum of dice over all players",
        "meaning": "T, the total number of dice in play",
        "observable": false
      },
      {
        "key": "to_act",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the player to act this round",
        "observable": false
      },
      {
        "key": "opener",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that opens the current hand",
        "observable": false
      },
      {
        "key": "current_qty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Quantity of the current bid; 0 means no current bid",
        "observable": false
      },
      {
        "key": "current_face",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face of the current bid (2 to 6); 0 means no bid",
        "observable": false
      },
      {
        "key": "current_bidder",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that made the current bid; 0 means none",
        "observable": false
      },
      {
        "key": "bids",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Bids made so far in this hand, as 'seat: quantity x face'",
        "observable": false
      },
      {
        "key": "action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's choice by the player to act: bid, raise or dudo",
        "observable": false
      },
      {
        "key": "bid_qty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Quantity named this round",
        "observable": false
      },
      {
        "key": "bid_face",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face named this round",
        "observable": false
      },
      {
        "key": "matching",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "At a Dudo, the count of revealed dice showing the bid face or 1",
        "observable": false
      },
      {
        "key": "loser",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that lost a die when the hand ended; 0 while the hand is in progress",
        "observable": false
      },
      {
        "key": "survivors",
        "type": "number",
        "visible": "public",
        "initial": "player_count",
        "meaning": "Number of players with at least one die",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat the players in random order, numbered seat 1 upward; clockwise means increasing seat number, wrapping from the last seat to seat 1.",
    "Each player's dice is set to 6 minus the player count: 4 with 2 players, 3 with 3, 2 with 4.",
    "Each player's faces is set to that many random integers from 1 to 6 and is shown privately to its owner only.",
    "total_dice is set to the sum of dice; opener and to_act are set to 1; current_qty, current_face and current_bidder are set to 0; bids is emptied; survivors is set to the player count."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round_no += 1; loser = 0; action = ''; bid_qty = 0; bid_face = 0"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce each seat's dice, total_dice (T), the current bid (current_qty x current_face by current_bidder, or 'none'), bids, and that seat to_act is to act"
    },
    {
      "action": "ask",
      "who": "seat to_act",
      "answer": "choice: 'bid' or 'dudo' when current_qty = 0; 'raise' or 'dudo' when 0 < current_qty < total_dice; only 'dudo' when current_qty = total_dice",
      "effect": "action = the choice"
    },
    {
      "action": "ask",
      "who": "seat to_act, when action is 'bid' or 'raise'",
      "answer": "whole number from max(1, floor(total_dice / 4)) to total_dice when action = 'bid'; from current_qty + 1 to total_dice when action = 'raise'",
      "effect": "bid_qty = the number"
    },
    {
      "action": "ask",
      "who": "seat to_act, when action is 'bid' or 'raise'",
      "answer": "whole number from 2 to 6",
      "effect": "bid_face = the number"
    },
    {
      "action": "update",
      "who": "table, when action is 'bid' or 'raise'",
      "answer": null,
      "effect": "current_qty = bid_qty; current_face = bid_face; current_bidder = to_act; append 'seat to_act: bid_qty x bid_face' to bids; to_act = the next seat clockwise from to_act with eliminated = false; announce the new bid"
    },
    {
      "action": "update",
      "who": "table, when action = 'dudo' and current_qty = 0",
      "answer": null,
      "effect": "Failed opening: loser = to_act; that player's dice -= 1; announce that the opener lost a die with no count"
    },
    {
      "action": "update",
      "who": "table, when action = 'dudo' and current_qty > 0",
      "answer": null,
      "effect": "Reveal every player's faces to all; matching = number of faces over all surviving players equal to current_face or to 1; if matching >= current_qty then loser = to_act (the caller), else loser = current_bidder; the loser's dice -= 1; announce the reveal, matching, and the loser"
    },
    {
      "action": "update",
      "who": "table, when loser > 0",
      "answer": null,
      "effect": "Every player with dice = 0 gets eliminated = true, announced; survivors = number of players with dice >= 1"
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if survivors = 1"
    },
    {
      "action": "update",
      "who": "table, when loser > 0",
      "answer": null,
      "effect": "opener = loser if the loser has eliminated = false, else the next seat clockwise from loser with eliminated = false; current_qty = 0; current_face = 0; current_bidder = 0; empty bids; each surviving player's faces = dice new random integers from 1 to 6, shown privately to the owner; total_dice = sum of dice; to_act = opener"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own faces and the public state"
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round_no >= 40; a hand still in progress is not resolved"
    }
  ],
  "ending": {
    "condition": "survivors = 1 or round_no >= 40",
    "rank_by": "you.dice",
    "decided_by": "Each player's standing is the number of dice they hold. If only one player has dice, they win alone. If round 40 ends with several players holding dice, the player with the most dice wins, and players tied for the most share the win (a draw among them). Every other player loses."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts with 2, 3 or 4 players, then each player holds 4, 3 or 2 dice respectively."
    },
    {
      "id": "R2",
      "text": "When dice are rolled, then each die shows a face from 1 to 6, and each player sees only their own faces."
    },
    {
      "id": "R3",
      "text": "When the game starts, then seat 1 is the opener and acts in round 1."
    },
    {
      "id": "R4",
      "text": "When there is no current bid, then the player to act must make an opening bid with quantity from max(1, floor(T/4)) to T and face from 2 to 6, or call Dudo."
    },
    {
      "id": "R5",
      "text": "When the opener calls Dudo with no current bid, then the opener loses 1 die and the hand ends with no count."
    },
    {
      "id": "R6",
      "text": "When there is a current bid of quantity q with q < T, then the player to act either raises with quantity from q+1 to T and any face from 2 to 6, or calls Dudo."
    },
    {
      "id": "R7",
      "text": "When the current bid's quantity equals T, then the player to act must call Dudo."
    },
    {
      "id": "R8",
      "text": "When a valid bid or raise is made, then it becomes the current bid, it is added to the hand's bid list, and the next surviving seat clockwise acts next round."
    },
    {
      "id": "R9",
      "text": "When Dudo is called on a bid of q dice of face f, then all dice are revealed, and the count is the dice showing f plus all dice showing 1."
    },
    {
      "id": "R10",
      "text": "When at a Dudo the count is at least q, then the caller loses 1 die; otherwise the bidder loses 1 die."
    },
    {
      "id": "R11",
      "text": "When a player reaches 0 dice, then that player is eliminated and this is announced."
    },
    {
      "id": "R12",
      "text": "When a hand ends, then the player who lost the die opens the next hand, or the next surviving seat clockwise from them if they were eliminated."
    },
    {
      "id": "R13",
      "text": "When a hand ends, then the current bid and bid list are cleared, every surviving player rerolls all their dice privately, and T is recomputed."
    },
    {
      "id": "R14",
      "text": "When only one player has dice left, then the game ends immediately and that player wins."
    },
    {
      "id": "R15",
      "text": "When round 40 ends with more than one player holding dice, then the game ends, the hand in progress is not resolved, and the player(s) with the most dice win, sharing the win if tied."
    },
    {
      "id": "R16",
      "text": "At every turn, all players are told each player's dice count, T, the current bid and who made it, and this hand's bid list."
    }
  ],
  "offers": [
    {
      "question": "Choose an action",
      "who": "seat to_act",
      "options": "with no current bid: bid, dudo; with a current bid below T: raise, dudo; with a current bid equal to T: dudo"
    },
    {
      "question": "Bid quantity",
      "who": "seat to_act after choosing bid or raise",
      "options": "opening bid: max(1, floor(T/4)) to T; raise: current_qty + 1 to T"
    },
    {
      "question": "Bid face",
      "who": "seat to_act after choosing bid or raise",
      "options": "2, 3, 4, 5, 6"
    }
  ],
  "choices": [
    {
      "what": "2 to 4 players, suggested 3",
      "why": "The designer suggests 3. The minimum is 2 because one rival is enough to bluff against. The maximum is 4 because the source scales starting dice only that far (2 each at 4 players), and more seats would leave too few dice per player."
    },
    {
      "what": "Starting dice written as 6 minus the player count",
      "why": "This matches 4, 3 and 2 for 2, 3 and 4 players, so it holds at every table size."
    },
    {
      "what": "No separate talk step",
      "why": "The bids themselves are the communication and bluff. Free talk would add words without a decision the rules contain."
    },
    {
      "what": "The opener is offered 'dudo' at an empty table",
      "why": "The source explicitly gives this option and its penalty (the opener loses 1 die)."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player estimates expected matches from their own faces plus about a third of unseen dice (ones are wild), raises to a bid they can defend, bluffs when the next player is likely to over-call, and calls Dudo when a bid exceeds a plausible count."
    }
  ],
  "simplifications": [
    {
      "what": "Invalid bids cannot be entered",
      "why": "The engine restricts answers to the allowed choices and number ranges, so the source rules 'an invalid bid or raise counts as Dudo / a failed opening' never trigger."
    },
    {
      "what": "A bid is asked as three questions: action, quantity, face",
      "why": "Each answer must be a single choice or a single number."
    },
    {
      "what": "'Next surviving seat clockwise' is computed arithmetically over seat numbers and eliminated flags",
      "why": "The engine has no seating operand; this uses the player-attribute comparison workaround."
    },
    {
      "what": "Rolling dice is modeled as setting the faces list to random integers from 1 to 6",
      "why": "The engine's seeded randomness stands in for physical dice."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: dice, eliminated; table: round_no, survivors.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Do not assert that a value is never offered to a seat when that value is legal on another prompt that seat sees. For the opening bid with T = 9, assert that quantities 1 and 10 are not offered and 2 through 9 are. For the face, check only face-range exclusions that cannot clash with legal quantities: face 1 is already covered by the quantity check, and 7 is a legal quantity. Better still, check the face by its effect: play a face move of 2 or 6 and assert the resulting current bid, rather than asserting that 7 is absent from all of seat 1's options. Keep asserting the resulting current bid and the scores, not internal bookkeeping.
````

## Reply

````
```json
[
  {"name": "Two players start with 4 dice each", "rule": "R1", "players": 2, "rounds": 0,
   "expect": {"players": {"1": {"dice": 4, "eliminated": false}, "2": {"dice": 4, "eliminated": false}},
              "game": {"round_no": 0, "survivors": 2}}},
  {"name": "Three players start with 3 dice each", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"dice": 3}, "2": {"dice": 3}, "3": {"dice": 3}},
              "game": {"round_no": 0, "survivors": 3}}},
  {"name": "Four players start with 2 dice each", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"players": {"1": {"dice": 2}, "2": {"dice": 2}, "3": {"dice": 2}, "4": {"dice": 2}},
              "game": {"survivors": 4}}},
  {"name": "Each player rolls as many faces as dice (values are chance, only counts asserted)", "rule": "R2", "players": 3, "rounds": 0,
   "expect": {"lens": {"players": {"1": {"faces": 3}, "2": {"faces": 3}, "3": {"faces": 3}}}}},
  {"name": "Seat 1 opens and acts in round 1", "rule": "R3", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 4}],
   "expect": {"offered": [{"seat": 1, "option": "bid"}, {"seat": 1, "option": "dudo"}],
              "not_offered": [{"seat": 2, "option": "bid"}, {"seat": 3, "option": "bid"}, {"seat": 2, "option": "dudo"}, {"seat": 3, "option": "dudo"}],
              "game": {"round_no": 1},
              "players": {"1": {"dice": 3}, "2": {"dice": 3}, "3": {"dice": 3}}}},
  {"name": "Opening bid quantity ranges from max(1, floor(9/4)) = 2 to T = 9", "rule": "R4", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 6}],
   "expect": {"offered": [{"seat": 1, "option": "bid"}, {"seat": 1, "option": "dudo"}, {"seat": 1, "option": 2}, {"seat": 1, "option": 9}],
              "not_offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": 1}, {"seat": 1, "option": 10}],
              "players": {"1": {"dice": 3}, "2": {"dice": 3}, "3": {"dice": 3}}}},
  {"name": "Opener calling Dudo with no bid loses one die", "rule": "R5", "players": 3, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice": 2, "eliminated": false}, "2": {"dice": 3}, "3": {"dice": 3}},
              "game": {"round_no": 1, "survivors": 3}}},
  {"name": "With a bid of 7 and T = 9 the raise ranges from 8 to 9", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"game": {"current_qty": 7, "current_face": 4, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "rules": [{"seat": 2, "options_include": "raise"}, {"seat": 2, "options_include": 9}, {"seat": 2, "options_include": 5}],
   "expect": {"offered": [{"seat": 2, "option": "raise"}, {"seat": 2, "option": "dudo"}, {"seat": 2, "option": 8}, {"seat": 2, "option": 9}],
              "not_offered": [{"seat": 2, "option": "bid"}, {"seat": 2, "option": 7}, {"seat": 2, "option": 10}],
              "players": {"1": {"dice": 3}, "2": {"dice": 3}, "3": {"dice": 3}}}},
  {"name": "Bid equal to T forces Dudo; count 9 of 9 so the caller loses", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"faces": [1, 4, 4]}, "2": {"faces": [4, 4, 1]}, "3": {"faces": [4, 1, 4]}},
             "game": {"current_qty": 9, "current_face": 4, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "expect": {"offered": [{"seat": 2, "option": "dudo"}],
              "not_offered": [{"seat": 2, "option": "raise"}, {"seat": 2, "option": "bid"}],
              "players": {"1": {"dice": 3}, "2": {"dice": 2}, "3": {"dice": 3}}}},
  {"name": "After seat 1 bids, seat 2 acts next and may raise or call", "rule": "R8", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"faces": [4, 4, 2]}, "2": {"faces": [2, 3, 5]}, "3": {"faces": [1, 6, 6]}}},
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 4},
             {"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 2, "option": "raise"}],
              "not_offered": [{"seat": 2, "option": "bid"}, {"seat": 3, "option": "raise"}, {"seat": 3, "option": "dudo"}],
              "players": {"1": {"dice": 3}, "2": {"dice": 2}, "3": {"dice": 3}},
              "game": {"round_no": 2}}},
  {"name": "Ones are wild in the count: 4 fives bid, 2 fives + 2 ones, caller loses", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"faces": [5, 2, 3]}, "2": {"faces": [1, 2, 3]}, "3": {"faces": [1, 5, 6]}},
             "game": {"current_qty": 4, "current_face": 5, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice": 3}, "2": {"dice": 2}, "3": {"dice": 3}}}},
  {"name": "Count below the bid makes the bidder lose a die", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"faces": [5, 2, 3]}, "2": {"faces": [1, 2, 3]}, "3": {"faces": [1, 5, 6]}},
             "game": {"current_qty": 5, "current_face": 5, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice": 2}, "2": {"dice": 3}, "3": {"dice": 3}}}},
  {"name": "A player losing their last die is eliminated", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"dice": 3, "faces": [6, 6, 1]}, "2": {"dice": 1, "faces": [2]}, "3": {"dice": 3, "faces": [6, 3, 3]}},
             "game": {"current_qty": 4, "current_face": 6, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 7}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice": 3, "eliminated": false}, "2": {"dice": 0, "eliminated": true}, "3": {"dice": 3, "eliminated": false}},
              "game": {"survivors": 2}}},
  {"name": "The losing bidder opens the next hand", "rule": "R12", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"faces": [5, 2, 3]}, "2": {"faces": [1, 2, 3]}, "3": {"faces": [1, 5, 6]}},
             "game": {"current_qty": 5, "current_face": 5, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "rules": [{"seat": 2, "options_include": "dudo"}, {"seat": 1, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": "bid"}],
              "not_offered": [{"seat": 2, "option": "bid"}, {"seat": 3, "option": "bid"}, {"seat": 3, "option": "dudo"}],
              "players": {"1": {"dice": 1}, "2": {"dice": 3}, "3": {"dice": 3}},
              "game": {"round_no": 2}}},
  {"name": "An eliminated loser passes the opening to the next surviving seat", "rule": "R12", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"dice": 3, "faces": [6, 6, 1]}, "2": {"dice": 1, "faces": [2]}, "3": {"dice": 3, "faces": [6, 3, 3]}},
             "game": {"current_qty": 4, "current_face": 6, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 7}},
   "rules": [{"seat": 2, "options_include": "dudo"}, {"seat": 3, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 3, "option": "bid"}],
              "not_offered": [{"seat": 1, "option": "bid"}, {"seat": 1, "option": "dudo"}],
              "players": {"1": {"dice": 3}, "2": {"dice": 0, "eliminated": true}, "3": {"dice": 2}},
              "game": {"survivors": 2, "round_no": 2}}},
  {"name": "After a hand the bid is cleared, dice reroll and T drops to 8", "rule": "R13", "players": 3, "rounds": 2,
   "given": {"players": {"1": {"faces": [5, 2, 3]}, "2": {"faces": [1, 2, 3]}, "3": {"faces": [1, 5, 6]}},
             "game": {"current_qty": 5, "current_face": 5, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 9}},
   "rules": [{"seat": 2, "options_include": "dudo"},
             {"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 8}, {"seat": 1, "options_include": 3}],
   "expect": {"offered": [{"seat": 1, "option": "bid"}, {"seat": 1, "option": 2}, {"seat": 1, "option": 8}],
              "not_offered": [{"seat": 1, "option": "raise"}, {"seat": 1, "option": 9}],
              "lens": {"players": {"1": {"faces": 2}, "2": {"faces": 3}, "3": {"faces": 3}}},
              "players": {"1": {"dice": 2}, "2": {"dice": 3}, "3": {"dice": 3}}}},
  {"name": "Last player with dice wins at once", "rule": "R14", "players": 2,
   "given": {"players": {"1": {"dice": 2, "faces": [6, 1]}, "2": {"dice": 1, "faces": [3]}},
             "game": {"current_qty": 2, "current_face": 6, "current_bidder": 1, "to_act": 2, "opener": 1, "total_dice": 3}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"winner": 1, "standings": {"1": 2, "2": 0},
              "players": {"1": {"dice": 2, "eliminated": false}, "2": {"dice": 0, "eliminated": true}},
              "game": {"survivors": 1, "round_no": 1}}},
  {"name": "Round 40 ends the game; most dice wins", "rule": "R15", "players": 3,
   "given": {"players": {"1": {"dice": 3}, "2": {"dice": 2}, "3": {"dice": 2}},
             "game": {"round_no": 39, "total_dice": 7, "to_act": 1, "opener": 1}},
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": 3}],
   "expect": {"winner": 1, "standings": {"1": 3, "2": 2, "3": 2},
              "game": {"round_no": 40, "survivors": 3}}},
  {"name": "Round 40 ends with a tie for most dice; tied seats share the win", "rule": "R15", "players": 3,
   "given": {"players": {"1": {"dice": 3}, "2": {"dice": 3}, "3": {"dice": 2}},
             "game": {"round_no": 39, "total_dice": 8, "to_act": 1, "opener": 1}},
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": 3}],
   "expect": {"winner": [1, 2], "standings": {"1": 3, "2": 3, "3": 2},
              "game": {"round_no": 40}}},
  {"name": "Each turn keeps public dice counts and advances the round number", "rule": "R16", "players": 4, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "bid"}, {"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 5}],
   "expect": {"players": {"1": {"dice": 2}, "2": {"dice": 2}, "3": {"dice": 2}, "4": {"dice": 2}},
              "game": {"round_no": 1, "survivors": 4}}}
]
```
````
