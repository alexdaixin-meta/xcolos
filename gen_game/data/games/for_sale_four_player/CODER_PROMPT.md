# Task: write the XColos game file for "For Sale: Sealed Bids - Four Player"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 4 to 4; set `meta.players` to {"min": 4, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. 4 players numbered 1, 2, 3, 4. Each starts with 18 coins (private) and 0 cheques (private cheque total) and empty property hand (public). Property deck: cards 1 to 30, one each. Cheque deck: values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15, two of each, 30 cheques. Game lasts 14 rounds: rounds 1-7 BUYING, rounds 8-14 SELLING. No talk phase: every choice is sealed to preserve bluff; promises are unenforceable and following a rival's suggestion to bid low leaves you with LOW. BUYING ROUND (rounds 1-7): 1. In round 1 only, shuffle the property deck. Only the top 28 cards will ever be used; the bottom 2 stay unseen. 2. Reveal the next 4 cards from the property deck. Sort them and call them HIGH, SECOND, THIRD, LOW by value. 3. All players at the same moment secretly submit a bid: whole number 0 up to current coins. 4. Rank bids highest to lowest. Break ties by priority order: in round r priority goes first to player ((r-1) mod 4)+1, then next number wrapping 4 to 1. 5. First-ranked takes HIGH and pays full bid. Second-ranked takes SECOND and pays half bid rounded UP. Third-ranked takes THIRD and pays half bid rounded UP. Fourth-ranked takes LOW and pays half bid rounded UP. Example: bid 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2. 6. Payments go to the bank from private coins. 7. Announce publicly which player took HIGH, SECOND, THIRD, LOW. Bid amounts and coin totals are NOT announced. After round 7 each holds 7 properties. SELLING ROUND (rounds 8-14): 1. In round 8 only, shuffle the cheque deck. Only the top 28 cheques will ever be used; bottom 2 unseen. 2. Reveal the next 4 cheques from the cheque deck, sorted highest to lowest. 3. All players at the same moment secretly choose one property from own hand. 4. Reveal chosen properties. All properties are different so no ties. 5. Highest property adds highest cheque to cheque total; second-highest adds second-highest cheque; third adds third; lowest adds lowest. 6. Played properties are discarded. 7. Announce publicly who played which property and who took which cheque. Running cheque totals stay private. END. After round 14 hands are empty. Reveal cheque totals, remaining coins, and final money = cheque total + remaining coins.

How the winner is decided: Player with most final money (cheques plus remaining coins) wins. If tied for most, tied player with more remaining coins wins. If still tied, game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: For Sale: Sealed Bids - Four Player (4 to 4 players, best with 4)

Bid secretly for properties then sell them secretly for cheques; richest total wins.

