# 01 design

- time: 2026-11-19T23:15:26+00:00 (81.5s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ae0524f5bd4833b5, reply sha256 5aa77a06b6724d12

## Sent

````
Original game: One Night Revolution
Players in the original: 3 to 10

Original rules:
Each player gets a secret ID token (Rebel or Informant) plus a secret Specialist card giving a night power; three extra IDs go to the HQ. At night eyes closed, controller leads informants to recognize each other, then clockwise each player opens eyes alone to do their Specialist action which may look at or swap ID tokens. By day, players in order claim a Specialist token (may lie) then discuss freely for 5-10 minutes, without looking at cards, trying to deduce current alignments. Then all simultaneously point at someone to Terminate. Most-voted players reveal IDs. If any Informant is terminated, Rebels win. If none or only Rebels are terminated, Informants win. Rebels can also win by voting in a circle with zero eliminations if all Informant tokens are correctly believed to be on HQ.

THE PREVIOUS VARIATION, the one to revise:
Name: One Night Revolution: Ten Nights
Players: 5 to 5
Rules: SETUP: There are 5 players, each starting with 0 points. Each player also keeps two sub-totals, Rebel points and Informant points, both starting at 0. Before round 1, the engine lists all 10 possible pairs of players and shuffles that list secretly. This is the only random event in the game. In round r (r = 1 to 10), the pair in position r of the shuffled list are the Informants; the other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 4 rounds, with each other player as partner exactly once, and a Rebel in exactly 6 rounds. All players are told this rule but not the order.

EACH ROUND:
1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.
2. NIGHT (simultaneous): Every player privately names one other player as a target. A Rebel's target is investigated. An Informant's target is framed. An Informant may name any other player, including their partner (framing a partner has no extra effect).
3. NIGHT RESULTS: Each Rebel is privately told one result about their target. The result is 'Informant' if the target is an Informant this round, or if at least one Informant framed that target this round. Otherwise it is 'Rebel'. A 'Rebel' result is therefore always true; an 'Informant' result may be a frame. Informants receive no result.
4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.
5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.
6. VOTE (simultaneous): Every player names one other player to Terminate. All votes, showing who voted for whom, are then announced publicly.
7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise, every player tied for the most votes is terminated. The round roles of the terminated players only are announced publicly; no other roles are revealed.
8. SCORING (individual):
   - Each Rebel who voted for an Informant gains 2 points.
   - If at least one terminated player is an Informant, each Rebel gains 1 more point.
   - Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3).
   - If no Informant was terminated, each Informant gains 2 more points.
   - Points gained as a Rebel are also added to that player's Rebel points; points gained as an Informant are also added to their Informant points.
   - Everyone's totals are announced.
9. Termination does not remove anyone; all 5 players take part in every round. After round 10 the game ends.
How the winner is decided: After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
CHANGES APPROVED BY ALEX DAI (2026-11-19), who owns this game. They were proposed in a review of
recorded matches and approved before this run. Make exactly these two changes:

1. No running scores. Do not announce any player's points (total, Rebel points or Informant points)
   during the game. After round 10, announce every player's final total, Rebel points and Informant
   points. Keep announcing, every round, the votes (who voted for whom) and the round roles of the
   players who were terminated.
2. Survival bonus per Informant. Each Informant who was not terminated this round gains 2 points,
   instead of both Informants gaining 2 only when no Informant was terminated.

Keep everything else exactly as it is: 5 players and 10 rounds; the secret, shuffled schedule of all
10 pairs (each pair Informants exactly once, the only random event); the night (Rebels investigate,
Informants frame) and its results; the two simultaneous messages; the simultaneous vote and the
termination rule (2 or more votes, everyone tied for the most is terminated); the other point values
(a Rebel gains 2 for voting for an Informant and 1 more if an Informant is terminated; an Informant
gains 1 for each Rebel who voted for a Rebel); individual scoring and the tie-breaks.

