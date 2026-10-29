# wizard: needs review

Built from the variation **Wizard Triad** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a 28-card deck (3 suits of 1-8, 2 Wizards, 2 Jesters), 3 players, 12 hands of exactly 3 tricks each, with one trick per round, for 36 rounds. (fixes: The original is far too long: up to 20 hands of growing size, so hundreds of card plays, beyond the 40-round limit.): This keeps the bid-then-play identity within 40 rounds and 4 choice steps per round.
- Use a fixed hand size of 3. A Wizard or Jester turned as the trump card means no trump; the dealer never chooses. The first lead rotates so each seat leads first in 4 hands. (fixes: Variable hand size and the dealer's trump choice add steps and branches the engine cannot handle cleanly.): This removes branches and keeps the seats balanced.
- Replace rule (8) with one total, deterministic priority order. (a) If there is a led suit and the player holds it, play their lowest-ranked card of that suit. (b) Otherwise, play a Jester if held. (c) Otherwise, play their lowest-ranked suited card, breaking ties between equal ranks Red < Blue < Green. (d) Otherwise, play a Wizard. Step (a) is skipped whenever there is no led suit. The phrase 'first legal card' is removed. (fixes: In the previous variation, rule (8), the fallback for an illegal or unknown card, was not deterministic. It had no tiebreak between equal ranks of different suits, did not place Wizards in the order, was undefined when a Wizard was led, and its phrase 'first legal card' conflicted with its explicit ordering.): The engine can then apply the fallback without inventing an order, and the rule covers every hand.
- A missing or illegal bid counts as a bid of 1. (fixes: The previous variation did not say what happens with an illegal or missing bid.): This makes bidding total and deterministic.
- Define the led suit as the suit of the first suited card in the trick, provided no Wizard was played before it. If a Wizard is played before any suited card, the trick has no led suit. The impossible all-Jester case is replaced by a note that it cannot occur, with a harmless fallback (the first Jester wins). (fixes: The previous variation did not say what the led suit is when a Jester is led and a Wizard is played before any suited card. It also had an 'all three Jesters' rule that cannot happen with only 2 Jesters, which left the edge cases looking incomplete.): This leaves no undefined trick states.

Objective: After hand 12, the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SCORING TABLE (per player per hand). Exact bid: bid 0 = 30, bid 1 = 35, bid 2 = 40, bid 3 = 45. Off by d tricks: -10d. So the miss table is: off by 1 = -10, off by 2 = -20, off by 3 = -30. The label '30 + 5 x bid' matches these numbers. A hit against a 1-trick miss is a swing of 40 to 55, while the 
- playable: pass. COMPLETENESS:
- Deck: 28 cards; 9 dealt plus 1 trump card per hand.
- Trump: a suited card sets trump; a Wizard or Jester means no trump. This is clear, and the original's dealer choice is removed.
- Bids: simultaneous poll, 0-3, with a default of 1 for missing or invalid bids.
- Lead rotation: fixe
- reasoning_over_luck: pass. WHAT THERE IS TO INFER:
- Each player holds 3 of 28 cards; 18 cards are unseen each hand.
- Revealed bids signal opponents' hand strength. A bid of 2-3 suggests a Wizard or high trumps; a bid of 0 suggests Jesters and low cards.
- Played cards stay visible, so later tricks allow deduction of what re

## Complexity

- steps_per_round: designed 14, built 15, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 16, built 44, limit 20 (built: 80)
- hidden_elements: designed 2, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 36, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- FAIL: R1: a new hand deals 3 cards to each seat and 1 trump card; after the first trick the deck holds 18 and each hand 2 (the cards themselves are random) | rule R1 is broken: When a hand starts (trick_in_hand == 1), then all 28 cards are shuffled into deck and each player is dealt exactly 3 cards into their hand, seen only by them.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- pass: R2: with a suited trump (G), a green card played off-suit beats the led red card
- FAIL: R3: simultaneous bids 2, 0 and 3 are recorded as given, although they do not sum to 3 | rule R3 is broken: When bidding, then all three players bid 0, 1, 2 or 3 simultaneously, and a missing or invalid bid becomes 1; all bids are then revealed, and they need not sum to 3.; seat 1 bid: expected 2, got 0; seat 3 bid: expected 3, got 0; Ada: the rule for 2 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: R4: after hand 1 is scored, the next round starts hand 2 with a fresh deal | rule R4 is broken: When hand h starts, then the first leader is seat ((h - 1) mod 3) + 1: P1 for hands 1, 4, 7, 10; P2 for hands 2, 5, 8, 11; P3 for hands 3, 6, 9, 12.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- pass: R5: leader seat 2 leads red, then seats 3 and 1 must follow red; seat 1's R7 wins
- pass: R6: a led Wizard leaves the trick with no led suit, so later seats may play any card
- pass: R7: a seat holding the led suit may not play another suit; a seat without it may play anything
- pass: R8: a Jester and a Wizard are legal even when holding the led suit; the Wizard wins
- FAIL: R9: an invalid answer falls back to the seat's lowest card of the led suit (R2 rather than R6) | rule R9 is broken: When a player's choice is missing or not a legal card they hold, then the engine plays, in order of priority: (a) their lowest led-suit card if a led suit exists and they hold one; (b) else a Jester; (c) else their lowest suited card, with ties broken Red, then Blue, then Green; (d) else a Wizard.; seat 1 tricks_taken: expected 1, got 0; seat 2 played_card: expected 'R2', got 'R6'; seat 2 tricks_taken: expected 0, got 1
- pass: R10: when two Wizards are played, the first one wins, even against trump
- pass: R11: the highest trump beats the led suit and a lower trump
- pass: R12: with no Wizard and no trump, the highest card of the led suit wins over a higher off-suit card
- FAIL: R13: two Jesters and no other card played: the first Jester wins | rule R13 is broken: When no card qualifies under R10-R12, then the first Jester played wins the trick.; the match crashed: CalcError: "card[0] in ['R', 'B', 'G'] and led_suit == '' and not wizard_played": string index out of range
- pass: R14: the trick winner (seat 2) leads the next trick, so its red lead wins and every bid is made
- pass: R15: cards played stay in played_cards (3 from trick 1 plus 3 from trick 2)
- pass: R16: exact bids score 30 + 5 x bid (bid 3 gives +45, bid 0 gives +30)
- pass: R17: missed bids lose 10 per trick of difference
- pass: R18: after a hand is scored, tricks_taken resets to 0 while the bids stay as they were
- pass: R19: the game ends after hand 12 is scored and the highest total wins
- pass: R19: two seats level at the top after hand 12 share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 1': 4, 'seat 2': 14, 'seat 3': 2}, 89-98 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 144.0 decisions, prompts of 176 characters on average (longest 271)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 20, 'seat 2': 25, 'seat 3': 14, 'seats 2 and 3': 1}
- always `first@seat1`: won 26, lost 34, drew 0
- always `first@seat2`: won 25, lost 34, drew 1
- always `last@seat1`: won 1, lost 59, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The game asks for bids as a numeric choice with no option list, and offers only legal cards when a player plays. The tests are built on matching option strings ('1', '2', '0', '3', an illegal 'B8'), so their answer rules never fired and defaults were used instead. The game's own trace matches the rules: deck 28-9-1=18, 2 cards left in each hand after the first trick, a trump card turned, and a trump suit set.
- round 1: fix_game: Every failing scenario breaks at the bidding poll. No seat was ever offered the options 0 or 2 that the tests look for, and all bids came out as 0, even though the rules say a missing bid counts as 1. The rules and the tests are consistent; the game file builds the bid poll wrongly.
- round 1: fix_game: The bidding poll never offered the options 0, 1, 2 and 3 to any seat, so the tests' bid answers never matched. Even the 0 that was sent was overwritten with the default of 1 and later reset to 0, so the bids are not recorded as the rules require. This is a bug in the game file, not in the tests or the rules.

## Choices the rules did not make

- 3 players (min = max = suggested = 3): The designer fixed the table at 3, and the lead rotation, 3-card hands and deck size are built for exactly 3 seats.
- No talk step: The rules say explicitly that there is no talk phase. The strategy lies in judging hand strength for the bid and in playing to hit the bid exactly, including ducking tricks.
- Card codes such as 'R5', 'W1', 'J2': These give a text form for cards in list attributes, so suits and ranks can be compared arithmetically.
- Trick winner tracked by a running strength value (Wizard 100, trump 20 + rank, led suit = rank, Jester 0, off-suit -1), replaced only when strictly greater: This reproduces rule (9) by arithmetic. A strict comparison keeps the first Wizard and the first Jester winning ties.
- Only legal cards are offered: This enforces rule (7) directly. The fallback priority of rule (8) still applies to missing or invalid answers.

## Simplifications

- A tie for the highest score is a shared win rather than a labelled draw: The engine has no separate draw outcome: players level at the top share the win.
- The trump card is drawn at random from the remaining deck rather than taken as the literal 10th card: With a random shuffle the two are equivalent.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1: trump card R2 (trump suit R); your cards are {hand}. Secretly bid how many of the '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1: trump card R2 (trump suit R); your cards are {hand}. Secretly bid how many of the '); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {hand} (in `prompt`: 'Hand 1: trump card R2 (trump suit R); your cards are {hand}. Secretly bid how many of the '); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (fallback, played_card, played_card, played_card) in `your_cards`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `card_order` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 4: passed
