# 29 scenarios

- time: 2026-10-27T17:43:45+00:00 (60.3s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 78ef7fff69abb413, reply sha256 3a615a71f30b2504

## Sent

````
SPEC:
{
  "name": "Point Salad: Secret Recipes",
  "summary": "Three players each hold a secret two-vegetable Recipe. Over 12 rounds they talk, then all at once pick a vegetable or the shared scoring Card. Collisions shrink or cancel gains, and the highest points plus recipe score wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "rounds": 12,
    "card_types_count": 6,
    "fan_multiplier": 2,
    "rainbow_multiplier": 3,
    "big_bowl_multiplier": 1,
    "balance_value": 6,
    "balance_min_each": 1,
    "balance_max_spread": 1,
    "sole_vegetable_gain": 2,
    "pair_vegetable_gain": 1,
    "triple_vegetable_gain": 0,
    "recipe_first_weight": 2,
    "recipe_second_weight": 2,
    "recipe_min_weight": 2,
    "start_vegetables": 0,
    "start_points": 0
  },
  "attributes": {
    "player": [
      {
        "key": "t",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tomatoes in basket",
        "observable": true
      },
      {
        "key": "l",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "lettuces in basket",
        "observable": true
      },
      {
        "key": "c",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "carrots in basket",
        "observable": true
      },
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points won from the Card",
        "observable": true
      },
      {
        "key": "recipe",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "secret Recipe tile: TL, LC or CT; revealed at game end",
        "observable": false
      },
      {
        "key": "pick",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's pick: Tomato, Lettuce, Carrot or Card",
        "observable": true
      },
      {
        "key": "card_value",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "value of this round's drawn card, computed from the basket at the start of the round",
        "observable": false
      },
      {
        "key": "recipe_score",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "2*first + 2*second + 2*min(first, second) for the two Recipe vegetables; revealed at game end",
        "observable": true
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's talk message",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rounds started so far",
        "observable": true
      },
      {
        "key": "card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the scoring card drawn this round",
        "observable": true
      },
      {
        "key": "card_types",
        "type": "list",
        "visible": "public",
        "initial": [
          "Tomato Fan",
          "Lettuce Fan",
          "Carrot Fan",
          "Rainbow",
          "Big Bowl",
          "Balance"
        ],
        "meaning": "the 6 card types, drawn from with replacement",
        "observable": false
      },
      {
        "key": "recipe_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "TL",
          "LC",
          "CT"
        ],
        "meaning": "Recipe tiles still to deal",
        "observable": false
      },
      {
        "key": "n_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "players who picked Card this round",
        "observable": false
      },
      {
        "key": "n_t",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "players who picked Tomato this round",
        "observable": false
      },
      {
        "key": "n_l",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "players who picked Lettuce this round",
        "observable": false
      },
      {
        "key": "n_c",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "players who picked Carrot this round",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player starts with t=0, l=0, c=0 and points=0, all public.",
    "The three Recipe tiles TL, LC and CT are dealt at random from recipe_deck, one into each player's recipe; recipe_deck ends empty.",
    "Each player is told only their own recipe."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; card = one entry of card_types drawn at random, with replacement and equally likely; announce round and card to everyone"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each player, card_value is set from the current t, l, c: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if t>=1 and l>=1 and c>=1 and max(t,l,c)-min(t,l,c)<=1, otherwise 0"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "message set for each player; then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}; messages bind no one"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of Tomato, Lettuce, Carrot, Card",
      "effect": "pick set for each player; nobody sees a pick until all are in"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "n_card = number of players with pick == Card; n_t = number with pick == Tomato; n_l = number with pick == Lettuce; n_c = number with pick == Carrot"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each player: if pick == Card and n_card == 1, then points += card_value; otherwise no change"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each player: if pick == Tomato, t += 2 when n_t == 1, t += 1 when n_t == 2, and nothing when n_t == 3; the same for Lettuce with l and n_l, and for Carrot with c and n_c"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "recipe_score set for each player: TL gives 2*t + 2*l + 2*min(t,l); LC gives 2*l + 2*c + 2*min(l,c); CT gives 2*c + 2*t + 2*min(c,t)"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce every player's pick, what each received (Card points or vegetables), and every player's t, l, c and points"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when round == 12: reveal every player's recipe, recipe_score and points + recipe_score to everyone"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "if round >= 12, end the game; otherwise start the next round"
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.points + you.recipe_score",
    "decided_by": "Each player's final_total is points plus recipe_score. The highest final_total wins, and players tied at the top share a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, each of the 3 players gets exactly one distinct Recipe from TL, LC and CT, and starts with t=0, l=0, c=0 and points=0."
    },
    {
      "id": "R2",
      "text": "Each round, exactly one card is drawn at random with replacement from the 6 types and announced to everyone."
    },
    {
      "id": "R3",
      "text": "When the card is Tomato Fan, its value for a player is 2*t; when it is Lettuce Fan, 2*l; when it is Carrot Fan, 2*c."
    },
    {
      "id": "R4",
      "text": "When the card is Rainbow, its value is 3*min(t,l,c); for example, t=3, l=1, c=2 gives 3."
    },
    {
      "id": "R5",
      "text": "When the card is Big Bowl, its value is t+l+c; for example, t=3, l=1, c=2 gives 6."
    },
    {
      "id": "R6",
      "text": "When the card is Balance, its value is 6 if t, l and c are each at least 1 and max minus min is at most 1, otherwise 0; for example, t=3, l=1, c=2 gives 0."
    },
    {
      "id": "R7",
      "text": "The card's value is computed from the basket as it stood at the start of the round, before any vegetables are added."
    },
    {
      "id": "R8",
      "text": "Each round, every player writes one short message at the same time, and all messages are then shown to everyone."
    },
    {
      "id": "R9",
      "text": "Each round, every player simultaneously picks exactly one of Tomato, Lettuce, Carrot or Card."
    },
    {
      "id": "R10",
      "text": "When exactly one player picks Card, that player's points increase by the card's value."
    },
    {
      "id": "R11",
      "text": "When zero players or two or more players pick Card, nobody's points change from the card."
    },
    {
      "id": "R12",
      "text": "When exactly one player picks a vegetable, that player adds 2 of it to their basket."
    },
    {
      "id": "R13",
      "text": "When exactly two players pick the same vegetable, each of them adds 1 of it."
    },
    {
      "id": "R14",
      "text": "When all three players pick the same vegetable, nobody receives any of it."
    },
    {
      "id": "R15",
      "text": "After each round, every pick, what each player received, and all baskets and points are announced."
    },
    {
      "id": "R16",
      "text": "The game ends after round 12."
    },
    {
      "id": "R17",
      "text": "A player's recipe_score is 2*first + 2*second + 2*min(first,second) over the Recipe's two vegetables: TL uses t and l, LC uses l and c, CT uses c and t. For example, CT with c=3 and t=2 scores 14, and LC with l=0 and c=6 scores 12."
    },
    {
      "id": "R18",
      "text": "At the end, recipes are revealed and the player with the highest points + recipe_score wins; for example, points 10 with recipe 12 (total 22) beats points 0 with recipe 14 (total 14)."
    },
    {
      "id": "R19",
      "text": "When two or three players tie for the highest points + recipe_score, the game is a draw among them."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every seat",
      "options": "any short free text"
    },
    {
      "question": "Pick",
      "who": "every seat",
      "options": "Tomato, Lettuce, Carrot, Card"
    }
  ],
  "choices": [
    {
      "what": "3 players, fixed",
      "why": "The designer fixed exactly 3: the three Recipes are all dealt and the collision rules (1, 2 or 3 pickers) are written for three seats."
    },
    {
      "what": "Keep simultaneous talk before the pick, as a poll with broadcast",
      "why": "The rules ask for simultaneous messages. Players clash over the Card and over shared vegetables, so a proposal can cost the one who follows it, and the talk gives players something to bluff and coordinate with."
    },
    {
      "what": "recipe_score is recomputed every round as owner-only state and revealed in the final round",
      "why": "The ranking needs it as an attribute, and computing it as the baskets change gives the same value at the end."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player reads the public baskets to guess the others' secret Recipes and Card values, avoids colliding on the Card when another player has a big payoff, and uses talk to bluff or steer the others away from shared picks."
    }
  ],
  "simplifications": [
    {
      "what": "The Recipe reveal is an announcement step that runs when round == 12, before the end check",
      "why": "The engine has no separate end phase. The reveal is equivalent and does not change scoring."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: t, l, c, points, pick, recipe_score; table: round, card.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
If a test rigs the draw by shrinking card_types to a single entry, it must also set card_types_count to 1 in the same `given` block (game: {card_types: ["Rainbow"], card_types_count: 1}) so the list and the count agree. Otherwise, do not predict which card is drawn, because chance decides it. Instead, check that `card` is one of the six names and that the sole Card picker's points equal that card's value from their starting basket. Apply this to the R2, R3 (Tomato Fan, Carrot Fan) and R4 Rainbow scenarios. Keep the expected values as they are: 2*t = 6 for t=3, and Rainbow worth 3 for t=3, l=1, c=2.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup: every basket and points start at 0 and all three Recipe tiles are dealt",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"t": 0, "l": 0, "c": 0, "points": 0},
        "2": {"t": 0, "l": 0, "c": 0, "points": 0},
        "3": {"t": 0, "l": 0, "c": 0, "points": 0}
      },
      "lens": {"game": {"recipe_deck": 0}}
    }
  },
  {
    "name": "One card is drawn and announced each round (draw rigged to Big Bowl)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl"], "card_types_count": 1},
      "players": {"1": {"t": 1, "l": 1, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 1, "card": "Big Bowl"},
      "players": {
        "1": {"points": 3, "t": 1, "l": 1, "c": 1},
        "2": {"l": 2},
        "3": {"c": 2}
      }
    }
  },
  {
    "name": "Tomato Fan is worth 2*t: t=3 gives 6 (draw rigged)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan"], "card_types_count": 1},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Lettuce", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Tomato Fan"},
      "players": {
        "1": {"points": 6, "t": 3},
        "2": {"l": 1},
        "3": {"l": 1}
      }
    }
  },
  {
    "name": "Carrot Fan is worth 2*c: c=2 gives 4 (draw rigged)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Carrot Fan"], "card_types_count": 1},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Lettuce", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Carrot Fan"},
      "players": {
        "1": {"points": 4, "c": 2},
        "2": {"t": 2},
        "3": {"l": 2}
      }
    }
  },
  {
    "name": "Lettuce Fan is worth 2*l: l=4 gives 8 (draw rigged)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Lettuce Fan"], "card_types_count": 1},
      "players": {"1": {"t": 0, "l": 4, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Lettuce Fan"},
      "players": {"1": {"points": 8, "l": 4}}
    }
  },
  {
    "name": "Rainbow is worth 3*min(t,l,c): t=3, l=1, c=2 gives 3 (draw rigged)",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Rainbow"], "card_types_count": 1},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Rainbow"},
      "players": {
        "1": {"points": 3},
        "2": {"t": 1},
        "3": {"t": 1}
      }
    }
  },
  {
    "name": "Big Bowl is worth t+l+c: t=3, l=1, c=2 gives 6 (draw rigged)",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl"], "card_types_count": 1},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Big Bowl"},
      "players": {"1": {"points": 6}}
    }
  },
  {
    "name": "Balance is worth 0 when the spread is too big: t=3, l=1, c=2 gives 0 (draw rigged)",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Balance"], "card_types_count": 1},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Balance"},
      "players": {"1": {"points": 0}}
    }
  },
  {
    "name": "Balance is worth 6 when each is at least 1 and the spread is at most 1: t=1, l=2, c=2 (draw rigged)",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Balance"], "card_types_count": 1},
      "players": {"1": {"t": 1, "l": 2, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Balance"},
      "players": {"1": {"points": 6}}
    }
  },
  {
    "name": "Card value uses the basket at the start of the round: 2 tomatoes from round 1 make Tomato Fan worth 4 in round 2 (draw rigged)",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 2,
    "given": {
      "game": {"card_types": ["Tomato Fan"], "card_types_count": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": 1},
      {"seat": 1, "options_include": "Card", "times": 1},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 2},
      "players": {
        "1": {"t": 2, "points": 4, "pick": "Card"},
        "2": {"l": 4, "points": 0},
        "3": {"c": 4, "points": 0}
      }
    }
  },
  {
    "name": "Talk happens each round and binds no one; the round still resolves",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 1},
      "players": {
        "1": {"t": 2},
        "2": {"l": 2},
        "3": {"c": 2}
      }
    }
  },
  {
    "name": "Every seat is offered Tomato, Lettuce, Carrot and Card, and its pick is recorded",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"pick": "Tomato"},
        "2": {"pick": "Lettuce"},
        "3": {"pick": "Carrot"}
      },
      "offered": [
        {"seat": 1, "option": "Tomato"},
        {"seat": 1, "option": "Lettuce"},
        {"seat": 1, "option": "Carrot"},
        {"seat": 1, "option": "Card"},
        {"seat": 2, "option": "Card"},
        {"seat": 3, "option": "Card"}
      ]
    }
  },
  {
    "name": "The sole Card picker gains the card value (Tomato Fan rigged, t=2 gives 4)",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan"], "card_types_count": 1},
      "players": {"2": {"t": 2, "points": 5}}
    },
    "rules": [
      {"seat": 1, "options_include": "Lettuce", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0},
        "2": {"points": 9},
        "3": {"points": 0}
      }
    }
  },
  {
    "name": "Two Card pickers cancel: nobody gains points",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan"], "card_types_count": 1},
      "players": {"1": {"t": 3}, "2": {"t": 3}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0, "t": 3},
        "2": {"points": 0, "t": 3},
        "3": {"points": 0, "t": 2}
      }
    }
  },
  {
    "name": "No Card picker: nobody's points change",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"points": 4}, "2": {"points": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 4},
        "2": {"points": 2},
        "3": {"points": 0}
      }
    }
  },
  {
    "name": "A sole vegetable picker adds 2 of it",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Carrot", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"c": 3, "t": 0, "l": 0},
        "2": {"c": 0},
        "3": {"c": 0}
      }
    }
  },
  {
    "name": "Two players picking the same vegetable each add 1",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Lettuce", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"l": 1},
        "2": {"l": 1},
        "3": {"t": 2, "l": 0}
      }
    }
  },
  {
    "name": "All three picking the same vegetable get nothing",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Carrot", "times": "all"},
      {"seat": 2, "options_include": "Carrot", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"c": 1},
        "2": {"c": 0},
        "3": {"c": 0}
      }
    }
  },
  {
    "name": "After the round every pick, basket and points total is public",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl"], "card_types_count": 1},
      "players": {"3": {"t": 1, "l": 1, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"pick": "Tomato", "t": 1, "points": 0},
        "2": {"pick": "Tomato", "t": 1, "points": 0},
        "3": {"pick": "Card", "t": 1, "l": 1, "c": 1, "points": 3}
      }
    }
  },
  {
    "name": "The game ends after round 12 and the best recipe total wins",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "TL", "t": 3, "l": 3, "c": 0},
        "2": {"recipe": "LC", "t": 0, "l": 1, "c": 1},
        "3": {"recipe": "CT", "t": 0, "l": 0, "c": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 18, "2": 6, "3": 0},
      "game": {"round": 12},
      "players": {
        "1": {"recipe_score": 18},
        "2": {"recipe_score": 6},
        "3": {"recipe_score": 0}
      }
    }
  },
  {
    "name": "Recipe score: CT with c=3, t=2 is 14; LC with l=0, c=6 is 12",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"recipe": "TL", "t": 0, "l": 0, "c": 0},
        "2": {"recipe": "LC", "t": 0, "l": 0, "c": 6},
        "3": {"recipe": "CT", "t": 2, "l": 0, "c": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"recipe_score": 0, "points": 0},
        "2": {"recipe_score": 12, "points": 0},
        "3": {"recipe_score": 14, "points": 0}
      }
    }
  },
  {
    "name": "Points 10 plus recipe 12 (22) beats points 0 plus recipe 14 (14)",
    "rule": "R18",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "LC", "t": 0, "l": 0, "c": 6, "points": 10},
        "2": {"recipe": "CT", "t": 2, "l": 0, "c": 3, "points": 0},
        "3": {"recipe": "TL", "t": 0, "l": 0, "c": 0, "points": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 22, "2": 14, "3": 0},
      "players": {
        "1": {"recipe_score": 12, "points": 10},
        "2": {"recipe_score": 14, "points": 0}
      }
    }
  },
  {
    "name": "Two players tied at the top share the win",
    "rule": "R19",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "TL", "t": 1, "l": 1, "c": 0, "points": 0},
        "2": {"recipe": "LC", "t": 0, "l": 1, "c": 1, "points": 0},
        "3": {"recipe": "CT", "t": 0, "l": 0, "c": 0, "points": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 6, "2": 6, "3": 0}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 3: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 4: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 5: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 6: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 7: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 8: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 9: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 10: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 13: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 14: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c); scenario 19: given table attribute `card_types_count` is not in the spec (spec has: round, card, card_types, recipe_deck, n_card, n_t, n_l, n_c)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Setup: every basket and points start at 0 and all three Recipe tiles are dealt",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"t": 0, "l": 0, "c": 0, "points": 0},
        "2": {"t": 0, "l": 0, "c": 0, "points": 0},
        "3": {"t": 0, "l": 0, "c": 0, "points": 0}
      },
      "lens": {"game": {"recipe_deck": 0}}
    }
  },
  {
    "name": "One card is drawn and announced each round (draw rigged: all 6 entries Big Bowl)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl"]},
      "players": {"1": {"t": 1, "l": 1, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 1, "card": "Big Bowl"},
      "players": {
        "1": {"points": 3, "t": 1, "l": 1, "c": 1},
        "2": {"l": 2},
        "3": {"c": 2}
      }
    }
  },
  {
    "name": "Tomato Fan is worth 2*t: t=3 gives 6 (draw rigged: all 6 entries Tomato Fan)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan"]},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Lettuce", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Tomato Fan"},
      "players": {
        "1": {"points": 6, "t": 3},
        "2": {"l": 1},
        "3": {"l": 1}
      }
    }
  },
  {
    "name": "Carrot Fan is worth 2*c: c=2 gives 4 (draw rigged: all 6 entries Carrot Fan)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Carrot Fan", "Carrot Fan", "Carrot Fan", "Carrot Fan", "Carrot Fan", "Carrot Fan"]},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Lettuce", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Carrot Fan"},
      "players": {
        "1": {"points": 4, "c": 2},
        "2": {"t": 2},
        "3": {"l": 2}
      }
    }
  },
  {
    "name": "Lettuce Fan is worth 2*l: l=4 gives 8 (draw rigged: all 6 entries Lettuce Fan)",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Lettuce Fan", "Lettuce Fan", "Lettuce Fan", "Lettuce Fan", "Lettuce Fan", "Lettuce Fan"]},
      "players": {"1": {"t": 0, "l": 4, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Lettuce Fan"},
      "players": {"1": {"points": 8, "l": 4}}
    }
  },
  {
    "name": "Rainbow is worth 3*min(t,l,c): t=3, l=1, c=2 gives 3 (draw rigged: all 6 entries Rainbow)",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Rainbow", "Rainbow", "Rainbow", "Rainbow", "Rainbow", "Rainbow"]},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Rainbow"},
      "players": {
        "1": {"points": 3},
        "2": {"t": 1},
        "3": {"t": 1}
      }
    }
  },
  {
    "name": "Big Bowl is worth t+l+c: t=3, l=1, c=2 gives 6 (draw rigged: all 6 entries Big Bowl)",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl"]},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Big Bowl"},
      "players": {"1": {"points": 6}}
    }
  },
  {
    "name": "Balance is worth 0 when the spread is too big: t=3, l=1, c=2 gives 0 (draw rigged: all 6 entries Balance)",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Balance", "Balance", "Balance", "Balance", "Balance", "Balance"]},
      "players": {"1": {"t": 3, "l": 1, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Balance"},
      "players": {"1": {"points": 0}}
    }
  },
  {
    "name": "Balance is worth 6 when each is at least 1 and the spread is at most 1: t=1, l=2, c=2 (draw rigged: all 6 entries Balance)",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Balance", "Balance", "Balance", "Balance", "Balance", "Balance"]},
      "players": {"1": {"t": 1, "l": 2, "c": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"card": "Balance"},
      "players": {"1": {"points": 6}}
    }
  },
  {
    "name": "Card value uses the basket at the start of the round: 2 tomatoes from round 1 make Tomato Fan worth 4 in round 2 (draw rigged: all 6 entries Tomato Fan)",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 2,
    "given": {
      "game": {"card_types": ["Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan"]}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": 1},
      {"seat": 1, "options_include": "Card", "times": 1},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 2},
      "players": {
        "1": {"t": 2, "points": 4, "pick": "Card"},
        "2": {"l": 4, "points": 0},
        "3": {"c": 4, "points": 0}
      }
    }
  },
  {
    "name": "Talk happens each round and binds no one; the round still resolves",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "game": {"round": 1},
      "players": {
        "1": {"t": 2},
        "2": {"l": 2},
        "3": {"c": 2}
      }
    }
  },
  {
    "name": "Every seat is offered Tomato, Lettuce, Carrot and Card, and its pick is recorded",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"pick": "Tomato"},
        "2": {"pick": "Lettuce"},
        "3": {"pick": "Carrot"}
      },
      "offered": [
        {"seat": 1, "option": "Tomato"},
        {"seat": 1, "option": "Lettuce"},
        {"seat": 1, "option": "Carrot"},
        {"seat": 1, "option": "Card"},
        {"seat": 2, "option": "Card"},
        {"seat": 3, "option": "Card"}
      ]
    }
  },
  {
    "name": "The sole Card picker gains the card value (Tomato Fan rigged, t=2 gives 4)",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan"]},
      "players": {"2": {"t": 2, "points": 5}}
    },
    "rules": [
      {"seat": 1, "options_include": "Lettuce", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0},
        "2": {"points": 9},
        "3": {"points": 0}
      }
    }
  },
  {
    "name": "Two Card pickers cancel: nobody gains points",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan", "Tomato Fan"]},
      "players": {"1": {"t": 3}, "2": {"t": 3}}
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 0, "t": 3},
        "2": {"points": 0, "t": 3},
        "3": {"points": 0, "t": 2}
      }
    }
  },
  {
    "name": "No Card picker: nobody's points change",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"points": 4}, "2": {"points": 2}}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"points": 4},
        "2": {"points": 2},
        "3": {"points": 0}
      }
    }
  },
  {
    "name": "A sole vegetable picker adds 2 of it",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Carrot", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"c": 3, "t": 0, "l": 0},
        "2": {"c": 0},
        "3": {"c": 0}
      }
    }
  },
  {
    "name": "Two players picking the same vegetable each add 1",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "Lettuce", "times": "all"},
      {"seat": 2, "options_include": "Lettuce", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"l": 1},
        "2": {"l": 1},
        "3": {"t": 2, "l": 0}
      }
    }
  },
  {
    "name": "All three picking the same vegetable get nothing",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Carrot", "times": "all"},
      {"seat": 2, "options_include": "Carrot", "times": "all"},
      {"seat": 3, "options_include": "Carrot", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"c": 1},
        "2": {"c": 0},
        "3": {"c": 0}
      }
    }
  },
  {
    "name": "After the round every pick, basket and points total is public",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"card_types": ["Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl", "Big Bowl"]},
      "players": {"3": {"t": 1, "l": 1, "c": 1}}
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"pick": "Tomato", "t": 1, "points": 0},
        "2": {"pick": "Tomato", "t": 1, "points": 0},
        "3": {"pick": "Card", "t": 1, "l": 1, "c": 1, "points": 3}
      }
    }
  },
  {
    "name": "The game ends after round 12 and the best recipe total wins",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "TL", "t": 3, "l": 3, "c": 0},
        "2": {"recipe": "LC", "t": 0, "l": 1, "c": 1},
        "3": {"recipe": "CT", "t": 0, "l": 0, "c": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Tomato", "times": "all"},
      {"seat": 2, "options_include": "Tomato", "times": "all"},
      {"seat": 3, "options_include": "Tomato", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 18, "2": 6, "3": 0},
      "game": {"round": 12},
      "players": {
        "1": {"recipe_score": 18},
        "2": {"recipe_score": 6},
        "3": {"recipe_score": 0}
      }
    }
  },
  {
    "name": "Recipe score: CT with c=3, t=2 is 14; LC with l=0, c=6 is 12",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"recipe": "TL", "t": 0, "l": 0, "c": 0},
        "2": {"recipe": "LC", "t": 0, "l": 0, "c": 6},
        "3": {"recipe": "CT", "t": 2, "l": 0, "c": 3}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"recipe_score": 0, "points": 0},
        "2": {"recipe_score": 12, "points": 0},
        "3": {"recipe_score": 14, "points": 0}
      }
    }
  },
  {
    "name": "Points 10 plus recipe 12 (22) beats points 0 plus recipe 14 (14)",
    "rule": "R18",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "LC", "t": 0, "l": 0, "c": 6, "points": 10},
        "2": {"recipe": "CT", "t": 2, "l": 0, "c": 3, "points": 0},
        "3": {"recipe": "TL", "t": 0, "l": 0, "c": 0, "points": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 22, "2": 14, "3": 0},
      "players": {
        "1": {"recipe_score": 12, "points": 10},
        "2": {"recipe_score": 14, "points": 0}
      }
    }
  },
  {
    "name": "Two players tied at the top share the win",
    "rule": "R19",
    "players": 3,
    "seed": 1,
    "given": {
      "game": {"round": 11},
      "players": {
        "1": {"recipe": "TL", "t": 1, "l": 1, "c": 0, "points": 0},
        "2": {"recipe": "LC", "t": 0, "l": 1, "c": 1, "points": 0},
        "3": {"recipe": "CT", "t": 0, "l": 0, "c": 0, "points": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "Card", "times": "all"},
      {"seat": 2, "options_include": "Card", "times": "all"},
      {"seat": 3, "options_include": "Card", "times": "all"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 6, "2": 6, "3": 0}
    }
  }
]
```
````
