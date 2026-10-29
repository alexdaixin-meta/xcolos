# 33 design

- time: 2026-10-27T09:21:43+00:00 (83.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 7c98f06195c6ad3b, reply sha256 a6f5bedfc22266b1

## Sent

````
Original game: Lost Cities
Players in the original: 2 to 2

Original rules:
Place board with 5 color discard spaces between players. Shuffle 60 cards (9 numbers 2-10 and 3 wagers per color). Deal 8 cards to each player; remaining cards form face-down draw pile. Oldest player starts; turns alternate. On your turn you must first play one card from hand, then draw one. To play to your expeditions: start or extend a column of that color on your side; numbers must be strictly increasing within a column; wager cards can only be played before any number card in that column, multiple allowed. To discard: place a card face-up on its color discard pile, only top visible. Then draw: take top card of draw pile or top card of any discard pile, but not the card you just discarded. Game ends immediately when last card is drawn from draw pile. Score each color: sum numbers, subtract 20 if column exists, multiply result by 1 plus number of wagers (x2,x3,x4), add 20 bonus if column has 8+ cards. No column scores 0. Highest total after three rounds wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- reasoning_over_luck FAILED: SAMPLE SIZE. Each player makes only 8 plays per hand and there are only 2 hands, so the match rests on about 16 plays per player from a 30-card shuffle. Each player sees about 13 of 30 cards per hand.

VARIANCE. Column value is dominated by which high cards (8, 9, 10) and Wagers you are dealt or draw, and the Wager multiplier amplifies it.
- Example: W,5,7,9,10 scores (31-8)x2 + 10 = 56.
- Example: 3,6,9 scores 10.
- Between two competent players the per-hand swing from the deal alone is easily 30-50 points.
- Decisions (lock choice, sequencing, denial draws) are worth perhaps 5-15.
- Estimate: with equal good play, the deal decides about 60-70% of matches. Over just 2 hands, this means chance often decides the winner.

THE HIDDEN LOCK GIVES ALMOST NOTHING TO INFER. Any discard of a colour whose column is empty must be the locked colour, because any card is legal in an empty column. So the first locked discard publicly reveals the lock. Before that, the opponent's columns already show which colours are in use.

OPPONENT MODELLING IS THIN. It reduces to watching public columns and occasionally denying a discard.

NO VOLUNTARY DISCARD. Players cannot discard a playable non-locked card except by taking -1. This removes the original game's main tactical lever (hold vs dump vs feed the opponent).

A skilled player clearly beats a careless one. But between good players the random deal, not reasoning, usually decides the winner.
- change: Cut deal luck with a mirrored deal: shuffle once and use the identical card order in hand 2 with seats swapped (Seat 2 receives Seat 1's hand-1 cards and turn positions). Or play 4 hands of 10 turns each (40 rounds) with the same mirroring per pair.
- change: Reduce wager amplification: make a Wager add +50% of S (S x 1.5, rounded down) instead of doubling. Or cap one Wager per column.
- change: Add a voluntary discard: at step (1) the player chooses a slot AND chooses 'play' or 'discard'. Discarding is free; the -1 applies only to an attempted illegal play. This restores the hold/dump/feed decisions and the denial game.
- change: Make the lock genuinely hidden: since discards are free under the change above, a discard no longer reveals the lock. Or reveal only 'card discarded' without saying whether it was a locked or illegal discard, and keep running totals private until the hand ends.
- change: Give the lock a payoff to reason about. For example, at end of hand a player scores +1 per card of the opponent's locked colour that the player holds in columns, or +5 if the player correctly names the opponent's lock in a final simultaneous guess. This creates real inference about the opponent's hidden choice.
The variation that was reviewed: Lost Cities: Locked Routes: COMPONENTS. A 30-card deck in three colours: Red, Green and Blue. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10, plus one Wager card. There are three face-up discard piles, one per colour, and only the top card of each is visible and takeable. Each player has one expedition column per colour.

STRUCTURE. The match is 2 hands of 16 turns each, 32 rounds in total. A round is one turn of the active player. In hand 1, Seat 1 takes turns 1, 3, 5, ..., 15 and Seat 2 takes turns 2, 4, ..., 16. In hand 2, Seat 2 takes the odd turns and Seat 1 the even turns.

HAND SETUP (first round of each hand). Clear all columns and discard piles, shuffle all 30 cards, and deal 5 cards to each player in order. Each player's hand is an ordered list of 5 slots; slot 1 is the oldest card. The remaining 20 cards form a face-down draw pile.

LOCKING. Each player then secretly and simultaneously locks one colour (Red, Green or Blue) for this hand. The lock stays hidden from the opponent until the hand ends. A player can never build an expedition in their locked colour.

A TURN. The active player privately sees their hand, both players' columns, the tops of the discard piles, and the size of the draw pile.
(1) Choose a card by slot. The card is resolved automatically:
- If its colour is the player's locked colour, it goes face-up onto that colour's discard pile at no cost.
- Otherwise, if it is a legal play, it is added to the player's column of that colour.
- Otherwise it goes onto that colour's discard pile and the player loses 1 point.
A number card is legal if it is higher than every number already in that column. A Wager is legal only if that column contains no number card yet.
(2) Choose where to draw from: the draw pile, the Red pile, the Green pile or the Blue pile. The player takes the top card of the chosen pile. If that pile is empty, or its top card is the card the player just discarded this turn, they take the top card of the draw pile instead. The drawn card goes into slot 5, and the other cards close up to the left.
(3) Both players are told what was played or discarded, and from which pile the player drew.

END OF HAND (after turn 16). Score each player's columns:
- A column with no cards scores 0.
- Otherwise, let S = (sum of its number cards) - 8.
- If S > 0, the column scores S x (1 + number of Wagers in it). If S <= 0, it scores S; Wagers add nothing.
- A column with 5 or more cards, Wagers included, gains a further +10.
Add the column scores to the player's running total; illegal-play penalties have already been subtracted. Both locks are then revealed.

END OF MATCH. After hand 2, compare totals. Winner: After both hands, the player with the higher total wins. Equal totals are a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Lost Cities is a two-player card game. Each turn a player plays one card to a strictly ascending colour column (wagers first) or discards it, then draws from the deck or a discard top. Columns cost 20 to open, wagers multiply the result, and there is a bonus for long columns. The previous adaptation, 'Locked Routes', cut it to 3 colours, 2 hands of 16 turns and a secret locked colour.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "In the reviewed variation no fixed policy wins. Always-play-slot-1 collects -1 penalties and negative columns. Always-discard scores near 0. Seats alternate first move between hands. Choices clearly change the outcome."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "A skilled player beats a careless one. Between competent players, though, the deal decides about 60-70% of matches. Example: W,5,7,9,10 scores 56 while 3,6,9 scores 10, so the deal swings 30-50 points per hand against 5-15 points of decision value. Only about 16 plays per player per match."
    },
    {
      "criterion": "headroom",
      "verdict": "weak",
      "evidence": "Weak players can score, but the strongest levers of the original are missing. There is no voluntary discard, so no hold/dump/feed play. The lock carries little information. This caps how much a strong player can gain over a decent one."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "bad",
      "evidence": "The hidden lock is exposed structurally. With 3 colours and one forbidden, once a player has two columns the lock is known. Any free discard into an empty colour revealed it even earlier. Opponent modelling shrinks to watching public columns."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is arithmetic on cards in columns and counted penalties."
    },
    {
      "criterion": "fits_platform",
      "verdict": "good",
      "evidence": "Turn-based and text-only, using hidden hands and discard piles handled as list operations. 32 rounds, with no board needed."
    }
  ],
  "problems": [
    "P1 Deal luck dominates: the high cards and Wagers a player is dealt or draws decide most matches between good players.",
    "P2 Small sample: about 16 plays per player per match from a fresh shuffle each hand.",
    "P3 Wager amplification: a Wager doubles (or more) a column, which magnifies deal luck.",
    "P4 No voluntary discard: the hold / dump / feed-the-opponent decision, central to Lost Cities, is missing.",
    "P5 The hidden lock reveals itself: it is exposed by the second column or the first discard into an empty colour, so there is almost nothing to infer.",
    "P6 Opponent modelling is thin: a player cannot gain by reading the opponent's hidden hand or intentions beyond public columns."
  ],
  "changes": [
    {
      "what": "Mirrored deal. Hand 1 is shuffled once, and hand 2 reuses exactly the same card order with seats swapped: the player who moved second in hand 1 receives the first player's hand-1 starting cards and moves first. Both players face the same starting hand and the same draw-pile sequence once each.",
      "why": "Removes most of the 'who was dealt the 10s and Wagers' difference. What remains is how each player handled the same cards, plus the divergence caused by different discard draws.",
      "fixes": "P1 Deal luck dominates"
    },
    {
      "what": "Two hands of 20 turns (10 plays per player per hand, 40 rounds in total) instead of 16.",
      "why": "Gives 20 decisions per player and enough turns to build 5-card columns. Stays within the 40-round limit.",
      "fixes": "P2 Small sample"
    },
    {
      "what": "A Wager multiplies a positive column score by 1.5 (rounded down) instead of doubling it. Each colour still has only one Wager.",
      "why": "Wagers remain a real gamble but no longer swing a hand by 30+ points on their own.",
      "fixes": "P3 Wager amplification"
    },
    {
      "what": "Each turn the player chooses a slot AND 'play' or 'discard'. Discarding is free. Only an attempted illegal play costs 1 point and sends the card to the discard pile. Announcements say only 'discarded X', never whether it was voluntary or illegal.",
      "why": "Restores the original game's main tactical lever: whether to hold, dump, or avoid feeding the opponent a card they want from the discard pile.",
      "fixes": "P4 No voluntary discard"
    },
    {
      "what": "The self-lock is replaced by a secret Embargo. At the start of each hand each player secretly names one colour against the OPPONENT. At the end of the hand, the opponent's column in that colour has its score halved (rounded down) if it is positive. All three colours are buildable by everyone.",
      "why": "A self-lock with 3 colours is revealed by play. An embargo chosen against the opponent stays hidden: the embargoed player never sees it until scoring. The choice is a real inference. The colours you hold few cards and no high cards in are likely the opponent's strength, so embargo there. The opponent anticipates this and may avoid over-committing to one column. The mirrored deal adds a second-hand layer: you now hold the opponent's hand-1 cards and saw how they used them.",
      "fixes": "P5 The hidden lock reveals itself"
    },
    {
      "what": "Running totals and penalties stay private until each hand's scoring. Discard draws are announced with the card taken.",
      "why": "Each player must infer the opponent's hand from the cards they pick up, the cards they discard and the cards they hold back. That is the opponent-reading of real Lost Cities, now with free discards that can be bluffs or denials.",
      "fixes": "P6 Opponent modelling is thin"
    }
  ],
  "keeps": [
    "Ascending colour columns, with Wagers allowed only before any number card",
    "Play-then-draw turn structure, drawing from the deck or any discard top, but not the card just discarded",
    "Opening cost per column (sum - 8), the multiplier for Wagers, and the long-column bonus",
    "Face-up colour discard piles that feed the opponent",
    "The reviewed variation's 3-colour, 30-card deck size"
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core push-your-luck and denial game is sound and fits the engine. The mirrored deal, free discards and a genuinely hidden embargo fix luck and inference within the limits."
  },
  "variation": {
    "name": "Lost Cities: Embargo",
    "summary": "A two-player Lost Cities with 3 colours over two mirrored hands of 20 turns. Players build ascending colour columns, can discard freely to dump or deny, and each secretly embargoes one colour of the opponent, which halves that column's score.",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "rules": "COMPONENTS. A 30-card deck in three colours: Red, Green, Blue. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9, 10 and one Wager card. There are three face-up discard piles, one per colour; only the top card of each is visible and takeable. Each player has one column per colour.\n\nSTRUCTURE. The match is 2 hands of 20 turns each, 40 rounds in total. A round is one turn of the active player. In hand 1, Seat 1 takes the odd turns (1, 3, ..., 19) and Seat 2 the even turns. In hand 2, Seat 2 takes the odd turns and Seat 1 the even turns.\n\nHAND 1 SETUP (round 1). Shuffle the 30 cards once and record this order as the match order. Deal cards 1-5 to Seat 1 and cards 6-10 to Seat 2. Cards 11-30, in order, form the face-down draw pile (card 11 on top). Each hand is an ordered list of 5 slots; slot 1 is the oldest card.\n\nHAND 2 SETUP (round 21). Clear all columns and discard piles. Do NOT reshuffle. Use the recorded match order: cards 1-5 go to Seat 2 and cards 6-10 go to Seat 1. Cards 11-30 form the draw pile in the same order. Each seat therefore starts hand 2 with the cards the other seat started hand 1 with, and moves at the same position.\n\nEMBARGO (at each hand setup, after the deal). Each player secretly and simultaneously names one colour: Red, Green or Blue. This is their embargo against the opponent for this hand. It is revealed only at end-of-hand scoring.\n\nA TURN. The active player privately sees their own hand. Both players see both players' columns, the tops of the three discard piles, the number of cards in the draw pile, and all earlier announcements of the current hand.\n(1) Choose a card by slot, and choose PLAY or DISCARD.\n- DISCARD: the card goes face-up onto its colour's discard pile. There is no cost.\n- PLAY: if the play is legal, the card is added to the player's column of its colour. If it is illegal, the card goes onto its colour's discard pile and the player loses 1 point.\nA number card is legal if it is higher than every number already in that column. A Wager is legal only if that column contains no number card yet.\n(2) Choose where to draw from: the draw pile, the Red pile, the Green pile or the Blue pile. The player takes the top card of the chosen pile. If that discard pile is empty, or its top card is the card the player discarded this turn, they take the top card of the draw pile instead. The drawn card goes into slot 5, and the other cards close up to the left. The draw pile always has at least one card at this point.\n(3) Announcement to both players: either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]'. A discard announcement never says whether it was voluntary or an illegal play. The announcement also gives the pile drawn from, and the card taken if it came from a discard pile. Penalties and totals are not announced.\n\nEND OF HAND (after turn 20). Score each of a player's three columns:\n- An empty column scores 0.\n- Otherwise let S = (sum of its number cards) - 8.\n- If S > 0 and the column holds the Wager, multiply S by 1.5 and round down. If S <= 0, the Wager has no effect.\n- A column with 5 or more cards, the Wager included, gains +10.\n- Embargo: if this column's colour is the one the opponent embargoed, and its score so far is positive, halve it, rounding down. A zero or negative score is unchanged.\nThe hand score is the sum of the three column scores minus the player's illegal-play penalties for that hand. Add it to the player's total. Then announce both embargoes, both hand scores and both totals.\n\nEND OF MATCH. After hand 2 is scored, the match ends.",
    "objective": "After both hands, the player with the higher total wins. Equal totals are a draw.",
    "expected_effect": "Mirroring means both players start from the same cards and draw-pile sequence, so the gap between them measures play rather than the deal. Expect deal luck to fall from deciding most matches to a minority. The halved Wager keeps the gamble without wild swings. Free, ambiguous discards bring back holding, dumping and denial, and make reading the opponent's hand from their pickups and discards worthwhile. The embargo forces an inference at the start of each hand: guess where the opponent is strong, from the gaps in your own hand. The opponent must hedge between one big column (high payoff, embargo risk) and two medium ones. Simple policies lose. Always discarding scores about 0. Always playing slot 1 bleeds penalties and negative columns. Always drawing from the deck feeds the opponent useful discards unchecked."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 13,
    "choice_steps_per_round": 3,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 40
  }
}
```
````
