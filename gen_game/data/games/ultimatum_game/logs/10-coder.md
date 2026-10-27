# 10 coder

- time: 2026-10-27T21:43:19+00:00 (50.2s)  model: claude-opus-5-5
- system prompt: [system/16a5676c-coder.md](system/16a5676c-coder.md) (sha256 16a5676c082f6d22)
- sent sha256 0ca3b176cce86603, reply sha256 682a0065d769a642

## Sent

````
# Task: write the XColos game file for "Hidden Pie Ultimatum III"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 3; set `meta.players` to {"min": 3, "max": 3, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: Three players, P1, P2 and P3, each start with a score of 0. Each player has a pot list (a game list, not a player attribute) holding the four values 70, 90, 110 and 130. Everyone knows the contents of every list.

ROUNDS: There are 12 proposal rounds. The Proposer by round is:
- rounds 1-3: P1, P2, P3
- rounds 4-6: P3, P2, P1
- rounds 7-9: P1, P2, P3
- rounds 10-12: P3, P2, P1
Each player proposes exactly 4 times. The other two players are that round's Responders; the first Responder is the one with the lower seat number.

EACH ROUND:
1. Draw: one value is drawn at random from the Proposer's remaining pot list and removed from it. This is the pot. Only the Proposer is told it. Because each list loses one value per proposal, every player plays all four values exactly once.
2. Talk: every player writes one short message at the same time, without seeing the others. Then all three messages are shown to everyone. Messages are not binding and may be false.
3. Offer: the Proposer announces two whole numbers: a for the first Responder and b for the second. Each must be 0 or more, and a + b must be at most 130. The offer is shown to everyone; the pot is not.
4. Response: both Responders choose Accept or Reject at the same time, without seeing each other's choice.
5. Scoring:
   - If at least one Responder accepts, the deal passes. The Proposer gains pot - a - b; if a + b exceeds the pot, this is negative and the Proposer loses points. Each Responder who accepted gains their offered amount. A Responder who rejected gains 0, and their share is destroyed (the Proposer still pays it).
   - If both Responders reject, the deal fails and all three gain 0 this round.
6. Reveal: the pot, both responses and all three scores are announced.

END: The game ends after round 12.

How the winner is decided: After round 12, the player with the strictly highest total score wins. If two or three players tie for the highest total, the game is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Hidden Pie Ultimatum III (3 to 3 players, best with 3)

