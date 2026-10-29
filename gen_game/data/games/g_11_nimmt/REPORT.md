# g_11_nimmt: ready for review

Built from the variation **11 Nimmt: Two Hot Piles** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Forced fitting, as in the original 11 Nimmt. You may take a pile only if no card in your hand can be placed on any pile with room. (fixes: P1): This removes the cheap dodge. Whoever holds a fitter must place it, so takes come from running out of fitters or from full piles, as the original intends.
- Two piles instead of one, each capped at 5 cards. Placing a fitting card on a full pile counts as a take. Each turn's choice is a card plus a pile. (fixes: P2): Ten slots fit neither a 3-seat nor a 4-seat cycle, and forced takes from empty hands come irregularly. Who faces two full piles therefore depends on play, not seats. Choosing which pile to feed and which top to leave restores the original's 'play onto any pile' decision.
- Use the two piles to block opponents and to time the full piles. (fixes: P5): Players can steer tops away from what opponents are likely to hold, judged by counting cards. They can also time when piles fill so that someone else is the one forced. This gives card counting something to act on.
- Each bull is worth -2, earned for taking a pile of 3 or more cards. When forced, the player chooses which pile to take and which card restarts it. (fixes: P3): A 5-card pile averages about 6.7 ox, or about 4.7 net of the bull. A 3-card pile is about 4.0, or 2.0 net. A 1-card pile is about 1.3 with no bull. The forced player faces a real choice, and piles do build to 3-5 cards, so bulls happen.
- Penalty comes only from piles you take, and the pile you take is built by everyone. (fixes: P4): A penalty is no longer one predecessor's hand passed on. Who is forced, and when, depends on blocking, timing and the forced player's choice of pile, so play rather than the deal sets the gap.
- Drop the voluntary-take mechanic entirely. Every simple policy is now restricted to fitting plays: always the lowest fitter, always the highest fitter, always pile A, or random. (fixes: P1): The reflex no longer exists. Each remaining fixed policy ignores where the tops will land and who will face full piles, so it can be steered into the forced takes. This was checked case by case in expected_effect.

