# Variation: Modern Art: Four Seasons

Four players auction paintings from four artists in 16 sealed-bid auctions over 4 seasons. Auctioneer duty rotates evenly. At each season's end every player secretly nominates an artist to boost. Artist values accumulate, prices are private, and the richest eligible player wins.

Players: 4 to 4, best with 4

## Review of the original

Modern Art is a 3-5 player auction game. Players take turns selling painting cards from five artists under several auction formats. Artists that are played most often in a round pay their owners values that build up over four rounds, and the player with the most money at the end wins.

- **non_degenerate**: good. Never bidding leaves you with only auctioneer income. Overbidding loses money. Prices depend on rankings that the players themselves shape. In the original, seat order matters a little, because the round-ending player gets a timing edge. In the previously tested 12-auction variation seat order mattered a lot: seats 3 and 4 had about 7.5 more expected auctioneer income in the high-value season, and seat 4 alone chose the final Season 2 ranking with full information.
- **skill_sensitive**: good. The deal decides which artists you can push, but valuation, timing of the round-ending card, and pricing your own auctions dominate. Experienced players reliably beat novices.
- **headroom**: good. Valuing a painting needs a forecast of the rankings, of opponents' hands and of their incentives. There is no closed-form solution. A weak player still earns from selling cards.
- **reasoning_dependent**: good. Hands are hidden and future rankings are uncertain. You must infer which artists rivals hold and will push, and plan across rounds because values accumulate. In the previous variation, money was claimed as hidden but was fully computable from announced prices.
- **verifiable**: good. Rankings, values, payouts and the winner are pure arithmetic. The previous variation's bid tie-break said 'clockwise from the auctioneer's left' without defining the direction in seat numbers, so the same tie could be resolved differently.
- **fits_platform**: weak. Open ascending and once-around auctions need long sequential bidding chains. Five auction types and five artists push the step and attribute budgets. A round of variable length that ends on the fifth card is awkward. The sealed-bid core fits well.

## Problems

- P1: Open, once-around, fixed-price and double auctions need many sequential steps and conditional blocks, which the engine cannot branch between.
- P2: Seat asymmetry in the previous variation. Some seats auctioned twice in the low-value season and others twice in the high-value season, an edge of about 7.5 money.
- P3: Full-information kingmaker. The auctioneer of a season's last card alone fixes that season's ranking before bidding. A simple rotation cannot remove this edge, because seasons differ in value and the seat holding the final card of the richest season gains most.
- P4: The bid tie-break was undefined: 'clockwise' and 'left' were never mapped to seat numbers.
- P5: Money was claimed as hidden but was computable from announced prices, so the claimed hidden element was false.
- P6: Fixed artist tie priority (Red > Blue > Green > Yellow) in every season permanently favours holders of Red.

## Changes

- Use one auction type only: a simultaneous sealed first-price bid in which every player, including the auctioneer, bids. (fixes: P1): One poll per auction fits the engine and keeps valuation as the core skill.
- Use 16 auctions in 4 seasons of 4. The auctioneer order rotates each season: S1 seats 1,2,3,4; S2 seats 2,3,4,1; S3 seats 3,4,1,2; S4 seats 4,1,2,3. Deal 5 cards each from 24, leaving each player one spare card. (fixes: P2): Every seat auctions exactly once in every value tier, so expected auctioneer income is equal.
- Add a season-end nomination. After the 4th auction of a season, every player secretly and simultaneously names one artist, and each nomination adds 1 to that artist's season count before ranking. The 4 nominations weigh as much as the 4 cards played that season. (fixes: P3): The last card no longer settles the ranking. The last painting is bought without knowing the final ranking. The power to decide the ranking is shared by all four players at once, so they must predict each other's nominations.
- Make the bid tie-break explicit. Tied highest bidders are ordered auctioneer+1, auctioneer+2, auctioneer+3 (seat numbers, with 5 wrapping to 1, 6 to 2, 7 to 3), with the auctioneer last. (fixes: P4): This gives an arithmetic, unambiguous result. It rotates with the auctioneer, so it is symmetric over a season.
- After each sale, announce only the artist and the buyer. The price is told privately to the buyer and the auctioneer only. (fixes: P5): Money becomes genuinely hidden, so players must infer rivals' wealth and standing from their behaviour and their talk.
- Break artist ranking ties by higher cumulative value, then by a priority that rotates each season (S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G). (fixes: P6): No artist is favoured over the whole game, and established artists keep a natural edge.
- Starting money becomes 100, and a player must buy at least 3 paintings to be eligible to win. (fixes: P1): Players can afford Season 3-4 prices, and the 'never buy' policy stays losing over 16 auctions.

## Kept from the original

