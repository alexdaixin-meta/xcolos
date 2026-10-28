# button_men: needs review

Built from the variation **Loaded Button Men** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- A failed attack hands the attacking die to the defender: it is captured and the defender scores its size. In a failed two-die attack, the larger-size attacker is captured. (fixes: P1 Free probing): Probing now risks points. Attacking a big target with a weak die can lose more than it gains, and passing becomes a real option.
- On a failure, nobody is told the target's value. Only the value of a die at the moment it is captured is announced publicly. (fixes: P7 Thin inference): Exact values are no longer handed out. Players must deduce them from the allocation total, the captured values and the attacks made.
- Starting values are not rolled. Each player secretly sets their own four dice, each between 1 and its size, totalling exactly 16. The two players do this at the same time at the start of each leg. (fixes: P5 Luck dominance; P6 Platform limits; P2 Solved targeting): This removes the 8-die setup roll and its luck. It also creates a hidden allocation to read and to bluff with: load the d12 as a fortress or as a 12-power hammer, or spread strength over the small dice.
- The expected value of a target now depends on the opponent's allocation and on the cost of a miss, which is the size of your own attacker. (fixes: P2 Solved targeting): A d12 defended by a 12 can only be taken by a 12 or an exact sum. Low-valued small dice become the efficient targets. Target choice becomes a read of the opponent, not a fixed rule.
- The match is two legs with fresh secret allocations. The player who moved first in leg 1 moves second in leg 2. Scores from both legs are added. (fixes: P3 Seat edge): Each player holds each seat once, so any first-mover advantage cancels out.
- Equal totals are a draw. Neither seat wins ties. (fixes: P4 Tie and double-pass rule favours the second player): The always-pass policy can now at best draw against another passer and loses to any profitable attacker.
- Skill attacks use exactly two different dice. On success only the larger-size attacker is rerolled, and the smaller keeps its value. Power attacks use exactly one die. Failed attacks reroll nothing. (fixes: P6 Platform limits): Every turn uses at most one random draw.
- Explicit rules are added: no die listed twice, one attacker means a power attack and two attackers means a skill attack, invalid declarations count as a pass, and a fixed order of resolution and end checks. (fixes: P8 Ambiguities): Leaves nothing to interpretation.

