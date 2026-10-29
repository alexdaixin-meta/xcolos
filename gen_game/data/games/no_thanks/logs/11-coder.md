# 11 coder

- time: 2026-10-27T16:49:56+00:00 (112.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 592e6d043324bde0, reply sha256 0b9b68909b8585d9

## Sent

````
# Task: write the XColos game file for "No Thanks! Two Laps"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP:
- Take cards numbered 3 to 35 (33 cards), shuffle them, and remove 13 face-down without anyone seeing them. The removed cards are out of the game. The remaining 20 cards form the deck.
- Players are numbered 1 to N clockwise (N = 3 or 4).
- Each player receives 11 chips. A player's chip count is private: only that player is told it.
- Every action (pay, take, chips gained, burn) is announced publicly.
- Each player has a face-up tableau, which starts empty, and a card-points total, which starts at 0.
- The game keeps three public values: the current card (none at start), the pot (0 at start) and the lap count of the current card (0).
- The lead player for the first card is player 1.

EACH ROUND:
1. If there is no current card, reveal the top deck card. It becomes the current card, its lap count is set to 0, and the pot is unchanged: it may hold chips carried over from a burned card.
2. The current card is offered once around the table. Offers start with the lead player and go clockwise, and stop when someone takes it or every player has been offered it once this round.
3. When offered the card, a player chooses PAY or TAKE. A player with 0 chips must choose TAKE.
   - PAY: the player puts 1 chip from their hand into the pot, and the card is offered to the next player.
   - TAKE: the player adds all chips in the pot to their hand, places the card in their tableau, and the pot becomes 0. The card is no longer current. The taker becomes the lead player for the next card, and the round ends at once.
4. Card-point update when a player takes card c: their card-points total changes by (c if they do not hold c-1, else 0) minus (c+1 if they hold c+1, else 0). Card points therefore always equal the sum of the lowest card of each run of consecutive numbers in the tableau.
5. If every player chose PAY this round, the card's lap count increases by 1.
   - If the lap count is now 1, the card stays current with its pot, and the next round offers it again starting from the same lead player.
   - If the lap count is now 2, the card is burned (removed from the game). The pot stays in the middle for the next card, and the lead player for the next card becomes the player clockwise of the current lead player.
6. Announce what happened: who paid, who took what with how many chips, or that the card was burned, plus the pot size and every tableau.
7. If the deck is empty and there is no current card, the game ends. Any chips left in the pot are out of the game.

There is no discussion phase.

END: Each player's final score is card points minus chips in hand.

How the winner is decided: The player with the lowest final score (card points minus remaining chips) wins. If several players tie for lowest, the one among them with more remaining chips wins. If they are still tied, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: No Thanks! Two Laps (3 to 4 players, best with 4)

Players pay a chip to refuse each card or take it with the pot. A card refused for two full laps is burned and its pot carries over. The lowest score of card points minus chips wins.

STATE (every item below must exist in the file):
  - each player: chips (number, starts 11); only its owner sees it. Chips in this player's hand. Only the owner is told the count.
  - each player: tableau (list, starts []); everyone sees it. The face-up cards this player has taken.
  - each player: card_points (number, starts 0); everyone sees it. The sum of the lowest card of each run of consecutive numbers in the tableau.
  - each player: final_score (number, starts 0); everyone sees it. card_points minus chips, set when the game ends.
  - the table: deck (list, starts 'the 20 cards left after the shuffle and removal'); hidden from all players. The face-down draw deck.
  - the table: removed (list, starts 'the 13 cards removed at setup'); hidden from all players. Cards removed unseen at setup. They are out of the game.
  - the table: burned (list, starts []); everyone sees it. Cards burned after two laps with no taker.
  - the table: current_card (number, starts 0); everyone sees it. The card on offer. 0 means there is no current card.
  - the table: pot (number, starts 0); everyone sees it. Chips in the middle.
  - the table: lap_count (number, starts 0); everyone sees it. Full laps in which every player paid on the current card.
  - the table: lead_seat (number, starts 1); everyone sees it. The seat that is offered the current card first.
  - the table: taken (bool, starts False); everyone sees it. Whether the current card was taken this round.
  - parameters, each kept as a table attribute: card_min = 3, card_max = 35, total_cards = 33, removed_cards = 13, deck_size = 20, starting_chips = 11, pay_cost = 1, laps_to_stay = 1, laps_to_burn = 2, first_lead_seat = 1, rank_score_multiplier = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Make a list of the cards 3 to 35 (33 cards) and shuffle it.
  2. Move 13 cards at random, unseen, into the hidden table list removed. They are out of the game.
  3. The remaining 20 cards form the hidden table list deck.
  4. Each player gets chips = 11, which is private to that player, an empty public tableau, card_points = 0 and final_score = 0.
  5. Set current_card = 0, pot = 0, lap_count = 0 and lead_seat = 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] table. What happens: Set taken = false. If current_card == 0 and deck is not empty: draw one card at random from deck, remove it from deck, set current_card to it and set lap_count = 0. pot is unchanged. Announce the current card and the pot.
  2. [ask] each player in turn, clockwise, starting at lead_seat, each seat once; a seat is skipped once taken == true answers: one of PAY, TAKE (only TAKE when the player's chips == 0). What happens: PAY: chips -= 1, pot += 1, announced publicly. TAKE: card_points += (current_card if (current_card-1) is not in tableau, else 0) - (current_card+1 if (current_card+1) is in tableau, else 0); append current_card to tableau; chips += pot; pot = 0; current_card = 0; lap_count = 0; lead_seat = this seat; taken = true. Announce the take and the number of chips gained.
  3. [update] table. What happens: When taken == false: lap_count += 1. Then, if lap_count == 2: append current_card to burned, set current_card = 0, set lap_count = 0, and set lead_seat = (lead_seat mod N) + 1. pot stays as it is. If lap_count == 1, the card stays current with its pot and lead_seat is unchanged.
  4. [tell] all players. What happens: Announce who paid, who took which card with how many chips (or that the card was burned), the pot, every tableau and every card_points.
  5. [sync] all players. What happens: Each player is sent their own state, including their private chips.
  6. [update] all players. What happens: When deck is empty and current_card == 0: each player's final_score = card_points - chips, and pot = 0 (leftover chips are out of the game).
  7. [check] table. What happens: End the game if deck is empty and current_card == 0; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, 13 of the 33 cards numbered 3 to 35 are removed unseen and the remaining 20 form the deck.
  R2. At setup, each player has 11 chips, an empty tableau and 0 card points. Chips are visible only to their owner.
  R3. At setup, current_card is 0 (none), pot is 0, lap_count is 0 and lead_seat is 1.
  R4. When a round starts with current_card == 0 and a non-empty deck, then one deck card becomes current_card, the deck shrinks by 1, lap_count becomes 0 and the pot is unchanged.
  R5. When the current card is offered, then offers start at lead_seat, go clockwise, and each seat is offered it at most once per round.
  R6. When a player chooses PAY, then their chips decrease by 1, the pot increases by 1, and the next seat clockwise is offered the card.
  R7. When a player has 0 chips and is offered the card, then their only option is TAKE.
  R8. When a player chooses TAKE, then their chips increase by the pot, the pot becomes 0, current_card is appended to their tableau, current_card becomes 0, and no further seat is offered the card this round.
  R9. When a player takes a card, then lead_seat becomes that player's seat.
  R10. When a player takes card c, then their card_points change by (c if they do not hold c-1, else 0) minus (c+1 if they hold c+1, else 0). For example, taking 20 with 21 in the tableau and no 19 changes card_points by 20 - 21 = -1.
  R11. When every player chooses PAY in a round and lap_count becomes 1, then the card stays current with its pot and the next round starts its offers at the same lead_seat.
  R12. When every player chooses PAY in a round and lap_count becomes 2, then the card is appended to burned, current_card becomes 0, the pot stays unchanged for the next card, and lead_seat becomes (lead_seat mod N) + 1.
  R13. When a round ends, then every pay, take, chips gained or burn is announced publicly, together with the pot and every tableau.
  R14. When the deck is empty and current_card == 0, then the game ends and any chips left in the pot are out of the game.
  R15. When the game ends, then each player's final_score = card_points - chips.
  R16. When the game ends, then the lowest final_score wins; a tie for lowest goes to the player with more chips; players still tied share a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - PAY or TAKE the current card | asked: each seat in turn from lead_seat, clockwise, until someone takes or all seats have been asked once | options: a seat with chips >= 1: PAY, TAKE; a seat with chips == 0: TAKE

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: count(deck) == 0 and current_card == 0
  - each player's standing: (you.chips - you.card_points) * 100 + you.chips (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Final score is card points minus chips, and the lowest final score wins. Among players tied for lowest, the one with more chips wins. Players still tied share the win, which is a draw.
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

- each player: `tableau` (list, visible: public, starts []): The face-up cards this player has taken.
- each player: `card_points` (number, visible: public, starts 0): The sum of the lowest card of each run of consecutive numbers in the tableau.
- each player: `final_score` (number, visible: public, starts 0): card_points minus chips, set when the game ends.
- the table: `burned` (list, visible: public, starts []): Cards burned after two laps with no taker.
- the table: `current_card` (number, visible: public, starts 0): The card on offer. 0 means there is no current card.
- the table: `pot` (number, visible: public, starts 0): Chips in the middle.
- the table: `lap_count` (number, visible: public, starts 0): Full laps in which every player paid on the current card.
- the table: `lead_seat` (number, visible: public, starts 1): The seat that is offered the current card first.
- parameters (each must be an attribute holding this value, never a number buried in a step): card_min = 3, card_max = 35, total_cards = 33, removed_cards = 13, deck_size = 20, starting_chips = 11, pay_cost = 1, laps_to_stay = 1, laps_to_burn = 2, first_lead_seat = 1, rank_score_multiplier = 100
- the game ends with ONE ending whose `rank_by` is `(you.chips - you.card_points) * 100 + you.chips`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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

Implement the offer as a real per-seat sequential choice. Starting at lead_seat and going clockwise, present a choice step to each seat in turn while the card is still untaken (gate each step with a `when` on taken == false and on the seat not yet having been offered this round). The options should be PAY and TAKE. When the seat's chips are 0, offer only TAKE, but still pose it as a choice step that the player answers. Do not auto-apply TAKE or skip the poll. Make sure the step that draws a card from the deck when current_card is 0 runs before the offers, so a card is on offer when the first seat is asked. On TAKE: add the pot to the taker's chips, append the card to their tableau, update card_points by the run rule, set pot to 0, current_card to 0 and lead_seat to the taker, and skip the remaining offers. When all seats PAY: increment lap_count. If it equals laps_to_stay, keep the card and lead_seat for the next round. If it equals laps_to_burn, append the card to burned, set current_card to 0, keep the pot, and advance lead_seat clockwise. The game ends only when the deck is empty and current_card is 0. Then set final_score = card_points - chips and use the specified rank_by ending.

````

## Reply

````
```json
{
  "schema": 1,
  "meta": {
    "id": "no_thanks_two_laps",
    "name": "No Thanks! Two Laps",
    "players": {
      "min": 3,
      "max": 4,
      "suggested": 4
    },
    "blurb": "Pay a chip to refuse each card or take it with the pot. A card refused for two full laps is burned and its pot carries over. Lowest card points minus chips wins."
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
        "key": "chips",
        "visible": "ally",
        "type": "number",
        "initial": 11
      },
      {
        "key": "tableau",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "card_points",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "final_score",
        "visible": "public",
        "type": "number",
        "initial": 0
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
        "initial": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
      },
      {
        "key": "removed",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "burned",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "current_card",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pot",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lap_count",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "lead_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "taken",
        "visible": "public",
        "type": "bool",
        "initial": false
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_card",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_gain",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_taker",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "last_outcome",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "card_min",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "card_max",
        "visible": "public",
        "type": "number",
        "initial": 35
      },
      {
        "key": "total_cards",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "removed_cards",
        "visible": "public",
        "type": "number",
        "initial": 13
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "starting_chips",
        "visible": "public",
        "type": "number",
        "initial": 11
      },
      {
        "key": "pay_cost",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "laps_to_stay",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "laps_to_burn",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "first_lead_seat",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "rank_score_multiplier",
        "visible": "public",
        "type": "number",
        "initial": 100
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "remove cards unseen",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"key": "removed", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": 0}}
      ]
    },
    {
      "use": "update",
      "label": "players and table start",
      "do": [
        {"set": {"players": "all", "key": "chips", "value": {"calc": "starting_chips"}}},
        {"set": {"players": "all", "key": "tableau", "value": []}},
        {"set": {"players": "all", "key": "card_points", "value": 0}},
        {"set": {"players": "all", "key": "final_score", "value": 0}},
        {"set": {"key": "current_card", "value": 0}},
        {"set": {"key": "pot", "value": 0}},
        {"set": {"key": "lap_count", "value": 0}},
        {"set": {"key": "lead_seat", "value": {"calc": "first_lead_seat"}}}
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
      "phase": "reveal",
      "label": "the card on offer",
      "do": [
        {"set": {"key": "taken", "value": false}},
        {"set": {"key": "last_outcome", "value": ""}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "current_card == 0 and len(deck) > 0"}}},
        {"set": {"key": "lap_count", "value": 0, "if": {"calc": "current_card == 0 and len(deck) > 0"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "current_card == 0 and len(deck) > 0"}}},
        {"set": {"key": "current_card", "value": {"calc": "pick"}, "if": {"calc": "current_card == 0 and pick > 0"}}},
        {"set": {"key": "pick", "value": 0}},
        {"set": {"players": "all", "key": "offer", "value": {"calc": "(['PAY'] if you.chips >= pay_cost else []) + ['TAKE']"}}}
      ],
      "text": "Card {current_card} is on offer. Pot: {pot}. Laps so far on this card: {lap_count}. Seat {lead_seat} is offered it first."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer to the lead seat",
      "when": {"calc": "(not taken) and current_card > 0"},
      "to": {"where": "you.seat == ((lead_seat - 1) % len(players)) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "each": {
        "do": [
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "-pay_cost"}, "if": {"calc": "$answer == 'PAY'"}}},
          {"adjust": {"key": "pot", "value": {"calc": "pay_cost"}, "if": {"calc": "$answer == 'PAY'"}, "text": "The pot is now {pot}."}},
          {"set": {"key": "last_card", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_gain", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_taker", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "card_points", "value": {"calc": "(current_card if not ((current_card - 1) in players[$seat - 1].tableau) else 0) - (current_card + 1 if (current_card + 1) in players[$seat - 1].tableau else 0)"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"append": {"player": "$seat", "key": "tableau", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}, "text": "Seat {last_taker} takes card {last_card} and gains {last_gain} chips."}},
          {"set": {"key": "pot", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "current_card", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lap_count", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lead_seat", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_outcome", "value": "taken", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "taken", "value": true, "if": {"calc": "$answer == 'TAKE'"}}}
        ]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "text": "Card {current_card} is offered to you. Pot: {pot}. PAY puts {pay_cost} chip from your hand into the pot and passes the card to the next seat clockwise. TAKE gives you the card and every chip in the pot. With 0 chips you must TAKE."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer to the second seat",
      "when": {"calc": "(not taken) and current_card > 0"},
      "to": {"where": "you.seat == ((lead_seat - 1 + 1) % len(players)) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "each": {
        "do": [
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "-pay_cost"}, "if": {"calc": "$answer == 'PAY'"}}},
          {"adjust": {"key": "pot", "value": {"calc": "pay_cost"}, "if": {"calc": "$answer == 'PAY'"}, "text": "The pot is now {pot}."}},
          {"set": {"key": "last_card", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_gain", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_taker", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "card_points", "value": {"calc": "(current_card if not ((current_card - 1) in players[$seat - 1].tableau) else 0) - (current_card + 1 if (current_card + 1) in players[$seat - 1].tableau else 0)"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"append": {"player": "$seat", "key": "tableau", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}, "text": "Seat {last_taker} takes card {last_card} and gains {last_gain} chips."}},
          {"set": {"key": "pot", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "current_card", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lap_count", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lead_seat", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_outcome", "value": "taken", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "taken", "value": true, "if": {"calc": "$answer == 'TAKE'"}}}
        ]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "text": "Card {current_card} is offered to you. Pot: {pot}. PAY puts {pay_cost} chip from your hand into the pot and passes the card to the next seat clockwise. TAKE gives you the card and every chip in the pot. With 0 chips you must TAKE."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer to the third seat",
      "when": {"calc": "(not taken) and current_card > 0"},
      "to": {"where": "you.seat == ((lead_seat - 1 + 2) % len(players)) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "each": {
        "do": [
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "-pay_cost"}, "if": {"calc": "$answer == 'PAY'"}}},
          {"adjust": {"key": "pot", "value": {"calc": "pay_cost"}, "if": {"calc": "$answer == 'PAY'"}, "text": "The pot is now {pot}."}},
          {"set": {"key": "last_card", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_gain", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_taker", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "card_points", "value": {"calc": "(current_card if not ((current_card - 1) in players[$seat - 1].tableau) else 0) - (current_card + 1 if (current_card + 1) in players[$seat - 1].tableau else 0)"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"append": {"player": "$seat", "key": "tableau", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}, "text": "Seat {last_taker} takes card {last_card} and gains {last_gain} chips."}},
          {"set": {"key": "pot", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "current_card", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lap_count", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lead_seat", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_outcome", "value": "taken", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "taken", "value": true, "if": {"calc": "$answer == 'TAKE'"}}}
        ]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "text": "Card {current_card} is offered to you. Pot: {pot}. PAY puts {pay_cost} chip from your hand into the pot and passes the card to the next seat clockwise. TAKE gives you the card and every chip in the pot. With 0 chips you must TAKE."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer to the fourth seat",
      "when": {"calc": "(not taken) and current_card > 0 and len(players) > 3"},
      "to": {"where": "you.seat == ((lead_seat - 1 + 3) % len(players)) + 1"},
      "answer": {"type": "choice", "options": {"attribute": "offer"}},
      "each": {
        "do": [
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "-pay_cost"}, "if": {"calc": "$answer == 'PAY'"}}},
          {"adjust": {"key": "pot", "value": {"calc": "pay_cost"}, "if": {"calc": "$answer == 'PAY'"}, "text": "The pot is now {pot}."}},
          {"set": {"key": "last_card", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_gain", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_taker", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "card_points", "value": {"calc": "(current_card if not ((current_card - 1) in players[$seat - 1].tableau) else 0) - (current_card + 1 if (current_card + 1) in players[$seat - 1].tableau else 0)"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"append": {"player": "$seat", "key": "tableau", "value": {"calc": "current_card"}, "if": {"calc": "$answer == 'TAKE'"}}},
          {"adjust": {"player": "$seat", "key": "chips", "value": {"calc": "pot"}, "if": {"calc": "$answer == 'TAKE'"}, "text": "Seat {last_taker} takes card {last_card} and gains {last_gain} chips."}},
          {"set": {"key": "pot", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "current_card", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lap_count", "value": 0, "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "lead_seat", "value": "$seat", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "last_outcome", "value": "taken", "if": {"calc": "$answer == 'TAKE'"}}},
          {"set": {"key": "taken", "value": true, "if": {"calc": "$answer == 'TAKE'"}}}
        ]
      },
      "broadcast": {"to": "all", "text": "Seat {seat} chooses {value}."},
      "text": "Card {current_card} is offered to you. Pot: {pot}. PAY puts {pay_cost} chip from your hand into the pot and passes the card to the next seat clockwise. TAKE gives you the card and every chip in the pot. With 0 chips you must TAKE."
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "a full lap of pays",
      "when": {"calc": "(not taken) and current_card > 0"},
      "do": [
        {"adjust": {"key": "lap_count", "value": 1}},
        {"set": {"key": "last_outcome", "value": {"calc": "'burned' if lap_count >= laps_to_burn else 'stayed'"}}},
        {"set": {"key": "last_card", "value": {"calc": "current_card"}}},
        {"append": {"key": "burned", "value": {"calc": "current_card"}, "if": {"calc": "last_outcome == 'burned'"}}},
        {"set": {"key": "current_card", "value": 0, "if": {"calc": "last_outcome == 'burned'"}}},
        {"set": {"key": "lap_count", "value": 0, "if": {"calc": "last_outcome == 'burned'"}}},
        {"set": {"key": "lead_seat", "value": {"calc": "(lead_seat % len(players)) + 1"}, "if": {"calc": "last_outcome == 'burned'"}}}
      ]
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the card was taken",
      "when": {"calc": "last_outcome == 'taken'"},
      "to": "all",
      "text": "Seat {last_taker} took card {last_card} with {last_gain} chips and leads the next card. Pot: {pot}. Tableaus and card points [seat, tableau, card points]: {[[p.seat, p.tableau, p.card_points] for p in players]}. Burned: {burned}."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the card stays",
      "when": {"calc": "last_outcome == 'stayed'"},
      "to": "all",
      "text": "Every player paid. Card {last_card} stays on offer after lap {lap_count} with a pot of {pot}; seat {lead_seat} is offered it first again. Tableaus and card points [seat, tableau, card points]: {[[p.seat, p.tableau, p.card_points] for p in players]}. Burned: {burned}."
    },
    {
      "use": "tell",
      "phase": "resolve",
      "label": "the card is burned",
      "when": {"calc": "last_outcome == 'burned'"},
      "to": "all",
      "text": "Every player paid for a second lap. Card {last_card} is burned. The pot of {pot} stays for the next card, which seat {lead_seat} is offered first. Tableaus and card points [seat, tableau, card points]: {[[p.seat, p.tableau, p.card_points] for p in players]}. Burned: {burned}."
    },
    {
      "use": "sync",
      "phase": "resolve",
      "label": "your standing",
      "mode": "self",
      "to": "all",
      "text": "Where you stand:"
    },
    {
      "use": "update",
      "phase": "resolve",
      "label": "final scores",
      "when": {"calc": "len(deck) == 0 and current_card == 0"},
      "do": [
        {"set": {"players": "all", "key": "final_score", "value": {"calc": "you.card_points - you.chips"}}},
        {"set": {"key": "pot", "value": 0}}
      ],
      "text": "The deck is empty. Leftover chips in the pot are out of the game."
    },
    {
      "use": "check",
      "phase": "resolve",
      "label": "deck exhausted",
      "when": {"calc": "len(deck) == 0 and current_card == 0"},
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {"calc": "len(deck) == 0 and current_card == 0"},
      "rank_by": "(you.chips - you.card_points) * 100 + you.chips",
      "reveal": ["chips"],
      "text": "Winner: {result}. Final scores [seat, final score, chips]: {[[p.seat, p.final_score, p.chips] for p in players]}."
    }
  },
  "limits": {
    "rounds": 60,
    "rounds_max": 60,
    "actions_max": 1000,
    "deadline_s": 120
  },
  "rules": "SETUP: Cards numbered {card_min} to {card_max} ({total_cards} cards) are shuffled and {removed_cards} are removed face-down without anyone seeing them; they are out of the game. The remaining {deck_size} cards form the deck. Players are numbered 1 to N clockwise. Each player receives {starting_chips} chips; your chip count is private, only you are told it. Every action (pay, take, chips gained, burn) is announced publicly. Each player has a face-up tableau, which starts empty, and a card-points total, which starts at 0. The current card, the pot and the lap count of the current card are public. The lead player for the first card is player {first_lead_seat}.\n\nEACH ROUND:\n1. If there is no current card, the top deck card is revealed. It becomes the current card, its lap count is set to 0, and the pot is unchanged: it may hold chips carried over from a burned card.\n2. The current card is offered once around the table. Offers start with the lead player and go clockwise, and stop when someone takes it or every player has been offered it once this round.\n3. When offered the card, you choose PAY or TAKE. A player with 0 chips must choose TAKE.\n- PAY: you put {pay_cost} chip from your hand into the pot, and the card is offered to the next player.\n- TAKE: you add all chips in the pot to your hand, place the card in your tableau, and the pot becomes 0. The card is no longer current. You become the lead player for the next card, and the round ends at once.\n4. When you take card c, your card-points total changes by (c if you do not hold c-1, else 0) minus (c+1 if you hold c+1, else 0). Card points therefore always equal the sum of the lowest card of each run of consecutive numbers in your tableau. Example: taking 20 with 21 in your tableau and no 19 changes your card points by 20 - 21 = -1.\n5. If every player chose PAY this round, the card's lap count increases by 1.\n- If the lap count is now {laps_to_stay}, the card stays current with its pot, and the next round offers it again starting from the same lead player.\n- If the lap count is now {laps_to_burn}, the card is burned (removed from the game). The pot stays in the middle for the next card, and the lead player for the next card becomes the player clockwise of the current lead player.\n6. What happened is announced: who paid, who took what with how many chips, or that the card was burned, plus the pot size and every tableau.\n7. If the deck is empty and there is no current card, the game ends. Any chips left in the pot are out of the game.\n\nThere is no discussion phase.\n\nEND: Each player's final score is card points minus chips in hand. The player with the lowest final score wins. If several players tie for lowest, the one among them with more remaining chips wins. If they are still tied, the game is a draw among them."
}
```
````
