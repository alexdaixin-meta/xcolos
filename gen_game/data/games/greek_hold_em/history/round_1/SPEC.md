# Greek Hold 'em Lite

A simplified simultaneous-betting poker for 3 to 5 players: ante, flop bet, call or fold, river bet, call or fold, then an arithmetic showdown, over 15 hands; most chips wins.

Players: 3 to 5, best with 4

## Parameters

- `starting_chips` = 40
- `deck_size` = 32
- `card_value_min` = 1
- `card_value_max` = 8
- `copies_per_value` = 4
- `hands` = 15
- `ante` = 1
- `hole_cards` = 2
- `board_cards` = 5
- `flop_cards` = 3
- `min_bet` = 0
- `max_bet` = 4
- `match_weight` = 20
- `max_matches` = 3
- `pair_bonus` = 30
- `elimination_chips` = 0

## Round

1. **update** (all players): hand_no += 1. For each player with out = false: chips -= 1, pot += 1, in_hand = true. For each player with out = true: in_hand = false. Every player gets bet = 0, strength = 0, hole = [] and shown_hole = []. Set board = [] and board_shown = []. A player left with 0 chips after the ante is all-in and stays in the hand.
2. **update** (all players): Rebuild deck as the 32 cards (values 1-8, four of each). For each player with in_hand = true, draw 2 cards at random: remove each from deck and append it to that player's hole. Then draw 5 cards at random from deck and append them in order to board.
3. **sync** (all players): Each player privately sees their own hole cards.
4. **update** (all players): Flop: board_shown = the first 3 cards of board. Announce board_shown, pot and every player's chips to everyone.
5. **poll** (every player with in_hand = true): Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together.
6. **poll** (every player with in_hand = true and bet < high_bet): call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid, and the player stays in. fold: in_hand = false, and chips already put in stay in pot. Players with bet = high_bet stay in automatically.
7. **update** (all players): in_hand_count = number of players with in_hand = true. If in_hand_count = 1: that player's chips += pot and pot = 0, and the hand skips to elimination.
8. **update** (all players): When in_hand_count >= 2: board_shown = all 5 cards of board, every player's bet = 0, and high_bet = 0. Announce board_shown and pot.
9. **poll** (every player with in_hand = true, when in_hand_count >= 2): Each answering player gets bet = answer, chips -= answer and pot += answer. high_bet = the largest bet among players with in_hand = true. All bets are revealed together.
10. **poll** (every player with in_hand = true and bet < high_bet, when in_hand_count >= 2): call: paid = min(high_bet - bet, chips); chips -= paid, pot += paid, bet += paid. fold: in_hand = false, and chips stay in pot.
11. **update** (all players): When in_hand_count >= 2 before this step: recount in_hand_count. If it is 1, that player's chips += pot and pot = 0. Otherwise it is a showdown. For each player with in_hand = true: shown_hole = hole; matches = number of board cards whose value equals either hole value; pair = 1 if hole[0] = hole[1], else 0; strength = 20*min(matches,3) + 30*pair + hole[0] + hole[1]. Then best_strength = max strength among in-hand players and winners_count = number of in-hand players with strength = best_strength. Each such player's chips += floor(pot / winners_count), and pot = pot mod winners_count. Announce the shown hole cards, the strengths and the winners.
12. **update** (all players): Elimination: every player with out = false and chips = 0 gets out = true and in_hand = false. alive_count = number of players with out = false. Announce each player's chips and who is eliminated.
13. **check** (all players): End the game if hand_no >= 15 or alive_count <= 1; otherwise run the next hand.

## Ending

- ends when: hand_no >= 15 or alive_count <= 1
- ranked by: `you.chips` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their chip count. The player with the most chips wins, and players tied for the most chips share the win (a draw). If only one player has chips left before hand 15, that player wins, because every other player has 0.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggests 4, so it is kept. The minimum is 3 because with 2 players simultaneous betting is a pure guess against one rival, and 3 or more make folding and calling a reading of several opponents. The maximum is 5 because 10 hole cards and 5 board cards already use half the 32-card deck, and more seats dilute each bet's effect on the pot.
- No pre-bet talk step: The rules contain no table talk. Adding it would add a mechanic, and the bluffing already lives in the simultaneous bet sizes.
- Strategy at the table: A thoughtful player bets according to their likely matches against the 3 shown board cards and pair potential. They read big bets as strength, fold weak hands when H is high, and use the carried-over pot and opponents' short stacks (who are forced all-in) to decide when calling is worth it.
- The call cost is computed against the player's current-round bet: The rules say a caller pays 'the difference so their bet equals H'. Bets reset between the flop and river rounds, since each is a separate betting round.
- A player at 0 chips bets 0 and calls for 0: The rules cap bets at the stack and let an all-in caller stay in, so a 0-chip player stays in at no cost.
- No side pots: The rules give the whole pot to the highest strength, including an all-in player, so no side pots are created.

## Simplifications

- 'Skip to step 10' is done with a 'when in_hand_count >= 2' condition on each turn, river and showdown step instead of a jump: The step list is flat. Per-step arithmetic conditions give the same result.
- Revealing hole cards at showdown is done by copying hole into a public shown_hole list: Hole cards are owner-only, so a public copy is how the engine reveals them to everyone.

## Unsupported (needs engine work)

- none
