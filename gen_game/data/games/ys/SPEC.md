# Ys: Brokers of the Blind Market

Three brokers secretly favor one gem color each. Over 6 rounds they split 6 influence across Red, Blue, Green and Commerce districts to win gems or points, then vote on prices, with favored gems scoring double at the end.

Players: 3 to 3, best with 3

## Parameters

- `colors` = 3
- `starting_price` = 3
- `rounds` = 6
- `influence_budget` = 6
- `gem_first_award` = 2
- `gem_second_award` = 1
- `gem_tied_first_award` = 1
- `commerce_first_award` = 8
- `commerce_second_award` = 3
- `commerce_tied_first_award` = 3
- `price_rise_per_vote` = 1
- `price_fall_no_votes` = 1
- `price_floor` = 1
- `favored_extra_multiplier` = 1

## Round

1. **update** (all players): round += 1.
2. **tell** (all players): Announce: 'Round {round}. Prices: Red {price_red}, Blue {price_blue}, Green {price_green}.' Also show every player's public gems and commerce_points.
3. **poll** (all players): Every message is broadcast to all once everyone has answered: {"to": "all", "text": "Seat {seat} says: {value}"}. Nothing is stored, and nothing is binding.
4. **poll** (all players): pending_allocation := the choice. It stays hidden until every answer is in.
5. **update** (all players): Parse pending_allocation into alloc_red, alloc_blue, alloc_green and alloc_commerce, then announce all four values for every seat.
6. **update** (all players): Resolve each district D in {red, blue, green} with x = alloc_D. Let M = max of x over the players and N = the count of players with x == M. Let S = max of x over the players with x < M, and K = the count of players with x == S. For each player: if M > 0, x == M and N == 1, then D_gems += 2. If M > 0, x == M and N >= 2, then D_gems += 1. If N == 1, M > 0, S > 0, x == S and K == 1, then D_gems += 1. Otherwise nothing.
7. **update** (all players): Resolve Commerce the same way with x = alloc_commerce: a single first gets commerce_points += 8, each tied-first gets commerce_points += 3, and a single untied second gets commerce_points += 3. A player with 0 influence gains nothing.
8. **poll** (all players): vote := the choice.
9. **update** (all players): votes_red := count of players with vote == 'Red'. votes_blue := count with vote == 'Blue'. votes_green := count with vote == 'Green'. For each color C: if votes_C > 0, then price_C += votes_C; else price_C := max(1, price_C - 1). Announce every seat's vote and the new prices.
10. **update** (all players): When round == 6: revealed_color := favored_color. score := red_gems*price_red + blue_gems*price_blue + green_gems*price_green + (favored_color=='Red' ? red_gems*price_red : 0) + (favored_color=='Blue' ? blue_gems*price_blue : 0) + (favored_color=='Green' ? green_gems*price_green : 0) + commerce_points. Announce every seat's revealed_color and score.
11. **check** (all players): If round >= 6, end the game; otherwise run the round again.

## Ending

- ends when: round >= 6
- ranked by: `you.score` (the highest wins; players level at the top share the win)
- decided by: Each player's standing is their final score: gem values at final prices, favored-color gems counted twice, plus commerce points. The highest score wins. If two or three players tie at the top, they share the result, which is the source's draw.

## Choices the source did not make

- Exactly 3 players, suggested 3: The designer chose 3, and the game has three colors dealt one per player, so it cannot run at any other size.
- Strategy check: A thoughtful player hides their favored color, reads rivals' colors from their allocations and votes, contests gem districts where rivals are thin, takes Commerce when gems are crowded, and steers votes toward their own color without revealing it.
- Keep talk as a simultaneous poll broadcast to all: The rules make talk simultaneous. Talk earns its place because each player wants a different color pumped and can bluff about it, so following a proposal can cost them.
- Allocation as one choice from the 84 valid 'r/b/g/c' splits: The engine takes one answer per question. A list of every valid split enforces the sum of 6 and keeps all four numbers in one simultaneous secret submission.
- Votes stored in a public attribute and announced after the price update: The poll keeps votes hidden until all are in, and the rules show the votes after prices change.
- Score computed in the round-6 update: The final score is needed only once the game ends, and computing it in that step keeps rank_by a single attribute.

## Simplifications

- A tie for highest score is a shared win at the top rather than a separately labeled draw: The engine has no separate draw: players level at the top share the win, which matches the source's draw outcome.
- Allocations are held in pending_allocation and copied to public alloc_* attributes at the reveal: This keeps the submission secret until all are in, then reveals it as the rules require.

## Unsupported (needs engine work)

- none
