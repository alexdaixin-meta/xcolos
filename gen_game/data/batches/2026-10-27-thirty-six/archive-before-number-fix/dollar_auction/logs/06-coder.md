# 06 coder

- time: 2026-10-27T16:42:35+00:00 (90.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 61b91937bb3ff942, reply sha256 b3d338fb98b1235a

## Sent

````
# Task: write the XColos game file for "War of Attrition Auctions"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: Each player starts with 100 coins. Each player is secretly dealt a random ordering of the six prize values 10, 15, 20, 25, 30 and 40, one value for each of auctions 1 to 6. A player sees only their own list, so every player's six values total 140. Coin totals are public; prize values are private.

The game has 6 auctions (rounds). Each auction proceeds as follows.

1. Announce the auction number.

2. TALK: Every player writes one short message at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding: players may claim values, propose who takes which auction, or bluff.

3. RAISE STAGE 1: At the same time, each player secretly chooses a raise, a whole number from 0 up to their available coins. Available coins are coins held minus everything they have already committed in this auction. Each player's committed bid for this auction becomes the sum of their raises so far. All committed bids are then announced.

4. RAISE STAGE 2: Same as stage 1. Committed bids are announced again.

5. RAISE STAGE 3: Same as stage 1. Final committed bids are announced.

6. RESOLUTION: Every player pays their full committed bid, which is subtracted from their coins, whether or not they win. If exactly one player has the highest committed bid and it is at least 1, that player wins the prize and adds their OWN private value for this auction to their prize points. The value is not revealed to others. If two or more players tie for the highest bid, or all bids are 0, nobody wins the prize.

7. Announce who (if anyone) won and everyone's remaining coins. Committed bids reset to 0 for the next auction.

END: After auction 6, each player's final score is coins remaining plus prize points. All private value lists are then revealed.

How the winner is decided: The player with the highest final score (coins remaining plus prize points) wins. If two or more players tie for the highest final score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: War of Attrition Auctions (3 to 4 players, best with 3)

Over 6 sealed-raise auctions, players pay their full committed bids whether or not they win, and chase prizes whose values each player knows only for themselves.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 100); everyone sees it. Coins held. Committed bids are paid from this at resolution.
  - each player: prize_points (number, starts 0); only its owner sees it. Sum of the player's own private values for the auctions they won.
  - each player: values (list, starts []); only its owner sees it. The player's private ordering of the six prize values. Entry k is their value for auction k. It becomes public at game end.
  - each player: committed (number, starts 0); everyone sees it. Sum of this player's raises in the current auction. It is announced after each stage and reset to 0 after each auction.
  - each player: raise (number, starts 0); only its owner sees it. The secret raise chosen in the current stage.
  - each player: final_score (number, starts 0); everyone sees it. coins + prize_points, set after auction 6.
  - the table: auction (number, starts 0); everyone sees it. The current auction number, 1 to 6.
  - the table: prize_deck (list, starts [10, 15, 20, 25, 30, 40]); hidden from all players. The six prize values, copied and drawn at random to build each player's private ordering.
  - the table: top_bid (number, starts 0); everyone sees it. The highest committed bid in the current auction.
  - the table: top_count (number, starts 0); everyone sees it. How many players hold a committed bid equal to top_bid.
  - the table: auction_winner (text, starts 'none'); everyone sees it. The seat that won the current auction, or 'none'.
  - parameters, each kept as a table attribute: starting_coins = 100, auctions = 6, raise_stages = 3, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_value_total = 140, min_winning_bid = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player gets coins = 100, prize_points = 0, committed = 0 and final_score = 0.
  2. For each player, a fresh copy of prize_deck [10, 15, 20, 25, 30, 40] is made. Its six values are drawn one at a time at random and appended to that player's values list, giving a random ordering where entry k is the player's value for auction k.
  3. Each player is sent their own values list. Coins are public, and values are seen only by their owner.
  4. auction is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: auction += 1; auction_winner = 'none'; every player's committed = 0
  2. [tell] all players. What happens: Announce 'Auction {auction} of 6 begins.'
  3. [sync] all players. What happens: Each player is sent their own coins, committed and values, plus their value for this auction, values[auction].
  4. [poll] all players answers: short text message. What happens: Messages are collected simultaneously, then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. No state changes; messages are not binding.
  5. [poll] all players answers: whole number from 0 to coins - committed. What happens: Raise stage 1: each player's raise = answer; then committed += raise for every player.
  6. [tell] all players. What happens: Announce every player's committed bid after stage 1.
  7. [poll] all players answers: whole number from 0 to coins - committed. What happens: Raise stage 2: each player's raise = answer; then committed += raise for every player.
  8. [tell] all players. What happens: Announce every player's committed bid after stage 2.
  9. [poll] all players answers: whole number from 0 to coins - committed. What happens: Raise stage 3: each player's raise = answer; then committed += raise for every player.
  10. [tell] all players. What happens: Announce every player's final committed bid.
  11. [update] all players. What happens: top_bid = max over players of committed; top_count = number of players with committed == top_bid.
  12. [update] all players. What happens: For the player with committed == top_bid, if top_count == 1 and top_bid >= 1: prize_points += values[auction] and auction_winner = that seat. The value is not announced.
  13. [update] all players. What happens: Every player: coins -= committed, whether or not they won.
  14. [tell] all players. What happens: Announce 'Auction {auction} winner: {auction_winner}' and every player's remaining coins.
  15. [update] all players. What happens: Every player's committed = 0 and raise = 0.
  16. [update] all players. What happens: when auction == 6: every player's final_score = coins + prize_points; every player's values and prize_points are revealed to all.
  17. [check] all players. What happens: If auction >= 6, end the game; otherwise run the round again.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player has coins = 100 and prize_points = 0.
  R2. When the game starts, then each player's values list is a permutation of [10, 15, 20, 25, 30, 40] totalling 140, visible only to its owner.
  R3. When a round begins, then auction increases by 1 and every committed resets to 0.
  R4. When the talk step runs, then every player submits one text message simultaneously and all messages are shown to everyone, with no effect on state.
  R5. When a raise stage runs, then each player chooses a raise from 0 to coins - committed simultaneously, and committed increases by that raise.
  R6. When a player has coins 40 and committed 30, then their raise options are 0 to 10.
  R7. When each of the 3 raise stages ends, then every player's committed bid is announced to all.
  R8. When an auction resolves, then every player's coins decrease by their committed bid, whether or not they won (bids 20, 15, 0 leave coins 80, 85, 100 from 100 each).
  R9. When exactly one player holds the highest committed bid and it is at least 1, then that player's prize_points increase by their own values entry for this auction.
  R10. When two or more players tie for the highest committed bid (e.g. 20, 20, 5), then nobody's prize_points change, and all three still pay.
  R11. When all committed bids are 0, then nobody wins the prize and no coins change.
  R12. When an auction resolves, then the winner's seat (or none) and all coins are announced, but the prize value won is not.
  R13. When auction 6 has resolved, then the game ends, final_score = coins + prize_points for each player, and all values lists are revealed.
  R14. When the game ends, then the player with the highest coins + prize_points wins, and players tied at the top share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all players | options: any short text message
  - Raise stage 1, 2 or 3 | asked: all players | options: every whole number from 0 to coins - committed; a player with no available coins is offered only 0

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: auction >= 6
  - each player's standing: you.coins + you.prize_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final score is coins remaining plus prize points. The highest final score wins; players tied at the top share the result (the source calls this a draw).
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

