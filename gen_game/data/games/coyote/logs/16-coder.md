# 16 coder

- time: 2026-10-27T09:00:32+00:00 (70.7s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 66edf44aadf98692, reply sha256 9b2fd39762c5684d

## Sent

````
# Task: write the XColos game file for "Coyote Lap"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

DECK (33 cards): one -10, two -5, three 0, four each of 1, 2, 3, 4 and 5, three 10, two 15, one 20, and one special card 'Max→0'.

SETUP: Seat players in a fixed clockwise order. Each player starts with 0 Coyote tokens. The player in seat 1 opens hand 1. The game lasts exactly 12 hands.

EACH HAND:
1. Deal: shuffle the full 33-card deck and deal one card face down to each player.
2. Bandana: each player is told privately the cards of all other players, but never their own card.
3. Opening declaration: the opener declares a whole number from -30 to 60, a claim about the TRUE TOTAL of all cards in play this hand.
4. Responses: each other player, one at a time in clockwise order from the opener, chooses one of two options:
   (a) RAISE: declare a whole number strictly higher than the current declaration, at most 60. It becomes the current declaration, and this player becomes the current declarer.
   (b) CALL COYOTE: challenge the current declaration. Bidding stops immediately, and later players do not act this hand.
   Every declaration is announced to all players as it is made.
5. Automatic call: if every responder raised, the opener is treated as having called Coyote on the final declaration.
6. True total: add up the numbers on all cards in play. If the 'Max→0' card is in play, it counts as 0 itself, and the highest-valued other card in play also counts as 0. If several cards tie for highest, only one of them counts as 0. If the highest other card is negative, it still becomes 0.
7. Resolution: if the true total is LESS than the current declaration, the current declarer takes 1 Coyote token. Otherwise the caller, or the opener in the case of an automatic call, takes 1 Coyote token.
8. Reveal: all cards, the true total and the token taken are announced to everyone.
9. Rotate: the next player clockwise opens the next hand.

END: After hand 12, the game ends.

How the winner is decided: After 12 hands, the player with the fewest Coyote tokens wins. If two or more players tie for the fewest, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Coyote Lap (3 to 4 players, best with 4)

Each player sees every card but their own. Players bid upward on the true total of the cards in play until someone calls Coyote, and whoever is wrong takes a token. After 12 hands the fewest tokens wins.

STATE (every item below must exist in the file):
  - each player: tokens (number, starts 0); everyone sees it. Coyote tokens taken so far (fewer is better)
  - each player: card (number, starts 0); everyone but its owner sees it. The card dealt this hand, as its face value, or 100 for the special 'Max→0' card. Every other player sees it; the owner does not (the bandana).
  - the table: deck (list, starts [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]); hidden from all players. The undealt cards of the 33-card deck (100 = 'Max→0')
  - the table: hand_number (number, starts 1); everyone sees it. The current hand, from 1 to 12
  - the table: opener_seat (number, starts 1); everyone sees it. Seat that opens this hand
  - the table: current_declaration (number, starts 0); everyone sees it. The highest declaration made so far this hand
  - the table: current_declarer (number, starts 0); everyone sees it. Seat that made the current declaration
  - the table: bidding_open (bool, starts False); everyone sees it. True while nobody has called Coyote this hand
  - the table: caller (number, starts 0); everyone sees it. Seat that called Coyote, or the opener on an automatic call
  - the table: true_total (number, starts 0); everyone sees it. The true total of the cards in play, computed after bidding
  - the table: hand_loser (number, starts 0); everyone sees it. Seat that took the token this hand
  - parameters, each kept as a table attribute: deck_size = 33, count_minus_10 = 1, count_minus_5 = 2, count_0 = 3, count_each_1_to_5 = 4, count_10 = 3, count_15 = 2, count_20 = 1, count_max_to_zero = 1, max_to_zero_code = 100, hands = 12, declaration_min = -30, declaration_max = 60, raise_min_step = 1, tokens_per_loss = 1, starting_tokens = 0, cards_per_player = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seat the players in a fixed clockwise order, seats 1 to N.
  2. Every player's tokens is set to 0.
  3. hand_number is set to 1 and opener_seat to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Reset deck to the full 33-card list. For each player, draw one card at random from deck: set that player's card to its value and remove it from deck. Set caller = 0, current_declarer = 0, hand_loser = 0, true_total = 0, bidding_open = true.
  2. [sync] all players. What happens: Each player privately sees the card of every other player (card is visible to others) but never their own.
  3. [ask] the opener (seat opener_seat) answers: a whole number from -30 to 60. What happens: Set current_declaration = answer and current_declarer = opener_seat. Announce to all: 'Seat {opener_seat} opens at {current_declaration}.'
  4. [ask] responder 1: seat ((opener_seat) mod N) + 1, when bidding_open answers: a choice: raise or call_coyote (raise is offered only if current_declaration < 60). What happens: If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
  5. [ask] responder 1, when bidding_open and they chose raise answers: a whole number from current_declaration + 1 to 60. What happens: Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
  6. [ask] responder 2: seat ((opener_seat + 1) mod N) + 1, when bidding_open answers: a choice: raise or call_coyote (raise is offered only if current_declaration < 60). What happens: If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
  7. [ask] responder 2, when bidding_open and they chose raise answers: a whole number from current_declaration + 1 to 60. What happens: Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
  8. [ask] responder 3: seat ((opener_seat + 2) mod N) + 1, only when N = 4 and bidding_open answers: a choice: raise or call_coyote (raise is offered only if current_declaration < 60). What happens: If call_coyote: set caller = this seat, set bidding_open = false, and announce the call. If raise: go on to the next step.
  9. [ask] responder 3, only when N = 4, bidding_open and they chose raise answers: a whole number from current_declaration + 1 to 60. What happens: Set current_declaration = answer and current_declarer = this seat. Announce the declaration to all.
  10. [update] the opener, when bidding_open. What happens: Automatic call: set caller = opener_seat and bidding_open = false. Announce: 'Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}.'
  11. [update] table. What happens: true_total = sum of every card that is not 100. If some player's card = 100, subtract the maximum of the other players' cards (exactly one copy of the highest, even if that value is negative).
  12. [update] table. What happens: If true_total < current_declaration: the current_declarer's tokens += 1 and hand_loser = current_declarer. Otherwise: the caller's tokens += 1 and hand_loser = caller.
  13. [tell] all players. What happens: Reveal every player's card (100 shown as 'Max→0'), plus true_total, current_declaration and hand_loser: 'Cards: {cards}. True total {true_total} against a declaration of {current_declaration}. Seat {hand_loser} takes a Coyote token.'
  14. [update] table. What happens: opener_seat = (opener_seat mod N) + 1; hand_number += 1.
  15. [check] table. What happens: If hand_number > 12, end the game; otherwise continue to the next hand.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, every player has 0 tokens, hand_number is 1 and opener_seat is 1.
  R2. When a hand begins, the deck is reset to the 33 cards (one -10, two -5, three 0, four each of 1 to 5, three 10, two 15, one 20, one Max→0), and each player is dealt exactly 1 card that is removed from the deck.
  R3. When cards are dealt, each player can see every other player's card but not their own.
  R4. When the opener declares, the value must be a whole number from -30 to 60, and the opener becomes current_declarer.
  R5. When a responder raises, the new declaration must be a whole number strictly greater than current_declaration and at most 60, and that responder becomes current_declarer.
  R6. When current_declaration is 60, a responder is offered only call_coyote.
  R7. When a responder calls Coyote, bidding stops and no later responder acts this hand.
  R8. When every responder raises, the opener is the caller (an automatic call) on the final declaration.
  R9. When no Max→0 card is in play, true_total is the plain sum of all cards in play (for example, cards 5, 10 and -5 give 10).
  R10. When the Max→0 card is in play, it counts 0 and exactly one copy of the highest other card counts 0 (for example, Max→0, 15, 15 and 3 give 18).
  R11. When the Max→0 card is in play and the highest other card is negative, that card still counts 0 (for example, Max→0, -5 and -10 give -10).
  R12. When true_total < current_declaration, the current_declarer's tokens rise by 1.
  R13. When true_total >= current_declaration, the caller's tokens rise by 1 (the opener's on an automatic call).
  R14. When a hand ends, every card, true_total and the seat that took the token are announced to all players.
  R15. When a hand ends, opener_seat moves to the next seat clockwise, wrapping from seat N to seat 1.
  R16. When 12 hands have been played, the game ends.
  R17. When the game ends, the player with the fewest tokens wins, and players tied for the fewest share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Opening declaration | asked: the opener (seat opener_seat) | options: any whole number from -30 to 60
  - Raise or call | asked: each responder in clockwise order from the opener, while bidding is open | options: raise or call_coyote when current_declaration < 60; only call_coyote when current_declaration = 60
  - Raise amount | asked: a responder who chose raise | options: any whole number from current_declaration + 1 to 60

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number > 12
  - each player's standing: 0 - you.tokens (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player's standing is the negative of their Coyote tokens. The player with the fewest tokens wins, and players tied for the fewest share the result (the source calls this a draw).
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

