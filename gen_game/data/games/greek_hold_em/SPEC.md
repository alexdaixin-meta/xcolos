# Greek Hold 'em Mini II

Three players play 36 hands of a tiny one-bet poker with an 18-card suitless deck; the highest net chip total after hand 36 wins.

Players: 3 to 3, best with 3

## Parameters

- `num_players` = 3
- `ranks` = 6
- `copies_per_rank` = 3
- `deck_size` = 18
- `hands` = 36
- `hole_cards` = 2
- `board_cards` = 4
- `board_face_up_before_betting` = 3
- `ante` = 1
- `starting_pot` = 3
- `bet_small` = 2
- `bet_large` = 4
- `pair_bonus` = 6
- `match_bonus` = 4
- `max_matches` = 3
- `starting_total` = 0

## Round

1. **update** (all players): Increment hand by 1. Set first_actor = ((hand-1) mod 3)+1, second_actor = (first_actor mod 3)+1, and third_actor = (second_actor mod 3)+1. Return all cards to deck, so it again holds the 18 cards. For every player: clear hole and revealed_hole, set hand_score and revealed_score to 0, set action to empty, set folded to false, and set paid and won to 0. Clear board_up and board_hidden. Set bet_amount to 0.
2. **update** (all players): Deal: draw 2 random cards from deck into each player's hole. Draw 3 random cards from deck into board_up and 1 into board_hidden.
3. **update** (all players): Ante: each player's paid += 1, so pot = 3.
4. **sync** (all players): Each player sees their own hole, the 3 cards of board_up, the pot, the hand number and who acts first, second and third.
5. **ask** (the first actor (seat first_actor)): On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. The choice is announced to all.
6. **ask** (the second actor (seat second_actor)): On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true. The choice is announced to all.
7. **ask** (the third actor (seat third_actor)): Same effects as the second actor's step. The choice is announced to all.
8. **poll** (every player whose action = CHECK, only when bet_amount > 0 (these players checked before the bet)): Answers are collected simultaneously, then revealed. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true.
9. **update** (all players): Final board: move the card in board_hidden into board_up, so board_up holds 4 cards.
10. **update** (all players): For each player with hole ranks a and b: matches = the number of cards in board_up whose rank equals a or b. hand_score = a + b + (6 if a = b else 0) + 4 * min(3, matches).
11. **update** (all players): Set in_count = the number of players with folded = false. If in_count = 1, the unfolded player gets won = pot. If in_count >= 2: for each unfolded player, revealed_hole = hole and revealed_score = hand_score; best_score = the maximum hand_score among unfolded players; winner_count = the number of unfolded players with hand_score = best_score; each such player gets won = pot / winner_count. Folded players' hole cards are never revealed.
12. **update** (all players): Totals: each player's total += won - paid. All three totals, the showdown result and the pot split are announced.
13. **check** (all players): If hand >= 36, end the game. Otherwise play the next hand.

## Ending

- ends when: hand >= 36
- ranked by: `you.total` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their net chip total after 36 hands. The highest total wins, and players tied at the top share the win (the source calls this a draw).

## Choices the source did not make

- 3 players (min = max = suggested = 3): The designer fixes the game at three seats. The actor rotation, the response step and the split pots all assume exactly three players. With three, bluffing works because a bet must get past two opponents, one of whom may hold the third copy of a rank.
- No pre-choice talk step: The source has no table talk. The information in play is the actions themselves (check, bet size, call or fold), so adding talk would add a mechanic.
- Responders are identified by action = CHECK while bet_amount > 0: Anyone still showing CHECK once a bet exists must have checked before the bet. Since only one bet is possible, this matches 'each player who checked before the bet'.
- Score computed for everyone, but published only at a showdown with 2 or more players: This keeps the arithmetic uniform while honoring the rule that folded hands and uncontested winners' hands are never revealed.
- Strategy at this table: A thoughtful player weighs the visible board against their hole cards, bets 4 with strong pairs or matches, uses bet size and position to bluff, and reads opponents' checks and calls over 36 hands. A thoughtless player calls or bets blindly.

## Simplifications

- Ante, bets and calls are tracked in `paid`, and the net change is applied to `total` at the end of the hand: This is arithmetically the same as paying at once, and it keeps fractional split pots exact.

## Unsupported (needs engine work)

- none
