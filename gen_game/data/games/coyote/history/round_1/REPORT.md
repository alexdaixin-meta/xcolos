# coyote: needs review

Built from the variation **Coyote Lap** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Each hand is one round with exactly one lap of bidding. The opener declares, then each other player in clockwise order either raises or calls Coyote, once each. If nobody calls, the opener is automatically treated as calling Coyote on the final declaration. (fixes: P1): This bounds a hand at 4 choices while keeping the declare-or-call tension. The last responder can still dump the risk on someone else by raising only when confident, which keeps the late-position decision meaningful.
- The blue specials are replaced by one special card, 'Max→0': if it is in play, the highest other card counts as 0. (fixes: P2): This keeps Coyote's signature twist, which players can see and reason about because everyone else sees the card. It removes all post-bidding draws and reshuffles, so the outcome depends on reading, not on late luck.
- The game is a fixed 12 hands, and the opener rotates clockwise every hand, so each seat opens equally often (3 times with 4 players, 4 times with 3). Coyote tokens are counted and fewest tokens wins, instead of elimination. (fixes: P3): Every player holds every position (opener, middle, last responder) equally often, so no seat has an edge. The length is fixed and short.
- Elimination is dropped and the game ends after hand 12. (fixes: P4): This gives a bounded game length, and all players stay active and informative to the end.
- The player count is set to 3 or 4. (fixes: P5): The bidding lap fits within 4 choices, and there are enough visible cards to give real inference.

Objective: After 12 hands, the player with the fewest Coyote tokens wins. If two or more players tie for the fewest, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. DECK CHECK: 1+2+3+(4x5)+3+2+1+1 = 33 cards. Numeric sum = -10-10+0+4(1+2+3+4+5)+30+30+20 = 120, so the mean card is 3.75. E[x^2] = (100+50+220+300+450+400)/32 = 47.5, so the variance is 33.4 and the SD is about 5.8.

RANGE OF THE TRUE TOTAL T: maximum with 4 players is 20+15+15+10 = 60. Minimum is -
- playable: pass. COMPLETENESS:
- The deal, private visibility of others' cards, the opening range, the raise bounds (strictly higher, at most 60) and the stop on CALL are all specified.
- The auto-call by the opener is defined.
- Resolution covers both the caller case and the auto-call case.
- Max->0 is fully specif
- reasoning_over_luck: pass. SOURCE OF CHANCE: in each hand, a player's own card is unknown, with SD about 5.8 around a mean of 3.75 from that player's view. An uninformed estimate of T therefore has SD about 6.

INFERENCE CHANNEL: other players see your card, and their declarations encode it. Example with 3 players, where O se

## Complexity

