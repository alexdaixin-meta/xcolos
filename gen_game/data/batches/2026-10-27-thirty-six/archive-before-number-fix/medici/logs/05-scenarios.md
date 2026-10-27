# 05 scenarios

- time: 2026-10-27T16:42:27+00:00 (119.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 7a0b0f5baeda7cf2, reply sha256 82471b731a908ff8

## Sent

````
SPEC:
{
  "name": "Medici: Sealed Ledgers",
  "summary": "Over 3 days the active player picks a lot of 1 to 3 revealed goods cards, everyone bids for it in a sealed auction, the best ships each day are paid, and at the end good majorities and secret favoured goods are paid. Most florins wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "starting_florins": 40,
    "goods_count": 4,
    "cards_per_good": 12,
    "deck_size": 48,
    "value_0_copies_per_good": 1,
    "value_1_copies_per_good": 2,
    "value_2_copies_per_good": 2,
    "value_3_copies_per_good": 3,
    "value_4_copies_per_good": 2,
    "value_5_copies_per_good": 2,
    "days": 3,
    "rounds_per_day_per_player": 2,
    "total_rounds_per_player": 6,
    "cards_revealed_per_round": 3,
    "min_lot_size": 1,
    "max_lot_size": 3,
    "ship_capacity": 5,
    "min_bid": 0,
    "day_first_prize": 15,
    "day_second_prize": 7,
    "day_tied_first_pool": 22,
    "majority_prize": 10,
    "favoured_per_card": 3,
    "rank_florins_weight": 1000
  },
  "attributes": {
    "player": [
      {
        "key": "florins",
        "type": "number",
        "visible": "ally",
        "initial": 40,
        "meaning": "Florins held. This is the score, and only its owner sees it.",
        "observable": true
      },
      {
        "key": "favoured_good",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Secret favoured good (Grain, Cloth, Spice or Dye). Every player has a different one, and it is revealed at game end.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid. It is set to 0 if the bid is invalid.",
        "observable": false
      },
      {
        "key": "ship_cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards loaded on the ship today.",
        "observable": false
      },
      {
        "key": "ship_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the card values on the ship today.",
        "observable": false
      },
      {
        "key": "ship_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards on the ship today (at most 5).",
        "observable": true
      },
      {
        "key": "grain_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Grain cards collected over the whole game.",
        "observable": false
      },
      {
        "key": "cloth_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cloth cards collected over the whole game.",
        "observable": false
      },
      {
        "key": "spice_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Spice cards collected over the whole game.",
        "observable": false
      },
      {
        "key": "dye_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Dye cards collected over the whole game.",
        "observable": false
      },
      {
        "key": "total_cards",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total cards collected over the game. This is the tie-break.",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "48 cards: Grain-0, Grain-1, Grain-1, Grain-2, Grain-2, Grain-3, Grain-3, Grain-3, Grain-4, Grain-4, Grain-5, Grain-5, and the same 12 values for Cloth, Spice and Dye",
        "meaning": "Today's shuffled deck. A draw takes a card at random.",
        "observable": false
      },
      {
        "key": "revealed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards A, B and C revealed this round, in order.",
        "observable": false
      },
      {
        "key": "lot",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The cards on offer this round.",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Today's unchosen revealed cards and unsold lots.",
        "observable": false
      },
      {
        "key": "lot_size",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in the lot (1 to 3).",
        "observable": false
      },
      {
        "key": "lot_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the card values in the lot.",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Round number, from 1 to 6N.",
        "observable": true
      },
      {
        "key": "day",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current day, from 1 to 3.",
        "observable": true
      },
      {
        "key": "active_seat",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The active player, equal to ((round-1) mod N)+1.",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won this round's lot (0 if nobody did).",
        "observable": false
      },
      {
        "key": "price_paid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Winning bid paid this round.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player gets 40 florins, which only that player can see.",
    "The four goods Grain, Cloth, Spice and Dye are shuffled. Each player is secretly dealt a different one as favoured_good, without replacement.",
    "Seats are numbered 1 to N. round=1, day=1 and active_seat=1.",
    "Ship cards, ship_value, ship_count, the four good counts and total_cards all start empty or at 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If round mod (2N) == 1 (first round of a day), deck is rebuilt as all 48 cards, discard is emptied, and every ship_cards, ship_value and ship_count is reset to empty or 0. Then active_seat = ((round-1) mod N)+1, and winner_seat and price_paid are set to 0."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "Three cards are drawn at random from deck, in order, into revealed as cards A, B and C, and removed from deck."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Day {day}, round {round}: the active seat is {active_seat}. The revealed cards A, B, C are {revealed}."
    },
    {
      "action": "ask",
      "who": "the active seat",
      "answer": "a choice: 1, 2 or 3",
      "effect": "lot_size is set to the choice. lot = the first lot_size cards of revealed, and lot_value is set to the sum of their values. The remaining revealed cards are appended to discard, and revealed is emptied."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "The lot is {lot} ({lot_size} cards, total value {lot_value})."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to your own florins (0 is a pass)",
      "effect": "Each player's bid is set to their answer. Bids stay hidden from the other players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player: if ship_count + lot_size > 5, then bid is set to 0."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "If every bid is 0, the lot is appended to discard and winner_seat stays 0. Otherwise winner_seat is the seat with the highest bid, with ties broken by priority = N - ((seat - active_seat + N) mod N). This makes the active seat highest, then the seats after it in order. price_paid is set to the winner's bid."
    },
    {
      "action": "update",
      "who": "the winner",
      "answer": null,
      "effect": "If winner_seat > 0: the winner loses price_paid florins, the lot is appended to their ship_cards, ship_value rises by lot_value, ship_count rises by lot_size, and total_cards rises by lot_size. grain_count, cloth_count, spice_count and dye_count each rise by the number of lot cards of that good. lot is then emptied."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Winner: seat {winner_seat} paid {price_paid} florins (seat 0 means the lot was discarded). Ship card counts of every seat: {ship_count}. Florins are not announced."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round mod (2N) == 0 (end of a day), day scoring is applied. Let top = max ship_value. If top > 0 and exactly one player has top, that player gains 15. If k>1 players have top, each gains floor(22/k) and no second place is paid. If exactly one player has top, let second = the highest ship_value below top. If second > 0, the m players with second each gain floor(7/m). Then every ship_cards, ship_value and ship_count is reset to empty or 0, discard is emptied, and day rises by 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round == 6N (after day 3 scoring), majorities are paid. For each of grain_count, cloth_count, spice_count and dye_count: let M = the max over players. If M > 0, the j players with M each gain floor(10/j). Then each player gains 3 \u00d7 their count of their own favoured_good."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "If round == 6N, every player's favoured_good is revealed to everyone."
    },
    {
      "action": "update",
      "who": "table",
      "answer": null,
      "effect": "round rises by 1."
    },
    {
      "action": "check",
      "who": "table",
      "answer": null,
      "effect": "If round > 6N, the game ends. Otherwise the next round begins."
    }
  ],
  "ending": {
    "condition": "round > 6 * N",
    "rank_by": "you.florins * 1000 + you.total_cards",
    "decided_by": "The player with the most florins after end-of-game scoring wins. A tie on florins goes to the tied player with more total cards collected over the game. Players still tied share the win, which is the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has 40 florins, visible only to that player."
    },
    {
      "id": "R2",
      "text": "When the game starts, then each player holds a different favoured good drawn at random from Grain, Cloth, Spice and Dye, known only to that player."
    },
    {
      "id": "R3",
      "text": "When a day starts (round mod 2N == 1), then the deck is rebuilt as 48 cards: 12 per good, with values 0,1,1,2,2,3,3,3,4,4,5,5."
    },
    {
      "id": "R4",
      "text": "When it is round r, then the active seat is ((r-1) mod N)+1."
    },
    {
      "id": "R5",
      "text": "When the game has N players, then each day has 2N rounds and the game has 6N rounds: 18 with 3 players, 24 with 4."
    },
    {
      "id": "R6",
      "text": "When a round starts, then 3 cards are drawn from the deck and revealed in order as A, B and C."
    },
    {
      "id": "R7",
      "text": "When the active player chooses lot size 1, 2 or 3, then the lot is A, A+B or A+B+C, and the unchosen revealed cards are discarded."
    },
    {
      "id": "R8",
      "text": "When bidding happens, then all players, including the active player, bid at the same time a whole number from 0 to their own current florins, and 0 is a pass."
    },
    {
      "id": "R9",
      "text": "When a player's ship_count + lot_size > 5, then that player's bid is treated as 0."
    },
    {
      "id": "R10",
      "text": "When one valid bid above 0 is strictly highest, then that bidder wins the lot."
    },
    {
      "id": "R11",
      "text": "When the highest valid bids tie and the active player is among them, then the active player wins."
    },
    {
      "id": "R12",
      "text": "When the highest valid bids tie without the active player, then the tied player who comes first in seat order after the active seat wins."
    },
    {
      "id": "R13",
      "text": "When every bid is 0, then the lot is discarded and nobody pays."
    },
    {
      "id": "R14",
      "text": "When a player wins a lot with bid b, then their florins fall by b, ship_value rises by the sum of the lot's card values, ship_count and total_cards rise by the lot size, and each good count rises by that good's cards in the lot."
    },
    {
      "id": "R15",
      "text": "When a round ends, then the winner, the price paid and every player's ship_count are announced, and florins are not announced."
    },
    {
      "id": "R16",
      "text": "When a day ends and one player alone has the highest ship value (above 0), then that player gains 15 florins."
    },
    {
      "id": "R17",
      "text": "When a day ends and k>1 players tie for the highest ship value (above 0), then each gains floor(22/k) florins and no second place is paid."
    },
    {
      "id": "R18",
      "text": "When a day ends with a single leader, then the m players with the second-highest ship value (above 0) each gain floor(7/m) florins."
    },
    {
      "id": "R19",
      "text": "When a player's ship value is 0 at day end, then that player earns nothing from day scoring."
    },
    {
      "id": "R20",
      "text": "When day scoring is done, then all ships are emptied (value 0, count 0), and the game-long good counts are kept."
    },
    {
      "id": "R21",
      "text": "When the game ends, then for each good the j players with the most cards of it (more than 0) each gain floor(10/j) florins, and a good nobody collected pays nothing."
    },
    {
      "id": "R22",
      "text": "When the game ends, then each player gains 3 florins per card of their favoured good collected, and favoured goods are revealed."
    },
    {
      "id": "R23",
      "text": "When round 6N has been completed, then the game ends."
    },
    {
      "id": "R24",
      "text": "When the game ends, then the player with the most florins wins, a tie goes to more total_cards, and players still tied share the win."
    }
  ],
  "offers": [
    {
      "question": "Lot size",
      "who": "the active seat only",
      "options": "1, 2 or 3"
    },
    {
      "question": "Sealed bid",
      "who": "every seat, including the active seat",
      "options": "any whole number from 0 to that seat's current florins. A seat whose ship cannot hold the lot is still asked, but its bid counts as 0."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer chose 4. 3 is the least where a sealed auction has real rivals and both day prizes are contested. More than 4 is impossible because only 4 favoured goods can be dealt, and majorities would get too thin."
    },
    {
      "what": "No talk phase",
      "why": "The source says there is no talk. Bidding is sealed and simultaneous, so it is a poll."
    },
    {
      "what": "Tie-break order computed as priority = N - ((seat - active_seat + N) mod N)",
      "why": "This turns 'active player first, then seats after the active player' into arithmetic."
    },
    {
      "what": "Cards encoded as text like 'Spice-3'",
      "why": "The good and the value are both needed for the counts and the ship value."
    },
    {
      "what": "Card values given as the number of copies of each value per good, and round counts given per player (2 per day, 6 per game)",
      "why": "Parameters must be plain numbers. 1,2,2,3,2,2 copies of values 0 to 5 give the 12-card distribution, and rounds = 2N per day and 6N in total."
    },
    {
      "what": "ship_value is public",
      "why": "Lots and winners are announced, so ship contents are public knowledge. Only florins, bids and favoured goods are secret."
    },
    {
      "what": "Second place is computed only among ship values above 0 and strictly below the top",
      "why": "The source says a value of 0 earns nothing and a tied first place cancels second place."
    },
    {
      "what": "Rank expression florins*1000 + total_cards",
      "why": "total_cards cannot reach 1000, so florins decide first and cards break ties. Any remaining tie shares the win, which is the draw."
    }
  ],
  "simplifications": [
    {
      "what": "The deck rebuild and ship emptying at a day boundary are done by conditional updates on round, at the start of a day and at its end",
      "why": "The step list is flat, so day transitions use if-conditions on round."
    },
    {
      "what": "Favoured goods are revealed by a public tell at the end of the game",
      "why": "The attribute stays private to its owner, so the reveal is an announcement."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: florins, ship_count, total_cards; table: round, day.
````

## Reply

````
```json
[
  {"name": "Every seat starts with 40 florins and no cards", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"florins": 40, "total_cards": 0, "ship_count": 0}, "2": {"florins": 40, "total_cards": 0, "ship_count": 0}, "3": {"florins": 40, "total_cards": 0, "ship_count": 0}},
              "game": {"round": 1, "day": 1}}},

  {"name": "Favoured goods (random) pay 3 per card whichever good is dealt: equal holdings give equal end scores", "rule": "R2", "players": 3, "seed": 1,
   "given": {"players": {"1": {"florins": 40, "grain_count": 2, "cloth_count": 2, "spice_count": 2, "dye_count": 2, "total_cards": 8, "ship_value": 0, "ship_count": 0},
                         "2": {"florins": 40, "grain_count": 2, "cloth_count": 2, "spice_count": 2, "dye_count": 2, "total_cards": 8, "ship_value": 0, "ship_count": 0},
                         "3": {"florins": 40, "grain_count": 2, "cloth_count": 2, "spice_count": 2, "dye_count": 2, "total_cards": 8, "ship_value": 0, "ship_count": 0}},
             "game": {"round": 18, "day": 3, "deck": ["Dye-0", "Dye-0", "Dye-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"winner": [1, 2, 3],
              "standings": {"1": 58008, "2": 58008, "3": 58008},
              "players": {"1": {"florins": 58}, "2": {"florins": 58}, "3": {"florins": 58}}}},

  {"name": "A new day rebuilds the 48-card deck and empties ships", "rule": "R3", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_count": 3, "ship_value": 9}},
             "game": {"round": 7, "day": 2, "deck": ["Grain-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 1, "options_include": 1}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"lens": {"game": {"deck": 45}},
              "players": {"1": {"ship_count": 0, "florins": 40}},
              "game": {"round": 8, "day": 2}}},

  {"name": "In round 5 of a 3-player game only seat 2 chooses the lot size", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"florins": 0}, "3": {"florins": 0}},
             "game": {"round": 5, "day": 1, "deck": ["Grain-2", "Grain-2", "Grain-2"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 3}, {"seat": 1, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"offered": [{"seat": 2, "option": 3}],
              "not_offered": [{"seat": 1, "option": 1}, {"seat": 3, "option": 1}, {"seat": 1, "option": 3}, {"seat": 3, "option": 3}],
              "game": {"round": 6}}},

  {"name": "With 4 players a day lasts 8 rounds: round 16 ends day 2", "rule": "R5", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"ship_count": 2, "ship_value": 0, "total_cards": 2}},
             "game": {"round": 16, "day": 2, "deck": ["Cloth-3", "Cloth-3", "Cloth-3"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 4, "options_include": 0, "times": "all"}, {"seat": 4, "options_include": 1}],
   "expect": {"game": {"round": 17, "day": 3}, "players": {"1": {"ship_count": 0, "total_cards": 2}}}},

  {"name": "With 4 players the game ends after round 24", "rule": "R5", "players": 4,
   "given": {"players": {"1": {"florins": 40}, "2": {"florins": 40}, "3": {"florins": 40}, "4": {"florins": 50}},
             "game": {"round": 24, "day": 3, "deck": ["Cloth-3", "Cloth-3", "Cloth-3"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 4, "options_include": 0, "times": "all"}, {"seat": 4, "options_include": 1}],
   "expect": {"winner": 4, "standings": {"1": 40000, "2": 40000, "3": 40000, "4": 50000}}},

  {"name": "Each round draws 3 cards from the deck", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1", "Grain-1"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 1}, {"seat": 1, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"lens": {"game": {"deck": 7}}, "game": {"round": 3}}},

  {"name": "Lot size 2 offers A+B and discards C", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Spice-4", "Spice-4", "Spice-4"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 2},
             {"seat": 1, "options_include": 0, "answer": 5}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"lens": {"game": {"discard": 1, "deck": 0}},
              "players": {"1": {"florins": 35, "ship_count": 2, "total_cards": 2}, "2": {"florins": 40, "ship_count": 0}, "3": {"florins": 40}}}},

  {"name": "Bids range from 0 to own florins and the active seat bids too", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"florins": 12}},
             "game": {"round": 2, "day": 1, "deck": ["Dye-2", "Dye-2", "Dye-2"]}},
   "rules": [{"seat": 2, "options_include": 0, "answer": 7}, {"seat": 2, "options_include": 1},
             {"seat": 1, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"offered": [{"seat": 1, "option": 12}, {"seat": 1, "option": 0}, {"seat": 2, "option": 0}],
              "not_offered": [{"seat": 1, "option": 13}],
              "players": {"2": {"florins": 33, "ship_count": 1, "total_cards": 1}, "1": {"florins": 12}}}},

  {"name": "A bid from a seat whose ship cannot hold the lot counts as 0", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_count": 4, "ship_value": 8, "total_cards": 4}},
             "game": {"round": 2, "day": 1, "deck": ["Cloth-1", "Cloth-1", "Cloth-1"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 2},
             {"seat": 1, "options_include": 0, "answer": 20}, {"seat": 3, "options_include": 0, "answer": 5}],
   "expect": {"players": {"1": {"florins": 40, "ship_count": 4, "total_cards": 4}, "3": {"florins": 35, "ship_count": 2, "total_cards": 2}}}},

  {"name": "The strictly highest bid wins the lot", "rule": "R10", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Dye-5", "Dye-5", "Dye-5"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 1},
             {"seat": 1, "options_include": 0, "answer": 4}, {"seat": 3, "options_include": 0, "answer": 9}],
   "expect": {"players": {"1": {"florins": 40, "ship_count": 0}, "2": {"florins": 40}, "3": {"florins": 31, "ship_count": 1, "total_cards": 1}}}},

  {"name": "A tie including the active seat goes to the active seat", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Grain-3", "Grain-3", "Grain-3"]}},
   "rules": [{"seat": 2, "options_include": 0, "answer": 6}, {"seat": 2, "options_include": 1},
             {"seat": 1, "options_include": 0, "answer": 6}, {"seat": 3, "options_include": 0, "answer": 6}],
   "expect": {"players": {"1": {"florins": 40, "ship_count": 0}, "2": {"florins": 34, "ship_count": 1}, "3": {"florins": 40, "ship_count": 0}}}},

  {"name": "A tie without the active seat goes to the first seat after it (seat 3 before seat 1 when seat 2 is active)", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Grain-3", "Grain-3", "Grain-3"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 1},
             {"seat": 1, "options_include": 0, "answer": 6}, {"seat": 3, "options_include": 0, "answer": 6}],
   "expect": {"players": {"1": {"florins": 40, "ship_count": 0}, "2": {"florins": 40, "ship_count": 0}, "3": {"florins": 34, "ship_count": 1, "total_cards": 1}}}},

  {"name": "When every bid is 0 the lot is discarded and nobody pays", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"game": {"round": 2, "day": 1, "deck": ["Spice-5", "Spice-5", "Spice-5"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 3},
             {"seat": 1, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"lens": {"game": {"discard": 3}},
              "players": {"1": {"florins": 40, "ship_count": 0, "total_cards": 0}, "2": {"florins": 40, "ship_count": 0, "total_cards": 0}, "3": {"florins": 40, "ship_count": 0, "total_cards": 0}}}},

  {"name": "Winning a 3-card lot with bid 11 costs 11 and adds 3 cards", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"florins": 30, "ship_count": 1, "ship_value": 2, "total_cards": 4}},
             "game": {"round": 2, "day": 1, "deck": ["Grain-2", "Grain-2", "Grain-2"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 3},
             {"seat": 1, "options_include": 0, "answer": 11}, {"seat": 3, "options_include": 0, "times": "all"}],
   "expect": {"players": {"1": {"florins": 19, "ship_count": 4, "total_cards": 7}, "2": {"florins": 40}, "3": {"florins": 40}}}},

  {"name": "After a round every seat's ship count reflects the sale", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"players": {"2": {"ship_count": 1, "ship_value": 3, "total_cards": 1}},
             "game": {"round": 2, "day": 1, "deck": ["Cloth-4", "Cloth-4", "Cloth-4"]}},
   "rules": [{"seat": 2, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 2},
             {"seat": 1, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "answer": 8}],
   "expect": {"players": {"1": {"ship_count": 0, "florins": 40}, "2": {"ship_count": 1, "florins": 40}, "3": {"ship_count": 2, "florins": 32}}}},

  {"name": "A lone top ship at day end gains 15", "rule": "R16", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_value": 10, "ship_count": 3}, "2": {"ship_value": 0}, "3": {"ship_value": 0}},
             "game": {"round": 6, "day": 1, "deck": ["Dye-1", "Dye-1", "Dye-1"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"florins": 55}, "2": {"florins": 40}, "3": {"florins": 40}}, "game": {"day": 2, "round": 7}}},

  {"name": "Two ships tied for top each gain 11 and no second place is paid", "rule": "R17", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_value": 8, "ship_count": 2}, "2": {"ship_value": 8, "ship_count": 2}, "3": {"ship_value": 5, "ship_count": 2}},
             "game": {"round": 6, "day": 1, "deck": ["Dye-1", "Dye-1", "Dye-1"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"florins": 51}, "2": {"florins": 51}, "3": {"florins": 40}}}},

  {"name": "Two ships tied for second each gain 3", "rule": "R18", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_value": 10, "ship_count": 3}, "2": {"ship_value": 6, "ship_count": 2}, "3": {"ship_value": 6, "ship_count": 2}},
             "game": {"round": 6, "day": 1, "deck": ["Dye-1", "Dye-1", "Dye-1"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"florins": 55}, "2": {"florins": 43}, "3": {"florins": 43}}}},

  {"name": "A ship of value 0 earns nothing at day end", "rule": "R19", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_value": 10, "ship_count": 3}, "2": {"ship_value": 4, "ship_count": 1}, "3": {"ship_value": 0, "ship_count": 1}},
             "game": {"round": 6, "day": 1, "deck": ["Dye-1", "Dye-1", "Dye-1"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"florins": 55}, "2": {"florins": 47}, "3": {"florins": 40}}}},

  {"name": "Day scoring empties ships but keeps total cards", "rule": "R20", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"ship_value": 7, "ship_count": 3, "total_cards": 5}, "2": {"ship_value": 0, "ship_count": 0, "total_cards": 2}},
             "game": {"round": 6, "day": 1, "deck": ["Dye-1", "Dye-1", "Dye-1"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"players": {"1": {"ship_count": 0, "total_cards": 5, "florins": 55}, "2": {"ship_count": 0, "total_cards": 2}},
              "game": {"day": 2}}},

  {"name": "End majorities: sole grain leader gains 10, cloth tie gains 5 each, uncollected goods pay nothing", "rule": "R21", "players": 3,
   "given": {"players": {"1": {"florins": 40, "favoured_good": "Spice", "grain_count": 3, "cloth_count": 2, "spice_count": 0, "dye_count": 0, "total_cards": 5, "ship_value": 0, "ship_count": 0},
                         "2": {"florins": 40, "favoured_good": "Dye", "grain_count": 1, "cloth_count": 2, "spice_count": 0, "dye_count": 0, "total_cards": 3, "ship_value": 0, "ship_count": 0},
                         "3": {"florins": 40, "favoured_good": "Grain", "grain_count": 0, "cloth_count": 0, "spice_count": 0, "dye_count": 0, "total_cards": 0, "ship_value": 0, "ship_count": 0}},
             "game": {"round": 18, "day": 3, "deck": ["Dye-0", "Dye-0", "Dye-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"winner": 1, "standings": {"1": 55005, "2": 45003, "3": 40000},
              "players": {"1": {"florins": 55}, "2": {"florins": 45}, "3": {"florins": 40}}}},

  {"name": "Favoured goods pay 3 per card at game end", "rule": "R22", "players": 3,
   "given": {"players": {"1": {"florins": 40, "favoured_good": "Grain", "grain_count": 2, "cloth_count": 0, "spice_count": 0, "dye_count": 0, "total_cards": 2, "ship_value": 0, "ship_count": 0},
                         "2": {"florins": 40, "favoured_good": "Cloth", "grain_count": 0, "cloth_count": 3, "spice_count": 0, "dye_count": 0, "total_cards": 3, "ship_value": 0, "ship_count": 0},
                         "3": {"florins": 40, "favoured_good": "Spice", "grain_count": 0, "cloth_count": 0, "spice_count": 1, "dye_count": 0, "total_cards": 1, "ship_value": 0, "ship_count": 0}},
             "game": {"round": 18, "day": 3, "deck": ["Dye-0", "Dye-0", "Dye-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"winner": 2, "standings": {"1": 56002, "2": 59003, "3": 53001},
              "players": {"1": {"florins": 56}, "2": {"florins": 59}, "3": {"florins": 53}}}},

  {"name": "A 3-player game ends after round 18", "rule": "R23", "players": 3,
   "given": {"players": {"1": {"florins": 50, "ship_value": 0}, "2": {"florins": 40, "ship_value": 0}, "3": {"florins": 30, "ship_value": 0}},
             "game": {"round": 18, "day": 3, "deck": ["Dye-0", "Dye-0", "Dye-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"winner": 1, "standings": {"1": 50000, "2": 40000, "3": 30000},
              "players": {"1": {"florins": 50}, "2": {"florins": 40}, "3": {"florins": 30}}}},

  {"name": "Florins tie broken by total cards, remaining tie shares the win", "rule": "R24", "players": 3,
   "given": {"players": {"1": {"florins": 40, "total_cards": 2, "ship_value": 0}, "2": {"florins": 40, "total_cards": 5, "ship_value": 0}, "3": {"florins": 40, "total_cards": 5, "ship_value": 0}},
             "game": {"round": 18, "day": 3, "deck": ["Dye-0", "Dye-0", "Dye-0"]}},
   "rules": [{"seat": 1, "options_include": 0, "times": "all"}, {"seat": 2, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 0, "times": "all"}, {"seat": 3, "options_include": 1}],
   "expect": {"winner": [2, 3], "standings": {"1": 40002, "2": 40005, "3": 40005}}}
]
```
````
