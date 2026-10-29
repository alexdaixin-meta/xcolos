# 07 scenarios

- time: 2026-10-28T04:20:08+00:00 (70.6s)  model: claude-opus-5-5
- system prompt: [system/6dcf03e1-scenarios.md](system/6dcf03e1-scenarios.md) (sha256 6dcf03e15fe36c21)
- sent sha256 a35f592bcde214a5, reply sha256 9a6d5a4921846398

## Sent

````
SPEC:
{
  "name": "Go Nuts for Donuts: Premium Picks",
  "summary": "Four players secretly split 6 premium picks between Glazed and Jelly, then for 10 rounds talk and simultaneously pick one of five donuts; a donut scores only for a lone chooser.",
  "players": {
    "min": 4,
    "max": 4,
    "suggested": 4
  },
  "parameters": {
    "player_count": 4,
    "rounds": 10,
    "glazed_value": 9,
    "jelly_value": 6,
    "cruller_value": 4,
    "sprinkle_value": 2,
    "plain_value": 1,
    "premium_picks_total": 6,
    "split_min": 0,
    "split_max": 6,
    "lone_chooser_count": 1,
    "donut_collected_increment": 1,
    "pick_use_per_choice": 1,
    "tiebreak_multiplier": 100
  },
  "attributes": {
    "player": [
      {
        "key": "score",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points total",
        "observable": true
      },
      {
        "key": "donuts",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "donuts collected (won as lone chooser)",
        "observable": true
      },
      {
        "key": "glazed_picks",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Glazed picks remaining (G at start); never told to others",
        "observable": false
      },
      {
        "key": "jelly_picks",
        "type": "number",
        "visible": "ally",
        "initial": 0,
        "meaning": "Jelly picks remaining (6 - G at start); never told to others",
        "observable": false
      },
      {
        "key": "glazed_used",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "non-void Glazed choices made so far (announced each round)",
        "observable": true
      },
      {
        "key": "jelly_used",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "non-void Jelly choices made so far (announced each round)",
        "observable": true
      },
      {
        "key": "choice",
        "type": "text",
        "visible": "ally",
        "initial": "",
        "meaning": "this round's donut choice, secret until the reveal",
        "observable": false
      },
      {
        "key": "void",
        "type": "bool",
        "visible": "public",
        "initial": false,
        "meaning": "this round's choice was VOID (Glazed with 0 glazed_picks or Jelly with 0 jelly_picks)",
        "observable": true
      },
      {
        "key": "gain",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "points gained this round",
        "observable": false
      }
    ],
    "game": [
      {
        "key": "round",
        "type": "number",
        "visible": "public",
        "initial": 0,
        "meaning": "current round number (1 to 10)",
        "observable": true
      }
    ]
  },
  "setup": [
    "Every player starts with score 0, donuts 0, glazed_used 0 and jelly_used 0.",
    "All players are polled at once, privately, for a whole number G from 0 to 6.",
    "Each player's glazed_picks is set to G and jelly_picks to 6 - G. Only the owner sees these values, and nobody else is ever told G."
  ],
  "round": [
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "round += 1"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce the round number and, for every seat, score, donuts, glazed_used and jelly_used. Remaining picks are not announced."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "short text message",
      "effect": "Every message is broadcast to all once all are in: 'Seat {seat} says: {value}'. Messages are not binding."
    },
    {
      "action": "poll",
      "who": "all players",
      "answer": "one of: Glazed, Jelly, Cruller, Sprinkle, Plain",
      "effect": "choice = answer (secret until the reveal)"
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "void = (choice == 'Glazed' and glazed_picks == 0) or (choice == 'Jelly' and jelly_picks == 0); gain = 0"
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Reveal every seat's choice together, with VOID shown for each seat whose void is true."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "For each donut D, let n_D = the number of seats with choice == D and void == false. A seat with void == false whose choice D has n_D == 1 gets gain = value of D (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), score += gain and donuts += 1. When n_D >= 2, nobody gains from D."
    },
    {
      "action": "update",
      "who": "all players",
      "answer": null,
      "effect": "If void == false and choice == 'Glazed': glazed_picks -= 1 and glazed_used += 1. If void == false and choice == 'Jelly': jelly_picks -= 1 and jelly_used += 1. This applies whether the donut was won or discarded."
    },
    {
      "action": "tell",
      "who": "all players",
      "answer": null,
      "effect": "Announce each seat's gain this round and every seat's new score and donuts."
    },
    {
      "action": "check",
      "who": "all players",
      "answer": null,
      "effect": "End the game if round >= 10, otherwise continue."
    }
  ],
  "ending": {
    "condition": "round >= 10",
    "rank_by": "you.score * 100 + you.donuts",
    "decided_by": "Highest point total wins. Among players tied on points, the one with the most donuts collected wins. Players still tied share the win, which stands for the source's draw."
  },
  "rules": [
    {
      "id": "R1",
      "text": "When the game starts, every player has score 0, donuts 0, glazed_used 0 and jelly_used 0."
    },
    {
      "id": "R2",
      "text": "When a player answers G (a whole number from 0 to 6) before round 1, then glazed_picks = G and jelly_picks = 6 - G, visible only to that player."
    },
    {
      "id": "R3",
      "text": "No player other than the owner is ever shown that player's G, glazed_picks or jelly_picks."
    },
    {
      "id": "R4",
      "text": "When each round begins, round increases by 1, and the round number plus every seat's score, donuts, glazed_used and jelly_used are announced."
    },
    {
      "id": "R5",
      "text": "When the talk step runs, every player submits one short message simultaneously, and all four messages are shown to everyone only after all are in."
    },
    {
      "id": "R6",
      "text": "When the choose step runs, every player simultaneously chooses exactly one of Glazed, Jelly, Cruller, Sprinkle or Plain."
    },
    {
      "id": "R7",
      "text": "When a player chooses Glazed with glazed_picks == 0, or Jelly with jelly_picks == 0, then void = true. Otherwise void = false."
    },
    {
      "id": "R8",
      "text": "When a choice is void, that player gains 0, uses no pick, and is not counted as choosing that donut."
    },
    {
      "id": "R9",
      "text": "When choices are revealed, all four choices are shown together, and each void choice is marked VOID."
    },
    {
      "id": "R10",
      "text": "When exactly one non-void player chooses Glazed, that player gains 9 points and donuts += 1."
    },
    {
      "id": "R11",
      "text": "When exactly one non-void player chooses Jelly, that player gains 6 points and donuts += 1."
    },
    {
      "id": "R12",
      "text": "When exactly one non-void player chooses Cruller, that player gains 4 points and donuts += 1."
    },
    {
      "id": "R13",
      "text": "When exactly one non-void player chooses Sprinkle, that player gains 2 points and donuts += 1."
    },
    {
      "id": "R14",
      "text": "When exactly one non-void player chooses Plain, that player gains 1 point and donuts += 1."
    },
    {
      "id": "R15",
      "text": "When two or more non-void players choose the same donut, each of them gains 0 for it and donuts is unchanged."
    },
    {
      "id": "R16",
      "text": "When a player makes a non-void Glazed choice, glazed_picks decreases by 1 and glazed_used increases by 1, whether the donut was won or discarded."
    },
    {
      "id": "R17",
      "text": "When a player makes a non-void Jelly choice, jelly_picks decreases by 1 and jelly_used increases by 1, whether the donut was won or discarded."
    },
    {
      "id": "R18",
      "text": "When a round ends, each seat's gain and new score and donuts totals are announced."
    },
    {
      "id": "R19",
      "text": "When round 10 has been resolved, the game ends, and unused picks are worth 0."
    },
    {
      "id": "R20",
      "text": "When the game ends, the highest score wins. A tie on score is broken by the most donuts, and players still tied share the win."
    }
  ],
  "offers": [
    {
      "question": "Secret split before round 1: how many Glazed picks G?",
      "who": "every seat",
      "options": "a whole number from 0 to 6"
    },
    {
      "question": "Talk: your message this round",
      "who": "every seat",
      "options": "a short free-text message"
    },
    {
      "question": "Choose a donut",
      "who": "every seat",
      "options": "Glazed, Jelly, Cruller, Sprinkle, Plain, offered in every situation. A Glazed or Jelly choice made with no matching picks left is allowed but void."
    }
  ],
  "choices": [
    {
      "what": "Exactly 4 players (min 4, max 4, suggested 4)",
      "why": "The designer fixed the table at 4. The five-donut row against four choosers is what creates the collision tension, so another count would change the game."
    },
    {
      "what": "Talk kept as a simultaneous poll broadcast to all",
      "why": "The rules specify simultaneous, non-binding messages. Players want different donuts, so claims and bluffs about plans (and hidden pick splits) give real material to reason about."
    },
    {
      "what": "Strategy at the table",
      "why": "A thoughtful player infers others' remaining premium picks from the public glazed_used and jelly_used, times Glazed for rounds when others are likely out, and uses talk to bluff or deter. A thoughtless player always grabs Glazed and collides."
    },
    {
      "what": "Tie-break encoded as score * 100 + donuts",
      "why": "Donuts can never exceed 10, so multiplying the score by 100 keeps points primary and donuts as the tie-break."
    },
    {
      "what": "Glazed and Jelly are always offered, even with no picks left",
      "why": "The rules define void choices as possible outcomes, so the option must exist."
    }
  ],
  "simplifications": [
    {
      "what": "A final draw among tied players is represented as a shared win",
      "why": "The engine has no separate draw: players level at the top share the win, which matches the source's draw among those players."
    }
  ],
  "unsupported": []
}

