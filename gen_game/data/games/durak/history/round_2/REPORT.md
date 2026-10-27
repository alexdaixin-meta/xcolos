# durak: needs review

Built from the variation **Duel Durak (seeded)** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Randomness happens exactly once, at step 1 of round 1. The 36-card deck is built as an ordered list: Clubs, Diamonds, Hearts, Spades, and ranks 6 to 14 within each suit, with card id = suit index × 9 + rank − 6. The engine's seeded shuffle is applied to this list. Cards are dealt by fixed positions: positions 1–8 to player 1, then 9–16 to player 2, and 17–36 to the set-aside list in that order. No other random operation, clock value or external source is used anywhere. (fixes: P1: Non-determinism): The game has a single seeded source of randomness, so the same seed always gives the same deal.
- All hands, the discard pile and the set-aside pile are stored as ordered lists sorted ascending by card id. Every announcement and every fallback reads them in that order. Nothing iterates over a set or map. (fixes: P1: Non-determinism): This removes output and fallbacks that depend on iteration order.
- Every fallback is a fixed rule on ordered data. An illegal or missing offer becomes Hearts and Spades. An illegal or missing trump pick becomes the first offered suit in suit order. An illegal or missing attack becomes the attacker's lowest-rank card, with ties broken by lower suit index. An illegal or missing defence counts as TAKE. An illegal or missing throw-in counts as PASS. (fixes: P1: Non-determinism; P6: guaranteed end and deterministic resolution): Every fallback is deterministic and reproducible.
- Two players, 8 cards each, no drawing. The other 20 cards stay set aside face down and are never used. (fixes: P2: talon luck and repeated draws; P4: seat and coalition effects): This removes talon luck and repeated draws. It keeps a real inference problem: 28 unseen cards, of which 8 are in the opponent's hand.
- Each bout has one attack, one optional throw-in matching a rank on the table, and up to two defences. (fixes: P3: too many choice steps): This keeps choice steps at 4 per round while keeping attack, defend, take and add.
- The trump suit is chosen by cut-and-choose. Player 2 offers two different suits, and player 1 picks one of them as trump. The holder of the lowest trump attacks first. If neither player holds a trump, player 2 attacks first. (fixes: P5: deal deciding the game): Player 2 must offer two suits it can live with, and player 1 chooses after reading its own hand. Reasoning can offset a lopsided deal, and the two seat roles balance each other.
- The game ends when a hand empties, with a cap at round 40. At the cap, the player with fewer cards wins, and equal counts are a draw. (fixes: P6: guaranteed end and deterministic resolution): This guarantees an end with an arithmetic result.

Objective: The first player whose hand reaches 0 cards after a bout wins. If both reach 0 at the same resolution, the game is a draw. If round 40 ends with both players holding cards, the player with fewer cards wins; equal counts are a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. STRUCTURE. The game is zero-sum. There are 8 cards each and no drawing; 20 cards are set aside. A beaten bout removes the same number of cards from both hands (1 or 2 each), so the card counts stay equal until someone says TAKE. A TAKE adds the table to the taker's hand and keeps the initiative with
- playable: pass. Two players, so the rule on talk does not apply. The game is zero-sum, so the cooperation check does not apply.

RULES ARE COMPLETE.
- Card ids are unique, so 'lowest-rank trump' never ties.
- Every choice step has a deterministic fallback computed from the sorted lists.
- The beat test is arithmeti
- reasoning_over_luck: pass. CHANCE. Chance enters only through the deal of 8+8 cards from 36. On average about 4 cards of a given suit are dealt in total (16 × 9/36).

PLAYER CONTROL. Players, not the deck, set the trump. Player 2 offers suits matching its hand, and player 1 picks between them. A deal that is weak in one suit 

## Complexity

