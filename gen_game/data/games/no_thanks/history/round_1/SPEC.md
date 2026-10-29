# No Thanks! Two Laps

Players pay a chip to refuse each card or take it with the pot. A card refused for two full laps is burned and its pot carries over. The lowest score of card points minus chips wins.

Players: 3 to 4, best with 4

## Parameters

- `card_min` = 3
- `card_max` = 35
- `total_cards` = 33
- `removed_cards` = 13
- `deck_size` = 20
- `starting_chips` = 11
- `pay_cost` = 1
- `laps_to_stay` = 1
- `laps_to_burn` = 2
- `first_lead_seat` = 1
- `rank_score_multiplier` = 100

## Round

1. **update** (table): Set taken = false. If current_card == 0 and deck is not empty: draw one card at random from deck, remove it from deck, set current_card to it and set lap_count = 0. pot is unchanged. Announce the current card and the pot.
2. **ask** (each player in turn, clockwise, starting at lead_seat, each seat once; a seat is skipped once taken == true): PAY: chips -= 1, pot += 1, announced publicly. TAKE: card_points += (current_card if (current_card-1) is not in tableau, else 0) - (current_card+1 if (current_card+1) is in tableau, else 0); append current_card to tableau; chips += pot; pot = 0; current_card = 0; lap_count = 0; lead_seat = this seat; taken = true. Announce the take and the number of chips gained.
3. **update** (table): When taken == false: lap_count += 1. Then, if lap_count == 2: append current_card to burned, set current_card = 0, set lap_count = 0, and set lead_seat = (lead_seat mod N) + 1. pot stays as it is. If lap_count == 1, the card stays current with its pot and lead_seat is unchanged.
4. **tell** (all players): Announce who paid, who took which card with how many chips (or that the card was burned), the pot, every tableau and every card_points.
5. **sync** (all players): Each player is sent their own state, including their private chips.
6. **update** (all players): When deck is empty and current_card == 0: each player's final_score = card_points - chips, and pot = 0 (leftover chips are out of the game).
7. **check** (table): End the game if deck is empty and current_card == 0; otherwise continue to the next round.

## Ending

- ends when: count(deck) == 0 and current_card == 0
- ranked by: `(you.chips - you.card_points) * 100 + you.chips` (the highest wins; players level at the top share the win)
- decided by: Final score is card points minus chips, and the lowest final score wins. Among players tied for lowest, the one with more chips wins. Players still tied share the win, which is a draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: This is the designer's count. With 3 or more players, the pot grows enough to make chicken-style refusal tense. More than 4 is not in the source and would stretch a 20-card deck thin.
- current_card = 0 stands for 'no current card': Real cards run from 3 to 35, so 0 is never a real card.
- Revealing the top deck card is a random draw from the hidden deck list: The deck is shuffled, so a random draw is equivalent to taking the top card.
- Offers use sequential ask, not poll: The rules make offers in clockwise order, and each player sees earlier payments and stops once someone takes.
- No talk step: The rules say there is no discussion phase.
- Strategy at the table: A thoughtful player tracks opponents' chips from the public pays and takes. They let the pot grow on cards that extend their own runs, and take a card early when a rival would want it or when their own chips run low.

## Simplifications

- The ranking is one expression: (chips - card_points) * 100 + chips: The engine ranks highest-wins. Negating the score makes lowest-score-wins, and since total chips (at most 44) are under 100, the trailing chips term breaks ties on more chips without disturbing the score order.
- A final_score attribute is computed at game end: It gives an observable score without revealing private chips during play.
- A scratch taken flag tracks whether the card was taken this round: It lets the round skip the remaining offers and decide between a lap and a take with arithmetic.

## Unsupported (needs engine work)

- none
