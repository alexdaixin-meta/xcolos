# Biblios: Scriptorium Lots (revised)

Three scribes take turns splitting three cards among keep, give and auction. They bid gold for the auction cards and use Church cards to push colour dice, then score each colour they alone lead at its final die value.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `deck_size` = 36
- `colours` = 5
- `colour_cards_per_colour` = 6
- `colour_value_1_copies` = 2
- `colour_value_2_copies` = 2
- `colour_value_3_copies` = 1
- `colour_value_4_copies` = 1
- `colour_cards_total` = 30
- `gold_card_small` = 2
- `gold_card_mid` = 3
- `gold_card_large` = 4
- `gold_cards` = 3
- `church_cards` = 3
- `starting_gold` = 8
- `starting_colour_total` = 0
- `die_start` = 3
- `die_min` = 1
- `die_max` = 6
- `die_step` = 1
- `rounds` = 12
- `cards_per_round` = 3
- `split_options` = 6
- `church_options` = 10
- `max_church_actions_per_round` = 1
- `min_bid` = 0
- `winning_bid_must_exceed` = 0
- `active_seat_round_1` = 1
- `active_seat_round_2` = 2
- `active_seat_round_3` = 3
- `active_seat_round_4` = 2
- `active_seat_round_5` = 3
- `active_seat_round_6` = 1
- `active_seat_round_7` = 3
- `active_seat_round_8` = 1
- `active_seat_round_9` = 2
- `active_seat_round_10` = 1
- `active_seat_round_11` = 2
- `active_seat_round_12` = 3
- `rank_gold_weight` = 1
- `rank_vp_weight` = 1000

## Round

1. **update** (all players): round += 1; active_seat = active_order[round-1]; announce 'Round {round}: seat {active_seat} is active.'
2. **update** (seat active_seat): Draw 3 cards at random from deck into dealt, removing them from deck. Reveal dealt privately to the active seat only.
3. **ask** (seat active_seat): records which dealt card is keep_card, auction_card and give_card
4. **update** (seat active_seat): keep_card is appended to the active player's kept list and takes effect for them. A colour card adds its value to that colour total, a Gold card adds to gold, and a Church card sets church = true (no extra effect if already true). Nothing is announced except the public change in gold.
5. **update** (next seat of active_seat (1->2, 2->3, 3->1)): give_card is revealed to everyone, takes effect for the next seat (colour total, gold or church = true), and is appended to that player's public_record.
6. **update** (all players): auction_card = the AUCTION card; announce it to everyone. dealt is emptied.
7. **poll** (all players): broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in; non-binding
8. **poll** (all players): records each player's secret bid
9. **update** (all players): All bids are revealed and top = max bid. If top > 0 and exactly one player bid top, that player's gold -= top (the gold leaves the game), auction_card takes effect for them (colour total, gold or church = true) and is appended to their public_record. Otherwise auction_card is appended to discard and nobody pays.
10. **poll** (every player whose church is true (step skipped if none)): Choices are applied in seat order 1, 2, 3: the named die is changed by +1 or -1 and clamped to 1..6.
11. **update** (all players): church = false for every player.
12. **tell** (all players): Announce the five die values, each player's gold and each player's public_record. Kept cards and true colour totals are not shown.
13. **update** (all players): when round == 12: for each colour, a player whose total in that colour is strictly greater than both other players' totals gets vp += that colour's die value; a tied top scores nobody.
14. **check** (all players): end the game if round == 12, otherwise continue

## Ending

- ends when: round == 12
- ranked by: `you.vp * 1000 + you.gold` (the highest wins; players level at the top share the win)
- decided by: Most VP wins. A tie on VP goes to the tied player with the most gold. Players still level share the win (a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3, and the 12-round active order and next-seat cycle are written for seats 1-3, so the minimum and maximum are both 3. At 3 an auction has two rivals, and a colour majority can be contested or shared.
- Strategy at the table: A thoughtful player keeps cards that build hidden majorities and gives away cards that cannot tip a colour. They bid according to what an auction card is worth in the colours they can win, and use Church to raise colours they lead and lower colours rivals lead. They also read public records and gold changes to infer the others' hidden kept cards.
- Talk kept, as a simultaneous poll broadcast to all: The source says all three write at the same time and messages are shown together. Players disagree about who should win each auction, so talk (bluffing about majorities, proposing who drops out of bidding) has strategic weight.
- Church flag visibility is ally (owner only): A kept Church card is face-down, so a public flag would reveal it. The rules publish only dice, gold and records.
- Rank expression vp*1000 + gold: Gold can never exceed 17 (8 at the start plus 9 from Gold cards), so the factor 1000 makes VP decide first and gold break ties. A remaining tie is a shared win, which matches the source's draw.
- Card representation as text like 'Red 3', 'Gold 4', 'Church': The source does not name a format; text labels let the effect be read off the card.
- Unwon auction cards go to a public discard list: The source says 'discarded' without naming a pile; a list keeps the card stated somewhere.
- List-valued numbers (card values, active order) split into separate numeric parameters: Parameters must each be a single number, so each count, value and per-round active seat is listed on its own.

## Simplifications

- Colour majority scoring uses comparisons kept beside the scores (for each colour, the top total and how many players hold it): The engine has no direct player-to-player attribute operand, so the workaround compares each player's total with maxima kept on the table.
- Dealt cards are held in a hidden table list and revealed privately to the active seat: A table attribute cannot be visible to one changing seat, so a private reveal provides 'shown only to the active player'.
- Final scoring is a round step gated by round == 12 before the ending check: The step list is flat; a single conditional update computes VP once, at the end.

## Unsupported (needs engine work)

- none
