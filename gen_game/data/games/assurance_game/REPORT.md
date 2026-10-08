# assurance_game: needs review

Built from the variation **Assurance Threshold - Three Hunters** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace winner rule from highest total to target threshold (38 in 10 rounds) (fixes: higher_total_wins_trap): Defect-alone pays 4/round max 40, mutual defect 2/round max 20, mutual cooperation 5/round max 50. Target 38 is unreachable by mutual defection and only reachable by sustained unanimous cooperation or sustained lone-defection exploiting cooperators. Difference no longer decides, sustained cooperation is required to win. Allows cooperation to still pay after a betrayal.
- Expand to 3 players with unanimous-cooperation requirement: C pays 5 only if n_C==3 else sucker payoff, D pays 4 if n_C==2 (lone defector) else 2 (fixes: two_players_insufficient_for_coordination_tension): Makes coordination strictly harder and faithful to stag hunt (stag needs all hunters). With 3, one defector spoils all cooperators, raising risk. Minimum for meaningful assurance; 2-player is binary.
- Add one-time private type: Sheltered vs Exposed (50/50), independent per player, hidden. Payoffs equalized: if you cooperate and n_C<3 you get 1 if Sheltered else 0; all other payoffs identical across types (5 for n_C==3, 4 for lone defector, 2 otherwise) (fixes: no_hidden_information): Creates inference from limited information and divergent risk tolerance without lottery: both types have same max (50) and same safe (20) totals, so type matters for what to do (Exposed needs more assurance to cooperate) not who ends ahead. Provides opponent modelling.
- Set rounds=10 and payoffs a=5,c=4,d=2,b=0/1 with target 38 and no communication (fixes: endgame_unraveling): Calibrates headroom: 8 unanimous CC rounds needed for target (40), 10 lone-defections also 40 but requires victims to keep cooperating. Last rounds still matter because target not yet reached after a defection, fixing endgame unraveling. 10 rounds keeps complexity low.
- Keep simultaneous choice, no talk (fixes: lottery_risk_if_types_added_naively): With common target interests talk would be cheap 'let's all cooperate' and pass conflict test failure; private risk types already create disagreement without talk, talk would remove inference.

Objective: Target winner: after 10 rounds every player whose cumulative total is >=38 wins. If one player reaches target and others do not, that player is the sole winner. If multiple reach target they draw among themselves (shared win). If none reaches target the game is a draw. Higher total alone does not win unless it reaches 38.

## Complexity

- steps_per_round: designed 3, built 7, limit 12
- choice_steps_per_round: designed 1, built 3, limit 4
- attributes: designed 4, built 12, limit 20
- hidden_elements: designed 1, built 1, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 10, built -, limit 15

## Fidelity to the rules (independent tests written from the spec alone; they do not decide whether the file works)

- pass: All cooperate ten rounds - shared win deterministic 50 each
- pass: Lone defector every round - seat 3 sole winner chance-invariant for defector
- pass: All defect ten rounds - draw with D_other payoff at n_c 0
- pass: Single cooperator stranded - D_other at n_c 1 chance-invariant for defectors
- pass: Mixed cooperation threshold edge - 6xC_all then 4xD_other to reach exactly 38 shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'draw': 20}, 30-30 turns

## Balance (tier 1, informational: a thoughtless policy that always wins, or luck deciding everything)

- every random match ended 'draw': choices do not change the result
- random seats: {'draw': 60}
- always `first@seat1`: won 0, lost 10, drew 50
- always `first@seat2`: won 0, lost 8, drew 52
- always `last@seat1`: won 0, lost 0, drew 60
- always `last@seat2`: won 0, lost 0, drew 60

## Choices the rules did not make

- 3 to 3 players: Coordination with threshold 3 and lone-defector bonus at n_C==2 only meaningful with exactly 3; with 2 there is no threshold tension, with >3 payoff thresholds 3 and 2 become arbitrary and one player's deviation matters less. Minimum 3 makes agreement hard and a single holdout breaks full cooperation.
- No pre-round communication poll: Source rules have simultaneous choice with no talk; adding free-text talk would change assurance dilemma into bargaining and is not in source. With 3 players payoff conflict already gives disagreement without talk.
- Use poll for simultaneous C/D choice: Source says simultaneously every player chooses; poll is required so later players do not see earlier answers, per engine capability
- Parameter values 5,4,2,1,0 and threshold 38: Source fixes 5>4>=2>1 and 5>4>=2>0 and example satisfies with 5 for C if n_C==3, 1 if Sheltered else 0 if Exposed when C and n_C!=3, 4 if D and n_C==2 else 2; threshold 38 explicitly given for winner determination
- Win condition as shared win / draw, not ranking: Source says higher total alone does not win unless it reaches 38; multiple qualifiers draw among themselves, zero qualifiers is draw. Implemented as arithmetic count of qualifiers, not highest-score ranking.

## Simplifications

- Payoff matrix implemented as conditional arithmetic updates instead of lookup table: Engine has no payoff-matrix lookup; same arithmetic effect achieved with conditional adds per player using n_c and type (supported with workaround: ~5 conditional branches)
- n_C and private payoff revealed via tell/sync rather than separate private channels: Engine's tell/sync delivers private state; matches source 'each player is told n_C and their own payoff, but not who chose what'
- Type draw implemented as independent 50% via initial hidden attribute: Engine initialize with hidden_hands/private_values; no deck needed

## Encoding attempts

- 1: passed
