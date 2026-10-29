# 13 coder

- time: 2026-10-27T08:45:28+00:00 (70.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 c2577f2facaf6606, reply sha256 92fc9ade04e48888

## Sent

````
# Task: write the XColos game file for "Bidder's Choice: Shared Worth"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP
1. There are six objects, named A, B, C, D, E and F.
2. Each player starts with 20 coins.
3. Each player is privately dealt a random assignment of the values 2, 4, 6, 8, 10 and 14 to the six objects, one value per object, independently of the other players. Each player sees only their own assignment. Every player's values therefore total 44.

ROUNDS
The game lasts exactly 6 rounds. Each round:
1. TALK. Every player writes one short public message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding and may be false.
2. BID. Every player at the same moment submits a sealed bid. A bid is a whole number from 0 up to the coins that player currently holds.
3. RESOLVE. The highest bid wins the round. If several players tie for highest, the tied player holding the fewest objects wins. If they are still tied, one of them is chosen at random with equal chance.
4. PAY. The round winner pays their bid: it is subtracted from their coins and leaves the game. All other players pay nothing.
5. PICK. The round winner chooses one object still in the pool. That object is removed from the pool and added to the winner's holdings, and they gain their own private value for it. A player may win any number of rounds.
6. ANNOUNCE. Everyone is told all bids, who won, the price paid and which object was taken. Private values are never revealed.

END
After round 6 all six objects have been taken. Each player's final score is their remaining coins plus the sum of their own private values for the objects they hold. All values are then revealed.

How the winner is decided: The player with the highest final score (remaining coins plus their own values for the objects they hold) wins. If two or more players tie for the highest score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Bidder's Choice: Shared Worth (3 to 5 players, best with 4)

Over 6 rounds players talk, then bid sealed coins for the right to take one of six objects A-F that each values privately; the highest coins plus own object values wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 20); everyone sees it. Coins the player currently holds. Everyone can track this because winning prices are announced.
  - each player: values (list, starts "a private random ordering of [2,4,6,8,10,14]; position 1..6 is the player's value for object A..F"); only its owner sees it. The player's private value for each object.
  - each player: holdings (list, starts []); everyone sees it. Names of the objects this player has taken.
  - each player: object_count (number, starts 0); everyone sees it. How many objects the player holds. Used to break ties.
  - each player: object_points (number, starts 0); only its owner sees it. Sum of the player's own private values for the objects they hold.
  - each player: bid (number, starts 0); only its owner sees it. The player's sealed bid this round.
  - each player: last_bid (number, starts 0); everyone sees it. The player's bid in the last resolved round, revealed at the announcement.
  - each player: final_score (number, starts 0); everyone sees it. coins + object_points, set and revealed after round 6.
  - the table: pool (list, starts ['A', 'B', 'C', 'D', 'E', 'F']); everyone sees it. Objects not yet taken.
  - the table: round (number, starts 0); everyone sees it. The current round number, from 1 to 6.
  - the table: high_bid (number, starts 0); everyone sees it. The highest bid this round.
  - the table: winner_seat (number, starts 0); everyone sees it. The seat that won this round.
  - the table: price (number, starts 0); everyone sees it. The amount the round winner paid.
  - the table: last_object (text, starts ''); everyone sees it. The object taken this round.
  - parameters, each kept as a table attribute: object_count_total = 6, starting_coins = 20, value_1 = 2, value_2 = 4, value_3 = 6, value_4 = 8, value_5 = 10, value_6 = 14, values_total_per_player = 44, rounds = 6, min_bid = 0, objects_won_per_round = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The pool is set to the six objects A, B, C, D, E and F.
  2. Each player's coins are set to 20.
  3. Each player is privately dealt a random assignment of the values 2, 4, 6, 8, 10 and 14 to objects A to F, one value per object, independently of the other players. This is stored in that player's values list, visible only to them, and totals 44.
  4. Each player's holdings start empty, with object_count 0 and object_points 0.
  5. A sync step sends each player their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; announce 'Round {round} of 6'.
  2. [poll] all players answers: short free text: one public message, not binding and possibly false. What happens: After all are in, each message is broadcast to all as 'Seat {seat} says: {value}'.
  3. [poll] all players answers: a whole number from 0 to that player's coins. What happens: Sets each player's bid. Nobody sees any bid until all are in.
  4. [update] all players. What happens: high_bid = the maximum bid. Among players whose bid == high_bid, keep those with the minimum object_count. winner_seat = that player, or one of them chosen at random with equal chance if several remain. price = high_bid. Each player's last_bid = bid.
  5. [update] the winner_seat. What happens: The winner's coins -= price. The paid coins leave the game. All other players pay nothing.
  6. [ask] the winner_seat answers: one object name from the current pool. What happens: last_object = the choice; remove it from pool; append it to the winner's holdings; the winner's object_count += 1; the winner's object_points += the winner's values entry for that object (A=1st ... F=6th).
  7. [tell] all players. What happens: Announce every seat's last_bid, winner_seat, price and last_object. Private values are not revealed.
  8. [update] all players. What happens: When round == 6: each player's final_score = coins + object_points, and every player's values and object_points are revealed to everyone.
  9. [check] all players. What happens: End the game if round == 6; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has 20 coins, no objects, and the pool is A, B, C, D, E, F.
  R2. When values are dealt, then each player privately receives the values 2, 4, 6, 8, 10 and 14, one per object A-F in random order, independently of others, totalling 44.
  R3. When a player's values are dealt, then only that player sees them until the game ends.
  R4. When a round begins, then every player writes one short message at the same time, and all messages are shown to everyone only after all are in.
  R5. When bidding, then every player simultaneously submits a whole-number bid from 0 to their current coins.
  R6. When one player has the strictly highest bid, then that player wins the round.
  R7. When several players tie for the highest bid, then the tied player with the fewest objects wins.
  R8. When tied players also hold equally few objects, then the winner is chosen at random among them with equal chance.
  R9. When a player wins a round with bid X, then their coins drop by X, and every other player's coins are unchanged.
  R10. When a player wins a round, then they choose one object still in the pool; it is removed from the pool, added to their holdings, and their object_points rise by their own value for it.
  R11. When a player has already won rounds, then they may still win again; there is no limit.
  R12. When a round resolves, then everyone is told all bids, the winner, the price and the object taken, but no private values.
  R13. When round 6 ends, then the game ends with the pool empty and all values revealed.
  R14. When the game ends, then each player's final score is coins + object_points, and the highest score wins; tied top scores share the result (a draw).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat | options: any short free-text message
  - Sealed bid | asked: every seat | options: whole numbers from 0 to that seat's current coins (only 0 if the seat has 0 coins)
  - Pick an object | asked: only the round winner | options: exactly the object names still in the pool; the other seats are not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 6
  - each player's standing: you.coins + you.object_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their remaining coins plus the sum of their own private values for the objects they hold. The highest wins. Players level at the top share the result, which the source calls a draw.
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

