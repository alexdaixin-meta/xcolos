# Task: write the XColos game file for "Battle of Wits: High Affinity Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2.

Setup: Engine assigns each player a private type independently: Crimson (High=Left) or Azure (High=Right) with probability 0.5 each. Show each player only own type. Scores start 0. Play 12 rounds. Roles alternate: odd rounds 1,3,5,7,9,11 Player 1 is Poisoner and Player 2 is Chooser; even rounds 2,4,6,8,10,12 Player 2 is Poisoner and Player 1 is Chooser.
Each round:
1. Poisoner secretly chooses Left or Right as the sole poisoned goblet.
2. Chooser secretly chooses Left or Right to drink (the other goes to Poisoner). Choices simultaneous and hidden until reveal.
3. Reveal both choices and score:
- If Poisoner's choice == Chooser's choice (match): Poisoner scores points, Chooser 0. Points = 3 if the matched side equals Poisoner's High side, else 1.
- If choices mismatch: Chooser scores points, Poisoner 0. Points = 3 if Chooser's chosen side equals Chooser's High side, else 1.
Examples: Crimson Poisoner poisons Left and Chooser picks Left => Poisoner +3. Azure Poisoner poisons Left and Chooser picks Left => Poisoner +1. Crimson Chooser picks Right while Poisoner poisoned Left (mismatch) => Chooser +1 (Right is Low for Crimson). Azure Chooser picks Right while Poisoner poisoned Left => Chooser +3.
Announce choices, who scored and how many. Types stay hidden. After 12 rounds end.

How the winner is decided: Highest total points after 12 rounds wins. Equal totals = draw. Winner decided solely by sum of round points.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `affinity_type` (text, visible: none, starts 'Crimson'): private type: Crimson (High=Left) or Azure (High=Right), assigned independently 0.5 each
- each player: `type_code` (number, visible: none, starts 0): numeric encoding of affinity_type for arithmetic: 0=Crimson High Left, 1=Azure High Right
- each player: `total_score` (number, visible: public, starts 0): cumulative points scored across rounds
- each player: `current_choice` (text, visible: none, starts ''): Left or Right chosen this round; hidden until reveal
- the table: `round_number` (number, visible: public, starts 1): current round 1 to 12
- the table: `poisoner_seat` (number, visible: public, starts 1): seat number acting as Poisoner this round (1 on odd, 2 on even)
- the table: `chooser_seat` (number, visible: public, starts 2): seat number acting as Chooser this round
- the table: `last_poisoner_choice` (text, visible: public, starts ''): poisoner Left/Right choice after reveal for scoring
- the table: `last_chooser_choice` (text, visible: public, starts ''): chooser Left/Right choice after reveal for scoring
- the table: `last_poisoner_choice_code` (number, visible: public, starts 0): numeric encoding of last_poisoner_choice: 0=Left, 1=Right, mirrored from player for arithmetic
- the table: `last_chooser_choice_code` (number, visible: public, starts 0): numeric encoding of last_chooser_choice: 0=Left, 1=Right
- the table: `last_match` (number, visible: public, starts 0): 1 if poisoner and chooser choices matched, 0 if mismatched
- the table: `last_poisoner_points` (number, visible: public, starts 0): points awarded to poisoner this round (0,1,3)
- the table: `last_chooser_points` (number, visible: public, starts 0): points awarded to chooser this round (0,1,3)
- parameters (each must be an attribute holding this value, never a number buried in a step): num_rounds = 12, high_payoff = 3, low_payoff = 1, low_payoff_value = 1, high_payoff_value = 3, initial_score = 0, type_probability_crimson = 0.5, type_probability_azure = 0.5
- the game ends with exactly one of these results, named exactly: `seat 1`, `seat 2`, `draw`

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: every
ending's `when` is a calc condition, no prose conditions, no `llm`; every step uses `text`; choices made at the same
moment are a `poll`. End with a `result` and a calc condition as the `rps` example does (not the `auction`'s `winner`).

- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.
- Keep a round to at most 12 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is rejected as too large, however well it plays.

## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{"where": "you.seat == N"}`, with `"verify": {"bind": "aN"}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and the endings in `end`, comparing `players[0].score` and `players[1].score`.
Every attribute is set by a step that runs. Adapt this; do not invent another way to store answers.

```json
{
  "schema": 1,
  "meta": {
    "id": "match_or_miss",
    "name": "Match or Miss",
    "players": {
      "min": 2,
      "max": 2
    },
    "blurb": "Two players choose A or B in secret; seat 1 scores when they match, seat 2 when they differ."
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
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "rounds_left",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "last_a1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_a2",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ]
  },
  "rules": "Three rounds. Each round both players secretly choose A or B. If the choices match, seat 1 scores a point; if they differ, seat 2 does. The higher score wins.",
  "setup": [
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
      "use": "ask",
      "label": "seat 1 chooses",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a1"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "ask",
      "label": "seat 2 chooses",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B"
        ]
      },
      "verify": {
        "bind": "a2"
      },
      "text": "Choose A or B. Your opponent will not see it."
    },
    {
      "use": "update",
      "label": "score the round",
      "do": [
        {
          "set": {
            "key": "last_a1",
            "value": "$a1"
          }
        },
        {
          "set": {
            "key": "last_a2",
            "value": "$a2"
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "1 if $a1 == $a2 else 0"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "0 if $a1 == $a2 else 1"
            }
          }
        },
        {
          "adjust": {
            "key": "rounds_left",
            "value": -1
          }
        }
      ],
      "text": "Seat 1 chose {last_a1}, seat 2 chose {last_a2}."
    },
    {
      "use": "check",
      "label": "is it over",
      "when": {
        "calc": "rounds_left <= 0"
      },
      "against": [
        "seat_1_wins",
        "seat_2_wins",
        "draw"
      ]
    }
  ],
  "end": {
    "seat_1_wins": {
      "when": {
        "calc": "players[0].score > players[1].score"
      },
      "result": "seat 1",
      "text": "Seat 1 wins."
    },
    "seat_2_wins": {
      "when": {
        "calc": "players[1].score > players[0].score"
      },
      "result": "seat 2",
      "text": "Seat 2 wins."
    },
    "draw": {
      "when": {
        "calc": "players[0].score == players[1].score"
      },
      "result": "draw",
      "text": "A draw."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.
