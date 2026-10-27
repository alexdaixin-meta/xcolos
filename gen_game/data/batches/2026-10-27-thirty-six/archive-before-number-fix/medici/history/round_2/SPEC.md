# Medici: Sealed Ledgers (revised)

Players take turns as the active seat and set the size of a lot of 1 to 3 revealed goods cards. Everyone then makes a sealed bid for the lot. Each day pays florins for the most valuable ships, for majorities in each good and for a secret favoured good. Most florins after 6N rounds wins.

Players: 3 to 6, best with 4

## Parameters

- `starting_florins` = 40
- `ship_capacity` = 5
- `goods_count` = 4
- `deck_size` = 48
- `cards_per_good` = 12
- `value_0_cards_per_good` = 1
- `value_1_cards_per_good` = 2
- `value_2_cards_per_good` = 2
- `value_3_cards_per_good` = 3
- `value_4_cards_per_good` = 2
- `value_5_cards_per_good` = 2
- `value_sum_per_good` = 33
- `favour_pool_copies_3_to_4_players` = 1
- `favour_pool_copies_5_to_6_players` = 2
- `rounds_per_day_per_player` = 2
- `days` = 3
- `rounds_per_game_per_player` = 6
- `revealed_cards_per_round` = 3
- `lot_size_min` = 1
- `lot_size_max` = 3
- `bid_min` = 0
- `top_ship_bonus` = 10
- `second_ship_bonus` = 5
- `majority_bonus` = 4
- `majority_min_count` = 1
- `favoured_card_bonus` = 3

## Round

1. **update** (the table): round += 1; active_seat = ((round-1) mod N)+1; winner_seat = 0; high_bid = 0; high_count = 0; every player's bid = 0.
2. **update** (the table): when round mod 2N = 1: deck is set to all 48 cards (Grain, Cloth, Spice and Dye, each with values 0,1,1,2,2,3,3,3,4,4,5,5); discard = []. Cards are drawn at random, so the deck is shuffled.
3. **update** (all players): when round mod 2N = 1: every player's ship_cards = [], ship_value = 0, ship_count = 0, ship_favoured = 0. Florins and cumulative good counts are kept.
4. **update** (the table): revealed = []; draw 3 cards at random from deck, in order, appending each to revealed and removing it from deck. Announce revealed cards 1, 2 and 3 to everyone.
5. **ask** (the active seat (seat active_seat)): lot_size = the answer.
6. **update** (the table): lot = the first lot_size cards of revealed; the remaining revealed cards are appended to discard; revealed = []. Announce the lot.
7. **sync** (all players): Each player is sent their own florins, favoured_good and ship_favoured, plus the public state.
8. **poll** (all players): Each player's bid = the answer; nobody sees any bid until all are in.
9. **update** (all players): For each player: if ship_count + lot_size > 5 then bid = 0.
10. **update** (the table): high_bid = the maximum bid over all players; high_count = the number of players whose bid = high_bid.
11. **update** (the winning player): when high_bid > 0 and high_count = 1: winner_seat = the seat whose bid = high_bid; that player's florins -= bid (paid to the bank, leaving the game). Otherwise winner_seat = 0, the lot is appended to discard, and nobody pays.
12. **update** (the winning player): when winner_seat > 0: the lot cards are appended to the winner's ship_cards; ship_value += sum of the lot values; ship_count += lot_size; ship_favoured += the number of lot cards whose good = favoured_good; grain_count, cloth_count, spice_count and dye_count each += the number of lot cards of that good; lot = [].
13. **tell** (all players): Announce the lot, every player's bid, and winner_seat with price high_bid, or 'no sale'.
14. **update** (the table): when round mod 2N = 0: top_value = the maximum ship_value over all players; second_value = the maximum ship_value among players whose ship_value < top_value, or 0 if there is none.
15. **update** (all players): when round mod 2N = 0: each player with ship_value = top_value and top_value > 0 gains 10 florins; each player with ship_value = second_value and second_value > 0 gains 5 florins.
16. **update** (all players): when round mod 2N = 0: grain_max, cloth_max, spice_max and dye_max = the maximum of that cumulative count over all players; for each good, each player whose count = that max, when the max >= 1, gains 4 florins.
17. **update** (all players): when round mod 2N = 0: each player's florins += 3 * ship_favoured.
18. **tell** (all players): when round mod 2N = 0: announce the day-end ship values and cumulative good counts. Florins and favoured goods are not shown.
19. **check** (the table): If round = 6N the game ends; otherwise the next round begins.

## Ending

- ends when: round = 6 * N
- ranked by: `you.florins` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their florins after round 6N. The most florins wins, and players tied for the most share the win (a draw).

## Choices the source did not make

- 3 to 6 players, suggested 4: The designer suggests 4. Three is the minimum where sealed bids face more than one rival and majorities can be contested. Above 6, the favour pool and the day length would no longer fit the 48-card deck.
- No talk phase: The source states there is no talk phase. The strategy lies in reading public bids, ships and counts to infer others' florins and favoured goods.
- Cards encoded as Good-Value text in lists: This lets drawing, lots, ships and discards be list operations, and lets values and goods be counted arithmetically.
- Card value distribution given as one count per value (value_0_cards_per_good ... value_5_cards_per_good): Parameters must be single numbers, so the list 0,1,1,2,2,3,3,3,4,4,5,5 is written as how many cards of each value each good has.
- ship_favoured kept visible only to its owner (ally): Making it public would reveal the favoured good, which the rules keep secret until the end.
- Bids stored in a public attribute filled by a poll: Nobody sees a bid until all are in, and the rules make all bids public at the announcement.

## Simplifications

- Shuffling the deck is done as drawing cards at random from the deck list: The engine has no shuffle operation; random draws are equivalent and seeded.
- Day-start and day-end steps run every round but carry a 'when round mod 2N' condition: The step list is flat; each conditional step is a single conditioned update, not an alternative block.

## Unsupported (needs engine work)

- none
