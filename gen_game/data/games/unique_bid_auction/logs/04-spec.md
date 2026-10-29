# 04 spec

- time: 2026-10-27T21:37:15+00:00 (27.3s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 b3690a15442cd55b, reply sha256 9c8c76abe7bceaec

## Sent

````
Game: Lowest Unique Number
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
Setup: 3 to 5 players (4 suggested). Every player starts with a score of 0. The game lasts exactly 12 rounds.

Each round has these phases:

1. Talk. Every player writes one short message (at most 30 words) at the same time, without seeing the others. All messages are then shown to everyone together. Messages are not binding: players may claim, threaten or lie freely.

2. Pick. Every player secretly and simultaneously picks one whole number from 1 to 5. No player sees any other pick before choosing.

3. Reveal. All picks are revealed together, showing who picked what.

4. Count. For each number from 1 to 5, count how many players picked it.

5. Winner of the round. A number is 'unique' if exactly one player picked it. The round winner is the player who picked the lowest unique number. If no number is unique, nobody wins the round.

6. Score. The round winner adds points equal to their number (1 to 5) to their score. Nobody else scores this round.

7. Announce. The round's picks, the winning number (or 'no winner') and all players' current scores are announced to everyone.

After round 12 the game ends.

How the winner is decided: After 12 rounds, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Lowest Unique Number",
  "summary": "Over 12 rounds every player secretly picks a number from 1 to 5, and the player with the lowest number nobody else picked scores that many points.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "rounds": 12,
    "min_pick": 1,
    "max_pick": 5,
    "message_max_words": 30,
    "starting_score": 0,
    "unique_count": 1,
    "no_winner_number": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points won so far", "observable": true},
      {"key": "pick", "type": "number", "visible": "ally", "initial": 0, "meaning": "This round's secret pick from 1 to 5, before the reveal", "observable": false},
      {"key": "revealed_pick", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's pick, copied from pick at the reveal", "observable": true},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's talk message, shown to all after everyone has written", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of rounds completed", "observable": true},
      {"key": "count_1", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players picked 1 this round", "observable": false},
      {"key": "count_2", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players picked 2 this round", "observable": false},
      {"key": "count_3", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players picked 3 this round", "observable": false},
      {"key": "count_4", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players picked 4 this round", "observable": false},
      {"key": "count_5", "type": "number", "visible": "public", "initial": 0, "meaning": "How many players picked 5 this round", "observable": false},
      {"key": "winning_number", "type": "number", "visible": "public", "initial": 0, "meaning": "The lowest unique number this round, or 0 if no number is unique", "observable": true}
    ]
  },
  "setup": [
    "Seat 3 to 5 players (4 suggested).",
    "Set every player's score to 0.",
    "Set round to 0. The game lasts exactly 12 rounds."
  ],
  "round": [
    {"action": "poll", "who": "all players", "answer": "short text, at most 30 words", "effect": "Each player's message is set to their text. When all messages are in, they are broadcast together: {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Messages are not binding."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 1 to 5", "effect": "Each player's pick is set to their number. Nobody sees another pick until all are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For every player, revealed_pick = pick. All picks are shown together with who picked what."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each k from 1 to 5, count_k = the number of players whose pick == k."},
    {"action": "update", "who": "all players", "answer": null, "effect": "winning_number = 1 if count_1 == 1, else 2 if count_2 == 1, else 3 if count_3 == 1, else 4 if count_4 == 1, else 5 if count_5 == 1, else 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player, if winning_number > 0 and pick == winning_number, then score += pick. Nobody else scores."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce to all every seat's revealed_pick, the winning_number (or 'no winner' if it is 0), and every player's score."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round >= 12, end the game. Otherwise start the next round."}
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 12 rounds. The highest score wins, and players tied for the highest score share the result."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player's score is 0 and round is 0."},
    {"id": "R2", "text": "When a round begins, then every player writes one message of at most 30 words at the same time, and all messages are shown to everyone together."},
    {"id": "R3", "text": "When players pick, then every player picks one whole number from 1 to 5 simultaneously, and no player sees another pick before choosing."},
    {"id": "R4", "text": "When all picks are in, then every player's revealed_pick equals their pick and is visible to everyone."},
    {"id": "R5", "text": "When picks are counted, then for each k from 1 to 5, count_k equals the number of players who picked k."},
    {"id": "R6", "text": "When exactly one player picked a number, then that number is unique."},
    {"id": "R7", "text": "When at least one number is unique, then winning_number is the lowest unique number (for example, picks 1,1,2,3 give winning_number 2)."},
    {"id": "R8", "text": "When no number is unique (for example, picks 2,2,4,4), then winning_number is 0 and nobody scores that round."},
    {"id": "R9", "text": "When a player's pick equals a winning_number above 0, then their score increases by that number (for example, a unique pick of 3 adds 3)."},
    {"id": "R10", "text": "When a player's pick is not the winning_number, then their score does not change that round."},
    {"id": "R11", "text": "When a round ends, then round increases by 1, and the picks, the winning number (or no winner) and all scores are announced."},
    {"id": "R12", "text": "When round reaches 12, then the game ends."},
    {"id": "R13", "text": "When the game ends, then the player with the highest score wins, and players tied for the highest score share the result."}
  ],
  "offers": [
    {"question": "Talk: write a short message (at most 30 words)", "who": "all players, at once", "options": "free text of at most 30 words, for every seat"},
    {"question": "Pick a number", "who": "all players, at once", "options": "every seat: 1, 2, 3, 4, 5"}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer suggested 4, so it is kept. With 2 players, uniqueness is trivial: any two different picks make both unique, so the game reduces to guessing the other player. 3 is the smallest table where collisions and blocking create a real dilemma. Above 5, the 5 numbers fill up, most rounds have no winner, and one player's choice matters little."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The source requires simultaneous talk. Players disagree here, since each wants to be the unique low picker, so claims, threats and bluffs ('I'm taking 1') give the others something to reason about. A thoughtful player weighs whether others will avoid a claimed number or collide on it, and uses the scores so far to guess who will block whom."},
    {"what": "winning_number = 0 means no winner", "why": "The source does not encode 'no winner' as a number. 0 cannot be a pick, so it is safe."},
    {"what": "Separate revealed_pick attribute", "why": "Keeps each pick hidden until all are in, then makes the picks public for the reveal."}
  ],
  "simplifications": [
    {"what": "A tie for the highest score is a shared win, not a 'draw'", "why": "The engine has no separate draw: players level at the top share the win. With a tie at the top, this means the same thing as a draw among the leaders."},
    {"what": "The 30-word limit on messages is stated to players rather than enforced word by word", "why": "The engine takes short text answers. The limit is given in the question."}
  ],
  "unsupported": []
}
```
````
