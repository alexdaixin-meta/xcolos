# Variation: One Night Revolution: Ten Nights

Five players play 10 rounds of a one-night hidden-role game. Every pair of players is the Informant pair exactly once, in a secret random order. Points are individual: Rebels score by voting for Informants, Informants score by misleading Rebels.

Players: 5 to 5, best with 5

## Review of the original

One Night Revolution is a hidden-role social deduction game. Rebels try to find and vote out a hidden Informant after a night in which players use secret powers to investigate or swap ID tokens. A day of claims and discussion is followed by one simultaneous vote. The reviewed variation turned it into five rounds among five players, with team points and a fixed chained schedule of Informant pairs.

- **non_degenerate**: bad. In the reviewed variation, uniform outcomes end in draws. If Rebels win every round, everyone has 6 base points (9 with perfect votes); if Informants win every round, everyone has 6. Mixed outcomes are decided by hidden seat. Positions 1 and 2 reach 9 base points while positions 3 to 5 reach 4 under the likely run of Informants winning round 1 and Rebels winning rounds 2 to 5. Expected value is 7.8 for position 2 against 4.8 for position 5. Informants earn flat team points, so a thoughtless Informant free-rides on their partner.
- **skill_sensitive**: weak. Claims, frames and cross-round consistency checks reward skill. But points are shared by role, and neighbours in the hidden order share a team in 3 of 5 rounds. The only individual reward is a +1 vote bonus, worth at most 3 per game. An estimated 60% or more of the final ranking comes from the shuffle.
- **headroom**: weak. Round 1 is played blind and rounds 2 to 5 are nearly solved for Rebels. From round 2, a Rebel knows one Informant for certain because the schedule leaks. A strong player has little room to outplay others once the leak is understood.
- **reasoning_dependent**: weak. The core is good: hidden roles, frames that can lie, true 'Rebel' clears, and public claims. The chained schedule, though, replaces inference with a certainty, because a former partner's next-round role is known.
- **verifiable**: good. Termination, round winner and points are all counting and comparisons on recorded choices.
- **fits_platform**: good. The game is text only, uses simultaneous polls and talk, and has no board. The original's eyes-closed sequential night and token swapping were already reduced to simultaneous target choices that fit the engine.

## Problems

- P1: The chained 5-cycle schedule leaks roles. From round 2, a Rebel knows one current Informant for certain because their former partner is next in the chain.
- P2: Hidden seat decides the winner. Positions that are Informants in the blind round 1 gain about a 5-point lead and about 3 more expected points, regardless of play.
- P3: Team points dilute skill. Informants score flat team points, so a weak Informant is carried by their partner, and neighbours in the order share most outcomes.
- P4: Uniform outcomes produce many-way draws. All Rebel wins or all Informant wins tie everyone.
- P5: Individual reward is tiny. The +1 vote bonus, at most 3 per game, is the only thing separating teammates.
- P6: Framing rules were unclear. It was not stated whether an Informant may target their partner, or what a Rebel sees when investigating a framed player.

## Changes

- Replace the chained cycle with all 10 possible Informant pairs among 5 players, each used exactly once, in an order shuffled secretly before round 1. The game lasts 10 rounds. (fixes: P1): Every player is an Informant exactly 4 times and a Rebel exactly 6 times, so role exposure is identical. Knowing a past partner only tells you that pair will not recur; it never tells you who is an Informant now.
- Random order of pairs instead of a fixed position chain, and only terminated players' roles are revealed each round. (fixes: P2): No position is structurally tied to the blind first round, and the hidden pair list cannot be reconstructed from public reveals.
- Fully individual scoring per round. A Rebel scores 2 for voting for an Informant, plus 1 if an Informant is terminated. An Informant scores 1 for each Rebel who voted for a Rebel, plus 2 if no Informant is terminated. (fixes: P3): Each player's points come mostly from their own vote or from deceiving specific Rebels. Skill is not shared with whoever happened to be on your team.
- The individual vote reward is now 2 per round as a Rebel (12 possible over the game). Deception points scale with how many Rebels you misled. (fixes: P5): Individual reasoning becomes the main source of points rather than a tiebreaker.
- Arithmetic tiebreak: most points earned as a Rebel, then most points earned as an Informant, then a draw. (fixes: P4): Uniform round outcomes no longer tie everyone, because individual vote accuracy differs.
- State that an Informant may frame any other player, including their partner (which has no extra effect). Any Rebel who investigates a framed player or an Informant sees 'Informant'. (fixes: P6): This removes ambiguity so the night can be built and reasoned about exactly.
- Publicly announce who voted for whom after each vote. (fixes: P1): Gives cross-round evidence for opponent modelling (who frames, who protects whom). Because pairs never repeat, this does not leak future roles.

## Kept from the original

- Secret Rebel/Informant roles, with Informants knowing each other.
- A night phase where Rebels investigate and Informants frame. A 'Rebel' result is always true; an 'Informant' result may be a frame.
- Day claims where lying is allowed, followed by a simultaneous Terminate vote.
- Most-voted players are terminated and their roles revealed. Rebels win the round by terminating an Informant.
- Five players, simultaneous talk, multiple rounds.

## The variation's rules

SETUP: There are 5 players, each starting with 0 points. Each player also keeps two sub-totals, Rebel points and Informant points, both starting at 0. Before round 1, the engine lists all 10 possible pairs of players and shuffles that list secretly. This is the only random event in the game. In round r (r = 1 to 10), the pair in position r of the shuffled list are the Informants; the other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 4 rounds, with each other player as partner exactly once, and a Rebel in exactly 6 rounds. All players are told this rule but not the order.

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

Objective: After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.

Expected effect: Every player has the same 4 Informant and 6 Rebel rounds, so hidden seat no longer decides the ranking. The order of rounds is random and leaks nothing certain: knowing a past partner only rules out that pair. Points are individual, so a Rebel must find an Informant personally rather than ride a team win, and an Informant earns by convincing specific Rebels to vote wrongly. Talk passes both tests. Rebels and Informants want opposite outcomes, and even Rebels compete with each other for the vote points. A player who simply follows a confident proposal can lose 2 points as a Rebel whenever that proposal came from an Informant framing a Rebel. Public vote records across 10 rounds reward opponent modelling: who claims falsely, who frames, who protects whom. Simple policies lose. Always voting the first-listed other player hits an Informant only about 40% of the time, about 0.8 points per Rebel round against well over 1 for a reasoning player. An Informant who never misleads anyone loses their deception points. Skill should dominate, with modest luck from which rounds you happen to be an Informant in.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 12 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
