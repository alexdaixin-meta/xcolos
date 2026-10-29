# 19 spec

- time: 2026-10-28T04:29:47+00:00 (34.7s)  model: claude-opus-5-5
- system prompt: [system/bc335988-spec.md](system/bc335988-spec.md) (sha256 bc335988cecc1ece)
- sent sha256 353cddfd5a940fb3, reply sha256 e197f0e76b4113df

## Sent

````
Game: Go Nuts for Donuts: Secret Budget
Players in the source: 4 to 4
Suggested table size, chosen by the designer of these rules (keep it): 4

Rules, as filed in the inventory:
PLAYERS AND DONUTS. Exactly 4 players. Every round the same five donuts are offered: Glazed (9 points), Jelly (6 points), Cruller (4 points), Sprinkle (2 points), Plain (1 point). There are no cards, deck or random events.

STARTING STATE. Every player starts with score 0, donuts 0, glazed_used 0, jelly_used 0. The game lasts exactly 10 rounds.

SECRET SPLIT (once, before round 1). Each player has 6 premium picks for the whole game. All players are asked at the same time: 'How many of your 6 premium picks are Glazed picks?' The options are exactly the whole numbers 0, 1, 2, 3, 4, 5, 6. The answer is stored as that player's split_g and is visible only to that player. That player then has split_g Glazed picks and (6 - split_g) Jelly picks. split_g is set by this poll only and is never changed by any later step. No step resets glazed_used or jelly_used except as stated below.

EACH ROUND:
1. TALK. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages bind no one.
2. CHOOSE. All players choose at the same time one of: Glazed, Jelly, Cruller, Sprinkle, Plain. Before choosing, each player is privately reminded of their own Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used).
3. VOID CHECK. A player's choice is void if and only if (a) they chose Glazed and glazed_used >= split_g, or (b) they chose Jelly and jelly_used >= 6 - split_g. Every other choice is not void. Cruller, Sprinkle and Plain are never void.
4. COUNT. For each donut, count how many players made a NON-VOID choice of it. Void choices are not counted for any donut.
5. AWARD. For each donut, if exactly 1 player made a non-void choice of it, that player adds the donut's points to their score and adds 1 to donuts. If 2 or more players made a non-void choice of it, it is discarded and none of them gains anything for it. A void choice gains 0.
6. USE PICKS. Every player who made a non-void Glazed choice adds 1 to glazed_used. Every player who made a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded. A void choice uses nothing.
7. REVEAL. Everyone is shown every player's choice (marked VOID if void), what each player gained this round, and all scores and donut counts. Nobody's split_g is ever shown.
8. END CHECK. After round 10 the game ends.

How the winner is decided: After round 10, the player with the highest score wins. If several are tied on score, the one among them with the most donuts wins (rank value = score x 100 + donuts). If players are still tied on both, the game is a draw among them.
````

## Reply

