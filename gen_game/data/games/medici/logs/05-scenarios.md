# 05 scenarios

- time: 2026-10-27T18:18:28+00:00 (141.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 e1ace13e5fdb02a0, reply sha256 6709ac364de22f88

## Sent

````
SPEC:
{
  "name": "Medici: Secret Patrons",
  "summary": "Three merchants auction lots of commodity cards from a dock over 3 days of 9 rounds. They score for ship value, for commodity track majorities and a second time for majorities in their own secret Patron commodity. The most florins wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "starting_florins": 30,
    "ship_capacity": 5,
    "days": 3,
    "rounds_per_day": 9,
    "dock_size": 3,
    "max_lot_size": 3,
    "min_lot_size": 1,
    "min_bid": 1,
    "deck_size": 30,
    "commodities": 3,
    "cards_per_commodity": 10,
    "card_value_min": 0,
    "card_value_max": 5,
    "copies_of_value_0_per_commodity": 1,
    "copies_of_value_1_per_commodity": 2,
    "copies_of_value_2_per_commodity": 2,
    "copies_of_value_3_per_commodity": 2,
    "copies_of_value_4_per_commodity": 2,
    "copies_of_value_5_per_commodity": 1,
    "track_start": 0,
    "track_max": 10,
    "ship_prize_first": 20,
    "ship_prize_second": 10,
    "majority_prize_first": 10,
    "majority_prize_second": 5,
    "patron_multiplier_extra": 1
  },
  "attributes": {
    "player": [
      {
        "key": "florins",
        "type": "number",
        "visible": "public",
        "initial": 30,
        "meaning": "Money, and also the score.",
        "observable": true
      },
      {
        "key": "patron",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The secret Patron commodity (Spice, Silk or Grain). Each player holds a different one. It is revealed at game end.",
        "observable": false
      },
      {
        "key": "ship",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards loaded on the ship this day, written as 'Commodity-value', e.g. 'Silk-3'.",
        "observable": false
      },
      {
        "key": "ship_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards on the ship (at most 5).",
        "observable": false
      },
      {
        "key": "ship_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the values of the cards on the ship.",
        "observable": false
      },
      {
        "key": "track_spice",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Spice commodity track, 0 to 10, never reset.",
        "observable": true
      },
      {
        "key": "track_silk",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Silk commodity track, 0 to 10, never reset.",
        "observable": true
      },
      {
        "key": "track_grain",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Grain commodity track, 0 to 10, never reset.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The face-down deck of the cards remaining this day.",
        "observable": false
      },
      {
        "key": "dock",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up Dock cards in order first, second, third.",
        "observable": false
      },
      {
        "key": "day",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current day, 1 to 3. It becomes 4 when the game is over.",
        "observable": true
      },
      {
        "key": "round_in_day",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Round number within the day, 1 to 9.",
        "observable": false
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the active player this round (1=A, 2=B, 3=C).",
        "observable": false
      },
      {
        "key": "lot",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards in the current lot (the first lot_size Dock cards).",
        "observable": false
      },
      {
        "key": "lot_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the current lot.",
        "observable": false
      },
      {
        "key": "lot_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the card values in the current lot.",
        "observable": false
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current highest bid in this auction (0 = no bid yet).",
        "observable": false
      },
      {
        "key": "high_bidder",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of the current highest bidder (0 = nobody).",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are fixed in order A (seat 1), B (seat 2), C (seat 3).",
    "Every player gets florins = 30, all three tracks = 0, an empty ship, ship_count = 0 and ship_value = 0.",
    "The three commodities Spice, Silk and Grain are shuffled, and one is dealt secretly into each player's patron. Every player has a different Patron and sees only their own.",
    "day = 1 and round_in_day = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_day == 1 (start of a day): set deck to all 30 cards (Spice, Silk and Grain, each valued 0,1,1,2,2,3,3,4,4,5). Empty every ship and set ship_count = 0 and ship_value = 0 for all players (tracks are NOT reset). Empty dock, then draw 3 cards at random from deck, removing them, and append them in order to dock."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "active_seat = ((day - 1) + (round_in_day - 1)) mod 3 + 1. high_bid = 0, high_bidder = 0, lot = [], lot_size = 0, lot_value = 0."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce day, round_in_day, active_seat, the dock in order, and every player's ship, ship_value, track_spice, track_silk, track_grain and florins."
    },
    {
      "action": "ask",
      "who": "the seat equal to active_seat",
      "answer": "a whole number from 1 to min(3, length of dock)",
      "effect": "lot_size = answer. lot = the first lot_size cards of dock. lot_value = sum of the values of the cards in lot. Announce the lot."
    },
    {
      "action": "ask",
      "who": "each player in turn: seat active_seat+1, then seat active_seat+2, then active_seat (seats counted mod 3)",
      "answer": "0 to pass, or a whole number at least max(1, high_bid + 1) and at most own florins. A seat with ship_count + lot_size > 5, or with florins <= high_bid, may only answer 0",
      "effect": "If answer > 0: high_bid = answer, high_bidder = this seat. Each later bidder hears the earlier bids."
    },
    {
      "action": "update",
      "who": "the seat equal to high_bidder",
      "answer": null,
      "effect": "If high_bidder > 0: that player's florins -= high_bid. Append every card of lot to their ship. ship_count += lot_size. ship_value += lot_value. For each commodity, add the number of lot cards of that commodity to the matching track, capped at 10. Whether or not anyone bid, remove the lot cards from dock (if nobody bid they are discarded)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Refill dock: while length of dock < 3 and deck is not empty, draw a random card from deck (remove it) and append it to the end of dock."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce who won the lot and for how much (high_bidder, high_bid), or that everyone passed and the lot was discarded."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_day == 9, ship scoring. Only players with ship_count > 0 take part. For each such player, h = number of participants with a higher ship_value and e = number of participants with an equal ship_value (self included). The player occupies places h+1 to h+e. Prizes are place 1 = 20, place 2 = 10, place 3 = 0. florins += floor((sum of the prizes for places h+1..h+e) / e). Players with ship_count == 0 get nothing."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round_in_day == 9, for each commodity in Spice, Silk, Grain: only players with that track > 0 take part. For each such player, h = participants with a higher track and e = participants with an equal track (self included). Prizes are place 1 = 10, place 2 = 5, place 3 = 0. award = floor((sum of the prizes for places h+1..h+e) / e) and florins += award. If that commodity equals the player's patron, florins += award again (Patron bonus)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round_in_day += 1. If round_in_day > 9: day += 1 and round_in_day = 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When day > 3: reveal every player's patron and announce final florins."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If day > 3, end the game. Otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "day > 3",
    "rank_by": "you.florins",
    "decided_by": "After the day 3 end-of-day scoring, each player's standing is their florins. The player with the most florins wins. Players tied for the most share the top, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has 30 florins, all three tracks at 0, an empty ship, and a secret patron that differs from the other two players' patrons."
    },
    {
      "id": "R2",
      "text": "When a day starts (round_in_day == 1), then the deck is reset to the 30 cards, every ship is emptied with ship_count 0 and ship_value 0, tracks keep their values, and the dock holds 3 cards drawn from the deck."
    },
    {
      "id": "R3",
      "text": "When it is day d and round r of that day, then active_seat = ((d-1)+(r-1)) mod 3 + 1, so A is active first on day 1, B on day 2 and C on day 3."
    },
    {
      "id": "R4",
      "text": "When the active player chooses a lot size, then it is 1, 2 or 3 and no more than the number of dock cards, and the lot is the first that many dock cards."
    },
    {
      "id": "R5",
      "text": "When the auction runs, then the seat after the active seat bids first, then the other non-active seat, then the active seat last, each exactly once."
    },
    {
      "id": "R6",
      "text": "When a player bids, then the bid is at least 1, higher than the current high_bid, and at most their florins. Otherwise they pass (answer 0)."
    },
    {
      "id": "R7",
      "text": "When a player's ship_count + lot_size > 5, then that player may only pass."
    },
    {
      "id": "R8",
      "text": "When at least one player bid, then the highest bidder loses exactly high_bid florins, and their ship gains every lot card, ship_count rises by lot_size and ship_value rises by lot_value."
    },
    {
      "id": "R9",
      "text": "When a player loads a card, then their track in that card's commodity rises by 1, but never above 10."
    },
    {
      "id": "R10",
      "text": "When every player passes, then the lot is discarded and no florins, ships or tracks change."
    },
    {
      "id": "R11",
      "text": "When a lot is resolved, then its cards leave the dock, the remaining dock cards keep their order, and the dock is refilled to 3 from the deck, or fewer if the deck is empty."
    },
    {
      "id": "R12",
      "text": "When round 9 of a day ends, then among players with non-empty ships the highest ship_value gains 20 florins and the second gains 10."
    },
    {
      "id": "R13",
      "text": "When players tie in ship scoring, then they add the prizes of the places they occupy and each gets the sum divided equally, rounded down: two tied first get 15 each, three tied first get 10 each, two tied second get 5 each."
    },
    {
      "id": "R14",
      "text": "When a player's ship is empty at end of day, then they get no ship prize."
    },
    {
      "id": "R15",
      "text": "When round 9 of a day ends, then for each commodity the highest track (above 0) gains 10 florins and the second highest gains 5, with ties split as in R13 (two tied first get 7 each, two tied second get 2 each, three tied first get 5 each)."
    },
    {
      "id": "R16",
      "text": "When a player's track in a commodity is 0, then they earn no majority award in that commodity."
    },
    {
      "id": "R17",
      "text": "When a player earns a majority award in the commodity equal to their patron, then they gain that same amount again."
    },
    {
      "id": "R18",
      "text": "When the day 3 scoring is done, then the patrons are revealed and the game ends."
    },
    {
      "id": "R19",
      "text": "When the game ends, then the player with the most florins wins, and players tied for the most share the result (a draw)."
    }
  ],
  "offers": [
    {
      "question": "Lot size",
      "who": "the active seat only",
      "options": "the whole numbers 1 to min(3, number of dock cards). With a full dock this is 1, 2 or 3."
    },
    {
      "question": "Auction bid",
      "who": "each seat once, starting after the active seat and ending with the active seat",
      "options": "a seat with ship_count + lot_size <= 5 and florins > high_bid: 0 (pass) or any whole number from max(1, high_bid+1) to its florins. A seat whose ship lacks room, or whose florins do not exceed high_bid: 0 (pass) only."
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed 3 seats. The game needs exactly three different Patrons for the three commodities, so the count cannot change. The strategy lies in reading rivals' Patrons from their bidding and hiding your own while still building your Patron track."
    },
    {
      "what": "No free-text talk step",
      "why": "The source rules have no negotiation phase. Adding talk would be a new mechanic."
    },
    {
      "what": "A pass is answered as bid 0",
      "why": "This keeps the bid as one whole-number answer. 0 can never be a legal bid because the minimum is 1."
    },
    {
      "what": "Players with an empty ship, or a track at 0, are left out of the ranking and occupy no place",
      "why": "The source says they earn nothing but does not say whether they occupy a place. Leaving them out lets the other players take the prizes in order."
    },
    {
      "what": "Third place earns 0 in the tie-split arithmetic",
      "why": "Only first and second prizes exist, so a place beyond second contributes 0 to a tied group's sum."
    },
    {
      "what": "Cards are written as 'Commodity-value' text in lists",
      "why": "This lets one card carry both its commodity, for tracks, and its value, for ship_value."
    },
    {
      "what": "The card value list is given as separate copy-count parameters",
      "why": "Parameters must each be a single number. The values 0,1,1,2,2,3,3,4,4,5 are written as how many copies of each value every commodity has."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most florins is a shared win at the top, not a separate draw",
      "why": "The engine has no draw outcome. Tied leaders sharing the win expresses the same result."
    },
    {
      "what": "Start-of-day and end-of-day work are single updates with a round_in_day condition",
      "why": "The engine runs one flat round list. Each conditional step is a single arithmetic update, not a separate block."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: florins, track_spice, track_silk, track_grain; table: day.
````

## Reply

````
```json
[
  {
    "name": "Game start: 30 florins, all tracks at 0, empty ships",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"florins": 30, "track_spice": 0, "track_silk": 0, "track_grain": 0},
        "2": {"florins": 30, "track_spice": 0, "track_silk": 0, "track_grain": 0},
        "3": {"florins": 30, "track_spice": 0, "track_silk": 0, "track_grain": 0}
      },
      "game": {"day": 1},
      "lens": {"players": {"1": {"ship": 0}, "2": {"ship": 0}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Day start resets the deck, empties ships, keeps tracks and deals a dock of 3 (all pass, lot of 1 discarded)",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"track_spice": 4, "ship": ["Silk-3", "Spice-2"], "ship_count": 2, "ship_value": 5},
        "2": {"track_grain": 2}
      },
      "game": {"day": 1, "round_in_day": 1}
    },
    "rules": [{"seat": 1, "options_include": 1}],
    "expect": {
      "players": {
        "1": {"florins": 30, "track_spice": 4, "track_silk": 0, "track_grain": 0},
        "2": {"florins": 30, "track_grain": 2},
        "3": {"florins": 30}
      },
      "lens": {"game": {"deck": 26, "dock": 3}, "players": {"1": {"ship": 0}}}
    }
  },
  {
    "name": "Day 2 round 1: seat 2 is active and chooses the lot, then bids last",
    "rule": "R3",
    "players": 3,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"day": 2, "round_in_day": 1}},
    "rules": [
      {"seat": 2, "options_include": 3},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "players": {"1": {"florins": 30}, "2": {"florins": 25}, "3": {"florins": 30}},
      "lens": {"players": {"2": {"ship": 3}}}
    }
  },
  {
    "name": "Day 3 round 1: seat 3 is active and chooses the lot, then bids last",
    "rule": "R3",
    "players": 3,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"day": 3, "round_in_day": 1}},
    "rules": [
      {"seat": 3, "options_include": 2},
      {"seat": 3, "options_include": 4}
    ],
    "expect": {
      "players": {"1": {"florins": 30}, "2": {"florins": 30}, "3": {"florins": 26}},
      "lens": {"players": {"3": {"ship": 2}}}
    }
  },
  {
    "name": "Lot size is capped by the dock length (2 cards) and takes the first dock cards",
    "rule": "R4",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"florins": 2}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-1", "Silk-4"], "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 4}
    ],
    "expect": {
      "players": {
        "1": {"florins": 2},
        "2": {"florins": 26, "track_spice": 1, "track_silk": 1, "track_grain": 0}
      },
      "offered": [{"seat": 1, "option": 2}],
      "not_offered": [{"seat": 1, "option": 3}]
    }
  },
  {
    "name": "Lot of 1 is only the first dock card",
    "rule": "R4",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Grain-3", "Spice-2", "Silk-5"], "deck": ["Spice-0", "Silk-1"]}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 2}
    ],
    "expect": {
      "players": {"2": {"florins": 28, "track_grain": 1, "track_spice": 0, "track_silk": 0}}
    }
  },
  {
    "name": "Auction order with seat 1 active: seat 2, then seat 3, then seat 1",
    "rule": "R5",
    "players": 3,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-2", "Silk-1", "Grain-3"], "deck": ["Spice-0", "Silk-3"]}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 5},
      {"seat": 3, "options_include": 6},
      {"seat": 1, "options_include": 7}
    ],
    "expect": {
      "players": {
        "1": {"florins": 23, "track_spice": 1},
        "2": {"florins": 30, "track_spice": 0},
        "3": {"florins": 30, "track_spice": 0}
      }
    }
  },
  {
    "name": "Auction order with seat 3 active: seat 1, then seat 2, then seat 3",
    "rule": "R5",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "decline",
    "given": {
      "game": {"day": 1, "round_in_day": 3, "active_seat": 3, "dock": ["Silk-2", "Spice-1", "Grain-3"], "deck": ["Spice-0", "Silk-3"]}
    },
    "rules": [
      {"seat": 3, "options_include": 1},
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 5}
    ],
    "expect": {
      "players": {
        "1": {"florins": 30},
        "2": {"florins": 30},
        "3": {"florins": 25, "track_silk": 1}
      }
    }
  },
  {
    "name": "Bids must exceed the high bid and not exceed own florins; a seat whose florins do not exceed the high bid may only pass",
    "rule": "R6",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"florins": 12}, "3": {"florins": 8}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Silk-2", "Spice-1", "Grain-3"], "deck": ["Spice-0", "Silk-3"]}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 10}
    ],
    "expect": {
      "players": {
        "1": {"florins": 12},
        "2": {"florins": 20, "track_silk": 1},
        "3": {"florins": 8}
      },
      "offered": [{"seat": 1, "option": 12}],
      "not_offered": [
        {"seat": 1, "option": 13},
        {"seat": 3, "option": 8},
        {"seat": 3, "option": 1}
      ]
    }
  },
  {
    "name": "A seat whose ship lacks room for the lot may only pass",
    "rule": "R7",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "2": {"ship": ["Spice-1", "Spice-1", "Silk-2", "Grain-0"], "ship_count": 4, "ship_value": 4, "track_spice": 2, "track_silk": 1, "track_grain": 1}
      },
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Grain-4", "Grain-1", "Spice-3"], "deck": ["Spice-0", "Silk-3"]}
    },
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "players": {
        "2": {"florins": 30, "track_spice": 2, "track_silk": 1, "track_grain": 1},
        "3": {"florins": 27, "track_grain": 2, "track_spice": 0, "track_silk": 0}
      },
      "not_offered": [{"seat": 2, "option": 1}]
    }
  },
  {
    "name": "The winning bidder pays exactly the high bid and loads every lot card",
    "rule": "R8",
    "players": 3,
    "seed": 11,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"3": {"ship": ["Grain-2"], "ship_count": 1, "ship_value": 2, "track_grain": 1}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-3", "Silk-4", "Grain-5"], "deck": ["Spice-0", "Silk-1", "Grain-2"]}
    },
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 3, "options_include": 9}
    ],
    "expect": {
      "players": {
        "1": {"florins": 30},
        "2": {"florins": 30},
        "3": {"florins": 21, "track_spice": 1, "track_silk": 1, "track_grain": 2}
      },
      "lens": {"players": {"3": {"ship": 4}}}
    }
  },
  {
    "name": "Tracks rise by 1 per loaded card but are capped at 10",
    "rule": "R9",
    "players": 3,
    "seed": 12,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"2": {"track_spice": 9}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-1", "Spice-2", "Silk-0"], "deck": ["Grain-0", "Silk-1", "Grain-2"]}
    },
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": 1}
    ],
    "expect": {
      "players": {"2": {"florins": 29, "track_spice": 10, "track_silk": 1, "track_grain": 0}}
    }
  },
  {
    "name": "When everyone passes, the lot is discarded and nothing else changes",
    "rule": "R10",
    "players": 3,
    "seed": 13,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {"1": {"track_spice": 2}, "3": {"track_grain": 3}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-3", "Silk-4", "Grain-5"], "deck": ["Spice-0", "Silk-1", "Grain-2", "Spice-4", "Silk-5"]}
    },
    "rules": [{"seat": 1, "options_include": 2}],
    "expect": {
      "players": {
        "1": {"florins": 30, "track_spice": 2, "track_silk": 0, "track_grain": 0},
        "2": {"florins": 30, "track_spice": 0, "track_silk": 0, "track_grain": 0},
        "3": {"florins": 30, "track_spice": 0, "track_silk": 0, "track_grain": 3}
      },
      "lens": {
        "game": {"dock": 3, "deck": 3},
        "players": {"1": {"ship": 0}, "2": {"ship": 0}, "3": {"ship": 0}}
      }
    }
  },
  {
    "name": "Resolved lot cards leave the dock, the rest keep their order, and an empty deck refills nothing",
    "rule": "R11",
    "players": 3,
    "seed": 14,
    "rounds": 2,
    "default": "decline",
    "given": {
      "players": {"2": {"florins": 0}},
      "game": {"day": 1, "round_in_day": 4, "active_seat": 1, "dock": ["Spice-1", "Silk-2", "Grain-3"], "deck": []}
    },
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 1},
      {"seat": 3, "options_include": 1, "times": 2}
    ],
    "expect": {
      "players": {"3": {"florins": 28, "track_spice": 1, "track_silk": 1, "track_grain": 0}},
      "lens": {"game": {"dock": 1}}
    }
  },
  {
    "name": "End of day ship scoring: highest ship value +20, second +10",
    "rule": "R12",
    "players": 3,
    "seed": 15,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"ship": ["Spice-5", "Silk-5"], "ship_count": 2, "ship_value": 10},
        "2": {"ship": ["Grain-4", "Silk-3"], "ship_count": 2, "ship_value": 7},
        "3": {"ship": ["Spice-3"], "ship_count": 1, "ship_value": 3}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 50}, "2": {"florins": 40}, "3": {"florins": 30}},
      "game": {"day": 2}
    }
  },
  {
    "name": "Ship scoring tie for first: two tied first get 15 each, third gets 0",
    "rule": "R13",
    "players": 3,
    "seed": 16,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"ship": ["Spice-4", "Silk-4"], "ship_count": 2, "ship_value": 8},
        "2": {"ship": ["Grain-5", "Silk-3"], "ship_count": 2, "ship_value": 8},
        "3": {"ship": ["Spice-2"], "ship_count": 1, "ship_value": 2}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 45}, "2": {"florins": 45}, "3": {"florins": 30}}
    }
  },
  {
    "name": "Ship scoring tie for second: two tied second get 5 each",
    "rule": "R13",
    "players": 3,
    "seed": 17,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"ship": ["Spice-5", "Silk-4"], "ship_count": 2, "ship_value": 9},
        "2": {"ship": ["Grain-4"], "ship_count": 1, "ship_value": 4},
        "3": {"ship": ["Spice-3", "Silk-1"], "ship_count": 2, "ship_value": 4}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 50}, "2": {"florins": 35}, "3": {"florins": 35}}
    }
  },
  {
    "name": "Ship scoring three-way tie for first: 10 each",
    "rule": "R13",
    "players": 3,
    "seed": 18,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"ship": ["Spice-3"], "ship_count": 1, "ship_value": 3},
        "2": {"ship": ["Grain-2", "Silk-1"], "ship_count": 2, "ship_value": 3},
        "3": {"ship": ["Silk-3"], "ship_count": 1, "ship_value": 3}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 40}, "2": {"florins": 40}, "3": {"florins": 40}}
    }
  },
  {
    "name": "An empty ship earns no ship prize and takes no place; a ship worth 0 still places second",
    "rule": "R14",
    "players": 3,
    "seed": 19,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"ship": ["Spice-5"], "ship_count": 1, "ship_value": 5},
        "2": {"ship": ["Grain-0"], "ship_count": 1, "ship_value": 0},
        "3": {"ship": [], "ship_count": 0, "ship_value": 0}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 50}, "2": {"florins": 40}, "3": {"florins": 30}}
    }
  },
  {
    "name": "Majority scoring with ties and no patron bonus earned",
    "rule": "R15",
    "players": 3,
    "seed": 20,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"patron": "Silk", "track_spice": 6, "track_silk": 0, "track_grain": 4},
        "2": {"patron": "Grain", "track_spice": 2, "track_silk": 3, "track_grain": 0},
        "3": {"patron": "Spice", "track_spice": 0, "track_silk": 3, "track_grain": 4}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {
        "1": {"florins": 47, "track_spice": 6, "track_grain": 4},
        "2": {"florins": 42},
        "3": {"florins": 44}
      }
    }
  },
  {
    "name": "Majority scoring: two tied second get 2 each, three tied first get 5 each (patron bonuses included)",
    "rule": "R15",
    "players": 3,
    "seed": 21,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"patron": "Silk", "track_spice": 5, "track_silk": 0, "track_grain": 1},
        "2": {"patron": "Spice", "track_spice": 3, "track_silk": 0, "track_grain": 1},
        "3": {"patron": "Grain", "track_spice": 3, "track_silk": 0, "track_grain": 1}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 45}, "2": {"florins": 39}, "3": {"florins": 42}}
    }
  },
  {
    "name": "A track at 0 earns no majority award and takes no place",
    "rule": "R16",
    "players": 3,
    "seed": 22,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"patron": "Silk", "track_spice": 3, "track_silk": 0, "track_grain": 0},
        "2": {"patron": "Spice", "track_spice": 0, "track_silk": 0, "track_grain": 2},
        "3": {"patron": "Grain", "track_spice": 0, "track_silk": 0, "track_grain": 0}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 40}, "2": {"florins": 40}, "3": {"florins": 30}}
    }
  },
  {
    "name": "Patron bonus doubles the majority award in the patron commodity (first and second place)",
    "rule": "R17",
    "players": 3,
    "seed": 23,
    "rounds": 1,
    "default": "decline",
    "given": {
      "players": {
        "1": {"patron": "Grain", "track_spice": 4, "track_silk": 0, "track_grain": 0},
        "2": {"patron": "Spice", "track_spice": 1, "track_silk": 0, "track_grain": 0},
        "3": {"patron": "Silk", "track_spice": 0, "track_silk": 2, "track_grain": 0}
      },
      "game": {"day": 1, "round_in_day": 9, "active_seat": 3, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 3, "options_include": 1}],
    "expect": {
      "players": {"1": {"florins": 40}, "2": {"florins": 40}, "3": {"florins": 50}}
    }
  },
  {
    "name": "After the day 3 scoring the game ends with day 4; all level, all share the win",
    "rule": "R18",
    "players": 3,
    "seed": 24,
    "default": "decline",
    "given": {
      "game": {"day": 3, "round_in_day": 9, "active_seat": 2, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 2, "options_include": 1}],
    "expect": {
      "winner": [1, 2, 3],
      "standings": {"1": 30, "2": 30, "3": 30},
      "game": {"day": 4}
    }
  },
  {
    "name": "The most florins after the final scoring wins",
    "rule": "R19",
    "players": 3,
    "seed": 25,
    "default": "decline",
    "given": {
      "players": {
        "1": {"florins": 40, "ship": ["Spice-3"], "ship_count": 1, "ship_value": 3},
        "2": {"florins": 25, "ship": ["Silk-5", "Grain-4"], "ship_count": 2, "ship_value": 9},
        "3": {"florins": 35, "ship": [], "ship_count": 0, "ship_value": 0}
      },
      "game": {"day": 3, "round_in_day": 9, "active_seat": 2, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 2, "options_include": 1}],
    "expect": {
      "winner": 1,
      "standings": {"1": 50, "2": 45, "3": 35}
    }
  },
  {
    "name": "Players tied for the most florins share the win",
    "rule": "R19",
    "players": 3,
    "seed": 26,
    "default": "decline",
    "given": {
      "players": {
        "1": {"florins": 30, "ship": ["Spice-5", "Silk-5"], "ship_count": 2, "ship_value": 10},
        "2": {"florins": 40, "ship": [], "ship_count": 0, "ship_value": 0},
        "3": {"florins": 50, "ship": [], "ship_count": 0, "ship_value": 0}
      },
      "game": {"day": 3, "round_in_day": 9, "active_seat": 2, "dock": ["Grain-0", "Grain-1", "Spice-0"], "deck": ["Silk-1", "Grain-2"]}
    },
    "rules": [{"seat": 2, "options_include": 1}],
    "expect": {
      "winner": [1, 3],
      "standings": {"1": 50, "2": 40, "3": 50}
    }
  }
]
```
````
