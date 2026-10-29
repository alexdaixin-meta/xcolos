# 03 design

- time: 2026-10-27T17:54:47+00:00 (47.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 3375831336580bf6, reply sha256 d2652f999d78f665

## Sent

````
Original game: Wizard
Players in the original: 3 to 6

Original rules:
Wizard uses 60 cards: 1-13 in four suits plus 4 Wizards (highest) and 4 Jesters (lowest). 3-6 players play 60/players rounds, dealt 1 card first round, 2 second, etc. After each deal one card is turned for trump; Jester means no trump, Wizard lets dealer choose. In turn order each player bids number of tricks they will take (bids need not sum to tricks available). Then cards are played clockwise; must follow led suit if possible, but Wizards/Jesters may be played anytime. Trick won by first Wizard, else highest trump, else highest of led suit; Jester led means next suit sets led suit, and only Jesters means first Jester wins. Scoring: exact bid = 20 + 10 per trick taken; otherwise -10 per trick off bid. Highest total after final round wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Limits: 14 steps (≤20), 4 choice steps: one bid poll plus three card plays (≤4), 16 attributes (≤20), 2 hidden elements: hands and secret bids (≤3), 1 random draw: one shuffle per hand, then the deal and trump turn are removals from the shuffled list (≤1), 36 rounds (≤40). The once-per-hand deal/trump/bid steps use per-step `when` conditions (trick index = 1), not a conditional block, so this is legal. Trick resolution is a complex check a referee may rule. Scores are arithmetic. It is finite, needs no board and no clock, and the bid is a simultaneous poll as required. No talk with 3 players is defensible: bids and played cards are public and give material to reason about. Trick winner, lead, led suit, Jester-led and Wizard-led cases are all specified. DEFECT: rule (8), the engine's fallback for an illegal or unknown card, is not deterministic. (i) 'Lowest card overall' gives no tiebreak between equal ranks of different suits, e.g. Red 2 vs Blue 2. (ii) It does not say where Wizards rank in that ordering, e.g. a hand of Wizard plus Green 5. (iii) 'Lowest card of the led suit' is undefined when a Wizard was led. The phrase 'first legal card' also conflicts with the explicit ordering. An engine cannot apply this rule without inventing an order, so the rules are not complete.
- change: Playable: rewrite rule (8) as a total, deterministic order. Example: 'If a player names an illegal or unknown card, the engine plays, in this priority: (a) if there is a led suit and the player holds it, their lowest card of that suit; (b) otherwise a Jester if held; (c) otherwise their lowest suited card, with ties between equal ranks broken Red < Blue < Green; (d) otherwise a Wizard. When a Wizard was led there is no led suit, so skip (a).' Remove the phrase 'first legal card' so there is only one ordering.
The variation that was reviewed: Wizard Triad: DECK: 28 cards. Three suits (Red, Blue, Green), each with ranks 1 to 8 (24 cards), plus 2 Wizards and 2 Jesters.

STRUCTURE: The game is 12 hands. Each hand is 3 tricks, and each trick is one round, so the game is 36 rounds. Players are P1, P2 and P3, seated in that order, and play always proceeds P1 -> P2 -> P3 -> P1.

START OF A HAND (first trick of each hand only):
(1) Shuffle all 28 cards. Deal 3 cards face down to each player; each player sees only their own cards.
(2) Turn the next card face up as the trump card. If it is a suited card, that suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.
(3) Bidding: all three players at the same moment secretly choose a bid of 0, 1, 2 or 3 tricks. Then all bids are revealed to everyone. Bids need not add up to 3.
(4) The first lead of hand h goes to P1 if h is 1, 4, 7 or 10; to P2 if h is 2, 5, 8 or 11; and to P3 if h is 3, 6, 9 or 12.

EACH TRICK:
(5) The leader plays one card face up. Then the next player in seat order plays one card, then the third.
(6) Legal plays: a Wizard or a Jester may always be played. Otherwise a player must play a card of the led suit if they hold one; if they hold none, they may play any card.
(7) The led suit is the suit of the first suited card played in the trick. If a Jester is led, the next suited card played sets the led suit. If a Wizard is led, there is no led suit for this trick, and everyone may play anything.
(8) Illegal choices: if a player names an illegal or unknown card, the engine plays the first legal card in that player's hand, in this order: the lowest card of the led suit; otherwise a Jester; otherwise the lowest card overall.
(9) Winning the trick:
   - If any Wizard was played, the first Wizard played wins.
   - Otherwise, if any trump was played, the highest trump wins.
   - Otherwise, the highest card of the led suit wins.
   - If all three cards are Jesters, the first Jester played wins.
(10) All played cards stay visible to everyone for the rest of the hand. The trick winner adds 1 to their tricks taken this hand and leads the next trick of the hand.

END OF A HAND (after the third trick):
(11) Each player compares their tricks taken with their bid.
   - Exact: they score 30 + 5 × bid. So bid 0 scores 30, bid 1 scores 35, bid 2 scores 40, bid 3 scores 45.
   - Not exact: they score -10 × |tricks taken - bid|.
(12) Scores and all bids and tricks are announced. Tricks taken reset to 0.

There is no talk phase. Winner: After hand 12 (round 36), the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Wizard is a 3-6 player trick-taking game played with a 60-card deck (four suits of 1-13, plus 4 Wizards and 4 Jesters). Hands grow from 1 card up to 60/players cards, each player bids the exact number of tricks they will take, and exact bids score 20 + 10 per trick while misses lose 10 per trick off.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "No simple policy is safe. Always bidding 0 fails whenever a player is dealt Wizards or high trumps. Always bidding the hand size fails almost every time. Every miss costs points, so each bid has to fit the hand. Seat advantage comes only from who leads, and the deal rotates that."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Over many hands, good hand evaluation, reading the other bids and managing tricks (ducking, throwing a Jester, taking a trick on purpose to wreck an opponent's bid) beat naive play reliably. Card luck is real but averages out across about 15-20 hands."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still score on easy hands. Strong players keep improving at counting played cards, inferring holdings from bids and playing to break opponents' contracts."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Bids reveal partial information about what others hold. Play requires inferring which cards remain and what each opponent needs to make their bid."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Trick winners and scores follow mechanically from the cards played and the bids made."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "Up to 20 rounds with up to 20 tricks each means hundreds of sequential card plays. Hand size changes every round and the dealer may choose trump. This is far too long and varied for the step and round limits, so it must be compressed."
    }
  ],
  "problems": [
    "The original is far too long: up to 20 hands of growing size, so hundreds of card plays, beyond the 40-round limit.",
    "Variable hand size and the dealer's trump choice add steps and branches the engine cannot handle cleanly.",
    "In the previous variation, rule (8), the fallback for an illegal or unknown card, was not deterministic. It had no tiebreak between equal ranks of different suits, did not place Wizards in the order, was undefined when a Wizard was led, and its phrase 'first legal card' conflicted with its explicit ordering.",
    "The previous variation did not say what happens with an illegal or missing bid.",
    "The previous variation did not say what the led suit is when a Jester is led and a Wizard is played before any suited card. It also had an 'all three Jesters' rule that cannot happen with only 2 Jesters, which left the edge cases looking incomplete."
  ],
  "changes": [
    {
      "what": "Use a 28-card deck (3 suits of 1-8, 2 Wizards, 2 Jesters), 3 players, 12 hands of exactly 3 tricks each, with one trick per round, for 36 rounds.",
      "why": "This keeps the bid-then-play identity within 40 rounds and 4 choice steps per round.",
      "fixes": "The original is far too long: up to 20 hands of growing size, so hundreds of card plays, beyond the 40-round limit."
    },
    {
      "what": "Use a fixed hand size of 3. A Wizard or Jester turned as the trump card means no trump; the dealer never chooses. The first lead rotates so each seat leads first in 4 hands.",
      "why": "This removes branches and keeps the seats balanced.",
      "fixes": "Variable hand size and the dealer's trump choice add steps and branches the engine cannot handle cleanly."
    },
    {
      "what": "Replace rule (8) with one total, deterministic priority order. (a) If there is a led suit and the player holds it, play their lowest-ranked card of that suit. (b) Otherwise, play a Jester if held. (c) Otherwise, play their lowest-ranked suited card, breaking ties between equal ranks Red < Blue < Green. (d) Otherwise, play a Wizard. Step (a) is skipped whenever there is no led suit. The phrase 'first legal card' is removed.",
      "why": "The engine can then apply the fallback without inventing an order, and the rule covers every hand.",
      "fixes": "In the previous variation, rule (8), the fallback for an illegal or unknown card, was not deterministic. It had no tiebreak between equal ranks of different suits, did not place Wizards in the order, was undefined when a Wizard was led, and its phrase 'first legal card' conflicted with its explicit ordering."
    },
    {
      "what": "A missing or illegal bid counts as a bid of 1.",
      "why": "This makes bidding total and deterministic.",
      "fixes": "The previous variation did not say what happens with an illegal or missing bid."
    },
    {
      "what": "Define the led suit as the suit of the first suited card in the trick, provided no Wizard was played before it. If a Wizard is played before any suited card, the trick has no led suit. The impossible all-Jester case is replaced by a note that it cannot occur, with a harmless fallback (the first Jester wins).",
      "why": "This leaves no undefined trick states.",
      "fixes": "The previous variation did not say what the led suit is when a Jester is led and a Wizard is played before any suited card. It also had an 'all three Jesters' rule that cannot happen with only 2 Jesters, which left the edge cases looking incomplete."
    }
  ],
  "keeps": [
    "Wizards always win and Jesters always lose, and both may be played at any time.",
    "A trump suit is set by turning a card after the deal.",
    "Each player bids an exact number of tricks, and bids need not sum to the tricks available.",
    "Exact bids score a bonus and misses are penalised per trick off.",
    "Players must follow the led suit when they can.",
    "The highest total after the final hand wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The compressed design already met every limit. The only defect was a non-deterministic fallback rule plus small edge cases, and all of these are now specified exactly."
  },
  "variation": {
    "name": "Wizard Triad",
    "summary": "A 3-player, 36-round compressed Wizard. There are 12 hands of 3 cards each. Players bid secretly at the same moment, then play 3 tricks with trump, Wizards and Jesters, scoring for exact bids.",
    "players": {"min": 3, "max": 3, "suggested": 3},
    "rules": "DECK: 28 cards. Three suits (Red, Blue, Green), each with ranks 1 to 8 (24 cards), plus 2 Wizards and 2 Jesters.\n\nSTRUCTURE: The game is 12 hands. Each hand is 3 tricks and each trick is one round, so the game is 36 rounds. Players are P1, P2 and P3, seated in that order. Play always proceeds P1 -> P2 -> P3 -> P1. There is no talk phase.\n\nSTART OF A HAND (on the first trick of each hand only):\n(1) Shuffle all 28 cards. Deal 3 cards face down to each player. Each player sees only their own cards.\n(2) Turn the next card (the 10th) face up as the trump card. If it is a suited card, that suit is trump for this hand. If it is a Wizard or a Jester, there is no trump this hand.\n(3) Bidding: all three players at the same moment secretly choose a bid of 0, 1, 2 or 3 tricks. A missing or invalid bid counts as 1. Then all bids are revealed to everyone. Bids need not add up to 3.\n(4) The first lead of hand h goes to P1 if h is 1, 4, 7 or 10; to P2 if h is 2, 5, 8 or 11; and to P3 if h is 3, 6, 9 or 12.\n\nEACH TRICK:\n(5) The leader plays one card face up. Then the next player in seat order plays one card face up, then the third player.\n(6) Led suit: the led suit is the suit of the first suited card played in the trick, but only if no Wizard was played before that card. If a Wizard is played before any suited card (for example, a Wizard is led, or a Jester is led and then a Wizard is played), the trick has no led suit. Until a suited card is played, there is no led suit yet.\n(7) Legal plays: a Wizard or a Jester may always be played. If there is a led suit and the player holds a card of it, they must play a Wizard, a Jester or a card of the led suit. Otherwise they may play any card they hold.\n(8) Illegal or unknown choices: if a player names a card they do not hold, or a card they may not legally play, the engine plays a card for them using this priority, checked in order:\n   (a) if there is a led suit and the player holds a card of it, their lowest-ranked card of the led suit;\n   (b) otherwise, a Jester, if they hold one;\n   (c) otherwise, their lowest-ranked suited card, with ties between equal ranks broken Red before Blue before Green (for example, Red 2 is played before Blue 2);\n   (d) otherwise, a Wizard.\n   Step (a) is skipped whenever there is no led suit at that moment.\n(9) Winning the trick:\n   - If any Wizard was played, the first Wizard played wins.\n   - Otherwise, if any trump card was played, the highest-ranked trump wins.\n   - Otherwise, the highest-ranked card of the led suit wins.\n   - With only 2 Jesters in the deck, a trick of three Jesters cannot occur. If no card qualifies under the rules above, the first Jester played wins.\n(10) All played cards stay visible to everyone for the rest of the hand. The trick winner adds 1 to their tricks taken this hand and leads the next trick of the hand.\n\nEND OF A HAND (after the third trick):\n(11) Each player compares their tricks taken with their bid.\n   - Exact: they score 30 + 5 x bid. So bid 0 scores 30, bid 1 scores 35, bid 2 scores 40 and bid 3 scores 45.\n   - Not exact: they score -10 x |tricks taken - bid|.\n(12) Scores and all bids and tricks taken are announced. Tricks taken reset to 0 and all cards are collected for the next shuffle.\n\nEND OF GAME: after hand 12 (round 36).",
    "objective": "After hand 12, the player with the highest total score wins. If two or three players tie for the highest total, the game is a draw.",
    "expected_effect": "Play is the same as the previously tested design, except the engine can now always resolve a bad card choice or bid deterministically. Bids are secret and simultaneous, so no one simply copies an earlier bid. Players must judge their hand from three cards and the trump. During play they infer opponents' remaining cards from bids and from cards already played, and they can deliberately feed or deny tricks to break a rival's exact bid. Talk is omitted because the public bids and cards already give the material to reason with, and negotiation in a three-way contest would only invite non-binding collusion. The lead rotates evenly (4 hands per seat). With 12 hands averaging out the deal, bid accuracy and trick management decide the winner. No fixed bidding policy is safe: always bidding 0 misses whenever a player holds Wizards or trumps, and always bidding 3 almost always misses."
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
