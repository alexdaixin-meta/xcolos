# 03 design

- time: 2026-10-28T03:34:04+00:00 (52.8s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 c7c0ee316b0d485d, reply sha256 5f642314f72a9b17

## Sent

````
Original game: Smear
Players in the original: 3 to 8

Original rules:
Deal 10 cards each from 54 cards including two jokers and left bower Jick. Players in order bid the points they will win or pass; highest bidder becomes pitcher and declares trump. Pitcher takes 14-card stock and discards to six, others discard to six, keeping trumps if possible. Pitcher leads trump. Must follow suit led if able, but may play trump instead. Highest of led suit wins unless trumped. Play 6 tricks. Score up to 10 points per deal: High trump, Low trump, Jack, Jick, each Joker, Game by most card points with A=4 K=3 Q=2 J=1 10=10, and 3 for winning trump Three. Pitcher failing bid goes set back and scores zero. First team to 21 over multiple deals wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Most of the game is complete and finite. There are 9 deals of 4 tricks, so 36 rounds, which is within the 40-round limit. Each player is dealt 4 cards and plays 4, so 'dealt' equals 'played' for the Three. A trump is always played, so High and Low always exist. Card ranks are distinct, so tricks cannot tie. The all-pass fallback is defined. The pitcher is guaranteed to hold a trump to lead. The follow-suit legality check can go to the referee. Scoring is pure arithmetic. One random draw per deal fits the limit, and there are 2 hidden elements (hands and the unseen 12). No talk is defensible: in a trick-taking game, talk would only leak hand information, and the bids and played cards already carry the signals to reason about. There is no cooperation-decay problem, because this is not a cooperation game. Two defects remain. (1) BID AMBIGUITY: 'All bids are revealed together' does not say whether the non-winning players' named suits are revealed. That suit is meaningful hidden information about each hand, so a model with only these words cannot know what its opponents learn. (2) CHOICE-STEP BUDGET: round 1 has the bid and suit, then three sequential card plays. If the bid (a) and suit (b) are separate submissions, round 1 has 5 choice steps, which exceeds the limit of 4. The stated count of 4 only holds if (a) and (b) are one combined simultaneous poll, and the rules do not say so. Attribute count is tight: 3 scores, 3 pile-point totals, contract, trump, pitcher, leader, led suit, the High and Low holder and value, the Three holder, and the dealer come to about 18 or more. This is under 20, but deal points must be computed rather than stored.
- change: State explicitly whether the suits named by non-winning bidders are revealed or stay secret, e.g. 'Only bid amounts and the pitcher's suit are revealed; other named suits stay secret.'
- change: Specify that the bid (a) and the suit (b) are submitted together as a single simultaneous poll, so round 1 uses exactly 4 choice steps (bid poll plus three card plays).
The variation that was reviewed: Pocket Smear: DECK. 24 cards: three suits (Red, Blue, Green), each with ranks 1 to 8. Card points (used only for Game): 8 = 4, 7 = 3, 6 = 2, 5 = 1, all other ranks 0.

STRUCTURE. The game is 9 deals. Each deal is 4 rounds, one trick per round, so 36 rounds in total. Player 1 deals deal 1, Player 2 deals deal 2, Player 3 deals deal 3, and so on in rotation, so each player deals 3 times. 'Priority order' for a deal is: the player after the dealer, then the next player, then the dealer.

DEAL (first round of each deal). Shuffle all 24 cards and deal 4 to each player privately. The remaining 12 cards are set aside unseen for the whole deal. Each player sees only their own hand.

BID (first round of each deal, at the same moment). Each player secretly submits:
(a) a bid, either PASS or a whole number from 2 to 6;
(b) a suit that is among the suits in their own hand.
All bids are revealed together. The highest bid wins, and ties go to the tied player earliest in priority order. That player becomes the PITCHER, the bid becomes the CONTRACT, and the pitcher's named suit becomes TRUMP. If all three pass, the dealer becomes pitcher with a contract of 2, and trump is the suit the dealer named. The pitcher, contract and trump are announced to all.

TRICKS. In each round, three cards are played one at a time, starting with the LEADER and continuing in seat order (1, 2, 3, wrapping around).
- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. In later tricks, the leader is whoever won the previous trick, and may lead any card.
- Following: each later player must play a card of the led suit if they have one, but may instead play a trump even if they hold the led suit. A player with no card of the led suit may play any card.
- Winning: the trick goes to the highest trump played. If no trump was played, it goes to the highest card of the led suit.
- Every played card is visible to all. The three cards go face up into the winner's captured pile.

DEAL SCORING (after the 4th trick of each deal). Only cards played this deal count.
- HIGH (1 point): to the player who captured the highest-ranked trump played.
- LOW (1 point): to the player who captured the lowest-ranked trump played. This can be the same card as High.
- GAME (1 point): to the player whose captured pile has the most card points. If players tie for most, nobody scores Game.
- THREE (3 points): to the player who captured the trump of rank 3, if it was played. If it was undealt, nobody scores it.
Each player's deal points are the sum of the categories they won, from 0 to 6.
- Defenders add their deal points to their score.
- If the pitcher's deal points are at least the contract, the pitcher adds their deal points.
- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score, and their deal points are not added.
Scores may go negative. Captured piles are cleared and the next deal begins.

No table talk: players communicate only through bids and cards.

END. After the 9th deal is scored, the game ends. Winner: After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Smear is a 3-8 player trick-taking game from the Pitch family. Players bid for the right to name trump and must then earn at least their bid in category points (High, Low, Jack, Jick, Jokers, Game, Three) over 6 tricks, or be set back by the bid. The first to 21 wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Always passing gives up the pitcher's trump advantage and only collects scraps as a defender. Always bidding the maximum gets set often and loses the bid each time. The deal and lead rotate, so no seat keeps an edge. Bids and card choices clearly change who scores which category."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Over many deals, skilled bidding and card play win. In any single deal the hand dominates: the stock exchange and the joker and jick holdings swing points. A short race to 21 leaves a lot of variance."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Hand evaluation, choosing a bid level, inferring hands from bids, card counting, and deciding when to protect or capture the Three and the Low all reward deeper play. A weak player still scores defensive points."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "good",
      "evidence": "Hands are hidden. Bids signal strength. Played cards reveal what is held. Players must infer where High, Low and the Three are and plan over the tricks of a deal and across deals."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is counting: categories, card points and set penalties. Follow-suit legality is mechanical."
    },
    {
      "criterion": "fits_platform",
      "verdict": "bad",
      "evidence": "As written it does not fit: a 54-card deck with jokers and jick, a 14-card stock exchange and discard, 6-trick deals, variable player counts up to 8, and an open-ended race to 21 exceed the attribute, choice-step and round limits. Teams are also ambiguous. The previous Pocket Smear cut it down well but left two defects: it did not say whether non-pitchers' named suits are revealed, and it did not say the bid and suit are one poll, which pushes round 1 to 5 choice steps."
    }
  ],
  "problems": [
    "The original's deck (54 cards, jokers, jick), the stock exchange and discards, and the 6-trick deals make far too much state and too many steps for the engine.",
    "The original's open-ended race to 21 with possible teams gives no fixed, buildable length and an unclear winner structure.",
    "Previous variation, bid ambiguity: it did not say whether the suits named by non-winning bidders are revealed. That suit is meaningful hidden information, so players could not know what opponents learn.",
    "Previous variation, choice-step budget: if the bid and suit are separate submissions, round 1 has 5 choice steps (bid, suit, three card plays), over the limit of 4.",
    "Previous variation: the all-pass fallback needs the dealer to have named a suit, but the rules let a passing player's suit seem optional.",
    "Previous variation: the attribute count was tight (about 18). Deal points must be computed at scoring time, not stored per player."
  ],
  "changes": [
    {
      "what": "Keep the compact Pocket Smear core: 24 cards in three suits of ranks 1-8, 4-card hands, 4 tricks per deal, 9 deals (36 rounds), 3 players, and the categories High, Low, Game and Three.",
      "why": "This keeps the game within the step, attribute and round limits while preserving bidding, trump and category scoring.",
      "fixes": "The original's deck (54 cards, jokers, jick), the stock exchange and discards, and the 6-trick deals make far too much state and too many steps for the engine."
    },
    {
      "what": "The game has a fixed length of 9 deals with rotating dealer and priority. There are exactly 3 players, no teams, and the highest total wins (a tie for highest is a draw).",
      "why": "This gives a buildable fixed length and a clear arithmetic winner. With three rivals, sandbagging or always passing does not guarantee a result.",
      "fixes": "The original's open-ended race to 21 with possible teams gives no fixed, buildable length and an unclear winner structure."
    },
    {
      "what": "The bid amount and the named suit are submitted together as ONE answer in ONE simultaneous poll (for example '4 Blue' or 'PASS Green').",
      "why": "Round 1 then uses exactly 4 choice steps: the bid poll plus three card plays.",
      "fixes": "Previous variation, choice-step budget: if the bid and suit are separate submissions, round 1 has 5 choice steps (bid, suit, three card plays), over the limit of 4."
    },
    {
      "what": "State explicitly that only bid amounts (including PASS) and the pitcher's suit are revealed. Every other named suit stays secret for the whole game.",
      "why": "Everyone now knows exactly what is public. The hidden suits stay private information, so opponents must infer them from bids and play.",
      "fixes": "Previous variation, bid ambiguity: it did not say whether the suits named by non-winning bidders are revealed. That suit is meaningful hidden information, so players could not know what opponents learn."
    },
    {
      "what": "Every player must name a suit from their own hand even when passing. In an all-pass deal, the dealer's named suit becomes trump.",
      "why": "The fallback always has a defined trump, and the forced pitcher always holds a trump to lead.",
      "fixes": "Previous variation: the all-pass fallback needs the dealer to have named a suit, but the rules let a passing player's suit seem optional."
    },
    {
      "what": "Track only running state: High trump value and holder, Low trump value and holder, Three captor, and each player's pile card points. Each player's deal points are computed at the scoring step and not stored.",
      "why": "This keeps attributes at about 18, under the limit of 20.",
      "fixes": "Previous variation: the attribute count was tight (about 18). Deal points must be computed at scoring time, not stored per player."
    }
  ],
  "keeps": [
    "Bidding for the right to name trump, with the highest bid becoming the pitcher's contract.",
    "The pitcher must lead trump to the first trick.",
    "A player may trump in even while holding the led suit.",
    "Category scoring: High, Low, Game by card points, and a 3-point Three of trump.",
    "Being set back by the contract on a failed bid, with scores allowed to go negative.",
    "No table talk: information flows only through bids and cards."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The compact variation already preserves Smear's bidding, trump and category tension within the limits. Only the bid-poll format and the reveal rule needed fixing."
  },
  "variation": {
    "name": "Pocket Smear",
    "summary": "A 3-player, 9-deal miniature of Smear. Players secretly bid and name a trump suit in one poll, the highest bidder becomes pitcher and must make the contract in category points over 4 tricks or be set, and the highest total after 9 deals wins.",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "rules": "PLAYERS: exactly 3, seated as Player 1, Player 2 and Player 3. Seat order is 1, 2, 3, then back to 1.\n\nDECK: 24 cards in three suits (Red, Blue, Green). Each suit has ranks 1 to 8. Card points, used only for Game: rank 8 = 4, rank 7 = 3, rank 6 = 2, rank 5 = 1, all other ranks = 0.\n\nSTRUCTURE: The game is 9 deals. Each deal is 4 rounds with one trick per round, so the game is 36 rounds. The dealer rotates: Player 1 deals deals 1, 4 and 7; Player 2 deals deals 2, 5 and 8; Player 3 deals deals 3, 6 and 9. For each deal, PRIORITY ORDER is: the player after the dealer in seat order, then the next player, then the dealer. All scores start at 0.\n\nDEAL (first round of each deal): Shuffle all 24 cards and deal 4 cards privately to each player. The other 12 cards are set aside face down, unseen by anyone, for the whole deal. Each player sees only their own hand.\n\nBID (first round of each deal, one simultaneous poll): Every player at the same moment submits ONE answer made of two parts: (a) either PASS or a whole number from 2 to 6, and (b) one suit that appears in their own hand. A suit must be named even when passing. Examples: '4 Blue', 'PASS Red'. When all answers are in, the engine reveals every player's bid amount (or PASS).\n- The highest number wins. A tie goes to the tied player who comes first in priority order.\n- The winner becomes the PITCHER, their number becomes the CONTRACT, and their named suit becomes TRUMP.\n- If all three pass, the dealer becomes the pitcher with a contract of 2, and trump is the suit the dealer named.\n- The engine announces the pitcher, the contract and trump. The suits named by the other two players are NEVER revealed.\n\nTRICKS (each round of a deal): Three cards are played one at a time, starting with the LEADER and continuing in seat order.\n- Leader: in the first trick of a deal, the leader is the pitcher, who must lead a trump card. The pitcher always holds one, because they named a suit from their hand. In later tricks of the deal, the leader is the winner of the previous trick, who may lead any card.\n- Following: each later player must play a card of the led suit if they hold one, but may instead play a trump even if they hold the led suit. A player holding no card of the led suit may play any card.\n- Winning: the trick goes to the highest-ranked trump played. If no trump was played, it goes to the highest-ranked card of the led suit.\n- All played cards are visible to everyone. The three cards go into the trick winner's captured pile.\n\nDEAL SCORING (after the 4th trick of each deal; only cards played this deal count; every dealt card is played):\n- HIGH, 1 point: to the player who captured the highest-ranked trump played.\n- LOW, 1 point: to the player who captured the lowest-ranked trump played. This may be the same card as High. At least one trump is always played, because the first lead is trump.\n- GAME, 1 point: to the player whose captured pile has the most card points. If two or more players tie for most, nobody scores Game.\n- THREE, 3 points: to the player who captured the trump of rank 3, if it was dealt. If it was not dealt, nobody scores it.\n- Each player's deal points are the sum of the categories they won, from 0 to 6.\n- Each of the two non-pitchers adds their deal points to their score.\n- If the pitcher's deal points are at least the contract, the pitcher adds their deal points to their score.\n- Otherwise the pitcher is SET: the pitcher subtracts the contract from their score and does not add their deal points.\n- Scores may go negative. Captured piles are then cleared and the next deal begins.\n\nCOMMUNICATION: There is no table talk. Players communicate only through bids and played cards.\n\nEND: After the 9th deal is scored, the game ends.",
    "objective": "After 9 deals, the player with the highest total score wins. If two or more players tie for the highest total, the game is a draw.",
    "expected_effect": "Players must judge a 4-card hand's worth in a chosen trump, bid high enough to win trump control without overreaching, and read opponents' bid sizes for strength. They must also guess which suits the opponents secretly named, since those suits stay hidden and hint at their holdings. During play, players count cards to locate the Three, High and Low, decide when to trump in, and, as defenders, pool their efforts implicitly to set the pitcher. Simple policies lose. Always passing forfeits trump control, and a passer who is forced to pitch as dealer can still be set. Always bidding 6 is set most deals and loses 6 each time. Playing a random legal card throws away the Three and Low. Talk is omitted because it would only leak hands, and bids and cards already carry the signals worth reasoning about. This is not a cooperation game, so endgame unraveling does not apply. Rotating dealer and priority order remove seat advantage."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 14,
    "choice_steps_per_round": 4,
    "attributes": 18,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
