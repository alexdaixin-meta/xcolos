# 26 coder

- time: 2026-10-27T17:00:42+00:00 (57.0s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b3f591457422b2be, reply sha256 0196698b178f2062

## Sent

````
# Task: write the XColos game file for "Escalation Auction"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 3} (the suggested size is the one the game plays best at).

PARAMETERS (stored as table attributes): starting_coins = 100; auctions = 6; raise_stages = 3; min_winning_bid = 1; prize_deck = [10, 15, 20, 25, 30, 40].

R1 Setup: every player has coins = 100, prize_points = 0, committed = 0, final_score = 0. Table: auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'.

R2 Private values: at setup each player is dealt their own values list, a random order of [10, 15, 20, 25, 30, 40] (total 140), visible only to its owner. Entry k is that player's value for auction k. Players' lists are dealt independently, so two players may hold the same value for the same auction.

Each round is one auction. There are 6 rounds.

R3 Round start: auction increases by 1 and every player's committed is set to 0. Each player is privately told their value for this auction (entry number 'auction' of their values list). Everyone is told the auction number and every player's current coins.

R4 Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and change no numbers.

R5 Raise stage (runs 3 times per auction): all players choose at the same time a raise, a whole number from 0 up to (their own coins − their own committed). The range is computed for each player at that moment from their current coins and committed attributes. For example, it is 0..100 at the start of an auction with 100 coins, and 0..55 for a player with 85 coins who committed 30 earlier in the same auction. Immediately after the poll, each player's committed increases by the raise they chose.

R6 Budget limit: a player can never commit more than their coins in one auction. With coins 40 and committed 30, the options are exactly 0 to 10.

R7 Announcement: after each of the 3 raise stages, every player's committed total is announced to all.

R8 Resolution, payment: after the third stage, top_bid = the highest committed, and top_count = the number of players whose committed equals top_bid. Every player's coins decrease by their committed, whether or not they won. For example, bids of 20, 15 and 0 leave coins of 80, 85 and 100 from 100 each.

R9 Resolution, prize: if top_count = 1 and top_bid ≥ 1, that player is the auction_winner and adds their own value for this auction to prize_points. Otherwise auction_winner = 'none' and nobody gets a prize. The winner and every player's coins are announced. Each player's committed is then reset to 0.

R10 End: after the 6th auction, each player's final_score = coins + prize_points.

How the winner is decided: After 6 auctions, the player with the highest final_score (coins remaining + prize_points) wins. If several players tie for the highest final_score, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Escalation Auction (3 to 5 players, best with 3)

Six sealed all-pay auctions, each with three simultaneous raise stages. Every bidder pays what they committed, only a sole top bidder wins their private prize value, and the highest coins plus prize points wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 100); everyone sees it. Coins the player still holds. All committed coins are paid at the end of each auction.
  - each player: prize_points (number, starts 0); only its owner sees it. Sum of the player's own private values for the auctions they won.
  - each player: committed (number, starts 0); everyone sees it. Total the player has raised so far in the current auction. It is announced after each raise stage.
  - each player: final_score (number, starts 0); everyone sees it. coins + prize_points, computed after the 6th auction.
  - each player: values (list, starts 'a random order of [10, 15, 20, 25, 30, 40], dealt independently to each player'); only its owner sees it. Entry k is the player's private value for auction k.
  - each player: current_value (number, starts 0); only its owner sees it. The player's value for the current auction (entry number 'auction' of values).
  - the table: prize_deck (list, starts [10, 15, 20, 25, 30, 40]); everyone sees it. The six prize values that each player's values list is a permutation of.
  - the table: auction (number, starts 0); everyone sees it. Number of the current auction, from 1 to 6.
  - the table: top_bid (number, starts 0); everyone sees it. The highest committed total at the resolution of the auction.
  - the table: top_count (number, starts 0); everyone sees it. Number of players whose committed equals top_bid.
  - the table: auction_winner (text, starts 'none'); everyone sees it. The seat that won the current auction, or 'none'.
  - parameters, each kept as a table attribute: starting_coins = 100, auctions = 6, raise_stages = 3, min_winning_bid = 1, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_values_total = 140, initial_prize_points = 0, initial_committed = 0, initial_final_score = 0, min_raise = 0, winning_top_count = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player gets coins = 100, prize_points = 0, committed = 0, final_score = 0 and current_value = 0.
  2. The table gets auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none' and prize_deck = [10, 15, 20, 25, 30, 40].
  3. Each player is dealt their own values list, a random order of prize_deck (total 140). The lists are dealt independently and seeded, and each is visible only to its owner.
  4. Each player is sent their own state (sync).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: auction += 1. Every player's committed = 0. Every player's current_value = entry number 'auction' (1-based) of their values list.
  2. [sync] all players. What happens: Each player is privately sent their current_value for this auction.
  3. [tell] all players. What happens: Announce: 'Auction {auction} of 6.' plus every seat's coins.
  4. [poll] all players answers: short text message. What happens: No state change. Broadcast {"to": "all", "text": "Seat {seat} says: {value}"} once all are in.
  5. [poll] all players answers: whole number from 0 to (you.coins - you.committed). What happens: Raise stage 1: each player's committed += their raise.
  6. [tell] all players. What happens: Announce every seat's committed after stage 1.
  7. [poll] all players answers: whole number from 0 to (you.coins - you.committed). What happens: Raise stage 2: each player's committed += their raise.
  8. [tell] all players. What happens: Announce every seat's committed after stage 2.
  9. [poll] all players answers: whole number from 0 to (you.coins - you.committed). What happens: Raise stage 3: each player's committed += their raise.
  10. [tell] all players. What happens: Announce every seat's committed after stage 3.
  11. [update] all players. What happens: top_bid = max over players of committed. top_count = number of players with committed == top_bid. Every player's coins -= committed.
  12. [update] all players. What happens: If top_count == 1 and top_bid >= 1: auction_winner = the seat with committed == top_bid, and that player's prize_points += their current_value. Otherwise auction_winner = 'none'.
  13. [tell] all players. What happens: Announce: 'Auction {auction} winner: {auction_winner}.' plus every seat's coins.
  14. [update] all players. What happens: Every player's committed = 0. If auction == 6: every player's final_score = coins + prize_points.
  15. [check] all players. What happens: End the game if auction >= 6. Otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup every player has coins = 100, prize_points = 0, committed = 0, final_score = 0, and the table has auction = 0, top_bid = 0, top_count = 0, auction_winner = 'none'.
  R2. At setup each player is dealt a values list that is a random order of [10, 15, 20, 25, 30, 40] (sum 140), visible only to its owner. Lists are dealt independently, so two players may hold the same value for the same auction.
  R3. When a round starts, auction increases by 1, every player's committed becomes 0, and each player's current_value becomes entry number 'auction' of their values list.
  R4. At the start of each auction, each player is told only their own current_value, and everyone is told the auction number and every player's coins.
  R5. Each auction, every player sends one short message simultaneously, all messages are shown to everyone, and no number changes.
  R6. Each auction has exactly 3 simultaneous raise stages, and after each one every player's committed increases by the raise they chose.
  R7. In a raise stage a player's options are exactly the whole numbers 0 to (coins - committed): 0..100 with coins 100 and committed 0, 0..55 with coins 85 and committed 30, 0..10 with coins 40 and committed 30.
  R8. A player's committed can never exceed their coins within one auction.
  R9. After each of the 3 raise stages, every player's committed total is announced to all.
  R10. After the third stage, top_bid = the highest committed and top_count = the number of players whose committed equals top_bid.
  R11. After the third stage every player's coins decrease by their committed, win or lose: bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100.
  R12. When top_count = 1 and top_bid >= 1, the player with committed = top_bid becomes auction_winner and adds their current_value to prize_points.
  R13. When top_count >= 2 (a tie for the highest bid), auction_winner = 'none' and nobody's prize_points change, although all players still pay their committed.
  R14. When top_bid = 0 (everyone bid 0), auction_winner = 'none' and nobody's prize_points change.
  R15. After resolution the auction_winner and every player's coins are announced, and every player's committed is reset to 0.
  R16. After the 6th auction, each player's final_score = coins + prize_points, and the game ends.
  R17. The player with the highest final_score wins, and players tied for the highest final_score share the win as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message each auction | asked: every seat | options: one short free-text message
  - Raise in each of the 3 raise stages | asked: every seat | options: every whole number from 0 to (own coins - own committed). A seat with coins equal to committed is offered only 0.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: auction >= 6
  - each player's standing: you.final_score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is final_score = coins remaining + prize_points. The highest final_score wins, and players tied at the top share the win (a draw among them).
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

