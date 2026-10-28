# 44 scenarios

- time: 2026-10-28T03:55:41+00:00 (65.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 5bfbc10a7e978ac7, reply sha256 36a118fe5a3642f1

## Sent

````
SPEC:
{
  "name": "Mini Mari\u00e1\u0161 with Hidden Talon",
  "summary": "Three players play 5 deals of a 24-card trick-taking game: each deal starts with a sealed bid for a point contract, then 7 tricks with strict follow, overtake and trump rules, and the stake scales with the contract, Hearts trump and flek.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 24,
    "suits": 4,
    "cards_per_suit": 6,
    "hand_size": 7,
    "talon_size": 3,
    "ace_points": 10,
    "ten_points": 10,
    "other_card_points": 0,
    "last_trick_bonus": 10,
    "max_card_points": 90,
    "deals": 5,
    "rounds_per_deal": 8,
    "tricks_per_deal": 7,
    "total_rounds": 40,
    "bid_low": 40,
    "bid_mid": 50,
    "bid_high": 60,
    "stake_for_40": 1,
    "stake_for_50": 2,
    "stake_for_60": 4,
    "hearts_trump_multiplier": 2,
    "flek_multiplier": 2,
    "declarer_win_multiplier": 2,
    "defender_win_multiplier": 1,
    "starting_score": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "match score",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "cards held this deal, shown to the owner sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "this deal's bid: 0 for PASS, otherwise 40, 50 or 60",
        "observable": false
      },
      {
        "key": "is_declarer",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "whether this seat is the declarer this deal",
        "observable": false
      },
      {
        "key": "flek",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "a defender's flek choice this deal: FLEK or NO, empty for the declarer",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the card this seat played to the current trick",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "rounds played in the match, 1 to 40",
        "observable": false
      },
      {
        "key": "deal_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the current deal, 1 to 5",
        "observable": false
      },
      {
        "key": "round_in_deal",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the round within the deal, 1 to 8",
        "observable": false
      },
      {
        "key": "eldest",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "the eldest seat this deal: 1, 2, 3, 1, 2 for deals 1 to 5",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "undealt cards while dealing; each card is written as 'Suit Rank', e.g. 'Hearts A'",
        "observable": false
      },
      {
        "key": "talon",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 3 face-down cards, never played and never shown",
        "observable": false
      },
      {
        "key": "deal_played",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "false when all three players passed this deal",
        "observable": false
      },
      {
        "key": "declarer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the declarer's seat this deal, 0 if none",
        "observable": true
      },
      {
        "key": "contract",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the winning bid: 40, 50 or 60",
        "observable": true
      },
      {
        "key": "trump",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the trump suit",
        "observable": false
      },
      {
        "key": "stake_v",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the stake V this deal",
        "observable": true
      },
      {
        "key": "declarer_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the declarer's card points this deal",
        "observable": false
      },
      {
        "key": "defender_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the defenders' pooled card points this deal",
        "observable": false
      },
      {
        "key": "leader",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat leading the current trick",
        "observable": false
      },
      {
        "key": "led_suit",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the suit of the first card of the current trick",
        "observable": false
      },
      {
        "key": "trick",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "the cards played to the current trick, in order",
        "observable": false
      },
      {
        "key": "winning_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the seat whose card currently wins the trick, and after the trick, its winner",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 sit in seat order 1, 2, 3, 1 and so on.",
    "Every match score is set to 0, public.",
    "The 24 cards are Hearts, Bells, Leaves and Acorns, each with A, 10, K, O, U and 9. Rank values from high to low are A=6, 10=5, K=4, O=3, U=2, 9=1.",
    "There is no talk at any time in the match."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_number += 1; round_in_deal = ((round_number - 1) mod 8) + 1; deal_number = floor((round_number - 1) / 8) + 1; when round_in_deal == 1, eldest = ((deal_number - 1) mod 3) + 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1: deck = all 24 cards. Every hand is emptied; bid = 0, flek = '', is_declarer = false, played_card = ''. declarer = 0, contract = 0, trump = '', stake_v = 0, declarer_points = 0, defender_points = 0. Deal 7 cards to each hand, each a random draw removed from deck. The remaining 3 cards are moved from deck to talon."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1, each player sees only their own hand, sorted by suit (Hearts, Bells, Leaves, Acorns), then by rank from high to low."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of PASS, 40, 50, 60",
      "effect": "When round_in_deal == 1: bid = 0 for PASS, otherwise the number. Nobody sees another bid."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1: deal_played = (max bid > 0). If deal_played: among the seats with the highest bid, the one with the lowest score; if still tied, the one first in seat order starting from eldest. That seat becomes declarer, contract = its bid, and its is_declarer = true."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1 and not deal_played: 'All three passed; deal {deal_number} is not played.'"
    },
    {
      "action": "ask",
      "who": "the declarer",
      "answer": "one of Hearts, Bells, Leaves, Acorns",
      "effect": "When round_in_deal == 1 and deal_played: trump = the answer."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1 and deal_played: 'Declarer: Seat {declarer}, contract {contract}, trump {trump}. The other two seats are the defenders.'"
    },
    {
      "action": "poll",
      "who": "the two defenders",
      "answer": "one of FLEK, NO",
      "effect": "When round_in_deal == 1 and deal_played: flek = the answer, then both choices are announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 1 and deal_played: stake_v = 1 if contract == 40, 2 if 50, 4 if 60; multiply by 2 if trump == Hearts; multiply by 2 again if at least one defender has flek == FLEK. Announce 'Flek: {flek choices}. V = {stake_v}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal >= 2 and deal_played: trick = [], led_suit = '', played_card = '' for every seat, winning_seat = 0. leader = declarer if round_in_deal == 2, otherwise the previous trick's winner."
    },
    {
      "action": "ask",
      "who": "the seat equal to leader",
      "answer": "one card from own hand (any card)",
      "effect": "When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; led_suit = its suit; winning_seat = leader. The card is shown to everyone."
    },
    {
      "action": "ask",
      "who": "the next seat after leader in seat order",
      "answer": "one legal card from own hand (rules R10 to R14)",
      "effect": "When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick. winning_seat is updated: a trump beats any non-trump, a higher trump beats a lower trump, and a higher card of led_suit beats the current winner when no trump is in the trick. The card is shown to everyone.",
      "judged": "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."
    },
    {
      "action": "ask",
      "who": "the third seat (the seat before leader in seat order)",
      "answer": "one legal card from own hand (rules R10 to R14)",
      "effect": "When round_in_deal >= 2 and deal_played: the card is removed from hand, set as played_card and appended to trick; winning_seat is updated as in the previous step. The card is shown to everyone.",
      "judged": "The card played obeys the legal-card rules: follow the suit led if able, and then overtake when the currently winning card is of the suit led; if void in the suit led, play a trump if able, overtaking the highest trump played if able; otherwise any card."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal >= 2 and deal_played: pts = 10 x (number of Aces and Tens in trick), plus 10 if round_in_deal == 8. If winning_seat == declarer, declarer_points += pts, otherwise defender_points += pts. Announce 'Seat {winning_seat} wins the trick. Declarer {declarer_points}, defenders {defender_points}.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_deal == 8 and deal_played: if declarer_points >= contract, the declarer's score += 2 x stake_v and each defender's score -= stake_v; otherwise the declarer's score -= 2 x stake_v and each defender's score += stake_v. Announce the result and the match scores."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round_number == 40; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round_number == 40",
    "rank_by": "you.score",
    "decided_by": "Each player's match score after round 40. The highest score wins, and players tied at the top share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a deal starts (rounds 1, 9, 17, 25, 33), then all 24 cards are shuffled, each seat's hand gets 7 cards and the talon gets the remaining 3."
    },
    {
      "id": "R2",
      "text": "When cards are dealt, then each player sees only their own hand, and the talon is never shown to anyone, even at the end of the deal."
    },
    {
      "id": "R3",
      "text": "When deals 1, 2, 3, 4 and 5 are dealt, then the eldest is Seat 1, 2, 3, 1 and 2 respectively."
    },
    {
      "id": "R4",
      "text": "When bidding, then all three players choose PASS, 40, 50 or 60 at the same time, without seeing the other bids."
    },
    {
      "id": "R5",
      "text": "When all three players pass, then the deal is not played and rounds 2-8 of that deal have no plays and no scoring."
    },
    {
      "id": "R6",
      "text": "When at least one player bids, then the highest bidder becomes declarer and contract equals that bid."
    },
    {
      "id": "R7",
      "text": "When several players tie for the highest bid, then the tied player with the lowest match score becomes declarer; if they are still tied, the tied player first in seat order starting from the eldest does."
    },
    {
      "id": "R8",
      "text": "When the declarer is chosen, then the declarer picks trump from Hearts, Bells, Leaves and Acorns, and the declarer, the contract and trump are announced."
    },
    {
      "id": "R9",
      "text": "When trump is announced, then the two defenders choose FLEK or NO at the same time, and stake_v = 1, 2 or 4 for a 40, 50 or 60 contract, doubled if trump is Hearts and doubled again if at least one defender chose FLEK (e.g. a 60 contract in Hearts with a flek gives V = 16)."
    },
    {
      "id": "R10",
      "text": "When a player holds a card of the suit led, then they must play a card of that suit."
    },
    {
      "id": "R11",
      "text": "When the currently winning card is of the suit led and the player holds a higher card of that suit, then they must play a higher card of that suit, including when trump was led."
    },
    {
      "id": "R12",
      "text": "When the currently winning card is a trump and the suit led is not trump, then any card of the suit led is legal for a player who holds that suit."
    },
    {
      "id": "R13",
      "text": "When a player holds no card of the suit led but holds a trump, then they must play a trump, and if a trump has already been played to the trick they must play a higher trump than the highest one played if they have one, otherwise any trump."
    },
    {
      "id": "R14",
      "text": "When a player holds neither the suit led nor a trump, then they may play any card."
    },
    {
      "id": "R15",
      "text": "When a trick is complete, then the highest trump in it wins, or if it contains no trump, the highest card of the suit led wins, with ranks A > 10 > K > O > U > 9."
    },
    {
      "id": "R16",
      "text": "When the declarer wins a trick, then declarer_points increases by 10 for each Ace and each Ten in it; when a defender wins it, defender_points increases by the same amount."
    },
    {
      "id": "R17",
      "text": "When the round 8 trick (the 7th trick) is won, then the winning side also gets 10 card points."
    },
    {
      "id": "R18",
      "text": "When round 2 of a played deal begins, then the declarer leads; in rounds 3 to 8, the winner of the previous trick leads, and play continues in seat order."
    },
    {
      "id": "R19",
      "text": "When a played deal ends and declarer_points >= contract, then the declarer gains 2 x stake_v and each defender loses stake_v."
    },
    {
      "id": "R20",
      "text": "When a played deal ends and declarer_points < contract, then the declarer loses 2 x stake_v and each defender gains stake_v."
    },
    {
      "id": "R21",
      "text": "When round 40 is over, then the game ends, the highest match score wins and players tied at the top share a draw."
    },
    {
      "id": "R22",
      "text": "When at any point in the match, then there is no talk between players."
    }
  ],
  "offers": [
    {
      "question": "Bid (round 1 of each deal)",
      "who": "all three seats",
      "options": "PASS, 40, 50, 60"
    },
    {
      "question": "Trump choice",
      "who": "the declarer only",
      "options": "Hearts, Bells, Leaves, Acorns"
    },
    {
      "question": "Flek",
      "who": "each of the two defenders; the declarer is not asked",
      "options": "FLEK, NO"
    },
    {
      "question": "Lead a card",
      "who": "the leader of the trick",
      "options": "every card in their hand"
    },
    {
      "question": "Play to the trick (second and third seat)",
      "who": "the two seats after the leader, in seat order",
      "options": "Holding the suit led, with the currently winning card of the suit led: the cards of that suit higher than it, or if none, any card of that suit. Holding the suit led, with the currently winning card a trump of another suit: any card of the suit led. Void in the suit led but holding a trump: the trumps higher than the highest trump in the trick, or if none, any trump. Holding neither: any card in hand."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at 3: one declarer against two pooled defenders is the whole structure of the game. The minimum cannot be lower and the maximum cannot be higher because the 24-card deal (3x7 + 3) and the 2V/V scoring only balance with three seats."
    },
    {
      "what": "No talk step",
      "why": "The source says there is no talk at any time. Strategy is in bid sizing against your own hand, the trump choice, when to flek, and card play that reads which cards the others are forced to play."
    },
    {
      "what": "Bids stay private to their owner",
      "why": "The source announces only the declarer, contract and trump, not the losing bids."
    },
    {
      "what": "Card encoding 'Suit Rank' with rank values A=6, 10=5, K=4, O=3, U=2, 9=1",
      "why": "This lets the trick winner and the card points be worked out by arithmetic."
    },
    {
      "what": "Card legality is enforced by offering only legal cards, with a judged sentence as a check",
      "why": "The follow, overtake and trump rules are long. The legal set is worked out from trick, led_suit and trump, and a referee confirms it."
    },
    {
      "what": "PASS is stored as bid 0",
      "why": "This makes the highest bid and the all-pass test simple arithmetic."
    }
  ],
  "simplifications": [
    {
      "what": "One engine round equals one source round; rounds 2-8 of an all-pass deal still run as engine rounds with every step skipped by its condition",
      "why": "This keeps the count at 40 rounds and matches the source's 'skipped with no plays and no scoring'."
    },
    {
      "what": "Each step carries a condition on round_in_deal and deal_played instead of separate bidding and trick blocks",
      "why": "The step list is flat; per-step conditions express the same flow."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: declarer, contract, stake_v.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
{"name":"R1 deal: 7 cards per hand, 3 in talon, deck empty (the cards dealt are chance, the counts are not)","rule":"R1","players":3,"rounds":1,"seed":1,"default":"decline",
 "expect":{"lens":{"game":{"talon":3,"deck":0},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}}}},
{"name":"R1 deal 2 starts at round 9 with a fresh 7/7/7/3 deal","rule":"R1","players":3,"rounds":1,"seed":2,"default":"decline",
 "given":{"game":{"round_number":8,"deal_number":1,"round_in_deal":8,"eldest":1}},
 "expect":{"lens":{"game":{"talon":3,"deck":0},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}}}},
{"name":"R2 each seat holds only its own 7 cards and the talon keeps 3 cards","rule":"R2","players":3,"rounds":1,"seed":3,"default":"decline",
 "expect":{"lens":{"game":{"talon":3},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},
{"name":"R3 deal 2 eldest is seat 2: three-way tie at 40 with equal scores goes to seat 2","rule":"R3","players":3,"rounds":1,"seed":4,"default":"decline",
 "given":{"game":{"round_number":8,"deal_number":1,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"40"},{"seat":3,"options_include":"40"}],
 "expect":{"game":{"declarer":2,"contract":40}}},
{"name":"R3 deal 3 eldest is seat 3: three-way tie at 40 with equal scores goes to seat 3","rule":"R3","players":3,"rounds":1,"seed":5,"default":"decline",
 "given":{"game":{"round_number":16,"deal_number":2,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"40"},{"seat":3,"options_include":"40"}],
 "expect":{"game":{"declarer":3,"contract":40}}},
{"name":"R3 deal 5 eldest is seat 2: three-way tie at 50 with equal scores goes to seat 2","rule":"R3","players":3,"rounds":1,"seed":6,"default":"decline",
 "given":{"game":{"round_number":32,"deal_number":4,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"50"},{"seat":2,"options_include":"50"},{"seat":3,"options_include":"50"}],
 "expect":{"game":{"declarer":2,"contract":50}}},
{"name":"R4 every seat is offered PASS, 40, 50 and 60","rule":"R4","players":3,"rounds":1,"seed":7,"default":"decline",
 "expect":{"offered":[{"seat":1,"option":"PASS"},{"seat":1,"option":"60"},{"seat":2,"option":"PASS"},{"seat":2,"option":"40"},{"seat":3,"option":"50"},{"seat":3,"option":"60"}],
           "game":{"declarer":0}}},
{"name":"R5 all three pass: the deal is not played and nobody scores","rule":"R5","players":3,"rounds":8,"seed":8,"default":"decline",
 "expect":{"game":{"declarer":0,"contract":0},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},
           "not_offered":[{"seat":1,"option":"FLEK"},{"seat":2,"option":"FLEK"},{"seat":3,"option":"FLEK"},{"seat":1,"option":"Acorns"},{"seat":2,"option":"Acorns"},{"seat":3,"option":"Acorns"}]}},
{"name":"R6 highest bid 60 by seat 2 makes it declarer with contract 60","rule":"R6","players":3,"rounds":1,"seed":9,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"60"},{"seat":3,"options_include":"PASS"}],
 "expect":{"game":{"declarer":2,"contract":60}}},
{"name":"R7 tie at 50: the tied seat with the lower score (seat 3) becomes declarer","rule":"R7","players":3,"rounds":1,"seed":10,"default":"decline",
 "given":{"players":{"1":{"score":0},"2":{"score":3},"3":{"score":-5}}},
 "rules":[{"seat":1,"options_include":"50"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"50"}],
 "expect":{"game":{"declarer":3,"contract":50}}},
{"name":"R7 tie at 60 with equal scores in deal 1: seat 2 comes before seat 3 from eldest seat 1","rule":"R7","players":3,"rounds":1,"seed":11,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"60"},{"seat":3,"options_include":"60"}],
 "expect":{"game":{"declarer":2,"contract":60}}},
{"name":"R8 only the declarer picks trump; Leaves at 40 with no flek gives V = 1","rule":"R8","players":3,"rounds":1,"seed":12,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":1,"options_include":"Leaves"}],
 "expect":{"game":{"declarer":1,"contract":40,"stake_v":1},
           "offered":[{"seat":1,"option":"Acorns"}],
           "not_offered":[{"seat":2,"option":"Leaves"},{"seat":3,"option":"Leaves"}]}},
{"name":"R9 60 contract in Hearts with one flek gives V = 16; the declarer is not asked to flek","rule":"R9","players":3,"rounds":1,"seed":13,"default":"decline",
 "rules":[{"seat":1,"options_include":"60"},{"seat":1,"options_include":"Hearts"},{"seat":2,"options_include":"FLEK"},{"seat":3,"options_include":"NO"}],
 "expect":{"game":{"declarer":1,"contract":60,"stake_v":16},
           "not_offered":[{"seat":1,"option":"FLEK"}]}},
{"name":"R9 50 contract in Bells with both defenders saying NO gives V = 2","rule":"R9","players":3,"rounds":1,"seed":14,"default":"decline",
 "rules":[{"seat":2,"options_include":"50"},{"seat":2,"options_include":"Bells"},{"seat":1,"options_include":"NO"},{"seat":3,"options_include":"NO"}],
 "expect":{"game":{"declarer":2,"contract":50,"stake_v":2}}},
{"name":"R10 a seat holding the suit led must follow it","rule":"R10","players":3,"rounds":1,"seed":15,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Bells 9","Leaves A"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Bells 9"}],"not_offered":[{"seat":2,"option":"Leaves A"}]}},
{"name":"R11 a seat following a winning card of the suit led must overtake it","rule":"R11","players":3,"rounds":1,"seed":16,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells O","Hearts 9"]},"2":{"hand":["Bells A","Bells 9","Leaves 10"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Bells O"}],
 "expect":{"offered":[{"seat":2,"option":"Bells A"}],"not_offered":[{"seat":2,"option":"Bells 9"},{"seat":2,"option":"Leaves 10"}]}},
{"name":"R11 overtaking also applies when trump is led","rule":"R11","players":3,"rounds":1,"seed":17,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Acorns K","Hearts 9"]},"2":{"hand":["Acorns A","Acorns U","Leaves 10"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Acorns K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns A"}],"not_offered":[{"seat":2,"option":"Acorns U"},{"seat":2,"option":"Leaves 10"}]}},
{"name":"R12 after a trump wins a non-trump lead, any card of the suit led is legal","rule":"R12","players":3,"rounds":1,"seed":18,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns 9","Leaves A"]},"3":{"hand":["Bells A","Bells 9","Acorns A"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns 9"},{"seat":3,"option":"Bells 9"},{"seat":3,"option":"Bells A"}],
           "not_offered":[{"seat":2,"option":"Leaves A"},{"seat":3,"option":"Acorns A"}]}},
{"name":"R13 a seat void in the suit led must trump and overtake the highest trump if able","rule":"R13","players":3,"rounds":1,"seed":19,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns K","Leaves A"]},"3":{"hand":["Acorns A","Acorns 9","Leaves 10"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns K"},{"seat":3,"option":"Acorns A"}],
           "not_offered":[{"seat":2,"option":"Leaves A"},{"seat":3,"option":"Acorns 9"},{"seat":3,"option":"Leaves 10"}]}},
{"name":"R13 a seat void in the suit led that cannot overtake the trump may play any trump","rule":"R13","players":3,"rounds":1,"seed":20,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns K","Leaves A"]},"3":{"hand":["Acorns U","Acorns 9","Leaves 10"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":3,"option":"Acorns U"},{"seat":3,"option":"Acorns 9"}],
           "not_offered":[{"seat":3,"option":"Leaves 10"}]}},
{"name":"R14 a seat with neither the suit led nor a trump may play any card","rule":"R14","players":3,"rounds":1,"seed":21,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Leaves A","Hearts O"]},"3":{"hand":["Bells 9","Leaves K"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"},{"seat":2,"options_include":"Hearts O"}],
 "expect":{"offered":[{"seat":2,"option":"Leaves A"},{"seat":2,"option":"Hearts O"}]}},
{"name":"R15 a low trump beats the Ace of the suit led: declarer seat 3 trumps the last trick and makes 60 of 40","rule":"R15","players":3,"rounds":1,"seed":22,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":3,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":30,"defender_points":50,"leader":1,"winning_seat":1},
          "players":{"1":{"hand":["Bells 10"]},"2":{"hand":["Bells A"]},"3":{"is_declarer":true,"hand":["Acorns 9"]}}},
 "expect":{"players":{"1":{"score":-1},"2":{"score":-1},"3":{"score":2}}}},
{"name":"R16 declarer wins a trick with an Ace and a Ten: 20 points plus last-trick 10 reaches the 50 contract","rule":"R16","players":3,"rounds":1,"seed":23,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":50,"trump":"Acorns","stake_v":2,"declarer_points":20,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Hearts A"]},"2":{"hand":["Hearts K"]},"3":{"hand":["Hearts 10"]}}},
 "expect":{"players":{"1":{"score":4},"2":{"score":-2},"3":{"score":-2}}}},
{"name":"R17 the last-trick 10 alone lifts the declarer from 30 to 40 and makes the contract","rule":"R17","players":3,"rounds":1,"seed":24,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":30,"defender_points":50,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Hearts K"]},"2":{"hand":["Hearts 9"]},"3":{"hand":["Hearts O"]}}},
 "expect":{"players":{"1":{"score":2},"2":{"score":-1},"3":{"score":-1}}}},
{"name":"R18 the declarer (seat 2) leads round 2 and seat 1 plays third","rule":"R18","players":3,"rounds":1,"seed":25,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":2,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"hand":["Bells A","Leaves A"]},"2":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"3":{"hand":["Bells 9","Leaves 9"]}}},
 "rules":[{"seat":2,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Bells K"},{"seat":1,"option":"Bells A"}],
           "not_offered":[{"seat":1,"option":"Leaves A"},{"seat":3,"option":"Leaves 9"}]}},
{"name":"R19 declarer seat 2 ends with 60 of a 60 contract at V = 16: +32, defenders -16","rule":"R19","players":3,"rounds":1,"seed":26,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":2,"contract":60,"trump":"Hearts","stake_v":16,"declarer_points":60,"defender_points":20,"leader":1,"winning_seat":1},
          "players":{"1":{"hand":["Leaves K"]},"2":{"is_declarer":true,"hand":["Leaves 9"]},"3":{"hand":["Leaves O"]}}},
 "expect":{"players":{"1":{"score":-16},"2":{"score":32},"3":{"score":-16}}}},
{"name":"R20 declarer seat 1 ends with 40 of a 50 contract at V = 4: -8, defenders +4","rule":"R20","players":3,"rounds":1,"seed":27,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":50,"trump":"Acorns","stake_v":4,"declarer_points":40,"defender_points":20,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Leaves 9"]},"2":{"hand":["Leaves A"]},"3":{"hand":["Leaves K"]}}},
 "expect":{"players":{"1":{"score":-8},"2":{"score":4},"3":{"score":4}}}},
{"name":"R21 the match ends after round 40 and the highest score wins","rule":"R21","players":3,"seed":28,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":39,"deal_number":5,"round_in_deal":7,"eldest":2,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":40,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"score":5,"is_declarer":true,"hand":["Leaves K"]},"2":{"score":3,"hand":["Leaves 9"]},"3":{"score":2,"hand":["Leaves O"]}}},
 "expect":{"winner":1,"standings":{"1":7,"2":2,"3":1},"players":{"1":{"score":7},"2":{"score":2},"3":{"score":1}}}},
{"name":"R21 seats level at the top after round 40 share the win","rule":"R21","players":3,"seed":29,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":39,"deal_number":5,"round_in_deal":7,"eldest":2,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":40,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"score":2,"is_declarer":true,"hand":["Leaves K"]},"2":{"score":5,"hand":["Leaves 9"]},"3":{"score":3,"hand":["Leaves O"]}}},
 "expect":{"winner":[1,2],"standings":{"1":4,"2":4,"3":2}}},
{"name":"R22 no talk: an all-pass first round asks only bids and changes no score","rule":"R22","players":3,"rounds":1,"seed":30,"default":"decline",
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},"game":{"declarer":0},
           "offered":[{"seat":1,"option":"PASS"},{"seat":2,"option":"PASS"},{"seat":3,"option":"PASS"}]}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name); scenario 23: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 26: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name); scenario 28: needs `rules` (what each seat answers, by option name); scenario 29: needs `rules` (what each seat answers, by option name); scenario 30: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
{"name":"R1 deal: 7 cards per hand, 3 in talon, deck empty (the cards dealt are chance, the counts are not)","rule":"R1","players":3,"rounds":1,"seed":1,"default":"decline",
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"lens":{"game":{"talon":3,"deck":0},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}}}},
{"name":"R1 deal 2 starts at round 9 with a fresh 7/7/7/3 deal","rule":"R1","players":3,"rounds":1,"seed":2,"default":"decline",
 "given":{"game":{"round_number":8,"deal_number":1,"round_in_deal":8,"eldest":1}},
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"lens":{"game":{"talon":3,"deck":0},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}}}},
{"name":"R2 each seat holds only its own 7 cards and the talon keeps 3 cards","rule":"R2","players":3,"rounds":1,"seed":3,"default":"decline",
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"lens":{"game":{"talon":3},"players":{"1":{"hand":7},"2":{"hand":7},"3":{"hand":7}}},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}}}},
{"name":"R3 deal 2 eldest is seat 2: three-way tie at 40 with equal scores goes to seat 2","rule":"R3","players":3,"rounds":1,"seed":4,"default":"decline",
 "given":{"game":{"round_number":8,"deal_number":1,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"40"},{"seat":3,"options_include":"40"}],
 "expect":{"game":{"declarer":2,"contract":40}}},
{"name":"R3 deal 3 eldest is seat 3: three-way tie at 40 with equal scores goes to seat 3","rule":"R3","players":3,"rounds":1,"seed":5,"default":"decline",
 "given":{"game":{"round_number":16,"deal_number":2,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"40"},{"seat":3,"options_include":"40"}],
 "expect":{"game":{"declarer":3,"contract":40}}},
{"name":"R3 deal 5 eldest is seat 2: three-way tie at 50 with equal scores goes to seat 2","rule":"R3","players":3,"rounds":1,"seed":6,"default":"decline",
 "given":{"game":{"round_number":32,"deal_number":4,"round_in_deal":8}},
 "rules":[{"seat":1,"options_include":"50"},{"seat":2,"options_include":"50"},{"seat":3,"options_include":"50"}],
 "expect":{"game":{"declarer":2,"contract":50}}},
{"name":"R4 every seat is offered PASS, 40, 50 and 60","rule":"R4","players":3,"rounds":1,"seed":7,"default":"decline",
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"offered":[{"seat":1,"option":"PASS"},{"seat":1,"option":"60"},{"seat":2,"option":"PASS"},{"seat":2,"option":"40"},{"seat":3,"option":"50"},{"seat":3,"option":"60"}],
           "game":{"declarer":0}}},
{"name":"R5 all three pass: the deal is not played and nobody scores","rule":"R5","players":3,"rounds":8,"seed":8,"default":"decline",
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"game":{"declarer":0,"contract":0},"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},
           "not_offered":[{"seat":1,"option":"FLEK"},{"seat":2,"option":"FLEK"},{"seat":3,"option":"FLEK"},{"seat":1,"option":"Acorns"},{"seat":2,"option":"Acorns"},{"seat":3,"option":"Acorns"}]}},
{"name":"R6 highest bid 60 by seat 2 makes it declarer with contract 60","rule":"R6","players":3,"rounds":1,"seed":9,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"60"},{"seat":3,"options_include":"PASS"}],
 "expect":{"game":{"declarer":2,"contract":60}}},
{"name":"R7 tie at 50: the tied seat with the lower score (seat 3) becomes declarer","rule":"R7","players":3,"rounds":1,"seed":10,"default":"decline",
 "given":{"players":{"1":{"score":0},"2":{"score":3},"3":{"score":-5}}},
 "rules":[{"seat":1,"options_include":"50"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"50"}],
 "expect":{"game":{"declarer":3,"contract":50}}},
{"name":"R7 tie at 60 with equal scores in deal 1: seat 2 comes before seat 3 from eldest seat 1","rule":"R7","players":3,"rounds":1,"seed":11,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":2,"options_include":"60"},{"seat":3,"options_include":"60"}],
 "expect":{"game":{"declarer":2,"contract":60}}},
{"name":"R8 only the declarer picks trump; Leaves at 40 with no flek gives V = 1","rule":"R8","players":3,"rounds":1,"seed":12,"default":"decline",
 "rules":[{"seat":1,"options_include":"40"},{"seat":1,"options_include":"Leaves"}],
 "expect":{"game":{"declarer":1,"contract":40,"stake_v":1},
           "offered":[{"seat":1,"option":"Acorns"}],
           "not_offered":[{"seat":2,"option":"Leaves"},{"seat":3,"option":"Leaves"}]}},
{"name":"R9 60 contract in Hearts with one flek gives V = 16; the declarer is not asked to flek","rule":"R9","players":3,"rounds":1,"seed":13,"default":"decline",
 "rules":[{"seat":1,"options_include":"60"},{"seat":1,"options_include":"Hearts"},{"seat":2,"options_include":"FLEK"},{"seat":3,"options_include":"NO"}],
 "expect":{"game":{"declarer":1,"contract":60,"stake_v":16},
           "not_offered":[{"seat":1,"option":"FLEK"}]}},
{"name":"R9 50 contract in Bells with both defenders saying NO gives V = 2","rule":"R9","players":3,"rounds":1,"seed":14,"default":"decline",
 "rules":[{"seat":2,"options_include":"50"},{"seat":2,"options_include":"Bells"},{"seat":1,"options_include":"NO"},{"seat":3,"options_include":"NO"}],
 "expect":{"game":{"declarer":2,"contract":50,"stake_v":2}}},
{"name":"R10 a seat holding the suit led must follow it","rule":"R10","players":3,"rounds":1,"seed":15,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Bells 9","Leaves A"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Bells 9"}],"not_offered":[{"seat":2,"option":"Leaves A"}]}},
{"name":"R11 a seat following a winning card of the suit led must overtake it","rule":"R11","players":3,"rounds":1,"seed":16,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells O","Hearts 9"]},"2":{"hand":["Bells A","Bells 9","Leaves 10"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Bells O"}],
 "expect":{"offered":[{"seat":2,"option":"Bells A"}],"not_offered":[{"seat":2,"option":"Bells 9"},{"seat":2,"option":"Leaves 10"}]}},
{"name":"R11 overtaking also applies when trump is led","rule":"R11","players":3,"rounds":1,"seed":17,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Acorns K","Hearts 9"]},"2":{"hand":["Acorns A","Acorns U","Leaves 10"]},"3":{"hand":["Leaves 9","Hearts K"]}}},
 "rules":[{"seat":1,"options_include":"Acorns K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns A"}],"not_offered":[{"seat":2,"option":"Acorns U"},{"seat":2,"option":"Leaves 10"}]}},
{"name":"R12 after a trump wins a non-trump lead, any card of the suit led is legal","rule":"R12","players":3,"rounds":1,"seed":18,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns 9","Leaves A"]},"3":{"hand":["Bells A","Bells 9","Acorns A"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns 9"},{"seat":3,"option":"Bells 9"},{"seat":3,"option":"Bells A"}],
           "not_offered":[{"seat":2,"option":"Leaves A"},{"seat":3,"option":"Acorns A"}]}},
{"name":"R13 a seat void in the suit led must trump and overtake the highest trump if able","rule":"R13","players":3,"rounds":1,"seed":19,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns K","Leaves A"]},"3":{"hand":["Acorns A","Acorns 9","Leaves 10"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Acorns K"},{"seat":3,"option":"Acorns A"}],
           "not_offered":[{"seat":2,"option":"Leaves A"},{"seat":3,"option":"Acorns 9"},{"seat":3,"option":"Leaves 10"}]}},
{"name":"R13 a seat void in the suit led that cannot overtake the trump may play any trump","rule":"R13","players":3,"rounds":1,"seed":20,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Acorns K","Leaves A"]},"3":{"hand":["Acorns U","Acorns 9","Leaves 10"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":3,"option":"Acorns U"},{"seat":3,"option":"Acorns 9"}],
           "not_offered":[{"seat":3,"option":"Leaves 10"}]}},
{"name":"R14 a seat with neither the suit led nor a trump may play any card","rule":"R14","players":3,"rounds":1,"seed":21,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"2":{"hand":["Leaves A","Hearts O"]},"3":{"hand":["Bells 9","Leaves K"]}}},
 "rules":[{"seat":1,"options_include":"Bells K"},{"seat":2,"options_include":"Hearts O"}],
 "expect":{"offered":[{"seat":2,"option":"Leaves A"},{"seat":2,"option":"Hearts O"}]}},
{"name":"R15 a low trump beats the Ace of the suit led: declarer seat 3 trumps the last trick and makes 60 of 40","rule":"R15","players":3,"rounds":1,"seed":22,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":3,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":30,"defender_points":50,"leader":1,"winning_seat":1},
          "players":{"1":{"hand":["Bells 10"]},"2":{"hand":["Bells A"]},"3":{"is_declarer":true,"hand":["Acorns 9"]}}},
 "rules":[{"seat":1,"options_include":"Bells 10"},{"seat":2,"options_include":"Bells A"},{"seat":3,"options_include":"Acorns 9"}],
 "expect":{"players":{"1":{"score":-1},"2":{"score":-1},"3":{"score":2}}}},
{"name":"R16 declarer wins a trick with an Ace and a Ten: 20 points plus last-trick 10 reaches the 50 contract","rule":"R16","players":3,"rounds":1,"seed":23,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":50,"trump":"Acorns","stake_v":2,"declarer_points":20,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Hearts A"]},"2":{"hand":["Hearts K"]},"3":{"hand":["Hearts 10"]}}},
 "rules":[{"seat":1,"options_include":"Hearts A"},{"seat":2,"options_include":"Hearts K"},{"seat":3,"options_include":"Hearts 10"}],
 "expect":{"players":{"1":{"score":4},"2":{"score":-2},"3":{"score":-2}}}},
{"name":"R17 the last-trick 10 alone lifts the declarer from 30 to 40 and makes the contract","rule":"R17","players":3,"rounds":1,"seed":24,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":30,"defender_points":50,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Hearts K"]},"2":{"hand":["Hearts 9"]},"3":{"hand":["Hearts O"]}}},
 "rules":[{"seat":1,"options_include":"Hearts K"},{"seat":2,"options_include":"Hearts 9"},{"seat":3,"options_include":"Hearts O"}],
 "expect":{"players":{"1":{"score":2},"2":{"score":-1},"3":{"score":-1}}}},
{"name":"R18 the declarer (seat 2) leads round 2 and seat 1 plays third","rule":"R18","players":3,"rounds":1,"seed":25,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":1,"deal_number":1,"round_in_deal":1,"eldest":1,"deal_played":true,"declarer":2,"contract":40,"trump":"Acorns","stake_v":1},
          "players":{"1":{"hand":["Bells A","Leaves A"]},"2":{"is_declarer":true,"hand":["Bells K","Hearts 9"]},"3":{"hand":["Bells 9","Leaves 9"]}}},
 "rules":[{"seat":2,"options_include":"Bells K"}],
 "expect":{"offered":[{"seat":2,"option":"Bells K"},{"seat":1,"option":"Bells A"}],
           "not_offered":[{"seat":1,"option":"Leaves A"},{"seat":3,"option":"Leaves 9"}]}},
{"name":"R19 declarer seat 2 ends with 60 of a 60 contract at V = 16: +32, defenders -16","rule":"R19","players":3,"rounds":1,"seed":26,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":2,"contract":60,"trump":"Hearts","stake_v":16,"declarer_points":60,"defender_points":20,"leader":1,"winning_seat":1},
          "players":{"1":{"hand":["Leaves K"]},"2":{"is_declarer":true,"hand":["Leaves 9"]},"3":{"hand":["Leaves O"]}}},
 "rules":[{"seat":1,"options_include":"Leaves K"},{"seat":2,"options_include":"Leaves 9"},{"seat":3,"options_include":"Leaves O"}],
 "expect":{"players":{"1":{"score":-16},"2":{"score":32},"3":{"score":-16}}}},
{"name":"R20 declarer seat 1 ends with 40 of a 50 contract at V = 4: -8, defenders +4","rule":"R20","players":3,"rounds":1,"seed":27,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":7,"deal_number":1,"round_in_deal":7,"eldest":1,"deal_played":true,"declarer":1,"contract":50,"trump":"Acorns","stake_v":4,"declarer_points":40,"defender_points":20,"leader":1,"winning_seat":1},
          "players":{"1":{"is_declarer":true,"hand":["Leaves 9"]},"2":{"hand":["Leaves A"]},"3":{"hand":["Leaves K"]}}},
 "rules":[{"seat":1,"options_include":"Leaves 9"},{"seat":2,"options_include":"Leaves A"},{"seat":3,"options_include":"Leaves K"}],
 "expect":{"players":{"1":{"score":-8},"2":{"score":4},"3":{"score":4}}}},
{"name":"R21 the match ends after round 40 and the highest score wins","rule":"R21","players":3,"seed":28,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":39,"deal_number":5,"round_in_deal":7,"eldest":2,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":40,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"score":5,"is_declarer":true,"hand":["Leaves K"]},"2":{"score":3,"hand":["Leaves 9"]},"3":{"score":2,"hand":["Leaves O"]}}},
 "rules":[{"seat":1,"options_include":"Leaves K"},{"seat":2,"options_include":"Leaves 9"},{"seat":3,"options_include":"Leaves O"}],
 "expect":{"winner":1,"standings":{"1":7,"2":2,"3":1},"players":{"1":{"score":7},"2":{"score":2},"3":{"score":1}}}},
{"name":"R21 seats level at the top after round 40 share the win","rule":"R21","players":3,"seed":29,"default":"decline",
 "judge":{"The card played obeys the legal-card rules":true},
 "given":{"game":{"round_number":39,"deal_number":5,"round_in_deal":7,"eldest":2,"deal_played":true,"declarer":1,"contract":40,"trump":"Acorns","stake_v":1,"declarer_points":40,"defender_points":40,"leader":1,"winning_seat":1},
          "players":{"1":{"score":2,"is_declarer":true,"hand":["Leaves K"]},"2":{"score":5,"hand":["Leaves 9"]},"3":{"score":3,"hand":["Leaves O"]}}},
 "rules":[{"seat":1,"options_include":"Leaves K"},{"seat":2,"options_include":"Leaves 9"},{"seat":3,"options_include":"Leaves O"}],
 "expect":{"winner":[1,2],"standings":{"1":4,"2":4,"3":2}}},
{"name":"R22 no talk: an all-pass first round asks only bids and changes no score","rule":"R22","players":3,"rounds":1,"seed":30,"default":"decline",
 "rules":[{"seat":1,"options_include":"PASS"},{"seat":2,"options_include":"PASS"},{"seat":3,"options_include":"PASS"}],
 "expect":{"players":{"1":{"score":0},"2":{"score":0},"3":{"score":0}},"game":{"declarer":0},
           "offered":[{"seat":1,"option":"PASS"},{"seat":2,"option":"PASS"},{"seat":3,"option":"PASS"}]}}
]
````
