# 09 scenarios

- time: 2026-10-28T03:16:00+00:00 (149.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 1375769f282a6339, reply sha256 c0fca0aef768cf84

## Sent

````
SPEC:
{
  "name": "Concealed Quadrille",
  "summary": "Four-player trick-taking game over 8 hands of 5 tricks. Players bid for the contract, the Taker names trumps and secretly calls a partner (or plays solo), and the hand is scored to zero sum.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 20,
    "suits": 4,
    "ranks_per_suit": 5,
    "hand_size": 5,
    "hands": 8,
    "tricks_per_hand": 5,
    "rounds": 40,
    "bid_pass_value": 0,
    "bid_min": 3,
    "bid_max": 5,
    "all_pass_contract": 3,
    "declaration_options": 16,
    "spadille_code": 11,
    "baste_code": 21,
    "power_spadille": 30,
    "power_manille": 29,
    "power_baste": 28,
    "power_trump_base": 20,
    "power_off_suit": 0,
    "solo_multiplier": 3,
    "trumps_red": 7,
    "trumps_black": 6,
    "tiebreak_key_bid_multiplier": 10,
    "rank_score_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "running game score",
        "observable": true
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tricks won over the whole game, used as the tie-break",
        "observable": true
      },
      {
        "key": "hand_tricks",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tricks won in the current hand, reset each hand",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "card codes held, shown by name and code",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "this hand's bid (0 = Pass, else 3, 4 or 5)",
        "observable": false
      },
      {
        "key": "is_partner",
        "type": "bool",
        "visible": "ally",
        "initial": false,
        "meaning": "privately told: you are the Taker's partner in this hand (call only)",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "code of the card played to the current trick",
        "observable": false
      },
      {
        "key": "power",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "card power of played_card in the current trick",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          11,
          12,
          13,
          14,
          15,
          21,
          22,
          23,
          24,
          25,
          31,
          32,
          33,
          34,
          35,
          41,
          42,
          43,
          44,
          45
        ],
        "meaning": "undealt cards",
        "observable": false
      },
      {
        "key": "round_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round (trick) number, 1 to 40",
        "observable": false
      },
      {
        "key": "hand_no",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current hand h = ceil(round_no / 5)",
        "observable": false
      },
      {
        "key": "trick_in_hand",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "round_no - 5*(hand_no - 1), 1 to 5",
        "observable": false
      },
      {
        "key": "priority_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "((hand_no - 1) mod 4) + 1",
        "observable": false
      },
      {
        "key": "taker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Taker's seat this hand",
        "observable": true
      },
      {
        "key": "contract",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "contract B",
        "observable": true
      },
      {
        "key": "trump",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "trump suit number t (1 Spades, 2 Clubs, 3 Hearts, 4 Diamonds)",
        "observable": true
      },
      {
        "key": "partner_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "seat named by the Taker; equal to taker means solo; announced at hand end",
        "observable": false
      },
      {
        "key": "is_solo",
        "type": "bool",
        "visible": "none",
        "initial": false,
        "meaning": "partner_seat == taker; announced at hand end",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat leading the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "led suit L: trump if the led card is 11, 21 or of suit trump, else floor(code/10)",
        "observable": false
      },
      {
        "key": "last_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "winner of the most recent trick",
        "observable": false
      },
      {
        "key": "hand_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "T: Taker's hand_tricks plus partner's if call (announced at hand end)",
        "observable": false
      },
      {
        "key": "hand_delta",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "d for the hand (announced at hand end)",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1 to 4 sit clockwise.",
    "Every player's score, tricks_won and hand_tricks are 0.",
    "The deck holds the 20 codes 11-15, 21-25, 31-35, 41-45 (code = 10 x suit + rank; suits Spades 1, Clubs 2, Hearts 3, Diamonds 4; ranks A 1, 2 2, J 3, Q 4, K 5).",
    "Cards are always shown to players by name and code (e.g. 11 = Ace of Spades, Spadille; 21 = Ace of Clubs, Baste).",
    "round_no is 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_no += 1; hand_no = ceil(round_no/5); trick_in_hand = round_no - 5*(hand_no-1); priority_seat = ((hand_no-1) mod 4)+1; every played_card = 0 and power = 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 1: return all cards to deck (deck = all 20 codes, every hand = []), then deal 5 random cards from deck to each player's hand (remove from deck, append to hand); every hand_tricks = 0, bid = 0, is_partner = false"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 1: each player is sent their own hand by name and code"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Pass, 3, 4, 5",
      "effect": "when trick_in_hand == 1: bid = 0 for Pass, else the number; all bids announced together"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 1: key(seat) = bid*10 + (4 - ((seat - priority_seat) mod 4)); if every bid == 0 then taker = priority_seat and contract = 3, else taker = seat with max key and contract = that seat's bid; announce taker and contract"
    },
    {
      "action": "ask",
      "who": "seat taker",
      "answer": "one of 16 options: trump suit (Spades, Clubs, Hearts, Diamonds) x partner seat (1, 2, 3, 4; own seat = solo)",
      "effect": "when trick_in_hand == 1: trump = chosen suit number; partner_seat = chosen seat; is_solo = (partner_seat == taker); announce trump only"
    },
    {
      "action": "update",
      "who": "seat partner_seat",
      "answer": null,
      "effect": "when trick_in_hand == 1 and is_solo == false: is_partner of partner_seat = true; that player alone is privately told 'you are the Taker's partner'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "leader = taker if trick_in_hand == 1, else last_winner"
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "any card code in the leader's hand",
      "effect": "leader's played_card = chosen code; remove it from hand; announce the card by name and code"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "suit(c) = trump if c in {11,21}, else floor(c/10); led_suit = suit(leader's played_card)"
    },
    {
      "action": "poll",
      "who": "every seat except leader",
      "answer": "a card code from own hand: if the hand holds any card with suit(c) == led_suit, only those cards are offered, else any card",
      "effect": "each responder's played_card = chosen code; remove it from hand"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each player with c = played_card, r = c mod 10: power = 30 if c == 11; 29 if c == 10*trump+2; 28 if c == 21; 20 + r if floor(c/10) == trump; r if suit(c) == led_suit; else 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "last_winner = seat with the highest power (ties impossible); last_winner's tricks_won += 1 and hand_tricks += 1; announce all four cards and the winner"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 5: hand_total = taker.hand_tricks + (is_solo ? 0 : partner_seat.hand_tricks); hand_delta = contract-1 if hand_total >= contract; -(contract-1) if hand_total == contract-1; -contract if hand_total <= contract-2"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 5: if is_solo then taker.score += 3*hand_delta and each other seat score -= hand_delta; else taker and partner_seat score += hand_delta and the other two score -= hand_delta"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "when trick_in_hand == 5: announce partner_seat (or that it was a solo), hand_total, hand_delta and all scores"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round_no == 40, else continue"
    }
  ],
  "ending": {
    "condition": "round_no == 40",
    "rank_by": "you.score * 100 + you.tricks_won",
    "decided_by": "Highest score wins; among players tied on score, the one with the most tricks won over the game wins; players still level share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The pack has 20 cards with codes 10 x suit + rank, suits Spades 1, Clubs 2, Hearts 3, Diamonds 4 and ranks A 1, 2 2, J 3, Q 4, K 5; 11 is Spadille and 21 is Baste."
    },
    {
      "id": "R2",
      "text": "The game has 40 rounds; each round is one trick; hand h covers rounds 5h-4 to 5h, so there are 8 hands of 5 tricks."
    },
    {
      "id": "R3",
      "text": "The priority seat of hand h is ((h-1) mod 4)+1, giving 1, 2, 3, 4, 1, 2, 3, 4."
    },
    {
      "id": "R4",
      "text": "On the first trick of each hand, all 20 cards are shuffled, each player is dealt 5 private cards, and every hand_tricks is set to 0."
    },
    {
      "id": "R5",
      "text": "On the first trick of each hand, all players bid at once, each choosing Pass, 3, 4 or 5, and all bids are announced."
    },
    {
      "id": "R6",
      "text": "The highest bid becomes Taker with contract B equal to that bid; ties go to the tied seat first clockwise from the priority seat (key = bid*10 + 4 - ((seat - priority) mod 4))."
    },
    {
      "id": "R7",
      "text": "When all four players pass, the priority seat is Taker with contract 3."
    },
    {
      "id": "R8",
      "text": "The Taker privately chooses a trump suit and a partner seat from 16 options, and the trump suit is announced to all."
    },
    {
      "id": "R9",
      "text": "When the Taker names another seat, the hand is a call and only that seat is privately told it is the partner."
    },
    {
      "id": "R10",
      "text": "When the Taker names their own seat, the hand is a solo and nobody is told anything beyond the trump suit."
    },
    {
      "id": "R11",
      "text": "The partner seat stays hidden until the hand ends."
    },
    {
      "id": "R12",
      "text": "The trumps are every card of the trump suit plus 11 and 21; 11 and 21 count only as the trump suit, and Manille is code 10*trump+2."
    },
    {
      "id": "R13",
      "text": "The Taker leads the first trick of a hand, and the previous trick's winner leads every later trick."
    },
    {
      "id": "R14",
      "text": "The led card leaves the leader's hand and is shown to all; the led suit is trump if the card is 11, 21 or of the trump suit, else the card's suit."
    },
    {
      "id": "R15",
      "text": "The other three players play at once, and a player holding any card of the led suit (11 and 21 count as trump) must play one."
    },
    {
      "id": "R16",
      "text": "A player holding no card of the led suit may play any card, and illegal cards are never accepted."
    },
    {
      "id": "R17",
      "text": "Card power is 30 for 11, 29 for Manille, 28 for 21, 20 + rank for other trump-suit cards, the rank for non-trump cards of the led suit, and 0 for any other card."
    },
    {
      "id": "R18",
      "text": "The highest power wins the trick; all four cards and the winner are announced, and the winner gains 1 tricks_won and 1 hand_tricks."
    },
    {
      "id": "R19",
      "text": "After the fifth trick of a hand, T is the Taker's hand_tricks plus the partner's hand_tricks if the hand is a call."
    },
    {
      "id": "R20",
      "text": "When T >= B, d = B-1 (made); when T = B-1, d = -(B-1) (remise); when T <= B-2, d = -B (codille)."
    },
    {
      "id": "R21",
      "text": "In a call, the Taker and the partner each gain d and the other two each lose d."
    },
    {
      "id": "R22",
      "text": "In a solo, the Taker gains 3d and each of the other three loses d."
    },
    {
      "id": "R23",
      "text": "After each hand, the partner seat (or solo), T, d and all scores are announced."
    },
    {
      "id": "R24",
      "text": "There is no talk phase; players communicate only through bids and cards."
    },
    {
      "id": "R25",
      "text": "After round 40 the game ends: highest score wins, ties on score are broken by most tricks_won, and a further tie is a shared win (draw)."
    }
  ],
  "offers": [
    {
      "question": "Bid (first trick of each hand)",
      "who": "all seats",
      "options": "Pass, 3, 4, 5"
    },
    {
      "question": "Declaration (first trick of each hand)",
      "who": "the Taker only",
      "options": "16 combinations of trump suit (Spades, Clubs, Hearts, Diamonds) and partner seat (1, 2, 3, 4, own seat meaning solo)"
    },
    {
      "question": "Lead",
      "who": "the leader only",
      "options": "every card in the leader's hand"
    },
    {
      "question": "Follow",
      "who": "the three seats other than the leader",
      "options": "a seat holding any card of the led suit (11 and 21 counted as trump suit): only those cards; a seat holding none: every card in its hand"
    }
  ],
  "choices": [
    {
      "what": "4 players, fixed",
      "why": "The designer set 4. The deck (20 cards = 4 x 5), the partner call and the priority rotation are all built for exactly four seats."
    },
    {
      "what": "No talk phase",
      "why": "The rules forbid discussion; bids and cards are the only signals. A player's strategy lies in bidding to hand strength, choosing a partner who likely holds key trumps, and inferring the hidden partner from play."
    },
    {
      "what": "Ranking expression score*100 + tricks_won",
      "why": "tricks_won is at most 40 (under 100), so score dominates and tricks_won only breaks ties; players still level share the win, which serves as the draw."
    },
    {
      "what": "Card power stored as public player attributes",
      "why": "Power is computed only from public played cards, so showing it reveals nothing new."
    }
  ],
  "simplifications": [
    {
      "what": "The deck is rebuilt from all 20 codes at the start of each hand instead of physically gathering the cards",
      "why": "This is equivalent to gathering and shuffling, since all 20 cards are always played out over the 5 tricks."
    },
    {
      "what": "Hand-start and hand-end steps run in every round, gated by conditions on trick_in_hand",
      "why": "The engine's step list is flat; per-step conditions reproduce the source's 'first trick' and 'fifth trick' steps."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, tricks_won, hand_tricks; table: taker, contract, trump.
````

## Reply

````
[
{"name":"R1 deck holds the 20 cards before any deal","rule":"R1","players":4,"rounds":0,
 "expect":{"lens":{"game":{"deck":20},"players":{"1":{"hand":0},"2":{"hand":0},"3":{"hand":0},"4":{"hand":0}}}}},

{"name":"R2 game ends after round 40 and highest score wins","rule":"R2","players":4,"seed":1,"default":"decline",
 "given":{"game":{"round_no":39,"taker":1,"contract":3,"trump":3,"partner_seat":2,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"score":5,"tricks_won":10,"hand_tricks":1},
                     "2":{"hand":[12],"score":5,"tricks_won":10,"hand_tricks":1,"is_partner":true},
                     "3":{"hand":[13],"score":20,"tricks_won":10,"hand_tricks":1},
                     "4":{"hand":[14],"score":0,"tricks_won":9,"hand_tricks":1}}},
 "rules":[],
 "expect":{"winner":3,"standings":{"1":711,"2":710,"3":1810,"4":-191},
           "players":{"1":{"score":7,"tricks_won":11},"2":{"score":7},"3":{"score":18},"4":{"score":-2}}}},

{"name":"R3 priority seat of hand 2 is seat 2 (all pass)","rule":"R3","players":4,"seed":2,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":5}},
 "rules":[],
 "expect":{"game":{"taker":2,"contract":3}}},

{"name":"R3 priority seat of hand 4 is seat 4 (all pass)","rule":"R3","players":4,"seed":3,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":15}},
 "rules":[],
 "expect":{"game":{"taker":4,"contract":3}}},

{"name":"R4 each seat is dealt 5 cards, deck emptied (one card played after)","rule":"R4","players":4,"seed":4,"rounds":1,"default":"decline",
 "rules":[],
 "expect":{"lens":{"game":{"deck":0},"players":{"1":{"hand":4},"2":{"hand":4},"3":{"hand":4},"4":{"hand":4}}}}},

{"name":"R5 every seat is offered Pass, 3, 4 and 5","rule":"R5","players":4,"seed":5,"rounds":1,"default":"decline",
 "rules":[],
 "expect":{"offered":[{"seat":1,"option":"Pass"},{"seat":2,"option":"Pass"},{"seat":3,"option":"Pass"},{"seat":4,"option":"Pass"},
                      {"seat":1,"option":5},{"seat":2,"option":3},{"seat":3,"option":4},{"seat":4,"option":5}]}},

{"name":"R6 highest bid takes the contract","rule":"R6","players":4,"seed":6,"rounds":1,"default":"decline",
 "rules":[{"seat":4,"options_include":5},{"seat":1,"options_include":3}],
 "expect":{"game":{"taker":4,"contract":5}}},

{"name":"R6 tie with priority 1 goes to seat 2 over seat 3","rule":"R6","players":4,"seed":7,"rounds":1,"default":"decline",
 "rules":[{"seat":2,"options_include":4},{"seat":3,"options_include":4}],
 "expect":{"game":{"taker":2,"contract":4}}},

{"name":"R6 tie with priority 3 goes to seat 4 over seat 1","rule":"R6","players":4,"seed":8,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":10}},
 "rules":[{"seat":1,"options_include":3},{"seat":4,"options_include":3}],
 "expect":{"game":{"taker":4,"contract":3}}},

{"name":"R7 all pass in hand 1: seat 1 takes contract 3","rule":"R7","players":4,"seed":9,"rounds":1,"default":"decline",
 "rules":[],
 "expect":{"game":{"taker":1,"contract":3}}},

{"name":"R8 Taker's chosen trump suit is set","rule":"R8","players":4,"seed":10,"rounds":1,"default":"decline",
 "rules":[{"seat":1,"options_include":5},{"seat":1,"options_include":"Hearts"}],
 "expect":{"game":{"taker":1,"contract":5,"trump":3}}},

{"name":"R9 named seat is the partner and shares the made contract","rule":"R9","players":4,"seed":11,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":3,"trump":3,"partner_seat":4,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"hand_tricks":1},"2":{"hand":[12],"hand_tricks":2},
                     "3":{"hand":[13],"hand_tricks":0},"4":{"hand":[14],"hand_tricks":1,"is_partner":true}}},
 "rules":[],
 "expect":{"players":{"1":{"score":2},"2":{"score":-2},"3":{"score":-2},"4":{"score":2}}}},

