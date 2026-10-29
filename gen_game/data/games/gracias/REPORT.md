# gracias: ready for review

Built from the variation **Gracias: The Counted Gift** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a finite 48-card deck (12 per colour), shuffled once at the start of each session (rounds 1, 5 and 9 only). Each round, deal by removing the top 12 cards of the shuffled list into 4 triplets. (fixes: P1: Randomness exceeds the platform): One shuffle per session is a single random draw, and dealing becomes list removal, the supported workaround. No round has more than one draw.
- All 48 cards are used every session. Face-up cards, keeps and gifts are public, so each colour's hidden total among opponents equals 12 minus all public cards of that colour minus your own hidden cards of it. (fixes: P3: No inference): Card counting lets players infer what rivals are hiding, so gifts that push a rival into a majority or away from a stack are planned rather than guessed.
- Restore the triplet draft. Each round, the 4 triplets are laid out with their two face-up cards shown. Players pick in turn, the start seat rotating each round. Each pick names the triplet, which face-up card to keep and which opponent receives the other. (fixes: P5: The previous variation removed the draft (also reduces P2)): Players choose among offers instead of receiving a private random deal, so decisions outweigh the deal. Rotation gives each seat first pick 3 times and last pick 3 times. Picking in turn lets later players react to earlier gifts.
- Use stacks of 4 worth 3 points each. Loose cards are worth 1 each, with loose = total mod 4 (0-3). Majority discard applies to the highest loose value per colour (ties all discard). (fixes: P4: The majority discard was nearly meaningless; P6: The stack value made the swing small (also reduces P2)): Loose values now range 0-3 and genuinely differ between players. Completing a rival's stack (+3 to them) versus pushing them into the majority is a large, readable swing.
- Drop the talk phase. (fixes: P1: Randomness exceeds the platform (keeps the build within limits)): Four turn-based picks already use the full 4 choice steps per round. The conflict over who gets burdened is expressed directly through public gifts in turn order.

Objective: After session 3, the player with the highest game total wins. If several players tie, the one among them with the highest best session score wins. If they are still tied, the game is a draw among them.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. PER-COLOUR SCORE TABLE (total = public + hidden; stacks = floor(t/4), loose = t mod 4). Format is score if your loose is not the highest / score if it is the highest (tied or alone). t0: 0/0. t1: 1/0. t2: 2/0. t3: 3/0. t4: 3 (immune). t5: 4/3. t6: 5/3. t7: 6/3. t8: 6 (immune). This gives three tensi
- playable: pass. RULES COMPLETENESS. The deck size matches usage: 48 cards = 4 rounds x 12, with shuffles only in rounds 1, 5 and 9. Pick order, gift rules (must gift, not to self), the forced last triplet, reveal, stacks, loose, the ties-all-discard rule, scoring, reset and the tie-break are all specified with arit
- reasoning_over_luck: pass. CHANCE SOURCES: the deck order sets which A/B cards appear in which round, and which H card lies under each triplet. Each player receives 4 random hidden cards per session, which affects whether colours reach 4. SKILL SOURCES: (1) Counting. The colour make-up of the unseen cards is exactly computabl

## Complexity