STATE (every item below must exist in the file):
  - each player: coins (number, starts 18); only its owner sees it. remaining private coins for bidding
  - each player: cheque_total (number, starts 0); only its owner sees it. sum of cheques won kept private until end
  - each player: properties (list, starts []); everyone sees it. property cards held in hand public
  - each player: bid (number, starts 0); only its owner sees it. sealed bid submitted this buying round
  - each player: selected_property (number, starts 0); only its owner sees it. property chosen to sell this selling round
  - each player: final_money (number, starts 0); everyone sees it. cheque_total plus remaining coins revealed at end
  - the table: property_deck (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]); hidden from all players. unseen property cards 1 to 30
  - the table: cheque_deck (list, starts [0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]); hidden from all players. unseen cheques 0 and 2 to 15 two each
  - the table: current_offer (list, starts []); everyone sees it. 4 properties or cheques revealed this round sorted high to low
  - the table: round_number (number, starts 1); everyone sees it. current round 1 to 14
  - the table: priority_seat (number, starts 1); everyone sees it. first seat in tie break order this round
  - the table: property_discard (list, starts []); everyone sees it. played properties discarded
  - parameters, each kept as a table attribute: starting_coins = 18, property_low = 1, property_high = 30, property_deck_size = 30, property_deck_used = 28, cheque_low = 0, cheque_high = 15, cheque_copies = 2, cheque_deck_size = 30, cheque_deck_used = 28, total_rounds = 14, buying_rounds = 7, selling_rounds = 7, cards_per_round = 4

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Give each of seats 1 to 4 exactly 18 coins, 0 cheque_total, 0 final_money and empty properties hand.
  2. Build property_deck as cards 1 to 30 one each and cheque_deck as 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two each for 30 cheques.
  3. Set round_number to 1 and current_offer to empty and property_discard to empty.
  4. Only the top 28 properties and top 28 cheques will ever be used and the bottom 2 of each deck stay unseen.
  5. There is no talk phase and all choices are sealed.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [initialize] all players. What happens: set coins to 18 cheque_total to 0 properties to [] bid to 0 selected_property to 0 final_money to 0 property_deck to 1 to 30 cheque_deck to 0,0,2,2 to 15,15 round_number to 1 current_offer to []
  2. [sync] all players. What happens: send each player their coins cheque_total and properties
  3. [update] all players. What happens: when round_number is 1 remove 2 unseen cards from property_deck then move next 4 cards from property_deck to current_offer sorted HIGH SECOND THIRD LOW and set priority_seat to ((round_number-1) mod 4)+1
  4. [poll] all players answers: {'type': 'number', 'min': 0, 'max': 'coins'}. What happens: set you.bid to sealed bid 0 up to you.coins
  5. [update] all players. What happens: rank bids high to low breaking ties by priority_seat order wrapping 4 to 1 then first-ranked takes HIGH and pays full bid from coins second takes SECOND and pays (bid+1)//2 third takes THIRD and pays (bid+1)//2 fourth takes LOW and pays (bid+1)//2 and append taken property to you.properties
  6. [tell] all players. What happens: broadcast which player took HIGH SECOND THIRD LOW without revealing bid amounts or coin totals
  7. [update] all players. What happens: when round_number is 8 remove 2 unseen cheques from cheque_deck then move next 4 cheques from cheque_deck to current_offer sorted highest to lowest
  8. [poll] all players answers: {'type': 'choice', 'from': 'you.properties'}. What happens: set you.selected_property to one property from you.properties
  9. [update] all players. What happens: rank selected_property high to low with no ties then highest adds highest cheque in current_offer to cheque_total second-highest adds second-highest third adds third lowest adds lowest and remove selected_property from you.properties to property_discard
  10. [tell] all players. What happens: broadcast who played which property and who took which cheque without revealing running cheque totals
  11. [update] all players. What happens: set round_number to round_number+1 and if round_number>14 set you.final_money to you.cheque_total+you.coins
  12. [check] all players. What happens: end the game when round_number>14 else continue

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then each of 4 players holds 18 coins, 0 cheque_total and empty properties hand.
  R2. When built, then property_deck holds cards 1 to 30 one each for 30 cards.
  R3. When built, then cheque_deck holds values 0,2,3,4,5,6,7,8,9,10,11,12,13,14,15 two of each for 30 cheques.
  R4. When the game runs, then rounds 1 to 7 are buying and rounds 8 to 14 are selling for 14 rounds total.
  R5. When decks are prepared, then only the top 28 properties and top 28 cheques are ever used and the bottom 2 stay unseen.
  R6. When a buying round starts, then reveal the next 4 property cards sorted HIGH SECOND THIRD LOW by value.
  R7. When bidding, then all players at the same moment secretly submit a whole-number bid from 0 up to current coins.
  R8. When bids are ranked, then rank highest to lowest and break ties by priority order starting at seat ((r-1) mod 4)+1 then next wrapping 4 to 1 in round r.
  R9. When buying resolves, then first-ranked takes HIGH and pays full bid and second-ranked takes SECOND and pays half rounded up and third takes THIRD and pays half rounded up and fourth takes LOW and pays half rounded up where 0 pays 0, 1 pays 1, 2 pays 1, 3 pays 2, 4 pays 2.
  R10. When payments are made, then they go to the bank from private coins.
  R11. When a buying round ends, then announce publicly which player took HIGH SECOND THIRD LOW and do not announce bid amounts or coin totals.
  R12. When round 7 ends, then each player holds 7 properties.
  R13. When a selling round starts, then reveal the next 4 cheques sorted highest to lowest.
  R14. When selling, then all players at the same moment secretly choose one property from own hand.
  R15. When chosen properties are revealed, then all properties are different so there are no ties.
  R16. When cheques are awarded, then highest property adds highest cheque to cheque total and second-highest adds second-highest and third adds third and lowest adds lowest.
  R17. When cheques are awarded, then played properties are discarded.
  R18. When a selling round ends, then announce publicly who played which property and who took which cheque and keep running cheque totals private.
  R19. When round 14 ends, then hands are empty and cheque totals, remaining coins and final money equal to cheque total plus remaining coins are revealed.
  R20. When the game ends, then the player with most final money wins.
  R21. When players tie for most final money, then the tied player with more remaining coins wins and if still tied the game is a draw among them.
  R22. When choices are made, then there is no talk phase and every choice is sealed.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - sealed bid | asked: all players | options: in buying rounds 1 to 7: any whole number 0 up to your current coins
  - choose property to sell | asked: all players | options: in selling rounds 8 to 14: any one property from your own properties hand (7 options in round 8 down to 1 option in round 14)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_number > 14
  - each player's standing: you.final_money * 1000 + you.coins (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Standing is final_money equal to cheque_total plus remaining coins with remaining coins as tie-break; highest value wins and players level at the top share the win
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

- each player: `properties` (list, visible: public, starts []): property cards held in hand public
- each player: `final_money` (number, visible: public, starts 0): cheque_total plus remaining coins revealed at end
- the table: `current_offer` (list, visible: public, starts []): 4 properties or cheques revealed this round sorted high to low
- parameters (each must be an attribute holding this value, never a number buried in a step): starting_coins = 18, property_low = 1, property_high = 30, property_deck_size = 30, property_deck_used = 28, cheque_low = 0, cheque_high = 15, cheque_copies = 2, cheque_deck_size = 30, cheque_deck_used = 28, total_rounds = 14, buying_rounds = 7, selling_rounds = 7, cards_per_round = 4
- the game ends with ONE ending whose `rank_by` is `you.final_money * 1000 + you.coins`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