OBSERVABLE (the only attributes you may assert on): player: score, donuts, glazed_used, jelly_used, void; table: round.
````

## Reply

````
[
{"name": "Every seat starts with score 0, donuts 0, glazed_used 0 and jelly_used 0", "rule": "R1", "players": 4, "seed": 1, "rounds": 0, "default": "last",
 "expect": {"players": {"1": {"score": 0, "donuts": 0, "glazed_used": 0, "jelly_used": 0}, "2": {"score": 0, "donuts": 0, "glazed_used": 0, "jelly_used": 0}, "3": {"score": 0, "donuts": 0, "glazed_used": 0, "jelly_used": 0}, "4": {"score": 0, "donuts": 0, "glazed_used": 0, "jelly_used": 0}}, "game": {"round": 0}}},

{"name": "A split of G=3 gives Glazed picks, so a lone Glazed choice is not void and scores 9", "rule": "R2", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "rules": [{"seat": 1, "options_include": 3}, {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"void": false, "score": 9, "donuts": 1, "glazed_used": 1, "jelly_used": 0}, "2": {"score": 4, "donuts": 1}, "3": {"score": 2, "donuts": 1}, "4": {"score": 1, "donuts": 1}}}},

{"name": "A split of G=0 leaves no Glazed picks, so a Glazed choice is void", "rule": "R2", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "rules": [{"seat": 1, "options_include": 0}, {"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"void": true, "score": 0, "donuts": 0, "glazed_used": 0}, "2": {"score": 4}, "3": {"score": 2}, "4": {"score": 1}}}},

{"name": "The public counters reveal nothing of the secret split at the start", "rule": "R3", "players": 4, "seed": 1, "rounds": 0, "default": "last",
 "expect": {"players": {"1": {"glazed_used": 0, "jelly_used": 0}, "2": {"glazed_used": 0, "jelly_used": 0}, "3": {"glazed_used": 0, "jelly_used": 0}, "4": {"glazed_used": 0, "jelly_used": 0}}}},

{"name": "Each round begins by adding 1 to the round number", "rule": "R4", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"game": {"round": 4}},
 "rules": [{"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Sprinkle"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Jelly"}],
 "expect": {"game": {"round": 5}}},

{"name": "Talk and choose run for all seats and the first round is round 1", "rule": "R5", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 0, "jelly_picks": 6}, "2": {"glazed_picks": 0, "jelly_picks": 6}, "3": {"glazed_picks": 0, "jelly_picks": 6}, "4": {"glazed_picks": 0, "jelly_picks": 6}}},
 "rules": [{"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Sprinkle"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Jelly"}],
 "expect": {"game": {"round": 1}, "players": {"1": {"score": 4}, "2": {"score": 2}, "3": {"score": 1}, "4": {"score": 6}}}},

{"name": "All five donuts are offered, even Glazed and Jelly with no picks left", "rule": "R6", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 0, "jelly_picks": 0}}},
 "rules": [{"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Plain"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"offered": [{"seat": 1, "option": "Glazed"}, {"seat": 1, "option": "Jelly"}, {"seat": 1, "option": "Cruller"}, {"seat": 1, "option": "Sprinkle"}, {"seat": 1, "option": "Plain"}],
            "players": {"1": {"score": 4, "donuts": 1}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}}}},

