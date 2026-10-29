# big_two: needs review

Built from the variation **Little Two** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a 30-card deck numbered 1 to 30. Card number = 3 × (rank − 1) + suit, with ranks 1 to 10 (rank 10 plays the role of the 2s) and suits 1 to 3. Every comparison is then a comparison of numbers. (fixes: P6): Rank and suit order become plain arithmetic, so no lookup table is needed.
- Allow only singles, pairs, triples and three-card runs. A triple may also be played as a bomb on any single or pair. (fixes: P1): This keeps the core tension of Big Two (whether to break a combination, when to bomb) with short legality checks.
- Play with exactly 3 players, 9 cards each and 3 cards left face-down unseen all deal. (fixes: P2): Deals are short enough to fit three into 40 orbits. Card counting becomes reasoning under uncertainty rather than exact elimination.
- Play a match of 3 deals with an exact penalty per deal. The lowest total penalty wins. (fixes: P3, P4): Averaging over deals and penalising every card left rewards damage control with a weak hand, not only winning with a strong one.
- The first lead of deal 1 goes to seat A, deal 2 to seat B and deal 3 to seat C, instead of to the holder of the lowest card. (fixes: P5): Each seat gets the opening tempo exactly once.
- Add an exact extra penalty for 2s (rank 10) left in hand and double the penalty for a hand of 7 or more cards. (fixes: P4): This turns the original's gambling flavour into exact arithmetic and punishes hoarding and passivity.

Objective: The player with the lowest total penalty after the match ends wins. If two or three players tie for the lowest total, the match is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. CARD ARITHMETIC CHECK: rank = floor((c+2)/3). Card 1 gives rank 1, card 3 gives rank 1, card 4 gives rank 2 and card 30 gives rank 10. Suit = c - 3(rank-1) gives 1, 2 or 3. So there are 10 ranks of 3 cards, and the three 'twos' are cards 28, 29 and 30. Each player gets 9 cards and 3 are set aside.


- playable: pass. COMPLETENESS: the rules cover all of the following.
- Each combination kind and its value (the highest card number).
- Which plays beat which: same kind and higher value; a triple bombs a single or a pair; a run is beaten only by a higher run; a triple only by a higher triple.
- Forced leads, and re
- reasoning_over_luck: pass. SOURCES OF CHANCE: the deal decides who holds the twos and the complete triples (bombs), plus the 3 hidden aside cards. With only 3 deals, variance is meaningful. I estimate chance decides about 40-50% of match results between equal players.

SKILL LEVERS:
(a) Hand partitioning: splitting 9 cards in

## Complexity

- steps_per_round: designed 14, built 17, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 17, built 37, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- FAIL: R1: cards 13 and 14 share rank 5 and form a pair, 14 and 16 do not | rule R1 is broken: When card c is ranked, then rank = floor((c+2)/3) (1-10) and suit = c - 3*(rank-1) (1-3); e.g. card 14 has rank 5, suit 2.; seat 1 card_count: expected 2, got 3
- pass: R2: a deal gives 9 cards to each seat and puts 3 aside; passing seats keep 9
- pass: R3: in deal 2 seat B leads and seat A does not act in the first orbit
- pass: R3: in deal 3 seat C leads and seats A and B do not act in the first orbit (they still hold 9 after passing next orbit)
- pass: R4: on an empty pile the leader may not pass and must play
- FAIL: R5: on a single the seat may pass or play a higher single, not a lower one | rule R5 is broken: When the pile is not empty, then the acting player may pass or play the same kind with a higher value (highest card number).; seat 1 card_count: expected 2, got 3; seat 3 card_count: expected 2, got 1
- FAIL: R6: a low triple bombs a high pair | rule R6 is broken: When a triple is played on a single or a pair of any value, then it is legal (a bomb) and pile_kind becomes triple.; seat 1 card_count: expected 1, got 4; seat 3 card_count: expected 3, got 2
- FAIL: R7: on a triple only a higher triple may be played | rule R7 is broken: When a triple is on the pile, then only a triple with a higher value may be played on it.; seat 1 card_count: expected 4, got 7; seat 3 card_count: expected 3, got 2
- FAIL: R8: on a run only a higher run may be played, and ranks 9-10-1 are no run | rule R8 is broken: When a run is on the pile, then only a run with a higher value may be played on it; runs are three consecutive ranks without wrap, so ranks 9-10-1 are not a run.; seat 1 card_count: expected 3, got 6; seat 3 card_count: expected 3, got 2
- FAIL: R9: a pair must share a rank (4 5 yes, 5 7 no) | rule R9 is broken: When a pair or triple is played, then all its cards must share a rank; e.g. 4,5,6 is a triple of rank 2 and 4,5 is a pair of rank 2.; seat 1 card_count: expected 2, got 3
- FAIL: R10: legal plays leave the hand and lower card_count | rule R10 is broken: When a legal play is made, then the cards leave the player's hand, card_count drops by the number played, pile_value becomes the highest card, last_player becomes that seat, and the cards are announced to everyone.; seat 2 card_count: expected 2, got 3; seat 2 hand: expected 2 items, got 3
- FAIL: R11: a seat that passed may play on its next turn in the same trick | rule R11 is broken: When a player passes, then they may still play on their next turn in the same trick.; seat 1 card_count: expected 2, got 3; seat 2 card_count: expected 2, got 3; seat 3 card_count: expected 2, got 1
- pass: R12: when play returns to the last player the pile clears and they must lead
- pass: R15: playing the last card wins the deal with no penalty and skips the others
- pass: R16: non-winners take card_count plus 1 per card 28-30
- pass: R17: a non-winner holding 7 or more cards takes double penalty
- pass: R18: when orbit 40 ends mid-deal everyone is penalised and the match ends
- pass: R19: the end of the third deal ends the match
- pass: R20: seats tied for the lowest penalty share the win

