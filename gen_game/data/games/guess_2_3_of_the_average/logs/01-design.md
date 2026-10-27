# 01 design

- time: 2026-10-27T21:15:28+00:00 (66.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 441e1a6fc57b8669, reply sha256 518e848b0eea1e96

## Sent

````
Original game: Guess 2/3 of the average
Players in the original: 2 to 100

Original rules:
Each player privately chooses a real number between 0 and 100 inclusive. All choices are revealed at the same time. Compute the arithmetic mean of all chosen numbers, then multiply by 2/3 to get the target number. The player whose chosen number is closest to the target wins. If several players are equally close, they tie for the win. The game is played once, though it can be repeated to study learning.
````

## Reply

````
```json
{
  "original_summary": "Each player secretly picks a number from 0 to 100. The player closest to two-thirds of the average of all picks wins, and players who are equally close tie. It is a one-shot test of how many steps of 'what will the others think' each player goes through.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "With 2 players the lower number is always closer to 2/3 of the mean, so 'always pick 0' can never lose: at worst it draws. With many players the only equilibrium is everyone picking 0. Strong model players will all compute it and pick 0, so every game becomes a mass tie."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "There is no luck, but skill only shows when opponents are not fully rational. Among equally rational players every outcome is a tie. Being 'one level deeper' than the field can also overshoot and lose, so a single round is noisy."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "The solution is known: iterated elimination of dominated choices reaches 0. Once a player knows this there is little left to improve except guessing how irrational the others are."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "The only thing to infer is the opponents' depth of reasoning. Nothing is hidden about the world, and one-shot play allows no learning across rounds."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The target and the distances are pure arithmetic on the revealed numbers."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "It is one simultaneous numeric choice, text-only, with an arithmetic winner. It is very short, which is fine to extend."
    }
  ],
  "problems": [
    "P1: In the 2-player game 'always pick the lowest number (0)' cannot lose: it only wins or draws.",
    "P2: The unique equilibrium of 0 is common knowledge, so rational players all tie and nothing separates them.",
    "P3: Nothing is hidden except opponents' reasoning depth, so there is little to infer.",
    "P4: A single round makes the result noisy and gives no room to model opponents over time or to learn.",
    "P5: The winner-takes-all closest rule with real numbers is fine for one shot, but it gives no graded measure of how good a guess was."
  ],
  "changes": [
    {
      "what": "Add a private card. Each round every player is dealt one card from a shuffled deck numbered 0 to 30, seen only by them. The target becomes 2/3 of the average guess PLUS the average of all dealt cards.",
      "why": "The target now depends on information no one fully has. Each player must estimate the others' cards from their own card, and also predict how the others will weigh their cards and the 2/3 shrink. The answer is no longer a common-knowledge 0.",
      "fixes": "P2, P3"
    },
    {
      "what": "Require at least 3 players (3 to 6). The card term also means the lower guess no longer automatically wins.",
      "why": "This removes the 2-player 'lowest always wins' collapse. With a card average typically around 15, a guess of 0 is far from the target.",
      "fixes": "P1"
    },
    {
      "what": "Play 10 rounds. After each round reveal all cards, guesses, the target and distances. The winner has the lowest total distance over all rounds.",
      "why": "Graded scoring rewards being close, not just closest. Repetition lets players learn each opponent's habits. Ten deals average out who happened to hold a typical card.",
      "fixes": "P4, P5"
    },
    {
      "what": "Add a simultaneous talk phase before guessing. Everyone writes one short message at once, the messages are shown, then everyone guesses. Cards are revealed at the end of the round, so lies about cards are exposed afterwards.",
      "why": "A player gains by making the others misjudge the card average, so claims are bluffs to be read. Because the truth comes out each round, reputation for honesty becomes something to track and exploit across rounds.",
      "fixes": "P3, P4"
    }
  ],
  "keeps": [
    "Secret simultaneous number picks from 0 to 100.",
    "The target is 2/3 of the average of everyone's picks, so the 'guess what others guess' regress remains the core.",
    "Being closest to the target is what counts.",
    "Arithmetic, judge-free resolution."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The beauty-contest regress is a good opponent-modelling core. Adding a private signal, repetition and graded scoring removes the collapse to 0 and the 2-player dominance while staying well within the limits."
  },
  "variation": {
    "name": "Hidden-Card Beauty Contest",
    "summary": "Over 10 rounds, players guess 2/3 of the average guess plus the average of privately dealt cards. They talk, bluff about their cards, and try to stay closest to the target on aggregate.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 5
    },
    "rules": "Setup: 3 to 6 players. Each player starts with a penalty total of 0. The game lasts 10 rounds. The deck consists of 31 cards numbered 0, 1, 2, ..., 30.\n\nEach round:\n1. Deal. Shuffle all 31 cards and deal one card face down to each player. Each player sees only their own card. The undealt cards are not used this round.\n2. Talk. Every player writes one short message (at most 40 words) at the same time, without seeing the others' messages. Players may say anything, including true or false claims about their card. Nothing said is binding. All messages are then shown to everyone.\n3. Guess. Every player privately and simultaneously chooses a whole number from 0 to 100 inclusive. An invalid or missing guess counts as 0.\n4. Reveal and score. All guesses and all dealt cards are revealed.\n   - Average guess G = sum of guesses divided by the number of players.\n   - Average card C = sum of dealt cards divided by the number of players.\n   - Target T = (2/3) x G + C.\n   - Each player's distance this round = |their guess - T|, rounded to two decimals.\n   - Each player's distance is added to their penalty total.\n5. Announce. Announce the target and every player's card, guess, distance and penalty total.\n6. If 10 rounds have been played, the game ends. Otherwise start the next round.",
    "objective": "After round 10, the player with the lowest penalty total wins. If two or more players share the lowest total, the game is a draw among them.",
    "expected_effect": "The target is no longer the common-knowledge 0. A player must combine their own card, an estimate of the unseen cards (about 15 each on average, slightly adjusted by knowing one card is theirs), and a forecast of how far the others shrink their guesses.\n\nSimple policies lose to thinkers:\n- Always 0 misses by roughly the card average, about 15 per round.\n- Always 100 misses by about 50.\n- Always guessing your own card ignores the 2/3 x G term.\n- If everyone plays 0, anyone who deviates toward the card estimate wins, so all-0 is unstable.\n\nTalk passes both tests.\n- Reasoning: players make claims about their cards and must judge whom to believe, using the end-of-round reveals that expose past lies.\n- Conflict: only one player can win, and each gains by making the others misjudge the card average. A player who simply believes the claims can be steered away from the target while the liar, who knows the truth, lands close to it.\n\nLuck in the deal changes only how much each player knows, which is symmetric in expectation, and 10 rounds of graded scoring let skill dominate. Repetition rewards modelling each opponent's depth of reasoning and honesty."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 2,
    "attributes": 11,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 10
  }
}
```
````
