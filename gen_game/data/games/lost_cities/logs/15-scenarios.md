# 15 scenarios

- time: 2026-10-27T08:53:59+00:00 (92.9s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 30f8cb5731e6f5d7, reply sha256 7f77880be897f4c7

## Sent

````
SPEC:
{
  "name": "Lost Cities: Three Expeditions",
  "summary": "Two explorers build rising number runs in three colours, betting with wager cards and fighting over a shared discard row, while a 21-card deck runs out.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "colours": 3,
    "total_cards": 33,
    "lowest_number": 2,
    "highest_number": 10,
    "wagers_per_colour": 2,
    "hand_size": 6,
    "deck_after_deal": 21,
    "expedition_cost": 15,
    "wager_multiplier_base": 1,
    "bonus_card_count": 5,
    "bonus_points": 10,
    "max_rounds": 20,
    "max_discard_tops_per_colour": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": "6 cards dealt from deck",
        "meaning": "The cards the player holds. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "sum_r",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of the Red numbers played",
        "observable": false
      },
      {
        "key": "top_r",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest Red number played. 0 means none yet.",
        "observable": false
      },
      {
        "key": "wag_r",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red wagers played",
        "observable": false
      },
      {
        "key": "cnt_r",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cards in the Red expedition, wagers included",
        "observable": false
      },
      {
        "key": "sum_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of the Blue numbers played",
        "observable": false
      },
      {
        "key": "top_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest Blue number played. 0 means none yet.",
        "observable": false
      },
      {
        "key": "wag_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue wagers played",
        "observable": false
      },
      {
        "key": "cnt_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cards in the Blue expedition, wagers included",
        "observable": false
      },
      {
        "key": "sum_g",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total of the Green numbers played",
        "observable": false
      },
      {
        "key": "top_g",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest Green number played. 0 means none yet.",
        "observable": false
      },
      {
        "key": "wag_g",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green wagers played",
        "observable": false
      },
      {
        "key": "cnt_g",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cards in the Green expedition, wagers included",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current total score over the three colours",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 33 cards shuffled, 21 left after the deal",
        "meaning": "The face-down draw deck",
        "observable": false
      },
      {
        "key": "deck_size",
        "type": "number",
        "visible": "public",
        "initial": 21,
        "meaning": "Cards remaining in the deck. The rules show this to both players.",
        "observable": true
      },
      {
        "key": "discard_tops",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up discards, at most one per colour",
        "observable": true
      },
      {
        "key": "last_discard",
        "type": "text",
        "visible": "none",
        "initial": "none",
        "meaning": "The card discarded this turn. It cannot be drawn back on the same turn.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rounds completed",
        "observable": true
      }
    ]
  },
  "setup": [
    "Build the 33-card deck: R2-R10, B2-B10, G2-G10, and two each of RW, BW and GW.",
    "Shuffle the deck. This is the only random event in the game.",
    "Choose seat 1 at random.",
    "Deal 6 cards to each player's hand by drawing at random from deck, leaving 21 cards in deck. Set deck_size to 21.",
    "Set discard_tops to an empty list and last_discard to 'none'.",
    "Sync each player their own state."
  ],
  "round": [
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand and all public state: the expedition numbers, discard_tops and deck_size."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "answer": "one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand)",
      "effect": "On a legal PLAY of X in colour c: remove X from hand and add 1 to cnt_c. For a number, add X to sum_c and set top_c to X. For a wager, add 1 to wag_c. On DISCARD X: remove X from hand, remove any card of X's colour from discard_tops (it leaves the game), append X to discard_tops and set last_discard to X. An illegal PLAY, or a card not in hand, is treated as DISCARD of the first card in hand."
    },
    {
      "action": "ask",
      "who": "seat 1",
      "answer": "'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard",
      "effect": "DECK: draw a random card from deck into hand and subtract 1 from deck_size. A named card: move it from discard_tops to hand. An invalid answer, or naming last_discard, means DECK. If deck is empty and no eligible discard exists, nothing is drawn. Then set last_discard to 'none'."
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "effect": "Announce the card played or discarded, what was drawn (deck or the named discard), and the new deck_size and discard_tops."
    },
    {
      "action": "sync",
      "who": "seat 2",
      "answer": null,
      "effect": "Seat 2 sees their updated state."
    },
    {
      "action": "ask",
      "who": "seat 2",
      "answer": "one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand)",
      "effect": "Same as seat 1's play or discard step."
    },
    {
      "action": "ask",
      "who": "seat 2",
      "answer": "'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard",
      "effect": "Same as seat 1's draw step. Then set last_discard to 'none'."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player and each colour c: if cnt_c = 0 the colour scores 0, otherwise it scores (sum_c - 15) * (1 + wag_c), plus 10 if cnt_c >= 5. Set score to the total of the three colours. Add 1 to round. Announce both scores."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if deck_size = 0 or round >= 20. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "deck_size == 0 or round >= 20 (checked at the end of a round, after seat 2's turn)",
    "rank_by": "you.score",
    "decided_by": "The player with the higher score wins. If the scores are equal, both share the result, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, the deck has 33 cards (numbers 2-10 in R, B and G, plus two wagers per colour), each player is dealt 6 cards, and 21 remain in deck."
    },
    {
      "id": "R2",
      "text": "When the game starts, seat 1 is chosen at random, and each round seat 1 takes a full turn and then seat 2 does."
    },
    {
      "id": "R3",
      "text": "When a player PLAYs a number X of colour c with X > top_c, then X leaves the hand, cnt_c rises by 1, sum_c rises by X and top_c becomes X."
    },
    {
      "id": "R4",
      "text": "When a player PLAYs a wager of colour c while top_c = 0, then it leaves the hand, cnt_c rises by 1 and wag_c rises by 1."
    },
    {
      "id": "R5",
      "text": "When a player attempts a PLAY of a number X <= top_c, or of a wager while top_c > 0, or of a card not in hand, then it is treated as DISCARD of the first card in hand."
    },
    {
      "id": "R6",
      "text": "When a player DISCARDs X, then X leaves the hand, any card of X's colour already in discard_tops is removed from the game, X is appended to discard_tops, and last_discard becomes X."
    },
    {
      "id": "R7",
      "text": "When a player draws DECK and the deck is not empty, then one card moves from deck to hand and deck_size falls by 1."
    },
    {
      "id": "R8",
      "text": "When a player names a card in discard_tops other than last_discard, then that card moves from discard_tops to hand."
    },
    {
      "id": "R9",
      "text": "When a player gives an invalid draw answer or names last_discard, then they draw from DECK."
    },
    {
      "id": "R10",
      "text": "When the deck is empty, then the player must take a card from discard_tops other than last_discard, and if none exists they draw nothing."
    },
    {
      "id": "R11",
      "text": "When a draw step ends, then last_discard is reset to 'none'."
    },
    {
      "id": "R12",
      "text": "When a round ends and a colour has cnt_c = 0, then it scores 0."
    },
    {
      "id": "R13",
      "text": "When a round ends and a colour has cnt_c >= 1, then it scores (sum_c - 15) * (1 + wag_c), so one wager with numbers totalling 20 scores 10."
    },
    {
      "id": "R14",
      "text": "When a round ends and a colour has cnt_c >= 5, then it scores an extra 10 points."
    },
    {
      "id": "R15",
      "text": "When a round ends, then each player's score is the sum of their three colour scores."
    },
    {
      "id": "R16",
      "text": "When a round ends with deck_size = 0, then the game ends, and seat 2 always completes the round first."
    },
    {
      "id": "R17",
      "text": "When round 20 ends, then the game ends."
    },
    {
      "id": "R18",
      "text": "When the game ends, then the higher score wins, and equal scores are a draw."
    }
  ],
  "offers": [
    {
      "question": "Play or discard",
      "who": "the active seat (seat 1, then seat 2)",
      "options": "'DISCARD X' for every card X in hand. 'PLAY X' for every number X in hand greater than top_c of its colour, and for every wager in hand whose colour has top_c = 0."
    },
    {
      "question": "Draw",
      "who": "the active seat",
      "options": "If deck is not empty: 'DECK' plus every card in discard_tops except last_discard. If deck is empty: every card in discard_tops except last_discard. If deck is empty and none exist: 'NOTHING' only."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed 2 players. The game is a duel over a shared discard row: what you discard feeds your one opponent."
    },
    {
      "what": "No talk step",
      "why": "The rules have no communication, and the game is a pure two-player contest of hand management and denial."
    },
    {
      "what": "Only legal plays are offered",
      "why": "A seat is never offered what it may not do. The fallback rule (an illegal play becomes a discard of the first card in hand) is kept for malformed answers."
    },
    {
      "what": "Public deck_size counter",
      "why": "The rules say both players see how many cards remain, while the deck itself stays hidden."
    },
    {
      "what": "Public round counter",
      "why": "Needed to apply the 20-round limit arithmetically."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player commits only to colours they can reach 15+ in, times wagers before the numbers, avoids discarding cards the opponent needs, and watches the deck count to judge how much longer the game runs."
    }
  ],
  "simplifications": [
    {
      "what": "Taking the top card of the deck is a random pick from the deck list",
      "why": "The deck is shuffled, so a random draw is equivalent and keeps the match seed-reproducible."
    },
    {
      "what": "Each seat's turn is written as explicit seat 1 and seat 2 steps",
      "why": "The step list is flat. This keeps both players' turns equal within a round."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: deck_size, discard_tops, round.
````

## Reply

````
[
{"name": "Setup: 6 cards each, 21 left in deck, empty discard row", "rule": "R1", "players": 2, "seed": 1, "rounds": 0,
 "expect": {"game": {"deck_size": 21, "round": 0, "discard_tops": []},
            "lens": {"game": {"deck": 21}, "players": {"1": {"hand": 6}, "2": {"hand": 6}}}}},

{"name": "Seat 1 takes its turn before seat 2, so seat 2 can pick up seat 1's discard", "rule": "R2", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R4", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R4"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD B3"}, {"seat": 2, "options_include": "R4"}],
 "expect": {"offered": [{"seat": 2, "option": "R4"}],
            "game": {"discard_tops": ["B3"], "deck_size": 3, "round": 1},
            "players": {"1": {"score": 0}, "2": {"score": 0}}}},

{"name": "Playing a higher red number adds it to the red run; lower numbers not offered", "rule": "R3", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R5", "R2", "B2"], "top_r": 3, "sum_r": 3, "cnt_r": 1}, "2": {"hand": ["G2", "B3", "G6"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "PLAY R5"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G2"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"offered": [{"seat": 1, "option": "PLAY R5"}],
            "not_offered": [{"seat": 1, "option": "PLAY R2"}],
            "players": {"1": {"score": -7}, "2": {"score": 0}},
            "game": {"deck_size": 2, "discard_tops": ["G2"]}}},

{"name": "A wager on an empty colour doubles its (negative) score; wager on a started colour not offered", "rule": "R4", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["RW", "BW", "R6"], "top_b": 4, "sum_b": 4, "cnt_b": 1}, "2": {"hand": ["G2", "B3", "G6"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "PLAY RW"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G2"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"offered": [{"seat": 1, "option": "PLAY RW"}],
            "not_offered": [{"seat": 1, "option": "PLAY BW"}],
            "players": {"1": {"score": -41}, "2": {"score": 0}}}},

{"name": "Illegal plays (low number, late wager) are never offered; the legal play is", "rule": "R5", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R3", "R8", "BW"], "top_r": 5, "sum_r": 5, "cnt_r": 1, "top_b": 2, "sum_b": 2, "cnt_b": 1}, "2": {"hand": ["G2", "B3", "G6"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "PLAY R8"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G2"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"offered": [{"seat": 1, "option": "PLAY R8"}, {"seat": 1, "option": "DISCARD R3"}],
            "not_offered": [{"seat": 1, "option": "PLAY R3"}, {"seat": 1, "option": "PLAY BW"}],
            "players": {"1": {"score": -15}, "2": {"score": 0}}}},

{"name": "Discarding replaces the same colour's discard and appends to the row", "rule": "R6", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": ["R4", "B5"]}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"game": {"discard_tops": ["B5", "R9", "G3"], "deck_size": 2}}},

{"name": "Drawing from the deck moves one card to hand and lowers deck_size", "rule": "R7", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"game": {"deck_size": 2, "discard_tops": ["R9", "G3"]},
            "lens": {"game": {"deck": 2}, "players": {"1": {"hand": 3}, "2": {"hand": 3}}}}},

{"name": "Naming a discard top takes it into hand", "rule": "R8", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": ["B5"]}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "B5"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"game": {"discard_tops": ["R9", "G3"], "deck_size": 3},
            "lens": {"players": {"1": {"hand": 3}}}}},

