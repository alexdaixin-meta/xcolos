# 04 design

- time: 2026-10-28T01:34:32+00:00 (123.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 45d308cd367da017, reply sha256 1ea2f2bc25180b9b

## Sent

````
Original game: Open-face Chinese poker
Players in the original: 2 to 4

Original rules:
Each player builds a 13-card hand divided into front (3 cards), middle (5) and back (5). Players are dealt 5 cards face up initially, then one card per turn for 8 more turns, clockwise, starting left of dealer. Each dealt card must be placed in any incomplete row and cannot be moved afterward. When a row is full, remaining cards must go elsewhere. Final hands must satisfy back >= middle >= front in poker strength; front cannot be straight or flush; best front is trips. A foul (illegal ordering) forfeits the hand: fouler loses 6 points to each non-fouler plus royalties and loses own royalties. Scoring: 1 point per row won vs each opponent, +3 bonus for winning all three rows (scoop). Royalty bonuses are paid for strong hands regardless of row win if hand is legal. Fantasyland bonus (QQx+ in front without fouling) gives next hand all 13 cards at once while others play open-face.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Limits as declared: steps 16 <= 20, choice steps 1 <= 4, rounds 16 <= 40, random draws: one shuffle, reused. No talk is needed with 2 players. This is not a cooperation game. The rules are mostly complete. Minor problem: step (5) contradicts step (2), which forbids naming a full row, though the fallback does define the outcome. Hand-2 foreknowledge is implied by the rules: each player knows the opponent's whole hand-2 deal and one card of each own pair. This is legal but should be stated.

The resource accounting is not credible:
(a) Attributes: 8 slots x 2 players = 16 attributes before anything else. Add the 2 held cards per player (4), the scores/match totals (2) and a hand or round marker. That is at least 22 or 23, which exceeds 20, yet 16 is declared. No packing scheme is given.
(b) Hidden elements: private dealt hands, private discards, the face-down first Back card, and the recorded deck order. That is 4, against 3 declared, unless hands and discards are explicitly merged into one element.
(c) Steps: one step per round must also do all the end-of-hand scoring under a round-8 condition:
- 6 row category/strength calcs (pair, flush and triple detection each need card-by-card comparisons)
- 2 foul checks
- 3 row comparisons
- scoop
- 4 royalty types per player
- the one-fouler and two-fouler branches
Add dealing (2), the choice poll (1), conditional row placement and fallback for 2 players (about 6+) and reveal. This is very unlikely to fit in 16 steps unless steps carry many operations, and the design does not show this.
- change: Playable: give a concrete encoding that fits 20 attributes. For example: one attribute per row per player holding packed card codes (suit*10+value packed base 100), which is 6; 2 held-card attributes per player, packed into 1 each, which is 2; 2 match totals; 1 hand marker. That is about 11 attributes. Declare the true count.
- change: Playable: declare the hidden elements as (1) private hand plus own discards, treated as one element, (2) the face-down first Back card, (3) the deck order. Confirm the engine treats hands and discards as a single element.
- change: Playable: write the scoring as an explicit step list under a 'round == 8' condition, with operation counts per step. Show that dealing, the poll, placement, reveal and scoring fit within 20 steps per round. If they do not, simplify, for example by dropping the Flush category or computing row categories incrementally as cards are placed.
- change: Playable: remove the contradiction between steps (2) and (5). Either forbid full rows outright, or keep the fallback and drop 'must have an empty slot'. Also state explicitly that players may use hand-1 knowledge in hand 2.
The variation that was reviewed: Duplicate Open-Face Rows: DECK: 32 cards, values 1 to 8 in each of four suits (Red, Blue, Green, Gold).

MATCH: 2 hands of 8 rounds each, 16 rounds in total. At the start of hand 1 the deck is shuffled once and its order is recorded. Hand 2 uses the same order, but every card dealt to Player A in hand 1 goes to Player B in hand 2, and vice versa.

ROWS: Each player builds a Front row (2 slots), a Middle row (3 slots) and a Back row (3 slots).

EACH ROUND:
(1) Deal: each player privately receives the next 2 cards from the deck. Player A takes deck positions 4r-3 and 4r-2, and Player B takes positions 4r-1 and 4r, where r is the round number within the hand. In hand 2, A and B swap these positions.
(2) Choice: at the same moment, each player secretly chooses which of their 2 cards to keep and which row to put it in. The row must have an empty slot.
(3) The other card is discarded face down. Only its owner ever knows it.
(4) Reveal: both kept cards are revealed in their rows. Exception: the first card a player puts into their Back row stays face down until scoring.
(5) If a player names a full row, the card goes to their first non-full row in the order Back, Middle, Front.

After round 8 each player has exactly 8 placed cards, and the hand is scored.

ROW STRENGTH = category x 100 + sum of the card values in the row.
Categories for a 3-card row:
- Triple (all three values equal) = 3
- Flush (all three the same suit) = 2
- Pair (exactly two values equal) = 1
- otherwise = 0
If a row is both Pair and Flush, use Flush.
Front row: Pair (two equal values) = 1, otherwise 0. The Front has no flush category.

FOUL: a hand fouls if Front strength > Middle strength, or Middle strength > Back strength.

SCORING EACH HAND:
- If exactly one player fouls, the other scores 6 plus their own royalties, and the fouler scores 0.
- If both foul, both score 0.
- Otherwise compare each row. The higher strength scores 1 point; equal strengths score nothing. A player who wins all three rows gains 3 more points (scoop).
- Then each non-fouling player adds royalties:
  - Front pair: +2
  - Middle Flush: +2
  - Middle Triple: +6
  - Back Triple: +4
Royalties are added to the hand total. A fouling player gets no royalties.

After hand 1 all rows are cleared and hand 2 is played the same way. Winner: After both hands, the player with the higher match total (sum of points from hand 1 and hand 2) wins. Equal totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Open-face Chinese poker: each player places dealt cards one at a time, face up and permanently, into a 3-card front, 5-card middle and 5-card back poker hand. The rows must rise in strength from front to back or the hand fouls. Players score per row won against each opponent, plus a scoop bonus and royalties for strong rows.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Neither the original nor the previous variation has a safe dominant policy. 'Always keep the highest card and fill Back first' often ends with a high last card forced into Front, which fouls. 'Fill Front first' fouls even more often. Random placement fouls about half the time. The previous variation's duplicate deal (both seats get both halves of the same shuffle) already removed the seat edge, and that is kept."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, 13-card hands give a lot of card luck, and a single match is noisy. The previous variation's duplicate structure cancels deal luck, which is good, but it was only 2 hands long. The real problem was that its scoring could not be built as written, so its skill signal was never realised. The revision keeps duplicate dealing, plays 4 hands (two shuffles, each played from both seats) and gives 3 options per decision instead of 2."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "A weak player who simply avoids fouling still wins some rows. A strong player gains by tracking cards (4 copies of each value), deciding when to chase pair royalties against foul risk, deciding which rows to contest given the opponent's visible rows, and, in the second hand of each pair, predicting the opponent from the exact cards they will be offered."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Each player's options and discards are hidden. Future cards are unknown but can be estimated by counting. In the mirrored hand, a player knows exactly which 3 cards the opponent is offered each round, because they are the cards that player held earlier. This lets them model the opponent and plan over several rounds: commit early to a pair line, or keep slots flexible."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Row strength, fouls, row wins, scoop and royalties are all arithmetic on card values. No judge is needed."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "The original has 13 cards per player, poker-hand categories, 2 to 4 players and Fantasyland: far beyond the limits. The previous variation failed its playability review for four reasons. It declared 16 attributes but needed 22 or more. It declared 3 hidden elements but had 4. Its scoring (flush, pair and triple detection over 3-card rows, plus a face-down card) could not plausibly fit the step count. Its rules contradicted themselves on full rows."
    }
  ],
  "problems": [
    "P1 Attribute count was understated: 8 row slots per player, held cards, totals and a marker came to 22 or more, against a limit of 20.",
    "P2 Hidden elements were understated: private hands, private discards, a face-down Back card and the deck order made 4, against a limit of 3.",
    "P3 End-of-hand scoring was too heavy to build. Category detection for 3-card rows (flush, pair, triple, each needing card-by-card comparison), foul checks, comparisons, royalties and foul branches were all crammed into an undeclared step budget.",
    "P4 The rules contradicted themselves: one step forbade naming a full row, and another gave a fallback for doing so.",
    "P5 Knowledge carried between hands (the mirrored deal) was implied but never stated, so players might not know they may use it.",
    "P6 A match of only 2 hands, with 2 options per decision, gives a thin skill signal. One mistake decides the match."
  ],
  "changes": [
    {
      "what": "Drop suits and flushes. Use 32 cards: values 1 to 8, four copies of each. The only made hand is a pair.",
      "why": "Pair detection in a 2-card row is a single equality test, so category scoring becomes one arithmetic expression.",
      "fixes": "P3 Scoring too heavy to build"
    },
    {
      "what": "Rows become Front 1 slot, Middle 2 slots, Back 2 slots: 5 cards per hand, one per round. Front strength = 2 x card value. Middle and Back strength = sum of the two cards + 100 if they pair.",
      "why": "This removes 3-card category logic entirely. It also cuts row slots from 8 to 5 per player. Doubling the Front card puts it on the same scale as a two-card sum, so the rising-strength rule still bites.",
      "fixes": "P1 Attribute count understated; P3 Scoring too heavy to build"
    },
    {
      "what": "Remove the face-down first Back card. Each player's dealt cards are one private hand list, and discards are simply removed from it and never shown. Declared hidden elements: (1) each player's private hand, (2) the deck order.",
      "why": "Two hidden elements is honest and within limits. Discards need no storage because only their owner ever knew them.",
      "fixes": "P2 Hidden elements understated"
    },
    {
      "what": "Use an explicit encoding of 19 attributes. Per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a match total, a chosen card and a chosen row, which is 9 x 2 = 18. Add 1 shared deck list. At scoring, strengths are written over F, M1 and B1, so no extra attributes are needed.",
      "why": "Gives a credible count inside the limit of 20.",
      "fixes": "P1 Attribute count understated"
    },
    {
      "what": "Write an explicit step list of 17 steps. Scoring steps carry a 'last round of a hand' condition.",
      "why": "Shows that dealing, the two polls, placement, reveal and scoring fit within 20 steps.",
      "fixes": "P3 Scoring too heavy to build"
    },
    {
      "what": "Keep only the fallback: a player may name any row, and if it is full the card goes to the first non-full row in the order Back, Middle, Front.",
      "why": "One consistent rule, with no forbidden choice that the engine would have to block.",
      "fixes": "P4 Rules contradicted themselves on full rows"
    },
    {
      "what": "State explicitly that everything seen in earlier hands may be used, including that in the mirrored hand the opponent receives exactly the cards you were dealt.",
      "why": "Makes the main inference lever visible and legal.",
      "fixes": "P5 Cross-hand knowledge not stated"
    },
    {
      "what": "Play 4 hands of 5 rounds (20 rounds). Hands 1 and 2 use one shuffle from both seats; hands 3 and 4 use a second shuffle from both seats. Each player is dealt 3 cards per round and keeps 1.",
      "why": "Doubles the duplicate sample and gives a real choice each round, while keeping at most one random draw per round.",
      "fixes": "P6 Thin skill signal"
    }
  ],
  "keeps": [
    "Cards are placed permanently, one per round, into Front, Middle and Back rows.",
    "Rows must not decrease in strength from Front to Back, or the hand fouls.",
    "A foul pays the opponent 6 plus their royalties, and the fouler scores nothing.",
    "1 point per row won, plus 3 for a scoop.",
    "Royalties for strong rows tempt players into foul risk.",
    "Kept cards are face up, so each player builds against the opponent's visible rows.",
    "Duplicate dealing from the previous variation: both seats of every shuffle are played by both players."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core tension of open-face placement (commit now, foul risk later, contest visible rows) survives a smaller hand. With suits removed and 2-card rows, scoring becomes a few arithmetic expressions that fit the limits honestly."
  },
  "variation": {
    "name": "Duplicate Open-Face Pairs",
    "summary": "A two-player, five-card open-face poker duel. Each round, each player privately picks 1 of 3 cards and places it permanently in Front, Middle or Back. Rows must not decrease in strength from Front to Back. Every deal is played from both seats, so deal luck cancels and placement skill decides.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "DECK: 32 cards: values 1 to 8, four copies of each value. There are no suits.\n\nMATCH: 4 hands of 5 rounds each, 20 rounds in total. At the start of hand 1 the deck is shuffled and its order is fixed; hands 1 and 2 both use this order. At the start of hand 3 it is shuffled again; hands 3 and 4 both use the new order.\n\nSEATS: In each round r of a hand (r = 1 to 5), Seat X receives deck positions 6r-5, 6r-4 and 6r-3, and Seat Y receives positions 6r-2, 6r-1 and 6r. Positions 31 and 32 are never used. In hands 1 and 3, Player A is Seat X and Player B is Seat Y. In hands 2 and 4 they swap: B is Seat X and A is Seat Y. So in hand 2 each player is dealt exactly the cards the other was dealt in hand 1, round by round, and likewise for hand 4 and hand 3.\n\nROWS: Each player builds a Front row (1 slot), a Middle row (2 slots) and a Back row (2 slots).\n\nEACH ROUND:\n(1) Deal: each player privately receives their 3 cards for this round.\n(2) Card choice: at the same moment, each player secretly chooses 1 of their 3 cards to keep.\n(3) Row choice: at the same moment, each player secretly names a row (Front, Middle or Back) for the kept card. If the named row is full, the card goes to the first row that is not full, checking in the order Back, Middle, Front.\n(4) The 2 unkept cards are discarded. Discards are never shown to the opponent.\n(5) Reveal: both kept cards are announced face up, with the row each went to.\n\nAfter round 5 each player has exactly 5 placed cards, and the hand is scored.\n\nROW STRENGTH:\n- Front = 2 x its card value.\n- Middle and Back = the sum of the two card values, plus 100 if the two values are equal (a pair).\n\nFOUL: a hand fouls if Front strength > Middle strength, or Middle strength > Back strength. Equal strengths are allowed.\n\nROYALTIES (non-fouling players only):\n- Front card value 7 or 8: +1.\n- Middle pair: +2.\n- Back pair: +1.\n\nSCORING EACH HAND:\n- If neither player fouls, compare each row. The higher strength scores 1 point for its owner; equal strengths score nothing. A player who wins all three rows scores 3 more points (scoop). Each player then adds their own royalties.\n- If exactly one player fouls, the other scores 6 plus their own royalties, and the fouler scores 0.\n- If both foul, both score 0.\nThe hand scores are added to the match totals. All row strengths, both foul results and both hand scores are announced. Rows are then cleared for the next hand.\n\nINFORMATION: Each player sees their own dealt cards and every revealed placement. Players may use anything seen in earlier hands. In particular, in hands 2 and 4 you know exactly which 3 cards your opponent is offered each round, because they are the cards you were offered in the previous hand. In hands 1 and 3 you know the opponent was offered the cards you are about to receive in the next hand.\n\nBUILD NOTE (engine encoding):\n- Attributes per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a total, a chosen card and a chosen row. Plus one shared deck list. 19 in all.\n- Dealing copies cards by position: take a card from the front of the deck list and append it to the back, so the order survives for the mirrored hand. At the end of each odd hand, 2 more cards are rotated so the deck returns to its starting order.\n- At scoring: F becomes 2F, M1 becomes M1+M2+100*(M1==M2), and B1 becomes B1+B2+100*(B1==B2). Foul tests, row comparisons, scoop and royalties are then single arithmetic expressions on these values.",
    "objective": "After round 20, the player with the higher match total (the sum of their four hand scores) wins. Equal totals are a draw.",
    "expected_effect": "Because each shuffle is played from both seats, card luck largely cancels and the winner is whoever places better from identical cards. Each round poses a real trade-off: take the high card or the pairing card, and commit it to Back for safety or to Middle for the +2 royalty at foul risk. Front placement is a running hazard, because a late high card can force a foul. Visible opponent rows invite targeted contests, such as conceding Front to secure Middle and Back, or chasing a scoop. The mirrored hands add opponent modelling: you know the opponent's exact options and can predict their lines from how they played your cards. Simple policies all lose to careful play. 'Highest card, Back first' tends to foul through Front. 'Front first' fouls early. Random play fouls about half the time. When both players play well, the outcome turns on small edges in card counting and risk judgement, not on the draw. Talk is not used: with two players and a strictly competitive score, there is nothing to negotiate."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 20
  }
}
```
````