- each player: `tokens` (number, visible: public, starts 0): Coyote tokens taken so far (fewer is better)
- the table: `hand_number` (number, visible: public, starts 1): The current hand, from 1 to 12
- the table: `opener_seat` (number, visible: public, starts 1): Seat that opens this hand
- the table: `current_declaration` (number, visible: public, starts 0): The highest declaration made so far this hand
- the table: `current_declarer` (number, visible: public, starts 0): Seat that made the current declaration
- the table: `caller` (number, visible: public, starts 0): Seat that called Coyote, or the opener on an automatic call
- the table: `true_total` (number, visible: public, starts 0): The true total of the cards in play, computed after bidding
- the table: `hand_loser` (number, visible: public, starts 0): Seat that took the token this hand
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 33, count_minus_10 = 1, count_minus_5 = 2, count_0 = 3, count_each_1_to_5 = 4, count_10 = 3, count_15 = 2, count_20 = 1, count_max_to_zero = 1, max_to_zero_code = 100, hands = 12, declaration_min = -30, declaration_max = 60, raise_min_step = 1, tokens_per_loss = 1, starting_tokens = 0, cards_per_player = 1
- the game ends with ONE ending whose `rank_by` is `0 - you.tokens`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Rework the response phase so each responder, in clockwise order from the opener, gets a choice between two options named exactly 'raise' and 'call_coyote'. When 'raise' is chosen, have that same seat pick a whole number strictly greater than current_declaration and at most declaration_max (60). Then set current_declaration to it and current_declarer to that seat. Bidding must continue to the next responder until someone calls. When someone calls, set caller to that seat and skip the remaining responders with a `when` condition on each later step. If every responder raised, set caller to opener_seat (the automatic call). Then compute true_total, including the Max→0 rule, and add tokens_per_loss to current_declarer if true_total < current_declaration, otherwise to caller. Set hand_loser accordingly. Check that the raise option is actually offered for every responder seat in 3- and 4-player games, not just to seat 2, and that its step's `when` condition is not wrongly false after a previous raise.


