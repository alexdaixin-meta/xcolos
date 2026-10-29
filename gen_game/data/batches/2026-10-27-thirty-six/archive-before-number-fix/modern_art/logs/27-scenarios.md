# 27 scenarios

- time: 2026-10-27T17:18:16+00:00 (90.4s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 c1469a7cae705c4c, reply sha256 43cfc785d03af834

## Sent

````
SPEC:
{
  "name": "Modern Art: Three Studios",
  "summary": "Three dealers take turns auctioning paintings by three artists with sealed bids; at the end of each season the most-played artists pay out, and after 3 seasons or when all cards are gone the richest player wins.",
  "players": {
    "min": 3,
    "max": 3,
    "suggested": 3
  },
  "parameters": {
    "player_count": 3,
    "starting_money": 60,
    "hand_size": 7,
    "composition_A_red": 4,
    "composition_A_blue": 2,
    "composition_A_green": 1,
    "composition_B_red": 1,
    "composition_B_blue": 4,
    "composition_B_green": 2,
    "composition_C_red": 2,
    "composition_C_blue": 1,
    "composition_C_green": 4,
    "deal_roll_min": 1,
    "deal_roll_max": 6,
    "season_ending_count": 3,
    "first_place_bonus": 20,
    "second_place_bonus": 10,
    "seasons_to_end": 3,
    "max_rounds": 21,
    "min_bid": 0,
    "first_auctioneer_seat": 1
  },
  "attributes": {
    "player": [
      {
        "key": "money",
        "type": "number",
        "visible": "public",
        "initial": 60,
        "meaning": "Money held; the score",
        "observable": true
      },
      {
        "key": "hand_red",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Red cards in hand",
        "observable": false
      },
      {
        "key": "hand_blue",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Blue cards in hand",
        "observable": false
      },
      {
        "key": "hand_green",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Green cards in hand",
        "observable": false
      },
      {
        "key": "owned_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red paintings bought this season",
        "observable": true
      },
      {
        "key": "owned_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue paintings bought this season",
        "observable": true
      },
      {
        "key": "owned_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green paintings bought this season",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "This round's sealed bid. It stays hidden until all bids are in, then all bids are announced",
        "observable": false
      },
      {
        "key": "message",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "This round's talk message, shown once all are in",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "auctioneer",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "Seat of the current auctioneer",
        "observable": true
      },
      {
        "key": "seasons_done",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seasons scored so far",
        "observable": true
      },
      {
        "key": "current_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Artist of the card just played (Red, Blue or Green)",
        "observable": true
      },
      {
        "key": "season_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Red cards played this season",
        "observable": true
      },
      {
        "key": "season_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Blue cards played this season",
        "observable": true
      },
      {
        "key": "season_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Green cards played this season",
        "observable": true
      },
      {
        "key": "value_red",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Red",
        "observable": true
      },
      {
        "key": "value_blue",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Blue",
        "observable": true
      },
      {
        "key": "value_green",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Cumulative value of Green",
        "observable": true
      },
      {
        "key": "deal_roll",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "Random 1-6 that picks which seat gets which hand composition",
        "observable": false
      },
      {
        "key": "season_ended",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when the card just played was the season-ending card",
        "observable": false
      },
      {
        "key": "winner_seat",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Seat that won this round's auction",
        "observable": true
      },
      {
        "key": "price",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Price paid by this round's auction winner",
        "observable": true
      },
      {
        "key": "scoring_now",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "True when season scoring happens this round",
        "observable": false
      },
      {
        "key": "first_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Artist placed first this season",
        "observable": false
      },
      {
        "key": "second_artist",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "Artist placed second this season, or empty if none",
        "observable": false
      }
    ]
  },
  "setup": [
    "Seats 1, 2 and 3 each get money 60 and all hand and owned counts at 0. All season counts and cumulative values are 0, seasons_done is 0, and auctioneer is 1.",
    "The engine draws deal_roll uniformly from 1 to 6. This is the only random event in the game.",
    "Compositions are dealt to seats 1, 2 and 3 by deal_roll: 1 gives A,B,C; 2 gives A,C,B; 3 gives B,A,C; 4 gives B,C,A; 5 gives C,A,B; 6 gives C,B,A. A sets hand_red/blue/green to 4/2/1, B sets them to 1/4/2, and C sets them to 2/1/4.",
    "Everyone is told that compositions A, B and C exist and that each seat holds a different one. Each player is sent only their own hand counts (sync)."
  ],
  "round": [
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player sees their own hand counts and all public state: money, owned counts, season counts, values and auctioneer."
    },
    {
      "action": "ask",
      "who": "the seat named by auctioneer",
      "answer": "one of Red, Blue, Green, limited to artists whose own hand count is above 0",
      "effect": "current_artist := the chosen artist"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The auctioneer's hand_<current_artist> -= 1; season_<current_artist> += 1; season_ended := (season_<current_artist> == 3). Announce: 'Seat {auctioneer} plays {current_artist}.' If season_ended, also announce that the card is discarded unsold."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text",
      "effect": "when season_ended is false: message := the answer; then broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}. The talk is not binding."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "whole number from 0 to own money",
      "effect": "when season_ended is false: bid := the answer, hidden until all are in"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when season_ended is false: compute each seat's offset = (seat - auctioneer + 3) mod 3 and key = bid*3 + ((3 - offset) mod 3), so the seat after the auctioneer breaks ties first and the auctioneer last. If the highest bid is 0, winner_seat := auctioneer and price := 0. Otherwise winner_seat := the seat with the highest key and price := that seat's bid. If winner_seat != auctioneer, the winner's money -= price and the auctioneer's money += price. If winner_seat == auctioneer, the auctioneer's money -= price (paid to the bank). The winner's owned_<current_artist> += 1. Announce all three bids, winner_seat and price."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "scoring_now := season_ended OR (sum over players of hand_red+hand_blue+hand_green == 0 AND season_red+season_blue+season_green > 0)"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when scoring_now: first_artist := the artist with the highest season count, ties broken Red > Blue > Green; value_<first_artist> += 20. second_artist := the highest of the other two by season count (same tie order) if its season count > 0, otherwise empty; if not empty, value_<second_artist> += 10. Each player's money += owned_<first_artist>*value_<first_artist> + (owned_<second_artist>*value_<second_artist> if second_artist is not empty). Unplaced artists pay 0. Announce the placings, the new values and each payout."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "when scoring_now: every owned_red, owned_blue and owned_green := 0; season_red, season_blue and season_green := 0; seasons_done += 1"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "auctioneer := the next seat after auctioneer in the order 1->2->3->1 whose hand_red+hand_blue+hand_green > 0. If no seat has cards, it is left unchanged."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if seasons_done >= 3 or the sum over players of hand_red+hand_blue+hand_green == 0; otherwise continue."
    }
  ],
  "ending": {
    "condition": "seasons_done >= 3 OR sum over players of (hand_red + hand_blue + hand_green) == 0",
    "rank_by": "you.money",
    "decided_by": "Each player's standing is their money. The player with the most money wins. Players tied for the most money share the result, which the source calls a draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At setup, every player has money 60 and all owned counts 0, every artist has season count 0 and value 0, seasons_done is 0, and auctioneer is seat 1."
    },
    {
      "id": "R2",
      "text": "At setup, when deal_roll is 1 the seats 1,2,3 get compositions A,B,C; for 2 they get A,C,B; for 3 B,A,C; for 4 B,C,A; for 5 C,A,B; for 6 C,B,A. A is Red 4, Blue 2, Green 1; B is Red 1, Blue 4, Green 2; C is Red 2, Blue 1, Green 4."
    },
    {
      "id": "R3",
      "text": "Each player's hand counts are visible only to that player, and every hand totals 7 cards at setup."
    },
    {
      "id": "R4",
      "text": "The auctioneer may choose only an artist for which their own hand count is above 0."
    },
    {
      "id": "R5",
      "text": "When the auctioneer plays artist X, their hand_X falls by 1, season_X rises by 1, and current_artist is announced as X."
    },
    {
      "id": "R6",
      "text": "When season_X reaches 3 after the play, the card is discarded unsold: there is no talk, no bidding, no money moves and no owned count changes, and season scoring happens."
    },
    {
      "id": "R7",
      "text": "When the card is not season-ending, all three players send one short message simultaneously, and all messages are then shown to everyone."
    },
    {
      "id": "R8",
      "text": "When the card is not season-ending, all three players including the auctioneer bid simultaneously a whole number from 0 to their current money."
    },
    {
      "id": "R9",
      "text": "The highest bid wins the painting; with the auctioneer at seat 1 and bids 15, 15, 15, seat 2 wins at 15."
    },
    {
      "id": "R10",
      "text": "When bids tie for highest, the tied seat first in order starting after the auctioneer wins, with the auctioneer last; with the auctioneer at seat 2 and bids seat1=10, seat2=10, seat3=5, seat 1 wins."
    },
    {
      "id": "R11",
      "text": "When every bid is 0, the auctioneer wins the painting at price 0."
    },
    {
      "id": "R12",
      "text": "When a non-auctioneer wins with bid 12, the winner's money falls by 12 and the auctioneer's money rises by 12."
    },
    {
      "id": "R13",
      "text": "When the auctioneer wins with bid 12, the auctioneer's money falls by 12 and no other player's money changes."
    },
    {
      "id": "R14",
      "text": "The auction winner's owned count for the current artist rises by 1, including when the winner is the auctioneer."
    },
    {
      "id": "R15",
      "text": "After an auction, all three bids, the winner and the price are announced to everyone."
    },
    {
      "id": "R16",
      "text": "Season scoring happens when the season-ending card was just played, or when all hands are empty and at least one season count is above 0."
    },
    {
      "id": "R17",
      "text": "At scoring, the artist with the highest season count places first, ties broken Red, then Blue, then Green, and its value rises by 20."
    },
    {
      "id": "R18",
      "text": "At scoring, the best of the remaining two artists by season count (same tie order) places second only if its season count is above 0, and its value rises by 10."
    },
    {
      "id": "R19",
      "text": "At scoring, each player gains, for each placed artist, owned count times that artist's new cumulative value; unplaced artists pay 0 even if their value is above 0. With Red first at value 30 and a player owning 2 Red, that player gains 60 from Red."
    },
    {
      "id": "R20",
      "text": "After scoring, all owned counts and season counts reset to 0 and seasons_done rises by 1."
    },
    {
      "id": "R21",
      "text": "After each round, the auctioneer passes to the next seat in the order 1->2->3->1, skipping any seat whose hand is empty."
    },
    {
      "id": "R22",
      "text": "The game ends when seasons_done reaches 3, or when all hands are empty after any unfinished season has been scored; it lasts at most 21 rounds."
    },
    {
      "id": "R23",
      "text": "When the game ends, the player with the most money wins; players tied for the most money share the result (a draw)."
    },
    {
      "id": "R24",
      "text": "Money and owned counts are public at all times."
    }
  ],
  "offers": [
    {
      "question": "Choose a card to auction",
      "who": "the seat named by auctioneer",
      "options": "each of Red, Blue, Green for which that seat's own hand count is above 0; never an artist with hand count 0"
    },
    {
      "question": "Talk message",
      "who": "all three seats, only when the card played is not season-ending",
      "options": "one short free-text message"
    },
    {
      "question": "Sealed bid",
      "who": "all three seats including the auctioneer, only when the card played is not season-ending",
      "options": "any whole number from 0 up to that seat's current money"
    }
  ],
  "choices": [
    {
      "what": "Exactly 3 players, suggested 3",
      "why": "The designer fixed the table at 3, and the deal (six permutations of three compositions) only works for 3 seats."
    },
    {
      "what": "Tie-break encoded as key = bid*3 + ((3 - offset) mod 3), where offset = (seat - auctioneer + 3) mod 3",
      "why": "This turns the seat-order tie rule into arithmetic: the seat after the auctioneer has priority 2, the next has 1, and the auctioneer has 0. All-zero bids are a separate case that gives the painting to the auctioneer."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all, before the bid poll",
      "why": "The source requires it. It also earns its place: players disagree about which artist to push and can bluff about their hidden compositions."
    },
    {
      "what": "Helper table attributes season_ended, scoring_now, winner_seat, price, first_artist and second_artist",
      "why": "The flat step list needs flags so that later steps can carry arithmetic 'when' conditions."
    },
    {
      "what": "If no seat has cards when the role passes, the auctioneer is left unchanged",
      "why": "The game ends at the check in the same round, so the value never matters."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player infers the others' compositions from what they play and bid, steers seasons toward artists they own, bids up to an artist's likely payout, and sometimes buys their own card so it scores for them."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the most money is reported as a shared win among the tied players, not as a separate draw",
      "why": "The engine ranks by one expression and players level at the top share the win, which corresponds to the source's draw."
    },
    {
      "what": "The hand is three counters (hand_red, hand_blue, hand_green) rather than a list of cards",
      "why": "Cards of one artist are identical, so counts carry exactly the same information."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: money, owned_red, owned_blue, owned_green; table: auctioneer, seasons_done, current_artist, season_red, season_blue, season_green, value_red, value_blue, value_green, winner_seat, price.
````

## Reply

````
```json
[
  {"name": "Setup: money 60, owned 0, seasons and values 0, auctioneer seat 1", "rule": "R1", "players": 3, "seed": 1, "rounds": 0,
   "expect": {"players": {"1": {"money": 60, "owned_red": 0, "owned_blue": 0, "owned_green": 0},
                          "2": {"money": 60, "owned_red": 0, "owned_blue": 0, "owned_green": 0},
                          "3": {"money": 60, "owned_red": 0, "owned_blue": 0, "owned_green": 0}},
              "game": {"auctioneer": 1, "seasons_done": 0, "season_red": 0, "season_blue": 0, "season_green": 0,
                       "value_red": 0, "value_blue": 0, "value_green": 0}}},

  {"name": "Deal (chance-independent): every composition holds all three artists, so seats 1 and 2 are each offered Red, Blue and Green", "rule": "R2", "players": 3, "seed": 1, "rounds": 2, "default": "first",
   "expect": {"offered": [{"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"},
                          {"seat": 2, "option": "Red"}, {"seat": 2, "option": "Blue"}, {"seat": 2, "option": "Green"}]}},

  {"name": "Hands (chance-independent): seat 1 opens holding cards of every artist", "rule": "R3", "players": 3, "seed": 2, "rounds": 1, "default": "first",
   "expect": {"offered": [{"seat": 1, "option": "Red"}, {"seat": 1, "option": "Blue"}, {"seat": 1, "option": "Green"}]}},

  {"name": "Auctioneer may only play an artist it holds", "rule": "R4", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 0, "hand_blue": 2, "hand_green": 0}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Blue"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 1, "option": "Blue"}],
              "not_offered": [{"seat": 1, "option": "Red"}, {"seat": 1, "option": "Green"}],
              "game": {"current_artist": "Blue", "season_blue": 1}}},

  {"name": "Playing Red raises season_red by 1 and sets current_artist", "rule": "R5", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"current_artist": "Red", "season_red": 1, "season_blue": 0, "season_green": 0}}},

  {"name": "Third Red card is discarded unsold: no bidding, no money moves, and the season scores", "rule": "R6", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}},
             "game": {"auctioneer": 1, "season_red": 2, "season_blue": 0, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Red"}],
   "expect": {"players": {"1": {"money": 60, "owned_red": 0}, "2": {"money": 60, "owned_red": 0}, "3": {"money": 60, "owned_red": 0}},
              "game": {"seasons_done": 1, "season_red": 0, "value_red": 20},
              "not_offered": [{"seat": 2, "option": 0}, {"seat": 3, "option": 0}]}},

  {"name": "A card that does not end the season goes to auction for the other seats", "rule": "R7", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 2, "option": 0}, {"seat": 3, "option": 0}]}},

  {"name": "Bids run from 0 to the bidder's own money, and the auctioneer bids too", "rule": "R8", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}, "2": {"money": 10}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"offered": [{"seat": 2, "option": 10}, {"seat": 1, "option": 0}],
              "not_offered": [{"seat": 2, "option": 11}]}},

  {"name": "Auctioneer seat 1, bids 15/15/15: seat 2 wins at 15", "rule": "R9", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 15},
             {"seat": 2, "options_include": 15}, {"seat": 3, "options_include": 15}],
   "expect": {"players": {"1": {"money": 75}, "2": {"money": 45, "owned_red": 1}, "3": {"money": 60, "owned_red": 0}},
              "game": {"winner_seat": 2, "price": 15}}},

  {"name": "Auctioneer seat 2, bids seat1=10 seat2=10 seat3=5: seat 1 wins the tie", "rule": "R10", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"2": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 2}},
   "rules": [{"seat": 2, "options_include": "Blue"}, {"seat": 2, "options_include": 10},
             {"seat": 1, "options_include": 10}, {"seat": 3, "options_include": 5}],
   "expect": {"players": {"1": {"money": 50, "owned_blue": 1}, "2": {"money": 70, "owned_blue": 0}, "3": {"money": 60}},
              "game": {"winner_seat": 1, "price": 10}}},

  {"name": "All bids 0: the auctioneer gets the painting at price 0", "rule": "R11", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"money": 60, "owned_green": 1}, "2": {"money": 60}, "3": {"money": 60}},
              "game": {"winner_seat": 1, "price": 0}}},

  {"name": "Non-auctioneer seat 3 wins at 12 and pays the auctioneer", "rule": "R12", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 12}],
   "expect": {"players": {"1": {"money": 72}, "2": {"money": 60}, "3": {"money": 48, "owned_red": 1}},
              "game": {"winner_seat": 3, "price": 12}}},

  {"name": "Auctioneer wins at 12 and pays the bank", "rule": "R13", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 12},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"money": 48, "owned_red": 1}, "2": {"money": 60}, "3": {"money": 60}},
              "game": {"winner_seat": 1, "price": 12}}},

  {"name": "Auctioneer buying its own card adds to its owned count", "rule": "R14", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2, "owned_blue": 1}}, "game": {"auctioneer": 1, "season_blue": 1}},
   "rules": [{"seat": 1, "options_include": "Blue"}, {"seat": 1, "options_include": 5},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"money": 55, "owned_blue": 2}}, "game": {"season_blue": 2}}},

  {"name": "Winner and price are announced: seat 3 bids 20 over seat 2's 7", "rule": "R15", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 20}],
   "expect": {"players": {"1": {"money": 80}, "2": {"money": 60}, "3": {"money": 40, "owned_green": 1}},
              "game": {"winner_seat": 3, "price": 20}}},

  {"name": "Last card played: season scores with all hands empty (Blue/Green tie goes to Blue), then the game ends", "rule": "R16", "players": 3, "seed": 1,
   "given": {"players": {"1": {"hand_red": 0, "hand_blue": 0, "hand_green": 1},
                         "2": {"hand_red": 0, "hand_blue": 0, "hand_green": 0},
                         "3": {"hand_red": 0, "hand_blue": 0, "hand_green": 0, "owned_blue": 1}},
             "game": {"auctioneer": 1, "season_red": 0, "season_blue": 1, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 10}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 3, "standings": {"1": 70, "2": 60, "3": 80},
              "game": {"value_blue": 20, "value_green": 10, "value_red": 0, "seasons_done": 1}}},

  {"name": "Three-way tie in season counts: Red first, Blue second, Green unplaced", "rule": "R17", "players": 3, "seed": 1,
   "given": {"players": {"1": {"hand_red": 0, "hand_blue": 0, "hand_green": 1},
                         "2": {"hand_red": 0, "hand_blue": 0, "hand_green": 0, "owned_red": 1},
                         "3": {"hand_red": 0, "hand_blue": 0, "hand_green": 0, "owned_blue": 1}},
             "game": {"auctioneer": 1, "season_red": 1, "season_blue": 1, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"winner": 2, "standings": {"1": 60, "2": 80, "3": 70},
              "game": {"value_red": 20, "value_blue": 10, "value_green": 0}}},

  {"name": "No second place when the other artists have season count 0", "rule": "R18", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}, "2": {"owned_red": 2}},
             "game": {"auctioneer": 1, "season_red": 2, "season_blue": 0, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Red"}],
   "expect": {"players": {"1": {"money": 60}, "2": {"money": 100}, "3": {"money": 60}},
              "game": {"value_red": 20, "value_blue": 0, "value_green": 0, "seasons_done": 1}}},

  {"name": "Payout uses the new cumulative value; an unplaced artist pays 0 despite its value", "rule": "R19", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2, "owned_blue": 1},
                         "2": {"owned_red": 2}, "3": {"owned_green": 1}},
             "game": {"auctioneer": 1, "season_red": 2, "season_blue": 1, "season_green": 1, "value_red": 10, "value_green": 30}},
   "rules": [{"seat": 1, "options_include": "Red"}],
   "expect": {"players": {"1": {"money": 70}, "2": {"money": 120}, "3": {"money": 60}},
              "game": {"value_red": 30, "value_blue": 10, "value_green": 30}}},

  {"name": "After scoring, owned and season counts reset and seasons_done rises", "rule": "R20", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2, "owned_green": 1}, "2": {"owned_blue": 1}},
             "game": {"auctioneer": 1, "seasons_done": 1, "season_red": 0, "season_blue": 1, "season_green": 2}},
   "rules": [{"seat": 1, "options_include": "Green"}],
   "expect": {"players": {"1": {"owned_red": 0, "owned_blue": 0, "owned_green": 0},
                          "2": {"owned_red": 0, "owned_blue": 0, "owned_green": 0},
                          "3": {"owned_red": 0, "owned_blue": 0, "owned_green": 0}},
              "game": {"seasons_done": 2, "season_red": 0, "season_blue": 0, "season_green": 0}}},

  {"name": "Auctioneer passes from 1 to 3, skipping seat 2 whose hand is empty", "rule": "R21", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2},
                         "2": {"hand_red": 0, "hand_blue": 0, "hand_green": 0},
                         "3": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}},
             "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Red"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 0}, {"seat": 3, "options_include": 0}],
   "expect": {"game": {"auctioneer": 3}}},

  {"name": "Third season scored ends the game; richest seat wins", "rule": "R22", "players": 3, "seed": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2, "money": 60}, "2": {"money": 70}, "3": {"money": 50}},
             "game": {"auctioneer": 1, "seasons_done": 2, "season_red": 2, "season_blue": 0, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Red"}],
   "expect": {"winner": 2, "standings": {"1": 60, "2": 70, "3": 50}, "game": {"seasons_done": 3, "value_red": 20}}},

  {"name": "Tied for most money at the end: both seats share the win", "rule": "R23", "players": 3, "seed": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2, "money": 80}, "2": {"money": 80}, "3": {"money": 50}},
             "game": {"auctioneer": 1, "seasons_done": 2, "season_red": 0, "season_blue": 2, "season_green": 0}},
   "rules": [{"seat": 1, "options_include": "Blue"}],
   "expect": {"winner": [1, 2], "standings": {"1": 80, "2": 80, "3": 50}}},

  {"name": "Money and owned counts are public after a purchase", "rule": "R24", "players": 3, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"hand_red": 2, "hand_blue": 2, "hand_green": 2}}, "game": {"auctioneer": 1}},
   "rules": [{"seat": 1, "options_include": "Green"}, {"seat": 1, "options_include": 0},
             {"seat": 2, "options_include": 7}, {"seat": 3, "options_include": 0}],
   "expect": {"players": {"1": {"money": 67, "owned_green": 0}, "2": {"money": 53, "owned_green": 1}, "3": {"money": 60, "owned_green": 0}}}}
]
```
````
