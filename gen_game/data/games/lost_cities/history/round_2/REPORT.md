# lost_cities: needs review

Built from the variation **Lost Cities: Three Expeditions** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Use 3 colours (Red, Blue, Green), each with numbers 2-10 and 2 wagers: 33 cards in total. Hands are 6 cards. Play a single deal instead of three. (fixes: P1): This brings the state to 17 attributes and the length to at most 20 rounds, while keeping full colour suits.
- Replace the per-colour discard text fields with one public list attribute, discard_tops. It holds the face-up cards, at most one per colour, and starts as an empty list (never a blank string). Discarding a card of a colour already shown removes the old card from the game and appends the new one. (fixes: P2, P4): A list has no blank fields to print, and keeping only the top card per colour removes the need for stacks.
- Each player's hand is a hidden list attribute, hand, which the engine shows only to its owner as part of their state. Prompts use only {seat} and {value}. (fixes: P3): The hand reaches the player through state the engine already displays, not through an unfillable placeholder.
- Store the just-discarded card in a hidden bookkeeping attribute, last_discard. It starts as the sentinel 'none', is never printed to players, and is reset to 'none' after each draw. (fixes: P7, P2): This enforces the no-retake rule without a blank field appearing in the state.
- Expedition state is held as per-colour numbers: sum, top number, wager count and card count, all starting at 0. (fixes: P1, P2): Numbers starting at 0 never print as blank, and scoring becomes direct arithmetic.
- The game ends at the end of the round in which the deck becomes empty, so both players always get the same number of turns. There is also a cap of 20 rounds. (fixes: P5, P1): This removes the second seat's lost-turn disadvantage and bounds the game's length.
- Rescale scoring. The cost per started expedition is 15. The length bonus is +10 for 5 or more cards. The multiplier stays at 1 plus the number of wagers. (fixes: P6): With about 11 turns each, good columns of 4-6 cards can still score positively, so committing to colours pays.

Objective: When the game ends, the player with the higher score wins. If the scores are equal, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF TABLE for one colour, score = (sum - 15) x (1 + wag), plus 10 if cnt >= 5. No column = 0. {9,10}: sum 19, scores 4 / 8 / 12 with 0 / 1 / 2 wagers. {8,9,10}: 27, scores 12 / 24 / 36. {6..10}: 40, cnt 5, scores 25+10 = 35 / 50+10 = 60 / 75+10 = 85. {2,3,4}: 9, scores -6 / -12 / -18. A lone wage
- playable: pass. Every situation is defined: (1) legal and illegal plays (an illegal play becomes a discard of the first card in hand); (2) discard replacement (the old top is removed from the game); (3) drawing, with last_discard blocked and an invalid answer meaning DECK; (4) an empty deck (take a non-last discard
- reasoning_over_luck: pass. CHANCE: the deal and the deck order set which high cards and wagers each player sees. There is only one scoring round, against three in the original, so variance is notable. I estimate chance decides about 35-45% of games between equally competent players. DECISIONS THAT MATTER: (1) Holding low card

## Complexity

- steps_per_round: designed 13, built 14, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 17, built 43, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 20, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 6 cards each, 21 left in deck, empty discard row
- pass: Seat 1 takes its turn before seat 2, so seat 2 can pick up seat 1's discard
- pass: Playing a higher red number adds it to the red run; lower numbers not offered
- pass: A wager on an empty colour doubles its (negative) score; wager on a started colour not offered
- pass: Illegal plays (low number, late wager) are never offered; the legal play is
- pass: Discarding replaces the same colour's discard and appends to the row
- pass: Drawing from the deck moves one card to hand and lowers deck_size
- pass: Naming a discard top takes it into hand
- pass: Naming the card just discarded draws from the deck instead
- pass: With an empty deck the draw must come from the discard row, excluding one's own discard
- pass: last_discard resets after seat 1's draw, so seat 2 may take seat 1's discard
- pass: Colours with no cards score 0; only the started colour counts
- pass: One wager with numbers totalling 20 scores 10
- pass: Fifth card in an expedition adds the 10-point bonus
- pass: Score is the sum of the three colour scores
- pass: Seat 1 empties the deck, seat 2 still finishes the round, then the game ends
- pass: The game ends after round 20 even with cards left
- pass: Equal final scores are shared

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 8, 'seat 2': 12}, 41-72 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 74.7 decisions, prompts of 147 characters on average (longest 176)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 95% of decided matches against random seats
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- always taking the last option as seat 1 wins 90% of decided matches against random seats
- always taking the last option as seat 2 wins 86% of decided matches against random seats
- random seats: {'seat 1': 28, 'seat 2': 30, 'seats 1 and 2': 2}
- always `first@seat1`: won 57, lost 3, drew 0
- always `first@seat2`: won 52, lost 7, drew 1
- always `last@seat1`: won 53, lost 6, drew 1
- always `last@seat2`: won 50, lost 8, drew 2

