# Variation: Lost Cities: Embargo

A two-player Lost Cities with 3 colours over two mirrored hands of 20 turns. Players build ascending colour columns, can discard freely to dump or deny, and each secretly embargoes one colour of the opponent, which halves that column's score.

Players: 2 to 2, best with 2

## Review of the original

Lost Cities is a two-player card game. Each turn a player plays one card to a strictly ascending colour column (wagers first) or discards it, then draws from the deck or a discard top. Columns cost 20 to open, wagers multiply the result, and there is a bonus for long columns. The previous adaptation, 'Locked Routes', cut it to 3 colours, 2 hands of 16 turns and a secret locked colour.

- **non_degenerate**: good. In the reviewed variation no fixed policy wins. Always-play-slot-1 collects -1 penalties and negative columns. Always-discard scores near 0. Seats alternate first move between hands. Choices clearly change the outcome.
- **skill_sensitive**: weak. A skilled player beats a careless one. Between competent players, though, the deal decides about 60-70% of matches. Example: W,5,7,9,10 scores 56 while 3,6,9 scores 10, so the deal swings 30-50 points per hand against 5-15 points of decision value. Only about 16 plays per player per match.
- **headroom**: weak. Weak players can score, but the strongest levers of the original are missing. There is no voluntary discard, so no hold/dump/feed play. The lock carries little information. This caps how much a strong player can gain over a decent one.
- **reasoning_dependent**: bad. The hidden lock is exposed structurally. With 3 colours and one forbidden, once a player has two columns the lock is known. Any free discard into an empty colour revealed it even earlier. Opponent modelling shrinks to watching public columns.
- **verifiable**: good. All scoring is arithmetic on cards in columns and counted penalties.
- **fits_platform**: good. Turn-based and text-only, using hidden hands and discard piles handled as list operations. 32 rounds, with no board needed.

## Problems

- P1 Deal luck dominates: the high cards and Wagers a player is dealt or draws decide most matches between good players.
- P2 Small sample: about 16 plays per player per match from a fresh shuffle each hand.
- P3 Wager amplification: a Wager doubles (or more) a column, which magnifies deal luck.
- P4 No voluntary discard: the hold / dump / feed-the-opponent decision, central to Lost Cities, is missing.
- P5 The hidden lock reveals itself: it is exposed by the second column or the first discard into an empty colour, so there is almost nothing to infer.
- P6 Opponent modelling is thin: a player cannot gain by reading the opponent's hidden hand or intentions beyond public columns.

## Changes

- Mirrored deal. Hand 1 is shuffled once, and hand 2 reuses exactly the same card order with seats swapped: the player who moved second in hand 1 receives the first player's hand-1 starting cards and moves first. Both players face the same starting hand and the same draw-pile sequence once each. (fixes: P1 Deal luck dominates): Removes most of the 'who was dealt the 10s and Wagers' difference. What remains is how each player handled the same cards, plus the divergence caused by different discard draws.
- Two hands of 20 turns (10 plays per player per hand, 40 rounds in total) instead of 16. (fixes: P2 Small sample): Gives 20 decisions per player and enough turns to build 5-card columns. Stays within the 40-round limit.
- A Wager multiplies a positive column score by 1.5 (rounded down) instead of doubling it. Each colour still has only one Wager. (fixes: P3 Wager amplification): Wagers remain a real gamble but no longer swing a hand by 30+ points on their own.
- Each turn the player chooses a slot AND 'play' or 'discard'. Discarding is free. Only an attempted illegal play costs 1 point and sends the card to the discard pile. Announcements say only 'discarded X', never whether it was voluntary or illegal. (fixes: P4 No voluntary discard): Restores the original game's main tactical lever: whether to hold, dump, or avoid feeding the opponent a card they want from the discard pile.
- The self-lock is replaced by a secret Embargo. At the start of each hand each player secretly names one colour against the OPPONENT. At the end of the hand, the opponent's column in that colour has its score halved (rounded down) if it is positive. All three colours are buildable by everyone. (fixes: P5 The hidden lock reveals itself): A self-lock with 3 colours is revealed by play. An embargo chosen against the opponent stays hidden: the embargoed player never sees it until scoring. The choice is a real inference. The colours you hold few cards and no high cards in are likely the opponent's strength, so embargo there. The opponent anticipates this and may avoid over-committing to one column. The mirrored deal adds a second-hand layer: you now hold the opponent's hand-1 cards and saw how they used them.
- Running totals and penalties stay private until each hand's scoring. Discard draws are announced with the card taken. (fixes: P6 Opponent modelling is thin): Each player must infer the opponent's hand from the cards they pick up, the cards they discard and the cards they hold back. That is the opponent-reading of real Lost Cities, now with free discards that can be bluffs or denials.

