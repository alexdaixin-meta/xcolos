# Put: Twelve Hands

Two players play 12 hands of three-card Put. Each hand they may check or Put, then see or fold, then secretly order their cards for three tricks. The higher total score wins.

Players: 2 to 2, best with 2

## Parameters

- `hands` = 12
- `deck_size` = 52
- `copies_per_rank` = 4
- `ranks` = 13
- `cards_per_player` = 3
- `face_up_cards_per_player` = 1
- `tricks_per_hand` = 3
- `fold_points` = 1
- `check_win_points` = 1
- `put_seen_points` = 3
- `start_score` = 0
- `max_puts_per_hand` = 1

## Round

1. **update** (all players): hand_number += 1; leader = 1 if hand_number is odd, else 2; deck is rebuilt as the full 52 cards (rank values 1 to 13, four each); each player's hand, order, tricks and up_card are reset; leader_call, responder_action and leader_reply are set to empty; putter = 0; folded = false
2. **update** (all players): Deal: 3 times for each player, a random card is removed from deck and appended to that player's hand. Each player's up_card = the first card of their hand.
3. **sync** (all players): Each player sees their own hand and both up_cards.
4. **ask** (the leader (seat 1 in odd hands, seat 2 in even hands)): leader_call = answer; if Put, putter = leader
5. **ask** (the responder (the seat that is not the leader)): responder_action = answer; if answer = Put, putter = responder; if answer = Fold, folded = true
6. **ask** (the leader, only when leader_call = Check and responder_action = Put): leader_reply = answer; if Fold, folded = true
7. **update** (all players): when folded = true: the putter's score += 1; the folder scores 0; no cards are played
8. **poll** (all players, only when folded = false): Each player's order = their hand rearranged by the chosen permutation. Nobody sees the other's order until both are in.
9. **update** (all players): when folded = false: for each trick i from 1 to 3, the player whose order[i] is higher gets tricks += 1; equal values give no one a trick
10. **update** (all players): when folded = false and putter = 0: the player with more tricks scores += 1, and nobody scores if tricks are equal. When folded = false and putter > 0: if the putter's tricks > the opponent's tricks, the putter's score += 3; otherwise the opponent's score += 3.
11. **tell** (all players): Reveal both hands, both orders, each trick's result, tricks, points scored this hand and the total scores.
12. **check** (all players): End the game if hand_number = 12; otherwise continue to the next hand.

## Ending

- ends when: hand_number = 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: After hand 12 the player with the higher total score wins; equal totals share the win, which is a draw.

## Choices the source did not make

- Exactly 2 players: The designer fixed the game at 2. It is a heads-up bluffing duel, and the leader/responder structure is built for two seats.
- Ranks stored as numbers 1 (for 4) to 13 (for 3): Tricks are then decided by a plain numeric comparison.
- Card order answered as a permutation of dealt positions: This gives a fixed choice list that names the player's own cards unambiguously.
- No talk step: The rules say talk is not part of the game.
- Strategy at the table: A good player reads the opponent's face-up card, bluffs or value-puts with their hidden cards, and chooses a card order that anticipates the opponent's ordering.

## Simplifications

- none

## Unsupported (needs engine work)

- none
