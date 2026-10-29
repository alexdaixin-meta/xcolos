# 05 scenarios

- time: 2026-10-27T18:18:00+00:00 (79.4s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 d2aa85600953b062, reply sha256 4e14dfae670ac387

## Sent

````
SPEC:
{
  "name": "Modern Art: Sealed Gallery",
  "summary": "Four art dealers take turns putting paintings by three artists up for sealed-bid auction. Each season ends when an artist's fourth painting appears, and the season's top two artists pay their owners. After three seasons the most money wins.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "player_count": 4,
    "deck_size": 36,
    "amber_cards": 14,
    "blue_cards": 12,
    "crimson_cards": 10,
    "hand_size": 9,
    "starting_money": 100,
    "season_end_count": 4,
    "first_artist_gain": 30,
    "second_artist_gain": 20,
    "third_artist_gain": 0,
    "seasons": 3,
    "max_turns": 30,
    "min_bid": 0,
    "rarity_amber": 1,
    "rarity_blue": 2,
    "rarity_crimson": 3
  },
  "attributes": {
    "player": [
      {
        "key": "money",
        "type": "number",
        "visible": "ally",
        "initial": 100,
        "meaning": "The player's money. It is known only to the owner, but every payment is announced.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Hidden hand of painting cards, each one 'Amber', 'Blue' or 'Crimson'. Dealt 9 at setup.",
        "observable": false
      },
      {
        "key": "owned_amber",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Amber paintings bought this season.",
        "observable": true
      },
      {
        "key": "owned_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue paintings bought this season.",
        "observable": true
      },
      {
        "key": "owned_crimson",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Crimson paintings bought this season.",
        "observable": true
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This turn's talk message.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This turn's sealed bid. All bids are announced after the auction.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": "14 x 'Amber', 12 x 'Blue', 10 x 'Crimson'",
        "meaning": "The shuffled painting deck. It is empty after the deal.",
        "observable": false
      },
      {
        "key": "auctioneer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the current auctioneer.",
        "observable": true
      },
      {
        "key": "current_card",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The artist of the painting revealed this turn.",
        "observable": false
      },
      {
        "key": "played_amber",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Amber cards played this season.",
        "observable": true
      },
      {
        "key": "played_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue cards played this season.",
        "observable": true
      },
      {
        "key": "played_crimson",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Crimson cards played this season.",
        "observable": true
      },
      {
        "key": "value_amber",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Amber's cumulative value.",
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
        "key": "value_crimson",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Crimson's cumulative value.",
        "observable": true
      },
      {
        "key": "season_ending",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when this turn's card was the 4th of its artist this season.",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The seat that won this turn's auction.",
        "observable": false
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The winning bid this turn.",
        "observable": false
      },
      {
        "key": "first_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The top-ranked artist at season end.",
        "observable": false
      },
      {
        "key": "second_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "The second-ranked artist at season end.",
        "observable": false
      },
      {
        "key": "season",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of seasons completed.",
        "observable": true
      }
    ]
  },
  "setup": [
    "Fill the deck with 14 'Amber', 12 'Blue' and 10 'Crimson' cards (36 in total).",
    "Deal 9 cards to each of the 4 players. Each deal is a random draw from the deck, appended to that player's hand and removed from the deck.",
    "Set each player's money to 100, all owned and played counts to 0, all artist values to 0, and season to 0.",
    "Set auctioneer to seat 1."
  ],
  "round": [
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the season (season + 1) and that seat {auctioneer} is the auctioneer."
    },
    {
      "action": "ask",
      "who": "the seat equal to auctioneer",
      "answer": "one artist name that appears in their hand: Amber, Blue or Crimson",
      "effect": "Set current_card to the answer and reveal it to all."
    },
    {
      "action": "update",
      "who": "the auctioneer",
      "answer": null,
      "effect": "Remove one copy of current_card from the auctioneer's hand. Add 1 to played_<current_card>. Set season_ending = (played_<current_card> == 4). Announce the card and its new count."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "When season_ending: announce that the 4th {current_card} ends the season, that the card is not auctioned, and that no one owns it."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a short text message",
      "effect": "When not season_ending: store each answer in message, then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. Talk binds no one."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to the player's money",
      "effect": "When not season_ending: store each answer in bid. No one sees a bid until all are in."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When not season_ending: work out key = bid * 10 + (4 - ((seat - auctioneer + 4) mod 4)) for each player. Set winner_seat to the seat with the highest key, and price to that seat's bid. This breaks ties toward the auctioneer, then clockwise, and gives the card to the auctioneer free if every bid is 0."
    },
    {
      "action": "update",
      "who": "winner_seat and auctioneer",
      "answer": null,
      "effect": "When not season_ending: winner_seat's money -= price. If winner_seat != auctioneer, the auctioneer's money += price; otherwise the price goes to the bank. winner_seat's owned_<current_card> += 1. Announce all bids, the buyer and the price."
    },
    {
      "action": "update",
      "who": "the table",
      "answer": null,
      "effect": "When season_ending: give each artist the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3). first_artist = the highest key and second_artist = the middle key. value_<first_artist> += 30 and value_<second_artist> += 20. Announce the ranking and the values."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "When season_ending: each player's money += owned_<first_artist> * value_<first_artist> + owned_<second_artist> * value_<second_artist>, paid by the bank. Announce each payout."
    },
    {
      "action": "update",
      "who": "all players and the table",
      "answer": null,
      "effect": "When season_ending: set every owned_amber, owned_blue and owned_crimson to 0 and every played_amber, played_blue and played_crimson to 0. season += 1. Set season_ending to false. Hands are untouched."
    },
    {
      "action": "update",
      "who": "the table",
      "answer": null,
      "effect": "auctioneer = (auctioneer mod 4) + 1."
    },
    {
      "action": "check",
      "who": "the table",
      "answer": null,
      "effect": "If season == 3, end the game; otherwise continue."
    }
  ],
  "ending": {
    "condition": "season == 3",
    "rank_by": "you.money",
    "decided_by": "After season 3, the player with the most money wins. Players tied for the most money share the result, which is a draw among them."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game is set up, the deck holds 14 Amber, 12 Blue and 10 Crimson cards, each player is dealt 9 hidden cards, each player has 100 money, and every artist value is 0."
    },
    {
      "id": "R2",
      "text": "When a turn begins, the seat equal to auctioneer chooses one card from its own hand, and that card is removed from the hand and revealed."
    },
    {
      "id": "R3",
      "text": "When a card of an artist is revealed, that artist's played-this-season count rises by 1."
    },
    {
      "id": "R4",
      "text": "When a revealed card makes its artist's count 4, the card is not auctioned, no player's owned count changes, and the season ends."
    },
    {
      "id": "R5",
      "text": "When a card is auctioned, every player first sends one talk message at the same time, and all messages are then shown to everyone."
    },
    {
      "id": "R6",
      "text": "When a card is auctioned, all 4 players, the auctioneer included, bid at the same time a whole number from 0 up to their current money."
    },
    {
      "id": "R7",
      "text": "When bids are in, the highest bid wins the card."
    },
    {
      "id": "R8",
      "text": "When bids tie for highest, the auctioneer wins if tied, otherwise the tied seat first clockwise from the auctioneer wins."
    },
    {
      "id": "R9",
      "text": "When every bid is 0, the auctioneer gets the card for 0."
    },
    {
      "id": "R10",
      "text": "When a non-auctioneer wins with a bid of X, the winner's money falls by X and the auctioneer's money rises by X."
    },
    {
      "id": "R11",
      "text": "When the auctioneer wins with a bid of X, the auctioneer's money falls by X and no player receives it."
    },
    {
      "id": "R12",
      "text": "When a player wins an auction, that player's owned count for the card's artist rises by 1, and all bids, the buyer and the price are announced."
    },
    {
      "id": "R13",
      "text": "When a season ends, artists rank by played-this-season count, and ties go to the rarer artist: Crimson beats Blue, and Blue beats Amber."
    },
    {
      "id": "R14",
      "text": "When a season ends, the first artist's value rises by 30, the second's by 20, and the third's by 0."
    },
    {
      "id": "R15",
      "text": "When a season ends, each player receives from the bank owned(first) * value(first) + owned(second) * value(second), and the third artist pays nothing even if its value is above 0."
    },
    {
      "id": "R16",
      "text": "When season payouts are done, all owned counts and played counts reset to 0, hands keep their unplayed cards, and season rises by 1."
    },
    {
      "id": "R17",
      "text": "When a turn ends, whether or not a season ended, the auctioneer passes to the next seat (4 passes to 1)."
    },
    {
      "id": "R18",
      "text": "When season reaches 3, the game ends, and the player with the most money wins, with tied leaders drawing."
    }
  ],
  "offers": [
    {
      "question": "Choose a card to reveal",
      "who": "the auctioneer only",
      "options": "each distinct artist name (Amber, Blue, Crimson) that appears at least once in the auctioneer's hand; no other seat is asked"
    },
    {
      "question": "Talk message",
      "who": "all 4 seats, only when the card is being auctioned",
      "options": "any short text"
    },
    {
      "question": "Sealed bid",
      "who": "all 4 seats, only when the card is being auctioned",
      "options": "a whole number from 0 to that seat's current money"
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players, suggested 4",
      "why": "The designer fixed 4, and the deck deals exactly 9 cards to each of 4 players. Fewer players would leave no rivals to bid against; more would not fit the deal."
    },
    {
      "what": "Talk kept as a simultaneous poll before each bid",
      "why": "The source requires it. It also earns its place: players disagree about prices, and they can use it to talk up artists or bluff about their holdings."
    },
    {
      "what": "Bid tie-break encoded as the key bid * 10 + (4 - clockwise distance from the auctioneer)",
      "why": "This gives the source's tie order, auctioneer first and then clockwise, in plain arithmetic, and it also covers the all-zero case."
    },
    {
      "what": "Artist ranking encoded as the key played * 10 + rarity (Amber 1, Blue 2, Crimson 3)",
      "why": "This gives the source's tie rule, rarer artist wins, in plain arithmetic."
    },
    {
      "what": "Cards are stored as artist names",
      "why": "Paintings of the same artist are indistinguishable in these rules."
    },
    {
      "what": "The 'auctioneer has no cards' skip is not built as a step",
      "why": "The source says it cannot happen: at most 30 cards are played and each hand holds 9."
    },
    {
      "what": "Money is marked observable",
      "why": "It is the score, and every payment is announced, even though money is formally known only to its owner."
    }
  ],
  "simplifications": [
    {
      "what": "The season-end block is written as individual steps each guarded by 'when season_ending', and the auction steps are guarded by 'when not season_ending'",
      "why": "The step list is flat, but per-step conditions express the same flow exactly."
    },
    {
      "what": "A tie for most money is a shared win among the tied leaders",
      "why": "The engine has no separate draw. The rules call this a draw, and sharing the top is how that is reported."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, owned_amber, owned_blue, owned_crimson; table: auctioneer, played_amber, played_blue, played_crimson, value_amber, value_blue, value_crimson, season.
````

## Reply

````
```json
[
  {
    "name": "Setup: deck fully dealt, 9 cards each, 100 money, values 0",
    "rule": "R1",
    "players": 4,
    "rounds": 0,
    "expect": {
      "lens": {
        "game": {"deck": 0},
        "players": {"1": {"hand": 9}, "2": {"hand": 9}, "3": {"hand": 9}, "4": {"hand": 9}}
      },
      "players": {
        "1": {"money": 100, "owned_amber": 0, "owned_blue": 0, "owned_crimson": 0},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      },
      "game": {"value_amber": 0, "value_blue": 0, "value_crimson": 0, "season": 0, "auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    }
  },
  {
    "name": "Auctioneer picks Blue from own hand and it leaves the hand",
    "rule": "R2",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue", "Crimson"]}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "lens": {"players": {"1": {"hand": 2}}},
      "game": {"played_blue": 1, "played_amber": 0, "played_crimson": 0},
      "offered": [{"seat": 1, "option": "Blue"}],
      "not_offered": [{"seat": 2, "option": "Blue"}, {"seat": 3, "option": "Amber"}]
    }
  },
  {
    "name": "Revealing a Crimson raises played_crimson from 2 to 3",
    "rule": "R3",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Crimson"]}},
      "game": {"auctioneer": 1, "played_amber": 1, "played_blue": 0, "played_crimson": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "Crimson"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "game": {"played_crimson": 3, "played_amber": 1, "played_blue": 0}
    }
  },
  {
    "name": "4th Amber is not auctioned, no bids, season ends",
    "rule": "R4",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue"]}},
      "game": {"auctioneer": 1, "played_amber": 3, "played_blue": 0, "played_crimson": 0, "season": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"}
    ],
    "expect": {
      "players": {
        "1": {"money": 100, "owned_amber": 0},
        "2": {"money": 100, "owned_amber": 0},
        "3": {"money": 100},
        "4": {"money": 100}
      },
      "game": {"season": 1, "played_amber": 0, "value_amber": 30, "value_crimson": 20, "value_blue": 0, "auctioneer": 2},
      "not_offered": [
        {"seat": 1, "option": 0},
        {"seat": 2, "option": 0},
        {"seat": 3, "option": 0},
        {"seat": 4, "option": 0}
      ]
    }
  },
  {
    "name": "Auctioned card: all seats talk then bid; all-zero gives it to auctioneer",
    "rule": "R5",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Crimson", "Blue"]}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Crimson"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"owned_crimson": 1, "money": 100}},
      "game": {"played_crimson": 1},
      "offered": [
        {"seat": 1, "option": 0},
        {"seat": 2, "option": 0},
        {"seat": 3, "option": 0},
        {"seat": 4, "option": 0}
      ]
    }
  },
  {
    "name": "Bid range is 0 to current money: seat with 50 may bid 50 but not 51",
    "rule": "R6",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue"]}, "2": {"money": 50}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 50},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {"1": {"money": 150}, "2": {"money": 0, "owned_amber": 1}},
      "offered": [{"seat": 2, "option": 50}, {"seat": 1, "option": 100}],
      "not_offered": [{"seat": 2, "option": 51}]
    }
  },
  {
    "name": "Highest bid (seat 2, 30) wins the card",
    "rule": "R7",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue"]}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 1, "options_include": 10},
      {"seat": 2, "options_include": 30},
      {"seat": 3, "options_include": 20},
      {"seat": 4, "options_include": 5}
    ],
    "expect": {
      "players": {
        "1": {"money": 130, "owned_blue": 0},
        "2": {"money": 70, "owned_blue": 1},
        "3": {"money": 100, "owned_blue": 0},
        "4": {"money": 100, "owned_blue": 0}
      }
    }
  },
  {
    "name": "Tie among non-auctioneers goes to first clockwise from auctioneer 2 (seat 3)",
    "rule": "R8",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"2": {"hand": ["Amber", "Blue"]}},
      "game": {"auctioneer": 2, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 2, "options_include": "Amber"},
      {"seat": 1, "options_include": 20},
      {"seat": 2, "options_include": 10},
      {"seat": 3, "options_include": 20},
      {"seat": 4, "options_include": 20}
    ],
    "expect": {
      "players": {
        "1": {"money": 100, "owned_amber": 0},
        "2": {"money": 120, "owned_amber": 0},
        "3": {"money": 80, "owned_amber": 1},
        "4": {"money": 100, "owned_amber": 0}
      }
    }
  },
  {
    "name": "Tie involving the auctioneer goes to the auctioneer",
    "rule": "R8",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue"]}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"},
      {"seat": 1, "options_include": 15},
      {"seat": 2, "options_include": 15},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 85, "owned_amber": 1},
        "2": {"money": 100, "owned_amber": 0},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "All bids 0: auctioneer 3 gets the Crimson for free",
    "rule": "R9",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"3": {"hand": ["Crimson", "Amber"]}},
      "game": {"auctioneer": 3, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 3, "options_include": "Crimson"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 100, "owned_crimson": 0},
        "2": {"money": 100, "owned_crimson": 0},
        "3": {"money": 100, "owned_crimson": 1},
        "4": {"money": 100, "owned_crimson": 0}
      }
    }
  },
  {
    "name": "Non-auctioneer seat 1 wins at 40: pays 40 to auctioneer 4",
    "rule": "R10",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Blue", "Amber"]}},
      "game": {"auctioneer": 4, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 4, "options_include": "Blue"},
      {"seat": 1, "options_include": 40},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 60, "owned_blue": 1},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 140, "owned_blue": 0}
      }
    }
  },
  {
    "name": "Auctioneer wins at 25: pays the bank, nobody receives it",
    "rule": "R11",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Blue", "Amber"]}},
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"},
      {"seat": 1, "options_include": 25},
      {"seat": 2, "options_include": 10},
      {"seat": 3, "options_include": 10},
      {"seat": 4, "options_include": 10}
    ],
    "expect": {
      "players": {
        "1": {"money": 75, "owned_blue": 1},
        "2": {"money": 100},
        "3": {"money": 100},
        "4": {"money": 100}
      }
    }
  },
  {
    "name": "Winner's owned count for the artist rises from 1 to 2",
    "rule": "R12",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Amber", "Blue"]}, "3": {"owned_amber": 1}},
      "game": {"auctioneer": 1, "played_amber": 1, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 12},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "players": {
        "1": {"money": 112, "owned_amber": 0},
        "3": {"money": 88, "owned_amber": 2},
        "2": {"owned_amber": 0},
        "4": {"owned_amber": 0}
      },
      "game": {"played_amber": 2}
    }
  },
  {
    "name": "Season-end tie for second (Blue 2, Crimson 2) goes to rarer Crimson",
    "rule": "R13",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Amber", "Blue"]},
        "2": {"owned_crimson": 2},
        "3": {"owned_blue": 3},
        "4": {"owned_amber": 1}
      },
      "game": {"auctioneer": 1, "played_amber": 3, "played_blue": 2, "played_crimson": 2, "value_blue": 10, "season": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"}
    ],
    "expect": {
      "players": {
        "1": {"money": 100},
        "2": {"money": 140},
        "3": {"money": 100},
        "4": {"money": 130}
      },
      "game": {"value_amber": 30, "value_crimson": 20, "value_blue": 10, "season": 1}
    }
  },
  {
    "name": "Season end adds 30 to first (Blue), 20 to second (Amber), 0 to third",
    "rule": "R14",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand": ["Blue", "Amber"]}},
      "game": {"auctioneer": 1, "played_amber": 2, "played_blue": 3, "played_crimson": 1, "value_amber": 20, "value_blue": 30, "value_crimson": 0, "season": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"}
    ],
    "expect": {
      "game": {"value_blue": 60, "value_amber": 40, "value_crimson": 0, "season": 1}
    }
  },
  {
    "name": "Payouts: first and second artists pay owners, third (valued Crimson) pays nothing",
    "rule": "R15",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Amber", "Blue"], "owned_amber": 2},
        "2": {"owned_blue": 1},
        "3": {"owned_crimson": 3}
      },
      "game": {"auctioneer": 1, "played_amber": 3, "played_blue": 2, "played_crimson": 1, "value_amber": 0, "value_blue": 0, "value_crimson": 50, "season": 0}
    },
    "rules": [
      {"seat": 1, "options_include": "Amber"}
    ],
    "expect": {
      "players": {
        "1": {"money": 160},
        "2": {"money": 120},
        "3": {"money": 100},
        "4": {"money": 100}
      },
      "game": {"value_amber": 30, "value_blue": 20, "value_crimson": 50}
    }
  },
  {
    "name": "After payouts owned and played counts reset, hands keep cards, season 1 -> 2",
    "rule": "R16",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {
        "1": {"hand": ["Amber", "Blue", "Crimson"], "owned_blue": 1},
        "2": {"hand": ["Amber", "Amber", "Blue", "Crimson", "Crimson"], "owned_amber": 2},
        "4": {"owned_crimson": 1}
      },
      "game": {"auctioneer": 1, "played_amber": 2, "played_blue": 3, "played_crimson": 1, "season": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "Blue"}
    ],
    "expect": {
      "lens": {"players": {"1": {"hand": 2}, "2": {"hand": 5}}},
      "players": {
        "1": {"owned_amber": 0, "owned_blue": 0, "owned_crimson": 0},
        "2": {"owned_amber": 0, "owned_blue": 0, "owned_crimson": 0},
        "3": {"owned_amber": 0, "owned_blue": 0, "owned_crimson": 0},
        "4": {"owned_amber": 0, "owned_blue": 0, "owned_crimson": 0}
      },
      "game": {"played_amber": 0, "played_blue": 0, "played_crimson": 0, "season": 2}
    }
  },
  {
    "name": "Auctioneer passes from seat 4 to seat 1 after an auction turn",
    "rule": "R17",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"4": {"hand": ["Amber", "Blue"]}},
      "game": {"auctioneer": 4, "played_amber": 0, "played_blue": 0, "played_crimson": 0}
    },
    "rules": [
      {"seat": 4, "options_include": "Amber"},
      {"seat": 1, "options_include": 0},
      {"seat": 2, "options_include": 0},
      {"seat": 3, "options_include": 0},
      {"seat": 4, "options_include": 0}
    ],
    "expect": {
      "game": {"auctioneer": 1}
    }
  },
  {
    "name": "Auctioneer passes from seat 3 to seat 4 after a season-ending turn",
    "rule": "R17",
    "players": 4,
    "rounds": 1,
    "given": {
      "players": {"3": {"hand": ["Crimson", "Amber"]}},
      "game": {"auctioneer": 3, "played_amber": 0, "played_blue": 0, "played_crimson": 3, "season": 0}
    },
    "rules": [
      {"seat": 3, "options_include": "Crimson"}
    ],
    "expect": {
      "game": {"auctioneer": 4, "season": 1}
    }
  },
  {
    "name": "Third season ends: most money (seat 3) wins",
    "rule": "R18",
    "players": 4,
    "given": {
      "players": {
        "1": {"hand": ["Crimson", "Amber"], "money": 100},
        "2": {"money": 120},
        "3": {"money": 90, "owned_crimson": 2},
        "4": {"money": 110, "owned_blue": 1}
      },
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 3, "value_amber": 0, "value_blue": 0, "value_crimson": 0, "season": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "Crimson"}
    ],
    "expect": {
      "winner": 3,
      "standings": {"1": 100, "2": 120, "3": 150, "4": 130},
      "game": {"season": 3}
    }
  },
  {
    "name": "Third season ends with seats 2 and 3 tied for most money: shared win",
    "rule": "R18",
    "players": 4,
    "given": {
      "players": {
        "1": {"hand": ["Crimson", "Amber"], "money": 100},
        "2": {"money": 150},
        "3": {"money": 90, "owned_crimson": 2},
        "4": {"money": 110, "owned_blue": 1}
      },
      "game": {"auctioneer": 1, "played_amber": 0, "played_blue": 0, "played_crimson": 3, "value_amber": 0, "value_blue": 0, "value_crimson": 0, "season": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "Crimson"}
    ],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 100, "2": 150, "3": 150, "4": 130}
    }
  }
]
```
````
