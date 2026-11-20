# Variation: One Night Revolution: Ten Nights, Hidden Ledger

Five players repeat 10 hidden Rebel-vs-Informant rounds on a secret pair schedule; Rebels investigate, Informants frame, all talk twice then vote to terminate, scoring hidden until the end.

Players: 5 to 5, best with 5

## Review of the original

One Night Revolution is a 3-10 player hidden-ID deduction game: secret Rebels vs Informants use night look/swap powers, then day claims and discussion, then a simultaneous point to Terminate; Rebels win if an Informant is terminated.

- **non_degenerate**: good. No always-vote-X, always-target-X or always-claim-Rebel policy can lock a win: votes need 2+ to terminate, ties terminate all tied, framing changes Rebel results, and totals are not zero-sum. An Informant who always frames the same Rebel is eventually investigated and voted; a Rebel who always votes the same player misses 8 of 10 pairs.
- **skill_sensitive**: good. Every player is Informant exactly 4 rounds and Rebel exactly 6 rounds with each partner once, so type-luck is equalized; only order is random. With scores hidden, round 9 still has ~5 candidate pairs, so investigation choice, framing, claim logic and vote reading decide points, not the draw.
- **headroom**: good. Weak play can still score by lucky votes; strong play can improve by optimal investigate targets given elimination history, partner-aware framing, deceptive claims, schedule deduction, and tie-engineering votes. Not solved in 10 rounds with 4 choice steps.
- **reasoning_dependent**: good. Each round roles are private, Informants privately know each other, Rebel results are noisy because 'Informant' can be true or framed, and the pair schedule is hidden. Winning votes require inferring who knows what and who will vote where.
- **verifiable**: good. Winner follows by arithmetic: sum of stated per-round points, tie-break on Rebel points then Informant points. No referee judgment.
- **fits_platform**: good. Turn-based text-only: private role tells, simultaneous target, simultaneous claims, simultaneous responses, simultaneous vote, public vote and terminated-role announcements. No board, no trading, no binding agreements, 10 rounds.

## Problems

- Running announcements of total, Rebel points and Informant points let anyone read off every earlier Informant pair in all 20 matches; with each pair used once round 9 had one candidate pair left and round 10 Informants were terminated in 19 of 20.
- Team survival bonus gave both Informants 2 points only if no Informant was terminated, so an Informant lost the bonus because its partner was terminated in 14 of 80 Informant rounds, punishing play it could not control.

## Changes

- Hide all scores until the end: announce no points during the game; announce votes and terminated roles each round only; announce every final total, Rebel points and Informant points after round 10. (fixes: Running announcements of total, Rebel points and Informant points let anyone read off every earlier Informant pair in all 20 matches; with each pair used once round 9 had one candidate pair left and round 10 Informants were terminated in 19 of 20.): Removes the deterministic schedule leak while keeping vote and termination information for deduction; round 9 keeps ~5 candidate pairs so deception and planning stay relevant.
- Individual survival bonus: each Informant who was not terminated this round gains 2 points, regardless of partner fate. (fixes: Team survival bonus gave both Informants 2 points only if no Informant was terminated, so an Informant lost the bonus because its partner was terminated in 14 of 80 Informant rounds, punishing play it could not control.): Rewards own survival and deceptive play instead of punishing a player for a partner error; keeps Informant scoring skill-sensitive.

## Kept from the original

- 5 players, 10 rounds, secret shuffled schedule of all 10 pairs as the only random event
- Night: Rebels investigate one target, Informants frame one target, noisy 'Informant'/'Rebel' results to Rebels only
- Two simultaneous message phases with lying allowed, then simultaneous vote
- Termination rule: 2+ votes required, all tied for most terminated, only terminated roles revealed
- Other point values: Rebel 2 for voting Informant plus 1 if an Informant terminated; Informant 1 per Rebel voting Rebel
- Individual scoring with Rebel/Informant sub-totals and highest-total-wins with Rebel then Informant tie-breaks

## The variation's rules

SETUP: 5 players. Each starts with 0 total points, 0 Rebel points, 0 Informant points. Before round 1 the engine lists all 10 unordered pairs of players and shuffles the list secretly. This is the only random event. In round r (r=1 to 10) the pair in position r is the Informants; the other 3 are Rebels. Every player is Informant in exactly 4 rounds with each other player as partner exactly once, and Rebel in exactly 6 rounds. Players are told this rule but not the order. EACH ROUND, in order: 1. ROLES: Each player is privately told Rebel or Informant for this round. Each Informant is also privately told who the other Informant is. 2. NIGHT (simultaneous): Every player privately names one other player as target. A Rebel target is investigated. An Informant target is framed. An Informant may name any other player including the partner; framing a partner has no extra effect. 3. NIGHT RESULTS: Each Rebel is privately told one result about their target: 'Informant' if the target is an Informant this round OR at least one Informant framed that target this round, otherwise 'Rebel'. A 'Rebel' result is always true; an 'Informant' result may be true or a frame. Informants receive no result. 4. CLAIMS (simultaneous): Every player writes one short message, e.g. claimed role, target or result. Lying allowed. All messages then shown to everyone. 5. RESPONSES (simultaneous): Every player writes one more short message. All shown to everyone. 6. VOTE (simultaneous): Every player names one other player to Terminate. All votes showing who voted for whom are then announced publicly. 7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise every player tied for the most votes is terminated. The round roles of terminated players only are announced publicly; no other roles revealed. 8. SCORING (hidden): Each Rebel who voted for an Informant gains 2 points. If at least one terminated player is an Informant, each Rebel gains 1 more point. Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3). Each Informant who was not terminated this round gains 2 points. Points gained while Rebel are also added to Rebel points; points gained while Informant also added to Informant points. No totals of any kind are announced during the game. Only the votes and the terminated roles are announced each round. Termination removes no one; all 5 play every round. After round 10 the engine announces every player's final total, Rebel points and Informant points and the game ends.

Objective: After 10 rounds the player with the highest total points wins. Tie-break: among tied, most Rebel points wins; if still tied, most Informant points wins; if still tied, draw.

Expected effect: Hiding the ledger restores late-game uncertainty so Informants can still bluff and Rebels must still infer schedule, results and voting intent. Individual survival lets a good Informant profit even if its partner is caught. Talk earns its place: Rebels want to coordinate on a true Informant, Informants want Rebels to vote Rebels; interests conflict. A Rebel who just follows a proposal can lose by voting a Rebel (loses 2, gives Informants 1 each plus survival) while a correct independent vote earns 2-3.

## Complexity (the designer's count, against the limits)

- steps_per_round: 9 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 6 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
