# Short Dudo

A short bluffing dice game. Players bid on how many dice around the table show a face, with 1s wild. The next players raise, call Dudo (false) or call Calza (exact), and the loser of each call loses a die.

Players: 2 to 4, best with 3

## Parameters

- `start_dice` = 5
- `max_dice` = 5
- `die_faces` = 6
- `wild_face` = 1
- `min_bid_face` = 2
- `max_bid_face` = 6
- `opening_min_divisor` = 3
- `opening_min_floor` = 1
- `opening_max_divisor` = 2
- `raise_small` = 1
- `raise_big` = 2
- `dudo_loss` = 1
- `calza_loss` = 1
- `calza_gain` = 1
- `max_rounds` = 30
- `first_opener_seat` = 1
- `max_responses_per_round` = 3

## Round

1. **update** (all players): round_num += 1. call_type = '', caller_seat = 0 and loser_seat = 0. total_dice = sum of dice_count over players with out = false.
2. **initialize** (all players): In one deal, every player with out = false gets hand set to dice_count random faces from 1 to 6. Out players keep an empty hand.
3. **sync** (all players): Each player sees their own hand, total_dice and every player's dice_count and out.
4. **ask** (seat opener_seat): current_face = the chosen face. current_bidder = opener_seat.
5. **ask** (seat opener_seat): current_qty = the number. The bid is announced to all. responder_seat = the next seat after current_bidder with out = false.
6. **ask** (seat responder_seat (response 1)): On raiseK_faceF: current_qty += K, current_face = F, current_bidder = responder_seat, then responder_seat = the next seat after current_bidder with out = false. On dudo or calza: call_type = the choice, caller_seat = responder_seat. The choice is announced to all.
7. **ask** (seat responder_seat (response 2), when call_type = ''): The same as response 1. With 2 players this seat is the opener.
8. **ask** (seat responder_seat (final response), when call_type = ''): call_type = the choice, caller_seat = responder_seat. The choice is announced to all.
9. **update** (all players): Reveal: every hand is shown to all. reveal_count = count over all hands of dice equal to current_face or equal to 1.
10. **update** (all players): Settle. If call_type = 'dudo' and reveal_count >= current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. If call_type = 'dudo' and reveal_count < current_qty: current_bidder dice_count -= 1, loser_seat = current_bidder. If call_type = 'calza' and reveal_count = current_qty: caller_seat dice_count = min(dice_count + 1, 5), loser_seat = 0. If call_type = 'calza' and reveal_count != current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. The result is announced.
11. **update** (all players): Elimination: any player with dice_count = 0 gets out = true.
12. **update** (all players): Next opener. If loser_seat > 0, opener_seat = loser_seat; otherwise (a successful Calza) opener_seat = caller_seat. If that seat has out = true, opener_seat = the next seat after it with out = false.
13. **check** (all players): End the game if the number of players with out = false is 1, or if round_num >= 30. Otherwise start a new round.

## Ending

- ends when: count of players with out = false == 1 OR round_num >= 30
- ranked by: `you.dice_count` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is the dice they hold. A lone survivor holds the only dice and wins. After 30 rounds the player with the most dice wins, and players tied for the most share the result, which is the source's draw.

## Choices the source did not make

- 2 to 4 players, suggested 3: The designer suggests 3. Two is the smallest table where a bid can be doubted. Above 4 the 3-response limit means most seats never act in a round.
- No talk phase: The source says bids and calls are the only communication. Bluffing happens through the bids themselves.
- Strategy at the table: A thoughtful player estimates the expected count from their own hand plus T/3 for the unseen dice, bluffs bids toward faces they hold, reads the raises of others, and saves Calza for when they hold the bid face, since a correct Calza gains a die.

## Simplifications

- The opening bid is asked as two questions to the same seat, face then quantity: One answer is either a choice or a number, never both.
- A raise and its face are offered as one combined choice, such as raise2_face4: This lets one choice question carry the raise size and the face, with illegal raises left out.
- A tie for most dice after 30 rounds is a shared top result rather than a separate 'draw' outcome: The engine has no separate draw. Players level at the top share the win, which records the draw.

## Unsupported (needs engine work)

- none
