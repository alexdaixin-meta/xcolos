# Medici: Sealed Lots

Players bid sealed florins for lots of goods cards to fill their ships. Ships pay out at the end of each of 3 days, goods tracks pay bonuses, and a secret favoured good pays at the end. The most florins wins.

Players: 3 to 6, best with 4

## Parameters

- `starting_florins` = 40
- `deck_size` = 48
- `goods` = 4
- `cards_per_good` = 12
- `cards_of_value_0_per_good` = 1
- `cards_of_value_1_per_good` = 2
- `cards_of_value_2_per_good` = 2
- `cards_of_value_3_per_good` = 3
- `cards_of_value_4_per_good` = 2
- `cards_of_value_5_per_good` = 2
- `value_per_good_total` = 33
- `reveal_count` = 3
- `lot_size_min` = 1
- `lot_size_max` = 3
- `cards_cleared_per_round` = 3
- `ship_capacity` = 5
- `days` = 3
- `rounds_per_day_per_player` = 2
- `total_rounds_per_player` = 6
- `ship_first_payout` = 20
- `ship_second_payout` = 10
- `track_bonus` = 6
- `favour_multiplier` = 3
- `favour_tiles_per_good_small` = 1
- `favour_tiles_per_good_large` = 2
- `small_table_max` = 4
- `bid_min` = 0

## Round

1. **update** (all players): round = round + 1; active_seat = ((round - 1) mod N) + 1.
2. **update** (all players): When round mod 2N = 1: deck is rebuilt as the full 48-card list (for each of Grain, Cloth, Spice and Dye, the values 0,1,1,2,2,3,3,3,4,4,5,5) and placed in random order by drawing every card at random. Any old cards are discarded. Every player's ship_value = 0 and ship_count = 0. Florins and goods counts are kept.
3. **update** (all players): revealed = deck positions 1, 2 and 3. These are announced to everyone.
4. **ask** (the player at active_seat): Records the lot size choice.
5. **update** (all players): lot_size = the choice; lot_value = the sum of the values of deck positions 1..lot_size. lot_size and lot_value are announced.
6. **tell** (every player with ship_count + lot_size > 5): Tells each such player that their ship cannot fit this lot and only a bid of 0 counts.
7. **poll** (all players): bid = the answer. All players answer simultaneously, and no one sees a bid until all are in.
8. **update** (all players): For each player: if bid > florins or ship_count + lot_size > 5, then bid = 0.
9. **update** (all players): high_bid = the maximum bid; high_count = the number of players with bid = high_bid. Every bid is announced.
10. **update** (the sole high bidder): When high_bid > 0 and high_count = 1: the player with bid = high_bid has florins = florins - high_bid (these florins leave the game), and their florins are announced.
11. **update** (all players): When high_bid > 0 and high_count = 1: the winner's ship_value += lot_value and ship_count += lot_size, and the winner gains +1 grain_count, cloth_count, spice_count or dye_count for each lot card of that good. In every case, the top 3 cards are removed from deck (an unwon lot is simply discarded).
12. **update** (all players): When round mod 2N = 0: top = the maximum ship_value; second = the maximum ship_value strictly below top, or 0 if there is none.
13. **update** (all players): When round mod 2N = 0: if top > 0, every player with ship_value = top gains 20 florins; if second > 0, every player with ship_value = second gains 10 florins. Florins are announced.
14. **update** (all players): When round mod 2N = 0: track_max = the maximum grain_count; if track_max > 0, every player with grain_count = track_max gains 6 florins.
15. **update** (all players): When round mod 2N = 0: track_max = the maximum cloth_count; if track_max > 0, every player with cloth_count = track_max gains 6 florins.
16. **update** (all players): When round mod 2N = 0: track_max = the maximum spice_count; if track_max > 0, every player with spice_count = track_max gains 6 florins.
17. **update** (all players): When round mod 2N = 0: track_max = the maximum dye_count; if track_max > 0, every player with dye_count = track_max gains 6 florins. Florins are announced.
18. **update** (all players): When round = 6N: each player gains florins += 3 × (their count of their favoured_good). Every favoured_good is revealed to all, and final florins are announced.
19. **check** (all players): The game ends if round = 6N; otherwise play continues.

## Ending

- ends when: round = 6 * N
- ranked by: `you.florins` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their florins after round 6N. The most florins wins. Players tied for the most florins share the result, which stands for the source's draw.

## Choices the source did not make

- 3 to 6 players, suggested 4: The designer's suggested size of 4 is kept. The minimum is 3 because the second-place ship payout and sealed-bid ties need at least two rivals. The maximum is 6 because the 48-card deck supplies the 6N = 36 cards cleared per day at N=6, and a larger table would leave each player too few auctions to matter.
- No talk phase: The rules state there is no talk phase.
- Cards are coded as good:value text in the deck list: This lets the engine sum lot values and count goods per lot card arithmetically.
- Ship values, ship counts and goods counts are public: Every lot's cards, value and winning bid are announced, so all players can already work these out.
- Card value distribution given as counts per value in parameters: Parameters must be single numbers, so the per-good list 0,1,1,2,2,3,3,3,4,4,5,5 is written as how many cards of each value each good has.
- Strategy check: Players must value lots against their ship capacity, contest the ship ranks and goods tracks, hide their favoured good while chasing it, and avoid tied high bids that void a lot.

## Simplifications

- Shuffling the deck is done by drawing all 48 cards at random into an ordered list: The engine's randomness is random draws, and the result is an equivalent shuffle.
- A tie for the most florins is a shared win rather than a declared draw: The engine has no separate draw; players level at the top share the win.

## Unsupported (needs engine work)

- none
