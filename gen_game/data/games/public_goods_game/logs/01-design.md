# 01 design

- time: 2026-10-27T21:25:04+00:00 (123.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 aaaeac06ef93791d, reply sha256 72224fa77182ba84

## Sent

````
Original game: Public goods game
Players in the original: 2 to 20

Original rules:
Each of n players receives M tokens. Simultaneously each player i secretly chooses a contribution gi between 0 and M to put into the public pot, keeping M-gi. After all choices, the pot totaling sum gj is multiplied by factor a, where 1/n < a < 1, and divided equally: each player receives a * sum gj from the public good. Final payoff is Pi = M - gi + a * sum gj. In iterated version, the same group repeats this for a fixed number of rounds, seeing total contributions or payoffs between rounds. Selfish optimum is gi=0, social optimum is gi=M.
````

## Reply

````
```json
{
  "original_summary": "Each of n players gets M tokens and secretly splits them between a private stash and a public pot. The pot is multiplied by a factor a, with 1/n < a < 1, and every player receives a times the pot, so free-riding is individually best and full contribution is socially best. It can be repeated for a fixed number of rounds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "Every player receives the same pot share, so the difference between two players' payoffs is just the difference in what they kept. Under 'higher total wins', contributing 0 is strictly best against every opponent action and can never lose, only tie. Contributing anything can only lose. The choice is dead: 'always 0' wins or draws every game."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "The best policy is trivial and needs no information about opponents, so a careful player gains nothing over a thoughtless one who always keeps everything."
    },
    {
      "criterion": "headroom",
      "verdict": "bad",
      "evidence": "The game is solved in one line (give 0). Every competent player draws, and there is nothing further to learn."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "Free-riding is dominant regardless of beliefs, so there is nothing to infer. The secrecy of contributions is irrelevant because the best reply does not depend on them."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Payoffs are pure arithmetic on contributions: M - g_i + a * sum g_j."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It uses a simultaneous numeric choice, fixed rounds and arithmetic scoring, with no board. Its only flaw is the degenerate incentive under a winner-only scoring rule."
    }
  ],
  "problems": [
    "P1: Under a highest-total winner rule, contributing 0 strictly dominates in relative terms. It can never lose, and any contribution can only lose, so 'always keep' is an unbeatable simple policy.",
    "P2: Because the dominant action ignores opponents, nothing needs to be inferred or modelled. There is no reasoning, no skill gap and no headroom.",
    "P3: Full cooperation, the interesting outcome, can at best produce a draw, so the social dilemma has no bite for a model that is only rewarded for winning.",
    "P4: A continuous contribution between 0 and M and a variable group size of 2 to 20 make the payoffs hard to balance and check. Tuned numbers need a fixed group size.",
    "P5: In the iterated version, seeing payoffs or totals between rounds would reveal exactly who contributed, which removes any hidden information."
  ],
  "changes": [
    {
      "what": "Add a provision-point Matching Grant of 24 points. It is paid only if at least 2 players contribute in a round and is split equally among that round's contributors only.",
      "why": "Contributing now beats keeping when exactly 2 contribute (contributors +2 over keepers), but keeping still beats contributing when 3 contribute (keepers +2) and when 1 contributes (keeper +10). Neither 'always keep' nor 'always contribute' is safe: each loses against some opponent pattern.",
      "fixes": "P1"
    },
    {
      "what": "Fix the game at 4 players, two actions (Contribute all 10 or Keep all 10), a pot multiplier of 2 shared among all 4, and 10 rounds.",
      "why": "Exact, checkable payoffs where the relative advantage flips with the number of contributors (1, 2 or 3). The tuned anti-coordination tension only holds at this size.",
      "fixes": "P4"
    },
    {
      "what": "Individual choices and running totals stay secret until the game ends. After each round only the NUMBER of contributors is announced, and each player privately learns their own round payoff.",
      "why": "Players must infer who is contributing from counts, from their own choice and from talk. This creates a hidden state and makes opponent modelling (who tends to contribute after which count) the core skill.",
      "fixes": "P2, P5"
    },
    {
      "what": "Add a simultaneous talk phase each round: everyone writes one short message at the same time, then all are shown, then everyone chooses.",
      "why": "Players disagree about who should contribute. Each wants to be a contributor when exactly 2 contribute and a keeper when 3 do. Proposals, promises and lies about who will contribute become something to reason about, and following a proposal blindly can leave you in the losing group.",
      "fixes": "P2, P3"
    },
    {
      "what": "Winner is the highest total after 10 rounds, with ties drawing. The relative payoffs are now built so that cooperative contribution earns ground only in coordinated groups of exactly 2.",
      "why": "Cooperation now matters for winning, not just for the social total. Pairs who coordinate to contribute together gain on the keepers, while over-contribution by a crowd rewards the free-rider. The original's free-rider temptation survives, but it is no longer unconditional.",
      "fixes": "P3, P1"
    }
  ],
  "keeps": [
    "Each round every player secretly decides whether to put their endowment into a public pot or keep it.",
    "The pot is multiplied and shared equally among all players, contributors and free-riders alike, so free-riding on others' contributions remains a real temptation.",
    "All players contributing is the socially best outcome (26 points each per round, the highest possible group total).",
    "The same group repeats over a fixed number of rounds and sees aggregate contribution information between rounds."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core dilemma is sound, but 'highest total wins' makes free-riding unbeatable. A provision-point grant shared among contributors, hidden individual choices and simultaneous talk turn it into a game of inference and coordination that fits the limits easily."
  },
  "variation": {
    "name": "Matching Grant Commons",
    "summary": "Four players repeatedly decide whether to put 10 tokens into a doubled public pot. A 24-point Matching Grant rewards contributors only when at least two contribute, so contributing pays in a pair but free-riding pays when three contribute. Only the number of contributors is ever announced.",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "rules": "SETUP: Exactly 4 players. Each player has a total score starting at 0. The game lasts 10 rounds. Each player's total and each player's individual choices are private: they are not shown to the others until the game ends.\n\nEACH ROUND:\n1. Talk. Every player writes one short message at the same time, without seeing the others' messages. All four messages are then shown to everyone. Messages are not binding; players may promise, propose, accuse or lie.\n2. Choice. At the same time and in secret, each player chooses CONTRIBUTE or KEEP. Each player has 10 tokens this round. CONTRIBUTE puts all 10 into the public pot. KEEP keeps all 10 as points.\n3. Scoring. Let N be the number of players who chose CONTRIBUTE (0 to 4).\n   - Public pot: the pot holds 10 x N tokens. It is doubled to 20 x N and shared equally among all 4 players, so every player (contributor or keeper) receives 5 x N points.\n   - Matching Grant: if N is 2 or more, a grant of 24 points is split equally among the contributors only, so each contributor receives 24 / N points. If N is 0 or 1, no grant is paid.\n   - A KEEP player scores 10 + 5 x N this round.\n   - A CONTRIBUTE player scores 5 x N, plus 24 / N if N is at least 2.\n   For reference, the per-round scores are:\n   - N = 0: keepers 10.\n   - N = 1: the contributor 5, keepers 15.\n   - N = 2: contributors 22, keepers 20.\n   - N = 3: contributors 23, the keeper 25.\n   - N = 4: contributors 26.\n   Each player adds their round score to their own total.\n4. Announcement. The number N of contributors is announced to everyone. Each player is told privately their own score for the round. No one is told who contributed or anyone else's total.\n\nEND: After round 10, all totals and the full history of choices are revealed, and the winner is determined.",
    "objective": "After 10 rounds the player with the highest total wins. If two or more players share the highest total, the game is a draw.",
    "expected_effect": "Free-riding is no longer unbeatable. The temptation remains when three players contribute (the keeper gains 2), but a player who keeps while exactly two others contribute falls 2 behind. A lone contributor falls 10 behind every keeper. Every simple policy can lose: always-keep loses to two players who contribute together while the fourth keeps, and always-contribute loses whenever it ends up alone. Within a round the group wants exactly two contributors, but each individual wants to be one of those two (or the free-rider among three), so players genuinely disagree about who contributes. Talk becomes bargaining and bluffing: a player who follows a proposal like 'you and I contribute' can be left alone (-10 relative) or crowded into a group of three (-2 relative to the keeper). Because only the count N is revealed, players must infer from N, their own choice and the messages who actually did what, and track who keeps their word. Strong players will model each opponent's tendencies and steer into the winning group more often than chance. Weak players still score every round, because everyone gets the pot share. There is no trust to unravel at the end: the last round is the same coordination puzzle, without future reputation."
  },
  "model": {
    "players": 4,
    "rounds": 10,
    "actions": ["C", "K"],
    "types": null,
    "payoff": "(5 * n_C + (24 / n_C if n_C >= 2 else 0)) if action == 'C' else (10 + 5 * n_C)",
    "winner": {"kind": "highest_total"}
  },
  "complexity": {
    "steps_per_round": 8,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 10
  }
}
```
````
