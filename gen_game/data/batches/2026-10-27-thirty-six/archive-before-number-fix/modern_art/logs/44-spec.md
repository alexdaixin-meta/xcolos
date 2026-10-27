# 44 spec

- time: 2026-10-27T17:39:01+00:00 (57.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 6dd595fa1e63c0cf, reply sha256 34031c327316cc59

## Sent

````
Game: Modern Art: Sealed Gallery
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
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

How the winner is decided: After round 18, including the final season's scoring and payout, the player with the strictly highest money wins. If two or three players tie for the highest money, the game is a draw.
````

## Reply

````
```json
{
  "name": "Modern Art: Sealed Gallery",
  "summary": "Three players take turns as auctioneer of 18 paintings by three artists. Everyone bids at once in sealed bids, artists gain value at each season's end, owned paintings pay out, and the richest player after round 18 wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
  "parameters": {
    "start_money": 60,
    "artist_count": 3,
    "die_sides": 6,
    "composition_major": 4,
    "composition_middle": 2,
    "composition_minor": 1,
    "cards_per_hand": 7,
    "auctions_per_seat": 6,
    "season_end_count": 3,
    "first_place_value": 6,
    "second_place_value": 3,
    "tie_value": 3,
    "min_season_count_to_score": 1,
    "total_rounds": 18,
    "first_auctioneer": 1,
    "min_bid": 0
  },
  "attributes": {
    "player": [
      {"key": "money", "type": "number", "visible": "public", "initial": 60, "meaning": "Coins held. Every bid, price and payout is announced.", "observable": true},
      {"key": "hand_red", "type": "number", "visible": "ally", "initial": 0, "meaning": "Red cards in this player's private hand.", "observable": false},
      {"key": "hand_blue", "type": "number", "visible": "ally", "initial": 0, "meaning": "Blue cards in this player's private hand.", "observable": false},
      {"key": "hand_green", "type": "number", "visible": "ally", "initial": 0, "meaning": "Green cards in this player's private hand.", "observable": false},
      {"key": "owned_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Red paintings bought this season.", "observable": false},
      {"key": "owned_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Blue paintings bought this season.", "observable": false},
      {"key": "owned_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Green paintings bought this season.", "observable": false},
      {"key": "message", "type": "text", "visible": "public", "initial": "", "meaning": "This round's talk message.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This round's sealed bid, revealed once all bids are in.", "observable": true},
      {"key": "last_payout", "type": "number", "visible": "public", "initial": 0, "meaning": "Money received at the most recent season scoring.", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Round counter, from 1 to 18.", "observable": true},
      {"key": "auctioneer", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the current auctioneer.", "observable": true},
      {"key": "season_over", "type": "number", "visible": "public", "initial": 0, "meaning": "Set to 1 when the season ends this round.", "observable": false},
      {"key": "deal_roll", "type": "number", "visible": "none", "initial": 0, "meaning": "Hidden die roll (1 to 6) that decides which seat gets which composition.", "observable": false},
      {"key": "season_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Red cards played this season.", "observable": true},
      {"key": "season_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Blue cards played this season.", "observable": true},
      {"key": "season_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Green cards played this season.", "observable": true},
      {"key": "value_red", "type": "number", "visible": "public", "initial": 0, "meaning": "Cumulative value of Red.", "observable": true},
      {"key": "value_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "Cumulative value of Blue.", "observable": true},
      {"key": "value_green", "type": "number", "visible": "public", "initial": 0, "meaning": "Cumulative value of Green.", "observable": true},
      {"key": "current_artist", "type": "text", "visible": "public", "initial": "", "meaning": "Artist played this round (red, blue or green).", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Highest bid this round.", "observable": false},
      {"key": "winner", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat that won this round's painting.", "observable": false},
      {"key": "price", "type": "number", "visible": "public", "initial": 0, "meaning": "Price paid this round.", "observable": false},
      {"key": "scored_red", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if Red scored at this season's end, else 0.", "observable": false},
      {"key": "scored_blue", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if Blue scored at this season's end, else 0.", "observable": false},
      {"key": "scored_green", "type": "number", "visible": "public", "initial": 0, "meaning": "1 if Green scored at this season's end, else 0.", "observable": false}
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each get money 60, and owned_red, owned_blue and owned_green 0.",
    "season_red, season_blue and season_green are set to 0, and value_red, value_blue and value_green to 0.",
    "auctioneer is set to 1, round to 0 and season_over to 0.",
    "deal_roll is set to a random whole number from 1 to 6 (seeded).",
    "Composition A is Red 4, Blue 2, Green 1. Composition B is Red 1, Blue 4, Green 2. Composition C is Red 2, Blue 1, Green 4.",
    "The compositions go to seats 1, 2 and 3 by roll: roll 1 gives A,B,C; roll 2 gives A,C,B; roll 3 gives B,A,C; roll 4 gives B,C,A; roll 5 gives C,A,B; roll 6 gives C,B,A. This sets each seat's hand_red, hand_blue and hand_green.",
    "Each player is shown only their own hand and is told that the other two seats hold the other two compositions."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; season_over = 0."},
    {"action": "ask", "who": "the seat equal to auctioneer", "answer": "one artist from red, blue, green, offering only those whose hand count for this seat is above 0", "effect": "The chosen artist is X."},
    {"action": "update", "who": "the seat equal to auctioneer", "answer": null, "effect": "That seat's hand_X -= 1; season_X += 1; current_artist = X. Announce current_artist to all."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If season_X == 3, then season_over = 1 and announce that the card is discarded unsold and the season ends. Otherwise season_over stays 0."},
    {"action": "poll", "who": "all players, when season_over == 0", "answer": "short free text", "effect": "Set each player's message, then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."},
    {"action": "poll", "who": "all players, when season_over == 0", "answer": "a whole number from 0 to your own money", "effect": "Set each player's bid. Once all bids are in, announce all three bids."},
    {"action": "update", "who": "all players, when season_over == 0", "answer": null, "effect": "high_bid = max of the bids. If high_bid == 0: winner = auctioneer and price = 0. Otherwise price = high_bid and winner = the first seat with bid == high_bid in this order: auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer."},
    {"action": "update", "who": "all players, when season_over == 0", "answer": null, "effect": "If winner != auctioneer: the winner's money -= price and the auctioneer's money += price. If winner == auctioneer: the auctioneer's money -= price (paid to the bank). The winner's owned_X += 1. Announce winner and price."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If round == 18, then season_over = 1."},
    {"action": "update", "who": "all players, when season_over == 1", "answer": null, "effect": "Set scored_red, scored_blue and scored_green to 0. Let top = the largest season count. If top >= 1 and exactly one artist has season == top, that artist gets value += 6 and scored = 1; then let s = the larger season count of the other two, and if s >= 1 and exactly one of them has season == s, that artist gets value += 3 and scored = 1. If top >= 1 and two or three artists have season == top, each of them gets value += 3 and scored = 1, and no other artist scores."},
    {"action": "update", "who": "all players, when season_over == 1", "answer": null, "effect": "For each player: last_payout = owned_red*value_red*scored_red + owned_blue*value_blue*scored_blue + owned_green*value_green*scored_green; money += last_payout."},
    {"action": "update", "who": "all players, when season_over == 1", "answer": null, "effect": "Every player's owned_red, owned_blue and owned_green = 0; season_red, season_blue and season_green = 0. Values are kept."},
    {"action": "tell", "who": "all players, when season_over == 1", "answer": null, "effect": "Announce the scoring artists, value_red, value_blue, value_green, and each player's last_payout and money."},
    {"action": "update", "who": "all players", "answer": null, "effect": "auctioneer = auctioneer % 3 + 1."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round == 18, end the game. Otherwise start the next round."}
  ],
  "ending": {
    "condition": "round == 18",
    "rank_by": "you.money",
    "decided_by": "After round 18, including the last season's scoring and payout, the player with the most money wins. Players tied for the most money share the result, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then every player has money 60 and owned_red, owned_blue and owned_green 0; every season count and every value is 0; auctioneer is 1; round is 0."},
    {"id": "R2", "text": "When deal_roll is 1, then seats 1, 2 and 3 get compositions A, B and C, where A is Red 4/Blue 2/Green 1, B is Red 1/Blue 4/Green 2, and C is Red 2/Blue 1/Green 4."},
    {"id": "R3", "text": "When deal_roll is 2, 3, 4, 5 or 6, then seats 1, 2 and 3 get A,C,B or B,A,C or B,C,A or C,A,B or C,B,A respectively."},
    {"id": "R4", "text": "When hands are dealt, then each player sees only their own hand_red, hand_blue and hand_green."},
    {"id": "R5", "text": "When a round starts, then round rises by 1 and season_over is set to 0."},
    {"id": "R6", "text": "When the auctioneer chooses an artist, then only artists with the auctioneer's hand count above 0 are offered."},
    {"id": "R7", "text": "When artist X is played, then the auctioneer's hand_X falls by 1, season_X rises by 1, and current_artist is announced as X."},
    {"id": "R8", "text": "When season_X reaches 3 after a play, then season_over is 1, the card is discarded unsold, and no talk, bid or sale happens that round."},
    {"id": "R9", "text": "When season_over is 0, then all three players write one message at the same time, and all are shown labelled by seat."},
    {"id": "R10", "text": "When season_over is 0, then all three players, including the auctioneer, bid simultaneously a whole number from 0 to their own money, and all bids are announced."},
    {"id": "R11", "text": "When the highest bid is positive, then the highest bidder wins at a price equal to that bid."},
    {"id": "R12", "text": "When all bids are 0, then the auctioneer takes the painting at price 0."},
    {"id": "R13", "text": "When a positive top bid is tied, then the winner is the tied seat that comes first in the order: seat after the auctioneer, the next seat, then the auctioneer (for example, with auctioneer 1 the order is 2, 3, 1)."},
    {"id": "R14", "text": "When the winner is not the auctioneer, then the winner pays the price to the auctioneer; for example, a price of 10 moves 10 from the winner's money to the auctioneer's."},
    {"id": "R15", "text": "When the winner is the auctioneer, then the auctioneer's money falls by the price, paid to the bank."},
    {"id": "R16", "text": "When a painting of X is sold, then the winner's owned_X rises by 1 and the winner and price are announced."},
    {"id": "R17", "text": "When round is 18, then season_over is set to 1 after the sale."},
    {"id": "R18", "text": "When a season ends and one artist has the strictly highest season count (at least 1), then its value rises by 6."},
    {"id": "R19", "text": "When a single artist was top, and one of the other two has a season count strictly higher than the third and at least 1, then that artist's value rises by 3; otherwise no second artist scores."},
    {"id": "R20", "text": "When two or three artists tie for the highest season count (at least 1), then each of them gains 3 value and no other artist scores."},
    {"id": "R21", "text": "When a season ends, then for each artist that scored, every player's money rises by their owned count of it times its new cumulative value; artists that did not score pay nothing but keep their value."},
    {"id": "R22", "text": "When a season's payout is done, then every owned count and every season count is reset to 0, and values are kept."},
    {"id": "R23", "text": "When a season ends, then the scoring artists, new values, each player's payout and each player's money are announced."},
    {"id": "R24", "text": "When a round ends, then the auctioneer passes 1 to 2, 2 to 3, and 3 to 1."},
    {"id": "R25", "text": "When round 18 has ended, then the game ends and the player with the most money wins; players tied for the most money share the result (a draw)."}
  ],
  "offers": [
    {"question": "Which artist do you play?", "who": "the auctioneer only", "options": "each of red, blue and green for which the auctioneer's own hand count is above 0; other seats are not asked"},
    {"question": "Your message to the table", "who": "all three seats, only when season_over == 0", "options": "short free text"},
    {"question": "Your sealed bid", "who": "all three seats including the auctioneer, only when season_over == 0", "options": "a whole number from 0 to that seat's current money"}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed 3. The deal uses three compositions, one per seat, and 18 rounds give each seat exactly 6 auctions. With fewer seats there are no rivals to hide compositions from, and more seats would break the deal."},
    {"what": "Talk kept as a simultaneous poll broadcast to all", "why": "The rules say the messages are written at the same time without seeing the others. Players disagree about which artist to boost, so talk gives them something to bluff and bargain over."},
    {"what": "Tie order written as auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer", "why": "This is the source's seat order expressed as arithmetic."},
    {"what": "Owned counts and season counts are public", "why": "Every played artist, winner and price is announced, so these are already known to all."},
    {"what": "Season scoring is done by arithmetic, with no referee", "why": "The comparisons of the three season counts are all arithmetic."},
    {"what": "The round-18 auction still runs before the forced season end", "why": "The source's R11 sets season_over only after the sale steps."}
  ],
  "simplifications": [
    {"what": "A tie for the most money is reported as a shared win", "why": "The engine has no separate draw; players level at the top share the win, which is the source's draw."},
    {"what": "The die roll is a seeded random number from 1 to 6", "why": "The engine's randomness is seeded so a match replays exactly."}
  ],
  "unsupported": []
}
```
````
