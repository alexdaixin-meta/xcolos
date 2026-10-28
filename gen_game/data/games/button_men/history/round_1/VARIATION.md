# Variation: Loaded Button Men

Two players secretly load four dice with values totalling 16, then take turns attacking each other's dice. A capture scores the target's size; a miss gives your attacker to the opponent. Two legs with swapped first mover; higher combined total wins.

Players: 2 to 2, best with 2

## Review of the original

Button Men is a two-player dice duel. Each player rolls a set of dice of different sizes in public. Players take turns capturing opposing dice, either with one die of equal or higher value (power attack) or with several dice summing exactly to the target's value (skill attack). The attacking dice are rerolled, and the player whose captures add up to more sides wins the round, best of five.

- **non_degenerate**: bad. Original: captures are compulsory when possible and all rolls are public, so most turns have one obvious or forced move. First mover gets the first capture on a fresh roll. In the previous hidden variation a failed attack cost nothing and told the attacker the exact target value. That made 'attack the d12 with my highest die, then finish it with a die known to beat it' near-optimal. Player A won about 60% by capturing B's d12 on turn 1. Always-pass as B won about 50% against random play through the 0-0 double pass, because ties went to B.
- **skill_sensitive**: weak. Opening rolls, the random seat and every reroll drive the result. In the previous variation, two good players were judged to be decided by seat and rolls in more than 60% of games. The only real decision, which target to take, was nearly solved by expected value: the d12 is always the best target.
- **headroom**: weak. With public rolls the original is a short tactical calculation that a strong model solves turn by turn. With free probing the previous variation became near-perfect information after a few misses. There was little room above the greedy policy, and a weak player still won often by luck.
- **reasoning_dependent**: bad. The original has nothing hidden: rolls are public, so there is no inference and no opponent type. The previous variation hid values but gave them away for free on a miss. The defender learned only a weak bound. There was no bluff, no allocation and no cost of being wrong.
- **verifiable**: good. Captures, sizes and totals are pure arithmetic. The previous variation left a few ambiguities: duplicate attackers, whether two dice counts as a power or a skill attack, and the order of end checks. These are fixable without a judge.
- **fits_platform**: weak. The game is turn-based and text-only with no board. But setup rolls 8 dice at once, and a successful skill attack rerolls 2 to 4 dice in one turn, both above the 1-random-draw-per-round limit. Best of five rounds would need 8 fresh rolls each round. Special die skills add long rule chains.

## Problems

- P1 Free probing: a failed attack costs nothing and reveals the exact target value, so attacking weakly dominates passing and the probe-then-capture policy is near-optimal.
- P2 Solved targeting: with no cost of failure, attacking the d12 maximises expected value for every attacker value, so target choice takes no thought.
- P3 Seat edge: the first mover takes the opponent's d12 on turn 1 about 60% of the time and then stalls, and the seat is assigned at random.
- P4 Tie and double-pass rule favours the second player: always-pass as B wins about half of games against random play by forcing a 0-0 tie.
- P5 Luck dominance: the opening 8-die roll decides much of the game, so a reasoning player is not reliably favoured.
- P6 Platform limits: setup rolls 8 dice in one round, and a skill attack can reroll up to 4 dice in one turn, against a limit of 1 random draw per round.
- P7 Thin inference: the defender learns almost nothing, and the attacker learns too much, so there is little to deduce or bluff about.
- P8 Ambiguities: duplicate attackers, power versus skill attack with several dice, and the order of end checks are unspecified.

## Changes

- A failed attack hands the attacking die to the defender: it is captured and the defender scores its size. In a failed two-die attack, the larger-size attacker is captured. (fixes: P1 Free probing): Probing now risks points. Attacking a big target with a weak die can lose more than it gains, and passing becomes a real option.
- On a failure, nobody is told the target's value. Only the value of a die at the moment it is captured is announced publicly. (fixes: P7 Thin inference): Exact values are no longer handed out. Players must deduce them from the allocation total, the captured values and the attacks made.
- Starting values are not rolled. Each player secretly sets their own four dice, each between 1 and its size, totalling exactly 16. The two players do this at the same time at the start of each leg. (fixes: P5 Luck dominance; P6 Platform limits; P2 Solved targeting): This removes the 8-die setup roll and its luck. It also creates a hidden allocation to read and to bluff with: load the d12 as a fortress or as a 12-power hammer, or spread strength over the small dice.
- The expected value of a target now depends on the opponent's allocation and on the cost of a miss, which is the size of your own attacker. (fixes: P2 Solved targeting): A d12 defended by a 12 can only be taken by a 12 or an exact sum. Low-valued small dice become the efficient targets. Target choice becomes a read of the opponent, not a fixed rule.
- The match is two legs with fresh secret allocations. The player who moved first in leg 1 moves second in leg 2. Scores from both legs are added. (fixes: P3 Seat edge): Each player holds each seat once, so any first-mover advantage cancels out.
- Equal totals are a draw. Neither seat wins ties. (fixes: P4 Tie and double-pass rule favours the second player): The always-pass policy can now at best draw against another passer and loses to any profitable attacker.
- Skill attacks use exactly two different dice. On success only the larger-size attacker is rerolled, and the smaller keeps its value. Power attacks use exactly one die. Failed attacks reroll nothing. (fixes: P6 Platform limits): Every turn uses at most one random draw.
- Explicit rules are added: no die listed twice, one attacker means a power attack and two attackers means a skill attack, invalid declarations count as a pass, and a fixed order of resolution and end checks. (fixes: P8 Ambiguities): Leaves nothing to interpretation.

