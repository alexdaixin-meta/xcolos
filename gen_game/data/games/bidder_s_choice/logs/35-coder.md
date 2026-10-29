# 35 coder

- time: 2026-10-27T09:12:13+00:00 (50.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 cdfc5563854d6023, reply sha256 b28dcdc1b05f6b43

## Sent

````
# Task: write the XColos game file for "Bidder's Choice: Sealed Pool"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 5; set `meta.players` to {"min": 3, "max": 5, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP.
1) There are 3 to 5 players. Every player starts with 20 coins and no objects. The pool holds six objects: A, B, C, D, E, F.
2) Each player privately receives the six values 2, 4, 6, 8, 10 and 14, one value per object, in an independent random order for each player. Every player's values therefore total 44. A player sees only his own values.

ROUNDS. The game lasts exactly 6 rounds. Each round:
3) ANNOUNCE. The round number, the objects still in the pool, every player's coins and every player's holdings are shown to all.
4) TALK. Every player writes one message of at most 40 words at the same time, without seeing the others. Any words beyond the 40th are dropped. Then all messages are shown to everyone. Messages are not binding and may be false.
5) BID. Every player at the same time submits a sealed bid: a whole number from 0 up to his current coins. A bid that is missing, not a whole number, negative, or above his current coins counts as 0.
6) WINNER. The highest bid wins. If several players share the highest bid, the one among them holding the fewest objects wins. If several of those also hold equally few objects, there is NO SALE this round: nobody pays, no object leaves the pool, and the round still counts as played.
7) PAY AND PICK. If there is a winner, he pays his bid, so his coins decrease by his bid. He then names one object still in the pool. That object leaves the pool and is added to his holdings. If he names no object still in the pool, or gives no answer, he receives instead the remaining object with the highest of his own values (ties: earliest letter). A player may win any number of rounds.
8) REVEAL. All bids, the winner (or 'no sale') and the object taken are announced to all.

END.
9) After round 6, any objects still in the pool are discarded.
10) Each player's final score = his remaining coins + the sum of HIS OWN values for the objects he holds. All values are then revealed.

How the winner is decided: The player with the highest final score (coins left plus the sum of his own values for the objects he holds) wins. If two or more players share the highest final score, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Bidder's Choice: Sealed Pool (3 to 5 players, best with 3)

