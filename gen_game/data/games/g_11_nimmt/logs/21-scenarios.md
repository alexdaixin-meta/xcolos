# 21 scenarios

- time: 2026-10-27T21:48:40+00:00 (101.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 2543be9c0544aad8, reply sha256 b95d67d7a7db694c

## Sent

````
SPEC:
{
  "name": "11 Nimmt: Two Hot Piles",
  "summary": "Each turn, place one card from a hidden hand on one of two shared piles where it fits; a player with no legal placement must take a pile's ox-heads as penalty, though taking a pile of 3 or more cards earns a bull worth -2. The lowest penalty minus twice bulls wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 3
  },
  "parameters": {
    "deck_size_3p": 30,
    "deck_size_4p": 40,
    "hand_size_3p": 9,
    "hand_size_4p": 8,
    "set_aside_3p": 1,
    "set_aside_4p": 6,
    "start_turns_per_seat_3p": 3,
    "start_turns_per_seat_4p": 2,
    "starting_piles": 2,
    "starting_pile_size": 1,
    "fit_min_distance": 1,
    "fit_max_distance": 10,
    "pile_room_limit": 5,
    "bull_pile_threshold": 3,
    "bull_value": 2,
    "ox_special_cards": 3,
    "ox_multiple_of_5": 2,
    "ox_other": 1,
    "special_card_1": 11,
    "special_card_2": 22,
    "special_card_3": 33,
    "starting_penalty": 0,
    "starting_bulls": 0
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards (numbers) in this player's private hand",
        "observable": false
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total ox-heads taken from piles",
        "observable": true
      },
      {
        "key": "bulls",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bulls earned by taking piles of 3 or more cards; each is worth -2 at the end",
        "observable": true
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final score so far: penalty - 2 * bulls (lower is better)",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck_size",
        "type": "number",
        "visible": "public",
        "initial": 30,
        "meaning": "N: 30 with 3 players, 40 with 4 players",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 9,
        "meaning": "H, which is also the number of rounds: 9 with 3 players, 8 with 4 players",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The shuffled undealt cards, used only during setup",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Cards set aside unseen that take no part in the game",
        "observable": false
      },
      {
        "key": "pile_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards in Pile A, in play order; the last card is the top",
        "observable": true
      },
      {
        "key": "pile_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards in Pile B, in play order; the last card is the top",
        "observable": true
      },
      {
        "key": "top_a",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Top card of Pile A",
        "observable": false
      },
      {
        "key": "top_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Top card of Pile B",
        "observable": false
      },
      {
        "key": "size_a",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in Pile A",
        "observable": false
      },
      {
        "key": "size_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in Pile B",
        "observable": false
      },
      {
        "key": "ox_a",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Ox-head total of Pile A",
        "observable": false
      },
      {
        "key": "ox_b",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Ox-head total of Pile B",
        "observable": false
      },
      {
        "key": "discarded",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards from taken piles, now out of the game",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round, from 1 to H",
        "observable": false
      },
      {
        "key": "current_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat whose turn it is",
        "observable": false
      },
      {
        "key": "turns_in_round",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Scratch counter of turns taken this round",
        "observable": false
      },
      {
        "key": "last_play",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Description of the latest turn: who played, which card, which pile, and whether it was a take",
        "observable": false
      }
    ]
  },
  "setup": [
    "Set deck_size N = 30 and hand_size H = 9 with 3 players, or N = 40 and H = 8 with 4 players.",
    "Fill deck with the cards 1 to N.",
    "Each card's ox value is 3 if it is 11, 22 or 33; otherwise 2 if it is a multiple of 5; otherwise 1.",
    "Deal each player H cards into hand, each one drawn at random from deck and removed from it.",
    "Draw one random card from deck into pile_a (top_a = that card, size_a = 1, ox_a = its ox), and one into pile_b (top_b, size_b = 1, ox_b = its ox). Both piles are public.",
    "Move every remaining deck card into set_aside (1 card with 3 players, 6 with 4). They are never seen and never used.",
    "Every player starts with penalty 0, bulls 0 and score 0, and round = 1.",
    "Sync each player's hand to that player only."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "current_seat = ((round - 1) mod number_of_players) + 1; turns_in_round = 0"
    },
    {
      "action": "ask",
      "who": "seat current_seat",
      "answer": "One option naming a card from own hand and a pile, e.g. '17 on A'. If the seat holds at least one placement (card c fits pile X, meaning (c - top_X) mod N is between 1 and 10, and size_X < 5), only placements are offered. Otherwise every card in hand on A and on B is offered, each marked as a take.",
      "effect": "Records the chosen card c and pile X"
    },
    {
      "action": "update",
      "who": "seat current_seat",
      "answer": null,
      "effect": "Remove c from hand. If c fits X ((c - top_X) mod N in 1..10) and size_X < 5 (a placement): append c to pile_X, top_X = c, size_X += 1, ox_X += ox(c). Otherwise (a take): penalty += ox_X; if size_X >= 3 then bulls += 1; move all of pile_X into discarded; pile_X = [c], top_X = c, size_X = 1, ox_X = ox(c). The other pile is unchanged. Then score = penalty - 2 * bulls, and last_play describes the move."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce last_play, both piles (cards, top, size, ox total) and every player's penalty, bulls and score."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "current_seat = (current_seat mod number_of_players) + 1; turns_in_round += 1"
    },
    {
      "action": "repeat",
      "who": "table",
      "answer": null,
      "effect": "Repeat steps 2 to 5 until turns_in_round = number_of_players."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own hand and the public state."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round > hand_size, end the game; otherwise continue."
    }
  ],
  "ending": {
    "condition": "round > hand_size",
    "rank_by": "2 * you.bulls - you.penalty",
    "decided_by": "Each player's final score is penalty - 2 * bulls. The lowest final score wins, so ranking is by its negative. Players tied for lowest share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "With 3 players the deck is cards 1 to 30 and each hand is 9 cards; with 4 players the deck is cards 1 to 40 and each hand is 8 cards."
    },
    {
      "id": "R2",
      "text": "Cards 11, 22 and 33 carry 3 ox-heads, every other multiple of 5 carries 2, and all other cards carry 1 (e.g. 11 -> 3, 25 -> 2, 7 -> 1)."
    },
    {
      "id": "R3",
      "text": "At setup two face-up cards start pile_a and pile_b, each of size 1 with ox equal to its card; the remaining 1 (3 players) or 6 (4 players) cards go to set_aside and are never used."
    },
    {
      "id": "R4",
      "text": "All players start with penalty 0 and bulls 0."
    },
    {
      "id": "R5",
      "text": "A card c fits a pile with top t when (c - t) mod N is between 1 and 10 inclusive; with N = 30 and top 25, cards 26 to 30 and 1 to 5 fit, and 6 and 25 do not."
    },
    {
      "id": "R6",
      "text": "A pile has room when it holds fewer than 5 cards; a pile of 5 cards accepts no placement."
    },
    {
      "id": "R7",
      "text": "When a player holds at least one placement (a card that fits a pile with room), only placements are offered to them."
    },
    {
      "id": "R8",
      "text": "When a player places card c on pile X, c leaves the hand, becomes top_X, size_X rises by 1 and ox_X rises by ox(c); the other pile is unchanged."
    },
    {
      "id": "R9",
      "text": "When a player holds no placement, they must take: they may choose any card from hand and either pile."
    },
    {
      "id": "R10",
      "text": "When a player takes pile X, their penalty rises by ox_X, the pile's cards go to discarded, and the chosen card becomes the pile's only card (size 1, ox equal to its ox)."
    },
    {
      "id": "R11",
      "text": "When the taken pile had 3 or more cards the taker gains 1 bull; when it had 1 or 2 cards they gain none."
    },
    {
      "id": "R12",
      "text": "In round r, seats act one after another starting with seat ((r - 1) mod number_of_players) + 1 and wrapping round in seat order."
    },
    {
      "id": "R13",
      "text": "Every turn removes exactly one card from the acting player's hand, so all hands are empty after round H."
    },
    {
      "id": "R14",
      "text": "The game ends after exactly H rounds (9 with 3 players, 8 with 4)."
    },
    {
      "id": "R15",
      "text": "A player's final score is penalty - 2 * bulls; e.g. penalty 7 with 2 bulls scores 3."
    },
    {
      "id": "R16",
      "text": "Cards left in the two piles at the end count against nobody."
    },
    {
      "id": "R17",
      "text": "The player with the lowest final score wins; players tied for lowest share a draw."
    }
  ],
  "offers": [
    {
      "question": "Your turn: choose a card and a pile",
      "who": "seat current_seat",
      "options": "If the seat holds any placement: exactly the pairs 'c on A' where c is in hand, (c - top_a) mod N is in 1..10 and size_a < 5, plus the pairs 'c on B' meeting the same test against top_b and size_b. If the seat holds no placement: every card in hand paired with A and with B, each labelled as a take (e.g. 'take A with 17')."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 3",
      "why": "The source defines the deck and hand only for 3 and 4 players, and the designer suggests 3. With fewer, there is too little contention over the two piles; the rules define no larger deck."
    },
    {
      "what": "No talk step before each turn",
      "why": "The source has no communication phase, and adding one would be adding a mechanic. Play is about hand management: keeping low-risk cards, timing takes while piles are small, and taking a pile of 3 or more cards when the bull's -2 outweighs its ox-heads."
    },
    {
      "what": "Card and pile are chosen as one combined option",
      "why": "The rules ask for both together, and a single choice lets the offers enforce the placement-first rule exactly."
    },
    {
      "what": "Rank by 2 * bulls - penalty",
      "why": "The engine ranks the highest value first, and the rules want the lowest penalty - 2 * bulls."
    },
    {
      "what": "A running score attribute updated every turn",
      "why": "It makes the standing observable and testable during play."
    }
  ],
  "simplifications": [
    {
      "what": "The rotating start seat and sequential turns are built as a repeat loop over current_seat with a per-turn update",
      "why": "Each turn changes the piles before the next seat chooses, so each turn's update must run before the next ask."
    },
    {
      "what": "Whether a move is a take is worked out at update time by testing if the chosen card fits the chosen pile with room",
      "why": "The offers allow non-placements only when no placement exists, so this test is equivalent to the rule."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: penalty, bulls, score; table: pile_a, pile_b.
````

## Reply

````
```json
[
  {
    "name": "3 players: each hand holds 9 cards right after setup",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}},
        "game": {"deck": 0}
      }
    }
  },
  {
    "name": "4 players: each hand holds 8 cards right after setup",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}, "4": {"hand": 8}},
        "game": {"deck": 0}
      }
    }
  },
  {
    "name": "Ox values: 11 carries 3 and 25 carries 2 when their piles are taken",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [22]}, "2": {"hand": [7]}, "3": {"hand": [8]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [11], "top_a": 11, "size_a": 1, "ox_a": 3,
        "pile_b": [25], "top_b": 25, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [
      {"seat": 1, "options_include": "take A with 22"},
      {"seat": 2, "options_include": "take B with 7"}
    ],
    "expect": {
      "players": {
        "1": {"penalty": 3, "bulls": 0, "score": 3},
        "2": {"penalty": 2, "bulls": 0, "score": 2},
        "3": {"penalty": 0, "bulls": 0, "score": 0}
      },
      "game": {"pile_a": [22], "pile_b": [7, 8]}
    }
  },
  {
    "name": "3 players setup: two piles of one card each and 1 card set aside",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 0,
    "expect": {"lens": {"game": {"pile_a": 1, "pile_b": 1, "set_aside": 1, "deck": 0}}}
  },
  {
    "name": "4 players setup: two piles of one card each and 6 cards set aside",
    "rule": "R3",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "expect": {"lens": {"game": {"pile_a": 1, "pile_b": 1, "set_aside": 6, "deck": 0}}}
  },
  {
    "name": "All players start with penalty 0, bulls 0 and score 0",
    "rule": "R4",
    "players": 3,
    "seed": 3,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"penalty": 0, "bulls": 0, "score": 0},
        "2": {"penalty": 0, "bulls": 0, "score": 0},
        "3": {"penalty": 0, "bulls": 0, "score": 0}
      }
    }
  },
  {
    "name": "Fit wraps round: on top 25, cards 26 and 5 fit and card 6 does not",
    "rule": "R5",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [5, 6, 26]}, "2": {"hand": [16]}, "3": {"hand": [17]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [25], "top_a": 25, "size_a": 1, "ox_a": 2,
        "pile_b": [15], "top_b": 15, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [{"seat": 1, "options_include": "5 on A"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "5 on A"},
        {"seat": 1, "option": "26 on A"}
      ],
      "not_offered": [
        {"seat": 1, "option": "6 on A"},
        {"seat": 1, "option": "6 on B"},
        {"seat": 1, "option": "26 on B"},
        {"seat": 1, "option": "take A with 6"}
      ],
      "game": {"pile_a": [25, 5], "pile_b": [15, 16, 17]},
      "players": {
        "1": {"penalty": 0},
        "2": {"penalty": 0},
        "3": {"penalty": 0}
      }
    }
  },
  {
    "name": "A pile of 5 cards accepts no placement even when the card fits",
    "rule": "R6",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [6, 21]}, "2": {"hand": [22]}, "3": {"hand": [23]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [1, 2, 3, 4, 5], "top_a": 5, "size_a": 5, "ox_a": 6,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [{"seat": 1, "options_include": "21 on B"}],
    "expect": {
      "not_offered": [{"seat": 1, "option": "6 on A"}],
      "game": {"pile_a": [1, 2, 3, 4, 5], "pile_b": [20, 21, 22, 23]},
      "players": {
        "1": {"penalty": 0, "bulls": 0},
        "2": {"penalty": 0, "bulls": 0},
        "3": {"penalty": 0, "bulls": 0}
      }
    }
  },
  {
    "name": "A seat holding a placement is offered no take",
    "rule": "R7",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [12, 29]}, "2": {"hand": [13]}, "3": {"hand": [16]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [10], "top_a": 10, "size_a": 1, "ox_a": 2,
        "pile_b": [15], "top_b": 15, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [
      {"seat": 1, "options_include": "12 on A"},
      {"seat": 3, "options_include": "16 on B"}
    ],
    "expect": {
      "not_offered": [
        {"seat": 1, "option": "take A with 29"},
        {"seat": 1, "option": "take B with 29"},
        {"seat": 1, "option": "take A with 12"},
        {"seat": 1, "option": "29 on A"},
        {"seat": 1, "option": "29 on B"}
      ],
      "game": {"pile_a": [10, 12, 13], "pile_b": [15, 16]},
      "players": {
        "1": {"penalty": 0},
        "2": {"penalty": 0},
        "3": {"penalty": 0}
      }
    }
  },
  {
    "name": "Placing a card puts it on top of the chosen pile and leaves the other pile unchanged",
    "rule": "R8",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [8]}, "2": {"hand": [9]}, "3": {"hand": [19]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [3], "top_a": 3, "size_a": 1, "ox_a": 1,
        "pile_b": [18], "top_b": 18, "size_b": 1, "ox_b": 1
      }
    },
    "rules": [{"seat": 3, "options_include": "19 on B"}],
    "expect": {
      "game": {"pile_a": [3, 8, 9], "pile_b": [18, 19]},
      "players": {
        "1": {"penalty": 0, "bulls": 0, "score": 0},
        "2": {"penalty": 0, "bulls": 0, "score": 0},
        "3": {"penalty": 0, "bulls": 0, "score": 0}
      },
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}
    }
  },
  {
    "name": "A seat with no placement may take with any card on either pile",
    "rule": "R9",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [22, 23]}, "2": {"hand": [12]}, "3": {"hand": [13]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [11], "top_a": 11, "size_a": 1, "ox_a": 3,
        "pile_b": [25], "top_b": 25, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [{"seat": 1, "options_include": "take B with 23"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "take A with 22"},
        {"seat": 1, "option": "take B with 22"},
        {"seat": 1, "option": "take A with 23"},
        {"seat": 1, "option": "take B with 23"}
      ],
      "game": {"pile_a": [11, 12, 13], "pile_b": [23]},
      "players": {
        "1": {"penalty": 2, "bulls": 0, "score": 2},
        "2": {"penalty": 0},
        "3": {"penalty": 0}
      }
    }
  },
  {
    "name": "Taking a pile of 2 adds its ox total to penalty and the card starts a new pile",
    "rule": "R10",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [16]}, "2": {"hand": [6]}, "3": {"hand": [7]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [20, 25], "top_a": 25, "size_a": 2, "ox_a": 4,
        "pile_b": [5], "top_b": 5, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [{"seat": 1, "options_include": "take A with 16"}],
    "expect": {
      "game": {"pile_a": [16], "pile_b": [5, 6, 7]},
      "players": {
        "1": {"penalty": 4, "bulls": 0, "score": 4},
        "2": {"penalty": 0},
        "3": {"penalty": 0}
      },
      "lens": {"game": {"discarded": 2}}
    }
  },
  {
    "name": "Taking a pile of 3 earns a bull and taking a pile of 1 earns none",
    "rule": "R11",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [14]}, "2": {"hand": [9]}, "3": {"hand": [15]}},
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [1, 2, 3], "top_a": 3, "size_a": 3, "ox_a": 3,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [
      {"seat": 1, "options_include": "take A with 14"},
      {"seat": 2, "options_include": "take B with 9"},
      {"seat": 3, "options_include": "15 on A"}
    ],
    "expect": {
      "game": {"pile_a": [14, 15], "pile_b": [9]},
      "players": {
        "1": {"penalty": 3, "bulls": 1, "score": 1},
        "2": {"penalty": 2, "bulls": 0, "score": 2},
        "3": {"penalty": 0, "bulls": 0, "score": 0}
      }
    }
  },
  {
    "name": "In round 2 of 3 players seat 2 acts first, then seat 3, then seat 1",
    "rule": "R12",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": [4]}, "2": {"hand": [2]}, "3": {"hand": [3]}},
      "game": {
        "round": 2, "current_seat": 2,
        "pile_a": [1], "top_a": 1, "size_a": 1, "ox_a": 1,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "expect": {
      "game": {"pile_a": [1, 2, 3, 4], "pile_b": [20]},
      "players": {
        "1": {"penalty": 0, "bulls": 0},
        "2": {"penalty": 0, "bulls": 0},
        "3": {"penalty": 0, "bulls": 0}
      }
    }
  },
  {
    "name": "One round removes exactly one card from each hand (chance-proof: only counts)",
    "rule": "R13",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "first",
    "expect": {"lens": {"players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}}}}
  },
  {
    "name": "After 9 rounds with 3 players every hand is empty (chance-proof: only counts)",
    "rule": "R13",
    "players": 3,
    "seed": 5,
    "rounds": 9,
    "default": "first",
    "expect": {"lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}
  },
  {
    "name": "Game ends after round 9 with 3 players; lowest score wins",
    "rule": "R14",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [3], "penalty": 5, "bulls": 0, "score": 5},
        "2": {"hand": [4], "penalty": 3, "bulls": 0, "score": 3},
        "3": {"hand": [2], "penalty": 4, "bulls": 0, "score": 4}
      },
      "game": {
        "round": 9, "current_seat": 3,
        "pile_a": [1], "top_a": 1, "size_a": 1, "ox_a": 1,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "expect": {
      "winner": 2,
      "standings": {"1": -5, "2": -3, "3": -4},
      "game": {"pile_a": [1, 2, 3, 4], "pile_b": [20]},
      "players": {"1": {"score": 5}, "2": {"score": 3}, "3": {"score": 4}}
    }
  },
  {
    "name": "Penalty 7 with 2 bulls scores 3",
    "rule": "R15",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": [14], "penalty": 4, "bulls": 1, "score": 2},
        "2": {"hand": [25]},
        "3": {"hand": [26]}
      },
      "game": {
        "round": 1, "current_seat": 1,
        "pile_a": [1, 2, 3], "top_a": 3, "size_a": 3, "ox_a": 3,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "rules": [{"seat": 1, "options_include": "take A with 14"}],
    "expect": {
      "game": {"pile_a": [14], "pile_b": [20, 25, 26]},
      "players": {
        "1": {"penalty": 7, "bulls": 2, "score": 3},
        "2": {"penalty": 0, "score": 0},
        "3": {"penalty": 0, "score": 0}
      }
    }
  },
  {
    "name": "Cards left in the piles at the end count against nobody",
    "rule": "R16",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [15], "penalty": 1, "bulls": 0, "score": 1},
        "2": {"hand": [23], "penalty": 3, "bulls": 0, "score": 3},
        "3": {"hand": [14], "penalty": 2, "bulls": 0, "score": 2}
      },
      "game": {
        "round": 9, "current_seat": 3,
        "pile_a": [11, 12, 13], "top_a": 13, "size_a": 3, "ox_a": 5,
        "pile_b": [22], "top_b": 22, "size_b": 1, "ox_b": 3
      }
    },
    "expect": {
      "winner": 1,
      "standings": {"1": -1, "2": -3, "3": -2},
      "game": {"pile_a": [11, 12, 13, 14, 15], "pile_b": [22, 23]},
      "players": {
        "1": {"penalty": 1, "score": 1},
        "2": {"penalty": 3, "score": 3},
        "3": {"penalty": 2, "score": 2}
      }
    }
  },
  {
    "name": "Seats tied for the lowest final score share the win",
    "rule": "R17",
    "players": 3,
    "seed": 1,
    "given": {
      "players": {
        "1": {"hand": [3], "penalty": 4, "bulls": 1, "score": 2},
        "2": {"hand": [4], "penalty": 2, "bulls": 0, "score": 2},
        "3": {"hand": [2], "penalty": 3, "bulls": 0, "score": 3}
      },
      "game": {
        "round": 9, "current_seat": 3,
        "pile_a": [1], "top_a": 1, "size_a": 1, "ox_a": 1,
        "pile_b": [20], "top_b": 20, "size_b": 1, "ox_b": 2
      }
    },
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -2, "2": -2, "3": -3},
      "players": {"1": {"score": 2}, "2": {"score": 2}, "3": {"score": 3}}
    }
  }
]
```
````
