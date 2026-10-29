# wizard: needs review

Built from the variation **Three-Card Wizard** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Three players, a 28-card deck (Red, Blue, Green 1-8, plus 2 Wizards and 2 Jesters), 12 hands of exactly 3 cards. Each round is one trick, so there are 36 rounds. (fixes: P1): This keeps trick-taking, trump and exact bidding within 40 rounds and at most 4 choices per round. Every hand is large enough to plan over.
- Every hand has 3 cards instead of 1 to 20. (fixes: P5): Removes the near-random one-card hands. Every hand now offers a real bid decision and in-hand planning.
- Bids are a single simultaneous poll. The literal fixed options 0, 1, 2 and 3 are written directly into the step, not computed from attributes. The answer is stored exactly as given. The default of 1 applies only if the answer is missing or not one of 0-3. The bid is not touched again until end-of-hand scoring. (fixes: P3): Simultaneous bidding removes the last-bidder edge. Hard-coding the option list fixes the build failure where no options were offered and every bid became 1.
- A turned Wizard or Jester simply means no trump. (fixes: P2): Removes the dealer-choice sub-procedure and the dealer's advantage.
- The first leader of hand h is seat ((h - 1) mod 3) + 1. After that, the trick winner leads. (fixes: P2): Balances the leading advantage over 12 hands (4 each).
- The illegal-choice fallback is one rule: play the first card of the player's legal-card list, which keeps the order the cards sit in their hand. (fixes: P4): This is a one-operation fallback that is deterministic and easy to build and test, replacing the broken priority chain.
- Trick resolution uses one numeric strength per card, and the best card is replaced only by a strictly greater strength. A Wizard is 100, a trump is 20 + rank, a led-suit card is its rank, and anything else is 0. (fixes: P1): Implements 'first Wizard wins, else highest trump, else highest led suit, all Jesters means the first Jester wins' as plain arithmetic, with no lookup table.

