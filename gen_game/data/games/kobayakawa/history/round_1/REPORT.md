# kobayakawa: needs review

Built from the variation **Kobayakawa: Held Cards** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- FIGHT becomes a sequential choice in seat order. It starts with the player who won the last pot. If the last pot was not won, it starts with the seat after the previous start player. Everyone sees all earlier decisions and stakes before choosing. (fixes: P1): Later players can read commitments, and early players can try to deter others. Rotating the start and carrying tied pots keep any seat from having a built-in edge. The winner acting first next round is a small catch-up brake.
- Fighters choose LOW (the minimum stake: 1, or 2 in round 10) or HIGH (minimum + 1). Once anyone has fought HIGH, every later fighter in that round must also stake HIGH. Earlier LOW fighters do not top up. The pot winner takes everything. (fixes: P2, P4): A raise signals strength or bluffs it, and it raises the price for later callers. Reading stakes becomes part of opponent modelling.
- Cards carry between rounds. A player who passes keeps their hand card into the next round. Every fighter's card is discarded after the fight, and the fighter gets a fresh card next round. (fixes: P3): Holding a strong card until a favourable Kobayakawa appears becomes a multi-round plan. Opponents can infer a held card from a pass history, from discards and from draw behaviour. Fresh luck enters only after fights.
- Keep the simultaneous talk phase before the fight. Messages are short and shown all at once. (fixes: P4): Only one player takes each pot, so claims such as 'I'm holding a high card' are real bluffs or deterrents. Combined with the sequential fight, claims can now be tested against actions.

Objective: When the game ends, the player with the most kamons wins. If two or more players tie for the most, the game is a draw. If only one active player remains before round 10, that player wins.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. KAMON ACCOUNTING. Total kamons = 4N + 11. The centre feeds 1 kamon in each of rounds 1-9 (9 kamons) and the remaining 2 in round 10, so the centre empties exactly. The only leaks are round-10 split remainders and a pot that is left unclaimed after round 10.

