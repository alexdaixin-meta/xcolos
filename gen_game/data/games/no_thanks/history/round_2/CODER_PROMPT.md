# Task: write the XColos game file for "No Thanks! (Bounded Laps)"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. (R1) Take the 33 cards numbered 3 to 35. Remove 13 of them at random, unseen by anyone; they stay hidden all game. The other 20 cards, shuffled, form the deck. (R2) Each player starts with 11 chips, an empty tableau and 0 card points. A player's chip count is visible only to that player. Tableaus, the current card, the pot and the number of burned cards are public. (R3) Game state: current_card = 0 (meaning no card), pot = 0, lap_count = 0, lead_seat = 1, an empty burned list, pay_cost = 1, laps_to_burn = 2. Seats are numbered 1 to N clockwise.

EACH ROUND, in this exact order:

Step 1, DRAW (R4). Only if current_card = 0 and the deck is not empty: draw the top deck card at random, make it current_card, and set lap_count = 0. The pot is NOT changed, so it may hold chips left over from a burned card. If current_card is not 0, skip this step: the same card and pot continue.

Step 2, ANNOUNCE. Show everyone the current card, the pot, every tableau, the number of cards left in the deck and the number of burned cards.

Steps 3 to 6, OFFERS (R5). Offer k (k = 1 to N) goes to the seat k-1 places clockwise from lead_seat. Make an offer only while current_card is not 0. The options are TAKE (always offered) and PAY (offered only if that seat has at least pay_cost = 1 chip).
- PAY: the seat moves 1 chip from its hand into the pot.
- TAKE: the seat adds the current card c to its tableau. Its card points change by c, minus (c+1) if c+1 was already in its tableau, minus c if c-1 was already in its tableau. It gains all chips in the pot, and the pot becomes 0. Then current_card becomes 0 and lead_seat becomes the taker's seat. No further offers are made this round.

Step 7, END OF LAP (R11). Only if current_card is still not 0 (everyone paid): add 1 to lap_count.
- If lap_count is now less than laps_to_burn (that is, lap_count = 1): change nothing else. The same card and pot stay current, lead_seat stays the same, and next round's offers start again at lead_seat with TAKE offered to every seat.
- If lap_count = laps_to_burn = 2: put the card into the burned list (it scores for no one), set current_card = 0, keep the pot as it is, and move lead_seat one seat clockwise.

Step 8, ANNOUNCE RESULT. Tell everyone who paid and who took (or that the card was burned). Players' own chip counts are shown only to themselves.

Step 9, END CHECK. If the deck is empty and current_card = 0, the game ends. Otherwise start the next round. The game cannot last more than 40 rounds.

SCORING. Each player's final score = card points minus chips in hand. Card points equal the sum of the lowest card of each run of consecutive numbers in the tableau. Any chips left in the pot at the end belong to no one.

How the winner is decided: Each player's final score is card points minus remaining chips. The single player with the lowest final score wins. If two or more players tie for lowest, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: No Thanks! (Bounded Laps) (3 to 4 players, best with 4)

Players pay one chip to refuse a card or take it with the pot. Each card may circle the table at most twice before it is burned. The lowest score, card points minus chips, wins.

