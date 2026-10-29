# 27 scenarios

- time: 2026-10-27T21:58:25+00:00 (76.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 4b977dcb30238bf0, reply sha256 2fef184391c59268

## Sent

````
SPEC:
{
  "name": "Little Two",
  "summary": "A three-player climbing card game over up to 3 deals: shed your 9 cards by beating the pile with singles, pairs, triples or runs. Triples bomb singles and pairs. The lowest total penalty wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "deck_size": 30,
    "ranks": 10,
    "suits": 3,
    "hand_size": 9,
    "aside_size": 3,
    "max_deals": 3,
    "max_orbits": 40,
    "double_penalty_threshold": 7,
    "double_penalty_factor": 2,
    "top_rank_card_low": 28,
    "top_rank_card_high": 30,
    "top_card_penalty": 1,
    "min_play_cards": 1,
    "max_play_cards": 3,
    "run_length": 3,
    "initial_penalty": 0,
    "initial_deals_won": 0,
    "deals_won_tiebreak_multiplier": 10
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "card numbers (1-30) the player holds",
        "observable": false
      },
      {
        "key": "card_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of cards in hand",
        "observable": true
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "total penalty points; lower is better",
        "observable": true
      },
      {
        "key": "deals_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "deals this player won by emptying their hand",
        "observable": true
      },
      {
        "key": "last_action",
        "type": "text",
        "visible": "public",
        "initial": "no play yet",
        "meaning": "'pass' or the last play string, e.g. '13 14'",
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
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          13,
          14,
          15,
          16,
          17,
          18,
          19,
          20,
          21,
          22,
          23,
          24,
          25,
          26,
          27,
          28,
          29,
          30
        ],
        "meaning": "undealt cards during a deal",
        "observable": false
      },
      {
        "key": "aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the 3 undealt cards set aside each deal, seen by nobody",
        "observable": false
      },
      {
        "key": "deal_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of deals started",
        "observable": true
      },
      {
        "key": "orbit",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of orbits (engine rounds) begun",
        "observable": true
      },
      {
        "key": "deal_active",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "whether a deal is in progress",
        "observable": false
      },
      {
        "key": "leader_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that leads the current deal (equals deal_number)",
        "observable": false
      },
      {
        "key": "first_orbit",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true during the orbit in which a deal started",
        "observable": false
      },
      {
        "key": "pile_kind",
        "type": "text",
        "visible": "public",
        "initial": "empty",
        "meaning": "'empty', 'single', 'pair', 'triple' or 'run'",
        "observable": true
      },
      {
        "key": "pile_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "highest card number of the play on top of the pile",
        "observable": true
      },
      {
        "key": "last_player",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat of the last non-pass play (0 = nobody)",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat the 3 players in seats 1, 2 and 3.",
    "Every player starts with an empty hand, card_count 0, penalty 0, deals_won 0 and last_action 'no play yet'.",
    "The table starts with deal_number 0, orbit 0, deal_active false, pile_kind 'empty', pile_value 0 and last_player 0.",
    "No cards are dealt in setup. The first deal starts in step 2 of orbit 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "orbit += 1"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "deal_active == false and deal_number < 3",
      "effect": "Start a deal: deal_number += 1; set deck to cards 1..30, every hand to [] and aside to []; draw 9 random cards from deck into each player's hand (remove from deck, append to hand); move the remaining 3 deck cards into aside; every card_count = 9; leader_seat = deal_number; deal_active = true; first_orbit = true; pile_kind = 'empty'; pile_value = 0; last_player = leader_seat. Announce that deal {deal_number} has started and seat {leader_seat} leads."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "each player privately sees their own hand and the public state"
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat) and last_player == 1",
      "effect": "Clearance: pile_kind = 'empty', pile_value = 0"
    },
    {
      "action": "ask",
      "who": "seat 1",
      "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat)",
      "answer": "one option from the legal-play list built from seat 1's hand and the pile (see offers); the choice is shown to everyone",
      "effect": "the chosen option is recorded for the next step"
    },
    {
      "action": "update",
      "who": "seat 1",
      "answer": null,
      "when": "deal_active == true and not (first_orbit == true and 1 < leader_seat)",
      "effect": "If 'pass': seat1.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat1.hand; seat1.card_count -= number of cards; pile_kind = 'single' if 1 card, 'pair' if 2, 'triple' if 3 of one rank, 'run' if 3 of consecutive ranks; pile_value = highest card; last_player = 1; seat1.last_action = option."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "deal_active == true and seat1.card_count == 0",
      "effect": "seat1.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"
    },
    {
      "action": "update",
      "who": "seat 2",
      "answer": null,
      "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat) and last_player == 2",
      "effect": "Clearance: pile_kind = 'empty', pile_value = 0"
    },
    {
      "action": "ask",
      "who": "seat 2",
      "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat)",
      "answer": "one option from the legal-play list built from seat 2's hand and the pile (see offers); the choice is shown to everyone",
      "effect": "the chosen option is recorded for the next step"
    },
    {
      "action": "update",
      "who": "seat 2",
      "answer": null,
      "when": "deal_active == true and not (first_orbit == true and 2 < leader_seat)",
      "effect": "If 'pass': seat2.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat2.hand; seat2.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 2; seat2.last_action = option."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "deal_active == true and seat2.card_count == 0",
      "effect": "seat2.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"
    },
    {
      "action": "update",
      "who": "seat 3",
      "answer": null,
      "when": "deal_active == true and last_player == 3",
      "effect": "Clearance: pile_kind = 'empty', pile_value = 0"
    },
    {
      "action": "ask",
      "who": "seat 3",
      "when": "deal_active == true",
      "answer": "one option from the legal-play list built from seat 3's hand and the pile (see offers); the choice is shown to everyone",
      "effect": "the chosen option is recorded for the next step"
    },
    {
      "action": "update",
      "who": "seat 3",
      "answer": null,
      "when": "deal_active == true",
      "effect": "If 'pass': seat3.last_action = 'pass'. Otherwise split the option on spaces into cards; remove each card from seat3.hand; seat3.card_count -= number of cards; set pile_kind by the cards (single, pair, triple or run); pile_value = highest card; last_player = 3; seat3.last_action = option."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "deal_active == true and seat3.card_count == 0",
      "effect": "seat3.deals_won += 1; for each other seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "first_orbit = false"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "when": "orbit == 40 and deal_active == true",
      "effect": "For every seat with n = card_count: penalty += n * (2 if n >= 7 else 1) + (number of cards in hand numbered 28, 29 or 30); deal_active = false"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if (deal_number == 3 and deal_active == false) or orbit >= 40; otherwise continue"
    }
  ],
  "ending": {
    "condition": "(deal_number == 3 and deal_active == false) or orbit >= 40",
    "rank_by": "you.deals_won - 10 * you.penalty",
    "decided_by": "The lowest total penalty wins. Among players tied for lowest penalty, the one with the most deals_won wins. Players still tied share the win, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "Card c has rank floor((c+2)/3), from 1 to 10, and suit c - 3*(rank-1), from 1 to 3; for example card 13 is rank 5 suit 1 and card 16 is rank 6 suit 1."
    },
    {
      "id": "R2",
      "text": "A higher card number is always a higher card, and the value of a play is its highest card number."
    },
    {
      "id": "R3",
      "text": "A single is 1 card, a pair is 2 cards of the same rank, a triple is 3 cards of the same rank, and a run is 3 cards of three consecutive ranks without wrap-around; any other set of cards is not a play."
    },
    {
      "id": "R4",
      "text": "When '13 14' is offered it is a pair; '14 16' is never offered as a pair."
    },
    {
      "id": "R5",
      "text": "Each orbit begins with orbit increased by 1."
    },
    {
      "id": "R6",
      "text": "When deal_active is false and deal_number < 3 at the start of an orbit, deal_number increases by 1, each player gets 9 random cards, 3 cards go to the hidden aside, every card_count becomes 9, leader_seat = deal_number, first_orbit = true, pile_kind = 'empty', pile_value = 0 and last_player = leader_seat."
    },
    {
      "id": "R7",
      "text": "Seat 1 leads deal 1, seat 2 leads deal 2 and seat 3 leads deal 3."
    },
    {
      "id": "R8",
      "text": "Seats take turns in order 1, 2, 3; a seat is skipped when deal_active is false, or when first_orbit is true and its seat number is below leader_seat."
    },
    {
      "id": "R9",
      "text": "When a seat's turn starts and last_player equals that seat, pile_kind becomes 'empty' and pile_value becomes 0, and that seat leads."
    },
    {
      "id": "R10",
      "text": "When pile_kind is 'empty', the seat is offered every single, pair, triple and run from its hand, and 'pass' is not offered."
    },
    {
      "id": "R11",
      "text": "When pile_kind is 'single', the seat is offered 'pass', every single with value > pile_value and every triple of any value."
    },
    {
      "id": "R12",
      "text": "When pile_kind is 'pair', the seat is offered 'pass', every pair with value > pile_value and every triple of any value."
    },
    {
      "id": "R13",
      "text": "When pile_kind is 'triple', the seat is offered 'pass' and every triple with value > pile_value."
    },
    {
      "id": "R14",
      "text": "When pile_kind is 'run', the seat is offered 'pass' and every run with value > pile_value."
    },
    {
      "id": "R15",
      "text": "When a seat passes, its last_action becomes 'pass' and nothing else changes."
    },
    {
      "id": "R16",
      "text": "When a seat plays k cards, those cards leave its hand, card_count drops by k, pile_value becomes the highest card played, last_player becomes that seat and last_action becomes the option string."
    },
    {
      "id": "R17",
      "text": "After a play, pile_kind is 'single' for 1 card, 'pair' for 2, 'triple' for 3 of one rank and 'run' for 3 consecutive ranks; a triple bombing a single or pair sets pile_kind to 'triple'."
    },
    {
      "id": "R18",
      "text": "When a seat's card_count reaches 0, its deals_won increases by 1, deal_active becomes false and the rest of that orbit's turns are skipped."
    },
    {
      "id": "R19",
      "text": "When a deal is won, each other seat with n cards adds n to penalty, or 2n if n >= 7, plus 1 per card numbered 28, 29 or 30 it holds; for example 7 cards including card 30 adds 15."
    },
    {
      "id": "R20",
      "text": "At the end of every orbit first_orbit becomes false."
    },
    {
      "id": "R21",
      "text": "When orbit 40 ends with a deal still active, every seat adds the same penalty formula for the cards it holds."
    },
    {
      "id": "R22",
      "text": "The game ends when deal 3 has ended or when orbit 40 is complete, and deals that never started are not played."
    },
    {
      "id": "R23",
      "text": "The lowest penalty wins, ties are broken by the most deals_won, and players still tied share the win."
    },
    {
      "id": "R24",
      "text": "Hands and the aside cards are hidden; card_count, penalty, deals_won, last_action and the pile are public."
    }
  ],
  "offers": [
    {
      "question": "Turn choice when pile_kind is 'empty' (leading)",
      "who": "the seat whose turn it is",
      "options": "every single, pair, triple and run that can be made from its hand, each written as ascending card numbers separated by single spaces; no 'pass'"
    },
    {
      "question": "Turn choice when pile_kind is 'single'",
      "who": "the seat whose turn it is",
      "options": "'pass'; every single from its hand with card number > pile_value; every triple from its hand of any value"
    },
    {
      "question": "Turn choice when pile_kind is 'pair'",
      "who": "the seat whose turn it is",
      "options": "'pass'; every pair from its hand whose higher card > pile_value; every triple from its hand of any value"
    },
    {
      "question": "Turn choice when pile_kind is 'triple'",
      "who": "the seat whose turn it is",
      "options": "'pass'; every triple from its hand whose highest card > pile_value"
    },
    {
      "question": "Turn choice when pile_kind is 'run'",
      "who": "the seat whose turn it is",
      "options": "'pass'; every run from its hand whose highest card > pile_value"
    },
    {
      "question": "Any turn",
      "who": "seats skipped by rule R8 or after the deal ended",
      "options": "not asked"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the game at 3 seats. The clearance rule ('the other two have passed') and the leader rotation over 3 deals assume exactly three seats."
    },
    {
      "what": "No talk phase",
      "why": "The rules say there is no talk phase. All information comes from public plays, passes and card counts."
    },
    {
      "what": "Turns use ask, one seat at a time",
      "why": "The order of play matters, and each seat must see the earlier plays it has to beat."
    },
    {
      "what": "rank_by = deals_won - 10 * penalty",
      "why": "deals_won is at most 3, so a factor of 10 makes a lower penalty dominate and uses deals_won only as the tie-break. Players still tied share the win, which matches the source's draw."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player keeps triples as bombs, holds high cards (28-30) to regain the lead, tracks which high cards are gone, and dumps cards before falling to 7 or more, where the penalty doubles."
    }
  ],
  "simplifications": [
    {
      "what": "The legal-play option list is computed by the engine from the seat's hand list and the pile each turn",
      "why": "The engine offers choices from a list. The rules define the options exactly, so they are generated by arithmetic on card numbers rather than typed freely."
    },
    {
      "what": "Each deal resets the deck to cards 1..30 and empties hands and aside before dealing",
      "why": "This is the 'shuffle all 30 cards' step expressed as list operations followed by random draws."
    },
    {
      "what": "The three seat turns are written out as three fixed blocks of steps, each with a when-condition",
      "why": "The step list is flat. Per-step conditions reproduce the skip rules and the end-of-deal cutoff."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: card_count, penalty, deals_won, last_action; table: deal_number, orbit, pile_kind, pile_value.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "R1 ranks: 13,14,15 make a triple and 13,16,19 make a run", "rule": "R1", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,14,15,16,19,1,4,25,27], "card_count": 9},
                         "2": {"hand": [2,3,5,6,8,9,10,11,12], "card_count": 9},
                         "3": {"hand": [17,18,20,21,22,23,24,26,28], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "13 16 19"}],
   "expect": {"offered": [{"seat": 1, "option": "13 14 15"}, {"seat": 1, "option": "13 16 19"}],
              "not_offered": [{"seat": 1, "option": "13 16"}, {"seat": 1, "option": "14 16"}],
              "players": {"1": {"card_count": 6, "last_action": "13 16 19"}},
              "game": {"pile_kind": "run", "pile_value": 19}}},

  {"name": "R2 a higher card number beats a single of the same rank", "rule": "R2", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,15,1,4,7,10,22,25,28], "card_count": 9},
                         "2": {"hand": [2,5,8,11,16,19,23,26,29], "card_count": 9},
                         "3": {"hand": [3,6,9,12,17,20,24,27,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "15"}],
   "expect": {"not_offered": [{"seat": 1, "option": "13"}],
              "players": {"1": {"card_count": 8, "last_action": "15"}},
              "game": {"pile_kind": "single", "pile_value": 15}}},

  {"name": "R3 runs and triples are offered when leading, other sets are not", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,11,12,20,25,28], "card_count": 9},
                         "2": {"hand": [2,5,8,13,16,19,22,26,29], "card_count": 9},
                         "3": {"hand": [3,6,9,14,17,21,23,27,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "10 11 12"}],
   "expect": {"offered": [{"seat": 1, "option": "1 4 7"}, {"seat": 1, "option": "10 11 12"}],
              "not_offered": [{"seat": 1, "option": "1 4 10"}, {"seat": 1, "option": "1 4 28"}, {"seat": 1, "option": "1 4"}],
              "players": {"1": {"card_count": 6, "last_action": "10 11 12"}},
              "game": {"pile_kind": "triple", "pile_value": 12}}},

  {"name": "R4 13 14 is a pair, 14 16 is not", "rule": "R4", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,14,16,1,5,9,21,26,30], "card_count": 9},
                         "2": {"hand": [2,4,7,10,17,19,22,25,28], "card_count": 9},
                         "3": {"hand": [3,6,8,11,12,18,20,23,29], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "13 14"}],
   "expect": {"offered": [{"seat": 1, "option": "13 14"}],
              "not_offered": [{"seat": 1, "option": "14 16"}],
              "players": {"1": {"card_count": 7, "last_action": "13 14"}},
              "game": {"pile_kind": "pair", "pile_value": 14}}},

  {"name": "R5 orbit increases by 1 each round", "rule": "R5", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,5,9,13,17,21,25,29,30], "card_count": 9},
                         "2": {"hand": [2,6,10,14,18,22,26,27,28], "card_count": 9},
                         "3": {"hand": [3,4,7,8,11,12,15,16,19], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "1"}],
   "expect": {"game": {"orbit": 6}, "players": {"1": {"card_count": 8}}}},

  {"name": "R6 first deal gives 9 cards each and 3 aside (chance: only counts asserted)", "rule": "R6", "players": 3, "rounds": 1, "default": "decline",
   "expect": {"game": {"deal_number": 1, "orbit": 1},
              "players": {"2": {"card_count": 9, "last_action": "pass"}, "3": {"card_count": 9, "last_action": "pass"}},
              "lens": {"game": {"aside": 3, "deck": 0}, "players": {"2": {"hand": 9}, "3": {"hand": 9}}}}},

  {"name": "R7 seat 2 leads deal 2 and seat 1 is skipped in its first orbit (chance: counts only)", "rule": "R7", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"penalty": 4, "deals_won": 1}, "2": {"penalty": 6}, "3": {"penalty": 9}},
             "game": {"deal_number": 1, "deal_active": false, "orbit": 10, "pile_kind": "empty", "pile_value": 0}},
   "expect": {"game": {"deal_number": 2, "orbit": 11},
              "players": {"1": {"card_count": 9}, "3": {"card_count": 9, "last_action": "pass"}},
              "lens": {"game": {"aside": 3}}}},

  {"name": "R8 in deal 3's first orbit seats 1 and 2 are skipped (chance: counts only)", "rule": "R8", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"penalty": 4}, "2": {"penalty": 6}, "3": {"penalty": 9}},
             "game": {"deal_number": 2, "deal_active": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0}},
   "expect": {"game": {"deal_number": 3, "orbit": 21},
              "players": {"1": {"card_count": 9}, "2": {"card_count": 9}}}},

  {"name": "R9 the pile clears when play comes back to the last player", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,13], "card_count": 5},
                         "2": {"hand": [5,8,26], "card_count": 3},
                         "3": {"hand": [27,29,30], "card_count": 3}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 20, "last_player": 2}},
   "rules": [{"seat": 2, "options_include": "5"}],
   "expect": {"not_offered": [{"seat": 2, "option": "pass"}],
              "players": {"1": {"last_action": "pass", "card_count": 5}, "2": {"card_count": 2, "last_action": "5"}},
              "game": {"pile_kind": "single", "pile_value": 5}}},

  {"name": "R10 leading on an empty pile: pass is not offered", "rule": "R10", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3,6,9,12,14,17,20,23,26], "card_count": 9},
                         "2": {"hand": [1,4,7,10,15,18,21,24,27], "card_count": 9},
                         "3": {"hand": [2,5,8,11,13,16,19,22,25], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "3"}],
   "expect": {"offered": [{"seat": 1, "option": "3"}, {"seat": 1, "option": "26"}],
              "not_offered": [{"seat": 1, "option": "pass"}],
              "players": {"1": {"card_count": 8, "last_action": "3"}},
              "game": {"pile_kind": "single", "pile_value": 3}}},

  {"name": "R11 on a single: pass, higher singles and any triple are offered", "rule": "R11", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [10,15,20,22,23,24,1,4,7], "card_count": 9},
                         "2": {"hand": [2,5,8,11,16,19,25,28,29], "card_count": 9},
                         "3": {"hand": [3,6,9,12,13,17,18,21,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "pass"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "15"}, {"seat": 1, "option": "20"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "10"}, {"seat": 1, "option": "22 23"}],
              "players": {"1": {"card_count": 9, "last_action": "pass"}}}},

  {"name": "R12 on a pair: pass, higher pairs and any triple are offered", "rule": "R12", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [10,11,15,16,17,22,23,24,1], "card_count": 9},
                         "2": {"hand": [2,4,7,12,18,19,25,28,29], "card_count": 9},
                         "3": {"hand": [3,5,6,8,9,20,21,26,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "pair", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "16 17"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "16 17"}, {"seat": 1, "option": "22 23"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "10 11"}, {"seat": 1, "option": "15"}],
              "players": {"1": {"card_count": 7, "last_action": "16 17"}},
              "game": {"pile_kind": "pair", "pile_value": 17}}},

  {"name": "R13 on a triple: only pass and higher triples", "rule": "R13", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4,5,6,22,23,24,15,16,1], "card_count": 9},
                         "2": {"hand": [2,3,7,8,9,17,18,19,25], "card_count": 9},
                         "3": {"hand": [13,14,20,21,26,27,28,29,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "triple", "pile_value": 12, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "22 23 24"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "4 5 6"}, {"seat": 1, "option": "15"}, {"seat": 1, "option": "1"}],
              "players": {"1": {"card_count": 6, "last_action": "22 23 24"}},
              "game": {"pile_kind": "triple", "pile_value": 24}}},

  {"name": "R14 on a run: only pass and higher runs", "rule": "R14", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2,5,8,22,23,24,30], "card_count": 7},
                         "2": {"hand": [3,6,9,10,11,12,13,14,15], "card_count": 9},
                         "3": {"hand": [16,17,18,19,20,21,25,26,27], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "run", "pile_value": 7, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "2 5 8"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "2 5 8"}],
              "not_offered": [{"seat": 1, "option": "22 23 24"}, {"seat": 1, "option": "30"}],
              "players": {"1": {"card_count": 4, "last_action": "2 5 8"}},
              "game": {"pile_kind": "run", "pile_value": 8}}},

  {"name": "R15 passing only sets last_action", "rule": "R15", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [25,1,4], "card_count": 3, "penalty": 2, "deals_won": 1},
                         "2": {"hand": [2,5,8,11], "card_count": 4},
                         "3": {"hand": [3,6,9,12,15], "card_count": 5}},
             "game": {"deal_number": 2, "deal_active": true, "leader_seat": 2, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 20, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "pass"}],
   "expect": {"offered": [{"seat": 1, "option": "25"}],
              "players": {"1": {"card_count": 3, "last_action": "pass", "penalty": 2, "deals_won": 1}}}},

  {"name": "R16 playing a pair removes 2 cards and records the play", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [16,17,2,5,8,11,26,27,29], "card_count": 9},
                         "2": {"hand": [1,4,7,10,13,19,22,25,28], "card_count": 9},
                         "3": {"hand": [3,6,9,12,14,15,18,20,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "16 17"}],
   "expect": {"players": {"1": {"card_count": 7, "last_action": "16 17"}},
              "game": {"pile_kind": "pair", "pile_value": 17}}},

  {"name": "R17 a triple bombs a single and the pile becomes a triple", "rule": "R17", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,2,3,22,23,24,10,13,26], "card_count": 9},
                         "2": {"hand": [4,5,7,8,11,16,19,25,28], "card_count": 9},
                         "3": {"hand": [6,9,12,17,18,20,21,29,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "22 23 24"}],
   "expect": {"offered": [{"seat": 1, "option": "1 2 3"}, {"seat": 1, "option": "22 23 24"}],
              "players": {"1": {"card_count": 6, "last_action": "22 23 24"}},
              "game": {"pile_kind": "triple", "pile_value": 24}}},

  {"name": "R18 emptying a hand wins the deal and skips the rest of the orbit", "rule": "R18", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1},
                         "2": {"hand": [1,2,4,5,7,8,10], "card_count": 7},
                         "3": {"hand": [28,3,6], "card_count": 3}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"not_offered": [{"seat": 2, "option": "pass"}, {"seat": 3, "option": "pass"}],
              "players": {"1": {"card_count": 0, "deals_won": 1, "penalty": 0},
                          "2": {"card_count": 7, "penalty": 14},
                          "3": {"card_count": 3, "penalty": 4}}}},

  {"name": "R19 penalty: 7 cards with card 30 adds 15, 6 cards with card 28 adds 7", "rule": "R19", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [29], "card_count": 1},
                         "2": {"hand": [1,4,7,10,13,16,30], "card_count": 7, "penalty": 3},
                         "3": {"hand": [28,2,5,8,11,14], "card_count": 6}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "29"}],
   "expect": {"players": {"1": {"penalty": 0, "deals_won": 1},
                          "2": {"penalty": 18},
                          "3": {"penalty": 7}}}},

  {"name": "R20 after the first orbit of deal 2, seat 1 gets its turn (chance: counts only)", "rule": "R20", "players": 3, "rounds": 2, "default": "decline",
   "given": {"game": {"deal_number": 1, "deal_active": false, "orbit": 10, "pile_kind": "empty", "pile_value": 0}},
   "expect": {"offered": [{"seat": 1, "option": "pass"}],
              "players": {"1": {"card_count": 9, "last_action": "pass"}},
              "game": {"deal_number": 2, "orbit": 12}}},

  {"name": "R21 orbit 40 ends an active deal and every seat is penalised", "rule": "R21", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,13,16,19], "card_count": 7},
                         "2": {"hand": [2,5,8], "card_count": 3},
                         "3": {"hand": [3,6,28,29], "card_count": 4}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 39, "pile_kind": "single", "pile_value": 30, "last_player": 3}},
   "rules": [{"seat": 3, "options_include": "3"}],
   "expect": {"winner": 2,
              "standings": {"1": -140, "2": -30, "3": -50},
              "players": {"1": {"penalty": 14}, "2": {"penalty": 3}, "3": {"penalty": 5, "card_count": 3}},
              "game": {"orbit": 40, "deal_number": 1}}},

  {"name": "R22 the game ends when deal 3 is won", "rule": "R22", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 5, "deals_won": 1},
                         "2": {"hand": [1,2], "card_count": 2, "penalty": 2, "deals_won": 1},
                         "3": {"hand": [4], "card_count": 1, "penalty": 10, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": 2,
              "standings": {"1": -48, "2": -39, "3": -110},
              "players": {"1": {"penalty": 5, "deals_won": 2}, "2": {"penalty": 4}, "3": {"penalty": 11}},
              "game": {"deal_number": 3, "orbit": 21}}},

  {"name": "R23 tied lowest penalty and tied deals_won share the win", "rule": "R23", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 6, "deals_won": 0},
                         "2": {"hand": [1], "card_count": 1, "penalty": 5, "deals_won": 1},
                         "3": {"hand": [4], "card_count": 1, "penalty": 5, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": -59, "2": -59, "3": -60},
              "players": {"1": {"penalty": 6, "deals_won": 1}, "2": {"penalty": 6}, "3": {"penalty": 6}}}},

  {"name": "R23 tied lowest penalty is broken by more deals_won", "rule": "R23", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 6, "deals_won": 0},
                         "2": {"hand": [1], "card_count": 1, "penalty": 5, "deals_won": 2},
                         "3": {"hand": [4], "card_count": 1, "penalty": 5, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": 2,
              "standings": {"1": -59, "2": -58, "3": -60},
              "players": {"1": {"penalty": 6, "deals_won": 1}, "2": {"penalty": 6, "deals_won": 2}, "3": {"penalty": 6}}}},

  {"name": "R24 public state right after setup, no cards dealt yet", "rule": "R24", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"card_count": 0, "penalty": 0, "deals_won": 0, "last_action": "no play yet"},
                          "2": {"card_count": 0, "penalty": 0, "deals_won": 0, "last_action": "no play yet"},
                          "3": {"card_count": 0, "penalty": 0, "deals_won": 0, "last_action": "no play yet"}},
              "game": {"deal_number": 0, "orbit": 0, "pile_kind": "empty", "pile_value": 0},
              "lens": {"game": {"aside": 0}, "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}}
]

