# Variation: Medici: Sealed Lots

A 3-6 player sealed-bid auction over 3 days. The active player picks a lot of 1-3 revealed commodity cards, and everyone bids secretly at once, with ties discarding the lot. Ships of 5 slots score daily for value. Cumulative goods counts score daily for majorities. A secret favoured good pays at the end.

Players: 3 to 6, best with 4

## Review of the original

Medici is a 2-6 player auction game over 3 days. Players take turns drawing 1-3 commodity cards as a lot, which is then auctioned once around the table. They fill limited ships to win florins for ship value and for majorities on commodity tracks, and the most florins after day 3 wins.

- **non_degenerate**: good. Simple policies lose. Always passing earns nothing while rivals collect ship and track payouts. Always bidding high bankrupts a player for low-value lots. The drawer's choice of lot size changes what is worth bidding. The fixed clockwise order gives the drawer a last-bid edge, but the active seat rotates.
- **skill_sensitive**: good. Valuing a lot against ship space, track standings and rivals' cash decides games. Card draws add variance, but every player bids on the same lots, so the luck is shared.
- **headroom**: good. Weak players still fill ships and score something. Strong players keep improving through cash management across days, denial bidding and timing their ship fills.
- **reasoning_dependent**: weak. Inference covers rivals' valuations and what remains in the deck. Ships and money are mostly public, so there is no private information about a player's own goals.
- **verifiable**: good. All scoring is arithmetic on ship values, track positions and florins.
- **fits_platform**: weak. The sequential once-around auction, variable-length days, the free fill for the last ship and track boards are costly to build. The previous adaptation fitted the step budget but used 23-25 attributes, over the limit of 20.

## Problems

- The previous variation tracked 23-25 attributes, over the platform limit of 20.
- Revealed cards 1-3 were stored as separate attributes when the deck positions already hold them.
- Four separate good_max attributes (grain_max, cloth_max, spice_max, dye_max) duplicated one reusable value.
- Keeping the undealt favour pool as an attribute after setup wasted an attribute and was counted as an extra hidden element.
- Track maxima and payouts used paired steps per good, which would cost 8 steps if itemised honestly.
- Original (kept fixed): the sequential once-around auction gives a positional edge and is costly to build; this is replaced by a sealed simultaneous bid.
- Original (kept fixed): there is little private information; the secret favoured good is kept so bids reflect hidden valuations.

## Changes

- Drop revealed cards 1-3. The top 3 deck cards are announced in place. The lot is the first lot_size cards of the deck. After resolving, the top 3 cards are removed from the deck. (fixes: Revealed cards 1-3 were stored as separate attributes when the deck positions already hold them.): This saves three attributes with no change to play.
- Replace the four good maxima with one reusable track_max. Each good is scored in a single step: set track_max to the highest count of that good, then pay 6 florins to every player who has that count, provided it is above 0. (fixes: Four separate good_max attributes (grain_max, cloth_max, spice_max, dye_max) duplicated one reusable value.): This saves three attributes and halves the track-scoring steps (4 instead of 8).
- The favour pool exists only during the setup deal. Undealt tiles are simply never revealed and are not tracked. (fixes: Keeping the undealt favour pool as an attribute after setup wasted an attribute and was counted as an extra hidden element.): This removes an attribute and a counted hidden element.
- Store lot_value once at the cut, so the announcement and the load use the same number. Merge the new-deck and ship-reset steps into one day-start step. (fixes: Track maxima and payouts used paired steps per good, which would cost 8 steps if itemised honestly.): This keeps the step count at 19 and the attribute count at 19 while staying explicit.
- Keep the sealed simultaneous bid. A tie for the high bid discards the lot. The active seat rotates so that every seat chooses lot size exactly twice per day. (fixes: Original (kept fixed): the sequential once-around auction gives a positional edge and is costly to build; this is replaced by a sealed simultaneous bid.): This removes the positional edge and is a simple poll.
- Keep the secret favoured good, worth 3 florins per card of that good loaded over the game. (fixes: Original (kept fixed): there is little private information; the secret favoured good is kept so bids reflect hidden valuations.): Each player values goods differently and secretly, so rivals must infer favours from bidding patterns. All goods are symmetric, so no tile is better than another.