{"name": "Glazed with 0 Glazed picks and Jelly with 0 Jelly picks are void; Glazed with picks is not", "rule": "R7", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 0, "jelly_picks": 6}, "2": {"glazed_picks": 6, "jelly_picks": 0}, "3": {"glazed_picks": 2, "jelly_picks": 4}}},
 "rules": [{"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Jelly"}, {"seat": 3, "options_include": "Glazed"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"void": true, "score": 0}, "2": {"void": true, "score": 0}, "3": {"void": false, "score": 9, "donuts": 1}, "4": {"void": false, "score": 1}}}},

{"name": "A void Jelly gains 0, uses no pick and does not collide with a real Jelly", "rule": "R8", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 6, "jelly_picks": 0}, "2": {"glazed_picks": 3, "jelly_picks": 3}}},
 "rules": [{"seat": 1, "options_include": "Jelly"}, {"seat": 2, "options_include": "Jelly"}, {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Sprinkle"}],
 "expect": {"players": {"1": {"void": true, "score": 0, "donuts": 0, "jelly_used": 0}, "2": {"void": false, "score": 6, "donuts": 1, "jelly_used": 1}, "3": {"score": 4}, "4": {"score": 2}}}},

{"name": "At the reveal only the void choice is marked void", "rule": "R9", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 0, "jelly_picks": 6}}},
 "rules": [{"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"void": true}, "2": {"void": false}, "3": {"void": false}, "4": {"void": false}}}},

{"name": "A lone Glazed chooser gains 9 and one donut", "rule": "R10", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 4, "jelly_picks": 2}}},
 "rules": [{"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"score": 9, "donuts": 1}}}},

{"name": "A lone Jelly chooser gains 6 and one donut", "rule": "R11", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 4, "jelly_picks": 2}}},
 "rules": [{"seat": 1, "options_include": "Jelly"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"score": 6, "donuts": 1, "jelly_used": 1}}}},

