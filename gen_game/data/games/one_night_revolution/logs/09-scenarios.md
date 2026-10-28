# 09 scenarios

- time: 2026-10-28T01:40:58+00:00 (71.0s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 da77dd58e08c8130, reply sha256 7b0e35d2f82c54bb

## Sent

````
SPEC:
{
  "name": "One Night Revolution: Ten Nights",
  "summary": "Five players play ten rounds of hidden roles. Each round a secretly scheduled pair are Informants and the other three are Rebels; players investigate or frame at night, talk twice, then vote, and score points individually.",
  "players": {
    "min": 5,
    "max": 5,
    "suggested": 5
  },
  "parameters": {
    "player_count": 5,
    "rounds": 10,
    "possible_pairs": 10,
    "informants_per_round": 2,
    "rebels_per_round": 3,
    "informant_rounds_per_player": 4,
    "rebel_rounds_per_player": 6,
    "starting_points": 0,
    "termination_vote_threshold": 2,
    "rebel_correct_vote_points": 2,
    "rebel_informant_terminated_bonus": 1,
    "informant_points_per_rebel_misvote": 1,
    "informant_max_misvote_points": 3,
    "informant_survival_bonus": 2,
    "messages_per_round": 2
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "total points",
        "observable": true
      },
      {
        "key": "rebel_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points gained while a Rebel (first tie-break)",
        "observable": true
      },
      {
        "key": "informant_points",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points gained while an Informant (second tie-break)",
        "observable": true
      },
      {
        "key": "role",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "this round's role: 'Informant' or 'Rebel'",
        "observable": false
      },
      {
        "key": "partner",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "for an Informant, the seat of the other Informant this round; empty for a Rebel",
        "observable": false
      },
      {
        "key": "target",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "the seat named at night (investigated by a Rebel, framed by an Informant)",
        "observable": false
      },
      {
        "key": "result",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "a Rebel's night result about their target: 'Informant' or 'Rebel'",
        "observable": false
      },
      {
        "key": "claim",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's claims message",
        "observable": false
      },
      {
        "key": "response",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "this round's response message",
        "observable": false
      },
      {
        "key": "vote",
        "type": "text",
        "visible": "public",
        "initial": "",
        "meaning": "the seat this player voted to Terminate this round",
        "observable": true
      },
      {
        "key": "votes_received",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of Terminate votes received this round",
        "observable": false
      },
      {
        "key": "terminated",
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
        "meaning": "this round's role, announced only when the player is terminated; otherwise empty",
        "observable": true
      }
    ],
    "game": [
      {
        "key": "pair_order",
        "type": "list",
        "visible": "none",
        "initial": "the 10 pairs of seats, shuffled secretly at setup",
        "meaning": "entry r is the Informant pair for round r",
        "observable": false
      },
      {
        "key": "framed_seats",
        "type": "list",
        "visible": "none",
        "initial": [],
        "meaning": "the seats framed by at least one Informant this round; hidden, the engine keeps it",
        "observable": false
      },
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number",
        "observable": true
      },
      {
        "key": "max_votes",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "the highest votes_received this round",
        "observable": false
      },
      {
        "key": "informant_terminated",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "true if at least one terminated player is an Informant this round",
        "observable": false
      },
      {
        "key": "rebel_misvotes",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "number of Rebels who voted for a Rebel this round",
        "observable": false
      }
    ]
  },
  "setup": [
    "Five seats are filled; each player's score, rebel_points and informant_points start at 0.",
    "The engine lists all 10 pairs of the 5 seats and shuffles the list secretly into pair_order. This is the only random event in the game.",
    "All players are told that in round r the pair in position r of pair_order are the Informants and the other 3 are Rebels. Each player is therefore an Informant in exactly 4 rounds, partnered with each other player exactly once, and a Rebel in 6 rounds. They are not told the order."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1. For every player, reset target, result, claim, response and vote to '', terminated to false, revealed_role to '' and votes_received to 0. Set framed_seats to [] and reset max_votes, informant_terminated and rebel_misvotes."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "Let the pair be pair_order[round]. Each seat in the pair gets role = 'Informant' and partner = the other seat of the pair. Every other seat gets role = 'Rebel' and partner = ''."
    },
    {
      "action": "sync",
      "who": "all players",
      "answer": null,
      "effect": "Each player privately sees their own role and, if an Informant, their partner."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one other seat",
      "effect": "Set target. Then, for each Informant, append that Informant's target to framed_seats if it is not already there. Framing the partner has no extra effect."
    },
    {
      "action": "update",
      "who": "each Rebel",
      "answer": null,
      "effect": "result = 'Informant' if target.role == 'Informant' or target is in framed_seats; otherwise result = 'Rebel'."
    },
    {
      "action": "sync",
      "who": "each Rebel",
      "answer": null,
      "effect": "Each Rebel privately sees their result. Informants receive no result."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text (claims; lying allowed)",
      "effect": "Set claim; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text (responses; lying allowed)",
      "effect": "Set response; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} responds: {value}\"}."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one other seat to Terminate",
      "effect": "Set vote; publicly announce every voter and whom they voted for."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "votes_received = number of players whose vote names this seat; max_votes = the highest votes_received."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If max_votes >= 2, then terminated = true for each player with votes_received == max_votes. For each terminated player, revealed_role = role. informant_terminated = true if any terminated player has role 'Informant'. Announce the revealed roles of terminated players only."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "rebel_misvotes = number of Rebels whose vote names a Rebel. Each Rebel gains g = (2 if their vote names an Informant else 0) + (1 if informant_terminated else 0); score += g and rebel_points += g. Each Informant gains g = rebel_misvotes + (2 if not informant_terminated else 0); score += g and informant_points += g."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce every player's score, rebel_points and informant_points."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "If round >= 10, end the game; otherwise run the next round. No one is ever removed from play."
    }
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 10000 + you.rebel_points * 100 + you.informant_points",
    "decided_by": "Highest total points wins. Ties are broken by most Rebel points, then by most Informant points. Players still level share the result, which counts as the draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "At the start, every player has score 0, rebel_points 0 and informant_points 0."
    },
    {
      "id": "R2",
      "text": "Before round 1, the 10 pairs of the 5 seats are shuffled once into pair_order, and no other randomness occurs."
    },
    {
      "id": "R3",
      "text": "In round r, the two seats in pair_order position r have role Informant and the other 3 have role Rebel."
    },
    {
      "id": "R4",
      "text": "Over 10 rounds, each player is an Informant exactly 4 times, with each other player as partner exactly once, and a Rebel exactly 6 times."
    },
    {
      "id": "R5",
      "text": "Each round, each Informant privately learns the seat of the other Informant; Rebels learn no partner."
    },
    {
      "id": "R6",
      "text": "At night, every player names exactly one other seat as target, simultaneously; naming oneself is not allowed."
    },
    {
      "id": "R7",
      "text": "When a Rebel's target is an Informant this round, the Rebel's result is 'Informant'."
    },
    {
      "id": "R8",
      "text": "When a Rebel's target is a Rebel framed by at least one Informant this round, the result is 'Informant'."
    },
    {
      "id": "R9",
      "text": "When a Rebel's target is a Rebel that no Informant framed, the result is 'Rebel'."
    },
    {
      "id": "R10",
      "text": "Informants receive no night result."
    },
    {
      "id": "R11",
      "text": "Every player sends one claim message and then one response message, each collected simultaneously and shown to all."
    },
    {
      "id": "R12",
      "text": "Every player votes for exactly one other seat, simultaneously, and all votes are announced with voter and target."
    },
    {
      "id": "R13",
      "text": "When no player receives 2 or more votes, nobody is terminated."
    },
    {
      "id": "R14",
      "text": "When the highest vote count is 2 or more, every player with that count is terminated (for example, a 2-2-1 split terminates two players)."
    },
    {
      "id": "R15",
      "text": "Only terminated players have their round role announced publicly."
    },
    {
      "id": "R16",
      "text": "When a Rebel votes for an Informant, that Rebel gains 2 points."
    },
    {
      "id": "R17",
      "text": "When at least one terminated player is an Informant, each Rebel gains 1 more point."
    },
    {
      "id": "R18",
      "text": "Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3)."
    },
    {
      "id": "R19",
      "text": "When no Informant is terminated (including when nobody is terminated), each Informant gains 2 more points."
    },
    {
      "id": "R20",
      "text": "Points gained as a Rebel are added to both score and rebel_points; points gained as an Informant are added to both score and informant_points."
    },
    {
      "id": "R21",
      "text": "Termination removes no one; all 5 players take part in every round."
    },
    {
      "id": "R22",
      "text": "After round 10 the game ends, and the highest score wins."
    },
    {
      "id": "R23",
      "text": "When scores tie at the top, the player with the most rebel_points wins; if still tied, the one with the most informant_points; if still tied, the tied players share a draw."
    }
  ],
  "offers": [
    {
      "question": "Night target",
      "who": "every seat",
      "options": "any one of the 4 other seats (an Informant may name their partner)"
    },
    {
      "question": "Claim message",
      "who": "every seat",
      "options": "short free text"
    },
    {
      "question": "Response message",
      "who": "every seat",
      "options": "short free text"
    },
    {
      "question": "Terminate vote",
      "who": "every seat",
      "options": "any one of the 4 other seats"
    }
  ],
  "choices": [
    {
      "what": "Exactly 5 players (min = max = suggested = 5)",
      "why": "The designer fixed 5. The schedule of 10 pairs over 10 rounds, with each player an Informant 4 times and partnered with everyone once, only works with 5 seats. Five also leaves 3 Rebels, enough for a 2-Informant minority to hide in."
    },
    {
      "what": "Keep both talk phases as simultaneous polls broadcast to all",
      "why": "The rules make both message phases simultaneous. Talk matters because Informants want Rebels to misvote while Rebels want to find the Informants, so following a claim can cost a player."
    },
    {
      "what": "rebel_points and informant_points are public",
      "why": "The rules announce everyone's totals and use these sub-totals as tie-breaks; making them public is the plainest reading."
    },
    {
      "what": "Rank expression score*10000 + rebel_points*100 + informant_points",
      "why": "Each sub-total stays well below 100 over 10 rounds, so the weights keep the order: score first, then Rebel points, then Informant points. Players still level share the win, which is the draw."
    },
    {
      "what": "Player strategy",
      "why": "Rebels compare results and claims, knowing a 'Rebel' result is always true while an 'Informant' result may be a frame. Informants frame Rebels and coordinate a story with their partner. Everyone tracks past pairings, since each pair is Informants only once."
    }
  ],
  "simplifications": [
    {
      "what": "The secret schedule is stored as a hidden table list pair_order, and roles are recomputed from it each round",
      "why": "The engine needs the schedule as stated state; this is the rule's own mechanism."
    },
    {
      "what": "Which players were framed is kept in a hidden table list framed_seats rather than on each player",
      "why": "A player attribute cannot be hidden from its owner, and a framed player must not learn of the frame; a table list with visibility none keeps it secret."
    },
    {
      "what": "Per-round scratch values (votes_received, max_votes, informant_terminated, rebel_misvotes) are held as attributes",
      "why": "The engine computes termination and scoring by arithmetic on stated attributes."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, rebel_points, informant_points, vote, terminated, revealed_role; table: round.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
[
  {"name": "R1: every player starts at 0 points", "rule": "R1", "players": 5, "seed": 1, "rounds": 0,
   "expect": {"players": {
     "1": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "2": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "3": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "4": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "5": {"score": 0, "rebel_points": 0, "informant_points": 0}},
     "game": {"round": 0}}},

  {"name": "R2: the schedule of 10 pairs exists at setup", "rule": "R2", "players": 5, "seed": 2, "rounds": 0,
   "expect": {"lens": {"game": {"pair_order": 10}}, "game": {"round": 0}}},

  {"name": "R3: the scheduled pair (2,5) are Informants, the others Rebels (seen through revealed roles)", "rule": "R3", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 3, "options_include": 2, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 2, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Rebel", "score": 3},
     "2": {"terminated": true, "revealed_role": "Informant", "score": 0},
     "3": {"terminated": false, "revealed_role": "", "score": 3},
     "4": {"terminated": false, "revealed_role": "", "score": 3},
     "5": {"terminated": false, "revealed_role": "", "score": 0}},
     "game": {"round": 1}}},

  {"name": "R4: with cyclic votes every schedule gives each seat 20 points (6 Rebel, 14 Informant), so all share the result", "rule": "R4", "players": 5, "seed": 3,
   "rules": [{"seat": 1, "options_include": 2, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 4, "times": "all"},
             {"seat": 4, "options_include": 5, "times": "all"},
             {"seat": 5, "options_include": 1, "times": "all"}],
   "expect": {"winner": [1, 2, 3, 4, 5],
              "standings": {"1": 200614, "2": 200614, "3": 200614, "4": 200614, "5": 200614},
              "players": {
                "1": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "2": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "3": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "4": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "5": {"score": 20, "rebel_points": 6, "informant_points": 14}},
              "game": {"round": 10}}},

  {"name": "R5: both seats of the pair act as Informants (partner itself is hidden; both get Informant scoring)", "rule": "R5", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 2, "rebel_points": 2, "informant_points": 0},
     "2": {"score": 3, "rebel_points": 0, "informant_points": 3},
     "3": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "4": {"score": 2, "rebel_points": 2, "informant_points": 0},
     "5": {"score": 3, "rebel_points": 0, "informant_points": 3}}}},

  {"name": "R6: no seat may name itself", "rule": "R6", "players": 5, "seed": 1, "rounds": 1,
   "expect": {"not_offered": [{"seat": 1, "option": 1}, {"seat": 2, "option": 2}, {"seat": 3, "option": 3}, {"seat": 4, "option": 4}, {"seat": 5, "option": 5}],
              "offered": [{"seat": 1, "option": 2}, {"seat": 5, "option": 4}]}},

  {"name": "R7: a Rebel investigating an Informant (result is hidden; round scores as usual)", "rule": "R7", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant"},
     "2": {"score": 0},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 3, "rebel_points": 3}}}},

  {"name": "R8: an Informant frames the Rebel another Rebel investigates (result is hidden; scoring unaffected)", "rule": "R8", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": 3},
             {"seat": 3, "options_include": 4}, {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant"},
     "2": {"score": 0},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 3, "rebel_points": 3}}}},

  {"name": "R9: a Rebel investigating an unframed Rebel (result is hidden; scoring unaffected)", "rule": "R9", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 3, "options_include": 5}, {"seat": 3, "options_include": 1},
             {"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true},
     "3": {"score": 3},
     "4": {"score": 3},
     "5": {"score": 3}}}},

  {"name": "R10: Informants get no result; their scoring follows votes only", "rule": "R10", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"score": 5, "informant_points": 5, "rebel_points": 0},
     "2": {"score": 5, "informant_points": 5, "rebel_points": 0}}}},

  {"name": "R11: both talk phases are collected and the round completes", "rule": "R11", "players": 5, "seed": 1, "rounds": 1,
   "expect": {"game": {"round": 1}}},

  {"name": "R12: every vote is recorded with its target and no one may vote for itself", "rule": "R12", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"vote": "3"}, "2": {"vote": "3"}, "3": {"vote": "4"}, "4": {"vote": "3"}, "5": {"vote": "4"}},
     "not_offered": [{"seat": 3, "option": 3}, {"seat": 4, "option": 4}]}},

  {"name": "R13: a 1-1-1-1-1 split terminates nobody", "rule": "R13", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": false, "revealed_role": ""},
     "2": {"terminated": false, "revealed_role": ""},
     "3": {"terminated": false, "revealed_role": ""},
     "4": {"terminated": false, "revealed_role": ""},
     "5": {"terminated": false, "revealed_role": ""}}}},

  {"name": "R14: a 2-2-1 split terminates both players on 2 votes", "rule": "R14", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 2, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Informant", "score": 0},
     "2": {"terminated": false, "revealed_role": "", "score": 0},
     "3": {"terminated": true, "revealed_role": "Rebel", "score": 3},
     "4": {"terminated": false, "score": 3},
     "5": {"terminated": false, "score": 3}}}},

  {"name": "R15: only the terminated Rebel's role is revealed", "rule": "R15", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"revealed_role": "", "terminated": false},
     "2": {"revealed_role": "", "terminated": false},
     "3": {"revealed_role": "Rebel", "terminated": true},
     "4": {"revealed_role": "", "terminated": false},
     "5": {"revealed_role": "", "terminated": false}}}},

  {"name": "R16: a Rebel voting for an Informant gains 2 (nobody terminated)", "rule": "R16", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "3": {"score": 0, "rebel_points": 0},
     "4": {"score": 0, "rebel_points": 0},
     "5": {"score": 2, "rebel_points": 2}}}},

  {"name": "R17: an Informant is terminated, so every Rebel gains 1 more", "rule": "R17", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 4, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Informant", "score": 1, "informant_points": 1},
     "2": {"score": 1, "informant_points": 1},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 1, "rebel_points": 1}}}},

  {"name": "R18: all 3 Rebels misvote, each Informant gains 3 (+2 survival)", "rule": "R18", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"score": 5, "informant_points": 5},
     "2": {"score": 5, "informant_points": 5},
     "3": {"score": 0}, "4": {"score": 0}, "5": {"score": 0}}}},

  {"name": "R19: nobody terminated, each Informant gets the 2-point survival bonus plus 2 misvotes", "rule": "R19", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 4, "informant_points": 4},
     "2": {"score": 4, "informant_points": 4}}}},

  {"name": "R20: gains are added to score and to the matching sub-total", "rule": "R20", "players": 5, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"score": 10, "rebel_points": 6, "informant_points": 4},
                         "5": {"score": 7, "rebel_points": 5, "informant_points": 2}},
             "game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 14, "rebel_points": 6, "informant_points": 8},
     "5": {"score": 9, "rebel_points": 7, "informant_points": 2}}}},

  {"name": "R21: a terminated player still plays the next round", "rule": "R21", "players": 5, "seed": 1, "rounds": 2,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 1, "times": "all"},
             {"seat": 4, "options_include": 1, "times": "all"},
             {"seat": 5, "options_include": 1, "times": "all"}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant", "vote": "3"},
     "3": {"score": 6, "rebel_points": 6},
     "4": {"score": 6, "rebel_points": 6},
     "5": {"score": 6, "rebel_points": 6}},
     "game": {"round": 2}}},

  {"name": "R22: the game ends after round 10 and the far-ahead score wins (last round's gains cannot change it)", "rule": "R22", "players": 5, "seed": 4,
   "given": {"players": {"1": {"score": 50, "rebel_points": 30, "informant_points": 20},
                         "2": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "3": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "4": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "5": {"score": 10, "rebel_points": 5, "informant_points": 5}},
             "game": {"round": 9}},
   "expect": {"winner": 1, "game": {"round": 10}}},

  {"name": "R23: equal scores, more rebel_points wins", "rule": "R23", "players": 5, "seed": 1,
   "given": {"players": {"1": {"score": 40, "rebel_points": 25, "informant_points": 15},
                         "2": {"score": 40, "rebel_points": 20, "informant_points": 20}},
             "game": {"round": 9, "pair_order": [[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2}],
   "expect": {"winner": 1,
              "standings": {"1": 432815, "2": 432320, "3": 0, "4": 0, "5": 30300},
              "players": {"1": {"score": 43, "rebel_points": 28, "informant_points": 15},
                          "2": {"score": 43, "rebel_points": 23, "informant_points": 20},
                          "3": {"terminated": true, "revealed_role": "Informant"}},
              "game": {"round": 10}}}
]
```

Why it was refused: scenario 1: needs `rules` (what each seat answers, by option name); scenario 2: needs `rules` (what each seat answers, by option name); scenario 6: needs `rules` (what each seat answers, by option name); scenario 11: needs `rules` (what each seat answers, by option name); scenario 22: needs `rules` (what each seat answers, by option name)
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
[
  {"name": "R1: every player starts at 0 points (one round of cyclic votes adds exactly the round's gains)", "rule": "R1", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 4, "rebel_points": 0, "informant_points": 4},
     "2": {"score": 4, "rebel_points": 0, "informant_points": 4},
     "3": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "4": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "5": {"score": 2, "rebel_points": 2, "informant_points": 0}},
     "game": {"round": 1}}},

  {"name": "R2: the schedule of 10 pairs exists (round 1 played; chance only orders the pairs)", "rule": "R2", "players": 5, "seed": 2, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"lens": {"game": {"pair_order": 10}}, "game": {"round": 1}}},

  {"name": "R3: the scheduled pair (2,5) are Informants, the others Rebels (seen through revealed roles)", "rule": "R3", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 3, "options_include": 2, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 2, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Rebel", "score": 3},
     "2": {"terminated": true, "revealed_role": "Informant", "score": 0},
     "3": {"terminated": false, "revealed_role": "", "score": 3},
     "4": {"terminated": false, "revealed_role": "", "score": 3},
     "5": {"terminated": false, "revealed_role": "", "score": 0}},
     "game": {"round": 1}}},

  {"name": "R4: with cyclic votes every schedule gives each seat 20 points (6 Rebel, 14 Informant), so all share the result", "rule": "R4", "players": 5, "seed": 3,
   "rules": [{"seat": 1, "options_include": 2, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 4, "times": "all"},
             {"seat": 4, "options_include": 5, "times": "all"},
             {"seat": 5, "options_include": 1, "times": "all"}],
   "expect": {"winner": [1, 2, 3, 4, 5],
              "standings": {"1": 200614, "2": 200614, "3": 200614, "4": 200614, "5": 200614},
              "players": {
                "1": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "2": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "3": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "4": {"score": 20, "rebel_points": 6, "informant_points": 14},
                "5": {"score": 20, "rebel_points": 6, "informant_points": 14}},
              "game": {"round": 10}}},

  {"name": "R5: both seats of the pair act as Informants (partner itself is hidden; both get Informant scoring)", "rule": "R5", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5],[2,5]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 2, "rebel_points": 2, "informant_points": 0},
     "2": {"score": 3, "rebel_points": 0, "informant_points": 3},
     "3": {"score": 0, "rebel_points": 0, "informant_points": 0},
     "4": {"score": 2, "rebel_points": 2, "informant_points": 0},
     "5": {"score": 3, "rebel_points": 0, "informant_points": 3}}}},

  {"name": "R6: no seat may name itself", "rule": "R6", "players": 5, "seed": 1, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"not_offered": [{"seat": 1, "option": 1}, {"seat": 2, "option": 2}, {"seat": 3, "option": 3}, {"seat": 4, "option": 4}, {"seat": 5, "option": 5}],
              "offered": [{"seat": 1, "option": 2}, {"seat": 5, "option": 4}]}},

  {"name": "R7: a Rebel investigating an Informant (result is hidden; round scores as usual)", "rule": "R7", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant"},
     "2": {"score": 0},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 3, "rebel_points": 3}}}},

  {"name": "R8: an Informant frames the Rebel another Rebel investigates (result is hidden; scoring unaffected)", "rule": "R8", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 4}, {"seat": 1, "options_include": 3},
             {"seat": 3, "options_include": 4}, {"seat": 3, "options_include": 1},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant"},
     "2": {"score": 0},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 3, "rebel_points": 3}}}},

  {"name": "R9: a Rebel investigating an unframed Rebel (result is hidden; scoring unaffected)", "rule": "R9", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 3, "options_include": 5}, {"seat": 3, "options_include": 1},
             {"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true},
     "3": {"score": 3},
     "4": {"score": 3},
     "5": {"score": 3}}}},

  {"name": "R10: Informants get no result; their scoring follows votes only", "rule": "R10", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"score": 5, "informant_points": 5, "rebel_points": 0},
     "2": {"score": 5, "informant_points": 5, "rebel_points": 0}}}},

  {"name": "R11: both talk phases are collected and the round completes", "rule": "R11", "players": 5, "seed": 1, "rounds": 1,
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"game": {"round": 1}}},

  {"name": "R12: every vote is recorded with its target and no one may vote for itself", "rule": "R12", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"vote": "3"}, "2": {"vote": "3"}, "3": {"vote": "4"}, "4": {"vote": "3"}, "5": {"vote": "4"}},
     "not_offered": [{"seat": 3, "option": 3}, {"seat": 4, "option": 4}]}},

  {"name": "R13: a 1-1-1-1-1 split terminates nobody", "rule": "R13", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": false, "revealed_role": ""},
     "2": {"terminated": false, "revealed_role": ""},
     "3": {"terminated": false, "revealed_role": ""},
     "4": {"terminated": false, "revealed_role": ""},
     "5": {"terminated": false, "revealed_role": ""}}}},

  {"name": "R14: a 2-2-1 split terminates both players on 2 votes", "rule": "R14", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 2, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Informant", "score": 0},
     "2": {"terminated": false, "revealed_role": "", "score": 0},
     "3": {"terminated": true, "revealed_role": "Rebel", "score": 3},
     "4": {"terminated": false, "score": 3},
     "5": {"terminated": false, "score": 3}}}},

  {"name": "R15: only the terminated Rebel's role is revealed", "rule": "R15", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"revealed_role": "", "terminated": false},
     "2": {"revealed_role": "", "terminated": false},
     "3": {"revealed_role": "Rebel", "terminated": true},
     "4": {"revealed_role": "", "terminated": false},
     "5": {"revealed_role": "", "terminated": false}}}},

  {"name": "R16: a Rebel voting for an Informant gains 2 (nobody terminated)", "rule": "R16", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "3": {"score": 0, "rebel_points": 0},
     "4": {"score": 0, "rebel_points": 0},
     "5": {"score": 2, "rebel_points": 2}}}},

  {"name": "R17: an Informant is terminated, so every Rebel gains 1 more", "rule": "R17", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 4, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"terminated": true, "revealed_role": "Informant", "score": 1, "informant_points": 1},
     "2": {"score": 1, "informant_points": 1},
     "3": {"score": 3, "rebel_points": 3},
     "4": {"score": 3, "rebel_points": 3},
     "5": {"score": 1, "rebel_points": 1}}}},

  {"name": "R18: all 3 Rebels misvote, each Informant gains 3 (+2 survival)", "rule": "R18", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 4, "times": 2}],
   "expect": {"players": {
     "1": {"score": 5, "informant_points": 5},
     "2": {"score": 5, "informant_points": 5},
     "3": {"score": 0}, "4": {"score": 0}, "5": {"score": 0}}}},

  {"name": "R19: nobody terminated, each Informant gets the 2-point survival bonus plus 2 misvotes", "rule": "R19", "players": 5, "seed": 1, "rounds": 1,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 4, "informant_points": 4},
     "2": {"score": 4, "informant_points": 4}}}},

  {"name": "R20: gains are added to score and to the matching sub-total", "rule": "R20", "players": 5, "seed": 1, "rounds": 1,
   "given": {"players": {"1": {"score": 10, "rebel_points": 6, "informant_points": 4},
                         "5": {"score": 7, "rebel_points": 5, "informant_points": 2}},
             "game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"players": {
     "1": {"score": 14, "rebel_points": 6, "informant_points": 8},
     "5": {"score": 9, "rebel_points": 7, "informant_points": 2}}}},

  {"name": "R21: a terminated player still plays the next round", "rule": "R21", "players": 5, "seed": 1, "rounds": 2,
   "given": {"game": {"round": 0, "pair_order": [[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2],[1,2]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": "all"},
             {"seat": 2, "options_include": 3, "times": "all"},
             {"seat": 3, "options_include": 1, "times": "all"},
             {"seat": 4, "options_include": 1, "times": "all"},
             {"seat": 5, "options_include": 1, "times": "all"}],
   "expect": {"players": {
     "1": {"score": 0, "terminated": true, "revealed_role": "Informant", "vote": "3"},
     "3": {"score": 6, "rebel_points": 6},
     "4": {"score": 6, "rebel_points": 6},
     "5": {"score": 6, "rebel_points": 6}},
     "game": {"round": 2}}},

  {"name": "R22: the game ends after round 10 and the far-ahead score wins (last round's gains cannot change it)", "rule": "R22", "players": 5, "seed": 4,
   "given": {"players": {"1": {"score": 50, "rebel_points": 30, "informant_points": 20},
                         "2": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "3": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "4": {"score": 10, "rebel_points": 5, "informant_points": 5},
                         "5": {"score": 10, "rebel_points": 5, "informant_points": 5}},
             "game": {"round": 9}},
   "rules": [{"seat": 1, "options_include": 2, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 4, "times": 2},
             {"seat": 4, "options_include": 5, "times": 2},
             {"seat": 5, "options_include": 1, "times": 2}],
   "expect": {"winner": 1, "game": {"round": 10}}},

  {"name": "R23: equal scores, more rebel_points wins", "rule": "R23", "players": 5, "seed": 1,
   "given": {"players": {"1": {"score": 40, "rebel_points": 25, "informant_points": 15},
                         "2": {"score": 40, "rebel_points": 20, "informant_points": 20}},
             "game": {"round": 9, "pair_order": [[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4],[3,4]]}},
   "rules": [{"seat": 1, "options_include": 3, "times": 2},
             {"seat": 2, "options_include": 3, "times": 2},
             {"seat": 5, "options_include": 3, "times": 2},
             {"seat": 3, "options_include": 1, "times": 2},
             {"seat": 4, "options_include": 1, "times": 2}],
   "expect": {"winner": 1,
              "standings": {"1": 432815, "2": 432320, "3": 0, "4": 0, "5": 30300},
              "players": {"1": {"score": 43, "rebel_points": 28, "informant_points": 15},
                          "2": {"score": 43, "rebel_points": 23, "informant_points": 20},
                          "3": {"terminated": true, "revealed_role": "Informant"}},
              "game": {"round": 10}}}
]
```
````
