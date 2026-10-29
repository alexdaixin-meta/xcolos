# Variation: Ys: Brokers of the Blind Market

Three brokers secretly split their influence across three gem districts and a Commerce district each round, then vote to push gem prices. Each broker secretly favors one color whose gems score double, so the game turns on hiding your color while inferring and undercutting the others'.

Players: 3 to 3, best with 3

## Review of the original

Ys is a 2-4 player, 4-round majority game. Players bid brokers to set turn order, then take turns placing valued brokers (0-4), face up or face down, into neighborhood areas and a market grid. Majorities award gems, instant points and character cards, and the market moves gem prices that are scored at the end.

- **non_degenerate**: good. Majorities are contested and placement order matters. No single placement policy dominates, because concentrating loses breadth and spreading loses majorities. Turn order gives some seat edge, but it is bid for.
- **skill_sensitive**: good. Ship and character draws add variance, but bluffing with face-down brokers, reading opponents' commitments and steering gem prices reward skill over 4 rounds.
- **headroom**: good. Deep interplay between majorities, market prices and bluffs. Weak players still collect some gems.
- **reasoning_dependent**: good. Face-down broker values hide state. Players must infer true majorities and opponents' gem interests from partial information.
- **verifiable**: good. Every result is arithmetic: sums of broker values, ranks, gem counts times prices.
- **fits_platform**: bad. It uses a physical board with a market grid (row and column intersections) and 4 neighborhoods of 3 sub-areas each. It has 10 sequential placements per player per round, several decks (ships, market, characters, order cards) and character powers. This far exceeds 4 choice steps per round and 1 random draw per round, and relies on spatial row/column layout.

## Problems

- Ten sequential broker placements per player per round far exceed the choice-step limit.
- The market grid (rows intersecting columns) is a spatial board structure.
- Several random decks per round (ships, market card, characters) exceed one random draw per round and add luck.
- Character cards with special powers create long rule chains and many attributes.
- Face-down brokers create a large amount of hidden state (many hidden elements).
- Turn-order bidding plus sequential placement gives later or earlier seats structural edges that need a tie-break deck.
- The 2-player version reduces to a pure difference contest in which denial dominates.

## Changes

- Replace sequential broker placement with one simultaneous secret allocation: each player splits 6 broker strength among 4 districts. (fixes: Ten sequential broker placements per player per round far exceed the choice-step limit.): Keeps blind majority bidding and its bluff-by-concealment in a single choice step.
- Replace the market grid with a simultaneous market vote: each player names one gem color, each vote raises that color's price by 1, and colors receiving no vote drop by 1 (minimum 1). (fixes: The market grid (rows intersecting columns) is a spatial board structure.): Keeps price manipulation without any row/column structure.
- Remove the ship, market and character decks. Districts always offer fixed rewards. The only randomness is a one-time secret deal of each player's favored color. (fixes: Several random decks per round (ships, market card, characters) exceed one random draw per round and add luck.): Removes per-round luck and keeps random draws at 0 per round.
- Drop character cards. The palace is replaced by a Commerce district that pays flat points. (fixes: Character cards with special powers create long rule chains and many attributes.): Cuts rule chains while keeping a non-gem majority option like Ys's commercial area.
- Use ONE hidden element: each player's secret favored color, whose gems score double. Allocations are revealed after each round. (fixes: Face-down brokers create a large amount of hidden state (many hidden elements).): Bluffing is now about hiding which color you truly want. Opponents must infer it from bids and votes in order to avoid raising your color.
- Make all choices simultaneous and drop turn order. (fixes: Turn-order bidding plus sequential placement gives later or earlier seats structural edges that need a tie-break deck.): Removes seat advantage and the tie-break deck.
- Fix the player count at 3, one secret color per player, with colors dealt as a random permutation. (fixes: The 2-player version reduces to a pure difference contest in which denial dominates.): Three players mean a rival's gain is not purely your loss. Symmetric types mean no player is dealt a better type.

## Kept from the original

- Blind majority bidding of broker strength across neighborhoods
- Top ranks in each neighborhood earn colored gems
- A commercial majority that pays instant points
- A market that players push to change gem values scored at the end
- Bluffing about which gems you really want
- End scoring of gems times market price

## The variation's rules

SETUP: There are three gem colors: Red, Blue and Green. Each color's price starts at 3. Before round 1, the three colors are dealt randomly, one to each player, as that player's SECRET FAVORED COLOR. Every player has a different color, and each player knows only their own. All players start with 0 gems of each color and 0 commerce points. The game lasts 6 rounds.

EACH ROUND:
1. Announce. The round number and the current prices of Red, Blue and Green are shown to all.
2. Talk. Everyone writes one short message at the same time without seeing the others. All messages are then shown. Talk is not binding.
3. Allocate (simultaneous, secret). Each player submits four whole numbers, each 0 or more, summing to exactly 6: their influence in the Red district, the Blue district, the Green district and the Commerce district.
4. Reveal. All allocations are shown to everyone.
5. Resolve each of the four districts separately:
   - If one player has the strictly highest influence (above 0), they win FIRST. Otherwise, all players tied at the highest value (above 0) each count as tied-first.
   - If there is a single first, the player with the strictly next-highest influence (above 0) wins SECOND. Second is not awarded if there is a tie for it, or if first was tied.
   - In a gem district, a single first gains 2 gems of that color, second gains 1 gem, and each tied-first gains 1 gem.
   - In Commerce, a single first gains 8 commerce points, second gains 3, and each tied-first gains 3.
   - A player with 0 influence in a district gains nothing there.
6. Market vote (simultaneous). Each player names one color: Red, Blue or Green.
7. Price update. Each color's price rises by 1 for every vote it received. Each color that received 0 votes falls by 1, but never below 1. The votes are then shown.
8. End check. After round 6 the game ends.

FINAL SCORING: Each player's score is the sum over the three colors of (gems of that color × that color's final price). Then add (gems of their secret favored color × that color's final price) again, so favored gems count double. Then add their commerce points. Secret colors are revealed at the end.

Objective: The player with the highest final score wins. If two or three players tie for the highest score, the game is a draw.

Expected effect: Players disagree about which gem prices should rise, because each secretly wants their own color high and the others' low. Talk therefore invites bluffing ('Blue is worth pushing'), and a player who just follows a proposal may raise a rival's favored color, handing that rival the win. Heavy, obvious investment in one color reveals your type and invites rivals to contest that district at a tie (6 vs 6) or starve its price with their votes. Concealing is not free either: spending on decoy colors or Commerce costs gems. Simple policies can all lose. 'All 6 on my color' is tied and denied by a rival and its price is starved. 'Always Commerce' caps out near 48 points against gem totals that can exceed it. 'Always vote my color' reveals the color. Types are symmetric, so the deal decides what to do, not who is ahead.

## Complexity (the designer's count, against the limits)

- steps_per_round: 12 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 10 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
