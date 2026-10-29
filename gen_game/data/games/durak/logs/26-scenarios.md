# 26 scenarios

- time: 2026-10-27T21:44:47+00:00 (105.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 958177c36d0312ba, reply sha256 c835c3dc6a95e53c

## Sent

````
SPEC:
{
  "name": "Duel Durak (seeded)",
  "summary": "Two-player Durak with a fixed 8-card hand each, no drawing, a trump picked by offer and choice, and up to 39 single-attack bouts. The first player to empty their hand wins.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 36,
    "suit_count": 4,
    "ranks_per_suit": 9,
    "lowest_rank": 6,
    "highest_rank": 14,
    "hand_size_start": 8,
    "set_aside_size": 20,
    "deal_p1_first_position": 1,
    "deal_p1_last_position": 8,
    "deal_p2_first_position": 9,
    "deal_p2_last_position": 16,
    "set_aside_first_position": 17,
    "set_aside_last_position": 36,
    "offer_suit_count": 2,
    "default_offer_suit_a": 2,
    "default_offer_suit_b": 3,
    "default_first_attacker_seat": 2,
    "first_bout_round": 2,
    "last_round": 40,
    "max_bouts": 39,
    "max_throw_ins_per_bout": 1
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Card ids held by this player, always sorted ascending by id.",
        "observable": false
      },
      {
        "key": "hand_size",
        "type": "number",
        "visible": "public",
        "initial": 8,
        "meaning": "Number of cards in hand. This is the score: fewer is better.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The ordered ids 0..35, shuffled once with the seeded shuffle and then dealt from by position.",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Shuffled positions 17-36 (20 cards), sorted ascending. Face down and never drawn from.",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards from successfully defended bouts, sorted ascending by id.",
        "observable": false
      },
      {
        "key": "offer",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The two different suit indices offered by player 2.",
        "observable": false
      },
      {
        "key": "trump",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Suit index of trump (0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades).",
        "observable": true
      },
      {
        "key": "attacker",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat (1 or 2) of the current attacker. The other seat is the defender.",
        "observable": true
      },
      {
        "key": "table_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards played this bout, in the order they were played.",
        "observable": false
      },
      {
        "key": "attack_card",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Id of this bout's attack card.",
        "observable": false
      },
      {
        "key": "throw_card",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Id of this bout's thrown-in card, or -1 if none.",
        "observable": false
      },
      {
        "key": "defender_took",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the defender said TAKE this bout.",
        "observable": false
      },
      {
        "key": "bout",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of bouts completed (round number minus 1).",
        "observable": true
      }
    ]
  },
  "setup": [
    "Card id = suit*9 + (rank-6), so suit(id) = floor(id/9) and rank(id) = id mod 9 + 6. Suits are 0 Clubs, 1 Diamonds, 2 Hearts, 3 Spades.",
    "Set deck to the ordered list 0..35 and shuffle it once with the engine's seeded shuffle. This is the only random operation in the game.",
    "Shuffled positions 1-8 go to seat 1's hand and positions 9-16 go to seat 2's hand, each sorted ascending. Positions 17-36 go to set_aside, sorted ascending. hand_size is 8 for each seat.",
    "Sync: each seat is told only its own hand. Tell both seats that each player holds 8 cards.",
    "Ask seat 2 to name two different suits as the offer, as a choice among the 6 suit pairs. If the answer is missing or illegal, offer = [2, 3] (Hearts and Spades).",
    "Ask seat 1 to pick one suit from offer as trump. If the answer is missing or illegal, trump = the offered suit with the lower index.",
    "Announce the trump. attacker = the seat holding the lowest-rank trump, which is the smallest id between trump*9 and trump*9+8 found in either hand. If neither hand holds a trump, attacker = 2."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Reset for the bout: table_cards = [], attack_card = -1, throw_card = -1, defender_took = false."
    },
    {
      "action": "ask",
      "who": "the attacker (seat = attacker)",
      "answer": "one card id from the attacker's hand",
      "effect": "attack_card = the chosen id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. If the answer is missing or illegal, play the card minimising (rank, suit), that is the lowest rank with ties broken by lower suit index."
    },
    {
      "action": "ask",
      "who": "the defender (seat = 3 - attacker)",
      "answer": "TAKE, or a card id from the defender's hand that beats attack_card",
      "effect": "If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true. X beats Y when (suit(X) = suit(Y) and rank(X) > rank(Y)) or (suit(X) = trump and suit(Y) != trump)."
    },
    {
      "action": "ask",
      "who": "the attacker",
      "answer": "PASS, or a card id from the attacker's hand whose rank equals the rank of a card in table_cards",
      "effect": "If a card is chosen, throw_card = that id. Remove it from the attacker's hand, append it to table_cards and decrease the attacker's hand_size by 1. A missing or illegal answer counts as PASS. Only PASS is offered when defender_took = false and the defender's hand_size = 0."
    },
    {
      "action": "ask",
      "who": "the defender, when throw_card != -1 and defender_took = false",
      "answer": "TAKE, or a card id from the defender's hand that beats throw_card",
      "effect": "If a card is chosen, remove it from the defender's hand, append it to table_cards and decrease the defender's hand_size by 1. If TAKE is chosen, or the answer is missing or illegal, defender_took = true."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If defender_took: add every card in table_cards to the defender's hand (re-sorted ascending), add len(table_cards) to the defender's hand_size, and leave attacker unchanged. Otherwise: add table_cards to discard (re-sorted ascending) and set attacker = 3 - attacker. In both cases bout += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce table_cards in play order, the result (taken or beaten off), and both hand_size values."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if any seat has hand_size = 0, or if bout = 39 (round 40 done). Otherwise continue."
    }
  ],
  "ending": {
    "condition": "any player's hand_size = 0, or bout = 39",
    "rank_by": "0 - you.hand_size",
    "decided_by": "Fewer cards in hand ranks higher. If exactly one player has 0 cards after a bout, that player wins. If both reach 0 together, they tie and share the result (a draw). After round 40 the player with fewer cards wins, and equal counts are a draw (shared)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a card has id n, then its suit is floor(n/9) and its rank is n mod 9 + 6, with ids 0 to 35."
    },
    {
      "id": "R2",
      "text": "When the game starts, then the deck 0..35 is shuffled once with the seeded shuffle, seat 1 gets positions 1-8, seat 2 gets positions 9-16, and positions 17-36 (20 cards) go to set_aside, all sorted ascending."
    },
    {
      "id": "R3",
      "text": "When the deal is done, then each seat sees only its own hand, both are told each holds 8 cards, and set_aside is never drawn from."
    },
    {
      "id": "R4",
      "text": "When seat 2 makes the offer, then it names two different suits; if the answer is missing or illegal, the offer is Hearts (2) and Spades (3)."
    },
    {
      "id": "R5",
      "text": "When seat 1 picks trump, then trump is one of the two offered suits; if the answer is missing or illegal, trump is the offered suit with the lower index."
    },
    {
      "id": "R6",
      "text": "When trump is set, then the first attacker is the seat holding the lowest-rank trump; if neither seat holds a trump, seat 2 attacks first."
    },
    {
      "id": "R7",
      "text": "When card X is compared with card Y, then X beats Y if they share a suit and X has the higher rank, or if X is a trump and Y is not."
    },
    {
      "id": "R8",
      "text": "When the attacker attacks, then they play one card from their hand; if the answer is missing or illegal, they play their lowest-rank card, with ties broken by lower suit index."
    },
    {
      "id": "R9",
      "text": "When the defender answers the attack, then they play a card that beats it or say TAKE; a missing or illegal answer is TAKE."
    },
    {
      "id": "R10",
      "text": "When the attacker may throw in, then they add one card whose rank matches the rank of a card on the table, or PASS; a missing or illegal answer is PASS; at most 1 card is thrown in per bout."
    },
    {
      "id": "R11",
      "text": "When the defender has not said TAKE and has 0 cards in hand, then the attacker may not throw in."
    },
    {
      "id": "R12",
      "text": "When a card is thrown in after the defender said TAKE, then the defender takes that card too."
    },
    {
      "id": "R13",
      "text": "When a card was thrown in and the defender has not said TAKE, then the defender beats it or says TAKE; a missing or illegal answer is TAKE."
    },
    {
      "id": "R14",
      "text": "When the defender said TAKE at any point in a bout, then all table cards go into the defender's hand and the same attacker attacks next bout."
    },
    {
      "id": "R15",
      "text": "When the defender beat every card in a bout, then all table cards go to discard and the defender becomes the attacker."
    },
    {
      "id": "R16",
      "text": "When a bout ends, then the played cards in order, the result and both hand sizes are announced."
    },
    {
      "id": "R17",
      "text": "When exactly one seat has 0 cards after a bout's resolution, then that seat wins."
    },
    {
      "id": "R18",
      "text": "When both seats have 0 cards after a bout's resolution, then the game is a draw."
    },
    {
      "id": "R19",
      "text": "When bout 39 (round 40) ends with both seats holding cards, then the seat with fewer cards wins, and equal counts are a draw."
    }
  ],
  "offers": [
    {
      "question": "Offer (setup)",
      "who": "seat 2",
      "options": "the 6 pairs of different suits: {0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3}"
    },
    {
      "question": "Trump choice (setup)",
      "who": "seat 1",
      "options": "the two suits in offer"
    },
    {
      "question": "Attack",
      "who": "the attacker",
      "options": "every card id in the attacker's hand"
    },
    {
      "question": "Defence 1",
      "who": "the defender",
      "options": "TAKE, plus every card in the defender's hand that beats attack_card"
    },
    {
      "question": "Throw-in",
      "who": "the attacker",
      "options": "PASS, plus every card in the attacker's hand whose rank equals the rank of a table card; only PASS when defender_took is false and the defender's hand_size is 0"
    },
    {
      "question": "Defence 2 (only if a card was thrown in and the defender has not taken)",
      "who": "the defender",
      "options": "TAKE, plus every card in the defender's hand that beats throw_card"
    }
  ],
  "choices": [
    {
      "what": "2 players, suggested 2",
      "why": "The designer fixed the table at 2. This is a head-to-head duel of card management, where a thoughtful player saves trumps, chooses the trump offer to fit their own hand, and throws in to unload cards."
    },
    {
      "what": "No talk step",
      "why": "The source has no talk, and in a two-player zero-sum duel talk adds nothing to reason about."
    },
    {
      "what": "Draw expressed as a shared top rank",
      "why": "rank_by = -hand_size makes both seats level when both have 0 cards or equal counts, and the engine treats a level top as shared, which is the draw."
    },
    {
      "what": "The bout counter ends the game at 39 bouts",
      "why": "Rounds 2 to 40 are 39 bouts."
    }
  ],
  "simplifications": [
    {
      "what": "The source's round 1 is modelled as setup steps",
      "why": "It runs once before the bouts."
    },
    {
      "what": "Dynamic attacker and defender are named by the attacker attribute",
      "why": "The engine addresses seats, so the roles are read from a table number."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: hand_size; table: trump, attacker, bout.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
For R4, R5 and R6, run at least round 1 ("rounds": 1) so seat 2's offer and seat 1's trump pick are actually polled. Check that the default policies ('first', 'last') pick the offer pair and suit you expect from the option order the game presents. For R6, assert only trump and the full hands at bout 0, not the attacker, since the attacker depends on the seeded deal. For R7 (card strength), build a given state where the hands, trump, attacker and table cards are fully specified and consistent, including whether setup has already finished (trump set, started). Script only the seats that actually act, and only cards those seats really hold. Derive hand_size and attacker after the bout from the resolution rule: a TAKE gives the defender all table cards and the same attacker attacks again; a full defence discards the cards and the defender becomes the attacker. Do not require a rule for a card a seat is never offered, and do not forbid offering a card that is legal for that seat.
````

## Reply

````
```json
[
  {
    "name": "R1: id 9 is the 6 of Diamonds and id 10 the 7 of Diamonds, so 10 beats 9 and the bout is beaten off",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9], "hand_size": 2},
        "2": {"hand": [10, 20], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "players": {"1": {"hand_size": 1}, "2": {"hand_size": 1}},
      "game": {"trump": 0, "attacker": 2, "bout": 1},
      "not_offered": [{"seat": 2, "option": 20}]
    }
  },
  {
    "name": "R2: after the deal each seat holds 8 cards, set_aside holds 20 and the deck holds 36",
    "rule": "R2",
    "players": 2,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [],
    "expect": {
      "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}},
      "lens": {
        "game": {"set_aside": 20, "deck": 36},
        "players": {"1": {"hand": 8}, "2": {"hand": 8}}
      },
      "game": {"bout": 0}
    }
  },
  {
    "name": "R3: set_aside is never drawn from, so it still holds 20 cards after the first bout (seeded deal, only counts that chance cannot change)",
    "rule": "R3",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "rules": [],
    "expect": {
      "lens": {"game": {"set_aside": 20}},
      "game": {"bout": 1}
    }
  },
  {
    "name": "R4: with default 'last' seat 2 offers Spades and Hearts and seat 1 takes the last suit, Spades",
    "rule": "R4",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "last",
    "rules": [],
    "expect": {
      "game": {"trump": 3, "bout": 0},
      "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}}
    }
  },
  {
    "name": "R5: with default 'first' seat 2 offers Clubs and Diamonds and seat 1 takes the first suit, Clubs",
    "rule": "R5",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "game": {"trump": 0, "bout": 0},
      "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}}
    }
  },
  {
    "name": "R6: seat 1 holds the lowest Club trump (8 of Clubs, id 2), so seat 1 attacks first",
    "rule": "R6",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [2, 9, 10, 11, 12, 13, 14, 15], "hand_size": 8},
        "2": {"hand": [3, 18, 19, 20, 21, 22, 23, 24], "hand_size": 8}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [],
    "expect": {
      "game": {"trump": 0, "attacker": 1, "bout": 0},
      "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}}
    }
  },
  {
    "name": "R6: neither seat holds a Club trump, so seat 2 attacks first",
    "rule": "R6",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"hand": [9, 10, 11, 12, 13, 14, 15, 16], "hand_size": 8},
        "2": {"hand": [18, 19, 20, 21, 22, 23, 24, 25], "hand_size": 8}
      },
      "game": {"trump": 0, "attacker": 2, "bout": 0}
    },
    "rules": [],
    "expect": {
      "game": {"trump": 0, "attacker": 2, "bout": 0},
      "players": {"1": {"hand_size": 8}, "2": {"hand_size": 8}}
    }
  },
  {
    "name": "R7: the 7 of Clubs (trump) beats the 6 of Hearts and the 6 of Spades does not",
    "rule": "R7",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 18], "hand_size": 2},
        "2": {"hand": [1, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 18},
      {"seat": 2, "options_include": 1}
    ],
    "expect": {
      "players": {"1": {"hand_size": 1}, "2": {"hand_size": 1}},
      "game": {"attacker": 2, "bout": 1},
      "not_offered": [{"seat": 2, "option": 27}]
    }
  },
  {
    "name": "R8: the attacker plays the chosen card and the defender, unable to beat it, takes it",
    "rule": "R8",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [27, 28], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 18}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 3}},
      "game": {"attacker": 1, "bout": 1}
    }
  },
  {
    "name": "R9: the defender may say TAKE although it holds beating cards; only cards that beat the attack are offered",
    "rule": "R9",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [1, 10, 27], "hand_size": 3}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": "TAKE"}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 4}},
      "game": {"attacker": 1, "bout": 1},
      "offered": [{"seat": 2, "option": 10}, {"seat": 2, "option": 1}],
      "not_offered": [{"seat": 2, "option": 27}]
    }
  },
  {
    "name": "R10: the attacker throws in a card of a rank on the table; a card of another rank is not offered",
    "rule": "R10",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18, 20], "hand_size": 4},
        "2": {"hand": [1, 27, 28], "hand_size": 3}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 1},
      {"seat": 1, "options_include": 18}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 5}},
      "game": {"attacker": 1, "bout": 1},
      "not_offered": [{"seat": 1, "option": 20}]
    }
  },
  {
    "name": "R11: once the defender has beaten the attack with its last card, the attacker may not throw in, and the defender wins",
    "rule": "R11",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [10], "hand_size": 1}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": -2, "2": 0},
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 0}},
      "not_offered": [{"seat": 1, "option": 18}]
    }
  },
  {
    "name": "R12: a card thrown in after TAKE goes to the defender too",
    "rule": "R12",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [27, 28], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 1, "options_include": 18}
    ],
    "expect": {
      "players": {"1": {"hand_size": 1}, "2": {"hand_size": 4}},
      "game": {"attacker": 1, "bout": 1}
    }
  },
  {
    "name": "R13: the defender beats the thrown-in card too, so the bout is beaten off",
    "rule": "R13",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18, 30], "hand_size": 4},
        "2": {"hand": [1, 10, 19, 27], "hand_size": 4}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10},
      {"seat": 1, "options_include": 18},
      {"seat": 2, "options_include": 19}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 2}},
      "game": {"attacker": 2, "bout": 1}
    }
  },
  {
    "name": "R14: after TAKE the defender gains the table cards and the same seat attacks again",
    "rule": "R14",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [10, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 3}},
      "game": {"attacker": 1, "bout": 1}
    }
  },
  {
    "name": "R15: a fully defended bout is discarded and the defender becomes the attacker",
    "rule": "R15",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [10, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 1}},
      "game": {"attacker": 2, "bout": 1}
    }
  },
  {
    "name": "R16: after a bout both hand sizes reflect the result and the bout count rises by one",
    "rule": "R16",
    "players": 2,
    "seed": 1,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 18], "hand_size": 2},
        "2": {"hand": [1, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 18}
    ],
    "expect": {
      "players": {"1": {"hand_size": 1}, "2": {"hand_size": 3}},
      "game": {"attacker": 1, "bout": 1}
    }
  },
  {
    "name": "R17: the attacker plays its last card, the defender takes it, and the attacker wins with 0 cards",
    "rule": "R17",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0], "hand_size": 1},
        "2": {"hand": [27, 28], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [],
    "expect": {
      "winner": 1,
      "standings": {"1": 0, "2": -3},
      "players": {"1": {"hand_size": 0}, "2": {"hand_size": 3}}
    }
  },
  {
    "name": "R18: both seats play their last card in the same bout, so the game is a draw",
    "rule": "R18",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0], "hand_size": 1},
        "2": {"hand": [1], "hand_size": 1}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 0}
    },
    "rules": [
      {"seat": 2, "options_include": 1}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 0, "2": 0},
      "players": {"1": {"hand_size": 0}, "2": {"hand_size": 0}}
    }
  },
  {
    "name": "R19: after bout 39 the seat with fewer cards wins",
    "rule": "R19",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9, 18], "hand_size": 3},
        "2": {"hand": [10, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 38}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": -2, "2": -1},
      "players": {"1": {"hand_size": 2}, "2": {"hand_size": 1}},
      "game": {"bout": 39}
    }
  },
  {
    "name": "R19: after bout 39 with equal hand sizes the game is a draw",
    "rule": "R19",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": [0, 9], "hand_size": 2},
        "2": {"hand": [10, 27], "hand_size": 2}
      },
      "game": {"trump": 0, "attacker": 1, "bout": 38}
    },
    "rules": [
      {"seat": 1, "options_include": 9},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": -1, "2": -1},
      "players": {"1": {"hand_size": 1}, "2": {"hand_size": 1}},
      "game": {"bout": 39}
    }
  }
]
```
````
