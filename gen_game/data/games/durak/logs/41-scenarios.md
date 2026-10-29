# 41 scenarios

- time: 2026-10-27T22:04:00+00:00 (102.3s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 8a2224d7b2881601, reply sha256 6c9b506062d5647f

## Sent

````
SPEC:
{
  "name": "Duel Durak",
  "summary": "Two-player Durak with no drawing: one bout per round, each with one attack and at most one throw-in; the first player to empty their hand wins, or after round 40 the player with fewer cards wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 36,
    "suits": 4,
    "cards_per_suit": 9,
    "rank_offset": 6,
    "hand_size": 8,
    "set_aside_size": 20,
    "seat1_first_position": 1,
    "seat1_last_position": 8,
    "seat2_first_position": 9,
    "seat2_last_position": 16,
    "set_aside_first_position": 17,
    "set_aside_last_position": 36,
    "trump_unset": -1,
    "card_unset": -1,
    "max_throw_ins_per_bout": 1,
    "trump_round": 1,
    "first_bout_round": 2,
    "last_round": 40,
    "suit_pairs": 6
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card ids (0-35) the player holds, kept in ascending order.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 8,
        "meaning": "Number of cards in hand. It is announced after every bout. Fewer is better, and 0 wins.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "ids 0..35",
        "meaning": "The shuffled deck that the hands and the set-aside pile are dealt from.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 20 cards at shuffled positions 17-36. They are never seen and never drawn.",
        "observable": false
      },
      {
        "key": "suit_pair",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The pair of suits seat 2 offers for trump.",
        "observable": false
      },
      {
        "key": "trump",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The trump suit: 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades. It is -1 until chosen.",
        "observable": true
      },
      {
        "key": "attacker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that attacks this bout (0 means none yet). The defender is the other seat.",
        "observable": true
      },
      {
        "key": "bout",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of bouts completed.",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current round. Round 1 is the trump choice, and rounds 2-40 are bouts.",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards from bouts that were beaten off.",
        "observable": false
      },
      {
        "key": "table_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played in the current bout.",
        "observable": false
      },
      {
        "key": "attack_card",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The attacking card this bout.",
        "observable": false
      },
      {
        "key": "defence_card",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The card that beat the attack card this bout.",
        "observable": false
      },
      {
        "key": "throw_card",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The thrown-in card this bout.",
        "observable": false
      },
      {
        "key": "defender_took",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the defender chose TAKE this bout.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Shuffle the deck of ids 0..35 once.",
    "Deal shuffled positions 1-8 into seat 1's hand and positions 9-16 into seat 2's hand. Sort both hands ascending.",
    "Put positions 17-36 (20 cards) into set_aside. They are never seen or drawn.",
    "Each seat sees only its own hand. Tell both players that each player holds 8 cards (hand_size = 8 each).",
    "Set trump = -1, attacker = 0 (none), bout = 0, discard = empty, round_number = 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_number += 1"
    },
    {
      "action": "ask",
      "who": "seat 2 (only when round_number = 1)",
      "answer": "one of: Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades. A missing or illegal answer means Clubs and Diamonds.",
      "effect": "suit_pair = the chosen pair, announced"
    },
    {
      "action": "ask",
      "who": "seat 1 (only when round_number = 1)",
      "answer": "one of the two suits in suit_pair. A missing or illegal answer means the first suit named.",
      "effect": "trump = the chosen suit's number (0-3), announced to both"
    },
    {
      "action": "update",
      "who": "all players (only when round_number = 1)",
      "answer": null,
      "effect": "attacker = the seat whose hand holds the lowest id c with floor(c/9) = trump. If neither seat holds a trump card, attacker = 2. Announced."
    },
    {
      "action": "update",
      "who": "all players (only when round_number >= 2)",
      "answer": null,
      "effect": "Step 1: table_cards = [], attack_card = -1, defence_card = -1, throw_card = -1, defender_took = false"
    },
    {
      "action": "ask",
      "who": "the attacker (only when round_number >= 2)",
      "answer": "any card in the attacker's hand. A missing or illegal answer means their lowest id.",
      "effect": "Step 2: remove the card from attacker.hand, append it to table_cards, set attack_card = card, and show it to both players"
    },
    {
      "action": "ask",
      "who": "the defender (only when round_number >= 2)",
      "answer": "TAKE, or any card d in the defender's hand that beats attack_card [(floor(d/9) = floor(attack_card/9) and d > attack_card) or (floor(d/9) = trump and floor(attack_card/9) != trump)]. A missing or illegal answer means TAKE.",
      "effect": "Steps 3-4: if a card is chosen, remove it from defender.hand, append it to table_cards, set defence_card = card, and show it. If TAKE, defender_took = true."
    },
    {
      "action": "ask",
      "who": "the attacker (only when round_number >= 2)",
      "answer": "PASS, plus (only if (defender_took or the defender's hand_size >= 1) and the attacker's hand_size >= 1) every card c in the attacker's hand with c mod 9 = attack_card mod 9, or with defence_card != -1 and c mod 9 = defence_card mod 9. A missing or illegal answer means PASS.",
      "effect": "Steps 5-6: if a card is chosen, remove it from attacker.hand, append it to table_cards, set throw_card = card, and show it"
    },
    {
      "action": "ask",
      "who": "the defender (only when round_number >= 2 and throw_card != -1 and defender_took = false)",
      "answer": "TAKE, or any card in the defender's hand that beats throw_card (same beating rule). A missing or illegal answer means TAKE.",
      "effect": "Steps 7-8: if a card is chosen, remove it from defender.hand and append it to table_cards. If TAKE, defender_took = true."
    },
    {
      "action": "update",
      "who": "all players (only when round_number >= 2)",
      "answer": null,
      "effect": "Step 9: if defender_took, append all table_cards to defender.hand (sorted ascending), keep the attacker, and announce 'taken'. Otherwise append table_cards to discard, set attacker = the defender's seat, and announce 'beaten off'. Then table_cards = []."
    },
    {
      "action": "update",
      "who": "all players (only when round_number >= 2)",
      "answer": null,
      "effect": "Step 10: hand_size = length of hand for both seats, announced. bout += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "Step 11: end if round_number >= 2 and any seat has hand_size = 0, or if round_number = 40. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "(round_number >= 2 and (seat1.hand_size = 0 or seat2.hand_size = 0)) or round_number = 40",
    "rank_by": "0 - you.hand_size",
    "decided_by": "Fewer cards in hand ranks higher. A seat at 0 cards while the other holds cards wins. Both at 0 is a shared result (draw). After round 40 the seat with fewer cards wins, and equal counts share (draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card id c has suit floor(c/9) (0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades) and rank (c mod 9) + 6. Two cards have the same rank when their ids are equal mod 9."
    },
    {
      "id": "R2",
      "text": "Card d beats card a when floor(d/9) = floor(a/9) and d > a, or when floor(d/9) = trump and floor(a/9) != trump. For example, with trump = 3, card 27 beats card 8, card 5 beats card 3, and card 3 does not beat card 5."
    },
    {
      "id": "R3",
      "text": "At setup, seat 1 holds shuffled positions 1-8 and seat 2 holds positions 9-16. Each has hand_size = 8, and the 20 remaining cards go to set_aside, which is never drawn."
    },
    {
      "id": "R4",
      "text": "At setup, trump = -1, attacker = 0 (none), bout = 0 and discard is empty."
    },
    {
      "id": "R5",
      "text": "In round 1, seat 2 picks one of 6 suit pairs. A missing or illegal answer gives Clubs and Diamonds."
    },
    {
      "id": "R6",
      "text": "In round 1, seat 1 picks one suit of that pair as trump. A missing or illegal answer gives the first suit named. Trump is announced."
    },
    {
      "id": "R7",
      "text": "After trump is set, the attacker is the seat holding the lowest-id trump card. If neither seat holds a trump card, seat 2 attacks first."
    },
    {
      "id": "R8",
      "text": "At the start of each bout, table_cards = [], attack_card = -1, defence_card = -1, throw_card = -1 and defender_took = false."
    },
    {
      "id": "R9",
      "text": "When the attacker attacks, the chosen card leaves their hand, goes to table_cards as attack_card and is shown. A missing or illegal answer plays their lowest id."
    },
    {
      "id": "R10",
      "text": "The defender is offered TAKE plus exactly the cards in their hand that beat attack_card. A missing or illegal answer means TAKE."
    },
    {
      "id": "R11",
      "text": "When the defender plays a card, it leaves their hand, goes to table_cards and becomes defence_card. When the defender chooses TAKE, defender_took becomes true."
    },
    {
      "id": "R12",
      "text": "The throw-in options are PASS plus attacker cards matching attack_card mod 9 or defence_card mod 9 (when defence_card != -1). Cards are added only if (defender_took or the defender holds >= 1 card) and the attacker holds >= 1 card."
    },
    {
      "id": "R13",
      "text": "When the defender beat the attack with their last card, the throw-in options are only PASS."
    },
    {
      "id": "R14",
      "text": "At most 1 card is thrown in per bout. A thrown card leaves the attacker's hand, goes to table_cards as throw_card and is shown. A missing or illegal answer means PASS."
    },
    {
      "id": "R15",
      "text": "When throw_card != -1 and defender_took is false, the defender is offered TAKE plus the cards in their hand that beat throw_card. A chosen card goes to table_cards, TAKE sets defender_took = true, and a missing or illegal answer means TAKE."
    },
    {
      "id": "R16",
      "text": "When throw_card != -1 and defender_took is already true, there is no second defence."
    },
    {
      "id": "R17",
      "text": "When defender_took is true at resolve, all table_cards go into the defender's hand, the attacker stays the attacker, and 'taken' is announced."
    },
    {
      "id": "R18",
      "text": "When defender_took is false at resolve, all table_cards go to discard, the defender becomes the attacker, and 'beaten off' is announced."
    },
    {
      "id": "R19",
      "text": "After each bout, both hand_size values are updated and announced, and bout increases by 1."
    },
    {
      "id": "R20",
      "text": "When exactly one seat has hand_size = 0 at an end check, that seat wins and the game ends."
    },
    {
      "id": "R21",
      "text": "When both seats have hand_size = 0 at an end check, the game ends in a draw."
    },
    {
      "id": "R22",
      "text": "When round 40 ends with both seats holding cards, the seat with fewer cards wins, and equal counts are a draw."
    }
  ],
  "offers": [
    {
      "question": "Round 1, suit pair",
      "who": "seat 2",
      "options": "Clubs and Diamonds; Clubs and Hearts; Clubs and Spades; Diamonds and Hearts; Diamonds and Spades; Hearts and Spades"
    },
    {
      "question": "Round 1, trump suit",
      "who": "seat 1",
      "options": "the two suits of suit_pair"
    },
    {
      "question": "Attack",
      "who": "the attacker",
      "options": "every card in the attacker's hand"
    },
    {
      "question": "Defence",
      "who": "the defender",
      "options": "TAKE, plus every card in the defender's hand that beats attack_card"
    },
    {
      "question": "Throw-in",
      "who": "the attacker",
      "options": "If (defender_took or the defender holds >= 1 card) and the attacker holds >= 1 card: PASS plus attacker cards with the same rank (id mod 9) as attack_card or as defence_card (if one was played). Otherwise, including when the defender beat the attack with their last card: PASS only."
    },
    {
      "question": "Second defence",
      "who": "the defender, only when throw_card != -1 and defender_took = false",
      "options": "TAKE, plus every card in the defender's hand that beats throw_card"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players, suggested 2",
      "why": "The designer fixed the table at 2. The rules (one attacker, one defender, seat-specific trump choice) only work for 2."
    },
    {
      "what": "No talk step",
      "why": "The source has none. With two opposed players, talk would only add words."
    },
    {
      "what": "attacker = 0 stands for 'none'",
      "why": "The attribute is numeric, and seats are 1 and 2."
    },
    {
      "what": "A round_number counter gates the round-1 trump steps and the round 2-40 bout steps",
      "why": "The step list is flat. Single-step `when` conditions reproduce the source's distinct round 1 without choosing blocks."
    },
    {
      "what": "rank_by = 0 - hand_size",
      "why": "This gives every stated outcome: an empty hand beats a non-empty one, both empty ties (draw), and after round 40 fewer cards wins with equal counts tying."
    },
    {
      "what": "Strategy at the table",
      "why": "Seat 2 offers a suit pair that avoids its opponent's likely strength, seat 1 picks the trump that suits its hand, and attackers lead cards the defender is unlikely to beat or that set up a same-rank throw-in, while defenders weigh beating against saving trumps."
    }
  ],
  "simplifications": [
    {
      "what": "Hand sorting is described in the update, not computed by a dedicated operation",
      "why": "Order affects only how a hand is displayed, never an outcome."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size; table: trump, attacker, bout.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the 'Two bouts' scenario so each given hand_size equals the number of cards in that seat's given hand. Derive the expected values by the rules: each TAKE adds the table cards (attack card plus any throw-in) to the defender's hand, and the attacker's hand shrinks by the cards played. With seat 2 starting on 3 cards and taking one card in each of two bouts, expect seat 2 hand_size 5, seat 1 hand_size reduced by 2, and bout = 2. Also make sure a given hand never contains cards that the setup left in set_aside, or override set_aside to match.
````

## Reply

````
```json
[
  {"name": "Setup deals 8 cards to each seat and sets 20 aside", "rule": "R3", "players": 2, "rounds": 0, "seed": 1,
   "expect": {"players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}},
              "lens": {"game": {"set_aside": 20}, "players": {"1": {"hand": 8}, "2": {"hand": 8}}}}},

  {"name": "Setup: no trump, no attacker, no bouts, empty discard", "rule": "R4", "players": 2, "rounds": 0, "seed": 2,
   "expect": {"game": {"trump": -1, "attacker": 0, "bout": 0}, "lens": {"game": {"discard": 0}}}},

  {"name": "Seat 2 picks Clubs and Hearts and seat 1 picks Hearts", "rule": "R5", "players": 2, "rounds": 1, "seed": 3, "default": "decline",
   "rules": [{"seat": 2, "options_include": "Clubs and Hearts"}, {"seat": 1, "options_include": "Hearts"}],
   "expect": {"game": {"trump": 2, "bout": 0},
              "offered": [{"seat": 2, "option": "Clubs and Diamonds"}, {"seat": 2, "option": "Hearts and Spades"}, {"seat": 2, "option": "Diamonds and Spades"}],
              "not_offered": [{"seat": 1, "option": "Clubs and Hearts"}]}},

  {"name": "Seat 1 picks Spades from Diamonds and Spades", "rule": "R6", "players": 2, "rounds": 1, "seed": 4, "default": "decline",
   "rules": [{"seat": 2, "options_include": "Diamonds and Spades"}, {"seat": 1, "options_include": "Spades"}],
   "expect": {"game": {"trump": 3},
              "offered": [{"seat": 1, "option": "Diamonds"}],
              "not_offered": [{"seat": 1, "option": "Clubs"}, {"seat": 1, "option": "Hearts"}]}},

  {"name": "Lowest trump (9) is held by seat 2, so seat 2 attacks", "rule": "R7", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [10, 20], "hand_size": 2}, "2": {"hand": [9, 30], "hand_size": 2}},
             "game": {"set_aside": []}},
   "rules": [{"seat": 2, "options_include": "Diamonds and Hearts"}, {"seat": 1, "options_include": "Diamonds"}],
   "expect": {"game": {"trump": 1, "attacker": 2},
              "players": {"1": {"hand_size": 2}, "2": {"hand_size": 2}}}},

  {"name": "Lowest trump (27) is held by seat 1, so seat 1 attacks", "rule": "R7", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [5, 27], "hand_size": 2}, "2": {"hand": [6, 28], "hand_size": 2}},
             "game": {"set_aside": []}},
   "rules": [{"seat": 2, "options_include": "Hearts and Spades"}, {"seat": 1, "options_include": "Spades"}],
   "expect": {"game": {"trump": 3, "attacker": 1}}},

  {"name": "No trump in either hand, so seat 2 attacks", "rule": "R7", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1], "hand_size": 2}, "2": {"hand": [2, 3], "hand_size": 2}},
             "game": {"set_aside": []}},
   "rules": [{"seat": 2, "options_include": "Hearts and Spades"}, {"seat": 1, "options_include": "Spades"}],
   "expect": {"game": {"trump": 3, "attacker": 2}}},

  {"name": "Same rank across suits: attack 0 lets seat 1 throw in 9, 18 or 27 but not 1", "rule": "R1", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1, 9, 18, 27], "hand_size": 5}, "2": {"hand": [5, 10], "hand_size": 2}},
             "game": {"trump": 2, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": "TAKE"}, {"seat": 1, "options_include": 9}],
   "expect": {"players": {"1": {"hand_size": 3}, "2": {"hand_size": 4}}, "game": {"attacker": 1, "bout": 1},
              "offered": [{"seat": 1, "option": 18}, {"seat": 1, "option": 27}, {"seat": 2, "option": 5}],
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 2, "option": 10}]}},

  {"name": "Trump 3: card 27 beats 8, card 7 and 3 do not", "rule": "R2", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [8, 12], "hand_size": 2}, "2": {"hand": [3, 7, 27], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 8}, {"seat": 2, "options_include": 27}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 2}}, "game": {"attacker": 2, "bout": 1},
              "not_offered": [{"seat": 2, "option": 3}, {"seat": 2, "option": 7}]}},

  {"name": "Trump 3: card 5 beats 3, card 2 does not", "rule": "R2", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3, 31], "hand_size": 2}, "2": {"hand": [2, 5, 27], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 3}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 4}}, "game": {"attacker": 1, "bout": 1},
              "offered": [{"seat": 2, "option": 5}, {"seat": 2, "option": 27}],
              "not_offered": [{"seat": 2, "option": 2}]}},

  {"name": "Second bout starts fresh: a take, then a beat-off passes the attack", "rule": "R8", "players": 2, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1, 5], "hand_size": 3}, "2": {"hand": [10, 20], "hand_size": 2}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 5}, {"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 5}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 2}}, "game": {"attacker": 2, "bout": 2}}},

  {"name": "Attack card leaves the attacker's hand", "rule": "R9", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4, 14], "hand_size": 2}, "2": {"hand": [22, 23], "hand_size": 2}},
             "game": {"trump": 0, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 14}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 3}}, "game": {"attacker": 1, "bout": 1},
              "lens": {"players": {"1": {"hand": 1}, "2": {"hand": 3}}}}},

  {"name": "Defender is offered TAKE plus exactly the beating cards 15 and 19", "rule": "R10", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [7, 12], "hand_size": 2}, "2": {"hand": [11, 15, 19, 30], "hand_size": 4}},
             "game": {"trump": 2, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 12}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 5}},
              "offered": [{"seat": 2, "option": 15}, {"seat": 2, "option": 19}, {"seat": 2, "option": "TAKE"}],
              "not_offered": [{"seat": 2, "option": 11}, {"seat": 2, "option": 30}]}},

  {"name": "Defence card leaves the defender's hand", "rule": "R11", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2, 16], "hand_size": 2}, "2": {"hand": [6, 20, 21], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 2}, {"seat": 2, "options_include": 6}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 2}}, "game": {"attacker": 2, "bout": 1}}},

  {"name": "Throw-in may match the defence card's rank (13 matches 4), not other ranks", "rule": "R12", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 13, 14], "hand_size": 3}, "2": {"hand": [4, 20, 21], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 4}, {"seat": 1, "options_include": 13}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 5}}, "game": {"attacker": 1, "bout": 1},
              "not_offered": [{"seat": 1, "option": 14}]}},

  {"name": "Defender beats with last card: only PASS, defender wins", "rule": "R13", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 9], "hand_size": 2}, "2": {"hand": [5], "hand_size": 1}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}],
   "expect": {"winner": 2, "standings": {"1": -1, "2": 0},
              "players": {"1": {"hand_size": 1}, "2": {"hand_size": 0}},
              "not_offered": [{"seat": 1, "option": 9}]}},

  {"name": "Only one card is thrown in after a take", "rule": "R14", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 9, 18, 27], "hand_size": 4}, "2": {"hand": [20, 21], "hand_size": 2}},
             "game": {"trump": 1, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 1, "options_include": 18}],
   "expect": {"players": {"1": {"hand_size": 2}, "2": {"hand_size": 4}}, "game": {"attacker": 1, "bout": 1},
              "offered": [{"seat": 1, "option": 9}, {"seat": 1, "option": 27}]}},

  {"name": "Second defence beats the throw-in and the bout is beaten off", "rule": "R15", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 9, 14], "hand_size": 3}, "2": {"hand": [5, 10, 30], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 5}, {"seat": 1, "options_include": 9}, {"seat": 2, "options_include": 10}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 1}}, "game": {"attacker": 2, "bout": 1},
              "offered": [{"seat": 2, "option": 30}, {"seat": 1, "option": 14}]}},

  {"name": "After TAKE, a thrown card gets no second defence", "rule": "R16", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1, 10, 22], "hand_size": 3}, "2": {"hand": [11, 20], "hand_size": 2}},
             "game": {"trump": 0, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 1}, {"seat": 1, "options_include": 10}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 4}}, "game": {"attacker": 1, "bout": 1},
              "not_offered": [{"seat": 2, "option": 11}]}},

  {"name": "Two bouts: seat 2 takes one card each time and seat 1 keeps attacking", "rule": "R17", "players": 2, "rounds": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1, 2, 3], "hand_size": 4}, "2": {"hand": [20, 21, 22], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 1, "options_include": 1}],
   "expect": {"players": {"1": {"hand_size": 2}, "2": {"hand_size": 5}}, "game": {"attacker": 1, "bout": 2}}},

  {"name": "Beaten off: cards leave play and the defender becomes attacker", "rule": "R18", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [12, 30], "hand_size": 2}, "2": {"hand": [15, 25], "hand_size": 2}},
             "game": {"trump": 2, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 12}, {"seat": 2, "options_include": 15}],
   "expect": {"players": {"1": {"hand_size": 1}, "2": {"hand_size": 1}}, "game": {"attacker": 2, "bout": 1}}},

  {"name": "One bout updates both hand sizes and bout becomes 1", "rule": "R19", "players": 2, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1, 2], "hand_size": 3}, "2": {"hand": [20, 21], "hand_size": 2}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 2}],
   "expect": {"players": {"1": {"hand_size": 2}, "2": {"hand_size": 3}}, "game": {"bout": 1}}},

  {"name": "Attacker plays its last card and wins", "rule": "R20", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [5], "hand_size": 1}, "2": {"hand": [20, 21], "hand_size": 2}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "expect": {"winner": 1, "standings": {"1": 0, "2": -3},
              "players": {"1": {"hand_size": 0}, "2": {"hand_size": 3}}}},

  {"name": "Both hands empty after the bout: shared result", "rule": "R21", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 9], "hand_size": 2}, "2": {"hand": [5, 10], "hand_size": 2}},
             "game": {"trump": 3, "attacker": 1, "round_number": 1, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}, {"seat": 2, "options_include": 5}, {"seat": 1, "options_include": 9}, {"seat": 2, "options_include": 10}],
   "expect": {"winner": [1, 2], "standings": {"1": 0, "2": 0},
              "players": {"1": {"hand_size": 0}, "2": {"hand_size": 0}}}},

  {"name": "After round 40 the seat with fewer cards wins", "rule": "R22", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1], "hand_size": 2}, "2": {"hand": [20, 21, 22], "hand_size": 3}},
             "game": {"trump": 3, "attacker": 1, "round_number": 39, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}],
   "expect": {"winner": 1, "standings": {"1": -1, "2": -4},
              "players": {"1": {"hand_size": 1}, "2": {"hand_size": 4}}}},

  {"name": "After round 40 equal hand sizes share the result", "rule": "R22", "players": 2, "default": "decline",
   "given": {"players": {"1": {"hand": [0, 1, 2], "hand_size": 3}, "2": {"hand": [20], "hand_size": 1}},
             "game": {"trump": 3, "attacker": 1, "round_number": 39, "set_aside": []}},
   "rules": [{"seat": 1, "options_include": 0}],
   "expect": {"winner": [1, 2], "standings": {"1": -2, "2": -2},
              "players": {"1": {"hand_size": 2}, "2": {"hand_size": 2}}}}
]
```
````