{"name": "Naming the card just discarded draws from the deck instead", "rule": "R9", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "answer": "R9"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"game": {"discard_tops": ["R9", "G3"], "deck_size": 2},
            "lens": {"players": {"1": {"hand": 3}}}}},

{"name": "With an empty deck the draw must come from the discard row, excluding one's own discard", "rule": "R10", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": [], "deck_size": 0, "discard_tops": ["B5"]}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "B5"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "R9"}],
 "expect": {"offered": [{"seat": 1, "option": "B5"}, {"seat": 2, "option": "R9"}],
            "not_offered": [{"seat": 1, "option": "DECK"}, {"seat": 2, "option": "DECK"}],
            "game": {"discard_tops": ["G3"], "deck_size": 0},
            "players": {"1": {"score": 0}, "2": {"score": 0}}}},

{"name": "last_discard resets after seat 1's draw, so seat 2 may take seat 1's discard", "rule": "R11", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"]}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "PLAY G3"}, {"seat": 2, "options_include": "R9"}],
 "expect": {"offered": [{"seat": 2, "option": "R9"}],
            "game": {"discard_tops": [], "deck_size": 3},
            "players": {"1": {"score": 0}, "2": {"score": -12}}}},

{"name": "Colours with no cards score 0; only the started colour counts", "rule": "R12", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"], "sum_b": 20, "top_b": 10, "cnt_b": 2}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "R7", "R8"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"players": {"1": {"score": 5}, "2": {"score": 0}}}},

{"name": "One wager with numbers totalling 20 scores 10", "rule": "R13", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["B2", "G4", "B6"], "sum_r": 20, "top_r": 9, "cnt_r": 4, "wag_r": 1}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD B2"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"players": {"1": {"score": 10}, "2": {"score": 0}}}},

{"name": "Fifth card in an expedition adds the 10-point bonus", "rule": "R14", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R6", "B2", "G4"], "sum_r": 14, "top_r": 5, "cnt_r": 4, "wag_r": 0}, "2": {"hand": ["G3", "B3", "R7"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "PLAY R6"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"players": {"1": {"score": 15}, "2": {"score": 0}}}},

{"name": "Score is the sum of the three colour scores", "rule": "R15", "players": 2, "seed": 1, "rounds": 1,
 "given": {"players": {"1": {"hand": ["R2", "B2", "G2"], "sum_r": 20, "top_r": 10, "cnt_r": 2, "sum_b": 10, "top_b": 10, "cnt_b": 1, "sum_g": 18, "top_g": 10, "cnt_g": 3, "wag_g": 1},
                       "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["R7", "B7", "G7", "R6"], "deck_size": 4, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R2"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"players": {"1": {"score": 6}, "2": {"score": 0}}}},

{"name": "Seat 1 empties the deck, seat 2 still finishes the round, then the game ends", "rule": "R16", "players": 2, "seed": 1,
 "given": {"players": {"1": {"hand": ["R9", "B2", "G4"], "sum_b": 20, "top_b": 10, "cnt_b": 2}, "2": {"hand": ["G9", "B3", "R3"]}},
           "game": {"deck": ["G10"], "deck_size": 1, "discard_tops": []}},
 "rules": [{"seat": 1, "options_include": "DISCARD R9"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "PLAY G9"}, {"seat": 2, "options_include": "R9"}],
 "expect": {"winner": 1,
            "standings": {"1": 5, "2": -6},
            "players": {"1": {"score": 5}, "2": {"score": -6}},
            "game": {"deck_size": 0, "round": 1, "discard_tops": []}}},

{"name": "The game ends after round 20 even with cards left", "rule": "R17", "players": 2, "seed": 1,
 "given": {"players": {"1": {"hand": ["R2", "B2", "G4"], "sum_r": 20, "top_r": 10, "cnt_r": 2}, "2": {"hand": ["G3", "B3", "R3"]}},
           "game": {"deck": ["G9", "G10", "B9", "B10", "B8", "G8", "B7", "G7", "B6", "G6"], "deck_size": 10, "discard_tops": [], "round": 19}},
 "rules": [{"seat": 1, "options_include": "DISCARD B2"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"winner": 1,
            "standings": {"1": 5, "2": 0},
            "game": {"round": 20, "deck_size": 8}}},

{"name": "Equal final scores are shared", "rule": "R18", "players": 2, "seed": 1,
 "given": {"players": {"1": {"hand": ["R2", "B2", "G4"], "sum_r": 20, "top_r": 10, "cnt_r": 2}, "2": {"hand": ["G3", "B3", "R3"], "sum_b": 20, "top_b": 10, "cnt_b": 2}},
           "game": {"deck": ["G9", "G10", "B9", "R9"], "deck_size": 4, "discard_tops": [], "round": 19}},
 "rules": [{"seat": 1, "options_include": "DISCARD B2"}, {"seat": 1, "options_include": "DECK", "times": "all"},
           {"seat": 2, "options_include": "DISCARD G3"}, {"seat": 2, "options_include": "DECK", "times": "all"}],
 "expect": {"winner": [1, 2],
            "standings": {"1": 5, "2": 5},
            "game": {"round": 20}}}
]
````
