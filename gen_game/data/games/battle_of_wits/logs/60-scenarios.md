# 60 scenarios

- time: 2026-10-07T19:07:00+00:00 (105.6s)  model: rl-muse-spark-1-2-playground
- system prompt: [system/428781a3-scenarios.md](system/428781a3-scenarios.md) (sha256 428781a34d8364c1)
- sent sha256 8143831f4794084a, reply sha256 c8883817ecfd54b9

## Sent

````
SPEC:
{
  "name": "Battle of Wits: High Affinity Duel",
  "summary": "Two players with hidden Crimson/Azure types alternate as Poisoner and Chooser over 12 simultaneous Left/Right picks, scoring 3 on their High side and 1 on their Low side.",
  "players": {
    "min": 2,
    "max": 2
  },
  "parameters": {
    "num_rounds": 12,
    "high_payoff": 3,
    "low_payoff": 1,
    "type_probability": 0.5
  },
  "attributes": {
    "player": [
      {
        "key": "player_type",
        "type": "text",
        "visible": "none",
        "initial": null,
        "meaning": "private type Crimson (High=Left) or Azure (High=Right) assigned independently with p=0.5",
        "observable": false
      },
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "total points scored across rounds",
        "observable": true
      },
      {
        "key": "current_choice",
        "type": "text",
        "visible": "none",
        "initial": null,
        "meaning": "Left or Right chosen this round (Poisoner's poisoned goblet if player is Poisoner, Chooser's drink if player is Chooser)",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number 1-12",
        "observable": false
      }
    ]
  },
  "setup": [
    "Engine assigns each player a private type independently: Crimson (High=Left) or Azure (High=Right) with probability 0.5 each",
    "Show each player only own type via private channel",
    "Set every player's score to 0 and game round_number to 0",
    "Roles are fixed by round parity: odd rounds Player 1 is Poisoner and Player 2 is Chooser, even rounds Player 2 is Poisoner and Player 1 is Chooser"
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "increment game round_number by 1"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce game round_number and who is Poisoner and who is Chooser this round (odd: seat 1 Poisoner / seat 2 Chooser, even: seat 2 Poisoner / seat 1 Chooser)"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "options": [
          "Left",
          "Right"
        ]
      },
      "effect": "each player's current_choice set to chosen Left or Right simultaneously; Poisoner's choice is poisoned goblet, Chooser's choice is goblet to drink, hidden until reveal"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "reveal both players' current_choice to all players"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd (seat 1 Poisoner) and seat 1 current_choice == seat 2 current_choice and seat 1 player_type == Crimson and seat 1 current_choice == Left then adjust seat 1 score by 3 (match on Poisoner's High)",
      "when": "game.round_number % 2 == 1 and seat1.current_choice == seat2.current_choice and seat1.player_type == \"Crimson\" and seat1.current_choice == \"Left\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd and seat 1 current_choice == seat 2 current_choice and seat 1 player_type == Azure and seat 1 current_choice == Right then adjust seat 1 score by 3 (match on Poisoner's High)",
      "when": "game.round_number % 2 == 1 and seat1.current_choice == seat2.current_choice and seat1.player_type == \"Azure\" and seat1.current_choice == \"Right\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd and seat 1 current_choice == seat 2 current_choice and not High match then adjust seat 1 score by 1 (match on Poisoner's Low)",
      "when": "game.round_number % 2 == 1 and seat1.current_choice == seat2.current_choice and ((seat1.player_type == \"Crimson\" and seat1.current_choice == \"Right\") or (seat1.player_type == \"Azure\" and seat1.current_choice == \"Left\"))"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even (seat 2 Poisoner) and seat 1 current_choice == seat 2 current_choice and seat 2 player_type == Crimson and seat 2 current_choice == Left then adjust seat 2 score by 3",
      "when": "game.round_number % 2 == 0 and seat1.current_choice == seat2.current_choice and seat2.player_type == \"Crimson\" and seat2.current_choice == \"Left\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even and seat 1 current_choice == seat 2 current_choice and seat 2 player_type == Azure and seat 2 current_choice == Right then adjust seat 2 score by 3",
      "when": "game.round_number % 2 == 0 and seat1.current_choice == seat2.current_choice and seat2.player_type == \"Azure\" and seat2.current_choice == \"Right\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even and seat 1 current_choice == seat 2 current_choice and not High match then adjust seat 2 score by 1",
      "when": "game.round_number % 2 == 0 and seat1.current_choice == seat2.current_choice and ((seat2.player_type == \"Crimson\" and seat2.current_choice == \"Right\") or (seat2.player_type == \"Azure\" and seat2.current_choice == \"Left\"))"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd (seat 2 Chooser) and seat 1 current_choice != seat 2 current_choice and seat 2 player_type == Azure and seat 2 current_choice == Right then adjust seat 2 score by 3 (mismatch, Chooser High)",
      "when": "game.round_number % 2 == 1 and seat1.current_choice != seat2.current_choice and seat2.player_type == \"Azure\" and seat2.current_choice == \"Right\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd and seat 1 current_choice != seat 2 current_choice and seat 2 player_type == Crimson and seat 2 current_choice == Left then adjust seat 2 score by 3",
      "when": "game.round_number % 2 == 1 and seat1.current_choice != seat2.current_choice and seat2.player_type == \"Crimson\" and seat2.current_choice == \"Left\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is odd and seat 1 current_choice != seat 2 current_choice and not Chooser High then adjust seat 2 score by 1 (mismatch, Chooser Low)",
      "when": "game.round_number % 2 == 1 and seat1.current_choice != seat2.current_choice and ((seat2.player_type == \"Crimson\" and seat2.current_choice == \"Right\") or (seat2.player_type == \"Azure\" and seat2.current_choice == \"Left\"))"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even (seat 1 Chooser) and seat 1 current_choice != seat 2 current_choice and seat 1 player_type == Crimson and seat 1 current_choice == Left then adjust seat 1 score by 3",
      "when": "game.round_number % 2 == 0 and seat1.current_choice != seat2.current_choice and seat1.player_type == \"Crimson\" and seat1.current_choice == \"Left\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even and seat 1 current_choice != seat 2 current_choice and seat 1 player_type == Azure and seat 1 current_choice == Right then adjust seat 1 score by 3",
      "when": "game.round_number % 2 == 0 and seat1.current_choice != seat2.current_choice and seat1.player_type == \"Azure\" and seat1.current_choice == \"Right\""
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "if game round_number is even and seat 1 current_choice != seat 2 current_choice and not Chooser High then adjust seat 1 score by 1",
      "when": "game.round_number % 2 == 0 and seat1.current_choice != seat2.current_choice and ((seat1.player_type == \"Crimson\" and seat1.current_choice == \"Right\") or (seat1.player_type == \"Azure\" and seat1.current_choice == \"Left\"))"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announce both current_choice values, whether choices matched or mismatched, who scored and how many points (3 or 1), types stay hidden"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "continue if game round_number < 12, otherwise end game"
    }
  ],
  "ending": {
    "condition": "game.round_number >= 12",
    "results": [
      "seat 1",
      "seat 2",
      "draw"
    ],
    "decided_by": "highest total score wins; if seat 1 score > seat 2 score result is seat 1, if seat 2 score > seat 1 score result is seat 2, otherwise draw"
  },
  "choices": [],
  "simplifications": [
    {
      "what": "Payoff matrix implemented as 12 conditional single-step updates with when conditions instead of lookup operation",
      "why": "Engine has no payoff_matrix lookup; workaround requires arithmetic conditional updates (about 13 steps for 9 cells) - here 8 scoring cases split by parity"
    },
    {
      "what": "Simultaneous hidden choices implemented via poll storing each player's current_choice and comparing equality to detect match/mismatch, rather than a Poisoner-only then Chooser-only step",
      "why": "Engine poll addresses all players at once; using poll guarantees simultaneity with no player hearing earlier answer, as required; match detection is equivalent to poisoner_choice == chooser_choice"
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score; table: none.

EARLIER TESTS FOR THIS SPEC WERE FOUND WRONG. What to do differently:
Rewrite tests to not assert exact numeric scores that depend on hidden types. Keep only the invariant assertions (e.g., shutout 0-24, draw totals) or fix the expected values by computing them for the seeded types correctly, and assert only on result (seat 1/seat 2/draw) and on score totals that are invariant to High side; do not predict chance-dependent per-player scores.
````

## Reply

````
[
  {
    "name": "P1 shutout invariant 24-0 regardless of types - balanced Left/Right",
    "players": 2,
    "seed": 1,
    "moves": {
      "1": ["Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right"],
      "2": ["Left", "Left", "Left", "Left", "Left", "Left", "Left", "Left", "Left", "Left", "Left", "Left"]
    },
    "expect": {
      "result": "seat 1",
      "players": {
        "1": {"score": 24},
        "2": {"score": 0}
      }
    }
  },
  {
    "name": "P2 shutout invariant 0-24 regardless of types - balanced Left/Right",
    "players": 2,
    "seed": 2,
    "moves": {
      "1": ["Right", "Right", "Right", "Right", "Right", "Right", "Right", "Right", "Right", "Right", "Right", "Right"],
      "2": ["Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right", "Left", "Right"]
    },
    "expect": {
      "result": "seat 2",
      "players": {
        "1": {"score": 0},
        "2": {"score": 24}
      }
    }
  },
  {
    "name": "Draw invariant 12-12 via Poisoner scoring (all matches) balanced",
    "players": 2,
    "seed": 3,
    "moves": {
      "1": ["Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left"],
      "2": ["Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left"]
    },
    "expect": {
      "result": "draw",
      "players": {
        "1": {"score": 12},
        "2": {"score": 12}
      }
    }
  },
  {
    "name": "Draw invariant 12-12 via Chooser scoring (all mismatches) balanced",
    "players": 2,
    "seed": 4,
    "moves": {
      "1": ["Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left"],
      "2": ["Right", "Left", "Left", "Right", "Right", "Left", "Left", "Right", "Right", "Left", "Left", "Right"]
    },
    "expect": {
      "result": "draw",
      "players": {
        "1": {"score": 12},
        "2": {"score": 12}
      }
    }
  }
]
````
