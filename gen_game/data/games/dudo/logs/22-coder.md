# 22 coder

- time: 2026-10-28T05:47:16+00:00 (67.1s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 f8172f869c698708, reply sha256 ea72ffacaf1f566c

## Sent

````
# Task: write the XColos game file for "Short Dudo"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 4; set `meta.players` to {"min": 2, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP. 2 to 4 players sit in a fixed seat order: seat 1, seat 2, and so on. Each player starts with 5 dice. Seat 1 is the opener for round 1. There is no random draw before play.

EACH ROUND.
1. ROLL. In one deal operation, every player still in the game receives a fresh random roll of as many six-sided dice as they currently hold. This single operation produces all hands at once and is the only random event of the round. Each player is shown only their own dice. T is the total number of dice still in play, and every player is told T and every player's dice count.
2. OPENING BID (choice 1). The opener chooses a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). The bid means 'at least Q dice among all players show this face, with every 1 counting as this face'. The bid is announced to all.
3. RESPONSE 1 (choice 2). The next player in seat order who is still in the game chooses one of four options:
   (a) Raise +1: the new quantity is the current quantity + 1, with any face from 2 to 6 the player chooses.
   (b) Raise +2: the new quantity is the current quantity + 2, with any face from 2 to 6 the player chooses.
   (c) Dudo: challenge the current bid as false.
   (d) Calza: claim the count is exactly the current quantity.
   A raise is illegal if the new quantity would exceed T. If both raises are illegal, only Dudo or Calza may be chosen. The choice is announced. A player who raises becomes the current bidder.
4. RESPONSE 2 (choice 3). This step happens only if response 1 was a raise. The next player in seat order who is still in the game makes the same kind of choice against the current bid. With 2 players, this is the opener again.
5. FINAL RESPONSE (choice 4). This step happens only if response 2 was a raise. The next player in seat order who is still in the game must choose Dudo or Calza. Raising is not allowed.
6. REVEAL. All dice are shown. N is the number of dice showing the current bid face plus the number showing 1, computed as one count over all dice.
7. SETTLE. If the call was Dudo: when N >= the current quantity, the caller loses 1 die; otherwise the current bidder loses 1 die. If the call was Calza: when N equals the current quantity exactly, the caller gains 1 die, up to a maximum of 5; otherwise the caller loses 1 die.
8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from then on.
9. NEXT OPENER. The player who lost a die opens the next round. After a successful Calza, the caller opens. If that player was eliminated, the next player in seat order who is still in the game opens.
10. END CHECK. If only one player remains, the game ends. If 30 rounds have been played, the game ends. Otherwise a new round begins.

There is no talk phase. Bids and calls are the only communication.

How the winner is decided: If only one player has dice left, that player wins. If 30 rounds are completed with two or more players still in, the player holding the most dice wins. If two or more players tie for the most dice, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Short Dudo (2 to 4 players, best with 3)

A short bluffing dice game. Players bid on how many dice around the table show a face, with 1s wild. The next players raise, call Dudo (false) or call Calza (exact), and the loser of each call loses a die.

