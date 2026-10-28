# 04 scenarios

- time: 2026-10-28T01:43:28+00:00 (116.1s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 3bd2baf4d56eb996, reply sha256 e561fb2b8f86aed1

## Sent

````
SPEC:
{
  "name": "Greek Hold 'em Lite",
  "summary": "A simplified simultaneous-betting poker for 3 to 5 players: ante, flop bet, call or fold, river bet, call or fold, then an arithmetic showdown, over 15 hands; most chips wins.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "starting_chips": 40,
    "deck_size": 32,
    "card_value_min": 1,
    "card_value_max": 8,
    "copies_per_value": 4,
    "hands": 15,
    "ante": 1,
    "hole_cards": 2,
    "board_cards": 5,
    "flop_cards": 3,
    "min_bet": 0,
    "max_bet": 4,
    "match_weight": 20,
    "max_matches": 3,
    "pair_bonus": 30,
    "elimination_chips": 0
  },
  "attributes": {
    "player": [
      {
        "key": "chips",
        "type": "number",
        "visible": "public",
        "initial": 40,
        "meaning": "The player's chip stack. It is the score.",
        "observable": true
      },
      {
        "key": "out",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once the player reached 0 chips at the end of a hand and was eliminated.",
        "observable": true
      },
      {
        "key": "hole",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's 2 hole cards (values 1-8), seen only by the owner.",
        "observable": false
      },
      {
        "key": "shown_hole",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Hole cards revealed at showdown by a player still in the hand.",
        "observable": true
      },
      {
        "key": "in_hand",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True while the player is still contesting the current hand (has not folded and is not eliminated).",
        "observable": false
      },
      {
        "key": "bet",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips the player has put in during the current betting round, including any call.",
        "observable": false
      },
      {
        "key": "strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Showdown Strength = 20*min(matches,3) + 30*pair + hole1 + hole2.",
        "observable": false
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
        "meaning": "The 32-card deck, rebuilt and shuffled each hand.",
        "observable": false
      },
      {
        "key": "board",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 5 face-down board cards, in order.",
        "observable": false
      },
      {
        "key": "board_shown",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Board cards revealed so far: the first 3 at the flop, all 5 at the turn and river.",
        "observable": true
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips in the pot. A leftover from a split carries to the next hand.",
        "observable": true
      },
      {
        "key": "hand_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of the current hand, from 1 to 15.",
        "observable": true
      },
      {
        "key": "high_bet",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "H, the largest bet in the current betting round.",
        "observable": false
      },
      {
        "key": "in_hand_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many players have in_hand true.",
        "observable": false
      },
      {
        "key": "alive_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many players have out false.",
        "observable": false
      },
      {
        "key": "best_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest strength among players in the hand at showdown.",
        "observable": false
      },
      {
        "key": "winners_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many in-hand players have strength equal to best_strength.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player gets chips = 40, out = false, hole = [] and shown_hole = [].",
    "Set pot = 0, hand_no = 0, and alive_count to the number of players.",
    "There is no dealer and no acting order. Every decision is made simultaneously."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "hand_no += 1. For each player with out = false: chips -= 1, pot += 1, in_hand = true. For each player with out = true: in_hand = false. Every player gets bet = 0, strength = 0, hole = [] and shown_hole = []. Set board = [] and board_shown = []. A player left with 0 chips after the ante is all-in and stays in the hand."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Rebuild deck as the 32 cards (values 1-8, four of each). For each player with in_hand = true, draw 2 cards at random: remove each from deck and append it to that player's hole. Then draw 5 cards at random from deck and append them in order to board."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hole cards."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Flop: board_shown = the first 3 cards of board. Announce board_shown, pot and every player's chips to everyone."
    },
    {
      "action": "poll",
      "who": "every player with in_hand = true",
      "answer": "a whole number from 0 to min(4, chips)",
      "effect": "Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together."
    },
    {
      "action": "poll",
      "who": "every player with in_hand = true and bet < high_bet",
      "answer": "call | fold",
      "effect": "call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid, and the player stays in. fold: in_hand = false, and chips already put in stay in pot. Players with bet = high_bet stay in automatically."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "in_hand_count = number of players with in_hand = true. If in_hand_count = 1: that player's chips += pot and pot = 0, and the hand skips to elimination."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When in_hand_count >= 2: board_shown = all 5 cards of board, every player's bet = 0, and high_bet = 0. Announce board_shown and pot."
    },
    {
      "action": "poll",
      "who": "every player with in_hand = true, when in_hand_count >= 2",
      "answer": "a whole number from 0 to min(4, chips)",
      "effect": "Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together."
    },
    {
      "action": "poll",
      "who": "every player with in_hand = true and bet < high_bet, when in_hand_count >= 2",
      "answer": "call | fold",
      "effect": "call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid. fold: in_hand = false, and chips stay in pot."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When in_hand_count >= 2 before this step: recount in_hand_count. If it is 1, that player's chips += pot and pot = 0. Otherwise it is a showdown. For each player with in_hand = true: shown_hole = hole; matches = number of board cards whose value equals either hole value; pair = 1 if hole[0] = hole[1], else 0; strength = 20*min(matches,3) + 30*pair + hole[0] + hole[1]. Then best_strength = max strength among in-hand players and winners_count = number of in-hand players with strength = best_strength. Each such player's chips += floor(pot / winners_count), and pot = pot mod winners_count. Announce the shown hole cards, the strengths and the winners."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Elimination: every player with out = false and chips = 0 gets out = true and in_hand = false. alive_count = number of players with out = false. Announce each player's chips and who is eliminated."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_no >= 15 or alive_count <= 1; otherwise run the next hand."
    }
  ],
  "ending": {
    "condition": "hand_no >= 15 or alive_count <= 1",
    "rank_by": "you.chips",
    "decided_by": "Each player's standing is their chip count. The player with the most chips wins, and players tied for the most chips share the win (a draw). If only one player has chips left before hand 15, that player wins, because every other player has 0."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, each player has 40 chips and the pot is 0."
    },
    {
      "id": "R2",
      "text": "When a hand starts, each player not eliminated pays 1 chip into the pot, so a player with 5 chips goes to 4 and the pot rises by 1 per player."
    },
    {
      "id": "R3",
      "text": "When a player with exactly 1 chip antes, they have 0 chips and still take part in the hand (all-in)."
    },
    {
      "id": "R4",
      "text": "When a hand starts, the deck is rebuilt to 32 cards (values 1 to 8, four of each), each player in the hand receives 2 hole cards from it, and 5 board cards are drawn from it."
    },
    {
      "id": "R5",
      "text": "When the flop happens, exactly the first 3 board cards become public in board_shown."
    },
    {
      "id": "R6",
      "text": "When a player bets in a betting round, the bet is a whole number from 0 to 4 and no more than their chips, and it moves from their chips to the pot."
    },
    {
      "id": "R7",
      "text": "When bets are revealed, H is the largest bet among players still in the hand, and only players who bet less than H are asked to call or fold."
    },
    {
      "id": "R8",
      "text": "When a player calls, they pay H minus their bet, so a player who bet 1 against H = 4 pays 3 more."
    },
    {
      "id": "R9",
      "text": "When a player calls with fewer chips than the difference, they pay all their chips, go to 0, and stay in the hand."
    },
    {
      "id": "R10",
      "text": "When a player folds, they leave the hand and the chips they already bet stay in the pot."
    },
    {
      "id": "R11",
      "text": "When only one player remains in the hand after the flop call or fold, that player takes the whole pot, the pot becomes 0, and the turn, river and showdown do not happen."
    },
    {
      "id": "R12",
      "text": "When 2 or more players remain after the flop, board cards 4 and 5 are revealed, so board_shown has all 5 cards."
    },
    {
      "id": "R13",
      "text": "When the river betting happens, it follows R6 to R10, with bets reset to 0 for the new round."
    },
    {
      "id": "R14",
      "text": "When only one player remains after the river call or fold, that player takes the whole pot."
    },
    {
      "id": "R15",
      "text": "When a showdown happens, each remaining player's hole cards become public, and strength = 20*min(matches,3) + 30*pair + hole1 + hole2."
    },
    {
      "id": "R16",
      "text": "When counting matches, a board card counts if its value equals either hole value, and it counts once even if both hole cards share that value; for example hole 5,5 with board 5,5,2,3,8 gives matches = 2, pair = 1, strength = 40+30+10 = 80."
    },
    {
      "id": "R17",
      "text": "When matches exceeds 3, only 3 count; for example hole 2,7 with board 2,2,7,7,1 gives strength = 60+0+9 = 69."
    },
    {
      "id": "R18",
      "text": "When one player has the highest strength at showdown, that player takes the whole pot."
    },
    {
      "id": "R19",
      "text": "When k players tie for the highest strength, each receives floor(pot/k) chips and pot mod k chips stay in the pot for the next hand; for example a pot of 11 split 3 ways gives 3 each and leaves 2."
    },
    {
      "id": "R20",
      "text": "When a hand ends and a player has 0 chips, that player is eliminated (out = true) and takes no further part."
    },
    {
      "id": "R21",
      "text": "When hand 15 ends, the game ends."
    },
    {
      "id": "R22",
      "text": "When only one player is not eliminated at the end of a hand, the game ends at once."
    },
    {
      "id": "R23",
      "text": "When the game ends, the player with the most chips wins, and players tied for the most chips share the win."
    }
  ],
  "offers": [
    {
      "question": "Flop bet",
      "who": "every player with in_hand = true",
      "options": "a whole number from 0 to min(4, chips); a player with 0 chips (all-in) may only bet 0"
    },
    {
      "question": "Flop call or fold",
      "who": "every player with in_hand = true whose bet is less than high_bet",
      "options": "call, fold; players whose bet equals high_bet, folded players and eliminated players are not asked"
    },
    {
      "question": "River bet",
      "who": "every player with in_hand = true, only when 2 or more players remain",
      "options": "a whole number from 0 to min(4, chips); a player with 0 chips may only bet 0"
    },
    {
      "question": "River call or fold",
      "who": "every player with in_hand = true whose river bet is less than high_bet, only when 2 or more players remain",
      "options": "call, fold; everyone else is not asked"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggests 4, so it is kept. The minimum is 3 because with 2 players simultaneous betting is a pure guess against one rival, and 3 or more make folding and calling a reading of several opponents. The maximum is 5 because 10 hole cards and 5 board cards already use half the 32-card deck, and more seats dilute each bet's effect on the pot."
    },
    {
      "what": "No pre-bet talk step",
      "why": "The rules contain no table talk. Adding it would add a mechanic, and the bluffing already lives in the simultaneous bet sizes."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player bets according to their likely matches against the 3 shown board cards and pair potential. They read big bets as strength, fold weak hands when H is high, and use the carried-over pot and opponents' short stacks (who are forced all-in) to decide when calling is worth it."
    },
    {
      "what": "The call cost is computed against the player's current-round bet",
      "why": "The rules say a caller pays 'the difference so their bet equals H'. Bets reset between the flop and river rounds, since each is a separate betting round."
    },
    {
      "what": "A player at 0 chips bets 0 and calls for 0",
      "why": "The rules cap bets at the stack and let an all-in caller stay in, so a 0-chip player stays in at no cost."
    },
    {
      "what": "No side pots",
      "why": "The rules give the whole pot to the highest strength, including an all-in player, so no side pots are created."
    }
  ],
  "simplifications": [
    {
      "what": "'Skip to step 10' is done with a 'when in_hand_count >= 2' condition on each turn, river and showdown step instead of a jump",
      "why": "The step list is flat. Per-step arithmetic conditions give the same result."
    },
    {
      "what": "Revealing hole cards at showdown is done by copying hole into a public shown_hole list",
      "why": "Hole cards are owner-only, so a public copy is how the engine reveals them to everyone."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: chips, out, shown_hole; table: board_shown, pot, hand_no.
````

## Reply

````
```json
[
  {
    "name": "Start: 40 chips each, pot 0, nobody out",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"chips": 40, "out": false},
        "2": {"chips": 40, "out": false},
        "3": {"chips": 40, "out": false}
      },
      "game": {"pot": 0, "hand_no": 0}
    }
  },
  {
    "name": "Ante: seat with 5 goes to 4; others fold to seat 2's bet",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"chips": 5}}},
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "players": {
        "1": {"chips": 4},
        "2": {"chips": 42},
        "3": {"chips": 39}
      },
      "game": {"pot": 0, "hand_no": 1}
    }
  },
  {
    "name": "Player with 1 chip antes to 0 and stays in to showdown (pot 4 splits evenly, chance-independent)",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"chips": 1}}},
    "rules": [
      {"seat": 1, "options_include": "call"},
      {"seat": 2, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "call"}],
      "lens": {"players": {"1": {"shown_hole": 2}, "3": {"shown_hole": 0}}},
      "players": {"3": {"chips": 39}},
      "game": {"pot": 0}
    }
  },
  {
    "name": "Deal: 2 hole cards each, 5 board, deck left with 21 (chance-independent counts)",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "lens": {
        "game": {"deck": 21, "board": 5},
        "players": {"1": {"hole": 2}, "2": {"hole": 2}, "3": {"hole": 2}}
      }
    }
  },
  {
    "name": "Flop reveals exactly 3 board cards (hand ends at flop)",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 2},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "lens": {"game": {"board_shown": 3}},
      "players": {
        "1": {"chips": 39},
        "2": {"chips": 42},
        "3": {"chips": 39}
      }
    }
  },
  {
    "name": "Bet capped by chips and moves from chips to pot",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"chips": 3}}},
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": 2},
        {"seat": 2, "option": 4}
      ],
      "not_offered": [
        {"seat": 1, "option": 3},
        {"seat": 2, "option": 5}
      ],
      "players": {
        "1": {"chips": 0, "out": true},
        "2": {"chips": 44},
        "3": {"chips": 39}
      },
      "game": {"pot": 0}
    }
  },
  {
    "name": "Only players below H are asked to call or fold",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 3},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 1},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "offered": [{"seat": 3, "option": "call"}],
      "not_offered": [
        {"seat": 1, "option": "call"},
        {"seat": 2, "option": "call"},
        {"seat": 1, "option": "fold"},
        {"seat": 2, "option": "fold"}
      ],
      "players": {"3": {"chips": 38}},
      "game": {"pot": 0}
    }
  },
  {
    "name": "Bet 1 against H=4: call pays 3 more",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 1, "options_include": "call"},
      {"seat": 1, "options_include": 0},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 4},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": 4},
      {"seat": 3, "options_include": 1}
    ],
    "expect": {
      "players": {"1": {"chips": 35, "out": false}},
      "lens": {"players": {"1": {"shown_hole": 0}}}
    }
  },
  {
    "name": "Short call pays all chips and stays in to showdown (chance-independent)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"chips": 3}}},
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 1, "options_include": "call"},
      {"seat": 2, "options_include": 4},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 4},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "call"}],
      "lens": {
        "players": {
          "1": {"shown_hole": 2},
          "2": {"shown_hole": 2},
          "3": {"shown_hole": 2}
        },
        "game": {"board_shown": 5}
      }
    }
  },
  {
    "name": "Fold leaves the hand, bet chips are lost",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 3},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 3},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"chips": 37}},
      "lens": {
        "players": {
          "1": {"shown_hole": 0},
          "2": {"shown_hole": 2},
          "3": {"shown_hole": 2}
        }
      }
    }
  },
  {
    "name": "Last player after flop takes the pot; no turn or river",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "players": {
        "1": {"chips": 42},
        "2": {"chips": 39},
        "3": {"chips": 39}
      },
      "game": {"pot": 0},
      "lens": {
        "game": {"board_shown": 3},
        "players": {"1": {"shown_hole": 0}}
      }
    }
  },
  {
    "name": "Two remain after flop: all 5 board cards shown",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 2},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 1},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "lens": {"game": {"board_shown": 5}},
      "players": {"3": {"chips": 38}},
      "game": {"pot": 0}
    }
  },
  {
    "name": "River betting: fresh bets, chips to pot, fold loses river bet",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 1, "options_include": 1},
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 4},
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": 4},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": "call"}],
      "not_offered": [
        {"seat": 2, "option": "call"},
        {"seat": 3, "option": "call"}
      ],
      "players": {"1": {"chips": 34}},
      "game": {"pot": 0}
    }
  },
  {
    "name": "Last player after river takes the pot without showdown",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 0, "times": 2},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": 0, "times": 2},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "players": {
        "1": {"chips": 42},
        "2": {"chips": 39},
        "3": {"chips": 39}
      },
      "game": {"pot": 0},
      "lens": {
        "game": {"board_shown": 5},
        "players": {"1": {"shown_hole": 0}}
      }
    }
  },
  {
    "name": "Showdown reveals every remaining hole (chance-independent counts)",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"pot": 3}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 2},
      {"seat": 2, "options_include": 0, "times": 2},
      {"seat": 3, "options_include": 0, "times": 2}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"shown_hole": 2},
          "2": {"shown_hole": 2},
          "3": {"shown_hole": 2}
        },
        "game": {"board_shown": 5}
      },
      "game": {"pot": 0}
    }
  },
  {
    "name": "Two-way showdown with even pot 8 empties the pot (chance-independent)",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 2},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 1},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "lens": {
        "players": {
          "1": {"shown_hole": 2},
          "2": {"shown_hole": 2},
          "3": {"shown_hole": 0}
        }
      },
      "game": {"pot": 0}
    }
  },
  {
    "name": "Three-way showdown with pot 12 empties the pot (chance-independent)",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"pot": 9}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 2},
      {"seat": 2, "options_include": 0, "times": 2},
      {"seat": 3, "options_include": 0, "times": 2}
    ],
    "expect": {
      "game": {"pot": 0},
      "lens": {"players": {"1": {"shown_hole": 2}}}
    }
  },
  {
    "name": "Showdown pays out the pot; folded seat unchanged (chance-independent)",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 3},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 1},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "players": {"3": {"chips": 38}},
      "game": {"pot": 0}
    }
  },
  {
    "name": "Pot of 6 split among any number of 1-3 tied winners leaves 0 (chance-independent)",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"pot": 3}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 2},
      {"seat": 2, "options_include": 0, "times": 2},
      {"seat": 3, "options_include": 0, "times": 2}
    ],
    "expect": {
      "game": {"pot": 0, "hand_no": 1}
    }
  },
  {
    "name": "Player at 0 chips after the hand is eliminated",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"chips": 1}}},
    "rules": [
      {"seat": 1, "options_include": "fold"},
      {"seat": 2, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 1},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"chips": 0, "out": true},
        "2": {"out": false},
        "3": {"out": false}
      }
    }
  },
  {
    "name": "Game ends after hand 15",
    "rule": "R21",
    "players": 3,
    "given": {"game": {"hand_no": 14}},
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 42, "2": 39, "3": 39},
      "game": {"hand_no": 15}
    }
  },
  {
    "name": "Game ends at once when only one player is left",
    "rule": "R22",
    "players": 3,
    "given": {
      "players": {"2": {"chips": 1}, "3": {"chips": 1}},
      "game": {"hand_no": 3}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 42, "2": 0, "3": 0},
      "players": {
        "2": {"out": true},
        "3": {"out": true}
      },
      "game": {"hand_no": 4}
    }
  },
  {
    "name": "Tied for most chips at the end share the win",
    "rule": "R23",
    "players": 3,
    "given": {
      "players": {
        "1": {"chips": 40},
        "2": {"chips": 43},
        "3": {"chips": 20}
      },
      "game": {"hand_no": 14}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 2, "options_include": "fold"},
      {"seat": 3, "options_include": 0},
      {"seat": 3, "options_include": "fold"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 42, "2": 42, "3": 19}
    }
  }
]
```
````
