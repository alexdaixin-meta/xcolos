# modern_art: needs review

Built from the variation **Modern Art: Three Studios** (design round 2); see VARIATION.md.

## What was changed from the original, and why

- Use one auction type: a simultaneous sealed bid in which the auctioneer also bids. If the auctioneer is highest, they pay the bank; if every bid is 0, the auctioneer keeps the painting for free. (fixes: Five auction types (open ascending, once-around, fixed price, double) need sequential or near-real-time bidding and many steps; only sealed simultaneous bidding fits cheaply.): This keeps Modern Art's 'buy your own painting from the bank' tension. It needs only one simultaneous poll and replaces the secret reserve.
- Replace the card deal with three fixed 7-card hand compositions, each strong in one artist. One random draw at setup (a number 1-6) assigns the compositions to the seats through a fixed table. (fixes: Dealing dozens of random cards one at a time breaks the limit of 1 random draw per round and costs many remove/append steps (previous variation: 30+ draws declared as 0).): This takes exactly one random draw and one assignment step. The compositions are rotations of each other, so the deal is balanced. A player's composition is a hidden type that rivals must infer from what they auction and bid on.
- Cut to 3 artists and 3 players. Only the top two artists place, earning +20 and +10. The ranking uses a fixed tie order (Red, Blue, Green). The payout is one formula per player: owned count times cumulative value, summed over placed artists. Owned paintings are tracked as per-player counts for each artist. (fixes: Ranking 4-5 artists with tie-breaks, and paying every player for every artist, exceeds the step and attribute budget (previous variation understated both).): The ranking takes 2 calc steps and the payout 1 step, so the game fits 20 attributes and 20 steps when counted honestly.
- After every auction, announce all bids, the buyer and the price. Money and owned paintings are public. Only hand contents are hidden. The card played is always announced. (fixes: The previous variation never said what is announced after an auction (bids, winner, price, reserve), nor whether money and owned paintings are public, so players cannot track rivals.): Every player has the same public record to reason from. The hidden information is concentrated in hands, as in the original.
- State explicitly that every painting the auctioneer keeps (bought from the bank or taken for free) is added to the auctioneer's owned count for that artist and scores normally. (fixes: The previous variation did not state that a painting the auctioneer keeps joins their owned paintings and scores.): This removes the ambiguity about whether kept paintings score.
- Remove the reserve. (fixes: The secret reserve added a fourth hidden element and an extra choice step for little strategic gain.): The auctioneer's own sealed bid serves the same purpose. This leaves 2 hidden elements (hands and sealed bids) and 3 choice steps.
- Play 3 seasons. A season ends when the third card of one artist is played; that card is unsold. The game lasts at most 21 rounds, one card per round. (fixes: Full game length (4 rounds, about 70 auctions) is too long for the platform.): The game stays short while keeping cumulative artist values across seasons.

Objective: When the game ends, the player with the most money wins. If two or three players tie for the most money, the game is a draw.

## The critic (2 review(s) before the rules went to a coder)

- balanced: pass. Symmetry: the compositions are cyclic shifts (A = 4R/2B/1G, B = 1R/4B/2G, C = 2R/1B/4G). Each artist has 7 cards in total. Each player holds a 4-2-1 split. The only asymmetries are the Red>Blue>Green tie order, which mildly favours the A holder in second-place ties, and seat 1 auctioning first.

Sea
- playable: pass. Rules cover every case:
- Choosing a card is limited to non-empty hand counts.
- The season ender is discarded, with explicit skips.
- The sealed-bid tie-break rotates from the seat after the auctioneer, with the all-zero case overridden explicitly.
- Payment goes to the auctioneer, or to the bank i
- reasoning_over_luck: pass. The single draw only assigns which cyclic composition each seat receives. The compositions are equivalent up to relabelling, apart from the Red tie order. Chance accounts for roughly 10-15% of outcomes (tie order plus seat interplay).

With all players playing well, the winner is decided by:
- bid s

## Complexity

