# 17 scenarios

- time: 2026-10-28T02:01:55+00:00 (65.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 78da9e953a1a42b3, reply sha256 b977a919699ca5af

## Sent

````
SPEC:
{
  "name": "Greek Hold 'em Mini II",
  "summary": "Three players play 36 hands of a tiny one-bet poker with an 18-card suitless deck; the highest net chip total after hand 36 wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "num_players": 3,
    "ranks": 6,
    "copies_per_rank": 3,
    "deck_size": 18,
    "hands": 36,
    "hole_cards": 2,
    "board_cards": 4,
    "board_face_up_before_betting": 3,
    "ante": 1,
    "starting_pot": 3,
    "bet_small": 2,
    "bet_large": 4,
    "pair_bonus": 6,
    "match_bonus": 4,
    "max_matches": 3,
    "starting_total": 0
  },
  "attributes": {
    "player": [
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Net chip total across all hands. It may be negative or fractional.",
        "observable": true
      },
      {
        "key": "hole",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The player's 2 hole cards for this hand. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "revealed_hole",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Hole cards shown at a showdown with 2 or more players. Empty otherwise.",
        "observable": true
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This hand's score: a+b, plus 6 if a pair, plus 4 per matching board card, with at most 3 matches.",
        "observable": false
      },
      {
        "key": "revealed_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "hand_score, published at a showdown for players still in. 0 otherwise.",
        "observable": true
      },
      {
        "key": "action",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The player's last announced action this hand: CHECK, BET, CALL or FOLD.",
        "observable": true
      },
      {
        "key": "folded",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the player has folded this hand.",
        "observable": true
      },
      {
        "key": "paid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips paid into the pot this hand.",
        "observable": false
      },
      {
        "key": "won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips won from the pot this hand.",
        "observable": false
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
          2,
          2,
          2,
          3,
          3,
          3,
          4,
          4,
          4,
          5,
          5,
          5,
          6,
          6,
          6
        ],
        "meaning": "The undealt cards.",
        "observable": false
      },
      {
        "key": "board_up",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up board cards: 3 during betting, 4 after the final board.",
        "observable": true
      },
      {
        "key": "board_hidden",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Board card 4 while it is still face down.",
        "observable": false
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips in the pot this hand.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The current hand number, from 1 to 36.",
        "observable": true
      },
      {
        "key": "first_actor",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat ((hand-1) mod 3)+1.",
        "observable": false
      },
      {
        "key": "second_actor",
        "type": "number",
        "visible": "public",
        "initial": 2,
        "meaning": "The seat after the first actor, wrapping from 3 to 1.",
        "observable": false
      },
      {
        "key": "third_actor",
        "type": "number",
        "visible": "public",
        "initial": 3,
        "meaning": "The remaining seat.",
        "observable": false
      },
      {
        "key": "bet_amount",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The size of this hand's single bet (2 or 4). 0 if nobody has bet.",
        "observable": true
      },
      {
        "key": "in_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players who have not folded.",
        "observable": false
      },
      {
        "key": "best_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest hand_score among players still in.",
        "observable": false
      },
      {
        "key": "winner_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of players still in who hold best_score.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each start with a total of 0.",
    "The table's deck holds 18 cards: ranks 1 to 6, three copies of each, with no suits.",
    "The hand counter starts at 0. The game lasts exactly 36 hands."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Increment hand by 1. Set first_actor = ((hand-1) mod 3)+1, second_actor = (first_actor mod 3)+1, and third_actor = (second_actor mod 3)+1. Return all cards to deck, so it again holds the 18 cards. For every player: clear hole and revealed_hole, set hand_score and revealed_score to 0, set action to empty, set folded to false, and set paid and won to 0. Clear board_up and board_hidden. Set bet_amount to 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal: draw 2 random cards from deck into each player's hole. Draw 3 random cards from deck into board_up and 1 into board_hidden."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Ante: each player's paid += 1, so pot = 3."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hole, the 3 cards of board_up, the pot, the hand number and who acts first, second and third."
    },
    {
      "action": "ask",
      "who": "the first actor (seat first_actor)",
      "answer": "one of CHECK, BET 2, BET 4",
      "effect": "On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. The choice is announced to all."
    },
    {
      "action": "ask",
      "who": "the second actor (seat second_actor)",
      "answer": "if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD",
      "effect": "On CHECK: action = CHECK. On BET x: action = BET, bet_amount = x, paid += x, pot += x. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true. The choice is announced to all."
    },
    {
      "action": "ask",
      "who": "the third actor (seat third_actor)",
      "answer": "if bet_amount = 0: CHECK, BET 2 or BET 4; if bet_amount > 0: CALL or FOLD",
      "effect": "Same effects as the second actor's step. The choice is announced to all."
    },
    {
      "action": "poll",
      "who": "every player whose action = CHECK, only when bet_amount > 0 (these players checked before the bet)",
      "answer": "CALL or FOLD",
      "effect": "Answers are collected simultaneously, then revealed. On CALL: action = CALL, paid += bet_amount, pot += bet_amount. On FOLD: action = FOLD, folded = true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Final board: move the card in board_hidden into board_up, so board_up holds 4 cards."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player with hole ranks a and b: matches = the number of cards in board_up whose rank equals a or b. hand_score = a + b + (6 if a = b else 0) + 4 * min(3, matches)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set in_count = the number of players with folded = false. If in_count = 1, the unfolded player gets won = pot. If in_count >= 2: for each unfolded player, revealed_hole = hole and revealed_score = hand_score; best_score = the maximum hand_score among unfolded players; winner_count = the number of unfolded players with hand_score = best_score; each such player gets won = pot / winner_count. Folded players' hole cards are never revealed."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Totals: each player's total += won - paid. All three totals, the showdown result and the pot split are announced."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If hand >= 36, end the game. Otherwise play the next hand."
    }
  ],
  "ending": {
    "condition": "hand >= 36",
    "rank_by": "you.total",
    "decided_by": "Each player's standing is their net chip total after 36 hands. The highest total wins, and players tied at the top share the win (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When a hand begins, then the deck holds all 18 cards (ranks 1-6, three of each), each player receives 2 hole cards and the board receives 4 cards, all drawn at random."
    },
    {
      "id": "R2",
      "text": "When a hand begins, then each player pays an ante of 1 and the pot is 3."
    },
    {
      "id": "R3",
      "text": "When betting starts, then 3 board cards are face up and board card 4 is hidden from everyone."
    },
    {
      "id": "R4",
      "text": "When it is hand h, then the first actor is seat ((h-1) mod 3)+1, the second actor is the next seat (wrapping from 3 to 1), and the third actor is the remaining seat."
    },
    {
      "id": "R5",
      "text": "When no bet has been made and a player acts, then they may CHECK, BET 2 or BET 4, and a bet adds that amount to their paid and to the pot."
    },
    {
      "id": "R6",
      "text": "When a bet has been made and a later actor acts, then they may only CALL (pay the bet amount into the pot) or FOLD."
    },
    {
      "id": "R7",
      "text": "When a bet is made after one or more players checked, then those checkers choose CALL or FOLD simultaneously, and the choices are revealed afterwards."
    },
    {
      "id": "R8",
      "text": "When a hand has a bet, then there is exactly one bet: there are no raises and the bettor never acts again."
    },
    {
      "id": "R9",
      "text": "When a player folds, then they leave the hand, forfeit everything they paid, and their hole cards are never revealed."
    },
    {
      "id": "R10",
      "text": "When betting ends, then board card 4 is turned face up."
    },
    {
      "id": "R11",
      "text": "When hole cards are ranks a and b, then the hand score is a + b, plus 6 if a = b, plus 4 for each board card whose rank equals a or b, counting at most 3 matches."
    },
    {
      "id": "R12",
      "text": "When exactly one player has not folded, then that player takes the whole pot and no hole cards are revealed."
    },
    {
      "id": "R13",
      "text": "When two or three players have not folded, then their hole cards and scores are revealed and the highest score takes the pot."
    },
    {
      "id": "R14",
      "text": "When players at showdown tie for the highest score, then they split the pot equally, which may give fractional totals."
    },
    {
      "id": "R15",
      "text": "When all three players check, then all three go to showdown with a pot of 3."
    },
    {
      "id": "R16",
      "text": "When a hand ends, then each player's total changes by the chips won minus the chips paid, all three totals are announced, and the totals sum to 0."
    },
    {
      "id": "R17",
      "text": "When hand 36 ends, then the game ends and the highest total wins, with tied leaders sharing the win."
    }
  ],
  "offers": [
    {
      "question": "First actor's choice",
      "who": "seat first_actor",
      "options": "CHECK, BET 2, BET 4"
    },
    {
      "question": "Second actor's choice",
      "who": "seat second_actor",
      "options": "if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD"
    },
    {
      "question": "Third actor's choice",
      "who": "seat third_actor",
      "options": "if bet_amount = 0: CHECK, BET 2, BET 4; if bet_amount > 0: CALL, FOLD"
    },
    {
      "question": "Response to a bet made after a check",
      "who": "every seat whose action is CHECK while bet_amount > 0; other seats are not asked",
      "options": "CALL, FOLD"
    }
  ],
  "choices": [
    {
      "what": "3 players (min = max = suggested = 3)",
      "why": "The designer fixes the game at three seats. The actor rotation, the response step and the split pots all assume exactly three players. With three, bluffing works because a bet must get past two opponents, one of whom may hold the third copy of a rank."
    },
    {
      "what": "No pre-choice talk step",
      "why": "The source has no table talk. The information in play is the actions themselves (check, bet size, call or fold), so adding talk would add a mechanic."
    },
    {
      "what": "Responders are identified by action = CHECK while bet_amount > 0",
      "why": "Anyone still showing CHECK once a bet exists must have checked before the bet. Since only one bet is possible, this matches 'each player who checked before the bet'."
    },
    {
      "what": "Score computed for everyone, but published only at a showdown with 2 or more players",
      "why": "This keeps the arithmetic uniform while honoring the rule that folded hands and uncontested winners' hands are never revealed."
    },
    {
      "what": "Strategy at this table",
      "why": "A thoughtful player weighs the visible board against their hole cards, bets 4 with strong pairs or matches, uses bet size and position to bluff, and reads opponents' checks and calls over 36 hands. A thoughtless player calls or bets blindly."
    }
  ],
  "simplifications": [
    {
      "what": "Ante, bets and calls are tracked in `paid`, and the net change is applied to `total` at the end of the hand",
      "why": "This is arithmetically the same as paying at once, and it keeps fractional split pots exact."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total, revealed_hole, revealed_score, action, folded; table: board_up, pot, hand, bet_amount.
````

## Reply

````
```json
[
  {
    "name": "R1: a hand is dealt; chance only decides ranks, so assert the 4-card board and the 2-card reveals after an all-check showdown",
    "rule": "R1", "players": 3, "rounds": 1, "seed": 1, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "CHECK"},
      {"seat": 3, "options_include": "CHECK"}
    ],
    "expect": {
      "game": {"hand": 1},
      "lens": {"game": {"board_up": 4}, "players": {"1": {"revealed_hole": 2}, "2": {"revealed_hole": 2}, "3": {"revealed_hole": 2}}}
    }
  },
  {
    "name": "R2: ante of 1 each makes pot 3; bet 4 and two folds give +2/-1/-1",
    "rule": "R2", "players": 3, "rounds": 1, "seed": 2, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 4"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {"1": {"total": 2}, "2": {"total": -1, "folded": true}, "3": {"total": -1, "folded": true}},
      "game": {"pot": 7, "bet_amount": 4}
    }
  },
  {
    "name": "R3: betting happens over 3 visible board cards, and the board shows 4 after the hand (card values are random)",
    "rule": "R3", "players": 3, "rounds": 1, "seed": 3, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "CHECK"},
      {"seat": 3, "options_include": "CHECK"}
    ],
    "expect": {
      "players": {"1": {"action": "CHECK"}, "2": {"action": "CHECK"}, "3": {"action": "CHECK"}},
      "lens": {"game": {"board_up": 4}}
    }
  },
  {
    "name": "R4: in hand 2 seat 2 acts first, then seat 3, then seat 1",
    "rule": "R4", "players": 3, "rounds": 1, "seed": 4, "default": "decline",
    "given": {"game": {"hand": 1}},
    "rules": [
      {"seat": 2, "options_include": "BET 2"},
      {"seat": 3, "options_include": "FOLD"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"hand": 2, "pot": 5, "bet_amount": 2},
      "players": {"1": {"total": -1, "folded": true}, "2": {"total": 2, "action": "BET"}, "3": {"total": -1, "folded": true}},
      "not_offered": [{"seat": 1, "option": "CHECK"}, {"seat": 3, "option": "CHECK"}]
    }
  },
  {
    "name": "R4: in hand 3 seat 3 acts first",
    "rule": "R4", "players": 3, "rounds": 1, "seed": 5, "default": "decline",
    "given": {"game": {"hand": 2}},
    "rules": [
      {"seat": 3, "options_include": "BET 4"},
      {"seat": 1, "options_include": "FOLD"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"hand": 3, "pot": 7},
      "players": {"1": {"total": -1}, "2": {"total": -1}, "3": {"total": 2}},
      "not_offered": [{"seat": 1, "option": "CHECK"}, {"seat": 2, "option": "CHECK"}]
    }
  },
  {
    "name": "R5: a BET 2 adds 2 to the pot",
    "rule": "R5", "players": 3, "rounds": 1, "seed": 6, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 2"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"pot": 5, "bet_amount": 2},
      "players": {"1": {"total": 2, "action": "BET"}, "2": {"total": -1}, "3": {"total": -1}},
      "offered": [{"seat": 1, "option": "CHECK"}, {"seat": 1, "option": "BET 4"}]
    }
  },
  {
    "name": "R6: after a bet, later actors may only CALL or FOLD (showdown result is random)",
    "rule": "R6", "players": 3, "rounds": 1, "seed": 7, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 4"},
      {"seat": 2, "options_include": "CALL"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"pot": 11, "bet_amount": 4},
      "players": {"2": {"action": "CALL"}, "3": {"total": -1, "action": "FOLD", "folded": true}},
      "offered": [{"seat": 3, "option": "CALL"}, {"seat": 2, "option": "FOLD"}],
      "not_offered": [{"seat": 2, "option": "CHECK"}, {"seat": 2, "option": "BET 2"}, {"seat": 3, "option": "CHECK"}, {"seat": 3, "option": "BET 4"}]
    }
  },
  {
    "name": "R7: earlier checkers answer CALL or FOLD to a later bet",
    "rule": "R7", "players": 3, "rounds": 1, "seed": 8, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "CHECK"},
      {"seat": 3, "options_include": "BET 2"},
      {"seat": 1, "options_include": "FOLD"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"pot": 5, "bet_amount": 2},
      "players": {"1": {"total": -1, "action": "FOLD"}, "2": {"total": -1, "action": "FOLD"}, "3": {"total": 2, "action": "BET"}},
      "offered": [{"seat": 1, "option": "CALL"}, {"seat": 2, "option": "CALL"}]
    }
  },
  {
    "name": "R8: only one bet; the bettor never acts again (showdown is random)",
    "rule": "R8", "players": 3, "rounds": 1, "seed": 9, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 2"},
      {"seat": 2, "options_include": "CALL"},
      {"seat": 3, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"pot": 9, "bet_amount": 2},
      "players": {"1": {"action": "BET"}, "2": {"action": "CALL"}, "3": {"action": "CALL"}},
      "not_offered": [{"seat": 1, "option": "CALL"}, {"seat": 1, "option": "FOLD"}, {"seat": 2, "option": "BET 4"}, {"seat": 3, "option": "BET 4"}]
    }
  },
  {
    "name": "R9: a folder loses the ante and its hole cards stay hidden",
    "rule": "R9", "players": 3, "rounds": 1, "seed": 10, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 4"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "CALL"}
    ],
    "expect": {
      "game": {"pot": 11},
      "players": {"2": {"total": -1, "folded": true, "action": "FOLD", "revealed_hole": [], "revealed_score": 0}},
      "lens": {"players": {"1": {"revealed_hole": 2}, "2": {"revealed_hole": 0}, "3": {"revealed_hole": 2}}}
    }
  },
  {
    "name": "R10: board card 4 is face up after betting",
    "rule": "R10", "players": 3, "rounds": 1, "seed": 11, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 2"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {"lens": {"game": {"board_up": 4}}}
  },
  {
    "name": "R11: scores come from random cards; only assert that showdown hands are published",
    "rule": "R11", "players": 3, "rounds": 1, "seed": 12, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "CHECK"},
      {"seat": 3, "options_include": "CHECK"}
    ],
    "expect": {"lens": {"players": {"1": {"revealed_hole": 2}, "2": {"revealed_hole": 2}, "3": {"revealed_hole": 2}}, "game": {"board_up": 4}}}
  },
  {
    "name": "R12: an uncontested winner takes the pot unrevealed",
    "rule": "R12", "players": 3, "rounds": 1, "seed": 13, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 2"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {
      "players": {"1": {"total": 2, "revealed_hole": [], "revealed_score": 0}, "2": {"total": -1, "revealed_hole": []}, "3": {"total": -1, "revealed_hole": []}}
    }
  },
  {
    "name": "R13: a two-player showdown reveals both hands (winner is random)",
    "rule": "R13", "players": 3, "rounds": 1, "seed": 14, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "BET 2"},
      {"seat": 2, "options_include": "CALL"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"pot": 7},
      "players": {"3": {"total": -1, "revealed_hole": []}},
      "lens": {"players": {"1": {"revealed_hole": 2}, "2": {"revealed_hole": 2}, "3": {"revealed_hole": 0}}}
    }
  },
  {
    "name": "R14: ties are random; only the folder's loss is fixed in a contested pot",
    "rule": "R14", "players": 3, "rounds": 1, "seed": 15, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "BET 4"},
      {"seat": 3, "options_include": "CALL"},
      {"seat": 1, "options_include": "FOLD"}
    ],
    "expect": {
      "game": {"pot": 11},
      "players": {"1": {"total": -1, "folded": true}},
      "lens": {"players": {"2": {"revealed_hole": 2}, "3": {"revealed_hole": 2}}}
    }
  },
  {
    "name": "R15: three checks go to showdown with pot 3 and no response step",
    "rule": "R15", "players": 3, "rounds": 1, "seed": 16, "default": "decline",
    "rules": [
      {"seat": 1, "options_include": "CHECK"},
      {"seat": 2, "options_include": "CHECK"},
      {"seat": 3, "options_include": "CHECK"}
    ],
    "expect": {
      "game": {"pot": 3, "bet_amount": 0},
      "players": {"1": {"action": "CHECK", "folded": false}, "2": {"action": "CHECK", "folded": false}, "3": {"action": "CHECK", "folded": false}},
      "not_offered": [{"seat": 1, "option": "CALL"}, {"seat": 2, "option": "CALL"}, {"seat": 3, "option": "CALL"}],
      "lens": {"players": {"1": {"revealed_hole": 2}, "2": {"revealed_hole": 2}, "3": {"revealed_hole": 2}}}
    }
  },
  {
    "name": "R16: totals change by won minus paid from prior fractional totals",
    "rule": "R16", "players": 3, "rounds": 1, "seed": 17, "default": "decline",
    "given": {"players": {"1": {"total": 5}, "2": {"total": -2.5}, "3": {"total": -2.5}}},
    "rules": [
      {"seat": 1, "options_include": "BET 4"},
      {"seat": 2, "options_include": "FOLD"},
      {"seat": 3, "options_include": "FOLD"}
    ],
    "expect": {"players": {"1": {"total": 7}, "2": {"total": -3.5}, "3": {"total": -3.5}}}
  },
  {
    "name": "R17: after hand 36 the highest total wins",
    "rule": "R17", "players": 3, "seed": 18, "default": "decline",
    "given": {"game": {"hand": 35}, "players": {"1": {"total": 10}, "2": {"total": -5}, "3": {"total": -5}}},
    "rules": [
      {"seat": 3, "options_include": "BET 2"},
      {"seat": 1, "options_include": "FOLD"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 9, "2": -6, "3": -3},
      "game": {"hand": 36}
    }
  },
  {
    "name": "R17: tied leaders after hand 36 share the win",
    "rule": "R17", "players": 3, "seed": 19, "default": "decline",
    "given": {"game": {"hand": 35}, "players": {"1": {"total": 2}, "2": {"total": -1}, "3": {"total": -1}}},
    "rules": [
      {"seat": 3, "options_include": "BET 2"},
      {"seat": 1, "options_include": "FOLD"},
      {"seat": 2, "options_include": "FOLD"}
    ],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 1, "2": -2, "3": 1}
    }
  }
]
```
````
