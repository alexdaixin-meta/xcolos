# Variation: Put: Twelve Hands

A two-player bluffing game over 12 hands of three cards. Players may call Put to raise a hand's stake from 1 to 3. A Put can be seen or folded, and a seen Put is won only if the putter takes strictly more tricks. Card play is a simultaneous commitment to an order of the three cards.

Players: 2 to 2, best with 2

## Review of the original

Put is an old two-to-four player trick-taking and bluffing game played with three cards each, in the unusual rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with no obligation to follow suit. Winning two of three tricks scores 1 point, and a player may call 'Put' to stake the whole game, which the opponent either sees or folds.

- **non_degenerate**: bad. In the original, a Put that is seen stakes the whole match, so the match swings on one bluff. In the previous variation, always taking the first option (raise or see) won 54 of 60 matches from seat 1 and 53 of 60 from seat 2. Aggression was nearly free: folds paid the raiser, tied hands paid nobody, and seeing a raise cost little more than folding.
- **skill_sensitive**: weak. Whether to call Put or fold is a real decision. But with whole-game stakes, one seen Put with a lucky deal decides everything. In the previous variation, a mindless line beat varied play about 90% of the time, so skill was not what decided matches.
- **headroom**: weak. Bluffing, reading a Put and choosing card order give real depth. However, with the payoffs tilted towards aggression, the best play collapsed to 'always push', leaving nothing to improve on.
- **reasoning_dependent**: good. Hands are hidden. A Put may be a bluff, and the opponent must infer hand strength from the betting. Card play without following suit becomes a guessing contest over which card the opponent commits to each trick.
- **verifiable**: good. Tricks are settled by comparing ranks, and scores follow from trick counts and the betting outcome. Everything is arithmetic.
- **fits_platform**: weak. The game is turn-based and text-only. Playing three tricks with alternating leads needs six card-play choices per hand plus betting, which exceeds 4 choice steps per round. The match length ('first to 5 or 7') is also open-ended.

## Problems

- Always-aggressive play dominates: the previous variation's 'first option' policy (raise or see) won about 90% of decided matches from either seat.
- Seeing a Put with a weak hand cost little more than folding, so folding was rarely right and bluff-reading did not matter.
- Tied hands paid nobody, so a Put that ended level was free for the putter, which made aggression costless.
- Whole-game stakes on one seen Put turn a match into a single coin flip on the deal.
- Three tricks with alternating leads need too many choice steps per round for the engine.
- Little information beyond one's own three cards: nothing about the opponent's hand to reason from except the betting.
- Open-ended match length ('first to 5 or 7') does not fit a fixed, short game and lets one hand end it.

## Changes

- The putter must win strictly MORE tricks than the opponent to collect a seen Put. If tricks are equal or the opponent wins more, the opponent collects instead. The stake is 3 points, not the whole game. (fixes: Tied hands paid nobody, so a Put that ended level was free for the putter, which made aggression costless.): A seen Put with an average hand now loses slightly on average (equal-trick hands go against the putter), so putting must be backed by strength or by a credible bluff. The 3-point stake keeps a seen Put big without deciding the match.
- A fold gives the putter only 1 point, while a seen Put is worth 3 either way. (fixes: Seeing a Put with a weak hand cost little more than folding, so folding was rarely right and bluff-reading did not matter.): Folding becomes the cheap exit for genuinely weak hands, and seeing a strong Put costs 3. The choice between seeing and folding now depends on reading the opponent's hand.
- Options are listed with the cautious choice first (Check before Put) and See before Fold. A seat's 'always first' line is now 'never put, always see', and 'always last' is 'always put, always fold'. (fixes: Always-aggressive play dominates: the previous variation's 'first option' policy (raise or see) won about 90% of decided matches from either seat.): Each line is now exploitable. 'Never put, always see' loses 3 every time a thoughtful opponent puts with a strong hand. 'Always put, always fold' gets seen by strong hands and folds away 1 point every time the opponent puts. Neither can dominate.
- After betting, both players secretly and simultaneously commit the order in which they will play their three cards. Trick 1 compares the first cards, trick 2 the second, trick 3 the third. (fixes: Three tricks with alternating leads need too many choice steps per round for the engine.): This keeps 'play any card, no need to follow' and the tie rule while fitting into one choice step. Ordering becomes a guessing contest: whether to sacrifice a low card against the opponent's expected high card, or where to place a known strong card.
- The first card dealt to each player is shown face up to both. The other two stay hidden. (fixes: Little information beyond one's own three cards: nothing about the opponent's hand to reason from except the betting.): This gives real information to infer from in both betting and ordering, at no extra choice cost. Players can judge how credible a Put is and plan around a known card.
- The match is exactly 12 hands, with the leader alternating so each seat leads 6. The higher total wins, and equal totals are a draw. (fixes: Open-ended match length ('first to 5 or 7') does not fit a fixed, short game and lets one hand end it.): Fixed and short, seat-balanced, and no single hand decides the match. A trailing player must decide when to take risks in the late hands.
- Stakes are capped at 3 per hand instead of the whole game. (fixes: Whole-game stakes on one seen Put turn a match into a single coin flip on the deal.): Over 12 hands, the betting and ordering decisions accumulate. A single lucky deal can no longer end the match.