Three players take turns as Proposer over 12 rounds. Each Proposer splits a pot that only they can see between two Responders, and the deal passes if at least one Responder accepts.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points gained so far.
  - the table: round (number, starts 0); everyone sees it. Current round number, 1 to 12.
  - the table: proposer (number, starts 0); everyone sees it. Seat of this round's Proposer.
  - the table: responder1 (number, starts 0); everyone sees it. First Responder this round, the lower-numbered seat of the two non-Proposers.
  - the table: responder2 (number, starts 0); everyone sees it. Second Responder this round, the higher-numbered seat of the two non-Proposers.
  - the table: pots_p1 (list, starts [70, 90, 110, 130]); hidden from all players. Pot values P1 has not yet played as Proposer.
  - the table: pots_p2 (list, starts [70, 90, 110, 130]); hidden from all players. Pot values P2 has not yet played as Proposer.
  - the table: pots_p3 (list, starts [70, 90, 110, 130]); hidden from all players. Pot values P3 has not yet played as Proposer.
  - the table: pot (number, starts 0); hidden from all players. This round's pot. Only the Proposer is told it before the reveal.
  - the table: offer_a (number, starts 0); everyone sees it. Amount offered to the first Responder.
  - the table: offer_b (number, starts 0); everyone sees it. Amount offered to the second Responder.
  - the table: response1 (text, starts ''); everyone sees it. First Responder's choice, Accept or Reject, shown at the reveal.
  - the table: response2 (text, starts ''); everyone sees it. Second Responder's choice, Accept or Reject, shown at the reveal.
  - parameters, each kept as a table attribute: rounds = 12, player_count = 3, pot_value_1 = 70, pot_value_2 = 90, pot_value_3 = 110, pot_value_4 = 130, max_offer_total = 130, min_offer = 0, proposals_per_player = 4, initial_score = 0, rounds_per_block = 3

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Seats 1, 2 and 3 are P1, P2 and P3, and each starts with score 0.
  2. The table lists pots_p1, pots_p2 and pots_p3 each hold the values 70, 90, 110 and 130.
  3. Everyone is told that each player's pot list starts as 70, 90, 110 and 130, and that each value is used exactly once when that player proposes.
  4. Everyone is told the Proposer order: rounds 1-3 are P1, P2, P3; rounds 4-6 are P3, P2, P1; rounds 7-9 are P1, P2, P3; rounds 10-12 are P3, P2, P1.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round += 1. Let k = (round-1) div 3 and j = (round-1) mod 3. proposer = j+1 if k is even, otherwise 3-j. responder1 = 2 if proposer == 1, else 1. responder2 = 2 if proposer == 3, else 3. Announce the round, the proposer, responder1 and responder2.
  2. [update] seat proposer. What happens: Draw: pick one value at random from pots_p{proposer}, set pot to it, and remove it from pots_p{proposer}.
  3. [tell] seat proposer. What happens: Privately tell the Proposer: 'This round's pot is {pot}.'
  4. [poll] all players answers: short text message. What happens: All messages are collected at the same time, then broadcast to all as 'Seat {seat} says: {value}'. Messages are not binding.
  5. [ask] seat proposer answers: whole number from 0 to 130. What happens: offer_a = answer (the amount for responder1).
  6. [ask] seat proposer answers: whole number from 0 to 130 - offer_a. What happens: offer_b = answer (the amount for responder2), so that offer_a + offer_b <= 130.
  7. [tell] all players. What happens: Announce: 'Seat {proposer} offers {offer_a} to Seat {responder1} and {offer_b} to Seat {responder2}.' The pot is not shown.
  8. [poll] seat responder1 and seat responder2 answers: Accept or Reject. What happens: response1 = responder1's choice and response2 = responder2's choice. Neither Responder sees the other's choice before answering.
  9. [update] all players. What happens: If response1 == Accept or response2 == Accept: the Proposer's score += pot - offer_a - offer_b (this may be negative); if response1 == Accept, responder1's score += offer_a; if response2 == Accept, responder2's score += offer_b. If both are Reject, no score changes.
  10. [tell] all players. What happens: Reveal: 'The pot was {pot}. Seat {responder1}: {response1}. Seat {responder2}: {response2}. Scores: P1 {score of seat 1}, P2 {score of seat 2}, P3 {score of seat 3}.'
  11. [check] all players. What happens: End the game if round >= 12; otherwise continue to the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When the game starts, then every player's score is 0 and each of pots_p1, pots_p2 and pots_p3 holds 70, 90, 110 and 130.
  R2. When the round is 1, 2 or 3, then the proposer is seat 1, 2 or 3 respectively.
  R3. When the round is 4, 5 or 6, then the proposer is seat 3, 2 or 1 respectively.
  R4. When the round is 7, 8 or 9, then the proposer is seat 1, 2 or 3 respectively.
  R5. When the round is 10, 11 or 12, then the proposer is seat 3, 2 or 1 respectively.
  R6. When the proposer is seat 1, then responder1 is seat 2 and responder2 is seat 3; when the proposer is seat 2, then they are seats 1 and 3; when the proposer is seat 3, then they are seats 1 and 2.
  R7. When a round begins, then one value is drawn at random from the proposer's pot list, set as pot, and removed from that list, so the list shrinks by 1.
  R8. When the game ends after 12 rounds, then every player has proposed exactly 4 times, has used each of 70, 90, 110 and 130 once, and has an empty pot list.
  R9. When the pot is drawn, then only the proposer is told its value before the reveal.
  R10. When the talk step runs, then every player submits one message at the same time and all three messages are shown to everyone afterwards.
  R11. When the proposer makes an offer, then offer_a and offer_b are whole numbers with offer_a >= 0, offer_b >= 0 and offer_a + offer_b <= 130.
  R12. When the offer is made, then offer_a and offer_b are shown to everyone and the pot is not.
  R13. When the Responders respond, then each chooses Accept or Reject at the same time without seeing the other's choice.
  R14. When both Responders accept, then the proposer gains pot - offer_a - offer_b, responder1 gains offer_a and responder2 gains offer_b (pot 110, offers 30 and 40: proposer +40, responders +30 and +40).
  R15. When exactly one Responder accepts, then the proposer gains pot - offer_a - offer_b, the accepting Responder gains their offer, and the rejecting Responder gains 0 (pot 90, offers 30 and 40, only responder1 accepts: proposer +20, responder1 +30, responder2 +0).
  R16. When the deal passes and offer_a + offer_b exceeds the pot, then the proposer's score goes down by the difference (pot 70, offers 50 and 50: proposer -30).
  R17. When both Responders reject, then all three players gain 0 this round.
  R18. When a round's scoring is done, then the pot, both responses and all three scores are announced to everyone.
  R19. When round 12's scoring is done, then the game ends.
  R20. When the game ends, then the player with the highest score wins, and players tied for the highest score share the result.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: all three seats | options: any short text message
  - Offer for the first Responder (offer_a) | asked: the proposer only | options: a whole number from 0 to 130
  - Offer for the second Responder (offer_b) | asked: the proposer only | options: a whole number from 0 to 130 - offer_a
  - Response to the offer | asked: responder1 and responder2 only (the proposer is not asked) | options: Accept, Reject

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round >= 12
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their total score after round 12. The highest total wins. Players tied at the top share the result, which stands in for the source's draw.
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

