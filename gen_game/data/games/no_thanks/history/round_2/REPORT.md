# no_thanks: needs review

Built from the variation **No Thanks! (Bounded Laps)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Each round is at most one lap of offers on the current card. If everyone pays, lap_count goes up by 1. After laps_to_burn = 2 full all-PAY laps, the card is burned (removed from play unscored), its pot stays in the middle for the next card, and the lead seat moves one place clockwise. The deck has 20 cards, so the game lasts at most 20 x 2 = 40 rounds. (fixes: P1): This bounds the game length while keeping 'pay to refuse' tension. The pot carried over from a burned card makes the next card more tempting.
- The player count is set to 3-4. (fixes: P2): A lap is then at most 4 sequential choice steps.
- The rules now state the order of operations exactly. Offer step k goes to the k-th seat clockwise from lead_seat, and its only condition is that a card is current (current_card is not 0). TAKE is always offered. PAY is offered only if the seat has at least pay_cost chips. The draw step runs only when current_card is 0. The end-of-lap step runs only if the card is still current after all offers. When lap_count becomes 1, nothing else changes: same card, same pot, same lead seat. (fixes: P3): This removes the conditions that suppressed the offers after the first all-PAY lap. The tests written from the rules (R1-R4, R11) are correct and match these rules.
- The rules use one lap parameter, laps_to_burn = 2, plus pay_cost = 1. Both are stored as game attributes. (fixes: P4): Removing the redundant parameter leaves a single, unambiguous burn condition.
- Card points are updated incrementally when a card c is taken: add c, subtract (c+1) if c+1 is already in the tableau, and subtract c if c-1 is already in the tableau. (fixes: P5): This always equals 'sum of the lowest card of each run' and needs only membership checks and one arithmetic update. Example: holding 10 and 12, then taking 11, gives 11 - 12 - 11 = -12, so the points go from 22 to 10, which is correct.
- Whoever takes a card becomes lead_seat. The rest of that round's offers are skipped. The next round draws a new card and offers it to the taker first. (fixes: P6): This keeps the original 'taker decides first on the next card' as a clean between-round rule.