YOUR PREVIOUS GAME FILE WAS REFUSED. Here it is:
```json
{
  "schema": 1,
  "meta": {
    "id": "coyote_lap",
    "name": "Coyote Lap",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "See every card but your own, bid upward on the true total, call Coyote when it is too high; after 12 hands the fewest tokens wins."
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
        "key": "tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card",
        "visible": "others",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]
      },
      {
        "key": "full_deck",
        "visible": "none",
        "type": "list",
        "initial": [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "current_declaration",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_declarer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidding_open",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "caller",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "true_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_loser",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_cards",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "resp1",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "resp2",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "resp3",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "response",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "count_minus_10",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_minus_5",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_0",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_each_1_to_5",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "count_10",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_15",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_20",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_max_to_zero",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_to_zero_code",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "declaration_min",
        "visible": "public",
        "type": "number",
        "initial": -30
      },
      {
        "key": "declaration_max",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "raise_min_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tokens_per_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
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
            "key": "tokens",
            "value": {
              "calc": "starting_tokens"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": 1
          }
        }
      ],
      "text": "Players are seated clockwise in seat order. Everyone starts with {starting_tokens} Coyote tokens. Seat {opener_seat} opens hand {hand_number}."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": {
              "calc": "full_deck"
            }
          }
        },
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "card",
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
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "resp1",
            "value": {
              "calc": "opener_seat % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "resp2",
            "value": {
              "calc": "(opener_seat + 1) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "resp3",
            "value": {
              "calc": "(opener_seat + 2) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "caller",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_declarer",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_declaration",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_loser",
            "value": 0
          }
        },
        {
          "set": {
            "key": "true_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "bidding_open",
            "value": true
          }
        }
      ],
      "text": "Hand {hand_number} of {hands}: the full deck is shuffled and one card is dealt face down to each player. Seat {opener_seat} opens."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "the bandana",
      "mode": "others",
      "to": "all",
      "fields": [
        "card"
      ],
      "text": "This player's card (100 means the Max→0 card):"
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "opening declaration",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "declaration_min"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp1"
              },
              "if": {
                "calc": "current_declaration >= declaration_max"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp1} must call Coyote."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} opens at {value}."
      },
      "text": "You open hand {hand_number}. You can see everyone's card but your own. Declare a whole number from {declaration_min} to {declaration_max}: your claim about the true total of all cards in play this hand."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 1 raises or calls",
      "when": {
        "calc": "bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 1 raise amount",
      "when": {
        "calc": "bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp1"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp2"
              },
              "if": {
                "calc": "current_declaration >= declaration_max"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp2} must call Coyote."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number from {current_declaration} + {raise_min_step} up to {declaration_max}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 2 raises or calls",
      "when": {
        "calc": "bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 2 raise amount",
      "when": {
        "calc": "bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp2"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp3"
              },
              "if": {
                "calc": "current_declaration >= declaration_max and len(players) >= 4"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp3} must call Coyote."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max and len(players) >= 4"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number from {current_declaration} + {raise_min_step} up to {declaration_max}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 3 raises or calls",
      "when": {
        "calc": "len(players) >= 4 and bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp3"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 3 raise amount",
      "when": {
        "calc": "len(players) >= 4 and bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp3"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number from {current_declaration} + {raise_min_step} up to {declaration_max}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "automatic call",
      "when": {
        "calc": "bidding_open"
      },
      "do": [
        {
          "set": {
            "key": "caller",
            "value": {
              "calc": "opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "bidding_open",
            "value": false
          }
        }
      ],
      "text": "Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "true total",
      "do": [
        {
          "set": {
            "key": "true_total",
            "value": {
              "calc": "sum([p.card for p in players if p.card != max_to_zero_code]) - (max([p.card for p in players if p.card != max_to_zero_code]) if any(p.card == max_to_zero_code for p in players) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_cards",
            "value": {
              "calc": "[[p.seat, ('Max→0' if p.card == max_to_zero_code else p.card)] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the token",
      "do": [
        {
          "set": {
            "key": "hand_loser",
            "value": {
              "calc": "current_declarer if true_total < current_declaration else caller"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "hand_loser"
            },
            "key": "tokens",
            "value": {
              "calc": "tokens_per_loss"
            },
            "if": {
              "calc": "hand_loser > 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "Cards [seat, card]: {last_cards}. True total {true_total} against a declaration of {current_declaration} (declared by seat {current_declarer}, called by seat {caller}). Seat {hand_loser} takes a Coyote token."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "rotate",
      "do": [
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "opener_seat % len(players) + 1"
            }
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number > hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number > hands"
      },
      "rank_by": "0 - you.tokens",
      "text": "Winner: {result} (fewest Coyote tokens). Final tokens [seat, tokens]: {[[p.seat, p.tokens] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 13,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed clockwise order, seats 1 to N. Everyone starts with {starting_tokens} Coyote tokens. Seat 1 opens hand 1, and the game lasts exactly {hands} hands.\n\nThe deck has {deck_size} cards: {count_minus_10} of -10, {count_minus_5} of -5, {count_0} of 0, {count_each_1_to_5} each of 1, 2, 3, 4 and 5, {count_10} of 10, {count_15} of 15, {count_20} of 20, and {count_max_to_zero} special card 'Max→0' (shown as {max_to_zero_code} on a player's card).\n\nEach hand:\n1. Deal: the full deck is shuffled and {cards_per_player} card is dealt face down to each player.\n2. Bandana: each player is told privately the cards of all other players, but never their own card.\n3. Opening declaration: the opener declares a whole number from {declaration_min} to {declaration_max}, a claim about the TRUE TOTAL of all cards in play this hand. T
... (cut)

Why it was refused: it plays, but part of it does nothing: game attribute `full_deck` is never changed in 3 random matches, so nothing updates it. No step sets it. Either remove the attribute from the file, or add the update that sets it.. Every attribute must be changed by a step that actually runs. If the script in the task lists the attribute, do NOT delete it: write the step that really changes it (for cards, follow the deck recipe). Delete it only if the script does not list it.
Correct it: change what the problem requires and keep the rest. Reply in the same format as before, complete, and nothing else.
````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "coyote_lap",
    "name": "Coyote Lap",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "See every card but your own, bid upward on the true total, call Coyote when it is too high; after 12 hands the fewest tokens wins."
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
        "key": "tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "card",
        "visible": "others",
        "type": "number",
        "initial": 0
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": [-10, -5, -5, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 10, 10, 10, 15, 15, 20, 100]
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_number",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "opener_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "current_declaration",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "current_declarer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "bidding_open",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "caller",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "true_total",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "hand_loser",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_cards",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "resp1",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "resp2",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "resp3",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "response",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "count_minus_10",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_minus_5",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_0",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_each_1_to_5",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "count_10",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "count_15",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "count_20",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "count_max_to_zero",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "max_to_zero_code",
        "visible": "public",
        "type": "number",
        "initial": 100
      },
      {
        "key": "hands",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "declaration_min",
        "visible": "public",
        "type": "number",
        "initial": -30
      },
      {
        "key": "declaration_max",
        "visible": "public",
        "type": "number",
        "initial": 60
      },
      {
        "key": "raise_min_step",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "tokens_per_loss",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "starting_tokens",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cards_per_player",
        "visible": "public",
        "type": "number",
        "initial": 1
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
            "key": "tokens",
            "value": {
              "calc": "starting_tokens"
            }
          }
        },
        {
          "set": {
            "key": "hand_number",
            "value": 1
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": 1
          }
        }
      ],
      "text": "Players are seated clockwise in seat order. Everyone starts with {starting_tokens} Coyote tokens. Seat {opener_seat} opens hand {hand_number}."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "deal",
      "label": "the deal",
      "do": [
        {
          "set": {
            "key": "pick",
            "value": {
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 1,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 2,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            }
          }
        },
        {
          "set": {
            "player": 3,
            "key": "card",
            "value": {
              "calc": "pick"
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
              "calc": "deck[int(uniform(0, len(deck)))]"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "player": 4,
            "key": "card",
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
            "key": "deck",
            "value": {
              "calc": "pick"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "resp1",
            "value": {
              "calc": "opener_seat % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "resp2",
            "value": {
              "calc": "(opener_seat + 1) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "resp3",
            "value": {
              "calc": "(opener_seat + 2) % len(players) + 1"
            }
          }
        },
        {
          "set": {
            "key": "caller",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_declarer",
            "value": 0
          }
        },
        {
          "set": {
            "key": "current_declaration",
            "value": 0
          }
        },
        {
          "set": {
            "key": "hand_loser",
            "value": 0
          }
        },
        {
          "set": {
            "key": "true_total",
            "value": 0
          }
        },
        {
          "set": {
            "key": "response",
            "value": ""
          }
        },
        {
          "set": {
            "key": "bidding_open",
            "value": true
          }
        }
      ],
      "text": "Hand {hand_number} of {hands}: the full deck is shuffled and one card is dealt face down to each player. Seat {opener_seat} opens."
    },
    {
      "use": "sync",
      "phase": "deal",
      "label": "the bandana",
      "mode": "others",
      "to": "all",
      "fields": [
        "card"
      ],
      "text": "This player's card (100 means the Max→0 card):"
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "opening declaration",
      "to": {
        "where": "you.seat == opener_seat"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "declaration_min"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp1"
              },
              "if": {
                "calc": "current_declaration >= declaration_max"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp1} can only call Coyote, and does."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} opens at {value}."
      },
      "text": "You open hand {hand_number}. You can see everyone's card but your own. Declare a whole number from {declaration_min} to {declaration_max}: your claim about the true total of all cards in play this hand."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 1 raises or calls",
      "when": {
        "calc": "bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp1"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 1 raise amount",
      "when": {
        "calc": "bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp1"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp2"
              },
              "if": {
                "calc": "current_declaration >= declaration_max"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp2} can only call Coyote, and does."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number greater than {current_declaration} and at most {declaration_max}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 2 raises or calls",
      "when": {
        "calc": "bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 2 raise amount",
      "when": {
        "calc": "bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp2"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          },
          {
            "set": {
              "key": "caller",
              "value": {
                "calc": "resp3"
              },
              "if": {
                "calc": "current_declaration >= declaration_max and len(players) >= 4"
              },
              "text": "The declaration is at the maximum {declaration_max}, so seat {resp3} can only call Coyote, and does."
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "current_declaration >= declaration_max and len(players) >= 4"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number greater than {current_declaration} and at most {declaration_max}."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 3 raises or calls",
      "when": {
        "calc": "len(players) >= 4 and bidding_open and current_declaration < declaration_max"
      },
      "to": {
        "where": "you.seat == resp3"
      },
      "answer": {
        "type": "choice",
        "options": [
          "raise",
          "call_coyote"
        ]
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "response",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "caller",
              "value": "$seat",
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          },
          {
            "set": {
              "key": "bidding_open",
              "value": false,
              "if": {
                "calc": "$answer == 'call_coyote'"
              }
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} chooses {value} on the declaration of {current_declaration}."
      },
      "text": "The current declaration is {current_declaration} by seat {current_declarer}. Choose raise (declare a higher number, at most {declaration_max}) or call_coyote (challenge it; bidding stops)."
    },
    {
      "use": "ask",
      "phase": "bidding",
      "label": "responder 3 raise amount",
      "when": {
        "calc": "len(players) >= 4 and bidding_open and response == 'raise'"
      },
      "to": {
        "where": "you.seat == resp3"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "current_declaration + raise_min_step"
        },
        "max": {
          "calc": "declaration_max"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "current_declaration",
              "value": "$answer"
            }
          },
          {
            "set": {
              "key": "current_declarer",
              "value": "$seat"
            }
          },
          {
            "set": {
              "key": "response",
              "value": ""
            }
          }
        ]
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} raises to {value}."
      },
      "text": "Declare a whole number greater than {current_declaration} and at most {declaration_max}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "automatic call",
      "when": {
        "calc": "bidding_open"
      },
      "do": [
        {
          "set": {
            "key": "caller",
            "value": {
              "calc": "opener_seat"
            }
          }
        },
        {
          "set": {
            "key": "bidding_open",
            "value": false
          }
        }
      ],
      "text": "Everyone raised; Seat {opener_seat} calls Coyote automatically on {current_declaration}."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "true total",
      "do": [
        {
          "set": {
            "key": "true_total",
            "value": {
              "calc": "sum([p.card for p in players if p.card != max_to_zero_code]) - (max([p.card for p in players if p.card != max_to_zero_code]) if any(p.card == max_to_zero_code for p in players) else 0)"
            }
          }
        },
        {
          "set": {
            "key": "last_cards",
            "value": {
              "calc": "[[p.seat, ('Max→0' if p.card == max_to_zero_code else p.card)] for p in players]"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "the token",
      "do": [
        {
          "set": {
            "key": "hand_loser",
            "value": {
              "calc": "current_declarer if true_total < current_declaration else caller"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "hand_loser"
            },
            "key": "tokens",
            "value": {
              "calc": "tokens_per_loss"
            },
            "if": {
              "calc": "hand_loser > 0"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the reveal",
      "to": "all",
      "text": "Cards [seat, card]: {last_cards}. True total {true_total} against a declaration of {current_declaration} (declared by seat {current_declarer}, called by seat {caller}). Seat {hand_loser} takes a Coyote token."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "collect the cards and rotate",
      "do": [
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "players[0].card"
            }
          }
        },
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "players[1].card"
            }
          }
        },
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "players[2].card"
            }
          }
        },
        {
          "append": {
            "key": "deck",
            "value": {
              "calc": "players[3].card"
            },
            "if": {
              "calc": "len(players) >= 4"
            }
          }
        },
        {
          "set": {
            "key": "opener_seat",
            "value": {
              "calc": "opener_seat % len(players) + 1"
            }
          }
        },
        {
          "adjust": {
            "key": "hand_number",
            "value": 1
          }
        }
      ]
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "after the last hand",
      "when": {
        "calc": "hand_number > hands"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "hand_number > hands"
      },
      "rank_by": "0 - you.tokens",
      "text": "Winner: {result} (fewest Coyote tokens). Final tokens [seat, tokens]: {[[p.seat, p.tokens] for p in players]}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 13,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "Players sit in a fixed clockwise order, seats 1 to N. Everyone starts with {starting_tokens} Coyote tokens. Seat 1 opens hand 1, and the game lasts exactly {hands} hands.\n\nThe deck has {deck_size} cards: {count_minus_10} of -10, {count_minus_5} of -5, {count_0} of 0, {count_each_1_to_5} each of 1, 2, 3, 4 and 5, {count_10} of 10, {count_15} of 15, {count_20} of 20, and {count_max_to_zero} special card 'Max→0' (shown as {max_to_zero_code} on a player's card).\n\nEach hand:\n1. Deal: the full deck is shuffled and {cards_per_player} card is dealt face down to each player.\n2. Bandana: each player is told privately the cards of all other players, but never their own card.\n3. Opening declaration: the opener declares a whole number from {declaration_min} to {declaration_max}, a claim about the TRUE TOTAL of all cards in play this hand. The opener becomes the current declarer.\n4. Responses: each other player, one at a time in clockwise order from the opener, chooses one of two options: (a) raise: declare a whole number strictly higher than the current declaration, at most {declaration_max}; it becomes the current declaration and this player becomes the current declarer, and bidding passes to the next responder. (b) call_coyote: challenge the current declaration; bidding stops immediately and later players do not act this hand. Every declaration is announced to all players as it is made. When the current declaration is already {declaration_max}, raising is impossible, so the next responder can only call Coyote.\n5. Automatic call: if every responder raised, the opener is treated as having called Coyote on the final declaration.\n6. True total: add up the numbers on all cards in play. If the 'Max→0' card is in play, it counts as 0 itself, and the highest-valued other card in play also counts as 0. If several cards tie for highest, only one of them counts as 0. If the highest other card is negative, it still becomes 0.\n7. Resolution: if the true total is LESS than the current declaration, the current declarer takes {tokens_per_loss} Coyote token (the call was right). Otherwise (the true total is equal to or greater than the declaration) the caller, or the opener in the case of an automatic call, takes {tokens_per_loss} Coyote token (the call was wrong).\n8. Reveal: all cards, the true total and the token taken are announced to everyone.\n9. Rotate: the next player clockwise opens the next hand.\n\nAfter hand {hands}, the game ends. The player with the fewest Coyote tokens wins; players tied for the fewest share the result."
}
```
````
