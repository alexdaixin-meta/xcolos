# Variation: Modern Art: Sealed Season

An auction game for 3 to 4 players over 3 seasons. Players take turns auctioning paintings by four artists. The auctioneer announces a reserve price, and the others bid sealed and simultaneously. At each season's end, the two most-sold artists pay their owners a value that accumulates over seasons. The richest player wins.

Players: 3 to 4, best with 4

## Review of the original

Modern Art is an auction game for 3 to 5 players. Each player takes turns auctioning painting cards by five artists, using five different auction formats. At the end of each of four seasons, artists are ranked by how many of their paintings were sold, and the paintings of the top artists pay their owners cumulative values. The richest player after four seasons wins.

- **non_degenerate**: good. Always bidding high goes broke by overpaying. Never bidding leaves you selling only your own hand and lets rivals buy cheap paintings. The auctioneer seat rotates, so no seat has a lasting edge. Which artist is auctioned changes which artists pay out.
- **skill_sensitive**: good. Valuing a painting depends on the artist counts on the table, the cumulative markers, guesses about what others hold, and when the season will end. Strong players reliably outbid weak ones at the right moments. The deal matters, but every card is either sold for money or bought at a price, so the deal is largely corrected through play.
- **headroom**: good. Weak players still collect auction income from their own sales. Strong players can keep refining valuation, timing the season end and reading other players' hands. The game is not solved.
- **reasoning_dependent**: good. Hands and money are hidden. Values depend on future plays nobody controls alone. Sealed bids and once-around bids require predicting rivals' valuations.
- **verifiable**: good. Payments, rankings, marker values and final money are all arithmetic.
- **fits_platform**: weak. Open ascending auctions and first-to-accept fixed price are real-time or long sequential loops. Five auction types plus the double auction create branching blocks of steps the engine cannot select between. The value markers sit on a board track, though that track is only numbers. Four seasons with 5 artists and up to 5 players is long.

## Problems

- The open ascending auction is effectively real-time or an unbounded loop of turns, which the engine cannot run.
- Five auction types each need their own block of steps, chosen per card. The engine has a flat step list with no conditional subsequences.
- The double auction and first-to-accept fixed price add long sequential chains for little extra reasoning.
- Four seasons, five artists and up to 5 players make the game long and push past the attribute and step limits.
- The rules leave money hidden but do not say what bid information becomes public. Inference needs a clear information rule.

## Changes

- Every auction uses one format. The auctioneer secretly picks a card and announces a public reserve price. Then all other players submit sealed bids at the same moment. The highest bid at or above the reserve buys the card and pays the auctioneer. If nobody meets the reserve, the auctioneer must buy the card at the reserve, paying the bank. (fixes: The open ascending auction is effectively real-time or an unbounded loop of turns, which the engine cannot run.): Sealed simultaneous bids are a single poll. The public reserve with forced purchase keeps the fixed-price risk and tension of the original, all inside one flat step list.
- Drop the per-card auction icons and the double auction. (fixes: Five auction types each need their own block of steps, chosen per card. The engine has a flat step list with no conditional subsequences.): This removes the branching blocks and long chains. The bluffing and valuation that made those formats interesting survive through the reserve and the sealed bids.
- Use a fixed-price idea only as the auctioneer's reserve. There is no first-to-accept sequence. (fixes: The double auction and first-to-accept fixed price add long sequential chains for little extra reasoning.): This keeps the auctioneer's pricing decision without a turn-by-turn accept loop.
- Use 4 artists (46 cards), 3 to 4 players and 3 seasons. A season ends at an artist's 4th card. The top two artists earn 30 and 20. Cards are dealt once, at the start. The game lasts at most 32 auctions. (fixes: Four seasons, five artists and up to 5 players make the game long and push past the attribute and step limits.): This keeps seasons, cumulative values and the uncertain season end, while staying inside the limits on rounds, attributes and draws.
- After each auction, all bids are revealed. Money and hands stay private. Each round also has a simultaneous one-message talk phase before bidding. (fixes: The rules leave money hidden but do not say what bid information becomes public. Inference needs a clear information rule.): Revealed bids give evidence about rivals' valuations and holdings. Talk allows bluffing about which artists will rise, and players disagree about which artists should win.

## Kept from the original

