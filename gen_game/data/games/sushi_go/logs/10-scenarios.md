# 10 scenarios

- time: 2026-10-27T16:50:08+00:00 (77.4s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 7b9e46e66b202dd5, reply sha256 6e9d494f9d4e8b75

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

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Do not write scenarios that need a particular card to show up in a particular player's hand. A shuffled deal cannot guarantee that.

- **Per-card recording (tempura, sashimi, dumplings, maki icons, puddings, nigiri with wasabi):** check only what holds however the cards fall:
  - each pick moves one card from hand to the face-up area;
  - puddings never decrease and are not reset at the end of a hand;
  - scores change only at the last pick of a hand;
  - score totals agree with the scoring formulas applied to the cards each player actually took.
- **Card-specific rules:** a rule such as 'if Pudding is offered, pick it' must be optional. The scenario must not fail when that option never appears.
- **Single-card auto-pick:** assert that at the last pick of a hand (hand size 1) no choice is asked and the hand size goes to 0. Do not expect a named card to be offered.
- **Specific-card checks:** if the harness has a fixed deck order or seed, use it so the needed cards are certainly dealt. Otherwise drop those checks.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"Setup: every seat starts at score 0 and puddings 0, hand 1, full 104-card deck","rule":"R1","players":4,"rounds":0,
 "expect":{"players":{"1":{"score":0,"puddings":0},"2":{"score":0,"puddings":0},"3":{"score":0,"puddings":0},"4":{"score":0,"puddings":0}},
 "game":{"hand_number":1},"lens":{"game":{"deck":104}}}},

{"name":"Deal with 4 players: 8 cards each leave the deck (72 left), one picked so 7 remain in hand","rule":"R2","players":4,"rounds":1,"default":"first",
 "expect":{"lens":{"game":{"deck":72},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7},"4":{"hand":7}}}}},

{"name":"Deal with 3 players: 9 cards each leave the deck (77 left), one picked so 8 remain in hand","rule":"R2","players":3,"rounds":1,"default":"first",
 "expect":{"lens":{"game":{"deck":77},"players":{"1":{"hand":8},"2":{"hand":8},"3":{"hand":8}}}}},

{"name":"Deck is not reshuffled: after a full hand and the next deal, 104-32-32=40 cards remain","rule":"R3","players":4,"rounds":9,"default":"first",
 "expect":{"game":{"hand_number":2},"lens":{"game":{"deck":40},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7},"4":{"hand":7}}}}},

{"name":"Every seat is asked to pick from its own hand only","rule":"R4","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":2,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura","Pudding"]},"2":{"hand":["Pudding","Sashimi"]},"3":{"hand":["Pudding","Dumpling"]},"4":{"hand":["Pudding","Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Pudding"},{"seat":2,"options_include":"Pudding"},{"seat":3,"options_include":"Pudding"},{"seat":4,"options_include":"Pudding"}],
 "expect":{"players":{"1":{"puddings":1,"score":0},"2":{"puddings":1,"score":0},"3":{"puddings":1,"score":0},"4":{"puddings":1,"score":0}},
  "offered":[{"seat":1,"option":"Tempura"},{"seat":1,"option":"Pudding"},{"seat":2,"option":"Sashimi"},{"seat":3,"option":"Dumpling"},{"seat":4,"option":"Wasabi"}],
  "not_offered":[{"seat":1,"option":"Sashimi"},{"seat":1,"option":"Dumpling"},{"seat":2,"option":"Tempura"},{"seat":4,"option":"Dumpling"}],
  "lens":{"players":{"1":{"hand":1},"2":{"hand":1},"3":{"hand":1},"4":{"hand":1}}}}},

{"name":"A single card in hand is taken automatically with no question and the hand empties","rule":"R5","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding"]},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"puddings":1,"score":0},"2":{"score":0},"3":{"score":0},"4":{"score":0}},
  "not_offered":[{"seat":1,"option":"Pudding"},{"seat":2,"option":"Wasabi"}],
  "lens":{"players":{"1":{"hand":0},"2":{"hand":0},"3":{"hand":0},"4":{"hand":0}}}}},

