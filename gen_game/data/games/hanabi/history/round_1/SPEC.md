# Hanabi: Three Fireworks

A cooperative card game for 2 to 4 players. Each player sees everyone's cards except their own, and the team uses hints, discards and plays to build three colour piles from 1 to 5 and reach a target score before the fuses run out.

Players: 2 to 4, best with 3

## Parameters

- `deck_size` = 30
- `colours` = 3
- `copies_rank_1` = 3
- `copies_rank_2` = 2
- `copies_rank_3` = 2
- `copies_rank_4` = 2
- `copies_rank_5` = 1
- `hand_size_2_players` = 5
- `hand_size_3_or_4_players` = 4
- `deck_after_deal_2_players` = 20
- `deck_after_deal_3_players` = 18
- `deck_after_deal_4_players` = 14
- `hint_tokens_start` = 8
- `hint_tokens_max` = 8
- `hint_cost` = 1
- `discard_token_gain` = 1
- `completed_pile_token_gain` = 1
- `fuses_start` = 3
- `failed_play_fuse_loss` = 1
- `pile_start` = 0
- `pile_max` = 5
- `target_2_or_3_players` = 10
- `target_4_players` = 9
- `max_team_score` = 15
- `max_turns` = 40
- `turns_played_start` = 0
- `final_round_counter_start` = -1
- `first_seat` = 1

## Round

1. **tell** (all players): Announce pile_red, pile_green, pile_blue, hint_tokens, fuses, deck_count, turns_played, the full discard_pile with faces, and the full hint_log.
2. **update** (the seat equal to active_seat): Build legal_options for the active seat. Add PLAY <ID> and DISCARD <ID> for every ID in their own hand_ids. If hint_tokens >= 1, also add HINT <seat> <X> for every other seat and every X in {R, G, B, 1, 2, 3, 4, 5} that matches at least one face in that seat's hand_faces.
3. **sync** (the seat equal to active_seat): Privately send the active seat the hand_faces and hand_ids of every other seat, their own hand_ids (never their own faces), and their legal_options.
4. **ask** (the seat equal to active_seat): Set last_move to the answer. If the answer is unreadable or not a legal move (a hint with 0 tokens, a hint to yourself, a hint matching no card, an ID not in your own hand), set last_move to DISCARD <first ID in own hand_ids>.
5. **update** (the seat equal to active_seat): When last_move is HINT <seat s> <X>: hint_tokens -= 1. Append to hint_log the giver, s, X, the IDs in s's hand_ids whose face matches X, and every other ID currently in s's hand_ids as not matching. Announce this to everyone.
6. **update** (the seat equal to active_seat): When last_move is DISCARD <ID>: remove the ID from hand_ids and its face from hand_faces. Append ID=face to discard_pile. hint_tokens = min(8, hint_tokens + 1). Announce the face to everyone.
7. **update** (the seat equal to active_seat): When last_move is PLAY <ID>: remove the ID and its face from the hand and announce the face. If the rank equals the matching pile (pile_red, pile_green or pile_blue) + 1, set that pile to the rank, and if the rank is 5, hint_tokens = min(8, hint_tokens + 1). Otherwise append ID=face to discard_pile and fuses -= 1.
8. **update** (all players): Set counter_set_this_turn to false. If final_round_counter > 0, final_round_counter -= 1. This only happens on turns after the last-card turn, because the counter is still -1 until the draw step below sets it.
9. **update** (the seat equal to active_seat): When last_move is DISCARD or PLAY and deck_count > 0: move the first entry of deck_ids and deck_faces to the end of the active seat's hand_ids and hand_faces, deck_count -= 1, and announce the new ID to everyone. If deck_count is now 0, set final_round_counter to num_players and counter_set_this_turn to true.
10. **update** (all players): turns_played += 1. team_score = 0 if fuses = 0, otherwise pile_red + pile_green + pile_blue. Set every player's total to team_score.
11. **check** (all players): End the game if fuses = 0, or team_score = 15, or final_round_counter = 0, or turns_played = 40. Otherwise continue.
12. **update** (all players): active_seat = (active_seat mod num_players) + 1.

## Ending

- ends when: fuses == 0 OR team_score == 15 OR final_round_counter == 0 OR turns_played == 40
- results: all players win, no winner
- decided by: If team_score >= target (10 with 2 or 3 players, 9 with 4), the result is 'all players win'. Otherwise it is 'no winner' (a shared draw). No player can win alone.

## Choices the source did not make

- 2 to 4 players, suggested 3: The designer suggested 3, so it is kept. The minimum is 2 because hidden-hand cooperation needs at least one teammate who can see your cards. The maximum is 4 because larger tables shrink hands and the deck, and each player's turns grow rare. The key skill is giving hints whose meaning a teammate can read from the timing and from which IDs they mark, while saving tokens and avoiding risky plays.
- No talk phase: The rules forbid all communication except hints, so no talk poll is added.
- Moves offered as a choice list (legal_options) instead of free text: This keeps answers readable and ensures a seat is never offered an illegal move. The invalid-answer fallback, DISCARD of the oldest ID, is kept for unreadable replies.
- Dealing goes one card at a time around the table in seat order: The source says 'deal from the top in seat order' without saying whether cards go one at a time or a full hand at once. Since the deck is shuffled, the outcome is the same in distribution.
- A hand is stored as two parallel lists, hand_ids (public) and hand_faces (others): IDs are announced to everyone, while faces must be hidden from the owner only.
- Final-round timing uses the flag counter_set_this_turn and a decrement step placed before the draw step: This gives each player, from the next seat through the player who drew the last card, exactly one more turn.
- Game results are named 'all players win' and 'no winner': The source describes a shared win or a shared loss recorded as no winner.

## Simplifications

- hand_faces is visible to every non-owner at all times, not only to the active player during their private view: The engine's 'others' visibility is per attribute. Teammates seeing the faces off-turn changes no decision, because only the active player acts and there is no talk.
- The deck is an ordered hidden list and drawing takes its first entry: This matches 'take the top card'. Drawing at random from a shuffled deck would be equivalent.

## Unsupported (needs engine work)

- none
