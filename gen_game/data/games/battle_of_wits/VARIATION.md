# Variation: Battle of Wits: High Affinity Duel

Two-player alternating Poisoner-Chooser with persistent private High side. You score 3 when you win on your own High goblet, 1 when you win on your Low goblet, revealing opponent type over rounds.

Players: 2 to 2

## Review of the original

Two players: Poisoner secretly poisons one of two goblets, Chooser picks one to drink. Whoever drinks poison loses (or scores). Classic Battle of Wits is pure deduction/bluff with no score.

- **non_degenerate**: bad. In the tested Affinity Duel with 3/2 points, Chooser's optimal mix q*=0.5 independent of type and Poisoner's 40/60 mix makes Chooser indifferent, so Always-Left, Always-Right and Always-High all tie equilibrium 16.2-16.2 in expectation; no simple policy loses.
- **skill_sensitive**: bad. When both play equilibrium p*=0.4 High, expected points 1.2 each per round, total 14.4-14.4. Per-round variance var[D]=6, sd total ~8.5 over 12 rounds dominates; winner among optimal players decided by variance of own mixes, not by exploiting deviators, so better player not reliably wins.
- **headroom**: weak. 12 rounds of identical 3/2 matching pennies is essentially solved (unique mixed equilibrium) with no persistent information to exploit; headroom limited to frequency detection that does not move win probability measurably.
- **reasoning_dependent**: bad. Inference target exists (opponent High side) but equilibrium Chooser strategy independent of Poisoner type and Chooser type irrelevant to payoff, so learning opponent type gives no change in best response at equilibrium; reasoning not rewarded.
- **verifiable**: good. Scores are 3/2 arithmetic adds, announced each round, winner by highest total - fully verifiable from numbers.
- **fits_platform**: good. Turn-based text-only, simultaneous secret choices, arithmetic winner, 12 fixed rounds - fits simultaneous_choice + private_values, no board.

## Problems

- Higher-total-wins with 3/2 poison-side-only scoring makes Chooser indifferent at equilibrium, so thoughtless Always-Left/Always-Right cannot lose - non_degenerate fails (higher-total-wins trap).
- Chooser payoff depends only on Poisoner's High side, so optimal Chooser mix is type-independent; inferring opponent type does not change best response - reasoning_dependent fails.
- Equilibrium vs equilibrium ties in expectation and per-round variance (var ~6) dominates 12-round total (~8.5 sd), so winner among good players is lottery on own mixing variance, not skill.
- With 3 vs 2 gap, exploitation of deviators is small; equilibrium vs thoughtless draws, so skill edge weak.

## Changes