{"name":"A revealed pick leaves the hand and goes to the tableau","rule":"R6","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":2,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"2":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"3":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"4":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]}}},
 "rules":[{"seat":1,"options_include":"Tempura"},{"seat":2,"options_include":"Wasabi"},{"seat":3,"options_include":"Sashimi"},{"seat":4,"options_include":"Tempura"}],
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0},"4":{"score":0}},
  "lens":{"players":{"1":{"hand":2,"tableau":1},"2":{"hand":2,"tableau":1},"3":{"hand":2,"tableau":1},"4":{"hand":2,"tableau":1}}}}},

{"name":"Tempura, Sashimi and Dumpling picks count toward their sets (2nd tempura 5, 3rd sashimi 10, 3rd dumpling 6)","rule":"R7","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura"],"tempura":1},"2":{"hand":["Sashimi"],"sashimi":2},"3":{"hand":["Dumpling"],"dumplings":2},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":5},"2":{"score":10},"3":{"score":6},"4":{"score":0}},"game":{"hand_number":2}}},

{"name":"Maki-3/1/1 add icons: totals 3,2,1,0 give 6 and 3","rule":"R8","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-3"],"maki":0},"2":{"hand":["Maki-1"],"maki":1},"3":{"hand":["Maki-1"],"maki":0},"4":{"hand":["Wasabi"],"maki":0}}},
 "expect":{"players":{"1":{"score":6},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Pudding adds 1 and puddings survive the end of a hand","rule":"R9","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding"],"puddings":2},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"puddings":3,"score":0},"2":{"puddings":0},"3":{"puddings":0},"4":{"puddings":0}},"game":{"hand_number":2}}},

{"name":"Wasabi picked earlier triples the next nigiri; passing decides who gets what","rule":"R10","players":4,"rounds":2,
 "given":{"game":{"hand_number":1,"pick_number":7,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi","Salmon Nigiri"]},"2":{"hand":["Wasabi","Salmon Nigiri"]},"3":{"hand":["Wasabi","Salmon Nigiri"]},"4":{"hand":["Wasabi","Salmon Nigiri"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi"},{"seat":2,"options_include":"Wasabi"},{"seat":3,"options_include":"Salmon Nigiri"},{"seat":4,"options_include":"Salmon Nigiri"}],
 "expect":{"players":{"1":{"score":0},"2":{"score":6},"3":{"score":4},"4":{"score":2}}}},

{"name":"Nigiri without wasabi: Egg 1, Salmon 2, Squid 3","rule":"R11","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Egg Nigiri"]},"2":{"hand":["Salmon Nigiri"]},"3":{"hand":["Squid Nigiri"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":1},"2":{"score":2},"3":{"score":3},"4":{"score":0}}}},

{"name":"Nigiri on wasabi: Egg 3, Salmon 6, Squid 9","rule":"R12","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Egg Nigiri"],"wasabi_unused":1},"2":{"hand":["Salmon Nigiri"],"wasabi_unused":1},"3":{"hand":["Squid Nigiri"],"wasabi_unused":1},"4":{"hand":["Wasabi"],"wasabi_unused":1}}},
 "expect":{"players":{"1":{"score":3},"2":{"score":6},"3":{"score":9},"4":{"score":0}}}},

{"name":"Remaining hand passes left: seat 1's leftover Pudding reaches seat 2","rule":"R13","players":4,"rounds":2,
 "given":{"game":{"hand_number":1,"pick_number":7,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding","Wasabi"]},"2":{"hand":["Wasabi","Wasabi"]},"3":{"hand":["Wasabi","Wasabi"]},"4":{"hand":["Wasabi","Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi"}],
 "expect":{"players":{"1":{"puddings":0,"score":0},"2":{"puddings":1,"score":0},"3":{"puddings":0},"4":{"puddings":0}}}},

{"name":"Tempura: 3 gives 5, 4 gives 10, 1 gives 0","rule":"R14","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura"],"tempura":2},"2":{"hand":["Tempura"],"tempura":3},"3":{"hand":["Tempura"],"tempura":0},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":5},"2":{"score":10},"3":{"score":0},"4":{"score":0}}}},

{"name":"Sashimi: 5 gives 10, 6 gives 20, 2 gives 0","rule":"R15","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Sashimi"],"sashimi":4},"2":{"hand":["Sashimi"],"sashimi":5},"3":{"hand":["Sashimi"],"sashimi":1},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":10},"2":{"score":20},"3":{"score":0},"4":{"score":0}}}},

