# g_3up_3down: needs review

Built from the variation **Three Up: Even Rounds** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Every player always gets the same number of turns. The win check happens once, at the end of each round, after all three players have acted. A player who empties mid-round simply passes on their remaining turns that round, and the others still take their turns. (fixes: Seat edge: the game ends the instant a player empties, so First wins every race in which players need equal numbers of plays, and with 7 to 9 plays needed such ties are common.): Moving first no longer lets a player finish a turn ahead of an equally fast opponent. A player who needs the same number of plays as First now finishes in the same round.
- Remove the extra '1' handicap card. Each player gets exactly 3 Low, 3 Mid, 3 High and 1 Clear, which uses all 30 cards. (fixes: The compensation for First (an extra '1') is nearly free: it costs a play in only about 24% of deals, and it can even complete a run of three 1s and clear the Pile, so it does not offset the tempo edge.): Once turns are equalised, no compensation is needed, and the handicap only created a new asymmetry of its own.
- If two or three players empty in the same round, the one who picked up the fewest cards over the whole game wins. If they are still tied, the game is a draw. The engine keeps a public 'cards picked up' count for each player. (fixes: When several players finish level, nothing decided by skill separates them; the result falls to seat order alone.): Ties in the race are settled by play quality, since avoiding pickups and forcing them on others is the core skill, not by seat.
- The step budget is laid out explicitly. Per round: 1 talk poll and 1 reveal. Per player: 1 choice, 1 apply step (play or pickup, using if-conditions) and 1 run/clear step. Then 1 end check and 1 cap check. That is 13 steps and 4 choice steps per round. (fixes: The step budget was asserted rather than shown, and an end check after every individual turn inflates the step count.): This makes the build verifiable within the 20-step and 4-choice limits.

Objective: At the end of each round, if exactly one player has no cards left in Hand or Up pile, that player wins. If several players emptied by the end of the same round, the one with the lowest total of cards picked up during the game wins; if they are tied on that total, the game is a draw. If round 40 ends with nobody out of cards, the player with the fewest remaining cards wins, ties are broken by the lowest picked-up total, and a remaining tie is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SETUP SYMMETRY. Every player gets 3 Low, 3 Mid, 3 High and 1 Clear, so nobody can be dealt all the high cards or all the Clears. Each player knows their own 10 cards and every Up pile, so all three start with the same information.

SEAT EDGE. First opens on an empty Pile and may play anything. Secon
- playable: pass. COMPLETENESS. The rules cover every situation:
- Legal plays: rank at or above the top rank, or an empty Pile.
- Source: Hand first, then the Up pile.
- Clear: always legal and played alone.
- Run count update and the clear at 3 or more.
- Pickup: Pile into Hand, picked-up count increases, Pile rese
- reasoning_over_luck: pass. CHANCE. The chance elements are the seat order and which ranks you get within each band. That decides how many pairs and triples you hold, and so your minimum number of turns: roughly 7 to 10 groups, with a spread of about 2 turns. The stratified deal and the guaranteed Clear limit this variance.

R

## Complexity

