# 06 scenarios

- time: 2026-10-28T06:08:12+00:00 (134.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 1d29f89f1313b1dc, reply sha256 162799011eefaac1

## Sent

````
SPEC:
{
  "name": "Gracias: The Counted Gift",
  "summary": "Four players draft face-up/face-down card triplets over 3 sessions of 4 rounds. In each pick a player keeps one face-up card, gifts the other to an opponent and secretly takes the hidden card. Sets of 4 in a colour score 3 points, and the largest leftover pile in each colour is discarded.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "players": 4,
    "colours": 4,
    "cards_per_colour": 12,
    "deck_size": 48,
    "sessions": 3,
    "rounds_per_session": 4,
    "total_rounds": 12,
    "triplets_per_round": 4,
    "cards_per_triplet": 3,
    "cards_laid_out_per_round": 12,
    "shuffle_rounds_first": 1,
    "shuffle_rounds_second": 5,
    "shuffle_rounds_third": 9,
    "stack_size": 4,
    "points_per_stack": 3,
    "points_per_loose_card": 1,
    "min_loose_for_discard": 1,
    "count_increment": 1,
    "rank_tiebreak_multiplier": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "pub_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Public count of Red cards this session (kept plus received as gifts)",
        "observable": false
      },
      {
        "key": "pub_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Public count of Blue cards this session",
        "observable": false
      },
      {
        "key": "pub_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Public count of Green cards this session",
        "observable": false
      },
      {
        "key": "pub_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Public count of Yellow cards this session",
        "observable": false
      },
      {
        "key": "hid_red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Hidden count of Red H cards taken this session, known only to the owner until the session reveal",
        "observable": false
      },
      {
        "key": "hid_blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Hidden count of Blue H cards this session",
        "observable": false
      },
      {
        "key": "hid_green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Hidden count of Green H cards this session",
        "observable": false
      },
      {
        "key": "hid_yellow",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Hidden count of Yellow H cards this session",
        "observable": false
      },
      {
        "key": "totals",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0
        ],
        "meaning": "At session end, public + hidden count per colour, in the order Red, Blue, Green, Yellow",
        "observable": false
      },
      {
        "key": "stacks",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0
        ],
        "meaning": "At session end, floor(total/4) per colour, in the order Red, Blue, Green, Yellow",
        "observable": false
      },
      {
        "key": "loose",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0
        ],
        "meaning": "At session end, total - 4*stacks per colour (0-3), in the order Red, Blue, Green, Yellow",
        "observable": false
      },
      {
        "key": "session_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Score of the session just ended",
        "observable": true
      },
      {
        "key": "game_total",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of session scores; the main score",
        "observable": true
      },
      {
        "key": "best_session_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest single session score so far; the tie-break",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "Undealt cards (colour names); refilled to 12 of each colour (48) at rounds 1, 5 and 9",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round, 1 to 12",
        "observable": true
      },
      {
        "key": "session",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current session, 1 to 3",
        "observable": true
      },
      {
        "key": "t1_a",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T1 face-up card A colour",
        "observable": false
      },
      {
        "key": "t1_b",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T1 face-up card B colour",
        "observable": false
      },
      {
        "key": "t1_h",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Triplet T1 face-down card H colour",
        "observable": false
      },
      {
        "key": "t2_a",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T2 face-up card A colour",
        "observable": false
      },
      {
        "key": "t2_b",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T2 face-up card B colour",
        "observable": false
      },
      {
        "key": "t2_h",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Triplet T2 face-down card H colour",
        "observable": false
      },
      {
        "key": "t3_a",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T3 face-up card A colour",
        "observable": false
      },
      {
        "key": "t3_b",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T3 face-up card B colour",
        "observable": false
      },
      {
        "key": "t3_h",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Triplet T3 face-down card H colour",
        "observable": false
      },
      {
        "key": "t4_a",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T4 face-up card A colour",
        "observable": false
      },
      {
        "key": "t4_b",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Triplet T4 face-up card B colour",
        "observable": false
      },
      {
        "key": "t4_h",
        "type": "text",
        "visible": "none",
        "initial": "",
        "meaning": "Triplet T4 face-down card H colour",
        "observable": false
      },
      {
        "key": "open_triplets",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Triplets not yet taken this round (subset of T1, T2, T3, T4)",
        "observable": false
      },
      {
        "key": "max_loose",
        "type": "list",
        "visible": "public",
        "initial": [
          0,
          0,
          0,
          0
        ],
        "meaning": "At session end, the highest loose value among the 4 players per colour, in the order Red, Blue, Green, Yellow",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seat 4 players in seats 1-4.",
    "Set every player's public and hidden counts for Red, Blue, Green and Yellow to 0, and set game_total, session_score and best_session_score to 0.",
    "Set round = 1 and session = 1. The deck is filled at the start of round 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round mod 4 == 1 (rounds 1, 5, 9): set deck to 48 cards, 12 each of Red, Blue, Green and Yellow (shuffle). No other round refills or shuffles the deck."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Lay out: draw 12 cards at random from deck, removing each one from deck, into t1_a, t1_b, t1_h, t2_a, t2_b, t2_h, t3_a, t3_b, t3_h, t4_a, t4_b, t4_h. Set open_triplets = [T1, T2, T3, T4]."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the A and B colours of T1-T4 (t1_a, t1_b, ..., t4_a, t4_b). The H cards stay secret."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting at seat ((round-1) mod 4)+1 and going up in seat order, wrapping from 4 to 1",
      "answer": "a choice from the list of every combination of (a triplet in open_triplets) x (keep A or keep B) x (an opponent seat to receive the other face-up card), e.g. 'T2: keep A (Red), give B (Blue) to seat 3'",
      "effect": "The picker's pub_<kept colour> += 1. The chosen receiver's pub_<gifted colour> += 1. The triplet's H colour is told privately to the picker only, and the picker's hid_<H colour> += 1. The triplet is removed from open_triplets. The keep and the gift (not H) are announced to all at once."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's pub_red, pub_blue, pub_green and pub_yellow."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round mod 4 == 0: reveal every player's hid_red, hid_blue, hid_green and hid_yellow to everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round mod 4 == 0: for each player and colour c, totals[c] = pub_c + hid_c, stacks[c] = floor(totals[c] / 4), loose[c] = totals[c] - 4*stacks[c]."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "When round mod 4 == 0: for each colour c, max_loose[c] = the maximum of loose[c] over the 4 players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round mod 4 == 0: session_score = sum over the 4 colours of (3*stacks[c] + (loose[c] if NOT (max_loose[c] >= 1 and loose[c] == max_loose[c]) else 0)). Then game_total += session_score, and if session_score > best_session_score, best_session_score = session_score. Announce session_score, game_total and best_session_score."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round mod 4 == 0: set every pub_* and hid_* to 0, and session += 1."
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
      "effect": "End the game if round > 12; otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "round > 12",
    "rank_by": "you.game_total * 1000 + you.best_session_score",
    "decided_by": "Highest game_total wins. Among players tied on it, the highest best_session_score wins. Players still tied share the win, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "The deck has 48 cards: 12 each of Red, Blue, Green and Yellow."
    },
    {
      "id": "R2",
      "text": "When the round is 1, 5 or 9, the deck is reset to all 48 cards and shuffled; in no other round is it shuffled or refilled."
    },
    {
      "id": "R3",
      "text": "Each round, 12 cards leave the deck and form triplets T1-T4, each with face-up A and B and face-down H, so after the 4th round of a session the deck is empty."
    },
    {
      "id": "R4",
      "text": "When the triplets are laid out, the A and B colours of all four triplets are announced to everyone, and no H colour is announced."
    },
    {
      "id": "R5",
      "text": "In round r, seat ((r-1) mod 4)+1 picks first, then the others in increasing seat order, wrapping from 4 to 1 (round 2: seats 2, 3, 4, 1)."
    },
    {
      "id": "R6",
      "text": "When a player picks, they choose one triplet still open, keep exactly one of its face-up cards, and gift the other face-up card to one opponent; gifting to oneself or not gifting is not offered."
    },
    {
      "id": "R7",
      "text": "When a player keeps a card of colour c, their pub_c rises by 1."
    },
    {
      "id": "R8",
      "text": "When a player is gifted a card of colour c, their pub_c rises by 1."
    },
    {
      "id": "R9",
      "text": "When a player takes a triplet, its H colour is told only to that player and their hid_<H colour> rises by 1."
    },
    {
      "id": "R10",
      "text": "When a triplet is taken, it is removed from open_triplets, and the 4th picker has exactly one triplet left but still chooses which card to keep and whom to gift."
    },
    {
      "id": "R11",
      "text": "After each round, every player's four public counts are announced."
    },
    {
      "id": "R12",
      "text": "After rounds 4, 8 and 12, every player's hidden counts are revealed and total = public + hidden per colour, and each colour's totals over the 4 players sum to 12."
    },
    {
      "id": "R13",
      "text": "At session end, stacks = floor(total/4) and loose = total - 4*stacks per colour (for example total 7 gives 1 stack and 3 loose)."
    },
    {
      "id": "R14",
      "text": "For each colour, if the highest loose value among the players is at least 1, every player whose loose equals it scores 0 for those loose cards, and ties all discard."
    },
    {
      "id": "R15",
      "text": "Session score = 3 points per stack + 1 point per loose card not discarded, summed over the 4 colours (for example Red total 5 with Red max loose 2 gives 3+1 = 4 points)."
    },
    {
      "id": "R16",
      "text": "When the session score is added, game_total rises by it, and best_session_score becomes it if it is greater than the old best."
    },
    {
      "id": "R17",
      "text": "After the session score, all public and hidden counts return to 0."
    },
    {
      "id": "R18",
      "text": "The game ends after round 12 (3 sessions of 4 rounds)."
    },
    {
      "id": "R19",
      "text": "The highest game_total wins; a tie is broken by the highest best_session_score; players still tied share the win."
    }
  ],
  "offers": [
    {
      "question": "Draft pick (each player in turn)",
      "who": "the seat whose turn it is",
      "options": "Every triplet in open_triplets x {keep A and gift B, keep B and gift A} x {each of the 3 other seats as receiver}: 24 options for the first picker, 18 for the second, 12 for the third, and 6 for the last picker (one triplet). The picker's own seat is never offered as receiver."
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players (min = max = suggested = 4)",
      "why": "The designer fixed 4. The 4 triplets per round, 12 cards per colour and the rotating first pick are all sized to 4 seats. The game is about counting cards and gifting tactically against several rivals, and it needs 3 opponents to choose among as gift targets."
    },
    {
      "what": "No talk step",
      "why": "The source has no communication phase. Adding one would add a mechanic."
    },
    {
      "what": "The whole pick (triplet, which card to keep, receiver) is asked as one choice from a generated list",
      "why": "The source resolves the pick as a single action. One question keeps it atomic and offers only legal combinations."
    },
    {
      "what": "rank_by multiplier 1000",
      "why": "best_session_score is far below 1000, so game_total always dominates and the best session only breaks ties."
    },
    {
      "what": "totals, stacks, loose and max_loose kept as 4-element lists in the order Red, Blue, Green, Yellow",
      "why": "The rules name these values, so they are declared, and lists keep the attribute count manageable."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player counts the unseen cards to estimate opponents' hidden colours, completes stacks of 4, and gifts cards that push a rival into a majority-loose discard or past a stack boundary that breaks their leftovers."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling and dealing from the top is modelled as drawing 12 cards at random without replacement from the deck list each round, with the deck refilled only at rounds 1, 5 and 9",
      "why": "This has the same distribution as one shuffle per session followed by top-card dealing, and it is the engine's way to draw."
    },
    {
      "what": "The session-end reveal is a broadcast of hidden counts rather than a change in visibility",
      "why": "Attribute visibility is fixed. Announcing the values gives everyone the same information."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: session_score, game_total, best_session_score; table: round, session.
````

## Reply

````
```json
[
  {"name": "A full first session plays out from a fresh 48-card deck (colour mix is random, only progress is asserted)", "rule": "R1", "players": 4, "seed": 1, "rounds": 4, "default": "first",
   "rules": [],
   "expect": {"game": {"round": 5, "session": 2},
              "offered": [{"seat": 1, "option": "T1"}, {"seat": 1, "option": "keep A"}]}},

  {"name": "Round 2 does not refill or reshuffle: an all-Red remaining deck offers only Red cards", "rule": "R2", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 2, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [],
   "expect": {"game": {"round": 3, "session": 1},
              "offered": [{"seat": 2, "option": "Red"}],
              "not_offered": [{"seat": 1, "option": "Blue"}, {"seat": 2, "option": "Blue"}, {"seat": 3, "option": "Green"}, {"seat": 4, "option": "Yellow"},
                              {"seat": 2, "option": "Green"}, {"seat": 3, "option": "Yellow"}, {"seat": 4, "option": "Blue"}, {"seat": 1, "option": "Green"}]}},

  {"name": "Four rounds of 12 cards use the whole deck and the session closes into session 2", "rule": "R3", "players": 4, "seed": 2, "rounds": 4, "default": "decline",
   "rules": [],
   "expect": {"game": {"round": 5, "session": 2}}},

  {"name": "Face-up colours are shown in the pick options", "rule": "R4", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 2, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [],
   "expect": {"offered": [{"seat": 2, "option": "Red"}, {"seat": 3, "option": "Red"}, {"seat": 4, "option": "Red"}, {"seat": 1, "option": "Red"}]}},

  {"name": "Round 3 pick order is seats 3, 4, 1, 2", "rule": "R5", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 3, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [{"seat": 3, "options_include": "T1"}, {"seat": 4, "options_include": "T2"}, {"seat": 1, "options_include": "T3"}],
   "expect": {"offered": [{"seat": 2, "option": "T4"}],
              "not_offered": [{"seat": 4, "option": "T1"}, {"seat": 1, "option": "T1"}, {"seat": 1, "option": "T2"},
                              {"seat": 2, "option": "T1"}, {"seat": 2, "option": "T2"}, {"seat": 2, "option": "T3"}]}},

  {"name": "A pick keeps A or B and gifts to an opponent; gifting to oneself is never offered", "rule": "R6", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 2, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [],
   "expect": {"offered": [{"seat": 2, "option": "keep A"}, {"seat": 2, "option": "keep B"}, {"seat": 2, "option": "to seat 1"}, {"seat": 2, "option": "to seat 3"}, {"seat": 2, "option": "to seat 4"}],
              "not_offered": [{"seat": 1, "option": "to seat 1"}, {"seat": 2, "option": "to seat 2"}, {"seat": 3, "option": "to seat 3"}, {"seat": 4, "option": "to seat 4"}]}},

  {"name": "Kept cards count: seat 2 with 2 Red reaches a stack of 4 by keeping and taking H", "rule": "R7", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"2": {"pub_red": 2}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 3"}],
   "expect": {"players": {"1": {"session_score": 4}, "2": {"session_score": 3}, "3": {"session_score": 0}, "4": {"session_score": 2}}}},

  {"name": "Gifted cards count: three gifts to seat 1 give it 5 Red", "rule": "R8", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"players": {"1": {"session_score": 4}, "2": {"session_score": 0}, "3": {"session_score": 2}, "4": {"session_score": 2}}}},

  {"name": "The hidden card counts toward totals: seat 1 with 1 Red reaches exactly 4", "rule": "R9", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"pub_red": 1}}},
   "rules": [{"seat": 1, "options_include": "to seat 2"}, {"seat": 2, "options_include": "to seat 3"}, {"seat": 3, "options_include": "to seat 4"}, {"seat": 4, "options_include": "to seat 1"}],
   "expect": {"players": {"1": {"session_score": 3}, "2": {"session_score": 0}, "3": {"session_score": 0}, "4": {"session_score": 0}}}},

  {"name": "The last picker has only the one remaining triplet but still chooses the card and the receiver", "rule": "R10", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 2, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [{"seat": 2, "options_include": "T1"}, {"seat": 3, "options_include": "T2"}, {"seat": 4, "options_include": "T3"}],
   "expect": {"offered": [{"seat": 1, "option": "T4"}, {"seat": 1, "option": "keep A"}, {"seat": 1, "option": "keep B"},
                          {"seat": 1, "option": "to seat 2"}, {"seat": 1, "option": "to seat 3"}, {"seat": 1, "option": "to seat 4"}],
              "not_offered": [{"seat": 1, "option": "T1"}, {"seat": 1, "option": "T2"}, {"seat": 1, "option": "T3"}]}},

  {"name": "After a mid-session round play moves on with no scoring", "rule": "R11", "players": 4, "seed": 3, "rounds": 1, "default": "decline",
   "rules": [],
   "expect": {"game": {"round": 2, "session": 1},
              "players": {"1": {"session_score": 0, "game_total": 0}, "2": {"session_score": 0, "game_total": 0}, "3": {"session_score": 0, "game_total": 0}, "4": {"session_score": 0, "game_total": 0}}}},

  {"name": "Session reveal adds public and hidden counts (consistent 48-card session)", "rule": "R12", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"pub_blue": 3, "hid_blue": 1, "pub_green": 2, "hid_green": 2},
                         "2": {"pub_blue": 2, "hid_blue": 2, "pub_yellow": 3, "hid_yellow": 1},
                         "3": {"pub_blue": 3, "hid_blue": 1, "pub_yellow": 2, "hid_yellow": 2},
                         "4": {"pub_green": 6, "hid_green": 2, "pub_yellow": 3, "hid_yellow": 1}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"players": {"1": {"session_score": 10}, "2": {"session_score": 6}, "3": {"session_score": 8}, "4": {"session_score": 11}}}},

  {"name": "Stacks and loose: total 6 gives 1 stack and 2 loose, total 7 gives 1 stack and 3 loose", "rule": "R13", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"pub_blue": 4, "hid_blue": 2}, "2": {"pub_blue": 3}, "3": {"pub_green": 5, "hid_green": 2}}},
   "rules": [{"seat": 1, "options_include": "to seat 2"}, {"seat": 2, "options_include": "to seat 3"}, {"seat": 3, "options_include": "to seat 4"}, {"seat": 4, "options_include": "to seat 1"}],
   "expect": {"players": {"1": {"session_score": 5}, "2": {"session_score": 0}, "3": {"session_score": 3}, "4": {"session_score": 0}}}},

  {"name": "Players tied on the highest loose value all discard", "rule": "R14", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"pub_yellow": 2}, "2": {"pub_yellow": 1, "hid_yellow": 1}, "3": {"pub_yellow": 1}}},
   "rules": [{"seat": 1, "options_include": "to seat 2"}, {"seat": 2, "options_include": "to seat 3"}, {"seat": 3, "options_include": "to seat 4"}, {"seat": 4, "options_include": "to seat 1"}],
   "expect": {"players": {"1": {"session_score": 0}, "2": {"session_score": 0}, "3": {"session_score": 1}, "4": {"session_score": 0}}}},

  {"name": "Total 5 with a max loose of 2 scores 3+1 = 4; a clean stack of 4 scores 3", "rule": "R15", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"pub_blue": 5}, "2": {"pub_blue": 2}, "3": {"pub_green": 4}}},
   "rules": [{"seat": 1, "options_include": "to seat 2"}, {"seat": 2, "options_include": "to seat 3"}, {"seat": 3, "options_include": "to seat 4"}, {"seat": 4, "options_include": "to seat 1"}],
   "expect": {"players": {"1": {"session_score": 4}, "2": {"session_score": 0}, "3": {"session_score": 3}, "4": {"session_score": 0}}}},

  {"name": "Session score adds to game_total; best_session_score only rises when beaten", "rule": "R16", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"game_total": 10, "best_session_score": 6}, "2": {"game_total": 3, "best_session_score": 3},
                         "3": {"game_total": 5, "best_session_score": 1}, "4": {"game_total": 0, "best_session_score": 0}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"players": {"1": {"session_score": 4, "game_total": 14, "best_session_score": 6},
                          "2": {"session_score": 0, "game_total": 3, "best_session_score": 3},
                          "3": {"session_score": 2, "game_total": 7, "best_session_score": 2},
                          "4": {"session_score": 2, "game_total": 2, "best_session_score": 2}}}},

  {"name": "After the session score a new session starts at round 5", "rule": "R17", "players": 4, "seed": 1, "rounds": 1, "default": "first",
   "given": {"game": {"round": 4, "session": 1, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"game": {"round": 5, "session": 2},
              "players": {"1": {"game_total": 4}, "2": {"game_total": 0}, "3": {"game_total": 2}, "4": {"game_total": 2}}}},

  {"name": "The game ends after round 12 and the highest game_total wins", "rule": "R18", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 12, "session": 3, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"game_total": 10, "best_session_score": 5}, "2": {"game_total": 10, "best_session_score": 5},
                         "3": {"game_total": 10, "best_session_score": 5}, "4": {"game_total": 10, "best_session_score": 5}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"winner": 1,
              "standings": {"1": 14005, "2": 10005, "3": 12005, "4": 12005},
              "players": {"1": {"game_total": 14}, "2": {"game_total": 10}, "3": {"game_total": 12}, "4": {"game_total": 12}}}},

  {"name": "Tie on game_total is broken by best_session_score", "rule": "R19", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 12, "session": 3, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"game_total": 18, "best_session_score": 7}, "2": {"game_total": 15, "best_session_score": 9},
                         "3": {"game_total": 20, "best_session_score": 9}, "4": {"game_total": 10, "best_session_score": 5}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"winner": 3,
              "standings": {"1": 22007, "2": 15009, "3": 22009, "4": 12005}}},

  {"name": "Players tied on game_total and best_session_score share the win", "rule": "R19", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 12, "session": 3, "deck": ["Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red","Red"]},
             "players": {"1": {"game_total": 18, "best_session_score": 7}, "2": {"game_total": 15, "best_session_score": 9},
                         "3": {"game_total": 20, "best_session_score": 7}, "4": {"game_total": 10, "best_session_score": 5}}},
   "rules": [{"seat": 4, "options_include": "to seat 1"}, {"seat": 2, "options_include": "to seat 1"}, {"seat": 3, "options_include": "to seat 1"}, {"seat": 1, "options_include": "to seat 2"}],
   "expect": {"winner": [1, 3],
              "standings": {"1": 22007, "2": 15009, "3": 22007, "4": 12005}}}
]
```
````
