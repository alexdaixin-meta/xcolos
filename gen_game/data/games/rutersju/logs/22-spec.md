# 22 spec

- time: 2026-10-28T03:49:02+00:00 (46.4s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 4cafbf803bf53459, reply sha256 41caf8a272e3030f

## Sent

````
Game: Rutersju Hook
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP. Use a 36-card French pack (6, 7, 8, 9, 10, J, Q, K, A in ♣ ♥ ♠ ♦). Seats are numbered 1 to N (N = 3, 4 or 5). Every player starts with 0 points. The game lasts 3 deals per player: 9 deals with 3 players, 12 with 4, 15 with 5. The priority seat is seat 1 in deal 1 and moves one seat to the left after each deal.

CARD STRENGTH. Every card has a unique strength from 1 to 36. The higher strength always wins.
- ♦7 = 36.
- The other diamonds: ♦A=35, ♦K=34, ♦Q=33, ♦J=32, ♦10=31, ♦9=30, ♦8=29, ♦6=28.
- The plain suits: ♠A=27, ♥A=26, ♣A=25, ♠K=24, ♥K=23, ♣K=22, ♠Q=21, ♥Q=20, ♣Q=19, ♠J=18, ♥J=17, ♣J=16, ♠10=15, ♥10=14, ♣10=13, ♠9=12, ♥9=11, ♣9=10, ♠8=9, ♥8=8, ♣8=7, ♠7=6, ♥7=5, ♣7=4, ♠6=3, ♥6=2, ♣6=1.

EACH DEAL.
1. Deal. Shuffle the full pack and deal 3 cards face down to each player. Each hand is seen only by its owner. Undealt cards stay hidden for the whole deal.
2. Bid (in turn). Starting with the player to the LEFT of the priority seat and going left, each player in turn announces a bid of 0, 1, 2 or 3, hearing all earlier bids. The priority seat bids last.
3. The hook. The last bidder (the priority seat) may not choose a bid that makes the sum of all bids exactly 3. The sum of the others' bids can only exceed 3 in this case if… it never matters: when the others' sum is already above 3, every bid is allowed.
4. Declarer. The player with the highest bid is the declarer. If several players tie for the highest bid, the one among them who bid LAST is the declarer. If every bid is 0, there is no declarer (the hook allows this only when the bids can total 0, which is permitted because 0 ≠ 3). Announce all bids and the declarer.
5. Tricks. Play 3 tricks. In each trick, every player secretly and simultaneously chooses one card from their hand. All chosen cards are revealed together. The card with the highest strength wins the trick, and its player adds 1 to their trick count. There is no need to follow suit. Played cards stay face up and public.
6. Settlement, for each player separately, where d = |bid − tricks won|:
   a. If d = 0, the player gains 3 + bid points (bid 0 → 3, bid 1 → 4, bid 2 → 5, bid 3 → 6).
   b. If d > 0, the player loses 2 × d points.
   c. The declarer, if there is one, additionally gains 1 point if their d = 0, or loses 1 point if their d > 0.
   Because exactly 3 tricks are won and the bids never total 3, at least one player misses every deal.
7. Announce all bids, trick counts and point totals. Move the priority seat one place to the left.

There is no discussion phase. Players communicate only through their bids, which are public and made in turn, and through the cards they play. Scores may go negative.

END. After the last deal, the single player with the highest point total wins. If two or more players tie for the highest total, the game is a draw.

How the winner is decided: After 3N deals, the single player with the highest total points wins. A tie for the highest total is a draw.
````

## Reply

````
```json
{
  "name": "Rutersju Hook",
  "summary": "A trick-taking game played with a 36-card pack. In each deal players bid 0-3 tricks in turn, and the last bidder may not make the bids total exactly 3. Players then play 3 tricks with simultaneous card choices and score for hitting their bid exactly.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "deck_size": 36,
    "hand_size": 3,
    "tricks_per_deal": 3,
    "deals_per_player": 3,
    "min_bid": 0,
    "max_bid": 3,
    "forbidden_bid_total": 3,
    "exact_base_points": 3,
    "miss_penalty_per_trick": 2,
    "declarer_bonus": 1,
    "declarer_penalty": 1,
    "starting_score": 0,
    "highest_strength": 36,
    "lowest_strength": 1
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Running point total. It may go negative.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "Cards held this deal, each written 'strength:card', for example '36:♦7'.", "observable": false},
      {"key": "bid", "type": "number", "visible": "public", "initial": 0, "meaning": "This deal's bid, from 0 to 3.", "observable": true},
      {"key": "tricks", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks won this deal.", "observable": true},
      {"key": "played", "type": "text", "visible": "public", "initial": "", "meaning": "Card played in the current trick. It is revealed only after all cards are chosen.", "observable": false},
      {"key": "is_declarer", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this player is the declarer of the current deal.", "observable": false}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": "all 36 cards: 36:♦7, 35:♦A, 34:♦K, 33:♦Q, 32:♦J, 31:♦10, 30:♦9, 29:♦8, 28:♦6, 27:♠A, 26:♥A, 25:♣A, 24:♠K, 23:♥K, 22:♣K, 21:♠Q, 20:♥Q, 19:♣Q, 18:♠J, 17:♥J, 16:♣J, 15:♠10, 14:♥10, 13:♣10, 12:♠9, 11:♥9, 10:♣9, 9:♠8, 8:♥8, 7:♣8, 6:♠7, 5:♥7, 4:♣7, 3:♠6, 2:♥6, 1:♣6", "meaning": "The undealt cards. They stay hidden all deal.", "observable": false},
      {"key": "played_cards", "type": "list", "visible": "public", "initial": [], "meaning": "Cards played face up so far this deal.", "observable": false},
      {"key": "deal_number", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of deals completed.", "observable": true},
      {"key": "total_deals", "type": "number", "visible": "public", "initial": "3 * N", "meaning": "Length of the game: 3 deals per player.", "observable": false},
      {"key": "priority_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "The seat that bids last in this deal.", "observable": true},
      {"key": "bid_sum", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the bids made so far this deal.", "observable": false},
      {"key": "declarer_seat", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the declarer; 0 means no declarer.", "observable": true},
      {"key": "trick_number", "type": "number", "visible": "public", "initial": 0, "meaning": "Tricks completed in this deal.", "observable": false}
    ]
  },
  "setup": [
    "Seats are numbered 1 to N, where N is 3, 4 or 5.",
    "Every player's score is set to 0.",
    "total_deals is set to 3 * N, priority_seat to 1 and deal_number to 0."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Start a deal. Refill deck with all 36 cards. Clear every hand and played_cards. Set every bid, tricks and played to 0 or empty, every is_declarer to false, and bid_sum, declarer_seat and trick_number to 0. Deal 3 cards to each player: each card is a random draw removed from deck and appended to that player's hand."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player sees only their own hand."},
    {"action": "ask", "who": "each player in turn, starting with seat (priority_seat mod N) + 1, going up the seat numbers with wraparound, and ending with priority_seat", "answer": "A whole number from 0 to 3. For priority_seat, if bid_sum <= 3, the value 3 - bid_sum is not offered.", "effect": "The player's bid is set to the answer and bid_sum is increased by the answer. Each bidder hears all earlier bids."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If max bid is 0, set declarer_seat to 0. Otherwise declarer_seat is the seat with the highest bid; among tied players it is the one who bid latest in this deal's bidding order. Set is_declarer to true for that seat."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every bid and the declarer (or 'no declarer')."},
    {"action": "repeat", "who": "all players", "answer": null, "effect": "Repeat the next three steps until trick_number = 3."},
    {"action": "poll", "who": "all players", "answer": "One card from the player's own hand.", "effect": "Each player's played is set to the chosen card. No player sees any choice until all choices are in."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Remove each played card from its hand and append it to played_cards. The player whose played card has the highest strength (the number before the colon) adds 1 to tricks. Increase trick_number by 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal all played cards together and announce the trick winner."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Settle the deal. For each player, let d = |bid - tricks|. If d = 0, score += 3 + bid; otherwise score -= 2 * d. In addition, if is_declarer is true: if d = 0, score += 1; otherwise score -= 1. Then deal_number += 1 and priority_seat = (priority_seat mod N) + 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce all bids, trick counts and scores, and the new priority_seat."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if deal_number >= total_deals; otherwise start the next deal."}
  ],
  "ending": {
    "condition": "deal_number >= total_deals",
    "rank_by": "you.score",
    "decided_by": "After 3N deals, the player with the highest score wins. If several players tie for the highest score, they share the result, which is the source's draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, every player has 0 points, priority_seat is 1, and total_deals is 3 * N (9 for 3 players, 12 for 4, 15 for 5)."},
    {"id": "R2", "text": "When a deal starts, the full 36-card pack is reshuffled and each player is dealt exactly 3 cards into their hand, removed from deck. With N players, 36 - 3N cards stay hidden in deck."},
    {"id": "R3", "text": "When a hand is dealt, only its owner can see it, and deck is visible to no one."},
    {"id": "R4", "text": "When bidding happens, seats bid in order starting at the seat after priority_seat (wrapping from N to 1), each hearing all earlier bids, and priority_seat bids last."},
    {"id": "R5", "text": "When any player bids, the bid is a whole number from 0 to 3."},
    {"id": "R6", "text": "When the priority seat bids and the others' bids sum to s <= 3, the bid 3 - s is not allowed. For example, if the others sum to 1, the priority seat may bid 0, 1 or 3 but not 2."},
    {"id": "R7", "text": "When the others' bids sum to more than 3, the priority seat may bid any of 0, 1, 2 or 3."},
    {"id": "R8", "text": "When bidding ends, the player with the highest bid is the declarer. If players tie for the highest bid, the tied player who bid latest is the declarer."},
    {"id": "R9", "text": "When every bid is 0, there is no declarer (declarer_seat = 0)."},
    {"id": "R10", "text": "When a trick is played, every player simultaneously chooses one card from their hand, and no choice is seen until all are in."},
    {"id": "R11", "text": "When the cards of a trick are revealed, the card with the highest strength wins, with no need to follow suit, and its player's tricks increases by 1. For example, ♦7 (36) beats ♦A (35), and ♦6 (28) beats ♠A (27)."},
    {"id": "R12", "text": "When a card is played, it leaves the hand and is added to the public played_cards list."},
    {"id": "R13", "text": "When a deal has had 3 tricks, it moves to settlement."},
    {"id": "R14", "text": "When a player's tricks equals their bid, they gain 3 + bid points: 3 for bid 0, 4 for bid 1, 5 for bid 2, 6 for bid 3."},
    {"id": "R15", "text": "When a player's tricks differ from their bid by d > 0, they lose 2 * d points. For example, bid 3 with 1 trick loses 4."},
    {"id": "R16", "text": "When the declarer hits their bid exactly, they gain 1 extra point. When the declarer misses, they lose 1 extra point."},
    {"id": "R17", "text": "When settlement ends, scores may be negative, deal_number increases by 1, and priority_seat moves to (priority_seat mod N) + 1."},
    {"id": "R18", "text": "When deal_number reaches 3 * N, the game ends and the player with the highest score wins. A tie at the top is a draw, shared among the tied players."}
  ],
  "offers": [
    {"question": "Bid", "who": "every seat except priority_seat", "options": "0, 1, 2, 3"},
    {"question": "Bid", "who": "priority_seat", "options": "If the sum s of the earlier bids is <= 3: 0, 1, 2, 3 except 3 - s. If s > 3: 0, 1, 2, 3."},
    {"question": "Card for the trick", "who": "all players", "options": "Exactly the cards currently in that player's own hand (3 in trick 1, 2 in trick 2, 1 in trick 3)."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer suggests 4, so it is kept. 3 is the smallest table where the hook and declarer contests bite. Above 5, 3 tricks spread over too many players, so most bids are 0 and one choice matters little."},
    {"what": "'Left' means the next higher seat number, wrapping from N to 1", "why": "The engine has no physical table, and seat order must be concrete."},
    {"what": "Cards are written as 'strength:card', for example '36:♦7'", "why": "The engine has no lookup table, so putting the strength in the card text lets the trick winner be found by comparing numbers."},
    {"what": "No talk step", "why": "The rules forbid discussion; players communicate only through bids and cards."},
    {"what": "Bidding uses ask; card play uses poll", "why": "Bids are made in turn and each bidder hears earlier bids, while cards are chosen secretly and simultaneously."}
  ],
  "simplifications": [
    {"what": "A tie for the highest score is shown as a shared win among the tied players", "why": "The engine ranks by one expression and players level at the top share the win. This is equivalent to the source's draw."},
    {"what": "Scratch value d = |bid - tricks| is computed inside the settlement step rather than stored", "why": "The rules never refer to it outside settlement."}
  ],
  "unsupported": []
}
```
````