{"name": "A lone Cruller chooser gains 4 and one donut", "rule": "R12", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "rules": [{"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Plain"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"score": 4, "donuts": 1}, "2": {"score": 0, "donuts": 0}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},

{"name": "A lone Sprinkle chooser gains 2 and one donut", "rule": "R13", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "rules": [{"seat": 1, "options_include": "Sprinkle"}, {"seat": 2, "options_include": "Plain"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"score": 2, "donuts": 1}, "2": {"score": 0}, "3": {"score": 0}, "4": {"score": 0}}}},

{"name": "A lone Plain chooser gains 1 and one donut", "rule": "R14", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "rules": [{"seat": 1, "options_include": "Plain"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Cruller"}],
 "expect": {"players": {"1": {"score": 1, "donuts": 1}, "2": {"score": 0, "donuts": 0}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},

{"name": "Two non-void players on the same donut both gain nothing", "rule": "R15", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 3, "jelly_picks": 3}, "2": {"glazed_picks": 3, "jelly_picks": 3}}},
 "rules": [{"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Glazed"}, {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Cruller"}],
 "expect": {"players": {"1": {"score": 0, "donuts": 0}, "2": {"score": 0, "donuts": 0}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},

{"name": "A discarded non-void Glazed still uses a pick", "rule": "R16", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 1, "jelly_picks": 3, "glazed_used": 2}, "2": {"glazed_picks": 2, "jelly_picks": 4}}},
 "rules": [{"seat": 1, "options_include": "Glazed"}, {"seat": 2, "options_include": "Glazed"}, {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Sprinkle"}],
 "expect": {"players": {"1": {"glazed_used": 3, "score": 0, "void": false}, "2": {"glazed_used": 1, "score": 0, "void": false}}}},

{"name": "A discarded non-void Jelly still uses a pick", "rule": "R17", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"glazed_picks": 2, "jelly_picks": 1, "jelly_used": 3}, "2": {"glazed_picks": 0, "jelly_picks": 6}}},
 "rules": [{"seat": 1, "options_include": "Jelly"}, {"seat": 2, "options_include": "Jelly"}, {"seat": 3, "options_include": "Cruller"}, {"seat": 4, "options_include": "Sprinkle"}],
 "expect": {"players": {"1": {"jelly_used": 4, "score": 0, "void": false}, "2": {"jelly_used": 1, "score": 0, "void": false}}}},

{"name": "Round gains add to the existing score and donut totals", "rule": "R18", "players": 4, "seed": 1, "rounds": 1, "default": "last",
 "given": {"players": {"1": {"score": 10, "donuts": 2}, "2": {"score": 5, "donuts": 1}}},
 "rules": [{"seat": 1, "options_include": "Cruller"}, {"seat": 2, "options_include": "Sprinkle"}, {"seat": 3, "options_include": "Plain"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"players": {"1": {"score": 14, "donuts": 3}, "2": {"score": 7, "donuts": 2}, "3": {"score": 0, "donuts": 0}, "4": {"score": 0, "donuts": 0}}}},

{"name": "The game ends after round 10 and unused picks are worth nothing", "rule": "R19", "players": 4, "seed": 1, "default": "last",
 "given": {"game": {"round": 9},
           "players": {"1": {"score": 20, "donuts": 4, "glazed_picks": 6, "jelly_picks": 0}, "2": {"score": 18, "donuts": 4, "glazed_picks": 0, "jelly_picks": 0}, "3": {"score": 10, "donuts": 3, "glazed_picks": 0, "jelly_picks": 0}, "4": {"score": 5, "donuts": 2, "glazed_picks": 6, "jelly_picks": 0}}},
 "rules": [{"seat": 1, "options_include": "Plain"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Jelly"}],
 "expect": {"winner": 2, "standings": {"1": 2105, "2": 2205, "3": 1204, "4": 502},
            "game": {"round": 10},
            "players": {"1": {"score": 21, "donuts": 5}, "2": {"score": 22, "donuts": 5}, "3": {"score": 12, "donuts": 4}, "4": {"score": 5, "donuts": 2, "void": true}}}},

{"name": "A tie on score is broken by more donuts", "rule": "R20", "players": 4, "seed": 1, "default": "last",
 "given": {"game": {"round": 9},
           "players": {"1": {"score": 30, "donuts": 5}, "2": {"score": 26, "donuts": 7}, "3": {"score": 10, "donuts": 3}, "4": {"score": 4, "donuts": 2}}},
 "rules": [{"seat": 1, "options_include": "Sprinkle"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"winner": 2, "standings": {"1": 3005, "2": 3008, "3": 1003, "4": 503},
            "players": {"1": {"score": 30, "donuts": 5}, "2": {"score": 30, "donuts": 8}}}},

{"name": "Players level on score and donuts share the win", "rule": "R20", "players": 4, "seed": 1, "default": "last",
 "given": {"game": {"round": 9},
           "players": {"1": {"score": 30, "donuts": 5}, "2": {"score": 26, "donuts": 4}, "3": {"score": 10, "donuts": 3}, "4": {"score": 4, "donuts": 2}}},
 "rules": [{"seat": 1, "options_include": "Sprinkle"}, {"seat": 2, "options_include": "Cruller"}, {"seat": 3, "options_include": "Sprinkle"}, {"seat": 4, "options_include": "Plain"}],
 "expect": {"winner": [1, 2], "standings": {"1": 3005, "2": 3005, "3": 1003, "4": 503},
            "players": {"1": {"score": 30, "donuts": 5}, "2": {"score": 30, "donuts": 5}}}}
]
````
