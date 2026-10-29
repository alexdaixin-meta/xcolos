# yaniv: ready for review

Built from the variation **Row Yaniv** (design round 3); see VARIATION.md.

## What was changed from the original, and why

- When a shed card matches other slots, every other slot with the same value is also shed and stays empty. A triple sheds all three. (fixes: P1: Three of a kind on shedding is undefined.): Gives one unambiguous rule for pairs and triples.
- Shuffle once per hand, not every round. Deal from a running draw pile. Keep a public dead pile of every card that has left play this hand. If the draw pile cannot serve every player, that round's showdown is forced. (fixes: P2: The deck is re-shuffled full every round with held cards included.): Players can count the 54-card deck. They can infer what remains in the pile and what opponents hold from what they kept. There is still at most one random event per round, and no mid-hand reshuffle is needed.
- Replace the single upcard with an offer row. It holds all cards shed in the previous round, numbered in order. Each player may TAKE one card from it by position. Conflicts are resolved in rotating priority order, and a player who loses a conflict draws blind. Unclaimed offer cards go to the dead pile. (fixes: P3: Only one public takeable card exists.): Taking becomes a public, informative choice. It shows what you are collecting, for example pairs or low cards. It can deny an opponent the card they need, and it forces guesses about who else wants the same card.
- Raise the Yaniv threshold to 10. Extend the match to 24 rounds. End early when any total reaches 50 after a showdown. (fixes: P4: Hands last too long relative to the match.): Hands end in about 3 to 5 rounds, giving roughly 5 to 7 showdowns. Luck averages out, and the end total actually comes into play.
- Remove the bid. Rotate priority every round. Allow only 2 to 4 players with 24 rounds, a number divisible by 2, 3 and 4. (fixes: P6: The tie-break priority is shared unequally between seats; P7: The bid sub-game adds steps but mostly reduces to bidding 0 or 1.): Over a full match every seat gets priority equally often. Removing the bid frees steps for the offer row.
- The overall combination: counting, a choice of takeable cards, readable sheds and more showdowns. (fixes: P5: When everyone plays the obvious heuristic, the shuffle alone decides the winner.): Among heuristic players the draw still matters. A player who counts low cards, tracks what opponents took and times Yaniv against an opponent's likely total beats a fixed heuristic over 5 to 7 showdowns.

Objective: When the match ends, the player with the lowest penalty total wins. If two or more players share the lowest total, the match is a draw among them.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. DECK ARITHMETIC: The values sum to 0x2 + 4x(1+...+9) + 10x16 = 0 + 180 + 160 = 340. The mean card is 340/54 = 6.30, and P(10-value) = 16/54 = 0.296. A fresh 3-card hand averages about 18.9.

P(dealt H<=10), estimated with replacement:
- No zeros: ordered triples of 1..9 summing to 10 or less = sum o
- playable: pass. COMPLETENESS:
- Every phase is specified: deal, announce, a simultaneous 3-part poll, validity check, shed with pair/triple removal, priority-ordered TAKE with conflict fallback to DRAW, DRAW, row update, and showdown with explicit caller and non-caller formulas.
- Caller tie handling is explicit. N
- reasoning_over_luck: pass. CHANCE SOURCES:
- The deal: about 8% per player of an immediate legal call, and in that case the hand is decided by the deal.
- The hidden draws: mean 6.3, 30% chance of a 10.

SKILL SOURCES:
(a) Shed choice: dump the highest card, or a pair or triple to shrink the hand. A pair of 9s removes 18 poin

## Complexity

