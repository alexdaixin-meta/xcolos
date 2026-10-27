# 17 coder

- time: 2026-10-27T08:56:20+00:00 (137.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 60b3f8272bf1ec3e, reply sha256 c904ebd3b6d22c51

## Sent

````
# Task: write the XColos game file for "Lost Cities: Three Expeditions"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. There are 33 cards in 3 colours: Red (R), Blue (B) and Green (G). Each colour has number cards 2, 3, 4, 5, 6, 7, 8, 9 and 10, written like R7 or B10, plus 2 wager cards, written RW, BW and GW (two of each).

SETUP. Shuffle all 33 cards into a face-down deck. This is the only random event in the game. Deal 6 cards to each player. Each player's hand is a hidden list that only its owner can see; the engine shows it to its owner as part of that player's state.

Table state:
- deck: hidden list, 21 cards remaining after the deal.
- discard_tops: public list of face-up cards, at most one per colour. It starts as an empty list.
- last_discard: hidden bookkeeping value, never shown to players. It starts as 'none'.

Player state, for each player and each colour c in R, B, G:
- sum_c: total of the numbers played in that colour. Starts at 0.
- top_c: highest number played in that colour, 0 meaning no number yet. Starts at 0.
- wag_c: number of wagers played in that colour. Starts at 0.
- cnt_c: number of cards in that colour's expedition, wagers included. Starts at 0.
- score: the player's current score. Starts at 0.
All player state is public except hand.

ROUND. Seat 1 is chosen at random. Each round, seat 1 takes a turn and then seat 2 takes a turn.

A TURN has two choices.

(1) PLAY OR DISCARD. The active player answers with one of:
- 'PLAY X', where X is a card in their hand.
- 'DISCARD X', where X is a card in their hand.

A PLAY is legal if:
- X is a number greater than top_c of its colour; or
- X is a wager and top_c of its colour is still 0.

When a play is legal, remove X from the hand, add 1 to cnt_c, then:
- for a number: add X to sum_c and set top_c to X;
- for a wager: add 1 to wag_c.

An illegal PLAY, or a card not in the hand, is treated as DISCARD of the first card in the hand.

A DISCARD removes X from the hand. If discard_tops already contains a card of X's colour, that old card is removed from the game permanently. Then X is appended to discard_tops, and last_discard is set to X.

(2) DRAW. The active player answers one of:
- 'DECK': take the top card of the deck into the hand.
- The name of a card in discard_tops other than last_discard: move that card from discard_tops into the hand.

An invalid answer, or naming last_discard, means DECK. If the deck is empty, the player must take a card from discard_tops other than last_discard. If none is available, the player draws nothing.

After the draw, last_discard is reset to 'none'. Both players always see discard_tops, both players' expedition numbers, and how many cards remain in the deck.

END OF ROUND. Recompute both scores. For each colour:
- if cnt_c = 0, the colour scores 0;
- otherwise it scores (sum_c - 15) x (1 + wag_c), plus 10 if cnt_c is 5 or more.
A player's score is the total of their three colours.

The game ends at the end of the round in which the deck became empty, or at the end of round 20, whichever comes first. Seat 2 always finishes the round, so both players take the same number of turns.

How the winner is decided: When the game ends, the player with the higher score wins. If the scores are equal, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Lost Cities: Three Expeditions (2 to 2 players, best with 2)

Two explorers build rising number runs in three colours, betting with wager cards and fighting over a shared discard row, while a 21-card deck runs out.

STATE (every item below must exist in the file):
  - each player: hand (list, starts '6 cards dealt from deck'); only its owner sees it. The cards the player holds. Only the owner sees them.
  - each player: sum_r (number, starts 0); everyone sees it. Total of the Red numbers played
  - each player: top_r (number, starts 0); everyone sees it. Highest Red number played. 0 means none yet.
  - each player: wag_r (number, starts 0); everyone sees it. Red wagers played
  - each player: cnt_r (number, starts 0); everyone sees it. Cards in the Red expedition, wagers included
  - each player: sum_b (number, starts 0); everyone sees it. Total of the Blue numbers played
  - each player: top_b (number, starts 0); everyone sees it. Highest Blue number played. 0 means none yet.
  - each player: wag_b (number, starts 0); everyone sees it. Blue wagers played
  - each player: cnt_b (number, starts 0); everyone sees it. Cards in the Blue expedition, wagers included
  - each player: sum_g (number, starts 0); everyone sees it. Total of the Green numbers played
  - each player: top_g (number, starts 0); everyone sees it. Highest Green number played. 0 means none yet.
  - each player: wag_g (number, starts 0); everyone sees it. Green wagers played
  - each player: cnt_g (number, starts 0); everyone sees it. Cards in the Green expedition, wagers included
  - each player: score (number, starts 0); everyone sees it. Current total score over the three colours
  - the table: deck (list, starts 'all 33 cards shuffled, 21 left after the deal'); hidden from all players. The face-down draw deck
  - the table: deck_size (number, starts 21); everyone sees it. Cards remaining in the deck. The rules show this to both players.
  - the table: discard_tops (list, starts []); everyone sees it. Face-up discards, at most one per colour
  - the table: last_discard (text, starts 'none'); hidden from all players. The card discarded this turn. It cannot be drawn back on the same turn.
  - the table: round (number, starts 0); everyone sees it. Rounds completed
  - parameters, each kept as a table attribute: colours = 3, total_cards = 33, lowest_number = 2, highest_number = 10, wagers_per_colour = 2, hand_size = 6, deck_after_deal = 21, expedition_cost = 15, wager_multiplier_base = 1, bonus_card_count = 5, bonus_points = 10, max_rounds = 20, max_discard_tops_per_colour = 1

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Build the 33-card deck: R2-R10, B2-B10, G2-G10, and two each of RW, BW and GW.
  2. Shuffle the deck. This is the only random event in the game.
  3. Choose seat 1 at random.
  4. Deal 6 cards to each player's hand by drawing at random from deck, leaving 21 cards in deck. Set deck_size to 21.
  5. Set discard_tops to an empty list and last_discard to 'none'.
  6. Sync each player their own state.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [sync] all players. What happens: Each player sees their own hand and all public state: the expedition numbers, discard_tops and deck_size.
  2. [ask] seat 1 answers: one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand). What happens: On a legal PLAY of X in colour c: remove X from hand and add 1 to cnt_c. For a number, add X to sum_c and set top_c to X. For a wager, add 1 to wag_c. On DISCARD X: remove X from hand, remove any card of X's colour from discard_tops (it leaves the game), append X to discard_tops and set last_discard to X. An illegal PLAY, or a card not in hand, is treated as DISCARD of the first card in hand.
  3. [ask] seat 1 answers: 'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard. What happens: DECK: draw a random card from deck into hand and subtract 1 from deck_size. A named card: move it from discard_tops to hand. An invalid answer, or naming last_discard, means DECK. If deck is empty and no eligible discard exists, nothing is drawn. Then set last_discard to 'none'.
  4. [update] seat 1. What happens: Announce the card played or discarded, what was drawn (deck or the named discard), and the new deck_size and discard_tops.
  5. [sync] seat 2. What happens: Seat 2 sees their updated state.
  6. [ask] seat 2 answers: one of 'PLAY X' (X a card in hand that is legal to play) or 'DISCARD X' (X any card in hand). What happens: Same as seat 1's play or discard step.
  7. [ask] seat 2 answers: 'DECK' (if deck is not empty) or the name of a card in discard_tops other than last_discard. What happens: Same as seat 1's draw step. Then set last_discard to 'none'.
  8. [update] all players. What happens: For each player and each colour c: if cnt_c = 0 the colour scores 0, otherwise it scores (sum_c - 15) * (1 + wag_c), plus 10 if cnt_c >= 5. Set score to the total of the three colours. Add 1 to round. Announce both scores.
  9. [check] all players. What happens: End the game if deck_size = 0 or round >= 20. Otherwise continue.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, the deck has 33 cards (numbers 2-10 in R, B and G, plus two wagers per colour), each player is dealt 6 cards, and 21 remain in deck.
  R2. When the game starts, seat 1 is chosen at random, and each round seat 1 takes a full turn and then seat 2 does.
  R3. When a player PLAYs a number X of colour c with X > top_c, then X leaves the hand, cnt_c rises by 1, sum_c rises by X and top_c becomes X.
  R4. When a player PLAYs a wager of colour c while top_c = 0, then it leaves the hand, cnt_c rises by 1 and wag_c rises by 1.
  R5. When a player attempts a PLAY of a number X <= top_c, or of a wager while top_c > 0, or of a card not in hand, then it is treated as DISCARD of the first card in hand.
  R6. When a player DISCARDs X, then X leaves the hand, any card of X's colour already in discard_tops is removed from the game, X is appended to discard_tops, and last_discard becomes X.
  R7. When a player draws DECK and the deck is not empty, then one card moves from deck to hand and deck_size falls by 1.
  R8. When a player names a card in discard_tops other than last_discard, then that card moves from discard_tops to hand.
  R9. When a player gives an invalid draw answer or names last_discard, then they draw from DECK.
  R10. When the deck is empty, then the player must take a card from discard_tops other than last_discard, and if none exists they draw nothing.
  R11. When a draw step ends, then last_discard is reset to 'none'.
  R12. When a round ends and a colour has cnt_c = 0, then it scores 0.
  R13. When a round ends and a colour has cnt_c >= 1, then it scores (sum_c - 15) * (1 + wag_c), so one wager with numbers totalling 20 scores 10.
  R14. When a round ends and a colour has cnt_c >= 5, then it scores an extra 10 points.
  R15. When a round ends, then each player's score is the sum of their three colour scores.
  R16. When a round ends with deck_size = 0, then the game ends, and seat 2 always completes the round first.
  R17. When round 20 ends, then the game ends.
  R18. When the game ends, then the higher score wins, and equal scores are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Play or discard | asked: the active seat (seat 1, then seat 2) | options: 'DISCARD X' for every card X in hand. 'PLAY X' for every number X in hand greater than top_c of its colour, and for every wager in hand whose colour has top_c = 0.
  - Draw | asked: the active seat | options: If deck is not empty: 'DECK' plus every card in discard_tops except last_discard. If deck is empty: every card in discard_tops except last_discard. If deck is empty and none exist: 'NOTHING' only.

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: deck_size == 0 or round >= 20 (checked at the end of a round, after seat 2's turn)
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: The player with the higher score wins. If the scores are equal, both share the result, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Current total score over the three colours
- the table: `deck_size` (number, visible: public, starts 21): Cards remaining in the deck. The rules show this to both players.
- the table: `discard_tops` (list, visible: public, starts []): Face-up discards, at most one per colour
- the table: `round` (number, visible: public, starts 0): Rounds completed
- parameters (each must be an attribute holding this value, never a number buried in a step): colours = 3, total_cards = 33, lowest_number = 2, highest_number = 10, wagers_per_colour = 2, hand_size = 6, deck_after_deal = 21, expedition_cost = 15, wager_multiplier_base = 1, bonus_card_count = 5, bonus_points = 10, max_rounds = 20, max_discard_tops_per_colour = 1
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

````

## Reply

````
{
  "schema": 1,
  "meta": {
    "id": "lost_cities_three",
    "name": "Lost Cities: Three Expeditions",
    "players": {
      "min": 2,
      "max": 2,
      "suggested": 2
    },
    "blurb": "Two explorers build rising runs in three colours, bet with wagers and fight over a shared discard row while a 21-card deck runs out."
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
        "key": "hand",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "sum_r",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_r",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wag_r",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cnt_r",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sum_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wag_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cnt_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "sum_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "top_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "wag_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "cnt_g",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "draw_offer",
        "visible": "ally",
        "type": "list",
        "initial": []
      },
      {
        "key": "move",
        "visible": "ally",
        "type": "text",
        "initial": ""
      },
      {
        "key": "drew",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "deck",
        "visible": "none",
        "type": "list",
        "initial": []
      },
      {
        "key": "deck_size",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "discard_tops",
        "visible": "public",
        "type": "list",
        "initial": []
      },
      {
        "key": "last_discard",
        "visible": "none",
        "type": "text",
        "initial": "none"
      },
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pick",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_card",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_kind",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_col",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "act_val",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "draw_src",
        "visible": "none",
        "type": "text",
        "initial": ""
      },
      {
        "key": "colours",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "total_cards",
        "visible": "public",
        "type": "number",
        "initial": 33
      },
      {
        "key": "lowest_number",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "highest_number",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "wagers_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 2
      },
      {
        "key": "hand_size",
        "visible": "public",
        "type": "number",
        "initial": 6
      },
      {
        "key": "deck_after_deal",
        "visible": "public",
        "type": "number",
        "initial": 21
      },
      {
        "key": "expedition_cost",
        "visible": "public",
        "type": "number",
        "initial": 15
      },
      {
        "key": "wager_multiplier_base",
        "visible": "public",
        "type": "number",
        "initial": 1
      },
      {
        "key": "bonus_card_count",
        "visible": "public",
        "type": "number",
        "initial": 5
      },
      {
        "key": "bonus_points",
        "visible": "public",
        "type": "number",
        "initial": 10
      },
      {
        "key": "max_rounds",
        "visible": "public",
        "type": "number",
        "initial": 20
      },
      {
        "key": "max_discard_tops_per_colour",
        "visible": "public",
        "type": "number",
        "initial": 1
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "build and shuffle the deck",
      "do": [
        {
          "set": {
            "key": "deck",
            "value": ["R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "RW", "RW", "BW", "BW", "GW", "GW"]
          }
        }
      ],
      "text": "The {total_cards}-card deck is built and shuffled face down. Seats are assigned at random."
    },
    {
      "use": "update",
      "label": "deal the hands",
      "do": [
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}}},
        {"set": {"key": "deck_size", "value": {"calc": "len(deck)"}}}
      ],
      "text": "Each player is dealt {hand_size} cards. {deck_size} cards remain in the deck."
    },
    {
      "use": "update",
      "label": "clear the discard row",
      "do": [
        {"set": {"key": "discard_tops", "value": []}},
        {"set": {"key": "last_discard", "value": "none"}}
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
      "use": "sync",
      "phase": "start",
      "label": "your state",
      "mode": "self",
      "to": "all",
      "text": "Your state (discard row {discard_tops}, deck {deck_size}):"
    },
    {
      "use": "update",
      "phase": "start",
      "label": "what each seat may play",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "offer",
            "value": {
              "calc": "['PLAY ' + c for c in you.hand if (c[1] == 'W' and (you.top_r if c[0] == 'R' else (you.top_b if c[0] == 'B' else you.top_g)) == 0) or (c[1] != 'W' and (highest_number if len(c) == 3 else int(c[1])) > (you.top_r if c[0] == 'R' else (you.top_b if c[0] == 'B' else you.top_g)))] + ['DISCARD ' + c for c in you.hand]"
            }
          }
        },
        {"set": {"players": "all", "key": "move", "value": ""}}
      ]
    },
    {
      "use": "ask",
      "phase": "seat 1",
      "label": "seat 1 plays or discards",
      "to": {"where": "you.seat == 1"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "offer"}
      },
      "store": "move",
      "text": "Your turn. Choose PLAY X to add a card to its expedition (a number must be higher than your top number in that colour; a wager only before any number in that colour), or DISCARD X to put it face up on the discard row, replacing any card of its colour there."
    },
    {
      "use": "update",
      "phase": "seat 1",
      "label": "seat 1's card",
      "do": [
        {"set": {"key": "act_card", "value": {"calc": "([c for c in players[0].hand if players[0].move in ['PLAY ' + c, 'DISCARD ' + c]] + players[0].hand)[0]"}}},
        {"set": {"key": "act_kind", "value": {"calc": "'PLAY' if (players[0].move == 'PLAY ' + act_card and players[0].move in players[0].offer) else 'DISCARD'"}}},
        {"set": {"key": "act_col", "value": {"calc": "act_card[0]"}}},
        {"set": {"key": "act_val", "value": {"calc": "highest_number if len(act_card) == 3 else (0 if act_card[1] == 'W' else int(act_card[1]))"}}},
        {"remove": {"player": 1, "key": "hand", "value": {"calc": "act_card"}}},
        {"adjust": {"player": 1, "key": "cnt_r", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R'"}}},
        {"adjust": {"player": 1, "key": "sum_r", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val > 0"}}},
        {"set": {"player": 1, "key": "top_r", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val > 0"}}},
        {"adjust": {"player": 1, "key": "wag_r", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val == 0"}}},
        {"adjust": {"player": 1, "key": "cnt_b", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B'"}}},
        {"adjust": {"player": 1, "key": "sum_b", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val > 0"}}},
        {"set": {"player": 1, "key": "top_b", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val > 0"}}},
        {"adjust": {"player": 1, "key": "wag_b", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val == 0"}}},
        {"adjust": {"player": 1, "key": "cnt_g", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G'"}}},
        {"adjust": {"player": 1, "key": "sum_g", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val > 0"}}},
        {"set": {"player": 1, "key": "top_g", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val > 0"}}},
        {"adjust": {"player": 1, "key": "wag_g", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val == 0"}}},
        {"remove": {"key": "discard_tops", "value": {"calc": "([c for c in discard_tops if c[0] == act_col] + ['none'])[0]"}, "if": {"calc": "act_kind == 'DISCARD' and any(c[0] == act_col for c in discard_tops)"}}},
        {"append": {"key": "discard_tops", "value": {"calc": "act_card"}, "if": {"calc": "act_kind == 'DISCARD'"}}},
        {"set": {"key": "last_discard", "value": {"calc": "act_card"}, "if": {"calc": "act_kind == 'DISCARD'"}}},
        {"set": {"player": 1, "key": "draw_offer", "value": {"calc": "(['DECK'] if deck_size > 0 else []) + [c for c in discard_tops if c != last_discard]"}}},
        {"set": {"players": "all", "key": "drew", "value": ""}}
      ],
      "text": "Seat 1: {act_kind} {act_card}. Discard row: {discard_tops}."
    },
    {
      "use": "ask",
      "phase": "seat 1",
      "label": "seat 1 draws",
      "to": {"where": "you.seat == 1"},
      "when": {"calc": "len(players[0].draw_offer) > 1"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "draw_offer"}
      },
      "store": "drew",
      "text": "Draw a card: DECK for the top card of the deck, or name a card on the discard row to take it (not the card you just discarded)."
    },
    {
      "use": "update",
      "phase": "seat 1",
      "label": "seat 1's draw",
      "do": [
        {"set": {"key": "draw_src", "value": {"calc": "players[0].drew if players[0].drew in [c for c in discard_tops if c != last_discard] else ('DECK' if deck_size > 0 else ([c for c in discard_tops if c != last_discard] + ['NOTHING'])[0])"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"append": {"player": 1, "key": "hand", "value": {"calc": "draw_src"}, "if": {"calc": "draw_src not in ['DECK', 'NOTHING']"}}},
        {"remove": {"key": "discard_tops", "value": {"calc": "draw_src"}, "if": {"calc": "draw_src not in ['DECK', 'NOTHING']"}}},
        {"set": {"key": "deck_size", "value": {"calc": "len(deck)"}}},
        {"set": {"key": "last_discard", "value": "none"}}
      ],
      "text": "Seat 1 draws: {draw_src} (DECK means a hidden card from the deck). Deck: {deck_size} cards. Discard row: {discard_tops}."
    },
    {
      "use": "sync",
      "phase": "seat 2",
      "label": "seat 2's state",
      "mode": "self",
      "to": {"where": "you.seat == 2"},
      "text": "Your state (discard row {discard_tops}, deck {deck_size}):"
    },
    {
      "use": "ask",
      "phase": "seat 2",
      "label": "seat 2 plays or discards",
      "to": {"where": "you.seat == 2"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "offer"}
      },
      "store": "move",
      "text": "Your turn. Choose PLAY X to add a card to its expedition (a number must be higher than your top number in that colour; a wager only before any number in that colour), or DISCARD X to put it face up on the discard row, replacing any card of its colour there."
    },
    {
      "use": "update",
      "phase": "seat 2",
      "label": "seat 2's card",
      "do": [
        {"set": {"key": "act_card", "value": {"calc": "([c for c in players[1].hand if players[1].move in ['PLAY ' + c, 'DISCARD ' + c]] + players[1].hand)[0]"}}},
        {"set": {"key": "act_kind", "value": {"calc": "'PLAY' if (players[1].move == 'PLAY ' + act_card and players[1].move in players[1].offer) else 'DISCARD'"}}},
        {"set": {"key": "act_col", "value": {"calc": "act_card[0]"}}},
        {"set": {"key": "act_val", "value": {"calc": "highest_number if len(act_card) == 3 else (0 if act_card[1] == 'W' else int(act_card[1]))"}}},
        {"remove": {"player": 2, "key": "hand", "value": {"calc": "act_card"}}},
        {"adjust": {"player": 2, "key": "cnt_r", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R'"}}},
        {"adjust": {"player": 2, "key": "sum_r", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val > 0"}}},
        {"set": {"player": 2, "key": "top_r", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val > 0"}}},
        {"adjust": {"player": 2, "key": "wag_r", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'R' and act_val == 0"}}},
        {"adjust": {"player": 2, "key": "cnt_b", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B'"}}},
        {"adjust": {"player": 2, "key": "sum_b", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val > 0"}}},
        {"set": {"player": 2, "key": "top_b", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val > 0"}}},
        {"adjust": {"player": 2, "key": "wag_b", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'B' and act_val == 0"}}},
        {"adjust": {"player": 2, "key": "cnt_g", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G'"}}},
        {"adjust": {"player": 2, "key": "sum_g", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val > 0"}}},
        {"set": {"player": 2, "key": "top_g", "value": {"calc": "act_val"}, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val > 0"}}},
        {"adjust": {"player": 2, "key": "wag_g", "value": 1, "if": {"calc": "act_kind == 'PLAY' and act_col == 'G' and act_val == 0"}}},
        {"remove": {"key": "discard_tops", "value": {"calc": "([c for c in discard_tops if c[0] == act_col] + ['none'])[0]"}, "if": {"calc": "act_kind == 'DISCARD' and any(c[0] == act_col for c in discard_tops)"}}},
        {"append": {"key": "discard_tops", "value": {"calc": "act_card"}, "if": {"calc": "act_kind == 'DISCARD'"}}},
        {"set": {"key": "last_discard", "value": {"calc": "act_card"}, "if": {"calc": "act_kind == 'DISCARD'"}}},
        {"set": {"player": 2, "key": "draw_offer", "value": {"calc": "(['DECK'] if deck_size > 0 else []) + [c for c in discard_tops if c != last_discard]"}}},
        {"set": {"players": "all", "key": "drew", "value": ""}}
      ],
      "text": "Seat 2: {act_kind} {act_card}. Discard row: {discard_tops}."
    },
    {
      "use": "ask",
      "phase": "seat 2",
      "label": "seat 2 draws",
      "to": {"where": "you.seat == 2"},
      "when": {"calc": "len(players[1].draw_offer) > 1"},
      "answer": {
        "type": "choice",
        "options": {"attribute": "draw_offer"}
      },
      "store": "drew",
      "text": "Draw a card: DECK for the top card of the deck, or name a card on the discard row to take it (not the card you just discarded)."
    },
    {
      "use": "update",
      "phase": "seat 2",
      "label": "seat 2's draw",
      "do": [
        {"set": {"key": "draw_src", "value": {"calc": "players[1].drew if players[1].drew in [c for c in discard_tops if c != last_discard] else ('DECK' if deck_size > 0 else ([c for c in discard_tops if c != last_discard] + ['NOTHING'])[0])"}}},
        {"set": {"key": "pick", "value": {"calc": "deck[int(uniform(0, len(deck)))]"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "pick"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"remove": {"key": "deck", "value": {"calc": "pick"}, "if": {"calc": "draw_src == 'DECK'"}}},
        {"append": {"player": 2, "key": "hand", "value": {"calc": "draw_src"}, "if": {"calc": "draw_src not in ['DECK', 'NOTHING']"}}},
        {"remove": {"key": "discard_tops", "value": {"calc": "draw_src"}, "if": {"calc": "draw_src not in ['DECK', 'NOTHING']"}}},
        {"set": {"key": "deck_size", "value": {"calc": "len(deck)"}}},
        {"set": {"key": "last_discard", "value": "none"}}
      ],
      "text": "Seat 2 draws: {draw_src} (DECK means a hidden card from the deck). Deck: {deck_size} cards. Discard row: {discard_tops}."
    },
    {
      "use": "update",
      "phase": "end of round",
      "label": "score the round",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "(0 if you.cnt_r == 0 else (you.sum_r - expedition_cost) * (wager_multiplier_base + you.wag_r) + (bonus_points if you.cnt_r >= bonus_card_count else 0)) + (0 if you.cnt_b == 0 else (you.sum_b - expedition_cost) * (wager_multiplier_base + you.wag_b) + (bonus_points if you.cnt_b >= bonus_card_count else 0)) + (0 if you.cnt_g == 0 else (you.sum_g - expedition_cost) * (wager_multiplier_base + you.wag_g) + (bonus_points if you.cnt_g >= bonus_card_count else 0))"
            }
          }
        },
        {"adjust": {"key": "round", "value": 1}}
      ],
      "text": "Round {round} is over. Scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}. Deck: {deck_size} cards."
    },
    {
      "use": "check",
      "phase": "end of round",
      "label": "deck empty or last round",
      "when": {"calc": "deck_size == 0 or round >= max_rounds"},
      "against": ["over"]
    }
  ],
  "end": {
    "over": {
      "when": {"calc": "deck_size == 0 or round >= max_rounds"},
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}."
    }
  },
  "limits": {
    "rounds": 20,
    "rounds_max": 20,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "CARDS. There are {total_cards} cards in {colours} colours: Red (R), Blue (B) and Green (G). Each colour has number cards {lowest_number} to {highest_number}, written like R7 or B10, plus {wagers_per_colour} wager cards, written RW, BW and GW.\n\nSETUP. All cards are shuffled into a face-down deck; this is the only random event. Seat 1 is chosen at random. Each player is dealt {hand_size} cards, leaving {deck_after_deal} in the deck. Your hand is hidden from your opponent. The discard row (discard_tops) starts empty and holds at most {max_discard_tops_per_colour} face-up card per colour.\n\nROUND. Each round seat 1 takes a full turn, then seat 2 takes a full turn.\n\nA TURN has two choices.\n(1) PLAY OR DISCARD. Answer 'PLAY X' or 'DISCARD X', X being a card in your hand. A PLAY is legal if X is a number greater than your highest number played in its colour, or X is a wager and you have played no number in its colour yet. On a legal play, X leaves your hand and joins that colour's expedition (card count +1); a number adds its value to the colour's total and becomes its top number, a wager adds one wager to that colour. You are offered only legal plays; an illegal PLAY, or a card not in your hand, is treated as DISCARD of the first card in your hand. A DISCARD removes X from your hand; if the discard row already holds a card of X's colour, that old card leaves the game permanently; X is then placed face up on the discard row, and it becomes the card discarded this turn.\n(2) DRAW. Answer 'DECK' to take the top card of the deck, or name a card on the discard row other than the card discarded this turn to take it into your hand. An invalid answer, or naming the card discarded this turn, means DECK. If the deck is empty you must take a card from the discard row other than the card discarded this turn; if there is none, you draw nothing. When your only possible draw is DECK you are not asked. After the draw the card discarded this turn is forgotten and may be drawn by anyone later. Both players always see the discard row, both players' expeditions and the deck size ({deck_size} at the start).\n\nEND OF ROUND. Both scores are recomputed. For each colour: a colour with no cards scores 0; otherwise it scores (total of numbers - {expedition_cost}) x ({wager_multiplier_base} + wagers), plus {bonus_points} if the expedition has {bonus_card_count} or more cards. Your score is the total of your three colours. Example: one wager with numbers totalling 20 scores 10.\n\nThe game ends at the end of the round in which the deck became empty, or at the end of round {max_rounds}, whichever comes first. Seat 2 always finishes the round, so both players take the same number of turns. The higher score wins; equal scores share the result, which is a draw."
}
````