## Kept from the original

- Ascending colour columns, with Wagers allowed only before any number card
- Play-then-draw turn structure, drawing from the deck or any discard top, but not the card just discarded
- Opening cost per column (sum - 8), the multiplier for Wagers, and the long-column bonus
- Face-up colour discard piles that feed the opponent
- The reviewed variation's 3-colour, 30-card deck size

## The variation's rules

COMPONENTS. A 30-card deck in three colours: Red, Green, Blue. Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9, 10 and one Wager card. There are three face-up discard piles, one per colour; only the top card of each is visible and takeable. Each player has one column per colour.

STRUCTURE. The match is 2 hands of 20 turns each, 40 rounds in total. A round is one turn of the active player. In hand 1, Seat 1 takes the odd turns (1, 3, ..., 19) and Seat 2 the even turns. In hand 2, Seat 2 takes the odd turns and Seat 1 the even turns.

HAND 1 SETUP (round 1). Shuffle the 30 cards once and record this order as the match order. Deal cards 1-5 to Seat 1 and cards 6-10 to Seat 2. Cards 11-30, in order, form the face-down draw pile (card 11 on top). Each hand is an ordered list of 5 slots; slot 1 is the oldest card.

HAND 2 SETUP (round 21). Clear all columns and discard piles. Do NOT reshuffle. Use the recorded match order: cards 1-5 go to Seat 2 and cards 6-10 go to Seat 1. Cards 11-30 form the draw pile in the same order. Each seat therefore starts hand 2 with the cards the other seat started hand 1 with, and moves at the same position.

EMBARGO (at each hand setup, after the deal). Each player secretly and simultaneously names one colour: Red, Green or Blue. This is their embargo against the opponent for this hand. It is revealed only at end-of-hand scoring.

A TURN. The active player privately sees their own hand. Both players see both players' columns, the tops of the three discard piles, the number of cards in the draw pile, and all earlier announcements of the current hand.
(1) Choose a card by slot, and choose PLAY or DISCARD.
- DISCARD: the card goes face-up onto its colour's discard pile. There is no cost.
- PLAY: if the play is legal, the card is added to the player's column of its colour. If it is illegal, the card goes onto its colour's discard pile and the player loses 1 point.
A number card is legal if it is higher than every number already in that column. A Wager is legal only if that column contains no number card yet.
(2) Choose where to draw from: the draw pile, the Red pile, the Green pile or the Blue pile. The player takes the top card of the chosen pile. If that discard pile is empty, or its top card is the card the player discarded this turn, they take the top card of the draw pile instead. The drawn card goes into slot 5, and the other cards close up to the left. The draw pile always has at least one card at this point.
(3) Announcement to both players: either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]'. A discard announcement never says whether it was voluntary or an illegal play. The announcement also gives the pile drawn from, and the card taken if it came from a discard pile. Penalties and totals are not announced.

END OF HAND (after turn 20). Score each of a player's three columns:
- An empty column scores 0.
- Otherwise let S = (sum of its number cards) - 8.
- If S > 0 and the column holds the Wager, multiply S by 1.5 and round down. If S <= 0, the Wager has no effect.
- A column with 5 or more cards, the Wager included, gains +10.
- Embargo: if this column's colour is the one the opponent embargoed, and its score so far is positive, halve it, rounding down. A zero or negative score is unchanged.
The hand score is the sum of the three column scores minus the player's illegal-play penalties for that hand. Add it to the player's total. Then announce both embargoes, both hand scores and both totals.

END OF MATCH. After hand 2 is scored, the match ends.

Objective: After both hands, the player with the higher total wins. Equal totals are a draw.

Expected effect: Mirroring means both players start from the same cards and draw-pile sequence, so the gap between them measures play rather than the deal. Expect deal luck to fall from deciding most matches to a minority. The halved Wager keeps the gamble without wild swings. Free, ambiguous discards bring back holding, dumping and denial, and make reading the opponent's hand from their pickups and discards worthwhile. The embargo forces an inference at the start of each hand: guess where the opponent is strong, from the gaps in your own hand. The opponent must hedge between one big column (high payoff, embargo risk) and two medium ones. Simple policies lose. Always discarding scores about 0. Always playing slot 1 bleeds penalties and negative columns. Always drawing from the deck feeds the opponent useful discards unchecked.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 3 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 40 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
