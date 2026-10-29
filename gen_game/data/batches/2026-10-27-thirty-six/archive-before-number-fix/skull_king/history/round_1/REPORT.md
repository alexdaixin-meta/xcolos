# skull_king: needs review

Built from the variation **Skull King: Three-Card Raids** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Every round is one hand of exactly 3 cards: one bid poll then 3 tricks, each played as a poll where everyone plays at the same time. (fixes: Too long and too many choices per round: a hand of i cards needs i sequential trick turns per player, far over 4 choice steps and 20 steps per round.): Gives 4 choice steps per round and about 12 steps in total. Playing at the same time keeps the core tension of guessing what others will commit, without turn order.
- Remove suits, follow-suit, trump and Scary Mary. Use an 18-card deck where each card has a power number (Escape 0, numbers 1-12, Mermaid 20, Pirates 30 and 31, Skull King 40), with one exception: the Mermaid wins any trick containing the Skull King. (fixes: Follow-suit, lead-suit and trump rules plus the Scary Mary declaration create long rule chains that are hard to build and check.): The trick winner becomes a single max-and-one-exception calculation while keeping the signature Pirate, Mermaid and Skull King cycle.
- Trick winner rule written as arithmetic on power values, with distinct values for the two Pirates so there are no ties among cards that can win. (fixes: Trick-winner resolution with special-card exceptions needs to be expressible as arithmetic to be built reliably.): The engine can compute the winner directly, and no judge is needed.
- Fixed 3-card hands over 8 rounds with a small deck. All played cards are public, and 3 to 6 cards stay unseen each round depending on player count. Bonuses are moderate (+20 per Pirate captured by the Skull King, +40 for the Skull King captured by the Mermaid) and paid only on an exact bid. (fixes: Large deck and growing hand sizes give a big hidden state, and hand-to-hand luck swings (large special bonuses) can swamp skill within one game.): Smaller, repeated, comparable hands average out deal luck. Card counting and reading bids become the decisive skill, and the bonuses stay flavourful without dominating.

Objective: After 8 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Exact-bid payoffs: bid 0 = +30; bid 1 = +20; bid 2 = +40; bid 3 = +60, plus capture bonuses. A miss costs -30 on a zero bid and -10 per trick of difference otherwise. No bid is strictly best, because the right bid depends on the hand. Weak hands favour 0 (+30). Strong hands favour 2-3 (+40/+60). A m
- playable: pass. The rules are complete:
- the deal, the bid range 0-3, the simultaneous reveal and the 3 simultaneous tricks are all defined;
- trick resolution is fully specified, including Mermaid+SK+Pirate together, where Mermaid wins and earns +40;
- SK capture bonuses (+20 per Pirate) are defined;
- scoring co
- reasoning_over_luck: pass. Luck comes only from the deal. Its influence is limited:
- The per-round ceiling is +60 (+bonuses) for strong hands and +30 for weak hands, and a weak hand can almost guarantee +30 by bidding 0. For example, holding 1-2-3, your 1 wins only if both opponents play Escapes.
- I estimate the deal-driven

## Complexity

