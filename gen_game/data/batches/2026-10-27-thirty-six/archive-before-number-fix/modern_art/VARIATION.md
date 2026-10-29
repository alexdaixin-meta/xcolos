# Variation: Modern Art: Sealed Gallery

Three players each hold a hidden hand of seven paintings across three artists, in compositions 4/2/1 that are worth the same in total. They take turns as auctioneer, offering one painting per round to a simultaneous sealed-bid auction preceded by one round of simultaneous talk. The third painting of an artist in a season ends the season and is not sold. Artists ranked first and second gain value that accumulates over the game, owned paintings pay out, and after 18 rounds the richest player wins.

Players: 3 to 3, best with 3

## Review of the original

Modern Art is a 3-5 player auction game. Players take turns auctioning painting cards by five artists using five different auction formats. At the end of each of four seasons, the artists played most often gain value, and owned paintings of those artists pay out. The player with the most money wins.

- **non_degenerate**: good. Simple policies lose. A player who never bids gets only paintings nobody else wants and falls behind. A player who always bids high overpays for artists that may never score. The auctioneer seat rotates, so no seat has a built-in edge, and each auction choice changes which artists score.
- **skill_sensitive**: good. Valuing a painting means predicting which artists will finish in the top three. That depends on rivals' hands and incentives, so good valuation and timing reliably beat naive bidding. The deal adds variance, but over four seasons skill dominates.
- **headroom**: good. Strong players keep improving: they manipulate rankings, choose which cards to sell, end seasons early and read rivals' money. A weak player can still score by buying cheap paintings of leading artists.
- **reasoning_dependent**: good. Hands and money are hidden. Players must infer which artists rivals will push and how much they can afford, and plan across seasons because artist values accumulate.
- **verifiable**: good. Payouts, prices and the final money comparison are pure arithmetic.
- **fits_platform**: bad. Five auction formats, five artists, large hands, open ascending bidding (close to real time) and a value board make the game far too long and rule-heavy for the step and choice limits. It needs heavy compression.

## Problems

- The original is too large for the platform: five auction types, five artists, large hands and four long seasons exceed the step and choice limits, and open ascending bidding is close to real time.
- In the previous variation, the rules after scoring (payout, reset, announce) had no explicit condition. A flat step list read literally would wipe all paintings every round, which destroys the game.
- The previous variation did not say whether talk exists. The game has three players with real conflict (auctioneer wants high prices, bidders want low prices, only one player can win), so the omission leaves the design incomplete.
- The previous variation claimed money was private while announcing every bid, price and payout. Every balance could be computed exactly, so the claim was misleading about what is hidden.
- The auction steps (bid, winner, settle) in the previous variation also relied on prose to be skipped when the played card ends the season, rather than on an explicit tracked condition.

## Changes

