# Task: write the XColos game file for "Go Nuts for Donuts: Secret Budget"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

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

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Go Nuts for Donuts: Secret Budget (4 to 4 players, best with 4)

Four players spend 10 simultaneous rounds picking one of five donuts. A donut scores only for a player who picks it alone, and each player has a secret split of 6 premium picks between Glazed and Jelly.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Points from donuts won alone
  - each player: donuts (number, starts 0); everyone sees it. Number of donuts won
  - each player: split_g (number, starts 0); only its owner sees it. Secret number of the 6 premium picks that are Glazed picks. Jelly picks are 6 - split_g. Set once by the split poll and never changed.
  - each player: glazed_used (number, starts 0); everyone sees it. Non-void Glazed choices made so far
  - each player: jelly_used (number, starts 0); everyone sees it. Non-void Jelly choices made so far
  - each player: choice (text, starts ''); everyone sees it. This round's donut choice, gathered by a simultaneous poll and shown at the reveal
  - each player: void (bool, starts False); everyone sees it. Whether this round's choice is void
  - each player: gained (number, starts 0); everyone sees it. Points gained this round
  - the table: round (number, starts 0); everyone sees it. Rounds completed
  - the table: count_glazed (number, starts 0); everyone sees it. Non-void Glazed choices this round
  - the table: count_jelly (number, starts 0); everyone sees it. Non-void Jelly choices this round
  - the table: count_cruller (number, starts 0); everyone sees it. Cruller choices this round
  - the table: count_sprinkle (number, starts 0); everyone sees it. Sprinkle choices this round
  - the table: count_plain (number, starts 0); everyone sees it. Plain choices this round
  - parameters, each kept as a table attribute: glazed_points = 9, jelly_points = 6, cruller_points = 4, sprinkle_points = 2, plain_points = 1, rounds = 10, premium_picks = 6, split_g_min = 0, split_g_max = 6, rank_score_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Initialize every player with score 0, donuts 0, split_g 0, glazed_used 0 and jelly_used 0, and set round to 0.
  2. Poll all players at once: 'How many of your 6 premium picks are Glazed picks?' The options are 0, 1, 2, 3, 4, 5 and 6. Store each answer as that player's split_g, visible only to that player.
  3. Sync each player their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Reset each player's choice to empty, void to false and gained to 0. Reset count_glazed, count_jelly, count_cruller, count_sprinkle and count_plain to 0.
  2. [poll] all players answers: one short text message. What happens: Gather all messages at once, then broadcast to all: 'Seat {seat} says: {value}'. Messages bind no one.
  3. [sync] all players. What happens: Privately remind each player of their Glazed picks left (split_g - glazed_used) and Jelly picks left (6 - split_g - jelly_used).
  4. [poll] all players answers: one of: Glazed, Jelly, Cruller, Sprinkle, Plain. What happens: Store each answer in that player's choice.
  5. [update] all players. What happens: Set void = true if (choice == Glazed and glazed_used >= split_g) or (choice == Jelly and jelly_used >= 6 - split_g). Otherwise set void = false.
  6. [update] all players. What happens: Set count_glazed to the number of players with choice Glazed and not void, and count_jelly to the number with choice Jelly and not void. Set count_cruller, count_sprinkle and count_plain to the number of players who chose each.
  7. [update] all players. What happens: For each non-void player whose donut's count == 1, set gained to that donut's points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), add gained to score and add 1 to donuts. Every other player gets gained 0.
  8. [update] all players. What happens: Every player with a non-void Glazed choice adds 1 to glazed_used. Every player with a non-void Jelly choice adds 1 to jelly_used. This happens whether the donut was won or discarded.
  9. [tell] all players. What happens: Reveal each player's choice (marked VOID if void), gained, score and donuts. split_g is never shown.
  10. [update] all players. What happens: Add 1 to round.
  11. [check] all players. What happens: End the game if round >= 10. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. Before round 1, each player's answer to the split poll (0 to 6) is stored as split_g, visible only to that player, and is never changed afterwards.
  R2. When a player has split_g = s, they have s Glazed picks and 6 - s Jelly picks.
  R3. Each round, every player sends one message at the same time, and all messages are shown to everyone only after all are in.
  R4. Before choosing, each player is privately told split_g - glazed_used Glazed picks left and 6 - split_g - jelly_used Jelly picks left.
  R5. When a player chooses Glazed while glazed_used >= split_g, the choice is void, gains 0 and does not count toward Glazed.
  R6. When a player chooses Jelly while jelly_used >= 6 - split_g, the choice is void, gains 0 and does not count toward Jelly.
  R7. When a player chooses Cruller, Sprinkle or Plain, the choice is never void.
  R8. When exactly 1 player makes a non-void choice of a donut, that player gains its points (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1) and adds 1 to donuts.
  R9. When 2 or more players make a non-void choice of the same donut, none of them gains points or donuts for it.
  R10. When a player makes a non-void Glazed choice, glazed_used rises by 1 whether the donut was won or discarded.
  R11. When a player makes a non-void Jelly choice, jelly_used rises by 1 whether the donut was won or discarded.
  R12. When a choice is void, glazed_used and jelly_used do not change.
  R13. When a void choice of Glazed is made alongside one non-void Glazed choice, the non-void player still wins the Glazed for 9 points.
  R14. After each round, every player's choice (marked VOID if void), gain, score and donuts are shown to everyone, and split_g is never shown.
  R15. When round 10 ends, the game ends.
  R16. At the end, the player with the highest score * 100 + donuts wins, and players tied on that value share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Secret split: how many of your 6 premium picks are Glazed picks? | asked: all players, at once, before round 1 | options: 0, 1, 2, 3, 4, 5, 6
  - Talk | asked: all players, at once, each round | options: one short free-text message
  - Choose a donut | asked: all players, at once, each round | options: Glazed, Jelly, Cruller, Sprinkle, Plain, always all five, even with no picks left (such a choice is then void)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 10
  - each player's standing: you.score * 100 + you.donuts (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The highest score wins, with ties broken by most donuts won. Players still level on both share the win, which is a draw among them.
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

- each player: `score` (number, visible: public, starts 0): Points from donuts won alone
- each player: `donuts` (number, visible: public, starts 0): Number of donuts won
- parameters (each must be an attribute holding this value, never a number buried in a step): glazed_points = 9, jelly_points = 6, cruller_points = 4, sprinkle_points = 2, plain_points = 1, rounds = 10, premium_picks = 6, split_g_min = 0, split_g_max = 6, rank_score_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.donuts`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
