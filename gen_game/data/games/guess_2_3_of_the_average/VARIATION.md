# Variation: Leaning Beauty Contest

Each round, 3 or 4 players secretly guess a whole number. Each player is aiming at their own target: two-thirds of the average guess, plus 10, plus a hidden personal lean of +6 or -6 that stays fixed all game. The closest player scores the round. Guesses are public, leans are not, and winning takes a lead of at least 2 rounds after 10 rounds.

Players: 3 to 4, best with 3

## Review of the original

Guess 2/3 of the average: every player secretly picks a number from 0 to 100, and whoever is closest to two-thirds of the mean of all picks wins. The previous XColos variation added a fresh private card each round that shifted the target (T = (2/3)G + 2C), a hidden length of 8 to 12 rounds, a talk phase, and a lowest-total-distance winner.

- **non_degenerate**: weak. No single action wins outright. The card term keeps 0 from dominating, and guesses tied to the card beat a constant guess. But the margin is thin. A player who ignores the card and always guesses about 45 loses only about 1 point of distance per round. Over about 10 rounds the sd of the difference between totals is about 10, so the thoughtless policy still wins roughly 35 to 40% of games against a reasoner.
- **skill_sensitive**: bad. Under the equilibrium rule g ≈ 39.6 + 0.716c, each player's error comes from the two unseen cards (sd ≈ 4.6 each). The target moves about 0.83 points per point of each other card, so the error sd is ≈ 5.4 per round. Between equal good players the difference in totals has sd ≈ 10 to 12, while skill gaps are worth about 1 point per round. The deal decides most games.
- **headroom**: weak. The only real inference is the linear rule, solved in one step and then repeated. Rounds are independent, so later rounds teach nothing new. A weak player scores easily because the noise hides their mistakes. A strong player has nowhere to improve once the rule is found.
- **reasoning_dependent**: weak. There is hidden information (the cards), but no inference can recover it. Talk is babbling: a true card claim helps the opponents, and a false claim pulls their guesses away from T, which helps the liar, so no claim is credible. The hidden horizon adds nothing because rounds are independent and nothing carries over except totals.
- **verifiable**: good. The target, the distances and the totals are pure arithmetic on revealed numbers.
- **fits_platform**: good. It uses a simultaneous numeric poll, one deal per round, arithmetic scoring and a fixed or counted end, with no board. It fits the limits, but it spends its one random draw per round on noise.

## Problems

- P1: The per-round card deal puts noise into every target (error sd ≈ 5.4 per round) that is far larger than the skill differences, so among good players the deal picks the winner (lottery trap).
- P2: Nothing persists from round to round, so there is nothing to learn about opponents over time. The only inference is a one-step linear rule, and the game is solved after round 1.
- P3: Talk is cheap and adversarial (lying helps the liar), so it settles into babbling and adds words without reasoning.
- P4: The hidden 8 to 12 round horizon creates no planning decision because rounds are independent. It is idle uncertainty.
- P5: Lowest total distance lets a thoughtless constant guess stay competitive, because small per-round losses are buried in noise.
- P6: Any variant with persistent hidden information leaves some luck in the first rounds, before it can be inferred. A plain higher-total winner would let that early luck alone separate equal players.

## Changes

