# Variation: Duplicate Open-Face Pairs

A two-player, five-card open-face poker duel. Each round, each player privately picks 1 of 3 cards and places it permanently in Front, Middle or Back. Rows must not decrease in strength from Front to Back. Every deal is played from both seats, so deal luck cancels and placement skill decides.

Players: 2 to 2, best with 2

## Review of the original

Open-face Chinese poker: each player places dealt cards one at a time, face up and permanently, into a 3-card front, 5-card middle and 5-card back poker hand. The rows must rise in strength from front to back or the hand fouls. Players score per row won against each opponent, plus a scoop bonus and royalties for strong rows.

- **non_degenerate**: good. Neither the original nor the previous variation has a safe dominant policy. 'Always keep the highest card and fill Back first' often ends with a high last card forced into Front, which fouls. 'Fill Front first' fouls even more often. Random placement fouls about half the time. The previous variation's duplicate deal (both seats get both halves of the same shuffle) already removed the seat edge, and that is kept.
- **skill_sensitive**: weak. In the original, 13-card hands give a lot of card luck, and a single match is noisy. The previous variation's duplicate structure cancels deal luck, which is good, but it was only 2 hands long. The real problem was that its scoring could not be built as written, so its skill signal was never realised. The revision keeps duplicate dealing, plays 4 hands (two shuffles, each played from both seats) and gives 3 options per decision instead of 2.
- **headroom**: good. A weak player who simply avoids fouling still wins some rows. A strong player gains by tracking cards (4 copies of each value), deciding when to chase pair royalties against foul risk, deciding which rows to contest given the opponent's visible rows, and, in the second hand of each pair, predicting the opponent from the exact cards they will be offered.
- **reasoning_dependent**: good. Each player's options and discards are hidden. Future cards are unknown but can be estimated by counting. In the mirrored hand, a player knows exactly which 3 cards the opponent is offered each round, because they are the cards that player held earlier. This lets them model the opponent and plan over several rounds: commit early to a pair line, or keep slots flexible.
- **verifiable**: good. Row strength, fouls, row wins, scoop and royalties are all arithmetic on card values. No judge is needed.
- **fits_platform**: bad. The original has 13 cards per player, poker-hand categories, 2 to 4 players and Fantasyland: far beyond the limits. The previous variation failed its playability review for four reasons. It declared 16 attributes but needed 22 or more. It declared 3 hidden elements but had 4. Its scoring (flush, pair and triple detection over 3-card rows, plus a face-down card) could not plausibly fit the step count. Its rules contradicted themselves on full rows.

## Problems

- P1 Attribute count was understated: 8 row slots per player, held cards, totals and a marker came to 22 or more, against a limit of 20.
- P2 Hidden elements were understated: private hands, private discards, a face-down Back card and the deck order made 4, against a limit of 3.
- P3 End-of-hand scoring was too heavy to build. Category detection for 3-card rows (flush, pair, triple, each needing card-by-card comparison), foul checks, comparisons, royalties and foul branches were all crammed into an undeclared step budget.
- P4 The rules contradicted themselves: one step forbade naming a full row, and another gave a fallback for doing so.
- P5 Knowledge carried between hands (the mirrored deal) was implied but never stated, so players might not know they may use it.
- P6 A match of only 2 hands, with 2 options per decision, gives a thin skill signal. One mistake decides the match.

## Changes

- Drop suits and flushes. Use 32 cards: values 1 to 8, four copies of each. The only made hand is a pair. (fixes: P3 Scoring too heavy to build): Pair detection in a 2-card row is a single equality test, so category scoring becomes one arithmetic expression.
- Rows become Front 1 slot, Middle 2 slots, Back 2 slots: 5 cards per hand, one per round. Front strength = 2 x card value. Middle and Back strength = sum of the two cards + 100 if they pair. (fixes: P1 Attribute count understated; P3 Scoring too heavy to build): This removes 3-card category logic entirely. It also cuts row slots from 8 to 5 per player. Doubling the Front card puts it on the same scale as a two-card sum, so the rising-strength rule still bites.
- Remove the face-down first Back card. Each player's dealt cards are one private hand list, and discards are simply removed from it and never shown. Declared hidden elements: (1) each player's private hand, (2) the deck order. (fixes: P2 Hidden elements understated): Two hidden elements is honest and within limits. Discards need no storage because only their owner ever knew them.
- Use an explicit encoding of 19 attributes. Per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a match total, a chosen card and a chosen row, which is 9 x 2 = 18. Add 1 shared deck list. At scoring, strengths are written over F, M1 and B1, so no extra attributes are needed. (fixes: P1 Attribute count understated): Gives a credible count inside the limit of 20.
- Write an explicit step list of 17 steps. Scoring steps carry a 'last round of a hand' condition. (fixes: P3 Scoring too heavy to build): Shows that dealing, the two polls, placement, reveal and scoring fit within 20 steps.
- Keep only the fallback: a player may name any row, and if it is full the card goes to the first non-full row in the order Back, Middle, Front. (fixes: P4 Rules contradicted themselves on full rows): One consistent rule, with no forbidden choice that the engine would have to block.
- State explicitly that everything seen in earlier hands may be used, including that in the mirrored hand the opponent receives exactly the cards you were dealt. (fixes: P5 Cross-hand knowledge not stated): Makes the main inference lever visible and legal.
- Play 4 hands of 5 rounds (20 rounds). Hands 1 and 2 use one shuffle from both seats; hands 3 and 4 use a second shuffle from both seats. Each player is dealt 3 cards per round and keeps 1. (fixes: P6 Thin skill signal): Doubles the duplicate sample and gives a real choice each round, while keeping at most one random draw per round.

