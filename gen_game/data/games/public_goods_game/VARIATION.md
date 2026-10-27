# Variation: Guarded Commons II

A 4-player, 10-round public goods game with anonymous contributions and a target of 185. Each round players may contribute, keep, or contribute and stand guard. Guards fine keepers, but a guard profits only when other guards stand with them. The one player who reaches the target alone wins. Otherwise the game is a draw.

Players: 4 to 4, best with 4

## Review of the original

The public goods game: each of n players privately splits an endowment between keeping it and a shared pot, which is multiplied by a factor below 1 per player and shared equally, so keeping is individually best and contributing is socially best. The previous adaptation, Guarded Commons, was a 4-player, 10-round version with Contribute, Sanction or Keep, simultaneous talk, and a 190-point target where exactly one reacher wins.

- **non_degenerate**: bad. In the original, keeping strictly dominates contributing. In Guarded Commons, SANCTION paid 5m - 3 + 8k, which is never below 17 per round and grows with every keeper. Against random play, always-S won 92% of games and lost 0%. Against any opponents it could not do worse than 17 per round, and keepers were ruined by it. One simple policy controlled the game.
- **skill_sensitive**: weak. There is no luck, but the transfer from keepers to sanctioners was so large that the skilful questions (when to trust, when to punish, whom to suspect) were replaced by 'always sanction'. A careful cooperator could not out-score a mechanical sanctioner.
- **headroom**: weak. Once 'always sanction' is found, nothing remains to improve. The original one-shot game is solved at contribute 0.
- **reasoning_dependent**: weak. Choices are hidden and only counts are announced, which is good material for inference. But a sanctioner profits whether or not anyone kept, so there was no reason to infer who was defecting or to coordinate punishment.
- **verifiable**: good. All scores and the target check are plain arithmetic on the counts of each action.
- **fits_platform**: good. The game uses simultaneous polls, counts, fixed rounds and simultaneous talk. It needs no board and about 10 steps per round.

## Problems

- P1: SANCTION paid a profit of 8 per keeper and at least 17 per round in every case, so always-S could not lose and won 92% against random play.
- P2: Because sanctioning was profitable on its own, punishment needed no coordination and no inference about who kept. Talk and the anonymous count announcements did little work.
- P3: Sanctioning when nobody kept cost only 3 against a target that allowed it, so permanent sanctioning was a safe default rather than a costly bet.
- P4: In the original game, keeping dominates contributing, and under a highest-total rule a keeper always gains relative to contributors. A plain public goods game therefore has a policy that cannot lose.

## Changes

- A sanctioner's reward now scales with the number of OTHER sanctioners: 4 x (keepers) x (other sanctioners). A lone sanctioner earns nothing from keepers and only pays the guard cost. (fixes: P1): Punishment now pays only when it is coordinated. Against random play, a sanctioner averages about 14.7 per round (about 147 in total), far below the target, so always-S no longer wins.
- Sanctioning costs 3 per round. With no keepers, a sanctioner scores 17 against a contributor's 20, so a player who always sanctions in an honest group ends on 170, below the 185 target, and loses. (fixes: P3): Sanctioning becomes a real bet that someone is keeping. It loses when nobody is.
- The fine is 6 per sanctioner paid by each keeper. Three coordinated sanctioners facing one keeper score 20 each (200 over a game) while the keeper scores 7. (fixes: P4): A persistent free rider can now lose: an organised group still reaches the target and leaves the keeper as the only one short. Always-K is no longer unloseable.
- The target is lowered from 190 to 185. The rule stays: exactly one reacher wins, otherwise a draw. (fixes: P4): All-contribute gives 200 and reaches the target. A group that starts punishing a steady keeper as late as round 4 still reaches 185. A free rider must keep unpunished at least 4 times to push the others below 185 and win alone. Cooperation can recover after a betrayal, and a betrayal can still pay.
- Simultaneous talk and count-only announcements are kept, and the payoffs now give them a purpose. (fixes: P2): Players must agree when to sanction together, judge from the counts whether someone is keeping, and decide whether an accusation or a promise is genuine.

## Kept from the original

- Each round a private choice between putting 10 tokens into a pot that is doubled and shared, or keeping them.
- The tension between individual free-riding and group gain.
- Costly punishment of free riders as an optional institution, as in public goods experiments with punishment.
- Anonymous play: only aggregate counts are announced, as in iterated public goods experiments.
- Four players, 10 rounds, and simultaneous non-binding talk.

