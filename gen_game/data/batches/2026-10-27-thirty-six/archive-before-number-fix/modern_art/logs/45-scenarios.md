# 45 scenarios

- time: 2026-10-27T17:39:58+00:00 (96.8s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 e33c18b6ecd869ab, reply sha256 4859c88808e2c44b

## Sent

````
SPEC:
{
  "name": "Modern Art: Sealed Gallery",
  "summary": "Three players take turns as auctioneer of 18 paintings by three artists. Everyone bids at once in sealed bids, artists gain value at each season's end, owned paintings pay out, and the richest player after round 18 wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "start_money": 60,
    "artist_count": 3,
    "die_sides": 6,
    "composition_major": 4,
    "composition_middle": 2,
    "composition_minor": 1,
    "cards_per_hand": 7,
    "auctions_per_seat": 6,
    "season_end_count": 3,
    "first_place_value": 6,
    "second_place_value": 3,
    "tie_value": 3,
    "min_season_count_to_score": 1,
    "total_rounds": 18,
    "first_auctioneer": 1,
    "min_bid": 0
  },
  "attributes": {
    "player": [
      {
        "key": "money",
        "type": "number",
        "visible": "public",
        "initial": 60,
        "meaning": "Coins held. Every bid, price and payout is announced.",
        "observable": true
      },
      {
        "key": "hand_red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Red cards in this player's private hand.",
        "observable": false
      },
      {
        "key": "hand_blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Blue cards in this player's private hand.",
        "observable": false
      },
      {
        "key": "hand_green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Green cards in this player's private hand.",
        "observable": false
      },
      {
        "key": "owned_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red paintings bought this season.",
        "observable": false
      },
      {
        "key": "owned_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue paintings bought this season.",
        "observable": false
      },
      {
        "key": "owned_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green paintings bought this season.",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "This round's sealed bid, revealed once all bids are in.",
        "observable": true
      },
      {
        "key": "last_payout",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Money received at the most recent season scoring.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Round counter, from 1 to 18.",
        "observable": true
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
        "key": "season_over",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Set to 1 when the season ends this round.",
        "observable": false
      },
      {
        "key": "deal_roll",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Hidden die roll (1 to 6) that decides which seat gets which composition.",
        "observable": false
      },
      {
        "key": "season_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red cards played this season.",
        "observable": true
      },
      {
        "key": "season_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue cards played this season.",
        "observable": true
      },
      {
        "key": "season_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green cards played this season.",
        "observable": true
      },
      {
        "key": "value_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Red.",
        "observable": true
      },
      {
        "key": "value_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Blue.",
        "observable": true
      },
      {
        "key": "value_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Green.",
        "observable": true
      },
      {
        "key": "current_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Artist played this round (red, blue or green).",
        "observable": false
      },
      {
        "key": "high_bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Highest bid this round.",
        "observable": false
      },
      {
        "key": "winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won this round's painting.",
        "observable": false
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Price paid this round.",
        "observable": false
      },
      {
        "key": "scored_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if Red scored at this season's end, else 0.",
        "observable": false
      },
      {
        "key": "scored_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if Blue scored at this season's end, else 0.",
        "observable": false
      },
      {
        "key": "scored_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "1 if Green scored at this season's end, else 0.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each get money 60, and owned_red, owned_blue and owned_green 0.",
    "season_red, season_blue and season_green are set to 0, and value_red, value_blue and value_green to 0.",
    "auctioneer is set to 1, round to 0 and season_over to 0.",
    "deal_roll is set to a random whole number from 1 to 6 (seeded).",
    "Composition A is Red 4, Blue 2, Green 1. Composition B is Red 1, Blue 4, Green 2. Composition C is Red 2, Blue 1, Green 4.",
    "The compositions go to seats 1, 2 and 3 by roll: roll 1 gives A,B,C; roll 2 gives A,C,B; roll 3 gives B,A,C; roll 4 gives B,C,A; roll 5 gives C,A,B; roll 6 gives C,B,A. This sets each seat's hand_red, hand_blue and hand_green.",
    "Each player is shown only their own hand and is told that the other two seats hold the other two compositions."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; season_over = 0."
    },
    {
      "action": "ask",
      "who": "the seat equal to auctioneer",
      "answer": "one artist from red, blue, green, offering only those whose hand count for this seat is above 0",
      "effect": "The chosen artist is X."
    },
    {
      "action": "update",
      "who": "the seat equal to auctioneer",
      "answer": null,
      "effect": "That seat's hand_X -= 1; season_X += 1; current_artist = X. Announce current_artist to all."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If season_X == 3, then season_over = 1 and announce that the card is discarded unsold and the season ends. Otherwise season_over stays 0."
    },
    {
      "action": "poll",
      "who": "all players, when season_over == 0",
      "answer": "short free text",
      "effect": "Set each player's message, then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."
    },
    {
      "action": "poll",
      "who": "all players, when season_over == 0",
      "answer": "a whole number from 0 to your own money",
      "effect": "Set each player's bid. Once all bids are in, announce all three bids."
    },
    {
      "action": "update",
      "who": "all players, when season_over == 0",
      "answer": null,
      "effect": "high_bid = max of the bids. If high_bid == 0: winner = auctioneer and price = 0. Otherwise price = high_bid and winner = the first seat with bid == high_bid in this order: auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer."
    },
    {
      "action": "update",
      "who": "all players, when season_over == 0",
      "answer": null,
      "effect": "If winner != auctioneer: the winner's money -= price and the auctioneer's money += price. If winner == auctioneer: the auctioneer's money -= price (paid to the bank). The winner's owned_X += 1. Announce winner and price."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If round == 18, then season_over = 1."
    },
    {
      "action": "update",
      "who": "all players, when season_over == 1",
      "answer": null,
      "effect": "Set scored_red, scored_blue and scored_green to 0. Let top = the largest season count. If top >= 1 and exactly one artist has season == top, that artist gets value += 6 and scored = 1; then let s = the larger season count of the other two, and if s >= 1 and exactly one of them has season == s, that artist gets value += 3 and scored = 1. If top >= 1 and two or three artists have season == top, each of them gets value += 3 and scored = 1, and no other artist scores."
    },
    {
      "action": "update",
      "who": "all players, when season_over == 1",
      "answer": null,
      "effect": "For each player: last_payout = owned_red*value_red*scored_red + owned_blue*value_blue*scored_blue + owned_green*value_green*scored_green; money += last_payout."
    },
    {
      "action": "update",
      "who": "all players, when season_over == 1",
      "answer": null,
      "effect": "Every player's owned_red, owned_blue and owned_green = 0; season_red, season_blue and season_green = 0. Values are kept."
    },
    {
      "action": "tell",
      "who": "all players, when season_over == 1",
      "answer": null,
      "effect": "Announce the scoring artists, value_red, value_blue, value_green, and each player's last_payout and money."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auctioneer = auctioneer % 3 + 1."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round == 18, end the game. Otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "round == 18",
    "rank_by": "you.money",
    "decided_by": "After round 18, including the last season's scoring and payout, the player with the most money wins. Players tied for the most money share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player has money 60 and owned_red, owned_blue and owned_green 0; every season count and every value is 0; auctioneer is 1; round is 0."
    },
    {
      "id": "R2",
      "text": "When deal_roll is 1, then seats 1, 2 and 3 get compositions A, B and C, where A is Red 4/Blue 2/Green 1, B is Red 1/Blue 4/Green 2, and C is Red 2/Blue 1/Green 4."
    },
    {
      "id": "R3",
      "text": "When deal_roll is 2, 3, 4, 5 or 6, then seats 1, 2 and 3 get A,C,B or B,A,C or B,C,A or C,A,B or C,B,A respectively."
    },
    {
      "id": "R4",
      "text": "When hands are dealt, then each player sees only their own hand_red, hand_blue and hand_green."
    },
    {
      "id": "R5",
      "text": "When a round starts, then round rises by 1 and season_over is set to 0."
    },
    {
      "id": "R6",
      "text": "When the auctioneer chooses an artist, then only artists with the auctioneer's hand count above 0 are offered."
    },
    {
      "id": "R7",
      "text": "When artist X is played, then the auctioneer's hand_X falls by 1, season_X rises by 1, and current_artist is announced as X."
    },
    {
      "id": "R8",
      "text": "When season_X reaches 3 after a play, then season_over is 1, the card is discarded unsold, and no talk, bid or sale happens that round."
    },
    {
      "id": "R9",
      "text": "When season_over is 0, then all three players write one message at the same time, and all are shown labelled by seat."
    },
    {
      "id": "R10",
      "text": "When season_over is 0, then all three players, including the auctioneer, bid simultaneously a whole number from 0 to their own money, and all bids are announced."
    },
    {
      "id": "R11",
      "text": "When the highest bid is positive, then the highest bidder wins at a price equal to that bid."
    },
    {
      "id": "R12",
      "text": "When all bids are 0, then the auctioneer takes the painting at price 0."
    },
    {
      "id": "R13",
      "text": "When a positive top bid is tied, then the winner is the tied seat that comes first in the order: seat after the auctioneer, the next seat, then the auctioneer (for example, with auctioneer 1 the order is 2, 3, 1)."
    },
    {
      "id": "R14",
      "text": "When the winner is not the auctioneer, then the winner pays the price to the auctioneer; for example, a price of 10 moves 10 from the winner's money to the auctioneer's."
    },
    {
      "id": "R15",
      "text": "When the winner is the auctioneer, then the auctioneer's money falls by the price, paid to the bank."
    },
    {
      "id": "R16",
      "text": "When a painting of X is sold, then the winner's owned_X rises by 1 and the winner and price are announced."
    },
    {
      "id": "R17",
      "text": "When round is 18, then season_over is set to 1 after the sale."
    },
    {
      "id": "R18",
      "text": "When a season ends and one artist has the strictly highest season count (at least 1), then its value rises by 6."
    },
    {
      "id": "R19",
      "text": "When a single artist was top, and one of the other two has a season count strictly higher than the third and at least 1, then that artist's value rises by 3; otherwise no second artist scores."
    },
    {
      "id": "R20",
      "text": "When two or three artists tie for the highest season count (at least 1), then each of them gains 3 value and no other artist scores."
    },
    {
      "id": "R21",
      "text": "When a season ends, then for each artist that scored, every player's money rises by their owned count of it times its new cumulative value; artists that did not score pay nothing but keep their value."
    },
    {
      "id": "R22",
      "text": "When a season's payout is done, then every owned count and every season count is reset to 0, and values are kept."
    },
    {
      "id": "R23",
      "text": "When a season ends, then the scoring artists, new values, each player's payout and each player's money are announced."
    },
    {
      "id": "R24",
      "text": "When a round ends, then the auctioneer passes 1 to 2, 2 to 3, and 3 to 1."
    },
    {
      "id": "R25",
      "text": "When round 18 has ended, then the game ends and the player with the most money wins; players tied for the most money share the result (a draw)."
    }
  ],
  "offers": [
    {
      "question": "Which artist do you play?",
      "who": "the auctioneer only",
      "options": "each of red, blue and green for which the auctioneer's own hand count is above 0; other seats are not asked"
    },
    {
      "question": "Your message to the table",
      "who": "all three seats, only when season_over == 0",
      "options": "short free text"
    },
    {
      "question": "Your sealed bid",
      "who": "all three seats including the auctioneer, only when season_over == 0",
      "options": "a whole number from 0 to that seat's current money"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed 3. The deal uses three compositions, one per seat, and 18 rounds give each seat exactly 6 auctions. With fewer seats there are no rivals to hide compositions from, and more seats would break the deal."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules say the messages are written at the same time without seeing the others. Players disagree about which artist to boost, so talk gives them something to bluff and bargain over."
    },
    {
      "what": "Tie order written as auctioneer%3+1, then (auctioneer+1)%3+1, then auctioneer",
      "why": "This is the source's seat order expressed as arithmetic."
    },
    {
      "what": "Owned counts and season counts are public",
      "why": "Every played artist, winner and price is announced, so these are already known to all."
    },
    {
      "what": "Season scoring is done by arithmetic, with no referee",
      "why": "The comparisons of the three season counts are all arithmetic."
    },
    {
      "what": "The round-18 auction still runs before the forced season end",
      "why": "The source's R11 sets season_over only after the sale steps."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most money is reported as a shared win",
      "why": "The engine has no separate draw; players level at the top share the win, which is the source's draw."
    },
    {
      "what": "The die roll is a seeded random number from 1 to 6",
      "why": "The engine's randomness is seeded so a match replays exactly."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, bid; table: round, auctioneer, season_red, season_blue, season_green, value_red, value_blue, value_green.
````

## Reply

````
```json
[
  {
    "name": "Setup: everyone has 60 money, all counts and values are 0, auctioneer 1, round 0",
    "rule": "R1",
    "players": 3,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 60}, "3": {"money": 60}},
      "game": {"round": 0, "auctioneer": 1, "season_red": 0, "season_blue": 0, "season_green": 0, "value_red": 0, "value_blue": 0, "value_green": 0}
    }
  },
  {
    "name": "Deal (chance-proof): every composition holds each artist, so auctioneer 1 is offered red, blue and green in round 1",
    "rule": "R2",
    "players": 3,
    "seed": 1,
    "rounds": 1,
    "default": "decline",
    "expect": {
      "offered": [{"seat": 1, "option": "red"}, {"seat": 1, "option": "blue"}, {"seat": 1, "option": "green"}],
      "game": {"round": 1}
    }
  },
  {
    "name": "Deal with another seed (chance-proof): auctioneer 1 still holds every artist",
    "rule": "R3",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "expect": {
      "offered": [{"seat": 1, "option": "red"}, {"seat": 1, "option": "blue"}, {"seat": 1, "option": "green"}],
      "game": {"round": 1}
    }
  },
  {
    "name": "Artist choices follow the auctioneer's own hand, not another seat's hand",
    "rule": "R4",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 0, "hand_blue": 2, "hand_green": 1}, "2": {"hand_red": 4, "hand_blue": 1, "hand_green": 2}},
      "game": {"auctioneer": 1}
    },
    "rules": [{"seat": 1, "options_include": "blue"}],
    "expect": {
      "offered": [{"seat": 1, "option": "blue"}, {"seat": 1, "option": "green"}],
      "not_offered": [{"seat": 1, "option": "red"}],
      "game": {"season_blue": 1}
    }
  },
  {
    "name": "A new round raises the round counter by 1",
    "rule": "R5",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"round": 4, "auctioneer": 1}
    },
    "rules": [{"seat": 1, "options_include": "red"}],
    "expect": {"game": {"round": 5}}
  },
  {
    "name": "Only artists in the auctioneer's hand are offered, and only to the auctioneer",
    "rule": "R6",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 0, "hand_blue": 0, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "expect": {
      "offered": [{"seat": 1, "option": "green"}],
      "not_offered": [{"seat": 1, "option": "red"}, {"seat": 1, "option": "blue"}, {"seat": 2, "option": "red"}, {"seat": 3, "option": "red"}],
      "game": {"season_green": 1}
    }
  },
  {
    "name": "Playing blue raises season_blue by 1; with all bids 0 nobody's money changes",
    "rule": "R7",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 4, "hand_blue": 2, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [{"seat": 1, "options_include": "blue"}],
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 60}, "3": {"money": 60}},
      "game": {"season_red": 0, "season_blue": 1, "season_green": 0, "auctioneer": 2}
    }
  },
  {
    "name": "The third red card is discarded unsold: no sale, red scores 6, season counts reset",
    "rule": "R8",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1, "season_red": 2}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 2, "options_include": 10, "times": "all"}
    ],
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 60}, "3": {"money": 60}},
      "game": {"season_red": 0, "value_red": 6, "value_blue": 0, "value_green": 0}
    }
  },
  {
    "name": "With the season open, talk happens and the round goes on to a sale (seat 2 buys at 5)",
    "rule": "R9",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "players": {"1": {"money": 65}, "2": {"money": 55, "bid": 5}, "3": {"money": 60}},
      "game": {"season_red": 1}
    }
  },
  {
    "name": "All three bid including the auctioneer, bids are capped at own money and announced",
    "rule": "R10",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}, "2": {"money": 5}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 1, "options_include": 8},
      {"seat": 2, "options_include": 5},
      {"seat": 3, "options_include": 3}
    ],
    "expect": {
      "players": {"1": {"bid": 8, "money": 52}, "2": {"bid": 5, "money": 5}, "3": {"bid": 3, "money": 60}},
      "not_offered": [{"seat": 2, "option": 6}]
    }
  },
  {
    "name": "Highest bid 12 by seat 2 wins at price 12, paid to auctioneer 1",
    "rule": "R11",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 2, "options_include": 12},
      {"seat": 3, "options_include": 7}
    ],
    "expect": {
      "players": {"1": {"money": 72}, "2": {"money": 48, "bid": 12}, "3": {"money": 60, "bid": 7}}
    }
  },
  {
    "name": "All bids 0 in round 18: auctioneer 3 takes the red at 0 and is paid 6 when red scores",
    "rule": "R12",
    "players": 3,
    "given": {
      "players": {"3": {"hand_red": 1, "hand_blue": 0, "hand_green": 0}},
      "game": {"round": 17, "auctioneer": 3, "season_red": 1, "season_blue": 0, "season_green": 0, "value_red": 0}
    },
    "rules": [{"seat": 3, "options_include": "red"}],
    "expect": {
      "winner": 3,
      "standings": {"1": 60, "2": 60, "3": 66},
      "players": {"1": {"money": 60}, "2": {"money": 60}, "3": {"money": 66}},
      "game": {"round": 18, "value_red": 6}
    }
  },
  {
    "name": "Tie at 10 between seats 2 and 3 with auctioneer 1: seat 2 wins",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 2, "options_include": 10},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {"players": {"1": {"money": 70}, "2": {"money": 50}, "3": {"money": 60}}}
  },
  {
    "name": "Tie at 10 between seats 1 and 3 with auctioneer 2: order is 3,1,2 so seat 3 wins",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"2": {"hand_red": 1, "hand_blue": 4, "hand_green": 2}},
      "game": {"auctioneer": 2}
    },
    "rules": [
      {"seat": 2, "options_include": "blue"},
      {"seat": 1, "options_include": 10},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {"players": {"1": {"money": 60}, "2": {"money": 70}, "3": {"money": 50}}}
  },
  {
    "name": "Tie at 10 between auctioneer 1 and seat 3: the auctioneer comes last, so seat 3 wins",
    "rule": "R13",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 1, "options_include": 10},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {"players": {"1": {"money": 70}, "2": {"money": 60}, "3": {"money": 50}}}
  },
  {
    "name": "Seat 3 wins at 10: 10 moves from seat 3 to auctioneer 1",
    "rule": "R14",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "green"},
      {"seat": 3, "options_include": 10}
    ],
    "expect": {"players": {"1": {"money": 70}, "2": {"money": 60}, "3": {"money": 50}}}
  },
  {
    "name": "Auctioneer wins its own painting at 8 and pays the bank",
    "rule": "R15",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 2, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1}
    },
    "rules": [
      {"seat": 1, "options_include": "red"},
      {"seat": 1, "options_include": 8}
    ],
    "expect": {"players": {"1": {"money": 52}, "2": {"money": 60}, "3": {"money": 60}}}
  },
  {
    "name": "Seat 2 buys the red in round 18 at 5; its ownership pays 6 when red scores",
    "rule": "R16",
    "players": 3,
    "given": {
      "players": {"3": {"hand_red": 1, "hand_blue": 0, "hand_green": 0}},
      "game": {"round": 17, "auctioneer": 3, "season_red": 0, "season_blue": 0, "season_green": 0, "value_red": 0}
    },
    "rules": [
      {"seat": 3, "options_include": "red"},
      {"seat": 2, "options_include": 5}
    ],
    "expect": {
      "winner": 3,
      "standings": {"1": 60, "2": 61, "3": 65},
      "players": {"1": {"money": 60}, "2": {"money": 61}, "3": {"money": 65}},
      "game": {"value_red": 6}
    }
  },
  {
    "name": "Round 18: the sale runs, then the season ends (blue +6 to 9, red second +3 to 3) and pays out",
    "rule": "R17",
    "players": 3,
    "given": {
      "players": {"3": {"hand_red": 0, "hand_blue": 1, "hand_green": 0}, "2": {"owned_red": 2}},
      "game": {"round": 17, "auctioneer": 3, "season_red": 1, "season_blue": 1, "season_green": 0, "value_red": 0, "value_blue": 3, "value_green": 0}
    },
    "rules": [
      {"seat": 3, "options_include": "blue"},
      {"seat": 1, "options_include": 4}
    ],
    "expect": {
      "winner": 2,
      "standings": {"1": 65, "2": 66, "3": 64},
      "players": {"1": {"money": 65}, "2": {"money": 66}, "3": {"money": 64}},
      "game": {"value_red": 3, "value_blue": 9, "value_green": 0, "season_red": 0, "season_blue": 0, "season_green": 0}
    }
  },
  {
    "name": "Green alone at 3 gains 6 (3 to 9); no second artist; seat 2's green pays 9",
    "rule": "R18",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 1, "hand_blue": 1, "hand_green": 1}, "2": {"owned_green": 1}},
      "game": {"auctioneer": 1, "season_red": 0, "season_blue": 0, "season_green": 2, "value_red": 0, "value_blue": 0, "value_green": 3}
    },
    "rules": [{"seat": 1, "options_include": "green"}],
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 69}, "3": {"money": 60}},
      "game": {"value_green": 9, "value_red": 0, "value_blue": 0}
    }
  },
  {
    "name": "Red top at 3, blue and green tied at 1: no second artist scores, so blue owners get nothing",
    "rule": "R19",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 1, "hand_blue": 1, "hand_green": 1}, "2": {"owned_blue": 1}, "3": {"owned_red": 2}},
      "game": {"auctioneer": 1, "season_red": 2, "season_blue": 1, "season_green": 1, "value_red": 0, "value_blue": 3, "value_green": 0}
    },
    "rules": [{"seat": 1, "options_include": "red"}],
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 60}, "3": {"money": 72}},
      "game": {"value_red": 6, "value_blue": 3, "value_green": 0}
    }
  },
  {
    "name": "Red and blue tie at 2 in the last season: each gains 3, green does not score; seats 2 and 3 share the win",
    "rule": "R20",
    "players": 3,
    "given": {
      "players": {"3": {"hand_red": 0, "hand_blue": 1, "hand_green": 0}, "1": {"owned_green": 1}, "2": {"owned_red": 1}},
      "game": {"round": 17, "auctioneer": 3, "season_red": 2, "season_blue": 1, "season_green": 0, "value_red": 0, "value_blue": 0, "value_green": 6}
    },
    "rules": [{"seat": 3, "options_include": "blue"}],
    "expect": {
      "winner": [2, 3],
      "standings": {"1": 60, "2": 63, "3": 63},
      "players": {"1": {"money": 60}, "2": {"money": 63}, "3": {"money": 63}},
      "game": {"value_red": 3, "value_blue": 3, "value_green": 6}
    }
  },
  {
    "name": "Payout is owned count times the new value, only for scoring artists",
    "rule": "R21",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 1, "hand_blue": 1, "hand_green": 1, "owned_green": 2}, "2": {"owned_red": 1}, "3": {"owned_blue": 3}},
      "game": {"auctioneer": 1, "season_red": 2, "season_blue": 1, "season_green": 0, "value_red": 2, "value_blue": 1, "value_green": 5}
    },
    "rules": [{"seat": 1, "options_include": "red"}],
    "expect": {
      "players": {"1": {"money": 60}, "2": {"money": 68}, "3": {"money": 72}},
      "game": {"value_red": 8, "value_blue": 4, "value_green": 5}
    }
  },
  {
    "name": "After the season payout, season counts reset to 0 and values are kept",
    "rule": "R22",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 1, "hand_blue": 1, "hand_green": 1}},
      "game": {"auctioneer": 1, "season_red": 1, "season_blue": 0, "season_green": 2, "value_red": 6, "value_blue": 3, "value_green": 0}
    },
    "rules": [{"seat": 1, "options_include": "green"}],
    "expect": {
      "game": {"season_red": 0, "season_blue": 0, "season_green": 0, "value_red": 9, "value_blue": 3, "value_green": 6}
    }
  },
  {
    "name": "Season end: new values and each player's money after payout are as announced",
    "rule": "R23",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"1": {"hand_red": 1, "hand_blue": 1, "hand_green": 1, "owned_blue": 1}, "3": {"owned_blue": 2}},
      "game": {"auctioneer": 1, "season_red": 0, "season_blue": 2, "season_green": 0, "value_red": 0, "value_blue": 0, "value_green": 0}
    },
    "rules": [{"seat": 1, "options_include": "blue"}],
    "expect": {
      "players": {"1": {"money": 66}, "2": {"money": 60}, "3": {"money": 72}},
      "game": {"value_blue": 6, "value_red": 0, "value_green": 0}
    }
  },
  {
    "name": "Auctioneer passes 3 to 1 at round end",
    "rule": "R24",
    "players": 3,
    "rounds": 1,
    "given": {
      "players": {"3": {"hand_red": 2, "hand_blue": 1, "hand_green": 4}},
      "game": {"round": 2, "auctioneer": 3}
    },
    "rules": [{"seat": 3, "options_include": "green"}],
    "expect": {"game": {"auctioneer": 1, "round": 3}}
  },
  {
    "name": "Auctioneer passes 1 to 2 to 3 over two rounds from the start",
    "rule": "R24",
    "players": 3,
    "seed": 3,
    "rounds": 2,
    "default": "decline",
    "expect": {"game": {"auctioneer": 3, "round": 2}}
  },
  {
    "name": "After round 18 the richest player wins, counting the last payout",
    "rule": "R25",
    "players": 3,
    "given": {
      "players": {"1": {"money": 80}, "3": {"hand_red": 0, "hand_blue": 1, "hand_green": 0}},
      "game": {"round": 17, "auctioneer": 3, "season_red": 0, "season_blue": 0, "season_green": 0, "value_blue": 0}
    },
    "rules": [{"seat": 3, "options_include": "blue"}],
    "expect": {
      "winner": 1,
      "standings": {"1": 80, "2": 60, "3": 66},
      "players": {"1": {"money": 80}, "2": {"money": 60}, "3": {"money": 66}},
      "game": {"round": 18, "value_blue": 6}
    }
  }
]
```
````
