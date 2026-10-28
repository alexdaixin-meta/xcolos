# Cat Lady: Secret Favourites (Balanced)

A card-drafting game for 3 to 4 players: each round players take turns picking a 2-card lot from a public market, collecting food, cats, strays, toys and catnip, and score at the end with a secret Favourite bonus.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 96
- `food1_cards` = 18
- `food1_value` = 1
- `food2_cards` = 10
- `food2_value` = 2
- `cat_cards` = 20
- `stray_cards` = 8
- `toy_cards_per_colour` = 8
- `toy_cards_total` = 24
- `catnip_cards` = 16
- `cards_per_lot` = 2
- `lots_with_3_players` = 4
- `lots_with_4_players` = 5
- `rounds_with_3_players` = 12
- `rounds_with_4_players` = 8
- `picks_per_position_3_players` = 4
- `picks_per_position_4_players` = 2
- `unused_deck_cards_4_players` = 16
- `food_per_cat` = 2
- `fed_cat_points` = 5
- `unfed_cat_points` = -1
- `stray_points` = 3
- `toy_points` = 1
- `toy_set_points` = 4
- `catnip_count_cap` = 6
- `catnip_max_points` = 21
- `food_penalty` = 2
- `food_penalty_min_leftover` = 1
- `fav_cats_per_fed_cat` = 2
- `fav_cats_max` = 10
- `fav_toys_per_toy` = 1
- `fav_catnip_per_card` = 2
- `fav_catnip_max` = 12
- `fav_strays_per_stray` = 3
- `rank_score_multiplier` = 100

## Round

1. **update** (all players): round += 1; first_picker = ((round - 1) mod N) + 1; lots_open = [A, B, C, D] with 3 players or [A, B, C, D, E] with 4 players.
2. **update** (all players): For each letter in lots_open, draw 2 cards at random from deck into lot_<letter> (append to the lot, remove from deck).
3. **tell** (all players): Announce round, first_picker and the contents of every lot in lots_open.
4. **ask** (each player in turn, starting with seat first_picker and continuing in seat order (wrapping from seat N to seat 1)): The chosen lot's cards are appended to the player's cards. For each card: food1 adds 1 to food, food2 adds 2 to food, cat adds 1 to cats, stray adds 1 to strays, toy_red/toy_blue/toy_green add 1 to toys_red/toys_blue/toys_green, catnip adds 1 to catnip. The lot list is emptied and its letter is removed from lots_open. The pick is announced to all.
5. **update** (all players): The cards of the one lot left in lots_open are appended to discard, that lot is emptied, and lots_open is emptied.
6. **update** (all players): When round == num_rounds, for each player: fed_cats = min(cats, floor(food / 2)); leftover_food = food - 2 * fed_cats; score = 5 * fed_cats - 1 * (cats - fed_cats) + 3 * strays + 1 * (toys_red + toys_blue + toys_green) + 4 * min(toys_red, toys_blue, toys_green) + m * (m + 1) / 2 where m = min(catnip, 6).
7. **update** (all players): When round == num_rounds: max_leftover = the largest leftover_food over all players.
8. **update** (all players): When round == num_rounds, for each player: if leftover_food == max_leftover and max_leftover >= 1, score -= 2. Favourite bonus: if favourite == cats, score += min(2 * fed_cats, 10); if toys, score += toys_red + toys_blue + toys_green; if catnip, score += min(2 * catnip, 12); if strays, score += 3 * strays. favourite_revealed = favourite.
9. **tell** (all players): When round == num_rounds, announce every player's favourite_revealed, fed_cats and score.
10. **check** (all players): End the game if round >= num_rounds; otherwise continue to the next round.

## Ending

- ends when: round >= num_rounds
- ranked by: `you.score * 100 + you.fed_cats` (the highest wins; players level at the top share the win)
- decided by: The highest final score wins. Among players tied on score, the one with the most fed cats wins. Players still tied on both share the win, which is a draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer chose 4. The minimum is 3 because with 2 players there is little contest over lots and almost nothing to hide a Favourite among. The maximum is 4 because the deck and the Favourite set (four Favourites) are built for at most 4.
- No talk step before picks: The source has no negotiation. Picks are public, and the interest lies in reading others' Favourites from their picks and hate-drafting, so talk would only add words.
- Strategy at the table: A thoughtful player balances food against cats to avoid unfed cats and the food penalty, chases toy sets and catnip, and infers rivals' secret Favourites from what they take so as to deny them key lots.
- Card codes food1, food2, cat, stray, toy_red, toy_blue, toy_green, catnip: The deck needs concrete list entries for drawing and counting.
- rank_by = score * 100 + fed_cats: fed_cats is at most 20 (below 100), so this ranks by score first and fed cats second, and remaining ties share the win as the source's draw.

## Simplifications

- Dealing the market from the top of the deck is done as random draws from the deck list: The deck is shuffled once, so drawing at random is equivalent.
- The Favourite is revealed by copying it to a public attribute favourite_revealed at final scoring: Visibility of an attribute is fixed, so revealing is done by copying the value.
- The food penalty uses a table attribute max_leftover: The engine has no direct player-to-player comparison; the maximum is kept on the table and each player is compared to it.
- Final scoring runs as conditional updates in the last round: The step list is flat, so the scoring steps carry a 'when round == num_rounds' condition.

## Unsupported (needs engine work)

- none
