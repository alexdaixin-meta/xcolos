# Libertalia: Shared Hand

Three pirates play identical 7-card hands over 2 campaigns of 5 days, revealing one character a day at the same time to share out booty tokens and trigger abilities, while avoiding clashes on the same rank.

Players: 3 to 3, best with 3

## Parameters

- `players` = 3
- `campaigns` = 2
- `days_per_campaign` = 5
- `total_rounds` = 10
- `starting_score` = 0
- `hand_size` = 7
- `lowest_rank` = 1
- `highest_rank` = 7
- `cards_discarded_per_campaign` = 2
- `cabin_boy_rank` = 1
- `cabin_boy_gain` = 3
- `gunner_rank` = 2
- `gunner_penalty` = 3
- `gunner_target_min_rank` = 6
- `quartermaster_rank` = 3
- `quartermaster_bonus_per_higher` = 1
- `bosun_rank` = 4
- `bosun_floor` = 0
- `merchant_rank` = 5
- `merchant_bonus` = 2
- `merchant_threshold` = 3
- `captain_rank` = 6
- `admiral_rank` = 7
- `admiral_wage` = 2
- `row_count` = 6
- `tokens_per_row` = 3
- `row_A_1` = 5
- `row_A_2` = 3
- `row_A_3` = 1
- `row_B_1` = 5
- `row_B_2` = 1
- `row_B_3` = -3
- `row_C_1` = 3
- `row_C_2` = 3
- `row_C_3` = 1
- `row_D_1` = 5
- `row_D_2` = 3
- `row_D_3` = -3
- `row_E_1` = 3
- `row_E_2` = 1
- `row_E_3` = -3
- `row_F_1` = 5
- `row_F_2` = 5
- `row_F_3` = -3

## Round

1. **update** (all players): day += 1; if day == 6, every player's hand is set to [1,2,3,4,5,6,7], which discards the 2 leftover cards and deals campaign 2; every player's card = 0, clashed = false, token = 0, ability = 0
2. **update** (all players): booty_row = one entry of booty_rows picked at random, each equally likely, without removing it (with replacement); announce booty_row to all
3. **poll** (all players): message = the text; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}
4. **poll** (all players): card = the chosen rank; no answer is seen until all are in
5. **update** (all players): remove card from hand; reveal every player's card to all
6. **update** (all players): clashed = (number of other players whose card == you.card) >= 1
7. **update** (all players): if not clashed and card >= 2: pos = 1 + number of other players with not clashed and card >= 2 and card > you.card; token = booty_row[pos]; if card == 4, token = max(token, 0); otherwise token = 0
8. **update** (all players): ability = 0; if not clashed and card == 1: ability += 3; if not clashed and card == 3: ability += 1 * (number of other non-clashed players with card > 3); if not clashed and card == 5 and token >= 3: ability += 2; if not clashed and card == 7: ability -= 2; if not clashed and card >= 6 and some other non-clashed player has card == 2: ability -= 3
9. **update** (all players): score += token + ability; announce each player's card, clashed, token, ability and score
10. **check** (all players): end the game if day == 10, otherwise continue

## Ending

- ends when: day == 10
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Highest doubloon total after 10 days wins; players tied at the top share the win (a draw).

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixed 3. With 3 seats, clashes are a real risk and the three tokens are enough for everyone. A different count would change the token count and how clashes play out.
- Keep the simultaneous talk poll before the card poll: The rules require it. Players disagree, since each wants the others to avoid their rank, so a bluff or proposal is worth weighing, and messages are not binding.
- Hands are public attributes: All hands start identical and played cards are revealed, so the remaining hand can be worked out by everyone. Only the day's choice is secret, and the simultaneous poll keeps it so.
- Gunner penalty is a flat 3: Only one non-clashed Gunner can exist on a day, because two Gunners clash each other.

## Simplifications

- Booty rows are stored as a list of token lists, and the row is picked at random without removal: Drawing with replacement needs no deck depletion.
- Leftover tokens and discarded cards are not tracked: The rules never refer to them again.

## Unsupported (needs engine work)

- none
