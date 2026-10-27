# 46 spec

- time: 2026-10-27T17:38:22+00:00 (39.2s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 84bef49ae5ea062f, reply sha256 0018d33c80a29c48

## Sent

````
Game: Medici: Sealed Lots
Players in the source: 3 to 6
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
GOODS AND CARDS
There are four goods: Grain, Cloth, Spice and Dye. The deck has 48 cards. For each good there is one card of each of these values: 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5. That is 12 cards per good, worth 33 in total per good.

SETUP
N is the number of players (3 to 6). Each player starts with:
- 40 florins. Florins are PUBLIC: every player's florins are announced at the start and after every change.
- ship_value 0 and ship_count 0.
- grain_count, cloth_count, spice_count and dye_count all 0.
- bid 0.
Favour deal: if N is 3 or 4, take one tile each of Grain, Cloth, Spice and Dye (4 tiles). If N is 5 or 6, take two tiles of each good (8 tiles). Deal each player one tile at random, face down. This is their secret favoured_good, known only to them. Undealt tiles are set aside and never revealed.
Set round = 0. The game lasts 6N rounds: 3 days of 2N rounds each. The game-level values are round, active_seat, lot_size, lot_value, deck, high_bid, high_count, top, second and track_max.

EACH ROUND, IN THIS ORDER
1. ADVANCE: round = round + 1. Then active_seat = ((round - 1) mod N) + 1.
2. NEW DAY (only when round mod 2N = 1): set the deck to the full 48-card list and shuffle it once. Any cards left from the previous day are gone. Set every player's ship_value and ship_count to 0. Florins and the four goods counts are kept.
3. REVEAL: announce the top 3 cards of the deck (positions 1, 2, 3) to everyone.
4. LOT SIZE (choice): the active seat chooses 1, 2 or 3.
5. CUT: lot_size = that choice. The lot is deck positions 1 to lot_size. lot_value = the sum of those cards' values. Announce lot_size and lot_value.
6. BID (simultaneous choice): every player whose ship_count + lot_size > 5 is told their ship cannot fit this lot and only a bid of 0 counts. Then all players, at the same moment, choose a whole-number bid from 0 to their florins.
7. VALIDATE: a bid becomes 0 if it exceeds the player's florins or if ship_count + lot_size > 5.
8. RESOLVE: high_bid = the largest bid. high_count = the number of players whose bid equals high_bid. Announce every bid.
9. PAY (only if high_bid > 0 and high_count = 1): the sole high bidder loses high_bid florins, which leave the game. Announce their florins.
10. LOAD AND CLEAR: if high_bid > 0 and high_count = 1, the winner adds lot_value to ship_value and lot_size to ship_count, and adds 1 to their count of each lot card's good. Then, in every case, remove the top 3 cards from the deck. If nobody won, the lot is simply discarded.
11. SHIP RANKS (only when round mod 2N = 0): top = the highest ship_value. second = the highest ship_value strictly below top, or 0 if there is none.
12. SHIP PAYOUT (same condition): if top > 0, every player with ship_value = top gains 20 florins. If second > 0, every player with ship_value = second gains 10 florins. Announce florins.
13. GRAIN TRACK (same condition): track_max = the highest grain_count. If track_max > 0, every player with grain_count = track_max gains 6 florins.
14. CLOTH TRACK (same condition): the same, for cloth_count.
15. SPICE TRACK (same condition): the same, for spice_count.
16. DYE TRACK (same condition): the same, for dye_count. Announce florins.
17. FAVOUR (only when round = 6N): each player gains 3 florins times their count of their own favoured_good. All favoured goods are revealed and final florins announced.
18. END: if round = 6N, the game ends.

There is no talk phase.

How the winner is decided: After round 6N, the player with the most florins wins. If two or more players tie for the most florins, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Medici: Sealed Lots",
  "summary": "Players bid sealed florins for lots of goods cards to fill their ships. Ships pay out at the end of each of 3 days, goods tracks pay bonuses, and a secret favoured good pays at the end. The most florins wins.",
  "players": {"min": 3, "max": 6, "suggested": 4},
  "parameters": {
    "starting_florins": 40,
    "deck_size": 48,
    "goods": 4,
    "cards_per_good": 12,
    "card_values_per_good": [0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5],
    "value_per_good_total": 33,
    "reveal_count": 3,
    "lot_size_min": 1,
    "lot_size_max": 3,
    "cards_cleared_per_round": 3,
    "ship_capacity": 5,
    "days": 3,
    "rounds_per_day_per_player": 2,
    "total_rounds_per_player": 6,
    "ship_first_payout": 20,
    "ship_second_payout": 10,
    "track_bonus": 6,
    "favour_multiplier": 3,
    "favour_tiles_per_good_small": 1,
    "favour_tiles_per_good_large": 2,
    "small_table_max": 4,
    "bid_min": 0
  },
  "attributes": {
    "player": [
      {"key": "florins", "type": "number", "visible": "public", "initial": 40, "meaning": "Money and score. It is announced at the start and after every change.", "observable": true},
      {"key": "ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of card values loaded on the ship today. It is reset each new day.", "observable": true},
      {"key": "ship_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards loaded on the ship today, at most 5. It is reset each new day.", "observable": false},
      {"key": "grain_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Grain cards won over the whole game.", "observable": false},
      {"key": "cloth_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Cloth cards won over the whole game.", "observable": false},
      {"key": "spice_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Spice cards won over the whole game.", "observable": false},
      {"key": "dye_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Dye cards won over the whole game.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's sealed bid. It is gathered by a simultaneous poll and announced at resolve.", "observable": false},
      {"key": "favoured_good", "type": "text", "visible": "ally", "initial": "", "meaning": "Secret favour tile (Grain, Cloth, Spice or Dye), known only to its owner. It is revealed at the end of the game.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Round counter, from 1 to 6N.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that chooses the lot size this round: ((round-1) mod N)+1.", "observable": false},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Today's ordered deck of cards coded good:value, for example Spice:3. Position 1 is the top.", "observable": false},
      {"key": "revealed", "type": "list", "visible": "public", "initial": [], "meaning": "The top 3 deck cards shown this round.", "observable": false},
      {"key": "lot_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in this round's lot (1 to 3).", "observable": false},
      {"key": "lot_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the values of the lot cards.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Largest valid bid this round.", "observable": false},
      {"key": "high_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players whose bid equals high_bid.", "observable": false},
      {"key": "top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest ship_value at the end of the day.", "observable": false},
      {"key": "second", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest ship_value strictly below top, or 0 if there is none.", "observable": false},
      {"key": "track_max", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest count on the goods track being scored.", "observable": false},
      {"key": "favour_tiles", "type": "list", "visible": "none", "initial": [], "meaning": "Favour tiles to deal from. Undealt tiles stay here and are never revealed.", "observable": false}
    ]
  },
  "setup": [
    "Every player starts with florins 40, ship_value 0, ship_count 0, grain_count 0, cloth_count 0, spice_count 0, dye_count 0 and bid 0.",
    "favour_tiles is set to one tile each of Grain, Cloth, Spice and Dye if N is 3 or 4, or to two tiles of each good (8 tiles) if N is 5 or 6.",
    "Each player draws one tile at random from favour_tiles into favoured_good, visible only to that player. The remaining tiles stay hidden in favour_tiles.",
    "round is set to 0. The game lasts 6N rounds: 3 days of 2N rounds each.",
    "Every player's florins are announced."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round = round + 1; active_seat = ((round - 1) mod N) + 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 1: deck is rebuilt as the full 48-card list (for each of Grain, Cloth, Spice, Dye the values 0,1,1,2,2,3,3,3,4,4,5,5), placed in random order by drawing every card at random, and any old cards are discarded. Every player's ship_value = 0 and ship_count = 0. Florins and goods counts are kept."},
    {"action": "update", "who": "all players", "answer": null, "effect": "revealed = deck positions 1, 2 and 3. These are announced to everyone."},
    {"action": "ask", "who": "the player at active_seat", "answer": "a choice of 1, 2 or 3", "effect": "Records the lot size choice."},
    {"action": "update", "who": "all players", "answer": null, "effect": "lot_size = the choice; lot_value = the sum of the values of deck positions 1..lot_size. lot_size and lot_value are announced."},
    {"action": "tell", "who": "every player with ship_count + lot_size > 5", "answer": null, "effect": "Tells each such player that their ship cannot fit this lot and only a bid of 0 counts."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to the player's florins", "effect": "bid = the answer. All players answer simultaneously, and no one sees a bid until all are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: if bid > florins or ship_count + lot_size > 5 then bid = 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "high_bid = the maximum bid; high_count = the number of players with bid = high_bid. Every bid is announced."},
    {"action": "update", "who": "the sole high bidder", "answer": null, "effect": "When high_bid > 0 and high_count = 1: the player with bid = high_bid has florins = florins - high_bid (these florins leave the game), and their florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When high_bid > 0 and high_count = 1: the winner's ship_value += lot_value and ship_count += lot_size, and the winner gains +1 grain_count/cloth_count/spice_count/dye_count for each lot card of that good. In every case, the top 3 cards are removed from deck (an unwon lot is simply discarded)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: top = the maximum ship_value; second = the maximum ship_value strictly below top, or 0 if there is none."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: if top > 0, every player with ship_value = top gains 20 florins; if second > 0, every player with ship_value = second gains 10 florins. Florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum grain_count; if track_max > 0, every player with grain_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum cloth_count; if track_max > 0, every player with cloth_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum spice_count; if track_max > 0, every player with spice_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum dye_count; if track_max > 0, every player with dye_count = track_max gains 6 florins. Florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round = 6N: each player gains florins += 3 × (their count of their favoured_good). Every favoured_good is revealed to all and final florins are announced."},
    {"action": "check", "who": "all players", "answer": null, "effect": "The game ends if round = 6N; otherwise play continues."}
  ],
  "ending": {
    "condition": "round = 6 * N",
    "rank_by": "you.florins",
    "decided_by": "Each player's standing is their florins after round 6N. The most florins wins. Players tied for the most florins share the result, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has 40 florins, ship_value 0, ship_count 0 and all four goods counts 0."},
    {"id": "R2", "text": "When N is 3 or 4, then favour tiles are 1 of each good (4 tiles); when N is 5 or 6, then they are 2 of each good (8 tiles), and each player is dealt exactly 1 tile, seen only by that player."},
    {"id": "R3", "text": "When a round begins, then round increases by 1 and active_seat = ((round - 1) mod N) + 1."},
    {"id": "R4", "text": "When round mod 2N = 1, then the deck is reset to the full 48 cards (12 per good, values 0,1,1,2,2,3,3,3,4,4,5,5) in random order, and every ship_value and ship_count is set to 0, while florins and goods counts are kept."},
    {"id": "R5", "text": "When a round's reveal happens, then the top 3 deck cards are shown to everyone."},
    {"id": "R6", "text": "When the active seat chooses a lot size, then it is 1, 2 or 3, and lot_value equals the sum of the values of the top lot_size cards."},
    {"id": "R7", "text": "When bids are made, then all players bid simultaneously with a whole number from 0 to their florins."},
    {"id": "R8", "text": "When a player's ship_count + lot_size > 5, then they are told only 0 counts, and their bid is set to 0."},
    {"id": "R9", "text": "When a bid exceeds the bidder's florins, then it becomes 0."},
    {"id": "R10", "text": "When high_bid > 0 and exactly one player bid high_bid, then that player loses high_bid florins, adds lot_value to ship_value and lot_size to ship_count, and gains 1 in the matching goods count per lot card."},
    {"id": "R11", "text": "When high_bid = 0 or two or more players tie at high_bid, then nobody pays and the lot is discarded."},
    {"id": "R12", "text": "When any round ends its load step, then the top 3 cards are removed from the deck regardless of lot size."},
    {"id": "R13", "text": "When round mod 2N = 0 and top > 0, then every player with ship_value = top gains 20 florins."},
    {"id": "R14", "text": "When round mod 2N = 0 and second > 0, then every player with ship_value = second (the highest value strictly below top) gains 10 florins."},
    {"id": "R15", "text": "When round mod 2N = 0, then for each of grain, cloth, spice and dye, if the highest count is > 0, every player with that highest count gains 6 florins."},
    {"id": "R16", "text": "When round = 6N, then each player gains 3 florins per card of their favoured_good, and all favoured goods are revealed."},
    {"id": "R17", "text": "When round = 6N, then the game ends and the player with the most florins wins, with players tied for the most sharing the result (a draw)."}
  ],
  "offers": [
    {"question": "Lot size", "who": "the player at active_seat only", "options": "1, 2 or 3"},
    {"question": "Sealed bid", "who": "all players", "options": "Any whole number from 0 to the player's current florins. A player whose ship_count + lot_size > 5 is offered the same range but is told that only a bid of 0 counts."}
  ],
  "choices": [
    {"what": "3 to 6 players, suggested 4", "why": "The designer's suggested size of 4 is kept. The minimum is 3 because the second-place ship payout and sealed-bid ties need at least two rivals. The maximum is 6 because the 48-card deck supplies 6N = 36 cards per day at N=6, and a larger table would leave each player too few auctions to matter."},
    {"what": "No talk phase", "why": "The rules state there is no talk phase."},
    {"what": "Card coding as good:value text in the deck list", "why": "Lets the engine sum lot values and count goods per lot card arithmetically."},
    {"what": "Ship values, ship counts and goods counts are public", "why": "Every lot's cards, value and winning bid are announced, so these are already derivable by all players."},
    {"what": "Strategy check", "why": "Players must value lots against their ship capacity, contest the ship ranks and goods tracks, hide their favoured good while chasing it, and avoid tied high bids that void a lot."}
  ],
  "simplifications": [
    {"what": "Shuffling the deck is done by drawing all 48 cards at random into an ordered list", "why": "The engine's randomness is random draws, and the result is an equivalent shuffle."},
    {"what": "A tie for the most florins is a shared win rather than a declared draw", "why": "The engine has no separate draw; players level at the top share the win."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Medici: Sealed Lots",
  "summary": "Players bid sealed florins for lots of goods cards to fill their ships. Ships pay out at the end of each of 3 days, goods tracks pay bonuses, and a secret favoured good pays at the end. The most florins wins.",
  "players": {"min": 3, "max": 6, "suggested": 4},
  "parameters": {
    "starting_florins": 40,
    "deck_size": 48,
    "goods": 4,
    "cards_per_good": 12,
    "cards_of_value_0_per_good": 1,
    "cards_of_value_1_per_good": 2,
    "cards_of_value_2_per_good": 2,
    "cards_of_value_3_per_good": 3,
    "cards_of_value_4_per_good": 2,
    "cards_of_value_5_per_good": 2,
    "value_per_good_total": 33,
    "reveal_count": 3,
    "lot_size_min": 1,
    "lot_size_max": 3,
    "cards_cleared_per_round": 3,
    "ship_capacity": 5,
    "days": 3,
    "rounds_per_day_per_player": 2,
    "total_rounds_per_player": 6,
    "ship_first_payout": 20,
    "ship_second_payout": 10,
    "track_bonus": 6,
    "favour_multiplier": 3,
    "favour_tiles_per_good_small": 1,
    "favour_tiles_per_good_large": 2,
    "small_table_max": 4,
    "bid_min": 0
  },
  "attributes": {
    "player": [
      {"key": "florins", "type": "number", "visible": "public", "initial": 40, "meaning": "Money and score. It is announced at the start and after every change.", "observable": true},
      {"key": "ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the card values loaded on the ship today. It is reset each new day.", "observable": true},
      {"key": "ship_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards loaded on the ship today, at most 5. It is reset each new day.", "observable": false},
      {"key": "grain_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Grain cards won over the whole game.", "observable": false},
      {"key": "cloth_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Cloth cards won over the whole game.", "observable": false},
      {"key": "spice_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Spice cards won over the whole game.", "observable": false},
      {"key": "dye_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Dye cards won over the whole game.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's sealed bid. It is gathered by a simultaneous poll and announced at resolve.", "observable": false},
      {"key": "favoured_good", "type": "text", "visible": "ally", "initial": "", "meaning": "Secret favour tile (Grain, Cloth, Spice or Dye), known only to its owner. It is revealed at the end of the game.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Round counter, from 1 to 6N.", "observable": true},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that chooses the lot size this round: ((round-1) mod N)+1.", "observable": false},
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "Today's ordered deck of cards, each coded good:value (for example Spice:3). Position 1 is the top.", "observable": false},
      {"key": "revealed", "type": "list", "visible": "public", "initial": [], "meaning": "The top 3 deck cards shown this round.", "observable": false},
      {"key": "lot_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in this round's lot (1 to 3).", "observable": false},
      {"key": "lot_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the values of the lot cards.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Largest valid bid this round.", "observable": false},
      {"key": "high_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of players whose bid equals high_bid.", "observable": false},
      {"key": "top", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest ship_value at the end of the day.", "observable": false},
      {"key": "second", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest ship_value strictly below top, or 0 if there is none.", "observable": false},
      {"key": "track_max", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest count on the goods track being scored.", "observable": false},
      {"key": "favour_tiles", "type": "list", "visible": "none", "initial": [], "meaning": "Favour tiles to deal from. Undealt tiles stay here and are never revealed.", "observable": false}
    ]
  },
  "setup": [
    "Every player starts with florins 40, ship_value 0, ship_count 0, grain_count 0, cloth_count 0, spice_count 0, dye_count 0 and bid 0.",
    "favour_tiles is set to one tile each of Grain, Cloth, Spice and Dye if N is 3 or 4, or to two tiles of each good (8 tiles) if N is 5 or 6.",
    "Each player draws one tile at random from favour_tiles into favoured_good, visible only to that player. The remaining tiles stay hidden in favour_tiles.",
    "round is set to 0. The game lasts 6N rounds: 3 days of 2N rounds each.",
    "Every player's florins are announced."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round = round + 1; active_seat = ((round - 1) mod N) + 1."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 1: deck is rebuilt as the full 48-card list (for each of Grain, Cloth, Spice and Dye, the values 0,1,1,2,2,3,3,3,4,4,5,5) and placed in random order by drawing every card at random. Any old cards are discarded. Every player's ship_value = 0 and ship_count = 0. Florins and goods counts are kept."},
    {"action": "update", "who": "all players", "answer": null, "effect": "revealed = deck positions 1, 2 and 3. These are announced to everyone."},
    {"action": "ask", "who": "the player at active_seat", "answer": "a choice of 1, 2 or 3", "effect": "Records the lot size choice."},
    {"action": "update", "who": "all players", "answer": null, "effect": "lot_size = the choice; lot_value = the sum of the values of deck positions 1..lot_size. lot_size and lot_value are announced."},
    {"action": "tell", "who": "every player with ship_count + lot_size > 5", "answer": null, "effect": "Tells each such player that their ship cannot fit this lot and only a bid of 0 counts."},
    {"action": "poll", "who": "all players", "answer": "a whole number from 0 to the player's florins", "effect": "bid = the answer. All players answer simultaneously, and no one sees a bid until all are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each player: if bid > florins or ship_count + lot_size > 5, then bid = 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "high_bid = the maximum bid; high_count = the number of players with bid = high_bid. Every bid is announced."},
    {"action": "update", "who": "the sole high bidder", "answer": null, "effect": "When high_bid > 0 and high_count = 1: the player with bid = high_bid has florins = florins - high_bid (these florins leave the game), and their florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When high_bid > 0 and high_count = 1: the winner's ship_value += lot_value and ship_count += lot_size, and the winner gains +1 grain_count, cloth_count, spice_count or dye_count for each lot card of that good. In every case, the top 3 cards are removed from deck (an unwon lot is simply discarded)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: top = the maximum ship_value; second = the maximum ship_value strictly below top, or 0 if there is none."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: if top > 0, every player with ship_value = top gains 20 florins; if second > 0, every player with ship_value = second gains 10 florins. Florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum grain_count; if track_max > 0, every player with grain_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum cloth_count; if track_max > 0, every player with cloth_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum spice_count; if track_max > 0, every player with spice_count = track_max gains 6 florins."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round mod 2N = 0: track_max = the maximum dye_count; if track_max > 0, every player with dye_count = track_max gains 6 florins. Florins are announced."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round = 6N: each player gains florins += 3 × (their count of their favoured_good). Every favoured_good is revealed to all, and final florins are announced."},
    {"action": "check", "who": "all players", "answer": null, "effect": "The game ends if round = 6N; otherwise play continues."}
  ],
  "ending": {
    "condition": "round = 6 * N",
    "rank_by": "you.florins",
    "decided_by": "Each player's standing is their florins after round 6N. The most florins wins. Players tied for the most florins share the result, which stands for the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has 40 florins, ship_value 0, ship_count 0 and all four goods counts 0."},
    {"id": "R2", "text": "When N is 3 or 4, then the favour tiles are 1 of each good (4 tiles); when N is 5 or 6, then they are 2 of each good (8 tiles). Each player is dealt exactly 1 tile, seen only by that player."},
    {"id": "R3", "text": "When a round begins, then round increases by 1 and active_seat = ((round - 1) mod N) + 1."},
    {"id": "R4", "text": "When round mod 2N = 1, then the deck is reset to the full 48 cards (12 per good, values 0,1,1,2,2,3,3,3,4,4,5,5) in random order, and every ship_value and ship_count is set to 0, while florins and goods counts are kept."},
    {"id": "R5", "text": "When a round's reveal happens, then the top 3 deck cards are shown to everyone."},
    {"id": "R6", "text": "When the active seat chooses a lot size, then it is 1, 2 or 3, and lot_value equals the sum of the values of the top lot_size cards."},
    {"id": "R7", "text": "When bids are made, then all players bid simultaneously with a whole number from 0 to their florins."},
    {"id": "R8", "text": "When a player's ship_count + lot_size > 5, then they are told that only 0 counts, and their bid is set to 0."},
    {"id": "R9", "text": "When a bid exceeds the bidder's florins, then it becomes 0."},
    {"id": "R10", "text": "When high_bid > 0 and exactly one player bid high_bid, then that player loses high_bid florins, adds lot_value to ship_value and lot_size to ship_count, and gains 1 in the matching goods count per lot card."},
    {"id": "R11", "text": "When high_bid = 0, or two or more players tie at high_bid, then nobody pays and the lot is discarded."},
    {"id": "R12", "text": "When any round ends its load step, then the top 3 cards are removed from the deck regardless of lot size."},
    {"id": "R13", "text": "When round mod 2N = 0 and top > 0, then every player with ship_value = top gains 20 florins."},
    {"id": "R14", "text": "When round mod 2N = 0 and second > 0, then every player with ship_value = second (the highest value strictly below top) gains 10 florins."},
    {"id": "R15", "text": "When round mod 2N = 0, then for each of grain, cloth, spice and dye, if the highest count is > 0, every player with that highest count gains 6 florins."},
    {"id": "R16", "text": "When round = 6N, then each player gains 3 florins per card of their favoured_good, and all favoured goods are revealed."},
    {"id": "R17", "text": "When round = 6N, then the game ends and the player with the most florins wins, with players tied for the most sharing the result (a draw)."}
  ],
  "offers": [
    {"question": "Lot size", "who": "the player at active_seat only", "options": "1, 2 or 3"},
    {"question": "Sealed bid", "who": "all players", "options": "Any whole number from 0 to the player's current florins. A player whose ship_count + lot_size > 5 is offered the same range but is told that only a bid of 0 counts."}
  ],
  "choices": [
    {"what": "3 to 6 players, suggested 4", "why": "The designer's suggested size of 4 is kept. The minimum is 3 because the second-place ship payout and sealed-bid ties need at least two rivals. The maximum is 6 because the 48-card deck supplies the 6N = 36 cards cleared per day at N=6, and a larger table would leave each player too few auctions to matter."},
    {"what": "No talk phase", "why": "The rules state there is no talk phase."},
    {"what": "Cards are coded as good:value text in the deck list", "why": "This lets the engine sum lot values and count goods per lot card arithmetically."},
    {"what": "Ship values, ship counts and goods counts are public", "why": "Every lot's cards, value and winning bid are announced, so all players can already work these out."},
    {"what": "Card value distribution given as counts per value in parameters", "why": "Parameters must be single numbers, so the per-good list 0,1,1,2,2,3,3,3,4,4,5,5 is written as how many cards of each value each good has."},
    {"what": "Strategy check", "why": "Players must value lots against their ship capacity, contest the ship ranks and goods tracks, hide their favoured good while chasing it, and avoid tied high bids that void a lot."}
  ],
  "simplifications": [
    {"what": "Shuffling the deck is done by drawing all 48 cards at random into an ordered list", "why": "The engine's randomness is random draws, and the result is an equivalent shuffle."},
    {"what": "A tie for the most florins is a shared win rather than a declared draw", "why": "The engine has no separate draw; players level at the top share the win."}
  ],
  "unsupported": []
}
```
````
