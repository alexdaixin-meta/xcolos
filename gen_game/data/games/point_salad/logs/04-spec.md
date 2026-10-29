# 04 spec

- time: 2026-10-27T17:23:02+00:00 (46.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 00e91d6581899bf6, reply sha256 095508df26c00ffd

## Sent

````
Game: Secret Salad
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP: There are three vegetables: Tomato (T), Lettuce (L), Carrot (C). There are three secret Recipes:
- Recipe TL is worth 2 per T + 2 per L + 2 per complete T-L pair (that is, 2 x the smaller of T and L).
- Recipe LC is worth 2 per L + 2 per C + 2 x the smaller of L and C.
- Recipe CT is worth 2 per C + 2 per T + 2 x the smaller of C and T.
Shuffle the three Recipes and deal one face down to each player. Each player sees only their own Recipe and knows the other two players hold the other two. Every player starts with T=0, L=0, C=0 and 0 points.

EACH ROUND (12 rounds):
1. Draw one point card at random, with replacement, from these 6 equally likely types:
- Tomato Fan: 2 points per T you hold.
- Lettuce Fan: 2 points per L you hold.
- Carrot Fan: 2 points per C you hold.
- Rainbow: 3 points per complete set of one T, one L and one C (3 x the smallest of your three counts).
- Big Bowl: 1 point per vegetable you hold (T+L+C).
- Balance: 6 points if you hold at least one of each vegetable and your largest count minus your smallest count is at most 1; otherwise 0.
2. Announce the round number, the point card, and every player's current T, L, C counts and points. Baskets and points are public; Recipes are not.
3. Talk: every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Talk is not binding and may be false.
4. Pick: every player simultaneously chooses exactly one of: Tomato, Lettuce, Carrot, or Card. The market each round holds exactly one Tomato, one Lettuce, one Carrot and the drawn point card.
5. Resolve: for each of the four options, count how many players chose it.
- If exactly one player chose a vegetable, that player adds 1 of it to their basket.
- If exactly one player chose Card, that player immediately scores the point card against their basket as it stands now, before this round's vegetables are added. Add those points to their total.
- If two or more players chose the same option, nobody receives it.
Unclaimed items are discarded.
6. Announce what every player picked and what they received.

END: After round 12, reveal all Recipes. Each player adds their Recipe score, computed on their final basket, to the points they earned from point cards. That sum is their final total.

How the winner is decided: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Secret Salad",
  "summary": "Three players each hold a secret Recipe that values two of three vegetables, and each round they pick at the same time from a market of one Tomato, one Lettuce, one Carrot and a random point card; any option two or more players pick goes to nobody.",
  "players": {"min": 3, "max": 3, "suggested": 3},
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
      {"key": "recipe", "type": "text", "visible": "ally", "initial": "", "meaning": "This player's secret Recipe: TL, LC or CT. It is revealed to all after round 12.", "observable": false},
      {"key": "t", "type": "number", "visible": "public", "initial": 0, "meaning": "Tomatoes in the basket.", "observable": true},
      {"key": "l", "type": "number", "visible": "public", "initial": 0, "meaning": "Lettuces in the basket.", "observable": true},
      {"key": "c", "type": "number", "visible": "public", "initial": 0, "meaning": "Carrots in the basket.", "observable": true},
      {"key": "points", "type": "number", "visible": "public", "initial": 0, "meaning": "Points earned from point cards.", "observable": true},
      {"key": "pick", "type": "text", "visible": "public", "initial": "", "meaning": "This round's pick: Tomato, Lettuce, Carrot or Card. It is collected by a simultaneous poll, so no one sees it until all picks are in.", "observable": true},
      {"key": "received", "type": "text", "visible": "public", "initial": "", "meaning": "What this player received this round: nothing, a vegetable, or the card points.", "observable": false},
      {"key": "recipe_score", "type": "number", "visible": "public", "initial": 0, "meaning": "Recipe score on the final basket. It is computed after round 12.", "observable": true},
      {"key": "final_total", "type": "number", "visible": "public", "initial": 0, "meaning": "points + recipe_score. It is computed after round 12.", "observable": true}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "The current round number, 1 to 12.", "observable": true},
      {"key": "recipe_deck", "type": "list", "visible": "none", "initial": ["TL", "LC", "CT"], "meaning": "The three Recipes, dealt one to each player at setup.", "observable": false},
      {"key": "card_types", "type": "list", "visible": "public", "initial": ["Tomato Fan", "Lettuce Fan", "Carrot Fan", "Rainbow", "Big Bowl", "Balance"], "meaning": "The six equally likely point card types. A draw picks one at random and does not remove it (with replacement).", "observable": false},
      {"key": "current_card", "type": "text", "visible": "public", "initial": "", "meaning": "The point card drawn this round.", "observable": true}
    ]
  },
  "setup": [
    "Shuffle recipe_deck (TL, LC, CT) and deal one Recipe at random into each player's recipe, removing it from recipe_deck, so that each player holds a different Recipe.",
    "Each player sees only their own recipe and knows the other two players hold the other two Recipes.",
    "Every player starts with t=0, l=0, c=0 and points=0; round=0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; current_card = one entry of card_types chosen at random, each of the 6 equally likely, without removing it (with replacement); every player's pick = '' and received = ''."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce round, current_card, and every player's t, l, c and points. Recipes are not shown."},
    {"action": "poll", "who": "all players", "answer": "short free text", "effect": "Each player writes one message without seeing the others. All messages are then broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding and may be false."},
    {"action": "poll", "who": "all players", "answer": "one of: Tomato, Lettuce, Carrot, Card", "effect": "Each player's pick is set to their choice. Picks are simultaneous."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Card resolves first, on baskets as they stand before this round's vegetables. If exactly one player has pick=='Card', that player's points += card value, where the card value is: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if min(t,l,c)>=1 and max(t,l,c)-min(t,l,c)<=1, else 0. Set that player's received to the points gained. If two or more players picked Card, nobody scores it."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If exactly one player has pick=='Tomato', that player's t += 1. If exactly one player has pick=='Lettuce', that player's l += 1. If exactly one player has pick=='Carrot', that player's c += 1. Set received for each of these players. Any vegetable picked by two or more players goes to nobody, and unclaimed items are discarded. Every player who received nothing gets received='nothing'."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every player's pick and received, and the updated t, l, c and points."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round==12, for each player: recipe_score = 2*t+2*l+2*min(t,l) if recipe=='TL'; 2*l+2*c+2*min(l,c) if recipe=='LC'; 2*c+2*t+2*min(c,t) if recipe=='CT'. Then final_total = points + recipe_score."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When round==12, reveal every player's recipe, recipe_score and final_total."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round==12; otherwise continue to the next round."}
  ],
  "ending": {
    "condition": "round == 12",
    "rank_by": "you.points + you.recipe_score",
    "decided_by": "Each player's final total is their point-card points plus their Recipe score on the final basket. The highest final total wins; players tied at the top share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "At setup, each of the 3 players is dealt a different Recipe from TL, LC, CT, visible only to that player."},
    {"id": "R2", "text": "At setup, every player has t=0, l=0, c=0 and points=0."},
    {"id": "R3", "text": "Each round, current_card is drawn at random with replacement from the 6 types Tomato Fan, Lettuce Fan, Carrot Fan, Rainbow, Big Bowl, Balance."},
    {"id": "R4", "text": "Each round, every player's t, l, c and points and the current_card are announced to all, while Recipes stay hidden."},
    {"id": "R5", "text": "Each round, every player writes one message simultaneously and all messages are then shown to everyone."},
    {"id": "R6", "text": "Each round, every player simultaneously picks exactly one of Tomato, Lettuce, Carrot, Card."},
    {"id": "R7", "text": "When exactly one player picks Tomato, then that player's t increases by 1."},
    {"id": "R8", "text": "When exactly one player picks Lettuce, then that player's l increases by 1."},
    {"id": "R9", "text": "When exactly one player picks Carrot, then that player's c increases by 1."},
    {"id": "R10", "text": "When two or more players pick the same option, then nobody receives that option."},
    {"id": "R11", "text": "When exactly one player picks Card, then that player scores the card on their basket as it stood before this round's vegetables are added."},
    {"id": "R12", "text": "When a player with t=3 scores Tomato Fan, then they gain 6 points (2 per T)."},
    {"id": "R13", "text": "When a player with l=2 scores Lettuce Fan, then they gain 4 points (2 per L)."},
    {"id": "R14", "text": "When a player with c=1 scores Carrot Fan, then they gain 2 points (2 per C)."},
    {"id": "R15", "text": "When a player with t=2, l=3, c=1 scores Rainbow, then they gain 3 points (3 x min)."},
    {"id": "R16", "text": "When a player with t=2, l=3, c=1 scores Big Bowl, then they gain 6 points (1 per vegetable)."},
    {"id": "R17", "text": "When a player with t=2, l=2, c=1 scores Balance, then they gain 6 points, because each count is at least 1 and max-min=1."},
    {"id": "R18", "text": "When a player with t=3, l=1, c=1 or with c=0 scores Balance, then they gain 0 points."},
    {"id": "R19", "text": "After each round, every player's pick and what they received are announced to all."},
    {"id": "R20", "text": "When round 12 ends, then the game ends and all Recipes are revealed."},
    {"id": "R21", "text": "When a TL player ends with t=3, l=2, then recipe_score=14 (2*3+2*2+2*2)."},
    {"id": "R22", "text": "When an LC player ends with l=1, c=4, then recipe_score=12 (2*1+2*4+2*1)."},
    {"id": "R23", "text": "When a CT player ends with c=2, t=2, then recipe_score=16."},
    {"id": "R24", "text": "Final total = points + recipe_score, and the highest final total wins, with players tied at the top sharing the win."}
  ],
  "offers": [
    {"question": "Talk message", "who": "all seats, simultaneously", "options": "Any short free-text message."},
    {"question": "Pick", "who": "all seats, simultaneously", "options": "Every seat, every round: Tomato, Lettuce, Carrot, Card."}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer set 3. The game needs exactly three Recipes split among three players, and three seats against four market items is what makes collisions and deduction interesting."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The rules specify simultaneous talk. Players disagree about which vegetables to take, since two Recipes overlap on each vegetable, so messages can steer or mislead picks."},
    {"what": "Card scored before vegetables in the same resolve", "why": "The rules say the card is scored on the basket as it stands before this round's vegetables are added, so the card update runs first."},
    {"what": "recipe_score and final_total stored as attributes computed after round 12", "why": "This makes the Recipe score explicit and checkable before ranking."},
    {"what": "Strategy at this table", "why": "A thoughtful player infers others' Recipes from their picks and talk, avoids collisions, contests the Card when it is valuable, and may bluff about their Recipe to send rivals elsewhere."}
  ],
  "simplifications": [
    {"what": "A tie for the highest total is treated as a shared win rather than a 'draw'", "why": "The engine ranks by one expression and players level at the top share the win, which carries the same outcome information."},
    {"what": "The Recipe reveal is an announcement", "why": "The recipe attribute stays ally-visible; the closing tell reveals every Recipe and score to all."}
  ],
  "unsupported": []
}
```
````
