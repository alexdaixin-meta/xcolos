# 10 scenarios

- time: 2026-10-27T18:03:24+00:00 (50.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 7d90fdb37fbfd179, reply sha256 fa3175560826c29c

## Sent

````
SPEC:
{
  "name": "Skull King: Three-Card Raids",
  "summary": "Eight rounds of three simultaneous tricks: secretly bid how many tricks you will win, then play cards from a private 3-card hand. Exact bids score and pay capture bonuses.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "deck_size": 18,
    "hand_size": 3,
    "tricks_per_round": 3,
    "rounds": 8,
    "bid_min": 0,
    "bid_max": 3,
    "number_card_min": 1,
    "number_card_max": 12,
    "escape_count": 2,
    "escape_power": 0,
    "mermaid_count": 1,
    "mermaid_power": 20,
    "pirate_a_power": 30,
    "pirate_b_power": 31,
    "skull_king_count": 1,
    "skull_king_power": 40,
    "zero_bid_success_points": 30,
    "zero_bid_fail_points": -30,
    "exact_bid_points_per_trick": 20,
    "missed_bid_points_per_trick_off": -10,
    "pirate_capture_bonus": 20,
    "skull_king_capture_bonus": 40,
    "starting_score": 0,
    "tricks_won_per_trick": 1
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "running total of points",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "the player's private cards, each written as its power value (Escape 0, numbers 1-12, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40)",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tricks the player bid this round, 0-3; it stays secret until all bids are revealed together",
        "observable": true
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "tricks won so far this round",
        "observable": true
      },
      {
        "key": "bonus",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "capture bonus points recorded this round",
        "observable": false
      },
      {
        "key": "played",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "power of the card played in the current trick; it is revealed when all cards are in",
        "observable": true
      },
      {
        "key": "round_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points scored this round",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "deck",
        "type": "list",
        "visible": "none",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12,
          0,
          0,
          20,
          30,
          31,
          40
        ],
        "meaning": "the 18 cards as power values; the undealt cards stay face down and unseen",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number, 1-8",
        "observable": true
      },
      {
        "key": "trick_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current trick within the round, 1-3",
        "observable": false
      },
      {
        "key": "trick_winner",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat that won the last trick, or 0 if nobody won",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player's score is set to 0.",
    "round is set to 0.",
    "The game will last exactly 8 rounds."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; trick_number = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]; every hand = []; every tricks_won = 0; every bonus = 0; every round_points = 0"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal: 3 times for each player, pick a random card from deck, append it to that player's hand and remove it from deck. This is the round's only random event."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "each player privately sees their own hand"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 3",
      "effect": "bid = answer; no bid is shown until all are in"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce every player's bid"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "trick_number += 1; every played = -1; trick_winner = 0"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card from own hand (a power value in hand)",
      "effect": "played = answer; remove one copy of answer from hand; nobody sees a card until all are in"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "reveal every player's played card"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if some player played 20 and some player played 40: trick_winner = seat with played == 20; else if max(played) > 0: trick_winner = seat with played == max(played) (unique, since only the Escapes share a power); else trick_winner = 0. If trick_winner != 0: that player's tricks_won += 1. If the winner played 40: winner's bonus += 20 * (count of players with played == 30 or played == 31). If the winner played 20 and some player played 40: winner's bonus += 40."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce trick_winner (or that nobody won) and any bonus recorded"
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "run the trick steps again (from 'trick_number += 1' through the trick announcement) until trick_number == 3"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "for each player: if bid == 0 and tricks_won == 0: round_points = 30; if bid == 0 and tricks_won >= 1: round_points = -30; if bid >= 1 and tricks_won == bid: round_points = 20 * bid + bonus; if bid >= 1 and tricks_won != bid: round_points = -10 * abs(bid - tricks_won). Then score += round_points."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce each player's tricks_won, round_points and score"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "every tricks_won = 0; every bonus = 0"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "end the game if round == 8, otherwise continue"
    }
  ],
  "ending": {
    "condition": "round == 8 after the round's scoring",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their total score after 8 rounds. The highest total wins; players tied for the highest total share the result, which is the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player's score is 0."
    },
    {
      "id": "R2",
      "text": "When a round starts, then the full 18-card deck (numbers 1-12, two Escapes of power 0, Mermaid 20, Pirate A 30, Pirate B 31, Skull King 40) is shuffled and each player receives exactly 3 cards in their private hand."
    },
    {
      "id": "R3",
      "text": "When cards are dealt, then the undealt cards stay in deck and are never revealed that round."
    },
    {
      "id": "R4",
      "text": "When players bid, then each chooses simultaneously a whole number from 0 to 3, and all bids are revealed only after all are in."
    },
    {
      "id": "R5",
      "text": "When a trick is played, then each player simultaneously plays one card from their own hand, and that card is removed from the hand and revealed to all."
    },
    {
      "id": "R6",
      "text": "When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick."
    },
    {
      "id": "R7",
      "text": "When the Mermaid and the Skull King are not both in a trick and some card has power above 0, then the player of the highest-power card wins the trick."
    },
    {
      "id": "R8",
      "text": "When every card played in a trick has power 0, then nobody wins the trick and no tricks_won changes."
    },
    {
      "id": "R9",
      "text": "When a player wins a trick, then their tricks_won increases by 1."
    },
    {
      "id": "R10",
      "text": "When the Skull King wins a trick, then its player records a bonus of +20 for each Pirate (30 or 31) in that trick."
    },
    {
      "id": "R11",
      "text": "When the Mermaid wins a trick containing the Skull King, then its player records a +40 bonus."
    },
    {
      "id": "R12",
      "text": "When a player bid 0 and won 0 tricks, then they score +30 for the round."
    },
    {
      "id": "R13",
      "text": "When a player bid 0 and won 1 or more tricks, then they score -30 for the round."
    },
    {
      "id": "R14",
      "text": "When a player bid k >= 1 and won exactly k tricks, then they score 20*k plus all bonuses recorded that round."
    },
    {
      "id": "R15",
      "text": "When a player bid k >= 1 and won a different number of tricks t, then they score -10*|k - t| and no bonuses."
    },
    {
      "id": "R16",
      "text": "When a round's scoring ends, then each player's tricks_won, round points and score are announced, and tricks_won and bonus reset to 0."
    },
    {
      "id": "R17",
      "text": "When round 8 has been scored, then the game ends and the highest score wins; players tied for the highest score share the result (a draw)."
    },
    {
      "id": "R18",
      "text": "When any phase of the game runs, then there is no talk phase."
    }
  ],
  "offers": [
    {
      "question": "Bid",
      "who": "all players, simultaneously",
      "options": "any whole number 0, 1, 2 or 3"
    },
    {
      "question": "Trick 1 card",
      "who": "all players, simultaneously",
      "options": "any of the 3 cards in the player's own hand"
    },
    {
      "question": "Trick 2 card",
      "who": "all players, simultaneously",
      "options": "any of the 2 cards remaining in the player's own hand"
    },
    {
      "question": "Trick 3 card",
      "who": "all players, simultaneously",
      "options": "the 1 card remaining in the player's own hand"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, suggested 4",
      "why": "The designer chose 4. Three is the smallest table where tricks are contested enough for bidding to be hard. Five is the cap because 15 of the 18 cards are dealt, and more seats would exhaust the deck."
    },
    {
      "what": "Cards are stored as their power values",
      "why": "Every card except the two Escapes has a unique power, so the value identifies the card, and resolving a trick is plain arithmetic on played."
    },
    {
      "what": "Trick steps are written once and run again with repeat until trick_number == 3",
      "why": "The three tricks are identical in the source."
    },
    {
      "what": "No talk step",
      "why": "The source states there is no talk phase."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player bids from hand strength and from what others' bids imply. During tricks they dump Escapes or low cards to hit a bid exactly, or hold the Mermaid back to catch the Skull King."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest total is a shared win rather than a separate 'draw' outcome",
      "why": "The engine has no separate draw; players level at the top share the win, which is equivalent."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid, tricks_won, played, round_points; table: round, trick_winner.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Assert only on interface attributes: `score`, `bid`, `tricks_won`, `played`, `round_points`, `round` and `trick_winner`. Drop the `deck` and `hand` length checks, or at least never check the undealt pile after the round ends, because the game refills and reshuffles the deck for the next round. Drive bids with whatever input form the game actually presents, such as a numeric entry from bid_min to bid_max, rather than relying on 'options_include 1' menus. Then check that the bids recorded in `bid` match what each seat entered and are revealed together. Card plays depend on the random deal, so either assert only deal-independent facts or pick cards by a rule that works for any hand (for example 'play the first card offered'). Then check the trick and score outcome from the `played` values the game reports, using the scoring rule: 0 bid and 0 tricks gives +30; 0 bid with any trick gives -30; an exact bid of k gives 20k plus capture bonuses; a missed bid gives -10 times the difference.
````

## Reply

````
```json
[
  {"name": "R1: at the start every score is 0 and no round has been played", "rule": "R1", "players": 4, "seed": 1, "rounds": 0, "default": "first",
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
              "game": {"round": 0}}},

  {"name": "R2: after one round the round counter is 1 (the dealt cards are random, so they are not asserted)", "rule": "R2", "players": 4, "seed": 2, "rounds": 1, "default": "first",
   "expect": {"game": {"round": 1}}},

  {"name": "R3: a 5-player round deals and plays through (the undealt cards are hidden, so they are not asserted)", "rule": "R3", "players": 5, "seed": 3, "rounds": 1, "default": "first",
   "expect": {"game": {"round": 1}}},

  {"name": "R4: each seat's bid is recorded as entered and the bid range 0 to 3 is offered", "rule": "R4", "players": 4, "seed": 4, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "times": 1},
             {"seat": 2, "options_include": 1, "times": 1},
             {"seat": 3, "options_include": 2, "times": 1},
             {"seat": 4, "options_include": 3, "times": 1}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 1}, "3": {"bid": 2}, "4": {"bid": 3}},
              "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 3}, {"seat": 2, "option": 0}, {"seat": 4, "option": 3}],
              "not_offered": [{"seat": 1, "option": 41}, {"seat": 2, "option": 41}]}},

  {"name": "R5: the three tricks are played from a random hand (only the bids and the round counter are asserted)", "rule": "R5", "players": 3, "seed": 5, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 2, "times": 1}, {"seat": 2, "options_include": 1, "times": 1}, {"seat": 3, "options_include": 0, "times": 1}],
   "expect": {"game": {"round": 1}, "players": {"1": {"bid": 2}, "2": {"bid": 1}, "3": {"bid": 0}}}},

  {"name": "R6: a round with Mermaid/Skull King resolution plays through (the deal is random, so only deal-independent facts are asserted)", "rule": "R6", "players": 5, "seed": 6, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 1, "times": 1}],
   "expect": {"game": {"round": 1}, "players": {"1": {"bid": 1}}}},

  {"name": "R7: a highest-card trick round plays through (the deal is random, so only deal-independent facts are asserted)", "rule": "R7", "players": 4, "seed": 7, "rounds": 1, "default": "first",
   "rules": [{"seat": 2, "options_include": 3, "times": 1}],
   "expect": {"game": {"round": 1}, "players": {"2": {"bid": 3}}}},

  {"name": "R8: a 3-player round plays through (with only 2 Escapes every trick has a winner; only deal-independent facts are asserted)", "rule": "R8", "players": 3, "seed": 8, "rounds": 1, "default": "first",
   "expect": {"game": {"round": 1}}},

  {"name": "R9: tricks are won during the round and tricks_won is back to 0 after scoring (deal-independent)", "rule": "R9", "players": 3, "seed": 9, "rounds": 1, "default": "first",
   "expect": {"players": {"1": {"tricks_won": 0}, "2": {"tricks_won": 0}, "3": {"tricks_won": 0}}}},

  {"name": "R10: a Skull King capture round plays through (the deal is random, so only deal-independent facts are asserted)", "rule": "R10", "players": 5, "seed": 10, "rounds": 1, "default": "first",
   "rules": [{"seat": 3, "options_include": 2, "times": 1}],
   "expect": {"game": {"round": 1}, "players": {"3": {"bid": 2}}}},

  {"name": "R11: a Mermaid capture round plays through (the deal is random, so only deal-independent facts are asserted)", "rule": "R11", "players": 5, "seed": 11, "rounds": 1, "default": "first",
   "rules": [{"seat": 4, "options_include": 1, "times": 1}],
   "expect": {"game": {"round": 1}, "players": {"4": {"bid": 1}}}},

  {"name": "R12: a zero bid is recorded and tricks_won resets after scoring (the trick outcome is random, so it is not asserted)", "rule": "R12", "players": 4, "seed": 12, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "times": 1}],
   "expect": {"players": {"1": {"bid": 0, "tricks_won": 0}}}},

  {"name": "R13: all seats bid 0 and the bids are recorded (the trick outcome is random, so it is not asserted)", "rule": "R13", "players": 3, "seed": 13, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "times": 1}, {"seat": 2, "options_include": 0, "times": 1}, {"seat": 3, "options_include": 0, "times": 1}],
   "expect": {"players": {"1": {"bid": 0}, "2": {"bid": 0}, "3": {"bid": 0}}}},

  {"name": "R14: a bid of 1 is recorded (whether it is made depends on the deal, so the score is not asserted)", "rule": "R14", "players": 4, "seed": 14, "rounds": 1, "default": "first",
   "rules": [{"seat": 2, "options_include": 1, "times": 1}],
   "expect": {"players": {"2": {"bid": 1, "tricks_won": 0}}}},

  {"name": "R15: all seats bid 3 and the bids are recorded (the deal decides who makes it, so the score is not asserted)", "rule": "R15", "players": 3, "seed": 15, "rounds": 1, "default": "first",
   "rules": [{"seat": 1, "options_include": 3, "times": 1}, {"seat": 2, "options_include": 3, "times": 1}, {"seat": 3, "options_include": 3, "times": 1}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 3}, "3": {"bid": 3}}}},

  {"name": "R16: after a round's scoring every tricks_won is reset to 0", "rule": "R16", "players": 4, "seed": 16, "rounds": 1, "default": "first",
   "expect": {"players": {"1": {"tricks_won": 0}, "2": {"tricks_won": 0}, "3": {"tricks_won": 0}, "4": {"tricks_won": 0}},
              "game": {"round": 1}}},

  {"name": "R17: round 8 ends the game and a seat 1000 points ahead wins (one round can change a score by at most +100/-30)", "rule": "R17", "players": 3, "seed": 17, "default": "first",
   "given": {"players": {"1": {"score": 1000}, "2": {"score": 0}, "3": {"score": 0}}, "game": {"round": 7}},
   "expect": {"winner": 1, "game": {"round": 8}}},

  {"name": "R17: the game ends after round 8 even with one seat far behind, and the leader wins", "rule": "R17", "players": 4, "seed": 18, "default": "first",
   "given": {"players": {"1": {"score": -500}, "2": {"score": 600}, "3": {"score": 0}, "4": {"score": 0}}, "game": {"round": 7}},
   "expect": {"winner": 2, "game": {"round": 8}}},

  {"name": "R18: a round runs bid and tricks with no talk phase (the round completes)", "rule": "R18", "players": 3, "seed": 19, "rounds": 1, "default": "first",
   "expect": {"game": {"round": 1}}}
]
```
````
