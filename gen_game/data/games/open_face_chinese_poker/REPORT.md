# open_face_chinese_poker: ready for review

Built from the variation **Duplicate Open-Face Pairs** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Drop suits and flushes. Use 32 cards: values 1 to 8, four copies of each. The only made hand is a pair. (fixes: P3 Scoring too heavy to build): Pair detection in a 2-card row is a single equality test, so category scoring becomes one arithmetic expression.
- Rows become Front 1 slot, Middle 2 slots, Back 2 slots: 5 cards per hand, one per round. Front strength = 2 x card value. Middle and Back strength = sum of the two cards + 100 if they pair. (fixes: P1 Attribute count understated; P3 Scoring too heavy to build): This removes 3-card category logic entirely. It also cuts row slots from 8 to 5 per player. Doubling the Front card puts it on the same scale as a two-card sum, so the rising-strength rule still bites.
- Remove the face-down first Back card. Each player's dealt cards are one private hand list, and discards are simply removed from it and never shown. Declared hidden elements: (1) each player's private hand, (2) the deck order. (fixes: P2 Hidden elements understated): Two hidden elements is honest and within limits. Discards need no storage because only their owner ever knew them.
- Use an explicit encoding of 19 attributes. Per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a match total, a chosen card and a chosen row, which is 9 x 2 = 18. Add 1 shared deck list. At scoring, strengths are written over F, M1 and B1, so no extra attributes are needed. (fixes: P1 Attribute count understated): Gives a credible count inside the limit of 20.
- Write an explicit step list of 17 steps. Scoring steps carry a 'last round of a hand' condition. (fixes: P3 Scoring too heavy to build): Shows that dealing, the two polls, placement, reveal and scoring fit within 20 steps.
- Keep only the fallback: a player may name any row, and if it is full the card goes to the first non-full row in the order Back, Middle, Front. (fixes: P4 Rules contradicted themselves on full rows): One consistent rule, with no forbidden choice that the engine would have to block.
- State explicitly that everything seen in earlier hands may be used, including that in the mirrored hand the opponent receives exactly the cards you were dealt. (fixes: P5 Cross-hand knowledge not stated): Makes the main inference lever visible and legal.
- Play 4 hands of 5 rounds (20 rounds). Hands 1 and 2 use one shuffle from both seats; hands 3 and 4 use a second shuffle from both seats. Each player is dealt 3 cards per round and keeps 1. (fixes: P6 Thin skill signal): Doubles the duplicate sample and gives a real choice each round, while keeping at most one random draw per round.

Objective: After round 20, the player with the higher match total (the sum of their four hand scores) wins. Equal totals are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SYMMETRY: Each deal is played once from Seat X and once from Seat Y. Player A is X in hands 1 and 3 and Y in hands 2 and 4. Choices are simultaneous. In hand 2 both players know exactly the opponent's offered cards, because each was dealt them in hand 1. Both have also seen which card the other kept
- playable: pass. RULES: The rules are complete.
- Deal positions are explicit (6r-5 to 6r). Positions 31 and 32 are unused.
- Overflow on a full row is defined in the order Back, Middle, Front. A full Front cannot be chosen once filled, because overflow handles it.
- The foul test, ties (no point), scoop, royalties 
- reasoning_over_luck: pass. LUCK: The duplicate format cancels deal luck. Each player plays both sides of the same 30-card sequence, twice in the match. When both players follow the same good strategy, they make essentially the same decisions on the same cards and the match tends to a draw. No random draw selects a winner. Any

## Complexity

- steps_per_round: designed 17, built 11, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 19, built 41, limit 20 (built: 80)
- hidden_elements: designed 2, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 20, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: the deck holds 32 cards and stays 32 after a deal; other rows stay empty (cards dealt by chance)
- pass: Match ends after hand 4; the higher total wins
- pass: Hand 2 is not reshuffled: B gets the first 3 deck cards and A the next 3
- pass: Each round deals the next 6 deck positions: Seat X first, then Seat Y
- pass: In hand 1 Player A is Seat X and receives the first 3 cards
- pass: After hand 1 the 2 undealt positions are skipped, so hand 2 deals B what A got in round 1
- pass: Each seat keeps exactly the one card it picks from its 3
- pass: The kept card goes into the row the seat names
- pass: Middle holds a second card after the first
- pass: A full named row falls back to Back, then Middle
- pass: Only the kept card is placed; the 2 unkept cards appear nowhere
- pass: Both kept cards are shown face up in their rows after the round
- pass: Front strength is doubled: Front 4 (8) beats Middle 3+4 (7), so A fouls
- pass: A Middle pair adds 100: 2+2 (104) beats Back 7+8 (15), so A fouls
- pass: Equal row strengths (6,6,6) do not foul
- pass: Front 7 earns +1 royalty (6 + 1 against a fouled opponent)
- pass: A Middle pair earns +2 (with the needed Back pair +1: 6+3 = 9)
- pass: A Back pair earns +1 (6 + 1 against a fouled opponent)
- pass: Only strictly higher rows score; tied Front and Back score nothing
- pass: Winning all 3 rows scores 3+3, plus A's royalties of 3 = 9
- pass: With no foul, each player adds their own royalties to rows won
- pass: Exactly one foul: the other scores 6 plus royalties and the fouler scores 0
- pass: Both players foul: both score 0 and totals stay
- pass: After a hand the score is added to the total, rows are cleared and hand 2 begins
- pass: Equal final totals share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 9, 'seats 1 and 2': 4, 'seat 2': 7}, 78-80 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 80.0 decisions, prompts of 155 characters on average (longest 200)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 22, 'seats 1 and 2': 15, 'seat 2': 23}
- always `first@seat1`: won 24, lost 23, drew 13
- always `first@seat2`: won 19, lost 24, drew 17
- always `last@seat1`: won 26, lost 20, drew 14
- always `last@seat2`: won 23, lost 26, drew 11

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer set 2, and the duplicate format mirrors one seat's deal onto the other, which only works with two seats. The strategy is to remember the cards seen in the odd hand and use them to predict the opponent's options in the even hand, and to balance foul risk against pairs.
- Player A is seat 1 and Player B is seat 2: The rules name players A and B but not their seats.
- No talk step: The rules have no communication, and in a two-player zero-sum game talk adds nothing to reason about.
- Row choice offers all three rows even when one is full: The rules let a player name a full row and apply a fallback, so the fallback is kept rather than hiding options.
- Strengths are stored back into front, mid1 and back1 at scoring: This follows the build note, so foul tests, comparisons and royalties are single expressions.

## Simplifications

- Fixed deck order is encoded by rotating dealt cards from the front of the deck list to the back, plus 2 extra rotations after each odd hand: The engine has no position lookup. Rotation keeps the order so the even hand repeats the odd hand's deal exactly.
- Row comparison uses a table list, seat_strengths, holding both players' strengths and fouls: The engine cannot compare one player's attribute directly to another's; a table copy is the documented workaround.
- Discards are simply removed from the hand list rather than kept in a discard pile: Discards are never shown or used again, so no pile is needed.

## Encoding attempts

- 1: playing it with random seats failed: seed 1, 2 players: the match crashed: FlowError: "you.chosen_row == 'Front'" reads `you` where there is no player
- 2: passed
