# Dropped: too simple

it is still degenerate or luck-driven: always taking the first option as seat 1 wins 100% of decided matches against random seats (after 3 variation(s))

## The last variation tried

Air, Land and Sea: Three Fronts: Two commanders secretly commit one card per round across three theaters for six rounds per battle. Each card goes face-up in its own theater or face-down anywhere as strength 3, and a commander may withdraw early to limit losses. The first to 12 VP wins the match.

## What was tried

- round 1: behavior problem; triage said fix_game: After a withdrawal the game keeps offering deploy and improvise to the players. It also never clears `battle_over` when the next battle starts: the final state 
- round 1: behavior problem; triage said fix_game: The rules are sound and expressible, but the game file mishandles the end of a battle and the withdrawal. After a withdrawal it still offered seat 1 'deploy Air
- round 1: behavior problem; triage said fix_tests: The failing scenarios demand moves the rules forbid. Three tests start with battle_over true (or in a round where no action can occur) and still script 'withdra
- round 2: behavior problem; triage said fix_tests: The failures come from scripted moves for seats the rules never ask to act, or for cards a seat may not hold. In round 13 seat 1 withdraws, so seat 2 correctly 
- round 2: behavior problem; triage said fix_tests: Other scenarios do get a 'withdraw' option, such as the battle 2 test where seat 1 withdraws, so the game does offer it in normal play. Only this battle_over sc
- round 2: design problem; triage said revise_rules: The game is built correctly, yet a thoughtless policy (always the first option) wins every decided match from either seat and always taking the last option lose
- round 3: design problem; triage said revise_rules: The game works as built, but one option dominates: always Fight (the first option) wins every decided match and always Withdraw loses every one. Withdrawing onl

To bring the game back, clear `dropped` in its inventory record.
