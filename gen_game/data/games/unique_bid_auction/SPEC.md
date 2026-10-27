# Lowest Unique Number

Over 12 rounds every player secretly picks a number from 1 to 5, and the player with the lowest number nobody else picked scores that many points.

Players: 3 to 5, best with 4

## Parameters

- `rounds` = 12
- `min_pick` = 1
- `max_pick` = 5
- `message_max_words` = 30
- `starting_score` = 0
- `unique_count` = 1
- `no_winner_number` = 0

## Round

1. **poll** (all players): Each player's message is set to their text. When all messages are in, they are broadcast together: {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding.
2. **poll** (all players): Each player's pick is set to their number. Nobody sees another pick until all are in.
3. **update** (all players): For every player, revealed_pick = pick. All picks are shown together with who picked what.
4. **update** (all players): For each k from 1 to 5, count_k = the number of players whose pick == k.
5. **update** (all players): winning_number = 1 if count_1 == 1, else 2 if count_2 == 1, else 3 if count_3 == 1, else 4 if count_4 == 1, else 5 if count_5 == 1, else 0.
6. **update** (all players): For each player, if winning_number > 0 and pick == winning_number, then score += pick. Nobody else scores.
7. **update** (all players): round += 1.
8. **tell** (all players): Announce to all every seat's revealed_pick, the winning_number (or 'no winner' if it is 0), and every player's score.
9. **check** (all players): If round >= 12, end the game. Otherwise start the next round.

## Ending

- ends when: round >= 12
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their total score after 12 rounds. The highest score wins, and players tied for the highest score share the result.

## Choices the source did not make

- 3 to 5 players, suggested 4: The designer suggested 4, so it is kept. With 2 players, uniqueness is trivial: any two different picks make both unique, so the game reduces to guessing the other player. 3 is the smallest table where collisions and blocking create a real dilemma. Above 5, the 5 numbers fill up, most rounds have no winner, and one player's choice matters little.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous talk. Players disagree here, since each wants to be the unique low picker, so claims, threats and bluffs ('I'm taking 1') give the others something to reason about. A thoughtful player weighs whether others will avoid a claimed number or collide on it, and uses the scores so far to guess who will block whom.
- winning_number = 0 means no winner: The source does not encode 'no winner' as a number. 0 cannot be a pick, so it is safe.
- Separate revealed_pick attribute: Keeps each pick hidden until all are in, then makes the picks public for the reveal.

## Simplifications

- A tie for the highest score is a shared win, not a 'draw': The engine has no separate draw: players level at the top share the win. With a tie at the top, this means the same thing as a draw among the leaders.
- The 30-word limit on messages is stated to players rather than enforced word by word: The engine takes short text answers. The limit is given in the question.

## Unsupported (needs engine work)

- none
