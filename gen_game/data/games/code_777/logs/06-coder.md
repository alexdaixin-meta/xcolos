# 06 coder

- time: 2026-10-27T20:47:13+00:00 (187.6s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 e253d3452cb54935, reply sha256 ba81d0148e7755b3

## Sent

````
# Task: write the XColos game file for "Code 777: Ask and Guess"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

TILES. There are 28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s and seven 7s.

SETUP. Shuffle the tiles into a face-down pile. Deal 3 tiles to each player's rack. Each player is told privately the numbers on every OTHER player's rack, but never their own. Each player starts with 0 points. The discard pile starts empty and is public: everyone always sees which tiles are in it. Seats are numbered 1 to N. Seat 1 is the active player in round 1, and the active player then rotates in seat order each round.

EACH ROUND:
1. The engine announces the round number and the active player.
2. The active player makes one choice: a question from the menu below, and a respondent, who must be one other player. For question 3, the active player also names a number k from 1 to 7.
3. The engine computes the answer exactly, counting only the tiles the respondent can see: every rack except the respondent's own. This includes the active player's rack. The engine announces the question, the respondent and the answer to everyone.
   Menu:
   (1) EVEN: how many even tiles (2, 4, 6) do you see?
   (2) HIGH: how many tiles numbered 5, 6 or 7 do you see?
   (3) NUMBER k: how many tiles numbered k do you see?
   (4) SUM15: how many of the racks you see total 15 or more?
   (5) PAIR: how many of the racks you see hold at least two tiles of the same number?
   (6) MISSING: how many of the numbers 1 to 7 appear on none of the racks you see?
4. GUESS POLL. All players answer at the same moment, without seeing each other's answers. Each either writes PASS or writes three numbers (order irrelevant) as a guess at their own rack.
5. SCORING. A guess that matches the player's rack exactly as a set of three numbers, duplicates included, scores +1 point. Any other guess scores -1 point. PASS scores 0. Scores may be negative.
6. REVEAL AND REPLACE. Every player who guessed, right or wrong, has their three tiles announced to all and moved to the discard pile. If the face-down pile then holds fewer tiles than are needed, the discard pile is shuffled into it. The engine then deals 3 new tiles to each player who guessed. This is the round's single random event.
7. Every player is privately told the current racks of all OTHER players.
8. END CHECK. If any player has 3 or more points, the game ends. Otherwise, if the final round has been played, the game ends. The final round is round 30 with 3 players and round 40 with 4 players.

There is no talk phase; the engine-answered questions are the only shared information.

How the winner is decided: When the game ends because someone reached 3 points, the player with the most points wins. If two or more players share that top score, the game is a draw. If the round limit is reached instead, the player with the highest score wins, and a tie for the highest score is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Code 777: Ask and Guess (3 to 4 players, best with 3)

Each player sees every rack but their own. Players ask engine-answered counting questions and guess their own three hidden tiles; the first to 3 points ends the game.

STATE (every item below must exist in the file):
  - each player: rack (list, starts []); everyone but its owner sees it. The player's three tiles. Every other player sees them; the owner never does.
  - each player: score (number, starts 0); everyone sees it. Points; may be negative.
  - each player: guess (text, starts ''); only its owner sees it. This round's answer to the guess poll: PASS or three numbers.
  - each player: guessed (bool, starts False); everyone sees it. True if the player submitted a guess (not PASS) this round.
  - the table: deck (list, starts '28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s'); hidden from all players. The face-down pile.
  - the table: discard (list, starts []); everyone sees it. The public discard pile of revealed tiles.
  - the table: round (number, starts 0); everyone sees it. The current round number.
  - the table: active_seat (number, starts 0); everyone sees it. The seat of this round's active player: ((round - 1) mod N) + 1.
  - the table: question (text, starts ''); everyone sees it. This round's chosen question: EVEN, HIGH, NUMBER, SUM15, PAIR or MISSING.
  - the table: respondent (number, starts 0); everyone sees it. The seat named as respondent.
  - the table: k (number, starts 0); everyone sees it. The number named for the NUMBER question.
  - the table: answer (number, starts 0); everyone sees it. The engine-computed answer to this round's question.
  - the table: final_round (number, starts '10 * N'); everyone sees it. The last round: 30 with 3 players, 40 with 4.
  - parameters, each kept as a table attribute: tiles_total = 28, count_of_1 = 1, count_of_2 = 2, count_of_3 = 3, count_of_4 = 4, count_of_5 = 5, count_of_6 = 6, count_of_7 = 7, rack_size = 3, starting_score = 0, correct_guess_points = 1, wrong_guess_points = -1, pass_points = 0, win_points = 3, rounds_per_player = 10, final_round_3_players = 30, final_round_4_players = 40, k_min = 1, k_max = 7, sum_threshold = 15, pair_min_same = 2, high_min = 5, number_range_min = 1, number_range_max = 7

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Fill the deck with the 28 tiles: one 1, two 2s, three 3s, four 4s, five 5s, six 6s and seven 7s.
  2. Deal 3 tiles at random from deck to each player's rack, removing each from deck.
  3. Set every score to 0 and discard to empty; set final_round to 10 * N.
  4. Sync: each player is privately shown the racks of every other player, never their own.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; active_seat = ((round - 1) mod N) + 1; every guess = '' and guessed = false. Announce the round number and the active seat.
  2. [ask] the seat equal to active_seat answers: a choice of question (EVEN, HIGH, NUMBER, SUM15, PAIR, MISSING) paired with a respondent, who is one other seat. What happens: question and respondent are set from the choice.
  3. [ask] the seat equal to active_seat, only when question = NUMBER answers: a whole number from 1 to 7. What happens: k is set.
  4. [update] all players. What happens: answer is computed over the racks of every seat except respondent (the active player's rack included). EVEN = count of tiles in {2,4,6}; HIGH = count of tiles in {5,6,7}; NUMBER = count of tiles equal to k; SUM15 = count of those racks whose sum >= 15; PAIR = count of those racks holding at least two tiles of the same number; MISSING = count of the numbers 1..7 that appear on none of those racks. Announce the question, the respondent (and k if used) and the answer to everyone.
  5. [poll] all players answers: short text: PASS, or three numbers from 1 to 7 (order irrelevant). What happens: guess is set for each player; guessed = (guess != PASS).
  6. [update] all players. What happens: For each player with guessed = true: if sorted(guess) equals sorted(rack), score += 1; otherwise score -= 1. A PASS leaves score unchanged.
  7. [update] all players. What happens: For each player with guessed = true: announce their rack to all, append the rack to discard, and set rack = []. If length(deck) < 3 * (number of players with guessed = true), move every tile from discard into deck. Then deal 3 tiles at random from deck to the rack of each player who guessed, removing each from deck.
  8. [sync] all players. What happens: Each player is privately shown the current racks of all other players.
  9. [check] all players. What happens: End the game if any score >= 3 or round >= final_round; otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck holds 28 tiles (one 1, two 2s, three 3s, four 4s, five 5s, six 6s, seven 7s), each player is dealt 3 tiles into rack, and the deck then holds 28 - 3N.
  R2. When racks are shown, each player sees every other player's rack and never their own.
  R3. When the game starts, every score is 0 and discard is empty.
  R4. When round r begins, the active seat is ((r - 1) mod N) + 1, so seat 1 is active in round 1.
  R5. When the active player chooses a respondent, the respondent must be a seat other than the active player.
  R6. When the question is NUMBER, the active player also names k from 1 to 7.
  R7. When an answer is computed, it counts only the racks of every seat except the respondent, including the active player's rack.
  R8. When the question is EVEN, the answer is the number of tiles showing 2, 4 or 6 on those racks.
  R9. When the question is HIGH, the answer is the number of tiles showing 5, 6 or 7 on those racks.
  R10. When the question is NUMBER with k, the answer is the number of tiles equal to k on those racks.
  R11. When the question is SUM15, the answer is the number of those racks whose three tiles sum to 15 or more.
  R12. When the question is PAIR, the answer is the number of those racks holding at least two tiles of the same number.
  R13. When the question is MISSING, the answer is how many of the numbers 1 to 7 appear on none of those racks.
  R14. When an answer is computed, the question, the respondent and the answer are announced to everyone.
  R15. When the guess poll runs, all players answer simultaneously, each with PASS or three numbers.
  R16. When a guess matches the player's rack as a multiset of three numbers, the player's score rises by 1.
  R17. When a guess does not match the player's rack, the player's score falls by 1, and the score may go negative.
  R18. When a player answers PASS, the player's score is unchanged and the rack is kept.
  R19. When a player guessed, right or wrong, their three tiles are announced to all and moved to discard, and they are dealt 3 new tiles from deck.
  R20. When the deck holds fewer than 3 times the number of guessers, all of discard is moved into deck before dealing.
  R21. When any player's score is 3 or more after scoring, the game ends.
  R22. When round 30 (with 3 players) or round 40 (with 4 players) has been played, the game ends.
  R23. When the game ends, the highest score wins, and a tie for the highest score is a draw shared by the tied players.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose a question and a respondent | asked: the active seat only | options: each of EVEN, HIGH, NUMBER, SUM15, PAIR, MISSING, paired with each seat other than the active seat (6 × (N - 1) options)
  - Choose k for NUMBER | asked: the active seat, only when question = NUMBER | options: 1, 2, 3, 4, 5, 6, 7
  - Guess poll | asked: every seat | options: PASS, or any three numbers each from 1 to 7 (repeats allowed, order irrelevant)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: max over players of score >= 3 OR round >= final_round (final_round = 10 * N)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the highest score wins. Players tied at the top share it, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Points; may be negative.
- the table: `discard` (list, visible: public, starts []): The public discard pile of revealed tiles.
- the table: `round` (number, visible: public, starts 0): The current round number.
- the table: `answer` (number, visible: public, starts 0): The engine-computed answer to this round's question.
- parameters (each must be an attribute holding this value, never a number buried in a step): tiles_total = 28, count_of_1 = 1, count_of_2 = 2, count_of_3 = 3, count_of_4 = 4, count_of_5 = 5, count_of_6 = 6, count_of_7 = 7, rack_size = 3, starting_score = 0, correct_guess_points = 1, wrong_guess_points = -1, pass_points = 0, win_points = 3, rounds_per_player = 10, final_round_3_players = 30, final_round_4_players = 40, k_min = 1, k_max = 7, sum_threshold = 15, pair_min_same = 2, high_min = 5, number_range_min = 1, number_range_max = 7
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

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "code777_ask_and_guess",
    "name": "Code 777: Ask and Guess",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 3
    },
    "blurb": "You see every rack but your own. Ask counting questions and guess your three hidden tiles; the first to 3 points ends the game."
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
        "key": "rack",
        "visible": "others",
        "type": "list",
        "initial": []
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guessed",
        "visible": "public",
        "type": "bool",
        "initial": false
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
        "initial": [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7]
      },
      {
        "key": "discard",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "active_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "question",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "respondent",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "k",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "answer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_reveal",
        "visible": "public",
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
        "key": "seen",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "reshuffle",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "guess_options",
        "visible": "none",
        "type": "list",
        "initial": [
          "PASS",
          "1 1 1", "1 1 2", "1 1 3", "1 1 4", "1 1 5", "1 1 6", "1 1 7",
          "1 2 2", "1 2 3", "1 2 4", "1 2 5", "1 2 6", "1 2 7",
          "1 3 3", "1 3 4", "1 3 5", "1 3 6", "1 3 7",
          "1 4 4", "1 4 5", "1 4 6", "1 4 7",
          "1 5 5", "1 5 6", "1 5 7",
          "1 6 6", "1 6 7",
          "1 7 7",
          "2 2 2", "2 2 3", "2 2 4", "2 2 5", "2 2 6", "2 2 7",
          "2 3 3", "2 3 4", "2 3 5", "2 3 6", "2 3 7",
          "2 4 4", "2 4 5", "2 4 6", "2 4 7",
          "2 5 5", "2 5 6", "2 5 7",
          "2 6 6", "2 6 7",
          "2 7 7",
          "3 3 3", "3 3 4", "3 3 5", "3 3 6", "3 3 7",
          "3 4 4", "3 4 5", "3 4 6", "3 4 7",
          "3 5 5", "3 5 6", "3 5 7",
          "3 6 6", "3 6 7",
          "3 7 7",
          "4 4 4", "4 4 5", "4 4 6", "4 4 7",
          "4 5 5", "4 5 6", "4 5 7",
          "4 6 6", "4 6 7",
          "4 7 7",
          "5 5 5", "5 5 6", "5 5 7",
          "5 6 6", "5 6 7",
          "5 7 7",
          "6 6 6", "6 6 7",
          "6 7 7",
          "7 7 7"
        ]
      },
      {
        "key": "tiles_total",
        "visible": "public",
        "type": "number",
        "initial": 28
      },
      {
        "key": "count_of_1",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_of_2",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_of_3",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_of_4",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "count_of_5",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "count_of_6",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "count_of_7",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "rack_size",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "correct_guess_points",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "wrong_guess_points",
        "visible": "public",
        "type": "number",
        "initial": -1
      },
      {
        "key": "pass_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "win_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_player",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "final_round_3_players",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "final_round_4_players",
        "visible": "public",
        "type": "number",
        "initial": 40
      },
      {
        "key": "k_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "k_max",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "sum_threshold",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "pair_min_same",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "high_min",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "number_range_min",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "number_range_max",
        "visible": "public",
        "type": "number",
        "initial": 7
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "deal the racks",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "len(players) >= 4"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "len(players) >= 4"}}}
      ]
    },
    {
      "use": "update",
      "label": "scores, discard and final round",
      "do": [
        {"set": {"players": "all", "key": "score", "value": {"calc": "starting_score"}}},
        {"set": {"key": "discard", "value": []}},
        {"set": {"key": "final_round", "value": {"calc": "rounds_per_player * len(players)"}}}
      ],
      "text": "Every score starts at {starting_score}. The discard pile is empty. The final round is round {final_round}."
    },
    {
      "use": "sync",
      "label": "the racks you see",
      "mode": "others",
      "to": "all",
      "fields": ["rack"],
      "text": "The racks of the other players:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "ask",
      "label": "a new round",
      "do": [
        {"adjust": {"key": "round", "value": 1}},
        {"set": {"key": "active_seat", "value": {"calc": "((round - 1) % len(players)) + 1"}}},
        {"set": {"players": "all", "key": "guess", "value": ""}},
        {"set": {"players": "all", "key": "guessed", "value": false}},
        {"set": {"key": "k", "value": 0}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "['EVEN to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat] + ['HIGH to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat] + ['NUMBER to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat] + ['SUM15 to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat] + ['PAIR to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat] + ['MISSING to seat ' + ['1','2','3','4'][p.seat - 1] for p in players if p.seat != you.seat]"}}}
      ],
      "text": "Round {round} of at most {final_round}: seat {active_seat} is the active player."
    },
    {
      "use": "ask",
      "phase": "ask",
      "label": "choose a question and respondent",
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "qr"
      },
      "text": "You are the active player. Choose a question and the other seat who answers it. EVEN: how many even tiles (2, 4, 6) do they see? HIGH: how many tiles numbered 5, 6 or 7? NUMBER: how many tiles of a number k you name next? SUM15: how many racks they see total 15 or more? PAIR: how many racks they see hold two or more tiles of the same number? MISSING: how many of the numbers 1 to 7 appear on none of the racks they see? The respondent sees every rack except their own, yours included."
    },
    {
      "use": "update",
      "phase": "ask",
      "label": "record the question",
      "do": [
        {"set": {"key": "question", "value": {"calc": "[q for q in ['EVEN', 'HIGH', 'NUMBER', 'SUM15', 'PAIR', 'MISSING'] if $qr in [q + ' to seat 1', q + ' to seat 2', q + ' to seat 3', q + ' to seat 4']][0]"}}},
        {"set": {"key": "respondent", "value": {"calc": "[s for s in [1, 2, 3, 4] if $qr == question + ' to seat ' + ['1','2','3','4'][s - 1]][0]"}}}
      ]
    },
    {
      "use": "ask",
      "phase": "ask",
      "label": "choose k",
      "when": {
        "calc": "question == 'NUMBER'"
      },
      "to": {
        "where": "you.seat == active_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "k_min"
        },
        "max": {
          "calc": "k_max"
        }
      },
      "verify": {
        "bind": "kk"
      },
      "text": "Name the number k (from {k_min} to {k_max}) for the NUMBER question: the respondent will say how many tiles numbered k they see."
    },
    {
      "use": "update",
      "phase": "ask",
      "label": "the answer",
      "do": [
        {"set": {"key": "k", "value": "$kk", "if": {"calc": "question == 'NUMBER'"}}},
        {"set": {"key": "seen", "value": {"calc": "[p.rack[0] for p in players if p.seat != respondent] + [p.rack[1] for p in players if p.seat != respondent] + [p.rack[2] for p in players if p.seat != respondent]"}}},
        {"set": {"key": "answer", "value": {"calc": "count(t % 2 == 0 for t in seen) if question == 'EVEN' else (count(t >= high_min for t in seen) if question == 'HIGH' else (count(t == k for t in seen) if question == 'NUMBER' else (count(sum(p.rack) >= sum_threshold for p in players if p.seat != respondent) if question == 'SUM15' else (count(p.rack[0] == p.rack[1] or p.rack[1] == p.rack[2] or p.rack[0] == p.rack[2] for p in players if p.seat != respondent) if question == 'PAIR' else count(v not in seen for v in [1, 2, 3, 4, 5, 6, 7])))))"}}}
      ],
      "text": "Seat {active_seat} asked seat {respondent} the {question} question (k = {k}; k applies only to NUMBER). Answer: {answer}."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guess poll",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "guess_options"
        }
      },
      "store": "guess",
      "text": "Guess your own rack or PASS. Choose PASS, or three numbers in ascending order (for example '3 5 7'). A correct guess (the same three numbers, duplicates included) scores {correct_guess_points}; a wrong guess scores {wrong_guess_points}; PASS scores {pass_points} and keeps your rack. Anyone who guesses, right or wrong, reveals their rack and gets three new tiles."
    },
    {
      "use": "update",
      "phase": "guess",
      "label": "scoring",
      "do": [
        {"set": {"players": "all", "key": "guessed", "value": {"calc": "you.guess != 'PASS' and you.guess != ''"}}},
        {"adjust": {"players": {"where": "you.guessed"}, "key": "score", "value": {"calc": "correct_guess_points if you.guess == ['1','2','3','4','5','6','7'][sorted(you.rack)[0] - 1] + ' ' + ['1','2','3','4','5','6','7'][sorted(you.rack)[1] - 1] + ' ' + ['1','2','3','4','5','6','7'][sorted(you.rack)[2] - 1] else wrong_guess_points"}}}
      ],
      "text": "Guesses scored. Scores [seat, score]: {[[p.seat, p.score] for p in players]}."
    },
    {
      "use": "update",
      "phase": "replace",
      "label": "reveal and replace",
      "when": {
        "calc": "count(p.guessed for p in players) > 0"
      },
      "do": [
        {"set": {"key": "last_reveal", "value": {"calc": "[[p.seat, p.rack] for p in players if p.guessed]"}}},
        {"set": {"key": "discard", "value": {"calc": "discard + players[0].rack"}, "if": {"calc": "players[0].guessed"}}},
        {"set": {"key": "discard", "value": {"calc": "discard + players[1].rack"}, "if": {"calc": "players[1].guessed"}}},
        {"set": {"key": "discard", "value": {"calc": "discard + players[2].rack"}, "if": {"calc": "players[2].guessed"}}},
        {"set": {"key": "discard", "value": {"calc": "discard + ([] if len(players) < 4 else players[3].rack)"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"set": {"players": {"where": "you.guessed"}, "key": "rack", "value": []}},
        {"set": {"key": "reshuffle", "value": {"calc": "len(deck) < rack_size * count(p.guessed for p in players)"}}},
        {"set": {"key": "deck", "value": {"calc": "deck + discard"}, "if": {"calc": "reshuffle"}}},
        {"set": {"key": "discard", "value": [], "if": {"calc": "reshuffle"}}},

        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 1, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 1 and p.guessed for p in players) > 0"}}},

        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 2, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 2 and p.guessed for p in players) > 0"}}},

        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 3, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 3 and p.guessed for p in players) > 0"}}},

        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"append": {"player": 4, "key": "rack", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "count(p.seat == 4 and p.guessed for p in players) > 0"}}}
      ],
      "text": "Racks revealed by the players who guessed [seat, tiles]: {last_reveal}. Those tiles went to the discard pile and each guesser was dealt three new tiles. Discard pile now: {discard}."
    },
    {
      "use": "sync",
      "phase": "replace",
      "label": "the racks you see",
      "mode": "others",
      "to": "all",
      "fields": ["rack"],
      "text": "The current racks of the other players:"
    },
    {
      "use": "check",
      "phase": "replace",
      "label": "end check",
      "when": {
        "calc": "max([p.score for p in players]) >= win_points or round >= final_round"
      },
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "max([p.score for p in players]) >= win_points or round >= final_round"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores [seat, score]: {[[p.seat, p.score] for p in players]}; target {win_points}, after round {round}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "TILES. There are {tiles_total} tiles: {count_of_1} 1, {count_of_2} 2s, {count_of_3} 3s, {count_of_4} 4s, {count_of_5} 5s, {count_of_6} 6s and {count_of_7} 7s.\n\nSETUP. The tiles are shuffled into a face-down pile. Each player is dealt {rack_size} tiles to their rack. Each player is told privately the numbers on every OTHER player's rack, but never their own. Each player starts with {starting_score} points. The discard pile starts empty and is public: everyone always sees which tiles are in it. Seat 1 is the active player in round 1, and the active player then rotates in seat order each round.\n\nEACH ROUND:\n1. The engine announces the round number and the active player.\n2. The active player chooses a question from the menu and a respondent, who must be one other player. For NUMBER, the active player also names a number k from {k_min} to {k_max}.\n3. The engine computes the answer exactly, counting only the tiles the respondent can see: every rack except the respondent's own, including the active player's rack. The question, the respondent and the answer are announced to everyone.\n   EVEN: how many even tiles (2, 4, 6) do you see?\n   HIGH: how many tiles numbered {high_min}, 6 or 7 do you see?\n   NUMBER k: how many tiles numbered k do you see?\n   SUM15: how many of the racks you see total {sum_threshold} or more?\n   PAIR: how many of the racks you see hold at least {pair_min_same} tiles of the same number?\n   MISSING: how many of the numbers {number_range_min} to {number_range_max} appear on none of the racks you see?\n4. GUESS POLL. All players answer at the same moment, without seeing each other's answers. Each either chooses PASS or three numbers (written in ascending order, order irrelevant) as a guess at their own rack.\n5. SCORING. A guess that matches your rack exactly as a set of three numbers, duplicates included, scores {correct_guess_points} point. Any other guess scores {wrong_guess_points} point. PASS scores {pass_points} and you keep your rack. Scores may be negative.\n6. REVEAL AND REPLACE. Every player who guessed, right or wrong, has their three tiles announced to all and moved to the discard pile. If the face-down pile then holds fewer tiles than are needed, the discard pile is shuffled into it. Each player who guessed is then dealt 3 new tiles.\n7. Every player is privately told the current racks of all OTHER players.\n8. END CHECK. If any player has {win_points} or more points, the game ends. Otherwise, if the final round has been played, the game ends. The final round is round {final_round_3_players} with 3 players and round {final_round_4_players} with 4 players ({rounds_per_player} rounds per player).\n\nThere is no talk phase; the engine-answered questions are the only shared information.\n\nWINNER. When the game ends, the player with the highest score wins; players tied for the highest score share the win (a draw)."
}
```
````
