# cockroach_poker: needs review

Built from the variation **Roach Bluff** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- At most one pass per card. A receiver who passes peeks, then sends the card with a new claim to a player who is neither the original sender nor themselves. That final receiver must call true or false. (fixes: The unbounded pass chain needs a variable number of choice steps per round. The engine cannot branch into repeating blocks.): This keeps the peek-and-pass double bluff but fits into a flat list of 4 choice steps, using `when` conditions on the pass steps.
- Use 24 cards: 4 creatures (Roach, Rat, Fly, Toad), 6 copies each. Collecting three of one creature face-up loses. (fixes: 64 cards with 8 creatures and four-of-a-kind to lose makes games too long, with too much state for the step and attribute budgets.): Games last about 8–20 rounds and the state stays small. Card counting stays tractable but non-trivial.
- When a player loses, the game ends immediately. Among the other players, the one with the fewest face-up cards wins. If several tie for fewest, the game is a draw. (fixes: The game names only one loser. The engine must declare a winner or a draw, so the outcome among the survivors is undefined.): The winner is decided by arithmetic. Players must avoid cards all game, not just avoid the losing set, which rewards consistent good calls throughout.
- Restrict play to 3–4 players and drop the 2-player mode. (fixes: The 2-player variant removes passing and plays almost like a pure guessing game. Wide player counts (2–6) make balancing hard.): With at least 3 players, passing is always possible and targeting has meaning. Fewer counts are easier to balance.

Objective: When the game ends, the player who triggered the end (three of one creature face-up, or no card to send) loses. Among all other players, the one with the fewest total face-up cards wins. If two or more of them tie for fewest, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF OF ONE CALL. Here q is the chance that the latest claim is true. From the judge's side:
- TRUE: correct with probability q, so the claimer takes the card; wrong with probability 1-q, so the judge takes it.
- FALSE: correct with probability 1-q, so the claimer takes it; wrong with probability 
- playable: pass. COMPLETENESS:
- Every branch is defined: TRUE/FALSE/PASS, a single pass, and a forced final call.
- Who judges is defined: the latest claimer is judged.
- Who takes the card and who sends next are defined.
- End checks: 3 of a kind, or a taker with an empty hand.
- In 3 players, the post-pass receiv
- reasoning_over_luck: pass. WHAT TO INFER:
- All 24 cards are dealt and the composition is public (6 of each creature). Your own hand of 6 or 8 cards plus the revealed face-up cards let you card-count. Example: holding 3 Roaches in 3 players leaves 3 of 6 Roaches among 16 unseen cards, so P(a given unseen card is a Roach) = 3/

## Complexity

- steps_per_round: designed 17, built 16, limit 20
- choice_steps_per_round: designed 4, built 7, limit 4
- attributes: designed 14, built 32, limit 20 (built: 80)
- hidden_elements: designed 2, built 12, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: 4 players: each seat is dealt 6 cards and the whole deck is dealt
- pass: 3 players: each seat is dealt 8 cards and the whole deck is dealt
- pass: At start every face-up count is 0
- pass: Seat 1 sends first: only seat 1's hand shrinks in round 1
- pass: Sent card leaves the hand and hand_size drops by 1
- pass: Sender may claim a creature it does not hold and cannot choose itself as receiver
- pass: Only the chosen receiver is asked to respond to the claim
- pass: TRUE on a true claim resolves against the sender's claim: sender takes
- pass: Passer makes a new claim to a seat that is neither sender nor itself
- pass: After a pass the final receiver may not pass again; a wrong FALSE makes it take
- pass: Correct FALSE on a bluff: claimer takes the card
- pass: Wrong FALSE on a true claim: judge takes the card
- pass: Taker becomes the next sender and its counts rise
- pass: Third face-up Roach makes the taker lose and ends the game
- pass: Next sender with an empty hand loses
- pass: Among non-losers the fewest face-up cards wins
- pass: The game ends after round 24

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seats 1 and 2': 5, 'seat 3': 7, 'seat 1': 8, 'seat 2': 12, 'seat 4': 3, 'seats 2 and 4': 2, 'seats 3 and 4': 2, 'seats 2, 3 and 4': 1}, 22-99 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 58.7 decisions, prompts of 117 characters on average (longest 209)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seats 1 and 2': 15, 'seat 3': 11, 'seat 1': 11, 'seat 2': 20, 'seats 1 and 3': 2, 'seats 2 and 3': 1}
- always `first@seat1`: won 4, lost 53, drew 3
- always `first@seat2`: won 2, lost 55, drew 3
- always `last@seat1`: won 20, lost 31, drew 9
- always `last@seat2`: won 21, lost 36, drew 3

## Triage (whose problem each failure was)

- round 1: revise_rules: The game is built correctly and behaves as specified, but the design needs 7 choice steps per round against a limit of 4. Those steps are the sender's card, claim and receiver, the receiver's response, then the passer's new claim, new receiver and the final judgment. That is a flaw in the rules, not in the file.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer set 4 as the suggested size. At least 3 players are needed so that a pass can reach someone who is neither the sender nor the passer. The deck of 24 only deals evenly to 3 or 4 players, so the maximum is 4.
- No talk step: The rules forbid table talk; the claims are the only communication. Players reason by reading the face-up piles and by bluffing with claims that target a near-loser.
- Rank expression 0 - faceup_total - 1000*lost: This makes the loser rank below everyone, and among the rest the fewest face-up cards ranks highest.
- Pass steps run as individual steps with a 'when passed' condition: Each pass step is a single step with an arithmetic condition, not a chosen block, so the engine supports it directly.

## Simplifications

- A tie for fewest face-up cards is a shared win rather than a draw: The engine has no separate draw outcome; players level at the top share the win.
- Sending is split into three questions: the card, then the claim, then the receiver: Each engine question takes a single answer. The card choice is kept private to the sender.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (claim, last_revealed, response) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (claim, last_revealed) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
