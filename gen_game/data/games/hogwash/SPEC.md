# Hogwash: Six Ranks

Three players take turns face-down dumping 1 to 4 cards that they claim are the required rank. The others secretly trust or challenge, and whoever holds the fewest cards after 24 rounds wins.

Players: 3 to 3, best with 3

## Parameters

- `deck_size` = 24
- `num_ranks` = 6
- `copies_per_rank` = 4
- `hand_size_initial` = 8
- `num_seats` = 3
- `total_rounds` = 24
- `k_min` = 1
- `k_max` = 4
- `turns_per_seat` = 8
- `catches_initial` = 0
- `caught_initial` = 0
- `pile_initial_size` = 0
- `rank_weight_hand` = 10000
- `rank_weight_catches` = 100
- `rank_weight_caught` = 1

## Round

1. **update** (table): round += 1; active_seat = ((round-1) mod 3)+1; required_rank = ((round-1) mod 6)+1; skipped = (hand_size of active_seat == 0); k = 0; statement = ''; played = []; challengers = 0; every response = ''
2. **tell** (all players): announce 'Round {round}: Seat {active_seat} must play rank {required_rank}' (plus 'and skips, holding 0 cards' when skipped)
3. **sync** (all players): each player sees their own hand
4. **ask** (seat active_seat, when skipped is false): k = min(answer, hand_size of active seat)
5. **ask** (seat active_seat, when skipped is false): statement = answer
6. **update** (table, when skipped is false): move k cards from the active player's hand to played and onto the top of pile: first cards equal to required_rank, then rank required_rank+1, and so on, wrapping 6 to 1, until k are taken; hand_size -= k; pile_size += k; play_true = (count of cards in played equal to required_rank == k)
7. **tell** (all players, when skipped is false): announce 'Seat {active_seat} claims {k} cards of rank {required_rank}. Statement: {statement}'
8. **poll** (every seat except active_seat, simultaneously, when skipped is false (including players holding 0 cards)): response = answer for each polled player; then reveal all responses together; challengers = count of polled players with response == Challenge
9. **tell** (all players, when skipped is false and challengers > 0): reveal the contents of played to everyone
10. **update** (table, when skipped is false and challengers > 0 and play_true is false): append all of pile to the active player's hand; pile = []; pile_size = 0; active player's caught += 1; each player with response == Challenge: catches += 1; refresh hand_size
11. **update** (table, when skipped is false and challengers == 1 and play_true is true): append all of pile to the hand of the player with response == Challenge; pile = []; pile_size = 0; refresh hand_size
12. **update** (table, when skipped is false and challengers == 2 and play_true is true): shuffle pile; each challenger draws floor(pile_size/2) cards at random from pile into hand; if 1 card remains, move it to removed; pile = []; pile_size = 0; refresh hand_size
13. **tell** (all players): announce every player's hand_size, pile_size, and every player's catches and caught
14. **check** (table): if round >= 24, end the game; otherwise continue

## Ending

- ends when: round >= 24
- ranked by: `0 - you.hand_size * 10000 + you.catches * 100 - you.caught` (the highest wins; players level at the top share the win)
- decided by: Fewest cards in hand wins. Ties go to the most CATCHES, then to the fewest CAUGHT. Players still level share the win, which is the source's draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The rank schedule (each seat facing two fixed ranks, 8 turns each) and the split rule for two challengers depend on exactly 3 seats, so neither the minimum nor the maximum can move.
- No all-players talk poll before the Trust/Challenge poll: The source gives only the active player one public statement. Adding free talk would add a mechanic; the bluffing lives in the claim and the statement.
- The statement is a separate ask after k: Each question takes one answer type, so the number and the text are asked in two steps by the same seat.
- Ranking expression -hand_size*10000 + catches*100 - caught: Catches are at most 24 (times 100 is under 10000) and caught is at most 8 (under 100), so the weights reproduce the strict tie-break order: fewest cards, then most catches, then fewest caught.
- Strategy at the table: A thoughtful player tracks how many of each rank have been revealed, picked up or must still be out, judges whether a claim of k is plausible, and weighs taking the pile against letting a rival shed cards. They also choose when an honest play invites a costly challenge, and use the statement to mislead.

## Simplifications

- The k cards are chosen by a fixed engine rule rather than by the player: The source already specifies this; it is carried out as remove/append operations on hand, played and pile.
- Shuffling and splitting the pile are random draws from the pile list: The engine shuffles by drawing at random, which gives the same result.
- The draw among tied players is a shared win: The engine has no separate draw; players level at the top share the win.

## Unsupported (needs engine work)

- none
