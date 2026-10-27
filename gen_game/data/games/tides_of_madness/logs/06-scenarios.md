# 06 scenarios

- time: 2026-10-27T17:54:35+00:00 (74.4s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 5c64d26662f01634, reply sha256 84798eb8fff18e71

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

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "R1: full deck holds 30 cards right after setup", "rule": "R1", "players": 2, "rounds": 0,
   "expect": {"lens": {"game": {"full_deck": 30}}, "game": {"round": 0, "madness_end": 0},
              "players": {"1": {"score": 0, "madness": 0, "retained": []}, "2": {"score": 0, "madness": 0, "retained": []}}}},

  {"name": "R2: round after 10 is round 11 (tide 3 starts, fresh 5-card deal then one pick)", "rule": "R2", "players": 2, "rounds": 1,
   "given": {"game": {"round": 10}},
   "expect": {"game": {"round": 11, "madness_end": 0}, "lens": {"players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}}}},

  {"name": "R3: first tide deals 5 each from 30, leaving 20 in the deck (random deal, counts only)", "rule": "R3", "players": 2, "rounds": 1,
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 20}, "players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}}}},

  {"name": "R3: tide 2 deck excludes retained cards: 30 - 2 - 10 = 18 (random deal, counts only)", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"round": 5}, "players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Deep-2"]}}},
   "expect": {"game": {"round": 6}, "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}},
              "players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Deep-2"]}}}},

  {"name": "R4: both seats are offered the five Obsession suits at tide start", "rule": "R4", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "Stars"}, {"seat": 2, "options_include": "Deep"}],
   "expect": {"offered": [{"seat": 1, "option": "Ruins"}, {"seat": 1, "option": "Shore"}, {"seat": 1, "option": "Stars"},
                          {"seat": 2, "option": "Idols"}, {"seat": 2, "option": "Deep"}]}},

  {"name": "R5: each round both players move one card from hand to tableau", "rule": "R5", "players": 2, "rounds": 1,
   "expect": {"lens": {"players": {"1": {"tableau": 1}, "2": {"tableau": 1}}}}},

  {"name": "R6: hands are swapped after picks in rounds 2 and 3", "rule": "R6", "players": 2, "rounds": 2,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["Ruins-1", "Ruins-2", "Ruins-3", "Ruins-4"], "tableau": ["Stars-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "tableau": ["Shore-1"], "obsession": "Deep"}}},
   "rules": [{"seat": 1, "options_include": "Ruins-1"}, {"seat": 2, "options_include": "Deep-1"}],
   "expect": {"offered": [{"seat": 1, "option": "Deep-4"}, {"seat": 2, "option": "Ruins-4"}],
              "not_offered": [{"seat": 1, "option": "Deep-1"}, {"seat": 2, "option": "Ruins-1"}],
              "lens": {"players": {"1": {"hand": 2, "tableau": 3}, "2": {"hand": 2, "tableau": 3}}},
              "game": {"round": 3}}},

  {"name": "R7: in round 5 of a tide the single hand card is the forced pick", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Stars-4"], "tableau": ["Ruins-1", "Ruins-2", "Idols-1", "Deep-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Shore-4"], "tableau": ["Deep-2", "Deep-3", "Stars-1", "Idols-2"], "obsession": "Deep"}}},
   "expect": {"offered": [{"seat": 1, "option": "Stars-4"}, {"seat": 2, "option": "Shore-4"}],
              "not_offered": [{"seat": 1, "option": "Shore-4"}, {"seat": 2, "option": "Stars-4"}],
              "game": {"round": 5}}},

  {"name": "R8: tide 1 ends with reveal and scoring (Shore x4 obsession 20+1; other 3+3+1)", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-1"], "tableau": ["Shore-1", "Shore-2", "Shore-3", "Shore-4"], "obsession": "Shore"},
                         "2": {"hand": ["Deep-1"], "tableau": ["Stars-1", "Stars-2", "Idols-1", "Idols-2"], "obsession": "Ruins"}}},
   "expect": {"players": {"1": {"score": 21, "madness": 0}, "2": {"score": 7, "madness": 0}}, "game": {"round": 5, "madness_end": 0}}},

  {"name": "R9: madness total grows by the '*' cards in the tide tableau (3 and 1)", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Deep*-1"], "tableau": ["Ruins*-1", "Idols*-1", "Deep-1", "Deep-2"], "obsession": "Stars"},
                         "2": {"hand": ["Shore*-1"], "tableau": ["Stars-1", "Stars-2", "Stars-3", "Shore-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"players": {"1": {"madness": 3, "score": 15}, "2": {"madness": 1, "score": 13}}, "game": {"madness_end": 0}}},

  {"name": "R10: set points 10 for four of a suit + 1 for a single; 3 + 6 for pair and triple", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-1"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Ruins-4"], "obsession": "Deep"},
                         "2": {"hand": ["Stars-3"], "tableau": ["Deep-1", "Deep-2", "Stars-1", "Stars-2"], "obsession": "Shore"}}},
   "expect": {"players": {"1": {"score": 11, "madness": 0}, "2": {"score": 9, "madness": 0}}}},

  {"name": "R11: Obsession suit set points doubled (3 cards score 12)", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Stars"}}},
   "expect": {"players": {"1": {"score": 15}, "2": {"score": 12}}}},

  {"name": "R12: +1 point per madness card (6+3+2 = 11 each)", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Idols-1"], "obsession": "Shore"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep*-2", "Deep-1", "Stars-1"], "obsession": "Shore"}}},
   "expect": {"players": {"1": {"score": 11, "madness": 2}, "2": {"score": 11, "madness": 2}}}},

  {"name": "R13: four different suits score +4; three suits do not", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Stars-2"], "tableau": ["Ruins-1", "Idols-1", "Deep-1", "Stars-1"], "obsession": "Shore"},
                         "2": {"hand": ["Deep-4"], "tableau": ["Ruins-2", "Idols-2", "Deep-2", "Deep-3"], "obsession": "Shore"}}},
   "expect": {"players": {"1": {"score": 10}, "2": {"score": 8}}}},

  {"name": "R14: seat with more icons may take madness -1", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Ruins-2"], "obsession": "Idols"},
                         "2": {"hand": ["Idols-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Stars"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"players": {"1": {"score": 12, "madness": 1}, "2": {"score": 11, "madness": 0}},
              "offered": [{"seat": 1, "option": "reduce_madness_1"}, {"seat": 1, "option": "gain_4_points"}],
              "not_offered": [{"seat": 2, "option": "gain_4_points"}, {"seat": 2, "option": "reduce_madness_1"}]}},

  {"name": "R14: seat with more icons may take +4 points", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Ruins-2"], "obsession": "Idols"},
                         "2": {"hand": ["Idols-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Stars"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"players": {"1": {"score": 16, "madness": 2}, "2": {"score": 11, "madness": 0}}}},

  {"name": "R15: equal icons, nobody is offered the madness bonus", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins*-1", "Ruins-1", "Ruins-2", "Idols-1"], "obsession": "Shore"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "expect": {"players": {"1": {"score": 10, "madness": 1}, "2": {"score": 10, "madness": 1}},
              "not_offered": [{"seat": 1, "option": "gain_4_points"}, {"seat": 1, "option": "reduce_madness_1"},
                              {"seat": 2, "option": "gain_4_points"}, {"seat": 2, "option": "reduce_madness_1"}]}},

  {"name": "R16: one seat reaches 9 madness after the bonus and loses", "rule": "R16", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 7, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 0, "hand": ["Stars-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"winner": 2, "standings": {"1": 0, "2": 1000000},
              "players": {"1": {"madness": 9, "score": 15}, "2": {"madness": 0, "score": 11}},
              "game": {"madness_end": 1, "round": 5}}},

  {"name": "R16: madness -1 bonus brings 9 back to 8, no loss, game continues", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 7, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 0, "hand": ["Stars-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"players": {"1": {"madness": 8, "score": 11}, "2": {"madness": 0}}, "game": {"madness_end": 0}}},

  {"name": "R17: both at 9+, higher madness (10 vs 9) loses", "rule": "R17", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 8, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 8, "hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"winner": 2, "standings": {"1": 0, "2": 1000000},
              "players": {"1": {"madness": 10}, "2": {"madness": 9}}, "game": {"madness_end": 1}}},

  {"name": "R17: both at 9 madness exactly is a draw", "rule": "R17", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 8, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 8, "hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"winner": [1, 2], "standings": {"1": 1000000, "2": 1000000},
              "players": {"1": {"madness": 9}, "2": {"madness": 9}}, "game": {"madness_end": 1}}},

  {"name": "R18: after tide 1 each seat retains one drafted card face up", "rule": "R18", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Deep"}}},
   "rules": [{"seat": 1, "options_include": "Ruins-3"}, {"seat": 2, "options_include": "Deep-2"}],
   "expect": {"players": {"1": {"retained": ["Ruins-3"]}, "2": {"retained": ["Deep-2"]}},
              "lens": {"players": {"1": {"tableau": 0, "retained": 1}, "2": {"tableau": 0, "retained": 1}}},
              "game": {"madness_end": 0}}},

  {"name": "R19: retained cards count for sets, icons, +1 and 4-suit bonus at tide 2", "rule": "R19", "players": 2, "rounds": 1,
   "given": {"game": {"round": 9},
             "players": {"1": {"retained": ["Ruins*-1"], "hand": ["Stars-1"], "tableau": ["Ruins-1", "Ruins-2", "Idols-1", "Deep-1"], "obsession": "Shore"},
                         "2": {"retained": ["Deep-3"], "hand": ["Shore-4"], "tableau": ["Deep-4", "Shore-1", "Shore-2", "Shore-3"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}, {"seat": 1, "options_include": "Idols-1"}, {"seat": 2, "options_include": "Shore-1"}],
   "expect": {"players": {"1": {"score": 18, "madness": 1, "retained": ["Ruins*-1", "Idols-1"]},
                          "2": {"score": 23, "madness": 0, "retained": ["Deep-3", "Shore-1"]}},
              "game": {"round": 10, "madness_end": 0}}},

  {"name": "R20: no card is retained after tide 3; higher score wins", "rule": "R20", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 20, "madness": 3, "retained": ["Ruins-1"], "hand": ["Idols-2"], "tableau": ["Ruins-2", "Ruins-3", "Ruins-4", "Idols-1"], "obsession": "Idols"},
                         "2": {"score": 20, "madness": 3, "retained": ["Deep-1"], "hand": ["Stars-2"], "tableau": ["Deep-2", "Stars-1", "Shore-1", "Idols-3"], "obsession": "Shore"}}},
   "expect": {"winner": 1, "standings": {"1": 3696, "2": 3396},
              "players": {"1": {"score": 36, "madness": 3, "retained": ["Ruins-1"]}, "2": {"score": 33, "madness": 3, "retained": ["Deep-1"]}},
              "lens": {"players": {"1": {"retained": 1}, "2": {"retained": 1}}},
              "game": {"round": 15, "madness_end": 0}}},

  {"name": "R21: tied score after tide 3, lower madness wins", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 10, "madness": 4, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 2, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "expect": {"winner": 2, "standings": {"1": 1995, "2": 1997},
              "players": {"1": {"score": 19, "madness": 4}, "2": {"score": 19, "madness": 2}}, "game": {"madness_end": 0}}},

  {"name": "R21: tied score and madness after tide 3 is a shared win", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 10, "madness": 3, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 3, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "expect": {"winner": [1, 2], "standings": {"1": 1996, "2": 1996},
              "players": {"1": {"score": 19}, "2": {"score": 19}}}},

  {"name": "R21: higher score after tide 3 wins despite higher madness", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 11, "madness": 5, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 1, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "expect": {"winner": 1, "standings": {"1": 2094, "2": 1998},
              "players": {"1": {"score": 20}, "2": {"score": 19}}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 24: needs `rules` (what each seat answers, by option name); scenario 25: needs `rules` (what each seat answers, by option name); scenario 26: needs `rules` (what each seat answers, by option name); scenario 27: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "R1: full deck holds 30 cards right after setup", "rule": "R1", "players": 2, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "Ruins"}, {"seat": 2, "options_include": "Ruins"}],
   "expect": {"lens": {"game": {"full_deck": 30}}, "game": {"round": 0, "madness_end": 0},
              "players": {"1": {"score": 0, "madness": 0, "retained": []}, "2": {"score": 0, "madness": 0, "retained": []}}}},

  {"name": "R2: round after 10 is round 11 (tide 3 starts, fresh 5-card deal then one pick)", "rule": "R2", "players": 2, "rounds": 1,
   "given": {"game": {"round": 10}},
   "rules": [{"seat": 1, "options_include": "Stars"}, {"seat": 2, "options_include": "Shore"}],
   "expect": {"game": {"round": 11, "madness_end": 0}, "lens": {"players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}}}},

  {"name": "R3: first tide deals 5 each from 30, leaving 20 in the deck (random deal, counts only)", "rule": "R3", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "Idols"}, {"seat": 2, "options_include": "Deep"}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"deck": 20}, "players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}}}},

  {"name": "R3: tide 2 deck excludes retained cards: 30 - 2 - 10 = 18 (random deal, counts only)", "rule": "R3", "players": 2, "rounds": 1,
   "given": {"game": {"round": 5}, "players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Deep-2"]}}},
   "rules": [{"seat": 1, "options_include": "Stars"}, {"seat": 2, "options_include": "Shore"}],
   "expect": {"game": {"round": 6}, "lens": {"game": {"deck": 18}, "players": {"1": {"hand": 4, "tableau": 1}, "2": {"hand": 4, "tableau": 1}}},
              "players": {"1": {"retained": ["Ruins-1"]}, "2": {"retained": ["Deep-2"]}}}},

  {"name": "R4: both seats are offered the five Obsession suits at tide start", "rule": "R4", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "Stars"}, {"seat": 2, "options_include": "Deep"}],
   "expect": {"offered": [{"seat": 1, "option": "Ruins"}, {"seat": 1, "option": "Shore"}, {"seat": 1, "option": "Stars"},
                          {"seat": 2, "option": "Idols"}, {"seat": 2, "option": "Deep"}]}},

  {"name": "R5: each round both players move one card from hand to tableau", "rule": "R5", "players": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": "Shore"}, {"seat": 2, "options_include": "Idols"}],
   "expect": {"lens": {"players": {"1": {"tableau": 1}, "2": {"tableau": 1}}}}},

  {"name": "R6: hands are swapped after picks in rounds 2 and 3", "rule": "R6", "players": 2, "rounds": 2,
   "given": {"game": {"round": 1},
             "players": {"1": {"hand": ["Ruins-1", "Ruins-2", "Ruins-3", "Ruins-4"], "tableau": ["Stars-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "tableau": ["Shore-1"], "obsession": "Deep"}}},
   "rules": [{"seat": 1, "options_include": "Ruins-1"}, {"seat": 2, "options_include": "Deep-1"}],
   "expect": {"offered": [{"seat": 1, "option": "Deep-4"}, {"seat": 2, "option": "Ruins-4"}],
              "not_offered": [{"seat": 1, "option": "Deep-1"}, {"seat": 2, "option": "Ruins-1"}],
              "lens": {"players": {"1": {"hand": 2, "tableau": 3}, "2": {"hand": 2, "tableau": 3}}},
              "game": {"round": 3}}},

  {"name": "R7: in round 5 of a tide the single hand card is the forced pick", "rule": "R7", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Stars-4"], "tableau": ["Ruins-1", "Ruins-2", "Idols-1", "Deep-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Shore-4"], "tableau": ["Deep-2", "Deep-3", "Stars-1", "Idols-2"], "obsession": "Deep"}}},
   "rules": [{"seat": 1, "options_include": "Stars-4"}, {"seat": 2, "options_include": "Shore-4"}],
   "expect": {"offered": [{"seat": 1, "option": "Stars-4"}, {"seat": 2, "option": "Shore-4"}],
              "not_offered": [{"seat": 1, "option": "Shore-4"}, {"seat": 2, "option": "Stars-4"}],
              "game": {"round": 5}}},

  {"name": "R8: tide 1 ends with reveal and scoring (Shore x4 obsession 20+1; other 3+3+1)", "rule": "R8", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-1"], "tableau": ["Shore-1", "Shore-2", "Shore-3", "Shore-4"], "obsession": "Shore"},
                         "2": {"hand": ["Deep-1"], "tableau": ["Stars-1", "Stars-2", "Idols-1", "Idols-2"], "obsession": "Ruins"}}},
   "rules": [{"seat": 1, "options_include": "Ruins-1"}, {"seat": 2, "options_include": "Deep-1"}],
   "expect": {"players": {"1": {"score": 21, "madness": 0}, "2": {"score": 7, "madness": 0}}, "game": {"round": 5, "madness_end": 0}}},

  {"name": "R9: madness total grows by the '*' cards in the tide tableau (3 and 1)", "rule": "R9", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Deep*-1"], "tableau": ["Ruins*-1", "Idols*-1", "Deep-1", "Deep-2"], "obsession": "Stars"},
                         "2": {"hand": ["Shore*-1"], "tableau": ["Stars-1", "Stars-2", "Stars-3", "Shore-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"players": {"1": {"madness": 3, "score": 15}, "2": {"madness": 1, "score": 13}}, "game": {"madness_end": 0}}},

  {"name": "R10: set points 10 for four of a suit + 1 for a single; 3 + 6 for pair and triple", "rule": "R10", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-1"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Ruins-4"], "obsession": "Deep"},
                         "2": {"hand": ["Stars-3"], "tableau": ["Deep-1", "Deep-2", "Stars-1", "Stars-2"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-1"}, {"seat": 2, "options_include": "Stars-3"}],
   "expect": {"players": {"1": {"score": 11, "madness": 0}, "2": {"score": 9, "madness": 0}}}},

  {"name": "R11: Obsession suit set points doubled (3 cards score 12)", "rule": "R11", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Stars"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"players": {"1": {"score": 15}, "2": {"score": 12}}}},

  {"name": "R12: +1 point per madness card (6+3+2 = 11 each)", "rule": "R12", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Idols-1"], "obsession": "Shore"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep*-2", "Deep-1", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"players": {"1": {"score": 11, "madness": 2}, "2": {"score": 11, "madness": 2}}}},

  {"name": "R13: four different suits score +4; three suits do not", "rule": "R13", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Stars-2"], "tableau": ["Ruins-1", "Idols-1", "Deep-1", "Stars-1"], "obsession": "Shore"},
                         "2": {"hand": ["Deep-4"], "tableau": ["Ruins-2", "Idols-2", "Deep-2", "Deep-3"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Stars-2"}, {"seat": 2, "options_include": "Deep-4"}],
   "expect": {"players": {"1": {"score": 10}, "2": {"score": 8}}}},

  {"name": "R14: seat with more icons may take madness -1", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Ruins-2"], "obsession": "Idols"},
                         "2": {"hand": ["Idols-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Stars"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"players": {"1": {"score": 12, "madness": 1}, "2": {"score": 11, "madness": 0}},
              "offered": [{"seat": 1, "option": "reduce_madness_1"}, {"seat": 1, "option": "gain_4_points"}],
              "not_offered": [{"seat": 2, "option": "gain_4_points"}, {"seat": 2, "option": "reduce_madness_1"}]}},

  {"name": "R14: seat with more icons may take +4 points", "rule": "R14", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Ruins-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Ruins-1", "Ruins-2"], "obsession": "Idols"},
                         "2": {"hand": ["Idols-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Stars"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"players": {"1": {"score": 16, "madness": 2}, "2": {"score": 11, "madness": 0}}}},

  {"name": "R15: equal icons, nobody is offered the madness bonus", "rule": "R15", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins*-1", "Ruins-1", "Ruins-2", "Idols-1"], "obsession": "Shore"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"players": {"1": {"score": 10, "madness": 1}, "2": {"score": 10, "madness": 1}},
              "not_offered": [{"seat": 1, "option": "gain_4_points"}, {"seat": 1, "option": "reduce_madness_1"},
                              {"seat": 2, "option": "gain_4_points"}, {"seat": 2, "option": "reduce_madness_1"}]}},

  {"name": "R16: one seat reaches 9 madness after the bonus and loses", "rule": "R16", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 7, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 0, "hand": ["Stars-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"winner": 2, "standings": {"1": 0, "2": 1000000},
              "players": {"1": {"madness": 9, "score": 15}, "2": {"madness": 0, "score": 11}},
              "game": {"madness_end": 1, "round": 5}}},

  {"name": "R16: madness -1 bonus brings 9 back to 8, no loss, game continues", "rule": "R16", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 7, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 0, "hand": ["Stars-1"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Deep-4"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"players": {"1": {"madness": 8, "score": 11}, "2": {"madness": 0}}, "game": {"madness_end": 0}}},

  {"name": "R17: both at 9+, higher madness (10 vs 9) loses", "rule": "R17", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 8, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 8, "hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}],
   "expect": {"winner": 2, "standings": {"1": 0, "2": 1000000},
              "players": {"1": {"madness": 10}, "2": {"madness": 9}}, "game": {"madness_end": 1}}},

  {"name": "R17: both at 9 madness exactly is a draw", "rule": "R17", "players": 2,
   "given": {"game": {"round": 4},
             "players": {"1": {"madness": 8, "hand": ["Idols-3"], "tableau": ["Ruins*-1", "Ruins*-2", "Idols-1", "Idols-2"], "obsession": "Shore"},
                         "2": {"madness": 8, "hand": ["Stars-2"], "tableau": ["Deep*-1", "Deep-1", "Deep-2", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "reduce_madness_1"}],
   "expect": {"winner": [1, 2], "standings": {"1": 1000000, "2": 1000000},
              "players": {"1": {"madness": 9}, "2": {"madness": 9}}, "game": {"madness_end": 1}}},

  {"name": "R18: after tide 1 each seat retains one drafted card face up", "rule": "R18", "players": 2, "rounds": 1,
   "given": {"game": {"round": 4},
             "players": {"1": {"hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Ruins"},
                         "2": {"hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Deep"}}},
   "rules": [{"seat": 1, "options_include": "Ruins-3"}, {"seat": 2, "options_include": "Deep-2"}],
   "expect": {"players": {"1": {"retained": ["Ruins-3"]}, "2": {"retained": ["Deep-2"]}},
              "lens": {"players": {"1": {"tableau": 0, "retained": 1}, "2": {"tableau": 0, "retained": 1}}},
              "game": {"madness_end": 0}}},

  {"name": "R19: retained cards count for sets, icons, +1 and 4-suit bonus at tide 2", "rule": "R19", "players": 2, "rounds": 1,
   "given": {"game": {"round": 9},
             "players": {"1": {"retained": ["Ruins*-1"], "hand": ["Stars-1"], "tableau": ["Ruins-1", "Ruins-2", "Idols-1", "Deep-1"], "obsession": "Shore"},
                         "2": {"retained": ["Deep-3"], "hand": ["Shore-4"], "tableau": ["Deep-4", "Shore-1", "Shore-2", "Shore-3"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "gain_4_points"}, {"seat": 1, "options_include": "Idols-1"}, {"seat": 2, "options_include": "Shore-1"}],
   "expect": {"players": {"1": {"score": 18, "madness": 1, "retained": ["Ruins*-1", "Idols-1"]},
                          "2": {"score": 23, "madness": 0, "retained": ["Deep-3", "Shore-1"]}},
              "game": {"round": 10, "madness_end": 0}}},

  {"name": "R20: no card is retained after tide 3; higher score wins", "rule": "R20", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 20, "madness": 3, "retained": ["Ruins-1"], "hand": ["Idols-2"], "tableau": ["Ruins-2", "Ruins-3", "Ruins-4", "Idols-1"], "obsession": "Idols"},
                         "2": {"score": 20, "madness": 3, "retained": ["Deep-1"], "hand": ["Stars-2"], "tableau": ["Deep-2", "Stars-1", "Shore-1", "Idols-3"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"winner": 1, "standings": {"1": 3696, "2": 3396},
              "players": {"1": {"score": 36, "madness": 3, "retained": ["Ruins-1"]}, "2": {"score": 33, "madness": 3, "retained": ["Deep-1"]}},
              "lens": {"players": {"1": {"retained": 1}, "2": {"retained": 1}}},
              "game": {"round": 15, "madness_end": 0}}},

  {"name": "R21: tied score after tide 3, lower madness wins", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 10, "madness": 4, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 2, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"winner": 2, "standings": {"1": 1995, "2": 1997},
              "players": {"1": {"score": 19, "madness": 4}, "2": {"score": 19, "madness": 2}}, "game": {"madness_end": 0}}},

  {"name": "R21: tied score and madness after tide 3 is a shared win", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 10, "madness": 3, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 3, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"winner": [1, 2], "standings": {"1": 1996, "2": 1996},
              "players": {"1": {"score": 19}, "2": {"score": 19}}}},

  {"name": "R21: higher score after tide 3 wins despite higher madness", "rule": "R21", "players": 2,
   "given": {"game": {"round": 14},
             "players": {"1": {"score": 11, "madness": 5, "hand": ["Idols-2"], "tableau": ["Ruins-1", "Ruins-2", "Ruins-3", "Idols-1"], "obsession": "Deep"},
                         "2": {"score": 10, "madness": 1, "hand": ["Stars-2"], "tableau": ["Deep-1", "Deep-2", "Deep-3", "Stars-1"], "obsession": "Shore"}}},
   "rules": [{"seat": 1, "options_include": "Idols-2"}, {"seat": 2, "options_include": "Stars-2"}],
   "expect": {"winner": 1, "standings": {"1": 2094, "2": 1998},
              "players": {"1": {"score": 20}, "2": {"score": 19}}}}
]
````
