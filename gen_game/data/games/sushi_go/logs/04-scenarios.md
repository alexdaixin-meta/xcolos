# 04 scenarios

- time: 2026-10-27T16:40:59+00:00 (106.9s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 1a30c910f22126d8, reply sha256 591874c7433c78c8

## Sent

````
SPEC:
{
  "name": "Sushi Draft",
  "summary": "A card-drafting game: each round every player secretly keeps one card from the hand they hold and passes the rest left. Sets of sushi score at the end of each of 3 hands, and puddings score at the end of the game.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 104,
    "count_tempura": 14,
    "count_sashimi": 14,
    "count_dumpling": 14,
    "count_maki_1": 6,
    "count_maki_2": 12,
    "count_maki_3": 8,
    "count_salmon_nigiri": 10,
    "count_squid_nigiri": 5,
    "count_egg_nigiri": 5,
    "count_pudding": 10,
    "count_wasabi": 6,
    "hands_per_game": 3,
    "hand_size_3_players": 9,
    "hand_size_4_players": 8,
    "rounds_3_players": 27,
    "rounds_4_players": 24,
    "maki_icons_1": 1,
    "maki_icons_2": 2,
    "maki_icons_3": 3,
    "egg_value": 1,
    "salmon_value": 2,
    "squid_value": 3,
    "wasabi_multiplier": 3,
    "tempura_set_size": 2,
    "tempura_set_points": 5,
    "sashimi_set_size": 3,
    "sashimi_set_points": 10,
    "dumpling_points_0": 0,
    "dumpling_points_1": 1,
    "dumpling_points_2": 3,
    "dumpling_points_3": 6,
    "dumpling_points_4": 10,
    "dumpling_points_5_plus": 15,
    "maki_first_points": 6,
    "maki_second_points": 3,
    "pudding_most_points": 6,
    "pudding_fewest_points": -6,
    "starting_score": 0,
    "starting_puddings": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total points so far.",
        "observable": true
      },
      {
        "key": "puddings",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Pudding cards collected. Kept across all hands.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player currently holds to pick from. Only the holder sees them.",
        "observable": false
      },
      {
        "key": "tableau",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up cards the player has chosen this hand.",
        "observable": false
      },
      {
        "key": "pick",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The card secretly chosen this round, before the reveal.",
        "observable": false
      },
      {
        "key": "tempura",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tempura taken this hand.",
        "observable": false
      },
      {
        "key": "sashimi",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sashimi taken this hand.",
        "observable": false
      },
      {
        "key": "dumplings",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Dumplings taken this hand.",
        "observable": false
      },
      {
        "key": "maki",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Maki icons taken this hand.",
        "observable": false
      },
      {
        "key": "wasabi_unused",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Wasabi taken this hand that no nigiri has been placed on yet.",
        "observable": false
      },
      {
        "key": "nigiri_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Nigiri value earned this hand, with the wasabi tripling already applied.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "the 104 cards listed in parameters, shuffled",
        "meaning": "Undealt cards. Hidden and never reshuffled.",
        "observable": false
      },
      {
        "key": "picks_per_hand",
        "type": "number",
        "visible": "public",
        "initial": "9 if 3 players, 8 if 4 players",
        "meaning": "Cards dealt per hand, which is also the number of picks per hand.",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current hand (1 to 3). It becomes 4 when the game is over.",
        "observable": true
      },
      {
        "key": "pick_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current pick within the hand, from 1 to picks_per_hand.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Build the deck list from the 104 cards (14 Tempura, 14 Sashimi, 14 Dumpling, 6 Maki-1, 12 Maki-2, 8 Maki-3, 10 Salmon Nigiri, 5 Squid Nigiri, 5 Egg Nigiri, 10 Pudding, 6 Wasabi) and shuffle it once.",
    "Set picks_per_hand to 9 with 3 players or 8 with 4 players.",
    "Every player starts with score 0, puddings 0, an empty hand, an empty tableau and all hand counts at 0.",
    "Set hand_number to 1 and pick_number to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When pick_number == 1: draw picks_per_hand cards at random from deck into each player's hand, removing each card from deck."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Announce to everyone each player's tableau, puddings and score, and the size of each hand. Show each player their own hand privately."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card name from the player's own hand",
      "effect": "When the size of hand > 1: set pick to the chosen card. No one sees another player's pick until all have answered."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When the size of hand == 1: set pick to the single card in hand automatically."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reveal: remove pick from hand, append it to tableau, and announce every player's pick to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Record pick. Tempura: tempura +1. Sashimi: sashimi +1. Dumpling: dumplings +1. Maki-1/2/3: maki +1/+2/+3. Pudding: puddings +1. Wasabi: wasabi_unused +1. Egg/Salmon/Squid Nigiri with base value v of 1, 2 or 3: if wasabi_unused >= 1, then nigiri_points += 3*v and wasabi_unused -= 1; otherwise nigiri_points += v."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Pass: each player's remaining hand moves to the player on their left (seat s gives its hand to seat s+1, and the last seat gives to seat 1)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When pick_number == picks_per_hand, add to score: floor(tempura/2)*5 + floor(sashimi/3)*10 + m*(m+1)/2 where m = min(dumplings,5) + nigiri_points. Maki: let M1 be the highest maki among players with maki >= 1, and k1 the number of players with maki == M1; each of them gains floor(6/k1). If k1 == 1, let M2 be the highest maki >= 1 below M1, and k2 the number of players with maki == M2; each of them gains floor(3/k2). Then set tempura, sashimi, dumplings, maki, wasabi_unused and nigiri_points to 0 and empty tableau. Puddings stay."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When pick_number == picks_per_hand and hand_number == 3, and not all players have equal puddings: players with puddings == max split +6, each gaining floor(6/count). Players with puddings == min (0 counts as fewest) split -6, each gaining -floor(6/count)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Advance: pick_number += 1. If pick_number > picks_per_hand, set pick_number to 1 and hand_number += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if hand_number > 3; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "hand_number > 3",
    "rank_by": "you.score * 100 + you.puddings",
    "decided_by": "Highest score wins. Among players tied on score, the one with the most puddings wins. Players still tied share the win, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, the 104-card deck is shuffled once, and every player has score 0 and puddings 0."
    },
    {
      "id": "R2",
      "text": "When pick_number is 1, each player is dealt 9 cards (3 players) or 8 cards (4 players) from the deck into their hand, and those cards leave the deck."
    },
    {
      "id": "R3",
      "text": "Undealt cards stay in the hidden deck and are never reshuffled."
    },
    {
      "id": "R4",
      "text": "When a pick is made, all players choose at the same time, and no player sees another's choice until all have chosen."
    },
    {
      "id": "R5",
      "text": "When a player's hand holds exactly 1 card, that card is picked automatically, without a question."
    },
    {
      "id": "R6",
      "text": "When picks are revealed, each picked card leaves its owner's hand and is added face up to their tableau."
    },
    {
      "id": "R7",
      "text": "When Tempura is picked, tempura +1. When Sashimi is picked, sashimi +1. When Dumpling is picked, dumplings +1."
    },
    {
      "id": "R8",
      "text": "When Maki-1, Maki-2 or Maki-3 is picked, maki increases by 1, 2 or 3."
    },
    {
      "id": "R9",
      "text": "When Pudding is picked, puddings +1, and puddings are never reset between hands."
    },
    {
      "id": "R10",
      "text": "When Wasabi is picked, wasabi_unused +1."
    },
    {
      "id": "R11",
      "text": "When a nigiri is picked with wasabi_unused 0, nigiri_points increases by 1 (Egg), 2 (Salmon) or 3 (Squid)."
    },
    {
      "id": "R12",
      "text": "When a nigiri is picked with wasabi_unused >= 1, nigiri_points increases by 3 (Egg), 6 (Salmon) or 9 (Squid), and wasabi_unused decreases by 1."
    },
    {
      "id": "R13",
      "text": "When picks are recorded, each player's remaining hand passes to the player on their left."
    },
    {
      "id": "R14",
      "text": "When a hand ends, each player gains floor(tempura/2)*5 points (for example, 3 tempura gives 5)."
    },
    {
      "id": "R15",
      "text": "When a hand ends, each player gains floor(sashimi/3)*10 points (for example, 5 sashimi gives 10)."
    },
    {
      "id": "R16",
      "text": "When a hand ends, dumplings score 0/1/3/6/10/15 for 0/1/2/3/4/5-or-more dumplings."
    },
    {
      "id": "R17",
      "text": "When a hand ends, each player gains their nigiri_points, and unused wasabi scores 0."
    },
    {
      "id": "R18",
      "text": "When a hand ends, the players with the highest maki total (at least 1) split 6 points, each gaining floor(6/k)."
    },
    {
      "id": "R19",
      "text": "When a hand ends and exactly one player has the highest maki, the players with the second-highest maki (at least 1) split 3 points, each gaining floor(3/k)."
    },
    {
      "id": "R20",
      "text": "When two or more players tie for the highest maki, no second-place maki points are awarded."
    },
    {
      "id": "R21",
      "text": "When a player has maki 0, they score no maki points."
    },
    {
      "id": "R22",
      "text": "When a hand ends, tempura, sashimi, dumplings, maki, wasabi_unused, nigiri_points and tableau reset, while puddings stay."
    },
    {
      "id": "R23",
      "text": "When the third hand ends, the players with the most puddings split +6, each gaining floor(6/k)."
    },
    {
      "id": "R24",
      "text": "When the third hand ends, the players with the fewest puddings (0 counts as fewest) split -6, rounded toward zero (two tied players get -3 each)."
    },
    {
      "id": "R25",
      "text": "When the third hand ends and all players have equal puddings, nobody scores for pudding."
    },
    {
      "id": "R26",
      "text": "When the last pick of the third hand is done (pick 27 with 3 players, pick 24 with 4 players), the game ends."
    },
    {
      "id": "R27",
      "text": "When the game ends, the highest score wins, ties are broken by most puddings, and players still tied share the win."
    }
  ],
  "offers": [
    {
      "question": "Pick: choose one card from your hand",
      "who": "all players, when their hand holds 2 or more cards",
      "options": "each distinct card name currently in that player's own hand"
    },
    {
      "question": "Pick when the hand holds 1 card",
      "who": "no one is asked",
      "options": "none: the single card is taken automatically"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer suggests 4, and hand sizes are defined only for 3 and 4. At 3, passing still creates drafting tension. Above 4 the rules give no hand size."
    },
    {
      "what": "No talk phase",
      "why": "The source says there is no talk phase. Drafting is decided by reading the visible tableaus and passed hands."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player tracks what others are collecting and what will come back around, denies key cards to rivals, times wasabi before high nigiri, and weighs the pudding race against points in each hand."
    },
    {
      "what": "Tie-break encoded as score*100 + puddings",
      "why": "There are at most 10 puddings, so puddings can never outweigh one point of score. Players still tied share the win, matching the source's draw."
    },
    {
      "what": "Dumpling table written as m*(m+1)/2 with m = min(dumplings,5)",
      "why": "This gives exactly 0, 1, 3, 6, 10, 15 and is pure arithmetic."
    }
  ],
  "simplifications": [
    {
      "what": "The left neighbour is the next seat number, wrapping to seat 1",
      "why": "The engine has no physical seating."
    },
    {
      "what": "Passing is done by rotating the hand lists between players in one update",
      "why": "The engine moves cards only through list operations."
    },
    {
      "what": "The automatic last pick is done as an update instead of a question",
      "why": "The rules take the single card without a choice."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, puddings; table: hand_number.
````

## Reply

````
```json
[
  {"name": "Setup: deck holds 104 cards, every score and pudding count is 0", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"score": 0, "puddings": 0}, "2": {"score": 0, "puddings": 0}, "3": {"score": 0, "puddings": 0}},
              "game": {"hand_number": 1},
              "lens": {"game": {"deck": 104}}}},

  {"name": "First pick with 3 players deals 9 each: deck 77 and 8 cards left in each hand after one pick (contents random)", "rule": "R2", "players": 3, "rounds": 1, "default": "first",
   "expect": {"game": {"hand_number": 1},
              "lens": {"game": {"deck": 77}, "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}}}},

  {"name": "First pick with 4 players deals 8 each: deck 72 and 7 cards left in each hand (contents random)", "rule": "R2", "players": 4, "rounds": 1, "default": "first",
   "expect": {"lens": {"game": {"deck": 72}, "players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}, "4": {"hand": 7}}}}},

  {"name": "Second pick deals nothing: deck stays at 77 and hands shrink to 7 (contents random)", "rule": "R3", "players": 3, "rounds": 2, "default": "first",
   "expect": {"lens": {"game": {"deck": 77}, "players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}}}}},

  {"name": "All seats are asked to pick in the same round and each pick counts", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 2},
             "players": {"1": {"hand": ["Pudding", "Wasabi"]}, "2": {"hand": ["Pudding", "Wasabi"]}, "3": {"hand": ["Pudding", "Wasabi"]}}},
   "rules": [{"seat": 1, "options_include": "Pudding"}, {"seat": 2, "options_include": "Pudding"}, {"seat": 3, "options_include": "Pudding"}],
   "expect": {"players": {"1": {"puddings": 1}, "2": {"puddings": 1}, "3": {"puddings": 1}},
              "offered": [{"seat": 1, "option": "Pudding"}, {"seat": 2, "option": "Pudding"}, {"seat": 3, "option": "Pudding"}]}},

  {"name": "A single-card hand is picked automatically", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"hand": ["Pudding"]}, "2": {"hand": ["Wasabi"]}, "3": {"hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"puddings": 1, "score": 0}, "2": {"puddings": 0}, "3": {"puddings": 0}},
              "game": {"hand_number": 2}}},

  {"name": "The picked card leaves the hand: 3-card hands become 2-card hands", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 2},
             "players": {"1": {"hand": ["Pudding", "Wasabi", "Tempura"]}, "2": {"hand": ["Pudding", "Wasabi", "Tempura"]}, "3": {"hand": ["Pudding", "Wasabi", "Tempura"]}}},
   "rules": [{"seat": 1, "options_include": "Pudding"}, {"seat": 2, "options_include": "Pudding"}, {"seat": 3, "options_include": "Pudding"}],
   "expect": {"players": {"1": {"puddings": 1}, "2": {"puddings": 1}, "3": {"puddings": 1}},
              "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 2}, "3": {"hand": 2}}}}},

  {"name": "Tempura, Sashimi and Dumpling picks count toward the hand-end score", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"tempura": 1, "hand": ["Tempura"]}, "2": {"sashimi": 2, "hand": ["Sashimi"]}, "3": {"dumplings": 2, "hand": ["Dumpling"]}}},
   "expect": {"players": {"1": {"score": 5}, "2": {"score": 10}, "3": {"score": 6}}}},

  {"name": "Maki-3 adds 3 icons and Maki-1 adds 1 icon", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"maki": 0, "hand": ["Maki-3"]}, "2": {"maki": 2, "hand": ["Wasabi"]}, "3": {"maki": 0, "hand": ["Maki-1"]}}},
   "expect": {"players": {"1": {"score": 6}, "2": {"score": 3}, "3": {"score": 0}}}},

  {"name": "A pudding pick adds 1 and puddings survive the end of a hand", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"puddings": 2, "hand": ["Pudding"]}, "2": {"hand": ["Wasabi"]}, "3": {"hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"puddings": 3, "score": 0}}, "game": {"hand_number": 2}}},

  {"name": "Wasabi picked first triples the Squid Nigiri that arrives on the next pick", "rule": "R10", "players": 3, "rounds": 2,
   "given": {"game": {"hand_number": 1, "pick_number": 8},
             "players": {"1": {"hand": ["Wasabi", "Tempura"]}, "2": {"hand": ["Pudding", "Tempura"]}, "3": {"hand": ["Pudding", "Squid Nigiri"]}}},
   "rules": [{"seat": 1, "options_include": "Wasabi"}, {"seat": 2, "options_include": "Pudding"}, {"seat": 3, "options_include": "Pudding"}],
   "expect": {"players": {"1": {"score": 9}, "2": {"score": 0, "puddings": 1}, "3": {"score": 0, "puddings": 1}}}},

  {"name": "Nigiri without wasabi score 1, 2 and 3", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"hand": ["Egg Nigiri"]}, "2": {"hand": ["Salmon Nigiri"]}, "3": {"hand": ["Squid Nigiri"]}}},
   "expect": {"players": {"1": {"score": 1}, "2": {"score": 2}, "3": {"score": 3}}}},

  {"name": "Nigiri on wasabi score triple (Salmon 6, Egg 3, Squid 9)", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"wasabi_unused": 1, "hand": ["Salmon Nigiri"]}, "2": {"wasabi_unused": 1, "hand": ["Egg Nigiri"]}, "3": {"wasabi_unused": 2, "hand": ["Squid Nigiri"]}}},
   "expect": {"players": {"1": {"score": 6}, "2": {"score": 3}, "3": {"score": 9}}}},

  {"name": "Hands pass left: seat 1's leftover Pudding reaches seat 2", "rule": "R13", "players": 3, "rounds": 2,
   "given": {"game": {"hand_number": 1, "pick_number": 8},
             "players": {"1": {"hand": ["Pudding", "Tempura"]}, "2": {"hand": ["Wasabi", "Tempura"]}, "3": {"hand": ["Wasabi", "Tempura"]}}},
   "rules": [{"seat": 1, "options_include": "Tempura"}, {"seat": 2, "options_include": "Tempura"}, {"seat": 3, "options_include": "Tempura"}],
   "expect": {"players": {"1": {"puddings": 0, "score": 0}, "2": {"puddings": 1, "score": 0}, "3": {"puddings": 0, "score": 0}}}},

  {"name": "Tempura: 3 gives 5, 4 gives 10, 1 gives 0", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"tempura": 2, "hand": ["Tempura"]}, "2": {"tempura": 3, "hand": ["Tempura"]}, "3": {"tempura": 0, "hand": ["Tempura"]}}},
   "expect": {"players": {"1": {"score": 5}, "2": {"score": 10}, "3": {"score": 0}}}},

  {"name": "Sashimi: 5 gives 10, 6 gives 20, 2 gives 0", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"sashimi": 4, "hand": ["Sashimi"]}, "2": {"sashimi": 5, "hand": ["Sashimi"]}, "3": {"sashimi": 1, "hand": ["Sashimi"]}}},
   "expect": {"players": {"1": {"score": 10}, "2": {"score": 20}, "3": {"score": 0}}}},

  {"name": "Dumplings: 1 gives 1, 2 gives 3, 4 gives 10, 6 gives 15", "rule": "R16", "players": 4, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 8},
             "players": {"1": {"dumplings": 0, "hand": ["Dumpling"]}, "2": {"dumplings": 3, "hand": ["Dumpling"]}, "3": {"dumplings": 5, "hand": ["Dumpling"]}, "4": {"dumplings": 1, "hand": ["Dumpling"]}}},
   "expect": {"players": {"1": {"score": 1}, "2": {"score": 10}, "3": {"score": 15}, "4": {"score": 3}}}},

  {"name": "Nigiri points are added at hand end and unused wasabi scores 0", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"nigiri_points": 7, "wasabi_unused": 2, "hand": ["Tempura"]}, "2": {"wasabi_unused": 1, "hand": ["Wasabi"]}, "3": {"nigiri_points": 4, "hand": ["Tempura"]}}},
   "expect": {"players": {"1": {"score": 7}, "2": {"score": 0}, "3": {"score": 4}}}},

  {"name": "Lone maki leader gains 6 and the runner-up 3", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"maki": 4, "hand": ["Wasabi"]}, "2": {"maki": 2, "hand": ["Wasabi"]}, "3": {"maki": 0, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 6}, "2": {"score": 3}, "3": {"score": 0}}}},

  {"name": "Three players tied for top maki gain 2 each", "rule": "R18", "players": 4, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 8},
             "players": {"1": {"maki": 5, "hand": ["Wasabi"]}, "2": {"maki": 5, "hand": ["Wasabi"]}, "3": {"maki": 5, "hand": ["Wasabi"]}, "4": {"maki": 2, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 2}, "4": {"score": 0}}}},

  {"name": "Two players tied for second maki gain 1 each", "rule": "R19", "players": 4, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 8},
             "players": {"1": {"maki": 6, "hand": ["Wasabi"]}, "2": {"maki": 3, "hand": ["Wasabi"]}, "3": {"maki": 3, "hand": ["Wasabi"]}, "4": {"maki": 0, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 6}, "2": {"score": 1}, "3": {"score": 1}, "4": {"score": 0}}}},

  {"name": "A tie for top maki gives 3 each and no second-place points", "rule": "R20", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"maki": 4, "hand": ["Wasabi"]}, "2": {"maki": 4, "hand": ["Wasabi"]}, "3": {"maki": 2, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 3}, "2": {"score": 3}, "3": {"score": 0}}}},

  {"name": "Seats with maki 0 get no second place even when nobody else has maki", "rule": "R21", "players": 3, "rounds": 1,
   "given": {"game": {"hand_number": 1, "pick_number": 9},
             "players": {"1": {"maki": 3, "hand": ["Wasabi"]}, "2": {"maki": 0, "hand": ["Wasabi"]}, "3": {"maki": 0, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 6}, "2": {"score": 0}, "3": {"score": 0}}}},

  {"name": "Hand counts reset between hands while puddings stay (hand 2 is dealt from an all-Tempura deck)", "rule": "R22", "players": 3, "rounds": 10, "default": "first",
   "given": {"game": {"hand_number": 1, "pick_number": 9,
                      "deck": ["Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura",
                               "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura",
                               "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura", "Tempura"]},
             "players": {"1": {"tempura": 1, "hand": ["Wasabi"]}, "2": {"dumplings": 2, "hand": ["Wasabi"]}, "3": {"puddings": 3, "hand": ["Wasabi"]}}},
   "expect": {"players": {"1": {"score": 20}, "2": {"score": 23}, "3": {"score": 20, "puddings": 3}},
              "game": {"hand_number": 3}}},

  {"name": "Two tied pudding leaders gain 3 each and the fewest loses 6; tied top seats share the win", "rule": "R23", "players": 4,
   "given": {"game": {"hand_number": 3, "pick_number": 8},
             "players": {"1": {"puddings": 3, "hand": ["Wasabi"]}, "2": {"puddings": 3, "hand": ["Wasabi"]}, "3": {"puddings": 1, "hand": ["Wasabi"]}, "4": {"puddings": 0, "hand": ["Wasabi"]}}},
   "expect": {"winner": [1, 2],
              "standings": {"1": 303, "2": 303, "3": 1, "4": -600},
              "players": {"1": {"score": 3}, "2": {"score": 3}, "3": {"score": 0}, "4": {"score": -6}}}},

  {"name": "Two seats tied for fewest puddings lose 3 each", "rule": "R24", "players": 3,
   "given": {"game": {"hand_number": 3, "pick_number": 9},
             "players": {"1": {"puddings": 5, "hand": ["Wasabi"]}, "2": {"puddings": 0, "hand": ["Wasabi"]}, "3": {"puddings": 0, "hand": ["Wasabi"]}}},
   "expect": {"winner": 1,
              "standings": {"1": 605, "2": -300, "3": -300},
              "players": {"1": {"score": 6}, "2": {"score": -3}, "3": {"score": -3}}}},

  {"name": "Equal puddings score nothing; all seats tie and share the win", "rule": "R25", "players": 3,
   "given": {"game": {"hand_number": 3, "pick_number": 9},
             "players": {"1": {"score": 10, "puddings": 2, "hand": ["Wasabi"]}, "2": {"score": 10, "puddings": 2, "hand": ["Wasabi"]}, "3": {"score": 10, "puddings": 2, "hand": ["Wasabi"]}}},
   "expect": {"winner": [1, 2, 3],
              "standings": {"1": 1002, "2": 1002, "3": 1002},
              "players": {"1": {"score": 10}, "2": {"score": 10}, "3": {"score": 10}}}},

  {"name": "The game ends after the last pick of hand 3", "rule": "R26", "players": 3,
   "given": {"game": {"hand_number": 3, "pick_number": 9},
             "players": {"1": {"score": 20, "puddings": 1, "hand": ["Wasabi"]}, "2": {"score": 10, "puddings": 1, "hand": ["Wasabi"]}, "3": {"score": 5, "puddings": 1, "hand": ["Wasabi"]}}},
   "expect": {"winner": 1,
              "standings": {"1": 2001, "2": 1001, "3": 501},
              "game": {"hand_number": 4}}},

  {"name": "A tie on score is broken by most puddings", "rule": "R27", "players": 3,
   "given": {"game": {"hand_number": 3, "pick_number": 9},
             "players": {"1": {"score": 10, "puddings": 3, "hand": ["Wasabi"]}, "2": {"score": 19, "puddings": 1, "hand": ["Wasabi"]}, "3": {"score": 13, "puddings": 1, "hand": ["Wasabi"]}}},
   "expect": {"winner": 1,
              "standings": {"1": 1603, "2": 1601, "3": 1001},
              "players": {"1": {"score": 16}, "2": {"score": 16}, "3": {"score": 10}}}}
]
```
````
