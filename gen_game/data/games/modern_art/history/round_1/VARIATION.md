# Variation: Modern Art: Sealed Gallery

Four dealers auction paintings by three artists from hidden hands with sealed bids. Artist values are set by how much each artist is played in a season. After three seasons, most money wins.

Players: 4 to 4, best with 4

## Review of the original

Modern Art is a 3-5 player auction game. Players take turns auctioning painting cards from hidden hands using five auction types. At the end of each of four rounds, artist values are set by how many of that artist's cards were played, and owned paintings pay out from the bank. Most money after four rounds wins.

- **non_degenerate**: good. No simple policy dominates. Always bidding nothing gives away every purchase and lets rivals buy cheaply. Always bidding high overpays for paintings that may score nothing. Always playing your biggest artist is predictable, so others bid it to its true value or above. Turn order rotates, and the auctioneer advantage is shared.
- **skill_sensitive**: good. Expert players reliably beat novices. The skill is valuing a painting before its artist's rank is known, timing when a season ends, and pricing bids against what rivals will pay. The deal of cards adds variance, but buying lets a player correct for a poor hand.
- **headroom**: good. Valuation depends on everyone's hands and intentions, so play is never solved. A weak player still collects money by selling cards.
- **reasoning_dependent**: good. Hands are hidden, so players must infer from what others play and bid which artists will be pushed. A painting's value is set collectively later. Ending a season with the closing card is a plan over several turns.
- **verifiable**: good. Payments, rankings and payouts are all arithmetic.
- **fits_platform**: weak. Five auction types are too much: open ascending bidding is effectively real-time, and the once-around and double auctions are chains of turn-by-turn steps. Five artists and four rounds with cumulative value markers exceed the attribute budget and run long. The value board itself is only a table, so that part is fine.

## Problems

- Open ascending auctions are real-time or need an unbounded number of bid turns, which the engine cannot run.
- Five auction types plus double auctions mean many separate step blocks, which cannot be chosen between because the step list is flat.
- Five artists times per-player hand and ownership counts, plus value columns, exceed the 20-attribute limit.
- Four rounds of up to 5 cards per artist across 5 artists can exceed 40 turns.
- Money is already effectively trackable from public payments, so having several hidden layers adds bookkeeping, not inference.

## Changes

- Use a single auction type: one simultaneous sealed bid from all four players, auctioneer included. Highest bid wins. Ties go to the auctioneer, then in seat order after the auctioneer. A buyer pays the auctioneer; if the auctioneer wins, they pay the bank. (fixes: Open ascending auctions are real-time or need an unbounded number of bid turns, which the engine cannot run.): This keeps the core Modern Art tension (sell to rivals or buy your own card at a cost) in one poll.
- Drop the fixed-price, once-around and double auctions. (fixes: Five auction types plus double auctions mean many separate step blocks, which cannot be chosen between because the step list is flat.): A flat step list cannot choose between auction blocks.
- Use three artists (deck of 14/12/10 cards). Each season, the most-played artist adds 30 to its cumulative value, the second adds 20, and the third adds nothing and pays nothing. (fixes: Five artists times per-player hand and ownership counts, plus value columns, exceed the 20-attribute limit.): This fits the attribute budget. Leaving one of three artists unpaid keeps the risk of backing the wrong artist.
- A season ends when an artist's 4th card is played; that card is not auctioned. Play three seasons, and deal all 9 cards per player at the start. (fixes: Four rounds of up to 5 cards per artist across 5 artists can exceed 40 turns.): A season holds at most 10 cards, so there are at most 30 turns. One deal at setup means no chance events during rounds.
- Keep hands as the one strong hidden element. Money stays private but every bid and payment is public. (fixes: Money is already effectively trackable from public payments, so having several hidden layers adds bookkeeping, not inference.): Inference centres on what rivals hold and want to push.

## Kept from the original

- Auctioning paintings from a hidden hand, with the auctioneer earning the sale price
- An auctioneer who buys their own card pays the bank
- Artist values set collectively by how often each artist is played in a season, and cumulative across seasons
- Only top-ranked artists pay; the rest are worthless
- The season-ending card is played but not sold
- Most money wins

## The variation's rules

SETUP: The deck has 36 painting cards: 14 by artist Amber, 12 by Blue, 10 by Crimson. Shuffle it and deal 9 cards to each of the 4 players as a hidden hand. Each player starts with 100 money, known only to them, though all payments are announced. Every artist starts with a cumulative value of 0. Seats are numbered 1-4, and seat 1 is the first auctioneer.

TURN (one engine round):
1) Announce the turn and the auctioneer.
2) The auctioneer chooses one card from their hand and reveals it. If the auctioneer has no cards, the turn passes to the next seat. This cannot happen in practice, because at most 30 cards are ever played.
3) The card leaves the hand, and that artist's played-this-season count goes up by 1.
4) If that count is now 4, the season ends. This card is not auctioned and no one owns it. Go to SEASON END.
5) Otherwise, there is talk. Every player writes one short message at the same time without seeing the others. All messages are then shown. Talk binds no one.
6) There is a sealed bid. All 4 players, auctioneer included, at the same time submit a whole-number bid from 0 up to their current money.
7) The highest bid wins. Ties are broken in favour of the auctioneer, then in seat order clockwise from the auctioneer. If every bid is 0, the auctioneer gets the card free.
8) A non-auctioneer winner pays their bid to the auctioneer. An auctioneer who wins pays their bid to the bank.
9) The winner adds the painting to their owned paintings of that artist. All bids, the buyer and the price are announced.
10) The auctioneer role passes to the next seat.

SEASON END:
a) Rank the artists by played-this-season count. Ties go to the rarer artist: Crimson beats Blue, and Blue beats Amber.
b) The first artist's cumulative value rises by 30. The second's rises by 20. The third gains nothing.
c) Each player receives, from the bank, (number of owned paintings of the first artist × its cumulative value) plus (number of owned paintings of the second artist × its cumulative value). Paintings of the third artist pay nothing this season, even if that artist has a cumulative value from earlier seasons.
d) All owned paintings are discarded, and all played-this-season counts reset to 0. Payouts are announced. Unplayed cards stay in hands.
e) The season count goes up by 1. If it is 3, the game ends. Otherwise the auctioneer role passes to the next seat and play continues.

GAME END: The game ends after the third season. At most 30 turns are possible.

Objective: After season 3, the player with the most money wins. If two or more players tie for most money, the game is a draw.

Expected effect: Players must value a painting before its season's ranking is known. They read rivals' hands from what they play and how they bid, and choose when to close a season so the artists they own score. Sellers profit from overbidders. Buying your own card costs money that goes out of play, so it must be worth it. Always bidding 0 loses to players who buy cheap winners. Always bidding high loses money on unscored artists. The deal's luck is eased because any painting can be bought. Talk is kept because only one player can win and players own different artists: each lobbies to push their own artist, perhaps bluffing about their hand. A player who simply follows a lobbying claim may overpay for an artist that ends third and pays nothing.

## Complexity (the designer's count, against the limits)

- steps_per_round: 18 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 0 (limit 1)
- rounds: 30 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