- Players auction paintings from their own hands, and the auctioneer profits from others' purchases.
- Artist popularity is set by how often an artist appears in a season. Only the top three pay out.
- Values accumulate over seasons, so a repeatedly popular artist becomes very valuable.
- Paintings are discarded after each season payout.
- The winner is the player with the most money, decided by arithmetic.
- Hidden hands and hidden money.

## The variation's rules

SETUP.
- Four players sit in seats 1-4.
- The deck has 24 cards: 6 each of Red, Blue, Green and Yellow.
- Shuffle the deck and deal each player 5 cards as a hidden hand. The remaining 4 cards are set aside unseen.
- Each player starts with 100 money. Money is hidden; each player sees only their own.
- Every artist starts with cumulative value 0 and season count 0.

STRUCTURE.
- There are 16 auctions in 4 seasons. Season s contains auctions 4s-3 to 4s.
- In auction k of season s, where k is 1 to 4 within the season, the auctioneer is seat ((s + k - 2) mod 4) + 1.
- This gives the order: Season 1: 1,2,3,4. Season 2: 2,3,4,1. Season 3: 3,4,1,2. Season 4: 4,1,2,3.
- Each player is auctioneer exactly once per season (4 times in all) and ends with 1 unused card.

EACH AUCTION.
(1) The auctioneer privately chooses one card from their hand and removes it from the hand. Its artist is announced to all.
(2) That artist's season count rises by 1, whether or not the painting sells.
(3) Talk: every player writes one short message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding.
(4) Every player, including the auctioneer, submits a sealed bid at the same time. A bid is a whole number from 0 to the bidder's current money.
(5) Resolution.
  - If the highest bid is 0, the painting is unsold and discarded.
  - Otherwise the highest bidder buys it. If several players tie for highest, the buyer is the first of them in the order: seat (A mod 4)+1, seat ((A+1) mod 4)+1, seat ((A+2) mod 4)+1, then the auctioneer, where A is the auctioneer's seat.
  - The buyer pays the bid. If the buyer is not the auctioneer, the auctioneer receives the bid divided by 2, rounded down, and the rest goes to the bank. If the auctioneer buys, the whole bid goes to the bank.
  - The painting joins the buyer's collection, and the buyer's paintings-bought count rises by 1.
(6) Announcement.
  - Everyone is told the artist and the buyer, or that the painting went unsold.
  - The price is told privately to the buyer and to the auctioneer only.
  - Losing bids are never revealed.

SEASON END (after the 4th auction of each season).
(a) Nomination. Every player at the same time secretly names one of the four artists. Each nomination adds 1 to that artist's season count. All nominations are then revealed.
(b) Ranking. Rank the artists by season count, higher first. Break ties first by higher cumulative value, then by this season's priority: Season 1 R>B>G>Y; Season 2 B>G>Y>R; Season 3 G>Y>R>B; Season 4 Y>R>B>G. An artist with season count 0 cannot place.
(c) Values. Add 30 to the cumulative value of the 1st artist, 20 to the 2nd and 10 to the 3rd. The 4th artist gains nothing.
(d) Payout. For each painting a player owns of an artist that placed in the top three this season, the bank pays that player the artist's cumulative value (after step c). Paintings of an artist that did not place pay 0. Each player is told their own payout privately. The artists' cumulative values are public.
(e) All owned paintings are discarded, and all season counts reset to 0.

GAME END. The game ends after the Season 4 payout. Final money totals are then revealed.

Objective: Only players who bought at least 3 paintings during the game are eligible. Among eligible players, the one with the most money wins. If two or more eligible players tie for most money, the game is a draw. If no player is eligible, the game is a draw.

Expected effect: Every seat now holds the same opportunities in every value tier. The season's last card is one count among eight, and the final say is a simultaneous nomination by all four players, so no seat has a kingmaker edge.

Players must value paintings under two kinds of uncertainty:
- which artists rivals still hold, inferred from the cards they have played and from their hands;
- how rivals will nominate, predictable from what each has bought.

Hidden prices make standings uncertain, so late-game bidding requires estimating rivals' money from their behaviour.

Talk passes both tests. Players disagree because the auctioneer wants high prices, bidders want low ones, and owners want different artists promoted. A player who follows a call such as 'let's all nominate Blue' or 'nobody bid above 20' may help the speaker's collection or sale at their own expense. Talk lets players propose nomination alliances, bluff about their hands and test promises over seasons.

Thoughtless policies all lose:
- Bid 0: never eligible, so it loses whenever anyone buys 3 paintings.
- Bid all money: overpays by tens in Season 1 and is then broke.
- Fixed bid: buys only overpriced or undervalued junk, depending on the other bids.
- Always play your first card, or always nominate Red: gives up control of the rankings.

The game is not about cooperation, so a highest-total winner does not cause endgame unraveling.

## Complexity (the designer's count, against the limits)

- steps_per_round: 15 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 16 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