## The variation's rules

SETUP: Exactly 4 players. Each has a private total starting at 0. The game lasts exactly 10 rounds. The target is 185 points. Individual choices and totals are hidden from the other players until the game ends.

EACH ROUND:
1. Talk. Every player writes one short message at the same time, without seeing the others' messages. All four messages are then shown to everyone. Messages are not binding: players may propose, promise, accuse or lie.
2. Choice. At the same time and in secret, each player chooses one action. Each player holds 10 tokens this round.
   - CONTRIBUTE: put all 10 tokens into the public pot.
   - SANCTION: put all 10 tokens into the public pot, and also pay 3 points to stand guard.
   - KEEP: keep all 10 tokens as 10 points.
3. Scoring. Let c, s and k be the numbers of players who chose CONTRIBUTE, SANCTION and KEEP (c + s + k = 4), and let m = c + s be the number who paid into the pot.
   - Public pot: it holds 10 x m tokens. It is doubled and shared equally, so every player, whatever they chose, receives 5 x m points.
   - A CONTRIBUTE player scores 5 x m.
   - A SANCTION player scores 5 x m - 3 + 4 x k x (s - 1). A guard collects 4 points per keeper for each OTHER guard standing with them, so a lone guard collects nothing.
   - A KEEP player scores 10 + 5 x m - 6 x s. A keeper pays a fine of 6 points for each guard.
   Reference (round scores; C = contribute, S = sanction, K = keep):
   - 4C: C 20. 3C 1S: C 20, S 17. 2C 2S: C 20, S 17. 1C 3S: C 20, S 17. 4S: S 17.
   - 3C 1K: C 15, K 25. 2C 1S 1K: C 15, S 12, K 19. 1C 2S 1K: C 15, S 16, K 13. 3S 1K: S 20, K 7.
   - 2C 2K: C 10, K 20. 1C 1S 2K: C 10, S 7, K 14. 2S 2K: S 15, K 8.
   - 1C 3K: C 5, K 15. 1S 3K: S 2, K 9.
   - 4K: K 10.
   Each player adds their round score to their own total. Totals are never reset and may go down.
4. Announcement. The numbers of players who chose CONTRIBUTE, SANCTION and KEEP are announced to everyone. Each player is told privately their own round score and total. No one is told who chose what or anyone else's total.

END: After round 10, all totals and the full history of choices are revealed, and the winner is decided by the objective.

Objective: After round 10, a player reaches the target if their total is 185 or more. If exactly one player reaches it, that player wins. If two or more players reach it, or nobody does, the game is a draw.

Expected effect: Full cooperation gives everyone 200 and a draw. A free rider who keeps 4 or more times without being punished pushes the others below 185 and wins alone. So the group must read the anonymous counts, work out whether someone is keeping, and punish. Punishment only pays when at least two players guard in the same round. A lone guard loses 3 points, and with 1 keeper and 2 contributors that keeper still scores 19. An unnecessary guard round also costs 3, and guarding in every round leaves a player on 170, below the target. Talk passes both tests. On reasoning, players propose joint guard rounds, accuse, promise and bluff. On conflict, every player wants to be the only one above 185 and wants others to bear the guard cost. A player who follows a call to guard when nobody else does pays 3 for nothing, and one who believes 'I'll cooperate' while the other keeps falls short. After a betrayal, cooperation still pays: the group can reach 185 even after several lost rounds, especially if it punishes together, as the final-round rescue against a keeper shows. Simple policies: always-C is exploited by keepers, always-K is crushed by three coordinated guards (it scores 70 while they reach 200), and always-S loses to honest contributors (170 against 200). Against random play every simple policy averages roughly 140 to 150 and almost never reaches 185.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 7 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers (every simple policy, 1200 games each)

no problems found

- numbers (seat 1's policy, outcome against random opponents): random: win 0% draw 99% loss 0%; always C: win 0% draw 93% loss 7%; always S: win 0% draw 100% loss 0%; always K: win 0% draw 100% loss 0%
- everyone playing 'always C' (best joint play): mean total 200.0; every player tied in 100% of games, so 0% are decided by the draw
