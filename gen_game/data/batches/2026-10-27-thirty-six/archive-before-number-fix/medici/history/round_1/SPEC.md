# Medici: Sealed Ledgers

Over 3 days the active player picks a lot of 1 to 3 revealed goods cards, everyone bids for it in a sealed auction, the best ships each day are paid, and at the end good majorities and secret favoured goods are paid. Most florins wins.

Players: 3 to 4, best with 4

## Parameters

- `starting_florins` = 40
- `goods_count` = 4
- `cards_per_good` = 12
- `deck_size` = 48
- `value_0_copies_per_good` = 1
- `value_1_copies_per_good` = 2
- `value_2_copies_per_good` = 2
- `value_3_copies_per_good` = 3
- `value_4_copies_per_good` = 2
- `value_5_copies_per_good` = 2
- `days` = 3
- `rounds_per_day_per_player` = 2
- `total_rounds_per_player` = 6
- `cards_revealed_per_round` = 3
- `min_lot_size` = 1
- `max_lot_size` = 3
- `ship_capacity` = 5
- `min_bid` = 0
- `day_first_prize` = 15
- `day_second_prize` = 7
- `day_tied_first_pool` = 22
- `majority_prize` = 10
- `favoured_per_card` = 3
- `rank_florins_weight` = 1000

## Round

1. **update** (table): If round mod (2N) == 1 (first round of a day), deck is rebuilt as all 48 cards, discard is emptied, and every ship_cards, ship_value and ship_count is reset to empty or 0. Then active_seat = ((round-1) mod N)+1, and winner_seat and price_paid are set to 0.
2. **update** (table): Three cards are drawn at random from deck, in order, into revealed as cards A, B and C, and removed from deck.
3. **tell** (all players): Day {day}, round {round}: the active seat is {active_seat}. The revealed cards A, B, C are {revealed}.
4. **ask** (the active seat): lot_size is set to the choice. lot = the first lot_size cards of revealed, and lot_value is set to the sum of their values. The remaining revealed cards are appended to discard, and revealed is emptied.
5. **tell** (all players): The lot is {lot} ({lot_size} cards, total value {lot_value}).
6. **poll** (all players): Each player's bid is set to their answer. Bids stay hidden from the other players.
7. **update** (all players): For each player: if ship_count + lot_size > 5, then bid is set to 0.
8. **update** (table): If every bid is 0, the lot is appended to discard and winner_seat stays 0. Otherwise winner_seat is the seat with the highest bid, with ties broken by priority = N - ((seat - active_seat + N) mod N). This makes the active seat highest, then the seats after it in order. price_paid is set to the winner's bid.
9. **update** (the winner): If winner_seat > 0: the winner loses price_paid florins, the lot is appended to their ship_cards, ship_value rises by lot_value, ship_count rises by lot_size, and total_cards rises by lot_size. grain_count, cloth_count, spice_count and dye_count each rise by the number of lot cards of that good. lot is then emptied.
10. **tell** (all players): Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means the lot was discarded). Ship card counts of every seat: {ship_count}. Florins are not announced.
11. **update** (all players): If round mod (2N) == 0 (end of a day), day scoring is applied. Let top = max ship_value. If top > 0 and exactly one player has top, that player gains 15. If k>1 players have top, each gains floor(22/k) and no second place is paid. If exactly one player has top, let second = the highest ship_value below top. If second > 0, the m players with second each gain floor(7/m). Then every ship_cards, ship_value and ship_count is reset to empty or 0, discard is emptied, and day rises by 1.
12. **update** (all players): If round == 6N (after day 3 scoring), majorities are paid. For each of grain_count, cloth_count, spice_count and dye_count: let M = the max over players. If M > 0, the j players with M each gain floor(10/j). Then each player gains 3 × their count of their own favoured_good.
13. **tell** (all players): If round == 6N, every player's favoured_good is revealed to everyone.
14. **update** (table): round rises by 1.
15. **check** (table): If round > 6N, the game ends. Otherwise the next round begins.

## Ending

- ends when: round > 6 * N
- ranked by: `you.florins * 1000 + you.total_cards` (the highest wins; players level at the top share the win)
- decided by: The player with the most florins after end-of-game scoring wins. A tie on florins goes to the tied player with more total cards collected over the game. Players still tied share the win, which is the draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer chose 4. 3 is the least where a sealed auction has real rivals and both day prizes are contested. More than 4 is impossible because only 4 favoured goods can be dealt, and majorities would get too thin.
- No talk phase: The source says there is no talk. Bidding is sealed and simultaneous, so it is a poll.
- Tie-break order computed as priority = N - ((seat - active_seat + N) mod N): This turns 'active player first, then seats after the active player' into arithmetic.
- Cards encoded as text like 'Spice-3': The good and the value are both needed for the counts and the ship value.
- Card values given as the number of copies of each value per good, and round counts given per player (2 per day, 6 per game): Parameters must be plain numbers. 1,2,2,3,2,2 copies of values 0 to 5 give the 12-card distribution, and rounds = 2N per day and 6N in total.
- ship_value is public: Lots and winners are announced, so ship contents are public knowledge. Only florins, bids and favoured goods are secret.
- Second place is computed only among ship values above 0 and strictly below the top: The source says a value of 0 earns nothing and a tied first place cancels second place.
- Rank expression florins*1000 + total_cards: total_cards cannot reach 1000, so florins decide first and cards break ties. Any remaining tie shares the win, which is the draw.

## Simplifications

- The deck rebuild and ship emptying at a day boundary are done by conditional updates on round, at the start of a day and at its end: The step list is flat, so day transitions use if-conditions on round.
- Favoured goods are revealed by a public tell at the end of the game: The attribute stays private to its owner, so the reveal is an announcement.

## Unsupported (needs engine work)

- none
