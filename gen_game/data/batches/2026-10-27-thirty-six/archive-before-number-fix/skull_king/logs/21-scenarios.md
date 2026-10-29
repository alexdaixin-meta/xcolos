# 21 scenarios

- time: 2026-10-27T18:13:57+00:00 (44.1s)  model: claude-opus-5-5
- system prompt: [system/8e9a17ed-scenarios.md](system/8e9a17ed-scenarios.md) (sha256 8e9a17ed7c2a08b3)
- sent sha256 3e54f6a068851dc5, reply sha256 223a3d777630d300

## Sent

````
SPEC:
{
  "name": "Skull King: Three-Card Bids",
  "summary": "Over 8 rounds, players are dealt 3 cards from an 18-card deck, bid at the same time on how many of 3 simultaneous tricks they will win, and score for bidding exactly right, with bonuses when the Skull King captures Pirates or the Mermaid captures the Skull King.",
  "players": {
    "min": 3,
    "max": 5,
    "suggested": 4
  },
  "parameters": {
    "hand_size": 3,
    "tricks_per_round": 3,
    "rounds": 8,
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
    "exact_bid_points_per_trick": 20,
    "missed_bid_penalty_per_trick": 10,
    "zero_bid_success_points": 20,
    "zero_bid_failure_penalty": 20,
    "skull_king_bonus_per_pirate": 30,
    "mermaid_captures_skull_king_bonus": 50
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The player's total score over all rounds.",
        "observable": true
      },
      {
        "key": "hand",
        "type": "list",
        "visible": "ally",
        "initial": [],
        "meaning": "The powers of the cards the player holds this round. Only the owner sees them.",
        "observable": false
      },
      {
        "key": "bid",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of tricks the player bid this round. It is collected by a simultaneous poll, so nobody sees it until all bids are in.",
        "observable": true
      },
      {
        "key": "tricks_won",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of tricks the player has won this round.",
        "observable": true
      },
      {
        "key": "bonus",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The capture bonus the player has earned this round. It is scored only on an exact non-zero bid.",
        "observable": false
      },
      {
        "key": "played",
        "type": "number",
        "visible": "public",
        "initial": -1,
        "meaning": "The power of the card the player played in the current trick. It is revealed after everyone has played.",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The round counter.",
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
        "meaning": "The undealt cards, listed by power. They are never revealed.",
        "observable": false
      },
      {
        "key": "trick",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of tricks played so far this round.",
        "observable": false
      },
      {
        "key": "mermaid_played",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the Mermaid (20) was played in the current trick.",
        "observable": false
      },
      {
        "key": "skull_king_played",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "Whether the Skull King (40) was played in the current trick.",
        "observable": false
      },
      {
        "key": "pirates_in_trick",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The number of Pirates (30 or 31) played in the current trick.",
        "observable": false
      },
      {
        "key": "max_power",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "The highest power played in the current trick.",
        "observable": false
      }
    ]
  },
  "setup": [
    "Every player's score is set to 0.",
    "The round counter is set to 0.",
    "The deck list holds the 18 card powers: 1 to 12, 0, 0, 20, 30, 31 and 40."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. For every player: tricks_won = 0, bonus = 0, hand = [], played = -1. Table: trick = 0."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "deck = [1,2,3,4,5,6,7,8,9,10,11,12,0,0,20,30,31,40]. All 18 cards are gathered; shuffling happens through the random draws."
    },
    {
      "action": "update",
      "who": "each player in turn",
      "answer": null,
      "effect": "Deal hand_size (3) cards to each player, one at a time in seat order. Each card is a random draw: it is removed from deck and appended to that player's hand. The remaining cards stay in deck, hidden."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own hand."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "a whole number from bid_min (0) to bid_max (3)",
      "effect": "Each player's answer is stored as that player's bid. No player sees another's bid until all are in."
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
      "answer": "one card (power) from the player's own current hand",
      "effect": "played = the chosen power. That card is removed from the player's hand."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal every player's played card to everyone."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Table: mermaid_played = (some player's played == 20); skull_king_played = (some player's played == 40); pirates_in_trick = count of players whose played is 30 or 31; max_power = the maximum of played over all players."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "The trick winner is: if mermaid_played and skull_king_played, the player whose played == 20; otherwise the player whose played == max_power. For the winner: tricks_won += 1. If the winner's played == 40: bonus += 30 * pirates_in_trick. If the winner's played == 20 and skull_king_played: bonus += 50. Then trick += 1."
    },
    {
      "action": "repeat",
      "who": "all players",
      "answer": null,
      "effect": "Run the play, reveal, resolve and award steps again until trick == tricks_per_round (3)."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each player: if bid >= 1 and tricks_won == bid, score += 20 * bid + bonus; if bid >= 1 and tricks_won != bid, score -= 10 * |tricks_won - bid|; if bid == 0 and tricks_won == 0, score += 20; if bid == 0 and tricks_won >= 1, score -= 20. Announce the round's results."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round == rounds (8), end the game; otherwise start the next round."
    }
  ],
  "ending": {
    "condition": "round == 8",
    "rank_by": "you.score",
    "decided_by": "After round 8, each player's standing is their total score. The highest score wins, and players tied for the highest share the win (a draw among them)."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then every player's score is 0 and the round counter is 0."
    },
    {
      "id": "R2",
      "text": "When a round starts, then round increases by 1, and every player's tricks_won is 0, bonus is 0 and hand is empty."
    },
    {
      "id": "R3",
      "text": "When a round starts, then the deck holds all 18 cards: powers 1 to 12, two 0s (Escapes), 20 (Mermaid), 30 (Pirate A), 31 (Pirate B) and 40 (Skull King)."
    },
    {
      "id": "R4",
      "text": "When cards are dealt, then each player receives exactly 3 random cards from the deck into their hand, and those cards are removed from the deck."
    },
    {
      "id": "R5",
      "text": "When cards are dealt, then a player's hand is visible only to that player, and the undealt deck is visible to no one."
    },
    {
      "id": "R6",
      "text": "When bidding, then every player at the same time chooses a whole number from 0 to 3, stored as bid, and no player sees another's bid before all are in."
    },
    {
      "id": "R7",
      "text": "When all bids are in, then every bid is announced to everyone."
    },
    {
      "id": "R8",
      "text": "When a trick is played, then every player at the same time chooses one card from their own current hand, that card is removed from the hand, and all played cards are revealed."
    },
    {
      "id": "R9",
      "text": "When both the Mermaid (20) and the Skull King (40) are played in a trick, then the Mermaid's player wins the trick."
    },
    {
      "id": "R10",
      "text": "When the Mermaid and the Skull King are not both played in a trick, then the player of the highest-power card wins it (for example, 31 beats 30, and 12 beats 0)."
    },
    {
      "id": "R11",
      "text": "When a player wins a trick, then their tricks_won increases by 1."
    },
    {
      "id": "R12",
      "text": "When the Skull King wins a trick, then its player's bonus increases by 30 for each Pirate (30 or 31) in that trick: 30 for one Pirate, 60 for both."
    },
    {
      "id": "R13",
      "text": "When the Mermaid wins a trick in which the Skull King was played, then the Mermaid's player's bonus increases by 50."
    },
    {
      "id": "R14",
      "text": "When 3 tricks have been played in a round, then the round's scoring happens."
    },
    {
      "id": "R15",
      "text": "When a player bid 1, 2 or 3 and tricks_won equals the bid, then their score increases by 20 times the bid plus their bonus (for example, a bid of 2 with 2 tricks and a bonus of 30 gains 70)."
    },
    {
      "id": "R16",
      "text": "When a player bid 1, 2 or 3 and tricks_won differs from the bid, then their score decreases by 10 times the difference, and the bonus is not scored (for example, a bid of 3 with 1 trick loses 20)."
    },
    {
      "id": "R17",
      "text": "When a player bid 0 and won 0 tricks, then their score increases by 20."
    },
    {
      "id": "R18",
      "text": "When a player bid 0 and won 1 or more tricks, then their score decreases by 20."
    },
    {
      "id": "R19",
      "text": "When the round counter reaches 8 after scoring, then the game ends."
    },
    {
      "id": "R20",
      "text": "When the game ends, then the player with the highest score wins, and players tied for the highest share the win."
    }
  ],
  "offers": [
    {
      "question": "Bid: how many tricks will you win this round?",
      "who": "all players, at once",
      "options": "every player: 0, 1, 2, 3"
    },
    {
      "question": "Play a card for this trick",
      "who": "all players, at once",
      "options": "each player: exactly the cards still in their own hand (3 choices in trick 1, 2 in trick 2, 1 in trick 3); two Escapes in a hand appear as two options of power 0"
    }
  ],
  "choices": [
    {
      "what": "3 to 5 players, 4 suggested",
      "why": "The designer's table size of 4 is kept. The minimum is 3 because, with fewer, one player could hold both Escapes and a trick could end in a tie, and bids would have no rivals to read. The maximum is 5 because 5 x 3 = 15 cards fit an 18-card deck with some cards left unseen, and more seats would leave no uncertainty about the undealt cards."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player bids from the strength of their hand and from how many high cards are still unseen. After the announced bids, they time their strong cards against the tricks rivals need, and they spend Escapes to avoid unwanted wins. Simultaneous play rewards predicting when others will commit their Pirates and the Skull King."
    },
    {
      "what": "No talk step",
      "why": "The source states there is no discussion phase."
    },
    {
      "what": "Table attributes mermaid_played, skull_king_played, pirates_in_trick, max_power and trick",
      "why": "The engine cannot compare one player's attribute against another's directly, so the trick resolution is computed through table attributes. The three tricks are counted with trick."
    },
    {
      "what": "The played attribute resets to -1 each round",
      "why": "This is a sentinel meaning no card played yet, so it cannot be confused with an Escape (power 0)."
    }
  ],
  "simplifications": [
    {
      "what": "Shuffling is modelled as random draws from the freshly refilled deck list",
      "why": "The engine draws at random from a list, which is equivalent to shuffling and dealing."
    },
    {
      "what": "The three tricks use a repeat over the play, reveal, resolve and award steps, counted by trick",
      "why": "The engine runs a flat step list, so repetition happens through repeat with a counter."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, bid, tricks_won; table: round.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {
    "name": "R1: at game start every score is 0, the round counter is 0 and the deck holds 18 cards",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"round": 0},
      "lens": {"game": {"deck": 18}}
    }
  },
  {
    "name": "R2: a new round increases the round counter by 1 (from 3 to 4)",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"round": 3}},
    "expect": {"game": {"round": 4}}
  },
  {
    "name": "R3: the deck is refilled to 18 at round start even if it was empty, so after dealing 4x3 it holds 6",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"deck": []}},
    "expect": {"lens": {"game": {"deck": 6}}, "game": {"round": 1}}
  },
  {
    "name": "R4: 5 players are dealt 3 cards each from the deck, so 3 cards stay undealt and all hands are played out",
    "rule": "R4",
    "players": 5,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "expect": {
      "lens": {
        "game": {"deck": 3},
        "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}, "5": {"hand": 0}}
      }
    }
  },
  {
    "name": "R5: dealt cards leave the hidden deck (3 players, 9 cards remain undealt)",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "expect": {"lens": {"game": {"deck": 9}}}
  },
  {
    "name": "R6: every seat is offered bids 0 to 3 and each bid is stored as chosen",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 2, "times": 1},
      {"seat": 3, "options_include": 3, "times": 1}
    ],
    "expect": {
      "players": {"1": {"bid": 0}, "2": {"bid": 2}, "3": {"bid": 3}},
      "offered": [
        {"seat": 1, "option": 3},
        {"seat": 2, "option": 0},
        {"seat": 3, "option": 1},
        {"seat": 1, "option": 2}
      ]
    }
  },
  {
    "name": "R7: all four bids are recorded publicly after bidding",
    "rule": "R7",
    "players": 4,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 3, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 0}, "4": {"bid": 3}}}
  },
  {
    "name": "R8: each trick removes the played card from the hand, so after 3 tricks every hand is empty",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "expect": {"lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}
  },
  {
    "name": "R9: seats lead the Mermaid and the Skull King when held (outcome depends on the deal, so only the bids and round are asserted)",
    "rule": "R9",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 20, "times": 1},
      {"seat": 2, "options_include": 20, "times": 1},
      {"seat": 3, "options_include": 20, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 1}}, "game": {"round": 1}}
  },
  {
    "name": "R10: seats play their Pirates first when held (the deal decides the winner, so only the bids and round are asserted)",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 31, "times": 1},
      {"seat": 2, "options_include": 30, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 0}, "3": {"bid": 1}}, "game": {"round": 1}}
  },
  {
    "name": "R11: three tricks are played and awarded in a round (the deal decides who wins them, so only the round and empty hands are asserted)",
    "rule": "R11",
    "players": 4,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "expect": {
      "game": {"round": 1},
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}}
    }
  },
  {
    "name": "R12: seats commit the Skull King and Pirates together when held (the deal decides the capture, so only the bids are asserted)",
    "rule": "R12",
    "players": 5,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 4, "options_include": 1, "times": 1},
      {"seat": 5, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1},
      {"seat": 4, "options_include": 40, "times": 1},
      {"seat": 5, "options_include": 40, "times": 1},
      {"seat": 1, "options_include": 30, "times": 1},
      {"seat": 2, "options_include": 30, "times": 1},
      {"seat": 3, "options_include": 30, "times": 1},
      {"seat": 4, "options_include": 30, "times": 1},
      {"seat": 5, "options_include": 30, "times": 1},
      {"seat": 1, "options_include": 31, "times": 1},
      {"seat": 2, "options_include": 31, "times": 1},
      {"seat": 3, "options_include": 31, "times": 1},
      {"seat": 4, "options_include": 31, "times": 1},
      {"seat": 5, "options_include": 31, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 1}, "4": {"bid": 1}, "5": {"bid": 1}}}
  },
  {
    "name": "R13: seats play the Mermaid and the Skull King first when held (the deal decides the capture, so only the bids and round are asserted)",
    "rule": "R13",
    "players": 5,
    "seed": 13,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 2, "times": 1},
      {"seat": 3, "options_include": 2, "times": 1},
      {"seat": 4, "options_include": 2, "times": 1},
      {"seat": 5, "options_include": 2, "times": 1},
      {"seat": 1, "options_include": 20, "times": 1},
      {"seat": 2, "options_include": 20, "times": 1},
      {"seat": 3, "options_include": 20, "times": 1},
      {"seat": 4, "options_include": 20, "times": 1},
      {"seat": 5, "options_include": 20, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1},
      {"seat": 4, "options_include": 40, "times": 1},
      {"seat": 5, "options_include": 40, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 2}, "3": {"bid": 2}, "4": {"bid": 2}, "5": {"bid": 2}}, "game": {"round": 1}}
  },
  {
    "name": "R14: after 3 tricks the round is complete and scored, with every hand empty",
    "rule": "R14",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "expect": {
      "game": {"round": 1},
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}
    }
  },
  {
    "name": "R15: bid-1 scoring stays within its bounds in the final round (seat 1 at 41 can drop at most 20, while bid-0 rivals at 0 reach at most 20), so seat 1 wins whatever the deal",
    "rule": "R15",
    "players": 3,
    "seed": 15,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 41}, "2": {"score": 0}, "3": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}, "players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 0}}}
  },
  {
    "name": "R16: a missed bid of 3 costs at most 30 and the bonus is never subtracted, so seat 1 at 51 beats bid-0 rivals at 0 whatever the deal",
    "rule": "R16",
    "players": 3,
    "seed": 16,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 51}, "2": {"score": 0}, "3": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R17: a bid of 0 scores +20 or -20, so bid-0 rivals at 0 end at most 20 and seat 1 at 41 with bid 0 wins whatever the deal",
    "rule": "R17",
    "players": 4,
    "seed": 17,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 41}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}, "players": {"1": {"bid": 0}, "2": {"bid": 0}, "3": {"bid": 0}, "4": {"bid": 0}}}
  },
  {
    "name": "R18: a failed bid of 0 loses exactly 20 at most, so seat 1 at 21 with bid 0 stays above the -20 floor of bid-0 rivals at -41 whatever the deal",
    "rule": "R18",
    "players": 3,
    "seed": 18,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 21}, "2": {"score": -41}, "3": {"score": -41}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R19: the game ends after round 8 is scored, starting from round 7",
    "rule": "R19",
    "players": 3,
    "seed": 19,
    "default": "decline",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 500}, "2": {"score": 0}, "3": {"score": 0}}},
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R20: the highest total score wins (seat 2 leads by far more than one round can change)",
    "rule": "R20",
    "players": 4,
    "seed": 20,
    "default": "decline",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 100}, "2": {"score": 600}, "3": {"score": 300}, "4": {"score": 0}}},
    "expect": {"winner": 2, "game": {"round": 8}}
  }
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 3: needs `rules` (what each seat answers, by option name); scenario 4: needs `rules` (what each seat answers, by option name); scenario 5: needs `rules` (what each seat answers, by option name); scenario 8: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 14: needs `rules` (what each seat answers, by option name); scenario 19: needs `rules` (what each seat answers, by option name); scenario 20: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {
    "name": "R1: at game start every score is 0, the round counter is 0 and the deck holds 18 cards",
    "rule": "R1",
    "players": 4,
    "seed": 1,
    "rounds": 0,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1}
    ],
    "expect": {
      "players": {"1": {"score": 0}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}},
      "game": {"round": 0},
      "lens": {"game": {"deck": 18}}
    }
  },
  {
    "name": "R2: a new round increases the round counter by 1 (from 3 to 4)",
    "rule": "R2",
    "players": 3,
    "seed": 2,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"round": 3}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"game": {"round": 4}}
  },
  {
    "name": "R3: the deck is refilled to 18 at round start even if it was empty, so after dealing 4x3 it holds 6",
    "rule": "R3",
    "players": 4,
    "seed": 3,
    "rounds": 1,
    "default": "decline",
    "given": {"game": {"deck": []}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 0, "times": 1}
    ],
    "expect": {"lens": {"game": {"deck": 6}}, "game": {"round": 1}}
  },
  {
    "name": "R4: 5 players are dealt 3 cards each from the deck, so 3 cards stay undealt and all hands are played out",
    "rule": "R4",
    "players": 5,
    "seed": 4,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 0, "times": 1},
      {"seat": 5, "options_include": 0, "times": 1}
    ],
    "expect": {
      "lens": {
        "game": {"deck": 3},
        "players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}, "5": {"hand": 0}}
      }
    }
  },
  {
    "name": "R5: dealt cards leave the hidden deck (3 players, 9 cards remain undealt)",
    "rule": "R5",
    "players": 3,
    "seed": 5,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"lens": {"game": {"deck": 9}}}
  },
  {
    "name": "R6: every seat is offered bids 0 to 3 and each bid is stored as chosen",
    "rule": "R6",
    "players": 3,
    "seed": 6,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 2, "times": 1},
      {"seat": 3, "options_include": 3, "times": 1}
    ],
    "expect": {
      "players": {"1": {"bid": 0}, "2": {"bid": 2}, "3": {"bid": 3}},
      "offered": [
        {"seat": 1, "option": 3},
        {"seat": 2, "option": 0},
        {"seat": 3, "option": 1},
        {"seat": 1, "option": 2}
      ]
    }
  },
  {
    "name": "R7: all four bids are recorded publicly after bidding",
    "rule": "R7",
    "players": 4,
    "seed": 7,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 3, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 0}, "4": {"bid": 3}}}
  },
  {
    "name": "R8: each trick removes the played card from the hand, so after 3 tricks every hand is empty",
    "rule": "R8",
    "players": 3,
    "seed": 8,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1}
    ],
    "expect": {"lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}}
  },
  {
    "name": "R9: seats lead the Mermaid and the Skull King when held (outcome depends on the deal, so only the bids and round are asserted)",
    "rule": "R9",
    "players": 3,
    "seed": 9,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 20, "times": 1},
      {"seat": 2, "options_include": 20, "times": 1},
      {"seat": 3, "options_include": 20, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 1}}, "game": {"round": 1}}
  },
  {
    "name": "R10: seats play their Pirates first when held (the deal decides the winner, so only the bids and round are asserted)",
    "rule": "R10",
    "players": 3,
    "seed": 10,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 31, "times": 1},
      {"seat": 2, "options_include": 30, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 0}, "3": {"bid": 1}}, "game": {"round": 1}}
  },
  {
    "name": "R11: three tricks are played and awarded in a round (the deal decides who wins them, so only the round and empty hands are asserted)",
    "rule": "R11",
    "players": 4,
    "seed": 11,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 4, "options_include": 1, "times": 1}
    ],
    "expect": {
      "game": {"round": 1},
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}, "4": {"hand": 0}}}
    }
  },
  {
    "name": "R12: seats commit the Skull King and Pirates together when held (the deal decides the capture, so only the bids are asserted)",
    "rule": "R12",
    "players": 5,
    "seed": 12,
    "rounds": 1,
    "default": "first",
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 1, "times": 1},
      {"seat": 3, "options_include": 1, "times": 1},
      {"seat": 4, "options_include": 1, "times": 1},
      {"seat": 5, "options_include": 1, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1},
      {"seat": 4, "options_include": 40, "times": 1},
      {"seat": 5, "options_include": 40, "times": 1},
      {"seat": 1, "options_include": 30, "times": 1},
      {"seat": 2, "options_include": 30, "times": 1},
      {"seat": 3, "options_include": 30, "times": 1},
      {"seat": 4, "options_include": 30, "times": 1},
      {"seat": 5, "options_include": 30, "times": 1},
      {"seat": 1, "options_include": 31, "times": 1},
      {"seat": 2, "options_include": 31, "times": 1},
      {"seat": 3, "options_include": 31, "times": 1},
      {"seat": 4, "options_include": 31, "times": 1},
      {"seat": 5, "options_include": 31, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 1}, "2": {"bid": 1}, "3": {"bid": 1}, "4": {"bid": 1}, "5": {"bid": 1}}}
  },
  {
    "name": "R13: seats play the Mermaid and the Skull King first when held (the deal decides the capture, so only the bids and round are asserted)",
    "rule": "R13",
    "players": 5,
    "seed": 13,
    "rounds": 1,
    "default": "last",
    "rules": [
      {"seat": 1, "options_include": 2, "times": 1},
      {"seat": 2, "options_include": 2, "times": 1},
      {"seat": 3, "options_include": 2, "times": 1},
      {"seat": 4, "options_include": 2, "times": 1},
      {"seat": 5, "options_include": 2, "times": 1},
      {"seat": 1, "options_include": 20, "times": 1},
      {"seat": 2, "options_include": 20, "times": 1},
      {"seat": 3, "options_include": 20, "times": 1},
      {"seat": 4, "options_include": 20, "times": 1},
      {"seat": 5, "options_include": 20, "times": 1},
      {"seat": 1, "options_include": 40, "times": 1},
      {"seat": 2, "options_include": 40, "times": 1},
      {"seat": 3, "options_include": 40, "times": 1},
      {"seat": 4, "options_include": 40, "times": 1},
      {"seat": 5, "options_include": 40, "times": 1}
    ],
    "expect": {"players": {"1": {"bid": 2}, "2": {"bid": 2}, "3": {"bid": 2}, "4": {"bid": 2}, "5": {"bid": 2}}, "game": {"round": 1}}
  },
  {
    "name": "R14: after 3 tricks the round is complete and scored, with every hand empty",
    "rule": "R14",
    "players": 3,
    "seed": 14,
    "rounds": 1,
    "default": "decline",
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {
      "game": {"round": 1},
      "lens": {"players": {"1": {"hand": 0}, "2": {"hand": 0}, "3": {"hand": 0}}}
    }
  },
  {
    "name": "R15: bid-1 scoring stays within its bounds in the final round (seat 1 at 41 can drop at most 20, while bid-0 rivals at 0 reach at most 20), so seat 1 wins whatever the deal",
    "rule": "R15",
    "players": 3,
    "seed": 15,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 41}, "2": {"score": 0}, "3": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 1, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}, "players": {"1": {"bid": 1}, "2": {"bid": 0}, "3": {"bid": 0}}}
  },
  {
    "name": "R16: a missed bid of 3 costs at most 30 and the bonus is never subtracted, so seat 1 at 51 beats bid-0 rivals at 0 whatever the deal",
    "rule": "R16",
    "players": 3,
    "seed": 16,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 51}, "2": {"score": 0}, "3": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 3, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R17: a bid of 0 scores +20 or -20, so bid-0 rivals at 0 end at most 20 and seat 1 at 41 with bid 0 wins whatever the deal",
    "rule": "R17",
    "players": 4,
    "seed": 17,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 41}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}, "players": {"1": {"bid": 0}, "2": {"bid": 0}, "3": {"bid": 0}, "4": {"bid": 0}}}
  },
  {
    "name": "R18: a failed bid of 0 loses exactly 20 at most, so seat 1 at 21 with bid 0 stays above the -20 floor of bid-0 rivals at -41 whatever the deal",
    "rule": "R18",
    "players": 3,
    "seed": 18,
    "default": "first",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 21}, "2": {"score": -41}, "3": {"score": -41}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R19: the game ends after round 8 is scored, starting from round 7",
    "rule": "R19",
    "players": 3,
    "seed": 19,
    "default": "decline",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 500}, "2": {"score": 0}, "3": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 1, "game": {"round": 8}}
  },
  {
    "name": "R20: the highest total score wins (seat 2 leads by far more than one round can change)",
    "rule": "R20",
    "players": 4,
    "seed": 20,
    "default": "decline",
    "given": {"game": {"round": 7}, "players": {"1": {"score": 100}, "2": {"score": 600}, "3": {"score": 300}, "4": {"score": 0}}},
    "rules": [
      {"seat": 1, "options_include": 0, "times": 1},
      {"seat": 2, "options_include": 0, "times": 1},
      {"seat": 3, "options_include": 0, "times": 1},
      {"seat": 4, "options_include": 0, "times": 1}
    ],
    "expect": {"winner": 2, "game": {"round": 8}}
  }
]
```
````
