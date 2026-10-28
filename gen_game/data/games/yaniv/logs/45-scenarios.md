# 45 scenarios

- time: 2026-10-28T06:53:16+00:00 (143.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 cde99063af2f8417, reply sha256 56a830884a8a8415

## Sent

````
SPEC:
{
  "name": "Row Yaniv",
  "summary": "A simultaneous-choice take on Yaniv: each round every player secretly chooses to call YANIV, draw blind or take from a public offer row, and sheds a card (with any matches). The lowest hand at showdown avoids penalty, and the lowest penalty total wins.",
  "players": {
    "min": 2,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 54,
    "joker_count": 2,
    "joker_value": 0,
    "copies_per_value_1_to_9": 4,
    "ten_value_cards": 16,
    "ten_value": 10,
    "slots_per_player": 3,
    "cards_dealt_per_player": 3,
    "initial_offer_row_length": 1,
    "max_rounds": 24,
    "yaniv_threshold": 10,
    "asaf_penalty": 20,
    "no_noncaller_n": 99,
    "end_penalty": 50,
    "initial_penalty": 0,
    "empty_slot_code": -1
  },
  "attributes": {
    "player": [
      {
        "key": "c1",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "Card value in slot 1 (0-10), or -1 if empty",
        "observable": false
      },
      {
        "key": "c2",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "Card value in slot 2 (0-10), or -1 if empty",
        "observable": false
      },
      {
        "key": "c3",
        "type": "number",
        "visible": "ally",
        "initial": -1,
        "meaning": "Card value in slot 3 (0-10), or -1 if empty",
        "observable": false
      },
      {
        "key": "hand_total",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "H: the sum of the non-empty slots",
        "observable": false
      },
      {
        "key": "card_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of non-empty slots",
        "observable": true
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Penalty total (the score; lower is better)",
        "observable": true
      },
      {
        "key": "action",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This round's action (YANIV, DRAW or TAKE) after invalid-YANIV and lost-TAKE conversions",
        "observable": false
      },
      {
        "key": "take_pos",
        "type": "number",
        "visible": "ally",
        "initial": 1,
        "meaning": "Chosen offer-row position, used only for TAKE",
        "observable": false
      },
      {
        "key": "shed_slot",
        "type": "number",
        "visible": "ally",
        "initial": 1,
        "meaning": "Effective shed slot (1-3), corrected to the lowest non-empty slot if the chosen one is empty",
        "observable": false
      },
      {
        "key": "is_caller",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Made a valid YANIV this round",
        "observable": false
      },
      {
        "key": "shed_values",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Card values shed this round, in slot order",
        "observable": false
      },
      {
        "key": "last_hand_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "H revealed at the most recent showdown",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Round number, 1 to 24",
        "observable": true
      },
      {
        "key": "priority_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that resolves first in TAKE and DRAW",
        "observable": false
      },
      {
        "key": "new_hand",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "When true, a fresh hand is shuffled and dealt at the start of the round",
        "observable": false
      },
      {
        "key": "draw_pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Card values in the draw pile; its order is hidden",
        "observable": false
      },
      {
        "key": "draw_pile_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the draw pile",
        "observable": true
      },
      {
        "key": "offer_row",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Ordered public offer row of card values",
        "observable": true
      },
      {
        "key": "dead_pile",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Every card that has left play this hand",
        "observable": true
      },
      {
        "key": "claimed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Offer-row positions already taken this round",
        "observable": false
      },
      {
        "key": "any_valid_yaniv",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "At least one valid YANIV was made this round",
        "observable": false
      },
      {
        "key": "showdown",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "A showdown happens this round",
        "observable": false
      },
      {
        "key": "min_caller_h",
        "type": "number",
        "visible": "public",
        "initial": 99,
        "meaning": "M: the lowest H among valid callers",
        "observable": false
      },
      {
        "key": "min_noncaller_h",
        "type": "number",
        "visible": "public",
        "initial": 99,
        "meaning": "N: the lowest H among non-callers (99 if everyone called)",
        "observable": false
      },
      {
        "key": "min_h",
        "type": "number",
        "visible": "public",
        "initial": 99,
        "meaning": "The lowest H overall, used when there is no valid caller",
        "observable": false
      },
      {
        "key": "max_penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest penalty total, kept beside the scores for the end check",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player's penalty is set to 0 and all slots c1, c2 and c3 are set to -1 (empty).",
    "round = 1, priority_seat = 1, new_hand = true, and offer_row and dead_pile are empty."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When new_hand is true: draw_pile is set to the full 54-card list [0,0, four each of 1-9, sixteen 10s]; all slots are set to -1; dead_pile is emptied; in seat order, each player draws 3 cards at random from draw_pile into c1, c2 and c3 (removed from draw_pile); one more random card from draw_pile becomes offer_row = [that card]; new_hand = false. Then hand_total, card_count and draw_pile_size are recomputed."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own c1, c2, c3 and hand_total."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce offer_row with positions and values, dead_pile, draw_pile_size, priority_seat and every player's card_count."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reset for the round: is_caller = false, shed_values = [], claimed = [], any_valid_yaniv = false, showdown = false."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of YANIV, DRAW, TAKE",
      "effect": "Stored privately in action; no answer is shown until all are in."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 1 to the length of offer_row",
      "effect": "Stored privately in take_pos (used only for TAKE)."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of 1, 2, 3",
      "effect": "Stored in shed_slot; if that slot is -1, shed_slot is set to the lowest-numbered non-empty slot."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "YANIV check: for each player with action = YANIV, if hand_total <= 10 then is_caller = true, otherwise action = DRAW and the YANIV is announced as invalid. any_valid_yaniv = (count of is_caller > 0)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "SHED, when any_valid_yaniv is false: each player appends the value in their shed slot to shed_values, then for each of their other slots, in slot order, holding that same value, appends it and sets that slot to -1. The shed slot is set to -1. Every player's shed_values is announced."
    },
    {
      "action": "update",
      "who": "each player in turn, starting at priority_seat and wrapping",
      "answer": null,
      "effect": "TAKE, when any_valid_yaniv is false: for each player with action = TAKE in that order, if take_pos is not in claimed, the shed slot is set to offer_row[take_pos], take_pos is appended to claimed, and the take is announced; otherwise action = DRAW."
    },
    {
      "action": "update",
      "who": "each player in turn, starting at priority_seat and wrapping",
      "answer": null,
      "effect": "DRAW, when any_valid_yaniv is false: for each player with action = DRAW in that order, one random card is removed from draw_pile and placed in the shed slot, told only to that player; draw_pile_size decreases by 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "ROW UPDATE, when any_valid_yaniv is false: offer_row cards at positions not in claimed are appended to dead_pile; offer_row = the concatenation of shed_values from seat 1 upward. hand_total and card_count are recomputed, and every card_count and draw_pile_size is announced."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their updated slots and hand_total."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "showdown = any_valid_yaniv OR draw_pile_size < number of players OR round = 24. When showdown is true: last_hand_total = hand_total for every player (all hands revealed); min_caller_h = the lowest hand_total among is_caller players (99 if none); min_noncaller_h = the lowest among the others (99 if none); min_h = the lowest hand_total overall."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "SCORING, when showdown is true. With any_valid_yaniv: a caller adds 0 if hand_total = min_caller_h and min_caller_h < min_noncaller_h, otherwise adds hand_total + 20; a non-caller adds 0 if hand_total <= min_caller_h, otherwise adds hand_total. Without any_valid_yaniv: a player adds 0 if hand_total = min_h, otherwise adds hand_total. Then max_penalty = the highest penalty, new_hand = true, and all hands and penalty totals are announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "priority_seat = (priority_seat mod number of players) + 1; round increases by 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if (showdown is true and max_penalty >= 50) or round > 24; otherwise continue."
    }
  ],
  "ending": {
    "condition": "(showdown == true and max_penalty >= 50) or round > 24",
    "rank_by": "0 - you.penalty",
    "decided_by": "Each player's standing is their penalty total; the lowest penalty wins, and players tied for the lowest share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a new hand starts, the draw pile is the 54 values (two 0s, four each of 1-9, sixteen 10s), each player receives 3 random cards into c1, c2 and c3, and 1 more card becomes the offer row, leaving 54 - 3*players - 1 cards in the draw pile."
    },
    {
      "id": "R2",
      "text": "When a new hand starts, the dead pile is emptied and the new-hand flag is switched off."
    },
    {
      "id": "R3",
      "text": "A player's hand total H is the sum of their non-empty slots (an empty slot counts as nothing)."
    },
    {
      "id": "R4",
      "text": "When a player calls YANIV with H <= 10, the call is valid; with H = 11 or more it is announced as invalid and the player is treated as DRAW."
    },
    {
      "id": "R5",
      "text": "When at least one valid YANIV is made, no card moves that round and a showdown follows."
    },
    {
      "id": "R6",
      "text": "When a player sheds, the card in their shed slot and every other slot of theirs with the same value are removed, so a pair sheds 2 cards and a triple sheds 3."
    },
    {
      "id": "R7",
      "text": "When the chosen shed slot is empty, the lowest-numbered non-empty slot is shed instead."
    },
    {
      "id": "R8",
      "text": "When two TAKE players choose the same position, the one earlier in seat order from the priority seat gets the card, and the other becomes DRAW."
    },
    {
      "id": "R9",
      "text": "A taken or drawn card is placed in the player's shed slot; extra slots emptied by a pair or triple stay empty for the rest of the hand."
    },
    {
      "id": "R10",
      "text": "A drawn card's value is told only to the drawing player, and the draw pile size drops by 1 per draw."
    },
    {
      "id": "R11",
      "text": "After the take step, untaken offer-row cards go to the dead pile, and the new offer row is all shed cards in seat order from seat 1, in slot order within each player."
    },
    {
      "id": "R12",
      "text": "A showdown happens when a valid YANIV was made, when the draw pile holds fewer cards than there are players after the row update, or in round 24."
    },
    {
      "id": "R13",
      "text": "With valid callers, a caller whose H equals M (the lowest caller H) scores 0 when M < N (the lowest non-caller H, or 99 if all called); otherwise the caller scores H + 20."
    },
    {
      "id": "R14",
      "text": "With valid callers, a non-caller scores 0 when their H <= M; otherwise they score H."
    },
    {
      "id": "R15",
      "text": "In a showdown with no valid caller, every player with the lowest H scores 0 and the others score their H."
    },
    {
      "id": "R16",
      "text": "After every showdown, scores are added to penalty totals, all hands are revealed, and the next round starts a fresh hand."
    },
    {
      "id": "R17",
      "text": "Every round the priority seat moves to the next seat, wrapping from the last seat to seat 1."
    },
    {
      "id": "R18",
      "text": "The match ends after a showdown that leaves some penalty total at 50 or more, or after round 24."
    },
    {
      "id": "R19",
      "text": "The player with the lowest penalty total wins, and players tied for the lowest share the win."
    }
  ],
  "offers": [
    {
      "question": "action",
      "who": "all players",
      "options": "YANIV, DRAW, TAKE (the offer row always holds at least one card)"
    },
    {
      "question": "take position",
      "who": "all players",
      "options": "a whole number from 1 to the current length of offer_row"
    },
    {
      "question": "shed slot",
      "who": "all players",
      "options": "1, 2, 3 (an empty slot is replaced by the lowest non-empty slot, as the rules allow)"
    }
  ],
  "choices": [
    {
      "what": "2 to 4 players, suggested 3",
      "why": "The designer suggested 3, which is kept. The minimum is 2 because two players still race to a low hand, contest the row and time YANIV against Asaf. The maximum is 4 because each hand uses 3 cards per player plus the row, and more seats make take collisions and draws so frequent that one player's choice matters little."
    },
    {
      "what": "Empty slots are coded as -1",
      "why": "A Joker is worth 0, so 0 cannot also mean empty."
    },
    {
      "what": "No talk phase",
      "why": "The rules say there is no discussion phase."
    },
    {
      "what": "Strategy exists",
      "why": "Thoughtful players track the dead pile and offer row to count cards, set up pairs to shed several cards at once, avoid contested row positions, and time YANIV to avoid being undercut (Asaf)."
    },
    {
      "what": "The end check uses max_penalty after a showdown",
      "why": "This keeps the 50-point condition arithmetic on a table attribute."
    }
  ],
  "simplifications": [
    {
      "what": "The three simultaneous answers are three consecutive polls",
      "why": "A question takes one answer. Answers are stored privately and never shown between polls, so the choices stay simultaneous."
    },
    {
      "what": "Shuffling and drawing from the top are modelled as random draws from the draw_pile list",
      "why": "Drawing at random from an unordered hidden list is equivalent to drawing the top card of a shuffled pile."
    },
    {
      "what": "Skipping steps 6-9 after a valid YANIV is done with a per-step condition (any_valid_yaniv is false)",
      "why": "The step list is flat, but single steps can carry arithmetic conditions."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: card_count, penalty, last_hand_total; table: round, draw_pile_size, offer_row, dead_pile.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Recount the draw pile in the R9 scenario. A TAKE player whose card is not claimed earlier does not draw, so with seat 1 TAKE / seat 2 DRAW in round 1 and both DRAW in round 2, three cards are drawn and draw_pile_size should be 7, not 6. Keep checking the R9 behaviour itself through public results: seat 1's card_count is 2 after the pair shed plus take and stays 2 after round 2's shed-and-draw, the offer row is [2, 7] and the dead pile is [6, 6, 1]. Do not add a draw for a successful TAKE.
````

## Reply

````
[
{"name":"R1 new hand deal: 3 players, all DRAW, the draw pile ends at 54-9-1-3 (chance cannot change these counts)","rule":"R1","players":3,"seed":1,"default":"first","rounds":1,
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"DRAW"}],
"expect":{"game":{"draw_pile_size":41},"lens":{"game":{"draw_pile":41,"dead_pile":1}}}},

{"name":"R2 new hand empties a leftover dead pile (only the untaken row card is dead after round 1)","rule":"R2","players":2,"seed":2,"default":"first","rounds":1,
"given":{"game":{"new_hand":true,"dead_pile":[5,5,3]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"lens":{"game":{"dead_pile":1}},"game":{"draw_pile_size":45}}},

{"name":"R2 new-hand flag switched off: no redeal in round 2, so the draw pile is 47-2-2 (chance-proof)","rule":"R2","players":2,"seed":3,"default":"first","rounds":2,
"rules":[{"seat":1,"options_include":"DRAW","times":"all"},{"seat":2,"options_include":"DRAW","times":"all"}],
"expect":{"game":{"draw_pile_size":43}}},

{"name":"R3 an empty slot counts as nothing in H (round 24 showdown)","rule":"R3","players":2,"seed":4,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":3,"c2":-1,"c3":4,"hand_total":7,"card_count":2},"2":{"c1":5,"c2":6,"c3":9,"hand_total":20,"card_count":3}},
"game":{"new_hand":false,"round":24,"priority_seat":1,"draw_pile":[7,7,7,7,7,7],"draw_pile_size":6,"offer_row":[8],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"last_hand_total":11,"card_count":2,"penalty":0},"2":{"last_hand_total":22,"card_count":3,"penalty":22}},
"game":{"draw_pile_size":4,"offer_row":[3,5],"dead_pile":[8]}}},

{"name":"R4 YANIV with H=11 is invalid and treated as DRAW","rule":"R4","players":2,"seed":5,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":2,"hand_total":11,"card_count":3},"2":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"card_count":3,"penalty":0,"last_hand_total":0},"2":{"card_count":3,"penalty":0}},
"game":{"draw_pile_size":8,"offer_row":[5,9],"dead_pile":[2]}}},

{"name":"R4 YANIV with H=10 is valid and leads to a showdown","rule":"R4","players":2,"seed":6,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":1,"hand_total":10,"card_count":3},"2":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"last_hand_total":10,"penalty":0},"2":{"last_hand_total":23,"penalty":23}},"game":{"draw_pile_size":10}}},

{"name":"R5 a valid YANIV stops all card movement, even another seat's TAKE","rule":"R5","players":2,"seed":7,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":1,"hand_total":10,"card_count":3},"2":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"TAKE"}],
"expect":{"players":{"1":{"card_count":3,"penalty":0,"last_hand_total":10},"2":{"card_count":3,"penalty":23,"last_hand_total":23}},
"game":{"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}}},

{"name":"R6 a pair sheds 2 cards and a triple sheds 3","rule":"R6","players":2,"seed":8,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":6,"c2":6,"c3":1,"hand_total":13,"card_count":3},"2":{"c1":4,"c2":4,"c3":4,"hand_total":12,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"card_count":2},"2":{"card_count":1}},
"game":{"draw_pile_size":8,"offer_row":[6,6,4,4,4],"dead_pile":[2]}}},

{"name":"R7 an empty chosen shed slot sheds the lowest non-empty slot instead","rule":"R7","players":2,"seed":9,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":-1,"c2":5,"c3":8,"hand_total":13,"card_count":2},"2":{"c1":9,"c2":8,"c3":3,"hand_total":20,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"card_count":2},"2":{"card_count":3}},
"game":{"draw_pile_size":8,"offer_row":[5,9],"dead_pile":[2]}}},

{"name":"R8 two TAKEs on the same position: the priority seat (2) gets it, seat 1 draws","rule":"R8","players":2,"seed":10,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3},"2":{"c1":10,"c2":8,"c3":5,"hand_total":23,"card_count":3}},
"game":{"new_hand":false,"round":24,"priority_seat":2,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[3,0],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"TAKE"},{"seat":2,"options_include":"TAKE"}],
"expect":{"players":{"1":{"last_hand_total":21,"penalty":21},"2":{"last_hand_total":16,"penalty":0}},
"game":{"draw_pile_size":9,"offer_row":[9,10],"dead_pile":[0]}}},

