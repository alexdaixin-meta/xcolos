# Three Up: Even Rounds

A three-player shedding game: each round everyone talks at the same time, then First, Second and Third each play cards of one rank at or above the Pile's top rank, play a Clear, or pick up the Pile; the first to empty Hand and Up pile wins, and the lowest picked-up total breaks ties.

Players: 3 to 3, best with 3

## Parameters

- `total_cards` = 30
- `lowest_rank` = 1
- `highest_rank` = 9
- `copies_per_rank` = 3
- `clear_cards` = 3
- `stack_size` = 9
- `low_ranks_max` = 3
- `mid_ranks_max` = 6
- `high_ranks_max` = 9
- `deal_per_stack` = 3
- `clear_per_player` = 1
- `cards_per_player` = 10
- `up_pile_size` = 3
- `hand_after_up` = 7
- `run_to_clear` = 3
- `max_rounds` = 40
- `rank_out_weight` = 1000000
- `rank_cards_weight` = 10000

## Round

1. **update** (all players): round += 1; announce the round number, pile, top_rank, run_count, every up_pile, hand_count and picked_up.
2. **poll** (all players): Every message is shown to everyone at once: broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes and nothing binds.
3. **sync** (all players): Each player receives their own hand, plus the public pile, top_rank, run_count, up_piles, hand_counts and picked_up counts.
4. **ask** (seat 1 (First), when out = false): Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
5. **update** (seat 1 (First), when out = false): PICK UP: append every pile card to hand; picked_up += len(pile); pile = []; top_rank = 0; run_count = 0. PLAY K x R: remove K R cards from the source and append them to pile; if R == top_rank then run_count += K, else run_count = K; top_rank = R; if run_count >= 3, move all pile cards to removed, set pile = [], top_rank = 0, run_count = 0. PLAY Clear: move the C and all pile cards to removed; pile = []; top_rank = 0; run_count = 0. Then recompute hand_count, up_count and cards_left = hand_count + up_count; out = (cards_left == 0); append the action to history; announce it.
6. **ask** (seat 2 (Second), when out = false): Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
7. **update** (seat 2 (Second), when out = false): Resolved exactly as for seat 1.
8. **ask** (seat 3 (Third), when out = false): Records the chosen action. An illegal or unreadable answer counts as 'pick up'.
9. **update** (seat 3 (Third), when out = false): Resolved exactly as for seat 1.
10. **update** (all players): players_out = the number of players with out = true.
11. **check** (all players): End the game if players_out >= 1 or round >= 40; otherwise continue to the next round.

## Ending

- ends when: players_out >= 1 or round >= 40 (checked only after seat 3's turn)
- ranked by: `you.out * 1000000 - you.cards_left * 10000 - you.picked_up` (the highest wins; players level at the top share the win)
- decided by: If any player is out at the end of the round, only the out players can win, and among them the lowest picked_up wins; out players tied on picked_up share the result (a draw). If round 40 ends with nobody out, the fewest cards_left wins, then the lowest picked_up, and players still tied share the result (a draw).

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at three: three ranked seats in a turn order, and an end check written for one, two or three emptied players.
- The talk round is a simultaneous poll with broadcast: The rules say messages are written at the same moment. Talk earns its place because players want opposite things (each wants the others to pick up) and can try to coax a rival into taking the Pile.
- Random seating maps to seat numbers 1, 2, 3 as First, Second, Third: The engine's seeded random seating gives the random order the rules ask for.
- Up pile chosen by three successive simultaneous polls into a private up_choice list, revealed afterwards: A single answer is one choice; three picks kept hidden until all are done keep the choice simultaneous.
- rank_by = out*1000000 - cards_left*10000 - picked_up: Out players rank above all others, then fewer cards, then fewer picked up. picked_up cannot reach 10000 in 40 rounds (at most 40 pickups of 27 cards), so the weights never overlap.
- Cards are written as text '1'..'9' and 'C'; top_rank is 0 for an empty pile: Gives the legality check a simple arithmetic comparison.

## Simplifications

- A draw is represented as all tied top players sharing the win: The engine has no separate draw; players level at the top share the result, and the other players still lose.
- Each seat's turn is written as its own ask plus update steps, in fixed seat order: Each play must resolve before the next seat chooses, against the current pile.

## Unsupported (needs engine work)

- none
