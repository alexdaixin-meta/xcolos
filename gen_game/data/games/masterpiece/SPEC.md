# Masterpiece: Secret Collectors

Four collectors take turns selling paintings in sealed-bid auctions against secret reserves, each guarding private knowledge of painting values and a secret theme style worth a 400 bonus per matching painting.

Players: 4 to 4, best with 4

## Parameters

- `starting_cash` = 1500
- `num_styles` = 4
- `paintings_per_player` = 4
- `value_low` = 0
- `value_mid_low` = 300
- `value_mid_high` = 600
- `value_high` = 1200
- `rounds` = 12
- `sales_per_player` = 3
- `bid_step` = 50
- `reserve_max` = 2000
- `bid_min` = 0
- `reserve_min` = 0
- `unsold_fee` = 50
- `fee_trigger_min_bid` = 50
- `theme_bonus` = 400

## Round

1. **update** (all players): round += 1; seller = ((round-1) mod 4) + 1; sold = false; high_bid = 0; high_bidder = 0; lot = ''; each player's bid = 0 and reserve = 0; tie_priority = 3 for seat ((seller) mod 4)+1, 2 for seat ((seller+1) mod 4)+1, 1 for seat ((seller+2) mod 4)+1, 0 for the seller. Announces the seller.
2. **ask** (the seat to the seller's left: ((seller) mod 4) + 1): when the seller's paintings list is not empty: lot = chosen name; lot_style = its style. The lot and its style are announced to all.
3. **poll** (all players): when the seller's paintings list is not empty: each player's message = their text; afterwards broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk is not binding.
4. **poll** (all players): when the seller's paintings list is not empty: each value is rounded down to a multiple of 50. Each non-seller's bid is set to their number; the seller's reserve is set to theirs. Nobody sees any answer until all are in.
5. **update** (all players): when the seller's paintings list is not empty: high_bid = max over non-sellers of bid; high_bidder = the non-seller with the largest (bid * 10 + tie_priority).
6. **update** (seller and high bidder): when the seller's paintings list is not empty: if high_bid > seller.reserve then sold = true; high_bidder.cash -= high_bid; seller.cash += high_bid; remove lot from seller.paintings; append lot to high_bidder.paintings; append the lot's 'name=value' entry from painting_values to high_bidder.known_values and tell the high bidder privately. Otherwise sold = false, and if high_bid >= 50 then seller.cash -= min(50, seller.cash), and that money leaves the game.
7. **tell** (all players): when the seller's paintings list is not empty: publish every non-seller's bid, whether the lot was sold or kept, the money moved (price or fee) and every player's new cash. The reserve and the painting's value are not published.
8. **update** (all players): when round == 12: reveal painting_values and every theme to all; each player's score = cash + sum of values of the paintings in their paintings list + 400 * (number of paintings in their list whose style equals their theme).
9. **check** (all players): end the game if round == 12, otherwise continue to the next round.

## Ending

- ends when: round == 12
- ranked by: `you.score * 100000 + you.cash` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score (cash + value of owned paintings + 400 per owned painting of their theme), with cash breaking ties. The highest wins; players still level on both score and cash share the win, which stands for the source's draw.

## Choices the source did not make

- Exactly 4 players (min 4, max 4, suggested 4): The designer chose 4. The structure needs it: 4 styles, 4 distinct themes, a 4x4 Latin square of values and 3 sales per seat over 12 rounds. Fewer seats break the value deal, and more have no theme or values to receive.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous unbinding talk. It earns its place because interests conflict: sellers want to talk up lots, and bidders want to bluff their themes and known values.
- Tie-break encoded as bid*10 + tie_priority: Bids are multiples of 50, so adding a priority from 0 to 3 never changes the order of different bids. It ranks the seller's left first, as the rules say.
- Ranking expression score*100000 + cash: Scores stay well under 100000, so cash only breaks ties in score. Players tied on both share the win, which stands for the source's draw.
- Strategy at the table: A thoughtful player infers others' themes from their bids and talk, uses known values to bid on undervalued lots, sets reserves to protect theme paintings, and bluffs in talk. A thoughtless one bids on face value.

## Simplifications

- Bids and reserves are entered as whole numbers and rounded down to a multiple of 50: The engine takes a whole number in a range; rounding enforces the multiple-of-50 rule.
- The skip when the seller has no paintings is done with a 'when' condition on each step: The step list is flat; per-step conditions give the same effect without choosing a block of steps.
- Painting values are stored as 'name=value' text entries in lists: The engine has lists, not maps; each player's known_values plays the role of 'values known to past owners'.
- Bids and the reserve are gathered in one simultaneous poll with different ranges per seat: The source makes them simultaneous; one poll keeps every answer hidden until all are in.

## Unsupported (needs engine work)

- none
