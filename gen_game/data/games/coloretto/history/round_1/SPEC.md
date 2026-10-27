# Coloretto: Secret Favourites

Three players take turns either adding the face-up card to one of three rows or taking a row. They collect colours, score their best three and lose points for the rest, and earn a bonus for a secret Favourite colour.

Players: 3 to 3, best with 3

## Parameters

- `colours` = 5
- `cards_per_colour` = 7
- `plus_two_cards` = 3
- `deck_size` = 38
- `rows` = 3
- `row_capacity` = 3
- `rounds` = 36
- `positive_colours` = 3
- `negative_colours` = 2
- `plus_two_value` = 2
- `favourite_bonus` = 6
- `points_for_count_0` = 0
- `points_for_count_1` = 1
- `points_for_count_2` = 3
- `points_for_count_3` = 6
- `points_for_count_4` = 10
- `points_for_count_5` = 15
- `points_for_count_6` = 21
- `points_for_count_7` = 28

## Round

1. **sync** (all players): Everyone sees top_card, row_1..row_3 with their open flags, every player's colour counts and plus_two, every taken flag and turn. Each player also sees their own favourite.
2. **ask** (the player at seat game.active_seat): Records the chosen action. An illegal or missing choice becomes take of the lowest-numbered open row with at least 1 card; if there is none, it becomes place on the lowest-numbered open row with fewer than 3 cards.
3. **update** (the active player): When the action is place_k: append top_card to row_k, then draw a random card from deck into top_card and remove it from deck.
4. **update** (the active player): When the action is take_k: for each card in row_k, add 1 to the active player's matching colour count, or to plus_two for a '+2' card. Then set row_k = [], row_k_open = false, active.taken = true and takers += 1.
5. **update** (table): When takers < 3: set active_seat to the first seat in order active_seat+1, active_seat+2, active_seat (wrapping 3 to 1) whose taken is false. This may be the same seat again.
6. **update** (table): When takers == 3 (the cycle has ended): set row_1, row_2 and row_3 to [], set every row_k_open = true, set every player's taken = false and takers = 0. active_seat stays the player who took last.
7. **update** (table): turn += 1.
8. **update** (all players): When turn > 36: rows are discarded. For each player, sort the counts of red, blue, green, yellow and purple from highest to lowest as s1..s5, with T(c) = c*(c+1)/2. Set score = T(s1)+T(s2)+T(s3) - T(s4) - T(s5) + 2*plus_two + (6 if the favourite colour's count >= s3, else 0). Copy favourite into favourite_revealed.
9. **check** (table): End the game when turn > 36; otherwise run the next round.

## Ending

- ends when: game.turn > 36
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's final score is their best three colours positive, their other two colours negative, plus 2 per '+2' card, plus 6 if their Favourite is among the colours that can score. The highest score wins, and players tied for the highest score draw (share the win).

## Choices the source did not make

- Exactly 3 players: The designer fixed the size at 3, and the rules are built around three rows and three takers per cycle. A fourth player has no row to take, and with two the cycle logic breaks.
- No talk step: The source rules include no discussion, and adding one would add a mechanic. The strategy lies in reading the other players' collections, guessing their Favourites from what they take, and deciding when to take a small row rather than wait.
- Points written as c*(c+1)/2: This matches the source table 0,1,3,6,10,15,21,28 exactly and is arithmetic.
- Favourite pool removes dealt colours: This makes every Favourite different, as the source requires.

## Simplifications

- One action per round; the active seat is tracked in active_seat and the asked seat is taken from it: The engine runs flat rounds, so the 'who' of the ask step comes from a table attribute.
- Top-3 versus bottom-2 scoring is computed by sorting the five colour counts in a calc step: There is no lookup operation; sorting counts gives the same result as sorting points because the points table is increasing.
- Favourites are revealed by copying them to a public attribute at the end: This is the engine's way to reveal hidden player state.

## Unsupported (needs engine work)

- none