- steps_per_round: designed 12, built 17, limit 20
- choice_steps_per_round: designed 4, built 3, limit 4
- attributes: designed 10, built 39, limit 20 (built: 80)
- hidden_elements: designed 1, built 6, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: at the start every score is 0 and no round has been played
- FAIL: R2: after one round the round counter is 1 (the dealt cards are random, so they are not asserted) | rule R2 is broken: When a round starts, then the full 18-card deck (numbers 1-12, two Escapes of power 0, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40) is shuffled and each player receives exactly 3 cards in their private hand.; seat 1 bid: expected 1, got 0; Ada: the rule for 1 was never matched (the game never put that option to this seat)
- FAIL: R3: a 5-player round deals and plays through (the undealt cards are hidden, so they are not asserted) | rule R3 is broken: When cards are dealt, then the undealt cards stay in deck and are never revealed that round.; seat 5 bid: expected 2, got 0; Eli: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: R4: each seat's bid is recorded as entered and the bid range 0 to 3 is offered | rule R4 is broken: When players bid, then each chooses simultaneously a whole number from 0 to 3, and all bids are revealed only after all are in.; seat 2 bid: expected 1, got 0; seat 3 bid: expected 2, got 0; seat 4 bid: expected 3, got 0; seat 1 was never offered 0, but should have been; seat 2 was never offered 0, but should have been; seat 4 was never offered 3, but should have been; Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: R5: the three tricks are played from a random hand (only the bids and the round counter are asserted) | rule R5 is broken: When a trick is played, then each player simultaneously plays one card from their own hand, and that card is removed from the hand and revealed to all.; seat 1 bid: expected 2, got 0; seat 2 bid: expected 1, got 0
- FAIL: R6: a round with Mermaid/Skull King resolution plays through (the deal is random, so only deal-independent facts are asserted) | rule R6 is broken: When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick.; seat 1 bid: expected 1, got 0
- FAIL: R7: a highest-card trick round plays through (the deal is random, so only deal-independent facts are asserted) | rule R7 is broken: When the Mermaid and the Skull King are not both in a trick and some card has power above 0, then the player of the highest-power card wins the trick.; seat 2 bid: expected 3, got 0; Blaise: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: R8: a 3-player round plays through (with only 2 Escapes every trick has a winner; only deal-independent facts are asserted) | rule R8 is broken: When every card played in a trick has power 0, then nobody wins the trick and no tricks_won changes.; seat 3 bid: expected 1, got 0
- pass: R9: tricks are won during the round and tricks_won is back to 0 after scoring (deal-independent)
- FAIL: R10: a Skull King capture round plays through (the deal is random, so only deal-independent facts are asserted) | rule R10 is broken: When the Skull King wins a trick, then its player records a bonus of +20 for each Pirate (30 or 31) in that trick.; seat 3 bid: expected 2, got 0; Cleo: the rule for 2 was never matched (the game never put that option to this seat)
- FAIL: R11: a Mermaid capture round plays through (the deal is random, so only deal-independent facts are asserted) | rule R11 is broken: When the Mermaid wins a trick containing the Skull King, then its player records a +40 bonus.; seat 4 bid: expected 1, got 0
- pass: R12: a zero bid is recorded and tricks_won resets after scoring (the trick outcome is random, so it is not asserted)
- FAIL: R13: all seats bid 0 and the bids are recorded (the trick outcome is random, so it is not asserted) | rule R13 is broken: When a player bid 0 and won 1 or more tricks, then they score -30 for the round.; Blaise: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: R14: a bid of 1 is recorded (whether it is made depends on the deal, so the score is not asserted) | rule R14 is broken: When a player bid k >= 1 and won exactly k tricks, then they score 20*k plus all bonuses recorded that round.; seat 2 bid: expected 1, got 0
- FAIL: R15: all seats bid 3 and the bids are recorded (the deal decides who makes it, so the score is not asserted) | rule R15 is broken: When a player bid k >= 1 and won a different number of tricks t, then they score -10*|k - t| and no bonuses.; seat 1 bid: expected 3, got 0; seat 2 bid: expected 3, got 0; seat 3 bid: expected 3, got 0; Ada: the rule for 3 was never matched (the game never put that option to this seat); Blaise: the rule for 3 was never matched (the game never put that option to this seat); Cleo: the rule for 3 was never matched (the game never put that option to this seat)
- FAIL: R16: after a round's scoring every tricks_won is reset to 0 | rule R16 is broken: When a round's scoring ends, then each player's tricks_won, round points and score are announced, and tricks_won and bonus reset to 0.; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- pass: R17: round 8 ends the game and a seat 1000 points ahead wins (one round can change a score by at most +100/-30)
- FAIL: R17: the game ends after round 8 even with one seat far behind, and the leader wins | rule R17 is broken: When round 8 has been scored, then the game ends and the highest score wins; players tied for the highest score share the result (a draw).; Blaise: the rule for 1 was never matched (the game never put that option to this seat)
- pass: R18: a round runs bid and tricks with no talk phase (the round completes)

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `repeat` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 11, 'seat 1': 14, 'seat 3': 5, 'seat 5': 4, 'seat 4': 5, 'seats 1 and 4': 1}, 70-120 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 96.0 decisions, prompts of 126 characters on average (longest 162)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 18, 'seat 1': 25, 'seat 3': 16, 'seats 1 and 2': 1}
- always `first@seat1`: won 11, lost 46, drew 3
- always `first@seat2`: won 8, lost 50, drew 2
- always `last@seat1`: won 5, lost 55, drew 0
- always `last@seat2`: won 2, lost 57, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: The failing assertions check `deck` and `hand`, which are the coder's own bookkeeping and not part of the interface. The deck is legitimately refilled to 18 for the next round's shuffle, so expecting 9 or 3 left after the round misreads the rules. The bid and 'rule never matched' failures come from the tests' choice scripting: they expect bids to be offered as a fixed menu containing 1, the game never offered such a menu, so the default choice of 0 was entered and the bid checks failed.
- round 1: fix_game: The trace shows only 12 moves in round 1. That is exactly three simultaneous card plays of 4 seats, so the game never polls a bid: `bid` stays at its starting 0, and seats are never offered 0-3. The tests correctly expect the bid each seat enters to be recorded, and the rules do not reset bids at round end.
- round 1: fix_game: The tests correctly expect each player to be offered the bids 0, 1, 2 and 3 and to have the chosen value recorded in `bid`. In the game file, the bid step never offered those options (not even 0), so every seat's bid stayed at the default 0 and the bid-0 scoring followed from that.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4. Three is the smallest table where tricks are contested enough for bidding to be hard. Five is the cap because 15 of the 18 cards are dealt, and more seats would exhaust the deck.
- Cards are stored as their power values: Every card except the two Escapes has a unique power, so the value identifies the card, and resolving a trick is plain arithmetic on played.
- Trick steps are written once and run again with repeat until trick_number == 3: The three tricks are identical in the source.
- No talk step: The source states there is no talk phase.
- Strategy at the table: A thoughtful player bids from hand strength and from what others' bids imply. During tricks they dump Escapes or low cards to hit a bid exactly, or hold the Mermaid back to catch the Skull King.

## Simplifications

- A tie for the highest total is a shared win rather than a separate 'draw' outcome: The engine has no separate draw; players level at the top share the win, which is equivalent.

## Encoding attempts

- 1: an option is offered and then refused (see the offer-only-what-is-allowed pattern): refused: seat 1 was offered 31 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards | refused: seat 2 was offered 4 in `play_a_card`, picked it, and was asked again without it (round 1): the first offer held an option that was not allowed. Offer each seat only what it may do, from its own state, instead of refusing afterwards
- 2: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
