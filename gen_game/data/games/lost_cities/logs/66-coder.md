# 66 coder

- time: 2026-10-27T10:35:34+00:00 (76.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 e9de03fc1047127d, reply sha256 06c4c9cc5f083b91

## Sent

````
# Task: write the XColos game file for "Lost Cities: Wager Draft"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

SETUP
1. The deck has 27 cards: Red, Blue and Green, each with one card of every value from 2 to 10. It is shuffled once, face down. Both players know this composition.
2. Each player has three expeditions, one per colour. Each starts empty and is tracked by its top value (0 when empty) and its sum. Each player also has a Burial penalty starting at 0. All of these are public.

EACH ROUND (12 rounds)
3. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds. This is announced.
4. The top two cards of the deck are turned face up as Card A and Card B. Their colours and values are shown to both players.
5. WAGER, at the start of round 5 only, before step 4's cards are revealed:
   - Both players secretly and at the same moment name one colour: Red, Blue or Green. This is their Wager.
   - The Wager cannot be changed and stays hidden until the end.
6. The priority player chooses A, B or NONE.
7. If they chose a card, they receive it and place it (see step 10).
8. The other player is told what was chosen. They then choose A, B or NONE. Naming the card already taken counts as NONE.
9. If they chose a card, they receive it and place it.
10. Placement is mandatory:
   - If the card's value is higher than the top value of that player's expedition in its colour (any card beats an empty expedition), it is added. Its value is added to the sum, and it becomes the new top value.
   - Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by 3.
11. Cards in the row that no one took are removed from the game.
12. Both choices, where each card went, and all expedition states and Burial penalties are announced.

After round 12, the 3 cards left in the deck are never revealed.

FINAL SCORING, for each player and each colour
13. An empty expedition scores 0. However, if the empty expedition is in the player's Wager colour, it scores -15.
14. Otherwise, the base is the sum minus 10.
15. If the colour is the player's Wager colour, the base is doubled. Negative bases are doubled too.
16. Add 10 if the expedition's sum is 25 or more.
17. A player's total is the sum of their three colour scores minus their Burial penalty.
18. Wagers are revealed and the totals are compared.

How the winner is decided: After round 12, the player with the higher total wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Lost Cities: Wager Draft (2 to 2 players, best with 2)

Two players draft face-up cards from a 27-card, three-colour deck over 12 rounds. They build rising expeditions, pay 3 for every burial, and score a secret colour Wager at double.

STATE (every item below must exist in the file):
  - each player: red_top (number, starts 0); everyone sees it. top value of the Red expedition (0 when empty)
  - each player: red_sum (number, starts 0); everyone sees it. sum of the Red expedition
  - each player: blue_top (number, starts 0); everyone sees it. top value of the Blue expedition (0 when empty)
  - each player: blue_sum (number, starts 0); everyone sees it. sum of the Blue expedition
  - each player: green_top (number, starts 0); everyone sees it. top value of the Green expedition (0 when empty)
  - each player: green_sum (number, starts 0); everyone sees it. sum of the Green expedition
  - each player: burial (number, starts 0); everyone sees it. Burial penalty, rising by 3 per buried card
  - each player: wager (text, starts ''); only its owner sees it. secret Wager colour (Red, Blue or Green), named in round 5 and revealed at the end
  - each player: choice (text, starts 'NONE'); everyone sees it. this round's pick: A, B or NONE (an already-taken card is recorded as NONE)
  - each player: score (number, starts 0); everyone sees it. final total, the sum of the three colour scores minus burial, computed after round 12
  - the table: deck (list, starts ['Red-2', 'Red-3', 'Red-4', 'Red-5', 'Red-6', 'Red-7', 'Red-8', 'Red-9', 'Red-10', 'Blue-2', 'Blue-3', 'Blue-4', 'Blue-5', 'Blue-6', 'Blue-7', 'Blue-8', 'Blue-9', 'Blue-10', 'Green-2', 'Green-3', 'Green-4', 'Green-5', 'Green-6', 'Green-7', 'Green-8', 'Green-9', 'Green-10']); hidden from all players. the shuffled face-down deck
  - the table: round (number, starts 0); everyone sees it. current round number, 1 to 12
  - the table: priority_seat (number, starts 1); everyone sees it. seat with priority this round: 1 in odd rounds, 2 in even rounds
  - the table: card_a_colour (text, starts ''); everyone sees it. colour of face-up Card A
  - the table: card_a_value (number, starts 0); everyone sees it. value of face-up Card A
  - the table: card_b_colour (text, starts ''); everyone sees it. colour of face-up Card B
  - the table: card_b_value (number, starts 0); everyone sees it. value of face-up Card B
  - the table: taken (text, starts 'NONE'); everyone sees it. which card the priority player took this round (A, B or NONE)
  - parameters, each kept as a table attribute: deck_size = 27, colours = 3, min_card_value = 2, max_card_value = 10, rounds = 12, row_size = 2, wager_round = 5, burial_penalty = 3, empty_wager_score = -15, empty_expedition_score = 0, base_offset = 10, wager_multiplier = 2, bonus_threshold = 25, bonus = 10, cards_left_unrevealed = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The table deck is filled with the 27 cards Red, Blue and Green 2 to 10 and shuffled once (cards are later drawn from it at random). Both players are told this composition.
  2. Each player's six expedition values (red_top, red_sum, blue_top, blue_sum, green_top, green_sum) and their burial start at 0, all public.
  3. Each player's wager starts empty and score starts at 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; priority_seat = 1 if round is odd, else 2; taken = NONE; every player's choice = NONE. Announce: 'Round {round}: seat {priority_seat} has priority.'
  2. [poll] all players answers: one of Red, Blue, Green. What happens: when round == 5: each player's wager = their answer. Nobody sees another's wager. This runs before Card A and Card B are revealed.
  3. [update] all players. What happens: Draw one card at random from deck and remove it: card_a_colour and card_a_value are set from it. Draw another and remove it: card_b_colour and card_b_value are set from it. Announce both cards to both players.
  4. [ask] seat {priority_seat} answers: one of A, B, NONE. What happens: the priority player's choice = answer; taken = answer. Both players are told what was chosen.
  5. [update] seat {priority_seat}. What happens: If choice is A or B, place that card (colour C, value v) for the priority player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game.
  6. [ask] the seat that is not priority_seat answers: one of A, B, NONE. What happens: choice = answer, except that choice = NONE if answer equals taken.
  7. [update] the seat that is not priority_seat. What happens: If choice is A or B, place that card (colour C, value v) for this player. If v > C_top: C_top = v and C_sum += v. Otherwise burial += 3 and the card is removed from the game.
  8. [update] all players. What happens: Any card in the row that nobody took is removed from the game. Announce both choices, where each card went (added or buried), every player's red/blue/green top and sum, and every player's burial.
  9. [update] all players. What happens: when round == 12: for each colour C, colour_score = (C_sum == 0 ? (wager == C ? -15 : 0) : (C_sum - 10) * (wager == C ? 2 : 1) + (C_sum >= 25 ? 10 : 0)); score = red score + blue score + green score - burial. Reveal each player's wager publicly and announce the totals. The 3 cards left in the deck are never revealed.
  10. [check] all players. What happens: end the game if round >= 12, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup the deck holds exactly 27 cards, Red, Blue and Green each valued 2 to 10, and every expedition top, sum and burial is 0.
  R2. When the round is odd, priority_seat is 1. When it is even, priority_seat is 2.
  R3. Each round, two cards are drawn from the deck as Card A and Card B and shown to both players, so the deck shrinks by 2 per round and holds 3 cards after round 12.
  R4. When round is 5, both players name a Wager of Red, Blue or Green simultaneously, before that round's cards are revealed. The Wager is never changed and stays hidden until the end.
  R5. The priority player chooses A, B or NONE first. The other player is then told that choice and chooses A, B or NONE.
  R6. When the second player names the card the priority player already took, their choice counts as NONE and they receive nothing.
  R7. When a player receives a card of colour C and value v, and v is greater than C_top, then C_top becomes v and C_sum rises by v (for example, Red 7 on an empty Red gives red_top 7 and red_sum 7).
  R8. When a player receives a card of colour C and value v, and v is not greater than C_top, the card is buried and that player's burial rises by 3 (for example, Red 5 on red_top 7 gives burial +3).
  R9. When a player chooses NONE, none of their attributes change.
  R10. Cards in the row that nobody took are removed from the game.
  R11. After each round, both choices, where each card went, all expedition tops and sums, and both burials are announced.
  R12. At final scoring, an empty expedition scores 0, unless it is in the player's Wager colour, in which case it scores -15.
  R13. At final scoring, a non-empty expedition's base is its sum minus 10 (for example, sum 18 gives base 8 and sum 6 gives base -4).
  R14. When the expedition is in the player's Wager colour, its base is doubled, negative or not (for example, sum 6 gives -8 and sum 18 gives 16).
  R15. When a non-empty expedition's sum is 25 or more, it gains 10 after any doubling (for example, a Wager-colour sum of 27 scores 2*17 + 10 = 44).
  R16. A player's score is the sum of their three colour scores minus their burial.
  R17. The game ends after round 12. Wagers are then revealed, the higher score wins, and equal scores are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Wager (round 5 only) | asked: both seats, simultaneously | options: Red, Blue, Green
  - Priority pick | asked: seat {priority_seat} | options: A, B, NONE
  - Second pick | asked: the non-priority seat | options: A, B, NONE (naming the card already taken is accepted but counts as NONE)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final total (the three colour scores minus the Burial penalty). The higher total wins, and equal totals share the win, which is a draw.
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

- each player: `red_top` (number, visible: public, starts 0): top value of the Red expedition (0 when empty)
- each player: `red_sum` (number, visible: public, starts 0): sum of the Red expedition
- each player: `blue_top` (number, visible: public, starts 0): top value of the Blue expedition (0 when empty)
- each player: `blue_sum` (number, visible: public, starts 0): sum of the Blue expedition
- each player: `green_top` (number, visible: public, starts 0): top value of the Green expedition (0 when empty)
- each player: `green_sum` (number, visible: public, starts 0): sum of the Green expedition
- each player: `burial` (number, visible: public, starts 0): Burial penalty, rising by 3 per buried card
- each player: `score` (number, visible: public, starts 0): final total, the sum of the three colour scores minus burial, computed after round 12
- the table: `round` (number, visible: public, starts 0): current round number, 1 to 12
- the table: `priority_seat` (number, visible: public, starts 1): seat with priority this round: 1 in odd rounds, 2 in even rounds
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 27, colours = 3, min_card_value = 2, max_card_value = 10, rounds = 12, row_size = 2, wager_round = 5, burial_penalty = 3, empty_wager_score = -15, empty_expedition_score = 0, base_offset = 10, wager_multiplier = 2, bonus_threshold = 25, bonus = 10, cards_left_unrevealed = 3
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
    "id": "lost_cities_wager_draft",
    "name": "Lost Cities: Wager Draft",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Draft face-up cards over 12 rounds, build rising expeditions in three colours, pay for every burial, and score a secret colour Wager at double."
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
        "key": "red_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "burial",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wager",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "choice",
        "visible": "public",
        "type": "text",
        "initial": "NONE"
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red-2",
          "Red-3",
          "Red-4",
          "Red-5",
          "Red-6",
          "Red-7",
          "Red-8",
          "Red-9",
          "Red-10",
          "Blue-2",
          "Blue-3",
          "Blue-4",
          "Blue-5",
          "Blue-6",
          "Blue-7",
          "Blue-8",
          "Blue-9",
          "Blue-10",
          "Green-2",
          "Green-3",
          "Green-4",
          "Green-5",
          "Green-6",
          "Green-7",
          "Green-8",
          "Green-9",
          "Green-10"
        ]
      },
      {
        "key": "card_table",
        "visible": "none",
        "type": "list",
        "initial": [
          ["Red-2", "Red", 2],
          ["Red-3", "Red", 3],
          ["Red-4", "Red", 4],
          ["Red-5", "Red", 5],
          ["Red-6", "Red", 6],
          ["Red-7", "Red", 7],
          ["Red-8", "Red", 8],
          ["Red-9", "Red", 9],
          ["Red-10", "Red", 10],
          ["Blue-2", "Blue", 2],
          ["Blue-3", "Blue", 3],
          ["Blue-4", "Blue", 4],
          ["Blue-5", "Blue", 5],
          ["Blue-6", "Blue", 6],
          ["Blue-7", "Blue", 7],
          ["Blue-8", "Blue", 8],
          ["Blue-9", "Blue", 9],
          ["Blue-10", "Blue", 10],
          ["Green-2", "Green", 2],
          ["Green-3", "Green", 3],
          ["Green-4", "Green", 4],
          ["Green-5", "Green", 5],
          ["Green-6", "Green", 6],
          ["Green-7", "Green", 7],
          ["Green-8", "Green", 8],
          ["Green-9", "Green", 9],
          ["Green-10", "Green", 10]
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_a_colour",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_a_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_b_colour",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_b_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "text",
        "initial": "NONE"
      },
      {
        "key": "second_choice",
        "visible": "none",
        "type": "text",
        "initial": "NONE"
      },
      {
        "key": "place_colour",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "place_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_top",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fate_first",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "fate_second",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_card_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_card_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "row_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "wager_round",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "burial_penalty",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "empty_wager_score",
        "visible": "public",
        "type": "number",
        "initial": -15
      },
      {
        "key": "empty_expedition_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "base_offset",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "wager_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bonus_threshold",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "cards_left_unrevealed",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deck and expeditions",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[e[0] for e in card_table]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "burial",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wager",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        }
      ],
      "text": "The deck of {deck_size} cards (Red, Blue and Green, each valued {min_card_value} to {max_card_value}) is shuffled face down. All expeditions start empty and every Burial penalty is 0."
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
      "use": "update",
      "phase": "start",
      "label": "the round begins",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "1 if round - 2 * int(round / 2) == 1 else 2"
            }
          }
        },
        {
          "set": {
            "key": "taken",
            "value": "NONE"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": "NONE"
          }
        }
      ],
      "text": "Round {round}: seat {priority_seat} has priority."
    },
    {
      "use": "poll",
      "phase": "wager",
      "label": "the wager",
      "when": {
        "calc": "round == wager_round"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red",
          "Blue",
          "Green"
        ]
      },
      "store": "wager",
      "text": "Name your secret Wager colour: Red, Blue or Green. It cannot be changed and stays hidden until the end. At final scoring your expedition in this colour has its base doubled (negative too), and if it is empty it scores {empty_wager_score}."
    },
    {
      "use": "update",
      "phase": "row",
      "label": "the row is turned up",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "set": {
            "key": "card_a_colour",
            "value": {
              "calc": "[e[1] for e in card_table if e[0] == pick][0]"
            }
          }
        },
        {
          "set": {
            "key": "card_a_value",
            "value": {
              "calc": "[e[2] for e in card_table if e[0] == pick][0]"
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
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "set": {
            "key": "card_b_colour",
            "value": {
              "calc": "[e[1] for e in card_table if e[0] == pick][0]"
            }
          }
        },
        {
          "set": {
            "key": "card_b_value",
            "value": {
              "calc": "[e[2] for e in card_table if e[0] == pick][0]"
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
      "text": "Round {round} row: Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}."
    },
    {
      "use": "ask",
      "phase": "draft",
      "label": "priority pick",
      "to": {
        "where": "you.seat == priority_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B",
          "NONE"
        ]
      },
      "store": "choice",
      "verify": {
        "bind": "p1pick"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (priority) chose {value}."
      },
      "text": "You have priority. Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}. Choose A, B or NONE. A card you take must be placed: if its value is higher than the top of your expedition in its colour it is added, otherwise it is buried and your Burial penalty rises by {burial_penalty}."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "priority placement",
      "do": [
        {
          "set": {
            "key": "taken",
            "value": "$p1pick"
          }
        },
        {
          "set": {
            "key": "place_colour",
            "value": {
              "calc": "card_a_colour if taken == 'A' else (card_b_colour if taken == 'B' else '')"
            }
          }
        },
        {
          "set": {
            "key": "place_value",
            "value": {
              "calc": "card_a_value if taken == 'A' else (card_b_value if taken == 'B' else 0)"
            }
          }
        },
        {
          "set": {
            "key": "place_top",
            "value": {
              "calc": "[(p.red_top if place_colour == 'Red' else (p.blue_top if place_colour == 'Blue' else p.green_top)) for p in players if p.seat == priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "fate_first",
            "value": {
              "calc": "'nothing taken' if taken == 'NONE' else ('added' if place_value > place_top else 'buried')"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "burial",
            "value": {
              "calc": "burial_penalty"
            },
            "if": {
              "calc": "fate_first == 'buried'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "red_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "red_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "blue_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "blue_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "green_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Green'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "green_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Green'"
            }
          }
        }
      ],
      "text": "Seat {priority_seat} chose {taken}: {fate_first}."
    },
    {
      "use": "ask",
      "phase": "draft",
      "label": "second pick",
      "to": {
        "where": "you.seat != priority_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B",
          "NONE"
        ]
      },
      "store": "choice",
      "verify": {
        "bind": "p2pick"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chose {value}."
      },
      "text": "Seat {priority_seat} had priority and chose {taken}. Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}. Choose A, B or NONE. Naming the card already taken counts as NONE and you receive nothing. A card you take must be placed: if its value is higher than the top of your expedition in its colour it is added, otherwise it is buried and your Burial penalty rises by {burial_penalty}."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "second placement",
      "do": [
        {
          "set": {
            "key": "second_choice",
            "value": {
              "calc": "[p.choice for p in players if p.seat != priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "second_choice",
            "value": {
              "calc": "'NONE' if second_choice == taken else second_choice"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "choice",
            "value": {
              "calc": "second_choice"
            }
          }
        },
        {
          "set": {
            "key": "place_colour",
            "value": {
              "calc": "card_a_colour if second_choice == 'A' else (card_b_colour if second_choice == 'B' else '')"
            }
          }
        },
        {
          "set": {
            "key": "place_value",
            "value": {
              "calc": "card_a_value if second_choice == 'A' else (card_b_value if second_choice == 'B' else 0)"
            }
          }
        },
        {
          "set": {
            "key": "place_top",
            "value": {
              "calc": "[(p.red_top if place_colour == 'Red' else (p.blue_top if place_colour == 'Blue' else p.green_top)) for p in players if p.seat != priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "fate_second",
            "value": {
              "calc": "'nothing taken' if second_choice == 'NONE' else ('added' if place_value > place_top else 'buried')"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "burial",
            "value": {
              "calc": "burial_penalty"
            },
            "if": {
              "calc": "fate_second == 'buried'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "red_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "red_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "blue_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "blue_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "green_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Green'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "green_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Green'"
            }
          }
        }
      ],
      "text": "The other player's pick counts as {second_choice}: {fate_second}."
    },
    {
      "use": "update",
      "phase": "report",
      "label": "the round report",
      "do": [],
      "text": "Round {round} summary. Priority seat {priority_seat} chose {taken} ({fate_first}); the other seat's pick counted as {second_choice} ({fate_second}). Cards nobody took are removed from the game. Seat 1: Red top {players[0].red_top} sum {players[0].red_sum}, Blue top {players[0].blue_top} sum {players[0].blue_sum}, Green top {players[0].green_top} sum {players[0].green_sum}, Burial {players[0].burial}. Seat 2: Red top {players[1].red_top} sum {players[1].red_sum}, Blue top {players[1].blue_top} sum {players[1].blue_sum}, Green top {players[1].green_top} sum {players[1].green_sum}, Burial {players[1].burial}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "((empty_wager_score if you.wager == 'Red' else empty_expedition_score) if you.red_sum == 0 else (you.red_sum - base_offset) * (wager_multiplier if you.wager == 'Red' else 1) + (bonus if you.red_sum >= bonus_threshold else 0)) + ((empty_wager_score if you.wager == 'Blue' else empty_expedition_score) if you.blue_sum == 0 else (you.blue_sum - base_offset) * (wager_multiplier if you.wager == 'Blue' else 1) + (bonus if you.blue_sum >= bonus_threshold else 0)) + ((empty_wager_score if you.wager == 'Green' else empty_expedition_score) if you.green_sum == 0 else (you.green_sum - base_offset) * (wager_multiplier if you.wager == 'Green' else 1) + (bonus if you.green_sum >= bonus_threshold else 0)) - you.burial"
            }
          }
        },
        {
          "disclose": {
            "attribute": "wager",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s Wager was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "wager",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s Wager was {value}."
          }
        }
      ],
      "text": "Final totals: seat 1 {players[0].score}, seat 2 {players[1].score}. The {cards_left_unrevealed} cards left in the deck are never revealed."
    },
    {
      "use": "check",
      "phase": "scoring
... (cut)

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (wager, card_a_colour, card_b_colour, fate_first); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "lost_cities_wager_draft",
    "name": "Lost Cities: Wager Draft",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Draft face-up cards over 12 rounds, build rising expeditions in three colours, pay for every burial, and score a secret colour Wager at double."
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
        "key": "red_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "red_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "blue_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_top",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "green_sum",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "burial",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wager",
        "visible": "ally",
        "type": "text",
        "initial": "not yet named"
      },
      {
        "key": "choice",
        "visible": "public",
        "type": "text",
        "initial": "NONE"
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
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red-2",
          "Red-3",
          "Red-4",
          "Red-5",
          "Red-6",
          "Red-7",
          "Red-8",
          "Red-9",
          "Red-10",
          "Blue-2",
          "Blue-3",
          "Blue-4",
          "Blue-5",
          "Blue-6",
          "Blue-7",
          "Blue-8",
          "Blue-9",
          "Blue-10",
          "Green-2",
          "Green-3",
          "Green-4",
          "Green-5",
          "Green-6",
          "Green-7",
          "Green-8",
          "Green-9",
          "Green-10"
        ]
      },
      {
        "key": "card_table",
        "visible": "none",
        "type": "list",
        "initial": [
          ["Red-2", "Red", 2],
          ["Red-3", "Red", 3],
          ["Red-4", "Red", 4],
          ["Red-5", "Red", 5],
          ["Red-6", "Red", 6],
          ["Red-7", "Red", 7],
          ["Red-8", "Red", 8],
          ["Red-9", "Red", 9],
          ["Red-10", "Red", 10],
          ["Blue-2", "Blue", 2],
          ["Blue-3", "Blue", 3],
          ["Blue-4", "Blue", 4],
          ["Blue-5", "Blue", 5],
          ["Blue-6", "Blue", 6],
          ["Blue-7", "Blue", 7],
          ["Blue-8", "Blue", 8],
          ["Blue-9", "Blue", 9],
          ["Blue-10", "Blue", 10],
          ["Green-2", "Green", 2],
          ["Green-3", "Green", 3],
          ["Green-4", "Green", 4],
          ["Green-5", "Green", 5],
          ["Green-6", "Green", 6],
          ["Green-7", "Green", 7],
          ["Green-8", "Green", 8],
          ["Green-9", "Green", 9],
          ["Green-10", "Green", 10]
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "priority_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "card_a_colour",
        "visible": "public",
        "type": "text",
        "initial": "none yet"
      },
      {
        "key": "card_a_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_b_colour",
        "visible": "public",
        "type": "text",
        "initial": "none yet"
      },
      {
        "key": "card_b_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "text",
        "initial": "NONE"
      },
      {
        "key": "second_choice",
        "visible": "none",
        "type": "text",
        "initial": "NONE"
      },
      {
        "key": "place_colour",
        "visible": "none",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "place_value",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "place_top",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "fate_first",
        "visible": "none",
        "type": "text",
        "initial": "nothing taken"
      },
      {
        "key": "fate_second",
        "visible": "none",
        "type": "text",
        "initial": "nothing taken"
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 27
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "min_card_value",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_card_value",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "row_size",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "wager_round",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "burial_penalty",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "empty_wager_score",
        "visible": "public",
        "type": "number",
        "initial": -15
      },
      {
        "key": "empty_expedition_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "base_offset",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "wager_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bonus_threshold",
        "visible": "public",
        "type": "number",
        "initial": 25
      },
      {
        "key": "bonus",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "cards_left_unrevealed",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the deck and expeditions",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "[e[0] for e in card_table]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "red_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "blue_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green_top",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "green_sum",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "burial",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "wager",
            "value": "not yet named"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": 0
          }
        }
      ],
      "text": "The deck of {deck_size} cards (Red, Blue and Green, each with one card of every value from {min_card_value} to {max_card_value}) is shuffled face down. All expeditions start empty and every Burial penalty is 0."
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
      "use": "update",
      "phase": "start",
      "label": "the round begins",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "priority_seat",
            "value": {
              "calc": "1 if round - 2 * int(round / 2) == 1 else 2"
            }
          }
        },
        {
          "set": {
            "key": "taken",
            "value": "NONE"
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": "NONE"
          }
        }
      ],
      "text": "Round {round}: seat {priority_seat} has priority."
    },
    {
      "use": "poll",
      "phase": "wager",
      "label": "the wager",
      "when": {
        "calc": "round == wager_round"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red",
          "Blue",
          "Green"
        ]
      },
      "store": "wager",
      "text": "Name your secret Wager colour: Red, Blue or Green. It cannot be changed and stays hidden until the end. At final scoring your expedition in this colour has its base doubled (negative too), and if it is empty it scores {empty_wager_score}."
    },
    {
      "use": "update",
      "phase": "row",
      "label": "the row is turned up",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "set": {
            "key": "card_a_colour",
            "value": {
              "calc": "[e[1] for e in card_table if e[0] == pick][0]"
            }
          }
        },
        {
          "set": {
            "key": "card_a_value",
            "value": {
              "calc": "[e[2] for e in card_table if e[0] == pick][0]"
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
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[min(len(deck) - 1, int(uniform(0, len(deck))))]"
            }
          }
        },
        {
          "set": {
            "key": "card_b_colour",
            "value": {
              "calc": "[e[1] for e in card_table if e[0] == pick][0]"
            }
          }
        },
        {
          "set": {
            "key": "card_b_value",
            "value": {
              "calc": "[e[2] for e in card_table if e[0] == pick][0]"
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
      "text": "Round {round} row: Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}."
    },
    {
      "use": "ask",
      "phase": "draft",
      "label": "priority pick",
      "to": {
        "where": "you.seat == priority_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B",
          "NONE"
        ]
      },
      "store": "choice",
      "verify": {
        "bind": "p1pick"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} (priority) chose {value}."
      },
      "text": "You have priority. Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}. Choose A, B or NONE. A card you take must be placed: if its value is higher than the top of your expedition in its colour it is added, otherwise it is buried and your Burial penalty rises by {burial_penalty}."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "priority placement",
      "do": [
        {
          "set": {
            "key": "taken",
            "value": "$p1pick"
          }
        },
        {
          "set": {
            "key": "place_colour",
            "value": {
              "calc": "card_a_colour if taken == 'A' else (card_b_colour if taken == 'B' else 'none')"
            }
          }
        },
        {
          "set": {
            "key": "place_value",
            "value": {
              "calc": "card_a_value if taken == 'A' else (card_b_value if taken == 'B' else 0)"
            }
          }
        },
        {
          "set": {
            "key": "place_top",
            "value": {
              "calc": "[(p.red_top if place_colour == 'Red' else (p.blue_top if place_colour == 'Blue' else p.green_top)) for p in players if p.seat == priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "fate_first",
            "value": {
              "calc": "'nothing taken' if taken == 'NONE' else ('added' if place_value > place_top else 'buried')"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "burial",
            "value": {
              "calc": "burial_penalty"
            },
            "if": {
              "calc": "fate_first == 'buried'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "red_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "red_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "blue_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "blue_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "green_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Green'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == priority_seat"
            },
            "key": "green_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_first == 'added' and place_colour == 'Green'"
            }
          }
        }
      ],
      "text": "Seat {priority_seat} chose {taken}: {fate_first}."
    },
    {
      "use": "ask",
      "phase": "draft",
      "label": "second pick",
      "to": {
        "where": "you.seat != priority_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "A",
          "B",
          "NONE"
        ]
      },
      "store": "choice",
      "verify": {
        "bind": "p2pick"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chose {value}."
      },
      "text": "Seat {priority_seat} had priority and chose {taken}. Card A is {card_a_colour} {card_a_value}; Card B is {card_b_colour} {card_b_value}. Choose A, B or NONE. Naming the card already taken counts as NONE and you receive nothing. A card you take must be placed: if its value is higher than the top of your expedition in its colour it is added, otherwise it is buried and your Burial penalty rises by {burial_penalty}."
    },
    {
      "use": "update",
      "phase": "draft",
      "label": "second placement",
      "do": [
        {
          "set": {
            "key": "second_choice",
            "value": {
              "calc": "[p.choice for p in players if p.seat != priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "second_choice",
            "value": {
              "calc": "'NONE' if second_choice == taken else second_choice"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "choice",
            "value": {
              "calc": "second_choice"
            }
          }
        },
        {
          "set": {
            "key": "place_colour",
            "value": {
              "calc": "card_a_colour if second_choice == 'A' else (card_b_colour if second_choice == 'B' else 'none')"
            }
          }
        },
        {
          "set": {
            "key": "place_value",
            "value": {
              "calc": "card_a_value if second_choice == 'A' else (card_b_value if second_choice == 'B' else 0)"
            }
          }
        },
        {
          "set": {
            "key": "place_top",
            "value": {
              "calc": "[(p.red_top if place_colour == 'Red' else (p.blue_top if place_colour == 'Blue' else p.green_top)) for p in players if p.seat != priority_seat][0]"
            }
          }
        },
        {
          "set": {
            "key": "fate_second",
            "value": {
              "calc": "'nothing taken' if second_choice == 'NONE' else ('added' if place_value > place_top else 'buried')"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "burial",
            "value": {
              "calc": "burial_penalty"
            },
            "if": {
              "calc": "fate_second == 'buried'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "red_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "red_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "blue_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "blue_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "green_sum",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Green'"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat != priority_seat"
            },
            "key": "green_top",
            "value": {
              "calc": "place_value"
            },
            "if": {
              "calc": "fate_second == 'added' and place_colour == 'Green'"
            }
          }
        }
      ],
      "text": "The other player's pick counts as {second_choice}: {fate_second}."
    },
    {
      "use": "update",
      "phase": "report",
      "label": "the round report",
      "do": [],
      "text": "Round {round} summary. Priority seat {priority_seat} chose {taken} ({fate_first}); the other seat's pick counted as {second_choice} ({fate_second}). Cards nobody took are removed from the game. Seat 1: Red top {players[0].red_top} sum {players[0].red_sum}, Blue top {players[0].blue_top} sum {players[0].blue_sum}, Green top {players[0].green_top} sum {players[0].green_sum}, Burial {players[0].burial}. Seat 2: Red top {players[1].red_top} sum {players[1].red_sum}, Blue top {players[1].blue_top} sum {players[1].blue_sum}, Green top {players[1].green_top} sum {players[1].green_sum}, Burial {players[1].burial}."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "final scoring",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "((empty_wager_score if you.wager == 'Red' else empty_expedition_score) if you.red_sum == 0 else (you.red_sum - base_offset) * (wager_multiplier if you.wager == 'Red' else 1) + (bonus if you.red_sum >= bonus_threshold else 0)) + ((empty_wager_score if you.wager == 'Blue' else empty_expedition_score) if you.blue_sum == 0 else (you.blue_sum - base_offset) * (wager_multiplier if you.wager == 'Blue' else 1) + (bonus if you.blue_sum >= bonus_threshold else 0)) + ((empty_wager_score if you.wager == 'Green' else empty_expedition_score) if you.green_sum == 0 else (you.green_sum - base_offset) * (wager_multiplier if you.wager == 'Green' else 1) + (bonus if you.green_sum >= bonus_threshold else 0)) - you.burial"
            }
          }
        },
        {
          "disclose": {
            "attribute": "wager",
            "of": 1,
            "to": "all",
            "text": "Seat {subject}'s Wager was {value}."
          }
        },
        {
          "disclose": {
            "attribute": "wager",
            "of": 2,
            "to": "all",
            "text": "Seat {subject}'s Wager was {value}."
          }
        }
      ],
      "text": "Final totals: seat 1 {players[0].score}, seat 2 {players[1].score}. The {cards_left_unrevealed} cards left in the deck are never revealed."
    },
    {
      "use": "check",
      "phase": "scoring",
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
        "wager"
      ],
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "The deck has {deck_size} cards: Red, Blue and Green, each with one card of every value from {min_card_value} to {max_card_value}. It is shuffled once, face down. Each player has three expeditions, one per colour, each starting empty and tracked by its top value (0 when empty) and its sum. Each player also has a Burial penalty starting at 0. All of these are public.\n\nThe game lasts {rounds} rounds. Priority belongs to seat 1 in odd rounds and to seat 2 in even rounds; this is announced.\n\nWAGER: at the start of round {wager_round} only, before that round's cards are revealed, both players secretly and at the same moment name one colour: Red, Blue or Green. This is their Wager. It cannot be changed and stays hidden until the end.\n\nEach round the top {row_size} cards of the deck are turned face up as Card A and Card B, and their colours and values are shown to both players. The priority player chooses A, B or NONE. If they chose a card, they receive it and place it. The other player is told what was chosen, then chooses A, B or NONE. Naming the card already taken counts as NONE and that player receives nothing. If they chose a card, they receive it and place it. Choosing NONE changes nothing for that player.\n\nPlacement is mandatory. If the card's value is higher than the top value of that player's expedition in its colour (any card beats an empty expedition), it is added: its value is added to the sum and it becomes the new top value. Otherwise the card is buried: it is removed from the game and that player's Burial penalty rises by {burial_penalty}.\n\nCards in the row that no one took are removed from the game. Both choices, where each card went, and all expedition states and Burial penalties are announced. After round {rounds}, the {cards_left_unrevealed} cards left in the deck are never revealed.\n\nFINAL SCORING, for each player and each colour: an empty expedition scores {empty_expedition_score}; however, if the empty expedition is in the player's Wager colour, it scores {empty_wager_score}. Otherwise the base is the sum minus {base_offset}. If the colour is the player's Wager colour, the base is multiplied by {wager_multiplier}; negative bases are doubled too. Add {bonus} if the expedition's sum is {bonus_threshold} or more. A player's total is the sum of their three colour scores minus their Burial penalty. Wagers are revealed and the totals are compared: the higher total wins, and equal totals are a draw (a shared win)."
}
```
````
