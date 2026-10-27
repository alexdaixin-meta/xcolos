# 46 coder

- time: 2026-10-27T17:16:13+00:00 (90.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 84547cd1e998d30e, reply sha256 6607c769947a84bb

## Sent

````
# Task: write the XColos game file for "Sealed Escalation: Three-Way Dollar Auction"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

R1 Setup. Every player has coins = 100, prize_points = 0, committed = 0, max_raise = 0, raise_amt = 0, current_value = 0 and final_score = 0. The table has auction = 0, top_bid = 0, top_count = 0 and auction_winner = 'none'. The table prize_deck is [10, 15, 20, 25, 30, 40].

R2 Deal. At setup each player's values is set to an independent random shuffle of prize_deck, a list of 6 entries summing to 140. A player's values list is visible only to that player. Two players may hold the same value for the same auction.

R3 Round start. There are 6 rounds, and one round is one auction. At the start of a round:
- auction increases by 1.
- Every player's committed becomes 0.
- Each player's current_value becomes the entry of their values at position auction, counting from 1.
- Each player is told privately their current_value.
- Everyone is told the auction number and every player's coins and prize_points.

R4 Talk. Everyone writes one short message at the same time. All messages are then shown to everyone. Messages bind no one.

R5 Bound. Immediately before each raise stage, each player's max_raise is set to that same player's coins minus that same player's committed.

R6 Raise stages. Each auction has exactly 3 raise stages. In each stage all players choose at the same moment.
- Each player's options are exactly the whole numbers from 0 to their own max_raise. For example, 0..100 with coins 100 and committed 0; 0..55 with coins 85 and committed 30; 0..10 with coins 40 and committed 30.
- The choice is stored in raise_amt.
- Immediately after the stage, each player's committed increases by their raise_amt.
- Everyone is then told every player's committed.

R7 Limit. A player's committed can never exceed their coins within one auction. This is guaranteed by R5 and R6.

R8 Resolution. After the third stage:
- top_bid = the largest committed among players.
- top_count = the number of players whose committed equals top_bid.
- Every player's coins decreases by their committed.
- If top_count = 1 and top_bid ≥ 1, the player with committed = top_bid adds their own current_value to prize_points, and auction_winner = that player. Otherwise auction_winner = 'none' and no one gains prize_points.
- Everyone is told the auction_winner and top_bid.

R9 End. After auction 6, each player's final_score = coins + prize_points. The game ends.

How the winner is decided: The player with the highest final_score (coins left plus prize points) wins. If two or more players tie for the highest final_score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Sealed Escalation: Three-Way Dollar Auction (3 to 3 players, best with 3)

Three players hold 6 sealed all-pay auctions. Each auction has 3 simultaneous raise stages, everyone pays what they committed, and a unique top bidder gains their private value for the prize; the final score is coins left plus prize points.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 100); everyone sees it. Coins the player still holds. Every committed coin is paid, win or lose.
  - each player: prize_points (number, starts 0); everyone sees it. Sum of the current_value of every auction this player won outright.
  - each player: committed (number, starts 0); everyone sees it. Total raised by this player in the current auction. It is reset to 0 at the start of each auction and announced after each stage.
  - each player: max_raise (number, starts 0); only its owner sees it. Upper bound of this player's raise in the coming stage: coins minus committed.
  - each player: raise_amt (number, starts 0); only its owner sees it. The raise chosen in the latest stage.
  - each player: current_value (number, starts 0); only its owner sees it. This player's private value for the current auction's prize: values at position auction.
  - each player: values (list, starts 'independent random shuffle of prize_deck'); only its owner sees it. This player's private prize values for auctions 1 to 6, in order.
  - each player: final_score (number, starts 0); everyone sees it. coins + prize_points, set after auction 6.
  - the table: auction (number, starts 0); everyone sees it. Number of the current auction, from 1 to 6.
  - the table: top_bid (number, starts 0); everyone sees it. Largest committed among players at the resolution of the auction.
  - the table: top_count (number, starts 0); everyone sees it. Number of players whose committed equals top_bid.
  - the table: auction_winner (text, starts 'none'); everyone sees it. Seat that won the last auction, or 'none'.
  - the table: prize_deck (list, starts [10, 15, 20, 25, 30, 40]); hidden from all players. The six prize values that each player's values list is shuffled from.
  - parameters, each kept as a table attribute: starting_coins = 100, auctions = 6, raise_stages_per_auction = 3, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_values_total = 140, min_raise = 0, min_winning_bid = 1, unique_top_required_count = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player gets coins = 100, prize_points = 0, committed = 0, max_raise = 0, raise_amt = 0, current_value = 0 and final_score = 0.
  2. The table gets auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none' and prize_deck = [10, 15, 20, 25, 30, 40].
  3. Each player's values is set to an independent random shuffle of prize_deck (6 entries summing to 140), visible only to that player. Two players may hold the same value for the same auction.
  4. Each player is privately sent their values list.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: auction += 1. For every player: committed = 0; current_value = values[auction], counting from 1.
  2. [sync] all players. What happens: Each player is told privately their current_value.
  3. [tell] all players. What happens: Announce the auction number and every player's coins and prize_points.
  4. [poll] all players answers: short text message. What happens: Messages are collected at once, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes, and messages bind no one.
  5. [update] all players. What happens: Stage 1 bound: each player's max_raise = coins - committed.
  6. [poll] all players answers: whole number from 0 to own max_raise. What happens: Stage 1: the choice is stored in raise_amt, and no one sees a choice until all are in.
  7. [update] all players. What happens: Each player's committed += raise_amt.
  8. [tell] all players. What happens: Announce every player's committed after stage 1.
  9. [update] all players. What happens: Stage 2 bound: each player's max_raise = coins - committed.
  10. [poll] all players answers: whole number from 0 to own max_raise. What happens: Stage 2: the choice is stored in raise_amt.
  11. [update] all players. What happens: Each player's committed += raise_amt.
  12. [tell] all players. What happens: Announce every player's committed after stage 2.
  13. [update] all players. What happens: Stage 3 bound: each player's max_raise = coins - committed.
  14. [poll] all players answers: whole number from 0 to own max_raise. What happens: Stage 3: the choice is stored in raise_amt.
  15. [update] all players. What happens: Each player's committed += raise_amt.
  16. [tell] all players. What happens: Announce every player's committed after stage 3.
  17. [update] all players. What happens: top_bid = max over players of committed. top_count = count of players with committed = top_bid. Every player: coins -= committed. If top_count = 1 and top_bid >= 1: the player with committed = top_bid gets prize_points += current_value, and auction_winner = that seat. Otherwise auction_winner = 'none'.
  18. [tell] all players. What happens: Announce auction_winner and top_bid.
  19. [update] all players. What happens: When auction = 6: each player's final_score = coins + prize_points.
  20. [check] all players. What happens: End the game if auction >= 6; otherwise start the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup every player has coins = 100, prize_points = 0, committed = 0, max_raise = 0, raise_amt = 0, current_value = 0 and final_score = 0, and the table has auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none' and prize_deck = [10, 15, 20, 25, 30, 40].
  R2. At setup each player's values is an independent shuffle of [10, 15, 20, 25, 30, 40], summing to 140, visible only to that player; two players may hold the same value in the same position.
  R3. At the start of each round, auction increases by 1, every committed becomes 0, and each player's current_value becomes values[auction] (1-based), told to that player privately.
  R4. At the start of each round, everyone is told the auction number and every player's coins and prize_points.
  R5. Each round, all players write one short message at the same time, and all messages are then shown to everyone; no message changes any attribute.
  R6. Immediately before each of the 3 raise stages, each player's max_raise = coins - committed (for example coins 85 and committed 30 give max_raise 55).
  R7. In each raise stage, all players choose at once a whole number from 0 to their own max_raise, stored in raise_amt; then committed += raise_amt and every committed is announced.
  R8. A player's committed never exceeds their coins within an auction (with coins 40 and committed 30, the stage options are 0 to 10).
  R9. After the third stage, top_bid = the largest committed and top_count = the number of players with committed = top_bid.
  R10. After the third stage, every player's coins decreases by their committed, whether they won or not.
  R11. When top_count = 1 and top_bid >= 1, the player with committed = top_bid adds their current_value to prize_points and becomes auction_winner (for example committed 30, 20, 10 with current_value 25 gives that player prize_points +25 and coins -30).
  R12. When top_count >= 2 or top_bid = 0, auction_winner = 'none' and no one gains prize_points, but every player still pays their committed (for example committed 20, 20, 5: no winner, and the coins fall by 20, 20 and 5).
  R13. After each auction, everyone is told auction_winner and top_bid.
  R14. After auction 6, each player's final_score = coins + prize_points and the game ends.
  R15. The player with the highest final_score wins; players tied at the highest final_score share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each round | asked: all seats at once | options: any short text message
  - Raise stage 1, 2 or 3 | asked: all seats at once | options: every whole number from 0 to that seat's max_raise = coins - committed (a seat with 0 coins left is offered only 0)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: auction >= 6
  - each player's standing: you.final_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is final_score = coins left + prize points. The highest final_score wins, and players tied at the top share the win (the source calls this a draw).
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

