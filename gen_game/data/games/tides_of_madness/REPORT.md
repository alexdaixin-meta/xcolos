# tides_of_madness: ready for review

Built from the variation **Tides of Madness: Obsession** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the unique cards with a 30-card deck: 5 suits of 6 cards, 2 of each suit carrying a madness icon. Scoring is uniform: set points by suit count, +1 per madness card, and a diversity bonus. (fixes: Dozens of unique card scoring rules cannot be built within the limit of 20 attributes and 20 steps per round.): This keeps sets and madness, the heart of the game, while making the cards buildable and their scoring transparent.
- At the start of each tide, each player secretly chooses an Obsession suit whose set points are doubled for that tide. It is revealed only at tide scoring. (fixes: Two-player drafting with face-up tableaus leaves almost nothing hidden, so there is little to infer about the opponent.): This creates a hidden type chosen by the player, so it is not luck. The opponent must infer it from picks to decide what to deny, and a player may bluff by drafting a decoy suit.
- Drafted cards are placed face down until the end of the tide. Retained cards stay face up. (fixes: Two-player drafting with face-up tableaus leaves almost nothing hidden, so there is little to infer about the opponent.): The opponent's first pick from their unseen starting hand stays unknown. They may be hiding a madness card, which changes the race for the madness bonus.
- Give every card equal base value and draft from shared passed hands only. (fixes: Much of each card's value comes from its specific printed power, which adds luck from the deal unrelated to reasoning.): Both players see most of the same cards, so the deal mostly changes what is available to both, not who is ahead.
- Add explicit loss, tie and draw rules: both players crossing 9 madness, points ties broken by lower madness, otherwise a draw. (fixes: The original does not say what happens if both players cross 9 madness together, or how a points tie is broken, so the arithmetic winner is incomplete.): Every ending is then decided by arithmetic.

Objective: A player loses immediately if their madness total reaches 9 or more at a tide's madness check. If both reach it, the higher madness total loses, and equal totals are a draw. Otherwise, after tide 3 the higher score wins. If scores are tied, the lower madness total wins. If that is also tied, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. SCORING TABLE for a 5-card tide tableau with no retained card. Shapes are suit counts. O is the score if the Obsession suit is the largest group.
- 5 different suits: 5x1 + 4 diversity = 9; O = 10.
- 2+1+1+1 (4 suits): 3+1+1+1+4 = 10; O on the pair = 13.
- 2+2+1: 7; O = 10.
- 3+1+1: 8; O = 14.
- 3+2
- playable: pass. RULES COVERAGE: the deal, pick, swap, reveal, scoring order, bonus, elimination check, retain and tie-breaks are all specified. Hands shrink 5-4-3-2-1 and round 5 is forced. Retained cards are removed from the shuffle, so the 28-30 card deck can always deal 10. The game is finite at 15 rounds. Every
- reasoning_over_luck: pass. SOURCES OF SKILL:
- Inferring the opponent's hidden Obsession from their picks and from the cards missing from the hands passed back, then hate-drafting that suit.
- Planning which madness cards to absorb against the 9 threshold across three tides, including retained-card carryover.
- Choosing +4 or

## Complexity

- steps_per_round: designed 18, built 13, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 10, built 47, limit 20 (built: 80)
- hidden_elements: designed 2, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 15, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Full deck holds 30 cards at setup
- pass: Six rounds played reach round 6 (tide 2 started), no madness end possible
- pass: Tide start deals 5 each from a fresh 30-card deck (deck 20 after the deal, hands 4 after one pick and swap)
- pass: Tide 2 deck excludes the retained cards (28 minus 10 dealt = 18)
- pass: Both seats are offered the 5 suits as Obsession at tide start
- pass: One round moves one card from hand to tableau for each seat
- pass: After four rounds each hand holds 1 card and each tableau 4
- pass: Fifth round takes the last card: hands empty, one card retained, tableau cleared
- pass: Tide 1 ends and is scored and revealed without a madness end
- pass: Madness gains the icons in the tableau plus retained (2 each, equal so no bonus)
- pass: Set points: 3 Ruins plus 2 Idols scores 9; 4 Deep plus 1 Stars scores 11
- pass: Obsession doubles: seat 1 retains all 6 Ruins and obsesses Ruins (20 pts), outscoring anything seat 2 can draft whatever the cards
- pass: Plus 1 point per madness card (equal icons, no bonus)
- pass: Four different suits add 4 points; three suits do not
- pass: Seat with more icons is offered the bonus and takes +4 points; the other seat is not offered it
- pass: Bonus seat chooses madness -1 instead of points
- pass: Equal icons: nobody is offered the madness bonus
- pass: Taking points leaves seat 1 at madness 9: it loses at the madness check
- pass: Reducing madness to 8 after the bonus avoids the loss
- pass: Madness far over 9 ends the game at the end of tide 1 (any cards dealt)
- pass: Both at 9 or more: higher madness loses
- pass: Both at 9 or more with equal madness: draw (shared)
- pass: End of tide 2 adds one retained card; the earlier retained card is not offered
- pass: Retained cards count for sets, icons, +1 per icon and the 4-suit bonus
- pass: Tide 3 end keeps retained unchanged and asks no retain choice
- pass: After tide 3 the higher score wins
- pass: Tied score: lower madness wins
- pass: Tied score and madness: shared win
- pass: Huge score lead wins after a full tide 3 whatever the cards

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `tell` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 11, 'seat 2': 9}, 35-37 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 41.7 decisions, prompts of 164 characters on average (longest 169)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 30, 'seat 2': 29, 'seats 1 and 2': 1}
- always `first@seat1`: won 34, lost 26, drew 0
- always `first@seat2`: won 28, lost 32, drew 0
- always `last@seat1`: won 25, lost 34, drew 1
- always `last@seat2`: won 22, lost 36, drew 2

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed 2. The hand-swap draft only works between two players: what you pass is exactly what your single opponent gets. The strategy lies in reading the opponent's Obsession from what they take, hate-drafting their suit, and managing madness against theirs for the bonus without nearing 9.
- No talk step: The source has no communication. Picks are secret and simultaneous, and with only two rivals in direct conflict, talk would add nothing faithful to the rules.
- Card names such as 'Deep-3' and 'Deep*-1': Each of the 30 cards needs a distinct name so it can be removed from and appended to lists; '*' marks the madness icon, as in the source.
- rank_by encodes the madness loss with madness_end and lost: A single arithmetic expression must cover both endings. After a madness end only not-losing counts, and equal totals tie (draw). Otherwise score comes first, then lower madness.
- Madness reduction needs no floor at 0: The bonus seat added at least 1 icon this tide, so its madness total is at least 1 before the -1.

## Simplifications

- The Obsession is asked in its own simultaneous poll just before the first pick of the tide, not in the same answer: The engine takes one answer per question. Nothing is revealed between the two polls, so the choice is still made blind, at the same moment as the first pick.
- The reveal of face-down tableaus and Obsessions is done by an announcement, while the attributes stay owner-only: Visibility is fixed per attribute. The tell step makes the contents public at the moment the rules reveal them.
- The madness-bonus comparison uses a table attribute, bonus_seat: The engine has no operand for another player's attribute (player_attribute_compare workaround).
- Steps for the start and end of a tide carry a 'when' condition on round_in_tide inside one flat round list: Single conditional steps are supported; no block of steps replaces another.
