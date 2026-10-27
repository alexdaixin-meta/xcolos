# Task: write the XColos game file for "Secret Slice"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- There are 3 players, seated P1, P2, P3.
- The deck has 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy. It is shuffled once and split into 6 rows of 6.
- Each player is privately dealt one favourite topping, drawn without replacement from {Cheese, Mushroom, Pepperoni, Anchovy}. The three favourites are therefore all different, and one topping is nobody's favourite.
- Favourites stay secret until final scoring.

ROUNDS
The game has 6 rounds. The Slicer is P1 in round 1, then P2, P3, P1, P2, P3.

In each round:
1. Reveal. The next row of 6 slices is revealed, with positions numbered 1 to 6.
2. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Messages are not binding.
3. Cut. The Slicer states two whole numbers c1 and c2 with 1 <= c1 < c2 <= 5.
   - Portion A is positions 1 to c1.
   - Portion B is positions c1+1 to c2.
   - Portion C is positions c2+1 to 6.
   - In the same answer, the Slicer declares 'eat' or 'collect'. This applies to the pepperoni in whichever portion the Slicer ends up with.
   - The three portions are announced.
4. First pick. The player after the Slicer (P1→P2→P3→P1) chooses one portion and declares 'eat' or 'collect'.
5. Second pick. The remaining non-Slicer player chooses one of the two remaining portions and declares 'eat' or 'collect'.
6. Slicer. The Slicer takes the last portion, with the 'eat' or 'collect' declared at the cut.

EAT OR COLLECT
When a player takes a portion:
- With 'eat', each Pepperoni slice in it is eaten for +1 point and does not count as collected.
- With 'collect', every slice in the portion is collected.
- Non-pepperoni slices are always collected.

FINAL SCORING (after round 6)
Scoring uses only collected slices, plus eaten pepperoni and anchovy penalties.
- Majority: the player with strictly the most collected slices of a type scores Cheese 7, Mushroom 7, Pepperoni 5, Anchovy 10. If there is a tie for most, nobody scores that type.
- Eaten pepperoni: +1 per eaten Pepperoni slice.
- Anchovy penalty: -1 per collected Anchovy slice.
- Favourite: +1 per collected slice of your own favourite type. Eaten slices do not count.

The totals are announced.

How the winner is decided: The player with the highest final total wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Secret Slice (3 to 3 players, best with 3)

Three players take turns cutting a row of six pizza slices into three portions. The others pick first and the cutter gets the last portion. Each player chooses whether to eat pepperoni for points or collect it toward majorities, while chasing a secret favourite topping.