- Make points when you win depend on your OWN High side, not opponent's: Poisoner scores 3 if match on his High else 1; Chooser scores 3 if mismatch and his chosen goblet is his High else 1 (Crimson High=Left, Azure High=Right). (fixes: Higher-total-wins with 3/2 poison-side-only scoring makes Chooser indifferent at equilibrium, so thoughtless Always-Left/Always-Right cannot lose - non_degenerate fails (higher-total-wins trap).; Chooser payoff depends only on Poisoner's High side, so optimal Chooser mix is type-independent; inferring opponent type does not change best response - reasoning_dependent fails.; With 3 vs 2 gap, exploitation of deviators is small; equilibrium vs thoughtless draws, so skill edge weak.): Chooser's expected value of Left vs Right now is (1-p_bar)*val_C(Left) vs p_bar*val_C(Right), poisoner's is q_bar*val_P vs (1-q_bar)*val_P. This makes optimal play type-dependent, breaks Chooser indifference, and unconditional Always-Left/Always-Right loses when type mismatches High side.
- Increase gap to 3 vs 1 and keep alternating Poisoner roles over 12 rounds (6 each). Reveal choices and points each round but keep types hidden. (fixes: Equilibrium vs equilibrium ties in expectation and per-round variance (var ~6) dominates 12-round total (~8.5 sd), so winner among good players is lottery on own mixing variance, not skill.; With 3 vs 2 gap, exploitation of deviators is small; equilibrium vs thoughtless draws, so skill edge weak.): 3 vs 1 creates strict incentive to play High side at equilibrium (pure High is Bayesian Nash) and punishes off-type simple policies by ~12 points on average (expected 18-12 vs Always-Left). Alternating roles equalizes ex-ante expected totals (18-18 when both play High) so total is deterministic tie at equilibrium, removing per-round mixing variance as winner determinant.
- Keep private types Crimson/Azure (0.5 each) assigned once at start and persistent. Scoring announcements reveal side frequencies that perfectly signal opponent High after 1-2 observations, making inference payoff-relevant and exploitable for the rest of the game. (fixes: Chooser payoff depends only on Poisoner's High side, so optimal Chooser mix is type-independent; inferring opponent type does not change best response - reasoning_dependent fails.; Equilibrium vs equilibrium ties in expectation and per-round variance (var ~6) dominates 12-round total (~8.5 sd), so winner among good players is lottery on own mixing variance, not skill.): With own-High valuation, knowing opponent's High tells you which side they will favour as Poisoner (to match) and as Chooser (to mismatch on their High). Best response is to match their ChooserHigh as Poisoner and avoid their Poison High as Chooser, so 10+ remaining rounds benefit from early inference - reduces variance dominance and rewards opponent modelling over rounds.

## Kept from the original

- Two-player Poisoner/Chooser Battle of Wits with two goblets Left/Right
- Private type that makes one side High-value (Crimson Left-High vs Azure Right-High)
- Alternating Poisoner/Chooser roles each round and hidden types with revealed choices/scores
- Winner by arithmetic total points - no judge

## The variation's rules

Setup: Engine assigns each player a private type independently: Crimson (High=Left) or Azure (High=Right) with probability 0.5 each. Show each player only own type. Scores start 0. Play 12 rounds. Roles alternate: odd rounds 1,3,5,7,9,11 Player 1 is Poisoner and Player 2 is Chooser; even rounds 2,4,6,8,10,12 Player 2 is Poisoner and Player 1 is Chooser.
Each round:
1. Poisoner secretly chooses Left or Right as the sole poisoned goblet.
2. Chooser secretly chooses Left or Right to drink (the other goes to Poisoner). Choices simultaneous and hidden until reveal.
3. Reveal both choices and score:
- If Poisoner's choice == Chooser's choice (match): Poisoner scores points, Chooser 0. Points = 3 if the matched side equals Poisoner's High side, else 1.
- If choices mismatch: Chooser scores points, Poisoner 0. Points = 3 if Chooser's chosen side equals Chooser's High side, else 1.
Examples: Crimson Poisoner poisons Left and Chooser picks Left => Poisoner +3. Azure Poisoner poisons Left and Chooser picks Left => Poisoner +1. Crimson Chooser picks Right while Poisoner poisoned Left (mismatch) => Chooser +1 (Right is Low for Crimson). Azure Chooser picks Right while Poisoner poisoned Left => Chooser +3.
Announce choices, who scored and how many. Types stay hidden. After 12 rounds end.

Objective: Highest total points after 12 rounds wins. Equal totals = draw. Winner decided solely by sum of round points.

Expected effect: Unconditional Always-Left/Always-Right now loses heavily when type mismatches High (expected 12 vs 18 vs High-play). Equilibrium is pure High-play (play your High side always) giving deterministic 18-18 tie, so variance no longer decides winner; win comes from correctly inferring opponent High from early side frequencies and deviating to exploit (e.g., Poisoner matching opponent's High as Chooser). Inference over rounds is now payoff-relevant and persistent, and exploitation gap 3 vs 1 is large.

## Complexity (the designer's count, against the limits)

- steps_per_round: 4 (limit 12)
- choice_steps_per_round: 2 (limit 4)
- attributes: 3 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 15)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