{"name":"Dumplings: 1,4,5,6 score 1,10,15,15","rule":"R16","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Dumpling"],"dumplings":0},"2":{"hand":["Dumpling"],"dumplings":3},"3":{"hand":["Dumpling"],"dumplings":4},"4":{"hand":["Dumpling"],"dumplings":5}}},
 "expect":{"players":{"1":{"score":1},"2":{"score":10},"3":{"score":15},"4":{"score":15}}}},

{"name":"Nigiri points are scored; unused wasabi scores nothing","rule":"R17","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"nigiri_points":7,"wasabi_unused":2},"2":{"hand":["Wasabi"],"wasabi_unused":1},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":7},"2":{"score":0},"3":{"score":0},"4":{"score":0}}}},

{"name":"Three-way tie for most maki splits 6 as 2 each; no second place","rule":"R18","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-3"]},"2":{"hand":["Maki-3"]},"3":{"hand":["Maki-3"]},"4":{"hand":["Wasabi"],"maki":1}}},
 "expect":{"players":{"1":{"score":2},"2":{"score":2},"3":{"score":2},"4":{"score":0}}}},

{"name":"Single maki leader gets 6; two tied seconds get floor(3/2)=1 each","rule":"R19","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-1"],"maki":5},"2":{"hand":["Maki-1"],"maki":2},"3":{"hand":["Maki-3"],"maki":0},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":6},"2":{"score":1},"3":{"score":1},"4":{"score":0}}}},

{"name":"Two tied for most maki get 3 each and the next player gets nothing","rule":"R20","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-1"],"maki":3},"2":{"hand":["Maki-2"],"maki":2},"3":{"hand":["Maki-1"],"maki":1},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":3},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Players with 0 maki score no maki points even when only one other has maki","rule":"R21","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-2"]},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":6},"2":{"score":0},"3":{"score":0},"4":{"score":0}}}},

{"name":"Hand counts reset after a hand (all-Wasabi second hand scores nothing) while puddings stay","rule":"R22","players":4,"rounds":9,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8,
   "deck":["Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi"]},
  "players":{"1":{"hand":["Tempura"],"tempura":1,"sashimi":2},"2":{"hand":["Wasabi"],"nigiri_points":4},"3":{"hand":["Pudding"],"puddings":2},"4":{"hand":["Wasabi"]}}},
 "expect":{"players":{"1":{"score":5},"2":{"score":4},"3":{"score":0,"puddings":3},"4":{"score":0}},"game":{"hand_number":3}}},

{"name":"End of game: sole pudding leader gets +6, two tied fewest get -3 each","rule":"R23","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":3},"2":{"hand":["Wasabi"],"puddings":1},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":2}}},
 "expect":{"winner":1,"standings":{"1":603,"2":-299,"3":-299,"4":2},
  "players":{"1":{"score":6},"2":{"score":-3},"3":{"score":-3},"4":{"score":0}}}},

{"name":"End of game: two tied for most puddings get +3 each and share the win","rule":"R23","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":3},"2":{"hand":["Wasabi"],"puddings":3},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":2}}},
 "expect":{"winner":[1,2],"players":{"1":{"score":3},"2":{"score":3},"3":{"score":-6},"4":{"score":0}}}},

{"name":"End of game: 0 puddings counts as fewest; two seats at 0 get -3 each","rule":"R24","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2},"2":{"hand":["Wasabi"],"puddings":0},"3":{"hand":["Wasabi"],"puddings":0},"4":{"hand":["Wasabi"],"puddings":1}}},
 "expect":{"winner":1,"players":{"1":{"score":6},"2":{"score":-3},"3":{"score":-3},"4":{"score":0}}}},

{"name":"End of game: equal puddings score nothing","rule":"R25","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2,"score":10},"2":{"hand":["Wasabi"],"puddings":2,"score":4},"3":{"hand":["Wasabi"],"puddings":2,"score":0},"4":{"hand":["Wasabi"],"puddings":2,"score":7}}},
 "expect":{"winner":1,"standings":{"1":1002,"2":402,"3":2,"4":702},
  "players":{"1":{"score":10},"2":{"score":4},"3":{"score":0},"4":{"score":7}}}},

