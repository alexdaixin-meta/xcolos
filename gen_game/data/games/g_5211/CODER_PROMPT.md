# Task: write the XColos game file for "5211: Mirror Hands"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 4} (the suggested size is the one the game plays best at).

SETUP. Let n be the number of players (3 or 4). Every player receives an identical hand of 14 cards:
- the colours Red, Blue, Green and Yellow, each with values 1, 2 and 3 (12 cards);
- 2 Kododo cards, which have no colour and are worth 3 each.
Hands are private, but because every hand starts identical and all played cards are revealed, anyone can track what each player has left. Each player is then secretly dealt a bonus colour at random from Red, Blue, Green and Yellow, with no two players sharing one. Only that player knows it. Scores start at 0, and each player's scored-card count starts at 0.

EACH ROUND (7 rounds):
1. Talk. Every player writes one short message at the same time, without seeing the others. All messages are then shown to everyone. Nothing said is binding.
2. First card. Every player at the same time places one card from their hand face down.
3. Reveal. All first cards are revealed.
4. Second card. Every player at the same time places one more card from their hand face down.
5. Reveal. All second cards are revealed. Played cards leave the hands.
6. Count. Count K, the number of Kododos played this round (out of 2n cards). Count how many cards of each colour were played.
7. Kododo check. If K equals exactly n-1 (2 Kododos with 3 players, 3 with 4 players), each player scores 3 points per Kododo they played this round and adds that many cards to their scored-card count. No colour scores this round.
8. Colour check (only if K is not exactly n-1). A colour is busted if its count is n+1 or more (4 or more with 3 players, 5 or more with 4 players). Among the colours that are not busted and have a count of at least 1, find the highest count. If exactly one colour has that highest count, it is the scoring colour. If two or more colours share it, or no colour qualifies, nothing scores this round.
   Each player scores the face values of their cards of the scoring colour, plus 1 extra point per such card if it is their bonus colour, and adds those cards to their scored-card count.
   Kododos played in a round where the Kododo check fails score nothing.
9. Announce the round result and the updated scores.

END. After round 7, all 14 cards have been played and the game ends.

How the winner is decided: The player with the highest total score wins. If players are tied on total score, the one among them with the higher scored-card count wins. If they are still tied, the game is a draw among the tied players.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: 5211: Mirror Hands (3 to 4 players, best with 4)

Each player holds the same 14 cards. Over 7 rounds everyone plays two cards at once, and either the Kododos score (when exactly n-1 are played) or the single most-played colour that did not bust scores.