- Remove the per-round card deal. Each player instead gets one hidden personal lean of +6 or -6 (independent coin flip) at the start, fixed for the whole game. Each player's own target is (2/3) x average guess + 10 + their lean. (fixes: P1): The only random event happens once, and it is symmetric. A player's own lean does not make them closer or farther on average; it only changes what they should guess. After the first rounds the targets are pinned down by play, not by fresh draws.
- Show every player's guess publicly each round, but tell each player only their own target and distance. Leans are never announced. (fixes: P2): Opponents' leans must be inferred from their guesses. Those guesses mix the lean with each opponent's reasoning level and habits, which persist across rounds. Reading them predicts the next average, so modelling opponents over rounds pays.
- Score by round wins instead of total distance. Each round, the player or players with the smallest distance to their own target score 1 point. (fixes: P5): Only being the closest counts. A constant or careless guess that is a few points off loses the round outright instead of losing a little distance, so skill shows round by round.
- Margin winner rule: after 10 rounds a player wins only if their points exceed every other player's by at least 2. Otherwise the game is a draw. (fixes: P6): The one luck-affected stretch is round 1, while leans are unknown. A single lucky round cannot decide a game between equal good players; they draw. Winning requires repeatedly out-predicting opponents.
- Replace the hidden 8 to 12 round length with a known fixed 10 rounds. (fixes: P4): The hidden horizon created no decision. A known length removes idle uncertainty and lets players plan how to probe and exploit over the game.
- Drop the talk phase. (fixes: P3): Claims about one's lean are not credible because a successful lie makes opponents miss. Interests are purely opposed (only the closest scores), so talk would be babbling. Guesses themselves are the honest signal.
- Restrict to 3 or 4 players with leans of exactly ±6 and whole-number guesses. (fixes: P1): With these sizes every equilibrium guess is a whole number, so exact hits and clean ties are possible. With 3 or more players, a correct guess about one rival's mistake can be exploited by another player.

## Kept from the original

- The core rule: be closest to two-thirds of the average of everyone's guesses.
- A simultaneous secret numeric guess from 0 to 100.
- Level-k reasoning about how deeply the others think, now repeated so their habits can be read.
- A private element that shifts each player's target, as the card did, but persistent instead of re-dealt.

## The variation's rules

SETUP: Each player starts with 0 points. For each player separately, the engine flips a fair coin to set that player's LEAN to +6 or -6. Each player is told only their own lean, and it stays the same for the whole game. Leans are never announced. Players know that every lean is +6 or -6, chosen independently with equal chance. The game lasts exactly 10 rounds, and players know this.

EACH ROUND:
1. Guess. All players at the same moment secretly choose a whole number from 0 to 100 inclusive. A missing or invalid guess counts as 0.
2. Average. G = the sum of all guesses divided by the number of players.
3. Targets. Each player's own target is T = (2/3) x G + 10 + that player's lean.
4. Distance. Each player's distance is the absolute value of (their guess - their own target).
5. Score. Find the smallest distance among all players. Every player whose distance equals it scores 1 point; if several tie, each of them scores 1.
6. Public announcement. Announce to everyone: the round number, every player's guess, G, which player or players scored this round, and every player's point total.
7. Private message. Tell each player privately their own target and their own distance. They are not told anyone else's.
8. End check. After round 10 the game ends; otherwise play the next round.

END: Compare point totals after round 10.

Objective: After 10 rounds, if one player's point total is at least 2 more than every other player's total, that player wins. In every other case (two players level, or the leader ahead by only 1) the game is a draw.

Expected effect: If all leans were known, everyone could hit their target exactly. The average would be 30 + 3 x (mean lean), and each player's best guess would be (2/3) x G + 10 + their own lean. For example, with 3 players and leans +6, -6, -6, G = 24 and the best guesses are 32, 20 and 20. In round 1 leans are unknown, so a good player guesses about 30 + 1.29 x own lean and misses by about 0 or 3.4 depending on the others' leans. That luck lasts about one round, and the margin rule stops one lucky round from deciding a game. From round 2 on, players read rivals' leans and habits from their public guesses. Equal strong players then hit exactly, tie every round and draw. Against imperfect opponents, the winner is whoever best predicts how far others will deviate: over- or under-thinking, anchoring on their last guess, sticking near 30, or masking their lean at the cost of losing rounds. Simple policies all lose: always 0 or always 100 is far from every possible target (at least 4 and at most 52); a constant 30 is about 6 off whenever the leans do not happen to fit; random guessing rarely scores. Even a perfect equilibrium player can be out-scored by one who correctly anticipates a weak third player's error. Talk is left out because only the closest player scores, so interests are purely opposed, and a lie about one's lean helps the liar, so any talk would be babbling.

## Complexity (the designer's count, against the limits)

- steps_per_round: 10 (limit 20)
- choice_steps_per_round: 1 (limit 4)
- attributes: 8 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 10 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
