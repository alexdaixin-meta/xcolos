# 01 design

- time: 2026-10-27T20:41:52+00:00 (71.0s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 2600287fd1efd708, reply sha256 067c979e0c344e84

## Sent

````
Original game: Skull King
Players in the original: 2 to 8

Original rules:
Play 10 hands. The deck has 4 colored suits 1-14, 5 Pirates, 5 Escapes, 2 Mermaids, 1 Scary Mary, 1 Skull King. In hand i each player is dealt i cards. Players simultaneously bid how many tricks they will win. Tricks are played clockwise; must follow lead suit if possible, but any special card may be played at any time. Highest card of lead suit wins unless trumped. Black is permanent trump over colors. Mermaid beats all colors and black. Pirate beats mermaid and all colors/black. Skull King beats all except Mermaid, which beats Skull King. Scary Mary is declared as Pirate or Escape when played. Escape is 0, loses unless all Escape, then first wins. If first card is special, first colored card defines lead suit. Score: if bid equals tricks taken, gain 20 per trick, plus zero-bid gives hand-number*10, plus bonuses: 30 per Pirate captured by Skull King, 50 for Skull King captured by Mermaid. If bid fails, lose 10 per difference, or minus hand*10 for failed zero bid. Highest total after 10 hands wins.
````

## Reply

````
```json
{
  "original_summary": "Skull King is a 2-8 player trick-taking game played over 10 hands of growing size. In each hand players bid simultaneously on exactly how many tricks they will win, then play tricks that include special cards (Pirates, Escapes, Mermaids, the Skull King). They score heavily for an exact bid and lose points for a miss.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No fixed bid survives. Always bidding 0 and dumping low cards fails whenever a player is forced to win a trick, which costs hand-number x 10 and up to 100 in hand 10. Always bidding high rarely comes in exact. The deal and lead rotate, so there is little seat edge. One weakness is the zero bid: it pays hand x 10 regardless of hand size, so it is lopsided in late hands."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Reading your hand, adjusting play to land exactly on your bid, and playing to make opponents miss theirs all separate strong players from weak ones over 10 hands. The deal matters for bonuses (who holds the Skull King or a Mermaid), but the exact-bid rule rewards judgement whatever the cards."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting, inference from public bids, deliberately setting opponents, and endgame risk-taking when trailing give a deep skill ceiling. A beginner still scores by bidding conservatively."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden and bids are public signals. Players must infer what others hold from their bids and earlier plays, and plan the order of their own cards across a hand."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners and scores follow mechanically from the cards played and the bids."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and arithmetic, but too large to build. Hands grow to 10 cards, a full game runs 55 tricks per player, the deck has 70 cards, up to 8 players each act per trick (more than 4 choice steps), and Scary Mary adds a declaration choice. All of this must be compressed."
    }
  ],
  "problems": [
    "Too long and too large: 10 hands of growing size means 55 tricks, and with up to 8 players each trick needs more than the 4 choice steps allowed per round.",
    "The 70-card deck with many special cards inflates the dealing and resolution steps beyond what the engine builds reliably.",
    "Scary Mary needs an extra declaration choice when played, which adds a choice step for little strategic value.",
    "The zero-bid payoff (hand number x 10) grows with hand number rather than with difficulty, which distorts late-hand bidding.",
    "With growing hand sizes and an uneven count of hands per seat, the first-leader seat is not equalised."
  ],
  "changes": [
    {
      "what": "Fix the game at 3 players, every hand 3 cards, 9 hands, so each round of the engine is one trick (27 rounds).",
      "why": "One trick per round needs at most 4 choice steps (one bid poll plus 3 plays). 27 rounds is within the 40 limit.",
      "fixes": "Too long and too large: 10 hands of growing size means 55 tricks, and with up to 8 players each trick needs more than the 4 choice steps allowed per round."
    },
    {
      "what": "Use a 25-card deck: Green 1-7, Yellow 1-7, Black 1-5, 2 Pirates, 2 Escapes, 1 Mermaid, 1 Skull King. Drop Scary Mary and the second Mermaid.",
      "why": "This keeps every type of interaction (following suit, black trump, escapes, the pirate/mermaid/king triangle) with a deck small enough to deal in one random draw. 9 of 25 cards are dealt, so the unseen remainder still creates uncertainty.",
      "fixes": "The 70-card deck with many special cards inflates the dealing and resolution steps beyond what the engine builds reliably."
    },
    {
      "what": "Remove Scary Mary entirely.",
      "why": "This removes the extra declaration choice.",
      "fixes": "Scary Mary needs an extra declaration choice when played, which adds a choice step for little strategic value."
    },
    {
      "what": "Flat bid scoring: an exact bid of k (k at least 1) scores 20k; an exact zero bid scores 20; a missed zero bid scores -20; any other miss scores -10 per trick of difference. Bonuses (+30 per Pirate captured by the Skull King, +40 for a Mermaid capturing the Skull King) count only if the bid was exact.",
      "why": "The zero bid is now worth the same as bid 1. It is chosen for weak hands, not as a late-game jackpot. All four bids are live options for a 3-card hand.",
      "fixes": "The zero-bid payoff (hand number x 10) grows with hand number rather than with difficulty, which distorts late-hand bidding."
    },
    {
      "what": "Rotate the first leader of each hand among the 3 seats. 9 hands means each seat leads first exactly 3 times.",
      "why": "This equalises any first-lead advantage.",
      "fixes": "With growing hand sizes and an uneven count of hands per seat, the first-leader seat is not equalised."
    },
    {
      "what": "The engine offers each player only their legal cards when they play.",
      "why": "This keeps the game playable without a judge and prevents rule-breaking moves.",
      "fixes": "Too long and too large: 10 hands of growing size means 55 tricks, and with up to 8 players each trick needs more than the 4 choice steps allowed per round."
    }
  ],
  "keeps": [
    "Simultaneous exact-trick bidding after seeing your hand, with big rewards for hitting the bid and penalties for missing it.",
    "Must-follow-suit trick play with Black as permanent trump over the colours.",
    "The special-card triangle: Pirate beats Mermaid, Skull King beats Pirate, Mermaid beats Skull King, and Escapes always lose.",
    "Capture bonuses for the Skull King taking Pirates and a Mermaid taking the Skull King.",
    "Several hands with a highest-total winner, in which setting opponents' bids matters as much as making your own."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of exact-bid trick-taking with hidden hands is strongly reasoning-dependent. It compresses into 3 players, 3-card hands and one trick per round within the limits."
  },
  "variation": {
    "name": "Skull King: Three-Card Raids",
    "summary": "A compact 3-player Skull King. Over 9 hands of 3 cards each, players simultaneously bid how many of the 3 tricks they will win. They then play tricks with suits, black trump, Escapes, Pirates, a Mermaid and the Skull King, scoring for exact bids and bonus captures.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "PLAYERS AND DECK. 3 players, seats 1, 2 and 3. The deck has 25 cards: Green 1-7 (7 cards), Yellow 1-7 (7 cards), Black 1-5 (5 cards), 2 Pirates, 2 Escapes, 1 Mermaid and 1 Skull King. Green, Yellow and Black are the suited cards. Pirates, Escapes, the Mermaid and the Skull King are special cards.\n\nSTRUCTURE. The game has 9 hands of 3 tricks each, so 27 rounds; each round is one trick. Each player's score starts at 0.\n\nSTART OF EACH HAND (first trick of the hand only). Shuffle all 25 cards and deal 3 to each player, face down. Each player sees only their own cards. The other 16 cards are set aside unseen. All players then bid at the same moment, each secretly choosing a whole number from 0 to 3: the number of tricks they will win this hand. All bids are then revealed to everyone. The first leader of hand h is seat ((h-1) mod 3) + 1, so hands 1, 4 and 7 are led by seat 1, hands 2, 5 and 8 by seat 2, and hands 3, 6 and 9 by seat 3.\n\nPLAYING A TRICK. The leader plays one card face up, then the next seat clockwise (1 to 2, 2 to 3, 3 to 1), then the third player.\n- Lead suit: the suit of the first suited card played in the trick. If special cards are played before any suited card, the lead suit is set by the first suited card that follows. If no suited card is played, there is no lead suit.\n- Following: once a lead suit exists, a player who holds a card of that suit must play either a card of that suit or a special card. A player with no card of that suit may play any card. Special cards may always be played.\n- The engine offers each player only the cards they may legally play.\n\nWINNING A TRICK. Check these in order:\n(1) If the trick contains both the Skull King and the Mermaid, the Mermaid wins.\n(2) Otherwise, if it contains the Skull King, the Skull King wins.\n(3) Otherwise, if it contains a Pirate, the first Pirate played wins.\n(4) Otherwise, if it contains the Mermaid, the Mermaid wins.\n(5) Otherwise, if it contains any Black card, the highest Black card wins.\n(6) Otherwise, if there is a lead suit, the highest card of the lead suit wins.\n(7) Otherwise (all Escapes), the first card played wins.\n\nThe player who played the winning card wins the trick, adds 1 to their trick count for this hand and leads the next trick of the hand. Capture bonuses are recorded for the trick winner: +30 for each Pirate in a trick won by the Skull King, and +40 if the Mermaid wins a trick containing the Skull King. The winner, the cards played and any bonus are announced to everyone.\n\nEND OF EACH HAND (after the third trick). Each player scores:\n- Exact bid of 1, 2 or 3: +20 per trick bid, plus all capture bonuses they recorded this hand.\n- Exact bid of 0: +20, plus any capture bonuses they recorded this hand (normally none).\n- Missed bid of 0: -20, and bonuses are lost.\n- Missed bid of 1, 2 or 3: -10 per trick of difference between bid and tricks won, and bonuses are lost.\n\nScores are announced. Trick counts and bonuses reset to 0 for the next hand.\n\nEND OF GAME. After hand 9 (round 27), the game ends.",
    "objective": "After 9 hands the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw among the tied players.",
    "expected_effect": "Each hand becomes a tight puzzle. Players bid from 3 cards and the public bids of rivals. They then play to land exactly on their own bid while using card order, trumps and Escapes to force rivals over or under theirs. With only 9 of 25 cards dealt, players must infer who holds the Skull King, the Mermaid or a high Black from bids (a bid of 2 or 3 signals strength) and from the cards already played. Deal luck affects bonuses but is averaged over 9 hands, and the exact-bid rule rewards accurate judgement whatever the cards. Simple policies lose. Always bidding 0 gets set by opponents who lead so as to force it to win. Always bidding 3 almost never comes in exact. Always bidding 1 and playing randomly misses often against players who steer tricks. Seat edge is removed by the rotating first lead (3 times per seat). There is no cooperation to unravel, and trailing players in the final hands have a real reason to take risky bids. Talk is deliberately left out. With one winner, players do disagree, but the public simultaneous bids already serve as signals players can test against later play. Free talk would add unenforceable claims about hands at the cost of extra steps, and nothing to agree on that would change the trick play."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 12,
    "choice_steps_per_round": 4,
    "attributes": 13,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 27
  }
}
```
````
