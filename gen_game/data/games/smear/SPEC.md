# Pocket Smear

A three-player trick-taking game of 9 four-trick deals: bid blind, the highest bidder names trump, then everyone fights for High, Low, Game and Three while the pitcher tries to make the contract.

Players: 3 to 3, best with 3

## Parameters

- `players` = 3
- `deals` = 9
- `tricks_per_deal` = 4
- `total_rounds` = 36
- `suits` = 3
- `ranks_per_suit` = 8
- `deck_size` = 24
- `hand_size` = 4
- `set_aside_cards` = 12
- `bid_min` = 2
- `bid_max` = 6
- `pass_value` = 0
- `all_pass_contract` = 2
- `card_points_rank_8` = 4
- `card_points_rank_7` = 3
- `card_points_rank_6` = 2
- `card_points_rank_5` = 1
- `card_points_other_ranks` = 0
- `high_points` = 1
- `low_points` = 1
- `game_points` = 1
- `three_points` = 3
- `three_rank` = 3
- `max_deal_points` = 6
- `starting_score` = 0

## Round

1. **update** (all players): When trick_in_deal == 1: dealer = ((deal_number - 1) mod 3) + 1; deck = all 24 card codes; for each player, clear hand, captured and played_card, and set captured_points = 0, deal_points = 0, bid = 0, bid_suit = ''; draw 4 cards at random from deck into each player's hand; move the remaining 12 deck cards into set_aside; reset high_trump_rank = 0, high_trump_seat = 0, low_trump_rank = 9, low_trump_seat = 0, three_seat = 0.
2. **sync** (all players): When trick_in_deal == 1: each player sees their own hand, the dealer and every score.
3. **poll** (all players): When trick_in_deal == 1: bid = n (0 for PASS); bid_suit = the named suit. The bid amounts are broadcast: 'Seat {seat} bids {bid or PASS}'. The suits are not shown.
4. **update** (all players): When trick_in_deal == 1: if max(bid) > 0, pitcher = the seat with the highest bid, ties going to the earliest seat in priority order (dealer+1, dealer+2, dealer, mod 3), and contract = that bid; otherwise pitcher = dealer and contract = 2. trump = pitcher's bid_suit; leader = pitcher.
5. **tell** (all players): When trick_in_deal == 1: announce 'Pitcher: Seat {pitcher}, contract {contract}, trump {trump}'.
6. **ask** (seat leader): played_card = chosen card; remove it from hand; led_suit = floor(card/10); broadcast the card to all.
7. **ask** (seat (leader mod 3) + 1): played_card = chosen card; remove it from hand; broadcast the card to all.
8. **ask** (seat ((leader + 1) mod 3) + 1): played_card = chosen card; remove it from hand; broadcast the card to all.
9. **update** (all players): trick_winner = the seat whose played_card has suit == trump and the highest rank, or if no trump was played, the seat with the highest rank of led_suit. Append all three played cards to trick_winner's captured; add their card points to trick_winner's captured_points. For each played trump of rank r: if r > high_trump_rank, set high_trump_rank = r and high_trump_seat = trick_winner; if r < low_trump_rank, set low_trump_rank = r and low_trump_seat = trick_winner; if r == 3, set three_seat = trick_winner. Then leader = trick_winner, clear every played_card and announce the winner.
10. **update** (all players): When trick_in_deal == 4: deal_points = (seat == high_trump_seat ? 1 : 0) + (seat == low_trump_seat ? 1 : 0) + (captured_points strictly greater than both other players' captured_points ? 1 : 0) + (seat == three_seat ? 3 : 0). For each non-pitcher, score += deal_points. For the pitcher: if deal_points >= contract, score += deal_points; else score -= contract. Announce every deal_points value and score. Clear every captured pile.
11. **update** (all players): rounds_played += 1; if trick_in_deal == 4, then trick_in_deal = 1 and deal_number += 1; otherwise trick_in_deal += 1.
12. **check** (all players): End the game if rounds_played == 36 (9 deals scored); otherwise continue.

## Ending

- ends when: rounds_played == 36
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 9 deals; the highest score wins, and players tied for highest share the result (the source calls this a draw).

## Choices the source did not make

- 3 players, fixed: The designer set exactly 3; the priority order, dealer rotation and 12 set-aside cards are all built for 3 seats.
- Card encoding suit*10+rank (Red 1, Blue 2, Green 3): Lets trick winners, trump checks and card points be worked out by arithmetic; players see card names.
- Bid offered as one combined choice such as '4 Blue' or 'PASS Red': The engine takes one answer per question; listing only suits from the seat's own hand enforces that rule.
- PASS stored as bid 0: Allows a numeric comparison for the highest bid and an all-pass test with max(bid) == 0.
- No talk step: The rules forbid table talk; players communicate only through bids and cards.
- Strategy at the table: Players judge their hand's trump strength, bid against two rivals, and decide when to trump in, cash High or protect the 3, reading what is left from the cards played.

## Simplifications

- A tie for the highest final score is a shared win rather than a separate draw: The engine ranks by one expression and players level at the top share the win; this is the same outcome as a draw.
- Deal-start actions (deal, bid, pitcher resolution) are single steps carrying a 'when trick_in_deal == 1' condition: The step list is flat; per-step conditions reproduce the first round of each deal.

## Unsupported (needs engine work)

- none
