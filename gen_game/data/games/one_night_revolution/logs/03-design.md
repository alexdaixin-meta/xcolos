# 03 design

- time: 2026-10-28T01:35:04+00:00 (73.5s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 ef809e5f7a91f040, reply sha256 2c8c53265e739426

## Sent

````
Original game: One Night Revolution
Players in the original: 3 to 10

Original rules:
Each player gets a secret ID token (Rebel or Informant) plus a secret Specialist card giving a night power; three extra IDs go to the HQ. At night eyes closed, controller leads informants to recognize each other, then clockwise each player opens eyes alone to do their Specialist action which may look at or swap ID tokens. By day, players in order claim a Specialist token (may lie) then discuss freely for 5-10 minutes, without looking at cards, trying to deduce current alignments. Then all simultaneously point at someone to Terminate. Most-voted players reveal IDs. If any Informant is terminated, Rebels win. If none or only Rebels are terminated, Informants win. Rebels can also win by voting in a circle with zero eliminations if all Informant tokens are correctly believed to be on HQ.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: PAYOFF TABLE PER ROUND. If Rebels win, each Rebel gets 2, plus 1 if they voted for a terminated Informant: 6 to 9 points in total. If Informants win, each Informant gets 3: 6 in total. The team payoffs are even, so the problem is not the table. It is the fixed schedule. In a 5-cycle, round r's Informants are positions r and r+1. Each player is told their partner in both Informant rounds, which leaks the next round's Informant.

LEAK, ROUND BY ROUND:
- Round 2: the position-1 player was an Informant in round 1 and is not one now, so they know they are position 1. Their round-1 partner must be position 2, a current Informant. The player knows this for certain.
- Round 3: the position-2 player knows position 3 (their round-2 partner) is an Informant.
- Round 4: the position-3 player knows position 4.
- Round 5: the position-4 player knows position 5.
From round 2 on, a Rebel always knows one Informant for certain. Only round 1 is played mostly blind, so Informant win chances fall steeply after round 1.

HIDDEN-SEAT EDGE. Assume a plausible good-play run: Informants win round 1 and Rebels win rounds 2 to 5. Base scores before bonuses:
- pos1: 3 (round 1 as Informant) + 2+2+2 (Rebel rounds 2, 3, 4) + 0 (round 5 as Informant) = 9
- pos2: 3 + 3 + ... no: 3 (round 1) + 0 (round 2 as Informant) + 2+2+2 (Rebel rounds 3, 4, 5) = 9
- pos3: 0 (Rebel in round 1) + 0 + 0 (Informant rounds 2, 3) + 2+2 = 4
- pos4: 0 + 2 + 0 + 0 + 2 = 4
- pos5: 0 + 2 + 2 + 0 + 0 = 4
Two players lead by 5 only because of where the shuffle put them. Bonuses are worth at most 3 per player, and both leaders can earn all 3.

Expected values with Informant win chances of 0.6, 0.4, 0.2, 0.2, 0.2 for rounds 1 to 5:
- pos2 (Informant in rounds 1 and 2): 3(1.0) + 2(2.4) = 7.8
- pos5 (Informant in rounds 4 and 5): 3(0.4) + 2(1.8) = 4.8
The hidden order gives a large positional edge.

THOUGHTLESS POLICIES.
- 'Always vote the first-listed other player' as a Rebel gives up the bonus and adds noise. It does not avoid losses. As an Informant it free-rides, because Informant points are flat team points.
- If Rebels win every round, everyone scores 6 base, and 9 with perfect votes. That is a five-way DRAW.
- If Informants win every round, everyone scores 6: a DRAW.
Uniform outcomes therefore end in draws, and mixed outcomes are decided by seat. Pairs adjacent in the hidden order share a team in 3 of 5 rounds; non-adjacent pairs share only 1. Any skill gain is therefore shared heavily with neighbours rather than earned individually.
- reasoning_over_luck FAILED: There is real inference: claims, frames, true clears, and cross-round consistency checks. But the outcome under good play is set by the shuffle.

With competent play, round 1 is the only round Informants are favoured. From round 2 a Rebel knows an Informant for certain (see the leak above). The likely result is Informants winning round 1 and Rebels winning rounds 2 to 5. That puts positions 1 and 2 at 9 base and everyone else at 4. With equal bonuses the game is a draw between pos1 and pos2.

If Rebels win all five rounds, all players tie at 9 and the game is drawn. In both cases the winner, or the draw set, comes from the hidden order, not reasoning. Individual skill is diluted because team points are shared, and the only individual reward is a +1 vote bonus, at most 3 per game. I estimate over 60% of the final ranking comes from the shuffle.
- change: Remove the chained 5-cycle schedule. Draw a fresh secret Informant pair each round (one random draw per round is allowed), or hide the schedule so that knowing a partner does not reveal who is an Informant in the next round.
- change: Make scoring individual rather than flat team points:
- each Rebel scores +2 for voting for an Informant and 0 otherwise;
- each Informant scores +1 for every Rebel who voted for a Rebel, and +2 more if no Informant is terminated.
This rewards skill without sharing it with neighbours in the hidden order.
- change: Equalise role exposure across rounds of differing information. Either give every player the same mix of early and late Informant rounds, or score only rounds 2 to 5, so that no hidden position gets the blind round 1 as an Informant advantage.
- change: Replace 'tie = draw' with an arithmetic tiebreak, such as most correct votes as a Rebel and then fewest votes received as an Informant. Uniform round outcomes would then no longer produce five-way draws.
- change: State explicitly whether an Informant may frame their own partner, and that every Rebel investigating a framed player receives 'Informant'.
The variation that was reviewed: One Night Revolution: Five Nights: SETUP: There are 5 players, each starting with 0 points. Before round 1, the engine secretly shuffles the 5 players into a hidden order of positions 1 to 5. This is the only random event in the game. In round r (r = 1 to 5), the Informants are the players at positions r and r+1, with position 6 meaning position 1. The other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 2 rounds and a Rebel in 3. All players are told this quota rule but not the hidden order.

EACH ROUND:
1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.
2. NIGHT (simultaneous): Every player privately names one other player as a target.
   - A Rebel's target is investigated.
   - An Informant's target is framed.
3. NIGHT RESULTS: Each Rebel is privately told one result about their target.
   - The result is 'Informant' if the target is an Informant this round, or if the target was framed by at least one Informant this round.
   - Otherwise the result is 'Rebel'.
   - A 'Rebel' result is always true. An 'Informant' result may be a frame.
   - Informants receive no result.
4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.
5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.
6. VOTE (simultaneous): Every player names one other player to Terminate.
7. TERMINATION:
   - If the highest number of votes any player received is 1 or less, nobody is terminated.
   - Otherwise, every player tied for the most votes is terminated.
   - The round roles of the terminated players are announced publicly.
8. SCORING:
   - If at least one terminated player is an Informant this round, the Rebels win the round. Each Rebel gains 2 points, and each Rebel who voted for a terminated Informant gains 1 additional point.
   - Otherwise, the Informants win the round, and each Informant gains 3 points.
   - Everyone's totals are announced.
9. Termination does not remove anyone; all 5 players take part in every round. After round 5 the game ends. Winner: After 5 rounds, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "One Night Revolution is a hidden-role social deduction game. Rebels try to find and vote out a hidden Informant after a night in which players use secret powers to investigate or swap ID tokens. A day of claims and discussion is followed by one simultaneous vote. The reviewed variation turned it into five rounds among five players, with team points and a fixed chained schedule of Informant pairs.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the reviewed variation, uniform outcomes end in draws. If Rebels win every round, everyone has 6 base points (9 with perfect votes); if Informants win every round, everyone has 6. Mixed outcomes are decided by hidden seat. Positions 1 and 2 reach 9 base points while positions 3 to 5 reach 4 under the likely run of Informants winning round 1 and Rebels winning rounds 2 to 5. Expected value is 7.8 for position 2 against 4.8 for position 5. Informants earn flat team points, so a thoughtless Informant free-rides on their partner."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Claims, frames and cross-round consistency checks reward skill. But points are shared by role, and neighbours in the hidden order share a team in 3 of 5 rounds. The only individual reward is a +1 vote bonus, worth at most 3 per game. An estimated 60% or more of the final ranking comes from the shuffle."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Round 1 is played blind and rounds 2 to 5 are nearly solved for Rebels. From round 2, a Rebel knows one Informant for certain because the schedule leaks. A strong player has little room to outplay others once the leak is understood."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The core is good: hidden roles, frames that can lie, true 'Rebel' clears, and public claims. The chained schedule, though, replaces inference with a certainty, because a former partner's next-round role is known."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Termination, round winner and points are all counting and comparisons on recorded choices."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "The game is text only, uses simultaneous polls and talk, and has no board. The original's eyes-closed sequential night and token swapping were already reduced to simultaneous target choices that fit the engine."
    }
  ],
  "problems": [
    "P1: The chained 5-cycle schedule leaks roles. From round 2, a Rebel knows one current Informant for certain because their former partner is next in the chain.",
    "P2: Hidden seat decides the winner. Positions that are Informants in the blind round 1 gain about a 5-point lead and about 3 more expected points, regardless of play.",
    "P3: Team points dilute skill. Informants score flat team points, so a weak Informant is carried by their partner, and neighbours in the order share most outcomes.",
    "P4: Uniform outcomes produce many-way draws. All Rebel wins or all Informant wins tie everyone.",
    "P5: Individual reward is tiny. The +1 vote bonus, at most 3 per game, is the only thing separating teammates.",
    "P6: Framing rules were unclear. It was not stated whether an Informant may target their partner, or what a Rebel sees when investigating a framed player."
  ],
  "changes": [
    {
      "what": "Replace the chained cycle with all 10 possible Informant pairs among 5 players, each used exactly once, in an order shuffled secretly before round 1. The game lasts 10 rounds.",
      "why": "Every player is an Informant exactly 4 times and a Rebel exactly 6 times, so role exposure is identical. Knowing a past partner only tells you that pair will not recur; it never tells you who is an Informant now.",
      "fixes": "P1"
    },
    {
      "what": "Random order of pairs instead of a fixed position chain, and only terminated players' roles are revealed each round.",
      "why": "No position is structurally tied to the blind first round, and the hidden pair list cannot be reconstructed from public reveals.",
      "fixes": "P2"
    },
    {
      "what": "Fully individual scoring per round. A Rebel scores 2 for voting for an Informant, plus 1 if an Informant is terminated. An Informant scores 1 for each Rebel who voted for a Rebel, plus 2 if no Informant is terminated.",
      "why": "Each player's points come mostly from their own vote or from deceiving specific Rebels. Skill is not shared with whoever happened to be on your team.",
      "fixes": "P3"
    },
    {
      "what": "The individual vote reward is now 2 per round as a Rebel (12 possible over the game). Deception points scale with how many Rebels you misled.",
      "why": "Individual reasoning becomes the main source of points rather than a tiebreaker.",
      "fixes": "P5"
    },
    {
      "what": "Arithmetic tiebreak: most points earned as a Rebel, then most points earned as an Informant, then a draw.",
      "why": "Uniform round outcomes no longer tie everyone, because individual vote accuracy differs.",
      "fixes": "P4"
    },
    {
      "what": "State that an Informant may frame any other player, including their partner (which has no extra effect). Any Rebel who investigates a framed player or an Informant sees 'Informant'.",
      "why": "This removes ambiguity so the night can be built and reasoned about exactly.",
      "fixes": "P6"
    },
    {
      "what": "Publicly announce who voted for whom after each vote.",
      "why": "Gives cross-round evidence for opponent modelling (who frames, who protects whom). Because pairs never repeat, this does not leak future roles.",
      "fixes": "P1"
    }
  ],
  "keeps": [
    "Secret Rebel/Informant roles, with Informants knowing each other.",
    "A night phase where Rebels investigate and Informants frame. A 'Rebel' result is always true; an 'Informant' result may be a frame.",
    "Day claims where lying is allowed, followed by a simultaneous Terminate vote.",
    "Most-voted players are terminated and their roles revealed. Rebels win the round by terminating an Informant.",
    "Five players, simultaneous talk, multiple rounds."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The deduction core works. The failures came from a leaky fixed schedule and shared team points, and both can be fixed within the limits."
  },
  "variation": {
    "name": "One Night Revolution: Ten Nights",
    "summary": "Five players play 10 rounds of a one-night hidden-role game. Every pair of players is the Informant pair exactly once, in a secret random order. Points are individual: Rebels score by voting for Informants, Informants score by misleading Rebels.",
    "players": {
      "min": 5,
      "max": 5,
      "suggested": 5
    },
    "rules": "SETUP: There are 5 players, each starting with 0 points. Each player also keeps two sub-totals, Rebel points and Informant points, both starting at 0. Before round 1, the engine lists all 10 possible pairs of players and shuffles that list secretly. This is the only random event in the game. In round r (r = 1 to 10), the pair in position r of the shuffled list are the Informants; the other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 4 rounds, with each other player as partner exactly once, and a Rebel in exactly 6 rounds. All players are told this rule but not the order.\n\nEACH ROUND:\n1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.\n2. NIGHT (simultaneous): Every player privately names one other player as a target. A Rebel's target is investigated. An Informant's target is framed. An Informant may name any other player, including their partner (framing a partner has no extra effect).\n3. NIGHT RESULTS: Each Rebel is privately told one result about their target. The result is 'Informant' if the target is an Informant this round, or if at least one Informant framed that target this round. Otherwise it is 'Rebel'. A 'Rebel' result is therefore always true; an 'Informant' result may be a frame. Informants receive no result.\n4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.\n5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.\n6. VOTE (simultaneous): Every player names one other player to Terminate. All votes, showing who voted for whom, are then announced publicly.\n7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise, every player tied for the most votes is terminated. The round roles of the terminated players only are announced publicly; no other roles are revealed.\n8. SCORING (individual):\n   - Each Rebel who voted for an Informant gains 2 points.\n   - If at least one terminated player is an Informant, each Rebel gains 1 more point.\n   - Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3).\n   - If no Informant was terminated, each Informant gains 2 more points.\n   - Points gained as a Rebel are also added to that player's Rebel points; points gained as an Informant are also added to their Informant points.\n   - Everyone's totals are announced.\n9. Termination does not remove anyone; all 5 players take part in every round. After round 10 the game ends.",
    "objective": "After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.",
    "expected_effect": "Every player has the same 4 Informant and 6 Rebel rounds, so hidden seat no longer decides the ranking. The order of rounds is random and leaks nothing certain: knowing a past partner only rules out that pair. Points are individual, so a Rebel must find an Informant personally rather than ride a team win, and an Informant earns by convincing specific Rebels to vote wrongly. Talk passes both tests. Rebels and Informants want opposite outcomes, and even Rebels compete with each other for the vote points. A player who simply follows a confident proposal can lose 2 points as a Rebel whenever that proposal came from an Informant framing a Rebel. Public vote records across 10 rounds reward opponent modelling: who claims falsely, who frames, who protects whom. Simple policies lose. Always voting the first-listed other player hits an Informant only about 40% of the time, about 0.8 points per Rebel round against well over 1 for a reasoning player. An Informant who never misleads anyone loses their deception points. Skill should dominate, with modest luck from which rounds you happen to be an Informant in."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 4,
    "attributes": 12,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
