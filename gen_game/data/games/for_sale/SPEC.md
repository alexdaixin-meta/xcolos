# For Sale: Sealed Bids

Three players spend 8 sealed-bid rounds buying property cards with private coins, then 8 simultaneous rounds selling those properties for cheques; the most cheques plus leftover coins wins.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `starting_coins` = 18
- `property_min` = 1
- `property_max` = 30
- `property_deck_size` = 30
- `properties_used` = 24
- `properties_unused` = 6
- `cheque_min_value` = 0
- `cheque_max_value` = 15
- `cheque_missing_value` = 1
- `cheque_distinct_values` = 15
- `cheque_copies_each` = 2
- `cheque_deck_size` = 30
- `cheques_used` = 24
- `total_rounds` = 16
- `buying_rounds` = 8
- `first_selling_round` = 9
- `cards_revealed_per_round` = 3
- `first_place_pay_fraction` = 1
- `second_third_pay_divisor` = 2
- `properties_per_player_after_buying` = 8
- `initial_cheque_total` = 0
- `tie_break_bid_multiplier` = 10
- `rank_coin_tiebreak_multiplier` = 100

## Round

1. **update** (table): Set priority_first = ((round-1) mod 3)+1. When round <= 8: clear revealed_properties, then draw 3 cards at random from property_deck, removing each from property_deck and appending it to revealed_properties. Announce the 3 cards as LOW = min, MIDDLE = the remaining card and HIGH = max, and announce priority_first.
2. **sync** (all players): When round <= 8: each player is sent their own coins, all hands, revealed_properties and priority_first.
3. **poll** (all players): When round <= 8: set bid for each player. Nobody sees any bid.
4. **update** (all players): When round <= 8: for each player, bid_key = bid*10 + (3 - ((seat - priority_first + 3) mod 3)). Then bid_rank = 1 + the number of other players whose bid_key is larger than this player's.
5. **update** (all players): When round <= 8: the player with bid_rank 1 appends max(revealed_properties) to hand and pays coins -= bid. The player with bid_rank 2 appends the middle card to hand and pays coins -= floor(bid/2). The player with bid_rank 3 appends min(revealed_properties) to hand and pays coins -= floor(bid/2). Payments go to the bank. Publicly announce which seat took LOW, MIDDLE and HIGH, without bids or coin totals.
6. **update** (table): When round >= 9: clear revealed_cheques, then draw 3 cheques at random from cheque_deck, removing each from cheque_deck and appending it to revealed_cheques. Announce the 3 cheques.
7. **sync** (all players): When round >= 9: each player is sent their own cheques and coins, all hands, and revealed_cheques.
8. **poll** (all players): When round >= 9: set played for each player. The choices are revealed only after all are in.
9. **update** (all players): When round >= 9: the player with the highest played adds max(revealed_cheques) to cheques. The player with the middle played adds the middle cheque. The player with the lowest played adds min(revealed_cheques). Each player removes played from hand, which discards the card. Publicly announce who played which property and who took which cheque; cheque totals stay private.
10. **update** (table): round += 1.
11. **update** (all players): When round > 16: final_money = cheques + coins and final_coins = coins, both revealed publicly.
12. **check** (table): End the game if round > 16; otherwise continue with the next round.

## Ending

- ends when: round > 16
- ranked by: `you.final_money * 100 + you.final_coins` (the highest wins; players level at the top share the win)
- decided by: The most final money (cheque total plus remaining coins) wins. A tie goes to the tied player with more remaining coins; coins are at most 18, so the x100 weighting keeps money first. Players still level share the win, which is the draw.

## Choices the source did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed 3. The 3-card reveals, the 3-way priority rotation and the LOW/MIDDLE/HIGH payment tiers are all built for exactly 3 seats.
- No talk step before bids or plays: The source has no communication phase, and talk would add a mechanic. Strategy comes from reading public hands and the inferable coin spending: bid low when the top card is weak, keep coins for the tie-break, and time high properties against strong cheques.
- Tie-break computed as bid*10 + priority weight (3, 2, 1): This puts the rotating priority rule into one arithmetic key. Bids are at most 18, so the weight never outranks a higher bid.
- bid_key is visible to its owner only (ally): It is engine scratch derived from the player's own private bid, and a player attribute cannot be fully hidden.
- Cheque values described by numeric parameters (min 0, max 15, value 1 missing, 2 copies each): Parameters must be numbers, so the value list is given as its bounds and the one skipped value.
- rank_by = final_money*100 + final_coins: This encodes the remaining-coins tie-break in one expression. Coins never exceed 18, so the x100 weighting keeps final money first.
- Separate public final_coins attribute: Remaining coins decide ties and are revealed at the end, so they are made public then. Coins stay private during play.

## Simplifications

- Shuffling and taking the top of a deck are done as random draws from the deck list: Drawing at random is equivalent to drawing from the top of a shuffled deck. The 6 never-drawn cards and cheques simply remain in the hidden lists.
- Buying and selling steps share one flat round list, gated by 'when round <= 8' and 'when round >= 9': The engine has one repeating step list. Per-step arithmetic conditions select the phase without needing conditional blocks.

## Unsupported (needs engine work)

- none
