# Modern Art: Sealed Gallery

Four art dealers take turns putting paintings by three artists up for sealed-bid auction. Each season ends when an artist's fourth painting appears, and the season's top two artists pay their owners. After three seasons the most money wins.

Players: 4 to 4, best with 4

## Parameters

- `player_count` = 4
- `deck_size` = 36
- `amber_cards` = 14
- `blue_cards` = 12
- `crimson_cards` = 10
- `hand_size` = 9
- `starting_money` = 100
- `season_end_count` = 4
- `first_artist_gain` = 30
- `second_artist_gain` = 20
- `third_artist_gain` = 0
- `seasons` = 3
- `max_turns` = 30
- `min_bid` = 0
- `rarity_amber` = 1
- `rarity_blue` = 2
- `rarity_crimson` = 3

## Round

1. **tell** (all players): Announce the season (season + 1) and that seat {auctioneer} is the auctioneer.
2. **ask** (the seat equal to auctioneer): Set current_card to the answer and reveal it to all.
3. **update** (the auctioneer): Remove one copy of current_card from the auctioneer's hand. Add 1 to played_<current_card>. Set season_ending = (played_<current_card> == 4). Announce the card and its new count.
4. **tell** (all players): When season_ending: announce that the 4th {current_card} ends the season, that the card is not auctioned, and that no one owns it.
5. **poll** (all players): When not season_ending: store each answer in message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
6. **poll** (all players): When not season_ending: store each answer in bid. No one sees a bid until all are in.
7. **update** (all players): When not season_ending: work out key = bid * 10 + (4 - ((seat - auctioneer + 4) mod 4)) for each player. Set winner_seat to the seat with the highest key, and price to that seat's bid. This breaks ties toward the auctioneer, then clockwise, and gives the card to the auctioneer free if every bid is 0.
8. **update** (winner_seat and auctioneer): When not season_ending: winner_seat's money -= price. If winner_seat != auctioneer, the auctioneer's money += price; otherwise the price goes to the bank. winner_seat's owned_<current_card> += 1. Announce all bids, the buyer and the price.
9. **update** (the table): When season_ending: give each artist the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3). first_artist = the highest key and second_artist = the middle key. value_<first_artist> += 30 and value_<second_artist> += 20. Announce the ranking and the values.
10. **update** (all players): When season_ending: each player's money += owned_<first_artist> * value_<first_artist> + owned_<second_artist> * value_<second_artist>, paid by the bank. Announce each payout.
11. **update** (all players and the table): When season_ending: set every owned_amber, owned_blue and owned_crimson to 0 and every played_amber, played_blue and played_crimson to 0. season += 1. Set season_ending to false. Hands are untouched.
12. **update** (the table): auctioneer = (auctioneer mod 4) + 1.
13. **check** (the table): If season == 3, end the game; otherwise continue.

## Ending

- ends when: season == 3
- ranked by: `you.money` (the highest wins; players level at the top share the win)
- decided by: After season 3, the player with the most money wins. Players tied for the most money share the result, which is a draw among them.

## Choices the source did not make

- Exactly 4 players, suggested 4: The designer fixed 4, and the deck deals exactly 9 cards to each of 4 players. Fewer players would leave no rivals to bid against; more would not fit the deal.
- Talk kept as a simultaneous poll before each bid: The source requires it. It also earns its place: players disagree about prices, and they can use it to talk up artists or bluff about their holdings.
- Bid tie-break encoded as the key bid * 10 + (4 - clockwise distance from the auctioneer): This gives the source's tie order, auctioneer first and then clockwise, in plain arithmetic, and it also covers the all-zero case.
- Artist ranking encoded as the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3): This gives the source's tie rule, rarer artist wins, in plain arithmetic.
- Cards are stored as artist names: Paintings of the same artist are indistinguishable in these rules.
- The 'auctioneer has no cards' skip is not built as a step: The source says it cannot happen: at most 30 cards are played and each hand holds 9.
- Money is marked observable: It is the score, and every payment is announced, even though money is formally known only to its owner.

## Simplifications

- The season-end block is written as individual steps each guarded by 'when season_ending', and the auction steps are guarded by 'when not season_ending': The step list is flat, but per-step conditions express the same flow exactly.
- A tie for most money is a shared win among the tied leaders: The engine has no separate draw. The rules call this a draw, and sharing the top is how that is reported.

## Unsupported (needs engine work)

- none