- steps_per_round: designed 12, built 15, limit 20
- choice_steps_per_round: designed 4, built 7, limit 4
- attributes: designed 15, built 34, limit 20 (built: 80)
- hidden_elements: designed 1, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start of game: 0 tokens, hand 1, opener seat 1
- FAIL: Each of 3 players is dealt 1 card from the 33-card deck, leaving 30 (cards are random, so only counts are checked) | rule R2 is broken: When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck.; game deck: expected 30 items, got 33
- FAIL: Each of 4 players is dealt 1 card, leaving 29 in the deck | rule R2 is broken: When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck.; game deck: expected 29 items, got 33
- pass: Hidden cards are dealt and a hand still resolves: a call against -30 always costs the caller (any deal totals at least -20)
- pass: The opener may declare from -30 to 60 and becomes current_declarer
- pass: A raise must be above current_declaration and at most 60; the raiser becomes current_declarer
- FAIL: At a declaration of 60 the responder can only call, and with 3 players the total never exceeds 50, so the declarer loses | rule R6 is broken: When current_declaration is 60, a responder is offered only call_coyote.; Blaise: the rule for 'raise' was never matched (the game never put that option to this seat)
- pass: After a responder calls Coyote, no later responder acts
- pass: When everyone raises, the opener calls automatically, and loses on -28 since any deal totals at least -20
- pass: Total of 3 cards never exceeds 50 (plain sum or with Max to 0), so declaring 51 loses whatever the deal
- pass: With or without Max to 0 the total stays at most 50 for 3 players: a raise to 55 loses whatever the deal
- pass: The total is never below -20 (including Max to 0 with negative cards), so calling on -20 costs the caller whatever the deal
- pass: true_total below the declaration: the declarer takes a token (60 with 3 players)
- pass: true_total at or above the declaration: the caller takes a token (-25 always met)
- pass: At hand end the seat taking the token is recorded and announced
- pass: The opener moves clockwise and wraps from seat 3 to seat 1
- pass: After the 12th hand the game ends; level seats share the win
- pass: Fewest tokens wins at the end
- pass: Tied for fewest tokens share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 2': 11, 'seats 1, 2 and 3': 3, 'seat 3': 2, 'seats 1 and 3': 4, 'seat 1': 8, 'seats 2 and 3': 2, 'seats 2 and 4': 2, 'seat 4': 4, 'seats 3 and 4': 2, 'seats 1 and 2': 2}, 30-60 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 41.8 decisions, prompts of 146 characters on average (longest 205)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 21, 'seats 1, 2 and 3': 6, 'seat 3': 12, 'seats 1 and 3': 4, 'seat 1': 14, 'seats 2 and 3': 2, 'seats 1 and 2': 1}
- always `first@seat1`: won 19, lost 35, drew 6
- always `first@seat2`: won 19, lost 32, drew 9
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: Every failing scenario fails the same way: a responder was never offered the option 'raise'. The tests that only use 'call_coyote' and the opener's numeric declaration pass, so the game's response step is missing the RAISE choice the rules require (or names it differently), and later seats never get to raise.
- round 1: fix_tests: The game handled a declaration of 60 correctly. No raise is possible, so seat 2 was recorded as caller, the true total of 19 was below 60, and seat 1 (the declarer) took the token, exactly as the rules require. The test failed only because it demands that seat 2 be shown a menu holding the single forced option. Skipping a choice that has only one possible answer is legitimate and changes no result or score.
- round 1: fix_tests: The game deals 1 card per player from the 33-card deck correctly: the trace shows the deck going from 33 to 30 during the hand. It then returns the cards after resolution, so after a full round the deck is back at 33, ready for the next hand's fresh shuffle. The deck-count tests read internal bookkeeping at a moment the rules don't pin down. The 60-declaration test relies on an option literally named 'raise', a name the interface never defines; the game takes raises as numeric bids.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer suggests 4, so it is kept. 3 is the minimum because with fewer players there is too little hidden information to reason about and no chain of raises. 4 is the maximum the source allows, and more responders would push declarations past what the deck can support.
- Max→0 is stored as the code 100 in card: Cards must be numbers so the total can be computed. 100 is never a face value, so the code is unambiguous, and the reveal shows it as 'Max→0'.
- No free-talk step before the bidding: The source has no table talk. Information is carried by the declarations themselves, and adding talk would add a mechanic.
- Strategy at the table: Each player sums the cards they can see and estimates their own unseen card from the deck odds, watching for a visible Max→0. They then read the other players' declarations as signals about their own card. A thoughtful player raises only when the expected total supports it, and calls when the current bid outruns what they see.

## Simplifications

- The clockwise response sequence is written as fixed responder slots (responder 1, 2 and 3 relative to the opener), each a raise-or-call choice followed by a number step for raises: The engine runs flat step lists. Per-slot steps with when-conditions interleave the choice and the amount for each responder in order.
- A tie for the fewest tokens is a shared win rather than a declared draw: The engine's ranking makes players level at the top share the win. This matches the source's draw outcome in effect.
- The deck is reset and redealt with random draws each hand: Shuffling is modelled as drawing at random from the deck list.
