# Scriptorium Lots (Seller's Edition)

Three players take turns seeing a secret two-card lot. The active player keeps one card and auctions the other to the two bidders. Winners can nudge colour worths, and majorities in each colour plus leftover gold decide the victor.

Players: 3 to 3, best with 3

## Parameters

- `start_gold` = 12
- `start_holding` = 0
- `start_worth` = 3
- `worth_min` = 1
- `worth_max` = 5
- `worth_shift` = 1
- `rounds` = 12
- `lot_count` = 12
- `cards_per_lot` = 2
- `lot_sum` = 5
- `lots_per_card` = 2
- `active_turns_per_seat` = 4
- `min_bid` = 0
- `tie_share_divisor` = 2
- `gold_per_vp` = 4
- `rank_vp_weight` = 1000

## Round

1. **update** (engine): Set active_seat = ((round - 1) mod 3) + 1. Set current_lot = lots[round]. Reset every player's bid to 0, and reset winner_seat and auction_recipient to 0.
2. **ask** (the active seat (active_seat)): Add the kept card's value to the active seat's holding in its colour (red, blue or green). Set auction_colour and auction_value to the other card. No other player sees current_lot or the kept card.
3. **tell** (all players): Announce: 'Round {round}: seat {active_seat} auctions {auction_colour} {auction_value}.'
4. **poll** (all players): Set each player's message, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in. Messages are not binding.
5. **poll** (the two seats other than active_seat): Set each bidder's bid. No bid is seen until both are in.
6. **update** (engine): Announce both bids. If one bid is strictly higher, set winner_seat to that bidder: the winner's gold falls by the bid, the active seat's gold rises by the bid, the auction_value is added to the winner's holding in auction_colour, and auction_recipient = winner_seat. If the bids are equal (including 0 and 0), nobody pays: the auction_value is added to the active seat's holding in auction_colour, and auction_recipient = active_seat.
7. **ask** (seat winner_seat, when winner_seat > 0): Adjust the chosen worth by 1, but only if the result stays within 1..5; otherwise nothing changes.
8. **tell** (all players): Announce: 'Seat {auction_recipient} received the auction card. Worths: Red {worth_red}, Blue {worth_blue}, Green {worth_green}.'
9. **update** (engine): Increase round by 1.
10. **update** (engine, when round > 12): For each colour C with worth W: let M = the highest holding in C, and N = the number of players holding M. If M = 0, nobody scores C. If N = 1, that player gains W colour VP. If N >= 2, each tied player gains floor(W / 2). Then set each player's vp = colour VP + floor(gold / 4), and reveal all holdings.
11. **check** (engine): End the game if round > 12; otherwise continue with the next round.

## Ending

- ends when: round > 12
- ranked by: `you.vp * 1000 + you.gold` (the highest wins; players level at the top share the win)
- decided by: Most VP wins (colour majorities at final worth, plus 1 VP per full 4 gold). A tie on VP is broken by more remaining gold. Players still tied share the win, which stands for the source's draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed 3: one seller and two rival bidders each round. The lot deduction and rotation (4 turns each) are built for 3 seats, so the minimum and maximum are both 3.
- Keep the simultaneous talk poll before bidding: The rules require it. Players disagree (the seller wants high bids, and bidders want cheap cards and to hide their colours), so bluffing about the kept card or about worth plans gives the others something to reason about.
- Ranking expression vp*1000 + gold: Total gold never exceeds 36, so a factor of 1000 puts VP first and gold as the tie-break. Remaining exact ties share the win, which is the engine's form of a draw.
- The shift question is always offered as all 7 options: The rules say a change past the limits simply has no effect, so the options do not need to depend on the current worths.
- A strategy exists: Thoughtful players track used lots to infer the seller's kept colour, bid by how much a card swings a majority, use worth shifts to raise colours they lead and sink rivals', and bluff in talk.

## Simplifications

- Bids are stored as a private attribute and announced in the resolve update: The engine's poll keeps answers hidden until all are in; the announcement then reveals both bids as the rules require.
- End scoring is a single update step that runs when round > 12, before the ending check: The engine's ending ranks by one expression, so the colour majorities are computed into vp first.

## Unsupported (needs engine work)

- none
