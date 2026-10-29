# 19 scenarios

- time: 2026-10-27T18:37:54+00:00 (124.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 f1d937b4bf5e09a1, reply sha256 421d0686d225fe5c

## Sent

````
SPEC:
{
  "name": "Medici: Sealed Harbour",
  "summary": "Three Florentine merchants spend 3 days auctioning commodity cards in sealed-bid rounds against a seller's secret reserve, filling 3-card ships for ship prizes and secret patron bonuses; the most florins wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "start_florins": 25,
    "deck_size": 20,
    "commodity_count": 4,
    "card_value_min": 1,
    "card_value_max": 5,
    "patron_commodities_dealt": 3,
    "days": 3,
    "rounds_per_day": 6,
    "total_rounds": 18,
    "ship_capacity": 3,
    "sales_per_player_per_day": 2,
    "reserve_min": 1,
    "reserve_max": 6,
    "bid_min": 0,
    "bid_max": 10,
    "first_ship_prize": 12,
    "second_ship_prize": 6,
    "patron_bonus_per_card": 3,
    "empty_slot_penalty": 2,
    "florin_floor": 0
  },
  "attributes": {
    "player": [
      {
        "key": "florins",
        "type": "number",
        "visible": "public",
        "initial": 25,
        "meaning": "The player's florins. This is the score.",
        "observable": true
      },
      {
        "key": "patron",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The player's secret patron commodity, dealt from patron_pool.",
        "observable": false
      },
      {
        "key": "ship",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Cards loaded on the player's ship today, at most 3, such as 'Spice 4'. Public because every lot and buyer is announced.",
        "observable": false
      },
      {
        "key": "ship_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of cards in ship (0 to 3).",
        "observable": false
      },
      {
        "key": "ship_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Sum of the card values in ship.",
        "observable": false
      },
      {
        "key": "patron_cards",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Number of cards in ship whose commodity equals patron.",
        "observable": false
      },
      {
        "key": "reserve",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The secret reserve price set while this player is seller (1 to 6).",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid (0 to 10, 0 = pass). Revealed at the reveal step.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "patron_pool",
        "type": "list",
        "visible": "none",
        "initial": [
          "Grain",
          "Cloth",
          "Spice",
          "Dye"
        ],
        "meaning": "Commodities from which patrons are dealt. The one left over is nobody's patron.",
        "observable": false
      },
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The day's deck: the 20 cards Grain/Cloth/Spice/Dye x values 1-5, refilled at the start of each day.",
        "observable": false
      },
      {
        "key": "day",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current day (1 to 3).",
        "observable": true
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current round overall (1 to 18).",
        "observable": true
      },
      {
        "key": "seller",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of this round's seller.",
        "observable": false
      },
      {
        "key": "lot",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The card drawn this round.",
        "observable": false
      },
      {
        "key": "lot_commodity",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Commodity of lot.",
        "observable": false
      },
      {
        "key": "lot_value",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Value (1 to 5) of lot.",
        "observable": false
      },
      {
        "key": "buyer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that loaded the lot this round. 0 if the lot was discarded.",
        "observable": false
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Florins paid for the lot this round.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each receive florins = 25.",
    "Three commodities are drawn at random from patron_pool, one into each player's patron. The fourth stays in patron_pool and is nobody's patron.",
    "Each player sees only their own patron.",
    "Set day = 1 and round = 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When (round - 1) mod 6 == 0 (start of a day): set deck to the full 20 cards (each of Grain, Cloth, Spice, Dye with each value 1-5). Every player's ship = [], ship_count = 0, ship_value = 0, patron_cards = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Set seller = ((day - 1) + ((round - 1) mod 6)) mod 3 + 1. Day 1 runs 1,2,3,1,2,3, day 2 runs 2,3,1,2,3,1, and day 3 runs 3,1,2,3,1,2."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Draw: remove one card at random from deck and set lot to it. Set lot_commodity and lot_value from that card. Announce the lot to everyone."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "All messages are shown together: broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. The talk is not binding."
    },
    {
      "action": "ask",
      "who": "seat seller",
      "answer": "whole number 1 to 6",
      "effect": "The seller's reserve = the answer, kept secret."
    },
    {
      "action": "poll",
      "who": "the two players other than seller",
      "answer": "whole number 0 to min(10, you.florins); exactly 0 if you.ship_count >= 3",
      "effect": "Each non-seller's bid = the answer, sealed until all bids are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Resolve. Let R = seller's reserve. Let F = (seller mod 3) + 1, the first bidder clockwise after the seller. Case A, at least one non-seller bid >= R: the winner is the non-seller with the higher bid among those with bid >= R; if the two bids are equal, F wins. The winner's florins -= bid and the seller's florins += that bid. Set buyer = winner and price = bid. Case B, no bid >= R: if the seller's ship_count < 3, set buyer = seller, price = min(R, seller.florins), and seller.florins -= price, paid to the bank; otherwise set buyer = 0 and price = 0, and the lot is discarded. If buyer != 0: append lot to buyer's ship, buyer.ship_count += 1, buyer.ship_value += lot_value, and if lot_commodity == buyer.patron then buyer.patron_cards += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal to everyone: the seller's reserve, both non-sellers' bids, the buyer (or 'discarded'), and the price."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When round mod 6 == 0 (end of day), in this order. (1) Ship prize: for each player with ship_count > 0, let h = the number of players with ship_count > 0 and a higher ship_value, and k = the number of players with ship_count > 0 and an equal ship_value (including themself). Those players occupy places h+1 to h+k. Place prizes are 12 for place 1, 6 for place 2 and 0 otherwise. The player gains floor(sum of the prizes for places h+1..h+k / k). Players with ship_count == 0 gain nothing. (2) Patron bonus: florins += 3 * patron_cards. (3) Empty-slot penalty: florins = max(0, florins - 2 * (3 - ship_count)). (4) Reset: ship = [], ship_count = 0, ship_value = 0, patron_cards = 0, and day += 1."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round > 18. Otherwise continue with the next round."
    }
  ],
  "ending": {
    "condition": "round > 18",
    "rank_by": "you.florins",
    "decided_by": "After the end-of-day scoring of day 3, each player's standing is their florins. The most florins wins, and players tied for most share the win (a draw between them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each of the 3 players has 25 public florins."
    },
    {
      "id": "R2",
      "text": "When the game starts, then 3 of the 4 commodities (Grain, Cloth, Spice, Dye) are dealt at random as secret patrons, one per player, and the fourth is nobody's patron."
    },
    {
      "id": "R3",
      "text": "When a player's patron is dealt, then only that player can see it."
    },
    {
      "id": "R4",
      "text": "When a day starts (rounds 1, 7 and 13), then the deck holds all 20 cards (4 commodities x values 1-5) and every ship is empty."
    },
    {
      "id": "R5",
      "text": "When it is round r of day d (r = 0 to 5 within the day), then the seller is seat ((d-1)+r) mod 3 + 1, so day 1 starts with seat 1, day 2 with seat 2 and day 3 with seat 3."
    },
    {
      "id": "R6",
      "text": "When a day is played, then each player is seller exactly 2 times."
    },
    {
      "id": "R7",
      "text": "When a round begins, then one card is drawn at random from the deck as the lot and shown to everyone."
    },
    {
      "id": "R8",
      "text": "When the talk step runs, then all 3 players submit a message at the same time and all messages are shown to everyone afterwards."
    },
    {
      "id": "R9",
      "text": "When the seller sets a reserve, then it is a whole number from 1 to 6 and stays secret until the reveal."
    },
    {
      "id": "R10",
      "text": "When the two non-sellers bid, then they bid simultaneously, each a whole number from 0 to 10 and at most their current florins, where 0 means pass."
    },
    {
      "id": "R11",
      "text": "When a non-seller's ship holds 3 cards, then their only allowed bid is 0."
    },
    {
      "id": "R12",
      "text": "When at least one bid is >= the reserve, then the higher such bid wins, the winner pays their bid to the seller, and the winner loads the lot (for example, reserve 4 with bids 5 and 3: the 5-bidder pays 5 to the seller)."
    },
    {
      "id": "R13",
      "text": "When both bids are equal and >= the reserve, then the bidder at seat (seller mod 3)+1 wins (for example, seller 3 with bids of 6 and 6: seat 1 wins)."
    },
    {
      "id": "R14",
      "text": "When no bid reaches the reserve and the seller's ship holds fewer than 3 cards, then the seller loads the lot and pays the reserve to the bank."
    },
    {
      "id": "R15",
      "text": "When no bid reaches the reserve and the seller has fewer florins than the reserve, then the seller pays all their florins and still loads the lot if the ship has room."
    },
    {
      "id": "R16",
      "text": "When no bid reaches the reserve and the seller's ship holds 3 cards, then the lot is discarded and no one pays."
    },
    {
      "id": "R17",
      "text": "When a round resolves, then the reserve, both bids, the buyer and the price are announced to everyone."
    },
    {
      "id": "R18",
      "text": "When a ship holds 3 cards, then it can take no more cards that day."
    },
    {
      "id": "R19",
      "text": "When a day ends (after rounds 6, 12 and 18), then the highest ship value receives 12 florins and the second highest receives 6."
    },
    {
      "id": "R20",
      "text": "When players tie for ship value at day end, then they add the prizes for the places they occupy and split the sum equally, rounded down (two tied for first get floor(18/2) = 9 each; three tied get floor(18/3) = 6 each; two tied for second get floor(6/2) = 3 each)."
    },
    {
      "id": "R21",
      "text": "When a player's ship is empty at day end, then they receive no ship prize and occupy no place."
    },
    {
      "id": "R22",
      "text": "When a day ends, then each player gains 3 florins per card of their own patron commodity in their ship."
    },
    {
      "id": "R23",
      "text": "When a day ends, then each player pays 2 florins per empty ship slot (0 to 3 slots), and florins never drop below 0."
    },
    {
      "id": "R24",
      "text": "When day-end scoring is done, then all ships are emptied."
    },
    {
      "id": "R25",
      "text": "When round 18's day-end scoring is complete, then the game ends and the player with the most florins wins, with tied leaders sharing a draw."
    }
  ],
  "offers": [
    {
      "question": "Talk message",
      "who": "all three seats",
      "options": "Any short free-text message, every round."
    },
    {
      "question": "Reserve price",
      "who": "the seller only",
      "options": "A whole number from 1 to 6. Non-sellers are not asked."
    },
    {
      "question": "Sealed bid",
      "who": "the two non-sellers",
      "options": "A non-seller with ship_count < 3: a whole number from 0 to min(10, florins). A non-seller with ship_count = 3: 0 only. The seller is not asked."
    }
  ],
  "choices": [
    {
      "what": "3 players, min = max = suggested = 3",
      "why": "The designer fixed 3. The seller order, two sales each per day, two bidders per lot and the 12/6 two-place prize are all built for exactly 3 seats."
    },
    {
      "what": "Keep the simultaneous talk as a poll with broadcast",
      "why": "The source requires it. Talk earns its place because patrons are secret and players compete for the same lots, so bluffing about which commodity you want, or talking down a lot's value to the seller, can mislead rivals."
    },
    {
      "what": "Strategy at this table",
      "why": "A thoughtful player prices reserves to extract bids without being forced to buy junk, infers rivals' patrons from what they bid on, bids to deny a rival's ship prize, and avoids empty-slot penalties. A thoughtless one bids face value."
    },
    {
      "what": "Reading of the empty-ship prize rule",
      "why": "Players with empty ships are excluded from ranking entirely, so places are counted only among non-empty ships. The next non-empty ship can therefore take a prize."
    },
    {
      "what": "Day-end order: ship prize, patron bonus, then penalty with the floor at 0",
      "why": "The source lists them in this order and applies the floor only to the penalty."
    },
    {
      "what": "In case B, the seller loading their own patron commodity counts for the patron bonus",
      "why": "The patron bonus counts every patron card in the ship, however it was loaded."
    },
    {
      "what": "Reserve asked of the seller with a single-player ask",
      "why": "Only one seat answers, so ask and poll behave the same. The answer is kept in the seller's ally-visible reserve."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling and drawing the top card is done as drawing a random card from the deck list",
      "why": "Drawing at random is how the engine shuffles. The odds are the same."
    },
    {
      "what": "The bank is not tracked as an attribute",
      "why": "It has unlimited funds in the rules. Payments to and from it only change player florins."
    },
    {
      "what": "Ship contents are public lists",
      "why": "Every lot and buyer is announced to everyone, so the ships are already public information."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: florins; table: day, round.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite the full-ship scenario so it checks outcomes, not whether seat 1 was polled. Remove the `options_include` rule for the full-ship seat. Instead assert that seat 1 cannot win the lot: its ship stays at 3 cards and its florins are unchanged. Also assert that the lot goes to the other bidder if that bid reaches the reserve, or to the seller (who pays the reserve) otherwise. Assert on florins and the resulting ship contents only. Do not assert on internal bookkeeping such as bid_f or whose turn it is.
````

## Reply

````
```json
[
  {
    "name": "Each seat starts with 25 florins on day 1, round 1",
    "rule": "R1",
    "players": 3,
    "rounds": 0,
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 25}, "3": {"florins": 25}},
      "game": {"day": 1, "round": 1}
    }
  },
  {
    "name": "Three patrons are dealt and one commodity stays in the pool (which one is chance)",
    "rule": "R2",
    "players": 3,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"patron_pool": 1}},
      "players": {"1": {"florins": 25}, "2": {"florins": 25}, "3": {"florins": 25}}
    }
  },
  {
    "name": "Patron deal leaves one commodity undealt and no florins change",
    "rule": "R3",
    "players": 3,
    "rounds": 0,
    "expect": {
      "lens": {"game": {"patron_pool": 1}},
      "players": {"1": {"florins": 25}, "2": {"florins": 25}, "3": {"florins": 25}},
      "game": {"day": 1, "round": 1}
    }
  },
  {
    "name": "Start of day 2 refills the deck to 20 and empties stale ships",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12},
        "2": {"ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9},
        "3": {"ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6}
      },
      "game": {"day": 2, "round": 7, "deck": []}
    },
    "rules": [
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": 5},
      {"seat": 1, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 30}, "3": {"florins": 20}},
      "lens": {"game": {"deck": 19}, "players": {"1": {"ship": 0}, "2": {"ship": 0}, "3": {"ship": 1}}},
      "game": {"day": 2, "round": 8}
    }
  },
  {
    "name": "Day 3 starts with seat 3 as seller: seat 3 sets the reserve and buys it in when nobody bids",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"day": 3, "round": 13}},
    "rules": [
      {"seat": 3, "options_include": 6},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 25}, "3": {"florins": 19}},
      "lens": {"players": {"3": {"ship": 1}}}
    }
  },
  {
    "name": "Third round of day 2 (round 9) has seat 1 as seller",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {
      "game": {"day": 2, "round": 9, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 21}, "2": {"florins": 25}, "3": {"florins": 25}},
      "lens": {"players": {"1": {"ship": 1}}}
    }
  },
  {
    "name": "First five rounds of day 1 have sellers 1,2,3,1,2: each seller buys in at reserve 1",
    "rule": "R6",
    "players": 3,
    "rounds": 5,
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 1, "options_include": 1, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 1, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 1, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"florins": 23}, "2": {"florins": 23}, "3": {"florins": 24}},
      "lens": {"players": {"1": {"ship": 2}, "2": {"ship": 2}, "3": {"ship": 1}}},
      "game": {"day": 1, "round": 6}
    }
  },
  {
    "name": "Round 1 draws one lot from the fresh 20-card deck",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 23}, "2": {"florins": 25}, "3": {"florins": 25}},
      "lens": {"game": {"deck": 19}, "players": {"1": {"ship": 1}}}
    }
  },
  {
    "name": "Talk step runs and the round continues to resolution",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 1},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 24}, "2": {"florins": 25}, "3": {"florins": 25}},
      "game": {"round": 2}
    }
  },
  {
    "name": "Reserve ranges 1 to 6: 6 is accepted, 0 and 7 are not offered",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 19}, "2": {"florins": 25}, "3": {"florins": 25}},
      "offered": [{"seat": 1, "option": 6}],
      "not_offered": [{"seat": 1, "option": 7}, {"seat": 1, "option": 0}]
    }
  },
  {
    "name": "Bids are capped at min(10, florins): seat 2 with 4 florins bids up to 4",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"2": {"florins": 4}}},
    "rules": [
      {"seat": 1, "options_include": 3},
      {"seat": 2, "options_include": 4},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 29}, "2": {"florins": 0}, "3": {"florins": 25}},
      "offered": [{"seat": 2, "option": 4}, {"seat": 3, "option": 10}],
      "not_offered": [{"seat": 2, "option": 5}, {"seat": 3, "option": 11}]
    }
  },
  {
    "name": "Full-ship bidder cannot win: seat 3's bid meets the reserve and seat 3 loads the lot",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0}},
      "game": {"day": 1, "round": 2, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": 4}
    ],
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 29}, "3": {"florins": 21}},
      "lens": {"game": {"deck": 4}, "players": {"1": {"ship": 3}, "2": {"ship": 0}, "3": {"ship": 1}}},
      "not_offered": [{"seat": 1, "option": 1}]
    }
  },
  {
    "name": "Reserve 4, bids 5 and 3: the 5-bidder pays 5 to the seller",
    "rule": "R12",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 4},
      {"seat": 2, "options_include": 5},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "players": {"1": {"florins": 30}, "2": {"florins": 20}, "3": {"florins": 25}},
      "lens": {"players": {"1": {"ship": 0}, "2": {"ship": 1}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Seller 3, tied bids of 6: seat 1 wins and pays 6",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {"game": {"day": 1, "round": 3, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}},
    "rules": [
      {"seat": 3, "options_include": 4},
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 6}
    ],
    "expect": {
      "players": {"1": {"florins": 19}, "2": {"florins": 25}, "3": {"florins": 31}},
      "lens": {"players": {"1": {"ship": 1}, "2": {"ship": 0}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "No bid reaches reserve 5: seller loads the lot and pays 5 to the bank",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 5},
      {"seat": 2, "options_include": 2},
      {"seat": 3, "options_include": 4}
    ],
    "expect": {
      "players": {"1": {"florins": 20}, "2": {"florins": 25}, "3": {"florins": 25}},
      "lens": {"players": {"1": {"ship": 1}, "2": {"ship": 0}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Seller with 3 florins and reserve 6 pays all 3 and still loads the lot",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {"players": {"1": {"florins": 3}}},
    "rules": [
      {"seat": 1, "options_include": 6},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 0}, "2": {"florins": 25}, "3": {"florins": 25}},
      "lens": {"players": {"1": {"ship": 1}}}
    }
  },
  {
    "name": "Seller's ship full and no bid reaches the reserve: lot discarded, nobody pays",
    "rule": "R16",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0}},
      "game": {"day": 1, "round": 2, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 2, "options_include": 6},
      {"seat": 1, "options_include": 3},
      {"seat": 3, "options_include": 2}
    ],
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 25}, "3": {"florins": 25}},
      "lens": {"game": {"deck": 4}, "players": {"1": {"ship": 0}, "2": {"ship": 3}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Round resolves with tied bids of 3 over reserve 2: seat 2 (first after seller 1) pays 3",
    "rule": "R17",
    "players": 3,
    "rounds": 1,
    "rules": [
      {"seat": 1, "options_include": 2},
      {"seat": 2, "options_include": 3},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "players": {"1": {"florins": 28}, "2": {"florins": 22}, "3": {"florins": 25}},
      "lens": {"players": {"2": {"ship": 1}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Full ship takes no more cards: other bid misses reserve 5, seller 2 buys in, seat 1 unchanged",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0}},
      "game": {"day": 1, "round": 2, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 2, "options_include": 5},
      {"seat": 3, "options_include": 2}
    ],
    "expect": {
      "players": {"1": {"florins": 25}, "2": {"florins": 20}, "3": {"florins": 25}},
      "lens": {"players": {"1": {"ship": 3}, "2": {"ship": 1}, "3": {"ship": 0}}}
    }
  },
  {
    "name": "Day end: ship values 12/9/6 get prizes 12/6/0",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "players": {"1": {"florins": 37}, "2": {"florins": 31}, "3": {"florins": 25}},
      "game": {"day": 2, "round": 7}
    }
  },
  {
    "name": "Two tied for first with 12 split 18: 9 each; third gets 0",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "players": {"1": {"florins": 34}, "2": {"florins": 34}, "3": {"florins": 25}}
    }
  },
  {
    "name": "Three tied ship values split 18: 6 each",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 3", "Spice 3", "Dye 3"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 3", "Spice 3", "Dye 3"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 3", "Cloth 3", "Dye 3"], "ship_count": 3, "ship_value": 9, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "players": {"1": {"florins": 31}, "2": {"florins": 31}, "3": {"florins": 31}}
    }
  },
  {
    "name": "Two tied for second split 6: 3 each; first gets 12",
    "rule": "R20",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 4", "Cloth 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "players": {"1": {"florins": 37}, "2": {"florins": 28}, "3": {"florins": 28}}
    }
  },
  {
    "name": "Empty ship takes no place: the 9 and 6 ships get 12 and 6, empty ship pays 6 penalty",
    "rule": "R21",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": [], "ship_count": 0, "ship_value": 0, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 3, "options_include": 6},
      {"seat": 1, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 19}, "2": {"florins": 37}, "3": {"florins": 31}}
    }
  },
  {
    "name": "Patron bonus: two patron cards in ship add 6",
    "rule": "R22",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Grain 5", "Grain 4", "Cloth 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 2},
        "2": {"patron": "Cloth", "ship": ["Grain 3", "Spice 4", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "players": {"1": {"florins": 43}, "2": {"florins": 31}, "3": {"florins": 25}}
    }
  },
  {
    "name": "Empty-slot penalty 2 per slot, floored at 0",
    "rule": "R23",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"florins": 3, "patron": "Grain", "ship": [], "ship_count": 0, "ship_value": 0, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Dye 3"], "ship_count": 2, "ship_value": 7, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [
      {"seat": 3, "options_include": 6},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"florins": 0}, "2": {"florins": 35}, "3": {"florins": 31}}
    }
  },
  {
    "name": "After day-end scoring all ships are empty and day 2 begins",
    "rule": "R24",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 1, "round": 6, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 3, "options_include": 6}],
    "expect": {
      "lens": {"players": {"1": {"ship": 0}, "2": {"ship": 0}, "3": {"ship": 0}}},
      "players": {"1": {"florins": 37}, "2": {"florins": 31}, "3": {"florins": 25}},
      "game": {"day": 2, "round": 7}
    }
  },
  {
    "name": "Round 18 day-end scoring ends the game: seat 1 wins with 37",
    "rule": "R25",
    "players": 3,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 4", "Spice 3", "Dye 2"], "ship_count": 3, "ship_value": 9, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 3, "round": 18, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 2, "options_include": 6}],
    "expect": {
      "winner": 1,
      "standings": {"1": 37, "2": 31, "3": 25},
      "players": {"1": {"florins": 37}, "2": {"florins": 31}, "3": {"florins": 25}}
    }
  },
  {
    "name": "Round 18 ends with seats 1 and 2 tied on 34: shared win",
    "rule": "R25",
    "players": 3,
    "given": {
      "players": {
        "1": {"patron": "Grain", "ship": ["Cloth 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "2": {"patron": "Cloth", "ship": ["Grain 5", "Spice 4", "Dye 3"], "ship_count": 3, "ship_value": 12, "patron_cards": 0},
        "3": {"patron": "Spice", "ship": ["Grain 1", "Cloth 2", "Dye 3"], "ship_count": 3, "ship_value": 6, "patron_cards": 0}
      },
      "game": {"day": 3, "round": 18, "deck": ["Grain 1", "Cloth 2", "Spice 3", "Dye 4", "Grain 5"]}
    },
    "rules": [{"seat": 2, "options_include": 6}],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 34, "2": 34, "3": 25}
    }
  }
]
```
````