## Kept from the original

- Cards are placed permanently, one per round, into Front, Middle and Back rows.
- Rows must not decrease in strength from Front to Back, or the hand fouls.
- A foul pays the opponent 6 plus their royalties, and the fouler scores nothing.
- 1 point per row won, plus 3 for a scoop.
- Royalties for strong rows tempt players into foul risk.
- Kept cards are face up, so each player builds against the opponent's visible rows.
- Duplicate dealing from the previous variation: both seats of every shuffle are played by both players.

## The variation's rules

DECK: 32 cards: values 1 to 8, four copies of each value. There are no suits.

MATCH: 4 hands of 5 rounds each, 20 rounds in total. At the start of hand 1 the deck is shuffled and its order is fixed; hands 1 and 2 both use this order. At the start of hand 3 it is shuffled again; hands 3 and 4 both use the new order.

SEATS: In each round r of a hand (r = 1 to 5), Seat X receives deck positions 6r-5, 6r-4 and 6r-3, and Seat Y receives positions 6r-2, 6r-1 and 6r. Positions 31 and 32 are never used. In hands 1 and 3, Player A is Seat X and Player B is Seat Y. In hands 2 and 4 they swap: B is Seat X and A is Seat Y. So in hand 2 each player is dealt exactly the cards the other was dealt in hand 1, round by round, and likewise for hand 4 and hand 3.

ROWS: Each player builds a Front row (1 slot), a Middle row (2 slots) and a Back row (2 slots).

EACH ROUND:
(1) Deal: each player privately receives their 3 cards for this round.
(2) Card choice: at the same moment, each player secretly chooses 1 of their 3 cards to keep.
(3) Row choice: at the same moment, each player secretly names a row (Front, Middle or Back) for the kept card. If the named row is full, the card goes to the first row that is not full, checking in the order Back, Middle, Front.
(4) The 2 unkept cards are discarded. Discards are never shown to the opponent.
(5) Reveal: both kept cards are announced face up, with the row each went to.

After round 5 each player has exactly 5 placed cards, and the hand is scored.

ROW STRENGTH:
- Front = 2 x its card value.
- Middle and Back = the sum of the two card values, plus 100 if the two values are equal (a pair).

FOUL: a hand fouls if Front strength > Middle strength, or Middle strength > Back strength. Equal strengths are allowed.

ROYALTIES (non-fouling players only):
- Front card value 7 or 8: +1.
- Middle pair: +2.
- Back pair: +1.

SCORING EACH HAND:
- If neither player fouls, compare each row. The higher strength scores 1 point for its owner; equal strengths score nothing. A player who wins all three rows scores 3 more points (scoop). Each player then adds their own royalties.
- If exactly one player fouls, the other scores 6 plus their own royalties, and the fouler scores 0.
- If both foul, both score 0.
The hand scores are added to the match totals. All row strengths, both foul results and both hand scores are announced. Rows are then cleared for the next hand.

INFORMATION: Each player sees their own dealt cards and every revealed placement. Players may use anything seen in earlier hands. In particular, in hands 2 and 4 you know exactly which 3 cards your opponent is offered each round, because they are the cards you were offered in the previous hand. In hands 1 and 3 you know the opponent was offered the cards you are about to receive in the next hand.

BUILD NOTE (engine encoding):
- Attributes per player: F, M1, M2, B1, B2 (0 = empty), a hand list, a total, a chosen card and a chosen row. Plus one shared deck list. 19 in all.
- Dealing copies cards by position: take a card from the front of the deck list and append it to the back, so the order survives for the mirrored hand. At the end of each odd hand, 2 more cards are rotated so the deck returns to its starting order.
- At scoring: F becomes 2F, M1 becomes M1+M2+100*(M1==M2), and B1 becomes B1+B2+100*(B1==B2). Foul tests, row comparisons, scoop and royalties are then single arithmetic expressions on these values.

Objective: After round 20, the player with the higher match total (the sum of their four hand scores) wins. Equal totals are a draw.

Expected effect: Because each shuffle is played from both seats, card luck largely cancels and the winner is whoever places better from identical cards. Each round poses a real trade-off: take the high card or the pairing card, and commit it to Back for safety or to Middle for the +2 royalty at foul risk. Front placement is a running hazard, because a late high card can force a foul. Visible opponent rows invite targeted contests, such as conceding Front to secure Middle and Back, or chasing a scoop. The mirrored hands add opponent modelling: you know the opponent's exact options and can predict their lines from how they played your cards. Simple policies all lose to careful play. 'Highest card, Back first' tends to foul through Front. 'Front first' fouls early. Random play fouls about half the time. When both players play well, the outcome turns on small edges in card counting and risk judgement, not on the draw. Talk is not used: with two players and a strictly competitive score, there is nothing to negotiate.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 2 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 20 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
