# 24 design

- time: 2026-10-28T04:37:48+00:00 (51.9s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 f1e68f63cdaa222c, reply sha256 ceb33e67510b7305

## Sent

````
Original game: 3Up 3Down
Players in the original: 2 to 6

Original rules:
Each player gets 3 face-down blind cards (3DOWN) they cannot look at, then 6 cards to look at; they choose 3 to place face-up on their blind cards as their 3UP pile. Remaining 3 cards form their starting hand. Remaining deck is draw pile. On your turn clockwise you must play a card >= top of discard pile; you may play multiple copies of same rank together. If you can play, you must; after playing you refill hand to 3 from draw pile if possible. If you cannot play, you take the entire discard pile into your hand. Clear, Clear+1, Clear+2 beat any number and remove the discard pile from game; Clear ends turn, Clear+1 requires one extra play (may draw first), Clear+2 requires two extra plays. Three consecutive same numbers by any players also clears. When draw pile empty and hand empty, play from 3UP, then blindly flip one 3DOWN per turn if legal. First to empty all piles wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- balanced FAILED: DEAL: every seat gets 3 Low (1-3), 3 Mid (4-6), 3 High (7-9) and 1 C. That is 27+3=30 cards, so the deal is symmetric by band. Only the ranks inside each band are random.

THOUGHTLESS POLICIES, judged by the winner rule:
(a) Always first option (lowest legal rank, single copy). C is listed last, so this policy keeps C until it is the only legal play. That is sensible play. Its only weakness is never shedding pairs or triples, so it needs at least 10 turns to empty 10 cards, while sensible play sheds pairs and self-wipes with triples (e.g. holding three 2s is 3 cards in one turn). Against sensible opponents it usually loses the race. Against random play it usually wins. It does not win almost every time, so it is acceptable.
(b) Always last option. This plays C on turn 1, wiping an empty pile and wasting the only escape card. After that it plays the highest rank with maximum copies. It dumps its 7-9s early, then cannot beat high tops and is forced to PICK UP. It loses to sensible play.
(c) Always pass/PICK UP is not offered while a legal play exists.
No option is strictly dominant. Duplicating a top rank to complete run_count>=3 helps or hurts depending on who plays next, which is real opponent modelling.

SEAT EDGE (the failure): the game ends the instant a seat reaches cards_left=0, and seat 1 always acts first in every round. Treat the game as a race where seat i needs T_i turns. Then:
- seat 1 wins if T1 <= min(T2,T3);
- seat 2 wins if T2 < T1 and T2 <= T3;
- seat 3 wins only if T3 < T1 and T3 < T2.
With symmetric 10-card hands, T values cluster tightly (about 5-8 turns). Take T uniform on {5,6,7}:
- P(seat 1) = P(T1 <= min) = (1/3)(1 + 4/9 + 1/9) ≈ 0.52
- P(seat 3) = (1/3)(4/9 + 1/9) ≈ 0.19
- seat 2 ≈ 0.30
Seat 1 also opens round 1 on an empty pile (top_rank=0), the freest play in the game. Nothing compensates for move order: no rotation, no extra card for seat 1, no equal-turns rule. One seat having roughly 2.7 times seat 3's win rate from seating alone fails the check.
- change: Remove the move-order edge by equalising turns. When a seat reaches cards_left=0, set a flag but let the remaining seats in that round finish their turns. At round end, every seat with cards_left=0 shares the win (two or more is a draw). Only then set game_over=true. Implement this with a `when` condition on the round-end step rather than ending mid-round.
- change: Additionally (or alternatively), reduce seat 1's empty-pile opening advantage. Either rotate the first seat each round (round r starts with seat ((r-1) mod 3)+1) or deal seat 1 one extra Mid card, then re-check the race probabilities so no seat's win share exceeds about 0.4 under symmetric play.
- change: Optional cleanup: drop the unused players_out attribute, or use it in the end condition, so the attribute count reflects what the game actually needs.
The variation that was reviewed: 3Up Shed (Counted Deck): DECK. 30 cards: three copies each of ranks 1,2,3,4,5,6,7,8,9 and three Clears (C). These form four stacks: Low (1-3, nine cards), Mid (4-6, nine cards), High (7-9, nine cards) and Clear (three cards). Everyone knows the deck's composition.

SETUP (happens once, before round 1, and is completed even if 0 rounds are played).
S1. Shuffle Low, Mid and High separately.
S2. In seat order 1, 2, 3, each seat's hand receives the top 3 Low, the top 3 Mid, the top 3 High and 1 Clear. Every stack is now empty and every hand holds 10 cards.
S3. For each seat, the engine lists as up_offer every distinct choice of 3 cards from that hand. Each choice is written in ascending order, with C counting above 9, and the list is sorted ascending.
S4. All seats answer at the same moment, each picking one option into up_choice. A declined or invalid answer is replaced by the first option in up_offer.
S5. The chosen 3 cards move from hand to up_pile. Up piles are public; hands are secret.
S6. Set hand_count = 7, up_count = 3, cards_left = 10, out = false and picked_up = 0, and clear up_choice and up_offer.
S7. The table starts with an empty pile, top_rank = 0, run_count = 0, players_out = 0, game_over = false and round = 0.

ROUND (20 rounds at most). Increase round by 1. Then seats 1, 2 and 3 take one turn each, in that order. A seat's turn is skipped entirely if game_over is true or that seat's cards_left = 0 (out = true). A skipped seat makes no choice, picks nothing up and has no attribute changed.

TURN.
T1. Source: if the seat's hand is not empty, it plays from its hand. Otherwise it plays from its up_pile.
T2. Legal plays come from the source only:
- any rank r with r >= top_rank, played as 1, 2 or 3 copies, up to the number held;
- a single C, which is always legal.
On an empty pile (top_rank = 0) any card is legal. The engine lists the legal plays in ascending order of rank, then by number of copies, with C last. If the list is empty, the only option is PICK UP.
T3. The seat chooses one option. A declined or invalid answer takes the first option listed.
T4. Apply the choice:
- Rank play: put the cards on the pile and set top_rank = r. If the previous top was also rank r, add the number of cards played to run_count; otherwise set run_count to that number. If run_count >= 3, the pile is wiped: remove it from the game and set top_rank = 0 and run_count = 0.
- C: remove the pile and the C from the game, and set top_rank = 0 and run_count = 0.
- PICK UP: the whole pile goes into the seat's hand, picked_up increases by 1, and top_rank = 0 and run_count = 0.
The turn ends after any one choice; there are no extra plays.
T5. Immediately recompute hand_count, up_count and cards_left = hand_count + up_count. Set out = true if cards_left = 0, and recompute players_out. If this seat just reached cards_left = 0, it is the winner and game_over = true.

END. The game ends as soon as game_over is true, or after round 20 is completed. Winner: If a player empties all their cards (hand and up pile), that player wins immediately. Otherwise, after round 20, the player with the fewest cards_left wins. If two or more players tie for fewest, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "3Up 3Down is a shedding game for 2 to 6 players. Each turn you must play a card at least as high as the top of the discard pile or pick the whole pile up. Clear cards and three-of-a-kind runs wipe the pile. You play from your hand, then from your face-up cards, then blindly from your face-down cards, and the first to run out of cards wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "weak",
      "evidence": "In the original, playing is forced whenever a legal play exists, so many turns have only one choice. The blind 3DOWN flips are pure chance. In the previous variation no simple policy dominated. 'Lowest single' loses the race to players who shed pairs, and 'always last' wastes its Clear on turn 1. But the instant win on reaching zero cards, with seat 1 always moving first, gave seat 1 about 52% of wins against about 19% for seat 3."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "In the original, the shuffled draw pile and the blind flips decide a lot, so luck is large. The counted, band-symmetric deal of the previous variation removed most of that. However, seat order then outweighed skill."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "There is room to improve in several places: when to spend the Clear, whether to split or keep pairs, whether to complete a run of three (which wipes the pile and hands a free empty pile to the next player), which three cards to expose as the up pile, and card counting. A weak player still sheds cards every turn and finishes with some score."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden, but the deck composition is known, every deal is band-symmetric, up piles are public and every play is visible. So opponents' remaining ranks can be inferred by counting. Deciding what to leave on top for the next player requires modelling that player's likely holdings."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "The winner follows from cards_left counts, which are pure arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The original has a shared draw pile, extra plays after Clear+1 and Clear+2, and blind flips. These are costly or impossible as a flat step list. The previous variation fit the platform, but it ended mid-round and carried an unused attribute (players_out)."
    }
  ],
  "problems": [
    "P1 Seat edge: the game ends the instant a seat empties, and seat 1 always acts first in a round. Seat 1 wins about 52% of races against about 19% for seat 3.",
    "P2 Seat 1 alone opens round 1 on an empty pile and leads every round, so it always gets the earliest free plays.",
    "P3 The unused players_out attribute inflates the state.",
    "P4 Original only: blind face-down flips, the shuffled draw pile and multi-play Clears add luck and step complexity. These were already removed in the previous variation, and that removal is kept."
  ],
  "changes": [
    {
      "what": "Equal turns: reaching 0 cards no longer ends the game mid-round. Every remaining seat finishes the round. At round end, all seats with 0 cards share the win, and two or more such seats make a draw.",
      "why": "Turning the race into 'fewest turns needed' gives every seat the same number of turns, so move order no longer decides ties in turn count.",
      "fixes": "P1 Seat edge"
    },
    {
      "what": "Rotate the lead: in round r, the order is seat L, L+1, L+2 (wrapping), with L = ((r-1) mod 3)+1.",
      "why": "This spreads the lead, and the free plays onto a fresh pile that come with it, across all seats.",
      "fixes": "P2 Seat 1 opening advantage"
    },
    {
      "what": "Remove players_out. The end check uses each seat's out flag directly.",
      "why": "The state should hold only what the game uses.",
      "fixes": "P3 Unused attribute"
    },
    {
      "what": "Keep the counted 30-card deck, the band-symmetric deal and the single-play Clear, with no blind cards and no draw pile.",
      "why": "This keeps luck low and the step count small.",
      "fixes": "P4 Original luck and complexity"
    }
  ],
  "keeps": [
    "Play a card at least equal to the top of the pile, or pick the whole pile up",
    "Multiple copies of one rank may be played together",
    "Clear cards wipe the pile",
    "Three consecutive cards of the same rank wipe the pile",
    "Hand first, then the public face-up 3UP pile",
    "Choosing which 3 cards to place face-up",
    "Shedding all cards wins"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core shedding decisions are sound and fit the limits. Equal turns plus a rotating lead fix the measured seat edge."
  },
  "variation": {
    "name": "3Up Shed (Equal Turns)",
    "summary": "A three-player counted-deck shedding game. Each player has a hidden hand and a public 3-card up pile. Players must beat or match the pile or pick it up, Clears and triples wipe the pile, the lead rotates each round, and everyone who empties within the same round shares the win.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "DECK. There are 30 cards: three copies each of ranks 1 to 9, plus three Clears (C). They are split into four stacks: Low (ranks 1-3, nine cards), Mid (ranks 4-6, nine cards), High (ranks 7-9, nine cards) and Clear (three cards). Everyone knows the deck's composition.\n\nSETUP (once, before round 1).\nS1. Shuffle the Low, Mid and High stacks separately.\nS2. In seat order 1, 2, 3, each seat's hand receives the top 3 Low, the top 3 Mid and the top 3 High cards, plus 1 Clear. Each hand now holds 10 cards and every stack is empty.\nS3. For each seat, the engine lists as up_offer every distinct set of 3 cards from that hand. Each set is written in ascending order, with C counting above 9, and the list is sorted ascending.\nS4. All seats answer at the same moment, each picking one set. A missing or invalid answer takes the first set listed.\nS5. The chosen 3 cards move from the hand to that seat's up_pile. Up piles are public; hands are secret.\nS6. For each seat, set hand_count = 7, up_count = 3, cards_left = 10, out = false and picked_up = 0.\nS7. The table starts with an empty pile: top_rank = 0, run_count = 0, round = 0, game_over = false.\n\nROUND (at most 20 rounds).\nR1. Increase round by 1. Set lead = ((round - 1) mod 3) + 1.\nR2. Three turns are taken, in this order: seat lead, then the next seat, then the next (after seat 3 comes seat 1). A seat with out = true skips its turn: it makes no choice and nothing about it changes.\nR3. After the three turns: if at least one seat has out = true, set game_over = true.\nR4. If game_over is true, or round = 20, the game ends.\n\nTURN.\nT1. Source: if the seat's hand is not empty, it plays from its hand. Otherwise it plays from its up_pile.\nT2. Legal plays come from the source only:\n- a rank r with r >= top_rank, played as 1, 2 or 3 copies, up to the number held;\n- a single C, which is always legal.\nWhen top_rank = 0, every card is legal. The engine lists the legal plays by ascending rank, then by number of copies, with C last. If no play is legal, the only option is PICK UP.\nT3. The seat chooses one option. A missing or invalid answer takes the first option listed.\nT4. Apply the choice:\n- Rank play: the cards go onto the pile. If the previous top was also rank r, add the number of cards played to run_count; otherwise set run_count to that number. Set top_rank = r. If run_count >= 3, wipe the pile: remove it from the game and set top_rank = 0 and run_count = 0.\n- C: remove the pile and the C from the game, and set top_rank = 0 and run_count = 0.\n- PICK UP: the whole pile goes into the seat's hand, picked_up increases by 1, and top_rank = 0 and run_count = 0.\nEvery choice ends the turn; there are no extra plays.\nT5. Recompute hand_count and up_count, and set cards_left = hand_count + up_count. If cards_left = 0, set out = true.\n\nThere are no draw pile and no face-down cards.",
    "objective": "If the game ends because game_over is true, every seat with cards_left = 0 wins. If exactly one seat has 0 cards, it wins alone; if two or three do, the game is a draw. If round 20 ends with nobody out, the seat with the fewest cards_left wins, and a tie for fewest is a draw.",
    "expected_effect": "Every seat gets the same number of turns, so the race is decided by how few turns a player needs. Shedding pairs, timing the Clear and choosing the up pile then decide the game, not seating. Rotating the lead spreads out who plays onto a fresh pile. Two decisions now carry the opponent modelling: whether to complete a run of three (which hands the next player an empty pile), and what top card to leave for the next seat given its counted holdings. Ties for the fewest turns become draws, which is honest given the symmetric deals. Talk is left out. The conflict is real, since only the fastest wins, but nearly every play is forced by what the player holds. Any agreement such as 'don't feed the leader' cannot be enforced and changes few actual options. Talk would add words without reasoning."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 15,
    "choice_steps_per_round": 3,
    "attributes": 15,
    "hidden_elements": 1,
    "random_draws_per_round": 0,
    "rounds": 20
  }
}
```
````