STATE (every item below must exist in the file):
  - each player: chips (number, starts 11); only its owner sees it. Chips in hand. Only the owner sees this. Each chip lowers the final score by 1.
  - each player: tableau (list, starts []); everyone sees it. Card numbers this player has taken.
  - each player: card_points (number, starts 0); everyone sees it. Sum of the lowest card of each run of consecutive numbers in the tableau, kept up to date on every take.
  - the table: deck (list, starts '20 cards chosen at random from 3..35'); hidden from all players. Undrawn cards. Hidden order; only the count is announced.
  - the table: removed (list, starts 'the other 13 cards of 3..35'); hidden from all players. Cards removed unseen at setup. They stay hidden all game.
  - the table: current_card (number, starts 0); everyone sees it. The card on offer; 0 means there is no card.
  - the table: pot (number, starts 0); everyone sees it. Chips paid onto the current card. They carry over after a burn.
  - the table: lap_count (number, starts 0); everyone sees it. Full laps in which every seat paid on the current card.
  - the table: lead_seat (number, starts 1); everyone sees it. The seat that receives the first offer of the round.
  - the table: burned (list, starts []); everyone sees it. Cards burned after 2 full laps. They score for no one; their count is announced.
  - the table: round_number (number, starts 0); everyone sees it. Rounds played, used for the 40-round bound.
  - parameters, each kept as a table attribute: card_min = 3, card_max = 35, card_total = 33, cards_removed = 13, deck_size = 20, starting_chips = 11, pay_cost = 1, laps_to_burn = 2, max_rounds = 40, initial_lead_seat = 1, no_card_value = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Make the 33 cards numbered 3 to 35.
  2. Move 13 of them at random into the hidden table list `removed`; nobody ever sees them.
  3. The remaining 20 cards form the hidden table list `deck`.
  4. Each player gets chips = 11, an empty tableau and card_points = 0.
  5. Set current_card = 0, pot = 0, lap_count = 0, lead_seat = 1, burned = [] and round_number = 0.
  6. Seats are numbered 1 to N clockwise.
  7. Sync each player their own state, including their private chip count.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_number += 1. When current_card = 0 and deck is not empty: draw one card at random from deck (remove it from deck), set current_card to it and set lap_count = 0. The pot is unchanged.
  2. [tell] all players. What happens: Announce current_card, pot, every player's tableau and card_points, the length of deck and the length of burned.
  3. [ask] seat lead_seat (offer 1) answers: TAKE, or PAY if that seat has chips >= 1. What happens: When current_card != 0. PAY: chips -= 1 and pot += 1. TAKE: append current_card to tableau; card_points += c, minus (c+1) if c+1 is in the tableau, minus c if c-1 is in the tableau; chips += pot; pot = 0; lead_seat = this seat; current_card = 0.
  4. [ask] seat 1 place clockwise from lead_seat (offer 2) answers: TAKE, or PAY if chips >= 1. What happens: Same as offer 1. Runs only when current_card != 0.
  5. [ask] seat 2 places clockwise from lead_seat (offer 3) answers: TAKE, or PAY if chips >= 1. What happens: Same as offer 1. Runs only when current_card != 0.
  6. [ask] seat 3 places clockwise from lead_seat (offer 4) answers: TAKE, or PAY if chips >= 1. What happens: Same as offer 1. Runs only when current_card != 0 and N >= 4.
  7. [update] all players. What happens: End of lap, when current_card != 0: lap_count += 1. If lap_count = 2: append current_card to burned, set current_card = 0, keep pot, and set lead_seat = (lead_seat mod N) + 1. If lap_count = 1, nothing else changes.
  8. [tell] all players. What happens: Announce who paid and who took, or that the card was burned. Then sync each player their own chips privately.
  9. [check] all players. What happens: End the game if deck is empty and current_card = 0, or if round_number >= 40. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game is set up, the deck holds 20 distinct cards from 3..35 and the other 13 sit in the hidden removed list.
  R2. When the game starts, each player has chips = 11, an empty tableau and card_points = 0; chips are visible only to their owner.
  R3. When the game starts, current_card = 0, pot = 0, lap_count = 0, lead_seat = 1 and burned is empty.
  R4. When a round starts with current_card = 0 and a non-empty deck, then one card moves from deck to current_card, lap_count becomes 0 and the pot is unchanged.
  R4b. When a round starts with current_card != 0, then no card is drawn and the same card and pot continue.
  R5. When an offer is made, then the seat is offered TAKE, and also PAY only if its chips >= 1.
  R6. When a seat PAYs, then its chips fall by 1 and the pot rises by 1.
  R7. When a seat TAKEs card c, then c is appended to its tableau and card_points changes by c, minus (c+1) if c+1 was already held, minus c if c-1 was already held.
  R8. When a seat TAKEs, then its chips rise by the pot, the pot becomes 0, current_card becomes 0, lead_seat becomes that seat, and no further offers are made that round.
  R9. When offer k is made, then it goes to the seat k-1 places clockwise from lead_seat, for k = 1..N, and only while current_card != 0.
  R10. When a seat with 0 chips is offered the card, then its only option is TAKE.
  R11. When all N seats pay in a round and lap_count becomes 1, then the card, pot and lead_seat stay the same for the next round.
  R12. When all N seats pay and lap_count becomes 2, then the card is appended to burned, current_card becomes 0, the pot is kept and lead_seat moves one seat clockwise.
  R13. When the deck is empty and current_card = 0 at the end check, then the game ends.
  R14. When 40 rounds have been played, then the game ends.
  R15. When the game ends, then each final score is card_points minus chips, and chips left in the pot belong to no one.
  R16. When the game ends, then the player with the lowest final score wins, and players tied for lowest share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Offer on the current card (offers 1 to N) | asked: the seat k-1 places clockwise from lead_seat, while current_card != 0 | options: a seat with chips >= 1: TAKE, PAY; a seat with chips = 0: TAKE

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: (len(deck) == 0 and current_card == 0) or round_number >= 40
  - each player's standing: you.chips - you.card_points (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player's final score is card_points minus chips, and lower is better, so each player is ranked by chips minus card_points. The highest value (the lowest final score) wins. Players level at the top share the win, which stands in for the source's draw.
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

