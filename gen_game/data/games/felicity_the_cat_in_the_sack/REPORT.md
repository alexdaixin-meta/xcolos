# felicity_the_cat_in_the_sack: needs review

Built from the variation **Cat in the Sack: Paid Entry** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Staying costs a non-refundable entry fee of 1 mouse, paid when STAY is chosen. Losing stayers receive no consolation. Droppers receive 2 mice. (fixes: P1): A losing stayer now ends the round 3 mice behind a dropper (-1 against +2). Staying only pays when the chance of winning a good sack at a good price justifies it. DROP is not dominant either: if everyone else drops, a lone stayer wins at price 1 and nets V-2 against 2, which is better whenever V > 4.
- The stay/drop decision comes after the first reveal and the talk, and the entry fee makes it a real gamble. (fixes: P2): The revealed cards and the rivals' claims now decide whether paying to enter is worth it.
- Exact reveal counts are stated for every player count. With 3 players: 1 card in the first reveal, 1 in the second, 1 hidden. With 4 players: 2, then 1, with 1 hidden. With 5 players: 2, then 1, with 2 hidden. (fixes: P3): Removes the ambiguity, and every player count keeps at least one hidden card at bidding time.
- A player needs at least 2 mice to stay (1 for the fee and at least 1 to bid). Otherwise they must drop. (fixes: P4): Keeps the fee-plus-bid rule consistent. Always-STAY-bid-1 now bleeds 1 mouse per lost round and ends far behind.

Objective: After round 8 the player with the highest total (cat points plus mice) wins. If totals are tied, the tied player with the most cat points wins. If that is also tied, the game is a draw among those players.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Card pool per hand: cats -8-5+3+5+8+11+15 = 29, plus Rabbit 0 and Dog 0. One random card is removed, expected value 29/9 = 3.2, leaving about 25.8 per player over 8 placed cards. With 3 players, each holding a Dog 8/9 of the time, about 2.7 Dogs reach the sacks. A lone Dog removes the top cat, rough
- playable: pass. Rules are complete:
- Same 9 cards each, minus 1 removed, gives 8 cards for exactly 8 rounds, so the last placement is forced.
- The minimum mice to stay (2) covers the fee plus the minimum bid, so mice never go negative.
- Winner ties are defined: fewer current mice (after the fee), then seat order
- reasoning_over_luck: pass. Sources of chance:
- The removed card shifts a hand's total from 14 (15 removed) to 37 (-8 removed). But cards go into shared sacks, so this changes your options more than your score.
- The shuffle decides which cards are seen before stay/bid. With 3 players, 1 of 3 cards is seen before stay and 2 o

## Complexity

