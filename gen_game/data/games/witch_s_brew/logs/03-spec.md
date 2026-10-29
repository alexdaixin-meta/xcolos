# 03 spec

- time: 2026-10-27T22:10:01+00:00 (49.8s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 db3cf461bd7a0ade, reply sha256 5cde5ef1184e6199

## Sent

````
Game: Witch's Brew: Claims
Players in the source: 3 to 5
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
SETUP. N players (3-5) sit in a fixed clockwise order, numbered 1 to N. Everyone starts with 0 points. The game has 3 sets of N rounds each (3N rounds in total).

ROLES. There are six roles, each with a strong reward and a weak reward:
- Witch: strong 5, weak 2.
- Raven Keeper: strong 6, weak 0.
- Alchemist: strong 4, weak 1.
- Druid: strong 3, weak 2.
- Herb Hag: strong 2, weak 1.
- Thief: the strong reward is to take 3 points from the other player with the highest current total (ties go to the tied player first clockwise after the Thief). The Thief gains 3, that player loses 3, and a total may go below 0. Weak 1.

START OF A SET. At the start of each set, every player secretly and simultaneously chooses exactly 3 different roles to hold for that set. Hands are private; the engine records them. The list of roles led this set is emptied.

LEADER. In set k, the first round's leader is player k (set 3 with 3 players: player 3). Leadership then passes clockwise each round, so every player leads exactly once per set.

EACH ROUND:
1. The leader is announced.
2. The leader names one role that has not yet been led in this set. They may name a role they do not hold. The named role is added to this set's led list.
3. Talk: every player at the same time writes one short message without seeing the others. All messages are then shown to everyone. Messages bind no one.
4. Responses: every player other than the leader who holds the named role must respond. All of them choose at the same moment, either CONTEST or YIELD. Players who do not hold it pass automatically.
5. Reveal: all responses are shown, so everyone learns who held the role.
6. Resolve: start from the leader and go clockwise. The leader is the first claimant, and each contester, in clockwise order, takes over the claim. The final claimant is the last contester in clockwise order after the leader, or the leader if nobody contested.
   - The final claimant gets the role's strong reward. Exception: if the final claimant is the leader and the leader does not hold the named role, they get nothing.
   - The leader, if overtaken, gets 0. Every contester overtaken by a later contester gets 0.
   - Every player who yielded gets the role's weak reward.
7. The named role is removed from the hand of the leader (if held) and of every responder. A role cannot be led again this set.
8. Scores are announced and leadership passes clockwise.

Roles held but never led or responded to during a set are simply lost when the set ends. After round 3N, the game ends.

How the winner is decided: After the final round, the player with the highest total points wins. If two or more players tie for the highest total, the game is a draw.
````

## Reply

````
```json
{
  "name": "Witch's Brew: Claims",
  "summary": "Over 3 sets of N rounds, players secretly hold 3 of 6 roles. Each round a leader names a role, holders choose at once to contest or yield, and the last contester clockwise takes the strong reward.",
  "players": {"min": 3, "max": 5, "suggested": 4},
  "parameters": {
    "num_sets": 3,
    "roles_per_hand": 3,
    "role_count": 6,
    "witch_strong": 5,
    "witch_weak": 2,
    "raven_keeper_strong": 6,
    "raven_keeper_weak": 0,
    "alchemist_strong": 4,
    "alchemist_weak": 1,
    "druid_strong": 3,
    "druid_weak": 2,
    "herb_hag_strong": 2,
    "herb_hag_weak": 1,
    "thief_steal": 3,
    "thief_weak": 1,
    "starting_score": 0,
    "overtaken_reward": 0
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Total points. It may go below 0 because of the Thief.", "observable": true},
      {"key": "hand", "type": "list", "visible": "ally", "initial": [], "meaning": "The roles this player holds in the current set: 3 chosen at the start of the set, each removed once led or responded to.", "observable": false},
      {"key": "response", "type": "text", "visible": "public", "initial": "none", "meaning": "This round's response: contest, yield, or none (the player is the leader or does not hold the named role). It is shown to everyone at the reveal.", "observable": true}
    ],
    "game": [
      {"key": "set_number", "type": "number", "visible": "public", "initial": 1, "meaning": "The current set, from 1 to 3.", "observable": false},
      {"key": "round_in_set", "type": "number", "visible": "public", "initial": 1, "meaning": "The round within the current set, from 1 to N.", "observable": false},
      {"key": "round_count", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds completed so far.", "observable": false},
      {"key": "leader_seat", "type": "number", "visible": "public", "initial": 1, "meaning": "The seat leading this round.", "observable": false},
      {"key": "named_role", "type": "text", "visible": "public", "initial": "", "meaning": "The role named by the leader this round.", "observable": true},
      {"key": "led_list", "type": "list", "visible": "public", "initial": [], "meaning": "The roles already led in the current set.", "observable": false},
      {"key": "leader_holds", "type": "bool", "visible": "none", "initial": false, "meaning": "Whether the named role was in the leader's hand when it was named.", "observable": false},
      {"key": "final_claimant", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat that ends up with the claim this round.", "observable": false},
      {"key": "thief_target", "type": "number", "visible": "public", "initial": 0, "meaning": "The seat robbed by a strong Thief reward this round.", "observable": false}
    ]
  },
  "setup": [
    "Seats are numbered 1 to N clockwise, with N from 3 to 5.",
    "Every player's score is set to 0.",
    "set_number = 1, round_in_set = 1, round_count = 0, and led_list is empty."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "When round_in_set == 1: empty every player's hand (roles left unused from the previous set are lost) and empty led_list."},
    {"action": "poll", "who": "all players", "answer": "One of the 20 combinations of 3 different roles from {Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief}", "effect": "When round_in_set == 1: set each player's hand to the 3 roles in the chosen combination. Hands stay private (ally)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set leader_seat = ((set_number - 1) + (round_in_set - 1)) mod N + 1 and set every player's response to 'none'. Announce: 'Seat {leader_seat} leads this round.'"},
    {"action": "ask", "who": "seat leader_seat", "answer": "One role from {Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief} that is not in led_list", "effect": "Set named_role to the chosen role and append it to led_list. Set leader_holds = (named_role is in the leader's hand). Announce the named role."},
    {"action": "poll", "who": "all players", "answer": "Short text message", "effect": "Broadcast to all: 'Seat {seat} says: {value}'. Nothing binds."},
    {"action": "poll", "who": "each player other than leader_seat whose hand contains named_role", "answer": "contest | yield", "effect": "Set response to 'contest' or 'yield'. Players who do not hold the role keep 'none' (an automatic pass)."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal every seat's response, which shows who held named_role."},
    {"action": "update", "who": "all players", "answer": null, "effect": "If any player's response == 'contest', set final_claimant to the contester with the largest (seat - leader_seat) mod N. Otherwise set final_claimant = leader_seat."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Strong reward. If final_claimant != leader_seat or leader_holds is true, then: if named_role is not Thief, final_claimant's score += that role's strong value (Witch 5, Raven Keeper 6, Alchemist 4, Druid 3, Herb Hag 2). If named_role is Thief, set thief_target to the seat other than final_claimant with the highest score (ties go to the smallest (seat - final_claimant) mod N), then final_claimant's score += 3 and thief_target's score -= 3. If final_claimant == leader_seat and leader_holds is false, nobody gets the strong reward. The overtaken leader and overtaken contesters get 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Weak reward: every player with response == 'yield' gets score += the weak value of named_role (Witch 2, Raven Keeper 0, Alchemist 1, Druid 2, Herb Hag 1, Thief 1)."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Remove named_role from the hand of leader_seat (if held) and from the hand of every player whose response != 'none'."},
    {"action": "update", "who": "all players", "answer": null, "effect": "round_count += 1 and round_in_set += 1. If round_in_set > N, set round_in_set = 1 and set_number += 1. Announce all scores."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round_count >= 3 * N; otherwise continue."}
  ],
  "ending": {
    "condition": "round_count >= 3 * N",
    "rank_by": "you.score",
    "decided_by": "Each player's total score. The highest total wins, and players tied for the highest share the result (the source calls this a draw)."
  },
  "rules": [
    {"id": "R1", "text": "When the game starts, every player has score 0."},
    {"id": "R2", "text": "When round_in_set is 1, every player simultaneously chooses exactly 3 different roles, and these become their hand, replacing any roles left from the previous set."},
    {"id": "R3", "text": "When a new set begins, led_list is emptied."},
    {"id": "R4", "text": "When round r of set k is played, the leader is seat ((k-1)+(r-1)) mod N + 1, so set 1 starts with seat 1, set 2 with seat 2 and set 3 with seat 3."},
    {"id": "R5", "text": "When the leader names a role, it must not already be in led_list; it may be a role the leader does not hold, and it is appended to led_list."},
    {"id": "R6", "text": "When the role is named, every player submits one short message simultaneously, and all messages are then shown to everyone."},
    {"id": "R7", "text": "When a non-leader holds the named role, they must choose contest or yield simultaneously with the other holders; non-holders and the leader have response 'none'."},
    {"id": "R8", "text": "When responses are in, all responses are revealed to everyone."},
    {"id": "R9", "text": "When at least one player contests, the final claimant is the contester furthest clockwise from the leader (largest (seat - leader) mod N); otherwise the final claimant is the leader."},
    {"id": "R10", "text": "When the final claimant is not the leader, or is the leader and holds the named role, they gain the strong reward: Witch 5, Raven Keeper 6, Alchemist 4, Druid 3, Herb Hag 2."},
    {"id": "R11", "text": "When the final claimant is the leader and the leader does not hold the named role, nobody gains the strong reward."},
    {"id": "R12", "text": "When the strong Thief reward is given, the claimant gains 3 and the other player with the highest score loses 3 (ties go to the first tied seat clockwise after the claimant), and a score may go below 0."},
    {"id": "R13", "text": "When the leader or a contester is overtaken by a later contester, they gain 0 points."},
    {"id": "R14", "text": "When a player yields, they gain the weak reward: Witch 2, Raven Keeper 0, Alchemist 1, Druid 2, Herb Hag 1, Thief 1."},
    {"id": "R15", "text": "When a round resolves, the named role is removed from the leader's hand (if held) and from the hand of every player who contested or yielded."},
    {"id": "R16", "text": "When round_count reaches 3*N, the game ends, and the highest score wins, with tied top scores sharing the result."}
  ],
  "offers": [
    {"question": "Choose roles for the set (when round_in_set == 1)", "who": "all players", "options": "Any of the 20 combinations of 3 different roles from Witch, Raven Keeper, Alchemist, Druid, Herb Hag, Thief"},
    {"question": "Name a role", "who": "seat leader_seat", "options": "Every role not in led_list, whether held or not"},
    {"question": "Talk", "who": "all players", "options": "One short free-text message"},
    {"question": "Respond to the named role", "who": "each non-leader seat holding named_role", "options": "A holder other than the leader: contest, yield. The leader and non-holders are not asked."}
  ],
  "choices": [
    {"what": "3 to 5 players, suggested 4", "why": "The designer chose 4 and the source range is 3 to 5. Three is the minimum so that claim order and contest bluffing matter; more than 5 would exceed the 6 roles, which could run out within a set."},
    {"what": "Hand choice offered as one pick from the 20 three-role combinations", "why": "This guarantees exactly 3 different roles in a single simultaneous answer."},
    {"what": "Talk kept as a simultaneous poll, broadcast to all", "why": "The rules specify simultaneous messages. Players disagree about who should claim, so bluffing about holdings is meaningful."},
    {"what": "Leader formula ((set_number-1)+(round_in_set-1)) mod N + 1", "why": "This matches 'set k starts with player k' and clockwise passing; with 3 players set 3 starts with player 3."},
    {"what": "Thief tie-break uses the first tied seat clockwise from the final claimant", "why": "The final claimant is the one using the Thief's reward."}
  ],
  "simplifications": [
    {"what": "A tie for the top score is a shared win rather than a declared draw", "why": "The engine has no separate draw; tied top players share the win."},
    {"what": "Roles left in a hand at the end of a set are discarded by emptying hands at the start of the next set", "why": "This has the same effect as losing them at the end of the set."}
  ],
  "unsupported": []
}
```
````
