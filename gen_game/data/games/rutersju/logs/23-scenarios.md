# 23 scenarios

- time: 2026-10-28T03:49:48+00:00 (75.1s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 629747576266d91c, reply sha256 ebb4ca2122df7a81

## Sent

````
SPEC:
{
  "name": "Rutersju Hook",
  "summary": "A trick-taking game played with a 36-card pack. In each deal players bid 0-3 tricks in turn, and the last bidder may not make the bids total exactly 3. Players then play 3 tricks with simultaneous card choices and score for hitting their bid exactly.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
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
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running point total. It may go negative.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held this deal, each written 'strength:card', for example '36:\u26667'.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This deal's bid, from 0 to 3.",
        "observable": true
      },
      {
        "key": "tricks",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won this deal.",
        "observable": true
      },
      {
        "key": "played",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card played in the current trick. It is revealed only after all cards are chosen.",
        "observable": false
      },
      {
        "key": "is_declarer",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether this player is the declarer of the current deal.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 36 cards: 36:\u26667, 35:\u2666A, 34:\u2666K, 33:\u2666Q, 32:\u2666J, 31:\u266610, 30:\u26669, 29:\u26668, 28:\u26666, 27:\u2660A, 26:\u2665A, 25:\u2663A, 24:\u2660K, 23:\u2665K, 22:\u2663K, 21:\u2660Q, 20:\u2665Q, 19:\u2663Q, 18:\u2660J, 17:\u2665J, 16:\u2663J, 15:\u266010, 14:\u266510, 13:\u266310, 12:\u26609, 11:\u26659, 10:\u26639, 9:\u26608, 8:\u26658, 7:\u26638, 6:\u26607, 5:\u26657, 4:\u26637, 3:\u26606, 2:\u26656, 1:\u26636",
        "meaning": "The undealt cards. They stay hidden all deal.",
        "observable": false
      },
      {
        "key": "played_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played face up so far this deal.",
        "observable": false
      },
      {
        "key": "deal_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of deals completed.",
        "observable": true
      },
      {
        "key": "total_deals",
        "type": "number",
        "visible": "public",
        "initial": "3 * N",
        "meaning": "Length of the game: 3 deals per player.",
        "observable": false
      },
      {
        "key": "priority_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that bids last in this deal.",
        "observable": true
      },
      {
        "key": "bid_sum",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the bids made so far this deal.",
        "observable": false
      },
      {
        "key": "declarer_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the declarer; 0 means no declarer.",
        "observable": true
      },
      {
        "key": "trick_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks completed in this deal.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are numbered 1 to N, where N is 3, 4 or 5.",
    "Every player's score is set to 0.",
    "total_deals is set to 3 * N, priority_seat to 1 and deal_number to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Start a deal. Refill deck with all 36 cards. Clear every hand and played_cards. Set every bid, tricks and played to 0 or empty, every is_declarer to false, and bid_sum, declarer_seat and trick_number to 0. Deal 3 cards to each player: each card is a random draw removed from deck and appended to that player's hand."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees only their own hand."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting with seat (priority_seat mod N) + 1, going up the seat numbers with wraparound, and ending with priority_seat",
      "answer": "A whole number from 0 to 3. For priority_seat, if bid_sum <= 3, the value 3 - bid_sum is not offered.",
      "effect": "The player's bid is set to the answer and bid_sum is increased by the answer. Each bidder hears all earlier bids."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If max bid is 0, set declarer_seat to 0. Otherwise declarer_seat is the seat with the highest bid; among tied players it is the one who bid latest in this deal's bidding order. Set is_declarer to true for that seat."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every bid and the declarer (or 'no declarer')."
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "Repeat the next three steps until trick_number = 3."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "One card from the player's own hand.",
      "effect": "Each player's played is set to the chosen card. No player sees any choice until all choices are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Remove each played card from its hand and append it to played_cards. The player whose played card has the highest strength (the number before the colon) adds 1 to tricks. Increase trick_number by 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal all played cards together and announce the trick winner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Settle the deal. For each player, let d = |bid - tricks|. If d = 0, score += 3 + bid; otherwise score -= 2 * d. In addition, if is_declarer is true: if d = 0, score += 1; otherwise score -= 1. Then deal_number += 1 and priority_seat = (priority_seat mod N) + 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce all bids, trick counts and scores, and the new priority_seat."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if deal_number >= total_deals; otherwise start the next deal."
    }
  ],
  "ending": {
    "condition": "deal_number >= total_deals",
    "rank_by": "you.score",
    "decided_by": "After 3N deals, the player with the highest score wins. If several players tie for the highest score, they share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, every player has 0 points, priority_seat is 1, and total_deals is 3 * N (9 for 3 players, 12 for 4, 15 for 5)."
    },
    {
      "id": "R2",
      "text": "When a deal starts, the full 36-card pack is reshuffled and each player is dealt exactly 3 cards into their hand, removed from deck. With N players, 36 - 3N cards stay hidden in deck."
    },
    {
      "id": "R3",
      "text": "When a hand is dealt, only its owner can see it, and deck is visible to no one."
    },
    {
      "id": "R4",
      "text": "When bidding happens, seats bid in order starting at the seat after priority_seat (wrapping from N to 1), each hearing all earlier bids, and priority_seat bids last."
    },
    {
      "id": "R5",
      "text": "When any player bids, the bid is a whole number from 0 to 3."
    },
    {
      "id": "R6",
      "text": "When the priority seat bids and the others' bids sum to s <= 3, the bid 3 - s is not allowed. For example, if the others sum to 1, the priority seat may bid 0, 1 or 3 but not 2."
    },
    {
      "id": "R7",
      "text": "When the others' bids sum to more than 3, the priority seat may bid any of 0, 1, 2 or 3."
    },
    {
      "id": "R8",
      "text": "When bidding ends, the player with the highest bid is the declarer. If players tie for the highest bid, the tied player who bid latest is the declarer."
    },
    {
      "id": "R9",
      "text": "When every bid is 0, there is no declarer (declarer_seat = 0)."
    },
    {
      "id": "R10",
      "text": "When a trick is played, every player simultaneously chooses one card from their hand, and no choice is seen until all are in."
    },
    {
      "id": "R11",
      "text": "When the cards of a trick are revealed, the card with the highest strength wins, with no need to follow suit, and its player's tricks increases by 1. For example, \u26667 (36) beats \u2666A (35), and \u26666 (28) beats \u2660A (27)."
    },
    {
      "id": "R12",
      "text": "When a card is played, it leaves the hand and is added to the public played_cards list."
    },
    {
      "id": "R13",
      "text": "When a deal has had 3 tricks, it moves to settlement."
    },
    {
      "id": "R14",
      "text": "When a player's tricks equals their bid, they gain 3 + bid points: 3 for bid 0, 4 for bid 1, 5 for bid 2, 6 for bid 3."
    },
    {
      "id": "R15",
      "text": "When a player's tricks differ from their bid by d > 0, they lose 2 * d points. For example, bid 3 with 1 trick loses 4."
    },
    {
      "id": "R16",
      "text": "When the declarer hits their bid exactly, they gain 1 extra point. When the declarer misses, they lose 1 extra point."
    },
    {
      "id": "R17",
      "text": "When settlement ends, scores may be negative, deal_number increases by 1, and priority_seat moves to (priority_seat mod N) + 1."
    },
    {
      "id": "R18",
      "text": "When deal_number reaches 3 * N, the game ends and the player with the highest score wins. A tie at the top is a draw, shared among the tied players."
    }
  ],
  "offers": [
    {
      "question": "Bid",
      "who": "every seat except priority_seat",
      "options": "0, 1, 2, 3"
    },
    {
      "question": "Bid",
      "who": "priority_seat",
      "options": "If the sum s of the earlier bids is <= 3: 0, 1, 2, 3 except 3 - s. If s > 3: 0, 1, 2, 3."
    },
    {
      "question": "Card for the trick",
      "who": "all players",
      "options": "Exactly the cards currently in that player's own hand (3 in trick 1, 2 in trick 2, 1 in trick 3)."
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer suggests 4, so it is kept. 3 is the smallest table where the hook and declarer contests bite. Above 5, 3 tricks spread over too many players, so most bids are 0 and one choice matters little."
    },
    {
      "what": "'Left' means the next higher seat number, wrapping from N to 1",
      "why": "The engine has no physical table, and seat order must be concrete."
    },
    {
      "what": "Cards are written as 'strength:card', for example '36:\u26667'",
      "why": "The engine has no lookup table, so putting the strength in the card text lets the trick winner be found by comparing numbers."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid discussion; players communicate only through bids and cards."
    },
    {
      "what": "Bidding uses ask; card play uses poll",
      "why": "Bids are made in turn and each bidder hears earlier bids, while cards are chosen secretly and simultaneously."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is shown as a shared win among the tied players",
      "why": "The engine ranks by one expression and players level at the top share the win. This is equivalent to the source's draw."
    },
    {
      "what": "Scratch value d = |bid - tricks| is computed inside the settlement step rather than stored",
      "why": "The rules never refer to it outside settlement."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid, tricks; table: deal_number, priority_seat, declarer_seat.
````

## Reply

````
[
  {"name": "Game starts with 0 points, priority seat 1 and no deals completed", "rule": "R1", "players": 3, "seed": 1, "default": "decline", "rounds": 0,
   "rules": [],
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}},
              "game": {"priority_seat": 1, "deal_number": 0}}},
  {"name": "With 5 players the game lasts 15 deals: a game at 14 deals ends after one more deal (leader too far ahead for chance to matter)", "rule": "R1", "players": 5, "seed": 2, "default": "decline",
   "given": {"players": {"2": {"score": 100}}, "game": {"deal_number": 14}},
   "rules": [],
   "expect": {"winner": 2, "game": {"deal_number": 15}}},
  {"name": "3 players: each is dealt 3 cards, 27 cards stay in deck all deal", "rule": "R2", "players": 3, "seed": 3, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 27}}}},
  {"name": "4 players: 24 cards stay in deck", "rule": "R2", "players": 4, "seed": 4, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 24}}}},
  {"name": "5 players: hidden deck keeps 21 cards through the deal", "rule": "R3", "players": 5, "seed": 5, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 21}}}},
  {"name": "Priority seat 2 bids last after seats 3 and 1 (wraparound), and is refused the hook bid", "rule": "R4", "players": 3, "seed": 6, "default": "decline", "rounds": 1,
   "given": {"game": {"priority_seat": 2}},
   "rules": [{"seat": 3, "options_include": 1}, {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 1}},
              "game": {"declarer_seat": 1, "priority_seat": 3, "deal_number": 1},
              "not_offered": [{"seat": 2, "option": 1}]}},
  {"name": "A bid is a whole number from 0 to 3", "rule": "R5", "players": 3, "seed": 7, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 0}, {"seat": 1, "options_include": 1}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 3}, "3": {"bid": 0}},
              "game": {"declarer_seat": 2},
              "offered": [{"seat": 2, "option": 0}, {"seat": 2, "option": 3}],
              "not_offered": [{"seat": 2, "option": 4}, {"seat": 3, "option": 4}]}},
  {"name": "Others sum to 1: priority seat may bid 0, 1 or 3 but not 2", "rule": "R6", "players": 3, "seed": 8, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}, {"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 1}, "3": {"bid": 0}},
              "game": {"declarer_seat": 1},
              "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 1}, {"seat": 1, "option": 3}],
              "not_offered": [{"seat": 1, "option": 2}]}},
  {"name": "Others sum to 3: priority seat may not bid 0", "rule": "R6", "players": 3, "seed": 9, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 1}, {"seat": 1, "options_include": 1}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 1}},
              "game": {"declarer_seat": 2},
              "not_offered": [{"seat": 1, "option": 0}]}},
  {"name": "Others sum to 4: priority seat may bid any of 0 to 3", "rule": "R7", "players": 3, "seed": 10, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 1}, {"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 3}, "3": {"bid": 1}},
              "game": {"declarer_seat": 2},
              "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 1}, {"seat": 1, "option": 2}, {"seat": 1, "option": 3}]}},
  {"name": "Tie for highest bid: the latest bidder of the tied players is declarer", "rule": "R8", "players": 3, "seed": 11, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 2}, {"seat": 3, "options_include": 2}, {"seat": 1, "options_include": 0}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 2}, "3": {"bid": 2}},
              "game": {"declarer_seat": 3}}},
  {"name": "Unique highest bid makes that player declarer", "rule": "R8", "players": 4, "seed": 12, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 2}, {"seat": 4, "options_include": 1}, {"seat": 1, "options_include": 1}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 2}, "4": {"bid": 1}},
              "game": {"declarer_seat": 3}}},
  {"name": "All bids 0 means no declarer", "rule": "R9", "players": 4, "seed": 13, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 0}, {"seat": 1, "options_include": 0}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 0}, "3": {"bid": 0}, "4": {"bid": 0}},
              "game": {"declarer_seat": 0},
              "not_offered": [{"seat": 1, "option": 3}]}},
  {"name": "Every player plays one card per trick: all hands empty after 3 tricks (cards random)", "rule": "R10", "players": 3, "seed": 14, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}, "game": {"played_cards": 9}},
              "game": {"deal_number": 1}}},
  {"name": "Three tricks are played and revealed (winners depend on the random deal)", "rule": "R11", "players": 4, "seed": 15, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"played_cards": 12}}, "game": {"deal_number": 1}}},
  {"name": "Played cards leave hands and go to the public played_cards list", "rule": "R12", "players": 3, "seed": 16, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}, "game": {"played_cards": 9, "deck": 27}}}},
  {"name": "After 3 tricks the deal is settled: deal count and priority advance", "rule": "R13", "players": 3, "seed": 17, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"players": {"1": {"hand": 0}}}, "game": {"deal_number": 1, "priority_seat": 2}}},
  {"name": "Exact-bid scoring deal: tricks depend on chance, so only bids, declarer and deal count are asserted", "rule": "R14", "players": 4, "seed": 18, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 1}, {"seat": 3, "options_include": 0}, {"seat": 4, "options_include": 1}, {"seat": 1, "options_include": 0}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 1}, "3": {"bid": 0}, "4": {"bid": 1}},
              "game": {"declarer_seat": 4, "deal_number": 1, "priority_seat": 2},
              "not_offered": [{"seat": 1, "option": 1}]}},
  {"name": "Miss scoring deal: everyone bids 3 (at most one can hit); chance decides tricks, only bids and declarer asserted", "rule": "R15", "players": 3, "seed": 19, "default": "decline", "rounds": 1,
   "rules": [{"seat": 2, "options_include": 3}, {"seat": 3, "options_include": 3}, {"seat": 1, "options_include": 3}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 3}, "3": {"bid": 3}},
              "game": {"declarer_seat": 1, "deal_number": 1}}},
  {"name": "Declarer bonus deal: declarer set by highest bid; chance decides tricks, only bids and declarer asserted", "rule": "R16", "players": 3, "seed": 20, "default": "decline", "rounds": 1,
   "given": {"game": {"priority_seat": 2}},
   "rules": [{"seat": 3, "options_include": 1}, {"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 1}],
   "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 1}, "3": {"bid": 1}},
              "game": {"declarer_seat": 1, "priority_seat": 3},
              "not_offered": [{"seat": 2, "option": 0}]}},
  {"name": "After settlement deal_number rises by 1 and priority wraps from seat 3 to seat 1", "rule": "R17", "players": 3, "seed": 21, "default": "decline", "rounds": 1,
   "given": {"game": {"priority_seat": 3, "deal_number": 4}},
   "rules": [],
   "expect": {"game": {"deal_number": 5, "priority_seat": 1}}},
  {"name": "Game ends after 9 deals with 3 players; far-ahead seat 1 wins whatever the last deal brings", "rule": "R18", "players": 3, "seed": 22, "default": "decline",
   "given": {"players": {"1": {"score": 100}}, "game": {"deal_number": 8}},
   "rules": [],
   "expect": {"winner": 1, "game": {"deal_number": 9}}},
  {"name": "Game ends after 12 deals with 4 players; far-ahead seat 3 wins", "rule": "R18", "players": 4, "seed": 23, "default": "decline",
   "given": {"players": {"3": {"score": 50}}, "game": {"deal_number": 11}},
   "rules": [],
   "expect": {"winner": 3, "game": {"deal_number": 12}}}
]
````
