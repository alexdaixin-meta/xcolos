# 13 scenarios

- time: 2026-10-28T03:14:18+00:00 (159.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 cf5a350017a0ce1c, reply sha256 f8d4a6412796de08

## Sent

````
SPEC:
{
  "name": "Da Bai Fen Duplicate",
  "summary": "Four players in two fixed partnerships play 4 hands of 6 trick-taking rounds with a 26-card deck. Hands 3 and 4 replay the deals of hands 1 and 2, rotated one seat, and the team that captures more card points wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 26,
    "cards_per_seat": 6,
    "kitty_size": 2,
    "hands": 4,
    "tricks_per_hand": 6,
    "total_rounds": 24,
    "points_five": 5,
    "points_ten": 10,
    "points_king": 10,
    "points_other": 0,
    "points_per_suit": 25,
    "points_in_deck": 100,
    "kitty_multiplier": 2,
    "first_leader_hand_1": 1,
    "first_leader_hand_2": 2,
    "first_leader_hand_3": 2,
    "first_leader_hand_4": 3,
    "rank_big_joker": 8,
    "rank_small_joker": 7,
    "rank_ace": 6,
    "rank_king": 5,
    "rank_queen": 4,
    "rank_jack": 3,
    "rank_ten": 2,
    "rank_five": 1,
    "trump_strength_base": 200,
    "led_suit_strength_base": 100
  },
  "attributes": {
    "player": [
      {
        "key": "team",
        "type": "text",
        "visible": "public",
        "initial": "A for seats 1 and 3, B for seats 2 and 4",
        "meaning": "The seat's partnership.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards the seat currently holds. Each card is a code: suit letter S, H, C or D plus rank A, K, Q, 10, J or 5, or JOKER_BIG or JOKER_SMALL.",
        "observable": false
      },
      {
        "key": "hand1_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 6 cards this seat was dealt in hand 1, kept for the replay in hand 3.",
        "observable": false
      },
      {
        "key": "hand2_cards",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The 6 cards this seat was dealt in hand 2, kept for the replay in hand 4.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card this seat played to the current trick.",
        "observable": false
      },
      {
        "key": "card_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Strength of the played card in this trick: 200 + rank if it is a trump, 100 + rank if it is of the led non-trump suit, otherwise 0.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The match total of this seat's team, mirrored onto both partners.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 26 cards",
        "meaning": "Undealt cards for a fresh shuffle.",
        "observable": false
      },
      {
        "key": "kitty",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 2 face-down cards of the current hand.",
        "observable": false
      },
      {
        "key": "kitty_hand1",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The kitty of hand 1, kept for hand 3.",
        "observable": false
      },
      {
        "key": "kitty_hand2",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The kitty of hand 2, kept for hand 4.",
        "observable": false
      },
      {
        "key": "kitty_revealed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The kitty, shown after the 6th trick of a hand.",
        "observable": true
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current hand, from 1 to 4.",
        "observable": true
      },
      {
        "key": "trick_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current trick within the hand, from 1 to 6.",
        "observable": true
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "S",
        "meaning": "The trump suit: S in hands 1 and 3, H in hands 2 and 4.",
        "observable": true
      },
      {
        "key": "is_replay",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True in hands 3 and 4.",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "led_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The first card played to the current trick.",
        "observable": false
      },
      {
        "key": "led_is_trump",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the led card is a joker or a trump-suit card.",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The suit of the led card. TRUMP if the led card is trump.",
        "observable": false
      },
      {
        "key": "trick_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards played to the current trick, in order.",
        "observable": false
      },
      {
        "key": "played_this_hand",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "All cards played so far in the current hand.",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that won the last trick.",
        "observable": true
      },
      {
        "key": "trick_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The point value of the 4 cards in the last trick.",
        "observable": false
      },
      {
        "key": "team_a_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match total of Team A (seats 1 and 3).",
        "observable": true
      },
      {
        "key": "team_b_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match total of Team B (seats 2 and 4).",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats 1 and 3 are given team A, and seats 2 and 4 are given team B.",
    "The table deck is filled with the 26 cards: JOKER_BIG, JOKER_SMALL, and A, K, Q, J, 10, 5 of each of S, H, C, D.",
    "hand_number = 1, trick_number = 1, trump_suit = S, leader = 1, and team_a_total = team_b_total = 0. Every score is 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when trick_number == 1. Clears played_this_hand and kitty_revealed. If hand_number is 1 or 2, the deck is refilled with all 26 cards; each seat then draws 6 cards at random from the deck into its hand, and the 2 cards left move to the kitty. When hand_number == 1, each hand is copied to hand1_cards and the kitty to kitty_hand1. When hand_number == 2, each hand is copied to hand2_cards and the kitty to kitty_hand2. If hand_number == 3, each seat s gets hand = hand1_cards of seat s-1 (seat 1 gets seat 4's), and kitty = kitty_hand1. If hand_number == 4, each seat s gets hand = hand2_cards of seat s-1, and kitty = kitty_hand2. trump_suit is S if hand_number is 1 or 3, otherwise H. leader is 1, 2, 2 or 3 for hands 1 to 4. is_replay = (hand_number >= 3)."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when trick_number == 1. Announces 'Hand {hand_number} begins. Trump is {trump_suit}. Seat {leader} leads.' When is_replay is true, it adds 'This hand is a replay: each seat holds the cards the previous seat held in hand {hand_number - 2}.'"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each seat is sent its own hand, plus played_this_hand, team_a_total, team_b_total, trump_suit, trick_number and hand_number."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting with the seat in leader and going anticlockwise (leader, leader+1, ... wrapping 4 to 1)",
      "answer": "One card from the seat's own hand, chosen from the legal options only (see offers).",
      "effect": "The card is removed from the player's hand and appended to trick_cards and played_this_hand, and played_card is set. For the first player, led_card is set to the card. led_is_trump = (the card is a joker or of trump_suit). led_suit = TRUMP if led_is_trump, otherwise the card's suit."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Each seat gets card_strength = 200 + rank if played_card is a joker or of trump_suit; otherwise 100 + rank if led_is_trump is false and played_card's suit == led_suit; otherwise 0. Ranks are Big Joker 8, Small Joker 7, A 6, K 5, Q 4, J 3, 10 2, 5 1. trick_winner = the seat with the highest card_strength. trick_points = the sum of the points of the 4 trick_cards, where 5 = 5, 10 = 10, K = 10 and all others = 0. If trick_winner is 1 or 3, team_a_total += trick_points; otherwise team_b_total += trick_points. Seats 1 and 3 get score = team_a_total, and seats 2 and 4 get score = team_b_total. leader = trick_winner."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announces 'Trick {trick_number} of hand {hand_number}: cards {trick_cards}. Seat {trick_winner} wins {trick_points} points. Team A {team_a_total}, Team B {team_b_total}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when trick_number == 6. kitty_revealed = kitty. If trick_winner is 1 or 3, team_a_total += 2 * (points of kitty); otherwise team_b_total += 2 * (points of kitty). Both teams' scores are mirrored to the seats again."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Runs only when trick_number == 6. Announces 'End of hand {hand_number}. Kitty: {kitty_revealed}, doubled for the team of seat {trick_winner}. Team A {team_a_total}, Team B {team_b_total}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_cards is cleared, led_card is set to empty, and each played_card is set to empty. trick_number += 1. If trick_number > 6, then trick_number = 1 and hand_number += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "The game ends if hand_number > 4. Otherwise it continues with the next round."
    }
  ],
  "ending": {
    "condition": "hand_number > 4 (after 24 tricks)",
    "rank_by": "you.score",
    "decided_by": "Each seat's standing is its team's match total: captured card points plus doubled kitty points. Both partners of the team with the higher total win. If the totals are equal, all four seats tie at the top, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Team A is seats 1 and 3, and Team B is seats 2 and 4. Play goes 1, 2, 3, 4, 1."
    },
    {
      "id": "R2",
      "text": "The deck has 26 cards: Big Joker, Small Joker, and A, K, Q, J, 10, 5 of Spades, Hearts, Clubs and Diamonds."
    },
    {
      "id": "R3",
      "text": "A 5 is worth 5 points, a 10 is worth 10, a K is worth 10, and every other card is worth 0, so the deck holds 100 points."
    },
    {
      "id": "R4",
      "text": "In hands 1 and 3 the trump suit is Spades, and in hands 2 and 4 it is Hearts."
    },
    {
      "id": "R5",
      "text": "Trumps rank from high to low as Big Joker, Small Joker, A, K, Q, J, 10, 5 of the trump suit, and both jokers count as trump for following."
    },
    {
      "id": "R6",
      "text": "In a non-trump suit the cards rank A, K, Q, J, 10, 5."
    },
    {
      "id": "R7",
      "text": "At the start of hands 1 and 2, the 26 cards are shuffled, each seat gets 6 private cards, and the remaining 2 cards form a hidden kitty."
    },
    {
      "id": "R8",
      "text": "In hand 3, seat s holds exactly the 6 cards seat s-1 held in hand 1 (seat 1 gets seat 4's), and the kitty equals hand 1's kitty."
    },
    {
      "id": "R9",
      "text": "In hand 4, seat s holds exactly the 6 cards seat s-1 held in hand 2 (seat 1 gets seat 4's), and the kitty equals hand 2's kitty."
    },
    {
      "id": "R10",
      "text": "Players are told at the start of hands 3 and 4 that the hand is a replay."
    },
    {
      "id": "R11",
      "text": "The first leader is seat 1 in hand 1, seat 2 in hand 2, seat 2 in hand 3 and seat 3 in hand 4."
    },
    {
      "id": "R12",
      "text": "The leader may play any card in their hand."
    },
    {
      "id": "R13",
      "text": "When the led card is a trump, a player holding a trump is offered only their trumps."
    },
    {
      "id": "R14",
      "text": "When the led card is a non-trump suit, a player holding that suit is offered only cards of that suit."
    },
    {
      "id": "R15",
      "text": "A player with no card of the required suit is offered every card in their hand."
    },
    {
      "id": "R16",
      "text": "When any trump is played to a trick, the highest trump wins the trick."
    },
    {
      "id": "R17",
      "text": "When no trump is played, the highest card of the led suit wins, and off-suit non-trump cards never win."
    },
    {
      "id": "R18",
      "text": "After each trick, the winner's team adds the point value of the 4 cards to its match total."
    },
    {
      "id": "R19",
      "text": "The winner of a trick leads the next trick of the same hand."
    },
    {
      "id": "R20",
      "text": "After the 6th trick of a hand, the kitty is revealed and 2 times its point value is added to the team that won the 6th trick."
    },
    {
      "id": "R21",
      "text": "Other players' hands and the kitty stay hidden until the kitty is revealed at the end of the hand."
    },
    {
      "id": "R22",
      "text": "The match ends after hand 4 (24 tricks), and the team with the higher match total wins."
    },
    {
      "id": "R23",
      "text": "When the two match totals are equal, the match is a draw."
    },
    {
      "id": "R24",
      "text": "There is no table talk."
    }
  ],
  "offers": [
    {
      "question": "Play a card to the trick",
      "who": "the leader (first to play)",
      "options": "Every card in the leader's hand."
    },
    {
      "question": "Play a card to the trick",
      "who": "a following seat, when led_is_trump is true",
      "options": "If the seat holds any joker or trump_suit card, only those cards. Otherwise every card in its hand."
    },
    {
      "question": "Play a card to the trick",
      "who": "a following seat, when led_is_trump is false",
      "options": "If the seat holds any card of led_suit, counting only non-joker cards when led_suit is not the trump suit, only those cards. Otherwise every card in its hand."
    }
  ],
  "choices": [
    {
      "what": "4 players, suggested 4",
      "why": "The designer fixed two partnerships of two. The duplicate replay structure depends on exactly 4 seats rotating, so neither fewer nor more seats work."
    },
    {
      "what": "No talk step",
      "why": "The source forbids table talk. Partnership play here rests on inferring a partner's cards from what they play."
    },
    {
      "what": "Rank numbers 1 to 8 and strength bases of 100 (led suit) and 200 (trump)",
      "why": "These let the trick winner be found by arithmetic as the seat with the highest card_strength."
    },
    {
      "what": "The play order starts at the leader",
      "why": "The source says the leader plays first and the others follow anticlockwise. The ask step runs from the seat in leader."
    },
    {
      "what": "Saved hand1_cards and hand2_cards are visible to their owner (ally)",
      "why": "A player attribute cannot be hidden from its owner, and the owner already saw those cards when they were dealt."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player counts the trumps and points already played, keeps high trumps to capture the 6th trick (worth the doubled kitty), and feeds point cards to tricks the partner is winning."
    }
  ],
  "simplifications": [
    {
      "what": "Each team's match total is mirrored onto both partners as score",
      "why": "The ranking is a per-player expression, so both partners carry their team's total."
    },
    {
      "what": "A draw is represented as all four seats sharing the top rank",
      "why": "The engine has no separate draw outcome. Tied totals give every seat the same rank_by value."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: team, score; table: kitty_revealed, hand_number, trick_number, trump_suit, trick_winner, team_a_total, team_b_total.
````

## Reply

````
```json
[
  {
    "name": "Seats 1 and 3 are team A, seats 2 and 4 are team B; scores start at 0",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "default": "first",
    "rules": [],
    "expect": {
      "players": {
        "1": {"team": "A", "score": 0},
        "2": {"team": "B", "score": 0},
        "3": {"team": "A", "score": 0},
        "4": {"team": "B", "score": 0}
      },
      "game": {"team_a_total": 0, "team_b_total": 0, "hand_number": 1, "trick_number": 1}
    }
  },
  {
    "name": "The deck holds 26 cards before the first deal",
    "rule": "R2",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {
        "game": {"deck": 26, "kitty": 0},
        "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}
      }
    }
  },
  {
    "name": "5, 10 and K are worth 5, 10 and 10, A is worth 0: a trick of C5 C10 CK CA gives team B 25",
    "rule": "R3",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["C5"]},
        "2": {"hand": ["C10"]},
        "3": {"hand": ["CK"]},
        "4": {"hand": ["CA"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 4, "team_a_total": 0, "team_b_total": 25},
      "players": {"1": {"score": 0}, "2": {"score": 25}, "3": {"score": 0}, "4": {"score": 25}}
    }
  },
  {
    "name": "Hand 2 has Hearts as trump (deal is random, only the trump suit is asserted)",
    "rule": "R4",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "given": {"game": {"hand_number": 2, "trick_number": 1, "trump_suit": "S"}},
    "rules": [],
    "expect": {
      "game": {"trump_suit": "H", "hand_number": 2, "trick_number": 2},
      "lens": {
        "players": {
          "1": {"hand": 5, "hand2_cards": 6},
          "2": {"hand": 5, "hand2_cards": 6},
          "3": {"hand": 5, "hand2_cards": 6},
          "4": {"hand": 5, "hand2_cards": 6}
        }
      }
    }
  },
  {
    "name": "Hand 1 starts with Spades as trump",
    "rule": "R4",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "default": "first",
    "rules": [],
    "expect": {"game": {"trump_suit": "S"}}
  },
  {
    "name": "Big Joker beats Small Joker beats trump Ace; jokers must follow a trump lead",
    "rule": "R5",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["S5"]},
        "2": {"hand": ["JOKER_SMALL", "C5"]},
        "3": {"hand": ["JOKER_BIG", "D10"]},
        "4": {"hand": ["SA", "HK"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 5, "team_b_total": 0},
      "players": {"1": {"score": 5}, "3": {"score": 5}, "2": {"score": 0}, "4": {"score": 0}},
      "not_offered": [
        {"seat": 2, "option": "C5"},
        {"seat": 3, "option": "D10"},
        {"seat": 4, "option": "HK"}
      ]
    }
  },
  {
    "name": "In a non-trump suit K beats Q, J and 10",
    "rule": "R6",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DQ"]},
        "2": {"hand": ["DJ"]},
        "3": {"hand": ["DK"]},
        "4": {"hand": ["D10"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 20, "team_b_total": 0},
      "players": {"1": {"score": 20}, "3": {"score": 20}}
    }
  },
  {
    "name": "Hand 1 deal: 6 cards each, 2 in the kitty, deck emptied (random cards, only counts asserted)",
    "rule": "R7",
    "players": 4,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "game": {"hand_number": 1, "trick_number": 2},
      "lens": {
        "game": {"deck": 0, "kitty": 2, "kitty_hand1": 2},
        "players": {
          "1": {"hand": 5, "hand1_cards": 6},
          "2": {"hand": 5, "hand1_cards": 6},
          "3": {"hand": 5, "hand1_cards": 6},
          "4": {"hand": 5, "hand1_cards": 6}
        }
      }
    }
  },
  {
    "name": "Hand 3 gives each seat the hand-1 cards of the previous seat",
    "rule": "R8",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand1_cards": ["SA", "SK", "SQ", "SJ", "S10", "S5"]},
        "2": {"hand1_cards": ["HA", "HK", "HQ", "HJ", "H10", "H5"]},
        "3": {"hand1_cards": ["CA", "CK", "CQ", "CJ", "C10", "C5"]},
        "4": {"hand1_cards": ["DA", "DK", "DQ", "DJ", "D10", "D5"]}
      },
      "game": {"hand_number": 3, "trick_number": 1, "trump_suit": "H", "kitty_hand1": ["JOKER_BIG", "JOKER_SMALL"]}
    },
    "rules": [
      {"seat": 2, "options_include": "SA"},
      {"seat": 3, "options_include": "HA"},
      {"seat": 4, "options_include": "CA"},
      {"seat": 1, "options_include": "DA"}
    ],
    "expect": {
      "game": {"trick_winner": 2, "trump_suit": "S", "team_a_total": 0, "team_b_total": 0},
      "lens": {
        "game": {"kitty": 2},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      },
      "offered": [
        {"seat": 2, "option": "SK"},
        {"seat": 3, "option": "H5"},
        {"seat": 4, "option": "C5"},
        {"seat": 1, "option": "D5"}
      ],
      "not_offered": [{"seat": 2, "option": "DA"}]
    }
  },
  {
    "name": "Hand 4 gives each seat the hand-2 cards of the previous seat",
    "rule": "R9",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand2_cards": ["SA", "SK", "SQ", "SJ", "S10", "S5"]},
        "2": {"hand2_cards": ["HA", "HK", "HQ", "HJ", "H10", "H5"]},
        "3": {"hand2_cards": ["CA", "CK", "CQ", "CJ", "C10", "C5"]},
        "4": {"hand2_cards": ["DA", "DK", "DQ", "DJ", "D10", "D5"]}
      },
      "game": {"hand_number": 4, "trick_number": 1, "trump_suit": "S", "kitty_hand2": ["JOKER_BIG", "JOKER_SMALL"]}
    },
    "rules": [
      {"seat": 3, "options_include": "HA"},
      {"seat": 4, "options_include": "CA"},
      {"seat": 1, "options_include": "DA"},
      {"seat": 2, "options_include": "SA"}
    ],
    "expect": {
      "game": {"trick_winner": 3, "trump_suit": "H", "team_a_total": 0, "team_b_total": 0},
      "lens": {
        "game": {"kitty": 2},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      },
      "offered": [
        {"seat": 3, "option": "H5"},
        {"seat": 4, "option": "C5"},
        {"seat": 1, "option": "D5"},
        {"seat": 2, "option": "S5"}
      ]
    }
  },
  {
    "name": "Hand 3 is played as a replay of hand 1's cards",
    "rule": "R10",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand1_cards": ["SA", "SK", "SQ", "SJ", "S10", "S5"]},
        "2": {"hand1_cards": ["HA", "HK", "HQ", "HJ", "H10", "H5"]},
        "3": {"hand1_cards": ["CA", "CK", "CQ", "CJ", "C10", "C5"]},
        "4": {"hand1_cards": ["DA", "DK", "DQ", "DJ", "D10", "D5"]}
      },
      "game": {"hand_number": 3, "trick_number": 1, "kitty_hand1": ["JOKER_BIG", "JOKER_SMALL"]}
    },
    "rules": [],
    "expect": {
      "game": {"hand_number": 3, "trick_number": 2, "trump_suit": "S"},
      "offered": [{"seat": 2, "option": "SA"}]
    }
  },
  {
    "name": "Seat 2 leads the first trick of hand 3 (only seat 2 holds clubs and no trump is out)",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand1_cards": ["CA", "CK", "C5"]},
        "2": {"hand1_cards": ["DA", "DK", "D5"]},
        "3": {"hand1_cards": ["HA", "HK", "H5"]},
        "4": {"hand1_cards": ["DQ", "DJ", "HQ"]}
      },
      "game": {"hand_number": 3, "trick_number": 1, "kitty_hand1": ["SA", "S5"]}
    },
    "rules": [{"seat": 2, "options_include": "CA"}],
    "expect": {"game": {"trick_winner": 2, "trump_suit": "S"}}
  },
  {
    "name": "Seat 3 leads the first trick of hand 4 (only seat 3 holds clubs and no trump is out)",
    "rule": "R11",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand2_cards": ["DQ", "DJ", "SQ"]},
        "2": {"hand2_cards": ["CA", "CK", "C5"]},
        "3": {"hand2_cards": ["DA", "DK", "D5"]},
        "4": {"hand2_cards": ["SA", "SK", "S5"]}
      },
      "game": {"hand_number": 4, "trick_number": 1, "kitty_hand2": ["HA", "H5"]}
    },
    "rules": [{"seat": 3, "options_include": "CA"}],
    "expect": {"game": {"trick_winner": 3, "trump_suit": "H"}}
  },
  {
    "name": "The leader is offered every card in hand",
    "rule": "R12",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["C5", "SA", "JOKER_BIG", "HK"]},
        "2": {"hand": ["C10"]},
        "3": {"hand": ["CQ"]},
        "4": {"hand": ["D5"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [{"seat": 1, "options_include": "C5"}],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 20, "team_b_total": 0},
      "players": {"1": {"score": 20}, "3": {"score": 20}},
      "offered": [
        {"seat": 1, "option": "SA"},
        {"seat": 1, "option": "JOKER_BIG"},
        {"seat": 1, "option": "HK"}
      ]
    }
  },
  {
    "name": "On a trump lead, a seat holding trumps is offered only trumps",
    "rule": "R13",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["SK"]},
        "2": {"hand": ["S10", "HA", "CA"]},
        "3": {"hand": ["JOKER_SMALL", "DK"]},
        "4": {"hand": ["H5"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 25, "team_b_total": 0},
      "players": {"1": {"score": 25}, "3": {"score": 25}},
      "not_offered": [
        {"seat": 2, "option": "HA"},
        {"seat": 2, "option": "CA"},
        {"seat": 3, "option": "DK"}
      ]
    }
  },
  {
    "name": "On a non-trump lead, a seat holding that suit is offered only that suit",
    "rule": "R14",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["HQ"]},
        "2": {"hand": ["H5", "SA", "DA"]},
        "3": {"hand": ["HA", "HK"]},
        "4": {"hand": ["CK"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [{"seat": 3, "options_include": "HK"}],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 25, "team_b_total": 0},
      "players": {"1": {"score": 25}, "3": {"score": 25}},
      "offered": [{"seat": 3, "option": "HA"}],
      "not_offered": [
        {"seat": 2, "option": "SA"},
        {"seat": 2, "option": "DA"}
      ]
    }
  },
  {
    "name": "A seat void in the led suit is offered every card",
    "rule": "R15",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["CA"]},
        "2": {"hand": ["H5", "D10"]},
        "3": {"hand": ["C5"]},
        "4": {"hand": ["SK", "HA"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [
      {"seat": 2, "options_include": "D10"},
      {"seat": 4, "options_include": "HA"}
    ],
    "expect": {
      "game": {"trick_winner": 1, "team_a_total": 15, "team_b_total": 0},
      "players": {"1": {"score": 15}, "3": {"score": 15}},
      "offered": [
        {"seat": 2, "option": "H5"},
        {"seat": 4, "option": "SK"}
      ]
    }
  },
  {
    "name": "The highest trump wins over the led suit's Ace",
    "rule": "R16",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DA"]},
        "2": {"hand": ["S5"]},
        "3": {"hand": ["DK"]},
        "4": {"hand": ["SJ"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 4, "team_a_total": 0, "team_b_total": 15},
      "players": {"2": {"score": 15}, "4": {"score": 15}}
    }
  },
  {
    "name": "With no trump played, off-suit Aces lose to the led suit's 10",
    "rule": "R17",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["C10"]},
        "2": {"hand": ["HA"]},
        "3": {"hand": ["DA"]},
        "4": {"hand": ["C5"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 1, "team_a_total": 15, "team_b_total": 0},
      "players": {"1": {"score": 15}, "3": {"score": 15}}
    }
  },
  {
    "name": "Trick points add to the winning team's existing total",
    "rule": "R18",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["SK"], "score": 30},
        "2": {"hand": ["S5"], "score": 15},
        "3": {"hand": ["SA"], "score": 30},
        "4": {"hand": ["S10"], "score": 15}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1, "team_a_total": 30, "team_b_total": 15}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 55, "team_b_total": 15},
      "players": {"1": {"score": 55}, "2": {"score": 15}, "3": {"score": 55}, "4": {"score": 15}}
    }
  },
  {
    "name": "Seat 4 wins a trick and leads the next one with its lone heart",
    "rule": "R19",
    "players": 4,
    "seed": 1,
    "rounds": 2,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DK", "C5"]},
        "2": {"hand": ["D5", "CK"]},
        "3": {"hand": ["D10", "CA"]},
        "4": {"hand": ["DA", "H5"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [{"seat": 1, "options_include": "DK"}],
    "expect": {
      "game": {"trick_winner": 4, "team_a_total": 0, "team_b_total": 45},
      "players": {"2": {"score": 45}, "4": {"score": 45}}
    }
  },
  {
    "name": "After trick 6 the kitty is revealed and doubled for the trick winner's team",
    "rule": "R20",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["C5"]},
        "2": {"hand": ["CA"]},
        "3": {"hand": ["C10"]},
        "4": {"hand": ["CQ"]}
      },
      "game": {"hand_number": 1, "trick_number": 6, "trump_suit": "S", "leader": 1, "kitty": ["SK", "D5"]}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 2, "team_a_total": 0, "team_b_total": 45, "kitty_revealed": ["SK", "D5"], "hand_number": 2, "trick_number": 1},
      "players": {"1": {"score": 0}, "2": {"score": 45}, "3": {"score": 0}, "4": {"score": 45}}
    }
  },
  {
    "name": "The kitty is not revealed before the end of the hand",
    "rule": "R21",
    "players": 4,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {"lens": {"game": {"kitty_revealed": 0, "kitty": 2}}}
  },
  {
    "name": "Match ends after hand 4; team A with the higher total wins",
    "rule": "R22",
    "players": 4,
    "seed": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DA"], "score": 40},
        "2": {"hand": ["D5"], "score": 30},
        "3": {"hand": ["DQ"], "score": 40},
        "4": {"hand": ["DJ"], "score": 30}
      },
      "game": {"hand_number": 4, "trick_number": 6, "trump_suit": "H", "leader": 1, "kitty": ["DK", "C10"], "team_a_total": 40, "team_b_total": 30}
    },
    "rules": [],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 85, "2": 30, "3": 85, "4": 30},
      "game": {"team_a_total": 85, "team_b_total": 30}
    }
  },
  {
    "name": "Equal match totals: all four seats share the win",
    "rule": "R23",
    "players": 4,
    "seed": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DQ"], "score": 60},
        "2": {"hand": ["DA"], "score": 40},
        "3": {"hand": ["DJ"], "score": 60},
        "4": {"hand": ["CA"], "score": 40}
      },
      "game": {"hand_number": 4, "trick_number": 6, "trump_suit": "H", "leader": 1, "kitty": ["C10", "SQ"], "team_a_total": 60, "team_b_total": 40}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2, 3, 4],
      "standings": {"1": 60, "2": 60, "3": 60, "4": 60},
      "game": {"team_a_total": 60, "team_b_total": 60}
    }
  },
  {
    "name": "A trick plays through with no talk step and scores still at 0 for a pointless trick",
    "rule": "R24",
    "players": 4,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["DQ"]},
        "2": {"hand": ["DJ"]},
        "3": {"hand": ["DA"]},
        "4": {"hand": ["CQ"]}
      },
      "game": {"hand_number": 1, "trick_number": 2, "trump_suit": "S", "leader": 1}
    },
    "rules": [],
    "expect": {
      "game": {"trick_winner": 3, "team_a_total": 0, "team_b_total": 0},
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}}
    }
  }
]
```
````