- steps_per_round: designed 13, built 13, limit 20
- choice_steps_per_round: designed 4, built 5, limit 4
- attributes: designed 11, built 44, limit 20 (built: 80)
- hidden_elements: designed 1, built 13, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- FAIL: R1 setup holds 30 cards: 7 in hand and 3 up per seat, all stacks emptied | rule R1 is broken: When the game is set up, there are 30 cards: three each of ranks 1 to 9 and three Clears.; seat 1 hand: expected 7 items, got 10; seat 1 up_pile: expected 3 items, got 0; seat 2 hand: expected 7 items, got 10; seat 2 up_pile: expected 3 items, got 0; seat 3 hand: expected 7 items, got 10; seat 3 up_pile: expected 3 items, got 0
- FAIL: R2 each player is dealt 10 cards and every stack ends empty | rule R2 is broken: When cards are dealt, each player gets 3 cards from Low (ranks 1-3), 3 from Mid (4-6), 3 from High (7-9) and 1 Clear, 10 cards in all, and every stack ends empty.; seat 1 hand_count: expected 7, got 10; seat 1 up_count: expected 3, got 0; seat 2 hand_count: expected 7, got 10; seat 2 up_count: expected 3, got 0; seat 3 hand_count: expected 7, got 10; seat 3 up_count: expected 3, got 0
- FAIL: R3 every seat has a public Up pile of 3 and a hand of 7 after selection | rule R3 is broken: When Up piles are chosen, every player chooses exactly 3 of their own cards simultaneously; all Up piles are then made public and each hand holds 7 cards.; seat 1 hand_count: expected 7, got 10; seat 1 up_count: expected 3, got 0; seat 2 hand_count: expected 7, got 10; seat 2 up_count: expected 3, got 0; seat 3 hand_count: expected 7, got 10; seat 3 up_count: expected 3, got 0; seat 1 up_pile: expected 3 items, got 0; seat 1 hand: expected 7 items, got 10; seat 2 up_pile: expected 3 items, got 0; seat 2 hand: expected 7 items, got 10; seat 3 up_pile: expected 3 items, got 0; seat 3 hand: expected 7 items, got 10
- pass: R4 table starts empty with zero counters
- pass: R5 a round with talk then three pickups of an empty pile changes nothing but the round
- pass: R6 seats play in order 1, 2, 3
- FAIL: R6 a seat with no cards left is skipped | rule R6 is broken: When it is a player's turn, seats act in order 1 (First), 2 (Second), 3 (Third), and a player with cards_left = 0 skips the turn.; seat 2 cards_left: expected 0, got 4; seat 2 picked_up: expected 0, got 1; seat 2 out: expected True, got False; game pile: expected ['5', '7'], got ['7']; game players_out: expected 1, got 0; seat 2 was offered 'pick up', but must not be
- FAIL: R7 with cards in hand only hand cards are offered | rule R7 is broken: When a player has hand_count > 0, they may play only from hand; when hand_count = 0, they play from up_pile.; seat 1 up_pile: expected ['9', '9', '2'], got ['2', '3', '3']
- FAIL: R7 with an empty hand the seat plays from its Up pile | rule R7 is broken: When a player has hand_count > 0, they may play only from hand; when hand_count = 0, they play from up_pile.; seat 1 hand_count: expected 0, got 1; seat 1 up_count: expected 1, got 3; seat 1 cards_left: expected 1, got 4; seat 1 up_pile: expected ['2'], got ['1', '2', '3']; Ada: the rule for 'play 2 x rank 9' was never matched (the game never put that option to this seat)
- FAIL: R8 on top rank 5 a 5 or 9 is offered and a 4 is not | rule R8 is broken: When a player plays numbered cards, all cards are of one rank and from one source, and the play is legal only if the pile is empty or the rank >= top_rank (e.g., on top_rank 5, a 5 or 9 is legal and a 4 is not).; seat 2 hand_count: expected 3, got 2; seat 2 cards_left: expected 6, got 5
- pass: R9 same rank raises run_count, a new rank resets it
- FAIL: R10 a third card of the top rank clears the pile | rule R10 is broken: When run_count reaches 3 or more, all pile cards go to removed, the pile empties, and top_rank and run_count become 0.; game pile: expected ['3', '5'], got ['5']; seat 2 was never offered 'play 1 x rank 3', but should have been; Blaise: the rule for 'play 1 x rank 3' was never matched (the game never put that option to this seat)
- FAIL: R10 playing three of a new rank at once clears the pile | rule R10 is broken: When run_count reaches 3 or more, all pile cards go to removed, the pile empties, and top_rank and run_count become 0.; seat 2 hand_count: expected 1, got 0; seat 3 hand_count: expected 1, got 0
- FAIL: R11 a Clear is always offered and removes the whole pile | rule R11 is broken: When a player plays a Clear, it is played alone and is always legal; the Clear and the whole pile go to removed, and top_rank and run_count become 0.; game pile: expected ['1', '4'], got ['4']; Blaise: the rule for 'play 1 x rank 1' was never matched (the game never put that option to this seat)
- FAIL: R12 picking up takes the pile; picking up an empty pile changes nothing | rule R12 is broken: When a player picks up, every pile card moves to their hand, picked_up increases by the number of cards taken, and pile, top_rank and run_count reset to empty/0; picking up an empty pile changes nothing.; seat 1 hand_count: expected 4, got 3; seat 1 cards_left: expected 7, got 6; seat 2 picked_up: expected 2, got 0
- pass: R13 a seat that could play may pick up instead
- FAIL: R15 the only seat that empties wins | rule R15 is broken: When seat 3's turn ends and exactly one player has cards_left = 0, that player wins.; winner: expected 'seat 1', got 'seats 1, 2 and 3'; seat 1 standing: expected 999995, got -30000; seat 2 standing: expected -60001, got -30000; seat 3 standing: expected -40000, got -30000; seat 1 out: expected True, got False; seat 1 cards_left: expected 0, got 3; seat 2 picked_up: expected 1, got 0; seat 2 cards_left: expected 6, got 3; game players_out: expected 1, got 0; game round: expected 1, got 40; Ada: the rule for 'play 1 x rank 9' was never matched (the game never put that option to this seat)
- FAIL: R16 of two seats that empty, the lower picked_up wins | rule R16 is broken: When seat 3's turn ends and two or three players have cards_left = 0, the one among them with the lowest picked_up wins, and a tie on picked_up is a draw between them.; winner: expected 'seat 2', got 'seats 1, 2 and 3'; seat 1 standing: expected 999996, got -30000; seat 2 standing: expected 999998, got -30000; seat 3 standing: expected -60002, got -30000; seat 1 out: expected True, got False; seat 2 out: expected True, got False; seat 3 picked_up: expected 2, got 0; seat 3 cards_left: expected 6, got 3; game players_out: expected 2, got 0; Ada: the rule for 'play 1 x rank 9' was never matched (the game never put that option to this seat); Blaise: the rule for 'play 1 x rank 9' was never matched (the game never put that option to this seat)
- FAIL: R16 two emptied seats tied on picked_up share the win | rule R16 is broken: When seat 3's turn ends and two or three players have cards_left = 0, the one among them with the lowest picked_up wins, and a tie on picked_up is a draw between them.; seat 1 standing: expected 999997, got -30000; seat 2 standing: expected 999997, got -30000; seat 3 standing: expected -60002, got -40000; game players_out: expected 2, got 0; Ada: the rule for 'play 1 x rank 9' was never matched (the game never put that option to this seat); Blaise: the rule for 'play 1 x rank 9' was never matched (the game never put that option to this seat)
- FAIL: R17 after seat 1 empties, seats 2 and 3 still take their turns | rule R17 is broken: When a player empties mid-round, the round still continues to seat 3 before any end check.; winner: expected 'seat 1', got 'seat 2'; seat 1 out: expected True, got False; seat 1 cards_left: expected 0, got 5; seat 2 cards_left: expected 4, got 3; game pile: expected ['5', '6', '7'], got []; game top_rank: expected 7, got 0; game round: expected 1, got 40; game players_out: expected 1, got 0; Ada: the rule for 'play 1 x rank 5' was never matched (the game never put that option to this seat)
- pass: R18 at round 40 with nobody out, fewest cards then lowest picked_up wins
- pass: R18 at round 40 a full tie on cards and picked_up is shared

