# 40 design

- time: 2026-10-27T17:33:19+00:00 (49.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 a238fd75193db71a, reply sha256 605238a6d57ae3b1

## Sent

````
Original game: Medici
Players in the original: 2 to 6

Original rules:
Medici is played over 3 days. Set up a face-down commodity deck, adjusting size by player count, and give each player 30-40 florins and a ship for 5 cards (7 in 2p). Each turn the active player draws 1 to 3 cards face-up as a single lot, stopping at will up to 3. The lot is then auctioned: each other player in clockwise order may make one increasing bid or pass, the drawer bids last. Minimum bid is 1 and you cannot bid more than your current florins. Winner pays by decreasing money and loads the whole lot on his ship; lots cannot be split or discarded after purchase and you may not bid if the lot would overfill your ship. If all pass, the lot is discarded. When a ship is full that player sits out the rest of the day. Day ends when all but one ship are full, last player fills free from deck, or deck empties. Score ships by value and by commodity track progress, awarding florins, then start next day. Most florins after day 3 wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: WHAT IS FINE.
- Rounds = 6N, at most 36 (limit 40).
- Steps 17 (limit 20); choice steps 2 (lot size, bid; limit 4).
- Attributes: florins, ship_value, ship_count, 4 good counts, bid, favoured_good, plus round, active_seat, deck, revealed, lot, lot_size, high_bid, high_count, ship_ranks, good_max, giving roughly 19 (limit 20).
- One shuffle per day-opening round (at most 1 random draw per round).
- The bid is a simultaneous poll.
- Everything is decided by arithmetic: day boundaries via round mod 2N, the fill limit ship_count + lot_size <= 5, discard on a tie or a top bid of 0, rank payouts that handle ties, and final most-florins with ties a draw.
- No board, clock or judge is needed.
- No talk is reasonable. Every lot is contested and every bid is announced, so players reason from the public bid history rather than guessing. Talk would only add non-binding cartel chatter.

FAILURE: HIDDEN ELEMENTS. The design hides four things: the deck order, each player's favoured_good, the undealt favour tiles, and florins marked 'private (shown only to the owner)'. That breaks the limit of 3, against the stated count of 3. The florin privacy is also pointless, because every bid and every payout is announced, so anyone can work out every balance.

MINOR WORDING ISSUE. Step 8 says an over-capacity player 'is told before bidding', but step 8 comes after the bid in step 7. The notice belongs in step 7.
- change: Make florins public, or state plainly that they are derivable and not hidden. This brings hidden elements to 3 (deck order, favoured_good, undealt tiles).
- change: Move the notice in step 8 into step 7: before bidding, tell any player with ship_count + lot_size > 5 that only a bid of 0 counts.
The variation that was reviewed: Medici: Sealed Lots: GOODS AND CARDS
There are four goods: Grain, Cloth, Spice and Dye. The deck is 48 cards: for each good, one card of each value listed here, which is 12 cards worth 33 in total per good. The values are 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. Written out per good G: G-0, G-1, G-1, G-2, G-2, G-3, G-3, G-3, G-4, G-4, G-5, G-5.

SETUP
N is the number of players (3-6). Each player starts with:
- 40 florins, private (shown only to the owner);
- ship_value 0 and ship_count 0;
- grain_count, cloth_count, spice_count and dye_count all 0;
- bid 0.
The favour pool depends on N:
- N = 3 or 4: one tile each of Grain, Cloth, Spice and Dye.
- N = 5 or 6: two tiles of each good (8 tiles).
Each player is dealt one tile from the pool at random, face down. This is their secret favoured_good. Undealt tiles stay hidden. Set round = 0. The game lasts 6N rounds, made of 3 days of 2N rounds each.

EACH ROUND, IN THIS ORDER
1. ADVANCE: round = round + 1, exactly once. Then active_seat = ((round - 1) mod N) + 1.
2. NEW DAY DECK (only when round mod 2N = 1): set the deck to the full 48-card list above, then shuffle it once. Any cards left from the previous day are gone.
3. NEW DAY SHIPS (only when round mod 2N = 1): set every player's ship_value and ship_count to 0. Florins and the four cumulative good counts are kept.
4. REVEAL: move the top 3 cards of the deck, in order, into `revealed` as revealed cards 1, 2 and 3. Announce them to everyone. After round 1 the deck holds 45 cards.
5. LOT SIZE (choice): the active seat chooses 1, 2 or 3.
6. CUT: lot_size = that choice. Keep revealed cards 1 to lot_size as the lot and remove the rest from play. Announce the lot, its size and its total value (the sum of its card values).
7. BID (simultaneous choice): every player at the same moment chooses a whole-number bid from 0 up to their florins.
8. VALIDATE: a player's bid becomes 0 if it exceeds their florins or if ship_count + lot_size > 5. A player whose ship cannot fit the lot is told before bidding that only 0 counts.
9. RESOLVE: high_bid = the largest bid. high_count = the number of players who bid high_bid. Announce every player's bid.
10. PAY (only if high_bid > 0 and high_count = 1): the player whose bid equals high_bid loses high_bid florins. The money leaves the game.
11. LOAD (same condition as step 10): that player adds the lot's total value to ship_value and lot_size to ship_count. For each card in the lot, they add 1 to the cumulative count of that card's good. If high_bid = 0 or high_count > 1, the lot is discarded and nobody pays.
12. SHIP RANKS (only when round mod 2N = 0): ship_ranks = [top, second]. Top is the highest ship_value among players. Second is the highest ship_value strictly below top, or 0 if there is none.
13. SHIP PAYOUT (same condition as step 12):
- If top > 0, every player with ship_value = top gains 20 florins.
- If second > 0, every player with ship_value = second gains 10 florins.
14. TRACK MAXIMA (same condition): good_max = the highest grain_count, cloth_count, spice_count and dye_count among players.
15. TRACK PAYOUT (same condition): for each good whose maximum is above 0, every player whose count equals that maximum gains 6 florins.
16. FAVOUR (only when round = 6N): each player gains 3 florins times their cumulative count of their own favoured_good. Then every favoured_good is revealed.
17. END: if round = 6N, the game ends.

No talk phase. Winner: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Medici is a 2-6 player trading auction game played over 3 days. Players draw lots of 1-3 commodity cards, auction each lot in a single once-around bidding pass, and load the lots onto ships of limited capacity. At the end of each day they earn florins for ship value ranking and for majorities on commodity tracks, and the most florins after day 3 wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies lose. Always passing earns no ships and no track money, so the player ends near the starting cash while others gain 20-30 florins per day. Always bidding the maximum overpays and bankrupts the player early. No single bid level dominates, because lot values and ship space vary. The fixed clockwise order with the drawer bidding last gives the drawer an informational edge in each auction, but the seat rotates, so no player has a permanent edge."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "weak",
      "evidence": "Valuing lots, managing ship space and timing majorities reward skill. However, the face-up draws are pure luck, and the drawer's last-bid position can decide close auctions, so the draw order matters a lot over a short game."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Valuing a lot against ship rank, track majorities and remaining cash is never fully solved, and a weak player still earns some payouts."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Almost everything is public: lots, bids, money and ships. Only the deck order is hidden, so the main inference is predicting what opponents can still afford and fit. That is real but thin, and there are no hidden preferences to read."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "Payments, ship ranks, track majorities and the final florin count are all arithmetic."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "It is text-only and turn-based. But the once-around sequential auction with the drawer last, the 'last player fills free' rule, day ends that depend on how many ships are full, the deck size changing with player count, and the 2-player special case all add many steps and variable-length days."
    }
  ],
  "problems": [
    "A once-around sequential auction with the drawer bidding last costs many steps and gives the drawer a structural information edge in every lot.",
    "Day length depends on ship-filling and on the 'last player fills free' rule, which needs conditional blocks the flat step list cannot express.",
    "Very little is hidden: apart from the deck order it is a perfect-information money race, so opponent modelling is shallow.",
    "Luck of the face-up draws and of the bidding position can swamp valuation skill.",
    "Previous variation: four hidden elements (deck order, favoured_good, undealt tiles, private florins) exceed the limit of 3. The florin privacy was pointless anyway, because every bid and payout is announced and balances can be worked out.",
    "Previous variation: the notice to players whose ship cannot fit the lot was placed in the VALIDATE step, after bidding had already happened."
  ],
  "changes": [
    {
      "what": "Replace the sequential auction with one simultaneous sealed bid per lot. The highest unique bid wins and pays its bid. A tie for the top bid, or a top bid of 0, discards the lot.",
      "why": "One simultaneous poll is cheap to build and removes the last-bidder edge. Discarding on ties also punishes predictable bidding.",
      "fixes": "A once-around sequential auction with the drawer bidding last costs many steps and gives the drawer a structural information edge in every lot."
    },
    {
      "what": "Make every day a fixed 2N rounds, with each seat active twice per day. Each round reveals 3 cards and the active seat cuts the lot to 1-3 cards. Ships cap at 5 cards: a player whose ship cannot fit the lot can only bid 0.",
      "why": "Day boundaries become arithmetic on the round number, with no 'fills free' block, and the cut choice keeps the drawer's decision about lot size.",
      "fixes": "Day length depends on ship-filling and on the 'last player fills free' rule, which needs conditional blocks the flat step list cannot express."
    },
    {
      "what": "Deal each player a secret favoured good that pays 3 florins per card of that good collected over the game, revealed only at the end.",
      "why": "Bidding patterns now carry hidden motives that opponents must infer. All four goods have identical card distributions, so no favour is worth more than another.",
      "fixes": "Very little is hidden: apart from the deck order it is a perfect-information money race, so opponent modelling is shallow."
    },
    {
      "what": "Use identical 12-card suits and reshuffle a fresh 48-card deck each day. Pay ship ranking at 20/10 and track majorities at 6 per good every day.",
      "why": "Payout sizes are moderate relative to 40 starting florins, so overpaying is punished and valuation decides more than the draw.",
      "fixes": "Luck of the face-up draws and of the bidding position can swamp valuation skill."
    },
    {
      "what": "Make florins public: every player's balance is announced after every change.",
      "why": "Balances were derivable anyway. This brings hidden elements down to exactly 3: the deck order, each favoured_good, and the undealt favour tiles.",
      "fixes": "Previous variation: four hidden elements (deck order, favoured_good, undealt tiles, private florins) exceed the limit of 3. The florin privacy was pointless anyway, because every bid and payout is announced and balances can be worked out."
    },
    {
      "what": "Move the capacity notice into the BID step: before choosing, any player with ship_count + lot_size > 5 is told that only a bid of 0 will count.",
      "why": "Players get the information before they act, not after.",
      "fixes": "Previous variation: the notice to players whose ship cannot fit the lot was placed in the VALIDATE step, after bidding had already happened."
    }
  ],
  "keeps": [
    "Three trading days with ships that hold 5 cards and empty each day.",
    "The drawer decides how many face-up cards (1-3) form the lot.",
    "Lots are auctioned whole: they cannot be split, and the winner pays money that leaves the game.",
    "Daily payouts for ship value ranking and for majorities on cumulative commodity tracks.",
    "Most florins after day 3 wins."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The core tension of the auction is valuable once it is made simultaneous and fixed-length. A secret favoured good adds inference within the limits."
  },
  "variation": {
    "name": "Medici: Sealed Lots",
    "summary": "Over 3 days, players bid simultaneously and sealed on lots of 1-3 commodity cards, filling 5-card ships. They earn daily ship-rank and track-majority payouts, plus an end bonus for a secret favoured good.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "rules": "GOODS AND CARDS\nThere are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.\n\nSETUP\nN is the number of players (3 to 6). Each player starts with:\n- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.\n- ship_value 0 and ship_count 0.\n- grain_count, cloth_count, spice_count and dye_count all 0.\n- bid 0.\n\nThe favour pool depends on N:\n- N = 3 or 4: one tile each of Grain, Cloth, Spice and Dye (4 tiles).\n- N = 5 or 6: two tiles of each good (8 tiles).\nEach player is dealt one tile from the pool at random, face down. This is their secret favoured_good, known only to that player. Undealt tiles stay hidden from everyone.\n\nSet round = 0. The game lasts 6N rounds, made of 3 days of 2N rounds each.\n\nEACH ROUND, IN THIS ORDER\n1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.\n2. NEW DAY DECK (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone.\n3. NEW DAY SHIPS (only when round mod 2N = 1): set every player's ship_value and ship_count to 0. Florins and the four cumulative good counts are kept.\n4. REVEAL: move the top 3 cards of the deck, in order, into revealed cards 1, 2 and 3, and announce them to everyone.\n5. LOT SIZE (choice): the active seat chooses 1, 2 or 3.\n6. CUT: lot_size = that choice. Revealed cards 1 to lot_size form the lot, and the rest are removed from play. Announce the lot, lot_size and the lot's total value (the sum of its card values).\n7. BID (simultaneous choice): first, every player whose ship_count + lot_size > 5 is told that their ship cannot fit this lot and that only a bid of 0 will count. Then every player, at the same moment, chooses a whole-number bid from 0 up to their florins.\n8. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.\n9. RESOLVE: high_bid = the largest bid. high_count = the number of players who bid high_bid. Announce every player's bid.\n10. PAY (only if high_bid > 0 and high_count = 1): the player who bid high_bid loses high_bid florins. The money leaves the game. Announce that player's new florins.\n11. LOAD (same condition as step 10): that player adds the lot's total value to ship_value and lot_size to ship_count. For each card in the lot, they add 1 to their cumulative count of that card's good. If high_bid = 0 or high_count > 1, the lot is discarded and nobody pays.\n12. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value among players. second = the highest ship_value strictly below top, or 0 if there is none.\n13. SHIP PAYOUT (same condition as step 12): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce the florins.\n14. TRACK MAXIMA (same condition): for each good, good_max = the highest cumulative count of that good among players.\n15. TRACK PAYOUT (same condition): for each good whose maximum is above 0, every player whose count equals that maximum gains 6 florins. Announce the florins.\n16. FAVOUR (only when round = 6N): each player gains 3 florins times their cumulative count of their own favoured_good. Then every favoured_good is revealed and final florins are announced.\n17. END: if round = 6N, the game ends.\n\nThere is no talk phase.",
    "objective": "After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.",
    "expected_effect": "Sealed simultaneous bids with ties discarded make players model rivals' valuations. That valuation depends on each rival's ship space, rank position, track race and a hidden favoured good. Players infer favoured goods from who overbids on which goods, and can bluff by bidding on goods that are not their favour. The active seat's cut trades a richer lot against handing rivals a better prize. No talk is included: bids are already public signals, and with a single winner, talk would mostly be non-binding chatter about bidding low together that adds steps without adding much decision. Simple policies lose. Always bidding 0 earns only the starting 40 florins while others collect payouts. Always bidding everything goes broke on the first lot. Favoured goods are symmetric in value, so they change what to do, not who is ahead."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 17,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 3,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