- steps_per_round: designed 16, built 17, limit 20
- choice_steps_per_round: designed 4, built 6, limit 4
- attributes: designed 18, built 40, limit 20 (built: 80)
- hidden_elements: designed 3, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: id 9 is the 6 of Diamonds and id 10 the 7 of Diamonds, so 10 beats 9 and the bout is beaten off
- pass: R2: after the deal each seat holds 8 cards, set_aside holds 20 and the deck holds 36
- pass: R3: set_aside is never drawn from, so it still holds 20 cards after the first bout (seeded deal, only counts that chance cannot change)
- pass: R4: with default 'last' seat 2 offers Spades and Hearts and seat 1 takes the last suit, Spades
- pass: R5: with default 'first' seat 2 offers Clubs and Diamonds and seat 1 takes the first suit, Clubs
- pass: R6: seat 1 holds the lowest Club trump (8 of Clubs, id 2), so seat 1 attacks first
- pass: R6: neither seat holds a Club trump, so seat 2 attacks first
- pass: R7: the 7 of Clubs (trump) beats the 6 of Hearts and the 6 of Spades does not
- pass: R8: the attacker plays the chosen card and the defender, unable to beat it, takes it
- pass: R9: the defender may say TAKE although it holds beating cards; only cards that beat the attack are offered
- FAIL: R10: the attacker throws in a card of a rank on the table; a card of another rank is not offered | rule R10 is broken: When the attacker may throw in, then they add one card whose rank matches the rank of a card on the table, or PASS; a missing or illegal answer is PASS; at most 1 card is thrown in per bout.; seat 1 was offered 20, but must not be
- FAIL: R11: once the defender has beaten the attack with its last card, the attacker may not throw in, and the defender wins | rule R11 is broken: When the defender has not said TAKE and has 0 cards in hand, then the attacker may not throw in.; seat 1 was offered 18, but must not be
- pass: R12: a card thrown in after TAKE goes to the defender too
- pass: R13: the defender beats the thrown-in card too, so the bout is beaten off
- pass: R14: after TAKE the defender gains the table cards and the same seat attacks again
- pass: R15: a fully defended bout is discarded and the defender becomes the attacker
- pass: R16: after a bout both hand sizes reflect the result and the bout count rises by one
- pass: R17: the attacker plays its last card, the defender takes it, and the attacker wins with 0 cards
- pass: R18: both seats play their last card in the same bout, so the game is a draw
- pass: R19: after bout 39 the seat with fewer cards wins
- pass: R19: after bout 39 with equal hand sizes the game is a draw

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 10, 'seat 1': 10}, 13-45 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 23.0 decisions, prompts of 110 characters on average (longest 132)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 33, 'seat 1': 27}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 44, lost 15, drew 1
- always `last@seat2`: won 36, lost 24, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: In the failing scenario the attack was 61 (6 of Clubs) with Spades as trump, and the defender held 94, 104 and 114, all Spades trumps, so a one-card defence is a legal beat under rule (b). The game instead recorded defence_cards [999], treated the defence as TAKE and gave seat 2 four cards; the other three failures are the same bug: valid defences fail, so hands and penalties come out 2 too high.
- round 1: fix_game: In the failing scenario the trump was Spades and the defender held 94 (9 of Spades, a trump) against an attack of 61 (6 of Clubs), yet the game offered the defender only ['TAKE']. That is a legal beat under the rules, so the tests' expected discard (defender left with 2 cards) is correct, and the game never builds the defence options. The penalty failures follow from this same bug, because a defender who can never defend keeps picking up cards.
- round 1: fix_game: The rules have only one random event, the S1 shuffle at the start of each deal, and the platform supports seeded deck handling. Different logs from the same seed mean the game file brings in its own non-determinism: an unseeded draw, a clock, or iteration over an unordered collection.
- round 2: fix_tests: The offer, trump-pick and first-attacker scenarios run with "rounds": 0, so no moves are played (the log shows 'moves played: .'). Round 1, where seat 2 offers and seat 1 picks, never happens, and trump correctly stays -1. The game did the deal correctly, so the failures come from the test setup, not the game file.
- round 2: fix_game: The rules make round 1 setup only, with no bout, and bouts run in rounds 2 to 40. The game plays a full bout inside round 1 as well: in R1 seat 1 attacked 9, seat 2 beat it with 10 and seat 1 passed, all in r1. As a result `bout` is one ahead everywhere (R1, R3, R4), and in R4 cards changed hands after only the setup round.
- round 2: fix_game: The R10 and R11 failures show the game offering the attacker throw-in cards it may not play. In R10 it offered card 20 (the 8 of Hearts), whose rank matches nothing on the table. In R11 it offered card 18 after the defender had beaten the attack with their last card, when the rules forbid any throw-in. These are implementation errors in the throw-in step, not problems with the rules.
- round 2: fix_game: The throw-in options are wrong in the game file. In R10 the table holds 9 (6 of Diamonds) and 1 (7 of Clubs), so only rank-6 and rank-7 cards may be thrown in, but the game offered 20, the 8 of Hearts. In R11 the game offered a throw-in after the defender had beaten the attack with its last card, which rule Step 7 forbids.

## Choices the rules did not make

- 2 players, suggested 2: The designer fixed the table at 2. This is a head-to-head duel of card management, where a thoughtful player saves trumps, chooses the trump offer to fit their own hand, and throws in to unload cards.
- No talk step: The source has no talk, and in a two-player zero-sum duel talk adds nothing to reason about.
- Draw expressed as a shared top rank: rank_by = -hand_size makes both seats level when both have 0 cards or equal counts, and the engine treats a level top as shared, which is the draw.
- The bout counter ends the game at 39 bouts: Rounds 2 to 40 are 39 bouts.

## Simplifications

- The source's round 1 is modelled as setup steps: It runs once before the bouts.
- Dynamic attacker and defender are named by the attacker attribute: The engine addresses seats, so the roles are read from a table number.

## Encoding attempts

- 1: it plays, but part of it does nothing: game attribute `positions` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `suit_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 2: passed
