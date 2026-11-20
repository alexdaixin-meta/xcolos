# 12 scenarios

- time: 2026-11-20T01:59:29+00:00 (150.9s)  model: rl-muse-spark-1-3-sglang-playground
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 b669d491fac32472, reply sha256 e3b0c44298fc1c14
- ERROR: CompletionError: Model API returned 403: {"error":{"code":"network_access_required","message":"This API key belongs to an internal Meta team and requires the Meta corporate network. Connect to the corporate VPN and retry.","param":null,"type":"permission_error"}}

## Sent

````
SPEC:
{
  "name": "One Night Revolution: Ten Nights, Hidden Ledger",
  "summary": "5 players play 10 rounds as rotating Rebels and Informants with framing, claims, and termination votes for hidden points.",
  "players": {
    "min": 5,
    "max": 5,
    "suggested": 5
  },
  "parameters": {
    "num_players": 5,
    "num_rounds": 10,
    "num_pairs": 10,
    "initial_points": 0,
    "informant_rounds_per_player": 4,
    "rebel_rounds_per_player": 6,
    "rebel_correct_vote_gain": 2,
    "rebel_team_bonus": 1,
    "informant_per_misdirected_gain": 1,
    "informant_survival_gain": 2,
    "termination_min_votes": 2
  },
  "attributes": {
    "player": [
      {
        "key": "total_points",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "total hidden points",
        "observable": true
      },
      {
        "key": "rebel_points",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "points earned while Rebel",
        "observable": true
      },
      {
        "key": "informant_points",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "points earned while Informant",
        "observable": true
      },
      {
        "key": "current_role",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Rebel or Informant this round",
        "observable": false
      },
      {
        "key": "partner",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "other Informant seat this round, 0 if Rebel",
        "observable": false
      },
      {
        "key": "target",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "night target seat",
        "observable": false
      },
      {
        "key": "investigation_result",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "Rebel night result Rebel or Informant, empty for Informants",
        "observable": false
      },
      {
        "key": "claim_msg",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "round claim message shown to all",
        "observable": false
      },
      {
        "key": "response_msg",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "round response message shown to all",
        "observable": false
      },
      {
        "key": "vote",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "seat voted to Terminate",
        "observable": true
      },
      {
        "key": "is_terminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "terminated this round",
        "observable": true
      },
      {
        "key": "revealed_role",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "round role announced if terminated else empty",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "round_number",
        "type": "number",
        "visible": "public",
        "initial": 1,
        "meaning": "current round 1 to 10",
        "observable": false
      },
      {
        "key": "pair_order",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "secret shuffled list of all 10 unordered pairs, position r is Informants in round r",
        "observable": false
      },
      {
        "key": "terminated_informant_count",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of terminated players who were Informant this round",
        "observable": true
      }
    ]
  },
  "setup": [
    "Each of the 5 players starts with 0 total points, 0 Rebel points and 0 Informant points.",
    "The engine lists all 10 unordered pairs of the 5 players and shuffles the list secretly as pair_order.",
    "This shuffle is the only random event and players are told the schedule rule but not the order.",
    "The engine sets game round_number to 1."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "sets each player current_role and partner from pair_order for game.round_number; clears is_terminated, revealed_role, target, vote, investigation_result"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "privately sends each player current_role; Informants also receive partner"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "choice",
        "prompt": "name one other player as night target"
      },
      "effect": "sets player.target; Rebel target is investigated and Informant target is framed"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "sets player.investigation_result to Informant if target current_role is Informant or target was framed by any Informant, else Rebel; Informants keep empty"
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "privately sends each Rebel investigation_result; Informants receive no result"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "text",
        "prompt": "write one short claim message"
      },
      "effect": "sets player.claim_msg and broadcasts to all as Seat {seat} says: {value}"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "text",
        "prompt": "write one short response message"
      },
      "effect": "sets player.response_msg and broadcasts to all as Seat {seat} says: {value}"
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": {
        "type": "choice",
        "prompt": "name one other player to Terminate"
      },
      "effect": "sets player.vote"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announces all player.vote showing who voted for whom using vote"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "sets player.is_terminated: if no seat has 2 or more votes then false for all, else true for seats tied for most votes; sets player.revealed_role to current_role if is_terminated else empty; sets game.terminated_informant_count"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "announces player.is_terminated and player.revealed_role for terminated players only"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "adds hidden points: Rebels who voted for an Informant gain 2 to total_points and rebel_points; if terminated_informant_count >=1 each Rebel gains 1 more to total_points and rebel_points; each Informant gains 1 per Rebel who voted for a Rebel to total_points and informant_points; each Informant with is_terminated false gains 2 to total_points and informant_points; increments game.round_number; nothing about points is announced"
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "continues if game.round_number <= 10, otherwise ends and announces total_points, rebel_points and informant_points"
    }
  ],
  "ending": {
    "condition": "game.round_number > 10",
    "rank_by": "you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points",
    "decided_by": "standing is total_points, tie-break most rebel_points then most informant_points; highest wins and tied top share the win"
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, then each player has 0 total points, 0 Rebel points and 0 Informant points."
    },
    {
      "id": "R2",
      "text": "When the game is played, then there are 10 rounds and in round r the pair in position r of the shuffled 10 pairs is the Informants."
    },
    {
      "id": "R3",
      "text": "When the schedule is used, then each player is Informant in exactly 4 rounds with each other player as partner exactly once and Rebel in exactly 6 rounds."
    },
    {
      "id": "R4",
      "text": "When a round starts, then each player is privately told Rebel or Informant and each Informant is told who the other Informant is."
    },
    {
      "id": "R5",
      "text": "When night happens, then every player simultaneously names one other player as target."
    },
    {
      "id": "R6",
      "text": "When night targets are set, then a Rebel target is investigated and an Informant target is framed, and an Informant may target anyone including the partner with no extra effect for framing a partner."
    },
    {
      "id": "R7",
      "text": "When night results are given, then each Rebel is privately told Informant if the target is an Informant this round or at least one Informant framed that target, otherwise Rebel."
    },
    {
      "id": "R8",
      "text": "When night results are given, then a Rebel result is always true and an Informant result may be true or a frame."
    },
    {
      "id": "R9",
      "text": "When night results are given, then Informants receive no result."
    },
    {
      "id": "R10",
      "text": "When claims happen, then every player simultaneously writes one short message with lying allowed and all messages are then shown to everyone."
    },
    {
      "id": "R11",
      "text": "When responses happen, then every player simultaneously writes one more short message and all are then shown to everyone."
    },
    {
      "id": "R12",
      "text": "When voting happens, then every player simultaneously names one other player to Terminate and all votes showing who voted for whom are announced publicly."
    },
    {
      "id": "R13",
      "text": "When votes are counted, then if no player received 2 or more votes nobody is terminated."
    },
    {
      "id": "R14",
      "text": "When at least one player received 2 or more votes, then every player tied for the most votes is terminated."
    },
    {
      "id": "R15",
      "text": "When termination is announced, then only the round roles of terminated players are announced publicly and no other roles are revealed."
    },
    {
      "id": "R16",
      "text": "When scoring happens, then each Rebel who voted for an Informant gains 2 points."
    },
    {
      "id": "R17",
      "text": "When scoring happens, then if at least one terminated player is an Informant each Rebel gains 1 more point."
    },
    {
      "id": "R18",
      "text": "When scoring happens, then each Informant gains 1 point for every Rebel who voted for a Rebel."
    },
    {
      "id": "R19",
      "text": "When scoring happens, then each Informant who was not terminated this round gains 2 points."
    },
    {
      "id": "R20",
      "text": "When points are gained while Rebel, then they are also added to Rebel points and when gained while Informant also added to Informant points."
    },
    {
      "id": "R21",
      "text": "When the game is played, then no totals of any kind are announced during the game and only votes and terminated roles are announced each round."
    },
    {
      "id": "R22",
      "text": "When termination happens, then it removes no one and all 5 play every round."
    },
    {
      "id": "R23",
      "text": "When round 10 ends, then the engine announces every player's final total, Rebel points and Informant points and the game ends."
    },
    {
      "id": "R24",
      "text": "When the game ends, then the player with the highest total points wins with tie-break most Rebel points then most Informant points then draw."
    }
  ],
  "offers": [
    {
      "question": "night target",
      "who": "all players",
      "options": "any other living seat except self: the 4 other seats"
    },
    {
      "question": "claim message",
      "who": "all players",
      "options": "any short text, lying allowed"
    },
    {
      "question": "response message",
      "who": "all players",
      "options": "any short text, lying allowed"
    },
    {
      "question": "vote to Terminate",
      "who": "all players",
      "options": "any other living seat except self: the 4 other seats"
    }
  ],
  "choices": [
    {
      "what": "5 to 5 players, suggested 5",
      "why": "designer set 5; minimum 5 because 2 Informants versus 3 Rebels plus framing and 2-vote termination needs a minority that can hide; maximum not larger because 10-pair schedule and vote math are built for 5"
    },
    {
      "what": "simultaneous poll for night, claims, responses and votes",
      "why": "source says simultaneous, so poll with nobody seeing answers until all are in; ask not used because order must not leak"
    },
    {
      "what": "rank_by you.total_points * 1000000 + you.rebel_points * 1000 + you.informant_points",
      "why": "encodes total first then Rebel points then Informant points as tie-breaks within one arithmetic expression; scaling exceeds max attainable points"
    },
    {
      "what": "talk kept as two simultaneous polls with broadcast to all",
      "why": "claims and responses give material to reason about and players disagree because Informants want misdirected votes and Rebels want true votes, so following a proposal could cost them"
    }
  ],
  "simplifications": [
    {
      "what": "pair schedule stored as secret game list pair_order drawn by position each round",
      "why": "to fit shared_deck_draw workaround with remove/append operations and no extra randomness"
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: total_points, rebel_points, informant_points, vote, is_terminated, revealed_role; table: terminated_informant_count.
````

## Reply

````

````
