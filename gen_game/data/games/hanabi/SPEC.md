# Hanabi Trio

A cooperative card game. Each player sees everyone's cards but their own and plays coloured cards 1 to 5 in order onto three piles, using hints, discards and plays; the team wins together if it scores 13 or more of the 15 possible points.

Players: 2 to 4, best with 3

## Parameters

- `deck_size` = 30
- `num_colours` = 3
- `copies_of_rank_1` = 3
- `copies_of_rank_2` = 2
- `copies_of_rank_3` = 2
- `copies_of_rank_4` = 2
- `copies_of_rank_5` = 1
- `max_rank` = 5
- `hand_size_2_players` = 5
- `hand_size_3_players` = 4
- `hand_size_4_players` = 4
- `deck_count_start_2_players` = 20
- `deck_count_start_3_players` = 18
- `deck_count_start_4_players` = 14
- `pile_start` = 0
- `hint_tokens_start` = 8
- `hint_tokens_max` = 8
- `hint_cost` = 1
- `discard_hint_gain` = 1
- `five_played_hint_gain` = 1
- `fuses_start` = 3
- `fuse_loss_per_failed_play` = 1
- `score_per_successful_play` = 1
- `max_team_score` = 15
- `win_threshold` = 13
- `max_turns` = 40
- `final_turns_left_start` = -1
- `final_turns_extra` = 1
- `team_score_start` = 0
- `turns_played_start` = 0
- `first_active_seat` = 1

## Round

1. **update** (seat {active_seat}): Set legal_options of the active seat to: 'PLAY #id' for each id in its hand_ids; 'DISCARD #id' for each id in its hand_ids; and, if hint_tokens >= 1, 'HINT s v' for each other seat s and each v in {R,G,B,1,2,3,4,5} where at least one face in seat s's hand_faces has colour letter v or rank v. Set every other seat's legal_options to [].
2. **sync** (all players): Each seat receives its permitted view: all hand_ids, other seats' hand_faces, the piles, hint_tokens, fuses, deck_count, discard_pile, action_log, team_score, turns_played, active_seat, and its own legal_options.
3. **ask** (seat {active_seat}): Store the chosen option as this turn's choice.
4. **update** (seat {active_seat}): When the choice is 'HINT s v': hint_tokens -= 1. Append to action_log 'turn {turns_played+1}: seat {active_seat} hints seat s v = ' followed by every id in seat s's hand_ids whose paired face matches v. No card moves.
5. **update** (seat {active_seat}): When the choice is 'PLAY #id': find index i of #id in the active seat's hand_ids, take face = hand_faces[i], and remove index i from both hand_ids and hand_faces. If face rank == (pile of face colour) + 1: set that pile to the rank, team_score += 1, if rank == 5 and hint_tokens < 8 then hint_tokens += 1, and append 'turn t: seat a plays #id = face, success' to action_log. Otherwise: fuses -= 1, append '#id=face' to discard_pile, and append 'turn t: seat a plays #id = face, failure' to action_log.
6. **update** (seat {active_seat}): When the choice is 'DISCARD #id': find index i of #id in the active seat's hand_ids, take face = hand_faces[i], and remove index i from both lists. Append '#id=face' to discard_pile, set hint_tokens = min(8, hint_tokens + 1), and append 'turn t: seat a discards #id = face' to action_log.
7. **update** (seat {active_seat}): When the choice was PLAY or DISCARD and deck_ids is not empty: remove the front entry of deck_ids and of deck_faces together and append them to the end of the active seat's hand_ids and hand_faces. Set deck_count = length of deck_ids. If deck_count is now 0 and final_turns_left == -1, set final_turns_left = num_players + 1. After a HINT nobody draws.
8. **update** (all players): Set every seat's total = team_score. turns_played += 1. If final_turns_left > 0, final_turns_left -= 1. active_seat = active_seat + 1, or 1 after the last seat.
9. **tell** (all players): Announce the last action_log line with the current pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count and team_score.
10. **check** (all players): End the game if fuses == 0 or team_score == 15 or final_turns_left == 0 or turns_played == 40; otherwise continue with the next round.

## Ending

- ends when: fuses == 0 OR team_score == 15 OR final_turns_left == 0 OR turns_played == 40, checked at the end of each turn
- results: all seats win, no seat wins
- decided by: Every seat's total equals team_score = pile_red + pile_green + pile_blue. If team_score >= 13, every seat's total is at least 13 and all seats win together. Otherwise no seat wins. Pile progress counts even when the game ended because fuses reached 0.

## Choices the source did not make

- 2 to 4 players, suggested 3: The designer chose 3, so it is kept. 2 is the smallest table where hints between players happen. 4 is the source maximum: the 30-card deck leaves only 14 cards to draw, and with more seats each player waits longer between turns and each hint matters less.
- Strategy at the table: A thoughtful player reads the action_log to infer what a hint implies, spends scarce hint tokens on playable or critical cards, discards cards already played or with remaining duplicates, and avoids blind plays that burn fuses. A thoughtless player wastes hints or plays unknown cards.
- No talk phase: R18 forbids any message phase. Limited communication is the core of the game, so no talk poll is added even though there are 3 or more players.
- Turn choice is an ask to the active seat only: The rules give one seat one action per turn, so it is a sequential ask, not a poll.
- final_turns_left and active_seat are public: R6 does not list them. Both can be worked out from public information (deck_count, turn order), and players need to know whose turn it is.
- deck_ids is hidden (none): R6 does not list it as public. Its contents follow from the public hand_ids and discard_pile anyway, and it reveals no faces.
- Results are named 'all seats win' and 'no seat wins': The rules say the team wins or loses together, decided by team_score >= 13.
- The failure log text is 'turn t: seat a plays #id = face, failure': R13 says only that the failure and face are recorded; the wording mirrors the success line in R12.

## Simplifications

- A face's colour and rank are read from its two-character text (colour letter, rank digit): The engine compares numbers and text; this lets rank == pile + 1 and the hint matching be computed arithmetically, with no change to the rules.
- PLAY, DISCARD and HINT are three separate update steps, each guarded by a 'when' on the choice: The step list is flat. Each branch is a single conditional update, which the engine supports.

## Unsupported (needs engine work)

- none
