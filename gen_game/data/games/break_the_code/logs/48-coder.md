# 48 coder

- time: 2026-10-27T19:19:39+00:00 (53.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 f01c8d9910c386d3, reply sha256 b5107e7d89464601

## Sent

````
# Task: write the XColos game file for "Break the Code: Duel of Two Tiles"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

SETUP. The match is 4 legs of 6 turns each (24 turns). Scores start at 0.

CODES. At the start of each leg, both players at the same moment secretly choose a code of two tiles. Each tile is a whole number from 0 to 5. A code is written low tile then high tile, with low no greater than high; equal tiles are allowed, for example 3-3. There are 21 possible codes. A code cannot be changed during the leg.

TURNS. On each turn of a leg, both players choose at the same moment. Each picks exactly one of the following actions, about the opponent's code:
- Question A (Sum): is the sum of the two tiles LOW (0-3), MIDDLE (4-6) or HIGH (7-10)?
- Question B (Odd): how many tiles are odd: 0, 1 or 2?
- Question C (Gap): is high minus low 0 (PAIR), 1 (ADJACENT) or 2 or more (APART)?
- Question D (Big): how many tiles are 3 or more: 0, 1 or 2?
- Question E (Edge): how many tiles are 0 or 5: 0, 1 or 2?
- Guess: name a full code (low, high).
Repeating a question is allowed, but it gives the same answer again.

ANSWERS. After both have chosen, the engine announces to both players each player's action and its truthful answer, computed from the opponent's code.
- If a guess equals the opponent's code exactly, it is CORRECT. The guesser scores 7 minus the turn number within the leg: 6 points on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5 and 1 on turn 6.
- If a guess is wrong, it scores 0 and costs nothing else. The engine announces how many of the guessed tiles appear in the code, which is 0 or 1. Each code tile can match at most one guessed tile.

SOLVED. A player who guesses correctly has solved the leg. For the rest of that leg their choices are ignored and they score nothing more. The other player keeps playing normally.

END OF LEG. After turn 6 of a leg, both codes are revealed to both players. Unsolved legs score nothing for anyone. The next leg starts with new codes.

END OF MATCH. After 4 legs the match ends.

How the winner is decided: After 4 legs, the player with the higher total score wins. If totals are equal, the player who solved more legs wins. If that is also equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Break the Code: Duel of Two Tiles (2 to 2 players, best with 2)

Two players each hide a two-tile code (tiles 0-5) every leg, then ask simultaneous property questions or guess the opponent's code; earlier correct guesses score more over 4 legs of 6 turns.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. total points from correct guesses
  - each player: legs_solved (number, starts 0); everyone sees it. number of legs in which this player guessed the opponent's code; first tie-break
  - each player: code_low (number, starts 0); only its owner sees it. low tile of this player's secret code for the current leg (0-5)
  - each player: code_high (number, starts 0); only its owner sees it. high tile of this player's secret code for the current leg (0-5, at least code_low)
  - each player: solved (bool, starts False); everyone sees it. true once this player has guessed the opponent's code correctly in the current leg
  - each player: last_action (text, starts ''); everyone sees it. this turn's action (sum, odd, gap, big, edge or guess low-high), or 'solved' if the player's choices are ignored
  - each player: last_answer (text, starts ''); everyone sees it. the truthful answer to last_action, computed from the opponent's code
  - each player: guess_low (number, starts 0); everyone sees it. low tile of this turn's guess, if the action was a guess
  - each player: guess_high (number, starts 0); everyone sees it. high tile of this turn's guess, if the action was a guess
  - the table: leg (number, starts 1); everyone sees it. current leg, 1 to 4; becomes 5 when the match is over
  - the table: turn_in_leg (number, starts 1); everyone sees it. current turn within the leg, 1 to 6
  - the table: seat1_code_low (number, starts 0); hidden from all players. mirror of seat 1's code_low, so that seat 2's questions can be answered (player-attribute compare workaround)
  - the table: seat1_code_high (number, starts 0); hidden from all players. mirror of seat 1's code_high
  - the table: seat2_code_low (number, starts 0); hidden from all players. mirror of seat 2's code_low
  - the table: seat2_code_high (number, starts 0); hidden from all players. mirror of seat 2's code_high
  - parameters, each kept as a table attribute: legs = 4, turns_per_leg = 6, total_turns = 24, starting_score = 0, tile_min = 0, tile_max = 5, possible_codes = 21, guess_score_base = 7, sum_low_max = 3, sum_middle_min = 4, sum_middle_max = 6, sum_high_min = 7, sum_high_max = 10, gap_pair = 0, gap_adjacent = 1, gap_apart_min = 2, big_tile_min = 3, edge_tile_low = 0, edge_tile_high = 5, wrong_guess_cost = 0, tie_break_weight = 10

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Two seats are filled; score and legs_solved start at 0 for both.
  2. leg is set to 1 and turn_in_leg is set to 1.
  3. Both players are told the rules: 4 legs of 6 turns, the 21 codes, the five questions and how guesses score.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: when turn_in_leg == 1: set solved = false, last_action = '', last_answer = '' for both players
  2. [poll] all players answers: one of the 21 codes: 0-0, 0-1, 0-2, 0-3, 0-4, 0-5, 1-1, 1-2, 1-3, 1-4, 1-5, 2-2, 2-3, 2-4, 2-5, 3-3, 3-4, 3-5, 4-4, 4-5, 5-5. What happens: when turn_in_leg == 1: set code_low and code_high from the chosen code (low <= high), and copy them to seatN_code_low and seatN_code_high; no one sees another's choice
  3. [sync] all players. What happens: each player is shown their own code_low and code_high, their score, legs_solved, leg and turn_in_leg
  4. [poll] each player with solved == false answers: one of 26 choices: sum, odd, gap, big, edge, or guess X-Y for one of the 21 codes. What happens: set last_action to the choice; for a guess, set guess_low and guess_high from it. Players with solved == true are not asked and get last_action = 'solved'
  5. [update] all players. What happens: for each unsolved player, with the opponent's code (L, H) taken from the opponent's mirror attributes: sum -> last_answer = LOW if L+H <= 3, MIDDLE if 4 <= L+H <= 6, HIGH if L+H >= 7; odd -> number of odd tiles among L, H (0-2); gap -> PAIR if H-L == 0, ADJACENT if H-L == 1, APART if H-L >= 2; big -> number of tiles >= 3 (0-2); edge -> number of tiles equal to 0 or 5 (0-2); guess -> if guess_low == L and guess_high == H then last_answer = CORRECT, score += 7 - turn_in_leg, legs_solved += 1, solved = true; otherwise last_answer = WRONG with the count of guessed tiles that appear in the code, each code tile matching at most one guessed tile (0 or 1), and no other cost
  6. [tell] all players. What happens: announce to both: 'Leg {leg}, turn {turn_in_leg}. Seat 1: {last_action} -> {last_answer}. Seat 2: {last_action} -> {last_answer}. Scores: {score} / {score}.'
  7. [tell] all players. What happens: when turn_in_leg == 6: reveal both codes to both players: 'Seat 1's code was {seat1_code_low}-{seat1_code_high}; Seat 2's code was {seat2_code_low}-{seat2_code_high}.' Unsolved legs score nothing
  8. [update] all players. What happens: if turn_in_leg == 6 then turn_in_leg = 1 and leg += 1, else turn_in_leg += 1
  9. [check] all players. What happens: end the game if leg > 4, otherwise continue with the next turn

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The match is 4 legs of 6 turns each, 24 turns in all, and both scores start at 0.
  R2. When turn_in_leg is 1, both players choose a code at the same time and in secret from the 21 codes low-high with 0 <= low <= high <= 5, for example 3-3.
  R3. A player's code is not changed during a leg; code_low and code_high are only set on turn 1 of a leg.
  R4. On each turn, every unsolved player picks at the same time exactly one action: sum, odd, gap, big, edge, or guess of a full code.
  R5. When a player asks sum and the opponent's code is (L, H), then the answer is LOW if L+H is 0-3, MIDDLE if 4-6, HIGH if 7-10; for example code 2-5 gives HIGH.
  R6. When a player asks odd, then the answer is the number of odd tiles in the opponent's code; for example code 1-3 gives 2 and code 0-4 gives 0.
  R7. When a player asks gap, then the answer is PAIR if H-L = 0, ADJACENT if H-L = 1, APART if H-L >= 2; for example code 2-4 gives APART.
  R8. When a player asks big, then the answer is the number of tiles that are 3 or more; for example code 2-3 gives 1.
  R9. When a player asks edge, then the answer is the number of tiles equal to 0 or 5; for example code 0-5 gives 2 and code 0-0 gives 2.
  R10. When a player repeats a question in the same leg, then the answer is the same as before, because the code has not changed.
  R11. When a guess equals the opponent's code exactly, then it is CORRECT and the guesser scores 7 minus turn_in_leg: 6 on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5, 1 on turn 6.
  R12. When a guess is correct, then the guesser's legs_solved increases by 1 and solved becomes true for the rest of the leg.
  R13. When a guess is wrong, then it scores 0, costs nothing, and the answer is how many guessed tiles appear in the code, each code tile matching at most one guessed tile; for example guess 3-3 against code 3-4 answers 1, and guess 1-2 against code 3-4 answers 0.
  R14. When a player has solved == true, then they are not asked for an action for the rest of that leg and score nothing more in it, while the other player keeps playing normally.
  R15. After both have chosen on a turn, then both players are told each player's action and its truthful answer, computed from the opponent's code.
  R16. When turn 6 of a leg ends, then both codes are revealed to both players, solved is reset, and the next leg starts with new codes; a leg nobody solved scores nothing.
  R17. When leg becomes 5 after the fourth leg, then the match ends.
  R18. When the match ends, then the higher score wins; on equal scores the player with more legs_solved wins; if both are equal the match is a draw (shared win).

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - choose your secret code (turn 1 of each leg) | asked: both seats | options: the 21 codes: 0-0, 0-1, 0-2, 0-3, 0-4, 0-5, 1-1, 1-2, 1-3, 1-4, 1-5, 2-2, 2-3, 2-4, 2-5, 3-3, 3-4, 3-5, 4-4, 4-5, 5-5
  - choose your action this turn | asked: each seat with solved == false; a solved seat is not asked | options: sum, odd, gap, big, edge, or guess one of the 21 codes (guess 0-0 ... guess 5-5), 26 options in all

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: leg > 4
  - each player's standing: you.score * 10 + you.legs_solved (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The higher total score wins. If scores are equal, the player who solved more legs wins (legs_solved is at most 4, so a weight of 10 keeps score first). If both are equal, both share the win, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): total points from correct guesses
- each player: `legs_solved` (number, visible: public, starts 0): number of legs in which this player guessed the opponent's code; first tie-break
- each player: `last_action` (text, visible: public, starts ''): this turn's action (sum, odd, gap, big, edge or guess low-high), or 'solved' if the player's choices are ignored
- each player: `last_answer` (text, visible: public, starts ''): the truthful answer to last_action, computed from the opponent's code
- the table: `leg` (number, visible: public, starts 1): current leg, 1 to 4; becomes 5 when the match is over
- the table: `turn_in_leg` (number, visible: public, starts 1): current turn within the leg, 1 to 6
- parameters (each must be an attribute holding this value, never a number buried in a step): legs = 4, turns_per_leg = 6, total_turns = 24, starting_score = 0, tile_min = 0, tile_max = 5, possible_codes = 21, guess_score_base = 7, sum_low_max = 3, sum_middle_min = 4, sum_middle_max = 6, sum_high_min = 7, sum_high_max = 10, gap_pair = 0, gap_adjacent = 1, gap_apart_min = 2, big_tile_min = 3, edge_tile_low = 0, edge_tile_high = 5, wrong_guess_cost = 0, tie_break_weight = 10
- the game ends with ONE ending whose `rank_by` is `you.score * 10 + you.legs_solved`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

When codes are set on turn 1 of a leg, copy each opponent's code into the asker's scratch fields: seat 1's `opp_low`/`opp_high` from seat 2's `code_low`/`code_high`, and seat 2's from seat 1's. Do this after both codes are recorded and before any answer is computed, or compute answers directly from the table's `seatN_code_low`/`seatN_code_high` of the other seat. Then check every answer formula against the rules using the parameter attributes.
- **Sum:** LOW if the sum is at most `sum_low_max`, MIDDLE if it is from `sum_middle_min` to `sum_middle_max`, HIGH if it is `sum_high_min` or more.
- **Odd:** the count of odd tiles.
- **Gap:** PAIR if high minus low is `gap_pair`, ADJACENT if it is `gap_adjacent`, APART if it is at least `gap_apart_min`.
- **Big:** the count of tiles at or above `big_tile_min`.
- **Edge:** the count of tiles equal to `edge_tile_low` or `edge_tile_high`.
- **Guess:** correctness and the tile-overlap count must also be checked against the opponent's code.

Make sure the code values persist across turns 2 to 6 of the leg.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "break_the_code_duel",
    "name": "Break the Code: Duel of Two Tiles",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Hide a two-tile code each leg, ask property questions or guess your opponent's code; earlier correct guesses score more over 4 legs of 6 turns."
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
      },
      {
        "key": "legs_solved",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_low",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_high",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_answer",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess_low",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess_high",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "leg",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn_in_leg",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "seat1_code_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat1_code_high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat2_code_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat2_code_high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "legs",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "turns_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_turns",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tile_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tile_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "possible_codes",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "guess_score_base",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "sum_low_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "sum_middle_min",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "sum_middle_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "sum_high_min",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "sum_high_max",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "gap_pair",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gap_adjacent",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "gap_apart_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "big_tile_min",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "edge_tile_low",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "edge_tile_high",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "wrong_guess_cost",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tie_break_weight",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seats and scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "legs_solved",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first leg, first turn",
      "do": [
        {
          "set": {
            "key": "leg",
            "value": 1
          }
        },
        {
          "set": {
            "key": "turn_in_leg",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the rules",
      "to": "all",
      "text": "Break the Code: {legs} legs of {turns_per_leg} turns ({total_turns} turns). Each leg you hide one of the {possible_codes} two-tile codes (tiles {tile_min}-{tile_max}, low-high). Each turn ask Sum, Odd, Gap, Big or Edge about your opponent's code, or guess it. A correct guess scores {guess_score_base} minus the turn number; a wrong guess scores 0 and tells you how many guessed tiles appear in the code."
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
      "phase": "turn",
      "label": "new leg reset",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "solved",
            "value": false,
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_action",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_answer",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_pick",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "act",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "code",
      "label": "choose your secret code",
      "when": {
        "calc": "turn_in_leg == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "0-0",
          "0-1",
          "0-2",
          "0-3",
          "0-4",
          "0-5",
          "1-1",
          "1-2",
          "1-3",
          "1-4",
          "1-5",
          "2-2",
          "2-3",
          "2-4",
          "2-5",
          "3-3",
          "3-4",
          "3-5",
          "4-4",
          "4-5",
          "5-5"
        ]
      },
      "store": "code_pick",
      "text": "Leg {leg} begins. Choose your secret code for this leg (low tile - high tile). Your opponent will not see it, and it cannot be changed during the leg."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "record the codes",
      "when": {
        "calc": "turn_in_leg == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "code_low",
            "value": {
              "calc": "int(you.code_pick[0])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_high",
            "value": {
              "calc": "int(you.code_pick[2])"
            }
          }
        },
        {
          "set": {
            "key": "seat1_code_low",
            "value": {
              "calc": "players[0].code_low"
            }
          }
        },
        {
          "set": {
            "key": "seat1_code_high",
            "value": {
              "calc": "players[0].code_high"
            }
          }
        },
        {
          "set": {
            "key": "seat2_code_low",
            "value": {
              "calc": "players[1].code_low"
            }
          }
        },
        {
          "set": {
            "key": "seat2_code_high",
            "value": {
              "calc": "players[1].code_high"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "text": "Leg {leg}, turn {turn_in_leg}. Your code and standing:"
    },
    {
      "use": "poll",
      "phase": "turn",
      "label": "choose your action this turn",
      "to": {
        "where": "not you.solved"
      },
      "answer": {
        "type": "choice",
        "options": [
          "sum",
          "odd",
          "gap",
          "big",
          "edge",
          "guess 0-0",
          "guess 0-1",
          "guess 0-2",
          "guess 0-3",
          "guess 0-4",
          "guess 0-5",
          "guess 1-1",
          "guess 1-2",
          "guess 1-3",
          "guess 1-4",
          "guess 1-5",
          "guess 2-2",
          "guess 2-3",
          "guess 2-4",
          "guess 2-5",
          "guess 3-3",
          "guess 3-4",
          "guess 3-5",
          "guess 4-4",
          "guess 4-5",
          "guess 5-5"
        ]
      },
      "store": "act",
      "text": "Leg {leg}, turn {turn_in_leg}. Pick one action about your opponent's code: sum (LOW 0-3, MIDDLE 4-6, HIGH 7-10), odd (how many odd tiles), gap (PAIR, ADJACENT, APART), big (how many tiles are 3 or more), edge (how many tiles are 0 or 5), or guess a full code. A correct guess now scores {guess_score_base} minus {turn_in_leg}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "record the actions",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.solved"
            },
            "key": "last_action",
            "value": "solved"
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved"
            },
            "key": "last_action",
            "value": {
              "calc": "you.act"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_answer",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and len(you.act) == 9"
            },
            "key": "guess_low",
            "value": {
              "calc": "int(you.act[6])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and len(you.act) == 9"
            },
            "key": "guess_high",
            "value": {
              "calc": "int(you.act[8])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "answer the actions",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == 1 and not you.solved"
            },
            "key": "last_answer",
            "value": {
              "calc": "(('LOW' if seat2_code_low + seat2_code_high <= sum_low_max else ('MIDDLE' if seat2_code_low + seat2_code_high <= sum_middle_max else 'HIGH')) if you.act == 'sum' else (['0', '1', '2'][seat2_code_low % 2 + seat2_code_high % 2] if you.act == 'odd' else (('PAIR' if seat2_code_high - seat2_code_low == gap_pair else ('ADJACENT' if seat2_code_high - seat2_code_low == gap_adjacent else 'APART')) if you.act == 'gap' else (['0', '1', '2'][count(t >= big_tile_min for t in [seat2_code_low, seat2_code_high])] if you.act == 'big' else (['0', '1', '2'][count(t == edge_tile_low or t == edge_tile_high for t in [seat2_code_low, seat2_code_high])] if you.act == 'edge' else ('CORRECT' if you.guess_low == seat2_code_low and you.guess_high == seat2_code_high else 'WRONG, tiles matching: ' + ['0', '1', '2'][(count(t == you.guess_low for t in [seat2_code_low, seat2_code_high]) if you.guess_low == you.guess_high else count(g in [seat2_code_low, seat2_code_high] for g in [you.guess_low, you.guess_high]))]))))))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2 and not you.solved"
            },
            "key": "last_answer",
            "value": {
              "calc": "(('LOW' if seat1_code_low + seat1_code_high <= sum_low_max else ('MIDDLE' if seat1_code_low + seat1_code_high <= sum_middle_max else 'HIGH')) if you.act == 'sum' else (['0', '1', '2'][seat1_code_low % 2 + seat1_code_high % 2] if you.act == 'odd' else (('PAIR' if seat1_code_high - seat1_code_low == gap_pair else ('ADJACENT' if seat1_code_high - seat1_code_low == gap_adjacent else 'APART')) if you.act == 'gap' else (['0', '1', '2'][count(t >= big_tile_min for t in [seat1_code_low, seat1_code_high])] if you.act == 'big' else (['0', '1', '2'][count(t == edge_tile_low or t == edge_tile_high for t in [seat1_code_low, seat1_code_high])] if you.act == 'edge' else ('CORRECT' if you.guess_low == seat1_code_low and you.guess_high == seat1_code_high else 'WRONG, tiles matching: ' + ['0', '1', '2'][(count(t == you.guess_low for t in [seat1_code_low, seat1_code_high]) if you.guess_low == you.guess_high else count(g in [seat1_code_low, seat1_code_high] for g in [you.guess_low, you.guess_high]))]))))))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "score",
            "value": {
              "calc": "guess_score_base - turn_in_leg"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "legs_solved",
            "value": 1
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "solved",
            "value": true,
            "text": "Seat {player} has solved leg {leg}."
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "the answers",
      "to": "all",
      "text": "Leg {leg}, turn {turn_in_leg}. Seat 1: {players[0].last_action} -> {players[0].last_answer}. Seat 2: {players[1].last_action} -> {players[1].last_answer}. Scores: {players[0].score} / {players[1].score}."
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "reveal the codes",
      "when": {
        "calc": "turn_in_leg == turns_per_leg"
      },
      "to": "all",
      "text": "Leg {leg} is over. Seat 1's code was {seat1_code_low}-{seat1_code_high}; Seat 2's code was {seat2_code_low}-{seat2_code_high}. A leg nobody solved scores nothing."
    },
    {
      "use": "update",
      "phase": "leg end",
      "label": "advance the turn",
      "do": [
        {
          "adjust": {
            "key": "leg",
            "value": 1,
            "if": {
              "calc": "turn_in_leg >= turns_per_leg"
            }
          }
        },
        {
          "set": {
            "key": "turn_in_leg",
            "value": {
              "calc": "1 if turn_in_leg >= turns_per_leg else turn_in_leg + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "leg end",
      "label": "after the last leg",
      "when": {
        "calc": "leg > legs"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "leg > legs"
      },
      "rank_by": "you.score * 10 + you.legs_solved",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score} ({players[0].legs_solved} legs solved), Seat 2 {players[1].score} ({players[1].legs_solved} legs solved)."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "The match is {legs} legs of {turns_per_leg} turns each ({total_turns} turns in all). Scores start at {starting_score}.\n\nCODES. At the start of each leg (turn 1), both players at the same moment secretly choose a code of two tiles. Each tile is a whole number from {tile_min} to {tile_max}. A code is written low tile then high tile, with low no greater than high; equal tiles are allowed, for example 3-3. There are {possible_codes} possible codes. A code cannot be changed during the leg.\n\nTURNS. On each turn of a leg, both players choose at the same moment. Each picks exactly one of the following actions, about the opponent's code:\n- sum: is the sum of the two tiles LOW (0-{sum_low_max}), MIDDLE ({sum_middle_min}-{sum_middle_max}) or HIGH ({sum_high_min}-{sum_high_max})?\n- odd: how many tiles are odd: 0, 1 or 2?\n- gap: is high minus low {gap_pair} (PAIR), {gap_adjacent} (ADJACENT) or {gap_apart_min} or more (APART)?\n- big: how many tiles are {big_tile_min} or more: 0, 1 or 2?\n- edge: how many tiles are {edge_tile_low} or {edge_tile_high}: 0, 1 or 2?\n- guess: name a full code (low, high).\nRepeating a question is allowed, but it gives the same answer again.\n\nANSWERS. After both have chosen, both players are told each player's action and its truthful answer, computed from the opponent's code.\n- If a guess equals the opponent's code exactly, it is CORRECT. The guesser scores {guess_score_base} minus the turn number within the leg: 6 points on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5 and 1 on turn 6.\n- If a guess is wrong, it scores 0 and costs nothing else ({wrong_guess_cost}). The answer is WRONG with how many of the guessed tiles appear in the code, which is 0 or 1. Each code tile can match at most one guessed tile (guess 3-3 against code 3-4 answers 1; guess 1-2 against code 3-4 answers 0).\n\nSOLVED. A player who guesses correctly has solved the leg: their legs solved count goes up by 1, and for the rest of that leg they are not asked for an action and score nothing more. The other player keeps playing normally.\n\nEND OF LEG. After turn {turns_per_leg} of a leg, both codes are revealed to both players. Unsolved legs score nothing for anyone. The next leg starts with new codes.\n\nEND OF MATCH. After {legs} legs the match ends. The player with the higher total score wins. If totals are equal, the player who solved more legs wins. If that is also equal, the match is a draw (shared win)."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state shown to players has empty fields (act, last_action, last_answer, last_action) in `your_standing`; hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "break_the_code_duel",
    "name": "Break the Code: Duel of Two Tiles",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Hide a two-tile code each leg, ask property questions or guess your opponent's code; earlier correct guesses score more over 4 legs of 6 turns."
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
      },
      {
        "key": "legs_solved",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_low",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_high",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "last_action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "last_answer",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "guess_low",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guess_high",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code_pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "leg",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "turn_in_leg",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "seat1_code_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat1_code_high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat2_code_low",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "seat2_code_high",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "legs",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "turns_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "total_turns",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tile_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tile_max",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "possible_codes",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "guess_score_base",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "sum_low_max",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "sum_middle_min",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "sum_middle_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "sum_high_min",
        "visible": "public",
        "type": "number",
        "initial": 7
      },
      {
        "key": "sum_high_max",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "gap_pair",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "gap_adjacent",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "gap_apart_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "big_tile_min",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "edge_tile_low",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "edge_tile_high",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "wrong_guess_cost",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tie_break_weight",
        "visible": "public",
        "type": "number",
        "initial": 10
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seats and scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "starting_score"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "legs_solved",
            "value": 0
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "first leg, first turn",
      "do": [
        {
          "set": {
            "key": "leg",
            "value": 1
          }
        },
        {
          "set": {
            "key": "turn_in_leg",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the rules",
      "to": "all",
      "text": "Break the Code: {legs} legs of {turns_per_leg} turns ({total_turns} turns). Each leg you hide one of the {possible_codes} two-tile codes (tiles {tile_min}-{tile_max}, low-high). Each turn ask Sum, Odd, Gap, Big or Edge about your opponent's code, or guess it. A correct guess scores {guess_score_base} minus the turn number; a wrong guess scores 0 and tells you how many guessed tiles appear in the code."
    },
    {
      "use": "sync",
      "label": "the table",
      "mode": "self",
      "to": "all",
      "fields": [
        "score",
        "legs_solved"
      ],
      "text": "You start with:"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "turn",
      "label": "new leg reset",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "solved",
            "value": false,
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_action",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_answer",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_pick",
            "value": "",
            "if": {
              "calc": "turn_in_leg == 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "act",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "code",
      "label": "choose your secret code",
      "when": {
        "calc": "turn_in_leg == 1"
      },
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": [
          "0-0",
          "0-1",
          "0-2",
          "0-3",
          "0-4",
          "0-5",
          "1-1",
          "1-2",
          "1-3",
          "1-4",
          "1-5",
          "2-2",
          "2-3",
          "2-4",
          "2-5",
          "3-3",
          "3-4",
          "3-5",
          "4-4",
          "4-5",
          "5-5"
        ]
      },
      "store": "code_pick",
      "text": "Leg {leg} begins. Choose your secret code for this leg (low tile - high tile). Your opponent will not see it, and it cannot be changed during the leg."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "record the codes",
      "when": {
        "calc": "turn_in_leg == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "code_low",
            "value": {
              "calc": "int(you.code_pick[0])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_high",
            "value": {
              "calc": "int(you.code_pick[2])"
            }
          }
        },
        {
          "set": {
            "key": "seat1_code_low",
            "value": {
              "calc": "players[0].code_low"
            }
          }
        },
        {
          "set": {
            "key": "seat1_code_high",
            "value": {
              "calc": "players[0].code_high"
            }
          }
        },
        {
          "set": {
            "key": "seat2_code_low",
            "value": {
              "calc": "players[1].code_low"
            }
          }
        },
        {
          "set": {
            "key": "seat2_code_high",
            "value": {
              "calc": "players[1].code_high"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "phase": "turn",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "fields": [
        "code_low",
        "code_high",
        "score",
        "legs_solved"
      ],
      "text": "Leg {leg}, turn {turn_in_leg}. Your code and standing:"
    },
    {
      "use": "poll",
      "phase": "turn",
      "label": "choose your action this turn",
      "to": {
        "where": "not you.solved"
      },
      "answer": {
        "type": "choice",
        "options": [
          "sum",
          "odd",
          "gap",
          "big",
          "edge",
          "guess 0-0",
          "guess 0-1",
          "guess 0-2",
          "guess 0-3",
          "guess 0-4",
          "guess 0-5",
          "guess 1-1",
          "guess 1-2",
          "guess 1-3",
          "guess 1-4",
          "guess 1-5",
          "guess 2-2",
          "guess 2-3",
          "guess 2-4",
          "guess 2-5",
          "guess 3-3",
          "guess 3-4",
          "guess 3-5",
          "guess 4-4",
          "guess 4-5",
          "guess 5-5"
        ]
      },
      "store": "act",
      "text": "Leg {leg}, turn {turn_in_leg}. Pick one action about your opponent's code: sum (LOW 0-3, MIDDLE 4-6, HIGH 7-10), odd (how many odd tiles), gap (PAIR, ADJACENT, APART), big (how many tiles are 3 or more), edge (how many tiles are 0 or 5), or guess a full code. A correct guess now scores {guess_score_base} minus {turn_in_leg}."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "record the actions",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.solved"
            },
            "key": "last_action",
            "value": "solved"
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved"
            },
            "key": "last_action",
            "value": {
              "calc": "you.act"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "last_answer",
            "value": ""
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and len(you.act) == 9"
            },
            "key": "guess_low",
            "value": {
              "calc": "int(you.act[6])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and len(you.act) == 9"
            },
            "key": "guess_high",
            "value": {
              "calc": "int(you.act[8])"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "answer the actions",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.seat == 1 and not you.solved"
            },
            "key": "last_answer",
            "value": {
              "calc": "(('LOW' if seat2_code_low + seat2_code_high <= sum_low_max else ('MIDDLE' if seat2_code_low + seat2_code_high <= sum_middle_max else 'HIGH')) if you.act == 'sum' else (['0', '1', '2'][seat2_code_low % 2 + seat2_code_high % 2] if you.act == 'odd' else (('PAIR' if seat2_code_high - seat2_code_low == gap_pair else ('ADJACENT' if seat2_code_high - seat2_code_low == gap_adjacent else 'APART')) if you.act == 'gap' else (['0', '1', '2'][count(t >= big_tile_min for t in [seat2_code_low, seat2_code_high])] if you.act == 'big' else (['0', '1', '2'][count(t == edge_tile_low or t == edge_tile_high for t in [seat2_code_low, seat2_code_high])] if you.act == 'edge' else ('CORRECT' if you.guess_low == seat2_code_low and you.guess_high == seat2_code_high else 'WRONG, tiles matching: ' + ['0', '1', '2'][(count(t == you.guess_low for t in [seat2_code_low, seat2_code_high]) if you.guess_low == you.guess_high else count(g in [seat2_code_low, seat2_code_high] for g in [you.guess_low, you.guess_high]))]))))))"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == 2 and not you.solved"
            },
            "key": "last_answer",
            "value": {
              "calc": "(('LOW' if seat1_code_low + seat1_code_high <= sum_low_max else ('MIDDLE' if seat1_code_low + seat1_code_high <= sum_middle_max else 'HIGH')) if you.act == 'sum' else (['0', '1', '2'][seat1_code_low % 2 + seat1_code_high % 2] if you.act == 'odd' else (('PAIR' if seat1_code_high - seat1_code_low == gap_pair else ('ADJACENT' if seat1_code_high - seat1_code_low == gap_adjacent else 'APART')) if you.act == 'gap' else (['0', '1', '2'][count(t >= big_tile_min for t in [seat1_code_low, seat1_code_high])] if you.act == 'big' else (['0', '1', '2'][count(t == edge_tile_low or t == edge_tile_high for t in [seat1_code_low, seat1_code_high])] if you.act == 'edge' else ('CORRECT' if you.guess_low == seat1_code_low and you.guess_high == seat1_code_high else 'WRONG, tiles matching: ' + ['0', '1', '2'][(count(t == you.guess_low for t in [seat1_code_low, seat1_code_high]) if you.guess_low == you.guess_high else count(g in [seat1_code_low, seat1_code_high] for g in [you.guess_low, you.guess_high]))]))))))"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "score",
            "value": {
              "calc": "guess_score_base - turn_in_leg"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "legs_solved",
            "value": 1
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.solved and you.last_answer == 'CORRECT'"
            },
            "key": "solved",
            "value": true,
            "text": "Seat {player} has solved leg {leg}."
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "the answers",
      "to": "all",
      "text": "Leg {leg}, turn {turn_in_leg}. Seat 1: {players[0].last_action} -> {players[0].last_answer}. Seat 2: {players[1].last_action} -> {players[1].last_answer}. Scores: {players[0].score} / {players[1].score}."
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "reveal the codes",
      "when": {
        "calc": "turn_in_leg == turns_per_leg"
      },
      "to": "all",
      "text": "Leg {leg} is over. Seat 1's code was {seat1_code_low}-{seat1_code_high}; Seat 2's code was {seat2_code_low}-{seat2_code_high}. A leg nobody solved scores nothing."
    },
    {
      "use": "update",
      "phase": "leg end",
      "label": "advance the turn",
      "do": [
        {
          "adjust": {
            "key": "leg",
            "value": 1,
            "if": {
              "calc": "turn_in_leg >= turns_per_leg"
            }
          }
        },
        {
          "set": {
            "key": "turn_in_leg",
            "value": {
              "calc": "1 if turn_in_leg >= turns_per_leg else turn_in_leg + 1"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "leg end",
      "label": "after the last leg",
      "when": {
        "calc": "leg > legs"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "leg > legs"
      },
      "rank_by": "you.score * 10 + you.legs_solved",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score} ({players[0].legs_solved} legs solved), Seat 2 {players[1].score} ({players[1].legs_solved} legs solved)."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "The match is {legs} legs of {turns_per_leg} turns each ({total_turns} turns in all). Scores start at {starting_score}.\n\nCODES. At the start of each leg (turn 1), both players at the same moment secretly choose a code of two tiles. Each tile is a whole number from {tile_min} to {tile_max}. A code is written low tile then high tile, with low no greater than high; equal tiles are allowed, for example 3-3. There are {possible_codes} possible codes. A code cannot be changed during the leg.\n\nTURNS. On each turn of a leg, both players choose at the same moment. Each picks exactly one of the following actions, about the opponent's code:\n- sum: is the sum of the two tiles LOW (0-{sum_low_max}), MIDDLE ({sum_middle_min}-{sum_middle_max}) or HIGH ({sum_high_min}-{sum_high_max})?\n- odd: how many tiles are odd: 0, 1 or 2?\n- gap: is high minus low {gap_pair} (PAIR), {gap_adjacent} (ADJACENT) or {gap_apart_min} or more (APART)?\n- big: how many tiles are {big_tile_min} or more: 0, 1 or 2?\n- edge: how many tiles are {edge_tile_low} or {edge_tile_high}: 0, 1 or 2?\n- guess: name a full code (low, high).\nRepeating a question is allowed, but it gives the same answer again.\n\nANSWERS. After both have chosen, both players are told each player's action and its truthful answer, computed from the opponent's code.\n- If a guess equals the opponent's code exactly, it is CORRECT. The guesser scores {guess_score_base} minus the turn number within the leg: 6 points on turn 1, 5 on turn 2, 4 on turn 3, 3 on turn 4, 2 on turn 5 and 1 on turn 6.\n- If a guess is wrong, it scores 0 and costs nothing else ({wrong_guess_cost}). The answer is WRONG with how many of the guessed tiles appear in the code, which is 0 or 1. Each code tile can match at most one guessed tile (guess 3-3 against code 3-4 answers 1; guess 1-2 against code 3-4 answers 0).\n\nSOLVED. A player who guesses correctly has solved the leg: their legs solved count goes up by 1, and for the rest of that leg they are not asked for an action and score nothing more. The other player keeps playing normally.\n\nEND OF LEG. After turn {turns_per_leg} of a leg, both codes are revealed to both players. Unsolved legs score nothing for anyone. The next leg starts with new codes.\n\nEND OF MATCH. After {legs} legs the match ends. The player with the higher total score wins. If totals are equal, the player who solved more legs wins. If that is also equal, the match is a draw (shared win)."
}
```
````
