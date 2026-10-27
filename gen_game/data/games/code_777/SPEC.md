# Code 777: Ask and Guess

Each player sees every rack but their own. Players ask engine-answered counting questions and guess their own three hidden tiles; the first to 3 points ends the game.

Players: 3 to 4, best with 3

## Parameters

- `tiles_total` = 28
- `count_of_1` = 1
- `count_of_2` = 2
- `count_of_3` = 3
- `count_of_4` = 4
- `count_of_5` = 5
- `count_of_6` = 6
- `count_of_7` = 7
- `rack_size` = 3
- `starting_score` = 0
- `correct_guess_points` = 1
- `wrong_guess_points` = -1
- `pass_points` = 0
- `win_points` = 3
- `rounds_per_player` = 10
- `final_round_3_players` = 30
- `final_round_4_players` = 40
- `k_min` = 1
- `k_max` = 7
- `sum_threshold` = 15
- `pair_min_same` = 2
- `high_min` = 5
- `number_range_min` = 1
- `number_range_max` = 7

## Round

1. **update** (all players): round += 1; active_seat = ((round - 1) mod N) + 1; every guess = '' and guessed = false. Announce the round number and the active seat.
2. **ask** (the seat equal to active_seat): question and respondent are set from the choice.
3. **ask** (the seat equal to active_seat, only when question = NUMBER): k is set.
4. **update** (all players): answer is computed over the racks of every seat except respondent (the active player's rack included). EVEN = count of tiles in {2,4,6}; HIGH = count of tiles in {5,6,7}; NUMBER = count of tiles equal to k; SUM15 = count of those racks whose sum >= 15; PAIR = count of those racks holding at least two tiles of the same number; MISSING = count of the numbers 1..7 that appear on none of those racks. Announce the question, the respondent (and k if used) and the answer to everyone.
5. **poll** (all players): guess is set for each player; guessed = (guess != PASS).
6. **update** (all players): For each player with guessed = true: if sorted(guess) equals sorted(rack), score += 1; otherwise score -= 1. A PASS leaves score unchanged.
7. **update** (all players): For each player with guessed = true: announce their rack to all, append the rack to discard, and set rack = []. If length(deck) < 3 * (number of players with guessed = true), move every tile from discard into deck. Then deal 3 tiles at random from deck to the rack of each player who guessed, removing each from deck.
8. **sync** (all players): Each player is privately shown the current racks of all other players.
9. **check** (all players): End the game if any score >= 3 or round >= final_round; otherwise continue.

## Ending

- ends when: max over players of score >= 3 OR round >= final_round (final_round = 10 * N)
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: The player with the highest score wins. Players tied at the top share it, which is a draw.

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer's suggested size is 3 and the source allows 3 to 4. The minimum is 3 because with 2 players a respondent sees only the asker's rack, so answers reveal it almost directly. The maximum stays at 4, as in the source; more racks per question would make answers too diluted and turns too slow.
- Strategy at the table: A thoughtful player picks questions and respondents whose answers best split the possible racks they could hold, uses the public discard and the tile counts, notes what the questions reveal to opponents, and passes until confident, because a wrong guess costs a point.
- No talk phase: The source explicitly has none; the engine-answered questions are the only shared information.
- Question and respondent combined into one choice, with k asked in a separate step only for NUMBER: It fits the engine's choice-from-a-list answer type while keeping the active player's single decision.
- An unparseable guess is treated as PASS: The source does not cover malformed answers; PASS is the neutral reading.
- When the deck is replenished, the whole discard pile moves into the deck: The source says the discard pile is shuffled in; drawing at random makes an explicit shuffle unnecessary.

## Simplifications

- The guess is free text parsed into three numbers rather than a menu of all 84 multisets: This avoids an oversized option list.
- The two ways the game can end share one ranking (highest score; ties share the win): The source decides the winner the same way for both endings, and the engine treats a shared top as a draw.

## Unsupported (needs engine work)

- none
