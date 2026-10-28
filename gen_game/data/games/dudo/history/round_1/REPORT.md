# dudo: needs review

Built from the variation **Open-Table Dudo** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Make one round equal one bidding turn, not one hand. A hand continues around the table, wrapping as often as needed, until someone calls Dudo. There is no turn cap and no auto-challenge. New dice are rolled only in a round where a hand ends, using a step with a 'when' condition, so there is at most one random draw per round. (fixes: P1): This restores the original's open horizon. Nobody knows in advance who will face the decisive bid, so risk falls on whoever misjudges the dice, not on a fixed position. Each round has a single choice step, well inside the limits.
- Remove the auto-challenge entirely. A raise is only ever settled if the next player calls it. (fixes: P3): No position gets the 'best of call or raise' privilege, so the 'always raise minimally on the last turn' policy no longer exists.
- Every raise must increase the quantity by at least 1, with any face 2 to 6. A same-quantity raise with a higher face is not allowed. The opening bid must have quantity at least max(1, floor(total dice / 4)). (fixes: P2): Bids reach contested territory within two or three turns, so creeping is impossible and every bidder after the opener carries real risk. It also bounds a hand at most total-dice + 1 turns, which keeps the game within the round limit.
- Keep 'the loser opens the next hand' from the original. Because there is no fixed horizon, opening no longer maps to a fixed hot seat. (fixes: P4): Under an open horizon, the opener's safe first bid is only a mild catch-up help for the player who just lost. It does not decide who loses next, so losses stop rotating mechanically by seat.
- Scale starting dice to the player count: 2 players get 4 dice each, 3 players get 3 each, 4 players get 2 each. Cap players at 4. If 40 rounds pass, the player with the most dice wins and a tie for most dice is a draw. (fixes: P5): A full game needs at most 7 or 8 die losses. At about 3 to 4 turns per hand, that is about 20 to 30 rounds, so the 40-round cap rarely binds.

Objective: The last player with at least one die wins, and every other player loses. If the game ends after round 40 with more than one player holding dice, the player holding the most dice wins. If several players are tied for the most dice, it is a draw among those tied and every other player loses.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Chance that a given die counts for a named face (the face itself or a wild one) is p = 1/3. Two players, T = 8, minimum opening = floor(8/4) = 2. Binomial(8, 1/3) tail probabilities with no private information: P(>=1) = 0.961, P(>=2) = 0.805, P(>=3) = 0.532, P(>=4) = 0.259, P(>=5) = 0.088, P(>=6) = 
- playable: pass. The rules are complete:
- valid opening range [max(1, floor(T/4)), T];
- raise range [q+1, T] with any face from 2 to 6;
- a forced Dudo when q = T;
- invalid actions mapped to defined outcomes;
- the counting rule (bid face plus ones);
- who loses the die;
- elimination and the next opener, includi
- reasoning_over_luck: pass. There is real hidden information: each player sees only their own dice. A player can infer opponents' holdings from the face and quantity of their bids, and can update the binomial estimate (own matching dice plus Binomial(T - own, 1/3)). A player also decides when to switch faces, when to bluff, an

## Complexity

- steps_per_round: designed 16, built 14, limit 20
- choice_steps_per_round: designed 1, built 3, limit 4
- attributes: designed 13, built 30, limit 20 (built: 80)
- hidden_elements: designed 1, built 2, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Two players start with 4 dice each (kept after an opening bid)
- pass: Three players start with 3 dice each (kept after an opening bid)
- pass: Four players start with 2 dice each (kept after an opening bid)
- pass: Each player rolls as many faces as dice (values are chance, only counts asserted)
- pass: Seat 1 opens and acts in round 1
- pass: Opening bid quantity ranges from max(1, floor(9/4)) = 2 to T = 9
- pass: Opener calling Dudo with no bid loses one die
- pass: With a bid of 7 and T = 9 the raise ranges from 8 to 9
- pass: Bid equal to T forces Dudo; count 9 of 9 so the caller loses
- pass: After seat 1 bids, seat 2 acts next and may raise or call
- pass: Ones are wild in the count: 4 fives bid, 2 fives + 2 ones, caller loses
- pass: Count below the bid makes the bidder lose a die
- pass: A player losing their last die is eliminated
- pass: The losing bidder opens the next hand
- pass: An eliminated loser passes the opening to the next surviving seat
- pass: After a hand the bid is cleared, dice reroll and T drops to 8
- pass: Last player with dice wins at once
- pass: Round 40 ends the game; most dice wins
- pass: Round 40 ends with a tie for most dice; tied seats share the win
- pass: Each turn keeps public dice counts and advances the round number

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 4], results {'seat 1': 18, 'seat 2': 12, 'seat 4': 6, 'seat 3': 4}, 6-31 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 13.7 decisions, prompts of 133 characters on average (longest 142)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 90% of decided matches against random seats
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- random seats: {'seat 1': 22, 'seat 2': 38}
- always `first@seat1`: won 54, lost 6, drew 0
- always `first@seat2`: won 53, lost 7, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 26, lost 34, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: With T = 9 the opening quantity may be anything from 2 to 9, so offering 7 on the quantity prompt is correct. The test treats 7 as forbidden, apparently meaning 'face 7 is out of range', but its exclusion is not tied to a particular prompt, and the legal quantity 7 trips it.
- round 1: revise_rules: The game file works as specified, but one fixed choice dominates. Always taking the first option wins about 90% of decided matches from either seat. Always taking the last option (bidding the maximum T) almost always loses. Because raises may jump straight to any quantity up to T, most bids are wildly false, so calling Dudo or making the smallest bid wins without any thought.

## Choices the rules did not make

- 2 to 4 players, suggested 3: The designer suggests 3. The minimum is 2 because one rival is enough to bluff against. The maximum is 4 because the source scales starting dice only that far (2 each at 4 players), and more seats would leave too few dice per player.
- Starting dice written as 6 minus the player count: This matches 4, 3 and 2 for 2, 3 and 4 players, so it holds at every table size.
- No separate talk step: The bids themselves are the communication and bluff. Free talk would add words without a decision the rules contain.
- The opener is offered 'dudo' at an empty table: The source explicitly gives this option and its penalty (the opener loses 1 die).
- Strategy at the table: A thoughtful player estimates expected matches from their own faces plus about a third of unseen dice (ones are wild), raises to a bid they can defend, bluffs when the next player is likely to over-call, and calls Dudo when a bid exceeds a plausible count.

## Simplifications

- Invalid bids cannot be entered: The engine restricts answers to the allowed choices and number ranges, so the source rules 'an invalid bid or raise counts as Dudo / a failed opening' never trigger.
- A bid is asked as three questions: action, quantity, face: Each answer must be a single choice or a single number.
- 'Next surviving seat clockwise' is computed arithmetically over seat numbers and eliminated flags: The engine has no seating operand; this uses the player-attribute comparison workaround.
- Rolling dice is modeled as setting the faces list to random integers from 1 to 6: The engine's seeded randomness stands in for physical dice.
