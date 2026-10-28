# 06 scenarios

- time: 2026-10-28T05:52:26+00:00 (105.7s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 4c98d9ac263e3232, reply sha256 02938417d4d689c3

## Sent

````
SPEC:
{
  "name": "Cat Lady: Secret Favourites (Balanced)",
  "summary": "A card-drafting game for 3 to 4 players: each round players take turns picking a 2-card lot from a public market, collecting food, cats, strays, toys and catnip, and score at the end with a secret Favourite bonus.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 96,
    "food1_cards": 18,
    "food1_value": 1,
    "food2_cards": 10,
    "food2_value": 2,
    "cat_cards": 20,
    "stray_cards": 8,
    "toy_cards_per_colour": 8,
    "toy_cards_total": 24,
    "catnip_cards": 16,
    "cards_per_lot": 2,
    "lots_with_3_players": 4,
    "lots_with_4_players": 5,
    "rounds_with_3_players": 12,
    "rounds_with_4_players": 8,
    "picks_per_position_3_players": 4,
    "picks_per_position_4_players": 2,
    "unused_deck_cards_4_players": 16,
    "food_per_cat": 2,
    "fed_cat_points": 5,
    "unfed_cat_points": -1,
    "stray_points": 3,
    "toy_points": 1,
    "toy_set_points": 4,
    "catnip_count_cap": 6,
    "catnip_max_points": 21,
    "food_penalty": 2,
    "food_penalty_min_leftover": 1,
    "fav_cats_per_fed_cat": 2,
    "fav_cats_max": 10,
    "fav_toys_per_toy": 1,
    "fav_catnip_per_card": 2,
    "fav_catnip_max": 12,
    "fav_strays_per_stray": 3,
    "rank_score_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "favourite",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The player's secret Favourite: cats, toys, catnip or strays",
        "observable": false
      },
      {
        "key": "favourite_revealed",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The Favourite, copied here at final scoring when it is revealed",
        "observable": true
      },
      {
        "key": "cards",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Every card the player has taken (codes: food1, food2, cat, stray, toy_red, toy_blue, toy_green, catnip)",
        "observable": false
      },
      {
        "key": "food",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Total food value: food1 counts 1 and food2 counts 2",
        "observable": false
      },
      {
        "key": "cats",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Cat cards",
        "observable": false
      },
      {
        "key": "strays",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Stray Cat cards",
        "observable": false
      },
      {
        "key": "toys_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Red Toy cards",
        "observable": false
      },
      {
        "key": "toys_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Blue Toy cards",
        "observable": false
      },
      {
        "key": "toys_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Green Toy cards",
        "observable": false
      },
      {
        "key": "catnip",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of Catnip cards",
        "observable": false
      },
      {
        "key": "fed_cats",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Fed cats, worked out at final scoring as min(cats, floor(food/2)); also the tie-break",
        "observable": true
      },
      {
        "key": "leftover_food",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "food - 2 * fed_cats, worked out at final scoring",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Final total, worked out at final scoring",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "96 codes: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green, 16 catnip",
        "meaning": "The shuffled draw deck",
        "observable": false
      },
      {
        "key": "favourites_pool",
        "type": "list",
        "visible": "none",
        "initial": "[cats, toys, catnip] with 3 players; [cats, toys, catnip, strays] with 4 players",
        "meaning": "The Favourites still to be dealt",
        "observable": false
      },
      {
        "key": "num_rounds",
        "type": "number",
        "visible": "public",
        "initial": "12 if N = 3, 8 if N = 4",
        "meaning": "Total rounds",
        "observable": false
      },
      {
        "key": "num_lots",
        "type": "number",
        "visible": "public",
        "initial": "N + 1",
        "meaning": "Lots dealt each round: 4 with 3 players, 5 with 4 players",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Current round number",
        "observable": false
      },
      {
        "key": "first_picker",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat that picks first this round: ((round-1) mod N) + 1",
        "observable": false
      },
      {
        "key": "lot_a",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in Lot A",
        "observable": false
      },
      {
        "key": "lot_b",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in Lot B",
        "observable": false
      },
      {
        "key": "lot_c",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in Lot C",
        "observable": false
      },
      {
        "key": "lot_d",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in Lot D",
        "observable": false
      },
      {
        "key": "lot_e",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards in Lot E (used only with 4 players)",
        "observable": false
      },
      {
        "key": "lots_open",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Letters of the lots not yet picked this round",
        "observable": false
      },
      {
        "key": "discard",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards from leftover lots",
        "observable": false
      },
      {
        "key": "max_leftover",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Largest leftover_food among all players, worked out at final scoring",
        "observable": false
      }
    ]
  },
  "setup": [
    "Build the deck of 96 cards: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green and 16 catnip, and shuffle it once (all later draws are random picks from deck).",
    "Set favourites_pool to [cats, toys, catnip] with 3 players, or to [cats, toys, catnip, strays] with 4 players.",
    "Each player draws one Favourite at random from favourites_pool into their favourite (ally), and it is removed from the pool, so every Favourite is different. Each player is privately told their Favourite.",
    "Set num_rounds to 12 with 3 players or 8 with 4 players, and set num_lots to N + 1.",
    "Seats are fixed from seat 1 to seat N, and each player is sent their own state."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; first_picker = ((round - 1) mod N) + 1; lots_open = [A, B, C, D] with 3 players or [A, B, C, D, E] with 4 players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each letter in lots_open, draw 2 cards at random from deck into lot_<letter> (append to the lot, remove from deck)."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce round, first_picker and the contents of every lot in lots_open."
    },
    {
      "action": "ask",
      "who": "each player in turn, starting with seat first_picker and continuing in seat order (wrapping from seat N to seat 1)",
      "answer": "one letter from lots_open",
      "effect": "The chosen lot's cards are appended to the player's cards. For each card: food1 adds 1 to food, food2 adds 2 to food, cat adds 1 to cats, stray adds 1 to strays, toy_red/toy_blue/toy_green add 1 to toys_red/toys_blue/toys_green, catnip adds 1 to catnip. The lot list is emptied and its letter is removed from lots_open. The pick is announced to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The cards of the one lot left in lots_open are appended to discard, that lot is emptied, and lots_open is emptied."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == num_rounds, for each player: fed_cats = min(cats, floor(food / 2)); leftover_food = food - 2 * fed_cats; score = 5 * fed_cats - 1 * (cats - fed_cats) + 3 * strays + 1 * (toys_red + toys_blue + toys_green) + 4 * min(toys_red, toys_blue, toys_green) + m * (m + 1) / 2 where m = min(catnip, 6)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == num_rounds: max_leftover = the largest leftover_food over all players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round == num_rounds, for each player: if leftover_food == max_leftover and max_leftover >= 1, score -= 2. Favourite bonus: if favourite == cats, score += min(2 * fed_cats, 10); if toys, score += toys_red + toys_blue + toys_green; if catnip, score += min(2 * catnip, 12); if strays, score += 3 * strays. favourite_revealed = favourite."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When round == num_rounds, announce every player's favourite_revealed, fed_cats and score."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= num_rounds; otherwise continue to the next round."
    }
  ],
  "ending": {
    "condition": "round >= num_rounds",
    "rank_by": "you.score * 100 + you.fed_cats",
    "decided_by": "The highest final score wins. Among players tied on score, the one with the most fed cats wins. Players still tied on both share the win, which is a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup the deck holds 96 cards: 18 food1, 10 food2, 20 cat, 8 stray, 8 toy_red, 8 toy_blue, 8 toy_green and 16 catnip."
    },
    {
      "id": "R2",
      "text": "When there are 3 players, Favourites are dealt from {cats, toys, catnip}; when there are 4 players, from {cats, toys, catnip, strays}; no two players get the same Favourite."
    },
    {
      "id": "R3",
      "text": "A player's favourite is visible only to that player until final scoring, when it is copied to the public favourite_revealed."
    },
    {
      "id": "R4",
      "text": "When there are 3 players the game lasts 12 rounds; when there are 4 players it lasts 8 rounds."
    },
    {
      "id": "R5",
      "text": "In round r the first picker is seat ((r-1) mod N) + 1, and picking continues in seat order, wrapping around."
    },
    {
      "id": "R6",
      "text": "Each round, when there are 3 players, 4 lots (A to D) of 2 cards each are dealt from the deck; when there are 4 players, 5 lots (A to E) of 2 cards each are dealt."
    },
    {
      "id": "R7",
      "text": "Every lot's contents are announced to all players before any pick."
    },
    {
      "id": "R8",
      "text": "On their turn, a player must choose exactly one lot that no one has picked yet this round."
    },
    {
      "id": "R9",
      "text": "When a player takes a lot, each food1 adds 1 food, each food2 adds 2 food, and each cat, stray, toy of a colour or catnip adds 1 to the matching count."
    },
    {
      "id": "R10",
      "text": "After every player has picked, the one remaining lot is moved to the discard pile."
    },
    {
      "id": "R11",
      "text": "When there are 4 players, 16 cards remain in the deck at the end and are never used; when there are 3 players the deck is exactly used up."
    },
    {
      "id": "R12",
      "text": "At final scoring, fed_cats = min(cats, floor(food / 2)); for example 5 cats and 7 food give 3 fed cats."
    },
    {
      "id": "R13",
      "text": "Each fed cat scores 5 and each unfed cat scores -1; for example 5 cats with 3 fed score 15 - 2 = 13."
    },
    {
      "id": "R14",
      "text": "leftover_food = food - 2 * fed_cats."
    },
    {
      "id": "R15",
      "text": "Each stray scores 3."
    },
    {
      "id": "R16",
      "text": "Each toy scores 1, plus 4 for each set of one red, one blue and one green; for example 3 red, 2 blue and 1 green score 6 + 4 = 10."
    },
    {
      "id": "R17",
      "text": "With n catnip, a player scores m(m+1)/2 where m = min(n, 6); for example 4 catnip score 10, and 8 catnip score 21."
    },
    {
      "id": "R18",
      "text": "When a player's leftover_food equals the largest leftover_food at the table and that value is at least 1, the player loses 2 points; all players tied for the largest lose 2."
    },
    {
      "id": "R19",
      "text": "When the largest leftover_food at the table is 0, no player loses points for food."
    },
    {
      "id": "R20",
      "text": "When a player's Favourite is cats, they gain 2 per fed cat, at most 10."
    },
    {
      "id": "R21",
      "text": "When a player's Favourite is toys, they gain 1 per toy card."
    },
    {
      "id": "R22",
      "text": "When a player's Favourite is catnip, they gain 2 per catnip card, counting cards beyond 6, at most 12."
    },
    {
      "id": "R23",
      "text": "When a player's Favourite is strays (4 players only), they gain 3 per stray."
    },
    {
      "id": "R24",
      "text": "The game ends after round num_rounds; the highest score wins, ties go to the most fed cats, and players still tied draw."
    }
  ],
  "offers": [
    {
      "question": "Choose a lot this round",
      "who": "each player in turn, starting with first_picker",
      "options": "The letters still in lots_open: with 3 players the first picker sees 4 letters (A to D), then 3, then 2; with 4 players the first picker sees 5 letters (A to E), then 4, 3 and 2. A lot already taken is never offered."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer chose 4. The minimum is 3 because with 2 players there is little contest over lots and almost nothing to hide a Favourite among. The maximum is 4 because the deck and the Favourite set (four Favourites) are built for at most 4."
    },
    {
      "what": "No talk step before picks",
      "why": "The source has no negotiation. Picks are public, and the interest lies in reading others' Favourites from their picks and hate-drafting, so talk would only add words."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player balances food against cats to avoid unfed cats and the food penalty, chases toy sets and catnip, and infers rivals' secret Favourites from what they take so as to deny them key lots."
    },
    {
      "what": "Card codes food1, food2, cat, stray, toy_red, toy_blue, toy_green, catnip",
      "why": "The deck needs concrete list entries for drawing and counting."
    },
    {
      "what": "rank_by = score * 100 + fed_cats",
      "why": "fed_cats is at most 20 (below 100), so this ranks by score first and fed cats second, and remaining ties share the win as the source's draw."
    }
  ],
  "simplifications": [
    {
      "what": "Dealing the market from the top of the deck is done as random draws from the deck list",
      "why": "The deck is shuffled once, so drawing at random is equivalent."
    },
    {
      "what": "The Favourite is revealed by copying it to a public attribute favourite_revealed at final scoring",
      "why": "Visibility of an attribute is fixed, so revealing is done by copying the value."
    },
    {
      "what": "The food penalty uses a table attribute max_leftover",
      "why": "The engine has no direct player-to-player comparison; the maximum is kept on the table and each player is compared to it."
    },
    {
      "what": "Final scoring runs as conditional updates in the last round",
      "why": "The step list is flat, so the scoring steps carry a 'when round == num_rounds' condition."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: favourite_revealed, fed_cats, score; table: none.
````

## Reply

````
```json
[
  {"name": "Deck holds 96 cards right after setup", "rule": "R1", "players": 3, "seed": 1, "default": "first", "rounds": 0,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 96}}}},

  {"name": "3 players: favourites never include strays, so all-zero tables with 2 strays each score 6 apiece", "rule": "R2", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]}},
   "rules": [],
   "expect": {"winner": [1, 2, 3], "standings": {"1": 600, "2": 600, "3": 600},
              "players": {"1": {"score": 6}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "Favourite not revealed at setup", "rule": "R3", "players": 3, "seed": 1, "default": "first", "rounds": 0,
   "rules": [],
   "expect": {"players": {"1": {"favourite_revealed": ""}, "2": {"favourite_revealed": ""}, "3": {"favourite_revealed": ""}}}},

  {"name": "Favourite copied to favourite_revealed at final scoring", "rule": "R3", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys"}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": [1, 2, 3],
              "players": {"1": {"favourite_revealed": "toys"}, "2": {"favourite_revealed": "cats"}, "3": {"favourite_revealed": "catnip"}}}},

  {"name": "4 players: round 8 is the last, so final scoring runs", "rule": "R4", "players": 4, "seed": 1, "default": "first", "rounds": 1,
   "given": {"game": {"round": 7, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"cats": 2, "food": 4}}},
   "rules": [],
   "expect": {"players": {"1": {"fed_cats": 2}}}},

  {"name": "3 players: round 8 is not the last, so no scoring yet", "rule": "R4", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "given": {"game": {"round": 7}, "players": {"1": {"cats": 2, "food": 4}}},
   "rules": [],
   "expect": {"players": {"1": {"fed_cats": 0, "score": 0}}}},

  {"name": "Round 2 with 3 players: seat 2 picks first, then seat 3, then seat 1", "rule": "R5", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "given": {"game": {"round": 1}},
   "rules": [],
   "expect": {"offered": [{"seat": 2, "option": "A"}, {"seat": 3, "option": "B"}, {"seat": 1, "option": "C"}, {"seat": 1, "option": "D"}],
              "not_offered": [{"seat": 3, "option": "A"}, {"seat": 1, "option": "A"}, {"seat": 1, "option": "B"}]}},

  {"name": "3 players: 4 lots of 2 are dealt, so 8 cards leave the deck", "rule": "R6", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 88}},
              "offered": [{"seat": 1, "option": "D"}],
              "not_offered": [{"seat": 1, "option": "E"}]}},

  {"name": "4 players: 5 lots of 2 are dealt, so 10 cards leave the deck", "rule": "R6", "players": 4, "seed": 1, "default": "first", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 86}},
              "offered": [{"seat": 1, "option": "E"}]}},

  {"name": "First picker sees every lot before picking", "rule": "R7", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "rules": [],
   "expect": {"offered": [{"seat": 1, "option": "A"}, {"seat": 1, "option": "B"}, {"seat": 1, "option": "C"}, {"seat": 1, "option": "D"}]}},

  {"name": "A lot already taken is not offered again", "rule": "R8", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "rules": [{"seat": 1, "options_include": "C"}],
   "expect": {"not_offered": [{"seat": 2, "option": "C"}, {"seat": 3, "option": "C"}, {"seat": 3, "option": "A"}]}},

  {"name": "Each food2 adds 2 food (all lots are food2)", "rule": "R9", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["food2","food2","food2","food2","food2","food2","food2","food2"]},
             "players": {"1": {"favourite": "toys", "cats": 2}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "standings": {"1": 1002, "2": -200, "3": -200},
              "players": {"1": {"fed_cats": 2, "score": 10}, "2": {"score": -2}, "3": {"score": -2}}}},

  {"name": "Each food1 adds 1 food (all lots are food1)", "rule": "R9", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["food1","food1","food1","food1","food1","food1","food1","food1"]},
             "players": {"1": {"favourite": "toys", "cats": 1}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1,
              "players": {"1": {"fed_cats": 1, "score": 5}, "2": {"score": -2}, "3": {"score": -2}}}},

  {"name": "Each cat adds 1 cat (all lots are cats)", "rule": "R9", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["cat","cat","cat","cat","cat","cat","cat","cat"]},
             "players": {"1": {"favourite": "toys", "food": 4}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1,
              "players": {"1": {"fed_cats": 2, "score": 10}, "2": {"score": -2}, "3": {"score": -2}}}},

  {"name": "Leftover lot goes to discard", "rule": "R10", "players": 3, "seed": 1, "default": "first", "rounds": 1,
   "rules": [],
   "expect": {"lens": {"game": {"discard": 2, "lot_a": 0, "lot_b": 0, "lot_c": 0, "lot_d": 0}}}},

  {"name": "4 players: 16 cards remain unused after 8 rounds", "rule": "R11", "players": 4, "seed": 1, "default": "first", "rounds": 8,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"cards": 16}, "2": {"cards": 16}, "3": {"cards": 16}, "4": {"cards": 16}}}}},

  {"name": "3 players: deck exactly used up after 12 rounds", "rule": "R11", "players": 3, "seed": 1, "default": "first", "rounds": 12,
   "rules": [],
   "expect": {"lens": {"game": {"deck": 0}, "players": {"1": {"cards": 24}, "2": {"cards": 24}, "3": {"cards": 24}}}}},

  {"name": "5 cats and 7 food give 3 fed cats", "rule": "R12", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "cats": 5, "food": 7}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "standings": {"1": 1703, "2": 600, "3": 600},
              "players": {"1": {"fed_cats": 3, "score": 17}, "2": {"fed_cats": 0, "score": 6}, "3": {"score": 6}}}},

  {"name": "5 cats with 3 fed score 13 (plus 6 for strays)", "rule": "R13", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "cats": 5, "food": 6}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"fed_cats": 3, "score": 19}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "Leftover food is food minus 2 per fed cat: only the largest leftover is penalised", "rule": "R14", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "cats": 1, "food": 5}, "2": {"favourite": "catnip", "cats": 2, "food": 4}, "3": {"favourite": "cats", "food": 1}}},
   "rules": [],
   "expect": {"winner": 2, "standings": {"1": 901, "2": 1602, "3": 600},
              "players": {"1": {"fed_cats": 1, "score": 9}, "2": {"fed_cats": 2, "score": 16}, "3": {"fed_cats": 0, "score": 6}}}},

  {"name": "Each stray scores 3", "rule": "R15", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "strays": 3}, "2": {"favourite": "cats"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 15}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "3 red, 2 blue, 1 green toys score 10", "rule": "R16", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "cats", "toys_red": 3, "toys_blue": 2, "toys_green": 1}, "2": {"favourite": "toys"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 16}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "4 catnip score 10, 8 catnip score 21", "rule": "R17", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "cats", "catnip": 4}, "2": {"favourite": "toys", "catnip": 8}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 2, "players": {"1": {"score": 16}, "2": {"score": 27}, "3": {"score": 6}}}},

  {"name": "All players tied for the largest leftover lose 2", "rule": "R18", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "food": 2}, "2": {"favourite": "catnip", "food": 2}, "3": {"favourite": "cats"}}},
   "rules": [],
   "expect": {"winner": 3, "players": {"1": {"score": 4}, "2": {"score": 4}, "3": {"score": 6}}}},

  {"name": "No food penalty when every leftover is 0", "rule": "R19", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "cats": 2, "food": 4}, "2": {"favourite": "catnip", "cats": 1, "food": 2}, "3": {"favourite": "cats"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 16}, "2": {"score": 11}, "3": {"score": 6}}}},

  {"name": "Cats favourite: 2 per fed cat (3 fed gives 6)", "rule": "R20", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "cats", "cats": 3, "food": 6}, "2": {"favourite": "toys", "cats": 3, "food": 6}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 27}, "2": {"score": 21}, "3": {"score": 6}}}},

  {"name": "Cats favourite bonus capped at 10", "rule": "R20", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "cats", "cats": 6, "food": 12}, "2": {"favourite": "toys"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"fed_cats": 6, "score": 46}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "Toys favourite: 1 per toy card", "rule": "R21", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "toys_red": 2}, "2": {"favourite": "cats", "toys_red": 2}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 10}, "2": {"score": 8}, "3": {"score": 6}}}},

  {"name": "Catnip favourite: 2 per catnip, capped at 12", "rule": "R22", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "catnip", "catnip": 8}, "2": {"favourite": "toys", "catnip": 3}, "3": {"favourite": "cats"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 39}, "2": {"score": 12}, "3": {"score": 6}}}},

  {"name": "Catnip favourite: 5 catnip give 10 bonus", "rule": "R22", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "catnip", "catnip": 5}, "2": {"favourite": "toys"}, "3": {"favourite": "cats"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 31}, "2": {"score": 6}, "3": {"score": 6}}}},

  {"name": "Strays favourite (4 players): 3 per stray", "rule": "R23", "players": 4, "seed": 1, "default": "first",
   "given": {"game": {"round": 7, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "strays", "strays": 1}, "2": {"favourite": "cats"}, "3": {"favourite": "toys"}, "4": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": 1, "players": {"1": {"score": 18}, "2": {"score": 6}, "3": {"score": 6}, "4": {"score": 6}}}},

  {"name": "Score tie broken by fed cats", "rule": "R24", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "toys", "cats": 2, "food": 4}, "2": {"favourite": "catnip", "strays": 1, "toys_red": 7}, "3": {"favourite": "cats"}}},
   "rules": [],
   "expect": {"winner": 1, "standings": {"1": 1602, "2": 1600, "3": 600},
              "players": {"1": {"score": 16, "fed_cats": 2}, "2": {"score": 16, "fed_cats": 0}, "3": {"score": 6}}}},

  {"name": "Players tied on score and fed cats share the win", "rule": "R24", "players": 3, "seed": 1, "default": "first",
   "given": {"game": {"round": 11, "deck": ["stray","stray","stray","stray","stray","stray","stray","stray"]},
             "players": {"1": {"favourite": "cats"}, "2": {"favourite": "toys"}, "3": {"favourite": "catnip"}}},
   "rules": [],
   "expect": {"winner": [1, 2, 3], "standings": {"1": 600, "2": 600, "3": 600}}}
]
```
````
