# Trischettn Duel

A two-player, no-trump trick-taking duel with a 24-card deck. It runs three deals of 12 tricks, with talon draws, declarations of sets, and scoring in thirds of a point.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 24
- `suits` = 4
- `ranks_per_suit` = 6
- `hand_size` = 6
- `talon_size` = 12
- `tricks_per_deal` = 12
- `deals` = 3
- `total_tricks` = 36
- `talon_draw_tricks` = 6
- `ace_value` = 3
- `ten_value` = 1
- `nine_value` = 1
- `king_value` = 1
- `ober_value` = 1
- `unter_value` = 1
- `last_trick_bonus` = 3
- `thirds_per_deal` = 35
- `three_of_rank_points` = 9
- `four_of_rank_points` = 12
- `napoli_points` = 9
- `napoli_cards` = 3
- `rank_strength_ten` = 6
- `rank_strength_nine` = 5
- `rank_strength_ace` = 4
- `rank_strength_king` = 3
- `rank_strength_ober` = 2
- `rank_strength_unter` = 1
- `deal1_first_leader_seat` = 1
- `deal2_first_leader_seat` = 2
- `deal3_tie_first_leader_seat` = 2

## Round

1. **update** (table): Only when trick_in_deal == 0 (start of a deal):
- deal_no += 1.
- deck = all 24 cards (Ten, Nine, Ace, King, Ober and Unter of Hearts, Bells, Leaves and Acorns).
- Each hand = []. Then 6 times for each seat, move a random card from deck to that seat's hand.
- talon = the remaining 12 cards. Move one random talon card to talon_up. talon_count = 12.
- Each deal_points = 0 and each declared_this_deal = false.
- played_this_deal = [], declared_cards_shown = [], last_trick_winner = 0.
- leader = 1 if deal_no == 1. leader = 2 if deal_no == 2. If deal_no == 3: leader = 1 if seat 1 match_total < seat 2 match_total, otherwise 2.
- Announce: 'Deal {deal_no} begins; the face-up talon card is {talon_up}; seat {leader} leads.'
2. **sync** (all players): Each player sees their own hand, talon_up, talon_count, every deal_points and match_total, played_this_deal and declared_cards_shown.
3. **ask** (the leader (seat given by leader)): Asked only when all of these hold: trick_in_deal >= 1, last_trick_winner == leader, the leader's declared_this_deal is false, and the leader's declaration value is > 0.

The declaration value is the sum of these, over the hand:
- For each rank of Ten, Nine and Ace: 12 if the hand holds 4 of that rank, 9 if it holds exactly 3, otherwise 0.
- 9 for each suit whose Ten, Nine and Ace are all in hand.
4. **update** (table): When the leader answered declare:
- The leader's deal_points += declaration value.
- The leader's declared_this_deal = true.
- Append every card forming a qualifying set to declared_cards_shown.
- Announce: 'Seat {leader} declares {value} thirds, showing {cards}.'
5. **ask** (the leader (seat given by leader)): led_card = chosen card. Remove it from the leader's hand and append it to played_this_deal. Announce: 'Seat {leader} leads {led_card}.'
6. **ask** (the follower (the seat that is not leader)): follow_card = chosen card. Remove it from the follower's hand and append it to played_this_deal. Announce: 'Seat {follower} plays {follow_card}.'
7. **update** (table): Decide and score the trick:
- trick_winner = follower if follow_card has led_card's suit and a higher rank strength (Ten 6, Nine 5, Ace 4, King 3, Ober 2, Unter 1). Otherwise trick_winner = leader.
- trick_in_deal += 1 and tricks_played += 1.
- trick_winner's deal_points += value(led_card) + value(follow_card), where Ace = 3 and every other card = 1.
- If trick_in_deal == 12, trick_winner's deal_points += 3.
- last_trick_winner = trick_winner.
- Announce: 'Seat {trick_winner} wins the trick.'
8. **update** (table): Only when talon_count > 0:
- Append talon_up to trick_winner's hand. talon_count -= 1.
- Move one random talon card to the loser's hand and set the loser's drawn_hidden_card to it, seen only by the loser. talon_count -= 1.
- If talon is not empty, move one random talon card to talon_up. Otherwise talon_up = ''.
- Announce: 'Seat {trick_winner} takes the face-up card; the new face-up card is {talon_up}.'
9. **update** (table): leader = trick_winner.
10. **update** (table): Only when trick_in_deal == 12:
- Each player's match_total += deal_points.
- trick_in_deal = 0.
- Announce: 'Deal {deal_no} over. Seat 1 has {match_total}, seat 2 has {match_total}.'
11. **check** (table): End the game if tricks_played == 36, otherwise continue to the next round.

## Ending

- ends when: tricks_played == 36
- ranked by: `you.match_total` (the highest wins; players level at the top share the win)
- decided by: After three deals, the player with the higher match total in thirds wins; equal totals share the win, which is a draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed the game as a duel. The trick and draw rules (winner takes the face-up card, loser the hidden one) only work with two.
- No talk step: This is a zero-sum duel with no source rule for talk, so messages would add words without anything to disagree about or agree on.
- Talon draws pick a random remaining talon card: Drawing at random from a hidden shuffled list is equivalent to taking the next card of a fixed shuffled order.
- Declaring is optional when eligible: The source says the leader 'may' declare, so pass is offered.
- Rank strengths Ten 6 down to Unter 1: These are numeric codes so the trick winner can be computed by comparison.

## Simplifications

- Deal-start actions run as conditional single steps at the top of the round (when trick_in_deal == 0): The step list is flat. Each deal-start operation carries its own arithmetic condition, so no block of steps has to be chosen instead of another.
- The declaration value is computed arithmetically by counting ranks and suits in the hand: Outcomes must be calculated, and the set rules reduce to counts.

## Unsupported (needs engine work)

- none