- steps_per_round: designed 15, built 17, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 15, built 47, limit 20 (built: 80)
- hidden_elements: designed 2, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 new hand deal: 3 players, all DRAW, the draw pile ends at 54-9-1-3 (chance cannot change these counts)
- pass: R2 new hand empties a leftover dead pile (only the untaken row card is dead after round 1)
- pass: R2 new-hand flag switched off: no redeal in round 2, so the draw pile is 47-2-2 (chance-proof)
- pass: R3 an empty slot counts as nothing in H (round 24 showdown)
- pass: R4 YANIV with H=11 is invalid and treated as DRAW
- pass: R4 YANIV with H=10 is valid and leads to a showdown
- pass: R5 a valid YANIV stops all card movement, even another seat's TAKE
- pass: R6 a pair sheds 2 cards and a triple sheds 3
- pass: R7 an empty chosen shed slot sheds the lowest non-empty slot instead
- pass: R8 two TAKEs on the same position: the priority seat (2) gets it, seat 1 draws
- pass: R9 taken and drawn cards go into the shed slot; the slot emptied by a pair stays empty
- pass: R10 the draw pile drops by 1 per draw and not for a TAKE
- pass: R11 untaken row cards go dead and the new row is the shed cards from seat 1 up
- pass: R12 showdown when the draw pile falls below the number of players
- pass: R12 no showdown when the draw pile still holds as many cards as players
- pass: R13 both call: the lowest caller scores 0 (N=99), the other caller scores H+20
- pass: R13 Asaf: a caller tied by a non-caller scores H+20
- pass: R14 non-callers score 0 at or below M and their H above it
- pass: R15 showdown without a caller: everyone tied for the lowest H scores 0
- pass: R16 showdown scores add to the existing totals and the next round deals a fresh hand
- pass: R17 the priority seat moves from 1 to 2, so seat 2 wins round 24's TAKE collision
- pass: R18 the match ends after a showdown that pushes a penalty to 50 or more
- pass: R18 the match ends after round 24 even with every penalty below 50
- pass: R19 players tied for the lowest penalty share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 4], results {'seat 2': 15, 'seat 1': 14, 'seat 4': 6, 'seat 3': 4, 'seats 1 and 4': 1}, 36-288 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 156.0 decisions, prompts of 208 characters on average (longest 249)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 34, 'seat 1': 26}
- always `first@seat1`: won 38, lost 21, drew 1
- always `first@seat2`: won 35, lost 25, drew 0
- always `last@seat1`: won 28, lost 32, drew 0
- always `last@seat2`: won 19, lost 41, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The R3 test is consistent with the rules: seat 1 calls with the strictly lowest sum 7 and scores 0, while seats 2 and 3 score 8 and 20. The game ignored the preset hands: the trace shows it building the shoe and value tables and dealing fresh 5-card hands at the start of round 1, so seat 1 never held [3,4] and was never offered CALL. R4–R6 fail the same way, with totals coming from re-dealt random hands.
- round 1: fix_game: The R3 test agrees with the rules: seat 1 at sum 7 calls and is strictly lowest, so it scores 0, and seats 2 and 3 score 8 and 20. The game ignored the scenario's given hands and dealt fresh 5-card hands inside round 1 (seat 1 got [10,10,6,6,10], sum 42), so CALL was never offered. R4 to R6 fail the same way, because the dealt hands overwrite the given ones.
- round 1: fix_game: Several independent scenarios show the game file breaking clear, buildable rules. Discard offers are never put to other seats as claim options. The round-40 final showdown leaves every total at 0. The illegal-choice fallback does not discard the single highest card. Hands lose cards that were never chosen, for example [8,10,10,9,2] became [9,10,10]. These are implementation errors, not problems with the rules or limits of the platform.
- round 2: revise_rules: The same failure repeated over five attempts: the match hit the 400-turn cap. The design is too long for the platform. With random play a CALL (hand_sum 7 or less) is rare, so matches run the full 30 rounds. Each round has three simultaneous polls (talk, first choice, claim), so with 5 players that comes to 30 × 3 × 5 = 450 answers, more than the cap.
- round 3: fix_tests: Replaying the scenario gives 7 cards in the draw pile, which is what the game reports. Starting from 10: in round 1 seat 1 TAKEs the offered 2 (no draw) and seat 2 DRAWs one card (9 left); in round 2 both players DRAW (7 left). The test's expected 6 counts one draw too many, while the game's final slots (seat 1 c1=7, c2 empty, c3=3) show the take, the pair shed and the empty slot handled correctly.

## Choices the rules did not make

- 2 to 4 players, suggested 3: The designer suggested 3, which is kept. The minimum is 2 because two players still race to a low hand, contest the row and time YANIV against Asaf. The maximum is 4 because each hand uses 3 cards per player plus the row, and more seats make take collisions and draws so frequent that one player's choice matters little.
- Empty slots are coded as -1: A Joker is worth 0, so 0 cannot also mean empty.
- No talk phase: The rules say there is no discussion phase.
- Strategy exists: Thoughtful players track the dead pile and offer row to count cards, set up pairs to shed several cards at once, avoid contested row positions, and time YANIV to avoid being undercut (Asaf).
- The end check uses max_penalty after a showdown: This keeps the 50-point condition arithmetic on a table attribute.

## Simplifications

- The three simultaneous answers are three consecutive polls: A question takes one answer. Answers are stored privately and never shown between polls, so the choices stay simultaneous.
- Shuffling and drawing from the top are modelled as random draws from the draw_pile list: Drawing at random from an unordered hidden list is equivalent to drawing the top card of a shuffled pile.
- Skipping steps 6-9 after a valid YANIV is done with a per-step condition (any_valid_yaniv is false): The step list is flat, but single steps can carry arithmetic conditions.
