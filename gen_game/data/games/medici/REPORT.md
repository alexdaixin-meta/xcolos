# medici: ready for review

Built from the variation **Medici: Sealed Harbour** (design round 1); see VARIATION.md.

## What was changed from the original, and why

- The winning bid is paid in full to the selling (active) player. Only when the seller is forced to keep their own lot is the payment made to the bank. (fixes: P4: Spending is not a trade-off): Overpaying now enriches a rival and underselling now costs the seller, so price matters on both sides.
- The seller sets a reserve price of 1-6. If no bid reaches it, the seller must buy the lot at the reserve, paying the bank, if their ship has room. (fixes: P1: Cheap play is unpunished): This keeps Medici's 'drawer bids last' tension. A low reserve gives the lot away cheaply, and a high reserve risks being stuck paying for it. Setting the reserve is a read of what the others will pay.
- Each empty ship slot at the end of a day costs 2 florins. (fixes: P1: Cheap play is unpunished): A player who never buys pays 6 florins a day and wins no ship prize, so pure passivity loses.
- Bids are capped at 10. The money is rescaled to a 25-florin start, ship prizes of 12/6/0 per day, and a patron bonus of 3 per card. (fixes: P5: Prizes are out of scale with the starting florins): A card's worth to a buyer is roughly 3-6 florins. The cap limits the damage of random play, and paying 10 every time is clearly ruinous. Prizes are large enough that buying well beats not buying, but small enough that overpaying does not.
- Bids are sealed and simultaneous from the two non-sellers. Ties go to the tied bidder sitting first clockwise after the seller. The seller seat rotates every round, and day d starts with seat d. (fixes: P3: Seat edge): This removes the clockwise once-around order advantage. Across the 3 days every seat sells in every position exactly once and is 'first after the seller' equally often.
- Always-maximum play is checked against the new economy. A player paying 10 for 9 lots spends about 90 florins, and the rival sellers pocket it. (fixes: P2: Maximum bidding is always ruinous): This confirms that extreme bidding still loses but is no longer the only losing policy. Moderate overbidding for a needed card can now pay, through ship prizes and the patron bonus.
- Each lot is one drawn card (commodity and value 1-5). Each day the 20-card deck is reshuffled and 6 cards are auctioned. Ship capacity is 3. Majority tracks are replaced by a secret patron commodity per player. (fixes: P6: Platform limits): This uses one random draw per round and about 18 attributes, while keeping auctions, ship capacity, ship-value prizes and commodity-based scoring.
- Each player is secretly dealt a distinct patron commodity, and every patron card in their ship pays 3 florins at day end. A short simultaneous message phase is held before each auction. (fixes: P7: Little to infer about rivals' preferences): The same card is worth different amounts to different players, so bids and claims reveal or disguise types. Players must infer who will contest which card, and can bluff interest to drive up prices or feign disinterest to buy cheaply.

Objective: After the end-of-day scoring of day 3, the player with the most florins wins. If two or three players tie for most, it is a draw between them.

## The critic (1 review(s) before the rules went to a coder)

- balanced: pass. VALUE OF ONE CARD to a buyer = 2 (fills a slot that would otherwise cost 2) + 3 if it is the buyer's patron + its effect on the ship prize (12/6/0). Each day has 6 lots and 9 slots, so at least 3 slots stay empty. Ship size and the 6 lots make cards scarce: a player can get a third card only by outb
- playable: pass. RULES COMPLETE.
- Bid ranges, reserve range and the full-ship rule (must bid 0) are given.
- Case A (a bid reaches the reserve) and its tie-break are given.
- Case B is given, including a full ship (card discarded) and a broke seller (pays all).
- Ship-prize ties with empty-ship exclusion are given.
- reasoning_over_luck: pass. WHAT IS LUCK.
- Which 6 of the 20 cards appear each day.
- Which seller draws a high card.
- The random patron deal.

WHY SKILL STILL DECIDES.
- Every card goes to a sealed auction, so a lucky draw is priced by competition. The seller of a 5-value card mostly profits through bids or a well-judged re

## Complexity

- steps_per_round: designed 14, built 12, limit 20
- choice_steps_per_round: designed 3, built 3, limit 4
- attributes: designed 19, built 45, limit 20 (built: 80)
- hidden_elements: designed 2, built 8, limit 3
- random_draws_per_round: designed 1, built -, limit 1
- rounds: designed 18, built -, limit 40

## Fidelity to the rules (tier 1: independent tests written from the spec alone; they do not decide whether the file works)

- pass: Each seat starts with 25 florins: after seller 1 buys in at reserve 3, seat 1 has 22 and the others still 25
- pass: Three patrons are dealt and one commodity stays in the pool (which one is chance)
- pass: Patron deal leaves one commodity undealt and play goes on normally
- pass: Start of day 2 refills the deck to 20 and empties stale ships
- pass: Day 3 starts with seat 3 as seller: seat 3 sets the reserve and buys it in when nobody bids
- pass: Third round of day 2 (round 9) has seat 1 as seller
- pass: First five rounds of day 1 have sellers 1,2,3,1,2: each seller buys in at reserve 1
- pass: Round 1 draws one lot from the fresh 20-card deck
- pass: Talk step runs and the round continues to resolution
- pass: Reserve ranges 1 to 6: 6 is accepted, 0 and 7 are not offered
- pass: Bids are capped at min(10, florins): seat 2 with 4 florins bids up to 4
- pass: Full-ship bidder cannot win: seat 3's bid meets the reserve and seat 3 loads the lot
- pass: Reserve 4, bids 5 and 3: the 5-bidder pays 5 to the seller
- pass: Seller 3, tied bids of 6: seat 1 wins and pays 6
- pass: No bid reaches reserve 5: seller loads the lot and pays 5 to the bank
- pass: Seller with 3 florins and reserve 6 pays all 3 and still loads the lot
- pass: Seller's ship full and no bid reaches the reserve: lot discarded, nobody pays
- pass: Round resolves with tied bids of 3 over reserve 2: seat 2 (first after seller 1) pays 3
- pass: Full ship takes no more cards: other bid misses reserve 5, seller 2 buys in, seat 1 unchanged
- pass: Day end: ship values 12/9/6 get prizes 12/6/0
- pass: Two tied for first with 12 split 18: 9 each; third gets 0
- pass: Three tied ship values split 18: 6 each
- pass: Two tied for second split 6: 3 each; first gets 12
- pass: Empty ship takes no place: the 9 and 6 ships get 12 and 6, empty ship pays 6 penalty
- pass: Patron bonus: two patron cards in ship add 6
- pass: Empty-slot penalty 2 per slot, floored at 0
- pass: After day-end scoring all ships are empty and day 2 begins
- pass: Round 18 day-end scoring ends the game: seat 1 wins with 37
- pass: Round 18 ends with seats 1 and 2 tied on 34: shared win

## Does the file follow the spec's shape? (flags for a person)

- yes

## Works on the platform (tier 0: it loads, ends, replays identically, and every attribute it declares is updated)

- passed: 20 random matches at tables [3], results {'seat 2': 4, 'seat 1': 9, 'seat 3': 6, 'seats 2 and 3': 1}, 103-108 turns

## Play-trace checks (random matches: text that was never filled in, empty or repeated announcements, one-option questions)

- clean
- cost of a match: 106.0 decisions, prompts of 156 characters on average (longest 216)

## Balance (informational: a thoughtless policy that always wins, or luck deciding everything)

- no flags
- random seats: {'seat 2': 12, 'seat 1': 20, 'seat 3': 25, 'seats 2 and 3': 1, 'seats 1 and 2': 1, 'seats 1 and 3': 1}
- always `first@seat1`: won 43, lost 17, drew 0
- always `first@seat2`: won 40, lost 19, drew 1
- always `last@seat1`: won 0, lost 60, drew 0
- always `last@seat2`: won 0, lost 60, drew 0

## Choices the rules did not make

- 3 players, min = max = suggested = 3: The designer fixed 3. The seller order, two sales each per day, two bidders per lot and the 12/6 two-place prize are all built for exactly 3 seats.
- Keep the simultaneous talk as a poll with broadcast: The source requires it. Talk earns its place because patrons are secret and players compete for the same lots, so bluffing about which commodity you want, or talking down a lot's value to the seller, can mislead rivals.
- Strategy at this table: A thoughtful player prices reserves to extract bids without being forced to buy junk, infers rivals' patrons from what they bid on, bids to deny a rival's ship prize, and avoids empty-slot penalties. A thoughtless one bids face value.
- Reading of the empty-ship prize rule: Players with empty ships are excluded from ranking entirely, so places are counted only among non-empty ships. The next non-empty ship can therefore take a prize.
- Day-end order: ship prize, patron bonus, then penalty with the floor at 0: The source lists them in this order and applies the floor only to the penalty.
- In case B, the seller loading their own patron commodity counts for the patron bonus: The patron bonus counts every patron card in the ship, however it was loaded.
- Reserve asked of the seller with a single-player ask: Only one seat answers, so ask and poll behave the same. The answer is kept in the seller's ally-visible reserve.

## Simplifications

- Shuffling and drawing the top card is done as drawing a random card from the deck list: Drawing at random is how the engine shuffles. The odds are the same.
- The bank is not tracked as an attribute: It has unlimited funds in the rules. Payments to and from it only change player florins.
- Ship contents are public lists: Every lot and buyer is announced to everyone, so the ships are already public information.
