# 01 design

- time: 2026-10-27T17:52:48+00:00 (68.3s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5f3bd547f969f44b, reply sha256 965f63931c779a5e

## Sent

````
Original game: Wizard
Players in the original: 3 to 6

Original rules:
Wizard uses 60 cards: 1-13 in four suits plus 4 Wizards (highest) and 4 Jesters (lowest). 3-6 players play 60/players rounds, dealt 1 card first round, 2 second, etc. After each deal one card is turned for trump; Jester means no trump, Wizard lets dealer choose. In turn order each player bids number of tricks they will take (bids need not sum to tricks available). Then cards are played clockwise; must follow led suit if possible, but Wizards/Jesters may be played anytime. Trick won by first Wizard, else highest trump, else highest of led suit; Jester led means next suit sets led suit, and only Jesters means first Jester wins. Scoring: exact bid = 20 + 10 per trick taken; otherwise -10 per trick off bid. Highest total after final round wins.
````

## Reply

````
```json
{
  "original_summary": "Wizard is a trick-taking game for 3 to 6 players using a 60-card deck (four suits of 1-13, plus 4 Wizards and 4 Jesters). Hand sizes grow by one card each round. After each deal, every player bids exactly how many tricks they will win, scoring a bonus for an exact bid and a penalty for each trick they are off.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy wins. 'Always bid 0' misses whenever you hold a Wizard or a high trump, because a Wizard always wins its trick. 'Always bid high' misses on weak hands. Seat effects exist but rotate: the last bidder hears every earlier bid, and the leader and the last player to a trick have different information. Because the bonus needs an exact bid, choices of bid and card decide the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Good bidding and card play matter a lot over a long game. However, 20 + 10 per trick rewards an exact bid of many tricks far more than an exact bid of zero. Strong hands are therefore simply worth more, and over a short game the deal moves totals noticeably."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Card counting, reading bids, deliberately feeding or ducking tricks to make opponents miss, and protecting your own exact bid give a strong player plenty to improve on. A weak player still scores whenever their bid happens to land."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer holdings from bids and from the cards played, plan the order of their own cards across several tricks, and model whether opponents are trying to win or to avoid tricks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners follow mechanically from the cards played. Scores follow by arithmetic from bids and tricks taken."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Hands grow up to 20 cards, so a game has hundreds of sequential card plays and far more than 4 choices per round. The dealer chooses trump when a Wizard is turned, which is an extra choice. Sequential bidding by 3-6 players adds up to 6 choice steps. Supporting 6 players overflows the per-round choice limit."
    }
  ],
  "problems": [
    "P1: Length and per-round choices: growing hands mean far too many card plays per round and per game for the engine's limits (at most 4 choice steps per round, at most 40 rounds).",
    "P2: A variable player count of 3-6 makes each trick need up to 6 sequential plays, which exceeds the choice-step limit.",
    "P3: Sequential bidding costs one choice step per player and gives the last bidder a free information edge that the step budget cannot afford.",
    "P4: The dealer choosing trump on a turned Wizard is an extra choice step for a minor rule.",
    "P5: The scoring of 20 + 10 per trick makes strong hands worth much more than weak hands bid accurately, so the deal weighs heavily on totals (lottery pressure).",
    "P6: The 60-card deck with 13 ranks is larger than needed for small hands and makes the hidden-card space needlessly big for 3 players."
  ],
  "changes": [
    {
      "what": "Fix the hand size at 3 cards. Each engine round is one trick, so a hand is 3 consecutive rounds. Play 12 hands (36 rounds).",
      "why": "This keeps every round to one bid poll (only on the first trick of a hand) plus 3 card plays, which is 4 choice steps, and keeps the game within 40 rounds.",
      "fixes": "P1: Length and per-round choices"
    },
    {
      "what": "Fix the game at exactly 3 players.",
      "why": "Three sequential plays per trick plus one bid poll fits the 4-choice limit. Three players also avoid the two-player 'only the difference matters' trap, since bidding still matters for each player.",
      "fixes": "P2: Variable player count"
    },
    {
      "what": "Bids are sealed and simultaneous: all three players bid at the same moment, then all bids are revealed before the first card is played.",
      "why": "One choice step instead of three, and no seat gets the last-bidder information edge. Inferring hands from bids still matters during play.",
      "fixes": "P3: Sequential bidding"
    },
    {
      "what": "A turned Jester or a turned Wizard both mean no trump for that hand.",
      "why": "This removes the dealer's trump choice and its extra step.",
      "fixes": "P4: Dealer choosing trump"
    },
    {
      "what": "Scoring changes to: exact bid = 30 + 5 per trick bid; missed bid = -10 per trick off.",
      "why": "An exact zero bid now earns 30 against 45 for an exact three. Accuracy matters far more than hand strength, so a weak hand read correctly nearly matches a strong one, and making opponents miss becomes a central tactic.",
      "fixes": "P5: Scoring rewards strong hands (lottery pressure)"
    },
    {
      "what": "Use a 28-card deck: three suits (Red, Blue, Green) of ranks 1-8, plus 2 Wizards and 2 Jesters.",
      "why": "Each hand uses 9 cards dealt plus 1 turned card out of 28. That is enough to keep hands hidden and uncertain, while the deck stays small enough to count cards and reason about it.",
      "fixes": "P6: Deck larger than needed"
    },
    {
      "what": "The first lead of each hand rotates P1, P2, P3. Twelve hands give each player exactly 4 opening leads.",
      "why": "This removes any built-in seat edge.",
      "fixes": "P3: Sequential bidding"
    }
  ],
  "keeps": [
    "Wizards always win (the first Wizard played takes the trick) and Jesters always lose, and both may be played at any time regardless of suit.",
    "A turned trump card after each deal, with a Jester meaning no trump.",
    "Must follow the led suit if able; a Jester lead lets the next card set the suit.",
    "Bidding an exact number of tricks before play, with a bonus for hitting it and a penalty per trick off.",
    "Highest total after the final hand wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Wizard (exact trick bidding, hidden hands, Wizards and Jesters breaking suit rules) survives intact in a 3-player, 3-card format that fits the engine. The rescaled scoring makes bid accuracy, rather than the deal, decide the game."
  },
  "variation": {
    "name": "Wizard Triad",
    "summary": "A 3-player, 3-card-hand version of Wizard over 12 hands. Players make sealed simultaneous trick bids and score mainly for bidding exactly right.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK: 28 cards. Three suits (Red, Blue, Green), each with ranks 1 to 8 (24 cards), plus 2 Wizards and 2 Jesters.\n\nSTRUCTURE: The game is 12 hands. Each hand is 3 tricks, and each trick is one round, so the game is 36 rounds. Players are P1, P2 and P3, seated in that order, and play always proceeds P1 -> P2 -> P3 -> P1.\n\nSTART OF A HAND (first trick of each hand only):\n(1) Shuffle all 28 cards. Deal 3 cards face down to each player; each player sees only their own cards.\n(2) Turn the next card face up as the trump card. If it is a suited card, that suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.\n(3) Bidding: all three players at the same moment secretly choose a bid of 0, 1, 2 or 3 tricks. Then all bids are revealed to everyone. Bids need not add up to 3.\n(4) The first lead of hand h goes to P1 if h is 1, 4, 7 or 10; to P2 if h is 2, 5, 8 or 11; and to P3 if h is 3, 6, 9 or 12.\n\nEACH TRICK:\n(5) The leader plays one card face up. Then the next player in seat order plays one card, then the third.\n(6) Legal plays: a Wizard or a Jester may always be played. Otherwise a player must play a card of the led suit if they hold one; if they hold none, they may play any card.\n(7) The led suit is the suit of the first suited card played in the trick. If a Jester is led, the next suited card played sets the led suit. If a Wizard is led, there is no led suit for this trick, and everyone may play anything.\n(8) Illegal choices: if a player names an illegal or unknown card, the engine plays the first legal card in that player's hand, in this order: the lowest card of the led suit; otherwise a Jester; otherwise the lowest card overall.\n(9) Winning the trick:\n   - If any Wizard was played, the first Wizard played wins.\n   - Otherwise, if any trump was played, the highest trump wins.\n   - Otherwise, the highest card of the led suit wins.\n   - If all three cards are Jesters, the first Jester played wins.\n(10) All played cards stay visible to everyone for the rest of the hand. The trick winner adds 1 to their tricks taken this hand and leads the next trick of the hand.\n\nEND OF A HAND (after the third trick):\n(11) Each player compares their tricks taken with their bid.\n   - Exact: they score 30 + 5 × bid. So bid 0 scores 30, bid 1 scores 35, bid 2 scores 40, bid 3 scores 45.\n   - Not exact: they score -10 × |tricks taken - bid|.\n(12) Scores and all bids and tricks are announced. Tricks taken reset to 0.\n\nThere is no talk phase.",
    "objective": "After hand 12 (round 36), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.",
    "expected_effect": "Sealed bids remove the last-bidder edge and force each player to commit on the strength of their own hand. Revealed bids then become information to infer from: a player who bid 0 is probably holding Jesters and low cards, and a bid of 2 or 3 suggests Wizards or trumps. The flattened scoring (30 to 45 for exact bids, -10 per trick off) means a weak hand bid accurately is nearly as good as a strong one, so the deal matters much less than reading it right. The main tactics become counting the 10 visible cards, ducking or taking tricks to protect your own bid, and deliberately pushing tricks onto a zero-bidder or starving a high bidder to make them miss. Simple policies lose. 'Always bid 0' fails whenever you hold a Wizard. 'Always bid 3' rarely lands. 'Always play the highest card' wrecks low bids. Random play misses most hands. Talk is left out: it is a pure three-way contest, and table talk would mostly be cheap claims about holdings that cost steps without adding a decision that cards and bids do not already provide."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 16,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