- each player: `coins` (number, visible: public, starts 100): Coins the player still holds. Every committed coin is paid, win or lose.
- each player: `prize_points` (number, visible: public, starts 0): Sum of the current_value of every auction this player won outright.
- each player: `committed` (number, visible: public, starts 0): Total raised by this player in the current auction. It is reset to 0 at the start of each auction and announced after each stage.
- each player: `final_score` (number, visible: public, starts 0): coins + prize_points, set after auction 6.
- the table: `auction` (number, visible: public, starts 0): Number of the current auction, from 1 to 6.
- the table: `top_bid` (number, visible: public, starts 0): Largest committed among players at the resolution of the auction.
- the table: `auction_winner` (text, visible: public, starts 'none'): Seat that won the last auction, or 'none'.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 100, auctions = 6, raise_stages_per_auction = 3, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_values_total = 140, min_raise = 0, min_winning_bid = 1, unique_top_required_count = 1
- the game ends with ONE ending whose `rank_by` is `you.final_score`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1. Rebuild each of the 3 raise stages as a simultaneous poll whose options are every whole number from min_raise (0) up to that player's own max_raise. 2. Set max_raise = coins - committed immediately before each stage, not once per auction. 3. Store the chosen number in raise_amt, then add raise_amt to committed for every player right after the stage, then announce committed. 4. Make sure the poll does not fall back to 0 or offer only 0; check that a scripted pick such as 12 or 55 appears in the move log. 5. At resolution: compute top_bid and top_count from committed, subtract committed from coins, and give current_value to the single top bidder when top_bid >= min_winning_bid. 6. Read every bound from the parameter attributes, never from numbers written into a step.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "sealed_escalation_three_way_dollar_auction",
    "name": "Sealed Escalation: Three-Way Dollar Auction",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Six sealed all-pay auctions, three simultaneous raise stages each; everyone pays what they committed, and only a unique top bidder scores their private prize value."
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
        "initial": 100
      },
      {
        "key": "prize_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "committed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_raise",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise_amt",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
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
        "key": "auction",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_bid",
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
        "key": "auction_winner",
        "visible": "public",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "prize_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          10,
          15,
          20,
          25,
          30,
          40
        ]
      },
      {
        "key": "deal_pool",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "auctions",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "raise_stages_per_auction",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "prize_value_1",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "prize_value_2",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "prize_value_3",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "prize_value_4",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "prize_value_5",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "prize_value_6",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "prize_values_total",
        "visible": "public",
        "type": "number",
        "initial": 140
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "unique_top_required_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting values",
      "do": [
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
            "key": "prize_points",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "max_raise",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise_amt",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "current_value",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "auction",
            "value": 0
          }
        },
        {
          "set": {
            "key": "top_bid",
            "value": 0
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "auction_winner",
            "value": "none"
          }
        },
        {
          "set": {
            "key": "prize_deck",
            "value": {
              "calc": "[prize_value_1, prize_value_2, prize_value_3, prize_value_4, prize_value_5, prize_value_6]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "shuffle each player's values",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "values",
            "value": []
          }
        },
        {
          "set": {
            "key": "deal_pool",
            "value": {
              "calc": "[v for v in prize_deck]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 1,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pool",
            "value": {
              "calc": "[v for v in prize_deck]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 2,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "deal_pool",
            "value": {
              "calc": "[v for v in prize_deck]"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deal_pool[int(uniform(0, len(deal_pool)))]"
            }
          }
        },
        {
          "append": {
            "player": 3,
            "key": "values",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deal_pool",
            "value": {
              "calc": "pick"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your private values",
      "mode": "self",
      "to": "all",
      "fields": [
        "values"
      ],
      "text": "Your private prize values for auctions 1 to {auctions}, in order:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the next auction",
      "do": [
        {
          "adjust": {
            "key": "auction",
            "value": 1
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "current_value",
            "value": {
              "calc": "you.values[auction - 1]"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your value this auction",
      "mode": "self",
      "to": "all",
      "fields": [
        "current_value"
      ],
      "text": "Your private value for the prize in auction {auction}:"
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "the auction opens",
      "to": "all",
      "text": "Auction {auction} of {auctions} opens. Coins: Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}. Prize points: Seat 1 {players[0].prize_points}, Seat 2 {players[1].prize_points}, Seat 3 {players[2].prize_points}."
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
      "text": "Auction {auction}: say one short thing to the table. Nothing said binds anyone."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "stage 1 bound",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "raise_amt",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "max_raise",
            "value": {
              "calc": "you.coins - you.committed"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "stage 1",
      "label": "raise stage 1",
      "to": {
        "where": "you.max_raise > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.max_raise"
        }
      },
      "store": "raise_amt",
      "text": "Auction {auction}, raise stage 1 of {raise_stages_per_auction}. You have committed {committed} and may raise any whole number from {min_raise} to {max_raise}. All players choose at once; nobody sees a raise until all are in. Every committed coin is paid, win or lose."
    },
    {
      "use": "update",
      "phase": "stage 1",
      "label": "stage 1 commits",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise_amt"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "stage 1",
      "label": "committed after stage 1",
      "to": "all",
      "text": "After stage 1 of auction {auction}, committed: Seat 1 {players[0].committed}, Seat 2 {players[1].committed}, Seat 3 {players[2].committed}."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "stage 2 bound",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "raise_amt",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "max_raise",
            "value": {
              "calc": "you.coins - you.committed"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "stage 2",
      "label": "raise stage 2",
      "to": {
        "where": "you.max_raise > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.max_raise"
        }
      },
      "store": "raise_amt",
      "text": "Auction {auction}, raise stage 2 of {raise_stages_per_auction}. You have committed {committed} and may raise any whole number from {min_raise} to {max_raise}. All players choose at once; nobody sees a raise until all are in. Every committed coin is paid, win or lose."
    },
    {
      "use": "update",
      "phase": "stage 2",
      "label": "stage 2 commits",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise_amt"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "stage 2",
      "label": "committed after stage 2",
      "to": "all",
      "text": "After stage 2 of auction {auction}, committed: Seat 1 {players[0].committed}, Seat 2 {players[1].committed}, Seat 3 {players[2].committed}."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "stage 3 bound",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "raise_amt",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "max_raise",
            "value": {
              "calc": "you.coins - you.committed"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "stage 3",
      "label": "raise stage 3",
      "to": {
        "where": "you.max_raise > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.max_raise"
        }
      },
      "store": "raise_amt",
      "text": "Auction {auction}, raise stage 3 of {raise_stages_per_auction}, the last. You have committed {committed} and may raise any whole number from {min_raise} to {max_raise}. All players choose at once; nobody sees a raise until all are in. Every committed coin is paid, win or lose."
    },
    {
      "use": "update",
      "phase": "stage 3",
      "label": "stage 3 commits",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise_amt"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "stage 3",
      "label": "committed after stage 3",
      "to": "all",
      "text": "After stage 3 of auction {auction}, committed: Seat 1 {players[0].committed}, Seat 2 {players[1].committed}, Seat 3 {players[2].committed}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the auction resolves",
      "do": [
        {
          "set": {
            "key": "top_bid",
            "value": {
              "calc": "max([p.committed for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.committed == top_bid for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "auction_winner",
            "value": "none"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.committed == top_bid and top_count == unique_top_required_count and top_bid >= min_winning_bid"
            },
            "key": "auction_winner",
            "value": {
              "calc": "['1', '2', '3'][you.seat - 1]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.committed == top_bid and top_count == unique_top_required_count and top_bid >= min_winning_bid"
            },
            "key": "prize_points",
            "value": {
              "calc": "you.current_value"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "-you.committed"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolution",
      "label": "the result",
      "to": "all",
      "text": "Auction {auction} result: winner seat {auction_winner}, top bid {top_bid}. Everyone paid what they committed. Coins: Seat 1 {players[0].coins}, Seat 2 {players[1].coins}, Seat 3 {players[2].coins}. Prize points: Seat 1 {players[0].prize_points}, Seat 2 {players[1].prize_points}, Seat 3 {players[2].prize_points}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "final scores",
      "when": {
        "calc": "auction >= auctions"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "you.coins + you.prize_points"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolution",
      "label": "after the last auction",
      "when": {
        "calc": "auction >= auctions"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "auction >= auctions"
      },
      "rank_by": "you.final_score",
      "text": "Winner: {result}. Final scores (coins + prize points): Seat 1 {players[0].final_score}, Seat 2 {players[1].final_score}, Seat 3 {players[2].final_score}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "Three players hold {auctions} sealed all-pay auctions, one per round. Everyone starts with {starting_coins} coins and 0 prize points.\n\nAt setup each player's private values list is an independent random shuffle of the six prize values {prize_value_1}, {prize_value_2}, {prize_value_3}, {prize_value_4}, {prize_value_5} and {prize_value_6} (summing to {prize_values_total}). Only you see your list; two players may hold the same value for the same auction.\n\nAt the start of each auction, the auction number goes up by 1, every player's committed becomes 0, and your current_value becomes the entry of your values list at position auction (counting from 1); you are told it privately. Everyone is told the auction number and every player's coins and prize points.\n\nThen everyone writes one short message at the same time, and all messages are shown to everyone. Messages bind no one.\n\nEach auction has exactly {raise_stages_per_auction} raise stages. Immediately before each stage, your max_raise is set to your coins minus your committed. In each stage all players choose at the same moment a whole number from {min_raise} to their own max_raise (for example 0..55 with coins 85 and committed 30). The choice is your raise; immediately after the stage, your committed increases by it, and everyone is told every player's committed. A player with no coins left to raise raises 0. Your committed can never exceed your coins within one auction.\n\nAfter the third stage: the top bid is the largest committed, and the top count is the number of players whose committed equals it. Every player's coins decrease by their committed, whether they won or not. If exactly {unique_top_required_count} player holds the top bid and the top bid is at least {min_winning_bid}, that player adds their own current_value to their prize points and is the auction winner. Otherwise (a tie at the top, or a top bid of 0) the auction winner is none, no one gains prize points, and every player still pays their committed. Everyone is told the auction winner and the top bid.\n\nAfter auction {auctions}, each player's final score is coins + prize points and the game ends. The highest final score wins; players tied at the highest final score share the win."
}
```
````
