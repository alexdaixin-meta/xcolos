# ultimatum_game: needs review

Built from the variation **Hidden Pie Ultimatum III** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Three players. A proposal passes if at least one of two Responders accepts, and a rejected share is burned. (fixes: P1): With three players one rival's gain is not the other's loss. Two Responders compete for the offer, and a lone holdout punishes the Proposer only partly, so offering the minimum, rejecting everything or offering a fair split can each lose.
- The pot is hidden from the Responders. Each player has the list 70/90/110/130 and is told the pot only when it is drawn; the pot is revealed after the round. (fixes: P2): Responders must infer the pot from the offer size and from the values the Proposer has not yet played.
- 12 proposal rounds. Each player proposes exactly 4 times and plays every pot value once; only the order is random. (fixes: P3): Every player's pie is exactly 400, so the deal changes only what is known, not who is ahead. Under symmetric fair play everyone ends on 400 and the game is a draw.
- The tie-break is removed. A tie for the highest total is a draw. (fixes: P4): No tie-break that depends on the draw.
- The Split Demand round is removed entirely. (fixes: P5): It was a never-behind safe option. The final proposal rounds still let Responders retaliate, and a leading Responder who rejects can be overtaken if the other accepts.
- Snake proposer order: P1, P2, P3, P3, P2, P1, P1, P2, P3, P3, P2, P1. (fixes: P6): P1 proposes both first (least information) and last (most information). P3 proposes twice in a row in the middle, and P2's turns are evenly spread, so first-mover and last-mover effects offset.
- The pot lists are kept as game lists, not player attributes. (fixes: P7): This keeps the attribute count at 9.

Objective: After round 12, the player with the strictly highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Each player proposes exactly 4 times and draws each of 70, 90, 110 and 130 exactly once, so every player handles 400 units in total. Chance changes only the order of the pots, not the total.

Responder payoffs per round, with offer (a, b), pot V, and 'other' meaning the other Responder:
- Both accep
- playable: pass. Complexity against the limits:
- steps 12 (limit 20)
- choice steps 3: talk, offer, response (limit 4)
- attributes 9 (limit 20)
- hidden elements 1: the pot (limit 3)
- random draws 1 per round (limit 1)
- rounds 12 (limit 40)

The draw from a per-player game list uses the supported shared_deck_dra
- reasoning_over_luck: pass. Every player plays the same four pots, so chance affects only when each pot arrives, and therefore how much is hidden. I estimate under about 15% of the outcome comes from chance.

If all three play the same pot-dependent strategy, their totals are identical and the game is a draw. The random order 

## Complexity

- steps_per_round: designed 12, built 11, limit 20
- choice_steps_per_round: designed 3, built 4, limit 4
- attributes: designed 9, built 25, limit 20 (built: 80)
- hidden_elements: designed 1, built 5, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: all scores 0 and every pot list holds 4 values
- pass: Round 1 proposer is seat 1
- pass: Round 2 proposer is seat 2
- pass: Round 3 proposer is seat 3
- pass: Round 4 proposer is seat 3
- pass: Round 5 proposer is seat 2
- pass: Round 6 proposer is seat 1
- pass: Round 7 proposer is seat 1
- pass: Round 8 proposer is seat 2
- pass: Round 9 proposer is seat 3
- pass: Round 10 proposer is seat 3
- pass: Round 11 proposer is seat 2
- pass: Round 12 proposer is seat 1
- pass: Proposer 2: responder1 is seat 1 (gets offer_a), responder2 is seat 3
- pass: Draw removes one value from the proposer's pot list
- pass: Full game of rejections empties every pot list; all tied at 0 share the win
- pass: Only the proposer is asked for amounts; responders never see a number question
- pass: Round completes after simultaneous talk
- pass: Offer_b range is limited to 130 - offer_a
- pass: Offers are recorded publicly
- pass: Both responders answer; proposer is not asked to respond
- pass: Both accept: pot 110, offers 30/40 gives +40/+30/+40
- pass: Only responder1 accepts: pot 90, offers 30/40 gives +20/+30/0
- pass: Overpaying: pot 70, offers 50/50 accepted gives proposer -30
- pass: Both reject: no score changes
- pass: Reveal state: responses and scores after proposer 3 deal (pot 130, offers 20/30)
- pass: Game ends after round 12; leader with given scores wins
- pass: Tie at the top after round 12 is a shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 11, 'seat 3': 2, 'seat 2': 7}, 84-84 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 84.0 decisions, prompts of 220 characters on average (longest 346)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seat 1': 37, 'seat 3': 7, 'seat 2': 16}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 60, lost 0, drew 0
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: In every failing scenario the move log shows both Responders answering 'Accept', not 'Reject'. The game then correctly paid the Proposer pot - a - b, which gives 70+90+110+130 = 400 each over a full game, 130 in round 1 and +70 in the round-12 case. The game follows the rules; the tests assumed rejections they never actually scripted, since the 'decline' default resolved to Accept.
- round 1: revise_rules: The game file is correct; the design is degenerate. A single Accept passes the deal and rejecting never costs a Responder anything, so offering 0/0 keeps nearly the whole pot and accepting is never worse than rejecting, which is why the 'first option' policy wins every decided match and the 'last option' policy loses every one.

## Choices the rules did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed the table at 3. The Proposer order, the two-Responder structure and the 4 proposals each over 12 rounds only work with exactly 3 seats. The strategy is to infer the hidden pot from the offer size and from which values the Proposer has already used, to bluff about the pot in talk, and to decide whether to undercut a fellow Responder, since one acceptance is enough for the deal to pass.
- Talk is a simultaneous poll broadcast to all: The source requires all three messages to be written at the same time, unseen, and then shown to everyone. The players also disagree about the split, so talk earns its place.
- The pot lists are hidden table attributes (visibility none): If the remaining lists were public, they would show the drawn pot the moment it is removed. Their contents are announced at setup, and every used value is revealed at the end of each round, so players can still track what remains, as the source intends.
- The offer is asked as two sequential numbers, with b's range limited to 130 - a: A question takes one number, and limiting b's range enforces a + b <= 130 by arithmetic.

## Simplifications

- A tie for the highest score is a shared win rather than a draw: The engine ranks by one expression and has players level at the top share the win, with no separate draw outcome. A sole leader still wins outright, as in the source.