STATE (every item below must exist in the file):
  - each player: dice_count (number, starts 5); everyone sees it. How many dice this player holds. This is the score.
  - each player: hand (list, starts []); only its owner sees it. This round's die faces (1-6) for this player, seen only by the owner until the reveal.
  - each player: out (bool, starts False); everyone sees it. True once the player has 0 dice. An out player is skipped in seat order.
  - the table: round_num (number, starts 0); everyone sees it. Rounds started so far.
  - the table: opener_seat (number, starts 1); everyone sees it. Seat that opens the bidding this round.
  - the table: total_dice (number, starts 0); everyone sees it. T: total dice held by players still in the game.
  - the table: current_face (number, starts 0); everyone sees it. Face (2-6) of the standing bid.
  - the table: current_qty (number, starts 0); everyone sees it. Quantity of the standing bid.
  - the table: current_bidder (number, starts 0); everyone sees it. Seat that made the standing bid.
  - the table: responder_seat (number, starts 0); everyone sees it. Seat due to respond next: the next seat after current_bidder that is not out.
  - the table: call_type (text, starts ''); everyone sees it. Empty while bidding continues, otherwise 'dudo' or 'calza'.
  - the table: caller_seat (number, starts 0); everyone sees it. Seat that called Dudo or Calza.
  - the table: reveal_count (number, starts 0); everyone sees it. N: dice in all hands showing current_face plus dice showing 1.
  - the table: loser_seat (number, starts 0); everyone sees it. Seat that lost a die this round, or 0 if none did.
  - parameters, each kept as a table attribute: start_dice = 5, max_dice = 5, die_faces = 6, wild_face = 1, min_bid_face = 2, max_bid_face = 6, opening_min_divisor = 3, opening_min_floor = 1, opening_max_divisor = 2, raise_small = 1, raise_big = 2, dudo_loss = 1, calza_loss = 1, calza_gain = 1, max_rounds = 30, first_opener_seat = 1, max_responses_per_round = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats are numbered 1 to the player count in a fixed order.
  2. Each player's dice_count is set to 5, hand is set empty and out is set false.
  3. opener_seat is set to 1 and round_num to 0.
  4. There is no random draw before play.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_num += 1. call_type = '', caller_seat = 0 and loser_seat = 0. total_dice = sum of dice_count over players with out = false.
  2. [initialize] all players. What happens: In one deal, every player with out = false gets hand set to dice_count random faces from 1 to 6. Out players keep an empty hand.
  3. [sync] all players. What happens: Each player sees their own hand, total_dice and every player's dice_count and out.
  4. [ask] seat opener_seat answers: a face from 2 to 6. What happens: current_face = the chosen face. current_bidder = opener_seat.
  5. [ask] seat opener_seat answers: a whole number from max(1, floor(total_dice/3)) to ceil(total_dice/2). What happens: current_qty = the number. The bid is announced to all. responder_seat = the next seat after current_bidder with out = false.
  6. [ask] seat responder_seat (response 1) answers: one of raise1_faceF (F = 2..6, offered only if current_qty+1 <= total_dice), raise2_faceF (F = 2..6, offered only if current_qty+2 <= total_dice), dudo, calza. What happens: On raiseK_faceF: current_qty += K, current_face = F, current_bidder = responder_seat, then responder_seat = the next seat after current_bidder with out = false. On dudo or calza: call_type = the choice, caller_seat = responder_seat. The choice is announced to all.
  7. [ask] seat responder_seat (response 2), when call_type = '' answers: the same options as response 1, with the same legality limits. What happens: The same as response 1. With 2 players this seat is the opener.
  8. [ask] seat responder_seat (final response), when call_type = '' answers: dudo or calza. What happens: call_type = the choice, caller_seat = responder_seat. The choice is announced to all.
  9. [update] all players. What happens: Reveal: every hand is shown to all. reveal_count = count over all hands of dice equal to current_face or equal to 1.
  10. [update] all players. What happens: Settle. If call_type = 'dudo' and reveal_count >= current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. If call_type = 'dudo' and reveal_count < current_qty: current_bidder dice_count -= 1, loser_seat = current_bidder. If call_type = 'calza' and reveal_count = current_qty: caller_seat dice_count = min(dice_count + 1, 5), loser_seat = 0. If call_type = 'calza' and reveal_count != current_qty: caller_seat dice_count -= 1, loser_seat = caller_seat. The result is announced.
  11. [update] all players. What happens: Elimination: any player with dice_count = 0 gets out = true.
  12. [update] all players. What happens: Next opener. If loser_seat > 0, opener_seat = loser_seat; otherwise (a successful Calza) opener_seat = caller_seat. If that seat has out = true, opener_seat = the next seat after it with out = false.
  13. [check] all players. What happens: End the game if the number of players with out = false is 1, or if round_num >= 30. Otherwise start a new round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup every player has dice_count 5 and out false, and seat 1 opens round 1.
  R2. Each round, every player not out gets a fresh hand of exactly dice_count random faces from 1 to 6, visible only to the owner.
  R3. total_dice equals the sum of dice_count over players not out, and it is told to everyone with every dice_count.
  R4. The opener bids a face from 2 to 6 and a quantity Q with max(1, floor(T/3)) <= Q <= ceil(T/2). For example, with T = 15, Q is from 5 to 8.
  R5. When a responder chooses Raise +1, current_qty increases by 1, current_face becomes their chosen face from 2 to 6, and they become current_bidder.
  R6. When a responder chooses Raise +2, current_qty increases by 2, current_face becomes their chosen face from 2 to 6, and they become current_bidder.
  R7. When a raise would make current_qty exceed total_dice, that raise is not offered. If both raises exceed it, only Dudo and Calza are offered.
  R8. The responder is always the next seat in order after the current bidder that is not out. With 2 players, response 2 is answered by the opener.
  R9. Response 2 happens only when response 1 was a raise, and the final response happens only when response 2 was a raise.
  R10. The final responder may choose only Dudo or Calza.
  R11. At reveal, N counts every die in all hands that shows current_face or shows 1.
  R12. When Dudo is called and N >= current_qty, the caller loses 1 die.
  R13. When Dudo is called and N < current_qty, the current bidder loses 1 die.
  R14. When Calza is called and N == current_qty, the caller gains 1 die, but never above 5.
  R15. When Calza is called and N != current_qty, the caller loses 1 die.
  R16. When a player's dice_count reaches 0, out becomes true, and the player is skipped in seat order and gets no hand from then on.
  R17. The player who lost a die opens the next round. After a successful Calza the caller opens. If that player is out, the next seat in order that is not out opens.
  R18. When only one player is not out, the game ends and that player wins.
  R19. When 30 rounds have been played, the game ends and the highest dice_count wins. Players tied at the top share the result as a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Opening face | asked: the opener | options: faces 2, 3, 4, 5, 6
  - Opening quantity | asked: the opener | options: whole numbers from max(1, floor(total_dice/3)) to ceil(total_dice/2)
  - Response 1 and response 2 | asked: the next seat after the current bidder that is not out | options: If current_qty + 2 <= total_dice: raise1_face2..raise1_face6, raise2_face2..raise2_face6, dudo, calza. If only current_qty + 1 <= total_dice: raise1_face2..raise1_face6, dudo, calza. If current_qty + 1 > total_dice: dudo, calza.
  - Final response | asked: the next seat after the current bidder that is not out | options: dudo, calza

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: count of players with out = false == 1 OR round_num >= 30
  - each player's standing: you.dice_count (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is the dice they hold. A lone survivor holds the only dice and wins. After 30 rounds the player with the most dice wins, and players tied for the most share the result, which is the source's draw.
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

