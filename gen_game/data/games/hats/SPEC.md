# Ripening Hats

Over 12 rounds, players secretly pick one of 5 hat colours (or safe Black); a colour picked by exactly one player pays its ripening value, plus a bonus if it is that player's secret favourite, and contested colours pay nothing.

Players: 3 to 4, best with 4

## Parameters

- `num_colours` = 5
- `initial_colour_value` = 2
- `max_colour_value` = 7
- `reset_value` = 1
- `value_increment` = 1
- `black_points` = 1
- `favourite_bonus` = 3
- `contested_gain` = 0
- `rounds` = 12
- `initial_score` = 0

## Round

1. **tell** (all players): Announce: 'Round {round} of 12. Values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}, Purple {value_purple}.'
2. **poll** (all players): Set each player's message to their text. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
3. **poll** (all players): Set each player's choice to their answer. No answer is shown to anyone.
4. **update** (all players): Set count_red, count_blue, count_green, count_yellow and count_purple each to the number of players whose choice is that colour. Set black_count to the number of players whose choice is Black.
5. **update** (all players): For each player: if choice = Black, add 1 to score. If choice is a colour C and count_C = 1, add value_C to score, and add a further 3 if favourite = C. If count_C >= 2, add 0. Do not announce scores.
6. **update** (all players): For each colour C, set status_C to COLLECTED if count_C = 1, CONTESTED if count_C >= 2, and UNTOUCHED if count_C = 0.
7. **tell** (all players): Announce without naming players: 'Red {status_red}, Blue {status_blue}, Green {status_green}, Yellow {status_yellow}, Purple {status_purple}. Black chosen by {black_count}.'
8. **update** (all players): For each colour C: if count_C = 1, set value_C to 1; otherwise set value_C to min(7, value_C + 1).
9. **sync** (all players): Each player is sent their own score and favourite.
10. **update** (all players): Add 1 to round.
11. **check** (all players): If round > 12, end the game. Reveal every player's favourite and score to everyone. Otherwise continue to the next round.

## Ending

- ends when: round > 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score. The highest score wins. Players tied for the highest score share the result, which is the source's draw.

## Choices the source did not make

- 3 to 4 players, suggested 4: The designer's suggested size is 4, so it is kept. The minimum is 3 because with 2 players the competition over colours is too thin to be interesting. The maximum is 4 because with 5 colours, 4 players still leave room to spread out, while a fifth player would let every favourite be in play and make collisions near-constant.
- Talk is kept as a simultaneous poll with a broadcast: The rules say messages are written at the same time without seeing the others, so a poll fits rather than ask. Talk earns its place because players have conflicting interests. Each wants a ripe colour to themselves, so claiming, warning or bluffing about a favourite gives others something to weigh. Following a claim can cost a player a collision.
- Strategy at the table: A thoughtful player tracks which colours are ripening, reads the COLLECTED and CONTESTED history to infer others' favourites, and uses talk to steer rivals away from their own targets. They also judge when the safe 1 point from Black beats a likely collision.
- Favourites are dealt from a hidden colour_pool list: This makes 'all different' a matter of draw-and-remove, which the engine supports.
- Score is marked observable: The source reveals scores at the end, and tests need the score. It stays ally-visible during play.
- Each player is synced their own score after collection: The source says each player can see their own private score. The source does not say when updates are delivered, so the sync timing is my choice.

## Simplifications

- A tie for the highest score is represented as a shared win: The engine has no separate draw outcome: players level at the top share the win, which corresponds to the source's draw.
- Per-colour counts and statuses are kept as separate table attributes (count_red, status_red and so on): The engine has no lookup by colour, so each colour gets its own counter and status.

## Unsupported (needs engine work)

- none