- steps_per_round: designed 15, built 14, limit 20
- choice_steps_per_round: designed 4, built 1, limit 4
- attributes: designed 14, built 59, limit 20 (built: 80)
- hidden_elements: designed 2, built 18, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 12, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: a match starts from a full 48-card deck and 12 cards are dealt in round 1, leaving 36
- pass: R1: four rounds from setup complete session 1 and the match moves on to session 2
- pass: R2: in round 5 an empty deck is refilled to 48 before the deal, leaving 36
- pass: R2: round 2 does not refill the deck (24 cards become 12)
- pass: R3: after the 4th round of a session the deck is empty
- pass: R4: with an all-Red deck every face-up card offered is Red
- pass: R5: round 3 pick order is seats 3, 4, 1, 2, so seat 2 picks last and only T4 is left
- pass: R6: a picker may gift to any opponent but never to itself
- pass: R7: kept, gifted and hidden Red cards count, so seat 1 with 1 Red before round 4 ends on 4 Red (one stack, 3 points) and the others discard 3 loose
- pass: R8: three gifts to seat 1 give it 5 Red (3+1); seat 2 discards 3 loose; seats 3 and 4 keep 2
- pass: R9: the hidden card counts for the picker, so seat 1 with no gifts still totals 2 Red
- pass: R10: the last picker in round 2 (seat 1) sees only T4 but still chooses which card to keep and whom to gift
- pass: R11: a mid-session round only advances the round, with no session score
- pass: R12: at the session end, public and hidden counts add up to totals before scoring
- pass: R13: a total of 7 gives 1 stack and 3 loose (seat 1 scores 3); a total of 6 gives 1 stack and 2 loose kept (seat 2 scores 5)
- pass: R14: players tied on the highest loose value all discard (Red 3,3,3,3; Blue loose 2,2,1,0)
- pass: R15: Red total 5 with a Red max loose of 2 scores 3+1 = 4
- pass: R16: the session score adds to game_total, and best_session_score changes only when beaten
- pass: R17: after the session-end reset the next session starts and round 5 adds no score
- pass: R18: the game ends after round 12; seat 1 wins on game_total plus tie-break
- pass: R19: seats tied on game_total and best_session_score share the win; a lower best loses the tie

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 1': 7, 'seat 3': 4, 'seat 4': 6, 'seat 2': 3}, 48-48 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 48.0 decisions, prompts of 169 characters on average (longest 169)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 17, 'seat 3': 13, 'seat 4': 14, 'seat 2': 16}
- always `first@seat1`: won 10, lost 50, drew 0
- always `first@seat2`: won 3, lost 55, drew 2
- always `last@seat1`: won 9, lost 50, drew 1
- always `last@seat2`: won 11, lost 49, drew 0

## Triage (whose problem each failure was)

- round 1: fix_tests: The game plays correctly. Each pick is offered as one combined option, such as 'T1: keep A (Yellow), give B (Red) to seat 2'. The rules do not prescribe option labels, and a single combined choice is a valid way to make the triplet, keep and gift decision. The tests fail only because they expect separate options named exactly 'T1', 'keep A' or 'Red', which the game never offers. The game's round and session progress (round 5, session 2 after 4 rounds) and the round-3 pick order (seats 3, 4, 1, 2) match the rules.

## Choices the rules did not make

- Exactly 4 players (min = max = suggested = 4): The designer fixed 4. The 4 triplets per round, 12 cards per colour and the rotating first pick are all sized to 4 seats. The game is about counting cards and gifting tactically against several rivals, and it needs 3 opponents to choose among as gift targets.
- No talk step: The source has no communication phase. Adding one would add a mechanic.
- The whole pick (triplet, which card to keep, receiver) is asked as one choice from a generated list: The source resolves the pick as a single action. One question keeps it atomic and offers only legal combinations.
- rank_by multiplier 1000: best_session_score is far below 1000, so game_total always dominates and the best session only breaks ties.
- totals, stacks, loose and max_loose kept as 4-element lists in the order Red, Blue, Green, Yellow: The rules name these values, so they are declared, and lists keep the attribute count manageable.
- Strategy at the table: A thoughtful player counts the unseen cards to estimate opponents' hidden colours, completes stacks of 4, and gifts cards that push a rival into a majority-loose discard or past a stack boundary that breaks their leftovers.

## Simplifications

- Shuffling and dealing from the top is modelled as drawing 12 cards at random without replacement from the deck list each round, with the deck refilled only at rounds 1, 5 and 9: This has the same distribution as one shuffle per session followed by top-card dealing, and it is the engine's way to draw.
- The session-end reveal is a broadcast of hidden counts rather than a change in visibility: Attribute visibility is fixed. Announcing the values gives everyone the same information.
