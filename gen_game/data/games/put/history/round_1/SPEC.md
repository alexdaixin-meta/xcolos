# Put: Show One, Keep Three

A two-player betting card duel over 40 hands. Each player holds 3 hidden cards and 1 face-up card, calls are made to raise the stake, and then each secretly orders 3 of their 4 cards to fight 3 tricks.

Players: 2 to 2, best with 2

## Parameters

- `hands_total` = 40
- `deck_size` = 52
- `cards_dealt_per_player` = 4
- `private_cards_per_player` = 3
- `face_up_cards_per_player` = 1
- `cards_played` = 3
- `tricks_per_hand` = 3
- `tricks_to_win_hand` = 2
- `starting_points` = 0
- `starting_hands_won` = 0
- `stake_pass_pass` = 1
- `stake_put_see` = 2
- `stake_pass_put_see` = 2
- `stake_reput_see` = 4
- `fold_to_put_points` = 1
- `fold_to_reput_points` = 2
- `fold_to_put_after_pass_points` = 1
- `strength_3` = 13
- `strength_2` = 12
- `strength_A` = 11
- `strength_K` = 10
- `strength_Q` = 9
- `strength_J` = 8
- `strength_10` = 7
- `strength_9` = 6
- `strength_8` = 5
- `strength_7` = 4
- `strength_6` = 3
- `strength_5` = 2
- `strength_4` = 1
- `suits` = 4
- `rank_points_weight` = 1000

## Round

1. **update** (all players): Refill deck with all 52 cards. Clear each player's hand and play, set tricks_won = 0 and face_up = 0. Set stake = 0, folded = false, and caller_call, responder_answer and caller_answer to empty.
2. **update** (all players): Deal: for each player, draw 3 cards at random from deck into hand, then draw 1 card at random from deck into face_up. Each drawn card is removed from deck.
3. **tell** (all players): Announce hand_number, who is Caller and who is Responder, and both players' face_up cards.
4. **sync** (all players): Each player sees their own hand and face_up, the opponent's face_up, and both players' points and hands_won.
5. **ask** (the Caller (seat 1 if hand_number is odd, seat 2 if even)): Set caller_call to the answer.
6. **ask** (the Responder (seat 2 if hand_number is odd, seat 1 if even)): Set responder_answer to the answer.
7. **update** (all players): If caller_call = PUT and responder_answer = SEE, set stake = 2. If caller_call = PUT and responder_answer = FOLD, the Caller gets points += 1 and hands_won += 1, and folded = true. If caller_call = PASS and responder_answer = PASS, set stake = 1.
8. **ask** (the Caller, only when responder_answer is RE-PUT or PUT): Set caller_answer to the answer.
9. **update** (all players): If responder_answer = RE-PUT and caller_answer = SEE, set stake = 4. If responder_answer = RE-PUT and caller_answer = FOLD, the Responder gets points += 2 and hands_won += 1, and folded = true. If responder_answer = PUT and caller_answer = SEE, set stake = 2. If responder_answer = PUT and caller_answer = FOLD, the Responder gets points += 1 and hands_won += 1, and folded = true.
10. **poll** (all players, only when folded = false): Set each player's play to the chosen ordered list. Neither player sees the other's choice until both are in.
11. **update** (all players, only when folded = false): For each position i = 1, 2, 3, compare floor(play[i]/10) between the two players. The higher strength gets tricks_won += 1. Equal strength gives the trick to no one.
12. **update** (all players, only when folded = false): A player with tricks_won >= 2 gets points += stake and hands_won += 1. Otherwise nobody scores.
13. **tell** (all players): Announce caller_call, responder_answer, caller_answer, all 8 cards (both hands and face_up cards, including cards left out or never played), both play lists, tricks_won, the hand result, and both players' points and hands_won.
14. **update** (all players): hand_number += 1.
15. **check** (all players): End the game if hand_number > 40. Otherwise run the round again.

## Ending

- ends when: hand_number > 40
- ranked by: `you.points * 1000 + you.hands_won` (the highest wins; players level at the top share the win)
- decided by: After 40 hands the player with more points wins. If points are equal, the player with more hands won wins. If both are equal, the players share the result, which is a draw.

## Choices the source did not make

- Exactly 2 players (suggested 2): The designer fixed the game at 2. The call structure (Caller/Responder alternating by hand) and the head-to-head tricks only work with two seats.
- Card coding as strength*10+suit: Strength is then floor(card/10), which makes trick comparison pure arithmetic while keeping 52 distinct cards.
- Play offered as one choice among 24 ordered triples: This makes the simultaneous secret ordered list a single poll with only legal options (3 different cards from own 4).
- No free-text talk step: The rules contain no talk. With two players the calls themselves are the signalling and bluffing channel.
- Strategy check: A thoughtful player weighs the opponent's visible face-up card against their own, bluffs PUT or RE-PUT with weak hands, folds cheaply when outmatched, and orders cards to dodge the opponent's likely ordering (e.g. sacrificing a weak card against a strong one).
- rank_by weight 1000: Hands won is at most 40, so points*1000 + hands_won ranks by points first, then by hands won.

## Simplifications

- The Caller and Responder are worked out from hand_number parity in each step's 'who': The engine has no role-swap action; parity gives the same alternation.
- Conditional steps 4 and 5–7 are written as individual steps with when-conditions on caller_call, responder_answer and folded: The step list is flat, and per-step conditions reproduce the branching of the hand faithfully.
- Trick comparison between the two players' play lists uses a table-side comparison: Comparing one player's attribute with another's needs the documented workaround of copying values to the table.

## Unsupported (needs engine work)

- none
