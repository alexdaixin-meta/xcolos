# 05 scenarios

- time: 2026-10-27T16:42:22+00:00 (77.6s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 0e1774a8afb4773b, reply sha256 8ef245f44c1db7a9

## Sent

````
SPEC:
{
  "name": "Modern Art: Sealed Season",
  "summary": "Players auction paintings from their hands with a secret reserve and sealed bids, while trying to make the artists they own the most-played in each season, which raises those artists' value; most money after three seasons wins.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "starting_money": 100,
    "deck_size": 46,
    "red_cards": 10,
    "blue_cards": 11,
    "green_cards": 12,
    "yellow_cards": 13,
    "hand_size_3_players": 10,
    "hand_size_4_players": 8,
    "season_end_count": 4,
    "first_place_award": 30,
    "second_place_award": 20,
    "seasons_to_end": 3,
    "max_rounds": 32,
    "min_reserve": 0,
    "min_bid": 0,
    "artist_tiebreak_red": 3,
    "artist_tiebreak_blue": 2,
    "artist_tiebreak_green": 1,
    "artist_tiebreak_yellow": 0
  },
  "attributes": {
    "player": [
      {
        "key": "money",
        "type": "number",
        "visible": "ally",
        "initial": 100,
        "meaning": "The player's money, private to its owner until the end. This is the score.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Painting cards in hand, each an artist name (red, blue, green, yellow).",
        "observable": false
      },
      {
        "key": "paintings",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Face-up paintings bought this season, each an artist name.",
        "observable": true
      },
      {
        "key": "chosen_card",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The card the auctioneer secretly chose this round.",
        "observable": false
      },
      {
        "key": "reserve_choice",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The reserve price the auctioneer secretly chose this round.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid. It stays hidden until the announce step.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "10 red, 11 blue, 12 green, 13 yellow",
        "meaning": "The shuffled deck that hands are dealt from. The rest is unused.",
        "observable": false
      },
      {
        "key": "auctioneer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat number of the current auctioneer.",
        "observable": true
      },
      {
        "key": "current_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The artist of the card revealed this round.",
        "observable": true
      },
      {
        "key": "reserve",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The announced reserve price for this round.",
        "observable": true
      },
      {
        "key": "season_ended",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when the revealed card brought its artist's season count to 4.",
        "observable": false
      },
      {
        "key": "count_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red's season count.",
        "observable": true
      },
      {
        "key": "count_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue's season count.",
        "observable": true
      },
      {
        "key": "count_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green's season count.",
        "observable": true
      },
      {
        "key": "count_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Yellow's season count.",
        "observable": true
      },
      {
        "key": "value_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red's cumulative value.",
        "observable": true
      },
      {
        "key": "value_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue's cumulative value.",
        "observable": true
      },
      {
        "key": "value_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green's cumulative value.",
        "observable": true
      },
      {
        "key": "value_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Yellow's cumulative value.",
        "observable": true
      },
      {
        "key": "season",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "The current season number.",
        "observable": true
      },
      {
        "key": "seasons_scored",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "How many season scorings have happened.",
        "observable": true
      },
      {
        "key": "buyer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that took this round's painting (0 if none).",
        "observable": true
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Price paid for this round's painting.",
        "observable": true
      },
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Number of auctions started.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats are assigned in random order; seat 1 is the first auctioneer (auctioneer = 1).",
    "Every player's money is set to 100.",
    "The deck list is filled with 10 red, 11 blue, 12 green and 13 yellow cards.",
    "Each player draws cards at random from deck into hand: 10 each with 3 players, 8 each with 4 players. The remaining deck is unused.",
    "season = 1, seasons_scored = 0, and every count_<artist> and value_<artist> = 0.",
    "Each player is synced their own money and hand."
  ],
  "round": [
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "round_number += 1; season_ended = false; buyer = 0; price = 0; every player's bid = 0."
    },
    {
      "action": "ask",
      "who": "seat auctioneer",
      "answer": "one artist name present in own hand",
      "effect": "auctioneer.chosen_card = answer (kept secret)."
    },
    {
      "action": "ask",
      "who": "seat auctioneer",
      "answer": "whole number from 0 to auctioneer.money",
      "effect": "auctioneer.reserve_choice = answer (kept secret)."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "Remove one copy of auctioneer.chosen_card from auctioneer.hand; current_artist = chosen_card; count_<current_artist> += 1; season_ended = (count_<current_artist> == 4). Announce the artist to all."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "When season_ended is false: reserve = auctioneer.reserve_choice and the reserve is announced to all. When season_ended is true: announce that the card is discarded unsold and the season ends (the reserve is ignored)."
    },
    {
      "action": "poll",
      "who": "all players (when season_ended is false)",
      "answer": "one short text message",
      "effect": "Messages are broadcast to all: {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. They are not binding."
    },
    {
      "action": "poll",
      "who": "all players except the auctioneer (when season_ended is false)",
      "answer": "whole number from 0 to own money",
      "effect": "Each bidder's bid = answer, hidden until all bids are in."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "When season_ended is false: the eligible bids are those with bid >= reserve. If any exist, buyer = the highest eligible bidder, with ties going to the tied seat that comes first in seat order after the auctioneer; price = buyer.bid; buyer.money -= price; auctioneer.money += price; append current_artist to buyer.paintings. Otherwise buyer = auctioneer; price = reserve; auctioneer.money -= reserve (the money leaves the game); append current_artist to auctioneer.paintings."
    },
    {
      "action": "tell",
      "who": "all players (when season_ended is false)",
      "answer": null,
      "effect": "Announce every bidder's bid, the buyer and the price."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "When season_ended is true or the sum of hand sizes == 0, score the season. (a) Each artist's key = count*4 + tiebreak (red 3, blue 2, green 1, yellow 0); first = the highest key, second = the next highest. (b) value_<first> += 30; if count_<second> > 0 then value_<second> += 20, otherwise second scores nothing. (c) Each player's money += value_<first> times the number of first in paintings, plus (if count_<second> > 0) value_<second> times the number of second in paintings. (d) Every paintings list is emptied; every count_<artist> = 0; season += 1; seasons_scored += 1. Announce the new values and payouts."
    },
    {
      "action": "check",
      "who": "engine",
      "answer": null,
      "effect": "End the game if seasons_scored >= 3, or the sum of hand sizes == 0, or round_number >= 32; otherwise continue."
    },
    {
      "action": "update",
      "who": "engine",
      "answer": null,
      "effect": "auctioneer = the next seat in seat order after the current auctioneer whose hand is not empty. Seats with empty hands are skipped as auctioneer but still bid."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own money and hand, plus the public state."
    }
  ],
  "ending": {
    "condition": "seasons_scored >= 3 or sum over players of size(hand) == 0 or round_number >= 32",
    "rank_by": "you.money",
    "decided_by": "Each player's standing is their final money; it is revealed at the end and the most money wins. Players tied at the top share the win (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has 100 money, visible only to its owner."
    },
    {
      "id": "R2",
      "text": "When there are 3 players, then each is dealt 10 cards; when there are 4 players, then each is dealt 8 cards, from a 46-card deck of 10 red, 11 blue, 12 green and 13 yellow."
    },
    {
      "id": "R3",
      "text": "When a round begins, then the auctioneer secretly picks one card from their hand and a reserve from 0 to their current money."
    },
    {
      "id": "R4",
      "text": "When the card is revealed, then it leaves the auctioneer's hand, its artist is announced, and that artist's season count rises by 1."
    },
    {
      "id": "R5",
      "text": "When the revealed card brings its artist's season count to 4, then the card is discarded unsold, the reserve is ignored, there is no talk or bidding, and season scoring happens."
    },
    {
      "id": "R6",
      "text": "When the season does not end on the reveal, then the reserve is announced to everyone."
    },
    {
      "id": "R7",
      "text": "When the season does not end on the reveal, then every player including the auctioneer submits one short message simultaneously, and all messages are shown to everyone."
    },
    {
      "id": "R8",
      "text": "When bidding happens, then every player except the auctioneer submits a sealed bid from 0 to their own current money, simultaneously."
    },
    {
      "id": "R9",
      "text": "When at least one bid is >= the reserve, then the highest such bidder pays their bid to the auctioneer and appends the painting to their paintings."
    },
    {
      "id": "R10",
      "text": "When the highest eligible bids tie, then the tied bidder first in seat order after the auctioneer wins."
    },
    {
      "id": "R11",
      "text": "When no bid reaches the reserve, then the auctioneer pays the reserve to the bank (money leaves the game) and takes the painting."
    },
    {
      "id": "R12",
      "text": "When an auction resolves, then all bids, the buyer and the price are announced publicly."
    },
    {
      "id": "R13",
      "text": "When season scoring happens, then artists are ranked by season count with ties to the earlier of red, blue, green, yellow; the first gains 30 cumulative value and the second gains 20 unless its count is 0."
    },
    {
      "id": "R14",
      "text": "When season scoring happens, then each player gains, for each painting they own of a ranked artist, that artist's cumulative value after the increase; paintings of unranked artists pay 0."
    },
    {
      "id": "R15",
      "text": "When season scoring finishes, then all paintings are discarded, all season counts reset to 0, and the season number rises by 1."
    },
    {
      "id": "R16",
      "text": "When every hand is empty after an auction, then the current season is scored and the game ends."
    },
    {
      "id": "R17",
      "text": "When the third season scoring is done, then the game ends."
    },
    {
      "id": "R18",
      "text": "When the game would pass 32 rounds, then it ends."
    },
    {
      "id": "R19",
      "text": "When the auctioneer rotates, then it passes to the next seat in order holding at least one card; empty-handed players still bid."
    },
    {
      "id": "R20",
      "text": "When the game ends, then the player with the most money wins, and players tied for most share the result."
    },
    {
      "id": "R21",
      "text": "Money never goes below 0, because bids and reserves are capped at the player's current money."
    }
  ],
  "offers": [
    {
      "question": "Auctioneer chooses a card",
      "who": "the auctioneer",
      "options": "each distinct artist name (red, blue, green, yellow) that appears at least once in the auctioneer's hand"
    },
    {
      "question": "Auctioneer chooses a reserve",
      "who": "the auctioneer",
      "options": "any whole number from 0 to the auctioneer's current money"
    },
    {
      "question": "Talk",
      "who": "every seat including the auctioneer, only when the season did not end on the reveal",
      "options": "one short free-text message"
    },
    {
      "question": "Sealed bid",
      "who": "every seat except the auctioneer, including empty-handed seats, only when the season did not end on the reveal",
      "options": "any whole number from 0 to that seat's current money"
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "Kept from the designer. The minimum is 3 because a sealed auction needs at least two rival bidders against the auctioneer. The maximum is 4 because the 46-card deck and the 32-round limit are sized for it (4 x 8 = 32 cards)."
    },
    {
      "what": "Talk kept as a simultaneous poll before the bids",
      "why": "The rules say messages are written at the same time. Players disagree about which artists should rise, since each holds different hands and paintings, so talk gives material for bluffing and persuasion."
    },
    {
      "what": "Artist ranking computed as count*4 + tiebreak (red 3, blue 2, green 1, yellow 0)",
      "why": "Turns 'rank by count, ties by artist order' into arithmetic. Counts never exceed 4, so the tiebreak never outweighs a count difference."
    },
    {
      "what": "The auctioneer picks an artist name instead of a specific card",
      "why": "Cards of the same artist are identical, so naming the artist is equivalent."
    },
    {
      "what": "Cards the auctioneer chooses that end the season are revealed before the reserve is announced",
      "why": "Follows the step order: the reserve is chosen secretly, then announced only if the season did not end."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for most money is a shared win rather than a declared draw",
      "why": "The engine ranks by one expression and players level at the top share the win; there is no separate draw outcome."
    },
    {
      "what": "The card choice and the reserve choice are two consecutive questions to the auctioneer",
      "why": "A question takes one answer; both stay secret until the reveal, so nothing changes."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, paintings; table: auctioneer, current_artist, reserve, count_red, count_blue, count_green, count_yellow, value_red, value_blue, value_green, value_yellow, season, seasons_scored, buyer, price.
````

## Reply

````
[
  {"name": "Every player starts with 100 money", "rule": "R1", "players": 3, "rounds": 0,
   "expect": {"players": {"1": {"money": 100}, "2": {"money": 100}, "3": {"money": 100}}}},

  {"name": "3 players are dealt 10 cards each from the 46-card deck", "rule": "R2", "players": 3, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 16}, "players": {"1": {"hand": 10}, "2": {"hand": 10}, "3": {"hand": 10}}}}},

  {"name": "4 players are dealt 8 cards each from the 46-card deck", "rule": "R2", "players": 4, "rounds": 0,
   "expect": {"lens": {"game": {"deck": 14}, "players": {"1": {"hand": 8}, "2": {"hand": 8}, "3": {"hand": 8}, "4": {"hand": 8}}}}},

  {"name": "Auctioneer picks a card from own hand and a reserve up to own money", "rule": "R3", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["red", "blue"], "money": 100}, "2": {"hand": ["green"]}, "3": {"hand": ["yellow"]}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"current_artist": "blue", "reserve": 0},
              "offered": [{"seat": 1, "option": "red"}, {"seat": 1, "option": "blue"}, {"seat": 1, "option": 100}],
              "not_offered": [{"seat": 1, "option": "green"}, {"seat": 1, "option": "yellow"}, {"seat": 1, "option": 101}]}},

  {"name": "Revealed card leaves the hand and raises its artist's count", "rule": "R4", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"]}, "2": {"hand": ["green"]}, "3": {"hand": ["yellow"]}},
             "game": {"auctioneer": 1, "count_blue": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"current_artist": "blue", "count_blue": 2}, "lens": {"players": {"1": {"hand": 1}}}}},

  {"name": "Fourth card of an artist is discarded unsold, no bidding, season is scored", "rule": "R5", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["red", "blue"], "paintings": []}, "2": {"hand": ["green"], "paintings": ["red", "blue"]}, "3": {"hand": ["yellow"], "paintings": ["green"]}},
             "game": {"auctioneer": 1, "count_red": 3, "count_blue": 2, "count_green": 0, "count_yellow": 0}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"value_red": 30, "value_blue": 20, "value_green": 0, "seasons_scored": 1, "buyer": 0},
              "players": {"1": {"money": 100}, "2": {"money": 150}, "3": {"money": 100}},
              "not_offered": [{"seat": 2, "option": 0}, {"seat": 3, "option": 0}]}},

  {"name": "Reserve is announced when the season does not end", "rule": "R6", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"]}, "2": {"hand": ["green"]}, "3": {"hand": ["yellow"]}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 25}],
   "expect": {"game": {"reserve": 25, "current_artist": "blue"}}},

  {"name": "When the season continues, talk happens and the auction goes on to bidding", "rule": "R7", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"]}, "2": {"hand": ["green"]}, "3": {"hand": ["yellow"]}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}],
   "expect": {"game": {"buyer": 2, "price": 10}, "offered": [{"seat": 2, "option": 10}, {"seat": 3, "option": 0}]}},

  {"name": "Non-auctioneers bid from 0 to their own money", "rule": "R8", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"]}, "2": {"hand": ["green"], "money": 40}, "3": {"hand": ["yellow"], "money": 100}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 0}],
   "expect": {"offered": [{"seat": 2, "option": 40}, {"seat": 3, "option": 100}],
              "not_offered": [{"seat": 2, "option": 41}, {"seat": 3, "option": 101}]}},

  {"name": "Highest bid at or above reserve pays the auctioneer and takes the painting", "rule": "R9", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"], "paintings": []}, "2": {"hand": ["green"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 25},
             {"seat": 2, "options_include": 30}, {"seat": 3, "options_include": 20}],
   "expect": {"game": {"buyer": 2, "price": 30},
              "players": {"1": {"money": 130, "paintings": []}, "2": {"money": 70, "paintings": ["blue"]}, "3": {"money": 100, "paintings": []}}}},

  {"name": "Tied top bids go to the first seat after the auctioneer", "rule": "R10", "players": 4, "rounds": 1,
   "given": {"players": {"1": {"hand": ["red"], "paintings": []}, "2": {"hand": ["blue", "red"], "paintings": []}, "3": {"hand": ["green"], "paintings": []}, "4": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 2}},
   "rules": [{"seat": 2, "options_include": "blue"}, {"seat": 2, "options_include": 0},
             {"seat": 1, "options_include": 20}, {"seat": 4, "options_include": 20}, {"seat": 3, "options_include": 10}],
   "expect": {"game": {"buyer": 4, "price": 20},
              "players": {"1": {"money": 100}, "2": {"money": 120}, "3": {"money": 100}, "4": {"money": 80, "paintings": ["blue"]}}}},

  {"name": "No bid reaches the reserve: auctioneer pays the reserve to the bank and keeps the painting", "rule": "R11", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"], "paintings": []}, "2": {"hand": ["green"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 50},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"buyer": 1, "price": 50},
              "players": {"1": {"money": 50, "paintings": ["blue"]}, "2": {"money": 100, "paintings": []}, "3": {"money": 100}}}},

  {"name": "Buyer and price are made public after the auction", "rule": "R12", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"]}, "2": {"hand": ["green"]}, "3": {"hand": ["yellow"]}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": 12}, {"seat": 3, "options_include": 15}],
   "expect": {"game": {"buyer": 3, "price": 15}, "players": {"1": {"money": 115}, "3": {"money": 85}}}},

  {"name": "Season ranking: first gains 30, count tie for second goes to the earlier artist", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["green", "red"], "paintings": []}, "2": {"hand": ["blue"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 1, "count_red": 0, "count_blue": 2, "count_green": 3, "count_yellow": 2,
                      "value_red": 0, "value_blue": 10, "value_green": 20, "value_yellow": 5}},
   "rules": [{"seat": 1, "options_include": "green"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"value_green": 50, "value_blue": 30, "value_yellow": 5, "value_red": 0}}},

  {"name": "Second artist with count 0 gains nothing", "rule": "R13", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["red", "green"], "paintings": []}, "2": {"hand": ["blue"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 1, "count_red": 3, "count_blue": 0, "count_green": 0, "count_yellow": 0,
                      "value_red": 0, "value_blue": 10, "value_green": 0, "value_yellow": 0}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"value_red": 30, "value_blue": 10, "value_green": 0, "value_yellow": 0}}},

  {"name": "Paintings of ranked artists pay their cumulative value, unranked pay 0", "rule": "R14", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["green", "red"], "paintings": []}, "2": {"hand": ["blue"], "paintings": ["green", "green", "yellow"]}, "3": {"hand": ["yellow"], "paintings": ["blue", "red"]}},
             "game": {"auctioneer": 1, "count_red": 0, "count_blue": 2, "count_green": 3, "count_yellow": 2,
                      "value_red": 0, "value_blue": 10, "value_green": 20, "value_yellow": 5}},
   "rules": [{"seat": 1, "options_include": "green"}, {"seat": 1, "options_include": 0}],
   "expect": {"players": {"1": {"money": 100}, "2": {"money": 200}, "3": {"money": 130}}}},

  {"name": "After scoring, paintings are discarded, counts reset and the season advances", "rule": "R15", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["yellow", "red"], "paintings": ["red"]}, "2": {"hand": ["blue"], "paintings": ["yellow"]}, "3": {"hand": ["green"], "paintings": []}},
             "game": {"auctioneer": 1, "count_yellow": 3, "count_red": 1, "count_blue": 2, "count_green": 0, "season": 1, "seasons_scored": 0}},
   "rules": [{"seat": 1, "options_include": "yellow"}, {"seat": 1, "options_include": 0}],
   "expect": {"game": {"count_red": 0, "count_blue": 0, "count_green": 0, "count_yellow": 0, "season": 2, "seasons_scored": 1},
              "players": {"1": {"paintings": []}, "2": {"paintings": []}, "3": {"paintings": []}}}},

  {"name": "When all hands are empty after an auction the season is scored and the game ends", "rule": "R16", "players": 3,
   "given": {"players": {"1": {"hand": ["red"], "paintings": []}, "2": {"hand": [], "paintings": []}, "3": {"hand": [], "paintings": []}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 5}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 2, "standings": {"1": 105, "2": 125, "3": 100},
              "game": {"value_red": 30, "seasons_scored": 1}}},

  {"name": "The third season scoring ends the game", "rule": "R17", "players": 3,
   "given": {"players": {"1": {"hand": ["red", "blue"], "paintings": []}, "2": {"hand": ["green"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": ["red"]}},
             "game": {"auctioneer": 1, "season": 3, "seasons_scored": 2, "count_red": 3, "count_blue": 0, "count_green": 0, "count_yellow": 0,
                      "value_red": 0, "value_blue": 0, "value_green": 0, "value_yellow": 0}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 100, "2": 100, "3": 130}, "game": {"seasons_scored": 3}}},

  {"name": "The game ends after round 32", "rule": "R18", "players": 3,
   "given": {"players": {"1": {"hand": ["blue", "red"], "paintings": []}, "2": {"hand": ["green"], "paintings": []}, "3": {"hand": ["yellow"], "paintings": []}},
             "game": {"auctioneer": 1, "round_number": 31}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 1, "standings": {"1": 110, "2": 90, "3": 100}}},

  {"name": "Auctioneer passes over an empty-handed seat, which still bids", "rule": "R19", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["red", "blue"]}, "2": {"hand": []}, "3": {"hand": ["green"]}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auctioneer": 3, "buyer": 2, "price": 10}, "offered": [{"seat": 2, "option": 10}]}},

  {"name": "Players tied for most money share the win", "rule": "R20", "players": 3,
   "given": {"players": {"1": {"hand": ["red"], "money": 100, "paintings": []}, "2": {"hand": [], "money": 70, "paintings": []}, "3": {"hand": [], "money": 80, "paintings": []}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": [1, 2], "standings": {"1": 100, "2": 100, "3": 80}}},

  {"name": "Bids and reserves are capped at current money, so money never goes below 0", "rule": "R21", "players": 3, "rounds": 1,
   "given": {"players": {"1": {"hand": ["blue", "red"], "money": 20}, "2": {"hand": ["green"], "money": 15}, "3": {"hand": ["yellow"], "money": 100}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "blue"}, {"seat": 1, "options_include": 10},
             {"seat": 2, "options_include": 15}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"buyer": 2, "price": 15},
              "players": {"1": {"money": 35}, "2": {"money": 0}},
              "not_offered": [{"seat": 2, "option": 16}, {"seat": 1, "option": 21}]}}
]
````
