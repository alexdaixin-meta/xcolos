# for_sale: ready for review

Built from the variation **For Sale: Sealed Bids** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Replace the open auction with one simultaneous sealed bid per round. The highest bidder takes the highest property and pays the full bid. The second and third bidders take the middle and lowest properties and each pay half their bid, rounded down. (fixes: The open ascending auction is an indefinite loop of sequential raise/pass turns. The engine cannot express it inside one round within 20 steps.): This keeps the original's tension: a winner pays full, a loser pays half and takes a worse card. It fits in a single poll step.
- Break bid ties by a priority order that rotates each round (player 1 first in round 1, player 2 in round 2, player 3 in round 3, and so on). (fixes: Seat order matters in the auction: the starting player and the clockwise position change what each bidder knows when deciding.): Simultaneous bids plus a rotating tiebreak remove any fixed positional advantage.
- Keep bid amounts and coin totals private. Only who took which property is announced. (fixes: Too little is hidden. All bids, and therefore all coin totals, are public, so there is almost nothing to infer about rivals' spending power.): Players must infer rivals' remaining coins from the order in which properties were won. Bidding high against a rival who is secretly broke wastes money, so reading spending power becomes the core inference.
- Fix the player count at 3, using the original 3-player setup: 18 coins each, 24 properties and 24 cheques in play, 8 auction rounds and 8 selling rounds. (fixes: With 3 to 6 players, ranking bids and properties takes many steps, and the deck and coin rules change with player count. That pushes the game past the complexity limits.): Three ranks keep the ranking and award steps within limits. Three players also avoid the two-player difference trap, because one rival's loss is not automatically your gain.
- Shuffle the property deck only at the start of round 1 and the cheque deck only at the start of round 9. Every other reveal takes the top cards in order. (fixes: Two separate deck shuffles plus per-round reveals risk more than one random draw in a single round.): This keeps every round at no more than one random draw.

Objective: The player with the most final money (cheques plus remaining coins) wins. If two or more tie for most, the tied player with more remaining coins wins. If they are still tied, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Scale of money: the 30 cheques sum to 2 x (0+2+...+15) = 2 x 119 = 238, a mean of 7.93. The 24 used cheques average about 190, roughly 63 per player. All three players together start with 54 coins. Cheques decide the game, and coins only matter at the margin, as in the original.

Thoughtless policie
- playable: pass. Rules cover every case:
- bids are limited to 0..current coins;
- bid ties are broken by a defined rotating priority;
- property ties cannot happen because all cards are distinct;
- payments are stated, including the rounding rule;
- end and tie-breaks are defined: most money, then most coins, then 
- reasoning_over_luck: pass. Chance comes from the order of the 24 property cards and 24 cheques, plus 6 unseen of each.
- Every triple is contested by all three players at once, so the deal does not favour any seat.
- Luck affects how valuable individual rounds are, not who gets the good cards.

Skill enters in three ways:
- B

## Complexity

- steps_per_round: designed 18, built 12, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 12, built 40, limit 20 (built: 80)
- hidden_elements: designed 2, built 7, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: R1: at setup no seat holds any property and the game is at round 1
- pass: R2: at setup property_deck holds 30 cards and cheque_deck holds 30 cheques
- pass: R3: a buying round draws 3 properties, so the deck shrinks by 3 and each seat gains one card (which cards is chance)
- pass: R4: bid options run from 0 to the seat's current coins and no higher
- pass: R5: the highest bid takes HIGH, the next takes MIDDLE and the lowest takes LOW
- pass: R6: in round 2, tied bids give priority in the order 2, 3, 1
- pass: R6: in round 1, tied bids give priority in the order 1, 2, 3
- pass: R7: the top bidder pays the full bid of 7; all cheques are 0, so final money is the coins left
- pass: R8: second and third place pay floor(bid/2), so a bid of 5 costs 2 and a bid of 3 costs 1; all cheques are 0
- pass: R9: after a buying round the public hands show who took LOW, MIDDLE and HIGH
- pass: R10: after round 8 each seat holds 8 properties and 6 cards stay in property_deck
- pass: R11: a selling round draws 3 cheques from cheque_deck (which cheques is chance)
- pass: R12: in a selling round a seat is offered only the cards in its own hand
- pass: R13: in the last round the highest property takes cheque 15, the middle takes 9 and the lowest takes 2
- pass: R14: a played property is removed from its owner's hand
- pass: R15: after a selling round the public hands show which property each seat played
- pass: R16: after round 16 the game ends with final_money = cheques + coins
- pass: R17: equal final money is won by the seat with more remaining coins
- pass: R17: seats level on both money and coins share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 11, 'seat 3': 4, 'seat 1': 5}, 45-45 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 48.0 decisions, prompts of 263 characters on average (longest 325)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 33, 'seat 3': 11, 'seat 1': 15, 'seats 2 and 3': 1}
- always `first@seat1`: won 15, lost 45, drew 0
- always `first@seat2`: won 20, lost 40, drew 0
- always `last@seat1`: won 0, lost 59, drew 1
- always `last@seat2`: won 2, lost 57, drew 1

## Choices the rules did not make

- Exactly 3 players (min 3, max 3, suggested 3): The designer fixed 3. The 3-card reveals, the 3-way priority rotation and the LOW/MIDDLE/HIGH payment tiers are all built for exactly 3 seats.
- No talk step before bids or plays: The source has no communication phase, and talk would add a mechanic. Strategy comes from reading public hands and the inferable coin spending: bid low when the top card is weak, keep coins for the tie-break, and time high properties against strong cheques.
- Tie-break computed as bid*10 + priority weight (3, 2, 1): This puts the rotating priority rule into one arithmetic key. Bids are at most 18, so the weight never outranks a higher bid.
- bid_key is visible to its owner only (ally): It is engine scratch derived from the player's own private bid, and a player attribute cannot be fully hidden.
- Cheque values described by numeric parameters (min 0, max 15, value 1 missing, 2 copies each): Parameters must be numbers, so the value list is given as its bounds and the one skipped value.
- rank_by = final_money*100 + final_coins: This encodes the remaining-coins tie-break in one expression. Coins never exceed 18, so the x100 weighting keeps final money first.
- Separate public final_coins attribute: Remaining coins decide ties and are revealed at the end, so they are made public then. Coins stay private during play.

## Simplifications

- Shuffling and taking the top of a deck are done as random draws from the deck list: Drawing at random is equivalent to drawing from the top of a shuffled deck. The 6 never-drawn cards and cheques simply remain in the hidden lists.
- Buying and selling steps share one flat round list, gated by 'when round <= 8' and 'when round >= 9': The engine has one repeating step list. Per-step arithmetic conditions select the phase without needing conditional blocks.
