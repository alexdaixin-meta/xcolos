# Jaipur Bazaar (Balanced Schedule)

Two traders take turns over 16 rounds, taking goods and camels from a public market and selling sets of goods for falling prices. A camel-majority bonus is paid at the end, and the higher score wins.

Players: 2 to 2, best with 2

## Parameters

- `rounds` = 16
- `price_diamond_start` = 7
- `price_silver_start` = 5
- `price_cloth_start` = 3
- `deck_diamond` = 5
- `deck_silver` = 7
- `deck_cloth` = 8
- `deck_size` = 20
- `market_camel_start` = 2
- `market_silver_start` = 1
- `market_cloth_start` = 1
- `market_diamond_start` = 0
- `start_hand_silver` = 1
- `start_hand_cloth` = 1
- `start_camels` = 1
- `start_score` = 0
- `hand_limit` = 7
- `restock_per_round` = 1
- `draws_per_round` = 1
- `take_min` = 1
- `sell_min_diamond` = 2
- `sell_min_silver` = 2
- `sell_min_cloth` = 1
- `bonus_sell_3` = 3
- `bonus_sell_4` = 5
- `bonus_sell_5_plus` = 8
- `price_floor` = 1
- `camel_majority_bonus` = 5

## Round

1. **update** (all players): round += 1; first_seat = 1 if round in {1,4,5,8,9,12,13,16} else 2. Announce the round and the first seat.
2. **update** (all players): Restock by the public schedule: market_cloth += 1 if round in {1,2,9,10}; market_silver += 1 if round in {3,4,11,12}; market_camel += 1 if round in {5,6,15,16}; market_diamond += 1 if round in {7,8,13,14}. Announce the card added.
3. **update** (seat first_seat): Private draw: remove one random card from deck. If first player's diamond+silver+cloth < 7, add 1 to that player's matching count; otherwise append the card to discard. Set that player's last_draw to the card type and kept/discarded. Tell all players only that a draw happened.
4. **sync** (seat first_seat): The first player sees their own hand, including the drawn card type (last_draw), plus all public state.
5. **ask** (seat first_seat): TAKE g n (when market_g >= n, camels >= n-1, and diamond+silver+cloth+n <= 7): market_g -= n, player g += n, camels -= n-1, market_camel += n-1. CAMELS (when market_camel >= 1): camels += market_camel, market_camel = 0. SELL g n (when player g >= n, and n >= 2 for diamond/silver or n >= 1 for cloth): player g -= n, append n cards to discard, score += n*price_g + (3 if n==3, 5 if n==4, 8 if n>=5, else 0), price_g = max(1, price_g - n). An illegal or missing answer is a pass: nothing changes. Set last_action to the action type, good and n.
6. **tell** (all players): Announce publicly: 'Seat {first_seat} did {last_action}', then the market, prices, herds and scores. No drawn card type is announced.
7. **sync** (the seat that is not first_seat): The second player sees their own hand and all public state.
8. **ask** (the seat that is not first_seat): Same resolution as the first player's turn, applied to the second player. An illegal or missing answer is a pass. Set last_action.
9. **tell** (all players): Announce publicly: 'Seat {second seat} did {last_action}', then the market, prices, herds and scores.
10. **update** (all players): When round == 16: if seat 1 camels > seat 2 camels, seat 1 score += 5; if seat 2 camels > seat 1 camels, seat 2 score += 5; if they are tied, no change. Cards left in hand score nothing. Announce the final scores.
11. **check** (all players): End the game when round == 16; otherwise continue to the next round.

## Ending

- ends when: round == 16
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score after the camel-majority bonus. The higher score wins, and equal scores share the win (a draw).

## Choices the source did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed 2. The turn-order schedule, the camel majority and the market race are all built for two rivals, so a third seat would break the schedule.
- Seat 1 is player A and seat 2 is player B: The source names A and B. Mapping them to seats lets the turn-order schedule be applied.
- Only legal actions are offered, with PASS offered only when nothing is legal: The platform asks that a seat is never offered what it may not do. The source's illegal-is-a-pass rule is kept as a fallback for missing answers.
- No free talk step: The source has no talk. It is a pure two-player race, and talk would add words without changing incentives.
- The camel bonus is applied in an update step that runs only when round == 16, just before the ending check: This places the 'after round 16' bonus in a single step with a condition.
- Strategy at this table: A thoughtful player times sales before prices fall, uses private draws to plan set bonuses, takes camels to win the +5 majority or to fund multi-card takes, and denies the opponent restocked goods using the public schedule.

## Simplifications

- The deck is a hidden table list, and the 'top card' is drawn at random from it: Drawing at random from a shuffled list is equivalent to taking the top card of a deck shuffled once.
- Turn order is implemented as two ask steps addressed to first_seat and then to the other seat: The engine's step list is fixed. The acting seat is chosen from the table attribute first_seat.

## Unsupported (needs engine work)

- none
