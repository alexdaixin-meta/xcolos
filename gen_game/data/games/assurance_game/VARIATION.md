# Variation: Assurance Threshold - Three Hunters

Three hunters decide each round to hunt stag (C) or hare (D). Stag succeeds only if all three cooperate. Private resilience type changes sucker payoff. First to reach target 38 over 10 rounds wins; target demands sustained unanimous cooperation.

Players: 3 to 3

## Review of the original

Two players simultaneously choose Cooperate (stag) or Defect (rabbit) with payoffs a>c>=d>b, so mutual cooperation is payoff-dominant while mutual defection is risk-dominant; played once or repeated for fixed rounds with cumulative scoring and higher total wins.

- **non_degenerate**: bad. With highest-total wins the safe policy cannot lose: Always Defect vs Always Cooperate gives Defect c >=d > b per round (e.g. 3 vs 0), so Defect wins; Always Defect vs Always Defect ties (d vs d). Always Defect never loses, Always Cooperate can only tie at best when opponent also cooperates, so cooperation is weakly dominated in differences. Highest-total thus collapses stag hunt.
- **skill_sensitive**: weak. One-shot outcome depends on risk tolerance not skill; repeated with highest total, endgame unravels: after any defection safe play is dominant and last rounds are all D, so skill in rebuilding trust cannot pay. Payoff differences are small relative to coordination failure.
- **headroom**: weak. 2x2 is solved: two pure Nash equilibria (CC payoff-dominant, DD risk-dominant). Repeated play adds little headroom because backwards induction pushes to DD under highest-total. Weak player scores same ties as strong when both defect.
- **reasoning_dependent**: bad. No hidden state, private type or private signal. Payoffs are common knowledge and perfect-information after reveal. One-shot requires only guessing opponent, repeated requires only history, no inference from limited information, no type to model.
- **verifiable**: good. Winner by arithmetic on cumulative payoffs; reveals and sums are deterministic.
- **fits_platform**: good. Turn-based simultaneous choice, text-only, arithmetic ranking, no board, short. Fits engine but needs winner-rule fix.

## Problems

- higher_total_wins_trap: Always Defect cannot lose and cooperation can only draw, making risky cooperative choice pointless
- no_hidden_information: nothing to infer, opponent modelling trivial, reasoning_dependent fails
- endgame_unraveling: with fixed rounds and highest total, last rounds defect is dominant and trust cannot be rebuilt
- lottery_risk_if_types_added_naively: unequal max totals would let winner be decided by dealt type not play
- two_players_insufficient_for_coordination_tension: with 2, defection advantage is binary, with 3 assurance requires unanimous cooperation creating stronger dilemma

## Changes

- Replace winner rule from highest total to target threshold (38 in 10 rounds) (fixes: higher_total_wins_trap): Defect-alone pays 4/round max 40, mutual defect 2/round max 20, mutual cooperation 5/round max 50. Target 38 is unreachable by mutual defection and only reachable by sustained unanimous cooperation or sustained lone-defection exploiting cooperators. Difference no longer decides, sustained cooperation is required to win. Allows cooperation to still pay after a betrayal.
- Expand to 3 players with unanimous-cooperation requirement: C pays 5 only if n_C==3 else sucker payoff, D pays 4 if n_C==2 (lone defector) else 2 (fixes: two_players_insufficient_for_coordination_tension): Makes coordination strictly harder and faithful to stag hunt (stag needs all hunters). With 3, one defector spoils all cooperators, raising risk. Minimum for meaningful assurance; 2-player is binary.
- Add one-time private type: Sheltered vs Exposed (50/50), independent per player, hidden. Payoffs equalized: if you cooperate and n_C<3 you get 1 if Sheltered else 0; all other payoffs identical across types (5 for n_C==3, 4 for lone defector, 2 otherwise) (fixes: no_hidden_information): Creates inference from limited information and divergent risk tolerance without lottery: both types have same max (50) and same safe (20) totals, so type matters for what to do (Exposed needs more assurance to cooperate) not who ends ahead. Provides opponent modelling.
- Set rounds=10 and payoffs a=5,c=4,d=2,b=0/1 with target 38 and no communication (fixes: endgame_unraveling): Calibrates headroom: 8 unanimous CC rounds needed for target (40), 10 lone-defections also 40 but requires victims to keep cooperating. Last rounds still matter because target not yet reached after a defection, fixing endgame unraveling. 10 rounds keeps complexity low.
- Keep simultaneous choice, no talk (fixes: lottery_risk_if_types_added_naively): With common target interests talk would be cheap 'let's all cooperate' and pass conflict test failure; private risk types already create disagreement without talk, talk would remove inference.

## Kept from the original

- stag-hunt payoff ordering a>c>=d>b and Pareto-optimal mutual cooperation vs risk-dominant mutual defection
- simultaneous reveal and fixed-round cumulative scoring
- tension between safe rabbit and risky stag / invest vs not invest

## The variation's rules

Setup: 3 players play 10 rounds. At start each player is privately dealt a type: Sheltered or Exposed, each 50% independent. Type is seen only by that player and never revealed. Each round simultaneously every player chooses C (hunt stag / invest) or D (hunt hare / don't invest). Let n_C be number of players (0-3) who chose C this round. Payoffs this round: If you chose C: you get 5 if n_C==3, otherwise you get 1 if your type is Sheltered and 0 if Exposed. If you chose D: you get 4 if n_C==2 (you are the lone defector), otherwise you get 2. Note this satisfies 5>4>=2>1 and 5>4>=2>0. After the round each player is told n_C and their own payoff, but not who chose what. Types are not revealed. Totals accumulate over rounds. The game ends after 10 rounds.

Objective: Target winner: after 10 rounds every player whose cumulative total is >=38 wins. If one player reaches target and others do not, that player is the sole winner. If multiple reach target they draw among themselves (shared win). If none reaches target the game is a draw. Higher total alone does not win unless it reaches 38.

Expected effect: Three is the minimum where stag needs unanimity, so one doubt spoils cooperation and risk scales. Target fixes higher-total trap and endgame unraveling: defecting early gives 4 but burns cooperators who then switch to D giving only 2, making lone-defection unsustainable; after a betrayal players still need ~8 unanimous rounds to hit 38, so rebuilding trust remains profitable. Thoughtful player infers others' types from willingness to cooperate after being suckered (Sheltered tolerates one failure with 1, Exposed with 0 is quicker to abandon) and conditions cooperation on observed n_C history, while thoughtless Always C is exploited to 0s and Always D stalls at 20 and never reaches target.

## Complexity (the designer's count, against the limits)

- steps_per_round: 3 (limit 12)
- choice_steps_per_round: 1 (limit 4)
- attributes: 4 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 15)
