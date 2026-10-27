# red7: ready for review

Built from the variation **Red3 Duel** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- In 2-player matches, a hand winner scores 1 point and the loser 0. The first player to 3 points wins (best of five hands). (fixes: In 2 players the 2/1 hand scoring makes the score gap equal hands won minus hands lost, so any 2-2 split reaches 6-6 and the match is a draw (about 35-37% of matches).): An odd number of hands is needed to decide, so 2-2 can never end the match. A fifth hand always settles it, and the useless consolation point disappears.
- The 1-point consolation for the last-eliminated player applies only in 3-player matches. (fixes: The 1-point consolation is meaningless in 2 players, because the loser of a hand is always the last eliminated.): Finishing order genuinely varies in 3 players and is worth fighting for there. In 2 players it adds nothing.
- In 3 players, a tie for most points is broken in favour of the tied player who won the most recently completed hand. This applies both at the 6-point end and at the round-40 cap. (fixes: In 3 players a tie for most points at or above 6 (for example a hand winner going 4 to 6 while the runner-up goes 5 to 6) ends in a draw, and a tie at the round-40 cap also gives no winner.): Each hand has exactly one survivor, so 'most recent hand winner' always picks out one player. It also rewards closing out the deciding hand.
- The player count is fixed at 2 or 3. (fixes: The stated player range must match the deck: 4 players cannot be dealt from 21 cards.): The deal of 5 hidden cards plus 1 palette card per player needs 12 or 18 of the 21 cards. That always leaves some cards unseen, which keeps inference alive.

Objective: The player with the most points when the match ends wins. With 2 players this is the first to 3 points, and a tie cannot occur at that end. If two or more players share the most points, which can happen in 3 players or at the round-40 cap, the tied player who won the most recently completed hand wins. If no hand was completed at all, the match is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SCORING TABLE PER HAND: with 2 players the winner gets 1 and the loser 0. With 3 players the winner gets 2, the second player out gets 1 and the first out gets 0, so 3 points are handed out per hand. KEY RANGES: strength runs from 11 (1 Violet) to 73 (7 Red), and all 21 strengths are distinct. A Red
- playable: pass. COMPLETENESS: the rules cover the deck, strength, EVEN and LOW, the three keys (including the 0 case), strict leading with ties (no tied player is leading), setup, the four turn options, the elimination triggers (not leading, fold, naming a card not held), the empty-hand forced fold, turn order, the
- reasoning_over_luck: pass. WHAT DECIDES A HAND: the deal sets resources, but Red7-style play rewards three skills. First, conserving cards: lead by the smallest margin and keep high, even and low cards for later. Second, timing rule switches to a colour where your palette dominates. Third, inferring the opponent's hand. In 2p

## Complexity

- steps_per_round: designed 15, built 14, limit 20
- choice_steps_per_round: designed 3, built 1, limit 4
- attributes: designed 13, built 56, limit 20 (built: 80)
- hidden_elements: designed 2, built 16, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: card 7 Red is stored as strength 73 when played to the palette
- pass: R2: 2-player deal gives 5 hand cards, 1 palette card, 9 set aside (counts only, deal is random)
- pass: R2: 3-player deal gives 5 hand cards, 1 palette card, 3 set aside (counts only, deal is random)
- pass: R3: a new hand resets the canvas to Red and deals fresh palettes (deal is random)
- pass: R4: under Red the key is the highest palette strength; 41+33 does not beat 52
- pass: R5: under Green two even cards (241) beat one even card (163)
- pass: R6: under Violet two low cards (221) beat one low card (133)
- pass: R7: a tie at 0 under Green is not leading, so the actor is eliminated
- pass: R8: playing 6 Green moves it from the hand to the palette
- pass: R9: discarding 4 Violet sets the canvas to Violet and the card goes to no palette
- pass: R10: play 2 Green then discard 4 Violet does both, and a card cannot be paired with itself
- pass: R11: a play that leaves the actor behind under Red eliminates them; their palette stays
- pass: R12: folding eliminates even a leading player
- pass: R13: with an empty hand the only option is fold, so the player is eliminated
- pass: R14: an eliminated player's high palette stays visible but does not count against others
- pass: R15: play passes to the next living seat, skipping an eliminated one
- pass: R16: one round is one turn for each living player, then it stops
- pass: R17: when only one player is left the hand ends at once and the survivor is the recent winner
- pass: R18: with 2 players the hand winner scores 1 and the loser 0
- pass: R19: with 3 players the winner scores 2, second out 1, first out 0
- pass: R20: after a finished hand the next round sets up a new hand (counts only, deal is random)
- pass: R21: with 2 players the match ends when a player reaches 3 points
- pass: R22: with 3 players the match ends after a hand in which a player reaches 6
- pass: R23: after round 40 the match ends and the unfinished hand scores nothing
- pass: R24: a tie on points goes to the most recent hand winner
- pass: R24: with no completed hand the match ends with no winner

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [2, 3], results {'seat 1': 14, 'seat 2': 15, 'seat 3': 11}, 3-21 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 8.7 decisions, prompts of 278 characters on average (longest 278)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 27, 'seat 2': 33}
- always `first@seat1`: won 22, lost 38, drew 0
- always `first@seat2`: won 25, lost 35, drew 0
- always `last@seat1`: won 11, lost 49, drew 0
- always `last@seat2`: won 11, lost 49, drew 0

## Choices the rules did not make

- 2 to 3 players, suggested 2: The designer's suggested size is 2, which keeps it a pure duel of reading the rival's palette and timing rule changes. The minimum is 2 because a duel needs a rival. The maximum is 3 because the deck and the scoring are only defined for 2 or 3 players.
- Cards are stored as their strength numbers (11 to 73): Number = floor(s/10) and colour = s mod 10, so every key is plain arithmetic on the list.
- Even numbers listed as three separate parameters (even_number_1..3 = 2, 4, 6): Parameters must be single numbers.
- No talk step: The rules say there is no table talk.
- Turns use sequential ask: Turns are taken one at a time in seat order, and each player sees the result of the turns before.
- The draw when no hand was completed is made with min_to_win 1: With no completed hand everyone ranks at 0 and nobody qualifies, giving no winner. Any completed hand gives someone at least 1 point.
- A player's strategy: Hold back strong cards. Switch the rule only when a discard both keeps you leading and leaves the rival needing cards they may not have. Read what a rival's palette implies about their hand.

## Simplifications

- Naming a card not held is never offered: Options are built from the player's hand, so the 'named a card you do not hold' elimination cannot arise.
- The turns within a round are a repeat loop over living players who have not yet acted: Turn order starts at turn_seat and must skip eliminated seats, and the loop must stop the moment a hand ends.
- The new-hand setup is a set of update steps each guarded by 'when hand_over': The step list is flat, so the setup steps run only when a new hand is needed.
