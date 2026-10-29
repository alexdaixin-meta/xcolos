# 56 scenarios

- time: 2026-10-27T10:23:58+00:00 (110.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 3bd0e7d7c384781a, reply sha256 f2c38e28c868c56c

## Sent

````
SPEC:
{
  "name": "Lost Cities: Embargo",
  "summary": "Two players build ascending colour columns over two mirrored hands from one recorded shuffle. Each player secretly embargoes one opponent colour per hand, which halves a positive column score in that colour.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 30,
    "colours": 3,
    "lowest_number_card": 2,
    "highest_number_card": 10,
    "wagers_per_colour": 1,
    "hands": 2,
    "turns_per_hand": 20,
    "total_rounds": 40,
    "hand_size": 5,
    "draw_pile_size": 20,
    "column_offset": 8,
    "wager_multiplier": 1.5,
    "long_column_threshold": 5,
    "long_column_bonus": 10,
    "illegal_play_penalty": 1,
    "embargo_divisor": 2
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Ordered list of up to 5 card codes such as R5, G10 or BW (W = Wager). Slot 1 is the oldest card.",
        "observable": false
      },
      {
        "key": "red_col",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in this player's Red column, in play order",
        "observable": true
      },
      {
        "key": "green_col",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in this player's Green column, in play order",
        "observable": true
      },
      {
        "key": "blue_col",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in this player's Blue column, in play order",
        "observable": true
      },
      {
        "key": "embargo",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The colour this player embargoed against the opponent this hand. It is revealed in the end-of-hand announcement.",
        "observable": false
      },
      {
        "key": "penalty",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Illegal-play penalty points this hand (1 per illegal play), never announced",
        "observable": false
      },
      {
        "key": "hand_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Score of the last completed hand, set at end-of-hand scoring",
        "observable": true
      },
      {
        "key": "total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Match total. It changes only at end-of-hand scoring.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "match_order",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The recorded order of all 30 cards from the single shuffle in round 1",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Face-down draw pile, ordered; the first element is the top",
        "observable": false
      },
      {
        "key": "draw_count",
        "type": "number",
        "visible": "public",
        "initial": 20,
        "meaning": "Number of cards left in the draw pile",
        "observable": false
      },
      {
        "key": "red_pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Red discard pile; the last element is the top",
        "observable": false
      },
      {
        "key": "green_pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Green discard pile; the last element is the top",
        "observable": false
      },
      {
        "key": "blue_pile",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Blue discard pile; the last element is the top",
        "observable": false
      },
      {
        "key": "red_top",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Top card of the Red discard pile, or empty",
        "observable": false
      },
      {
        "key": "green_top",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Top card of the Green discard pile, or empty",
        "observable": false
      },
      {
        "key": "blue_top",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Top card of the Blue discard pile, or empty",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Round number, 1 to 40",
        "observable": false
      },
      {
        "key": "hand_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "1 for rounds 1-20, 2 for rounds 21-40",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat taking this round's turn. In hand 1: odd round gives seat 1, even round gives seat 2. In hand 2: odd round gives seat 2, even round gives seat 1.",
        "observable": false
      },
      {
        "key": "last_discard",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Card that went to a discard pile this turn (a voluntary discard or an illegal play), or empty",
        "observable": false
      },
      {
        "key": "announcements",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Turn announcements of the current hand, cleared at hand 2 setup",
        "observable": false
      }
    ]
  },
  "setup": [
    "The 30 cards are R2-R10, RW, G2-G10, GW, B2-B10 and BW.",
    "All totals start at 0. The round counter starts at 1.",
    "The shuffle, the deal and the embargoes happen as round steps guarded by round == 1 (and round == 21 for hand 2), so they belong to the script."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round == 1: draw all 30 cards at random into match_order. Seat 1 hand = match_order[1..5]. Seat 2 hand = match_order[6..10]. deck = match_order[11..30]. draw_count = 20."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round == 21: hand_number = 2. Clear red_col, green_col and blue_col for both seats. Clear red_pile, green_pile and blue_pile and their tops. Set penalty = 0 for both seats and clear announcements. Without reshuffling: Seat 2 hand = match_order[1..5], Seat 1 hand = match_order[6..10], deck = match_order[11..30], draw_count = 20."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "When round == 1 or round == 21: one of Red, Green, Blue",
      "effect": "embargo = the answer, kept secret (ally) until end-of-hand scoring."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Set active_seat: if hand_number == 1 then (1 if round is odd else 2), otherwise (2 if round is odd else 1). Set last_discard = ''."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each seat sees its own hand. Both see all columns, red_top, green_top, blue_top, draw_count and the announcements."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of 10 options: 'PLAY slot k (card)' or 'DISCARD slot k (card)' for k = 1..5",
      "effect": "Records the chosen slot and action."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "Remove the chosen card from hand. DISCARD: append it to its colour's pile, set that colour's top = card, last_discard = card. PLAY of a number card: legal if it is higher than every number in that colour's column, and then it is appended to the column. PLAY of a Wager: legal if the column holds no number card, and then it is appended to the column. An illegal PLAY goes to its colour's pile as a discard: top = card, last_discard = card, penalty += 1."
    },
    {
      "action": "ask",
      "who": "seat active_seat",
      "answer": "one of: draw pile, Red pile, Green pile, Blue pile",
      "effect": "Records the draw source."
    },
    {
      "action": "update",
      "who": "seat active_seat",
      "answer": null,
      "effect": "If a colour pile is chosen and it is non-empty and its top != last_discard: remove the top of that pile into hand slot 5 and reset that colour's top to the new top or ''. Otherwise remove deck[1] into hand slot 5 and set draw_count -= 1. The remaining cards close up to the left, so hand is ordered with the new card last."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Append to announcements and broadcast either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]' (illegal plays are also announced as discards), plus 'and drew from the draw pile' or 'and took [card] from the [colour] pile'. Penalties and totals are not announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == 20 or round == 40: score each column. An empty column scores 0. Otherwise S = (sum of number cards) - 8. If S > 0 and the column holds the Wager, S = floor(S * 1.5). If the column has >= 5 cards, S += 10. If the column's colour equals the opponent's embargo and S > 0, S = floor(S / 2). hand_score = the sum of the three column scores - penalty. total += hand_score."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round == 20 or round == 40: announce both seats' embargo, hand_score and total."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round += 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "End the game if round > 40, otherwise continue."
    }
  ],
  "ending": {
    "condition": "round > 40 (after hand 2 is scored)",
    "rank_by": "you.total",
    "decided_by": "Each player's match total after both hands. The higher total wins, and equal totals share the win (a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 30 cards: in each of Red, Green and Blue, the numbers 2 to 10 and one Wager."
    },
    {
      "id": "R2",
      "text": "In round 1 the deck is shuffled once into match_order. Seat 1 gets cards 1-5, Seat 2 gets cards 6-10, and cards 11-30 form the draw pile with card 11 on top (draw_count = 20)."
    },
    {
      "id": "R3",
      "text": "In round 21 all columns, discard piles and penalties are cleared and there is no reshuffle. Seat 2 gets match_order cards 1-5, Seat 1 gets cards 6-10, and cards 11-30 form the draw pile in the same order."
    },
    {
      "id": "R4",
      "text": "In rounds 1 and 21, both players simultaneously and secretly name an embargo colour (Red, Green or Blue), revealed only at end-of-hand scoring."
    },
    {
      "id": "R5",
      "text": "In hand 1, Seat 1 acts on odd rounds and Seat 2 on even rounds. In hand 2 (rounds 21-40), Seat 2 acts on odd rounds and Seat 1 on even rounds."
    },
    {
      "id": "R6",
      "text": "When a player discards a card, it goes onto its colour's discard pile at no cost."
    },
    {
      "id": "R7",
      "text": "When a player plays a number card higher than every number in that colour's column, it is added to the column."
    },
    {
      "id": "R8",
      "text": "When a player plays a number card not higher than every number in that colour's column, it goes onto its colour's discard pile and the player's penalty rises by 1."
    },
    {
      "id": "R9",
      "text": "When a player plays a Wager to a column with no number card, it is added to the column. If the column already has a number card, the play is illegal: the Wager is discarded and penalty rises by 1."
    },
    {
      "id": "R10",
      "text": "When a player draws from a discard pile that is empty, or whose top is the card that player sent to a discard pile this turn, they take the top card of the draw pile instead."
    },
    {
      "id": "R11",
      "text": "When a card is drawn it goes into hand slot 5, and the other cards close up so slot 1 stays the oldest."
    },
    {
      "id": "R12",
      "text": "Each turn's announcement says either 'Seat X played [card] to their [colour] column' or 'Seat X discarded [card]', never distinguishing an illegal play from a voluntary discard. It also gives the pile drawn from, and the card taken if it came from a discard pile."
    },
    {
      "id": "R13",
      "text": "When a hand is scored, an empty column scores 0. Otherwise S = sum of number cards - 8; for example R4, R9 gives 5."
    },
    {
      "id": "R14",
      "text": "When a column with S > 0 holds the Wager, S becomes floor(1.5 * S); for example S = 5 becomes 7. When S <= 0 the Wager has no effect."
    },
    {
      "id": "R15",
      "text": "When a column has 5 or more cards, Wager included, it gains +10."
    },
    {
      "id": "R16",
      "text": "When a column's colour is the opponent's embargo and its score so far is positive, it is halved rounding down (for example 17 becomes 8). A zero or negative score is unchanged."
    },
    {
      "id": "R17",
      "text": "Hand score = the sum of the three column scores - illegal-play penalties that hand. It is added to total, then both embargoes, hand scores and totals are announced."
    },
    {
      "id": "R18",
      "text": "After round 40 is scored the match ends. The higher total wins, and equal totals are a draw."
    }
  ],
  "offers": [
    {
      "question": "Embargo colour (rounds 1 and 21)",
      "who": "both seats",
      "options": "Red, Green, Blue"
    },
    {
      "question": "Card and action",
      "who": "active seat",
      "options": "PLAY or DISCARD for each of the 5 hand slots (10 options), each labelled with its card; illegal plays are offered because they are allowed at a penalty"
    },
    {
      "question": "Draw source",
      "who": "active seat",
      "options": "draw pile, Red pile, Green pile, Blue pile (an empty pile, or one topped by this turn's discard, falls back to the draw pile)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players",
      "why": "The designer fixed 2. The embargo and the mirrored hand swap are built around one opponent."
    },
    {
      "what": "No talk step",
      "why": "The source has no communication. With 2 players, free talk would only add cheap bluffing that the rules do not include."
    },
    {
      "what": "An illegal play counts as 'the card discarded this turn' for the draw fallback",
      "why": "The illegal card lands on the discard pile this turn exactly like a discard, and the announcement calls it a discard."
    },
    {
      "what": "Card codes R2..R10, RW and so on",
      "why": "Gives text tokens for list operations and arithmetic on the number part."
    }
  ],
  "simplifications": [
    {
      "what": "Slot and PLAY/DISCARD are combined into one 10-option choice",
      "why": "The engine takes one answer per question, and this keeps the two parts together."
    },
    {
      "what": "Discard piles are hidden lists with public top-card attributes",
      "why": "Only the top card is visible and takeable in the source."
    },
    {
      "what": "Hand setups and scoring are steps guarded by round == 1, 21, 20 and 40",
      "why": "The step list is flat. Single-step `when` conditions express the two hands without separate blocks."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: red_col, green_col, blue_col, hand_score, total; table: none.
````

## Reply

````
```json
[
  {
    "name": "R1: the recorded shuffle holds all 30 cards",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "rules": [],
    "expect": {
      "lens": {"game": {"match_order": 30}}
    }
  },
  {
    "name": "R2: round 1 deals 5 cards to each seat and leaves 20 in the draw pile (19 after seat 1 draws); chance-independent counts only",
    "rule": "R2",
    "players": 2,
    "seed": 3,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "lens": {"game": {"match_order": 30, "deck": 19}, "players": {"1": {"hand": 5}, "2": {"hand": 5}}}
    }
  },
  {
    "name": "R3: round 21 clears the columns, deals the mirrored hands from match_order and does not reshuffle",
    "rule": "R3",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "first",
    "given": {
      "players": {
        "1": {"red_col": ["R5"], "green_col": ["G4", "G7"], "blue_col": [], "total": 30, "hand": ["B2"]},
        "2": {"red_col": [], "green_col": [], "blue_col": ["B3", "B6"], "total": 12, "hand": ["G2"]}
      },
      "game": {
        "round": 21,
        "hand_number": 1,
        "match_order": ["R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "RW", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "GW", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "BW"],
        "deck": [],
        "draw_count": 0
      }
    },
    "rules": [
      {"seat": 2, "options_include": "PLAY slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {
        "1": {"red_col": [], "green_col": [], "blue_col": [], "total": 30},
        "2": {"red_col": ["R2"], "green_col": [], "blue_col": [], "total": 12}
      },
      "lens": {"game": {"deck": 19}, "players": {"1": {"hand": 5}, "2": {"hand": 5}}},
      "offered": [{"seat": 1, "option": "Red"}]
    }
  },
  {
    "name": "R4: in round 1 both seats are asked for an embargo colour",
    "rule": "R4",
    "players": 2,
    "seed": 2,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": "Green"},
      {"seat": 2, "options_include": "Blue"}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": "Green"},
        {"seat": 1, "option": "Blue"},
        {"seat": 2, "option": "Red"},
        {"seat": 2, "option": "Blue"}
      ]
    }
  },
  {
    "name": "R5: in hand 2, seat 1 acts on even round 22 and seat 2 does not",
    "rule": "R5",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 22, "hand_number": 2, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 1 (R5)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": ["R5"]}, "2": {"red_col": [], "green_col": [], "blue_col": []}},
      "not_offered": [{"seat": 2, "option": "draw pile"}]
    }
  },
  {
    "name": "R5: in hand 1, seat 2 acts on even round 4 and seat 1 does not",
    "rule": "R5",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 4, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "PLAY slot 3 (B2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"2": {"blue_col": ["B2"]}, "1": {"red_col": [], "green_col": [], "blue_col": []}},
      "not_offered": [{"seat": 1, "option": "draw pile"}]
    }
  },
  {
    "name": "R6: a discard goes onto its colour's pile at no cost",
    "rule": "R6",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 2 (G3)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": [], "green_col": [], "blue_col": [], "total": 0}},
      "lens": {"game": {"green_pile": 1, "deck": 4}, "players": {"1": {"hand": 5}}}
    }
  },
  {
    "name": "R7: a higher number card is added to the column",
    "rule": "R7",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R3"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 1 (R5)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": ["R3", "R5"]}},
      "lens": {"game": {"red_pile": 0}}
    }
  },
  {
    "name": "R8: a lower number play is discarded and costs 1 point at scoring",
    "rule": "R8",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "embargo": "Blue", "penalty": 0, "total": 0},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "red_col": ["R8"], "embargo": "Blue", "penalty": 0, "total": 0}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "PLAY slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {
        "2": {"red_col": ["R8"], "hand_score": -1, "total": -1},
        "1": {"hand_score": 0, "total": 0}
      },
      "lens": {"game": {"red_pile": 1}}
    }
  },
  {
    "name": "R9: a Wager played to a column with no number card is added",
    "rule": "R9",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 4 (RW)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": ["RW"]}}
    }
  },
  {
    "name": "R9: a Wager played to a column that has a number card is discarded",
    "rule": "R9",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R3"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 4 (RW)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": ["R3"]}},
      "lens": {"game": {"red_pile": 1}}
    }
  },
  {
    "name": "R10: drawing from an empty pile takes from the draw pile",
    "rule": "R10",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 2 (G3)"},
      {"seat": 1, "options_include": "Blue pile"}
    ],
    "expect": {
      "lens": {"game": {"deck": 4, "blue_pile": 0, "green_pile": 1}, "players": {"1": {"hand": 5}}}
    }
  },
  {
    "name": "R10: drawing from the pile topped by this turn's discard takes from the draw pile",
    "rule": "R10",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 2 (G3)"},
      {"seat": 1, "options_include": "Green pile"}
    ],
    "expect": {
      "lens": {"game": {"deck": 4, "green_pile": 1}, "players": {"1": {"hand": 5}}}
    }
  },
  {
    "name": "R10: drawing from a non-empty pile topped by an older card takes that card",
    "rule": "R10",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5, "green_pile": ["G6"], "green_top": "G6"}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 3 (B4)"},
      {"seat": 1, "options_include": "Green pile"}
    ],
    "expect": {
      "lens": {"game": {"deck": 5, "green_pile": 0, "blue_pile": 1}, "players": {"1": {"hand": 5}}}
    }
  },
  {
    "name": "R11: the drawn card goes to slot 5 and is offered there next turn",
    "rule": "R11",
    "players": 2,
    "seed": 1,
    "rounds": 3,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 1 (R5)"},
      {"seat": 1, "options_include": "PLAY slot 5 (R8)"},
      {"seat": 1, "options_include": "draw pile", "times": 2},
      {"seat": 2, "options_include": "DISCARD slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"red_col": ["R5", "R8"]}},
      "offered": [
        {"seat": 1, "option": "DISCARD slot 1 (G3)"},
        {"seat": 1, "option": "DISCARD slot 4 (G9)"}
      ]
    }
  },
  {
    "name": "R12: each turn adds one announcement",
    "rule": "R12",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"]},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"]}
      },
      "game": {"round": 3, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5, "announcements": []}
    },
    "rules": [
      {"seat": 1, "options_include": "PLAY slot 1 (R5)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "lens": {"game": {"announcements": 1}}
    }
  },
  {
    "name": "R13: a column of R4, R9 scores 5 and empty columns score 0",
    "rule": "R13",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R4", "R9"], "embargo": "Green", "penalty": 0, "total": 0},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "embargo": "Green", "penalty": 0, "total": 0}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "DISCARD slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"hand_score": 5, "total": 5}, "2": {"hand_score": 0, "total": 0}}
    }
  },
  {
    "name": "R14: a Wager multiplies a positive score (5 becomes 7) and leaves a negative one unchanged",
    "rule": "R14",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["RW", "R4", "R9"], "green_col": ["GW", "G3"], "embargo": "Blue", "penalty": 0, "total": 0},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "embargo": "Blue", "penalty": 0, "total": 0}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "DISCARD slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"hand_score": 2, "total": 2}}
    }
  },
  {
    "name": "R15: a column of 5 or more cards, Wager included, gains 10",
    "rule": "R15",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "blue_col": ["BW", "B2", "B3", "B4", "B5"], "green_col": ["G2", "G3", "G4", "G5", "G6"], "embargo": "Red", "penalty": 0, "total": 0},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "embargo": "Red", "penalty": 0, "total": 0}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "DISCARD slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"hand_score": 41, "total": 41}}
    }
  },
  {
    "name": "R16: the opponent's embargo halves a positive score (17 becomes 8) and leaves a negative one unchanged",
    "rule": "R16",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R7", "R8", "R10"], "green_col": ["G9"], "embargo": "Green", "penalty": 0, "total": 0},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "green_col": ["G3"], "embargo": "Red", "penalty": 0, "total": 0}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "DISCARD slot 5 (B9)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"hand_score": 9, "total": 9}, "2": {"hand_score": -5, "total": -5}}
    }
  },
  {
    "name": "R17: hand score subtracts penalties and is added to the total",
    "rule": "R17",
    "players": 2,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R9", "R10"], "embargo": "Green", "penalty": 2, "total": 20},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "embargo": "Blue", "penalty": 0, "total": 15}
      },
      "game": {"round": 20, "hand_number": 1, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 2, "options_include": "DISCARD slot 1 (R2)"},
      {"seat": 2, "options_include": "draw pile"}
    ],
    "expect": {
      "players": {"1": {"hand_score": 9, "total": 29}, "2": {"hand_score": 0, "total": 15}}
    }
  },
  {
    "name": "R18: after round 40 is scored the higher total wins",
    "rule": "R18",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R10"], "embargo": "Green", "penalty": 0, "total": 10},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "blue_col": ["B9"], "embargo": "Green", "penalty": 0, "total": 5}
      },
      "game": {"round": 40, "hand_number": 2, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 2 (G3)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "winner": 1,
      "standings": {"1": 12, "2": 6},
      "players": {"1": {"hand_score": 2, "total": 12}, "2": {"hand_score": 1, "total": 6}}
    }
  },
  {
    "name": "R18: equal totals after round 40 share the win",
    "rule": "R18",
    "players": 2,
    "seed": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"hand": ["R5", "G3", "B4", "RW", "G9"], "red_col": ["R10"], "embargo": "Green", "penalty": 0, "total": 5},
        "2": {"hand": ["R2", "G2", "B2", "BW", "B9"], "blue_col": ["B9"], "embargo": "Green", "penalty": 0, "total": 6}
      },
      "game": {"round": 40, "hand_number": 2, "deck": ["R8", "G8", "B8", "R10", "G10"], "draw_count": 5}
    },
    "rules": [
      {"seat": 1, "options_include": "DISCARD slot 2 (G3)"},
      {"seat": 1, "options_include": "draw pile"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 7, "2": 7},
      "players": {"1": {"total": 7}, "2": {"total": 7}}
    }
  }
]
```
````
