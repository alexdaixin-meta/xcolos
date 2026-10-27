# 11 Nimmt: Two Hot Piles

Each turn, place one card from a hidden hand on one of two shared piles where it fits; a player with no legal placement must take a pile's ox-heads as penalty, though taking a pile of 3 or more cards earns a bull worth -2. The lowest penalty minus twice bulls wins.

Players: 3 to 4, best with 3

## Parameters

- `deck_size_3p` = 30
- `deck_size_4p` = 40
- `hand_size_3p` = 9
- `hand_size_4p` = 8
- `set_aside_3p` = 1
- `set_aside_4p` = 6
- `start_turns_per_seat_3p` = 3
- `start_turns_per_seat_4p` = 2
- `starting_piles` = 2
- `starting_pile_size` = 1
- `fit_min_distance` = 1
- `fit_max_distance` = 10
- `pile_room_limit` = 5
- `bull_pile_threshold` = 3
- `bull_value` = 2
- `ox_special_cards` = 3
- `ox_multiple_of_5` = 2
- `ox_other` = 1
- `special_card_1` = 11
- `special_card_2` = 22
- `special_card_3` = 33
- `starting_penalty` = 0
- `starting_bulls` = 0

## Round

1. **update** (table): current_seat = ((round - 1) mod number_of_players) + 1; turns_in_round = 0
2. **ask** (seat current_seat): Records the chosen card c and pile X
3. **update** (seat current_seat): Remove c from hand. If c fits X ((c - top_X) mod N in 1..10) and size_X < 5 (a placement): append c to pile_X, top_X = c, size_X += 1, ox_X += ox(c). Otherwise (a take): penalty += ox_X; if size_X >= 3 then bulls += 1; move all of pile_X into discarded; pile_X = [c], top_X = c, size_X = 1, ox_X = ox(c). The other pile is unchanged. Then score = penalty - 2 * bulls, and last_play describes the move.
4. **tell** (all players): Announce last_play, both piles (cards, top, size, ox total) and every player's penalty, bulls and score.
5. **update** (table): current_seat = (current_seat mod number_of_players) + 1; turns_in_round += 1
6. **repeat** (table): Repeat steps 2 to 5 until turns_in_round = number_of_players.
7. **update** (table): round += 1
8. **sync** (all players): Each player is sent their own hand and the public state.
9. **check** (table): If round > hand_size, end the game; otherwise continue.

## Ending

- ends when: round > hand_size
- ranked by: `2 * you.bulls - you.penalty` (the highest wins; players level at the top share the win)
- decided by: Each player's final score is penalty - 2 * bulls. The lowest final score wins, so ranking is by its negative. Players tied for lowest share the win, which is a draw among them.

## Choices the source did not make

- 3 to 4 players, suggested 3: The source defines the deck and hand only for 3 and 4 players, and the designer suggests 3. With fewer, there is too little contention over the two piles; the rules define no larger deck.
- No talk step before each turn: The source has no communication phase, and adding one would be adding a mechanic. Play is about hand management: keeping low-risk cards, timing takes while piles are small, and taking a pile of 3 or more cards when the bull's -2 outweighs its ox-heads.
- Card and pile are chosen as one combined option: The rules ask for both together, and a single choice lets the offers enforce the placement-first rule exactly.
- Rank by 2 * bulls - penalty: The engine ranks the highest value first, and the rules want the lowest penalty - 2 * bulls.
- A running score attribute updated every turn: It makes the standing observable and testable during play.

## Simplifications

- The rotating start seat and sequential turns are built as a repeat loop over current_seat with a per-turn update: Each turn changes the piles before the next seat chooses, so each turn's update must run before the next ask.
- Whether a move is a take is worked out at update time by testing if the chosen card fits the chosen pile with room: The offers allow non-placements only when no placement exists, so this test is equivalent to the rule.

## Unsupported (needs engine work)

- none
