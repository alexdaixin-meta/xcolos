# unique_bid_auction: ready for review

Built from the variation **Lowest Unique Number** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Fix the player count at 3 to 5 (suggested 4), so that a collision on the minimum benefits third parties. (fixes: With 2 players, always bidding the minimum cannot lose, so the game is degenerate under a highest-total winner rule.): With three or more players, two players sitting on 1 cancel each other and hand the round to someone else, so always picking 1 can lose.
- Each player picks exactly one number per round, from 1 to 5. There are no fees and no multiple bids. (fixes: Unlimited multiple bids per player let a player buy coverage of a range instead of reasoning, and they explode the choice space.): This removes buying coverage and keeps the choice small, clear and buildable.
- Use a small whole-number range (1 to 5) instead of pennies, with a small field of players. (fixes: Penny-precise bids and up to 100 players make the choice space huge and the outcome a lottery.): Each pick then meaningfully changes who is unique, and choices change outcomes.
- Play 12 rounds, reveal all picks after each round, and decide the game by the highest total. (fixes: A single one-shot auction gives no history, so there is no opponent modelling or planning over rounds, and luck dominates skill.): Revealed history lets players model each opponent's habits, exploit them, and plan blocks against the leader over several rounds.
- The player with the lowest unique number wins the round and scores points equal to that number (1 to 5). (fixes: In the lowest-unique version the lowest number is always the most valuable to win with, so the only tension is the risk of collision, not value against safety.): Low numbers win more often but pay little, and high numbers pay a lot but rarely survive. This adds a real trade-off between safety and value on top of collision risk.
- Add a simultaneous one-message talk phase before each pick. (fixes: A single one-shot auction gives no history, so there is no opponent modelling or planning over rounds, and luck dominates skill.): Only one player can win each round and only one can win the game, so messages become bluffs, feints and calls to gang up on the leader by colliding with them. Talk gives players something to reason about; it is not a coordination device that removes the choice.

Objective: After 12 rounds, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Main tension: a low number is more often the lowest unique pick but scores less; a high number scores more but rarely wins. Round winner per profile (4 players): picks (1,2,2,3) -> 1 unique, P1 +1; (1,1,2,5) -> 2 unique, P3 +2; (1,1,5,5) -> no unique, nobody scores; (2,2,3,3) -> nobody scores; (1,1,
- playable: pass. The rules are complete:
- pick range 1-5, whole numbers;
- uniqueness means exactly one picker;
- the winner holds the lowest unique number and scores that number;
- no unique number means no score;
- 12 fixed rounds;
- highest total wins, and a tie for highest is a draw.
The game is finite and deci
- reasoning_over_luck: pass. There are no random draws, so chance contributes about 0%. The only uncertainty is opponents' simultaneous picks. With all players at the symmetric mixed equilibrium, outcomes vary through mixing. But 12 rounds of fully revealed picks, labelled by player, let a reasoner detect patterns, anticipate c

## Complexity

- steps_per_round: designed 10, built 11, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 9, built 18, limit 20 (built: 80)
- hidden_elements: designed 1, built 2, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Game starts with every score 0 and round 0 (a no-winner first round leaves scores at 0 and round at 1)
- pass: A round with talk then picks completes and counts as one round
- pass: Every seat is asked for a number from 1 to 5 and nothing outside it
- pass: Revealed picks equal the picks made
- pass: Counting picks 1,1,3,3,5 leaves only 5 with a count of one
- pass: A number picked by exactly one player is unique (picks 4,2,2)
- pass: Picks 1,1,2,3 give winning number 2
- pass: Picks 2,2,4,4 give no winner and nobody scores
- pass: A unique winning pick of 3 adds 3 to the score
- pass: Players whose pick is not the winning number keep their score
- pass: Round counter goes up by one at the end of a round
- pass: Game ends when round reaches 12
- pass: Highest score wins outright
- pass: Players tied for the highest score share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 10, 'seat 1': 13, 'seat 3': 6, 'seat 4': 6, 'seats 2 and 5': 1, 'seat 5': 3, 'seats 2 and 3': 1}, 72-120 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 190 characters on average (longest 209)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 22, 'seat 1': 21, 'seat 3': 15, 'seats 1 and 3': 1, 'seats 1 and 2': 1}
- always `first@seat1`: won 17, lost 40, drew 3
- always `first@seat2`: won 24, lost 30, drew 6
- always `last@seat1`: won 18, lost 41, drew 1
- always `last@seat2`: won 17, lost 41, drew 2

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer suggested 4, so it is kept. With 2 players, uniqueness is trivial: any two different picks make both unique, so the game reduces to guessing the other player. 3 is the smallest table where collisions and blocking create a real dilemma. Above 5, the 5 numbers fill up, most rounds have no winner, and one player's choice matters little.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous talk. Players disagree here, since each wants to be the unique low picker, so claims, threats and bluffs ('I'm taking 1') give the others something to reason about. A thoughtful player weighs whether others will avoid a claimed number or collide on it, and uses the scores so far to guess who will block whom.
- winning_number = 0 means no winner: The source does not encode 'no winner' as a number. 0 cannot be a pick, so it is safe.
- Separate revealed_pick attribute: Keeps each pick hidden until all are in, then makes the picks public for the reveal.

## Simplifications

- A tie for the highest score is a shared win, not a 'draw': The engine has no separate draw: players level at the top share the win. With a tie at the top, this means the same thing as a draw among the leaders.
- The 30-word limit on messages is stated to players rather than enforced word by word: The engine takes short text answers. The limit is given in the question.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (message, message, message); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
