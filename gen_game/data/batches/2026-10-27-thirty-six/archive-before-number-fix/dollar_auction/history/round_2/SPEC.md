# Escalation Auction

Six sealed all-pay auctions, each with three simultaneous raise stages. Every bidder pays what they committed, only a sole top bidder wins their private prize value, and the highest coins plus prize points wins.

Players: 3 to 5, best with 3

## Parameters

- `starting_coins` = 100
- `auctions` = 6
- `raise_stages` = 3
- `min_winning_bid` = 1
- `prize_value_1` = 10
- `prize_value_2` = 15
- `prize_value_3` = 20
- `prize_value_4` = 25
- `prize_value_5` = 30
- `prize_value_6` = 40
- `prize_values_total` = 140
- `initial_prize_points` = 0
- `initial_committed` = 0
- `initial_final_score` = 0
- `min_raise` = 0
- `winning_top_count` = 1

## Round

1. **update** (all players): auction += 1. Every player's committed = 0. Every player's current_value = entry number 'auction' (1-based) of their values list.
2. **sync** (all players): Each player is privately sent their current_value for this auction.
3. **tell** (all players): Announce: 'Auction {auction} of 6.' plus every seat's coins.
4. **poll** (all players): No state change. Broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in.
5. **poll** (all players): Raise stage 1: each player's committed += their raise.
6. **tell** (all players): Announce every seat's committed after stage 1.
7. **poll** (all players): Raise stage 2: each player's committed += their raise.
8. **tell** (all players): Announce every seat's committed after stage 2.
9. **poll** (all players): Raise stage 3: each player's committed += their raise.
10. **tell** (all players): Announce every seat's committed after stage 3.
11. **update** (all players): top_bid = max over players of committed. top_count = number of players with committed == top_bid. Every player's coins -= committed.
12. **update** (all players): If top_count == 1 and top_bid >= 1: auction_winner = the seat with committed == top_bid, and that player's prize_points += their current_value. Otherwise auction_winner = 'none'.
13. **tell** (all players): Announce: 'Auction {auction} winner: {auction_winner}.' plus every seat's coins.
14. **update** (all players): Every player's committed = 0. If auction == 6: every player's final_score = coins + prize_points.
15. **check** (all players): End the game if auction >= 6. Otherwise continue to the next round.

## Ending

- ends when: auction >= 6
- ranked by: `you.final_score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is final_score = coins remaining + prize_points. The highest final_score wins, and players tied at the top share the win (a draw among them).

## Choices the source did not make

- 3 to 5 players, suggested 3: The designer chose 3, and an auction needs at least two rivals for ties and bid-reading to matter. Above 5, the talk and announcements grow long and each player wins too few of the 6 auctions for budgeting to matter.
- Keep the simultaneous talk poll: The rules require it, and players genuinely disagree: everyone wants rivals to back off. Bluffs and threats about which auctions they value give players something to reason about, and since talk is not binding, believing it can be costly.
- prize_points visible only to its owner: The rules announce only the winner and coins. Publishing prize_points would reveal the winner's private value for that auction.
- Values entries indexed from 1: The rules say entry k is the value for auction k, and auction runs from 1 to 6.
- Strategy at the table: This is an all-pay auction, so overbidding is costly and ties waste both bids. A thoughtful player rations 100 coins over 6 auctions, pushes on high-value auctions, watches rivals' committed totals between stages, and avoids matching a rival's total.

## Simplifications

- The 3 raise stages are written out as explicit poll and tell steps rather than as a repeat: This keeps the flat step list clear without a scratch stage counter, and the behaviour is identical.
- final_score is computed in the last update of the 6th round: It is the same arithmetic as R10, placed just before the ending check.

## Unsupported (needs engine work)

- none
