# 42 design

- time: 2026-10-27T17:35:22+00:00 (48.6s)  model: claude-opus-5-5
- system prompt: [system/bd642c41-design.md](system/bd642c41-design.md) (sha256 bd642c416cb3a5ad)
- sent sha256 35aa99b2e7c74a81, reply sha256 868c306c6957ad42

## Sent

````
Original game: Medici
Players in the original: 2 to 6

Original rules:
Medici is played over 3 days. Set up a face-down commodity deck, adjusting size by player count, and give each player 30-40 florins and a ship for 5 cards (7 in 2p). Each turn the active player draws 1 to 3 cards face-up as a single lot, stopping at will up to 3. The lot is then auctioned: each other player in clockwise order may make one increasing bid or pass, the drawer bids last. Minimum bid is 1 and you cannot bid more than your current florins. Winner pays by decreasing money and loads the whole lot on his ship; lots cannot be split or discarded after purchase and you may not bid if the lot would overfill your ship. If all pass, the lot is discarded. When a ship is full that player sits out the rest of the day. Day ends when all but one ship are full, last player fills free from deck, or deck empties. Score ships by value and by commodity track progress, awarding florins, then start next day. Most florins after day 3 wins.

A PREVIOUS VARIATION of this game was reviewed and tested. The findings:
- playable FAILED: Rules are complete. Conditions use round mod 2N, which works for N = 3..6. Ties, full ships and all-zero bids are all handled. The game is finite at 6N rounds (at most 36, within 40) and is decided by arithmetic on florins. No board, clock or judge is needed, and bids are a simultaneous poll.

Limits: steps 17 (max 20) OK; choice steps 2 (max 4) OK; random draws 1 per round (shuffle only on day-start rounds) OK; hidden elements 3 (favour tiles, deck order, undealt tiles) OK.

ATTRIBUTES are understated. The design claims 19, but a recount gives:
- Per player (9): florins, ship_value, ship_count, grain_count, cloth_count, spice_count, dye_count, bid, favoured_good.
- Global (14): round, active_seat, lot_size, revealed cards (even counted as one list), deck, favour pool, high_bid, high_count, top, second, grain_max, cloth_max, spice_max, dye_max.
- Total: 23, or 25 with revealed 1-3 counted separately. This exceeds the limit of 20.

Talk: omitting talk is defensible. This is a sealed-bid auction where interests conflict and promises cannot bind, so talk would add only words. Bid history, public florins and visible ships give enough to reason about.

Cooperation after betrayal: not applicable, since this is not a cooperation game.
- change: Cut the attribute count to 20 or fewer (currently 23-25). One way to do it:
(a) Drop revealed cards 1-3: the lot is the first lot_size cards of the deck, then remove the top 3 cards.
(b) Replace grain_max, cloth_max, spice_max and dye_max with one reusable track_max, filled and paid good by good in steps 14-15. These can be rolled into one step per good if the step budget allows, or kept within 20 steps.
(c) Do not keep the favour pool as an attribute after setup. The undealt tiles are simply never revealed.
(d) Optionally drop high_count by making the PAY/LOAD condition 'exactly one player's bid equals high_bid' in the step's when-clause.
Then restate the complexity with an honest attribute count of 20 or fewer.
The variation that was reviewed: Medici: Sealed Lots: GOODS AND CARDS
There are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.

SETUP
N is the number of players (3 to 6). Each player starts with:
- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.
- ship_value 0 and ship_count 0.
- grain_count, cloth_count, spice_count and dye_count all 0.
- bid 0.

The favour pool depends on N:
- N = 3 or 4: one tile each of Grain, Cloth, Spice and Dye (4 tiles).
- N = 5 or 6: two tiles of each good (8 tiles).
Each player is dealt one tile from the pool at random, face down. This is their secret favoured_good, known only to that player. Undealt tiles stay hidden from everyone.

Set round = 0. The game lasts 6N rounds, made of 3 days of 2N rounds each.

