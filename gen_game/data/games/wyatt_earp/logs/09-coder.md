# 09 coder

- time: 2026-10-28T04:15:17+00:00 (63.8s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 f059954870a401d7, reply sha256 9f2998d2ac664337

## Sent

````
# Task: write the XColos game file for "Wanted: Dead or Alive (Majority Rule)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

OUTLAWS: There are five outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at $2,000.

SETUP: Each player receives 12 deputies, which must last the whole game, and $0. Each player is secretly assigned one informant outlaw at random, with no two players sharing one. Only that player knows it. The informant outlaw carries a hidden tip of $3,000, added to its poster at the end of the game. Outlaws that are nobody's informant carry no tip. Each player has a public deputy count on each outlaw, starting at 0. The game lasts 6 rounds.

EACH ROUND:
1. Sighting: one outlaw is drawn uniformly at random from all five (with replacement; the same outlaw may be sighted in several rounds). It is announced, and its poster rises by $1,000.
2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.
3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from 0 to 4. If the number exceeds their remaining deputies, it is reduced to their remaining deputies.
4. Reveal: all choices are announced.
5. Resolution: each player's remaining deputies fall by the number they committed, and their deputy count on the chosen outlaw rises by that number. Commitments do not change posters.

END OF GAME (after round 6):
- All informants are revealed. Each informant outlaw's poster rises by $3,000.
- For each outlaw: if no player has any deputies on it, it escapes and pays nobody. Otherwise the player with the highest deputy count on it receives its whole poster. If several players tie for the highest count, the poster is split equally among them, rounded down to the dollar.
- Unused deputies are worth nothing.
- Each player's money is the sum of their payouts.

How the winner is decided: The player with the most money after the final payout wins. If two or more players tie for the most money, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Wanted: Dead or Alive (Majority Rule) (3 to 4 players, best with 3)

Over 6 rounds, players secretly spread 12 deputies across five outlaws whose posters grow. The player with the most deputies on each outlaw collects its poster, and each player's secret informant outlaw is worth $3,000 more at the end.

STATE (every item below must exist in the file):
  - each player: money (number, starts 0); everyone sees it. Dollars won in the final payout. This is the score.
  - each player: deputies (number, starts 12); everyone sees it. Deputies the player has not yet committed.
  - each player: informant (text, starts ''); only its owner sees it. The player's secret informant outlaw, dealt at random and unique to each player. It is revealed at the end of the game.
  - each player: d_red (number, starts 0); everyone sees it. The player's deputy count on Red.
  - each player: d_blue (number, starts 0); everyone sees it. The player's deputy count on Blue.
  - each player: d_green (number, starts 0); everyone sees it. The player's deputy count on Green.
  - each player: d_yellow (number, starts 0); everyone sees it. The player's deputy count on Yellow.
  - each player: d_black (number, starts 0); everyone sees it. The player's deputy count on Black.
  - each player: choice_outlaw (text, starts ''); only its owner sees it. The outlaw chosen this round. It stays secret until the reveal.
  - each player: choice_number (number, starts 0); only its owner sees it. The deputies committed this round, after clamping to remaining deputies. It stays secret until the reveal.
  - the table: round (number, starts 0); everyone sees it. The current round, from 1 to 6.
  - the table: outlaws (list, starts ['Red', 'Blue', 'Green', 'Yellow', 'Black']); everyone sees it. The five outlaws. Sightings draw from this list with replacement.
  - the table: informant_deck (list, starts ['Red', 'Blue', 'Green', 'Yellow', 'Black']); hidden from all players. The hidden pool that informants are dealt from without replacement.
  - the table: sighted (text, starts ''); everyone sees it. The outlaw sighted this round.
  - the table: poster_red (number, starts 2000); everyone sees it. Red's poster value.
  - the table: poster_blue (number, starts 2000); everyone sees it. Blue's poster value.
  - the table: poster_green (number, starts 2000); everyone sees it. Green's poster value.
  - the table: poster_yellow (number, starts 2000); everyone sees it. Yellow's poster value.
  - the table: poster_black (number, starts 2000); everyone sees it. Black's poster value.
  - the table: max_red (number, starts 0); everyone sees it. Scratch value at the end: the highest deputy count on Red.
  - the table: max_blue (number, starts 0); everyone sees it. Scratch value at the end: the highest deputy count on Blue.
  - the table: max_green (number, starts 0); everyone sees it. Scratch value at the end: the highest deputy count on Green.
  - the table: max_yellow (number, starts 0); everyone sees it. Scratch value at the end: the highest deputy count on Yellow.
  - the table: max_black (number, starts 0); everyone sees it. Scratch value at the end: the highest deputy count on Black.
  - the table: tied_red (number, starts 0); everyone sees it. Scratch value at the end: the number of players whose count on Red equals max_red.
  - the table: tied_blue (number, starts 0); everyone sees it. Scratch value at the end: the number of players whose count on Blue equals max_blue.
  - the table: tied_green (number, starts 0); everyone sees it. Scratch value at the end: the number of players whose count on Green equals max_green.
  - the table: tied_yellow (number, starts 0); everyone sees it. Scratch value at the end: the number of players whose count on Yellow equals max_yellow.
  - the table: tied_black (number, starts 0); everyone sees it. Scratch value at the end: the number of players whose count on Black equals max_black.
  - parameters, each kept as a table attribute: outlaw_count = 5, starting_poster = 2000, sighting_bonus = 1000, starting_deputies = 12, starting_money = 0, informant_tip = 3000, rounds = 6, max_commit_per_round = 4, min_commit_per_round = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every poster is set to $2,000. Every player gets deputies = 12, money = 0 and all five deputy counts at 0.
  2. For each player, one outlaw is drawn at random from informant_deck, written into that player's informant and removed from informant_deck, so no two players share an informant.
  3. Each player is told privately which outlaw is their informant. Nobody else is told.
  4. round is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. sighted is set to one outlaw picked uniformly at random from outlaws, which is not removed (with replacement). The poster of sighted rises by 1000, for example poster_red += 1000 if sighted is Red.
  2. [tell] all players. What happens: The table hears: 'Round {round}: {sighted} was sighted; its poster is now {poster of sighted}.'
  3. [sync] all players. What happens: Each player is sent their own state: deputies, informant, their deputy counts, all posters and all public deputy counts.
  4. [poll] all players answers: one short text message. What happens: All messages are collected at once, then broadcast to everyone as 'Seat {seat} says: {value}'. Talk is not binding.
  5. [poll] all players answers: one choice from 25 options of the form '<outlaw> <n>', where outlaw is Red, Blue, Green, Yellow or Black and n is 0 to 4. What happens: choice_outlaw is set to the outlaw and choice_number to min(n, deputies). No answer is seen until all are in.
  6. [tell] all players. What happens: Every player's choice is announced: 'Seat {seat} commits {choice_number} deputies to {choice_outlaw}.'
  7. [update] all players. What happens: For each player, deputies -= choice_number, and the deputy count matching choice_outlaw (d_red, d_blue, d_green, d_yellow or d_black) += choice_number. Posters do not change.
  8. [update] all players. What happens: This step runs only when round == 6. Every player's informant is revealed to all. For each player, the poster of their informant += 3000.
  9. [update] all players. What happens: This step runs only when round == 6. For each outlaw X: max_X = the maximum over players of d_X, and tied_X = the number of players with d_X == max_X. For each player and each outlaw X, if max_X > 0 and d_X == max_X, then money += floor(poster_X / tied_X). An outlaw with max_X == 0 escapes and pays nobody. Unused deputies are worth nothing.
  10. [tell] all players. What happens: This step runs only when round == 6. The final posters, the informants and each player's money are announced.
  11. [check] all players. What happens: If round >= 6 the game ends. Otherwise play continues with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every poster is $2,000, and every player has 12 deputies, $0 and a deputy count of 0 on each of the five outlaws.
  R2. When the game starts, then each player is dealt a distinct informant outlaw at random that only they can see.
  R3. When a round begins, then one of the five outlaws is sighted uniformly at random with replacement, and its poster rises by $1,000.
  R4. When the same outlaw is sighted in two rounds, then its poster rises by $1,000 each time.
  R5. When the talk step runs, then every player submits one short message simultaneously, and all messages are shown to everyone only after all are in.
  R6. When the commitment step runs, then every player simultaneously chooses one outlaw and a number from 0 to 4, and no choice is seen before all are in.
  R7. When a player commits more deputies than they have remaining (for example 4 with 2 left), then the commitment is reduced to their remaining deputies (2).
  R8. When choices are in, then every player's outlaw and committed number are announced to all.
  R9. When a player commits n deputies to outlaw X, then their remaining deputies fall by n and their deputy count on X rises by n.
  R10. When deputies are committed, then no poster changes.
  R11. When round 6 ends, then all informants are revealed and each informant outlaw's poster rises by $3,000.
  R12. When an outlaw is nobody's informant, then its poster gets no $3,000 tip.
  R13. When no player has any deputies on an outlaw at the end, then it escapes and pays nobody.
  R14. When one player has the strictly highest deputy count on an outlaw at the end, then that player receives the outlaw's whole poster.
  R15. When k players tie for the highest positive deputy count on an outlaw, then each receives floor(poster / k) dollars (for example 3 players on a $5,000 poster get $1,666 each).
  R16. When the game ends, then unused deputies are worth $0, and each player's money is the sum of their payouts.
  R17. When round 6 has been resolved, then the game ends and the player with the most money wins. Players tied for the most money share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk: one short message | asked: every seat | options: Free short text, every round, for every seat.
  - Commitment: outlaw and number of deputies | asked: every seat | options: Any of the 25 combinations of outlaw (Red, Blue, Green, Yellow, Black) and n from 0 to 4, every round, even with fewer than 4 deputies left. A number above remaining deputies is reduced by the engine, as the rules say.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 6
  - each player's standing: you.money (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their money after the final payout. The player with the most money wins, and players tied for the most money share the result (the source calls this a draw).
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

- each player: `money` (number, visible: public, starts 0): Dollars won in the final payout. This is the score.
- each player: `deputies` (number, visible: public, starts 12): Deputies the player has not yet committed.
- each player: `d_red` (number, visible: public, starts 0): The player's deputy count on Red.
- each player: `d_blue` (number, visible: public, starts 0): The player's deputy count on Blue.
- each player: `d_green` (number, visible: public, starts 0): The player's deputy count on Green.
- each player: `d_yellow` (number, visible: public, starts 0): The player's deputy count on Yellow.
- each player: `d_black` (number, visible: public, starts 0): The player's deputy count on Black.
- the table: `round` (number, visible: public, starts 0): The current round, from 1 to 6.
- the table: `sighted` (text, visible: public, starts ''): The outlaw sighted this round.
- the table: `poster_red` (number, visible: public, starts 2000): Red's poster value.
- the table: `poster_blue` (number, visible: public, starts 2000): Blue's poster value.
- the table: `poster_green` (number, visible: public, starts 2000): Green's poster value.
- the table: `poster_yellow` (number, visible: public, starts 2000): Yellow's poster value.
- the table: `poster_black` (number, visible: public, starts 2000): Black's poster value.
- parameters (each must be an attribute holding this value, never a number buried in a step): outlaw_count = 5, starting_poster = 2000, sighting_bonus = 1000, starting_deputies = 12, starting_money = 0, informant_tip = 3000, rounds = 6, max_commit_per_round = 4, min_commit_per_round = 0
- the game ends with ONE ending whose `rank_by` is `you.money`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "wanted_dead_or_alive_majority",
    "name": "Wanted: Dead or Alive (Majority Rule)",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Over 6 rounds, secretly spread 12 deputies across five outlaws whose posters grow; the most deputies on an outlaw collects its poster."
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
        "key": "money",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deputies",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "informant",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "d_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_black",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "choice_outlaw",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "choice_number",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "commit_raw",
        "visible": "ally",
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
        "key": "outlaws",
        "visible": "public",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ]
      },
      {
        "key": "informant_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sighted",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sighted_poster",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "poster_red",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_blue",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_green",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_yellow",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_black",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "max_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_yellow",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_black",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_yellow",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_black",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "outlaw_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "starting_poster",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "sighting_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1000
      },
      {
        "key": "starting_deputies",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_tip",
        "visible": "public",
        "type": "number",
        "initial": 3000
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "max_commit_per_round",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_commit_per_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the posters and the deputies",
      "do": [
        {
          "set": {
            "key": "poster_red",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_blue",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_green",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_yellow",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_black",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "deputies",
            "value": {
              "calc": "starting_deputies"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "starting_money"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_yellow",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_black",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the informants",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "your informant",
      "to": "all",
      "text": "Your secret informant outlaw is {informant}. Only you know it. At the end of the game its poster rises by ${informant_tip}."
    },
    {
      "use": "update",
      "label": "the clock",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "sighting",
      "label": "the sighting",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "sighted",
            "value": {
              "calc": "outlaws[int(uniform(0, outlaw_count))]"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_red",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_blue",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_green",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Green'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_yellow",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Yellow'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_black",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Black'"
            }
          }
        },
        {
          "set": {
            "key": "sighted_poster",
            "value": {
              "calc": "poster_red if sighted == 'Red' else (poster_blue if sighted == 'Blue' else (poster_green if sighted == 'Green' else (poster_yellow if sighted == 'Yellow' else poster_black)))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "commit_raw",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "sighting",
      "label": "the sighting is announced",
      "to": "all",
      "text": "Round {round}: {sighted} was sighted; its poster is now {sighted_poster}."
    },
    {
      "use": "sync",
      "phase": "sighting",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
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
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are shown once all are in. Talk is not binding."
    },
    {
      "use": "poll",
      "phase": "commitment",
      "label": "commitment",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red 0",
          "Red 1",
          "Red 2",
          "Red 3",
          "Red 4",
          "Blue 0",
          "Blue 1",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Green 0",
          "Green 1",
          "Green 2",
          "Green 3",
          "Green 4",
          "Yellow 0",
          "Yellow 1",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Black 0",
          "Black 1",
          "Black 2",
          "Black 3",
          "Black 4"
        ]
      },
      "store": "commit_raw",
      "text": "Secretly choose one outlaw and a number of deputies from {min_commit_per_round} to {max_commit_per_round}, as '<outlaw> <n>'. You have {deputies} deputies left; a number above that is reduced to what you have left. Nobody sees any choice until all are in."
    },
    {
      "use": "update",
      "phase": "commitment",
      "label": "read the commitments",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "choice_outlaw",
            "value": {
              "calc": "('Red' if you.commit_raw[0] == 'R' else ('Green' if you.commit_raw[0] == 'G' else ('Yellow' if you.commit_raw[0] == 'Y' else ('Blue' if you.commit_raw[2] == 'u' else 'Black')))) if len(you.commit_raw) > 2 else 'Red'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice_number",
            "value": {
              "calc": "max(min_commit_per_round, min(max_commit_per_round, you.deputies, (4 if you.commit_raw[len(you.commit_raw) - 1] == '4' else (3 if you.commit_raw[len(you.commit_raw) - 1] == '3' else (2 if you.commit_raw[len(you.commit_raw) - 1] == '2' else (1 if you.commit_raw[len(you.commit_raw) - 1] == '1' else 0)))))) if len(you.commit_raw) > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Commitments this round [seat, deputies committed, outlaw]: {[[p.seat, p.choice_number, p.choice_outlaw] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the resolution",
      "do": [
        {
          "adjust": {
            "players": "all",
            "key": "d_red",
            "value": {
              "calc": "you.choice_number"
            },
            "if": {
              "calc": "you.choice_outlaw == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "d_blue",
            "value": {
              "calc": "you.choice_number"
            },
            "if": {
              "calc": "you.choice_outlaw == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "d_green",
            "value": {
              "calc": "you.choice_number"
            },
            "if": {
              "calc": "you.choice_outlaw == 'Green'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "d_yellow",
            "value": {
              "calc": "you.choice_number"
            },
            "if": {
              "calc": "you.choice_outlaw == 'Yellow'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "d_black",
            "value": {
              "calc": "you.choice_number"
            },
            "if": {
              "calc": "you.choice_outlaw == 'Black'"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "deputies",
            "value": {
              "calc": "-you.choice_number"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "the informants are revealed",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "adjust": {
            "key": "poster_red",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Red' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_blue",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Blue' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_green",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Green' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_yellow",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Yellow' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_black",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Black' for p in players)"
            }
          }
        }
      ],
      "text": "The informants are revealed [seat, informant]: {[[p.seat, p.informant] for p in players]}. Each informant outlaw's poster rises by {informant_tip}."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "the payout",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "set": {
            "key": "max_red",
            "value": {
              "calc": "max([p.d_red for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_blue",
            "value": {
              "calc": "max([p.d_blue for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_green",
            "value": {
              "calc": "max([p.d_green for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_yellow",
            "value": {
              "calc": "max([p.d_yellow for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_black",
            "value": {
              "calc": "max([p.d_black for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "tied_red",
            "value": {
              "calc": "count(p.d_red == max_red for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_blue",
            "value": {
              "calc": "count(p.d_blue == max_blue for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_green",
            "value": {
              "calc": "count(p.d_green == max_green for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_yellow",
            "value": {
              "calc": "count(p.d_yellow == max_yellow for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_black",
            "value": {
              "calc": "count(p.d_black == max_black for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "(int(poster_red / tied_red) if (max_red > 0 and you.d_red == max_red) else 0) + (int(poster_blue / tied_blue) if (max_blue > 0 and you.d_blue == max_blue) else 0) + (int(poster_green / tied_green) if (max_green > 0 and you.d_green == max_green) else 0) + (int(poster_yellow / tied_yellow) if (max_yellow > 0 and you.d_yellow == max_yellow) else 0) + (int(poster_black / tied_black) if (max_black > 0 and you.d_black == max_black) else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "end",
      "label": "the final figures",
      "when": {
        "calc": "round == rounds"
      },
      "to": "all",
      "text": "Final posters: Red {poster_red}, Blue {poster_blue}, Green {poster_green}, Yellow {poster_yellow}, Black {poster_black}. Informants [seat, outlaw]: {[[p.seat, p.informant] for p in players]}. Money [seat, dollars]: {[[p.seat, p.money] for p in players]}."
    },
    {
      "use": "check",
      "phase": "end",
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
      "rank_by": "you.money",
      "reveal": [
        "informant"
      ],
      "text": "Winner: {result}. Final money [seat, dollars]: {[[p.seat, p.money] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "There are {outlaw_count} outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at ${starting_poster}.\n\nSETUP: Each player receives {starting_deputies} deputies, which must last the whole game, and ${starting_money}. Each player is secretly assigned one informant outlaw at random, with no two players sharing one. Only that player knows it. The informant outlaw carries a hidden tip of ${informant_tip}, added to its poster at the end of the game. Outlaws that are nobody's informant carry no tip. Each player has a public deputy count on each outlaw, starting at 0. The game lasts {rounds} rounds.\n\nEACH ROUND:\n1. Sighting: one outlaw is drawn uniformly at random from all five (with replacement; the same outlaw may be sighted in several rounds). It is announced, and its poster rises by ${sighting_bonus}.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then
... (cut)

Why it was refused: playing it with random seats failed: seed 1, 3 players: the match crashed: FlowError: "you.choice_outlaw == 'Red'" reads `you` where there is no player
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "wanted_dead_or_alive_majority",
    "name": "Wanted: Dead or Alive (Majority Rule)",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Over 6 rounds, secretly spread 12 deputies across five outlaws whose posters grow; the most deputies on an outlaw collects its poster."
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
        "key": "money",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "deputies",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "informant",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "d_red",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_blue",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_green",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_yellow",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "d_black",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "choice_outlaw",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "choice_number",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "commit_raw",
        "visible": "ally",
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
        "key": "outlaws",
        "visible": "public",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ]
      },
      {
        "key": "informant_deck",
        "visible": "none",
        "type": "list",
        "initial": [
          "Red",
          "Blue",
          "Green",
          "Yellow",
          "Black"
        ]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sighted",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "sighted_poster",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "poster_red",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_blue",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_green",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_yellow",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "poster_black",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "max_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_yellow",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "max_black",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_red",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_blue",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_green",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_yellow",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tied_black",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "outlaw_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "starting_poster",
        "visible": "public",
        "type": "number",
        "initial": 2000
      },
      {
        "key": "sighting_bonus",
        "visible": "public",
        "type": "number",
        "initial": 1000
      },
      {
        "key": "starting_deputies",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "starting_money",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "informant_tip",
        "visible": "public",
        "type": "number",
        "initial": 3000
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "max_commit_per_round",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "min_commit_per_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the posters and the deputies",
      "do": [
        {
          "set": {
            "key": "poster_red",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_blue",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_green",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_yellow",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "key": "poster_black",
            "value": {
              "calc": "starting_poster"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "deputies",
            "value": {
              "calc": "starting_deputies"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "starting_money"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_red",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_blue",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_green",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_yellow",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d_black",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "deal the informants",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 1"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 3"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "informant_deck[int(uniform(0, len(informant_deck)))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 4"
            },
            "key": "informant",
            "value": {
              "calc": "pick"
            }
          }
        },
        {
          "remove": {
            "key": "informant_deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "your informant",
      "to": "all",
      "text": "Your secret informant outlaw is {informant}. Only you know it. At the end of the game its poster rises by ${informant_tip}."
    },
    {
      "use": "update",
      "label": "the clock",
      "do": [
        {
          "set": {
            "key": "round",
            "value": 0
          }
        }
      ]
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "sighting",
      "label": "the sighting",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "sighted",
            "value": {
              "calc": "outlaws[int(uniform(0, outlaw_count))]"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_red",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Red'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_blue",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Blue'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_green",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Green'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_yellow",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Yellow'"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_black",
            "value": {
              "calc": "sighting_bonus"
            },
            "if": {
              "calc": "sighted == 'Black'"
            }
          }
        },
        {
          "set": {
            "key": "sighted_poster",
            "value": {
              "calc": "poster_red if sighted == 'Red' else (poster_blue if sighted == 'Blue' else (poster_green if sighted == 'Green' else (poster_yellow if sighted == 'Yellow' else poster_black)))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "commit_raw",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "sighting",
      "label": "the sighting is announced",
      "to": "all",
      "text": "Round {round}: {sighted} was sighted; its poster is now {sighted_poster}."
    },
    {
      "use": "sync",
      "phase": "sighting",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
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
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are shown once all are in. Talk is not binding."
    },
    {
      "use": "poll",
      "phase": "commitment",
      "label": "commitment",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "Red 0",
          "Red 1",
          "Red 2",
          "Red 3",
          "Red 4",
          "Blue 0",
          "Blue 1",
          "Blue 2",
          "Blue 3",
          "Blue 4",
          "Green 0",
          "Green 1",
          "Green 2",
          "Green 3",
          "Green 4",
          "Yellow 0",
          "Yellow 1",
          "Yellow 2",
          "Yellow 3",
          "Yellow 4",
          "Black 0",
          "Black 1",
          "Black 2",
          "Black 3",
          "Black 4"
        ]
      },
      "store": "commit_raw",
      "text": "Secretly choose one outlaw and a number of deputies from {min_commit_per_round} to {max_commit_per_round}, as '<outlaw> <n>'. You have {deputies} deputies left; a number above that is reduced to what you have left. Nobody sees any choice until all are in."
    },
    {
      "use": "update",
      "phase": "commitment",
      "label": "read the commitments",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "choice_outlaw",
            "value": {
              "calc": "('Red' if you.commit_raw[0] == 'R' else ('Green' if you.commit_raw[0] == 'G' else ('Yellow' if you.commit_raw[0] == 'Y' else ('Blue' if you.commit_raw[2] == 'u' else 'Black')))) if len(you.commit_raw) > 2 else 'Red'"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice_number",
            "value": {
              "calc": "max(min_commit_per_round, min(max_commit_per_round, you.deputies, (4 if you.commit_raw[len(you.commit_raw) - 1] == '4' else (3 if you.commit_raw[len(you.commit_raw) - 1] == '3' else (2 if you.commit_raw[len(you.commit_raw) - 1] == '2' else (1 if you.commit_raw[len(you.commit_raw) - 1] == '1' else 0)))))) if len(you.commit_raw) > 0 else 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "Commitments this round [seat, deputies committed, outlaw]: {[[p.seat, p.choice_number, p.choice_outlaw] for p in players]}."
    },
    {
      "use": "update",
      "phase": "resolution",
      "label": "the resolution",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.choice_outlaw == 'Red'"
            },
            "key": "d_red",
            "value": {
              "calc": "you.choice_number"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.choice_outlaw == 'Blue'"
            },
            "key": "d_blue",
            "value": {
              "calc": "you.choice_number"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.choice_outlaw == 'Green'"
            },
            "key": "d_green",
            "value": {
              "calc": "you.choice_number"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.choice_outlaw == 'Yellow'"
            },
            "key": "d_yellow",
            "value": {
              "calc": "you.choice_number"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.choice_outlaw == 'Black'"
            },
            "key": "d_black",
            "value": {
              "calc": "you.choice_number"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "deputies",
            "value": {
              "calc": "0 - you.choice_number"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "end",
      "label": "the informants are revealed",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "adjust": {
            "key": "poster_red",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Red' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_blue",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Blue' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_green",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Green' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_yellow",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Yellow' for p in players)"
            }
          }
        },
        {
          "adjust": {
            "key": "poster_black",
            "value": {
              "calc": "informant_tip"
            },
            "if": {
              "calc": "any(p.informant == 'Black' for p in players)"
            }
          }
        }
      ],
      "text": "The informants are revealed [seat, informant]: {[[p.seat, p.informant] for p in players]}. Each informant outlaw's poster rises by {informant_tip}."
    },
    {
      "use": "update",
      "phase": "end",
      "label": "the payout",
      "when": {
        "calc": "round == rounds"
      },
      "do": [
        {
          "set": {
            "key": "max_red",
            "value": {
              "calc": "max([p.d_red for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_blue",
            "value": {
              "calc": "max([p.d_blue for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_green",
            "value": {
              "calc": "max([p.d_green for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_yellow",
            "value": {
              "calc": "max([p.d_yellow for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "max_black",
            "value": {
              "calc": "max([p.d_black for p in players])"
            }
          }
        },
        {
          "set": {
            "key": "tied_red",
            "value": {
              "calc": "count(p.d_red == max_red for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_blue",
            "value": {
              "calc": "count(p.d_blue == max_blue for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_green",
            "value": {
              "calc": "count(p.d_green == max_green for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_yellow",
            "value": {
              "calc": "count(p.d_yellow == max_yellow for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "tied_black",
            "value": {
              "calc": "count(p.d_black == max_black for p in players)"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "money",
            "value": {
              "calc": "(int(poster_red / tied_red) if (max_red > 0 and you.d_red == max_red) else 0) + (int(poster_blue / tied_blue) if (max_blue > 0 and you.d_blue == max_blue) else 0) + (int(poster_green / tied_green) if (max_green > 0 and you.d_green == max_green) else 0) + (int(poster_yellow / tied_yellow) if (max_yellow > 0 and you.d_yellow == max_yellow) else 0) + (int(poster_black / tied_black) if (max_black > 0 and you.d_black == max_black) else 0)"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "end",
      "label": "the final figures",
      "when": {
        "calc": "round == rounds"
      },
      "to": "all",
      "text": "Final posters: Red {poster_red}, Blue {poster_blue}, Green {poster_green}, Yellow {poster_yellow}, Black {poster_black}. Informants [seat, outlaw]: {[[p.seat, p.informant] for p in players]}. Money [seat, dollars]: {[[p.seat, p.money] for p in players]}."
    },
    {
      "use": "check",
      "phase": "end",
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
      "rank_by": "you.money",
      "reveal": [
        "informant"
      ],
      "text": "Winner: {result}. Final money [seat, dollars]: {[[p.seat, p.money] for p in players]}."
    }
  },
  "limits": {
    "rounds": 6,
    "rounds_max": 6,
    "actions_max": 500,
    "deadline_s": 120
  },
  "rules": "OUTLAWS: There are {outlaw_count} outlaws: Red, Blue, Green, Yellow and Black. Each has a public poster starting at ${starting_poster}.\n\nSETUP: Each player receives {starting_deputies} deputies, which must last the whole game, and ${starting_money}. Each player is secretly assigned one informant outlaw at random, with no two players sharing one. Only that player knows it. The informant outlaw carries a hidden tip of ${informant_tip}, added to its poster at the end of the game. Outlaws that are nobody's informant carry no tip. Each player has a public deputy count on each outlaw, starting at 0. The game lasts {rounds} rounds.\n\nEACH ROUND:\n1. Sighting: one outlaw is drawn uniformly at random from all five (with replacement; the same outlaw may be sighted in several rounds). It is announced, and its poster rises by ${sighting_bonus}.\n2. Talk: every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Talk is not binding.\n3. Commitment: at the same time, every player secretly chooses one outlaw and a number of deputies from {min_commit_per_round} to {max_commit_per_round}, answered as '<outlaw> <n>'. If the number exceeds their remaining deputies, it is reduced to their remaining deputies; otherwise it stands as chosen.\n4. Reveal: all choices are announced.\n5. Resolution: each player's remaining deputies fall by the number they committed, and their deputy count on the chosen outlaw rises by that number. Commitments do not change posters.\n\nEND OF GAME (after round {rounds}):\n- All informants are revealed. Each informant outlaw's poster rises by ${informant_tip}; an outlaw that is nobody's informant gets no tip.\n- For each outlaw: if no player has any deputies on it, it escapes and pays nobody. Otherwise the player with the highest deputy count on it receives its whole poster. If several players tie for the highest count, the poster is split equally among them, rounded down to the dollar.\n- Unused deputies are worth nothing.\n- Each player's money is the sum of their payouts.\n\nThe player with the most money after the final payout wins. If two or more players tie for the most money, they share the result (a draw)."
}
```
````
