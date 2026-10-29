# Love Letter: One Raise

Two-player Love Letter with a 16-card deck in which, once per hand, the player about to draw may raise the stake from 1 to 2 and the opponent must accept or concede 1 point; first to 5 points wins, capped at 40 turns.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 16
- `guard_rank` = 1
- `guard_copies` = 5
- `priest_rank` = 2
- `priest_copies` = 2
- `baron_rank` = 3
- `baron_copies` = 2
- `handmaid_rank` = 4
- `handmaid_copies` = 2
- `prince_rank` = 5
- `prince_copies` = 2
- `king_rank` = 6
- `king_copies` = 1
- `countess_rank` = 7
- `countess_copies` = 1
- `princess_rank` = 8
- `princess_copies` = 1
- `removed_face_up` = 3
- `cards_dealt_per_player` = 1
- `deck_after_deal` = 11
- `burned_cards` = 1
- `starting_points` = 0
- `starting_hands_won` = 0
- `starting_stake` = 1
- `raised_stake` = 2
- `concede_gain` = 1
- `max_raises_per_hand` = 1
- `guard_guess_min` = 2
- `guard_guess_max` = 8
- `hand_end_deck_threshold` = 1
- `points_to_win` = 5
- `max_turns` = 40
- `first_starter_seat` = 1

## Round

1. **update** (all players): When new_hand_due: deck = [1,1,1,1,1,2,2,3,3,4,4,5,5,6,7,8]. Move 3 random cards from deck to removed. Move 1 random card to the starter_seat player's hand, then 1 to the other player's hand. Move 1 random card from deck to burned, leaving 10 in deck. stake = 1, raised = false, hand_over = false, hand_winner = 0. Every player: protected = false, eliminated = false, discard_sum = 0. active_seat = starter_seat, new_hand_due = false.
2. **tell** (all players): When a new hand was just started: announce the 3 cards in removed and which seat starts.
3. **sync** (all players): Each player sees their own hand.
4. **update** (all players): turn += 1; raise_choice = '', response = '', last_discard = 0, guard_guess = 0, prince_target = 0, prince_discard = 0.
5. **ask** (the active player): When raised == false: set raise_choice.
6. **ask** (the opponent of the active player): When raise_choice == 'raise': set response.
7. **update** (all players): If response == 'concede': the active player's points += 1 and hands_won += 1; hand_winner = active_seat; hand_over = true. If response == 'accept': stake = 2 and raised = true.
8. **update** (the active player): When hand_over == false: the active player's protected = false; move 1 random card from deck to their hand.
9. **sync** (the active player): When hand_over == false: the active player sees both of their cards.
10. **ask** (the active player): When hand_over == false: set last_discard to the chosen rank.
11. **update** (the active player): When hand_over == false: remove last_discard from the active player's hand; their discard_sum += last_discard. If last_discard == 4, they become protected = true. If last_discard == 8, they become eliminated = true.
12. **ask** (the active player): When hand_over == false and last_discard == 1: set guard_guess.
13. **ask** (the active player): When hand_over == false and last_discard == 5: prince_target = the chosen seat.
14. **update** (all players): Guard: when hand_over == false, last_discard == 1, the opponent is not protected and the opponent's hand card == guard_guess, the opponent's eliminated = true.
15. **tell** (the active player): Priest: when hand_over == false, last_discard == 2 and the opponent is not protected, privately show the opponent's hand card to the active player.
16. **tell** (both players, each privately): Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, show each player the other's hand card privately.
17. **update** (all players): Baron: when hand_over == false, last_discard == 3 and the opponent is not protected, the player whose hand card is lower gets eliminated = true; if the cards are equal, nothing happens.
18. **update** (the Prince target): Prince: when hand_over == false and last_discard == 5: prince_discard = the target's hand card; empty the target's hand; the target's discard_sum += prince_discard. If prince_discard == 8, the target's eliminated = true. Otherwise move 1 random card from deck to the target's hand, or the burned card if deck is empty.
19. **update** (both players): King: when hand_over == false, last_discard == 6 and the opponent is not protected, swap the two players' hand lists.
20. **sync** (all players): When hand_over == false: each player sees their own current hand.
21. **tell** (all players): Announce last_discard, guard_guess or prince_target if any, prince_discard if any, any elimination with the eliminated player's revealed hand card, stake, both players' points, and the deck count (len(deck) + len(burned)).
22. **update** (all players): When hand_over == false: if a player is eliminated, the other player's points += stake and hands_won += 1, hand_winner = that seat, hand_over = true. Otherwise, if len(deck) + len(burned) <= 1: the higher hand card wins, and on equal cards the higher discard_sum wins. The winner's points += stake and hands_won += 1, hand_winner = that seat; if both are equal, hand_winner = 0. hand_over = true.
23. **tell** (all players): When a showdown happened: reveal both hand cards, both discard_sum values and the hand winner (or that nobody scored).
24. **update** (all players): If hand_over: starter_seat = the seat that is not hand_winner if hand_winner != 0, else the seat that is not starter_seat; new_hand_due = true. If not hand_over: active_seat = the other seat.
25. **check** (all players): End the game if any player's points >= 5 or turn >= 40; otherwise continue.

## Ending

- ends when: any player's points >= 5 or turn >= 40
- ranked by: `you.points * 1000 + you.hands_won` (the highest wins; players level at the top share the win)
- decided by: The player with the most points wins; the first to reach 5 ends the match at once, since only one player scores per hand. At the 40-turn limit, more points wins, then more hands won. Players level on both share the win, which is a draw.

## Choices the source did not make

- 2 players, suggested 2: The designer fixed the game at Seat 1 and Seat 2; the raise and concede duel is head to head and every rule addresses 'the opponent'. Strategy lies in raising on strong cards, bluffing raises on weak ones, and reading the removed and discarded cards.
- No free talk step: The source rules have no talk, and with two players the raise is itself the signal.
- The Countess is enforced by offering only the 7: The result is the same as 'discarded instead, whatever they chose', and the seat is never offered a move it may not make.
- rank_by = points * 1000 + hands_won: Points first, hands won as the tie-break; hands won never reaches 1000, and a full tie is a shared win, which is the draw.
- A 'no raise' does not use up the raise: The rules allow a raise whenever no raise has been made; only an accepted raise (or a concession, which ends the hand) closes it.

## Simplifications

- The burned bottom card is drawn at random at the start of the hand into a separate hidden 'burned' list, and draws take random cards from 'deck'.: The engine draws at random from a list rather than from an ordered pile; the outcome has the same distribution. The deck count is len(deck) + len(burned).
- Effect steps are flat steps each guarded by a condition on last_discard, hand_over and protection: The step list is flat; the per-step conditions reproduce skipping the rest of the turn after a concession.

## Unsupported (needs engine work)

- none
