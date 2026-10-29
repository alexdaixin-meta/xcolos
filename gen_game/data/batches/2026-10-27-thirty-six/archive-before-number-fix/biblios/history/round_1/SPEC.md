# Biblios: Scriptorium

Over 12 rounds, the active player draws 2 cards, secretly keeps one and auctions the other in a sealed bid. Church cards shift colour values, and the most cards in a colour wins that colour's VP.

Players: 3 to 4, best with 3

## Parameters

- `deck_size` = 24
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
- `vp_start` = 3
- `vp_min` = 1
- `vp_max` = 5
- `rounds` = 12
- `cards_drawn_per_round` = 2
- `cards_kept_per_round` = 1
- `min_bid` = 0
- `min_winning_bid` = 1
- `church_change` = 1
- `rank_vp_multiplier` = 1000

## Round

1. **update** (table): round += 1; active_seat = ((round-1) mod player_count) + 1; reset every player's bid = 0, church_pending = false, church_choice = ''; winner_seat = 0, sale_price = 0, high_bid = 0, high_count = 0, lot = ''
2. **update** (table): Draw: move 2 random cards from deck into drawn (remove from deck, append to drawn)
3. **ask** (the active seat (active_seat)): Kept colour card <c>-<v>: append it to the active player's hand and add v to kept_<c>. Kept gold-<v>: add v to the active player's gold. Kept church: append it to hand and set church_pending = true. The other card in drawn becomes lot, then drawn is cleared.
4. **tell** (all players): Offer: announce 'The lot is {lot}.'
5. **poll** (all players): Talk: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}; talk is not binding
6. **poll** (every seat except active_seat): Set each bidder's bid; no one sees a bid until all are in
7. **update** (table): high_bid = max bid among non-active seats; high_count = number of non-active seats with bid == high_bid. If high_count == 1 and high_bid >= 1: winner_seat = that seat, sale_price = high_bid, winner's gold -= high_bid, active player's gold += high_bid. Otherwise: winner_seat = 0, sale_price = 0, append lot to discard.
8. **update** (the winner (when winner_seat > 0)): Take: append lot to the winner's bought (public). Colour lot <c>-<v>: bought_<c> += v. Gold lot gold-<v>: winner's gold += v. Church lot: winner's church_pending = true.
9. **tell** (all players): Announce: 'Seat {winner_seat} bought {lot} for {sale_price} Gold.', or 'The lot {lot} was discarded.' when winner_seat == 0
10. **poll** (every player with church_pending == true (skipped if none)): Set church_choice and reveal that the player played a Church card. Then apply every choice one after another: vp_<c> = min(5, max(1, vp_<c> ± 1)), so a colour may receive two changes.
11. **tell** (all players): Announce each church_choice made this round and the VP values: 'Red {vp_red}, Blue {vp_blue}, Green {vp_green}.'
12. **update** (table (end scoring, only when round == 12)): For each colour c: each player's total_c = kept_c + bought_c; m_c = max total_c over players. If m_c > 0, each player with total_c == m_c adds vp_c / (number of players with total_c == m_c) to vp. Gold adds no VP. Reveal all hands.
13. **check** (table): If round == 12, end the game; otherwise continue

## Ending

- ends when: round == 12 after the step 9 Church resolution and end scoring
- ranked by: `you.vp * 1000 + you.gold` (the highest wins; players level at the top share the win)
- decided by: Most VP wins. A tie on VP is broken by the most leftover Gold. Players still tied on both share the win, which is a draw.

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer suggests 3, so it is kept. The minimum is 3 because with 2 players the auction has a single bidder and no rivalry. The maximum is 4 because that is the source's limit; the 24-card deck and 12 rounds are fixed, so more seats would leave each player too few turns as the active seller.
- Keep the simultaneous talk step as a poll broadcast to all: The source requires it, and it earns its place: players disagree about who should take each colour, and the seller can bluff about the hidden kept card to raise the price.
- Strategy at the table: A thoughtful player reads the others' bought cards and their bluffs to infer majorities. They price a lot by the gold it hands the seller, and use Church cards to raise colours they lead and lower colours they trail.
- Card encoding as text 'colour-value', 'gold-value', 'church': It gives the keep options and lots a readable, parseable form.
- Card distribution expressed as numeric counts per value in parameters: Parameters must be numbers, so the value lists are given as how many cards of each value exist.
- rank_by = vp*1000 + gold: It folds the Gold tie-break into one expression. Fractional VP differences are at least 1/12, and 1000/12 is about 83, which exceeds the maximum possible gold (26 with 4 players).
- Church changes applied one after another, with clamping at each step: The source says to apply all changes, limited to 1-5, but does not say whether clamping happens per change or at the end. Applying them in sequence is the natural reading.
- Separate kept (private) and bought (public) sums per colour: Kept cards are hidden and bought cards are face-up, so their visibility differs. Scoring adds the two.
- End scoring runs as an update conditioned on round == 12, placed before the end check: The check ends the game, so scoring must happen before it.

## Simplifications

- Shuffling is replaced by drawing random cards from the deck list: This is equivalent to a shuffled deck in the engine's draw model.
- The drawn cards are shown only to the active player as the options of the keep question, not through an 'active player only' visibility: The engine has no per-round visibility for the active player; private question options give the same effect.
- The Gold tie-break and the draw are folded into a single ranking where tied players share the win: The engine ranks by one arithmetic expression and has no separate draw.

## Unsupported (needs engine work)

- none
