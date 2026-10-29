# Task: write the XColos game file for "Psychological Jujitsu: Hidden Favourites"

Write the game below as one complete game definition for the XColos engine. Reply with ONE JSON object and nothing else.

## The game

Players: 3 to 4; set `meta.players` to {"min": 3, "max": 4, "suggested": 3} (the suggested size is the one the game plays best at).

SETUP: Each player receives a hand of 13 cards valued 1 to 13 (Ace=1 up to King=13). The prize pile holds 13 cards valued 1 to 13 and is shuffled face-down. Each player is then privately told one bonus value, drawn at random without replacement from {5,6,7,8,9}, so no two players share a bonus value. Only that player knows their bonus value. All scores start at 0.

EACH ROUND (13 rounds):
1. The engine reveals the top card of the prize pile as this round's prize. It also announces every player's remaining hand, every current score and the prize values still in the pile.
2. Talk: everyone writes one short message (at most 40 words) at the same time without seeing the others. All messages are then shown to everyone. Messages are not binding and may be false.
3. Bid: everyone secretly chooses one card from their remaining hand at the same time. If a player names a card they do not hold, or gives no valid bid, their lowest remaining card is used.
4. All bids are revealed, and each bid card is removed from its owner's hand permanently.
5. Resolution: any bid value chosen by two or more players is cancelled. The highest bid that is not cancelled wins the prize. If every bid is cancelled, the prize is discarded and nobody scores. Example: bids 10, 10 and 4 give the prize to the player who bid 4.
6. The winner adds the prize's value to their score. If the prize's value equals the winner's secret bonus value, they add 5 more points.
7. The result is announced: all bids, who won the prize (if anyone), and the new scores. When a bonus is scored, the announcement says only '+5 bonus' with the winner's new total, so the bonus value becomes known only through that event.

END: After 13 rounds, all hands and the prize pile are empty. Bonus values are revealed.

How the winner is decided: The player with the highest final score wins. If two or more players tie for the highest score, the game is a draw among them.

## The game as a script

This is the same game written out as a script: its state, how it starts, what happens in each step and how it ends. Convert it into the
file step by step. Every item under STATE becomes a declared attribute (hidden ones too). Every INITIALIZATION line becomes a step in `setup`
that really changes that state. Every EACH ROUND line becomes a step in `steps`, in this order. EVALUATION becomes the `end` rules and the check
that fires them. Do not drop a piece of state because it looks hard: write the steps that make it work.

GAME: Psychological Jujitsu: Hidden Favourites (3 to 4 players, best with 3)

Players secretly bid cards from identical 1-13 hands for 13 prizes. A bid value matched by anyone is cancelled, the highest unique bid wins, and each player has a secret favourite prize value worth +5.

STATE (every item below must exist in the file):
  - each player: hand (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]); everyone sees it. Cards still in this player's hand. The rules announce every hand each round.
  - each player: score (number, starts 0); everyone sees it. Points won from prizes and bonuses
  - each player: bonus (number, starts 0); only its owner sees it. Secret bonus value, dealt at setup from bonus_pool and revealed at game end
  - each player: message (text, starts ''); everyone sees it. This round's talk message
  - each player: bid (number, starts 0); everyone sees it. Card bid this round, revealed once all bids are in
  - each player: bid_unique (bool, starts False); everyone sees it. True when no other player bid the same value this round
  - each player: won_round (bool, starts False); everyone sees it. True when this player won this round's prize
  - each player: bonus_scored (bool, starts False); everyone sees it. True when this player scored the +5 bonus this round
  - the table: prize_pile (list, starts [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]); everyone sees it. Prize values still in the pile. The remaining values are announced; the draw order is random.
  - the table: bonus_pool (list, starts [5, 6, 7, 8, 9]); hidden from all players. Bonus values not yet dealt
  - the table: prize (number, starts 0); everyone sees it. This round's revealed prize value
  - the table: round_no (number, starts 0); everyone sees it. Rounds started so far
  - the table: winning_bid (number, starts 0); everyone sees it. Highest uncancelled bid this round; 0 if every bid was cancelled
  - parameters, each kept as a table attribute: hand_size = 13, card_min = 1, card_max = 13, prize_pile_size = 13, rounds = 13, bonus_value_min = 5, bonus_value_max = 9, bonus_points = 5, message_max_words = 40, starting_score = 0

INITIALIZATION (runs once before round 1; each line is a setup step that really changes the state it names):
  1. Every player's hand is set to the cards 1 to 13, and every score is set to 0.
  2. The prize pile is set to the values 1 to 13.
  3. Each player draws one value at random from bonus_pool into their bonus, and that value is removed from bonus_pool, so no two players share a bonus value.
  4. Each player is privately told their own bonus value.

