# Speicherstadt Queues (Even Rotation)

Over 12 rounds, 3-4 merchants secretly queue workers on three goods lots each round and buy through a falling-price offer that runs in a rotating priority order, trying to collect their hidden contract colour.

Players: 3 to 4, best with 4

## Parameters

- `colours` = 6
- `cards_per_colour` = 6
- `deck_size` = 36
- `rounds` = 12
- `lots_per_round` = 3
- `starting_coins` = 6
- `income_per_round` = 2
- `workers_per_player` = 2
- `limit_min` = 0
- `limit_max` = 6
- `lowest_offer_price` = 1
- `price_drop_per_decline` = 1
- `contract_good_points` = 5
- `other_good_points` = 2
- `coin_points` = 1
- `tiebreak_multiplier` = 100

## Round

1. **update** (table): round += 1; draw three cards at random from deck into lot1, lot2 and lot3, removing each from deck; announce the three lot colours.
2. **update** (all players): every player's coins += 2.
3. **update** (table): priority_start = ((round - 1) mod N) + 1; announce the priority order: priority_start, then the following seats in seat order, wrapping from N to 1.
4. **poll** (all players): after all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
5. **poll** (all players): set each player's limit1; answers are never revealed.
6. **poll** (all players): set each player's limit2; answers are never revealed.
7. **poll** (all players): set each player's limit3; answers are never revealed.
8. **update** (all players): worker cap of 2: for each player, if limit1 > 0 and limit2 > 0 and limit3 > 0, then limit3 = 0.
9. **update** (table): resolve Lot 1, setup: queue_len = count of players with limit1 > 0; offer_price = queue_len; lot_sold = false.
10. **update** (each player in priority order (positions 1..N, starting at priority_start)): resolve Lot 1, offers (one step per priority position): when lot_sold is false and this player's limit1 > 0, then if limit1 >= offer_price and coins >= offer_price, the player's coins -= offer_price, lot1 is appended to the player's goods, own_goods += 1 if lot1 == contract, and lot_sold = true; otherwise offer_price -= 1. Players with limit1 = 0 are skipped.
11. **update** (table): when lot_sold is false, append lot1 to discard (this covers an empty queue too).
12. **update** (table): resolve Lot 2, setup: queue_len = count of players with limit2 > 0; offer_price = queue_len; lot_sold = false.
13. **update** (each player in priority order (positions 1..N, starting at priority_start)): resolve Lot 2, offers: the same as Lot 1, using limit2 and lot2; coins spent on Lot 1 this round count in the coins check.
14. **update** (table): when lot_sold is false, append lot2 to discard.
15. **update** (table): resolve Lot 3, setup: queue_len = count of players with limit3 > 0; offer_price = queue_len; lot_sold = false.
16. **update** (each player in priority order (positions 1..N, starting at priority_start)): resolve Lot 3, offers: the same as Lot 1, using limit3 and lot3; coins spent earlier this round count in the coins check.
17. **update** (table): when lot_sold is false, append lot3 to discard.
18. **tell** (all players): announce, for each lot, which seats queued (a positive limit), who bought it if anyone, and the price paid; also every player's coins and goods. Limits are not revealed.
19. **update** (all players): when round == 12: score = coins + 5 * own_goods + 2 * (length(goods) - own_goods); reveal every player's contract to all.
20. **check** (table): end the game if round >= 12 (the deck is then empty); otherwise continue to the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.score * 100 + you.own_goods` (the highest wins; players level at the top share the win)
- decided by: Highest final score (coins + 5 per good of own contract colour + 2 per other good) wins. A tie is broken by more goods of own contract colour. Players still level share the win, which is a draw among them.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer chose 4, and the even rotation needs 12/N to be a whole number, which holds for 3 and 4. Three is the smallest table where two rivals contest a lot and the queue price ladder matters. Above 4, 6 contract colours and 3 lots per round get too thin. The strategy is to infer rivals' contracts from their purchases and talk, to bluff about your own, and to time your bids around the rounds where you hold priority.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Players compete for lots and hide their contracts, so talk invites bluffing and deterrence that could cost a player who believes it.
- Tie-break encoded as score * 100 + own_goods: own_goods is at most 6, which is below 100, so this ranks by score and then by own-contract goods. Players level on both share the win, which is the source's draw.
- Contracts marked not observable: They are hidden during play and revealed only at the end; the score is the observable outcome.

## Simplifications

- The three limits are collected as three consecutive simultaneous polls instead of one combined submission: The engine takes one number per question. Limits are never revealed, so no player learns anything between the polls.
- The falling-price offer is unrolled into one conditional update per priority position for each lot: The step list is flat. Up to N fixed steps with when/if conditions reproduce the sequential offer exactly.
- Final scoring and the contract reveal are a conditional update in round 12, just before the end check: The score must be computed before the arithmetic ranking runs.

## Unsupported (needs engine work)

- none