{"name":"Game ends after the last pick of hand 3 with 3 players (pick 27)","rule":"R26","players":3,
 "given":{"game":{"hand_number":3,"pick_number":9,"picks_per_hand":9},
  "players":{"1":{"hand":["Wasabi"],"puddings":1,"score":5},"2":{"hand":["Wasabi"],"puddings":1,"score":2},"3":{"hand":["Wasabi"],"puddings":1,"score":1}}},
 "expect":{"winner":1,"game":{"hand_number":4},"players":{"1":{"score":5},"2":{"score":2},"3":{"score":1}}}},

{"name":"Game ends after the last pick of hand 3 with 4 players (pick 24)","rule":"R26","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"]},"2":{"hand":["Wasabi"],"score":3},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "expect":{"winner":2,"game":{"hand_number":4},"players":{"1":{"score":0},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Score tie broken by most puddings","rule":"R27","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":4,"score":20},"2":{"hand":["Wasabi"],"puddings":3,"score":26},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":1}}},
 "expect":{"winner":1,"standings":{"1":2604,"2":2603,"3":-299,"4":-299},
  "players":{"1":{"score":26},"2":{"score":26},"3":{"score":-3},"4":{"score":-3}}}},

{"name":"Players tied on score and puddings share the win","rule":"R27","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2,"score":15},"2":{"hand":["Wasabi"],"puddings":2,"score":15},"3":{"hand":["Wasabi"],"puddings":2,"score":5},"4":{"hand":["Wasabi"],"puddings":2,"score":5}}},
 "expect":{"winner":[1,2],"players":{"1":{"score":15},"2":{"score":15},"3":{"score":5},"4":{"score":5}}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name); scenario 26: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name); scenario 28: needs `rules` (what each seat answers, by option name); scenario 29: needs `rules` (what each seat answers, by option name); scenario 30: needs `rules` (what each seat answers, by option name); scenario 31: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"Setup: every seat starts at score 0 and puddings 0, hand 1, full 104-card deck","rule":"R1","players":4,"rounds":0,
 "rules":[{"seat":1,"options_include":"Pudding","times":"all"}],
 "expect":{"players":{"1":{"score":0,"puddings":0},"2":{"score":0,"puddings":0},"3":{"score":0,"puddings":0},"4":{"score":0,"puddings":0}},
 "game":{"hand_number":1},"lens":{"game":{"deck":104}}}},

{"name":"Deal with 4 players: 8 cards each leave the deck (72 left), one picked so 7 remain in hand (any cards)","rule":"R2","players":4,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"Pudding","times":"all"}],
 "expect":{"lens":{"game":{"deck":72},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7},"4":{"hand":7}}}}},

{"name":"Deal with 3 players: 9 cards each leave the deck (77 left), one picked so 8 remain in hand (any cards)","rule":"R2","players":3,"rounds":1,"default":"first",
 "rules":[{"seat":1,"options_include":"Pudding","times":"all"}],
 "expect":{"lens":{"game":{"deck":77},"players":{"1":{"hand":8},"2":{"hand":8},"3":{"hand":8}}}}},

{"name":"Deck is not reshuffled: after a full hand and the next deal, 104-32-32=40 cards remain","rule":"R3","players":4,"rounds":9,"default":"first",
 "rules":[{"seat":1,"options_include":"Pudding","times":"all"}],
 "expect":{"game":{"hand_number":2},"lens":{"game":{"deck":40},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7},"4":{"hand":7}}}}},

{"name":"Every seat is asked to pick from its own hand only","rule":"R4","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":2,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura","Pudding"]},"2":{"hand":["Pudding","Sashimi"]},"3":{"hand":["Pudding","Dumpling"]},"4":{"hand":["Pudding","Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Pudding"},{"seat":2,"options_include":"Pudding"},{"seat":3,"options_include":"Pudding"},{"seat":4,"options_include":"Pudding"}],
 "expect":{"players":{"1":{"puddings":1,"score":0},"2":{"puddings":1,"score":0},"3":{"puddings":1,"score":0},"4":{"puddings":1,"score":0}},
  "offered":[{"seat":1,"option":"Tempura"},{"seat":1,"option":"Pudding"},{"seat":2,"option":"Sashimi"},{"seat":3,"option":"Dumpling"},{"seat":4,"option":"Wasabi"}],
  "not_offered":[{"seat":1,"option":"Sashimi"},{"seat":1,"option":"Dumpling"},{"seat":2,"option":"Tempura"},{"seat":4,"option":"Dumpling"}],
  "lens":{"players":{"1":{"hand":1},"2":{"hand":1},"3":{"hand":1},"4":{"hand":1}}}}},