EACH ROUND (steps in order; the round repeats until an ending):
  1. [update] all players. What happens: round_no += 1. One value is drawn at random from prize_pile into prize and removed from prize_pile. Every player's bid_unique, won_round and bonus_scored are set to false, and winning_bid is set to 0.
  2. [tell] all players. What happens: Announce: 'Round {round_no}: the prize is {prize}.' Also announce every player's hand, every score and the prize_pile values still remaining.
  3. [poll] all players answers: short text, at most 40 words. What happens: Each player's message is set to their text. Then broadcast {"to": "all", "text": "Seat {seat} says: {value}"}. Messages are not binding.
  4. [poll] all players answers: one card from your own hand. What happens: Each player's bid is set to the chosen card. If a player gives an invalid answer or none, bid = the minimum of their hand.
  5. [update] all players. What happens: Each player's bid is removed from their hand. For each player, bid_unique = (number of other players whose bid equals this bid) == 0. winning_bid = the maximum bid among players with bid_unique true, or 0 if no player has bid_unique true. For each player, won_round = bid_unique and bid == winning_bid.
  6. [update] all players. What happens: For the player with won_round true: score += prize, and if prize == bonus, then score += 5 and bonus_scored = true.
  7. [tell] all players. What happens: Announce every player's bid, the winner of the prize (or 'cancelled: nobody scores' if winning_bid == 0) and the new scores. If bonus_scored is true for the winner, announce only '+5 bonus' together with the winner's new total, not the bonus value.
  8. [check] all players. What happens: If round_no == 13, reveal every player's bonus to everyone and end the game. Otherwise continue with the next round.

RULES (each is tested by an independent scenario; the game must play every one exactly):
  R1. At setup, every player's hand is the 13 cards 1 to 13 and every score is 0.
  R2. At setup, each player gets a distinct bonus value drawn from {5,6,7,8,9}, and only that player can see it.
  R3. At the start of each round, one prize value is drawn at random from prize_pile, removed from it and announced, so each value 1 to 13 is a prize exactly once over 13 rounds.
  R4. Each round, every player sends one message of at most 40 words at the same time, and all messages are then shown to everyone.
  R5. Each round, every player secretly bids one card from their own hand at the same time, and no bid is seen until all are in.
  R6. When a player bids a card not in their hand, or gives no valid bid, then the lowest card in their hand is used as their bid.
  R7. After bidding, each player's bid card is removed from their hand permanently.
  R8. When two or more players bid the same value, all of those bids are cancelled.
  R9. The highest uncancelled bid wins the prize: with bids 10, 10 and 4, the player who bid 4 wins.
  R10. When every bid is cancelled (for example bids 7, 7 and 7), the prize is discarded and no score changes.
  R11. The winner adds the prize value to their score: winning a prize of 11 adds 11.
  R12. When the prize value equals the winner's bonus value, the winner adds 5 more: winning prize 7 with bonus 7 adds 12.
  R13. When a bonus is scored, the announcement says '+5 bonus' and the new total, but not the bonus value.
  R14. After round 13 the game ends and every bonus value is revealed.
  R15. The player with the highest final score wins, and players tied for the highest score share the win.

OFFERS (what each seat is offered when it is asked; a seat is never offered what it may not do, and nothing is refused afterwards):
  - Talk message | asked: every seat | options: a short free text of at most 40 words
  - Bid | asked: every seat | options: exactly the cards remaining in that seat's own hand (13 options in round 1, falling by one each round to 1 option in round 13)

EVALUATION (how the game ends and who wins; decided by calculation):
  - the game ends when: round_no == 13
  - each player's standing: you.score (worked out for every player, `you` being that player; the highest wins and players level at the top share the win)
  - how the result is decided: Each player's standing is their final score. The highest score wins, and players tied at the top share the win (a draw among them).
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

- each player: `score` (number, visible: public, starts 0): Points won from prizes and bonuses
- each player: `bid` (number, visible: public, starts 0): Card bid this round, revealed once all bids are in
- the table: `prize` (number, visible: public, starts 0): This round's revealed prize value
- the table: `round_no` (number, visible: public, starts 0): Rounds started so far
- parameters (each must be an attribute holding this value, never a number buried in a step): hand_size = 13, card_min = 1, card_max = 13, prize_pile_size = 13, rounds = 13, bonus_value_min = 5, bonus_value_max = 9, bonus_points = 5, message_max_words = 40, starting_score = 0
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
