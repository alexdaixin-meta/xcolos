# 18 scenarios

- time: 2026-10-27T09:01:58+00:00 (59.9s)  model: claude-opus-5-5
- system prompt: [system/2ddacf4d-scenarios.md](system/2ddacf4d-scenarios.md) (sha256 2ddacf4d74fa3789)
- sent sha256 bcdbb7d466496c0a, reply sha256 7a3e22b1bc6f8765

## Sent

````
SPEC:
{
  "name": "Coyote Lap",
  "summary": "Each player sees every card but their own. Players bid upward on the true total of the cards in play until someone calls Coyote, and whoever is wrong takes a token. After 12 hands the fewest tokens wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 33,
    "count_minus_10": 1,
    "count_minus_5": 2,
    "count_0": 3,
    "count_each_1_to_5": 4,
    "count_10": 3,
    "count_15": 2,
    "count_20": 1,
    "count_max_to_zero": 1,
    "max_to_zero_code": 100,
    "hands": 12,
    "declaration_min": -30,
    "declaration_max": 60,
    "raise_min_step": 1,
    "tokens_per_loss": 1,
    "starting_tokens": 0,
    "cards_per_player": 1
  },
  "attributes": {
    "player": [
      {
        "key": "tokens",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Coyote tokens taken so far (fewer is better)",
        "observable": true
      },
      {
        "key": "card",
        "type": "number",
        "visible": "others",
        "initial": 0,
        "meaning": "The card dealt this hand, as its face value, or 100 for the special 'Max\u21920' card. Every other player sees it; the owner does not (the bandana).",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          -10,
          -5,
          -5,
          0,
          0,
          0,
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
          10,
          10,
          10,
          15,
          15,
          20,
          100
        ],
        "meaning": "The undealt cards of the 33-card deck (100 = 'Max\u21920')",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current hand, from 1 to 12",
        "observable": true
      },
      {
        "key": "opener_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that opens this hand",
        "observable": true
      },
      {
        "key": "current_declaration",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest declaration made so far this hand",
        "observable": true
      },
      {
        "key": "current_declarer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that made the current declaration",
        "observable": true
      },
      {
        "key": "bidding_open",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True while nobody has called Coyote this hand",
        "observable": false
      },
      {
        "key": "caller",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that called Coyote, or the opener on an automatic call",
        "observable": true
      },
      {
        "key": "true_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The true total of the cards in play, computed after bidding",
        "observable": true
      },
      {
        "key": "hand_loser",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that took the token this hand",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat the players in a fixed clockwise order, seats 1 to N.",
    "Every player's tokens is set to 0.",
    "hand_number is set to 1 and opener_seat to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reset deck to the full 33-card list. For each player, draw one card at random from deck: set that player's card to its value and remove it from deck. Set caller = 0, current_declarer = 0, hand_loser = 0, true_total = 0, bidding_open = true."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees the card of every other player (card is visible to others) but never their own."
    },
    {
      "action": "ask",
      "who": "the opener (seat opener_seat)",
      "answer": "a whole number from -30 to 60",
      "effect": "Set current_declaration = answer and current_declarer = opener_seat. Announce to all: 'Seat {opener_seat} opens at {current_declaration}.'"
    },
    {
      "action": "ask",
      "who": "responder 1: seat ((opener_seat) mod N) + 1, when bidding_open",
      "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)",
      "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."
    },
    {
      "action": "ask",
      "who": "responder 1, when bidding_open and they chose raise",
      "answer": "a whole number from current_declaration + 1 to 60",
      "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."
    },
    {
      "action": "ask",
      "who": "responder 2: seat ((opener_seat + 1) mod N) + 1, when bidding_open",
      "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)",
      "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."
    },
    {
      "action": "ask",
      "who": "responder 2, when bidding_open and they chose raise",
      "answer": "a whole number from current_declaration + 1 to 60",
      "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."
    },
    {
      "action": "ask",
      "who": "responder 3: seat ((opener_seat + 2) mod N) + 1, only when N = 4 and bidding_open",
      "answer": "a choice: raise or call_coyote (raise is offered only if current_declaration < 60)",
      "effect": "If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step."
    },
    {
      "action": "ask",
      "who": "responder 3, only when N = 4, bidding_open and they chose raise",
      "answer": "a whole number from current_declaration + 1 to 60",
      "effect": "Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all."
    },
    {
      "action": "update",
      "who": "the opener, when bidding_open",
      "answer": null,
      "effect": "Automatic call: set caller = opener_seat and bidding_open = false. Announce: 'Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "true_total = sum of every card that is not 100. If some player's card = 100, subtract the maximum of the other players' cards (exactly one copy of the highest, even if that value is negative)."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If true_total < current_declaration: the current_declarer's tokens += 1 and hand_loser = current_declarer. Otherwise: the caller's tokens += 1 and hand_loser = caller."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal every player's card (100 shown as 'Max\u21920'), plus true_total, current_declaration and hand_loser: 'Cards: {cards}. True total {true_total} against a declaration of {current_declaration}. Seat {hand_loser} takes a Coyote token.'"
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "opener_seat = (opener_seat mod N) + 1; hand_number += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If hand_number > 12, end the game; otherwise continue to the next hand."
    }
  ],
  "ending": {
    "condition": "hand_number > 12",
    "rank_by": "0 - you.tokens",
    "decided_by": "A player's standing is the negative of their Coyote tokens. The player with the fewest tokens wins, and players tied for the fewest share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, every player has 0 tokens, hand_number is 1 and opener_seat is 1."
    },
    {
      "id": "R2",
      "text": "When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max\u21920), and each player is dealt exactly 1 card that is removed from the deck."
    },
    {
      "id": "R3",
      "text": "When cards are dealt, each player can see every other player's card but not their own."
    },
    {
      "id": "R4",
      "text": "When the opener declares, the value must be a whole number from -30 to 60, and the opener becomes current_declarer."
    },
    {
      "id": "R5",
      "text": "When a responder raises, the new declaration must be a whole number strictly greater than current_declaration and at most 60, and that responder becomes current_declarer."
    },
    {
      "id": "R6",
      "text": "When current_declaration is 60, a responder is offered only call_coyote."
    },
    {
      "id": "R7",
      "text": "When a responder calls Coyote, bidding stops and no later responder acts this hand."
    },
    {
      "id": "R8",
      "text": "When every responder raises, the opener is the caller (an automatic call) on the final declaration."
    },
    {
      "id": "R9",
      "text": "When no Max\u21920 card is in play, true_total is the plain sum of all cards in play (for example, cards 5, 10 and -5 give 10)."
    },
    {
      "id": "R10",
      "text": "When the Max\u21920 card is in play, it counts 0 and exactly one copy of the highest other card counts 0 (for example, Max\u21920, 15, 15 and 3 give 18)."
    },
    {
      "id": "R11",
      "text": "When the Max\u21920 card is in play and the highest other card is negative, that card still counts 0 (for example, Max\u21920, -5 and -10 give -10)."
    },
    {
      "id": "R12",
      "text": "When true_total < current_declaration, the current_declarer's tokens rise by 1."
    },
    {
      "id": "R13",
      "text": "When true_total >= current_declaration, the caller's tokens rise by 1 (the opener's on an automatic call)."
    },
    {
      "id": "R14",
      "text": "When a hand ends, every card, true_total and the seat that took the token are announced to all players."
    },
    {
      "id": "R15",
      "text": "When a hand ends, opener_seat moves to the next seat clockwise, wrapping from seat N to seat 1."
    },
    {
      "id": "R16",
      "text": "When 12 hands have been played, the game ends."
    },
    {
      "id": "R17",
      "text": "When the game ends, the player with the fewest tokens wins, and players tied for the fewest share the result."
    }
  ],
  "offers": [
    {
      "question": "Opening declaration",
      "who": "the opener (seat opener_seat)",
      "options": "any whole number from -30 to 60"
    },
    {
      "question": "Raise or call",
      "who": "each responder in clockwise order from the opener, while bidding is open",
      "options": "raise or call_coyote when current_declaration < 60; only call_coyote when current_declaration = 60"
    },
    {
      "question": "Raise amount",
      "who": "a responder who chose raise",
      "options": "any whole number from current_declaration + 1 to 60"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer suggests 4, so it is kept. 3 is the minimum because with fewer players there is too little hidden information to reason about and no chain of raises. 4 is the maximum the source allows, and more responders would push declarations past what the deck can support."
    },
    {
      "what": "Max\u21920 is stored as the code 100 in card",
      "why": "Cards must be numbers so the total can be computed. 100 is never a face value, so the code is unambiguous, and the reveal shows it as 'Max\u21920'."
    },
    {
      "what": "No free-talk step before the bidding",
      "why": "The source has no table talk. Information is carried by the declarations themselves, and adding talk would add a mechanic."
    },
    {
      "what": "Strategy at the table",
      "why": "Each player sums the cards they can see and estimates their own unseen card from the deck odds, watching for a visible Max\u21920. They then read the other players' declarations as signals about their own card. A thoughtful player raises only when the expected total supports it, and calls when the current bid outruns what they see."
    }
  ],
  "simplifications": [
    {
      "what": "The clockwise response sequence is written as fixed responder slots (responder 1, 2 and 3 relative to the opener), each a raise-or-call choice followed by a number step for raises",
      "why": "The engine runs flat step lists. Per-slot steps with when-conditions interleave the choice and the amount for each responder in order."
    },
    {
      "what": "A tie for the fewest tokens is a shared win rather than a declared draw",
      "why": "The engine's ranking makes players level at the top share the win. This matches the source's draw outcome in effect."
    },
    {
      "what": "The deck is reset and redealt with random draws each hand",
      "why": "Shuffling is modelled as drawing at random from the deck list."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: tokens; table: hand_number, opener_seat, current_declaration, current_declarer, caller, true_total, hand_loser.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
In the 'declaration of 60' scenario, do not require that the responder be offered 'call_coyote'. A forced call may be resolved automatically. Assert the outcome instead: current_declaration 60, current_declarer 1, caller 2, hand_loser 1, seat 1 tokens 1, seats 2 and 3 tokens 0, hand_number 2. Wherever possible, assert results and scores rather than which menus appear. Never assert on a responder's options when the rules leave that responder only one legal move.
````

## Reply

````
[
  {"name": "Start of game: 0 tokens, hand 1, opener seat 1", "rule": "R1", "players": 4, "rounds": 0, "seed": 1,
   "expect": {"players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}},
              "game": {"hand_number": 1, "opener_seat": 1}}},

  {"name": "Each of 3 players is dealt 1 card from the 33-card deck, leaving 30 (cards are random, so only counts are checked)", "rule": "R2", "players": 3, "rounds": 1, "seed": 2, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"lens": {"game": {"deck": 30}}}},

  {"name": "Each of 4 players is dealt 1 card, leaving 29 in the deck", "rule": "R2", "players": 4, "rounds": 1, "seed": 3, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"lens": {"game": {"deck": 29}}}},

  {"name": "Hidden cards are dealt and a hand still resolves: a call against -30 always costs the caller (any deal totals at least -20)", "rule": "R3", "players": 3, "rounds": 1, "seed": 4, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"game": {"caller": 2, "hand_loser": 2, "hand_number": 2},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "The opener may declare from -30 to 60 and becomes current_declarer", "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"game": {"current_declaration": -30, "current_declarer": 1},
              "offered": [{"seat": 1, "option": -30}, {"seat": 1, "option": 60}],
              "not_offered": [{"seat": 1, "option": 61}, {"seat": 1, "option": -31}]}},

  {"name": "A raise must be above current_declaration and at most 60; the raiser becomes current_declarer", "rule": "R5", "players": 4, "rounds": 1, "seed": 6, "default": "decline",
   "rules": [{"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": "raise"}, {"seat": 2, "options_include": 11},
             {"seat": 3, "options_include": "call_coyote"}],
   "expect": {"game": {"current_declaration": 11, "current_declarer": 2, "caller": 3},
              "offered": [{"seat": 2, "option": 11}, {"seat": 2, "option": 60}],
              "not_offered": [{"seat": 2, "option": 10}, {"seat": 2, "option": 61}]}},

  {"name": "At a declaration of 60 the responder can only call, and with 3 players the total never exceeds 50, so the declarer loses", "rule": "R6", "players": 3, "rounds": 1, "seed": 7, "default": "decline",
   "rules": [{"seat": 1, "options_include": 60}, {"seat": 2, "options_include": "raise"}],
   "expect": {"game": {"current_declaration": 60, "current_declarer": 1, "caller": 2, "hand_loser": 1, "hand_number": 2},
              "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "After a responder calls Coyote, no later responder acts", "rule": "R7", "players": 4, "rounds": 1, "seed": 8, "default": "decline",
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 2, "options_include": "call_coyote"},
             {"seat": 3, "options_include": "raise", "times": "all"}, {"seat": 4, "options_include": "raise", "times": "all"}],
   "expect": {"game": {"caller": 2, "current_declarer": 1, "current_declaration": 5},
              "not_offered": [{"seat": 3, "option": "raise"}, {"seat": 3, "option": "call_coyote"},
                              {"seat": 4, "option": "raise"}, {"seat": 4, "option": "call_coyote"}]}},

  {"name": "When everyone raises, the opener calls automatically, and loses on -28 since any deal totals at least -20", "rule": "R8", "players": 3, "rounds": 1, "seed": 9, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30},
             {"seat": 2, "options_include": "raise"}, {"seat": 2, "options_include": -29},
             {"seat": 3, "options_include": "raise"}, {"seat": 3, "options_include": -28}],
   "expect": {"game": {"caller": 1, "current_declarer": 3, "current_declaration": -28, "hand_loser": 1},
              "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "Total of 3 cards never exceeds 50 (plain sum or with Max to 0), so declaring 51 loses whatever the deal", "rule": "R9", "players": 3, "rounds": 1, "seed": 10, "default": "decline",
   "rules": [{"seat": 1, "options_include": 51}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"game": {"hand_loser": 1, "caller": 2},
              "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "With or without Max to 0 the total stays at most 50 for 3 players: a raise to 55 loses whatever the deal", "rule": "R10", "players": 3, "rounds": 1, "seed": 11, "default": "decline",
   "rules": [{"seat": 1, "options_include": 20},
             {"seat": 2, "options_include": "raise"}, {"seat": 2, "options_include": 55},
             {"seat": 3, "options_include": "call_coyote"}],
   "expect": {"game": {"current_declarer": 2, "current_declaration": 55, "caller": 3, "hand_loser": 2},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "The total is never below -20 (including Max to 0 with negative cards), so calling on -20 costs the caller whatever the deal", "rule": "R11", "players": 3, "rounds": 1, "seed": 12, "default": "decline",
   "rules": [{"seat": 1, "options_include": -20}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"game": {"caller": 2, "hand_loser": 2},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "true_total below the declaration: the declarer takes a token (60 with 3 players)", "rule": "R12", "players": 3, "rounds": 1, "seed": 13, "default": "decline",
   "rules": [{"seat": 1, "options_include": 60}],
   "expect": {"game": {"current_declaration": 60, "current_declarer": 1, "caller": 2, "hand_loser": 1, "hand_number": 2},
              "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "true_total at or above the declaration: the caller takes a token (-30 always met)", "rule": "R13", "players": 4, "rounds": 1, "seed": 14, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30},
             {"seat": 2, "options_include": "raise"}, {"seat": 2, "options_include": -25},
             {"seat": 3, "options_include": "call_coyote"}],
   "expect": {"game": {"caller": 3, "current_declarer": 2, "hand_loser": 3},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}, "4": {"tokens": 0}}}},

  {"name": "At hand end the seat taking the token is recorded and announced", "rule": "R14", "players": 4, "rounds": 1, "seed": 15, "default": "decline",
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"game": {"hand_loser": 2, "caller": 2, "current_declaration": -30},
              "players": {"2": {"tokens": 1}}}},

  {"name": "The opener moves clockwise and wraps from seat 3 to seat 1", "rule": "R15", "players": 3, "rounds": 1, "seed": 16, "default": "decline",
   "given": {"game": {"opener_seat": 3}},
   "rules": [{"seat": 3, "options_include": -30}, {"seat": 1, "options_include": "call_coyote"}],
   "expect": {"game": {"opener_seat": 1, "caller": 1, "hand_loser": 1, "current_declarer": 3},
              "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}}}},

  {"name": "After the 12th hand the game ends; level seats share the win", "rule": "R16", "players": 3, "seed": 17, "default": "decline",
   "given": {"game": {"hand_number": 12, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"winner": [1, 3], "standings": {"1": 0, "2": -1, "3": 0},
              "game": {"hand_number": 13},
              "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}}}},

  {"name": "Fewest tokens wins at the end", "rule": "R17", "players": 3, "seed": 18, "default": "decline",
   "given": {"players": {"1": {"tokens": 3}, "2": {"tokens": 1}, "3": {"tokens": 2}},
             "game": {"hand_number": 12, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": 60}],
   "expect": {"winner": 2, "standings": {"1": -4, "2": -1, "3": -2},
              "players": {"1": {"tokens": 4}, "2": {"tokens": 1}, "3": {"tokens": 2}}}},

  {"name": "Tied for fewest tokens share the win", "rule": "R17", "players": 3, "seed": 19, "default": "decline",
   "given": {"players": {"1": {"tokens": 2}, "2": {"tokens": 0}, "3": {"tokens": 1}},
             "game": {"hand_number": 12, "opener_seat": 1}},
   "rules": [{"seat": 1, "options_include": -30}, {"seat": 2, "options_include": "call_coyote"}],
   "expect": {"winner": [2, 3], "standings": {"1": -2, "2": -1, "3": -1},
              "players": {"1": {"tokens": 2}, "2": {"tokens": 1}, "3": {"tokens": 1}}}}
]
````