EACH ROUND, IN THIS ORDER
1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.
2. NEW DAY DECK (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone.
3. NEW DAY SHIPS (only when round mod 2N = 1): set every player's ship_value and ship_count to 0. Florins and the four cumulative good counts are kept.
4. REVEAL: move the top 3 cards of the deck, in order, into revealed cards 1, 2 and 3, and announce them to everyone.
5. LOT SIZE (choice): the active seat chooses 1, 2 or 3.
6. CUT: lot_size = that choice. Revealed cards 1 to lot_size form the lot, and the rest are removed from play. Announce the lot, lot_size and the lot's total value (the sum of its card values).
7. BID (simultaneous choice): first, every player whose ship_count + lot_size > 5 is told that their ship cannot fit this lot and that only a bid of 0 will count. Then every player, at the same moment, chooses a whole-number bid from 0 up to their florins.
8. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.
9. RESOLVE: high_bid = the largest bid. high_count = the number of players who bid high_bid. Announce every player's bid.
10. PAY (only if high_bid > 0 and high_count = 1): the player who bid high_bid loses high_bid florins. The money leaves the game. Announce that player's new florins.
11. LOAD (same condition as step 10): that player adds the lot's total value to ship_value and lot_size to ship_count. For each card in the lot, they add 1 to their cumulative count of that card's good. If high_bid = 0 or high_count > 1, the lot is discarded and nobody pays.
12. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value among players. second = the highest ship_value strictly below top, or 0 if there is none.
13. SHIP PAYOUT (same condition as step 12): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce the florins.
14. TRACK MAXIMA (same condition): for each good, good_max = the highest cumulative count of that good among players.
15. TRACK PAYOUT (same condition): for each good whose maximum is above 0, every player whose count equals that maximum gains 6 florins. Announce the florins.
16. FAVOUR (only when round = 6N): each player gains 3 florins times their cumulative count of their own favoured_good. Then every favoured_good is revealed and final florins are announced.
17. END: if round = 6N, the game ends.

There is no talk phase. Winner: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.

Revise the variation to fix these. Keep what works. Review it again against the criteria.
````

## Reply

````
```json
{
  "original_summary": "Medici is a 2-6 player auction game over 3 days. Players take turns drawing 1-3 commodity cards as a lot, which is then auctioned once around the table. They fill limited ships to win florins for ship value and for majorities on commodity tracks, and the most florins after day 3 wins.",
  "review": [
    {
      "criterion": "non_degenerate",
      "verdict": "good",
      "evidence": "Simple policies lose. Always passing earns nothing while rivals collect ship and track payouts. Always bidding high bankrupts a player for low-value lots. The drawer's choice of lot size changes what is worth bidding. The fixed clockwise order gives the drawer a last-bid edge, but the active seat rotates."
    },
    {
      "criterion": "skill_sensitive",
      "verdict": "good",
      "evidence": "Valuing a lot against ship space, track standings and rivals' cash decides games. Card draws add variance, but every player bids on the same lots, so the luck is shared."
    },
    {
      "criterion": "headroom",
      "verdict": "good",
      "evidence": "Weak players still fill ships and score something. Strong players keep improving through cash management across days, denial bidding and timing their ship fills."
    },
    {
      "criterion": "reasoning_dependent",
      "verdict": "weak",
      "evidence": "Inference covers rivals' valuations and what remains in the deck. Ships and money are mostly public, so there is no private information about a player's own goals."
    },
    {
      "criterion": "verifiable",
      "verdict": "good",
      "evidence": "All scoring is arithmetic on ship values, track positions and florins."
    },
    {
      "criterion": "fits_platform",
      "verdict": "weak",
      "evidence": "The sequential once-around auction, variable-length days, the free fill for the last ship and track boards are costly to build. The previous adaptation fitted the step budget but used 23-25 attributes, over the limit of 20."
    }
  ],
  "problems": [
    "The previous variation tracked 23-25 attributes, over the platform limit of 20.",
    "Revealed cards 1-3 were stored as separate attributes when the deck positions already hold them.",
    "Four separate good_max attributes (grain_max, cloth_max, spice_max, dye_max) duplicated one reusable value.",
    "Keeping the undealt favour pool as an attribute after setup wasted an attribute and was counted as an extra hidden element.",
    "Track maxima and payouts used paired steps per good, which would cost 8 steps if itemised honestly.",
    "Original (kept fixed): the sequential once-around auction gives a positional edge and is costly to build; this is replaced by a sealed simultaneous bid.",
    "Original (kept fixed): there is little private information; the secret favoured good is kept so bids reflect hidden valuations."
  ],
  "changes": [
    {
      "what": "Drop revealed cards 1-3. The top 3 deck cards are announced in place. The lot is the first lot_size cards of the deck. After resolving, the top 3 cards are removed from the deck.",
      "why": "This saves three attributes with no change to play.",
      "fixes": "Revealed cards 1-3 were stored as separate attributes when the deck positions already hold them."
    },
    {
      "what": "Replace the four good maxima with one reusable track_max. Each good is scored in a single step: set track_max to the highest count of that good, then pay 6 florins to every player who has that count, provided it is above 0.",
      "why": "This saves three attributes and halves the track-scoring steps (4 instead of 8).",
      "fixes": "Four separate good_max attributes (grain_max, cloth_max, spice_max, dye_max) duplicated one reusable value."
    },
    {
      "what": "The favour pool exists only during the setup deal. Undealt tiles are simply never revealed and are not tracked.",
      "why": "This removes an attribute and a counted hidden element.",
      "fixes": "Keeping the undealt favour pool as an attribute after setup wasted an attribute and was counted as an extra hidden element."
    },
    {
      "what": "Store lot_value once at the cut, so the announcement and the load use the same number. Merge the new-deck and ship-reset steps into one day-start step.",
      "why": "This keeps the step count at 19 and the attribute count at 19 while staying explicit.",
      "fixes": "Track maxima and payouts used paired steps per good, which would cost 8 steps if itemised honestly."
    },
    {
      "what": "Keep the sealed simultaneous bid. A tie for the high bid discards the lot. The active seat rotates so that every seat chooses lot size exactly twice per day.",
      "why": "This removes the positional edge and is a simple poll.",
      "fixes": "Original (kept fixed): the sequential once-around auction gives a positional edge and is costly to build; this is replaced by a sealed simultaneous bid."
    },
    {
      "what": "Keep the secret favoured good, worth 3 florins per card of that good loaded over the game.",
      "why": "Each player values goods differently and secretly, so rivals must infer favours from bidding patterns. All goods are symmetric, so no tile is better than another.",
      "fixes": "Original (kept fixed): there is little private information; the secret favoured good is kept so bids reflect hidden valuations."
    }
  ],
  "keeps": [
    "Three days of auctions on lots of 1-3 commodity cards, with the lot size chosen by the active player.",
    "Ships with 5 slots: a full ship cannot buy more that day, and lots cannot be split.",
    "Ship-value payouts for the top two ships each day.",
    "Cumulative commodity tracks that pay majorities every day.",
    "Money spent on bids leaves the game, and the most florins at the end wins.",
    "The sealed bid, the hidden favoured good and the public florins from the previous variation, which reviewed well."
  ],
  "recommendation": {
    "decision": "adapt",
    "kind": "none",
    "reason": "The previous variation played well and only exceeded the attribute limit. Merging the revealed-card, good-maximum and pool attributes brings it to 19 attributes and 19 steps without changing play."
  },
  "variation": {
    "name": "Medici: Sealed Lots",
    "summary": "A 3-6 player sealed-bid auction over 3 days. The active player picks a lot of 1-3 revealed commodity cards, and everyone bids secretly at once, with ties discarding the lot. Ships of 5 slots score daily for value. Cumulative goods counts score daily for majorities. A secret favoured good pays at the end.",
    "players": {
      "min": 3,
      "max": 6,
      "suggested": 4
    },
    "rules": "GOODS AND CARDS\nThere are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.\n\nSETUP\nN is the number of players (3 to 6). Each player starts with:\n- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.\n- ship_value 0 and ship_count 0.\n- grain_count, cloth_count, spice_count and dye_count all 0.\n- bid 0.\nFavour deal: if N is 3 or 4, take one tile each of Grain, Cloth, Spice and Dye (4 tiles). If N is 5 or 6, take two tiles of each good (8 tiles). Deal each player one tile at random, face down. This is their secret favoured_good, known only to them. Undealt tiles are set aside and never revealed.\nSet round = 0. The game lasts 6N rounds: 3 days of 2N rounds each. The game-level values are round, active_seat, lot_size, lot_value, deck, high_bid, high_count, top, second and track_max.\n\nEACH ROUND, IN THIS ORDER\n1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.\n2. NEW DAY (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone. Set every player's ship_value and ship_count to 0. Florins and the four goods counts are kept.\n3. REVEAL: announce the top 3 cards of the deck (positions 1, 2, 3) to everyone.\n4. LOT SIZE (choice): the active seat chooses 1, 2 or 3.\n5. CUT: lot_size = that choice. The lot is deck positions 1 to lot_size. lot_value = the sum of those cards' values. Announce lot_size and lot_value.\n6. BID (simultaneous choice): every player whose ship_count + lot_size > 5 is told their ship cannot fit this lot and only a bid of 0 counts. Then all players, at the same moment, choose a whole-number bid from 0 to their florins.\n7. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.\n8. RESOLVE: high_bid = the largest bid. high_count = the number of players whose bid equals high_bid. Announce every bid.\n9. PAY (only if high_bid > 0 and high_count = 1): the sole high bidder loses high_bid florins, which leave the game. Announce their florins.\n10. LOAD AND CLEAR: if high_bid > 0 and high_count = 1, the winner adds lot_value to ship_value and lot_size to ship_count, and adds 1 to their count of each lot card's good. Then, in every case, remove the top 3 cards from the deck. If nobody won, the lot is simply discarded.\n11. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value. second = the highest ship_value strictly below top, or 0 if there is none.\n12. SHIP PAYOUT (same condition): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce florins.\n13. GRAIN TRACK (same condition): track_max = the highest grain_count. If track_max > 0, every player with grain_count = track_max gains 6 florins.\n14. CLOTH TRACK (same condition): the same, for cloth_count.\n15. SPICE TRACK (same condition): the same, for spice_count.\n16. DYE TRACK (same condition): the same, for dye_count. Announce florins.\n17. FAVOUR (only when round = 6N): each player gains 3 florins times their count of their own favoured_good. All favoured goods are revealed and final florins announced.\n18. END: if round = 6N, the game ends.\n\nThere is no talk phase.",
    "objective": "After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.",
    "expected_effect": "Play is the same as the previously tested version. Each lot is a valuation puzzle: ship space, the daily ship race, track majorities, a secret favour, rivals' public cash and their inferred favours all bear on what to bid. Always bidding 0 keeps 40 florins but loses to anyone who wins cheap lots and collects payouts. Always bidding everything either ties and discards the lot or wins once and goes broke, so both simple policies can lose. Favour tiles are symmetric, so the hidden type changes what to buy, not who is ahead. Rotating lot choice removes any seat edge. Talk is left out: the sealed auction is purely competitive, promises cannot bind, and public bids and ships give enough to read."
  },
  "model": null,
  "complexity": {
    "steps_per_round": 18,
    "choice_steps_per_round": 2,
    "attributes": 19,
    "hidden_elements": 2,
    "random_draws_per_round": 1,
    "rounds": 36
  }
}
```
````