## Kept from the original

- Three days of auctions on lots of 1-3 commodity cards, with the lot size chosen by the active player.
- Ships with 5 slots: a full ship cannot buy more that day, and lots cannot be split.
- Ship-value payouts for the top two ships each day.
- Cumulative commodity tracks that pay majorities every day.
- Money spent on bids leaves the game, and the most florins at the end wins.
- The sealed bid, the hidden favoured good and the public florins from the previous variation, which reviewed well.

## The variation's rules

GOODS AND CARDS
There are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.

SETUP
N is the number of players (3 to 6). Each player starts with:
- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.
- ship_value 0 and ship_count 0.
- grain_count, cloth_count, spice_count and dye_count all 0.
- bid 0.
Favour deal: if N is 3 or 4, take one tile each of Grain, Cloth, Spice and Dye (4 tiles). If N is 5 or 6, take two tiles of each good (8 tiles). Deal each player one tile at random, face down. This is their secret favoured_good, known only to them. Undealt tiles are set aside and never revealed.
Set round = 0. The game lasts 6N rounds: 3 days of 2N rounds each. The game-level values are round, active_seat, lot_size, lot_value, deck, high_bid, high_count, top, second and track_max.

EACH ROUND, IN THIS ORDER
1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.
2. NEW DAY (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone. Set every player's ship_value and ship_count to 0. Florins and the four goods counts are kept.
3. REVEAL: announce the top 3 cards of the deck (positions 1, 2, 3) to everyone.
4. LOT SIZE (choice): the active seat chooses 1, 2 or 3.
5. CUT: lot_size = that choice. The lot is deck positions 1 to lot_size. lot_value = the sum of those cards' values. Announce lot_size and lot_value.
6. BID (simultaneous choice): every player whose ship_count + lot_size > 5 is told their ship cannot fit this lot and only a bid of 0 counts. Then all players, at the same moment, choose a whole-number bid from 0 to their florins.
7. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.
8. RESOLVE: high_bid = the largest bid. high_count = the number of players whose bid equals high_bid. Announce every bid.
9. PAY (only if high_bid > 0 and high_count = 1): the sole high bidder loses high_bid florins, which leave the game. Announce their florins.
10. LOAD AND CLEAR: if high_bid > 0 and high_count = 1, the winner adds lot_value to ship_value and lot_size to ship_count, and adds 1 to their count of each lot card's good. Then, in every case, remove the top 3 cards from the deck. If nobody won, the lot is simply discarded.
11. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value. second = the highest ship_value strictly below top, or 0 if there is none.
12. SHIP PAYOUT (same condition): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce florins.
13. GRAIN TRACK (same condition): track_max = the highest grain_count. If track_max > 0, every player with grain_count = track_max gains 6 florins.
14. CLOTH TRACK (same condition): the same, for cloth_count.
15. SPICE TRACK (same condition): the same, for spice_count.
16. DYE TRACK (same condition): the same, for dye_count. Announce florins.
17. FAVOUR (only when round = 6N): each player gains 3 florins times their count of their own favoured_good. All favoured goods are revealed and final florins announced.
18. END: if round = 6N, the game ends.

There is no talk phase.

Objective: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.

Expected effect: Play is the same as the previously tested version. Each lot is a valuation puzzle: ship space, the daily ship race, track majorities, a secret favour, rivals' public cash and their inferred favours all bear on what to bid. Always bidding 0 keeps 40 florins but loses to anyone who wins cheap lots and collects payouts. Always bidding everything either ties and discards the lot or wins once and goes broke, so both simple policies can lose. Favour tiles are symmetric, so the hidden type changes what to buy, not who is ahead. Rotating lot choice removes any seat edge. Talk is left out: the sealed auction is purely competitive, promises cannot bind, and public bids and ships give enough to read.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
