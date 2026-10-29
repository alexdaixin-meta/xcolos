# 05 scenarios

- time: 2026-10-28T06:13:18+00:00 (103.5s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 d698be50373ca791, reply sha256 0b160b956d0d3d98

## Sent

````
SPEC:
{
  "name": "Scopa Duel",
  "summary": "Two-player Scopa over 2 hands of 18 rounds. Players capture table cards by matching rank or summing to it, score Scopas for sweeping the table, then score cards, Coins, the Seven of Coins and sevens.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 40,
    "suits": 4,
    "ranks_per_suit": 10,
    "ace_rank": 1,
    "jack_rank": 8,
    "knight_rank": 9,
    "king_rank": 10,
    "hands": 2,
    "rounds_per_hand": 18,
    "total_rounds": 36,
    "table_deal": 4,
    "cards_per_deal": 3,
    "deals_per_hand": 6,
    "shuffle_round_hand1": 1,
    "shuffle_round_hand2": 19,
    "redeal_interval": 3,
    "first_redeal_round_hand1": 4,
    "last_redeal_round_hand1": 16,
    "first_redeal_round_hand2": 22,
    "last_redeal_round_hand2": 34,
    "final_play_round_hand1": 18,
    "final_play_round_hand2": 36,
    "scopa_points": 1,
    "most_cards_points": 1,
    "cards_tie_count": 20,
    "most_coins_points": 1,
    "coins_tie_count": 5,
    "seven_of_coins_points": 1,
    "most_sevens_points": 1,
    "primary_rank": 7,
    "secondary_rank": 6,
    "no_capturer": 0,
    "score_weight": 10000,
    "cards_weight": 100,
    "coins_weight": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards held privately, as codes such as '7Co' (rank 1-10 plus suit Co=Coins, Cu=Cups, Sw=Swords, Cl=Clubs).",
        "observable": false
      },
      {
        "key": "captures",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "This hand's capture pile. Captures are public.",
        "observable": false
      },
      {
        "key": "scopa_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Scopas scored in the current hand.",
        "observable": false
      },
      {
        "key": "played_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card chosen this turn.",
        "observable": false
      },
      {
        "key": "declared",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Table cards declared as captured this turn; may be empty.",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total points across both hands.",
        "observable": true
      },
      {
        "key": "total_cards",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total of cards captured across both hands.",
        "observable": true
      },
      {
        "key": "total_coins",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total of Coins captured across both hands.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Undealt cards. The order is hidden.",
        "observable": false
      },
      {
        "key": "table_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up cards on the table.",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round, 1 to 36.",
        "observable": true
      },
      {
        "key": "last_capturer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the most recent capture in this hand; 0 if none.",
        "observable": false
      },
      {
        "key": "full_deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "1Co",
          "2Co",
          "3Co",
          "4Co",
          "5Co",
          "6Co",
          "7Co",
          "8Co",
          "9Co",
          "10Co",
          "1Cu",
          "2Cu",
          "3Cu",
          "4Cu",
          "5Cu",
          "6Cu",
          "7Cu",
          "8Cu",
          "9Cu",
          "10Cu",
          "1Sw",
          "2Sw",
          "3Sw",
          "4Sw",
          "5Sw",
          "6Sw",
          "7Sw",
          "8Sw",
          "9Sw",
          "10Sw",
          "1Cl",
          "2Cl",
          "3Cl",
          "4Cl",
          "5Cl",
          "6Cl",
          "7Cl",
          "8Cl",
          "9Cl",
          "10Cl"
        ],
        "meaning": "The 40 card codes, used to refill the deck at the start of each hand.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 1 is Player A and seat 2 is Player B.",
    "Every player's score, total_cards and total_coins are set to 0, and round is set to 1.",
    "Dealing happens inside the round steps at rounds 1 and 19."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round is 1 or 19: deck = full_deck; table_cards, every hand, every captures and every declared are emptied; scopa_points = 0 for each player; last_capturer = 0. Then 4 cards are drawn at random from deck into table_cards, and 3 cards are drawn at random from deck into each player's hand (each draw is removed from deck and appended to its destination)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round is in {4,7,10,13,16,22,25,28,31,34}: 3 cards are drawn at random from deck into each player's hand."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand plus the public table_cards, captures, scopa_points, score, total_cards, total_coins and round."
    },
    {
      "action": "ask",
      "who": "the Leader: seat 1 when round <= 18, seat 2 when round >= 19",
      "answer": "one card from the Leader's own hand",
      "effect": "Leader.played_card = the chosen card; it is removed from Leader.hand."
    },
    {
      "action": "ask",
      "who": "the Leader",
      "answer": "short text listing the table card codes captured, separated by spaces, or 'none'",
      "effect": "Leader.declared = the listed table cards (empty if 'none')."
    },
    {
      "action": "update",
      "who": "the Leader",
      "answer": null,
      "judged": "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.",
      "effect": "If legal and declared is non-empty: the played_card and the declared cards are appended to Leader.captures, the declared cards are removed from table_cards, and last_capturer = Leader's seat; then, if table_cards is empty, Leader.scopa_points += 1. Otherwise (declared is empty, or the declaration is illegal): played_card is appended to table_cards and nothing is captured. The table is told what was played and captured."
    },
    {
      "action": "ask",
      "who": "the Dealer: seat 2 when round <= 18, seat 1 when round >= 19",
      "answer": "one card from the Dealer's own hand",
      "effect": "Dealer.played_card = the chosen card; it is removed from Dealer.hand."
    },
    {
      "action": "ask",
      "who": "the Dealer",
      "answer": "short text listing the table card codes captured, separated by spaces, or 'none'",
      "effect": "Dealer.declared = the listed table cards (empty if 'none')."
    },
    {
      "action": "update",
      "who": "the Dealer",
      "answer": null,
      "judged": "The declaration is legal: if some table card has the same rank as the played card, the declaration names exactly one such table card; otherwise it names either no cards or a set of distinct cards currently on the table whose ranks add up exactly to the played card's rank.",
      "effect": "If legal and declared is non-empty: the played_card and the declared cards are appended to Dealer.captures, the declared cards are removed from table_cards, and last_capturer = Dealer's seat; then, if table_cards is empty and round is not 18 or 36, Dealer.scopa_points += 1. Otherwise: played_card is appended to table_cards and nothing is captured. The table is told what was played and captured."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round is 18 or 36: if last_capturer > 0, all table_cards are appended to that seat's captures; otherwise they are discarded. table_cards is emptied. Hand scoring, using this hand's captures: +1 score to the player with strictly more cards; +1 to the player with strictly more cards whose suit is Co; +1 to the holder of '7Co'; +1 to the player with more rank-7 cards, or, if those are tied, more rank-6 cards, and no point if both are tied; each player's score += scopa_points. Each player's total_cards += count(captures) and total_coins += count of Co cards in captures. The hand's results are announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1."
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
    "rank_by": "you.score * 10000 + you.total_cards * 100 + you.total_coins",
    "decided_by": "Most total points across both hands wins. A tie goes to more total captured cards, then to more total captured Coins. If still tied, both players share the result (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When round is 1 or 19, then the deck is refilled to all 40 cards, 4 random cards go to table_cards, and each player's hand receives 3 random cards from the deck."
    },
    {
      "id": "R2",
      "text": "When round is 4, 7, 10, 13, 16, 22, 25, 28, 31 or 34, then each player receives 3 cards from the deck into their hand."
    },
    {
      "id": "R3",
      "text": "When round <= 18, then seat 1 plays first (Leader) and seat 2 plays second (Dealer); when round >= 19, then seat 2 leads and seat 1 deals."
    },
    {
      "id": "R4",
      "text": "When a player plays a card and a table card has the same rank, then the declaration is legal only if it names exactly one such card, and that card plus the played card go to the player's captures."
    },
    {
      "id": "R5",
      "text": "When no table card has the same rank and the declared table cards' ranks sum exactly to the played card's rank, then those cards plus the played card go to the player's captures."
    },
    {
      "id": "R6",
      "text": "When a player declares nothing, then the played card is added to table_cards."
    },
    {
      "id": "R7",
      "text": "When a declaration is illegal (for example, a sum is declared while a same-rank card is on the table, or the ranks do not add up), then the played card is added to table_cards and nothing is captured."
    },
    {
      "id": "R8",
      "text": "When a legal non-empty capture leaves table_cards empty, then the capturer's scopa_points increase by 1, unless it is the Dealer's play in round 18 or 36."
    },
    {
      "id": "R9",
      "text": "When a player makes a legal non-empty capture, then last_capturer is set to that player's seat."
    },
    {
      "id": "R10",
      "text": "When round 18 or 36 ends, then the remaining table_cards go to last_capturer's captures, or are discarded if last_capturer is 0."
    },
    {
      "id": "R11",
      "text": "When a hand is scored, then the player with more captured cards gets 1 point, and nobody gets it at 20-20."
    },
    {
      "id": "R12",
      "text": "When a hand is scored, then the player with more captured Coins gets 1 point, and nobody gets it at 5-5."
    },
    {
      "id": "R13",
      "text": "When a hand is scored, then the player whose captures contain 7Co gets 1 point."
    },
    {
      "id": "R14",
      "text": "When a hand is scored, then the player with more sevens gets 1 point; if sevens are tied, the player with more sixes gets it; if both are tied, nobody does."
    },
    {
      "id": "R15",
      "text": "When a hand is scored, then each player's scopa_points are added to their score, and their captured card count and Coins count are added to total_cards and total_coins."
    },
    {
      "id": "R16",
      "text": "When hand 2 begins at round 19, then captures, scopa_points and last_capturer are reset, while score, total_cards and total_coins are kept."
    },
    {
      "id": "R17",
      "text": "When round 36 is complete, then the game ends and the higher score wins, tie-broken by total_cards and then total_coins; if all three are equal, it is a draw."
    }
  ],
  "offers": [
    {
      "question": "Choose a card to play",
      "who": "the Leader, then the Dealer",
      "options": "Every card currently in that seat's own hand, and nothing else."
    },
    {
      "question": "Declare the table cards you capture",
      "who": "the Leader, then the Dealer",
      "options": "Free text: a space-separated list of card codes currently in table_cards, or 'none'. Any declaration may be sent; an illegal one sends the played card to the table and captures nothing."
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (suggested 2)",
      "why": "The designer's rules are a duel: fixed Leader/Dealer roles and a 40-card count that assumes exactly two hands of play."
    },
    {
      "what": "No pre-play talk step",
      "why": "This is a zero-sum duel with no coordination; talk would only add words."
    },
    {
      "what": "Card codes such as '7Co', '10Sw'",
      "why": "A compact text form of rank and suit, so suit and rank counts are simple arithmetic."
    },
    {
      "what": "Play is split into a card choice and a text declaration",
      "why": "Choosing from the hand list guarantees a real card; the capture set has too many possible subsets to list as options."
    },
    {
      "what": "Seat 1 is Player A, seat 2 is Player B",
      "why": "The source names players A and B but not seats."
    },
    {
      "what": "Leftover cards with no last capturer are not counted for either player",
      "why": "The source says they are discarded."
    },
    {
      "what": "Round lists are given as single-number parameters (first round, last round and an interval of 3 for redeals)",
      "why": "Each parameter must be one number. The redeal rounds are first_redeal_round plus multiples of redeal_interval, up to last_redeal_round."
    }
  ],
  "simplifications": [
    {
      "what": "Capture legality is decided by a judged referee sentence",
      "why": "Checking for a same-rank card and an exact subset sum over parsed text is too complex for a single arithmetic check. The effects of the ruling are still arithmetic."
    },
    {
      "what": "The three-step tie-break is folded into one rank expression: score*10000 + total_cards*100 + total_coins",
      "why": "rank_by must be a single expression. total_cards and total_coins never reach 100, so the order of the tie-breaks is preserved."
    },
    {
      "what": "A complete tie is a shared win",
      "why": "The engine treats players level at the top as sharing the win, which is equivalent to a draw."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, total_cards, total_coins; table: table_cards, round.
````

## Reply

````
```json
[
  {
    "name": "R1: round 1 deals 4 table cards and 3 to each hand; with no captures both played cards stay on the table (only counts asserted, the deal is random)",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {
        "game": {"deck": 30, "table_cards": 6},
        "players": {"1": {"hand": 2, "captures": 0}, "2": {"hand": 2, "captures": 0}}
      },
      "game": {"round": 2}
    }
  },
  {
    "name": "R1: round 19 refills the deck to 40 and deals afresh (only counts asserted)",
    "rule": "R1",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [], "captures": ["1Cu", "2Cu"]},
        "2": {"hand": [], "captures": ["3Cu"]}
      },
      "game": {"round": 19, "deck": [], "table_cards": ["9Sw"]}
    },
    "rules": [],
    "expect": {
      "lens": {
        "game": {"deck": 30, "table_cards": 6},
        "players": {"1": {"hand": 2, "captures": 0}, "2": {"hand": 2, "captures": 0}}
      },
      "game": {"round": 20}
    }
  },
  {
    "name": "R2: round 4 deals 3 cards to each player from the deck",
    "rule": "R2",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": []}, "2": {"hand": []}},
      "game": {"round": 4, "table_cards": [], "deck": ["1Cu", "2Cu", "3Cu", "4Cu", "5Cu", "6Cu"]}
    },
    "rules": [],
    "expect": {
      "lens": {
        "game": {"deck": 0, "table_cards": 2},
        "players": {"1": {"hand": 2}, "2": {"hand": 2}}
      },
      "game": {"round": 5}
    }
  },
  {
    "name": "R3: in hand 1 seat 1 leads, so its card reaches the table first",
    "rule": "R3",
    "players": 2,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": ["5Sw"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 2, "table_cards": [], "deck": []}
    },
    "rules": [],
    "expect": {
      "game": {"table_cards": ["5Sw", "9Cl"], "round": 3}
    }
  },
  {
    "name": "R3: in hand 2 seat 2 leads, so its card reaches the table first",
    "rule": "R3",
    "players": 2,
    "seed": 5,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": ["5Sw"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 20, "table_cards": [], "deck": []}
    },
    "rules": [],
    "expect": {
      "game": {"table_cards": ["9Cl", "5Sw"], "round": 21}
    }
  },
  {
    "name": "R4: a 7 captures the matching 7 on the table",
    "rule": "R4",
    "players": 2,
    "seed": 6,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {"1": {"hand": ["7Co"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 2, "table_cards": ["7Cu", "3Sw"], "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "7Cu"},
      {"seat": 2, "options_include": "none"}
    ],
    "expect": {
      "game": {"table_cards": ["3Sw", "9Cl"], "round": 3},
      "lens": {"players": {"1": {"captures": 2, "hand": 0}, "2": {"captures": 0}}}
    }
  },
  {
    "name": "R5: a 7 captures 3 and 4 by sum",
    "rule": "R5",
    "players": 2,
    "seed": 7,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {"1": {"hand": ["7Co"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 2, "table_cards": ["3Sw", "4Cu", "1Cl"], "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "3Sw 4Cu"},
      {"seat": 2, "options_include": "none"}
    ],
    "expect": {
      "game": {"table_cards": ["1Cl", "9Cl"], "round": 3},
      "lens": {"players": {"1": {"captures": 3}, "2": {"captures": 0}}}
    }
  },
  {
    "name": "R6: declaring none adds the played cards to the table",
    "rule": "R6",
    "players": 2,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {"1": {"hand": ["5Sw"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 2, "table_cards": ["5Cu"], "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": "none"},
      {"seat": 2, "options_include": "none"}
    ],
    "expect": {
      "game": {"table_cards": ["5Cu", "5Sw", "9Cl"], "round": 3},
      "lens": {"players": {"1": {"captures": 0}, "2": {"captures": 0}}}
    }
  },
  {
    "name": "R7: an illegal declaration sends the played card to the table and captures nothing",
    "rule": "R7",
    "players": 2,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": ["5Sw"]}, "2": {"hand": ["9Cl"]}},
      "game": {"round": 2, "table_cards": ["5Cu"], "deck": []}
    },
    "rules": [],
    "expect": {
      "game": {"table_cards": ["5Cu", "5Sw", "9Cl"], "round": 3},
      "lens": {"players": {"1": {"captures": 0}, "2": {"captures": 0}}}
    }
  },
  {
    "name": "R8: the Leader's sweep in round 18 scores a Scopa",
    "rule": "R8",
    "players": 2,
    "seed": 10,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["5Sw"], "captures": [], "scopa_points": 0},
        "2": {"hand": ["9Cl"], "captures": [], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": ["5Cu"], "deck": [], "last_capturer": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "5Cu"},
      {"seat": 2, "options_include": "none"}
    ],
    "expect": {
      "players": {
        "1": {"score": 2, "total_cards": 3, "total_coins": 0},
        "2": {"score": 0, "total_cards": 0, "total_coins": 0}
      },
      "game": {"table_cards": [], "round": 19}
    }
  },
  {
    "name": "R8: the Dealer's sweep in round 18 scores no Scopa",
    "rule": "R8",
    "players": 2,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["3Cl"], "captures": [], "scopa_points": 0},
        "2": {"hand": ["5Sw"], "captures": [], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": ["2Cu"], "deck": [], "last_capturer": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "none"},
      {"seat": 2, "options_include": "2Cu 3Cl"}
    ],
    "expect": {
      "players": {
        "1": {"score": 0, "total_cards": 0, "total_coins": 0},
        "2": {"score": 1, "total_cards": 3, "total_coins": 0}
      },
      "game": {"table_cards": [], "round": 19}
    }
  },
  {
    "name": "R9: a capture makes the capturer last_capturer, so it takes the leftovers",
    "rule": "R9",
    "players": 2,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "judge": {"The declaration is legal": true},
    "given": {
      "players": {
        "1": {"hand": ["5Sw"], "captures": [], "scopa_points": 0},
        "2": {"hand": ["1Cl"], "captures": [], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": ["5Cu", "9Sw"], "deck": [], "last_capturer": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "5Cu"},
      {"seat": 2, "options_include": "none"}
    ],
    "expect": {
      "players": {
        "1": {"score": 1, "total_cards": 4, "total_coins": 0},
        "2": {"score": 0, "total_cards": 0, "total_coins": 0}
      },
      "game": {"table_cards": [], "round": 19}
    }
  },
  {
    "name": "R10: leftover table cards go to last_capturer at the end of round 18",
    "rule": "R10",
    "players": 2,
    "seed": 13,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["3Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": ["4Sw", "5Sw"], "deck": [], "last_capturer": 2}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 0, "total_cards": 2, "total_coins": 0},
        "2": {"score": 1, "total_cards": 5, "total_coins": 0}
      },
      "game": {"table_cards": [], "round": 19}
    }
  },
  {
    "name": "R10: leftover table cards are discarded when there is no last capturer",
    "rule": "R10",
    "players": 2,
    "seed": 14,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["3Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": ["4Sw", "5Sw"], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 1, "total_cards": 2, "total_coins": 0},
        "2": {"score": 0, "total_cards": 1, "total_coins": 0}
      },
      "game": {"table_cards": [], "round": 19}
    }
  },
  {
    "name": "R11: more captured cards earns 1 point",
    "rule": "R11",
    "players": 2,
    "seed": 15,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu", "3Cu"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["4Cu", "5Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 1, "total_cards": 3, "total_coins": 0},
        "2": {"score": 0, "total_cards": 2, "total_coins": 0}
      }
    }
  },
  {
    "name": "R11: equal captured card counts earn nobody the point",
    "rule": "R11",
    "players": 2,
    "seed": 16,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["4Cu", "5Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 0, "total_cards": 2},
        "2": {"score": 0, "total_cards": 2}
      }
    }
  },
  {
    "name": "R12: more captured Coins earns 1 point",
    "rule": "R12",
    "players": 2,
    "seed": 17,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Co", "2Cu"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["3Cu", "4Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 1, "total_cards": 2, "total_coins": 1},
        "2": {"score": 0, "total_cards": 2, "total_coins": 0}
      }
    }
  },
  {
    "name": "R13: the holder of 7Co earns 1 point",
    "rule": "R13",
    "players": 2,
    "seed": 18,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["7Cu", "1Co"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["7Co", "2Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 0, "total_cards": 2, "total_coins": 1},
        "2": {"score": 1, "total_cards": 2, "total_coins": 1}
      }
    }
  },
  {
    "name": "R14: more sevens earns 1 point",
    "rule": "R14",
    "players": 2,
    "seed": 19,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["7Cu", "7Sw"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"score": 1}, "2": {"score": 0}}
    }
  },
  {
    "name": "R14: with sevens tied, more sixes earns the point",
    "rule": "R14",
    "players": 2,
    "seed": 20,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["7Cu", "6Sw"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["7Sw", "1Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"score": 1}, "2": {"score": 0}}
    }
  },
  {
    "name": "R14: with sevens and sixes both tied, nobody earns the point",
    "rule": "R14",
    "players": 2,
    "seed": 21,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["7Cu", "6Sw"], "scopa_points": 0},
        "2": {"hand": ["2Sw"], "captures": ["7Sw", "6Cu"], "scopa_points": 0}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}}
    }
  },
  {
    "name": "R15: scopa_points, card count and Coins count are added to the running totals",
    "rule": "R15",
    "players": 2,
    "seed": 22,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 2, "score": 1, "total_cards": 10, "total_coins": 2},
        "2": {"hand": ["2Sw"], "captures": ["3Cu", "4Cu"], "scopa_points": 0, "score": 0, "total_cards": 5, "total_coins": 1}
      },
      "game": {"round": 18, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 3, "total_cards": 12, "total_coins": 2},
        "2": {"score": 0, "total_cards": 7, "total_coins": 1}
      },
      "game": {"round": 19}
    }
  },
  {
    "name": "R16: hand 2 resets captures but keeps score, total_cards and total_coins",
    "rule": "R16",
    "players": 2,
    "seed": 23,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [], "captures": ["1Cu", "2Cu"], "scopa_points": 1, "score": 3, "total_cards": 20, "total_coins": 5},
        "2": {"hand": [], "captures": ["3Cu"], "scopa_points": 0, "score": 2, "total_cards": 18, "total_coins": 4}
      },
      "game": {"round": 19, "table_cards": [], "deck": [], "last_capturer": 1}
    },
    "rules": [],
    "expect": {
      "players": {
        "1": {"score": 3, "total_cards": 20, "total_coins": 5},
        "2": {"score": 2, "total_cards": 18, "total_coins": 4}
      },
      "lens": {"players": {"1": {"captures": 0}, "2": {"captures": 0}}},
      "game": {"round": 20}
    }
  },
  {
    "name": "R17: after round 36, a tie on score is broken by total_cards",
    "rule": "R17",
    "players": 2,
    "seed": 24,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0, "score": 5, "total_cards": 18, "total_coins": 4},
        "2": {"hand": ["2Sw"], "captures": ["3Cu", "4Cu"], "scopa_points": 0, "score": 5, "total_cards": 20, "total_coins": 6}
      },
      "game": {"round": 36, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "winner": 2,
      "standings": {"1": 52004, "2": 52206},
      "players": {
        "1": {"score": 5, "total_cards": 20, "total_coins": 4},
        "2": {"score": 5, "total_cards": 22, "total_coins": 6}
      }
    }
  },
  {
    "name": "R17: when score, total_cards and total_coins are all equal, both seats share the result",
    "rule": "R17",
    "players": 2,
    "seed": 25,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": ["1Sw"], "captures": ["1Cu", "2Cu"], "scopa_points": 0, "score": 5, "total_cards": 18, "total_coins": 4},
        "2": {"hand": ["2Sw"], "captures": ["3Cu", "4Cu"], "scopa_points": 0, "score": 5, "total_cards": 18, "total_coins": 4}
      },
      "game": {"round": 36, "table_cards": [], "deck": [], "last_capturer": 0}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 52004, "2": 52004}
    }
  }
]
```
````
