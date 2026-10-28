# hogwash: ready for review

Built from the variation **Hogwash: Six Ranks** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Use ranks 1-6 with 4 copies each (24 cards, 8 per player). The required rank in round r is ((r-1) mod 6)+1, so seat 1 always faces ranks 1 and 4, seat 2 faces 2 and 5, and seat 3 faces 3 and 6. (fixes: P1): Each player holds on average only about 2.7 cards of their two ranks. Roughly two-thirds of every hand can only leave through bluffs, which opponents must read by card counting (only 4 copies of each rank exist).
- Drop the early-end checks. The game always lasts exactly 24 rounds, so each seat is active 8 times and answers 16 claims. (fixes: P3): This removes the timing that favoured seat 3 and gives every seat the same number of turns and responses.
- Restore the original stakes. A caught bluffer takes the whole pile; a wrong lone challenger takes the whole pile. If two players wrongly challenge, the pile is shuffled and split evenly between them, with any odd card removed from the game. (fixes: P4, P5): Challenging becomes a real gamble whose cost grows with the pile. Seat order no longer decides who takes which cards.
- Remove the 'unchallenged bluff makes trusters take a card' rule. Trusting never adds cards; unchallenged bluff cards simply stay hidden in the pile. (fixes: P5): Trust and Challenge become a genuine read of the claimant, as in the original, and false information accumulates in the pile.
- Add a tiebreak for fewest cards: first, most correct challenges (bluffs caught); then, fewest times caught bluffing; draw only if still tied. (fixes: P2, P6): Players who reach 0 are separated by their reading skill, and a player at 0 still has a reason to keep making risky challenges.

Objective: After round 24, the player holding the fewest cards wins. If several players tie for fewest, the one with the most CATCHES wins. If still tied, the one with the fewest CAUGHT wins. If still tied, the game is a draw among those players.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. STRUCTURE. The active player's only choice is k. The engine picks the cards, so a play is TRUE exactly when the player holds at least k cards of the required rank. Challengers choose Trust or Challenge.

CHALLENGER PAYOFFS (change in your own hand; pile size P includes the k cards just played):
| Yo
- playable: pass. RULES ARE COMPLETE.
- The seat and rank formulas are checked: r=1 gives seat 1 rank 1, r=4 gives seat 1 rank 4, r=24 gives seat 3 rank 6.
- Card selection is deterministic: required rank first, then the next rank up, wrapping 6 to 1.
- k is capped at hand size, and a 0-card player skips.
- All three
- reasoning_over_luck: pass. CHANCE ENTERS THREE WAYS.
- The initial deal: own-rank count has mean 2.67 and standard deviation about 1.1.
- Which cards arrive in pile pickups.
- The 6(c) shuffle.

SKILL ENTERS SEVERAL WAYS.
(a) Choosing k. Truth requires holding at least k, and honest k leaks your count, so choosing between k =

## Complexity

- steps_per_round: designed 11, built 16, limit 20
- choice_steps_per_round: designed 2, built 3, limit 4
- attributes: designed 16, built 34, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: at setup each seat holds 8 cards and the deck is empty
- pass: R2: at setup pile_size is 0 and all catches and caught are 0
- pass: R3: round 4 has seat 1 active with rank 4 (true play of 4,4 trusted)
- pass: R3: round 6 has seat 3 active with rank 6
- pass: R4: active seat with 0 cards is skipped, no k asked, no poll, nothing moves
- pass: R5: choosing k=4 with 2 cards plays only 2
- pass: R6: required-rank cards are played first, so 5,5 from {1,6,5,5} is true and the lone challenger takes the pile
- pass: R7: playing 1,2 when rank 1 is required is a bluff, so the challenged player picks up the pile
- pass: R7: playing 1,1 when rank 1 is required is true, so the challenger takes the pile
- pass: R8: playing k=3 lowers hand_size by 3 and raises pile_size by 3
- pass: R9: the active seat makes a claim of k cards (only the play is checked; the text is not observable)
- pass: R10: both non-active seats are polled, including a seat holding 0 cards; the active seat is not polled
- pass: R11: a single challenge resolves the play (the reveal itself is not observable)
- pass: R12: a bluff challenged by both makes the bluffer take the pile; caught +1 and each challenger's catches +1
- pass: R13: a true play challenged by one player gives that challenger the whole pile, with no counters changed
- pass: R14: a true play challenged by both on a pile of 7 gives each challenger 3 cards and removes 1
- pass: R15: when both players Trust, even a bluff stays in the pile and no hands change
- pass: R16: the trusting player gains no cards when the other player challenges a true play
- pass: R17: after a round the public counters reflect the round's outcome
- pass: R18: the game ends after round 24 (seat 3 empties its hand and wins)
- pass: R19: with equal hand_size and equal catches, fewer caught wins
- pass: R19: seats level on cards, catches and caught share the win
- pass: R19: fewest cards wins outright over more catches

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 7, 'seat 1': 5, 'seat 3': 8}, 76-96 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 93.3 decisions, prompts of 260 characters on average (longest 330)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 19, 'seat 1': 19, 'seat 3': 22}
- always `first@seat1`: won 7, lost 53, drew 0
- always `first@seat2`: won 9, lost 51, drew 0
- always `last@seat1`: won 34, lost 26, drew 0
- always `last@seat2`: won 38, lost 22, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built correctly, but the design fails evaluation on two counts. A round has 6 choice steps against a limit of 4, and a thoughtless 'always take the first option' policy wins about 77–80% of its games from either seat while 'always take the last option' loses about 75–80%, so a trivial strategy dominates.
- round 2: fix_tests: In the final state seat 2 has hand_size 1, catches 2 and caught 1. The required formula gives 0 - 10000 + 200 - 1 = -9801, which is exactly what the game reported, so the game is right and the test's expected -9901 is an arithmetic error.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. The rank schedule (each seat facing two fixed ranks, 8 turns each) and the split rule for two challengers depend on exactly 3 seats, so neither the minimum nor the maximum can move.
- No all-players talk poll before the Trust/Challenge poll: The source gives only the active player one public statement. Adding free talk would add a mechanic; the bluffing lives in the claim and the statement.
- The statement is a separate ask after k: Each question takes one answer type, so the number and the text are asked in two steps by the same seat.
- Ranking expression -hand_size*10000 + catches*100 - caught: Catches are at most 24 (times 100 is under 10000) and caught is at most 8 (under 100), so the weights reproduce the strict tie-break order: fewest cards, then most catches, then fewest caught.
- Strategy at the table: A thoughtful player tracks how many of each rank have been revealed, picked up or must still be out, judges whether a claim of k is plausible, and weighs taking the pile against letting a rival shed cards. They also choose when an honest play invites a costly challenge, and use the statement to mislead.

## Simplifications

- The k cards are chosen by a fixed engine rule rather than by the player: The source already specifies this; it is carried out as remove/append operations on hand, played and pile.
- Shuffling and splitting the pile are random draws from the pile list: The engine shuffles by drawing at random, which gives the same result.
- The draw among tied players is a shared win: The engine has no separate draw; players level at the top share the win.
