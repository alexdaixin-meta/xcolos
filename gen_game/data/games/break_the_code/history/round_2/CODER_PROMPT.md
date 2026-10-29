# Task: write the XColos game file for "Break the Code: Coarse Clues"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

R1. Structure. Two players play a match of 12 rounds, split into 3 legs of 4 rounds each. Legs start at rounds 1, 5 and 9. The round counter starts at 0 and increases by exactly 1 at the very start of each round; nothing else changes it. Leg-round = ((round - 1) mod 4) + 1, so it runs 1, 2, 3, 4 within each leg.

R2. Player state. Each player has their own: score, wrong count, code, guesses left, solved, card asked, answer and guess. Score and wrong count start at 0 and carry over between legs. Both players are always handled separately: one player's result never blocks or changes the other's, except where a rule says the code's owner scores.

R3. New leg. When leg-round is 1, first reset each player's own guesses left to 2 and each player's own solved to 0. Then both players secretly and at the same time enter a code as a number, for example 147, 852, or 12 (meaning 0-1-2). In other rounds there is no code prompt and codes stay unchanged.

R4. Parsing a code. Read the entry x as digits A = floor(x / 100), B = floor(x / 10) mod 10 and C = x mod 10. If x is a whole number from 0 to 999 and A, B and C are all different, sort them ascending as a < b < c and store 100*a + 10*b + c. For example, 852 is stored as 258.

R5. Invalid code. Any other entry is stored as code 12 (digits 0, 1, 2). This covers repeated digits, out-of-range or non-numeric entries, and missing or declined entries.

R6. Asking. Every round, both players at the same time may pick one card number from 1 to 6 to ask about the opponent's code. Declining or giving an invalid number means no question this round. A card may be asked again; it gives the same answer. With the opponent's sorted digits a < b < c, the answers are:
- Card 1, High: how many of the three digits are 5 or higher (0-3).
- Card 2, Odd: how many of the digits are odd (0-3).
- Card 3, Prime: how many of the digits are 2, 3, 5 or 7 (0-3).
- Card 4, Threes: how many of the digits are 0, 3, 6 or 9 (0-3).
- Card 5, Chain: (1 if b - a = 1 else 0) + (1 if c - b = 1 else 0) (0-2).
- Card 6, Sum mod 4: (a + b + c) mod 4 (0-3).
Each answer is shown privately to the player who asked. Then both players are told which card number (or none) each player asked.

R7. Guessing. Then both players at the same time may enter a guess of the opponent's code. A player is prompted only if that player's own guesses left is above 0 and that player's own solved is 0. The guess is parsed as in R4.
- Pass: declining, or an entry that does not give three different digits from 0 to 999. A pass costs nothing.
- Correct: a valid guess equal to the opponent's stored code. The guesser scores 5 - leg-round, that is 4, 3, 2 or 1. That player's own solved becomes 1 for the rest of the leg.
- Wrong: any other valid guess. The guesser scores -1, their wrong count increases by 1, and their guesses left decreases by 1. The opponent, the code's owner, scores +1.
If both players guess correctly in the same round, both score.

R8. Results. After guessing, both players are told whether each player passed, guessed right or guessed wrong. Codes are not shown.

R9. End of leg. When leg-round is 4, after R8, each player whose own code was not guessed correctly during this leg scores +1. That is, a player scores +1 if the opponent's solved is still 0. Then both codes are revealed to both players.

R10. End. The game ends after round 12.

How the winner is decided: After round 12, the player with the higher total score wins. If the totals are equal, the player with fewer wrong guesses wins. If those are also equal, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Break the Code: Coarse Clues (2 to 2 players, best with 2)