{"name":"A single card in hand is taken automatically with no question and the hand empties","rule":"R5","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding"]},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":3,"options_include":"Wasabi","times":"all"}],
 "expect":{"players":{"1":{"puddings":1,"score":0},"2":{"score":0},"3":{"score":0},"4":{"score":0}},
  "not_offered":[{"seat":1,"option":"Pudding"},{"seat":2,"option":"Wasabi"}],
  "lens":{"players":{"1":{"hand":0},"2":{"hand":0},"3":{"hand":0},"4":{"hand":0}}}}},

{"name":"A revealed pick leaves the hand and goes to the tableau","rule":"R6","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":2,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"2":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"3":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]},"4":{"hand":["Tempura","Wasabi","Sashimi"],"tableau":[]}}},
 "rules":[{"seat":1,"options_include":"Tempura"},{"seat":2,"options_include":"Wasabi"},{"seat":3,"options_include":"Sashimi"},{"seat":4,"options_include":"Tempura"}],
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0},"4":{"score":0}},
  "lens":{"players":{"1":{"hand":2,"tableau":1},"2":{"hand":2,"tableau":1},"3":{"hand":2,"tableau":1},"4":{"hand":2,"tableau":1}}}}},

{"name":"Tempura, Sashimi and Dumpling picks count toward their sets (2nd tempura 5, 3rd sashimi 10, 3rd dumpling 6)","rule":"R7","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura"],"tempura":1},"2":{"hand":["Sashimi"],"sashimi":2},"3":{"hand":["Dumpling"],"dumplings":2},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Tempura","times":"all"}],
 "expect":{"players":{"1":{"score":5},"2":{"score":10},"3":{"score":6},"4":{"score":0}},"game":{"hand_number":2}}},

{"name":"Maki-3/1/1 add icons: totals 3,2,1,0 give 6 and 3","rule":"R8","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-3"],"maki":0},"2":{"hand":["Maki-1"],"maki":1},"3":{"hand":["Maki-1"],"maki":0},"4":{"hand":["Wasabi"],"maki":0}}},
 "rules":[{"seat":1,"options_include":"Maki-3","times":"all"}],
 "expect":{"players":{"1":{"score":6},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Pudding adds 1 and puddings survive the end of a hand","rule":"R9","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding"],"puddings":2},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Pudding","times":"all"}],
 "expect":{"players":{"1":{"puddings":3,"score":0},"2":{"puddings":0},"3":{"puddings":0},"4":{"puddings":0}},"game":{"hand_number":2}}},

{"name":"Wasabi picked earlier triples the next nigiri; passing decides who gets what","rule":"R10","players":4,"rounds":2,
 "given":{"game":{"hand_number":1,"pick_number":7,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi","Salmon Nigiri"]},"2":{"hand":["Wasabi","Salmon Nigiri"]},"3":{"hand":["Wasabi","Salmon Nigiri"]},"4":{"hand":["Wasabi","Salmon Nigiri"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi"},{"seat":2,"options_include":"Wasabi"},{"seat":3,"options_include":"Salmon Nigiri"},{"seat":4,"options_include":"Salmon Nigiri"}],
 "expect":{"players":{"1":{"score":0},"2":{"score":6},"3":{"score":4},"4":{"score":2}}}},

{"name":"Nigiri without wasabi: Egg 1, Salmon 2, Squid 3","rule":"R11","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Egg Nigiri"]},"2":{"hand":["Salmon Nigiri"]},"3":{"hand":["Squid Nigiri"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Egg Nigiri","times":"all"}],
 "expect":{"players":{"1":{"score":1},"2":{"score":2},"3":{"score":3},"4":{"score":0}}}},

{"name":"Nigiri on wasabi: Egg 3, Salmon 6, Squid 9","rule":"R12","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Egg Nigiri"],"wasabi_unused":1},"2":{"hand":["Salmon Nigiri"],"wasabi_unused":1},"3":{"hand":["Squid Nigiri"],"wasabi_unused":1},"4":{"hand":["Wasabi"],"wasabi_unused":1}}},
 "rules":[{"seat":1,"options_include":"Egg Nigiri","times":"all"}],
 "expect":{"players":{"1":{"score":3},"2":{"score":6},"3":{"score":9},"4":{"score":0}}}},