STATE (every item below must exist in the file):
  - each player: favourite (text, starts ''); only its owner sees it. secret favourite topping: Cheese, Mushroom, Pepperoni or Anchovy; revealed at final scoring
  - each player: cheese (number, starts 0); everyone sees it. collected Cheese slices
  - each player: mushroom (number, starts 0); everyone sees it. collected Mushroom slices
  - each player: pepperoni (number, starts 0); everyone sees it. collected Pepperoni slices
  - each player: anchovy (number, starts 0); everyone sees it. collected Anchovy slices
  - each player: eaten (number, starts 0); everyone sees it. eaten Pepperoni slices
  - each player: score (number, starts 0); everyone sees it. final total, computed after round 6
  - the table: deck (list, starts '9 x Cheese, 9 x Mushroom, 9 x Pepperoni, 9 x Anchovy'); hidden from all players. the undealt slices; each row is drawn from it at random
  - the table: toppings (list, starts ['Cheese', 'Mushroom', 'Pepperoni', 'Anchovy']); hidden from all players. favourites still undealt; one is left over and is nobody's favourite
  - the table: round (number, starts 0); everyone sees it. current round, 1 to 6
  - the table: slicer (number, starts 0); everyone sees it. seat of this round's Slicer
  - the table: first_picker (number, starts 0); everyone sees it. seat after the Slicer
  - the table: second_picker (number, starts 0); everyone sees it. remaining non-Slicer seat
  - the table: row (list, starts []); everyone sees it. this round's 6 slices, positions 1 to 6 in order
  - the table: c1 (number, starts 0); everyone sees it. first cut
  - the table: c2 (number, starts 0); everyone sees it. second cut
  - the table: slicer_mode (text, starts ''); everyone sees it. eat or collect, declared by the Slicer at the cut
  - the table: portion_a (list, starts []); everyone sees it. positions 1..c1
  - the table: portion_b (list, starts []); everyone sees it. positions c1+1..c2
  - the table: portion_c (list, starts []); everyone sees it. positions c2+1..6
  - the table: taken (list, starts []); everyone sees it. portions already picked this round (A, B, C)
  - parameters, each kept as a table attribute: player_count = 3, slices_per_type = 9, deck_size = 36, rows = 6, row_size = 6, rounds = 6, cut_min = 1, cut_max = 5, majority_cheese = 7, majority_mushroom = 7, majority_pepperoni = 5, majority_anchovy = 10, eaten_pepperoni_point = 1, anchovy_penalty = 1, favourite_bonus = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are P1, P2, P3.
  2. The deck list is filled with 9 Cheese, 9 Mushroom, 9 Pepperoni and 9 Anchovy.
  3. Each player is dealt a favourite at random from the toppings list, which is removed from that list (without replacement), so the three favourites differ and one topping is nobody's favourite.
  4. Each player is synced their own favourite, kept secret (ally) until final scoring.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; slicer = ((round-1) mod 3) + 1; first_picker = (slicer mod 3) + 1; second_picker = (first_picker mod 3) + 1; taken = []
  2. [update] all players. What happens: row = []; 6 times: draw one slice at random from deck, append it to row, remove it from deck. Announce the row with positions 1 to 6 and who is Slicer, first picker and second picker.
  3. [poll] all players answers: short text message. What happens: Nothing changes; all messages are broadcast at once: {"to": "all", "text": "Seat {seat} says: {value}"}
  4. [ask] seat slicer answers: one choice 'c1-c2 mode' with 1 <= c1 < c2 <= 5 and mode eat or collect (20 options). What happens: set c1, c2, slicer_mode; portion_a = row[1..c1]; portion_b = row[c1+1..c2]; portion_c = row[c2+1..6]; announce the three portions
  5. [ask] seat first_picker answers: one of: A eat, A collect, B eat, B collect, C eat, C collect. What happens: the picker adds the chosen portion's Cheese to cheese, Mushroom to mushroom and Anchovy to anchovy; its Pepperoni goes to eaten if eat, or to pepperoni if collect; append the letter to taken; announce
  6. [ask] seat second_picker answers: one of the two portions not in taken, each with eat or collect (4 options). What happens: same accounting as the first pick for the second picker; append the letter to taken; announce
  7. [update] seat slicer. What happens: the Slicer takes the portion not in taken, with slicer_mode: Cheese to cheese, Mushroom to mushroom, Anchovy to anchovy, Pepperoni to eaten if slicer_mode = eat, otherwise to pepperoni; announce
  8. [update] all players. What happens: when round = 6: for each player, score = 7 if cheese is strictly greater than both other players' cheese + 7 if mushroom is strictly greater than both others' + 5 if pepperoni is strictly greater than both others' + 10 if anchovy is strictly greater than both others' + eaten - anchovy + the collected count of their own favourite (cheese, mushroom, pepperoni or anchovy). Reveal every favourite and announce all totals.
  9. [check] all players. What happens: end the game if round >= 6, otherwise continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, the deck holds 36 slices: 9 Cheese, 9 Mushroom, 9 Pepperoni, 9 Anchovy.
  R2. At setup, each of the 3 players gets a different favourite from {Cheese, Mushroom, Pepperoni, Anchovy}, visible only to its owner until final scoring.
  R3. In each round, 6 slices are drawn from the deck into the row, so after round r the deck holds 36 - 6r slices.
  R4. The Slicer is P1 in rounds 1 and 4, P2 in rounds 2 and 5, and P3 in rounds 3 and 6.
  R5. The first picker is the seat after the Slicer (P1 to P2, P2 to P3, P3 to P1), and the second picker is the remaining seat.
  R6. Each round, every player sends one text message in a simultaneous poll, and all messages are shown together; messages change no state.
  R7. The Slicer chooses c1 and c2 with 1 <= c1 < c2 <= 5, plus eat or collect, in one answer; for example 2-4 gives A = positions 1-2, B = 3-4, C = 5-6.
  R8. The first picker may choose any of A, B or C with eat or collect; the second picker may choose only one of the two portions left.
  R9. The Slicer receives the last remaining portion, using the mode declared at the cut.
  R10. When a portion is taken with eat, each Pepperoni in it adds 1 to eaten and nothing to pepperoni.
  R11. When a portion is taken with collect, each Pepperoni in it adds 1 to pepperoni.
  R12. Cheese, Mushroom and Anchovy slices in a taken portion are always added to cheese, mushroom and anchovy, whichever mode is declared.
  R13. At final scoring, a player with strictly the most collected Cheese scores 7, Mushroom 7, Pepperoni 5, Anchovy 10; if the most is tied, nobody scores that type.
  R14. At final scoring, each eaten Pepperoni is worth +1.
  R15. At final scoring, each collected Anchovy is worth -1.
  R16. At final scoring, each collected slice of your own favourite type is worth +1; eaten slices do not count.
  R17. The game ends after round 6; the highest score wins, and tied top scores share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk | asked: all players | options: a short free-text message
  - Cut | asked: the Slicer | options: 1-2 eat, 1-2 collect, 1-3 eat, 1-3 collect, 1-4 eat, 1-4 collect, 1-5 eat, 1-5 collect, 2-3 eat, 2-3 collect, 2-4 eat, 2-4 collect, 2-5 eat, 2-5 collect, 3-4 eat, 3-4 collect, 3-5 eat, 3-5 collect, 4-5 eat, 4-5 collect
  - First pick | asked: the seat after the Slicer | options: A eat, A collect, B eat, B collect, C eat, C collect
  - Second pick | asked: the remaining non-Slicer seat | options: the two portions not taken by the first picker, each with eat or collect (e.g. after A is taken: B eat, B collect, C eat, C collect)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 6
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final total; the highest total wins, and players tied for the highest share the win (the source calls this a draw).
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

- each player: `favourite` (text, visible: ally, starts ''): secret favourite topping: Cheese, Mushroom, Pepperoni or Anchovy; revealed at final scoring
- each player: `cheese` (number, visible: public, starts 0): collected Cheese slices
- each player: `mushroom` (number, visible: public, starts 0): collected Mushroom slices
- each player: `pepperoni` (number, visible: public, starts 0): collected Pepperoni slices
- each player: `anchovy` (number, visible: public, starts 0): collected Anchovy slices
- each player: `eaten` (number, visible: public, starts 0): eaten Pepperoni slices
- each player: `score` (number, visible: public, starts 0): final total, computed after round 6
- the table: `round` (number, visible: public, starts 0): current round, 1 to 6
- parameters (each must be an attribute holding this value, never a number buried in a step): player_count = 3, slices_per_type = 9, deck_size = 36, rows = 6, row_size = 6, rounds = 6, cut_min = 1, cut_max = 5, majority_cheese = 7, majority_mushroom = 7, majority_pepperoni = 5, majority_anchovy = 10, eaten_pepperoni_point = 1, anchovy_penalty = 1, favourite_bonus = 1
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
