# Task: write the XColos game file for "Put: Sixteen Hands"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 2 to 2; set `meta.players` to {"min": 2, "max": 2, "suggested": 2} (the suggested size is the one the game plays best at).

CARDS. Use a deck of 52 cards made of four copies of each value from 1 to 13. Value 13 is a Three (highest), 12 a Two, 11 an Ace, 10 a King, 9 a Queen, 8 a Jack, 7 a Ten, 6 a Nine, 5 an Eight, 4 a Seven, 3 a Six, 2 a Five and 1 a Four (lowest). There are no suits. In any trick the higher value wins, and equal values tie the trick, which then belongs to no one.

SETUP. Both players start with a score of 0. The match is exactly 16 hands. Seat 1 leads in odd-numbered hands and seat 2 leads in even-numbered hands. The other seat is the responder.

EACH HAND, in this order:
1. Reset. Restore and shuffle the full 52-card deck. Clear each player's hand, played card, call, response and trick count, and clear the stake and the folded marker.
2. Deal. Deal 3 cards to each player. Each player sees only their own cards.
3. Lead (leader's choice). The leader chooses one of their 3 cards and plays it face up.
4. Announce the lead to both players.
5. Answer (responder's choice). Having seen the lead, the responder chooses one of their 3 cards and plays it face up.
6. Trick 1. Compare the two cards; the higher wins trick 1 and an equal pair is a tie. Announce the result.
7. Put window (both players at the same moment). Each player privately chooses Put or Check, without seeing the other's choice.
8. Announce both calls.
9. Reply. This step happens only if exactly one player chose Put. The player who chose Check now chooses See or Fold. If both chose Put, the Put counts as seen. If both chose Check, there is no Put. The stake for the hand is 4 if a Put was seen (by See or by both Putting), 1 if both Checked.
10. Fold. If a player folded, the player who Put scores 1 point and the hand ends there; skip to step 15. The remaining cards are not shown.
11. Trick 2. Each player automatically plays the higher of their two remaining cards. Compare them as in trick 1.
12. Trick 3. Each player automatically plays their last card. Compare them as in trick 1.
13. Reveal. Show all cards and each player's number of tricks won.
14. Hand scoring. A player who won at least 2 of the 3 tricks scores the stake (1 or 4). If neither player won 2 tricks, because of tied tricks, no one scores.
15. End check. After hand 16 the match ends; otherwise the next hand begins.

There is no talk phase.

How the winner is decided: After 16 hands, the player with the higher total score wins. If the totals are equal, the match is a draw.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Put: Sixteen Hands (2 to 2 players, best with 2)

A two-player trick-taking bluffing duel over 16 hands. After the first trick, each player may secretly call Put to raise the stake from 1 to 4, and a lone Put can be seen or folded to.

STATE (every item below must exist in the file):
  - each player: score (number, starts 0); everyone sees it. Total points over the match
  - each player: hand (list, starts []); only its owner sees it. The player's unplayed cards, as values 1-13
  - each player: card1 (number, starts 0); everyone sees it. Card played face up to trick 1 (0 = none yet)
  - each player: card2 (number, starts 0); everyone sees it. Card auto-played to trick 2, the higher of the two remaining
  - each player: card3 (number, starts 0); everyone sees it. Card auto-played to trick 3, the last card
  - each player: call (text, starts ''); everyone sees it. Put or Check, chosen secretly in the put window and announced after
  - each player: response (text, starts ''); everyone sees it. See or Fold, given only by the lone Checker when exactly one player Put
  - each player: tricks (number, starts 0); everyone sees it. Tricks won this hand
  - the table: deck (list, starts []); hidden from all players. The undealt cards: four copies of each value 1-13
  - the table: hand_number (number, starts 0); everyone sees it. Number of the current hand, 1 to 16
  - the table: leader (number, starts 1); everyone sees it. Seat that leads this hand: 1 in odd hands, 2 in even hands
  - the table: stake (number, starts 0); everyone sees it. Points the hand is worth: 4 if a Put was seen, 1 if both Checked
  - the table: folded (bool, starts False); everyone sees it. True if the lone Checker folded this hand
  - parameters, each kept as a table attribute: deck_size = 52, copies_per_value = 4, lowest_value = 1, highest_value = 13, hands = 16, cards_dealt_per_player = 3, tricks_per_hand = 3, tricks_needed_to_win_hand = 2, stake_put_seen = 4, stake_both_checked = 1, fold_points = 1, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Both players' score is set to 0.
  2. hand_number is set to 0.
  3. The match will last exactly 16 hands.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: Reset step. hand_number += 1. leader = 1 if hand_number is odd, else 2. deck = four copies of each value 1..13 (52 cards). Each player's hand, card1, card2 and card3 are cleared to empty or 0, call and response to empty text, and tricks to 0. stake = 0 and folded = false.
  2. [update] all players. What happens: Deal step. Each player draws 3 cards at random: each card is removed from deck and appended to that player's hand.
  3. [sync] all players. What happens: Each player privately sees their own hand.
  4. [ask] the leader (seat given by leader) answers: one card value from their hand. What happens: Lead step. leader.card1 = the chosen value; one copy of that value is removed from leader.hand.
  5. [tell] all players. What happens: Announce: 'Hand {hand_number}: Seat {leader} leads {card1}.'
  6. [ask] the responder (the seat that is not leader) answers: one card value from their hand. What happens: Answer step. responder.card1 = the chosen value; one copy of that value is removed from responder.hand.
  7. [update] all players. What happens: Trick 1. If seat1.card1 > seat2.card1, seat1.tricks += 1. If seat2.card1 > seat1.card1, seat2.tricks += 1. If the cards are equal, the trick is a tie and no one's tricks change. The result is announced.
  8. [poll] all players answers: Put or Check. What happens: Put window. Each player's call is set to their answer. Neither player sees the other's call until both have answered.
  9. [tell] all players. What happens: Announce: 'Seat 1 calls {seat1.call}; Seat 2 calls {seat2.call}.'
  10. [ask] the player whose call is Check, only when exactly one player's call is Put answers: See or Fold. What happens: Reply step. That player's response is set to the answer. When both called Put or both called Check, this step is skipped.
  11. [update] all players. What happens: Stake step. If both calls are Put, or one call is Put and the Checker's response is See, then stake = 4. If both calls are Check, then stake = 1. If the Checker's response is Fold, then folded = true.
  12. [update] all players. What happens: Fold scoring, only when folded is true. The player whose call is Put gets score += 1. The remaining cards are not shown.
  13. [update] all players. What happens: Trick 2, only when folded is false. Each player's card2 = the maximum value in their hand, and that card is removed from hand. Compare card2: the higher card gives its owner tricks += 1; equal cards are a tie.
  14. [update] all players. What happens: Trick 3, only when folded is false. Each player's card3 = their last card in hand, and hand becomes empty. Compare card3: the higher card gives its owner tricks += 1; equal cards are a tie.
  15. [tell] all players. What happens: Reveal, only when folded is false. Announce each seat's card1, card2 and card3 and each seat's tricks.
  16. [update] all players. What happens: Hand scoring, only when folded is false. A player with tricks >= 2 gets score += stake. If neither player has tricks >= 2, no one scores.
  17. [check] all players. What happens: End check. If hand_number >= 16, end the match; otherwise the next hand begins.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. When a hand begins, then the deck is restored to 52 cards, four copies of each value 1 to 13, and each player's hand, played cards, call, response and tricks are cleared, along with stake and folded.
  R2. When cards are dealt, then each player receives 3 cards drawn from the deck, and each player sees only their own cards.
  R3. When hand_number is odd, then seat 1 leads; when hand_number is even, then seat 2 leads.
  R4. When the leader leads, then they play one card from their own hand face up, and it is announced before the responder plays.
  R5. When the responder answers, then they play one card from their own hand face up, having seen the lead.
  R6. When a trick is compared, then the higher value wins the trick and adds 1 to its owner's tricks; when the values are equal, then the trick is a tie and no one's tricks change.
  R7. When the put window opens, then both players choose Put or Check simultaneously, without seeing the other's choice, and both calls are then announced.
  R8. When exactly one player calls Put, then the player who called Check chooses See or Fold.
  R9. When both players call Put, or one calls Put and the other Sees, then stake = 4.
  R10. When both players call Check, then there is no Put, no reply is asked, and stake = 1.
  R11. When the Checker folds, then the player who called Put scores 1 point, no further tricks are played, and the remaining cards are not shown.
  R12. When no one folded, then in trick 2 each player automatically plays the higher of their two remaining cards.
  R13. When no one folded, then in trick 3 each player automatically plays their last card.
  R14. When no one folded, then after trick 3 all cards and each player's tricks are revealed.
  R15. When no one folded and a player has won at least 2 of the 3 tricks, then that player's score increases by the stake, 1 or 4.
  R16. When no one folded and neither player has won 2 tricks because of tied tricks, then no one scores that hand.
  R17. When hand 16 has been scored, then the match ends, and the higher total score wins; equal totals are a draw.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Lead: which card to play | asked: the leader (seat 1 in odd hands, seat 2 in even hands) | options: each distinct card value in the leader's 3-card hand
  - Answer: which card to play | asked: the responder (the non-leader) | options: each distinct card value in the responder's 3-card hand
  - Put window | asked: both seats, simultaneously | options: Put, Check
  - Reply to a lone Put | asked: only the seat that called Check, and only when the other seat called Put | options: See, Fold

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: hand_number >= 16
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: After 16 hands, the player with the higher total score wins. Equal totals share the win, which is a draw.
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

- each player: `score` (number, visible: public, starts 0): Total points over the match
- each player: `tricks` (number, visible: public, starts 0): Tricks won this hand
- the table: `hand_number` (number, visible: public, starts 0): Number of the current hand, 1 to 16
- parameters (each must be an attribute holding this value, never a number buried in a step): deck_size = 52, copies_per_value = 4, lowest_value = 1, highest_value = 13, hands = 16, cards_dealt_per_player = 3, tricks_per_hand = 3, tricks_needed_to_win_hand = 2, stake_put_seen = 4, stake_both_checked = 1, fold_points = 1, starting_score = 0
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
