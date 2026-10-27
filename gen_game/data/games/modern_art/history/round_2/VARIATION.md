# Variation: Modern Art: Private Collections

Four dealers each hold five hidden paintings. In turn each chooses one to sell by sealed bid, and the artists whose works reach the market most become valuable. Players push the artists they own, read opponents' holdings from what they sell and how they bid, and bluff in open talk.

Players: 4 to 4, best with 4

## Review of the original

Modern Art is a 3–5 player auction game. Players sell painting cards from hidden hands using several auction types, and an artist's value depends on how many of that artist's cards are played. The auctioneer's choice of which card to sell is the main lever on the market, and the richest player after four seasons wins.

- **non_degenerate**: bad. In the previous variation the bid cap of 50 sat below the value of every top-two painting (60–100), so bidding 50 weakly dominated for every non-auctioneer. The fixed tie-break (earliest seat after the auctioneer) then decided who got every valuable painting, which handed seats 2, 3, 4 and 1 fixed rounds. No literal never-lose policy existed: always-50 loses to sensible play by overpaying for rank-4/5 cards, and always-0 never gains surplus. But allocation was decided by seat order, not by choices.
- **skill_sensitive**: bad. Market counts rose on every random draw regardless of play, so nobody could influence values. Under good play the outcome hinged on whether the deck put strong cards into your three tie-break rounds, a swing of about 90–150 points. A good player only gained by avoiding late overpays.
- **headroom**: weak. Once 'bid the cap on anything plausibly in the top two' is found, little remains to improve. The hot-artist bonus (+20, about +4 per painting on average) was too small to reward inference, and the four clues together revealed it exactly.
- **reasoning_dependent**: weak. There was hidden information (deck order, hot artist), but it could only be estimated, not acted on. There was no plan to make, since nobody controlled which cards entered the market, and bluffing in talk changed little under a capped bid and a fixed tie-break. The original's real reasoning, choosing which card to sell and reading opponents' hands from their sales, was missing.
- **verifiable**: good. Money, market counts, ranks, painting values and scores are all arithmetic on tracked numbers. No judge is needed.
- **fits_platform**: good. Turn-based sealed bids and text talk with no board. It sat within limits, though the attribute count had to be stated carefully.

## Problems

- P1: Bid cap below painting value. A cap of 50 under top-painting values of 60–100 makes bidding the cap dominant and removes price discovery.
- P2: Seat tie-break lottery. Ties at the cap went to the fixed seat after the auctioneer, so allocation of valuable paintings was decided by seat and deck order, not skill.
- P3: No player control of the market. Counts rose on random draws, removing the original game's central lever (the auctioneer choosing which artist to push) and leaving nothing to plan.
- P4: Weak and fully revealable hidden information. The hot bonus was small and the four clues jointly identified it, so inference and bluffing barely mattered.
- P5: Last-auctioneer advantage. With a fixed start, the same seat always auctions round 12 with an almost fully known market, a built-in seat edge.
- P6: Rank-5 values and the 80-point top value made weak paintings pure traps and the top artist a jackpot, amplifying luck.

## Changes

- Deal all 20 cards out, 5 hidden cards to each player. Each round the auctioneer chooses which card from their own hand to put up for sale. Only auctioned cards raise market counts, and each player auctions exactly 3 of their 5 cards, so 8 cards never reach the market. (fixes: P3): This restores the original's core decision of which artist to push, and makes hidden hands the hidden state to infer: what others still hold and what they will play.
- Make bids any whole number from 0 up to the bidder's current money, with no fixed cap. (fixes: P1): Prices are found by bidding, and no cap sits below value. Whole-number bids make exact ties rare.
- Resolve ties among highest non-auctioneer bids by giving the painting to the tied player with the least current money. If they are still tied, the painting is discarded unsold and nobody pays, though the market count still rises. (fixes: P2): No seat is favoured, and a full tie benefits no one, which discourages tying on purpose.
- Replace the hot artist and its clues with hidden hands as the single strong hidden element. Talk is about holdings and intentions ('I am sitting on C, it will top the market'). (fixes: P4): The hidden hand is the original game's real hidden information, and it drives both planning and bluffing. One strong hidden element is preferred over a weak extra one, and dropping the clues keeps the game inside the attribute limit.
- Draw the round-1 auctioneer at random at setup. Auctioneers then rotate clockwise, so each seat auctions exactly 3 times. (fixes: P5): The seat that makes the last, best-informed sale is no longer fixed. It is also no longer known before the game starts.
- Set painting values to 60 for an artist ranked 1st, 40 for 2nd, 20 for 3rd, and 0 for 4th and 5th, with starting money of 100. Rank ties are broken alphabetically, which is known in advance. (fixes: P6): This follows the original's top-three payout and narrows the top-artist jackpot. A known tie rule is something players can plan around rather than luck.

