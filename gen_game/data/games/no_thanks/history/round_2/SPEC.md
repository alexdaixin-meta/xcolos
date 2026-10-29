# No Thanks! (Bounded Laps)

Players pay one chip to refuse a card or take it with the pot. Each card may circle the table at most twice before it is burned. The lowest score, card points minus chips, wins.

Players: 3 to 4, best with 4

## Parameters

- `card_min` = 3
- `card_max` = 35
- `card_total` = 33
- `cards_removed` = 13
- `deck_size` = 20
- `starting_chips` = 11
- `pay_cost` = 1
- `laps_to_burn` = 2
- `max_rounds` = 40
- `initial_lead_seat` = 1
- `no_card_value` = 0

## Round

1. **update** (all players): round_number += 1. When current_card = 0 and deck is not empty: draw one card at random from deck (remove it from deck), set current_card to it and set lap_count = 0. The pot is unchanged.
2. **tell** (all players): Announce current_card, pot, every player's tableau and card_points, the length of deck and the length of burned.
3. **ask** (seat lead_seat (offer 1)): When current_card != 0. PAY: chips -= 1 and pot += 1. TAKE: append current_card to tableau; card_points += c, minus (c+1) if c+1 is in the tableau, minus c if c-1 is in the tableau; chips += pot; pot = 0; lead_seat = this seat; current_card = 0.
4. **ask** (seat 1 place clockwise from lead_seat (offer 2)): Same as offer 1. Runs only when current_card != 0.
5. **ask** (seat 2 places clockwise from lead_seat (offer 3)): Same as offer 1. Runs only when current_card != 0.
6. **ask** (seat 3 places clockwise from lead_seat (offer 4)): Same as offer 1. Runs only when current_card != 0 and N >= 4.
7. **update** (all players): End of lap, when current_card != 0: lap_count += 1. If lap_count = 2: append current_card to burned, set current_card = 0, keep pot, and set lead_seat = (lead_seat mod N) + 1. If lap_count = 1, nothing else changes.
8. **tell** (all players): Announce who paid and who took, or that the card was burned. Then sync each player their own chips privately.
9. **check** (all players): End the game if deck is empty and current_card = 0, or if round_number >= 40. Otherwise continue.

## Ending

- ends when: (len(deck) == 0 and current_card == 0) or round_number >= 40
- ranked by: `you.chips - you.card_points` (the highest wins; players level at the top share the win)
- decided by: A player's final score is card_points minus chips, and lower is better, so each player is ranked by chips minus card_points. The highest value (the lowest final score) wins. Players level at the top share the win, which stands in for the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer's count is kept. Three seats is the smallest table where pressing your luck against several rivals is tense. Four keeps each lap short and each refusal costly.
- No talk step: The rules contain no table talk. The strategy is when to pay to drive up the pot and when to take a card that extends a run; adding talk would add a mechanic.
- Tie-break by shared win: Players level at the top share the win, which is the engine's form of the source's draw.
- chips marked observable: The final score depends on chips, so an outside observer must read them, though players see only their own.

## Simplifications

- Lowest score wins, expressed as ranking by chips - card_points (highest wins): The engine ranks highest first, so the score is negated.
- card_points kept incrementally on each take instead of recomputed from runs: The incremental formula in R5 equals the sum of the lowest cards of each run, and it is simple arithmetic.
- Four fixed offer steps, the fourth skipped when N = 3: The step list is flat; each offer is one ask step with an arithmetic condition.
- A round_number counter was added: It enforces the 40-round bound stated in the rules.

## Unsupported (needs engine work)

- none
