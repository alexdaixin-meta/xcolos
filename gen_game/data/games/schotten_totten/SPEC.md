# Schotten Totten: Five Stones

Two players take turns placing cards from a private hand onto their side of five Stones, forming three-card poker-like formations; a player claims a Stone with the stronger side, and the first to claim 3 of the 5 Stones wins.

Players: 2 to 2, best with 2

## Parameters

- `deck_size` = 36
- `colours` = 4
- `max_card_value` = 9
- `stones` = 5
- `side_capacity` = 3
- `hand_size` = 6
- `draw_pile_after_deal` = 24
- `max_rounds` = 30
- `stones_to_win` = 3
- `straight_flush_bonus` = 120
- `three_of_a_kind_bonus` = 90
- `flush_bonus` = 60
- `straight_bonus` = 30
- `no_formation_bonus` = 0
- `straight_span` = 2

## Round

1. **update** (all players): round += 1; active_seat = 1 if round is odd, else 2.
2. **tell** (all players): Announce every Stone's sides (stone_k_a, stone_k_b), stone_owner, each player's claimed, and deck_count.
3. **sync** (all players): Each player privately sees their own hand.
4. **ask** (the active player (seat active_seat)): The chosen card is remembered as the card to play.
5. **ask** (the active player (seat active_seat)): The chosen Stone k is remembered.
6. **update** (the active player): Remove the chosen card from the active player's hand and append it to stone_k_a (if active_seat == 1) or stone_k_b (if active_seat == 2). Cards never move again.
7. **update** (the active player): If the active side of Stone k now has 3 cards and the opposite side has fewer than 3, set first_finisher[k] = the active player's role.
8. **update** (the active player): If deck_count > 0, draw a random card from deck into the active player's hand and set deck_count -= 1.
9. **update** (all players): For each Stone k = 1..5 where stone_owner[k] == '' and both len(stone_k_a) == 3 and len(stone_k_b) == 3, compute strength_a and strength_b by the strength formula. If strength_a > strength_b, the owner is 'A'. If strength_b > strength_a, the owner is 'B'. If they are equal, the owner is first_finisher[k]. Set stone_owner[k] to the owner and add 1 to that player's claimed. Announce the result.
10. **check** (all players): End the game if any player's claimed >= 3, or if round >= 30. Otherwise continue.

## Ending

- ends when: max over players of claimed >= 3, or round >= 30
- ranked by: `you.claimed` (the highest wins; players level at the top share the win)
- decided by: A player's standing is the number of Stones they have claimed. The first to reach 3 wins at once. If round 30 ends without that, the player with more claimed Stones wins, and equal counts share the win (a draw).

## Choices the source did not make

- Exactly 2 players, suggested 2: The designer fixed the game at 2. Each Stone has exactly two sides, A and B, so the game does not scale to more seats.
- No talk step: The rules include no table talk. This is a two-player positional duel, and messages would add nothing the rules call for.
- Card choice and Stone choice are two sequential asks: The source lists them as separate steps (2) and (3). Asking them separately keeps each option list exact.
- Drawing the top card is a random pick from deck: The deck is shuffled, so a random draw is equivalent to taking the top card.
- The round counter and active seat are updated at the start of each round: This lets the engine pick the active player by arithmetic on round parity.
- The end check also fires at round >= 30: The source caps the game at 30 rounds. At that point all 30 slots are filled and every Stone has been resolved.
- Strategy at the table: Each card commits to one Stone permanently. A thoughtful player judges which formations are still possible given the visible cards, decides which Stones to contest and which to concede, and races to finish a side first so they win ties.

## Simplifications

- Stone sides are table attributes (stone_k_a and stone_k_b) rather than per-player lists: The engine has no player-attribute operand for comparison. Keeping both sides on the table lets resolution compare the two strengths directly.
- Strength is computed by calculating each card's colour (first letter) and value (digit) inside the resolution update: The engine has no lookup operation. The formation test is pure arithmetic on the three values and colours, so no referee is needed.
- All five Stones are resolved in one update step, using per-Stone conditional operations: Each Stone's resolution is an independent conditional update. No branching block of steps is needed.

## Unsupported (needs engine work)

- none
