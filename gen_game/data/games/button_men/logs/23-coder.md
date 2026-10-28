# 23 coder

- time: 2026-10-28T05:37:16+00:00 (73.5s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 432903a0fad211df, reply sha256 7b268fdf07837e36

## Sent

````
# Task: write the XColos game file for "Button Men: Guard and Strike"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

DICE. Each player (A and B) owns three dice: a d4 (size 4), a d8 (size 8) and a d12 (size 12). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at 0.

RANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to 110,075,314,175. Write R in base 24 as digits D0 to D7, where Dk = floor(R / 24^k) mod 24. A die of size s set from digit D takes the value (D mod s) + 1.

LEGS. The match is exactly 30 exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.

EACH EXCHANGE:
1. Draw and leg start. Draw R. If this exchange starts a leg, set all six dice as described above.
2. Announcement. Both players are told the exchange number (1-30), the exchange number within the leg (1-10), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.
3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these 12 actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.
4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.
- If the target die is guarded by its owner this exchange, the attack fails. The defender scores 3, and the attacking die's value is announced to both players.
- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.
- Otherwise the attack fails. The defender scores 2, and both dice's values are announced to both players.
- A die may capture and be captured in the same exchange; both effects happen.
5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.
6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.
7. Leg end. If either player has no dice left, or this was exchange 10 of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +2, d8 +4, d12 +6. The next exchange starts a new leg.
8. Match end. After exchange 30, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.

How the winner is decided: After exchange 30 and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Button Men: Guard and Strike (2 to 2 players, best with 2)

Two players each hold a d4, d8 and d12 with hidden values. Over 30 exchanges they pick at the same moment to guard one of their dice or to attack an opponent's die, capturing it if the attacker's value is at least the target's. Legs reset the dice, and surviving dice score bonuses.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points so far
  - each player: d4_value (number, starts 1); only its owner sees it. Current value of own d4 (1-4)
  - each player: d8_value (number, starts 1); only its owner sees it. Current value of own d8 (1-8)
  - each player: d12_value (number, starts 1); only its owner sees it. Current value of own d12 (1-12)
  - each player: d4_alive (bool, starts True); everyone sees it. Own d4 not captured this leg
  - each player: d8_alive (bool, starts True); everyone sees it. Own d8 not captured this leg
  - each player: d12_alive (bool, starts True); everyone sees it. Own d12 not captured this leg
  - each player: action (number, starts 0); only its owner sees it. Action chosen this exchange (1-12); revealed in results
  - each player: attack_result (text, starts ''); everyone sees it. Outcome of own attack this exchange: none, success, fail_guarded, fail_low, or no_effect
  - each player: revealed_values (list, starts []); everyone sees it. Die values of this player announced this exchange because of failed attacks
  - the table: exchange (number, starts 1); everyone sees it. Current exchange number (1-30)
  - the table: leg_exchange (number, starts 1); everyone sees it. Exchange number within the current leg (1-10)
  - the table: leg_start (bool, starts True); everyone sees it. This exchange starts a new leg
  - the table: digits (list, starts []); hidden from all players. D0 to D7, the base-24 digits of this exchange's random R
  - parameters, each kept as a table attribute: dice_per_player = 3, small_die_size = 4, medium_die_size = 8, large_die_size = 12, starting_score = 0, random_max = 110075314175, digit_base = 24, digit_count = 8, total_exchanges = 30, max_exchanges_per_leg = 10, action_count = 12, guard_defense_points = 3, failed_attack_defense_points = 2, survive_bonus_d4 = 2, survive_bonus_d8 = 4, survive_bonus_d12 = 6, a_d4_digit = 0, a_d8_digit = 1, a_d12_digit = 2, b_d4_digit = 3, b_d8_digit = 4, b_d12_digit = 5, a_reroll_digit = 6, b_reroll_digit = 7

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat 1 is player A and seat 2 is player B.
  2. Both scores are set to 0.
  3. Set exchange to 1, leg_exchange to 1 and leg_start to true.
  4. All dice are marked alive.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Draw R uniformly from 0 to 110075314175 and store its base-24 digits D0..D7 in digits, where Dk = floor(R/24^k) mod 24. If leg_start: set every die's alive flag to true; set A's d4_value=(D0 mod 4)+1, d8_value=(D1 mod 8)+1, d12_value=(D2 mod 12)+1; set B's d4_value=(D3 mod 4)+1, d8_value=(D4 mod 8)+1, d12_value=(D5 mod 12)+1; set leg_exchange=1 and leg_start=false. Clear each player's revealed_values and attack_result.
  2. [tell] all players. What happens: Announce exchange, leg_exchange, both scores, and both players' d4_alive, d8_alive and d12_alive.
  3. [sync] all players. What happens: Each player privately sees their own d4_value, d8_value and d12_value.
  4. [poll] all players answers: one of 12 actions: 1 Guard my d4; 2 Guard my d8; 3 Guard my d12; 4 My d4 attacks their d4; 5 My d4 attacks their d8; 6 My d4 attacks their d12; 7 My d8 attacks their d4; 8 My d8 attacks their d8; 9 My d8 attacks their d12; 10 My d12 attacks their d4; 11 My d12 attacks their d8; 12 My d12 attacks their d12. What happens: Set each player's action. Nobody sees the other's choice until both are in.
  5. [update] all players. What happens: Resolve both attacks at once, using the values held at the start of this exchange. For each attacker X against opponent Y, where the action is 4-12 with attacking die a and target die t: if the X die a or the Y die t is not alive at the start of the exchange, attack_result=no_effect. Otherwise, if Y's action is the guard of die t (guard of d4=1, d8=2, d12=3) and that die is alive, attack_result=fail_guarded, Y.score += 3, and X's a value is appended to X.revealed_values. Otherwise, if X.a_value >= Y.t_value, attack_result=success, X.score += size of t (4, 8 or 12), and Y.t_alive is set to false after both attacks are resolved. Otherwise attack_result=fail_low, Y.score += 2, X's a value is appended to X.revealed_values and Y's t value is appended to Y.revealed_values. A die may capture and be captured in the same exchange.
  6. [update] all players. What happens: Rerolls, at most one die per player. A player's die is rerolled if it was guarded this exchange and was alive at the start (action 1-3), or if it attacked with attack_result=success and is still alive after the captures. Player A's rerolled die is set to (D6 mod size)+1. Player B's rerolled die is set to (D7 mod size)+1. New values are visible only to their owner.
  7. [tell] all players. What happens: Announce both actions, each attack_result, each player's revealed_values, which dice were captured, and both scores. Rerolled values are not announced.
  8. [update] all players. What happens: If a player has d4_alive, d8_alive and d12_alive all false, or leg_exchange = 10, or exchange = 30, the leg ends: each player's score += 2*d4_alive + 4*d8_alive + 6*d12_alive, and leg_start is set to true. Otherwise leg_exchange += 1. Then exchange += 1.
  9. [check] all players. What happens: End the game if exchange > 30; otherwise continue to the next exchange.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the match begins, then each player has a d4, a d8 and a d12, all alive, and both scores are 0.
  R2. When an exchange starts, then a random R from 0 to 110075314175 is drawn and split into base-24 digits D0..D7, with Dk = floor(R/24^k) mod 24.
  R3. When a leg starts, then all six dice are alive again; A's d4, d8 and d12 are set to (D0 mod 4)+1, (D1 mod 8)+1 and (D2 mod 12)+1; and B's d4, d8 and d12 are set to (D3 mod 4)+1, (D4 mod 8)+1 and (D5 mod 12)+1.
  R4. When an exchange begins, then both players are told the exchange number, the leg exchange number, both scores and which dice each player still has, and each player privately sees only their own die values.
  R5. When choosing, then both players choose at the same time one of the 12 actions, without seeing the other's choice.
  R6. When an action names a die that was already captured before this exchange (the actor's or the opponent's), then that action does nothing.
  R7. When an attack targets a die its owner guards this exchange, then the attack fails, the defender scores 3, and the attacking die's value is announced to both players.
  R8. When an unguarded target is attacked and the attacking value is greater than or equal to the target's value, then the attacker scores the target's size (4, 8 or 12) and the target is captured for the rest of the leg.
  R9. When an unguarded target is attacked and the attacking value is lower than the target's value, then the attack fails, the defender scores 2, and both dice's values are announced to both players.
  R10. When both attacks are resolved, then they use the values from the start of the exchange, and a die may both capture and be captured in the same exchange.
  R11. When a die guarded this exchange, or a die that attacked successfully and was not captured this exchange, then it is rerolled: A's from (D6 mod size)+1 and B's from (D7 mod size)+1, with the new value shown only to its owner.
  R12. When results are announced, then both actions, each attack's outcome, any announced values, any captures and the new scores are shown, but rerolled values are not.
  R13. When a player has no dice left, or the leg reaches its 10th exchange, then the leg ends and each player scores +2 for a surviving d4, +4 for a surviving d8 and +6 for a surviving d12.
  R14. When a leg ends, then the next exchange starts a new leg.
  R15. When exchange 30 ends and the leg in progress has not already ended, then it ends and the surviving-dice bonuses are scored.
  R16. When the match is over, then the higher total score wins, and equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choice of action each exchange | asked: both seats | options: always all 12: Guard my d4; Guard my d8; Guard my d12; My d4 attacks their d4/d8/d12; My d8 attacks their d4/d8/d12; My d12 attacks their d4/d8/d12. An action naming an already-captured die is allowed but does nothing.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: exchange > 30
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 30 exchanges and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals share the win, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Total points so far
- each player: `d4_alive` (bool, visible: public, starts True): Own d4 not captured this leg
- each player: `d8_alive` (bool, visible: public, starts True): Own d8 not captured this leg
- each player: `d12_alive` (bool, visible: public, starts True): Own d12 not captured this leg
- the table: `exchange` (number, visible: public, starts 1): Current exchange number (1-30)
- the table: `leg_exchange` (number, visible: public, starts 1): Exchange number within the current leg (1-10)
- parameters (each must be an attribute holding this value, never a number buried in a step): dice_per_player = 3, small_die_size = 4, medium_die_size = 8, large_die_size = 12, starting_score = 0, random_max = 110075314175, digit_base = 24, digit_count = 8, total_exchanges = 30, max_exchanges_per_leg = 10, action_count = 12, guard_defense_points = 3, failed_attack_defense_points = 2, survive_bonus_d4 = 2, survive_bonus_d8 = 4, survive_bonus_d12 = 6, a_d4_digit = 0, a_d8_digit = 1, a_d12_digit = 2, b_d4_digit = 3, b_d8_digit = 4, b_d12_digit = 5, a_reroll_digit = 6, b_reroll_digit = 7
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
    "id": "button_men_guard_strike",
    "name": "Button Men: Guard and Strike",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players, a hidden d4, d8 and d12 each: over 30 exchanges, guard a die or attack one of your opponent's, all at the same moment."
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
        "key": "d4_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d8_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d12_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d4_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "d8_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "d12_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "action",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attack_result",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_values",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "choice",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "att_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tgt_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "att_val",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tgt_val",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "att_ok",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "tgt_ok",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "lost_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reroll_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "exchange",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leg_exchange",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leg_start",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "digits",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "rand",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leg_over",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "action_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Guard my d4",
          "Guard my d8",
          "Guard my d12",
          "My d4 attacks their d4",
          "My d4 attacks their d8",
          "My d4 attacks their d12",
          "My d8 attacks their d4",
          "My d8 attacks their d8",
          "My d8 attacks their d12",
          "My d12 attacks their d4",
          "My d12 attacks their d8",
          "My d12 attacks their d12"
        ]
      },
      {
        "key": "action_codes",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12
        ]
      },
      {
        "key": "dice_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "small_die_size",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "medium_die_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "large_die_size",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "random_max",
        "visible": "public",
        "type": "number",
        "initial": 110075314175
      },
      {
        "key": "digit_base",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "digit_count",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_exchanges",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "max_exchanges_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "action_count",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "guard_defense_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "failed_attack_defense_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "survive_bonus_d4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "survive_bonus_d8",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "survive_bonus_d12",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "a_d4_digit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "a_d8_digit",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "a_d12_digit",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "b_d4_digit",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "b_d8_digit",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "b_d12_digit",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "a_reroll_digit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "b_reroll_digit",
        "visible": "public",
        "type": "number",
        "initial": 7
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
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
            "key": "exchange",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_exchange",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d4_alive",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d8_alive",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d12_alive",
            "value": true
          }
        }
      ],
      "text": "Seat 1 is player A and seat 2 is player B. Both scores are {starting_score}; every die is alive."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
      "label": "draw and leg start",
      "do": [
        {
          "set": {
            "key": "rand",
            "value": {
              "calc": "min(random_max, int(uniform(0, random_max + 1)))"
            }
          }
        },
        {
          "set": {
            "key": "digits",
            "value": {
              "calc": "[int(rand / digit_base ** k) % digit_base for k in [a_d4_digit, a_d8_digit, a_d12_digit, b_d4_digit, b_d8_digit, b_d12_digit, a_reroll_digit, b_reroll_digit]]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d4_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d8_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d12_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d4_value",
            "value": {
              "calc": "digits[a_d4_digit] % small_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d8_value",
            "value": {
              "calc": "digits[a_d8_digit] % medium_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d12_value",
            "value": {
              "calc": "digits[a_d12_digit] % large_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d4_value",
            "value": {
              "calc": "digits[b_d4_digit] % small_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d8_value",
            "value": {
              "calc": "digits[b_d8_digit] % medium_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d12_value",
            "value": {
              "calc": "digits[b_d12_digit] % large_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "key": "leg_exchange",
            "value": 1,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "attack_result",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the exchange begins",
      "to": "all",
      "text": "Exchange {exchange} of {total_exchanges} (exchange {leg_exchange} of this leg). Scores: seat 1 {players[0].score}, seat 2 {players[1].score}. Dice still held - seat 1: d4 {players[0].d4_alive}, d8 {players[0].d8_alive}, d12 {players[0].d12_alive}; seat 2: d4 {players[1].d4_alive}, d8 {players[1].d8_alive}, d12 {players[1].d12_alive}."
    },
    {
      "use": "sync",
      "phase": "announce",
      "label": "your dice",
      "mode": "self",
      "to": "all",
      "fields": [
        "d4_value",
        "d8_value",
        "d12_value"
      ],
      "text": "Your dice values (only you see these):"
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "the choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "action_names"
        }
      },
      "store": "choice",
      "text": "Choose one action for this exchange. Your opponent chooses at the same moment and will not see your choice until both are in. An action naming a die already captured (yours or theirs) does nothing."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": {
              "calc": "sum([k for k in action_codes if action_names[k - 1] == you.choice])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_size",
            "value": {
              "calc": "0 if you.action <= dice_per_player else [small_die_size, medium_die_size, large_die_size][int((you.action - dice_per_player - 1) / dice_per_player)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_size",
            "value": {
              "calc": "0 if you.action <= dice_per_player else [small_die_size, medium_die_size, large_die_size][(you.action - dice_per_player - 1) % dice_per_player]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guard_size",
            "value": {
              "calc": "[small_die_size, medium_die_size, large_die_size][you.action - 1] if you.action >= 1 and you.action <= dice_per_player else 0"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_val",
            "value": {
              "calc": "you.d4_value if you.att_size == small_die_size else (you.d8_value if you.att_size == medium_die_size else you.d12_value)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_ok",
            "value": {
              "calc": "you.d4_alive if you.att_size == small_die_size else (you.d8_alive if you.att_size == medium_die_size else (you.d12_alive if you.att_size == large_die_size else False))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_val",
            "value": {
              "calc": "sum([(p.d4_value if you.tgt_size == small_die_size else (p.d8_value if you.tgt_size == medium_die_size else p.d12_value)) for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_ok",
            "value": {
              "calc": "any([(p.d4_alive if you.tgt_size == small_die_size else (p.d8_alive if you.tgt_size == medium_die_size else (p.d12_alive if you.tgt_size == large_die_size else False))) for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "attack_result",
            "value": {
              "calc": "'none' if you.action <= dice_per_player else ('no_effect' if not (you.att_ok and you.tgt_ok) else ('fail_guarded' if you.tgt_size == sum([p.guard_size for p in players if p.seat != you.seat]) else ('success' if you.att_val >= you.tgt_val else 'fail_low')))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost_size",
            "value": {
              "calc": "sum([p.tgt_size for p in players if p.seat != you.seat and p.attack_result == 'success'])"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(you.tgt_size if you.attack_result == 'success' else 0) + guard_defense_points * count(p.seat != you.seat and p.attack_result == 'fail_guarded' for p in players) + failed_attack_defense_points * count(p.seat != you.seat and p.attack_result == 'fail_low' for p in players)"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.attack_result in ['fail_guarded', 'fail_low']"
            },
            "key": "revealed_values",
            "value": {
              "calc": "you.att_val"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "count(p.seat != you.seat and p.attack_result == 'fail_low' for p in players) > 0"
            },
            "key": "revealed_values",
            "value": {
              "calc": "sum([p.tgt_val for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == small_die_size"
            },
            "key": "d4_alive",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == medium_die_size"
            },
            "key": "d8_alive",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == large_die_size"
            },
            "key": "d12_alive",
            "value": false
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "rerolls",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "reroll_size",
            "value": {
              "calc": "you.guard_size if (you.guard_size > 0 and (you.d4_alive if you.guard_size == small_die_size else (you.d8_alive if you.guard_size == medium_die_size else you.d12_alive))) else (you.att_size if (you.attack_result == 'success' and you.lost_size != you.att_size) else 0)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == small_die_size"
            },
            "key": "d4_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % small_die_size + 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == medium_die_size"
            },
            "key": "d8_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % medium_die_size + 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == large_die_size"
            },
            "key": "d12_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % large_die_size + 1"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "results",
      "label": "the results",
      "to": "all",
      "text": "Results of exchange {exchange}: seat 1 chose '{players[0].choice}' (attack result: {players[0].attack_result}); seat 2 chose '{players[1].choice}' (attack result: {players[1].attack_result}). Announced values - seat 1: {players[0].revealed_values}; seat 2: {players[1].revealed_values}. Dice still held - seat 1: d4 {players[0].d4_alive}, d8 {players[0].d8_alive}, d12 {players[0].d12_alive}; seat 2: d4 {players[1].d4_alive}, d8 {players[1].d8_alive}, d12 {players[1].d12_alive}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "update",
      "phase": "leg end",
      "label": "leg end",
      "do": [
        {
          "set": {
            "key": "leg_over",
            "value": {
              "calc": "any([(not p.d4_alive) and (not p.d8_alive) and (not p.d12_alive) for p in players]) or leg_exchange >= max_exchanges_per_leg or exchange >= total_exchanges"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "survive_bonus_d4 * (1 if you.d4_alive else 0) + survive_bonus_d8 * (1 if you.d8_alive else 0) + survive_bonus_d12 * (1 if you.d12_alive else 0)"
            },
            "if": {
              "calc": "leg_over"
            }
          }
        },
        {
          "adjust": {
            "key": "leg_exchange",
            "value": 1,
            "if": {
              "calc": "not leg_over"
            }
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": {
              "calc": "leg_over"
            }
          }
        },
        {
          "adjust": {
            "key": "exchange",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "the leg ends",
      "when": {
        "calc": "leg_start"
      },
      "to": "all",
      "text": "The leg is over. Surviving-dice bonuses scored (d4 +{survive_bonus_d4}, d8 +{survive_bonus_d8}, d12 +{survive_bonus_d12}). Scores: seat 1 {players[0].score}, seat 2 {players[1].score}. The next exchange starts a new leg."
    },
    {
      "use": "check",
      "phase": "leg end",
      "label": "after exchange 30",
      "when": {
        "calc": "exchange > total_exchanges"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "exchange > total_exchanges"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 35,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Seat 1 is player A and seat 2 is player B. Each player owns {dice_per_player} dice: a d4 (size {small_die_size}), a d8 (size {medium_die_size}) and a d12 (size {large_die_size}). A die's value is a whole number from 1 to its size. You see your own values; you do not see your opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at {starting_score}.\n\nRANDOMNESS. At the start of every exchange the engine draws a random integer R from 0 to {random_max} and writes it in base {digit_base} as digits D0 to D7 (Dk = floor(R / {digit_base}^k) mod {digit_base}). A die of size s set from digit D takes the value (D mod s) + 1.\n\nLEGS. The match is exactly {total_exchanges} exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg both players get all three dice back. A's d4, d8 and d12 are set from D0, D1 and D2; B's d4, d8 and d12 from D3, D4 and D5.\n\nEACH EXCHANGE:\n1. Draw R; if the exchange starts a leg, set all six dice
... (cut)

Why it was refused: the game file was refused by the loader: button_men: steps[0].do[1].value.calc: '[int(rand / digit_base ** k) % digit_base for k in [a_d4_digit, a_d8_digit, a_d12_digit, b_d4_digit, b_d8_digit, b_d12_digit, a_reroll_digit, b_reroll_digit]]': Pow is not allowed
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "button_men_guard_strike",
    "name": "Button Men: Guard and Strike",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two players each hold a hidden d4, d8 and d12. Over 30 exchanges, both choose at the same moment to guard one of their dice or attack one of the opponent's."
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
        "key": "d4_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d8_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d12_value",
        "visible": "ally",
        "type": "number",
        "initial": 1
      },
      {
        "key": "d4_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "d8_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "d12_alive",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "action",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "attack_result",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "revealed_values",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "choice",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "att_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tgt_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "guard_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "att_val",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "tgt_val",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "att_ok",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "tgt_ok",
        "visible": "ally",
        "type": "bool",
        "initial": false
      },
      {
        "key": "lost_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reroll_size",
        "visible": "ally",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "exchange",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leg_exchange",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "leg_start",
        "visible": "public",
        "type": "bool",
        "initial": true
      },
      {
        "key": "digits",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "rand",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "leg_over",
        "visible": "none",
        "type": "bool",
        "initial": false
      },
      {
        "key": "action_names",
        "visible": "none",
        "type": "list",
        "initial": [
          "Guard my d4",
          "Guard my d8",
          "Guard my d12",
          "My d4 attacks their d4",
          "My d4 attacks their d8",
          "My d4 attacks their d12",
          "My d8 attacks their d4",
          "My d8 attacks their d8",
          "My d8 attacks their d12",
          "My d12 attacks their d4",
          "My d12 attacks their d8",
          "My d12 attacks their d12"
        ]
      },
      {
        "key": "action_codes",
        "visible": "none",
        "type": "list",
        "initial": [
          1,
          2,
          3,
          4,
          5,
          6,
          7,
          8,
          9,
          10,
          11,
          12
        ]
      },
      {
        "key": "dice_per_player",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "small_die_size",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "medium_die_size",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "large_die_size",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "starting_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "random_max",
        "visible": "public",
        "type": "number",
        "initial": 110075314175
      },
      {
        "key": "digit_base",
        "visible": "public",
        "type": "number",
        "initial": 24
      },
      {
        "key": "digit_count",
        "visible": "public",
        "type": "number",
        "initial": 8
      },
      {
        "key": "total_exchanges",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "max_exchanges_per_leg",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "action_count",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "guard_defense_points",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "failed_attack_defense_points",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "survive_bonus_d4",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "survive_bonus_d8",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "survive_bonus_d12",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "a_d4_digit",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "a_d8_digit",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "a_d12_digit",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "b_d4_digit",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "b_d8_digit",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "b_d12_digit",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "a_reroll_digit",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "b_reroll_digit",
        "visible": "public",
        "type": "number",
        "initial": 7
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the match begins",
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
            "key": "exchange",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_exchange",
            "value": 1
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d4_alive",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d8_alive",
            "value": true
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d12_alive",
            "value": true
          }
        }
      ],
      "text": "Seat 1 is player A and seat 2 is player B. Both scores are {starting_score}; every die is alive."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "draw",
      "label": "draw and leg start",
      "do": [
        {
          "set": {
            "key": "rand",
            "value": {
              "calc": "min(random_max, int(uniform(0, random_max + 1)))"
            }
          }
        },
        {
          "set": {
            "key": "digits",
            "value": {
              "calc": "[rand % digit_base, int(rand / digit_base) % digit_base, int(rand / (digit_base * digit_base)) % digit_base, int(rand / (digit_base * digit_base * digit_base)) % digit_base, int(rand / (digit_base * digit_base * digit_base * digit_base)) % digit_base, int(rand / (digit_base * digit_base * digit_base * digit_base * digit_base)) % digit_base, int(rand / (digit_base * digit_base * digit_base * digit_base * digit_base * digit_base)) % digit_base, int(rand / (digit_base * digit_base * digit_base * digit_base * digit_base * digit_base * digit_base)) % digit_base]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d4_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d8_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "d12_alive",
            "value": true,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d4_value",
            "value": {
              "calc": "digits[a_d4_digit] % small_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d8_value",
            "value": {
              "calc": "digits[a_d8_digit] % medium_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "d12_value",
            "value": {
              "calc": "digits[a_d12_digit] % large_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d4_value",
            "value": {
              "calc": "digits[b_d4_digit] % small_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d8_value",
            "value": {
              "calc": "digits[b_d8_digit] % medium_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "d12_value",
            "value": {
              "calc": "digits[b_d12_digit] % large_die_size + 1"
            },
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "key": "leg_exchange",
            "value": 1,
            "if": {
              "calc": "leg_start"
            }
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": false
          }
        },
        {
          "set": {
            "players": "all",
            "key": "revealed_values",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "attack_result",
            "value": ""
          }
        },
        {
          "set": {
            "players": "all",
            "key": "choice",
            "value": ""
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "announce",
      "label": "the exchange begins",
      "to": "all",
      "text": "Exchange {exchange} of {total_exchanges} (exchange {leg_exchange} of this leg). Scores: seat 1 {players[0].score}, seat 2 {players[1].score}. Dice still held - seat 1: d4 {players[0].d4_alive}, d8 {players[0].d8_alive}, d12 {players[0].d12_alive}; seat 2: d4 {players[1].d4_alive}, d8 {players[1].d8_alive}, d12 {players[1].d12_alive}."
    },
    {
      "use": "sync",
      "phase": "announce",
      "label": "your dice",
      "mode": "self",
      "to": "all",
      "fields": [
        "d4_value",
        "d8_value",
        "d12_value"
      ],
      "text": "Your dice values (only you see these):"
    },
    {
      "use": "poll",
      "phase": "choose",
      "label": "the choice",
      "to": "acting",
      "answer": {
        "type": "choice",
        "options": {
          "game": "action_names"
        }
      },
      "store": "choice",
      "text": "Choose one action for this exchange. Your opponent chooses at the same moment and will not see your choice until both are in. An action naming a die already captured (yours or theirs) does nothing."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "resolution",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "action",
            "value": {
              "calc": "sum([k for k in action_codes if action_names[k - 1] == you.choice])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_size",
            "value": {
              "calc": "0 if you.action <= dice_per_player else [small_die_size, medium_die_size, large_die_size][int((you.action - dice_per_player - 1) / dice_per_player)]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_size",
            "value": {
              "calc": "0 if you.action <= dice_per_player else [small_die_size, medium_die_size, large_die_size][(you.action - dice_per_player - 1) % dice_per_player]"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "guard_size",
            "value": {
              "calc": "[small_die_size, medium_die_size, large_die_size][you.action - 1] if you.action >= 1 and you.action <= dice_per_player else 0"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_val",
            "value": {
              "calc": "you.d4_value if you.att_size == small_die_size else (you.d8_value if you.att_size == medium_die_size else you.d12_value)"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "att_ok",
            "value": {
              "calc": "you.d4_alive if you.att_size == small_die_size else (you.d8_alive if you.att_size == medium_die_size else (you.d12_alive if you.att_size == large_die_size else False))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_val",
            "value": {
              "calc": "sum([(p.d4_value if you.tgt_size == small_die_size else (p.d8_value if you.tgt_size == medium_die_size else p.d12_value)) for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "tgt_ok",
            "value": {
              "calc": "any([(p.d4_alive if you.tgt_size == small_die_size else (p.d8_alive if you.tgt_size == medium_die_size else (p.d12_alive if you.tgt_size == large_die_size else False))) for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "attack_result",
            "value": {
              "calc": "'none' if you.action <= dice_per_player else ('no_effect' if not (you.att_ok and you.tgt_ok) else ('fail_guarded' if you.tgt_size == sum([p.guard_size for p in players if p.seat != you.seat]) else ('success' if you.att_val >= you.tgt_val else 'fail_low')))"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "lost_size",
            "value": {
              "calc": "sum([p.tgt_size for p in players if p.seat != you.seat and p.attack_result == 'success'])"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(you.tgt_size if you.attack_result == 'success' else 0) + guard_defense_points * count(p.seat != you.seat and p.attack_result == 'fail_guarded' for p in players) + failed_attack_defense_points * count(p.seat != you.seat and p.attack_result == 'fail_low' for p in players)"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "you.attack_result in ['fail_guarded', 'fail_low']"
            },
            "key": "revealed_values",
            "value": {
              "calc": "you.att_val"
            }
          }
        },
        {
          "append": {
            "players": {
              "where": "count(p.seat != you.seat and p.attack_result == 'fail_low' for p in players) > 0"
            },
            "key": "revealed_values",
            "value": {
              "calc": "sum([p.tgt_val for p in players if p.seat != you.seat])"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == small_die_size"
            },
            "key": "d4_alive",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == medium_die_size"
            },
            "key": "d8_alive",
            "value": false
          }
        },
        {
          "set": {
            "players": {
              "where": "you.lost_size == large_die_size"
            },
            "key": "d12_alive",
            "value": false
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "rerolls",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "reroll_size",
            "value": {
              "calc": "you.guard_size if (you.guard_size > 0 and (you.d4_alive if you.guard_size == small_die_size else (you.d8_alive if you.guard_size == medium_die_size else you.d12_alive))) else (you.att_size if (you.attack_result == 'success' and you.lost_size != you.att_size) else 0)"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == small_die_size"
            },
            "key": "d4_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % small_die_size + 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == medium_die_size"
            },
            "key": "d8_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % medium_die_size + 1"
            }
          }
        },
        {
          "set": {
            "players": {
              "where": "you.reroll_size == large_die_size"
            },
            "key": "d12_value",
            "value": {
              "calc": "digits[a_reroll_digit if you.seat == 1 else b_reroll_digit] % large_die_size + 1"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "results",
      "label": "the results",
      "to": "all",
      "text": "Results of exchange {exchange}: seat 1 chose '{players[0].choice}' (attack result: {players[0].attack_result}); seat 2 chose '{players[1].choice}' (attack result: {players[1].attack_result}). Announced values - seat 1: {players[0].revealed_values}; seat 2: {players[1].revealed_values}. Dice still held - seat 1: d4 {players[0].d4_alive}, d8 {players[0].d8_alive}, d12 {players[0].d12_alive}; seat 2: d4 {players[1].d4_alive}, d8 {players[1].d8_alive}, d12 {players[1].d12_alive}. Scores: seat 1 {players[0].score}, seat 2 {players[1].score}."
    },
    {
      "use": "update",
      "phase": "leg end",
      "label": "leg end",
      "do": [
        {
          "set": {
            "key": "leg_over",
            "value": {
              "calc": "any([(not p.d4_alive) and (not p.d8_alive) and (not p.d12_alive) for p in players]) or leg_exchange >= max_exchanges_per_leg or exchange >= total_exchanges"
            }
          }
        },
        {
          "adjust": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "survive_bonus_d4 * (1 if you.d4_alive else 0) + survive_bonus_d8 * (1 if you.d8_alive else 0) + survive_bonus_d12 * (1 if you.d12_alive else 0)"
            },
            "if": {
              "calc": "leg_over"
            }
          }
        },
        {
          "adjust": {
            "key": "leg_exchange",
            "value": 1,
            "if": {
              "calc": "not leg_over"
            }
          }
        },
        {
          "set": {
            "key": "leg_start",
            "value": {
              "calc": "leg_over"
            }
          }
        },
        {
          "adjust": {
            "key": "exchange",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "leg end",
      "label": "the leg ends",
      "when": {
        "calc": "leg_start"
      },
      "to": "all",
      "text": "The leg is over. Surviving-dice bonuses scored (d4 +{survive_bonus_d4}, d8 +{survive_bonus_d8}, d12 +{survive_bonus_d12}). Scores: seat 1 {players[0].score}, seat 2 {players[1].score}. The next exchange starts a new leg."
    },
    {
      "use": "check",
      "phase": "leg end",
      "label": "after exchange 30",
      "when": {
        "calc": "exchange > total_exchanges"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "exchange > total_exchanges"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 35,
    "actions_max": 2000,
    "deadline_s": 120
  },
  "rules": "Seat 1 is player A and seat 2 is player B. Each player owns {dice_per_player} dice: a d4 (size {small_die_size}), a d8 (size {medium_die_size}) and a d12 (size {large_die_size}). A die's value is a whole number from 1 to its size. Each player sees their own values. Neither sees the opponent's values unless a rule below reveals them. Both players always see which dice each player still has. Both scores start at {starting_score}.\n\nRANDOMNESS. Once per exchange, at its start, the engine draws one random integer R, uniform from 0 to {random_max}. R is written in base {digit_base} as digits D0 to D7, where Dk = floor(R / {digit_base}^k) mod {digit_base}. A die of size s set from digit D takes the value (D mod s) + 1.\n\nLEGS. The match is exactly {total_exchanges} exchanges, grouped into legs. A leg starts at exchange 1, and again at the exchange after any leg ends. At the start of a leg, both players get all three dice back. Player A's d4, d8 and d12 are set from D0, D1 and D2. Player B's d4, d8 and d12 are set from D3, D4 and D5. The leg counter is set to 1 and goes up by 1 each further exchange of the leg.\n\nEACH EXCHANGE:\n1. Draw and leg start. R is drawn. If this exchange starts a leg, all six dice are set as described above.\n2. Announcement. Both players are told the exchange number (1-{total_exchanges}), the exchange number within the leg (1-{max_exchanges_per_leg}), both scores, and which dice each player still has. Each player is privately told the current values of their own dice.\n3. Choice. Both players choose at the same moment, without seeing the other's choice, exactly one of these {action_count} actions: (1) Guard my d4; (2) Guard my d8; (3) Guard my d12; (4) My d4 attacks their d4; (5) My d4 attacks their d8; (6) My d4 attacks their d12; (7) My d8 attacks their d4; (8) My d8 attacks their d8; (9) My d8 attacks their d12; (10) My d12 attacks their d4; (11) My d12 attacks their d8; (12) My d12 attacks their d12. An action that names a die that is already captured (yours or theirs) does nothing.\n4. Resolution. Both actions are resolved at the same time, using the values the dice showed at the start of the exchange.\n- If the target die is guarded by its owner this exchange, the attack fails. The defender scores {guard_defense_points}, and the attacking die's value is announced to both players.\n- Otherwise, if the attacking value is greater than or equal to the target's value, the attack succeeds. The attacker scores points equal to the target's size, and the target is captured and removed for the rest of the leg.\n- Otherwise the attack fails. The defender scores {failed_attack_defense_points}, and both dice's values are announced to both players.\n- A die may capture and be captured in the same exchange; both effects happen.\n5. Rerolls. Each player rerolls at most one die. A die is rerolled if it attacked successfully and was not captured this exchange, or if it was guarded this exchange (whether or not it was attacked). Player A's rerolled die is set from digit D6. Player B's rerolled die is set from digit D7. New values are shown only to their owner.\n6. Results. Both actions, the success or failure of each attack, any announced values, any captures, and the new scores are announced to both players. Rerolled values are not announced. A die that was not rerolled keeps its value, including any value that has been announced.\n7. Leg end. If either player has no dice left, or this was exchange {max_exchanges_per_leg} of the leg, the leg ends. Each player scores a bonus for each of their surviving dice: d4 +{survive_bonus_d4}, d8 +{survive_bonus_d8}, d12 +{survive_bonus_d12}. The next exchange starts a new leg.\n8. Match end. After exchange {total_exchanges}, if the leg in progress has not already ended, it ends now and the surviving-dice bonuses are scored. The match is then over.\n\nWINNING. After exchange {total_exchanges} and the final surviving-dice bonuses, the player with the higher total score wins. Equal totals are a draw (the win is shared)."
}
```
````
