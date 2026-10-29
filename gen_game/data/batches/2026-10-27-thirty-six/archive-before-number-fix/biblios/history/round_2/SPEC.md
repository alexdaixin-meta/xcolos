# Biblios: Scriptorium Duel of Three

Three scribes take turns as the active seat. Each round the active seat secretly keeps one of two drawn cards, and the other two seats bid gold for the other card. Church cards shift colour values, and each colour scores for the single player with the strictly highest total.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 24
- `colour_cards` = 18
- `colour_cards_per_colour` = 6
- `colour_cards_value_1_per_colour` = 2
- `colour_cards_value_2_per_colour` = 2
- `colour_cards_value_3_per_colour` = 1
- `colour_cards_value_4_per_colour` = 1
- `gold_cards` = 4
- `gold_cards_value_2` = 2
- `gold_cards_value_3` = 2
- `church_cards` = 2
- `starting_gold` = 4
- `starting_colour_vp` = 3
- `vp_min` = 1
- `vp_max` = 5
- `rounds` = 12
- `cards_drawn_per_round` = 2
- `turns_active_per_seat` = 4
- `min_winning_bid` = 1
- `church_choices_max_per_round` = 2
- `tiebreak_weight` = 1000

## Round

1. **update** (table): round += 1; active_seat = ((round-1) mod 3)+1; announce the round and the active seat.
2. **update** (table): Two cards are drawn at random from deck into drawn and removed from deck. They are shown only to the active seat.
3. **ask** (the active seat): The chosen card is appended to the active player's hand. If it is red-v, blue-v or green-v, that colour total += v; if it is gold-v, gold += v; if it is church, church_pending = true. The choice is not announced.
4. **update** (table): The other drawn card becomes lot and is announced to everyone; drawn is emptied.
5. **poll** (all players): message is set for each player; then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing said is binding.
6. **poll** (the two non-active seats): bid is set for each bidder and stays secret until both bids are in.
7. **update** (table): If one bid is strictly greater than the other and at least 1, that bidder: gold -= bid; the active player's gold += that bid; lot is appended to bought; a colour lot adds its value to that colour total, a gold lot adds its value to gold, and a church lot sets church_pending = true. If the bids are equal (including 0-0), nobody pays and the lot is discarded. Both bids and the result (the winner and the price, or 'discarded') are announced. Then both bids are reset to 0 and lot = 'none'.
8. **poll** (every player with church_pending true (at most two)): church_choice is set for each chooser.
9. **update** (table): For each colour C: vp_C = min(5, max(1, vp_C + (count of 'C up') - (count of 'C down'))). All choices are announced with who made them. Then church_pending = false and church_choice = 'none' for everyone.
10. **check** (table): If round == 12, go to the end: reveal every hand, colour total and gold. For each colour C, a player whose C total is strictly greater than both other players' C totals gets vp += vp_C; a tied top total scores no one. Then the game ends. Otherwise continue.

## Ending

- ends when: round == 12 after the Church step, with colour scoring applied
- ranked by: `you.vp * 1000 + you.gold` (the highest wins; players level at the top share the win)
- decided by: The player with the highest vp wins. A tie on vp goes to the player with more remaining gold. Players still tied share the win, which is the source's draw.

## Choices the source did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3. The rotation ((r-1) mod 3)+1, the two-bidder auction and 4 active turns each over a 24-card deck only work at exactly 3. At 3, one rival always sits out of each auction, which creates kingmaking tension.
- Talk kept as a simultaneous poll with broadcast: The source requires simultaneous messages. Talk earns its place because players disagree about prices and Church moves, and they can bluff about their hidden keeps.
- rank_by = vp*1000 + gold: This puts vp first and gold as the tie-break. Total gold can never exceed 22, so 1000 separates the two cleanly. Equal values share the win, which is the source's draw.
- gold marked observable: The rules reveal all gold at scoring, and gold decides ties.
- Drawing two random cards stands in for taking the top two of a once-shuffled deck: This is equivalent in distribution, and the deck order is unknown to all anyway.
- The card values are listed as counts per value in parameters: Parameters must be numbers, so the value lists 1,1,2,2,3,4 and 2,2,3,3 are written as how many cards carry each value.

## Simplifications

- Comparing the two bids, and comparing colour totals at the end, use table helper values (for example the top and second bid, and the maximum of the other players' totals): The engine has no direct player-to-player attribute compare; this is the documented workaround.
- Card effects are applied by parsing the card name (colour and value) with conditional operations: There is no card-type lookup; the cards are text in lists.
- The end-of-game reveal and colour scoring are carried out within the final check step: The step list is flat, but the scoring is pure arithmetic, so it can be done with conditional updates when round == 12.

## Unsupported (needs engine work)

- none