Over 6 rounds, players talk and then place sealed bids from 20 coins; each round's winner pays and picks one of six objects that every player values privately, and the score is coins left plus own values of held objects.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 20); everyone sees it. Coins the player still holds.
  - each player: holdings (list, starts []); everyone sees it. Letters of the objects the player has won.
  - each player: holdings_count (number, starts 0); everyone sees it. Number of objects in holdings, used for the tie-break.
  - each player: value_a (number, starts 0); only its owner sees it. The player's private value for object A, dealt at setup.
  - each player: value_b (number, starts 0); only its owner sees it. The player's private value for object B.
  - each player: value_c (number, starts 0); only its owner sees it. The player's private value for object C.
  - each player: value_d (number, starts 0); only its owner sees it. The player's private value for object D.
  - each player: value_e (number, starts 0); only its owner sees it. The player's private value for object E.
  - each player: value_f (number, starts 0); only its owner sees it. The player's private value for object F.
  - each player: value_bag (list, starts [2, 4, 6, 8, 10, 14]); only its owner sees it. The player's own six values, not yet assigned to objects. They are drawn at random during setup, so the list is empty after setup.
  - each player: message (text, starts ''); everyone sees it. This round's talk message, at most 40 words, shown after all are in.
  - each player: bid (number, starts 0); only its owner sees it. This round's sealed bid, revealed to all in the reveal step.
  - each player: bid_key (number, starts 0); only its owner sees it. bid * 10 + (6 - holdings_count). The highest value wins, and a tie at the top means no sale.
  - each player: score (number, starts 0); everyone sees it. Final score: coins + the sum of own values of held objects, computed after round 6.
  - the table: round (number, starts 0); everyone sees it. Current round number, from 1 to 6.
  - the table: pool (list, starts ['A', 'B', 'C', 'D', 'E', 'F']); everyone sees it. Objects still available.
  - the table: top_key (number, starts 0); hidden from all players. Highest bid_key this round.
  - the table: top_count (number, starts 0); hidden from all players. Number of players whose bid_key equals top_key.
  - the table: winner_seat (number, starts 0); everyone sees it. Seat of this round's winner, or 0 for no sale.
  - the table: taken_object (text, starts ''); everyone sees it. Object taken this round, or empty if there was no sale.
  - parameters, each kept as a table attribute: starting_coins = 20, object_count = 6, value_1 = 2, value_2 = 4, value_3 = 6, value_4 = 8, value_5 = 10, value_6 = 14, value_total = 44, rounds = 6, talk_max_words = 40, min_bid = 0, tiebreak_key_multiplier = 10, min_players = 3, max_players = 5, suggested_players = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player starts with coins = 20, empty holdings and holdings_count = 0.
  2. The table pool is set to [A, B, C, D, E, F] and round = 0.
  3. Each player's value_bag starts as [2, 4, 6, 8, 10, 14]. For that player, value_a through value_f are assigned in turn: each draws one value at random from the player's own value_bag and removes it, so each player gets an independent random permutation that totals 44.
  4. Each player's values are visible only to that player (ally).

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; winner_seat = 0; taken_object = ''.
  2. [tell] all players. What happens: Announce round, pool, and every player's coins and holdings.
  3. [poll] all players answers: short text, at most 40 words (words beyond the 40th are dropped). What happens: Set each player's message, truncated to 40 words. Once all are in, broadcast {"to": "all", "text": "Seat {seat} says: {value}"}.
  4. [poll] all players answers: a whole number from 0 to you.coins. What happens: Set each player's bid. A missing, non-integer, negative or over-coins answer sets bid = 0.
  5. [update] all players. What happens: For each player, bid_key = bid * 10 + (6 - holdings_count); top_key = max of bid_key; top_count = number of players with bid_key == top_key; winner_seat = the seat with bid_key == top_key if top_count == 1, else 0.
  6. [update] the winner (when winner_seat != 0). What happens: The winner's coins -= the winner's bid.
  7. [ask] the winner (when winner_seat != 0) answers: one object letter from pool. What happens: Set taken_object to the chosen letter. If there is no valid answer, taken_object = the pool object with the highest of the winner's own values (ties: earliest letter).
  8. [update] the winner (when winner_seat != 0). What happens: Remove taken_object from pool; append it to the winner's holdings; the winner's holdings_count += 1.
  9. [tell] all players. What happens: Reveal every player's bid, the winner (or 'no sale' if winner_seat == 0), and taken_object.
  10. [update] all players (when round == 6). What happens: Pool objects are discarded (pool = []). For each player, score = coins + the sum of value_x over each object x in holdings.
  11. [tell] all players (when round == 6). What happens: Reveal all players' value_a through value_f and every score.
  12. [check] all players. What happens: End the game if round == 6; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each player has 20 coins, no objects, and the pool is A, B, C, D, E, F.
  R2. When values are dealt, then each player's values for A through F are a random permutation of 2, 4, 6, 8, 10, 14, totalling 44, and are visible only to that player.
  R3. When a round begins, then the round number, pool, and every player's coins and holdings are announced to all.
  R4. When players talk, then every player submits one message simultaneously, words beyond the 40th are dropped, and all messages are then shown to everyone.
  R5. When bids are made, then every player simultaneously bids a whole number from 0 to his current coins.
  R6. When a bid is missing, not a whole number, negative or above the bidder's coins, then it counts as 0.
  R7. When one player has the strictly highest bid, then he wins the round.
  R8. When several players share the highest bid, then the one among them with the fewest objects wins.
  R9. When several players share both the highest bid and the fewest objects, then there is no sale: nobody pays, the pool is unchanged, and the round still counts.
  R10. When there is a winner, then his coins decrease by his bid (for example, a bid of 7 from 20 coins leaves 13).
  R11. When the winner names an object in the pool, then it leaves the pool and is added to his holdings.
  R12. When the winner gives no valid object, then he receives the pool object with his highest own value, with ties going to the earliest letter.
  R13. When a player has won earlier rounds, then he may still bid and win again.
  R14. When a round ends, then all bids, the winner or 'no sale', and the object taken are announced to all.
  R15. When round 6 has been played, then the game ends and objects left in the pool are discarded.
  R16. When the game ends, then each player's score = coins + the sum of his own values for his held objects, and all values are revealed.
  R17. When the game ends, then the highest score wins, and a shared highest score is a draw among those players.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every player | options: free text of at most 40 words
  - Sealed bid | asked: every player | options: any whole number from 0 to that player's current coins
  - Pick an object | asked: the round's winner only (no one when there is no sale) | options: each object letter currently in pool

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round == 6
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is his final score: coins left plus the sum of his own values for the objects he holds. The highest score wins, and players level at the top share the result (the source calls this a draw).
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

