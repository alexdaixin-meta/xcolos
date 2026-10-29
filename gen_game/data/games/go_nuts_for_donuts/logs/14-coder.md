# 14 coder

- time: 2026-10-28T04:25:41+00:00 (54.3s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 417c1af2428a3004, reply sha256 febaedd10712721f

## Sent

````
# Task: write the XColos game file for "Go Nuts for Donuts: Premium Picks"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP: There are exactly 4 players, each starting with 0 points and 0 donuts collected.

THE ROW: Every round the same five donuts are offered:
- Glazed, worth 9 points
- Jelly, worth 6 points
- Cruller, worth 4 points
- Sprinkle, worth 2 points
- Plain, worth 1 point

SECRET SPLIT: Before round 1, each player privately and simultaneously writes a whole number G from 0 to 6. That player has G Glazed picks and 6 minus G Jelly picks. Nobody else is told this number, at any time during the game.

EACH ROUND (10 rounds):
1. ANNOUNCE: The round number is announced, along with, for every player, their points, how many donuts they have collected, and how many Glazed choices and how many Jelly choices they have made so far that used a pick. Remaining picks are not announced.
2. TALK: Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.
3. CHOOSE: Every player secretly and simultaneously chooses exactly one donut: Glazed, Jelly, Cruller, Sprinkle or Plain.
4. CHECK PICKS: A player who chose Glazed with no Glazed picks left, or Jelly with no Jelly picks left, has made a VOID choice. A void choice scores nothing, uses no pick, and does not count as choosing that donut for anyone else.
5. REVEAL: All four choices are revealed together, with any void choice marked VOID.
6. RESOLVE: For each donut, count the non-void players who chose it. If exactly one did, that player gains the donut's value and adds 1 to their donuts collected. If two or more did, the donut is discarded and none of them gains anything. A donut nobody chose has no effect.
7. USE PICKS: Every non-void Glazed choice uses up one of that player's Glazed picks, and every non-void Jelly choice uses up one of that player's Jelly picks. This happens whether the donut was won or discarded.
8. SCORE: Each player's gain this round and everyone's new totals are announced.

END: The game ends after round 10. Unused picks are worth nothing.

How the winner is decided: The player with the highest point total after round 10 wins. If several players tie for the highest total, the one among them with the most donuts collected wins. If they are still tied, the game is a draw among those players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Go Nuts for Donuts: Premium Picks (4 to 4 players, best with 4)

Four players secretly split 6 premium picks between Glazed and Jelly, then for 10 rounds talk and simultaneously pick one of five donuts; a donut scores only for a lone chooser.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. points total
  - each player: donuts (number, starts 0); everyone sees it. donuts collected (won as lone chooser)
  - each player: glazed_picks (number, starts 0); only its owner sees it. Glazed picks remaining (G at start); never told to others
  - each player: jelly_picks (number, starts 0); only its owner sees it. Jelly picks remaining (6 - G at start); never told to others
  - each player: glazed_used (number, starts 0); everyone sees it. non-void Glazed choices made so far (announced each round)
  - each player: jelly_used (number, starts 0); everyone sees it. non-void Jelly choices made so far (announced each round)
  - each player: choice (text, starts ''); only its owner sees it. this round's donut choice, secret until the reveal
  - each player: void (bool, starts False); everyone sees it. this round's choice was VOID (Glazed with 0 glazed_picks or Jelly with 0 jelly_picks)
  - each player: gain (number, starts 0); everyone sees it. points gained this round
  - the table: round (number, starts 0); everyone sees it. current round number (1 to 10)
  - parameters, each kept as a table attribute: player_count = 4, rounds = 10, glazed_value = 9, jelly_value = 6, cruller_value = 4, sprinkle_value = 2, plain_value = 1, premium_picks_total = 6, split_min = 0, split_max = 6, lone_chooser_count = 1, donut_collected_increment = 1, pick_use_per_choice = 1, tiebreak_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with score 0, donuts 0, glazed_used 0 and jelly_used 0.
  2. All players are polled at once, privately, for a whole number G from 0 to 6.
  3. Each player's glazed_picks is set to G and jelly_picks to 6 - G. Only the owner sees these values, and nobody else is ever told G.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1
  2. [tell] all players. What happens: Announce the round number and, for every seat, score, donuts, glazed_used and jelly_used. Remaining picks are not announced.
  3. [poll] all players answers: short text message. What happens: Every message is broadcast to all once all are in: 'Seat {seat} says: {value}'. Messages are not binding.
  4. [poll] all players answers: one of: Glazed, Jelly, Cruller, Sprinkle, Plain. What happens: choice = answer (secret until the reveal)
  5. [update] all players. What happens: void = (choice == 'Glazed' and glazed_picks == 0) or (choice == 'Jelly' and jelly_picks == 0); gain = 0
  6. [tell] all players. What happens: Reveal every seat's choice together, with VOID shown for each seat whose void is true.
  7. [update] all players. What happens: For each donut D, let n_D = the number of seats with choice == D and void == false. A seat with void == false whose choice D has n_D == 1 gets gain = value of D (Glazed 9, Jelly 6, Cruller 4, Sprinkle 2, Plain 1), score += gain and donuts += 1. When n_D >= 2, nobody gains from D.
  8. [update] all players. What happens: If void == false and choice == 'Glazed': glazed_picks -= 1 and glazed_used += 1. If void == false and choice == 'Jelly': jelly_picks -= 1 and jelly_used += 1. This applies whether the donut was won or discarded.
  9. [tell] all players. What happens: Announce each seat's gain this round and every seat's new score and donuts.
  10. [check] all players. What happens: End the game if round >= 10, otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player has score 0, donuts 0, glazed_used 0 and jelly_used 0.
  R2. When a player answers G (a whole number from 0 to 6) before round 1, then glazed_picks = G and jelly_picks = 6 - G, visible only to that player.
  R3. No player other than the owner is ever shown that player's G, glazed_picks or jelly_picks.
  R4. When each round begins, round increases by 1, and the round number plus every seat's score, donuts, glazed_used and jelly_used are announced.
  R5. When the talk step runs, every player submits one short message simultaneously, and all four messages are shown to everyone only after all are in.
  R6. When the choose step runs, every player simultaneously chooses exactly one of Glazed, Jelly, Cruller, Sprinkle or Plain.
  R7. When a player chooses Glazed with glazed_picks == 0, or Jelly with jelly_picks == 0, then void = true. Otherwise void = false.
  R8. When a choice is void, that player gains 0, uses no pick, and is not counted as choosing that donut.
  R9. When choices are revealed, all four choices are shown together, and each void choice is marked VOID.
  R10. When exactly one non-void player chooses Glazed, that player gains 9 points and donuts += 1.
  R11. When exactly one non-void player chooses Jelly, that player gains 6 points and donuts += 1.
  R12. When exactly one non-void player chooses Cruller, that player gains 4 points and donuts += 1.
  R13. When exactly one non-void player chooses Sprinkle, that player gains 2 points and donuts += 1.
  R14. When exactly one non-void player chooses Plain, that player gains 1 point and donuts += 1.
  R15. When two or more non-void players choose the same donut, each of them gains 0 for it and donuts is unchanged.
  R16. When a player makes a non-void Glazed choice, glazed_picks decreases by 1 and glazed_used increases by 1, whether the donut was won or discarded.
  R17. When a player makes a non-void Jelly choice, jelly_picks decreases by 1 and jelly_used increases by 1, whether the donut was won or discarded.
  R18. When a round ends, each seat's gain and new score and donuts totals are announced.
  R19. When round 10 has been resolved, the game ends, and unused picks are worth 0.
  R20. When the game ends, the highest score wins. A tie on score is broken by the most donuts, and players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Secret split before round 1: how many Glazed picks G? | asked: every seat | options: a whole number from 0 to 6
  - Talk: your message this round | asked: every seat | options: a short free-text message
  - Choose a donut | asked: every seat | options: Glazed, Jelly, Cruller, Sprinkle, Plain, offered in every situation. A Glazed or Jelly choice made with no matching picks left is allowed but void.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 10
  - each player's standing: you.score * 100 + you.donuts (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest point total wins. Among players tied on points, the one with the most donuts collected wins. Players still tied share the win, which stands for the source's draw.
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

- each player: `score` (number, visible: public, starts 0): points total
- each player: `donuts` (number, visible: public, starts 0): donuts collected (won as lone chooser)
- each player: `glazed_used` (number, visible: public, starts 0): non-void Glazed choices made so far (announced each round)
- each player: `jelly_used` (number, visible: public, starts 0): non-void Jelly choices made so far (announced each round)
- each player: `void` (bool, visible: public, starts False): this round's choice was VOID (Glazed with 0 glazed_picks or Jelly with 0 jelly_picks)
- the table: `round` (number, visible: public, starts 0): current round number (1 to 10)
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 4, rounds = 10, glazed_value = 9, jelly_value = 6, cruller_value = 4, sprinkle_value = 2, plain_value = 1, premium_picks_total = 6, split_min = 0, split_max = 6, lone_chooser_count = 1, donut_collected_increment = 1, pick_use_per_choice = 1, tiebreak_multiplier = 100
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

## Guidance from the last attempt

The previous attempt had problems:

The secret split must be applied exactly once, from each player's own answer to the simultaneous G poll (0 to 6). Set `glazed_picks` = G and `jelly_picks` = `premium_picks_total` - G for that player only. Remove the second assignment that overwrites the picks, or make sure `split_g` is stored from the answer before any step reads it, so it is never read as its default 0. Then check the following. (1) `void` is set per player each round: true only if the choice is Glazed with `glazed_picks` = 0 or Jelly with `jelly_picks` = 0, otherwise false. (2) Void choices are left out of the per-donut counts. (3) A lone non-void chooser gains the donut's value and +`donut_collected_increment`. (4) Every non-void Glazed or Jelly choice decrements the matching picks and increments `glazed_used` or `jelly_used`, whether the donut was won or discarded.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "go_nuts_for_donuts_premium_picks",
    "name": "Go Nuts for Donuts: Premium Picks",
    "players": {
      "min": 4,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Four players secretly split 6 premium picks between Glazed and Jelly, then for 10 rounds talk and pick one of five donuts; a donut scores only for a lone chooser."
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
      },
      {
        "key": "donuts",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "glazed_picks",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "jelly_picks",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "glazed_used",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "jelly_used",
        "visible": "public",
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
        "key": "void",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "gain",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "split_g",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "shown",
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
        "initial": 0
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "glazed_value",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "jelly_value",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cruller_value",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "sprinkle_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "plain_value",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "premium_picks_total",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "split_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "split_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "lone_chooser_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "donut_collected_increment",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick_use_per_choice",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tiebreak_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting totals",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "donuts",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "glazed_used",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "jelly_used",
            "value": 0
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
      "use": "poll",
      "phase": "split",
      "label": "secret split",
      "when": {
        "calc": "round == 0"
      },
      "to": "acting",
      "answer": {
        "type": "number",
        "min": {
          "calc": "split_min"
        },
        "max": {
          "calc": "split_max"
        }
      },
      "store": "split_g",
      "text": "Secretly choose how many of your {premium_picks_total} premium picks are Glazed picks: a whole number G from {split_min} to {split_max}. You get G Glazed picks and {premium_picks_total} minus G Jelly picks. Nobody else is ever told this number."
    },
    {
      "use": "update",
      "phase": "split",
      "label": "apply the split",
      "when": {
        "calc": "round == 0"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "glazed_picks",
            "value": {
              "calc": "you.split_g"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "jelly_picks",
            "value": {
              "calc": "premium_picks_total - you.split_g"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "announce",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
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
      "use": "tell",
      "phase": "announce",
      "label": "round announcement",
      "to": "all",
      "text": "Round {round} of {rounds}. Seat 1: {players[0].score} points, {players[0].donuts} donuts, Glazed used {players[0].glazed_used}, Jelly used {players[0].jelly_used}. Seat 2: {players[1].score} points, {players[1].donuts} donuts, Glazed used {players[1].glazed_used}, Jelly used {players[1].jelly_used}. Seat 3: {players[2].score} points, {players[2].donuts} donuts, Glazed used {players[2].glazed_used}, Jelly used {players[2].jelly_used}. Seat 4: {players[3].score} points, {players[3].donuts} donuts, Glazed used {players[3].glazed_used}, Jelly used {players[3].jelly_used}."
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
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are shown once all are in. Messages are not binding."
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "choose a donut",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Glazed",
          "Jelly",
          "Cruller",
          "Sprinkle",
          "Plain"
        ]
      },
      "store": "choice",
      "text": "Secretly choose one donut: Glazed ({glazed_value}), Jelly ({jelly_value}), Cruller ({cruller_value}), Sprinkle ({sprinkle_value}) or Plain ({plain_value}). Glazed needs a Glazed pick left and Jelly needs a Jelly pick left; without one the choice is VOID and scores nothing."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "check picks",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "void",
            "value": {
              "calc": "(you.choice == 'Glazed' and you.glazed_picks == 0) or (you.choice == 'Jelly' and you.jelly_picks == 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "gain",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "shown",
            "value": {
              "calc": "you.choice + (' (VOID)' if you.void else '')"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "reveal",
      "to": "all",
      "text": "Choices revealed for round {round}: Seat 1 {players[0].shown}, Seat 2 {players[1].shown}, Seat 3 {players[2].shown}, Seat 4 {players[3].shown}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve donuts",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "gain",
            "value": {
              "calc": "(glazed_value if you.choice == 'Glazed' else jelly_value if you.choice == 'Jelly' else cruller_value if you.choice == 'Cruller' else sprinkle_value if you.choice == 'Sprinkle' else plain_value if you.choice == 'Plain' else 0) if ((not you.void) and count((p.choice == you.choice and not p.void) for p in players) == lone_chooser_count) else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.gain"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "donuts",
            "value": {
              "calc": "donut_collected_increment if you.gain > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "use picks",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "glazed_picks",
            "value": {
              "calc": "-pick_use_per_choice if ((not you.void) and you.choice == 'Glazed') else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "glazed_used",
            "value": {
              "calc": "pick_use_per_choice if ((not you.void) and you.choice == 'Glazed') else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "jelly_picks",
            "value": {
              "calc": "-pick_use_per_choice if ((not you.void) and you.choice == 'Jelly') else 0"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "jelly_used",
            "value": {
              "calc": "pick_use_per_choice if ((not you.void) and you.choice == 'Jelly') else 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "score",
      "label": "round scores",
      "to": "all",
      "text": "Round {round} results. Seat 1 gained {players[0].gain} (total {players[0].score} points, {players[0].donuts} donuts). Seat 2 gained {players[1].gain} (total {players[1].score} points, {players[1].donuts} donuts). Seat 3 gained {players[2].gain} (total {players[2].score} points, {players[2].donuts} donuts). Seat 4 gained {players[3].gain} (total {players[3].score} points, {players[3].donuts} donuts)."
    },
    {
      "use": "check",
      "phase": "score",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.score * 100 + you.donuts",
      "text": "Winner: {result}. Final scores (points/donuts): Seat 1 {players[0].score}/{players[0].donuts}, Seat 2 {players[1].score}/{players[1].donuts}, Seat 3 {players[2].score}/{players[2].donuts}, Seat 4 {players[3].score}/{players[3].donuts}."
    }
  },
  "limits": {
    "rounds": 11,
    "rounds_max": 11,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "There are exactly {player_count} players, each starting with 0 points and 0 donuts collected.\n\nTHE ROW: Every round the same five donuts are offered: Glazed, worth {glazed_value} points; Jelly, worth {jelly_value} points; Cruller, worth {cruller_value} points; Sprinkle, worth {sprinkle_value} points; Plain, worth {plain_value} point.\n\nSECRET SPLIT: Before round 1, each player privately and simultaneously writes a whole number G from {split_min} to {split_max}. That player has G Glazed picks and {premium_picks_total} minus G Jelly picks. Nobody else is told this number, at any time during the game.\n\nEACH ROUND ({rounds} rounds):\n1. ANNOUNCE: The round number is announced, along with, for every player, their points, how many donuts they have collected, and how many Glazed choices and how many Jelly choices they have made so far that used a pick. Remaining picks are not announced.\n2. TALK: Every player writes one short message at the same time, without seeing the others. All four messages are then shown to everyone. Messages are not binding.\n3. CHOOSE: Every player secretly and simultaneously chooses exactly one donut: Glazed, Jelly, Cruller, Sprinkle or Plain.\n4. CHECK PICKS: A player who chose Glazed with no Glazed picks left, or Jelly with no Jelly picks left, has made a VOID choice. A void choice scores nothing, uses no pick, and does not count as choosing that donut for anyone else. A Glazed or Jelly choice made with a matching pick left is not void and counts normally.\n5. REVEAL: All four choices are revealed together, with any void choice marked VOID.\n6. RESOLVE: For each donut, count the non-void players who chose it. If exactly one did, that player gains the donut's value and adds 1 to their donuts collected. If two or more did, the donut is discarded and none of them gains anything. A donut nobody chose has no effect.\n7. USE PICKS: Every non-void Glazed choice uses up one of that player's Glazed picks, and every non-void Jelly choice uses up one of that player's Jelly picks. This happens whether the donut was won or discarded.\n8. SCORE: Each player's gain this round and everyone's new totals are announced.\n\nEND: The game ends after round {rounds}. Unused picks are worth nothing. The player with the highest point total wins. If several players tie for the highest total, the one among them with the most donuts collected wins. If they are still tied, they share the win."
}
```
````
