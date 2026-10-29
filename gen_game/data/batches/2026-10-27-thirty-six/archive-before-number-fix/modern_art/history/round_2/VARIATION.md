# Variation: Modern Art: Three Studios

Three players each hold a hidden 7-card hand strong in one of three artists. Each round one player auctions a card by simultaneous sealed bid, in which the auctioneer also bids. Seasons end when an artist's third card appears. The top two artists gain cumulative value, and owned paintings of those artists pay out. Most money after 3 seasons wins.

Players: 3 to 3, best with 3

## Review of the original

Modern Art is a 3-5 player auction game. Players auction paintings by five artists using five auction types. At the end of each of four rounds the most-played artists gain value, and the paintings players own of those artists pay out. Most money wins.

- **non_degenerate**: good. No simple policy wins. Never bidding leaves you with only the paintings you auction and keep, so you cash few placed paintings. Always bidding highest overpays and transfers money to rivals. Market value depends on which artists the table pushes. Seat order matters slightly, but the auction role rotates.
- **skill_sensitive**: good. Valuing a painting before an artist's ranking is known, and timing which cards to play, are well-known skill differentiators. The random deal matters, but a skilled player outbids, undersells and steers rankings over 4 rounds.
- **headroom**: good. Valuation is never solved, because it depends on rivals' hidden hands and intentions. A weak player still earns money by selling paintings, so scores are never zero.
- **reasoning_dependent**: good. Hands and money are hidden. A player must infer which artists rivals hold from what they auction and bid on, predict the ranking, and plan several rounds ahead because values accumulate.
- **verifiable**: good. Rankings, payouts and money totals are pure arithmetic.
- **fits_platform**: weak. It has five auction types, two of them sequential and open (open ascending is near real-time). It has a physical value board, five artists with ranking ties, a deal of 40+ random cards, and up to about 70 auctions. The previous variation left reveals undefined and understated its draws, steps and attributes.

## Problems

- Five auction types (open ascending, once-around, fixed price, double) need sequential or near-real-time bidding and many steps; only sealed simultaneous bidding fits cheaply.
- Dealing dozens of random cards one at a time breaks the limit of 1 random draw per round and costs many remove/append steps (previous variation: 30+ draws declared as 0).
- Ranking 4-5 artists with tie-breaks, and paying every player for every artist, exceeds the step and attribute budget (previous variation understated both).
- The previous variation never said what is announced after an auction (bids, winner, price, reserve), nor whether money and owned paintings are public, so players cannot track rivals.
- The previous variation did not state that a painting the auctioneer keeps joins their owned paintings and scores.
- The secret reserve added a fourth hidden element and an extra choice step for little strategic gain.
- Full game length (4 rounds, about 70 auctions) is too long for the platform.

## Changes

- Use one auction type: a simultaneous sealed bid in which the auctioneer also bids. If the auctioneer is highest, they pay the bank; if every bid is 0, the auctioneer keeps the painting for free. (fixes: Five auction types (open ascending, once-around, fixed price, double) need sequential or near-real-time bidding and many steps; only sealed simultaneous bidding fits cheaply.): This keeps Modern Art's 'buy your own painting from the bank' tension. It needs only one simultaneous poll and replaces the secret reserve.
- Replace the card deal with three fixed 7-card hand compositions, each strong in one artist. One random draw at setup (a number 1-6) assigns the compositions to the seats through a fixed table. (fixes: Dealing dozens of random cards one at a time breaks the limit of 1 random draw per round and costs many remove/append steps (previous variation: 30+ draws declared as 0).): This takes exactly one random draw and one assignment step. The compositions are rotations of each other, so the deal is balanced. A player's composition is a hidden type that rivals must infer from what they auction and bid on.
- Cut to 3 artists and 3 players. Only the top two artists place, earning +20 and +10. The ranking uses a fixed tie order (Red, Blue, Green). The payout is one formula per player: owned count times cumulative value, summed over placed artists. Owned paintings are tracked as per-player counts for each artist. (fixes: Ranking 4-5 artists with tie-breaks, and paying every player for every artist, exceeds the step and attribute budget (previous variation understated both).): The ranking takes 2 calc steps and the payout 1 step, so the game fits 20 attributes and 20 steps when counted honestly.
- After every auction, announce all bids, the buyer and the price. Money and owned paintings are public. Only hand contents are hidden. The card played is always announced. (fixes: The previous variation never said what is announced after an auction (bids, winner, price, reserve), nor whether money and owned paintings are public, so players cannot track rivals.): Every player has the same public record to reason from. The hidden information is concentrated in hands, as in the original.
- State explicitly that every painting the auctioneer keeps (bought from the bank or taken for free) is added to the auctioneer's owned count for that artist and scores normally. (fixes: The previous variation did not state that a painting the auctioneer keeps joins their owned paintings and scores.): This removes the ambiguity about whether kept paintings score.
- Remove the reserve. (fixes: The secret reserve added a fourth hidden element and an extra choice step for little strategic gain.): The auctioneer's own sealed bid serves the same purpose. This leaves 2 hidden elements (hands and sealed bids) and 3 choice steps.
- Play 3 seasons. A season ends when the third card of one artist is played; that card is unsold. The game lasts at most 21 rounds, one card per round. (fixes: Full game length (4 rounds, about 70 auctions) is too long for the platform.): The game stays short while keeping cumulative artist values across seasons.

