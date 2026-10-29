# 04 scenarios

- time: 2026-10-28T03:00:24+00:00 (122.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e762d12c1031b673, reply sha256 c1279936679feeb4

## Sent

````
SPEC:
{
  "name": "Da Bai Fen Lite",
  "summary": "A four-player partnership trick-taking game (NS v EW) over 4 hands of 7 tricks with a 30-card deck and jokers. Teams win match points by how many card points the defenders capture.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "seats": 4,
    "deck_size": 30,
    "suits": 4,
    "cards_per_suit": 7,
    "jokers": 2,
    "rank_5": 1,
    "rank_8": 2,
    "rank_10": 3,
    "rank_j": 4,
    "rank_q": 5,
    "rank_k": 6,
    "rank_a": 7,
    "points_k": 10,
    "points_10": 10,
    "points_5": 5,
    "points_other": 0,
    "total_points": 100,
    "hands": 4,
    "rounds_per_hand": 8,
    "total_rounds": 32,
    "tricks_per_hand": 7,
    "cards_dealt_each": 7,
    "kitty_size": 2,
    "trump_count": 9,
    "big_joker_strength": 40,
    "small_joker_strength": 39,
    "trump_base": 20,
    "led_suit_base": 10,
    "off_suit_base": 0,
    "band_declarer_3_max": 15,
    "band_declarer_2_min": 20,
    "band_declarer_2_max": 35,
    "band_defender_1_min": 40,
    "band_defender_1_max": 55,
    "band_defender_2_min": 60,
    "band_defender_2_max": 75,
    "band_defender_3_min": 80,
    "award_3": 3,
    "award_2": 2,
    "award_1": 1,
    "rank_weight_match_points": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "team",
        "type": "text",
        "visible": "public",
        "initial": "NS for seats 1 and 3, EW for seats 2 and 4",
        "meaning": "the player's team",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "the cards the player holds, as codes such as 'S-K', 'H-10', 'BJ' (Big Joker), 'SJ' (Small Joker)",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the card the player played to the current trick, face up",
        "observable": false
      },
      {
        "key": "card_strength",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the strength of played_card in the current trick",
        "observable": false
      },
      {
        "key": "match_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the team's match points, mirrored on both partners",
        "observable": true
      },
      {
        "key": "card_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the team's running card-point total over completed hands, mirrored on both partners",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "all 30 cards",
        "meaning": "the undealt cards: 4 suits x {5,8,10,J,Q,K,A} plus BJ and SJ",
        "observable": false
      },
      {
        "key": "kitty",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 2 face-down cards left after the deal",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the current hand, 1 to 4",
        "observable": true
      },
      {
        "key": "round_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the round within the hand, 1 to 8 (1 = deal and trumps, 2 to 8 = tricks)",
        "observable": false
      },
      {
        "key": "declarer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the declarer's seat, equal to hand_number",
        "observable": true
      },
      {
        "key": "declaring_team",
        "type": "text",
        "visible": "public",
        "initial": "NS",
        "meaning": "the declarer's team: NS when declarer is 1 or 3, EW when declarer is 2 or 4",
        "observable": false
      },
      {
        "key": "trump_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the trump suit named by the declarer",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the seat that leads the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the suit of the led card, or 'Trump' if the led card is a trump",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat whose card has the highest card_strength in the trick",
        "observable": false
      },
      {
        "key": "trick_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the sum of point values of the 4 cards in the trick",
        "observable": false
      },
      {
        "key": "ns_hand_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "card points NS has won this hand",
        "observable": true
      },
      {
        "key": "ew_hand_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "card points EW has won this hand",
        "observable": true
      },
      {
        "key": "defender_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "P, the Defending Team's hand points at the end of the hand",
        "observable": false
      },
      {
        "key": "ns_match_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "NS match points",
        "observable": true
      },
      {
        "key": "ew_match_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "EW match points",
        "observable": true
      },
      {
        "key": "ns_card_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "NS running card-point total",
        "observable": true
      },
      {
        "key": "ew_card_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "EW running card-point total",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seats 1 and 3 get team NS; seats 2 and 4 get team EW.",
    "All match_points, card_points and team totals start at 0.",
    "Set hand_number = 1, round_in_hand = 1, declarer = 1, declaring_team = NS."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand == 1: deck is reset to all 30 cards; every hand, kitty and trump_suit are cleared; ns_hand_points = ew_hand_points = 0; declarer = hand_number; declaring_team = NS if declarer is odd, else EW; leader = declarer"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand == 1: draw 7 random cards from deck into each player's hand (removed from deck), then move the 2 remaining cards of deck into kitty"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand == 1: each player sees their own hand only"
    },
    {
      "action": "ask",
      "who": "the declarer (seat = declarer)",
      "answer": "one of: Spades, Hearts, Clubs, Diamonds",
      "effect": "when round_in_hand == 1: trump_suit = the answer; announce to all 'Trump suit is {trump_suit}; seat {declarer} leads.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand >= 2: every played_card = '' and card_strength = 0; led_suit = ''"
    },
    {
      "action": "ask",
      "who": "each player in turn, starting from seat = leader and going anticlockwise (leader, leader+1, leader+2, leader+3, wrapping 4 to 1)",
      "answer": "one card from own hand: the leader may choose any card; a follower must choose a card of led_suit if holding one (jokers and trump_suit cards count as suit 'Trump'), otherwise any card",
      "effect": "when round_in_hand >= 2: the card moves from hand to played_card, face up to all; if the player is the leader, led_suit = 'Trump' when the card is a joker or of trump_suit, else the card's suit; card_strength = 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump card of led_suit, otherwise rank (5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7)",
      "judged": "The card this player chose is legal: either the player is the leader, or the card is of the led suit (jokers and trump-suit cards counting as Trump), or the player held no card of the led suit."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand >= 2: trick_winner = the seat with the highest card_strength; trick_points = sum over the 4 played cards of (10 for K, 10 for 10, 5 for 5, 0 otherwise); if trick_winner's team is NS then ns_hand_points += trick_points, else ew_hand_points += trick_points; leader = trick_winner; announce 'Seat {trick_winner} wins the trick for {trick_points} points.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand == 8: reveal kitty to all; add the kitty's point values to the hand points of trick_winner's team"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round_in_hand == 8: defender_points = ew_hand_points if declaring_team is NS, else ns_hand_points; if defender_points <= 15, the declaring team's match points += 3; if 20..35, the declaring team += 2; if 40..55, the defending team += 1; if 60..75, the defending team += 2; if >= 80, the defending team += 3; ns_card_points += ns_hand_points; ew_card_points += ew_hand_points; copy the team match points and card points onto each player's match_points and card_points; announce the hand result"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if round_in_hand == 8 then hand_number += 1 and round_in_hand = 1, else round_in_hand += 1"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game when hand_number > 4; otherwise continue"
    }
  ],
  "ending": {
    "condition": "hand_number > 4 (after 32 rounds)",
    "rank_by": "you.match_points * 1000 + you.card_points",
    "decided_by": "The team with more match points wins, and both its partners win. If match points are equal, the team with the higher card-point total wins. If both are equal, all four players share the top value, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Seats 1 and 3 are team NS and seats 2 and 4 are team EW, and no talk step exists."
    },
    {
      "id": "R2",
      "text": "When round_in_hand is 1, each player is dealt 7 cards from the 30-card deck and the other 2 cards go to the hidden kitty."
    },
    {
      "id": "R3",
      "text": "The declarer is seat 1 in hand 1, seat 2 in hand 2, seat 3 in hand 3 and seat 4 in hand 4."
    },
    {
      "id": "R4",
      "text": "When round_in_hand is 1, the declarer names one of Spades, Hearts, Clubs or Diamonds as trump_suit, it is announced to all, and the declarer leads the first trick."
    },
    {
      "id": "R5",
      "text": "Trumps are BJ, SJ and the 7 cards of trump_suit, 9 cards in all, and they count as the single suit 'Trump' for following."
    },
    {
      "id": "R6",
      "text": "When the leader plays a card, led_suit becomes that card's suit, or 'Trump' if the card is a joker or of trump_suit."
    },
    {
      "id": "R7",
      "text": "When a follower holds a card of led_suit, then only led_suit cards are offered; when they hold none, then every card in their hand is offered."
    },
    {
      "id": "R8",
      "text": "Players play to a trick in anticlockwise order starting from the leader, and each sees the cards already played."
    },
    {
      "id": "R9",
      "text": "Card strength is 40 for BJ, 39 for SJ, 20 + rank for a trump_suit card, 10 + rank for a non-trump led_suit card, and rank otherwise, with 5=1, 8=2, 10=3, J=4, Q=5, K=6, A=7."
    },
    {
      "id": "R10",
      "text": "The highest-strength card wins the trick; its team adds the trick's points (K=10, 10=10, 5=5, others 0) to its hand points, and its player leads next."
    },
    {
      "id": "R11",
      "text": "When round_in_hand is 8, after the trick the kitty is revealed and its points go to the team that won that trick."
    },
    {
      "id": "R12",
      "text": "At the end of a hand, if defender_points is 0 to 15, the Declaring Team gains 3 match points."
    },
    {
      "id": "R13",
      "text": "At the end of a hand, if defender_points is 20 to 35, the Declaring Team gains 2 match points."
    },
    {
      "id": "R14",
      "text": "At the end of a hand, if defender_points is 40 to 55, the Defending Team gains 1 match point."
    },
    {
      "id": "R15",
      "text": "At the end of a hand, if defender_points is 60 to 75, the Defending Team gains 2 match points."
    },
    {
      "id": "R16",
      "text": "At the end of a hand, if defender_points is 80 to 100, the Defending Team gains 3 match points."
    },
    {
      "id": "R17",
      "text": "At the end of each hand, each team adds its hand points to its card-point total, and hand points reset to 0 for the next hand."
    },
    {
      "id": "R18",
      "text": "After 4 hands (32 rounds), the team with more match points wins; if level, the team with more card points wins; if both are level, the match is a draw."
    }
  ],
  "offers": [
    {
      "question": "Name the trump suit (round 1 of each hand)",
      "who": "the declarer only",
      "options": "Spades, Hearts, Clubs, Diamonds"
    },
    {
      "question": "Play a card to the trick (rounds 2 to 8)",
      "who": "each seat in turn from the leader",
      "options": "the leader: every card in own hand; a follower holding at least one card of led_suit (for led_suit Trump: jokers and trump_suit cards; for any other suit: cards of that suit that are not trumps): only those cards; a follower holding no led_suit card: every card in own hand"
    }
  ],
  "choices": [
    {
      "what": "4 players (min = max = suggested = 4)",
      "why": "The designer fixed two partnerships of two. Fewer seats break the teams, and more seats do not fit the 30-card deal of 7 each plus a 2-card kitty."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid talk; signalling through card play is the skill. A thoughtful player tracks played trumps and points, smears points onto a partner's winning trick, and holds trumps back to capture kings and tens."
    },
    {
      "what": "Team scores are mirrored onto each player's match_points and card_points",
      "why": "The ranking expression works per player, so both partners carry the team's totals."
    },
    {
      "what": "Ranking expression match_points * 1000 + card_points",
      "why": "Card points can total at most 400, so match points always come first and card points break ties. A full tie makes all four seats share the win, which is the draw."
    },
    {
      "what": "Card codes such as 'S-K', 'H-10', 'BJ', 'SJ'",
      "why": "The rules do not say how cards are labelled; codes let suit, rank and points be read arithmetically."
    }
  ],
  "simplifications": [
    {
      "what": "The 32 rounds run as one repeated step list, with `when` conditions on round_in_hand choosing the deal steps (round 1) or the trick steps (rounds 2 to 8)",
      "why": "The step list is flat; a condition on each single step gives the same order."
    },
    {
      "what": "Legality of following suit is enforced by offering only legal cards, with a judged check as a backstop",
      "why": "The source rejects illegal plays and asks again; offering only legal cards has the same effect."
    },
    {
      "what": "A draw is shown as all four seats sharing the win",
      "why": "The engine has no separate draw outcome."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: team, match_points, card_points; table: hand_number, declarer, trump_suit, ns_hand_points, ew_hand_points, ns_match_points, ew_match_points, ns_card_points, ew_card_points.
````

## Reply

````
```json
[
  {
    "name": "Teams are NS for seats 1 and 3 and EW for seats 2 and 4 at setup",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"team": "NS", "match_points": 0, "card_points": 0},
        "2": {"team": "EW", "match_points": 0, "card_points": 0},
        "3": {"team": "NS", "match_points": 0, "card_points": 0},
        "4": {"team": "EW", "match_points": 0, "card_points": 0}
      },
      "game": {"hand_number": 1, "declarer": 1, "ns_match_points": 0, "ew_match_points": 0}
    }
  },
  {
    "name": "Deal gives 7 cards to each seat and 2 to the kitty (random deal, counts only)",
    "rule": "R2",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "rules": [{"seat": 1, "options_include": "Spades"}],
    "expect": {
      "lens": {
        "game": {"deck": 0, "kitty": 2},
        "players": {"1": {"hand": 7}, "2": {"hand": 7}, "3": {"hand": 7}, "4": {"hand": 7}}
      },
      "game": {"trump_suit": "Spades", "declarer": 1}
    }
  },
  {
    "name": "In hand 2 seat 2 declares and names trumps",
    "rule": "R3",
    "players": 4,
    "rounds": 1,
    "given": {"game": {"hand_number": 2, "round_in_hand": 1}},
    "rules": [{"seat": 2, "options_include": "Hearts"}],
    "expect": {
      "game": {"declarer": 2, "trump_suit": "Hearts", "hand_number": 2},
      "not_offered": [
        {"seat": 1, "option": "Hearts"},
        {"seat": 3, "option": "Hearts"},
        {"seat": 4, "option": "Hearts"}
      ]
    }
  },
  {
    "name": "In hand 3 seat 3 declares and names trumps",
    "rule": "R3",
    "players": 4,
    "rounds": 1,
    "given": {"game": {"hand_number": 3, "round_in_hand": 1}},
    "rules": [{"seat": 3, "options_include": "Clubs"}],
    "expect": {
      "game": {"declarer": 3, "trump_suit": "Clubs"},
      "not_offered": [
        {"seat": 1, "option": "Clubs"},
        {"seat": 2, "option": "Clubs"},
        {"seat": 4, "option": "Clubs"}
      ]
    }
  },
  {
    "name": "In hand 4 seat 4 declares and names trumps",
    "rule": "R3",
    "players": 4,
    "rounds": 1,
    "given": {"game": {"hand_number": 4, "round_in_hand": 1}},
    "rules": [{"seat": 4, "options_include": "Diamonds"}],
    "expect": {
      "game": {"declarer": 4, "trump_suit": "Diamonds"},
      "not_offered": [
        {"seat": 1, "option": "Diamonds"},
        {"seat": 2, "option": "Diamonds"},
        {"seat": 3, "option": "Diamonds"}
      ]
    }
  },
  {
    "name": "Declarer seat 1 names Diamonds as trumps in hand 1, and only the declarer is asked",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "Diamonds"}],
    "expect": {
      "game": {"trump_suit": "Diamonds", "declarer": 1, "hand_number": 1},
      "offered": [
        {"seat": 1, "option": "Spades"},
        {"seat": 1, "option": "Hearts"},
        {"seat": 1, "option": "Clubs"}
      ],
      "not_offered": [
        {"seat": 2, "option": "Spades"},
        {"seat": 3, "option": "Spades"},
        {"seat": 4, "option": "Spades"}
      ]
    }
  },
  {
    "name": "Jokers and trump-suit cards form one Trump suit for following",
    "rule": "R5",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["BJ", "C-5"]},
        "2": {"hand": ["S-8", "H-K"]},
        "3": {"hand": ["SJ", "D-A"]},
        "4": {"hand": ["H-5", "C-A"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [
      {"seat": 1, "options_include": "BJ"},
      {"seat": 4, "options_include": "H-5"}
    ],
    "expect": {
      "game": {"ns_hand_points": 5, "ew_hand_points": 0},
      "offered": [
        {"seat": 2, "option": "S-8"},
        {"seat": 3, "option": "SJ"},
        {"seat": 4, "option": "C-A"}
      ],
      "not_offered": [
        {"seat": 2, "option": "H-K"},
        {"seat": 3, "option": "D-A"}
      ]
    }
  },
  {
    "name": "A non-trump lead sets led suit to that suit; trump-suit cards do not follow it",
    "rule": "R6",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["H-A", "C-8"]},
        "2": {"hand": ["H-5", "S-A"]},
        "3": {"hand": ["H-K", "D-8"]},
        "4": {"hand": ["C-K", "S-5"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [
      {"seat": 1, "options_include": "H-A"},
      {"seat": 4, "options_include": "C-K"}
    ],
    "expect": {
      "game": {"ns_hand_points": 25, "ew_hand_points": 0},
      "offered": [{"seat": 4, "option": "S-5"}],
      "not_offered": [
        {"seat": 2, "option": "S-A"},
        {"seat": 3, "option": "D-8"}
      ]
    }
  },
  {
    "name": "Leading a trump-suit card sets led suit to Trump, so jokers must follow",
    "rule": "R6",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-8", "H-A"]},
        "2": {"hand": ["SJ", "H-K"]},
        "3": {"hand": ["D-8", "C-8"]},
        "4": {"hand": ["S-10", "H-10"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [
      {"seat": 1, "options_include": "S-8"},
      {"seat": 3, "options_include": "D-8"}
    ],
    "expect": {
      "game": {"ns_hand_points": 0, "ew_hand_points": 10},
      "offered": [{"seat": 3, "option": "C-8"}],
      "not_offered": [
        {"seat": 2, "option": "H-K"},
        {"seat": 4, "option": "H-10"}
      ]
    }
  },
  {
    "name": "A follower with no led-suit card is offered every card; a follower with one is offered only led-suit cards",
    "rule": "R7",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["D-A", "S-8"]},
        "2": {"hand": ["C-5", "S-10"]},
        "3": {"hand": ["D-5", "D-K", "C-A"]},
        "4": {"hand": ["H-8", "D-10"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Hearts",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [
      {"seat": 1, "options_include": "D-A"},
      {"seat": 2, "options_include": "S-10"},
      {"seat": 3, "options_include": "D-K"}
    ],
    "expect": {
      "game": {"ns_hand_points": 30, "ew_hand_points": 0},
      "offered": [
        {"seat": 2, "option": "C-5"},
        {"seat": 3, "option": "D-5"}
      ],
      "not_offered": [
        {"seat": 3, "option": "C-A"},
        {"seat": 4, "option": "H-8"}
      ]
    }
  },
  {
    "name": "Play goes anticlockwise from leader seat 3 and later seats follow the led suit",
    "rule": "R8",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["H-5", "D-8"]},
        "2": {"hand": ["C-10", "S-A"]},
        "3": {"hand": ["C-A", "H-Q"]},
        "4": {"hand": ["C-8", "H-K"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Spades",
        "leader": 3,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [
      {"seat": 3, "options_include": "C-A"},
      {"seat": 1, "options_include": "H-5"}
    ],
    "expect": {
      "game": {"ns_hand_points": 15, "ew_hand_points": 0},
      "offered": [{"seat": 1, "option": "D-8"}],
      "not_offered": [
        {"seat": 4, "option": "H-K"},
        {"seat": 2, "option": "S-A"}
      ]
    }
  },
  {
    "name": "A low trump beats the led suit's ace and king; an off-suit card is weakest",
    "rule": "R9",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["C-A"]},
        "2": {"hand": ["H-5", "D-A"]},
        "3": {"hand": ["C-K"]},
        "4": {"hand": ["S-A"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Hearts",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [{"seat": 2, "options_include": "H-5"}],
    "expect": {"game": {"ns_hand_points": 0, "ew_hand_points": 15}}
  },
  {
    "name": "Big Joker beats Small Joker, which beats the trump ace",
    "rule": "R9",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["H-A"]},
        "2": {"hand": ["SJ"]},
        "3": {"hand": ["BJ"]},
        "4": {"hand": ["H-K"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Hearts",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "expect": {"game": {"ns_hand_points": 10, "ew_hand_points": 0}}
  },
  {
    "name": "The trick winner's team takes the points and the winner leads the next trick",
    "rule": "R10",
    "players": 4,
    "rounds": 2,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["D-8", "C-K"]},
        "2": {"hand": ["D-A", "H-8"]},
        "3": {"hand": ["D-5", "C-8"]},
        "4": {"hand": ["D-10", "H-5"]}
      },
      "game": {
        "round_in_hand": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "rules": [{"seat": 1, "options_include": "D-8"}],
    "expect": {"game": {"ns_hand_points": 0, "ew_hand_points": 30}}
  },
  {
    "name": "The kitty's points go to the winner of the last trick (EW 5 + kitty 15 = 20)",
    "rule": "R11",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["C-A"]},
        "2": {"hand": ["C-5"]},
        "3": {"hand": ["D-8"]},
        "4": {"hand": ["S-8"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 1,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "kitty": ["S-K", "H-5"],
        "ns_hand_points": 0,
        "ew_hand_points": 0
      }
    },
    "expect": {
      "game": {
        "ew_hand_points": 20,
        "ns_hand_points": 0,
        "ew_card_points": 20,
        "ns_card_points": 0,
        "ns_match_points": 2,
        "ew_match_points": 0,
        "hand_number": 2
      },
      "players": {
        "2": {"card_points": 20},
        "4": {"card_points": 20},
        "1": {"match_points": 2}
      }
    }
  },
  {
    "name": "Defenders on 15 points: the declaring team NS gains 3 match points",
    "rule": "R12",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"]},
        "2": {"hand": ["H-8"]},
        "3": {"hand": ["H-Q"]},
        "4": {"hand": ["C-J"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 1,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 85,
        "ew_hand_points": 15
      }
    },
    "expect": {
      "game": {"ns_match_points": 3, "ew_match_points": 0, "ns_card_points": 85, "ew_card_points": 15},
      "players": {
        "1": {"match_points": 3, "card_points": 85},
        "3": {"match_points": 3, "card_points": 85},
        "2": {"match_points": 0, "card_points": 15},
        "4": {"match_points": 0, "card_points": 15}
      }
    }
  },
  {
    "name": "Defenders NS on 30 points: the declaring team EW gains 2 match points",
    "rule": "R13",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"]},
        "2": {"hand": ["H-8"]},
        "3": {"hand": ["H-Q"]},
        "4": {"hand": ["C-J"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 2,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 30,
        "ew_hand_points": 70
      }
    },
    "expect": {
      "game": {"ns_match_points": 0, "ew_match_points": 2, "ns_card_points": 30, "ew_card_points": 70, "hand_number": 3},
      "players": {
        "2": {"match_points": 2},
        "4": {"match_points": 2},
        "1": {"match_points": 0}
      }
    }
  },
  {
    "name": "Defenders EW on 50 points: the defending team gains 1 match point",
    "rule": "R14",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"]},
        "2": {"hand": ["H-8"]},
        "3": {"hand": ["H-Q"]},
        "4": {"hand": ["C-J"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 1,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 50,
        "ew_hand_points": 50
      }
    },
    "expect": {
      "game": {"ns_match_points": 0, "ew_match_points": 1, "ns_card_points": 50, "ew_card_points": 50},
      "players": {
        "2": {"match_points": 1},
        "4": {"match_points": 1},
        "3": {"match_points": 0}
      }
    }
  },
  {
    "name": "Defenders NS on 60 points: the defending team gains 2 match points",
    "rule": "R15",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"]},
        "2": {"hand": ["H-8"]},
        "3": {"hand": ["H-Q"]},
        "4": {"hand": ["C-J"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 2,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 60,
        "ew_hand_points": 40
      }
    },
    "expect": {
      "game": {"ns_match_points": 2, "ew_match_points": 0, "ns_card_points": 60, "ew_card_points": 40},
      "players": {
        "1": {"match_points": 2},
        "3": {"match_points": 2},
        "2": {"match_points": 0}
      }
    }
  },
  {
    "name": "Defenders EW on 85 points: the defending team gains 3 match points",
    "rule": "R16",
    "players": 4,
    "rounds": 1,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"]},
        "2": {"hand": ["H-8"]},
        "3": {"hand": ["H-Q"]},
        "4": {"hand": ["C-J"]}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 1,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 1,
        "declaring_team": "NS",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 15,
        "ew_hand_points": 85
      }
    },
    "expect": {
      "game": {"ns_match_points": 0, "ew_match_points": 3, "ns_card_points": 15, "ew_card_points": 85},
      "players": {
        "2": {"match_points": 3, "card_points": 85},
        "4": {"match_points": 3, "card_points": 85},
        "1": {"match_points": 0, "card_points": 15}
      }
    }
  },
  {
    "name": "Hand points add to the running card-point totals and reset to 0 when the next hand starts",
    "rule": "R17",
    "players": 4,
    "rounds": 2,
    "default": "first",
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"], "card_points": 55, "match_points": 0},
        "2": {"hand": ["H-8"], "card_points": 45, "match_points": 3},
        "3": {"hand": ["H-Q"], "card_points": 55, "match_points": 0},
        "4": {"hand": ["C-J"], "card_points": 45, "match_points": 3}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 2,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 2,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 70,
        "ew_hand_points": 30,
        "ns_card_points": 55,
        "ew_card_points": 45,
        "ns_match_points": 0,
        "ew_match_points": 3
      }
    },
    "expect": {
      "game": {
        "ns_card_points": 125,
        "ew_card_points": 75,
        "ns_match_points": 2,
        "ew_match_points": 3,
        "ns_hand_points": 0,
        "ew_hand_points": 0,
        "hand_number": 3,
        "declarer": 3
      },
      "players": {
        "1": {"card_points": 125, "match_points": 2},
        "3": {"card_points": 125, "match_points": 2},
        "2": {"card_points": 75, "match_points": 3},
        "4": {"card_points": 75, "match_points": 3}
      }
    }
  },
  {
    "name": "After hand 4 the team with more match points (NS) wins",
    "rule": "R18",
    "players": 4,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"], "match_points": 5, "card_points": 200},
        "2": {"hand": ["H-8"], "match_points": 4, "card_points": 100},
        "3": {"hand": ["H-Q"], "match_points": 5, "card_points": 200},
        "4": {"hand": ["C-J"], "match_points": 4, "card_points": 100}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 4,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 4,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 50,
        "ew_hand_points": 50,
        "ns_match_points": 5,
        "ew_match_points": 4,
        "ns_card_points": 200,
        "ew_card_points": 100
      }
    },
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 6250, "2": 4150, "3": 6250, "4": 4150},
      "game": {"ns_match_points": 6, "ew_match_points": 4}
    }
  },
  {
    "name": "Match points level after hand 4: the team with more card points (EW) wins",
    "rule": "R18",
    "players": 4,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"], "match_points": 4, "card_points": 100},
        "2": {"hand": ["H-8"], "match_points": 6, "card_points": 200},
        "3": {"hand": ["H-Q"], "match_points": 4, "card_points": 100},
        "4": {"hand": ["C-J"], "match_points": 6, "card_points": 200}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 4,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 4,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 60,
        "ew_hand_points": 40,
        "ns_match_points": 4,
        "ew_match_points": 6,
        "ns_card_points": 100,
        "ew_card_points": 200
      }
    },
    "expect": {
      "winner": [2, 4],
      "standings": {"1": 6160, "2": 6240, "3": 6160, "4": 6240},
      "game": {"ns_match_points": 6, "ew_match_points": 6, "ns_card_points": 160, "ew_card_points": 240}
    }
  },
  {
    "name": "Match points and card points both level after hand 4: all four seats share the win",
    "rule": "R18",
    "players": 4,
    "judge": {"The card this player chose is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["S-A"], "match_points": 4, "card_points": 140},
        "2": {"hand": ["H-8"], "match_points": 6, "card_points": 160},
        "3": {"hand": ["H-Q"], "match_points": 4, "card_points": 140},
        "4": {"hand": ["C-J"], "match_points": 6, "card_points": 160}
      },
      "game": {
        "round_in_hand": 8,
        "hand_number": 4,
        "trump_suit": "Spades",
        "leader": 1,
        "declarer": 4,
        "declaring_team": "EW",
        "kitty": ["C-8", "D-8"],
        "ns_hand_points": 60,
        "ew_hand_points": 40,
        "ns_match_points": 4,
        "ew_match_points": 6,
        "ns_card_points": 140,
        "ew_card_points": 160
      }
    },
    "expect": {
      "winner": [1, 2, 3, 4],
      "standings": {"1": 6200, "2": 6200, "3": 6200, "4": 6200}
    }
  }
]
```
````
