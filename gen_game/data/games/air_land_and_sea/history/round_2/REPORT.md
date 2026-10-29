# air_land_and_sea: needs review

Built from the variation **Air, Land and Sea: Four Battles** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Remove all card abilities. Cards are Air/Land/Sea 1–6 with strength equal to the number. Deploy (matching theater, full strength) and improvise (any theater, face-down, strength 2) remain. (fixes: P1): This keeps the core decisions (which theaters to fight for, what to hide, when to quit) inside the step budget.
- The match is exactly 4 battles of 6 rounds (24 rounds). Each player acts once per round. The higher VP total after round 24 wins; equal VP is a draw. (fixes: P2): A fixed length makes the game easy to build, and the tie rule is now unambiguous.
- Battle number, round-within-battle and first player are computed from the round number at the start of every round: battle = floor((round−1)/6)+1, round_in_battle = round − 6×(battle−1), first player = seat 1 in battles 1 and 3, seat 2 in battles 2 and 4. Nothing else ever changes them, and a withdrawal never does. (fixes: P3): This makes battle boundaries fixed and testable.
- A withdrawal sets battle_over to true immediately. The other seat is not asked to act that round. Every remaining round of that battle has no choices, and the battle gets no end-of-battle scoring. battle_over resets to false only at round_in_battle 1. (fixes: P4): This gives one precise reading of what a withdrawal does to the rest of the battle.
- Use a single withdrawal table for both seats, based on the withdrawer's hand size after withdrawing: 4 or more cards gives the opponent 2 VP; 2–3 cards gives 3 VP; 1 card gives 4 VP. Playing a battle out gives the winner 6 VP. (fixes: P6): It is simple and symmetric, and it keeps the original 'quit early, lose less' tension.
- State that equal VP after round 24 is a draw (no shared win). (fixes: P5): This removes the ambiguity in the end-of-game result.