- Compress the game to 3 players, 3 artists, 7-card hands with symmetric compositions (4/2/1), one sealed-bid auction format, seasons ending on the 3rd card of an artist, and 18 rounds. (fixes: The original is too large for the platform: five auction types, five artists, large hands and four long seasons exceed the step and choice limits, and open ascending bidding is close to real time.): This keeps auctions, season rankings and accumulating artist values within 15 steps per round and 3 choice steps per round.
- Add a single table flag, season_over. It is cleared at the start of every round, set to 1 by a season-ending card, and set to 1 in round 18. Scoring, payout, reset and season announcement each carry the explicit condition 'only if season_over = 1'. Rotation, the round counter and the end check are stated to run every round. (fixes: In the previous variation, the rules after scoring (payout, reset, announce) had no explicit condition. A flat step list read literally would wipe all paintings every round, which destroys the game.): A literal flat-list engine then can never wipe paintings in a round where no season ended.
- Give talk, bid, winner and settle the explicit condition 'only if season_over = 0' at that point, before the round-18 flag is set. (fixes: The previous variation's auction steps (bid, winner, settle) relied on prose to be skipped when the played card ends the season, rather than on an explicit tracked condition.): A season-ending card is then never auctioned, through a tracked number rather than prose.
- Add one simultaneous talk step each auctioned round, after the card is revealed and before bids. Every player writes one short message without seeing the others; all messages are then shown; then everyone bids. Talk is non-binding. (fixes: The previous variation did not say whether talk exists. The game has three players with real conflict (auctioneer wants high prices, bidders want low prices, only one player can win), so the omission leaves the design incomplete.): The game passes both talk tests. Players disagree: the auctioneer wants high bids, bidders want low prices, and only one player can win. Talk gives bluffing about hand composition and interest, and offers non-binding low-bid pacts that a rival can betray to grab the painting cheaply. Talk is simultaneous so that no one simply copies an earlier speaker.
- Declare money public. Each seat's hand composition remains the single hidden element. (fixes: The previous variation claimed money was private while announcing every bid, price and payout. Every balance could be computed exactly, so the claim was misleading about what is hidden.): The stated hidden information then matches what players can actually compute. The real inference is about who holds which composition, and therefore which artist each rival will push or end.

## Kept from the original

- Players take turns as auctioneer and sell a card from their own hand.
- A seller who buys their own painting pays the bank; otherwise the buyer pays the seller.
- A season ends when a set number of cards of one artist has been played, and the ending card is not sold.
- Artists are ranked by cards played in the season. Top artists gain value that accumulates across seasons, and owned paintings pay the artist's cumulative value.
- Paintings are discarded after each season.
- Most money at the end wins.

## The variation's rules

R1 SETUP (once, before round 1). There are three players, seats 1, 2 and 3, and three artists: Red, Blue and Green.
- Every player starts with money 60 and with owned_red, owned_blue and owned_green all 0.
- Each artist starts with season count 0 and value 0.
- The auctioneer is seat 1. The round counter is 0. The flag season_over is 0.
- Money is public: every bid, price and payout is announced, and anyone may track every balance. Each player's hand is private.

R2 DEAL (once, before round 1). The game rolls one six-sided die (deal_roll, 1 to 6).
- The three compositions are:
  - A: Red 4, Blue 2, Green 1.
  - B: Red 1, Blue 4, Green 2.
  - C: Red 2, Blue 1, Green 4.
- Seats 1, 2 and 3 receive compositions by roll:
  - Roll 1: A, B, C.
  - Roll 2: A, C, B.
  - Roll 3: B, A, C.
  - Roll 4: B, C, A.
  - Roll 5: C, A, B.
  - Roll 6: C, B, A.
- Exactly one case applies. It SETS each seat's hand_red, hand_blue and hand_green to the listed numbers.
- Each player sees only their own hand. Each player knows the other two seats hold the other two compositions, but not which seat holds which.

Each round runs R3 to R16 in order.

R3 START (every round). The round counter rises by 1. season_over is set to 0.

R4 PLAY (every round). The auctioneer chooses one artist X for which their own hand count is above 0. Only those artists are options.

R5 UPDATE (every round).
- The auctioneer's hand_X falls by 1.
- season_X rises by 1.
- current_artist is set to X and announced to all.

R6 SEASON-ENDING CARD (every round). If season_X is now 3, season_over is set to 1, the card is discarded unsold, and this is announced. Otherwise season_over stays 0.

R7 TALK (only if season_over = 0). Every player, including the auctioneer, writes one short message at the same time without seeing the others. All three messages are then shown to everyone, labelled by seat. Messages are free text and bind no one.

R8 BID (only if season_over = 0). All three players, including the auctioneer, bid at the same moment.
- Each bids a whole number from 0 up to their own current money.
- Bids are hidden until all are in, then all three are announced.

R9 WINNER (only if season_over = 0).
- The highest bid wins, and the price is the winning bid.
- If the highest bid is 0, the auctioneer takes the painting at price 0.
- Ties at a positive bid go to the tied seat that comes first in this order: the seat after the auctioneer, then the next seat, with the auctioneer last. (Auctioneer 1: order 2, 3, 1. Auctioneer 2: order 3, 1, 2. Auctioneer 3: order 1, 2, 3.)

R10 SETTLE (only if season_over = 0).
- If the winner is not the auctioneer, the winner's money falls by the price and the auctioneer's money rises by the price.
- If the winner is the auctioneer, the auctioneer's money falls by the price, which goes to the bank.
- The winner's owned_X rises by 1.
- The winner and price are announced.

R11 FINAL-ROUND FLAG (every round). If the round counter is 18, season_over is set to 1.

R12 SEASON SCORING (only if season_over = 1). Only artists with season count at least 1 can score.
- If one artist has the strictly highest season count, its value rises by 6. Then, if one of the other two artists has a strictly higher season count than the third and at least 1, that artist's value rises by 3.
- If two or three artists tie for the highest season count (at least 1), each of them gains value +3, and no other artist scores.

R13 PAYOUT (only if season_over = 1). For each artist that scored in R12 this round, every player's money rises by (their owned count of that artist) × (that artist's new cumulative value). Artists that did not score pay nothing, but keep their value.

R14 RESET (only if season_over = 1).
- Every player's owned_red, owned_blue and owned_green become 0 (paintings are discarded).
- Every artist's season count becomes 0.
- Values are kept.

R15 ANNOUNCE (only if season_over = 1). The scoring artists, their new values, each player's payout and each player's money are announced.

R16 ROTATE AND END (every round).
- The auctioneer passes to the next seat (1 to 2, 2 to 3, 3 to 1).
- If the round counter is 18, the game ends. Otherwise the next round begins at R3.
- Each seat is auctioneer exactly 6 times and plays 6 of its 7 cards, so the R4 options are never empty.

Objective: After round 18, including the final season's scoring and payout, the player with the strictly highest money wins. If two or three players tie for the highest money, the game is a draw.

Expected effect: Bids now hinge on predicting which artists will rank first and second this season and how values will accumulate. That prediction depends on inferring which composition each rival holds from what they auction, how they bid and what they say. Auctioneers choose which card to sell, and whether to end a season by playing an artist's third card, to strand rivals' paintings or cash in their own. Because compositions are symmetric (each seat holds one 4, one 2 and one 1), the deal changes what to do, not who is ahead.

Talk passes both tests. The players disagree: the auctioneer wants high bids, each bidder wants the painting cheap, and only one player can win. Players can bluff about their composition to steer rivals toward or away from an artist, or propose that both bidders bid low against the auctioneer. Such a pact is non-binding: a player who follows it by bidding 0 loses the painting to a partner who defects with a small bid, and with it the payout that may decide the game. A player who believes a bluff about which artist will lead overpays for paintings that score nothing.

Simple policies lose. Always bidding 0 cedes every contested painting. Always bidding all your money bankrupts you on non-scoring artists. Always playing your largest artist lets rivals predict and exploit your season endings. The fixed-length, highest-total rule is appropriate here because this is a competitive auction, not a cooperation game, so there is no trust for endgame unravelling to destroy.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 3 (limit 4)
- attributes: 19 (limit 20)
- hidden_elements: 1 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 18 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
