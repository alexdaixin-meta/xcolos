# Task: write the XColos game file for "Cockroach Poker: Straight Calls"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP
- The deck has 24 cards: 4 creatures (Cockroach, Rat, Stinkbug, Toad), 6 copies of each.
- Shuffle. Deal 7 cards face-down to each of the 3 players as their private hand. Set the remaining 3 cards aside face-down, unseen by anyone, for the whole game.
- Each player starts with no face-up cards.
- Choose the first sender uniformly at random.

EACH ROUND (at most 24 rounds)
1. Announce the round number, the sender, and every player's face-up cards (counts per creature) and hand size.
2. The sender privately chooses one card from their own hand.
3. The sender chooses a claim: one of the 4 creatures. It may be true or false.
4. The sender chooses a receiver: either of the other two players.
5. The receiver, who sees the claim but not the card, calls TRUE (the card is the claimed creature) or FALSE (it is not).
6. Reveal the card to everyone.
   - The receiver is correct if they called TRUE and the card matches the claim, or called FALSE and it does not.
   - If the receiver is correct, the sender takes the card face-up.
   - If the receiver is wrong, the receiver takes it face-up.
   - Either way, the card has left the sender's hand.
7. The player who took the card face-up becomes the sender for the next round.
8. Loss check: if the player who took the card now has 3 face-up cards of the same creature, that player LOSES and the game ends.
9. Empty-hand check: if the next sender has no cards in hand, that player LOSES and the game ends.
10. If round 24 has finished without a loser, the game ends with no loser.

TALK
There is no separate talk phase. The claim is the only message.

ENDING
When the game ends, the losing player (if any) cannot win. The players who did not lose are ranked by these tests in order:
(a) fewest total face-up cards;
(b) if tied, the smaller count of their single most common face-up creature;
(c) if still tied, the most cards remaining in hand.
The player ranked first wins. If the top players are tied on all three tests, the game is a draw between them.

How the winner is decided: Avoid being the loser, who ends the game with 3 face-up cards of one creature or must send with an empty hand. Among the players who did not lose, the one with the fewest face-up cards wins. Ties are broken by the smaller count of their most common face-up creature, then by more cards left in hand. Players tied on all three draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Cockroach Poker: Straight Calls (3 to 3 players, best with 3)