Why it was refused: scenario 6: needs `rules` (what each seat answers, by option name); scenario 7: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "R1 ranks: 13,14,15 make a triple and 13,16,19 make a run", "rule": "R1", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,14,15,16,19,1,4,25,27], "card_count": 9},
                         "2": {"hand": [2,3,5,6,8,9,10,11,12], "card_count": 9},
                         "3": {"hand": [17,18,20,21,22,23,24,26,28], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "13 16 19"}],
   "expect": {"offered": [{"seat": 1, "option": "13 14 15"}, {"seat": 1, "option": "13 16 19"}],
              "not_offered": [{"seat": 1, "option": "13 16"}, {"seat": 1, "option": "14 16"}],
              "players": {"1": {"card_count": 6, "last_action": "13 16 19"}},
              "game": {"pile_kind": "run", "pile_value": 19}}},

  {"name": "R2 a higher card number beats a single of the same rank", "rule": "R2", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,15,1,4,7,10,22,25,28], "card_count": 9},
                         "2": {"hand": [2,5,8,11,16,19,23,26,29], "card_count": 9},
                         "3": {"hand": [3,6,9,12,17,20,24,27,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "15"}],
   "expect": {"not_offered": [{"seat": 1, "option": "13"}],
              "players": {"1": {"card_count": 8, "last_action": "15"}},
              "game": {"pile_kind": "single", "pile_value": 15}}},

  {"name": "R3 runs and triples are offered when leading, other sets are not", "rule": "R3", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,11,12,20,25,28], "card_count": 9},
                         "2": {"hand": [2,5,8,13,16,19,22,26,29], "card_count": 9},
                         "3": {"hand": [3,6,9,14,17,21,23,27,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "10 11 12"}],
   "expect": {"offered": [{"seat": 1, "option": "1 4 7"}, {"seat": 1, "option": "10 11 12"}],
              "not_offered": [{"seat": 1, "option": "1 4 10"}, {"seat": 1, "option": "1 4 28"}, {"seat": 1, "option": "1 4"}],
              "players": {"1": {"card_count": 6, "last_action": "10 11 12"}},
              "game": {"pile_kind": "triple", "pile_value": 12}}},

  {"name": "R4 13 14 is a pair, 14 16 is not", "rule": "R4", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [13,14,16,1,5,9,21,26,30], "card_count": 9},
                         "2": {"hand": [2,4,7,10,17,19,22,25,28], "card_count": 9},
                         "3": {"hand": [3,6,8,11,12,18,20,23,29], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "13 14"}],
   "expect": {"offered": [{"seat": 1, "option": "13 14"}],
              "not_offered": [{"seat": 1, "option": "14 16"}],
              "players": {"1": {"card_count": 7, "last_action": "13 14"}},
              "game": {"pile_kind": "pair", "pile_value": 14}}},

  {"name": "R5 orbit increases by 1 each round", "rule": "R5", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,5,9,13,17,21,25,29,30], "card_count": 9},
                         "2": {"hand": [2,6,10,14,18,22,26,27,28], "card_count": 9},
                         "3": {"hand": [3,4,7,8,11,12,15,16,19], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "1"}],
   "expect": {"game": {"orbit": 6}, "players": {"1": {"card_count": 8}}}},

  {"name": "R6 first deal gives 9 cards each and 3 aside (chance: only counts asserted)", "rule": "R6", "players": 3, "rounds": 1, "default": "decline",
   "rules": [{"seat": 2, "options_include": "pass"}],
   "expect": {"game": {"deal_number": 1, "orbit": 1},
              "players": {"2": {"card_count": 9, "last_action": "pass"}, "3": {"card_count": 9, "last_action": "pass"}},
              "lens": {"game": {"aside": 3, "deck": 0}, "players": {"2": {"hand": 9}, "3": {"hand": 9}}}}},

  {"name": "R7 seat 2 leads deal 2 and seat 1 is skipped in its first orbit (chance: counts only)", "rule": "R7", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"penalty": 4, "deals_won": 1}, "2": {"penalty": 6}, "3": {"penalty": 9}},
             "game": {"deal_number": 1, "deal_active": false, "orbit": 10, "pile_kind": "empty", "pile_value": 0}},
   "rules": [{"seat": 3, "options_include": "pass"}],
   "expect": {"game": {"deal_number": 2, "orbit": 11},
              "not_offered": [{"seat": 1, "option": "pass"}],
              "players": {"1": {"card_count": 9}, "3": {"card_count": 9, "last_action": "pass"}},
              "lens": {"game": {"aside": 3}}}},

  {"name": "R8 in deal 3's first orbit seats 1 and 2 are skipped and seat 3 leads", "rule": "R8", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,13,16,19,22,25], "card_count": 9},
                         "2": {"hand": [2,5,8,11,14,17,20,23,26], "card_count": 9},
                         "3": {"hand": [3,6,9,12,15,18,21,24,27], "card_count": 9}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": true, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 3}},
   "rules": [{"seat": 3, "options_include": "3"}],
   "expect": {"game": {"deal_number": 3, "orbit": 21, "pile_kind": "single", "pile_value": 3},
              "not_offered": [{"seat": 1, "option": "1"}, {"seat": 2, "option": "2"}],
              "players": {"1": {"card_count": 9}, "2": {"card_count": 9}, "3": {"card_count": 8, "last_action": "3"}}}},

  {"name": "R9 the pile clears when play comes back to the last player", "rule": "R9", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,13], "card_count": 5},
                         "2": {"hand": [5,8,26], "card_count": 3},
                         "3": {"hand": [27,29,30], "card_count": 3}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 20, "last_player": 2}},
   "rules": [{"seat": 2, "options_include": "5"}],
   "expect": {"not_offered": [{"seat": 2, "option": "pass"}],
              "players": {"1": {"last_action": "pass", "card_count": 5}, "2": {"card_count": 2, "last_action": "5"}},
              "game": {"pile_kind": "single", "pile_value": 5}}},

  {"name": "R10 leading on an empty pile: pass is not offered", "rule": "R10", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [3,6,9,12,14,17,20,23,26], "card_count": 9},
                         "2": {"hand": [1,4,7,10,15,18,21,24,27], "card_count": 9},
                         "3": {"hand": [2,5,8,11,13,16,19,22,25], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "3"}],
   "expect": {"offered": [{"seat": 1, "option": "3"}, {"seat": 1, "option": "26"}],
              "not_offered": [{"seat": 1, "option": "pass"}],
              "players": {"1": {"card_count": 8, "last_action": "3"}},
              "game": {"pile_kind": "single", "pile_value": 3}}},

  {"name": "R11 on a single: pass, higher singles and any triple are offered", "rule": "R11", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [10,15,20,22,23,24,1,4,7], "card_count": 9},
                         "2": {"hand": [2,5,8,11,16,19,25,28,29], "card_count": 9},
                         "3": {"hand": [3,6,9,12,13,17,18,21,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "pass"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "15"}, {"seat": 1, "option": "20"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "10"}, {"seat": 1, "option": "22 23"}],
              "players": {"1": {"card_count": 9, "last_action": "pass"}}}},

  {"name": "R12 on a pair: pass, higher pairs and any triple are offered", "rule": "R12", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [10,11,15,16,17,22,23,24,1], "card_count": 9},
                         "2": {"hand": [2,4,7,12,18,19,25,28,29], "card_count": 9},
                         "3": {"hand": [3,5,6,8,9,20,21,26,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "pair", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "16 17"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "16 17"}, {"seat": 1, "option": "22 23"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "10 11"}, {"seat": 1, "option": "15"}],
              "players": {"1": {"card_count": 7, "last_action": "16 17"}},
              "game": {"pile_kind": "pair", "pile_value": 17}}},

  {"name": "R13 on a triple: only pass and higher triples", "rule": "R13", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [4,5,6,22,23,24,15,16,1], "card_count": 9},
                         "2": {"hand": [2,3,7,8,9,17,18,19,25], "card_count": 9},
                         "3": {"hand": [13,14,20,21,26,27,28,29,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "triple", "pile_value": 12, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "22 23 24"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "22 23 24"}],
              "not_offered": [{"seat": 1, "option": "4 5 6"}, {"seat": 1, "option": "15"}, {"seat": 1, "option": "1"}],
              "players": {"1": {"card_count": 6, "last_action": "22 23 24"}},
              "game": {"pile_kind": "triple", "pile_value": 24}}},

  {"name": "R14 on a run: only pass and higher runs", "rule": "R14", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [2,5,8,22,23,24,30], "card_count": 7},
                         "2": {"hand": [3,6,9,10,11,12,13,14,15], "card_count": 9},
                         "3": {"hand": [16,17,18,19,20,21,25,26,27], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "run", "pile_value": 7, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "2 5 8"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}, {"seat": 1, "option": "2 5 8"}],
              "not_offered": [{"seat": 1, "option": "22 23 24"}, {"seat": 1, "option": "30"}],
              "players": {"1": {"card_count": 4, "last_action": "2 5 8"}},
              "game": {"pile_kind": "run", "pile_value": 8}}},

  {"name": "R15 passing only sets last_action", "rule": "R15", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [25,1,4], "card_count": 3, "penalty": 2, "deals_won": 1},
                         "2": {"hand": [2,5,8,11], "card_count": 4},
                         "3": {"hand": [3,6,9,12,15], "card_count": 5}},
             "game": {"deal_number": 2, "deal_active": true, "leader_seat": 2, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 20, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "pass"}],
   "expect": {"offered": [{"seat": 1, "option": "25"}],
              "players": {"1": {"card_count": 3, "last_action": "pass", "penalty": 2, "deals_won": 1}}}},

  {"name": "R16 playing a pair removes 2 cards and records the play", "rule": "R16", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [16,17,2,5,8,11,26,27,29], "card_count": 9},
                         "2": {"hand": [1,4,7,10,13,19,22,25,28], "card_count": 9},
                         "3": {"hand": [3,6,9,12,14,15,18,20,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "16 17"}],
   "expect": {"players": {"1": {"card_count": 7, "last_action": "16 17"}},
              "game": {"pile_kind": "pair", "pile_value": 17}}},

  {"name": "R17 a triple bombs a single and the pile becomes a triple", "rule": "R17", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [1,2,3,22,23,24,10,13,26], "card_count": 9},
                         "2": {"hand": [4,5,7,8,11,16,19,25,28], "card_count": 9},
                         "3": {"hand": [6,9,12,17,18,20,21,29,30], "card_count": 9}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 14, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "22 23 24"}],
   "expect": {"offered": [{"seat": 1, "option": "1 2 3"}, {"seat": 1, "option": "22 23 24"}],
              "players": {"1": {"card_count": 6, "last_action": "22 23 24"}},
              "game": {"pile_kind": "triple", "pile_value": 24}}},

  {"name": "R18 emptying a hand wins the deal and skips the rest of the orbit", "rule": "R18", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1},
                         "2": {"hand": [1,2,4,5,7,8,10], "card_count": 7},
                         "3": {"hand": [28,3,6], "card_count": 3}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"not_offered": [{"seat": 2, "option": "pass"}, {"seat": 3, "option": "pass"}],
              "players": {"1": {"card_count": 0, "deals_won": 1, "penalty": 0},
                          "2": {"card_count": 7, "penalty": 14},
                          "3": {"card_count": 3, "penalty": 4}}}},

  {"name": "R19 penalty: 7 cards with card 30 adds 15, 6 cards with card 28 adds 7", "rule": "R19", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [29], "card_count": 1},
                         "2": {"hand": [1,4,7,10,13,16,30], "card_count": 7, "penalty": 3},
                         "3": {"hand": [28,2,5,8,11,14], "card_count": 6}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 5, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "29"}],
   "expect": {"players": {"1": {"penalty": 0, "deals_won": 1},
                          "2": {"penalty": 18},
                          "3": {"penalty": 7}}}},

  {"name": "R20 after the first orbit of deal 2, seat 1 gets its turn (chance: counts only)", "rule": "R20", "players": 3, "rounds": 2, "default": "decline",
   "given": {"game": {"deal_number": 1, "deal_active": false, "orbit": 10, "pile_kind": "empty", "pile_value": 0}},
   "rules": [{"seat": 1, "options_include": "pass"}],
   "expect": {"offered": [{"seat": 1, "option": "pass"}],
              "players": {"1": {"card_count": 9, "last_action": "pass"}},
              "game": {"deal_number": 2, "orbit": 12}}},

  {"name": "R21 orbit 40 ends an active deal and every seat is penalised", "rule": "R21", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [1,4,7,10,13,16,19], "card_count": 7},
                         "2": {"hand": [2,5,8], "card_count": 3},
                         "3": {"hand": [3,6,28,29], "card_count": 4}},
             "game": {"deal_number": 1, "deal_active": true, "leader_seat": 1, "first_orbit": false, "orbit": 39, "pile_kind": "single", "pile_value": 30, "last_player": 3}},
   "rules": [{"seat": 3, "options_include": "3"}],
   "expect": {"winner": 2,
              "standings": {"1": -140, "2": -30, "3": -50},
              "players": {"1": {"penalty": 14}, "2": {"penalty": 3}, "3": {"penalty": 5, "card_count": 3}},
              "game": {"orbit": 40, "deal_number": 1}}},

  {"name": "R22 the game ends when deal 3 is won", "rule": "R22", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 5, "deals_won": 1},
                         "2": {"hand": [1,2], "card_count": 2, "penalty": 2, "deals_won": 1},
                         "3": {"hand": [4], "card_count": 1, "penalty": 10, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": 2,
              "standings": {"1": -48, "2": -39, "3": -110},
              "players": {"1": {"penalty": 5, "deals_won": 2}, "2": {"penalty": 4}, "3": {"penalty": 11}},
              "game": {"deal_number": 3, "orbit": 21}}},

  {"name": "R23 tied lowest penalty and tied deals_won share the win", "rule": "R23", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 6, "deals_won": 0},
                         "2": {"hand": [1], "card_count": 1, "penalty": 5, "deals_won": 1},
                         "3": {"hand": [4], "card_count": 1, "penalty": 5, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": [1, 2],
              "standings": {"1": -59, "2": -59, "3": -60},
              "players": {"1": {"penalty": 6, "deals_won": 1}, "2": {"penalty": 6}, "3": {"penalty": 6}}}},

  {"name": "R23 tied lowest penalty is broken by more deals_won", "rule": "R23", "players": 3, "default": "decline",
   "given": {"players": {"1": {"hand": [30], "card_count": 1, "penalty": 6, "deals_won": 0},
                         "2": {"hand": [1], "card_count": 1, "penalty": 5, "deals_won": 2},
                         "3": {"hand": [4], "card_count": 1, "penalty": 5, "deals_won": 0}},
             "game": {"deal_number": 3, "deal_active": true, "leader_seat": 3, "first_orbit": false, "orbit": 20, "pile_kind": "empty", "pile_value": 0, "last_player": 1}},
   "rules": [{"seat": 1, "options_include": "30"}],
   "expect": {"winner": 2,
              "standings": {"1": -59, "2": -58, "3": -60},
              "players": {"1": {"penalty": 6, "deals_won": 1}, "2": {"penalty": 6, "deals_won": 2}, "3": {"penalty": 6}}}},

  {"name": "R24 a play is public: card_count, last_action and the pile change for all to see", "rule": "R24", "players": 3, "rounds": 1, "default": "decline",
   "given": {"players": {"1": {"hand": [25,1,4], "card_count": 3, "penalty": 2, "deals_won": 1},
                         "2": {"hand": [2,5,8,11], "card_count": 4},
                         "3": {"hand": [3,6,9,12,15], "card_count": 5}},
             "game": {"deal_number": 2, "deal_active": true, "leader_seat": 2, "first_orbit": false, "orbit": 5, "pile_kind": "single", "pile_value": 20, "last_player": 3}},
   "rules": [{"seat": 1, "options_include": "25"}],
   "expect": {"players": {"1": {"card_count": 2, "last_action": "25", "penalty": 2, "deals_won": 1},
                          "2": {"card_count": 4, "last_action": "pass"},
                          "3": {"card_count": 5, "last_action": "pass"}},
              "game": {"pile_kind": "single", "pile_value": 25, "deal_number": 2, "orbit": 6}}}
]
````
