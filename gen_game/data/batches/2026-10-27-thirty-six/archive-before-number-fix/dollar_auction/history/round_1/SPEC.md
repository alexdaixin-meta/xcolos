# War of Attrition Auctions

Over 6 sealed-raise auctions, players pay their full committed bids whether or not they win, and chase prizes whose values each player knows only for themselves.

Players: 3 to 4, best with 3

## Parameters

- `starting_coins` = 100
- `auctions` = 6
- `raise_stages` = 3
- `prize_value_1` = 10
- `prize_value_2` = 15
- `prize_value_3` = 20
- `prize_value_4` = 25
- `prize_value_5` = 30
- `prize_value_6` = 40
- `prize_value_total` = 140
- `min_winning_bid` = 1

## Round

1. **update** (all players): auction += 1; auction_winner = 'none'; every player's committed = 0
2. **tell** (all players): Announce 'Auction {auction} of 6 begins.'
3. **sync** (all players): Each player is sent their own coins, committed and values, plus their value for this auction, values[auction].
4. **poll** (all players): Messages are collected simultaneously, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes; messages are not binding.
5. **poll** (all players): Raise stage 1: each player's raise = answer; then committed += raise for every player.
6. **tell** (all players): Announce every player's committed bid after stage 1.
7. **poll** (all players): Raise stage 2: each player's raise = answer; then committed += raise for every player.
8. **tell** (all players): Announce every player's committed bid after stage 2.
9. **poll** (all players): Raise stage 3: each player's raise = answer; then committed += raise for every player.
10. **tell** (all players): Announce every player's final committed bid.
11. **update** (all players): top_bid = max over players of committed; top_count = number of players with committed == top_bid.
12. **update** (all players): For the player with committed == top_bid, if top_count == 1 and top_bid >= 1: prize_points += values[auction] and auction_winner = that seat. The value is not announced.
13. **update** (all players): Every player: coins -= committed, whether or not they won.
14. **tell** (all players): Announce 'Auction {auction} winner: {auction_winner}' and every player's remaining coins.
15. **update** (all players): Every player's committed = 0 and raise = 0.
16. **update** (all players): when auction == 6: every player's final_score = coins + prize_points; every player's values and prize_points are revealed to all.
17. **check** (all players): If auction >= 6, end the game; otherwise run the round again.

## Ending

- ends when: auction >= 6
- ranked by: `you.coins + you.prize_points` (the highest wins; players level at the top share the win)
- decided by: Each player's final score is coins remaining plus prize points. The highest final score wins; players tied at the top share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer suggested 3. With 3, a tie between two bidders lets the third steal cheaply, and talk can form two-against-one splits. At 4 the auctions are still contested. More would dilute each player's influence and lengthen talk beyond the source's range.
- Talk as a simultaneous poll with broadcast: The source says messages are written at the same time without seeing others. Players disagree over who takes which auction, so claims and bluffs about values matter.
- Each player's value ordering built by drawing all six values at random from a copy of prize_deck: This implements the 'random ordering' dealing with list draws.
- prize_points visible only to the owner until the end: The source says won values are not revealed. Only who won is announced.

## Simplifications

- A tie for the highest final score is a shared win rather than a separate draw: The engine ranking has tied top players share the win, which is equivalent to the source's draw.
- The highest bid is found through table attributes top_bid and top_count: The engine has no direct player-to-player attribute comparison, so a table attribute is kept beside the bids.
- A final_score attribute is set at the end: It gives an observable score, since prize_points stay hidden during play.

## Unsupported (needs engine work)

- none
