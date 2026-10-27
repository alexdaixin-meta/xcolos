# 12 scenarios

- time: 2026-10-27T18:02:32+00:00 (107.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 9ec0f23efa049cf2, reply sha256 61a5f22a0439704b

## Sent

````
SPEC:
{
  "name": "Tides of Madness: Obsession",
  "summary": "A two-player card draft over 3 tides of 5 rounds: pick a card, swap hands, score suit sets doubled for a secret Obsession suit, and avoid reaching 9 madness.",
  "players": {
    "min": 2,
    "max": 2,
    "suggested": 2
  },
  "parameters": {
    "deck_size": 30,
    "suits": 5,
    "cards_per_suit": 6,
    "plain_cards_per_suit": 4,
    "madness_cards_per_suit": 2,
    "total_rounds": 15,
    "tides": 3,
    "rounds_per_tide": 5,
    "hand_size": 5,
    "set_points_0": 0,
    "set_points_1": 1,
    "set_points_2": 3,
    "set_points_3": 6,
    "set_points_4_or_more": 10,
    "obsession_multiplier": 2,
    "points_per_madness_card": 1,
    "diversity_suits_needed": 4,
    "diversity_bonus": 4,
    "madness_bonus_points": 4,
    "madness_bonus_reduction": 1,
    "madness_loss_threshold": 9,
    "cards_retained_per_tide": 1,
    "retain_tides": 2,
    "starting_score": 0,
    "starting_madness": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Victory points so far.",
        "observable": true
      },
      {
        "key": "madness",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Madness total. Reaching 9 or more at a madness check loses the game.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The cards the player currently holds to draft from. Only the owner sees it.",
        "observable": false
      },
      {
        "key": "tableau",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Cards drafted face down this tide. Revealed by announcement at the end of the tide.",
        "observable": false
      },
      {
        "key": "obsession",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The secret Obsession suit for this tide. Revealed by announcement at the end of the tide.",
        "observable": false
      },
      {
        "key": "retained",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards kept face up from earlier tides. They are part of every later tide tableau.",
        "observable": true
      },
      {
        "key": "tide_icons",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Madness icons in this tide's tableau plus retained cards. Computed at the end of the tide.",
        "observable": false
      },
      {
        "key": "tide_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Points scored at this tide's scoring, before the madness bonus.",
        "observable": false
      },
      {
        "key": "lost",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if this player loses at a madness check, else 0.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round, 1 to 15.",
        "observable": true
      },
      {
        "key": "tide",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current tide, 1 to 3. Equals ceil(round / 5).",
        "observable": false
      },
      {
        "key": "round_in_tide",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Round within the tide, 1 to 5. Equals (round - 1) mod 5 + 1.",
        "observable": false
      },
      {
        "key": "full_deck",
        "type": "list",
        "visible": "public",
        "initial": [
          "Ruins-1",
          "Ruins-2",
          "Ruins-3",
          "Ruins-4",
          "Ruins*-1",
          "Ruins*-2",
          "Idols-1",
          "Idols-2",
          "Idols-3",
          "Idols-4",
          "Idols*-1",
          "Idols*-2",
          "Deep-1",
          "Deep-2",
          "Deep-3",
          "Deep-4",
          "Deep*-1",
          "Deep*-2",
          "Stars-1",
          "Stars-2",
          "Stars-3",
          "Stars-4",
          "Stars*-1",
          "Stars*-2",
          "Shore-1",
          "Shore-2",
          "Shore-3",
          "Shore-4",
          "Shore*-1",
          "Shore*-2"
        ],
        "meaning": "The full list of 30 cards, used to rebuild the deck each tide. A '*' marks a madness icon.",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "This tide's shuffled deck: the full deck minus all retained cards. Undealt cards are unused this tide.",
        "observable": false
      },
      {
        "key": "bonus_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat with strictly more tide_icons this tide (1 or 2), or 0 if the counts are equal.",
        "observable": false
      },
      {
        "key": "madness_end",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if the game ended at a madness check, else 0.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Seat 1 and seat 2 each start with score 0, madness 0, and empty hand, tableau, retained and obsession.",
    "The table's full_deck holds the 30 cards: in each of the 5 suits (Ruins, Idols, Deep, Stars, Shore), 4 plain cards and 2 madness cards marked '*'.",
    "round starts at 0. The deck is built and dealt at the start of each tide, inside the round steps."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; tide = ceil(round / 5); round_in_tide = (round - 1) mod 5 + 1. Announce the round and tide."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide == 1: deck = full_deck minus every card in either player's retained list; each player's hand = [] and tableau = []; then deal 5 cards to each player's hand. Each card is a random draw removed from deck and appended to hand. The cards left in deck are unused this tide."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand, tableau, obsession and both retained lists."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Ruins, Idols, Deep, Stars, Shore",
      "effect": "When round_in_tide == 1: set you.obsession to the chosen suit. It stays hidden from the opponent (ally) until the tide's reveal."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own hand",
      "effect": "Simultaneously, each player removes the chosen card from you.hand and appends it to you.tableau, face down. When round_in_tide == 5 the hand has 1 card, so the pick is forced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide < 5: swap hands, so seat 1's hand becomes seat 2's old hand and seat 2's hand becomes seat 1's old hand."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide == 5: reveal to everyone each player's tableau, retained cards and obsession."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide == 5, for each player, with T = tableau + retained: tide_icons = number of cards in T with '*'; madness += tide_icons. For each suit, n = cards of that suit in T and set_pts = 0 if n=0, 1 if n=1, 3 if n=2, 6 if n=3, 10 if n>=4, doubled if the suit equals obsession. tide_points = sum of set_pts + tide_icons * 1 + (4 if the number of distinct suits in T >= 4 else 0). score += tide_points. Then bonus_seat = 1 if seat 1's tide_icons > seat 2's, 2 if seat 2's > seat 1's, else 0. Announce each player's tide_points, score and madness."
    },
    {
      "action": "ask",
      "who": "the seat equal to bonus_seat (skipped if bonus_seat == 0)",
      "answer": "one of: gain_4_points, reduce_madness_1",
      "effect": "When round_in_tide == 5 and bonus_seat > 0: the bonus seat chooses privately. gain_4_points: you.score += 4. reduce_madness_1: you.madness -= 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide == 5, madness check. If exactly one player has madness >= 9, that player's lost = 1 and madness_end = 1. If both have madness >= 9: the one with the higher madness gets lost = 1; if equal, both keep lost = 0 (a draw); madness_end = 1 either way. Announce the result."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if madness_end == 1 or (round == 15 and round_in_tide == 5); otherwise continue."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from your own tableau (the cards drafted this tide)",
      "effect": "When round_in_tide == 5 and tide < 3: simultaneously, each player picks one card to retain permanently."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_tide == 5 and tide < 3: append each player's chosen card to you.retained, face up and public; set tableau = [] and obsession = ''. All other drafted cards go back to the pool used to rebuild the deck next tide. Announce the retained cards."
    }
  ],
  "ending": {
    "condition": "madness_end == 1 or (round == 15 and round_in_tide == 5)",
    "rank_by": "madness_end * (1 - you.lost) * 1000000 + (1 - madness_end) * (you.score * 100 + (99 - you.madness))",
    "decided_by": "If the game ended at a madness check, the player who did not lose wins; if both reached 9 or more with equal madness totals, both rank level and the game is a draw. Otherwise, after tide 3 the higher score wins; on tied scores the lower madness total wins; if both are tied, the game is a draw (shared win)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 30 cards: 5 suits (Ruins, Idols, Deep, Stars, Shore) of 6 cards each, 4 plain and 2 with a madness icon '*'."
    },
    {
      "id": "R2",
      "text": "The game has 15 rounds in 3 tides: rounds 1-5 are tide 1, rounds 6-10 tide 2, rounds 11-15 tide 3."
    },
    {
      "id": "R3",
      "text": "When a tide starts (rounds 1, 6, 11), then the deck is the 30 cards minus all retained cards, and each player is dealt a private hand of 5 drawn from it; the rest are unused that tide."
    },
    {
      "id": "R4",
      "text": "When a tide starts, then each player secretly chooses one of the 5 suits as their Obsession, hidden from the opponent until the tide is scored."
    },
    {
      "id": "R5",
      "text": "When a round is played, then both players simultaneously move one card from their own hand to their tableau, face down."
    },
    {
      "id": "R6",
      "text": "When the picks of rounds 1-4 of a tide are made, then the two players swap their remaining hands, so hands hold 5, 4, 3, 2, 1 cards."
    },
    {
      "id": "R7",
      "text": "When the fifth round of a tide is played, then each player's hand has exactly 1 card and that card is the forced pick."
    },
    {
      "id": "R8",
      "text": "When a tide ends (rounds 5, 10, 15), then both tableaus, retained cards and Obsessions are revealed to both players."
    },
    {
      "id": "R9",
      "text": "When a tide ends, then each player adds the number of '*' cards among their 5 drafted cards plus retained cards to their madness total."
    },
    {
      "id": "R10",
      "text": "When a tide ends, then each suit in a player's tide tableau scores 0/1/3/6/10 points for 0/1/2/3/4-or-more cards."
    },
    {
      "id": "R11",
      "text": "When a suit is the player's Obsession for that tide, then its set points are doubled (e.g., 3 cards score 12)."
    },
    {
      "id": "R12",
      "text": "When a tide ends, then a player scores +1 point per madness card in their tide tableau."
    },
    {
      "id": "R13",
      "text": "When a player's tide tableau contains at least 4 different suits, then that player scores +4 points."
    },
    {
      "id": "R14",
      "text": "When one player has strictly more madness icons than the other in their tide tableau, then that player privately chooses +4 points or madness total -1."
    },
    {
      "id": "R15",
      "text": "When both players have equal madness icons in their tide tableaus, then nobody gets the madness bonus."
    },
    {
      "id": "R16",
      "text": "When, after the madness bonus, exactly one player has madness total 9 or more, then the game ends immediately and that player loses."
    },
    {
      "id": "R17",
      "text": "When both players have madness 9 or more at a madness check, then the game ends and the one with the higher madness total loses; equal totals are a draw."
    },
    {
      "id": "R18",
      "text": "When tide 1 or tide 2 ends without a madness loss, then each player simultaneously chooses 1 card drafted that tide to retain face up permanently, and the other drafted cards return to the deck."
    },
    {
      "id": "R19",
      "text": "When a card is retained, then it counts in every later tide tableau for set points, madness icons, the +1 per madness card and the 4-suit bonus."
    },
    {
      "id": "R20",
      "text": "When tide 3 ends, then no card is retained."
    },
    {
      "id": "R21",
      "text": "When tide 3 is scored and no one lost to madness, then the higher score wins; on tied scores the lower madness total wins; if both are tied, the game is a draw."
    }
  ],
  "offers": [
    {
      "question": "Obsession choice (round 1 of each tide)",
      "who": "both seats",
      "options": "Ruins, Idols, Deep, Stars, Shore"
    },
    {
      "question": "Draft pick (every round)",
      "who": "both seats",
      "options": "each card currently in the seat's own hand (5, 4, 3, 2 or 1 options; in round 5 of a tide only the single remaining card)"
    },
    {
      "question": "Madness bonus (end of each tide)",
      "who": "only the seat with strictly more tide_icons; nobody if equal",
      "options": "gain_4_points, reduce_madness_1"
    },
    {
      "question": "Retain choice (end of tides 1 and 2 only, if the game continues)",
      "who": "both seats",
      "options": "each of the 5 cards the seat drafted this tide (its tableau, not earlier retained cards)"
    }
  ],
  "choices": [
    {
      "what": "Exactly 2 players (min 2, max 2, suggested 2)",
      "why": "The designer fixed 2. The hand-swap draft only works between two players: what you pass is exactly what your single opponent gets. The strategy lies in reading the opponent's Obsession from what they take, hate-drafting their suit, and managing madness against theirs for the bonus without nearing 9."
    },
    {
      "what": "No talk step",
      "why": "The source has no communication. Picks are secret and simultaneous, and with only two rivals in direct conflict, talk would add nothing faithful to the rules."
    },
    {
      "what": "Card names such as 'Deep-3' and 'Deep*-1'",
      "why": "Each of the 30 cards needs a distinct name so it can be removed from and appended to lists; '*' marks the madness icon, as in the source."
    },
    {
      "what": "rank_by encodes the madness loss with madness_end and lost",
      "why": "A single arithmetic expression must cover both endings. After a madness end only not-losing counts, and equal totals tie (draw). Otherwise score comes first, then lower madness."
    },
    {
      "what": "Madness reduction needs no floor at 0",
      "why": "The bonus seat added at least 1 icon this tide, so its madness total is at least 1 before the -1."
    }
  ],
  "simplifications": [
    {
      "what": "The Obsession is asked in its own simultaneous poll just before the first pick of the tide, not in the same answer",
      "why": "The engine takes one answer per question. Nothing is revealed between the two polls, so the choice is still made blind, at the same moment as the first pick."
    },
    {
      "what": "The reveal of face-down tableaus and Obsessions is done by an announcement, while the attributes stay owner-only",
      "why": "Visibility is fixed per attribute. The tell step makes the contents public at the moment the rules reveal them."
    },
    {
      "what": "The madness-bonus comparison uses a table attribute, bonus_seat",
      "why": "The engine has no operand for another player's attribute (player_attribute_compare workaround)."
    },
    {
      "what": "Steps for the start and end of a tide carry a 'when' condition on round_in_tide inside one flat round list",
      "why": "Single conditional steps are supported; no block of steps replaces another."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, madness, retained; table: round, madness_end.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the R20/R21 scenarios so they do not depend on which exact cards are dealt or passed. Pick options by a pattern that always matches, such as a suit prefix ('Idols', 'Stars') or simply any offered option, as the other tests already do. Do not preset hands or tableaus through attribute names that are not in the interface. To set up score and madness tie situations, use `given` only on interface attributes: `score`, `madness`, `retained`, `round` and `madness_end`. Start near the end of tide 3, then assert only on the ending and outcome: the winner, shared win or draw, and `madness_end` = 0. For R20, check that `retained` is unchanged after tide 3 ends; do not assert on dealt card identities.
````

## Reply

````
```json
[
  {
    "name": "Full deck holds 30 cards at setup",
    "rule": "R1",
    "players": 2,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"full_deck": 30}},
      "players": {"1": {"score": 0, "madness": 0, "retained": []}, "2": {"score": 0, "madness": 0, "retained": []}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Six rounds played reach round 6 (tide 2 started), no madness end possible",
    "rule": "R2",
    "players": 2,
    "seed": 2,
    "default": "first",
    "rounds": 6,
    "expect": {"game": {"round": 6, "madness_end": 0}}
  },
  {
    "name": "Tide start deals 5 each from a fresh 30-card deck (deck 20 after the deal, hands 4 after one pick and swap)",
    "rule": "R3",
    "players": 2,
    "seed": 3,
    "default": "first",
    "rounds": 1,
    "expect": {
      "lens": {"game": {"deck": 20}, "players": {"1": {"hand": 4}, "2": {"hand": 4}}},
      "game": {"round": 1}
    }
  },
  {
    "name": "Tide 2 deck excludes the retained cards (28 minus 10 dealt = 18)",
    "rule": "R3",
    "players": 2,
    "seed": 4,
    "default": "first",
    "rounds": 1,
    "given": {"players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Idols-1"]}}, "game": {"round": 5}},
    "expect": {
      "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 4}, "2": {"hand": 4}}},
      "players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Idols-1"]}},
      "game": {"round": 6}
    }
  },
  {
    "name": "Both seats are offered the 5 suits as Obsession at tide start",
    "rule": "R4",
    "players": 2,
    "seed": 5,
    "default": "first",
    "rounds": 1,
    "rules": [{"seat": 1, "options_include": "Stars"}, {"seat": 2, "options_include": "Shore"}],
    "expect": {
      "offered": [
        {"seat": 1, "option": "Ruins"}, {"seat": 1, "option": "Shore"},
        {"seat": 2, "option": "Idols"}, {"seat": 2, "option": "Deep"}
      ]
    }
  },
  {
    "name": "One round moves one card from hand to tableau for each seat",
    "rule": "R5",
    "players": 2,
    "seed": 6,
    "default": "first",
    "rounds": 1,
    "expect": {"lens": {"players": {"1": {"tableau": 1, "hand": 4}, "2": {"tableau": 1, "hand": 4}}}}
  },
  {
    "name": "After four rounds each hand holds 1 card and each tableau 4",
    "rule": "R6",
    "players": 2,
    "seed": 7,
    "default": "first",
    "rounds": 4,
    "expect": {"lens": {"players": {"1": {"hand": 1, "tableau": 4}, "2": {"hand": 1, "tableau": 4}}}}
  },
  {
    "name": "Fifth round takes the last card: hands empty, one card retained, tableau cleared",
    "rule": "R7",
    "players": 2,
    "seed": 8,
    "default": "first",
    "rounds": 5,
    "expect": {
      "lens": {"players": {"1": {"hand": 0, "retained": 1, "tableau": 0}, "2": {"hand": 0, "retained": 1, "tableau": 0}}},
      "game": {"round": 5, "madness_end": 0}
    }
  },
  {
    "name": "Tide 1 ends and is scored and revealed without a madness end",
    "rule": "R8",
    "players": 2,
    "seed": 9,
    "default": "first",
    "rounds": 5,
    "expect": {"game": {"round": 5, "madness_end": 0}, "lens": {"players": {"1": {"retained": 1}, "2": {"retained": 1}}}}
  },
  {
    "name": "Madness gains the icons in the tableau plus retained (2 each, equal so no bonus)",
    "rule": "R9",
    "players": 2,
    "seed": 10,
    "given": {"players": {"1": {"retained": ["Ruins*-1", "Idols*-1"]}, "2": {"retained": ["Deep*-1", "Stars*-1"]}}, "game": {"round": 14}},
    "expect": {
      "winner": [1, 2],
      "players": {"1": {"madness": 2, "score": 4}, "2": {"madness": 2, "score": 4}},
      "game": {"round": 15, "madness_end": 0}
    }
  },
  {
    "name": "Set points: 3 Ruins plus 2 Idols scores 9; 4 Deep plus 1 Stars scores 11",
    "rule": "R10",
    "players": 2,
    "seed": 11,
    "given": {"players": {"1": {"retained": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1", "Idols-2"]}, "2": {"retained": ["Deep-1", "Deep-2", "Deep-3", "Deep-4", "Stars-1"]}}, "game": {"round": 14}},
    "expect": {
      "winner": 2,
      "standings": {"1": 999, "2": 1199},
      "players": {"1": {"score": 9, "madness": 0}, "2": {"score": 11, "madness": 0}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Obsession doubles its suit: 3 Ruins with Ruins obsession scores 12, 3 Idols without scores 6",
    "rule": "R11",
    "players": 2,
    "seed": 12,
    "given": {"players": {"1": {"retained": ["Ruins-1", "Ruins-2", "Ruins-3"], "obsession": "Ruins"}, "2": {"retained": ["Idols-1", "Idols-2", "Idols-3"], "obsession": "Ruins"}}, "game": {"round": 14}},
    "expect": {
      "winner": 1,
      "players": {"1": {"score": 12}, "2": {"score": 6}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Plus 1 point per madness card (equal icons, no bonus)",
    "rule": "R12",
    "players": 2,
    "seed": 13,
    "given": {"players": {"1": {"retained": ["Ruins*-1", "Ruins*-2"]}, "2": {"retained": ["Idols*-1", "Idols*-2", "Idols-1"]}}, "game": {"round": 14}},
    "expect": {
      "winner": 2,
      "players": {"1": {"score": 5, "madness": 2}, "2": {"score": 8, "madness": 2}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Four different suits add 4 points; three suits do not",
    "rule": "R13",
    "players": 2,
    "seed": 14,
    "given": {"players": {"1": {"retained": ["Ruins-1", "Idols-1", "Deep-1", "Stars-1"]}, "2": {"retained": ["Ruins-2", "Idols-2", "Deep-2"]}}, "game": {"round": 14}},
    "expect": {
      "winner": 1,
      "players": {"1": {"score": 8}, "2": {"score": 3}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Seat with more icons is offered the bonus and takes +4 points; the other seat is not offered it",
    "rule": "R14",
    "players": 2,
    "seed": 15,
    "given": {"players": {"1": {"retained": ["Ruins*-1", "Idols-1"]}, "2": {"retained": ["Deep-1"]}}, "game": {"round": 14}},
    "rules": [{"seat": 1, "options_include": "gain_4_points"}],
    "expect": {
      "winner": 1,
      "players": {"1": {"score": 7, "madness": 1}, "2": {"score": 1, "madness": 0}},
      "offered": [{"seat": 1, "option": "reduce_madness_1"}],
      "not_offered": [{"seat": 2, "option": "gain_4_points"}, {"seat": 2, "option": "reduce_madness_1"}]
    }
  },
  {
    "name": "Bonus seat chooses madness -1 instead of points",
    "rule": "R14",
    "players": 2,
    "seed": 16,
    "given": {"players": {"1": {"retained": ["Ruins*-1", "Idols-1"], "madness": 5}, "2": {"retained": ["Deep-1"]}}, "game": {"round": 14}},
    "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
    "expect": {
      "winner": 1,
      "players": {"1": {"score": 3, "madness": 5}, "2": {"score": 1, "madness": 0}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Equal icons: nobody is offered the madness bonus",
    "rule": "R15",
    "players": 2,
    "seed": 17,
    "given": {"players": {"1": {"retained": ["Ruins*-1"]}, "2": {"retained": ["Idols*-1"]}}, "game": {"round": 14}},
    "expect": {
      "winner": [1, 2],
      "players": {"1": {"score": 2, "madness": 1}, "2": {"score": 2, "madness": 1}},
      "not_offered": [{"seat": 1, "option": "gain_4_points"}, {"seat": 2, "option": "gain_4_points"}, {"seat": 1, "option": "reduce_madness_1"}, {"seat": 2, "option": "reduce_madness_1"}]
    }
  },
  {
    "name": "Taking points leaves seat 1 at madness 9: it loses at the madness check",
    "rule": "R16",
    "players": 2,
    "seed": 18,
    "given": {"players": {"1": {"retained": ["Ruins*-1"], "madness": 8}, "2": {"retained": ["Idols-1"]}}, "game": {"round": 14}},
    "rules": [{"seat": 1, "options_include": "gain_4_points"}],
    "expect": {
      "winner": 2,
      "players": {"1": {"madness": 9}, "2": {"madness": 0}},
      "game": {"madness_end": 1}
    }
  },
  {
    "name": "Reducing madness to 8 after the bonus avoids the loss",
    "rule": "R16",
    "players": 2,
    "seed": 19,
    "given": {"players": {"1": {"retained": ["Ruins*-1"], "madness": 8}, "2": {"retained": ["Idols-1"]}}, "game": {"round": 14}},
    "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
    "expect": {
      "winner": 1,
      "players": {"1": {"madness": 8, "score": 2}, "2": {"madness": 0, "score": 1}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Madness far over 9 ends the game at the end of tide 1 (any cards dealt)",
    "rule": "R16",
    "players": 2,
    "seed": 20,
    "default": "first",
    "given": {"players": {"1": {"madness": 20}}},
    "expect": {"winner": 2, "game": {"round": 5, "madness_end": 1}}
  },
  {
    "name": "Both at 9 or more: higher madness loses",
    "rule": "R17",
    "players": 2,
    "seed": 21,
    "given": {"players": {"1": {"madness": 10}, "2": {"madness": 9}}, "game": {"round": 14}},
    "expect": {"winner": 2, "players": {"1": {"madness": 10}, "2": {"madness": 9}}, "game": {"madness_end": 1}}
  },
  {
    "name": "Both at 9 or more with equal madness: draw (shared)",
    "rule": "R17",
    "players": 2,
    "seed": 22,
    "given": {"players": {"1": {"madness": 9, "score": 50}, "2": {"madness": 9}}, "game": {"round": 14}},
    "expect": {"winner": [1, 2], "game": {"madness_end": 1}}
  },
  {
    "name": "End of tide 2 adds one retained card; the earlier retained card is not offered",
    "rule": "R18",
    "players": 2,
    "seed": 23,
    "default": "first",
    "rounds": 5,
    "given": {"players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Idols-1"]}}, "game": {"round": 5}},
    "expect": {
      "lens": {"players": {"1": {"retained": 2, "tableau": 0}, "2": {"retained": 2, "tableau": 0}}},
      "not_offered": [{"seat": 1, "option": "Ruins-1"}, {"seat": 2, "option": "Idols-1"}],
      "game": {"round": 10, "madness_end": 0}
    }
  },
  {
    "name": "Retained cards count for sets, icons, +1 per icon and the 4-suit bonus",
    "rule": "R19",
    "players": 2,
    "seed": 24,
    "given": {"players": {"1": {"retained": ["Ruins*-1", "Ruins-1", "Idols-1", "Deep-1", "Stars-1"]}, "2": {"retained": []}}, "game": {"round": 14}},
    "rules": [{"seat": 1, "options_include": "gain_4_points"}],
    "expect": {
      "winner": 1,
      "players": {"1": {"score": 15, "madness": 1}, "2": {"score": 0, "madness": 0}},
      "game": {"madness_end": 0}
    }
  },
  {
    "name": "Tide 3 end keeps retained unchanged and asks no retain choice",
    "rule": "R20",
    "players": 2,
    "seed": 25,
    "given": {"players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Idols-1"]}}, "game": {"round": 14}},
    "expect": {
      "winner": [1, 2],
      "players": {"1": {"retained": ["Ruins-1"], "score": 1}, "2": {"retained": ["Idols-1"], "score": 1}},
      "game": {"round": 15, "madness_end": 0}
    }
  },
  {
    "name": "After tide 3 the higher score wins",
    "rule": "R21",
    "players": 2,
    "seed": 26,
    "given": {"players": {"1": {"score": 10}, "2": {"score": 20}}, "game": {"round": 14}},
    "expect": {"winner": 2, "game": {"madness_end": 0}}
  },
  {
    "name": "Tied score: lower madness wins",
    "rule": "R21",
    "players": 2,
    "seed": 27,
    "given": {"players": {"1": {"score": 10, "madness": 3}, "2": {"score": 10, "madness": 5}}, "game": {"round": 14}},
    "expect": {"winner": 1, "game": {"madness_end": 0}}
  },
  {
    "name": "Tied score and madness: shared win",
    "rule": "R21",
    "players": 2,
    "seed": 28,
    "given": {"players": {"1": {"score": 10, "madness": 4}, "2": {"score": 10, "madness": 4}}, "game": {"round": 14}},
    "expect": {"winner": [1, 2], "game": {"madness_end": 0}}
  },
  {
    "name": "Huge score lead wins after a full tide 3 whatever the cards",
    "rule": "R21",
    "players": 2,
    "seed": 29,
    "default": "first",
    "given": {"players": {"1": {"score": 1000}, "2": {"score": 0}}, "game": {"round": 10}},
    "expect": {"winner": 1, "game": {"round": 15, "madness_end": 0}}
  }
]
```
````