Objective: The lowest final score (penalty minus twice bulls) wins. If two or more players tie for lowest, the game is a draw among them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PAYOFF TABLE FOR A TAKE (net = pile ox - 2 x bull). The minimum ox is 1 per card. Size 1: ox 1 to 3, no bull, net +1 to +3. Size 2: ox 2 to 6, net +2 to +6. Size 3: ox at least 3, bull, net at least +1 (up to +7). Size 4: net at least +2. Size 5: net at least +3 (5 cards with ox 1 to 3 each: up to 1
- playable: pass. The rules are complete. Fitting is defined arithmetically: d = (c - t) mod N in [1,10]. A collision with d = 0 is impossible because the cards are unique. Room is size < 5. A placement is both fit and room. If any placement exists it is compulsory; otherwise the player takes, choosing any card and e
- reasoning_over_luck: pass. There is substantial inference. With 3 players, 29 of 30 cards are in play: you hold 9, see 2 on the piles, and know the other 19 are split between two opponents plus 1 set-aside card. As cards are played you can narrow down which fits each opponent still holds. You can then fill a pile to 5, or lea

## Complexity

- steps_per_round: designed 18, built 10, limit 20
- choice_steps_per_round: designed 4, built 1, limit 4
- attributes: designed 15, built 59, limit 20 (built: 80)
- hidden_elements: designed 1, built 19, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 9, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: with 3 players each hand holds 9 cards at setup
- pass: R1: with 4 players each hand holds 8 cards at setup
- pass: R2: taking pile [11] costs 3 and taking pile [25] costs 2
- pass: R3: with 3 players each pile starts with 1 card and 1 card is set aside
- pass: R3: with 4 players each pile starts with 1 card and 6 cards are set aside
- pass: R4: every player starts with penalty 0, bulls 0 and score 0
- pass: R5: on top 25, cards 27 and 5 fit and card 6 does not
- pass: R6: a pile of 5 cards is never offered for placement
- pass: R7: a seat holding a placement is offered no take
- pass: R8: a placed card leaves the hand and tops its pile, the other pile unchanged
- pass: R9: a seat with no placement may take with any card on either pile
- pass: R10: taking a 2-card pile adds its ox total and the card starts a new pile
- pass: R11: taking a 3-card pile earns a bull
- pass: R11: taking a 2-card pile earns no bull
- pass: R12: round 1 starts with seat 1, then seat 2 and seat 3
- pass: R13: one round removes exactly one card from each hand
- pass: R14: a 3-player game runs 9 rounds until all hands are empty (seat 1 far ahead)
- pass: R14: a 4-player game runs 8 rounds until all hands are empty (seat 3 far ahead)
- pass: R15: penalty 7 with 2 bulls scores 3
- pass: R16: cards lying in the piles count against nobody
- pass: R17: the lowest final score wins (seat 2 far ahead)

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 1': 10, 'seat 2': 10, 'seat 3': 6, 'seats 2 and 3': 1, 'seats 1 and 2': 4, 'seat 4': 8, 'seats 2 and 4': 1}, 18-30 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 29.5 decisions, prompts of 328 characters on average (longest 345)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 19, 'seat 2': 12, 'seat 3': 17, 'seats 2 and 3': 3, 'seats 1 and 2': 6, 'seats 1 and 3': 3}
- always `first@seat1`: won 17, lost 38, drew 5
- always `first@seat2`: won 9, lost 47, drew 4
- always `last@seat1`: won 23, lost 33, drew 4
- always `last@seat2`: won 15, lost 43, drew 2

## Triage (whose problem each failure was)

- round 1: fix_game: The interface defines `ending_triggered` as true only once some player has emptied their hand. In the 3-player cycle-limit scenario no hand was empty (sizes 3, 2, 2), yet the game set it to True when `cycle` reached `max_cycles` = 12. The game is reusing that flag for the cycle-limit ending, so the test's expectation of False is correct.
- round 1: revise_rules: The game is built and behaves as specified, yet one fixed, thoughtless policy wins about 90% of decided matches and the opposite fixed policy loses nearly every game. The real decisions are degenerate: playing a card off your hand is almost always right, and taking a pile is almost always wrong, so little strategy remains.
- round 2: fix_tests: All four scenarios crash before any rule is checked, because the test `given` blocks set `round`, `current_seat`, `top_a`, `size_a`, `ox_a` and similar names. Those are internal bookkeeping the coder was free to name and organise, not part of the interface, so the failures say nothing about the game's rule logic.
- round 2: fix_game: The R2 test is correct, and the game breaks two rules. Seat 1 held 7 against tops 11 and 25 with N = 30; (7-11) mod 30 = 26 and (7-25) mod 30 = 12, so nothing fits and seat 1 must take, yet the game let it place '7 on A'. Seat 2 then took Pile B [25] and was charged 1 ox instead of 2, which points to an off-by-one in the ox lookup.

## Choices the rules did not make

- 3 to 4 players, suggested 3: The source defines the deck and hand only for 3 and 4 players, and the designer suggests 3. With fewer, there is too little contention over the two piles; the rules define no larger deck.
- No talk step before each turn: The source has no communication phase, and adding one would be adding a mechanic. Play is about hand management: keeping low-risk cards, timing takes while piles are small, and taking a pile of 3 or more cards when the bull's -2 outweighs its ox-heads.
- Card and pile are chosen as one combined option: The rules ask for both together, and a single choice lets the offers enforce the placement-first rule exactly.
- Rank by 2 * bulls - penalty: The engine ranks the highest value first, and the rules want the lowest penalty - 2 * bulls.
- A running score attribute updated every turn: It makes the standing observable and testable during play.

## Simplifications

- The rotating start seat and sequential turns are built as a repeat loop over current_seat with a per-turn update: Each turn changes the piles before the next seat chooses, so each turn's update must run before the next ask.
- Whether a move is a take is worked out at update time by testing if the chosen card fits the chosen pile with room: The offers allow non-placements only when no placement exists, so this test is equivalent to the rule.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'len(you.hand) < hand_size' reads `you` where there is no player
- 2: it plays, but part of it does nothing: game attribute `deck_size` is never changed in 3 random matches, so nothing updates it. Steps that name it: deck and hand size. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `hand_size` is never changed in 3 random matches, so nothing updates it. Steps that name it: deck and hand size. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `ox_multiple_base` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: it plays, but part of it does nothing: game attribute `labels_a` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `labels_b` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `takes_a` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `takes_b` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