{"name":"R10 solo: other seats' tricks do not help the Taker","rule":"R10","players":4,"seed":12,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":3,"trump":3,"partner_seat":1,"is_solo":true,"last_winner":1},
          "players":{"1":{"hand":[11],"hand_tricks":1},"2":{"hand":[12],"hand_tricks":0},
                     "3":{"hand":[13],"hand_tricks":3},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-6,"hand_tricks":2},"2":{"score":2},"3":{"score":2},"4":{"score":2}}}},

{"name":"R11 mid-hand trick changes no scores","rule":"R11","players":4,"seed":13,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"partner_seat":3,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11]},"2":{"hand":[12]},"3":{"hand":[13],"is_partner":true},"4":{"hand":[14]}}},
 "rules":[],
 "expect":{"players":{"1":{"score":0,"tricks_won":1},"2":{"score":0},"3":{"score":0},"4":{"score":0}}}},

{"name":"R12 Manille (2 of trump) beats Baste and trump King","rule":"R12","players":4,"seed":14,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":4,"last_winner":1},
          "players":{"1":{"hand":[21]},"2":{"hand":[42]},"3":{"hand":[45]},"4":{"hand":[25]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1,"hand_tricks":1},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R12 Baste is not a club: seat without clubs may play any card","rule":"R12","players":4,"seed":15,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[24]},"2":{"hand":[21,33]},"3":{"hand":[22]},"4":{"hand":[15]}}},
 "rules":[{"seat":2,"options_include":"Ace of Clubs"}],
 "expect":{"offered":[{"seat":2,"option":"Jack of Hearts"}],
           "players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R13 previous trick winner leads a later trick","rule":"R13","players":4,"seed":16,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":3},
          "players":{"1":{"hand":[25]},"2":{"hand":[12]},"3":{"hand":[14]},"4":{"hand":[13]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1},"4":{"tricks_won":0}}}},

{"name":"R14 leading Spadille makes trump the led suit","rule":"R14","players":4,"seed":17,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[11]},"2":{"hand":[33,15]},"3":{"hand":[12]},"4":{"hand":[41]}}},
 "rules":[],
 "expect":{"not_offered":[{"seat":2,"option":"King of Spades"}],
           "lens":{"players":{"1":{"hand":0},"2":{"hand":1}}},
           "players":{"1":{"tricks_won":1},"2":{"tricks_won":0},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R15 Baste counts as trump and must follow a trump lead","rule":"R15","players":4,"seed":18,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[35]},"2":{"hand":[21,14]},"3":{"hand":[13]},"4":{"hand":[44]}}},
 "rules":[],
 "expect":{"not_offered":[{"seat":2,"option":"Queen of Spades"}],
           "players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R15 a seat holding the led suit must follow it","rule":"R15","players":4,"seed":19,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[14]},"2":{"hand":[12,31]},"3":{"hand":[25]},"4":{"hand":[44]}}},
 "rules":[],
 "expect":{"not_offered":[{"seat":2,"option":"Ace of Hearts"}],
           "players":{"1":{"tricks_won":1},"2":{"tricks_won":0},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R16 a seat void in the led suit may trump","rule":"R16","players":4,"seed":20,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[14]},"2":{"hand":[31,44]},"3":{"hand":[12]},"4":{"hand":[45]}}},
 "rules":[{"seat":2,"options_include":"Ace of Hearts"}],
 "expect":{"offered":[{"seat":2,"option":"Queen of Diamonds"}],
           "players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R17 Spadille beats Manille and Baste","rule":"R17","players":4,"seed":21,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[21]},"2":{"hand":[32]},"3":{"hand":[35]},"4":{"hand":[11]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":0},"4":{"tricks_won":1}}}},

{"name":"R17 a trump beats a higher card of the led suit","rule":"R17","players":4,"seed":22,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[13]},"2":{"hand":[15]},"3":{"hand":[31]},"4":{"hand":[45]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":0},"3":{"tricks_won":1},"4":{"tricks_won":0}}}},

{"name":"R17 highest card of the led suit wins without trumps","rule":"R17","players":4,"seed":23,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":1,"contract":3,"trump":3,"last_winner":1},
          "players":{"1":{"hand":[13]},"2":{"hand":[15]},"3":{"hand":[45]},"4":{"hand":[24]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0},"2":{"tricks_won":1},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R18 trick winner gains 1 tricks_won and 1 hand_tricks","rule":"R18","players":4,"seed":24,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":1,"taker":2,"contract":3,"trump":3,"last_winner":2},
          "players":{"1":{"hand":[12]},"2":{"hand":[11],"tricks_won":3,"hand_tricks":1},"3":{"hand":[13]},"4":{"hand":[14]}}},
 "rules":[],
 "expect":{"players":{"1":{"tricks_won":0,"hand_tricks":0},"2":{"tricks_won":4,"hand_tricks":2},"3":{"tricks_won":0},"4":{"tricks_won":0}}}},

{"name":"R19 partner's tricks count toward T in a call","rule":"R19","players":4,"seed":25,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":4,"trump":3,"partner_seat":3,"is_solo":false,"last_winner":3},
          "players":{"1":{"hand":[12],"hand_tricks":2},"2":{"hand":[13],"hand_tricks":1},
                     "3":{"hand":[11],"hand_tricks":1,"is_partner":true},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":3},"2":{"score":-3},"3":{"score":3,"hand_tricks":2},"4":{"score":-3}}}},

{"name":"R20 made: T=4 of contract 4 gives d=3","rule":"R20","players":4,"seed":26,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":4,"trump":3,"partner_seat":3,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"hand_tricks":2},"2":{"hand":[12],"hand_tricks":1},
                     "3":{"hand":[13],"hand_tricks":1,"is_partner":true},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":3,"hand_tricks":3},"2":{"score":-3},"3":{"score":3},"4":{"score":-3}}}},

{"name":"R20 remise: T=3 of contract 4 gives d=-3","rule":"R20","players":4,"seed":27,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":4,"trump":3,"partner_seat":3,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"hand_tricks":1},"2":{"hand":[12],"hand_tricks":1},
                     "3":{"hand":[13],"hand_tricks":1,"is_partner":true},"4":{"hand":[14],"hand_tricks":1}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-3},"2":{"score":3},"3":{"score":-3},"4":{"score":3}}}},

{"name":"R20 codille: T=3 of contract 5 gives d=-5","rule":"R20","players":4,"seed":28,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":1,"contract":5,"trump":3,"partner_seat":3,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"hand_tricks":1},"2":{"hand":[12],"hand_tricks":2},
                     "3":{"hand":[13],"hand_tricks":1,"is_partner":true},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-5},"2":{"score":5},"3":{"score":-5},"4":{"score":5}}}},

