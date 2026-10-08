# 41 coder

- time: 2026-10-07T01:03:47+00:00 (99.0s)  model: rl-muse-spark-1-2-playground
- system prompt: [system/8b514415-coder.md](system/8b514415-coder.md) (sha256 8b514415baa6e594)
- sent sha256 b72022b251782ef6, reply sha256 ae49c9ddc4772492

## Sent (the whole conversation)

````
[
  {
    "role": "user",
    "content": "# Task: write the XColos game file for \"Battle of Wits: High Affinity Duel\"\n\nWrite the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.\n\n## The game\n\nPlayers: 2 to 2.\n\nSetup: Engine assigns each player a private type independently: Crimson (High=Left) or Azure (High=Right) with probability 0.5 each. Show each player only own type. Scores start 0. Play 12 rounds. Roles alternate: odd rounds 1,3,5,7,9,11 Player 1 is Poisoner and Player 2 is Chooser; even rounds 2,4,6,8,10,12 Player 2 is Poisoner and Player 1 is Chooser.\nEach round:\n1. Poisoner secretly chooses Left or Right as the sole poisoned goblet.\n2. Chooser secretly chooses Left or Right to drink (the other goes to Poisoner). Choices simultaneous and hidden until reveal.\n3. Reveal both choices and score:\n- If Poisoner's choice == Chooser's choice (match): Poisoner scores points, Chooser 0. Points = 3 if the matched side equals Poisoner's High side, else 1.\n- If choices mismatch: Chooser scores points, Poisoner 0. Points = 3 if Chooser's chosen side equals Chooser's High side, else 1.\nExamples: Crimson Poisoner poisons Left and Chooser picks Left => Poisoner +3. Azure Poisoner poisons Left and Chooser picks Left => Poisoner +1. Crimson Chooser picks Right while Poisoner poisoned Left (mismatch) => Chooser +1 (Right is Low for Crimson). Azure Chooser picks Right while Poisoner poisoned Left => Chooser +3.\nAnnounce choices, who scored and how many. Types stay hidden. After 12 rounds end.\n\nHow the winner is decided: Highest total points after 12 rounds wins. Equal totals = draw. Winner decided solely by sum of round points.\n\n## The interface the file must use\n\nIndependent tests were written against these names and you cannot see them, so use them exactly.\n\n- each player: `affinity_type` (text, visible: none, starts 'Crimson'): private type: Crimson (High=Left) or Azure (High=Right), assigned independently 0.5 each\n- each player: `type_code` (number, visible: none, starts 0): numeric encoding of affinity_type for arithmetic: 0=Crimson High Left, 1=Azure High Right\n- each player: `total_score` (number, visible: public, starts 0): cumulative points scored across rounds\n- each player: `current_choice` (text, visible: none, starts ''): Left or Right chosen this round; hidden until reveal\n- the table: `round_number` (number, visible: public, starts 1): current round 1 to 12\n- the table: `poisoner_seat` (number, visible: public, starts 1): seat number acting as Poisoner this round (1 on odd, 2 on even)\n- the table: `chooser_seat` (number, visible: public, starts 2): seat number acting as Chooser this round\n- the table: `last_poisoner_choice` (text, visible: public, starts ''): poisoner Left/Right choice after reveal for scoring\n- the table: `last_chooser_choice` (text, visible: public, starts ''): chooser Left/Right choice after reveal for scoring\n- the table: `last_poisoner_choice_code` (number, visible: public, starts 0): numeric encoding of last_poisoner_choice: 0=Left, 1=Right, mirrored from player for arithmetic\n- the table: `last_chooser_choice_code` (number, visible: public, starts 0): numeric encoding of last_chooser_choice: 0=Left, 1=Right\n- the table: `last_match` (number, visible: public, starts 0): 1 if poisoner and chooser choices matched, 0 if mismatched\n- the table: `last_poisoner_points` (number, visible: public, starts 0): points awarded to poisoner this round (0,1,3)\n- the table: `last_chooser_points` (number, visible: public, starts 0): points awarded to chooser this round (0,1,3)\n- parameters (each must be an attribute holding this value, never a number buried in a step): num_rounds = 12, high_payoff = 3, low_payoff = 1, low_payoff_value = 1, high_payoff_value = 3, initial_score = 0, type_probability_crimson = 0.5, type_probability_azure = 0.5\n- the game ends with exactly one of these results, named exactly: `seat 1`, `seat 2`, `draw`\n\n## How the platform works\n\nThe complete file format reference and two example games are in your system prompt. Follow them exactly: every key an\naction accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: every\nending's `when` is a calc condition, no prose conditions, no `llm`; every step uses `text`; choices made at the same\nmoment are a `poll`. End with a `result` and a calc condition as the `rps` example does (not the `auction`'s `winner`).\n\n- Mistakes the loader has refused before, so avoid them:\n  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table\n    attributes.) For something only its owner should see, use `ally`.\n  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.\n  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on\n    attributes, or with `set` operations in `setup`, instead.\n  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.\n  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {\"bind\": \"name\"}`; a later `update`\n    stores it with `\"value\": \"$name\"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the\n    answers away, and every score that depends on them stays at its starting value.\n  * An attribute declared `\"mutable\": false` is set once, by an `initialize` step, and any other step that sets it crashes the game\n    (\"declared static and has already been dealt\"). To set a hidden type or a starting value at setup, either use an `initialize`\n    step or leave the attribute mutable.\n  * Do not write steps that do nothing (for example an `if` of `{\"calc\": \"False\"}`), or two polls where one will do.\n  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,\n    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.\n- Keep a round to at most 12 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the\n  reveal. A game with more steps than that is rejected as too large, however well it plays.\n\nYour file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every\nattribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and\nshown your file again; fix what is wrong and keep the rest.\n\n## Guidance from the last attempt\n\nThe previous attempt had problems:\n\nCoder must fix game file: 1) Bind the simultaneous poll directly to player.current_choice (exact key, no spelling variant) and copy to table last_poisoner_choice/last_chooser_choice and last_*_choice_code (0=Left,1=Right) on reveal so those attributes actually change. 2) Fix role logic: poisoner_seat=1 on odd round else 2, chooser_seat=3-poisoner_seat, round_number increments correctly. 3) Fix scoring arithmetic: compute last_match=(last_poisoner_choice_code==last_chooser_choice_code), then if match: last_poisoner_points = (last_poisoner_choice_code==poisoner.type_code ? high_payoff_value : low_payoff_value), last_chooser_points=0 else opposite with chooser.type_code. Add to total_score. Remove when/if that never fires and ensure parameter attributes are used. 4) End after num_rounds=12 with arithmetic ranking on total_score -> seat 1 / seat 2 / draw.\n"
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"Battle of Wits: High Affinity Duel\",\n    \"name\": \"Battle of Wits: High Affinity Duel\",\n    \"players\": {\n      \"min\": 2,\n      \"max\": 2\n    },\n    \"blurb\": \"Private Crimson/Azure affinities duel over 12 rounds alternating Poisoner/Chooser for mismatched goblets.\",\n    \"rules\": \"12 rounds alternating Poisoner/Chooser. Each round both choose Left/Right simultaneously. Match gives Poisoner points, mismatch gives Chooser points. 3 points if scored side equals your High side (Crimson High Left, Azure High Right) else 1. After {num_rounds} rounds highest {total_score} wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"affinity_type\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"Crimson\",\n        \"values\": [\n          \"Crimson\",\n          \"Azure\"\n        ]\n      },\n      {\n        \"key\": \"type_code\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"total_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"current_choice\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Left\",\n          \"Right\",\n          \"\"\n        ]\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"poisoner_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"chooser_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"last_poisoner_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_chooser_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_poisoner_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_match\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_poisoner_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"num_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 12\n      },\n      {\n        \"key\": \"high_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"low_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"low_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"high_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"initial_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"type_probability_crimson\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      },\n      {\n        \"key\": \"type_probability_azure\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      }\n    ]\n  },\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"assign type codes\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"type_code\",\n            \"value\": {\n              \"calc\": \"0 if uniform(0,1) < type_probability_crimson else 1\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"assign affinity types\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"affinity_type\",\n            \"value\": {\n              \"calc\": \"'Crimson' if you.type_code == 0 else 'Azure'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"initial_score\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"update\",\n      \"phase\": \"roles\",\n      \"label\": \"set roles\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"poisoner_seat\",\n            \"value\": {\n              \"calc\": \"1 if round_number % 2 == 1 else 2\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"chooser_seat\",\n            \"value\": {\n              \"calc\": \"3 - poisoner_seat\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"choose\",\n      \"label\": \"choose goblet\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"Left\",\n          \"Right\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"current_choice\"\n      },\n      \"text\": \"Round {round_number} of {num_rounds}. You are {you.affinity_type}. Poisoner seat {poisoner_seat} Chooser seat {chooser_seat}. Secretly choose Left or Right. Poisoner poisons one goblet, Chooser drinks one; reveal is simultaneous.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"reveal\",\n      \"label\": \"reveal and score\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == poisoner_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == chooser_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_poisoner_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_chooser_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_match\",\n            \"value\": {\n              \"calc\": \"1 if last_poisoner_choice_code == last_chooser_choice_code else 0\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 0 else (high_payoff_value if last_poisoner_choice_code == [p.type_code for p in players if p.seat == poisoner_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 1 else (high_payoff_value if last_chooser_choice_code == [p.type_code for p in players if p.seat == chooser_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"poisoner_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_poisoner_points\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"chooser_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_chooser_points\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"reveal\",\n      \"label\": \"announce round\",\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} reveal: Poisoner seat {poisoner_seat} chose {last_poisoner_choice}, Chooser seat {chooser_seat} chose {last_chooser_choice}. Match={last_match}. Points this round: Poisoner {last_poisoner_points}, Chooser {last_chooser_points}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"advance\",\n      \"label\": \"next round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"advance\",\n      \"label\": \"game end\",\n      \"against\": [\n        \"seat 1\",\n        \"seat 2\",\n        \"draw\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"seat 1\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] > [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"seat 1\",\n      \"text\": \"Seat 1 wins with higher total points.\"\n    },\n    \"seat 2\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 2][0] > [p.total_score for p in players if p.seat == 1][0]\"\n      },\n      \"result\": \"seat 2\",\n      \"text\": \"Seat 2 wins with higher total points.\"\n    },\n    \"draw\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] == [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"draw\",\n      \"text\": \"Draw with equal total points.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 12,\n    \"rounds_max\": 12,\n    \"actions_max\": 200,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: it plays, but part of it does nothing: player attribute `current_choice` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `last_poisoner_choice` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `last_chooser_choice` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `last_chooser_points` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Declare only attributes the game uses, and make sure each one is set by a step that actually runs.\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"Battle of Wits: High Affinity Duel\",\n    \"name\": \"Battle of Wits: High Affinity Duel\",\n    \"players\": {\n      \"min\": 2,\n      \"max\": 2\n    },\n    \"blurb\": \"Private Crimson/Azure affinities duel over 12 rounds alternating Poisoner/Chooser for mismatched goblets.\",\n    \"rules\": \"12 rounds alternating Poisoner/Chooser. Each round both choose Left/Right simultaneously. Match gives Poisoner points, mismatch gives Chooser points. 3 points if scored side equals your High side (Crimson High Left, Azure High Right) else 1. After {num_rounds} rounds highest {total_score} wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"affinity_type\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"Crimson\",\n        \"values\": [\n          \"Crimson\",\n          \"Azure\"\n        ]\n      },\n      {\n        \"key\": \"type_code\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"total_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"current_choice\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Left\",\n          \"Right\",\n          \"\"\n        ]\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"poisoner_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"chooser_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"last_poisoner_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_chooser_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_poisoner_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_match\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_poisoner_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"num_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 12\n      },\n      {\n        \"key\": \"high_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"low_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"low_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"high_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"initial_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"type_probability_crimson\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      },\n      {\n        \"key\": \"type_probability_azure\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      }\n    ]\n  },\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"assign type codes\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"type_code\",\n            \"value\": {\n              \"calc\": \"0 if uniform(0,1) < type_probability_crimson else 1\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"assign affinity types\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"affinity_type\",\n            \"value\": {\n              \"calc\": \"'Crimson' if you.type_code == 0 else 'Azure'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"initial_score\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"update\",\n      \"phase\": \"roles\",\n      \"label\": \"set roles\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"poisoner_seat\",\n            \"value\": {\n              \"calc\": \"1 if round_number % 2 == 1 else 2\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"chooser_seat\",\n            \"value\": {\n              \"calc\": \"3 - poisoner_seat\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"choose\",\n      \"label\": \"choose goblet\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"Left\",\n          \"Right\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"current_choice\"\n      },\n      \"text\": \"Round {round_number} of {num_rounds}. Poisoner is seat {poisoner_seat}, Chooser is seat {chooser_seat}. Both secretly choose Left or Right simultaneously.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"reveal\",\n      \"label\": \"store choices\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"current_choice\",\n            \"value\": \"$current_choice\"\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"reveal\",\n      \"label\": \"reveal and score\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == poisoner_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == chooser_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_poisoner_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_chooser_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_match\",\n            \"value\": {\n              \"calc\": \"1 if last_poisoner_choice_code == last_chooser_choice_code else 0\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 0 else (high_payoff_value if last_poisoner_choice_code == [p.type_code for p in players if p.seat == poisoner_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 1 else (high_payoff_value if last_chooser_choice_code == [p.type_code for p in players if p.seat == chooser_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"poisoner_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_poisoner_points\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"chooser_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_chooser_points\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"reveal\",\n      \"label\": \"announce round\",\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} reveal: Poisoner seat {poisoner_seat} chose {last_poisoner_choice}, Chooser seat {chooser_seat} chose {last_chooser_choice}. Match={last_match}. Points this round: Poisoner {last_poisoner_points}, Chooser {last_chooser_points}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"advance\",\n      \"label\": \"next round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"advance\",\n      \"label\": \"game end\",\n      \"against\": [\n        \"seat 1\",\n        \"seat 2\",\n        \"draw\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"seat 1\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] > [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"seat 1\",\n      \"text\": \"Seat 1 wins with higher total points.\"\n    },\n    \"seat 2\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 2][0] > [p.total_score for p in players if p.seat == 1][0]\"\n      },\n      \"result\": \"seat 2\",\n      \"text\": \"Seat 2 wins with higher total points.\"\n    },\n    \"draw\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] == [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"draw\",\n      \"text\": \"Draw with equal total points.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 12,\n    \"rounds_max\": 12,\n    \"actions_max\": 200,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: it plays, but part of it does nothing: game attribute `last_chooser_points` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Declare only attributes the game uses, and make sure each one is set by a step that actually runs.\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  },
  {
    "role": "assistant",
    "content": "{\n  \"schema\": 1,\n  \"meta\": {\n    \"id\": \"Battle of Wits: High Affinity Duel\",\n    \"name\": \"Battle of Wits: High Affinity Duel\",\n    \"players\": {\n      \"min\": 2,\n      \"max\": 2\n    },\n    \"blurb\": \"Private Crimson/Azure affinities duel over 12 rounds alternating Poisoner/Chooser for mismatched goblets.\",\n    \"rules\": \"12 rounds alternating Poisoner/Chooser. Each round both choose Left/Right simultaneously. Match gives Poisoner points, mismatch gives Chooser points. 3 points if scored side equals your High side (Crimson High Left, Azure High Right) else 1. After {num_rounds} rounds highest {total_score} wins.\"\n  },\n  \"statuses\": [\n    {\n      \"id\": \"playing\",\n      \"acts\": true,\n      \"initial\": true\n    }\n  ],\n  \"attributes\": {\n    \"player\": [\n      {\n        \"key\": \"affinity_type\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"Crimson\",\n        \"values\": [\n          \"Crimson\",\n          \"Azure\"\n        ]\n      },\n      {\n        \"key\": \"type_code\",\n        \"visible\": \"ally\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"total_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"current_choice\",\n        \"visible\": \"ally\",\n        \"type\": \"text\",\n        \"initial\": \"\",\n        \"values\": [\n          \"Left\",\n          \"Right\",\n          \"\"\n        ]\n      }\n    ],\n    \"game\": [\n      {\n        \"key\": \"round_number\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"poisoner_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"chooser_seat\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 2\n      },\n      {\n        \"key\": \"last_poisoner_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_chooser_choice\",\n        \"visible\": \"public\",\n        \"type\": \"text\",\n        \"initial\": \"\"\n      },\n      {\n        \"key\": \"last_poisoner_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_choice_code\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_match\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_poisoner_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"last_chooser_points\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"num_rounds\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 12\n      },\n      {\n        \"key\": \"high_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"low_payoff\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"low_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 1\n      },\n      {\n        \"key\": \"high_payoff_value\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 3\n      },\n      {\n        \"key\": \"initial_score\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0\n      },\n      {\n        \"key\": \"type_probability_crimson\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      },\n      {\n        \"key\": \"type_probability_azure\",\n        \"visible\": \"public\",\n        \"type\": \"number\",\n        \"initial\": 0.5\n      }\n    ]\n  },\n  \"setup\": [\n    {\n      \"use\": \"update\",\n      \"label\": \"assign type codes\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"type_code\",\n            \"value\": {\n              \"calc\": \"0 if uniform(0,1) < type_probability_crimson else 1\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"update\",\n      \"label\": \"assign affinity types\",\n      \"do\": [\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"affinity_type\",\n            \"value\": {\n              \"calc\": \"'Crimson' if you.type_code == 0 else 'Azure'\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"players\": \"all\",\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"initial_score\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"sync\",\n      \"label\": \"the table\",\n      \"mode\": \"self\",\n      \"to\": \"all\",\n      \"text\": \"You start with:\"\n    }\n  ],\n  \"steps\": [\n    {\n      \"use\": \"update\",\n      \"phase\": \"roles\",\n      \"label\": \"set roles\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"poisoner_seat\",\n            \"value\": {\n              \"calc\": \"1 if round_number % 2 == 1 else 2\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"chooser_seat\",\n            \"value\": {\n              \"calc\": \"3 - poisoner_seat\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"poll\",\n      \"phase\": \"choose\",\n      \"label\": \"choose goblet\",\n      \"to\": \"acting\",\n      \"answer\": {\n        \"type\": \"choice\",\n        \"options\": [\n          \"Left\",\n          \"Right\"\n        ]\n      },\n      \"verify\": {\n        \"bind\": \"current_choice\"\n      },\n      \"text\": \"Round {round_number} of {num_rounds}. Poisoner is seat {poisoner_seat}, Chooser is seat {chooser_seat}. Both secretly choose Left or Right simultaneously.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"reveal\",\n      \"label\": \"reveal and score\",\n      \"do\": [\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == poisoner_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice\",\n            \"value\": {\n              \"calc\": \"[p.current_choice for p in players if p.seat == chooser_seat][0]\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_poisoner_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_choice_code\",\n            \"value\": {\n              \"calc\": \"0 if last_chooser_choice == 'Left' else 1\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_match\",\n            \"value\": {\n              \"calc\": \"1 if last_poisoner_choice_code == last_chooser_choice_code else 0\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_poisoner_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 0 else (high_payoff_value if last_poisoner_choice_code == [p.type_code for p in players if p.seat == poisoner_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"set\": {\n            \"key\": \"last_chooser_points\",\n            \"value\": {\n              \"calc\": \"0 if last_match == 1 else (high_payoff_value if last_chooser_choice_code == [p.type_code for p in players if p.seat == chooser_seat][0] else low_payoff_value)\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"poisoner_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_poisoner_points\"\n            }\n          }\n        },\n        {\n          \"adjust\": {\n            \"player\": {\n              \"calc\": \"chooser_seat\"\n            },\n            \"key\": \"total_score\",\n            \"value\": {\n              \"calc\": \"last_chooser_points\"\n            }\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"tell\",\n      \"phase\": \"reveal\",\n      \"label\": \"announce round\",\n      \"to\": \"all\",\n      \"text\": \"Round {round_number} reveal: Poisoner seat {poisoner_seat} chose {last_poisoner_choice}, Chooser seat {chooser_seat} chose {last_chooser_choice}. Match={last_match}. Points this round: Poisoner {last_poisoner_points}, Chooser {last_chooser_points}.\"\n    },\n    {\n      \"use\": \"update\",\n      \"phase\": \"advance\",\n      \"label\": \"next round\",\n      \"do\": [\n        {\n          \"adjust\": {\n            \"key\": \"round_number\",\n            \"value\": 1\n          }\n        }\n      ]\n    },\n    {\n      \"use\": \"check\",\n      \"phase\": \"advance\",\n      \"label\": \"game end\",\n      \"against\": [\n        \"seat 1\",\n        \"seat 2\",\n        \"draw\"\n      ]\n    }\n  ],\n  \"end\": {\n    \"seat 1\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] > [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"seat 1\",\n      \"text\": \"Seat 1 wins with higher total points.\"\n    },\n    \"seat 2\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 2][0] > [p.total_score for p in players if p.seat == 1][0]\"\n      },\n      \"result\": \"seat 2\",\n      \"text\": \"Seat 2 wins with higher total points.\"\n    },\n    \"draw\": {\n      \"when\": {\n        \"calc\": \"round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] == [p.total_score for p in players if p.seat == 2][0]\"\n      },\n      \"result\": \"draw\",\n      \"text\": \"Draw with equal total points.\"\n    }\n  },\n  \"limits\": {\n    \"rounds\": 12,\n    \"rounds_max\": 12,\n    \"actions_max\": 200,\n    \"deadline_s\": 120\n  }\n}"
  },
  {
    "role": "user",
    "content": "That game file was refused. Why: it plays, but part of it does nothing: player attribute `current_choice` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `last_poisoner_choice` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `last_chooser_choice` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.; game attribute `last_chooser_points` is never changed in 3 random matches, so nothing updates it. Steps that name it: reveal and score. They never change it: their `when`/`if` may never be true, the `key` may be spelled differently from the attribute, or the value written may equal what it already holds.. Declare only attributes the game uses, and make sure each one is set by a step that actually runs.\nCorrect it: change what the problem requires and keep the rest. Reply with the complete corrected game file as one JSON object, and nothing else."
  }
]
````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "Battle of Wits: High Affinity Duel",
    "name": "Battle of Wits: High Affinity Duel",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Private Crimson/Azure affinities duel over 12 rounds alternating Poisoner/Chooser for mismatched goblets.",
    "rules": "12 rounds alternating Poisoner/Chooser. Each round both choose Left/Right simultaneously. Match gives Poisoner points, mismatch gives Chooser points. 3 points if scored side equals your High side (Crimson High Left, Azure High Right) else 1. After {num_rounds} rounds highest {total_score} wins."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "affinity_type",
        "visible": "ally",
        "type": "text",
        "initial": "Crimson",
        "values": [
          "Crimson",
          "Azure"
        ]
      },
      {
        "key": "type_code",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_choice",
        "visible": "ally",
        "type": "text",
        "initial": "",
        "values": [
          "Left",
          "Right",
          ""
        ]
      }
    ],
    "game": [
      {
        "key": "round_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "poisoner_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "chooser_seat",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "last_poisoner_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_chooser_choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_poisoner_choice_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_chooser_choice_code",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_match",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_poisoner_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_chooser_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "num_rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "high_payoff",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "low_payoff",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "low_payoff_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "high_payoff_value",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "initial_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "type_probability_crimson",
        "visible": "public",
        "type": "number",
        "initial": 0.5
      },
      {
        "key": "type_probability_azure",
        "visible": "public",
        "type": "number",
        "initial": 0.5
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "assign type codes",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "type_code",
            "value": {
              "calc": "0 if uniform(0,1) < type_probability_crimson else 1"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "assign affinity types",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "affinity_type",
            "value": {
              "calc": "'Crimson' if you.type_code == 0 else 'Azure'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "total_score",
            "value": {
              "calc": "initial_score"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roles",
      "label": "set roles",
      "do": [
        {
          "set": {
            "key": "poisoner_seat",
            "value": {
              "calc": "1 if round_number % 2 == 1 else 2"
            }
          }
        },
        {
          "set": {
            "key": "chooser_seat",
            "value": {
              "calc": "3 - poisoner_seat"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "choose goblet",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Left",
          "Right"
        ]
      },
      "verify": {
        "bind": "current_choice"
      },
      "text": "Round {round_number} of {num_rounds}. Poisoner is seat {poisoner_seat}, Chooser is seat {chooser_seat}. Both secretly choose Left or Right simultaneously."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "store player choices",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "current_choice",
            "value": {
              "calc": "$current_choice"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal choices",
      "do": [
        {
          "set": {
            "key": "last_poisoner_choice",
            "value": {
              "calc": "[p.current_choice for p in players if p.seat == poisoner_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "last_chooser_choice",
            "value": {
              "calc": "[p.current_choice for p in players if p.seat == chooser_seat][0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "score round",
      "do": [
        {
          "set": {
            "key": "last_poisoner_choice_code",
            "value": {
              "calc": "0 if last_poisoner_choice == 'Left' else 1"
            }
          }
        },
        {
          "set": {
            "key": "last_chooser_choice_code",
            "value": {
              "calc": "0 if last_chooser_choice == 'Left' else 1"
            }
          }
        },
        {
          "set": {
            "key": "last_match",
            "value": {
              "calc": "1 if last_poisoner_choice == last_chooser_choice else 0"
            }
          }
        },
        {
          "set": {
            "key": "last_poisoner_points",
            "value": {
              "calc": "0 if last_match == 0 else (high_payoff_value if last_poisoner_choice_code == [p.type_code for p in players if p.seat == poisoner_seat][0] else low_payoff_value)"
            }
          }
        },
        {
          "set": {
            "key": "last_chooser_points",
            "value": {
              "calc": "0 if last_match == 1 else (high_payoff_value if last_chooser_choice_code == [p.type_code for p in players if p.seat == chooser_seat][0] else low_payoff_value)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "poisoner_seat"
            },
            "key": "total_score",
            "value": {
              "calc": "last_poisoner_points"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "chooser_seat"
            },
            "key": "total_score",
            "value": {
              "calc": "last_chooser_points"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "announce round",
      "to": "all",
      "text": "Round {round_number} reveal: Poisoner seat {poisoner_seat} chose {last_poisoner_choice}, Chooser seat {chooser_seat} chose {last_chooser_choice}. Match={last_match}. Points this round: Poisoner {last_poisoner_points}, Chooser {last_chooser_points}."
    },
    {
      "use": "update",
      "phase": "advance",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "advance",
      "label": "game end",
      "against": [
        "seat 1",
        "seat 2",
        "draw"
      ]
    }
  ],
  "end": {
    "seat 1": {
      "when": {
        "calc": "round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] > [p.total_score for p in players if p.seat == 2][0]"
      },
      "result": "seat 1",
      "text": "Seat 1 wins with higher total points."
    },
    "seat 2": {
      "when": {
        "calc": "round_number > num_rounds and [p.total_score for p in players if p.seat == 2][0] > [p.total_score for p in players if p.seat == 1][0]"
      },
      "result": "seat 2",
      "text": "Seat 2 wins with higher total points."
    },
    "draw": {
      "when": {
        "calc": "round_number > num_rounds and [p.total_score for p in players if p.seat == 1][0] == [p.total_score for p in players if p.seat == 2][0]"
      },
      "result": "draw",
      "text": "Draw with equal total points."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 200,
    "deadline_s": 120
  }
}
````