## Does the file follow the spec's shape? (flags for a person)

- rule R13 has no scenario: nothing checks it
- rule R14 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 2, 'seats 2 and 3': 1, 'seats 1, 2 and 3': 1, 'seat 1': 4, 'seats 1 and 3': 5, 'seats 1 and 2': 3, 'seat 3': 4}, 61-72 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 75.0 decisions, prompts of 128 characters on average (longest 129)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 11, 'seats 2 and 3': 5, 'seats 1, 2 and 3': 3, 'seat 1': 15, 'seats 1 and 3': 8, 'seats 1 and 2': 5, 'seat 3': 13}
- always `first@seat1`: won 15, lost 29, drew 16
- always `first@seat2`: won 11, lost 36, drew 13
- always `last@seat1`: won 15, lost 29, drew 16
- always `last@seat2`: won 11, lost 36, drew 13

## Triage (whose problem each failure was)

- round 1: fix_game: The game encodes multi-card combinations as concatenated numbers (the pair 13+14 is offered as 1314). That form is ambiguous (123 could be 1+23 or 12+3) and unreadable to the model players, and it is why every test's option for a pair, triple or run ('13 14', '4 5 6', '13 14 15', '10 13 16') was never matched. The rules and tests are consistent: 13 and 14 do form a pair, 4-5-6 is a rank-2 triple, and 10-13-16 is a run of ranks 4-5-6.
- round 1: fix_tests: After seat 2 played 22, seats 3 and 1 both passed, so by the clearing rule the pile was cleared and seat 2 had to lead. Its lead of 3 was legal and emptied its hand, so the game correctly gave card_count 0 and ended the deal. The test wrongly assumed the pile still held 22, making '3' illegal and treating it as a pass.
- round 1: fix_game: In R1 seat 1 sent the move '13 14', which the game itself offered as a pair. The game recorded 'played 13', removed only one card and set the pile to single 13. Multi-card combinations are being parsed or applied wrongly, and the same fault shows in the pair, triple and bomb scenarios (R5, R6, R7).
- round 1: fix_game: In R1 the game offered '13 14' and seat 1 chose it, yet only card 13 left the hand and the pile became a single of 13. The file is resolving a multi-card answer to its first card. The same miscount (seat 1 keeps too many cards, so the pile and the later seats' plays are wrong) explains the R5, R6 and R7 failures, and the tests match the rules.

## Choices the rules did not make

- 3 players (min = max = suggested = 3): The designer fixed 3 seats. The deal arithmetic (3 x 9 + 3 aside = 30) and the A-B-C rotation only work at 3.
- Strategy at the table: A thoughtful player tracks played cards and opponents' public card counts, saves triples as bombs, and passes to keep control, while sheding high-penalty cards (twos, a big hand) before someone goes out.
- No talk step: The source has no talk. It is a competitive individual game, so messages would add words without anything to agree on.
- Turns use ask, one seat at a time: The rules give a fixed turn order, and each player must see the current pile.
- Answer as free text listing card numbers: The set of legal combinations changes every turn. Free text plus the illegal-play-as-pass rule covers it faithfully.
- Seats numbered A=1, B=2, C=3: This lets the leader and last_player be compared arithmetically.

## Simplifications

- Play legality is checked by a judged referee step: Validating combination membership, rank equality, runs and kind/value comparison against the pile is too complex for single arithmetic operations. The resulting state changes are still arithmetic.
- Deal-start steps (shuffle, deal, reset) are separate flat steps each carrying the same 'when' condition: The engine has no conditional blocks. Each step is individually guarded instead.
- Lowest penalty wins is expressed as rank_by = 0 - penalty, and a tie at the top is a shared win: The engine ranks highest-wins and treats a tie at the top as shared. The source's 'draw' becomes a shared result.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (last_action, last_action, last_action); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: it plays, but part of it does nothing: game attribute `all_cards` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `labels` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
