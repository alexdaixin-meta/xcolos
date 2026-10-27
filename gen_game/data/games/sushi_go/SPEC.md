# Sushi Draft

A card-drafting game: each round every player secretly keeps one card from the hand they hold and passes the rest left. Sets of sushi score at the end of each of 3 hands, and puddings score at the end of the game.

Players: 3 to 4, best with 4

## Parameters

- `deck_size` = 104
- `count_tempura` = 14
- `count_sashimi` = 14
- `count_dumpling` = 14
- `count_maki_1` = 6
- `count_maki_2` = 12
- `count_maki_3` = 8
- `count_salmon_nigiri` = 10
- `count_squid_nigiri` = 5
- `count_egg_nigiri` = 5
- `count_pudding` = 10
- `count_wasabi` = 6
- `hands_per_game` = 3
- `hand_size_3_players` = 9
- `hand_size_4_players` = 8
- `rounds_3_players` = 27
- `rounds_4_players` = 24
- `maki_icons_1` = 1
- `maki_icons_2` = 2
- `maki_icons_3` = 3
- `egg_value` = 1
- `salmon_value` = 2
- `squid_value` = 3
- `wasabi_multiplier` = 3
- `tempura_set_size` = 2
- `tempura_set_points` = 5
- `sashimi_set_size` = 3
- `sashimi_set_points` = 10
- `dumpling_points_0` = 0
- `dumpling_points_1` = 1
- `dumpling_points_2` = 3
- `dumpling_points_3` = 6
- `dumpling_points_4` = 10
- `dumpling_points_5_plus` = 15
- `maki_first_points` = 6
- `maki_second_points` = 3
- `pudding_most_points` = 6
- `pudding_fewest_points` = -6
- `starting_score` = 0
- `starting_puddings` = 0

## Round

1. **update** (all players): When pick_number == 1: draw picks_per_hand cards at random from deck into each player's hand, removing each card from deck.
2. **sync** (all players): Announce to everyone each player's tableau, puddings and score, and the size of each hand. Show each player their own hand privately.
3. **poll** (all players): When the size of hand > 1: set pick to the chosen card. No one sees another player's pick until all have answered.
4. **update** (all players): When the size of hand == 1: set pick to the single card in hand automatically.
5. **update** (all players): Reveal: remove pick from hand, append it to tableau, and announce every player's pick to all.
6. **update** (all players): Record pick. Tempura: tempura +1. Sashimi: sashimi +1. Dumpling: dumplings +1. Maki-1/2/3: maki +1/+2/+3. Pudding: puddings +1. Wasabi: wasabi_unused +1. Egg/Salmon/Squid Nigiri with base value v of 1, 2 or 3: if wasabi_unused >= 1, then nigiri_points += 3*v and wasabi_unused -= 1; otherwise nigiri_points += v.
7. **update** (all players): Pass: each player's remaining hand moves to the player on their left (seat s gives its hand to seat s+1, and the last seat gives to seat 1).
8. **update** (all players): When pick_number == picks_per_hand, add to score: floor(tempura/2)*5 + floor(sashimi/3)*10 + m*(m+1)/2 where m = min(dumplings,5) + nigiri_points. Maki: let M1 be the highest maki among players with maki >= 1, and k1 the number of players with maki == M1; each of them gains floor(6/k1). If k1 == 1, let M2 be the highest maki >= 1 below M1, and k2 the number of players with maki == M2; each of them gains floor(3/k2). Then set tempura, sashimi, dumplings, maki, wasabi_unused and nigiri_points to 0 and empty tableau. Puddings stay.
9. **update** (all players): When pick_number == picks_per_hand and hand_number == 3, and not all players have equal puddings: players with puddings == max split +6, each gaining floor(6/count). Players with puddings == min (0 counts as fewest) split -6, each gaining -floor(6/count).
10. **update** (all players): Advance: pick_number += 1. If pick_number > picks_per_hand, set pick_number to 1 and hand_number += 1.
11. **check** (all players): End the game if hand_number > 3; otherwise continue with the next round.

## Ending

- ends when: hand_number > 3
- ranked by: `you.score * 100 + you.puddings` (the highest wins; players level at the top share the win)
- decided by: Highest score wins. Among players tied on score, the one with the most puddings wins. Players still tied share the win, which is the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer suggests 4, and hand sizes are defined only for 3 and 4. At 3, passing still creates drafting tension. Above 4 the rules give no hand size.
- No talk phase: The source says there is no talk phase. Drafting is decided by reading the visible tableaus and passed hands.
- Strategy at the table: A thoughtful player tracks what others are collecting and what will come back around, denies key cards to rivals, times wasabi before high nigiri, and weighs the pudding race against points in each hand.
- Tie-break encoded as score*100 + puddings: There are at most 10 puddings, so puddings can never outweigh one point of score. Players still tied share the win, matching the source's draw.
- Dumpling table written as m*(m+1)/2 with m = min(dumplings,5): This gives exactly 0, 1, 3, 6, 10, 15 and is pure arithmetic.

## Simplifications

- The left neighbour is the next seat number, wrapping to seat 1: The engine has no physical seating.
- Passing is done by rotating the hand lists between players in one update: The engine moves cards only through list operations.
- The automatic last pick is done as an update instead of a question: The rules take the single card without a choice.

## Unsupported (needs engine work)

- none
