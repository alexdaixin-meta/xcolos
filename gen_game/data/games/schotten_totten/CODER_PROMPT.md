# Task: write the XColos game file for "Schotten Totten: Five Stones"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

COMPONENTS: A deck of 36 cards, 4 colours (Red, Blue, Green, Yellow) x values 1-9, each card written like 'R7'. There are 5 Stones numbered 1-5. Each Stone has a side for Player A and a side for Player B, and each side holds at most 3 cards.

SETUP: Shuffle the deck. Deal 6 cards face down to each player. Each hand is private: only its owner sees it. The remaining 24 cards form a face-down draw pile. Randomly decide which player is A; A takes the first turn.

ROUNDS: The game has at most 30 rounds. In odd rounds Player A is active; in even rounds Player B is active. Each round:
(1) The engine announces to both players the cards on every side of every Stone, which Stones are claimed and by whom, each player's number of claimed Stones, and how many cards remain in the draw pile.
(2) The active player chooses one card from their hand.
(3) The active player chooses one Stone that is unclaimed and whose side for that player holds fewer than 3 cards. A player always has such a Stone and a card to play, and must play.
(4) The card moves from the hand to that player's side of the chosen Stone, face up. Cards never move again.
(5) If this card was the third card on that side and the other side has fewer than 3 cards, record this player as that Stone's 'first finisher'.
(6) If the draw pile is not empty, the active player draws its top card into their hand.
(7) For each unclaimed Stone where both sides now hold 3 cards, resolve it, as described below.
(8) If either player has claimed 3 Stones, the game ends immediately and that player wins.

STRENGTH OF A SIDE: Let the three values sum to S. The side has one formation:
- Straight Flush: all three cards share a colour, the values are all different, and highest minus lowest equals 2. Bonus 120.
- Three of a Kind: all three values are equal. Bonus 90.
- Flush: all three cards share a colour (and the side is not a Straight Flush). Bonus 60.
- Straight: the values are all different and highest minus lowest equals 2 (and the side is not a Straight Flush). Bonus 30.
- Otherwise: bonus 0.
Strength = S + bonus.

RESOLVING A STONE: The side with the higher strength claims the Stone. If the strengths are equal, the first finisher of that Stone claims it. A claimed Stone stays on the table with its cards visible, but it can no longer be played on.

END OF CARDS: After round 30 every Stone has been resolved. If no one has reached 3 Stones (possible only if the game has not yet ended), the player with more claimed Stones wins. Equal counts are a draw.

How the winner is decided: The first player to claim 3 of the 5 Stones wins immediately. If the game reaches the end of round 30 without this, the player with more claimed Stones wins, and equal counts are a draw. With the first-finisher tie-break every resolved Stone has an owner, so in practice someone reaches 3.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Schotten Totten: Five Stones (2 to 2 players, best with 2)

Two players take turns placing cards from a private hand onto their side of five Stones, forming three-card poker-like formations; a player claims a Stone with the stronger side, and the first to claim 3 of the 5 Stones wins.

