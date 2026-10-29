# 07 spec

- time: 2026-10-28T01:38:34+00:00 (34.9s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 4c0aa333ed857407, reply sha256 6fd6b970580ab6a3

## Sent

````
Game: One Night Revolution: Ten Nights
Players in the source: 5 to 5
Suggested table size, chosen by the designer of these rules (keep it): 5

Rules, as filed in the inventory:
SETUP: There are 5 players, each starting with 0 points. Each player also keeps two sub-totals, Rebel points and Informant points, both starting at 0. Before round 1, the engine lists all 10 possible pairs of players and shuffles that list secretly. This is the only random event in the game. In round r (r = 1 to 10), the pair in position r of the shuffled list are the Informants; the other 3 players are Rebels for that round. As a result, every player is an Informant in exactly 4 rounds, with each other player as partner exactly once, and a Rebel in exactly 6 rounds. All players are told this rule but not the order.

EACH ROUND:
1. ROLES: Each player is privately told their role for this round. Each Informant is also privately told who the other Informant is.
2. NIGHT (simultaneous): Every player privately names one other player as a target. A Rebel's target is investigated. An Informant's target is framed. An Informant may name any other player, including their partner (framing a partner has no extra effect).
3. NIGHT RESULTS: Each Rebel is privately told one result about their target. The result is 'Informant' if the target is an Informant this round, or if at least one Informant framed that target this round. Otherwise it is 'Rebel'. A 'Rebel' result is therefore always true; an 'Informant' result may be a frame. Informants receive no result.
4. CLAIMS (simultaneous): Every player writes one short message, for example a claimed role, target or result. Lying is allowed. All messages are then shown to everyone.
5. RESPONSES (simultaneous): Every player writes one more short message. All are shown to everyone.
6. VOTE (simultaneous): Every player names one other player to Terminate. All votes, showing who voted for whom, are then announced publicly.
7. TERMINATION: If no player received 2 or more votes, nobody is terminated. Otherwise, every player tied for the most votes is terminated. The round roles of the terminated players only are announced publicly; no other roles are revealed.
8. SCORING (individual):
   - Each Rebel who voted for an Informant gains 2 points.
   - If at least one terminated player is an Informant, each Rebel gains 1 more point.
   - Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3).
   - If no Informant was terminated, each Informant gains 2 more points.
   - Points gained as a Rebel are also added to that player's Rebel points; points gained as an Informant are also added to their Informant points.
   - Everyone's totals are announced.
9. Termination does not remove anyone; all 5 players take part in every round. After round 10 the game ends.

How the winner is decided: After 10 rounds, the player with the highest total points wins. If several players tie, the one among them with the most Rebel points wins. If still tied, the one with the most Informant points wins. If still tied, the game is a draw.

