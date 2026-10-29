# 07 coder

- time: 2026-10-27T16:44:56+00:00 (69.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 1b29068a965e8138, reply sha256 5b90c998845b5f56

## Sent

````
# Task: write the XColos game file for "Coloretto: Secret Favourites"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

COMPONENTS. 38 cards: 7 each of Red, Blue, Green, Yellow and Purple, plus 3 '+2' cards. There are three rows, numbered 1, 2 and 3, and each holds at most 3 cards.

SETUP. Shuffle the 38 cards into a face-down deck. The top card is always shown face up to everyone. Deal each player a different secret Favourite colour, chosen at random from the 5 colours. Only that player knows it. All rows start empty and open. No player has taken. Player 1 is active.

CYCLE. A cycle runs until all three players have taken a row.
- A player who has taken a row in the current cycle sits out until the cycle ends.
- A row that has been taken is closed for the rest of the cycle.
- When the third player takes, the cycle ends immediately. All three rows reopen empty, all players become eligible again, and the player who took last is active.

TURN (one per round, 36 rounds). The game shows everyone: the face-up top card, the contents of every row and whether it is open, every player's collected cards, who has taken this cycle, and the turn number. The active player chooses one action:
(a) PLACE on row k. This is legal only if row k is open and has fewer than 3 cards. Move the top card onto row k; the next card becomes the face-up top card.
(b) TAKE row k. This is legal only if row k is open and has at least 1 card. Add all its cards to your collection, close the row, and mark yourself as taken.
If every open row is full, the player must TAKE. An illegal or missing choice becomes TAKE of the lowest-numbered open row that has a card. If there is none, it becomes PLACE on the lowest-numbered open row that has room.

NEXT ACTIVE PLAYER. After a PLACE, or after a TAKE that does not end the cycle, the next active player is the next player in seat order (1, 2, 3, 1, ...) who has not taken this cycle. This may be the same player again if they are the only one left; that player may keep placing on the remaining row until it is full, then must take it.

END. The game ends after round 36. Cards still lying in rows are discarded.

SCORING. For each colour, count the cards of that colour you hold and convert the count to points: 0 = 0, 1 = 1, 2 = 3, 3 = 6, 4 = 10, 5 = 15, 6 = 21, 7 = 28.
- Your three colours with the highest counts score positive. If counts tie for third place, either tied colour can be counted; the points are the same.
- Your other two colours score negative.
- Add 2 for each '+2' card you hold.
- Add 6 if your Favourite colour's count is at least your third-highest colour count, that is, if it can be one of your scoring colours.
All favourites are revealed at the end.

How the winner is decided: The player with the highest final score wins. If two or three players tie for the highest score, those players draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Coloretto: Secret Favourites (3 to 3 players, best with 3)

Three players take turns either adding the face-up card to one of three rows or taking a row. They collect colours, score their best three and lose points for the rest, and earn a bonus for a secret Favourite colour.

STATE (every item below must exist in the file):
  - each player: red (number, starts 0); everyone sees it. Red cards collected
  - each player: blue (number, starts 0); everyone sees it. Blue cards collected
  - each player: green (number, starts 0); everyone sees it. Green cards collected
  - each player: yellow (number, starts 0); everyone sees it. Yellow cards collected
  - each player: purple (number, starts 0); everyone sees it. Purple cards collected
  - each player: plus_two (number, starts 0); everyone sees it. '+2' cards collected
  - each player: favourite (text, starts ''); only its owner sees it. Secret Favourite colour, known only to its owner during play
  - each player: favourite_revealed (text, starts ''); everyone sees it. Favourite colour, copied here when all favourites are revealed at the end
  - each player: taken (bool, starts False); everyone sees it. Has taken a row in the current cycle
  - each player: score (number, starts 0); everyone sees it. Final score, computed after round 36
  - the table: deck (list, starts '7 each of red, blue, green, yellow, purple plus 3 plus_two (38 cards)'); hidden from all players. Face-down draw deck
  - the table: favourite_pool (list, starts ['red', 'blue', 'green', 'yellow', 'purple']); hidden from all players. Colours not yet dealt as favourites
  - the table: top_card (text, starts ''); everyone sees it. Face-up top card of the deck
  - the table: row_1 (list, starts []); everyone sees it. Cards in row 1
  - the table: row_2 (list, starts []); everyone sees it. Cards in row 2
  - the table: row_3 (list, starts []); everyone sees it. Cards in row 3
  - the table: row_1_open (bool, starts True); everyone sees it. Row 1 not yet taken this cycle
  - the table: row_2_open (bool, starts True); everyone sees it. Row 2 not yet taken this cycle
  - the table: row_3_open (bool, starts True); everyone sees it. Row 3 not yet taken this cycle
  - the table: takers (number, starts 0); everyone sees it. Players who have taken this cycle
  - the table: active_seat (number, starts 1); everyone sees it. Seat of the active player
  - the table: turn (number, starts 1); everyone sees it. Current turn number
  - parameters, each kept as a table attribute: colours = 5, cards_per_colour = 7, plus_two_cards = 3, deck_size = 38, rows = 3, row_capacity = 3, rounds = 36, positive_colours = 3, negative_colours = 2, plus_two_value = 2, favourite_bonus = 6, points_for_count_0 = 0, points_for_count_1 = 1, points_for_count_2 = 3, points_for_count_3 = 6, points_for_count_4 = 10, points_for_count_5 = 15, points_for_count_6 = 21, points_for_count_7 = 28

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Fill the deck with the 38 cards: 7 each of red, blue, green, yellow and purple, plus 3 plus_two.
  2. Draw one card at random from deck into top_card, where it is face up for everyone.
  3. For each player, draw one colour at random from favourite_pool into that player's favourite and remove it from the pool, so every favourite is different and private.
  4. All rows are empty and open, no player has taken, takers = 0, active_seat = 1 and turn = 1.
  5. Send each player their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] all players. What happens: Everyone sees top_card, row_1..row_3 with their open flags, every player's colour counts and plus_two, every taken flag and turn. Each player also sees their own favourite.
  2. [ask] the player at seat game.active_seat answers: one of: place_1, place_2, place_3, take_1, take_2, take_3, limited to the legal options (see offers). What happens: Records the chosen action. An illegal or missing choice becomes take of the lowest-numbered open row with at least 1 card; if there is none, it becomes place on the lowest-numbered open row with fewer than 3 cards.
  3. [update] the active player. What happens: When the action is place_k: append top_card to row_k, then draw a random card from deck into top_card and remove it from deck.
  4. [update] the active player. What happens: When the action is take_k: for each card in row_k, add 1 to the active player's matching colour count, or to plus_two for a '+2' card. Then set row_k = [], row_k_open = false, active.taken = true and takers += 1.
  5. [update] table. What happens: When takers < 3: set active_seat to the first seat in order active_seat+1, active_seat+2, active_seat (wrapping 3 to 1) whose taken is false. This may be the same seat again.
  6. [update] table. What happens: When takers == 3 (the cycle has ended): set row_1, row_2 and row_3 to [], set every row_k_open = true, set every player's taken = false and takers = 0. active_seat stays the player who took last.
  7. [update] table. What happens: turn += 1.
  8. [update] all players. What happens: When turn > 36: rows are discarded. For each player, sort the counts of red, blue, green, yellow and purple from highest to lowest as s1..s5, with T(c) = c*(c+1)/2. Set score = T(s1)+T(s2)+T(s3) - T(s4) - T(s5) + 2*plus_two + (6 if the favourite colour's count >= s3, else 0). Copy favourite into favourite_revealed.
  9. [check] table. What happens: End the game when turn > 36; otherwise run the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the deck holds 38 cards (7 each of 5 colours plus 3 '+2'), and one random card is face up as top_card.
  R2. At setup each player receives a different random Favourite colour, visible only to that player.
  R3. When a player chooses place_k, then the action is legal only if row_k is open and holds fewer than 3 cards; top_card is appended to row_k and a new top_card is drawn from deck.
  R4. When a player chooses take_k, then the action is legal only if row_k is open and holds at least 1 card; every card in row_k is added to that player's counts, row_k becomes empty and closed, and the player is marked taken.
  R5. When every open row holds 3 cards, then the active player is offered only take options.
  R6. When a choice is illegal or missing, then it becomes take of the lowest-numbered open row with a card; if there is none, it becomes place on the lowest-numbered open row with room.
  R7. When a player has taken a row this cycle, then that player is never active again until the cycle ends.
  R8. When a place or a non-final take happens, then the next active player is the next seat in order 1,2,3,1 whose taken is false, which may be the same player.
  R9. When the third player takes in a cycle, then all three rows reopen empty, all taken flags reset to false, and the player who took last stays active.
  R10. When a '+2' card is taken, then the taker's plus_two rises by 1.
  R11. When round 36 has been played, then the game ends and cards left in rows are discarded.
  R12. When scoring, then a colour count c is worth c*(c+1)/2 points (0,1,3,6,10,15,21,28 for 0 to 7).
  R13. When scoring, then the three highest colour counts score positive and the other two score negative.
  R14. When scoring, then each '+2' card adds 2 points.
  R15. When the player's Favourite colour count is at least their third-highest colour count, then they gain 6 points.
  R16. When the game ends, then every player's Favourite is revealed in favourite_revealed.
  R17. When the game ends, then the highest score wins, and players tied for the highest score draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Active player's action | asked: seat game.active_seat | options: place_k for each row k that is open and holds fewer than 3 cards, and take_k for each row k that is open and holds at least 1 card. If every open row is full, only the take_k options. A seat that has taken this cycle is never asked.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game.turn > 36
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's final score is their best three colours positive, their other two colours negative, plus 2 per '+2' card, plus 6 if their Favourite is among the colours that can score. The highest score wins, and players tied for the highest score draw (share the win).
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

- each player: `favourite_revealed` (text, visible: public, starts ''): Favourite colour, copied here when all favourites are revealed at the end
- each player: `score` (number, visible: public, starts 0): Final score, computed after round 36
- the table: `turn` (number, visible: public, starts 1): Current turn number
- parameters (each must be an attribute holding this value, never a number buried in a step): colours = 5, cards_per_colour = 7, plus_two_cards = 3, deck_size = 38, rows = 3, row_capacity = 3, rounds = 36, positive_colours = 3, negative_colours = 2, plus_two_value = 2, favourite_bonus = 6, points_for_count_0 = 0, points_for_count_1 = 1, points_for_count_2 = 3, points_for_count_3 = 6, points_for_count_4 = 10, points_for_count_5 = 15, points_for_count_6 = 21, points_for_count_7 = 28
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
{
  "schema": 1,
  "meta": {
    "id": "coloretto_secret_favourites",
    "name": "Coloretto: Secret Favourites",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Add the face-up card to a row or take a row. Score your best three colours, lose points for the rest, and earn a bonus for your secret Favourite."
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
        "key": "red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "purple",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "plus_two",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "favourite",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "favourite_revealed",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "red", "red", "red", "red", "red", "red", "red",
          "blue", "blue", "blue", "blue", "blue", "blue", "blue",
          "green", "green", "green", "green", "green", "green", "green",
          "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow",
          "purple", "purple", "purple", "purple", "purple", "purple", "purple",
          "plus_two", "plus_two", "plus_two"
        ]
      },
      {
        "key": "favourite_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "red",
          "blue",
          "green",
          "yellow",
          "purple"
        ]
      },
      {
        "key": "top_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "row_1",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_2",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_3",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_1_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "row_2_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "row_3_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "takers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "legal",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "fallback",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "action",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "points_table",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "plus_two_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 38
      },
      {
        "key": "rows",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "row_capacity",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "positive_colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "negative_colours",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "plus_two_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "favourite_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "points_for_count_0",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_for_count_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_for_count_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_for_count_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "points_for_count_4",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_for_count_5",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "points_for_count_6",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "points_for_count_7",
        "visible": "public",
        "type": "number",
        "initial": 28
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "red", "red", "red", "red", "red", "red", "red",
              "blue", "blue", "blue", "blue", "blue", "blue", "blue",
              "green", "green", "green", "green", "green", "green", "green",
              "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow",
              "purple", "purple", "purple", "purple", "purple", "purple", "purple",
              "plus_two", "plus_two", "plus_two"
            ]
          }
        },
        {
          "set": {
            "key": "points_table",
            "value": {
              "calc": "[points_for_count_0, points_for_count_1, points_for_count_2, points_for_count_3, points_for_count_4, points_for_count_5, points_for_count_6, points_for_count_7]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "turn up the top card",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ],
      "text": "The face-up top card is {top_card}."
    },
    {
      "use": "update",
      "label": "deal the favourites",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "open the rows",
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": false
          }
        },
        {
          "set": {
            "key": "takers",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 1
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
      "use": "sync",
      "phase": "turn",
      "label": "the state",
      "mode": "self",
      "to": "all",
      "text": "Turn {turn}. Top card {top_card}. Row 1 {row_1} (open {row_1_open}), row 2 {row_2} (open {row_2_open}), row 3 {row_3} (open {row_3_open}). Active seat {active_seat}. Your state:"
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the offer",
      "do": [
        {
          "set": {
            "key": "legal",
            "value": {
              "calc": "(['place_1'] if row_1_open and len(row_1) < row_capacity else []) + (['place_2'] if row_2_open and len(row_2) < row_capacity else []) + (['place_3'] if row_3_open and len(row_3) < row_capacity else []) + (['take_1'] if row_1_open and len(row_1) > 0 else []) + (['take_2'] if row_2_open and len(row_2) > 0 else []) + (['take_3'] if row_3_open and len(row_3) > 0 else [])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "legal if you.seat == active_seat and not you.taken else []"
            }
          }
        },
        {
          "set": {
            "key": "fallback",
            "value": {
              "calc": "'take_1' if row_1_open and len(row_1) > 0 else ('take_2' if row_2_open and len(row_2) > 0 else ('take_3' if row_3_open and len(row_3) > 0 else ('place_1' if row_1_open and len(row_1) < row_capacity else ('place_2' if row_2_open and len(row_2) < row_capacity else 'place_3'))))"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "the action",
      "to": {
        "where": "you.seat == active_seat and not you.taken"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "choice"
      },
      "text": "Turn {turn}. Top card: {top_card}. Row 1: {row_1} (open {row_1_open}). Row 2: {row_2} (open {row_2_open}). Row 3: {row_3} (open {row_3_open}). Choose place_k to put the top card on open row k (fewer than {row_capacity} cards), or take_k to collect every card in open row k (at least 1 card)."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "record and place",
      "do": [
        {
          "set": {
            "key": "action",
            "value": {
              "calc": "$choice if $choice in legal else fallback"
            }
          }
        },
        {
          "append": {
            "key": "row_1",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_1'"
            },
            "text": "Seat {active_seat} places {value} on row 1."
          }
        },
        {
          "append": {
            "key": "row_2",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_2'"
            },
            "text": "Seat {active_seat} places {value} on row 2."
          }
        },
        {
          "append": {
            "key": "row_3",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_3'"
            },
            "text": "Seat {active_seat} places {value} on row 3."
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": "",
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) == 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            },
            "text": "The new top card is {value}."
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "take a row",
      "when": {
        "calc": "action in ['take_1', 'take_2', 'take_3']"
      },
      "do": [
        {
          "set": {
            "key": "taken_cards",
            "value": {
              "calc": "row_1 if action == 'take_1' else (row_2 if action == 'take_2' else row_3)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "count(c == 'red' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "count(c == 'blue' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "count(c == 'green' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "yellow",
            "value": {
              "calc": "count(c == 'yellow' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "purple",
            "value": {
              "calc": "count(c == 'purple' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "plus_two",
            "value": {
              "calc": "count(c == 'plus_two' for c in taken_cards)"
            }
          }
        },
        {
          "set": {
            "key": "row_1",
            "value": [],
            "if": {
              "calc": "action == 'take_1'"
            }
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": false,
            "if": {
              "calc": "action == 'take_1'"
            }
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": [],
            "if": {
              "calc": "action == 'take_2'"
            }
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": false,
            "if": {
              "calc": "action == 'take_2'"
            }
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": [],
            "if": {
              "calc": "action == 'take_3'"
            }
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": false,
            "if": {
              "calc": "action == 'take_3'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "taken",
            "value": true,
            "text": "Seat {player} takes a row: {taken_cards}."
          }
        },
        {
          "adjust": {
            "key": "takers",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next active player",
      "when": {
        "calc": "takers < len(players)"
      },
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "[s for s in [active_seat % len(players) + 1, (active_seat + 1) % len(players) + 1, active_seat] if not players[s - 1].taken][0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the cycle ends",
      "when": {
        "calc": "takers >= len(players)"
      },
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": false
          }
        },
        {
          "set": {
            "key": "takers",
            "value": 0,
            "text": "The cycle ends. All three rows reopen empty and seat {active_seat}, who took last, is active."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "advance the turn",
      "do": [
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "turn > rounds"
      },
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[4]] + points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[3]] + points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[2]] - points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[1]] - points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[0]] + plus_two_value * you.plus_two + (favourite_bonus if (you.red if you.favourite == 'red' else (you.blue if you.favourite == 'blue' else (you.green if you.favourite == 'green' else (you.yellow if you.favourite == 'yellow' else you.purple)))) >= sorted([you.red, you.blue, you.green, you.yellow, you.purple])[2] else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "favourite_revealed",
            "value": {
              "calc": "you.favourite"
            },
            "text": "Seat {player}'s Favourite was {value}."
          }
        }
      ],
      "text": "The game is over. Cards left in rows are discarded and the scores are counted."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last turn",
      "when": {
        "calc": "turn > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "turn > rounds"
      },
      "rank_by": "you.score",
      "reveal": [
        "favourite"
      ],
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}. Favourites: Seat 1 {players[0].favourite_revealed}, Seat 2 {players[1].favourite_revealed}, Seat 3 {players[2].favourite_revealed}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "COMPONENTS. {deck_size} cards: {cards_per_colour} each of Red, Blue, Green, Yellow and Pur
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (favourite_revealed, favourite_revealed, favourite_revealed) in `the_state`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "coloretto_secret_favourites",
    "name": "Coloretto: Secret Favourites",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Add the face-up card to a row or take a row. Score your best three colours, lose points for the rest, and earn a bonus for your secret Favourite."
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
        "key": "red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "purple",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "plus_two",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "favourite",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "favourite_revealed",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "red",
          "red",
          "red",
          "red",
          "red",
          "red",
          "red",
          "blue",
          "blue",
          "blue",
          "blue",
          "blue",
          "blue",
          "blue",
          "green",
          "green",
          "green",
          "green",
          "green",
          "green",
          "green",
          "yellow",
          "yellow",
          "yellow",
          "yellow",
          "yellow",
          "yellow",
          "yellow",
          "purple",
          "purple",
          "purple",
          "purple",
          "purple",
          "purple",
          "purple",
          "plus_two",
          "plus_two",
          "plus_two"
        ]
      },
      {
        "key": "favourite_pool",
        "visible": "none",
        "type": "list",
        "initial": [
          "red",
          "blue",
          "green",
          "yellow",
          "purple"
        ]
      },
      {
        "key": "top_card",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "row_1",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_2",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_3",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "row_1_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "row_2_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "row_3_open",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "takers",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "legal",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "fallback",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "action",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "taken_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "points_table",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "cards_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "plus_two_cards",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 38
      },
      {
        "key": "rows",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "row_capacity",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 36
      },
      {
        "key": "positive_colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "negative_colours",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "plus_two_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "favourite_bonus",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "points_for_count_0",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "points_for_count_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "points_for_count_2",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "points_for_count_3",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "points_for_count_4",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "points_for_count_5",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "points_for_count_6",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "points_for_count_7",
        "visible": "public",
        "type": "number",
        "initial": 28
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "fill the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": [
              "red",
              "red",
              "red",
              "red",
              "red",
              "red",
              "red",
              "blue",
              "blue",
              "blue",
              "blue",
              "blue",
              "blue",
              "blue",
              "green",
              "green",
              "green",
              "green",
              "green",
              "green",
              "green",
              "yellow",
              "yellow",
              "yellow",
              "yellow",
              "yellow",
              "yellow",
              "yellow",
              "purple",
              "purple",
              "purple",
              "purple",
              "purple",
              "purple",
              "purple",
              "plus_two",
              "plus_two",
              "plus_two"
            ]
          }
        },
        {
          "set": {
            "key": "points_table",
            "value": {
              "calc": "[points_for_count_0, points_for_count_1, points_for_count_2, points_for_count_3, points_for_count_4, points_for_count_5, points_for_count_6, points_for_count_7]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "turn up the top card",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            }
          }
        }
      ],
      "text": "The face-up top card is {top_card}."
    },
    {
      "use": "update",
      "label": "deal the favourites",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "favourite_pool[int(uniform(0, len(favourite_pool)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "favourite",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "favourite_pool",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "open the rows",
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": false
          }
        },
        {
          "set": {
            "key": "takers",
            "value": 0
          }
        },
        {
          "set": {
            "key": "active_seat",
            "value": 1
          }
        },
        {
          "set": {
            "key": "turn",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "plus_two",
        "favourite",
        "taken"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "sync",
      "phase": "turn",
      "label": "the state",
      "mode": "self",
      "to": "all",
      "fields": [
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "plus_two",
        "favourite",
        "taken"
      ],
      "text": "Turn {turn}. Top card {top_card}. Row 1 {row_1} (open {row_1_open}), row 2 {row_2} (open {row_2_open}), row 3 {row_3} (open {row_3_open}). Active seat {active_seat}. Your state:"
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the offer",
      "do": [
        {
          "set": {
            "key": "legal",
            "value": {
              "calc": "(['place_1'] if row_1_open and len(row_1) < row_capacity else []) + (['place_2'] if row_2_open and len(row_2) < row_capacity else []) + (['place_3'] if row_3_open and len(row_3) < row_capacity else []) + (['take_1'] if row_1_open and len(row_1) > 0 else []) + (['take_2'] if row_2_open and len(row_2) > 0 else []) + (['take_3'] if row_3_open and len(row_3) > 0 else [])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "legal if you.seat == active_seat and not you.taken else []"
            }
          }
        },
        {
          "set": {
            "key": "fallback",
            "value": {
              "calc": "'take_1' if row_1_open and len(row_1) > 0 else ('take_2' if row_2_open and len(row_2) > 0 else ('take_3' if row_3_open and len(row_3) > 0 else ('place_1' if row_1_open and len(row_1) < row_capacity else ('place_2' if row_2_open and len(row_2) < row_capacity else 'place_3'))))"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "the action",
      "to": {
        "where": "you.seat == active_seat and not you.taken"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "choice"
      },
      "text": "Turn {turn}. Top card: {top_card}. Row 1: {row_1} (open {row_1_open}). Row 2: {row_2} (open {row_2_open}). Row 3: {row_3} (open {row_3_open}). Choose place_k to put the top card on open row k (fewer than {row_capacity} cards), or take_k to collect every card in open row k (at least 1 card)."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "record and place",
      "do": [
        {
          "set": {
            "key": "action",
            "value": {
              "calc": "$choice if $choice in legal else fallback"
            }
          }
        },
        {
          "append": {
            "key": "row_1",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_1'"
            },
            "text": "Seat {active_seat} places {value} on row 1."
          }
        },
        {
          "append": {
            "key": "row_2",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_2'"
            },
            "text": "Seat {active_seat} places {value} on row 2."
          }
        },
        {
          "append": {
            "key": "row_3",
            "value": {
              "calc": "top_card"
            },
            "if": {
              "calc": "action == 'place_3'"
            },
            "text": "Seat {active_seat} places {value} on row 3."
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": "",
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) == 0"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            }
          }
        },
        {
          "set": {
            "key": "top_card",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            },
            "text": "The new top card is {value}."
          }
        },
        {
          "remove": {
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "action in ['place_1', 'place_2', 'place_3'] and len(deck) > 0"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "take a row",
      "when": {
        "calc": "action in ['take_1', 'take_2', 'take_3']"
      },
      "do": [
        {
          "set": {
            "key": "taken_cards",
            "value": {
              "calc": "row_1 if action == 'take_1' else (row_2 if action == 'take_2' else row_3)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "red",
            "value": {
              "calc": "count(c == 'red' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "blue",
            "value": {
              "calc": "count(c == 'blue' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "green",
            "value": {
              "calc": "count(c == 'green' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "yellow",
            "value": {
              "calc": "count(c == 'yellow' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "purple",
            "value": {
              "calc": "count(c == 'purple' for c in taken_cards)"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "active_seat"
            },
            "key": "plus_two",
            "value": {
              "calc": "count(c == 'plus_two' for c in taken_cards)"
            }
          }
        },
        {
          "set": {
            "key": "row_1",
            "value": [],
            "if": {
              "calc": "action == 'take_1'"
            }
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": false,
            "if": {
              "calc": "action == 'take_1'"
            }
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": [],
            "if": {
              "calc": "action == 'take_2'"
            }
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": false,
            "if": {
              "calc": "action == 'take_2'"
            }
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": [],
            "if": {
              "calc": "action == 'take_3'"
            }
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": false,
            "if": {
              "calc": "action == 'take_3'"
            }
          }
        },
        {
          "set": {
            "player": {
              "calc": "active_seat"
            },
            "key": "taken",
            "value": true,
            "text": "Seat {player} takes a row: {taken_cards}."
          }
        },
        {
          "adjust": {
            "key": "takers",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "next active player",
      "when": {
        "calc": "takers < len(players)"
      },
      "do": [
        {
          "set": {
            "key": "active_seat",
            "value": {
              "calc": "[s for s in [active_seat % len(players) + 1, (active_seat + 1) % len(players) + 1, active_seat] if not players[s - 1].taken][0]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the cycle ends",
      "when": {
        "calc": "takers >= len(players)"
      },
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_1_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_2_open",
            "value": true
          }
        },
        {
          "set": {
            "key": "row_3_open",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "taken",
            "value": false
          }
        },
        {
          "set": {
            "key": "takers",
            "value": 0,
            "text": "The cycle ends. All three rows reopen empty and seat {active_seat}, who took last, is active."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "advance the turn",
      "do": [
        {
          "adjust": {
            "key": "turn",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "turn > rounds"
      },
      "do": [
        {
          "set": {
            "key": "row_1",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_2",
            "value": []
          }
        },
        {
          "set": {
            "key": "row_3",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[4]] + points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[3]] + points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[2]] - points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[1]] - points_table[sorted([you.red, you.blue, you.green, you.yellow, you.purple])[0]] + plus_two_value * you.plus_two + (favourite_bonus if (you.red if you.favourite == 'red' else (you.blue if you.favourite == 'blue' else (you.green if you.favourite == 'green' else (you.yellow if you.favourite == 'yellow' else you.purple)))) >= sorted([you.red, you.blue, you.green, you.yellow, you.purple])[2] else 0)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "favourite_revealed",
            "value": {
              "calc": "you.favourite"
            },
            "text": "Seat {player}'s Favourite was {value}."
          }
        }
      ],
      "text": "The game is over. Cards left in rows are discarded and the scores are counted."
    },
    {
      "use": "check",
      "phase": "scoring",
      "label": "after the last turn",
      "when": {
        "calc": "turn > rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "turn > rounds"
      },
      "rank_by": "you.score",
      "reveal": [
        "favourite"
      ],
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}. Favourites: Seat 1 {players[0].favourite_revealed}, Seat 2 {players[1].favourite_revealed}, Seat 3 {players[2].favourite_revealed}."
    }
  },
  "limits": {
    "rounds": 36,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "COMPONENTS. {deck_size} cards: {cards_per_colour} each of Red, Blue, Green, Yellow and Purple ({colours} colours), plus {plus_two_cards} '+2' cards. There are {rows} rows, numbered 1, 2 and 3, and each holds at most {row_capacity} cards.\n\nSETUP. The {deck_size} cards are shuffled into a face-down deck. The top card is always shown face up to everyone. Each player is dealt a different secret Favourite colour, chosen at random from the {colours} colours. Only that player knows it. All rows start empty and open. No player has taken. Player 1 is active.\n\nCYCLE. A cycle runs until all three players have taken a row. A player who has taken a row in the current cycle sits out until the cycle ends. A row that has been taken is closed for the rest of the cycle. When the third player takes, the cycle ends immediately: all three rows reopen empty, all players become eligible again, and the player who took last is active.\n\nTURN (one per round, {rounds} rounds). Everyone sees the face-up top card, the contents of every row and whether it is open, every player's collected cards, who has taken this cycle, and the turn number. The active player chooses one action:\n(a) PLACE on row k (place_k). Legal only if row k is open and has fewer than {row_capacity} cards. The top card moves onto row k and the next card becomes the face-up top card.\n(b) TAKE row k (take_k). Legal only if row k is open and has at least 1 card. All its cards are added to your collection, the row closes, and you are marked as taken.\nYou are offered only the legal actions. If every open row is full, you must TAKE: only take options are offered. An illegal or missing choice becomes TAKE of the lowest-numbered open row that has a card; if there is none, it becomes PLACE on the lowest-numbered open row that has room.\n\nNEXT ACTIVE PLAYER. After a PLACE, or after a TAKE that does not end the cycle, the next active player is the next player in seat order (1, 2, 3, 1, ...) who has not taken this cycle. This may be the same player again if they are the only one left; that player may keep placing on the remaining row until it is full, then must take it.\n\nEND. The game ends after round {rounds}. Cards still lying in rows are discarded.\n\nSCORING. For each colour, count the cards of that colour you hold and convert the count to points: 0 = {points_for_count_0}, 1 = {points_for_count_1}, 2 = {points_for_count_2}, 3 = {points_for_count_3}, 4 = {points_for_count_4}, 5 = {points_for_count_5}, 6 = {points_for_count_6}, 7 = {points_for_count_7}. Your {positive_colours} colours with the highest counts score positive; if counts tie for third place, either tied colour can be counted, the points are the same. Your other {negative_colours} colours score negative. Add {plus_two_value} for each '+2' card you hold. Add {favourite_bonus} if your Favourite colour's count is at least your third-highest colour count (it can be one of your scoring colours); otherwise you get no bonus. All Favourites are revealed at the end.\n\nWINNER. The player with the highest final score wins. If two or three players tie for the highest score, those players draw and share the win."
}
```
````
