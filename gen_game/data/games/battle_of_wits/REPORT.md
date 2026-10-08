# battle_of_wits: ready for review

Built from the variation **Battle of Wits: High Affinity Duel** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Make points when you win depend on your OWN High side, not opponent's: Poisoner scores 3 if match on his High else 1; Chooser scores 3 if mismatch and his chosen goblet is his High else 1 (Crimson High=Left, Azure High=Right). (fixes: Higher-total-wins with 3/2 poison-side-only scoring makes Chooser indifferent at equilibrium, so thoughtless Always-Left/Always-Right cannot lose - non_degenerate fails (higher-total-wins trap).; Chooser payoff depends only on Poisoner's High side, so optimal Chooser mix is type-independent; inferring opponent type does not change best response - reasoning_dependent fails.; With 3 vs 2 gap, exploitation of deviators is small; equilibrium vs thoughtless draws, so skill edge weak.): Chooser's expected value of Left vs Right now is (1-p_bar)*val_C(Left) vs p_bar*val_C(Right), poisoner's is q_bar*val_P vs (1-q_bar)*val_P. This makes optimal play type-dependent, breaks Chooser indifference, and unconditional Always-Left/Always-Right loses when type mismatches High side.
- Increase gap to 3 vs 1 and keep alternating Poisoner roles over 12 rounds (6 each). Reveal choices and points each round but keep types hidden. (fixes: Equilibrium vs equilibrium ties in expectation and per-round variance (var ~6) dominates 12-round total (~8.5 sd), so winner among good players is lottery on own mixing variance, not skill.; With 3 vs 2 gap, exploitation of deviators is small; equilibrium vs thoughtless draws, so skill edge weak.): 3 vs 1 creates strict incentive to play High side at equilibrium (pure High is Bayesian Nash) and punishes off-type simple policies by ~12 points on average (expected 18-12 vs Always-Left). Alternating roles equalizes ex-ante expected totals (18-18 when both play High) so total is deterministic tie at equilibrium, removing per-round mixing variance as winner determinant.
- Keep private types Crimson/Azure (0.5 each) assigned once at start and persistent. Scoring announcements reveal side frequencies that perfectly signal opponent High after 1-2 observations, making inference payoff-relevant and exploitable for the rest of the game. (fixes: Chooser payoff depends only on Poisoner's High side, so optimal Chooser mix is type-independent; inferring opponent type does not change best response - reasoning_dependent fails.; Equilibrium vs equilibrium ties in expectation and per-round variance (var ~6) dominates 12-round total (~8.5 sd), so winner among good players is lottery on own mixing variance, not skill.): With own-High valuation, knowing opponent's High tells you which side they will favour as Poisoner (to match) and as Chooser (to mismatch on their High). Best response is to match their ChooserHigh as Poisoner and avoid their Poison High as Chooser, so 10+ remaining rounds benefit from early inference - reduces variance dominance and rewards opponent modelling over rounds.

Objective: Highest total points after 12 rounds wins. Equal totals = draw. Winner decided solely by sum of round points.

## The critic (3 review(s) before the rules went to a coder)

- balanced: pass. Payoff matrix for same-type (Hp=Hc): L/H vs L/H = (3,0), L/H vs R/L=(0,1), R/L vs L/H=(0,3), R/L vs R/L=(1,0). Poisoner expected = q*(4r-1)+(1-r) indifferent r=0.25; Chooser expected = r*(3-4q)+q indifferent q=0.75 => mixed NE (0.75,0.25) both expect 0.75. Opposite-type matrix: (Hp vs Hc opposite) L
- playable: pass. Rules are complete from text alone: type draw (0.5 each, private), scores 0, 12 rounds alternating Poisoner/Chooser, simultaneous secret choice Left/Right, reveal, deterministic scoring 3/1 for matcher/mismatcher based on own High side (with examples covering all cases), announcement, hidden types t
- reasoning_over_luck: pass. Hidden type and opponent mix must be inferred from 12 reveals of L/R. Ex-ante Bayesian NE with unknown opponent type (avg P(L)=0.5 regardless of r) makes High strictly dominant: E[High]=0.5*3=1.5 > E[Low]=0.5*1=0.5 for both roles, so good play is play High, beating thoughtless/random (Good 1.5/role=

## Complexity

- steps_per_round: designed 4, built 6, limit 12
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 3, built 9, limit 20
- hidden_elements: designed 1, built 1, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 12, built -, limit 15

## Fidelity to the rules (independent tests written from the spec alone; they do not decide whether the file works)

- pass: P1 shutout invariant 24-0 regardless of types - balanced Left/Right
- pass: P2 shutout invariant 0-24 regardless of types - balanced Left/Right
- pass: Draw invariant 12-12 via Poisoner scoring (all matches) balanced
- pass: Draw invariant 12-12 via Chooser scoring (all mismatches) balanced

## Does the file follow the spec's shape? (flags for a person)

- the spec has a simultaneous choice (poll) but the game file has none: players may answer after seeing others

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 1': 14, 'seat 2': 5, 'draw': 1}, 24-24 turns

## Balance (tier 1, informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 1': 35, 'seat 2': 21, 'draw': 4}
- always `first@seat1`: won 18, lost 38, drew 4
- always `first@seat2`: won 28, lost 26, drew 6
- always `last@seat1`: won 31, lost 25, drew 4
- always `last@seat2`: won 23, lost 32, drew 5

## Triage (whose problem each failure was)

- round 1: fix_tests: Game correctly implements the scoring (evidence 7-13 for AA moves matches rules) and exposes independent private types; tests predict exact scores that are not invariant to the random Crimson/Azure assignment (no type combination yields 8-16) and therefore predict chance, while the invariant shutout 24-0 should hold for any types.

## Choices the rules did not make

- none

## Simplifications

- Payoff matrix implemented as 12 conditional single-step updates with when conditions instead of lookup operation: Engine has no payoff_matrix lookup; workaround requires arithmetic conditional updates (about 13 steps for 9 cells) - here 8 scoring cases split by parity
- Simultaneous hidden choices implemented via poll storing each player's current_choice and comparing equality to detect match/mismatch, rather than a Poisoner-only then Chooser-only step: Engine poll addresses all players at once; using poll guarantees simultaneity with no player hearing earlier answer, as required; match detection is equivalent to poisoner_choice == chooser_choice