- steps_per_round: designed 15, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 13, built 46, limit 20 (built: 80)
- hidden_elements: designed 3, built 11, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 setup: every hand starts from the same 9 cards, one is removed at setup and one is placed in round 1, so 7 remain (count only; which cards go is random)
- pass: R2 setup: exactly one card removed per hand, so after placing one card in round 1 each hand holds 7 (count only, the cards are random)
- pass: R3 setup: 15 mice and 0 cat points each (all drop in round 1: 15+2=17 mice, cat points stay 0)
- pass: R4 round 1 has start seat 1
- pass: R4 round 2 has start seat 2
- pass: R5 the placed card leaves the hand
- FAIL: R6 with 3 players: 1 card at the first reveal plus 1 at the second gives 2 revealed | rule R6 is broken: After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them.; game revealed_cards: expected ['rabbit', 'rabbit'], got ['rabbit', 'rabbit', 'rabbit']; game revealed_cards: expected 2 items, got 3
- FAIL: R6 with 5 players: 2 cards at the first reveal plus 1 at the second gives 3 revealed | rule R6 is broken: After shuffling, the first reveal shows 1 sack card with 3 players and 2 sack cards with 4 or 5 players, without naming who placed them.; game revealed_cards: expected 3 items, got 5
- pass: R7 the talk step does not block the round (messages are not binding and change nothing)
- pass: R8 a seat with 1 mouse may only DROP
- pass: R9 STAY costs 1 mouse (lone stayer bids 1: 15-1-1=13)
- pass: R10 DROP gains 2 mice and the seat is not asked to bid
- FAIL: R11 one more card is revealed after stay-or-drop (4 players: 2+1=3) | rule R11 is broken: After stay-or-drop, one more sack card is revealed to everyone.; game revealed_cards: expected ['rabbit', 'rabbit', 'rabbit'], got ['rabbit', 'rabbit', 'rabbit', 'rabbit']; game revealed_cards: expected 3 items, got 4
- pass: R12 the bid range runs up to the mice left after the fee (5-1=4)
- FAIL: R13 the highest bid wins | rule R13 is broken: When bids differ, the highest bidder wins the sack.; seat 1 bid: expected 3, got 1; seat 1 mice: expected 14, got 13; seat 1 cat_points: expected 0, got 16; seat 2 bid: expected 5, got 1; seat 2 mice: expected 9, got 14; seat 2 cat_points: expected 16, got 0; game winner_seat: expected 2, got 1
- pass: R14 on a tied bid the seat with fewer mice wins
- pass: R15 on a tie in bid and mice, the first seat from start_seat wins (round 2, start seat 2 beats seat 1)
- pass: R16 when nobody stays, nobody wins and nobody pays
- pass: R17 a lone stayer wins and pays its bid
- pass: R18 sack value is the sum of the cats, rabbit worth 0 (15+3-5=13)
- pass: R19 one dog cancels the top cat (cat_15+cat_3+dog+rabbit=3)
- pass: R20 two dogs have no effect (cat_15+dog+dog+rabbit=15)
- pass: R21 the winner pays its bid and adds a negative sack value (5 + -10 = -5)
- pass: R22 losing stayers keep the 1-mouse fee paid and gain nothing
- pass: R23 sack cards are added to the public discard
- pass: R24 the game ends after round 8
- pass: R25 tied totals: the seat with more cat points wins
- pass: R25 equal totals and equal cat points share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 3': 13, 'seat 1': 9, 'seat 2': 10, 'seat 4': 5, 'seat 5': 3}, 73-135 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 109.0 decisions, prompts of 179 characters on average (longest 269)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 20, 'seat 1': 18, 'seat 2': 22}
- always `first@seat1`: won 19, lost 41, drew 0
- always `first@seat2`: won 25, lost 35, drew 0
- always `last@seat1`: won 21, lost 39, drew 0
- always `last@seat2`: won 21, lost 39, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: Step 11 reveals all remaining sack cards and step 14 discards them face up, so at the end of the round `revealed_cards` correctly holds the whole sack (3 cards with 3 players, 5 with 5). The tests check the round's final state but expect only the first and second reveals, which misreads the rules.
- round 1: fix_game: In all three failing scenarios the scripted bids (for example seat 1 bidding 3) never reached the game; every stayer ended up bidding 1, the minimum. The resulting winners, mice and cat points all follow from those wrong bids, and the game's other bookkeeping (fee of 1, sack value 8, tie broken by seat order) is consistent with them. The bid step is mis-built: it does not offer or accept the full numeric range the rules require.
- round 1: fix_tests: In all three failing scenarios the game applied the rules correctly to the moves it actually received: the fee was paid, the drop payment made, the tie-breaks by fewer mice and then seat order worked, and the sack was valued correctly. The tests' scripted bids (for example 3 for seat 1) were never applied, every stayer fell back to the default minimum bid of 1, and the expected mice, cat_points and winner_seat were all computed from bids that were never placed.
- round 1: fix_tests: Step 11 reveals every remaining sack card, and step 14 discards the whole sack face up, so after a round has fully finished every placed card has been shown. The game's revealed_cards holding the whole sack (3 of 3, 5 of 5, 4 of 4) is consistent with the rules; the R6 and R11 tests read that list after the round ended, when only the first and second reveals had been counted. In R13 both stayers bid 1, which looks like the scripted bids of 3 and 5 never matched a bid the game offered, so the game fell back to the minimum. That points at how the test scripted its moves, not at the winner logic: with equal bids of 1 the tie-break correctly gave seat 1 the sack.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4 and the source allows 3 to 5. 3 is the minimum because an auction needs rivals and the sack needs enough unknown cards to hide one's own. 5 is the maximum because the hand and reveal structure is built for 5, and with more seats one's own card would barely affect the sack.
- Talk kept as a simultaneous poll with broadcast: The source specifies simultaneous non-binding messages. Players disagree about the sack, since each wants others to drop or to overbid, so bluffing about one's placed card gives the others something to reason about.
- Cards encoded as text labels cat_<value>, rabbit and dog: The rabbit and dog are both worth 0 but behave differently, so a label is needed to count dogs.
- Cat card values listed as separate parameters cat_value_1 to cat_value_7: Each parameter must be a single number.
- Sack winner computed as one key: bid * 100000 - mice * 100 - seat offset from start_seat: This puts the source's three-level tie-break (bid, fewer mice, seat order from the start player) into a single arithmetic maximum.
- Ranking expression (mice + cat_points) * 1000 + cat_points: Cat points can never reach plus or minus 500, so the total is compared first and cat points break ties. Exact ties share the win, which is the source's draw.
- Stay/drop choices and bids are public once revealed: The source reveals bids together, and paying the fee or receiving the drop payment is visible. Who placed which card stays secret.
- Strategy at the table: A thoughtful player infers others' cards from the public discard, the reveals and their own removed card. They bluff in talk and weigh the 1-mouse fee against the 2-mouse drop payment. They also use the fewer-mice tie-break and the dog rule when sizing a bid.

## Simplifications

- The shuffle is done by drawing the sack cards at random into a new order: The engine shuffles by random draws from a list.
- The bank of mice is not tracked: It is unlimited, so only player mice change.
- A draw is represented as a shared win among the players tied at the top: The engine has no separate draw outcome.