SHOWDOWN TABLE (two fighters, cards a < b
- playable: pass. COMPLETENESS. The rules cover the deal, the three draw options, the keep/discard step, the shift trigger (any single SHIFT forces the replacement; 'vote' is loose wording but the trigger is unambiguous), required stakes after HIGH, the forced pass for players short of kamons, scoring for 0, 1 and 2+
- reasoning_over_luck: pass. WHAT THERE IS TO INFER.
- Opponents' hand ranges, from the announced draw choices, face-up discards, which players are holding kept cards and for how long, talk, and fight order.
- The chance of K changing: SHIFT is announced, the Alternate is hidden, and the spent cards are known.
- Whether lone-fi

## Complexity

- steps_per_round: designed 15, built 22, limit 20
- choice_steps_per_round: designed 4, built 4, limit 4
- attributes: designed 17, built 41, limit 20 (built: 80)
- hidden_elements: designed 3, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 10, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: 4 kamons each, centre 11, pot 0, start seat 1, round 1, no held cards
- pass: Deck excludes a held hand card: 3 players, one held card, deck ends round with 15-3-3-2=7
- pass: Players with no card are dealt one; all pass and keep it (held_rounds 1)
- pass: Reserves, Kobayakawa and Alternate dealt: 4 players leave 15-4-4-2=5 in deck (values are chance)
- pass: Minimum stake 1 in round 1: lone LOW fighter pays 1 and takes pot 2
- pass: Minimum stake 2 in round 10: LOW costs 2, seat with 2 kamons gets no HIGH
- pass: Announced round state advances: everyone passes in round 4
- pass: Every seat is offered KEEP, DRAW, SHIFT and its choice is recorded
- pass: Only the drawer is asked OLD or NEW
- pass: NEW replaces the held card (held_rounds reset, then +1 for passing); OLD keeps it
- pass: Undrawn reserves are discarded: reserves list is empty after the draw step
- pass: Draw choices revealed: one DRAW-NEW, others KEEP
- pass: A SHIFT voter keeps their hand card (new Kobayakawa value is chance, not asserted)
- pass: Talk step runs and the round completes normally
- pass: Fight starts at start seat 3: seat 3 may fight LOW, later seats see its HIGH and get no LOW
- pass: With exactly 1 kamon, LOW is offered but HIGH is not; LOW stakes 1
- pass: With 2 kamons HIGH is offered and stakes 2
- pass: After a HIGH, later seats are not offered LOW but may still fight HIGH
- pass: Seat with 1 kamon after a HIGH is forced to pass: no stake, keeps card
- pass: Fighters pay stakes 1 and 2; card 1 plus Kobayakawa (>=3) beats card 2 and takes pot 4
- pass: Rounds 1-9: centre feeds 1 kamon to the pot
- pass: Rounds 1-9: an empty centre feeds nothing
- pass: Round 10: whole centre (5) moves to the pot; nobody fights, all level
- pass: Nobody fights: pot of 3 carries and grows to 4, start seat moves on
- pass: Lone fighter takes the whole pot (2 carried + 1 stake + 1 centre)
- pass: Showdown: lowest card 1 gets the Kobayakawa (>=3) and beats card 2
- pass: Two fighters in round 1 (a tie depends on chance): only stakes, centre and card cleanup asserted
- pass: Round 10 showdown (tie depends on chance): the pot is emptied either way
- pass: Cleanup: fighter's held_rounds goes to 0, passer's held card count rises
- pass: No pot winner: start seat moves from 3 to the next active seat, wrapping to 1
- pass: Pot winner becomes the next start seat
- pass: A fighter left with 0 kamons is eliminated
- pass: Game ends when only one active player remains: card 1 beats cards 2 and 3
- pass: Game ends after round 10: most kamons wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 10, 'seat 3': 8, 'seat 1': 12, 'seat 5': 6, 'seat 4': 4}, 70-160 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 110.3 decisions, prompts of 204 characters on average (longest 289)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 22, 'seat 3': 21, 'seat 1': 17}
- always `first@seat1`: won 0, lost 60, drew 0
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 30, lost 30, drew 0
- always `last@seat2`: won 20, lost 39, drew 1

## Triage (whose problem each failure was)

- round 1: fix_tests: The game applied the rule correctly. Seat 2 had 1 kamon after seat 1 fought HIGH (stake 2), so the game recorded PASS for it without asking: fight_choice = PASS, stake 0, kamons still 1, held_rounds now 1, and seat 1 took the pot as the sole fighter. The test failed only because it required a menu offering PASS. A forced pass with no menu has the same result under the rules.
- round 1: revise_rules: The game was built and behaves as specified, but the design needs 22 steps per round, over the engine's limit of 20. The excess comes from the rules, not a coding mistake. A thoughtless 'always last option' policy also wins about half its games from seat 1, which hints that blind aggression pays too well.

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer chose 4. Three is the smallest table where fight order, reads and pot competition work. Five fits the 15-card deck: up to 5 hands, 5 reserves and 2 table cards is 12 cards, and more players would stretch the fight sequence.
- Talk kept as one simultaneous poll: The source specifies it. Bluffing about hand strength gives players something to disagree about.
- A SHIFT voter keeps their hand card: SHIFT replaces neither the hand nor the reserve, so the hand stays.
- Next start seat chosen after eliminations, skipping eliminated seats: The source says 'next active seat'.
- Centre feed in rounds 1-9 is limited by what remains: The centre cannot go negative.
- A drawer who keeps NEW has held_rounds reset to 0: Their card is no longer one kept from an earlier round.

## Simplifications

- A tie for the most kamons is a shared win rather than a declared draw: The engine treats players level at the top as sharing the win, with no separate draw.
- Reserve cards are kept in a hidden table list, indexed by seat: A player attribute cannot be hidden from its own owner, and the rules say the reserve is unseen until drawn.
