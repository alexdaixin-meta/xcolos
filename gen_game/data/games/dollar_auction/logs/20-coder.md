# 20 coder

- time: 2026-10-27T18:33:47+00:00 (59.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 7118e677cd76a9a3, reply sha256 9fb8bb09eff14882

## Sent

````
# Task: write the XColos game file for "Escalation Ledger III"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
There are four schedule types:
- North: high-value rounds 1, 5 and 9.
- East: high-value rounds 2, 6 and 10.
- South: high-value rounds 3, 7 and 11.
- West: high-value rounds 4, 8 and 12.
Three different types are dealt at random, one to each player, and each player is told only their own type. The fourth type goes to nobody, and nobody is told which it is. In that type's rounds, the prize is worth 6 to everyone.
Every total starts at 0. Totals may go below 0.
In each round the prize is worth 12 to a player if it is one of that player's high-value rounds, and 6 otherwise.

EACH ROUND (rounds 1 to 12)
1. Announce the round number.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing is binding, and players may lie.
3. Bid: every player secretly and simultaneously chooses 0, 2, 4, 6 or 8.
4. Reveal all bids.
5. Resolve:
   (a) All bids 0: nobody pays and nobody wins.
   (b) One bid strictly highest: that player wins. The winner pays the full bid and receives their own value of the prize (12 or 6). Every other player pays half of their own bid.
   (c) Two or three players tie for the highest bid (above 0): go to step 6. Players not in the tie pay half of their own bid.
6. Escalation, tied players only: each tied player secretly and simultaneously chooses RAISE or DROP. Every player who chooses RAISE pays 3.
   - Exactly one raiser: that player wins. The winner pays the full bid (plus the 3) and receives their own value of the prize. The other tied players pay half their bid.
   - Two or more raisers, or no raisers: nobody receives the prize. Every tied player pays half their bid; raisers have also paid 3.
7. Update all totals, then announce every bid, every escalation choice and every total.

END
After round 12 the game ends.

How the winner is decided: After round 12, the player with the highest total wins. If two or three players share the highest total, they draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Escalation Ledger III (3 to 3 players, best with 3)

Three players with secret high-value schedules bid over 12 rounds for a prize; tied top bids go to a raise-or-drop escalation, and the highest total wins.

STATE (every item below must exist in the file):
  - each player: schedule_type (text, starts ''); only its owner sees it. This player's secret schedule type: North, East, South or West.
  - each player: schedule_slot (number, starts 0); only its owner sees it. Value of round % 4 in this player's high-value rounds: North 1, East 2, South 3, West 0.
  - each player: prize_value (number, starts 6); only its owner sees it. This player's value of this round's prize: 12 if round % 4 == schedule_slot, else 6.
  - each player: bid (number, starts 0); everyone sees it. This round's bid: 0, 2, 4, 6 or 8. It is chosen secretly and revealed after all bids are in.
  - each player: in_tie (bool, starts False); everyone sees it. True if this player tied for the highest bid above 0 this round.
  - each player: escalation (text, starts ''); everyone sees it. This round's escalation choice, RAISE or DROP, or empty if the player was not in a tie.
  - each player: total (number, starts 0); everyone sees it. Running total. It may go below 0.
  - the table: round (number, starts 0); everyone sees it. Current round, 1 to 12.
  - the table: schedule_deck (list, starts ['North', 'East', 'South', 'West']); hidden from all players. The four schedule types, dealt from at setup.
  - the table: unused_type (text, starts ''); hidden from all players. The schedule type dealt to nobody. Nobody is told which it is.
  - the table: high_bid (number, starts 0); everyone sees it. The highest bid this round.
  - the table: top_count (number, starts 0); everyone sees it. The number of players whose bid equals high_bid.
  - the table: raise_count (number, starts 0); everyone sees it. The number of tied players who chose RAISE this round.
  - parameters, each kept as a table attribute: num_rounds = 12, high_value = 12, low_value = 6, bid_option_1 = 0, bid_option_2 = 2, bid_option_3 = 4, bid_option_4 = 6, bid_option_5 = 8, raise_cost = 3, loser_pay_fraction = 0.5, schedule_types = 4, schedule_cycle = 4, starting_total = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Set every player's total to 0 and the round to 0.
  2. For each player, draw one type at random from schedule_deck into that player's schedule_type and remove it from schedule_deck.
  3. Set each player's schedule_slot from their type: North 1, East 2, South 3, West 0.
  4. Move the one type left in schedule_deck into unused_type, which stays hidden from everyone.
  5. Tell each player privately only their own schedule type and its high-value rounds (North 1, 5, 9; East 2, 6, 10; South 3, 7, 11; West 4, 8, 12).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Add 1 to round. Set each player's prize_value = 12 if round % 4 == schedule_slot, else 6. Reset bid to 0, in_tie to false, escalation to empty and raise_count to 0. Announce 'Round {round} of 12.'
  2. [poll] all players answers: short text message. What happens: Every player writes one message at the same time. All messages are then broadcast to everyone as 'Seat {seat} says: {value}'. Nothing is binding, and players may lie.
  3. [poll] all players answers: one of 0, 2, 4, 6, 8. What happens: Store each player's answer in bid. No bid is seen until all are in.
  4. [update] all players. What happens: Set high_bid = max of all bids and top_count = number of players with bid == high_bid. Announce every player's bid.
  5. [update] all players. What happens: When high_bid > 0 and top_count == 1: the player with bid == high_bid adds prize_value - bid to total, and every other player subtracts bid / 2 from total. When high_bid == 0: nothing changes.
  6. [update] all players. What happens: When high_bid > 0 and top_count >= 2: set in_tie = (bid == high_bid) for each player, and every player with in_tie false subtracts bid / 2 from total.
  7. [poll] each player with in_tie true (only when high_bid > 0 and top_count >= 2) answers: RAISE or DROP. What happens: Store each tied player's answer in escalation. Choices are simultaneous and secret until all are in.
  8. [update] tied players. What happens: When high_bid > 0 and top_count >= 2: set raise_count = number of players with escalation == RAISE. Every raiser subtracts 3 from total. If raise_count == 1, the raiser adds prize_value - bid to total and every other tied player subtracts bid / 2. Otherwise every tied player subtracts bid / 2.
  9. [tell] all players. What happens: Announce every bid, every escalation choice and every total.
  10. [check] all players. What happens: If round >= 12, end the game; otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, three of the four types North, East, South and West are dealt at random, one to each player. Each player sees only their own type, and the fourth type is dealt to nobody and revealed to nobody.
  R2. When it is round r, then a player's prize value is 12 if r is one of their high-value rounds (North 1, 5, 9; East 2, 6, 10; South 3, 7, 11; West 4, 8, 12), and 6 otherwise.
  R3. Every total starts at 0, and a total may go below 0.
  R4. Each round, every player sends one short message at the same time, and all messages are then shown to everyone.
  R5. Each round, every player secretly and simultaneously bids 0, 2, 4, 6 or 8, and all bids are then revealed.
  R6. When all bids are 0, then no total changes in that round.
  R7. When one bid is strictly highest, then that player's total changes by prize value minus bid (for example, a bid of 8 in a high-value round gives +4), and each other player loses half their own bid (a bid of 4 costs 2).
  R8. When two or three players tie for the highest bid above 0, then players not in the tie lose half their own bid, and only the tied players choose RAISE or DROP, simultaneously.
  R9. When a tied player chooses RAISE, then that player loses 3.
  R10. When exactly one tied player raises, then that player's total changes by prize value minus bid minus 3 (for example, a tie at 6 with prize value 12 gives +3), and each other tied player loses half the bid.
  R11. When zero, two or three tied players raise, then nobody receives the prize, every tied player loses half the bid, and each raiser also loses 3.
  R12. After each round, every bid, every escalation choice and every total is announced.
  R13. When round 12 has been resolved, then the game ends, and the player or players with the highest total win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all seats | options: any short text, from every seat in every round
  - Bid | asked: all seats | options: 0, 2, 4, 6, 8 for every seat in every round
  - Escalation | asked: only seats whose bid equals the highest bid, when that bid is above 0 and two or three seats share it | options: a tied seat: RAISE, DROP; any other seat is not asked

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.total (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total after round 12. The highest total wins, and players level at the top share the win (a draw).
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

- each player: `bid` (number, visible: public, starts 0): This round's bid: 0, 2, 4, 6 or 8. It is chosen secretly and revealed after all bids are in.
- each player: `escalation` (text, visible: public, starts ''): This round's escalation choice, RAISE or DROP, or empty if the player was not in a tie.
- each player: `total` (number, visible: public, starts 0): Running total. It may go below 0.
- the table: `round` (number, visible: public, starts 0): Current round, 1 to 12.
- parameters (each must be an attribute holding this value, never a number buried in a step): num_rounds = 12, high_value = 12, low_value = 6, bid_option_1 = 0, bid_option_2 = 2, bid_option_3 = 4, bid_option_4 = 6, bid_option_5 = 8, raise_cost = 3, loser_pay_fraction = 0.5, schedule_types = 4, schedule_cycle = 4, starting_total = 0
- the game ends with ONE ending whose `rank_by` is `you.total`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "escalation_ledger_iii",
    "name": "Escalation Ledger III",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players with secret high-value schedules bid over 12 rounds for a prize; tied top bids go to a raise-or-drop escalation, and the highest total wins."
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
        "key": "schedule_type",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "schedule_slot",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "prize_value",
        "visible": "ally",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "in_tie",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "escalation",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "total",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "key": "schedule_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "North",
          "East",
          "South",
          "West"
        ]
      },
      {
        "key": "unused_type",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_options",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "high_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise_count",
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
        "key": "high_value",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "low_value",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bid_option_1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_option_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bid_option_3",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "bid_option_4",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "bid_option_5",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "raise_cost",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "loser_pay_fraction",
        "visible": "public",
        "type": "number",
        "initial": 0.5
      },
      {
        "key": "schedule_types",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "schedule_cycle",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "starting_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "reset totals",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "total",
            "value": {
              "calc": "starting_total"
            }
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bid_options",
            "value": {
              "calc": "[bid_option_1, bid_option_2, bid_option_3, bid_option_4, bid_option_5]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the schedules",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "schedule_deck[int(uniform(0, len(schedule_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "schedule_type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "schedule_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "schedule_deck[int(uniform(0, len(schedule_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "schedule_type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "schedule_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "schedule_deck[int(uniform(0, len(schedule_deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "schedule_type",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "schedule_deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "schedule slots",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "schedule_slot",
            "value": {
              "calc": "1 if you.schedule_type == 'North' else (2 if you.schedule_type == 'East' else (3 if you.schedule_type == 'South' else 0))"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the unused type",
      "do": [
        {
          "set": {
            "key": "unused_type",
            "value": {
              "calc": "schedule_deck[0]"
            }
          }
        },
        {
          "remove": {
            "key": "schedule_deck",
            "value": {
              "calc": "unused_type"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "your schedule",
      "to": "all",
      "text": "Your secret schedule type is {schedule_type}. High-value rounds by type: North 1, 5, 9; East 2, 6, 10; South 3, 7, 11; West 4, 8, 12. In your high-value rounds the prize is worth {high_value} to you; otherwise {low_value}."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "new round",
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
            "key": "prize_value",
            "value": {
              "calc": "high_value if round % schedule_cycle == you.schedule_slot else low_value"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "in_tie",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "escalation",
            "value": ""
          }
        },
        {
          "set": {
            "key": "raise_count",
            "value": 0
          }
        }
      ],
      "text": "Round {round} of {num_rounds}."
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
      "text": "Write one short message to the table. Everyone writes at the same time; nothing is binding and you may lie."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "bid",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "bid_options"
        }
      },
      "store": "bid",
      "text": "Round {round}: choose your secret bid: 0, 2, 4, 6 or 8. No bid is seen until all are in."
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "reveal bids",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid",
            "value": {
              "calc": "int(you.bid)"
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
            "key": "top_count",
            "value": {
              "calc": "count(p.bid == high_bid for p in players)"
            }
          }
        }
      ],
      "text": "Bids: Seat 1 {players[0].bid}, Seat 2 {players[1].bid}, Seat 3 {players[2].bid}. Highest bid {high_bid}, held by {top_count} player(s)."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "single winner",
      "when": {
        "calc": "high_bid > 0 and top_count == 1"
      },
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.bid == high_bid"
            },
            "key": "total",
            "value": {
              "calc": "you.prize_value - you.bid"
            },
            "text": "Seat {player} wins the prize with the highest bid."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.bid < high_bid"
            },
            "key": "total",
            "value": {
              "calc": "-(you.bid * loser_pay_fraction)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the tie",
      "when": {
        "calc": "high_bid > 0 and top_count >= 2"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "in_tie",
            "value": {
              "calc": "you.bid == high_bid"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.in_tie"
            },
            "key": "total",
            "value": {
              "calc": "-(you.bid * loser_pay_fraction)"
            }
          }
        }
      ],
      "text": "{top_count} players tie at {high_bid}. The tied players go to escalation."
    },
    {
      "use": "poll",
      "phase": "escalation",
      "label": "escalation",
      "when": {
        "calc": "high_bid > 0 and top_count >= 2"
      },
      "to": {
        "where": "you.in_tie"
      },
      "answer": {
        "type": "choice",
        "options": [
          "RAISE",
          "DROP"
        ]
      },
      "store": "escalation",
      "text": "You tied for the highest bid ({high_bid}). Choose RAISE or DROP, secretly. RAISE costs {raise_cost} whatever happens. If you are the only raiser you win the prize (paying your full bid plus {raise_cost}); if no one or more than one tied player raises, nobody gets the prize and every tied player pays half the bid."
    },
    {
      "use": "update",
      "phase": "escalation",
      "label": "resolve escalation",
      "when": {
        "calc": "high_bid > 0 and top_count >= 2"
      },
      "do": [
        {
          "set": {
            "key": "raise_count",
            "value": {
              "calc": "count(p.in_tie and p.escalation == 'RAISE' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_tie and you.escalation == 'RAISE'"
            },
            "key": "total",
            "value": {
              "calc": "-raise_cost"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_tie and you.escalation == 'RAISE'"
            },
            "key": "total",
            "value": {
              "calc": "you.prize_value - you.bid"
            },
            "if": {
              "calc": "raise_count == 1"
            },
            "text": "Seat {player} is the only raiser and wins the prize."
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_tie and you.escalation != 'RAISE'"
            },
            "key": "total",
            "value": {
              "calc": "-(you.bid * loser_pay_fraction)"
            },
            "if": {
              "calc": "raise_count == 1"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.in_tie"
            },
            "key": "total",
            "value": {
              "calc": "-(you.bid * loser_pay_fraction)"
            },
            "if": {
              "calc": "raise_count != 1"
            }
          }
        }
      ],
      "text": "Raisers: {raise_count}."
    },
    {
      "use": "tell",
      "phase": "report",
      "label": "round report",
      "to": "all",
      "text": "Round {round} results. Bids: Seat 1 {players[0].bid}, Seat 2 {players[1].bid}, Seat 3 {players[2].bid}. Escalation: Seat 1 '{players[0].escalation}', Seat 2 '{players[1].escalation}', Seat 3 '{players[2].escalation}'. Totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    },
    {
      "use": "check",
      "phase": "report",
      "label": "after the last round",
      "when": {
        "calc": "round >= num_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= num_rounds"
      },
      "rank_by": "you.total",
      "reveal": [
        "schedule_type"
      ],
      "text": "Winner: {result}. Final totals: Seat 1 {players[0].total}, Seat 2 {players[1].total}, Seat 3 {players[2].total}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "SETUP. There are four schedule types: North (high-value rounds 1, 5 and 9), East (2, 6 and 10), South (3, 7 and 11) and West (4, 8 and 12). Three different types are dealt at random, one to each player, and each player is told only their own type. The fourth type goes to nobody, and nobody is told which it is; in that type's rounds the prize is worth {low_value} to everyone. Every total starts at {starting_total}. Totals may go below 0. In each round the prize is worth {high_value} to a player if it is one of that player's high-value rounds, and {low_value} otherwise.\n\nEACH ROUND (rounds 1 to {num_rounds}):\n1. The round number is announced.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing is binding, and players may lie.\n3. Bid: every player secretly and simultaneously chooses {bid_option_1}, {bid_option_2}, {bid_option_3}, {bid_option_4} or {bid_option_5}.\n4. All bids are revealed.\n5. Resolve: (a) All bids 0: nobody pays and nobody wins. (b) One bid strictly highest: that player wins. The winner pays the full bid and receives their own value of the prize ({high_value} or {low_value}). Every other player pays half of their own bid. (c) Two or three players tie for the highest bid (above 0): go to escalation. Players not in the tie pay half of their own bid.\n6. Escalation, tied players only: each tied player secretly and simultaneously chooses RAISE or DROP. Every player who chooses RAISE pays {raise_cost}. Exactly one raiser: that player wins; the winner pays the full bid (plus the {raise_cost}) and receives their own value of the prize, and the other tied players pay half their bid. Two or more raisers, or no raisers: nobody receives the prize; every tied player pays half their bid, and raisers have also paid {raise_cost}. Players not in the tie are not asked.\n7. All totals are updated, then every bid, every escalation choice and every total is announced.\n\nEND. After round {num_rounds} the game ends. The player with the highest total wins. If two or three players share the highest total, they draw (share the win)."
}
```
````
