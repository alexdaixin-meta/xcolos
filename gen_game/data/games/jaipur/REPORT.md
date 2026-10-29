# jaipur: ready for review

Built from the variation **Jaipur Bazaar (Balanced Schedule)** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Turn order follows the ABBA pattern: A, B, B, A, A, B, B, A, A, B, B, A, A, B, B, A. Each player is first in 8 rounds. A makes the game's first action; B makes the game's last action. (fixes: P3): Pairs the rounds so that each consecutive pair (1-2, 3-4, ...) has one A-first round and one B-first round. It also splits the first-move and last-move advantages between the seats instead of giving A both opening tempo and final-information play.
- The restock schedule repeats the same type in both rounds of each pair. Cloth goes in rounds 1-2 and 9-10, Silver in 3-4 and 11-12, Camel in 5-6 and 15-16, and Diamond in 7-8 and 13-14. (fixes: P1): Each seat gets first refusal on exactly 2 Diamonds, 2 Silver, 2 Cloth and 2 Camels. The Diamonds arrive at comparable times for both players: B first in round 7 and A first in round 8; A first in round 13 and B first in round 14. All of them come early enough to be sold.
- The same pairing gives each seat exactly 2 Cloth first refusals. (fixes: P2): Removes B's extra Cloth.
- The final pair, rounds 15 and 16, restocks Camels instead of goods. (fixes: P4): A card taken in round 16 can still matter, through the camel majority. No unsellable goods card is ever restocked.

Objective: After the camel bonus, the player with the higher score wins. Equal scores are a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. SUPPLY. Both hands start with 1S+1C. The market starts with 1S+1C+2 camels. The schedule adds Cloth 4, Silver 4, Diamond 4 and Camel 4. Sixteen private draws come from the 20-card deck. Each player is first in exactly 8 rounds, so each makes exactly 8 draws.

SEAT ORDER. Rounds pair as A,B | B,A | A
- playable: pass. The rules cover every situation:
- Legality of TAKE (supply, n-1 camels, hand ≤7), CAMELS (≥1 in market) and SELL (minimum n per type, sufficient cards).
- Illegal or missing actions count as a pass.
- A draw into a full hand is discarded.
- Price floor is 1. The bonus tiers are exact.
- Camel ties 
- reasoning_over_luck: pass. The only randomness is which 8 of the 20 deck cards each player draws. Diamonds drawn per player follow a hypergeometric distribution: mean 2, variance 0.947, covariance -0.632. The A-minus-B Diamond difference therefore has an SD of about 1.78 cards.

A Diamond is worth about 3 points more than an 

## Complexity

- steps_per_round: designed 14, built 13, limit 20
- choice_steps_per_round: designed 2, built 2, limit 4
- attributes: designed 19, built 54, limit 20 (built: 80)
- hidden_elements: designed 2, built 14, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 16, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup market and prices
- pass: Setup players: 1 camel, score 0
- pass: Deck starts with 20 cards
- pass: Round 2 is led by seat 2
- pass: Round 4 is led by seat 1
- pass: Round 10 restocks one cloth
- pass: Round 3 restocks one silver
- pass: Round 5 restocks one camel
- pass: Round 7 restocks one diamond
- pass: One draw per round shrinks the deck by 1
- pass: Draw into a full hand is discarded
- pass: Draw into a non-full hand is kept, nothing discarded
- pass: Private draw leaves the public market untouched
- pass: TAKE Silver 3 pays 2 camels into the market
- pass: TAKE beyond camels+1 or beyond hand limit is not offered
- pass: CAMELS takes all market camels; not offered when none left
- pass: Selling 1 diamond/silver or more than held is not offered
- pass: Selling a single cloth is legal
- pass: Selling 2 silver scores 2 x 5
- pass: Selling 3 silver adds +3
- pass: Selling 4 cloth adds +5 and the price floors at 1
- pass: Selling 5 diamond adds +8
- pass: Selling 2 diamond at 7 scores 14, price becomes 5
- pass: Price floor: 2 cloth sold at price 2 leaves price 1
- pass: Illegal sale is not offered and the other seat's state is unchanged
- pass: Each turn's public result is visible after the round
- pass: Camel majority earns +5 at the end
- pass: Tied camels give no bonus
- pass: Cards left in hand score nothing
- pass: Equal final scores share the win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [2], results {'seat 2': 7, 'seat 1': 12, 'seats 1 and 2': 1}, 26-32 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 31.7 decisions, prompts of 227 characters on average (longest 228)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 26, 'seat 1': 33, 'seats 1 and 2': 1}
- always `first@seat1`: won 6, lost 54, drew 0
- always `first@seat2`: won 10, lost 50, drew 0
- always `last@seat1`: won 29, lost 31, drew 0
- always `last@seat2`: won 28, lost 30, drew 2

## Choices the rules did not make

- Exactly 2 players (min 2, max 2, suggested 2): The designer fixed 2. The turn-order schedule, the camel majority and the market race are all built for two rivals, so a third seat would break the schedule.
- Seat 1 is player A and seat 2 is player B: The source names A and B. Mapping them to seats lets the turn-order schedule be applied.
- Only legal actions are offered, with PASS offered only when nothing is legal: The platform asks that a seat is never offered what it may not do. The source's illegal-is-a-pass rule is kept as a fallback for missing answers.
- No free talk step: The source has no talk. It is a pure two-player race, and talk would add words without changing incentives.
- The camel bonus is applied in an update step that runs only when round == 16, just before the ending check: This places the 'after round 16' bonus in a single step with a condition.
- Strategy at this table: A thoughtful player times sales before prices fall, uses private draws to plan set bonuses, takes camels to win the +5 majority or to fund multi-card takes, and denies the opponent restocked goods using the public schedule.

## Simplifications

- The deck is a hidden table list, and the 'top card' is drawn at random from it: Drawing at random from a shuffled list is equivalent to taking the top card of a deck shuffled once.
- Turn order is implemented as two ask steps addressed to first_seat and then to the other seat: The engine's step list is fixed. The acting seat is chosen from the table attribute first_seat.