- each player: `coins` (number, visible: public, starts 20): Coins the player still holds.
- each player: `holdings` (list, visible: public, starts []): Letters of the objects the player has won.
- each player: `score` (number, visible: public, starts 0): Final score: coins + the sum of own values of held objects, computed after round 6.
- the table: `round` (number, visible: public, starts 0): Current round number, from 1 to 6.
- the table: `pool` (list, visible: public, starts ['A', 'B', 'C', 'D', 'E', 'F']): Objects still available.
- the table: `winner_seat` (number, visible: public, starts 0): Seat of this round's winner, or 0 for no sale.
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 20, object_count = 6, value_1 = 2, value_2 = 4, value_3 = 6, value_4 = 8, value_5 = 10, value_6 = 14, value_total = 44, rounds = 6, talk_max_words = 40, min_bid = 0, tiebreak_key_multiplier = 10, min_players = 3, max_players = 5, suggested_players = 3
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


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "bidders_choice_sealed_pool",
    "name": "Bidder's Choice: Sealed Pool",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six rounds of open talk and sealed bids for six objects that each player values privately; coins left plus own values decides."
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
        "key": "holdings",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "holdings_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_a",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_b",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_c",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_d",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_e",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_f",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_bag",
        "visible": "ally",
        "type": "list",
        "initial": [
          2,
          4,
          6,
          8,
          10,
          14
        ]
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_key",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fallback_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
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
        "key": "top_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
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
        "key": "taken_object",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "object_count",
        "visible": "public",
        "type": "number",
        "initial": 6
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
        "key": "value_total",
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
        "key": "talk_max_words",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tiebreak_key_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "min_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "suggested_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
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
            "key": "holdings",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "holdings_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pool",
            "value": {
              "calc": "['A', 'B', 'C', 'D', 'E', 'F']"
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
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "[value_1, value_2, value_3, value_4, value_5, value_6]"
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
            "key": "value_a",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_a"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_b",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_b"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_c",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_c"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_d",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_d"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_e",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_e"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_f",
            "value": {
              "calc": "you.value_bag[0]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_f"
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
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "announce",
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
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "taken_object",
            "value": ""
          }
        },
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
            "key": "bid",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the announcement",
      "to": "all",
      "text": "Round {round} of {rounds}. Objects still in the pool: {pool}. Coins and holdings [seat, coins, holdings]: {[[p.seat, p.coins, p.holdings] for p in players]}."
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
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one message to the table, at most {talk_max_words} words (words beyond that are dropped). Everyone writes at the same time; all messages are then shown to everyone. Messages are not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": "acting",
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
      "text": "Round {round}: submit a sealed bid, a whole number from {min_bid} up to your current coins. A missing or invalid bid counts as 0. Highest bid wins; ties go to the tied bidder holding the fewest objects; if still tied there is no sale."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "find the winner",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid_key",
            "value": {
              "calc": "you.bid * tiebreak_key_multiplier + (object_count - you.holdings_count)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "fallback_pick",
            "value": {
              "calc": "sorted([[-(you.value_a if x == 'A' else you.value_b if x == 'B' else you.value_c if x == 'C' else you.value_d if x == 'D' else you.value_e if x == 'E' else you.value_f), x] for x in pool])[0][1] if len(pool) > 0 else ''"
            }
          }
        },
        {
          "set": {
            "key": "top_key",
            "value": {
              "calc": "max([p.bid_key for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.bid_key == top_key for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.bid_key == top_key][0] if top_count == 1 and len(pool) > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the winner pays",
      "when": {
        "calc": "winner_seat != 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "coins",
            "value": {
              "calc": "-[p.bid for p in players if p.seat == winner_seat][0]"
            },
            "if": {
              "calc": "[p.coins - p.bid for p in players if p.seat == winner_seat][0] >= 0"
            },
            "text": "Seat {player} wins the round and pays the bid."
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick an object",
      "when": {
        "calc": "winner_seat != 0"
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
        "bind": "picked"
      },
      "text": "You won round {round}. Name one object still in the pool: {pool}. If you give no valid answer you receive the pool object with your highest own value."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the object changes hands",
      "when": {
        "calc": "winner_seat != 0"
      },
      "do": [
        {
          "set": {
            "key": "taken_object",
            "value": {
              "calc": "$picked if $picked in pool else [p.fallback_pick for p in players if p.seat == winner_seat][0]"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "taken_object"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "holdings",
            "value": {
              "calc": "taken_object"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "holdings_count",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "when": {
        "calc": "winner_seat != 0"
      },
      "to": "all",
      "text": "Round {round} bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. Winner: seat {winner_seat}, who took object {taken_object}. Pool now: {pool}."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal, no sale",
      "when": {
        "calc": "winner_seat == 0"
      },
      "to": "all",
      "text": "Round {round} bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. No sale: nobody pays and no object is taken. Pool: {pool}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "final scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "key": "pool",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.coins + (you.value_a if 'A' in you.holdings else 0) + (you.value_b if 'B' in you.holdings else 0) + (you.value_c if 'C' in you.holdings else 0) + (you.value_d if 'D' in you.holdings else 0) + (you.value_e if 'E' in you.holdings else 0) + (you.value_f if 'F' in you.holdings else 0)"
            }
          }
        }
      ],
      "text": "Round {rounds} is over. Objects left in the pool are discarded."
    },
    {
      "use": "tell",
      "phase": "final",
      "label": "values revealed",
      "when": {
        "calc": "round >= rounds"
      },
      "to": "all",
      "text": "All values [seat, A, B, C, D, E, F]: {[[p.seat, p.value_a, p.value_b, p.value_c, p.value_d, p.value_e, p.value_f] for p in players]}. Final scores [seat, coins, holdings, score]: {[[p.seat, p.coins, p.holdings, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "final",
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
      "rank_by": "you.score",
      "reveal": [
        "value_a",
        "value_b",
        "value_c",
        "value_d",
        "value_e",
        "value_f"
      ],
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "SETUP. There are 3 to 5 players. Every player starts with {starting_coins} coins and no objects. The pool holds six objects: A, B, C, D, E, F. Each player privately receives the six values {value_1}, {value_2}, {value_3}, {value_4}, {value_5} and {value_6}, one value per object, in an independent random order for each player. Every player's values therefore total {value_total}. A player sees only his own values.\n\nROUNDS. The game lasts exactly {rounds} rounds. Each round:\n1) ANNOUNCE. The round number, the objects still in the pool, every player's coins and every player's holdings are shown to all.\n2) TALK. Every player writes one message of at most {talk_max_words} words at the same time, without seeing the others. Any words beyond the {talk_max_words}th are dropped. Then all messages are shown to everyone. Messages are not binding and may be false.\n3) BID. Every player at the same time submits a sealed bid: a whole number from {min_bid} up to his current coins. A bid that is missing, not a whole number, negative, or above his current coins counts as 0.\n4) WINNER. The highest bid wins. If several players share the highest bid, the one among them holding the fewest objects wins. If several of those also hold equally few objects, there is NO SALE this round: nobody pays, no object leaves the pool, and the round still counts as played.\n5) PAY AND PICK. If there is a winner, he pays his bid, so his coins decrease by his bid. He then names one object still in the pool. That object leaves the pool and is added to his holdings. If he names no object still in the pool, or gives no answer, he receives instead the remaining object with the highest of his own values (ties: earliest letter). A player may win any number of rounds.\n6) REVEAL. All bids, the winner (or 'no sale') and the object taken are announced to all.\n\nEND. After round {rounds}, any objects still in the pool are discarded. Each player's final score = his remaining coins + the sum of HIS OWN values for the objects he holds. All values are then revealed. The player with the highest final score wins. If two or more players share the highest final score, they share the result (a draw among them)."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (fallback_pick, message, message, message) in `your_private_values`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "bidders_choice_sealed_pool",
    "name": "Bidder's Choice: Sealed Pool",
    "players": {
      "min": 3,
      "max": 5,
      "suggested": 3
    },
    "blurb": "Six rounds of open talk and sealed bids for six objects that each player values privately; coins left plus own values decides."
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
        "key": "holdings",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "holdings_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_a",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_b",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_c",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_d",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_e",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_f",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "value_bag",
        "visible": "ally",
        "type": "list",
        "initial": [
          2,
          4,
          6,
          8,
          10,
          14
        ]
      },
      {
        "key": "message",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_key",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fallback_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "score",
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
        "key": "top_key",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_count",
        "visible": "none",
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
        "key": "taken_object",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "starting_coins",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "object_count",
        "visible": "public",
        "type": "number",
        "initial": 6
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
        "key": "value_total",
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
        "key": "talk_max_words",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "min_bid",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tiebreak_key_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "min_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "max_players",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "suggested_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting table",
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
            "key": "holdings",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "holdings_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "pool",
            "value": {
              "calc": "['A', 'B', 'C', 'D', 'E', 'F']"
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
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "[value_1, value_2, value_3, value_4, value_5, value_6]"
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
            "key": "value_a",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_a"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_b",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_b"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_c",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_c"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_d",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_d"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_e",
            "value": {
              "calc": "you.value_bag[min(int(uniform(0, len(you.value_bag))), len(you.value_bag) - 1)]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_e"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "value_f",
            "value": {
              "calc": "you.value_bag[0]"
            }
          }
        },
        {
          "remove": {
            "players": "all",
            "key": "value_bag",
            "value": {
              "calc": "you.value_f"
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
        "coins",
        "holdings",
        "value_a",
        "value_b",
        "value_c",
        "value_d",
        "value_e",
        "value_f"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "announce",
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
            "key": "winner_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "taken_object",
            "value": ""
          }
        },
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
            "key": "bid",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the announcement",
      "to": "all",
      "text": "Round {round} of {rounds}. Objects still in the pool: {pool}. Coins and holdings [seat, coins, holdings]: {[[p.seat, p.coins, p.holdings] for p in players]}."
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
      "store": "message",
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one message to the table, at most {talk_max_words} words (words beyond that are dropped). Everyone writes at the same time; all messages are then shown to everyone. Messages are not binding and may be false."
    },
    {
      "use": "poll",
      "phase": "bid",
      "label": "sealed bid",
      "to": "acting",
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
      "text": "Round {round}: submit a sealed bid, a whole number from {min_bid} up to your current coins. A missing or invalid bid counts as 0. Highest bid wins; ties go to the tied bidder holding the fewest objects; if still tied there is no sale."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "find the winner",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "bid_key",
            "value": {
              "calc": "you.bid * tiebreak_key_multiplier + (object_count - you.holdings_count)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "fallback_pick",
            "value": {
              "calc": "sorted([[-(you.value_a if x == 'A' else you.value_b if x == 'B' else you.value_c if x == 'C' else you.value_d if x == 'D' else you.value_e if x == 'E' else you.value_f), x] for x in pool])[0][1] if len(pool) > 0 else ''"
            }
          }
        },
        {
          "set": {
            "key": "top_key",
            "value": {
              "calc": "max([p.bid_key for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "top_count",
            "value": {
              "calc": "count(p.bid_key == top_key for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "winner_seat",
            "value": {
              "calc": "[p.seat for p in players if p.bid_key == top_key][0] if top_count == 1 and len(pool) > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the winner pays",
      "when": {
        "calc": "winner_seat != 0"
      },
      "do": [
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "coins",
            "value": {
              "calc": "-[p.bid for p in players if p.seat == winner_seat][0]"
            },
            "if": {
              "calc": "[p.coins - p.bid for p in players if p.seat == winner_seat][0] >= 0"
            },
            "text": "Seat {player} wins the round and pays the bid."
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "resolve",
      "label": "pick an object",
      "when": {
        "calc": "winner_seat != 0"
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
        "bind": "picked"
      },
      "text": "You won round {round}. Name one object still in the pool: {pool}. If you give no valid answer you receive the pool object with your highest own value."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the object changes hands",
      "when": {
        "calc": "winner_seat != 0"
      },
      "do": [
        {
          "set": {
            "key": "taken_object",
            "value": {
              "calc": "$picked if $picked in pool else [p.fallback_pick for p in players if p.seat == winner_seat][0]"
            }
          }
        },
        {
          "remove": {
            "key": "pool",
            "value": {
              "calc": "taken_object"
            }
          }
        },
        {
          "append": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "holdings",
            "value": {
              "calc": "taken_object"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "winner_seat"
            },
            "key": "holdings_count",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "when": {
        "calc": "winner_seat != 0"
      },
      "to": "all",
      "text": "Round {round} bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. Winner: seat {winner_seat}, who took object {taken_object}. Pool now: {pool}."
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal, no sale",
      "when": {
        "calc": "winner_seat == 0"
      },
      "to": "all",
      "text": "Round {round} bids [seat, bid]: {[[p.seat, p.bid] for p in players]}. No sale: nobody pays and no object is taken. Pool: {pool}."
    },
    {
      "use": "update",
      "phase": "final",
      "label": "final scoring",
      "when": {
        "calc": "round >= rounds"
      },
      "do": [
        {
          "set": {
            "key": "pool",
            "value": {
              "calc": "[]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "you.coins + (you.value_a if 'A' in you.holdings else 0) + (you.value_b if 'B' in you.holdings else 0) + (you.value_c if 'C' in you.holdings else 0) + (you.value_d if 'D' in you.holdings else 0) + (you.value_e if 'E' in you.holdings else 0) + (you.value_f if 'F' in you.holdings else 0)"
            }
          }
        }
      ],
      "text": "Round {rounds} is over. Objects left in the pool are discarded."
    },
    {
      "use": "tell",
      "phase": "final",
      "label": "values revealed",
      "when": {
        "calc": "round >= rounds"
      },
      "to": "all",
      "text": "All values [seat, A, B, C, D, E, F]: {[[p.seat, p.value_a, p.value_b, p.value_c, p.value_d, p.value_e, p.value_f] for p in players]}. Final scores [seat, coins, holdings, score]: {[[p.seat, p.coins, p.holdings, p.score] for p in players]}."
    },
    {
      "use": "check",
      "phase": "final",
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
      "rank_by": "you.score",
      "reveal": [
        "value_a",
        "value_b",
        "value_c",
        "value_d",
        "value_e",
        "value_f"
      ],
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "SETUP. There are 3 to 5 players. Every player starts with {starting_coins} coins and no objects. The pool holds six objects: A, B, C, D, E, F. Each player privately receives the six values {value_1}, {value_2}, {value_3}, {value_4}, {value_5} and {value_6}, one value per object, in an independent random order for each player. Every player's values therefore total {value_total}. A player sees only his own values.\n\nROUNDS. The game lasts exactly {rounds} rounds. Each round:\n1) ANNOUNCE. The round number, the objects still in the pool, every player's coins and every player's holdings are shown to all.\n2) TALK. Every player writes one message of at most {talk_max_words} words at the same time, without seeing the others. Any words beyond the {talk_max_words}th are dropped. Then all messages are shown to everyone. Messages are not binding and may be false.\n3) BID. Every player at the same time submits a sealed bid: a whole number from {min_bid} up to his current coins. A bid that is missing, not a whole number, negative, or above his current coins counts as 0.\n4) WINNER. The highest bid wins. If several players share the highest bid, the one among them holding the fewest objects wins. If several of those also hold equally few objects, there is NO SALE this round: nobody pays, no object leaves the pool, and the round still counts as played.\n5) PAY AND PICK. If there is a winner, he pays his bid, so his coins decrease by his bid. He then names one object still in the pool. That object leaves the pool and is added to his holdings. If he names no object still in the pool, or gives no answer, he receives instead the remaining object with the highest of his own values (ties: earliest letter). A player may win any number of rounds.\n6) REVEAL. All bids, the winner (or 'no sale') and the object taken are announced to all.\n\nEND. After round {rounds}, any objects still in the pool are discarded. Each player's final score = his remaining coins + the sum of HIS OWN values for the objects he holds. All values are then revealed. The player with the highest final score wins. If two or more players share the highest final score, they share the result (a draw among them)."
}
```
````
