# Bidder's Choice: Sealed Pool

Over 6 rounds, players talk and then place sealed bids from 20 coins; each round's winner pays and picks one of six objects that every player values privately, and the score is coins left plus own values of held objects.

Players: 3 to 5, best with 3

## Parameters

- `starting_coins` = 20
- `object_count` = 6
- `value_1` = 2
- `value_2` = 4
- `value_3` = 6
- `value_4` = 8
- `value_5` = 10
- `value_6` = 14
- `value_total` = 44
- `rounds` = 6
- `talk_max_words` = 40
- `min_bid` = 0
- `tiebreak_key_multiplier` = 10
- `min_players` = 3
- `max_players` = 5
- `suggested_players` = 3

## Round

1. **update** (all players): round += 1; winner_seat = 0; taken_object = ''.
2. **tell** (all players): Announce round, pool, and every player's coins and holdings.
3. **poll** (all players): Set each player's message, truncated to 40 words. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
4. **poll** (all players): Set each player's bid. A missing, non-integer, negative or over-coins answer sets bid = 0.
5. **update** (all players): For each player, bid_key = bid * 10 + (6 - holdings_count); top_key = max of bid_key; top_count = number of players with bid_key == top_key; winner_seat = the seat with bid_key == top_key if top_count == 1, else 0.
6. **update** (the winner (when winner_seat != 0)): The winner's coins -= the winner's bid.
7. **ask** (the winner (when winner_seat != 0)): Set taken_object to the chosen letter. If there is no valid answer, taken_object = the pool object with the highest of the winner's own values (ties: earliest letter).
8. **update** (the winner (when winner_seat != 0)): Remove taken_object from pool; append it to the winner's holdings; the winner's holdings_count += 1.
9. **tell** (all players): Reveal every player's bid, the winner (or 'no sale' if winner_seat == 0), and taken_object.
10. **update** (all players (when round == 6)): Pool objects are discarded (pool = []). For each player, score = coins + the sum of value_x over each object x in holdings.
11. **tell** (all players (when round == 6)): Reveal all players' value_a through value_f and every score.
12. **check** (all players): End the game if round == 6; otherwise continue to the next round.

## Ending

- ends when: round == 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is his final score: coins left plus the sum of his own values for the objects he holds. The highest score wins, and players level at the top share the result (the source calls this a draw).

## Choices the source did not make

- 3 to 5 players, suggested 3: The designer suggests 3, which is kept. 3 is the minimum where the fewest-objects tie-break and rival bidding create real competition. Above 5, there is less than one object per player and the talk grows long.
- Talk kept as a simultaneous poll broadcast to all: The rules specify simultaneous talk. Players disagree because their private values differ, so bluffing about which object one wants, or about intending to sit out, can steer rivals' bids.
- Tie-break encoded as bid_key = bid * 10 + (6 - holdings_count): Holdings never exceed 6, so this single number orders players by bid first and then by fewest objects. A tie in bid_key at the top is exactly the no-sale case.
- Values stored as six ally attributes value_a through value_f, dealt by drawing from each player's own value_bag list: This gives each player an independent random permutation, as the rules require, and declares the dealing source as state.
- bid_key is an ally player attribute: It is a scratch number derived from the player's own bid, so only the owner may see it until bids are revealed.
- Score computed only after round 6: A public running score would leak private values.
- Strategy note: A thoughtful player bids up only for his high-value objects, shades bids against rivals' remaining coins, uses holding few objects as a tie-break edge, and bluffs in talk. A thoughtless one overpays for low-value objects.

## Simplifications

- A draw at the top is represented as a shared win among the tied players: The engine has no separate draw; players level at the top share the win.
- The pick is offered as a choice from the current pool, so an invalid letter cannot be chosen; the fallback applies only when there is no answer: Choice lists come from the pool list. The source's fallback rule is still kept.

## Unsupported (needs engine work)

- none