- each player: `score` (number, visible: public, starts 0): Total points gained so far.
- the table: `round` (number, visible: public, starts 0): Current round number, 1 to 12.
- the table: `proposer` (number, visible: public, starts 0): Seat of this round's Proposer.
- the table: `offer_a` (number, visible: public, starts 0): Amount offered to the first Responder.
- the table: `offer_b` (number, visible: public, starts 0): Amount offered to the second Responder.
- the table: `response1` (text, visible: public, starts ''): First Responder's choice, Accept or Reject, shown at the reveal.
- the table: `response2` (text, visible: public, starts ''): Second Responder's choice, Accept or Reject, shown at the reveal.
- parameters (each must be an attribute holding this value, never a number buried in a step): rounds = 12, player_count = 3, pot_value_1 = 70, pot_value_2 = 90, pot_value_3 = 110, pot_value_4 = 130, max_offer_total = 130, min_offer = 0, proposals_per_player = 4, initial_score = 0, rounds_per_block = 3
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
```json
{
  "schema": 1,
  "meta": {
    "id": "hidden_pie_ultimatum_iii",
    "name": "Hidden Pie Ultimatum III",
    "players": {
      "min": 3,
      "max": 3,
      "suggested": 3
    },
    "blurb": "Three players take turns splitting a pot only the Proposer can see between two Responders; the deal passes if at least one accepts."
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
      },
      {
        "key": "resp",
        "visible": "ally",
        "type": "text",
        "initial": ""
      }
    ],
    "game": [
      {
        "key": "round",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "proposer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "responder1",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "responder2",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "pots_p1",
        "visible": "none",
        "type": "list",
        "initial": [70, 90, 110, 130]
      },
      {
        "key": "pots_p2",
        "visible": "none",
        "type": "list",
        "initial": [70, 90, 110, 130]
      },
      {
        "key": "pots_p3",
        "visible": "none",
        "type": "list",
        "initial": [70, 90, 110, 130]
      },
      {
        "key": "pot",
        "visible": "none",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_a",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "offer_b",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "response1",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "response2",
        "visible": "public",
        "type": "text",
        "initial": ""
      },
      {
        "key": "rounds",
        "visible": "public",
        "type": "number",
        "initial": 12
      },
      {
        "key": "player_count",
        "visible": "public",
        "type": "number",
        "initial": 3
      },
      {
        "key": "pot_value_1",
        "visible": "public",
        "type": "number",
        "initial": 70
      },
      {
        "key": "pot_value_2",
        "visible": "public",
        "type": "number",
        "initial": 90
      },
      {
        "key": "pot_value_3",
        "visible": "public",
        "type": "number",
        "initial": 110
      },
      {
        "key": "pot_value_4",
        "visible": "public",
        "type": "number",
        "initial": 130
      },
      {
        "key": "max_offer_total",
        "visible": "public",
        "type": "number",
        "initial": 130
      },
      {
        "key": "min_offer",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "proposals_per_player",
        "visible": "public",
        "type": "number",
        "initial": 4
      },
      {
        "key": "initial_score",
        "visible": "public",
        "type": "number",
        "initial": 0
      },
      {
        "key": "rounds_per_block",
        "visible": "public",
        "type": "number",
        "initial": 3
      }
    ]
  },
  "setup": [
    {
      "use": "update",
      "label": "the starting scores",
      "do": [
        {
          "set": {
            "players": "all",
            "key": "score",
            "value": {
              "calc": "initial_score"
            }
          }
        }
      ]
    },
    {
      "use": "update",
      "label": "the pot lists",
      "do": [
        {
          "set": {
            "key": "pots_p1",
            "value": {
              "calc": "[pot_value_1, pot_value_2, pot_value_3, pot_value_4]"
            }
          }
        },
        {
          "set": {
            "key": "pots_p2",
            "value": {
              "calc": "[pot_value_1, pot_value_2, pot_value_3, pot_value_4]"
            }
          }
        },
        {
          "set": {
            "key": "pots_p3",
            "value": {
              "calc": "[pot_value_1, pot_value_2, pot_value_3, pot_value_4]"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "label": "the pot lists explained",
      "to": "all",
      "text": "Each player's pot list starts as {pot_value_1}, {pot_value_2}, {pot_value_3} and {pot_value_4}. Each value is used exactly once when that player proposes."
    },
    {
      "use": "tell",
      "label": "the proposer order",
      "to": "all",
      "text": "Proposer order: rounds 1-3 are P1, P2, P3; rounds 4-6 are P3, P2, P1; rounds 7-9 are P1, P2, P3; rounds 10-12 are P3, P2, P1."
    }
  ],
  "steps": [
    {
      "use": "update",
      "phase": "start",
      "label": "the new round",
      "do": [
        {
          "adjust": {
            "key": "round",
            "value": 1
          }
        },
        {
          "set": {
            "key": "proposer",
            "value": {
              "calc": "((round - 1) - rounds_per_block * int((round - 1) / rounds_per_block)) + 1 if (int((round - 1) / rounds_per_block) - 2 * int(int((round - 1) / rounds_per_block) / 2)) == 0 else rounds_per_block - ((round - 1) - rounds_per_block * int((round - 1) / rounds_per_block))"
            }
          }
        },
        {
          "set": {
            "key": "responder1",
            "value": {
              "calc": "2 if proposer == 1 else 1"
            }
          }
        },
        {
          "set": {
            "key": "responder2",
            "value": {
              "calc": "2 if proposer == 3 else 3"
            }
          }
        },
        {
          "set": {
            "players": "all",
            "key": "resp",
            "value": ""
          }
        },
        {
          "set": {
            "key": "response1",
            "value": ""
          }
        },
        {
          "set": {
            "key": "response2",
            "value": ""
          }
        }
      ],
      "text": "Round {round} of {rounds}. Proposer: Seat {proposer}. Responders: Seat {responder1} (first) and Seat {responder2} (second)."
    },
    {
      "use": "update",
      "phase": "draw",
      "label": "the draw",
      "do": [
        {
          "set": {
            "key": "pot",
            "value": {
              "calc": "pots_p1[int(uniform(0, len(pots_p1)))] if proposer == 1 else (pots_p2[int(uniform(0, len(pots_p2)))] if proposer == 2 else pots_p3[int(uniform(0, len(pots_p3)))])"
            }
          }
        },
        {
          "remove": {
            "key": "pots_p1",
            "value": {
              "calc": "pot"
            },
            "if": {
              "calc": "proposer == 1"
            }
          }
        },
        {
          "remove": {
            "key": "pots_p2",
            "value": {
              "calc": "pot"
            },
            "if": {
              "calc": "proposer == 2"
            }
          }
        },
        {
          "remove": {
            "key": "pots_p3",
            "value": {
              "calc": "pot"
            },
            "if": {
              "calc": "proposer == 3"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "draw",
      "label": "the private pot",
      "to": {
        "where": "you.seat == proposer"
      },
      "text": "This round's pot is {pot}."
    },
    {
      "use": "poll",
      "phase": "talk",
      "label": "talk",
      "to": "acting",
      "answer": {
        "type": "text",
        "max_words": 40
      },
      "broadcast": {
        "to": "all",
        "text": "Seat {seat} says: {value}"
      },
      "text": "Write one short message to the table. Everyone writes at the same time; all messages are then shown to everyone. Messages are not binding and may be false."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer for the first responder",
      "to": {
        "where": "you.seat == proposer"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_offer"
        },
        "max": {
          "calc": "max_offer_total"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "offer_a",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You are the Proposer. Choose a whole number a to offer the first Responder, Seat {responder1}: from {min_offer} to {max_offer_total}. a + b may not exceed {max_offer_total}."
    },
    {
      "use": "ask",
      "phase": "offer",
      "label": "offer for the second responder",
      "to": {
        "where": "you.seat == proposer"
      },
      "answer": {
        "type": "number",
        "min": {
          "calc": "min_offer"
        },
        "max": {
          "calc": "max_offer_total - offer_a"
        }
      },
      "each": {
        "do": [
          {
            "set": {
              "key": "offer_b",
              "value": "$answer"
            }
          }
        ]
      },
      "text": "You offered {offer_a} to Seat {responder1}. Choose a whole number b to offer the second Responder, Seat {responder2}: from {min_offer} up to {max_offer_total} minus {offer_a}."
    },
    {
      "use": "tell",
      "phase": "offer",
      "label": "the offer",
      "to": "all",
      "text": "Seat {proposer} offers {offer_a} to Seat {responder1} and {offer_b} to Seat {responder2}."
    },
    {
      "use": "poll",
      "phase": "response",
      "label": "the responses",
      "to": {
        "where": "you.seat == responder1 or you.seat == responder2"
      },
      "answer": {
        "type": "choice",
        "options": [
          "Accept",
          "Reject"
        ]
      },
      "store": "resp",
      "text": "Seat {proposer} offers {offer_a} to Seat {responder1} and {offer_b} to Seat {responder2}. You do not know the pot. Choose Accept or Reject; the other Responder chooses at the same time. If at least one Responder accepts, the deal passes: each accepter gains their offer, a rejecter gains 0, and the Proposer gains the pot minus both offers. If both reject, nobody gains anything this round."
    },
    {
      "use": "update",
      "phase": "scoring",
      "label": "the scoring",
      "do": [
        {
          "set": {
            "key": "response1",
            "value": {
              "calc": "[p.resp for p in players if p.seat == responder1][0]"
            }
          }
        },
        {
          "set": {
            "key": "response2",
            "value": {
              "calc": "[p.resp for p in players if p.seat == responder2][0]"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "proposer"
            },
            "key": "score",
            "value": {
              "calc": "pot - offer_a - offer_b"
            },
            "if": {
              "calc": "response1 == 'Accept' or response2 == 'Accept'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder1"
            },
            "key": "score",
            "value": {
              "calc": "offer_a"
            },
            "if": {
              "calc": "response1 == 'Accept'"
            }
          }
        },
        {
          "adjust": {
            "player": {
              "calc": "responder2"
            },
            "key": "score",
            "value": {
              "calc": "offer_b"
            },
            "if": {
              "calc": "response2 == 'Accept'"
            }
          }
        }
      ]
    },
    {
      "use": "tell",
      "phase": "reveal",
      "label": "the reveal",
      "to": "all",
      "text": "The pot was {pot}. Seat {responder1}: {response1}. Seat {responder2}: {response2}. Scores: P1 {players[0].score}, P2 {players[1].score}, P3 {players[2].score}."
    },
    {
      "use": "check",
      "phase": "reveal",
      "label": "after the last round",
      "when": {
        "calc": "round >= rounds"
      },
      "against": [
        "over"
      ]
    }
  ],
  "end": {
    "over": {
      "when": {
        "calc": "round >= rounds"
      },
      "rank_by": "you.score",
      "text": "Winner: {result}. Final scores: Seat 1 {players[0].score}, Seat 2 {players[1].score}, Seat 3 {players[2].score}."
    }
  },
  "limits": {
    "rounds": 12,
    "rounds_max": 12,
    "actions_max": 400,
    "deadline_s": 120
  },
  "rules": "Three players, P1, P2 and P3 (seats 1, 2 and 3), each start with a score of {initial_score}. Each player has a pot list holding the four values {pot_value_1}, {pot_value_2}, {pot_value_3} and {pot_value_4}. Everyone knows the contents of every list.\n\nThere are {rounds} proposal rounds. The Proposer by round is: rounds 1-3: P1, P2, P3; rounds 4-6: P3, P2, P1; rounds 7-9: P1, P2, P3; rounds 10-12: P3, P2, P1. Each player proposes exactly {proposals_per_player} times. The other two players are that round's Responders; the first Responder is the one with the lower seat number.\n\nEach round:\n1. Draw: one value is drawn at random from the Proposer's remaining pot list and removed from it. This is the pot. Only the Proposer is told it. Because each list loses one value per proposal, every player plays all four values exactly once.\n2. Talk: every player writes one short message at the same time, without seeing the others. Then all three messages are shown to everyone. Messages are not binding and may be false.\n3. Offer: the Proposer announces two whole numbers: a for the first Responder and b for the second. Each must be {min_offer} or more, and a + b must be at most {max_offer_total}. The offer is shown to everyone; the pot is not.\n4. Response: both Responders choose Accept or Reject at the same time, without seeing each other's choice.\n5. Scoring: If at least one Responder accepts, the deal passes. The Proposer gains pot - a - b; if a + b exceeds the pot, this is negative and the Proposer loses points. Each Responder who accepted gains their offered amount. A Responder who rejected gains 0, and their share is destroyed (the Proposer still pays it). If both Responders reject, the deal fails and all three gain 0 this round.\n6. Reveal: the pot, both responses and all three scores are announced.\n\nThe game ends after round {rounds}. The player with the highest total score wins; players tied for the highest total share the result."
}
```
````