## Does the file follow the spec's shape? (flags for a person)

- rule R14 has no scenario: nothing checks it

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 4, 'seat 3': 7, 'seat 2': 9}, 48-232 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 207.0 decisions, prompts of 149 characters on average (longest 216)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the last option as seat 1 wins 90% of decided matches against random seats
- always taking the last option as seat 2 wins 88% of decided matches against random seats
- random seats: {'seat 1': 21, 'seat 3': 18, 'seat 2': 21}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 54, lost 6, drew 0
- always `last@seat2`: won 53, lost 7, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: After the deal each seat's hand holds 10 cards, but hand_count, up_count and cards_left all stay at 0. The game never updates the public counts. It also never moves 3 cards into up_pile when the Up-pile choice is declined or missing, so no seat ends setup with 3 up and 7 in hand. The rules are clear and the platform can express this, so the fault is in the file.
- round 1: fix_game: The game crashes with a CalcError: `you.hand[0]` is read on an empty hand, a fault in the file and not in the rules. The setup also never finishes the simultaneous Up-pile choice: after setup every seat still holds 10 cards in hand and an empty up_pile, although the rules make that choice part of setup.
- round 1: fix_game: The rules put choosing the Up pile in SETUP (step 5), so after setup every seat must hold 7 Hand cards and 3 public Up cards. The game dealt the cards and built the Up-pile offers, but it never moved any cards: hands stayed at 10 and Up piles at 0. The tests check results the rules clearly require (counts and pile sizes), not internal bookkeeping.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at three: three ranked seats in a turn order, and an end check written for one, two or three emptied players.
- The talk round is a simultaneous poll with broadcast: The rules say messages are written at the same moment. Talk earns its place because players want opposite things (each wants the others to pick up) and can try to coax a rival into taking the Pile.
- Random seating maps to seat numbers 1, 2, 3 as First, Second, Third: The engine's seeded random seating gives the random order the rules ask for.
- Up pile chosen by three successive simultaneous polls into a private up_choice list, revealed afterwards: A single answer is one choice; three picks kept hidden until all are done keep the choice simultaneous.
- rank_by = out*1000000 - cards_left*10000 - picked_up: Out players rank above all others, then fewer cards, then fewer picked up. picked_up cannot reach 10000 in 40 rounds (at most 40 pickups of 27 cards), so the weights never overlap.
- Cards are written as text '1'..'9' and 'C'; top_rank is 0 for an empty pile: Gives the legality check a simple arithmetic comparison.

## Simplifications

- A draw is represented as all tied top players sharing the win: The engine has no separate draw; players level at the top share the result, and the other players still lose.
- Each seat's turn is written as its own ask plus update steps, in fixed seat order: Each play must resolve before the next seat chooses, against the current pile.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: "you.up_pick != ''" reads `you` where there is no player
- 2: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 'C' in `up_pile_pick`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered '5' in `up_pile_pick`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 3: the game file was refused by the loader: g_3up_3down: steps[6].do[4].value.calc: "'round ' + str(round) + ' seat 1: ' + act if False else 'seat 1: ' + act": only these functions exist: sum, min, max, len, abs, round, int, any, all, sorted, count, uniform, split
- 4: it plays, but part of it does nothing: game attribute `ranks` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `symbols` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `idx` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 5: passed
