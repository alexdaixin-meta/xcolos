# 14 coder

- time: 2026-10-27T18:35:51+00:00 (93.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 b3c265b7725a9954, reply sha256 d7fb11b013e0510a

## Sent

````
# Task: write the XColos game file for "Break the Code: Three-Leg Duel"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

OVERVIEW. Two players. The match has 3 legs of 4 rounds each (12 rounds in total). Leg 1 is rounds 1-4, leg 2 is rounds 5-8, leg 3 is rounds 9-12. The leg-round is 1, 2, 3 or 4 within each leg. Scores start at 0 and carry across legs.

CODES. A code is three different digits from 0 to 9, kept smallest first as A < B < C. Example: 2-5-8.

THE SIX QUESTION CARDS. Each answer is one number computed from the opponent's current code A < B < C.
1 SUM: A + B + C.
2 EVENS: how many of the three digits are even (0 counts as even).
3 RANGE: C - A.
4 HIGH: how many of the three digits are 5 or more.
5 STEPS: how many of the pairs (A,B) and (B,C) differ by exactly 1 (0, 1 or 2).
6 THREES: how many of the three digits are in {0, 3, 6, 9}.

EACH ROUND:

Step 1. Code choice (leg-round 1 only, i.e. rounds 1, 5, 9).
- Both players simultaneously and secretly write a code.
- Three different digits written in any order are sorted ascending and become that player's code for this leg.
- Any other entry (repeated digits, wrong count, non-digits, blank) becomes the code 0-1-2.
- Only the engine knows the codes.
- Each player's guesses for the leg are set to 2, their solved flag to no, and their used cards to none.

Step 2. Ask. Both players simultaneously and secretly name one card number (1-6) they have not used in this leg.
- If a player names nothing, an invalid number, or a card already used this leg, they are given the lowest-numbered card they have not used this leg.
- The card becomes used for that player until the leg ends.
- Each player uses exactly 4 different cards per leg; all six are available again at the start of the next leg.

Step 3. Answer. The engine computes each player's card from the opponent's code. It announces to both players which card each player asked and the answer.

Step 4. Guess. Both players simultaneously either pass or write a code guess.
- A guess of three different digits in any order is sorted ascending.
- Any other entry counts as a pass.
- A guess written by a player with 0 guesses left, or who has already guessed correctly this leg, counts as a pass.
- A pass costs nothing.
- A valid guess uses up 1 of that player's guesses for the leg.

Step 5. Check. Each valid guess is compared with the opponent's code.
- Correct (all three digits match): the guesser scores 5 minus the leg-round, so 4 points in leg-round 1, 3 in leg-round 2, 2 in leg-round 3, 1 in leg-round 4. The guesser is marked solved for the rest of the leg and makes no further guesses that leg.
- Wrong: the guesser loses 1 point and also gains 1 to their wrong-guess count.
- Every guess and its result (correct or wrong) is announced to both players.
- One player guessing correctly does not end the leg for the other player, who may keep asking and guessing.

Step 6. Leg end (leg-round 4 only, i.e. rounds 4, 8, 12). Both codes are revealed to both players, and the current scores are announced.

Step 7. End check. After round 12 the match ends.

ENGINE ENCODING (for builders):
- Per player: score, wrong_count, guesses_left, solved (0/1), used_mask, code (100A+10B+C), ask, answer, guess (100A+10B+C, or 0 for a pass).
- Plus one table attribute: round.
- Total: 17 attributes.
- Leg-round is ((round - 1) mod 4) + 1.
- Digits of a code are A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10.
- Card n is used if floor(used_mask / 2^(n-1)) mod 2 = 1.

How the winner is decided: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Break the Code: Three-Leg Duel (2 to 2 players, best with 2)

Two players each hide a three-digit code. Over three legs of four rounds they ask the same number-question cards at the same time and score points for cracking the opponent's code early.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points across all legs.
  - each player: wrong_count (number, starts 0); everyone sees it. Wrong guesses over the whole match; used as the tie-break (fewer is better).
  - each player: guesses_left (number, starts 2); everyone sees it. Valid guesses still allowed in this leg; reset to 2 at leg-round 1.
  - each player: solved (number, starts 0); everyone sees it. 1 if the player has guessed the opponent's code correctly this leg, else 0.
  - each player: used_mask (number, starts 0); everyone sees it. Bitmask of cards used this leg. Card n is used if floor(used_mask / 2^(n-1)) mod 2 = 1.
  - each player: code (number, starts 12); only its owner sees it. The player's secret code for this leg, written as 100A+10B+C with A<B<C. The opponent never sees it until the leg ends.
  - each player: ask (number, starts 0); everyone sees it. The card (1-6) the player asked this round.
  - each player: answer (number, starts 0); everyone sees it. The value of the asked card, computed from the opponent's code.
  - each player: guess (number, starts 0); everyone sees it. This round's guess as 100A+10B+C, or 0 for a pass.
  - the table: round (number, starts 0); everyone sees it. Current round, 1-12. Leg-round = ((round - 1) mod 4) + 1.
  - parameters, each kept as a table attribute: legs = 3, rounds_per_leg = 4, total_rounds = 12, digit_min = 0, digit_max = 9, code_length = 3, default_code = 12, question_cards = 6, cards_used_per_leg = 4, guesses_per_leg = 2, correct_score_base = 5, wrong_guess_penalty = 1, high_digit_threshold = 5, pass_value = 0, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat two players.
  2. Set every player's score and wrong_count to 0.
  3. Set round to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. Leg-round L = ((round - 1) mod 4) + 1.
  2. [poll] all players (only when L = 1, i.e. rounds 1, 5, 9) answers: short text: three different digits 0-9 in any order. What happens: Three different digits are sorted ascending and stored as code = 100A+10B+C. Any other entry sets code = 12 (0-1-2). Then guesses_left = 2, solved = 0, used_mask = 0. Each player's code is visible only to its owner.
  3. [sync] all players. What happens: Each player receives their own state: code, guesses_left, solved, used_mask, score.
  4. [poll] all players answers: choice of one card number from 1-6 not yet used this leg. What happens: ask = the chosen card. If the answer is missing or invalid, ask = the lowest card n with floor(used_mask/2^(n-1)) mod 2 = 0. Then used_mask += 2^(ask-1).
  5. [update] all players. What happens: For each player, with the opponent's code digits A = floor(code/100), B = floor(code/10) mod 10, C = code mod 10: answer = A+B+C if ask=1; count of digits with d mod 2 = 0 if ask=2; C-A if ask=3; count of digits >= 5 if ask=4; (B-A=1)+(C-B=1) if ask=5; count of digits with d mod 3 = 0 if ask=6. Announce to both players each player's ask and answer.
  6. [poll] all players answers: short text: 'pass' or three different digits 0-9 in any order. What happens: If the entry is three different digits AND guesses_left > 0 AND solved = 0, guess = the sorted code as 100A+10B+C and guesses_left -= 1. Otherwise guess = 0 (a pass).
  7. [update] all players. What happens: For each player with guess > 0: if guess = opponent's code, score += 5 - L and solved = 1; otherwise score -= 1 and wrong_count += 1. Announce every guess and its result (correct or wrong) to both players.
  8. [tell] all players (only when L = 4, i.e. rounds 4, 8, 12). What happens: Reveal both players' code to both players and announce the current score of each player.
  9. [check] all players. What happens: If round >= 12, end the game; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. The match has 12 rounds in 3 legs of 4 rounds each; leg-round = ((round - 1) mod 4) + 1.
  R2. Scores start at 0 and carry across legs.
  R3. When leg-round is 1 (rounds 1, 5, 9), both players secretly and simultaneously write a code.
  R4. When a code entry has three different digits in any order (e.g. 8,2,5), then it is sorted ascending and stored as code 258.
  R5. When a code entry is invalid (repeated digits, wrong count, non-digits, blank), then the code becomes 0-1-2 (code = 12).
  R6. When a leg starts, each player's guesses_left is set to 2, solved to 0 and used_mask to 0.
  R7. Each round, both players simultaneously name one card 1-6 not used this leg; that card becomes used until the leg ends.
  R8. When a player names nothing, an invalid number or an already used card, then they are given the lowest-numbered unused card.
  R9. Card 1 SUM answers A+B+C of the opponent's code (e.g. 2-5-8 gives 15).
  R10. Card 2 EVENS answers how many of the opponent's digits are even, with 0 counting as even (e.g. 2-5-8 gives 2).
  R11. Card 3 RANGE answers C-A (e.g. 2-5-8 gives 6).
  R12. Card 4 HIGH answers how many digits are 5 or more (e.g. 2-5-8 gives 2).
  R13. Card 5 STEPS answers how many of the pairs (A,B), (B,C) differ by exactly 1 (e.g. 3-4-5 gives 2, 2-5-8 gives 0).
  R14. Card 6 THREES answers how many digits are in {0,3,6,9} (e.g. 0-3-7 gives 2).
  R15. After asking, the engine announces to both players which card each player asked and its answer.
  R16. Each round, both players simultaneously pass or write a guess; a guess of three different digits is sorted ascending.
  R17. When a guess entry is not three different digits, or the guesser has guesses_left = 0, or solved = 1, then it counts as a pass and costs nothing.
  R18. When a valid guess is made, then the guesser's guesses_left decreases by 1.
  R19. When a valid guess equals the opponent's code, then the guesser scores 5 - leg-round (4, 3, 2, 1 in leg-rounds 1-4) and solved = 1 for the rest of the leg.
  R20. When a valid guess does not equal the opponent's code, then the guesser loses 1 point and wrong_count increases by 1.
  R21. Every guess and its result (correct or wrong) is announced to both players.
  R22. When one player guesses correctly, the other player still keeps asking and guessing in that leg.
  R23. When leg-round is 4 (rounds 4, 8, 12), both codes are revealed to both players and the scores are announced.
  R24. When round 12 is finished, the match ends; the higher score wins, then fewer wrong guesses, else a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Code choice (leg-round 1 only) | asked: both seats | options: free short text; three different digits are expected, and anything else becomes 0-1-2
  - Ask a card | asked: both seats | options: each card number 1-6 that seat has not used this leg (4 options in leg-round 2, 3 in leg-round 3, the remaining 3 in leg-round 4 as cards run down: 6, 5, 4, 3 options in leg-rounds 1-4)
  - Guess | asked: both seats | options: a seat with guesses_left > 0 and solved = 0: 'pass' or a three-digit code in free text; a seat with guesses_left = 0 or solved = 1: pass only

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.score * 100 - you.wrong_count (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest total score wins. If scores are equal, the player with fewer wrong guesses over the match wins. If both are equal, both share the win (a draw).
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

- each player: `score` (number, visible: public, starts 0): Total points across all legs.
- each player: `wrong_count` (number, visible: public, starts 0): Wrong guesses over the whole match; used as the tie-break (fewer is better).
- the table: `round` (number, visible: public, starts 0): Current round, 1-12. Leg-round = ((round - 1) mod 4) + 1.
- parameters (each must be an attribute holding this value, never a number buried in a step): legs = 3, rounds_per_leg = 4, total_rounds = 12, digit_min = 0, digit_max = 9, code_length = 3, default_code = 12, question_cards = 6, cards_used_per_leg = 4, guesses_per_leg = 2, correct_score_base = 5, wrong_guess_penalty = 1, high_digit_threshold = 5, pass_value = 0, starting_score = 0
- the game ends with ONE ending whose `rank_by` is `you.score * 100 - you.wrong_count`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

1) Accept guesses and code entries as entries of three different digits in any order, sort them ascending, and store them as 100A+10B+C. If you use an option list, it must contain every valid code: all 120 sorted codes, plus the unsorted spellings, or a free-text entry that the game parses. Never narrow the guess options to codes consistent with the answers so far; the player decides, and a wrong guess must still cost 1 point and add 1 to wrong_count. 2) Any code entry that is not three different digits, including a blank, must become code 12 (0-1-2) rather than being refused or left unchanged. 3) Advance round by exactly 1 per round, starting from 0 so that round 1 is the first round, and compute leg-round as ((round-1) mod 4)+1 from that value. 4) At leg-round 1, read the code from the entry and reset guesses_left to guesses_per_leg, solved to 0 and used_mask to 0 for both players, so that a seat that ran out of guesses in the previous leg can guess again. 5) Score a correct guess as correct_score_base minus leg-round, and a wrong guess as minus wrong_guess_penalty with wrong_count plus 1, all read from the parameter attributes.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "break_the_code_three_leg_duel",
    "name": "Break the Code: Three-Leg Duel",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players hide three-digit codes, ask number-question cards at the same time, and score for cracking the opponent's code early over three legs."
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
        "key": "wrong_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guesses_left",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "used_mask",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code",
        "visible": "ally",
        "type": "number",
        "initial": 12
      },
      {
        "key": "ask",
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
        "key": "guess",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "entry",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "pick",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "digits",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "code_digits",
        "visible": "ally",
        "type": "list",
        "initial": [
          0,
          1,
          2
        ]
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
        "key": "leg_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "legs",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "digit_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "digit_max",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "default_code",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "question_cards",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_used_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "guesses_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "correct_score_base",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "wrong_guess_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "high_digit_threshold",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "pass_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6"
        ]
      },
      {
        "key": "card_bits",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          4,
          8,
          16,
          32
        ]
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting scores",
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
            "key": "wrong_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
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
      "use": "update",
      "phase": "start",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_round",
            "value": {
              "calc": "(round - 1) % rounds_per_leg + 1"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "entry",
            "value": ""
          }
        }
      ],
      "text": "Round {round} of {total_rounds} begins (leg-round {leg_round} of {rounds_per_leg})."
    },
    {
      "use": "poll",
      "phase": "code",
      "label": "code choice",
      "when": {
        "calc": "leg_round == 1"
      },
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 60
      },
      "store": "entry",
      "text": "A new leg begins. Secretly write your code: three different digits from {digit_min} to {digit_max}, in any order (for example 8 2 5). They are sorted smallest first. Any other entry becomes the code 0-1-2."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "codes are set",
      "when": {
        "calc": "leg_round == 1"
      },
      "do": [
        {
          "set": {
            "players": "all",
            "key": "digits",
            "value": {
              "calc": "sorted([int(ch) for ch in you.entry if ch in '0123456789'])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code",
            "value": {
              "calc": "default_code if len(you.digits) != code_length else ((100 * you.digits[0] + 10 * you.digits[1] + you.digits[2]) if (you.digits[0] < you.digits[1] and you.digits[1] < you.digits[2]) else default_code)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "code_digits",
            "value": {
              "calc": "[int(you.code / 100), int(you.code / 10) % 10, you.code % 10]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guesses_left",
            "value": {
              "calc": "guesses_per_leg"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "solved",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "used_mask",
            "value": 0
          }
        }
      ],
      "text": "Both codes are set for this leg. Each player has {guesses_per_leg} guesses and all {question_cards} cards available."
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "fields": [
        "code",
        "guesses_left",
        "solved",
        "used_mask",
        "score"
      ],
      "text": "Your state:"
    },
    {
      "use": "update",
      "phase": "ask",
      "label": "cards on offer",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "pick",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in card_labels if int(you.used_mask / card_bits[int(c) - 1]) % 2 == 0]"
            }
          }
        }
      ]
    },
    {
      "use": "poll",
      "phase": "ask",
      "label": "ask a card",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "store": "pick",
      "text": "Secretly name one question card you have not used this leg: 1 SUM (A+B+C), 2 EVENS (how many digits are even, 0 counts), 3 RANGE (C-A), 4 HIGH (how many digits are {high_digit_threshold} or more), 5 STEPS (how many of the pairs A,B and B,C differ by exactly 1), 6 THREES (how many digits are 0, 3, 6 or 9). It is answered from your opponent's code."
    },
    {
      "use": "update",
      "phase": "answer",
      "label": "the answers",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "ask",
            "value": {
              "calc": "int(you.pick) if you.pick in you.offer else min([int(c) for c in you.offer])"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "used_mask",
            "value": {
              "calc": "card_bits[you.ask - 1]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "answer",
            "value": {
              "calc": "sum([p.code_digits for p in players if p.seat != you.seat][0]) if you.ask == 1 else (count(d % 2 == 0 for d in [p.code_digits for p in players if p.seat != you.seat][0]) if you.ask == 2 else (([p.code_digits for p in players if p.seat != you.seat][0][2] - [p.code_digits for p in players if p.seat != you.seat][0][0]) if you.ask == 3 else (count(d >= high_digit_threshold for d in [p.code_digits for p in players if p.seat != you.seat][0]) if you.ask == 4 else (((1 if [p.code_digits for p in players if p.seat != you.seat][0][1] - [p.code_digits for p in players if p.seat != you.seat][0][0] == 1 else 0) + (1 if [p.code_digits for p in players if p.seat != you.seat][0][2] - [p.code_digits for p in players if p.seat != you.seat][0][1] == 1 else 0)) if you.ask == 5 else count(d % 3 == 0 for d in [p.code_digits for p in players if p.seat != you.seat][0])))))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "entry",
            "value": ""
          }
        }
      ],
      "text": "Seat 1 asked card {players[0].ask} and the answer is {players[0].answer}. Seat 2 asked card {players[1].ask} and the answer is {players[1].answer}."
    },
    {
      "use": "poll",
      "phase": "guess",
      "label": "guess",
      "when": {
        "calc": "count(p.guesses_left > 0 and p.solved == 0 for p in players) > 0"
      },
      "to": {
        "where": "you.guesses_left > 0 and you.solved == 0"
      },
      "answer": {
        "type": "text",
        "max_words": 60
      },
      "store": "entry",
      "text": "Write 'pass', or guess your opponent's code as three different digits in any order. A correct guess scores {correct_score_base} minus the leg-round (now {leg_round}); a wrong guess costs {wrong_guess_penalty} point and adds 1 to your wrong guesses. A pass, or any entry that is not three different digits, costs nothing."
    },
    {
      "use": "update",
      "phase": "guess",
      "label": "read the guesses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "digits",
            "value": {
              "calc": "sorted([int(ch) for ch in you.entry if ch in '0123456789'])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guess",
            "value": {
              "calc": "pass_value if (you.guesses_left <= 0 or you.solved == 1 or len(you.digits) != code_length) else ((100 * you.digits[0] + 10 * you.digits[1] + you.digits[2]) if (you.digits[0] < you.digits[1] and you.digits[1] < you.digits[2]) else pass_value)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.guess > 0"
            },
            "key": "guesses_left",
            "value": -1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "check the guesses",
      "do": [
        {
          "adjust": {
            "players": {
              "where": "you.guess > 0 and you.guess == [p.code for p in players if p.seat != you.seat][0]"
            },
            "key": "score",
            "value": {
              "calc": "correct_score_base - leg_round"
            },
            "text": "Seat {player} guessed the code correctly and scores {value}.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "players": {
              "where": "you.guess > 0 and you.guess == [p.code for p in players if p.seat != you.seat][0]"
            },
            "key": "solved",
            "value": 1
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.guess > 0 and you.guess != [p.code for p in players if p.seat != you.seat][0]"
            },
            "key": "score",
            "value": {
              "calc": "-wrong_guess_penalty"
            },
            "text": "Seat {player} guessed wrong and loses {wrong_guess_penalty} point.",
            "announce_to": "all"
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.guess > 0 and you.guess != [p.code for p in players if p.seat != you.seat][0]"
            },
            "key": "wrong_count",
            "value": 1
          }
        }
      ],
      "text": "Guesses this round (written 100A+10B+C, 0 = pass): seat 1 {players[0].guess}, seat 2 {players[1].guess}."
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "leg end reveal",
      "when": {
        "calc": "leg_round == rounds_per_leg"
      },
      "to": "all",
      "text": "The leg is over. Codes (100A+10B+C): seat 1 {players[0].code}, seat 2 {players[1].code}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round 12",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "you.score * 100 - you.wrong_count",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score} ({players[0].wrong_count} wrong guesses), Seat 2 {players[1].score} ({players[1].wrong_count} wrong guesses)."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Two players. The match has {legs} legs of {rounds_per_leg} rounds each ({total_rounds} rounds in total). Leg 1 is rounds 1-4, leg 2 is rounds 5-8, leg 3 is rounds 9-12. The leg-round is 1, 2, 3 or 4 within each leg: leg-round = ((round - 1) mod 4) + 1. Scores start at {starting_score} and carry across legs.\n\nCODES. A code is three different digits from {digit_min} to {digit_max}, kept smallest first as A < B < C (example: 2-5-8). Codes are shown as 100A+10B+C, so 2-5-8 is 258 and 0-1-2 is 12.\n\nTHE SIX QUESTION CARDS. Each answer is one number computed from the opponent's current code A < B < C.\n1 SUM: A + B + C (2-5-8 gives 15).\n2 EVENS: how many of the three digits are even, 0 counts as even (2-5-8 gives 2).\n3 RANGE: C - A (2-5-8 gives 6).\n4 HIGH: how many of the three digits are {high_digit_threshold} or more (2-5-8 gives 2).\n5 STEPS: how many of the pairs (A,B) and (B,C) differ by exactly 1, so 0, 1 or 2 (3-4-5 gives 2, 2-5-8 gives 0).\n6 THREES: how many of the three digits are in {0, 3, 6, 9} (0-3-7 gives 2).\n\nEACH ROUND:\nStep 1. Code choice (leg-round 1 only, rounds 1, 5, 9). Both players simultaneously and secretly write a code. Three different digits written in any order are sorted ascending and become that player's code for this leg. Any other entry (repeated digits, wrong count, non-digits, blank) becomes the code 0-1-2. Only the engine knows the codes. Each player's guesses for the leg are set to {guesses_per_leg}, their solved flag to no, and their used cards to none.\nStep 2. Ask. Both players simultaneously and secretly name one card number (1-{question_cards}) they have not used in this leg; you are only offered your unused cards. If a player names nothing or an invalid card, they are given the lowest-numbered card they have not used this leg. The card becomes used for that player until the leg ends. Each player uses exactly {cards_used_per_leg} different cards per leg; all six are available again at the start of the next leg.\nStep 3. Answer. The engine computes each player's card from the opponent's code and announces to both players which card each player asked and the answer.\nStep 4. Guess. Both players simultaneously either pass or write a code guess. A guess of three different digits in any order is sorted ascending. Any other entry counts as a pass. A player with 0 guesses left, or who has already guessed correctly this leg, is not asked and passes. A pass costs nothing. A valid guess uses up 1 of that player's guesses for the leg.\nStep 5. Check. Each valid guess is compared with the opponent's code. Correct (all three digits match): the guesser scores {correct_score_base} minus the leg-round, so 4 points in leg-round 1, 3 in leg-round 2, 2 in leg-round 3, 1 in leg-round 4, and is marked solved for the rest of the leg, making no further guesses that leg. Wrong: the guesser loses {wrong_guess_penalty} point and gains 1 to their wrong-guess count. Every guess and its result (correct or wrong) is announced to both players. One player guessing correctly does not end the leg for the other player, who may keep asking and guessing.\nStep 6. Leg end (leg-round 4 only, rounds 4, 8, 12). Both codes are revealed to both players, and the current scores are announced.\nStep 7. End check. After round {total_rounds} the match ends.\n\nWINNING. After round {total_rounds}, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw and both share the win."
}
```

Why it was refused: the state shown to players is full of empty internal fields (see the bookkeeping rule): blank: the state a player is shown has empty fields (entry, pick); hide bookkeeping attributes (`none` on the table, `ally` on a player) so only what a player can use is printed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "break_the_code_three_leg_duel",
    "name": "Break the Code: Three-Leg Duel",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players hide three-digit codes, ask number-question cards at the same time, and score for cracking the opponent's code early over three legs."
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
        "key": "wrong_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guesses_left",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "solved",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "used_mask",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "code",
        "visible": "ally",
        "type": "number",
        "initial": 12
      },
      {
        "key": "ask",
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
        "key": "guess",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6"
        ]
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
        "key": "leg_round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "legs",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "rounds_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "total_rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "digit_min",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "digit_max",
        "visible": "public",
        "type": "number",
        "initial": 9
      },
      {
        "key": "code_length",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "default_code",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "question_cards",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "cards_used_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "guesses_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "correct_score_base",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "wrong_guess_penalty",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "high_digit_threshold",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "pass_value",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card_labels",
        "visible": "none",
        "type": "list",
        "initial": [
          "1",
          "2",
          "3",
          "4",
          "5",
          "6"
        ]
      },
      {
        "key": "card_bits",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          4,
          8,
          16,
          32
        ]
      },
      {
        "key": "scratch",
        "visible": "none",
        "type": "list",
        "initial": []
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting scores",
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
            "key": "wrong_count",
            "value": 0
          }
        },
        {
          "set": {
            "key": "round",
            "value": 0
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
      "use": "update",
      "phase": "start",
      "label": "next round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_round",
            "value": {
              "calc": "(round - 1) % rounds_per_leg + 1"
            }
          }
        }
      ],
      "text": "Round {round} of {total_rounds} begins (leg-round {leg_round} of {rounds_per_leg})."
    },
    {
      "use": "ask",
      "phase": "code",
      "label": "seat 1 code choice",
      "when": {
        "calc": "leg_round == 1"
      },
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "k1"
      },
      "text": "A new leg begins. Secretly write your code: three different digits from {digit_min} to {digit_max}, in any order (for example 8 2 5). They are sorted smallest first. Any other entry becomes the code 0-1-2."
    },
    {
      "use": "ask",
      "phase": "code",
      "label": "seat 2 code choice",
      "when": {
        "calc": "leg_round == 1"
      },
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "k2"
      },
      "text": "A new leg begins. Secretly write your code: three different digits from {digit_min} to {digit_max}, in any order (for example 8 2 5). They are sorted smallest first. Any other entry becomes the code 0-1-2."
    },
    {
      "use": "update",
      "phase": "code",
      "label": "codes are set",
      "when": {
        "calc": "leg_round == 1"
      },
      "do": [
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "sorted([int(ch) for ch in $k1 if ch in '0123456789'])"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "code",
            "value": {
              "calc": "(100 * scratch[0] + 10 * scratch[1] + scratch[2]) if (len(scratch) == code_length and scratch[0] < scratch[1] and scratch[1] < scratch[2]) else default_code"
            }
          }
        },
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "sorted([int(ch) for ch in $k2 if ch in '0123456789'])"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "code",
            "value": {
              "calc": "(100 * scratch[0] + 10 * scratch[1] + scratch[2]) if (len(scratch) == code_length and scratch[0] < scratch[1] and scratch[1] < scratch[2]) else default_code"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guesses_left",
            "value": {
              "calc": "guesses_per_leg"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "solved",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "used_mask",
            "value": 0
          }
        }
      ],
      "text": "Both codes are set for this leg. Each player has {guesses_per_leg} guesses and all {question_cards} cards available."
    },
    {
      "use": "sync",
      "phase": "code",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "fields": [
        "code",
        "guesses_left",
        "solved",
        "used_mask",
        "score"
      ],
      "text": "Your state:"
    },
    {
      "use": "update",
      "phase": "ask",
      "label": "cards on offer",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "[c for c in card_labels if int(you.used_mask / card_bits[int(c) - 1]) % 2 == 0]"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "ask",
      "label": "seat 1 asks a card",
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "q1"
      },
      "text": "Secretly name one question card you have not used this leg: 1 SUM (A+B+C), 2 EVENS (how many digits are even, 0 counts), 3 RANGE (C-A), 4 HIGH (how many digits are {high_digit_threshold} or more), 5 STEPS (how many of the pairs A,B and B,C differ by exactly 1), 6 THREES (how many digits are 0, 3, 6 or 9). It is answered from your opponent's code."
    },
    {
      "use": "ask",
      "phase": "ask",
      "label": "seat 2 asks a card",
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "q2"
      },
      "text": "Secretly name one question card you have not used this leg: 1 SUM (A+B+C), 2 EVENS (how many digits are even, 0 counts), 3 RANGE (C-A), 4 HIGH (how many digits are {high_digit_threshold} or more), 5 STEPS (how many of the pairs A,B and B,C differ by exactly 1), 6 THREES (how many digits are 0, 3, 6 or 9). It is answered from your opponent's code."
    },
    {
      "use": "update",
      "phase": "answer",
      "label": "the answers",
      "do": [
        {
          "set": {
            "player": 1,
            "key": "ask",
            "value": {
              "calc": "int($q1) if $q1 in players[0].offer else min([int(c) for c in players[0].offer])"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "ask",
            "value": {
              "calc": "int($q2) if $q2 in players[1].offer else min([int(c) for c in players[1].offer])"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "used_mask",
            "value": {
              "calc": "card_bits[you.ask - 1]"
            }
          }
        },
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "[int(players[1].code / 100), int(players[1].code / 10) % 10, players[1].code % 10]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "answer",
            "value": {
              "calc": "sum(scratch) if players[0].ask == 1 else (count(d % 2 == 0 for d in scratch) if players[0].ask == 2 else ((scratch[2] - scratch[0]) if players[0].ask == 3 else (count(d >= high_digit_threshold for d in scratch) if players[0].ask == 4 else (((1 if scratch[1] - scratch[0] == 1 else 0) + (1 if scratch[2] - scratch[1] == 1 else 0)) if players[0].ask == 5 else count(d % 3 == 0 for d in scratch)))))"
            }
          }
        },
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "[int(players[0].code / 100), int(players[0].code / 10) % 10, players[0].code % 10]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "answer",
            "value": {
              "calc": "sum(scratch) if players[1].ask == 1 else (count(d % 2 == 0 for d in scratch) if players[1].ask == 2 else ((scratch[2] - scratch[0]) if players[1].ask == 3 else (count(d >= high_digit_threshold for d in scratch) if players[1].ask == 4 else (((1 if scratch[1] - scratch[0] == 1 else 0) + (1 if scratch[2] - scratch[1] == 1 else 0)) if players[1].ask == 5 else count(d % 3 == 0 for d in scratch)))))"
            }
          }
        }
      ],
      "text": "Seat 1 asked card {players[0].ask} and the answer is {players[0].answer}. Seat 2 asked card {players[1].ask} and the answer is {players[1].answer}."
    },
    {
      "use": "ask",
      "phase": "guess",
      "label": "seat 1 guesses",
      "when": {
        "calc": "players[0].guesses_left > 0 and players[0].solved == 0"
      },
      "to": {
        "where": "you.seat == 1"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "g1"
      },
      "text": "Write 'pass', or guess your opponent's code as three different digits in any order. A correct guess scores {correct_score_base} minus the leg-round (now {leg_round}); a wrong guess costs {wrong_guess_penalty} point and adds 1 to your wrong guesses. A pass, or any entry that is not three different digits, costs nothing."
    },
    {
      "use": "ask",
      "phase": "guess",
      "label": "seat 2 guesses",
      "when": {
        "calc": "players[1].guesses_left > 0 and players[1].solved == 0"
      },
      "to": {
        "where": "you.seat == 2"
      },
      "answer": {
        "type": "text",
        "max_words": 20
      },
      "verify": {
        "bind": "g2"
      },
      "text": "Write 'pass', or guess your opponent's code as three different digits in any order. A correct guess scores {correct_score_base} minus the leg-round (now {leg_round}); a wrong guess costs {wrong_guess_penalty} point and adds 1 to your wrong guesses. A pass, or any entry that is not three different digits, costs nothing."
    },
    {
      "use": "update",
      "phase": "guess",
      "label": "read the guesses",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "guess",
            "value": {
              "calc": "pass_value"
            }
          }
        },
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "sorted([int(ch) for ch in $g1 if ch in '0123456789'])"
            },
            "if": {
              "calc": "players[0].guesses_left > 0 and players[0].solved == 0"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "guess",
            "value": {
              "calc": "100 * scratch[0] + 10 * scratch[1] + scratch[2]"
            },
            "if": {
              "calc": "players[0].guesses_left > 0 and players[0].solved == 0 and len(scratch) == code_length and scratch[0] < scratch[1] and scratch[1] < scratch[2]"
            }
          }
        },
        {
          "set": {
            "key": "scratch",
            "value": {
              "calc": "sorted([int(ch) for ch in $g2 if ch in '0123456789'])"
            },
            "if": {
              "calc": "players[1].guesses_left > 0 and players[1].solved == 0"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "guess",
            "value": {
              "calc": "100 * scratch[0] + 10 * scratch[1] + scratch[2]"
            },
            "if": {
              "calc": "players[1].guesses_left > 0 and players[1].solved == 0 and len(scratch) == code_length and scratch[0] < scratch[1] and scratch[1] < scratch[2]"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.guess > 0"
            },
            "key": "guesses_left",
            "value": -1
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "check",
      "label": "check the guesses",
      "do": [
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "correct_score_base - leg_round"
            },
            "if": {
              "calc": "players[0].guess > 0 and players[0].guess == players[1].code"
            },
            "text": "Seat 1 guessed {players[0].guess}: correct, scoring {value}.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "player": 1,
            "key": "solved",
            "value": 1,
            "if": {
              "calc": "players[0].guess > 0 and players[0].guess == players[1].code"
            }
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "score",
            "value": {
              "calc": "-wrong_guess_penalty"
            },
            "if": {
              "calc": "players[0].guess > 0 and players[0].guess != players[1].code"
            },
            "text": "Seat 1 guessed {players[0].guess}: wrong, losing {wrong_guess_penalty} point.",
            "announce_to": "all"
          }
        },
        {
          "adjust": {
            "player": 1,
            "key": "wrong_count",
            "value": 1,
            "if": {
              "calc": "players[0].guess > 0 and players[0].guess != players[1].code"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "correct_score_base - leg_round"
            },
            "if": {
              "calc": "players[1].guess > 0 and players[1].guess == players[0].code"
            },
            "text": "Seat 2 guessed {players[1].guess}: correct, scoring {value}.",
            "announce_to": "all"
          }
        },
        {
          "set": {
            "player": 2,
            "key": "solved",
            "value": 1,
            "if": {
              "calc": "players[1].guess > 0 and players[1].guess == players[0].code"
            }
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "score",
            "value": {
              "calc": "-wrong_guess_penalty"
            },
            "if": {
              "calc": "players[1].guess > 0 and players[1].guess != players[0].code"
            },
            "text": "Seat 2 guessed {players[1].guess}: wrong, losing {wrong_guess_penalty} point.",
            "announce_to": "all"
          }
        },
        {
          "adjust": {
            "player": 2,
            "key": "wrong_count",
            "value": 1,
            "if": {
              "calc": "players[1].guess > 0 and players[1].guess != players[0].code"
            }
          }
        }
      ],
      "text": "Guesses this round (written 100A+10B+C, 0 = pass): seat 1 {players[0].guess}, seat 2 {players[1].guess}."
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "leg end reveal",
      "when": {
        "calc": "leg_round == rounds_per_leg"
      },
      "to": "all",
      "text": "The leg is over. Codes (100A+10B+C): seat 1 {players[0].code}, seat 2 {players[1].code}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "check",
      "phase": "end",
      "label": "after round 12",
      "when": {
        "calc": "round >= total_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= total_rounds"
      },
      "rank_by": "you.score * 100 - you.wrong_count",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score} ({players[0].wrong_count} wrong guesses), Seat 2 {players[1].score} ({players[1].wrong_count} wrong guesses)."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Two players. The match has {legs} legs of {rounds_per_leg} rounds each ({total_rounds} rounds in total). Leg 1 is rounds 1-4, leg 2 is rounds 5-8, leg 3 is rounds 9-12. The leg-round is 1, 2, 3 or 4 within each leg: leg-round = ((round - 1) mod 4) + 1. Scores start at {starting_score} and carry across legs.\n\nCODES. A code is three different digits from {digit_min} to {digit_max}, kept smallest first as A < B < C (example: 2-5-8). Codes are shown as 100A+10B+C, so 2-5-8 is 258 and 0-1-2 is 12.\n\nTHE SIX QUESTION CARDS. Each answer is one number computed from the opponent's current code A < B < C.\n1 SUM: A + B + C (2-5-8 gives 15).\n2 EVENS: how many of the three digits are even, 0 counts as even (2-5-8 gives 2).\n3 RANGE: C - A (2-5-8 gives 6).\n4 HIGH: how many of the three digits are {high_digit_threshold} or more (2-5-8 gives 2).\n5 STEPS: how many of the pairs (A,B) and (B,C) differ by exactly 1, so 0, 1 or 2 (3-4-5 gives 2, 2-5-8 gives 0).\n6 THREES: how many of the three digits are in the set 0, 3, 6, 9 (0-3-7 gives 2).\n\nEACH ROUND:\nStep 1. Code choice (leg-round 1 only, rounds 1, 5, 9). Both players secretly write a code; neither sees the other's entry. Three different digits written in any order are sorted ascending and become that player's code for this leg. Any other entry (repeated digits, wrong count, non-digits, blank) becomes the code 0-1-2. Only the engine knows the codes. Each player's guesses for the leg are set to {guesses_per_leg}, their solved flag to no, and their used cards to none.\nStep 2. Ask. Both players secretly name one card number (1-{question_cards}) they have not used in this leg; you are only offered your unused cards. If a player names nothing or an invalid card, they are given the lowest-numbered card they have not used this leg. The card becomes used for that player until the leg ends. Each player uses exactly {cards_used_per_leg} different cards per leg; all six are available again at the start of the next leg.\nStep 3. Answer. The engine computes each player's card from the opponent's code and announces to both players which card each player asked and the answer.\nStep 4. Guess. Both players secretly either pass or write a code guess. A guess of three different digits in any order is sorted ascending. Any other entry counts as a pass. A player with 0 guesses left, or who has already guessed correctly this leg, is not asked and passes. A pass costs nothing. A valid guess uses up 1 of that player's guesses for the leg.\nStep 5. Check. Each valid guess is compared with the opponent's code. Correct (all three digits match): the guesser scores {correct_score_base} minus the leg-round, so 4 points in leg-round 1, 3 in leg-round 2, 2 in leg-round 3, 1 in leg-round 4, and is marked solved for the rest of the leg, making no further guesses that leg. Wrong: the guesser loses {wrong_guess_penalty} point and gains 1 to their wrong-guess count. Every guess and its result (correct or wrong) is announced to both players. One player guessing correctly does not end the leg for the other player, who may keep asking and guessing.\nStep 6. Leg end (leg-round 4 only, rounds 4, 8, 12). Both codes are revealed to both players, and the current scores are announced.\nStep 7. End check. After round {total_rounds} the match ends.\n\nWINNING. After round {total_rounds}, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses over the whole match wins. If that is also equal, the match is a draw and both share the win."
}
```
````
