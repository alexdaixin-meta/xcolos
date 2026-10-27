# 04 design

- time: 2026-10-27T21:18:20+00:00 (492.2s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 071c23de3aa3b860, reply sha256 8dbd98eecce18156

## Sent

````
Original game: Guess 2/3 of the average
Players in the original: 2 to 100

Original rules:
Each player privately chooses a real number between 0 and 100 inclusive. All choices are revealed at the same time. Compute the arithmetic mean of all chosen numbers, then multiply by 2/3 to get the target number. The player whose chosen number is closest to the target wins. If several players are equally close, they tie for the win. The game is played once, though it can be repeated to study learning.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Complete and finite: invalid=0, rounding set, 10 rounds, 13 steps 2 choices 11 attrs 1 hidden 1 draw all within limits, simultaneous talk and guesses, arithmetic lowest-total win, no judge needed. But talk fails: if all truthful all know xbar all guess 3xbar all distance 0 all draw, so honesty never wins. Lying wins e.g. n=3 cards 10/10/10 true T=30; liar claims 30 believers guess 50 liar best ~40.6 liar dist 0 vs ~9.4. Cards revealed so lies caught but punishment only distrust, none in round 10, so round10 ignore messages, unravels backward. Safe ignore-and-use-own-card cannot be exploited, talk only adds words. Also cooperation unravels late.
- reasoning_over_luck FAILED: Among good players winner by deal. Ex n=3 cards 2/15/28 xbar=15 guesses 39.9/45/50.1 G=45 T=45 dist 5.1/0/5.1 middle card wins. Ex 0/1/2 T=27.3 dist 11.8/12.2/12.6 lowest card wins. Over 10 rounds totals differ only by deal noise sd ~5 per round. Own-card coef b only 0.39 to 0.15, unseen-card uncertainty sd ~6, so edge of equilibrium over Always45 is 1-3 pts vs noise 5-6. Chance >50% of result among competent players; reasoning dominates only vs naive 0/33/random.
- change: Raise private-info value e.g. T=(2/3)G+2*xbar with cards 0-15 so b>0.6 and skill > noise.
- change: Give talk stakes e.g. optional verifiable reveal at small cost or private neighbour peek via private_channel so lies can be inferred.
- change: Score rounds by rank points not summed raw distance so common deal shock does not decide totals.
- change: Stop round-10 unravel e.g. hidden length 8-12 so honesty can pay.
The variation that was reviewed: Hidden-Card Beauty Contest: Setup: 3 to 6 players. Each player starts with a penalty total of 0. The game lasts 10 rounds. The deck consists of 31 cards numbered 0, 1, 2, ..., 30.

Each round:
1. Deal. Shuffle all 31 cards and deal one card face down to each player. Each player sees only their own card. The undealt cards are not used this round.
2. Talk. Every player writes one short message (at most 40 words) at the same time, without seeing the others' messages. Players may say anything, including true or false claims about their card. Nothing said is binding. All messages are then shown to everyone.
3. Guess. Every player privately and simultaneously chooses a whole number from 0 to 100 inclusive. An invalid or missing guess counts as 0.
4. Reveal and score. All guesses and all dealt cards are revealed.
   - Average guess G = sum of guesses divided by the number of players.
   - Average card C = sum of dealt cards divided by the number of players.
   - Target T = (2/3) x G + C.
   - Each player's distance this round = |their guess - T|, rounded to two decimals.
   - Each player's distance is added to their penalty total.
5. Announce. Announce the target and every player's card, guess, distance and penalty total.
6. If 10 rounds have been played, the game ends. Otherwise start the next round. Winner: After round 10, the player with the lowest penalty total wins. If two or more players share the lowest total, the game is a draw among them.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
{
  "original_summary": "Repeated beauty contest where each player guesses 0-100 to be closest to two-thirds of the average guess, with a private card shifting the target.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No seat edge with symmetric deal; guesses matter. One-shot liar can win e.g. n=3 cards 10/10/10, liar claims 30, believers guess 50, liar guesses ~40.6 and wins distance 0 vs ~9.4, so choices change outcome and no always-guess is unbeatable."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "bad",
      "evidence": "Among competent players winner is by deal. Ex cards 2/15/28, equilibrium guesses 39.9/45/50.1, middle wins; ex 0/1/2 lowest wins. Edge of using own card over Always45 is 1-3 pts vs per-round noise sd ~5-6, so chance >50% of result among good players."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Strong beats naive 0/33/random, but among competent little headroom: own-card coefficient b only 0.39 to 0.15, unseen-card uncertainty sd ~6, so improvement plateaus and totals differ only by deal noise."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "Talk adds no reasoning: if all truthful all know Cbar all guess same all distance 0 all draw, so honesty never wins; lying wins; safe ignore-and-use-own-card cannot be exploited. Round 10 messages ignored, unravels backward, cooperation unravels late."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Winner follows by arithmetic: G, C, T=(2/3)G+C, distance |guess-T| summed to penalty total, lowest wins. No judge needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Turn-based text-only, 10 rounds, 13 steps 2 choices 11 attrs 1 hidden 1 draw within limits, simultaneous talk and guesses, no board."
    }
  ],
  "problems": [
    "Cheap talk has no stakes: truthful sharing leads to all-tie draw, unilateral lie wins a round, cards revealed but punishment is only distrust with no payoff bite, so rational play ignores messages.",
    "Endgame unraveling: fixed 10 rounds, last round has no future so all ignore talk and play own-card only, induction unravels honesty backward.",
    "Lottery trap among good players: with T=(2/3)G+C and cards 0-30, private-info weight b 0.15-0.39 is small, unseen-card sd ~6 dominates 1-3 pt skill edge, middle/extreme card decides who is closest, totals differ by deal noise.",
    "Low value of inference: ignoring others loses little, so opponent modelling and reading messages barely pays versus Always45."
  ],
  "changes": [
    {
      "what": "Raise private-info weight to T=(2/3)G+2*C with cards 0-15, equilibrium guess 6*card and target 6*C",
      "why": "Own-card coefficient becomes 2/n (0.67 at n=3, 0.5 at n=4) instead of 1/n. Ignoring messages now costs ~6-24 points per round versus 1-3, so using own card plus inferring others' cards dominates naive 45 and skill exceeds per-round noise.",
      "fixes": "Lottery trap among good players: with truthful sharing all get ~0 regardless of cards, without sharing all lose large; Low value of inference"
    },
    {
      "what": "Keep summed-distance lowest-total win (positive-sum) instead of rank points",
      "why": "With sharing all can get 0 together; a liar stays at 0 once but pushes victims to ~20+, gaining relative standing once but destroying future cooperation worth ~20+ per round. Rank would be zero-sum average 1 and make all-tie no better than distrust, so cooperation could never pay.",
      "fixes": "Cheap talk has no stakes: truthful sharing leads to all-tie draw, unilateral lie wins a round"
    },
    {
      "what": "Hidden uncertain horizon: secret FinalRound uniform 8-12 drawn once at start, players told only 8-12 rounds",
      "why": "No known last round to defect for free; honesty can be sustained by future loss, and after one defection returning to truthful sharing (0 per round vs ~24 in distrust) still pays, stopping backward unravel.",
      "fixes": "Endgame unraveling: fixed 10 rounds, last round has no future so all ignore talk and play own-card only"
    },
    {
      "what": "Restrict to 3-4 players, suggested 3, same simultaneous 40-word talk then simultaneous 0-100 guess each round",
      "why": "Keeps own-card weight high and noise low, keeps talk simultaneous so no leader-following, preserves identity while making listening valuable and blind following punishable.",
      "fixes": "Low value of inference"
    }
  ],
  "keeps": [
    "Beauty-contest core: guess 0-100 to be closest to (2/3) average guess plus card component",
    "Private card dealt each round, seen only by owner until reveal, then all cards and guesses revealed",
    "Simultaneous cheap talk before simultaneous guess, non-binding, can be true or false",
    "Penalty total of summed absolute distances, lowest wins, arithmetic with no judge"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "Talk failure, unraveling and lottery are fixable inside limits by raising card weight, keeping positive-sum scoring, and hiding the horizon; core guessing remains."
  },
  "variation": {
    "name": "High-Weight Hidden-Horizon Beauty Contest",
    "summary": "3-4 players repeatedly guess to hit two-thirds average guess plus twice average private card, with simultaneous cheap talk and a secret 8-12 round ending; lowest summed distance wins.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "Setup: Each player starts with penalty total 0. The engine secretly picks FinalRound uniformly from {8,9,10,11,12}. Players are told the game lasts 8 to 12 rounds inclusive but not the exact number. The deck is 16 cards numbered 0,1,2,...,15. Each round in order: 1. Deal. Shuffle the 16 cards and deal one face down to each player. Each player sees only their own card. Undealt cards are unused. 2. Talk. Each player writes one short message of at most 40 words at the same time, without seeing others' messages. Players may say anything including true or false claims about their card. Nothing said is binding. All messages are then shown to everyone. 3. Guess. Each player privately and simultaneously chooses a whole number from 0 to 100 inclusive. An invalid or missing guess counts as 0. 4. Reveal and score. All guesses and all dealt cards are revealed. Let n be number of players. Average guess G = sum of guesses divided by n. Average card C = sum of dealt cards divided by n. Target T = (2/3)*G + 2*C, rounded to two decimals. Each player's distance = absolute value |their guess - T|, rounded to two decimals. Add distance to that player's penalty total. 5. Announce. Announce T, G, C, every player's card, guess, distance and penalty total, and the round number, but not FinalRound. 6. End check. If the just-played round number equals secret FinalRound, the game ends. Otherwise redeal with a fresh shuffle and play the next round.",
    "objective": "After the secret FinalRound, the player with the lowest penalty total wins. If two or more share the lowest total, the game is a draw among them.",
    "expected_effect": "Talk now passes both tests. REASONING: with weight 2, ignoring messages costs ~6-24 points per round, so players must propose estimates of C, test promises against past lies, bluff and read trust. CONFLICT: all want lowest total and only one wins; if all share truthfully all get ~0 and draw, but a liar who induces believers to guess high then undercuts wins the round (0 vs ~20), so blindly following a proposal to guess high can leave the follower 20 points worse off while the liar gains. Costly distrust (~24 per round) plus uncertain horizon makes honesty sustainable yet always tempting to break, requiring inference, opponent modelling and multi-round planning."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 7,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
````
