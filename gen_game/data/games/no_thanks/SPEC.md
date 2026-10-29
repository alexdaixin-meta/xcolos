# No Thanks! (Two-Lap)

Players pay chips to refuse unwanted numbered cards or take the card with its chip pot. A card nobody takes in two full laps is burned. The lowest card points minus chips wins.

Players: 3 to 4, best with 4

## Parameters

- `card_min` = 3
- `card_max` = 35
- `total_cards` = 33
- `deck_size` = 20
- `removed_count` = 13
- `starting_chips` = 11
- `pay_cost` = 1
- `burn_laps` = 2
- `max_rounds` = 40
- `no_card` = 0

## Round

1. **update** (all players): Set round_count += 1. When current_card = 0 and deck is not empty, draw one card at random from deck and set current_card to it, removing it from deck. The pot is not reset.
2. **tell** (all players): Announce current_card, pot, every tableau and the burned list.
3. **ask** (seat ((lead_seat - 1 + 0) mod N) + 1 (offer k=1); runs only when current_card != 0): PAY: that seat's chips -= 1 and pot += 1. TAKE: c = current_card; card_points += c; if c+1 is in tableau, card_points -= c+1; if c-1 is in tableau, card_points -= c; append c to tableau; chips += pot; pot = 0; current_card = 0; lap_count = 0; lead_seat = this seat.
4. **ask** (seat ((lead_seat - 1 + 1) mod N) + 1 (offer k=2); runs only when current_card != 0): Same as offer k=1.
5. **ask** (seat ((lead_seat - 1 + 2) mod N) + 1 (offer k=3); runs only when current_card != 0): Same as offer k=1.
6. **ask** (seat ((lead_seat - 1 + 3) mod N) + 1 (offer k=4); runs only when N = 4 and current_card != 0): Same as offer k=1.
7. **update** (all players): LAP: when current_card != 0, lap_count += 1.
8. **update** (all players): BURN: when current_card != 0 and lap_count >= 2, append current_card to burned, then set current_card = 0 and lap_count = 0. pot and lead_seat are unchanged.
9. **sync** (all players): Send each player its own chips and the public state.
10. **check** (all players): End the game when (current_card = 0 and deck is empty) or round_count >= 40. Otherwise continue.
11. **repeat** (all players): Run the round steps again until the check ends the game. At the end, reveal every player's chips and tableau to all players.

## Ending

- ends when: (current_card = 0 and count(deck) = 0) or round_count >= 40
- ranked by: `you.chips - you.card_points` (the highest wins; players level at the top share the win)
- decided by: A player's final score is card_points minus chips, and the lowest score wins. The ranking uses chips minus card_points, so the highest value wins, and players tied for the lowest score share the win (a draw among them).

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer chose 4. At 3 the chip pressure and the pot-baiting still work; above 4 the source rules do not apply.
- No talk phase: The rules say there is no talk. The tension comes from reading the pot and the other players' tableaus.
- card_points is public: Tableaus are public, so card_points can be worked out by anyone anyway. Making it visible changes no information.
- Ranking uses chips - card_points: The engine treats the highest value as the winner, so the lowest score becomes the highest negated score.
- A round_count scratch counter: It is needed to enforce the 40-round cap.

## Simplifications

- The clockwise offer loop is written as up to N separate ask steps, each with a seat formula and a when condition: The engine has a flat step list. The formula reproduces the clockwise order from lead_seat, and the condition skips offers once the card is taken.
- Drawing the top deck card is a random draw from the deck list: The deck is in random order, so drawing at random is equivalent.

## Unsupported (needs engine work)

- none
