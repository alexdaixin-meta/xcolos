# 32 scenarios

- time: 2026-10-27T18:51:51+00:00 (137.2s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 ecb66d7bcb40e55e, reply sha256 ee4f37a141e6769b

## Sent

````
SPEC:
{
  "name": "Modern Art: Four Seasons",
  "summary": "Four dealers auction paintings by four artists over four seasons with sealed bids. Each season the artists are ranked and pay out on paintings held. The richest player who bought at least 3 paintings wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 24,
    "cards_per_artist": 6,
    "hand_size": 5,
    "set_aside_cards": 4,
    "starting_money": 100,
    "seasons": 4,
    "auctions_per_season": 4,
    "total_auctions": 16,
    "value_first": 30,
    "value_second": 20,
    "value_third": 10,
    "value_fourth": 0,
    "auctioneer_share_divisor": 2,
    "min_paintings_to_be_eligible": 3,
    "min_bid": 0
  },
  "attributes": {
    "player": [
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Hidden hand of artist cards (Red, Blue, Green, Yellow), 5 dealt at setup",
        "observable": false
      },
      {
        "key": "money",
        "type": "number",
        "visible": "ally",
        "initial": 100,
        "meaning": "The player's money, seen only by its owner until it is revealed at game end; this is the score",
        "observable": true
      },
      {
        "key": "paintings_bought",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Paintings bought during the whole game; at least 3 are needed to be eligible to win",
        "observable": true
      },
      {
        "key": "collection",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "Artists of the paintings owned this season (buyers are announced publicly); emptied at season end",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This auction's sealed bid; losing bids are never revealed",
        "observable": false
      },
      {
        "key": "nomination",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "The artist this player names at season end; all nominations are revealed after the poll",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This auction's non-binding talk message",
        "observable": false
      },
      {
        "key": "payout_last",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "The player's payout from the last season end, told privately",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          "Red",
          "Red",
          "Red",
          "Red",
          "Red",
          "Red",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Blue",
          "Green",
          "Green",
          "Green",
          "Green",
          "Green",
          "Green",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow",
          "Yellow"
        ],
        "meaning": "The 24-card deck",
        "observable": false
      },
      {
        "key": "set_aside",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "The 4 cards set aside unseen after the deal",
        "observable": false
      },
      {
        "key": "season",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Current season, 1 to 4",
        "observable": false
      },
      {
        "key": "auction_in_season",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "k, the auction's number within the season, 1 to 4",
        "observable": false
      },
      {
        "key": "auctions_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Auctions completed so far, 0 to 16",
        "observable": false
      },
      {
        "key": "auctioneer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of this auction's auctioneer",
        "observable": false
      },
      {
        "key": "current_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Artist of the painting being auctioned",
        "observable": false
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Highest bid this auction (the price); told privately to the buyer and the auctioneer only",
        "observable": false
      },
      {
        "key": "buyer",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat of this auction's buyer, 0 if unsold",
        "observable": false
      },
      {
        "key": "count_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red's season count",
        "observable": false
      },
      {
        "key": "count_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue's season count",
        "observable": false
      },
      {
        "key": "count_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green's season count",
        "observable": false
      },
      {
        "key": "count_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Yellow's season count",
        "observable": false
      },
      {
        "key": "value_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red's cumulative value",
        "observable": true
      },
      {
        "key": "value_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue's cumulative value",
        "observable": true
      },
      {
        "key": "value_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green's cumulative value",
        "observable": true
      },
      {
        "key": "value_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Yellow's cumulative value",
        "observable": true
      },
      {
        "key": "place_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red's place this season: 1-3 = placed in the top three, 0 = did not place",
        "observable": false
      },
      {
        "key": "place_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue's place this season, as above",
        "observable": false
      },
      {
        "key": "place_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green's place this season, as above",
        "observable": false
      },
      {
        "key": "place_yellow",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Yellow's place this season, as above",
        "observable": false
      }
    ]
  },
  "setup": [
    "Four players sit in seats 1 to 4.",
    "The deck list holds 24 cards: 6 each of Red, Blue, Green and Yellow.",
    "Each player draws 5 cards at random from the deck into their hand. Each draw removes the card from the deck.",
    "The remaining 4 cards are moved from the deck to set_aside, unseen.",
    "Each player's money is set to 100 and their paintings_bought to 0.",
    "Every artist's cumulative value and season count are set to 0. Season is 1, auction_in_season is 1 and auctions_done is 0.",
    "Sync: each player is sent their own hand and money."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auctioneer = ((season + auction_in_season - 2) mod 4) + 1; every player's bid = 0 and message = ''; buyer = 0; high_bid = 0"
    },
    {
      "action": "ask",
      "who": "the seat equal to auctioneer",
      "answer": "one card from the auctioneer's hand",
      "effect": "Remove the chosen card from the auctioneer's hand and set current_card to its artist. Tell all players: 'Seat {auctioneer} auctions a {current_card} painting.'"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The season count of current_card's artist (count_red, count_blue, count_green or count_yellow) rises by 1, whether or not the painting sells"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a short text message",
      "effect": "Set each player's message, then broadcast to all: 'Seat {seat} says: {value}'. Messages are not binding."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to your current money",
      "effect": "Set each player's bid; no bid is shown to anyone"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "high_bid = the highest bid. If high_bid = 0: buyer = 0 and the card is discarded. Otherwise buyer = the seat with the highest bid*4 + (3 - ((seat - auctioneer - 1) mod 4)), which breaks ties in the order auctioneer+1, auctioneer+2, auctioneer+3, then the auctioneer. Buyer's money -= high_bid. If buyer != auctioneer, auctioneer's money += floor(high_bid / 2), and the rest goes to the bank. current_card is appended to the buyer's collection, and the buyer's paintings_bought += 1."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Public: 'Seat {buyer} bought the {current_card} painting', or 'The {current_card} painting went unsold' when buyer = 0. Private to the buyer and to the auctioneer only: 'The price was {high_bid}.' Losing bids are never revealed."
    },
    {
      "action": "poll",
      "who": "all players",
      "when": "auction_in_season == 4",
      "answer": "one of Red, Blue, Green, Yellow",
      "effect": "Set each player's nomination. Each nomination adds 1 to that artist's season count. All nominations are then revealed to everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "when": "auction_in_season == 4",
      "answer": null,
      "effect": "Each artist gets a key = count*10000 + value*10 + priority, where priority (3 highest) follows the season order: S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G. An artist's place = 1 + the number of artists with a higher key. An artist with count 0, or with place 4, gets place 0. Then value += 30 if place 1, 20 if place 2, 10 if place 3."
    },
    {
      "action": "update",
      "who": "all players",
      "when": "auction_in_season == 4",
      "answer": null,
      "effect": "For each player: payout_last = the sum, over the paintings in their collection, of that artist's value (after this season's increase) if the artist's place is 1 to 3, else 0. The player's money += payout_last. Tell each player privately: 'Your payout this season is {payout_last}.' Tell all players the four cumulative values."
    },
    {
      "action": "update",
      "who": "all players",
      "when": "auction_in_season == 4",
      "answer": null,
      "effect": "Every player's collection = []; count_red, count_blue, count_green and count_yellow = 0; every place = 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auctions_done += 1. If auction_in_season == 4, then season += 1 and auction_in_season = 1; otherwise auction_in_season += 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If auctions_done == 16, the game ends and every player's final money is revealed to all; otherwise continue with the next auction"
    }
  ],
  "ending": {
    "condition": "auctions_done == 16",
    "rank_by": "(you.paintings_bought >= 3) * (you.money + 1)",
    "min_to_win": 1,
    "decided_by": "Only players who bought at least 3 paintings are eligible. Among them the most money wins, and eligible players tied for most money share the result. If nobody is eligible, nobody wins."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, each of the 4 players is dealt 5 hidden cards from a 24-card deck of 6 Red, 6 Blue, 6 Green and 6 Yellow, and the remaining 4 cards are set aside unseen."
    },
    {
      "id": "R2",
      "text": "At setup, each player has 100 money, and every artist has cumulative value 0 and season count 0."
    },
    {
      "id": "R3",
      "text": "In auction k of season s, the auctioneer is seat ((s + k - 2) mod 4) + 1, giving Season 1: 1,2,3,4; Season 2: 2,3,4,1; Season 3: 3,4,1,2; Season 4: 4,1,2,3."
    },
    {
      "id": "R4",
      "text": "When the auctioneer chooses a card, it is removed from their hand and its artist is announced to all."
    },
    {
      "id": "R5",
      "text": "When a card is auctioned, its artist's season count rises by 1, whether or not it sells."
    },
    {
      "id": "R6",
      "text": "Every auction, all players send one talk message at the same time, and the messages are then shown to everyone."
    },
    {
      "id": "R7",
      "text": "Every player, including the auctioneer, bids a whole number from 0 to their current money, sealed and at the same time."
    },
    {
      "id": "R8",
      "text": "When the highest bid is 0, the painting is unsold and discarded, and no money changes hands."
    },
    {
      "id": "R9",
      "text": "When bids tie for highest, the buyer is the first tied seat in the order auctioneer+1, auctioneer+2, auctioneer+3 (wrapping round), then the auctioneer; for example, with auctioneer 2 and seats 1 and 4 tied at 30, seat 4 buys."
    },
    {
      "id": "R10",
      "text": "When a non-auctioneer buys for bid b, the buyer pays b and the auctioneer receives floor(b/2); for example, a bid of 25 gives the auctioneer 12."
    },
    {
      "id": "R11",
      "text": "When the auctioneer buys their own painting for b, they pay b to the bank and receive nothing."
    },
    {
      "id": "R12",
      "text": "When a painting sells, it is added to the buyer's collection and the buyer's paintings_bought rises by 1."
    },
    {
      "id": "R13",
      "text": "After each auction, the artist and the buyer (or 'unsold') are announced to all, the price is told only to the buyer and the auctioneer, and losing bids are never revealed."
    },
    {
      "id": "R14",
      "text": "After the 4th auction of a season, every player secretly nominates one artist, each nomination adds 1 to that artist's season count, and all nominations are then revealed."
    },
    {
      "id": "R15",
      "text": "Artists are ranked by season count, higher first; ties are broken by higher cumulative value, then by the season priority (S1 R>B>G>Y, S2 B>G>Y>R, S3 G>Y>R>B, S4 Y>R>B>G), and an artist with season count 0 cannot place."
    },
    {
      "id": "R16",
      "text": "At season end, the 1st artist gains 30 cumulative value, the 2nd gains 20, the 3rd gains 10, and the 4th gains nothing."
    },
    {
      "id": "R17",
      "text": "At season end, each owned painting of a top-three artist pays its owner that artist's cumulative value after the increase, and a painting of an artist that did not place pays 0."
    },
    {
      "id": "R18",
      "text": "Each player's payout is told only to them, while the artists' cumulative values are public."
    },
    {
      "id": "R19",
      "text": "After the payout, all collections are emptied and all season counts reset to 0."
    },
    {
      "id": "R20",
      "text": "The game ends after the 16th auction and the Season 4 payout, and all final money is then revealed."
    },
    {
      "id": "R21",
      "text": "Only a player with paintings_bought >= 3 can win; among those, the most money wins; eligible players tied for most money share the result; and with no eligible player nobody wins."
    }
  ],
  "offers": [
    {
      "question": "Choose a card to auction",
      "who": "the seat equal to auctioneer",
      "options": "each distinct artist currently in that seat's hand; other seats are not asked"
    },
    {
      "question": "Talk message",
      "who": "all seats",
      "options": "any short text"
    },
    {
      "question": "Sealed bid",
      "who": "all seats, including the auctioneer",
      "options": "a whole number from 0 to that seat's current money"
    },
    {
      "question": "Season-end nomination (after auction 4 of each season)",
      "who": "all seats",
      "options": "Red, Blue, Green, Yellow"
    }
  ],
  "choices": [
    {
      "what": "4 players (min 4, max 4, suggested 4)",
      "why": "The designer fixed the table at 4. The auctioneer rotation, the tie-break order and the card counts (4 auctions per player plus 1 unused card each, with 4 cards set aside) all depend on exactly 4 seats."
    },
    {
      "what": "Talk kept as a simultaneous poll each auction, broadcast to all",
      "why": "The rules specify it. Players have opposing interests (an auctioneer wants high bids, a bidder wants a cheap buy, and nominations push artists up or down), so non-binding talk gives them something to bluff and reason about."
    },
    {
      "what": "Ranking and the bid tie-break are computed as numeric keys",
      "why": "This puts the stated tie-break orders into plain arithmetic without changing them."
    },
    {
      "what": "The ranking expression adds 1 to money and requires a value of at least 1",
      "why": "An eligible player with 0 money still beats every ineligible player, and if nobody is eligible nobody wins."
    },
    {
      "what": "Strategy at the table",
      "why": "Players balance spending against later payouts, use nominations to steer which artists place, read whose talk is a bluff, and make sure they buy 3 paintings to stay eligible."
    }
  ],
  "simplifications": [
    {
      "what": "The source's 'draw' among eligible players tied for most money becomes a shared win",
      "why": "The engine has no separate draw; players level at the top share the win, which is the equivalent outcome. 'No eligible player' becomes no winner through min_to_win."
    },
    {
      "what": "Each auction is one round; the season-end steps carry a when-condition (auction_in_season == 4)",
      "why": "The step list is flat, so each season-end step is a single conditional step rather than a separate block."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, paintings_bought; table: value_red, value_blue, value_green, value_yellow.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Control every seat's season-end nomination explicitly, including the auctioneer and any seat left to the default. The default answer may be the first option, which is 'Red', so it silently adds 1 to Red's count. For the 'count 0 cannot place' test, make sure no auctioned card and no nomination is Red, so Red's season count really is 0, then assert that its value stays unchanged. For the payout and public-value test, likewise make sure no seat nominates an artist you expect not to place. Work out each artist's season count (auctioned cards plus all four nominations) before predicting the value changes. Assert on public values and money, not on internal fields.
````

## Reply

````
```json
[
  {
    "name": "Setup deals 5 cards to each seat, leaves the deck empty and sets 4 cards aside",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"deck": 0, "set_aside": 4},
        "players": {"1": {"hand": 5}, "2": {"hand": 5}, "3": {"hand": 5}, "4": {"hand": 5}}
      }
    }
  },
  {
    "name": "Setup gives 100 money, 0 paintings and all artist values at 0",
    "rule": "R2",
    "players": 4,
    "seed": 2,
    "rounds": 0,
    "expect": {
      "players": {
        "1": {"money": 100, "paintings_bought": 0},
        "2": {"money": 100, "paintings_bought": 0},
        "3": {"money": 100, "paintings_bought": 0},
        "4": {"money": 100, "paintings_bought": 0}
      },
      "game": {"value_red": 0, "value_blue": 0, "value_green": 0, "value_yellow": 0}
    }
  },
  {
    "name": "Season 2 auction 1: seat 2 is auctioneer and receives half of seat 3's bid of 20",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red"]}, "2": {"hand": ["Blue"]}},
      "game": {"season": 2, "auction_in_season": 1, "auctions_done": 4}
    },
    "rules": [
      {"seat": 3, "options_include": 20},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 100},
        "2": {"money": 110},
        "3": {"money": 80, "paintings_bought": 1},
        "4": {"money": 100}
      },
      "offered": [{"seat": 2, "option": "Blue"}],
      "not_offered": [{"seat": 1, "option": "Red"}]
    }
  },
  {
    "name": "Season 4 auction 2: seat 1 is auctioneer and receives half of seat 2's bid of 40",
    "rule": "R3",
    "players": 4,
    "seed": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Green"]}, "4": {"hand": ["Red"]}},
      "game": {"season": 4, "auction_in_season": 2, "auctions_done": 13}
    },
    "rules": [
      {"seat": 2, "options_include": 40},
      {"seat": 1, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 120},
        "2": {"money": 60, "paintings_bought": 1},
        "3": {"money": 100},
        "4": {"money": 100}
      },
      "offered": [{"seat": 1, "option": "Green"}],
      "not_offered": [{"seat": 4, "option": "Red"}]
    }
  },
  {
    "name": "The auctioneer chooses among its distinct artists and the chosen card leaves its hand",
    "rule": "R4",
    "players": 4,
    "seed": 5,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red", "Green", "Green"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Green"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "lens": {"players": {"1": {"hand": 2}}},
      "offered": [{"seat": 1, "option": "Red"}, {"seat": 1, "option": "Green"}],
      "players": {"1": {"money": 100}}
    }
  },
  {
    "name": "An unsold Yellow painting still counts for Yellow, so Yellow places 2nd behind Blue's 4 nominations",
    "rule": "R5",
    "players": 4,
    "seed": 6,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Yellow"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Blue"}
    ],
    "expect": {
      "game": {"value_blue": 30, "value_yellow": 20, "value_red": 0, "value_green": 0},
      "players": {
        "1": {"money": 100},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "After the talk poll every seat is still asked for a sealed bid, and an all-zero auction changes no money",
    "rule": "R6",
    "players": 4,
    "seed": 7,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "offered": [
        {"seat": 1, "option": 0},
        {"seat": 2, "option": 0},
        {"seat": 3, "option": 0},
        {"seat": 4, "option": 0}
      ],
      "players": {
        "1": {"money": 100},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "A bid ranges from 0 to the seat's money and the auctioneer may bid all of its 40",
    "rule": "R7",
    "players": 4,
    "seed": 8,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red"], "money": 40}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "offered": [{"seat": 1, "option": 40}, {"seat": 2, "option": 100}],
      "not_offered": [{"seat": 1, "option": 41}, {"seat": 2, "option": 101}],
      "players": {
        "1": {"money": 0, "paintings_bought": 1},
        "2": {"money": 100}
      }
    }
  },
  {
    "name": "When the highest bid is 0 the painting is unsold and no money or paintings change",
    "rule": "R8",
    "players": 4,
    "seed": 9,
    "rounds": 1,
    "given": {
      "players": {"2": {"hand": ["Blue"]}},
      "game": {"season": 1, "auction_in_season": 2, "auctions_done": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 100, "paintings_bought": 0},
        "2": {"money": 100, "paintings_bought": 0},
        "3": {"money": 100, "paintings_bought": 0},
        "4": {"money": 100, "paintings_bought": 0}
      }
    }
  },
  {
    "name": "Auctioneer 2 with seats 1 and 4 tied at 30: seat 4 buys",
    "rule": "R9",
    "players": 4,
    "seed": 10,
    "rounds": 1,
    "given": {
      "players": {"2": {"hand": ["Red"]}},
      "game": {"season": 1, "auction_in_season": 2, "auctions_done": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 30},
      {"seat": 4, "options_include": 30},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 100, "paintings_bought": 0},
        "2": {"money": 115},
        "3": {"money": 100},
        "4": {"money": 70, "paintings_bought": 1}
      }
    }
  },
  {
    "name": "Auctioneer 1 tied with seat 3 at 20: seat 3 buys, because the auctioneer comes last",
    "rule": "R9",
    "players": 4,
    "seed": 11,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 20},
      {"seat": 3, "options_include": 20},
      {"seat": 2, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 110, "paintings_bought": 0},
        "2": {"money": 100},
        "3": {"money": 80, "paintings_bought": 1},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "Seat 3 buys for 25: it pays 25 and auctioneer 1 receives 12",
    "rule": "R10",
    "players": 4,
    "seed": 12,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Green"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 3, "options_include": 25},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 112},
        "2": {"money": 100},
        "3": {"money": 75, "paintings_bought": 1},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "The auctioneer buys its own painting for 25: it pays 25 and receives nothing",
    "rule": "R11",
    "players": 4,
    "seed": 13,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Green"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 1, "options_include": 25},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 75, "paintings_bought": 1},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "A sale raises the buyer's paintings_bought from 2 to 3",
    "rule": "R12",
    "players": 4,
    "seed": 14,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Yellow"]}, "2": {"paintings_bought": 2}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 2, "options_include": 10},
      {"seat": 1, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 105, "paintings_bought": 0},
        "2": {"money": 90, "paintings_bought": 3}
      }
    }
  },
  {
    "name": "Only the winning bid is charged; seat 3's losing bid of 20 costs nothing",
    "rule": "R13",
    "players": 4,
    "seed": 15,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Blue"]}},
      "game": {"season": 1, "auction_in_season": 1, "auctions_done": 0}
    },
    "rules": [
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 20},
      {"seat": 1, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 115},
        "2": {"money": 70, "paintings_bought": 1},
        "3": {"money": 100, "paintings_bought": 0},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "Four Yellow nominations outrank one auctioned Green: Yellow gains 30 and Green 20",
    "rule": "R14",
    "players": 4,
    "seed": 16,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Green"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Yellow"},
      {"seat": 4, "options_include": "Yellow"}
    ],
    "expect": {
      "game": {"value_yellow": 30, "value_green": 20, "value_red": 0, "value_blue": 0},
      "offered": [{"seat": 1, "option": "Red"}, {"seat": 4, "option": "Blue"}]
    }
  },
  {
    "name": "Equal season counts are broken by higher cumulative value (Green 20 > Yellow 10 > Blue 0)",
    "rule": "R15",
    "players": 4,
    "seed": 17,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Red"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3, "value_green": 20, "value_yellow": 10}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Green"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Yellow"},
      {"seat": 4, "options_include": "Red"}
    ],
    "expect": {
      "game": {"value_red": 30, "value_green": 40, "value_yellow": 20, "value_blue": 0}
    }
  },
  {
    "name": "Season 2 priority B>G>Y>R breaks equal counts and values: Blue 2nd, Green 3rd, Red 4th",
    "rule": "R15",
    "players": 4,
    "seed": 18,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Red"]}},
      "game": {"season": 2, "auction_in_season": 4, "auctions_done": 7}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Green"},
      {"seat": 3, "options_include": "Yellow"},
      {"seat": 4, "options_include": "Yellow"}
    ],
    "expect": {
      "game": {"value_yellow": 30, "value_blue": 20, "value_green": 10, "value_red": 0}
    }
  },
  {
    "name": "Artists with season count 0 do not place: high-value Red and Green stay unchanged and only Blue gains",
    "rule": "R15",
    "players": 4,
    "seed": 19,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Blue"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3, "value_red": 50, "value_green": 40}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Blue"},
      {"seat": 2, "options_include": "Blue"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Blue"}
    ],
    "expect": {
      "game": {"value_red": 50, "value_green": 40, "value_blue": 30, "value_yellow": 0}
    }
  },
  {
    "name": "Season-end gains are 30, 20, 10 and 0 for 1st to 4th (Red, Blue, Green, Yellow)",
    "rule": "R16",
    "players": 4,
    "seed": 20,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Yellow"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Green"}
    ],
    "expect": {
      "game": {"value_red": 30, "value_blue": 20, "value_green": 10, "value_yellow": 0}
    }
  },
  {
    "name": "Paintings pay their artist's value after the increase; a 4th-placed Yellow pays 0",
    "rule": "R17",
    "players": 4,
    "seed": 21,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"collection": ["Red", "Blue"]},
        "2": {"collection": ["Yellow"]},
        "4": {"hand": ["Red"]}
      },
      "game": {
        "season": 1,
        "auction_in_season": 4,
        "auctions_done": 3,
        "value_red": 10,
        "count_red": 1,
        "count_blue": 1,
        "count_yellow": 1
      }
    },
    "rules": [
      {"seat": 1, "options_include": 10},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Blue"},
      {"seat": 4, "options_include": "Green"}
    ],
    "expect": {
      "game": {"value_red": 40, "value_blue": 20, "value_green": 10, "value_yellow": 0},
      "players": {
        "1": {"money": 190, "paintings_bought": 1},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 105}
      }
    }
  },
  {
    "name": "A held Green painting pays the public Green value of 30 when Green places 1st",
    "rule": "R18",
    "players": 4,
    "seed": 22,
    "rounds": 1,
    "given": {
      "players": {"3": {"collection": ["Green"]}, "4": {"hand": ["Green"]}},
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3, "count_green": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Green"},
      {"seat": 2, "options_include": "Green"},
      {"seat": 3, "options_include": "Green"},
      {"seat": 4, "options_include": "Green"}
    ],
    "expect": {
      "game": {"value_green": 30, "value_red": 0, "value_blue": 0, "value_yellow": 0},
      "players": {
        "1": {"money": 100},
        "2": {"money": 100},
        "3": {"money": 130},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "Collections and season counts are cleared after the payout: seat 1's old Red pays nothing in season 2",
    "rule": "R19",
    "players": 4,
    "seed": 23,
    "rounds": 5,
    "given": {
      "players": {
        "1": {"collection": ["Red"], "hand": ["Green"]},
        "2": {"hand": ["Green"]},
        "3": {"hand": ["Green"]},
        "4": {"hand": ["Blue", "Blue"]}
      },
      "game": {"season": 1, "auction_in_season": 4, "auctions_done": 3, "count_red": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 0, "times": "all"},
      {"seat": 2, "options_include": 0, "times": "all"},
      {"seat": 3, "options_include": 0, "times": "all"},
      {"seat": 4, "options_include": 0, "times": "all"},
      {"seat": 1, "options_include": "Red", "times": 2},
      {"seat": 2, "options_include": "Red"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Red"},
      {"seat": 3, "options_include": "Yellow"},
      {"seat": 4, "options_include": "Red"},
      {"seat": 4, "options_include": "Yellow"}
    ],
    "expect": {
      "game": {"value_red": 40, "value_blue": 20, "value_green": 30, "value_yellow": 20},
      "players": {
        "1": {"money": 130},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "The game ends after the 16th auction and Season 4 payout; seat 3 is richest but ineligible, so seat 2 wins",
    "rule": "R20",
    "players": 4,
    "seed": 24,
    "given": {
      "players": {
        "1": {"money": 120, "paintings_bought": 3},
        "2": {"money": 150, "paintings_bought": 3, "collection": ["Yellow"]},
        "3": {"money": 200, "paintings_bought": 2, "hand": ["Red"]},
        "4": {"money": 90, "paintings_bought": 3}
      },
      "game": {"season": 4, "auction_in_season": 4, "auctions_done": 15, "count_yellow": 1}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Yellow"},
      {"seat": 2, "options_include": "Yellow"},
      {"seat": 3, "options_include": "Yellow"},
      {"seat": 4, "options_include": "Yellow"}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 121, "2": 181, "3": 0, "4": 91},
      "game": {"value_yellow": 30, "value_red": 20, "value_blue": 0, "value_green": 0},
      "players": {
        "1": {"money": 120},
        "2": {"money": 180},
        "3": {"money": 200},
        "4": {"money": 90}
      }
    }
  },
  {
    "name": "Eligible seats 1 and 2 tied at 150 share the win over ineligible seat 3 with 300",
    "rule": "R21",
    "players": 4,
    "seed": 25,
    "given": {
      "players": {
        "1": {"money": 150, "paintings_bought": 3},
        "2": {"money": 150, "paintings_bought": 3},
        "3": {"money": 300, "paintings_bought": 2, "hand": ["Red"]},
        "4": {"money": 100, "paintings_bought": 3}
      },
      "game": {"season": 4, "auction_in_season": 4, "auctions_done": 15}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Red"},
      {"seat": 4, "options_include": "Red"}
    ],
    "expect": {
      "winner": [1, 2],
      "standings": {"1": 151, "2": 151, "3": 0, "4": 101}
    }
  },
  {
    "name": "With no seat holding 3 paintings, nobody wins",
    "rule": "R21",
    "players": 4,
    "seed": 26,
    "given": {
      "players": {
        "1": {"money": 150, "paintings_bought": 2},
        "2": {"money": 120, "paintings_bought": 2},
        "3": {"money": 300, "paintings_bought": 2, "hand": ["Red"]},
        "4": {"money": 100, "paintings_bought": 1}
      },
      "game": {"season": 4, "auction_in_season": 4, "auctions_done": 15}
    },
    "rules": [
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Red"},
      {"seat": 4, "options_include": "Red"}
    ],
    "expect": {
      "winner": null,
      "standings": {"1": 0, "2": 0, "3": 0, "4": 0}
    }
  },
  {
    "name": "Seat 3 buys its own painting in the last auction, reaches 3 paintings, and wins with 320",
    "rule": "R21",
    "players": 4,
    "seed": 27,
    "given": {
      "players": {
        "1": {"money": 150, "paintings_bought": 3},
        "2": {"money": 120, "paintings_bought": 3},
        "3": {"money": 300, "paintings_bought": 2, "hand": ["Red"]},
        "4": {"money": 100, "paintings_bought": 3}
      },
      "game": {"season": 4, "auction_in_season": 4, "auctions_done": 15}
    },
    "rules": [
      {"seat": 3, "options_include": 10},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 4, "options_include": 0},
      {"seat": 1, "options_include": "Red"},
      {"seat": 2, "options_include": "Red"},
      {"seat": 3, "options_include": "Red"},
      {"seat": 4, "options_include": "Red"}
    ],
    "expect": {
      "winner": 3,
      "standings": {"1": 151, "2": 121, "3": 321, "4": 101},
      "players": {"3": {"money": 320, "paintings_bought": 3}},
      "game": {"value_red": 30}
    }
  }
]
```
````
