# 23 scenarios

- time: 2026-10-27T18:29:38+00:00 (95.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 66a264fe6e4dbf7f, reply sha256 8b85d85bb83070a2

## Sent

````
SPEC:
{
  "name": "Knaves Short Deck with Bids",
  "summary": "Three players play 36 tricks with a 20-card deck, in six hands of six tricks. Each player bids how many tricks they will take each hand, Jacks in a won trick cost points, and an exact bid earns a bonus.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "num_players": 3,
    "deck_size": 20,
    "total_rounds": 36,
    "tricks_per_hand": 6,
    "num_hands": 6,
    "cards_per_player": 6,
    "turned_card_position": 19,
    "hidden_card_position": 20,
    "bid_min": 0,
    "bid_max": 6,
    "trick_base_points": 2,
    "penalty_JS": 1,
    "penalty_JC": 2,
    "penalty_JD": 3,
    "penalty_JH": 4,
    "exact_bid_bonus": 5,
    "rank_value_A": 5,
    "rank_value_K": 4,
    "rank_value_Q": 3,
    "rank_value_J": 2,
    "rank_value_10": 1,
    "trump_bonus": 10
  },
  "attributes": {
    "player": [
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running game score, added to at the end of each hand",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards the player holds in the current hand, seen only by the owner",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of tricks the player predicted for this hand, shown to all after the simultaneous bid",
        "observable": true
      },
      {
        "key": "tricks_taken",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won so far in this hand",
        "observable": true
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points scored in this hand so far",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card the player played to the current trick",
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
          "10S",
          "AC",
          "KC",
          "QC",
          "JC",
          "10C",
          "AD",
          "KD",
          "QD",
          "JD",
          "10D",
          "AH",
          "KH",
          "QH",
          "JH",
          "10H"
        ],
        "meaning": "Undealt cards; empty after each deal",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played so far this hand",
        "observable": false
      },
      {
        "key": "turned_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card 19 of the shuffled deck, face up and out of play",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit of turned_card (S, C, D or H)",
        "observable": true
      },
      {
        "key": "hidden_card",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Card 20 of the shuffled deck, face down, out of play, never revealed",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round (trick) number, 1 to 36",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current hand, floor((round-1)/6)+1",
        "observable": true
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Trick within the hand, ((round-1) mod 6)+1",
        "observable": false
      },
      {
        "key": "dealer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Dealer seat, ((hand_number-1) mod 3)+1",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "Seat that leads the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit of the leader's card in the current trick",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the most recent trick",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat three players, seats 1, 2 and 3.",
    "Set every player's total to 0 and hand to empty.",
    "Set round to 1, hand_number to 1 and trick_in_hand to 1.",
    "Set deck to the full 20-card list: AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: set dealer = ((hand_number-1) mod 3)+1 and leader = (dealer mod 3)+1. Set deck to the full 20-card list, empty every hand and discard, and set every bid, tricks_taken and hand_score to 0. Shuffle the deck once. Deal cards 1-6 to seat 1's hand, 7-12 to seat 2's hand and 13-18 to seat 3's hand. Put card 19 in turned_card and set trump_suit to its suit. Put card 20 in hidden_card. The deck is now empty. Announce turned_card, trump_suit, dealer and leader."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 1: each player is sent their own hand, plus the public turned_card and trump_suit."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 6",
      "effect": "When trick_in_hand == 1: set each player's bid to their answer. After all answers are in, broadcast every bid to all."
    },
    {
      "action": "ask",
      "who": "the seat equal to leader",
      "answer": "one card from own hand (any card)",
      "effect": "Remove the card from the leader's hand, set the leader's played_card to it, append it to discard, and set led_suit to its suit. Show the card to all."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 3)+1",
      "answer": "one card from own hand: a led_suit card if any is held, otherwise any card",
      "effect": "Remove the card from the hand, set played_card to it, append it to discard, and show it to all."
    },
    {
      "action": "ask",
      "who": "seat ((leader+1) mod 3)+1",
      "answer": "one card from own hand: a led_suit card if any is held, otherwise any card",
      "effect": "Remove the card from the hand, set played_card to it, append it to discard, and show it to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Score each played_card as rank value (A 5, K 4, Q 3, J 2, 10 1), plus 10 if its suit is trump_suit, or 0 if its suit is neither trump_suit nor led_suit. Set trick_winner to the seat with the highest score. That seat adds 1 to tricks_taken and adds 2 - (1 if JS played) - (2 if JC played) - (3 if JD played) - (4 if JH played) to hand_score. Set leader = trick_winner. Announce the winner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_hand == 6: each player with tricks_taken == bid adds 5 to hand_score. Every player then adds hand_score to total. Announce all totals."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Add 1 to round. Set trick_in_hand = ((round-1) mod 6)+1 and hand_number = floor((round-1)/6)+1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round > 36; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round > 36",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their total after the end-of-hand scoring of hand 6. The highest total wins. Players tied for the highest total share the result, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, every player's total is 0, hand_number is 1, and the deck holds the 20 cards AS KS QS JS 10S AC KC QC JC 10C AD KD QD JD 10D AH KH QH JH 10H."
    },
    {
      "id": "R2",
      "text": "Within a suit, cards rank A > K > Q > J > 10."
    },
    {
      "id": "R3",
      "text": "When round 36's trick and end-of-hand scoring are done, the game ends; it never runs a 37th trick."
    },
    {
      "id": "R4",
      "text": "When round is r, hand_number is floor((r-1)/6)+1 and trick_in_hand is ((r-1) mod 6)+1, so rounds 31-36 are hand 6."
    },
    {
      "id": "R5",
      "text": "When hand h begins, dealer is ((h-1) mod 3)+1: hand 1 is seat 1, hand 2 seat 2, hand 3 seat 3, hand 4 seat 1."
    },
    {
      "id": "R6",
      "text": "When a hand begins, leader of its first trick is (dealer mod 3)+1, so hand 1 is led by seat 2."
    },
    {
      "id": "R7",
      "text": "When trick_in_hand is 1, the deck is reset to 20 cards, hands and discard are emptied, bid, tricks_taken and hand_score are set to 0, and seats 1, 2 and 3 each receive 6 cards, seen only by their owner."
    },
    {
      "id": "R8",
      "text": "When a hand is dealt, card 19 becomes turned_card, visible to all, trump_suit is its suit, and it is not in any hand."
    },
    {
      "id": "R9",
      "text": "When a hand is dealt, card 20 becomes hidden_card, is never shown, and the deck then holds 0 cards."
    },
    {
      "id": "R10",
      "text": "When trick_in_hand is 1, all three seats bid simultaneously from 0-6, and after all are in, every bid is shown to all."
    },
    {
      "id": "R11",
      "text": "When a trick is played, the leader plays first, then seat (leader mod 3)+1, then the remaining seat; each played card leaves the hand, becomes played_card and is appended to discard."
    },
    {
      "id": "R12",
      "text": "When a non-leader holds a card of led_suit, they are offered only led_suit cards; when they hold none, they are offered every card in their hand."
    },
    {
      "id": "R13",
      "text": "When any trump is played, the highest trump wins the trick; otherwise the highest led_suit card wins; the winner leads the next trick."
    },
    {
      "id": "R14",
      "text": "When a player wins a trick, tricks_taken rises by 1 and hand_score rises by 2 minus 1 for JS, 2 for JC, 3 for JD and 4 for JH among the trick's cards, including a trump Jack (e.g. a trick containing JH and JS scores 2-4-1 = -3)."
    },
    {
      "id": "R15",
      "text": "When trick_in_hand 6 is scored, each player with tricks_taken equal to bid gains 5 hand_score, every player adds hand_score to total, and totals are announced."
    },
    {
      "id": "R16",
      "text": "When the game ends, the player with the highest total wins; players tied for highest share it, which the source calls a draw."
    }
  ],
  "offers": [
    {
      "question": "Bid (first round of each hand)",
      "who": "all three seats, simultaneously",
      "options": "0, 1, 2, 3, 4, 5, 6 for every seat"
    },
    {
      "question": "Lead a card",
      "who": "the seat equal to leader",
      "options": "every card in the leader's hand"
    },
    {
      "question": "Play a card (second and third to the trick)",
      "who": "seat (leader mod 3)+1, then the remaining seat",
      "options": "a seat holding a led_suit card: only its led_suit cards; a seat holding no led_suit card: every card in its hand"
    }
  ],
  "choices": [
    {
      "what": "3 players, min = max = suggested = 3",
      "why": "The designer fixed the game at 3. The deal uses exactly 18 of 20 cards, the dealer rotation is mod 3, and the 6-card hand fits only three seats."
    },
    {
      "what": "No talk step before bids or plays",
      "why": "The rules include no table talk, and adding it would add a mechanic."
    },
    {
      "what": "Trick winner computed by an arithmetic card score (rank 1-5, +10 for trump, 0 for an off-suit non-trump)",
      "why": "This reproduces R13 exactly by calculation, with no referee needed."
    },
    {
      "what": "hand_score, played_card and discard are public",
      "why": "The source leaves their visibility open; all are derivable from cards played face up."
    },
    {
      "what": "Strategy at the table",
      "why": "Players read their hand against the trump suit to bid accurately, dodge winning tricks loaded with costly Jacks (especially JH and JD), and dump Jacks onto opponents' tricks while steering toward their exact bid."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest total is a shared win for the tied players rather than a separate draw result",
      "why": "The engine ranks by one expression and lets players level at the top share the win. This is equivalent to the source's draw."
    },
    {
      "what": "Per-hand reset, deal and bid run as single steps carrying the condition trick_in_hand == 1, and end-of-hand scoring carries trick_in_hand == 6",
      "why": "The step list is flat; each conditional step is a single step, not an alternative block."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total, bid, tricks_taken; table: turned_card, trump_suit, hand_number, trick_winner.
````

## Reply

````
```json
[
  {
    "name": "Game starts with totals 0, hand 1 and the full 20-card deck",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {"1": {"total": 0}, "2": {"total": 0}, "3": {"total": 0}},
      "game": {"hand_number": 1},
      "lens": {"game": {"deck": 20}}
    }
  },
  {
    "name": "Within the led suit the Ace beats the King and the Queen",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["KS", "10C"], "tricks_taken": 0, "bid": 1, "hand_score": 0},
        "2": {"hand": ["AS", "10D"], "tricks_taken": 0, "bid": 1, "hand_score": 0},
        "3": {"hand": ["QS", "10H"], "tricks_taken": 0, "bid": 1, "hand_score": 0}
      },
      "game": {"round": 2, "trick_in_hand": 2, "hand_number": 1, "leader": 1, "dealer": 1, "trump_suit": "D", "turned_card": "JD", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "KS"},
      {"seat": 2, "options_include": "AS"},
      {"seat": 3, "options_include": "QS"}
    ],
    "expect": {
      "game": {"trick_winner": 2},
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 1}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "Game ends after round 36's scoring with no 37th trick",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": ["AS"], "bid": 6, "tricks_taken": 5, "hand_score": 0, "total": 10},
        "2": {"hand": ["KS"], "bid": 0, "tricks_taken": 0, "hand_score": 0, "total": 11},
        "3": {"hand": ["QS"], "bid": 1, "tricks_taken": 0, "hand_score": 0, "total": 0}
      },
      "game": {"round": 36, "trick_in_hand": 6, "hand_number": 6, "leader": 1, "dealer": 3, "trump_suit": "H", "turned_card": "10H", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "AS"},
      {"seat": 2, "options_include": "KS"},
      {"seat": 3, "options_include": "QS"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 17, "2": 16, "3": 0},
      "players": {"1": {"total": 17, "tricks_taken": 6}, "2": {"total": 16}, "3": {"total": 0}}
    }
  },
  {
    "name": "After round 30 the round becomes 31, which is hand 6",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["AD"], "bid": 1, "tricks_taken": 1, "hand_score": 0},
        "2": {"hand": ["KD"], "bid": 1, "tricks_taken": 1, "hand_score": 0},
        "3": {"hand": ["QD"], "bid": 1, "tricks_taken": 3, "hand_score": 0}
      },
      "game": {"round": 30, "trick_in_hand": 6, "hand_number": 5, "leader": 1, "dealer": 2, "trump_suit": "S", "turned_card": "10S", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "AD"},
      {"seat": 2, "options_include": "KD"},
      {"seat": 3, "options_include": "QD"}
    ],
    "expect": {
      "game": {"hand_number": 6, "trick_winner": 1}
    }
  },
  {
    "name": "Hand 4 begins with a fresh deal (random deal: only the hand number, the card counts and the bids are asserted)",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"total": 3}, "2": {"total": 6}, "3": {"total": 9}},
      "game": {"round": 19, "trick_in_hand": 1, "hand_number": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "2"},
      {"seat": 2, "options_include": "3"},
      {"seat": 3, "options_include": "4"}
    ],
    "expect": {
      "game": {"hand_number": 4},
      "players": {"1": {"bid": 2, "total": 3}, "2": {"bid": 3, "total": 6}, "3": {"bid": 4, "total": 9}},
      "lens": {"game": {"deck": 0, "discard": 3}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}
    }
  },
  {
    "name": "First trick of hand 1 is played by all seats (random deal: only the card counts and the bids are asserted)",
    "rule": "R6",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "3"},
      {"seat": 2, "options_include": "2"},
      {"seat": 3, "options_include": "5"}
    ],
    "expect": {
      "game": {"hand_number": 1},
      "players": {"1": {"bid": 3}, "2": {"bid": 2}, "3": {"bid": 5}},
      "lens": {"game": {"discard": 3, "deck": 0}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}
    }
  },
  {
    "name": "The start of a hand resets bids and re-deals 6 cards each without touching totals (random deal: only the counts are asserted)",
    "rule": "R7",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"total": 7, "bid": 5, "tricks_taken": 4, "hand_score": 3, "hand": []},
        "2": {"total": 3, "bid": 1, "tricks_taken": 1, "hand_score": 1, "hand": []},
        "3": {"total": 0, "bid": 0, "tricks_taken": 1, "hand_score": 2, "hand": []}
      },
      "game": {"round": 13, "trick_in_hand": 1, "hand_number": 3, "discard": ["AS", "KS", "QS"]}
    },
    "rules": [
      {"seat": 1, "options_include": "2"},
      {"seat": 2, "options_include": "2"},
      {"seat": 3, "options_include": "2"}
    ],
    "expect": {
      "players": {"1": {"total": 7, "bid": 2}, "2": {"total": 3, "bid": 2}, "3": {"total": 0, "bid": 2}},
      "lens": {"game": {"discard": 3, "deck": 0}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}
    }
  },
  {
    "name": "The deal uses 18 cards for the hands and none stays in the deck (random deal: only the counts are asserted)",
    "rule": "R8",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 0, "discard": 3}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}
    }
  },
  {
    "name": "After the deal the deck holds 0 cards (random deal: only the counts are asserted)",
    "rule": "R9",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 0}}
    }
  },
  {
    "name": "All three seats are offered bids 0 to 6 and each bid is recorded",
    "rule": "R10",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": "5"},
      {"seat": 2, "options_include": "3"},
      {"seat": 3, "options_include": "6"}
    ],
    "expect": {
      "players": {"1": {"bid": 5}, "2": {"bid": 3}, "3": {"bid": 6}},
      "offered": [
        {"seat": 1, "option": "6"}, {"seat": 2, "option": "6"}, {"seat": 3, "option": "2"},
        {"seat": 1, "option": "0"}, {"seat": 2, "option": "4"}, {"seat": 3, "option": "5"}
      ]
    }
  },
  {
    "name": "Leader seat 3 plays, then seat 1, then seat 2; the cards leave the hands and go to discard",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["QC", "10S"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "2": {"hand": ["KC", "JD"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "3": {"hand": ["AC", "KD"], "bid": 1, "tricks_taken": 1, "hand_score": 2}
      },
      "game": {"round": 2, "trick_in_hand": 2, "hand_number": 1, "leader": 3, "dealer": 1, "trump_suit": "S", "turned_card": "JS", "discard": ["AH", "KH", "QH"], "deck": []}
    },
    "rules": [
      {"seat": 3, "options_include": "AC"},
      {"seat": 1, "options_include": "QC"},
      {"seat": 2, "options_include": "KC"}
    ],
    "expect": {
      "game": {"trick_winner": 3},
      "players": {"3": {"tricks_taken": 2}, "1": {"tricks_taken": 0}, "2": {"tricks_taken": 0}},
      "lens": {"game": {"discard": 6}, "players": {"1": {"hand": 1}, "2": {"hand": 1}, "3": {"hand": 1}}}
    }
  },
  {
    "name": "A seat holding the led suit must follow it; a seat without the led suit may play any card",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["AS", "KD"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "2": {"hand": ["QS", "AH"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "3": {"hand": ["KH", "JC"], "bid": 1, "tricks_taken": 0, "hand_score": 0}
      },
      "game": {"round": 5, "trick_in_hand": 5, "hand_number": 1, "leader": 1, "dealer": 1, "trump_suit": "D", "turned_card": "10D", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "AS"},
      {"seat": 2, "options_include": "QS"},
      {"seat": 3, "options_include": "JC"}
    ],
    "expect": {
      "game": {"trick_winner": 1},
      "players": {"1": {"tricks_taken": 1}, "2": {"tricks_taken": 0}, "3": {"tricks_taken": 0}},
      "offered": [{"seat": 2, "option": "QS"}, {"seat": 3, "option": "KH"}, {"seat": 3, "option": "JC"}],
      "not_offered": [{"seat": 2, "option": "AH"}]
    }
  },
  {
    "name": "A low trump beats the led Ace, and the trick winner leads the next trick",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "rounds": 2,
    "given": {
      "players": {
        "1": {"hand": ["AS", "QD"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "2": {"hand": ["10H", "KC"], "bid": 1, "tricks_taken": 0, "hand_score": 0},
        "3": {"hand": ["KS", "JD"], "bid": 1, "tricks_taken": 0, "hand_score": 0}
      },
      "game": {"round": 2, "trick_in_hand": 2, "hand_number": 1, "leader": 1, "dealer": 1, "trump_suit": "H", "turned_card": "JH", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "AS"},
      {"seat": 2, "options_include": "10H"},
      {"seat": 3, "options_include": "KS"}
    ],
    "expect": {
      "game": {"trick_winner": 2},
      "players": {"1": {"tricks_taken": 0}, "2": {"tricks_taken": 2}, "3": {"tricks_taken": 0}}
    }
  },
  {
    "name": "A trick holding JD and JH scores 2-3-4 = -5 for its winner, shown in the end-of-hand total",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["AD"], "bid": 0, "tricks_taken": 2, "hand_score": 4, "total": 10},
        "2": {"hand": ["JD"], "bid": 4, "tricks_taken": 2, "hand_score": 0, "total": 0},
        "3": {"hand": ["JH"], "bid": 4, "tricks_taken": 1, "hand_score": 2, "total": 3}
      },
      "game": {"round": 6, "trick_in_hand": 6, "hand_number": 1, "leader": 1, "dealer": 1, "trump_suit": "S", "turned_card": "10S", "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "AD"},
      {"seat": 2, "options_include": "JD"},
      {"seat": 3, "options_include": "JH"}
    ],
    "expect": {
      "game": {"trick_winner": 1},
      "players": {"1": {"tricks_taken": 3, "total": 9}, "2": {"total": 0}, "3": {"total": 5}}
    }
  },
  {
    "name": "At the end of the hand an exact bid earns 5 and every hand_score is added to the total",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["10H"], "bid": 2, "tricks_taken": 3, "hand_score": 6, "total": 4},
        "2": {"hand": ["KH"], "bid": 3, "tricks_taken": 2, "hand_score": 1, "total": 5},
        "3": {"hand": ["QH"], "bid": 1, "tricks_taken": 1, "hand_score": 2, "total": 0}
      },
      "game": {"round": 12, "trick_in_hand": 6, "hand_number": 2, "leader": 2, "dealer": 2, "trump_suit": "C", "turned_card": "10C", "deck": []}
    },
    "rules": [
      {"seat": 2, "options_include": "KH"},
      {"seat": 3, "options_include": "QH"},
      {"seat": 1, "options_include": "10H"}
    ],
    "expect": {
      "game": {"trick_winner": 2, "hand_number": 3},
      "players": {"1": {"total": 10}, "2": {"tricks_taken": 3, "total": 13}, "3": {"total": 7}}
    }
  },
  {
    "name": "Seats level on the highest final total share the win",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": ["KS"], "bid": 0, "tricks_taken": 0, "hand_score": 0, "total": 25},
        "2": {"hand": ["QS"], "bid": 2, "tricks_taken": 3, "hand_score": 6, "total": 10},
        "3": {"hand": ["AS"], "bid": 4, "tricks_taken": 3, "hand_score": 3, "total": 20}
      },
      "game": {"round": 36, "trick_in_hand": 6, "hand_number": 6, "leader": 3, "dealer": 3, "trump_suit": "D", "turned_card": "10D", "deck": []}
    },
    "rules": [
      {"seat": 3, "options_include": "AS"},
      {"seat": 1, "options_include": "KS"},
      {"seat": 2, "options_include": "QS"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 30, "2": 16, "3": 30},
      "players": {"1": {"total": 30}, "2": {"total": 16}, "3": {"total": 30}}
    }
  }
]
```
````