Objective: After hand 12, the player with the highest score wins. If two or three players tie for the highest score, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. BID TABLE. There are 3 tricks among 3 players, so the mean is 1 trick each. For a random 3-card hand played thoughtlessly (always the first card of the offer), I estimate the tricks taken as P(0)≈0.30, P(1)≈0.44, P(2)≈0.21, P(3)≈0.05. Payoff of each bid against tricks taken t (exact = 20+10t, else -
- playable: pass. COMPLETENESS.
- The deck is 28 cards: 9 dealt, 1 turned for trump, 18 left. This matches the rule text.
- Trump: a suited card gives its suit; a Wizard or Jester gives 'none'. The dealer's choice is removed, so no extra decision is needed.
- Leader: hands 1-12 follow ((h-1) mod 3)+1; later tricks ar
- reasoning_over_luck: pass. THINGS TO INFER. Players see their own 3 cards and the trump card, so they know 10 of 28 cards. The opponents' announced bids reveal their hand strength: a bid of 2 or 3 signals a Wizard or high trumps. The cards played within a hand reveal more.
WAYS TO ACT ON IT. Players can:
- duck to protect a 0

## Complexity

- steps_per_round: designed 17, built 18, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 17, built 46, limit 20 (built: 80)
- hidden_elements: designed 1, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: scores 0, bids 0, hand_number 0, deck holds 28 cards
- pass: First round deals a hand: hand_number 1, each seat got 3 cards (2 left after one trick)
- pass: Deal removes one more card as trump, leaving 18 in the deck
- pass: Trump suit card beats led suit (trump_suit G stated in given)
- pass: New hand after hand 3 is hand 4 (seat 1 leads); random deal so only the count is checked
- pass: Valid bids are stored exactly, a 0 stays 0
- FAIL: An invalid bid answer becomes a bid of 1 | rule R6 is broken: When a bid answer is missing or not in {0, 1, 2, 3}, then that bid is 1.; seat 1 bid: expected 1, got 0
- pass: Bids need not sum to 3: all three bid 3
- pass: Trick state is reset: stale best_seat 3 and led_suit B do not carry over
- pass: Play order leader 2, then 3, then 1: seat 3's Wizard comes before seat 1's
- pass: Follower holding the led suit must follow (or play W/J); a void player may play anything
- FAIL: An invalid card answer plays the first card of the offer | rule R11 is broken: When a play answer is missing or not in the offer, then the first card of the offer is played.; seat 1 tricks_taken: expected 0, got 1; seat 2 tricks_taken: expected 1, got 0
- pass: A played card leaves the hand
- pass: After a Jester lead, the first suited card sets the led suit
- pass: After a Wizard lead no suit is led, so a later player may play any card, and the Wizard wins
- pass: Strength: a low trump (20+1) beats high led-suit cards
- pass: Equal strength does not take the lead: the first Wizard wins
- pass: Trick winner leads the next trick (seat 3's Wizard comes before seat 1's), then the hand is scored
- pass: Exact bids score 20 + 10 per trick at the end of trick 3
- pass: Missed bids lose 10 per trick off
- pass: Bids are reset to 0 after the hand is scored
- pass: After trick 1 the hand continues: no new deal, bids kept, hand_number stays 1
- pass: Game ends after hand 12 is scored; the highest score wins
- pass: Players tied at the top after hand 12 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 13, 'seat 3': 3, 'seats 2 and 3': 1, 'seats 1 and 2': 1, 'seat 1': 2}, 90-99 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 144.0 decisions, prompts of 137 characters on average (longest 203)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 26, 'seat 3': 15, 'seats 2 and 3': 3, 'seats 1 and 2': 1, 'seat 1': 14, 'seats 1 and 3': 1}
- always `first@seat1`: won 22, lost 35, drew 3
- always `first@seat2`: won 17, lost 41, drew 2
- always `last@seat1`: won 1, lost 57, drew 2
- always `last@seat2`: won 4, lost 56, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The game asks for bids as a numeric choice with no option list, and offers only legal cards when a player plays. The tests are built on matching option strings ('1', '2', '0', '3', an illegal 'B8'), so their answer rules never fired and defaults were used instead. The game's own trace matches the rules: deck 28-9-1=18, 2 cards left in each hand after the first trick, a trump card turned, and a trump suit set.
- round 1: fix_game: Every failing scenario breaks at the bidding poll. No seat was ever offered the options 0 or 2 that the tests look for, and all bids came out as 0, even though the rules say a missing bid counts as 1. The rules and the tests are consistent; the game file builds the bid poll wrongly.
- round 1: fix_game: The bidding poll never offered the options 0, 1, 2 and 3 to any seat, so the tests' bid answers never matched. Even the 0 that was sent was overwritten with the default of 1 and later reset to 0, so the bids are not recorded as the rules require. This is a bug in the game file, not in the tests or the rules.
- round 2: fix_game: The rules are clear and the platform can express them; the failures come from the game file. An invalid bid answer was stored as '0' (bid_said '0', bid 0) instead of being replaced by the default bid of 1. In the trick scenarios the game never offered the scripted, legal cards, so its per-trick setup and offer building do not follow Rules 5 to 7 when a hand is already in progress.
- round 2: fix_tests: In the failing scenario every seat's recorded bid answer was '0', which is a valid option. Rule 4 says 0 stays 0, so the game was right to store bid 0. The test never actually submitted a missing or invalid answer: the 'first' default picks option 0, so it expected 1 where the rules require 0.
- round 2: fix_tests: In both failing scenarios the game did what the rules say. In the bid scenario seat 1's recorded answer was '0', a legal bid that the rules say stays 0, so expecting 1 is wrong. In the card scenario seat 1 was dealt W2, R6, B5 by a random shuffle, the fallback played W2 (the first card of the offer), and a Wizard wins the trick, so seat 1 getting the trick is correct; the test predicted a winner that the random deal decides.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed 3 seats. The deal (9 cards plus the 10th as trump), the leader rotation mod 3 and the play order all assume three players. The game is about predicting tricks and managing the trick count against two rivals whose bids are public.
- Strategy at the table: A thoughtful player bids from card strength and the trump suit, then plays to hit the bid exactly: dumping Jesters or low cards to avoid tricks, spending Wizards or trumps to take them, and reading the opponents' public bids to disrupt them. A thoughtless player bids blindly and plays cards in any order.
- No talk step: The source has no table talk, and adding it would add a mechanic.
- Shuffle and deal written as random draws from the deck list: The engine shuffles by drawing at random; drawing 9 cards and then one more for trump matches 'top 3 to each seat, the 10th is trump'.
- The bid and tricks_taken are public attributes: The rules announce bids after the simultaneous poll and announce each trick winner, so both are open information. The poll keeps bids secret until all are in.

## Simplifications

- The source's 'draw' when two or three players tie for the top score becomes a shared win: The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome.
- Each of the three plays is written as three steps (build offer, ask, resolve) addressed to the computed seat: The engine runs a flat list of steps; play order is expressed by naming the seat from leader.
- Hand-start steps carry a 'when trick_in_hand = 1' condition, and scoring carries 'when trick_in_hand = 3': Single steps may be conditional, so no block substitution is needed.
