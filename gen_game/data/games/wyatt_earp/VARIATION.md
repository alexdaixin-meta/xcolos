# Variation: Wanted: Dead or Alive (Majority Rule)

Three or four bounty hunters spend a limited posse of deputies over 6 rounds to win control of five outlaws' posters. The most deputies on an outlaw takes its whole poster. Each hunter secretly knows which outlaw carries an extra $3,000 tip, and must cash in on it without giving it away.

Players: 3 to 4, best with 3

## Review of the original

Wyatt Earp is a rummy-style card game for 2 to 4 players. Players draw and meld sets of seven outlaw colours to raise each outlaw's shared reward poster and earn capture points (CP), use sheriff cards for shots, steals and blocks, and at the end of each hand split every poster in proportion to CP. The tested variation, 'Wanted: Dead or Alive', cut this down to five outlaws, 15 deputies per player, a secret informant (2x CP), random sightings and proportional payout.

- **non_degenerate**: bad. In the tested variation a commit of N raised the poster by (N-1)x$1000, so the poster added always went to whoever held the CP. 'Commit 5 to your own informant three times' was near-dominant. An invader collected about $2,430 instead of the $4,000 it would add at home, and handed the victim about $1,570 more. Contesting never paid, so the policy won or drew almost always. Seats were symmetric.
- **skill_sensitive**: bad. Under good play every player builds a poster of $13,000 plus sightings, alone. Sighting differences (Binomial(6,1/5) per outlaw, SD about $1,000) were the whole winning margin, so an estimated 70-90% of the result was chance. The one skilled move, grabbing an unassigned outlaw, was worth $1-2k, the same size as the noise.
- **headroom**: weak. Play was solved after one calculation: three commits of 5 on your own outlaw. A strong player had nothing left to improve, though a weak player still scored something.
- **reasoning_dependent**: bad. Informants showed openly in where players committed, but knowing them changed no decision because contesting helped the owner. The hidden 2x CP never mattered. Talk had nothing to resolve. The original card game's hidden hands are rich, but they rest on a deck, melds and many sheriff effects that the platform cannot carry.
- **verifiable**: good. Posters, CP and proportional payouts were all arithmetic. No judge was needed.
- **fits_platform**: weak. The variation fitted the limits (about 12 steps, 3 choice steps, 1 draw, 6 rounds, about 18 attributes). It did not say the sighting draw was with replacement. The original needs a 100+ card deck, melding, reshuffles and a dozen sheriff effects, which is far past the limits.

## Problems

- P1: Commits raised the poster, and the owner collected most of the raise. Contesting therefore enriched the victim, and 'all deputies on own informant' was near-dominant.
- P2: Under good play the winner was decided by random sighting counts on randomly assigned informants (a lottery).
- P3: The hidden informant had no use. Knowing an opponent's informant changed no decision, and the 2x CP never mattered.
- P4: Talk only added words. Nobody had anything to bargain over, bluff about or threaten.
- P5: The sighting draw did not state that it was with replacement.
- P6: Proportional payout rewarded spending the most deputies rather than out-guessing rivals. There was no contest for control.

## Changes

- Commits no longer raise posters. Posters grow only from a fixed base ($2,000 each), public sightings (+$1,000) and a hidden informant tip (+$3,000, revealed at the end). (fixes: P1): Investing in a rival's outlaw now takes value from the rival instead of adding to it.
- Payout becomes majority-takes-all: the player with the most deputies on an outlaw takes its whole poster, tied leaders split it equally, and an outlaw with no deputies pays nobody. The 2x informant CP is dropped. (fixes: P1, P6): This turns the game into a contest of hidden-value allocation (Colonel Blotto). Piling everything on one outlaw wins at most one poster and leaves the rest to others. Contesting, defending, conceding and sniping all become real choices.
- Each informant secretly adds $3,000 to one outlaw's poster, known only to the player who holds that informant. Base posters are equal, so every informant is worth the same. (fixes: P3, P2): Private knowledge now matters. The holder knows an outlaw is worth more than it looks. Rivals must infer it from commitments and talk. The holder must choose between claiming openly (and inviting a contest) and hiding the claim. Because tips are equal and anyone can win any poster, this is information, not a lottery.
- Sightings stay random but are public, announced before players commit, and contestable by everyone. The rules now state the draw is uniform over the five outlaws, with replacement. (fixes: P2, P5): A sighting changes what is worth fighting for, not who gets it. Good play reacts to sightings, so they cannot decide the winner on their own.
- Deputies drop to 12 per player, at most 4 committed per round, over 6 rounds. All commitments are revealed each round. (fixes: P3, P6): The per-round cap makes timing a decision: commit early to stake a claim (which signals your informant) or hold deputies back for late snipes that rivals cannot fully answer. Public reveals give players the evidence to read informants from.
- The game is set at 3-4 players, keeping simultaneous talk before each commitment. (fixes: P4): Only one player can win. Players bargain over spheres ('you take Blue, I take Green'), bluff about informants, and gang up on a leader. Pacts are not binding, and a final-round snipe punishes anyone who trusts blindly.

