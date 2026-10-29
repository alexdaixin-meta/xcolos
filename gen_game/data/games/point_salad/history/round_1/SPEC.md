# Secret Salad

Three players each hold a secret Recipe that values two of three vegetables, and each round they pick at the same time from a market of one Tomato, one Lettuce, one Carrot and a random point card; any option two or more players pick goes to nobody.

Players: 3 to 3, best with 3

## Parameters

- `players` = 3
- `rounds` = 12
- `recipe_per_vegetable` = 2
- `recipe_pair_bonus` = 2
- `card_types` = 6
- `fan_per_vegetable` = 2
- `rainbow_per_set` = 3
- `big_bowl_per_vegetable` = 1
- `balance_bonus` = 6
- `balance_max_spread` = 1
- `balance_min_each` = 1
- `market_vegetables_each` = 1
- `starting_count` = 0
- `starting_points` = 0

## Round

1. **update** (all players): round += 1; current_card = one entry of card_types chosen at random, each of the 6 equally likely, without removing it (with replacement); every player's pick = '' and received = ''.
2. **tell** (all players): Announce round, current_card, and every player's t, l, c and points. Recipes are not shown.
3. **poll** (all players): Each player writes one message without seeing the others. All messages are then broadcast to all as 'Seat {seat} says: {value}'. Talk is not binding and may be false.
4. **poll** (all players): Each player's pick is set to their choice. Picks are simultaneous.
5. **update** (all players): Card resolves first, on baskets as they stand before this round's vegetables. If exactly one player has pick=='Card', that player's points += card value, where the card value is: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if min(t,l,c)>=1 and max(t,l,c)-min(t,l,c)<=1, else 0. Set that player's received to the points gained. If two or more players picked Card, nobody scores it.
6. **update** (all players): If exactly one player has pick=='Tomato', that player's t += 1. If exactly one player has pick=='Lettuce', that player's l += 1. If exactly one player has pick=='Carrot', that player's c += 1. Set received for each of these players. Any vegetable picked by two or more players goes to nobody, and unclaimed items are discarded. Every player who received nothing gets received='nothing'.
7. **tell** (all players): Announce every player's pick and received, and the updated t, l, c and points.
8. **update** (all players): When round==12, for each player: recipe_score = 2*t+2*l+2*min(t,l) if recipe=='TL'; 2*l+2*c+2*min(l,c) if recipe=='LC'; 2*c+2*t+2*min(c,t) if recipe=='CT'. Then final_total = points + recipe_score.
9. **tell** (all players): When round==12, reveal every player's recipe, recipe_score and final_total.
10. **check** (all players): End the game if round==12; otherwise continue to the next round.

## Ending

- ends when: round == 12
- ranked by: `you.points + you.recipe_score` (the highest wins; players level at the top share the win)
- decided by: Each player's final total is their point-card points plus their Recipe score on the final basket. The highest final total wins; players tied at the top share the result (the source calls this a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer set 3. The game needs exactly three Recipes split among three players, and three seats against four market items is what makes collisions and deduction interesting.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous talk. Players disagree about which vegetables to take, since two Recipes overlap on each vegetable, so messages can steer or mislead picks.
- Card scored before vegetables in the same resolve: The rules say the card is scored on the basket as it stands before this round's vegetables are added, so the card update runs first.
- recipe_score and final_total stored as attributes computed after round 12: This makes the Recipe score explicit and checkable before ranking.
- Strategy at this table: A thoughtful player infers others' Recipes from their picks and talk, avoids collisions, contests the Card when it is valuable, and may bluff about their Recipe to send rivals elsewhere.

## Simplifications

- A tie for the highest total is treated as a shared win rather than a 'draw': The engine ranks by one expression and players level at the top share the win, which carries the same outcome information.
- The Recipe reveal is an announcement: The recipe attribute stays ally-visible; the closing tell reveals every Recipe and score to all.

## Unsupported (needs engine work)

- none
