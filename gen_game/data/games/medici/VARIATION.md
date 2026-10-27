# Variation: Medici: Sealed Harbour

Three merchants take turns selling single commodity cards over 3 days of 6 auctions each. The seller sets a reserve, the other two bid sealed, the money goes to the seller, and an unsold lot is forced back on the seller at the reserve. Ships hold 3 cards a day. Ship-value prizes, a secret patron commodity bonus and penalties for empty space decide who ends richest.

Players: 3 to 3, best with 3

## Review of the original

Medici is a 2-6 player auction game played over 3 days. Players take turns drawing lots of 1-3 commodity cards and auctioning them with once-around bidding, the drawer bidding last. Each player loads purchases onto a ship of limited size, and florins are awarded each day for the most valuable ships and for majorities on commodity tracks. Most florins after day 3 wins.

- **non_degenerate**: bad. In the tested previous variation, always taking the first option won 48 of 60 matches from seat 1 and 51 of 60 from seat 2. Always taking the last option lost all 60 from both seats. Against random seats, seat 2 won 23 matches outright, against 15-16 for the other seats. So a fixed menu position and a seat both carried an edge. The causes were cheap bidding being unpunished, prizes too large relative to prices, payments vanishing into the bank, and a fixed clockwise bid order.
- **skill_sensitive**: weak. Valuing a lot against ship space and majorities is real skill in the original. In the tested build, though, a thoughtless low-bid policy beat random play 80% of the time, which shows the payoff structure rewarded passivity rather than judgement.
- **headroom**: weak. Only the extremes were tested: minimum play almost always won and maximum play always lost. Little of the space between them rewarded refinement, because the best policy was a corner of the menu.
- **reasoning_dependent**: good. Hidden deck order, rivals' remaining ship space and their likely valuations all have to be inferred. Bidding last as the drawer rewards reading what the others will pay.
- **verifiable**: good. Ship values, majorities and florin totals are all arithmetic.
- **fits_platform**: weak. The original is turn-based and text-only. However, drawing 1-3 cards stop-at-will needs several random draws per turn, once-around sequential bidding creates seat order effects, and per-commodity majority tracks for many players exceed the attribute budget.

## Problems

- P1: Cheap play is unpunished. Bidding minimum or passing never costs anything, so 'first option' wins about 80% of matches.
- P2: Maximum bidding is always ruinous. Prices go to the bank and prizes cannot recover them, so 'last option' loses 100% of matches.
- P3: Seat edge. The fixed clockwise once-around bid order and the start-of-day rotation favoured seat 2 (23 outright wins against random seats, versus 15-16).
- P4: Spending is not a trade-off. Payments disappear into the bank, so there is no tension between the seller's price and the buyer's cost.
- P5: Prizes are out of scale with the starting florins, so the scoring does not reward a deliberate valuation over a fixed menu position.
- P6: Platform limits. Stop-at-will multi-card draws need several random draws per round, and per-commodity majority tracks for every player exceed the attribute budget.
- P7: Little to infer about rivals' preferences. Everyone values a card the same way, so opponent modelling reduces to counting ship space.

## Changes

