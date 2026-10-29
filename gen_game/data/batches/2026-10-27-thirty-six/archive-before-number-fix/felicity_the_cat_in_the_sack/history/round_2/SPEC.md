# Cat in the Sack: Two-Stage Auction

Each round every player secretly adds one card to a shared sack, then everyone bids mice in two simultaneous sealed stages for a sack whose cards are only partly revealed. Final score is cat points plus mice.

Players: 3 to 5, best with 4

## Parameters

- `starting_hand_size` = 10
- `set_aside_per_player` = 1
- `hand_size_after_setup` = 9
- `starting_mice` = 15
- `starting_cat_points` = 0
- `rounds` = 9
- `stage1_pass_bonus` = 2
- `stage2_loser_bonus` = 3
- `stage1_min_bid` = 0
- `cat_minus8_value` = -8
- `cat_minus5_value` = -5
- `cat_3_value` = 3
- `cat_5_value` = 5
- `cat_8_value` = 8
- `cat_11_value` = 11
- `cat_15_value` = 15
- `rabbit_value` = 0
- `large_dog_value` = 0
- `small_dog_value` = 0
- `dogs_needed_for_dog_rule` = 1
- `tiebreak_multiplier` = 1000

## Round

1. **update** (all players): For every player, set bid=0, effective_bid=0 and in_auction=true. Set standing_bid=0, leader_seat=0, bidder_count=0, sack_done=false, sack_winner=0, winning_bid=0 and sack_value=0. Set sack_cards=[] and sack_revealed=[].
2. **poll** (all players): The chosen card is removed from that player's hand and stored as their played_card, which is private.
3. **update** (all players): Set sack_owners to all seats in order, starting at start_seat and counting upward, wrapping from the last seat to seat 1. Set sack_cards to each owner's played_card in that same order. Announce sack_owners to everyone.
4. **poll** (all players): No state change. Broadcast to all: "Seat {seat} says: {value}". Talk is not binding.
5. **update** (all players): Stage 1: reveal sack_cards[1] (the start player's card) by appending it to sack_revealed, and announce it. standing_bid stays 0.
6. **poll** (all players): Store the number as that player's bid.
7. **update** (all players): Announce every bid by seat. For each player with bid=0 or bid>mice: mice += 2 and in_auction=false. Set bidder_count = the number of players with in_auction=true. If bidder_count=0: sack_done=true and start_seat = (start_seat mod N) + 1. If bidder_count=1: sack_winner = that seat and winning_bid = that player's bid. If bidder_count>=2: standing_bid = the highest bid, and leader_seat = the seat with that bid; on a tie, the tied seat with the smallest (seat - start_seat - 1 + N) mod N.
8. **update** (all players): When bidder_count>=2 (stage 2): reveal sack_cards[2] by appending it to sack_revealed, and announce it.
9. **poll** (each player with in_auction=true, when bidder_count>=2): Store the number as that player's bid.
10. **update** (all players): When bidder_count>=2: announce every stage-2 number by seat. For the leader, effective_bid = standing_bid if bid=0, else bid. For any other in_auction player, effective_bid = bid if standing_bid < bid <= mice, else 0. sack_winner = the seat with the highest effective_bid. On a tie, the leader wins if tied; otherwise the tied seat with the smallest (seat - start_seat - 1 + N) mod N wins. winning_bid = the winner's effective_bid. Every other player with in_auction=true gets mice += 3.
11. **update** (all players): When sack_winner != 0 (taking the sack): the winner pays mice -= winning_bid. Reveal all of sack_cards by setting sack_revealed = sack_cards. Dog rule, only when exactly one of large_dog and small_dog is in sack_cards. Large dog: remove the highest positive cat, or the most negative cat if there is no positive cat. Small dog: remove the most negative cat, or the lowest positive cat if there is no negative cat. No cat: nothing happens. sack_value = the sum of the remaining cat values (rabbit and dogs count 0). The winner gets cat_points += sack_value. Set start_seat = sack_winner and sack_done = true.
12. **update** (all players): Append all of sack_cards to discard_pile and set sack_cards=[]. round_number += 1. Announce mice and cat_points for every seat.
13. **sync** (all players): Each player is sent their own state (hand, mice, cat_points).
14. **check** (all players): If round_number >= 9 the game ends; otherwise the next round begins.

## Ending

- ends when: round_number >= 9
- ranked by: `(you.cat_points + you.mice) * 1000 + you.cat_points` (the highest wins; players level at the top share the win)
- decided by: Each player's score is cat_points + mice, and the highest score wins. Among tied players, more cat_points wins. Players still tied share the win (a draw).

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggests 4, which is kept. 3 is the minimum for a sack built from several hidden cards with rivals bidding. Above 5 the sack and the bidding become too diluted for one card or bid to matter.
- Talk is a simultaneous poll broadcast to all: The rules say messages are written simultaneously without seeing the others. Players disagree about the sack's value, so bluffing about one's own card matters.
- The tie-break uses the order (seat - start_seat - 1 + N) mod N: This is the arithmetic form of 'first tied seat starting from the seat after start_seat'.
- rank_by = (cat_points + mice) * 1000 + cat_points: This encodes score first and cat_points as the tie-break. |cat_points| stays well below 500 given the finite cards.
- Card values are read from the card name (cat_X is worth X; rabbit and dogs are worth 0): The rules give cards as named tokens with these values.
- Players are offered only legal numbers, though the rules also say out-of-range numbers mean pass or drop out: The engine offers ranges. The out-of-range rule is still stated so the resolution stays faithful.

## Simplifications

- The branches 'round ends' and 'go to R10' are run as per-step `when` conditions on bidder_count and sack_winner in a flat step list: The engine has no block branching. Single steps with arithmetic conditions give the same result.
- The dog rule and sack_value are worked out in one update step with conditional arithmetic over sack_cards: The removal rules are deterministic arithmetic, so no referee is needed.

## Unsupported (needs engine work)

- none
