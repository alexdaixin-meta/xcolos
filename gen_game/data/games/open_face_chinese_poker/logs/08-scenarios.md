# 08 scenarios

- time: 2026-10-28T01:38:52+00:00 (175.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 040212c5136848dd, reply sha256 1fbde5e479dc56bd

## Sent

````
SPEC:
{
  "name": "Duplicate Open-Face Pairs",
  "summary": "Two players build 1-2-2 card rows from mirrored deals over 4 hands. Rows must not foul. Players score row wins, scoops and royalties, and both players face the same cards in each pair of hands.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 32,
    "card_value_min": 1,
    "card_value_max": 8,
    "copies_per_value": 4,
    "hands": 4,
    "rounds_per_hand": 5,
    "total_rounds": 20,
    "cards_per_seat_per_round": 3,
    "cards_kept_per_round": 1,
    "cards_discarded_per_round": 2,
    "cards_used_per_hand": 30,
    "unused_positions": 2,
    "front_slots": 1,
    "middle_slots": 2,
    "back_slots": 2,
    "front_multiplier": 2,
    "pair_bonus": 100,
    "row_win_points": 1,
    "scoop_bonus": 3,
    "foul_win_points": 6,
    "front_royalty_min_value": 7,
    "front_royalty": 1,
    "middle_pair_royalty": 2,
    "back_pair_royalty": 1
  },
  "attributes": {
    "player": [
      {
        "key": "front",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card in the Front slot (0 = empty). At scoring it becomes the Front strength, 2 x value.",
        "observable": true
      },
      {
        "key": "mid1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "First Middle card (0 = empty). At scoring it becomes the Middle strength.",
        "observable": true
      },
      {
        "key": "mid2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Second Middle card (0 = empty).",
        "observable": true
      },
      {
        "key": "back1",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "First Back card (0 = empty). At scoring it becomes the Back strength.",
        "observable": true
      },
      {
        "key": "back2",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Second Back card (0 = empty).",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 3 cards dealt to this player this round. The unkept cards are discarded from here unseen.",
        "observable": false
      },
      {
        "key": "chosen_card",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The card kept this round.",
        "observable": false
      },
      {
        "key": "chosen_row",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The row named this round: Front, Middle or Back.",
        "observable": false
      },
      {
        "key": "fouled",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this player's rows fouled in the hand just scored.",
        "observable": true
      },
      {
        "key": "royalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Royalties earned in the hand just scored (0 if fouled).",
        "observable": false
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points scored in the hand just scored.",
        "observable": true
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match total: the sum of hand scores.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          3,
          3,
          3,
          3,
          4,
          4,
          4,
          4,
          5,
          5,
          5,
          5,
          6,
          6,
          6,
          6,
          7,
          7,
          7,
          7,
          8,
          8,
          8,
          8
        ],
        "meaning": "The 32-card deck in its fixed shuffled order. Dealing rotates cards from the front to the back, so the order survives for the mirrored hand.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, 1 to 4. Above 4 means the match is over.",
        "observable": true
      },
      {
        "key": "round_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round within the hand, 1 to 5.",
        "observable": true
      },
      {
        "key": "seat_strengths",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "meaning": "Table copy of each player's strengths for comparison: [A front, A middle, A back, A fouled, B front, B middle, B back, B fouled].",
        "observable": false
      }
    ]
  },
  "setup": [
    "Player A sits in seat 1 and Player B in seat 2.",
    "Each player's front, mid1, mid2, back1 and back2 are set to 0, and total is set to 0.",
    "The deck list holds 32 cards: values 1 to 8, four of each.",
    "hand_number is set to 1 and round_in_hand to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round_in_hand == 1 and hand_number is 1 or 3: shuffle deck into a new random fixed order.",
      "when": "round_in_hand == 1 and (hand_number == 1 or hand_number == 3)"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal by position. Take the first 3 cards of deck, append them to the back of deck, and copy them into the Seat X player's hand. Then take the next 3 cards the same way into the Seat Y player's hand. Seat X is Player A when hand_number is odd and Player B when it is even; Seat Y is the other player."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand, all placed rows, hand_number and round_in_hand."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of the 3 card values in your hand",
      "effect": "chosen_card = the chosen value. Nobody sees the other's answer."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "Front, Middle or Back",
      "effect": "chosen_row = the named row. Nobody sees the other's answer."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Place chosen_card in the first empty slot of chosen_row: front, else mid1 then mid2, else back1 then back2. If that row is full, place it in the first non-full row in the order Back, Middle, Front. Then empty hand: the 2 unkept cards are discarded unseen."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce both kept cards face up and the row each went to."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "round_in_hand == 5",
      "effect": "Score the hand. front = 2*front. mid1 = mid1+mid2+100*(mid1==mid2), using the old values. back1 = back1+back2+100*(back1==back2), using the old values. fouled = (front > mid1) or (mid1 > back1). Copy front, mid1, back1 and fouled into seat_strengths. royalty = 0 if fouled, else (old front >= 7)*1 + (old mid1 == old mid2)*2 + (old back1 == old back2)*1. hand_score: if neither player fouled = rows won (1 per row with strictly higher strength than the opponent's) + 3 if all 3 rows won + royalty; if only the opponent fouled = 6 + royalty; if this player fouled = 0. total += hand_score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "when": "round_in_hand == 5",
      "effect": "Announce all six row strengths, both foul results and both hand scores."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If round_in_hand == 5: set every player's front, mid1, mid2, back1 and back2 to 0. If hand_number is odd, rotate 2 more cards from the front of deck to the back, so deck returns to its starting order. Then hand_number += 1 and round_in_hand = 1. Otherwise round_in_hand += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if hand_number > 4; otherwise continue."
    }
  ],
  "ending": {
    "condition": "hand_number > 4",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their match total, the sum of their four hand scores. The higher total wins, and equal totals share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 32 cards, values 1 to 8 with four copies each, and no suits."
    },
    {
      "id": "R2",
      "text": "The match is 4 hands of 5 rounds, 20 rounds in total, and ends when hand_number exceeds 4."
    },
    {
      "id": "R3",
      "text": "When hand 1 or hand 3 begins, the deck is shuffled once. Hand 2 uses the same order as hand 1, and hand 4 the same order as hand 3."
    },
    {
      "id": "R4",
      "text": "In round r of a hand, Seat X receives deck positions 6r-5 to 6r-3 and Seat Y receives positions 6r-2 to 6r. Positions 31 and 32 are never dealt."
    },
    {
      "id": "R5",
      "text": "In hands 1 and 3 Player A is Seat X and Player B is Seat Y; in hands 2 and 4 B is Seat X and A is Seat Y."
    },
    {
      "id": "R6",
      "text": "When hand 2 or 4 is dealt, each player receives in each round exactly the 3 cards the other player received in that round of the previous hand."
    },
    {
      "id": "R7",
      "text": "Each round, both players simultaneously keep exactly 1 of their 3 dealt cards."
    },
    {
      "id": "R8",
      "text": "Each round, both players simultaneously name a row (Front, Middle or Back) for the kept card."
    },
    {
      "id": "R9",
      "text": "Front holds 1 card, Middle holds 2 and Back holds 2."
    },
    {
      "id": "R10",
      "text": "When the named row is full, the card goes to the first non-full row in the order Back, Middle, Front."
    },
    {
      "id": "R11",
      "text": "The 2 unkept cards are discarded and never shown to the opponent."
    },
    {
      "id": "R12",
      "text": "After the choices, both kept cards and the rows they went to are announced face up."
    },
    {
      "id": "R13",
      "text": "Front strength = 2 x the Front card value (for example, a Front 5 has strength 10)."
    },
    {
      "id": "R14",
      "text": "Middle or Back strength = the sum of its two values, plus 100 if they are equal (for example, 4 and 4 = 108; 3 and 6 = 9)."
    },
    {
      "id": "R15",
      "text": "A hand fouls when Front strength > Middle strength or Middle strength > Back strength; equal strengths do not foul."
    },
    {
      "id": "R16",
      "text": "A non-fouling player with a Front card of 7 or 8 earns a royalty of +1."
    },
    {
      "id": "R17",
      "text": "A non-fouling player with a Middle pair earns a royalty of +2."
    },
    {
      "id": "R18",
      "text": "A non-fouling player with a Back pair earns a royalty of +1."
    },
    {
      "id": "R19",
      "text": "When neither player fouls, each row with strictly higher strength scores 1 point for its owner, and equal rows score nothing."
    },
    {
      "id": "R20",
      "text": "When neither player fouls and a player wins all 3 rows, that player scores 3 extra points (a scoop), for 6 points before royalties."
    },
    {
      "id": "R21",
      "text": "When neither player fouls, each player adds their own royalties to their hand score."
    },
    {
      "id": "R22",
      "text": "When exactly one player fouls, the other scores 6 plus their royalties and the fouler scores 0."
    },
    {
      "id": "R23",
      "text": "When both players foul, both score 0 for the hand."
    },
    {
      "id": "R24",
      "text": "After each hand, each player's hand score is added to their total; all row strengths, both foul results and both hand scores are announced; and the rows are cleared."
    },
    {
      "id": "R25",
      "text": "When the match ends, the player with the higher total wins, and equal totals are a draw."
    }
  ],
  "offers": [
    {
      "question": "Card choice: which card to keep",
      "who": "both seats, simultaneously",
      "options": "Exactly the 3 card values in that seat's hand this round."
    },
    {
      "question": "Row choice: which row for the kept card",
      "who": "both seats, simultaneously",
      "options": "Front, Middle, Back. All three are always offered; a full row redirects by the Back, Middle, Front fallback."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer set 2, and the duplicate format mirrors one seat's deal onto the other, which only works with two seats. The strategy is to remember the cards seen in the odd hand and use them to predict the opponent's options in the even hand, and to balance foul risk against pairs."
    },
    {
      "what": "Player A is seat 1 and Player B is seat 2",
      "why": "The rules name players A and B but not their seats."
    },
    {
      "what": "No talk step",
      "why": "The rules have no communication, and in a two-player zero-sum game talk adds nothing to reason about."
    },
    {
      "what": "Row choice offers all three rows even when one is full",
      "why": "The rules let a player name a full row and apply a fallback, so the fallback is kept rather than hiding options."
    },
    {
      "what": "Strengths are stored back into front, mid1 and back1 at scoring",
      "why": "This follows the build note, so foul tests, comparisons and royalties are single expressions."
    }
  ],
  "simplifications": [
    {
      "what": "Fixed deck order is encoded by rotating dealt cards from the front of the deck list to the back, plus 2 extra rotations after each odd hand",
      "why": "The engine has no position lookup. Rotation keeps the order so the even hand repeats the odd hand's deal exactly."
    },
    {
      "what": "Row comparison uses a table list, seat_strengths, holding both players' strengths and fouls",
      "why": "The engine cannot compare one player's attribute directly to another's; a table copy is the documented workaround."
    },
    {
      "what": "Discards are simply removed from the hand list rather than kept in a discard pile",
      "why": "Discards are never shown or used again, so no pile is needed."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: front, mid1, mid2, back1, back2, fouled, hand_score, total; table: hand_number, round_in_hand.
````

## Reply

````
```json
[
  {"name": "Setup: the deck holds 32 cards and all rows start empty", "rule": "R1", "players": 2, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 32}},
              "players": {"1": {"front": 0, "mid1": 0, "mid2": 0, "back1": 0, "back2": 0, "total": 0},
                          "2": {"front": 0, "mid1": 0, "mid2": 0, "back1": 0, "back2": 0, "total": 0}},
              "game": {"hand_number": 1, "round_in_hand": 1}}},

  {"name": "Match ends after hand 4; the higher total wins", "rule": "R2", "players": 2,
   "given": {"game": {"hand_number": 4, "round_in_hand": 5,
                      "deck": [1,1,1,2,2,2,1,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 3, "mid2": 4, "back1": 5, "back2": 6, "total": 5},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5, "total": 8}}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"winner": 1, "standings": {"1": 11, "2": 8},
              "players": {"1": {"hand_score": 6, "total": 11}, "2": {"hand_score": 0, "total": 8}},
              "game": {"hand_number": 5}}},

  {"name": "Hand 2 is not reshuffled: B gets the first 3 deck cards and A the next 3", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 2, "round_in_hand": 1,
                      "deck": [8,8,8,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8]}},
   "rules": [{"seat": 2, "options_include": 8}, {"seat": 2, "options_include": "Front"},
             {"seat": 1, "options_include": 1}, {"seat": 1, "options_include": "Front"}],
   "expect": {"players": {"1": {"front": 1}, "2": {"front": 8}},
              "offered": [{"seat": 2, "option": 8}, {"seat": 1, "option": 1}],
              "not_offered": [{"seat": 1, "option": 8}, {"seat": 2, "option": 1}],
              "game": {"hand_number": 2, "round_in_hand": 2}}},

  {"name": "Each round deals the next 6 deck positions: Seat X first, then Seat Y", "rule": "R4", "players": 2, "rounds": 2,
   "given": {"game": {"hand_number": 2, "round_in_hand": 1,
                      "deck": [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8,1,2,3,4]}},
   "rules": [{"seat": 2, "options_include": 1}, {"seat": 2, "options_include": 3}, {"seat": 2, "options_include": "Back", "times": 2},
             {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Back", "times": 2}],
   "expect": {"players": {"1": {"back1": 2, "back2": 4}, "2": {"back1": 1, "back2": 3}},
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 1, "option": 3}, {"seat": 2, "option": 2}, {"seat": 2, "option": 4}],
              "game": {"round_in_hand": 3}}},

  {"name": "In hand 1 Player A is Seat X and receives the first 3 cards", "rule": "R5", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 2,
                      "deck": [8,8,8,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8]}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"front": 8}, "2": {"front": 1}},
              "not_offered": [{"seat": 2, "option": 8}, {"seat": 1, "option": 1}]}},

  {"name": "After hand 1 the 2 undealt positions are skipped, so hand 2 deals B what A got in round 1", "rule": "R6", "players": 2, "rounds": 2,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [5,5,5,6,6,6,7,7,1,1,1,2,2,2,1,2,3,3,3,3,4,4,4,4,5,6,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 3, "mid2": 4, "back1": 5, "back2": 6},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Front", "times": 2},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front", "times": 2}],
   "expect": {"players": {"1": {"front": 2}, "2": {"front": 1}},
              "not_offered": [{"seat": 1, "option": 7}, {"seat": 2, "option": 7}, {"seat": 1, "option": 1}, {"seat": 2, "option": 2}],
              "game": {"hand_number": 2, "round_in_hand": 2}}},

  {"name": "Each seat keeps exactly the one card it picks from its 3", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 2,
                      "deck": [2,5,8,1,3,7,1,1,1,2,2,2,3,3,3,4,4,4,4,5,5,5,6,6,6,6,7,7,7,8,8,8]}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": "Middle"},
             {"seat": 2, "options_include": 7}, {"seat": 2, "options_include": "Back"}],
   "expect": {"players": {"1": {"mid1": 5, "mid2": 0, "front": 0, "back1": 0, "back2": 0},
                          "2": {"back1": 7, "back2": 0, "front": 0, "mid1": 0, "mid2": 0}},
              "offered": [{"seat": 1, "option": 2}, {"seat": 1, "option": 8}, {"seat": 2, "option": 1}, {"seat": 2, "option": 3}],
              "not_offered": [{"seat": 1, "option": 7}, {"seat": 2, "option": 5}]}},

  {"name": "The kept card goes into the row the seat names", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 2,
                      "deck": [4,4,4,6,6,6,1,1,1,1,2,2,2,2,3,3,3,3,4,5,5,5,5,6,7,7,7,7,8,8,8,8]}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "Middle"}],
   "expect": {"players": {"1": {"front": 4, "mid1": 0, "back1": 0}, "2": {"mid1": 6, "front": 0, "back1": 0}},
              "offered": [{"seat": 1, "option": "Back"}, {"seat": 2, "option": "Back"}]}},

  {"name": "Middle holds a second card after the first", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 3,
                      "deck": [4,4,4,6,6,6,1,1,1,1,2,2,2,2,3,3,3,3,4,5,5,5,5,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"mid1": 3}, "2": {"front": 2}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Middle"},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "Back"}],
   "expect": {"players": {"1": {"mid1": 3, "mid2": 4, "back1": 0}, "2": {"front": 2, "back1": 6, "back2": 0}}}},

  {"name": "A full named row falls back to Back, then Middle", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 3,
                      "deck": [4,4,4,6,6,6,1,1,1,1,2,2,2,2,3,3,3,3,4,5,5,5,5,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 5}, "2": {"front": 3, "back1": 5, "back2": 6}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"front": 5, "back1": 4, "mid1": 0}, "2": {"front": 3, "mid1": 6, "back1": 5, "back2": 6}}}},

  {"name": "Only the kept card is placed; the 2 unkept cards appear nowhere", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 2,
                      "deck": [2,5,8,1,3,7,1,1,1,2,2,2,3,3,3,4,4,4,4,5,5,5,6,6,6,6,7,7,7,8,8,8]}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 1, "options_include": "Back"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"back1": 8, "back2": 0, "front": 0, "mid1": 0, "mid2": 0},
                          "2": {"front": 1, "mid1": 0, "mid2": 0, "back1": 0, "back2": 0}}}},

  {"name": "Both kept cards are shown face up in their rows after the round", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 2,
                      "deck": [4,4,4,6,6,6,1,1,1,1,2,2,2,2,3,3,3,3,4,5,5,5,5,6,7,7,7,7,8,8,8,8]}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Back"},
             {"seat": 2, "options_include": 6}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"back1": 4}, "2": {"front": 6}}, "game": {"hand_number": 1, "round_in_hand": 3}}},

  {"name": "Front strength is doubled: Front 4 (8) beats Middle 3+4 (7), so A fouls", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [4,4,4,1,1,1,1,2,2,2,2,3,3,3,3,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 3, "mid2": 4, "back1": 5, "back2": 6},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 5, "back2": 6}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": true, "hand_score": 0, "total": 0},
                          "2": {"fouled": false, "hand_score": 6, "total": 6}}}},

  {"name": "A Middle pair adds 100: 2+2 (104) beats Back 7+8 (15), so A fouls", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [8,8,8,5,5,5,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,6,6,6,6,7,7,7,7,8]},
             "players": {"1": {"front": 1, "mid1": 2, "mid2": 2, "back1": 7, "back2": 0},
                         "2": {"front": 1, "mid1": 2, "mid2": 3, "back1": 4, "back2": 0}}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 1, "options_include": "Back"},
             {"seat": 2, "options_include": 5}, {"seat": 2, "options_include": "Back"}],
   "expect": {"players": {"1": {"fouled": true, "hand_score": 0}, "2": {"fouled": false, "hand_score": 6}}}},

  {"name": "Equal row strengths (6,6,6) do not foul", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [3,3,3,1,1,1,1,2,2,2,2,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 2, "mid2": 4, "back1": 1, "back2": 5},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 2, "total": 2},
                          "2": {"fouled": false, "hand_score": 1, "total": 1}}}},

  {"name": "Front 7 earns +1 royalty (6 + 1 against a fouled opponent)", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [7,7,7,2,2,2,1,1,1,1,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 7, "mid2": 8, "back1": 8, "back2": 7},
                         "2": {"front": 0, "mid1": 1, "mid2": 1, "back1": 2, "back2": 3}}},
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 7}, "2": {"fouled": true, "hand_score": 0}}}},

  {"name": "A Middle pair earns +2 (with the needed Back pair +1: 6+3 = 9)", "rule": "R17", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [3,3,3,2,2,2,1,1,1,1,2,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 1, "mid1": 3, "mid2": 0, "back1": 5, "back2": 5},
                         "2": {"front": 0, "mid1": 1, "mid2": 1, "back1": 2, "back2": 3}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": "Middle"},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 9}, "2": {"fouled": true, "hand_score": 0}}}},

  {"name": "A Back pair earns +1 (6 + 1 against a fouled opponent)", "rule": "R18", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [4,4,4,2,2,2,1,1,1,1,2,3,3,3,3,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 1, "mid1": 2, "mid2": 3, "back1": 4, "back2": 0},
                         "2": {"front": 0, "mid1": 1, "mid2": 1, "back1": 2, "back2": 3}}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": "Back"},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 7}, "2": {"fouled": true, "hand_score": 0}}}},

  {"name": "Only strictly higher rows score; tied Front and Back score nothing", "rule": "R19", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [5,5,5,4,4,4,1,1,1,1,2,2,2,2,3,3,3,3,4,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 3, "mid1": 3, "mid2": 0, "back1": 4, "back2": 6},
                         "2": {"front": 3, "mid1": 2, "mid2": 0, "back1": 4, "back2": 6}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": "Middle"},
             {"seat": 2, "options_include": 4}, {"seat": 2, "options_include": "Middle"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 1}, "2": {"fouled": false, "hand_score": 0}}}},

  {"name": "Winning all 3 rows scores 3+3, plus A's royalties of 3 = 9", "rule": "R20", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [3,3,3,1,1,1,1,2,2,2,2,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 5, "mid2": 5, "back1": 6, "back2": 6},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 9, "total": 9},
                          "2": {"fouled": false, "hand_score": 0, "total": 0}}}},

  {"name": "With no foul, each player adds their own royalties to rows won", "rule": "R21", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [7,7,7,8,8,8,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,8]},
             "players": {"1": {"front": 0, "mid1": 7, "mid2": 7, "back1": 8, "back2": 8},
                         "2": {"front": 0, "mid1": 1, "mid2": 1, "back1": 2, "back2": 2}}},
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 8}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": false, "hand_score": 6}, "2": {"fouled": false, "hand_score": 5}}}},

  {"name": "Exactly one foul: the other scores 6 plus royalties and the fouler scores 0", "rule": "R22", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [5,5,5,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 1, "mid2": 2, "back1": 3, "back2": 4},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 4}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": true, "hand_score": 0}, "2": {"fouled": false, "hand_score": 7}}}},

  {"name": "Both players foul: both score 0 and totals stay", "rule": "R23", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [5,5,5,2,2,2,1,1,1,1,2,3,3,3,3,4,4,4,4,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 1, "mid2": 2, "back1": 3, "back2": 4, "total": 5},
                         "2": {"front": 0, "mid1": 1, "mid2": 1, "back1": 2, "back2": 3, "total": 3}}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 2}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"fouled": true, "hand_score": 0, "total": 5},
                          "2": {"fouled": true, "hand_score": 0, "total": 3}}}},

  {"name": "After a hand the score is added to the total, rows are cleared and hand 2 begins", "rule": "R24", "players": 2, "rounds": 1,
   "given": {"game": {"hand_number": 1, "round_in_hand": 5,
                      "deck": [3,3,3,1,1,1,1,2,2,2,2,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 5, "mid2": 5, "back1": 6, "back2": 6, "total": 10},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5, "total": 4}}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"players": {"1": {"hand_score": 9, "total": 19, "front": 0, "mid1": 0, "mid2": 0, "back1": 0, "back2": 0},
                          "2": {"hand_score": 0, "total": 4, "front": 0, "mid1": 0, "mid2": 0, "back1": 0, "back2": 0}},
              "game": {"hand_number": 2, "round_in_hand": 1}}},

  {"name": "Equal final totals share the win", "rule": "R25", "players": 2,
   "given": {"game": {"hand_number": 4, "round_in_hand": 5,
                      "deck": [1,1,1,2,2,2,1,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,7,7,7,7,8,8,8,8]},
             "players": {"1": {"front": 0, "mid1": 3, "mid2": 4, "back1": 5, "back2": 6, "total": 4},
                         "2": {"front": 0, "mid1": 2, "mid2": 3, "back1": 4, "back2": 5, "total": 10}}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 1, "options_include": "Front"},
             {"seat": 2, "options_include": 1}, {"seat": 2, "options_include": "Front"}],
   "expect": {"winner": [1, 2], "standings": {"1": 10, "2": 10},
              "players": {"1": {"hand_score": 6, "total": 10}, "2": {"hand_score": 0, "total": 10}}}}
]
```
````
