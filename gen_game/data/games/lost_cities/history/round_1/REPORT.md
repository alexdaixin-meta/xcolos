# lost_cities: needs review

Built from the variation **Lost Cities: Embargo** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Mirrored deal. Hand 1 is shuffled once, and hand 2 reuses exactly the same card order with seats swapped: the player who moved second in hand 1 receives the first player's hand-1 starting cards and moves first. Both players face the same starting hand and the same draw-pile sequence once each. (fixes: P1 Deal luck dominates): Removes most of the 'who was dealt the 10s and Wagers' difference. What remains is how each player handled the same cards, plus the divergence caused by different discard draws.
- Two hands of 20 turns (10 plays per player per hand, 40 rounds in total) instead of 16. (fixes: P2 Small sample): Gives 20 decisions per player and enough turns to build 5-card columns. Stays within the 40-round limit.
- A Wager multiplies a positive column score by 1.5 (rounded down) instead of doubling it. Each colour still has only one Wager. (fixes: P3 Wager amplification): Wagers remain a real gamble but no longer swing a hand by 30+ points on their own.
- Each turn the player chooses a slot AND 'play' or 'discard'. Discarding is free. Only an attempted illegal play costs 1 point and sends the card to the discard pile. Announcements say only 'discarded X', never whether it was voluntary or illegal. (fixes: P4 No voluntary discard): Restores the original game's main tactical lever: whether to hold, dump, or avoid feeding the opponent a card they want from the discard pile.
- The self-lock is replaced by a secret Embargo. At the start of each hand each player secretly names one colour against the OPPONENT. At the end of the hand, the opponent's column in that colour has its score halved (rounded down) if it is positive. All three colours are buildable by everyone. (fixes: P5 The hidden lock reveals itself): A self-lock with 3 colours is revealed by play. An embargo chosen against the opponent stays hidden: the embargoed player never sees it until scoring. The choice is a real inference. The colours you hold few cards and no high cards in are likely the opponent's strength, so embargo there. The opponent anticipates this and may avoid over-committing to one column. The mirrored deal adds a second-hand layer: you now hold the opponent's hand-1 cards and saw how they used them.
- Running totals and penalties stay private until each hand's scoring. Discard draws are announced with the card taken. (fixes: P6 Opponent modelling is thin): Each player must infer the opponent's hand from the cards they pick up, the cards they discard and the cards they hold back. That is the opponent-reading of real Lost Cities, now with free discards that can be bluffs or denials.

Objective: After both hands, the player with the higher total wins. Equal totals are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. COLUMN SCORE RANGE. Each colour's numbers 2-10 sum to 54.
- Best possible column: W+2..10 = (54-8)=46, x1.5 = 69, +10 = 79; embargoed, 39.
- Typical strong column 6,7,9,10: S = 24; with the Wager 36; at 5 cards +10 = 46; embargoed, 23.
- Weak column '2' alone: -6. Weak column '3,5': 0.
A sensible ha
- playable: pass. COMPLETENESS. The rules specify:
- the deck (30 cards);
- the deal by recorded order, and the hand-2 re-deal from the same order;
- slot order and how the hand closes up after a draw;
- legality (strictly higher number; Wager only before any number);
- the illegal-play penalty;
- the draw-source fal
- reasoning_over_luck: pass. CHANCE IS LIMITED. Chance enters only through one shuffle. Hand 2 reuses the same order with starting hands and seats swapped, which cancels most deal luck. The remaining luck is divergence in which pile cards each player ends up drawing, about 10-20% of the outcome.

WHAT THERE IS TO INFER:
- Oppon

## Complexity

- steps_per_round: designed 13, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 57, limit 20 (built: 80)
- hidden_elements: designed 3, built 28, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: the recorded shuffle holds all 30 cards
- pass: R2: round 1 deals 5 cards to each seat and leaves 20 in the draw pile (19 after seat 1 draws); chance-independent counts only
- pass: R3: round 21 clears the columns, deals the mirrored hands from match_order and does not reshuffle
- pass: R4: in round 1 both seats are asked for an embargo colour
- pass: R5: in hand 2, seat 1 acts on even round 22 and seat 2 does not
- pass: R5: in hand 1, seat 2 acts on even round 4 and seat 1 does not
- pass: R6: a discard goes onto its colour's pile at no cost
- pass: R7: a higher number card is added to the column
- pass: R8: a lower number play is discarded and costs 1 point at scoring
- pass: R9: a Wager played to a column with no number card is added
- pass: R9: a Wager played to a column that has a number card is discarded
- pass: R10: drawing from an empty pile takes from the draw pile
- pass: R10: drawing from the pile topped by this turn's discard takes from the draw pile
- pass: R10: drawing from a non-empty pile topped by an older card takes that card
- pass: R11: the drawn card goes to slot 5 and is offered there next turn
- pass: R12: each turn adds one announcement
- pass: R13: a column of R4, R9 scores 5 and empty columns score 0
- pass: R14: a Wager multiplies a positive score (5 becomes 7) and leaves a negative one unchanged
- pass: R15: a column of 5 or more cards, Wager included, gains 10
- pass: R16: the opponent's embargo halves a positive score (17 becomes 8) and leaves a negative one unchanged
- pass: R17: hand score subtracts penalties and is added to the total
- pass: R18: after round 40 is scored the higher total wins
- pass: R18: equal totals after round 40 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 11, 'seat 1': 9}, 84-84 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.0 decisions, prompts of 381 characters on average (longest 503)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 2 wins 87% of decided matches against random seats
- random seats: {'seat 2': 25, 'seat 1': 35}
- always `first@seat1`: won 50, lost 9, drew 1
- always `first@seat2`: won 52, lost 8, drew 0
- always `last@seat1`: won 39, lost 21, drew 0
- always `last@seat2`: won 29, lost 30, drew 1

## Triage (whose problem each failure was)

- round 1: revise_rules: The game is built to the rules, but a thoughtless 'always take the first option' policy wins about 85% of matches from either seat. That means a near-mindless line, probably playing or discarding the oldest card and always drawing from the draw pile while avoiding penalties and negative columns, beats varied play. The scoring rewards passivity and punishes any attempt to build columns.

## Choices the rules did not make

- Exactly 2 players: The designer fixed 2. The embargo and the mirrored hand swap are built around one opponent.
- No talk step: The source has no communication. With 2 players, free talk would only add cheap bluffing that the rules do not include.
- An illegal play counts as 'the card discarded this turn' for the draw fallback: The illegal card lands on the discard pile this turn exactly like a discard, and the announcement calls it a discard.
- Card codes R2..R10, RW and so on: Gives text tokens for list operations and arithmetic on the number part.

## Simplifications

- Slot and PLAY/DISCARD are combined into one 10-option choice: The engine takes one answer per question, and this keeps the two parts together.
- Discard piles are hidden lists with public top-card attributes: Only the top card is visible and takeable in the source.
- Hand setups and scoring are steps guarded by round == 1, 21, 20 and 40: The step list is flat. Single-step `when` conditions express the two hands without separate blocks.