## Kept from the original

- Two players, each with a d4, d6, d8 and d12 whose sizes are public.
- Power attacks (one die of equal or higher value) and skill attacks (dice summing exactly to the target's value).
- Captured dice score their size (number of sides), not their value.
- A die that makes a successful capture is rerolled.
- A match made of several parts with the seat alternating, echoing the original best-of-rounds format.

## The variation's rules

DICE. Each player owns four dice: a d4, a d6, a d8 and a d12.
- A die's SIZE is its number of sides (4, 6, 8 or 12). Sizes are public.
- A die's VALUE is a whole number from 1 to its size. A player always knows their own values. A player is never told the opponent's values, except as stated below.
- Each player has a SCORE that starts at 0 and carries over between legs.

MATCH STRUCTURE.
- The match has two legs: leg 1 is turns 1 to 20 and leg 2 is turns 21 to 40.
- Before turn 1, one player is chosen at random to be First.
- Leg 1: First acts on odd turns (1, 3, ..., 19) and the other player, Second, acts on even turns (2, 4, ..., 20).
- Leg 2: Second acts on odd turns (21, 23, ..., 39) and First acts on even turns (22, ..., 40).

LOADING (at the start of each leg, on turns 1 and 21).
- Both players at the same moment secretly choose a value for each of their four dice.
- Each value must be at least 1 and at most that die's size, and the four values must total exactly 16.
- An invalid loading is replaced by the default loading: d4=2, d6=3, d8=4, d12=7.
- All four dice of both players are in play at the start of each leg. Captures from leg 1 do not carry over, but scores do.

EACH TURN (while the current leg is not over):
1. Public status. Announce the turn number, the leg, whose turn it is, which die sizes each player still has in play, both scores, and whether the previous turn in this leg was a pass.
2. Private status. Tell each player the current values of their own remaining dice.
3. Choice. The active player either PASSES or declares an ATTACK:
   - one of the opponent's remaining dice as TARGET, and
   - either one of their own remaining dice (a POWER attack) or exactly two different dice of their own (a SKILL attack).
   A die may not be listed twice. Any declaration that breaks these rules counts as a pass.
4. Resolution.
   - A power attack succeeds if the attacker's value is greater than or equal to the target's value.
   - A skill attack succeeds if the two attackers' values sum exactly to the target's value.
5. Public result. Announce the pass, or the target size, the attacking die sizes and whether the attack succeeded.
6. Success.
   - The target is captured and removed from the leg.
   - Its value is announced publicly.
   - The attacker's score rises by the target's size.
   - The attacking die (in a skill attack, only the larger-size of the two) is rerolled to a uniformly random value from 1 to its size. Its new value is told only to its owner.
   - In a skill attack the smaller attacker keeps its value.
7. Failure.
   - The attacking die is captured by the defender. In a skill attack, only the larger-size attacker is captured; the smaller stays in play with its value unchanged.
   - The captured die's value is announced publicly.
   - The defender's score rises by the captured die's size.
   - Nothing is rerolled, and the target's value is not revealed.
8. Leg end check. The leg ends immediately if any of these is true:
   - either player has no dice left;
   - this turn and the previous turn in this leg were both passes;
   - this is turn 20 (for leg 1).
   If leg 1 ends early, the remaining turns up to 20 are skipped with no actions.
9. Match end. After turn 40, or when leg 2 ends, the match ends.

NOTES.
- Values change only by loading at the start of a leg or by the reroll after a successful attack.
- Captured dice never return within a leg.
- Captures are not compulsory: a player may always pass.

Objective: When the match ends, the player with the higher score (total sizes of all dice they captured across both legs, including dice won from the opponent's failed attacks) wins. Equal scores are a draw.

Expected effect: Loading becomes a bluffing and reading problem. One player hides a 12 on the d12 as a sure-capture hammer or as an untouchable fortress; another spreads strength over the small dice to sweep low-valued targets. A rigid opening of '12 on the d12, capture their d12 at once' gains 12 points but leaves three dice worth 4 between them, which an opponent who loaded its small dice sweeps for up to 18. Because a miss gives the opponent your attacker's size, each attack weighs the chance of success, inferred from the 16-point total, the publicly revealed captured values and the opponent's behaviour, against the risk. Passing to make the trailing player take risks becomes a real tactic.

Simple policies all lose to good play:
- Always-pass can only draw against another passer and loses to any profitable attacker.
- Always-attack-the-d12-with-my-highest-die feeds dice to a fortress loading.
- Random play feeds dice to the defender.

Swapping seats between legs cancels any first-mover edge. Removing the setup roll leaves only reroll luck, so reasoning, not the deal, should decide most matches. No talk phase is included, because talk between two players with opposed interests adds nothing to reason about here.

## Complexity (the designer's count, against the limits)

- steps_per_round: 16 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
