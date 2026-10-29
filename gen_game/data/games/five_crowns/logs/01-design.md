# 01 design

- time: 2026-10-28T06:42:39+00:00 (36.4s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 052e408137c69a41, reply sha256 f10e3b72671579b7

## Sent

````
Original game: Five Crowns
Players in the original: 1 to 7

Original rules:
Two 58-card decks are combined. Each has 5 suits (stars, hearts, clubs, spades, diamonds) with 3-K plus 3 Jokers. Jokers are always wild. Each round r, r+2 cards are dealt: round 1 =3 cards and 3s are wild, round 2=4 cards and 4s wild, up to round 11=13 cards and Kings wild. Remaining cards form draw pile, top card starts discard. On turn, player draws top of draw OR top of discard, then tries to form entire hand into books (3+ same rank) and/or runs (3+ consecutive same suit) using wilds anywhere. Hand stays hidden until going out. To go out, on your turn after drawing, meld all cards except one discard face up. Then each other player gets one final turn to meld what they can. Unmelded cards score face value, Jack 11, Queen 12, King 13, current wild 20, Joker 50. Lowest total after 11 rounds wins.
````

## Reply

````
```json
{
  "original_summary": "Five Crowns is a rummy game for 1 to 7 players. It runs over 11 hands of growing size, from 3 to 13 cards, dealt from a 116-card five-suit deck, and the wild rank rotates each hand. Players draw and discard to arrange their whole hidden hand into books and runs, then go out, and the lowest total of unmelded penalty points wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always draw from the deck' or 'always take the discard' each lose to a player who picks by need. Never going out leaves a player exposed to large penalties when someone else goes out. No seat has a fixed edge beyond rotating deal order."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Skill matters over 11 hands: reading opponents' discard pickups, timing when to go out, and dumping high cards early. In any single hand, however, the deal and draws dominate. A 3-card hand with two wilds goes out at once whatever anyone does. Only the full 11-hand length evens out the luck."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still form some melds. Strong players keep improving through probabilistic draw choices, inferring opponents' hands from what they pick up, and deciding when to go out versus keep building."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players infer opponents' needs from their discard-pile pickups and discards, estimate how close opponents are to going out, and weigh the risk of holding high cards."
    },
    {
      "criterion": "verifiable",
      "verdict": "weak",
      "evidence": "The penalty sum is arithmetic. But deciding whether a 13-card hand with several wilds splits fully into books and runs, and finding the lowest possible unmelded remainder, is a combinatorial search. The engine has no operation for it. A referee could rule on whether a declared meld is valid, but every player's score depends on the optimal arrangement, which pushes scoring onto a judge."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Turn-based and text-only, but far outside the limits. A full game is roughly 11 hands of many orbits each, at least 100 to 300 individual turns against a 40-round cap. Each turn needs a draw-source choice, a random draw and a discard choice, and going out triggers a final turn for every other player, so an orbit cannot fit in 4 choice steps. The hidden state (7 hands of up to 13 cards, plus the draw pile order out of 116 cards) far exceeds 3 hidden elements and 20 attributes."
    }
  ],
  "problems": [
    "The game's length is its identity: 11 hands that grow from 3 to 13 cards with a rotating wild. That needs hundreds of turns, far beyond the 40-round limit.",
    "Each player turn is a chain of draw choice, random draw, discard choice and going-out declaration, plus a final turn for every other player after someone goes out. A table orbit exceeds 4 choice steps per round.",
    "The hidden state is a large shared deck plus up to 7 hidden hands of up to 13 cards. That exceeds the attribute and hidden-element limits.",
    "Scoring needs the best split of a hand into books and runs with wilds. The engine cannot compute that search arithmetically, so scores would depend on a judge.",
    "Luck evens out only over the full 11 hands. Any version short enough to build (two or three small hands) is dominated by the deal."
  ],
  "changes": [
    {
      "what": "Considered: shrink to 2-3 players, two hands of 4-5 cards, a 3-suit deck, and one engine round per individual player turn.",
      "why": "It would fit roughly within 40 rounds and 4 choice steps. However, with only two short hands, the deal decides the winner, and the escalating 11-hand structure with a rotating wild disappears. What is left is a generic mini-rummy, not Five Crowns.",
      "fixes": "The game's length is its identity: 11 hands that grow from 3 to 13 cards with a rotating wild. That needs hundreds of turns, far beyond the 40-round limit."
    },
    {
      "what": "Considered: players declare their own melds and unmelded cards; a referee checks meld validity, and the penalty is the arithmetic sum of the declared unmelded cards.",
      "why": "This moves the combinatorial search onto the players. Even so, it needs per-card hand tracking with many attributes and a referee ruling every turn, while the luck problem remains.",
      "fixes": "Scoring needs the best split of a hand into books and runs with wilds. The engine cannot compute that search arithmetically, so scores would depend on a judge."
    }
  ],
  "keeps": [
    "No variation is proposed. A faithful adaptation would need to keep the escalating hand sizes, the rotating wild rank, hidden hands, the draw-from-deck-or-discard choice, the go-out-then-final-turn rule, and lowest-penalty scoring. None of these fits the limits together."
  ],
  "recommendation": {
    "decision": "drop",
    "kind": "too_complex",
    "reason": "Five Crowns' essence is a long escalating sequence of hands (3 to 13 cards, rotating wilds) over a 116-card deck, with a combinatorial meld search in every hand. That needs hundreds of turns, large per-card hidden state and multi-step turns far beyond 40 rounds, 4 choices per round and 3 hidden elements. Any cut short enough to build becomes a luck-dominated mini-rummy rather than Five Crowns."
  }
}
```
````