## Kept from the original

- The deck and the unusual rank order 3-2-A-K-Q-J-10-9-8-7-6-5-4, with suits irrelevant.
- Three cards each and three tricks, with no requirement to follow.
- Equal ranks tie the trick, and it belongs to no one.
- Winning more tricks scores 1 point in an ordinary hand.
- The 'Put' call, answered by 'I see it' (See) or by folding, which concedes to the putter.
- Bluffing and reading bluffs as the heart of the game.

## The variation's rules

CARDS. Use a standard 52-card deck. Suits do not matter. Ranks from highest to lowest are: 3, 2, A, K, Q, J, 10, 9, 8, 7, 6, 5, 4.

MATCH. The match is exactly 12 hands. Both players start at 0 points. Seat 1 is the leader in hands 1, 3, 5, 7, 9 and 11. Seat 2 is the leader in hands 2, 4, 6, 8, 10 and 12. The other player is the responder.

EACH HAND:
1. Deal. Shuffle the full deck and deal 3 cards to each player. Each player's first dealt card is placed face up and both players see it. Each player's other two cards are private. Each player's hand is listed in the order dealt.
2. Leader's call. The leader chooses one of two options: Check, or Put.
3. Responder's action. If the leader chose Put, the responder chooses See ('I see it') or Fold. If the leader chose Check, the responder chooses Check or Put.
4. Leader's reply. This happens only if the leader checked and the responder put. The leader then chooses See or Fold.
5. Fold. If either player folded, the hand ends at once. The player who put scores 1 point, the folder scores 0, and no cards are played.
6. Card order. Otherwise, both players secretly and at the same moment choose an order for their three cards, naming which of their cards they will play first, second and third.
7. Tricks. Trick 1 compares both players' first cards, trick 2 their second cards, and trick 3 their third cards. The higher-ranked card wins the trick. Equal ranks tie the trick, and it counts for no one. Count each player's tricks won.
8. Scoring when nobody put (both checked). The player with more tricks scores 1 point. If tricks are equal, nobody scores.
9. Scoring when a Put was seen. The player who put scores 3 points if they won strictly more tricks than the opponent. Otherwise (equal tricks, or the opponent won more), the opponent scores 3 points.
10. Results. Reveal all cards, both orders, the trick results and the scores.

Only one Put can be made per hand. There is no re-raise. Talk is not part of the game.

Objective: After hand 12, the player with the higher total score wins. If the totals are equal, the match is a draw.

Expected effect: Putting is no longer free. A seen Put with an average hand loses slightly on average, because equal-trick hands go to the non-putter. A seen Put with a weak hand loses 3, while folding loses only 1. Good play therefore means putting with strong hands and some well-chosen bluffs, seeing when the face-up card and the betting suggest a bluff, and folding marginal hands. 'Always check, always see' bleeds 3 points to every value Put. 'Always put, always fold' gets called by strong hands and concedes 1 every time the opponent puts first. Against random play, each simple policy should come out roughly even or only mildly ahead, rather than the previous 90%. The simultaneous card order adds a reading contest on every played hand: whether to sacrifice a low card against the expected high card, or where to place the visible card the opponent will plan around. Fixed alternation of the lead keeps the seats balanced. Twelve hands with stakes of 1 or 3 let skill accumulate over the luck of the deal. No talk is used: with two players and a zero-sum score, there is nothing to negotiate.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 15 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