- steps_per_round: designed 17, built 13, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 20, built 51, limit 20 (built: 80)
- hidden_elements: designed 2, built 13, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 21, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Setup: money 60, owned 0, seasons and values 0, auctioneer seat 1
- pass: Deal (chance-independent): every composition holds all three artists, so seats 1 and 2 are each offered Red, Blue and Green
- pass: Hands (chance-independent): seat 1 opens holding cards of every artist
- FAIL: Auctioneer may only play an artist it holds | rule R4 is broken: The auctioneer may choose only an artist for which their own hand count is above 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Playing Red raises season_red by 1 and sets current_artist | rule R5 is broken: When the auctioneer plays artist X, their hand_X falls by 1, season_X rises by 1, and current_artist is announced as X.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- pass: Third Red card is discarded unsold: no bidding, no money moves, and the season scores
- FAIL: A card that does not end the season goes to auction for the other seats | rule R7 is broken: When the card is not season-ending, all three players send one short message simultaneously, and all messages are then shown to everyone.; seat 2 was never offered 0, but should have been; seat 3 was never offered 0, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Bids run from 0 to the bidder's own money, and the auctioneer bids too | rule R8 is broken: When the card is not season-ending, all three players including the auctioneer bid simultaneously a whole number from 0 to their current money.; seat 2 was never offered 10, but should have been; seat 1 was never offered 0, but should have been; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Auctioneer seat 1, bids 15/15/15: seat 2 wins at 15 | rule R9 is broken: The highest bid wins the painting; with the auctioneer at seat 1 and bids 15, 15, 15, seat 2 wins at 15.; seat 1 money: expected 75, got 60; seat 2 money: expected 45, got 60; seat 2 owned_red: expected 1, got 0; game winner_seat: expected 2, got 1; game price: expected 15, got 0; Ada: the rule for 15 was never matched (the game never put that option to this seat); Blaise: the rule for 15 was never matched (the game never put that option to this seat); Cleo: the rule for 15 was never matched (the game never put that option to this seat)
- FAIL: Auctioneer seat 2, bids seat1=10 seat2=10 seat3=5: seat 1 wins the tie | rule R10 is broken: When bids tie for highest, the tied seat first in order starting after the auctioneer wins, with the auctioneer last; with the auctioneer at seat 2 and bids seat1=10, seat2=10, seat3=5, seat 1 wins.; seat 1 money: expected 50, got 60; seat 1 owned_blue: expected 1, got 0; seat 2 money: expected 70, got 60; seat 2 owned_blue: expected 0, got 1; game winner_seat: expected 1, got 2; game price: expected 10, got 0; Ada: the rule for 10 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat); Cleo: the rule for 5 was never matched (the game never put that option to this seat)
- FAIL: All bids 0: the auctioneer gets the painting at price 0 | rule R11 is broken: When every bid is 0, the auctioneer wins the painting at price 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Non-auctioneer seat 3 wins at 12 and pays the auctioneer | rule R12 is broken: When a non-auctioneer wins with bid 12, the winner's money falls by 12 and the auctioneer's money rises by 12.; seat 1 money: expected 72, got 60; seat 3 money: expected 48, got 60; seat 3 owned_red: expected 1, got 0; game winner_seat: expected 3, got 1; game price: expected 12, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 12 was never matched (the game never put that option to this seat)
- FAIL: Auctioneer wins at 12 and pays the bank | rule R13 is broken: When the auctioneer wins with bid 12, the auctioneer's money falls by 12 and no other player's money changes.; seat 1 money: expected 48, got 60; game price: expected 12, got 0; Ada: the rule for 12 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Auctioneer buying its own card adds to its owned count | rule R14 is broken: The auction winner's owned count for the current artist rises by 1, including when the winner is the auctioneer.; seat 1 money: expected 55, got 60; Ada: the rule for 5 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Winner and price are announced: seat 3 bids 20 over seat 2's 7 | rule R15 is broken: After an auction, all three bids, the winner and the price are announced to everyone.; seat 1 money: expected 80, got 60; seat 3 money: expected 40, got 60; seat 3 owned_green: expected 1, got 0; game winner_seat: expected 3, got 1; game price: expected 20, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat); Cleo: the rule for 20 was never matched (the game never put that option to this seat)
- FAIL: Last card played: season scores with all hands empty (Blue/Green tie goes to Blue), then the game ends | rule R16 is broken: Season scoring happens when the season-ending card was just played, or when all hands are empty and at least one season count is above 0.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 10 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- FAIL: Three-way tie in season counts: Red first, Blue second, Green unplaced | rule R17 is broken: At scoring, the artist with the highest season count places first, ties broken Red, then Blue, then Green, and its value rises by 20.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- pass: No second place when the other artists have season count 0
- pass: Payout uses the new cumulative value; an unplaced artist pays 0 despite its value
- pass: After scoring, owned and season counts reset and seasons_done rises
- FAIL: Auctioneer passes from 1 to 3, skipping seat 2 whose hand is empty | rule R21 is broken: After each round, the auctioneer passes to the next seat in the order 1->2->3->1, skipping any seat whose hand is empty.; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 0 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)
- pass: Third season scored ends the game; richest seat wins
- pass: Tied for most money at the end: both seats share the win
- FAIL: Money and owned counts are public after a purchase | rule R24 is broken: Money and owned counts are public at all times.; seat 1 money: expected 67, got 60; seat 1 owned_green: expected 0, got 1; seat 2 money: expected 53, got 60; seat 2 owned_green: expected 1, got 0; Ada: the rule for 0 was never matched (the game never put that option to this seat); Blaise: the rule for 7 was never matched (the game never put that option to this seat); Cleo: the rule for 0 was never matched (the game never put that option to this seat)