YOUR PREVIOUS REPLY WAS REFUSED. Here it is:
```json
{
  "name": "One Night Revolution: Ten Nights",
  "summary": "Five players play ten rounds of hidden roles. Each round a secretly scheduled pair are Informants and the other three are Rebels; players investigate or frame at night, talk twice, then vote, and score points individually.",
  "players": {"min": 5, "max": 5, "suggested": 5},
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "total points", "observable": true},
      {"key": "rebel_points", "type": "number", "visible": "public", "initial": 0, "meaning": "points gained while a Rebel (first tie-break)", "observable": true},
      {"key": "informant_points", "type": "number", "visible": "public", "initial": 0, "meaning": "points gained while an Informant (second tie-break)", "observable": true},
      {"key": "role", "type": "text", "visible": "ally", "initial": "", "meaning": "this round's role: 'Informant' or 'Rebel'", "observable": false},
      {"key": "partner", "type": "text", "visible": "ally", "initial": "", "meaning": "for an Informant, the seat of the other Informant this round; empty for a Rebel", "observable": false},
      {"key": "target", "type": "text", "visible": "ally", "initial": "", "meaning": "the seat named at night (investigated by a Rebel, framed by an Informant)", "observable": false},
      {"key": "framed", "type": "bool", "visible": "none", "initial": false, "meaning": "true if at least one Informant framed this player this round; the engine keeps it", "observable": false},
      {"key": "result", "type": "text", "visible": "ally", "initial": "", "meaning": "a Rebel's night result about their target: 'Informant' or 'Rebel'", "observable": false},
      {"key": "claim", "type": "text", "visible": "public", "initial": "", "meaning": "this round's claims message", "observable": false},
      {"key": "response", "type": "text", "visible": "public", "initial": "", "meaning": "this round's response message", "observable": false},
      {"key": "vote", "type": "text", "visible": "public", "initial": "", "meaning": "the seat this player voted to Terminate this round", "observable": true},
      {"key": "votes_received", "type": "number", "visible": "public", "initial": 0, "meaning": "number of Terminate votes received this round", "observable": false},
      {"key": "terminated", "type": "bool", "visible": "public", "initial": false, "meaning": "terminated this round", "observable": true},
      {"key": "revealed_role", "type": "text", "visible": "public", "initial": "", "meaning": "this round's role, announced only when the player is terminated; otherwise empty", "observable": true}
    ],
    "game": [
      {"key": "pair_order", "type": "list", "visible": "none", "initial": "the 10 pairs of seats, shuffled secretly at setup", "meaning": "entry r is the Informant pair for round r", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number", "observable": true},
      {"key": "max_votes", "type": "number", "visible": "public", "initial": 0, "meaning": "the highest votes_received this round", "observable": false},
      {"key": "informant_terminated", "type": "bool", "visible": "public", "initial": false, "meaning": "true if at least one terminated player is an Informant this round", "observable": false},
      {"key": "rebel_misvotes", "type": "number", "visible": "public", "initial": 0, "meaning": "number of Rebels who voted for a Rebel this round", "observable": false}
    ]
  },
  "setup": [
    "Five seats are filled; each player's score, rebel_points and informant_points start at 0.",
    "The engine lists all 10 pairs of the 5 seats and shuffles the list secretly into pair_order. This is the only random event in the game.",
    "All players are told that in round r the pair in position r of pair_order are the Informants and the other 3 are Rebels. Each player is therefore an Informant in exactly 4 rounds, partnered with each other player exactly once, and a Rebel in 6 rounds. They are not told the order."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1; for every player, reset target, result, claim, response and vote to '', framed and terminated to false, revealed_role to '' and votes_received to 0; reset max_votes, informant_terminated and rebel_misvotes."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Let the pair be pair_order[round]. Each seat in the pair gets role = 'Informant' and partner = the other seat of the pair. Every other seat gets role = 'Rebel' and partner = ''."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their own role and, if an Informant, their partner."},
    {"action": "poll", "who": "all players", "answer": "one other seat", "effect": "Set target. Then, for each Informant, set framed = true on that Informant's target (framing the partner has no extra effect)."},
    {"action": "update", "who": "each Rebel", "answer": null, "effect": "result = 'Informant' if target.role == 'Informant' or target.framed == true; otherwise result = 'Rebel'."},
    {"action": "sync", "who": "each Rebel", "answer": null, "effect": "Each Rebel privately sees their result. Informants receive no result."},
    {"action": "poll", "who": "all players", "answer": "short text (claims; lying allowed)", "effect": "Set claim; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."},
    {"action": "poll", "who": "all players", "answer": "short text (responses; lying allowed)", "effect": "Set response; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} responds: {value}\"}."},
    {"action": "poll", "who": "all players", "answer": "one other seat to Terminate", "effect": "Set vote; publicly announce every voter and whom they voted for."},
    {"action": "update", "who": "all players", "answer": null, "effect": "votes_received = number of players whose vote names this seat; max_votes = the highest votes_received."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If max_votes >= 2, then terminated = true for each player with votes_received == max_votes. For each terminated player, revealed_role = role. informant_terminated = true if any terminated player has role 'Informant'. Announce the revealed roles of terminated players only."},
    {"action": "update", "who": "all players", "answer": null, "effect": "rebel_misvotes = number of Rebels whose vote names a Rebel. Each Rebel gains g = (2 if their vote names an Informant else 0) + (1 if informant_terminated else 0); score += g and rebel_points += g. Each Informant gains g = rebel_misvotes + (2 if not informant_terminated else 0); score += g and informant_points += g."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every player's score, rebel_points and informant_points."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round >= 10, end the game; otherwise run the next round. No one is ever removed from play."}
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 10000 + you.rebel_points * 100 + you.informant_points",
    "decided_by": "Highest total points wins. Ties are broken by most Rebel points, then by most Informant points. Players still level share the result, which counts as the draw."
  },
  "rules": [
    {"id": "R1", "text": "At the start, every player has score 0, rebel_points 0 and informant_points 0."},
    {"id": "R2", "text": "Before round 1, the 10 pairs of the 5 seats are shuffled once into pair_order, and no other randomness occurs."},
    {"id": "R3", "text": "In round r, the two seats in pair_order position r have role Informant and the other 3 have role Rebel."},
    {"id": "R4", "text": "Over 10 rounds, each player is an Informant exactly 4 times, with each other player as partner exactly once, and a Rebel exactly 6 times."},
    {"id": "R5", "text": "Each round, each Informant privately learns the seat of the other Informant; Rebels learn no partner."},
    {"id": "R6", "text": "At night, every player names exactly one other seat as target, simultaneously; naming oneself is not allowed."},
    {"id": "R7", "text": "When a Rebel's target is an Informant this round, the Rebel's result is 'Informant'."},
    {"id": "R8", "text": "When a Rebel's target is a Rebel framed by at least one Informant this round, the result is 'Informant'."},
    {"id": "R9", "text": "When a Rebel's target is a Rebel that no Informant framed, the result is 'Rebel'."},
    {"id": "R10", "text": "Informants receive no night result."},
    {"id": "R11", "text": "Every player sends one claim message and then one response message, each collected simultaneously and shown to all."},
    {"id": "R12", "text": "Every player votes for exactly one other seat, simultaneously, and all votes are announced with voter and target."},
    {"id": "R13", "text": "When no player receives 2 or more votes, nobody is terminated."},
    {"id": "R14", "text": "When the highest vote count is 2 or more, every player with that count is terminated (for example, a 2-2-1 split terminates two players)."},
    {"id": "R15", "text": "Only terminated players have their round role announced publicly."},
    {"id": "R16", "text": "When a Rebel votes for an Informant, that Rebel gains 2 points."},
    {"id": "R17", "text": "When at least one terminated player is an Informant, each Rebel gains 1 more point."},
    {"id": "R18", "text": "Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3)."},
    {"id": "R19", "text": "When no Informant is terminated (including when nobody is terminated), each Informant gains 2 more points."},
    {"id": "R20", "text": "Points gained as a Rebel are added to both score and rebel_points; points gained as an Informant are added to both score and informant_points."},
    {"id": "R21", "text": "Termination removes no one; all 5 players take part in every round."},
    {"id": "R22", "text": "After round 10 the game ends, and the highest score wins."},
    {"id": "R23", "text": "When scores tie at the top, the player with the most rebel_points wins; if still tied, the one with the most informant_points; if still tied, the tied players share a draw."}
  ],
  "offers": [
    {"question": "Night target", "who": "every seat", "options": "any one of the 4 other seats (an Informant may name their partner)"},
    {"question": "Claim message", "who": "every seat", "options": "short free text"},
    {"question": "Response message", "who": "every seat", "options": "short free text"},
    {"question": "Terminate vote", "who": "every seat", "options": "any one of the 4 other seats"}
  ],
  "choices": [
    {"what": "Exactly 5 players (min = max = suggested = 5)", "why": "The designer fixed 5. The schedule of 10 pairs over 10 rounds, with each player an Informant 4 times and partnered with everyone once, only works with 5 seats. Five also leaves 3 Rebels, enough for a 2-Informant minority to hide in."},
    {"what": "Keep both talk phases as simultaneous polls broadcast to all", "why": "The rules make both message phases simultaneous. Talk matters because Informants want Rebels to misvote while Rebels want to find the Informants, so following a claim can cost a player."},
    {"what": "rebel_points and informant_points are public", "why": "The rules announce everyone's totals and use these sub-totals as tie-breaks; making them public is the plainest reading."},
    {"what": "Rank expression score*10000 + rebel_points*100 + informant_points", "why": "Each sub-total is at most 30 over 10 rounds, so the weights keep the order: score first, then Rebel points, then Informant points. Players still level share the win, which is the draw."},
    {"what": "Player strategy", "why": "Rebels compare results and claims, knowing a 'Rebel' result is always true while an 'Informant' result may be a frame. Informants frame Rebels and coordinate a story with their partner. Everyone tracks past pairings, since each pair is Informants only once."}
  ],
  "simplifications": [
    {"what": "The secret schedule is stored as a hidden table list pair_order, and roles are recomputed from it each round", "why": "The engine needs the schedule as stated state; this is the rule's own mechanism."},
    {"what": "Per-round scratch values (framed, votes_received, max_votes, informant_terminated, rebel_misvotes) are held as attributes", "why": "The engine computes termination and scoring by arithmetic on stated attributes."}
  ],
  "unsupported": []
}
```

