# 03 design

- time: 2026-10-27T21:28:21+00:00 (200.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 b22d20b79275dcab, reply sha256 729d1863dc671049

## Sent

````
Original game: Public goods game
Players in the original: 2 to 20

Original rules:
Each of n players receives M tokens. Simultaneously each player i secretly chooses a contribution gi between 0 and M to put into the public pot, keeping M-gi. After all choices, the pot totaling sum gj is multiplied by factor a, where 1/n < a < 1, and divided equally: each player receives a * sum gj from the public good. Final payoff is Pi = M - gi + a * sum gj. In iterated version, the same group repeats this for a fixed number of rounds, seeing total contributions or payoffs between rounds. Selfish optimum is gi=0, social optimum is gi=M.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: PAYOFFS (k = number of OTHER players who contribute; my score if I choose C or K):
- k=0: C 5 (N=1), K 10 (N=0). Gap: K +5.
- k=1: C 22 (N=2), K 15 (N=1). Gap: C +7.
- k=2: C 23 (N=3), K 20 (N=2). Gap: C +3.
- k=3: C 26 (N=4), K 25 (N=3). Gap: C +1.
In absolute points no option is strictly dominant. The grant creates a coordination structure, so the stated 'commons' dilemma only partly survives.

WINNER RULE (my standing against the best opponent this round):
- k=0: K ties everyone at 10. C is 10 behind the keepers.
- k=1: C ties the other contributor at 22, 2 ahead of the keepers. K ties two keepers at 15, 10 ahead of the contributor. Both are joint-top.
- k=2: C scores 23 against the keeper's 25 (2 behind). K scores 20 against the contributors' 22 (2 behind). Equal.
- k=3: C gives a four-way tie at 26. K gives 25 against 23, an outright lead of +2.
So for rank, KEEP is weakly dominant within a round: never worse, strictly better at k=0 and k=3.

THE FOCAL COOPERATIVE OUTCOME IS BROKEN BY THE WINNER RULE. The social optimum (all contribute, 26 each, total 260) ends in a four-way draw. A single keeper in any round gains +2 on every contributor. Choices are hidden and only N is announced, so the defector cannot be identified or punished individually. A keep in round 10 against three contributors wins the game outright with 259 against 257.

THOUGHTLESS POLICIES:
- Always-KEEP vs three cooperators (always C): 25 against 23 every round, so 250 against 230. Wins every game.
- Always-KEEP vs three random players (p=0.5): keeper expects 17.5 per round; each random player expects 0.5×18 + 0.5×15 = 16.5. That is about +10 over the game, so it usually wins.
- Always-KEEP loses only if the other three coordinate to keep N=2 among themselves. They average 21.33 per round against its 20, which needs talk-based rotation they cannot verify.
- Always-CONTRIBUTE vs random: about 18 per round against random keepers' higher relative standing at k=0 and k=3. It loses often.
A thoughtless 'always keep' wins against cooperative and random play. That fails the check.
- playable FAILED: WHAT WORKS:
- Rules are complete: grant shares 12, 8 and 6 are integers, and the reference table matches the formulas (N=3: 15+8=23, keeper 25; N=4: 20+6=26).
- The game is finite at 10 rounds and decided by arithmetic.
- Complexity is within limits: 8 steps, 2 choice steps, 11 attributes, 1 hidden element, 0 draws, 10 rounds.
- Talk is simultaneous and is justified with 4 players: interests diverge over who contributes when N=2 is the best split, so proposals can cost the follower.
- No board, judge or clock is needed.

WHY IT FAILS (repeated fixed-length game decided by the highest total):
- In round 10, KEEP is weakly dominant for rank (see balanced), so the safe option wins the last round. That unravels backwards through the late rounds.
- After a betrayal (N=3 seen when 4 were promised), the betrayer leads by 2 and cannot be identified, since only N is announced.
- The only way for the others to catch up is to keep themselves. Cooperation therefore does not pay after a betrayal, and late rounds collapse to KEEP.
- One cooperative arrangement does resist deviation: a pre-agreed pair rotation (exactly 2 contribute, 210 each). It produces a guaranteed four-way draw, so cooperation's best case is 'nobody wins'.
- change: Remove KEEP's rank advantage when others cooperate. Raise the grant to 36 (shares 18/12/9). Contributors then score N=2: 28, N=3: 27, N=4: 29, against keepers 20 and 25. Then lower the public return (e.g. pot ×1.5, so each player gets 3.75×N, or use 4×N with tokens adjusted) so that K still beats C when k=0 and the k=1 case remains a real dilemma. Re-derive the 4×2 table and the rank table and confirm neither option is weakly dominant for rank in any k.
- change: Reveal each player's choice after every round (keep totals hidden if you want inference). Betrayals are then attributable, cooperation can be restored by targeted retaliation, and a defector can be singled out.
- change: Add a sanction step. Each player may simultaneously pay 2 points to remove 4 points from one named player, so betrayal after round 1 can cost the betrayer.
- change: Remove the last-round unravelling. Use one random draw at setup to fix a hidden end between rounds 8 and 12 (within the 1-draw limit, rounds at most 40), so no round is known to be final.
- change: After the changes, re-test always-KEEP against three cooperators and against random play under the winner rule, and show it loses at least sometimes against sensible play.
The variation that was reviewed: Matching Grant Commons: SETUP: Exactly 4 players. Each player has a total score starting at 0. The game lasts 10 rounds. Each player's total and each player's individual choices are private: they are not shown to the others until the game ends.

EACH ROUND:
1. Talk. Every player writes one short message at the same time, without seeing the others' messages. All four messages are then shown to everyone. Messages are not binding; players may promise, propose, accuse or lie.
2. Choice. At the same time and in secret, each player chooses CONTRIBUTE or KEEP. Each player has 10 tokens this round. CONTRIBUTE puts all 10 into the public pot. KEEP keeps all 10 as points.
3. Scoring. Let N be the number of players who chose CONTRIBUTE (0 to 4).
   - Public pot: the pot holds 10 x N tokens. It is doubled to 20 x N and shared equally among all 4 players, so every player (contributor or keeper) receives 5 x N points.
   - Matching Grant: if N is 2 or more, a grant of 24 points is split equally among the contributors only, so each contributor receives 24 / N points. If N is 0 or 1, no grant is paid.
   - A KEEP player scores 10 + 5 x N this round.
   - A CONTRIBUTE player scores 5 x N, plus 24 / N if N is at least 2.
   For reference, the per-round scores are:
   - N = 0: keepers 10.
   - N = 1: the contributor 5, keepers 15.
   - N = 2: contributors 22, keepers 20.
   - N = 3: contributors 23, the keeper 25.
   - N = 4: contributors 26.
   Each player adds their round score to their own total.
4. Announcement. The number N of contributors is announced to everyone. Each player is told privately their own score for the round. No one is told who contributed or anyone else's total.

END: After round 10, all totals and the full history of choices are revealed, and the winner is determined. Winner: After 10 rounds the player with the highest total wins. If two or more players share the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Each of n players privately splits an endowment of M tokens between keeping them and a public pot. The pot is multiplied by a (1/n < a < 1) and every player receives a times the pot, so contributing nothing is individually dominant while full contribution is socially best. The iterated version repeats this for a fixed number of rounds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "Each token contributed returns only a < 1 to the contributor, so g=0 strictly dominates in points every round. Under a higher-total winner rule, contributing only helps rivals. Always-keep can never finish below a contributor. The previous variation (matching grant, higher total wins) repeated this flaw: KEEP was weakly dominant for rank, and always-KEEP beat three cooperators 250 to 230."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "There is no luck, but the dominant keep strategy is trivially found. Under highest-total, the thoughtless keeper beats the thoughtful cooperator, so skill is not rewarded."
    },
    {
      "criterion": "headroom",
      "verdict": "bad",
      "evidence": "The game is solved: contribute 0. In the iterated version backward induction from a known last round gives the same answer. The previous variation's best cooperative arrangement (pair rotation) could only produce a four-way draw."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "One-shot play needs no inference. The iterated version adds reading others' contribution patterns, but with a dominant strategy and only totals shown there is little worth inferring."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Payoffs are pure arithmetic: M - g_i + a*sum g_j."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Simultaneous numeric choices, fixed rounds and arithmetic scoring all fit. It has no board and is short. Only the winner rule needs rethinking."
    }
  ],
  "problems": [
    "P1: Keeping is dominant in points in the original, and keeping is weakly dominant for rank under 'highest total wins' (also in the previous variation), so a thoughtless always-keep policy wins against cooperators and against random play.",
    "P2: The cooperative outcome can only draw under highest-total, and a single late defection wins outright, so the game unravels from the last round.",
    "P3: After a betrayal there was no way to make the betrayer pay, and catching up required keeping too, so cooperation never restarted.",
    "P4: There is nothing meaningful to infer: the decision is solved, and the only hidden information is the others' contributions, which do not change the right move.",
    "P5: Talk had weak conflict: everyone could agree on full contribution and the defector simply profited."
  ],
  "changes": [
    {
      "what": "Replace 'highest total wins' with a target. Every player whose 10-round total reaches 190 'reaches the target'. Exactly one reacher wins; two or more reachers, or none, is a draw. Full cooperation gives 200, so the slack is only 10 points.",
      "why": "Cooperation now pays in absolute terms: you need sustained cooperation to reach 190, and keeping alone gives only 100. The only outright win is to reach 190 while pushing everyone else below it, which is the betrayal temptation, now with real risk.",
      "fixes": "P1, P2"
    },
    {
      "what": "Add a third action, SANCTION. You contribute your 10 tokens like CONTRIBUTE, but you pay 3 points. Every keeper pays 8 points to every sanctioner that round, a direct transfer.",
      "why": "Betrayal can now be deterred and punished anonymously, without identifying anyone. Sanctioning is a costly bet: it loses 3 if nobody keeps and gains 5 per keeper caught. Against a habitual keeper, three sanctioners score 20 per round (as much as full cooperation) while the keeper scores 1, so always-KEEP can lose.",
      "fixes": "P1, P3"
    },
    {
      "what": "Keep individual choices and totals hidden. Announce only the counts of each action every round. Each player learns their own score privately.",
      "why": "Players must infer who kept and how much slack each rival has left from the counts, their own choice and the talk. This decides whether to guard (sanction) or trust, and whether a rival is close to a sole win.",
      "fixes": "P4"
    },
    {
      "what": "Keep simultaneous talk each round before the choice.",
      "why": "Interests conflict. Each player wants others to bear the cost of guarding (3 points from a 10-point slack), and any player may be planning a betrayal or a two-player squeeze. A follower who takes guard duty or trusts a promise can lose their slack or be pushed below 190.",
      "fixes": "P5"
    },
    {
      "what": "Drop the matching grant and use a simple public pot. Every player receives 5 points per contributor (CONTRIBUTE or SANCTION). A keeper also scores their own 10 tokens.",
      "why": "Simpler arithmetic and a real dilemma: keeping against three contributors scores 25 against the contributors' 15. The sanction and target now carry the strategy, which the grant failed to do.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "An endowment of 10 tokens per round, kept privately or put into a public pot that is multiplied and shared equally (doubled, so 5 per contributor to everyone).",
    "The core dilemma: keeping beats contributing in points for that round when others contribute, yet everyone keeping leaves everyone far worse off.",
    "A repeated game with the same group of 4, simultaneous secret choices, and only aggregate contribution information revealed between rounds.",
    "Free-riding is the central temptation and sustained cooperation is the social optimum."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "A target winner rule plus a costly, profitable anonymous sanction turns the dominant-strategy commons into a game of trust, guarding and slack management that cannot be solved by a simple policy."
  },
  "variation": {
    "name": "Guarded Commons",
    "summary": "Four players repeatedly choose to contribute to a doubled public pot, keep their tokens, or contribute and stand guard against keepers. Anyone reaching 190 points over 10 rounds reaches the target. A lone reacher wins; otherwise the game is a draw.",
    "players": {"min": 4, "max": 4, "suggested": 4},
    "rules": "SETUP: Exactly 4 players. Each has a private total starting at 0. The game lasts exactly 10 rounds. The target is 190 points. Individual choices and totals are never shown to other players until the game ends.\n\nEACH ROUND:\n1. Talk. Every player writes one short message at the same time, without seeing the others' messages. All four messages are then shown to everyone. Messages are not binding: players may propose, promise, accuse or lie.\n2. Choice. At the same time and in secret, each player chooses one of three actions. Each player holds 10 tokens this round.\n   - CONTRIBUTE: put all 10 tokens into the public pot.\n   - SANCTION: put all 10 tokens into the public pot, and also pay 3 points to stand guard.\n   - KEEP: keep all 10 tokens as 10 points.\n3. Scoring. Let m be the number of players who chose CONTRIBUTE or SANCTION (0 to 4), s the number who chose SANCTION, and k the number who chose KEEP (k = 4 - m).\n   - Public pot: the pot holds 10 x m tokens. It is doubled and shared equally, so every player (whatever they chose) receives 5 x m points.\n   - A CONTRIBUTE player scores 5 x m.\n   - A SANCTION player scores 5 x m - 3 + 8 x k: they pay 3 for guarding and collect 8 points from each keeper.\n   - A KEEP player scores 10 + 5 x m - 8 x s: they pay 8 points to each sanctioner.\n   Reference (per-round scores):\n   - No keepers (m=4): CONTRIBUTE 20, SANCTION 17.\n   - One keeper (m=3): CONTRIBUTE 15, SANCTION 20, KEEP 25 - 8 x s (25, 17, 9 or 1).\n   - Two keepers (m=2): CONTRIBUTE 10, SANCTION 23, KEEP 20 - 8 x s.\n   - Three keepers (m=1): CONTRIBUTE 5, SANCTION 26, KEEP 15 - 8 x s.\n   - Four keepers: KEEP 10 each.\n   Each player adds their round score to their own total. Totals can go down only through sanctions and guard costs; they are never reset.\n4. Announcement. The numbers of players who chose CONTRIBUTE, SANCTION and KEEP are announced to everyone. Each player is told privately their own score for the round and their own total. No one is told who chose what or anyone else's total.\n\nEND: After round 10, all totals and the full history of choices are revealed, and the result is decided by the objective.",
    "objective": "After round 10, a player 'reaches the target' if their total is 190 or more. If exactly one player reaches the target, that player wins. If two or more players reach it, or nobody does, the game is a draw.",
    "expected_effect": "Full cooperation gives 200 each, a shared draw, but leaves only 10 points of slack. Each unguarded keep against three contributors takes 5 from every other player and adds 5 to the keeper, so three such keeps without retaliation hand the keeper a sole win. Guarding costs 3 when nobody keeps, so a player can afford about three guard rounds in total. Players must plan a guard rotation, judge whether announced guards will really sanction, and infer from the action counts who has kept and how much slack each rival has left. Sanctioning turns profitable exactly when a keeper appears, so a known or suspected betrayer faces 1 to 17 per round instead of 25, and the victims can still recover toward 190: cooperation remains worth restarting after a betrayal. The last round does not unravel: anyone with 3 points of slack can sanction safely, which makes a final-round keep costly. Two players keeping together squeeze the other two by 10 each while scoring 20, but they can at best share a draw, so each is tempted to double-cross the other. Talk carries real conflict: everyone wants someone else to pay for guard duty, any proposer may be setting up a betrayal, and a player who trusts promises and never guards can be pushed below 190 while the betrayer reaches it alone. Simple policies all lose somewhere. Always-CONTRIBUTE loses to one keeper (150 against 250). Always-KEEP loses to three sanctioners (10 against 200). Always-SANCTION loses when one contributor reaches 200 while the others drift below 190 through their own guard costs, and the always-sanctioner sits at 170."
  },
  "model": {
    "players": 4,
    "rounds": 10,
    "actions": ["C", "S", "K"],
    "types": null,
    "payoff": "(5*(n_C+n_S) - 3 + 8*n_K) if action == 'S' else ((5*(n_C+n_S)) if action == 'C' else (10 + 5*(n_C+n_S) - 8*n_S))",
    "winner": {"kind": "target", "target": 190}
  },
  "complexity": {
    "steps_per_round": 9,
    "choice_steps_per_round": 2,
    "attributes": 14,
    "hidden_elements": 2,
    "random_draws_per_round": 0,
    "rounds": 10
  }
}
```
````
