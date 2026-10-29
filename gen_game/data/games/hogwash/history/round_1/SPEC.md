# Hogwash: Even Rounds

A bluffing shedding game. Each turn the active player plays 1 to 3 cards face down and claims they are all the required rank. Others may challenge, and whoever is wrong takes the whole pile. The game ends at the end of the cycle in which someone empties their hand, or after 36 turns. Fewest cards wins, with fewest cards taken as the tie-break.

Players: 3 to 4, best with 3

## Parameters

- `deck_size` = 25
- `rank_count` = 5
- `copies_per_rank` = 5
- `hand_size_3_players` = 8
- `hand_size_4_players` = 6
- `initial_pile_cards` = 1
- `min_cards_per_play` = 1
- `max_cards_per_play` = 3
- `first_required_rank` = 1
- `max_turns` = 36
- `first_active_seat` = 1
- `initial_taken` = 0

## Round

1. **tell** (all players): Announce: 'Turn {turn}: Player {active_seat} is active; required rank is {required_rank}.' If the active player is finished (hand_count = 0), also announce that their turn passes with no play. In that case steps 2-9 do not run (each carries when: active player's hand_count > 0).
2. **ask** (seat active_seat (only when its hand_count > 0)): Set play_count = the answer.
3. **ask** (seat active_seat (when hand_count > 0)): Remove that card from the active player's hand and append it to last_played and to pile.
4. **ask** (seat active_seat (when play_count >= 2)): Remove that card from hand and append it to last_played and to pile.
5. **ask** (seat active_seat (when play_count >= 3)): Remove that card from hand and append it to last_played and to pile.
6. **update** (all players (when active player played)): active player's hand_count -= play_count; pile_count += play_count. Announce 'Player {active_seat} plays {play_count} cards, claiming {play_count} cards of rank {required_rank}.'
7. **poll** (every player with hand_count > 0, including the active player (when active player played)): No state change. Broadcast to all: 'Seat {seat} says: {value}'. Messages are non-binding.
8. **poll** (every non-active player with hand_count > 0 (when active player played)): Set each answering player's challenge to the answer. The active player and finished players keep challenge = PASS. Nobody sees any answer until all are in.
9. **update** (all players (when active player played)): resolver_seat = the first seat s in clockwise order active_seat+1, active_seat+2, ... (wrapping, excluding active_seat) whose challenge = CHALLENGE; 0 if none. If resolver_seat = 0, the cards stay in pile and 'No challenge' is announced. Otherwise reveal last_played to all and set was_bluff = (count of cards in last_played whose rank != required_rank) > 0. Set taker = active_seat if was_bluff, else resolver_seat. The taker's hand gets every card in pile appended, the taker's hand_count += pile_count, and the taker's taken += pile_count. Then pile = [] and pile_count = 0. Announce 'true' or 'bluff', who took the pile and how many cards. Other challengers lose nothing.
10. **update** (all players): For each player, finished = (hand_count = 0). If any player has finished = true and end_marked = false, set end_marked = true and announce that the game ends at the end of this cycle.
11. **check** (all players): End the game if active_seat = number of players AND (end_marked = true OR turn = 36). Otherwise continue.
12. **update** (all players): required_rank = (required_rank mod 5) + 1; active_seat = (active_seat mod number_of_players) + 1; turn += 1. Clear last_played = [], play_count = 0, resolver_seat = 0, was_bluff = false, and every player's challenge = PASS.

## Ending

- ends when: active_seat = number_of_players AND (end_marked = true OR turn = 36), checked after a turn
- ranked by: `0 - (you.hand_count * 1000 + you.taken)` (the highest wins; players level at the top share the win)
- decided by: Fewest cards in hand ranks best; anyone finished holds 0. Among players level on the fewest cards, the lowest taken counter is better. The highest value of -(hand_count*1000 + taken) wins, and players level on both share the win (the source calls that a draw).

## Choices the source did not make

- 3 to 4 players, suggested 3: The designer suggested 3. Bluff-calling needs at least two potential challengers, so at least 3 seats are needed for the clockwise resolver rule to matter. The deal (8 or 6 cards each from 25) only supports 3 or 4 seats.
- Keep the simultaneous talk poll before the challenge poll: The source requires it. It earns its place because players disagree: each wants someone else to be the one to challenge and risk the pile. Threats and bluffs about challenging give something to reason about.
- One engine round equals one turn: This makes the end check after the last seat's turn and the rank/seat advance straightforward arithmetic.
- Ranking expression -(hand_count*1000 + taken): This puts hand size first and taken second in one arithmetic value. taken cannot exceed about 109 (at most 108 cards played in 36 turns plus the first pile card), so the 1000 weight keeps the two levels separate.

## Simplifications

- Choosing 1-3 cards is asked as a count followed by up to three single-card picks gated by when-conditions: An engine answer is a single choice, number or text, not a multi-select.
- A tie on fewest cards and lowest taken is a shared win rather than a declared draw: The engine has no separate draw: players level at the top share the win, which is equivalent.

## Unsupported (needs engine work)

- none