## Kept from the original

- Players auction paintings from a hidden hand, and the auctioneer earns the sale price.
- The auctioneer may buy their own painting by paying the bank.
- The season ends when one artist reaches a card limit, and that final card goes unsold.
- Artists are ranked by cards played in the season, and the top artists gain value.
- Values accumulate across seasons, so a repeat winner becomes very valuable.
- Owned paintings pay out only if their artist placed this season, then are discarded.
- Most money wins.

## The variation's rules

R1 Setup. There are 3 players in seats 1, 2 and 3, and 3 artists: Red, Blue and Green. Each player starts with 60 money. Money is public at all times. Each player has hand counts for Red, Blue and Green and owned counts for Red, Blue and Green; all owned counts start at 0. On the table, each artist has a season count and a cumulative value, all starting at 0. seasons_done starts at 0 and the auctioneer is seat 1.

R2 Hands, at setup only. There are three hand compositions of 7 cards each. Composition A is 4 Red, 2 Blue, 1 Green. Composition B is 1 Red, 4 Blue, 2 Green. Composition C is 2 Red, 1 Blue, 4 Green. The engine draws one random whole number from 1 to 6 and gives compositions to seats 1, 2 and 3 as follows: 1 gives A,B,C; 2 gives A,C,B; 3 gives B,A,C; 4 gives B,C,A; 5 gives C,A,B; 6 gives C,B,A. Each player sees only their own hand counts. Everyone knows the three compositions exist and that each player has a different one. This is the only random event in the game.

R3 Choose a card. The auctioneer chooses one artist from those for which their hand count is above 0.

R4 Reveal. The chosen artist is announced to everyone as the current artist. The auctioneer's hand count for that artist falls by 1, and that artist's season count rises by 1.

R5 Season-ending card. If the current artist's season count is now 3, the card is discarded unsold. Skip R6 to R8 this round and go to R9.

R6 Talk. Otherwise, all three players each write one short message at the same moment without seeing the others. All messages are then shown to everyone. Talk is not binding.

R7 Sealed bids. Otherwise, all three players, the auctioneer included, submit at the same moment a whole-number bid from 0 up to their current money. The highest bid wins. If bids tie for highest, the tied player who comes first in seat order starting from the seat after the auctioneer wins, with the auctioneer last. If every bid is 0, the auctioneer wins at price 0.

R8 Settle and announce. If the winner is not the auctioneer, the winner pays their bid to the auctioneer. If the winner is the auctioneer, they pay their bid to the bank (nothing if it is 0). In every case the winner's owned count for the current artist rises by 1; this includes paintings the auctioneer keeps, which score like any other. All three bids, the winner and the price are announced to everyone. Owned counts are public.

R9 Season scoring. Scoring happens if the season-ending card was just played (R5), or if all hands are now empty and at least one season count is above 0. When it happens:
(a) First place is the artist with the highest season count, ties broken in the order Red, Blue, Green. Its cumulative value rises by 20.
(b) Second place is the highest of the remaining two artists by season count, same tie order, but only if its season count is above 0. Its cumulative value rises by 10.
(c) The third artist, and any artist with season count 0, does not place.
(d) Each player receives from the bank, for each placed artist, their owned count of that artist times that artist's cumulative value. Unplaced artists pay 0. Note that a cumulative value can be above 0 from earlier seasons, but it pays only if the artist placed this season.
(e) The placings, the new cumulative values and each player's payout are announced.
(f) All owned counts reset to 0, all season counts reset to 0, and seasons_done rises by 1.

R10 Pass the role. The auctioneer role passes to the next seat (1 to 2, 2 to 3, 3 to 1). It skips any seat whose hand is empty.

R11 End. The game ends when seasons_done reaches 3, or when all hands are empty (after R9 has scored any unfinished season). The game lasts at most 21 rounds.

Objective: When the game ends, the player with the most money wins. If two or three players tie for the most money, the game is a draw.

Expected effect: Each player wants their own strong artist to place, because they can supply it and buy it cheaply, and rivals' strong artists to fail. Bids therefore signal private information. Heavy bidding on Blue hints that you hold Blue or expect it to place, and the cards a player auctions reveal their composition. Players must infer rivals' compositions, value paintings before the ranking is known, and judge when to buy their own painting from the bank to keep a painting rather than sell it cheaply. Bidding 0 always only earns sale revenue and loses to profitable buyers; maximum bidding overpays and loses. Talk passes both tests: players disagree over prices (seller against buyers) and over which artist should place (each prefers their own strong one). A player who follows a rival's claim that 'Green will place' can buy Green, watch the rival play Red instead, and be left with worthless paintings. The deal is symmetric by rotation, so the hidden type changes what to do, not who is ahead. Seat 1 may auction one more time if the game ends at 3 seasons; the random seat assignment of compositions limits this.

## Complexity (the designer's count, against the limits)

- steps_per_round: 17 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 20 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 21 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
