# 19 scenarios

- time: 2026-10-28T03:19:51+00:00 (93.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 af108a7025b4906b, reply sha256 0669fce1dc6a4a72

## Sent

````
SPEC:
{
  "name": "Quick Reversis",
  "summary": "A four-player trick-avoidance card game over 4 hands of 6 tricks: take as few card points as possible, unless you take every trick of a hand (a reversis), which wipes that hand's points for you and charges 15 to each opponent; the lowest total wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 24,
    "cards_per_suit": 6,
    "suits": 4,
    "cards_dealt_per_player": 6,
    "hands": 4,
    "tricks_per_hand": 6,
    "total_rounds": 24,
    "ace_points": 4,
    "king_points": 3,
    "queen_points": 2,
    "jack_points": 1,
    "nine_points": 0,
    "eight_points": 0,
    "quinola_points": 5,
    "points_per_hand": 44,
    "reversis_subtract": 44,
    "reversis_bonus_to_others": 15,
    "rank_ace": 6,
    "rank_king": 5,
    "rank_queen": 4,
    "rank_jack": 3,
    "rank_nine": 2,
    "rank_eight": 1,
    "sweeper_none_code": 0
  },
  "attributes": {
    "player": [
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points taken so far, with reversis adjustments. Lower is better.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player holds in the current hand, for example 'QH' or 'JH'.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this player played to the current trick, revealed when all cards are shown.",
        "observable": true
      },
      {
        "key": "tricks_this_hand",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks this player has won in the current hand.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "AS",
          "KS",
          "QS",
          "JS",
          "9S",
          "8S",
          "AH",
          "KH",
          "QH",
          "JH",
          "9H",
          "8H",
          "AD",
          "KD",
          "QD",
          "JD",
          "9D",
          "8D",
          "AC",
          "KC",
          "QC",
          "JC",
          "9C",
          "8C"
        ],
        "meaning": "The undealt cards. It is refilled to all 24 cards at the start of each hand.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current trick number, from 1 to 24.",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current hand, from 1 to 4.",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that leads the current trick.",
        "observable": true
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The suit of the card led to the current trick: S, H, D or C.",
        "observable": true
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that played the highest card of the led suit in the current trick.",
        "observable": true
      },
      {
        "key": "trick_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The sum of the card points of the 4 cards in the current trick.",
        "observable": false
      },
      {
        "key": "sweeper",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that has won every trick of the hand so far, or 0 for 'none'.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats are numbered 1, 2, 3 and 4, and every player's total is set to 0.",
    "The table deck is defined as the 24 cards A, K, Q, J, 9 and 8 of Spades, Hearts, Diamonds and Clubs.",
    "round and hand_number start at 0, and sweeper starts at 0 (none)."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; if (round - 1) % 6 == 0: hand_number += 1, deck is reset to all 24 cards, every player's hand is cleared and tricks_this_hand is set to 0, then 6 cards are dealt to each player by random draws (each card is removed from deck and appended to that player's hand), leader = hand_number, and sweeper = 0 (none). Every player's played_card is cleared."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own hand, plus the public total, leader, round, hand_number and sweeper."
    },
    {
      "action": "ask",
      "who": "the seat equal to leader",
      "answer": "one card from their hand",
      "effect": "The card is removed from the leader's hand and set as the leader's played_card; led_suit = the suit of that card."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {leader} leads {played_card}; the led suit is {led_suit}.'"
    },
    {
      "action": "poll",
      "who": "every seat except leader",
      "answer": "one card from their hand; if the hand holds any card of led_suit, only cards of led_suit",
      "effect": "Each chosen card is removed from that player's hand and set as their played_card. No answer is seen until all three are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal all four played_card values together."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_winner = the seat whose played_card is of led_suit with the highest rank (A=6, K=5, Q=4, J=3, 9=2, 8=1); trick_points = the sum of the points of the 4 played cards (A=4, K=3, Q=2, J=1, 9=0, 8=0, but JH=5); the trick_winner's total += trick_points and their tricks_this_hand += 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If (round - 1) % 6 == 0: sweeper = trick_winner. Otherwise, if trick_winner != sweeper: sweeper = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "leader = trick_winner."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce: 'Seat {trick_winner} wins the trick and takes {trick_points} points. Totals: seat 1 {total}, seat 2 {total}, seat 3 {total}, seat 4 {total}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round % 6 == 0 and sweeper != 0: the player whose seat equals sweeper subtracts 44 from total, and every other player adds 15 to total. Announce the reversis if it happened."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round == 24, end the game; otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round == 24",
    "rank_by": "0 - you.total",
    "decided_by": "Each player's standing is minus their total, so the lowest total ranks highest. The player with the lowest total wins. If two or more players tie for the lowest total, they share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player's total is 0."
    },
    {
      "id": "R2",
      "text": "When a hand starts (rounds 1, 7, 13 and 19), then the deck is refilled to 24 cards and each player is dealt 6 cards from it into their hand, leaving the deck empty."
    },
    {
      "id": "R3",
      "text": "When hand h starts, then the leader of its first trick is seat h (hand 1 seat 1, hand 2 seat 2, hand 3 seat 3, hand 4 seat 4)."
    },
    {
      "id": "R4",
      "text": "When a hand starts, then the sweeper is set to none (0)."
    },
    {
      "id": "R5",
      "text": "When a player's hand is dealt, then only that player sees it; other players do not."
    },
    {
      "id": "R6",
      "text": "When the leader leads, then they may play any card in their hand, and that card's suit becomes the led suit."
    },
    {
      "id": "R7",
      "text": "When a non-leader holds at least one card of the led suit, then they must play a card of the led suit."
    },
    {
      "id": "R8",
      "text": "When a non-leader holds no card of the led suit, then they may play any card in their hand."
    },
    {
      "id": "R9",
      "text": "When the three non-leaders choose, then they choose simultaneously, and no choice is seen until all are revealed together."
    },
    {
      "id": "R10",
      "text": "When cards are compared, then the highest card of the led suit wins, with ranking A > K > Q > J > 9 > 8, and cards of other suits never win because there are no trumps."
    },
    {
      "id": "R11",
      "text": "When a trick is won, then its winner adds the points of all 4 cards to their total: Ace 4, King 3, Queen 2, Jack 1, Nine 0, Eight 0, except the Jack of Hearts (Quinola), which counts 5."
    },
    {
      "id": "R12",
      "text": "When a card is played, then it is removed from the player's hand and does not return for the rest of the hand."
    },
    {
      "id": "R13",
      "text": "When the first trick of a hand is won, then the sweeper becomes that trick's winner."
    },
    {
      "id": "R14",
      "text": "When a later trick of a hand is won by a player other than the sweeper, then the sweeper becomes none (0)."
    },
    {
      "id": "R15",
      "text": "When a trick is won, then its winner leads the next trick."
    },
    {
      "id": "R16",
      "text": "When a trick ends, then every player's total is announced."
    },
    {
      "id": "R17",
      "text": "When a hand ends (after tricks 6, 12, 18 and 24) and the sweeper is a player who took all 6 tricks, then that player subtracts 44 from their total and each other player adds 15 to their total."
    },
    {
      "id": "R18",
      "text": "When a hand ends and the sweeper is none, then no totals are adjusted."
    },
    {
      "id": "R19",
      "text": "When round 24 has been played, then the game ends."
    },
    {
      "id": "R20",
      "text": "When the game ends, then the player with the lowest total wins, and players tied for the lowest total share the result (a draw)."
    },
    {
      "id": "R21",
      "text": "When a hand is played, then there is no table talk."
    }
  ],
  "offers": [
    {
      "question": "The leader's lead",
      "who": "the seat equal to leader",
      "options": "every card currently in that seat's hand"
    },
    {
      "question": "A follower's card",
      "who": "each of the three seats other than leader",
      "options": "if the seat holds any card of led_suit: exactly the cards of led_suit in its hand; otherwise: every card in its hand"
    }
  ],
  "choices": [
    {
      "what": "4 players: min 4, max 4, suggested 4",
      "why": "The designer fixed 4. The 24-card deck deals exactly 6 cards to each of 4 players, and the 44-point and 15-point values assume this size. Fewer seats would leave cards undealt and change the avoidance tension; more would not fit the deck."
    },
    {
      "what": "The sweeper's 'none' is encoded as 0",
      "why": "Seats are 1 to 4, so 0 marks no sweeper unambiguously as a number."
    },
    {
      "what": "Card ranks are encoded as numbers (A=6, K=5, Q=4, J=3, 9=2, 8=1)",
      "why": "This lets the trick winner be found by arithmetic comparison within the led suit."
    },
    {
      "what": "Card names are written as rank followed by suit letter (for example JH is the Quinola)",
      "why": "Hands, the deck and played cards need a compact text form."
    },
    {
      "what": "No talk step",
      "why": "The source says there is no table talk."
    },
    {
      "what": "The leader is asked with ask; the followers answer with poll",
      "why": "The source plays the lead face up first, then has the other three choose at the same moment."
    },
    {
      "what": "Ranking expression 0 - total",
      "why": "The engine picks the highest value, and the source's winner is the lowest total. A tie at the top is shared, which matches the source's draw."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player sheds high-point cards (especially the Quinola) when void in the led suit, ducks under the current high card, tracks which cards have left the hand, and judges when to try a reversis or deliberately break an opponent's sweep."
    }
  ],
  "simplifications": [
    {
      "what": "The reveal of the three simultaneous cards is a tell after the poll",
      "why": "The engine reveals the polled answers together once all are in, which matches 'all cards are revealed together'."
    },
    {
      "what": "The trick winner's tricks_this_hand counter is added",
      "why": "It is a scratch counter that makes 'took all 6 tricks' checkable. The sweeper alone already decides the reversis."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total, played_card; table: round, hand_number, leader, led_suit, trick_winner, sweeper.
````

## Reply

````
```json
[
  {
    "name": "Every total starts at 0",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"total": 0},
        "2": {"total": 0},
        "3": {"total": 0},
        "4": {"total": 0}
      },
      "game": {"round": 0, "hand_number": 0, "sweeper": 0}
    }
  },
  {
    "name": "First hand deals 6 cards each and empties the deck (5 left after trick 1, deal is random)",
    "rule": "R2",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "expect": {
      "game": {"round": 1, "hand_number": 1},
      "lens": {
        "game": {"deck": 0},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "Hand 4 starts at round 19 with a fresh deal (who wins the trick depends on the random deal)",
    "rule": "R3",
    "players": 4,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 18, "hand_number": 3, "leader": 1, "sweeper": 0, "deck": []},
      "players": {"1": {"hand": []}, "2": {"hand": []}, "3": {"hand": []}, "4": {"hand": []}}
    },
    "expect": {
      "game": {"round": 19, "hand_number": 4},
      "lens": {
        "game": {"deck": 0},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "A new hand starts at round 7 after a sweep in hand 1 (random deal)",
    "rule": "R4",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 6, "hand_number": 1, "leader": 3, "sweeper": 3, "deck": []},
      "players": {"1": {"hand": []}, "2": {"hand": []}, "3": {"hand": []}, "4": {"hand": []}}
    },
    "expect": {
      "game": {"round": 7, "hand_number": 2},
      "lens": {
        "game": {"deck": 0},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "Each player holds their own dealt hand (random deal)",
    "rule": "R5",
    "players": 4,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "expect": {
      "lens": {
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "Leader may lead any card; KD sets led suit D",
    "rule": "R6",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "8H"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "game": {"led_suit": "D", "trick_winner": 1, "leader": 1, "round": 2},
      "players": {
        "1": {"played_card": "KD", "total": 5},
        "2": {"played_card": "QD"},
        "3": {"played_card": "8H"},
        "4": {"played_card": "9D"}
      },
      "offered": [
        {"seat": 1, "option": "8S"},
        {"seat": 1, "option": "AH"},
        {"seat": 1, "option": "QC"}
      ]
    }
  },
  {
    "name": "A follower holding the led suit must follow it",
    "rule": "R7",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "8H"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "players": {"2": {"played_card": "QD"}, "4": {"played_card": "9D"}},
      "offered": [
        {"seat": 4, "option": "8D"},
        {"seat": 4, "option": "9D"},
        {"seat": 2, "option": "QD"}
      ],
      "not_offered": [
        {"seat": 4, "option": "QH"},
        {"seat": 4, "option": "KH"},
        {"seat": 4, "option": "AC"},
        {"seat": 2, "option": "JS"},
        {"seat": 2, "option": "KC"}
      ]
    }
  },
  {
    "name": "A follower void in the led suit may play any card",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "JC"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "players": {"3": {"played_card": "JC"}, "1": {"total": 6}},
      "offered": [
        {"seat": 3, "option": "AS"},
        {"seat": 3, "option": "KS"},
        {"seat": 3, "option": "8H"},
        {"seat": 3, "option": "JC"}
      ]
    }
  },
  {
    "name": "All three followers' cards are revealed after the poll",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "9H"},
      {"seat": 4, "options_include": "8D"}
    ],
    "expect": {
      "players": {
        "1": {"played_card": "KD"},
        "2": {"played_card": "QD"},
        "3": {"played_card": "9H"},
        "4": {"played_card": "8D"}
      }
    }
  },
  {
    "name": "An off-suit ace does not win; the highest card of the led suit does",
    "rule": "R10",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "AS"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "game": {"trick_winner": 1},
      "players": {
        "1": {"total": 9},
        "2": {"total": 0},
        "3": {"total": 0},
        "4": {"total": 0}
      }
    }
  },
  {
    "name": "The Quinola (JH) counts 5: AH+JH+8H+KC = 12 to seat 3",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8H", "8S", "9S", "8D", "9D"]},
        "2": {"hand": ["JH", "AS", "KS", "QS", "JS"]},
        "3": {"hand": ["AH", "AD", "KD", "QD", "JD"]},
        "4": {"hand": ["KC", "QC", "JC", "9C", "8C"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "8H"},
      {"seat": 4, "options_include": "KC"}
    ],
    "expect": {
      "game": {"trick_winner": 3},
      "players": {
        "1": {"total": 0},
        "2": {"total": 0, "played_card": "JH"},
        "3": {"total": 12, "played_card": "AH"},
        "4": {"total": 0}
      }
    }
  },
  {
    "name": "Played cards leave the hand: each hand drops from 5 to 4",
    "rule": "R12",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "8H"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "lens": {
        "players": {"1": {"hand": 4}, "2": {"hand": 4}, "3": {"hand": 4}, "4": {"hand": 4}}
      }
    }
  },
  {
    "name": "First trick of a new hand is played after a broken hand (winner depends on the random deal)",
    "rule": "R13",
    "players": 4,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "given": {
      "game": {"round": 12, "hand_number": 2, "leader": 2, "sweeper": 0, "deck": []},
      "players": {"1": {"hand": []}, "2": {"hand": []}, "3": {"hand": []}, "4": {"hand": []}}
    },
    "expect": {
      "game": {"round": 13, "hand_number": 3},
      "lens": {
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "A later trick won by a non-sweeper sets sweeper to 0",
    "rule": "R14",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8H", "8S", "9S", "8D", "9D"]},
        "2": {"hand": ["JH", "AS", "KS", "QS", "JS"]},
        "3": {"hand": ["AH", "AD", "KD", "QD", "JD"]},
        "4": {"hand": ["KC", "QC", "JC", "9C", "8C"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "8H"},
      {"seat": 4, "options_include": "KC"}
    ],
    "expect": {
      "game": {"sweeper": 0, "trick_winner": 3}
    }
  },
  {
    "name": "The trick winner leads next",
    "rule": "R15",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8H", "8S", "9S", "8D", "9D"]},
        "2": {"hand": ["JH", "AS", "KS", "QS", "JS"]},
        "3": {"hand": ["AH", "AD", "KD", "QD", "JD"]},
        "4": {"hand": ["KC", "QC", "JC", "9C", "8C"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "8H"},
      {"seat": 4, "options_include": "KC"}
    ],
    "expect": {
      "game": {"leader": 3, "trick_winner": 3}
    }
  },
  {
    "name": "Totals after a trick are as announced",
    "rule": "R16",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8H", "8S", "9S", "8D", "9D"], "total": 2},
        "2": {"hand": ["JH", "AS", "KS", "QS", "JS"], "total": 0},
        "3": {"hand": ["AH", "AD", "KD", "QD", "JD"], "total": 0},
        "4": {"hand": ["KC", "QC", "JC", "9C", "8C"], "total": 0}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "8H"},
      {"seat": 4, "options_include": "KC"}
    ],
    "expect": {
      "players": {
        "1": {"total": 2},
        "2": {"total": 0},
        "3": {"total": 12},
        "4": {"total": 0}
      }
    }
  },
  {
    "name": "Reversis: seat 2 takes all 6 tricks, loses 44 and others gain 15",
    "rule": "R17",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 5, "hand_number": 1, "leader": 2, "sweeper": 2, "deck": []},
      "players": {
        "1": {"hand": ["8S"], "total": 2},
        "2": {"hand": ["AS"], "total": 30, "tricks_this_hand": 5},
        "3": {"hand": ["9H"], "total": 4},
        "4": {"hand": ["JC"], "total": 3}
      }
    },
    "expect": {
      "game": {"round": 6, "sweeper": 2, "trick_winner": 2},
      "players": {
        "1": {"total": 17},
        "2": {"total": -9},
        "3": {"total": 19},
        "4": {"total": 18}
      }
    }
  },
  {
    "name": "No sweeper at hand end: no adjustment",
    "rule": "R18",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 5, "hand_number": 1, "leader": 2, "sweeper": 0, "deck": []},
      "players": {
        "1": {"hand": ["8S"], "total": 2},
        "2": {"hand": ["AS"], "total": 30, "tricks_this_hand": 3},
        "3": {"hand": ["9H"], "total": 4},
        "4": {"hand": ["JC"], "total": 3}
      }
    },
    "expect": {
      "game": {"round": 6, "sweeper": 0},
      "players": {
        "1": {"total": 2},
        "2": {"total": 35},
        "3": {"total": 4},
        "4": {"total": 3}
      }
    }
  },
  {
    "name": "Game ends after round 24; lowest total wins",
    "rule": "R19",
    "players": 4,
    "seed": 1,
    "given": {
      "game": {"round": 23, "hand_number": 4, "leader": 4, "sweeper": 0, "deck": []},
      "players": {
        "1": {"hand": ["KC"], "total": 20},
        "2": {"hand": ["9D"], "total": 10},
        "3": {"hand": ["QH"], "total": 12},
        "4": {"hand": ["8C"], "total": 30}
      }
    },
    "expect": {
      "winner": 2,
      "standings": {"1": -25, "2": -10, "3": -12, "4": -30},
      "game": {"round": 24},
      "players": {
        "1": {"total": 25},
        "2": {"total": 10},
        "3": {"total": 12},
        "4": {"total": 30}
      }
    }
  },
  {
    "name": "Tied lowest totals share the win",
    "rule": "R20",
    "players": 4,
    "seed": 1,
    "given": {
      "game": {"round": 23, "hand_number": 4, "leader": 4, "sweeper": 0, "deck": []},
      "players": {
        "1": {"hand": ["KC"], "total": 20},
        "2": {"hand": ["9D"], "total": 10},
        "3": {"hand": ["QH"], "total": 10},
        "4": {"hand": ["8C"], "total": 30}
      }
    },
    "expect": {
      "winner": [2, 3],
      "standings": {"1": -25, "2": -10, "3": -10, "4": -30}
    }
  },
  {
    "name": "A trick plays through with only card choices (no talk)",
    "rule": "R21",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "given": {
      "game": {"round": 1, "hand_number": 1, "leader": 1, "sweeper": 1, "deck": []},
      "players": {
        "1": {"hand": ["8S", "AH", "KD", "9C", "QC"]},
        "2": {"hand": ["QD", "JS", "9S", "8C", "KC"]},
        "3": {"hand": ["AS", "KS", "8H", "9H", "JC"]},
        "4": {"hand": ["8D", "9D", "QH", "KH", "AC"]}
      }
    },
    "rules": [
      {"seat": 1, "options_include": "KD"},
      {"seat": 3, "options_include": "8H"},
      {"seat": 4, "options_include": "9D"}
    ],
    "expect": {
      "game": {"round": 2, "trick_winner": 1, "sweeper": 1},
      "players": {"1": {"total": 5}}
    }
  }
]
```
````