## Kept from the original

- Outlaws with public reward posters that grow during play
- Players compete for shares of posters by committing resources, which plays the role of capture points
- Shared bounties: one player's sighting or commitment changes what everyone is chasing
- A secret informant giving private knowledge about one outlaw
- Money from poster payouts decides the winner

## The variation's rules

OUTLAWS: There are five outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at $2,000.

SETUP: Each player receives 12 deputies, which must last the whole game, and $0. Each player is secretly assigned one informant outlaw at random, with no two players sharing one. Only that player knows it. The informant outlaw carries a hidden tip of $3,000, added to its poster at the end of the game. Outlaws that are nobody's informant carry no tip. Each player has a public deputy count on each outlaw, starting at 0. The game lasts 6 rounds.

EACH ROUND:
1. Sighting: one outlaw is drawn uniformly at random from all five (with replacement; the same outlaw may be sighted in several rounds). It is announced, and its poster rises by $1,000.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from 0 to 4. If the number exceeds their remaining deputies, it is reduced to their remaining deputies.
4. Reveal: all choices are announced.
5. Resolution: each player's remaining deputies fall by the number they committed, and their deputy count on the chosen outlaw rises by that number. Commitments do not change posters.

END OF GAME (after round 6):
- All informants are revealed. Each informant outlaw's poster rises by $3,000.
- For each outlaw: if no player has any deputies on it, it escapes and pays nobody. Otherwise the player with the highest deputy count on it receives its whole poster. If several players tie for the highest count, the poster is split equally among them, rounded down to the dollar.
- Unused deputies are worth nothing.
- Each player's money is the sum of their payouts.

Objective: The player with the most money after the final payout wins. If two or more players tie for the most money, the game is a draw.

Expected effect: The prize pool is $25,000 with 3 players (5 x $2,000, plus $6,000 from sightings, plus 3 x $3,000 in tips), or $28,000 with 4. Simple policies now lose. 'Always 4 on own informant' puts 12 deputies on one outlaw by round 3 and wins at most about $6,000. It also reveals the informant at once, while the other two players split about $19,000 of remaining posters, roughly $9,500 each. 'Always 0' scores $0. Random spreading loses to concentrated snipes. 'Always 4 on the highest poster' is predictable and gets tied or out-timed. Good play weighs public sightings against private tips. It reads rivals' informants from their commitment patterns and talk, decides when to reveal a claim and when to hide or feint, and keeps deputies back for the last two rounds, where the cap of 4 per round limits how far anyone can answer a late snipe. Sightings are public and contestable, and every tip is worth the same, so the draw changes what to fight for but not who wins. With all players playing well, the result turns on inference and timing. TALK: Players disagree about who controls which posters, because only one player can win. Typical proposals are dividing the outlaws ('Red and Blue are mine, leave them') or ganging up on the leader. A player who just follows such a pact can lose: the proposer may honour it until round 6 and then snipe the follower's outlaw with a reserve of 4, or may have steered the follower away from the proposer's own informant. Messages can also bluff about one's informant to draw rivals' deputies onto a worthless outlaw. Talk therefore rewards reading trustworthiness and holding back insurance deputies.

## Complexity (the designer's count, against the limits)

- steps_per_round: 11 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 13 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 6 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