Objective: Each player's final score is card points minus remaining chips. The single player with the lowest final score wins. If two or more players tie for lowest, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. TAKE update check: adding c with only c+1 held gives c-(c+1) = -1, which is correct because the run's lowest card drops from c+1 to c. With only c-1 held it gives c-c = 0, correct. With both held, two runs a..c-1 and c+1..b merge with lowest a, so the change should be -(c+1); the formula gives c-(c+
- playable: pass. The rules cover every state:
- DRAW happens only when no card is current.
- The offer order is defined from lead_seat.
- PAY is gated on chips, so a seat with no chips must TAKE.
- After a TAKE no further offers are made.
- The lap counter has explicit branches for lap 1 and lap 2.
- The pot carry-o
- reasoning_over_luck: pass. Chance enters through the deal order and the 13 removed cards, which make runs uncertain. Skill matters in several ways:
- Valuing pot against card, roughly take when pot ≥ c minus run savings.
- Tracking opponents' chips from announced history, to know who is forced to take.
- Predicting who will d

## Complexity

- steps_per_round: designed 12, built 10, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 13, built 26, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck holds 20 cards, removed holds 13
- pass: Setup: each player starts with 11 chips, empty tableau, 0 card points
- pass: Setup: no card on offer, empty pot, nothing burned
- pass: Round start with no card draws the only deck card and keeps the pot
- pass: Round start with a card already on offer draws nothing
- pass: A seat with chips is offered both TAKE and PAY
- pass: Paying costs 1 chip and raises the pot by 1
- pass: Taking 11 between held 10 and 12 merges the runs
- FAIL: Taker collects the pot and no further offers are made | rule R8 is broken: When a seat TAKEs, then its chips rise by the pot, the pot becomes 0, current_card becomes 0, lead_seat becomes that seat, and no further offers are made that round.; Dara: the rule for 'TAKE' was never matched (the game never put that option to this seat)
- FAIL: Offers go clockwise from the lead seat (lead 3: 3, 4, 1) | rule R9 is broken: When offer k is made, then it goes to the seat k-1 places clockwise from lead_seat, for k = 1..N, and only while current_card != 0.; Blaise: the rule for 'TAKE' was never matched (the game never put that option to this seat)
- pass: A seat with 0 chips may only TAKE
- pass: First full lap of pays keeps the card and grows the pot
- pass: Second full lap burns the card, keeps the pot, and the next round starts at seat 2
- pass: Game ends when the deck is empty and the last card is taken
- pass: Game ends after round 40 even with cards left
- pass: Chips left in the pot at the end belong to no one
- pass: Lowest final score (card points minus chips) wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 4], results {'seat 3': 10, 'seat 1': 9, 'seat 2': 13, 'seat 4': 8}, 30-47 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 38.3 decisions, prompts of 130 characters on average (longest 130)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 1 wins 97% of decided matches against random seats
- always taking the last option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seat 3': 24, 'seat 1': 16, 'seat 2': 20}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 58, lost 2, drew 0
- always `last@seat2`: won 60, lost 0, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: In three scenarios the game never actually put a PAY/TAKE choice to the seats: 'moves played' is empty, yet seat 1 ended up holding card 20 with offer ['TAKE']. So the offer step is being resolved inside the file instead of being presented as a real choice. The rules are clear and the engine supports sequential choices, so this is an implementation error.
- round 1: fix_game: The test follows rule 5: after a lap where everyone pays, the card stays current and the next round offers it again from the same lead seat. The game never offered TAKE to the scripted seats in that next round, so the second lap is not being run correctly.
- round 1: fix_game: The test matches the rules: after a full lap of PAYs with lap_count becoming 1, the card stays current and is offered again starting at lead_seat. The game never offered TAKE to Ada or Cleo, so it does not run that second offering round correctly.
- round 2: fix_tests: The game did what the rules require: seat 1 had 0 chips, could not PAY, and ended up taking the card. Its tableau became [10], it collected the pot (chips 0 -> 2) and current_card returned to 0. The test failed only because it expected seat 1 to be shown a choice containing TAKE. With a single legal option the move can be resolved without a poll ('moves played' is empty), which gives the same outcome.
- round 2: fix_game: The rules say TAKE is offered to every seat whenever current_card is not 0. In three separate scenarios the game never offered TAKE to the seat in question, including a 0-chip seat whose only legal option is TAKE. So the offer steps in the file are mis-built; the tests and rules are not the problem.
- round 2: fix_game: The rules say TAKE is always offered to each seat while a card is current. In both failing scenarios the game never put TAKE to a seat that the rules say should get an offer, so the take path, and probably the offer order from lead_seat, is missing or wrongly gated in the file. The tests that only use PAY pass, which points at the TAKE option and its offer order rather than at the tests.

## Choices the rules did not make

- 3 to 4 players, suggested 4: The designer's count is kept. Three seats is the smallest table where pressing your luck against several rivals is tense. Four keeps each lap short and each refusal costly.
- No talk step: The rules contain no table talk. The strategy is when to pay to drive up the pot and when to take a card that extends a run; adding talk would add a mechanic.
- Tie-break by shared win: Players level at the top share the win, which is the engine's form of the source's draw.
- chips marked observable: The final score depends on chips, so an outside observer must read them, though players see only their own.

## Simplifications

- Lowest score wins, expressed as ranking by chips - card_points (highest wins): The engine ranks highest first, so the score is negated.
- card_points kept incrementally on each take instead of recomputed from runs: The incremental formula in R5 equals the sum of the lowest cards of each run, and it is simple arithmetic.
- Four fixed offer steps, the fourth skipped when N = 3: The step list is flat; each offer is one ask step with an arithmetic condition.
- A round_number counter was added: It enforces the 40-round bound stated in the rules.

## Encoding attempts

- 1: passed
