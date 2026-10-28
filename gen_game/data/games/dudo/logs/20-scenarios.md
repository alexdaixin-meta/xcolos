# 20 scenarios

- time: 2026-10-28T05:44:59+00:00 (36.9s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e4c60a56168fc929, reply sha256 4c308d4ae4f4dce6

## Sent

````
SPEC:
{
  "name": "Short Dudo",
  "summary": "A short bluffing dice game. Players bid on how many dice around the table show a face, with 1s wild. The next players raise, call Dudo (false) or call Calza (exact), and the loser of each call loses a die.",
  "players": {
    "min": 2,
    "max": 4,
    "suggested": 3
  },
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
      {
        "key": "dice_count",
        "type": "number",
        "visible": "public",
        "initial": 5,
        "meaning": "How many dice this player holds. This is the score.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "This round's die faces (1-6) for this player, seen only by the owner until the reveal.",
        "observable": false
      },
      {
        "key": "out",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the player has 0 dice. An out player is skipped in seat order.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round_num",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rounds started so far.",
        "observable": true
      },
      {
        "key": "opener_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that opens the bidding this round.",
        "observable": false
      },
      {
        "key": "total_dice",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "T: total dice held by players still in the game.",
        "observable": false
      },
      {
        "key": "current_face",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Face (2-6) of the standing bid.",
        "observable": false
      },
      {
        "key": "current_qty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Quantity of the standing bid.",
        "observable": false
      },
      {
        "key": "current_bidder",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that made the standing bid.",
        "observable": false
      },
      {
        "key": "responder_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat due to respond next: the next seat after current_bidder that is not out.",
        "observable": false
      },
      {
        "key": "call_type",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Empty while bidding continues, otherwise 'dudo' or 'calza'.",
        "observable": false
      },
      {
        "key": "caller_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that called Dudo or Calza.",
        "observable": false
      },
      {
        "key": "reveal_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "N: dice in all hands showing current_face plus dice showing 1.",
        "observable": false
      },
      {
        "key": "loser_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that lost a die this round, or 0 if none did.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are numbered 1 to the player count in a fixed order.",
    "Each player's dice_count is set to 5, hand is set empty and out is set false.",
    "opener_seat is set to 1 and round_num to 0.",
    "There is no random draw before play."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_num += 1. call_type = '', caller_seat = 0 and loser_seat = 0. total_dice = sum of dice_count over players with out = false."
    },
    {
      "action": "initialize",
      "who": "all players",
      "answer": null,
      "effect": "In one deal, every player with out = false gets hand set to dice_count random faces from 1 to 6. Out players keep an empty hand."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand, total_dice and every player's dice_count and out."
    },
    {
      "action": "ask",
      "who": "seat opener_seat",
      "answer": "a face from 2 to 6",
      "effect": "current_face = the chosen face. current_bidder = opener_seat."
    },
    {
      "action": "ask",
      "who": "seat opener_seat",
      "answer": "a whole number from max(1, floor(total_dice/3)) to ceil(total_dice/2)",
      "effect": "current_qty = the number. The bid is announced to all. responder_seat = the next seat after current_bidder with out = false."
    },
    {
      "action": "ask",
      "who": "seat responder_seat (response 1)",
      "answer": "one of raise1_faceF (F = 2..6, offered only if current_qty+1 <= total_dice), raise2_faceF (F = 2..6, offered only if current_qty+2 <= total_dice), dudo, calza",
      "effect": "On raiseK_faceF: current_qty += K, current_face = F, current_bidder = responder_seat, then responder_seat = the next seat after current_bidder with out = false. On dudo or calza: call_type = the choice, caller_seat = responder_seat. The choice is announced to all."
    },
    {
      "action": "ask",
      "who": "seat responder_seat (response 2), when call_type = ''",
      "answer": "the same options as response 1, with the same legality limits",
      "effect": "The same as response 1. With 2 players this seat is the opener."
    },
    {
      "action": "ask",
      "who": "seat responder_seat (final response), when call_type = ''",
      "answer": "dudo or calza",
      "effect": "call_type = the choice, caller_seat = responder_seat. The choice is announced to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reveal: every hand is shown to all. reveal_count = count over all hands of dice equal to current_face or equal to 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Settle. If call_type = 'dudo' and reveal_count >= current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. If call_type = 'dudo' and reveal_count < current_qty: current_bidder dice_count -= 1, loser_seat = current_bidder. If call_type = 'calza' and reveal_count = current_qty: caller_seat dice_count = min(dice_count + 1, 5), loser_seat = 0. If call_type = 'calza' and reveal_count != current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. The result is announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Elimination: any player with dice_count = 0 gets out = true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Next opener. If loser_seat > 0, opener_seat = loser_seat; otherwise (a successful Calza) opener_seat = caller_seat. If that seat has out = true, opener_seat = the next seat after it with out = false."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if the number of players with out = false is 1, or if round_num >= 30. Otherwise start a new round."
    }
  ],
  "ending": {
    "condition": "count of players with out = false == 1 OR round_num >= 30",
    "rank_by": "you.dice_count",
    "decided_by": "Each player's standing is the dice they hold. A lone survivor holds the only dice and wins. After 30 rounds the player with the most dice wins, and players tied for the most share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup every player has dice_count 5 and out false, and seat 1 opens round 1."
    },
    {
      "id": "R2",
      "text": "Each round, every player not out gets a fresh hand of exactly dice_count random faces from 1 to 6, visible only to the owner."
    },
    {
      "id": "R3",
      "text": "total_dice equals the sum of dice_count over players not out, and it is told to everyone with every dice_count."
    },
    {
      "id": "R4",
      "text": "The opener bids a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). For example, with T = 15, Q is from 5 to 8."
    },
    {
      "id": "R5",
      "text": "When a responder chooses Raise +1, current_qty increases by 1, current_face becomes their chosen face from 2 to 6, and they become current_bidder."
    },
    {
      "id": "R6",
      "text": "When a responder chooses Raise +2, current_qty increases by 2, current_face becomes their chosen face from 2 to 6, and they become current_bidder."
    },
    {
      "id": "R7",
      "text": "When a raise would make current_qty exceed total_dice, that raise is not offered. If both raises exceed it, only Dudo and Calza are offered."
    },
    {
      "id": "R8",
      "text": "The responder is always the next seat in order after the current bidder that is not out. With 2 players, response 2 is answered by the opener."
    },
    {
      "id": "R9",
      "text": "Response 2 happens only when response 1 was a raise, and the final response happens only when response 2 was a raise."
    },
    {
      "id": "R10",
      "text": "The final responder may choose only Dudo or Calza."
    },
    {
      "id": "R11",
      "text": "At reveal, N counts every die in all hands that shows current_face or shows 1."
    },
    {
      "id": "R12",
      "text": "When Dudo is called and N >= current_qty, the caller loses 1 die."
    },
    {
      "id": "R13",
      "text": "When Dudo is called and N < current_qty, the current bidder loses 1 die."
    },
    {
      "id": "R14",
      "text": "When Calza is called and N == current_qty, the caller gains 1 die, but never above 5."
    },
    {
      "id": "R15",
      "text": "When Calza is called and N != current_qty, the caller loses 1 die."
    },
    {
      "id": "R16",
      "text": "When a player's dice_count reaches 0, out becomes true, and the player is skipped in seat order and gets no hand from then on."
    },
    {
      "id": "R17",
      "text": "The player who lost a die opens the next round. After a successful Calza the caller opens. If that player is out, the next seat in order that is not out opens."
    },
    {
      "id": "R18",
      "text": "When only one player is not out, the game ends and that player wins."
    },
    {
      "id": "R19",
      "text": "When 30 rounds have been played, the game ends and the highest dice_count wins. Players tied at the top share the result as a draw."
    }
  ],
  "offers": [
    {
      "question": "Opening face",
      "who": "the opener",
      "options": "faces 2, 3, 4, 5, 6"
    },
    {
      "question": "Opening quantity",
      "who": "the opener",
      "options": "whole numbers from max(1, floor(total_dice/3)) to ceil(total_dice/2)"
    },
    {
      "question": "Response 1 and response 2",
      "who": "the next seat after the current bidder that is not out",
      "options": "If current_qty + 2 <= total_dice: raise1_face2..raise1_face6, raise2_face2..raise2_face6, dudo, calza. If only current_qty + 1 <= total_dice: raise1_face2..raise1_face6, dudo, calza. If current_qty + 1 > total_dice: dudo, calza."
    },
    {
      "question": "Final response",
      "who": "the next seat after the current bidder that is not out",
      "options": "dudo, calza"
    }
  ],
  "choices": [
    {
      "what": "2 to 4 players, suggested 3",
      "why": "The designer suggests 3. Two is the smallest table where a bid can be doubted. Above 4 the 3-response limit means most seats never act in a round."
    },
    {
      "what": "No talk phase",
      "why": "The source says bids and calls are the only communication. Bluffing happens through the bids themselves."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player estimates the expected count from their own hand plus T/3 for the unseen dice, bluffs bids toward faces they hold, reads the raises of others, and saves Calza for when they hold the bid face, since a correct Calza gains a die."
    }
  ],
  "simplifications": [
    {
      "what": "The opening bid is asked as two questions to the same seat, face then quantity",
      "why": "One answer is either a choice or a number, never both."
    },
    {
      "what": "A raise and its face are offered as one combined choice, such as raise2_face4",
      "why": "This lets one choice question carry the raise size and the face, with illegal raises left out."
    },
    {
      "what": "A tie for most dice after 30 rounds is a shared top result rather than a separate 'draw' outcome",
      "why": "The engine has no separate draw. Players level at the top share the win, which records the draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: dice_count, out; table: round_num.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup: every seat holds 5 dice, none is out, no round started", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"dice_count": 5, "out": false}, "2": {"dice_count": 5, "out": false}, "3": {"dice_count": 5, "out": false}},
              "game": {"round_num": 0}}},

  {"name": "Seat 1 opens round 1 and is the only seat asked for an opening quantity", "rule": "R1", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"3": {"dice_count": 5, "out": false}}, "game": {"round_num": 1},
              "offered": [{"seat": 1, "option": 5}, {"seat": 1, "option": 8}],
              "not_offered": [{"seat": 2, "option": 5}, {"seat": 3, "option": 5}]}},

  {"name": "Each seat that is still in is dealt exactly dice_count dice; an out seat gets none", "rule": "R2", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 3}, "2": {"dice_count": 2}, "3": {"dice_count": 0, "out": true}}, "status": {"3": "out"}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"lens": {"players": {"1": {"hand": 3}, "2": {"hand": 2}, "3": {"hand": 0}}}}},

  {"name": "Total dice 4+3+2=9 gives an opening quantity range of 3 to 5", "rule": "R3", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 4}, "2": {"dice_count": 3}, "3": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 3}, {"seat": 1, "option": 5}],
              "not_offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 6}]}},

  {"name": "An out seat adds nothing to the total: T=8 gives an opening range of 2 to 4", "rule": "R3", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 4}, "2": {"dice_count": 4}, "3": {"dice_count": 0, "out": true}}, "status": {"3": "out"}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 4}],
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 5}]}},

  {"name": "With T=15 the opening quantity runs from 5 to 8", "rule": "R4", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 5}, {"seat": 1, "option": 8}],
              "not_offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 9}]}},

  {"name": "With T=2 the opening quantity is floored at 1, so only 1 is allowed", "rule": "R4", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 1}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 1}], "not_offered": [{"seat": 1, "option": 2}]}},

  {"name": "Raise +1 from 2 to 3 with T=4: the next responder may raise by 1 but not by 2", "rule": "R5", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "raise1_face3"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}], "not_offered": [{"seat": 1, "option": "raise2_face2"}]}},

  {"name": "Raise +2 from 3 to 5 with T=6: the next responder may raise by 1 but not by 2", "rule": "R6", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 3}, "2": {"dice_count": 3}}},
   "rules": [{"seat": 2, "options_include": "raise2_face4"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}], "not_offered": [{"seat": 1, "option": "raise2_face2"}]}},

  {"name": "When the bid already equals the total dice, only dudo and calza are offered", "rule": "R7", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "raise2_face5"}],
   "expect": {"offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}],
              "not_offered": [{"seat": 1, "option": "raise1_face6"}, {"seat": 1, "option": "raise2_face6"}]}},

  {"name": "With a bid of 2 and T=3, raise +1 is offered but raise +2 is not", "rule": "R7", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 2, "option": "raise1_face4"}], "not_offered": [{"seat": 2, "option": "raise2_face4"}]}},

  {"name": "The responder skips an out seat: seat 3 answers seat 1's bid", "rule": "R8", "players": 4, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 0, "out": true}}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"2": {"dice_count": 0, "out": true}, "4": {"dice_count": 5}},
              "offered": [{"seat": 3, "option": "dudo"}],
              "not_offered": [{"seat": 2, "option": "dudo"}, {"seat": 4, "option": "dudo"}]}},

  {"name": "With 2 players the opener answers response 2", "rule": "R8", "players": 2, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}, {"seat": 1, "option": "calza"}]}},

  {"name": "A call at response 1 ends the bidding: there is no response 2", "rule": "R9", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"not_offered": [{"seat": 3, "option": "dudo"}, {"seat": 3, "option": "calza"}, {"seat": 1, "option": "dudo"}]}},

  {"name": "A call at response 2 ends the bidding: there is no final response", "rule": "R9", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "dudo"}],
   "expect": {"not_offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}]}},

  {"name": "The final responder is offered only dudo and calza, even with room to raise", "rule": "R10", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "raise1_face4"}],
   "expect": {"offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}],
              "not_offered": [{"seat": 1, "option": "raise1_face5"}, {"seat": 1, "option": "raise2_face5"}]}},

  {"name": "A reveal and settlement between seats 1 and 2 leaves seat 3 untouched (the counted dice are random)", "rule": "R11", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"3": {"dice_count": 5, "out": false}}, "game": {"round_num": 1}}},

  {"name": "Dudo by seat 3 on seat 2's raise costs a die only to seat 3 or seat 2, so seat 1 keeps 5 (which of them loses is random)", "rule": "R12", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice_count": 5, "out": false}}}},

  {"name": "Dudo by seat 2 on seat 1's bid costs a die only to seat 2 or seat 1, so seats 3 and 4 keep 5 (which of them loses is random)", "rule": "R13", "players": 4, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"3": {"dice_count": 5}, "4": {"dice_count": 5}}}},

  {"name": "Calza changes only the caller's dice: the bidder and seat 3 keep 5 (the result is random)", "rule": "R14", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "calza"}],
   "expect": {"players": {"1": {"dice_count": 5}, "3": {"dice_count": 5}}}},

  {"name": "Calza by seat 3 on seat 2's raise changes only seat 3's dice: seats 1 and 2 keep theirs (the result is random)", "rule": "R15", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 3}}},
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "calza"}],
   "expect": {"players": {"1": {"dice_count": 5}, "2": {"dice_count": 3}}}},

  {"name": "An out seat is skipped, gets no hand and stays out", "rule": "R16", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 0, "out": true}}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"2": {"dice_count": 0, "out": true}},
              "lens": {"players": {"2": {"hand": 0}}},
              "not_offered": [{"seat": 2, "option": "dudo"}, {"seat": 2, "option": "calza"}]}},

  {"name": "After a calza, won or lost, the caller (seat 2) opens the next round and seat 3 does not", "rule": "R17", "players": 3, "rounds": 2, "default": "first",
   "rules": [{"seat": 2, "options_include": "calza"}],
   "expect": {"game": {"round_num": 2},
              "offered": [{"seat": 2, "option": 5}],
              "not_offered": [{"seat": 3, "option": 5}]}},

  {"name": "Two seats with 1 die each: the dudo knocks one out and the game ends after round 1 (the winner is random)", "rule": "R18", "players": 2, "rounds": 2, "default": "last",
   "given": {"players": {"1": {"dice_count": 1}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"game": {"round_num": 1}}},

  {"name": "Round 30 ends the game and the seat holding the most dice wins", "rule": "R19", "players": 3, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}, "3": {"dice_count": 5}}, "game": {"round_num": 29}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"winner": 3, "standings": {"3": 5}, "players": {"3": {"dice_count": 5}}, "game": {"round_num": 30}}},

  {"name": "Round 30 ends the game and seats tied for the most dice share the win", "rule": "R19", "players": 4, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}, "3": {"dice_count": 5}, "4": {"dice_count": 5}}, "game": {"round_num": 29}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"winner": [3, 4], "standings": {"3": 5, "4": 5}, "game": {"round_num": 30}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Seat 1 opens round 1 and is the only seat asked for an opening quantity; no seat is out after the first call", "rule": "R1", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"1": {"out": false}, "2": {"out": false}, "3": {"dice_count": 5, "out": false}}, "game": {"round_num": 1},
              "offered": [{"seat": 1, "option": 5}, {"seat": 1, "option": 8}],
              "not_offered": [{"seat": 2, "option": 5}, {"seat": 3, "option": 5}]}},

  {"name": "Each seat that is still in is dealt exactly dice_count dice; an out seat gets none", "rule": "R2", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 3}, "2": {"dice_count": 2}, "3": {"dice_count": 0, "out": true}}, "status": {"3": "out"}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"lens": {"players": {"1": {"hand": 3}, "2": {"hand": 2}, "3": {"hand": 0}}}}},

  {"name": "Total dice 4+3+2=9 gives an opening quantity range of 3 to 5", "rule": "R3", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 4}, "2": {"dice_count": 3}, "3": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 3}, {"seat": 1, "option": 5}],
              "not_offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 6}]}},

  {"name": "An out seat adds nothing to the total: T=8 gives an opening range of 2 to 4", "rule": "R3", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 4}, "2": {"dice_count": 4}, "3": {"dice_count": 0, "out": true}}, "status": {"3": "out"}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 4}],
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 5}]}},

  {"name": "With T=15 the opening quantity runs from 5 to 8", "rule": "R4", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 5}, {"seat": 1, "option": 8}],
              "not_offered": [{"seat": 1, "option": 4}, {"seat": 1, "option": 9}]}},

  {"name": "With T=2 the opening quantity is floored at 1, so only 1 is allowed", "rule": "R4", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 1}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 1, "option": 1}], "not_offered": [{"seat": 1, "option": 2}]}},

  {"name": "Raise +1 from 2 to 3 with T=4: the next responder may raise by 1 but not by 2", "rule": "R5", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "raise1_face3"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}], "not_offered": [{"seat": 1, "option": "raise2_face2"}]}},

  {"name": "Raise +2 from 3 to 5 with T=6: the next responder may raise by 1 but not by 2", "rule": "R6", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 3}, "2": {"dice_count": 3}}},
   "rules": [{"seat": 2, "options_include": "raise2_face4"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}], "not_offered": [{"seat": 1, "option": "raise2_face2"}]}},

  {"name": "When the bid already equals the total dice, only dudo and calza are offered", "rule": "R7", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}}},
   "rules": [{"seat": 2, "options_include": "raise2_face5"}],
   "expect": {"offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}],
              "not_offered": [{"seat": 1, "option": "raise1_face6"}, {"seat": 1, "option": "raise2_face6"}]}},

  {"name": "With a bid of 2 and T=3, raise +1 is offered but raise +2 is not", "rule": "R7", "players": 2, "rounds": 1, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"offered": [{"seat": 2, "option": "raise1_face4"}], "not_offered": [{"seat": 2, "option": "raise2_face4"}]}},

  {"name": "The responder skips an out seat: seat 3 answers seat 1's bid", "rule": "R8", "players": 4, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 0, "out": true}}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"2": {"dice_count": 0, "out": true}, "4": {"dice_count": 5}},
              "offered": [{"seat": 3, "option": "dudo"}],
              "not_offered": [{"seat": 2, "option": "dudo"}, {"seat": 4, "option": "dudo"}]}},

  {"name": "With 2 players the opener answers response 2", "rule": "R8", "players": 2, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}],
   "expect": {"offered": [{"seat": 1, "option": "raise1_face2"}, {"seat": 1, "option": "calza"}]}},

  {"name": "A call at response 1 ends the bidding: there is no response 2", "rule": "R9", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"not_offered": [{"seat": 3, "option": "dudo"}, {"seat": 3, "option": "calza"}, {"seat": 1, "option": "dudo"}]}},

  {"name": "A call at response 2 ends the bidding: there is no final response", "rule": "R9", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "dudo"}],
   "expect": {"not_offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}]}},

  {"name": "The final responder is offered only dudo and calza, even with room to raise", "rule": "R10", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "raise1_face4"}],
   "expect": {"offered": [{"seat": 1, "option": "dudo"}, {"seat": 1, "option": "calza"}],
              "not_offered": [{"seat": 1, "option": "raise1_face5"}, {"seat": 1, "option": "raise2_face5"}]}},

  {"name": "A reveal and settlement between seats 1 and 2 leaves seat 3 untouched (the counted dice are random)", "rule": "R11", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"3": {"dice_count": 5, "out": false}}, "game": {"round_num": 1}}},

  {"name": "Dudo by seat 3 on seat 2's raise costs a die only to seat 3 or seat 2, so seat 1 keeps 5 (which of them loses is random)", "rule": "R12", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"1": {"dice_count": 5, "out": false}}}},

  {"name": "Dudo by seat 2 on seat 1's bid costs a die only to seat 2 or seat 1, so seats 3 and 4 keep 5 (which of them loses is random)", "rule": "R13", "players": 4, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"players": {"3": {"dice_count": 5}, "4": {"dice_count": 5}}}},

  {"name": "Calza changes only the caller's dice: the bidder and seat 3 keep 5 (the result is random)", "rule": "R14", "players": 3, "rounds": 1, "default": "last",
   "rules": [{"seat": 2, "options_include": "calza"}],
   "expect": {"players": {"1": {"dice_count": 5}, "3": {"dice_count": 5}}}},

  {"name": "Calza by seat 3 on seat 2's raise changes only seat 3's dice: seats 1 and 2 keep theirs (the result is random)", "rule": "R15", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 3}}},
   "rules": [{"seat": 2, "options_include": "raise1_face3"}, {"seat": 3, "options_include": "calza"}],
   "expect": {"players": {"1": {"dice_count": 5}, "2": {"dice_count": 3}}}},

  {"name": "An out seat is skipped, gets no hand and stays out", "rule": "R16", "players": 3, "rounds": 1, "default": "last",
   "given": {"players": {"2": {"dice_count": 0, "out": true}}, "status": {"2": "out"}},
   "rules": [{"seat": 3, "options_include": "dudo"}],
   "expect": {"players": {"2": {"dice_count": 0, "out": true}},
              "lens": {"players": {"2": {"hand": 0}}},
              "not_offered": [{"seat": 2, "option": "dudo"}, {"seat": 2, "option": "calza"}]}},

  {"name": "After a calza, won or lost, the caller (seat 2) opens the next round and seat 3 does not", "rule": "R17", "players": 3, "rounds": 2, "default": "first",
   "rules": [{"seat": 2, "options_include": "calza"}],
   "expect": {"game": {"round_num": 2},
              "offered": [{"seat": 2, "option": 5}],
              "not_offered": [{"seat": 3, "option": 5}]}},

  {"name": "Two seats with 1 die each: the dudo knocks one out and the game ends after round 1 (the winner is random)", "rule": "R18", "players": 2, "rounds": 2, "default": "last",
   "given": {"players": {"1": {"dice_count": 1}, "2": {"dice_count": 1}}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"game": {"round_num": 1}}},

  {"name": "Round 30 ends the game and the seat holding the most dice wins", "rule": "R19", "players": 3, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}, "3": {"dice_count": 5}}, "game": {"round_num": 29}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"winner": 3, "standings": {"3": 5}, "players": {"3": {"dice_count": 5}}, "game": {"round_num": 30}}},

  {"name": "Round 30 ends the game and seats tied for the most dice share the win", "rule": "R19", "players": 4, "default": "last",
   "given": {"players": {"1": {"dice_count": 2}, "2": {"dice_count": 2}, "3": {"dice_count": 5}, "4": {"dice_count": 5}}, "game": {"round_num": 29}},
   "rules": [{"seat": 2, "options_include": "dudo"}],
   "expect": {"winner": [3, 4], "standings": {"3": 5, "4": 5}, "game": {"round_num": 30}}}
]
```
````
