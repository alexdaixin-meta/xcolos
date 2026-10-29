# 10 scenarios

- time: 2026-10-27T08:45:45+00:00 (33.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 5976b45279c45a85, reply sha256 8df809a9b2774be6

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
1. Do not assert on the `deck` list or its length. It is the coder's internal bookkeeping, and after a completed hand the cards are back in it. If you want to test the deal, check that each player's dealt card is a valid card value, or check `true_total` against the revealed cards.
2. The opening declaration and raises are numeric bids from -30 to 60, not entries in an option list. Drive them with a numeric-bid move that gives the exact value (for example, the opener bids 25). Then assert `current_declaration` = 25 and `current_declarer` = 1. Use `options_include` only for the named choices `raise` and `call_coyote`.
3. Keep the outcome check that does not depend on chance. If the opener declares -30 and seat 2 calls Coyote, assert seat 2 has 1 token, `hand_loser` = 2 and `hand_number` = 2, with the opener actually set to declare -30.
4. Do not predict results that depend on which cards are dealt.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "Setup: every seat has 0 tokens, hand 1, seat 1 opens",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_number": 1, "opener_seat": 1}
    }
  },
  {
    "name": "A hand is dealt and resolved with 4 players. An opening of -30 called by seat 2 costs seat 2, whatever cards are dealt",
    "rule": "R2",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_number": 2, "hand_loser": 2, "caller": 2, "current_declaration": -30, "current_declarer": 1}
    }
  },
  {
    "name": "Hidden cards do not stop a 3-player hand resolving. An opening of -30 called by seat 2 costs seat 2 (independent of the deal)",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}},
      "game": {"hand_loser": 2, "hand_number": 2}
    }
  },
  {
    "name": "Opener declares 25 and becomes current_declarer (the loser is not asserted because it depends on the deal)",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 25, "answer": 25},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"current_declaration": 25, "current_declarer": 1, "caller": 2}
    }
  },
  {
    "name": "Seat 2 raises from 10 to 20 and becomes current_declarer. Seat 3 calls",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 10, "answer": 10},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 20, "answer": 20},
      {"seat": 3, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"current_declaration": 20, "current_declarer": 2, "caller": 3}
    }
  },
  {
    "name": "At a declaration of 60 the responder may only call. With 3 players the total never reaches 60, so the declarer loses",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 60, "answer": 60},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"current_declaration": 60, "current_declarer": 1, "caller": 2, "hand_loser": 1},
      "offered": [{"seat": 2, "option": "call_coyote"}],
      "not_offered": [{"seat": 2, "option": "raise"}]
    }
  },
  {
    "name": "After seat 2 calls Coyote, seats 3 and 4 are not asked",
    "rule": "R7",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"2": {"tokens": 1}},
      "game": {"caller": 2, "hand_loser": 2},
      "not_offered": [
        {"seat": 3, "option": "raise"},
        {"seat": 3, "option": "call_coyote"},
        {"seat": 4, "option": "raise"},
        {"seat": 4, "option": "call_coyote"}
      ]
    }
  },
  {
    "name": "Everyone raises, so the opener calls automatically on 60. With 3 players the total is below 60 and the last raiser loses",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "answer": 0},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 59, "answer": 59},
      {"seat": 3, "options_include": "raise", "times": 1},
      {"seat": 3, "options_include": 60, "answer": 60}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}},
      "game": {"current_declaration": 60, "current_declarer": 3, "caller": 1, "hand_loser": 3}
    }
  },
  {
    "name": "Plain sums of 3 cards never reach 51, so an opening of 51 called by seat 2 costs the opener (independent of the deal)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 51, "answer": 51},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"hand_loser": 1}
    }
  },
  {
    "name": "Max to 0 counts 0, never 100, so a 3-player total never reaches 55 and the opener's 55 loses (independent of the deal)",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 55, "answer": 55},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"hand_loser": 1, "caller": 2}
    }
  },
  {
    "name": "The total is never below -20 (with Max to 0 and negative cards the minimum is -15), so an opening of -20 called by seat 2 costs the caller",
    "rule": "R11",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -20, "answer": -20},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_loser": 2}
    }
  },
  {
    "name": "Declaration above any possible 3-player total: the current declarer (seat 2, raised to 55) takes the token",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 40, "answer": 40},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 55, "answer": 55},
      {"seat": 3, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}},
      "game": {"current_declaration": 55, "current_declarer": 2, "caller": 3, "hand_loser": 2}
    }
  },
  {
    "name": "Automatic call on -28: the total is always at least -28, so the opener (the caller) takes the token",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": -29, "answer": -29},
      {"seat": 3, "options_include": "raise", "times": 1},
      {"seat": 3, "options_include": -28, "answer": -28}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"current_declaration": -28, "current_declarer": 3, "caller": 1, "hand_loser": 1}
    }
  },
  {
    "name": "At the end of a hand the loser seat is announced as hand_loser (opening -30, seat 2 calls)",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"hand_loser": 2, "current_declaration": -30, "caller": 2}
    }
  },
  {
    "name": "The opener moves from seat 3 to seat 1 (wrap) after the hand",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"opener_seat": 3, "hand_number": 5}},
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}},
      "game": {"opener_seat": 1, "hand_number": 6, "hand_loser": 1, "caller": 1}
    }
  },
  {
    "name": "The game ends after hand 12, and the seat with the fewest tokens wins",
    "rule": "R16",
    "players": 3,
    "given": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 12, "opener_seat": 3}
    },
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": -1, "2": -3, "3": -2},
      "players": {"1": {"tokens": 1}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 13}
    }
  },
  {
    "name": "Seats tied for the fewest tokens share the win",
    "rule": "R17",
    "players": 3,
    "given": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 12, "opener_seat": 3}
    },
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": -2, "2": -3, "3": -2},
      "players": {"1": {"tokens": 2}, "2": {"tokens": 3}, "3": {"tokens": 2}}
    }
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "Setup: every seat has 0 tokens, hand 1, seat 1 opens",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "rules": [
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_number": 1, "opener_seat": 1}
    }
  },
  {
    "name": "A hand is dealt and resolved with 4 players. An opening of -30 called by seat 2 costs seat 2, whatever cards are dealt",
    "rule": "R2",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_number": 2, "hand_loser": 2, "caller": 2, "current_declaration": -30, "current_declarer": 1}
    }
  },
  {
    "name": "Hidden cards do not stop a 3-player hand resolving. An opening of -30 called by seat 2 costs seat 2 (independent of the deal)",
    "rule": "R3",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}},
      "game": {"hand_loser": 2, "hand_number": 2}
    }
  },
  {
    "name": "Opener declares 25 and becomes current_declarer (the loser is not asserted because it depends on the deal)",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 25, "answer": 25},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"current_declaration": 25, "current_declarer": 1, "caller": 2}
    }
  },
  {
    "name": "Seat 2 raises from 10 to 20 and becomes current_declarer. Seat 3 calls",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 10, "answer": 10},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 20, "answer": 20},
      {"seat": 3, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"current_declaration": 20, "current_declarer": 2, "caller": 3}
    }
  },
  {
    "name": "At a declaration of 60 the responder may only call. With 3 players the total never reaches 60, so the declarer loses",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 60, "answer": 60},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"current_declaration": 60, "current_declarer": 1, "caller": 2, "hand_loser": 1},
      "offered": [{"seat": 2, "option": "call_coyote"}],
      "not_offered": [{"seat": 2, "option": "raise"}]
    }
  },
  {
    "name": "After seat 2 calls Coyote, seats 3 and 4 are not asked",
    "rule": "R7",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"2": {"tokens": 1}},
      "game": {"caller": 2, "hand_loser": 2},
      "not_offered": [
        {"seat": 3, "option": "raise"},
        {"seat": 3, "option": "call_coyote"},
        {"seat": 4, "option": "raise"},
        {"seat": 4, "option": "call_coyote"}
      ]
    }
  },
  {
    "name": "Everyone raises, so the opener calls automatically on 60. With 3 players the total is below 60 and the last raiser loses",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 0, "answer": 0},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 59, "answer": 59},
      {"seat": 3, "options_include": "raise", "times": 1},
      {"seat": 3, "options_include": 60, "answer": 60}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 0}, "3": {"tokens": 1}},
      "game": {"current_declaration": 60, "current_declarer": 3, "caller": 1, "hand_loser": 3}
    }
  },
  {
    "name": "Plain sums of 3 cards never reach 51, so an opening of 51 called by seat 2 costs the opener (independent of the deal)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 51, "answer": 51},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"hand_loser": 1}
    }
  },
  {
    "name": "Max to 0 counts 0, never 100, so a 3-player total never reaches 55 and the opener's 55 loses (independent of the deal)",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 55, "answer": 55},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"hand_loser": 1, "caller": 2}
    }
  },
  {
    "name": "The total is never below -20 (with Max to 0 and negative cards the minimum is -15), so an opening of -20 called by seat 2 costs the caller",
    "rule": "R11",
    "players": 4,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -20, "answer": -20},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}, "4": {"tokens": 0}},
      "game": {"hand_loser": 2}
    }
  },
  {
    "name": "Declaration above any possible 3-player total: the current declarer (seat 2, raised to 55) takes the token",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 40, "answer": 40},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": 55, "answer": 55},
      {"seat": 3, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 1}, "3": {"tokens": 0}},
      "game": {"current_declaration": 55, "current_declarer": 2, "caller": 3, "hand_loser": 2}
    }
  },
  {
    "name": "Automatic call on -28: the total is always at least -28, so the opener (the caller) takes the token",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "raise", "times": 1},
      {"seat": 2, "options_include": -29, "answer": -29},
      {"seat": 3, "options_include": "raise", "times": 1},
      {"seat": 3, "options_include": -28, "answer": -28}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 0}, "3": {"tokens": 0}},
      "game": {"current_declaration": -28, "current_declarer": 3, "caller": 1, "hand_loser": 1}
    }
  },
  {
    "name": "At the end of a hand the loser seat is announced as hand_loser (opening -30, seat 2 calls)",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": -30, "answer": -30},
      {"seat": 2, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "game": {"hand_loser": 2, "current_declaration": -30, "caller": 2}
    }
  },
  {
    "name": "The opener moves from seat 3 to seat 1 (wrap) after the hand",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"opener_seat": 3, "hand_number": 5}},
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "players": {"1": {"tokens": 1}},
      "game": {"opener_seat": 1, "hand_number": 6, "hand_loser": 1, "caller": 1}
    }
  },
  {
    "name": "The game ends after hand 12, and the seat with the fewest tokens wins",
    "rule": "R16",
    "players": 3,
    "given": {
      "players": {"1": {"tokens": 0}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 12, "opener_seat": 3}
    },
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": -1, "2": -3, "3": -2},
      "players": {"1": {"tokens": 1}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 13}
    }
  },
  {
    "name": "Seats tied for the fewest tokens share the win",
    "rule": "R17",
    "players": 3,
    "given": {
      "players": {"1": {"tokens": 1}, "2": {"tokens": 3}, "3": {"tokens": 2}},
      "game": {"hand_number": 12, "opener_seat": 3}
    },
    "rules": [
      {"seat": 3, "options_include": -30, "answer": -30},
      {"seat": 1, "options_include": "call_coyote", "times": "all"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": -2, "2": -3, "3": -2},
      "players": {"1": {"tokens": 2}, "2": {"tokens": 3}, "3": {"tokens": 2}}
    }
  }
]
```
````