- each player: `coins` (number, visible: public, starts 100): Coins the player still holds. All committed coins are paid at the end of each auction.
- each player: `committed` (number, visible: public, starts 0): Total the player has raised so far in the current auction. It is announced after each raise stage.
- each player: `final_score` (number, visible: public, starts 0): coins + prize_points, computed after the 6th auction.
- the table: `auction` (number, visible: public, starts 0): Number of the current auction, from 1 to 6.
- the table: `top_bid` (number, visible: public, starts 0): The highest committed total at the resolution of the auction.
- the table: `top_count` (number, visible: public, starts 0): Number of players whose committed equals top_bid.
- the table: `auction_winner` (text, visible: public, starts 'none'): The seat that won the current auction, or 'none'.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 100, auctions = 6, raise_stages = 3, min_winning_bid = 1, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_values_total = 140, initial_prize_points = 0, initial_committed = 0, initial_final_score = 0, min_raise = 0, winning_top_count = 1
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "escalation_auction",
    "name": "Escalation Auction",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six sealed all-pay auctions with three raise stages each: everyone pays what they commit, only a sole top bidder wins their private prize value."
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
        "visible": "ally",
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
        "key": "final_score",
        "visible": "public",
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
        "key": "current_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pool",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick_v",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stage_raise",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "prize_deck",
        "visible": "public",
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
        "key": "raise_stages",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "initial_prize_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_committed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_final_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winning_top_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting purses",
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
            "value": {
              "calc": "initial_prize_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "initial_committed"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "initial_final_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "current_value",
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
      "label": "deal the private values",
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
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "prize_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your starting state",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
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
            "value": {
              "calc": "initial_committed"
            }
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
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your value",
      "mode": "self",
      "to": "all",
      "fields": [
        "current_value"
      ],
      "text": "Your private value for this auction:"
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "auction opens",
      "to": "all",
      "text": "Auction {auction} of {auctions}. Coins [seat, coins]: {[[p.seat, p.coins] for p in players]}."
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
      "text": "Say one short thing to the table before the raises. It is not binding."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 1",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 1 of {raise_stages} in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 1",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 1",
      "to": "all",
      "text": "After raise stage 1, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 2",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 2 of {raise_stages} in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 2",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 2",
      "to": "all",
      "text": "After raise stage 2, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 3",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 3 of {raise_stages} (the last) in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 3",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 3",
      "to": "all",
      "text": "After raise stage 3, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "payment",
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
          "adjust": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "-you.committed"
            },
            "if": {
              "calc": "you.coins >= you.committed"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "prize",
      "do": [
        {
          "set": {
            "key": "auction_winner",
            "value": {
              "calc": "['1', '2', '3', '4', '5'][min([p.seat for p in players if p.committed == top_bid]) - 1] if top_count == winning_top_count and top_bid >= min_winning_bid else 'none'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.committed == top_bid and top_count == winning_top_count and top_bid >= min_winning_bid"
            },
            "key": "prize_points",
            "value": {
              "calc": "you.current_value"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "auction result",
      "to": "all",
      "text": "Auction {auction} winner: {auction_winner} (top bid {top_bid}, held by {top_count} player(s)). Coins [seat, coins]: {[[p.seat, p.coins] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "reset and score",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "initial_committed"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "you.coins + you.prize_points"
            },
            "if": {
              "calc": "auction >= auctions"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
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
      "text": "Winner: {result}. Final scores (coins + prize points) [seat, score]: {[[p.seat, p.final_score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Escalation Auction: {auctions} sealed all-pay auctions. Everyone starts with {starting_coins} coins and 0 prize points.\n\nPrivate values: at the start each player is dealt their own values list, a random order of {prize_deck} (total {prize_values_total}), seen only by its owner. Entry k is your value for auction k. Lists are dealt independently, so two players may hold the same value for the same auction.\n\nEach round is one auction. At its start the auction number goes up by 1 and everyone's committed total is set to 0. You are privately told your value for this auction; everyone is told the auction number and every player's coins.\n\nTalk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and change no numbers.\n\nRaise stages ({raise_stages} per auction): all players choose at the same time a raise, a whole number from {min_raise} up to (their own coins minus their own committed). Your committed then increases by your raise. You can never commit more than your coins in one auction: with 40 coins and 30 committed, your options are exactly 0 to 10. A player with nothing left to commit is not asked and raises 0. After each stage every player's committed total is announced to all.\n\nResolution, payment: after the third stage, top_bid is the highest committed and top_count is the number of players whose committed equals top_bid. Every player's coins decrease by their committed, whether or not they won (bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100).\n\nResolution, prize: if top_count is {winning_top_count} and top_bid is at least {min_winning_bid}, that sole top bidder is the auction winner and adds their own value for this auction to their prize points. Otherwise (a tie for the highest bid, or everyone bid 0) the auction winner is 'none' and nobody gets a prize, though everyone still pays what they committed. The winner and every player's coins are announced, and each player's committed is reset to 0.\n\nEnd: after the {auctions}th auction, each player's final score = coins + prize points. The highest final score wins; players tied for the highest final score share the win as a draw."
}
```

Why it was refused: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: 'you.coins >= you.committed' reads `you` where there is no player
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "escalation_auction",
    "name": "Escalation Auction",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six sealed all-pay auctions with three raise stages each: everyone pays what they commit, only a sole top bidder wins their private prize value."
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
        "visible": "ally",
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
        "key": "final_score",
        "visible": "public",
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
        "key": "current_value",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pool",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "pick_v",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "stage_raise",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "prize_deck",
        "visible": "public",
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
        "key": "raise_stages",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_winning_bid",
        "visible": "public",
        "type": "number",
        "initial": 1
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
        "key": "initial_prize_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_committed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "initial_final_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "min_raise",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "winning_top_count",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting purses",
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
            "value": {
              "calc": "initial_prize_points"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "initial_committed"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "initial_final_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "current_value",
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
      "label": "deal the private values",
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
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "prize_deck"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "pick_v",
            "value": {
              "calc": "you.pool[min(int(uniform(0, len(you.pool))), len(you.pool) - 1)]"
            }
          }
        },
        {
          "append": {
            "players": "all",
            "key": "values",
            "value": {
              "calc": "you.pick_v"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "pool",
            "value": {
              "calc": "you.pick_v"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your starting state",
      "mode": "self",
      "to": "all",
      "text": "You start with:"
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
            "value": {
              "calc": "initial_committed"
            }
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
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "start",
      "label": "your value",
      "mode": "self",
      "to": "all",
      "fields": [
        "current_value"
      ],
      "text": "Your private value for this auction:"
    },
    {
      "use": "tell",
      "phase": "start",
      "label": "auction opens",
      "to": "all",
      "text": "Auction {auction} of {auctions}. Coins [seat, coins]: {[[p.seat, p.coins] for p in players]}."
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
      "text": "Say one short thing to the table before the raises. It is not binding."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 1",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 1 of {raise_stages} in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 1",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 1",
      "to": "all",
      "text": "After raise stage 1, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 2",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 2 of {raise_stages} in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 2",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 2",
      "to": "all",
      "text": "After raise stage 2, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 3",
      "to": {
        "where": "you.coins - you.committed > min_raise"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_raise"
        },
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "stage_raise",
      "text": "Raise stage 3 of {raise_stages} (the last) in auction {auction}. Choose a whole number to add to your committed total, from 0 up to your coins minus what you have committed. Every coin you commit is paid at the end of the auction, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "apply stage 3",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.stage_raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "stage_raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "committed after stage 3",
      "to": "all",
      "text": "After raise stage 3, committed [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "payment",
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
          "adjust": {
            "players": "all",
            "key": "coins",
            "value": {
              "calc": "-min(you.committed, you.coins)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "prize",
      "do": [
        {
          "set": {
            "key": "auction_winner",
            "value": {
              "calc": "['1', '2', '3', '4', '5'][min([p.seat for p in players if p.committed == top_bid]) - 1] if top_count == winning_top_count and top_bid >= min_winning_bid else 'none'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.committed == top_bid and top_count == winning_top_count and top_bid >= min_winning_bid"
            },
            "key": "prize_points",
            "value": {
              "calc": "you.current_value"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "auction result",
      "to": "all",
      "text": "Auction {auction} winner: {auction_winner} (top bid {top_bid}, held by {top_count} player(s)). Coins [seat, coins]: {[[p.seat, p.coins] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "reset and score",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "initial_committed"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "final_score",
            "value": {
              "calc": "you.coins + you.prize_points"
            },
            "if": {
              "calc": "auction >= auctions"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
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
      "text": "Winner: {result}. Final scores (coins + prize points) [seat, score]: {[[p.seat, p.final_score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Escalation Auction: {auctions} sealed all-pay auctions. Everyone starts with {starting_coins} coins and 0 prize points.\n\nPrivate values: at the start each player is dealt their own values list, a random order of {prize_deck} (total {prize_values_total}), seen only by its owner. Entry k is your value for auction k. Lists are dealt independently, so two players may hold the same value for the same auction.\n\nEach round is one auction. At its start the auction number goes up by 1 and everyone's committed total is set to 0. You are privately told your value for this auction; everyone is told the auction number and every player's coins.\n\nTalk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding and change no numbers.\n\nRaise stages ({raise_stages} per auction): all players choose at the same time a raise, a whole number from {min_raise} up to (their own coins minus their own committed). Your committed then increases by your raise. You can never commit more than your coins in one auction: with 40 coins and 30 committed, your options are exactly 0 to 10. A player with nothing left to commit is not asked and raises 0. After each stage every player's committed total is announced to all.\n\nResolution, payment: after the third stage, top_bid is the highest committed and top_count is the number of players whose committed equals top_bid. Every player's coins decrease by their committed, whether or not they won (bids of 20, 15 and 0 from 100 coins each leave 80, 85 and 100).\n\nResolution, prize: if top_count is {winning_top_count} and top_bid is at least {min_winning_bid}, that sole top bidder is the auction winner and adds their own value for this auction to their prize points. Otherwise (a tie for the highest bid, or everyone bid 0) the auction winner is 'none' and nobody gets a prize, though everyone still pays what they committed. The winner and every player's coins are announced, and each player's committed is reset to 0.\n\nEnd: after the {auctions}th auction, each player's final score = coins + prize points. The highest final score wins; players tied for the highest final score share the win as a draw."
}
```
````
