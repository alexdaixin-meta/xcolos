# 24 scenarios

- time: 2026-10-28T03:18:15+00:00 (147.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5b8968802f17d733, reply sha256 dd02876e96cf81a7

## Sent

````
SPEC:
{
  "name": "Mal\u00fd Mari\u00e1\u0161 (Little Mari\u00e1\u0161)",
  "summary": "Three-player trick-taking game with 12 cards: a secret bid picks a declarer, contract and trump, defenders may double (flek) and the declarer redouble (re), and 9 deals of 4 tricks are settled zero-sum.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "num_cards": 12,
    "num_suits": 4,
    "num_ranks": 3,
    "cards_per_hand": 4,
    "ace_points": 10,
    "ten_points": 10,
    "king_points": 0,
    "last_trick_bonus": 10,
    "points_per_deal": 90,
    "deals": 9,
    "tricks_per_deal": 4,
    "total_rounds": 36,
    "bid_min": 50,
    "bid_max": 90,
    "bid_step": 10,
    "eldest_default_bid": 50,
    "stake_divisor": 10,
    "stake_offset": 4,
    "initial_multiplier": 1,
    "flek_factor": 2,
    "re_factor": 2,
    "hearts_factor": 2,
    "declarer_win_factor": 2,
    "declarer_loss_factor": 2,
    "trump_key_bonus": 10,
    "led_suit_key_bonus": 5,
    "initial_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running match score, the sum of the deal settlements.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card codes held (code = 3 x suit + rank; suits H=0, B=1, L=2, A=3; ranks K=0, 10=1, A=2).",
        "observable": false
      },
      {
        "key": "bid",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "This deal's secret bid, 'PASS' or 'N S'. It is announced after resolution.",
        "observable": false
      },
      {
        "key": "bid_value",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "N of the bid (0 for PASS), after the eldest default is applied.",
        "observable": false
      },
      {
        "key": "flek_answer",
        "type": "text",
        "visible": "ally",
        "initial": "NO",
        "meaning": "Answer in the flek poll: FLEK, RE or NO. It is announced after resolution.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          0,
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11
        ],
        "meaning": "The 12 card codes, shuffled and dealt at trick 1 of each deal.",
        "observable": false
      },
      {
        "key": "deal",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current deal, 1 to 9 (10 means the match is over).",
        "observable": true
      },
      {
        "key": "trick",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current trick within the deal, 1 to 4.",
        "observable": false
      },
      {
        "key": "eldest",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Eldest seat of this deal, equal to ((deal-1) mod 3)+1.",
        "observable": false
      },
      {
        "key": "declarer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the declarer for this deal.",
        "observable": true
      },
      {
        "key": "contract",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Contract N (50 to 90).",
        "observable": true
      },
      {
        "key": "trump",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Trump suit index (H=0, B=1, L=2, A=3).",
        "observable": true
      },
      {
        "key": "base_stake",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Base stake, contract/10 - 4.",
        "observable": false
      },
      {
        "key": "multiplier",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Stake multiplier from flek and re.",
        "observable": true
      },
      {
        "key": "declarer_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points taken by the declarer this deal.",
        "observable": false
      },
      {
        "key": "defender_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points taken by the defenders this deal.",
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
        "key": "trick_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Card codes played to the current trick, in order.",
        "observable": false
      },
      {
        "key": "trick_seats",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Seats that played each card of the current trick, in order.",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Suit index of the first card of the current trick.",
        "observable": false
      },
      {
        "key": "best_key",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Internal strength of the best card so far in the trick.",
        "observable": false
      },
      {
        "key": "best_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Internal: seat currently winning the trick.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player's score is set to 0.",
    "Set deal = 1, trick = 1, eldest = 1, multiplier = 1.",
    "The 12 card codes 0-11 are placed in the table list deck."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when trick = 1] Shuffle deck once. Give positions 1-4 to seat 1's hand, 5-8 to seat 2's hand and 9-12 to seat 3's hand. Set declarer_points = 0, defender_points = 0, multiplier = 1, trick_cards = [], trick_seats = []."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "[when trick = 1] Each player is sent their own hand and the public state."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "eldest: one of the 20 bids 'N S' (N in 50,60,70,80,90; S in H,B,L,A); others: 'PASS' or one of the 20 bids",
      "effect": "[when trick = 1] Set each player's bid. If the eldest answers PASS or an invalid bid, it becomes '50 A'. An invalid answer from any other player becomes 'PASS'. Set bid_value = N, or 0 for PASS."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when trick = 1] The declarer is the seat with the highest value of bid_value*10 + (3 - ((seat - eldest) mod 3)), so ties go to the seat first in order from the eldest. Set contract = that seat's N, trump = that seat's suit index, base_stake = contract/10 - 4, leader = declarer. Announce all bids, the declarer, the contract and the trump."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "defenders: FLEK or NO; declarer: RE or NO",
      "effect": "[when trick = 2] Set each player's flek_answer. An invalid answer counts as NO."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when trick = 2] If at least one defender has flek_answer = FLEK, multiplier = multiplier x 2. If, in addition, the declarer's flek_answer = RE, multiplier = multiplier x 2 again. Announce all answers and the multiplier."
    },
    {
      "action": "ask",
      "who": "the seat equal to leader",
      "answer": "a card from their hand",
      "effect": "The named card is recorded."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If the named card is not in the leader's hand, use the lowest code in that hand instead. Remove the card from the hand. Append it to trick_cards and append leader to trick_seats. Set led_suit = floor(card/3), best_key = (card mod 3) + (10 if floor(card/3) = trump) + 5, best_seat = leader. Announce the card."
    },
    {
      "action": "ask",
      "who": "the seat (leader mod 3)+1",
      "answer": "a card from their hand",
      "effect": "The named card is recorded."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "The card is legal if its suit = led_suit; or the hand has no led_suit card and its suit = trump; or the hand has neither led_suit cards nor trumps. If it is not held or not legal, use the lowest-code held led_suit card, else the lowest-code held trump, else the lowest-code held card. Remove it from the hand and append it to trick_cards and the seat to trick_seats. key = (card mod 3) + (10 if suit = trump) + (5 if suit = led_suit). If key > best_key, set best_key = key and best_seat = this seat. Announce the card."
    },
    {
      "action": "ask",
      "who": "the seat ((leader mod 3)+1) mod 3 + 1",
      "answer": "a card from their hand",
      "effect": "The named card is recorded."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Same as the second-card resolution, for this seat."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Trick points = sum over trick_cards of (10 if card mod 3 >= 1 else 0), plus 10 if trick = 4. If best_seat = declarer, add them to declarer_points, otherwise to defender_points. Set leader = best_seat, then clear trick_cards and trick_seats. Announce the trick winner, declarer_points and defender_points."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "[when trick = 4] stake = base_stake x multiplier x (2 if trump = 0 else 1). If declarer_points >= contract: the declarer's score += 2 x stake and each defender's score -= stake. Otherwise: the declarer's score -= 2 x stake and each defender's score += stake. Announce the result and the scores."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "trick += 1. If trick > 4: trick = 1, deal += 1, eldest = ((deal-1) mod 3)+1, and every player's bid is reset to '', bid_value to 0 and flek_answer to 'NO'."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the match if deal > 9, otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "deal > 9",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their score, the sum of the zero-sum deal settlements over 9 deals. The highest score wins, and players tied at the top draw by sharing the win."
  },
  "rules": [
    {
      "id": "R1",
      "text": "There are 12 cards, codes 0-11, with suit = floor(code/3) (H=0, B=1, L=2, A=3) and rank = code mod 3 (K=0, 10=1, A=2), and the rank order within a suit is A > 10 > K."
    },
    {
      "id": "R2",
      "text": "When a trick is awarded, each Ace and each Ten in it is worth 10 points and each King 0."
    },
    {
      "id": "R3",
      "text": "When trick 4 of a deal is awarded, its winner's side gets 10 extra points, so a deal totals 90 points."
    },
    {
      "id": "R4",
      "text": "The match is 9 deals of 4 tricks (36 rounds), and the eldest of deal d is seat ((d-1) mod 3)+1."
    },
    {
      "id": "R5",
      "text": "When trick 1 of a deal begins, the 12 codes are shuffled and positions 1-4 go to seat 1, 5-8 to seat 2 and 9-12 to seat 3, and declarer_points, defender_points and multiplier are reset to 0, 0 and 1."
    },
    {
      "id": "R6",
      "text": "When bidding at trick 1, every player answers secretly and at the same time with PASS or 'N S', where N is in {50,60,70,80,90} and S is in {H,B,L,A}."
    },
    {
      "id": "R7",
      "text": "When the eldest answers PASS or an invalid bid, it counts as '50 A'."
    },
    {
      "id": "R8",
      "text": "When a non-eldest player gives an invalid bid, it counts as PASS."
    },
    {
      "id": "R9",
      "text": "When bids are resolved, the highest N becomes the declarer with contract N and trump S, and on a tie the tied seat first in seat order starting from the eldest wins."
    },
    {
      "id": "R10",
      "text": "When the declarer is set, base_stake = N/10 - 4 (50\u21921, 60\u21922, 70\u21923, 80\u21924, 90\u21925), and the declarer leads trick 1."
    },
    {
      "id": "R11",
      "text": "When bids are resolved, all bids, the declarer, the contract and the trump are announced."
    },
    {
      "id": "R12",
      "text": "When the flek poll runs at trick 2, defenders answer FLEK or NO and the declarer answers RE or NO, all at the same time, and invalid answers count as NO."
    },
    {
      "id": "R13",
      "text": "When at least one defender says FLEK, the multiplier doubles to 2."
    },
    {
      "id": "R14",
      "text": "When at least one defender says FLEK and the declarer says RE, the multiplier becomes 4."
    },
    {
      "id": "R15",
      "text": "When no defender says FLEK, the multiplier stays 1, even if the declarer says RE."
    },
    {
      "id": "R16",
      "text": "When the leader names a card not in their hand, their lowest-code card is played instead."
    },
    {
      "id": "R17",
      "text": "When the first card is played, led_suit = its suit, best_key = rank + (10 if trump) + 5, and best_seat = the leader."
    },
    {
      "id": "R18",
      "text": "When a following player plays, the card must be of the led suit; failing that a trump; failing both, any card."
    },
    {
      "id": "R19",
      "text": "When a following player names an illegal or unheld card, the lowest-code held led-suit card is played, else the lowest-code held trump, else the lowest-code held card."
    },
    {
      "id": "R20",
      "text": "When a following card's key = rank + (10 if trump) + (5 if led suit) exceeds best_key, that seat becomes best_seat."
    },
    {
      "id": "R21",
      "text": "When a trick is awarded, its points go to declarer_points if best_seat is the declarer, otherwise to defender_points, and best_seat leads the next trick."
    },
    {
      "id": "R22",
      "text": "When a deal is settled, stake = base_stake x multiplier x (2 if trump is Hearts, else 1)."
    },
    {
      "id": "R23",
      "text": "When declarer_points >= contract at settlement, the declarer gains 2 x stake and each defender loses stake."
    },
    {
      "id": "R24",
      "text": "When declarer_points < contract at settlement, the declarer loses 2 x stake and each defender gains stake."
    },
    {
      "id": "R25",
      "text": "When deal 9's trick 4 has been settled, the match ends and the highest score wins, with players tied at the top drawing."
    }
  ],
  "offers": [
    {
      "question": "Bid (trick 1)",
      "who": "all players at once",
      "options": "the eldest: the 20 bids '50 H' \u2026 '90 A' (no PASS); any other seat: PASS plus the 20 bids"
    },
    {
      "question": "Flek poll (trick 2)",
      "who": "all players at once",
      "options": "the declarer: RE, NO; each defender: FLEK, NO"
    },
    {
      "question": "First card",
      "who": "the leader",
      "options": "every card in the leader's hand"
    },
    {
      "question": "Second card / third card",
      "who": "the next seat clockwise, then the one after",
      "options": "the cards in that hand of the led suit; if none, the trumps held; if neither, every card held"
    }
  ],
  "choices": [
    {
      "what": "3 players (min = max = suggested = 3)",
      "why": "The designer fixed 3. The game is built on one declarer against two defenders, and the 12-card deck deals exactly 4 to each of 3 seats."
    },
    {
      "what": "No talk step",
      "why": "The rules say there is no discussion phase. Strategy lies in bidding to hand strength, choosing trump, fleking against overbids and card play."
    },
    {
      "what": "Bid tie-break computed as bid_value*10 + (3 - ((seat - eldest) mod 3))",
      "why": "This is an arithmetic form of 'first in seat order starting from the eldest'."
    },
    {
      "what": "Bids, flek answers and the trick list are reset in the advance step",
      "why": "The source leaves the moment of resetting these working values unstated."
    }
  ],
  "simplifications": [
    {
      "what": "Players are offered only legal options (no PASS for the eldest, only legal cards to follow)",
      "why": "A seat is never offered what it may not do. The source's fallback rules for invalid or illegal answers are kept in the effects anyway."
    },
    {
      "what": "Steps for trick 1, trick 2 and trick 4 are single steps with a 'when trick = k' condition",
      "why": "The step list is flat, and each conditional part is a single step, so no block branching is needed."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: deal, declarer, contract, trump, multiplier.
````

## Reply

````
```json
[
  {
    "name": "Rank order A > 10 > K within a suit: the Ace played third wins the trick",
    "rule": "R1",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [6]}, "2": {"hand": [7]}, "3": {"hand": [8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 3, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 20, "defender_points": 40, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": -1}, "2": {"score": -1}, "3": {"score": 2}}}
  },
  {
    "name": "Ace and Ten count 10 each, King 0: declarer reaches exactly 80",
    "rule": "R2",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11]}, "2": {"hand": [0]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 80, "trump": 3, "base_stake": 4, "multiplier": 1, "declarer_points": 50, "defender_points": 10, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 8}, "2": {"score": -4}, "3": {"score": -4}}}
  },
  {
    "name": "Last trick bonus of 10 makes the declarer reach the contract exactly",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11]}, "2": {"hand": [0]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 70, "trump": 3, "base_stake": 3, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 6}, "2": {"score": -3}, "3": {"score": -3}}}
  },
  {
    "name": "After trick 4 the next deal starts and seat 2 is eldest (no PASS for seat 2)",
    "rule": "R4",
    "players": 3,
    "rounds": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11]}, "2": {"hand": [0]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {
      "game": {"deal": 2},
      "players": {"1": {"score": 2}, "2": {"score": -1}, "3": {"score": -1}},
      "offered": [{"seat": 1, "option": "PASS"}, {"seat": 3, "option": "PASS"}],
      "not_offered": [{"seat": 2, "option": "PASS"}]
    }
  },
  {
    "name": "A new deal resets the multiplier to 1",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {"game": {"deal": 1, "eldest": 1, "trick": 1, "multiplier": 4}},
    "rules": [],
    "expect": {"game": {"multiplier": 1, "deal": 1}}
  },
  {
    "name": "Bid options: non-eldest seats may PASS or bid any of the 20 bids",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "50 H"}],
    "expect": {
      "offered": [{"seat": 2, "option": "PASS"}, {"seat": 2, "option": "90 A"}, {"seat": 3, "option": "PASS"}, {"seat": 3, "option": "50 H"}, {"seat": 1, "option": "90 A"}]
    }
  },
  {
    "name": "The eldest is not offered PASS",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "50 A"}],
    "expect": {
      "game": {"declarer": 1, "contract": 50, "trump": 3},
      "not_offered": [{"seat": 1, "option": "PASS"}]
    }
  },
  {
    "name": "Highest bid wins: 70 L beats 60 B, the third seat passes",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "60 B"}, {"seat": 2, "options_include": "70 L"}],
    "expect": {"game": {"declarer": 2, "contract": 70, "trump": 2}}
  },
  {
    "name": "Tie between seats 2 and 3 goes to seat 2 (first after the eldest)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "50 A"}, {"seat": 2, "options_include": "80 H"}, {"seat": 3, "options_include": "80 H"}],
    "expect": {"game": {"declarer": 2, "contract": 80, "trump": 0}}
  },
  {
    "name": "Tie involving the eldest goes to the eldest",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "70 A"}, {"seat": 3, "options_include": "70 H"}],
    "expect": {"game": {"declarer": 1, "contract": 70, "trump": 3}}
  },
  {
    "name": "With seat 2 eldest, a tie between seats 1 and 3 goes to seat 3",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {"game": {"deal": 2, "eldest": 2, "trick": 1}},
    "rules": [{"seat": 2, "options_include": "50 H"}, {"seat": 1, "options_include": "60 B"}, {"seat": 3, "options_include": "60 L"}],
    "expect": {"game": {"declarer": 3, "contract": 60, "trump": 2}}
  },
  {
    "name": "A 90 bid sets contract 90 with the declarer's trump",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "60 H"}, {"seat": 2, "options_include": "80 B"}, {"seat": 3, "options_include": "90 A"}],
    "expect": {"game": {"declarer": 3, "contract": 90, "trump": 3}}
  },
  {
    "name": "Bid resolution publishes the declarer, contract and trump",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "rules": [{"seat": 1, "options_include": "50 B"}, {"seat": 3, "options_include": "60 H"}],
    "expect": {"game": {"declarer": 3, "contract": 60, "trump": 0}}
  },
  {
    "name": "Flek poll: declarer offered RE/NO, defenders FLEK/NO",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0, 1, 2]}, "2": {"hand": [3, 4, 5]}, "3": {"hand": [6, 7, 8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 2, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 0, "defender_points": 0, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {
      "game": {"multiplier": 1},
      "offered": [{"seat": 1, "option": "RE"}, {"seat": 1, "option": "NO"}, {"seat": 2, "option": "FLEK"}, {"seat": 3, "option": "FLEK"}],
      "not_offered": [{"seat": 1, "option": "FLEK"}, {"seat": 2, "option": "RE"}, {"seat": 3, "option": "RE"}]
    }
  },
  {
    "name": "One defender FLEK doubles the multiplier to 2",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0, 1, 2]}, "2": {"hand": [3, 4, 5]}, "3": {"hand": [6, 7, 8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 2, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 0, "defender_points": 0, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [{"seat": 2, "options_include": "FLEK"}],
    "expect": {"game": {"multiplier": 2}}
  },
  {
    "name": "FLEK plus RE makes the multiplier 4",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0, 1, 2]}, "2": {"hand": [3, 4, 5]}, "3": {"hand": [6, 7, 8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 2, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 0, "defender_points": 0, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [{"seat": 3, "options_include": "FLEK"}, {"seat": 1, "options_include": "RE"}],
    "expect": {"game": {"multiplier": 4}}
  },
  {
    "name": "Both defenders FLEK and declarer RE still give multiplier 4",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0, 1, 2]}, "2": {"hand": [3, 4, 5]}, "3": {"hand": [6, 7, 8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 2, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 0, "defender_points": 0, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [{"seat": 2, "options_include": "FLEK"}, {"seat": 3, "options_include": "FLEK"}, {"seat": 1, "options_include": "RE"}],
    "expect": {"game": {"multiplier": 4}}
  },
  {
    "name": "RE without any FLEK leaves the multiplier at 1",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0, 1, 2]}, "2": {"hand": [3, 4, 5]}, "3": {"hand": [6, 7, 8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 2, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 0, "defender_points": 0, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [{"seat": 1, "options_include": "RE"}],
    "expect": {"game": {"multiplier": 1}}
  },
  {
    "name": "Led King of Hearts beats off-suit Aces (led-suit bonus)",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0]}, "2": {"hand": [5]}, "3": {"hand": [8]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 20, "defender_points": 40, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 2}, "2": {"score": -1}, "3": {"score": -1}}}
  },
  {
    "name": "A follower void in the led suit must trump rather than discard",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "last",
    "given": {
      "players": {"1": {"hand": [2]}, "2": {"hand": [9, 3]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 2, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 20, "defender_points": 40, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": -1}, "2": {"score": 2}, "3": {"score": -1}}}
  },
  {
    "name": "A follower holding the led suit must follow and may not trump",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": [2]}, "2": {"hand": [9, 1]}, "3": {"hand": [0]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 20, "defender_points": 40, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 2}, "2": {"score": -1}, "3": {"score": -1}}}
  },
  {
    "name": "A trump King beats the led Ace",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [2]}, "2": {"hand": [9]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 2, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 20, "defender_points": 40, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": -1}, "2": {"score": 2}, "3": {"score": -1}}}
  },
  {
    "name": "A trick won by a defender goes to the defenders, so the declarer falls short",
    "rule": "R21",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [0]}, "2": {"hand": [2]}, "3": {"hand": [5]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 60, "trump": 3, "base_stake": 2, "multiplier": 1, "declarer_points": 50, "defender_points": 10, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": -4}, "2": {"score": 2}, "3": {"score": 2}}}
  },
  {
    "name": "Stake = base 3 x multiplier 4 x 2 for Hearts = 24",
    "rule": "R22",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [2]}, "2": {"hand": [3]}, "3": {"hand": [4]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 70, "trump": 0, "base_stake": 3, "multiplier": 4, "declarer_points": 50, "defender_points": 10, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 48}, "2": {"score": -24}, "3": {"score": -24}}}
  },
  {
    "name": "A made contract: declarer +2 x stake, each defender -stake",
    "rule": "R23",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11]}, "2": {"hand": [0]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": 2}, "2": {"score": -1}, "3": {"score": -1}}}
  },
  {
    "name": "A failed contract (70 < 80): declarer -2 x stake, each defender +stake",
    "rule": "R24",
    "players": 3,
    "rounds": 1,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11]}, "2": {"hand": [0]}, "3": {"hand": [1]}},
      "game": {"deal": 1, "eldest": 1, "trick": 4, "declarer": 1, "contract": 80, "trump": 3, "base_stake": 4, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {"players": {"1": {"score": -8}, "2": {"score": 4}, "3": {"score": 4}}}
  },
  {
    "name": "Match ends after deal 9 and the highest score wins",
    "rule": "R25",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11], "score": 5}, "2": {"hand": [0], "score": 3}, "3": {"hand": [1], "score": -8}},
      "game": {"deal": 9, "eldest": 3, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 7, "2": 2, "3": -9},
      "game": {"deal": 10}
    }
  },
  {
    "name": "Players tied at the top after deal 9 share the win",
    "rule": "R25",
    "players": 3,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"hand": [11], "score": 3}, "2": {"hand": [0], "score": 6}, "3": {"hand": [1], "score": -9}},
      "game": {"deal": 9, "eldest": 3, "trick": 4, "declarer": 1, "contract": 50, "trump": 3, "base_stake": 1, "multiplier": 1, "declarer_points": 40, "defender_points": 20, "leader": 1, "trick_cards": [], "trick_seats": []}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 5, "2": 5, "3": -10}
    }
  }
]
```
````
