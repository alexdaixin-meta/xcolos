# Variation: Pocket Smear

A 3-player, 9-deal miniature of Smear. Players secretly bid and name a trump suit in one poll, the highest bidder becomes pitcher and must make the contract in category points over 4 tricks or be set, and the highest total after 9 deals wins.

Players: 3 to 3, best with 3

## Review of the original

Smear is a 3-8 player trick-taking game from the Pitch family. Players bid for the right to name trump and must then earn at least their bid in category points (High, Low, Jack, Jick, Jokers, Game, Three) over 6 tricks, or be set back by the bid. The first to 21 wins.

- **non_degenerate**: good. Always passing gives up the pitcher's trump advantage and only collects scraps as a defender. Always bidding the maximum gets set often and loses the bid each time. The deal and lead rotate, so no seat keeps an edge. Bids and card choices clearly change who scores which category.
- **skill_sensitive**: weak. Over many deals, skilled bidding and card play win. In any single deal the hand dominates: the stock exchange and the joker and jick holdings swing points. A short race to 21 leaves a lot of variance.
- **headroom**: good. Hand evaluation, choosing a bid level, inferring hands from bids, card counting, and deciding when to protect or capture the Three and the Low all reward deeper play. A weak player still scores defensive points.
- **reasoning_dependent**: good. Hands are hidden. Bids signal strength. Played cards reveal what is held. Players must infer where High, Low and the Three are and plan over the tricks of a deal and across deals.
- **verifiable**: good. All scoring is counting: categories, card points and set penalties. Follow-suit legality is mechanical.
- **fits_platform**: bad. As written it does not fit: a 54-card deck with jokers and jick, a 14-card stock exchange and discard, 6-trick deals, variable player counts up to 8, and an open-ended race to 21 exceed the attribute, choice-step and round limits. Teams are also ambiguous. The previous Pocket Smear cut it down well but left two defects: it did not say whether non-pitchers' named suits are revealed, and it did not say the bid and suit are one poll, which pushes round 1 to 5 choice steps.

## Problems

- The original's deck (54 cards, jokers, jick), the stock exchange and discards, and the 6-trick deals make far too much state and too many steps for the engine.
- The original's open-ended race to 21 with possible teams gives no fixed, buildable length and an unclear winner structure.
- Previous variation, bid ambiguity: it did not say whether the suits named by non-winning bidders are revealed. That suit is meaningful hidden information, so players could not know what opponents learn.
- Previous variation, choice-step budget: if the bid and suit are separate submissions, round 1 has 5 choice steps (bid, suit, three card plays), over the limit of 4.
- Previous variation: the all-pass fallback needs the dealer to have named a suit, but the rules let a passing player's suit seem optional.
- Previous variation: the attribute count was tight (about 18). Deal points must be computed at scoring time, not stored per player.

## Changes