## Does the file follow the spec's shape? (flags for a person)

- the spec uses `sync` but the game file does not

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 3': 11, 'seat 2': 6, 'seat 1': 3}, 65-117 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 91.7 decisions, prompts of 131 characters on average (longest 164)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- always taking the first option as seat 1 wins 98% of decided matches against random seats
- always taking the first option as seat 2 wins 98% of decided matches against random seats
- random seats: {'seat 3': 29, 'seat 2': 10, 'seat 1': 21}
- always `first@seat1`: won 59, lost 1, drew 0
- always `first@seat2`: won 59, lost 1, drew 0
- always `last@seat1`: won 7, lost 53, drew 0
- always `last@seat2`: won 4, lost 56, drew 0

## Triage (whose problem each failure was)

- round 1: fix_game: The tests match the rules: the auctioneer must pick a reserve from 0 up to their current money. The game never put 0, 25 or 100 to seat 1 as a reserve option, so the reserve fell back to a default and the table `reserve` stayed 0 when it should have been 25. The reserve choice step is missing or wrongly built in the game file; the rules themselves are fine.
- round 1: fix_game: The reserve choice is not built correctly. Seat 1 was never offered a reserve of 0 or 100, and an auctioneer choosing 25 still left the table `reserve` at 0. The card choice worked, so the fault is in the reserve step, not in the rules or the tests.
- round 1: fix_game: The rules are clear and within the platform's capabilities, but the file deals 9 cards each instead of 10. Its trace shows some 'pick' draws (e.g. green) that never reach a hand, so the deal loop loses picks. The R3 to R5 scenarios also show the reserve choice is never put to the auctioneer as options from 0 to their current money.
- round 2: fix_game: The trace shows the file departing from the rules. Seat 1's dealt hand was overwritten after the deal: on roll 6 it got C (2,1,4), then hand_blue went 1->2 and hand_green 4->2. The bid and choice steps also do not offer what R3 and R7 require: no seat was ever offered a bid of 0 or 10, and seat 1 played Green although its rule asked for Red.
- round 2: fix_game: The trace shows the game mishandling hands: after seat 1 played Green, its hand_blue rose from 1 to 2 and hand_green fell from 4 to 2, which breaks R4 (only the chosen artist's count falls, by 1). The bid step also never presents the 0 to money range in a way the tests recognise, so the seats were never offered 0 or 10 as bids.
- round 2: fix_game: The tests' expectations follow R2, R3 and R7. The game never offered the sealed bids as options from 0 up to each bidder's money, so the bid rules 'never matched' for any seat. The deal is also corrupted: seat 1 was dealt C (2/1/4) and then its hand_blue went 1 -> 2, ending at 2/2/1 after one Green play.

## Choices the rules did not make

- Exactly 3 players, suggested 3: The designer fixed the table at 3, and the deal (six permutations of three compositions) only works for 3 seats.
- Tie-break encoded as key = bid*3 + ((3 - offset) mod 3), where offset = (seat - auctioneer + 3) mod 3: This turns the seat-order tie rule into arithmetic: the seat after the auctioneer has priority 2, the next has 1, and the auctioneer has 0. All-zero bids are a separate case that gives the painting to the auctioneer.
- Talk kept as a simultaneous poll broadcast to all, before the bid poll: The source requires it. It also earns its place: players disagree about which artist to push and can bluff about their hidden compositions.
- Helper table attributes season_ended, scoring_now, winner_seat, price, first_artist and second_artist: The flat step list needs flags so that later steps can carry arithmetic 'when' conditions.
- If no seat has cards when the role passes, the auctioneer is left unchanged: The game ends at the check in the same round, so the value never matters.
- Strategy at the table: A thoughtful player infers the others' compositions from what they play and bid, steers seasons toward artists they own, bids up to an artist's likely payout, and sometimes buys their own card so it scores for them.

## Simplifications

- A tie for the most money is reported as a shared win among the tied players, not as a separate draw: The engine ranks by one expression and players level at the top share the win, which corresponds to the source's draw.
- The hand is three counters (hand_red, hand_blue, hand_green) rather than a list of cards: Cards of one artist are identical, so counts carry exactly the same information.

## Encoding attempts

- 1: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (current_artist, first_artist, second_artist) in `your_hand`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
- 2: passed
