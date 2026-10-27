# Point Salad: Secret Recipes

Three players each hold a secret two-vegetable Recipe. Over 12 rounds they talk, then all at once pick a vegetable or the shared scoring Card. Collisions shrink or cancel gains, and the highest points plus recipe score wins.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `rounds` = 12
- `card_types_count` = 6
- `fan_multiplier` = 2
- `rainbow_multiplier` = 3
- `big_bowl_multiplier` = 1
- `balance_value` = 6
- `balance_min_each` = 1
- `balance_max_spread` = 1
- `sole_vegetable_gain` = 2
- `pair_vegetable_gain` = 1
- `triple_vegetable_gain` = 0
- `recipe_first_weight` = 2
- `recipe_second_weight` = 2
- `recipe_min_weight` = 2
- `start_vegetables` = 0
- `start_points` = 0

## Round

1. **update** (all players): round += 1; card = one entry of card_types drawn at random, with replacement and equally likely; announce round and card to everyone
2. **update** (all players): for each player, card_value is set from the current t, l, c: Tomato Fan 2*t; Lettuce Fan 2*l; Carrot Fan 2*c; Rainbow 3*min(t,l,c); Big Bowl t+l+c; Balance 6 if t>=1 and l>=1 and c>=1 and max(t,l,c)-min(t,l,c)<=1, otherwise 0
3. **poll** (all players): message set for each player; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; messages bind no one
4. **poll** (all players): pick set for each player; nobody sees a pick until all are in
5. **update** (all players): n_card = number of players with pick == Card; n_t = number with pick == Tomato; n_l = number with pick == Lettuce; n_c = number with pick == Carrot
6. **update** (all players): for each player: if pick == Card and n_card == 1, then points += card_value; otherwise no change
7. **update** (all players): for each player: if pick == Tomato, t += 2 when n_t == 1, t += 1 when n_t == 2, and nothing when n_t == 3; the same for Lettuce with l and n_l, and for Carrot with c and n_c
8. **update** (all players): recipe_score set for each player: TL gives 2*t + 2*l + 2*min(t,l); LC gives 2*l + 2*c + 2*min(l,c); CT gives 2*c + 2*t + 2*min(c,t)
9. **tell** (all players): announce every player's pick, what each received (Card points or vegetables), and every player's t, l, c and points
10. **tell** (all players): when round == 12: reveal every player's recipe, recipe_score and points + recipe_score to everyone
11. **check** (all players): if round >= 12, end the game; otherwise start the next round

## Ending

- ends when: round >= 12
- ranked by: `you.points + you.recipe_score` (the highest wins; players level at the top share the win)
- decided by: Each player's final_total is points plus recipe_score. The highest final_total wins, and players tied at the top share a draw.

## Choices the source did not make

- 3 players, fixed: The designer fixed exactly 3: the three Recipes are all dealt and the collision rules (1, 2 or 3 pickers) are written for three seats.
- Keep simultaneous talk before the pick, as a poll with broadcast: The rules ask for simultaneous messages. Players clash over the Card and over shared vegetables, so a proposal can cost the one who follows it, and the talk gives players something to bluff and coordinate with.
- recipe_score is recomputed every round as owner-only state and revealed in the final round: The ranking needs it as an attribute, and computing it as the baskets change gives the same value at the end.
- Strategy at the table: A thoughtful player reads the public baskets to guess the others' secret Recipes and Card values, avoids colliding on the Card when another player has a big payoff, and uses talk to bluff or steer the others away from shared picks.

## Simplifications

- The Recipe reveal is an announcement step that runs when round == 12, before the end check: The engine has no separate end phase. The reveal is equivalent and does not change scoring.

## Unsupported (needs engine work)

- none
