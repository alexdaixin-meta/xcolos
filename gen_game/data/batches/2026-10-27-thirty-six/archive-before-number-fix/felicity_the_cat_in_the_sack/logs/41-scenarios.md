# 41 scenarios

- time: 2026-10-27T17:40:04+00:00 (81.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 396331bdf7033d05, reply sha256 de509d3cee9b565b

## Sent

````
SPEC:
{
  "name": "Cat in the Sack: Two Peeks",
  "summary": "Each round every player secretly adds a card to a sack. Players bid mice in up to two sealed stages, seeing one card before each stage. The winner pays and scores the cats inside, and dogs may remove the best or worst cat. Most cat points plus mice after 9 rounds wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "starting_mice": 15,
    "stage1_pass_bonus": 2,
    "stage2_pass_bonus": 3,
    "rounds": 9,
    "hand_size_dealt": 10,
    "set_aside_per_player": 1,
    "hand_size_after_setup": 9,
    "cat_neg8_value": -8,
    "cat_neg5_value": -5,
    "cat_3_value": 3,
    "cat_5_value": 5,
    "cat_8_value": 8,
    "cat_11_value": 11,
    "cat_15_value": 15,
    "rabbit_value": 0,
    "large_dog_value": 0,
    "small_dog_value": 0,
    "first_peek_index": 1,
    "second_peek_index": 2,
    "min_bid_to_count": 1,
    "rank_score_multiplier": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [
          "cat_-8",
          "cat_-5",
          "cat_3",
          "cat_5",
          "cat_8",
          "cat_11",
          "cat_15",
          "rabbit",
          "large_dog",
          "small_dog"
        ],
        "meaning": "Cards the player may still play. It starts with all 10 cards, and setup removes 1 at random, leaving 9.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The card chosen this round. It stays private until the sack is revealed.",
        "observable": false
      },
      {
        "key": "mice",
        "type": "number",
        "visible": "public",
        "initial": 15,
        "meaning": "Currency used for bidding. It counts toward the score.",
        "observable": true
      },
      {
        "key": "cat_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total value of the cats won in sacks.",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The latest sealed bid, made public after each poll. 0 is a pass.",
        "observable": false
      },
      {
        "key": "in_auction",
        "type": "bool",
        "visible": "public",
        "initial": true,
        "meaning": "Whether the player is still in this round's auction.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 15,
        "meaning": "cat_points + mice, recalculated at the end of each round.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The cards removed unseen from each hand at setup.",
        "observable": false
      },
      {
        "key": "start_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat whose card is first in the sack. It is chosen at random once.",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round, from 1 to 9.",
        "observable": true
      },
      {
        "key": "sack_owners",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Seat order in the sack, starting at start_seat and wrapping round.",
        "observable": false
      },
      {
        "key": "sack_cards",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The played cards in sack_owners order.",
        "observable": false
      },
      {
        "key": "sack_revealed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The sack cards peeked at so far this round.",
        "observable": false
      },
      {
        "key": "standing_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current highest bid, which is the price.",
        "observable": false
      },
      {
        "key": "leader_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The stage-1 high bidder.",
        "observable": false
      },
      {
        "key": "bidder_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players with a stage-1 bid above 0.",
        "observable": false
      },
      {
        "key": "sack_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that wins the sack. 0 means none.",
        "observable": false
      },
      {
        "key": "sack_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The cat value awarded this round.",
        "observable": false
      }
    ]
  },
  "setup": [
    "This normal setup runs only when a scenario does not supply hands, mice or other state. Supplied state is never replaced.",
    "Each player's hand is set to the 10 cards: cat_-8, cat_-5, cat_3, cat_5, cat_8, cat_11, cat_15, rabbit, large_dog, small_dog.",
    "From each hand, one card is chosen at random, removed from hand and appended to set_aside, unseen by everyone. Each hand is left with 9 cards.",
    "Each player gets mice = starting_mice (15), cat_points = 0 and score = 15.",
    "round_number = 0.",
    "start_seat is chosen uniformly at random from the seats, once.",
    "Each player is synced with their own hand."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_number += 1. For every player: bid = 0, in_auction = true, played_card = ''. For the table: standing_bid = 0, leader_seat = 0, bidder_count = 0, sack_winner = 0, sack_value = 0, sack_revealed = [], sack_owners = [], sack_cards = []."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own hand",
      "effect": "The chosen card is removed from hand and stored in played_card."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "sack_owners = the seats in ascending order starting at start_seat and wrapping after the last seat to seat 1 (for example, start_seat 3 of 4 gives [3,4,1,2]). sack_cards = each owner's played_card in the same order."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "First peek: sack_cards[1] (the start seat's card) is appended to sack_revealed and broadcast to all."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to your own mice (0 = pass)",
      "effect": "Stored in bid, then made public."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "bidder_count = the number of players with bid > 0. standing_bid = the maximum bid. leader_seat = the seat with the maximum bid; ties go to the seat earliest in sack_owners. Every player with bid = 0 gets in_auction = false. If bidder_count >= 1, every player with bid = 0 also gets mice += stage1_pass_bonus (2)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when bidder_count = 0. sack_cards = []. start_seat = (start_seat mod player_count) + 1. Nobody gains anything, and no later step that needs bidders runs."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when bidder_count = 1. sack_winner = leader_seat, and the price stays at standing_bid. There is no stage 2."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when bidder_count >= 2. Second peek: sack_cards[2] is appended to sack_revealed and broadcast to all."
    },
    {
      "action": "poll",
      "who": "every player with in_auction = true, when bidder_count >= 2",
      "answer": "0, or a whole number from standing_bid+1 to your own mice. A player with mice <= standing_bid may only answer 0.",
      "effect": "The answer replaces bid, which is then made public."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when bidder_count >= 2. If any in-auction player has bid > 0: sack_winner = the in-auction seat with the highest bid (ties go to the seat earliest in sack_owners) and standing_bid = that bid. Otherwise sack_winner = leader_seat and standing_bid is unchanged. Then every in-auction player with bid = 0 who is not sack_winner gets mice += stage2_pass_bonus (3)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when sack_winner > 0. The sack_winner's mice -= standing_bid. Dog rule: if exactly one of large_dog or small_dog is in sack_cards and at least one cat is there, then large_dog removes one cat with the highest value, or small_dog removes one cat with the lowest value. With 0 or 2 dogs, or no cats, nothing is removed. sack_value = the sum of the values of the remaining cat cards (rabbit and dogs count 0). The sack_winner's cat_points += sack_value. All sack_cards are broadcast to everyone, then sack_cards = []."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "This step runs when sack_winner > 0. start_seat = sack_winner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For every player: score = cat_points + mice. Mice, cat_points and score are announced."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round_number >= 9. Otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round_number >= 9",
    "rank_by": "(you.cat_points + you.mice) * 1000 + you.cat_points",
    "decided_by": "The highest cat_points + mice wins. Ties are broken by higher cat_points. Players still tied share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At normal setup each player's hand holds the 10 cards, and 1 random card per hand is moved to set_aside, leaving 9 cards per hand. State supplied by a scenario is not replaced."
    },
    {
      "id": "R2",
      "text": "At setup each player has mice = 15 and cat_points = 0, round_number = 0, and start_seat is chosen at random once."
    },
    {
      "id": "R3",
      "text": "At the start of each round, round_number increases by 1. Every player has bid = 0 and in_auction = true. standing_bid, leader_seat, bidder_count, sack_winner and sack_value are 0, and sack_revealed is empty."
    },
    {
      "id": "R4",
      "text": "Each round every player simultaneously plays one card from their own hand to played_card, so the hand shrinks by 1."
    },
    {
      "id": "R5",
      "text": "sack_owners lists the seats from start_seat ascending and wrapping (start_seat 3 of 4 gives [3,4,1,2]), and sack_cards holds the played cards in that order."
    },
    {
      "id": "R6",
      "text": "Before stage 1, sack_cards[1] is appended to sack_revealed and shown to all."
    },
    {
      "id": "R7",
      "text": "In stage 1 each player simultaneously bids a whole number from 0 to their own mice, and 0 is a pass."
    },
    {
      "id": "R8",
      "text": "After stage 1, bidder_count is the number of bids above 0, standing_bid is the highest bid, and leader_seat is the highest bidder, with ties going to the seat earliest in sack_owners."
    },
    {
      "id": "R9",
      "text": "After stage 1, every player with bid 0 gets in_auction = false. If bidder_count >= 1, each of them also gains 2 mice."
    },
    {
      "id": "R10",
      "text": "When bidder_count = 0, nobody gains or pays, sack_cards is cleared, and start_seat advances by 1 (after the last seat comes seat 1)."
    },
    {
      "id": "R11",
      "text": "When bidder_count = 1, sack_winner = leader_seat at a price of their stage-1 bid, and there is no second peek or stage 2."
    },
    {
      "id": "R12",
      "text": "When bidder_count >= 2, sack_cards[2] is appended to sack_revealed and shown to all."
    },
    {
      "id": "R13",
      "text": "In stage 2, each in-auction player simultaneously bids 0 or a number from standing_bid+1 to their mice. A player with mice <= standing_bid may only bid 0."
    },
    {
      "id": "R14",
      "text": "If any stage-2 bid is above 0, the highest stage-2 bidder wins (ties go to the seat earliest in sack_owners) and standing_bid becomes that bid. Otherwise leader_seat wins at the stage-1 standing_bid."
    },
    {
      "id": "R15",
      "text": "Every in-auction player who bid 0 in stage 2 and is not sack_winner gains 3 mice."
    },
    {
      "id": "R16",
      "text": "The sack_winner pays standing_bid mice to the bank."
    },
    {
      "id": "R17",
      "text": "If exactly one dog is in the sack, large_dog removes the highest-value cat or small_dog removes the lowest-value cat. With 0 or 2 dogs, or no cats, nothing is removed."
    },
    {
      "id": "R18",
      "text": "sack_value is the sum of the values of the remaining cats (rabbit and dogs are worth 0) and is added to the sack_winner's cat_points. All sack_cards are then shown and cleared."
    },
    {
      "id": "R19",
      "text": "When there is a sack_winner, start_seat becomes sack_winner."
    },
    {
      "id": "R20",
      "text": "The game ends after round 9, and each player's score = cat_points + mice."
    },
    {
      "id": "R21",
      "text": "The highest score wins, and ties are broken by higher cat_points. Players still tied share the win."
    }
  ],
  "offers": [
    {
      "question": "Play a card",
      "who": "all players",
      "options": "Every card currently in the player's own hand."
    },
    {
      "question": "Stage 1 bid",
      "who": "all players",
      "options": "A whole number from 0 to the player's own mice. A player with 0 mice may only choose 0."
    },
    {
      "question": "Stage 2 bid",
      "who": "players with in_auction = true, only when bidder_count >= 2",
      "options": "A player with mice > standing_bid may choose 0 or a whole number from standing_bid+1 to their mice. A player with mice <= standing_bid may choose only 0. Players out of the auction are not asked."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggested 4, and the source allows 3 to 5. 3 is the minimum because the auction needs rivals and the pass bonuses only matter with several bidders. Above 5 the sack has too many unseen cards, so the peeks tell too little."
    },
    {
      "what": "No talk step added",
      "why": "The source has no talk phase, and adding one would add a mechanic. The strategy lies in reading the peeks and others' public bids, and in choosing between passing for the bonus and paying."
    },
    {
      "what": "When a dog removes a cat and several cats share the highest or lowest value, only one of them is removed",
      "why": "The source says 'the cat', which means a single card."
    },
    {
      "what": "The tie-break is folded into rank_by as score*1000 + cat_points",
      "why": "cat_points stays within -65 to 210, so a 1-point score difference always outweighs it."
    },
    {
      "what": "score is kept as an attribute and updated every round",
      "why": "This makes the final score observable. It equals cat_points + mice after round 9, as the rules state."
    }
  ],
  "simplifications": [
    {
      "what": "The stage-2 range has a gap (0, or standing_bid+1 to mice). It is offered as a number with validation rejecting 1 to standing_bid. If the engine can only express a contiguous range, any value from 1 to standing_bid is treated as 0 (a pass).",
      "why": "Engine number questions take a single range."
    },
    {
      "what": "Stages and branches (no bidders, sole bidder, two or more bidders) are built as a flat step list with arithmetic 'when' conditions on single steps.",
      "why": "The engine runs a flat step list, and each branch here is one condition per step."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: mice, cat_points, score; table: start_seat, round_number.
````

## Reply

````
```json
[
  {"name": "Normal setup: each hand holds 9 cards and 1 card per player is set aside (exact cards are random)", "rule": "R1", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"lens": {"game": {"set_aside": 3}, "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}}}}},

  {"name": "Supplied hands are not replaced by setup", "rule": "R1", "players": 3, "seed": 2, "rounds": 0,
   "given": {"players": {"1": {"hand": ["cat_3", "rabbit"]}, "2": {"hand": ["cat_5", "rabbit"]}, "3": {"hand": ["cat_8", "rabbit"]}}},
   "expect": {"lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "Setup gives 15 mice, 0 cat points, score 15 and round 0 (start seat is random, so it is not asserted)", "rule": "R2", "players": 4, "seed": 3, "rounds": 0,
   "expect": {"players": {"1": {"mice": 15, "cat_points": 0, "score": 15}, "2": {"mice": 15, "cat_points": 0, "score": 15}, "3": {"mice": 15, "cat_points": 0, "score": 15}, "4": {"mice": 15, "cat_points": 0, "score": 15}},
              "game": {"round_number": 0}}},

  {"name": "Round number goes up by 1 at the start of a round", "rule": "R3", "players": 3, "seed": 4, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3", "rabbit"]}, "2": {"hand": ["cat_5", "rabbit"]}, "3": {"hand": ["cat_8", "rabbit"]}},
             "game": {"round_number": 4, "start_seat": 1}},
   "expect": {"game": {"round_number": 5}}},

  {"name": "Each player plays one card, so the hand shrinks by 1", "rule": "R4", "players": 3, "seed": 5, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3", "rabbit"]}, "2": {"hand": ["cat_5", "rabbit"]}, "3": {"hand": ["cat_8", "rabbit"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": "cat_3"}, {"seat": 2, "options_include": "cat_5"}, {"seat": 3, "options_include": "cat_8"}],
   "expect": {"lens": {"players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}, "players": {"1": {"mice": 15}, "2": {"mice": 15}, "3": {"mice": 15}}}},

  {"name": "Sack order starts at start_seat 3 and wraps, so seat 3 wins a tie with seat 1", "rule": "R5", "players": 3, "seed": 6, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 3}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 3, "options_include": 5}],
   "expect": {"players": {"1": {"mice": 18, "cat_points": 0, "score": 18}, "2": {"mice": 17, "cat_points": 0, "score": 17}, "3": {"mice": 10, "cat_points": 16, "score": 26}},
              "game": {"start_seat": 3}}},

  {"name": "First peek reveals one card before stage 1 (all pass, so no second peek)", "rule": "R6", "players": 3, "seed": 7, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "expect": {"lens": {"game": {"sack_revealed": 1}}}},

  {"name": "Stage 1 bid ranges from 0 to the player's own mice", "rule": "R7", "players": 3, "seed": 8, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"], "mice": 3}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "expect": {"offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 3}, {"seat": 2, "option": 15}],
              "not_offered": [{"seat": 1, "option": 4}, {"seat": 2, "option": 16}],
              "players": {"1": {"mice": 3}, "2": {"mice": 15}, "3": {"mice": 15}}}},

  {"name": "The highest stage-1 bidder leads and wins when nobody bids in stage 2", "rule": "R8", "players": 3, "seed": 9, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 8, "cat_points": 16, "score": 24}, "2": {"mice": 18, "cat_points": 0, "score": 18}, "3": {"mice": 17, "cat_points": 0, "score": 17}},
              "game": {"start_seat": 1}}},

  {"name": "Stage-1 passers gain 2 mice when someone bids", "rule": "R9", "players": 3, "seed": 10, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 2, "options_include": 4}],
   "expect": {"players": {"1": {"mice": 17, "cat_points": 0}, "2": {"mice": 11, "cat_points": 16}, "3": {"mice": 17, "cat_points": 0}}}},

  {"name": "Nobody bids: no gains or payments, and start seat advances from the last seat to seat 1", "rule": "R10", "players": 3, "seed": 11, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 3}},
   "expect": {"players": {"1": {"mice": 15, "cat_points": 0, "score": 15}, "2": {"mice": 15, "cat_points": 0, "score": 15}, "3": {"mice": 15, "cat_points": 0, "score": 15}},
              "game": {"start_seat": 1}}},

  {"name": "Nobody bids: start seat advances by 1", "rule": "R10", "players": 3, "seed": 12, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "expect": {"game": {"start_seat": 2}, "players": {"1": {"mice": 15}, "2": {"mice": 15}, "3": {"mice": 15}}}},

  {"name": "Sole bidder wins at their stage-1 bid with no second peek", "rule": "R11", "players": 3, "seed": 13, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 3, "options_include": 6}],
   "expect": {"lens": {"game": {"sack_revealed": 1}},
              "players": {"1": {"mice": 17}, "2": {"mice": 17}, "3": {"mice": 9, "cat_points": 16, "score": 25}},
              "game": {"start_seat": 3}}},

  {"name": "Two bidders: the second peek reveals a second card", "rule": "R12", "players": 3, "seed": 14, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 7}, {"seat": 2, "options_include": 4}],
   "expect": {"lens": {"game": {"sack_revealed": 2}}}},

  {"name": "Stage 2: a player with mice at the standing bid can only pass, and a rival outbids above the standing bid", "rule": "R13", "players": 3, "seed": 15, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"], "mice": 5}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 3}, {"seat": 2, "options_include": 6}],
   "expect": {"offered": [{"seat": 2, "option": 6}],
              "players": {"1": {"mice": 8, "cat_points": 0}, "2": {"mice": 9, "cat_points": 16, "score": 25}, "3": {"mice": 17, "cat_points": 0}},
              "game": {"start_seat": 2}}},

  {"name": "Stage-2 high bidder beats the stage-1 leader and pays the stage-2 bid", "rule": "R14", "players": 3, "seed": 16, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": 3}, {"seat": 2, "options_include": 7}],
   "expect": {"players": {"1": {"mice": 18, "cat_points": 0}, "2": {"mice": 8, "cat_points": 16, "score": 24}, "3": {"mice": 17, "cat_points": 0}}}},

  {"name": "Stage-2 tie goes to the seat earliest in the sack order", "rule": "R14", "players": 3, "seed": 17, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 2}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 3}, {"seat": 2, "options_include": 8}],
   "expect": {"players": {"1": {"mice": 15, "cat_points": 0}, "2": {"mice": 7, "cat_points": 16, "score": 23}, "3": {"mice": 17, "cat_points": 0}},
              "game": {"start_seat": 2}}},

  {"name": "In-auction stage-2 passers who lose gain 3 mice", "rule": "R15", "players": 3, "seed": 18, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 1}, {"seat": 3, "options_include": 10}],
   "expect": {"players": {"1": {"mice": 18, "cat_points": 0}, "2": {"mice": 18, "cat_points": 0}, "3": {"mice": 5, "cat_points": 16, "score": 21}},
              "game": {"start_seat": 3}}},

  {"name": "Winner pays the standing bid for a sack of rabbits worth 0", "rule": "R16", "players": 3, "seed": 19, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["rabbit"]}, "3": {"hand": ["rabbit"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 9}],
   "expect": {"players": {"1": {"mice": 6, "cat_points": 0, "score": 6}, "2": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "A single large dog removes the highest cat", "rule": "R17", "players": 3, "seed": 20, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["large_dog"]}, "2": {"hand": ["cat_15"]}, "3": {"hand": ["cat_3"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 3, "score": 16}}}},

  {"name": "A single small dog removes the lowest cat", "rule": "R17", "players": 3, "seed": 21, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["small_dog"]}, "2": {"hand": ["cat_15"]}, "3": {"hand": ["cat_-8"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"mice": 13, "cat_points": 15, "score": 28}}}},

  {"name": "Two dogs cancel and no cat is removed", "rule": "R17", "players": 3, "seed": 22, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["large_dog"]}, "2": {"hand": ["small_dog"]}, "3": {"hand": ["cat_11"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 2, "options_include": 4}],
   "expect": {"players": {"2": {"mice": 11, "cat_points": 11, "score": 22}, "1": {"mice": 17}, "3": {"mice": 17}}}},

  {"name": "Sack value sums the cats, with the rabbit worth 0, including a negative cat", "rule": "R18", "players": 3, "seed": 23, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["rabbit"]}, "2": {"hand": ["cat_-5"]}, "3": {"hand": ["cat_11"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 3, "options_include": 1}],
   "expect": {"players": {"3": {"mice": 14, "cat_points": 6, "score": 20}, "1": {"mice": 17, "cat_points": 0}, "2": {"mice": 17, "cat_points": 0}},
              "lens": {"game": {"sack_cards": 0}}}},

  {"name": "Start seat becomes the sack winner", "rule": "R19", "players": 4, "seed": 24, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"]}, "2": {"hand": ["cat_5"]}, "3": {"hand": ["cat_8"]}, "4": {"hand": ["rabbit"]}},
             "game": {"round_number": 0, "start_seat": 1}},
   "rules": [{"seat": 2, "options_include": 3}],
   "expect": {"game": {"start_seat": 2}, "players": {"2": {"mice": 12, "cat_points": 16, "score": 28}, "1": {"mice": 17}, "3": {"mice": 17}, "4": {"mice": 17}}}},

  {"name": "Game ends after round 9 and the score is cat_points + mice", "rule": "R20", "players": 3, "seed": 25, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"], "mice": 20, "cat_points": 0}, "2": {"hand": ["cat_5"], "mice": 15, "cat_points": 0}, "3": {"hand": ["cat_8"], "mice": 10, "cat_points": 0}},
             "game": {"round_number": 8, "start_seat": 1}},
   "expect": {"winner": 1, "standings": {"1": 20000, "2": 15000, "3": 10000},
              "players": {"1": {"score": 20}, "2": {"score": 15}, "3": {"score": 10}},
              "game": {"round_number": 9}}},

  {"name": "Tied score is broken by higher cat_points", "rule": "R21", "players": 3, "seed": 26, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"], "mice": 10, "cat_points": 10}, "2": {"hand": ["cat_5"], "mice": 15, "cat_points": 5}, "3": {"hand": ["cat_8"], "mice": 5, "cat_points": 0}},
             "game": {"round_number": 8, "start_seat": 1}},
   "expect": {"winner": 1, "standings": {"1": 20010, "2": 20005, "3": 5000},
              "players": {"1": {"score": 20}, "2": {"score": 20}, "3": {"score": 5}}}},

  {"name": "Players level on score and cat_points share the win", "rule": "R21", "players": 3, "seed": 27, "default": "decline",
   "given": {"players": {"1": {"hand": ["cat_3"], "mice": 10, "cat_points": 10}, "2": {"hand": ["cat_5"], "mice": 10, "cat_points": 10}, "3": {"hand": ["cat_8"], "mice": 5, "cat_points": 0}},
             "game": {"round_number": 8, "start_seat": 1}},
   "expect": {"winner": [1, 2], "standings": {"1": 20010, "2": 20010, "3": 5000}}}
]
```
````
