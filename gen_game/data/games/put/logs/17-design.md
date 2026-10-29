# 17 design

- time: 2026-10-28T06:32:05+00:00 (118.1s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c81d2bf03b0f8e8d, reply sha256 1a1f60bbc05d30cb

## Sent

````
Original game: Put
Players in the original: 2 to 4

Original rules:
Use 52 cards ranking 3-2-A-K-Q-J-10-9-8-7-6-5-4, no trumps. Players ante to game score, 5 or 7 points to win match. Deal 3 cards each singly. Non-dealer leads. Any card may be played, no need to follow. Higher rank wins trick; equal ranks tie the trick and it belongs to none. Winner leads next, same leader after a tie. Winning 2 of 3 tricks scores 1 point, trick-and-tie scores none. Before a trick, holder may say "Put" to play for the whole game. If opponent folds, putter scores 1. If opponent says "I see it", the hand is played and winner of most tricks wins the whole game (5 or 7) not just 1. A player may also fold on seeing cards, conceding 1. Deal alternates.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
Rebalance the betting so that never folding and always raising is not a dominant mindless line.
- Make the cost of seeing a raise with a weak hand meaningfully larger than the cost of folding. For example, a player who SEEs a PUT or RE-PUT and then loses on tricks pays a penalty, or the fold payouts shrink relative to the see stakes.
- Reduce how often hands end with nobody scoring, since that makes aggression free. A tied hand could go to the player with the higher face-up card, or to the side that did not raise.
- Add more real information to reason about, such as more private cards or the face-up card affecting the stakes, so that playing well beats an indiscriminate policy.
- Make sure no single fixed response is best regardless of the cards. Then confirm that seats remain balanced.
the game was built and behaves as specified, but evaluation found design flaws:
- always taking the first option as seat 1 wins 90% of decided matches against random seats
- always taking the first option as seat 2 wins 88% of decided matches against random seats
- against random seats the results were {'seat 2': 33, 'seat 1': 27}
- a thoughtless policy `first@seat1`: won 54, lost 6, drew 0
- a thoughtless policy `first@seat2`: won 53, lost 7, drew 0
- a thoughtless policy `last@seat1`: won 25, lost 35, drew 0
- a thoughtless policy `last@seat2`: won 34, lost 26, drew 0

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Put is an old two-to-four player trick-taking and bluffing game played with three cards each, in the unusual rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with no obligation to follow suit. Winning two of three tricks scores 1 point, and a player may call 'Put' to stake the whole game, which the opponent either sees or folds.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "bad",
      "evidence": "In the original, a Put that is seen stakes the whole match, so the match swings on one bluff. In the previous variation, always taking the first option (raise or see) won 54 of 60 matches from seat 1 and 53 of 60 from seat 2. Aggression was nearly free: folds paid the raiser, tied hands paid nobody, and seeing a raise cost little more than folding."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Whether to call Put or fold is a real decision. But with whole-game stakes, one seen Put with a lucky deal decides everything. In the previous variation, a mindless line beat varied play about 90% of the time, so skill was not what decided matches."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Bluffing, reading a Put and choosing card order give real depth. However, with the payoffs tilted towards aggression, the best play collapsed to 'always push', leaving nothing to improve on."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. A Put may be a bluff, and the opponent must infer hand strength from the betting. Card play without following suit becomes a guessing contest over which card the opponent commits to each trick."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Tricks are settled by comparing ranks, and scores follow from trick counts and the betting outcome. Everything is arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The game is turn-based and text-only. Playing three tricks with alternating leads needs six card-play choices per hand plus betting, which exceeds 4 choice steps per round. The match length ('first to 5 or 7') is also open-ended."
    }
  ],
  "problems": [
    "Always-aggressive play dominates: the previous variation's 'first option' policy (raise or see) won about 90% of decided matches from either seat.",
    "Seeing a Put with a weak hand cost little more than folding, so folding was rarely right and bluff-reading did not matter.",
    "Tied hands paid nobody, so a Put that ended level was free for the putter, which made aggression costless.",
    "Whole-game stakes on one seen Put turn a match into a single coin flip on the deal.",
    "Three tricks with alternating leads need too many choice steps per round for the engine.",
    "Little information beyond one's own three cards: nothing about the opponent's hand to reason from except the betting.",
    "Open-ended match length ('first to 5 or 7') does not fit a fixed, short game and lets one hand end it."
  ],
  "changes": [
    {
      "what": "The putter must win strictly MORE tricks than the opponent to collect a seen Put. If tricks are equal or the opponent wins more, the opponent collects instead. The stake is 3 points, not the whole game.",
      "why": "A seen Put with an average hand now loses slightly on average (equal-trick hands go against the putter), so putting must be backed by strength or by a credible bluff. The 3-point stake keeps a seen Put big without deciding the match.",
      "fixes": "Tied hands paid nobody, so a Put that ended level was free for the putter, which made aggression costless."
    },
    {
      "what": "A fold gives the putter only 1 point, while a seen Put is worth 3 either way.",
      "why": "Folding becomes the cheap exit for genuinely weak hands, and seeing a strong Put costs 3. The choice between seeing and folding now depends on reading the opponent's hand.",
      "fixes": "Seeing a Put with a weak hand cost little more than folding, so folding was rarely right and bluff-reading did not matter."
    },
    {
      "what": "Options are listed with the cautious choice first (Check before Put) and See before Fold. A seat's 'always first' line is now 'never put, always see', and 'always last' is 'always put, always fold'.",
      "why": "Each line is now exploitable. 'Never put, always see' loses 3 every time a thoughtful opponent puts with a strong hand. 'Always put, always fold' gets seen by strong hands and folds away 1 point every time the opponent puts. Neither can dominate.",
      "fixes": "Always-aggressive play dominates: the previous variation's 'first option' policy (raise or see) won about 90% of decided matches from either seat."
    },
    {
      "what": "After betting, both players secretly and simultaneously commit the order in which they will play their three cards. Trick 1 compares the first cards, trick 2 the second, trick 3 the third.",
      "why": "This keeps 'play any card, no need to follow' and the tie rule while fitting into one choice step. Ordering becomes a guessing contest: whether to sacrifice a low card against the opponent's expected high card, or where to place a known strong card.",
      "fixes": "Three tricks with alternating leads need too many choice steps per round for the engine."
    },
    {
      "what": "The first card dealt to each player is shown face up to both. The other two stay hidden.",
      "why": "This gives real information to infer from in both betting and ordering, at no extra choice cost. Players can judge how credible a Put is and plan around a known card.",
      "fixes": "Little information beyond one's own three cards: nothing about the opponent's hand to reason from except the betting."
    },
    {
      "what": "The match is exactly 12 hands, with the leader alternating so each seat leads 6. The higher total wins, and equal totals are a draw.",
      "why": "Fixed and short, seat-balanced, and no single hand decides the match. A trailing player must decide when to take risks in the late hands.",
      "fixes": "Open-ended match length ('first to 5 or 7') does not fit a fixed, short game and lets one hand end it."
    },
    {
      "what": "Stakes are capped at 3 per hand instead of the whole game.",
      "why": "Over 12 hands, the betting and ordering decisions accumulate. A single lucky deal can no longer end the match.",
      "fixes": "Whole-game stakes on one seen Put turn a match into a single coin flip on the deal."
    }
  ],
  "keeps": [
    "The deck and the unusual rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with suits irrelevant.",
    "Three cards each and three tricks, with no requirement to follow.",
    "Equal ranks tie the trick, and it belongs to no one.",
    "Winning more tricks scores 1 point in an ordinary hand.",
    "The 'Put' call, answered by 'I see it' (See) or by folding, which concedes to the putter.",
    "Bluffing and reading bluffs as the heart of the game."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The bluff-and-call core is strong strategic material. It failed only because the payoffs made aggression free and the trick play did not fit the step limits, and both are fixable with stakes, a tie rule and simultaneous card ordering."
  },
  "variation": {
    "name": "Put: Twelve Hands",
    "summary": "A two-player bluffing game over 12 hands of three cards. Players may call Put to raise a hand's stake from 1 to 3. A Put can be seen or folded, and a seen Put is won only if the putter takes strictly more tricks. Card play is a simultaneous commitment to an order of the three cards.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "CARDS. Use a standard 52-card deck. Suits do not matter. Ranks from highest to lowest are: 3, 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4.\n\nMATCH. The match is exactly 12 hands. Both players start at 0 points. Seat 1 is the leader in hands 1, 3, 5, 7, 9 and 11. Seat 2 is the leader in hands 2, 4, 6, 8, 10 and 12. The other player is the responder.\n\nEACH HAND:\n1. Deal. Shuffle the full deck and deal 3 cards to each player. Each player's first dealt card is placed face up and both players see it. Each player's other two cards are private. Each player's hand is listed in the order dealt.\n2. Leader's call. The leader chooses one of two options: Check, or Put.\n3. Responder's action. If the leader chose Put, the responder chooses See ('I see it') or Fold. If the leader chose Check, the responder chooses Check or Put.\n4. Leader's reply. This happens only if the leader checked and the responder put. The leader then chooses See or Fold.\n5. Fold. If either player folded, the hand ends at once. The player who put scores 1 point, the folder scores 0, and no cards are played.\n6. Card order. Otherwise, both players secretly and at the same moment choose an order for their three cards, naming which of their cards they will play first, second and third.\n7. Tricks. Trick 1 compares both players' first cards, trick 2 their second cards, and trick 3 their third cards. The higher-ranked card wins the trick. Equal ranks tie the trick, and it counts for no one. Count each player's tricks won.\n8. Scoring when nobody put (both checked). The player with more tricks scores 1 point. If tricks are equal, nobody scores.\n9. Scoring when a Put was seen. The player who put scores 3 points if they won strictly more tricks than the opponent. Otherwise (equal tricks, or the opponent won more), the opponent scores 3 points.\n10. Results. Reveal all cards, both orders, the trick results and the scores.\n\nOnly one Put can be made per hand. There is no re-raise. Talk is not part of the game.",
    "objective": "After hand 12, the player with the higher total score wins. If the totals are equal, the match is a draw.",
    "expected_effect": "Putting is no longer free. A seen Put with an average hand loses slightly on average, because equal-trick hands go to the non-putter. A seen Put with a weak hand loses 3, while folding loses only 1. Good play therefore means putting with strong hands and some well-chosen bluffs, seeing when the face-up card and the betting suggest a bluff, and folding marginal hands. 'Always check, always see' bleeds 3 points to every value Put. 'Always put, always fold' gets called by strong hands and concedes 1 every time the opponent puts first. Against random play, each simple policy should come out roughly even or only mildly ahead, rather than the previous 90%. The simultaneous card order adds a reading contest on every played hand: whether to sacrifice a low card against the expected high card, or where to place the visible card the opponent will plan around. Fixed alternation of the lead keeps the seats balanced. Twelve hands with stakes of 1 or 3 let skill accumulate over the luck of the deal. No talk is used: with two players and a zero-sum score, there is nothing to negotiate."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