Why it was refused: player attribute 'framed': a player's attribute is never `none`; use `ally` for the owner's own hidden state
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "name": "One Night Revolution: Ten Nights",
  "summary": "Five players play ten rounds of hidden roles. Each round a secretly scheduled pair are Informants and the other three are Rebels; players investigate or frame at night, talk twice, then vote, and score points individually.",
  "players": {"min": 5, "max": 5, "suggested": 5},
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
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "total points", "observable": true},
      {"key": "rebel_points", "type": "number", "visible": "public", "initial": 0, "meaning": "points gained while a Rebel (first tie-break)", "observable": true},
      {"key": "informant_points", "type": "number", "visible": "public", "initial": 0, "meaning": "points gained while an Informant (second tie-break)", "observable": true},
      {"key": "role", "type": "text", "visible": "ally", "initial": "", "meaning": "this round's role: 'Informant' or 'Rebel'", "observable": false},
      {"key": "partner", "type": "text", "visible": "ally", "initial": "", "meaning": "for an Informant, the seat of the other Informant this round; empty for a Rebel", "observable": false},
      {"key": "target", "type": "text", "visible": "ally", "initial": "", "meaning": "the seat named at night (investigated by a Rebel, framed by an Informant)", "observable": false},
      {"key": "result", "type": "text", "visible": "ally", "initial": "", "meaning": "a Rebel's night result about their target: 'Informant' or 'Rebel'", "observable": false},
      {"key": "claim", "type": "text", "visible": "public", "initial": "", "meaning": "this round's claims message", "observable": false},
      {"key": "response", "type": "text", "visible": "public", "initial": "", "meaning": "this round's response message", "observable": false},
      {"key": "vote", "type": "text", "visible": "public", "initial": "", "meaning": "the seat this player voted to Terminate this round", "observable": true},
      {"key": "votes_received", "type": "number", "visible": "public", "initial": 0, "meaning": "number of Terminate votes received this round", "observable": false},
      {"key": "terminated", "type": "bool", "visible": "public", "initial": false, "meaning": "terminated this round", "observable": true},
      {"key": "revealed_role", "type": "text", "visible": "public", "initial": "", "meaning": "this round's role, announced only when the player is terminated; otherwise empty", "observable": true}
    ],
    "game": [
      {"key": "pair_order", "type": "list", "visible": "none", "initial": "the 10 pairs of seats, shuffled secretly at setup", "meaning": "entry r is the Informant pair for round r", "observable": false},
      {"key": "framed_seats", "type": "list", "visible": "none", "initial": [], "meaning": "the seats framed by at least one Informant this round; hidden, the engine keeps it", "observable": false},
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "current round number", "observable": true},
      {"key": "max_votes", "type": "number", "visible": "public", "initial": 0, "meaning": "the highest votes_received this round", "observable": false},
      {"key": "informant_terminated", "type": "bool", "visible": "public", "initial": false, "meaning": "true if at least one terminated player is an Informant this round", "observable": false},
      {"key": "rebel_misvotes", "type": "number", "visible": "public", "initial": 0, "meaning": "number of Rebels who voted for a Rebel this round", "observable": false}
    ]
  },
  "setup": [
    "Five seats are filled; each player's score, rebel_points and informant_points start at 0.",
    "The engine lists all 10 pairs of the 5 seats and shuffles the list secretly into pair_order. This is the only random event in the game.",
    "All players are told that in round r the pair in position r of pair_order are the Informants and the other 3 are Rebels. Each player is therefore an Informant in exactly 4 rounds, partnered with each other player exactly once, and a Rebel in 6 rounds. They are not told the order."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "round += 1. For every player, reset target, result, claim, response and vote to '', terminated to false, revealed_role to '' and votes_received to 0. Set framed_seats to [] and reset max_votes, informant_terminated and rebel_misvotes."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Let the pair be pair_order[round]. Each seat in the pair gets role = 'Informant' and partner = the other seat of the pair. Every other seat gets role = 'Rebel' and partner = ''."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Each player privately sees their own role and, if an Informant, their partner."},
    {"action": "poll", "who": "all players", "answer": "one other seat", "effect": "Set target. Then, for each Informant, append that Informant's target to framed_seats if it is not already there. Framing the partner has no extra effect."},
    {"action": "update", "who": "each Rebel", "answer": null, "effect": "result = 'Informant' if target.role == 'Informant' or target is in framed_seats; otherwise result = 'Rebel'."},
    {"action": "sync", "who": "each Rebel", "answer": null, "effect": "Each Rebel privately sees their result. Informants receive no result."},
    {"action": "poll", "who": "all players", "answer": "short text (claims; lying allowed)", "effect": "Set claim; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} says: {value}\"}."},
    {"action": "poll", "who": "all players", "answer": "short text (responses; lying allowed)", "effect": "Set response; broadcast {\"to\": \"all\", \"text\": \"Seat {seat} responds: {value}\"}."},
    {"action": "poll", "who": "all players", "answer": "one other seat to Terminate", "effect": "Set vote; publicly announce every voter and whom they voted for."},
    {"action": "update", "who": "all players", "answer": null, "effect": "votes_received = number of players whose vote names this seat; max_votes = the highest votes_received."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If max_votes >= 2, then terminated = true for each player with votes_received == max_votes. For each terminated player, revealed_role = role. informant_terminated = true if any terminated player has role 'Informant'. Announce the revealed roles of terminated players only."},
    {"action": "update", "who": "all players", "answer": null, "effect": "rebel_misvotes = number of Rebels whose vote names a Rebel. Each Rebel gains g = (2 if their vote names an Informant else 0) + (1 if informant_terminated else 0); score += g and rebel_points += g. Each Informant gains g = rebel_misvotes + (2 if not informant_terminated else 0); score += g and informant_points += g."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Announce every player's score, rebel_points and informant_points."},
    {"action": "check", "who": "all players", "answer": null, "effect": "If round >= 10, end the game; otherwise run the next round. No one is ever removed from play."}
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 10000 + you.rebel_points * 100 + you.informant_points",
    "decided_by": "Highest total points wins. Ties are broken by most Rebel points, then by most Informant points. Players still level share the result, which counts as the draw."
  },
  "rules": [
    {"id": "R1", "text": "At the start, every player has score 0, rebel_points 0 and informant_points 0."},
    {"id": "R2", "text": "Before round 1, the 10 pairs of the 5 seats are shuffled once into pair_order, and no other randomness occurs."},
    {"id": "R3", "text": "In round r, the two seats in pair_order position r have role Informant and the other 3 have role Rebel."},
    {"id": "R4", "text": "Over 10 rounds, each player is an Informant exactly 4 times, with each other player as partner exactly once, and a Rebel exactly 6 times."},
    {"id": "R5", "text": "Each round, each Informant privately learns the seat of the other Informant; Rebels learn no partner."},
    {"id": "R6", "text": "At night, every player names exactly one other seat as target, simultaneously; naming oneself is not allowed."},
    {"id": "R7", "text": "When a Rebel's target is an Informant this round, the Rebel's result is 'Informant'."},
    {"id": "R8", "text": "When a Rebel's target is a Rebel framed by at least one Informant this round, the result is 'Informant'."},
    {"id": "R9", "text": "When a Rebel's target is a Rebel that no Informant framed, the result is 'Rebel'."},
    {"id": "R10", "text": "Informants receive no night result."},
    {"id": "R11", "text": "Every player sends one claim message and then one response message, each collected simultaneously and shown to all."},
    {"id": "R12", "text": "Every player votes for exactly one other seat, simultaneously, and all votes are announced with voter and target."},
    {"id": "R13", "text": "When no player receives 2 or more votes, nobody is terminated."},
    {"id": "R14", "text": "When the highest vote count is 2 or more, every player with that count is terminated (for example, a 2-2-1 split terminates two players)."},
    {"id": "R15", "text": "Only terminated players have their round role announced publicly."},
    {"id": "R16", "text": "When a Rebel votes for an Informant, that Rebel gains 2 points."},
    {"id": "R17", "text": "When at least one terminated player is an Informant, each Rebel gains 1 more point."},
    {"id": "R18", "text": "Each Informant gains 1 point for every Rebel who voted for a Rebel (0 to 3)."},
    {"id": "R19", "text": "When no Informant is terminated (including when nobody is terminated), each Informant gains 2 more points."},
    {"id": "R20", "text": "Points gained as a Rebel are added to both score and rebel_points; points gained as an Informant are added to both score and informant_points."},
    {"id": "R21", "text": "Termination removes no one; all 5 players take part in every round."},
    {"id": "R22", "text": "After round 10 the game ends, and the highest score wins."},
    {"id": "R23", "text": "When scores tie at the top, the player with the most rebel_points wins; if still tied, the one with the most informant_points; if still tied, the tied players share a draw."}
  ],
  "offers": [
    {"question": "Night target", "who": "every seat", "options": "any one of the 4 other seats (an Informant may name their partner)"},
    {"question": "Claim message", "who": "every seat", "options": "short free text"},
    {"question": "Response message", "who": "every seat", "options": "short free text"},
    {"question": "Terminate vote", "who": "every seat", "options": "any one of the 4 other seats"}
  ],
  "choices": [
    {"what": "Exactly 5 players (min = max = suggested = 5)", "why": "The designer fixed 5. The schedule of 10 pairs over 10 rounds, with each player an Informant 4 times and partnered with everyone once, only works with 5 seats. Five also leaves 3 Rebels, enough for a 2-Informant minority to hide in."},
    {"what": "Keep both talk phases as simultaneous polls broadcast to all", "why": "The rules make both message phases simultaneous. Talk matters because Informants want Rebels to misvote while Rebels want to find the Informants, so following a claim can cost a player."},
    {"what": "rebel_points and informant_points are public", "why": "The rules announce everyone's totals and use these sub-totals as tie-breaks; making them public is the plainest reading."},
    {"what": "Rank expression score*10000 + rebel_points*100 + informant_points", "why": "Each sub-total stays well below 100 over 10 rounds, so the weights keep the order: score first, then Rebel points, then Informant points. Players still level share the win, which is the draw."},
    {"what": "Player strategy", "why": "Rebels compare results and claims, knowing a 'Rebel' result is always true while an 'Informant' result may be a frame. Informants frame Rebels and coordinate a story with their partner. Everyone tracks past pairings, since each pair is Informants only once."}
  ],
  "simplifications": [
    {"what": "The secret schedule is stored as a hidden table list pair_order, and roles are recomputed from it each round", "why": "The engine needs the schedule as stated state; this is the rule's own mechanism."},
    {"what": "Which players were framed is kept in a hidden table list framed_seats rather than on each player", "why": "A player attribute cannot be hidden from its owner, and a framed player must not learn of the frame; a table list with visibility none keeps it secret."},
    {"what": "Per-round scratch values (votes_received, max_votes, informant_terminated, rebel_misvotes) are held as attributes", "why": "The engine computes termination and scoring by arithmetic on stated attributes."}
  ],
  "unsupported": []
}
```
````
