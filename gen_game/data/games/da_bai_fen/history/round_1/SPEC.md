# Da Bai Fen Lite

A four-player partnership trick-taking game (NS v EW) over 4 hands of 7 tricks with a 30-card deck and jokers. Teams win match points by how many card points the defenders capture.

Players: 4 to 4, best with 4

## Parameters

- `seats` = 4
- `deck_size` = 30
- `suits` = 4
- `cards_per_suit` = 7
- `jokers` = 2
- `rank_5` = 1
- `rank_8` = 2
- `rank_10` = 3
- `rank_j` = 4
- `rank_q` = 5
- `rank_k` = 6
- `rank_a` = 7
- `points_k` = 10
- `points_10` = 10
- `points_5` = 5
- `points_other` = 0
- `total_points` = 100
- `hands` = 4
- `rounds_per_hand` = 8
- `total_rounds` = 32
- `tricks_per_hand` = 7
- `cards_dealt_each` = 7
- `kitty_size` = 2
- `trump_count` = 9
- `big_joker_strength` = 40
- `small_joker_strength` = 39
- `trump_base` = 20
- `led_suit_base` = 10
- `off_suit_base` = 0
- `band_declarer_3_max` = 15
- `band_declarer_2_min` = 20
- `band_declarer_2_max` = 35
- `band_defender_1_min` = 40
- `band_defender_1_max` = 55
- `band_defender_2_min` = 60
- `band_defender_2_max` = 75
- `band_defender_3_min` = 80
- `award_3` = 3
- `award_2` = 2
- `award_1` = 1
- `rank_weight_match_points` = 1000

## Round

1. **update** (all players): when round_in_hand == 1: deck is reset to all 30 cards; every hand, kitty and trump_suit are cleared; ns_hand_points = ew_hand_points = 0; declarer = hand_number; declaring_team = NS if declarer is odd, else EW; leader = declarer
2. **update** (all players): when round_in_hand == 1: draw 7 random cards from deck into each player's hand (removed from deck), then move the 2 remaining cards of deck into kitty
3. **sync** (all players): when round_in_hand == 1: each player sees their own hand only
4. **ask** (the declarer (seat = declarer)): when round_in_hand == 1: trump_suit = the answer; announce to all 'Trump suit is {trump_suit}; seat {declarer} leads.'
5. **update** (all players): when round_in_hand >= 2: every played_card = '' and card_strength = 0; led_suit = ''
6. **ask** (each player in turn, starting from seat = leader and going anticlockwise (leader, leader+1, leader+2, leader+3, wrapping 4 to 1)): when round_in_hand >= 2: the card moves from hand to played_card, face up to all; if the player is the leader, led_suit = 'Trump' when the card is a joker or of trump_suit, else the card's suit; card_strength = 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump card of led_suit, otherwise rank (5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7) (judged: "The card this player chose is legal: either the player is the leader, or the card is of the led suit (jokers and trump-suit cards counting as Trump), or the player held no card of the led suit.")
7. **update** (all players): when round_in_hand >= 2: trick_winner = the seat with the highest card_strength; trick_points = sum over the 4 played cards of (10 for K, 10 for 10, 5 for 5, 0 otherwise); if trick_winner's team is NS then ns_hand_points += trick_points, else ew_hand_points += trick_points; leader = trick_winner; announce 'Seat {trick_winner} wins the trick for {trick_points} points.'
8. **update** (all players): when round_in_hand == 8: reveal kitty to all; add the kitty's point values to the hand points of trick_winner's team
9. **update** (all players): when round_in_hand == 8: defender_points = ew_hand_points if declaring_team is NS, else ns_hand_points; if defender_points <= 15, the declaring team's match points += 3; if 20..35, the declaring team += 2; if 40..55, the defending team += 1; if 60..75, the defending team += 2; if >= 80, the defending team += 3; ns_card_points += ns_hand_points; ew_card_points += ew_hand_points; copy the team match points and card points onto each player's match_points and card_points; announce the hand result
10. **update** (all players): if round_in_hand == 8 then hand_number += 1 and round_in_hand = 1, else round_in_hand += 1
11. **check** (all players): end the game when hand_number > 4; otherwise continue

## Ending

- ends when: hand_number > 4 (after 32 rounds)
- ranked by: `you.match_points * 1000 + you.card_points` (the highest wins; players level at the top share the win)
- decided by: The team with more match points wins, and both its partners win. If match points are equal, the team with the higher card-point total wins. If both are equal, all four players share the top value, which is a draw.

## Choices the source did not make

- 4 players (min = max = suggested = 4): The designer fixed two partnerships of two. Fewer seats break the teams, and more seats do not fit the 30-card deal of 7 each plus a 2-card kitty.
- No talk step: The rules forbid talk; signalling through card play is the skill. A thoughtful player tracks played trumps and points, smears points onto a partner's winning trick, and holds trumps back to capture kings and tens.
- Team scores are mirrored onto each player's match_points and card_points: The ranking expression works per player, so both partners carry the team's totals.
- Ranking expression match_points * 1000 + card_points: Card points can total at most 400, so match points always come first and card points break ties. A full tie makes all four seats share the win, which is the draw.
- Card codes such as 'S-K', 'H-10', 'BJ', 'SJ': The rules do not say how cards are labelled; codes let suit, rank and points be read arithmetically.

## Simplifications

- The 32 rounds run as one repeated step list, with `when` conditions on round_in_hand choosing the deal steps (round 1) or the trick steps (rounds 2 to 8): The step list is flat; a condition on each single step gives the same order.
- Legality of following suit is enforced by offering only legal cards, with a judged check as a backstop: The source rejects illegal plays and asks again; offering only legal cards has the same effect.
- A draw is shown as all four seats sharing the win: The engine has no separate draw outcome.

## Unsupported (needs engine work)

- none
