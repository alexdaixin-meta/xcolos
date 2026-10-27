# modern_art: needs review

Built from the variation **Modern Art: Sealed Gallery** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- Use a single auction type: one simultaneous sealed bid from all four players, auctioneer included. Highest bid wins. Ties go to the auctioneer, then in seat order after the auctioneer. A buyer pays the auctioneer; if the auctioneer wins, they pay the bank. (fixes: Open ascending auctions are real-time or need an unbounded number of bid turns, which the engine cannot run.): This keeps the core Modern Art tension (sell to rivals or buy your own card at a cost) in one poll.
- Drop the fixed-price, once-around and double auctions. (fixes: Five auction types plus double auctions mean many separate step blocks, which cannot be chosen between because the step list is flat.): A flat step list cannot choose between auction blocks.
- Use three artists (deck of 14/12/10 cards). Each season, the most-played artist adds 30 to its cumulative value, the second adds 20, and the third adds nothing and pays nothing. (fixes: Five artists times per-player hand and ownership counts, plus value columns, exceed the 20-attribute limit.): This fits the attribute budget. Leaving one of three artists unpaid keeps the risk of backing the wrong artist.
- A season ends when an artist's 4th card is played; that card is not auctioned. Play three seasons, and deal all 9 cards per player at the start. (fixes: Four rounds of up to 5 cards per artist across 5 artists can exceed 40 turns.): A season holds at most 10 cards, so there are at most 30 turns. One deal at setup means no chance events during rounds.
- Keep hands as the one strong hidden element. Money stays private but every bid and payment is public. (fixes: Money is already effectively trackable from public payments, so having several hidden layers adds bookkeeping, not inference.): Inference centres on what rivals hold and want to push.

Objective: After season 3, the player with the most money wins. If two or more players tie for most money, the game is a draw.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. Value of a painting. In season 1 the artist that reaches a count of 4 is always ranked first, because only one artist can reach 4. It gains +30. Second place gains +20, with ties going to the rarer artist. Third pays 0. Values build up over seasons. If one artist ranks first in all three seasons, ea
- playable: pass. The rules cover the following:
- card choice;
- forced season end on the 4th card, with that card unowned;
- simultaneous talk, then a simultaneous sealed bid;
- winner, tie-break and an all-zero rule;
- who receives payment, and that the auctioneer pays the bank on their own card;
- ranking tie-bre
- reasoning_over_luck: pass. Chance enters only through the setup deal of 9 cards from 14A/12B/10C. A hand rich in one artist gives control over when that artist reaches 4, but it is also visible pressure that rivals can price around.

Things a player can infer:
- Every card is dealt, so each player knows the remaining distribu

## Complexity

- steps_per_round: designed 18, built 14, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 41, limit 20 (built: 80)
- hidden_elements: designed 2, built 11, limit 3
- random_draws_per_round: designed 0, built -, limit 1
- rounds: designed 30, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: deck fully dealt, 9 cards each, 100 money, values 0 (checked after one all-zero turn; the card revealed is chance and not asserted)
- pass: Auctioneer picks Blue from own hand and it leaves the hand
- pass: Revealing a Crimson raises played_crimson from 2 to 3
- pass: 4th Amber is not auctioned, no bids, season ends
- pass: Auctioned card: all seats talk then bid; all-zero gives it to auctioneer
- pass: Bid range is 0 to current money: seat with 50 may bid 50 but not 51
- pass: Highest bid (seat 2, 30) wins the card
- pass: Tie among non-auctioneers goes to first clockwise from auctioneer 2 (seat 3)
- pass: Tie involving the auctioneer goes to the auctioneer
- pass: All bids 0: auctioneer 3 gets the Crimson for free
- pass: Non-auctioneer seat 1 wins at 40: pays 40 to auctioneer 4
- pass: Auctioneer wins at 25: pays the bank, nobody receives it
- pass: Winner's owned count for the artist rises from 1 to 2
- pass: Season-end tie for second (Blue 2, Crimson 2) goes to rarer Crimson
- pass: Season end adds 30 to first (Blue), 20 to second (Amber), 0 to third
- pass: Payouts: first and second artists pay owners, third (valued Crimson) pays nothing
- pass: After payouts owned and played counts reset, hands keep cards, season 1 -> 2
- pass: Auctioneer passes from seat 4 to seat 1 after an auction turn
- pass: Auctioneer passes from seat 3 to seat 4 after a season-ending turn
- pass: Third season ends: most money (seat 3) wins
- pass: Third season ends with seats 2 and 3 tied for most money: shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [4], results {'seat 3': 7, 'seat 2': 4, 'seat 4': 4, 'seat 1': 4, 'seats 2 and 4': 1}, 120-235 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 159.0 decisions, prompts of 227 characters on average (longest 341)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 98% of decided matches against random seats
- always taking the first option as seat 2 wins 97% of decided matches against random seats
- random seats: {'seat 3': 17, 'seat 2': 16, 'seat 4': 14, 'seat 1': 12, 'seats 2 and 4': 1}
- always `first@seat1`: won 59, lost 1, drew 0
- always `first@seat2`: won 58, lost 2, drew 0
- always `last@seat1`: won 5, lost 55, drew 0
- always `last@seat2`: won 7, lost 53, drew 0

## Triage (whose problem each failure was)

- round 1: revise_rules: The game file works as specified, but the design lets a thoughtless policy dominate. Always taking the first option, in practice bidding 0 and never spending, wins about 98% of decided matches. Always taking the last option, bidding everything, loses about 90%. Holding cash beats competing for paintings, which is a flaw in the economy, not in the code.

## Choices the rules did not make

- Exactly 4 players, suggested 4: The designer fixed 4, and the deck deals exactly 9 cards to each of 4 players. Fewer players would leave no rivals to bid against; more would not fit the deal.
- Talk kept as a simultaneous poll before each bid: The source requires it. It also earns its place: players disagree about prices, and they can use it to talk up artists or bluff about their holdings.
- Bid tie-break encoded as the key bid * 10 + (4 - clockwise distance from the auctioneer): This gives the source's tie order, auctioneer first and then clockwise, in plain arithmetic, and it also covers the all-zero case.
- Artist ranking encoded as the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3): This gives the source's tie rule, rarer artist wins, in plain arithmetic.
- Cards are stored as artist names: Paintings of the same artist are indistinguishable in these rules.
- The 'auctioneer has no cards' skip is not built as a step: The source says it cannot happen: at most 30 cards are played and each hand holds 9.
- Money is marked observable: It is the score, and every payment is announced, even though money is formally known only to its owner.

## Simplifications

- The season-end block is written as individual steps each guarded by 'when season_ending', and the auction steps are guarded by 'when not season_ending': The step list is flat, but per-step conditions express the same flow exactly.
- A tie for most money is a shared win among the tied leaders: The engine has no separate draw. The rules call this a draw, and sharing the top is how that is reported.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (message, message, message, message) in `your_starting_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (current_card, first_artist, second_artist) in `your_starting_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 3: passed
