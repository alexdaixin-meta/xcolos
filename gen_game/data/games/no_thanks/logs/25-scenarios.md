# 25 scenarios

- time: 2026-10-27T17:05:29+00:00 (36.9s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 d128817513483536, reply sha256 067a27aa08e26426

## Sent

````
SPEC:
{
  "name": "No Thanks! (Bounded Laps)",
  "summary": "Players pay one chip to refuse a card or take it with the pot. Each card may circle the table at most twice before it is burned. The lowest score, card points minus chips, wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "card_min": 3,
    "card_max": 35,
    "card_total": 33,
    "cards_removed": 13,
    "deck_size": 20,
    "starting_chips": 11,
    "pay_cost": 1,
    "laps_to_burn": 2,
    "max_rounds": 40,
    "initial_lead_seat": 1,
    "no_card_value": 0
  },
  "attributes": {
    "player": [
      {
        "key": "chips",
        "type": "number",
        "visible": "ally",
        "initial": 11,
        "meaning": "Chips in hand. Only the owner sees this. Each chip lowers the final score by 1.",
        "observable": true
      },
      {
        "key": "tableau",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Card numbers this player has taken.",
        "observable": true
      },
      {
        "key": "card_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the lowest card of each run of consecutive numbers in the tableau, kept up to date on every take.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "20 cards chosen at random from 3..35",
        "meaning": "Undrawn cards. Hidden order; only the count is announced.",
        "observable": false
      },
      {
        "key": "removed",
        "type": "list",
        "visible": "none",
        "initial": "the other 13 cards of 3..35",
        "meaning": "Cards removed unseen at setup. They stay hidden all game.",
        "observable": false
      },
      {
        "key": "current_card",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The card on offer; 0 means there is no card.",
        "observable": true
      },
      {
        "key": "pot",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Chips paid onto the current card. They carry over after a burn.",
        "observable": true
      },
      {
        "key": "lap_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Full laps in which every seat paid on the current card.",
        "observable": false
      },
      {
        "key": "lead_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The seat that receives the first offer of the round.",
        "observable": false
      },
      {
        "key": "burned",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards burned after 2 full laps. They score for no one; their count is announced.",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Rounds played, used for the 40-round bound.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Make the 33 cards numbered 3 to 35.",
    "Move 13 of them at random into the hidden table list `removed`; nobody ever sees them.",
    "The remaining 20 cards form the hidden table list `deck`.",
    "Each player gets chips = 11, an empty tableau and card_points = 0.",
    "Set current_card = 0, pot = 0, lap_count = 0, lead_seat = 1, burned = [] and round_number = 0.",
    "Seats are numbered 1 to N clockwise.",
    "Sync each player their own state, including their private chip count."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_number += 1. When current_card = 0 and deck is not empty: draw one card at random from deck (remove it from deck), set current_card to it and set lap_count = 0. The pot is unchanged."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce current_card, pot, every player's tableau and card_points, the length of deck and the length of burned."
    },
    {
      "action": "ask",
      "who": "seat lead_seat (offer 1)",
      "answer": "TAKE, or PAY if that seat has chips >= 1",
      "effect": "When current_card != 0. PAY: chips -= 1 and pot += 1. TAKE: append current_card to tableau; card_points += c, minus (c+1) if c+1 is in the tableau, minus c if c-1 is in the tableau; chips += pot; pot = 0; lead_seat = this seat; current_card = 0."
    },
    {
      "action": "ask",
      "who": "seat 1 place clockwise from lead_seat (offer 2)",
      "answer": "TAKE, or PAY if chips >= 1",
      "effect": "Same as offer 1. Runs only when current_card != 0."
    },
    {
      "action": "ask",
      "who": "seat 2 places clockwise from lead_seat (offer 3)",
      "answer": "TAKE, or PAY if chips >= 1",
      "effect": "Same as offer 1. Runs only when current_card != 0."
    },
    {
      "action": "ask",
      "who": "seat 3 places clockwise from lead_seat (offer 4)",
      "answer": "TAKE, or PAY if chips >= 1",
      "effect": "Same as offer 1. Runs only when current_card != 0 and N >= 4."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "End of lap, when current_card != 0: lap_count += 1. If lap_count = 2: append current_card to burned, set current_card = 0, keep pot, and set lead_seat = (lead_seat mod N) + 1. If lap_count = 1, nothing else changes."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce who paid and who took, or that the card was burned. Then sync each player their own chips privately."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if deck is empty and current_card = 0, or if round_number >= 40. Otherwise continue."
    }
  ],
  "ending": {
    "condition": "(len(deck) == 0 and current_card == 0) or round_number >= 40",
    "rank_by": "you.chips - you.card_points",
    "decided_by": "A player's final score is card_points minus chips, and lower is better, so each player is ranked by chips minus card_points. The highest value (the lowest final score) wins. Players level at the top share the win, which stands in for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck holds 20 distinct cards from 3..35 and the other 13 sit in the hidden removed list."
    },
    {
      "id": "R2",
      "text": "When the game starts, each player has chips = 11, an empty tableau and card_points = 0; chips are visible only to their owner."
    },
    {
      "id": "R3",
      "text": "When the game starts, current_card = 0, pot = 0, lap_count = 0, lead_seat = 1 and burned is empty."
    },
    {
      "id": "R4",
      "text": "When a round starts with current_card = 0 and a non-empty deck, then one card moves from deck to current_card, lap_count becomes 0 and the pot is unchanged."
    },
    {
      "id": "R4b",
      "text": "When a round starts with current_card != 0, then no card is drawn and the same card and pot continue."
    },
    {
      "id": "R5",
      "text": "When an offer is made, then the seat is offered TAKE, and also PAY only if its chips >= 1."
    },
    {
      "id": "R6",
      "text": "When a seat PAYs, then its chips fall by 1 and the pot rises by 1."
    },
    {
      "id": "R7",
      "text": "When a seat TAKEs card c, then c is appended to its tableau and card_points changes by c, minus (c+1) if c+1 was already held, minus c if c-1 was already held."
    },
    {
      "id": "R8",
      "text": "When a seat TAKEs, then its chips rise by the pot, the pot becomes 0, current_card becomes 0, lead_seat becomes that seat, and no further offers are made that round."
    },
    {
      "id": "R9",
      "text": "When offer k is made, then it goes to the seat k-1 places clockwise from lead_seat, for k = 1..N, and only while current_card != 0."
    },
    {
      "id": "R10",
      "text": "When a seat with 0 chips is offered the card, then its only option is TAKE."
    },
    {
      "id": "R11",
      "text": "When all N seats pay in a round and lap_count becomes 1, then the card, pot and lead_seat stay the same for the next round."
    },
    {
      "id": "R12",
      "text": "When all N seats pay and lap_count becomes 2, then the card is appended to burned, current_card becomes 0, the pot is kept and lead_seat moves one seat clockwise."
    },
    {
      "id": "R13",
      "text": "When the deck is empty and current_card = 0 at the end check, then the game ends."
    },
    {
      "id": "R14",
      "text": "When 40 rounds have been played, then the game ends."
    },
    {
      "id": "R15",
      "text": "When the game ends, then each final score is card_points minus chips, and chips left in the pot belong to no one."
    },
    {
      "id": "R16",
      "text": "When the game ends, then the player with the lowest final score wins, and players tied for lowest share the result."
    }
  ],
  "offers": [
    {
      "question": "Offer on the current card (offers 1 to N)",
      "who": "the seat k-1 places clockwise from lead_seat, while current_card != 0",
      "options": "a seat with chips >= 1: TAKE, PAY; a seat with chips = 0: TAKE"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer's count is kept. Three seats is the smallest table where pressing your luck against several rivals is tense. Four keeps each lap short and each refusal costly."
    },
    {
      "what": "No talk step",
      "why": "The rules contain no table talk. The strategy is when to pay to drive up the pot and when to take a card that extends a run; adding talk would add a mechanic."
    },
    {
      "what": "Tie-break by shared win",
      "why": "Players level at the top share the win, which is the engine's form of the source's draw."
    },
    {
      "what": "chips marked observable",
      "why": "The final score depends on chips, so an outside observer must read them, though players see only their own."
    }
  ],
  "simplifications": [
    {
      "what": "Lowest score wins, expressed as ranking by chips - card_points (highest wins)",
      "why": "The engine ranks highest first, so the score is negated."
    },
    {
      "what": "card_points kept incrementally on each take instead of recomputed from runs",
      "why": "The incremental formula in R5 equals the sum of the lowest cards of each run, and it is simple arithmetic."
    },
    {
      "what": "Four fixed offer steps, the fourth skipped when N = 3",
      "why": "The step list is flat; each offer is one ask step with an arithmetic condition."
    },
    {
      "what": "A round_number counter was added",
      "why": "It enforces the 40-round bound stated in the rules."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: chips, tableau, card_points; table: current_card, pot, burned.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
For the scenario 'A seat with 0 chips may only TAKE', do not assert that seat 1 is presented an options list including TAKE. A forced single option may be applied automatically. Assert the result after the round instead: seat 1's tableau contains the given current card; seat 1's chips equal 0 plus the given pot; pot = 0; current_card = 0; card_points updated per the run rule; lead_seat = 1. Also check that seat 1 never paid, so its chips never went below 0. Keep the given state minimal (seat 1 chips 0, a known current card and pot, lead_seat 1) so the outcome is deterministic.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "Setup: deck holds 20 cards, removed holds 13", "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 20, "removed": 13}}}},

  {"name": "Setup: each player starts with 11 chips, empty tableau, 0 card points", "rule": "R2", "players": 4, "seed": 1, "rounds": 0,
   "expect": {"players": {"1": {"chips": 11, "tableau": [], "card_points": 0},
                          "2": {"chips": 11, "tableau": [], "card_points": 0},
                          "3": {"chips": 11, "tableau": [], "card_points": 0},
                          "4": {"chips": 11, "tableau": [], "card_points": 0}}}},

  {"name": "Setup: no card on offer, empty pot, nothing burned", "rule": "R3", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"game": {"current_card": 0, "pot": 0, "burned": []}}},

  {"name": "Round start with no card draws the only deck card and keeps the pot", "rule": "R4", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 0, "pot": 3, "deck": [17], "lap_count": 0, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": "all"}, {"seat": 2, "options_include": "PAY", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": "all"}, {"seat": 4, "options_include": "PAY", "times": "all"}],
   "expect": {"game": {"current_card": 17, "pot": 7},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}, "4": {"chips": 10}},
              "lens": {"game": {"deck": 0}}}},

  {"name": "Round start with a card already on offer draws nothing", "rule": "R4b", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 2, "deck": [5, 6], "lap_count": 1, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"tableau": [20], "chips": 13, "card_points": 20}},
              "game": {"current_card": 0, "pot": 0},
              "lens": {"game": {"deck": 2}}}},

  {"name": "A seat with chips is offered both TAKE and PAY", "rule": "R5", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"offered": [{"seat": 1, "option": "TAKE"}, {"seat": 1, "option": "PAY"}]}},

  {"name": "Paying costs 1 chip and raises the pot by 1", "rule": "R6", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 10}, "2": {"chips": 12, "tableau": [20]}},
              "game": {"pot": 0, "current_card": 0}}},

  {"name": "Taking 11 between held 10 and 12 merges the runs", "rule": "R7", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"tableau": [10, 12], "card_points": 22}},
             "game": {"current_card": 11, "pot": 0, "deck": [30, 31], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"tableau": [10, 12, 11], "card_points": 10, "chips": 11}}}},

  {"name": "Taker collects the pot and no further offers are made", "rule": "R8", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 1, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"},
             {"seat": 3, "options_include": "TAKE"}, {"seat": 4, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 14, "tableau": [20], "card_points": 20},
                          "4": {"chips": 11, "tableau": []}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 4, "option": "TAKE"}]}},

  {"name": "Offers go clockwise from the lead seat (lead 3: 3, 4, 1)", "rule": "R9", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 3}},
   "rules": [{"seat": 3, "options_include": "PAY"}, {"seat": 4, "options_include": "PAY"},
             {"seat": 1, "options_include": "TAKE"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 13, "tableau": [20]}, "2": {"chips": 11, "tableau": []},
                          "3": {"chips": 10}, "4": {"chips": 10}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 2, "option": "TAKE"}]}},

  {"name": "A seat with 0 chips may only TAKE", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"chips": 0, "tableau": [], "card_points": 0}},
             "game": {"current_card": 20, "pot": 4, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "expect": {"players": {"1": {"tableau": [20], "chips": 4, "card_points": 20}, "2": {"chips": 11}, "3": {"chips": 11}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 1, "option": "PAY"}]}},

  {"name": "First full lap of pays keeps the card and grows the pot", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": "all"}, {"seat": 2, "options_include": "PAY", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": "all"}],
   "expect": {"game": {"current_card": 20, "pot": 3, "burned": []},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}},
              "lens": {"game": {"deck": 2}}}},

  {"name": "Second full lap burns the card, keeps the pot, and the next round starts at seat 2", "rule": "R12", "players": 3, "seed": 1, "rounds": 2,
   "given": {"game": {"current_card": 20, "pot": 3, "deck": [5], "lap_count": 1, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": 1}, {"seat": 1, "options_include": "TAKE", "times": "all"},
             {"seat": 2, "options_include": "PAY", "times": 1}, {"seat": 2, "options_include": "TAKE", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": 1}, {"seat": 3, "options_include": "TAKE", "times": "all"}],
   "expect": {"winner": 2,
              "standings": {"1": 10, "2": 11, "3": 10},
              "game": {"burned": [20], "current_card": 0, "pot": 0},
              "players": {"1": {"chips": 10, "tableau": []}, "2": {"chips": 16, "tableau": [5], "card_points": 5},
                          "3": {"chips": 10, "tableau": []}}}},

  {"name": "Game ends when the deck is empty and the last card is taken", "rule": "R13", "players": 3, "seed": 1,
   "given": {"game": {"current_card": 20, "pot": 2, "deck": [], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": -7, "2": 11, "3": 11},
              "players": {"1": {"chips": 13, "card_points": 20, "tableau": [20]}},
              "game": {"current_card": 0, "pot": 0}}},

  {"name": "Game ends after round 40 even with cards left", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"players": {"1": {"tableau": [30], "card_points": 30}},
             "game": {"round_number": 39, "current_card": 20, "pot": 0, "deck": [5, 6, 7], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"}, {"seat": 3, "options_include": "PAY"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": -20, "2": 10, "3": 10},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}},
              "game": {"current_card": 20, "pot": 3}}},

  {"name": "Chips left in the pot at the end belong to no one", "rule": "R15", "players": 3, "seed": 1,
   "given": {"players": {"1": {"chips": 3}},
             "game": {"current_card": 20, "pot": 5, "deck": [], "lap_count": 1, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"}, {"seat": 3, "options_include": "PAY"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": 2, "2": 10, "3": 10},
              "players": {"1": {"chips": 2}, "2": {"chips": 10}, "3": {"chips": 10}},
              "game": {"pot": 8, "burned": [20], "current_card": 0}}},

  {"name": "Lowest final score (card points minus chips) wins", "rule": "R16", "players": 3, "seed": 1,
   "given": {"players": {"1": {"chips": 5, "tableau": [10], "card_points": 10},
                         "2": {"chips": 2, "tableau": [], "card_points": 0},
                         "3": {"chips": 11, "tableau": [20], "card_points": 20}},
             "game": {"current_card": 3, "pot": 0, "deck": [], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"winner": 2,
              "standings": {"1": -8, "2": 2, "3": -9},
              "players": {"1": {"card_points": 13, "chips": 5}}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "Setup: deck holds 20 cards, removed holds 13", "rule": "R1", "players": 4, "seed": 1, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "PAY"}],
   "expect": {"lens": {"game": {"deck": 20, "removed": 13}}}},

  {"name": "Setup: each player starts with 11 chips, empty tableau, 0 card points", "rule": "R2", "players": 4, "seed": 1, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "PAY"}],
   "expect": {"players": {"1": {"chips": 11, "tableau": [], "card_points": 0},
                          "2": {"chips": 11, "tableau": [], "card_points": 0},
                          "3": {"chips": 11, "tableau": [], "card_points": 0},
                          "4": {"chips": 11, "tableau": [], "card_points": 0}}}},

  {"name": "Setup: no card on offer, empty pot, nothing burned", "rule": "R3", "players": 3, "seed": 1, "rounds": 0,
   "rules": [{"seat": 1, "options_include": "PAY"}],
   "expect": {"game": {"current_card": 0, "pot": 0, "burned": []}}},

  {"name": "Round start with no card draws the only deck card and keeps the pot", "rule": "R4", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 0, "pot": 3, "deck": [17], "lap_count": 0, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": "all"}, {"seat": 2, "options_include": "PAY", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": "all"}, {"seat": 4, "options_include": "PAY", "times": "all"}],
   "expect": {"game": {"current_card": 17, "pot": 7},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}, "4": {"chips": 10}},
              "lens": {"game": {"deck": 0}}}},

  {"name": "Round start with a card already on offer draws nothing", "rule": "R4b", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 2, "deck": [5, 6], "lap_count": 1, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"tableau": [20], "chips": 13, "card_points": 20}},
              "game": {"current_card": 0, "pot": 0},
              "lens": {"game": {"deck": 2}}}},

  {"name": "A seat with chips is offered both TAKE and PAY", "rule": "R5", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"offered": [{"seat": 1, "option": "TAKE"}, {"seat": 1, "option": "PAY"}]}},

  {"name": "Paying costs 1 chip and raises the pot by 1", "rule": "R6", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 10}, "2": {"chips": 12, "tableau": [20]}},
              "game": {"pot": 0, "current_card": 0}}},

  {"name": "Taking 11 between held 10 and 12 merges the runs", "rule": "R7", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"tableau": [10, 12], "card_points": 22}},
             "game": {"current_card": 11, "pot": 0, "deck": [30, 31], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"tableau": [10, 12, 11], "card_points": 10, "chips": 11}}}},

  {"name": "Taker collects the pot and no further offers are made", "rule": "R8", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 1, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"},
             {"seat": 3, "options_include": "TAKE"}, {"seat": 4, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 14, "tableau": [20], "card_points": 20},
                          "4": {"chips": 11, "tableau": []}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 4, "option": "TAKE"}]}},

  {"name": "Offers go clockwise from the lead seat (lead 3: 3, 4, 1)", "rule": "R9", "players": 4, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 3}},
   "rules": [{"seat": 3, "options_include": "PAY"}, {"seat": 4, "options_include": "PAY"},
             {"seat": 1, "options_include": "TAKE"}, {"seat": 2, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"chips": 13, "tableau": [20]}, "2": {"chips": 11, "tableau": []},
                          "3": {"chips": 10}, "4": {"chips": 10}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 2, "option": "TAKE"}]}},

  {"name": "A seat with 0 chips may only TAKE", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"chips": 0, "tableau": [], "card_points": 0}},
             "game": {"current_card": 20, "pot": 4, "deck": [5, 6], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"players": {"1": {"tableau": [20], "chips": 4, "card_points": 20}, "2": {"chips": 11}, "3": {"chips": 11}},
              "game": {"pot": 0, "current_card": 0},
              "not_offered": [{"seat": 1, "option": "PAY"}]}},

  {"name": "First full lap of pays keeps the card and grows the pot", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
   "given": {"game": {"current_card": 20, "pot": 0, "deck": [5, 6], "lap_count": 0, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": "all"}, {"seat": 2, "options_include": "PAY", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": "all"}],
   "expect": {"game": {"current_card": 20, "pot": 3, "burned": []},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}},
              "lens": {"game": {"deck": 2}}}},

  {"name": "Second full lap burns the card, keeps the pot, and the next round starts at seat 2", "rule": "R12", "players": 3, "seed": 1, "rounds": 2,
   "given": {"game": {"current_card": 20, "pot": 3, "deck": [5], "lap_count": 1, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY", "times": 1}, {"seat": 1, "options_include": "TAKE", "times": "all"},
             {"seat": 2, "options_include": "PAY", "times": 1}, {"seat": 2, "options_include": "TAKE", "times": "all"},
             {"seat": 3, "options_include": "PAY", "times": 1}, {"seat": 3, "options_include": "TAKE", "times": "all"}],
   "expect": {"winner": 2,
              "standings": {"1": 10, "2": 11, "3": 10},
              "game": {"burned": [20], "current_card": 0, "pot": 0},
              "players": {"1": {"chips": 10, "tableau": []}, "2": {"chips": 16, "tableau": [5], "card_points": 5},
                          "3": {"chips": 10, "tableau": []}}}},

  {"name": "Game ends when the deck is empty and the last card is taken", "rule": "R13", "players": 3, "seed": 1,
   "given": {"game": {"current_card": 20, "pot": 2, "deck": [], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": -7, "2": 11, "3": 11},
              "players": {"1": {"chips": 13, "card_points": 20, "tableau": [20]}},
              "game": {"current_card": 0, "pot": 0}}},

  {"name": "Game ends after round 40 even with cards left", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"players": {"1": {"tableau": [30], "card_points": 30}},
             "game": {"round_number": 39, "current_card": 20, "pot": 0, "deck": [5, 6, 7], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"}, {"seat": 3, "options_include": "PAY"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": -20, "2": 10, "3": 10},
              "players": {"1": {"chips": 10}, "2": {"chips": 10}, "3": {"chips": 10}},
              "game": {"current_card": 20, "pot": 3}}},

  {"name": "Chips left in the pot at the end belong to no one", "rule": "R15", "players": 3, "seed": 1,
   "given": {"players": {"1": {"chips": 3}},
             "game": {"current_card": 20, "pot": 5, "deck": [], "lap_count": 1, "lead_seat": 1, "burned": []}},
   "rules": [{"seat": 1, "options_include": "PAY"}, {"seat": 2, "options_include": "PAY"}, {"seat": 3, "options_include": "PAY"}],
   "expect": {"winner": [2, 3],
              "standings": {"1": 2, "2": 10, "3": 10},
              "players": {"1": {"chips": 2}, "2": {"chips": 10}, "3": {"chips": 10}},
              "game": {"pot": 8, "burned": [20], "current_card": 0}}},

  {"name": "Lowest final score (card points minus chips) wins", "rule": "R16", "players": 3, "seed": 1,
   "given": {"players": {"1": {"chips": 5, "tableau": [10], "card_points": 10},
                         "2": {"chips": 2, "tableau": [], "card_points": 0},
                         "3": {"chips": 11, "tableau": [20], "card_points": 20}},
             "game": {"current_card": 3, "pot": 0, "deck": [], "lap_count": 0, "lead_seat": 1}},
   "rules": [{"seat": 1, "options_include": "TAKE"}],
   "expect": {"winner": 2,
              "standings": {"1": -8, "2": 2, "3": -9},
              "players": {"1": {"card_points": 13, "chips": 5}}}}
]
```
````