## Triage (whose problem each failure was)

- round 1: revise_rules: Four of five attempts failed on the same check. The interface requires the public table attributes discard_red/blue/green/yellow to start as '' to mean 'no card', and the platform flags a public field shown blank as unusable. The coder cannot hide these fields, because players need to see them, and cannot change their starting value without breaking the interface, so the interface itself has to change.
- round 2: fix_game: The tests follow the rules, but the game's setup and draw options are wrong. The trace shows the setup rebuilding the full 33-card deck and dealing again on top of the scenario's given state, and the draw step is never offered 'DECK' or the correct discard-row cards.
- round 2: fix_game: The rules say every draw is a choice the player answers: 'DECK' or the name of an eligible card in discard_tops. The game skips that choice whenever only one option is legal. DECK was never put to Ada when it was the only legal draw, and seat 2 silently 'took R9 from the discard row' without being offered it. Nothing here exceeds the platform; the file resolves the draw step automatically instead of polling.
- round 2: revise_rules: The game is built correctly, but fixed one-option policies beat random play 85-95% of the time from either seat. The likely cause is the scoring: any expedition starts at -15 and wagers multiply losses, so a policy that never opens one (always discarding, or always repeating one kind of answer) sits near 0 while varied play usually goes negative.

## Choices the rules did not make

- Exactly 2 players: The designer fixed 2 players. The game is a duel over a shared discard row: what you discard feeds your one opponent.
- No talk step: The rules have no communication, and the game is a pure two-player contest of hand management and denial.
- Only legal plays are offered: A seat is never offered what it may not do. The fallback rule (an illegal play becomes a discard of the first card in hand) is kept for malformed answers.
- Public deck_size counter: The rules say both players see how many cards remain, while the deck itself stays hidden.
- Public round counter: Needed to apply the 20-round limit arithmetically.
- Strategy at the table: A thoughtful player commits only to colours they can reach 15+ in, times wagers before the numbers, avoids discarding cards the opponent needs, and watches the deck count to judge how much longer the game runs.

## Simplifications

- Taking the top card of the deck is a random pick from the deck list: The deck is shuffled, so a random draw is equivalent and keeps the match seed-reproducible.
- Each seat's turn is written as explicit seat 1 and seat 2 steps: The step list is flat. This keeps both players' turns equal within a round.

## Encoding attempts

- 1: it plays, but part of it does nothing: player attribute `wag_b` is never changed in 3 random matches, so nothing updates it. Steps that name it: seat 1 play resolves, seat 2 play resolves. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; player attribute `wag_g` is never changed in 3 random matches, so nothing updates it. Steps that name it: seat 1 play resolves, seat 2 play resolves. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `fallback` is never changed in 3 random matches, so nothing updates it. Steps that name it: seat 1 play resolves, seat 2 play resolves. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: the game file was refused by the loader: lost_cities: steps[3].do[0].value.calc: "'PLAY' if len([c for c in players[0].hand if 'PLAY ' + c == $p1]) > 0 or $p1[0:4] == 'PLAY' else 'DISCARD'": Slice is not allowed
- 3: passed
