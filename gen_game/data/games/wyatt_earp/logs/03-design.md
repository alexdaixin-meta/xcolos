# 03 design

- time: 2026-10-28T04:09:17+00:00 (76.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 03faeb6db9dd55db, reply sha256 96e236a39fc1530a

## Sent

````
Original game: Wyatt Earp
Players in the original: 2 to 4

Original rules:
The game is played over multiple hands. Seven outlaw colors exist. Setup: 10 cards dealt to each player, remaining cards form a draw pile with one discard. Each outlaw has a reward poster starting at $1000. On your turn you must draw: either 2 from draw pile or 1 from discard. Then you may play any number of outlaw cards of one or more colors, but at most one sheriff card. The first play for a color must be a set of at least 3 same-color outlaws. Later any number can be added. When you play N cards of a color, add (N-1)*$1000 to that poster's bounty. Sheriff cards modify CP and bounty: Photo adds 4 CP and $1000, requires color already opened; Stagecoach and Bank Robbery require a shot - reveal top draw card, succeed on outlaw (bullet hole) then add 1 CP+$3000 or 2 CP+$1000. Other sheriffs steal, block, etc. You must discard one card to end turn, with no effect. When draw pile empties first time, reshuffle discard except top card. When it empties second time, hand ends and each poster is split among players proportional to CP in that color. Most total money after agreed number of hands wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: MAIN DECISION. In round r a player chooses an outlaw and N (0 to 5). Committing N raises the poster by (N-1)x$1000. Over 15 deputies the poster added is (sum of N) minus (number of commits) = 15 - k, in thousands. Three commits of 5 add $12,000; five commits of 3 add $10,000; fifteen commits of 1 add $0. So the only sensible size is N=5 in three of the six rounds.

OWN INFORMANT, UNCONTESTED. Three commits of 5 give a poster of 1000 + 12000 + S, where S is $1000 per sighting of that outlaw. The player holds 30 CP of 30, so the payout is $13,000 + S.

INVASION TABLE. Opponent B commits 5 to A's informant, on top of A's 30 CP:
| | Poster | CP split | A gets | B gets |
|---|---|---|---|---|
| B stays home | 13000+S | 30/30 | 13000+S | 0 from this poster; +4000 at home |
| B invades | 17000+S | 30/35 vs 5/35 | 14571+ | 2428+ |
- Invading pays B about $2,430, against the $4,000 B would add to its own all-owned poster.
- Invading pays the victim A about +$1,570.
- Contesting is therefore worse for the invader and better for the victim, in every case.
- The 2x informant CP only matters when an outlaw is contested, and contesting never pays.
- So 'commit 5 to your own informant until deputies run out' is effectively dominant. The only refinement is that one 5-commit may go to an unassigned outlaw, worth (1000 + S_u + 4000) instead of 4000, when it is clearly uncontested.

THOUGHTLESS POLICY 'always 5, own informant', by WINNER RULE:
- Against random play (spread N, random outlaws): the random player adds less poster value and splits what it adds. The policy wins about every game.
- Against sensible play: sensible play is the same policy, plus at most one grab of an unassigned outlaw. The result is about $13,000 to $14,000 each plus sightings, so the winner is whoever had more sightings on their own outlaw. The policy does not lose systematically.
- Against itself: equal base totals, so ties happen whenever sighting counts on the informants are equal, giving frequent draws.
- Conclusion: the policy wins or draws almost always and loses only to sighting luck or to a slightly better grab. That fails the check.

SEATS. Choices are simultaneous and informants are symmetric, so neither seat has an edge. The game is still not balanced in the sense required: one near-dominant policy, no reason to interact.
- playable FAILED: WHAT WORKS.
- Limits: 12 steps, 3 choice steps, 1 random draw, 6 rounds and 2 hidden elements are all within platform limits.
- Attribute count: per player there are deputies, informant, 5 CP and money (8 attributes); per table there are 5 posters and 5 deputy totals (10). That is about 18 attribute types, not the stated 14, but still at most 20.
- Proportional payout is arithmetic (calc).
- Choices are a simultaneous poll and the game is finite.

PROBLEMS.
1. The sighting draw does not say whether it is with replacement. It must be, because there are 6 rounds and 5 outlaws, but the rule should say so.
2. Talk is simultaneous, which is correct, but it only adds words.
   - Every player's best move is to pile onto their own informant.
   - Invading another player's poster enriches that player, so there is nothing to negotiate, threaten or bluff about.
   - Informants can be deduced from nothing useful, since knowing one changes no decision.
   - The only real conflict, who grabs an unassigned outlaw, is a one-shot simultaneous coordination that the talk rule does not frame.
   - This is talk present where everyone just follows their own obvious plan.
- reasoning_over_luck FAILED: OUTCOME UNDER INTENDED GOOD PLAY. Every player commits 5, 5, 5 to their own informant, giving each player $13,000 plus sightings on their informant.

THE SIGHTING DIFFERENCE IS PURE CHANCE.
- Each outlaw gets Binomial(6, 1/5) sightings: mean 1.2, SD about 0.98, so about $1,000 per player.
- Sighting differences of $1,000 to $3,000 are the entire winning margin.
- The informant is also assigned at random, so which posters get sighted decides the winner outright.
- Estimated share of the result due to chance: 70 to 90% among competent players.

THERE IS NOTHING USEFUL TO INFER.
- Opponents' informants are visible from where they commit, but the knowledge cannot be exploited: contesting helps the owner.
- The hidden CP multiplier changes no decision.
- The one real reasoning point, timing a single 5-commit onto an unassigned outlaw after seeing sightings and predicting whether others will also go there, is worth about $1,000 to $2,000. That is comparable to sighting noise, so a good reasoner is not clearly favoured.
- change: Make contesting an opponent's outlaw harmful to that opponent. Contributions should not raise a poster that the owner then mostly collects. For example: posters rise only from sightings and a fixed per-round amount, not from commits. Or: the player with the most CP on an outlaw takes 70% and the rest is split, and the informant's 2x matters only in a contested majority. Then invading and defending become real decisions and the 'always 5 on own informant' policy can lose.
- change: Reduce sighting luck so good play decides ties of base value. Options: announce the full 6-round sighting schedule at setup; or let the deputies committed in a round determine which outlaw is sighted next; or cut the sighting bonus to $500 and give each outlaw a fixed known number of sightings.
- change: Give hidden information a use. For example, award a $3,000 bonus for correctly naming an opponent's informant at game end. Or let informants be bluffable by having commits on any outlaw count 2x only if that outlaw is the committer's informant AND they hold the majority, so that misdirection in talk and commitments pays.
- change: State that the sighting draw is with replacement (uniform over 5 each round).
- change: Once contesting matters, keep simultaneous talk but give it something to resolve, such as who goes for which unassigned or contested outlaw, with a real cost to following a rival's proposal. Otherwise remove the talk step.
- change: Verify with a worked table that, after the changes, a pure 'own informant, 5 per round' policy loses to sensible play in a meaningful share of games, and that the all-good-play winner is not decided by the random draw alone.
The variation that was reviewed: Wanted: Dead or Alive: OUTLAWS: There are five outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at $1000.

SETUP: Each player receives 15 deputies, which must last the whole game, and $0. Each player is secretly assigned one informant outlaw, chosen at random so that no two players share an informant. Only that player knows it. Each player has a hidden capture-point (CP) count for each outlaw, starting at 0. The game lasts 6 rounds.

EACH ROUND:
1. Sighting: one outlaw is drawn at random from the five and announced as Sighted. Its poster immediately rises by $1000.
2. Talk: every player writes one short message at the same time. Nobody sees the others' messages before writing. All messages are then shown to everyone. Talk is not binding.
3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from 0 to 5. The number may not exceed their remaining deputies; if it does, it is reduced to their remaining deputies.
4. Reveal: all choices (outlaw and number) are announced. CP is not announced.
5. Resolution, for each player who committed N of 1 or more deputies:
   (a) The player's remaining deputies fall by N.
   (b) The outlaw's public deputy total rises by N.
   (c) The player's hidden CP on that outlaw rises by N, or by 2N if it is their informant outlaw.
   (d) The outlaw's poster rises by (N-1) x $1000.
   Several players may commit to the same outlaw in the same round; each is resolved separately.

END OF GAME (after round 6):
- An outlaw with a public deputy total below 4 escapes. Its poster pays nobody.
- Every other poster is paid out. Each player with CP on that outlaw receives the poster value x (their CP on it / all players' CP on it), rounded down to the dollar.
- Unused deputies are worth nothing.
- All CP and informants are revealed, and each player's money is the sum of their payouts. Winner: The player with the most money after the final payout wins. If two or more players tie for the most, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Wyatt Earp is a rummy-style card game for 2 to 4 players. Players draw and meld sets of seven outlaw colours to raise each outlaw's shared reward poster and earn capture points (CP), use sheriff cards for shots, steals and blocks, and at the end of each hand split every poster in proportion to CP. The tested variation, 'Wanted: Dead or Alive', cut this down to five outlaws, 15 deputies per player, a secret informant (2x CP), random sightings and proportional payout.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the tested variation a commit of N raised the poster by (N-1)x$1000, so the poster added always went to whoever held the CP. 'Commit 5 to your own informant three times' was near-dominant. An invader collected about $2,430 instead of the $4,000 it would add at home, and handed the victim about $1,570 more. Contesting never paid, so the policy won or drew almost always. Seats were symmetric."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Under good play every player builds a poster of $13,000 plus sightings, alone. Sighting differences (Binomial(6,1/5) per outlaw, SD about $1,000) were the whole winning margin, so an estimated 70-90% of the result was chance. The one skilled move, grabbing an unassigned outlaw, was worth $1-2k, the same size as the noise."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Play was solved after one calculation: three commits of 5 on your own outlaw. A strong player had nothing left to improve, though a weak player still scored something."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "Informants showed openly in where players committed, but knowing them changed no decision because contesting helped the owner. The hidden 2x CP never mattered. Talk had nothing to resolve. The original card game's hidden hands are rich, but they rest on a deck, melds and many sheriff effects that the platform cannot carry."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Posters, CP and proportional payouts were all arithmetic. No judge was needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The variation fitted the limits (about 12 steps, 3 choice steps, 1 draw, 6 rounds, about 18 attributes). It did not say the sighting draw was with replacement. The original needs a 100+ card deck, melding, reshuffles and a dozen sheriff effects, which is far past the limits."
    }
  ],
  "problems": [
    "P1: Commits raised the poster, and the owner collected most of the raise. Contesting therefore enriched the victim, and 'all deputies on own informant' was near-dominant.",
    "P2: Under good play the winner was decided by random sighting counts on randomly assigned informants (a lottery).",
    "P3: The hidden informant had no use. Knowing an opponent's informant changed no decision, and the 2x CP never mattered.",
    "P4: Talk only added words. Nobody had anything to bargain over, bluff about or threaten.",
    "P5: The sighting draw did not state that it was with replacement.",
    "P6: Proportional payout rewarded spending the most deputies rather than out-guessing rivals. There was no contest for control."
  ],
  "changes": [
    {
      "what": "Commits no longer raise posters. Posters grow only from a fixed base ($2,000 each), public sightings (+$1,000) and a hidden informant tip (+$3,000, revealed at the end).",
      "why": "Investing in a rival's outlaw now takes value from the rival instead of adding to it.",
      "fixes": "P1"
    },
    {
      "what": "Payout becomes majority-takes-all: the player with the most deputies on an outlaw takes its whole poster, tied leaders split it equally, and an outlaw with no deputies pays nobody. The 2x informant CP is dropped.",
      "why": "This turns the game into a contest of hidden-value allocation (Colonel Blotto). Piling everything on one outlaw wins at most one poster and leaves the rest to others. Contesting, defending, conceding and sniping all become real choices.",
      "fixes": "P1, P6"
    },
    {
      "what": "Each informant secretly adds $3,000 to one outlaw's poster, known only to the player who holds that informant. Base posters are equal, so every informant is worth the same.",
      "why": "Private knowledge now matters. The holder knows an outlaw is worth more than it looks. Rivals must infer it from commitments and talk. The holder must choose between claiming openly (and inviting a contest) and hiding the claim. Because tips are equal and anyone can win any poster, this is information, not a lottery.",
      "fixes": "P3, P2"
    },
    {
      "what": "Sightings stay random but are public, announced before players commit, and contestable by everyone. The rules now state the draw is uniform over the five outlaws, with replacement.",
      "why": "A sighting changes what is worth fighting for, not who gets it. Good play reacts to sightings, so they cannot decide the winner on their own.",
      "fixes": "P2, P5"
    },
    {
      "what": "Deputies drop to 12 per player, at most 4 committed per round, over 6 rounds. All commitments are revealed each round.",
      "why": "The per-round cap makes timing a decision: commit early to stake a claim (which signals your informant) or hold deputies back for late snipes that rivals cannot fully answer. Public reveals give players the evidence to read informants from.",
      "fixes": "P3, P6"
    },
    {
      "what": "The game is set at 3-4 players, keeping simultaneous talk before each commitment.",
      "why": "Only one player can win. Players bargain over spheres ('you take Blue, I take Green'), bluff about informants, and gang up on a leader. Pacts are not binding, and a final-round snipe punishes anyone who trusts blindly.",
      "fixes": "P4"
    }
  ],
  "keeps": [
    "Outlaws with public reward posters that grow during play",
    "Players compete for shares of posters by committing resources, which plays the role of capture points",
    "Shared bounties: one player's sighting or commitment changes what everyone is chasing",
    "A secret informant giving private knowledge about one outlaw",
    "Money from poster payouts decides the winner"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The structure of posters plus contested shares works. Majority control, hidden equal-value tips and public contestable sightings make inference, timing and bluffing decide the game within the limits."
  },
  "variation": {
    "name": "Wanted: Dead or Alive (Majority Rule)",
    "summary": "Three or four bounty hunters spend a limited posse of deputies over 6 rounds to win control of five outlaws' posters. The most deputies on an outlaw takes its whole poster. Each hunter secretly knows which outlaw carries an extra $3,000 tip, and must cash in on it without giving it away.",
    "players": {"min": 3, "max": 4, "suggested": 3},
    "rules": "OUTLAWS: There are five outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at $2,000.\n\nSETUP: Each player receives 12 deputies, which must last the whole game, and $0. Each player is secretly assigned one informant outlaw at random, with no two players sharing one. Only that player knows it. The informant outlaw carries a hidden tip of $3,000, added to its poster at the end of the game. Outlaws that are nobody's informant carry no tip. Each player has a public deputy count on each outlaw, starting at 0. The game lasts 6 rounds.\n\nEACH ROUND:\n1. Sighting: one outlaw is drawn uniformly at random from all five (with replacement; the same outlaw may be sighted in several rounds). It is announced, and its poster rises by $1,000.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.\n3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from 0 to 4. If the number exceeds their remaining deputies, it is reduced to their remaining deputies.\n4. Reveal: all choices are announced.\n5. Resolution: each player's remaining deputies fall by the number they committed, and their deputy count on the chosen outlaw rises by that number. Commitments do not change posters.\n\nEND OF GAME (after round 6):\n- All informants are revealed. Each informant outlaw's poster rises by $3,000.\n- For each outlaw: if no player has any deputies on it, it escapes and pays nobody. Otherwise the player with the highest deputy count on it receives its whole poster. If several players tie for the highest count, the poster is split equally among them, rounded down to the dollar.\n- Unused deputies are worth nothing.\n- Each player's money is the sum of their payouts.",
    "objective": "The player with the most money after the final payout wins. If two or more players tie for the most money, the game is a draw.",
    "expected_effect": "The prize pool is $25,000 with 3 players (5 x $2,000, plus $6,000 from sightings, plus 3 x $3,000 in tips), or $28,000 with 4. Simple policies now lose. 'Always 4 on own informant' puts 12 deputies on one outlaw by round 3 and wins at most about $6,000. It also reveals the informant at once, while the other two players split about $19,000 of remaining posters, roughly $9,500 each. 'Always 0' scores $0. Random spreading loses to concentrated snipes. 'Always 4 on the highest poster' is predictable and gets tied or out-timed. Good play weighs public sightings against private tips. It reads rivals' informants from their commitment patterns and talk, decides when to reveal a claim and when to hide or feint, and keeps deputies back for the last two rounds, where the cap of 4 per round limits how far anyone can answer a late snipe. Sightings are public and contestable, and every tip is worth the same, so the draw changes what to fight for but not who wins. With all players playing well, the result turns on inference and timing. TALK: Players disagree about who controls which posters, because only one player can win. Typical proposals are dividing the outlaws ('Red and Blue are mine, leave them') or ganging up on the leader. A player who just follows such a pact can lose: the proposer may honour it until round 6 and then snipe the follower's outlaw with a reserve of 4, or may have steered the follower away from the proposer's own informant. Messages can also bluff about one's informant to draw rivals' deputies onto a worthless outlaw. Talk therefore rewards reading trustworthiness and holding back insurance deputies."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 11,
    "choice_steps_per_round": 3,
    "attributes": 13,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 6
  }
}
```
````
