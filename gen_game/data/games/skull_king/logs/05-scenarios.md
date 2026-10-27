# 05 scenarios

- time: 2026-10-27T20:46:32+00:00 (67.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 8638bc048cffc271, reply sha256 a5c74a212960a1b5

## Sent

````
SPEC:
{
  "name": "Skull King: Three-Card Raids",
  "summary": "Three players play 9 hands of 3 tricks each. Before each hand every player secretly bids how many tricks they will win, then scores for hitting the bid exactly and loses points for missing it, with bonuses for capturing Pirates or the Skull King.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "deck_size": 25,
    "green_cards": 7,
    "green_max_rank": 7,
    "yellow_cards": 7,
    "yellow_max_rank": 7,
    "black_cards": 5,
    "black_max_rank": 5,
    "pirates": 2,
    "escapes": 2,
    "mermaids": 1,
    "skull_kings": 1,
    "hands": 9,
    "tricks_per_hand": 3,
    "total_rounds": 27,
    "cards_dealt_per_player": 3,
    "cards_set_aside": 16,
    "bid_min": 0,
    "bid_max": 3,
    "exact_bid_points_per_trick": 20,
    "exact_zero_bid_points": 20,
    "missed_zero_bid_points": -20,
    "missed_bid_points_per_trick_difference": -10,
    "pirate_captured_by_skull_king_bonus": 30,
    "skull_king_captured_by_mermaid_bonus": 40,
    "trick_win_increment": 1,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total score across all hands.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player holds this hand; only the owner sees them.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks the player bid for the current hand (0-3). Chosen secretly, then revealed.",
        "observable": true
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won so far this hand.",
        "observable": true
      },
      {
        "key": "bonus",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Capture bonuses recorded this hand. Paid only if the bid is exact.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this player played in the current trick.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "G1",
          "G2",
          "G3",
          "G4",
          "G5",
          "G6",
          "G7",
          "Y1",
          "Y2",
          "Y3",
          "Y4",
          "Y5",
          "Y6",
          "Y7",
          "B1",
          "B2",
          "B3",
          "B4",
          "B5",
          "Pirate",
          "Pirate",
          "Escape",
          "Escape",
          "Mermaid",
          "SkullKing"
        ],
        "meaning": "The 25-card deck. After dealing, the 16 undealt cards stay here, set aside unseen.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current trick number in the game (1-27).",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand (1-9).",
        "observable": false
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Which trick of the hand is being played (1-3).",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "lead_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit of the first suited card in the trick (Green, Yellow or Black). Empty if no suited card has been played yet.",
        "observable": false
      },
      {
        "key": "trick_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played to the current trick, in play order, each tagged with the seat that played it.",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the most recent trick.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 are seated clockwise (1 to 2, 2 to 3, 3 to 1).",
    "Every player's score is set to 0.",
    "The deck list holds all 25 cards: G1-G7, Y1-Y7, B1-B5, 2 Pirate, 2 Escape, 1 Mermaid, 1 SkullKing.",
    "round = 1, hand_number = 1, trick_in_hand = 1, leader = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: return every card in each player's hand and in trick_cards to deck. Then, for each player, draw 3 cards at random from deck into their hand (remove from deck, append to hand); the 16 cards left in deck are set aside unseen. Set each player's bid = 0, tricks_won = 0, bonus = 0. Set leader = ((hand_number - 1) mod 3) + 1."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each player is sent their own hand. Nobody sees another player's hand."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 3",
      "effect": "When trick_in_hand == 1: each player's bid is set to their answer. No bid is shown until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: announce every seat's bid for hand {hand_number} and the first leader, seat {leader}."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set trick_cards = [], lead_suit = '', and each player's played_card = ''."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting with seat leader and going clockwise",
      "answer": "one card from the player's hand that is legal to play (see offers)",
      "effect": "Remove the chosen card from the player's hand, append it (with the seat) to trick_cards, and set played_card. If lead_suit == '' and the card is Green, Yellow or Black, set lead_suit to that suit. Each player hears the cards played before them."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set trick_winner to the seat holding the first applicable card: (1) if trick_cards holds both SkullKing and Mermaid, the Mermaid; (2) else the SkullKing; (3) else the first Pirate played; (4) else the Mermaid; (5) else the highest Black card; (6) else, if lead_suit is not empty, the highest card of lead_suit; (7) else (all Escapes) the first card played. Add 1 to the winner's tricks_won. If the winning card is the SkullKing, add 30 to the winner's bonus for each Pirate in trick_cards. If the winning card is the Mermaid and trick_cards holds the SkullKing, add 40 to the winner's bonus. Set leader = trick_winner."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the cards played (trick_cards), the trick_winner seat and any bonus just recorded."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 3, for each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid == 0 and tricks_won == 0, score += 20 + bonus; if bid == 0 and tricks_won > 0, score -= 20; if bid >= 1 and tricks_won != bid, score -= 10 * |bid - tricks_won|. Then set tricks_won = 0 and bonus = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 3: announce every seat's score after hand {hand_number}."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. If trick_in_hand == 3, then hand_number += 1 and trick_in_hand = 1; otherwise trick_in_hand += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round > 27; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round > 27",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 9 hands. The highest score wins, and players tied for the highest share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand starts (trick_in_hand == 1), then each of the 3 players is dealt 3 cards at random from the 25-card deck into their hand, and the 16 undealt cards stay in deck unseen."
    },
    {
      "id": "R2",
      "text": "When cards are dealt, then each player sees only their own hand."
    },
    {
      "id": "R3",
      "text": "When a hand starts, then all players bid at the same time, each a whole number from 0 to 3, and all bids are revealed only after everyone has bid."
    },
    {
      "id": "R4",
      "text": "When hand h starts, then its first leader is seat ((h-1) mod 3) + 1: seat 1 for hands 1, 4 and 7, seat 2 for hands 2, 5 and 8, and seat 3 for hands 3, 6 and 9."
    },
    {
      "id": "R5",
      "text": "When a trick is played, then the leader plays first, then the next seat clockwise, then the third seat, each playing one card face up from their hand."
    },
    {
      "id": "R6",
      "text": "When the first suited card (Green, Yellow or Black) is played in a trick, then its suit becomes the lead suit, even if special cards were played before it."
    },
    {
      "id": "R7",
      "text": "When no suited card is played in a trick, then the trick has no lead suit."
    },
    {
      "id": "R8",
      "text": "When a lead suit exists and a player holds a card of that suit, then they are offered only cards of that suit and special cards."
    },
    {
      "id": "R9",
      "text": "When a player holds no card of the lead suit, or there is no lead suit yet, then they are offered every card in their hand."
    },
    {
      "id": "R10",
      "text": "When a trick contains both the Skull King and the Mermaid, then the Mermaid wins it."
    },
    {
      "id": "R11",
      "text": "When a trick contains the Skull King and no Mermaid, then the Skull King wins it."
    },
    {
      "id": "R12",
      "text": "When a trick contains no Skull King and at least one Pirate, then the first Pirate played wins it."
    },
    {
      "id": "R13",
      "text": "When a trick contains the Mermaid but no Skull King and no Pirate, then the Mermaid wins it."
    },
    {
      "id": "R14",
      "text": "When a trick contains no Skull King, Pirate or Mermaid but at least one Black card, then the highest Black card wins it."
    },
    {
      "id": "R15",
      "text": "When a trick contains no special card that wins and no Black card, then the highest card of the lead suit wins it."
    },
    {
      "id": "R16",
      "text": "When a trick contains only Escapes, then the first card played wins it."
    },
    {
      "id": "R17",
      "text": "When a player wins a trick, then their tricks_won rises by 1 and they lead the next trick of the hand."
    },
    {
      "id": "R18",
      "text": "When the Skull King wins a trick, then its player's bonus rises by 30 for each Pirate in that trick."
    },
    {
      "id": "R19",
      "text": "When the Mermaid wins a trick containing the Skull King, then its player's bonus rises by 40."
    },
    {
      "id": "R20",
      "text": "When a trick ends, then its cards, its winner and any bonus are announced to everyone."
    },
    {
      "id": "R21",
      "text": "When a hand ends and a player bid 1, 2 or 3 and won exactly that many tricks, then they score +20 per trick bid plus their bonus (for example, bid 2 and won 2 scores +40 plus bonus)."
    },
    {
      "id": "R22",
      "text": "When a hand ends and a player bid 0 and won 0 tricks, then they score +20 plus their bonus."
    },
    {
      "id": "R23",
      "text": "When a hand ends and a player bid 0 but won at least 1 trick, then they score -20 and lose their bonus."
    },
    {
      "id": "R24",
      "text": "When a hand ends and a player bid 1, 2 or 3 but missed, then they score -10 per trick of difference and lose their bonus (for example, bid 3 and won 1 scores -20)."
    },
    {
      "id": "R25",
      "text": "When a hand ends, then scores are announced and every player's tricks_won and bonus reset to 0."
    },
    {
      "id": "R26",
      "text": "When round 27 (the third trick of hand 9) has been scored, then the game ends."
    },
    {
      "id": "R27",
      "text": "When the game ends, then the player with the highest score wins, and players tied for the highest share the win."
    }
  ],
  "offers": [
    {
      "question": "Bid at the start of a hand",
      "who": "all seats, at once",
      "options": "0, 1, 2 or 3"
    },
    {
      "question": "Card to play in a trick",
      "who": "each seat in turn, starting with the leader",
      "options": "If lead_suit is empty (the player leads, or only special cards have been played so far): every card in their hand. If lead_suit is set and the player holds at least one card of that suit: only their cards of the lead suit plus any Pirate, Escape, Mermaid or SkullKing they hold. If lead_suit is set and the player holds no card of that suit: every card in their hand."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the game at 3 seats, and the 25-card deck, the 3-card deal and the clockwise leader rotation are all built for 3. Minimum and maximum are both 3."
    },
    {
      "what": "No free-talk step before bids or plays",
      "why": "The source has no talk. Strategy comes from reading the revealed bids and the cards played (whether to win or duck a trick to land your own bid, or to spoil a rival's), so added talk would only add words."
    },
    {
      "what": "One trick per round, with the deal, bid and scoring steps run only when trick_in_hand is 1 or 3",
      "why": "The source sets each round to one trick (27 rounds). Single-step 'when' conditions keep the step list flat."
    },
    {
      "what": "Ties at the top share the win",
      "why": "The source calls a top tie a draw among the tied players, which is exactly a shared win."
    }
  ],
  "simplifications": [
    {
      "what": "The 16 undealt cards stay in the deck list rather than a separate set-aside pile",
      "why": "They are unseen and unused until the next hand's reshuffle, so a separate list adds nothing."
    },
    {
      "what": "Card play uses ask in seat order starting from the leader",
      "why": "Tricks are sequential in the source; each later player must see the earlier cards to follow suit."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid, tricks_won; table: none.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
{"name":"Deal: each seat gets 3 cards, 16 stay in deck (after one trick each hand holds 2)","rule":"R1","players":3,"seed":1,"default":"first","rounds":1,
 "expect":{"lens":{"game":{"deck":16},"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"Each player holds their own dealt hand (hand sizes only, deal is random)","rule":"R2","players":3,"seed":2,"default":"first","rounds":1,
 "expect":{"lens":{"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"All seats bid 0-3 and the bids are recorded","rule":"R3","players":3,"seed":3,"default":"first","rounds":1,
 "rules":[{"seat":1,"options_include":3},{"seat":2,"options_include":0},{"seat":3,"options_include":2}],
 "expect":{"players":{"1":{"bid":3},"2":{"bid":0},"3":{"bid":2}},
           "offered":[{"seat":1,"option":0},{"seat":1,"option":3},{"seat":2,"option":3},{"seat":3,"option":0}]}},
{"name":"Hand 2 is led by seat 2 (all-Escape deal, so the leader wins the trick)","rule":"R4","players":3,"seed":4,"default":"first","rounds":1,
 "given":{"game":{"deck":["Escape","Escape","Escape","Escape","Escape","Escape","Escape","Escape","Escape"],"hand_number":2,"trick_in_hand":1,"round":4,"leader":1,"trick_cards":[]},
          "players":{"1":{"hand":[]},"2":{"hand":[]},"3":{"hand":[]}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"Play goes clockwise from the leader: the first Pirate (seat 1, after leader 3) wins","rule":"R5","players":3,"seed":5,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":3},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["Pirate"],"tricks_won":0},"3":{"hand":["G5"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":1},"2":{"tricks_won":0},"3":{"tricks_won":0}}}},
{"name":"A suited card played after an Escape sets the lead suit, so seat 3 must follow Yellow","rule":"R6","players":3,"seed":6,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Y3"],"tricks_won":0},"3":{"hand":["G7","Y5"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}},
           "offered":[{"seat":3,"option":"Y5"}],"not_offered":[{"seat":3,"option":"G7"}]}},
{"name":"No suited card played: no lead suit, the Mermaid wins","rule":"R7","players":3,"seed":7,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Escape"],"tricks_won":0},"3":{"hand":["Mermaid"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Holding the lead suit, seat 2 is offered only Green and special cards","rule":"R8","players":3,"seed":8,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G3"],"tricks_won":0},"2":{"hand":["G5","Y7","Pirate"],"tricks_won":0},"3":{"hand":["Y1"],"tricks_won":0}}},
 "rules":[{"seat":2,"options_include":"G5"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}},
           "offered":[{"seat":2,"option":"G5"},{"seat":2,"option":"Pirate"}],"not_offered":[{"seat":2,"option":"Y7"}]}},
{"name":"The leader and a player void in the lead suit are offered every card","rule":"R9","players":3,"seed":9,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G3","Y2"],"tricks_won":0},"2":{"hand":["Y7","B2"],"tricks_won":0},"3":{"hand":["Y1"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"G3"},{"seat":2,"options_include":"B2"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}},
           "offered":[{"seat":1,"option":"Y2"},{"seat":2,"option":"Y7"},{"seat":2,"option":"B2"}]}},
{"name":"Mermaid beats the Skull King","rule":"R10","players":3,"seed":10,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0},"2":{"hand":["G5"],"tricks_won":0},"3":{"hand":["Mermaid"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Skull King beats a Pirate when there is no Mermaid","rule":"R11","players":3,"seed":11,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["SkullKing"],"tricks_won":0},"3":{"hand":["Y7"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The first Pirate played wins","rule":"R12","players":3,"seed":12,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":2},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["Y7"],"tricks_won":0},"3":{"hand":["Pirate"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Mermaid wins without Skull King or Pirate","rule":"R13","players":3,"seed":13,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G7"],"tricks_won":0},"2":{"hand":["Mermaid"],"tricks_won":0},"3":{"hand":["B5"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The highest Black card wins over the lead suit","rule":"R14","players":3,"seed":14,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G7"],"tricks_won":0},"2":{"hand":["B1"],"tricks_won":0},"3":{"hand":["B3"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"The highest card of the lead suit wins and an off-suit card does not","rule":"R15","players":3,"seed":15,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Y2"],"tricks_won":0},"2":{"hand":["Y6"],"tricks_won":0},"3":{"hand":["G7"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"All Escapes: the first card played (the leader, seat 2) wins","rule":"R16","players":3,"seed":16,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":2},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Escape"],"tricks_won":0},"3":{"hand":["Escape"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The trick winner gains a trick and leads the next trick (shown by the all-Escape last trick)","rule":"R17","players":3,"seed":17,"default":"first","rounds":2,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2","Escape"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["G6","Escape"],"tricks_won":0,"bid":2,"score":0,"bonus":0},
                     "3":{"hand":["G4","Escape"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"G2"},{"seat":2,"options_include":"G6"},{"seat":3,"options_include":"G4"}],
 "expect":{"players":{"1":{"score":20},"2":{"score":40},"3":{"score":20}}}},
{"name":"Skull King capturing two Pirates adds 60 bonus, paid on an exact bid","rule":"R18","players":3,"seed":18,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":80},"2":{"score":20},"3":{"score":20}}}},
{"name":"Mermaid capturing the Skull King adds 40 bonus","rule":"R19","players":3,"seed":19,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["Mermaid"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "3":{"hand":["G1"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":20},"2":{"score":60},"3":{"score":20}}}},
{"name":"After a trick the winner is recorded for everyone (tricks_won)","rule":"R20","players":3,"seed":20,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2"],"tricks_won":0},"2":{"hand":["G4"],"tricks_won":0},"3":{"hand":["G3"],"tricks_won":0}}},
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"An exact bid of 2 scores +40 and an exact bid of 1 scores +20","rule":"R21","players":3,"seed":21,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":1,"bid":2,"score":10,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":1,"bid":1,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":50},"2":{"score":20},"3":{"score":-10}}}},
{"name":"Bid 0 and won 0 scores +20","rule":"R22","players":3,"seed":22,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":20},"2":{"score":20},"3":{"score":20}}}},
{"name":"Bid 0 but won a trick scores -20 and loses the Skull King bonus","rule":"R23","players":3,"seed":23,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["G1"],"tricks_won":1,"bid":1,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":-20},"2":{"score":20},"3":{"score":20}}}},
{"name":"A missed bid scores -10 per trick of difference and loses the bonus","rule":"R24","players":3,"seed":24,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":3,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":2,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":-20},"2":{"score":-20},"3":{"score":-10}}}},
{"name":"At the end of a hand scores are applied and tricks_won resets to 0","rule":"R25","players":3,"seed":25,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2"],"tricks_won":1,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["G6"],"tricks_won":1,"bid":2,"score":0,"bonus":0},
                     "3":{"hand":["G4"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "expect":{"players":{"1":{"score":20,"tricks_won":0},"2":{"score":40,"tricks_won":0},"3":{"score":20,"tricks_won":0}}}},
{"name":"The game ends after round 27 is scored; the highest score wins","rule":"R26","players":3,"seed":26,"default":"first",
 "given":{"game":{"trick_in_hand":3,"round":27,"hand_number":9,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":100,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":90,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":1,"bid":1,"score":120,"bonus":0}}},
 "expect":{"winner":3,"standings":{"1":120,"2":110,"3":140},"players":{"1":{"score":120},"2":{"score":110},"3":{"score":140}}}},
{"name":"Seats tied for the highest final score share the win","rule":"R27","players":3,"seed":27,"default":"first",
 "given":{"game":{"trick_in_hand":3,"round":27,"hand_number":9,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":100,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":90,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":130,"bonus":0}}},
 "expect":{"winner":[1,3],"standings":{"1":120,"2":110,"3":120}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 16: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 21: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name); scenario 26: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
{"name":"Deal: each seat gets 3 cards, 16 stay in deck (after one trick each hand holds 2)","rule":"R1","players":3,"seed":1,"default":"first","rounds":1,
 "rules":[{"seat":1,"options_include":0},{"seat":2,"options_include":0},{"seat":3,"options_include":0}],
 "expect":{"lens":{"game":{"deck":16},"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"Each player holds their own dealt hand (hand sizes only, deal is random)","rule":"R2","players":3,"seed":2,"default":"first","rounds":1,
 "rules":[{"seat":1,"options_include":1},{"seat":2,"options_include":1},{"seat":3,"options_include":1}],
 "expect":{"lens":{"players":{"1":{"hand":2},"2":{"hand":2},"3":{"hand":2}}}}},
{"name":"All seats bid 0-3 and the bids are recorded","rule":"R3","players":3,"seed":3,"default":"first","rounds":1,
 "rules":[{"seat":1,"options_include":3},{"seat":2,"options_include":0},{"seat":3,"options_include":2}],
 "expect":{"players":{"1":{"bid":3},"2":{"bid":0},"3":{"bid":2}},
           "offered":[{"seat":1,"option":0},{"seat":1,"option":3},{"seat":2,"option":3},{"seat":3,"option":0}]}},
{"name":"Hand 2 is led by seat 2 (all-Escape deal, so the leader wins the trick)","rule":"R4","players":3,"seed":4,"default":"first","rounds":1,
 "given":{"game":{"deck":["Escape","Escape","Escape","Escape","Escape","Escape","Escape","Escape","Escape"],"hand_number":2,"trick_in_hand":1,"round":4,"leader":1,"trick_cards":[]},
          "players":{"1":{"hand":[]},"2":{"hand":[]},"3":{"hand":[]}}},
 "rules":[{"seat":1,"options_include":0},{"seat":2,"options_include":1},{"seat":3,"options_include":0},
          {"seat":1,"options_include":"Escape"},{"seat":2,"options_include":"Escape"},{"seat":3,"options_include":"Escape"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"Play goes clockwise from the leader: the first Pirate (seat 1, after leader 3) wins","rule":"R5","players":3,"seed":5,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":3},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["Pirate"],"tricks_won":0},"3":{"hand":["G5"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Pirate"},{"seat":2,"options_include":"Pirate"},{"seat":3,"options_include":"G5"}],
 "expect":{"players":{"1":{"tricks_won":1},"2":{"tricks_won":0},"3":{"tricks_won":0}}}},
{"name":"A suited card played after an Escape sets the lead suit, so seat 3 must follow Yellow","rule":"R6","players":3,"seed":6,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Y3"],"tricks_won":0},"3":{"hand":["G7","Y5"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Escape"},{"seat":2,"options_include":"Y3"},{"seat":3,"options_include":"Y5"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}},
           "offered":[{"seat":3,"option":"Y5"}],"not_offered":[{"seat":3,"option":"G7"}]}},
{"name":"No suited card played: no lead suit, the Mermaid wins","rule":"R7","players":3,"seed":7,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Escape"],"tricks_won":0},"3":{"hand":["Mermaid"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Escape"},{"seat":2,"options_include":"Escape"},{"seat":3,"options_include":"Mermaid"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Holding the lead suit, seat 2 is offered only Green and special cards","rule":"R8","players":3,"seed":8,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G3"],"tricks_won":0},"2":{"hand":["G5","Y7","Pirate"],"tricks_won":0},"3":{"hand":["Y1"],"tricks_won":0}}},
 "rules":[{"seat":2,"options_include":"G5"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}},
           "offered":[{"seat":2,"option":"G5"},{"seat":2,"option":"Pirate"}],"not_offered":[{"seat":2,"option":"Y7"}]}},
{"name":"The leader and a player void in the lead suit are offered every card","rule":"R9","players":3,"seed":9,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G3","Y2"],"tricks_won":0},"2":{"hand":["Y7","B2"],"tricks_won":0},"3":{"hand":["Y1"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"G3"},{"seat":2,"options_include":"B2"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}},
           "offered":[{"seat":1,"option":"Y2"},{"seat":2,"option":"Y7"},{"seat":2,"option":"B2"}]}},
{"name":"Mermaid beats the Skull King","rule":"R10","players":3,"seed":10,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0},"2":{"hand":["G5"],"tricks_won":0},"3":{"hand":["Mermaid"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"SkullKing"},{"seat":2,"options_include":"G5"},{"seat":3,"options_include":"Mermaid"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Skull King beats a Pirate when there is no Mermaid","rule":"R11","players":3,"seed":11,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["SkullKing"],"tricks_won":0},"3":{"hand":["Y7"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Pirate"},{"seat":2,"options_include":"SkullKing"},{"seat":3,"options_include":"Y7"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The first Pirate played wins","rule":"R12","players":3,"seed":12,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":2},
          "players":{"1":{"hand":["Pirate"],"tricks_won":0},"2":{"hand":["Y7"],"tricks_won":0},"3":{"hand":["Pirate"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Pirate"},{"seat":2,"options_include":"Y7"},{"seat":3,"options_include":"Pirate"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"Mermaid wins without Skull King or Pirate","rule":"R13","players":3,"seed":13,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G7"],"tricks_won":0},"2":{"hand":["Mermaid"],"tricks_won":0},"3":{"hand":["B5"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"G7"},{"seat":2,"options_include":"Mermaid"},{"seat":3,"options_include":"B5"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The highest Black card wins over the lead suit","rule":"R14","players":3,"seed":14,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G7"],"tricks_won":0},"2":{"hand":["B1"],"tricks_won":0},"3":{"hand":["B3"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"G7"},{"seat":2,"options_include":"B1"},{"seat":3,"options_include":"B3"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1}}}},
{"name":"The highest card of the lead suit wins and an off-suit card does not","rule":"R15","players":3,"seed":15,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["Y2"],"tricks_won":0},"2":{"hand":["Y6"],"tricks_won":0},"3":{"hand":["G7"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Y2"},{"seat":2,"options_include":"Y6"},{"seat":3,"options_include":"G7"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"All Escapes: the first card played (the leader, seat 2) wins","rule":"R16","players":3,"seed":16,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":2},
          "players":{"1":{"hand":["Escape"],"tricks_won":0},"2":{"hand":["Escape"],"tricks_won":0},"3":{"hand":["Escape"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"Escape"},{"seat":2,"options_include":"Escape"},{"seat":3,"options_include":"Escape"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"The trick winner gains a trick and leads the next trick (shown by the all-Escape last trick)","rule":"R17","players":3,"seed":17,"default":"first","rounds":2,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2","Escape"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["G6","Escape"],"tricks_won":0,"bid":2,"score":0,"bonus":0},
                     "3":{"hand":["G4","Escape"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"G2"},{"seat":2,"options_include":"G6"},{"seat":3,"options_include":"G4"}],
 "expect":{"players":{"1":{"score":20},"2":{"score":40},"3":{"score":20}}}},
{"name":"Skull King capturing two Pirates adds 60 bonus, paid on an exact bid","rule":"R18","players":3,"seed":18,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"SkullKing"},{"seat":2,"options_include":"Pirate"},{"seat":3,"options_include":"Pirate"}],
 "expect":{"players":{"1":{"score":80},"2":{"score":20},"3":{"score":20}}}},
{"name":"Mermaid capturing the Skull King adds 40 bonus","rule":"R19","players":3,"seed":19,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["Mermaid"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "3":{"hand":["G1"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"SkullKing"},{"seat":2,"options_include":"Mermaid"},{"seat":3,"options_include":"G1"}],
 "expect":{"players":{"1":{"score":20},"2":{"score":60},"3":{"score":20}}}},
{"name":"After a trick the winner is recorded for everyone (tricks_won)","rule":"R20","players":3,"seed":20,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":2,"round":2,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2"],"tricks_won":0},"2":{"hand":["G4"],"tricks_won":0},"3":{"hand":["G3"],"tricks_won":0}}},
 "rules":[{"seat":1,"options_include":"G2"},{"seat":2,"options_include":"G4"},{"seat":3,"options_include":"G3"}],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0}}}},
{"name":"An exact bid of 2 scores +40 and an exact bid of 1 scores +20","rule":"R21","players":3,"seed":21,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":1,"bid":2,"score":10,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":1,"bid":1,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"B5"},{"seat":2,"options_include":"G1"},{"seat":3,"options_include":"Y1"}],
 "expect":{"players":{"1":{"score":50},"2":{"score":20},"3":{"score":-10}}}},
{"name":"Bid 0 and won 0 scores +20","rule":"R22","players":3,"seed":22,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"B5"},{"seat":2,"options_include":"G1"},{"seat":3,"options_include":"Y1"}],
 "expect":{"players":{"1":{"score":20},"2":{"score":20},"3":{"score":20}}}},
{"name":"Bid 0 but won a trick scores -20 and loses the Skull King bonus","rule":"R23","players":3,"seed":23,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":0,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["G1"],"tricks_won":1,"bid":1,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"SkullKing"},{"seat":2,"options_include":"Pirate"},{"seat":3,"options_include":"G1"}],
 "expect":{"players":{"1":{"score":-20},"2":{"score":20},"3":{"score":20}}}},
{"name":"A missed bid scores -10 per trick of difference and loses the bonus","rule":"R24","players":3,"seed":24,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["SkullKing"],"tricks_won":0,"bid":3,"score":0,"bonus":0},
                     "2":{"hand":["Pirate"],"tricks_won":2,"bid":0,"score":0,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"SkullKing"},{"seat":2,"options_include":"Pirate"},{"seat":3,"options_include":"Y1"}],
 "expect":{"players":{"1":{"score":-20},"2":{"score":-20},"3":{"score":-10}}}},
{"name":"At the end of a hand scores are applied and tricks_won resets to 0","rule":"R25","players":3,"seed":25,"default":"first","rounds":1,
 "given":{"game":{"trick_in_hand":3,"round":3,"hand_number":1,"leader":1},
          "players":{"1":{"hand":["G2"],"tricks_won":1,"bid":1,"score":0,"bonus":0},
                     "2":{"hand":["G6"],"tricks_won":1,"bid":2,"score":0,"bonus":0},
                     "3":{"hand":["G4"],"tricks_won":0,"bid":0,"score":0,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"G2"},{"seat":2,"options_include":"G6"},{"seat":3,"options_include":"G4"}],
 "expect":{"players":{"1":{"score":20,"tricks_won":0},"2":{"score":40,"tricks_won":0},"3":{"score":20,"tricks_won":0}}}},
{"name":"The game ends after round 27 is scored; the highest score wins","rule":"R26","players":3,"seed":26,"default":"first",
 "given":{"game":{"trick_in_hand":3,"round":27,"hand_number":9,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":100,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":90,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":1,"bid":1,"score":120,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"B5"},{"seat":2,"options_include":"G1"},{"seat":3,"options_include":"Y1"}],
 "expect":{"winner":3,"standings":{"1":120,"2":110,"3":140},"players":{"1":{"score":120},"2":{"score":110},"3":{"score":140}}}},
{"name":"Seats tied for the highest final score share the win","rule":"R27","players":3,"seed":27,"default":"first",
 "given":{"game":{"trick_in_hand":3,"round":27,"hand_number":9,"leader":1},
          "players":{"1":{"hand":["B5"],"tricks_won":0,"bid":1,"score":100,"bonus":0},
                     "2":{"hand":["G1"],"tricks_won":0,"bid":0,"score":90,"bonus":0},
                     "3":{"hand":["Y1"],"tricks_won":0,"bid":1,"score":130,"bonus":0}}},
 "rules":[{"seat":1,"options_include":"B5"},{"seat":2,"options_include":"G1"},{"seat":3,"options_include":"Y1"}],
 "expect":{"winner":[1,3],"standings":{"1":120,"2":110,"3":120}}}
]
```
````