{"name":"Remaining hand passes left: seat 1's leftover Pudding reaches seat 2","rule":"R13","players":4,"rounds":2,
 "given":{"game":{"hand_number":1,"pick_number":7,"picks_per_hand":8},
  "players":{"1":{"hand":["Pudding","Wasabi"]},"2":{"hand":["Wasabi","Wasabi"]},"3":{"hand":["Wasabi","Wasabi"]},"4":{"hand":["Wasabi","Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi"}],
 "expect":{"players":{"1":{"puddings":0,"score":0},"2":{"puddings":1,"score":0},"3":{"puddings":0},"4":{"puddings":0}}}},

{"name":"Tempura: 3 gives 5, 4 gives 10, 1 gives 0","rule":"R14","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Tempura"],"tempura":2},"2":{"hand":["Tempura"],"tempura":3},"3":{"hand":["Tempura"],"tempura":0},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Tempura","times":"all"}],
 "expect":{"players":{"1":{"score":5},"2":{"score":10},"3":{"score":0},"4":{"score":0}}}},

{"name":"Sashimi: 5 gives 10, 6 gives 20, 2 gives 0","rule":"R15","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Sashimi"],"sashimi":4},"2":{"hand":["Sashimi"],"sashimi":5},"3":{"hand":["Sashimi"],"sashimi":1},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Sashimi","times":"all"}],
 "expect":{"players":{"1":{"score":10},"2":{"score":20},"3":{"score":0},"4":{"score":0}}}},

{"name":"Dumplings: 1,4,5,6 score 1,10,15,15","rule":"R16","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Dumpling"],"dumplings":0},"2":{"hand":["Dumpling"],"dumplings":3},"3":{"hand":["Dumpling"],"dumplings":4},"4":{"hand":["Dumpling"],"dumplings":5}}},
 "rules":[{"seat":1,"options_include":"Dumpling","times":"all"}],
 "expect":{"players":{"1":{"score":1},"2":{"score":10},"3":{"score":15},"4":{"score":15}}}},

{"name":"Nigiri points are scored; unused wasabi scores nothing","rule":"R17","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"nigiri_points":7,"wasabi_unused":2},"2":{"hand":["Wasabi"],"wasabi_unused":1},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"players":{"1":{"score":7},"2":{"score":0},"3":{"score":0},"4":{"score":0}}}},

{"name":"Three-way tie for most maki splits 6 as 2 each; no second place","rule":"R18","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-3"]},"2":{"hand":["Maki-3"]},"3":{"hand":["Maki-3"]},"4":{"hand":["Wasabi"],"maki":1}}},
 "rules":[{"seat":1,"options_include":"Maki-3","times":"all"}],
 "expect":{"players":{"1":{"score":2},"2":{"score":2},"3":{"score":2},"4":{"score":0}}}},

{"name":"Single maki leader gets 6; two tied seconds get floor(3/2)=1 each","rule":"R19","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-1"],"maki":5},"2":{"hand":["Maki-1"],"maki":2},"3":{"hand":["Maki-3"],"maki":0},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Maki-1","times":"all"}],
 "expect":{"players":{"1":{"score":6},"2":{"score":1},"3":{"score":1},"4":{"score":0}}}},

{"name":"Two tied for most maki get 3 each and the next player gets nothing","rule":"R20","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-1"],"maki":3},"2":{"hand":["Maki-2"],"maki":2},"3":{"hand":["Maki-1"],"maki":1},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Maki-1","times":"all"}],
 "expect":{"players":{"1":{"score":3},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Players with 0 maki score no maki points even when only one other has maki","rule":"R21","players":4,"rounds":1,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Maki-2"]},"2":{"hand":["Wasabi"]},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Maki-2","times":"all"}],
 "expect":{"players":{"1":{"score":6},"2":{"score":0},"3":{"score":0},"4":{"score":0}}}},

