# 38 scenarios

- time: 2026-10-27T18:30:23+00:00 (25.2s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 8ec54e30c4766c4b, reply sha256 5b4c8b3bbab37f82

## Sent

````
SPEC:
{
  "name": "Skull King: Blind Broadsides",
  "summary": "A simultaneous trick-taking game over 10 rounds: players bid how many of 3 tricks they will win, then all play a card at once in each trick, scoring for exact bids and a bonus when the Mermaid captures the Skull King.",
  "players": {
    "min": 3,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "rounds": 10,
    "hand_size": 3,
    "tricks_per_round": 3,
    "revealed_cards": 3,
    "bid_min": 0,
    "bid_max": 3,
    "deck_size": 18,
    "number_card_min": 1,
    "number_card_max": 12,
    "escape_count": 2,
    "escape_power": 0,
    "mermaid_power": 20,
    "pirate_a_power": 30,
    "pirate_b_power": 31,
    "skull_king_power": 40,
    "made_bid_points": 30,
    "mermaid_capture_bonus": 10,
    "miss_penalty_per_trick": 10,
    "initial_score": 0,
    "initial_round": 0
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Running total of points.",
        "observable": true
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks bid this round (0 to 3). It is gathered by a simultaneous poll, so no bid is seen until all are in.",
        "observable": true
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Tricks won this round.",
        "observable": true
      },
      {
        "key": "bonus",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Bonus earned this round: +10 each time this player's Mermaid captures the Skull King.",
        "observable": false
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "Private hand of card powers (0 = Escape, 1-12 = numbers, 20 = Mermaid, 30 = Pirate A, 31 = Pirate B, 40 = Skull King).",
        "observable": false
      },
      {
        "key": "played",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Power of the card played in the current trick, shown after all have played; -1 means none.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Round counter, 1 to 10.",
        "observable": true
      },
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
        "meaning": "Hidden deck of card powers. It is reset to all 18 cards each round, and cards are drawn from it at random.",
        "observable": false
      },
      {
        "key": "revealed",
        "type": "list",
        "visible": "public",
        "initial": [],
        "meaning": "The 3 face-up cards that are out of play this round.",
        "observable": true
      },
      {
        "key": "trick",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "Trick counter within the round, 0 to 3.",
        "observable": false
      },
      {
        "key": "winning_power",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "Power that wins the current trick: 20 if both the Mermaid and the Skull King were played, otherwise the highest played power.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player's score is set to 0.",
    "The table's round counter is set to 0."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1; for every player: tricks_won = 0, bonus = 0, hand = [], played = -1; revealed = []; trick = 0; deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. Announce the new round number."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Deal: for each player, 3 times, pick a random card from deck, append it to that player's hand and remove it from deck (random picks are the shuffle)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Reveal: 3 times, pick a random card from deck, append it to revealed and remove it from deck. The rest of deck stays hidden (3 cards with 4 players, 6 with 3)."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player is sent their own hand, the revealed list, the scores and the round number."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from 0 to 3",
      "effect": "Each player's bid = their answer. No one sees a bid until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's bid to everyone."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one card (power) from the player's own hand",
      "effect": "Each player's played = the chosen card, which is removed from their hand. No one sees a choice until all are in."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Show every player's played card to everyone at once."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "winning_power = 20 if some player's played == 20 and some player's played == 40, otherwise the maximum of played over all players. The player whose played == winning_power gets tricks_won += 1. If that player's played == 20 and some played == 40, that player also gets bonus += 10. trick += 1. Announce the trick winner."
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "Run the play, show and resolve steps again until trick == 3."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Scoring for each player: if tricks_won == bid then score += 30 + bonus; otherwise score -= 10 * |bid - tricks_won| and the bonus is lost. Announce all scores."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round == 10 the game ends; otherwise go back to the first round step."
    }
  ],
  "ending": {
    "condition": "round == 10 (checked after the round's scoring)",
    "rank_by": "you.score",
    "decided_by": "Each player's standing is their final score after round 10. The highest score wins, and players tied for the highest score share the result (the source calls this a draw)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, every player's score is 0 and round is 0."
    },
    {
      "id": "R2",
      "text": "When a round starts, round increases by 1, and every player's tricks_won is set to 0, bonus to 0 and hand to empty, while revealed is set to empty."
    },
    {
      "id": "R3",
      "text": "When a round starts, deck is reset to the 18 cards [1..12, 0, 0, 20, 30, 31, 40]."
    },
    {
      "id": "R4",
      "text": "When cards are dealt, each player receives exactly 3 random cards from deck into their private hand, and those cards are removed from deck."
    },
    {
      "id": "R5",
      "text": "When cards are revealed, 3 further random cards move from deck to the public revealed list, are out of play this round, and leave 3 hidden cards in deck with 4 players or 6 with 3 players."
    },
    {
      "id": "R6",
      "text": "When bidding, all players answer at the same time with exactly 0, 1, 2 or 3, and the answer is stored as bid."
    },
    {
      "id": "R7",
      "text": "When all bids are in, every player's bid is shown to everyone."
    },
    {
      "id": "R8",
      "text": "When a trick is played, every player at the same time chooses one card from their own hand, and that card is removed from hand and stored as played."
    },
    {
      "id": "R9",
      "text": "When all cards of a trick are chosen, every played card is shown to everyone together."
    },
    {
      "id": "R10",
      "text": "When the played cards include both the Mermaid (20) and the Skull King (40), the Mermaid's player wins the trick even if a Pirate (30 or 31) was played, and gains bonus +10."
    },
    {
      "id": "R11",
      "text": "When the played cards do not include both the Mermaid and the Skull King, the player with the highest played power wins the trick (for example 31 beats 30, and 1 beats an Escape at 0)."
    },
    {
      "id": "R12",
      "text": "When a player wins a trick, their tricks_won increases by 1."
    },
    {
      "id": "R13",
      "text": "When the round is played, exactly 3 tricks are played, so each player plays all 3 cards in hand."
    },
    {
      "id": "R14",
      "text": "When a player's tricks_won equals their bid after the third trick (including bid 0 with 0 tricks), their score increases by 30 + bonus (for example bid 1, won 1, bonus 10 gives +40)."
    },
    {
      "id": "R15",
      "text": "When a player's tricks_won differs from their bid after the third trick, their score decreases by 10 \u00d7 |bid \u2212 tricks_won| and the bonus is lost (for example bid 3, won 1 gives \u221220)."
    },
    {
      "id": "R16",
      "text": "When round equals 10 after scoring, the game ends; otherwise a new round starts."
    },
    {
      "id": "R17",
      "text": "When the game ends, the player with the highest score wins, and players tied at the highest score share the top place."
    }
  ],
  "offers": [
    {
      "question": "Bid",
      "who": "all players",
      "options": "0, 1, 2 or 3, for every seat in every round."
    },
    {
      "question": "Play a card",
      "who": "all players",
      "options": "Each seat is offered exactly the cards currently in its own hand: 3 cards in the first trick, the 2 remaining in the second, the 1 remaining in the third."
    }
  ],
  "choices": [
    {
      "what": "3 to 4 players, suggested 4",
      "why": "The designer suggests 4 and the source allows 3 to 4. The minimum is 3 because the rules need at least 3 players to guarantee a unique trick winner, given that only the two Escapes share a power. The maximum stays at 4 because 4 \u00d7 3 dealt cards plus 3 revealed cards leaves 3 hidden cards; larger tables would remove the hidden cards and break the source deck."
    },
    {
      "what": "Cards represented by their power numbers",
      "why": "Power is all the rules use. The two Escapes are both 0, and the labels are 0 Escape, 20 Mermaid, 30 Pirate A, 31 Pirate B, 40 Skull King."
    },
    {
      "what": "No talk step",
      "why": "The source states there is no discussion phase."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player counts the revealed cards and their own hand to judge which high cards are still out, bids accordingly, then reads the public bids and tricks so far to decide when to dump a winner or duck with a low card. They also hold the Mermaid back for a trick where the Skull King is likely to appear."
    },
    {
      "what": "Shuffling as random draws from the deck list",
      "why": "Drawing a random card from a freshly reset deck is equivalent to dealing from a shuffled deck."
    },
    {
      "what": "A table attribute winning_power and a trick counter",
      "why": "Used to resolve each trick by arithmetic and to repeat the trick steps exactly 3 times."
    },
    {
      "what": "played initial value -1",
      "why": "Marks 'no card played yet'. -1 is below every real power."
    }
  ],
  "simplifications": [
    {
      "what": "A tie for the highest score is a shared win rather than a draw",
      "why": "The engine ranks by one expression and players level at the top share the win, which corresponds to the source's draw."
    },
    {
      "what": "The three tricks use a repeat over the play, show and resolve steps",
      "why": "The engine runs a flat step list and repeats steps until a condition holds."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid, tricks_won; table: round, revealed.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
[
  {"name": "Game starts with every score 0 and round 0", "rule": "R1", "players": 4, "rounds": 0,
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
              "game": {"round": 0}}},

  {"name": "Round start increments round from a given value (trick outcomes random, only round asserted)", "rule": "R2", "players": 4, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"round": 4}},
   "expect": {"game": {"round": 5}}},

  {"name": "Fresh deck each round: round 1 reveals exactly 3 cards (which cards is random)", "rule": "R3", "players": 4, "rounds": 1, "seed": 2, "default": "first",
   "given": {"game": {"revealed": [], "deck": []}},
   "expect": {"game": {"round": 1}, "lens": {"game": {"revealed": 3}}}},

  {"name": "Deal gives 3 cards, so each seat is asked to play a card from its hand (cards random)", "rule": "R4", "players": 3, "rounds": 1, "seed": 3, "default": "first",
   "expect": {"game": {"round": 1}, "lens": {"game": {"revealed": 3}}}},

  {"name": "Reveal leaves exactly 3 public cards with 3 players (cards random)", "rule": "R5", "players": 3, "rounds": 1, "seed": 4, "default": "first",
   "expect": {"lens": {"game": {"revealed": 3}}}},

  {"name": "Reveal leaves exactly 3 public cards with 4 players (cards random)", "rule": "R5", "players": 4, "rounds": 1, "seed": 5, "default": "first",
   "expect": {"lens": {"game": {"revealed": 3}}}},

  {"name": "Bids are stored as answered and only 0 to 3 are offered", "rule": "R6", "players": 4, "rounds": 1, "seed": 6, "default": "first",
   "rules": [{"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 2, "answer": 2},
             {"seat": 4, "options_include": 1, "answer": 1}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 0}, "3": {"bid": 2}, "4": {"bid": 1}},
              "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 3}, {"seat": 4, "option": 0}, {"seat": 4, "option": 3}],
              "not_offered": [{"seat": 1, "option": 4}, {"seat": 2, "option": 4}]}},

  {"name": "Bids are public after the poll", "rule": "R7", "players": 3, "rounds": 1, "seed": 7, "default": "first",
   "rules": [{"seat": 1, "options_include": 1, "answer": 1},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 0}}}},

  {"name": "Playing cards over a round completes it (cards random, round asserted)", "rule": "R8", "players": 4, "rounds": 1, "seed": 8, "default": "last",
   "expect": {"game": {"round": 1}}},

  {"name": "All played cards shown; round completes (outcome random)", "rule": "R9", "players": 3, "rounds": 1, "seed": 9, "default": "first",
   "expect": {"game": {"round": 1}}},

  {"name": "Mermaid capture bonus cannot exceed the score lead; dominant seat still wins (deal random)", "rule": "R10", "players": 4, "seed": 10, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 200}, "3": {"score": 0}, "4": {"score": 0}}},
   "expect": {"winner": 2, "game": {"round": 10}}},

  {"name": "Highest power wins tricks; round completes (outcome random)", "rule": "R11", "players": 4, "rounds": 1, "seed": 11, "default": "last",
   "expect": {"game": {"round": 1}}},

  {"name": "Trick wins are counted each round (outcome random, round asserted)", "rule": "R12", "players": 3, "rounds": 1, "seed": 12, "default": "first",
   "expect": {"game": {"round": 1}}},

  {"name": "Three tricks per round then next round (two rounds played)", "rule": "R13", "players": 4, "rounds": 2, "seed": 13, "default": "first",
   "expect": {"game": {"round": 2}}},

  {"name": "Max gain per round is 40, so a 100-point lead in the last round decides the winner", "rule": "R14", "players": 3, "seed": 14, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 100}, "2": {"score": 0}, "3": {"score": 0}}},
   "expect": {"winner": 1, "game": {"round": 10}}},

  {"name": "Max loss per round is 30, so a seat 100 ahead stays ahead (deal random)", "rule": "R15", "players": 4, "seed": 15, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 100}, "4": {"score": 0}}},
   "rules": [{"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"winner": 3, "game": {"round": 10}}},

  {"name": "Game does not end before round 10", "rule": "R16", "players": 4, "rounds": 1, "seed": 16, "default": "first",
   "given": {"game": {"round": 5}},
   "expect": {"game": {"round": 6}}},

  {"name": "Game ends after round 10's scoring", "rule": "R16", "players": 3, "seed": 17, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 150}}},
   "expect": {"winner": 3, "game": {"round": 10}}},

  {"name": "Highest final score wins (lead too large for one random round)", "rule": "R17", "players": 4, "seed": 18, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 300}, "2": {"score": 50}, "3": {"score": 50}, "4": {"score": 50}}},
   "expect": {"winner": 1, "game": {"round": 10}}}
]

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 9: needs `rules` (what each seat answers, by option name); scenario 10: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 12: needs `rules` (what each seat answers, by option name); scenario 13: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 15: needs `rules` (what each seat answers, by option name); scenario 17: needs `rules` (what each seat answers, by option name); scenario 18: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
[
  {"name": "Game starts with every score 0 and round 0", "rule": "R1", "players": 4, "rounds": 0,
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
              "game": {"round": 0}}},

  {"name": "Round start increments round from a given value (trick outcomes random, only round asserted)", "rule": "R2", "players": 4, "rounds": 1, "seed": 1, "default": "first",
   "given": {"game": {"round": 4}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 5}}},

  {"name": "Fresh deck each round: round 1 reveals exactly 3 cards (which cards is random)", "rule": "R3", "players": 4, "rounds": 1, "seed": 2, "default": "first",
   "given": {"game": {"revealed": [], "deck": []}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"revealed": 3}}}},

  {"name": "Deal gives 3 cards, so the round plays through and 3 cards are revealed (cards random)", "rule": "R4", "players": 3, "rounds": 1, "seed": 3, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}, "lens": {"game": {"revealed": 3}}}},

  {"name": "Reveal leaves exactly 3 public cards with 3 players (cards random)", "rule": "R5", "players": 3, "rounds": 1, "seed": 4, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"lens": {"game": {"revealed": 3}}}},

  {"name": "Reveal leaves exactly 3 public cards with 4 players (cards random)", "rule": "R5", "players": 4, "rounds": 1, "seed": 5, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"lens": {"game": {"revealed": 3}}}},

  {"name": "Bids are stored as answered and only 0 to 3 are offered", "rule": "R6", "players": 4, "rounds": 1, "seed": 6, "default": "first",
   "rules": [{"seat": 1, "options_include": 3, "answer": 3},
             {"seat": 2, "options_include": 0, "answer": 0},
             {"seat": 3, "options_include": 2, "answer": 2},
             {"seat": 4, "options_include": 1, "answer": 1}],
   "expect": {"players": {"1": {"bid": 3}, "2": {"bid": 0}, "3": {"bid": 2}, "4": {"bid": 1}},
              "offered": [{"seat": 1, "option": 0}, {"seat": 1, "option": 3}, {"seat": 4, "option": 0}, {"seat": 4, "option": 3}],
              "not_offered": [{"seat": 1, "option": 4}, {"seat": 2, "option": 4}]}},

  {"name": "Bids are public after the poll", "rule": "R7", "players": 3, "rounds": 1, "seed": 7, "default": "first",
   "rules": [{"seat": 1, "options_include": 1, "answer": 1},
             {"seat": 2, "options_include": 2, "answer": 2},
             {"seat": 3, "options_include": 0, "answer": 0}],
   "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 2}, "3": {"bid": 0}}}},

  {"name": "Playing cards over a round completes it (cards random, round asserted)", "rule": "R8", "players": 4, "rounds": 1, "seed": 8, "default": "last",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}}},

  {"name": "All played cards shown; round completes (outcome random)", "rule": "R9", "players": 3, "rounds": 1, "seed": 9, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}}},

  {"name": "Mermaid capture bonus cannot exceed the score lead; dominant seat still wins (deal random)", "rule": "R10", "players": 4, "seed": 10, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 200}, "3": {"score": 0}, "4": {"score": 0}}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"winner": 2, "game": {"round": 10}}},

  {"name": "Highest power wins tricks; round completes (outcome random)", "rule": "R11", "players": 4, "rounds": 1, "seed": 11, "default": "last",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}}},

  {"name": "Trick wins are counted each round (outcome random, round asserted)", "rule": "R12", "players": 3, "rounds": 1, "seed": 12, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 1}}},

  {"name": "Three tricks per round then next round (two rounds played)", "rule": "R13", "players": 4, "rounds": 2, "seed": 13, "default": "first",
   "rules": [{"seat": 1, "options_include": 0, "answer": 0, "times": "all"}],
   "expect": {"game": {"round": 2}}},

  {"name": "Max gain per round is 40, so a 100-point lead in the last round decides the winner", "rule": "R14", "players": 3, "seed": 14, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 100}, "2": {"score": 0}, "3": {"score": 0}}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1, "game": {"round": 10}}},

  {"name": "Max loss per round is 30, so a seat 100 ahead stays ahead (deal random)", "rule": "R15", "players": 4, "seed": 15, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 100}, "4": {"score": 0}}},
   "rules": [{"seat": 3, "options_include": 3, "answer": 3}],
   "expect": {"winner": 3, "game": {"round": 10}}},

  {"name": "Game does not end before round 10", "rule": "R16", "players": 4, "rounds": 1, "seed": 16, "default": "first",
   "given": {"game": {"round": 5}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"game": {"round": 6}}},

  {"name": "Game ends after round 10's scoring", "rule": "R16", "players": 3, "seed": 17, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 150}}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"winner": 3, "game": {"round": 10}}},

  {"name": "Highest final score wins (lead too large for one random round)", "rule": "R17", "players": 4, "seed": 18, "default": "first",
   "given": {"game": {"round": 9}, "players": {"1": {"score": 300}, "2": {"score": 50}, "3": {"score": 50}, "4": {"score": 50}}},
   "rules": [{"seat": 1, "options_include": 0, "answer": 0}],
   "expect": {"winner": 1, "game": {"round": 10}}}
]
````