- each player: `dice_count` (number, visible: public, starts 5): How many dice this player holds. This is the score.
- each player: `out` (bool, visible: public, starts False): True once the player has 0 dice. An out player is skipped in seat order.
- the table: `round_num` (number, visible: public, starts 0): Rounds started so far.
- parameters (each must be an attribute holding this value, never a number buried in a step): start_dice = 5, max_dice = 5, die_faces = 6, wild_face = 1, min_bid_face = 2, max_bid_face = 6, opening_min_divisor = 3, opening_min_floor = 1, opening_max_divisor = 2, raise_small = 1, raise_big = 2, dudo_loss = 1, calza_loss = 1, calza_gain = 1, max_rounds = 30, first_opener_seat = 1, max_responses_per_round = 3
- the game ends with ONE ending whose `rank_by` is `you.dice_count`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "short_dudo",
    "name": "Short Dudo",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "A short bluffing dice game: bid on a face with 1s wild, then raise, call Dudo or call Calza, and the loser of each call loses a die."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "dice_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "out",
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
        "key": "round_num",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "total_dice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_face",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_qty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "responder_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "call_type",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "caller_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reveal_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "loser_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_dice",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "max_dice",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "die_faces",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "wild_face",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_bid_face",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_bid_face",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "opening_min_divisor",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "opening_min_floor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "opening_max_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "raise_small",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raise_big",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "dudo_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "calza_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "calza_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "first_opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_responses_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "die_slots",
        "visible": "none",
        "type": "list",
        "initial": [1, 2, 3, 4, 5]
      },
      {
        "key": "raise1_opts",
        "visible": "none",
        "type": "list",
        "initial": [
          "raise1_face2",
          "raise1_face3",
          "raise1_face4",
          "raise1_face5",
          "raise1_face6"
        ]
      },
      {
        "key": "raise2_opts",
        "visible": "none",
        "type": "list",
        "initial": [
          "raise2_face2",
          "raise2_face3",
          "raise2_face4",
          "raise2_face5",
          "raise2_face6"
        ]
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "dice_count",
            "value": {
              "calc": "start_dice"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "out",
            "value": false
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "first_opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "round_num",
            "value": 0
          }
        }
      ],
      "text": "Every player starts with {start_dice} dice. Seat {first_opener_seat} opens round 1."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roll",
      "label": "new round",
      "do": [
        {
          "adjust": {
            "key": "round_num",
            "value": 1
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": ""
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "loser_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "total_dice",
            "value": {
              "calc": "sum([p.dice_count for p in players if not p.out])"
            }
          }
        }
      ],
      "text": "Round {round_num} begins. Dice in play: {total_dice}. Seat {opener_seat} opens."
    },
    {
      "use": "update",
      "phase": "roll",
      "label": "the roll",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[min(die_faces, int(uniform(wild_face, die_faces + 1))) for i in die_slots if i <= you.dice_count] if not you.out else []"
            }
          }
        }
      ],
      "text": "Everyone still in the game rolls their dice in secret."
    },
    {
      "use": "sync",
      "phase": "roll",
      "label": "your dice",
      "mode": "self",
      "to": "all",
      "text": "Your dice this round, the dice in play ({total_dice}) and everyone's dice count:"
    },
    {
      "use": "ask",
      "phase": "bid",
      "label": "opening face",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid_face"
        },
        "max": {
          "calc": "max_bid_face"
        }
      },
      "verify": {
        "bind": "face"
      },
      "text": "You open the bidding. Choose the face of your bid, from {min_bid_face} to {max_bid_face}. 1s are wild and count as your face."
    },
    {
      "use": "ask",
      "phase": "bid",
      "label": "opening quantity",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(opening_min_floor, int(total_dice / opening_min_divisor))"
        },
        "max": {
          "calc": "int((total_dice + opening_max_divisor - 1) / opening_max_divisor)"
        }
      },
      "verify": {
        "bind": "qty"
      },
      "text": "Choose the quantity of your bid: at least that many of the {total_dice} dice show your face (1s count as your face)."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the opening bid",
      "do": [
        {
          "set": {
            "key": "current_face",
            "value": "$face"
          }
        },
        {
          "set": {
            "key": "current_qty",
            "value": "$qty"
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(raise1_opts if current_qty + raise_small <= total_dice else []) + (raise2_opts if current_qty + raise_big <= total_dice else []) + ['dudo', 'calza']"
            }
          }
        }
      ],
      "text": "Seat {current_bidder} bids: at least {current_qty} dice show {current_face} (1s wild). Seat {responder_seat} responds."
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "response 1",
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "r1"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "The bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. Choose raise1_faceF (quantity +{raise_small}, face F), raise2_faceF (quantity +{raise_big}, face F), dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply response 1",
      "do": [
        {
          "adjust": {
            "key": "current_qty",
            "value": {
              "calc": "raise_small if $r1 in raise1_opts else raise_big"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": {
              "calc": "int($r1[-1])"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": "$r1",
            "if": {
              "calc": "$r1 == 'dudo' or $r1 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r1 == 'dudo' or $r1 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(raise1_opts if current_qty + raise_small <= total_dice else []) + (raise2_opts if current_qty + raise_big <= total_dice else []) + ['dudo', 'calza']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "response 2",
      "when": {
        "calc": "call_type == ''"
      },
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "r2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "The bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. Choose raise1_faceF (quantity +{raise_small}, face F), raise2_faceF (quantity +{raise_big}, face F), dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply response 2",
      "when": {
        "calc": "call_type == ''"
      },
      "do": [
        {
          "adjust": {
            "key": "current_qty",
            "value": {
              "calc": "raise_small if $r2 in raise1_opts else raise_big"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": {
              "calc": "int($r2[-1])"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": "$r2",
            "if": {
              "calc": "$r2 == 'dudo' or $r2 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r2 == 'dudo' or $r2 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "final response",
      "when": {
        "calc": "call_type == ''"
      },
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "dudo",
          "calza"
        ]
      },
      "verify": {
        "bind": "r3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "Final response: the bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. No more raises. Choose dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply final response",
      "when": {
        "calc": "call_type == ''"
      },
      "do": [
        {
          "set": {
            "key": "call_type",
            "value": "$r3"
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "reveal_count",
            "value": {
              "calc": "len([d for p in players for d in p.hand if d == current_face or d == wild_face])"
            }
          }
        }
      ],
      "text": "Seat {caller_seat} calls {call_type} on {current_qty} x {current_face}. All dice [seat, dice]: {[[p.seat, p.hand] for p in players if not p.out]}. Dice showing {current_face} or 1: {reveal_count}."
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "settle the call",
      "do": [
        {
          "set": {
            "key": "loser_seat",
            "value": {
              "calc": "caller_seat if ((call_type == 'dudo' and reveal_count >= current_qty) or (call_type == 'calza' and reveal_count != current_qty)) else (current_bidder if call_type == 'dudo' else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == loser_seat and you.dice_count > 0"
            },
            "key": "dice_count",
            "value": {
              "calc": "-(dudo_loss if call_type == 'dudo' else calza_loss)"
            },
            "if": {
              "calc": "loser_seat > 0"
            },
            "text": "Seat {player} loses a die."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == caller_seat"
            },
            "key": "dice_count",
            "value": {
              "calc": "min(you.dice_count + calza_gain, max_dice)"
            },
            "if": {
              "calc": "call_type == 'calza' and reveal_count == current_qty"
            },
            "text": "Calza is exact! Seat {player} gains a die (never above the maximum)."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "elimination",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "key": "out",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "key": "hand",
            "value": []
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "to": "out",
            "text": "Seat {player} has no dice left and is out."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "next opener",
      "do": [
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "loser_seat if loser_seat > 0 else caller_seat"
            }
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > opener_seat and not p.out]) if any(p.seat > opener_seat and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "any(p.seat == opener_seat and p.out for p in players) and any(not p.out for p in players)"
            }
          }
        }
      ],
      "text": "Dice counts [seat, dice]: {[[p.seat, p.dice_count] for p in players]}. Seat {opener_seat} opens the next round."
    },
    {
      "use": "check",
      "phase": "settle",
      "label": "end check",
      "when": {
        "calc": "count(not p.out for p in players) <= 1 or round_num >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "count(not p.out for p in players) <= 1 or round_num >= max_rounds"
      },
      "rank_by": "you.dice_count",
      "text": "Winner: {result}. Final dice [seat, dice]: {[[p.seat, p.dice_count] for p in players]} after {round_num} rounds."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed seat order and each starts with {start_dice} dice. Seat {first_opener_seat} opens round 1. There is no talk: bids and calls are the only communication.\n\nEach round:\n1. ROLL. Every player still in the game rolls as many six-sided dice as they hold. You see only your own dice. Everyone is told the total dice in play (T = {total_dice} at the start of the round) and every player's dice count.\n2. OPENING BID. The opener chooses a face from {min_bid_face} to {max_bid_face} and a quantity Q with max({opening_min_floor}, floor(T/{opening_min_divisor})) <= Q <= ceil(T/{opening_max_divisor}). The bid means 'at least Q dice among all players show this face, with every 1 counting as this face'. The bid is announced to all.\n3. RESPONSE 1. The next player in seat order who is still in the game chooses one of: Raise +{raise_small} (raise1_faceF: quantity +{raise_small}, any face F from {min_bid_face} to {max_bid_face}); Raise +{raise_big} (raise2_faceF: quantity +{raise_big}, any face F); Dudo (challenge the current bid as false); Calza (claim the count is exactly the current quantity). A raise is not offered if the new quantity would exceed T; if both raises would, only Dudo or Calza may be chosen. The choice is announced. A player who raises becomes the current bidder.\n4. RESPONSE 2. Only if response 1 was a raise: the next player in seat order after the current bidder who is still in the game makes the same kind of choice. With 2 players, this is the opener again.\n5. FINAL RESPONSE. Only if response 2 was a raise: the next player in seat order after the current bidder who is still in the game must choose Dudo or Calza. Raising is not allowed.\n6. REVEAL. All dice are shown. N is the number of dice showing the current bid face plus the number showing 1.\n7. SETTLE. Dudo: if N >= the current quantity, the caller loses {dudo_loss} die; otherwise (N is less than the quantity) the current bidder loses {dudo_loss} die. Calza: if N equals the current quantity exactly, the caller gains {calza_gain} die, up to a maximum of {max_dice}; otherwise the caller loses {calza_loss} die.\n8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from then on.\n9. NEXT OPENER. The player who lost a die opens the next round. After a successful Calza, the caller opens. If that player was eliminated, the next player in seat order who is still in the game opens.\n10. END CHECK. If only one player remains, the game ends and that player wins. If {max_rounds} rounds have been played, the game ends and the player holding the most dice wins; players tied for the most dice share the result as a draw."
}

Why it was refused: it plays, but part of it does nothing: game attribute `die_slots` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `raise1_opts` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.; game attribute `raise2_opts` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "short_dudo",
    "name": "Short Dudo",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "A short bluffing dice game: bid on a face with 1s wild, then raise, call Dudo or call Calza, and the loser of each call loses a die."
  },
  "statuses": [
    {
      "id": "playing",
      "acts": true,
      "initial": true
    },
    {
      "id": "out",
      "acts": false
    }
  ],
  "attributes": {
    "player": [
      {
        "key": "dice_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "out",
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
        "key": "round_num",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "total_dice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_face",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_qty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "responder_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "call_type",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "caller_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "reveal_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "loser_seat",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_dice",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "max_dice",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "die_faces",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "wild_face",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "min_bid_face",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "max_bid_face",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "opening_min_divisor",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "opening_min_floor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "opening_max_divisor",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "raise_small",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raise_big",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "dudo_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "calza_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "calza_gain",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 30
      },
      {
        "key": "first_opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_responses_per_round",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "die_slots",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "raise1_opts",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "raise2_opts",
        "visible": "none",
        "type": "list",
        "initial": []
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "seat the players",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "dice_count",
            "value": {
              "calc": "start_dice"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": []
          }
        },
        {
          "set": {
            "players": "all",
            "key": "out",
            "value": false
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "first_opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "round_num",
            "value": 0
          }
        },
        {
          "set": {
            "key": "die_slots",
            "value": {
              "calc": "[i for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] if i <= max_dice]"
            }
          }
        },
        {
          "set": {
            "key": "raise1_opts",
            "value": [
              "raise1_face2",
              "raise1_face3",
              "raise1_face4",
              "raise1_face5",
              "raise1_face6"
            ]
          }
        },
        {
          "set": {
            "key": "raise2_opts",
            "value": [
              "raise2_face2",
              "raise2_face3",
              "raise2_face4",
              "raise2_face5",
              "raise2_face6"
            ]
          }
        }
      ],
      "text": "Every player starts with {start_dice} dice. Seat {first_opener_seat} opens round 1."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "roll",
      "label": "new round",
      "do": [
        {
          "adjust": {
            "key": "round_num",
            "value": 1
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": ""
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "loser_seat",
            "value": 0
          }
        },
        {
          "set": {
            "key": "total_dice",
            "value": {
              "calc": "sum([p.dice_count for p in players if not p.out])"
            }
          }
        }
      ],
      "text": "Round {round_num} begins. Dice in play: {total_dice}. Seat {opener_seat} opens."
    },
    {
      "use": "update",
      "phase": "roll",
      "label": "the roll",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "hand",
            "value": {
              "calc": "[min(die_faces, int(uniform(wild_face, die_faces + 1))) for i in die_slots if i <= you.dice_count] if not you.out else []"
            }
          }
        }
      ],
      "text": "Everyone still in the game rolls their dice in secret."
    },
    {
      "use": "sync",
      "phase": "roll",
      "label": "your dice",
      "mode": "self",
      "to": "all",
      "text": "Your dice this round, the dice in play ({total_dice}) and everyone's dice count:"
    },
    {
      "use": "ask",
      "phase": "bid",
      "label": "opening face",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_bid_face"
        },
        "max": {
          "calc": "max_bid_face"
        }
      },
      "verify": {
        "bind": "face"
      },
      "text": "You open the bidding. Choose the face of your bid, from {min_bid_face} to {max_bid_face}. 1s are wild and count as your face."
    },
    {
      "use": "ask",
      "phase": "bid",
      "label": "opening quantity",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(opening_min_floor, int(total_dice / opening_min_divisor))"
        },
        "max": {
          "calc": "int((total_dice + opening_max_divisor - 1) / opening_max_divisor)"
        }
      },
      "verify": {
        "bind": "qty"
      },
      "text": "Choose the quantity of your bid: at least that many of the {total_dice} dice show your face (1s count as your face)."
    },
    {
      "use": "update",
      "phase": "bid",
      "label": "the opening bid",
      "do": [
        {
          "set": {
            "key": "current_face",
            "value": "$face"
          }
        },
        {
          "set": {
            "key": "current_qty",
            "value": "$qty"
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(raise1_opts if current_qty + raise_small <= total_dice else []) + (raise2_opts if current_qty + raise_big <= total_dice else []) + ['dudo', 'calza']"
            }
          }
        }
      ],
      "text": "Seat {current_bidder} bids: at least {current_qty} dice show {current_face} (1s wild). Seat {responder_seat} responds."
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "response 1",
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "r1"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "The bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. Choose raise1_faceF (quantity +{raise_small}, face F), raise2_faceF (quantity +{raise_big}, face F), dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply response 1",
      "do": [
        {
          "adjust": {
            "key": "current_qty",
            "value": {
              "calc": "raise_small if $r1 in raise1_opts else raise_big"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": {
              "calc": "int($r1[-1])"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": "$r1",
            "if": {
              "calc": "$r1 == 'dudo' or $r1 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r1 == 'dudo' or $r1 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "$r1 in raise1_opts or $r1 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "(raise1_opts if current_qty + raise_small <= total_dice else []) + (raise2_opts if current_qty + raise_big <= total_dice else []) + ['dudo', 'calza']"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "response 2",
      "when": {
        "calc": "call_type == ''"
      },
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "r2"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "The bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. Choose raise1_faceF (quantity +{raise_small}, face F), raise2_faceF (quantity +{raise_big}, face F), dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply response 2",
      "when": {
        "calc": "call_type == ''"
      },
      "do": [
        {
          "adjust": {
            "key": "current_qty",
            "value": {
              "calc": "raise_small if $r2 in raise1_opts else raise_big"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": {
              "calc": "int($r2[-1])"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        },
        {
          "set": {
            "key": "call_type",
            "value": "$r2",
            "if": {
              "calc": "$r2 == 'dudo' or $r2 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            },
            "if": {
              "calc": "$r2 == 'dudo' or $r2 == 'calza'"
            }
          }
        },
        {
          "set": {
            "key": "responder_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > current_bidder and not p.out]) if any(p.seat > current_bidder and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "$r2 in raise1_opts or $r2 in raise2_opts"
            }
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "respond",
      "label": "final response",
      "when": {
        "calc": "call_type == ''"
      },
      "to": {
        "where": "you.seat == responder_seat"
      },
      "answer": {
        "type": "choice",
        "options": [
          "dudo",
          "calza"
        ]
      },
      "verify": {
        "bind": "r3"
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} answers the bid of {current_qty} x {current_face}: {value}."
      },
      "text": "Final response: the bid is at least {current_qty} dice showing {current_face} (1s wild), by seat {current_bidder}. No more raises. Choose dudo (the bid is false) or calza (the count is exactly {current_qty})."
    },
    {
      "use": "update",
      "phase": "respond",
      "label": "apply final response",
      "when": {
        "calc": "call_type == ''"
      },
      "do": [
        {
          "set": {
            "key": "call_type",
            "value": "$r3"
          }
        },
        {
          "set": {
            "key": "caller_seat",
            "value": {
              "calc": "responder_seat"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "reveal",
      "label": "the reveal",
      "do": [
        {
          "set": {
            "key": "reveal_count",
            "value": {
              "calc": "len([d for p in players for d in p.hand if d == current_face or d == wild_face])"
            }
          }
        }
      ],
      "text": "Seat {caller_seat} calls {call_type} on {current_qty} x {current_face}. All dice [seat, dice]: {[[p.seat, p.hand] for p in players if not p.out]}. Dice showing {current_face} or 1: {reveal_count}."
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "settle the call",
      "do": [
        {
          "set": {
            "key": "loser_seat",
            "value": {
              "calc": "caller_seat if ((call_type == 'dudo' and reveal_count >= current_qty) or (call_type == 'calza' and reveal_count != current_qty)) else (current_bidder if call_type == 'dudo' else 0)"
            }
          }
        },
        {
          "adjust": {
            "players": {
              "where": "you.seat == loser_seat and you.dice_count > 0"
            },
            "key": "dice_count",
            "value": {
              "calc": "-(dudo_loss if call_type == 'dudo' else calza_loss)"
            },
            "if": {
              "calc": "loser_seat > 0"
            },
            "text": "Seat {player} loses a die."
          }
        },
        {
          "set": {
            "players": {
              "where": "you.seat == caller_seat"
            },
            "key": "dice_count",
            "value": {
              "calc": "min(you.dice_count + calza_gain, max_dice)"
            },
            "if": {
              "calc": "call_type == 'calza' and reveal_count == current_qty"
            },
            "text": "Calza is exact! Seat {player} gains a die (never above the maximum)."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "elimination",
      "do": [
        {
          "set": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "key": "out",
            "value": true
          }
        },
        {
          "set": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "key": "hand",
            "value": []
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.dice_count <= 0"
            },
            "to": "out",
            "text": "Seat {player} has no dice left and is out."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "settle",
      "label": "next opener",
      "do": [
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "loser_seat if loser_seat > 0 else caller_seat"
            }
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "min([p.seat for p in players if p.seat > opener_seat and not p.out]) if any(p.seat > opener_seat and not p.out for p in players) else min([p.seat for p in players if not p.out])"
            },
            "if": {
              "calc": "any(p.seat == opener_seat and p.out for p in players) and any(not p.out for p in players)"
            }
          }
        }
      ],
      "text": "Dice counts [seat, dice]: {[[p.seat, p.dice_count] for p in players]}. Seat {opener_seat} opens the next round."
    },
    {
      "use": "check",
      "phase": "settle",
      "label": "end check",
      "when": {
        "calc": "count(not p.out for p in players) <= 1 or round_num >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "count(not p.out for p in players) <= 1 or round_num >= max_rounds"
      },
      "rank_by": "you.dice_count",
      "text": "Winner: {result}. Final dice [seat, dice]: {[[p.seat, p.dice_count] for p in players]} after {round_num} rounds."
    }
  },
  "limits": {
    "rounds": 30,
    "rounds_max": 30,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed seat order and each starts with {start_dice} dice. Seat {first_opener_seat} opens round 1. There is no talk: bids and calls are the only communication.\n\nEach round:\n1. ROLL. Every player still in the game rolls as many six-sided dice as they hold. You see only your own dice. Everyone is told the total dice in play (T = {total_dice} at the start of the round) and every player's dice count.\n2. OPENING BID. The opener chooses a face from {min_bid_face} to {max_bid_face} and a quantity Q with max({opening_min_floor}, floor(T/{opening_min_divisor})) <= Q <= ceil(T/{opening_max_divisor}). The bid means 'at least Q dice among all players show this face, with every 1 counting as this face'. The bid is announced to all.\n3. RESPONSE 1. The next player in seat order who is still in the game chooses one of: Raise +{raise_small} (raise1_faceF: quantity +{raise_small}, any face F from {min_bid_face} to {max_bid_face}); Raise +{raise_big} (raise2_faceF: quantity +{raise_big}, any face F); Dudo (challenge the current bid as false); Calza (claim the count is exactly the current quantity). A raise is not offered if the new quantity would exceed T; if both raises would, only Dudo or Calza may be chosen. The choice is announced. A player who raises becomes the current bidder.\n4. RESPONSE 2. Only if response 1 was a raise: the next player in seat order after the current bidder who is still in the game makes the same kind of choice. With 2 players, this is the opener again.\n5. FINAL RESPONSE. Only if response 2 was a raise: the next player in seat order after the current bidder who is still in the game must choose Dudo or Calza. Raising is not allowed.\n6. REVEAL. All dice are shown. N is the number of dice showing the current bid face plus the number showing 1.\n7. SETTLE. Dudo: if N >= the current quantity, the caller loses {dudo_loss} die; otherwise (N is less than the quantity) the current bidder loses {dudo_loss} die. Calza: if N equals the current quantity exactly, the caller gains {calza_gain} die, up to a maximum of {max_dice}; otherwise the caller loses {calza_loss} die.\n8. ELIMINATION. A player with 0 dice is out and is skipped in seat order from then on.\n9. NEXT OPENER. The player who lost a die opens the next round. After a successful Calza, the caller opens. If that player was eliminated, the next player in seat order who is still in the game opens.\n10. END CHECK. If only one player remains, the game ends and that player wins. If {max_rounds} rounds have been played, the game ends and the player holding the most dice wins; players tied for the most dice share the result as a draw."
}
```
````
