# 09 coder

- time: 2026-10-28T05:17:05+00:00 (60.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 7dee5367fdc02e69, reply sha256 1521b57849f31d39

## Sent

````
# Task: write the XColos game file for "Ripening Hats"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. There are 5 hat colours, listed in this fixed order: Red, Blue, Green, Yellow, Purple. Each colour has a public value, and all five start at 2. Each player is dealt a secret favourite colour at random, all different; only that player knows it. Every player has a private score starting at 0, which only that player can see.

EACH ROUND (12 rounds):
1. Announce to everyone: the round number and the current value of each of the 5 colours.
2. Talk: everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.
3. Choice: everyone simultaneously and secretly chooses one of Red, Blue, Green, Yellow, Purple or Black.
4. Collection. A player who chose Black adds 1 to their score. A player who chose a colour that no other player chose this round collects it: they add that colour's current value to their score, plus 3 more if it is their favourite. A colour chosen by two or more players is contested, and none of them gains anything.
5. Announce to everyone, without naming players: for each colour, whether it was COLLECTED (exactly one chooser), CONTESTED (two or more) or UNTOUCHED (no one), and how many players chose Black. Individual choices and scores are never announced.
6. Value update. Each colour that was collected this round resets to 1. Each colour that was contested or untouched gains +1, to a maximum of 7.
7. After round 12 the game ends.

END. All favourites and scores are revealed.

How the winner is decided: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Ripening Hats (3 to 4 players, best with 4)

Over 12 rounds, players secretly pick one of 5 hat colours (or safe Black); a colour picked by exactly one player pays its ripening value, plus a bonus if it is that player's secret favourite, and contested colours pay nothing.

STATE (every item below must exist in the file):
  - each player: favourite (text, starts ''); only its owner sees it. The player's secret favourite colour, dealt at random from the colour pool, different for every player; revealed at the end
  - each player: score (number, starts 0); only its owner sees it. The player's private score, revealed at the end
  - each player: choice (text, starts ''); only its owner sees it. This round's secret choice: Red, Blue, Green, Yellow, Purple or Black
  - each player: message (text, starts ''); everyone sees it. This round's talk message, shown to everyone after all are in
  - the table: round (number, starts 1); everyone sees it. The current round number, 1 to 12
  - the table: colour_pool (list, starts ['Red', 'Blue', 'Green', 'Yellow', 'Purple']); hidden from all players. Hidden list of colours not yet dealt as favourites; each deal removes one
  - the table: value_red (number, starts 2); everyone sees it. Current value of Red
  - the table: value_blue (number, starts 2); everyone sees it. Current value of Blue
  - the table: value_green (number, starts 2); everyone sees it. Current value of Green
  - the table: value_yellow (number, starts 2); everyone sees it. Current value of Yellow
  - the table: value_purple (number, starts 2); everyone sees it. Current value of Purple
  - the table: count_red (number, starts 0); hidden from all players. How many players chose Red this round
  - the table: count_blue (number, starts 0); hidden from all players. How many players chose Blue this round
  - the table: count_green (number, starts 0); hidden from all players. How many players chose Green this round
  - the table: count_yellow (number, starts 0); hidden from all players. How many players chose Yellow this round
  - the table: count_purple (number, starts 0); hidden from all players. How many players chose Purple this round
  - the table: status_red (text, starts ''); everyone sees it. Red's result this round: COLLECTED, CONTESTED or UNTOUCHED
  - the table: status_blue (text, starts ''); everyone sees it. Blue's result this round: COLLECTED, CONTESTED or UNTOUCHED
  - the table: status_green (text, starts ''); everyone sees it. Green's result this round: COLLECTED, CONTESTED or UNTOUCHED
  - the table: status_yellow (text, starts ''); everyone sees it. Yellow's result this round: COLLECTED, CONTESTED or UNTOUCHED
  - the table: status_purple (text, starts ''); everyone sees it. Purple's result this round: COLLECTED, CONTESTED or UNTOUCHED
  - the table: black_count (number, starts 0); everyone sees it. How many players chose Black this round
  - parameters, each kept as a table attribute: num_colours = 5, initial_colour_value = 2, max_colour_value = 7, reset_value = 1, value_increment = 1, black_points = 1, favourite_bonus = 3, contested_gain = 0, rounds = 12, initial_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set all five colour values (value_red, value_blue, value_green, value_yellow, value_purple) to 2.
  2. Set every player's score to 0 and round to 1.
  3. For each player, draw one colour at random from colour_pool into that player's favourite and remove it from colour_pool, so all favourites are different.
  4. Sync: each player is told their own favourite and score.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce: 'Round {round} of 12. Values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}, Purple {value_purple}.'
  2. [poll] all players answers: short text. What happens: Set each player's message to their text. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Talk binds no one.
  3. [poll] all players answers: one of: Red, Blue, Green, Yellow, Purple, Black. What happens: Set each player's choice to their answer. No answer is shown to anyone.
  4. [update] all players. What happens: Set count_red, count_blue, count_green, count_yellow and count_purple each to the number of players whose choice is that colour. Set black_count to the number of players whose choice is Black.
  5. [update] all players. What happens: For each player: if choice = Black, add 1 to score. If choice is a colour C and count_C = 1, add value_C to score, and add a further 3 if favourite = C. If count_C >= 2, add 0. Do not announce scores.
  6. [update] all players. What happens: For each colour C, set status_C to COLLECTED if count_C = 1, CONTESTED if count_C >= 2, and UNTOUCHED if count_C = 0.
  7. [tell] all players. What happens: Announce without naming players: 'Red {status_red}, Blue {status_blue}, Green {status_green}, Yellow {status_yellow}, Purple {status_purple}. Black chosen by {black_count}.'
  8. [update] all players. What happens: For each colour C: if count_C = 1, set value_C to 1; otherwise set value_C to min(7, value_C + 1).
  9. [sync] all players. What happens: Each player is sent their own score and favourite.
  10. [update] all players. What happens: Add 1 to round.
  11. [check] all players. What happens: If round > 12, end the game. Reveal every player's favourite and score to everyone. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then all five colour values are 2 and every player's score is 0.
  R2. When favourites are dealt, then each player gets one of Red, Blue, Green, Yellow or Purple at random, no two players get the same colour, and only the owner can see it.
  R3. When a round begins, then everyone is told the round number and the current value of each of the 5 colours.
  R4. When the talk step runs, then every player writes one short message at the same time, and all messages are shown to everyone only after all are in.
  R5. When the choice step runs, then every player secretly and simultaneously picks exactly one of Red, Blue, Green, Yellow, Purple or Black.
  R6. When a player chooses Black, then that player's score increases by 1.
  R7. When a player is the only one to choose colour C and C is not their favourite, then their score increases by value_C (for example, by 4 if value_C is 4).
  R8. When a player is the only one to choose colour C and C is their favourite, then their score increases by value_C + 3 (for example, by 5 if value_C is 2).
  R9. When two or more players choose the same colour, then none of them gains any points that round.
  R10. When choices are resolved, then each colour's status is announced as COLLECTED (exactly 1 chooser), CONTESTED (2 or more) or UNTOUCHED (0), along with the number of Black choosers, without naming any player.
  R11. When a colour was collected this round, then its value becomes 1 for the next round.
  R12. When a colour was contested or untouched this round, then its value rises by 1, but never above 7 (a colour at 7 stays at 7).
  R13. When the game is running, then individual choices and scores are never announced.
  R14. When round 12 has been resolved, then the game ends and all favourites and scores are revealed.
  R15. When the game ends, then the player with the highest score wins, and if two or more players tie for the highest score, the result is a draw among them.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk: write one short message | asked: all players | options: Any short free text, the same for every seat.
  - Choice: pick a hat | asked: all players | options: Every seat, in every round: Red, Blue, Green, Yellow, Purple, Black.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round > 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score. The highest score wins. Players tied for the highest score share the result, which is the source's draw.
  - the end screen states the final scores or deciding figures, and a short model-written summary of how the game went

## Recipe: a shared deck and hidden hands (tested on the engine)

When the script has a deck and hands, both must exist as attributes, and setup must really deal. Declare the hand as a PLAYER attribute
`{"key": "hand", "visible": "ally", "type": "list", "initial": []}` (only its owner sees it; a player attribute is never `none`) and the
deck as a TABLE attribute `{"key": "deck", "visible": "none", "type": "list", "initial": [every card, one entry per copy]}`, plus a table text
attribute `pick` (visible `none`, initial `""`) to hold the card just drawn. Then ONE draw, of a random card into seat N's hand, is three operations
in an `update`'s `do` list, in this order:

  {"set":    {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
  {"append": {"player": N, "key": "hand", "value": {"calc": "pick"}}},
  {"remove": {"key": "deck", "value": {"calc": "pick"}}}

Dealing two cards to three seats is that block repeated twice for each seat (6 draws), never a fixed list written into `initial`: the deal
is random and different each match, and every player's hand must differ. A card coming back is `{"append": {"key": "deck", ...}}` and
`{"remove": {"player": N, "key": "hand", ...}}`. "Has a card of role R" is `"R" in you.hand`. Use `{"if": {"calc": ...}}` on an operation to make
it conditional. Never declare `hand` or `deck` and then leave them unchanged: the rules would then claim cards that do not exist.

## Pattern: offer each seat only what it may do (tested on the engine)

A question's options may come from state, and the state can differ for every player. So make who may do what part of the OFFER, never a check
afterwards. Declare a PLAYER list attribute (say `offer`, visible `ally`), and set it for everyone in one `update` just before the question,
from each player's own attributes and the table's:

  {"set": {"players": "all", "key": "offer",
           "value": {"calc": "['wait'] + (['buy'] if you.coins >= price else []) + (['block'] if you.seat == target else [])"}}}

then ask with `"answer": {"type": "choice", "options": {"attribute": "offer"}}` and `to` naming who is asked. `you` is each player in turn, and a
list can be built with `+` and `(... if ... else [])`. Whatever a seat may not do is not in its list: a seat that cannot pay is not offered the
paid action, only the target of an action is offered a block against it, a player already out is not asked. Do the same for a target: put the
legal seats in a list attribute.

When only one option is left (the last unused action, the only legal card), still ask the question: the engine answers a choice with one
option for the seat, with no model call, and records it as the seat's move. Do not skip the question with a `when` and set the answer
yourself: that move is then missing from the match, and a test that scripts it fails.

When a player is eliminated, set the PLATFORM status as well as your own counters: declare a status for it (`{"id": "out", "acts": false}`) next to `playing` and
run `{"set_status": {"player": N, "to": "out", "text": "Seat {player} is out."}}`. Without it the platform and the console show the player as still in the game, and the
prompts list them as playing, whatever your own `alive` attribute says. Name the cards it reveals in the same announcement.

Do NOT offer a broad list and then refuse illegal answers and ask again (a `repeat` that asks, checks, and asks again, or an update that removes
an option the player just picked). It costs a model call, it lets a model choose something illegal, and the pipeline reports it as a failure:
"an option is offered and then refused". If you find yourself writing a step called "refuse...", "check the answer is legal" or "not allowed",
you are filling the wrong list: fix the offer.

## Rounds and the safety cap

If the script ends when someone wins (the last player standing, a target reached) and not after a set number of rounds, do not add a fixed
round count to the rules. The game file still has a `limits` block: set `limits.rounds` to the generous cap the script gives (the number of
rounds it says a match may run at most) and `limits.rounds_max` to at least that. The ending's `when` holds for the real ending AND when the cap
is reached, and its `rank_by` also ranks the players as the script says at the cap, so a match that hits the cap still ends with a winner.

## The interface the file must use

Independent tests were written against these names and you cannot see them, so use them exactly.

- each player: `score` (number, visible: ally, starts 0): The player's private score, revealed at the end
- the table: `round` (number, visible: public, starts 1): The current round number, 1 to 12
- the table: `value_red` (number, visible: public, starts 2): Current value of Red
- the table: `value_blue` (number, visible: public, starts 2): Current value of Blue
- the table: `value_green` (number, visible: public, starts 2): Current value of Green
- the table: `value_yellow` (number, visible: public, starts 2): Current value of Yellow
- the table: `value_purple` (number, visible: public, starts 2): Current value of Purple
- the table: `status_red` (text, visible: public, starts ''): Red's result this round: COLLECTED, CONTESTED or UNTOUCHED
- the table: `status_blue` (text, visible: public, starts ''): Blue's result this round: COLLECTED, CONTESTED or UNTOUCHED
- the table: `status_green` (text, visible: public, starts ''): Green's result this round: COLLECTED, CONTESTED or UNTOUCHED
- the table: `status_yellow` (text, visible: public, starts ''): Yellow's result this round: COLLECTED, CONTESTED or UNTOUCHED
- the table: `status_purple` (text, visible: public, starts ''): Purple's result this round: COLLECTED, CONTESTED or UNTOUCHED
- the table: `black_count` (number, visible: public, starts 0): How many players chose Black this round
- parameters (each must be an attribute holding this value, never a number buried in a step): num_colours = 5, initial_colour_value = 2, max_colour_value = 7, reset_value = 1, value_increment = 1, black_points = 1, favourite_bonus = 3, contested_gain = 0, rounds = 12, initial_score = 0
- the game ends with ONE ending whose `rank_by` is `you.score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
- anything else the game needs to keep track of is yours to design: name it as you like.

## How the platform works

The complete file format reference and two example games are in your system prompt. Follow them exactly: every key an
action accepts is listed there, and the loader refuses any other. The outcome must be decided by arithmetic: write ONE
ending, whose `when` is a calc condition and whose `rank_by` is the ranking in the interface below; no `result`, no `winner`, no prose
ending, no `llm` in an ending. Use calc for any rule that is arithmetic. For a spec step marked `judged`, make that step's `when` `{"prose": "<the judged sentence, verbatim>"}`: a referee answers it
true or false at play time. You may add `llm` wording to a tell, sync or update (never an ask or poll, never an outcome branch), but always keep its `text`, which is used when no
model answers. Choices made at the same moment are a `poll`. The end screen announces only the result: the ending's `text` says who won (`{result}`) and the final scores or deciding figures with
placeholders such as `{players[0].score}`, in a line or two, with no retelling of how the game went. End with `rank_by` as both examples do.

- Mistakes the loader has refused before, so avoid them:
  * A PLAYER attribute's `visible` is one of public, ally or others, never `none`. (`none` is only for table
    attributes.) For something only its owner should see, use `ally`.
  * A `poll` step has no `each` key, and no key the format reference does not list for `poll`. `each` belongs to `ask`.
  * Do not write a `deal` block unless it has the `into` it requires. Set starting values with `initial` on
    attributes, or with `set` operations in `setup`, instead.
  * Every key must be one the reference lists for that action; a misspelled or invented key is refused.
  * TALK that everyone hears is a `poll` with a free-text answer and `"broadcast": {"to": "all", "text": "Seat {seat} says: {value}"}`
    (or `"broadcast": "all"` with no `text`, which shows each message word for word). A broadcast may use ONLY `{value}` (what that
    player answered), `{seat}` (who) and table attributes: a name bound by `verify` is not set yet, so `{talk_msg}` reaches players as
    the literal braces, and the loader refuses it.
  * WHO answered what (who challenged, who blocked, who raised a hand) is `"store": "attr"` on the `poll` or `ask`, naming a PLAYER
    attribute declared under `attributes.player` (a `text` attribute for a choice). Each player's own answer is written to it and a calc reads
    them all: `count(p.said == 'Challenge' for p in players)`, `min([p.seat for p in players if p.said == 'Challenge'])`. A `verify`
    tally gives ONE winning value and loses who gave which: one "Challenge" against three "Pass" tallies to "Pass". Never write a seat
    number into a calc by guessing (`2 if active_seat == 1 else 1`); read it from a stored answer. Reset the stored attribute with a `set`
    to `""` (`players: "all"`) before each poll, so last round's answers do not count.
  * `meta.players` carries `min`, `max` and `suggested`, exactly as the task gives them: the console fills a table to the suggested size and the real-model tests play at it.
  * THE RULES TEXT SAYS BOTH OUTCOMES. For every decision point (a challenge, a block, a claim, a cost), say what happens when it is true AND when it is false,
    and whether the action still goes ahead; a player decides on this text and nothing else, and a check compares it with each numbered rule.
  * THE RULES TEXT PLAYERS READ IS THE DESIGN'S. `meta.rules` (the brief) says each mechanic in the design's own words and in its order: how a challenge is resolved,
    what a block costs, who counts when several answer. Do not paraphrase a mechanic: a reordered sentence is a different rule.
  * BOOKKEEPING IS HIDDEN. An attribute that only the game's own steps read (a scratch value, a counter, a copy of an option list, who is blocking) is declared
    hidden (`none` on the table, `ally` on a player), not `public`: every public attribute is printed into every player's prompt on every turn.
  * THE DEAL REMOVES WHAT IT DEALS. Every card put into a hand is taken out of the deck in the same step (see the deck recipe); after setup, deck plus hands holds
    exactly the cards the rules start with, and no card appears more often than the rules say.
  * OFFER ONLY WHAT A SEAT MAY DO. Build each seat's option list from its own state (see the offer pattern) and never refuse an answer afterwards
    and ask again: an option that is offered, taken and then taken back fails the pipeline's check.
  * A QUESTION WITH ONE POSSIBLE ANSWER IS NEVER WORTH ASKING ("pass" and nothing else): the engine answers it itself, but write the step so
    it is not asked at all, and never announce a seat's answer when the seat was not asked (eliminated players).
  * ASK ONLY WHAT IS NEEDED. Put a `when` on a question that applies only sometimes: a target is asked only for the actions that take one
    (`"when": {"calc": "chosen_action in ['Steal', 'Assassinate', 'Coup']"}`), a block only when something can be blocked.
  * A counter must not go below what the rules allow. Guard every payment and loss with an `if` (`"if": {"calc": "you.coins >= cost"}`,
    or check it before the action is allowed), and treat an action the player cannot afford as the cheapest legal one, as the rules say.
  * An answer to an `ask` or a `poll` exists ONLY if the step binds it with `verify: {"bind": "name"}`; a later `update`
    stores it with `"value": "$name"` (see the `rps` example, `card1`). A step that asks and binds nothing throws the
    answers away, and every score that depends on them stays at its starting value.
  * An attribute declared `"mutable": false` is set once, by an `initialize` step, and any other step that sets it crashes the game
    ("declared static and has already been dealt"). To set a hidden type or a starting value at setup, either use an `initialize`
    step or leave the attribute mutable.
  * Do not write steps that do nothing (for example an `if` of `{"calc": "False"}`), or two polls where one will do.
  * Reply with one complete JSON object: double-quoted keys and strings, no comments, no trailing commas. WRITE IT INDENTED,
    two spaces per level and one key per line, so you can see the nesting and count the brackets; do not put it on one line.
- Keep a round to at most 20 steps. Put several operations in one `update`'s `do` list, and use one `tell` for the
  reveal. A game with more steps than that is flagged as too large in the report, however well it plays, and `verify` tells you the count.

## A pattern that works (this complete game is tested: it loads, ends, and every attribute it declares is updated)

For "each player chooses in private, then the choices decide the score":
1. One `ask` per seat, addressed with `{"where": "you.seat == N"}`, with `"verify": {"bind": "aN"}`. The answer exists only because it is bound.
2. One `update` after both. It `set`s the bound answers into table attributes with `"$aN"`, and `adjust`s each player's score with a
   `calc` that may use `$aN` and `if ... else`.
3. A `check` with `when` and `against`, and ONE ending in `end` whose `rank_by` is `you.score`: the engine ranks the players by it.
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
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "rounds_left <= 0"
      },
      "rank_by": "you.score",
      "text": "{result} wins."
    }
  }
}
```

Your file is checked by the platform's loader, a rule that the outcome is arithmetic, random play, a check that every
attribute is actually updated, and tests written independently from the rules. If it is refused you will be told why and
shown your file again; fix what is wrong and keep the rest.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "ripening_hats",
    "name": "Ripening Hats",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Twelve rounds of secretly picking hat colours: a colour only you pick pays its ripening value, with a bonus for your secret favourite; contested colours pay nothing."
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
        "key": "favourite",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "colour_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "value_red",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_blue",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_green",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_yellow",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_purple",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_yellow",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "count_purple",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "status_red",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "status_blue",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "status_green",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "status_yellow",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "status_purple",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "black_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "num_colours",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "initial_colour_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_colour_value",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "reset_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "value_increment",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "black_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "favourite_bonus",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "contested_gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "initial_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "set colour values",
      "do": [
        {
          "set": {
            "key": "value_red",
            "value": {
              "calc": "initial_colour_value"
            }
          }
        },
        {
          "set": {
            "key": "value_blue",
            "value": {
              "calc": "initial_colour_value"
            }
          }
        },
        {
          "set": {
            "key": "value_green",
            "value": {
              "calc": "initial_colour_value"
            }
          }
        },
        {
          "set": {
            "key": "value_yellow",
            "value": {
              "calc": "initial_colour_value"
            }
          }
        },
        {
          "set": {
            "key": "value_purple",
            "value": {
              "calc": "initial_colour_value"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "set scores and round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "initial_score"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal favourites",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "colour_pool[min(len(colour_pool) - 1, int(uniform(0, len(colour_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "colour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "colour_pool[min(len(colour_pool) - 1, int(uniform(0, len(colour_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "colour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "colour_pool[min(len(colour_pool) - 1, int(uniform(0, len(colour_pool))))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "colour_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "colour_pool[min(len(colour_pool) - 1, int(uniform(0, len(colour_pool))))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "colour_pool",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your favourite",
      "mode": "self",
      "to": "all",
      "fields": [
        "favourite",
        "score"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "tell",
      "phase": "announce",
      "label": "round begins",
      "to": "all",
      "text": "Round {round} of {rounds}. Values: Red {value_red}, Blue {value_blue}, Green {value_green}, Yellow {value_yellow}, Purple {value_purple}."
    },
    {
      "use": "update",
      "phase": "announce",
      "label": "clear last round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "message",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 30
      },
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are shown once all are in. Talk binds no one."
    },
    {
      "use": "poll",
      "phase": "choice",
      "label": "pick a hat",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Purple",
          "Black"
        ]
      },
      "store": "choice",
      "text": "Secretly choose one of Red, Blue, Green, Yellow, Purple or Black. A colour only you choose pays its value (plus the favourite bonus if it is your favourite); a colour chosen by two or more pays nothing; Black always pays {black_points}."
    },
    {
      "use": "update",
      "phase": "collect",
      "label": "count choices",
      "do": [
        {
          "set": {
            "key": "count_red",
            "value": {
              "calc": "count(p.choice == 'Red' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "count_blue",
            "value": {
              "calc": "count(p.choice == 'Blue' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "count_green",
            "value": {
              "calc": "count(p.choice == 'Green' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "count_yellow",
            "value": {
              "calc": "count(p.choice == 'Yellow' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "count_purple",
            "value": {
              "calc": "count(p.choice == 'Purple' for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "black_count",
            "value": {
              "calc": "count(p.choice == 'Black' for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "collect",
      "label": "collect",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(black_points if you.choice == 'Black' else 0) + ((((value_red + (favourite_bonus if you.favourite == 'Red' else 0)) if count_red == 1 else contested_gain)) if you.choice == 'Red' else 0) + ((((value_blue + (favourite_bonus if you.favourite == 'Blue' else 0)) if count_blue == 1 else contested_gain)) if you.choice == 'Blue' else 0) + ((((value_green + (favourite_bonus if you.favourite == 'Green' else 0)) if count_green == 1 else contested_gain)) if you.choice == 'Green' else 0) + ((((value_yellow + (favourite_bonus if you.favourite == 'Yellow' else 0)) if count_yellow == 1 else contested_gain)) if you.choice == 'Yellow' else 0) + ((((value_purple + (favourite_bonus if you.favourite == 'Purple' else 0)) if count_purple == 1 else contested_gain)) if you.choice == 'Purple' else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "collect",
      "label": "colour results",
      "do": [
        {
          "set": {
            "key": "status_red",
            "value": {
              "calc": "'COLLECTED' if count_red == 1 else ('CONTESTED' if count_red >= 2 else 'UNTOUCHED')"
            }
          }
        },
        {
          "set": {
            "key": "status_blue",
            "value": {
              "calc": "'COLLECTED' if count_blue == 1 else ('CONTESTED' if count_blue >= 2 else 'UNTOUCHED')"
            }
          }
        },
        {
          "set": {
            "key": "status_green",
            "value": {
              "calc": "'COLLECTED' if count_green == 1 else ('CONTESTED' if count_green >= 2 else 'UNTOUCHED')"
            }
          }
        },
        {
          "set": {
            "key": "status_yellow",
            "value": {
              "calc": "'COLLECTED' if count_yellow == 1 else ('CONTESTED' if count_yellow >= 2 else 'UNTOUCHED')"
            }
          }
        },
        {
          "set": {
            "key": "status_purple",
            "value": {
              "calc": "'COLLECTED' if count_purple == 1 else ('CONTESTED' if count_purple >= 2 else 'UNTOUCHED')"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "collect",
      "label": "results",
      "to": "all",
      "text": "Red {status_red}, Blue {status_blue}, Green {status_green}, Yellow {status_yellow}, Purple {status_purple}. Black chosen by {black_count}."
    },
    {
      "use": "update",
      "phase": "ripen",
      "label": "value update",
      "do": [
        {
          "set": {
            "key": "value_red",
            "value": {
              "calc": "reset_value if count_red == 1 else min(max_colour_value, value_red + value_increment)"
            }
          }
        },
        {
          "set": {
            "key": "value_blue",
            "value": {
              "calc": "reset_value if count_blue == 1 else min(max_colour_value, value_blue + value_increment)"
            }
          }
        },
        {
          "set": {
            "key": "value_green",
            "value": {
              "calc": "reset_value if count_green == 1 else min(max_colour_value, value_green + value_increment)"
            }
          }
        },
        {
          "set": {
            "key": "value_yellow",
            "value": {
              "calc": "reset_value if count_yellow == 1 else min(max_colour_value, value_yellow + value_increment)"
            }
          }
        },
        {
          "set": {
            "key": "value_purple",
            "value": {
              "calc": "reset_value if count_purple == 1 else min(max_colour_value, value_purple + value_increment)"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "ripen",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "fields": [
        "score",
        "favourite"
      ],
      "text": "Where you stand:"
    },
    {
      "use": "update",
      "phase": "ripen",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "ripen",
      "label": "after the last round",
      "when": {
        "calc": "round > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round > rounds"
      },
      "rank_by": "you.score",
      "reveal": [
        "favourite",
        "score"
      ],
      "text": "Winner: {result}. Final [seat, score, favourite]: {[[p.seat, p.score, p.favourite] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "There are {num_colours} hat colours, in this fixed order: Red, Blue, Green, Yellow, Purple. Each colour has a public value, and all five start at {initial_colour_value}. Each player is dealt a secret favourite colour at random, all different; only that player knows it. Every player has a private score starting at {initial_score}, which only that player can see.\n\nThe game lasts {rounds} rounds. Each round:\n1. Everyone is told the round number and the current value of each of the 5 colours.\n2. Talk: everyone writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk binds no one.\n3. Choice: everyone simultaneously and secretly chooses one of Red, Blue, Green, Yellow, Purple or Black.\n4. Collection. A player who chose Black adds {black_points} to their score. A player who chose a colour that no other player chose this round collects it: they add that colour's current value to their score, plus {favourite_bonus} more if it is their favourite; if it is not their favourite, they add only the colour's value. A colour chosen by two or more players is contested, and none of them gains anything ({contested_gain}).\n5. Everyone is told, without naming players: for each colour, whether it was COLLECTED (exactly one chooser), CONTESTED (two or more) or UNTOUCHED (no one), and how many players chose Black. Individual choices and scores are never announced.\n6. Value update. Each colour that was collected this round resets to {reset_value}. Each colour that was contested or untouched gains +{value_increment}, to a maximum of {max_colour_value} (a colour at {max_colour_value} stays there).\n\nAfter round {rounds} the game ends and all favourites and scores are revealed. The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw among them (they share the result)."
}
```
````
