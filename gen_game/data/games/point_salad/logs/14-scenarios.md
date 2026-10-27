# 14 scenarios

- time: 2026-10-27T17:31:06+00:00 (68.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 a7c2cc8ed1412953, reply sha256 20ee651daa0a13bc

## Sent

````
SPEC:
{
  "name": "Secret Salad",
  "summary": "Three players each hold a secret Recipe that values two of three vegetables, and each round they pick at the same time from a market of one Tomato, one Lettuce, one Carrot and a random point card; any option two or more players pick goes to nobody.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "players": 3,
    "rounds": 12,
    "recipe_per_vegetable": 2,
    "recipe_pair_bonus": 2,
    "card_types": 6,
    "fan_per_vegetable": 2,
    "rainbow_per_set": 3,
    "big_bowl_per_vegetable": 1,
    "balance_bonus": 6,
    "balance_max_spread": 1,
    "balance_min_each": 1,
    "market_vegetables_each": 1,
    "starting_count": 0,
    "starting_points": 0
  },
  "attributes": {
    "player": [
      {
        "key": "recipe",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This player's secret Recipe: TL, LC or CT. It is revealed to all after round 12.",
        "observable": false
      },
      {
        "key": "t",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tomatoes in the basket.",
        "observable": true
      },
      {
        "key": "l",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Lettuces in the basket.",
        "observable": true
      },
      {
        "key": "c",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Carrots in the basket.",
        "observable": true
      },
      {
        "key": "points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points earned from point cards.",
        "observable": true
      },
      {
        "key": "pick",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's pick: Tomato, Lettuce, Carrot or Card. It is collected by a simultaneous poll, so no one sees it until all picks are in.",
        "observable": true
      },
      {
        "key": "received",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "What this player received this round: nothing, a vegetable, or the card points.",
        "observable": false
      },
      {
        "key": "recipe_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Recipe score on the final basket. It is computed after round 12.",
        "observable": true
      },
      {
        "key": "final_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points + recipe_score. It is computed after round 12.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round number, 1 to 12.",
        "observable": true
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
        "meaning": "The three Recipes, dealt one to each player at setup.",
        "observable": false
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
        "meaning": "The six equally likely point card types. A draw picks one at random and does not remove it (with replacement).",
        "observable": false
      },
      {
        "key": "current_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The point card drawn this round.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Shuffle recipe_deck (TL, LC, CT) and deal one Recipe at random into each player's recipe, removing it from recipe_deck, so that each player holds a different Recipe.",
    "Each player sees only their own recipe and knows the other two players hold the other two Recipes.",
    "Every player starts with t=0, l=0, c=0 and points=0; round=0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; current_card = one entry of card_types chosen at random, each of the 6 equally likely, without removing it (with replacement); every player's pick = '' and received = ''."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, current_card, and every player's t, l, c and points. Recipes are not shown."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short free text",
      "effect": "Each player writes one message without seeing the others. All messages are then broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding and may be false."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Tomato, Lettuce, Carrot, Card",
      "effect": "Each player's pick is set to their choice. Picks are simultaneous."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Card resolves first, on baskets as they stand before this round's vegetables. If exactly one player has pick=='Card', that player's points += card value, where the card value is: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if min(t,l,c)>=1 and max(t,l,c)-min(t,l,c)<=1, else 0. Set that player's received to the points gained. If two or more players picked Card, nobody scores it."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If exactly one player has pick=='Tomato', that player's t += 1. If exactly one player has pick=='Lettuce', that player's l += 1. If exactly one player has pick=='Carrot', that player's c += 1. Set received for each of these players. Any vegetable picked by two or more players goes to nobody, and unclaimed items are discarded. Every player who received nothing gets received='nothing'."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's pick and received, and the updated t, l, c and points."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round==12, for each player: recipe_score = 2*t+2*l+2*min(t,l) if recipe=='TL'; 2*l+2*c+2*min(l,c) if recipe=='LC'; 2*c+2*t+2*min(c,t) if recipe=='CT'. Then final_total = points + recipe_score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round==12, reveal every player's recipe, recipe_score and final_total."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round==12; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.points + you.recipe_score",
    "decided_by": "Each player's final total is their point-card points plus their Recipe score on the final basket. The highest final total wins; players tied at the top share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, each of the 3 players is dealt a different Recipe from TL, LC, CT, visible only to that player."
    },
    {
      "id": "R2",
      "text": "At setup, every player has t=0, l=0, c=0 and points=0."
    },
    {
      "id": "R3",
      "text": "Each round, current_card is drawn at random with replacement from the 6 types Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance."
    },
    {
      "id": "R4",
      "text": "Each round, every player's t, l, c and points and the current_card are announced to all, while Recipes stay hidden."
    },
    {
      "id": "R5",
      "text": "Each round, every player writes one message simultaneously and all messages are then shown to everyone."
    },
    {
      "id": "R6",
      "text": "Each round, every player simultaneously picks exactly one of Tomato, Lettuce, Carrot, Card."
    },
    {
      "id": "R7",
      "text": "When exactly one player picks Tomato, then that player's t increases by 1."
    },
    {
      "id": "R8",
      "text": "When exactly one player picks Lettuce, then that player's l increases by 1."
    },
    {
      "id": "R9",
      "text": "When exactly one player picks Carrot, then that player's c increases by 1."
    },
    {
      "id": "R10",
      "text": "When two or more players pick the same option, then nobody receives that option."
    },
    {
      "id": "R11",
      "text": "When exactly one player picks Card, then that player scores the card on their basket as it stood before this round's vegetables are added."
    },
    {
      "id": "R12",
      "text": "When a player with t=3 scores Tomato Fan, then they gain 6 points (2 per T)."
    },
    {
      "id": "R13",
      "text": "When a player with l=2 scores Lettuce Fan, then they gain 4 points (2 per L)."
    },
    {
      "id": "R14",
      "text": "When a player with c=1 scores Carrot Fan, then they gain 2 points (2 per C)."
    },
    {
      "id": "R15",
      "text": "When a player with t=2, l=3, c=1 scores Rainbow, then they gain 3 points (3 x min)."
    },
    {
      "id": "R16",
      "text": "When a player with t=2, l=3, c=1 scores Big Bowl, then they gain 6 points (1 per vegetable)."
    },
    {
      "id": "R17",
      "text": "When a player with t=2, l=2, c=1 scores Balance, then they gain 6 points, because each count is at least 1 and max-min=1."
    },
    {
      "id": "R18",
      "text": "When a player with t=3, l=1, c=1 or with c=0 scores Balance, then they gain 0 points."
    },
    {
      "id": "R19",
      "text": "After each round, every player's pick and what they received are announced to all."
    },
    {
      "id": "R20",
      "text": "When round 12 ends, then the game ends and all Recipes are revealed."
    },
    {
      "id": "R21",
      "text": "When a TL player ends with t=3, l=2, then recipe_score=14 (2*3+2*2+2*2)."
    },
    {
      "id": "R22",
      "text": "When an LC player ends with l=1, c=4, then recipe_score=12 (2*1+2*4+2*1)."
    },
    {
      "id": "R23",
      "text": "When a CT player ends with c=2, t=2, then recipe_score=16."
    },
    {
      "id": "R24",
      "text": "Final total = points + recipe_score, and the highest final total wins, with players tied at the top sharing the win."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all seats, simultaneously",
      "options": "Any short free-text message."
    },
    {
      "question": "Pick",
      "who": "all seats, simultaneously",
      "options": "Every seat, every round: Tomato, Lettuce, Carrot, Card."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer set 3. The game needs exactly three Recipes split among three players, and three seats against four market items is what makes collisions and deduction interesting."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules specify simultaneous talk. Players disagree about which vegetables to take, since two Recipes overlap on each vegetable, so messages can steer or mislead picks."
    },
    {
      "what": "Card scored before vegetables in the same resolve",
      "why": "The rules say the card is scored on the basket as it stands before this round's vegetables are added, so the card update runs first."
    },
    {
      "what": "recipe_score and final_total stored as attributes computed after round 12",
      "why": "This makes the Recipe score explicit and checkable before ranking."
    },
    {
      "what": "Strategy at this table",
      "why": "A thoughtful player infers others' Recipes from their picks and talk, avoids collisions, contests the Card when it is valuable, and may bluff about their Recipe to send rivals elsewhere."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest total is treated as a shared win rather than a 'draw'",
      "why": "The engine ranks by one expression and players level at the top share the win, which carries the same outcome information."
    },
    {
      "what": "The Recipe reveal is an announcement",
      "why": "The recipe attribute stays ally-visible; the closing tell reveals every Recipe and score to all."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: t, l, c, points, pick, recipe_score, final_total; table: round, current_card.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Never override `card_types` with a list. It is the number of card types (6) and must stay a number. The test cannot force a specific card through it.

Do not predict which card a random draw produces. Write assertions that hold whatever card is drawn:
- **R3:** after each round, `current_card` is one of the six names Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance.
- **R10:** when two or more players pick Card, every player's `points` stays unchanged, whatever card was drawn.
- **R11 and R12:** set up baskets where every possible card gives a known score, and check that only the sole Card picker's `points` changes. For example, with an empty basket every card scores 0, so check that a player who picks Card on an empty basket gains 0 even after collecting vegetables that same round. Otherwise, check the gain against the formula for whichever `current_card` was actually announced.
- **Fan values (R12):** checking a specific value such as Tomato Fan with t=3 giving 6 requires knowing the drawn card. Either assert conditionally on the announced `current_card`, or drop the scenario.

Assert on results and scores, not on internal pools.
````

## Reply

````
[
{"name":"R1 setup: no turn played yet, every seat starts empty (recipes are hidden, so only the clean start is checked)","rule":"R1","players":3,"rounds":0,
 "expect":{"game":{"round":0},"players":{"1":{"t":0,"l":0,"c":0,"points":0},"2":{"t":0,"l":0,"c":0,"points":0},"3":{"t":0,"l":0,"c":0,"points":0}}}},
{"name":"R2 setup: every player has t=l=c=0 and points=0","rule":"R2","players":3,"rounds":0,
 "expect":{"game":{"round":0},"players":{"1":{"t":0,"l":0,"c":0,"points":0},"2":{"t":0,"l":0,"c":0,"points":0},"3":{"t":0,"l":0,"c":0,"points":0}}}},
{"name":"R3 a round draws a card and advances the round; all pick Card so the draw cannot change any score","rule":"R3","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"game":{"round":1},"players":{"1":{"points":0},"2":{"points":0},"3":{"points":0}}}},
{"name":"R4 baskets and points carry through a round where everybody collides on Card","rule":"R4","players":3,"rounds":1,
 "given":{"players":{"1":{"t":2,"l":1,"c":0,"points":5},"2":{"t":0,"l":3,"c":1,"points":2},"3":{"t":1,"l":0,"c":4,"points":0}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"players":{"1":{"t":2,"l":1,"c":0,"points":5},"2":{"t":0,"l":3,"c":1,"points":2},"3":{"t":1,"l":0,"c":4,"points":0}}}},
{"name":"R5 the talk poll happens and play continues normally","rule":"R5","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Tomato","times":"all"},{"seat":2,"options_include":"Lettuce","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"game":{"round":1},"players":{"1":{"t":1},"2":{"l":1},"3":{"c":1}}}},
{"name":"R6 every seat is offered Tomato, Lettuce, Carrot and Card","rule":"R6","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Tomato","times":"all"},{"seat":2,"options_include":"Lettuce","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"offered":[{"seat":1,"option":"Tomato"},{"seat":1,"option":"Lettuce"},{"seat":1,"option":"Carrot"},{"seat":1,"option":"Card"},
  {"seat":2,"option":"Tomato"},{"seat":2,"option":"Lettuce"},{"seat":2,"option":"Carrot"},{"seat":2,"option":"Card"},
  {"seat":3,"option":"Tomato"},{"seat":3,"option":"Lettuce"},{"seat":3,"option":"Carrot"},{"seat":3,"option":"Card"}],
  "players":{"1":{"pick":"Tomato"},"2":{"pick":"Lettuce"},"3":{"pick":"Carrot"}}}},
{"name":"R7 the sole Tomato picker gains one tomato; two Card pickers score nothing","rule":"R7","players":3,"rounds":1,
 "given":{"players":{"1":{"t":1},"2":{"t":2,"points":3},"3":{"l":2}}},
 "rules":[{"seat":1,"options_include":"Tomato","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"players":{"1":{"t":2,"l":0,"c":0,"points":0},"2":{"t":2,"points":3},"3":{"l":2,"points":0}}}},
{"name":"R8 the sole Lettuce picker gains one lettuce","rule":"R8","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Lettuce","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"players":{"1":{"t":0,"l":0,"c":0,"points":0},"2":{"t":0,"l":1,"c":0,"points":0},"3":{"t":0,"l":0,"c":0,"points":0}}}},
{"name":"R9 the sole Carrot picker gains one carrot","rule":"R9","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"players":{"1":{"t":0,"l":0,"c":0,"points":0},"2":{"t":0,"l":0,"c":0,"points":0},"3":{"t":0,"l":0,"c":1,"points":0}}}},
{"name":"R10 two Tomato pickers get nothing; the sole Card picker on an empty basket gains 0 whatever card is drawn","rule":"R10","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Tomato","times":"all"},{"seat":2,"options_include":"Tomato","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"players":{"1":{"t":0,"points":0},"2":{"t":0,"points":0},"3":{"t":0,"l":0,"c":0,"points":0}}}},
{"name":"R10 three Card pickers on full baskets: nobody scores, whatever card is drawn","rule":"R10","players":3,"rounds":1,
 "given":{"players":{"1":{"t":3,"l":3,"c":3,"points":1},"2":{"t":2,"l":2,"c":1,"points":4},"3":{"t":5,"l":0,"c":2,"points":0}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"players":{"1":{"points":1,"t":3,"l":3,"c":3},"2":{"points":4,"t":2,"l":2,"c":1},"3":{"points":0,"t":5,"l":0,"c":2}}}},
{"name":"R11 the sole Card picker on an empty basket gains 0 whatever card is drawn, while others collect vegetables","rule":"R11","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Tomato","times":"all"},{"seat":3,"options_include":"Lettuce","times":"all"}],
 "expect":{"players":{"1":{"t":0,"l":0,"c":0,"points":0,"pick":"Card"},"2":{"t":1,"points":0},"3":{"l":1,"points":0}}}},
{"name":"R12 sole Card picker with t=3: basket unchanged, other seats' points unchanged (card value depends on the draw, not asserted)","rule":"R12","players":3,"rounds":1,
 "given":{"players":{"1":{"t":3},"2":{"points":2},"3":{"points":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Tomato","times":"all"},{"seat":3,"options_include":"Tomato","times":"all"}],
 "expect":{"players":{"1":{"t":3,"l":0,"c":0,"pick":"Card"},"2":{"t":0,"points":2},"3":{"t":0,"points":1}}}},
{"name":"R13 sole Card picker with l=2: basket unchanged, other seats unaffected (card value depends on the draw)","rule":"R13","players":3,"rounds":1,
 "given":{"players":{"1":{"l":2}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Lettuce","times":"all"},{"seat":3,"options_include":"Lettuce","times":"all"}],
 "expect":{"players":{"1":{"t":0,"l":2,"c":0,"pick":"Card"},"2":{"l":0,"points":0},"3":{"l":0,"points":0}}}},
{"name":"R14 sole Card picker with c=1: basket unchanged, other seats unaffected (card value depends on the draw)","rule":"R14","players":3,"rounds":1,
 "given":{"players":{"1":{"c":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Carrot","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"players":{"1":{"t":0,"l":0,"c":1,"pick":"Card"},"2":{"c":0,"points":0},"3":{"c":0,"points":0}}}},
{"name":"R15 sole Card picker with t=2,l=3,c=1: basket unchanged, others collect normally (card value depends on the draw)","rule":"R15","players":3,"rounds":1,
 "given":{"players":{"1":{"t":2,"l":3,"c":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Tomato","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"players":{"1":{"t":2,"l":3,"c":1},"2":{"t":1,"points":0},"3":{"c":1,"points":0}}}},
{"name":"R16 sole Card picker with t=2,l=3,c=1: basket unchanged, others unaffected (card value depends on the draw)","rule":"R16","players":3,"rounds":1,
 "given":{"players":{"1":{"t":2,"l":3,"c":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Lettuce","times":"all"},{"seat":3,"options_include":"Lettuce","times":"all"}],
 "expect":{"players":{"1":{"t":2,"l":3,"c":1,"pick":"Card"},"2":{"l":0,"points":0},"3":{"l":0,"points":0}}}},
{"name":"R17 sole Card picker with t=2,l=2,c=1: basket unchanged, others unaffected (card value depends on the draw)","rule":"R17","players":3,"rounds":1,
 "given":{"players":{"1":{"t":2,"l":2,"c":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Carrot","times":"all"},{"seat":3,"options_include":"Carrot","times":"all"}],
 "expect":{"players":{"1":{"t":2,"l":2,"c":1,"pick":"Card"},"2":{"c":0,"points":0},"3":{"c":0,"points":0}}}},
{"name":"R18 sole Card picker with t=3,l=1,c=1: basket unchanged, others unaffected (card value depends on the draw)","rule":"R18","players":3,"rounds":1,
 "given":{"players":{"1":{"t":3,"l":1,"c":1}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Tomato","times":"all"},{"seat":3,"options_include":"Tomato","times":"all"}],
 "expect":{"players":{"1":{"t":3,"l":1,"c":1,"pick":"Card"},"2":{"t":0,"points":0},"3":{"t":0,"points":0}}}},
{"name":"R19 each player's pick is recorded and shown after the round","rule":"R19","players":3,"rounds":1,
 "rules":[{"seat":1,"options_include":"Carrot","times":"all"},{"seat":2,"options_include":"Carrot","times":"all"},{"seat":3,"options_include":"Lettuce","times":"all"}],
 "expect":{"players":{"1":{"pick":"Carrot","c":0},"2":{"pick":"Carrot","c":0},"3":{"pick":"Lettuce","l":1}}}},
{"name":"R20 the game ends after round 12; empty baskets give everyone 0, so all share the win","rule":"R20","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL"},"2":{"recipe":"LC"},"3":{"recipe":"CT"}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":[1,2,3],"standings":{"1":0,"2":0,"3":0},"game":{"round":12},
  "players":{"1":{"recipe_score":0,"final_total":0},"2":{"recipe_score":0,"final_total":0},"3":{"recipe_score":0,"final_total":0}}}},
{"name":"R21 TL player ending with t=3,l=2 scores recipe 14","rule":"R21","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL","t":3,"l":2},"2":{"recipe":"LC"},"3":{"recipe":"CT"}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":1,"standings":{"1":14,"2":0,"3":0},"players":{"1":{"recipe_score":14,"final_total":14},"2":{"recipe_score":0},"3":{"recipe_score":0}}}},
{"name":"R22 LC player ending with l=1,c=4 scores recipe 12","rule":"R22","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL"},"2":{"recipe":"LC","l":1,"c":4},"3":{"recipe":"CT"}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":2,"standings":{"1":0,"2":12,"3":0},"players":{"2":{"recipe_score":12,"final_total":12},"1":{"recipe_score":0},"3":{"recipe_score":0}}}},
{"name":"R23 CT player ending with c=2,t=2 scores recipe 16","rule":"R23","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL"},"2":{"recipe":"LC"},"3":{"recipe":"CT","c":2,"t":2}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":3,"standings":{"1":0,"2":0,"3":16},"players":{"3":{"recipe_score":16,"final_total":16},"1":{"recipe_score":0},"2":{"recipe_score":0}}}},
{"name":"R24 final total adds points to recipe score; a tie at the top is shared","rule":"R24","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL","t":3,"l":2,"points":0},"2":{"recipe":"LC","l":1,"c":4,"points":2},"3":{"recipe":"CT","points":5}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":[1,2],"standings":{"1":14,"2":14,"3":5},
  "players":{"1":{"recipe_score":14,"final_total":14},"2":{"recipe_score":12,"final_total":14},"3":{"recipe_score":0,"final_total":5}}}},
{"name":"R24 points can decide the winner over a higher recipe score","rule":"R24","players":3,
 "given":{"game":{"round":11},"players":{"1":{"recipe":"TL","t":3,"l":2,"points":3},"2":{"recipe":"LC"},"3":{"recipe":"CT","c":2,"t":2,"points":0}}},
 "rules":[{"seat":1,"options_include":"Card","times":"all"},{"seat":2,"options_include":"Card","times":"all"},{"seat":3,"options_include":"Card","times":"all"}],
 "expect":{"winner":1,"standings":{"1":17,"2":0,"3":16},
  "players":{"1":{"recipe_score":14,"final_total":17},"2":{"recipe_score":0,"final_total":0},"3":{"recipe_score":16,"final_total":16}}}}
]
````
