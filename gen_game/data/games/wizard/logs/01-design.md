# 01 design

- time: 2026-10-27T20:41:52+00:00 (57.2s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 5f3bd547f969f44b, reply sha256 16e8ecc2500f9eca

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
  "original_summary": "Wizard is a trick-taking card game for 3 to 6 players using a 60-card deck (four suits of 1-13, 4 Wizards, 4 Jesters). Hand size grows by one card each round. Players bid exactly how many tricks they will take and score well only for hitting the bid exactly.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Exact-bid scoring defeats every simple policy. Always bidding 0 loses whenever an opponent dumps a trick on you or your cards force wins. Always bidding high loses when the cards are weak. Always playing the highest card wastes winners. The dealer bids last, which gives a small informational edge, but the deal rotates so every seat holds it equally often."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Card quality matters within a single round, but the scoring rewards accuracy rather than strength: a bad hand that bids 0 and takes no tricks scores 20. Over many rounds, strong players reliably outscore weak ones through bidding judgement, card counting and sabotaging opponents' bids."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A novice can score by bidding conservatively. Expert play still improves through inference from bids, ducking and overtaking, and forcing tricks onto opponents who bid zero."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Players must infer opponents' holdings from their bids and from cards already played. The play of a round must be planned so that it lands exactly on the bid, which takes planning over several tricks."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The trick winner follows from fixed card-ranking rules, and the score is simple arithmetic on bid and tricks taken."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Later rounds have up to 20 tricks, meaning up to 20 sequential play steps in one round, far over 4 choice steps per round. The number of rounds varies (10 to 20). When a Wizard is turned for trump the dealer makes an extra choice. The full 60-card deck makes trick resolution long."
    }
  ],
  "problems": [
    "Growing hand sizes produce up to 20 tricks in a round, far beyond the limit of 4 choice steps per round.",
    "Round count and hand size depend on player count, producing long, uneven games that are hard to build.",
    "The dealer choosing trump when a Wizard is turned adds an extra choice step and an extra branch.",
    "Bids may total the number of tricks available, so every player can sometimes hit their bid without conflict, weakening the opponent-modelling tension.",
    "The large deck (60 cards, 4 suits) makes trick resolution and tracking heavy for a text engine with little gain for small hands."
  ],
  "changes": [
    {
      "what": "Every round deals exactly 3 cards to each player, so a round has 1 bid step plus 3 trick-play steps.",
      "why": "Keeps choice steps per round at exactly 4 while preserving bidding and multi-trick planning.",
      "fixes": "Growing hand sizes produce up to 20 tricks in a round, far beyond the limit of 4 choice steps per round."
    },
    {
      "what": "The game always lasts 12 rounds, for 3 or 4 players, with the dealer rotating each round.",
      "why": "12 is divisible by 3 and 4, so every seat deals and bids last equally often. The length is fixed and short.",
      "fixes": "Round count and hand size depend on player count, producing long, uneven games that are hard to build."
    },
    {
      "what": "If the turned trump card is a Wizard or a Jester, there is no trump this round.",
      "why": "Removes the dealer's extra choice without changing the core trick logic.",
      "fixes": "The dealer choosing trump when a Wizard is turned adds an extra choice step and an extra branch."
    },
    {
      "what": "The dealer, bidding last, may not make the total of all bids equal 3 (the number of tricks).",
      "why": "Guarantees at least one player cannot be exactly right. Players must read bids and fight to push others off theirs. The burden rotates fairly.",
      "fixes": "Bids may total the number of tricks available, so every player can sometimes hit their bid without conflict, weakening the opponent-modelling tension."
    },
    {
      "what": "The deck is reduced to 25 cards: three suits (Red, Blue, Green) of 1-7, plus 2 Wizards and 2 Jesters.",
      "why": "Small enough for 3-card hands with 4 players while keeping suits, trump, Wizards and Jesters. Card counting becomes feasible and meaningful.",
      "fixes": "The large deck (60 cards, 4 suits) makes trick resolution and tracking heavy for a text engine with little gain for small hands."
    }
  ],
  "keeps": [
    "Exact-bid scoring: 20 + 10 per trick if exact, otherwise -10 per trick off.",
    "Wizards always win (the first one played), Jesters always lose, and both may be played at any time regardless of the follow-suit rule.",
    "A trump suit set by a turned card.",
    "Must follow the led suit if able.",
    "Bidding in turn order with the dealer last, and a rotating dealer.",
    "Hidden hands and highest total wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core of Wizard (exact bidding plus trick play with hidden hands) is rich in inference and opponent modelling. Fixing the hand size at 3 cards and using a smaller deck brings it within the limits without losing its identity."
  },
  "variation": {
    "name": "Three-Card Wizard",
    "summary": "A compact Wizard for 3-4 players: 12 rounds of 3-card hands. Players bid exactly how many of the 3 tricks they will take, the dealer cannot let the bids total 3, and exact bids score big.",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "rules": "DECK: 25 cards: three suits (Red, Blue, Green), each numbered 1 to 7 (21 cards), plus 2 Wizards and 2 Jesters. Wizards and Jesters have no suit.\n\nSETUP: Seat players in a fixed order. Player 1 is dealer in round 1. The dealer moves one seat along each round. All scores start at 0. The game lasts 12 rounds.\n\nEACH ROUND:\n1. Deal: shuffle all 25 cards, deal 3 cards face down to each player (seen only by their owner), then turn the next card face up as the trump card.\n2. Trump: if the trump card is a numbered card, its suit is trump for this round. If it is a Wizard or a Jester, there is no trump this round.\n3. Bidding: starting with the player after the dealer and ending with the dealer, each player in turn publicly bids a whole number from 0 to 3: the number of tricks they expect to take. Each bidder sees earlier bids. The dealer may not choose a bid that makes the total of all bids exactly 3.\n4. Tricks: 3 tricks are played. The player after the dealer leads the first trick; the winner of each trick leads the next. In each trick, starting with the leader, each player in turn plays one card face up from their hand, seeing the cards already played to that trick.\n5. Led suit: the led suit is the suit of the first numbered card played to the trick.\n   - If a Jester is led, the next numbered card played sets the led suit.\n   - If a Wizard is led, there is no led suit for that trick and anything may be played.\n6. Following: a player holding a numbered card of the led suit must play either a card of that suit or a Wizard or Jester. Wizards and Jesters may always be played. A player with no card of the led suit may play any card. Only legal cards are offered.\n7. Trick winner:\n   - the first Wizard played wins;\n   - if there is no Wizard, the highest trump card wins;\n   - if there is no trump, the highest card of the led suit wins;\n   - if every card is a Jester, the first Jester played wins.\n   The winner adds 1 to their tricks taken this round.\n8. Scoring: each player whose tricks taken equals their bid scores 20 + 10 x tricks taken. Each other player loses 10 x |bid - tricks taken|.\n9. Reset bids and tricks taken, and pass the deal to the next seat.\n\nEND: after round 12 the game ends.",
    "objective": "After 12 rounds the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.",
    "expected_effect": "Every round is a small puzzle of inference: read your 3 cards against the trump, read opponents' bids to estimate their hands, then play so that you land exactly on your bid while forcing unwanted tricks onto others or stealing tricks they need. The dealer's restriction guarantees conflict: at least one player must miss, so bids become weapons and signals, and the last bidder must judge whom to squeeze. Exact-bid scoring lets weak hands score by bidding low, so skill outweighs the deal over 12 rounds. Simple policies (always bid 0, always bid 1, always play the highest card) all lose to opponents who exploit them, for example by dumping Wizard-free tricks on a zero-bidder. Talk is left out: bids already carry the public signal, and because only one player can win, open talk would add words without adding decisions."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 11,
    "hidden_elements": 1,
    "random_draws_per_round": 1,
    "rounds": 12
  }
}
```
````
