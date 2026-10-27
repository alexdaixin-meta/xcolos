# 04 spec

- time: 2026-10-27T18:17:48+00:00 (40.1s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 e403673b3ac86c6b, reply sha256 124b74ec04a5d8d9

## Sent

````
Game: Medici: Secret Patrons
Players in the source: 3 to 3
Suggested table size, chosen by the designer of these rules (keep it): 3

Rules, as filed in the inventory:
SETUP. Three players sit in fixed order A, B, C. Each starts with 30 florins (public). Each has a ship with room for 5 cards and three public commodity tracks (Spice, Silk, Grain), all at 0. The three commodities are shuffled and one is dealt secretly to each player as their Patron, so every player has a different Patron and knows only their own. The deck has 30 cards: for each of Spice, Silk and Grain there are 10 cards valued 0, 1, 1, 2, 2, 3, 3, 4, 4, 5.

START OF EACH DAY. There are 3 days. Shuffle all 30 cards into a face-down deck and empty every ship (tracks are NOT reset). Turn the top 3 cards face up in a row: this is the Dock, ordered first, second, third. The first active player is A on day 1, B on day 2 and C on day 3. The active role then passes in seat order A, B, C, A... each round. Each day has exactly 9 rounds.

EACH ROUND.
(1) The Dock, all ships, tracks and florins are announced.
(2) The active player chooses a lot size of 1, 2 or 3 (no more than the cards in the Dock). The lot is the first that many Dock cards. Its size is its card count and its value is the sum of its card values.
(3) Auction, once around. The next player in seat order after the active player bids first, then the other non-active player, then the active player last. Each bidder either passes or bids a whole number that is at least 1, higher than the current highest bid, and no more than their florins. A player whose ship lacks room for the whole lot must pass.
(4) If anyone bid, the highest bidder pays that many florins to the bank and loads every card of the lot onto their ship. For each card loaded, that player's track in the card's commodity rises by 1, to a maximum of 10. If everyone passed, the lot is discarded.
(5) Remove the lot's cards from the Dock, slide the remaining Dock cards forward, and refill the Dock to 3 cards from the top of the deck (fewer if the deck runs out).

END OF DAY (after round 9 of the day).
(a) Ship scoring: rank players by total value of the cards on their ship. The highest gets 20 florins and the second gets 10. Tied players add the prizes for the places they occupy and split them equally, rounded down. A player with an empty ship gets nothing.
(b) Commodity majorities: for each commodity, the player with the highest track gets 10 florins and the second highest gets 5. Ties split as above. A track at 0 earns nothing.
(c) Patron: a player who earned a majority award in step (b) in their own Patron commodity receives that same amount again.
All awards are added to florins.

END OF GAME. After day 3 scoring, Patrons are revealed and the player with the most florins wins.

How the winner is decided: After the end-of-day scoring of day 3, the player with the most florins wins. If two or more players tie for the most, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "Medici: Secret Patrons",
  "summary": "Three merchants auction lots of commodity cards from a dock over 3 days of 9 rounds. They score for ship value, for commodity track majorities and a second time for majorities in their own secret Patron commodity. The most florins wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
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
    "cards_per_commodity": 10,
    "card_values_per_commodity": [0, 1, 1, 2, 2, 3, 3, 4, 4, 5],
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
      {"key": "florins", "type": "number", "visible": "public", "initial": 30, "meaning": "Money, and also the score.", "observable": true},
      {"key": "patron", "type": "text", "visible": "ally", "initial": "", "meaning": "The secret Patron commodity (Spice, Silk or Grain). Each player holds a different one. It is revealed at game end.", "observable": false},
      {"key": "ship", "type": "list", "visible": "public", "initial": [], "meaning": "Cards loaded on the ship this day, written as 'Commodity-value', e.g. 'Silk-3'.", "observable": false},
      {"key": "ship_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards on the ship (at most 5).", "observable": false},
      {"key": "ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the values of the cards on the ship.", "observable": false},
      {"key": "track_spice", "type": "number", "visible": "public", "initial": 0, "meaning": "Spice commodity track, 0 to 10, never reset.", "observable": true},
      {"key": "track_silk", "type": "number", "visible": "public", "initial": 0, "meaning": "Silk commodity track, 0 to 10, never reset.", "observable": true},
      {"key": "track_grain", "type": "number", "visible": "public", "initial": 0, "meaning": "Grain commodity track, 0 to 10, never reset.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The face-down deck of the remaining cards this day.", "observable": false},
      {"key": "dock", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up Dock cards in order first, second, third.", "observable": false},
      {"key": "day", "type": "number", "visible": "public", "initial": 1, "meaning": "Current day, 1 to 3. It becomes 4 when the game is over.", "observable": true},
      {"key": "round_in_day", "type": "number", "visible": "public", "initial": 1, "meaning": "Round number within the day, 1 to 9.", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the active player this round (1=A, 2=B, 3=C).", "observable": false},
      {"key": "lot", "type": "list", "visible": "public", "initial": [], "meaning": "The cards in the current lot (the first lot_size Dock cards).", "observable": false},
      {"key": "lot_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the current lot.", "observable": false},
      {"key": "lot_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the card values in the current lot.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Current highest bid this auction (0 = no bid yet).", "observable": false},
      {"key": "high_bidder", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the current highest bidder (0 = nobody).", "observable": false}
    ]
  },
  "setup": [
    "Seats are fixed in order A (seat 1), B (seat 2), C (seat 3).",
    "Every player gets florins = 30, all three tracks = 0, an empty ship, ship_count = 0 and ship_value = 0.",
    "The three commodities Spice, Silk and Grain are shuffled, and one is dealt secretly into each player's patron. Every player has a different Patron and sees only their own.",
    "day = 1 and round_in_day = 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 1 (start of a day): set deck to all 30 cards (Spice, Silk and Grain, each valued 0,1,1,2,2,3,3,4,4,5). Empty every ship and set ship_count = 0 and ship_value = 0 for all players (tracks are NOT reset). Draw 3 cards at random from deck, removing them, and append them in order to dock (dock emptied first)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "active_seat = ((day - 1) + (round_in_day - 1)) mod 3 + 1. high_bid = 0, high_bidder = 0, lot = [], lot_size = 0, lot_value = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce day, round_in_day, active_seat, the dock in order, and every player's ship, ship_value, track_spice, track_silk, track_grain and florins."},
    {"action": "ask", "who": "the seat equal to active_seat", "answer": "a whole number from 1 to min(3, length of dock)", "effect": "lot_size = answer. lot = the first lot_size cards of dock. lot_value = sum of the values of the cards in lot. Announce the lot."},
    {"action": "ask", "who": "each player in turn: seat active_seat+1, then seat active_seat+2, then active_seat (seats counted mod 3)", "answer": "0 to pass, or a whole number at least max(1, high_bid + 1) and at most own florins. A seat with ship_count + lot_size > 5, or with florins <= high_bid, may only answer 0", "effect": "If answer > 0: high_bid = answer, high_bidder = this seat. Each later bidder hears the earlier bids."},
    {"action": "update", "who": "the seat equal to high_bidder", "answer": null, "effect": "If high_bidder > 0: that player's florins -= high_bid. Append every card of lot to their ship. ship_count += lot_size. ship_value += lot_value. For each commodity, add the number of lot cards of that commodity to the matching track, capped at 10. Whether or not anyone bid, remove the lot cards from dock (if nobody bid they are discarded)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Refill dock: while length of dock < 3 and deck is not empty, draw a random card from deck (remove it) and append it to the end of dock."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce who won the lot and for how much (high_bidder, high_bid), or that everyone passed and the lot was discarded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 9, ship scoring. Only players with ship_count > 0 take part. For each such player, h = number of participants with a higher ship_value and e = number of participants with an equal ship_value (self included). The player occupies places h+1 to h+e. Prizes are place 1 = 20, place 2 = 10, place 3 = 0. florins += floor((sum of the prizes for places h+1..h+e) / e). Players with ship_count == 0 get nothing."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 9, for each commodity in Spice, Silk, Grain: only players with that track > 0 take part. For each such player, h = participants with a higher track and e = participants with an equal track (self included). Prizes are place 1 = 10, place 2 = 5, place 3 = 0. award = floor((sum of the prizes for places h+1..h+e) / e) and florins += award. If that commodity equals the player's patron, florins += award again (Patron bonus)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round_in_day += 1. If round_in_day > 9: day += 1 and round_in_day = 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When day > 3: reveal every player's patron and announce final florins."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If day > 3, end the game. Otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "day > 3",
    "rank_by": "you.florins",
    "decided_by": "After the day 3 end-of-day scoring, each player's standing is their florins. The player with the most florins wins. Players tied for the most share the top, which the source calls a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then each player has 30 florins, all three tracks at 0, an empty ship, and a secret patron that differs from the other two players' patrons."},
    {"id": "R2", "text": "When a day starts (round_in_day == 1), then the deck is reset to the 30 cards, every ship is emptied with ship_count 0 and ship_value 0, tracks keep their values, and the dock holds 3 cards drawn from the deck."},
    {"id": "R3", "text": "When it is day d and round r of that day, then active_seat = ((d-1)+(r-1)) mod 3 + 1, so A is active first on day 1, B on day 2 and C on day 3."},
    {"id": "R4", "text": "When the active player chooses a lot size, then it is 1, 2 or 3 and no more than the number of dock cards, and the lot is the first that many dock cards."},
    {"id": "R5", "text": "When the auction runs, then the seat after the active seat bids first, then the other non-active seat, then the active seat last, each exactly once."},
    {"id": "R6", "text": "When a player bids, then the bid is at least 1, higher than the current high_bid, and at most their florins. Otherwise they pass (answer 0)."},
    {"id": "R7", "text": "When a player's ship_count + lot_size > 5, then that player may only pass."},
    {"id": "R8", "text": "When at least one player bid, then the highest bidder loses exactly high_bid florins, and their ship gains every lot card, ship_count rises by lot_size and ship_value rises by lot_value."},
    {"id": "R9", "text": "When a player loads a card, then their track in that card's commodity rises by 1, but never above 10."},
    {"id": "R10", "text": "When every player passes, then the lot is discarded and no florins, ships or tracks change."},
    {"id": "R11", "text": "When a lot is resolved, then its cards leave the dock, the remaining dock cards keep their order, and the dock is refilled to 3 from the deck, or fewer if the deck is empty."},
    {"id": "R12", "text": "When round 9 of a day ends, then among players with non-empty ships the highest ship_value gains 20 florins and the second gains 10."},
    {"id": "R13", "text": "When players tie in ship scoring, then they add the prizes of the places they occupy and each gets the sum divided equally, rounded down: two tied first get 15 each, three tied first get 10 each, two tied second get 5 each."},
    {"id": "R14", "text": "When a player's ship is empty at end of day, then they get no ship prize."},
    {"id": "R15", "text": "When round 9 of a day ends, then for each commodity the highest track (above 0) gains 10 florins and the second highest gains 5, with ties split as in R13 (two tied first get 7 each, two tied second get 2 each, three tied first get 5 each)."},
    {"id": "R16", "text": "When a player's track in a commodity is 0, then they earn no majority award in that commodity."},
    {"id": "R17", "text": "When a player earns a majority award in the commodity equal to their patron, then they gain that same amount again."},
    {"id": "R18", "text": "When the day 3 scoring is done, then the patrons are revealed and the game ends."},
    {"id": "R19", "text": "When the game ends, then the player with the most florins wins, and players tied for the most share the result (a draw)."}
  ],
  "offers": [
    {"question": "Lot size", "who": "the active seat only", "options": "the whole numbers 1 to min(3, number of dock cards). With a full dock this is 1, 2 or 3."},
    {"question": "Auction bid", "who": "each seat once, starting after the active seat and ending with the active seat", "options": "a seat with ship_count + lot_size <= 5 and florins > high_bid: 0 (pass) or any whole number from max(1, high_bid+1) to its florins. A seat whose ship lacks room, or whose florins do not exceed high_bid: 0 (pass) only."}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed 3 seats. The game needs exactly three different Patrons for the three commodities, so the count cannot change. The strategy lies in reading rivals' Patrons from their bidding and hiding your own while still building your Patron track."},
    {"what": "No free-text talk step", "why": "The source rules have no negotiation phase. Adding talk would be a new mechanic."},
    {"what": "A pass is answered as bid 0", "why": "This keeps the bid as one whole-number answer. 0 can never be a legal bid because the minimum is 1."},
    {"what": "Players with an empty ship, or a track at 0, are left out of the ranking and occupy no place", "why": "The source says they earn nothing but does not say whether they occupy a place. Leaving them out lets the other players take the prizes in order."},
    {"what": "Third place earns 0 in the tie-split arithmetic", "why": "Only first and second prizes exist, so a place beyond second contributes 0 to a tied group's sum."},
    {"what": "Cards are written as 'Commodity-value' text in lists", "why": "This lets one card carry both its commodity, for tracks, and its value, for ship_value."}
  ],
  "simplifications": [
    {"what": "A tie for the most florins is a shared win at the top, not a separate draw", "why": "The engine has no draw outcome. Tied leaders sharing the win expresses the same result."},
    {"what": "Start-of-day and end-of-day work are single updates with a round_in_day condition", "why": "The engine runs one flat round list. Each conditional step is a single arithmetic update, not a separate block."}
  ],
  "unsupported": []
}
```

Why it was refused: parameters must map each name to a number
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "Medici: Secret Patrons",
  "summary": "Three merchants auction lots of commodity cards from a dock over 3 days of 9 rounds. They score for ship value, for commodity track majorities and a second time for majorities in their own secret Patron commodity. The most florins wins.",
  "players": {"min": 3, "max": 3, "suggested": 3},
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
      {"key": "florins", "type": "number", "visible": "public", "initial": 30, "meaning": "Money, and also the score.", "observable": true},
      {"key": "patron", "type": "text", "visible": "ally", "initial": "", "meaning": "The secret Patron commodity (Spice, Silk or Grain). Each player holds a different one. It is revealed at game end.", "observable": false},
      {"key": "ship", "type": "list", "visible": "public", "initial": [], "meaning": "Cards loaded on the ship this day, written as 'Commodity-value', e.g. 'Silk-3'.", "observable": false},
      {"key": "ship_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards on the ship (at most 5).", "observable": false},
      {"key": "ship_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the values of the cards on the ship.", "observable": false},
      {"key": "track_spice", "type": "number", "visible": "public", "initial": 0, "meaning": "Spice commodity track, 0 to 10, never reset.", "observable": true},
      {"key": "track_silk", "type": "number", "visible": "public", "initial": 0, "meaning": "Silk commodity track, 0 to 10, never reset.", "observable": true},
      {"key": "track_grain", "type": "number", "visible": "public", "initial": 0, "meaning": "Grain commodity track, 0 to 10, never reset.", "observable": true}
    ],
    "game": [
      {"key": "deck", "type": "list", "visible": "none", "initial": [], "meaning": "The face-down deck of the cards remaining this day.", "observable": false},
      {"key": "dock", "type": "list", "visible": "public", "initial": [], "meaning": "Face-up Dock cards in order first, second, third.", "observable": false},
      {"key": "day", "type": "number", "visible": "public", "initial": 1, "meaning": "Current day, 1 to 3. It becomes 4 when the game is over.", "observable": true},
      {"key": "round_in_day", "type": "number", "visible": "public", "initial": 1, "meaning": "Round number within the day, 1 to 9.", "observable": false},
      {"key": "active_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "Seat of the active player this round (1=A, 2=B, 3=C).", "observable": false},
      {"key": "lot", "type": "list", "visible": "public", "initial": [], "meaning": "The cards in the current lot (the first lot_size Dock cards).", "observable": false},
      {"key": "lot_size", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of cards in the current lot.", "observable": false},
      {"key": "lot_value", "type": "number", "visible": "public", "initial": 0, "meaning": "Sum of the card values in the current lot.", "observable": false},
      {"key": "high_bid", "type": "number", "visible": "public", "initial": 0, "meaning": "Current highest bid in this auction (0 = no bid yet).", "observable": false},
      {"key": "high_bidder", "type": "number", "visible": "public", "initial": 0, "meaning": "Seat of the current highest bidder (0 = nobody).", "observable": false}
    ]
  },
  "setup": [
    "Seats are fixed in order A (seat 1), B (seat 2), C (seat 3).",
    "Every player gets florins = 30, all three tracks = 0, an empty ship, ship_count = 0 and ship_value = 0.",
    "The three commodities Spice, Silk and Grain are shuffled, and one is dealt secretly into each player's patron. Every player has a different Patron and sees only their own.",
    "day = 1 and round_in_day = 1."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 1 (start of a day): set deck to all 30 cards (Spice, Silk and Grain, each valued 0,1,1,2,2,3,3,4,4,5). Empty every ship and set ship_count = 0 and ship_value = 0 for all players (tracks are NOT reset). Empty dock, then draw 3 cards at random from deck, removing them, and append them in order to dock."},
    {"action": "update", "who": "all players", "answer": null, "effect": "active_seat = ((day - 1) + (round_in_day - 1)) mod 3 + 1. high_bid = 0, high_bidder = 0, lot = [], lot_size = 0, lot_value = 0."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce day, round_in_day, active_seat, the dock in order, and every player's ship, ship_value, track_spice, track_silk, track_grain and florins."},
    {"action": "ask", "who": "the seat equal to active_seat", "answer": "a whole number from 1 to min(3, length of dock)", "effect": "lot_size = answer. lot = the first lot_size cards of dock. lot_value = sum of the values of the cards in lot. Announce the lot."},
    {"action": "ask", "who": "each player in turn: seat active_seat+1, then seat active_seat+2, then active_seat (seats counted mod 3)", "answer": "0 to pass, or a whole number at least max(1, high_bid + 1) and at most own florins. A seat with ship_count + lot_size > 5, or with florins <= high_bid, may only answer 0", "effect": "If answer > 0: high_bid = answer, high_bidder = this seat. Each later bidder hears the earlier bids."},
    {"action": "update", "who": "the seat equal to high_bidder", "answer": null, "effect": "If high_bidder > 0: that player's florins -= high_bid. Append every card of lot to their ship. ship_count += lot_size. ship_value += lot_value. For each commodity, add the number of lot cards of that commodity to the matching track, capped at 10. Whether or not anyone bid, remove the lot cards from dock (if nobody bid they are discarded)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Refill dock: while length of dock < 3 and deck is not empty, draw a random card from deck (remove it) and append it to the end of dock."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce who won the lot and for how much (high_bidder, high_bid), or that everyone passed and the lot was discarded."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 9, ship scoring. Only players with ship_count > 0 take part. For each such player, h = number of participants with a higher ship_value and e = number of participants with an equal ship_value (self included). The player occupies places h+1 to h+e. Prizes are place 1 = 20, place 2 = 10, place 3 = 0. florins += floor((sum of the prizes for places h+1..h+e) / e). Players with ship_count == 0 get nothing."},
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_day == 9, for each commodity in Spice, Silk, Grain: only players with that track > 0 take part. For each such player, h = participants with a higher track and e = participants with an equal track (self included). Prizes are place 1 = 10, place 2 = 5, place 3 = 0. award = floor((sum of the prizes for places h+1..h+e) / e) and florins += award. If that commodity equals the player's patron, florins += award again (Patron bonus)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round_in_day += 1. If round_in_day > 9: day += 1 and round_in_day = 1."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "When day > 3: reveal every player's patron and announce final florins."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If day > 3, end the game. Otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "day > 3",
    "rank_by": "you.florins",
    "decided_by": "After the day 3 end-of-day scoring, each player's standing is their florins. The player with the most florins wins. Players tied for the most share the top, which the source calls a draw."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, then each player has 30 florins, all three tracks at 0, an empty ship, and a secret patron that differs from the other two players' patrons."},
    {"id": "R2", "text": "When a day starts (round_in_day == 1), then the deck is reset to the 30 cards, every ship is emptied with ship_count 0 and ship_value 0, tracks keep their values, and the dock holds 3 cards drawn from the deck."},
    {"id": "R3", "text": "When it is day d and round r of that day, then active_seat = ((d-1)+(r-1)) mod 3 + 1, so A is active first on day 1, B on day 2 and C on day 3."},
    {"id": "R4", "text": "When the active player chooses a lot size, then it is 1, 2 or 3 and no more than the number of dock cards, and the lot is the first that many dock cards."},
    {"id": "R5", "text": "When the auction runs, then the seat after the active seat bids first, then the other non-active seat, then the active seat last, each exactly once."},
    {"id": "R6", "text": "When a player bids, then the bid is at least 1, higher than the current high_bid, and at most their florins. Otherwise they pass (answer 0)."},
    {"id": "R7", "text": "When a player's ship_count + lot_size > 5, then that player may only pass."},
    {"id": "R8", "text": "When at least one player bid, then the highest bidder loses exactly high_bid florins, and their ship gains every lot card, ship_count rises by lot_size and ship_value rises by lot_value."},
    {"id": "R9", "text": "When a player loads a card, then their track in that card's commodity rises by 1, but never above 10."},
    {"id": "R10", "text": "When every player passes, then the lot is discarded and no florins, ships or tracks change."},
    {"id": "R11", "text": "When a lot is resolved, then its cards leave the dock, the remaining dock cards keep their order, and the dock is refilled to 3 from the deck, or fewer if the deck is empty."},
    {"id": "R12", "text": "When round 9 of a day ends, then among players with non-empty ships the highest ship_value gains 20 florins and the second gains 10."},
    {"id": "R13", "text": "When players tie in ship scoring, then they add the prizes of the places they occupy and each gets the sum divided equally, rounded down: two tied first get 15 each, three tied first get 10 each, two tied second get 5 each."},
    {"id": "R14", "text": "When a player's ship is empty at end of day, then they get no ship prize."},
    {"id": "R15", "text": "When round 9 of a day ends, then for each commodity the highest track (above 0) gains 10 florins and the second highest gains 5, with ties split as in R13 (two tied first get 7 each, two tied second get 2 each, three tied first get 5 each)."},
    {"id": "R16", "text": "When a player's track in a commodity is 0, then they earn no majority award in that commodity."},
    {"id": "R17", "text": "When a player earns a majority award in the commodity equal to their patron, then they gain that same amount again."},
    {"id": "R18", "text": "When the day 3 scoring is done, then the patrons are revealed and the game ends."},
    {"id": "R19", "text": "When the game ends, then the player with the most florins wins, and players tied for the most share the result (a draw)."}
  ],
  "offers": [
    {"question": "Lot size", "who": "the active seat only", "options": "the whole numbers 1 to min(3, number of dock cards). With a full dock this is 1, 2 or 3."},
    {"question": "Auction bid", "who": "each seat once, starting after the active seat and ending with the active seat", "options": "a seat with ship_count + lot_size <= 5 and florins > high_bid: 0 (pass) or any whole number from max(1, high_bid+1) to its florins. A seat whose ship lacks room, or whose florins do not exceed high_bid: 0 (pass) only."}
  ],
  "choices": [
    {"what": "Exactly 3 players, suggested 3", "why": "The designer fixed 3 seats. The game needs exactly three different Patrons for the three commodities, so the count cannot change. The strategy lies in reading rivals' Patrons from their bidding and hiding your own while still building your Patron track."},
    {"what": "No free-text talk step", "why": "The source rules have no negotiation phase. Adding talk would be a new mechanic."},
    {"what": "A pass is answered as bid 0", "why": "This keeps the bid as one whole-number answer. 0 can never be a legal bid because the minimum is 1."},
    {"what": "Players with an empty ship, or a track at 0, are left out of the ranking and occupy no place", "why": "The source says they earn nothing but does not say whether they occupy a place. Leaving them out lets the other players take the prizes in order."},
    {"what": "Third place earns 0 in the tie-split arithmetic", "why": "Only first and second prizes exist, so a place beyond second contributes 0 to a tied group's sum."},
    {"what": "Cards are written as 'Commodity-value' text in lists", "why": "This lets one card carry both its commodity, for tracks, and its value, for ship_value."},
    {"what": "The card value list is given as separate copy-count parameters", "why": "Parameters must each be a single number. The values 0,1,1,2,2,3,3,4,4,5 are written as how many copies of each value every commodity has."}
  ],
  "simplifications": [
    {"what": "A tie for the most florins is a shared win at the top, not a separate draw", "why": "The engine has no draw outcome. Tied leaders sharing the win expresses the same result."},
    {"what": "Start-of-day and end-of-day work are single updates with a round_in_day condition", "why": "The engine runs one flat round list. Each conditional step is a single arithmetic update, not a separate block."}
  ],
  "unsupported": []
}
```
````