Objective: After round 24, the player with more VP wins. Equal VP is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. WITHDRAW PAYOFF (VP gained by the opponent, by cards left in the withdrawer's hand): 6 to 4 cards = 2; 3 or 2 cards = 3; 1 card = 4. Losing a played-out battle gives the opponent 6. As a zero-sum swing, withdrawing early costs -2, and playing on with win chance p is worth 6p - 6(1-p) = 12p - 6. With
- playable: pass. Complete and finite: exactly 24 rounds. The battle, round_in_battle and first player are derived from the round number alone. The withdrawal and battle-end rules cover every case: the first player withdrawing skips the second player, and dead rounds pass silently. Tied theaters go to the first playe
- reasoning_over_luck: pass. CHANCE: hand face value has sd of about 3.5, so the difference between the two hands has sd of about 5, and the split across theaters also varies. Raw deal quality is therefore a large factor in any single battle; I estimate it decides about 50-60% of battles between equal players.

SKILL LEVERS tha

## Complexity

- steps_per_round: designed 13, built 12, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 16, built 38, limit 20 (built: 80)
- hidden_elements: designed 3, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 24, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: A card's strength is its number: deploying Sea 6 adds 6 to sea, Land 3 adds 3 to land
- pass: Round 7 belongs to battle 2
- pass: In battle 2 seat 2 acts first; its withdrawal means seat 1 is never asked
- pass: In battle 3 seat 1 acts first; its withdrawal means seat 2 is never asked
- pass: At the start of battle 2 every theater strength is reset to 0
- pass: Battle start deals 6 cards to each hand and sets 6 aside (first player withdraws, so no card leaves a hand)
- pass: With the battle running, the first player acts and then the second player acts once
- pass: Deploying Land 5 raises land strength by 5
- pass: Improvising Sea 6 to Air adds only 2 to air and nothing to sea
- pass: An improvised Land 6 shows publicly as only +2 in land, not 6
- pass: Withdrawing with 4 cards in hand gives the opponent 2 VP
- pass: The second player withdrawing with 2 cards in hand gives the opponent 3 VP
- pass: Withdrawing with 1 card in hand in round 6 gives the opponent 4 VP and no battle-end scoring
- pass: When the first player withdraws, the second player gets no action that round
- pass: After a withdrawal the rest of the battle passes with no actions and no scoring, then battle 2 starts at round 7
- pass: At the end of battle 1, tied theaters go to seat 1 (the first player), so seat 1 wins the battle
- pass: At the end of battle 2, tied theaters go to seat 2 (the first player), so seat 2 wins the battle
- pass: Controlling 2 of the 3 theaters at battle end gains 6 VP
- pass: After round 24 the game ends and the seat with more VP wins
- pass: Equal VP after round 24 is a draw shared by both seats

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 12, 'seat 1': 8}, 19-47 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 40.0 decisions, prompts of 304 characters on average (longest 305)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 100% of decided matches against random seats
- always taking the first option as seat 2 wins 100% of decided matches against random seats
- random seats: {'seat 2': 31, 'seat 1': 28, 'seats 1 and 2': 1}
- always `first@seat1`: won 60, lost 0, drew 0
- always `first@seat2`: won 59, lost 0, drew 1
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: After a withdrawal the game keeps offering deploy and improvise to the players. It also never clears `battle_over` when the next battle starts: the final state shows battle 2 with `battle_over` still true. As a result, no seat is ever offered 'withdraw' in later battles, which is what makes the R3 and R17 scenarios fail; these are implementation errors, and the rules are sound.
- round 1: fix_game: The rules are sound and expressible, but the game file mishandles the end of a battle and the withdrawal. After a withdrawal it still offered seat 1 'deploy Air 1' in that battle. When it moved on to battle 2 it left battle_over true and never dealt: the deck still holds 18 cards, set_aside is empty and the old hands remain. So no seat was offered actions, including withdraw, in later scenarios.
- round 1: fix_tests: The failing scenarios demand moves the rules forbid. Three tests start with battle_over true (or in a round where no action can occur) and still script 'withdraw' for both seats, which the game rightly never offers. The withdrawal test also forbids 'deploy' in the very round where seat 1 must be offered its normal options before it withdraws. As far as the trace shows, the game's withdrawal handling is correct: 2 VP to the opponent for 4 cards held, battle_over set, offers cleared.
- round 2: fix_tests: The failures come from scripted moves for seats the rules never ask to act, or for cards a seat may not hold. In round 13 seat 1 withdraws, so seat 2 correctly never acts. In round 8 seat 2 withdraws first, so seat 1 correctly never acts. The game is behaving as the rules require.
- round 2: fix_tests: Other scenarios do get a 'withdraw' option, such as the battle 2 test where seat 1 withdraws, so the game does offer it in normal play. Only this battle_over scenario fails, with neither seat ever offered 'withdraw', which is what the rules require while battle_over is true: the remaining rounds pass with no actions at all.
- round 2: revise_rules: The game is built correctly, yet a thoughtless policy (always the first option) wins every decided match from either seat and always taking the last option loses every match. Play is decided by one mechanical habit, not by decisions: deploying face-up beats improvising for almost every card, and withdrawing only gives points away.

## Choices the rules did not make

- Exactly 2 players: The designer fixed the table at 2. Theater control is a head-to-head comparison, the tie rule names the battle's first player, and withdrawal VP goes to 'the opponent', so the game is defined only for two.
- No talk step: The source has none. With two directly opposed players there is no coalition to form, so talk would only add words. The strategy lies in bluffing with face-down cards, reading the opponent's public strengths and judging when to withdraw cheaply.
- Actions use sequential ask: The rules order the first player before the second, and the second player reacts to the first player's public play.
- Withdrawal VP for 0 cards is not defined: A player always holds at least 1 card when acting, since 6 cards cover 6 actions, so the 0-card case never occurs.

## Simplifications

- Theater control compares two players' attributes: The engine has no player-attribute operand. The comparison of seat 1's and seat 2's air, land and sea is done with a table-attribute mirror beside the strengths, the listed workaround; the outcome is unchanged.
- Battle start is a single update with operations guarded by round_in_battle = 1: The step list is flat, so conditional operations replace a separate block. The behavior is identical.
- Shuffling is modeled as random draws from the deck list: Drawing at random is equivalent to shuffling and then dealing.
