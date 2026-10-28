# Go Nuts for Donuts: Secret Budget

Four players spend 10 simultaneous rounds picking one of five donuts. A donut scores only for a player who picks it alone, and each player has a secret split of 6 premium picks between Glazed and Jelly.

Players: 4 to 4, best with 4

## Parameters

- `glazed_points` = 9
- `jelly_points` = 6
- `cruller_points` = 4
- `sprinkle_points` = 2
- `plain_points` = 1
- `rounds` = 10
- `premium_picks` = 6
- `split_g_min` = 0
- `split_g_max` = 6
- `rank_score_multiplier` = 100

## Round

1. **update** (all players): Reset each player's choice to empty, void to false and gained to 0. Reset count_glazed, count_jelly, count_cruller, count_sprinkle and count_plain to 0.
2. **poll** (all players): Gather all messages at once, then broadcast to all: 'Seat {seat} says: {value}'. Messages bind no one.
3. **sync** (all players): Privately remind each player of their Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used).
4. **poll** (all players): Store each answer in that player's choice.
5. **update** (all players): Set void = true if (choice == Glazed and glazed_used >= split_g) or (choice == Jelly and jelly_used >= 6 - split_g). Otherwise set void = false.
6. **update** (all players): Set count_glazed to the number of players with choice Glazed and not void, and count_jelly to the number with choice Jelly and not void. Set count_cruller, count_sprinkle and count_plain to the number of players who chose each.
7. **update** (all players): For each non-void player whose donut's count == 1, set gained to that donut's points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), add gained to score and add 1 to donuts. Every other player gets gained 0.
8. **update** (all players): Every player with a non-void Glazed choice adds 1 to glazed_used. Every player with a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded.
9. **tell** (all players): Reveal each player's choice (marked VOID if void), gained, score and donuts. split_g is never shown.
10. **update** (all players): Add 1 to round.
11. **check** (all players): End the game if round >= 10. Otherwise continue with the next round.

## Ending

- ends when: round >= 10
- ranked by: `you.score * 100 + you.donuts` (the highest wins; players level at the top share the win)
- decided by: The highest score wins, with ties broken by most donuts won. Players still level on both share the win, which is a draw among them.

## Choices the source did not make

- Exactly 4 players, suggested 4: The rules fix the table at 4 and the designer chose it. Five donuts for four players makes collisions frequent but avoidable, which is what the game is about.
- Keep simultaneous talk each round, built as a poll and then a broadcast: The rules require it. Players disagree about who should take the high donuts, so talk can be used to bluff about one's remaining budget or to stake claims.
- glazed_used and jelly_used are public: The reveal shows every choice and whether it was void, so these counts can be deduced by anyone. Only split_g stays secret.
- Per-donut counters and the per-player choice, void and gained fields as attributes: The void check, the count and the award need state to work on. These are reset at the start of each round.
- Rank value score * 100 + donuts: This is given by the rules. Donuts can never exceed 10, so the score always dominates the tie-break.

## Simplifications

- The private reminder of picks left is delivered as a sync of each player's own state, with the computed values: The engine sends private state through sync. This has the same effect as the rule's reminder.

## Unsupported (needs engine work)

- none