Three players pass cards face-down with a creature claim. The receiver calls the claim true or false, and whoever is wrong about the card takes it face-up. Three face-up cards of one creature, or having to send from an empty hand, loses.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The player's private hand of creature cards, one entry per card, such as 'Rat'.
  - each player: hand_size (number, starts 0); everyone sees it. Number of cards in the hand.
  - each player: face_cockroach (number, starts 0); everyone sees it. Face-up Cockroach cards.
  - each player: face_rat (number, starts 0); everyone sees it. Face-up Rat cards.
  - each player: face_stinkbug (number, starts 0); everyone sees it. Face-up Stinkbug cards.
  - each player: face_toad (number, starts 0); everyone sees it. Face-up Toad cards.
  - each player: face_total (number, starts 0); everyone sees it. Total face-up cards, the sum of the four face counts.
  - each player: max_face (number, starts 0); everyone sees it. Largest of the four face counts.
  - each player: lost (number, starts 0); everyone sees it. 1 if this player has lost, otherwise 0.
  - the table: deck (list, starts ['Cockroach x6', 'Rat x6', 'Stinkbug x6', 'Toad x6']); hidden from all players. The 24-card deck before dealing: 6 entries of each creature.
  - the table: aside (list, starts []); hidden from all players. The 3 cards set aside face-down, unseen by anyone, for the whole game.
  - the table: round (number, starts 1); everyone sees it. Current round number.
  - the table: sender (number, starts 0); everyone sees it. Seat of the current sender.
  - the table: receiver (number, starts 0); everyone sees it. Seat chosen as receiver this round.
  - the table: card_in_play (text, starts ''); hidden from all players. The creature on the card being passed. It stays hidden until the reveal.
  - the table: revealed_card (text, starts ''); everyone sees it. The passed card's creature, made public at the reveal.
  - the table: claim (text, starts ''); everyone sees it. The sender's claimed creature.
  - the table: call (text, starts ''); everyone sees it. The receiver's call, TRUE or FALSE.
  - the table: taker (number, starts 0); everyone sees it. Seat that took the card face-up this round.
  - the table: game_over (number, starts 0); everyone sees it. 1 once the game has ended.
  - parameters, each kept as a table attribute: deck_size = 24, creature_kinds = 4, copies_per_creature = 6, hand_size_start = 7, aside_cards = 3, max_rounds = 24, loss_same_creature = 3, receiver_options = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Fill deck with 24 cards: 6 each of Cockroach, Rat, Stinkbug and Toad.
  2. Deal 7 cards to each of the 3 players. Each card is a random draw removed from deck and appended to that player's hand. Set each hand_size to 7.
  3. Move the remaining 3 cards from deck to aside, unseen by anyone, for the whole game.
  4. Every player starts with all face counts, face_total, max_face and lost at 0.
  5. Set sender to a seat chosen uniformly at random, and set round to 1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [tell] all players. What happens: Announce round, sender, and each player's face_cockroach, face_rat, face_stinkbug, face_toad and hand_size.
  2. [ask] the sender (seat = sender) answers: one creature present in the sender's hand. What happens: Set card_in_play to the chosen creature. Remove one card of that creature from the sender's hand and decrease the sender's hand_size by 1.
  3. [ask] the sender (seat = sender) answers: one of Cockroach, Rat, Stinkbug, Toad. What happens: Set claim to the answer, visible to all.
  4. [ask] the sender (seat = sender) answers: one of the two other seats. What happens: Set receiver to the chosen seat.
  5. [ask] the receiver (seat = receiver) answers: TRUE or FALSE. What happens: Set call to the answer.
  6. [update] all players. What happens: Set revealed_card = card_in_play and announce it. Let correct = (call == TRUE and card_in_play == claim) or (call == FALSE and card_in_play != claim). If correct, taker = sender, otherwise taker = receiver. Add 1 to the taker's face_<card_in_play> and to their face_total, and recompute the taker's max_face.
  7. [update] all players. What happens: Set sender = taker for the next round.
  8. [check] all players. What happens: If the taker's face count for revealed_card >= 3, set the taker's lost = 1 and game_over = 1, and end the game.
  9. [check] all players. What happens: If the new sender's hand_size == 0, set that player's lost = 1 and game_over = 1, and end the game.
  10. [check] all players. What happens: If round >= 24, set game_over = 1 and end the game with no loser. Otherwise add 1 to round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, each of the 3 players holds 7 cards, 3 cards are set aside unseen, and the deck of 24 (6 of each of 4 creatures) is fully used.
  R2. At setup, every player has 0 face-up cards and lost = 0, and the first sender is a random seat.
  R3. Each round, the sender passes one card from their own hand, and the sender's hand_size falls by 1.
  R4. The sender's claim is one of Cockroach, Rat, Stinkbug or Toad, and it may differ from the card.
  R5. The receiver must be one of the two seats other than the sender.
  R6. When the receiver calls TRUE and the card matches the claim, the sender takes the card face-up.
  R7. When the receiver calls FALSE and the card does not match the claim, the sender takes the card face-up.
  R8. When the receiver calls TRUE and the card does not match, or calls FALSE and it matches, the receiver takes the card face-up.
  R9. The card is revealed to everyone after the call, and the taker's count for that creature and face_total rise by 1.
  R10. The player who took the card face-up is the sender of the next round.
  R11. When the taker reaches 3 face-up cards of one creature, the taker's lost becomes 1 and the game ends.
  R12. When the next sender has 0 cards in hand, that player's lost becomes 1 and the game ends.
  R13. When round 24 finishes without a loser, the game ends with no loser.
  R14. A player with lost = 1 cannot win.
  R15. Among the players who did not lose, the one with the fewest face_total wins.
  R16. If face_total is tied, the smaller max_face wins. If that is still tied, the larger hand_size wins. If all three are tied, the tied players draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Which card to pass | asked: the sender only | options: each distinct creature currently in the sender's hand
  - Which creature to claim | asked: the sender only | options: Cockroach, Rat, Stinkbug, Toad
  - Who receives the card | asked: the sender only | options: the two seats other than the sender
  - Call the claim | asked: the receiver only | options: TRUE, FALSE

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: game_over == 1, which happens when some player's lost == 1 or when round 24 has finished
  - each player's standing: (1 - you.lost) * 1000000 - you.face_total * 10000 - you.max_face * 100 + you.hand_size (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player who lost can never rank above a player who did not. Among the others, fewest face-up cards ranks first, then the smaller most-common face-up creature count, then more cards left in hand. The highest value wins, and players level on all three tests share the win (a draw).
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

- each player: `hand_size` (number, visible: public, starts 0): Number of cards in the hand.
- each player: `face_cockroach` (number, visible: public, starts 0): Face-up Cockroach cards.
- each player: `face_rat` (number, visible: public, starts 0): Face-up Rat cards.
- each player: `face_stinkbug` (number, visible: public, starts 0): Face-up Stinkbug cards.
- each player: `face_toad` (number, visible: public, starts 0): Face-up Toad cards.
- each player: `face_total` (number, visible: public, starts 0): Total face-up cards, the sum of the four face counts.
- each player: `max_face` (number, visible: public, starts 0): Largest of the four face counts.
- each player: `lost` (number, visible: public, starts 0): 1 if this player has lost, otherwise 0.
- the table: `round` (number, visible: public, starts 1): Current round number.
- the table: `sender` (number, visible: public, starts 0): Seat of the current sender.
- the table: `receiver` (number, visible: public, starts 0): Seat chosen as receiver this round.
- the table: `revealed_card` (text, visible: public, starts ''): The passed card's creature, made public at the reveal.
- the table: `claim` (text, visible: public, starts ''): The sender's claimed creature.
- the table: `call` (text, visible: public, starts ''): The receiver's call, TRUE or FALSE.
- the table: `taker` (number, visible: public, starts 0): Seat that took the card face-up this round.
- the table: `game_over` (number, visible: public, starts 0): 1 once the game has ended.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 24, creature_kinds = 4, copies_per_creature = 6, hand_size_start = 7, aside_cards = 3, max_rounds = 24, loss_same_creature = 3, receiver_options = 2
- the game ends with ONE ending whose `rank_by` is `(1 - you.lost) * 1000000 - you.face_total * 10000 - you.max_face * 100 + you.hand_size`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
