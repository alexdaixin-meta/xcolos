# Rutersju Twelve

A 12-deal trick-taking game: each player is dealt 3 cards, players bid 0 to 3 in turn, the highest bidder plays to take exactly that many tricks, and the opponents score when the declarer misses.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 36
- `suits` = 4
- `ranks_per_suit` = 9
- `hand_size` = 3
- `tricks_per_deal` = 3
- `deals` = 12
- `bid_min` = 0
- `bid_max` = 3
- `made_bonus` = 1
- `starting_score` = 0
- `first_bidder_deal_1` = 1

## Round

1. **update** (all players): Add 1 to deal_number. Set first_bidder = ((deal_number - 1) mod N) + 1. Refill deck with all 36 cards. For every player, clear hand and set bid = 0, tricks = 0 and is_declarer = false. Set high_bid = -1, declarer_seat = 0, contract = 0, trick_number = 0 and led_suit = ''. Clear trick_cards and played_cards.
2. **update** (all players): Deal 3 cards to each player. Each card is drawn at random from deck, appended to that player's hand and removed from deck.
3. **sync** (all players): Each player is shown their own hand, plus deal_number, first_bidder and every score.
4. **ask** (each player in turn, clockwise, starting at first_bidder): Set the player's bid to the answer and broadcast it to all. If bid >= high_bid, set high_bid = bid and declarer_seat = the player's seat. Because the comparison is >=, a later equal bid takes the declarership.
5. **update** (all players): Set contract = high_bid and leader_seat = declarer_seat. Set is_declarer = true for the player at declarer_seat. Announce the declarer and the contract.
6. **ask** (each player in turn, clockwise, starting at leader_seat): Remove the card from hand and append seat:card to trick_cards and to played_cards. If this is the first card of the trick, set led_suit to its suit. Broadcast the played card to all.
7. **update** (all players): If trick_cards contains 7D, its player wins the trick. Otherwise the highest-ranked card of led_suit wins (A>K>Q>J>10>9>8>7>6). Add 1 to the winner's tricks, set leader_seat = the winner's seat, add 1 to trick_number, clear trick_cards and set led_suit = ''. Announce the trick winner.
8. **repeat** (all players): Run the two previous steps (play a trick, resolve the trick) again until trick_number = 3.
9. **update** (all players): Let D be the player with is_declarer = true. If D.tricks = contract, add contract + 1 to D.score. Otherwise add |contract - D.tricks| to the score of every player with is_declarer = false, and D scores nothing. Opponents' own tricks are not scored.
10. **tell** (all players): Announce every player's score after deal {deal_number}.
11. **check** (all players): End the game if deal_number = 12. Otherwise continue with the next deal.

## Ending

- ends when: deal_number = 12 after the 12th deal is scored
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 12 deals. The highest total wins. Players tied for the highest total share the result, which the source calls a draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The source allows 3 to 4 and the designer chose 4. Three is the smallest table with more than one opponent to set the contract against. More than 4 would exceed the 36-card pack's balance and make each trick too crowded for a 3-card hand to steer.
- No talk step: The rules forbid discussion; players communicate only through bids and cards.
- Card codes such as 'AS', '10H', '7D': A text code per card lets the engine check suits and ranks arithmetically.
- Declarer tie-break done by updating on bid >= high_bid in bidding order: This makes the last of the tied highest bidders the declarer, exactly as the rules require, using only arithmetic.
- Strategy at the table: A thoughtful player bids from hand strength and from the bids already made, since bidding last wins ties. Opponents cooperate to break the contract, either by taking tricks from the declarer or by giving tricks away when the declarer bid low.

## Simplifications

- The source's draw on a tied top total is represented as a shared win among the tied players: The engine has no separate draw; players level at the top share the result.
- The 3-trick play loop is expressed as a repeat over two steps: The engine runs flat step lists and repeats them until a condition holds.

## Unsupported (needs engine work)

- none
