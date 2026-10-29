# english_auction: ready for review

Built from the variation **Budget English Auctions** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Play 8 auctions in a row. Each player has one fixed budget of 40 coins for the whole game; unspent coins have no value except as a tiebreak. (fixes: P1): Truthful bidding now exhausts the budget on low-margin items. A player must plan which auctions to contest and save coins for later, so bidding to value stops being dominant.
- Every player owns an identical private deck of 8 valuations {2,4,6,8,10,12,14,16}, shuffled separately. One card is revealed privately to each player per round, so every value is used exactly once. (fixes: P2): All players receive the same total opportunity over the game. Luck changes only timing, which budgeting and reading opponents can correct for.
- Only the winner's valuation is revealed after each auction; drop-outs and bids are public. (fixes: P3): Players can count which values an opponent has already used and infer their remaining cards and budget from how they bid. This builds inference and opponent modelling across rounds.
- Each auction has at most 3 bidding steps. In each step, all active non-leaders at once either raise (a whole number at least 2 above the standing bid) or drop for good. Ties are broken by lower score, then by a rotating seat order. (fixes: P4): This keeps the ascending, open, drop-out character of an English auction. It is bounded and fits the step limits, and the cap on steps makes jump bids a meaningful signal.
- There are 3 to 5 players, and the highest total profit wins. Tie on profit goes to more coins left, then a draw. Overpaying can drive profit below zero. (fixes: P5): With three or more players the game is not zero-sum between any two. 'Always pass' scores 0 and loses to anyone who makes profitable purchases, and 'always bid high' goes negative.
- Add one simultaneous message per player before bidding each round. (fixes: P3): This allows non-binding bidding rings ('you take this one, I take the next'), bluffs about one's card and tests of trust. Only one player can win, so following a proposal can cost you.

Objective: The player with the highest score (total of value minus price over items won) wins. If scores are tied for the top, the tied player with more coins remaining wins. If still tied, the game is a draw among them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Every player holds the same eight values (2, 4, 6, 8, 10, 12, 14, 16; sum 72) and the same 40 coins, so no seat starts with more value or money. The seat tie-break rotates with the round, and the lowest-score tie-break favours whoever is behind, so no seat has a fixed edge from move order. The budge
- playable: pass. Rules cover every situation:
- Minimum raise is standing bid + 2, capped at current coins.
- A player who cannot afford the minimum is forced to drop.
- The leader is skipped; an outbid former leader stays active.
- Ties for the highest raise resolve by lowest score, then by rotating seat order.
- B
- reasoning_over_luck: pass. Chance only sets the order in which each player's identical cards arrive. Everyone receives the same total value over the game, so the deal cannot hand anyone a better hand overall.

There is a lot to infer. Each player knows their own remaining cards. When a leader wins, their value is revealed, so

## Complexity

- steps_per_round: designed 15, built 12, limit 20
- choice_steps_per_round: designed 4, built 2, limit 4
- attributes: designed 11, built 32, limit 20 (built: 80)
- hidden_elements: designed 1, built 9, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 8, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Start: every seat has 40 coins and score 0 (checked after one all-drop round, which changes nothing)
- pass: Start: each private deck holds 8 cards, so 7 remain after the first draw
- pass: One round with everyone dropping: each deck shrinks by one
- pass: Full match where everyone always drops: all 8 cards used, all tie and share the win
- pass: Round 2 starts fresh: no leader, standing bid 0, the seats that dropped in round 1 are asked again
- pass: Talk changes no state
- pass: Only active non-leaders are asked: seat 2 leads at 6 and seat 1 is asked and drops
- pass: Raise range: standing bid 6 and coins 10 allow 8 to 10 only
- pass: A seat with 1 coin is forced to drop and never asked
- pass: A seat that drops in step 1 stays out while the others bid on
- pass: Leader at 10 is not asked and keeps the item when the others drop
- pass: Highest raise 8 sets the standing bid and its bidder leads
- pass: Tie at 6: the lower score (seat 2 at -5) leads
- pass: Round 2 with 4 seats: tied raises and scores, seat 2 beats seat 1
- pass: Round 3 with 4 seats: counting from seat 3 wraps, so seat 1 beats seat 2
- pass: Outbid seat 1 stays active, raises to 10 in step 2 and wins
- pass: After the steps resolve, standing bid and leader are public
- pass: Nobody raises in step 2: bidding ends and leader seat 1 pays 4
- pass: Bidding ends after step 3: seat 2 leads at 8 and pays
- pass: Value 6 bought at 10: coins 30, score -4
- pass: The buyer's value 14 is revealed
- pass: Everyone drops at once: item unsold, nothing changes
- pass: Coins carry over: buy at 10 in round 1, then spend the remaining 30 in round 2
- pass: Game ends after round 8 settles; highest score wins
- pass: Tie on score is broken by more coins
- pass: Same score and same coins share the win

## Does the file follow the spec's shape? (flags for a person)

- the spec declares player attribute `raise` but the game file does not: a piece of state the rules need is missing

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 40 random matches at tables [3, 5], results {'seat 2': 14, 'seat 3': 11, 'seat 1': 8, 'seat 5': 4, 'seat 4': 3}, 36-83 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 61.3 decisions, prompts of 223 characters on average (longest 293)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 20, 'seat 3': 20, 'seat 1': 20}
- always `first@seat1`: won 44, lost 15, drew 1
- always `first@seat2`: won 47, lost 13, drew 0
- always `last@seat1`: won 0, lost 59, drew 1
- always `last@seat2`: won 2, lost 58, drew 0

## Choices the rules did not make

- 3 to 5 players, suggested 4: The designer's suggested size of 4 is kept. The minimum is 3 because an auction needs at least two rivals for a bidder, so that the tie-breaks and the budget pressure matter. The maximum stays at 5 because with more seats one player's bids rarely decide an item and the talk becomes long.
- Talk kept as a simultaneous poll broadcast to all: The source requires simultaneous messages. Talk earns its place because players disagree about who should win each item and can bluff about their values or signal restraint, and none of it is binding.
- Strategy at the table: A thoughtful player bids below their value, saves coins for high-value rounds since the deck's remaining cards are known to them, reads rivals' coins and messages, and uses the 3-step limit to jump-bid. A thoughtless player overpays early or drops good items.
- Tie-break encoded as a priority number: The priority raise*10000 + (500 - score)*10 - ((seat - start_seat + n) mod n) orders by highest raise, then lowest score, then seat order from start_seat. Scores stay within about -40 to 128, so the terms never overlap.
- Ranking expression score*1000 + coins: Coins never exceed 40, so coins act only as a tie-break after score, as the source states.
- Forced drop applied at the start of each step: The source says such a player must drop. Applying it before the poll means they are never offered a choice they cannot make.
- Card values given as card_min_value 2, card_value_step 2 and card_max_value 16: Parameters must be single numbers. The deck 2, 4, ..., 16 is every value from the minimum to the maximum in steps of 2, which is 8 cards (deck_size).

## Simplifications

- The secretly shuffled deck is modelled as random draws without replacement from the player's deck list: This is equivalent to drawing in order from a separately shuffled deck, and the order stays secret even from its owner.
- The 3 bidding steps are a repeated block of four steps that stops when bidding_open becomes false: The engine runs steps in a flat list with repeat. A step where nobody raises, or step 3, closes the bidding.
