# Lost Cities: Three Expeditions

Two explorers build rising number runs in three colours, betting with wager cards and fighting over a shared discard row, while a 21-card deck runs out.

Players: 2 to 2, best with 2

## Parameters

- `colours` = 3
- `total_cards` = 33
- `lowest_number` = 2
- `highest_number` = 10
- `wagers_per_colour` = 2
- `hand_size` = 6
- `deck_after_deal` = 21
- `expedition_cost` = 15
- `wager_multiplier_base` = 1
- `bonus_card_count` = 5
- `bonus_points` = 10
- `max_rounds` = 20
- `max_discard_tops_per_colour` = 1

## Round

1. **sync** (all players): Each player sees their own hand and all public state: the expedition numbers, discard_tops and deck_size.
2. **ask** (seat 1): On a legal PLAY of X in colour c: remove X from hand and add 1 to cnt_c. For a number, add X to sum_c and set top_c to X. For a wager, add 1 to wag_c. On DISCARD X: remove X from hand, remove any card of X's colour from discard_tops (it leaves the game), append X to discard_tops and set last_discard to X. An illegal PLAY, or a card not in hand, is treated as DISCARD of the first card in hand.
3. **ask** (seat 1): DECK: draw a random card from deck into hand and subtract 1 from deck_size. A named card: move it from discard_tops to hand. An invalid answer, or naming last_discard, means DECK. If deck is empty and no eligible discard exists, nothing is drawn. Then set last_discard to 'none'.
4. **update** (seat 1): Announce the card played or discarded, what was drawn (deck or the named discard), and the new deck_size and discard_tops.
5. **sync** (seat 2): Seat 2 sees their updated state.
6. **ask** (seat 2): Same as seat 1's play or discard step.
7. **ask** (seat 2): Same as seat 1's draw step. Then set last_discard to 'none'.
8. **update** (all players): For each player and each colour c: if cnt_c = 0 the colour scores 0, otherwise it scores (sum_c - 15) * (1 + wag_c), plus 10 if cnt_c >= 5. Set score to the total of the three colours. Add 1 to round. Announce both scores.
9. **check** (all players): End the game if deck_size = 0 or round >= 20. Otherwise continue.

## Ending

- ends when: deck_size == 0 or round >= 20 (checked at the end of a round, after seat 2's turn)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: The player with the higher score wins. If the scores are equal, both share the result, which is a draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed 2 players. The game is a duel over a shared discard row: what you discard feeds your one opponent.
- No talk step: The rules have no communication, and the game is a pure two-player contest of hand management and denial.
- Only legal plays are offered: A seat is never offered what it may not do. The fallback rule (an illegal play becomes a discard of the first card in hand) is kept for malformed answers.
- Public deck_size counter: The rules say both players see how many cards remain, while the deck itself stays hidden.
- Public round counter: Needed to apply the 20-round limit arithmetically.
- Strategy at the table: A thoughtful player commits only to colours they can reach 15+ in, times wagers before the numbers, avoids discarding cards the opponent needs, and watches the deck count to judge how much longer the game runs.

## Simplifications

- Taking the top card of the deck is a random pick from the deck list: The deck is shuffled, so a random draw is equivalent and keeps the match seed-reproducible.
- Each seat's turn is written as explicit seat 1 and seat 2 steps: The step list is flat. This keeps both players' turns equal within a round.

## Unsupported (needs engine work)

- none