Two players each hide a three-digit code of distinct digits, ask coarse clue cards about the opponent's code, and try to guess it early in a 4-round leg, over 3 legs.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total score, carried over between legs
  - each player: wrong_count (number, starts 0); everyone sees it. Number of wrong guesses over the match. It is the tie-break, and fewer is better
  - each player: code (number, starts 12); only its owner sees it. Own stored code: sorted distinct digits stored as 100a+10b+c
  - each player: revealed_code (number, starts -1); everyone sees it. Copy of code made public at the end of each leg; -1 means not yet revealed
  - each player: guesses_left (number, starts 2); everyone sees it. Wrong guesses still allowed in this leg
  - each player: solved (number, starts 0); everyone sees it. 1 once this player has correctly guessed the opponent's code in this leg
  - each player: card_asked (number, starts 0); everyone sees it. Card asked this round, 1-6; 0 means none. Announced after both players have asked
  - each player: answer (number, starts -1); only its owner sees it. Private answer to this round's card about the opponent's code; -1 means no question
  - each player: guess (number, starts -1); only its owner sees it. This round's parsed guess of the opponent's code; -1 means pass
  - each player: result (text, starts 'pass'); everyone sees it. This round's guess outcome: pass, right or wrong
  - the table: round (number, starts 0); everyone sees it. Round counter; increases by exactly 1 at the start of each round
  - the table: leg_round (number, starts 0); everyone sees it. ((round - 1) mod 4) + 1, running 1 to 4 within each leg
  - parameters, each kept as a table attribute: total_rounds = 12, legs = 3, rounds_per_leg = 4, leg_start_1 = 1, leg_start_2 = 5, leg_start_3 = 9, guesses_per_leg = 2, code_min = 0, code_max = 999, invalid_code_default = 12, card_min = 1, card_max = 6, high_threshold = 5, correct_score_base = 5, wrong_guess_penalty = -1, owner_bonus_on_wrong_guess = 1, unsolved_leg_bonus = 1, initial_score = 0, initial_wrong_count = 0, rank_score_weight = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 and seat 2 sit down; each seat's opponent is the other seat.
  2. Each player's score and wrong_count are set to 0. Each player's code is set to 12, revealed_code to -1, guesses_left to 2 and solved to 0.
  3. The table's round is set to 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round += 1; leg_round = ((round - 1) mod 4) + 1; for each player, card_asked = 0, answer = -1, guess = -1 and result = 'pass'.
  2. [update] all players. What happens: When leg_round == 1: for each player, guesses_left = 2, solved = 0 and revealed_code = -1.
  3. [poll] all players (only when leg_round == 1) answers: a whole number from 0 to 999, or decline. What happens: Each player's entry x is parsed into A = floor(x/100), B = floor(x/10) mod 10 and C = x mod 10. If A, B and C are all different, they are sorted ascending as a<b<c and code = 100a+10b+c. Otherwise, or if the player declines, code = 12. Neither player sees the other's entry.
  4. [poll] all players answers: a card number from 1 to 6, or decline. What happens: card_asked = the chosen card, or 0 if the player declines. Answers stay hidden until both are in.
  5. [update] all players. What happens: For each player with card_asked > 0, using the opponent's code digits a<b<c: card 1 gives the count of digits >= 5; card 2 the count of odd digits; card 3 the count of digits in {2,3,5,7}; card 4 the count of digits in {0,3,6,9}; card 5 gives (1 if b-a == 1 else 0) + (1 if c-b == 1 else 0); card 6 gives (a+b+c) mod 4. The result goes into that player's answer (ally, seen only by the asker).
  6. [sync] all players. What happens: Each player privately sees their own answer.
  7. [tell] all players. What happens: Announce 'Seat 1 asked card {card_asked of seat 1}; Seat 2 asked card {card_asked of seat 2}', where 0 means no question.
  8. [poll] each player with guesses_left > 0 and solved == 0 answers: a whole number from 0 to 999 as a guess of the opponent's code, or pass. What happens: The entry is parsed as for codes. If its three digits are all different, guess = the sorted value; otherwise, or on a pass, guess = -1.
  9. [update] all players. What happens: Applied to each player separately, using the guesses as entered. If guess == -1: result = 'pass'. If guess == the opponent's code: score += 5 - leg_round, solved = 1 and result = 'right'. If guess >= 0 and guess != the opponent's code: score -= 1, wrong_count += 1, guesses_left -= 1, result = 'wrong', and the opponent's score += 1.
  10. [tell] all players. What happens: Announce 'Seat 1: {result of seat 1}; Seat 2: {result of seat 2}'. Codes are not shown.
  11. [update] all players. What happens: When leg_round == 4: each player whose opponent's solved == 0 gets score += 1. Then, for each player, revealed_code = code.
  12. [tell] all players. What happens: When leg_round == 4, announce 'Codes this leg: Seat 1 {revealed_code of seat 1}, Seat 2 {revealed_code of seat 2}'.
  13. [check] table. What happens: If round >= 12, end the game; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a round starts, round increases by exactly 1 and leg_round = ((round - 1) mod 4) + 1, so rounds 1, 5 and 9 have leg_round 1 and rounds 4, 8 and 12 have leg_round 4.
  R2. When the game starts, each player's score is 0 and wrong_count is 0, and neither is reset between legs.
  R3. When leg_round is 1, each player's guesses_left is set to 2 and solved to 0 before codes are entered.
  R4. When leg_round is 1, both players are polled at the same time for a code; when leg_round is 2, 3 or 4, no code is asked for and codes stay unchanged.
  R5. When a player enters 852 as a code, code is stored as 258; when a player enters 12, code is stored as 12.
  R6. When a code entry has repeated digits (for example 447) or is declined, code is stored as 12.
  R7. When a player asks card 1 and the opponent's code is 258, answer is 2 (digits 5 and 8 are 5 or higher).
  R8. When a player asks card 2 and the opponent's code is 258, answer is 1 (the count of odd digits).
  R9. When a player asks card 3 and the opponent's code is 258, answer is 2 (the count of digits in 2, 3, 5, 7).
  R10. When a player asks card 4 and the opponent's code is 369, answer is 3 (the count of digits in 0, 3, 6, 9).
  R11. When a player asks card 5 and the opponent's code is 123, answer is 2; when the code is 258, answer is 0.
  R12. When a player asks card 6 and the opponent's code is 258, answer is 3 ((2+5+8) mod 4).
  R13. When a player declines to ask, card_asked is 0 and no answer is given; asking the same card again gives the same answer.
  R14. After asking, the answer is shown only to the asker, and both players are told which card each player asked.
  R15. When a player's guesses_left is 0 or solved is 1, that player is not asked for a guess.
  R16. When a guess is declined or has repeated digits, it is a pass, and score, wrong_count and guesses_left are unchanged.
  R17. When a valid guess equals the opponent's code, the guesser scores 5 - leg_round (4, 3, 2 or 1 in leg-rounds 1 to 4) and solved becomes 1.
  R18. When a valid guess does not equal the opponent's code, the guesser's score decreases by 1, wrong_count increases by 1, guesses_left decreases by 1, and the opponent's score increases by 1.
  R19. When both players guess correctly in the same round, both score 5 - leg_round.
  R20. After guessing, both players are told whether each player passed, guessed right or guessed wrong, and codes are not shown.
  R21. When leg_round is 4, each player whose opponent's solved is 0 scores +1, and then both codes are revealed to both players.
  R22. When round 12 has finished, the game ends; the higher score wins, a level score is broken by the lower wrong_count, and a full tie is a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Enter your secret code (only when leg_round is 1) | asked: both seats | options: any whole number from 0 to 999, or decline
  - Pick a card to ask about the opponent's code | asked: both seats, every round | options: card 1 (High), 2 (Odd), 3 (Prime), 4 (Threes), 5 (Chain), 6 (Sum mod 4), or decline
  - Guess the opponent's code | asked: each seat with guesses_left > 0 and solved == 0; a seat with guesses_left 0 or solved 1 is not asked | options: any whole number from 0 to 999, or pass

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.score * 100 - you.wrong_count (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The higher total score wins. If the scores are level, the player with fewer wrong guesses wins. If both are level, the two players share the win, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Total score, carried over between legs
- each player: `wrong_count` (number, visible: public, starts 0): Number of wrong guesses over the match. It is the tie-break, and fewer is better
- each player: `revealed_code` (number, visible: public, starts -1): Copy of code made public at the end of each leg; -1 means not yet revealed
- the table: `round` (number, visible: public, starts 0): Round counter; increases by exactly 1 at the start of each round
- parameters (each must be an attribute holding this value, never a number buried in a step): total_rounds = 12, legs = 3, rounds_per_leg = 4, leg_start_1 = 1, leg_start_2 = 5, leg_start_3 = 9, guesses_per_leg = 2, code_min = 0, code_max = 999, invalid_code_default = 12, card_min = 1, card_max = 6, high_threshold = 5, correct_score_base = 5, wrong_guess_penalty = -1, owner_bonus_on_wrong_guess = 1, unsolved_leg_bonus = 1, initial_score = 0, initial_wrong_count = 0, rank_score_weight = 100
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
