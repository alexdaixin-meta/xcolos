# 06 scenarios

- time: 2026-10-28T02:28:58+00:00 (214.1s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 9a735f5917cd2b56, reply sha256 377ed7db908b0d75

## Sent

````
SPEC:
{
  "name": "Little Bidding Mari\u00e1\u0161",
  "summary": "Three-player trick-taking game over 6 deals of 6 tricks: one simultaneous bid picks a declarer and trump, marriages are announced, and the declarer plays alone against two defenders to reach the contract.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "card_count": 20,
    "suit_count": 4,
    "ranks_per_suit": 5,
    "suit_code_multiplier": 5,
    "hand_size": 6,
    "talon_size": 2,
    "tricks_per_deal": 6,
    "deals": 6,
    "total_rounds": 36,
    "ace_points": 10,
    "ten_points": 10,
    "last_trick_bonus": 10,
    "deal_card_points_total": 90,
    "min_bid": 50,
    "max_bid": 150,
    "bid_step": 10,
    "eldest_forced_bid": 50,
    "trump_marriage_value": 40,
    "plain_marriage_value": 20,
    "contract_offset": 40,
    "contract_divisor": 10,
    "hearts_multiplier": 2,
    "declarer_score_multiplier": 2,
    "defender_score_multiplier": 1,
    "trump_key_bonus": 10,
    "led_suit_key_bonus": 5,
    "starting_score": 0,
    "min_tricks_for_marriages": 1
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match score, the sum of the deal settlements so far.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card codes (suit*5+rank) held privately. 6 are dealt each deal and one is removed per trick.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "text",
        "visible": "public",
        "initial": "PASS",
        "meaning": "This deal's bid: PASS or 50..150 in steps of 10. Submitted in a simultaneous poll and revealed together.",
        "observable": false
      },
      {
        "key": "bid_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Suit named with the bid: Hearts, Bells, Leaves or Acorns.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Round (trick) counter, 1..36. deal = floor((round-1)/6)+1, trick = (round-1)%6+1, eldest seat = ((deal-1)%3)+1.",
        "observable": true
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "codes 0..19",
        "meaning": "The full 20-card pack that each deal is shuffled and dealt from.",
        "observable": false
      },
      {
        "key": "talon",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 2 undealt cards, face down and out of play for the deal.",
        "observable": false
      },
      {
        "key": "declarer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this deal's declarer.",
        "observable": true
      },
      {
        "key": "contract",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Contract T, the declarer's winning bid.",
        "observable": true
      },
      {
        "key": "trump",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Trump suit, the declarer's bid suit.",
        "observable": true
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that leads the current trick.",
        "observable": false
      },
      {
        "key": "trick_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played to the current trick, in play order starting with the leader.",
        "observable": false
      },
      {
        "key": "declarer_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points won by the declarer this deal, including the last-trick 10.",
        "observable": true
      },
      {
        "key": "defender_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card points won by the defenders together this deal.",
        "observable": true
      },
      {
        "key": "declarer_tricks",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won by the declarer this deal. Defender tricks = tricks completed - declarer_tricks.",
        "observable": false
      },
      {
        "key": "declarer_marriages",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total marriage value held by the declarer.",
        "observable": false
      },
      {
        "key": "defender_marriages",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total marriage value held by the two defenders.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat the players as P1, P2 and P3. Seat order is cyclic.",
    "Set every score to 0 and round to 1.",
    "Fill the deck with the 20 card codes 0..19 (suit*5+rank; Hearts=0, Bells=1, Leaves=2, Acorns=3; U=0, O=1, K=2, 10=3, A=4).",
    "Players may not exchange messages at any time, so the game has no talk step."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when (round-1)%6==0] Return all cards to the deck. Draw 6 cards at random from the deck into each player's hand and the remaining 2 into talon (hidden). Set declarer_points=0, defender_points=0, declarer_tricks=0, trick_cards=[]."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "[when (round-1)%6==0] Each player privately sees their own hand, named by card names (e.g. 'Ten of Leaves')."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "One choice of 'BID SUIT', where BID is PASS or 50,60,...,150 and SUIT is Hearts, Bells, Leaves or Acorns. The eldest is not offered PASS.",
      "effect": "[when (round-1)%6==0] Sets bid and bid_suit for every player. No answer is seen until all are in."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when (round-1)%6==0] A bid not in the list becomes PASS. An eldest PASS or invalid bid becomes 50. A missing or invalid suit becomes the suit with the most cards in that player's hand, ties broken by Hearts, Bells, Leaves, Acorns. declarer = the seat with the maximum of bidvalue*10 + (3 - ((seat - eldest) mod 3)), with PASS = 0. Set contract = declarer's bid, trump = declarer's bid_suit, leader = declarer."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "[when (round-1)%6==0] For each player and each suit s where both codes s*5+2 (K) and s*5+1 (O) are in hand, the marriage is worth 40 if s is trump, else 20. declarer_marriages = the sum for the declarer. defender_marriages = the sum for the two other seats."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "[when (round-1)%6==0] Announce all bids and suits, the declarer, the contract, the trump, and every marriage with its holder and value."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Set trick_cards = []."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "One card from own hand, chosen by name.",
      "effect": "The chosen card is the lead."
    },
    {
      "action": "update",
      "who": "seat leader",
      "answer": null,
      "effect": "If the card is not in hand, use the lowest-rank card in hand, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it to all."
    },
    {
      "action": "ask",
      "who": "seat leader%3+1",
      "answer": "One card from own hand, chosen by name (offered the legal cards).",
      "effect": "The chosen card is this seat's play."
    },
    {
      "action": "update",
      "who": "seat leader%3+1",
      "answer": null,
      "effect": "If the card is illegal or not in hand, play the legal card of lowest rank, ties broken by suit order. Remove it from hand, append it to trick_cards, and announce it.",
      "judged": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."
    },
    {
      "action": "ask",
      "who": "seat (leader+1)%3+1",
      "answer": "One card from own hand, chosen by name (offered the legal cards).",
      "effect": "The chosen card is this seat's play."
    },
    {
      "action": "update",
      "who": "seat (leader+1)%3+1",
      "answer": null,
      "effect": "Validate as in the second player's step, using the fallback if needed. Remove the card from hand, append it to trick_cards, and announce it.",
      "judged": "The named card is in the player's hand and obeys the rules: follow the led suit and beat the highest led-suit card if possible (the beating duty is lifted when the led suit is not trump and a trump is already in the trick); otherwise play a trump that beats the highest trump if possible; otherwise any card."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Each card's key = rank + 10*(suit==trump) + 5*(suit==led suit). The winner is the seat that played the maximum key, the i-th card belonging to seat ((leader-1+i)%3)+1. points = 10 per Ace or Ten in trick_cards, +10 if (round-1)%6==5. If winner==declarer, add points to declarer_points and 1 to declarer_tricks; otherwise add points to defender_points. Set leader = winner. Announce the winner, declarer_points and defender_points."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "[when (round-1)%6==5] tally = declarer_points + (declarer_tricks>=1 ? declarer_marriages : 0) - ((6-declarer_tricks)>=1 ? defender_marriages : 0). S = (contract-40)/10. If tally < contract, S = -(S+1). If trump == Hearts, S = 2*S. The declarer's score += 2*S; each defender's score -= S."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "[when (round-1)%6==5] Announce the tally, whether the contract was made, and all scores."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the match if round > 36; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round > 36",
    "rank_by": "you.score",
    "decided_by": "After 6 deals (36 tricks), the player with the highest total score wins. Players tied at the top share the result."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a deal starts (round 1, 7, 13, 19, 25, 31), then each player receives 6 hidden cards and 2 cards go to the talon, which is out of play."
    },
    {
      "id": "R2",
      "text": "When a deal starts, then declarer_points, defender_points and declarer_tricks are reset to 0."
    },
    {
      "id": "R3",
      "text": "When the deal is d, then the eldest is seat ((d-1)%3)+1: P1 in deals 1 and 4, P2 in deals 2 and 5, P3 in deals 3 and 6."
    },
    {
      "id": "R4",
      "text": "When bidding, then all players submit a bid and suit simultaneously and all are revealed together."
    },
    {
      "id": "R5",
      "text": "When a bid is not one of PASS, 50, 60, ..., 150, then it counts as PASS."
    },
    {
      "id": "R6",
      "text": "When the eldest passes or bids invalidly, then the eldest's bid counts as 50."
    },
    {
      "id": "R7",
      "text": "When a suit is missing or invalid, then it becomes the suit in which that player holds the most cards, ties broken by Hearts, Bells, Leaves, Acorns."
    },
    {
      "id": "R8",
      "text": "When bids are compared, then the highest bid wins; on a tie the eldest wins, then the next seat after the eldest."
    },
    {
      "id": "R9",
      "text": "When the declarer is set, then contract equals the declarer's bid, trump equals the declarer's suit, and the declarer leads trick 1."
    },
    {
      "id": "R10",
      "text": "When a player holds the K and O of one suit, then that is a marriage worth 40 in trump and 20 otherwise, credited to the holder's side and publicly announced."
    },
    {
      "id": "R11",
      "text": "When a later player holds a card of the led suit, then they must play that suit and beat the highest led-suit card in the trick if they can, unless the led suit is not trump and a trump is already in the trick."
    },
    {
      "id": "R12",
      "text": "When a later player has no card of the led suit but holds a trump, then they must play a trump that beats the highest trump in the trick if they can."
    },
    {
      "id": "R13",
      "text": "When a later player has neither the led suit nor a trump, then they may play any card."
    },
    {
      "id": "R14",
      "text": "When a player names an illegal card or one not in their hand, then the engine plays their legal card of lowest rank, ties broken by suit order."
    },
    {
      "id": "R15",
      "text": "When a trick is complete, then the card with the highest key (rank + 10 if trump + 5 if of the led suit) wins."
    },
    {
      "id": "R16",
      "text": "When a trick is won, then its Aces and Tens score 10 each to the winner's side, plus 10 if it is the 6th trick of the deal."
    },
    {
      "id": "R17",
      "text": "When a trick is won, then the winner leads the next trick."
    },
    {
      "id": "R18",
      "text": "When a deal ends, then tally = declarer_points + declarer_marriages (if the declarer won at least 1 trick) - defender_marriages (if the defenders won at least 1 trick)."
    },
    {
      "id": "R19",
      "text": "When a deal ends with tally >= contract, then S = (contract-40)/10. For example, a 50 contract that is made gives S = 1."
    },
    {
      "id": "R20",
      "text": "When a deal ends with tally < contract, then S = -((contract-40)/10 + 1). For example, a failed 50 contract gives S = -2."
    },
    {
      "id": "R21",
      "text": "When trump is Hearts, then S is doubled."
    },
    {
      "id": "R22",
      "text": "When a deal is settled, then the declarer's score changes by 2*S and each defender's score changes by -S."
    },
    {
      "id": "R23",
      "text": "When round 36 is complete, then the match ends and the highest score wins; a tie at the top is shared."
    }
  ],
  "offers": [
    {
      "question": "Bid and suit poll",
      "who": "all players",
      "options": "The eldest: each of 50,60,...,150 combined with each of Hearts, Bells, Leaves, Acorns (44 options). Any other seat: those 44 plus PASS with each suit (48 options)."
    },
    {
      "question": "Leader's card",
      "who": "seat leader",
      "options": "Every card in the leader's hand."
    },
    {
      "question": "Second and third player's card",
      "who": "the two non-leading seats",
      "options": "Only the cards in hand that are legal under the follow/beat/trump rules. With no led suit and no trump in hand, every card in hand."
    }
  ],
  "choices": [
    {
      "what": "3 players exactly",
      "why": "The designer fixed 3 seats: a lone declarer against a two-defender team, with 20 cards dealt 6-6-6 plus a 2-card talon. No other count works with this pack."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid all messages; defenders cooperate only through their card play."
    },
    {
      "what": "Bid and suit as one combined choice",
      "why": "The rules ask for one answer holding both. A combined list keeps it to one simultaneous poll."
    },
    {
      "what": "Eldest not offered PASS",
      "why": "The eldest may not pass. The rule still maps an eldest PASS to 50 if one arrives."
    },
    {
      "what": "Card plays use ask, in seat order",
      "why": "Trick play is sequential and each player sees the earlier cards."
    },
    {
      "what": "Strategy",
      "why": "Bid to the hand's strength including marriages, choose trump (Hearts doubles the stakes), and as defenders signal through play and save Aces and Tens for each other."
    }
  ],
  "simplifications": [
    {
      "what": "Legality of a played card is judged by a referee sentence; the fallback card is then computed",
      "why": "The follow/beat/trump rule is long to express as plain arithmetic in one step."
    },
    {
      "what": "A tie for top score is a shared win rather than a named draw",
      "why": "The engine has no separate draw; players level at the top share the win, which matches no single winner."
    },
    {
      "what": "Deal-start and deal-end steps carry a when-condition on the round counter",
      "why": "The step list is flat; per-step conditions reproduce the [trick 1] and [trick 6] markers."
    },
    {
      "what": "Added a hidden deck list",
      "why": "Dealing needs a list to draw from."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: round, declarer, contract, trump, declarer_points, defender_points.
````

## Reply

````
```json
[
  {"name": "Deal start: each seat gets 6 cards and 2 go to the talon (one trick later each hand holds 5; random cards not asserted)", "rule": "R1", "players": 3, "seed": 1, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"game": {"round": 2},
              "lens": {"game": {"talon": 2}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}}},

  {"name": "A new deal starts at round 7: hands and talon are dealt again (random cards and points not asserted)", "rule": "R2", "players": 3, "seed": 2, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 7, "declarer_points": 500, "defender_points": 500, "declarer_tricks": 6, "trick_cards": []},
             "players": {"1": {"hand": []}, "2": {"hand": []}, "3": {"hand": []}}},
   "rules": [{"seat": 2, "options_include": "60 Leaves"}],
   "expect": {"game": {"round": 8, "declarer": 2, "contract": 60, "trump": "Leaves"},
              "lens": {"game": {"talon": 2}, "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}}}}},

  {"name": "Deal 2: P2 is eldest, cannot pass and wins a three-way tie", "rule": "R3", "players": 3, "seed": 3, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 7}},
   "rules": [{"seat": 1, "options_include": "80 Acorns"},
             {"seat": 2, "options_include": "80 Acorns"},
             {"seat": 3, "options_include": "80 Acorns"}],
   "expect": {"game": {"declarer": 2, "contract": 80, "trump": "Acorns"},
              "not_offered": [{"seat": 2, "option": "PASS Hearts"}],
              "offered": [{"seat": 1, "option": "PASS Hearts"}, {"seat": 3, "option": "PASS Hearts"}]}},

  {"name": "Deal 3: P3 is eldest and becomes declarer when the others pass", "rule": "R3", "players": 3, "seed": 4, "default": "decline", "rounds": 1,
   "given": {"game": {"round": 13}},
   "rules": [{"seat": 3, "options_include": "60 Leaves"}],
   "expect": {"game": {"declarer": 3, "contract": 60, "trump": "Leaves"},
              "not_offered": [{"seat": 3, "option": "PASS Hearts"}]}},

  {"name": "Simultaneous bids are revealed together and the highest bid declares", "rule": "R4", "players": 3, "seed": 5, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "50 Hearts"},
             {"seat": 2, "options_include": "70 Bells"},
             {"seat": 3, "options_include": "PASS Leaves"}],
   "expect": {"game": {"declarer": 2, "contract": 70, "trump": "Bells"},
              "not_offered": [{"seat": 1, "option": "PASS Hearts"}]}},

  {"name": "PASS bids count as no bid, so the eldest's 50 declares", "rule": "R5", "players": 3, "seed": 6, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "50 Leaves"},
             {"seat": 2, "options_include": "PASS Bells"},
             {"seat": 3, "options_include": "PASS Bells"}],
   "expect": {"game": {"declarer": 1, "contract": 50, "trump": "Leaves"}}},

  {"name": "The eldest is never offered PASS and declares when the others pass", "rule": "R6", "players": 3, "seed": 7, "default": "decline", "rounds": 1,
   "rules": [],
   "expect": {"game": {"declarer": 1},
              "not_offered": [{"seat": 1, "option": "PASS Hearts"}, {"seat": 1, "option": "PASS Bells"},
                              {"seat": 1, "option": "PASS Leaves"}, {"seat": 1, "option": "PASS Acorns"}]}},

  {"name": "Tie between non-eldest seats goes to the seat after the eldest", "rule": "R8", "players": 3, "seed": 8, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "50 Hearts"},
             {"seat": 2, "options_include": "90 Leaves"},
             {"seat": 3, "options_include": "90 Acorns"}],
   "expect": {"game": {"declarer": 2, "contract": 90, "trump": "Leaves"}}},

  {"name": "Tie with the eldest goes to the eldest", "rule": "R8", "players": 3, "seed": 9, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "100 Hearts"},
             {"seat": 2, "options_include": "PASS Bells"},
             {"seat": 3, "options_include": "100 Bells"}],
   "expect": {"game": {"declarer": 1, "contract": 100, "trump": "Hearts"}}},

  {"name": "Contract and trump are the declarer's bid and suit", "rule": "R9", "players": 3, "seed": 10, "default": "decline", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "60 Hearts"},
             {"seat": 2, "options_include": "80 Bells"},
             {"seat": 3, "options_include": "120 Acorns"}],
   "expect": {"game": {"declarer": 3, "contract": 120, "trump": "Acorns"}}},

  {"name": "A trump marriage of 40 is credited to the declarer's tally (Hearts 60 made, S=2 doubled)", "rule": "R10", "players": 3, "seed": 11, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 1, "contract": 60, "trump": "Hearts", "leader": 1, "trick_cards": [],
                      "declarer_points": 20, "defender_points": 20, "declarer_tricks": 2, "declarer_marriages": 40, "defender_marriages": 0},
             "players": {"1": {"hand": [4], "score": 0}, "2": {"hand": [9], "score": 0}, "3": {"hand": [8], "score": 0}}},
   "rules": [],
   "expect": {"game": {"round": 7, "declarer_points": 50},
              "players": {"1": {"score": 8}, "2": {"score": -4}, "3": {"score": -4}}}},

  {"name": "Must follow the led suit and beat it: Ace of Leaves forced, off-suit cards not offered", "rule": "R11", "players": 3, "seed": 12, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 1, "contract": 50, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [12]}, "2": {"hand": [14, 3]}, "3": {"hand": [13, 4]}}},
   "rules": [],
   "expect": {"game": {"round": 3, "declarer_points": 0, "defender_points": 20},
              "not_offered": [{"seat": 2, "option": "Ten of Hearts"}, {"seat": 3, "option": "Ace of Hearts"}]}},

  {"name": "The beating duty is lifted when a trump is already on a non-trump lead", "rule": "R11", "players": 3, "seed": 13, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 1, "contract": 50, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [12]}, "2": {"hand": [15]}, "3": {"hand": [14, 13]}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 0, "defender_points": 10},
              "offered": [{"seat": 3, "option": "Ten of Leaves"}, {"seat": 3, "option": "Ace of Leaves"}]}},

  {"name": "Void in the led suit: must trump and overtrump the highest trump", "rule": "R12", "players": 3, "seed": 14, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 3, "contract": 50, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [14]}, "2": {"hand": [18, 4]}, "3": {"hand": [19, 15, 3]}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 30, "defender_points": 0},
              "not_offered": [{"seat": 2, "option": "Ace of Hearts"}, {"seat": 3, "option": "Ten of Hearts"}]}},

  {"name": "With neither the led suit nor a trump, any card may be played", "rule": "R13", "players": 3, "seed": 15, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 2, "contract": 50, "trump": "Acorns", "leader": 2, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [4]}, "2": {"hand": [14]}, "3": {"hand": [3, 9]}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 30, "defender_points": 0},
              "offered": [{"seat": 3, "option": "Ten of Hearts"}, {"seat": 3, "option": "Ace of Bells"}]}},

  {"name": "A low trump beats the Ace of the led suit (highest key wins)", "rule": "R15", "players": 3, "seed": 16, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 1, "contract": 50, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [14]}, "2": {"hand": [15]}, "3": {"hand": [13]}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 0, "defender_points": 20}}},

  {"name": "Last trick scores its Aces and Tens plus the 10 bonus; 50 Bells made", "rule": "R16", "players": 3, "seed": 17, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 1, "contract": 50, "trump": "Bells", "leader": 1, "trick_cards": [],
                      "declarer_points": 40, "defender_points": 30, "declarer_tricks": 3, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [14], "score": 0}, "2": {"hand": [3], "score": 0}, "3": {"hand": [10], "score": 0}}},
   "rules": [],
   "expect": {"game": {"round": 7, "declarer_points": 70, "defender_points": 30},
              "players": {"1": {"score": 2}, "2": {"score": -1}, "3": {"score": -1}}}},

  {"name": "The trick winner leads the next trick", "rule": "R17", "players": 3, "seed": 18, "default": "decline", "rounds": 2,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 2, "declarer": 2, "contract": 50, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 0, "defender_points": 0, "declarer_tricks": 0},
             "players": {"1": {"hand": [14, 8]}, "2": {"hand": [15, 3]}, "3": {"hand": [13, 9]}}},
   "rules": [],
   "expect": {"game": {"round": 4, "declarer_points": 50, "defender_points": 0}}},

  {"name": "Tally adds the declarer's marriages and subtracts the defenders' (90 Leaves made exactly)", "rule": "R18", "players": 3, "seed": 19, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 2, "contract": 90, "trump": "Leaves", "leader": 2, "trick_cards": [],
                      "declarer_points": 50, "defender_points": 20, "declarer_tricks": 2, "declarer_marriages": 40, "defender_marriages": 20},
             "players": {"1": {"hand": [5], "score": 0}, "2": {"hand": [4], "score": 0}, "3": {"hand": [0], "score": 0}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 70},
              "players": {"1": {"score": -5}, "2": {"score": 10}, "3": {"score": -5}}}},

  {"name": "Defenders with no trick do not subtract their marriage (110 Acorns made)", "rule": "R18", "players": 3, "seed": 20, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 1, "contract": 110, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 70, "defender_points": 0, "declarer_tricks": 5, "declarer_marriages": 20, "defender_marriages": 20},
             "players": {"1": {"hand": [4], "score": 0}, "2": {"hand": [1], "score": 0}, "3": {"hand": [6], "score": 0}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 90},
              "players": {"1": {"score": 14}, "2": {"score": -7}, "3": {"score": -7}}}},

  {"name": "A made 70 contract gives S=3", "rule": "R19", "players": 3, "seed": 21, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 3, "contract": 70, "trump": "Leaves", "leader": 3, "trick_cards": [],
                      "declarer_points": 60, "defender_points": 0, "declarer_tricks": 3, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [18], "score": 10}, "2": {"hand": [5], "score": 5}, "3": {"hand": [19], "score": 0}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 90},
              "players": {"1": {"score": 7}, "2": {"score": 2}, "3": {"score": 6}}}},

  {"name": "A failed 50 contract gives S=-2", "rule": "R20", "players": 3, "seed": 22, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 1, "contract": 50, "trump": "Bells", "leader": 2, "trick_cards": [],
                      "declarer_points": 20, "defender_points": 40, "declarer_tricks": 1, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [0], "score": 0}, "2": {"hand": [4], "score": 0}, "3": {"hand": [3], "score": 0}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 20, "defender_points": 70},
              "players": {"1": {"score": -4}, "2": {"score": 2}, "3": {"score": 2}}}},

  {"name": "Hearts trump doubles S: a made 70 gives S=6", "rule": "R21", "players": 3, "seed": 23, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 3, "contract": 70, "trump": "Hearts", "leader": 3, "trick_cards": [],
                      "declarer_points": 60, "defender_points": 0, "declarer_tricks": 3, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [18], "score": 0}, "2": {"hand": [5], "score": 0}, "3": {"hand": [19], "score": 0}}},
   "rules": [],
   "expect": {"players": {"1": {"score": -6}, "2": {"score": -6}, "3": {"score": 12}}}},

  {"name": "Settlement: the declarer gains 2*S and each defender loses S, added to existing scores", "rule": "R22", "players": 3, "seed": 24, "default": "decline", "rounds": 1,
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 6, "declarer": 2, "contract": 60, "trump": "Acorns", "leader": 1, "trick_cards": [],
                      "declarer_points": 50, "defender_points": 20, "declarer_tricks": 2, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [12], "score": 3}, "2": {"hand": [14], "score": -2}, "3": {"hand": [11], "score": 5}}},
   "rules": [],
   "expect": {"game": {"declarer_points": 70},
              "players": {"1": {"score": 1}, "2": {"score": 2}, "3": {"score": 3}}}},

  {"name": "After round 36 the match ends and the highest score wins", "rule": "R23", "players": 3, "seed": 25, "default": "decline",
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 36, "declarer": 2, "contract": 50, "trump": "Bells", "leader": 2, "trick_cards": [],
                      "declarer_points": 60, "defender_points": 10, "declarer_tricks": 3, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [6], "score": 5}, "2": {"hand": [9], "score": 8}, "3": {"hand": [5], "score": 6}}},
   "rules": [],
   "expect": {"winner": 2,
              "standings": {"1": 4, "2": 10, "3": 5},
              "players": {"1": {"score": 4}, "2": {"score": 10}, "3": {"score": 5}}}},

  {"name": "Seats tied at the top after round 36 share the win", "rule": "R23", "players": 3, "seed": 26, "default": "decline",
   "judge": {"The named card is in the player's hand and obeys the rules": true},
   "given": {"game": {"round": 36, "declarer": 2, "contract": 50, "trump": "Bells", "leader": 2, "trick_cards": [],
                      "declarer_points": 60, "defender_points": 10, "declarer_tricks": 3, "declarer_marriages": 0, "defender_marriages": 0},
             "players": {"1": {"hand": [6], "score": 11}, "2": {"hand": [9], "score": 8}, "3": {"hand": [5], "score": 6}}},
   "rules": [],
   "expect": {"winner": [1, 2],
              "standings": {"1": 10, "2": 10, "3": 5},
              "players": {"1": {"score": 10}, "2": {"score": 10}, "3": {"score": 5}}}}
]
```
````
