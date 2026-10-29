# Malý Mariáš (Little Mariáš)

Three-player trick-taking game with 12 cards: a secret bid picks a declarer, contract and trump, defenders may double (flek) and the declarer redouble (re), and 9 deals of 4 tricks are settled zero-sum.

Players: 3 to 3, best with 3

## Parameters

- `num_cards` = 12
- `num_suits` = 4
- `num_ranks` = 3
- `cards_per_hand` = 4
- `ace_points` = 10
- `ten_points` = 10
- `king_points` = 0
- `last_trick_bonus` = 10
- `points_per_deal` = 90
- `deals` = 9
- `tricks_per_deal` = 4
- `total_rounds` = 36
- `bid_min` = 50
- `bid_max` = 90
- `bid_step` = 10
- `eldest_default_bid` = 50
- `stake_divisor` = 10
- `stake_offset` = 4
- `initial_multiplier` = 1
- `flek_factor` = 2
- `re_factor` = 2
- `hearts_factor` = 2
- `declarer_win_factor` = 2
- `declarer_loss_factor` = 2
- `trump_key_bonus` = 10
- `led_suit_key_bonus` = 5
- `initial_score` = 0

## Round

1. **update** (table): [when trick = 1] Shuffle deck once. Give positions 1-4 to seat 1's hand, 5-8 to seat 2's hand and 9-12 to seat 3's hand. Set declarer_points = 0, defender_points = 0, multiplier = 1, trick_cards = [], trick_seats = [].
2. **sync** (all players): [when trick = 1] Each player is sent their own hand and the public state.
3. **poll** (all players): [when trick = 1] Set each player's bid. If the eldest answers PASS or an invalid bid, it becomes '50 A'. An invalid answer from any other player becomes 'PASS'. Set bid_value = N, or 0 for PASS.
4. **update** (table): [when trick = 1] The declarer is the seat with the highest value of bid_value*10 + (3 - ((seat - eldest) mod 3)), so ties go to the seat first in order from the eldest. Set contract = that seat's N, trump = that seat's suit index, base_stake = contract/10 - 4, leader = declarer. Announce all bids, the declarer, the contract and the trump.
5. **poll** (all players): [when trick = 2] Set each player's flek_answer. An invalid answer counts as NO.
6. **update** (table): [when trick = 2] If at least one defender has flek_answer = FLEK, multiplier = multiplier x 2. If, in addition, the declarer's flek_answer = RE, multiplier = multiplier x 2 again. Announce all answers and the multiplier.
7. **ask** (the seat equal to leader): The named card is recorded.
8. **update** (table): If the named card is not in the leader's hand, use the lowest code in that hand instead. Remove the card from the hand. Append it to trick_cards and append leader to trick_seats. Set led_suit = floor(card/3), best_key = (card mod 3) + (10 if floor(card/3) = trump) + 5, best_seat = leader. Announce the card.
9. **ask** (the seat (leader mod 3)+1): The named card is recorded.
10. **update** (table): The card is legal if its suit = led_suit; or the hand has no led_suit card and its suit = trump; or the hand has neither led_suit cards nor trumps. If it is not held or not legal, use the lowest-code held led_suit card, else the lowest-code held trump, else the lowest-code held card. Remove it from the hand and append it to trick_cards and the seat to trick_seats. key = (card mod 3) + (10 if suit = trump) + (5 if suit = led_suit). If key > best_key, set best_key = key and best_seat = this seat. Announce the card.
11. **ask** (the seat ((leader mod 3)+1) mod 3 + 1): The named card is recorded.
12. **update** (table): Same as the second-card resolution, for this seat.
13. **update** (table): Trick points = sum over trick_cards of (10 if card mod 3 >= 1 else 0), plus 10 if trick = 4. If best_seat = declarer, add them to declarer_points, otherwise to defender_points. Set leader = best_seat, then clear trick_cards and trick_seats. Announce the trick winner, declarer_points and defender_points.
14. **update** (all players): [when trick = 4] stake = base_stake x multiplier x (2 if trump = 0 else 1). If declarer_points >= contract: the declarer's score += 2 x stake and each defender's score -= stake. Otherwise: the declarer's score -= 2 x stake and each defender's score += stake. Announce the result and the scores.
15. **update** (table): trick += 1. If trick > 4: trick = 1, deal += 1, eldest = ((deal-1) mod 3)+1, and every player's bid is reset to '', bid_value to 0 and flek_answer to 'NO'.
16. **check** (table): End the match if deal > 9, otherwise continue with the next round.

## Ending

- ends when: deal > 9
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their score, the sum of the zero-sum deal settlements over 9 deals. The highest score wins, and players tied at the top draw by sharing the win.

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixed 3. The game is built on one declarer against two defenders, and the 12-card deck deals exactly 4 to each of 3 seats.
- No talk step: The rules say there is no discussion phase. Strategy lies in bidding to hand strength, choosing trump, fleking against overbids and card play.
- Bid tie-break computed as bid_value*10 + (3 - ((seat - eldest) mod 3)): This is an arithmetic form of 'first in seat order starting from the eldest'.
- Bids, flek answers and the trick list are reset in the advance step: The source leaves the moment of resetting these working values unstated.

## Simplifications

- Players are offered only legal options (no PASS for the eldest, only legal cards to follow): A seat is never offered what it may not do. The source's fallback rules for invalid or illegal answers are kept in the effects anyway.
- Steps for trick 1, trick 2 and trick 4 are single steps with a 'when trick = k' condition: The step list is flat, and each conditional part is a single step, so no block branching is needed.

## Unsupported (needs engine work)

- none