EVIDENCE (20 recorded matches on a fixed schedule: one evaluated agent and four Muse players):
- The per-round announcement of Rebel and Informant points let anyone read off every earlier
  round's Informant pair, in all 20 matches. With each pair used once, a Rebel voting in round 9 had
  one candidate pair left, and round 10's Informants were terminated in 19 of 20 matches. Without
  those announcements, round 9 still leaves about 5 candidate pairs.
- Rebels voted for an Informant in 118 of 120 of the agent's Rebel rounds, so voting tested little.
- In 14 of the agent's 80 Informant rounds it lost the survival bonus only because its partner was
  terminated.

THIS PIPELINE'S OWN REASONING CHECK of the current game said:
**Verdict: adequate.** Winning takes real reasoning: schedule deduction from scores, information-optimal investigations and modelling what each Rebel can infer decide most votes, and good tie-engineering earns points. The fixed pair schedule makes late rounds deterministic and hands luck to whoever is Informant early. Hiding scoring sub-totals, or leaving the schedule's later rounds less determined, would keep deception and multi-round planning relevant to the end.


Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{"original_summary": "One Night Revolution is a 3-10 player hidden-ID deduction game: secret Rebels vs Informants use night look/swap powers, then day claims and discussion, then a simultaneous point to Terminate; Rebels win if an Informant is terminated.", "review": [{"criterion": "non_degenerate", "evidence": "No always-vote-X, always-target-X or always-claim-Rebel policy can lock a win: votes need 2+ to terminate, ties terminate all tied, framing changes Rebel results, and totals are not zero-sum. An Informant who always frames the same Rebel is eventually investigated and voted; a Rebel who always votes the same player misses 8 of 10 pairs.", "verdict": "good"}, {"criterion": "skill_sensitive", "evidence": "Every player is Informant exactly 4 rounds and Rebel exactly 6 rounds with each partner once, so type-luck is equalized; only order is random. With scores hidden, round 9 still has ~5 candidate pairs, so investigation choice, framing, claim logic and vote reading decide points, not the draw.", "verdict": "good"}, {"criterion": "headroom", "evidence": "Weak play can still score by lucky votes; strong play can improve by optimal investigate targets given elimination history, partner-aware framing, deceptive claims, schedule deduction, and tie-engineering votes. Not solved in 10 rounds with 4 choice steps.", "verdict": "good"}, {"criterion": "reasoning_dependent", "evidence": "Each round roles are private, Informants privately know each other, Rebel results are noisy because 'Informant' can be true or framed, and the pair schedule is hidden. Winning votes require inferring who knows what and who will vote where.", "verdict": "good"}, {"criterion": "verifiable", "evidence": "Winner follows by arithmetic: sum of stated per-round points, tie-break on Rebel points then Informant points. No referee judgment.", "verdict": "good"}, {"criterion": "fits_platform", "evidence": "Turn-based text-only: private role tells, simultaneous target, simultaneous claims, simultaneous responses, simultaneous vote, public vote and terminated-role announcements. No board, no trading, no binding agreements, 10 rounds.", "verdict": "good"}], "problems": ["Running announcements of total, Rebel points and Informant points let anyone read off every earlier Informant pair in all 20 matches; with each pair used once round 9 had one candidate pair left and round 10 Informants were terminated in 19 of 20.", "Team survival bonus gave both Informants 2 points only if no Informant was terminated, so an Informant lost the bonus because its partner was terminated in 14 of 80 Informant rounds, punishing play it could not control."], "changes": [{"fixes": "Running announcements of total, Rebel points and Informant points let anyone read off every earlier Informant pair in all 20 matches; with each pair used once round 9 had one candidate pair left and round 10 Informants were terminated in 19 of 20.", "what": "Hide all scores until the end: announce no points during the game; announce votes and terminated roles each round only; announce every final total, Rebel points and Informant points after round 10.", "why": "Removes the deterministic schedule leak while keeping vote and termination information for deduction; round 9 keeps ~5 candidate pairs so deception and planning stay relevant."}, {"fixes": "Team survival bonus gave both Informants 2 points only if no Informant was terminated, so an Informant lost the bonus because its partner was terminated in 14 of 80 Informant rounds, punishing play it could not control.", "what": "Individual survival bonus: each Informant who was not terminated this round gains 2 points, regardless of partner fate.", "why": "Rewards own survival and deceptive play instead of punishing a player for a partner error; keeps Informant scoring skill-sensitive."}], "keeps": ["5 players, 10 rounds, secret shuffled schedule of all 10 pairs as the only random event", "Night: Rebels investigate one target, Informants frame one target, noisy 'Informant'/'Rebel' results to Rebels only", "Two simultaneous message phases with lying allowed, then simultaneous vote", "Termination rule: 2+ votes required, all tied for most terminated, only terminated roles revealed", "Other point values: Rebel 2 for voting Informant plus 1 if an Informant terminated; Informant 1 per Rebel voting Rebel", "Individual scoring with Rebel/Informant sub-totals and highest-total-wins with Rebel then Informant tie-breaks"], "recommendation": {"decision": "adapt", "kind": "none", "reason": "With hidden scores and individual survival the game is balanced, playable, and reasoning-dependent within limits."}, "variation": {"name": "One Night Revolution: Ten Nights, Hidden Ledger", "summary": "Five players repeat 10 hidden Rebel-vs-Informant rounds on a secret pair schedule; Rebels investigate, Informants frame, all talk twice then vote to terminate, scoring hidden until the end.", "players": {"max": 5, "min": 5, "suggested": 5}, "rules": "SETUP: 5 players. Each starts with 0 total points, 0 Rebel points, 0 Informant points. Before round 1 the engine lists all 10 unordered pairs of players and shuffles the list secretly. This is the only random event. In round r (r=1 to 10) the pair in position r is the Informants; the other 3 are Rebels. Every player is Informant in exactly 4 rounds with each other player as partner exactly once, and Rebel in exactly 6 rounds. Players are told this rule but not the order. EACH ROUND, in order: 1. ROLES: Each player is privately told Rebel or Informant for this round. Each Informant is also privately told who the other Informant is. 2. NIGHT (simultaneous): Every player privately names one other player as target. A Rebel target is investigated. An Informant target is framed. An Informant may name any other player including the partner; framing a partner has no extra effect. 3. NIGHT RESULTS: Each Rebel is privately told one result about their target: 'Informant' if the target is an Informant this round OR at least one Informant framed that target this round, otherwise 'Rebel'. A 'Rebel' result is always true; an 'Informant' result may be true or a frame. Informants receive no result. 4. CLAIMS (simultaneous): Every player writes one short message, e.g. claimed role, target or result. Lying allowed. All messages then shown to everyone. 5. RESPONSES (simultaneous): Every player writes one more short message. All shown to everyone. 6. VOTE (simultaneous): Every player names one other player to Terminate. All votes showing who voted for whom are then announced publicly. 7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise every player tied for the most votes is terminated. The round roles of terminated players only are announced publicly; no other roles revealed. 8. SCORING (hidden): Each Rebel who voted for an Informant gains 2 points. If at least one terminated player is an Informant, each Rebel gains 1 more point. Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3). Each Informant who was not terminated this round gains 2 points. Points gained while Rebel are also added to Rebel points; points gained while Informant also added to Informant points. No totals of any kind are announced during the game. Only the votes and the terminated roles are announced each round. Termination removes no one; all 5 play every round. After round 10 the engine announces every player's final total, Rebel points and Informant points and the game ends.", "objective": "After 10 rounds the player with the highest total points wins. Tie-break: among tied, most Rebel points wins; if still tied, most Informant points wins; if still tied, draw.", "expected_effect": "Hiding the ledger restores late-game uncertainty so Informants can still bluff and Rebels must still infer schedule, results and voting intent. Individual survival lets a good Informant profit even if its partner is caught. Talk earns its place: Rebels want to coordinate on a true Informant, Informants want Rebels to vote Rebels; interests conflict. A Rebel who just follows a proposal can lose by voting a Rebel (loses 2, gives Informants 1 each plus survival) while a correct independent vote earns 2-3."}, "model": null, "complexity": {"attributes": 6, "choice_steps_per_round": 4, "hidden_elements": 3, "random_draws_per_round": 0, "rounds": 10, "steps_per_round": 9}}
````