- each player: `coins` (number, visible: public, starts 20): Coins the player currently holds. Everyone can track this because winning prices are announced.
- each player: `holdings` (list, visible: public, starts []): Names of the objects this player has taken.
- each player: `object_count` (number, visible: public, starts 0): How many objects the player holds. Used to break ties.
- each player: `last_bid` (number, visible: public, starts 0): The player's bid in the last resolved round, revealed at the announcement.
- each player: `final_score` (number, visible: public, starts 0): coins + object_points, set and revealed after round 6.
- the table: `pool` (list, visible: public, starts ['A', 'B', 'C', 'D', 'E', 'F']): Objects not yet taken.
- the table: `round` (number, visible: public, starts 0): The current round number, from 1 to 6.
- the table: `winner_seat` (number, visible: public, starts 0): The seat that won this round.
- the table: `price` (number, visible: public, starts 0): The amount the round winner paid.
- the table: `last_object` (text, visible: public, starts ''): The object taken this round.
- parameters (each must be an attribute holding this value, never a number buried in a step): object_count_total = 6, starting_coins = 20, value_1 = 2, value_2 = 4, value_3 = 6, value_4 = 8, value_5 = 10, value_6 = 14, values_total_per_player = 44, rounds = 6, min_bid = 0, objects_won_per_round = 1
- the game ends with ONE ending whose `rank_by` is `you.coins + you.object_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Add a TALK step at the start of each round: a simultaneous free-text message from every player, shown to all only after everyone has written. 2) Make BID a simultaneous poll in which each seat is offered every whole number from `min_bid` (0) up to that seat's current `coins`, built from the parameter attributes rather than literal numbers. A seat with 20 coins must be offered 0 through 20; a seat with 5 must be offered 0 through 5. 3) After the poll, copy each seat's bid into `last_bid`. Then find the highest bid. Among the seats tied at that bid, pick the one with the lowest `object_count`, and only if still tied choose at random. Set `winner_seat` and `price` to the winning bid, and subtract `price` from the winner's `coins`. 4) The winner then picks from `pool`: remove the object, append it to `holdings`, increment `object_count`, add their private value for that object to `object_points`, and set `last_object`. 5) After round 6, set `final_score` to coins + object_points for every player, and keep the single ending with rank_by `you.coins + you.object_points`.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "bidders_choice_shared_worth",
    "name": "Bidder's Choice: Shared Worth",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 4
    },
    "blurb": "Six rounds of talk and sealed bids for six objects you each value privately; coins plus your own object values decide the winner."
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
        "key": "coins",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "holdings",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "object_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "object_points",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "pool",
        "visible": "public",
        "type": "list",
        "initial": [
          "A",
          "B",
          "C",
          "D",
          "E",
          "F"
        ]
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winner_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "price",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_object",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "object_count_total",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "value_1",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "value_2",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "value_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "value_4",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "value_5",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "value_6",
        "visible": "public",
        "type": "number",
        "initial": 14
      },
      {
        "key": "values_total_per_player",
        "visible": "public",
        "type": "number",
        "initial": 44
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "objects_won_per_round",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "object_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "A",
          "B",
          "C",
          "D",
          "E",
          "F"
        ]
      },
      {
        "key": "object_index",
        "visible": "none",
        "type": "list",
        "initial": [
          0,
          1,
          2,
          3,
          4,
          5
        ]
      },
      {
        "key": "contenders",
        "visible": "none",
        "type": "list",
        "initial": []
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pool",
            "value": {
              "calc": "object_names"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "starting_coins"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "[x[1] for x in sorted([[uniform(0, 1), v] for v in [value_1, value_2, value_3, value_4, value_5, value_6]])]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "holdings",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "object_count",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "object_points",
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
      "text": "You start with (your values list gives your value for objects A to F in order):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "talk",
      "label": "a new round",
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
            "key": "bid",
            "value": {
              "calc": "min_bid"
            }
          }
        }
      ],
      "text": "Round {round} of {rounds}. Objects still in the pool: {pool}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short public message to the table. Nobody sees it until everyone has written. It is not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": {
        "where": "you.coins > min_bid"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid"
        },
        "max": {
          "calc": "you.coins"
        }
      },
      "store": "bid",
      "text": "Round {round}: submit a sealed bid, a whole number from {min_bid} up to the coins you hold. Nobody sees any bid until all are in. Only the winner pays."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolve the bids",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "last_bid",
            "value": {
              "calc": "you.bid"
            }
          }
        },
        {
          "set": {
            "key": "high_bid",
            "value": {
              "calc": "max([p.bid for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "contenders",
            "value": {
              "calc": "[p.seat for p in players if p.bid == high_bid and p.object_count == min([q.object_count for q in players if q.bid == high_bid])]"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "contenders[min(len(contenders) - 1, int(uniform(0, len(contenders))))]"
            }
          }
        },
        {
          "set": {
            "key": "price",
            "value": {
              "calc": "high_bid"
            }
          }
        }
      ],
      "text": "The bids are in. Seat {winner_seat} wins round {round} with a bid of {high_bid}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the winner pays",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "coins",
            "value": {
              "calc": "-price"
            },
            "if": {
              "calc": "you.coins >= price"
            },
            "text": "Seat {player} pays {price} coins, which leave the game."
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "pick",
      "label": "pick an object",
      "when": {
        "calc": "len(pool) > 1"
      },
      "to": {
        "where": "you.seat == winner_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "game": "pool"
        }
      },
      "verify": {
        "bind": "obj"
      },
      "text": "You won round {round}. Choose one object still in the pool: {pool}. You gain your own private value for it."
    },
    {
      "use": "update",
      "phase": "pick",
      "label": "take the object",
      "do": [
        {
          "set": {
            "key": "last_object",
            "value": {
              "calc": "pool[0] if len(pool) == 1 else $obj"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "last_object"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "holdings",
            "value": {
              "calc": "last_object"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "object_count",
            "value": {
              "calc": "objects_won_per_round"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == winner_seat"
            },
            "key": "object_points",
            "value": {
              "calc": "sum([you.values[i] for i in object_index if object_names[i] == last_object])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the announcement",
      "to": "all",
      "text": "Round {round} result. Bids [seat, bid]: {[[p.seat, p.last_bid] for p in players]}. Seat {winner_seat} won, paid {price} and took object {last_object}. Pool left: {pool}."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "final scores and reveal",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "you.coins + you.object_points"
            }
          }
        },
        {
          "disclose": {
            "of": 1,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values for A-F: {value}."
          }
        },
        {
          "disclose": {
            "of": 1,
            "attribute": "object_points",
            "to": "all",
            "text": "Seat {subject}'s object points: {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values for A-F: {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "object_points",
            "to": "all",
            "text": "Seat {subject}'s object points: {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values for A-F: {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "object_points",
            "to": "all",
            "text": "Seat {subject}'s object points: {value}."
          }
        },
        {
          "disclose": {
            "of": 4,
            "attribute": "values",
            "to": "all",
            "if": {
              "calc": "len(players) >= 4"
            },
            "text": "Seat {subject}'s values for A-F: {value}."
          }
        },
        {
          "disclose": {
            "of": 4,
            "attribute": "object_points",
            "to": "all",
            "if": {
              "calc": "len(players) >= 4"
            },
            "text": "Seat {subject}'s object points: {value}."
          }
        },
        {
          "disclose": {
            "of": 5,
            "attribute": "values",
            "to": "all",
            "if": {
              "calc": "len(players) >= 5"
            },
            "text": "Seat {subject}'s values for A-F: {value}."
          }
        },
        {
          "disclose": {
            "of": 5,
            "attribute": "object_points",
            "to": "all",
            "if": {
              "calc": "len(players) >= 5"
            },
            "text": "Seat {subject}'s object points: {value}."
          }
        }
      ],
      "text": "All six objects are taken. Final scores [seat, score]: {[[p.seat, p.final_score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round six",
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
      "rank_by": "you.coins + you.object_points",
      "reveal": [
        "values",
        "object_points"
      ],
      "text": "Winner: {result}. Final scores [seat, coins + object points]: {[[p.seat, p.coins + p.object_points] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 200,
    "deadline_s": 120
  },
  "rules": "There are {object_count_total} objects, named A, B, C, D, E and F, all starting in the pool: {pool}. Each player starts with {starting_coins} coins. Each player is privately dealt a random assignment of the values {value_1}, {value_2}, {value_3}, {value_4}, {value_5} and {value_6} to the six objects, one value per object, independently of the other players. Your values list gives your value for A, B, C, D, E and F in that order. Each player sees only their own assignment; every player's values total {values_total_per_player}.\n\nThe game lasts exactly {rounds} rounds. Each round:\n1. TALK. Every player writes one short public message at the same time, without seeing the others' messages. All messages are then shown to everyone. Messages are not binding and may be false.\n2. BID. Every player at the same moment submits a sealed bid: a whole number from {min_bid} up to the coins that player currently holds. A player with no coins bids {min_bid} automatically.\n3. RESOLVE. The highest bid wins the round. If several players tie for highest, the tied player holding the fewest objects wins. If they are still tied, one of them is chosen at random with equal chance. Players who do not win the round lose nothing.\n4. PAY. The round winner pays their bid: it is subtracted from their coins and leaves the game. All other players pay nothing, whatever they bid.\n5. PICK. The round winner chooses one object still in the pool. That object is removed from the pool and added to the winner's holdings, and they gain their own private value for it. When only one object is left, the winner takes it. A player may win any number of rounds.\n6. ANNOUNCE. Everyone is told all bids, who won, the price paid and which object was taken. Private values are never revealed during play.\n\nAfter round {rounds} all six objects have been taken. Each player's final score is their remaining coins plus the sum of their own private values for the objects they hold. All values are then revealed. The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw: they share the result."
}
```
````