## Kept from the original

- Auctioneer sells a card from a hidden hand; the buyer pays the auctioneer, or the bank if the auctioneer buys their own card.
- Artist value is set by how many of that artist's cards were played, with the top three artists paying.
- The sealed-bid auction type from the original.
- If nobody bids, the auctioneer keeps the painting for free (the original open-auction rule).
- The richest player at the end wins, counting money plus painting value.

## The variation's rules

SETUP
- There are exactly 4 players, in seats 1 to 4.
- There are five artists: A, B, C, D and E. The deck has 20 cards, 4 of each artist.
- Shuffle the deck and deal 5 cards to each player. Each hand is private: only its owner sees it.
- Each player starts with 100 money. Money is public.
- Each artist has a MARKET COUNT, starting at 0. Market counts are public.
- Each player has a COLLECTION, starting empty. Collections are public.
- Draw one seat at random to be the auctioneer in round 1.

EACH ROUND (12 rounds)
1. OFFER. The auctioneer chooses one card from their own hand. It is removed from the hand and revealed as the painting for sale. That artist's market count rises by 1, whether or not the painting sells.
2. TALK. Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages bind nobody, and players may lie.
3. BID. All 4 players, including the auctioneer, secretly and simultaneously choose a bid. A bid is any whole number from 0 up to the player's current money. A bid above the player's money counts as all of their money.
4. RESOLVE.
   a. If every bid is 0, the auctioneer keeps the painting for free.
   b. Otherwise the highest bid wins.
   c. The auctioneer wins only if their bid is strictly higher than every other bid. If the auctioneer wins, they pay their bid to the bank.
   d. If one non-auctioneer has the highest bid, that player wins and pays their bid to the auctioneer.
   e. If two or more non-auctioneers tie for the highest bid (and the auctioneer did not bid more), the tied player with the least current money wins and pays their bid to the auctioneer.
   f. If the tied players also have equal money, the painting is discarded unsold and nobody pays. The market count still keeps its +1.
   g. A won painting goes into the winner's collection and stays there to the end.
5. REVEAL. All four bids, the winner (if any) and the price paid are announced.
6. ROTATE. The auctioneer role passes clockwise to the next seat, so each seat is auctioneer in exactly 3 rounds.
- Each player auctions 3 of their 5 cards. Their remaining 2 cards are never played and never count.

END OF GAME (after round 12)
1. Rank the five artists by market count, highest first. Ties are broken alphabetically: A above B above C above D above E.
2. Each painting in a collection is worth: 60 if its artist ranks 1st, 40 if 2nd, 20 if 3rd, and 0 if 4th or 5th.
3. Each player's SCORE is their money plus the total value of their collection.

Objective: After round 12, the player with the highest score (money plus collection value) wins. If two or more players tie for the highest score, the game is a draw between them.

Expected effect: Auctioneers choose sales that push artists they and their allies of the moment already own, or that starve a rival's collection. Buyers must estimate final ranks from public counts, their own hand and what others' choices reveal about their hands. They then bid up to their estimate of value, not to a cap, so price discovery decides who buys. Holding back cards (only 3 of 5 are played) creates planning over several rounds and bluffing. Talk passes both tests. Players disagree because the seller wants high prices while buyers want low ones, and each player wants the artists in their own collection and hand to rank top. A player who believes 'C will win, I hold three' may overpay for C when the speaker actually intends to sell D, so following a claim can lose. Thoughtless policies lose: always-0 gains no surplus and falls behind; always bidding all its money spends 100 on one painting worth at most 60; always selling a random card wastes the lever. Seat order no longer decides allocation, and the last auction belongs to a randomly drawn seat.

## Complexity (the designer's count, against the limits)

- steps_per_round: 13 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 12 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