````
```json
{
  "name": "Go Nuts for Donuts: Secret Budget",
  "summary": "Four players spend 10 simultaneous rounds picking one of five donuts. A donut scores only for a player who picks it alone, and each player has a secret split of 6 premium picks between Glazed and Jelly.",
  "players": {"min": 4, "max": 4, "suggested": 4},
  "parameters": {
    "glazed_points": 9,
    "jelly_points": 6,
    "cruller_points": 4,
    "sprinkle_points": 2,
    "plain_points": 1,
    "rounds": 10,
    "premium_picks": 6,
    "split_g_min": 0,
    "split_g_max": 6,
    "rank_score_multiplier": 100
  },
  "attributes": {
    "player": [
      {"key": "score", "type": "number", "visible": "public", "initial": 0, "meaning": "Points from donuts won alone", "observable": true},
      {"key": "donuts", "type": "number", "visible": "public", "initial": 0, "meaning": "Number of donuts won", "observable": true},
      {"key": "split_g", "type": "number", "visible": "ally", "initial": 0, "meaning": "Secret number of the 6 premium picks that are Glazed picks. Jelly picks are 6 - split_g. Set once by the split poll and never changed.", "observable": false},
      {"key": "glazed_used", "type": "number", "visible": "public", "initial": 0, "meaning": "Non-void Glazed choices made so far", "observable": false},
      {"key": "jelly_used", "type": "number", "visible": "public", "initial": 0, "meaning": "Non-void Jelly choices made so far", "observable": false},
      {"key": "choice", "type": "text", "visible": "public", "initial": "", "meaning": "This round's donut choice, gathered by a simultaneous poll and shown at the reveal", "observable": false},
      {"key": "void", "type": "bool", "visible": "public", "initial": false, "meaning": "Whether this round's choice is void", "observable": false},
      {"key": "gained", "type": "number", "visible": "public", "initial": 0, "meaning": "Points gained this round", "observable": false}
    ],
    "game": [
      {"key": "round", "type": "number", "visible": "public", "initial": 0, "meaning": "Rounds completed", "observable": false},
      {"key": "count_glazed", "type": "number", "visible": "public", "initial": 0, "meaning": "Non-void Glazed choices this round", "observable": false},
      {"key": "count_jelly", "type": "number", "visible": "public", "initial": 0, "meaning": "Non-void Jelly choices this round", "observable": false},
      {"key": "count_cruller", "type": "number", "visible": "public", "initial": 0, "meaning": "Cruller choices this round", "observable": false},
      {"key": "count_sprinkle", "type": "number", "visible": "public", "initial": 0, "meaning": "Sprinkle choices this round", "observable": false},
      {"key": "count_plain", "type": "number", "visible": "public", "initial": 0, "meaning": "Plain choices this round", "observable": false}
    ]
  },
  "setup": [
    "Initialize every player with score 0, donuts 0, split_g 0, glazed_used 0 and jelly_used 0, and set round to 0.",
    "Poll all players at once: 'How many of your 6 premium picks are Glazed picks?' The options are 0, 1, 2, 3, 4, 5 and 6. Store each answer as that player's split_g, visible only to that player.",
    "Sync each player their own state."
  ],
  "round": [
    {"action": "update", "who": "all players", "answer": null, "effect": "Reset each player's choice to empty, void to false and gained to 0. Reset count_glazed, count_jelly, count_cruller, count_sprinkle and count_plain to 0."},
    {"action": "poll", "who": "all players", "answer": "one short text message", "effect": "Gather all messages at once, then broadcast to all: 'Seat {seat} says: {value}'. Messages bind no one."},
    {"action": "sync", "who": "all players", "answer": null, "effect": "Privately remind each player of their Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used)."},
    {"action": "poll", "who": "all players", "answer": "one of: Glazed, Jelly, Cruller, Sprinkle, Plain", "effect": "Store each answer in that player's choice."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set void = true if (choice == Glazed and glazed_used >= split_g) or (choice == Jelly and jelly_used >= 6 - split_g). Otherwise set void = false."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Set count_glazed to the number of players with choice Glazed and not void, and count_jelly to the number with choice Jelly and not void. Set count_cruller, count_sprinkle and count_plain to the number of players who chose each."},
    {"action": "update", "who": "all players", "answer": null, "effect": "For each non-void player whose donut's count == 1, set gained to that donut's points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), add gained to score and add 1 to donuts. Every other player gets gained 0."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Every player with a non-void Glazed choice adds 1 to glazed_used. Every player with a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded."},
    {"action": "tell", "who": "all players", "answer": null, "effect": "Reveal each player's choice (marked VOID if void), gained, score and donuts. split_g is never shown."},
    {"action": "update", "who": "all players", "answer": null, "effect": "Add 1 to round."},
    {"action": "check", "who": "all players", "answer": null, "effect": "End the game if round >= 10. Otherwise continue with the next round."}
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 100 + you.donuts",
    "decided_by": "The highest score wins, with ties broken by most donuts won. Players still level on both share the win, which is a draw among them."
  },
  "rules": [
    {"id": "R1", "text": "Before round 1, each player's answer to the split poll (0 to 6) is stored as split_g, visible only to that player, and is never changed afterwards."},
    {"id": "R2", "text": "When a player has split_g = s, they have s Glazed picks and 6 - s Jelly picks."},
    {"id": "R3", "text": "Each round, every player sends one message at the same time, and all messages are shown to everyone only after all are in."},
    {"id": "R4", "text": "Before choosing, each player is privately told split_g - glazed_used Glazed picks left and 6 - split_g - jelly_used Jelly picks left."},
    {"id": "R5", "text": "When a player chooses Glazed while glazed_used >= split_g, the choice is void, gains 0 and does not count toward Glazed."},
    {"id": "R6", "text": "When a player chooses Jelly while jelly_used >= 6 - split_g, the choice is void, gains 0 and does not count toward Jelly."},
    {"id": "R7", "text": "When a player chooses Cruller, Sprinkle or Plain, the choice is never void."},
    {"id": "R8", "text": "When exactly 1 player makes a non-void choice of a donut, that player gains its points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1) and adds 1 to donuts."},
    {"id": "R9", "text": "When 2 or more players make a non-void choice of the same donut, none of them gains points or donuts for it."},
    {"id": "R10", "text": "When a player makes a non-void Glazed choice, glazed_used rises by 1 whether the donut was won or discarded."},
    {"id": "R11", "text": "When a player makes a non-void Jelly choice, jelly_used rises by 1 whether the donut was won or discarded."},
    {"id": "R12", "text": "When a choice is void, glazed_used and jelly_used do not change."},
    {"id": "R13", "text": "When a void choice of Glazed is made alongside one non-void Glazed choice, the non-void player still wins the Glazed for 9 points."},
    {"id": "R14", "text": "After each round, every player's choice (marked VOID if void), gain, score and donuts are shown to everyone, and split_g is never shown."},
    {"id": "R15", "text": "When round 10 ends, the game ends."},
    {"id": "R16", "text": "At the end, the player with the highest score * 100 + donuts wins, and players tied on that value share the win."}
  ],
  "offers": [
    {"question": "Secret split: how many of your 6 premium picks are Glazed picks?", "who": "all players, at once, before round 1", "options": "0, 1, 2, 3, 4, 5, 6"},
    {"question": "Talk", "who": "all players, at once, each round", "options": "one short free-text message"},
    {"question": "Choose a donut", "who": "all players, at once, each round", "options": "Glazed, Jelly, Cruller, Sprinkle, Plain, always all five, even with no picks left (such a choice is then void)"}
  ],
  "choices": [
    {"what": "Exactly 4 players, suggested 4", "why": "The rules fix the table at 4 and the designer chose it. Five donuts for four players makes collisions frequent but avoidable, which is what the game is about."},
    {"what": "Keep simultaneous talk each round, built as a poll and then a broadcast", "why": "The rules require it. Players disagree about who should take the high donuts, so talk can be used to bluff about one's remaining budget or to stake claims."},
    {"what": "glazed_used and jelly_used are public", "why": "The reveal shows every choice and whether it was void, so these counts can be deduced by anyone. Only split_g stays secret."},
    {"what": "Per-donut counters and the per-player choice, void and gained fields as attributes", "why": "The void check, the count and the award need state to work on. These are reset at the start of each round."},
    {"what": "Rank value score * 100 + donuts", "why": "This is given by the rules. Donuts can never exceed 10, so the score always dominates the tie-break."}
  ],
  "simplifications": [
    {"what": "The private reminder of picks left is delivered as a sync of each player's own state, with the computed values", "why": "The engine sends private state through sync. This has the same effect as the rule's reminder."}
  ],
  "unsupported": []
}
```
````