- Keep the compact Pocket Smear core: 24 cards in three suits of ranks 1-8, 4-card hands, 4 tricks per deal, 9 deals (36 rounds), 3 players, and the categories High, Low, Game and Three. (fixes: The original's deck (54 cards, jokers, jick), the stock exchange and discards, and the 6-trick deals make far too much state and too many steps for the engine.): This keeps the game within the step, attribute and round limits while preserving bidding, trump and category scoring.
- The game has a fixed length of 9 deals with rotating dealer and priority. There are exactly 3 players, no teams, and the highest total wins (a tie for highest is a draw). (fixes: The original's open-ended race to 21 with possible teams gives no fixed, buildable length and an unclear winner structure.): This gives a buildable fixed length and a clear arithmetic winner. With three rivals, sandbagging or always passing does not guarantee a result.
- The bid amount and the named suit are submitted together as ONE answer in ONE simultaneous poll (for example '4 Blue' or 'PASS Green'). (fixes: Previous variation, choice-step budget: if the bid and suit are separate submissions, round 1 has 5 choice steps (bid, suit, three card plays), over the limit of 4.): Round 1 then uses exactly 4 choice steps: the bid poll plus three card plays.
- State explicitly that only bid amounts (including PASS) and the pitcher's suit are revealed. Every other named suit stays secret for the whole game. (fixes: Previous variation, bid ambiguity: it did not say whether the suits named by non-winning bidders are revealed. That suit is meaningful hidden information, so players could not know what opponents learn.): Everyone now knows exactly what is public. The hidden suits stay private information, so opponents must infer them from bids and play.
- Every player must name a suit from their own hand even when passing. In an all-pass deal, the dealer's named suit becomes trump. (fixes: Previous variation: the all-pass fallback needs the dealer to have named a suit, but the rules let a passing player's suit seem optional.): The fallback always has a defined trump, and the forced pitcher always holds a trump to lead.
- Track only running state: High trump value and holder, Low trump value and holder, Three captor, and each player's pile card points. Each player's deal points are computed at the scoring step and not stored. (fixes: Previous variation: the attribute count was tight (about 18). Deal points must be computed at scoring time, not stored per player.): This keeps attributes at about 18, under the limit of 20.

## Kept from the original

- Bidding for the right to name trump, with the highest bid becoming the pitcher's contract.
- The pitcher must lead trump to the first trick.
- A player may trump in even while holding the led suit.
- Category scoring: High, Low, Game by card points, and a 3-point Three of trump.
- Being set back by the contract on a failed bid, with scores allowed to go negative.
- No table talk: information flows only through bids and cards.

## The variation's rules

PLAYERS: exactly 3, seated as Player 1, Player 2 and Player 3. Seat order is 1, 2, 3, then back to 1.

DECK: 24 cards in three suits (Red, Blue, Green). Each suit has ranks 1 to 8. Card points, used only for Game: rank 8 = 4, rank 7 = 3, rank 6 = 2, rank 5 = 1, all other ranks = 0.

STRUCTURE: The game is 9 deals. Each deal is 4 rounds with one trick per round, so the game is 36 rounds. The dealer rotates: Player 1 deals deals 1, 4 and 7; Player 2 deals deals 2, 5 and 8; Player 3 deals deals 3, 6 and 9. For each deal, PRIORITY ORDER is: the player after the dealer in seat order, then the next player, then the dealer. All scores start at 0.

DEAL (first round of each deal): Shuffle all 24 cards and deal 4 cards privately to each player. The other 12 cards are set aside face down, unseen by anyone, for the whole deal. Each player sees only their own hand.

BID (first round of each deal, one simultaneous poll): Every player at the same moment submits ONE answer made of two parts: (a) either PASS or a whole number from 2 to 6, and (b) one suit that appears in their own hand. A suit must be named even when passing. Examples: '4 Blue', 'PASS Red'. When all answers are in, the engine reveals every player's bid amount (or PASS).
- The highest number wins. A tie goes to the tied player who comes first in priority order.
- The winner becomes the PITCHER, their number becomes the CONTRACT, and their named suit becomes TRUMP.
- If all three pass, the dealer becomes the pitcher with a contract of 2, and trump is the suit the dealer named.
- The engine announces the pitcher, the contract and trump. The suits named by the other two players are NEVER revealed.

TRICKS (each round of a deal): Three cards are played one at a time, starting with the LEADER and continuing in seat order.
- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. The pitcher always holds one, because they named a suit from their hand. In later tricks of the deal, the leader is the winner of the previous trick, who may lead any card.
- Following: each later player must play a card of the led suit if they hold one, but may instead play a trump even if they hold the led suit. A player holding no card of the led suit may play any card.
- Winning: the trick goes to the highest-ranked trump played. If no trump was played, it goes to the highest-ranked card of the led suit.
- All played cards are visible to everyone. The three cards go into the trick winner's captured pile.

DEAL SCORING (after the 4th trick of each deal; only cards played this deal count; every dealt card is played):
- HIGH, 1 point: to the player who captured the highest-ranked trump played.
- LOW, 1 point: to the player who captured the lowest-ranked trump played. This may be the same card as High. At least one trump is always played, because the first lead is trump.
- GAME, 1 point: to the player whose captured pile has the most card points. If two or more players tie for most, nobody scores Game.
- THREE, 3 points: to the player who captured the trump of rank 3, if it was dealt. If it was not dealt, nobody scores it.
- Each player's deal points are the sum of the categories they won, from 0 to 6.
- Each of the two non-pitchers adds their deal points to their score.
- If the pitcher's deal points are at least the contract, the pitcher adds their deal points to their score.
- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score and does not add their deal points.
- Scores may go negative. Captured piles are then cleared and the next deal begins.

COMMUNICATION: There is no table talk. Players communicate only through bids and played cards.

END: After the 9th deal is scored, the game ends.

Objective: After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

Expected effect: Players must judge a 4-card hand's worth in a chosen trump, bid high enough to win trump control without overreaching, and read opponents' bid sizes for strength. They must also guess which suits the opponents secretly named, since those suits stay hidden and hint at their holdings. During play, players count cards to locate the Three, High and Low, decide when to trump in, and, as defenders, pool their efforts implicitly to set the pitcher. Simple policies lose. Always passing forfeits trump control, and a passer who is forced to pitch as dealer can still be set. Always bidding 6 is set most deals and loses 6 each time. Playing a random legal card throws away the Three and Low. Talk is omitted because it would only leak hands, and bids and cards already carry the signals worth reasoning about. This is not a cooperation game, so endgame unraveling does not apply. Rotating dealer and priority order remove seat advantage.

## Complexity (the designer's count, against the limits)

- steps_per_round: 14 (limit 20)
- choice_steps_per_round: 4 (limit 4)
- attributes: 18 (limit 20)
- hidden_elements: 2 (limit 3)
- random_draws_per_round: 1 (limit 1)
- rounds: 36 (limit 40)

## The rules played with numbers

not simulated: the game does not fit the simultaneous-choice model
