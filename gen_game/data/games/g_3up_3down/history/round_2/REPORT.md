# g_3up_3down: needs review

Built from the variation **3Up Shed (Equal Turns)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Equal turns: reaching 0 cards no longer ends the game mid-round. Every remaining seat finishes the round. At round end, all seats with 0 cards share the win, and two or more such seats make a draw. (fixes: P1 Seat edge): Turning the race into 'fewest turns needed' gives every seat the same number of turns, so move order no longer decides ties in turn count.
- Rotate the lead: in round r, the order is seat L, L+1, L+2 (wrapping), with L = ((r-1) mod 3)+1. (fixes: P2 Seat 1 opening advantage): This spreads the lead, and the free plays onto a fresh pile that come with it, across all seats.
- Remove players_out. The end check uses each seat's out flag directly. (fixes: P3 Unused attribute): The state should hold only what the game uses.
- Keep the counted 30-card deck, the band-symmetric deal and the single-play Clear, with no blind cards and no draw pile. (fixes: P4 Original luck and complexity): This keeps luck low and the step count small.

Objective: If the game ends because game_over is true, every seat with cards_left = 0 wins. If exactly one seat has 0 cards, it wins alone; if two or three do, the game is a draw. If round 20 ends with nobody out, the seat with the fewest cards_left wins, and a tie for fewest is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. TURN EQUALITY: R3 only sets game_over after all three turns of a round, so every non-out seat gets exactly one turn per round. When several seats go out in the same round the result is a draw. Seat leads over 20 rounds: seat 1 leads rounds 1,4,...,19 (7 times), seat 2 leads 2,5,...,20 (7 times), sea
- playable: pass. COMPLETENESS: every situation is covered.
- Source: hand first, then up_pile.
- Legal set: r >= top_rank as 1-3 copies, or a single C, which is always legal.
- PICK UP happens only when no play is legal. With top_rank = 0 everything is legal, so an empty-pile pickup cannot happen.
- Run counting wor
- reasoning_over_luck: pass. CHANCE SOURCES: there is one shuffle, constrained so that every seat gets 3 cards per band plus 1 C.
- The main luck is the number of pairs and triples, worth about 0 to 2 turns of tempo.
- There is no draw pile and no blind cards, so after setup there is no further randomness.
- Estimated chance sh

## Complexity

- steps_per_round: designed 15, built 8, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 15, built 45, limit 20 (built: 80)
- hidden_elements: designed 1, built 14, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 20, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- FAIL: After setup each seat holds 7 in hand and 3 up, cards_left 10, and every stack is empty | rule R1 is broken: When setup is done, each seat has hand_count 7, up_count 3 and cards_left 10. Its 10 dealt cards were 3 Low (1-3), 3 Mid (4-6), 3 High (7-9) and 1 C.; seat 1 hand: expected 7 items, got 10; seat 1 up_pile: expected 3 items, got 0; seat 2 hand: expected 7 items, got 10; seat 2 up_pile: expected 3 items, got 0; seat 3 hand: expected 7 items, got 10; seat 3 up_pile: expected 3 items, got 0
- FAIL: The chosen up set of 3 cards moves from hand to up_pile (only counts asserted, the deal is random) | rule R2 is broken: When a seat picks its up set at setup, then exactly those 3 cards move from hand to the public up_pile, and an invalid or missing pick takes the first set of up_offer.; seat 1 hand: expected 7 items, got 10; seat 1 up_pile: expected 3 items, got 0; seat 2 hand: expected 7 items, got 10; seat 2 up_pile: expected 3 items, got 0; seat 3 hand: expected 7 items, got 10; seat 3 up_pile: expected 3 items, got 0
- pass: Round 2 is led by seat 2, so the order is 2, 3, 1
- pass: With an empty hand a seat plays from up_pile; with a hand it plays only from the hand
- pass: With top_rank 5, a held 3 is not offered: the first option is 6, and C is offered
- pass: With an empty pile, any held rank is offered, even 9, and so is C
- pass: A seat holding only cards below top_rank and no C is offered only PICK UP
- FAIL: Playing the same rank as the top adds to run_count | rule R8 is broken: When a seat plays k cards of rank r and top_rank was already r, then run_count increases by k; otherwise run_count = k. In both cases top_rank = r.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: Playing a higher rank resets run_count to the copies played | rule R8 is broken: When a seat plays k cards of rank r and top_rank was already r, then run_count increases by k; otherwise run_count = k. In both cases top_rank = r.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: A third 5 in a row wipes the pile | rule R9 is broken: When run_count reaches 3 or more after a play, then pile is emptied out of the game, top_rank = 0 and run_count = 0.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: Playing C removes it and the whole pile | rule R10 is broken: When a seat plays a C, then the C and the whole pile leave the game, top_rank = 0 and run_count = 0.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: Picking up moves the whole pile into the hand and resets the pile | rule R11 is broken: When a seat picks up, then every card of pile goes into its hand, pile becomes empty, picked_up increases by 1, top_rank = 0 and run_count = 0.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: Counts are recomputed after each turn and a seat with no cards left is out | rule R12 is broken: When any turn ends, then hand_count, up_count and cards_left = hand_count + up_count are recomputed, and cards_left = 0 sets out = true.; seat 1 up_count: expected 0, got 3; seat 1 cards_left: expected 0, got 3; seat 1 out: expected True, got False
- FAIL: An out seat is skipped and asked nothing | rule R13 is broken: When a seat has out = true, then it is skipped: it is asked nothing and its attributes do not change.; the match crashed: FlowError: 'out' is not a declared status
- FAIL: Lead seat 3 goes out in round 3, seats 1 and 2 still play their turns, then the game ends | rule R15 is broken: When a round's three turns end with at least one seat out, then game_over = true and the game ends after that round, so every seat has had the same number of turns.; winner: expected 'seat 3', got 'seat 1'; seat 1 standing: expected -2, got 0; seat 3 standing: expected 0, got -4; seat 1 cards_left: expected 2, got 0; seat 2 picked_up: expected 1, got 2; seat 3 cards_left: expected 0, got 4; seat 3 out: expected True, got False; game round: expected 3, got 5
- pass: Round 20 ends the game with nobody out; the fewest cards wins
- pass: Two seats tied for fewest cards at round 20 share the win
- FAIL: Two seats going out in the same round share the win | rule R17 is broken: When the game ends, then the seats with the lowest cards_left win, and seats tied at the lowest share the win.; winner: expected 'seats 1 and 2', got 'seat 3'; seat 1 standing: expected 0, got -6; seat 2 standing: expected 0, got -4; seat 3 standing: expected -4, got 0; seat 1 out: expected True, got False; seat 2 out: expected True, got False; seat 3 out: expected False, got True; seat 3 cards_left: expected 4, got 0; game round: expected 1, got 5

