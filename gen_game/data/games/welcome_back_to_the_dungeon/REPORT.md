# welcome_back_to_the_dungeon: ready for review

Built from the variation **Dungeon Dare** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- The runner also fights the top 2 cards still in the deck, revealed at run time. The adventurer's base HP is lowered to 3, so a run with no equipment is almost always lethal. (fixes: P1: Never passing (always stripping or always adding) is a winning policy.): Every run now carries hidden danger, and stripping all the equipment then running is suicide. A player who never passes ends up running a stripped dungeon and fails.
- Points replace successes and eliminations. A successful runner gains 2 points. A failed runner loses 1 point (not below 0). When the runner fails, each player who passed earns 1 point, but only if they added at least one monster to that dungeon. (fixes: P2: Passing earns nothing.): Passing at the right moment now pays: build a deadly dungeon, then leave. Passing immediately pays nothing, so always-pass sits at 0 and loses. Running pays more than passing, so someone still wants to stay in.
- The leader (first to act) rotates seat by seat each dungeon. There is one fixed adventurer kit. (fixes: P3: There are seat imbalances.): This removes the persistent first-seat effect and the winner's choice of adventurer.
- The first to 4 points wins, checked after each run, with a cap of 40 turns. At the cap the highest total wins, and a tie for highest is a draw. There is no elimination. (fixes: P4: Elimination and 'two successes' make length open-ended.): Gives a bounded length, keeps all players active, and one run is not decisive.
- One engine round is one player's turn. The only random event is the shuffle at the start of a new dungeon. Drawing takes the top card of the already-shuffled deck. (fixes: P5: Platform limits.): This fits the limit of one random draw per round and a flat step list.
- A short simultaneous message phase is held each turn before the active player acts. (fixes: P2: Passing earns nothing.): Players disagree about who should be left holding the dungeon. Bluffing about what you added ('only goblins in there') is the heart of the original.

Objective: When the game ends, the player with the most points wins. If two or more players tie for the most points, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. BASELINE. Full kit gives HP 3+4+3 = 10. TORCH removes the 1s, 2s and 3s; SPEAR removes the 7 and the 9. The live threats are 4,4,5,5,6, which total 24 over 13 cards, so each card carries about 1.85 expected damage. Empty dungeon with full kit: the run fails only if both deck cards are threats summin
- playable: pass. The rules are complete:
- deck size and contents are given;
- legal options are listed in a fixed order;
- the forced pass at 2 or fewer deck cards guarantees 2 cards are left for the run;
- all three can never pass, because the run triggers at exactly one IN player;
- the PASS card returns to the t
- reasoning_over_luck: pass. WHERE CHANCE ENTERS.
- The shuffle decides which card each player draws.
- The 2 blind deck cards in the run add about 3.7 expected effective damage against a 10 HP budget.
- Rough estimate: chance is about 35-40% of a single run's outcome.
WHAT GOOD PLAY CONTROLS.
- Players decide whether each thre

## Complexity

- steps_per_round: designed 16, built 12, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 15, built 61, limit 20 (built: 80)
- hidden_elements: designed 3, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1 a new dungeon resets deck, items, piles and player flags
- pass: R1 first turn of the match starts dungeon 1 with a full deck
- pass: R2 dungeon 2 is led by seat 2
- pass: R2 dungeon 4 is led by seat 1
- pass: R3 the turn passes from seat 1 to seat 3, skipping OUT seat 2
- pass: R4 with 2 cards in the deck only PASS is offered and nothing is drawn
- pass: R5 with 3 or more cards the active player draws the top card
- pass: R6 a drawing turn with an OUT seat runs its talk and continues normally
- pass: R7 PASS makes the player OUT and returns the drawn card to the deck
- pass: R8 ADD puts the drawn card in the dungeon and marks the player
- pass: R9 SACRIFICE_TORCH removes the torch and sets the card aside without marking added
- pass: R10 a removed item's sacrifice is not offered
- pass: R11 a sacrifice is shown in the public item state and the pile count is unchanged
- pass: R12 when only one player is left IN that player runs at once
- pass: R13 HP is 6 without armor: damage 5 succeeds
- pass: R13 HP is 7 without shield: damage 7 fails
- pass: R14 the faced monsters are the dungeon pile plus the top 2 deck cards
- pass: R15 torch and spear cancel weak and strong monsters
- pass: R15 without torch weak monsters deal their strength
- pass: R16 a successful run gives the runner 2 points
- pass: R17 a failed run costs the runner 1 point
- pass: R17 a failed run at 0 points stays at 0
- pass: R18 on a failed run OUT players who added gain 1 point
- pass: R19 after a run the next turn starts a new dungeon
- pass: R20 a run that brings a player to 4 points ends the game
- pass: R21 the game ends after turn 40 even mid-dungeon
- pass: R22 players tied for the most points share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 8, 'seat 2': 6, 'seat 1': 3, 'seats 1, 2 and 3': 1, 'seats 2 and 3': 2}, 56-160 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 146.0 decisions, prompts of 173 characters on average (longest 331)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 3': 19, 'seat 2': 15, 'seat 1': 14, 'seats 1, 2 and 3': 1, 'seats 2 and 3': 6, 'seats 1 and 2': 2, 'seats 1 and 3': 3}
- always `first@seat1`: won 0, lost 58, drew 2
- always `first@seat2`: won 0, lost 60, drew 0
- always `last@seat1`: won 4, lost 53, drew 3
- always `last@seat2`: won 4, lost 53, drew 3

## Triage (whose problem each failure was)

- round 1: revise_rules: The file works as specified, but a mindless fixed policy (always the last option, likely DRAW and then SACRIFICE or ADD) wins about 90% of decided games, and always taking the first option (PASS) never wins. Never passing makes you the runner, and the run is too easy to survive, so the pass-or-draw decision has no real tension.

## Choices the rules did not make

- 3 players (min 3, max 3, suggested 3): The designer fixed 3. Leadership rotation and the push-your-luck tension are built around three seats. With more seats each player's added bet matters less and turns run long; with two, the first pass ends the dungeon at once.
- Talk kept as a simultaneous poll each drawing turn: The rules require a simultaneous message from every player. Players disagree, since each wants the others to pass or to run a deadly dungeon, so bluffing about the drawn card carries real strategic weight.
- Deck as an ordered list shuffled once per dungeon; draws take the first element: This honors 'top card', the card returned on top after a PASS, and 'top 2 cards' in the run, with the shuffle as the only random event.
- Monsters stored by strength only: Names carry no rule effect; strength alone decides damage, TORCH and SPEAR.
- Talk is skipped on a forced pass: The rules send a forced pass straight from step (a) to step (d), skipping the talk in (c).

## Simplifications

- A tie for most points is reported as a shared win rather than a draw: The engine ranks by one expression and players level at the top share the win; this is equivalent to the source's draw.
- Dungeon reset, run and turn advance are single steps gated by arithmetic conditions: The step list is flat, so each block is expressed as conditional updates within one round.

## Encoding attempts

- 1: passed
