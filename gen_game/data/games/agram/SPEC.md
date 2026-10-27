# Agram Match

35-card trick game over 6 hands of 6 tricks where only trick 6 of each hand scores 1 point and most points wins.

Players: 3 to 4, best with 4

## Parameters

- `num_hands` = 6
- `tricks_per_hand` = 6
- `cards_per_player` = 6
- `deal_batch_size` = 3
- `deck_size` = 35
- `points_per_hand_win` = 1
- `stub_3p` = 17
- `stub_4p` = 11

## Round

1. **initialize** (all players): if hand_number==0 then set each match_points to 0 and build deck of 35 cards
2. **update** (all players): hand_number+=1; if hand_number==1 keep random dealer_seat else dealer_seat rotates one clockwise; shuffle deck; deal 6 cards to each hand in two batches of 3 clockwise from left of dealer; set stub to remainder; set trick_number to 0; clear lead_suit and trick_plays
3. **sync** (all players): send each seat private hand: Your hand list plus dealer_seat plus hand_number of 6 plus all match_points
4. **ask** (trick leader): leader plays one card from hand to trick_plays; set lead_suit to its suit; trick_number+=1 for first play of trick
5. **ask** (each player in turn): each follower clockwise plays one card from hand to trick_plays following lead_suit when possible
6. **update** (all players): set trick_winner_seat to seat with highest rank of lead_suit among trick_plays; remove trick cards; shrink each hand by one; clear lead_suit for next trick after announcement
7. **tell** (all players): announce trick_winner_seat and played cards with seats and that winner leads next trick
8. **repeat** (all players): repeat leader play and follower play and resolve and announce until trick_number==6
9. **update** (all players): if trick_number==6 then trick 6 winner trick_winner_seat gains 1 match_points; others gain 0
10. **tell** (all players): announce hand winner and standings Points seat 1 to num_players with match_points
11. **check** (all players): continue redealing with next dealer until hand_number==6 else end match

## Ending

- ends when: hand_number==6
- ranked by: `you.match_points` (the highest wins; players level at the top share the win)
- decided by: the seat with the most match_points wins the match; seats tied for the most share the win; announce Final points for seats 1 to num_players with points, then the winner (the winning seat, or seats when they share the win)

## Choices the source did not make

- 3 to 4 players with suggested 4: kept designer choice: 3 is smallest where following and void discards matter, 4 maximizes stub pressure and trick contention while each choice still matters
- no talk poll before choices: source says no discussion: hands stay hidden so follow-void signals must be read and one winner per hand makes cheap talk noise
- sequential ask for tricks, not poll: source order matters: leader sets lead_suit then each follower in clockwise turn sees prior plays
- parameters stub_3p 17 and stub_4p 11: 35 minus 3x6=17 and 35 minus 4x6=11 undealt cards per source

## Simplifications

- enumerated deck strings like HA and S10 for 35 distinct cards: engine needs explicit list values to shuffle, draw and compare rank
- inner trick loop via repeat step plus outer hand loop via round check until hand_number==6: engine step list is flat with repeat and check for counted repetition to 6 hands of 6 tricks
- restricted follow enforced by offer filtering rather than illegal-play penalty: engine offers never include what a seat may not do, so off-suit when holding led suit is never offered

## Unsupported (needs engine work)

- none