- The winning bid is paid in full to the selling (active) player. Only when the seller is forced to keep their own lot is the payment made to the bank. (fixes: P4: Spending is not a trade-off): Overpaying now enriches a rival and underselling now costs the seller, so price matters on both sides.
- The seller sets a reserve price of 1-6. If no bid reaches it, the seller must buy the lot at the reserve, paying the bank, if their ship has room. (fixes: P1: Cheap play is unpunished): This keeps Medici's 'drawer bids last' tension. A low reserve gives the lot away cheaply, and a high reserve risks being stuck paying for it. Setting the reserve is a read of what the others will pay.
- Each empty ship slot at the end of a day costs 2 florins. (fixes: P1: Cheap play is unpunished): A player who never buys pays 6 florins a day and wins no ship prize, so pure passivity loses.
- Bids are capped at 10. The money is rescaled to a 25-florin start, ship prizes of 12/6/0 per day, and a patron bonus of 3 per card. (fixes: P5: Prizes are out of scale with the starting florins): A card's worth to a buyer is roughly 3-6 florins. The cap limits the damage of random play, and paying 10 every time is clearly ruinous. Prizes are large enough that buying well beats not buying, but small enough that overpaying does not.
- Bids are sealed and simultaneous from the two non-sellers. Ties go to the tied bidder sitting first clockwise after the seller. The seller seat rotates every round, and day d starts with seat d. (fixes: P3: Seat edge): This removes the clockwise once-around order advantage. Across the 3 days every seat sells in every position exactly once and is 'first after the seller' equally often.
- Always-maximum play is checked against the new economy. A player paying 10 for 9 lots spends about 90 florins, and the rival sellers pocket it. (fixes: P2: Maximum bidding is always ruinous): This confirms that extreme bidding still loses but is no longer the only losing policy. Moderate overbidding for a needed card can now pay, through ship prizes and the patron bonus.
- Each lot is one drawn card (commodity and value 1-5). Each day the 20-card deck is reshuffled and 6 cards are auctioned. Ship capacity is 3. Majority tracks are replaced by a secret patron commodity per player. (fixes: P6: Platform limits): This uses one random draw per round and about 18 attributes, while keeping auctions, ship capacity, ship-value prizes and commodity-based scoring.
- Each player is secretly dealt a distinct patron commodity, and every patron card in their ship pays 3 florins at day end. A short simultaneous message phase is held before each auction. (fixes: P7: Little to infer about rivals' preferences): The same card is worth different amounts to different players, so bids and claims reveal or disguise types. Players must infer who will contest which card, and can bluff interest to drive up prices or feign disinterest to buy cheaply.

## Kept from the original

- 3 days, with ships of limited capacity filled through auctions
- The active player draws and offers a lot, and effectively bids last through the reserve
- Prizes each day for the highest and second-highest ship value
- Commodity identity matters for scoring (now through the secret patron instead of tracks)
- Most florins after day 3 wins

## The variation's rules

SETUP
- Players and money: 3 players in seats 1, 2 and 3. Each starts with 25 florins. Florin totals are public.
- Deck: 20 cards, one of each combination of 4 commodities (Grain, Cloth, Spice, Dye) and values 1, 2, 3, 4 and 5.
- Patron commodity: at the start of the game, 3 of the 4 commodities are dealt at random, one to each player, as that player's secret patron commodity. Each player sees only their own. The fourth commodity is nobody's patron.

STRUCTURE
- Days and rounds: the game has 3 days of 6 rounds each, 18 rounds in all.
- Start of day: the full 20-card deck is shuffled and every ship is empty. Each ship holds at most 3 cards per day.
- Seller order: day 1 begins with seat 1 as seller, day 2 with seat 2, day 3 with seat 3. The seller then moves to the next seat each round (1, 2, 3, 1, ...). Each player sells exactly twice per day.

EACH ROUND
1. Draw: the top card of the deck is revealed to everyone. This card is the lot.
2. Talk: all three players write one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Reserve: the seller secretly chooses a reserve price, a whole number from 1 to 6.
4. Bids: at the same moment, the two non-sellers each choose a sealed bid, a whole number from 0 to 10, no more than their current florins.
   - A bid of 0 means pass.
   - A player whose ship already holds 3 cards must bid 0.
5. Resolve, case A (a bid reaches the reserve): the highest bid wins. If the two bids tie, the bidder sitting first clockwise after the seller wins. The winner pays their bid to the seller and loads the card.
6. Resolve, case B (no bid reaches the reserve):
   - If the seller's ship has room, the seller must load the card and pay the reserve to the bank.
   - If the seller's ship is full, the card is discarded.
   - If the seller has fewer florins than the reserve, they pay all they have.
7. Reveal: the reserve, both bids, the buyer and the price are announced to everyone.

END OF EACH DAY (after round 6, 12 and 18)
- Ship prize: each player's ship value is the sum of the card values in their ship. Highest ship value receives 12 florins and second highest receives 6.
  - If two or more players tie, they add together the prizes for the places they occupy and split the sum equally, rounded down.
  - A player with an empty ship never receives a prize.
- Patron bonus: each player receives 3 florins for each card of their own patron commodity in their ship.
- Empty-slot penalty: each player pays the bank 2 florins for each empty slot in their ship (0 to 3 slots). Florins cannot drop below 0.
- Reset: ships are emptied and the next day begins.

Objective: After the end-of-day scoring of day 3, the player with the most florins wins. If two or three players tie for most, it is a draw between them.

Expected effect: Simple policies now lose. A player who always sets reserve 1 and passes sells cheaply, never wins a prize and pays 18 in empty-slot penalties, falling behind any player who buys. A player who always reserves 6 and bids 10 hands about 90 florins to rivals and is forced to buy their own lots at 6. A random player overpays to the sellers. Seat order is neutralised by sealed simultaneous bids and the rotation of starting sellers.

Good play means pricing each card from its value, its fit with your patron and the space left in all ships, and setting reserves that extract the most a rival will pay without leaving you stuck. Late-day lots matter, because full ships remove bidders and the empty-slot penalty pressures players with space.

The secret patron gives each card a different worth to each player. Bids and messages leak information, and bluffing interest raises a rival's price. Talk passes both tests because interests conflict: only one player wins and every payment goes to a rival. A player who follows a proposal like 'you take this Spice, I'll take the next card' can end with a weaker ship or pay a rival seller more than the card is worth to them. Likewise, believing 'I don't care about Dye' can let the speaker take their patron card cheaply.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 18 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
