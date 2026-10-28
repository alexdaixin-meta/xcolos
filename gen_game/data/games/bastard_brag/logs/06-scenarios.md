# 06 scenarios

- time: 2026-10-28T01:48:39+00:00 (131.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 b184bfe5643290b2, reply sha256 79637399d9186853

## Sent

````
SPEC:
{
  "name": "Knock Brag (3-player)",
  "summary": "Three players swap cards with a shared three-card table hand to build the best Brag hand; the leader may knock to force a showdown, the lowest hand at each showdown loses lives, and the last player with lives wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "starting_lives": 3,
    "deck_size": 36,
    "copies_per_value": 4,
    "lowest_card_value": 1,
    "highest_card_value": 9,
    "hand_size": 3,
    "table_cards": 3,
    "max_rounds": 40,
    "prial_base": 300,
    "prial_333_score": 310,
    "run_base": 200,
    "run_123_score": 210,
    "pair_base": 100,
    "pair_multiplier": 10,
    "knock_min_deal_round": 2,
    "life_loss_lowest": 1,
    "life_loss_knocker_lowest": 2,
    "forced_showdown_offset": 1,
    "rank_lives_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "lives",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "Lives remaining. The player is eliminated at 0. It is never set below 0.",
        "observable": true
      },
      {
        "key": "eliminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True once lives reach 0. An eliminated player takes no further part.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's 3 card values, as positions 1 to 3, seen only by the owner until the showdown.",
        "observable": false
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The hand's Brag score, computed and shown at each showdown.",
        "observable": false
      },
      {
        "key": "last_showdown_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's score at the most recent showdown. Used as the tie-break on lives.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          3,
          3,
          3,
          3,
          4,
          4,
          4,
          4,
          5,
          5,
          5,
          5,
          6,
          6,
          6,
          6,
          7,
          7,
          7,
          7,
          8,
          8,
          8,
          8,
          9,
          9,
          9,
          9
        ],
        "meaning": "The 36-card deck. It is rebuilt and dealt from at the start of each deal. Undealt cards are unused.",
        "observable": false
      },
      {
        "key": "table_up",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The face-up table card in slot U.",
        "observable": true
      },
      {
        "key": "table_d1",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "The face-down table card in slot D1, seen by nobody.",
        "observable": false
      },
      {
        "key": "table_d2",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "The face-down table card in slot D2, seen by nobody.",
        "observable": false
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current round, from 1 to 40.",
        "observable": true
      },
      {
        "key": "deal_round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The round number within the current deal.",
        "observable": true
      },
      {
        "key": "leader_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that leads this round.",
        "observable": true
      },
      {
        "key": "knocker_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that knocked in this deal, or 0 if nobody has knocked.",
        "observable": true
      },
      {
        "key": "active_count",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "The number of players not eliminated.",
        "observable": true
      },
      {
        "key": "showdown_now",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when this round ends in a showdown.",
        "observable": false
      },
      {
        "key": "lowest_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The lowest hand_score among active players at the showdown.",
        "observable": false
      },
      {
        "key": "highest_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest hand_score among active players at the showdown.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 sit clockwise. Each player starts with 3 lives and is active.",
    "round_number = 1, deal_round = 1, leader_seat = 1, knocker_seat = 0, active_count = 3.",
    "Every player's last_showdown_score is 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When deal_round == 1 (a new deal): rebuild deck as the 36 cards (four each of 1 to 9). Empty every hand. For each active player, draw 3 cards at random from deck into their hand. Then draw 1 card each into table_up, table_d1 and table_d2. Set knocker_seat = 0. The rest of deck is unused this deal."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When deal_round == 1: announce 'New deal. The face-up card U is {table_up}.'"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand, table_up, lives, deal_round, leader_seat and knocker_seat."
    },
    {
      "action": "ask",
      "who": "each active player in turn, clockwise starting at leader_seat and skipping eliminated seats",
      "answer": "One choice from: take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3, knock. Knock is offered only to the leader when deal_round >= 2.",
      "effect": "take_up_give_k: swap hand[k] with table_up, then announce 'Seat X took the face-up [old U] and left a face-up [new U]'. blind_Dj_give_k: swap hand[k] with table_dj; the player now sees the received card in their hand; announce 'Seat X made a blind swap with Dj'. whole_hand_expose_k: the old hand [h1,h2,h3] becomes the table and the hand becomes [table_up, table_d1, table_d2]; table_up = old hk, and the other two old cards go to table_d1 and table_d2 in order; announce 'Seat X swapped the whole hand and exposed a [table_up]'. knock: no exchange, set knocker_seat = the leader's seat, announce 'Seat X knocks'. Each effect applies before the next player is asked."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "showdown_now = (knocker_seat > 0) or (deal_round == active_count + 1)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When showdown_now: for each active player, let a = min(hand), c = max(hand), b = sum(hand) - a - c. Then hand_score = 310 if a == 3 and c == 3; else 300 + a if a == c; else 210 if a == 1 and b == 2 and c == 3; else 200 + c if b == a + 1 and c == b + 1; else 100 + 10*b + (a + c - b) if a == b or b == c; else a + b + c. Set last_showdown_score = hand_score. Set lowest_score = min and highest_score = max of hand_score over active players."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When showdown_now: reveal every active player's hand and announce 'Seat X shows [hand] scoring {hand_score}' for each."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When showdown_now and lowest_score < highest_score: each active player with hand_score == lowest_score loses 2 lives if their seat == knocker_seat, otherwise 1 life. Lives are floored at 0. Any player with lives == 0 gets eliminated = true. Recompute active_count as the number of players not eliminated. Announce each life lost and each elimination."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If showdown_now, deal_round = 1; otherwise deal_round = deal_round + 1. Then round_number = round_number + 1, and leader_seat = the next seat clockwise after leader_seat that is not eliminated."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if active_count <= 1 or round_number > 40; otherwise continue."
    }
  ],
  "ending": {
    "condition": "active_count <= 1 or round_number > 40",
    "rank_by": "you.lives * 1000 + you.last_showdown_score",
    "decided_by": "Most lives wins. A lone survivor is the only player with lives above 0. A tie on lives is broken by the higher last showdown score, and players still level share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, each of the 3 players has 3 lives, seat 1 leads round 1, and deal_round is 1."
    },
    {
      "id": "R2",
      "text": "When a deal starts (round 1, or the round after a showdown), the 36-card deck (four each of 1 to 9) is shuffled, each active player gets 3 private cards, and table_up, table_d1 and table_d2 get 1 card each, with table_up announced."
    },
    {
      "id": "R3",
      "text": "When a hand sorted a<=b<=c has a == c, then it scores 300 + a, except 3-3-3, which scores 310."
    },
    {
      "id": "R4",
      "text": "When a hand has b == a+1 and c == b+1, then it scores 200 + c, except 1-2-3, which scores 210; 8-9-1 and 9-1-2 are not runs."
    },
    {
      "id": "R5",
      "text": "When a hand has a == b or b == c but is not a prial, then it scores 100 + 10*b + (a + c - b); for example, 5-5-2 scores 152."
    },
    {
      "id": "R6",
      "text": "When a hand is no prial, run or pair, then it scores a + b + c; for example, 2-5-9 scores 16."
    },
    {
      "id": "R7",
      "text": "When a player takes up giving card k, then hand[k] and table_up are swapped and the new table_up is announced."
    },
    {
      "id": "R8",
      "text": "When a player makes a blind swap with Dj giving card k, then hand[k] and table_dj are swapped, only that player sees the received card, and only the slot is announced."
    },
    {
      "id": "R9",
      "text": "When a player swaps the whole hand exposing old card k, then the hand becomes the three table cards, old card k becomes table_up, the other two old cards go face down to D1 and D2, and the exposed value is announced."
    },
    {
      "id": "R10",
      "text": "When the leader acts and deal_round >= 2, then knock is offered; no other player, and no leader in deal_round 1, may knock."
    },
    {
      "id": "R11",
      "text": "When the leader knocks, then the players after them that round must take up, blind swap or whole-hand swap, and the showdown happens at the end of that round."
    },
    {
      "id": "R12",
      "text": "When nobody has knocked and deal_round == active_count + 1 (4 with 3 active, 3 with 2 active), then a showdown happens at the end of the round."
    },
    {
      "id": "R13",
      "text": "When there is a showdown, then every active hand is revealed and scored, and each score is recorded as that player's last_showdown_score."
    },
    {
      "id": "R14",
      "text": "When all active scores at a showdown are equal, then nobody loses a life."
    },
    {
      "id": "R15",
      "text": "When scores at a showdown differ, then every player on the lowest score loses 1 life, except a knocker on the lowest score, who loses 2."
    },
    {
      "id": "R16",
      "text": "When a player's lives reach 0 or fewer, then lives is set to 0 and the player is eliminated and takes no further part."
    },
    {
      "id": "R17",
      "text": "When a round ends, then the next leader is the next non-eliminated seat clockwise from the current leader, and deal_round resets to 1 after a showdown or rises by 1 otherwise."
    },
    {
      "id": "R18",
      "text": "When only one active player remains, then the game ends and that player wins."
    },
    {
      "id": "R19",
      "text": "When round 40 ends with 2 or 3 active players, then the player with the most lives wins, a tie is broken by the higher last_showdown_score, and a remaining tie is a shared draw."
    }
  ],
  "offers": [
    {
      "question": "Your action this round",
      "who": "the leader (leader_seat) when deal_round >= 2",
      "options": "take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3, knock"
    },
    {
      "question": "Your action this round",
      "who": "the leader when deal_round == 1, and every other active seat (including after a knock)",
      "options": "take_up_give_1, take_up_give_2, take_up_give_3, blind_D1_give_1, blind_D1_give_2, blind_D1_give_3, blind_D2_give_1, blind_D2_give_2, blind_D2_give_3, whole_hand_expose_1, whole_hand_expose_2, whole_hand_expose_3"
    },
    {
      "question": "Your action this round",
      "who": "eliminated seats",
      "options": "not asked"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the game at 3, and the forced-showdown timing and leader rotation are written for it. A 3-seat table already gives rivals whose swaps and exposed cards can be read. The player's strategy is to infer opponents' hands from what they take and leave face up, to decide when to knock, and to avoid feeding a strong card into U."
    },
    {
      "what": "No free-talk step before actions",
      "why": "The source has no talk, and adding it would add a mechanic."
    },
    {
      "what": "Cards are named by hand position 1 to 3 in the choice options",
      "why": "Each action must be a single choice carrying every detail. The player sees their hand list, so a position identifies the card."
    },
    {
      "what": "Lives are floored at 0 when a loss would make them negative",
      "why": "The player is eliminated either way, and flooring keeps the ranking expression clean without changing who wins."
    },
    {
      "what": "Whole-hand swap puts the two unexposed old cards into D1 then D2 in their hand order",
      "why": "The source does not say which goes where. Nobody sees D1 or D2, so the order does not matter."
    },
    {
      "what": "rank_by = lives*1000 + last_showdown_score",
      "why": "Scores are at most 310, so lives always dominate and the showdown score breaks ties. Eliminated players have 0 lives and cannot tie with a survivor. A showdown happens at least every 4 rounds, so by round 40 one has always occurred."
    }
  ],
  "simplifications": [
    {
      "what": "The turn order is one ask step running clockwise from leader_seat and skipping eliminated seats, rather than fixed seat order",
      "why": "The engine asks in a flat sequence; the starting seat is taken from the table attribute leader_seat."
    },
    {
      "what": "Hand reveal at showdown is an announcement listing each active hand and score, not a change of the hand's visibility",
      "why": "The engine reveals through messages; hand_score is public."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: lives, eliminated, last_showdown_score; table: table_up, round_number, deal_round, leader_seat, knocker_seat, active_count.
````

## Reply

````
```json
[
  {
    "name": "Game starts with 3 lives each, seat 1 leading, deal_round 1",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "rules": [],
    "expect": {
      "players": {
        "1": {"lives": 3, "eliminated": false, "last_showdown_score": 0},
        "2": {"lives": 3, "eliminated": false, "last_showdown_score": 0},
        "3": {"lives": 3, "eliminated": false, "last_showdown_score": 0}
      },
      "game": {"round_number": 1, "deal_round": 1, "leader_seat": 1, "knocker_seat": 0, "active_count": 3}
    }
  },
  {
    "name": "First deal gives 3 cards to each player and 3 to the table (random cards, only counts asserted)",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {
        "game": {"deck": 24},
        "players": {"1": {"hand": 3}, "2": {"hand": 3}, "3": {"hand": 3}}
      },
      "game": {"deal_round": 2, "round_number": 2, "leader_seat": 2, "active_count": 3}
    }
  },
  {
    "name": "Prials score 300+a and 3-3-3 scores 310",
    "rule": "R3",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [5, 5, 5]}, "2": {"hand": [3, 3, 3]}, "3": {"hand": [2, 4, 9]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 5, "table_d1": 3, "table_d2": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 305, "lives": 3},
        "2": {"last_showdown_score": 310, "lives": 3},
        "3": {"last_showdown_score": 15, "lives": 2}
      }
    }
  },
  {
    "name": "Runs score 200+c, 1-2-3 scores 210, 9-1-2 is not a run",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 2, 3]}, "2": {"hand": [7, 8, 9]}, "3": {"hand": [9, 1, 2]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 1, "table_d1": 7, "table_d2": 9}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 210, "lives": 3},
        "2": {"last_showdown_score": 209, "lives": 3},
        "3": {"last_showdown_score": 12, "lives": 2}
      }
    }
  },
  {
    "name": "8-9-1 is not a run; 4-5-6 and unsorted 3-2-4 are runs",
    "rule": "R4",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [8, 9, 1]}, "2": {"hand": [4, 5, 6]}, "3": {"hand": [3, 2, 4]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 8, "table_d1": 4, "table_d2": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 18, "lives": 2},
        "2": {"last_showdown_score": 206, "lives": 3},
        "3": {"last_showdown_score": 204, "lives": 3}
      }
    }
  },
  {
    "name": "Pairs score 100 + 10*b + (a+c-b)",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [5, 5, 2]}, "2": {"hand": [2, 9, 9]}, "3": {"hand": [4, 4, 9]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 5, "table_d1": 2, "table_d2": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 152, "lives": 3},
        "2": {"last_showdown_score": 192, "lives": 3},
        "3": {"last_showdown_score": 149, "lives": 2}
      }
    }
  },
  {
    "name": "High-card hands score the sum of the cards",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [2, 5, 9]}, "2": {"hand": [1, 4, 6]}, "3": {"hand": [3, 7, 8]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 2, "table_d1": 1, "table_d2": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 16, "lives": 3},
        "2": {"last_showdown_score": 11, "lives": 2},
        "3": {"last_showdown_score": 18, "lives": 3}
      }
    }
  },
  {
    "name": "Take up giving card 2 leaves that card face up",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [4, 6, 8]}, "2": {"hand": [1, 2, 3]}, "3": {"hand": [5, 5, 7]}},
      "game": {"deal_round": 2, "round_number": 2, "leader_seat": 1, "knocker_seat": 0, "table_up": 7, "table_d1": 1, "table_d2": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_2"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "game": {"table_up": 6, "deal_round": 3, "round_number": 3, "leader_seat": 2},
      "players": {"1": {"lives": 3}, "2": {"lives": 3}, "3": {"lives": 3}}
    }
  },
  {
    "name": "Blind swap with D1 changes the hand but not the face-up card",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [4, 6, 8]}, "2": {"hand": [3, 3, 7]}, "3": {"hand": [3, 1, 5]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 7, "table_d1": 4, "table_d2": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "blind_D1_give_3"},
      {"seat": 2, "options_include": "blind_D2_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "game": {"table_up": 7},
      "players": {
        "1": {"last_showdown_score": 146, "lives": 3},
        "2": {"last_showdown_score": 137, "lives": 3},
        "3": {"last_showdown_score": 9, "lives": 2}
      }
    }
  },
  {
    "name": "Whole-hand swap takes the three table cards and exposes old card 1",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [2, 6, 9]}, "2": {"hand": [6, 1, 2]}, "3": {"hand": [9, 8, 7]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 4, "table_d1": 4, "table_d2": 4}
    },
    "rules": [
      {"seat": 1, "options_include": "whole_hand_expose_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "game": {"table_up": 2},
      "players": {
        "1": {"last_showdown_score": 304, "lives": 3},
        "2": {"last_showdown_score": 9, "lives": 2},
        "3": {"last_showdown_score": 209, "lives": 3}
      }
    }
  },
  {
    "name": "Nobody may knock in deal_round 1",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "not_offered": [
        {"seat": 1, "option": "knock"},
        {"seat": 2, "option": "knock"},
        {"seat": 3, "option": "knock"}
      ],
      "offered": [{"seat": 1, "option": "take_up_give_1"}]
    }
  },
  {
    "name": "Only the leader is offered knock in deal_round 2",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {"1": {"hand": [4, 6, 8]}, "2": {"hand": [1, 2, 3]}, "3": {"hand": [5, 5, 7]}},
      "game": {"deal_round": 2, "round_number": 2, "leader_seat": 1, "knocker_seat": 0, "table_up": 7, "table_d1": 1, "table_d2": 5}
    },
    "rules": [],
    "expect": {
      "offered": [{"seat": 1, "option": "knock"}],
      "not_offered": [
        {"seat": 2, "option": "knock"},
        {"seat": 3, "option": "knock"}
      ],
      "game": {"deal_round": 3, "knocker_seat": 0}
    }
  },
  {
    "name": "A knock forces a showdown at the end of the round; others still swap",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [5, 5, 5]}, "2": {"hand": [2, 4, 9]}, "3": {"hand": [7, 7, 1]}},
      "game": {"deal_round": 2, "round_number": 2, "leader_seat": 1, "knocker_seat": 0, "table_up": 3, "table_d1": 2, "table_d2": 7}
    },
    "rules": [
      {"seat": 1, "options_include": "knock"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "game": {"knocker_seat": 1, "deal_round": 1, "table_up": 3},
      "players": {
        "1": {"last_showdown_score": 305, "lives": 3},
        "2": {"last_showdown_score": 15, "lives": 2},
        "3": {"last_showdown_score": 171, "lives": 3}
      },
      "not_offered": [
        {"seat": 2, "option": "knock"},
        {"seat": 3, "option": "knock"}
      ]
    }
  },
  {
    "name": "With 2 active players a showdown happens at deal_round 3",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [5, 5, 5]},
        "2": {"hand": [2, 4, 9]},
        "3": {"lives": 0, "eliminated": true}
      },
      "game": {"deal_round": 3, "round_number": 5, "leader_seat": 1, "knocker_seat": 0, "active_count": 2, "table_up": 5, "table_d1": 2, "table_d2": 8}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 305, "lives": 3},
        "2": {"last_showdown_score": 15, "lives": 2},
        "3": {"lives": 0, "eliminated": true}
      },
      "game": {"deal_round": 1, "round_number": 6, "leader_seat": 2},
      "not_offered": [{"seat": 3, "option": "take_up_give_1"}]
    }
  },
  {
    "name": "With 3 active players there is no showdown at deal_round 3",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [5, 5, 5]}, "2": {"hand": [2, 4, 9]}, "3": {"hand": [3, 7, 8]}},
      "game": {"deal_round": 3, "round_number": 3, "leader_seat": 1, "knocker_seat": 0, "table_up": 5, "table_d1": 2, "table_d2": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"lives": 3, "last_showdown_score": 0},
        "2": {"lives": 3, "last_showdown_score": 0},
        "3": {"lives": 3, "last_showdown_score": 0}
      },
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 2}
    }
  },
  {
    "name": "Showdown records every active score, leader 2 acting first",
    "rule": "R13",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [6, 6, 3]}, "2": {"hand": [4, 5, 6]}, "3": {"hand": [1, 7, 8]}},
      "game": {"deal_round": 4, "round_number": 8, "leader_seat": 2, "knocker_seat": 0, "table_up": 4, "table_d1": 1, "table_d2": 6}
    },
    "rules": [
      {"seat": 2, "options_include": "take_up_give_1"},
      {"seat": 3, "options_include": "blind_D1_give_1"},
      {"seat": 1, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 163, "lives": 3},
        "2": {"last_showdown_score": 206, "lives": 3},
        "3": {"last_showdown_score": 16, "lives": 2}
      },
      "game": {"deal_round": 1, "round_number": 9, "leader_seat": 3}
    }
  },
  {
    "name": "All scores equal at showdown: nobody loses a life",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [2, 5, 8]}, "2": {"hand": [1, 6, 8]}, "3": {"hand": [3, 4, 8]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 2, "table_d1": 1, "table_d2": 3}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 15, "lives": 3},
        "2": {"last_showdown_score": 15, "lives": 3},
        "3": {"last_showdown_score": 15, "lives": 3}
      }
    }
  },
  {
    "name": "A knocker with the lowest hand loses 2 lives",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 2, 4]}, "2": {"hand": [5, 5, 5]}, "3": {"hand": [2, 4, 9]}},
      "game": {"deal_round": 2, "round_number": 2, "leader_seat": 1, "knocker_seat": 0, "table_up": 6, "table_d1": 5, "table_d2": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "knock"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 7, "lives": 1},
        "2": {"last_showdown_score": 305, "lives": 3},
        "3": {"last_showdown_score": 15, "lives": 3}
      }
    }
  },
  {
    "name": "Two players tied on the lowest score each lose 1 life",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [2, 4, 9]}, "2": {"hand": [1, 5, 9]}, "3": {"hand": [8, 8, 8]}},
      "game": {"deal_round": 4, "round_number": 4, "leader_seat": 1, "knocker_seat": 0, "table_up": 2, "table_d1": 1, "table_d2": 8}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"last_showdown_score": 15, "lives": 2},
        "2": {"last_showdown_score": 15, "lives": 2},
        "3": {"last_showdown_score": 308, "lives": 3}
      }
    }
  },
  {
    "name": "A knocker on 1 life who is lowest drops to 0 and is eliminated",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [1, 2, 4], "lives": 1}, "2": {"hand": [5, 5, 5]}, "3": {"hand": [2, 4, 9]}},
      "game": {"deal_round": 2, "round_number": 6, "leader_seat": 1, "knocker_seat": 0, "table_up": 6, "table_d1": 5, "table_d2": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "knock"},
      {"seat": 2, "options_include": "blind_D1_give_1"},
      {"seat": 3, "options_include": "blind_D2_give_1"}
    ],
    "expect": {
      "players": {
        "1": {"lives": 0, "eliminated": true, "last_showdown_score": 7},
        "2": {"lives": 3, "eliminated": false},
        "3": {"lives": 3, "eliminated": false}
      },
      "game": {"active_count": 2, "leader_seat": 2, "deal_round": 1}
    }
  },
  {
    "name": "Leadership skips an eliminated seat and deal_round rises without a showdown",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 6, 8]},
        "2": {"lives": 0, "eliminated": true},
        "3": {"hand": [1, 2, 3]}
      },
      "game": {"deal_round": 2, "round_number": 5, "leader_seat": 1, "knocker_seat": 0, "active_count": 2, "table_up": 7, "table_d1": 1, "table_d2": 5}
    },
    "rules": [],
    "expect": {
      "game": {"leader_seat": 3, "deal_round": 3, "round_number": 6, "active_count": 2},
      "players": {"1": {"lives": 3}, "2": {"lives": 0, "eliminated": true}, "3": {"lives": 3}},
      "not_offered": [{"seat": 2, "option": "take_up_give_1"}]
    }
  },
  {
    "name": "Last player with lives wins once the other survivor is eliminated",
    "rule": "R18",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [5, 5, 5]},
        "2": {"hand": [2, 4, 9], "lives": 1},
        "3": {"lives": 0, "eliminated": true}
      },
      "game": {"deal_round": 3, "round_number": 10, "leader_seat": 1, "knocker_seat": 0, "active_count": 2, "table_up": 5, "table_d1": 2, "table_d2": 8}
    },
    "rules": [
      {"seat": 1, "options_include": "take_up_give_1"},
      {"seat": 2, "options_include": "blind_D1_give_1"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 3305, "2": 15, "3": 0},
      "players": {
        "1": {"lives": 3},
        "2": {"lives": 0, "eliminated": true}
      },
      "game": {"active_count": 1}
    }
  },
  {
    "name": "After round 40 the tie on lives is broken by the last showdown score",
    "rule": "R19",
    "players": 3,
    "seed": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 6, 8], "lives": 2, "last_showdown_score": 150},
        "2": {"hand": [1, 2, 3], "lives": 2, "last_showdown_score": 120},
        "3": {"hand": [5, 5, 7], "lives": 1, "last_showdown_score": 300}
      },
      "game": {"deal_round": 2, "round_number": 40, "leader_seat": 1, "knocker_seat": 0, "table_up": 7, "table_d1": 1, "table_d2": 5}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 2150, "2": 2120, "3": 1300}
    }
  },
  {
    "name": "After round 40 players level on lives and score share the win",
    "rule": "R19",
    "players": 3,
    "seed": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [4, 6, 8], "lives": 2, "last_showdown_score": 150},
        "2": {"hand": [1, 2, 3], "lives": 2, "last_showdown_score": 150},
        "3": {"hand": [5, 5, 7], "lives": 1, "last_showdown_score": 300}
      },
      "game": {"deal_round": 2, "round_number": 40, "leader_seat": 1, "knocker_seat": 0, "table_up": 7, "table_d1": 1, "table_d2": 5}
    },
    "rules": [],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 2150, "2": 2150, "3": 1300}
    }
  }
]
```
````
