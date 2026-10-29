# 09 coder

- time: 2026-10-28T05:32:53+00:00 (81.4s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 ed54966555779de7, reply sha256 b426df55d9ade4c8

## Sent

````
# Task: write the XColos game file for "Open-Table Dudo"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 4; set `meta.players` to {"min": 2, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: Seat the players in a random order, numbered seat 1 upward, with clockwise meaning increasing seat number and wrapping from the last seat to seat 1. Starting dice depend on the number of players: 2 players start with 4 dice each, 3 players with 3 each, 4 players with 2 each. Every player rolls their dice (six-sided, faces 1 to 6). Each player is privately shown their own faces and no one else's. Seat 1 is the opener of the first hand.

PUBLIC INFORMATION: At every turn all players are told how many dice each player holds, the total number of dice in play (T), the current bid and who made it (if any), and the list of bids made so far in this hand.

BIDS: A bid is a quantity and a face from 2 to 6, for example 'three 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face. Ones cannot be named as a bid face.

EACH ROUND IS ONE TURN by the player to act.
(a) If there is no current bid, the player to act is the opener and must make an opening bid. The quantity must be at least max(1, floor(T / 4)) and at most T. If the opener calls Dudo instead, or makes an invalid bid, the opener loses one die and the hand ends with no count.
(b) If there is a current bid, the player to act either raises or calls 'Dudo'. A raise is a new bid whose quantity is at least the current quantity plus 1 and at most T, with any face from 2 to 6. An invalid raise counts as a Dudo call. If the current quantity already equals T, the player must call Dudo.
(c) After a valid bid or raise, it becomes the current bid, and the next surviving player clockwise is the player to act in the next round. Bidding wraps around the table as many times as needed.
(d) DUDO: When a player calls Dudo on the current bid, all dice are revealed to everyone. Count the dice showing the bid face plus all ones. If the count is at least the bid quantity, the bid was true and the caller loses one die. Otherwise the bid was false and the bidder loses one die. The hand ends.

AFTER A HAND ENDS (this happens in the same round as the Dudo call or failed opening): A player with 0 dice is eliminated, and this is announced. The player who lost the die becomes the opener of the next hand. If that player was eliminated, the next surviving player clockwise from them is the opener. The current bid is cleared. Every surviving player rolls all their remaining dice and is privately shown their own faces. T is recomputed. The opener acts in the next round.

END: The game ends immediately when only one player has dice left. The game also ends after round 40. In that case any hand still in progress is not resolved and its bids are ignored.

How the winner is decided: The last player with at least one die wins, and every other player loses. If the game ends after round 40 with more than one player holding dice, the player holding the most dice wins. If several players are tied for the most dice, it is a draw among those tied and every other player loses.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Open-Table Dudo (2 to 4 players, best with 3)

Bluffing dice game: players secretly roll dice, raise bids on how many dice show a face (ones are wild), and call Dudo to challenge; each lost challenge costs a die, and the last player with dice wins.

STATE (every item below must exist in the file):
  - each player: dice (number, starts '6 - player_count (4 with 2 players, 3 with 3, 2 with 4)'); everyone sees it. How many dice this player still holds; 0 means eliminated
  - each player: faces (list, starts 'dice random integers from 1 to 6'); only its owner sees it. This player's current rolled faces, shown only to the owner until a Dudo reveals them
  - each player: eliminated (bool, starts False); everyone sees it. True once the player has 0 dice
  - the table: round_no (number, starts 0); everyone sees it. Number of rounds (turns) played so far
  - the table: total_dice (number, starts 'sum of dice over all players'); everyone sees it. T, the total number of dice in play
  - the table: to_act (number, starts 1); everyone sees it. Seat of the player to act this round
  - the table: opener (number, starts 1); everyone sees it. Seat that opens the current hand
  - the table: current_qty (number, starts 0); everyone sees it. Quantity of the current bid; 0 means no current bid
  - the table: current_face (number, starts 0); everyone sees it. Face of the current bid (2 to 6); 0 means no bid
  - the table: current_bidder (number, starts 0); everyone sees it. Seat that made the current bid; 0 means none
  - the table: bids (list, starts []); everyone sees it. Bids made so far in this hand, as 'seat: quantity x face'
  - the table: action (text, starts ''); everyone sees it. This round's choice by the player to act: bid, raise or dudo
  - the table: bid_qty (number, starts 0); everyone sees it. Quantity named this round
  - the table: bid_face (number, starts 0); everyone sees it. Face named this round
  - the table: matching (number, starts 0); everyone sees it. At a Dudo, the count of revealed dice showing the bid face or 1
  - the table: loser (number, starts 0); everyone sees it. Seat that lost a die when the hand ended; 0 while the hand is in progress
  - the table: survivors (number, starts 'player_count'); everyone sees it. Number of players with at least one die
  - parameters, each kept as a table attribute: start_dice_2_players = 4, start_dice_3_players = 3, start_dice_4_players = 2, die_sides = 6, wild_face = 1, bid_face_min = 2, bid_face_max = 6, opening_quantity_divisor = 4, opening_quantity_floor = 1, raise_quantity_step = 1, dice_lost_per_challenge = 1, max_rounds = 40

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players in random order, numbered seat 1 upward; clockwise means increasing seat number, wrapping from the last seat to seat 1.
  2. Each player's dice is set to 6 minus the player count: 4 with 2 players, 3 with 3, 2 with 4.
  3. Each player's faces is set to that many random integers from 1 to 6 and is shown privately to its owner only.
  4. total_dice is set to the sum of dice; opener and to_act are set to 1; current_qty, current_face and current_bidder are set to 0; bids is emptied; survivors is set to the player count.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: round_no += 1; loser = 0; action = ''; bid_qty = 0; bid_face = 0
  2. [tell] all players. What happens: Announce each seat's dice, total_dice (T), the current bid (current_qty x current_face by current_bidder, or 'none'), bids, and that seat to_act is to act
  3. [ask] seat to_act answers: choice: 'bid' or 'dudo' when current_qty = 0; 'raise' or 'dudo' when 0 < current_qty < total_dice; only 'dudo' when current_qty = total_dice. What happens: action = the choice
  4. [ask] seat to_act, when action is 'bid' or 'raise' answers: whole number from max(1, floor(total_dice / 4)) to total_dice when action = 'bid'; from current_qty + 1 to total_dice when action = 'raise'. What happens: bid_qty = the number
  5. [ask] seat to_act, when action is 'bid' or 'raise' answers: whole number from 2 to 6. What happens: bid_face = the number
  6. [update] table, when action is 'bid' or 'raise'. What happens: current_qty = bid_qty; current_face = bid_face; current_bidder = to_act; append 'seat to_act: bid_qty x bid_face' to bids; to_act = the next seat clockwise from to_act with eliminated = false; announce the new bid
  7. [update] table, when action = 'dudo' and current_qty = 0. What happens: Failed opening: loser = to_act; that player's dice -= 1; announce that the opener lost a die with no count
  8. [update] table, when action = 'dudo' and current_qty > 0. What happens: Reveal every player's faces to all; matching = number of faces over all surviving players equal to current_face or to 1; if matching >= current_qty then loser = to_act (the caller), else loser = current_bidder; the loser's dice -= 1; announce the reveal, matching, and the loser
  9. [update] table, when loser > 0. What happens: Every player with dice = 0 gets eliminated = true, announced; survivors = number of players with dice >= 1
  10. [check] table. What happens: End the game if survivors = 1
  11. [update] table, when loser > 0. What happens: opener = loser if the loser has eliminated = false, else the next seat clockwise from loser with eliminated = false; current_qty = 0; current_face = 0; current_bidder = 0; empty bids; each surviving player's faces = dice new random integers from 1 to 6, shown privately to the owner; total_dice = sum of dice; to_act = opener
  12. [sync] all players. What happens: Each player is sent their own faces and the public state
  13. [check] table. What happens: End the game if round_no >= 40; a hand still in progress is not resolved

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts with 2, 3 or 4 players, then each player holds 4, 3 or 2 dice respectively.
  R2. When dice are rolled, then each die shows a face from 1 to 6, and each player sees only their own faces.
  R3. When the game starts, then seat 1 is the opener and acts in round 1.
  R4. When there is no current bid, then the player to act must make an opening bid with quantity from max(1, floor(T/4)) to T and face from 2 to 6, or call Dudo.
  R5. When the opener calls Dudo with no current bid, then the opener loses 1 die and the hand ends with no count.
  R6. When there is a current bid of quantity q with q < T, then the player to act either raises with quantity from q+1 to T and any face from 2 to 6, or calls Dudo.
  R7. When the current bid's quantity equals T, then the player to act must call Dudo.
  R8. When a valid bid or raise is made, then it becomes the current bid, it is added to the hand's bid list, and the next surviving seat clockwise acts next round.
  R9. When Dudo is called on a bid of q dice of face f, then all dice are revealed, and the count is the dice showing f plus all dice showing 1.
  R10. When at a Dudo the count is at least q, then the caller loses 1 die; otherwise the bidder loses 1 die.
  R11. When a player reaches 0 dice, then that player is eliminated and this is announced.
  R12. When a hand ends, then the player who lost the die opens the next hand, or the next surviving seat clockwise from them if they were eliminated.
  R13. When a hand ends, then the current bid and bid list are cleared, every surviving player rerolls all their dice privately, and T is recomputed.
  R14. When only one player has dice left, then the game ends immediately and that player wins.
  R15. When round 40 ends with more than one player holding dice, then the game ends, the hand in progress is not resolved, and the player(s) with the most dice win, sharing the win if tied.
  R16. At every turn, all players are told each player's dice count, T, the current bid and who made it, and this hand's bid list.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Choose an action | asked: seat to_act | options: with no current bid: bid, dudo; with a current bid below T: raise, dudo; with a current bid equal to T: dudo
  - Bid quantity | asked: seat to_act after choosing bid or raise | options: opening bid: max(1, floor(T/4)) to T; raise: current_qty + 1 to T
  - Bid face | asked: seat to_act after choosing bid or raise | options: 2, 3, 4, 5, 6

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: survivors = 1 or round_no >= 40
  - each player's standing: you.dice (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is the number of dice they hold. If only one player has dice, they win alone. If round 40 ends with several players holding dice, the player with the most dice wins, and players tied for the most share the win (a draw among them). Every other player loses.
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

- each player: `dice` (number, visible: public, starts '6 - player_count (4 with 2 players, 3 with 3, 2 with 4)'): How many dice this player still holds; 0 means eliminated
- each player: `eliminated` (bool, visible: public, starts False): True once the player has 0 dice
- the table: `round_no` (number, visible: public, starts 0): Number of rounds (turns) played so far
- the table: `survivors` (number, visible: public, starts 'player_count'): Number of players with at least one die
- parameters (each must be an attribute holding this value, never a number buried in a step): start_dice_2_players = 4, start_dice_3_players = 3, start_dice_4_players = 2, die_sides = 6, wild_face = 1, bid_face_min = 2, bid_face_max = 6, opening_quantity_divisor = 4, opening_quantity_floor = 1, raise_quantity_step = 1, dice_lost_per_challenge = 1, max_rounds = 40
- the game ends with ONE ending whose `rank_by` is `you.dice`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
    "id": "open_table_dudo",
    "name": "Open-Table Dudo",
    "players": {
      "min": 2,
      "max": 4,
      "suggested": 3
    },
    "blurb": "Roll hidden dice, raise bids on how many show a face (ones are wild), call Dudo to challenge; last player with dice wins."
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
        "key": "dice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "faces",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "eliminated",
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
        "key": "round_no",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "total_dice",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "to_act",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "opener",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "current_qty",
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
        "key": "current_bidder",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bids",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "action",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "bid_qty",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bid_face",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "matching",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "loser",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "survivors",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "start_dice_2_players",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "start_dice_3_players",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "start_dice_4_players",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "die_sides",
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
        "key": "bid_face_min",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "bid_face_max",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "opening_quantity_divisor",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "opening_quantity_floor",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "raise_quantity_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "dice_lost_per_challenge",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 40
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "starting dice",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "dice",
            "value": {
              "calc": "start_dice_2_players if len(players) == 2 else (start_dice_3_players if len(players) == 3 else start_dice_4_players)"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the first roll",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "faces",
            "value": {
              "calc": "[min(die_sides, int(uniform(wild_face, die_sides + 1))) for i in [1, 2, 3, 4] if i <= you.dice]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the table",
      "do": [
        {
          "set": {
            "key": "total_dice",
            "value": {
              "calc": "sum(p.dice for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "opener",
            "value": 1
          }
        },
        {
          "set": {
            "key": "to_act",
            "value": 1
          }
        },
        {
          "set": {
            "key": "current_qty",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bids",
            "value": []
          }
        },
        {
          "set": {
            "key": "survivors",
            "value": {
              "calc": "len(players)"
            }
          }
        }
      ]
    },
    {
      "use": "sync",
      "label": "your dice",
      "mode": "self",
      "to": "all",
      "text": "You start with (your faces are shown to you alone):"
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "turn",
      "label": "a new turn",
      "do": [
        {
          "adjust": {
            "key": "round_no",
            "value": 1
          }
        },
        {
          "set": {
            "key": "loser",
            "value": 0
          }
        },
        {
          "set": {
            "key": "action",
            "value": ""
          }
        },
        {
          "set": {
            "key": "bid_qty",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bid_face",
            "value": 0
          }
        },
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['bid', 'dudo'] if current_qty == 0 else (['raise', 'dudo'] if current_qty < total_dice else ['dudo'])"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "turn",
      "label": "the table state",
      "to": "all",
      "text": "Round {round_no}. Dice held [seat, dice]: {[[p.seat, p.dice] for p in players]}. Total dice T = {total_dice}. Current bid: {current_qty} x {current_face}s by seat {current_bidder} (0 means no bid yet). Bids this hand [seat, quantity, face]: {bids}. Seat {to_act} is to act."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "choose an action",
      "to": {
        "where": "you.seat == to_act"
      },
      "answer": {
        "type": "choice",
        "options": {
          "attribute": "offer"
        }
      },
      "verify": {
        "bind": "act_choice"
      },
      "text": "It is your turn. Current bid: {current_qty} x {current_face}s (0 means none), T = {total_dice}. Choose: 'bid' to open, 'raise' to beat the current bid, or 'dudo' to challenge it."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "record the action",
      "do": [
        {
          "set": {
            "key": "action",
            "value": "$act_choice"
          }
        }
      ]
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "bid quantity",
      "when": {
        "calc": "action in ['bid', 'raise']"
      },
      "to": {
        "where": "you.seat == to_act"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "max(opening_quantity_floor, int(total_dice / opening_quantity_divisor)) if action == 'bid' else current_qty + raise_quantity_step"
        },
        "max": {
          "calc": "total_dice"
        }
      },
      "verify": {
        "bind": "q"
      },
      "text": "Name the quantity of your bid: how many dice on the whole table (ones wild) show your face."
    },
    {
      "use": "ask",
      "phase": "turn",
      "label": "bid face",
      "when": {
        "calc": "action in ['bid', 'raise']"
      },
      "to": {
        "where": "you.seat == to_act"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "bid_face_min"
        },
        "max": {
          "calc": "bid_face_max"
        }
      },
      "verify": {
        "bind": "f"
      },
      "text": "Name the face of your bid, from {bid_face_min} to {bid_face_max} (ones are wild and cannot be named)."
    },
    {
      "use": "update",
      "phase": "turn",
      "label": "the new bid",
      "when": {
        "calc": "action in ['bid', 'raise']"
      },
      "do": [
        {
          "set": {
            "key": "bid_qty",
            "value": "$q"
          }
        },
        {
          "set": {
            "key": "bid_face",
            "value": "$f"
          }
        },
        {
          "set": {
            "key": "current_qty",
            "value": {
              "calc": "bid_qty"
            }
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": {
              "calc": "bid_face"
            }
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": {
              "calc": "to_act"
            }
          }
        },
        {
          "append": {
            "key": "bids",
            "value": {
              "calc": "[to_act, bid_qty, bid_face]"
            }
          }
        },
        {
          "set": {
            "key": "to_act",
            "value": {
              "calc": "(sorted([p.seat for p in players if p.seat > to_act and not p.eliminated]) + sorted([p.seat for p in players if not p.eliminated]))[0]"
            },
            "text": "New bid: {current_qty} x {current_face}s by seat {current_bidder}. Seat {to_act} acts next."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "failed opening",
      "when": {
        "calc": "action == 'dudo' and current_qty == 0"
      },
      "do": [
        {
          "set": {
            "key": "loser",
            "value": {
              "calc": "to_act"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "loser"
            },
            "key": "dice",
            "value": {
              "calc": "-dice_lost_per_challenge"
            },
            "if": {
              "calc": "loser > 0"
            },
            "text": "Seat {player} called Dudo with no bid to open and loses a die. The hand ends with no count."
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "dudo",
      "when": {
        "calc": "action == 'dudo' and current_qty > 0"
      },
      "do": [
        {
          "set": {
            "key": "matching",
            "value": {
              "calc": "sum(count(x == current_face or x == wild_face for x in p.faces) for p in players if not p.eliminated)"
            }
          }
        },
        {
          "set": {
            "key": "loser",
            "value": {
              "calc": "to_act if matching >= current_qty else current_bidder"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "loser"
            },
            "key": "dice",
            "value": {
              "calc": "-dice_lost_per_challenge"
            },
            "if": {
              "calc": "loser > 0"
            }
          }
        }
      ],
      "text": "Seat {to_act} calls Dudo on {current_qty} x {current_face}s by seat {current_bidder}. All dice revealed [seat, faces]: {[[p.seat, p.faces] for p in players if not p.eliminated]}. Dice showing {current_face} or 1: {matching}. Seat {loser} loses a die."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "eliminations",
      "when": {
        "calc": "loser > 0"
      },
      "do": [
        {
          "set": {
            "players": {
              "where": "you.dice == 0 and not you.eliminated"
            },
            "key": "eliminated",
            "value": true,
            "text": "Seat {player} has no dice left and is eliminated."
          }
        },
        {
          "set_status": {
            "players": {
              "where": "you.dice == 0"
            },
            "to": "out"
          }
        },
        {
          "set": {
            "key": "survivors",
            "value": {
              "calc": "count(p.dice >= 1 for p in players)"
            }
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "last player standing",
      "when": {
        "calc": "survivors <= 1"
      },
      "against": [
        "over"
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the next hand",
      "when": {
        "calc": "loser > 0"
      },
      "do": [
        {
          "set": {
            "key": "opener",
            "value": {
              "calc": "loser if loser in [p.seat for p in players if not p.eliminated] else (sorted([p.seat for p in players if p.seat > loser and not p.eliminated]) + sorted([p.seat for p in players if not p.eliminated]))[0]"
            }
          }
        },
        {
          "set": {
            "key": "current_qty",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_face",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_bidder",
            "value": 0
          }
        },
        {
          "set": {
            "key": "bids",
            "value": []
          }
        },
        {
          "set": {
            "players": {
              "where": "not you.eliminated"
            },
            "key": "faces",
            "value": {
              "calc": "[min(die_sides, int(uniform(wild_face, die_sides + 1))) for i in [1, 2, 3, 4] if i <= you.dice]"
            }
          }
        },
        {
          "set": {
            "key": "total_dice",
            "value": {
              "calc": "sum(p.dice for p in players)"
            }
          }
        },
        {
          "set": {
            "key": "to_act",
            "value": {
              "calc": "opener"
            }
          }
        }
      ],
      "text": "A new hand: everyone rerolls. Seat {opener} opens. T = {total_dice}."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "round cap",
      "when": {
        "calc": "round_no >= max_rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "survivors <= 1 or round_no >= max_rounds"
      },
      "rank_by": "you.dice",
      "text": "Winner: {result}. Dice left [seat, dice]: {[[p.seat, p.dice] for p in players]}."
    }
  },
  "limits": {
    "rounds": 40,
    "rounds_max": 40,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Players sit in seats numbered from 1; clockwise means increasing seat number, wrapping from the last seat to seat 1. With 2 players each starts with {start_dice_2_players} dice, with 3 players {start_dice_3_players}, with 4 players {start_dice_4_players}. Every player rolls their dice (faces 1 to {die_sides}) and sees only their own faces. Seat 1 opens the first hand.\n\nAt every turn everyone is told how many dice each player holds, the total dice in play (T), the current bid and who made it, and the bids made so far this hand.\n\nA bid is a quantity and a face from {bid_face_min} to {bid_face_max}, e.g. 'three 5s'. It claims that at least that many dice on the whole table show that face. Ones are wild and count toward every face; ones cannot be named as a bid face.\n\nEach round is one turn by the player to act.\n(a) With no current bid, the player to act is the opener and must make an opening bid: quantity at least max({opening_quantity_floor}, floor(T / {opening_quantity_divisor})) and at most T. If the opener calls Dudo instead, the opener loses {dice_lost_per_challenge} die and the hand ends with no count.\n(b) With a current bid, the player to act either raises or calls Dudo. A raise has quantity at least the current quantity plus {raise_quantity_step} and at most T, with any face from {bid_face_min} to {bid_face_max}. If the current quantity already equals T, the player must call Dudo.\n(c) A bid or raise becomes the current bid and is added to the hand's bid list, and the next surviving player clockwise acts next round. Bidding wraps around the table as often as needed.\n(d) DUDO: all dice are revealed to everyone. Count the dice showing the bid face plus all ones. If the count is at least the bid quantity, the bid was true and the caller loses {dice_lost_per_challenge} die. Otherwise the bid was false and the bidder loses {dice_lost_per_challenge} die. The hand ends.\n\nAfter a hand ends (in the same round): a player with 0 dice is eliminated, and this is announced. The player who lost the die opens the next hand; if that player was eliminated, the next surviving player clockwise from them opens. The current bid is cleared, every surviving player rerolls all their remaining dice privately, and T is recomputed. The opener acts next round.\n\nThe game ends immediately when only one player has dice left; that player wins and everyone else loses. The game also ends after round {max_rounds}: any hand in progress is not resolved and its bids are ignored, and the player holding the most dice wins; players tied for the most share the win, and everyone else loses."
}
```
````
