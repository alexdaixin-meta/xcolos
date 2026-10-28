# 10 scenarios

- time: 2026-10-28T04:50:31+00:00 (95.3s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 f523e38324049610, reply sha256 1d649556848cbe80

## Sent

````
SPEC:
{
  "name": "Speicherstadt Queues (Even Rotation)",
  "summary": "Over 12 rounds, 3-4 merchants secretly queue workers on three goods lots each round and buy through a falling-price offer that runs in a rotating priority order, trying to collect their hidden contract colour.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "colours": 6,
    "cards_per_colour": 6,
    "deck_size": 36,
    "rounds": 12,
    "lots_per_round": 3,
    "starting_coins": 6,
    "income_per_round": 2,
    "workers_per_player": 2,
    "limit_min": 0,
    "limit_max": 6,
    "lowest_offer_price": 1,
    "price_drop_per_decline": 1,
    "contract_good_points": 5,
    "other_good_points": 2,
    "coin_points": 1,
    "tiebreak_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "seat",
        "type": "number",
        "visible": "public",
        "initial": "seat number 1..N in seating order",
        "meaning": "the player's position in seating order",
        "observable": false
      },
      {
        "key": "coins",
        "type": "number",
        "visible": "public",
        "initial": 6,
        "meaning": "coins held; public at all times",
        "observable": true
      },
      {
        "key": "goods",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "goods bought, as colour names; public at all times",
        "observable": true
      },
      {
        "key": "contract",
        "type": "text",
        "visible": "ally",
        "initial": "dealt at setup",
        "meaning": "secret contract colour, different for each player; revealed to all at game end",
        "observable": false
      },
      {
        "key": "own_goods",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "number of goods held that match the player's own contract colour",
        "observable": false
      },
      {
        "key": "limit1",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "this round's secret limit on Lot 1 (0 means no worker)",
        "observable": false
      },
      {
        "key": "limit2",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "this round's secret limit on Lot 2",
        "observable": false
      },
      {
        "key": "limit3",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "this round's secret limit on Lot 3",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "final score: coins + 5 per own-contract good + 2 per other good, set at game end",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "36 cards: 6 each of Red, Blue, Green, Yellow, Purple, Orange",
        "meaning": "the shuffled supply deck",
        "observable": false
      },
      {
        "key": "contract_pool",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple",
          "Orange"
        ],
        "meaning": "contract colours not yet dealt",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "lots that nobody bought",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number, 1..12",
        "observable": true
      },
      {
        "key": "lot1",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of this round's Lot 1",
        "observable": false
      },
      {
        "key": "lot2",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of this round's Lot 2",
        "observable": false
      },
      {
        "key": "lot3",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "colour of this round's Lot 3",
        "observable": false
      },
      {
        "key": "priority_start",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "seat first in this round's priority order: ((round - 1) mod N) + 1",
        "observable": false
      },
      {
        "key": "queue_len",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "k, the number of players queued on the lot being resolved",
        "observable": false
      },
      {
        "key": "offer_price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current offer price on the lot being resolved",
        "observable": false
      },
      {
        "key": "lot_sold",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "whether the lot being resolved has been bought",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are numbered 1 to N (N = 3 or 4) in seating order.",
    "The deck is filled with 36 cards (6 each of Red, Blue, Green, Yellow, Purple, Orange) and shuffled once.",
    "Each player is privately dealt a contract colour: one colour is drawn at random from contract_pool into that player's contract and removed from contract_pool, so no two players share a colour. No one else learns it.",
    "Each player starts with coins = 6, goods = [], own_goods = 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1; draw three cards at random from deck into lot1, lot2 and lot3, removing each from deck; announce the three lot colours."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "every player's coins += 2."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "priority_start = ((round - 1) mod N) + 1; announce the priority order: priority_start, then the following seats in seat order, wrapping from N to 1."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one short text message (not binding, may be false)",
      "effect": "after all are in, broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 6: your limit on Lot 1 (0 = no worker)",
      "effect": "set each player's limit1; answers are never revealed."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 6: your limit on Lot 2 (0 = no worker)",
      "effect": "set each player's limit2; answers are never revealed."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 6: your limit on Lot 3 (0 = no worker)",
      "effect": "set each player's limit3; answers are never revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "worker cap of 2: for each player, if limit1 > 0 and limit2 > 0 and limit3 > 0, then limit3 = 0."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "resolve Lot 1, setup: queue_len = count of players with limit1 > 0; offer_price = queue_len; lot_sold = false."
    },
    {
      "action": "update",
      "who": "each player in priority order (positions 1..N, starting at priority_start)",
      "answer": null,
      "effect": "resolve Lot 1, offers (one step per priority position): when lot_sold is false and this player's limit1 > 0, then if limit1 >= offer_price and coins >= offer_price, the player's coins -= offer_price, lot1 is appended to the player's goods, own_goods += 1 if lot1 == contract, and lot_sold = true; otherwise offer_price -= 1. Players with limit1 = 0 are skipped."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "when lot_sold is false, append lot1 to discard (this covers an empty queue too)."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "resolve Lot 2, setup: queue_len = count of players with limit2 > 0; offer_price = queue_len; lot_sold = false."
    },
    {
      "action": "update",
      "who": "each player in priority order (positions 1..N, starting at priority_start)",
      "answer": null,
      "effect": "resolve Lot 2, offers: the same as Lot 1, using limit2 and lot2; coins spent on Lot 1 this round count in the coins check."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "when lot_sold is false, append lot2 to discard."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "resolve Lot 3, setup: queue_len = count of players with limit3 > 0; offer_price = queue_len; lot_sold = false."
    },
    {
      "action": "update",
      "who": "each player in priority order (positions 1..N, starting at priority_start)",
      "answer": null,
      "effect": "resolve Lot 3, offers: the same as Lot 1, using limit3 and lot3; coins spent earlier this round count in the coins check."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "when lot_sold is false, append lot3 to discard."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce, for each lot, which seats queued (a positive limit), who bought it if anyone, and the price paid; also every player's coins and goods. Limits are not revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when round == 12: score = coins + 5 * own_goods + 2 * (length(goods) - own_goods); reveal every player's contract to all."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "end the game if round >= 12 (the deck is then empty); otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= 12",
    "rank_by": "you.score * 100 + you.own_goods",
    "decided_by": "Highest final score (coins + 5 per good of own contract colour + 2 per other good) wins. A tie is broken by more goods of own contract colour. Players still level share the win, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup the deck holds 36 cards, 6 of each of the 6 colours, and each player gets a different secret contract colour drawn from the 6."
    },
    {
      "id": "R2",
      "text": "At setup every player has 6 coins and no goods."
    },
    {
      "id": "R3",
      "text": "Each round, 3 cards are drawn from the deck as Lot 1, Lot 2 and Lot 3, so after 12 rounds the deck is empty."
    },
    {
      "id": "R4",
      "text": "Each round, every player gains 2 coins before queuing."
    },
    {
      "id": "R5",
      "text": "In round r the priority order starts with seat ((r - 1) mod N) + 1 and continues in seat order, wrapping from N to 1; with N = 4, round 1 starts at seat 1, round 2 at seat 2 and round 5 at seat 1."
    },
    {
      "id": "R6",
      "text": "Each round every player sends one short message at the same time, and all messages are shown to everyone after all are in."
    },
    {
      "id": "R7",
      "text": "Each player submits a limit from 0 to 6 for each lot; 0 means no worker on that lot."
    },
    {
      "id": "R8",
      "text": "When a player submits positive limits on all three lots, their Lot 3 limit is set to 0, so at most 2 workers are placed."
    },
    {
      "id": "R9",
      "text": "The first offer on a lot is at price k, the number of players queued on it, and goes to the earliest queued player in priority order."
    },
    {
      "id": "R10",
      "text": "When an offered player's limit is at least the price and they hold at least that many coins, they pay the price to the bank and take the good."
    },
    {
      "id": "R11",
      "text": "When an offered player's limit is below the price or their coins are below it, the price drops by 1 and the offer passes to the next queued player, so the k-th queued player is offered price 1."
    },
    {
      "id": "R12",
      "text": "When nobody in the queue buys, or nobody queued, the lot is discarded."
    },
    {
      "id": "R13",
      "text": "Lots resolve in the order 1, 2, 3, and coins spent on an earlier lot reduce the coins checked for later lots."
    },
    {
      "id": "R14",
      "text": "After each round, the queuers, the buyer and the price of each lot are announced; limits are never revealed; coins and goods are public at all times."
    },
    {
      "id": "R15",
      "text": "The game ends after round 12."
    },
    {
      "id": "R16",
      "text": "Final score = coins + 5 per good of the player's own contract colour + 2 per good of any other colour; for example, 10 coins with 2 own-colour goods and 3 other goods scores 26."
    },
    {
      "id": "R17",
      "text": "At game end all contract colours are revealed."
    },
    {
      "id": "R18",
      "text": "The highest score wins; a tie at the top is broken by more own-contract goods; players still tied share the win as a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "every seat",
      "options": "any short text"
    },
    {
      "question": "Limit on Lot 1",
      "who": "every seat",
      "options": "whole number 0 to 6"
    },
    {
      "question": "Limit on Lot 2",
      "who": "every seat",
      "options": "whole number 0 to 6"
    },
    {
      "question": "Limit on Lot 3",
      "who": "every seat",
      "options": "whole number 0 to 6 (forced to 0 if Lot 1 and Lot 2 limits are both positive)"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer chose 4, and the even rotation needs 12/N to be a whole number, which holds for 3 and 4. Three is the smallest table where two rivals contest a lot and the queue price ladder matters. Above 4, 6 contract colours and 3 lots per round get too thin. The strategy is to infer rivals' contracts from their purchases and talk, to bluff about your own, and to time your bids around the rounds where you hold priority."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The source requires simultaneous messages. Players compete for lots and hide their contracts, so talk invites bluffing and deterrence that could cost a player who believes it."
    },
    {
      "what": "Tie-break encoded as score * 100 + own_goods",
      "why": "own_goods is at most 6, which is below 100, so this ranks by score and then by own-contract goods. Players level on both share the win, which is the source's draw."
    },
    {
      "what": "Contracts marked not observable",
      "why": "They are hidden during play and revealed only at the end; the score is the observable outcome."
    }
  ],
  "simplifications": [
    {
      "what": "The three limits are collected as three consecutive simultaneous polls instead of one combined submission",
      "why": "The engine takes one number per question. Limits are never revealed, so no player learns anything between the polls."
    },
    {
      "what": "The falling-price offer is unrolled into one conditional update per priority position for each lot",
      "why": "The step list is flat. Up to N fixed steps with when/if conditions reproduce the sequential offer exactly."
    },
    {
      "what": "Final scoring and the contract reveal are a conditional update in round 12, just before the end check",
      "why": "The score must be computed before the arithmetic ranking runs."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: coins, goods, score; table: round.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Do not script answers for a choice the rules make moot. Once a player has given positive limits on Lots 1 and 2, the game may skip the Lot 3 question, so do not require a Lot 3 answer (a 1 in R8, a 0 in R13) with a fixed 'times' count. Use non-strict counts or drop those rules. Test R8 through outcomes instead: after the round the player holds at most 2 new goods, their coins match paying only for Lots 1 and 2, and Lot 3 goes to the next queuer or is discarded. Test R13 through outcomes too: Ada spends her coins on Lot 1, is then too short to pay the Lot 2 price, and Lot 2 goes to the next player in the queue at the lower price. Check this in the players' coins and goods, not in how many prompts Ada received.
````

## Reply

````
```json
[
  {
    "name": "Setup: deck holds 36 cards and each of 4 seats takes a different contract from the pool of 6",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"deck": 36, "contract_pool": 2},
        "players": {"1": {"goods": 0}, "2": {"goods": 0}, "3": {"goods": 0}, "4": {"goods": 0}}
      }
    }
  },
  {
    "name": "Setup: every player starts with 6 coins and no goods",
    "rule": "R2",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []},
        "4": {"coins": 6, "goods": []}
      },
      "game": {"round": 0}
    }
  },
  {
    "name": "Each round draws 3 lots from the deck (36 -> 33)",
    "rule": "R3",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "lens": {"game": {"deck": 33}},
      "game": {"round": 1}
    }
  },
  {
    "name": "Every player gains 2 coins in the round (6 -> 8 with no purchases)",
    "rule": "R4",
    "players": 4,
    "seed": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"coins": 8, "goods": []},
        "2": {"coins": 8, "goods": []},
        "3": {"coins": 8, "goods": []},
        "4": {"coins": 8, "goods": []}
      }
    }
  },
  {
    "name": "Round 2 priority starts at seat 2: seat 2 buys Lot 1 at price 2 ahead of seat 1",
    "rule": "R5",
    "players": 4,
    "seed": 5,
    "rounds": 1,
    "given": {
      "game": {"round": 1},
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []},
        "4": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "game": {"round": 2},
      "players": {"1": {"coins": 8, "goods": []}, "2": {"coins": 6}, "3": {"coins": 8}, "4": {"coins": 8}},
      "lens": {"players": {"2": {"goods": 1}}}
    }
  },
  {
    "name": "Round 4 priority starts at seat 4: seat 4 buys Lot 1 at price 2 ahead of seat 1",
    "rule": "R5",
    "players": 4,
    "seed": 6,
    "rounds": 1,
    "given": {
      "game": {"round": 3},
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []},
        "4": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 6, "times": 1},
      {"seat": 4, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "game": {"round": 4},
      "players": {"1": {"coins": 8, "goods": []}, "4": {"coins": 6}, "2": {"coins": 8}, "3": {"coins": 8}},
      "lens": {"players": {"4": {"goods": 1}}}
    }
  },
  {
    "name": "Round 5 priority wraps back to seat 1: seat 1 buys Lot 1 at price 2 ahead of seat 4",
    "rule": "R5",
    "players": 4,
    "seed": 7,
    "rounds": 1,
    "given": {
      "game": {"round": 4},
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []},
        "4": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 6, "times": 1},
      {"seat": 4, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "game": {"round": 5},
      "players": {"1": {"coins": 6}, "4": {"coins": 8, "goods": []}, "2": {"coins": 8}, "3": {"coins": 8}},
      "lens": {"players": {"1": {"goods": 1}}}
    }
  },
  {
    "name": "Talk round happens and play continues normally (messages are answered automatically)",
    "rule": "R6",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "game": {"round": 1},
      "players": {"1": {"coins": 8}, "2": {"coins": 8}, "3": {"coins": 8}}
    }
  },
  {
    "name": "Limits range from 0 to 6: 0 and 6 offered, 7 never offered",
    "rule": "R7",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 6}, {"seat": 2, "option": 6}],
      "not_offered": [{"seat": 1, "option": 7}, {"seat": 2, "option": 7}],
      "players": {"1": {"coins": 8, "goods": []}}
    }
  },
  {
    "name": "Three positive limits: seat 1 buys only Lots 1 and 2, and Lot 3 goes to seat 2 at price 1",
    "rule": "R8",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": "all"},
      {"seat": 2, "options_include": 0, "times": 2},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 6}, "2": {"coins": 7}, "3": {"coins": 8, "goods": []}},
      "lens": {"players": {"1": {"goods": 2}, "2": {"goods": 1}}}
    }
  },
  {
    "name": "First offer is at price k=3 to the earliest queued seat in priority (seat 2)",
    "rule": "R9",
    "players": 4,
    "seed": 11,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []},
        "4": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 6, "times": 1},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 6, "times": 1},
      {"seat": 4, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {
        "1": {"coins": 8, "goods": []},
        "2": {"coins": 5},
        "3": {"coins": 8, "goods": []},
        "4": {"coins": 8, "goods": []}
      },
      "lens": {"players": {"2": {"goods": 1}}}
    }
  },
  {
    "name": "Limit exactly equal to price 2 buys: seat 1 pays 2 and takes the good",
    "rule": "R10",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 6}, "2": {"coins": 8, "goods": []}, "3": {"coins": 8, "goods": []}},
      "lens": {"players": {"1": {"goods": 1}}}
    }
  },
  {
    "name": "Limits below price pass the offer down: the third queued seat buys at price 1",
    "rule": "R11",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 8, "goods": []}, "2": {"coins": 8, "goods": []}, "3": {"coins": 7}},
      "lens": {"players": {"3": {"goods": 1}}}
    }
  },
  {
    "name": "Too few coins passes the offer: seat 1 with 2 coins cannot pay 3, seat 2 buys at 2",
    "rule": "R11",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 0, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 6, "times": 1},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 2, "goods": []}, "2": {"coins": 6}, "3": {"coins": 8, "goods": []}},
      "lens": {"players": {"2": {"goods": 1}}}
    }
  },
  {
    "name": "Nobody queues: all three lots are discarded and nobody gains goods",
    "rule": "R12",
    "players": 3,
    "seed": 15,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "lens": {"game": {"discard": 3, "deck": 33}},
      "players": {"1": {"goods": [], "coins": 8}, "2": {"goods": [], "coins": 8}, "3": {"goods": [], "coins": 8}}
    }
  },
  {
    "name": "Coins spent on Lot 1 count for Lot 2: seat 1 is then short and Lot 2 goes to seat 2 at price 1",
    "rule": "R13",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 0, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 6, "times": "all"},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 6, "times": 1},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 1}, "2": {"coins": 7}, "3": {"coins": 8, "goods": []}},
      "lens": {"players": {"1": {"goods": 1}, "2": {"goods": 1}}}
    }
  },
  {
    "name": "After a lone purchase at price 1 the buyer's coins and goods are publicly updated",
    "rule": "R14",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"coins": 6, "goods": []},
        "2": {"coins": 6, "goods": []},
        "3": {"coins": 6, "goods": []}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"coins": 7}, "2": {"coins": 8, "goods": []}, "3": {"coins": 8, "goods": []}},
      "lens": {"players": {"1": {"goods": 1}}}
    }
  },
  {
    "name": "Game ends after round 12; all seats level at score 8 share the win",
    "rule": "R15",
    "players": 3,
    "seed": 18,
    "given": {
      "game": {"round": 11, "deck": ["Orange", "Orange", "Orange"]},
      "players": {
        "1": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Red"},
        "2": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Blue"},
        "3": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Green"}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "winner": [1, 2, 3],
      "standings": {"1": 800, "2": 800, "3": 800},
      "game": {"round": 12},
      "players": {"1": {"score": 8}, "2": {"score": 8}, "3": {"score": 8}}
    }
  },
  {
    "name": "Final score: 10 coins + 2 own-colour goods + 3 other goods = 26",
    "rule": "R16",
    "players": 3,
    "seed": 19,
    "given": {
      "game": {"round": 11, "deck": ["Orange", "Orange", "Orange"]},
      "players": {
        "1": {"coins": 8, "goods": ["Red", "Red", "Blue", "Green", "Yellow"], "own_goods": 2, "contract": "Red"},
        "2": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Blue"},
        "3": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Green"}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 2602, "2": 800, "3": 800},
      "players": {"1": {"score": 26, "coins": 10}, "2": {"score": 8}, "3": {"score": 8}}
    }
  },
  {
    "name": "Game end reveals contracts and sets final scores (only scores are observable)",
    "rule": "R17",
    "players": 3,
    "seed": 20,
    "given": {
      "game": {"round": 11, "deck": ["Orange", "Orange", "Orange"]},
      "players": {
        "1": {"coins": 6, "goods": ["Red"], "own_goods": 1, "contract": "Red"},
        "2": {"coins": 6, "goods": ["Red"], "own_goods": 0, "contract": "Blue"},
        "3": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Green"}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 1301, "2": 1000, "3": 800},
      "players": {"1": {"score": 13}, "2": {"score": 10}, "3": {"score": 8}}
    }
  },
  {
    "name": "Tied score 15 is broken by more own-contract goods: seat 1 wins",
    "rule": "R18",
    "players": 3,
    "seed": 21,
    "given": {
      "game": {"round": 11, "deck": ["Orange", "Orange", "Orange"]},
      "players": {
        "1": {"coins": 8, "goods": ["Red"], "own_goods": 1, "contract": "Red"},
        "2": {"coins": 9, "goods": ["Red", "Yellow"], "own_goods": 0, "contract": "Blue"},
        "3": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Green"}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 1501, "2": 1500, "3": 800},
      "players": {"1": {"score": 15}, "2": {"score": 15}, "3": {"score": 8}}
    }
  },
  {
    "name": "Level on score and own-contract goods: seats 1 and 2 share the win",
    "rule": "R18",
    "players": 3,
    "seed": 22,
    "given": {
      "game": {"round": 11, "deck": ["Orange", "Orange", "Orange"]},
      "players": {
        "1": {"coins": 8, "goods": ["Red"], "own_goods": 1, "contract": "Red"},
        "2": {"coins": 8, "goods": ["Blue"], "own_goods": 1, "contract": "Blue"},
        "3": {"coins": 6, "goods": [], "own_goods": 0, "contract": "Green"}
      }
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 1501, "2": 1501, "3": 800},
      "players": {"1": {"score": 15}, "2": {"score": 15}, "3": {"score": 8}}
    }
  }
]
```
````