STATE (every item below must exist in the file):
  - each player: hand (list, starts []); only its owner sees it. The card codes this player holds, like 'R7'. Only the owner sees them.
  - each player: claimed (number, starts 0); everyone sees it. Number of Stones this player has claimed. This is the score.
  - each player: role (text, starts ''); everyone sees it. 'A' for seat 1 or 'B' for seat 2. A acts in odd rounds and B in even rounds.
  - the table: deck (list, starts 'all 36 codes R1..R9, B1..B9, G1..G9, Y1..Y9'); hidden from all players. The face-down draw pile.
  - the table: deck_count (number, starts 36); everyone sees it. Number of cards left in the draw pile. It is 24 after the deal.
  - the table: round (number, starts 0); everyone sees it. The current round, from 1 to 30.
  - the table: active_seat (number, starts 1); everyone sees it. 1 (A) in odd rounds and 2 (B) in even rounds.
  - the table: stone_1_a (list, starts []); everyone sees it. Face-up cards on A's side of Stone 1, at most 3.
  - the table: stone_1_b (list, starts []); everyone sees it. Face-up cards on B's side of Stone 1, at most 3.
  - the table: stone_2_a (list, starts []); everyone sees it. A's side of Stone 2.
  - the table: stone_2_b (list, starts []); everyone sees it. B's side of Stone 2.
  - the table: stone_3_a (list, starts []); everyone sees it. A's side of Stone 3.
  - the table: stone_3_b (list, starts []); everyone sees it. B's side of Stone 3.
  - the table: stone_4_a (list, starts []); everyone sees it. A's side of Stone 4.
  - the table: stone_4_b (list, starts []); everyone sees it. B's side of Stone 4.
  - the table: stone_5_a (list, starts []); everyone sees it. A's side of Stone 5.
  - the table: stone_5_b (list, starts []); everyone sees it. B's side of Stone 5.
  - the table: stone_owner (list, starts ['', '', '', '', '']); everyone sees it. Who has claimed each Stone 1-5: '' (unclaimed), 'A' or 'B'.
  - the table: first_finisher (list, starts ['', '', '', '', '']); everyone sees it. For each Stone, 'A' or 'B': the player who first completed 3 cards on their side while the other side held fewer than 3.
  - parameters, each kept as a table attribute: deck_size = 36, colours = 4, max_card_value = 9, stones = 5, side_capacity = 3, hand_size = 6, draw_pile_after_deal = 24, max_rounds = 30, stones_to_win = 3, straight_flush_bonus = 120, three_of_a_kind_bonus = 90, flush_bonus = 60, straight_bonus = 30, no_formation_bonus = 0, straight_span = 2

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. The deck holds the 36 cards R1-R9, B1-B9, G1-G9 and Y1-Y9.
  2. Seats are assigned at random: seat 1 is Player A (role 'A') and seat 2 is Player B (role 'B'). A takes the first turn.
  3. Each player is dealt 6 cards: each draw picks a random card from deck, appends it to that player's hand and removes it from deck.
  4. deck_count is set to 24.
  5. All ten Stone sides start empty. stone_owner and first_finisher start as five empty entries.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1; active_seat = 1 if round is odd, else 2.
  2. [tell] all players. What happens: Announce every Stone's sides (stone_k_a, stone_k_b), stone_owner, each player's claimed, and deck_count.
  3. [sync] all players. What happens: Each player privately sees their own hand.
  4. [ask] the active player (seat active_seat) answers: one card code from their hand. What happens: The chosen card is remembered as the card to play.
  5. [ask] the active player (seat active_seat) answers: one Stone number from 1-5 that is unclaimed (stone_owner[k] == '') and where the active player's side holds fewer than 3 cards. What happens: The chosen Stone k is remembered.
  6. [update] the active player. What happens: Remove the chosen card from the active player's hand and append it to stone_k_a (if active_seat == 1) or stone_k_b (if active_seat == 2). Cards never move again.
  7. [update] the active player. What happens: If the active side of Stone k now has 3 cards and the opposite side has fewer than 3, set first_finisher[k] = the active player's role.
  8. [update] the active player. What happens: If deck_count > 0, draw a random card from deck into the active player's hand and set deck_count -= 1.
  9. [update] all players. What happens: For each Stone k = 1..5 where stone_owner[k] == '' and both len(stone_k_a) == 3 and len(stone_k_b) == 3, compute strength_a and strength_b by the strength formula. If strength_a > strength_b, the owner is 'A'. If strength_b > strength_a, the owner is 'B'. If they are equal, the owner is first_finisher[k]. Set stone_owner[k] to the owner and add 1 to that player's claimed. Announce the result.
  10. [check] all players. What happens: End the game if any player's claimed >= 3, or if round >= 30. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, each player holds 6 cards in hand and the deck holds 24.
  R2. When the round number is odd, seat 1 (A) is the only player asked to act; when it is even, seat 2 (B) is the only one asked.
  R3. When the active player is asked for a card, the options are exactly the cards in their hand.
  R4. When the active player is asked for a Stone, the options are exactly the Stones that are unclaimed and whose side for that player holds fewer than 3 cards.
  R5. When a card is played on Stone k, it leaves the player's hand, is appended to that player's side of Stone k, and never moves again.
  R6. When a played card is the third on its side and the other side holds fewer than 3 cards, first_finisher[k] is set to the player's role.
  R7. When deck_count > 0 after a play, the active player draws one card and deck_count drops by 1; when deck_count == 0, no card is drawn.
  R8. When all three cards on a side share a colour, have different values, and highest minus lowest is 2, the strength is the sum of the values + 120 (for example, R3 R4 R5 has strength 132).
  R9. When all three values on a side are equal, the strength is the sum + 90 (for example, R7 B7 G7 has strength 111).
  R10. When all three cards share a colour but the side is not a straight flush, the strength is the sum + 60 (for example, B1 B5 B9 has strength 75).
  R11. When the values are all different with highest minus lowest equal to 2 but the colours are mixed, the strength is the sum + 30 (for example, R6 B7 G8 has strength 51).
  R12. When a side has no formation, its strength is just the sum (for example, R2 B5 G9 has strength 16).
  R13. When both sides of an unclaimed Stone hold 3 cards, the side with the higher strength claims it and that player's claimed goes up by 1.
  R14. When both sides of a completed Stone have equal strength, the Stone's first_finisher claims it.
  R15. When a Stone is claimed, it can no longer be offered as a Stone to play on.
  R16. When a player's claimed reaches 3, the game ends immediately and that player wins.
  R17. When round 30 ends and nobody has 3 Stones, the player with more claimed Stones wins, and equal counts are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Which card to play | asked: the active seat only (seat 1 in odd rounds, seat 2 in even rounds) | options: Every card code currently in that seat's hand. The inactive seat is asked nothing.
  - Which Stone to play on | asked: the active seat only | options: Every Stone number 1-5 with stone_owner[k] == '' whose side for the active player holds fewer than 3 cards. Claimed Stones and Stones where the player's side is full are never offered.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: max over players of claimed >= 3, or round >= 30
  - each player's standing: you.claimed (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: A player's standing is the number of Stones they have claimed. The first to reach 3 wins at once. If round 30 ends without that, the player with more claimed Stones wins, and equal counts share the win (a draw).
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

- each player: `claimed` (number, visible: public, starts 0): Number of Stones this player has claimed. This is the score.
- the table: `stone_owner` (list, visible: public, starts ['', '', '', '', '']): Who has claimed each Stone 1-5: '' (unclaimed), 'A' or 'B'.
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 36, colours = 4, max_card_value = 9, stones = 5, side_capacity = 3, hand_size = 6, draw_pile_after_deal = 24, max_rounds = 30, stones_to_win = 3, straight_flush_bonus = 120, three_of_a_kind_bonus = 90, flush_bonus = 60, straight_bonus = 30, no_formation_bonus = 0, straight_span = 2
- the game ends with ONE ending whose `rank_by` is `you.claimed`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