- Players take turns as auctioneer, selling a painting from their own hidden hand.
- The buyer pays the auctioneer. If the auctioneer ends up with the card, they pay the bank.
- A season ends abruptly when one artist reaches a set number of cards. The triggering card is discarded, not sold.
- Artists are ranked by cards sold this season. Only the top artists pay, at their cumulative value across seasons.
- Paintings are discarded after each season's payout.
- Hidden money, and the richest player wins.

## The variation's rules

COMPONENTS
- A deck of 46 painting cards by four artists: Red 10 cards, Blue 11, Green 12, Yellow 13.
- Artist order, used for ties: Red, then Blue, then Green, then Yellow.
- Each artist has a cumulative value, starting at 0.

SETUP
- Each player starts with 100 money. Money is private: only its owner sees it.
- Shuffle the deck. Deal each player a private hand: 10 cards with 3 players, 8 cards with 4 players. The rest of the deck is unused.
- Seat order is random. The first player in seat order is the first auctioneer.
- The season number starts at 1. Every artist's season count starts at 0.

EACH ROUND (ONE AUCTION)
1. Choose (auctioneer only). The auctioneer secretly chooses one card from their hand and a reserve price, a whole number from 0 up to their current money.
2. Reveal. The chosen card leaves the auctioneer's hand. Its artist is announced to all, and that artist's season count goes up by 1.
3. Season-end check. If that artist's season count is now 4, the card is discarded unsold and the reserve is ignored. Skip steps 4 to 7 and go to step 8, season scoring. Otherwise, announce the reserve to everyone.
4. Talk. Every player (auctioneer included) writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
5. Bid. Every player except the auctioneer submits a sealed bid at the same moment. A bid is a whole number from 0 up to the bidder's current money.
6. Resolve. The winner is the highest bid that is at least the reserve. If bids tie, the tied bidder who comes first in seat order after the auctioneer wins. The winner pays the bid to the auctioneer and takes the painting face-up in front of them.
   - If no bid reaches the reserve, the auctioneer must buy the painting. They pay the reserve to the bank (the money leaves the game) and take the painting.
7. Announce. All bids, the buyer and the price are announced publicly.
8. Season scoring. This step happens only if the season ended in step 3, or if every hand is now empty.
   a. Rank the four artists by season count, highest first. Ties go to the artist earlier in artist order.
   b. Add 30 to the cumulative value of the first-ranked artist and 20 to the second-ranked artist. If the second-ranked artist has a season count of 0, it gets nothing.
   c. Each player receives, for every face-up painting they own of the two ranked artists, money equal to that artist's cumulative value after step b. Paintings of the other two artists pay nothing, even if those artists scored in earlier seasons.
   d. Discard all face-up paintings. Reset every artist's season count to 0. Add 1 to the season number.
9. End check. The game ends after the third season scoring, or when every hand is empty (that final season is scored in step 8 first).
10. Rotate. The auctioneer passes to the next player in seat order who still holds at least one card. Any player with no cards is skipped as auctioneer but still bids.

LIMITS
- Money can never go below 0. Bids and reserves cannot exceed the player's current money.
- The game has at most 32 rounds.

Objective: When the game ends, each player's money is revealed. The player with the most money wins. If two or more players tie for the most, the game is a draw.

Expected effect: Players must value each painting from public counts, cumulative values, their own hand and inferences about rivals' hands. Those inferences come from which artists rivals choose to auction, what reserves they set and how they bid (all bids are revealed). Timing matters: an artist close to 4 cards can end the season. A player holding that artist can end the season by auctioning it, which voids its sale but locks in the current ranking.

The reserve creates real risk. Set it too high and the auctioneer must buy at that price. Set it too low and the painting sells cheaply.

Talk earns its place because interests conflict. Each player wants the artists they own or hold to finish top two, and wants rivals to overpay. A player who believes another's claim that 'Green will win this season' and bids up Green may be holding worthless paintings when Blue ends the season. Players must judge claims against the bids and auctions they observe.

Simple policies lose. Always bidding 0 forfeits profitable purchases and lets rivals buy cheaply. Always bidding everything overpays and goes broke. Always setting a reserve of 0 gives paintings away. A player dealt a weak hand can still win by selling cleverly and buying the right artists, so the deal does not decide the game.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 32 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
