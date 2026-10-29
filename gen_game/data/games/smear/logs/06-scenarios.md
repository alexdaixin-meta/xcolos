# 06 scenarios

- time: 2026-10-28T03:36:58+00:00 (139.8s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 87411e14fdeb5429, reply sha256 fbbd15d773770236

## Sent

````
SPEC:
{
  "name": "Pocket Smear",
  "summary": "A three-player trick-taking game of 9 four-trick deals: bid blind, the highest bidder names trump, then everyone fights for High, Low, Game and Three while the pitcher tries to make the contract.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "players": 3,
    "deals": 9,
    "tricks_per_deal": 4,
    "total_rounds": 36,
    "suits": 3,
    "ranks_per_suit": 8,
    "deck_size": 24,
    "hand_size": 4,
    "set_aside_cards": 12,
    "bid_min": 2,
    "bid_max": 6,
    "pass_value": 0,
    "all_pass_contract": 2,
    "card_points_rank_8": 4,
    "card_points_rank_7": 3,
    "card_points_rank_6": 2,
    "card_points_rank_5": 1,
    "card_points_other_ranks": 0,
    "high_points": 1,
    "low_points": 1,
    "game_points": 1,
    "three_points": 3,
    "three_rank": 3,
    "max_deal_points": 6,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total score. It may go negative.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held this deal, as codes suit*10+rank (Red=1, Blue=2, Green=3), so 18 is Red 8 and 23 is Blue 3.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bid amount this deal: 2 to 6, or 0 for PASS. It is revealed after the bid poll.",
        "observable": true
      },
      {
        "key": "bid_suit",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Suit named with the bid. It must be in the player's hand and is never revealed, except that the pitcher's suit becomes trump.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Card code played in the current trick, or 0 if none yet.",
        "observable": false
      },
      {
        "key": "captured",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards captured in tricks this deal.",
        "observable": false
      },
      {
        "key": "captured_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of card points in the captured pile this deal: rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0.",
        "observable": false
      },
      {
        "key": "deal_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Category points won in this deal, from 0 to 6.",
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
          16,
          17,
          18,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          31,
          32,
          33,
          34,
          35,
          36,
          37,
          38
        ],
        "meaning": "Undealt cards. It is rebuilt to all 24 cards at the start of each deal.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 12 cards set aside face down and unseen for the deal.",
        "observable": false
      },
      {
        "key": "rounds_played",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks completed so far, from 0 to 36.",
        "observable": false
      },
      {
        "key": "deal_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current deal, from 1 to 9.",
        "observable": true
      },
      {
        "key": "trick_in_deal",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current trick within the deal, from 1 to 4.",
        "observable": false
      },
      {
        "key": "dealer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Dealer seat: ((deal_number - 1) mod 3) + 1.",
        "observable": false
      },
      {
        "key": "pitcher",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the bid winner this deal.",
        "observable": true
      },
      {
        "key": "contract",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The pitcher's winning bid, or 2 if all passed.",
        "observable": true
      },
      {
        "key": "trump",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Trump suit code (1 Red, 2 Blue, 3 Green): the pitcher's named suit.",
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
        "key": "led_suit",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Suit code of the card led in the current trick.",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won the last trick.",
        "observable": false
      },
      {
        "key": "high_trump_rank",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Highest trump rank played this deal (0 = none yet).",
        "observable": false
      },
      {
        "key": "high_trump_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Seat that captured the highest trump played.",
        "observable": false
      },
      {
        "key": "low_trump_rank",
        "type": "number",
        "visible": "none",
        "initial": 9,
        "meaning": "Lowest trump rank played this deal (9 = none yet).",
        "observable": false
      },
      {
        "key": "low_trump_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Seat that captured the lowest trump played.",
        "observable": false
      },
      {
        "key": "three_seat",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Seat that captured the trump 3 this deal (0 = not played or not dealt).",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat the 3 players as Player 1, Player 2 and Player 3; seat order is 1, 2, 3, then back to 1.",
    "Set every score to 0, deal_number to 1, trick_in_deal to 1 and rounds_played to 0.",
    "Encode the 24 cards as suit*10+rank, with Red=1, Blue=2, Green=3 and ranks 1 to 8; they are shown to players as names such as 'Red 8'."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_deal == 1: dealer = ((deal_number - 1) mod 3) + 1; deck = all 24 card codes; for each player, clear hand, captured and played_card, and set captured_points = 0, deal_points = 0, bid = 0, bid_suit = ''; draw 4 cards at random from deck into each player's hand; move the remaining 12 deck cards into set_aside; reset high_trump_rank = 0, high_trump_seat = 0, low_trump_rank = 9, low_trump_seat = 0, three_seat = 0."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_deal == 1: each player sees their own hand, the dealer and every score."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "One choice from: 'PASS <suit>' or '<n> <suit>' for n in 2..6, where <suit> is any suit present in the player's own hand",
      "effect": "When trick_in_deal == 1: bid = n (0 for PASS); bid_suit = the named suit. The bid amounts are broadcast: 'Seat {seat} bids {bid or PASS}'. The suits are not shown."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_deal == 1: if max(bid) > 0, pitcher = the seat with the highest bid, ties going to the earliest seat in priority order (dealer+1, dealer+2, dealer, mod 3), and contract = that bid; otherwise pitcher = dealer and contract = 2. trump = pitcher's bid_suit; leader = pitcher."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_deal == 1: announce 'Pitcher: Seat {pitcher}, contract {contract}, trump {trump}'."
    },
    {
      "action": "ask",
      "who": "seat leader",
      "answer": "A card from own hand; on trick_in_deal == 1 only trump cards are offered",
      "effect": "played_card = chosen card; remove it from hand; led_suit = floor(card/10); broadcast the card to all."
    },
    {
      "action": "ask",
      "who": "seat (leader mod 3) + 1",
      "answer": "A legal card from own hand: if the hand holds the led suit, cards of the led suit plus any trumps; otherwise any card",
      "effect": "played_card = chosen card; remove it from hand; broadcast the card to all."
    },
    {
      "action": "ask",
      "who": "seat ((leader + 1) mod 3) + 1",
      "answer": "A legal card from own hand, by the same following rule",
      "effect": "played_card = chosen card; remove it from hand; broadcast the card to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_winner = the seat whose played_card has suit == trump and the highest rank, or if no trump was played, the seat with the highest rank of led_suit. Append all three played cards to trick_winner's captured; add their card points to trick_winner's captured_points. For each played trump of rank r: if r > high_trump_rank, set high_trump_rank = r and high_trump_seat = trick_winner; if r < low_trump_rank, set low_trump_rank = r and low_trump_seat = trick_winner; if r == 3, set three_seat = trick_winner. Then leader = trick_winner, clear every played_card and announce the winner."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When trick_in_deal == 4: deal_points = (seat == high_trump_seat ? 1 : 0) + (seat == low_trump_seat ? 1 : 0) + (captured_points strictly greater than both other players' captured_points ? 1 : 0) + (seat == three_seat ? 3 : 0). For each non-pitcher, score += deal_points. For the pitcher: if deal_points >= contract, score += deal_points; else score -= contract. Announce every deal_points value and score. Clear every captured pile."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "rounds_played += 1; if trick_in_deal == 4, then trick_in_deal = 1 and deal_number += 1; otherwise trick_in_deal += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if rounds_played == 36 (9 deals scored); otherwise continue."
    }
  ],
  "ending": {
    "condition": "rounds_played == 36",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 9 deals; the highest score wins, and players tied for highest share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When deal d begins, then the dealer is seat ((d-1) mod 3)+1: seat 1 deals deals 1, 4 and 7, seat 2 deals 2, 5 and 8, and seat 3 deals 3, 6 and 9."
    },
    {
      "id": "R2",
      "text": "When a deal begins, then all 24 cards are shuffled, each player receives exactly 4 private cards, and the other 12 are set aside unseen for the whole deal."
    },
    {
      "id": "R3",
      "text": "When bidding, then every player answers at once with PASS or a number from 2 to 6, plus one suit present in their own hand; a suit is named even when passing."
    },
    {
      "id": "R4",
      "text": "When the bids are in, then every player's amount or PASS is revealed, and the suits of the two non-pitchers are never revealed."
    },
    {
      "id": "R5",
      "text": "When bids differ, then the highest number wins: that player becomes pitcher, the number becomes the contract and the named suit becomes trump."
    },
    {
      "id": "R6",
      "text": "When the highest bid is tied, then the tied player earliest in priority order (dealer+1, then dealer+2, then dealer) wins the bid."
    },
    {
      "id": "R7",
      "text": "When all three players pass, then the dealer becomes pitcher with contract 2, and trump is the dealer's named suit."
    },
    {
      "id": "R8",
      "text": "When the first trick of a deal is played, then the pitcher leads and must lead a trump card."
    },
    {
      "id": "R9",
      "text": "When a later trick of a deal is played, then the winner of the previous trick leads any card."
    },
    {
      "id": "R10",
      "text": "When a trick is played, then the cards go one at a time from the leader in seat order."
    },
    {
      "id": "R11",
      "text": "When a following player holds the led suit, then they must play the led suit or a trump."
    },
    {
      "id": "R12",
      "text": "When a following player holds no card of the led suit, then they may play any card."
    },
    {
      "id": "R13",
      "text": "When at least one trump is in a trick, then the highest-ranked trump wins it; otherwise the highest-ranked card of the led suit wins it."
    },
    {
      "id": "R14",
      "text": "When a trick is won, then all three cards are visible to everyone and go into the winner's captured pile."
    },
    {
      "id": "R15",
      "text": "When a deal is scored, then 1 point (High) goes to the player who captured the highest-ranked trump played."
    },
    {
      "id": "R16",
      "text": "When a deal is scored, then 1 point (Low) goes to the player who captured the lowest-ranked trump played, which may be the same card as High."
    },
    {
      "id": "R17",
      "text": "When a deal is scored, then 1 point (Game) goes to the player with the most captured card points (rank 8 = 4, 7 = 3, 6 = 2, 5 = 1, others 0), and nobody scores Game if two or more players tie for most."
    },
    {
      "id": "R18",
      "text": "When the trump 3 was dealt and played, then 3 points (Three) go to the player who captured it; if it was not dealt, nobody scores Three."
    },
    {
      "id": "R19",
      "text": "When a deal is scored, then each non-pitcher adds their deal points (0 to 6) to their score."
    },
    {
      "id": "R20",
      "text": "When the pitcher's deal points are at least the contract, then the pitcher adds their deal points to their score."
    },
    {
      "id": "R21",
      "text": "When the pitcher's deal points are below the contract, then the pitcher is set: they subtract the contract from their score and add nothing; scores may go negative."
    },
    {
      "id": "R22",
      "text": "When the 9th deal (36th trick) has been scored, then the game ends and the highest total score wins; players tied for highest share it, which the source calls a draw."
    },
    {
      "id": "R23",
      "text": "When playing, then there is no table talk: players communicate only through bids and played cards."
    }
  ],
  "offers": [
    {
      "question": "Bid poll",
      "who": "all seats",
      "options": "For each suit S present in the seat's own hand: 'PASS S', '2 S', '3 S', '4 S', '5 S', '6 S'. Suits not in the hand are never offered."
    },
    {
      "question": "Lead card",
      "who": "the leader",
      "options": "First trick of a deal (the pitcher leading): only the trump cards in their hand. Later tricks: every card in their hand."
    },
    {
      "question": "Follow card (second and third player)",
      "who": "the two seats after the leader, in seat order",
      "options": "If the hand holds the led suit: every card of the led suit plus every trump in the hand. If the hand holds no card of the led suit: every card in the hand."
    }
  ],
  "choices": [
    {
      "what": "3 players, fixed",
      "why": "The designer set exactly 3; the priority order, dealer rotation and 12 set-aside cards are all built for 3 seats."
    },
    {
      "what": "Card encoding suit*10+rank (Red 1, Blue 2, Green 3)",
      "why": "Lets trick winners, trump checks and card points be worked out by arithmetic; players see card names."
    },
    {
      "what": "Bid offered as one combined choice such as '4 Blue' or 'PASS Red'",
      "why": "The engine takes one answer per question; listing only suits from the seat's own hand enforces that rule."
    },
    {
      "what": "PASS stored as bid 0",
      "why": "Allows a numeric comparison for the highest bid and an all-pass test with max(bid) == 0."
    },
    {
      "what": "No talk step",
      "why": "The rules forbid table talk; players communicate only through bids and cards."
    },
    {
      "what": "Strategy at the table",
      "why": "Players judge their hand's trump strength, bid against two rivals, and decide when to trump in, cash High or protect the 3, reading what is left from the cards played."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest final score is a shared win rather than a separate draw",
      "why": "The engine ranks by one expression and players level at the top share the win; this is the same outcome as a draw."
    },
    {
      "what": "Deal-start actions (deal, bid, pitcher resolution) are single steps carrying a 'when trick_in_deal == 1' condition",
      "why": "The step list is flat; per-step conditions reproduce the first round of each deal."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid; table: deal_number, pitcher, contract, trump.
````

## Reply

````
[
{"name":"R1 dealer rotation: in deal 9 seat 3 deals, so an all-pass makes seat 3 pitcher","rule":"R1","players":3,"seed":1,"default":"decline","rounds":1,
 "given":{"game":{"deal_number":9,"rounds_played":32,"trick_in_deal":1}},
 "rules":[],
 "expect":{"game":{"pitcher":3,"contract":2,"deal_number":9},"players":{"1":{"bid":0},"2":{"bid":0},"3":{"bid":0}}}},
{"name":"R1 dealer rotation: in deal 5 seat 2 deals, so an all-pass makes seat 2 pitcher","rule":"R1","players":3,"seed":2,"default":"decline","rounds":1,
 "given":{"game":{"deal_number":5,"rounds_played":16,"trick_in_deal":1}},
 "rules":[],
 "expect":{"game":{"pitcher":2,"contract":2,"deal_number":5}}},
{"name":"R2 deal gives 4 cards each and sets 12 aside (random cards, only counts asserted after the first trick)","rule":"R2","players":3,"seed":3,"default":"decline","rounds":1,
 "rules":[],
 "expect":{"lens":{"game":{"set_aside":12,"deck":0},"players":{"1":{"hand":3},"2":{"hand":3},"3":{"hand":3}}},
           "game":{"pitcher":1,"contract":2}}},
{"name":"R3 every seat passing is recorded as bid 0 (random hands)","rule":"R3","players":3,"seed":4,"default":"decline","rounds":1,
 "rules":[],
 "expect":{"players":{"1":{"bid":0,"score":0},"2":{"bid":0,"score":0},"3":{"bid":0,"score":0}}}},
{"name":"R4 bid amounts are revealed: everyone bids 6 in deal 2, seat 3 has priority","rule":"R4","players":3,"seed":5,"default":"last","rounds":1,
 "given":{"game":{"deal_number":2,"rounds_played":4,"trick_in_deal":1}},
 "rules":[],
 "expect":{"players":{"1":{"bid":6},"2":{"bid":6},"3":{"bid":6}},"game":{"pitcher":3,"contract":6}}},
{"name":"R5 the winning bid becomes the contract (deal 3, all bid 6, seat 1 has priority)","rule":"R5","players":3,"seed":6,"default":"last","rounds":1,
 "given":{"game":{"deal_number":3,"rounds_played":8,"trick_in_deal":1}},
 "rules":[],
 "expect":{"game":{"pitcher":1,"contract":6},"players":{"1":{"bid":6}}}},
{"name":"R6 tied top bid in deal 1 goes to dealer+1 = seat 2","rule":"R6","players":3,"seed":7,"default":"last","rounds":1,
 "rules":[],
 "expect":{"game":{"pitcher":2,"contract":6},"players":{"1":{"bid":6},"2":{"bid":6},"3":{"bid":6}}}},
{"name":"R7 all pass in deal 1: dealer seat 1 pitches with contract 2","rule":"R7","players":3,"seed":8,"default":"decline","rounds":1,
 "rules":[],
 "expect":{"game":{"pitcher":1,"contract":2,"deal_number":1},"players":{"1":{"bid":0},"2":{"bid":0},"3":{"bid":0}}}},
{"name":"R8 first trick is led by the pitcher (random hands, only pitcher and hand sizes asserted)","rule":"R8","players":3,"seed":9,"default":"decline","rounds":1,
 "rules":[],
 "expect":{"game":{"pitcher":1,"contract":2},"lens":{"players":{"1":{"hand":3},"2":{"hand":3},"3":{"hand":3}}}}},
{"name":"R9 a later trick's leader may lead any card, not only trump","rule":"R9","players":3,"seed":10,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":2,"rounds_played":1,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":2},
          "players":{"1":{"hand":[24,11,37]},"2":{"hand":[21,15,33]},"3":{"hand":[22,31,12]}}},
 "rules":[{"seat":2,"options_include":"Blue 1"},{"seat":3,"options_include":"Blue 2"},{"seat":1,"options_include":"Blue 4"}],
 "expect":{"offered":[{"seat":2,"option":"Blue 1"},{"seat":2,"option":"Red 5"},{"seat":2,"option":"Green 3"}],
           "players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},"game":{"deal_number":1}}},
{"name":"R10 play goes leader then seat order: seat 3 leads, then seats 1 and 2 follow","rule":"R10","players":3,"seed":11,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":2,"rounds_played":1,"deal_number":1,"dealer":1,"pitcher":3,"contract":2,"trump":1,"leader":3},
          "players":{"1":{"hand":[22,13,31]},"2":{"hand":[37,14,28]},"3":{"hand":[25,16,34]}}},
 "rules":[{"seat":3,"options_include":"Blue 5"},{"seat":1,"options_include":"Blue 2"},{"seat":2,"options_include":"Blue 8"}],
 "expect":{"offered":[{"seat":1,"option":"Red 3"},{"seat":2,"option":"Red 4"}],
           "not_offered":[{"seat":1,"option":"Green 1"},{"seat":2,"option":"Green 7"}],
           "players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},
{"name":"R11 a follower holding the led suit may play only that suit or trump","rule":"R11","players":3,"seed":12,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":2,"rounds_played":1,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":3,"leader":1},
          "players":{"1":{"hand":[14,26,35]},"2":{"hand":[12,33,27]},"3":{"hand":[11,24,38]}}},
 "rules":[{"seat":1,"options_include":"Red 4"},{"seat":2,"options_include":"Red 2"},{"seat":3,"options_include":"Red 1"}],
 "expect":{"offered":[{"seat":2,"option":"Green 3"},{"seat":3,"option":"Green 8"}],
           "not_offered":[{"seat":2,"option":"Blue 7"},{"seat":3,"option":"Blue 4"}],
           "players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},
{"name":"R12 a follower void in the led suit may play any card","rule":"R12","players":3,"seed":13,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":2,"rounds_played":1,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":1},
          "players":{"1":{"hand":[24,15,36]},"2":{"hand":[31,32,12]},"3":{"hand":[23,17,38]}}},
 "rules":[{"seat":1,"options_include":"Blue 4"},{"seat":2,"options_include":"Green 1"},{"seat":3,"options_include":"Blue 3"}],
 "expect":{"offered":[{"seat":2,"option":"Green 2"},{"seat":2,"option":"Red 2"}],
           "not_offered":[{"seat":3,"option":"Green 8"}],
           "players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},
{"name":"R13 a low trump beats the led Red 8: seat 2 takes High, Low and Game, pitcher seat 1 is set","rule":"R13","players":3,"seed":14,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":2,"leader":1,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[18],"captured_points":0,"score":0},"2":{"hand":[21],"captured_points":0,"score":0},"3":{"hand":[17],"captured_points":0,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-2},"2":{"score":3},"3":{"score":0}},"game":{"deal_number":2}}},
{"name":"R14 the trick's cards go to the winner: seat 1's Green 8 capture gives it Game","rule":"R14","players":3,"seed":15,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":1,
                  "high_trump_rank":8,"high_trump_seat":1,"low_trump_rank":1,"low_trump_seat":1,"three_seat":0},
          "players":{"1":{"hand":[38],"captured_points":3,"score":0},"2":{"hand":[31],"captured_points":4,"score":0},"3":{"hand":[32],"captured_points":0,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":3},"2":{"score":0},"3":{"score":0}}}},
{"name":"R15 High goes to the capturer of the highest trump (seat 2), Low and Game stay with seat 3","rule":"R15","players":3,"seed":16,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":1,
                  "high_trump_rank":1,"high_trump_seat":3,"low_trump_rank":1,"low_trump_seat":3,"three_seat":0},
          "players":{"1":{"hand":[12],"captured_points":0,"score":0},"2":{"hand":[17],"captured_points":0,"score":0},"3":{"hand":[21],"captured_points":10,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-2},"2":{"score":1},"3":{"score":2}}}},
{"name":"R16 a single trump played is both High and Low: pitcher seat 2 makes 2","rule":"R16","players":3,"seed":17,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":2,"contract":2,"trump":2,"leader":2,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[12],"captured_points":5,"score":0},"2":{"hand":[26],"captured_points":0,"score":0},"3":{"hand":[11],"captured_points":0,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":1},"2":{"score":2},"3":{"score":0}}}},
{"name":"R17 tied most card points means nobody scores Game","rule":"R17","players":3,"seed":18,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":1,
                  "high_trump_rank":8,"high_trump_seat":1,"low_trump_rank":1,"low_trump_seat":1,"three_seat":0},
          "players":{"1":{"hand":[21],"captured_points":3,"score":0},"2":{"hand":[22],"captured_points":3,"score":0},"3":{"hand":[23],"captured_points":0,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":2},"2":{"score":0},"3":{"score":0}}}},
{"name":"R18 the capturer of the trump 3 scores Three (seat 2 gets 5), pitcher set","rule":"R18","players":3,"seed":19,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":4,"trump":3,"leader":1,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[33],"captured_points":0,"score":0},"2":{"hand":[35],"captured_points":0,"score":0},"3":{"hand":[11],"captured_points":6,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-4},"2":{"score":5},"3":{"score":1}}}},
{"name":"R19 non-pitchers add their deal points to their running scores","rule":"R19","players":3,"seed":20,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":4,"trump":3,"leader":1,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[33],"captured_points":0,"score":0},"2":{"hand":[35],"captured_points":0,"score":5},"3":{"hand":[11],"captured_points":6,"score":7}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-4},"2":{"score":10},"3":{"score":8}}}},
{"name":"R20 pitcher reaching exactly the contract (6 of 6) adds the deal points","rule":"R20","players":3,"seed":21,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":6,"trump":1,"leader":1,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[18],"captured_points":0,"score":10},"2":{"hand":[13],"captured_points":0,"score":0},"3":{"hand":[22],"captured_points":0,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":16},"2":{"score":0},"3":{"score":0}},"game":{"deal_number":2}}},
{"name":"R21 a set pitcher loses the contract and may go negative (1 - 4 = -3)","rule":"R21","players":3,"seed":22,"default":"decline","rounds":1,
 "given":{"game":{"trick_in_deal":4,"rounds_played":3,"deal_number":1,"dealer":1,"pitcher":1,"contract":4,"trump":3,"leader":1,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[33],"captured_points":0,"score":1},"2":{"hand":[35],"captured_points":0,"score":0},"3":{"hand":[11],"captured_points":6,"score":0}}},
 "rules":[],
 "expect":{"players":{"1":{"score":-3},"2":{"score":5},"3":{"score":1}}}},
{"name":"R22 after the 36th trick the highest score wins","rule":"R22","players":3,"seed":23,"default":"decline",
 "given":{"game":{"trick_in_deal":4,"rounds_played":35,"deal_number":9,"dealer":3,"pitcher":3,"contract":2,"trump":1,"leader":3,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[21],"captured_points":0,"score":10},"2":{"hand":[22],"captured_points":0,"score":12},"3":{"hand":[18],"captured_points":0,"score":5}}},
 "rules":[],
 "expect":{"winner":2,"standings":{"1":10,"2":12,"3":8}}},
{"name":"R22 players tied for the highest final score share the win","rule":"R22","players":3,"seed":24,"default":"decline",
 "given":{"game":{"trick_in_deal":4,"rounds_played":35,"deal_number":9,"dealer":3,"pitcher":3,"contract":2,"trump":1,"leader":3,
                  "high_trump_rank":0,"high_trump_seat":0,"low_trump_rank":9,"low_trump_seat":0,"three_seat":0},
          "players":{"1":{"hand":[21],"captured_points":0,"score":12},"2":{"hand":[22],"captured_points":0,"score":12},"3":{"hand":[18],"captured_points":0,"score":5}}},
 "rules":[],
 "expect":{"winner":[1,2],"standings":{"1":12,"2":12,"3":8}}},
{"name":"R23 a mid-deal trick passes with only card plays and leaves scores unchanged","rule":"R23","players":3,"seed":25,"default":"first","rounds":1,
 "given":{"game":{"trick_in_deal":2,"rounds_played":1,"deal_number":1,"dealer":1,"pitcher":1,"contract":2,"trump":1,"leader":1},
          "players":{"1":{"hand":[24,15,36]},"2":{"hand":[31,32,12]},"3":{"hand":[23,17,38]}}},
 "rules":[],
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},"game":{"deal_number":1,"pitcher":1,"contract":2,"trump":1}}}
]
````
