# reversis: needs review

Built from the variation **Short Reversis** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a 24-card deck (A K Q J 9 8 in four suits) and deal 6 cards each, so a hand is 6 tricks. (fixes: 52 cards and 13 tricks per deal is too long for the round limit once several deals are played to reduce luck.): This keeps the full rank and counting structure, including the Quinola, while making a hand short enough to play several.
- Play 4 hands. The first lead rotates so that each seat leads first exactly once. Penalty points carry over between hands. (fixes: A single long deal makes the result depend heavily on the cards dealt (luck swamps skill).): Averaging over 4 deals and equal lead order reduces deal luck and seat advantage. It also creates multi-hand planning, such as pushing points onto the current leader.
- Before each hand except the 4th, every player at the same moment secretly passes 2 cards: to the left in hand 1, to the right in hand 2, across in hand 3, and no pass in hand 4. (fixes: There is no decision before play that lets a player fix a bad deal, so the deal often decides the game before any reasoning happens.): Passing lets good players repair a bad deal. It also creates hidden knowledge to exploit, since you know two cards an opponent holds and they know two of yours, and it opens the option to build toward a reversis.
- Fix the scoring: A=4, K=3, Q=2, J=1 per card taken, with the Quinola (J of hearts) worth 5 instead of 1. The total is 44 per hand. The winner is the player with the lowest total after 4 hands. (fixes: Pools, talon payments, side payments and the variant Quinola bonuses are underspecified and not a winner rule the engine can use.): This gives one exact, arithmetic objective with no pools or payments.
- Reversis: a player who takes all 6 tricks of a hand scores 0 for that hand, and each other player scores 15 instead of their card points. (fixes: The reversis reward ('wins outright, sweeps pools') is not stated as numbers, so its risk and reward cannot be weighed.): This keeps the reversal with a stated payoff that is large but not game-ending. The three others must sometimes take a counter on purpose to break a sweep, which creates conflict among them.

Objective: After 4 hands, the player with the lowest running total wins. If two or more players tie for the lowest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. ARITHMETIC: Each suit holds A4+K3+Q2+J1 = 10, so four suits make 40. The Jack of Hearts is worth 5 instead of 1, adding 4, for 44. The stated total of 44 is correct. A reversis scores 0 for the shooter and 3x15 = 45 for the others. With an ordinary hand averaging 11 per player, a reversis is a swing
- playable: pass. COMPLETENESS: The deck, ranks, follow-suit rule, trick winner (highest card of the led suit, no trumps), lead rules, pass timing and direction, pass visibility, scoring, the reversis condition, end of game and tie handling are all specified. Passes are chosen simultaneously, so a player cannot pass 
- reasoning_over_luck: pass. INFERENCE AVAILABLE: All 24 cards are in play, and each player knows 6 cards plus the 2 they passed. Counting the played cards narrows the remaining holdings each trick, and voids are revealed when a player fails to follow. By trick 4 or 5 the remaining distribution is largely deducible.

PLANNING: 

## Complexity

- steps_per_round: designed 13, built 19, limit 20
- choice_steps_per_round: designed 4, built 6, limit 4
- attributes: designed 12, built 49, limit 20 (built: 80)
- hidden_elements: designed 1, built 10, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 28, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Before any hand starts, nobody holds cards and hand_number is 0
- pass: Hand 1 deal empties the 24-card deck and each player holds 6 (chance-independent)
- pass: Hand 1 passing: every seat chooses two cards and still holds 6 afterwards
- pass: Hand 1 pass to the left keeps every hand at 6 cards
- pass: Hand 2 pass to the right keeps every hand at 6 cards
- pass: Hand 3 pass across keeps every hand at 6 cards
- pass: After passing, every hand still holds 6 cards and the deck is empty
- pass: Hand 4 has no pass and every hand holds 6 cards
- pass: Passing completes and play continues with full hands
- pass: First trick of hand 1: each seat plays one card, leaving 5 each
- pass: Later tricks are led and played: after 3 tricks each seat holds 3 cards
- pass: In a trick every player plays exactly one card face up
- pass: Leader may play any card: the trick completes with 5 cards left each
- pass: Following suit when able: all 6 tricks are played out legally
- pass: A void player may play any card: the hand plays out to empty hands
- pass: Each trick is decided and a full hand of 6 tricks is played
- pass: Trick points and counts are reset to 0 after the hand is scored
- pass: Normal scoring: the hand is scored and its counters reset (chance decides the scores)
- pass: Reversis scoring: the hand is scored and its counters reset (chance decides whether a reversis happens)
- pass: End of hand resets hand points and trick counts to 0
- pass: Game ends after hand 4 is scored; seat 1, far ahead, wins whatever the deal
- pass: Lowest total wins: seat 3 at 0 against 100s cannot be caught in the last hand

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `repeat` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 1': 5, 'seat 2': 5, 'seat 4': 6, 'seat 3': 3, 'seats 1 and 3': 1}, 75-87 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 120.0 decisions, prompts of 91 characters on average (longest 153)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 15, 'seat 2': 10, 'seat 4': 21, 'seat 3': 13, 'seats 1 and 3': 1}
- always `first@seat1`: won 16, lost 44, drew 0
- always `first@seat2`: won 19, lost 41, drew 0
- always `last@seat1`: won 21, lost 38, drew 1
- always `last@seat2`: won 8, lost 50, drew 2

## Triage (whose problem each failure was)

- round 1: fix_tests: The rules make the first round of each hand the passing round, with the 6 trick rounds coming after it. After `rounds: 1` each player should therefore still hold 6 cards (dealt, then 2 passed and 2 received), which is exactly what the game showed: deck empty, every hand 6 cards, trick_number 0. The tests wrongly expect every hand to be empty after only one round.
- round 1: revise_rules: The game was built correctly, but the design needs 6 choice steps per round, over the limit of 4. The extra steps come from the passing choice plus four trick plays in seat order starting from a leader who changes. Against random seats the results are also lopsided, with seat 4 winning 21 games and seat 2 only 10.

## Choices the rules did not make

- 4 players, minimum 4 and maximum 4: The designer fixed 4 seats. The deck of 24 cards deals exactly 6 to each of 4 players, the left/right/across passing needs exactly 4 seats, and the 15-point reversis payment is set for 3 opponents.
- No talk step before plays: The source has no table talk. Adding it would add a mechanic, and in a trick game it would leak hidden hands.
- One script round equals one hand (deal, pass, then 6 tricks run by a repeat): The source's 7 rounds per hand (1 pass + 6 tricks) map onto one script round, and the game ends after 4 such rounds, giving 28 source rounds in all.
- Cards coded as rank+suit text (e.g. 'JH'), with rank values A=6, K=5, Q=4, J=3, 9=2, 8=1 for comparing: Finding the trick winner needs a number to compare; these values keep the source order A > K > Q > J > 9 > 8.
- Strategy at the table: Players pass away dangerous high cards and the Quinola, then duck under the led card and discard point cards when void. A player with a very strong hand may instead aim to win all 6 tricks for a reversis, so opponents must watch for it and take one trick to stop it.

## Simplifications

- Passing 2 cards is two simultaneous polls of one card each: A question takes a single choice from a list. The second poll excludes the first card, and no card moves until both polls are done, so passing stays simultaneous and secret.
- The winner is computed as the highest of 0 - total, and a tie at the lowest total is a shared result: The engine ranks by highest value and shares ties at the top. This matches 'lowest total wins, a tie for lowest is a draw'.