{"name":"R21 call: Taker and partner gain d, others lose d, added to running scores","rule":"R21","players":4,"seed":29,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":2,"contract":3,"trump":3,"partner_seat":4,"is_solo":false,"last_winner":4},
          "players":{"1":{"hand":[12],"hand_tricks":2,"score":4},"2":{"hand":[13],"hand_tricks":1,"score":-1},
                     "3":{"hand":[14],"hand_tricks":0,"score":0},"4":{"hand":[11],"hand_tricks":1,"score":2,"is_partner":true}}},
 "rules":[],
 "expect":{"players":{"1":{"score":2},"2":{"score":1},"3":{"score":-2},"4":{"score":4}}}},

{"name":"R22 solo made: Taker gains 3d, others lose d","rule":"R22","players":4,"seed":30,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":2,"contract":3,"trump":3,"partner_seat":2,"is_solo":true,"last_winner":2},
          "players":{"1":{"hand":[12],"hand_tricks":1},"2":{"hand":[11],"hand_tricks":2,"score":1},
                     "3":{"hand":[13],"hand_tricks":1},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-2},"2":{"score":7},"3":{"score":-2},"4":{"score":-2}}}},

{"name":"R22 solo codille: Taker loses 12, others gain 4","rule":"R22","players":4,"seed":31,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":2,"contract":4,"trump":3,"partner_seat":2,"is_solo":true,"last_winner":2},
          "players":{"1":{"hand":[12],"hand_tricks":2},"2":{"hand":[11],"hand_tricks":1},
                     "3":{"hand":[13],"hand_tricks":1},"4":{"hand":[14],"hand_tricks":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":4},"2":{"score":-12},"3":{"score":4},"4":{"score":4}}}},

{"name":"R23 scores are updated at hand end","rule":"R23","players":4,"seed":32,"rounds":1,"default":"decline",
 "given":{"game":{"round_no":4,"taker":3,"contract":3,"trump":3,"partner_seat":1,"is_solo":false,"last_winner":3},
          "players":{"1":{"hand":[12],"hand_tricks":0,"is_partner":true},"2":{"hand":[13],"hand_tricks":1},
                     "3":{"hand":[11],"hand_tricks":2},"4":{"hand":[14],"hand_tricks":1}}},
 "rules":[],
 "expect":{"players":{"1":{"score":2},"2":{"score":-2},"3":{"score":2,"hand_tricks":3},"4":{"score":-2}}}},

{"name":"R24 no talk option is ever offered","rule":"R24","players":4,"seed":33,"rounds":1,"default":"decline",
 "rules":[],
 "expect":{"not_offered":[{"seat":1,"option":"Talk"},{"seat":2,"option":"Talk"},{"seat":3,"option":"Talk"},{"seat":4,"option":"Talk"}]}},

{"name":"R25 tie on score broken by tricks_won","rule":"R25","players":4,"seed":34,"default":"decline",
 "given":{"game":{"round_no":39,"taker":1,"contract":3,"trump":3,"partner_seat":2,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"score":10,"tricks_won":8,"hand_tricks":1},
                     "2":{"hand":[12],"score":10,"tricks_won":12,"hand_tricks":1,"is_partner":true},
                     "3":{"hand":[13],"score":0,"tricks_won":10,"hand_tricks":1},
                     "4":{"hand":[14],"score":0,"tricks_won":5,"hand_tricks":1}}},
 "rules":[],
 "expect":{"winner":2,"standings":{"1":1209,"2":1212,"3":-190,"4":-195},
           "players":{"1":{"score":12,"tricks_won":9},"2":{"score":12,"tricks_won":12},"3":{"score":-2},"4":{"score":-2}}}},

{"name":"R25 level on score and tricks_won share the win","rule":"R25","players":4,"seed":35,"default":"decline",
 "given":{"game":{"round_no":39,"taker":1,"contract":3,"trump":3,"partner_seat":2,"is_solo":false,"last_winner":1},
          "players":{"1":{"hand":[11],"score":10,"tricks_won":11,"hand_tricks":1},
                     "2":{"hand":[12],"score":10,"tricks_won":12,"hand_tricks":1,"is_partner":true},
                     "3":{"hand":[13],"score":0,"tricks_won":10,"hand_tricks":1},
                     "4":{"hand":[14],"score":0,"tricks_won":5,"hand_tricks":1}}},
 "rules":[],
 "expect":{"winner":[1,2],"standings":{"1":1212,"2":1212,"3":-190,"4":-195},
           "players":{"1":{"score":12,"tricks_won":12},"2":{"score":12}}}}
]
````
