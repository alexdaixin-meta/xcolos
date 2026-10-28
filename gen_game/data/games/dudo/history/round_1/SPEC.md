# Open-Table Dudo

Bluffing dice game: players secretly roll dice, raise bids on how many dice show a face (ones are wild), and call Dudo to challenge; each lost challenge costs a die, and the last player with dice wins.

Players: 2 to 4, best with 3

## Parameters

- `start_dice_2_players` = 4
- `start_dice_3_players` = 3
- `start_dice_4_players` = 2
- `die_sides` = 6
- `wild_face` = 1
- `bid_face_min` = 2
- `bid_face_max` = 6
- `opening_quantity_divisor` = 4
- `opening_quantity_floor` = 1
- `raise_quantity_step` = 1
- `dice_lost_per_challenge` = 1
- `max_rounds` = 40

## Round

1. **update** (table): round_no += 1; loser = 0; action = ''; bid_qty = 0; bid_face = 0
2. **tell** (all players): Announce each seat's dice, total_dice (T), the current bid (current_qty x current_face by current_bidder, or 'none'), bids, and that seat to_act is to act
3. **ask** (seat to_act): action = the choice
4. **ask** (seat to_act, when action is 'bid' or 'raise'): bid_qty = the number
5. **ask** (seat to_act, when action is 'bid' or 'raise'): bid_face = the number
6. **update** (table, when action is 'bid' or 'raise'): current_qty = bid_qty; current_face = bid_face; current_bidder = to_act; append 'seat to_act: bid_qty x bid_face' to bids; to_act = the next seat clockwise from to_act with eliminated = false; announce the new bid
7. **update** (table, when action = 'dudo' and current_qty = 0): Failed opening: loser = to_act; that player's dice -= 1; announce that the opener lost a die with no count
8. **update** (table, when action = 'dudo' and current_qty > 0): Reveal every player's faces to all; matching = number of faces over all surviving players equal to current_face or to 1; if matching >= current_qty then loser = to_act (the caller), else loser = current_bidder; the loser's dice -= 1; announce the reveal, matching, and the loser
9. **update** (table, when loser > 0): Every player with dice = 0 gets eliminated = true, announced; survivors = number of players with dice >= 1
10. **check** (table): End the game if survivors = 1
11. **update** (table, when loser > 0): opener = loser if the loser has eliminated = false, else the next seat clockwise from loser with eliminated = false; current_qty = 0; current_face = 0; current_bidder = 0; empty bids; each surviving player's faces = dice new random integers from 1 to 6, shown privately to the owner; total_dice = sum of dice; to_act = opener
12. **sync** (all players): Each player is sent their own faces and the public state
13. **check** (table): End the game if round_no >= 40; a hand still in progress is not resolved

## Ending

- ends when: survivors = 1 or round_no >= 40
- ranked by: `you.dice` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is the number of dice they hold. If only one player has dice, they win alone. If round 40 ends with several players holding dice, the player with the most dice wins, and players tied for the most share the win (a draw among them). Every other player loses.

## Choices the source did not make

- 2 to 4 players, suggested 3: The designer suggests 3. The minimum is 2 because one rival is enough to bluff against. The maximum is 4 because the source scales starting dice only that far (2 each at 4 players), and more seats would leave too few dice per player.
- Starting dice written as 6 minus the player count: This matches 4, 3 and 2 for 2, 3 and 4 players, so it holds at every table size.
- No separate talk step: The bids themselves are the communication and bluff. Free talk would add words without a decision the rules contain.
- The opener is offered 'dudo' at an empty table: The source explicitly gives this option and its penalty (the opener loses 1 die).
- Strategy at the table: A thoughtful player estimates expected matches from their own faces plus about a third of unseen dice (ones are wild), raises to a bid they can defend, bluffs when the next player is likely to over-call, and calls Dudo when a bid exceeds a plausible count.

## Simplifications

- Invalid bids cannot be entered: The engine restricts answers to the allowed choices and number ranges, so the source rules 'an invalid bid or raise counts as Dudo / a failed opening' never trigger.
- A bid is asked as three questions: action, quantity, face: Each answer must be a single choice or a single number.
- 'Next surviving seat clockwise' is computed arithmetically over seat numbers and eliminated flags: The engine has no seating operand; this uses the player-attribute comparison workaround.
- Rolling dice is modeled as setting the faces list to random integers from 1 to 6: The engine's seeded randomness stands in for physical dice.

## Unsupported (needs engine work)

- none
