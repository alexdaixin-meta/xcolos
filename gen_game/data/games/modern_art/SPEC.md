# Modern Art: Four Seasons

Four dealers auction paintings by four artists over four seasons with sealed bids. Each season the artists are ranked and pay out on paintings held. The richest player who bought at least 3 paintings wins.

Players: 4 to 4, best with 4

## Parameters

- `deck_size` = 24
- `cards_per_artist` = 6
- `hand_size` = 5
- `set_aside_cards` = 4
- `starting_money` = 100
- `seasons` = 4
- `auctions_per_season` = 4
- `total_auctions` = 16
- `value_first` = 30
- `value_second` = 20
- `value_third` = 10
- `value_fourth` = 0
- `auctioneer_share_divisor` = 2
- `min_paintings_to_be_eligible` = 3
- `min_bid` = 0

## Round

1. **update** (all players): auctioneer = ((season + auction_in_season - 2) mod 4) + 1; every player's bid = 0 and message = ''; buyer = 0; high_bid = 0
2. **ask** (the seat equal to auctioneer): Remove the chosen card from the auctioneer's hand and set current_card to its artist. Tell all players: 'Seat {auctioneer} auctions a {current_card} painting.'
3. **update** (all players): The season count of current_card's artist (count_red, count_blue, count_green or count_yellow) rises by 1, whether or not the painting sells
4. **poll** (all players): Set each player's message, then broadcast to all: 'Seat {seat} says: {value}'. Messages are not binding.
5. **poll** (all players): Set each player's bid; no bid is shown to anyone
6. **update** (all players): high_bid = the highest bid. If high_bid = 0: buyer = 0 and the card is discarded. Otherwise buyer = the seat with the highest bid*4 + (3 - ((seat - auctioneer - 1) mod 4)), which breaks ties in the order auctioneer+1, auctioneer+2, auctioneer+3, then the auctioneer. Buyer's money -= high_bid. If buyer != auctioneer, auctioneer's money += floor(high_bid / 2), and the rest goes to the bank. current_card is appended to the buyer's collection, and the buyer's paintings_bought += 1.
7. **tell** (all players): Public: 'Seat {buyer} bought the {current_card} painting', or 'The {current_card} painting went unsold' when buyer = 0. Private to the buyer and to the auctioneer only: 'The price was {high_bid}.' Losing bids are never revealed.
8. **poll** (all players): Set each player's nomination. Each nomination adds 1 to that artist's season count. All nominations are then revealed to everyone.
9. **update** (all players): Each artist gets a key = count*10000 + value*10 + priority, where priority (3 highest) follows the season order: S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G. An artist's place = 1 + the number of artists with a higher key. An artist with count 0, or with place 4, gets place 0. Then value += 30 if place 1, 20 if place 2, 10 if place 3.
10. **update** (all players): For each player: payout_last = the sum, over the paintings in their collection, of that artist's value (after this season's increase) if the artist's place is 1 to 3, else 0. The player's money += payout_last. Tell each player privately: 'Your payout this season is {payout_last}.' Tell all players the four cumulative values.
11. **update** (all players): Every player's collection = []; count_red, count_blue, count_green and count_yellow = 0; every place = 0
12. **update** (all players): auctions_done += 1. If auction_in_season == 4, then season += 1 and auction_in_season = 1; otherwise auction_in_season += 1.
13. **check** (all players): If auctions_done == 16, the game ends and every player's final money is revealed to all; otherwise continue with the next auction

## Ending

- ends when: auctions_done == 16
- ranked by: `(you.paintings_bought >= 3) * (you.money + 1)` (the highest wins; players level at the top share the win)
- min_to_win: `1` (a player below it cannot win; if none reaches it, nobody wins)
- decided by: Only players who bought at least 3 paintings are eligible. Among them the most money wins, and eligible players tied for most money share the result. If nobody is eligible, nobody wins.

## Choices the source did not make

- 4 players (min 4, max 4, suggested 4): The designer fixed the table at 4. The auctioneer rotation, the tie-break order and the card counts (4 auctions per player plus 1 unused card each, with 4 cards set aside) all depend on exactly 4 seats.
- Talk kept as a simultaneous poll each auction, broadcast to all: The rules specify it. Players have opposing interests (an auctioneer wants high bids, a bidder wants a cheap buy, and nominations push artists up or down), so non-binding talk gives them something to bluff and reason about.
- Ranking and the bid tie-break are computed as numeric keys: This puts the stated tie-break orders into plain arithmetic without changing them.
- The ranking expression adds 1 to money and requires a value of at least 1: An eligible player with 0 money still beats every ineligible player, and if nobody is eligible nobody wins.
- Strategy at the table: Players balance spending against later payouts, use nominations to steer which artists place, read whose talk is a bluff, and make sure they buy 3 paintings to stay eligible.

## Simplifications

- The source's 'draw' among eligible players tied for most money becomes a shared win: The engine has no separate draw; players level at the top share the win, which is the equivalent outcome. 'No eligible player' becomes no winner through min_to_win.
- Each auction is one round; the season-end steps carry a when-condition (auction_in_season == 4): The step list is flat, so each season-end step is a single conditional step rather than a separate block.

## Unsupported (needs engine work)

- none
