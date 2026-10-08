# 04 scenarios

- time: 2026-10-08T17:48:45+00:00 (98.3s)  model: rl-muse-spark-1-2-playground
- system prompt: [system/428781a3-scenarios.md](system/428781a3-scenarios.md) (sha256 428781a34d8364c1)
- sent sha256 1336321e8cd872ae, reply sha256 cde069791e3e95ae

## Sent

````
SPEC:
{
  "name": "Assurance Threshold - Three Hunters",
  "summary": "Three hunters with hidden sheltered/exposed types simultaneously choose to invest (C) or not (D) for ten rounds, scoring by threshold participation payoffs toward a 38-point target.",
  "players": {
    "min": 3,
    "max": 3
  },
  "parameters": {
    "rounds": 10,
    "payoff_c_all_cooperate": 5,
    "payoff_c_sheltered_partial": 1,
    "payoff_c_exposed_partial": 0,
    "payoff_d_lone_defector": 4,
    "payoff_d_other": 2,
    "win_threshold": 38,
    "type_probability_sheltered": 0.5
  },
  "attributes": {
    "player": [
      {
        "key": "type",
        "type": "text",
        "visible": "none",
        "initial": null,
        "meaning": "private type Sheltered or Exposed dealt at start, never revealed",
        "observable": false
      },
      {
        "key": "choice",
        "type": "text",
        "visible": "none",
        "initial": null,
        "meaning": "current round choice C or D",
        "observable": false
      },
      {
        "key": "total_score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "cumulative payoff over all rounds",
        "observable": true
      },
      {
        "key": "round_payoff",
        "type": "number",
        "visible": "none",
        "initial": 0,
        "meaning": "payoff earned this round, told privately",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of rounds completed",
        "observable": true
      },
      {
        "key": "n_c",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of players who chose C this round, revealed to all",
        "observable": true
      }
    ]
  },
  "setup": [
    "Deal each of the 3 players a private type Sheltered or Exposed independently with 50% probability each, visible only to owner",
    "Set every player's total_score to 0 and round_number to 0",
    "Explain payoff rules and win threshold 38 to all players"
  ],
  "round": [
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "choice",
        "options": [
          "C",
          "D"
        ]
      },
      "effect": "each player simultaneously chooses C (hunt stag / invest) or D (hunt hare / do not invest), stored in player.choice"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "set game.n_c to count of players with choice==C (0-3) and increment game.round_number by 1"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "adjust player.total_score and set player.round_payoff: if player.choice==C and game.n_c==3 add payoff_c_all_cooperate (5); else if player.choice==C and game.n_c!=3 and player.type==Sheltered add payoff_c_sheltered_partial (1); else if player.choice==C and game.n_c!=3 and player.type==Exposed add payoff_c_exposed_partial (0); else if player.choice==D and game.n_c==2 add payoff_d_lone_defector (4); else if player.choice==D and game.n_c!=2 add payoff_d_other (2)"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "tell each player game.n_c and their own player.round_payoff and player.total_score; do not reveal other players' choices or types"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "continue if game.round_number < rounds (10), otherwise end game"
    }
  ],
  "ending": {
    "condition": "game.round_number >= 10",
    "results": [
      "seat 1",
      "seat 2",
      "seat 3",
      "shared win",
      "draw"
    ],
    "decided_by": "after 10 rounds count players with player.total_score >= win_threshold (38): if count==1 sole winner is that seat; if count>1 shared win among those seats (draw among qualifiers); if count==0 draw; higher total without reaching 38 does not win"
  },
  "choices": [
    {
      "what": "3 to 3 players",
      "why": "Coordination with threshold 3 and lone-defector bonus at n_C==2 only meaningful with exactly 3; with 2 there is no threshold tension, with >3 payoff thresholds 3 and 2 become arbitrary and one player's deviation matters less. Minimum 3 makes agreement hard and a single holdout breaks full cooperation."
    },
    {
      "what": "No pre-round communication poll",
      "why": "Source rules have simultaneous choice with no talk; adding free-text talk would change assurance dilemma into bargaining and is not in source. With 3 players payoff conflict already gives disagreement without talk."
    },
    {
      "what": "Use poll for simultaneous C/D choice",
      "why": "Source says simultaneously every player chooses; poll is required so later players do not see earlier answers, per engine capability"
    },
    {
      "what": "Parameter values 5,4,2,1,0 and threshold 38",
      "why": "Source fixes 5>4>=2>1 and 5>4>=2>0 and example satisfies with 5 for C if n_C==3, 1 if Sheltered else 0 if Exposed when C and n_C!=3, 4 if D and n_C==2 else 2; threshold 38 explicitly given for winner determination"
    },
    {
      "what": "Win condition as shared win / draw, not ranking",
      "why": "Source says higher total alone does not win unless it reaches 38; multiple qualifiers draw among themselves, zero qualifiers is draw. Implemented as arithmetic count of qualifiers, not highest-score ranking."
    }
  ],
  "simplifications": [
    {
      "what": "Payoff matrix implemented as conditional arithmetic updates instead of lookup table",
      "why": "Engine has no payoff-matrix lookup; same arithmetic effect achieved with conditional adds per player using n_c and type (supported with workaround: ~5 conditional branches)"
    },
    {
      "what": "n_C and private payoff revealed via tell/sync rather than separate private channels",
      "why": "Engine's tell/sync delivers private state; matches source 'each player is told n_C and their own payoff, but not who chose what'"
    },
    {
      "what": "Type draw implemented as independent 50% via initial hidden attribute",
      "why": "Engine initialize with hidden_hands/private_values; no deck needed"
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total_score; table: round_number, n_c.
````

## Reply

````
[
  {
    "name": "All cooperate ten rounds - shared win deterministic 50 each",
    "players": 3,
    "seed": 1,
    "moves": {
      "1": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
      "2": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
      "3": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"]
    },
    "expect": {
      "result": "shared win",
      "players": {
        "1": {"total_score": 50},
        "2": {"total_score": 50},
        "3": {"total_score": 50}
      },
      "game": {"round_number": 10, "n_c": 3}
    }
  },
  {
    "name": "Lone defector every round - seat 3 sole winner chance-invariant for defector",
    "players": 3,
    "seed": 2,
    "moves": {
      "1": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
      "2": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
      "3": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"]
    },
    "expect": {
      "result": "seat 3",
      "players": {
        "3": {"total_score": 40}
      },
      "game": {"round_number": 10, "n_c": 2}
    }
  },
  {
    "name": "All defect ten rounds - draw with D_other payoff at n_c 0",
    "players": 3,
    "seed": 3,
    "moves": {
      "1": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
      "2": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
      "3": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"]
    },
    "expect": {
      "result": "draw",
      "players": {
        "1": {"total_score": 20},
        "2": {"total_score": 20},
        "3": {"total_score": 20}
      },
      "game": {"round_number": 10, "n_c": 0}
    }
  },
  {
    "name": "Single cooperator stranded - D_other at n_c 1 chance-invariant for defectors",
    "players": 3,
    "seed": 4,
    "moves": {
      "1": ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C"],
      "2": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
      "3": ["D", "D", "D", "D", "D", "D", "D", "D", "D", "D"]
    },
    "expect": {
      "result": "draw",
      "players": {
        "2": {"total_score": 20},
        "3": {"total_score": 20}
      },
      "game": {"round_number": 10, "n_c": 1}
    }
  },
  {
    "name": "Mixed cooperation threshold edge - 6xC_all then 4xD_other to reach exactly 38 shared win",
    "players": 3,
    "seed": 5,
    "moves": {
      "1": ["C", "C", "C", "C", "C", "C", "D", "D", "D", "D"],
      "2": ["C", "C", "C", "C", "C", "C", "D", "D", "D", "D"],
      "3": ["C", "C", "C", "C", "C", "C", "D", "D", "D", "D"]
    },
    "expect": {
      "result": "shared win",
      "players": {
        "1": {"total_score": 38},
        "2": {"total_score": 38},
        "3": {"total_score": 38}
      },
      "game": {"round_number": 10, "n_c": 0}
    }
  }
]
````
