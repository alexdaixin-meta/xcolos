# coloretto: ready for review

Built from the variation **Coloretto: Secret Favourites** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Delete 'takers'. The cycle ends when all three players' taken flags are true. (fixes: 'takers' duplicates the number of players whose taken flag is true.): It removes a duplicated attribute.
- Delete 'turn'. The game ends only when cycle reaches 4. (fixes: 'turn' is redundant: the cycle structure already limits the game to 36 turns.): Each cycle has at most 9 placements and 3 takes, so the game is bounded at 36 turns without a counter.
- Replace row_1_open, row_2_open and row_3_open with one table list 'closed_rows'. A row is closed if its number is in the list, and the list is emptied at cycle end. (fixes: Three row_k_open flags store what one closed-rows list can hold.): It saves two attributes and keeps the legality rules identical.
- Delete favourite_pool and favourite_revealed. At game end, Favourites are revealed by an announcement. (fixes: 'favourite_pool' and 'favourite_revealed' have no gameplay use; the reveal can be a plain announcement.): Neither attribute affects play.
- Keep 'score' as a per-player attribute that is written once, at game end, by a single calculation step. (fixes: The attribute count was understated (18 declared, about 22 to 23 actual), which is over the limit of 20.): The winner needs a number to compare, but no running total is kept. The count is then stated honestly as 17.

Objective: After the third cycle, each player's score is computed by the formula. The single highest score wins. If two or more players tie for the highest score, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SCORING ARITHMETIC. T = 0,1,3,6,10,15,21,28 for 0 to 7 cards. score = T(F) + 2·max(o) − Σo + 2·plus2, which equals T(F) + max(o) − (sum of the other three), plus 2·plus2. This matches the description: the Favourite and the largest other colour score positive, the remaining three score negative. Each
- playable: pass. COMPLETENESS.
- Legality of every option is defined: place_k needs row k open and holding fewer than 3 cards; take_k needs row k open and holding at least 1 card.
- Open rows always equal the number of players who have not taken. An open empty row can always be placed into, and a non-empty one can a
- reasoning_over_luck: pass. WHAT THERE IS TO INFER. Each opponent's Favourite is hidden, but their takes and placements reveal it. A player who takes Blue-heavy rows, or keeps feeding Blue into one row, signals Blue.

HOW TO ACT ON IT.
- Hate-placing: put an opponent's off-colours into the row they want, or keep their Favourit

## Complexity

- steps_per_round: designed 11, built 9, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 17, built 37, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 37 cards left in deck after turning up top_card, rows and closed_rows empty, cycle 1
- pass: Setup: 3 Favourites dealt, 2 colours left in pool, none revealed yet
- pass: Tableau counts are updated publicly when seat 2 takes a row
- pass: Only the active seat is asked on a turn
- pass: place_k is not offered for a full row
- pass: place_k is not offered for a closed row
- pass: take_k is offered only for an open row with at least one card
- pass: place_1 adds top_card to row 1 and draws one card from the deck
- pass: take_2 adds the row's cards to the tableau, empties and closes the row
- pass: Last take of the cycle resets rows and increases cycle
- pass: After the cycle ends, the player who just took starts the next cycle
- pass: Turn passes over a seat that has already taken
- pass: The only player who has not taken acts again
- pass: Last player with a full open row can only take it
- pass: Game ends when the third cycle closes
- pass: Favourites are revealed at game end
- pass: Score formula: favourite 4, others 3,1,0,0, one +2 gives 10+2*6-7+2 = 17
- pass: Two tied largest other colours: only one scores positive
- pass: Players tied for the highest score share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seats 1 and 3': 2, 'seats 2 and 3': 2, 'seat 3': 6, 'seat 2': 5, 'seat 1': 5}, 18-28 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 23.0 decisions, prompts of 246 characters on average (longest 247)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 3': 3, 'seats 2 and 3': 3, 'seat 3': 20, 'seat 2': 15, 'seat 1': 15, 'seats 1 and 2': 4}
- always `first@seat1`: won 24, lost 33, drew 3
- always `first@seat2`: won 31, lost 25, drew 4
- always `last@seat1`: won 14, lost 36, drew 10
- always `last@seat2`: won 14, lost 40, drew 6

## Choices the rules did not make

- Exactly 3 players: The designer fixed the table at 3, and the rules tie the 3 rows and 3 distinct Favourites to 3 players, so the minimum and maximum are both 3.
- No talk step: The rules state there is no table talk. The strategy is in reading which colours rivals take, guessing their hidden Favourites, and placing cards that hurt them while hiding your own.
- favourite_pool table list and favourite_shown attribute: These give the dealing of distinct Favourites and the end-of-game reveal a concrete piece of state to act on.
- Score computed only at game end: The rules say scoring happens once, at game end.

## Simplifications

- One engine round is one player's turn, with the active seat tracked in active_seat: The engine runs a flat step list. Turn order, including the same player acting again, is handled by arithmetic on taken.
- A tie for the highest score is shown as a shared win: The engine has no separate draw; players level at the top share the win, which corresponds to the source's draw.
- Shuffling is done as random draws from the deck list: The engine draws at random from a list.