- each player: `coins` (number, visible: public, starts 100): Coins held. Committed bids are paid from this at resolution.
- each player: `committed` (number, visible: public, starts 0): Sum of this player's raises in the current auction. It is announced after each stage and reset to 0 after each auction.
- each player: `final_score` (number, visible: public, starts 0): coins + prize_points, set after auction 6.
- the table: `auction` (number, visible: public, starts 0): The current auction number, 1 to 6.
- the table: `auction_winner` (text, visible: public, starts 'none'): The seat that won the current auction, or 'none'.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 100, auctions = 6, raise_stages = 3, prize_value_1 = 10, prize_value_2 = 15, prize_value_3 = 20, prize_value_4 = 25, prize_value_5 = 30, prize_value_6 = 40, prize_value_total = 140, min_winning_bid = 1
- the game ends with ONE ending whose `rank_by` is `you.coins + you.prize_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "war_of_attrition_auctions",
    "name": "War of Attrition Auctions",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Six sealed-raise auctions where every bid is paid, win or lose, for prizes only you know the worth of."
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
        "key": "values",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "committed",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "raise",
        "visible": "ally",
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
        "key": "value_now",
        "visible": "ally",
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
        "key": "prize_deck",
        "visible": "none",
        "type": "list",
        "initial": [10, 15, 20, 25, 30, 40]
      },
      {
        "key": "deal_pile",
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
        "key": "prize_value_total",
        "visible": "public",
        "type": "number",
        "initial": 140
      },
      {
        "key": "min_winning_bid",
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
            "key": "final_score",
            "value": 0
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
      "label": "deal seat 1",
      "do": [
        {"set": {"key": "deal_pile", "value": {"calc": "prize_deck"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[0]"}}},
        {"append": {"player": 1, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 2",
      "do": [
        {"set": {"key": "deal_pile", "value": {"calc": "prize_deck"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[0]"}}},
        {"append": {"player": 2, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 3",
      "do": [
        {"set": {"key": "deal_pile", "value": {"calc": "prize_deck"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[0]"}}},
        {"append": {"player": 3, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "update",
      "label": "deal seat 4",
      "when": {
        "calc": "len(players) >= 4"
      },
      "do": [
        {"set": {"key": "deal_pile", "value": {"calc": "prize_deck"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[min(int(uniform(0, len(deal_pile))), len(deal_pile) - 1)]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deal_pile[0]"}}},
        {"append": {"player": 4, "key": "values", "value": {"calc": "pick"}}},
        {"remove": {"key": "deal_pile", "value": {"calc": "pick"}}}
      ]
    },
    {
      "use": "sync",
      "label": "your private values",
      "mode": "self",
      "to": "all",
      "fields": [
        "coins",
        "values"
      ],
      "text": "Your coins and your private prize values (entry k is your value for auction k):"
    },
    {
      "use": "update",
      "label": "auction counter",
      "do": [
        {
          "set": {
            "key": "auction",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "open",
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
            "key": "auction_winner",
            "value": "none"
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
            "key": "raise",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_now",
            "value": {
              "calc": "you.values[auction - 1]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "open",
      "label": "auction announced",
      "to": "all",
      "text": "Auction {auction} of {auctions} begins."
    },
    {
      "use": "sync",
      "phase": "open",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "fields": [
        "coins",
        "committed",
        "values",
        "value_now"
      ],
      "text": "Your coins, committed bid, private values, and your value for this auction (value_now):"
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
      "text": "Auction {auction}: write one short message to the table. Everyone writes at once; messages are not binding."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 1",
      "to": {
        "where": "you.coins - you.committed > 0"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "raise",
      "text": "Auction {auction}, raise stage 1 of {raise_stages}: choose a secret raise, a whole number from 0 up to your available coins (coins minus what you have committed this auction). All committed bids are paid at resolution, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "commit stage 1",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "bids after stage 1",
      "to": "all",
      "text": "Committed bids after stage 1 [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 2",
      "to": {
        "where": "you.coins - you.committed > 0"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "raise",
      "text": "Auction {auction}, raise stage 2 of {raise_stages}: choose a secret raise, a whole number from 0 up to your available coins (coins minus what you have committed this auction). All committed bids are paid at resolution, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "commit stage 2",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "bids after stage 2",
      "to": "all",
      "text": "Committed bids after stage 2 [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "poll",
      "phase": "raise",
      "label": "raise stage 3",
      "to": {
        "where": "you.coins - you.committed > 0"
      },
      "answer": {
        "type": "number",
        "min": 0,
        "max": {
          "calc": "you.coins - you.committed"
        }
      },
      "store": "raise",
      "text": "Auction {auction}, raise stage 3 of {raise_stages} (the last): choose a secret raise, a whole number from 0 up to your available coins (coins minus what you have committed this auction). All committed bids are paid at resolution, win or lose."
    },
    {
      "use": "update",
      "phase": "raise",
      "label": "commit stage 3",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "committed",
            "value": {
              "calc": "you.raise"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "raise",
      "label": "final bids",
      "to": "all",
      "text": "Final committed bids [seat, committed]: {[[p.seat, p.committed] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
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
            "value": {
              "calc": "['seat 1', 'seat 2', 'seat 3', 'seat 4'][[p.seat for p in players if p.committed == top_bid][0] - 1] if top_count == 1 and top_bid >= min_winning_bid else 'none'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.committed == top_bid and top_count == 1 and top_bid >= min_winning_bid"
            },
            "key": "prize_points",
            "value": {
              "calc": "you.values[auction - 1]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.committed > 0 and you.coins >= you.committed"
            },
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
      "phase": "resolve",
      "label": "auction result",
      "to": "all",
      "text": "Auction {auction} winner: {auction_winner}. Remaining coins [seat, coins]: {[[p.seat, p.coins] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "reset bids",
      "do": [
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
            "key": "raise",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "final scores",
      "when": {
        "calc": "auction == auctions"
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
        },
        {
          "disclose": {
            "of": 1,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values were: {value}."
          }
        },
        {
          "disclose": {
            "of": 2,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values were: {value}."
          }
        },
        {
          "disclose": {
            "of": 3,
            "attribute": "values",
            "to": "all",
            "text": "Seat {subject}'s values were: {value}."
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
            "text": "Seat {subject}'s values were: {value}."
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
      "rank_by": "you.coins + you.prize_points",
      "reveal": [
        "values",
        "prize_points"
      ],
      "text": "Winner: {result}. Final scores [seat, coins + prize points]: {[[p.seat, p.coins + p.prize_points] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 7,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "Each player starts with {starting_coins} coins. Each player is secretly dealt a random ordering of the six prize values {prize_value_1}, {prize_value_2}, {prize_value_3}, {prize_value_4}, {prize_value_5} and {prize_value_6}, one value for each of auctions 1 to {auctions}. You see only your own list, so every player's six values total {prize_value_total}. Coin totals are public; prize values are private.\n\nThe game has {auctions} auctions. Each auction:\n\n1. The auction number is announced.\n2. TALK: every player writes one short message at the same time without seeing the others; all messages are then shown to everyone. Messages are not binding: you may claim values, propose who takes which auction, or bluff.\n3-5. {raise_stages} RAISE STAGES: at the same time, each player secretly chooses a raise, a whole number from 0 up to their available coins (coins held minus everything already committed in this auction). Your committed bid is the sum of your raises so far. After each stage all committed bids are announced. A player with no available coins is not asked and raises 0.\n6. RESOLUTION: every player pays their full committed bid, subtracted from their coins, whether or not they win. If exactly one player has the highest committed bid and it is at least {min_winning_bid}, that player wins the prize and adds their OWN private value for this auction to their prize points; the value is not revealed. If two or more players tie for the highest bid, or all bids are 0, nobody wins the prize, and everyone still pays what they committed (a bid of 0 costs nothing).\n7. The winner (or none) and everyone's remaining coins are announced. Committed bids reset to 0.\n\nAfter auction {auctions}, each player's final score is coins remaining plus prize points, and all private value lists are revealed. The highest final score wins; players tied at the top share the win."
}
```
````