{"name":"Hand counts reset after a hand (all-Wasabi second hand scores nothing) while puddings stay","rule":"R22","players":4,"rounds":9,
 "given":{"game":{"hand_number":1,"pick_number":8,"picks_per_hand":8,
   "deck":["Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi","Wasabi"]},
  "players":{"1":{"hand":["Tempura"],"tempura":1,"sashimi":2},"2":{"hand":["Wasabi"],"nigiri_points":4},"3":{"hand":["Pudding"],"puddings":2},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"},{"seat":2,"options_include":"Wasabi","times":"all"},{"seat":3,"options_include":"Wasabi","times":"all"},{"seat":4,"options_include":"Wasabi","times":"all"}],
 "expect":{"players":{"1":{"score":5},"2":{"score":4},"3":{"score":0,"puddings":3},"4":{"score":0}},"game":{"hand_number":3}}},

{"name":"End of game: sole pudding leader gets +6, two tied fewest get -3 each","rule":"R23","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":3},"2":{"hand":["Wasabi"],"puddings":1},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":2}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":1,"standings":{"1":603,"2":-299,"3":-299,"4":2},
  "players":{"1":{"score":6},"2":{"score":-3},"3":{"score":-3},"4":{"score":0}}}},

{"name":"End of game: two tied for most puddings get +3 each and share the win","rule":"R23","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":3},"2":{"hand":["Wasabi"],"puddings":3},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":2}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":[1,2],"players":{"1":{"score":3},"2":{"score":3},"3":{"score":-6},"4":{"score":0}}}},

{"name":"End of game: 0 puddings counts as fewest; two seats at 0 get -3 each","rule":"R24","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2},"2":{"hand":["Wasabi"],"puddings":0},"3":{"hand":["Wasabi"],"puddings":0},"4":{"hand":["Wasabi"],"puddings":1}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":1,"players":{"1":{"score":6},"2":{"score":-3},"3":{"score":-3},"4":{"score":0}}}},

{"name":"End of game: equal puddings score nothing","rule":"R25","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2,"score":10},"2":{"hand":["Wasabi"],"puddings":2,"score":4},"3":{"hand":["Wasabi"],"puddings":2,"score":0},"4":{"hand":["Wasabi"],"puddings":2,"score":7}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":1,"standings":{"1":1002,"2":402,"3":2,"4":702},
  "players":{"1":{"score":10},"2":{"score":4},"3":{"score":0},"4":{"score":7}}}},

{"name":"Game ends after the last pick of hand 3 with 3 players (pick 27)","rule":"R26","players":3,
 "given":{"game":{"hand_number":3,"pick_number":9,"picks_per_hand":9},
  "players":{"1":{"hand":["Wasabi"],"puddings":1,"score":5},"2":{"hand":["Wasabi"],"puddings":1,"score":2},"3":{"hand":["Wasabi"],"puddings":1,"score":1}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":1,"game":{"hand_number":4},"players":{"1":{"score":5},"2":{"score":2},"3":{"score":1}}}},

{"name":"Game ends after the last pick of hand 3 with 4 players (pick 24)","rule":"R26","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"]},"2":{"hand":["Wasabi"],"score":3},"3":{"hand":["Wasabi"]},"4":{"hand":["Wasabi"]}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":2,"game":{"hand_number":4},"players":{"1":{"score":0},"2":{"score":3},"3":{"score":0},"4":{"score":0}}}},

{"name":"Score tie broken by most puddings","rule":"R27","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":4,"score":20},"2":{"hand":["Wasabi"],"puddings":3,"score":26},"3":{"hand":["Wasabi"],"puddings":1},"4":{"hand":["Wasabi"],"puddings":1}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":1,"standings":{"1":2604,"2":2603,"3":-299,"4":-299},
  "players":{"1":{"score":26},"2":{"score":26},"3":{"score":-3},"4":{"score":-3}}}},

{"name":"Players tied on score and puddings share the win","rule":"R27","players":4,
 "given":{"game":{"hand_number":3,"pick_number":8,"picks_per_hand":8},
  "players":{"1":{"hand":["Wasabi"],"puddings":2,"score":15},"2":{"hand":["Wasabi"],"puddings":2,"score":15},"3":{"hand":["Wasabi"],"puddings":2,"score":5},"4":{"hand":["Wasabi"],"puddings":2,"score":5}}},
 "rules":[{"seat":1,"options_include":"Wasabi","times":"all"}],
 "expect":{"winner":[1,2],"players":{"1":{"score":15},"2":{"score":15},"3":{"score":5},"4":{"score":5}}}}
]
````