- each player: `chips` (number, visible: ally, starts 11): Chips in hand. Only the owner sees this. Each chip lowers the final score by 1.
- each player: `tableau` (list, visible: public, starts []): Card numbers this player has taken.
- each player: `card_points` (number, visible: public, starts 0): Sum of the lowest card of each run of consecutive numbers in the tableau, kept up to date on every take.
- the table: `current_card` (number, visible: public, starts 0): The card on offer; 0 means there is no card.
- the table: `pot` (number, visible: public, starts 0): Chips paid onto the current card. They carry over after a burn.
- the table: `burned` (list, visible: public, starts []): Cards burned after 2 full laps. They score for no one; their count is announced.
- parameters (each must be an attribute holding this value, never a number buried in a step): card_min = 3, card_max = 35, card_total = 33, cards_removed = 13, deck_size = 20, starting_chips = 11, pay_cost = 1, laps_to_burn = 2, max_rounds = 40, initial_lead_seat = 1, no_card_value = 0
- the game ends with ONE ending whose `rank_by` is `you.chips - you.card_points`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Rework the offer steps (R5/R9/R10).
1. Each offer k (k = 1..N) must go to the seat k-1 places clockwise from lead_seat, computed with modular arithmetic from a table attribute such as lead_seat.
2. Each offer step's `when` should be only `current_card != no_card_value`. Do not add conditions on lap_count, chips or other scratch values that could suppress the whole offer.
3. Inside the offer, the option must be named exactly `TAKE` and always be present.
4. `PAY` is the only conditional option, available only when that seat's chips >= pay_cost.
5. A 0-chip seat must still get the offer, with TAKE as its only option. Do not skip the step when only one option remains.
6. TAKE must:
   - append current_card to the taker's tableau and update card_points (+c, minus (c+1) if c+1 is already in the tableau, minus c if c-1 is);
   - add pot to the taker's chips, then set pot to 0;
   - set current_card to no_card_value and lead_seat to the taker's seat.
   After that, later offers that round are skipped because current_card is now 0.
7. Make sure the offers also work when a scenario supplies current_card, lead_seat and pot directly in the given state, rather than only after a draw: use those attributes rather than values cached at draw time.