STATE (every item below must exist in the file):
  - each player: hand (list, starts ['R1', 'R2', 'R3', 'B1', 'B2', 'B3', 'G1', 'G2', 'G3', 'Y1', 'Y2', 'Y3', 'K', 'K']); only its owner sees it. cards still held; R/B/G/Y = Red/Blue/Green/Yellow with face value, K = Kododo
  - each player: bonus_colour (text, starts ''); only its owner sees it. secret bonus colour (Red, Blue, Green or Yellow), unique per player
  - each player: first_card (text, starts ''); everyone sees it. card played first this round (revealed after all have placed)
  - each player: second_card (text, starts ''); everyone sees it. card played second this round (revealed after all have placed)
  - each player: round_points (number, starts 0); everyone sees it. points scored by this player this round
  - each player: score (number, starts 0); everyone sees it. total score
  - each player: scored_cards (number, starts 0); everyone sees it. number of this player's cards that have scored (tie-break)
  - the table: bonus_pool (list, starts ['Red', 'Blue', 'Green', 'Yellow']); hidden from all players. bonus colours not yet dealt
  - the table: round (number, starts 0); everyone sees it. rounds completed
  - the table: kododo_count (number, starts 0); everyone sees it. K: Kododos played this round
  - the table: red_count (number, starts 0); everyone sees it. Red cards played this round
  - the table: blue_count (number, starts 0); everyone sees it. Blue cards played this round
  - the table: green_count (number, starts 0); everyone sees it. Green cards played this round
  - the table: yellow_count (number, starts 0); everyone sees it. Yellow cards played this round
  - the table: scoring_colour (text, starts 'none'); everyone sees it. what scored this round: Red, Blue, Green, Yellow, Kododo or none
  - parameters, each kept as a table attribute: rounds = 7, hand_size = 14, colours = 4, min_card_value = 1, max_card_value = 3, kododos_per_hand = 2, kododo_value = 3, cards_per_round = 2, bonus_extra_per_card = 1, kododo_target_offset = -1, bust_offset = 1, score_weight_in_ranking = 100

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Let n be the number of seated players (3 or 4).
  2. Every player's hand is set to the same 14 cards: R1, R2, R3, B1, B2, B3, G1, G2, G3, Y1, Y2, Y3, K, K.
  3. For each player in seat order, one colour is drawn at random from bonus_pool, written to that player's bonus_colour (visible only to them) and removed from bonus_pool, so no two players share one.
  4. score and scored_cards start at 0 for every player, and round starts at 0.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [poll] all players answers: a short text message. What happens: All messages are broadcast to everyone at once ({"to": "all", "text": "Seat {seat} says: {value}"}). Nothing is binding and no state changes.
  2. [poll] all players answers: one card from your own hand. What happens: Set first_card to the chosen card and remove one copy of it from hand. Nobody sees a choice until all are in.
  3. [tell] all players. What happens: Reveal every player's first_card to everyone.
  4. [poll] all players answers: one card from your remaining hand. What happens: Set second_card to the chosen card and remove one copy of it from hand. Nobody sees a choice until all are in.
  5. [tell] all players. What happens: Reveal every player's second_card to everyone.
  6. [update] all players. What happens: Set round_points = 0 for each player. Set kododo_count = the number of K among all first_card and second_card values. Set red_count, blue_count, green_count and yellow_count = the number of played cards starting with R, B, G and Y respectively.
  7. [update] all players. What happens: When kododo_count == n - 1: set scoring_colour = 'Kododo'; each player adds 3 x (their K cards this round) to round_points and score, and (their K cards this round) to scored_cards.
  8. [update] all players. What happens: When kododo_count != n - 1: a colour is eligible if 1 <= its count <= n. If exactly one eligible colour has the highest count among eligible colours, scoring_colour = that colour; otherwise scoring_colour = 'none'. If scoring_colour is a colour, each player sums the face values of their played cards of that colour, plus 1 per such card if bonus_colour == scoring_colour. They add that sum to round_points and score, and add the number of such cards to scored_cards. Kododos score nothing.
  9. [tell] all players. What happens: Announce scoring_colour, the colour counts, kododo_count, each player's round_points, score and scored_cards.
  10. [update] all players. What happens: round += 1.
  11. [check] all players. What happens: End the game if round >= 7, otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, every player's hand holds exactly the 14 cards R1, R2, R3, B1, B2, B3, G1, G2, G3, Y1, Y2, Y3, K, K.
  R2. At setup, each player gets a different bonus colour from Red, Blue, Green and Yellow, visible only to that player.
  R3. At setup, every player's score and scored_cards are 0.
  R4. Each round, every player sends one short message at the same time, and all messages are shown to everyone.
  R5. Each round, every player plays a first card from their hand at the same time; the cards are revealed only after all are chosen, and each leaves the hand.
  R6. Each round, every player then plays a second card from their remaining hand at the same time; the cards are revealed only after all are chosen, and each leaves the hand.
  R7. When exactly n-1 Kododos are played in a round (2 with 3 players, 3 with 4 players), each player scores 3 points and 1 scored card per Kododo they played, and no colour scores.
  R8. When 4 players play 3 Kododos in a round and one player played 2 of them, that player gains 6 points and 2 scored cards.
  R9. When the Kododo count is not exactly n-1, the Kododos played that round score nothing.
  R10. A colour played n+1 or more times in a round (4+ with 3 players, 5+ with 4 players) is busted and cannot score.
  R11. When the Kododo check fails and exactly one non-busted colour has the highest count (at least 1), that colour scores: each player gains the face values of their cards of that colour and 1 scored card per such card.
  R12. When a player's scoring-colour cards match their bonus colour, they gain 1 extra point per such card (for example, playing R3 and R2 with bonus Red while Red scores gives 7 points).
  R13. When two or more non-busted colours tie for the highest count, or no colour is eligible, nothing scores that round.
  R14. After round 7, all 14 cards have been played and the game ends.
  R15. The highest score wins; a tie on score is broken by the higher scored_cards; players still tied share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all players | options: any short text
  - First card | asked: all players | options: each distinct card currently in that player's own hand (K offered while at least one K remains)
  - Second card | asked: all players | options: each distinct card remaining in that player's own hand after the first card was removed

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 7
  - each player's standing: you.score * 100 + you.scored_cards (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Highest total score wins. Among players tied on score, the higher scored_cards count wins. Players still tied share the win, which is the draw.
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

- each player: `score` (number, visible: public, starts 0): total score
- each player: `scored_cards` (number, visible: public, starts 0): number of this player's cards that have scored (tie-break)
- the table: `round` (number, visible: public, starts 0): rounds completed
- the table: `scoring_colour` (text, visible: public, starts 'none'): what scored this round: Red, Blue, Green, Yellow, Kododo or none
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 7, hand_size = 14, colours = 4, min_card_value = 1, max_card_value = 3, kododos_per_hand = 2, kododo_value = 3, cards_per_round = 2, bonus_extra_per_card = 1, kododo_target_offset = -1, bust_offset = 1, score_weight_in_ranking = 100
- the game ends with ONE ending whose `rank_by` is `you.score * 100 + you.scored_cards`: worked out for every player (`you` is that player), the highest wins and players level at the top share the win
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