{"name":"R9 taken and drawn cards go into the shed slot; the slot emptied by a pair stays empty","rule":"R9","players":2,"seed":11,"default":"first","rounds":2,
"given":{"players":{"1":{"c1":6,"c2":6,"c3":2,"hand_total":14,"card_count":3},"2":{"c1":1,"c2":7,"c3":9,"hand_total":17,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[5,5,5,5,5,5,5,5,5,5],"draw_pile_size":10,"offer_row":[3],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"TAKE"},{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW","times":"all"}],
"expect":{"players":{"1":{"card_count":2},"2":{"card_count":3}},
"game":{"draw_pile_size":7,"offer_row":[3,5],"dead_pile":[6,6,1],"round":3}}},

{"name":"R10 the draw pile drops by 1 per draw and not for a TAKE","rule":"R10","players":3,"seed":12,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3},"2":{"c1":10,"c2":8,"c3":5,"hand_total":23,"card_count":3},"3":{"c1":7,"c2":3,"c3":2,"hand_total":12,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[4],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"TAKE"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"DRAW"}],
"expect":{"game":{"draw_pile_size":8,"offer_row":[9,10,7],"dead_pile":[]}}},

{"name":"R11 untaken row cards go dead and the new row is the shed cards from seat 1 up","rule":"R11","players":3,"seed":13,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":5,"c3":1,"hand_total":11,"card_count":3},"2":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3},"3":{"c1":7,"c2":3,"c3":2,"hand_total":12,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[4,0],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"TAKE"},{"seat":3,"options_include":2}],
"expect":{"players":{"1":{"card_count":2},"2":{"card_count":3},"3":{"card_count":3}},
"game":{"draw_pile_size":8,"offer_row":[5,5,9,7],"dead_pile":[4]}}},

{"name":"R12 showdown when the draw pile falls below the number of players","rule":"R12","players":2,"seed":14,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":9,"hand_total":18,"card_count":3},"2":{"c1":10,"c2":8,"c3":3,"hand_total":21,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7],"draw_pile_size":3,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"last_hand_total":20,"penalty":20},"2":{"last_hand_total":18,"penalty":0}},"game":{"draw_pile_size":1}}},

{"name":"R12 no showdown when the draw pile still holds as many cards as players","rule":"R12","players":2,"seed":15,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":9,"hand_total":18,"card_count":3},"2":{"c1":10,"c2":8,"c3":3,"hand_total":21,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7],"draw_pile_size":4,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"last_hand_total":0,"penalty":0},"2":{"last_hand_total":0,"penalty":0}},"game":{"draw_pile_size":2}}},

{"name":"R13 both call: the lowest caller scores 0 (N=99), the other caller scores H+20","rule":"R13","players":2,"seed":16,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":2,"c2":2,"c3":1,"hand_total":5,"card_count":3},"2":{"c1":3,"c2":4,"c3":1,"hand_total":8,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"YANIV"}],
"expect":{"players":{"1":{"penalty":0,"last_hand_total":5},"2":{"penalty":28,"last_hand_total":8}}}},

{"name":"R13 Asaf: a caller tied by a non-caller scores H+20","rule":"R13","players":2,"seed":17,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":3,"c2":3,"c3":1,"hand_total":7,"card_count":3},"2":{"c1":4,"c2":2,"c3":1,"hand_total":7,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"DRAW"}],
"expect":{"players":{"1":{"penalty":27,"last_hand_total":7},"2":{"penalty":0,"last_hand_total":7}}}},

{"name":"R14 non-callers score 0 at or below M and their H above it","rule":"R14","players":3,"seed":18,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":1,"c2":2,"c3":3,"hand_total":6,"card_count":3},"2":{"c1":1,"c2":1,"c3":2,"hand_total":4,"card_count":3},"3":{"c1":10,"c2":10,"c3":5,"hand_total":25,"card_count":3}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"DRAW"}],
"expect":{"players":{"1":{"penalty":26},"2":{"penalty":0},"3":{"penalty":25}}}},

{"name":"R15 showdown without a caller: everyone tied for the lowest H scores 0","rule":"R15","players":3,"seed":19,"default":"first","rounds":1,
"given":{"players":{"1":{"c1":5,"c2":2,"c3":9,"hand_total":16,"card_count":3},"2":{"c1":8,"c2":2,"c3":9,"hand_total":19,"card_count":3},"3":{"c1":6,"c2":10,"c3":10,"hand_total":26,"card_count":3}},
"game":{"new_hand":false,"round":24,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[1],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"},{"seat":3,"options_include":"DRAW"}],
"expect":{"players":{"1":{"penalty":0,"last_hand_total":18},"2":{"penalty":0,"last_hand_total":18},"3":{"penalty":27,"last_hand_total":27}},"game":{"draw_pile_size":7}}},

{"name":"R16 showdown scores add to the existing totals and the next round deals a fresh hand","rule":"R16","players":2,"seed":20,"default":"first","rounds":2,
"given":{"players":{"1":{"c1":5,"c2":4,"c3":1,"hand_total":10,"card_count":3,"penalty":10},"2":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3,"penalty":5}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW","times":"all"}],
"expect":{"players":{"1":{"penalty":10,"last_hand_total":10},"2":{"penalty":28,"last_hand_total":23}},
"game":{"draw_pile_size":45,"round":3},"lens":{"game":{"dead_pile":1}}}},

{"name":"R17 the priority seat moves from 1 to 2, so seat 2 wins round 24's TAKE collision","rule":"R17","players":2,"seed":21,"default":"first","rounds":2,
"given":{"players":{"1":{"c1":9,"c2":8,"c3":6,"hand_total":23,"card_count":3},"2":{"c1":10,"c2":8,"c3":5,"hand_total":23,"card_count":3}},
"game":{"new_hand":false,"round":23,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[4],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":1,"options_include":"TAKE"},{"seat":2,"options_include":"DRAW"},{"seat":2,"options_include":"TAKE"}],
"expect":{"players":{"1":{"last_hand_total":21,"penalty":0},"2":{"last_hand_total":22,"penalty":22}},
"game":{"draw_pile_size":7,"offer_row":[7,7],"dead_pile":[4,10]}}},

{"name":"R18 the match ends after a showdown that pushes a penalty to 50 or more","rule":"R18","players":2,"seed":22,"default":"first",
"given":{"players":{"1":{"c1":5,"c2":6,"c3":4,"hand_total":15,"card_count":3,"penalty":40},"2":{"c1":1,"c2":2,"c3":0,"hand_total":3,"card_count":3,"penalty":0}},
"game":{"new_hand":false,"round":1,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"YANIV"}],
"expect":{"winner":2,"standings":{"1":-55,"2":0},"players":{"1":{"penalty":55},"2":{"penalty":0}},"game":{"round":2}}},

{"name":"R18 the match ends after round 24 even with every penalty below 50","rule":"R18","players":2,"seed":23,"default":"first",
"given":{"players":{"1":{"c1":1,"c2":2,"c3":3,"hand_total":6,"card_count":3},"2":{"c1":5,"c2":5,"c3":9,"hand_total":19,"card_count":3}},
"game":{"new_hand":false,"round":24,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"DRAW"},{"seat":2,"options_include":"DRAW"}],
"expect":{"winner":1,"standings":{"1":0,"2":-16},"players":{"1":{"penalty":0,"last_hand_total":12,"card_count":3},"2":{"penalty":16,"last_hand_total":16,"card_count":2}},"game":{"round":25}}},

{"name":"R19 players tied for the lowest penalty share the win","rule":"R19","players":2,"seed":24,"default":"first",
"given":{"players":{"1":{"c1":1,"c2":1,"c3":2,"hand_total":4,"card_count":3,"penalty":30},"2":{"c1":5,"c2":3,"c3":2,"hand_total":10,"card_count":3,"penalty":20}},
"game":{"new_hand":false,"round":24,"priority_seat":1,"draw_pile":[7,7,7,7,7,7,7,7,7,7],"draw_pile_size":10,"offer_row":[2],"dead_pile":[]}},
"rules":[{"seat":1,"options_include":"YANIV"},{"seat":2,"options_include":"DRAW"}],
"expect":{"winner":[1,2],"standings":{"1":-30,"2":-30},"players":{"1":{"penalty":30},"2":{"penalty":30}}}}
]
````