Objective: When the match ends, the player with the higher score (total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks) wins. Equal scores are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Loading constraint: four values with min 1 each and total exactly 16. d12 can be loaded to 12 only if the others are (1,1,2) in some order. A d12 at 12 wins any power attack (12 >= every possible target value), so the leg's first mover F can load HEAVY = (d4,d6,d8,d12) = (1,1,2,12) and take S's d12 
- playable: pass. Limits: 40 rounds (turns), at the limit of 40. 16 steps <= 20. 2 choice steps (simultaneous loading poll on turns 1 and 21, plus the active player's choice) <= 4. 13 attributes <= 20. 1 hidden element type (die values) <= 3. At most one random draw per turn (the reroll after a success). The random F
- reasoning_over_luck: pass. The key decisions are skill-based.
- Loading is a simultaneous guessing game with the payoffs in the table above.
- Each attack requires inference. Opponent values are constrained by the public total of 16, by values revealed on capture, and by failed attacks (a failed power attack reveals that the 

## Complexity

- steps_per_round: designed 16, built 18, limit 20
- choice_steps_per_round: designed 2, built 5, limit 4
- attributes: designed 13, built 50, limit 20 (built: 80)
- hidden_elements: designed 1, built 12, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 40, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Each player starts with dice of sizes 4, 6, 8 and 12 in play
- pass: Scores carry over from leg 1 into leg 2
- pass: Chance picks First; only chance-independent facts after turn 1 are checked
- pass: Leg 1 odd turn: First acts, Second is not asked
- pass: Leg 1 even turn: Second acts, First is not asked
- pass: Leg 2 even turn: First acts
- pass: Leg 2 odd turn: Second acts
- pass: On turn 1 both seats load all four dice
- pass: No loading on a turn other than 1 or 21
- pass: Loads totalling 16 become the values: loaded d4=4 beats loaded d8=2
- pass: Loads not totalling 16 fall back to defaults: loaded d8=1 fails against default d4=2
- pass: At the start of leg 2 both in_play lists reset and scores stay
- pass: Each turn advances the public turn counter within leg 1
- pass: A pass turn leaves the public state unchanged
- pass: Active seat is offered pass, power and skill only with remaining dice
- pass: Power attack 5 vs 5 succeeds
- pass: Power attack 4 vs 5 fails
- pass: Skill attack 3 + 4 vs 7 succeeds
- pass: Skill attack 3 + 4 vs 6 fails
- pass: Capturing a d12 adds 12 to the attacker's score
- pass: After a successful skill attack the smaller die keeps its value (d6=3 later captures a d6 showing 3)
- pass: Failed skill attack: only the larger attacker is lost and the defender gains its size
- pass: After a failed skill attack the smaller die keeps its value (d4=1 later captures a d4 showing 1)
- pass: Capturing the opponent's last die ends leg 1 at once (turn jumps to 20)
- pass: Two passes in a row end leg 1 (turn jumps to 20)
- pass: Completing turn 20 ends leg 1 and the next turn starts leg 2
- pass: Early end of leg 1 skips to turn 21 with leg 2 loading
- pass: Completing turn 40 ends the match and the higher score wins
- pass: Leg 2 ending early (last die captured) ends the match
- pass: Equal scores at the end share the win
- pass: A failed attack rerolls nothing: defender's d12=8 then captures a d8 showing 8

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 9, 'seat 1': 11}, 26-33 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 28.7 decisions, prompts of 300 characters on average (longest 495)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 92% of decided matches against random seats
- always taking the first option as seat 2 wins 93% of decided matches against random seats
- random seats: {'seat 2': 34, 'seat 1': 26}
- always `first@seat1`: won 55, lost 5, drew 0
- always `first@seat2`: won 55, lost 4, drew 1
- always `last@seat1`: won 4, lost 52, drew 4
- always `last@seat2`: won 9, lost 48, drew 3

## Triage (whose problem each failure was)

- round 1: revise_rules: The game was built as specified, but the design has two problems. One fixed option wins about 92% of decided matches from either seat, because passing or a fixed safe choice beats random attackers whose failures feed the defender points. And the rules need 5 choice steps per round, over the limit of 4.

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed the table at 2. Every mechanic (attacker vs defender, alternating turns, loading against one opponent) is head-to-head and has no meaning with more seats.
- No pre-choice talk step: The source has no talk. In a two-player zero-sum duel, talk adds no shared decision to negotiate.
- Leg-1 early end jumps the turn counter to 20: The source says the skipped turns pass with no actions. Jumping turn to 20 is equivalent and avoids empty rounds.
- Die sizes listed as separate parameters d4_size, d6_size, d8_size, d12_size: Each parameter must be a single number.
- Strategy note: A thoughtful player loads to bait or defend, for example a high d12 for power and small dice that sum to likely targets. They infer hidden values from failed attacks and rerolls, and pass when attacking risks feeding the opponent a large die.

## Simplifications

- Loading is asked as four simultaneous number questions, one per die, then validated: The engine takes one number per question. The sum-to-16 check and the default replacement are done by arithmetic afterwards.
- Turn declarations are offered as a list of legal choices only: Choosing from a list makes illegal declarations impossible, so the 'invalid counts as pass' rule never triggers. The effect on play is identical.
- Attack resolution copies the attacker's and target's values into table scratch attributes (attack_value, target_value) before comparing: The engine has no direct operand for comparing attributes of two different players.
- The winner is computed as the highest you.score with ties shared: The engine has no separate draw. Equal top scores sharing the win is how a draw is represented.

## Encoding attempts

- 1: players are sent text with a `{name}` that was never filled in: placeholder: players are shown the literal {d6_value} (in `attack_succeeds_set`: 'Your d6 was rerolled to {d6_value}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {d12_value} (in `attack_succeeds_set`: 'Your d12 was rerolled to {d12_value}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat}) | placeholder: players are shown the literal {d4_value} (in `attack_succeeds_set`: 'Your d4 was rerolled to {d4_value}.'); use only names the step can fill in (see the broadcast rule: {value} and {seat})
- 2: passed