## Does the file follow the spec's shape? (flags for a person)

- rule R14 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 5, 'seat 2': 9, 'seat 1': 4, 'seats 1 and 2': 2}, 16-42 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 46.0 decisions, prompts of 299 characters on average (longest 311)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 16, 'seat 2': 21, 'seat 1': 20, 'seats 1 and 2': 2, 'seats 2 and 3': 1}
- always `first@seat1`: won 19, lost 37, drew 4
- always `first@seat2`: won 17, lost 37, drew 6
- always `last@seat1`: won 1, lost 58, drew 1
- always `last@seat2`: won 2, lost 57, drew 1

## Triage (whose problem each failure was)

- round 1: fix_game: After the deal each seat's hand holds 10 cards, but hand_count, up_count and cards_left all stay at 0. The game never updates the public counts. It also never moves 3 cards into up_pile when the Up-pile choice is declined or missing, so no seat ends setup with 3 up and 7 in hand. The rules are clear and the platform can express this, so the fault is in the file.
- round 1: fix_game: The game crashes with a CalcError: `you.hand[0]` is read on an empty hand, a fault in the file and not in the rules. The setup also never finishes the simultaneous Up-pile choice: after setup every seat still holds 10 cards in hand and an empty up_pile, although the rules make that choice part of setup.
- round 1: fix_game: The rules put choosing the Up pile in SETUP (step 5), so after setup every seat must hold 7 Hand cards and 3 public Up cards. The game dealt the cards and built the Up-pile offers, but it never moved any cards: hands stayed at 10 and Up piles at 0. The tests check results the rules clearly require (counts and pile sizes), not internal bookkeeping.
- round 2: fix_game: Under rule S6, setup must end with hand_count = 7, up_count = 3 and cards_left = 10. With rounds = 0 the game dealt the hands and listed up_offer, but it never applied the up-set choice and never set the counts (hand_count stayed 0). The later scenarios also show wrong up_pile and hand_count values, which suggests setup work is spilling into round 1 or the counts are not recomputed after each play.
- round 2: fix_game: After setup every seat still holds 10 cards in hand and 0 up. The engine built up_offer, but the simultaneous up-set pick (S4) and the move into up_pile (S5) were never applied, and hand_count, up_count and cards_left were not set to 7/3/10 (S6). Setup is part of the rules before round 1, so the tests are right to expect it to finish even with rounds: 0, and the later play-source and legal-play failures follow from the same broken bookkeeping.
- round 2: fix_game: Two scenarios crash with "FlowError: 'out' is not a declared status". The game file treats the interface attribute `out` as an engine status, which is a coder error. The setup scenarios also end with each hand still at 10 cards and an empty up_pile, so the up-set choice (S4–S5) never moved any cards before play.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3. Rotating the lead over 3 seats and the equal-turns ending are built for that count.
- No talk step before turns: The source has no talk. Turns are sequential and fully specified, so adding talk would add a mechanic.
- rank_by = 0 - cards_left for both endings: A seat that is out has cards_left 0, the lowest possible. Ranking by fewest cards therefore picks exactly the out seats when game_over is true, and the fewest-cards seat at round 20.
- C sorts as 10 in up_offer: The source says C counts above 9, so a numeric stand-in of 10 keeps the ordering.

## Simplifications

- A shared top rank is a shared win: The engine has no separate draw. The source's draw (two or three seats out, or a tie for fewest at round 20) becomes a shared win among the tied seats.
- The turn rotation is described as 'each player in turn starting at seat lead': The step list is flat. The three turns are one ask over the seats in rotated order, each followed by its update, with out seats skipped.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `rank_list` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
