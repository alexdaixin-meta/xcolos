# Recommended drop: too complex

Five Crowns' essence is a long escalating sequence of hands (3 to 13 cards, rotating wilds) over a 116-card deck, with a combinatorial meld search in every hand. That needs hundreds of turns, large per-card hidden state and multi-step turns far beyond 40 rounds, 4 choices per round and 3 hidden elements. Any cut short enough to build becomes a luck-dominated mini-rummy rather than Five Crowns.

## Review of the original

Five Crowns is a rummy game for 1 to 7 players. It runs over 11 hands of growing size, from 3 to 13 cards, dealt from a 116-card five-suit deck, and the wild rank rotates each hand. Players draw and discard to arrange their whole hidden hand into books and runs, then go out, and the lowest total of unmelded penalty points wins.

- **non_degenerate**: good. No simple policy wins. 'Always draw from the deck' or 'always take the discard' each lose to a player who picks by need. Never going out leaves a player exposed to large penalties when someone else goes out. No seat has a fixed edge beyond rotating deal order.
- **skill_sensitive**: weak. Skill matters over 11 hands: reading opponents' discard pickups, timing when to go out, and dumping high cards early. In any single hand, however, the deal and draws dominate. A 3-card hand with two wilds goes out at once whatever anyone does. Only the full 11-hand length evens out the luck.
- **headroom**: good. Weak players still form some melds. Strong players keep improving through probabilistic draw choices, inferring opponents' hands from what they pick up, and deciding when to go out versus keep building.
- **reasoning_dependent**: good. Hands are hidden. Players infer opponents' needs from their discard-pile pickups and discards, estimate how close opponents are to going out, and weigh the risk of holding high cards.
- **verifiable**: weak. The penalty sum is arithmetic. But deciding whether a 13-card hand with several wilds splits fully into books and runs, and finding the lowest possible unmelded remainder, is a combinatorial search. The engine has no operation for it. A referee could rule on whether a declared meld is valid, but every player's score depends on the optimal arrangement, which pushes scoring onto a judge.
- **fits_platform**: bad. Turn-based and text-only, but far outside the limits. A full game is roughly 11 hands of many orbits each, at least 100 to 300 individual turns against a 40-round cap. Each turn needs a draw-source choice, a random draw and a discard choice, and going out triggers a final turn for every other player, so an orbit cannot fit in 4 choice steps. The hidden state (7 hands of up to 13 cards, plus the draw pile order out of 116 cards) far exceeds 3 hidden elements and 20 attributes.

## Problems

- The game's length is its identity: 11 hands that grow from 3 to 13 cards with a rotating wild. That needs hundreds of turns, far beyond the 40-round limit.
- Each player turn is a chain of draw choice, random draw, discard choice and going-out declaration, plus a final turn for every other player after someone goes out. A table orbit exceeds 4 choice steps per round.
- The hidden state is a large shared deck plus up to 7 hidden hands of up to 13 cards. That exceeds the attribute and hidden-element limits.
- Scoring needs the best split of a hand into books and runs with wilds. The engine cannot compute that search arithmetically, so scores would depend on a judge.
- Luck evens out only over the full 11 hands. Any version short enough to build (two or three small hands) is dominated by the deal.
