# button_men: ready for review

Built from the variation **Button Men: Guard and Strike** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Enlarge the random draw to R uniform on 0 to 110,075,314,175 (24^8 - 1), giving eight base-24 digits D0 to D7. Leg-start dice still use D0 to D5. Player A's reroll uses D6 and player B's reroll uses D7. (fixes: Previous variation: seat B's leg-start guard reroll used digit D1, which also set A's d8, so B learned A's d8 for free at least 3 times per match and A had no equivalent. This is a systematic seat edge.): No digit ever sets both a reroll and a leg-start die, so no reroll can reveal an opponent value. A and B are treated identically.
- Keep hidden die values, revealed only by failed attacks. (fixes: Original: rolls are public, so there is nothing hidden to infer and many turns are forced captures.): This gives players something to infer and remember.
- Keep identical fixed dice (d4, d8, d12) for both players and simultaneous choices. (fixes: Original: Button choice and turn order create seat and setup edges.): This removes the setup and turn-order edges.
- Keep single-die power attacks plus a guard action, and keep the 12-action menu. (fixes: Original: multi-die skill attacks and special dice need long rule chains, beyond the build limits.): This preserves the capture-by-value core within the build limits.
- Keep 30 exchanges in legs of at most 10, with survival bonuses. (fixes: Original: best of five rounds is a small sample, so luck weighs heavily.): The larger sample lets skill dominate, and the legs keep the original's round structure.

Objective: After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. SYMMETRY: both players own identical dice (d4, d8, d12), choose at the same moment, and draw from independent uniform digits. Neither seat has an edge from move order or information.

RANDOMNESS CHECK: 24^8 = 110,075,314,176, so R in [0, 24^8 - 1] gives eight independent uniform base-24 digits. 4, 8
- playable: pass. COMPLETENESS: the rules cover every case.
- All 144 action pairs resolve through three ordered conditions (guarded / value comparison / fail).
- A simultaneous capture by both sides is explicitly allowed.
- Actions naming captured dice do nothing, which also acts as a pass.
- Rerolls are well define
- reasoning_over_luck: pass. WHERE LUCK ENTERS: chance sets the die values at each leg start and on rerolls.

WHERE SKILL ENTERS: each exchange is a simultaneous guess about which die the opponent will attack or guard. Several things feed that guess:
- Your own values are known to you.
- Failed attacks reveal values that persis

## Complexity

- steps_per_round: designed 14, built 10, limit 20
- choice_steps_per_round: designed 1, built 1, limit 4
- attributes: designed 18, built 52, limit 20 (built: 80)
- hidden_elements: designed 1, built 19, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Match begins with all dice alive and both scores 0
- pass: An exchange with guards only advances the counters (random digits not asserted)
- pass: Leg start revives every captured die
- pass: Both seats are offered the guard actions each exchange
- pass: Both seats choose from all 12 actions, including attacks
- pass: Attacking an already captured die does nothing
- pass: Attack into a guarded die fails and the defender scores 3
- pass: Higher attack on unguarded d8 captures it for 8 points
- pass: Equal attack value captures an unguarded d12 for 12 points
- pass: Lower attack on unguarded die fails and the defender scores 2
- pass: Two d8s capture each other at the same time
- pass: Guarding rerolls privately but changes no score or capture
- pass: Results show the new score after a guarded attack
- pass: Capturing the last die ends the leg with surviving-dice bonuses
- pass: 10th exchange of a leg ends it with bonuses for surviving dice
- pass: After a leg ends the next exchange starts a new leg with all dice alive
- pass: Exchange 30 closes the leg in progress and bonuses decide the match
- pass: Equal final totals share the win
- pass: Higher final total wins

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 9, 'seat 2': 11}, 60-60 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 60.0 decisions, prompts of 197 characters on average (longest 197)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 27, 'seat 2': 32, 'seats 1 and 2': 1}
- always `first@seat1`: won 26, lost 32, drew 2
- always `first@seat2`: won 14, lost 46, drew 0
- always `last@seat1`: won 13, lost 45, drew 2
- always `last@seat2`: won 13, lost 44, drew 3

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built as specified, but the design has two problems. One fixed option wins about 92% of decided matches from either seat, because passing or a fixed safe choice beats random attackers whose failures feed the defender points. And the rules need 5 choice steps per round, over the limit of 4.

## Choices the rules did not make

- 2 players, as filed: The designer fixed the game at 2. It is a head-to-head duel in which every action targets the single opponent's dice, so there is no room for more seats.
- Seat 1 is player A and seat 2 is player B: The rules assign different random digits to A and B, so each seat needs a fixed role.
- No talk step: The rules give no communication, and the game is purely adversarial with simultaneous choices.
- All 12 actions are offered even when a named die is captured: The rules list exactly 12 actions and state that an action naming a captured die does nothing, so offering them stays faithful.
- Strategy at the table: A thoughtful player tracks announced values and which dice were rerolled, guards a high-value die that is likely to be attacked, and attacks dice whose values are revealed as low or that are small. A thoughtless player attacks blindly into guards.

## Simplifications

- R is stored as its eight base-24 digits: 24^8 = 110075314176, so a uniform R from 0 to 110075314175 is exactly eight independent uniform digits from 0 to 23. Every die value rule is unchanged.
- The match-end leg closure is folded into the leg-end step as the condition exchange = 30: This gives the same scoring without needing a separate block of steps.
- Announced die values are kept in a per-exchange public list, revealed_values: Every reveal needs a stated piece of state.

## Encoding attempts

- 1: the game file was refused by the loader: button_men: steps[0].do[1].value.calc: '[int(rand / digit_base ** k) % digit_base for k in [a_d4_digit, a_d8_digit, a_d12_digit, b_d4_digit, b_d8_digit, b_d12_digit, a_reroll_digit, b_reroll_digit]]': Pow is not allowed
- 2: it plays, but part of it does nothing: game attribute `action_names` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `action_codes` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
- 3: passed
