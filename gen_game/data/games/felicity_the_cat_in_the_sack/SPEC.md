# Cat in the Sack: Paid Entry

Each round every player secretly puts one card into a shared sack. Some sack cards are revealed, players talk, then pay to stay or get paid to drop. Stayers bid sealed mice for the sack, whose cat value may be negative.

Players: 3 to 5, best with 4

## Parameters

- `cat_value_1` = -8
- `cat_value_2` = -5
- `cat_value_3` = 3
- `cat_value_4` = 5
- `cat_value_5` = 8
- `cat_value_6` = 11
- `cat_value_7` = 15
- `rabbit_value` = 0
- `dog_value` = 0
- `cards_per_hand` = 9
- `cards_removed_per_hand` = 1
- `starting_mice` = 15
- `starting_cat_points` = 0
- `rounds` = 8
- `stay_fee` = 1
- `drop_payment` = 2
- `min_mice_to_stay` = 2
- `min_bid` = 1
- `first_reveal_with_3_players` = 1
- `first_reveal_with_4_or_5_players` = 2
- `second_reveal_count` = 1
- `dogs_that_cancel_top_cat` = 1
- `start_seat_round_1` = 1

## Round

1. **update** (table): round += 1. start_seat = ((round - 1) mod player_count) + 1. Every player: stayed = false, bid = 0, placed_card = ''. sack = [], revealed_cards = [], winner_seat = 0, sack_value = 0. Announce the round and the start seat.
2. **poll** (all players): Each player's choice is removed from hand, stored in placed_card and appended to sack. Nobody sees the choices.
3. **update** (table): Shuffle the sack: rebuild it by repeatedly drawing a card at random from it, which gives a random order.
4. **update** (table): First reveal: append the first k cards of sack to revealed_cards, where k = 1 if player_count = 3, else 2. Tell everyone the revealed cards, without owners.
5. **poll** (all players): message is set for each player. Broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all messages are in.
6. **poll** (all players): stayed = true for STAY, false for DROP. stayer_count = number of players with stayed = true. All choices are shown together.
7. **update** (all players): Each player with stayed = true: mice -= 1 (never refunded). Each player with stayed = false: mice += 2.
8. **update** (table): Second reveal: append sack card number k+1 to revealed_cards, where k is the first-reveal count. Tell everyone.
9. **poll** (each player with stayed = true): bid is set for each stayer. All bids are revealed together.
10. **update** (table): If stayer_count = 0: winner_seat = 0. Otherwise winner_seat is the stayer with the highest key = bid * 100000 - mice * 100 - ((seat - start_seat + player_count) mod player_count). The ordering is: highest bid, then fewer current mice, then first in seat order counting from start_seat. Announce it.
11. **update** (table): Reveal all sack cards to everyone. Let cats = the values of the cat_ cards in sack, and dogs = the count of 'dog' in sack. sack_value = sum(cats), minus max(cats) if dogs = 1 and at least one cat is present. Rabbit and dog are worth 0, and 2 or more dogs have no effect. Announce sack_value.
12. **update** (the winner_seat player): If winner_seat != 0: that player's mice -= bid and cat_points += sack_value (which may be negative). Losing stayers change nothing more.
13. **update** (table): Append every sack card to discard (face up, public). sack = []. Announce mice and cat_points.
14. **check** (table): If round >= 8, end the game. Otherwise continue to the next round.

## Ending

- ends when: round >= 8
- ranked by: `(you.mice + you.cat_points) * 1000 + you.cat_points` (the highest wins; players level at the top share the win)
- decided by: Each player's total is cat_points plus mice, and the highest total wins. If totals tie, the tied player with more cat points wins. If that also ties, those players share the win (a draw).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer chose 4 and the source allows 3 to 5. 3 is the minimum because an auction needs rivals and the sack needs enough unknown cards to hide one's own. 5 is the maximum because the hand and reveal structure is built for 5, and with more seats one's own card would barely affect the sack.
- Talk kept as a simultaneous poll with broadcast: The source specifies simultaneous non-binding messages. Players disagree about the sack, since each wants others to drop or to overbid, so bluffing about one's placed card gives the others something to reason about.
- Cards encoded as text labels cat_<value>, rabbit and dog: The rabbit and dog are both worth 0 but behave differently, so a label is needed to count dogs.
- Cat card values listed as separate parameters cat_value_1 to cat_value_7: Each parameter must be a single number.
- Sack winner computed as one key: bid * 100000 - mice * 100 - seat offset from start_seat: This puts the source's three-level tie-break (bid, fewer mice, seat order from the start player) into a single arithmetic maximum.
- Ranking expression (mice + cat_points) * 1000 + cat_points: Cat points can never reach plus or minus 500, so the total is compared first and cat points break ties. Exact ties share the win, which is the source's draw.
- Stay/drop choices and bids are public once revealed: The source reveals bids together, and paying the fee or receiving the drop payment is visible. Who placed which card stays secret.
- Strategy at the table: A thoughtful player infers others' cards from the public discard, the reveals and their own removed card. They bluff in talk and weigh the 1-mouse fee against the 2-mouse drop payment. They also use the fewer-mice tie-break and the dog rule when sizing a bid.

## Simplifications

- The shuffle is done by drawing the sack cards at random into a new order: The engine shuffles by random draws from a list.
- The bank of mice is not tracked: It is unlimited, so only player mice change.
- A draw is represented as a shared win among the players tied at the top: The engine has no separate draw outcome.

## Unsupported (needs engine work)

- none
