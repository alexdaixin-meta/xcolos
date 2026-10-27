# Knaves' Wager

A 3-player trick-taking game over 6 hands of 6 tricks: bid your trick count secretly, take tricks for 2 points each, avoid winning Jacks, and score a 4-point bonus for an exact bid.

Players: 3 to 3, best with 3

## Parameters

- `player_count` = 3
- `deck_size` = 20
- `suits` = 4
- `ranks_per_suit` = 5
- `hands` = 6
- `tricks_per_hand` = 6
- `total_rounds` = 36
- `cards_dealt_per_player` = 6
- `trump_card_position` = 19
- `hidden_card_position` = 20
- `bid_min` = 0
- `bid_max` = 6
- `trick_points` = 2
- `jack_of_spades_penalty` = 1
- `jack_of_clubs_penalty` = 2
- `jack_of_diamonds_penalty` = 3
- `jack_of_hearts_penalty` = 4
- `exact_bid_bonus` = 4
- `deals_per_player` = 2
- `first_dealer_seat` = 1
- `rank_value_A` = 14
- `rank_value_K` = 13
- `rank_value_Q` = 12
- `rank_value_J` = 11
- `rank_value_10` = 10

## Round

1. **update** (all players): When trick_in_hand = 1: gather all 20 cards into deck and empty every hand. Deal 6 cards to each player by drawing at random from deck into hand. Draw one more card at random into turned_card, and set trump_suit to its suit. Move the last card into hidden_card. Set leader = eldest. Set every player's tricks_taken, bid and hand_score to 0.
2. **sync** (all players): Each player is shown their own hand and the public state.
3. **tell** (all players): When trick_in_hand = 1: announce hand_number, dealer, eldest, turned_card and trump_suit.
4. **poll** (all players): When trick_in_hand = 1: each player's answer is stored in bid, and no bid is seen until all three are in.
5. **tell** (all players): When trick_in_hand = 1: reveal all three bids to everyone.
6. **ask** (the seat equal to leader): Remove the card from the leader's hand and set the leader's played_card to it. Set led_suit to the card's suit. The play is shown to everyone.
7. **ask** (the seat to the leader's left (leader mod 3 + 1)): Remove the card from that player's hand and set their played_card to it. The play is shown to everyone.
8. **ask** (the third seat ((leader + 1) mod 3 + 1)): Remove the card from that player's hand and set their played_card to it. The play is shown to everyone.
9. **update** (all players): Rank values are A=14, K=13, Q=12, J=11, 10=10. If any played_card has suit trump_suit, trick_winner is the seat whose trump has the highest rank value; otherwise it is the seat whose led_suit card has the highest rank value. The winner gets tricks_taken += 1 and hand_score += 2, then hand_score -= 1 for JS, 2 for JC, 3 for JD and 4 for JH among the three played cards. Set leader = trick_winner.
10. **tell** (all players): Announce the three played cards, trick_winner, and every player's tricks_taken and hand_score.
11. **update** (all players): When trick_in_hand = 6: each player with tricks_taken = bid gets hand_score += 4. Then each player's total += hand_score. Announce each hand_score and total. Then set every hand_score to 0, set dealer = dealer mod 3 + 1, set eldest = dealer mod 3 + 1, and set hand_number += 1.
12. **update** (all players): Set round_number += 1. Set trick_in_hand = trick_in_hand mod 6 + 1. Clear every played_card and led_suit.
13. **check** (all players): If round_number > 36, the game ends; otherwise the round repeats.

## Ending

- ends when: round_number > 36
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total after 6 hands (36 tricks). The highest total wins; if two or three players tie for the highest total, they share the result, which is the source's draw.

## Choices the source did not make

- Exactly 3 players (min, max and suggested 3): The designer fixed 3. The 20-card deck is built for it: 3 x 6 dealt cards plus the turned trump card and the hidden card make 20, so no other count works without changing the deck.
- No talk phase: The source has no table talk, and adding one would add a mechanic. The strategy is already in the exact bid (balancing taking tricks against hitting the bid), in dumping or avoiding Jacks, and in reading the revealed bids.
- Cards are written as rank plus suit letter (AS, 10H, ...), with rank values A=14, K=13, Q=12, J=11, 10=10: This lets the trick winner be worked out by arithmetic comparison.
- Seat to the left means the next seat number, with seat 1 after seat 3: The source says 'left' but gives no numbering, and a direction is needed for dealer rotation, eldest and play order.
- The first-round-of-hand steps (deal, bid, reveal) and the end-of-hand step carry a when condition on trick_in_hand: This keeps the step list flat while running those steps only on tricks 1 and 6 of each hand.

## Simplifications

- A tie for the highest total is a shared win rather than a separately named draw: The engine has no separate draw outcome; players level at the top share the result, which matches the source's draw.
- Dealing is done by random draws from the deck list rather than by a physical shuffle and dealing in order: Drawing at random is equivalent to shuffling, so the 19th and 20th cards are simply the two left after the 18 dealt cards.
- The order of play within a trick is three ask steps addressed relative to leader: The engine has no seat-order rotation, so the leader, the next seat and the third seat are each named by arithmetic on leader.

## Unsupported (needs engine work)

- none
